"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-mfe hooks would be created in the context of some other plugin that imports
them.
"""

from __future__ import annotations

import typing as t

from tutor.core.hooks import Filter

EXTERNAL_SCRIPTS: Filter[list[tuple[str, str]], []] = Filter()

FRONTEND_APP_ATTRS_TYPE = t.Dict[
    t.Literal["npm_package", "npm_version", "enabled", "source"],
    t.Union[str, bool],
]

FRONTEND_APPS: Filter[dict[str, FRONTEND_APP_ATTRS_TYPE], []] = Filter()

FRONTEND_SLOTS: Filter[list[str], []] = Filter()

# TODO(fpf-removal): FRONTEND_COMPAT_PLUGINS, FRONTEND_COMPAT_SLOTS,
# FRONTEND_SLOT_COMPAT_MAPS, and FRONTEND_WIDGET_COMPAT_MAPS all feed the
# frontend-base compatibility shim and go away with env.config.compat.jsx
# itself.
FRONTEND_COMPAT_PLUGINS: Filter[list[str], []] = Filter()

FRONTEND_COMPAT_SLOTS: Filter[list[tuple[str, str]], []] = Filter()

FRONTEND_SLOT_COMPAT_MAPS: Filter[list[tuple[str, dict[str, t.Any]]], []] = Filter()

FRONTEND_WIDGET_COMPAT_MAPS: Filter[list[tuple[str, dict[str, t.Any]]], []] = Filter()

# TODO(legacy-mfe-removal): MFE_ATTRS_TYPE, MFE_APPS, and PLUGIN_SLOTS all go
# away with the legacy MFE cleanup. See the central TODO block in plugin.py for
# the full list.
MFE_ATTRS_TYPE = t.Dict[t.Literal["repository", "port", "version"], t.Union["str", int]]

MFE_APPS: Filter[dict[str, MFE_ATTRS_TYPE], []] = Filter()

PLUGIN_SLOTS: Filter[list[tuple[str, str, str]], []] = Filter()
