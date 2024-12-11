"""Provide a mixin class for an editor window controller.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nveditor.nveditor_globals import FEATURE
from nveditor.nveditor_help import NveditorHelp
from nveditor.nveditor_locale import _
import xml.etree.ElementTree as ET


class EditorViewCtrl(SubController):
    """A controller for the section editor window.
    
    Public instance methods:
        show_wordcount()-- Display the word count on the status bar.    
    """
    liveWordCount = None
    # to be overwritten by the client with tk.BooleanVar()
    colorMode = None
    # to be overwritten by the client with tk.IntVar()

    def initialize_controller(self, model, view, controller, scId):
        super().initialize_controller(model, view, controller)
        self._section = self._mdl.novel.sections[scId]
        self._scId = scId

    def open_help(self, event=None):
        NveditorHelp.open_help_page()

    def show_wordcount(self, event=None):
        """Display the word count on the status bar."""
        wc = self.sectionEditor.count_words()
        diff = wc - self._initialWc
        self._statusBar.config(text=f'{wc} {_("words")} ({diff} {_("new")})')

    def _apply_changes(self, event=None):
        """Transfer the editor content to the project, if modified."""
        try:
            self.sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_error(
                str(ex),
                title=FEATURE,
                parent=self
                )
            self.lift()
            return

        sectionText = self.sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                self._transfer_text(sectionText)

    def _apply_changes_after_asking(self, event=None):
        """Transfer the editor content to the project, if modified. Ask first."""
        sectionText = self.sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                if self._ui.ask_yes_no(
                    _('Apply section changes?'),
                    title=FEATURE,
                    parent=self
                    ):
                    try:
                        self.sectionEditor.check_validity()
                    except ValueError as ex:
                        self._ui.show_error(
                            str(ex),
                            title=FEATURE,
                            parent=self
                            )
                        self.lift()
                        return False

                    self._transfer_text(sectionText)
        return True

    def _create_section(self, event=None):
        """Create a new section after the currently edited section.
        
        On success, return the ID of the new section, otherwise return None.
        """
        if self._ctrl.isLocked:
            self._ui.show_info(
                _('Cannot create sections, because the project is locked.'),
                title=FEATURE,
                parent=self
                )
            self.lift()
            return

        self.lift()
        # Add a section after the currently edited section.
        thisNode = self._scId
        sceneKind = self._mdl.novel.sections[self._scId].scene
        if sceneKind == 1:
            sceneKind = 2
        elif sceneKind == 2:
            sceneKind = 1
        newId = self._ctrl.add_new_section(
            targetNode=thisNode,
            scType=self._mdl.novel.sections[self._scId].scType,
            scene=sceneKind,
            )
        # Go to the new section.
        self._load_next()
        return newId

    def _load_next(self, event=None):
        """Load the next section in the tree."""
        if not self._apply_changes_after_asking():
            return

        nextNode = self._ui.tv.next_node(self._scId)
        if nextNode:
            self._ui.tv.go_to_node(nextNode)
            self.mainCtrl.close_editor_window(self._scId)
            self.mainCtrl.open_editor_window()

    def _load_prev(self, event=None):
        """Load the previous section in the tree."""
        if not self._apply_changes_after_asking():
            return

        prevNode = self._ui.tv.prev_node(self._scId)
        if prevNode:
            self._ui.tv.go_to_node(prevNode)
            self.mainCtrl.close_editor_window(self._scId)
            self.mainCtrl.open_editor_window()

    def _load_section(self):
        """Load the section content into the text editor."""
        self.title(f'{self._section.title} - {self._mdl.novel.title}, {_("Section")} ID {self._scId}')
        self.sectionEditor.set_text(self._section.sectionContent)
        self._initialWc = self.sectionEditor.count_words()
        self.show_wordcount()

    def _split_section(self, event=None):
        """Split a section at the cursor position."""

        try:
            self.sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_error(
                str(ex),
                title=FEATURE,
                parent=self
                )
            self.lift()
            return

        if self._ctrl.isLocked:
            self._ui.show_info(
                _('Cannot split the section, because the project is locked.'),
                title=FEATURE,
                parent=self
                )
            self.lift()
            return

        # Verify that the split would produce a valid result.
        try:
            ET.fromstring(f"<a>{self.sectionEditor.get('1.0', 'insert')}</a>")
            ET.fromstring(f"<a>{self.sectionEditor.get('insert', 'end')}</a>")
        except:
            self._ui.show_error(
                _('Cannot split the section at the cursor position.'),
                title=FEATURE,
                parent=self
                )
            self.lift()
            return

        if self._ui.ask_yes_no(
            f'{_("Move the text from the cursor position to the end into a new section")}?',
            title=FEATURE,
            parent=self
            ):
            self.lift()
        else:
            self.lift()
            return

        # Add a new section.
        thisNode = self._scId
        sceneKind = self._mdl.novel.sections[self._scId].scene
        if sceneKind == 1:
            sceneKind = 2
        elif sceneKind == 2:
            sceneKind = 1
        newId = self._ctrl.add_new_section(
            targetNode=thisNode,
            appendToPrev=True,
            scType=self._mdl.novel.sections[self._scId].scType,
            scene=sceneKind,
            status=self._mdl.novel.sections[self._scId].status
            )
        if newId:

            # Cut the actual section's content from the cursor position to the end.
            newContent = self.sectionEditor.get_text('insert', 'end').strip(' \n')
            self.sectionEditor.delete('insert', 'end')
            self._apply_changes()

            # Copy the section content to the new section.
            self._mdl.novel.sections[newId].sectionContent = newContent

            # Copy the viewpoint character.
            if self._mdl.novel.sections[self._scId].characters:
                viewpoint = self._mdl.novel.sections[self._scId].characters[0]
                self._mdl.novel.sections[newId].characters = [viewpoint]

            # Go to the new section.
            self._load_next()

    def _transfer_text(self, sectionText):
        """Transfer the changed editor content to the section, if possible.
        
        """
        try:
            self.sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_error(
                str(ex),
                title=FEATURE,
                parent=self
                )
            self.lift()
            return

        if self._ctrl.isLocked:
            if self._ui.ask_yes_no(
                _('Cannot apply section changes, because the project is locked.\nUnlock and apply changes?'),
                title=FEATURE,
                parent=self
                ):
                self._ctrl.unlock()
                self._section.sectionContent = sectionText
            self.lift()
        else:
            self._section.sectionContent = sectionText

