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
    },
}

hooks = {
    "build-image": {
        "mfe": "{{ MFE_DOCKER_IMAGE }}",
    },
    "remote-image": {
        "mfe": "{{ MFE_DOCKER_IMAGE }}",
    },
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
