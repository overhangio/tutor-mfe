from __future__ import annotations

import functools
import os
import typing as t
from glob import glob

import importlib_resources
from tutor import fmt
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__
from tutor.hooks import priorities
from tutor.types import Config, get_typed

from .__about__ import __version__
from .hooks import MFE_APPS, MFE_ATTRS_TYPE, PLUGIN_SLOTS

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
    },
}

CORE_MFE_APPS: dict[str, MFE_ATTRS_TYPE] = {
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
}


# The core MFEs are added with a high priority, such that other users can override or
# remove them.
@MFE_APPS.add(priority=tutor_hooks.priorities.HIGH)
def _add_core_mfe_apps(apps: dict[str, MFE_ATTRS_TYPE]) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(CORE_MFE_APPS)
    return apps


@tutor_hooks.lru_cache
def get_mfes() -> dict[str, MFE_ATTRS_TYPE]:
    """
    This function is cached for performance.
    """
    return MFE_APPS.apply({})


@tutor_hooks.lru_cache
def get_plugin_slots(mfe_name: str) -> list[tuple[str, str]]:
    """
    This function is cached for performance.
    """
    return [i[-2:] for i in PLUGIN_SLOTS.iterate() if i[0] == mfe_name]


def iter_mfes() -> t.Iterable[tuple[str, MFE_ATTRS_TYPE]]:
    """
    Yield:

        (name, dict)
    """
    yield from get_mfes().items()


def iter_plugin_slots(mfe_name: str) -> t.Iterable[tuple[str, str]]:
    """
    Yield:

        (slot_name, plugin_config)
    """
    yield from get_plugin_slots(mfe_name)


def is_mfe_enabled(mfe_name: str) -> bool:
    return mfe_name in get_mfes()


def get_mfe(mfe_name: str) -> t.Union[MFE_ATTRS_TYPE, t.Any]:
    return get_mfes().get(mfe_name, {})


# Make the mfe functions available within templates
tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [
        ("get_mfe", get_mfe),
        ("iter_mfes", iter_mfes),
        ("iter_plugin_slots", iter_plugin_slots),
        ("is_mfe_enabled", is_mfe_enabled),
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


@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_frontend_apps(
    volumes: list[tuple[str, str]], path_basename: str
) -> list[tuple[str, str]]:
    """
    If the user mounts any repo named frontend-app-APPNAME, then make sure
    it's available in the APPNAME service container. This is only applicable
    in dev mode, because in production, all MFEs are built and hosted on the
    singular 'mfe' service container.
    """
    if path_basename.startswith(REPO_PREFIX):
        # Assumption:
        # For each repo named frontend-app-APPNAME, there is an associated
        # docker-compose service named APPNAME. If this assumption is broken,
        # then Tutor will try to mount the repo in a service that doesn't exist.
        app_name = path_basename[len(REPO_PREFIX) :]
        volumes += [(app_name, "/openedx/app")]
    return volumes


@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_frontend_apps_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename.startswith(REPO_PREFIX):
        # Bind-mount repo at build-time, both for prod and dev images
        app_name = path_basename[len(REPO_PREFIX) :]
        mounts.append(("mfe", f"{app_name}-src"))
        mounts.append((f"{app_name}-dev", f"{app_name}-src"))
    return mounts


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_mfe_public_hosts(
    hostnames: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "local":
        hostnames.append("{{ MFE_HOST }}")
    else:
        for mfe_name, mfe_attrs in iter_mfes():
            hostnames.append("{{ MFE_HOST }}" + f":{mfe_attrs['port']}/{mfe_name}")
    return hostnames


@tutor_hooks.Filters.IMAGES_BUILD_REQUIRED.add()
def _build_3rd_party_dev_mfes_on_launch(
    image_names: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if __version_suffix__:
        # Build mfe image in main mode
        image_names.append("mfe")

    for mfe_name, _mfe_attrs in iter_mfes():
        if __version_suffix__ or (
            context_name == "dev" and mfe_name not in CORE_MFE_APPS
        ):
            # We build MFE images:
            # - in main
            # - in development for non-core apps
            image_names.append(f"{mfe_name}-dev")
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
        # Here we force tutor-mfe lms patches to be loaded first, thus ensuring when operators override
        # MFE_CONFIG and/or MFE_CONFIG_OVERRIDES, their patches will be loaded after this plugin's
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
            f'Warning: MFE_HOST="{mfe_host}" is not a subdomain of LMS_HOST="{lms_host}". '
            "This configuration is not typically recommended and may lead to unexpected behavior."
        )
