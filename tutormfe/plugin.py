from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__

config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-mfe:{{ MFE_VERSION }}",
        "HOST": "apps.{{ LMS_HOST }}",
        "COMMON_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "CADDY_DOCKER_IMAGE": "{{ DOCKER_IMAGE_CADDY }}",
        "ACCOUNT_MFE_APP": {
            "name": "account",
            "repository": "https://github.com/edx/frontend-app-account",
            "port": 1997,
            "env": {
                "production": {
                    "COACHING_ENABLED": "",
                    "ENABLE_DEMOGRAPHICS_COLLECTION": "",
                },
            },
        },
        "GRADEBOOK_MFE_APP": {
            "name": "gradebook",
            "repository": "https://github.com/edx/frontend-app-gradebook",
            "port": 1994,
        },
        "LEARNING_MFE_APP": {
            "name": "learning",
            "repository": "https://github.com/edx/frontend-app-learning",
            "port": 2000,
        },
        "PROFILE_MFE_APP": {
            "name": "profile",
            "repository": "https://github.com/edx/frontend-app-profile",
            "port": 1995,
        },
    },
}

tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("mfe", "tasks", "lms", "init"),
    )
)
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "mfe",
        ("plugins", "mfe", "build", "mfe"),
        "{{ MFE_DOCKER_IMAGE }}",
        (),
    )
)


@tutor_hooks.Filters.IMAGES_PULL.add()
@tutor_hooks.Filters.IMAGES_PUSH.add()
def _add_remote_mfe_image_iff_customized(images, user_config):
    """
    Register MFE image for pushing & pulling if and only if it has
    been set to something other than the default.

    This is work-around to an upstream issue with MFE config. Briefly:
    User config is baked into MFE builds, so Tutor cannot host a generic
    pre-built MFE image. Howevever, individual Tutor users may want/need to
    build and host their own MFE image. So, as a compromise, we tell Tutor
    to push/pull the MFE image if the user has customized it to anything
    other than the default image URL.
    """
    image_tag = user_config["MFE_DOCKER_IMAGE"]
    if not image_tag.startswith("docker.io/overhangio/openedx-mfe:"):
        # Image has been customized. Add to list for pulling/pushing.
        images.append(("mfe", image_tag))
    return images

####### Boilerplate code
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
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"MFE_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"MFE_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
