"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-mfe hooks would be created in the context of some other plugin that imports
them.
"""

from __future__ import annotations

import typing as t

from tutor.core.hooks import Filter

MFE_ATTRS_TYPE = t.Dict[t.Literal["repository", "port", "version"], t.Union["str", int]]
FRONTEND_TEMPLATE_SITE_ATTRS_TYPE = t.Dict

MFE_APPS: Filter[dict[str, MFE_ATTRS_TYPE], []] = Filter()

# TODO: This will hold the list of which apps are "enabled" so we can switch between mfe
# and frontend-base ones
FRONTEND_APPS: Filter[dict[str, t.Dict], []] = Filter()

PLUGIN_SLOTS: Filter[list[tuple[str, str, str]], []] = Filter()
