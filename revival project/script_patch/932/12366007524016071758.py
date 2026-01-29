# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPinganjing/ActivityH5InviteBindingWidget.py
import game3d
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import rank_const
from common.cfg import confmgr
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.const import PLAYER_INFO_DETAIL
from logic.gutils.role_head_utils import set_role_head_photo
from logic.gutils.activity_utils import get_activity_conf_ui_data
from logic.gutils.template_utils import init_tempate_reward
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon import time_utility as tutil
PROG_ICON_PATH = 'gui/ui_res_2/activity/activity_202307/h5_recruitment/icon_h5_recruitment_arrow_{}.png'

class ActivityH5InviteBindingWidget(object):

    def __init__(self, panel, activity_type):
        self.panel = panel
        self._activity_type = str(activity_type)
        self.init_parameters()
        self.init_ui()
        self.init_ui_event()
        self.init_event()

    def destroy(self):
        self._item_list = None
        global_data.emgr.message_on_player_detail_inf -= self.update_binding_widget
        global_data.emgr.message_on_newbie_enlist_verify -= self.update_view
        global_data.emgr.message_on_update_newbie_enlist_newbie_score -= self.update_top_widget
        global_data.emgr.message_on_receive_newbie_enlist_bind_reward -= self.update_top_widget
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
        self.init_top_widget()
        self.update_view()

    def init_ui_event(self):

        @self.panel.btn_paste.unique_callback()
        def OnClick(btn, touch):
            self._on_paste_click()

        @self.panel.temp_btn_1.btn_common.unique_callback()
        def OnClick(btn, touch):
            self._on_bind_click()

    def _on_paste_click(self):
        from logic.gutils import deeplink_utils
        text = ''
        if G_IS_NA_USER:
            player_id = deeplink_utils.get_deep_link_param(deeplink_utils.DEEP_LINK_ADD_FRIEND)
            if player_id:
                try:
                    group = player_id.split('_')
                    text = group[0]
                except Exception as e:
                    print 'player_id error'

        else:
            text = game3d.get_clipboard_text()
            text = text if text else deeplink_utils.TEMP_CLIPBOARD_TEXT
        if not text:
            return
        self._input_box.set_text(text)

    def _on_bind_click(self):
        code = self._input_box.get_text()
        if not code:
            global_data.game_mgr.show_tip(get_text_by_id(634831))
            return
        try:
            int(code, 16)
        except Exception as e:
            print 'input_callback error, input is not hex'
            global_data.game_mgr.show_tip(get_text_by_id(634831))
            return

        def confirm_callback():
            global_data.player.try_newbie_enlist_from_code(self._activity_type, code)

        SecondConfirmDlg2().confirm(content=get_text_by_id(634832), confirm_callback=confirm_callback)

    def init_event(self):
        global_data.emgr.message_on_player_detail_inf += self.update_binding_widget
        global_data.emgr.message_on_newbie_enlist_verify += self.update_view
        global_data.emgr.message_on_update_newbie_enlist_newbie_score += self.update_top_widget
        global_data.emgr.message_on_receive_newbie_enlist_bind_reward += self.update_top_widget

    def init_top_widget(self):
        self._item_list = {}
        enlist_bind_gift = get_activity_conf_ui_data(self._activity_type, 'enlist_bind_gift')
        list_item = self.panel.list_item
        list_item.DeleteAllSubItem()
        for gift_info in enlist_bind_gift:
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
                current_score = global_data.player.get_binding_newbie_enlist_score(self._activity_type)
                if not global_data.player.check_binding_reward_has_receive(self._activity_type, score) and current_score >= score:
                    global_data.player.receive_newbie_enlist_bind_reward(self._activity_type, score)
                else:
                    x, y = btn.GetPosition()
                    w, _ = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                return

    def update_view(self):
        self.update_binding_widget()
        self.update_top_widget()

    def update_binding_widget(self, *args):
        enlist_from_uid = global_data.player.get_newbie_enlist_from_uid(self._activity_type)
        if enlist_from_uid:
            self.panel.nd_share.setVisible(True)
            self.panel.nd_invitation.setVisible(False)
            self.panel.temp_btn_1.setVisible(False)
            player_info = global_data.message_data.get_player_detail_inf(enlist_from_uid)
            if not player_info:
                player_info = {}
            temp_head = self.panel.temp_head
            set_role_head_photo(temp_head, player_info.get('head_photo', None))
            temp_head.lab_name.SetString(player_info.get('char_name', ''))
            temp_head2 = self.panel.temp_head2
            set_role_head_photo(temp_head2, global_data.player.get_head_photo())
            temp_head2.lab_name.SetString(global_data.player.get_name())
        else:
            self.panel.nd_share.setVisible(False)
            self.panel.nd_invitation.setVisible(True)
            self.panel.temp_btn_1.setVisible(True)
            self._input_box = InputBox.InputBox(self.panel.temp_input, max_length=12, placeholder='')
            self._input_box.set_rise_widget(self.panel)
        return

    def update_top_widget(self):
        current_score = global_data.player.get_binding_newbie_enlist_score(self._activity_type)
        self.panel.lab_points.SetString(str(current_score))
        for score, item in self._item_list.items():
            score = int(score)
            max_score = score
            if global_data.player.check_binding_reward_has_receive(self._activity_type, score):
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