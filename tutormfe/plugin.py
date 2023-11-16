from __future__ import annotations

import os
import typing as t
from glob import glob

import pkg_resources
from tutor import fmt
from tutor import hooks as tutor_hooks
from tutor.hooks import priorities
from tutor.types import Config, get_typed

from .__about__ import __version__, __version_suffix__
from .hooks import MFE_APPS, MFE_ATTRS_TYPE

config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-mfe:{{ MFE_VERSION }}",
        "HOST": "apps.{{ LMS_HOST }}",
        "COMMON_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "CADDY_DOCKER_IMAGE": "{{ DOCKER_IMAGE_CADDY }}",
    },
}


def get_github_refs_path(name: str) -> str:
    """
    Generate a URL to access refs in heads (nightly) or tags (stable) via Github API.
    Args:
        name (str): Consisted of the repository owner and the repository name, as a string in 'owner/repo' format.

    Returns:
        str: A string URL to the Github API, pointing to heads if version_suffix is set, tags otherwise.

    """

    return f"https://api.github.com/repos/{name}/git/refs/{'heads' if __version_suffix__ else 'tags'}"


CORE_MFE_APPS: dict[str, MFE_ATTRS_TYPE] = {
    "authn": {
        "repository": "https://github.com/openedx/frontend-app-authn",
        "refs": get_github_refs_path("openedx/frontend-app-authn"),
        "port": 1999,
    },
    "account": {
        "repository": "https://github.com/openedx/frontend-app-account",
        "refs": get_github_refs_path("openedx/frontend-app-account"),
        "port": 1997,
    },
    "communications": {
        "repository": "https://github.com/openedx/frontend-app-communications",
        "refs": get_github_refs_path("openedx/frontend-app-communications"),
        "port": 1984,
    },
    "course-authoring": {
        "repository": "https://github.com/openedx/frontend-app-course-authoring",
        "refs": get_github_refs_path("openedx/frontend-app-course-authoring"),
        "port": 2001,
    },
    "discussions": {
        "repository": "https://github.com/openedx/frontend-app-discussions",
        "refs": get_github_refs_path("openedx/frontend-app-discussions"),
        "port": 2002,
    },
    "gradebook": {
        "repository": "https://github.com/openedx/frontend-app-gradebook",
        "refs": get_github_refs_path("openedx/frontend-app-gradebook"),
        "port": 1994,
    },
    "learner-dashboard": {
        "repository": "https://github.com/openedx/frontend-app-learner-dashboard",
        "refs": get_github_refs_path("openedx/frontend-app-learner-dashboard"),
        "port": 1996,
    },
    "learning": {
        "repository": "https://github.com/openedx/frontend-app-learning",
        "refs": get_github_refs_path("openedx/frontend-app-learning"),
        "port": 2000,
    },
    "ora-grading": {
        "repository": "https://github.com/openedx/frontend-app-ora-grading",
        "refs": get_github_refs_path("openedx/frontend-app-ora-grading"),
        "port": 1993,
    },
    "profile": {
        "repository": "https://github.com/openedx/frontend-app-profile",
        "refs": get_github_refs_path("openedx/frontend-app-profile"),
        "port": 1995,
    },
}


# The core MFEs are added with a high priority, such that other users can override or
# remove them.
@MFE_APPS.add(priority=tutor_hooks.priorities.HIGH)
def _add_core_mfe_apps(apps: dict[str, MFE_ATTRS_TYPE]) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(CORE_MFE_APPS)
    return apps


def iter_mfes() -> t.Iterable[tuple[str, MFE_ATTRS_TYPE]]:
    """
    Yield:

        (name, dict)
    """
    yield from MFE_APPS.apply({}).items()


def is_mfe_enabled(mfe_name: str) -> bool:
    return mfe_name in MFE_APPS.apply({})


# Make the mfe functions available within templates
tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [("iter_mfes", iter_mfes), ("is_mfe_enabled", is_mfe_enabled)]
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
for mfe_name, mfe_attrs in iter_mfes():
    name = f"{mfe_name}-dev"
    tag = "{{ DOCKER_REGISTRY }}overhangio/openedx-" + name + ":{{ MFE_VERSION }}"
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
        pkg_resources.resource_filename("tutormfe", "templates"),
        "mfe",
        "tasks",
        "lms",
        "init",
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
    for mfe_name, _mfe_attrs in iter_mfes():
        if __version_suffix__ or (context_name == "dev" and mfe_name not in CORE_MFE_APPS):
            # We build MFE images:
            # - in nightly
            # - in development for non-core apps
            image_names.append(f"{mfe_name}-dev")
    return image_names


# Boilerplate code
# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutormfe", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("mfe/build", "plugins"),
        ("mfe/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutormfe", "patches"),
        "*",
    )
):
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
