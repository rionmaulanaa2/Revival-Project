# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ArmRace/ArmRaceWeaponBarSelectUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.const.uiconst import SMALL_MAP_ZORDER
from logic.gcommon import const
from logic.gutils.dress_utils import get_weapon_default_fashion
from logic.gutils import item_utils
from logic.gutils.weapon_skin_utils import set_weapon_skin_pic_pos_and_scale
from logic.gcommon.common_const import weapon_const
import math
import cc

class ArmRaceWeaponBarSelectUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arms_race/change_weapon_arms_race'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def init_parameters(self):
        self.play_data_cfg = global_data.game_mode.get_cfg_data('play_data')
        self.gun_list = []
        self.level_up_num = 0
        self.is_uping = False

    def init_event(self):
        emgr = global_data.emgr
        econf = {'on_observer_pick_up_weapon': self.on_bullet_changed,
           'on_observer_weapon_bullet_num_changed': self.on_bullet_changed,
           'update_armrace_level_kill': self.armrace_level_up,
           'scene_player_setted_event': self.on_player_setted,
           'scene_observed_player_setted_event': self.on_player_setted
           }
        emgr.bind_events(econf)

    def on_player_setted(self, lplayer):
        self.panel.stopAllActions()
        self.level_up_num = 0
        self.is_uping = False
        armrace_level = global_data.armrace_battle_data.get_armrace_level()
        now_level_kill = global_data.armrace_battle_data.get_now_level_kill()
        self.armrace_level_up(armrace_level, now_level_kill, True)

    def init_panel(self):
        self.panel.temp_a.RecordAnimationNodeState('start')
        self.panel.temp_b.RecordAnimationNodeState('start')
        self.panel.temp_c.RecordAnimationNodeState('start')
        self.gun_list = ['temp_a', 'temp_b', 'temp_c']
        self.init_weapon_ui()
        self.init_progress_list()

    def get_gun_now(self):
        return getattr(self.panel, self.gun_list[0])

    def get_gun_next(self):
        return getattr(self.panel, self.gun_list[1])

    def get_gun_final(self):
        return getattr(self.panel, self.gun_list[2])

    def on_bullet_changed(self, *args):
        gun_now = self.get_gun_now()
        self.update_bullet_info(gun_now)

    def init_weapon_ui(self):
        if not global_data.cam_lplayer:
            return
        gun_now = self.get_gun_now()
        gun_next = self.get_gun_next()
        gun_final = self.get_gun_final()
        gun_final.setVisible(False)
        self.update_gun_now(gun_now, True)
        self.update_bullet_info(gun_now)
        self.update_gun_next(gun_next)

    def init_progress_list(self):
        armrace_level = global_data.armrace_battle_data.get_armrace_level()
        now_level_kill = global_data.armrace_battle_data.get_now_level_kill()
        self.update_progress_list(armrace_level, now_level_kill)

    def update_gun_now(self, node, is_init=False):
        if not global_data.cam_lplayer:
            return
        else:
            main_weapon_data = global_data.cam_lplayer.ev_g_wpbar_all_weapon()
            weapon = main_weapon_data.get(const.PART_WEAPON_POS_MAIN1, None)
            if weapon:
                weapon_data = weapon.get_data()
                item_no = weapon_data['item_id']
                armrace_level_weapon = global_data.battle.get_armrace_level_weapom()
                lobby_item_fashion = get_weapon_default_fashion(item_no)
                if lobby_item_fashion:
                    pic_path = item_utils.get_lobby_item_pic_by_item_no(lobby_item_fashion)
                else:
                    pic_path = item_utils.get_gun_pic_by_item_id(item_no, is_shadow=False)
                weapon_name = item_utils.get_item_name(item_no)
                node.img_gun_now.SetDisplayFrameByPath('', pic_path)
                node.lab_gun_name.SetString(weapon_name)
                if item_no == armrace_level_weapon[-1]:
                    node.lab_full_level_words.setVisible(True)
                    node.img_now.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_arms_race/weapon_list/img_full_level.png')
                if is_init:
                    node.PlayAnimation('start')
            return

    def update_gun_next(self, node):
        armrace_level = global_data.armrace_battle_data.get_armrace_level()
        armrace_level_weapon = global_data.battle.get_armrace_level_weapom()
        max_level = len(armrace_level_weapon)
        if armrace_level >= max_level:
            node.setVisible(False)
        else:
            next_item_no = armrace_level_weapon[armrace_level]
            lobby_item_fashion = get_weapon_default_fashion(next_item_no)
            if lobby_item_fashion:
                pic_path = item_utils.get_lobby_item_pic_by_item_no(lobby_item_fashion)
            else:
                pic_path = item_utils.get_gun_pic_by_item_id(next_item_no, is_shadow=False)
            weapon_name = item_utils.get_item_name(next_item_no)
            node.img_gun_now.SetDisplayFrameByPath('', pic_path)

    def update_bullet_info(self, node):
        if not global_data.cam_lplayer:
            return
        else:
            main_weapon_data = global_data.cam_lplayer.ev_g_wpbar_all_weapon()
            weapon = main_weapon_data.get(const.PART_WEAPON_POS_MAIN1, None)
            if weapon:
                max_bullet = weapon.get_bullet_cap()
                show_ratio = weapon.get_show_ratio()
                weapon_data = weapon.get_data()
                cur_bullet_num = weapon_data.get('iBulletNum', 0)
                reload_ratio = weapon.get_reload_ratio()
                bullet_type = weapon.get_bullet_type()
                bullet_color = '#SW'
                if 1 <= cur_bullet_num < math.ceil(max_bullet * 0.4):
                    bullet_color = '#SR'
                elif cur_bullet_num < 1:
                    bullet_color = '#SR'
                if bullet_type == weapon_const.ITEM_ID_INFINITE_BULLET:
                    show_bullet_num = max_bullet
                elif bullet_type == weapon_const.ITEM_ID_LIMITED_BULLET:
                    show_bullet_num = weapon.get_carry_bullet_num()
                else:
                    show_bullet_num = self.get_bag_bullet_num(bullet_type) * reload_ratio
                text_format_str = '<size={part_1_font_size}>{part_1_text}</size><size={part_2_font_size}>{part_2_text}</size>'
                text_args = {'part_1_font_size': 22,
                   'part_1_text': ''.join([bullet_color, str(int(cur_bullet_num * show_ratio))]),
                   'part_2_font_size': 18,
                   'part_2_text': ''.join(['#SW', '/', str(int(show_bullet_num * show_ratio))])
                   }
                context_txt = text_format_str.format(**text_args)
                node.tf_cur_bullet.SetString(context_txt)
            return

    def up_gun_level(self, level):
        self.is_uping = True

        def change_gun_list():
            now = self.gun_list.pop(0)
            self.gun_list.append(now)
            self.is_uping = False
            self.level_up_num -= 1
            if self.level_up_num > 0:
                self.up_gun_level(level + 1)

        armrace_level_weapon = global_data.battle.get_armrace_level_weapom()
        max_level = len(armrace_level_weapon)
        gun_now = self.get_gun_now()
        gun_next = self.get_gun_next()
        gun_final = self.get_gun_final()
        animation_time_in = gun_final.GetAnimationMaxRunTime('in')
        ac_list = [
         cc.CallFunc.create(lambda : gun_next.PlayAnimation('appear')),
         cc.DelayTime.create(0.2),
         cc.CallFunc.create(lambda : gun_next.PlayAnimation('change_01')),
         cc.CallFunc.create(lambda : gun_now.PlayAnimation('change_02')),
         cc.DelayTime.create(0.2),
         cc.CallFunc.create(lambda : self.update_gun_now(gun_next)),
         cc.CallFunc.create(lambda : self.update_bullet_info(gun_next)),
         cc.CallFunc.create(lambda : gun_final.RecoverAnimationNodeState('start')),
         cc.CallFunc.create(lambda : gun_final.setVisible(True)),
         cc.CallFunc.create(lambda : self.update_gun_next(gun_final)),
         cc.CallFunc.create(lambda : gun_final.PlayAnimation('in'))]
        if level >= max_level:
            ac_list.append(cc.DelayTime.create(0.07))
            ac_list.append(cc.CallFunc.create(lambda : gun_next.PlayAnimation('full_show')))
        ac_list.append(cc.DelayTime.create(animation_time_in))
        ac_list.append(cc.CallFunc.create(change_gun_list))
        self.panel.runAction(cc.Sequence.create(ac_list))

    def armrace_level_up(self, level, now_level_kill, level_up):
        if level_up:
            self.level_up_num += 1
            if not self.is_uping:
                self.up_gun_level(level)
        else:
            gun_next = self.get_gun_next()
            self.update_gun_next(gun_next)
        self.update_progress_list(level, now_level_kill)

    def update_progress_list(self, level, now_level_kill):
        armrace_level_weapon = global_data.battle.get_armrace_level_weapom()
        max_level = len(armrace_level_weapon)
        sub_act_list = self.panel.list_progress
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(max_level)
        for i in range(max_level):
            item_widget = sub_act_list.GetItem(i)
            true_idx = max_level - i
            if true_idx < level:
                item_widget.img_point_3.setVisible(True)
                item_widget.img_point_2.setVisible(False)
                item_widget.img_point_1.setVisible(False)
            elif true_idx == level:
                if now_level_kill == 0:
                    img_path = 'gui/ui_res_2/battle_arms_race/weapon_list/img_emp_point.png'
                elif now_level_kill == 1:
                    img_path = 'gui/ui_res_2/battle_arms_race/weapon_list/img_half_point.png'
                else:
                    img_path = 'gui/ui_res_2/battle_arms_race/weapon_list/img_full_point.png'
                item_widget.img_point_2.setVisible(True)
                item_widget.img_point_3.setVisible(False)
                item_widget.img_point_1.setVisible(False)
                item_widget.img_point_2.SetDisplayFrameByPath('', img_path)
                item_widget.lab_level.SetString(str(level))
            else:
                item_widget.img_point_1.setVisible(True)
                item_widget.img_point_2.setVisible(False)
                item_widget.img_point_3.setVisible(False)

        if level == 1:
            self.panel.lab_level_1.setVisible(False)
            self.panel.lab_level_13.setVisible(True)
            self.panel.lab_level_13.SetString(str(max_level))
        elif level == max_level:
            self.panel.lab_level_1.setVisible(True)
            self.panel.lab_level_1.SetString(str(1))
            self.panel.lab_level_13.setVisible(False)
        else:
            self.panel.lab_level_1.setVisible(True)
            self.panel.lab_level_1.SetString(str(1))
            self.panel.lab_level_13.setVisible(True)
            self.panel.lab_level_13.SetString(str(max_level))