from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import fmt
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__
from tutor.bindmount import iter_mounts
from tutor.hooks import priorities
from tutor.types import Config, get_typed

from .__about__ import __version__
from .commands import mfe_command
from .hooks import (
    EXTERNAL_SCRIPTS,
    FRONTEND_APP_ATTRS_TYPE,
    FRONTEND_APPS,
    FRONTEND_COMPAT_PLUGINS,
    FRONTEND_COMPAT_SLOTS,
    FRONTEND_SLOT_COMPAT_MAPS,
    FRONTEND_SLOTS,
    FRONTEND_WIDGET_COMPAT_MAPS,
    MFE_APPS,
    MFE_ATTRS_TYPE,
    PLUGIN_SLOTS,
)

tutor_hooks.Filters.CLI_COMMANDS.add_item(mfe_command)

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-mfe:{{ MFE_VERSION }}",
        "DOCKER_IMAGE_DEV_PREFIX": "{{ DOCKER_REGISTRY }}overhangio/openedx",
        "HOST": "apps.{{ LMS_HOST }}",
        "COMMON_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "CADDY_DOCKER_IMAGE": "{{ DOCKER_IMAGE_CADDY }}",
        "HOST_EXTRA_FILES": False,
        "SITE_PORT": 8080,
        "SITE_REPOSITORY": "",
        "SITE_VERSION": "",
    },
}

# TODO(legacy-mfe-removal): once all legacy MFEs have been converted to
# frontend-base apps and only the shared site remains, remove the code paths
# supporting legacy MFEs. Grep for `legacy-mfe-removal` to find all sites.
# Broadly, this covers:
#   - The MFE_APPS / PLUGIN_SLOTS filters and their helpers and type aliases
#     (frontend-base ships via FRONTEND_APPS / FRONTEND_SLOTS).
#   - The legacy-MFE targets of EXTERNAL_SCRIPTS (the "site" target stays).
#   - The per-MFE Dockerfile and Caddyfile stages, env.config.jsx,
#     webpack.dev-tutor.config.js, and the per-MFE dev-service compose entries.
#   - The is_mfe_enabled guards and per-MFE URL/flag blocks across patches and
#     templates, plus the mfe-env-config-* / mfe-dockerfile-*-<mfe_name> /
#     mfe-caddyfile patch hook names.
CORE_MFE_APPS: dict[str, MFE_ATTRS_TYPE] = {
    "admin-console": {
        "repository": "https://github.com/openedx/frontend-app-admin-console.git",
        "port": 2025,
    },
    "authn": {
        "repository": "https://github.com/openedx/frontend-app-authn.git",
        "port": 1999,
    },
    "authoring": {
        "repository": "https://github.com/openedx/frontend-app-authoring.git",
        "port": 2001,
    },
    "account": {
        "repository": "https://github.com/openedx/frontend-app-account.git",
        "port": 1997,
    },
    "communications": {
        "repository": "https://github.com/openedx/frontend-app-communications.git",
        "port": 1984,
    },
    "discussions": {
        "repository": "https://github.com/openedx/frontend-app-discussions.git",
        "port": 2002,
    },
    "gradebook": {
        "repository": "https://github.com/openedx/frontend-app-gradebook.git",
        "port": 1994,
    },
    "learner-dashboard": {
        "repository": "https://github.com/openedx/frontend-app-learner-dashboard.git",
        "port": 1996,
    },
    "learning": {
        "repository": "https://github.com/openedx/frontend-app-learning.git",
        "port": 2000,
    },
    "ora-grading": {
        "repository": "https://github.com/openedx/frontend-app-ora-grading.git",
        "port": 1993,
    },
    "profile": {
        "repository": "https://github.com/openedx/frontend-app-profile.git",
        "port": 1995,
    },
    "catalog": {
        "repository": "https://github.com/openedx/frontend-app-catalog.git",
        "port": 1998,
    },
}

CORE_FRONTEND_APPS: dict[str, FRONTEND_APP_ATTRS_TYPE] = {
    "authn": {
        "npm_package": "@openedx/frontend-app-authn",
        "npm_version": "^1.0.0-alpha || 0.0.0-dev",
        "enabled": False,
    },
    "learner-dashboard": {
        "npm_package": "@openedx/frontend-app-learner-dashboard",
        "npm_version": "^1.0.0-alpha || 0.0.0-dev",
        "enabled": False,
    },
    "instructor-dashboard": {
        "npm_package": "@openedx/frontend-app-instructor-dashboard",
        "npm_version": "^1.0.0-alpha || 0.0.0-dev",
        "enabled": True,
    },
    "notifications": {
        "npm_package": "@openedx/frontend-app-notifications",
        "npm_version": "^3.0.0-alpha || 0.0.0-dev",
        "enabled": True,
    },
}


# TODO(legacy-mfe-removal)
# The core MFEs are added with a high priority, such that other users can override or
# remove them.
@MFE_APPS.add(priority=tutor_hooks.priorities.HIGH)
def _add_core_mfe_apps(apps: dict[str, MFE_ATTRS_TYPE]) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(CORE_MFE_APPS)
    return apps


@FRONTEND_APPS.add(priority=tutor_hooks.priorities.HIGH)
def _add_core_frontend_apps(
    apps: dict[str, FRONTEND_APP_ATTRS_TYPE],
) -> dict[str, FRONTEND_APP_ATTRS_TYPE]:
    apps.update(CORE_FRONTEND_APPS)
    return apps


# TODO(legacy-mfe-removal)
@tutor_hooks.lru_cache
def get_mfes() -> dict[str, MFE_ATTRS_TYPE]:
    """
    This function is cached for performance.
    """
    return MFE_APPS.apply({})


@tutor_hooks.lru_cache
def get_frontend_apps() -> dict[str, FRONTEND_APP_ATTRS_TYPE]:
    """
    This function is cached for performance.
    """
    return FRONTEND_APPS.apply({})


# TODO(legacy-mfe-removal)
class MFEMountData:
    """Stores categorized mounted and unmounted MFEs."""

    def __init__(self, mounts: list[str]):
        self.mounted: list[tuple[str, MFE_ATTRS_TYPE, list[str]]] = []
        self.unmounted: list[tuple[str, MFE_ATTRS_TYPE]] = []
        self._categorize_mfes(mounts)

    def _categorize_mfes(self, mounts: list[str]) -> None:
        """Populates mounted and unmounted MFE lists based on mount data."""
        for app_name, app in iter_mfes():
            mfe_mounts = list(iter_mounts(mounts, app_name))
            if mfe_mounts:
                self.mounted.append((app_name, app, mfe_mounts))
            else:
                self.unmounted.append((app_name, app))


def get_site_mounts(mounts: list[str]) -> list[str]:
    return list(iter_mounts(mounts, SITE_MOUNT_NAME))


# TODO(legacy-mfe-removal): get_plugin_slots / iter_plugin_slots
@tutor_hooks.lru_cache
def get_plugin_slots(mfe_name: str) -> list[tuple[str, str]]:
    """
    This function is cached for performance.
    """
    return [i[-2:] for i in PLUGIN_SLOTS.iterate() if i[0] == mfe_name]


@tutor_hooks.lru_cache
def get_external_scripts(mfe_name: str) -> list[str]:
    """
    This function is cached for performance.
    """
    return [i[-1] for i in EXTERNAL_SCRIPTS.iterate() if i[0] == mfe_name]


@tutor_hooks.lru_cache
def get_frontend_slots() -> list[str]:
    return FRONTEND_SLOTS.apply([])


# TODO(fpf-removal): get_frontend_compat_slots and iter_frontend_compat_slots
# exist to render env.config.compat.jsx, which serves frontend-base sites
# running the frontend-base compatibility shim (@openedx/frontend-base-compat).
# When FPF deprecation completes and no plugin contributes via
# FRONTEND_COMPAT_SLOTS or FRONTEND_COMPAT_PLUGINS, these helpers and the
# compat template can be removed.
@tutor_hooks.lru_cache
def get_frontend_compat_slots() -> list[tuple[str, str]]:
    """
    Yield (slot_name, plugin_config) pairs.

    Sourced from two filters:

    - FRONTEND_COMPAT_PLUGINS: bulk opt-ins by plugin name.  Every PLUGIN_SLOTS
      contribution registered in that plugin's hook context is folded in,
      regardless of which legacy MFE it targeted.
    - FRONTEND_COMPAT_SLOTS: per-slot opt-ins.  The plugin author lists registers
      each slot they want rendered through the shim.

    Dedup collapses identical (slot_name, plugin_config) pairs across both
    sources, so opting a plugin in by name and then re-opting one of its slots
    individually is a safe no-op.
    """
    seen: set[tuple[str, str]] = set()
    flattened: list[tuple[str, str]] = []

    def _record(slot_name: str, plugin_config: str) -> None:
        key = (slot_name, plugin_config)
        if key in seen:
            return
        seen.add(key)
        flattened.append(key)

    for plugin_name in FRONTEND_COMPAT_PLUGINS.iterate():
        context = tutor_hooks.Contexts.app(plugin_name).name
        for _mfe_name, slot_name, plugin_config in PLUGIN_SLOTS.iterate_from_context(
            context
        ):
            _record(slot_name, plugin_config)

    for slot_name, plugin_config in FRONTEND_COMPAT_SLOTS.iterate():
        _record(slot_name, plugin_config)

    return flattened


@tutor_hooks.lru_cache
def get_frontend_slot_compat_map() -> dict[str, dict[str, t.Any]]:
    return _merge_frontend_compat_maps(FRONTEND_SLOT_COMPAT_MAPS.iterate(), kind="slot")


@tutor_hooks.lru_cache
def get_frontend_widget_compat_map() -> dict[str, dict[str, t.Any]]:
    return _merge_frontend_compat_maps(
        FRONTEND_WIDGET_COMPAT_MAPS.iterate(), kind="widget"
    )


def _merge_frontend_compat_maps(
    extensions: t.Iterable[tuple[str, dict[str, t.Any]]],
    kind: str,
) -> dict[str, dict[str, t.Any]]:
    """
    Identical contributions dedup silently. Divergent ones warn and
    last-wins so a transient conflict during a plugin upgrade still
    produces a working bundle.
    """
    merged: dict[str, dict[str, t.Any]] = {}
    for legacy_id, mapping in extensions:
        existing = merged.get(legacy_id)
        if existing is None:
            merged[legacy_id] = mapping
            continue
        if existing == mapping:
            continue
        fmt.echo_alert(
            f"Conflicting compat {kind}-map extensions for {legacy_id!r}: "
            f"{existing!r} overridden by {mapping!r}. "
            "Last contribution wins; consider removing one of the plugins "
            "or aligning their compat-map contributions."
        )
        merged[legacy_id] = mapping
    return merged


# TODO(legacy-mfe-removal)
def iter_mfes() -> t.Iterable[tuple[str, MFE_ATTRS_TYPE]]:
    """
    Yield:

        (name, dict)
    """
    yield from get_mfes().items()


def iter_frontend_apps() -> t.Iterable[tuple[str, FRONTEND_APP_ATTRS_TYPE]]:
    yield from get_frontend_apps().items()


# TODO(legacy-mfe-removal)
def iter_legacy_paths() -> t.Iterable[str]:
    """
    Yield MFE names that are not superseded by an enabled frontend app.
    """
    for name, _attrs in iter_mfes():
        if not is_frontend_app_enabled(name):
            yield name


def iter_plugin_slots(mfe_name: str) -> t.Iterable[tuple[str, str]]:
    """
    Yield:

        (slot_name, plugin_config)
    """
    yield from get_plugin_slots(mfe_name)


def iter_frontend_compat_slots() -> t.Iterable[tuple[str, str]]:
    yield from get_frontend_compat_slots()


def iter_external_scripts(mfe_name: str) -> t.Iterable[str]:
    """
    Yield:

        (script_config)
    """
    yield from get_external_scripts(mfe_name)


def iter_frontend_slots() -> t.Iterable[str]:
    yield from get_frontend_slots()


# TODO(legacy-mfe-removal)
def is_mfe_enabled(mfe_name: str) -> bool:
    return mfe_name in get_mfes()


def is_frontend_app_enabled(app_name: str) -> bool:
    """
    Returns True if the frontend app is configured and has enabled=True.
    """
    return bool(get_frontend_app(app_name).get("enabled", False))


# TODO(legacy-mfe-removal)
def get_mfe(mfe_name: str) -> t.Union[MFE_ATTRS_TYPE, t.Any]:
    return get_mfes().get(mfe_name, {})


def get_frontend_app(app_name: str) -> t.Union[FRONTEND_APP_ATTRS_TYPE, t.Any]:
    """
    Returns the attributes of a configured frontend app.
    """
    return get_frontend_apps().get(app_name, {})


# Make the mfe functions available within templates
tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [
        # TODO(legacy-mfe-removal): get_mfe, iter_mfes, iter_legacy_paths,
        # iter_plugin_slots, is_mfe_enabled, MFEMountData
        ("get_mfe", get_mfe),
        ("iter_mfes", iter_mfes),
        ("iter_legacy_paths", iter_legacy_paths),
        ("iter_frontend_apps", iter_frontend_apps),
        ("get_frontend_app", get_frontend_app),
        ("get_frontend_apps", get_frontend_apps),
        ("iter_plugin_slots", iter_plugin_slots),
        ("iter_frontend_compat_slots", iter_frontend_compat_slots),
        ("iter_external_scripts", iter_external_scripts),
        ("get_frontend_compat_slots", get_frontend_compat_slots),
        ("get_frontend_slot_compat_map", get_frontend_slot_compat_map),
        ("get_frontend_widget_compat_map", get_frontend_widget_compat_map),
        ("iter_frontend_slots", iter_frontend_slots),
        ("is_mfe_enabled", is_mfe_enabled),
        ("is_frontend_app_enabled", is_frontend_app_enabled),
        ("MFEMountData", MFEMountData),
        ("get_site_mounts", get_site_mounts),
    ]
)


# Build, pull and push mfe base image
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "mfe",
        os.path.join("plugins", "mfe", "build", "mfe"),
        "{{ MFE_DOCKER_IMAGE }}",
        (),
    )
)
tutor_hooks.Filters.IMAGES_PULL.add_item(
    (
        "mfe",
        "{{ MFE_DOCKER_IMAGE }}",
    )
)
tutor_hooks.Filters.IMAGES_PUSH.add_item(
    (
        "mfe",
        "{{ MFE_DOCKER_IMAGE }}",
    )
)


# TODO(legacy-mfe-removal)
# Build, pull and push {mfe}-dev images
@tutor_hooks.Actions.PLUGINS_LOADED.add()
def _mounted_mfe_image_management() -> None:
    for mfe_name, _mfe_attrs in iter_mfes():
        name = f"{mfe_name}-dev"
        tag = "{{ MFE_DOCKER_IMAGE_DEV_PREFIX }}-" + name + ":{{ MFE_VERSION }}"
        tutor_hooks.Filters.IMAGES_BUILD.add_item(
            (
                name,
                os.path.join("plugins", "mfe", "build", "mfe"),
                tag,
                (f"--target={mfe_name}-dev",),
            )
        )
        tutor_hooks.Filters.IMAGES_PULL.add_item((name, tag))
        tutor_hooks.Filters.IMAGES_PUSH.add_item((name, tag))


# Build, pull and push mfe-dev image
@tutor_hooks.Actions.PLUGINS_LOADED.add()
def _site_image_management() -> None:
    if get_frontend_apps():
        name = "mfe-dev"
        tag = "{{ MFE_DOCKER_IMAGE_DEV_PREFIX }}-" + name + ":{{ MFE_VERSION }}"
        tutor_hooks.Filters.IMAGES_BUILD.add_item(
            (
                name,
                os.path.join("plugins", "mfe", "build", "mfe"),
                tag,
                ("--target=mfe-dev",),
            )
        )
        tutor_hooks.Filters.IMAGES_PULL.add_item((name, tag))
        tutor_hooks.Filters.IMAGES_PUSH.add_item((name, tag))


# init script
with open(
    os.path.join(
        str(
            importlib_resources.files("tutormfe")
            / "templates"
            / "mfe"
            / "tasks"
            / "lms"
            / "init"
        )
    ),
    encoding="utf-8",
) as task_file:
    tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(("lms", task_file.read()))

REPO_PREFIX = "frontend-app-"
SITE_MOUNT_NAME = "frontend-site"


@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_frontend_apps(
    volumes: list[tuple[str, str]], path_basename: str
) -> list[tuple[str, str]]:
    """
    If the user mounts any repo named frontend-app-APPNAME, then make sure
    it's available in the appropriate dev service container: the shared
    frontend-site service for frontend-base apps, or the per-app APPNAME
    service for legacy MFEs.
    """
    if path_basename.startswith(REPO_PREFIX):
        app_name = path_basename[len(REPO_PREFIX) :]
        # frontend-base apps are mounted as workspace packages in the shared
        # frontend-site service, while legacy MFEs each have their own
        # dedicated service named after the app.
        if is_frontend_app_enabled(app_name):
            container_path = f"/openedx/site/packages/frontend-app-{app_name}"
            volumes += [(SITE_MOUNT_NAME, container_path)]
        # TODO(legacy-mfe-removal): drop the elif branch
        elif is_mfe_enabled(app_name):
            volumes += [(app_name, "/openedx/app")]
    return volumes


@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_site(
    volumes: list[tuple[str, str]], path_basename: str
) -> list[tuple[str, str]]:
    """
    If the user mounts a directory named SITE_MOUNT_NAME, make it available
    in the site dev service container at /openedx/site.
    """
    if path_basename == SITE_MOUNT_NAME:
        volumes += [(SITE_MOUNT_NAME, "/openedx/site")]
    return volumes


@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_frontend_apps_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename.startswith(REPO_PREFIX):
        # Bind-mount repo at build-time, both for prod and dev images.
        # frontend-base apps target the shared mfe/mfe-dev images, while
        # legacy MFEs target their own per-app dev image.
        app_name = path_basename[len(REPO_PREFIX) :]
        if is_frontend_app_enabled(app_name):
            mounts.append(("mfe", f"frontend-app-{app_name}-src"))
            mounts.append(("mfe-dev", f"frontend-app-{app_name}-src"))
        # TODO(legacy-mfe-removal): drop the elif branch
        elif is_mfe_enabled(app_name):
            mounts.append(("mfe", f"{app_name}-src"))
            mounts.append((f"{app_name}-dev", f"{app_name}-src"))
    return mounts


@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_site_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == SITE_MOUNT_NAME:
        # Bind-mount site at build-time, both for prod and dev images
        mounts.append(("mfe", "site-src"))
        mounts.append(("mfe-dev", "site-src"))
    return mounts


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_mfe_public_hosts(
    hostnames: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "local":
        hostnames.append("{{ MFE_HOST }}")
    else:
        # TODO(legacy-mfe-removal): drop the iter_mfes loop
        for mfe_name, mfe_attrs in iter_mfes():
            hostnames.append("{{ MFE_HOST }}" + f":{mfe_attrs['port']}/{mfe_name}")
        if get_frontend_apps():
            hostnames.append("{{ MFE_HOST }}:{{ MFE_SITE_PORT }}")
    return hostnames


@tutor_hooks.Filters.IMAGES_BUILD_REQUIRED.add()
def _build_3rd_party_dev_mfes_on_launch(
    image_names: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if __version_suffix__:
        # Build mfe image in main mode
        image_names.append("mfe")

    # TODO(legacy-mfe-removal): drop the iter_mfes loop
    for mfe_name, _mfe_attrs in iter_mfes():
        if __version_suffix__ or (
            context_name == "dev" and mfe_name not in CORE_MFE_APPS
        ):
            # We build MFE images:
            # - in main
            # - in development for non-core apps
            image_names.append(f"{mfe_name}-dev")
    if get_frontend_apps():
        if __version_suffix__ or context_name == "dev":
            image_names.append("mfe-dev")
    return image_names


# Boilerplate code
# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutormfe") / "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("mfe/build", "plugins"),
        ("mfe/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(str(importlib_resources.files("tutormfe") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        # Here we force tutor-mfe lms patches to be loaded first, thus ensuring when
        # operators override MFE_CONFIG and/or MFE_CONFIG_OVERRIDES, their patches
        # will be loaded after this plugin's
        patch_name = os.path.basename(path)
        priority = (
            priorities.HIGH
            if patch_name
            in ["openedx-lms-production-settings", "openedx-lms-development-settings"]
            else priorities.DEFAULT
        )
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (patch_name, patch_file.read()), priority=priority
        )

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"MFE_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"MFE_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("NOTIFICATIONS_DEFAULT_FROM_EMAIL", "{{ CONTACT_EMAIL }}"),
    ]
)


# Actions
@tutor_hooks.Actions.CONFIG_LOADED.add()
def _check_mfe_host(config: Config) -> None:
    """
    This will check if the MFE_HOST is a subdomain of LMS_HOST.
    if not, prints a warning to notify the user.
    """

    lms_host = get_typed(config, "LMS_HOST", str, "")
    mfe_host = get_typed(config, "MFE_HOST", str, "")
    if not mfe_host.endswith("." + lms_host):
        fmt.echo_alert(
            f'Warning: MFE_HOST="{mfe_host}" is not a subdomain of '
            f'LMS_HOST="{lms_host}". '
            "This configuration is not typically recommended and may lead "
            "to unexpected behavior."
        )
