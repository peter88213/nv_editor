"""Build a section editor novelibre plugin.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the novelibre project. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}nv_editor.py'
TARGET_FILE = f'{BUILD}nv_editor.py'


def main():
    os.makedirs(BUILD, exist_ok=True)
    inliner.run(SOURCE_FILE, TARGET_FILE, 'nveditorlib', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'nvlib', '../../novelibre/src/')
    print('Done.')


if __name__ == '__main__':
    main()
