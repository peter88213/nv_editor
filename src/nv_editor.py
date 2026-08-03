"""A multi-section "plain text" editor plugin for novelibre.

Requires Python 3.7+
Copyright (c) Peter Triesberger
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
from nvlib.controller.plugin.plugin_base import PluginBase
from nveditor.platform.platform_settings import KEYS


class Plugin(PluginBase):
    """novelibre multi-section "plain text" editor plugin class."""
    VERSION = '@release'
    API_VERSION = '5.63'
    DESCRIPTION = 'A multi-section "plain text" editor'
    URL = 'https://github.com/peter88213/nv_editor'

    def install(self, model, view, controller):
        """Install the plugin at runtime.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.editorService = EditorService(model, view, controller)
        self._icon = self._get_icon('editor.png')

        #--- Configure the user interface.

        def open_editor_window(event=None):
            self.editorService.open_editor_window()

        def open_help():
            self._ctrl.helpService.open_help_page('nv_editor')

        # Add the Edit command to novelibre's Section menu.
        self._ui.sectionMenu.add_separator()

        label = _('Edit')
        self._ui.sectionMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            accelerator=KEYS.START_EDITOR[1],
            command=open_editor_window,
        )
        self._ui.sectionMenu.disableOnLock.append(label)

        # Add the Edit command to novelibre's section context menu.
        self._ui.sectionContextMenu.add_separator()
        self._ui.sectionContextMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            accelerator=KEYS.START_EDITOR[1],
            command=open_editor_window,
        )
        self._ui.sectionContextMenu.disableOnLock.append(label)

        # Add an entry to the Help menu.
        label = _('Editor plugin Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=open_help,
        )

        # Hotkey to start the section editor.
        self._ui.tv.tree.bind(KEYS.START_EDITOR[0], open_editor_window)

    def on_close(self, event=None):
        self.editorService.on_close()

    def on_quit(self, event=None):
        self.editorService.on_quit()

