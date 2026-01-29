# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleHitFeedBack.py
from __future__ import absolute_import
import time
from logic.gcommon import const
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import battle_const
from common.const.uiconst import NORMAL_LAYER_ZORDER_00, UI_TYPE_MESSAGE
from common.const import uiconst
from logic.gutils.client_unit_tag_utils import preregistered_tags
import cc
from logic.gcommon.common_const import ui_operation_const as uoc

class BattleHitFeedBack(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_hit_feedback'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_MESSAGE
    IS_FULLSCREEN = True
    STAY_TIME = 1
    INTERVAL_TIME = 0.5
    DEATH_SHOW_TIME = 0.5
    HIT_OTHER_ACTION_TAG = 10001
    NORMAL_PATH = 'gui/ui_res_2/battle/attack/atk_hit_normal.png'
    HEAD_HIT_PATH = 'gui/ui_res_2/battle/attack/img_down_1.png'

    def on_init_panel(self):
        super(BattleHitFeedBack, self).on_init_panel()
        self._mp_handler = {battle_const.FIGHT_EVENT_DAMAGE: self._handle_damage_event,
           battle_const.FIGHT_EVENT_MECHA_DEATH: self._handle_death_event,
           battle_const.FIGHT_EVENT_MONSTER_DEATH: self._handle_death_event,
           battle_const.FIGHT_EVENT_BLEED: self._handle_death_event,
           battle_const.FIGHT_EVENT_DEATH: self._handle_death_event,
           battle_const.FIGHT_EVENT_DEFEAT: self._handle_death_event,
           battle_const.FIGHT_EVENT_KILL_GROUP: self._handle_death_event,
           battle_const.FIGHT_EVENT_HIT_OTHER: self._handle_hit_other_event
           }
        self.panel.nd_hit.setVisible(False)
        self.panel.nd_down.setVisible(False)
        self._timer_id = None
        self._last_damage_time = time.time()
        self._interval_damage = 0
        self._damage_record = []
        self._hit_target = None
        self._death_show_time = 0
        self._hit_node = (self.panel.nd_hit.hit1, self.panel.nd_hit.hit2,
         self.panel.nd_hit.hit3, self.panel.nd_hit.hit4)
        self._down_normal_color = global_data.player.get_setting(uoc.DOWN_COLOR_VAL)
        self.init_event()
        self.on_update_down_color()
        return

    def init_event(self):
        emgr = global_data.emgr
        econf = {'change_down_color_event': self.on_update_down_color
           }
        emgr.bind_events(econf)

    def on_update_down_color(self):
        if global_data.player:
            cur_color_val = global_data.player.get_setting(uoc.DOWN_COLOR_VAL)
            self._down_normal_color = cur_color_val
            for child in self.panel.nd_people_down.GetChildren():
                child.SetColor(self._down_normal_color)

            for child in self.panel.nd_down.GetChildren():
                child.SetColor(self._down_normal_color)

    def deal_message(self, message):
        if type(message) in (list, tuple):
            event_type = message[0]
            self._hit_target = message[1]
            arg = [message[2], message[3]]
        else:
            event_type = message
            arg = message
        if event_type not in self._mp_handler:
            return
        handler = self._mp_handler[event_type]
        handler(arg)

    def _handle_hit_other_event(self, fade_out_time, scale, is_change_target):
        self.panel.nd_hit.setOpacity(255)
        self.panel.nd_hit.SetEnableCascadeOpacityRecursion(True)
        self.panel.nd_hit.stopActionByTag(self.HIT_OTHER_ACTION_TAG)
        fadeout_action = self.panel.nd_hit.runAction(cc.FadeOut.create(fade_out_time))
        fadeout_action.setTag(self.HIT_OTHER_ACTION_TAG)
        for one_node in self._hit_node:
            one_node.setScaleY(scale)

    def _handle_damage_event(self, args):
        damage = args[0]
        hit_part = args[1]
        self._head_shot_effect(hit_part)
        self.panel.nd_hit.setOpacity(255)
        self._last_damage_time = time.time()
        self._damage_record.append((time.time(), damage))
        if not self._timer_id:
            self._timer_id = global_data.game_mgr.register_logic_timer(self._tick_func, 0.05)
        self.panel.setVisible(True)
        self.panel.nd_hit.setVisible(True)

    def _handle_death_event(self, e_type):
        if e_type == battle_const.FIGHT_EVENT_KILL_GROUP:
            anim_name = 'ace_down'
        elif e_type in (battle_const.FIGHT_EVENT_MECHA_DEATH, battle_const.FIGHT_EVENT_MONSTER_DEATH):
            anim_name = 'down'
        else:
            anim_name = 'people_down'
        anim_time = self.panel.GetAnimationMaxRunTime(anim_name)
        self.panel.nd_hit.setOpacity(150)
        self.panel.setVisible(True)
        self.panel.StopAnimation(anim_name)
        self.panel.PlayAnimation(anim_name)
        global_data.emgr.hit_down_enemy.emit()
        if global_data.mecha and global_data.mecha.logic:
            mecha = global_data.mecha.logic
            if mecha and mecha.is_valid() and mecha.ev_g_is_avatar():
                mecha.send_event('E_KILL_ACTION')

    def _tick_func(self):
        now_time = time.time()
        if now_time - self._last_damage_time > self.STAY_TIME:
            self.panel.nd_hit.setVisible(False)
            self._reset()
        else:
            damage_record = []
            interval_damage = 0
            for damage_time, damage in self._damage_record:
                if now_time - damage_time > self.INTERVAL_TIME:
                    continue
                else:
                    damage_record.append((damage_time, damage))
                    interval_damage += damage

            self._damage_record = damage_record
            self._show_hit_effect(interval_damage)

    def on_finalize_panel(self):
        super(BattleHitFeedBack, self).on_finalize_panel()
        self._reset()

    def _reset(self):
        self._reset_timer()
        self._hit_target = None
        return

    def _reset_timer(self):
        if self._timer_id:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def _show_hit_effect(self, interval_damage):
        return
        if time.time() - self._death_show_time < self.DEATH_SHOW_TIME:
            return
        max_damage_limit = 100 if self._hit_target and self._hit_target.MASK & preregistered_tags.HUMAN_TAG_VALUE else 500
        scale_y = 0.5 + 0.5 * interval_damage / max_damage_limit
        if scale_y > 1:
            scale_y = 1
        for node in self._hit_node:
            node.setScaleY(scale_y)

    def _head_shot_effect(self, hit_part):
        path = self.HEAD_HIT_PATH if hit_part == const.HIT_PART_HEAD else self.NORMAL_PATH
        for node in self._hit_node:
            node.SetDisplayFrameByPath('', path)