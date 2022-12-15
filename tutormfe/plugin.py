from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks
from tutor.hooks import priorities

from .__about__ import __version__

config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-mfe:{{ MFE_VERSION }}",
        "HOST": "apps.{{ LMS_HOST }}",
        "COMMON_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "CADDY_DOCKER_IMAGE": "{{ DOCKER_IMAGE_CADDY }}",
        "AUTHN_MFE_APP": {
            "name": "authn",
            "repository": "https://github.com/openedx/frontend-app-authn",
            "port": 1999,
        },
        "ACCOUNT_MFE_APP": {
            "name": "account",
            "repository": "https://github.com/openedx/frontend-app-account",
            "port": 1997,
        },
        "COURSE_AUTHORING_MFE_APP": {
            "name": "course-authoring",
            "repository": "https://github.com/openedx/frontend-app-course-authoring",
            "port": 2001,
        },
        "DISCUSSIONS_MFE_APP": {
            "name": "discussions",
            "repository": "https://github.com/openedx/frontend-app-discussions",
            "port": 2002,
        },
        "GRADEBOOK_MFE_APP": {
            "name": "gradebook",
            "repository": "https://github.com/openedx/frontend-app-gradebook",
            "port": 1994,
        },
        "LEARNING_MFE_APP": {
            "name": "learning",
            "repository": "https://github.com/openedx/frontend-app-learning",
            "port": 2000,
        },
        "PROFILE_MFE_APP": {
            "name": "profile",
            "repository": "https://github.com/openedx/frontend-app-profile",
            "port": 1995,
        },
    },
}
ALL_MFES = (
    "account",
    "course-authoring",
    "discussions",
    "authn",
    "gradebook",
    "learning",
    "profile",
)

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

# Build, pull and push mfe base image
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "mfe",
        ("plugins", "mfe", "build", "mfe"),
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
def mfe_dev_docker_image(mfe: str) -> str:
    return "{{ DOCKER_REGISTRY }}overhangio/openedx-" + mfe + "-dev:{{ MFE_VERSION }}"


tutor_hooks.Filters.ENV_TEMPLATE_FILTERS.add_item(
    ("mfe_dev_docker_image", mfe_dev_docker_image)
)

for mfe in ALL_MFES:
    name = f"{mfe}-dev"
    tag = mfe_dev_docker_image(mfe)
    tutor_hooks.Filters.IMAGES_BUILD.add_item(
        (
            name,
            ("plugins", "mfe", "build", "mfe"),
            tag,
            (f"--target={mfe}-dev",),
        )
    )
    tutor_hooks.Filters.IMAGES_PULL.add_item((name, tag))
    tutor_hooks.Filters.IMAGES_PUSH.add_item((name, tag))


@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_frontend_apps(volumes, name):
    """
    If the user mounts any repo named frontend-app-APPNAME, then make sure
    it's available in the APPNAME service container. This is only applicable
    in dev mode, because in production, all MFEs are built and hosted on the
    singular 'mfe' service container.
    """
    prefix = "frontend-app-"
    if name.startswith(prefix):
        # Assumption:
        # For each repo named frontend-app-APPNAME, there is an associated
        # docker-compose service named APPNAME. If this assumption is broken,
        # then Tutor will try to mount the repo in a service that doesn't exist.
        app_name = name.split(prefix)[1]
        volumes += [(app_name, "/openedx/app")]
    return volumes


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
        # Here we force tutor-mfe lms patches to be loaded first, thus ensuring when opreators override
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
