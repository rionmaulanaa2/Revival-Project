# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Lib/xml/etree/XMLTreeBuilder.py
from __future__ import absolute_import
from . import ElementTree

class TreeBuilder(ElementTree.XMLTreeBuilder):
    pass


class FancyTreeBuilder(TreeBuilder):

    def __init__(self, html=0):
        TreeBuilder.__init__(self, html)
        self._parser.StartNamespaceDeclHandler = self._start_ns
        self._parser.EndNamespaceDeclHandler = self._end_ns
        self.namespaces = []

    def _start(self, tag, attrib_in):
        elem = TreeBuilder._start(self, tag, attrib_in)
        self.start(elem)

    def _start_list(self, tag, attrib_in):
        elem = TreeBuilder._start_list(self, tag, attrib_in)
        self.start(elem)

    def _end(self, tag):
        elem = TreeBuilder._end(self, tag)
        self.end(elem)

    def _start_ns(self, prefix, value):
        self.namespaces.insert(0, (prefix, value))

    def _end_ns(self, prefix):
        pass

    def start(self, element):
        pass

    def end(self, element):
        pass