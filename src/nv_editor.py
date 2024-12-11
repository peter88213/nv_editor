"""A multi-section "plain text" editor plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
from pathlib import Path
import sys

from nveditor.editor_service import EditorService
from nveditor.nveditor_globals import ICON
from nveditor.nveditor_help import NveditorHelp
from nveditor.nveditor_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
import tkinter as tk


class Plugin(PluginBase):
    """novelibre multi-section "plain text" editor plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A multi-section "plain text" editor'
    URL = 'https://github.com/peter88213/nv_editor'

    INI_FILENAME = 'editor.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        win_geometry='600x800',
        color_mode=0,
        color_bg_bright='white',
        color_fg_bright='black',
        color_bg_light='antique white',
        color_fg_light='black',
        color_bg_dark='gray20',
        color_fg_dark='light grey',
        font_family='Courier',
        font_size=12,
        line_spacing=4,
        paragraph_spacing=4,
        margin_x=40,
        margin_y=20,
    )
    OPTIONS = dict(
        live_wordcount=False,
    )

    def install(self, model, view, controller):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Extends the superclass method.
        """
        super().install(model, view, controller)

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

        # Add the "Edit" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()
        self._ui.sectionMenu.add_command(label=_('Edit'), underline=0, command=self.open_editor_window)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Editor plugin Online help'), command=self.open_help)

        # Set window icon.
        try:
            path = os.path.dirname(sys.argv[0])
            if not path:
                path = '.'
            icon = tk.PhotoImage(file=f'{path}/icons/{ICON}.png')
        except:
            icon = None

        # Set Key bindings.
        self._ui.tv.tree.bind('<Double-1>', self.open_editor_window)
        self._ui.tv.tree.bind('<Return>', self.open_editor_window)

        self.editorService = EditorService(model, view, controller, icon, self.prefs)

    def on_close(self, event=None):
        """Actions to be performed when a project is closed.
        
        Close all open section editor windows. 
        Overrides the superclass method.
        """
        self.editorService.on_close()

    def on_quit(self, event=None):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        self.editorService.on_quit()

        #--- Save project specific configuration
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)

    def open_editor_window(self, event=None):
        self.editorService.open_editor_window()

    def open_help(self, event=None):
        NveditorHelp.open_help_page()

