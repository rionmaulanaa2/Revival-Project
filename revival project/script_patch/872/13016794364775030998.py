# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/RoleChooseUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import C_file
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.gutils import template_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.role_profile import RoleInfoUI
from logic.gutils import bond_utils, role_utils, battle_pass_utils
from common.cfg import confmgr
from logic.gutils import red_point_utils, mall_utils
from common.const import uiconst
from logic.gutils.role_utils import get_role_check_show_handler, is_crossover_role, get_crossover_info
from logic.gutils.dress_utils import get_role_dress_clothing_id
from logic.gutils.video_utils import check_play_chuchang_video, get_relative_video_skin_list, get_chuchang_video_path
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils import role_skin_utils, item_utils
from logic.gcommon.common_const.role_const import ROLE_SKIN_RARE_BACKGROUND, ROLE_SKIN_RARE_BACKGROUND_DEFAULT
from logic.gutils.item_utils import check_skin_tag
EXCEPT_HIDE_UI_LIST = []

class RoleChooseUI(BasePanel):
    PANEL_CONFIG_NAME = 'role_profile/role_choose'
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    OPEN_SOUND_NAME = 'ui_mecha_zoom_in'
    BACK_BTN_SOUND_NAME = 'ui_click_mecha_back'
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self.init_parameters()
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        self.panel.PlayAnimation('appear')
        self.bind_event(True)
        self.refresh_role_list()
        self.panel.temp_btn_back.btn_back.set_click_sound_name(self.BACK_BTN_SOUND_NAME)
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)
        self._is_animing = False

    def init_parameters(self):
        self.role_info_config = confmgr.get('role_info', 'RoleInfo', 'Content')
        self.role_config = confmgr.get('role_info', 'RoleProfile', 'Content')
        self.role_2_item = {}
        self.bond_guide_nd = None
        self.video_role_id = None
        self.video_item = None
        return

    def bind_event(self, bind):
        e_conf = {'net_reconnect_event': self._on_login_reconnect,
           'buy_good_success_with_list': self._on_buy_good_success_goods_list,
           'refresh_item_red_point': self.refresh_item_red_point,
           'bond_role_reward': self.refresh_item_red_point,
           'bond_update_role_level': self.refresh_item_red_point,
           'on_check_bond_exchange_driver_gift': self.refresh_item_red_point,
           'role_fashion_chagne': self._on_role_fashion_chagne
           }
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _init_role_item(self, item, role_id):
        item.lab_name.SetString(self.role_config[str(role_id)]['role_name'])
        item_data = global_data.player.get_item_by_no(role_id)
        item.img_not_owned.setVisible(False)
        item.nd_lock.setVisible(False)
        item.lab_secondary.setVisible(False)
        crossover_info = get_crossover_info(str(role_id))
        if crossover_info and crossover_info.get('text'):
            item.lab_secondary.SetString(get_text_by_id(crossover_info.get('text')))
            item.lab_secondary.setVisible(True)
        else:
            item.lab_secondary.setVisible(False)
        item.temp_level.setVisible(False)
        if item_data:
            skin_id = get_role_dress_clothing_id(role_id, check_default=True)
            pic = mall_utils.get_half_pic_by_item_no(skin_id)
            item.img_role.SetDisplayFrameByPath('', pic)
            if not role_skin_utils.is_default_role_skin(skin_id, role_id):
                item.nd_cut.setVisible(True)
                rare_degree = item_utils.get_item_rare_degree(skin_id)
                background_img = ROLE_SKIN_RARE_BACKGROUND.get(rare_degree, ROLE_SKIN_RARE_BACKGROUND_DEFAULT)
                if background_img:
                    item.bar_level.SetDisplayFrameByPath('', background_img)
                item.temp_level.setVisible(True)
                check_skin_tag(item.temp_level, skin_id)
            else:
                item.bar_level.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/role_%d.png' % role_id)
                item.nd_cut.setVisible(False)
        else:
            item.bar_level.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/role_%d_lock.png' % role_id)
            item.nd_cut.setVisible(False)
            if role_utils.is_role_publish(role_id):
                role_goods_id = self.role_info_config.get(str(role_id), {}).get('goods_id') if 1 else None
                item.img_not_owned.setVisible(bool(role_goods_id))
                available_time = role_goods_id or self.role_config[str(role_id)].get('available_date')
                if available_time:
                    from logic.gcommon import time_utility as tutil
                    now = tutil.get_server_time()
                    if available_time - now > tutil.ONE_DAY_SECONDS:
                        delta = tutil.get_rela_day_no(now, base_time=available_time)
                        text_content = str(delta) + get_text_by_id(81156)
                    else:
                        text_content = 81157
                else:
                    text_content = 14008
                item.lab_secondary.setVisible(True)
                item.lab_secondary.SetString(text_content)
        is_battlepass_free = battle_pass_utils.get_is_battlepass_free_trial(role_id)
        item.nd_bp_free.setVisible(is_battlepass_free)
        return

    def refresh_role_list(self):
        self.panel.preview_role.setVisible(False)
        role_id_list = global_data.player.get_role_open_seq()
        role_id_list_owned = []
        role_id_list_not_owned = []
        for role_id in role_id_list:
            role_id = int(role_id)
            if not self.check_show_role_panel(role_id):
                continue
            role_data = global_data.player.get_item_by_no(role_id)
            has_role = role_data is not None
            if has_role:
                role_id_list_owned if 1 else role_id_list_not_owned.append(role_id)

        def cmp_not_open(role_id):
            role_goods_id = self.role_info_config.get(str(role_id), {}).get('goods_id') if role_utils.is_role_publish(role_id) else None
            return bool(role_goods_id)

        role_id_list_not_owned.sort(key=cmp_not_open, reverse=True)
        role_id_list = role_id_list_owned + role_id_list_not_owned
        owned_list_len = len(role_id_list_owned)
        roll_container = self.panel.list_role
        roll_container.RecycleAllItem()
        self.role_2_item = {}
        need_show_bond_guide = bond_utils.need_bond_guided()
        for index, role_id in enumerate(role_id_list):
            self.role_2_item[role_id] = index
            item = roll_container.AddTemplateItem()
            item.setLocalZOrder(len(role_id_list) - index)
            self._init_role_item(item, role_id)

            @global_unique_click(item.btn_role_choose)
            def OnClick(btn, touch, role_id=role_id, item=item):
                if self.video_role_id is not None:
                    return
                else:
                    if self.check_play_role_vidoe(role_id, item):
                        return
                    if RoleInfoUI.USE_NEW_BG:
                        self.show_trans_anim(item, role_id, lambda : self.on_select_role_id(role_id))
                    else:
                        self.on_select_role_id(role_id)
                    show_new = global_data.lobby_red_point_data.get_rp_by_no(role_id)
                    if self.bond_guide_nd:
                        self.bond_guide_nd.setVisible(False)
                    if show_new:
                        global_data.player.req_del_item_redpoint(role_id)
                    return

            has_role = index < owned_list_len
            if need_show_bond_guide and has_role:
                need_show_bond_guide = False
                self.show_bond_guide(item)
                item.setLocalZOrder(len(role_id_list) + 1)

        container_height = roll_container.GetInnerContentSize().height
        _, scroll_list_size = roll_container.GetContentSize()
        if container_height <= scroll_list_size + 1:
            roll_container.UnBindMethod('OnScrolling')
        else:
            max_offset = scroll_list_size - container_height

            @roll_container.callback()
            def OnScrolling(widget):
                cur_offset = widget.GetContentOffset().y
                cur_offset = min(max(max_offset, cur_offset), 0)
                x, y = self.panel.img_progress.GetPosition()
                y = 50 / max_offset * cur_offset + 50
                self.panel.img_progress.SetPosition(x, '%f%%' % y)

        return

    def _on_buy_good_success(self, item_id):
        role_id_list = global_data.player.get_role_open_seq()
        if str(item_id) not in role_id_list:
            return
        self.refresh_role_list()

    def _on_buy_good_success_goods_list(self, goods_list):
        role_id_list = global_data.player.get_role_open_seq()
        for goods_info in goods_list:
            if str(goods_info[0]) in role_id_list:
                self.refresh_role_list()
                break

    def on_finalize_panel(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)
        self.role_2_item = None
        self.bind_event(False)
        self.show_main_ui()
        return

    def do_hide_panel(self):
        super(RoleChooseUI, self).do_hide_panel()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)

    def do_show_panel(self):
        super(RoleChooseUI, self).do_show_panel()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def _on_login_reconnect(self):
        if self.panel and self.panel.isValid() and self.panel.isVisible():

            def gao_si_effect():
                if self.panel and self.panel.isValid() and self.panel.isVisible():
                    global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

            global_data.game_mgr.delay_exec(1, gao_si_effect)

    def on_click_close_btn(self, *args):
        self.close()

    def show_bond_guide(self, item):
        wpos = item.ConvertToWorldSpacePercentage(50, 50)
        if self.bond_guide_nd:
            self.bond_guide_nd.Destroy()
            self.bond_guide_nd = None
        self.bond_guide_nd = template_utils.init_guide_temp(item, wpos, text_id=870043)
        return

    def show_trans_anim(self, item, role_id, callback):
        from common.uisys import color_table
        skin_id = get_role_dress_clothing_id(role_id, check_default=True)
        scene_path = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), 'zhanshi_scene_path')
        if scene_path:
            callback()
            return
        _pos = item.getPosition()
        pos = self.panel.list_role.ConvertToWorldSpace(_pos.x, _pos.y)
        self.panel.preview_role.setPosition(pos)
        self.set_role_item_status(self.panel.preview_role, role_id)
        self.panel.preview_role.lab_name.SetString(self.role_config[str(role_id)]['role_name'])
        self.panel.preview_role.setVisible(True)
        item = self.panel.preview_role
        ani_conf = confmgr.get('role_info', 'Role_UI', 'Content', str(role_id))
        clr = color_table.get_color_rgb_hex(ani_conf['vxbg_1'])
        item.bg_role_white_1.SetColor(clr)
        item.bg_role_white_2.SetColor(clr)
        aniName = 'choose'
        item.PlayAnimation(aniName)
        max_time = item.GetAnimationMaxRunTime(aniName)

        def cb():
            callback()
            self.panel.preview_role.setVisible(False)

        item.SetTimeOut(max_time * 0.8, cb)

    def on_select_role_id(self, role_id):
        ui = global_data.ui_mgr.show_ui('RoleInfoUI', 'logic.comsys.role_profile')
        if self.video_role_id is not None:
            cur_skin_id = get_role_dress_clothing_id(self.video_role_id)
            for skin_id in get_relative_video_skin_list(cur_skin_id):
                ui.chuchang_video_dict[skin_id] = True

        ui.set_role_id(role_id)
        return

    def refresh_role_item_rp(self, item, role_id):
        rp_level = red_point_utils.get_RoleChooseUI_rp_level(role_id)
        red_point_utils.show_red_point_template(item.nd_new, rp_level, rp_level)

    def refresh_item_red_point(self, *args):
        for role_id, info in six.iteritems(self.role_config):
            if not self.check_show_role_panel(role_id):
                continue
            role_id = int(role_id)
            index = self.role_2_item.get(role_id)
            if index is not None:
                item = self.panel.list_role.GetItem(index)
                self.refresh_role_item_rp(item, role_id)

        return

    def guide_get_role_to_ui_item(self, role_id):
        print('guide_get_role_to_ui_item', type(role_id), type(six_ex.keys(self.role_2_item)[0]))
        index = self.role_2_item.get(role_id)
        if index is not None:
            return self.panel.list_role.GetItem(index)
        else:
            return
            return

    def check_show_role_panel(self, role_id):
        check_show_handler_name = self.role_config.get(str(role_id), {}).get('check_show_handler')
        if not check_show_handler_name:
            return True
        check_show_handler_func = get_role_check_show_handler(check_show_handler_name)
        if check_show_handler_func and not check_show_handler_func():
            return False
        return True

    def check_play_role_vidoe(self, role_id, item):
        skin_id = get_role_dress_clothing_id(role_id, check_default=True)
        if check_play_chuchang_video(skin_id):
            if not global_data.video_player.is_in_init_state():
                if not global_data.video_player.player:
                    global_data.video_player.reset_data()
                else:
                    return True
            self.video_role_id = role_id
            self.video_item = item
            video_path = get_chuchang_video_path(skin_id)
            if video_path:
                video_path = 'video/%s.mp4' % video_path
                if not C_file.find_res_file(video_path, ''):
                    self.on_end_load_role_video()
                else:
                    global_data.video_player.play_video(video_path, self.on_end_play_role_video, repeat_time=1, video_ready_cb=self.on_end_load_role_video)
            return True
        return False

    def on_end_load_role_video(self):
        role_id = self.video_role_id
        item = self.video_item
        if RoleInfoUI.USE_NEW_BG:
            self.show_trans_anim(item, role_id, lambda : self.on_select_role_id(role_id))
        else:
            self.on_select_role_id(role_id)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(role_id)
        if self.bond_guide_nd:
            self.bond_guide_nd.setVisible(False)
        if show_new:
            global_data.player.req_del_item_redpoint(role_id)
        self.video_role_id = None
        self.video_item = None
        return

    def on_end_play_role_video(self):
        ui = global_data.ui_mgr.get_ui('RoleInfoUI')
        if ui:
            ui.on_finish_play_video()

    def _on_role_fashion_chagne(self, item_no, fashion_data):
        self.refresh_role_list()