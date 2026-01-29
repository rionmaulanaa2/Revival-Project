# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySSBanner2.py
from __future__ import absolute_import
from logic.gutils import item_utils
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
SKIN_LST = [
 201800351, 201001245, 201800637, 201001441, 201800435, 201001633]

class LotterySSBanner2(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/lottery_ss_banner_2'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5

    def set_content(self):
        for idx, skin_id in enumerate(SKIN_LST):
            node = getattr(self.panel, 'temp_name_%s' % idx)
            item_utils.check_skin_tag(node.temp_quality.nd_kind, skin_id)
            name_text = item_utils.get_lobby_item_name(skin_id)
            node.lab_name.SetString(name_text)
            node.lab_name.ResizeAndPosition()