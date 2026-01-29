# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/WeaponBarSelectUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
import cc
import time
from common.const.uiconst import BASE_LAYER_ZORDER
from .WeaponBarBaseUI import WeaponBarBaseUI
from logic.gcommon import const
from common.framework import Functor
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gcommon.item import item_utility as iutil
from logic.gcommon.common_const import weapon_const
from logic.gutils.template_utils import get_item_quality
import math
import copy
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.dress_utils import get_weapon_default_fashion
PUNCH_PIC_PATH = 'gui/ui_res_2/item/gun/1011.png'
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_SKIN_SHOW_KEY
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const

class WeaponBarSelectBaseUI(WeaponBarBaseUI):
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    DLG_ZORDER = BASE_LAYER_ZORDER
    HOT_KEY_FUNC_MAP = {'switch_to_gun_1': (
                         'keyboard_try_switch_weapon', const.PART_WEAPON_POS_MAIN1),
       'switch_to_gun_2': (
                         'keyboard_try_switch_weapon', const.PART_WEAPON_POS_MAIN2),
       'switch_to_gun_3': (
                         'keyboard_try_switch_weapon', const.PART_WEAPON_POS_MAIN3),
       'switch_to_uzi': (
                       'keyboard_try_switch_weapon', const.PART_WEAPON_POS_MAIN_DF)
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_to_gun_1': {'node': 'nd_weapon_1.temp_pc'},'switch_to_gun_2': {'node': 'nd_weapon_2.temp_pc'},'switch_to_gun_3': {'node': 'nd_weapon_3.temp_pc'},'switch_to_uzi': {'node': ['nd_weapon_4.ccb_weapon_4.temp_pc', 'nd_weapon_4.ccb_weapon_4_sel.temp_pc']}}
    HOT_KEY_NEED_SCROLL_SUPPORT = True

    def on_init_panel(self):
        super(WeaponBarSelectBaseUI, self).on_init_panel()
        self._timer = 0
        self.last_pass_time = 0
        self.reload_cost_time = 0
        self.reload_pass_time = 0
        self._reload_time_scale = 0.0
        self._begin_roll_time = 0
        self._old_scale_anchorPoint = self.panel.ccb_weapon_4.getAnchorPoint()
        self._cur_mouse_dist = 0
        self._show_weapon_skin = True
        self.init_widget()
        self.init_custom_com()
        self.on_player_setted()

    def init_event(self):
        super(WeaponBarSelectBaseUI, self).init_event()
        self.process_event(True)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        super(WeaponBarSelectBaseUI, self).on_finalize_panel()
        self.unregister_timer()
        self.process_event(False)
        self.destroy_widget('custom_ui_com')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'settle_stage_event': self.on_create_settle_stage_ui,
           'on_reload_bullet_event': self.on_reload_bullet,
           'on_cancel_reload_event': self.on_cancel_reload,
           'on_begin_roll_event': self.on_begin_roll,
           'on_end_roll_event': self.on_roll_end,
           'improvise_highlight_on_time': self._on_improvise_highlight,
           'player_armor_changed': self.tick_armor_hp,
           'weapon_skin_ope_change_event': self.on_weapon_skin_ope_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_improvise_highlight(self):
        from logic.gcommon import const
        self._improvise_highlight_pos_list = (
         const.PART_WEAPON_POS_MAIN1,
         const.PART_WEAPON_POS_MAIN2,
         const.PART_WEAPON_POS_MAIN3)
        for pos in self._improvise_highlight_pos_list:
            normal, sel = self.get_weapon_ui_by_pos(pos)
            if normal and normal.HasAnimation('renovate'):
                normal.RecordAnimationNodeState('renovate', black_dict={'sp_weapon': {'visibility'}})
            if sel and sel.HasAnimation('renovate'):
                sel.RecordAnimationNodeState('renovate', black_dict={'sp_weapon': {'visibility'}})

    def init_widget(self):
        self.show_weapon_ui()
        self.switch_scale_ani = None
        self.weapon_pos_to_eid = {}
        self._renew_ani_sequence = {}
        self.weapon_widget_dict = {const.PART_WEAPON_POS_MAIN1: (
                                       self.panel.ccb_weapon_1, self.panel.ccb_weapon_1_sel),
           const.PART_WEAPON_POS_MAIN2: (
                                       self.panel.ccb_weapon_2, self.panel.ccb_weapon_2_sel),
           const.PART_WEAPON_POS_MAIN3: (
                                       self.panel.ccb_weapon_3, self.panel.ccb_weapon_3_sel),
           const.PART_WEAPON_POS_MAIN_DF: (
                                         self.panel.ccb_weapon_4, self.panel.ccb_weapon_4_sel)
           }
        self._init_improvise_highlight()
        for k, v in six.iteritems(self.weapon_widget_dict):
            for ccb_btn in v:
                ccb_btn.btn_weapon.disabled = False
                ccb_btn.btn_weapon.EnableCustomState(True)
                ccb_btn.btn_weapon.SetNoEventAfterMove(True, '10w')
                ccb_btn.anim_timer = None

            self._renew_ani_sequence[k] = []

        self.init_ui_event()
        return

    @execute_by_mode(True, (game_mode_const.GAME_MODE_CONCERT,))
    def show_weapon_ui(self):
        for nd in (self.panel.nd_weapon_2, self.panel.nd_weapon_3, self.panel.nd_weapon_4):
            nd.setVisible(False)

    def on_player_setted(self):
        super(WeaponBarSelectBaseUI, self).on_player_setted()
        self.init_ui_event()

    def init_ui_event(self):
        player = global_data.player
        if not player or not player.logic:
            return
        self._show_weapon_skin = global_data.player.get_setting_2(WEAPON_BAR_SKIN_SHOW_KEY)
        if player.logic.ev_g_is_in_spectate():
            self.panel.SetTouchEnabledRecursion(False)
            global_data.emgr.scene_observed_player_setted_event += self.on_enter_observe
            global_data.emgr.on_observer_join_mecha += self.on_join_mecha
            global_data.emgr.on_observer_leave_mecha += self.on_leave_mecha
        else:
            self.panel.SetTouchEnabledRecursion(True)
            self.bind_weapon_btn_click_event(self.ccb_weapon_1, self.ccb_weapon_1_sel, Functor(self.on_click_on_weapon_btn, const.PART_WEAPON_POS_MAIN1))
            self.bind_weapon_btn_click_event(self.ccb_weapon_2, self.ccb_weapon_2_sel, Functor(self.on_click_on_weapon_btn, const.PART_WEAPON_POS_MAIN2))
            self.bind_weapon_btn_click_event(self.ccb_weapon_3, self.ccb_weapon_3_sel, Functor(self.on_click_on_weapon_btn, const.PART_WEAPON_POS_MAIN3))
            self.bind_weapon_btn_click_event(self.ccb_weapon_4, self.ccb_weapon_4_sel, Functor(self.on_click_on_weapon_btn, const.PART_WEAPON_POS_MAIN_DF))
            self.panel.nd_background.setVisible(True)

    def on_weapon_skin_ope_changed(self):
        if not global_data.player:
            return
        self._show_weapon_skin = global_data.player.get_setting_2(WEAPON_BAR_SKIN_SHOW_KEY)
        print('ZHELI qucuole ma ?', self._show_weapon_skin)
        import traceback
        traceback.print_stack()
        self.update_weapon_ui()

    def bind_weapon_btn_click_event(self, btn_widget, btn_select_widget, click_callback):
        btn_widget.btn_weapon.BindMethod('OnClick', click_callback)
        btn_select_widget.btn_weapon.BindMethod('OnClick', click_callback)

    def on_create_settle_stage_ui(self, *args):
        pass

    def on_enter_observe(self, ltarget):
        if not ltarget:
            return
        if ltarget.ev_g_in_mecha('Mecha'):
            self.panel.SetTouchEnabledRecursion(False)
            self.add_hide_count(self.__class__.__name__)
        elif self.get_show_count(self.__class__.__name__) < 0:
            self.add_show_count(self.__class__.__name__)
        self.update_weapon_ui()

    def init_weapon_info(self):
        self.update_weapon_ui()
        self.check_renew_weapon(True)

    def update_weapon_ui(self, is_init=False):
        if not global_data.cam_lplayer:
            return
        if self.is_in_pick_ani:
            return
        self.update_weapon_item_visible()
        self.update_all_main_weapon_widgets()

    def on_click_on_weapon_btn(self, weapon_pos, *args):
        player = global_data.cam_lplayer
        if not player:
            return
        else:
            if player.id != global_data.player.id:
                return
            weapon_info = player.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
            weapon_data = None if weapon_info is None else weapon_info.get_data()
            if player.share_data.ref_wp_bar_cur_pos != weapon_pos:
                if weapon_data:
                    switch_pos = weapon_pos
                    player.send_event('E_TRY_SWITCH', switch_pos)
                    global_data.emgr.restart_avatar_fire_by_ui.emit()
                    return
                else:
                    player.send_event('E_TRY_CONFIG_WEAPON', weapon_pos)
                    return

            if weapon_data:
                cur_bullet_num = weapon_data.get('iBulletNum', 0)
                max_bullet = weapon_info.get_bullet_cap()
                if cur_bullet_num != max_bullet:
                    player.send_event('E_TRY_RELOAD')
            return

    def update_all_main_weapon_widgets(self, need_refresh=False):
        main_weapon_pos_list = self.ALL_MAIN_WEAPON
        main_weapon_data = self.get_weapon_data(True) or {}
        for weapon_pos in main_weapon_pos_list:
            weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
            weapon_object = main_weapon_data.get(weapon_pos, None)
            if hasattr(weapon_ui_tuple[0], 'img_weapon_num') and weapon_ui_tuple[0].img_weapon_num:
                weapon_ui_tuple[0].img_weapon_num.setVisible(not bool(weapon_object))
            for idx, weapon_ui in enumerate(weapon_ui_tuple):
                self.update_main_weapon_info(weapon_ui, weapon_pos, weapon_object, idx=idx)

        self.tick_armor_hp()
        need_switch_to_small = True
        target_pos, is_custom = self.get_df_node_custom_target_pos(need_switch_to_small)
        ani_name = 'switch_to_small' if need_switch_to_small else 'switch_to_big'
        if ani_name != self.switch_scale_ani or need_refresh:
            if ani_name == 'switch_to_small' and not is_custom:
                self.panel.PlayAnimation(ani_name)
            else:
                self.panel.nd_weapon_4.setPosition(target_pos)
            weapon_ui_tuple = self.get_weapon_ui_by_pos(const.PART_WEAPON_POS_MAIN_DF)
            for ui in weapon_ui_tuple:
                ui and self.switch_scale_ani and ui.StopAnimation(self.switch_scale_ani)
                ui and ui.PlayAnimation(ani_name)
                target_anchor = self._old_scale_anchorPoint
                if ani_name == 'switch_to_small':
                    if is_custom:
                        target_anchor = cc.Vec2(0.5, 0.5)
                if ui:
                    if abs(target_anchor.x - ui.getAnchorPoint().x) > 0.05:
                        self.switch_node_anchorPoint(ui, target_anchor)

            self.switch_scale_ani = ani_name
        return

    def get_df_node_custom_target_pos(self, switch_to_small):
        custom_pos = None
        query_node_name = 'nd_custom_4' if switch_to_small else 'nd_weapon_3'
        q_nd = getattr(self.panel, query_node_name)
        is_custom = False
        if self.custom_ui_com:
            set_key = self.custom_ui_com.custom_keys[0] if len(self.custom_ui_com.custom_keys) > 0 else ''
            nd_conf = self.custom_ui_com.get_panel_node_custom_data(self.__class__.__name__, query_node_name, set_key)
            if nd_conf and 'pos' in nd_conf:
                pos = nd_conf['pos']
                pos = copy.deepcopy(pos)
                real_width = global_data.ui_mgr.design_screen_size.width
                if global_data.player:
                    width = global_data.player.get_cur_custom_setting_resolution_data('human')
                    if width != real_width:
                        pos['x'] = float(pos['x']) * real_width / width
                custom_pos = cc.Vec2(pos['x'], pos['y'])
                if global_data.player and global_data.player.is_cur_custom_setting_old_data('human'):
                    custom_pos = q_nd.getParent().convertToWorldSpace(custom_pos)
                is_custom = True
            else:
                custom_pos = q_nd.getParent().convertToWorldSpace(q_nd.getPosition())
        lpos = None
        if custom_pos:
            wpos = custom_pos
            lpos = self.panel.nd_weapon_4.getParent().convertToNodeSpace(wpos)
        return (lpos, is_custom)

    def switch_node_anchorPoint(self, nd, new_anchor):
        old_pos = nd.getPosition()
        sz = nd.getContentSize()
        old_chor = nd.getAnchorPoint()
        x_diff = new_anchor.x - old_chor.x
        new_pos_x = old_pos.x + x_diff * sz.width
        nd.setAnchorPoint(new_anchor)
        nd.setPositionX(new_pos_x)

    def get_weapon_ui_by_pos(self, pos):
        return self.weapon_widget_dict.get(pos, (None, None))

    def update_weapon_item_visible(self):
        cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        for pos, ccb_btn_tuple in six.iteritems(self.weapon_widget_dict):
            ccb_btn, ccb_btn_sel = ccb_btn_tuple
            pos_equal = pos == cur_weapon_pos
            ccb_btn.setVisible(not pos_equal)
            ccb_btn_sel.setVisible(pos_equal)

    def register_timer(self, ccb_btn_sel):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=lambda : self.set_progress_time(ccb_btn_sel), interval=0.033, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def set_progress_time(self, ccb_btn_sel):
        from common import utilities
        now = time.time()
        pass_time = (now - self.last_pass_time) * (1.0 + self._reload_time_scale)
        self.last_pass_time = now
        self.reload_pass_time += pass_time
        left_time = self.reload_cost_time - self.reload_pass_time
        left_time = max(0, left_time)
        ccb_btn_sel.progress_reload.SetPercentage(utilities.safe_percent(self.reload_pass_time, self.reload_cost_time))
        if left_time <= 0:
            self.on_cancel_reload()

    def on_reload_bullet(self, reload_time, times, *args):
        from data import rush_arg
        if not global_data.cam_lplayer:
            return
        cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        if not cur_weapon_pos:
            return
        ccb_btn_sel = self.get_weapon_ui_by_pos(cur_weapon_pos)[1]
        self.last_pass_time = time.time()
        left_time = self.last_pass_time - self._begin_roll_time
        if left_time > rush_arg.DEFAULT_ROLL_DURATION:
            left_time = 0
        left_time = max(0, left_time)
        self.reload_cost_time = reload_time + left_time
        self.reload_pass_time = 0
        ccb_btn_sel.progress_reload.setVisible(True)
        self.register_timer(ccb_btn_sel)

    def on_cancel_reload(self, *args):
        if not global_data.cam_lplayer:
            return
        cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        if not cur_weapon_pos:
            return
        self.unregister_timer()
        ccb_btn_sel = self.get_weapon_ui_by_pos(cur_weapon_pos)[1]
        ccb_btn_sel.progress_reload.SetPercentage(0)
        ccb_btn_sel.progress_reload.setVisible(False)

    def on_begin_roll(self, *args):
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_reload():
            self._reload_time_scale = global_data.cam_lplayer.ev_g_attr_get('fRollReloadSpeedFactor', 0.0)
        self._begin_roll_time = time.time()

    def on_roll_end(self, *args):
        self._reload_time_scale = 0.0

    def tick_armor_hp(self, *args):
        need_tick = False
        main_weapon_data = self.get_weapon_data(True) or {}
        main_weapon_list = self.ALL_MAIN_WEAPON
        for weapon_pos in main_weapon_list:
            weapon_object = main_weapon_data.get(weapon_pos)
            weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
            for weapon_ui in weapon_ui_tuple:
                if weapon_ui and weapon_ui.isVisible():
                    need_tick = self.update_armor_hp(weapon_ui, weapon_object) or need_tick

        tag = 10086
        self.panel.weapon_2.stopActionByTag(tag)
        if need_tick:
            self.panel.weapon_2.DelayCallWithTag(0.05, self.tick_armor_hp, tag)

    def update_armor_hp(self, weapon_ui_item, wp):
        if not wp or not wp.check_shield_owned():
            weapon_ui_item.nd_shield.setVisible(False)
            return False
        from logic.gcommon.ctypes.Armor import Armor
        from logic.gcommon import time_utility as tutil
        is_recovering, can_open_shield, cur_hp, max_hp = Armor.get_recovering_info(wp.get_data(), tutil.time())
        visible = cur_hp < max_hp
        weapon_ui_item.nd_shield.setVisible(visible)
        if visible:
            weapon_ui_item.nd_broke.setVisible(not can_open_shield)
            weapon_ui_item.nd_broke.img_mask.setVisible(not wp.check_can_equip())
            if can_open_shield:
                texture_path = 'gui/ui_res_2/battle/progress/img_sheild_recover_1.png'
            else:
                texture_path = 'gui/ui_res_2/battle/progress/img_sheild_ban_progress_1.png'
            weapon_ui_item.progress_bar.SetProgressTexture(texture_path)
            weapon_ui_item.progress_bar.SetPercentage(100.0 * cur_hp / max_hp)
        return is_recovering

    def update_bullet_info(self, weapon_ui_item, wp):
        if not wp:
            return
        max_bullet = wp.get_bullet_cap()
        show_ratio = wp.get_show_ratio()
        weapon_data = wp.get_data()
        cur_bullet_num = weapon_data.get('iBulletNum', 0)
        iReloadRatio = wp.get_reload_ratio()
        bullet_type = wp.get_bullet_type()
        bullet_color = '#SW'
        if 1 <= cur_bullet_num < math.ceil(max_bullet * 0.4):
            bullet_color = '#SR'
        elif cur_bullet_num < 1:
            bullet_color = '#SR'
        if bullet_type == weapon_const.ITEM_ID_INFINITE_BULLET:
            show_bullet_num = max_bullet
        elif bullet_type == weapon_const.ITEM_ID_LIMITED_BULLET:
            show_bullet_num = wp.get_carry_bullet_num()
        else:
            show_bullet_num = self.get_bag_bullet_num(bullet_type) * iReloadRatio
        text_format_str = '<size={part_1_font_size}>{part_1_text}</size><size={part_2_font_size}>{part_2_text}</size>'
        text_args = {'part_1_font_size': 22,
           'part_1_text': ''.join([bullet_color, str(int(cur_bullet_num * show_ratio))]),
           'part_2_font_size': 18,
           'part_2_text': ''.join(['#SW', '/', str(int(show_bullet_num * show_ratio))])
           }
        context_txt = text_format_str.format(**text_args)
        weapon_ui_item.tf_cur_bullet.SetString(context_txt)

    def update_gun_widget(self, weapon_ui_item, weapon, idx=0):
        weapon_data = weapon.get_data()
        item_no = weapon_data['item_id']
        if self._show_weapon_skin:
            lobby_item_fashion = weapon_data.get('fashion', {}).get(FASHION_POS_SUIT, None) or get_weapon_default_fashion(item_no)
        else:
            lobby_item_fashion = get_weapon_default_fashion(item_no)
        if lobby_item_fashion:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(lobby_item_fashion)
        else:
            pic_path = item_utils.get_gun_pic_by_item_id(item_no, is_shadow=False)
        from logic.gutils.weapon_skin_utils import set_weapon_skin_pic_pos_and_scale
        set_weapon_skin_pic_pos_and_scale(weapon_ui_item.sp_weapon, lobby_item_fashion, item_no)
        level = get_item_quality(item_no)
        tail = 'btn_change_l_choose' if idx == 1 else 'btn_change_l_nml'
        path = 'gui/ui_res_2/battle/button/' + tail + '_%s.png' % str(level)
        weapon_ui_item.img_weapon_level.SetDisplayFrameByPath('', path)
        weapon_ui_item.img_weapon_level.setVisible(True)
        weapon_ui_item.sp_weapon.SetDisplayFrameByPath('', pic_path)
        if hasattr(weapon_ui_item, 'icon_type') and weapon_ui_item.icon_type:
            weapon_ui_item.icon_type.setVisible(False)
            if weapon and weapon.is_multi_wp():
                wp_id = weapon.get_item_id()
                mode_pic = confmgr.get('firearm_res_config', str(wp_id), 'cModeBarPic')
                if mode_pic:
                    weapon_ui_item.icon_type.setVisible(True)
                    weapon_ui_item.icon_type.SetDisplayFrameByPath('', mode_pic)
        return

    def update_widgets_visible(self, weapon_ui_item, is_vis):
        weapon_ui_item.sp_weapon.setVisible(is_vis)
        weapon_ui_item.tf_cur_bullet.setVisible(is_vis)
        if weapon_ui_item.icon_reload:
            weapon_ui_item.icon_reload.setVisible(is_vis)
            weapon_ui_item.icon_reload_2.setVisible(is_vis)

    def update_main_weapon_info(self, weapon_ui_item, weapon_pos, weapon, play_ani=False, idx=0):
        self.update_widgets_visible(weapon_ui_item, bool(weapon))
        if not weapon:
            weapon_ui_item.img_weapon_level.setVisible(False)
            return
        self.update_gun_widget(weapon_ui_item, weapon, idx=idx)
        self.update_bullet_info(weapon_ui_item, weapon)

    def play_renew_animation(self, weapon_pos, itype=None):
        weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
        wp = global_data.cam_lplayer.share_data.ref_wp_bar_mp_weapons.get(weapon_pos) if global_data.cam_lplayer else None
        if wp and self._show_weapon_skin:
            lobby_item_fashion = wp.get_fashion().get(FASHION_POS_SUIT, None) or get_weapon_default_fashion(itype)
        else:
            lobby_item_fashion = get_weapon_default_fashion(itype)
        for weapon_ui in weapon_ui_tuple:
            if not weapon_ui.isVisible():
                continue
            weapon_ui.parts.setVisible(False)
            vis_change_attr_list = ['renew3', 'renew2']
            if itype is not None:
                if not item_utils.is_gun(itype):
                    pic_path = item_utils.get_item_pic_by_item_no(itype)
                elif lobby_item_fashion:
                    pic_path = item_utils.get_lobby_item_pic_by_item_no(lobby_item_fashion)
                else:
                    pic_path = item_utils.get_gun_pic_by_item_id(itype, is_shadow=False)
                weapon_ui.parts.SetDisplayFrameByPath('', pic_path)
                vis_change_attr_list.append('parts')
            self._is_in_renew_ani[weapon_pos] = True
            self.PlayAnimationInWeaponItem(weapon_ui, 'renew', lambda : self.check_next_renew_ani(weapon_pos), vis_change_attr_list)

        return

    def play_renew_animation_by_sequence(self, weapon_pos, itype=None):
        if self._is_in_renew_ani[weapon_pos]:
            self._renew_ani_sequence[weapon_pos].append(itype)
        else:
            self.play_renew_animation(weapon_pos, itype)

    def check_next_renew_ani(self, weapon_pos):
        self._is_in_renew_ani[weapon_pos] = False
        if len(self._renew_ani_sequence[weapon_pos]) > 0:
            self.play_renew_animation(weapon_pos, self._renew_ani_sequence[weapon_pos].pop(0))

    def on_weapon_in_hand_changed(self, *args):
        self.update_weapon_ui()

    def check_renew_weapon(self, is_init=False):
        for weapon_pos in self.ALL_MAIN_WEAPON:
            if global_data.cam_lplayer:
                wp = global_data.cam_lplayer.share_data.ref_wp_bar_mp_weapons.get(weapon_pos) if 1 else None
                self.weapon_pos_to_eid[weapon_pos] = wp or None
            else:
                eid = wp.get_data()['entity_id']
                if self.weapon_pos_to_eid.get(weapon_pos, None) != eid:
                    if not is_init:
                        self.play_renew_animation_by_sequence(weapon_pos, wp.get_id())
                    self.weapon_pos_to_eid[weapon_pos] = eid

        return

    def on_item_data_changed(self, item_data):
        from logic.gutils import item_utils
        if item_data:
            item_id = item_data['item_id']
            if item_utils.is_bullet(item_id):
                self.update_weapon_ui()
            elif iutil.is_special_effect_item(item_id):
                self.on_special_effect_items_changed(item_id, item_data)

    def on_special_effect_items_changed(self, item_id, item_data):
        other_items = global_data.cam_lplayer.ev_g_others()
        if not other_items:
            self.sp_items_key_dict = {}
        else:
            cnt_item = other_items.get(item_data['entity_id'], None)
            if cnt_item:
                self.sp_items_key_dict[item_id] = item_data['entity_id']
            elif item_id in self.sp_items_key_dict:
                del self.sp_items_key_dict[item_id]
        self.update_sp_items_info()
        return

    def on_change_weapon_attachment(self, weapon_pos, attachment_pos):
        wp_obj = global_data.cam_lplayer.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        if wp_obj:
            attach_attr = wp_obj.get_attachment_attr(attachment_pos)
            if attach_attr:
                itype = attach_attr.get('iType')
                self.play_renew_animation_by_sequence(weapon_pos, itype)

    def on_weapon_data_changed(self, weapon_pos):
        self.update_weapon_ui()

    def on_pick_up_weapon(self, *args):
        self.is_in_pick_ani = True
        self.check_renew_weapon()

        def _clear_flag():
            self.is_in_pick_ani = False
            self.update_weapon_ui()

        self.panel.SetTimeOut(1.0, _clear_flag)

    def on_weapon_deleted(self, weapon_pos):
        self.check_renew_weapon()
        self.update_weapon_ui()

    def on_weapon_data_switched(self, *args):
        self.update_weapon_ui()
        self.check_renew_weapon()

    def PlayAnimationInWeaponItem(self, weapon_item, anim_name, callback=None, vis_change_attr_list=[]):
        if not weapon_item.HasAnimation(anim_name):
            return
        self.StopAnimationInWeaponItem(weapon_item, anim_name)
        anim_duration = weapon_item.GetAnimationMaxRunTime(anim_name)
        self.set_ani_widget_vis(weapon_item, vis_change_attr_list, True)

        def _OnAnimationEnd(*args):
            self.set_ani_widget_vis(weapon_item, vis_change_attr_list, False)
            self.StopAnimationInWeaponItem(weapon_item, anim_name)
            if callback and callable(callback):
                callback()

        ani_play_times = weapon_item.GetAnimationPlayTimes(anim_name)
        if ani_play_times < 1000:
            weapon_item.SetTimeOut(anim_duration * ani_play_times, _OnAnimationEnd)
        weapon_item.PlayAnimation(anim_name)

    def set_ani_widget_vis(self, weapon_item, vis_change_attr_list, is_vis):
        for attr_name in vis_change_attr_list:
            attr_widget = getattr(weapon_item, attr_name, None)
            if attr_widget:
                attr_widget.setVisible(is_vis)

        return

    def StopAnimationInWeaponItem(self, weapon_item, anim_name, vis_change_attr_list=[]):
        self.set_ani_widget_vis(weapon_item, vis_change_attr_list, False)
        if weapon_item.anim_timer is not None:
            weapon_item.stopAction(weapon_item.anim_timer)
            weapon_item.anim_timer = None
        weapon_item.StopAnimation(anim_name)
        return

    def on_join_mecha(self):
        self.add_hide_count(self.__class__.__name__)

    def on_leave_mecha(self):
        if self.get_show_count(self.__class__.__name__) < 0:
            self.add_show_count(self.__class__.__name__)

    def on_change_ui_custom_data(self):
        self.update_all_main_weapon_widgets(True)

    def change_ui_data(self):
        scale_type_adjust_list = []
        pos_type_adjust_list = []
        need_to_adjust_scale_type_nodes = (
         ('nd_weapon_1', 'nd_weapon_1', None), ('nd_weapon_2', 'nd_weapon_2', None), ('nd_weapon_3', 'nd_weapon_3', None))
        for source_nd_name, target_nd_name, target_scale_nd_name in need_to_adjust_scale_type_nodes:
            nd = getattr(self.panel, source_nd_name)
            w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
            scale = nd.getScale()
            scale_type_adjust_list.append((w_pos, scale, target_nd_name, target_scale_nd_name))

        ret_dict = {'scale_type': scale_type_adjust_list,
           'pos_type': pos_type_adjust_list
           }
        return ret_dict

    def on_weapon_bullet_num_changed(self, pos_or_pos_list):
        weapon_pos_list = [pos_or_pos_list] if isinstance(pos_or_pos_list, int) else pos_or_pos_list
        main_weapon_data = self.get_weapon_data(True)
        for weapon_pos in weapon_pos_list:
            weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
            weapon_object = main_weapon_data.get(weapon_pos, None)
            for idx, weapon_ui in enumerate(weapon_ui_tuple):
                if weapon_object:
                    self.update_bullet_info(weapon_ui, weapon_object)

        return

    def keyboard_try_switch_weapon(self, weapon_pos, msg, keycode):
        player = global_data.cam_lplayer
        if not player:
            return
        else:
            if player.id != global_data.player.id:
                return
            weapon_info = player.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
            weapon_data = None if weapon_info is None else weapon_info.get_data()
            if player.share_data.ref_wp_bar_cur_pos != weapon_pos:
                if weapon_data:
                    switch_pos = weapon_pos
                    player.send_event('E_TRY_SWITCH', switch_pos)
                    global_data.emgr.restart_avatar_fire_by_ui.emit()
                return
            return

    def check_can_mouse_scroll(self):
        if not (global_data.player and global_data.player.logic):
            return False
        return True

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        player = global_data.player.logic
        cur_weapon = player.share_data.ref_wp_bar_cur_pos
        dist = -delta
        _weapon_data_dict = player.share_data.ref_wp_bar_mp_weapons
        if not _weapon_data_dict:
            return
        else:
            valid_weapon_list = [ i for i in self.ALL_MAIN_WEAPON if i in _weapon_data_dict ]
            if cur_weapon not in valid_weapon_list:
                return
            cur_weapon_index = valid_weapon_list.index(cur_weapon)
            self._cur_mouse_dist += dist
            if abs(self._cur_mouse_dist) > self.ui_scroll_sensitivity:
                changed_index = int(self._cur_mouse_dist / self.ui_scroll_sensitivity)
                changed_index = min(max(-1, changed_index), 1)
                self._cur_mouse_dist = 0
                cur_weapon_index = (cur_weapon_index + changed_index) % len(valid_weapon_list)
                new_weapon_pos = valid_weapon_list[cur_weapon_index]
                self.keyboard_try_switch_weapon(new_weapon_pos, None, None)
            return

    def _on_improvise_highlight(self, left_ready_time):
        main_weapon_data = self.get_weapon_data(True) or {}
        for pos in self._improvise_highlight_pos_list:
            normal, sel = self.get_weapon_ui_by_pos(pos)
            weapon_pos_data = main_weapon_data.get(pos, None)
            play_new = bool(weapon_pos_data)
            if normal:
                self.stop_improvise_highlight_efx_single(normal)
                play_new and self.play_improvise_highlight_efx_single(normal)
            if sel:
                self.stop_improvise_highlight_efx_single(sel)
                play_new and self.play_improvise_highlight_efx_single(sel)

        return

    def play_improvise_highlight_efx_single(self, weapon_item):
        if not weapon_item.HasAnimation('renovate'):
            return
        weapon_item.PlayAnimation('renovate')

    def stop_improvise_highlight_efx_single(self, weapon_item):
        if not weapon_item.HasAnimation('renovate'):
            return
        weapon_item.StopAnimation('renovate')
        weapon_item.RecoverAnimationNodeState('renovate')


class WeaponBarSelectUI(WeaponBarSelectBaseUI):
    PANEL_CONFIG_NAME = 'battle/change_weapon'