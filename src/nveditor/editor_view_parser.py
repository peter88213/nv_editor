"""Provide a class for parsing novx section content, generating tags for the text box.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml import sax


class EditorViewParser(sax.ContentHandler):
    """A novx section content parser."""
    BULLET = '•'

    def __init__(self):
        super().__init__()
        self.textTag = ''
        self.xmlTag = ''
        self.update = False

        self.taggedText = None
        # tagged text, assembled by the parser

        self._list = None

    def feed(self, xmlString):
        """Feed a string file to the parser.
        
        Positional arguments:
            filePath: str -- novx document path.        
        """
        self.taggedText = []
        self._list = False
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        """Receive notification of character data.
        
        Overrides the xml.sax.ContentHandler method             
        """
        tag = self.textTag
        self.taggedText.append((content, tag))

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method     
        """
        tag = self.xmlTag
        suffix = ''
        if name == 'p' and not self._list:
            suffix = '\n'
        elif name in ('li', 'creator', 'date', 'note-citation'):
            suffix = '\n'
        elif name == 'ul':
            self._list = False
            suffix = '\n'
        if self.update:
            self.taggedText.append((f'</{name}>', tag))
        else:
            self.taggedText.append((f'</{name}>{suffix}', tag))

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method             
        """
        attributes = ''
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            attributes = f'{attributes} {attrKey}="{attrValue}"'
        tag = self.xmlTag
        suffix = ''
        if name == 'ul':
            self._list = True
            suffix = '\n'
        elif name == 'comment':
            suffix = '\n'
        elif name == 'note':
            suffix = '\n'
        self.taggedText.append((f'<{name}{attributes}>{suffix}', tag))
