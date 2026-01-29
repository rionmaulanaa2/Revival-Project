# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSelectionDrone.py
from __future__ import absolute_import
from .ComSelectionBase import ComSelectionBase
import math3d
import world

class ComSelectionMecha(ComSelectionBase):
    BIND_EVENT = ComSelectionBase.BIND_EVENT.copy()
    BIND_EVENT.update({})

    def __init__(self):
        super(ComSelectionMecha, self).__init__()

    def do_model_binding(self, id_selector, mdl_selector, mdl_target):
        pass