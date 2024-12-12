"""Provide a service class for editor window management.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/editor_service
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import sys

from mvclib.controller.sub_controller import SubController
from mvclib.view.observer import Observer
from nveditor.editor_view import EditorView
from nveditor.nveditor_globals import FEATURE
from nveditor.nveditor_globals import ICON
from nveditor.nveditor_locale import _
from nvlib.novx_globals import SECTION_PREFIX
import tkinter as tk


class EditorService(SubController, Observer):
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

    def __init__(self, model, view, controller):
        super().initialize_controller(model, view, controller)

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

        # Set window icon.
        try:
            path = os.path.dirname(sys.argv[0])
            if not path:
                path = '.'
            self.icon = tk.PhotoImage(file=f'{path}/icons/{ICON}.png')
        except:
            self.icon = None

        # Register to be refreshed when a section is deleted.
        self._mdl.add_observer(self)

        # Configure the editor box.
        EditorView.colorMode = tk.IntVar(
            value=int(self.prefs['color_mode'])
            )
        EditorView.liveWordCount = tk.BooleanVar(
            value=self.prefs['live_wordcount']
            )

        self.sectionEditors = {}
        # editor windows
        # key: str -- Section ID
        # value:  reference to the EditorView instance

    def close_editor_window(self, nodeId):
        if nodeId in self.sectionEditors and self.sectionEditors[nodeId].isOpen:
            self.sectionEditors[nodeId].on_quit()
            del self.sectionEditors[nodeId]

    def on_close(self):
        """Close all open section editor windows."""
        for scId in self.sectionEditors:
            if self.sectionEditors[scId].isOpen:
                self.sectionEditors[scId].on_quit()

    def on_quit(self):
        """Save project specific configuration."""
        self.on_close()
        self.prefs['color_mode'] = EditorView.colorMode.get()
        self.prefs['live_wordcount'] = EditorView.liveWordCount.get()

        #--- Save configuration
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)

    def open_editor_window(self):
        """Create a section editor window with a menu bar, a text box, and a status bar.
        
        Overrides the superclass method.
        """
        try:
            nodeId = self._ui.selectedNode
            if nodeId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[nodeId].scType > 1:
                    return

                # A section is selected
                if self._ctrl.isLocked:
                    self._ui.show_info(_('Cannot edit sections, because the project is locked.'), title=FEATURE)
                    return

                if nodeId in self.sectionEditors and self.sectionEditors[nodeId].isOpen:
                    self.sectionEditors[nodeId].lift()
                    return

                self.sectionEditors[nodeId] = EditorView(
                    self._mdl,
                    self._ui,
                    self._ctrl,
                    nodeId,
                    self,
                    icon=self.icon
                    )

        except IndexError:
            # Nothing selected
            pass

    def refresh(self):
        """Close editor window in case the corresmpnding section is deleted.
        
        Overrides the superclass method.
        """
        for scId in list(self.sectionEditors):
            if not scId in self._mdl.novel.sections:
                self.sectionEditors[scId].on_quit()
                del self.sectionEditors[scId]
