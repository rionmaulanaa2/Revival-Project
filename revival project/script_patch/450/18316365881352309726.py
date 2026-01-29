# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Lib/xml/etree/SgmlopXMLTreeBuilder.py
from __future__ import absolute_import
from . import ElementTree

class TreeBuilder:

    def __init__(self, html=0):
        try:
            import sgmlop
        except ImportError:
            raise RuntimeError('sgmlop parser not available')

        self.__builder = ElementTree.TreeBuilder()
        if html:
            import six.moves.html_entities
            self.entitydefs.update(six.moves.html_entities.entitydefs)
        self.__parser = sgmlop.XMLParser()
        self.__parser.register(self)

    def feed(self, data):
        self.__parser.feed(data)

    def close(self):
        self.__parser.close()
        self.__parser = None
        return self.__builder.close()

    def finish_starttag(self, tag, attrib):
        self.__builder.start(tag, attrib)

    def finish_endtag(self, tag):
        self.__builder.end(tag)

    def handle_data(self, data):
        self.__builder.data(data)