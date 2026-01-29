# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/predownload/hotfix_tempcode.py
import patch.predownload.uni_extend as uni_extend

def new_name_getter(self):
    if self._channel_delegate:
        return self._channel_delegate.get_name()
    else:
        return self._channel.name


uni_extend.ChannelWrapper.name = property(new_name_getter, None)