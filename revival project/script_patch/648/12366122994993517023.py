# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndStatisticsUI.py
from __future__ import absolute_import
import functools
from common.const import uiconst
from .EndSceneUIBase import EndSceneUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.end_statics_utils import init_end_person_statistics_new, init_end_teammate_statistics_new
from logic.gcommon.common_utils.local_text import get_text_by_id
PatchPath = 'gui/ui_res_2/icon/icon_coin.png'

class EndStatisticsUI(EndSceneUIBase):
    PANEL_CONFIG_NAME = 'end/end_statistics_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = EndSceneUIBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'btn_exit.btn_major.OnClick': '_on_click_btn_exit',
       'btn_details.OnClick': '_on_click_btn_show_details',
       'nd_stat_details.btn_close.OnClick': '_on_click_btn_close_details',
       'btn_report.OnClick': 'on_click_report_btn'
       })
    SHARE_TIPS_INFO = (
     'btn_share.btn_major', 3154, ('50%', '100%-30'))

    def on_init_panel(self, settle_dict, reward, teammate_num, teaminfo, achievement, is_done, total_fighter_num):
        super(EndStatisticsUI, self).on_init_panel()
        self._is_done = is_done
        self.show_details = False
        self._teaminfo = teaminfo
        self._teammate_num = teammate_num
        self._total_fighter_num = total_fighter_num
        self._settle_dict = settle_dict
        self._reward = reward
        self._init_teammate(teaminfo, achievement)
        self._init_statistics(teammate_num, settle_dict, achievement, total_fighter_num)
        self._play_animation()
        self.init_share_btn()
        self.init_event()
        self.panel.nd_stat_details.setVisible(False)
        self.panel.btn_exit.btn_major.SetText(get_text_by_id(80552))
        from logic.comsys.report.UserReportUI import UserReportUI
        report_target_list = UserReportUI.get_possible_report_targets()
        if len(report_target_list) > 0:
            self.panel.btn_report.setVisible(True)
        else:
            self.panel.btn_report.setVisible(False)
        from logic.gutils.new_template_utils import ModeSatSurveyButtonWidget
        self.comment_widget = ModeSatSurveyButtonWidget(self.panel.btn_comment)

    def _init_teammate(self, teaminfo, achievement):
        groupmate_info = global_data.player.logic.ev_g_teammate_infos()
        init_end_teammate_statistics_new(self.panel, groupmate_info, teaminfo, achievement)

    def _init_statistics(self, teammate_num, settle_dict, achievement, total_fighter_num):
        role_id = global_data.player.logic.get_value('G_ROLE_ID')
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        fashion_dict = global_data.player.logic.ev_g_fashion()
        clothing_id = fashion_dict.get(FASHION_POS_SUIT)
        mecha_id = settle_dict.get('mecha_id', 0)
        head_frame = global_data.player.get_head_frame()
        player_info = {'eid': global_data.player.id,
           'role_id': role_id,
           'clothing_id': clothing_id,
           'mecha_id': mecha_id,
           'head_frame': head_frame,
           'char_name': global_data.player.logic.ev_g_char_name()
           }
        init_end_person_statistics_new(self.panel, teammate_num, settle_dict, achievement, total_fighter_num, player_info)

    def _init_reward(self, settle_dict, reward):
        from logic.gutils.lv_template_utils import init_lv_node, is_full_lv, MIN_LV
        old_lv = settle_dict.get('lv', 1)
        old_exp = settle_dict.get('exp', 0)
        old_gold = settle_dict.get('gold', 0)
        gain_gold = reward.gold
        new_gold = old_gold + gain_gold
        gain_exp = reward.exp
        new_lv, new_exp = self._calc_new_lv_exp(old_lv, old_exp, gain_exp)
        cur_need_exp = self._get_need_exp_from_lv(old_lv)
        self._reward_info = {'old_lv': old_lv,
           'new_lv': new_lv,'old_exp': old_exp,
           'new_exp': new_exp,'old_gold': old_gold,
           'new_gold': new_gold}
        if is_full_lv(old_lv):
            self.panel.nd_level.setVisible(False)
            self.panel.nd_level_full.setVisible(True)
        else:
            self.panel.nd_level.setVisible(True)
            self.panel.nd_level_full.setVisible(False)
            self.panel.exp_progress.setPercent(old_exp * 100.0 / cur_need_exp)
            self.panel.lab_lv_gain.setString('+' + str(gain_exp))
            init_lv_node(self.panel.temp_level_new, old_lv)
            init_lv_node(self.panel.temp_level_next, old_lv + 1)

    def _calc_new_lv_exp(self, old_lv, old_exp, gain_exp):
        from logic.gutils.lv_template_utils import is_full_lv
        cur_lv, cur_exp = old_lv, old_exp
        while gain_exp > 0:
            if is_full_lv(cur_lv):
                return (cur_lv, 0)
            cur_need_exp = self._get_need_exp_from_lv(cur_lv)
            cur_need_exp -= cur_exp
            if gain_exp >= cur_need_exp:
                cur_lv, cur_exp = cur_lv + 1, 0
                gain_exp -= cur_need_exp
            else:
                cur_exp += gain_exp
                gain_exp = 0

        return (
         cur_lv, cur_exp)

    def _get_need_exp_from_lv(self, lv):
        from logic.gutils.lv_template_utils import get_lv_upgrade_need_exp
        need_exp = get_lv_upgrade_need_exp(lv)
        return need_exp

    def _play_animation(self):
        self.panel.PlayAnimation('appear')
        self.panel.DelayCall(self.panel.GetAnimationMaxRunTime('appear'), self._play_animation_step1)

    def _play_animation_step1(self):
        global_data.player.do_pending_survey()

    def _play_animation_step2(self):
        self._gaining_items = [
         'exp', 'gold']
        self._gaining_reward()

    def _play_animation_step3(self):
        if len(self._gaining_items) > 0 or self._is_done:
            return
        if global_data.game_mode.mode:
            return

    def _gaining_reward(self):
        cur_lv, new_lv = self._reward_info['old_lv'], self._reward_info['new_lv']
        cur_exp, new_exp = self._reward_info['old_exp'], self._reward_info['new_exp']
        cur_gold, new_gold = self._reward_info['old_gold'], self._reward_info['new_gold']
        self._gaining_reward_exp(cur_lv, new_lv, cur_exp, new_exp)
        self._gaining_reward_gold(cur_gold, new_gold)

    def _gaining_reward_exp(self, cur_lv, new_lv, cur_exp, new_exp):
        from logic.gutils.lv_template_utils import init_lv_node, is_full_lv
        if is_full_lv(cur_lv):
            self.panel.nd_level.setVisible(False)
            self.panel.nd_level_full.setVisible(True)
            return
        if cur_lv != new_lv:
            global_data.sound_mgr.play_ui_sound('upgrade')
        global_data.sound_mgr.play_ui_sound('experience_up')
        self.panel.nd_level.setVisible(True)
        self.panel.nd_level_full.setVisible(False)
        init_lv_node(self.panel.temp_level_new, cur_lv)
        init_lv_node(self.panel.temp_level_next, cur_lv + 1)
        cur_need_exp = self._get_need_exp_from_lv(cur_lv)
        self.panel.exp_progress.setPercent(cur_exp * 100.0 / cur_need_exp)
        if cur_lv == new_lv:
            duration = 2.0 * (new_exp - cur_exp) / cur_need_exp

            def end_cb():
                self._gaining_items.remove('exp')
                self._play_animation_step3()

            self.panel.exp_progress.SetPercent(new_exp * 100.0 / cur_need_exp, duration, end_cb=end_cb)
        else:
            duration = 2.0 * (cur_need_exp - cur_exp) / cur_need_exp
            end_cb = functools.partial(self._gaining_reward_exp, cur_lv + 1, new_lv, 0, new_exp)
            self.panel.exp_progress.SetPercent(100, duration, end_cb=end_cb)

    def _gaining_reward_gold(self, cur_gold, new_gold):
        self.panel.lab_coin_num.SetString(str(cur_gold))
        if cur_gold < new_gold:
            cur_gold = int(min(cur_gold + 50.0, new_gold))
            func = functools.partial(self._gaining_reward_gold, cur_gold, new_gold)
            self.panel.SetTimeOut(0.1, func)
        else:
            self._gaining_items.remove('gold')
            self._play_animation_step3()

    def _on_click_btn_exit(self, *args):
        if self.show_details:
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            SettleSystem().show_settle_exp(self._settle_dict, self._reward)
            self.close()
        else:
            self._on_click_btn_show_details()

    def _on_click_btn_report(self, *args):
        global_data.emgr.battle_show_message_event.emit(get_text_by_id(2139))

    def _on_click_btn_watch(self, *args):
        if global_data.player is not None and global_data.player.logic is not None:
            global_data.player.logic.send_event('E_REQ_SPECTATE')
        return

    def _on_click_btn_share(self, btn, touch):
        from logic.comsys.share.EndStaticsShareCreator import EndStaticsShareCreator
        if not self._share_content:
            share_creator = EndStaticsShareCreator()
            share_creator.create(None)
            self._share_content = share_creator
        self._share_content.init_end_person_nd(self._teammate_num, self._total_fighter_num, self._settle_dict)
        self._share_content.update_mecha_sprite_bg()
        from logic.comsys.share.ShareUI import ShareUI
        ShareUI(parent=self.panel).set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)
        return

    def init_share_btn(self):
        self._share_content = None

        @self.panel.btn_share.btn_major.callback()
        def OnClick(btn, touch):
            self._on_click_btn_share(btn, touch)

        return

    def init_event(self):
        global_data.emgr.player_first_success_share_event += self.on_first_success_share

    def on_first_success_share(self):
        from logic.gutils.share_utils import hide_share_tips
        hide_share_tips(self.panel.btn_share)

    def _on_click_btn_show_details(self, *args):
        self.panel.nd_stat_details.setVisible(True)
        if self.show_details is False:
            self.show_details = True
            self.panel.btn_exit.btn_major.SetText(get_text_by_id(80376))

    def _on_click_btn_close_details(self, *args):
        self.panel.nd_stat_details.setVisible(False)

    def on_finalize_panel--- This code section failed: ---

 400       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_share_content'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    49  'to 49'

 401      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  '_share_content'
          18  POP_JUMP_IF_FALSE    37  'to 37'

 402      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  '_share_content'
          27  LOAD_ATTR             2  'destroy'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          
          34  JUMP_FORWARD          0  'to 37'
        37_0  COME_FROM                '34'

 403      37  LOAD_CONST            0  ''
          40  LOAD_FAST             0  'self'
          43  STORE_ATTR            1  '_share_content'
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

 405      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             4  'destroy_widget'
          55  LOAD_CONST            2  'comment_widget'
          58  CALL_FUNCTION_1       1 
          61  POP_TOP          

 406      62  LOAD_GLOBAL           5  'super'
          65  LOAD_GLOBAL           6  'EndStatisticsUI'
          68  LOAD_FAST             0  'self'
          71  CALL_FUNCTION_2       2 
          74  LOAD_ATTR             7  'on_finalize_panel'
          77  CALL_FUNCTION_0       0 
          80  POP_TOP          
          81  LOAD_CONST            0  ''
          84  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_click_report_btn(self, btn, touch):
        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_END, REPORT_CLASS_BATTLE
        ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
        ui.report_battle_users([], True, True)
        ui.set_report_class(REPORT_CLASS_BATTLE)
        ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)
        ui.set_settle_info(self._settle_dict)