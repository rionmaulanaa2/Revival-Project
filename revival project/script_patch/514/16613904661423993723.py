# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFAChooseMechaInfoWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr

class FFAChooseMechaInfoWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type):
        super(FFAChooseMechaInfoWidget, self).__init__(parent, panel)
        self.init_param()
        self.on_switch_to_mecha_type(mecha_type)

    def on_switch_to_mecha_type(self, mecha_type):
        self._cur_mecha_id = mecha_type
        self._on_show_ability()

    def init_param(self):
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._cur_mecha_id = None
        return

    def get_difficult_level(self, score):
        if 0 <= score < 30:
            return (2216, 'gui/ui_res_2/battle/ffa/img_ffa_mecha_tag_simple.png')
        if 30 <= score < 60:
            return (2217, 'gui/ui_res_2/battle/ffa/img_ffa_mecha_tag_mid.png')
        if score >= 60:
            return (2218, 'gui/ui_res_2/battle/ffa/img_ffa_mecha_tag_hard.png')

    def _on_show_ability(self, *args):
        conf = self._mecha_conf[str(self._cur_mecha_id)]
        score_range = conf.get('score_range', 50)
        score_armor = conf.get('score_armor', 50)
        score_move = conf.get('score_move', 50)
        score_difficult = conf.get('score_difficult', 50)
        score_support = conf.get('score_support', 50)
        score_list = [score_range, score_armor, score_move, score_support]
        for i in range(len(score_list)):
            score = score_list[i]
            temp = getattr(self.panel, 'temp_%d' % (i + 1))
            temp.GetItem(0).prog_mech_ability.SetPercentage(score)

        desc = get_text_by_id(conf.get('desc_mecha_text_id', 19094))
        self.panel.nd_speciality.lab_speciality.SetString(desc)
        difficult_text_id, difficult_bg = self.get_difficult_level(score_difficult)
        self.panel.nd_difficulty.lab_difficulty.SetString(get_text_by_id(difficult_text_id))
        self.panel.nd_difficulty.img_difficulty.SetDisplayFrameByPath('', difficult_bg)