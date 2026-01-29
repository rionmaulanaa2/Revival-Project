# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathReviewWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.Death.TabBaseWidget import TabBaseWidget
from logic.gutils.item_utils import get_gun_pic_by_item_id
from logic.gcommon.ctypes.FightData import FD_MAKER_SOUL, FD_MAKER_MECHA, FD_MAKER_MONSTER
from common.cfg import confmgr

class DeathReviewWidget(TabBaseWidget):

    def __init__(self, panel, rise_panel):
        super(DeathReviewWidget, self).__init__(panel)
        self.rise_panel = rise_panel

    def init_parameters(self):
        pass

    def init_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.init_event(False)

    def on_show_defeat_info(self, killer_id, kill_info):
        temp_revive = self.panel.nd_revive_view
        maker_type = kill_info.get('maker_type', None)
        if maker_type is None:
            temp_revive.setVisible(False)
            return
        else:
            if maker_type == FD_MAKER_MONSTER:
                temp_revive.nd_method.nd_mech.setVisible(False)
                temp_revive.nd_method.nd_human.setVisible(False)
                temp_revive.nd_enemy.camp_icon.setVisible(False)
                temp_revive.nd_enemy.lab_name.SetString(18549)
                temp_revive.nd_score.lab_name.SetString(str(0))
            else:
                killer_name = kill_info['trigger_name']
                points = kill_info['points']
                trigger_faction = kill_info['trigger_faction']
                temp_revive.nd_enemy.lab_name.SetString(str(killer_name))
                temp_revive.nd_score.lab_name.SetString(str(points))
            if maker_type == FD_MAKER_MECHA:
                mecha_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
                mecha_id = kill_info.get('mecha_id')
                conf = mecha_conf[str(mecha_id)]
                icon_path = conf.get('icon_path', [])
                temp_revive.nd_method.nd_human.setVisible(False)
                temp_revive.nd_method.nd_mech.setVisible(True)
                temp_revive.nd_method.nd_mech.img_mech.SetDisplayFrameByPath('', icon_path[0])
            elif maker_type == FD_MAKER_SOUL:
                item_id = kill_info.get('item_id')
                if item_id:
                    gun_path = get_gun_pic_by_item_id(item_id)
                    temp_revive.nd_method.nd_human.img_gun.SetDisplayFrameByPath('', gun_path)
                else:
                    log_error('no item_id in kill info in event target_defeated_event')
                temp_revive.nd_method.nd_mech.setVisible(False)
                temp_revive.nd_method.nd_human.setVisible(True)
            return