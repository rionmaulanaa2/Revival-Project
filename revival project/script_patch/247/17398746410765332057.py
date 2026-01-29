# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMyInvite.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common import utilities
from logic.gcommon import const
from logic.gutils import template_utils
from logic.gutils import role_head_utils
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
import cc

class ActivityMyInvite(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_new_domestic/i_activity_recruit_pop'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'nd_touch.OnClick': 'close'
       }
    GLOBAL_EVENT = {'message_on_players_detail_inf': 'on_players_detail_inf'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):

        @self.panel.btn_ask.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(607801, 607816)
            x, y = self.panel.btn_ask.GetPosition()
            wpos = self.panel.btn_ask.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 0.5))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.request_players_info()
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        pass

    def do_show_panel(self):
        super(ActivityMyInvite, self).do_show_panel()

    def _on_login_reconnected(self, *args):
        self.close()

    def request_players_info(self):
        uids = global_data.player.get_enlist_uids()
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

    def show_my_list(self):
        from logic.gutils.role_head_utils import set_gray
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        message_data = global_data.message_data
        friend_online_state = message_data.get_player_online_state()
        uids = list(global_data.player.get_enlist_uids())

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
        list_head = self.panel.list
        list_head.DeleteAllSubItem()
        list_head.SetInitCount(count)
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
            role_head_utils.init_role_head(item_widget.temp_head.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            self.add_player_simple_callback(item_widget.temp_head.temp_head, uid)
            cur_level = player_info.get('lv', 1)
            item_widget.temp_head.btn_lv.SetText(str(cur_level))
            score = global_data.player.get_enlist_data(uid)
            item_widget.lab_core.SetString('{} {}'.format(get_text_by_id(800069), score))
            sex = player_info.get('sex', const.AVATAR_SEX_NONE)
            template_utils.set_sex_node_img(item_widget.img_sex, sex)
            if cur_level < 10:
                min_level = 0
                top_level = 10
            elif cur_level < 100:
                min_level = cur_level / 10 * 10
                if cur_level >= min_level + 5:
                    min_level += 5
                top_level = min_level + 5
            else:
                min_level = 95
                top_level = 100
            item_widget.lab_level.SetString(get_text_by_id(81809, {'lv': min_level}))
            if min_level == 100:
                item_widget.lab_level01.SetString('-')
            else:
                item_widget.lab_level01.SetString(get_text_by_id(81809, {'lv': top_level}))
            item_widget.prog_bar.SetPercentage(utilities.safe_percent(cur_level - min_level, top_level - min_level))
            if state != const.STATE_OFFLINE:
                online = True if 1 else False
                item_widget.btn_team.SetShowEnable(online)
                if online:
                    item_widget.btn_team.SetText(80956)
                    role_head_utils.set_gray(item_widget.temp_head.temp_head, False)
                else:
                    item_widget.btn_team.SetText(13002)
                    role_head_utils.set_gray(item_widget.temp_head.temp_head, True)

                @item_widget.btn_team.unique_callback()
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