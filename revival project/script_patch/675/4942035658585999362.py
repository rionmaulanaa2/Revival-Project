# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/BattleInfoSubWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from common.const.property_const import U_LV, U_EXP
from logic.gcommon.cdata import dan_data
from logic.gutils import role_head_utils
from logic.gutils.lv_template_utils import get_cur_lv_reward, init_lv_template, get_cur_lv_percentage
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gcommon.cdata.dan_data import get_dan_name_id
from logic.gcommon.common_const import statistics_const as sconst
from logic.client.const import player_battle_info_const as battle_const
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
SURVIVAL_MODES = [
 battle_const.RANK_MODE_SINGLE, battle_const.CUSTOM_MODE_SINGLE,
 battle_const.RANK_MODE_DOUBLE, battle_const.CUSTOM_MODE_DOUBLE,
 battle_const.RANK_MODE_SQUAD, battle_const.CUSTOM_MODE_SQUAD]
DEATH_MODES = [
 battle_const.RANK_MODE_DEATH, battle_const.CUSTOM_MODE_DEATH]
STATISTICS_INFO = [
 ('gui/ui_res_2/mech_display/icon_drive.png', 82099, '%dmin'),
 ('gui/ui_res_2/mech_display/icon_eliminated.png', 82100, '%d')]
G_NEW_MEMORY_STAT = True

class BattleInfoSubWidget(BaseUIWidget):

    def _register_press_button_event(self, nd_btn, nd_show):

        @nd_btn.unique_callback()
        def OnBegin(*args):
            nd_show.setVisible(True)

        @nd_btn.unique_callback()
        def OnEnd(*args):
            nd_show.setVisible(False)

        @nd_btn.unique_callback()
        def OnCancel(*args):
            nd_show.setVisible(False)

    def _register_press_button_event_new(self, nd_btn, uid, mecha_id):

        @nd_btn.unique_callback()
        def OnBegin(*args):
            self.show_memory_stat(nd_btn, uid, mecha_id)

        @nd_btn.unique_callback()
        def OnEnd(*args):
            self.hide_memory_stat()

        @nd_btn.unique_callback()
        def OnCancel(*args):
            self.hide_memory_stat()

    def __init__(self, parent_ui, panel):
        super(BattleInfoSubWidget, self).__init__(parent_ui, panel)

    def show_memory_stat(self, nd_btn, uid, mecha_id):
        from logic.comsys.mecha_display.mecha_memory.MechaMemorySimpleUI import MechaMemorySimpleUI
        ui = MechaMemorySimpleUI()
        if ui:
            ui.show_mecha_memory_simple_info(uid, mecha_id)
            wpos = nd_btn.ConvertToWorldSpacePercentage(50, 100)
            ui.set_position(wpos)

    def hide_memory_stat(self):
        global_data.ui_mgr.close_ui('MechaMemorySimpleUI')

    def show(self):
        self.panel.setVisible(True)
        animation_time = self.panel.GetAnimationMaxRunTime('in')

        def finished_in():
            self.panel.StopAnimation('in')
            self.panel.PlayAnimation('coin')

        self.panel.PlayAnimation('in')
        self.panel.SetTimeOut(animation_time, finished_in)

    def hide(self):
        self.panel.setVisible(False)

    def is_visible(self):
        if self.panel.IsVisible():
            return True
        return False

    def refresh(self, player_inf):
        lv = player_inf.get(U_LV, 1)
        exp = player_inf.get(U_EXP, 0)
        init_lv_template(self.panel.temp_level, lv)
        reward_item_no, gold = get_cur_lv_reward(lv + 1)
        self.panel.img_reward.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(reward_item_no))
        self.panel.nd_reward.setVisible(gold > 0)
        self.panel.lab_num.SetString(str(gold))
        dan_info = player_inf.get('dan_info', {})
        uid = player_inf.get('uid')
        is_settled = role_head_utils.init_dan_info(self.panel.nd_tier_now.temp_tier, uid)
        role_head_utils.init_dan_info(self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.temp_tier, uid)
        if not is_settled:
            self.panel.nd_tier_now.lab_none.setVisible(True)
            self.panel.nd_tier_now.temp_star.setVisible(False)
            self.panel.nd_tier_now.lab_star_num.setVisible(False)
            self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.lab_none.setVisible(True)
            self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.temp_star.setVisible(False)
            self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.lab_star_num.setVisible(False)
        else:
            dan_type_info = dan_info.get(dan_data.DAN_SURVIVAL, {})
            dan = dan_type_info.get('dan', 1)
            star_img = 'gui/ui_res_2/rank/icon_star_{}.png'.format(dan)
            self.panel.nd_tier_now.temp_star.img_star.SetDisplayFrameByPath('', star_img)
            self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.temp_star.img_star.SetDisplayFrameByPath('', star_img)
            cur_star = dan_type_info.get('star', 0)
            self.panel.nd_tier_now.lab_star_num.SetString('x%d' % (cur_star,))
            self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.lab_star_num.SetString('x%d' % (cur_star,))
            self.panel.nd_tier_now.temp_tips_tier_now.nd_tier_now.lab_name.SetString(get_dan_name_id(dan))
        max_dan_info = player_inf.get('history_max_dan', {})
        role_head_utils.set_role_dan(self.panel.nd_tier_toppest.temp_tier, max_dan_info)
        role_head_utils.set_role_dan(self.panel.nd_tier_toppest.temp_tips_tier_toppest.nd_tier_now.temp_tier, max_dan_info)
        max_dan_type_info = max_dan_info.get(dan_data.DAN_SURVIVAL, {})
        dan = max_dan_type_info.get('dan', 1)
        star_img = 'gui/ui_res_2/rank/icon_star_{}.png'.format(dan)
        self.panel.nd_tier_toppest.temp_star.img_star.SetDisplayFrameByPath('', star_img)
        self.panel.nd_tier_toppest.temp_tips_tier_toppest.nd_tier_now.temp_star.img_star.SetDisplayFrameByPath('', star_img)
        max_dan_star = max_dan_type_info.get('star', 0)
        self.panel.nd_tier_toppest.lab_star_num.SetString('x%d' % (max_dan_star,))
        self.panel.nd_tier_toppest.temp_tips_tier_toppest.nd_tier_now.lab_star_num.SetString('x%d' % (max_dan_star,))
        self.panel.nd_tier_toppest.temp_tips_tier_toppest.nd_tier_now.lab_name.SetString(get_dan_name_id(dan))
        top_mecha_info = player_inf.get('top_mechas', [])
        top_mecha_career = player_inf.get('top_mechas_career_statistics', [])
        if global_data.player:
            is_avatar = player_inf.get('uid') == global_data.player.uid
        else:
            is_avatar = False
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content', default=[])
        for idx, node in enumerate([self.panel.nd_mech.nd_1, self.panel.nd_mech.nd_2, self.panel.nd_mech.nd_3]):
            if idx < len(top_mecha_info):
                mecha_id, mecha_lv = top_mecha_info[idx]
                mecha_path = 'gui/ui_res_2/role/icon_mech_%s.png' % (mecha_id,)
                node.img_mech.SetDisplayFrameByPath('', mecha_path)
                node.lab_level.SetString('LV.%d' % (mecha_lv,))
                nd_statistic = getattr(node, 'temp_statistics_{}'.format(idx + 1))
                task_statistics_list = mecha_conf.get(str(mecha_id), {}).get('task_statistics', [])
                nd_statistic.list_temp_skill.SetInitCount(len(task_statistics_list))
                if not G_NEW_MEMORY_STAT:
                    if is_avatar:
                        self._register_press_button_event(node, nd_statistic)
                        for index, task_id in enumerate(task_statistics_list):
                            task_cur_prog = global_data.player.get_task_prog(task_id)
                            item = nd_statistic.list_temp_skill.GetItem(index)
                            item.img_skill.SetDisplayFrameByPath('', STATISTICS_INFO[index][0])
                            item.lab_skill_name.SetString(STATISTICS_INFO[index][1])
                            item.lab_skil_num.SetString(STATISTICS_INFO[index][2] % task_cur_prog)

                    elif top_mecha_career:
                        self._register_press_button_event(node, nd_statistic)
                        for index, data in enumerate(top_mecha_career[idx]):
                            item = nd_statistic.list_temp_skill.GetItem(index)
                            item.img_skill.SetDisplayFrameByPath('', STATISTICS_INFO[index][0])
                            item.lab_skill_name.SetString(STATISTICS_INFO[index][1])
                            item.lab_skil_num.SetString(STATISTICS_INFO[index][2] % data)

                elif is_avatar:
                    self._register_press_button_event_new(node, player_inf.get('uid'), mecha_id)
                elif top_mecha_career:
                    self._register_press_button_event_new(node, player_inf.get('uid'), mecha_id)
            else:
                node.setVisible(False)

        stat_inf = self.parent._stat_inf
        game_total_seconds = player_inf.get('total_game_time', 0)
        game_total_hours = round(game_total_seconds / 3600.0, 1)
        self.panel.nd_game_time.lab_star_num.SetString('%.1f' % game_total_hours)
        survival_seconds = 0.0
        for mode in SURVIVAL_MODES:
            prop = sconst.CAREER_STATISTICS_BATTLE_PROP(mode, sconst.SURVIVAL_TIME)
            survival_seconds += stat_inf.get(prop, 0)

        survival_total_hours = round(survival_seconds / 3600.0, 1)
        death_seconds = 0.0
        for mode in DEATH_MODES:
            prop = sconst.CAREER_STATISTICS_BATTLE_PROP(mode, sconst.SURVIVAL_TIME)
            death_seconds += stat_inf.get(prop, 0)

        death_total_hours = round(death_seconds / 3600.0, 1)
        others_total_hours = game_total_hours - survival_total_hours - death_total_hours
        if others_total_hours < 0:
            others_total_hours = 0.0
        self.panel.nd_game_time.temp_tips_game_time.lab_item_br.SetString(get_text_by_id(10381).format('%.1f' % survival_total_hours))
        self.panel.nd_game_time.temp_tips_game_time.lab_item_ffa.SetString(get_text_by_id(10382).format('%.1f' % death_total_hours))
        self.panel.nd_game_time.temp_tips_game_time.lab_item_weekly.SetString(get_text_by_id(10383).format('%.1f' % others_total_hours))
        exp_percent = get_cur_lv_percentage(lv, exp)
        self.panel.nd_exp.exp_progress.SetPercent(int(exp_percent * 100))
        per = int(exp_percent * 100)
        if 0 < per < 100:
            self.panel.nd_exp.progress_light.setVisible(True)
            self.panel.nd_exp.progress_light.SetPosition('%d%%' % int(exp_percent * 100), self.panel.nd_exp.progress_light.getPositionY())
        else:
            self.panel.nd_exp.progress_light.setVisible(False)