"""Provide a section editor class for the novelibre plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
from tkinter import messagebox
from tkinter import ttk
import webbrowser

from nveditorlib.nveditor_globals import APPLICATION
from nveditorlib.nveditor_globals import _
from nveditorlib.text_box import TextBox
import tkinter as tk
import xml.etree.ElementTree as ET

HELP_URL = 'https://github.com/peter88213/nv_editor/usage'
KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')
KEY_APPLY_CHANGES = ('<Control-s>', 'Ctrl-S')
KEY_UPDATE_WORDCOUNT = ('<F5>', 'F5')
KEY_SPLIT_SCENE = ('<Control-Alt-s>', 'Ctrl-Alt-S')
KEY_CREATE_SCENE = ('<Control-Alt-n>', 'Ctrl-Alt-N')
KEY_ITALIC = ('<Control-i>', 'Ctrl-I')
KEY_BOLD = ('<Control-b>', 'Ctrl-B')
KEY_PLAIN = ('<Control-m>', 'Ctrl-M')

COLOR_MODES = [
    (_('Bright mode'), 'black', 'white'),
    (_('Light mode'), 'black', 'antique white'),
    (_('Dark mode'), 'light grey', 'gray20'),
    ]
# (name, foreground, background) tuples for color modes.


class SectionEditor(tk.Toplevel):
    """A separate section editor window with a menu bar, a text box, and a status bar.
    
    Public instance methods:
        lift() -- Bring window to the foreground and set the focus to the editor box.
        on_quit() -- Exit the editor. Apply changes, if possible.
        show_status(message=None) -- Display a message on the status bar.
        show_wordcount()-- Display the word count on the status bar.
    """
    liveWordCount = False
    colorMode = 0

    def __init__(self, plugin, model, view, controller, scId, size, icon=None):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._plugin = plugin
        self._section = self._mdl.novel.sections[scId]
        self._scId = scId

        # Create an independent editor window.
        super().__init__()
        self.geometry(size)
        if icon:
            self.iconphoto(False, icon)

        # Add a main menu bar to the editor window.
        self._mainMenu = tk.Menu(self)
        self.config(menu=self._mainMenu)

        '''
        # Add a button bar to the editor window.
        self._buttonBar = tk.Frame(self)
        self._buttonBar.pack(expand=False, fill='both')
        '''

        # Add a text editor with scrollbar to the editor window.
        self._sectionEditor = TextBox(
            self,
            wrap='word',
            undo=True,
            autoseparators=True,
            spacing1=self._plugin.kwargs['paragraph_spacing'],
            spacing2=self._plugin.kwargs['line_spacing'],
            maxundo=-1,
            padx=self._plugin.kwargs['margin_x'],
            pady=self._plugin.kwargs['margin_y'],
            font=(self._plugin.kwargs['font_family'], self._plugin.kwargs['font_size']),
            )
        self._sectionEditor.pack(expand=True, fill='both')
        self._sectionEditor.pack_propagate(0)
        self._set_editor_colors()

        # Add a status bar to the editor window.
        self._statusBar = tk.Label(self, text='', anchor='w', padx=5, pady=2)
        self._statusBar.pack(expand=False, side='left')

        # Add buttons to the bottom line.
        ttk.Button(self, text=_('Next'), command=self._load_next).pack(side='right')
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right')
        ttk.Button(self, text=_('Previous'), command=self._load_prev).pack(side='right')

        # Load the section content into the text editor.
        self._load_section()

        #--- Configure the user interface.
        '''
        # Add buttons to the button bar.
        tk.Button(self._buttonBar, text=_('Copy'), command=lambda: self._sectionEditor.event_generate("<<Copy>>")).pack(side='left')
        tk.Button(self._buttonBar, text=_('Cut'), command=lambda: self._sectionEditor.event_generate("<<Cut>>")).pack(side='left')
        tk.Button(self._buttonBar, text=_('Paste'), command=lambda: self._sectionEditor.event_generate("<<Paste>>")).pack(side='left')
        tk.Button(self._buttonBar, text=_('Italic'), command=self._sectionEditor.emphasis).pack(side='left')
        tk.Button(self._buttonBar, text=_('Bold'), command=self._sectionEditor.strong_emphasis).pack(side='left')
        '''

        # Add a "Section" Submenu to the editor window.
        self._sectionMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Section'), menu=self._sectionMenu)
        self._sectionMenu.add_command(label=_('Next'), command=self._load_next)
        self._sectionMenu.add_command(label=_('Previous'), command=self._load_prev)
        self._sectionMenu.add_command(label=_('Apply changes'), accelerator=KEY_APPLY_CHANGES[1], command=self._apply_changes)
        if sys.platform == 'win32':
            self._sectionMenu.add_command(label=_('Exit'), accelerator='Alt-F4', command=self.on_quit)
        else:
            self._sectionMenu.add_command(label=_('Quit'), accelerator=KEY_QUIT_PROGRAM[1], command=self.on_quit)

        # Add a "View" Submenu to the editor window.
        self._viewMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('View'), menu=self._viewMenu)
        self._viewMenu.add_command(label=COLOR_MODES[0][0], command=lambda: self._set_view_mode(mode=0))
        self._viewMenu.add_command(label=COLOR_MODES[1][0], command=lambda: self._set_view_mode(mode=1))
        self._viewMenu.add_command(label=COLOR_MODES[2][0], command=lambda: self._set_view_mode(mode=2))
        # note: this can't be done with a loop because of the "lambda" evaluation at runtime

        # Add an "Edit" Submenu to the editor window.
        self._editMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Edit'), menu=self._editMenu)
        self._editMenu.add_command(label=_('Copy'), accelerator='Ctrl-C', command=lambda: self._sectionEditor.event_generate("<<Copy>>"))
        self._editMenu.add_command(label=_('Cut'), accelerator='Ctrl-X', command=lambda: self._sectionEditor.event_generate("<<Cut>>"))
        self._editMenu.add_command(label=_('Paste'), accelerator='Ctrl-V', command=lambda: self._sectionEditor.event_generate("<<Paste>>"))
        self._editMenu.add_separator()
        self._editMenu.add_command(label=_('Split at cursor position'), accelerator=KEY_SPLIT_SCENE[1], command=self._split_section)
        self._editMenu.add_command(label=_('Create section'), accelerator=KEY_CREATE_SCENE[1], command=self._create_section)

        # Add a "Format" Submenu to the editor window.
        self._formatMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Format'), menu=self._formatMenu)
        self._formatMenu.add_command(label=_('Emphasis'), accelerator=KEY_ITALIC[1], command=self._sectionEditor.emphasis)
        self._formatMenu.add_command(label=_('Strong emphasis'), accelerator=KEY_BOLD[1], command=self._sectionEditor.strong_emphasis)
        self._formatMenu.add_command(label=_('Plain'), accelerator=KEY_PLAIN[1], command=self._sectionEditor.plain)

        # Add a "Word count" Submenu to the editor window.
        self._wcMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Word count'), menu=self._wcMenu)
        self._wcMenu.add_command(label=_('Update'), accelerator=KEY_UPDATE_WORDCOUNT[1], command=self.show_wordcount)
        self._wcMenu.add_command(label=_('Enable live update'), command=self._live_wc_on)
        self._wcMenu.add_command(label=_('Disable live update'), command=self._live_wc_off)

        # Help
        self.helpMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), command=lambda: webbrowser.open(HELP_URL))

        # Event bindings.
        if sys.platform != 'win32':
            self.bind_class('Text', KEY_QUIT_PROGRAM[0], self.on_quit)
        self.bind_class('Text', KEY_APPLY_CHANGES[0], self._apply_changes)
        self.bind_class('Text', KEY_UPDATE_WORDCOUNT[0], self.show_wordcount)
        self.bind_class('Text', KEY_SPLIT_SCENE[0], self._split_section)
        self.bind_class('Text', KEY_CREATE_SCENE[0], self._create_section)
        self.bind_class('Text', KEY_ITALIC[0], self._sectionEditor.emphasis)
        self.bind_class('Text', KEY_BOLD[0], self._sectionEditor.strong_emphasis)
        self.bind_class('Text', KEY_PLAIN[0], self._sectionEditor.plain)
        self.bind_class('Text', '<Return>', self._sectionEditor.new_paragraph)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        if SectionEditor.liveWordCount:
            self._live_wc_on()
        else:
            self._wcMenu.entryconfig(_('Disable live update'), state='disabled')

        self.lift()
        self.isOpen = True

    def lift(self):
        """Bring window to the foreground and set the focus to the editor box.
        
        Extends the superclass method.
        """
        super().lift()
        self._sectionEditor.focus()

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'
            # keeping the editor window open due to an XML error to be fixed before saving

        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def show_status(self, message=None):
        """Display a message on the status bar."""
        self._statusBar.config(text=message)

    def show_wordcount(self, event=None):
        """Display the word count on the status bar."""
        wc = self._sectionEditor.count_words()
        diff = wc - self._initialWc
        self._statusBar.config(text=f'{wc} {_("words")} ({diff} {_("new")})')

    def _create_section(self, event=None):
        """Create a new section after the currently edited section."""
        if self._ctrl.isLocked:
            messagebox.showinfo(
                APPLICATION,
                _('Cannot create sections, because the project is locked.'),
                parent=self
                )
            self.lift()
            return

        self.lift()
        # Add a section after the currently edited section.
        thisNode = self._scId
        newId = self._ctrl.add_section(
            targetNode=thisNode,
            scType=self._mdl.novel.sections[self._scId].scType,
            scPacing=self._mdl.novel.sections[self._scId].scPacing,
            )
        # Go to the new section.
        self._load_next()

    def _apply_changes(self, event=None):
        """Transfer the editor content to the project, if modified."""
        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_warning(str(ex))
            self.lift()
            return

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                self._transfer_text(sectionText)

    def _apply_changes_after_asking(self, event=None):
        """Transfer the editor content to the project, if modified. Ask first."""
        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                if messagebox.askyesno(APPLICATION, _('Apply section changes?'), parent=self):
                    try:
                        self._sectionEditor.check_validity()
                    except ValueError as ex:
                        self._ui.show_warning(str(ex))
                        self.lift()
                        return False

                    self._transfer_text(sectionText)
        return True

    def _live_wc_off(self, event=None):
        self.unbind('<KeyRelease>')
        self._wcMenu.entryconfig(_('Enable live update'), state='normal')
        self._wcMenu.entryconfig(_('Disable live update'), state='disabled')
        SectionEditor.liveWordCount = False

    def _live_wc_on(self, event=None):
        self.bind('<KeyRelease>', self.show_wordcount)
        self._wcMenu.entryconfig(_('Enable live update'), state='disabled')
        self._wcMenu.entryconfig(_('Disable live update'), state='normal')
        self.show_wordcount()
        SectionEditor.liveWordCount = True

    def _load_next(self, event=None):
        """Load the next section in the tree."""
        if not self._apply_changes_after_asking():
            return

        nextNode = self._ui.tv.next_node(self._scId)
        if nextNode:
            self._ui.tv.go_to_node(nextNode)
            self._scId = nextNode
            self._section = self._mdl.novel.sections[nextNode]
            self._sectionEditor.clear()
            self._load_section()
        self.lift()

    def _load_prev(self, event=None):
        """Load the previous section in the tree."""
        if not self._apply_changes_after_asking():
            return

        prevNode = self._ui.tv.prev_node(self._scId)
        if prevNode:
            self._ui.tv.go_to_node(prevNode)
            self._scId = prevNode
            self._section = self._mdl.novel.sections[prevNode]
            self._sectionEditor.clear()
            self._load_section()
        self.lift()

    def _load_section(self):
        """Load the section content into the text editor."""
        self.title(f'{self._section.title} - {self._mdl.novel.title}, {_("Section")} ID {self._scId}')
        self._sectionEditor.set_text(self._section.sectionContent)
        self._initialWc = self._sectionEditor.count_words()
        self.show_wordcount()

    def _set_editor_colors(self):
        self._sectionEditor['fg'] = COLOR_MODES[SectionEditor.colorMode][1]
        self._sectionEditor['bg'] = COLOR_MODES[SectionEditor.colorMode][2]
        self._sectionEditor['insertbackground'] = COLOR_MODES[SectionEditor.colorMode][1]

    def _set_view_mode(self, event=None, mode=0):
        SectionEditor.colorMode = mode
        self._set_editor_colors()

    def _split_section(self, event=None):
        """Split a section at the cursor position."""

        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_warning(str(ex))
            self.lift()
            return

        if self._ctrl.isLocked:
            messagebox.showinfo(
                APPLICATION,
                _('Cannot split the section, because the project is locked.'),
                parent=self
                )
            self.lift()
            return

        # Verify that the split would produce a valid result.
        try:
            ET.fromstring(f"<a>{self._sectionEditor.get('1.0', 'insert')}</a>")
            ET.fromstring(f"<a>{self._sectionEditor.get('insert', 'end')}</a>")
        except:
            self._ui.show_warning(_('Cannot split the section at the cursor position.'))
            self.lift()
            return

        if messagebox.askyesno(
            APPLICATION,
            f'{_("Move the text from the cursor position to the end into a new section")}?',
            parent=self
            ):
            self.lift()
        else:
            self.lift()
            return

        # Add a new section.
        thisNode = self._scId
        newId = self._ctrl.add_section(
            targetNode=thisNode,
            appendToPrev=True,
            scType=self._mdl.novel.sections[self._scId].scType,
            scPacing=self._mdl.novel.sections[self._scId].scPacing,
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
            if self._mdl.novel.sections[self._scId].characters:
                viewpoint = self._mdl.novel.sections[self._scId].characters[0]
                self._mdl.novel.sections[newId].characters = [viewpoint]

            # Go to the new section.
            self._load_next()

    def _transfer_text(self, sectionText):
        """Transfer the changed editor content to the section, if possible.
        
        """
        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_warning(str(ex))
            self.lift()
            return

        if self._ctrl.isLocked:
            if messagebox.askyesno(
                APPLICATION,
                _('Cannot apply section changes, because the project is locked.\nUnlock and apply changes?'),
                parent=self
                ):
                self._ctrl.unlock()
                self._section.sectionContent = sectionText
            self.lift()
        else:
            self._section.sectionContent = sectionText
        self._ui.show_status()

