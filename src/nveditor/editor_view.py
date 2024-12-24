"""Provide a class for the novelibre section editor window.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nveditor.editor_box import EditorBox
from nveditor.editor_view_ctrl import EditorViewCtrl
from nveditor.nveditor_locale import _
from nveditor.platform.platform_settings import KEYS
from nveditor.platform.platform_settings import PLATFORM
import tkinter as tk


class EditorView(tk.Toplevel, EditorViewCtrl):
    """A pop-up window with a menu bar, a text box, and a status bar.
    
    Public instance methods:
        lift() -- Bring window to the foreground and set the focus to the editor box.
        on_quit() -- Exit the editor. Apply changes, if possible.
        show_status(message=None) -- Display a message on the status bar.
    """
    liveWordCount = None
    # to be overwritten by the client with tk.BooleanVar()
    colorMode = None
    # to be overwritten by the client with tk.IntVar()

    def __init__(self, model, view, controller, scId, service, icon=None):
        self.initialize_controller(model, view, controller, scId, service)
        self.prefs = service.prefs

        self.colorModes = [
            (
                _('Bright mode'),
                self.prefs['color_fg_bright'],
                self.prefs['color_bg_bright'],
                ),
            (
                _('Light mode'),
                self.prefs['color_fg_light'],
                self.prefs['color_bg_light'],
                ),
            (
                _('Dark mode'),
                self.prefs['color_fg_dark'],
                self.prefs['color_bg_dark'],
                ),
            ]
        # (name, foreground, background) tuples for color modes.

        # Create an independent editor window.
        super().__init__()
        self.geometry(self.prefs['win_geometry'])
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
        self.sectionEditor = EditorBox(
            self,
            wrap='word',
            undo=True,
            autoseparators=True,
            spacing1=self.prefs['paragraph_spacing'],
            spacing2=self.prefs['line_spacing'],
            maxundo=-1,
            padx=self.prefs['margin_x'],
            pady=self.prefs['margin_y'],
            font=(self.prefs['font_family'], self.prefs['font_size']),
            )
        self.sectionEditor.pack(expand=True, fill='both')
        self.sectionEditor.pack_propagate(0)
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
        self._sectionMenu.add_command(label=_('Apply changes'), accelerator=KEYS.APPLY_CHANGES[1], command=self._apply_changes)
        if PLATFORM == 'win':
            self._sectionMenu.add_command(label=_('Exit'), accelerator=KEYS.QUIT_PROGRAM[1], command=self.on_quit)
        else:
            self._sectionMenu.add_command(label=_('Quit'), accelerator=KEYS.QUIT_PROGRAM[1], command=self.on_quit)

        # Add a "View" Submenu to the editor window.
        self._viewMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('View'), menu=self._viewMenu)
        for i, cm in enumerate(self.colorModes):
            self._viewMenu.add_radiobutton(label=cm[0], variable=EditorView.colorMode, command=self._set_editor_colors, value=i)

        # Add an "Edit" Submenu to the editor window.
        self._editMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Edit'), menu=self._editMenu)
        self._editMenu.add_command(label=_('Copy'), accelerator=KEYS.COPY[1], command=lambda: self.sectionEditor.event_generate("<<Copy>>"))
        self._editMenu.add_command(label=_('Cut'), accelerator=KEYS.CUT[1], command=lambda: self.sectionEditor.event_generate("<<Cut>>"))
        self._editMenu.add_command(label=_('Paste'), accelerator=KEYS.PASTE[1], command=lambda: self.sectionEditor.event_generate("<<Paste>>"))
        self._editMenu.add_separator()
        self._editMenu.add_command(label=_('Split at cursor position'), accelerator=KEYS.SPLIT_SCENE[1], command=self._split_section)
        self._editMenu.add_command(label=_('Create section'), accelerator=KEYS.CREATE_SCENE[1], command=self._create_section)

        # Add a "Format" Submenu to the editor window.
        self._formatMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Format'), menu=self._formatMenu)
        self._formatMenu.add_command(label=_('Emphasis'), accelerator=KEYS.ITALIC[1], command=self.sectionEditor.emphasis)
        self._formatMenu.add_command(label=_('Strong emphasis'), accelerator=KEYS.BOLD[1], command=self.sectionEditor.strong_emphasis)
        self._formatMenu.add_command(label=_('Plain'), accelerator=KEYS.PLAIN[1], command=self.sectionEditor.plain)

        # Add a "Word count" Submenu to the editor window.
        self._wcMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Word count'), menu=self._wcMenu)
        self._wcMenu.add_command(label=_('Update'), accelerator=KEYS.UPDATE_WORDCOUNT[1], command=self.show_wordcount)
        self._wcMenu.add_checkbutton(label=_('Live update'), variable=EditorView.liveWordCount, command=self._set_wc_mode)

        # Help
        self.helpMenu = tk.Menu(self._mainMenu, tearoff=0)
        self._mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), accelerator=KEYS.OPEN_HELP[1], command=self.open_help)

        # Event bindings.
        self.bind(KEYS.OPEN_HELP[0], self.open_help)
        if PLATFORM != 'win':
            self.sectionEditor.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)
        self.sectionEditor.bind(KEYS.APPLY_CHANGES[0], self._apply_changes)
        self.sectionEditor.bind(KEYS.UPDATE_WORDCOUNT[0], self.show_wordcount)
        self.sectionEditor.bind('<space>', self.sectionEditor.colorize)
        self.sectionEditor.bind(KEYS.SPLIT_SCENE[0], self._split_section)
        self.sectionEditor.bind(KEYS.CREATE_SCENE[0], self._create_section)
        self.sectionEditor.bind(KEYS.ITALIC[0], self.sectionEditor.emphasis)
        self.sectionEditor.bind(KEYS.BOLD[0], self.sectionEditor.strong_emphasis)
        self.sectionEditor.bind(KEYS.PLAIN[0], self.sectionEditor.plain)
        self.sectionEditor.bind('<Return>', self.sectionEditor.new_paragraph)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        self._set_wc_mode()
        self.lift()
        self.isOpen = True

    def lift(self):
        """Bring window to the foreground and set the focus to the editor box.
        
        Extends the superclass method.
        """
        if self.state() == 'iconic':
            self.state('normal')
        super().lift()
        self.sectionEditor.focus()

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'
            # keeping the editor window open due to an XML error to be fixed before saving

        self.prefs['win_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def _set_editor_colors(self):
        cm = EditorView.colorMode.get()
        self.sectionEditor['fg'] = self.colorModes[cm][1]
        self.sectionEditor['bg'] = self.colorModes[cm][2]
        self.sectionEditor['insertbackground'] = self.colorModes[cm][1]

    def _set_wc_mode(self, *args):
        if EditorView.liveWordCount.get():
            self.bind('<KeyRelease>', self.show_wordcount)
            self.show_wordcount()
        else:
            self.unbind('<KeyRelease>')

    def show_status(self, message=None):
        """Display a message on the status bar."""
        self._statusBar.config(text=message)

