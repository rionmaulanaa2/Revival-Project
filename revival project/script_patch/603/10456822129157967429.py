# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LArtTestMecha.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(client=('ComDataAnimator', 'com_art_check.ComArtCheckMechaModel', 'com_art_check.ComArtCheckCharacter',
                   'com_art_check.ComArtCheckMechaMoveAppr', 'com_art_check.ComArtCheckSender',
                   'com_art_check.ComArtCheckSocketLogic', 'com_art_check.ComArtCheckMechaShooter',
                   'com_character_ctrl.ComSpringAnim', 'com_character_ctrl.ComAnimMgr',
                   'com_character_ctrl.ComInput'))
class LArtTestMecha(Unit):
    MASK = 0