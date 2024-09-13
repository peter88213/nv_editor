"""Provide platform specific key definitions for the nv_editor plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nveditorlib.nveditor_globals import PLATFORM
from nveditorlib.generic_keys import GenericKeys
from nveditorlib.mac_keys import MacKeys
from nveditorlib.windows_keys import WindowsKeys

if PLATFORM == 'win':
    KEYS = WindowsKeys()
elif PLATFORM == 'ix':
    KEYS = GenericKeys()
elif PLATFORM == 'mac':
    KEYS = MacKeys()
else:
    KEYS = GenericKeys()
