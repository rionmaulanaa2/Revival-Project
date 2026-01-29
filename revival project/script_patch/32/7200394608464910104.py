# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/ObserveInfoUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
import math
from logic.gutils import item_utils
from logic.gcommon import const
from logic.gutils.weapon_utils import get_weapon_conf
from logic.gutils.template_utils import get_item_quality
from logic.gcommon.common_const import weapon_const
from common.const import uiconst
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.dress_utils import get_weapon_default_fashion

class ObserveInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/change_weapon'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    ALL_MAIN_WEAPON = const.MAIN_WEAPON_LIST

    def on_init_panel(self, *args, **kwargs):
        self.panel.setVisible(False)
        self.init_widget()
        self.init_event()
        self.init_observe()

    def on_finalize_panel(self):
        self.destroy_widget('buff_com')

    def init_observe(self):
        spectate_target = None
        if global_data.player and global_data.player.logic:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self.on_enter_observe(spectate_target.logic)
        return

    def init_event(self):
        global_data.emgr.scene_observed_player_setted_event += self.on_enter_observe
        global_data.emgr.on_weapon_data_switched_event += self.switch_weapon_data
        global_data.emgr.on_wpbar_switch_cur_event += self.on_switch_cur_weapon
        global_data.emgr.on_observer_join_mecha += self.on_join_mecha
        global_data.emgr.on_observer_leave_mecha += self.on_leave_mecha

    def init_widget(self):
        self.cnt_select_sp_item = None
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
        for k, v in six.iteritems(self.weapon_widget_dict):
            for ccb_btn in v:
                ccb_btn.btn_weapon.disabled = False
                ccb_btn.btn_weapon.EnableCustomState(True)
                ccb_btn.btn_weapon.SetNoEventAfterMove(True, '10w')
                ccb_btn.anim_timer = None

            self._renew_ani_sequence[k] = []

        return

    def on_enter_observe(self, ltarget):
        if not ltarget:
            return
        if ltarget.ev_g_in_mecha():
            self.panel.setVisible(False)
        else:
            self.panel.setVisible(True)
        self.init_weapon_data(ltarget)
        self.update_weapon_ui()

    def init_weapon_data(self, ltarget):
        import copy
        if ltarget is None:
            self.weapon_data_dict = {}
            return
        else:
            _weapon_data_dict = ltarget.share_data.ref_wp_bar_mp_weapons
            weapon_data_dict = {}
            for pos, wp_obj in six.iteritems(_weapon_data_dict):
                if wp_obj is not None:
                    weapon_data_dict[pos] = copy.deepcopy(wp_obj.get_data())

            for weapon_pos, weapon_pos_data in six.iteritems(weapon_data_dict):
                if weapon_pos in const.MAIN_WEAPON_LIST:
                    wp = ltarget.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
                    if wp:
                        max_bullet = wp.get_bullet_cap()
                        weapon_pos_data['max_bullet_cap'] = max_bullet

            self.weapon_data_dict = weapon_data_dict
            self.cur_weapon_pos = ltarget.ev_g_wpbar_cur_gun_pos()
            return

    def update_weapon_ui(self):
        self.update_weapon_item_visible()
        self.update_all_main_weapon_widgets()

    def update_weapon_item_visible(self):
        if not global_data.cam_lplayer:
            return
        cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        for pos, ccb_btn_tuple in six.iteritems(self.weapon_widget_dict):
            ccb_btn, ccb_btn_sel = ccb_btn_tuple
            pos_equal = pos == cur_weapon_pos
            ccb_btn.setVisible(not pos_equal)
            ccb_btn_sel.setVisible(pos_equal)

        self.update_sp_item_widget_vis()

    def update_sp_item_widget_vis(self):
        tools_vis = self.nd_more_tools.isVisible()
        sel_vis = False
        normal_vis = False
        if not tools_vis and global_data.cam_lplayer:
            cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
            sel_vis = bool(cur_weapon_pos == const.PART_WEAPON_POS_MAIN_DF and self.cnt_select_sp_item is None)
            normal_vis = not sel_vis
        self.ccb_weapon_4.setVisible(normal_vis)
        self.ccb_weapon_4_sel.setVisible(sel_vis)
        return

    def update_all_main_weapon_widgets(self):
        main_weapon_pos_list = self.ALL_MAIN_WEAPON
        main_weapon_data = self.weapon_data_dict
        weapon_pos_main3_data = None
        for weapon_pos in main_weapon_pos_list:
            weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
            weapon_data = main_weapon_data.get(weapon_pos, None)
            if hasattr(weapon_ui_tuple[0], 'img_weapon_num') and weapon_ui_tuple[0].img_weapon_num:
                weapon_ui_tuple[0].img_weapon_num.setVisible(not bool(weapon_data))
            for idx, weapon_ui in enumerate(weapon_ui_tuple):
                self.update_main_weapon_info(weapon_ui, weapon_pos, weapon_data, idx=idx)

        weapon_pos_main3_data = main_weapon_data.get(const.PART_WEAPON_POS_MAIN3, None)
        self.panel.nd_weapon_3.setVisible(bool(weapon_pos_main3_data))
        ani_name = 'switch_to_small' if bool(weapon_pos_main3_data) else 'switch_to_big'
        if ani_name != self.switch_scale_ani:
            self.switch_scale_ani and self.panel.StopAnimation(self.switch_scale_ani)
            self.panel.PlayAnimation(ani_name)
            weapon_ui_tuple = self.get_weapon_ui_by_pos(const.PART_WEAPON_POS_MAIN_DF)
            for ui in weapon_ui_tuple:
                ui and self.switch_scale_ani and ui.StopAnimation(self.switch_scale_ani)
                ui and ui.PlayAnimation(ani_name)

            self.switch_scale_ani = ani_name
        return

    def get_weapon_ui_by_pos(self, pos):
        return self.weapon_widget_dict.get(pos, (None, None))

    def update_main_weapon_info(self, weapon_ui_item, weapon_pos, weapon_data, play_ani=False, idx=0):
        self.update_widgets_visible(weapon_ui_item, bool(weapon_data))
        if not weapon_data:
            weapon_ui_item.img_weapon_level.setVisible(False)
            return
        else:
            item_no = weapon_data['item_id']
            item_fashion_no = weapon_data.get('fashion', {}).get(FASHION_POS_SUIT, None) or get_weapon_default_fashion(item_no)
            item_conf = get_weapon_conf(str(item_no))
            self.update_gun_widget(weapon_ui_item, item_no, idx=idx, item_fashion_no=item_fashion_no)
            self.update_bullet_info(weapon_ui_item, weapon_pos, weapon_data, item_conf)
            return

    def update_widgets_visible(self, weapon_ui_item, is_vis):
        weapon_ui_item.sp_weapon.setVisible(is_vis)
        weapon_ui_item.tf_cur_bullet.setVisible(is_vis)
        if weapon_ui_item.icon_reload:
            weapon_ui_item.icon_reload.setVisible(is_vis)
            weapon_ui_item.icon_reload_2.setVisible(is_vis)

    def update_gun_widget(self, weapon_ui_item, item_no, idx=0, item_fashion_no=None):
        if item_fashion_no:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_fashion_no)
        else:
            pic_path = item_utils.get_gun_pic_by_item_id(item_no, is_shadow=False)
        level = get_item_quality(item_no)
        tail = 'btn_change_l_choose' if idx == 1 else 'btn_change_l_nml'
        path = 'gui/ui_res_2/battle/button/' + tail + '_%s.png' % str(level)
        weapon_ui_item.img_weapon_level.SetDisplayFrameByPath('', path)
        weapon_ui_item.img_weapon_level.setVisible(True)
        weapon_ui_item.sp_weapon.SetDisplayFrameByPath('', pic_path)
        from logic.gutils.weapon_skin_utils import set_weapon_skin_pic_pos_and_scale
        set_weapon_skin_pic_pos_and_scale(weapon_ui_item.sp_weapon, item_fashion_no, item_no)
        from logic.gutils.weapon_skin_utils import set_weapon_skin_pic_pos_and_scale
        set_weapon_skin_pic_pos_and_scale(weapon_ui_item.sp_weapon, item_fashion_no, item_no)

    def update_bullet_info(self, weapon_ui_item, weapon_pos, weapon_data, item_conf):
        if not global_data.cam_lplayer:
            return
        else:
            cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
            max_bullet = weapon_data['max_bullet_cap']
            cur_bullet_num = weapon_data.get('iBulletNum', 0)
            item_id = weapon_data['item_id']
            if item_conf is None:
                log_error('No this item_no item_data:', weapon_data)
                return
            bullet_type = item_conf['iBulletType']
            bullet_color = '#SW'
            if 1 <= cur_bullet_num < math.ceil(max_bullet * 0.4):
                bullet_color = '#SR'
            elif cur_bullet_num < 1:
                bullet_color = '#SR'
            if bullet_type == weapon_const.ITEM_ID_INFINITE_BULLET:
                show_bullet_num = max_bullet
            elif bullet_type == weapon_const.ITEM_ID_LIMITED_BULLET:
                show_bullet_num = weapon_data.get('iCarryBulletNum', 0)
            else:
                show_bullet_num = self.get_bag_bullet_num(bullet_type) * item_conf.get('iReloadRatio', 1)
            text_format_str = '<size={part_1_font_size}>{part_1_text}</size><size={part_2_font_size}>{part_2_text}</size>'
            text_args = {'part_1_font_size': 22,
               'part_1_text': ''.join([bullet_color, str(cur_bullet_num)]),
               'part_2_font_size': 18,
               'part_2_text': ''.join(['#SW', '/', str(show_bullet_num)])
               }
            context_txt = text_format_str.format(**text_args)
            weapon_ui_item.tf_cur_bullet.SetString(context_txt)
            return

    def update_main_weapon_data(self, ui_item, weapon_pos, weapon_data, cur_weapon_pos):
        from logic.gutils import item_utils
        from logic.gcommon.item import item_utility as iutil
        from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
        from logic.gcommon.item import item_utility as iutils
        ui_item.sp_weapon.setVisible(False)
        ui_item.weapon_pos = weapon_pos
        if hasattr(ui_item, 'img_gun_empty') and ui_item.img_gun_empty:
            ui_item.img_gun_empty.setVisible(True)
        ui_item.img_nd_bg.setVisible(True)
        ui_item.img_select.setVisible(False)
        if not weapon_data:
            return
        else:
            item_id = weapon_data['item_id']
            item_fashion_no = weapon_data.get('fashion', {}).get(FASHION_POS_SUIT, None) or get_weapon_default_fashion(item_id)
            if not item_utils.is_gun(item_id):
                return
            ui_item.nd_weapon.setVisible(True)
            if hasattr(ui_item, 'img_gun_empty') and ui_item.img_gun_empty:
                ui_item.img_gun_empty.setVisible(False)
            weapon_ui_item = ui_item.nd_weapon
            if weapon_pos == cur_weapon_pos:
                ui_item.img_select.setVisible(True)
                ui_item.img_nd_bg.setVisible(False)
            if hasattr(weapon_ui_item, 'tf_cur_bullet') and weapon_ui_item.tf_cur_bullet:
                max_bullet = weapon_data['max_bullet_cap']
                cur_bullet_num = weapon_data.get('iBulletNum', 0)
                from logic.gutils.weapon_utils import get_weapon_conf
                item_conf = get_weapon_conf(str(item_id))
                if item_conf is None:
                    log_error('No this item_no item_data:', weapon_data)
                    return
                bullet_type = item_conf['iBulletType']
                bag_bullet_num = self.get_item_count(bullet_type) * item_conf.get('iReloadRatio', 1)
                if bullet_type == weapon_const.ITEM_ID_LIMITED_BULLET:
                    bag_bullet_num = item_conf.get('iCarryBulletNum', 0)
                self.update_gun_bullet_num(weapon_ui_item, cur_bullet_num, max_bullet, bag_bullet_num, bullet_type)
            if item_utils.is_gun(item_id):
                if item_fashion_no:
                    pic_path = get_lobby_item_pic_by_item_no(item_fashion_no)
                else:
                    pic_path = item_utils.get_gun_pic_by_item_id(item_id, is_shadow=False)
            else:
                pic_path = self.get_weapon_pic_path(item_id)
            weapon_ui_item.sp_weapon.SetDisplayFrameByPath('', pic_path)
            return

    def update_gun_bullet_num(self, weapon_ui_item, cur_bullet_num, max_bullet, bag_bullet_num, bullet_type):
        import math
        if 1 <= cur_bullet_num < math.ceil(max_bullet * 0.4):
            bullet_color = '#SR'
        elif cur_bullet_num < 1:
            bullet_color = '#SR'
        else:
            bullet_color = '#SW'
        weapon_ui_item.tf_cur_bullet.SetString(str(cur_bullet_num))
        weapon_ui_item.tf_cur_bullet.SetColor(bullet_color)
        if hasattr(weapon_ui_item, 'tf_total_bullet') and weapon_ui_item.tf_total_bullet:
            lcpos_x, _ = weapon_ui_item.tf_cur_bullet.GetPosition()
            sz = weapon_ui_item.tf_cur_bullet.getContentSize()
            end_lcpos_x = lcpos_x + (1.0 - weapon_ui_item.tf_cur_bullet.getAnchorPoint().x) * sz.width
            weapon_ui_item.tf_total_bullet.SetPosition(end_lcpos_x, weapon_ui_item.tf_total_bullet.getPosition().y)
            if bullet_type == weapon_const.ITEM_ID_INFINITE_BULLET:
                weapon_ui_item.tf_total_bullet.SetString('/' + str(max_bullet))
            else:
                weapon_ui_item.tf_total_bullet.SetString('/' + str(bag_bullet_num))

    def switch_weapon_data(self, pos1, pos2):
        tmp = self.weapon_data_dict.get(pos1, None)
        self.weapon_data_dict[pos1] = self.weapon_data_dict.get(pos2, None)
        self.weapon_data_dict[pos2] = tmp
        if global_data.cam_lplayer:
            self.cur_weapon_pos = global_data.cam_lplayer.ev_g_wpbar_cur_gun_pos()
            self.update_weapon_ui()
        return

    def on_switch_cur_weapon(self, cur_pos):
        if cur_pos in const.MAIN_WEAPON_LIST or cur_pos == const.PART_WEAPON_POS_NONE:
            self.cur_weapon_pos = cur_pos
            self.update_weapon_ui()

    def on_weapon_data_changed(self, weapon_data):
        self.weapon_data_dict = weapon_data
        self.update_weapon_ui()

    def get_item_count(self, item_id):
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_item_count(item_id)
        else:
            return 0

    def get_newest_weapon_data(self, ltarget, weapon_pos):
        if not ltarget:
            return
        else:
            wp = ltarget.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
            if wp:
                import copy
                weapon_pos_data = copy.deepcopy(wp.get_data())
                if weapon_pos in const.MAIN_WEAPON_LIST:
                    max_bullet = wp.get_bullet_cap()
                    weapon_pos_data['max_bullet_cap'] = max_bullet
                return weapon_pos_data
            return

    def init_buff_com(self):
        from logic.comsys.battle.ArmorBuffWidget import ArmorBuffWidget
        self.buff_com = ArmorBuffWidget(self.panel.list_defend)

    def on_join_mecha(self):
        self.panel.setVisible(False)

    def on_leave_mecha(self):
        self.panel.setVisible(True)