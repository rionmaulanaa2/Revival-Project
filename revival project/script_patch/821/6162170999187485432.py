# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Meta/montageTrack.py
from __future__ import absolute_import
from . import TMontageRootBase, TrackMeta

@TrackMeta
class TMontageRoot(TMontageRootBase):
    _VALID_CHILDREN = TMontageRootBase._VALID_CHILDREN + [('\xe5\xad\x97\xe5\xb9\x95', 'TSubtitle'), ('\xe6\xb5\x81\xe9\x9f\xb3\xe9\xa2\x91\xe8\xbd\xa8\xe9\x81\x93', 'TWemAudio')]