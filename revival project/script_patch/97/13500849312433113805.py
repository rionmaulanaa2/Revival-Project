# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaBasicInfoProficiencyWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.mall_utils import mecha_has_owned_by_mecha_id
STATISTICS_INFO = [
 ('gui/ui_res_2/mech_display/icon_drive.png', 82099, '%dmin'),
 ('gui/ui_res_2/mech_display/icon_eliminated.png', 82100, '%d')]

class MechaBasicInfoProficiencyWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type):
        self.global_events = {'update_proficiency_event': self.on_update_proficiency,
           'update_proficiency_reward_event': self._check_has_unreceived_reward,
           'player_item_update_event': self.on_update_mecha_status
           }
        super(MechaBasicInfoProficiencyWidget, self).__init__(parent, panel)
        self.init_parameters()
        self.init_ui_event()
        self.on_switch_mecha_type(mecha_type)

    def on_switch_mecha_type(self, mecha_type):
        self.init_widget(str(mecha_type))

    def init_parameters(self):
        self._prof_conf = confmgr.get('proficiency_config', 'Proficiency')
        self._dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        self._mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content', default=[])
        self._reward_levels = confmgr.get('proficiency_config', 'RewardLevels')
        self._max_dan_lv = len(self._dan_conf)
        self._max_level = len(self._prof_conf)
        self._cur_mecha_type = None
        return

    def init_widget(self, mecha_type):
        if not global_data.player:
            return
        if self._cur_mecha_type == mecha_type:
            return
        if self._cur_mecha_type:
            self._cur_mecha_type = mecha_type
        self._cur_mecha_type = mecha_type
        level, proficiency = global_data.player.get_proficiency(self._cur_mecha_type)
        mecha_name = item_utils.get_mecha_name_by_id(self._cur_mecha_type)
        self.panel.lab_name.SetString(mecha_name)
        self.on_update_proficiency(mecha_type, level, proficiency)
        nd = self.panel
        has_mecha = mecha_has_owned_by_mecha_id(self._cur_mecha_type)
        nd.nd_proficiency.setVisible(has_mecha)
        nd.nd_proficiency_lock.setVisible(not has_mecha)
        self._check_has_unreceived_reward()

    def _check_has_unreceived_reward(self, *args):
        nd = self.panel
        need_tip = global_data.player.has_unreceived_prof_reward(self._cur_mecha_type)
        from logic.gutils import red_point_utils
        red_point_utils.show_red_point_template(nd.img_tips, need_tip, red_point_utils.RED_POINT_LEVEL_30)
        if need_tip:
            self.panel.PlayAnimation('reward_tips')
        else:
            self.panel.StopAnimation('reward_tips')

    def init_ui_event(self):
        nd = self.panel
        nd.nd_proficiency.btn_tips.BindMethod('OnClick', self.on_show_tips)
        nd.nd_proficiency.nd_proficiency_level.BindMethod('OnClick', self.on_show_details)

    def on_update_mecha_status(self):
        if self._cur_mecha_type:
            nd = self.panel
            if nd and nd.nd_proficiency and nd.nd_proficiency_lock:
                has_mecha = mecha_has_owned_by_mecha_id(self._cur_mecha_type)
                nd.nd_proficiency.setVisible(has_mecha)
                nd.nd_proficiency_lock.setVisible(not has_mecha)

    def on_show_tips(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(608082), get_text_by_id(608083))

    def on_show_details(self, btn, touch):
        from logic.comsys.mecha_display.MechaProficiencyDetailsUI import MechaProficiencyDetailsUI
        MechaProficiencyDetailsUI(None, self._cur_mecha_type)
        return

    def on_update_proficiency(self, mecha_type, level, proficiency, lv_up=False):
        if self._cur_mecha_type != mecha_type:
            return
        if level < self._max_level:
            upgrade_value = self._prof_conf.get(str(level + 1), {}).get('upgrade_value', 0)
        else:
            upgrade_value = self._prof_conf.get(str(level), {}).get('upgrade_value', 0)
            proficiency = upgrade_value
        nd = self.panel
        nd.lab_level.SetString('Lv%d' % level)
        if upgrade_value:
            nd.progress_exp.SetPercent(proficiency * 100.0 / upgrade_value)
        else:
            nd.progress_exp.SetPercent(100)
        dan_lv = self.get_dan_lv(level)
        self.update_nd_dan_lv(nd, dan_lv)

    def update_nd_dan_lv(self, nd, dan_lv, show_dan_level=True):
        if not show_dan_level:
            nd.img_proficiency_level.setVisible(False)
            nd.lab_proficiency_level.setVisible(False)
        else:
            icon_path = self._dan_conf.get(str(dan_lv), {}).get('icon_path', '')
            name = self._dan_conf.get(str(dan_lv), {}).get('name', 0)
            if icon_path:
                nd.img_proficiency_level.SetDisplayFrameByPath('', icon_path)
            if name:
                nd.lab_proficiency_level.SetString(get_text_by_id(name))

    def get_dan_lv(self, level):
        dan_lv = 1
        for dan_lv in range(1, self._max_dan_lv + 1):
            max_level = self._dan_conf[str(dan_lv)]['max_level']
            if level < max_level:
                break

        return dan_lv

    def on_click_proficiency(self, *args):
        has_mecha = mecha_has_owned_by_mecha_id(self._cur_mecha_type)
        if not has_mecha:
            return
        nd = self.panel.nd_details
        nd.nd_proficiency_reward.setVisible(True)
        self.panel.nd_details.PlayAnimation('proficiency_reward_appear')
        self.panel.nd_details.PlayAnimation('proficiency_reward_checking')

    def destroy(self):
        self._prof_conf = None
        self._dan_conf = None
        super(MechaBasicInfoProficiencyWidget, self).destroy()
        return