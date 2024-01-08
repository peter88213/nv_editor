[Project homepage](https://peter88213.github.io/noveltree_editor) > Instructions for use

--- 

A simple [noveltree](https://peter88213.github.io/noveltree/) multi-section editor plugin based on the *tkinter.scrolledtext* widget.

---

# Installation

If [noveltree](https://peter88213.github.io/noveltree/) is installed, the setup script auto-installs the *nv_editor* plugin in the *noveltree* plugin directory.

The plugin adds an **Edit** entry to the *noveltree* **Section** menu, and an **Editor plugin Online help** entry to the **Help** menu.  

---

# Operation

---

## Launch the section editor

- Open a section editor window by double-clicking on a section or via the **Section > Edit** menu entry when a section is selected, or by hitting the *Enter* key.
- If the project is locked, editor windows cannot be opened.
- If you choose a section already open, the window will be brought to the foreground.

---

## Select text

- Select a word via double-clicking.
- Select a paragraph via triple-clicking.
- Extend the selection via **Shift-Arrow**.
- Extend the selection to the next word via **Ctrl-Shift-Arrow**.
- **Ctrl-A** selects the whole text.

---

## Copy/Paste text

- **Ctrl-C** copies the selected text to the clipboard.
- **Ctrl-X** cuts the selected text and moves it to the clipboard.
- **Ctrl-V** pastes the clipboard text content to the cursor position.

---

## Format text

- **Ctrl-I** places "Italic" markup around the selected text or at the cursor. If the selection is already italic, remove markup.
- **Ctrl-B** places "Bold" markup around the selected text or at the cursor. If the selection is already bold, remove markup.
- **Ctrl-M** removes "Bold" and "Italic" markup from the selection.

*The operations described above do not take effect on markup outsides the selection. Be sure not to nest markup by accident.*


### A note about formatting text

It is assumed that very few types of text markup are needed for a novel text:

- *Emphasized* (usually shown as italics).
- *Strongly emphasized* (usually shown as capitalized).
- *Citation* (paragraph visually distinguished from body text).

When exporting to ODT format, *noveltree* replaces these formattings as follows: 

- Text with `[i]Italic markup[/i]` is formatted as *Emphasized*.
- Text with `[b]Bold markup[/b]` is formatted as *Strongly emphasized*. 
- Paragraphs starting with `> ` are formatted as *Quote*.

---

## Undo/Redo

- **Ctrl-Z** undoes the last editing. Multiple undo is possible.
- **Ctrl-Y** redoes the last undo. Multiple redo is possible.

---

## Split a section

Via **File > Split at cursor position** or **Ctrl-Alt-S** you can split the section at the cursor position. 

- All the text from the cursor position is cut and pasted into a newly created section. 
- The new section is placed after the currently edited section.
- The new section is appended to the currently edited section.
- The new section has the same status as the currently edited section.  
- The new section is of the same type as the currently edited section.  
- The new section has the same viewpoint character as the currently edited section.  
- The editor loads the newly created section.

---

## Create a section

Via **File > Create section** or **Ctrl-Alt-N** you can create a section. 

- The new section is placed after the currently edited section.
- The new section is of the same type as the currently edited section.  
- The editor loads the newly created section.

---

## Word count

- The section word count is displayed at the status bar at the bottom of the window.
- By default, word count is updated manually, either by pressing the **F5** key, or via the **Word count > Update** menu entry.
- The word count can be updated "live", i.e. just while entering text. This is enabled via the **Word count > Enable live update** menu entry. 
- Live update is disabled by the **Word count > Disable live update** menu entry. 

**Please note**

*Live updating the word count is resource intensive and may slow down the program when editing big sections. This is why it's disabled by default.*

---

## Apply changes

- You can apply changes to the section with **Ctrl-S**. Then "Modified" status is displayed in *noveltree*.
- If the project is locked in *noveltree*, you will be asked to unlock it before changes can be applied.

---

## Exit 

- You can exit via **File > Exit**, or with **Ctrl-Q**.
- When exiting the program, you will be asked for applying changes.

---

# License

This is Open Source software, and the *nv_editor* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/noveltree_editor/blob/main/LICENSE) file.
