"""nv_editor installer library module. 

Version @release

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from shutil import copytree
from shutil import copy2
import os
import sys
import zipfile
from pathlib import Path
try:
    from tkinter import *
except ModuleNotFoundError:
    input(
        (
            'The tkinter module is missing. '
            'Please install the tk support package for your python3 version.'
        )
    )
    sys.exit(1)

PLUGIN = 'nv_editor.py'
VERSION = ' @release'

root = Tk()
processInfo = Label(root, text='')
message = []


def extract_file(sourceFile, targetDir):
    with zipfile.ZipFile(pyz) as z:
        z.extract(sourceFile, targetDir)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def fix_ini(iniFile):
    if not os.path.isfile(iniFile):
        return

    with open(iniFile, 'r') as f:
        text = f.read()
    if 'color_bg_bright = black' in text:
        output('Removing outdated configuration file ...')
        os.remove(iniFile)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


pyz = os.path.dirname(__file__)


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def main(zipped=True):
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.title('Setup')
    output(f'*** Installing {PLUGIN}{VERSION} ***\n')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Install the plugin.
    homePath = str(Path.home()).replace('\\', '/')
    applicationDir = f'{homePath}/.novx'
    if os.path.isdir(applicationDir):
        pluginDir = f'{applicationDir}/plugin'
        os.makedirs(pluginDir, exist_ok=True)
        output(f'Copying "{PLUGIN}" ...')
        copy_file(PLUGIN, pluginDir)

        # Install the localization files.
        output('Copying locale ...')
        copy_tree('locale', applicationDir)

        # Install the icon files.
        output('Copying icons ...')
        copy_tree('icons', applicationDir)

        # Show a success message.
        output(
            (
                f'Sucessfully installed "{PLUGIN}" '
                f'at "{os.path.normpath(pluginDir)}".'
            )
        )

        # Remove the configuration file, if outdated.
        fix_ini(f'{applicationDir}/config/editor.ini')
    else:
        output(
            (
                'ERROR: Cannot find a novelibre installation '
                f'at "{os.path.normpath(applicationDir)}".'
            )
        )
    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
