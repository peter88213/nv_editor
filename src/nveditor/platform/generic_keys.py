"""Provide a class with key definitions.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nveditor.nveditor_locale import _


class GenericKeys:

    APPLY_CHANGES = ('<Control-s>', f'{_("Ctrl")}-S')
    BOLD = ('<Control-b>', f'{_("Ctrl")}-B')
    COPY = ('<Control-c>', f'{_("Ctrl")}-C')
    CREATE_SECTION = ('<Control-n>', f'{_("Ctrl")}-N')
    CUT = ('<Control-x>', f'{_("Ctrl")}-X')
    PASTE = ('<Control-v>', f'{_("Ctrl")}-V')
    ITALIC = ('<Control-i>', f'{_("Ctrl")}-I')
    NEXT = ('<Control-Next>', f'{_("Ctrl")}-{_("PgDn")}')
    OPEN_HELP = ('<F1>', 'F1')
    PLAIN = ('<Control-m>', f'{_("Ctrl")}-M')
    PREVIOUS = ('<Control-Prior>', f'{_("Ctrl")}-{_("PgUp")}')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    SPLIT_SECTION = ('<Control-l>', f'{_("Ctrl")}-L')
    START_EDITOR = ('<F4>', 'F4')
