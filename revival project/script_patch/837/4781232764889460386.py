# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/client/const/ui_const.py
from __future__ import absolute_import
_reload_all = True
import six
if six.PY3:
    TH_SEP = '\\u200a'
    UNCOUNT_CHAR_UNICODE = TH_SEP + '\r\n\t '
    TH_SEP_UTF_8 = TH_SEP
else:
    TH_SEP = '\\u200a'.decode('raw_unicode_escape')
    UNCOUNT_CHAR_UNICODE = TH_SEP + '\r\n\t '
    UNCOUNT_CHAR_UTF_8 = UNCOUNT_CHAR_UNICODE.encode('utf-8')
    TH_SEP_UTF_8 = TH_SEP.encode('utf-8')