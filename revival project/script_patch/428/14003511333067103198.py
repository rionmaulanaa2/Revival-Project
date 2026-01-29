# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPinganjing/ActivityH5MyInvite.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common import utilities
from logic.gcommon import const
from logic.gutils import template_utils
from logic.gutils import role_head_utils
from logic.gutils import online_state_utils
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.cdata import dan_data
from logic.gutils import season_utils
import cc
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from common.cfg import confmgr

class ActivityH5MyInvite(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202307/h5_recruitment/open_h5_recruitment_team'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close',
       'btn_share.OnClick': 'on_click_btn_share'
       }
    GLOBAL_EVENT = {'message_on_players_detail_inf': 'on_players_detail_inf'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        self._activity_type = None
        return

    def set_activity_type(self, activity_type):
        self._activity_type = activity_type
        self.request_players_info()

    def do_show_panel(self):
        super(ActivityH5MyInvite, self).do_show_panel()

    def request_players_info(self):
        uids = global_data.player.get_recruit_newbie_enlist_uid_list(self._activity_type)
        message_data = global_data.message_data
        count = 0
        r_uid_list = []
        for uid in uids:
            uid = int(uid)
            if not message_data.has_player_inf(uid):
                r_uid_list.append(uid)
                count += 1

        if count > 0:
            global_data.player.request_players_detail_inf(r_uid_list)
        else:
            self.on_players_detail_inf()

    def on_players_detail_inf(self, *args):
        self.show_my_list()

    def add_player_simple_callback(self, panel, uid):

        @panel.unique_callback()
        def OnClick(layer, touch):
            from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
            if global_data.player and uid == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.refresh_by_uid(uid)
                ui.set_position(touch.getLocation(), cc.Vec2(0.0, 0.5))

    def on_click_btn_share(self, *args):
        self.do_share()

    def do_share(self):

        def ready_share--- This code section failed: ---

  86       0  LOAD_CONST            1  'share_url'
           3  LOAD_FAST             0  'url'
           6  BUILD_TUPLE_2         2 
           9  PRINT_ITEM       
          10  PRINT_NEWLINE_CONT

  87      11  LOAD_FAST             0  'url'
          14  POP_JUMP_IF_FALSE    72  'to 72'

  88      17  LOAD_GLOBAL           0  'get_text_by_id'
          20  LOAD_CONST            2  634834
          23  CALL_FUNCTION_1       1 
          26  STORE_FAST            1  'share_message'

  89      29  LOAD_GLOBAL           0  'get_text_by_id'
          32  LOAD_CONST            3  634833
          35  CALL_FUNCTION_1       1 
          38  STORE_FAST            2  'share_title'

  90      41  LOAD_GLOBAL           1  'ShareScreenCaptureUI'
          44  LOAD_CONST            4  'text'
          47  LOAD_CONST            5  607229
          50  LOAD_CONST            6  'share_link'
          53  LOAD_CONST            7  'share_title'
          56  LOAD_FAST             2  'share_title'
          59  LOAD_CONST            8  'share_message'
          62  LOAD_FAST             1  'share_message'
          65  CALL_FUNCTION_1024  1024 
          68  POP_TOP          
          69  JUMP_FORWARD         22  'to 94'

  92      72  LOAD_GLOBAL           2  'global_data'
          75  LOAD_ATTR             3  'game_mgr'
          78  LOAD_ATTR             4  'show_tip'
          81  LOAD_GLOBAL           0  'get_text_by_id'
          84  LOAD_CONST            9  193
          87  CALL_FUNCTION_1       1 
          90  CALL_FUNCTION_1       1 
          93  POP_TOP          
        94_0  COME_FROM                '69'

Parse error at or near `CALL_FUNCTION_1024' instruction at offset 65

        share_utils.get_h5_invite_url(ready_share, global_data.player.get_newbie_enlist_code(self._activity_type))

    def show_my_list(self):
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        message_data = global_data.message_data
        friend_online_state = message_data.get_player_online_state()
        uids = list(global_data.player.get_recruit_newbie_enlist_uid_list(self._activity_type))
        count = len(uids)
        list_head = self.panel.list_partner
        list_head.DeleteAllSubItem()
        list_head.SetInitCount(count)
        has_player = bool(count)
        self.panel.nd_noplayer.setVisible(not has_player)
        self.panel.nd_contain.setVisible(has_player)
        for i, uid in enumerate(uids):
            uid = int(uid)
            item_widget = list_head.GetItem(i)
            player_info = message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
            if not player_info:
                player_info = {}
            state = int(friend_online_state.get(int(uid), const.STATE_OFFLINE))
            _, color = ui_utils.get_online_inf(state)
            name = player_info.get('char_name', '')
            item_widget.lab_name.SetString(name)
            item_widget.lab_name.SetColor(color)
            role_head_utils.set_role_head_photo(item_widget.temp_head, player_info.get('head_photo', None))
            role_head_utils.set_role_head_frame(item_widget.temp_head, player_info.get('head_frame', None))
            self.add_player_simple_callback(item_widget.temp_head, uid)
            cur_level = player_info.get('lv', 1)
            item_widget.temp_head.btn_lv.SetText(str(cur_level))
            item_widget.temp_head.btn_lv.setVisible(True)
            dan_info = player_info.get('dan_info', {})
            if 'survival_dan' in dan_info:
                survival_dan = dan_info.get('survival_dan', {})
            else:
                survival_dan = dan_info
            dan = survival_dan.get('dan', dan_data.BROZE)
            lv = survival_dan.get('lv', dan_data.get_lv_num(dan_data.BROZE))
            item_widget.img_rank.SetDisplayFrameByPath('', role_head_utils.get_dan_path(dan, lv))
            item_widget.lab_rank.SetString(season_utils.get_dan_lv_name(dan, lv))
            sex = player_info.get('sex', const.AVATAR_SEX_NONE)
            template_utils.set_sex_node_img(item_widget.img_gender, sex)
            online = not online_state_utils.is_not_online(state)
            item_widget.btn_party.SetShowEnable(online)
            if online:
                color = 7616256
                img_path = 'gui/ui_res_2/common/button/btn_secondary_major.png'
                item_widget.btn_party.SetText(10004, None, color, color, color)
                item_widget.btn_party.SetFrames('', [img_path, img_path, img_path])
                role_head_utils.set_gray(item_widget.temp_head, False)
            else:
                color = 15523828
                item_widget.btn_party.SetText(609970, None, color, color, color)
                img_path = 'gui/ui_res_2/common/button/btn_secondary_minor.png'
                item_widget.btn_party.SetFrames('', [img_path, img_path, img_path])
                role_head_utils.set_gray(item_widget.temp_head, True)

            @item_widget.btn_party.unique_callback()
            def OnClick(btn, touch, uid=uid, online=online):
                self.on_click_party(uid, online)

        return

    def on_click_party(self, uid, online):
        from logic.gutils import share_utils
        from logic.gcommon.common_const.log_const import TEAM_MODE_INFO
        from logic.gcommon.common_const.battle_const import DEFAULT_INVITE_TID
        from logic.comsys.share.ShareScreenCaptureUI import ShareScreenCaptureUI
        if online:
            battle_tid = global_data.player.get_battle_tid()
            if battle_tid is None:
                battle_tid = DEFAULT_INVITE_TID
            team_info = global_data.player.get_team_info() or {}
            auto_flag = team_info.get('auto_match', global_data.player.get_self_auto_match())
            global_data.player.invite_frd(uid, battle_tid, auto_flag, TEAM_MODE_INFO)
        else:

            def ready_share--- This code section failed: ---

 187       0  LOAD_CONST            1  'share_url'
           3  LOAD_FAST             0  'url'
           6  BUILD_TUPLE_2         2 
           9  PRINT_ITEM       
          10  PRINT_NEWLINE_CONT

 188      11  LOAD_FAST             0  'url'
          14  POP_JUMP_IF_FALSE    72  'to 72'

 189      17  LOAD_GLOBAL           0  'get_text_by_id'
          20  LOAD_CONST            2  634834
          23  CALL_FUNCTION_1       1 
          26  STORE_FAST            1  'share_message'

 190      29  LOAD_GLOBAL           0  'get_text_by_id'
          32  LOAD_CONST            3  634833
          35  CALL_FUNCTION_1       1 
          38  STORE_FAST            2  'share_title'

 191      41  LOAD_DEREF            0  'ShareScreenCaptureUI'
          44  LOAD_CONST            4  'text'
          47  LOAD_CONST            5  607229
          50  LOAD_CONST            6  'share_link'
          53  LOAD_CONST            7  'share_title'
          56  LOAD_FAST             2  'share_title'
          59  LOAD_CONST            8  'share_message'
          62  LOAD_FAST             1  'share_message'
          65  CALL_FUNCTION_1024  1024 
          68  POP_TOP          
          69  JUMP_FORWARD         22  'to 94'

 193      72  LOAD_GLOBAL           1  'global_data'
          75  LOAD_ATTR             2  'game_mgr'
          78  LOAD_ATTR             3  'show_tip'
          81  LOAD_GLOBAL           0  'get_text_by_id'
          84  LOAD_CONST            9  193
          87  CALL_FUNCTION_1       1 
          90  CALL_FUNCTION_1       1 
          93  POP_TOP          
        94_0  COME_FROM                '69'

Parse error at or near `CALL_FUNCTION_1024' instruction at offset 65

            share_utils.get_h5_invite_url(ready_share, global_data.player.get_newbie_enlist_code(self._activity_type))
        return