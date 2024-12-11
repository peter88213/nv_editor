"""Provide a service class for editor window management.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from mvclib.view.observer import Observer
from nveditor.editor_view import EditorView
from nveditor.nveditor_globals import FEATURE
from nvlib.novx_globals import SECTION_PREFIX
import tkinter as tk


class EditorService(SubController, Observer):

    def __init__(self, model, view, controller, icon, prefs):
        super().initialize_controller(model, view, controller)
        self.icon = icon
        self.prefs = prefs

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
