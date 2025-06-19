"""Provide a class for the novelibre section editor window.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nveditor.editor_box import EditorBox
from nveditor.nveditor_globals import FEATURE
from nveditor.nveditor_help import NveditorHelp
from nveditor.nveditor_locale import _
from nveditor.platform.platform_settings import KEYS
from nveditor.platform.platform_settings import PLATFORM
from nvlib.controller.sub_controller import SubController
import tkinter as tk
import xml.etree.ElementTree as ET


class EditorView(tk.Toplevel, SubController):
    """A pop-up window with a menu bar, a text box, and a status bar.
    
    Public instance methods:
        lift() -- Bring window to the foreground and set the focus to the editor box.
        on_quit() -- Exit the editor. Apply changes, if possible.
    """
    liveWordCount = None
    # to be overwritten by the client with tk.BooleanVar()
    colorMode = None
    # to be overwritten by the client with tk.IntVar()

    def __init__(self, model, view, controller, scId, service, icon=None):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._scId = scId
        self._service = service
        self._section = self._mdl.novel.sections[scId]

        self.colorModes = [
            (
                _('Bright mode'),
                self._service.prefs['color_fg_bright'],
                self._service.prefs['color_bg_bright'],
            ),
            (
                _('Light mode'),
                self._service.prefs['color_fg_light'],
                self._service.prefs['color_bg_light'],
            ),
            (
                _('Dark mode'),
                self._service.prefs['color_fg_dark'],
                self._service.prefs['color_bg_dark'],
            ),
        ]
        # (name, foreground, background) tuples for color modes.

        # Create an independent editor window.
        super().__init__()
        self.geometry(self._service.prefs['win_geometry'])
        if icon:
            self.iconphoto(False, icon)

        # Add a main menu bar to the editor window.
        self._mainMenu = tk.Menu(self)
        self.config(menu=self._mainMenu)

        '''
        # Add a button bar to the editor window.
        self._buttonBar = ttk.Frame(self)
        self._buttonBar.pack(expand=False, fill='both')
        '''

        # Add a text editor with scrollbar to the editor window.
        self._sectionEditor = EditorBox(
            self,
            wrap='word',
            undo=True,
            autoseparators=True,
            spacing1=self._service.prefs['paragraph_spacing'],
            spacing2=self._service.prefs['line_spacing'],
            maxundo=-1,
            padx=self._service.prefs['margin_x'],
            pady=self._service.prefs['margin_y'],
            font=(
                self._service.prefs['font_family'],
                self._service.prefs['font_size'],
            ),
        )
        self._sectionEditor.pack(expand=True, fill='both')
        self._sectionEditor.pack_propagate(0)
        self._set_editor_colors()

        # Add a status bar to the editor window.
        self._statusBar = tk.Label(self, text='', anchor='w', padx=5, pady=2)
        self._statusBar.pack(expand=False, side='left')

        # Add buttons to the bottom line.
        ttk.Button(
            self,
            text=_('Next'),
            command=self._load_next,
        ).pack(side='right')
        ttk.Button(
            self,
            text=_('Close'),
            command=self._request_closing,
        ).pack(side='right')
        ttk.Button(
            self,
            text=_('Previous'),
            command=self._load_prev,
        ).pack(side='right')

        # Load the section content into the text editor.
        self._load_section()

        #--- Configure the user interface.
        '''
        # Add buttons to the button bar.
        tk.Button(
            self._buttonBar, 
            text=_('Copy'), 
            command=lambda: self._sectionEditor.event_generate("<<Copy>>"),
        ).pack(side='left')
        tk.Button(
            self._buttonBar, 
            text=_('Cut'), 
            command=lambda: self._sectionEditor.event_generate("<<Cut>>"),
        ).pack(side='left')
        tk.Button(
            self._buttonBar, 
            text=_('Paste'), 
            command=lambda: self._sectionEditor.event_generate("<<Paste>>"),
        ).pack(side='left')
        tk.Button(
            self._buttonBar, 
            text=_('Italic'), 
            command=self._sectionEditor.emphasis,
        ).pack(side='left')
        tk.Button(
            self._buttonBar, 
            text=_('Bold'), 
            command=self._sectionEditor.strong_emphasis).pack(side='left'),
        '''

        # Add a "Section" Submenu to the editor window.
        self._sectionMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(
            label=_('Section'),
            menu=self._sectionMenu,
        )
        self._sectionMenu.add_command(
            label=_('Next'),
            command=self._load_next,
        )
        self._sectionMenu.add_command(
            label=_('Previous'),
            command=self._load_prev,
        )
        self._sectionMenu.add_command(
            label=_('Apply changes'),
            accelerator=KEYS.APPLY_CHANGES[1],
            command=self._apply_changes,
        )
        if PLATFORM == 'win':
            self._sectionMenu.add_command(
                label=_('Exit'),
                accelerator=KEYS.QUIT_PROGRAM[1],
                command=self._request_closing,
            )
        else:
            self._sectionMenu.add_command(
                label=_('Quit'),
                accelerator=KEYS.QUIT_PROGRAM[1],
                command=self._request_closing,
            )

        # Add a "View" Submenu to the editor window.
        self._viewMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(
            label=_('View'),
            menu=self._viewMenu,
        )
        for i, cm in enumerate(self.colorModes):
            self._viewMenu.add_radiobutton(
                label=cm[0],
                variable=EditorView.colorMode,
                command=self._set_editor_colors,
                value=i,
            )

        # Add an "Edit" Submenu to the editor window.
        self._editMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(
            label=_('Edit'),
            menu=self._editMenu,
        )
        self._editMenu.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=lambda: self._sectionEditor.event_generate("<<Copy>>"),
        )
        self._editMenu.add_command(
            label=_('Cut'), accelerator=KEYS.CUT[1],
            command=lambda: self._sectionEditor.event_generate("<<Cut>>"),
        )
        self._editMenu.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=lambda: self._sectionEditor.event_generate("<<Paste>>"),
        )
        self._editMenu.add_separator()
        self._editMenu.add_command(
            label=_('Split at cursor position'),
            accelerator=KEYS.SPLIT_SCENE[1],
            command=self._split_section,
        )
        self._editMenu.add_command(
            label=_('Create section'),
            accelerator=KEYS.CREATE_SCENE[1],
            command=self._create_section,
        )

        # Add a "Format" Submenu to the editor window.
        self._formatMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(
            label=_('Format'),
            menu=self._formatMenu,
        )
        self._formatMenu.add_command(
            label=_('Emphasis'),
            accelerator=KEYS.ITALIC[1],
            command=self._sectionEditor.emphasis,
        )
        self._formatMenu.add_command(
            label=_('Strong emphasis'),
            accelerator=KEYS.BOLD[1],
            command=self._sectionEditor.strong_emphasis,
        )
        self._formatMenu.add_command(
            label=_('Plain'),
            accelerator=KEYS.PLAIN[1],
            command=self._sectionEditor.plain,
        )

        # Add a "Word count" Submenu to the editor window.
        self._wcMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(
            label=_('Word count'),
            menu=self._wcMenu,
        )
        self._wcMenu.add_command(
            label=_('Update'),
            accelerator=KEYS.UPDATE_WORDCOUNT[1],
            command=self._show_wordcount,
        )
        self._wcMenu.add_checkbutton(
            label=_('Live update'),
            variable=EditorView.liveWordCount,
            command=self._set_wc_mode,
        )

        # Help
        self._helpMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(
            label=_('Help'),
            menu=self._helpMenu,
        )
        self._helpMenu.add_command(
            label=_('Online help'),
            accelerator=KEYS.OPEN_HELP[1],
            command=self._open_help,
        )

        # Event bindings.
        self.bind(KEYS.OPEN_HELP[0], self._open_help)
        if PLATFORM != 'win':
            self._sectionEditor.bind(KEYS.QUIT_PROGRAM[0], self._request_closing)
        self._sectionEditor.bind(KEYS.APPLY_CHANGES[0], self._apply_changes)
        self._sectionEditor.bind(KEYS.UPDATE_WORDCOUNT[0], self._show_wordcount)
        self._sectionEditor.bind('<space>', self._sectionEditor.colorize)
        self._sectionEditor.bind(KEYS.SPLIT_SCENE[0], self._split_section)
        self._sectionEditor.bind(KEYS.CREATE_SCENE[0], self._create_section)
        self._sectionEditor.bind(KEYS.ITALIC[0], self._sectionEditor.emphasis)
        self._sectionEditor.bind(KEYS.BOLD[0], self._sectionEditor.strong_emphasis)
        self._sectionEditor.bind(KEYS.PLAIN[0], self._sectionEditor.plain)
        self._sectionEditor.bind('<Return>', self._sectionEditor.new_paragraph)
        self.protocol("WM_DELETE_WINDOW", self._request_closing)

        self._set_wc_mode()
        self.lift()

        self.update_idletasks()
        self.geometry(self._service.prefs['win_geometry'])

        self.isOpen = True

    def lift(self):
        """Bring window to the foreground and set the focus to the editor box.
        
        Extends the superclass method.
        """
        if self.state() == 'iconic':
            self.state('normal')
        super().lift()
        self._sectionEditor.focus()

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'
            # keeping the editor window open
            # due to malformed XML to be fixed before saving

        self._service.prefs['win_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def _apply_changes(self, event=None):
        # Transfer the editor content to the project, if modified.
        if not self._scId in self._mdl.novel.sections:
            return

        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_error(
                message=_('Invalid changes'),
                detail=str(ex),
                parent=self
                )
            self.lift()
            return

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                self._transfer_text(sectionText)

    def _apply_changes_after_asking(self, event=None):
        # Transfer the editor content to the project, if modified. Ask first.
        if not self._scId in self._mdl.novel.sections:
            return True

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                if self._ui.ask_yes_no(
                    message=_('Apply section changes?'),
                    title=FEATURE,
                    parent=self
                    ):
                    try:
                        self._sectionEditor.check_validity()
                    except ValueError as ex:
                        self._ui.show_error(
                            message=_('Invalid changes'),
                            detail=str(ex),
                            parent=self
                            )
                        self.lift()
                        return False

                    self._transfer_text(sectionText)
        return True

    def _create_section(self, event=None):
        # Create a new section after the currently edited section.
        # On success, return the ID of the new section,
        # otherwise return None.
        if self._ctrl.isLocked:
            self._ui.show_info(
                message=_('Cannot create section'),
                detail=f"{_('The project is locked')}.",
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
        # Load the next section in the tree.
        if not self._apply_changes_after_asking():
            return

        nextNode = self._ui.tv.next_node(self._scId)
        if nextNode:
            self._ui.tv.go_to_node(nextNode)
            self._request_closing()
            self._service.open_editor_window()

    def _load_prev(self, event=None):
        # Load the previous section in the tree.
        if not self._apply_changes_after_asking():
            return

        prevNode = self._ui.tv.prev_node(self._scId)
        if prevNode:
            self._ui.tv.go_to_node(prevNode)
            self._request_closing()
            self._service.open_editor_window()

    def _load_section(self):
        # Load the section content into the text editor.
        self.title(
            (
                f'{self._section.title} - {self._mdl.novel.title}'
                f', {_("Section")} ID {self._scId}'
            )
        )
        self._sectionEditor.set_text(self._section.sectionContent)
        self._initialWc = self._sectionEditor.count_words()
        self._show_wordcount()

    def _open_help(self, event=None):
        NveditorHelp.open_help_page()

    def _request_closing(self, event=None):
        self._service.close_editor_window(self._scId)
        # making sure the service removes this instance from the list

    def _set_editor_colors(self):
        cm = EditorView.colorMode.get()
        self._sectionEditor['fg'] = self.colorModes[cm][1]
        self._sectionEditor['bg'] = self.colorModes[cm][2]
        self._sectionEditor['insertbackground'] = self.colorModes[cm][1]

    def _set_wc_mode(self, *args):
        if EditorView.liveWordCount.get():
            self.bind('<KeyRelease>', self._show_wordcount)
            self._show_wordcount()
        else:
            self.unbind('<KeyRelease>')

    def _show_wordcount(self, event=None):
        # Display the word count on the status bar.
        wc = self._sectionEditor.count_words()
        diff = wc - self._initialWc
        self._statusBar.config(text=f'{wc} {_("words")} ({diff} {_("new")})')

    def _split_section(self, event=None):
        # Split a section at the cursor position.

        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_error(
                message=_('Invalid changes'),
                detail=str(ex),
                parent=self,
            )
            self.lift()
            return

        if self._ctrl.isLocked:
            self._ui.show_info(
                message=_('Cannot split the section'),
                detail=f"{_('The project is locked')}.",
                title=FEATURE,
                parent=self,
            )
            self.lift()
            return

        # Verify that the split would produce a valid result.
        try:
            ET.fromstring(f"<a>{self._sectionEditor.get('1.0', 'insert')}</a>")
            ET.fromstring(f"<a>{self._sectionEditor.get('insert', 'end')}</a>")
        except:
            self._ui.show_error(
                message=_('Cannot split the section at the cursor position'),
                detail=f"{_('The result would not be well-formed XML')}.",
                parent=self,
            )
            self.lift()
            return

        if self._ui.ask_yes_no(
            message=_('Move the text from the cursor position to the end into a new section?'),
            title=FEATURE,
            parent=self,
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
            newContent = self._sectionEditor.get_text('insert', 'end').strip(' \n')
            self._sectionEditor.delete('insert', 'end')
            self._apply_changes()

            # Copy the section content to the new section.
            self._mdl.novel.sections[newId].sectionContent = newContent

            # Copy the viewpoint character.
            self._mdl.novel.sections[newId].viewpoint = self._mdl.novel.sections[self._scId].viewpoint

            # Go to the new section.
            self._load_next()

    def _transfer_text(self, sectionText):
        # Transfer the changed editor content to the section, if possible.
        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_error(
                message=_('Invalid changes'),
                detail=str(ex),
                parent=self,
            )
            self.lift()
            return

        if self._ctrl.isLocked:
            if self._ui.ask_yes_no(
                message=_('Unlock and apply changes?'),
                detail=_('Cannot apply section changes as long as the project is locked.'),
                title=FEATURE,
                parent=self,
            ):
                self._ctrl.unlock()
                self._section.sectionContent = sectionText
            self.lift()
        else:
            self._section.sectionContent = sectionText

