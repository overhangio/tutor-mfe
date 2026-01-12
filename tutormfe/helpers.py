import os

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from tutor import hooks

from .hooks import PLUGIN_SLOTS


class SlotOp(str, Enum):
    """Enum of supported `op` values in a slot configuration."""

    INSERT = "Insert"
    MODIFY = "Modify"
    WRAP = "Wrap"
    HIDE = "Hide"


class PluginType(str, Enum):
    """Enum of support frontend plugin types."""

    DIRECT = "DIRECT_PLUGIN"
    IFRAME = "IFRAME_PLUGIN"


@dataclass
class SlotConfig:
    """Configurations for frontend plugin slots."""

    mfe: str | list[str] | Literal["all"]
    """Name of the MFE(s). Specify `all` for configuring a specific slot in all the
    MFEs."""

    slot_id: str
    """Plugin slot's ID."""

    component: str = field(default="")
    """The component to be used in the slot. Only components imported from NPM packages
    are supported. Custom functions & inline React components declarations are not
    supported.
    """

    op: SlotOp = field(default=SlotOp.INSERT)
    """Plugin operation. Defaults to `Insert`."""

    widget_id: str = field(default="")
    """OPTIONAL. Widget's ID. This is auto-generated if not specified.
    Use `default_contents` to change behaviour of default contents of the slot.
    """

    plugin_type: PluginType = field(default=PluginType.DIRECT)
    """OPTIONAL. The plugin's type. Defaults to `DIRECT_PLUGIN`."""

    priority: int = field(default=50)
    """OPTIONAL. Priority deciding the position of the widget. Range of 1-100."""

    url: str = field(default="")
    """OPTIONAL. URL for the Iframe, when an IFRAME_PLUGIN is used."""

    title: str = field(default="")
    """OPTIONAL. Title for the Iframe, when an IFRAME_PLUGIN is used."""


@dataclass
class FrontendPlugin:
    """Helper class for defining the necessary configuration for a frontned plugin.

    A typical Tutor plugin for setting up a frontend plugin in MFE slots require:
        * A Dockerfile patch to install the frontend plugin's NPM package
        * A build-time import patch
        * Slot configurations mapping components to slots

    This helper class provides a way to define all 3 in a single declaration.

    For example, a Tutor plugin with the following declaration will setup the
    necessary patches and configuration mentioned above. Additionally, it would
    also mount the frontend plugin's directory correctly for development (tutor dev)
    with hot-reloading.

        FrontendPlugin(
            package="my-package",
            package_url="https://github.com/user/my-package",
            local_path="/home/user/path/to/my-package",
            slots=[...],
        ).register()

    """

    package: str
    """The NPM package name."""

    package_url: str = field(default="")
    """OPTIONAL. Location of the plugin's package if it is not in NPM default registry.
    """

    local_path: str = field(default="")
    """OPTIONAL. Absolute path to the local directory. Needed when developing a plugin
    locally. Ignored in other contexts"""

    slots: list[SlotConfig] = field(default_factory=list)
    """List of slot configuration that the plugin is filling in."""

    def _patch_npm_install(self) -> None:
        """
        Add the "mfe-dockerfile-post-npm-install" patch for the package
        """
        package = self.package
        if self.package_url:
            package = self.package_url

        # NOTE: Installing plugin packages just for a specific MFE isn't supported yet
        # as that requires runtime definitions and results silent failures - harder to
        # debug.
        patch = "mfe-dockerfile-post-npm-install"
        hooks.Filters.ENV_PATCHES.add_item((patch, f"RUN npm install {package}"))

    def _patch_mfe_buildtime_imports(self) -> None:
        """
        Adds the "mfe-env-config-buildtime-imports" patch for the component imports.

        This is only added when slots are configured to be included in "all" the MFEs.
        """
        components = ", ".join(set(s.component for s in self.slots if s.component))

        hooks.Filters.ENV_PATCHES.add_item(
            (
                "mfe-env-config-buildtime-imports",
                f"""
import {{ {components} }} from '{self.package}';
""",
            )
        )

    @staticmethod
    def _slot_config_object(slot: SlotConfig) -> str:
        if slot.op == SlotOp.HIDE:
            return f"""{{
            op: PLUGIN_OPERATIONS.Hide,
            widgetId: '{slot.widget_id}',
            }}"""
        elif slot.op == SlotOp.WRAP:
            return "// TODO - implement support for PLUGIN_OPERATIONS.Wrap"
        elif slot.op == SlotOp.MODIFY:
            return "// TODO - implement support for PLUGIN_OPERATIONS.Modify"

        w_id = slot.widget_id or f"{slot.slot_id.replace('.', '_')}_{slot.component}"

        if slot.plugin_type == PluginType.DIRECT:
            if not slot.component:
                raise ValueError(
                    "Parameter `component` missing for DIRECT_PLUGIN in slot "
                    f"`{slot.slot_id}`."
                )
            widget = f"""{{
                id: '{w_id}',
                type: DIRECT_PLUGIN,
                priority: {slot.priority},
                RenderWidget: {slot.component},
            }}"""
        else:  # IFRAME_PLUGIN
            widget = f"""{{
                id: '{w_id}',
                type: IFRAME_PLUGIN,
                priority: {slot.priority},
                url: {slot.url},
                title: {slot.title},
            }}"""

        return f"""{{
            op: PLUGIN_OPERATIONS.Insert,
            widget: {widget}
        }}"""

    def _add_plugin_slot_configs(self) -> None:
        """Adds all the necessary plugin slot configurations."""
        # {mfe: {slot_id: [configs...]}}
        slot_configs: dict[str, dict[str, list[str]]] = {}
        for slot in self.slots:
            # Support for specifying multiple mfes in a single slot config
            mfes = slot.mfe
            if isinstance(slot.mfe, str):
                mfes = [slot.mfe]

            for mfe in mfes:
                slot_config = self._slot_config_object(slot)
                if mfe not in slot_configs:
                    slot_configs[mfe] = {slot.slot_id: [slot_config]}
                else:
                    slot_configs[mfe][slot.slot_id].append(slot_config)

        for mfe in slot_configs:
            for slot_id in slot_configs[mfe]:
                PLUGIN_SLOTS.add_item(
                    (mfe, slot_id, ",".join(slot_configs[mfe][slot_id]))
                )

    def _setup_dev_mounts(self):
        """Setup the necessary mounts for developing the plugin"""
        if not self.local_path:
            return

        if not os.path.exists(self.local_path):
            raise ValueError(f"Plugin repo doesn't exist in local_path={self.local_path}")

    def register(self) -> None:
        """Generates Registers the necessary patches."""
        self._patch_npm_install()
        self._patch_mfe_buildtime_imports()
        self._add_plugin_slot_configs()
        self._setup_dev_mounts()
