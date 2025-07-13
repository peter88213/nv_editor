"""A multi-section "plain text" editor plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
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
from pathlib import Path

from nveditor.nveditor_locale import _
from nveditor.editor_service import EditorService
from nveditor.nveditor_help import NveditorHelp
from nvlib.controller.plugin.plugin_base import PluginBase
import tkinter as tk


class Plugin(PluginBase):
    """novelibre multi-section "plain text" editor plugin class."""
    VERSION = '@release'
    API_VERSION = '5.27'
    DESCRIPTION = 'A multi-section "plain text" editor'
    URL = 'https://github.com/peter88213/nv_editor'

    def install(self, model, view, controller):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.editorService = EditorService(model, view, controller)
        self._icon = self._get_icon('editor.png')

        # Add the "Edit" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()
        self._ui.sectionMenu.add_command(
            label=_('Edit'),
            image=self._icon,
            compound='left',
            underline=0,
            command=self._open_editor_window,
        )

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(
            label=_('Editor plugin Online help'),
            image=self._icon,
            compound='left',
            command=self._open_help,
        )

        # Set Key bindings.
        self._ui.tv.tree.bind('<Double-1>', self._open_editor_window)
        self._ui.tv.tree.bind('<Return>', self._open_editor_window)

    def lock(self):
        self._ui.sectionMenu.entryconfig(_('Edit'), state='disabled')

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

    def unlock(self):
        self._ui.sectionMenu.entryconfig(_('Edit'), state='normal')

    def _open_editor_window(self, event=None):
        self.editorService.open_editor_window()

    def _open_help(self, event=None):
        NveditorHelp.open_help_page()

    def _get_icon(self, fileName):
        # Return the icon for the main view.
        if self._ctrl.get_preferences().get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
            icon = tk.PhotoImage(file=f'{iconPath}/{fileName}')
        except:
            icon = None
        return icon
