"""Generate German translation files for GNU gettext.

- Update the project's 'de.po' translation file.
- Generate the language specific 'novxlib.mo' dictionary.

Usage: 
translate_de.py
   
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from shutil import copyfile
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import translations
import msgfmt

APP_NAME = 'nv_editor'
PO_PATH = '../i18n/de.po'
MO_PATH = '../i18n/locale/de/LC_MESSAGES/nv_editor.mo'
MO_COPY = '../../novelibre/src/locale/de/LC_MESSAGES/nv_editor.mo'


def main(version='unknown'):
    if translations.main('de', app=APP_NAME, appVersion=version, json=True):
        print(f'Writing "{MO_PATH}" ...')
        msgfmt.make(PO_PATH, MO_PATH)
        copyfile(MO_PATH, MO_COPY)
    else:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        main()
