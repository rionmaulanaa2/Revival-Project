# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Lib/xml/etree/HTMLTreeBuilder.py
from __future__ import absolute_import
import six
from six import unichr
import six.moves.html_entities
import re
import string
import sys
import mimetools
from . import ElementTree
AUTOCLOSE = ('p', 'li', 'tr', 'th', 'td', 'head', 'body')
IGNOREEND = ('img', 'hr', 'meta', 'link', 'br')
if sys.version[:3] == '1.5':
    is_not_ascii = re.compile('[\\x80-\\xff]').search
else:
    is_not_ascii = re.compile(eval('u"[\\u0080-\\uffff]"')).search
try:
    from six.moves.html_parser import HTMLParser
except ImportError:
    from sgmllib import SGMLParser

    class HTMLParser(SGMLParser):

        def unknown_starttag(self, tag, attrs):
            self.handle_starttag(tag, attrs)

        def unknown_endtag(self, tag):
            self.handle_endtag(tag)


class HTMLTreeBuilder(HTMLParser):

    def __init__(self, builder=None, encoding=None):
        self.__stack = []
        if builder is None:
            builder = ElementTree.TreeBuilder()
        self.__builder = builder
        self.encoding = encoding or 'iso-8859-1'
        HTMLParser.__init__(self)
        return

    def close(self):
        HTMLParser.close(self)
        return self.__builder.close()

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            http_equiv = content = None
            for k, v in attrs:
                if k == 'http-equiv':
                    http_equiv = string.lower(v)
                elif k == 'content':
                    content = v

            if http_equiv == 'content-type' and content:
                header = mimetools.Message(six.moves.StringIO.StringIO('%s: %s\n\n' % (http_equiv, content)))
                encoding = header.getparam('charset')
                if encoding:
                    self.encoding = encoding
        if tag in AUTOCLOSE:
            if self.__stack and self.__stack[-1] == tag:
                self.handle_endtag(tag)
        self.__stack.append(tag)
        attrib = {}
        if attrs:
            for k, v in attrs:
                attrib[string.lower(k)] = v

        self.__builder.start(tag, attrib)
        if tag in IGNOREEND:
            self.__stack.pop()
            self.__builder.end(tag)
        return

    def handle_endtag(self, tag):
        if tag in IGNOREEND:
            return
        lasttag = self.__stack.pop()
        if tag != lasttag and lasttag in AUTOCLOSE:
            self.handle_endtag(lasttag)
        self.__builder.end(tag)

    def handle_charref(self, char):
        if char[:1] == 'x':
            char = int(char[1:], 16)
        else:
            char = int(char)
        if 0 <= char < 128:
            self.__builder.data(six.int2byte(char))
        else:
            self.__builder.data(unichr(char))

    def handle_entityref(self, name):
        entity = six.moves.html_entities.entitydefs.get(name)
        if entity:
            if len(entity) == 1:
                entity = ord(entity)
            else:
                entity = int(entity[2:-1])
            if 0 <= entity < 128:
                self.__builder.data(six.int2byte(entity))
            else:
                self.__builder.data(unichr(entity))
        else:
            self.unknown_entityref(name)

    def handle_data(self, data):
        if isinstance(data, type('')) and is_not_ascii(data):
            data = six.text_type(data, self.encoding, 'ignore')
        self.__builder.data(data)

    def unknown_entityref(self, name):
        pass


TreeBuilder = HTMLTreeBuilder

def parse(source, encoding=None):
    return ElementTree.parse(source, HTMLTreeBuilder(encoding=encoding))


if __name__ == '__main__':
    import sys
    ElementTree.dump(parse(open(sys.argv[1])))