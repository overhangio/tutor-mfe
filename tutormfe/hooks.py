"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-mfe hooks would be created in the context of some other plugin that imports
them.
"""

from __future__ import annotations

import typing as t

from tutor.core.hooks import Filter

MFE_ATTRS_TYPE = t.Dict[t.Literal["repository", "port", "version"], t.Union["str", int]]

FRONTEND_APP_ATTRS_TYPE = t.Dict[
    t.Literal["npm_package", "npm_version", "enabled", "repository", "branch"],
    t.Union[str, bool],
]

MFE_APPS: Filter[dict[str, MFE_ATTRS_TYPE], []] = Filter()

FRONTEND_APPS: Filter[dict[str, FRONTEND_APP_ATTRS_TYPE], []] = Filter()

PLUGIN_SLOTS: Filter[list[tuple[str, str, str]], []] = Filter()

FRONTEND_SLOTS: Filter[list[str], []] = Filter()
