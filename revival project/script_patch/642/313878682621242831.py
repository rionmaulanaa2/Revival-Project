# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPinganjing/ActivityH5Invite.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.activity_utils import get_activity_conf_ui_data
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from .ActivityH5InviteBindingWidget import ActivityH5InviteBindingWidget
from .ActivityH5InviteRecruitWidget import ActivityH5InviteRecruitWidget
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gcommon import time_utility as tutil

def check_binding_red_point--- This code section failed: ---

  16       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  LOAD_ATTR             2  'check_is_newbie_on_start'
           9  LOAD_FAST             0  'activity_type'
          12  CALL_FUNCTION_1       1 
          15  POP_JUMP_IF_TRUE     22  'to 22'

  18      18  LOAD_GLOBAL           3  'False'
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

  19      22  LOAD_GLOBAL           4  'get_activity_conf_ui_data'
          25  LOAD_GLOBAL           1  'player'
          28  CALL_FUNCTION_2       2 
          31  STORE_FAST            1  'enlist_bind_gift'

  20      34  LOAD_GLOBAL           0  'global_data'
          37  LOAD_ATTR             1  'player'
          40  LOAD_ATTR             5  'get_binding_newbie_enlist_score'
          43  LOAD_FAST             0  'activity_type'
          46  CALL_FUNCTION_1       1 
          49  STORE_FAST            2  'current_score'

  21      52  SETUP_LOOP           73  'to 128'
          55  LOAD_FAST             1  'enlist_bind_gift'
          58  GET_ITER         
          59  FOR_ITER             65  'to 127'
          62  STORE_FAST            3  'gift_info'

  22      65  LOAD_FAST             3  'gift_info'
          68  LOAD_CONST            2  ''
          71  BINARY_SUBSCR    
          72  LOAD_FAST             3  'gift_info'
          75  LOAD_CONST            3  1
          78  BINARY_SUBSCR    
          79  ROT_TWO          
          80  STORE_FAST            4  'score'
          83  STORE_FAST            5  '_'

  23      86  LOAD_GLOBAL           0  'global_data'
          89  LOAD_ATTR             1  'player'
          92  LOAD_ATTR             6  'check_binding_reward_has_receive'
          95  LOAD_FAST             0  'activity_type'
          98  LOAD_FAST             4  'score'
         101  CALL_FUNCTION_2       2 
         104  UNARY_NOT        
         105  POP_JUMP_IF_FALSE    59  'to 59'
         108  LOAD_FAST             2  'current_score'
         111  LOAD_FAST             4  'score'
         114  COMPARE_OP            5  '>='
       117_0  COME_FROM                '105'
         117  POP_JUMP_IF_FALSE    59  'to 59'

  25     120  LOAD_GLOBAL           7  'True'
         123  RETURN_END_IF    
       124_0  COME_FROM                '117'
         124  JUMP_BACK            59  'to 59'
         127  POP_BLOCK        
       128_0  COME_FROM                '52'

  26     128  LOAD_GLOBAL           3  'False'
         131  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 28


def check_recruit_red_point(activity_type):
    is_newbie = global_data.player.get_recruit_newbie_enlist_count(activity_type) > 0
    gift_str = 'enlist_newbie_gift' if is_newbie else 'enlist_gift'
    enlist_recruit_gift = get_activity_conf_ui_data(activity_type, gift_str)
    current_score = global_data.player.get_recruit_newbie_enlist_score(activity_type)
    for gift_info in enlist_recruit_gift:
        score, _ = gift_info[0], gift_info[1]
        if not global_data.player.check_recruit_reward_has_receive(activity_type, score) and current_score >= score:
            return True

    return False


class InviteWindowTopSingleSelectListHelper(WindowTopSingleSelectListHelper):

    def set_up_list(self, list_tab, data_list, template_func, click_cb):
        self.cur_select_node = None
        list_tab.SetInitCount(len(data_list))
        allItems = list_tab.GetAllItem()
        for idx, item in enumerate(allItems):
            if template_func:
                template_func(item, data_list[idx])
            item.btn_tab.SetSelect(False)
            item.btn_tab.EnableCustomState(True)
            data = data_list[idx]

            @item.btn_tab.unique_callback()
            def OnClick(btn, touch, item=item, data=data, idx=idx):
                if click_cb:
                    click_cb(item, data, idx=idx)

        return


class ActivityH5Invite(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityH5Invite, self).__init__(dlg, activity_type)
        self._activity_type = activity_type

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.init_widget()
        self.init_ui_event()

    def init_parameters(self):
        self.tab_item_list = []
        self.tab_list = [{'index': 0,'text': 634826,'text2': 634804,'widget_func': self.init_binding_template,'anim_name': 'show_binding'}, {'index': 1,'text': 634805,'text2': 634805,'widget_func': self.init_recruit_template,'anim_name': 'show_recruit'}]
        self._binding_widget = None
        self._recruit_widget = None
        self._isAniming = False
        self._current_index = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_newbie_enlist_verify': self.update_invite_btn,
           'message_on_update_newbie_enlist_newbie_score': self.check_red_point,
           'message_on_receive_newbie_enlist_bind_reward': self.check_red_point,
           'message_on_update_newbie_enlist_team_score': self.check_red_point,
           'message_on_receive_newbie_enlist_reward_ret': self.check_red_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self._recruit_widget = ActivityH5InviteRecruitWidget(self.panel.temp_recruit, self._activity_type)
        if global_data.player.check_is_newbie_on_start(self._activity_type):
            self._binding_widget = ActivityH5InviteBindingWidget(self.panel.temp_binding, self._activity_type)
            self.init_invite_bar()
        else:
            self.panel.PlayAnimation('show_recruit')
            self.panel.list_tab.setVisible(False)
        self.check_red_point()

    def init_ui_event(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(634814, 634835)

    def init_invite_bar(self):
        list_tab = self.panel.list_tab

        def init_invite_btn(node, data):
            self.tab_item_list.append(node)
            self.update_invite_btn(node, data)

        def invite_btn_click_cb(ui_item, data, idx):
            if not self._isAniming:
                self.panel.PlayAnimation(data.get('anim_name'))
                self._isAniming = True
                self._invite_bar_wrapper.set_node_select(ui_item)
            else:
                return
            delay = 0.66

            def cb():
                self._isAniming = False

            self.panel.DelayCall(delay, cb)

        self._invite_bar_wrapper = InviteWindowTopSingleSelectListHelper()
        self._invite_bar_wrapper.set_up_list(list_tab, self.tab_list, init_invite_btn, invite_btn_click_cb)
        self._invite_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def init_binding_template(self, nd):
        return ActivityH5InviteBindingWidget(nd)

    def init_recruit_template(self, nd):
        return ActivityH5InviteRecruitWidget(nd)

    def update_invite_btn(self, node=None, data=None):
        enlist_from_uid = global_data.player.get_newbie_enlist_from_uid(self._activity_type)
        if node and data:
            if enlist_from_uid:
                node.btn_tab.SetText(get_text_by_id(data.get('text2', '')))
            else:
                node.btn_tab.SetText(get_text_by_id(data.get('text', '')))
        else:
            for index, node in enumerate(self.tab_item_list):
                data = self.tab_list[index]
                if enlist_from_uid:
                    node.btn_tab.SetText(get_text_by_id(data.get('text2', '')))
                else:
                    node.btn_tab.SetText(get_text_by_id(data.get('text', '')))

    def check_red_point(self):
        if global_data.player.check_is_newbie_on_start(self._activity_type):
            self.tab_item_list[0].temp_red.setVisible(check_binding_red_point(self._activity_type))
            self.tab_item_list[1].temp_red.setVisible(check_recruit_red_point(self._activity_type))

    def on_finalize_panel(self):
        self.process_event(False)
        self.tab_item_list = None
        self.tab_list = None
        if self._binding_widget:
            self._binding_widget.destroy()
            self._binding_widget = None
        if self._recruit_widget:
            self._recruit_widget.destroy()
            self._recruit_widget = None
        self._isAniming = None
        self._current_index = None
        return