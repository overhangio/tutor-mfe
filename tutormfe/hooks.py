"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-mfe hooks would be created in the context of some other plugin that imports
them.
"""
from __future__ import annotations
import typing as t

from tutor.core.hooks import Filter


MFE_ATTRS_TYPE = t.Dict[t.Literal["repository", "port"], t.Union["str", int]]

MFE_APPS: Filter[dict[str, MFE_ATTRS_TYPE], []] = Filter()
