# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIMyInvite.py
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

class ActivityKizunaAIMyInvite(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/new_player/i_activity_kizuna_party'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close',
       'btn_share.OnClick': 'on_click_btn_share'
       }
    GLOBAL_EVENT = {'message_on_players_detail_inf': 'on_players_detail_inf'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.request_players_info()
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        pass

    def do_show_panel(self):
        super(ActivityKizunaAIMyInvite, self).do_show_panel()

    def _on_login_reconnected(self, *args):
        self.close()

    def request_players_info(self):
        uids = global_data.player.get_spec_enlist_uids()
        message_data = global_data.message_data
        count = 0
        r_uid_list = []
        for uid in uids:
            if not message_data.has_player_inf(uid):
                r_uid_list.append(uid)
                count += 1

        if count > 0:
            global_data.player.request_players_detail_inf(r_uid_list)
        else:
            self.on_players_detail_inf()

    def on_players_detail_inf(self, *argv):
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

    def on_click_btn_share(self, btn, touch):
        self.do_share()

    def do_share(self):
        from logic.gutils import share_utils
        from logic.client.const.share_const import DEEP_LINK_KIZUNA_AI_RECRUIT
        from logic.comsys.share.CommonShareBubbleUI import CommonShareBubbleUI
        share_message = get_text_by_id(609971)
        share_title = get_text_by_id(602049)

        def share_cb(*argv):
            global_data.player.on_enlist_share()

        def ready_share--- This code section failed: ---

 106       0  LOAD_FAST             0  'url'
           3  POP_JUMP_IF_FALSE   130  'to 130'

 107       6  LOAD_DEREF            0  'CommonShareBubbleUI'
           9  LOAD_CONST            1  'share_link'
          12  LOAD_CONST            2  'share_title'
          15  LOAD_DEREF            1  'share_title'
          18  LOAD_CONST            3  'share_message'
          21  LOAD_DEREF            2  'share_message'
          24  LOAD_CONST            4  'desc'
          27  LOAD_DEREF            2  'share_message'
          30  LOAD_CONST            5  'share_cb'
          33  LOAD_DEREF            3  'share_cb'
          36  CALL_FUNCTION_1280  1280 
          39  STORE_FAST            1  'ui'

 108      42  LOAD_DEREF            4  'self'
          45  LOAD_ATTR             0  'panel'
          48  LOAD_ATTR             1  'nd_share_dot'
          51  STORE_FAST            2  'nd'

 109      54  LOAD_FAST             2  'nd'
          57  LOAD_ATTR             2  'getPosition'
          60  CALL_FUNCTION_0       0 
          63  STORE_FAST            3  'lpos'

 110      66  LOAD_FAST             2  'nd'
          69  LOAD_ATTR             3  'getParent'
          72  CALL_FUNCTION_0       0 
          75  LOAD_ATTR             4  'convertToWorldSpace'
          78  LOAD_FAST             3  'lpos'
          81  CALL_FUNCTION_1       1 
          84  STORE_FAST            4  'world_pos'

 111      87  LOAD_FAST             1  'ui'
          90  LOAD_ATTR             3  'getParent'
          93  CALL_FUNCTION_0       0 
          96  LOAD_ATTR             5  'convertToNodeSpace'
          99  LOAD_FAST             4  'world_pos'
         102  CALL_FUNCTION_1       1 
         105  STORE_FAST            3  'lpos'

 112     108  LOAD_FAST             1  'ui'
         111  JUMP_IF_FALSE_OR_POP   126  'to 126'
         114  LOAD_FAST             1  'ui'
         117  LOAD_ATTR             6  'setPosition'
         120  LOAD_FAST             3  'lpos'
         123  CALL_FUNCTION_1       1 
       126_0  COME_FROM                '111'
         126  POP_TOP          
         127  JUMP_FORWARD         22  'to 152'

 114     130  LOAD_GLOBAL           7  'global_data'
         133  LOAD_ATTR             8  'game_mgr'
         136  LOAD_ATTR             9  'show_tip'
         139  LOAD_GLOBAL          10  'get_text_by_id'
         142  LOAD_CONST            6  193
         145  CALL_FUNCTION_1       1 
         148  CALL_FUNCTION_1       1 
         151  POP_TOP          
       152_0  COME_FROM                '127'

Parse error at or near `CALL_FUNCTION_1280' instruction at offset 36

        share_utils.get_kizunai_share_url('%s=%s' % (DEEP_LINK_KIZUNA_AI_RECRUIT, str(global_data.player.uid)), ready_share)

    def show_my_list(self):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        from logic.gcommon.common_const.activity_const import ACTIVITY_KIZUNA_AI_RECRUIT
        from common.cfg import confmgr
        conf = confmgr.get('c_activity_config', ACTIVITY_KIZUNA_AI_RECRUIT, 'cUiData')
        team_score = conf.get('team_score', 5)
        message_data = global_data.message_data
        friend_online_state = message_data.get_player_online_state()
        uids = list(global_data.player.get_spec_enlist_uids())

        def cmp_func(a, b):
            a_score = global_data.player.get_spec_enlist_data(a)
            a_times = a_score / team_score
            b_score = global_data.player.get_spec_enlist_data(b)
            b_times = b_score / team_score
            if a_times >= 5:
                a_sort_index = 1
            else:
                a_sort_index = 0
            if b_times >= 5:
                b_sort_index = 1
            else:
                b_sort_index = 0
            return six_ex.compare(a_sort_index, b_sort_index)

        uids = sorted(uids, key=cmp_to_key(cmp_func))

        def cmp_func(a, b):
            state_a = int(friend_online_state.get(int(a), const.STATE_OFFLINE))
            state_b = int(friend_online_state.get(int(b), const.STATE_OFFLINE))
            if state_a == const.STATE_SINGLE:
                state_a += 20
            if state_b == const.STATE_SINGLE:
                state_b += 20
            return six_ex.compare(state_a, state_b)

        uids = sorted(uids, key=cmp_to_key(cmp_func), reverse=True)
        count = len(uids)
        list_head = self.panel.list_partner
        list_head.DeleteAllSubItem()
        list_head.SetInitCount(count)
        has_player = bool(count)
        self.panel.nd_noplayer.setVisible(not has_player)
        self.panel.nd_contain.setVisible(has_player)
        for i, uid in enumerate(uids):
            item_widget = list_head.GetItem(i)
            player_info = message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
            if not player_info:
                player_info = {}
            state = int(friend_online_state.get(int(uid), const.STATE_OFFLINE))
            text_id, color = ui_utils.get_online_inf(state)
            name = player_info.get('char_name', '')
            item_widget.lab_name.SetString(name)
            item_widget.lab_name.SetColor(color)
            role_head_utils.init_role_head(item_widget.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            self.add_player_simple_callback(item_widget.temp_head, uid)
            cur_level = player_info.get('lv', 1)
            item_widget.temp_head.btn_lv.SetText(str(cur_level))
            item_widget.temp_head.btn_lv.setVisible(True)
            score = global_data.player.get_spec_enlist_data(uid)
            times = score / team_score
            item_widget.lab_party_times.SetString(get_text_by_id(609734).format(times, 5))
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
                enough_time = times < 5
                color = 7616256 if enough_time else 2369169
                if enough_time:
                    img_path = 'gui/ui_res_2/common/button/btn_secondary_major.png' if 1 else 'gui/ui_res_2/common/button/btn_secondary_middle.png'
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
                        url, s_title, s_message = share_utils.get_mainland_invite_team_url()
                        ShareScreenCaptureUI(text=607229, share_link=url, share_title=s_title, share_message=s_message)
                    return

        return