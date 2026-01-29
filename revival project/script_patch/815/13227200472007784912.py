# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/homeland/WinningStreakUI.py
from __future__ import absolute_import
from six.moves import range
import time
from common.const.property_const import *
from common.uisys.basepanel import BasePanel
from logic.gutils import lobby_model_display_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.comsys.message.message_data import get_channel_name_by_chid
from logic.gcommon import const
from logic.gcommon.item import item_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.chat_const import WINNING_STREAK_CHANNEL, CHAT_CLAN, CHAT_WORLD
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
from logic.gutils.role_head_utils import init_role_head
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gcommon.time_utility import get_date_str
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from collections import defaultdict
IMG_PATH = 'ui_res_2/common/panel/pnl_mode_list_ash.png'

class WinningStreakUI(BasePanel):
    PANEL_CONFIG_NAME = 'share/i_share_data'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    DELAY_TAG = 202208221
    DELAY_TAG_MODEL = 202208222
    LAST_SHARE_TIME = defaultdict(int)
    STATUS_TOTAL_INFO = 1
    STATUS_AVG_INFO = 2
    GLOBAL_EVENT = {'message_on_player_detail_inf': 'on_refresh_player_detail_inf'
       }
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_close_btn',
       'nd_share.temp_btn_share.btn_common_big.OnClick': 'on_click_share_ui',
       'nd_share.list_share.nd_close.OnClick': 'close_share',
       'nd_data.btn_switch.OnClick': 'on_click_switch'
       }

    def on_init_panel(self, close_cb=None):
        self._tmp_show_share_channel = False
        self._winning_info = None
        self._raw_data = None
        self._uid = None
        self._share_content = None
        self._screen_capture_helper = ScreenFrameHelper()
        self.cur_show_model_item_no = ()
        self._loaded_model_set = set()
        self._message_data = global_data.message_data
        self._cur_uid = None
        self.panel.nd_share.btn_share.setVisible(False)
        self._change_scene()
        self.hide_main_ui()
        self.init_share_list()
        self._share_cd = 60
        self._last_share_time = -1
        self._info_status = self.STATUS_TOTAL_INFO
        return

    def init_share_list(self):
        list_share = self.panel.nd_share.list_share.option_list
        for i in range(len(WINNING_STREAK_CHANNEL)):
            tmp_ui = list_share.GetItem(i)
            tmp_channel = WINNING_STREAK_CHANNEL[i]
            tmp_ui.button.SetText(get_channel_name_by_chid(tmp_channel))
            if tmp_channel == CHAT_CLAN and global_data.player.get_clan_id() == -1:
                tmp_ui.button.SetShowEnable(False)
            self.set_click_callback(tmp_ui, tmp_channel)

    def set_click_callback(self, nd, channel):

        @nd.button.unique_callback()
        def OnClick(btn, touch):
            if channel == CHAT_CLAN and global_data.player.get_clan_id() == -1:
                global_data.game_mgr.show_tip(get_text_by_id(800098))
                return
            self.on_switch_share_channel(channel)

    def on_finalize_panel(self):
        super(WinningStreakUI, self).on_finalize_panel()
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()

    def generate_share_content(self):
        from logic.comsys.share.WinningStreakShareCreator import WinningSreakShareCreator
        share_creator = WinningSreakShareCreator()
        share_creator.create()
        share_content = share_creator
        share_content.set_winning_info(self._winning_info, self._uid)
        return share_content

    def try_share(self):
        ui_names = [
         'LobbyFullScreenBgUI']

        def cb(*args):
            pass

        if self._screen_capture_helper:
            if not self._share_content:
                self._share_content = self.generate_share_content()
            else:
                self._share_content.set_winning_info(self._winning_info, self._uid)
            self._screen_capture_helper.set_custom_share_content(self._share_content)
            btn_infos = [{'template_name': 'common/i_common_button_2','click_cb': self.on_click_friend_btn,'btn_name': 'btn_common','btn_text': 10259}, {'template_name': 'common/i_common_button_2','click_cb': self.on_click_chat_btn,'btn_name': 'btn_common','btn_text': 800150}]
            is_head = True
            self._screen_capture_helper.set_custom_share_button(btn_infos, is_head)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)

    def on_click_friend_btn(self, *args):
        share_ui = self._screen_capture_helper.get_share_ui()
        if share_ui:
            share_ui.on_click_friend_btn(self.on_click_friend)

    def on_click_friend(self, f_data):
        if not self._raw_data:
            return
        msg = self._raw_data['msg']
        notify_type = self._raw_data.get('sender_info', {}).get('notify_type', {}) or self._raw_data.get('extra', {}).get('notify_type', {})
        extra_data = {'notify_type': notify_type
           }
        share_ui = self._screen_capture_helper.get_share_ui()
        if not share_ui:
            return
        from logic.comsys.message.MainFriend import FRIEND_TAB_RELATIONSHIP
        share_ui.close()

        def ui_init_finish_cb():
            sub_panel = ui.touch_tab_by_index(0)
            sub_panel.click_uid_button(f_data[U_ID])
            global_data.message_data.recv_to_friend_msg(f_data[U_ID], f_data[C_NAME], msg, f_data[U_LV], extra=extra_data)
            global_data.player.req_friend_msg(f_data[U_ID], f_data[U_LV], f_data.get(CLAN_ID, -1), msg, extra=extra_data)

        ui = global_data.ui_mgr.get_ui('MainFriend')
        if ui:
            ui_init_finish_cb()
            return
        ui = global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
        ui.set_ui_init_finish_cb(FRIEND_TAB_RELATIONSHIP, ui_init_finish_cb)

    def _check_share_cd(self):
        now = time.time()
        delta = now - self._last_share_time
        if delta < self._share_cd:
            global_data.player.notify_client_message((get_text_by_id(10273).format(int(self._share_cd - delta)),))
            return False
        self._last_share_time = now
        return True

    def on_click_chat_btn(self, *args):
        if not self._check_share_cd():
            return
        global_data.player.call_server_method('share_winning_info_to_channel', (CHAT_WORLD, self._winning_info))
        global_data.game_mgr.show_tip(get_text_by_id(2177))

    def _change_scene(self):
        from logic.gcommon.common_const import scene_const
        from logic.client.const import lobby_model_display_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.MAIN_RANK_SCENE, scene_content_type=scene_const.SCENE_MAIN_RANK)

    def refresh_by_uid(self, uid):
        self._cur_uid = uid
        player_inf = self._message_data.get_player_detail_inf(self._cur_uid)
        if player_inf and time.time() - player_inf['save_time'] < 300:
            self.on_refresh_player_detail_inf(player_inf)
        else:
            global_data.player.request_player_detail_inf(self._cur_uid)

    def on_refresh_player_detail_inf(self, player_inf):
        if player_inf[U_ID] != self._cur_uid:
            return
        self._player_detail_inf = player_inf
        player_info_nd = self.panel.nd_player_info_1
        head_frame = self._player_detail_inf[HEAD_FRAME]
        head_photo = self._player_detail_inf[HEAD_PHOTO]
        init_role_head(player_info_nd.temp_head, head_frame, head_photo)
        player_info_nd.lab_name.SetString(self._player_detail_inf[C_NAME])
        player_info_nd.lab_id.SetString(str(self._player_detail_inf[U_ID]))
        self._show_model()

    def _show_model(self):
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.panel.DelayCallWithTag(self.DELAY_TIME, self._do_show_model, self.DELAY_TAG)

    def _do_show_model(self):
        if not self.panel or not self.panel.isVisible():
            return
        else:
            if not self._player_detail_inf:
                return
            if self._cur_uid == global_data.player.uid:
                mecha_id = global_data.player.get_lobby_selected_mecha_id()
                mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
                mecha_item_no = global_data.player.get_mecha_fashion(mecha_item_id)
                role_id = global_data.player.get_role()
                item_data = global_data.player.get_item_by_no(role_id)
                fashion_data = item_data.get_fashion()
            else:
                mecha_item_no = self._player_detail_inf.get(item_const.MECHA_LOBBY_FASHION_KEY, None)
                if mecha_item_no is None:
                    mecha_item_no = self._player_detail_inf.get(item_const.MECHA_LOBBY_ID_KEY, 101008001)
                fashion_data = self._player_detail_inf.get(item_const.INF_ROLE_FASHION_KEY, {})
            role_item_no = fashion_data.get(item_const.FASHION_POS_SUIT, 201001100)
            role_head_no = fashion_data.get(item_const.FASHION_POS_HEADWEAR, None)
            bag_id = fashion_data.get(item_const.FASHION_POS_BACK, None)
            suit_id = fashion_data.get(item_const.FASHION_POS_SUIT_2, None)
            other_pendants = [ fashion_data.get(pos) for pos in item_const.FASHION_OTHER_PENDANT_LIST ]
            if role_item_no <= 0 or mecha_item_no <= 0:
                return
            if self.cur_show_model_item_no == (role_item_no, mecha_item_no):
                return
            self.cur_show_model_item_no = (role_item_no, mecha_item_no)
            is_mine = True if self._cur_uid == global_data.player.uid else False
            role_model_data = lobby_model_display_utils.get_lobby_model_data(role_item_no, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
            for data in role_model_data:
                data['model_scale'] = data.get('model_scale', 1.0) * const.ROLE_SCALE
                data['off_euler_rot'][1] = const.ROLE_ROTATION_Y
                data['ignore_chuchang_sfx'] = True
                if not is_mine and fashion_data.get(item_const.FASHION_POS_WEAPON_SFX):
                    data['improved_skin_sfx_id'] = fashion_data[item_const.FASHION_POS_WEAPON_SFX]

            mecha_model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_no, is_get_player_data=is_mine)
            for data in mecha_model_data:
                data['skin_id'] = mecha_item_no
                data['model_scale'] = data.get('model_scale', 1.0) * const.MECHA_SCALE
                data['off_euler_rot'][1] = const.MECHA_ROTATION_Y
                if is_mine:
                    data['decal_list'] = global_data.player.get_mecha_decal().get(str(get_main_skin_id(mecha_item_no)), [])
                    data['color_dict'] = global_data.player.get_mecha_color().get(str(mecha_item_no), {})
                else:
                    skin_define_data = self._player_detail_inf.get(item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY, {})
                    if skin_define_data:
                        data['decal_list'] = skin_define_data.get('decal', [])
                        data['color_dict'] = skin_define_data.get('color', {})
                if not is_mine and self._player_detail_inf.get(item_const.MECHA_LOBBY_WP_SFX_KEY) > 0:
                    data['shiny_weapon_id'] = self._player_detail_inf.get(item_const.MECHA_LOBBY_WP_SFX_KEY)

            global_data.emgr.change_model_display_scene_item_ex.emit(mecha_model_data, role_model_data, create_callback=self._on_load_model_success)
            self._loaded_model_set = set()
            return

    def _on_load_model_success(self, model):
        self._loaded_model_set.add(model.get_unique_id())

    def on_click_close_btn(self, *args):
        self.close()

    def on_click_channel_choose_ui(self, *args):
        self.on_switch_share_channel(None)
        return

    def close_share(self, *args):
        self._tmp_show_share_channel = False
        nd_share = self.panel.nd_share
        nd_share.btn_share.img_icon.SetFlippedY(self._tmp_show_share_channel)
        nd_share.list_share.setVisible(self._tmp_show_share_channel)

    def on_switch_share_channel(self, channel):
        nd_share = self.panel.nd_share
        self._tmp_show_share_channel = not self._tmp_show_share_channel
        if channel is not None:
            if not self.check_cd(channel):
                return
            global_data.player.call_server_method('share_winning_info_to_channel', (channel, self._winning_info))
            global_data.game_mgr.show_tip(get_text_by_id(2177))
        nd_share.btn_share.img_icon.SetFlippedY(self._tmp_show_share_channel)
        nd_share.list_share.setVisible(self._tmp_show_share_channel)
        return

    def on_click_share_ui(self, *args):
        self.try_share()

    def on_click_switch(self, *args):
        self._switch_info_status()
        self._refresh_battle_statistic_info()

    def check_cd(self, channel):
        res_time = WinningStreakUI.LAST_SHARE_TIME[channel] + 60 - time.time()
        if res_time > 0:
            global_data.game_mgr.show_tip(get_text_by_id(10273).format(int(res_time)))
            return False
        WinningStreakUI.LAST_SHARE_TIME[channel] = time.time()
        return True

    def set_winning_info(self, info, uid, raw_data):
        if global_data.player.uid == uid:
            self.panel.nd_share.setVisible(True)
        else:
            self.panel.nd_share.setVisible(False)
        self._winning_info = info
        self._raw_data = raw_data
        self._uid = uid
        time = get_date_str('%Y.%m.%d', timestamp=info.get('streak_update_time', 0))
        self.panel.nd_data.lab_num.SetString(str(info.get('winning_streak', 0)))
        self.panel.lab_day.SetString(time)
        self._refresh_battle_statistic_info()
        self.panel.nd_qr.setVisible(False)
        self.refresh_by_uid(uid)

    def _switch_info_status(self):
        if self._info_status == self.STATUS_TOTAL_INFO:
            self._info_status = self.STATUS_AVG_INFO
        else:
            self._info_status = self.STATUS_TOTAL_INFO

    def _refresh_battle_statistic_info(self):
        info = self._winning_info
        status = self._info_status
        if status == self.STATUS_TOTAL_INFO:
            self.panel.nd_data.nd_data_1.lab_value.SetString(str(info.get('streak_kill_mecha', 0)))
            self.panel.nd_data.nd_data_2.lab_value.SetString(str(info.get('streak_kill_human', 0)))
            self.panel.nd_data.nd_data_3.lab_value.SetString(str(int(info.get('streak_total_damage', 0))))
            self.panel.nd_data.nd_data_1.lab_data.SetString(get_text_by_id(304))
            self.panel.nd_data.nd_data_2.lab_data.SetString(get_text_by_id(303))
            self.panel.nd_data.nd_data_3.lab_data.SetString(get_text_by_id(5074))
        else:
            winning_streak = info.get('winning_streak', 1)
            per_kill_mecha = float(info.get('streak_kill_mecha', 0)) / winning_streak
            per_kill_human = float(info.get('streak_kill_human', 0)) / winning_streak
            per_damage = float(info.get('streak_total_damage', 0)) / winning_streak
            data_list = [
             per_kill_mecha,
             per_kill_human,
             per_damage]
            node_list = [
             self.panel.nd_data.nd_data_1.lab_value,
             self.panel.nd_data.nd_data_2.lab_value,
             self.panel.nd_data.nd_data_3.lab_value]
            for i in range(len(data_list)):
                data = data_list[i]
                if i == 2:
                    node_list[i].SetString('%d' % data)
                else:
                    node_list[i].SetString('%.1f' % data)

            self.panel.nd_data.nd_data_1.lab_data.SetString(get_text_by_id(634135))
            self.panel.nd_data.nd_data_2.lab_data.SetString(get_text_by_id(634136))
            self.panel.nd_data.nd_data_3.lab_data.SetString(get_text_by_id(634137))