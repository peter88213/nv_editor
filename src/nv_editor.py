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
from tkinter import messagebox

from nveditorlib.editor_window import EditorWindow
from nveditorlib.nveditor_globals import APPLICATION
from nveditorlib.nveditor_globals import ICON
from nveditorlib.nveditor_globals import SECTION_PREFIX
from nveditorlib.nveditor_globals import _
from nveditorlib.nveditor_globals import open_help
from nvlib.plugin.plugin_base import PluginBase
import tkinter as tk

SETTINGS = dict(
        ed_win_geometry='600x800',
        ed_color_mode=0,
        ed_color_fg_bright='white',
        ed_color_bg_bright='black',
        ed_color_fg_light='antique white',
        ed_color_bg_light='black',
        ed_color_fg_dark='light grey',
        ed_color_bg_dark='gray20',
        ed_font_family='Courier',
        ed_font_size=12,
        ed_line_spacing=4,
        ed_paragraph_spacing=4,
        ed_margin_x=40,
        ed_margin_y=20,
)
OPTIONS = dict(
        ed_live_wordcount=False,
)


class Plugin(PluginBase):
    """novelibre multi-section "plain text" editor plugin class."""
    VERSION = '@release'
    API_VERSION = '4.6'
    DESCRIPTION = 'A multi-section "plain text" editor'
    URL = 'https://github.com/peter88213/nv_editor'

    def install(self, model, view, controller, prefs=None):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Overrides the superclass method.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.novx/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/editor.ini'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=SETTINGS,
            options=OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add the "Edit" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()
        self._ui.sectionMenu.add_command(label=_('Edit'), underline=0, command=self.open_node)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Editor plugin Online help'), command=open_help)

        # Set window icon.
        self.sectionEditors = {}
        try:
            path = os.path.dirname(sys.argv[0])
            if not path:
                path = '.'
            self._icon = tk.PhotoImage(file=f'{path}/icons/{ICON}.png')
        except:
            self._icon = None

        # Configure the editor box.
        EditorWindow.colorMode = tk.IntVar(
            value=int(self.kwargs['ed_color_mode'])
            )
        EditorWindow.liveWordCount = tk.BooleanVar(
            value=self.kwargs['ed_live_wordcount']
            )

        # Set Key bindings.
        self._ui.tv.tree.bind('<Double-1>', self.open_node)
        self._ui.tv.tree.bind('<Return>', self.open_node)

    def on_close(self, event=None):
        """Actions to be performed when a project is closed.
        
        Close all open section editor windows. 
        Overrides the superclass method.
        """
        for scId in self.sectionEditors:
            if self.sectionEditors[scId].isOpen:
                self.sectionEditors[scId].on_quit()

    def on_quit(self, event=None):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        self.on_close()

        #--- Save project specific configuration
        self.kwargs['ed_color_mode'] = EditorWindow.colorMode.get()
        self.kwargs['ed_live_wordcount'] = EditorWindow.liveWordCount.get()
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def open_node(self, event=None):
        """Create a section editor window with a menu bar, a text box, and a status bar.
        
        Overrides the superclass method.
        """
        try:
            nodeId = self._ui.tv.tree.selection()[0]
            if nodeId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[nodeId].scType > 1:
                    return

                # A section is selected
                if self._ctrl.isLocked:
                    messagebox.showinfo(APPLICATION, _('Cannot edit sections, because the project is locked.'))
                    return

                if nodeId in self.sectionEditors and self.sectionEditors[nodeId].isOpen:
                    self.sectionEditors[nodeId].lift()
                    return

                self.sectionEditors[nodeId] = EditorWindow(self, self._mdl, self._ui, self._ctrl, nodeId, self.kwargs['ed_win_geometry'], icon=self._icon)

        except IndexError:
            # Nothing selected
            pass

