"""Provide a class with key definitions for Linux.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nveditor.nveditor_locale import _
from nveditor.platform.generic_keys import GenericKeys


class LinuxKeys(GenericKeys):

    # Numpad keys (needed for Linux)
    NEXT_KP = ('<Control-KP_Next>', f'{_("Ctrl")}-{_("PgDn")}')
    PREVIOUS_KP = ('<Control-KP_Prior>', f'{_("Ctrl")}-{_("PgUp")}')
