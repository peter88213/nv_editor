"""A multi-section "plain text" editor plugin for novelibre.

Requires Python 3.7+
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
from nveditor.nveditor_locale import _
from nveditor.editor_service import EditorService
from nveditor.nveditor_help import NveditorHelp
from nvlib.controller.plugin.plugin_base import PluginBase


class Plugin(PluginBase):
    """novelibre multi-section "plain text" editor plugin class."""
    VERSION = '@release'
    API_VERSION = '5.44'
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

        #--- Configure the main menu.

        # Add the "Edit" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()

        label = _('Edit')
        self._ui.sectionMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            underline=0,
            command=self._open_editor_window,
        )
        self._ui.sectionMenu.disableOnLock.append(label)

        # Add an entry to the Help menu.
        label = _('Editor plugin Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self._open_help,
        )

        #--- Set Key bindings.
        self._ui.tv.tree.bind('<Double-1>', self._open_editor_window)
        self._ui.tv.tree.bind('<Return>', self._open_editor_window)

    def on_close(self, event=None):
        self.editorService.on_close()

    def on_quit(self, event=None):
        self.editorService.on_quit()

    def _open_editor_window(self, event=None):
        self.editorService.open_editor_window()

    def _open_help(self, event=None):
        NveditorHelp.open_help_page()

