# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIInvite.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gutils import template_utils
from logic.gutils import role_head_utils
from logic.gutils import share_utils
from logic.client.const.share_const import DEEP_LINK_KIZUNA_AI_RECRUIT
from common.cfg import confmgr
from common.platform.dctool import interface
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon import const
from logic.gcommon.item import item_const
from cocosui import cc, ccui, ccs

def from_create_time_to_3days():
    from logic.gcommon import time_utility as tutil
    if not global_data.player:
        return 0
    now_stamp = tutil.get_server_time()
    create_time = global_data.player.get_create_time()
    return 3 * tutil.ONE_DAY_SECONDS - (now_stamp - create_time)


def has_link_btn():
    enlist_uids = global_data.player.get_spec_enlist_uids()
    if enlist_uids:
        return False
    has_gift = global_data.player.has_spec_enlist_verify_gift()
    enable_link = can_enlist_link() or has_gift
    return enable_link


def can_enlist_link():
    if not global_data.player:
        return False
    enlist_from_uid = global_data.player.get_spec_enlist_from_uid()
    if not enlist_from_uid and from_create_time_to_3days() > 0:
        return True
    return False


def has_score_reward--- This code section failed: ---

  48       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('ACTIVITY_KIZUNA_AI_RECRUIT',)
           6  IMPORT_NAME           0  'logic.gcommon.common_const.activity_const'
           9  IMPORT_FROM           1  'ACTIVITY_KIZUNA_AI_RECRUIT'
          12  STORE_FAST            0  'ACTIVITY_KIZUNA_AI_RECRUIT'
          15  POP_TOP          

  49      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('confmgr',)
          22  IMPORT_NAME           2  'common.cfg'
          25  IMPORT_FROM           3  'confmgr'
          28  STORE_FAST            1  'confmgr'
          31  POP_TOP          

  50      32  LOAD_FAST             1  'confmgr'
          35  LOAD_ATTR             4  'get'
          38  LOAD_CONST            4  'c_activity_config'
          41  LOAD_CONST            5  'cUiData'
          44  CALL_FUNCTION_3       3 
          47  STORE_FAST            2  'conf'

  51      50  LOAD_FAST             2  'conf'
          53  LOAD_CONST            0  ''
          56  COMPARE_OP            8  'is'
          59  POP_JUMP_IF_FALSE    71  'to 71'

  52      62  BUILD_LIST_0          0 
          65  STORE_FAST            3  'enlist_gifts'
          68  JUMP_FORWARD         18  'to 89'

  54      71  LOAD_FAST             2  'conf'
          74  LOAD_ATTR             4  'get'
          77  LOAD_CONST            6  'enlist_gift'
          80  BUILD_LIST_0          0 
          83  CALL_FUNCTION_2       2 
          86  STORE_FAST            3  'enlist_gifts'
        89_0  COME_FROM                '68'

  56      89  SETUP_LOOP           75  'to 167'
          92  LOAD_GLOBAL           6  'enumerate'
          95  LOAD_FAST             3  'enlist_gifts'
          98  CALL_FUNCTION_1       1 
         101  GET_ITER         
         102  FOR_ITER             61  'to 166'
         105  UNPACK_SEQUENCE_2     2 
         108  STORE_FAST            4  'i'
         111  STORE_FAST            5  'info'

  57     114  LOAD_FAST             5  'info'
         117  UNPACK_SEQUENCE_2     2 
         120  STORE_FAST            6  'score'
         123  STORE_FAST            7  '_'

  58     126  LOAD_GLOBAL           7  'global_data'
         129  LOAD_ATTR             8  'player'
         132  LOAD_ATTR             9  'get_spec_enlist_reward_st'
         135  LOAD_FAST             6  'score'
         138  CALL_FUNCTION_1       1 
         141  STORE_FAST            8  'status'

  59     144  LOAD_FAST             8  'status'
         147  LOAD_GLOBAL          10  'item_const'
         150  LOAD_ATTR            11  'ITEM_UNRECEIVED'
         153  COMPARE_OP            2  '=='
         156  POP_JUMP_IF_FALSE   102  'to 102'

  60     159  LOAD_GLOBAL          12  'True'
         162  RETURN_END_IF    
       163_0  COME_FROM                '156'
         163  JUMP_BACK           102  'to 102'
         166  POP_BLOCK        
       167_0  COME_FROM                '89'

  62     167  LOAD_GLOBAL          13  'False'
         170  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 44


SCORE_TO_PERCENT = {0: 8,20: 23,40: 39,60: 55,80: 71,100: 100}

class ActivityKizunaAIInvite(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaAIInvite, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_event(True)
        self.register_timer()
        self.panel.lan_time_limite.setVisible(False)
        self._timer_cb[0] = lambda : self.refresh_invite_time()
        self.refresh_invite_time()
        share_utils.get_kizunai_share_url('%s=%s' % (DEEP_LINK_KIZUNA_AI_RECRUIT, str(global_data.player.uid)), None)
        return

    def refresh_invite_time(self):
        enlist_from_uid = global_data.player.get_spec_enlist_from_uid()
        if enlist_from_uid:
            self.panel.lan_time_limite.setVisible(False)
            self.unregister_timer()
            return
        from logic.gcommon import time_utility as tutil
        left_time = from_create_time_to_3days()
        if left_time > 0:
            self.panel.lan_time_limite.setVisible(True)
            self.panel.lan_time_limite.SetString(get_text_by_id(607014).format(tutil.get_readable_time_2(left_time)))
        else:
            self.panel.lan_time_limite.setVisible(False)
            self.unregister_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        self.enlist_gifts = conf.get('enlist_gift', [])

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_players_detail_inf': self.on_players_detail_inf,
           'message_on_spec_enlist_verify': self.on_enlist_verify_gift,
           'message_on_spec_enlist_verify_gift': self.on_enlist_verify_gift,
           'message_on_spec_enlist_reward': self.on_enlist_reward,
           'message_on_spec_enlist_score': self.on_enlist_reward,
           'message_on_spec_enlist_my': self.on_enlist_my
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def do_share(self):
        from logic.comsys.share.CommonShareBubbleUI import CommonShareBubbleUI
        share_message = get_text_by_id(609971)
        share_title = get_text_by_id(602049)

        def share_cb(*argv):
            global_data.player.on_enlist_share()

        def ready_share--- This code section failed: ---

 144       0  LOAD_FAST             0  'url'
           3  POP_JUMP_IF_FALSE   130  'to 130'

 145       6  LOAD_DEREF            0  'CommonShareBubbleUI'
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

 146      42  LOAD_DEREF            4  'self'
          45  LOAD_ATTR             0  'panel'
          48  LOAD_ATTR             1  'nd_share_dot'
          51  STORE_FAST            2  'nd'

 147      54  LOAD_FAST             2  'nd'
          57  LOAD_ATTR             2  'getPosition'
          60  CALL_FUNCTION_0       0 
          63  STORE_FAST            3  'lpos'

 148      66  LOAD_FAST             2  'nd'
          69  LOAD_ATTR             3  'getParent'
          72  CALL_FUNCTION_0       0 
          75  LOAD_ATTR             4  'convertToWorldSpace'
          78  LOAD_FAST             3  'lpos'
          81  CALL_FUNCTION_1       1 
          84  STORE_FAST            4  'world_pos'

 149      87  LOAD_FAST             1  'ui'
          90  LOAD_ATTR             3  'getParent'
          93  CALL_FUNCTION_0       0 
          96  LOAD_ATTR             5  'convertToNodeSpace'
          99  LOAD_FAST             4  'world_pos'
         102  CALL_FUNCTION_1       1 
         105  STORE_FAST            3  'lpos'

 150     108  LOAD_FAST             1  'ui'
         111  JUMP_IF_FALSE_OR_POP   126  'to 126'
         114  LOAD_FAST             1  'ui'
         117  LOAD_ATTR             6  'setPosition'
         120  LOAD_FAST             3  'lpos'
         123  CALL_FUNCTION_1       1 
       126_0  COME_FROM                '111'
         126  POP_TOP          
         127  JUMP_FORWARD         22  'to 152'

 153     130  LOAD_GLOBAL           7  'global_data'
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

    def on_init_panel(self):
        global_data.player and global_data.player.query_ai_help_score()
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch):
            self.do_share()

        self.panel.img_point.setVisible(False)

        @self.panel.btn_my.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.activity import ActivityKizunaAIMyInvite
            ActivityKizunaAIMyInvite.ActivityKizunaAIMyInvite(None)
            return

        btn_question = self.panel.btn_question
        if btn_question:

            @btn_question.unique_callback()
            def OnClick(btn, touch):
                from logic.comsys.activity.KizunaAITeachingStepsUI import KizunaAITeachingStepsUI
                if interface.is_mainland_package():
                    KizunaAITeachingStepsUI()
                else:
                    dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                    dlg.set_show_rule(607801, 610021)
                    x, y = btn_question.GetPosition()
                    wpos = btn_question.GetParent().ConvertToWorldSpace(x, y)
                    dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                    template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.refresh_link_btn()
        self.request_players_info()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.show_reward_list()
        lv = global_data.player.get_lv()
        if global_data.player.has_spec_enlist_verify_gift() and lv >= 5:
            from logic.comsys.activity import ActivityKizunaAIInviteLink
            ActivityKizunaAIInviteLink.ActivityKizunaAIInviteLink(None)
        return

    def refresh_link_btn(self):

        @self.panel.btn_relevance.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.activity import ActivityKizunaAIInviteLink
            ActivityKizunaAIInviteLink.ActivityKizunaAIInviteLink(None)
            return

        self.panel.nd_relevance.setVisible(has_link_btn())
        enlist_from_uid = global_data.player.get_spec_enlist_from_uid()
        lv = global_data.player.get_lv()
        if not enlist_from_uid:
            text_id = 609949
        elif lv < 5:
            text_id = 609950
        else:
            text_id = 609951
        self.panel.btn_relevance.SetText(text_id)
        has_gift = global_data.player.has_spec_enlist_verify_gift()
        self.panel.btn_relevance.img_dot_red_01.setVisible(has_gift and lv >= 5)

    def show_reward_list(self):
        nd_reward_list = self.panel.list_item.temp_item_cell
        cur_score = global_data.player.get_total_spec_enlist_score()
        self.panel.lab_point_num.SetString(str(cur_score))
        for i, info in enumerate(self.enlist_gifts):
            item_widget = nd_reward_list.GetItem(i)
            if not item_widget:
                continue
            score, reward_id = info
            rl = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = rl[0]
            temp_item_ui = item_widget.temp_item
            if item_num > 1:
                temp_item_ui.lab_quantity.setVisible(True)
                temp_item_ui.lab_quantity.SetString(str(item_num))
            else:
                temp_item_ui.lab_quantity.setVisible(False)

            @temp_item_ui.btn_choose.callback()
            def OnClick(btn, touch, temp_item_ui=temp_item_ui, score=score, item_no=item_no):
                status = global_data.player.get_spec_enlist_reward_st(score)
                can_get = True if status == item_const.ITEM_UNRECEIVED else False
                if can_get:
                    global_data.player.receive_spec_enlist_reward(score)
                else:
                    x, y = btn.GetPosition()
                    w, h = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                return

        if cur_score < 0:
            percent = 0
        elif cur_score >= 100:
            percent = 100
        else:
            last_score_key = cur_score / 20 * 20
            next_score_key = last_score_key + 20
            last_percent = SCORE_TO_PERCENT.get(last_score_key)
            next_percent = SCORE_TO_PERCENT.get(next_score_key)
            percent = last_percent + 1.0 * (cur_score - last_score_key) / (next_score_key - last_score_key) * (next_percent - last_percent)
        self.panel.img_progress.SetPercentage(percent)
        self.panel.img_progress_02.SetPercentage(percent)
        self.refresh_reward_list()

    def refresh_reward_list(self):
        nd_reward_list = self.panel.list_item.temp_item_cell
        cur_score = global_data.player.get_total_spec_enlist_score()
        cur_score1 = global_data.player.get_spec_enlist_score()
        cur_score2 = global_data.player.get_spec_team_score()
        cur_score3 = global_data.player.get_ai_help_score()
        self.panel.lab_point_num.SetString(str(cur_score))
        self.panel.lab_num_recruit.SetString(str(cur_score1))
        self.panel.lab_num_party.SetString(str(cur_score2))
        self.panel.lab_num_call.SetString(str(cur_score3))
        for i, info in enumerate(self.enlist_gifts):
            item_widget = nd_reward_list.GetItem(i)
            if not item_widget:
                continue
            score, _ = info
            item_widget.lab_node_num.SetString(str(score))
            status = global_data.player.get_spec_enlist_reward_st(score)
            is_get = True if status == item_const.ITEM_RECEIVED else False
            item_widget.img_get.setVisible(is_get)
            if status == item_const.ITEM_UNRECEIVED:
                can_get = True if 1 else False
                item_widget.plis_lizi.setVisible(can_get)
                item_widget.img_can_get.setVisible(can_get)

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
        self.show_my_invite()

    def on_enlist_verify_gift(self):
        global_data.player.read_activity_list(self._activity_type)
        self.refresh_link_btn()

    def on_enlist_my(self):
        global_data.player.read_activity_list(self._activity_type)
        self.refresh_link_btn()
        self.show_my_invite()

    def on_enlist_reward(self):
        global_data.player.read_activity_list(self._activity_type)
        self.refresh_reward_list()

    def add_player_simple_callback(self, panel, uid):

        @panel.unique_callback()
        def OnClick(layer, touch):
            from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
            if global_data.player and uid == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.refresh_by_uid(uid)
                ui.set_position(touch.getLocation(), cc.Vec2(0.0, 0.0))

    def show_my_invite(self):
        uids = list(global_data.player.get_spec_enlist_uids())
        message_data = global_data.message_data
        count = len(uids)
        show_count = max(4, count + 1)
        list_head = self.panel.list_head
        list_head.DeleteAllSubItem()
        list_head.SetInitCount(show_count)
        for i in range(show_count):
            item_widget = list_head.GetItem(i)
            item_widget.btn_empty.setVisible(False)
            item_widget.temp_head.setVisible(False)
            if i >= count:
                item_widget.btn_empty.setVisible(True)
                item_widget.lab_name.SetString(609968)
                continue
            item_widget.temp_head.setVisible(True)
            uid = uids[i]
            player_info = message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
            if not player_info:
                player_info = {}
            role_head_utils.init_role_head(item_widget.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            self.add_player_simple_callback(item_widget.temp_head, uid)
            item_widget.btn_lv.SetText(str(player_info.get('lv', 1)))
            item_widget.lab_name.SetString(player_info.get('char_name', ''))
            item_widget.temp_head.img_head_frame.setVisible(False)
            item_widget.temp_head.img_role_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202109/kizuna/new_player/img_frame_player1.png')

        return