"""Provide platform specific key definitions for the nv_editor plugin.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nveditor.platform.generic_keys import GenericKeys
from nveditor.platform.mac_keys import MacKeys
from nveditor.platform.windows_keys import WindowsKeys

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
else:
    PLATFORM = ''
    KEYS = GenericKeys()

