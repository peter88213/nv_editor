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

PLUGIN = 'nv_editor.py'
VERSION = ' @release'


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
        print('Removing outdated configuration file ...')
        os.remove(iniFile)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


pyz = os.path.dirname(__file__)


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

    print(f'*** Installing {PLUGIN} {VERSION} ***')

    # Install the plugin.
    homePath = str(Path.home()).replace('\\', '/')
    applicationDir = f'{homePath}/.novx'
    if os.path.isdir(applicationDir):
        pluginDir = f'{applicationDir}/plugin'
        os.makedirs(pluginDir, exist_ok=True)
        print(f'Copying "{PLUGIN}" ...')
        copy_file(PLUGIN, pluginDir)

        # Install the localization files.
        print('Copying locale ...')
        copy_tree('locale', applicationDir)

        # Install the icon files.
        print('Copying icons ...')
        copy_tree('icons', applicationDir)

        # Show a success message.
        print(
            (
                f'Sucessfully installed "{PLUGIN}" '
                f'at "{os.path.normpath(pluginDir)}".'
            )
        )

        # Remove the configuration file, if outdated.
        fix_ini(f'{applicationDir}/config/editor.ini')
    else:
        print(
            (
                'ERROR: Cannot find a novelibre installation '
                f'at "{os.path.normpath(applicationDir)}".'
            )
        )
    input('Press any key to quit.')
