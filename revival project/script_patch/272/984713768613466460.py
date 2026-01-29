# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPinganjing/ActivityH5InviteRecruitWidget.py
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import rank_const
from logic.gutils import share_utils
from common.cfg import confmgr
from logic.comsys.share.ShareScreenCaptureUI import ShareScreenCaptureUI
from logic.gcommon.const import PLAYER_INFO_DETAIL
from logic.gutils.role_head_utils import set_role_head_photo
from logic.gutils.activity_utils import get_activity_conf_ui_data
from logic.gutils.template_utils import init_tempate_reward
PROG_ICON_PATH = 'gui/ui_res_2/activity/activity_202307/h5_recruitment/icon_h5_recruitment_arrow_{}.png'

class ActivityH5InviteRecruitWidget(object):

    def __init__(self, panel, activity_type):
        self.panel = panel
        self._activity_type = str(activity_type)
        self.init_parameters()
        self.init_ui()
        self.init_ui_event()
        self.init_event()

    def destroy(self):
        self._item_list = None
        global_data.emgr.message_on_player_detail_inf -= self.update_enlist_list
        global_data.emgr.message_on_newbie_enlist_succ -= self.update_view
        global_data.emgr.message_on_update_newbie_enlist_team_score -= self.update_top_widget
        global_data.emgr.message_on_receive_newbie_enlist_reward_ret -= self.update_top_widget
        return

    def init_parameters(self):
        self.icon_prog_dict = {'icon_prog_0': self.panel.icon_prog_0,
           'icon_prog_20': self.panel.icon_prog_20,
           'icon_prog_40': self.panel.icon_prog_40,
           'icon_prog_60': self.panel.icon_prog_60,
           'icon_prog_80': self.panel.icon_prog_80,
           'icon_prog_100': self.panel.icon_prog_100
           }

    def init_ui(self):
        self.panel.lab_tips_invitation.SetString(get_text_by_id(634807).format(global_data.player.get_newbie_enlist_code(self._activity_type)))
        temp_head = self.panel.temp_head
        set_role_head_photo(temp_head, global_data.player.get_head_photo())
        temp_head.lab_name.SetString(global_data.player.get_name())
        self.update_enlist_list()
        self.init_top_widget()

    def init_ui_event(self):

        @self.panel.temp_btn_1.btn_common.unique_callback()
        def OnClick(btn, touch):
            if global_data.player.get_recruit_newbie_enlist_count(self._activity_type) == 0:
                global_data.game_mgr.show_tip(get_text_by_id(634824))
            else:
                ui = global_data.ui_mgr.show_ui('ActivityH5MyInvite', 'logic.comsys.activity.ActivityPinganjing')
                ui.set_activity_type(self._activity_type)

        @self.panel.temp_btn_2.btn_common.unique_callback()
        def OnClick(btn, touch):

            def ready_share--- This code section failed: ---

  66       0  LOAD_CONST            1  'share_url'
           3  LOAD_FAST             0  'url'
           6  BUILD_TUPLE_2         2 
           9  PRINT_ITEM       
          10  PRINT_NEWLINE_CONT

  67      11  LOAD_FAST             0  'url'
          14  POP_JUMP_IF_FALSE    72  'to 72'

  68      17  LOAD_GLOBAL           0  'get_text_by_id'
          20  LOAD_CONST            2  634834
          23  CALL_FUNCTION_1       1 
          26  STORE_FAST            1  'share_message'

  69      29  LOAD_GLOBAL           0  'get_text_by_id'
          32  LOAD_CONST            3  634833
          35  CALL_FUNCTION_1       1 
          38  STORE_FAST            2  'share_title'

  70      41  LOAD_GLOBAL           1  'ShareScreenCaptureUI'
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

  72      72  LOAD_GLOBAL           2  'global_data'
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

    def init_event(self):
        global_data.emgr.message_on_player_detail_inf += self.update_enlist_list
        global_data.emgr.message_on_newbie_enlist_succ += self.update_view
        global_data.emgr.message_on_update_newbie_enlist_team_score += self.update_top_widget
        global_data.emgr.message_on_receive_newbie_enlist_reward_ret += self.update_top_widget

    def update_view(self):
        self.update_enlist_list()
        self.update_top_widget()

    def update_enlist_list(self, *args):
        enlist_uid_list = global_data.player.get_recruit_newbie_enlist_uid_list(self._activity_type)
        list_role_head = self.panel.list_role_head
        list_role_head.DeleteAllSubItem()
        for uid in enlist_uid_list:
            uid = int(uid)
            item = list_role_head.AddTemplateItem()
            player_info = global_data.message_data.get_player_detail_inf(uid)
            if not player_info:
                player_info = {}
            set_role_head_photo(item, player_info.get('head_photo', None))
            item.lab_name.SetString(player_info.get('char_name', ''))

        temp_btn_1 = self.panel.temp_btn_1.btn_common
        if len(enlist_uid_list) == 0:
            temp_btn_1.SetShowEnable(False)
        else:
            temp_btn_1.SetShowEnable(True)
        temp_btn_2 = self.panel.temp_btn_2.btn_common
        temp_btn_2.SetText(get_text_by_id(634816))
        temp_btn_2.SetShowEnable(True)
        return

    def init_top_widget(self):
        self._item_list = {}
        gift_str = 'enlist_newbie_gift' if global_data.player.check_is_newbie_on_start(self._activity_type) else 'enlist_gift'
        enlist_recruit_gift = get_activity_conf_ui_data(self._activity_type, gift_str)
        list_item = self.panel.list_item
        list_item.DeleteAllSubItem()
        for gift_info in enlist_recruit_gift:
            score, reward_id = gift_info[0], gift_info[1]
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no = reward_list[0][0]
            num = reward_list[0][1]
            item = list_item.AddTemplateItem()
            self._item_list[int(score)] = item
            init_tempate_reward(item, item_no, num, show_tips=True)
            btn_choose = item.btn_choose
            btn_choose.EnableCustomState(True)

            @btn_choose.unique_callback()
            def OnClick(btn, touch, score=int(score), item_no=item_no):
                current_score = global_data.player.get_recruit_newbie_enlist_score(self._activity_type)
                if not global_data.player.check_recruit_reward_has_receive(self._activity_type, score) and current_score >= score:
                    global_data.player.receive_newbie_enlist_reward(self._activity_type, score)
                else:
                    x, y = btn.GetPosition()
                    w, _ = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                return

        self.update_top_widget()

    def update_top_widget(self):
        current_score = global_data.player.get_recruit_newbie_enlist_score(self._activity_type)
        self.panel.lab_points.SetString(str(current_score))
        for score, item in self._item_list.items():
            score = int(score)
            max_score = score
            if global_data.player.check_recruit_reward_has_receive(self._activity_type, score):
                item.btn_choose.SetSelect(False)
                item.nd_get.setVisible(True)
            else:
                item.nd_get.setVisible(False)
                if current_score >= score:
                    item.btn_choose.SetSelect(True)
                else:
                    item.btn_choose.SetSelect(False)
            if current_score >= score:
                self.icon_prog_dict.get('icon_prog_{}'.format(score)).SetDisplayFrameByPath('', PROG_ICON_PATH.format('1'))
            else:
                self.icon_prog_dict.get('icon_prog_{}'.format(score)).SetDisplayFrameByPath('', PROG_ICON_PATH.format('2'))

        self.panel.prog.SetPercent(current_score / float(max_score) * 100)