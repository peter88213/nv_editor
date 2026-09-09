"""Provide global variables and functions.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import font as tkFont

from nveditor.nveditor_locale import _

prefs = {}

FEATURE = _('Section Editor')
ICON = 'editor'
HELP_PAGE = 'nv_editor'

FONTS = [
    'DejaVu Sans Mono',  # usually bundled with LibreOffice
    'Consolas',  # available on Windows
    'Liberation Mono',
    'Courier',  # fallback, if none of the above is installed
]
INSTALLED_FONTS = tkFont.families()
for editorFont in FONTS:
    if editorFont in INSTALLED_FONTS:
        break

DEFAULT_FONT = editorFont


def check_editor_settings():

    if not prefs['editor_font'] in INSTALLED_FONTS:
        prefs['editor_font'] = DEFAULT_FONT

    prefs['color_mode'] = int(prefs['color_mode'])

    return True
