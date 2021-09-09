from glob import glob
import os

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-mfe:{{ MFE_VERSION }}",
        "HOST": "apps.{{ LMS_HOST }}",
        "COMMON_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
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

hooks = {
    "build-image": {
        "mfe": "{{ MFE_DOCKER_IMAGE }}",
    },
    "init": ["lms"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
