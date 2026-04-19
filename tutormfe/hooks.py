"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-mfe hooks would be created in the context of some other plugin that imports
them.
"""

from __future__ import annotations

import typing as t

from tutor.core.hooks import Filter

# TODO(legacy-mfe-removal): MFE_ATTRS_TYPE, MFE_APPS, and PLUGIN_SLOTS all go
# away with the legacy MFE cleanup. See the central TODO block in plugin.py for
# the full list.
MFE_ATTRS_TYPE = t.Dict[t.Literal["repository", "port", "version"], t.Union["str", int]]

FRONTEND_APP_ATTRS_TYPE = t.Dict[
    t.Literal["npm_package", "npm_version", "enabled", "source"],
    t.Union[str, bool],
]

MFE_APPS: Filter[dict[str, MFE_ATTRS_TYPE], []] = Filter()

FRONTEND_APPS: Filter[dict[str, FRONTEND_APP_ATTRS_TYPE], []] = Filter()

PLUGIN_SLOTS: Filter[list[tuple[str, str, str]], []] = Filter()

EXTERNAL_SCRIPTS: Filter[list[tuple[str, str]], []] = Filter()

FRONTEND_SLOTS: Filter[list[str], []] = Filter()
