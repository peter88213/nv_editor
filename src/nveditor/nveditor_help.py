"""Provide a service class for the help function.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser

from nveditor.nveditor_locale import _


class NveditorHelp:

    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_editor/'

    @classmethod
    def open_help_page(cls):
        """Show the online help page."""
        webbrowser.open(cls.HELP_URL)
