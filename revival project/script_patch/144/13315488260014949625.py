# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETipsMgr.py
from common.framework import Singleton
from logic.gcommon.common_const.pve_const import TIP_TYPE_COMMON, TIP_TYPE_WARN, TIP_TYPE_BOSS, TIP_TYPE_SMALL, TIP_TYPE_BIG, TIP_TYPE_BOX_SHOP, TIP_TYPE_BUFF, TIP_TYPE_REGION, TIP_TYPE_TEAMMATE_DEAD, TIP_TYPE_TEAMMATE_QUIT, TIP_TYPE_TEAM_DEFEAT, TIP_TYPE_TEAM_REVIVE, TIP_TYPE_DONATE_BLESS
from logic.gcommon.common_const.battle_const import GRANBELM_PORTAL_REFRESH_TIPS, MAIN_NODE_COMMON_INFO
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.EntityManager import EntityManager
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex

class PVETipsMgr(Singleton):
    ALIAS_NAME = 'pve_tips_mgr'

    def init(self):
        self.init_params()
        self.init_ui()
        self.process_events(True)

    def init_params(self):
        self._pve_tips_ui = None
        self._pve_top_tips_ui = None
        self.tips_widgets = {}
        self.tips_widgets_sound = {}
        self.tips_queue = []
        self.tips_appearing_tag = False
        self._cur_tip_type = None
        self._cur_text_id = None
        self._cur_text_id_2 = None
        self._timer = None
        self._revive_timer = None
        self.showing_buff_id = None
        self.warning_tips_widget = None
        self.boss_tips_widget = None
        self.small_tips_widget = None
        self.big_tips_widget = None
        self.box_shop_show_widget = None
        self.buff_tips_widget = None
        self.region_tips_widget = None
        self.teammate_dead_tips_widget = None
        self.teammate_quit_tips_widget = None
        self.team_defeat_tips_widget = None
        self.team_revive_tips_widget = None
        self.donate_bless_tips_widget = None
        self.bless_conf = confmgr.get('bless_data', default=None)
        return

    def init_ui(self):
        self._init_tips_ui()
        self._init_tips_widget()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pve_level_tips': self.show_level_tips,
           'pve_boss_enter_sec_stage': self.show_boss_sec_stage_tips,
           'pve_show_box_shop_tips': self.show_box_shop_tips,
           'pve_show_buff_tips': self.show_buff_tips,
           'pve_fight_state_changed': self.on_fight_state_changed,
           'mecha_crashed_event': self.show_teammate_dead_tips,
           'pve_teammate_quit_event': self.show_teammate_quit_tips,
           'pve_team_defeat_event': self.show_team_defeat_tips,
           'pve_team_revive_event': self.show_team_revive_tips,
           'pve_team_revive_end_event': self.show_team_revive_end_tips,
           'on_pve_donate_bless': self.show_donate_bless_tips,
           'on_pve_handle_donate_bless': self.show_handle_donate_bless_tips,
           'on_pve_notify_donate_bless_result': self.show_donate_bless_tips_result
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def unregister_logic_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return

    def unregister_revive_logic_timer(self):
        if self._revive_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._revive_timer)
            self._revive_timer = None
        return

    def clear(self):
        self.clear_all()

    def clear_all(self):
        self.unregister_logic_timer()
        self.unregister_revive_logic_timer()
        for widget in six_ex.values(self.tips_widgets):
            if callable(widget):
                continue
            if widget and widget.isValid():
                widget.setVisible(False)

        self.showing_buff_id = None
        self.tips_appearing_tag = False
        self.tips_queue = []
        return

    def on_finalize(self):
        self.process_events(False)
        self.unregister_logic_timer()
        self.unregister_revive_logic_timer()
        self.init_params()
        global_data.ui_mgr.close_ui('PVETopTipsUI')

    def _init_tips_ui(self):
        pve_tips_ui = global_data.ui_mgr.get_ui('PVETipsUI')
        if not pve_tips_ui:
            pve_tips_ui = global_data.ui_mgr.show_ui('PVETipsUI', 'logic.comsys.battle.pve')
        self._pve_tips_ui = pve_tips_ui.get_widget()
        pve_top_tips_ui = global_data.ui_mgr.get_ui('PVETopTipsUI')
        if not pve_top_tips_ui:
            pve_top_tips_ui = global_data.ui_mgr.show_ui('PVETopTipsUI', 'logic.comsys.battle.pve')
        self._pve_top_tips_ui = pve_top_tips_ui.get_widget()

    def _init_tips_widget(self):
        self.warning_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_monster_coming', self._pve_tips_ui)
        self.warning_tips_widget.setVisible(False)
        self.boss_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_boss_coming', self._pve_top_tips_ui)
        self.boss_tips_widget.setVisible(False)
        self.small_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_reward_got', self._pve_tips_ui)
        self.small_tips_widget.setVisible(False)
        self.big_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_passing', self._pve_tips_ui)
        self.big_tips_widget.setVisible(False)
        self.box_shop_show_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_shop_appear', self._pve_tips_ui)
        self.box_shop_show_widget.setVisible(False)
        self.buff_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_passing_2', self._pve_tips_ui)
        self.buff_tips_widget.setVisible(False)
        self.showing_buff_id = None
        self.region_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_passing_2', self._pve_tips_ui)
        self.region_tips_widget.setVisible(False)
        self.teammate_dead_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_team_death', self._pve_tips_ui)
        self.teammate_dead_tips_widget.setVisible(False)
        self.teammate_quit_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_team_quit', self._pve_tips_ui)
        self.teammate_quit_tips_widget.setVisible(False)
        self.team_defeat_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_team_defeat', self._pve_tips_ui)
        self.team_defeat_tips_widget.setVisible(False)
        self.team_revive_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_team_revive', self._pve_tips_ui)
        self.team_revive_tips_widget.setVisible(False)
        self.donate_bless_tips_widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_passing_2', self._pve_top_tips_ui)
        self.donate_bless_tips_widget.setVisible(False)
        self.tips_widgets = {TIP_TYPE_WARN: self.warning_tips_widget,
           TIP_TYPE_BOSS: self.boss_tips_widget,
           TIP_TYPE_SMALL: self.small_tips_widget,
           TIP_TYPE_BIG: self.big_tips_widget,
           TIP_TYPE_BOX_SHOP: self.box_shop_show_widget,
           TIP_TYPE_BUFF: self.buff_tips_widget,
           TIP_TYPE_REGION: self.region_tips_widget,
           TIP_TYPE_TEAMMATE_DEAD: self.teammate_dead_tips_widget,
           TIP_TYPE_TEAMMATE_QUIT: self.teammate_quit_tips_widget,
           TIP_TYPE_TEAM_DEFEAT: self.team_defeat_tips_widget,
           TIP_TYPE_TEAM_REVIVE: self.team_revive_tips_widget,
           TIP_TYPE_DONATE_BLESS: self.donate_bless_tips_widget,
           TIP_TYPE_COMMON: self.show_common_tips
           }
        self.tips_widgets_sound = {TIP_TYPE_WARN: 'Play_ui_pve_warning',
           TIP_TYPE_BOSS: 'Play_ui_pve_boss_come'
           }
        return

    def show_tips_widget(self, tip_type, text_id, text_id_2, text_fix=None):
        widget = self.tips_widgets.get(tip_type)
        if not widget:
            return
        if callable(widget):
            widget(text_id)
            return
        for tip in self.tips_queue:
            if tip_type == tip[0] and text_id == tip[1] and text_id_2 == tip[2]:
                return

        if tip_type == self._cur_tip_type:
            if text_id == self._cur_text_id and text_id_2 == self._cur_text_id_2:
                return
        self.tips_queue.append([tip_type, text_id, text_id_2, text_fix])
        self.show_next_tips()

    def show_next_tips(self):
        if self.tips_appearing_tag:
            return
        else:
            if not self.tips_queue:
                return
            tip_type, text_id, text_id_2, text_fix = self.tips_queue.pop(0)
            widget = self.tips_widgets.get(tip_type)
            if not widget:
                return
            if callable(widget):
                return
            if getattr(widget, 'lab_text', None) and text_id:
                text = get_text_by_id(text_id).format(text_fix) if text_fix else get_text_by_id(text_id)
                widget.lab_text.SetString(text)
            if getattr(widget, 'lab_text_2', None) and text_id_2:
                widget.lab_text_2.SetString(get_text_by_id(text_id_2))
            ani_time = float(widget.GetAnimationMaxRunTime('show'))
            widget.setVisible(True)
            widget.PlayAnimation('show')
            self.tips_appearing_tag = True
            self._cur_tip_type = tip_type
            self._cur_text_id = text_id
            self._cur_text_id_2 = text_id_2
            sound = self.tips_widgets_sound.get(tip_type, None)
            sound and global_data.sound_mgr.post_event_2d_non_opt(sound, None)

            def delay_call():
                if not widget or not widget.isValid():
                    return
                else:
                    widget.setVisible(False)
                    widget.StopAnimation('show')
                    self.tips_appearing_tag = False
                    self._cur_tip_type = None
                    self._cur_text_id = None
                    self._cur_text_id_2 = None
                    self.unregister_logic_timer()
                    self.show_next_tips()
                    return

            self.unregister_logic_timer()
            self._timer = global_data.game_mgr.get_logic_timer().register(func=delay_call, interval=ani_time, times=1, mode=CLOCK)
            return

    def show_buff_tips(self, show, buff_id, text):
        widget = self.tips_widgets.get(TIP_TYPE_BUFF)
        if not widget or callable(widget):
            return
        else:
            if show:
                self.showing_buff_id = buff_id
                widget.lab_1.SetString(text)
                widget.setVisible(True)
                widget.PlayAnimation('show')
            elif self.showing_buff_id == buff_id:
                self.showing_buff_id = None
                widget.setVisible(False)
            return

    def show_level_tips(self, tip_type, text_id, text_id_2):
        self.show_tips_widget(tip_type, text_id, text_id_2)

    def show_boss_sec_stage_tips(self, tip_type, text_id, text_id_2):
        self.show_tips_widget(tip_type, text_id, text_id_2)

    def show_box_shop_tips(self):
        self.show_tips_widget(TIP_TYPE_BOX_SHOP, None, None)
        return

    def show_teammate_dead_tips(self, eid):
        if global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_is_mecha:
            if global_data.cam_lctarget.id != eid:
                mecha_entity = EntityManager.getentity(eid)
                if mecha_entity and mecha_entity.logic:
                    driver_id = mecha_entity.logic.sd.ref_driver_id
                    driver_entity = EntityManager.getentity(driver_id)
                    if driver_entity and driver_entity.logic:
                        text_fix = driver_entity.logic.ev_g_char_name()
                        self.show_tips_widget(TIP_TYPE_TEAMMATE_DEAD, 487, None, text_fix)
        return

    def show_teammate_quit_tips(self, char_name):
        text_fix = char_name
        self.show_tips_widget(TIP_TYPE_TEAMMATE_QUIT, 488, None, text_fix)
        return

    def show_team_defeat_tips(self):
        self.show_tips_widget(TIP_TYPE_TEAM_DEFEAT, None, None)
        return

    def show_team_revive_tips(self, rescuer_name):
        text = get_text_by_id(491).format(name=rescuer_name)
        widget = self.tips_widgets.get(TIP_TYPE_TEAM_REVIVE, None)
        if not widget:
            return
        else:
            widget.lab_text.SetString(text)
            self.show_tips_widget(TIP_TYPE_TEAM_REVIVE, None, None)

            def delay_call--- This code section failed: ---

 313       0  LOAD_CONST            1  -1
           3  LOAD_CONST            2  ('EndTransitionUI',)
           6  IMPORT_NAME           0  'logic.comsys.battle.Settle.EndTransitionUI'
           9  IMPORT_FROM           1  'EndTransitionUI'
          12  STORE_FAST            0  'EndTransitionUI'
          15  POP_TOP          

 314      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  LOAD_GLOBAL           2  'True'
          22  CALL_FUNCTION_256   256 
          25  POP_TOP          

 315      26  LOAD_DEREF            0  'self'
          29  LOAD_ATTR             3  'unregister_revive_logic_timer'
          32  CALL_FUNCTION_0       0 
          35  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 16

            self._revive_timer = global_data.game_mgr.get_logic_timer().register(func=delay_call, interval=3.33, times=1, mode=CLOCK)
            return

    def show_team_revive_end_tips(self):
        self.show_tips_widget(TIP_TYPE_BIG, 500, 501)

    def show_donate_bless_tips(self, char_name):
        widget = self.tips_widgets.get(TIP_TYPE_DONATE_BLESS, None)
        if not widget:
            return
        else:
            text = get_text_by_id(527).format(name=char_name)
            widget.lab_1.SetString(text)
            self.show_tips_widget(TIP_TYPE_DONATE_BLESS, None, None)
            return

    def show_handle_donate_bless_tips(self, char_name, bless_id, accepted):
        widget = self.tips_widgets.get(TIP_TYPE_DONATE_BLESS, None)
        if not widget:
            return
        else:
            bless_conf = self.bless_conf.get(str(bless_id), {})
            bless_name = get_text_by_id(bless_conf.get('name_id', 0))
            if accepted:
                text = get_text_by_id(528).format(name=char_name, bless=bless_name)
            else:
                text = get_text_by_id(529).format(name=char_name, bless=bless_name)
            widget.lab_1.SetString(text)
            self.show_tips_widget(TIP_TYPE_DONATE_BLESS, None, None)
            return

    def show_donate_bless_tips_result(self, char_name, bless_id, accepted):
        widget = self.tips_widgets.get(TIP_TYPE_DONATE_BLESS, None)
        if not widget:
            return
        else:
            bless_conf = self.bless_conf.get(str(bless_id), {})
            bless_name = get_text_by_id(bless_conf.get('name_id', 0))
            if accepted:
                text = get_text_by_id(519).format(name=char_name, bless=bless_name)
            else:
                text = get_text_by_id(520).format(name=char_name, bless=bless_name)
            widget.lab_1.SetString(text)
            self.show_tips_widget(TIP_TYPE_DONATE_BLESS, None, None)
            return

    def show_common_tips(self, text_id):
        message = {'i_type': GRANBELM_PORTAL_REFRESH_TIPS,'content_txt': get_text_by_id(text_id)}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    def on_fight_state_changed(self, state, is_boss=False):
        if state:
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_battlein', None)
        else:
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_battleout', None)
        return