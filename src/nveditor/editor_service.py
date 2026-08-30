"""Provide a service class for editor window management.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import sys

from nveditor.editor_box import EditorBox
from nveditor.editor_view import EditorView
from nveditor.nveditor_globals import DEFAULT_FONT
from nveditor.nveditor_globals import FEATURE
from nveditor.nveditor_globals import ICON
from nveditor.nveditor_globals import prefs
from nveditor.nveditor_locale import _
from nvlib.controller.sub_controller import SubController
from nvlib.gui.observer import Observer
from nvlib.novx_globals import SECTION_PREFIX
import tkinter as tk


class EditorService(SubController, Observer):
    INI_FILENAME = 'editor.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        win_geometry='600x800',
        color_mode=0,
        color_bg='#ffffff',
        color_fg='#000000',
        color_xml_tag='#0000ff',
        editor_font=DEFAULT_FONT,
        font_size=12,
        line_spacing=4,
        paragraph_spacing=4,
        margin_x=40,
        margin_y=20,
    )
    OPTIONS = {}

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS,
            filePath=f'{configDir}/{self.INI_FILENAME}',
        )
        self.configuration.read()
        prefs.update(self.configuration.settings)
        prefs.update(self.configuration.options)

        # Set window icon.
        try:
            path = os.path.dirname(sys.argv[0])
            if not path:
                path = '.'
            self.icon = tk.PhotoImage(file=f'{path}/icons/{ICON}.png')
        except:
            self.icon = None

        self._sectionEditors = {}
        # editor windows
        # key: str -- Section ID
        # value:  reference to the EditorView instance

        # Register to be refreshed when a section is deleted.
        self._mdl.add_observer(self)

        # Configure the editor box.
        EditorView.colorModeVar = tk.IntVar(
            value=int(prefs['color_mode']),
        )
        EditorBox.colorXmlTag = prefs['color_xml_tag']

    def close_editor_window(self, scId):
        """Close the editor window without data loss.
         
        In case of malformed XML to be fixed before saving,
        Keep the editor window open.
        """
        if self._sectionEditors[scId].apply_changes_after_asking():
            self.close_editor_window_without_asking(scId)

    def close_editor_window_without_asking(self, scId):
        """Immediately close the editor window."""
        prefs['win_geometry'] = self._sectionEditors[scId].winfo_geometry()
        self._sectionEditors[scId].destroy()
        del self._sectionEditors[scId]

    def on_close(self):
        """Close all open section editor windows.
        
        The project may be closed, so that changes no longe can be applied.
        """
        for scId in self._sectionEditors:
            self.close_editor_window_without_asking(scId)

    def on_quit(self):
        """Save project specific configuration."""
        self.on_close()
        prefs['color_mode'] = EditorView.colorModeVar.get()

        #--- Save configuration
        for keyword in prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = prefs[keyword]
        self.configuration.write()

    def open_editor_window(self):
        """Create a section editor window 
        
        with a menu bar, a text box, and a status bar.
        """
        try:
            nodeId = self._ui.selectedNode
            if nodeId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[nodeId].scType > 1:
                    return

                # A section is selected
                if self._ctrl.isLocked:
                    self._ui.show_info(
                        message=_('Cannot edit sections'),
                        detail=f"{_('The project is locked')}.",
                        title=FEATURE,
                    )
                    return

                if nodeId in self._sectionEditors:
                    self._sectionEditors[nodeId].lift()
                    return

                self._sectionEditors[nodeId] = EditorView(
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

    def ready_to_close(self):
        """Close all open section editor windows if their content is valid.
        
        Return True if no editor window is open.
        Return False, if an editor window remains open due to invalid content.
        """

        # First run: Close editor windows with unchanged content.
        # Put any other editor window to the front.
        for scId in list(self._sectionEditors):
            if not self._sectionEditors[scId].changes_made:
                self.close_editor_window_without_asking(scId)
            else:
                self._sectionEditors[scId].lift()

        # Second run: Try closing the editor windows with changed content.
        for scId in list(self._sectionEditors):
            if not self._sectionEditors[scId].apply_changes_after_asking():
                # the editor window remains open due to invalid content
                return False

            self.close_editor_window_without_asking(scId)
        return True

    def refresh(self):
        """Close editor window in case the corresponding section is deleted.
        
        Overrides the superclass method.
        """
        for scId in list(self._sectionEditors):
            if not scId in self._mdl.novel.sections:
                self.close_editor_window_without_asking(scId)

