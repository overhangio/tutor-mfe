"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-mfe hooks would be created in the context of some other plugin that imports
them.
"""

from __future__ import annotations

import typing as t

from tutor.core.hooks import Filter

MFE_ATTRS_TYPE = t.Dict[t.Literal["repository", "port", "version"], t.Union["str", int]]

# Extended MFE type that includes externalRoutes
FRONTEND_SITE_ATTRS_TYPE = t.Dict[
    t.Literal["repository", "port", "version", "siteConfig"],
    t.Union[str, int, dict],
]

FRONTEND_APP_ATTRS_TYPE = t.Dict[
    t.Literal["repository", "version", "site", "appEntryPoints", "appId"],
    t.Union["str", int, dict],
]

MFE_APPS: Filter[dict[str, MFE_ATTRS_TYPE], []] = Filter()

# This holds which apps are enabled and if they will build from a custom repo
FRONTEND_APPS: Filter[dict[str, FRONTEND_APP_ATTRS_TYPE], []] = Filter()
# This holds all the possible frontend-sites which by default it's the internal one.
FRONTEND_SITES: Filter[dict[str, FRONTEND_SITE_ATTRS_TYPE], []] = Filter()

PLUGIN_SLOTS: Filter[list[tuple[str, str, str]], []] = Filter()

FRONTEND_SLOTS: Filter[list[tuple[str, str]], []] = Filter()
