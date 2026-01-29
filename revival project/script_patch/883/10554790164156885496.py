# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Compat.py
import sys
PY2 = sys.version_info[0] == 2
PY3 = not PY2
if PY2:
    text_type = unicode
    string_types = basestring
    integer_types = (int, long)

    def iterkeys(d, **kw):
        return d.iterkeys(**kw)


    def itervalues(d, **kw):
        return d.itervalues(**kw)


    def iteritems(d, **kw):
        return d.iteritems(**kw)


    def iterlists(d, **kw):
        return d.iterlists(**kw)


else:
    text_type = str
    string_types = str
    integer_types = int

    def iterkeys(d, **kw):
        return iter(d.keys(**kw))


    def itervalues(d, **kw):
        return iter(d.values(**kw))


    def iteritems(d, **kw):
        return iter(d.items(**kw))


    def iterlists(d, **kw):
        return iter(d.lists(**kw))


del sys