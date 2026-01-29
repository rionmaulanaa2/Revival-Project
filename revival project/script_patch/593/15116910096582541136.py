# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/OpenIntimacyRequestUI.py
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils.intimacy_utils import init_intimacy_request_frame, init_intimacy_pic, OPERATION_FAIL_TEXT
from logic.gcommon.const import INTIMACY_NAME_MAP, IDX_INTIMACY_TYPE, IDX_INTIMACY_NAME, INTIMACY_COLOR_MAP, INTIMACY_MSG_TYPE_OPERATION_FAIL, INTIMACY_MSG_TYPE_BUILD_AGREE, INTIMACY_INTRODUCE_MAP
from logic.gutils.role_head_utils import PlayerInfoManager
from common.const.property_const import C_NAME
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI
from logic.gcommon.common_utils.text_utils import get_color_str
import copy

class OpenIntimacyRequestUI(BasePanel):
    PANEL_CONFIG_NAME = 'friend/open_intimacy_request'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'pnl_bg.btn_close.OnClick': 'on_click_close_ui'
       }

    def on_click_close_ui(self, *args):
        self.try_close()

    def try_close(self):
        next_data = self._intimacy_mgr.peek_next_request_msg()
        if next_data is None:
            self.close()
        else:
            self._update_data()
        return

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self._update_data()

    def init_parameters(self):
        self._uid = None
        self._intimacy_type = None
        self._friend_list = global_data.message_data.get_friends()
        self._friend_info = None
        self._intimacy_mgr = global_data.intimacy_mgr
        self.process_event(True)
        return

    def process_event(self, is_bind):
        econf = {'message_refresh_intimacy_msg': self.show_msg
           }
        if is_bind:
            global_data.emgr.bind_events(econf)
        else:
            global_data.emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self._uid = None
        self._intimacy_type = None
        self._friend_list = None
        self._friend_info = None
        self._intimacy_mgr = None
        self.process_event(False)
        return

    def _update_data(self):
        data = self._intimacy_mgr.pop_next_request_msg()
        self._uid = int(data[0])
        self._intimacy_type = data[1]
        self._friend_info = copy.deepcopy(self._friend_list.get(self._uid))
        if not self._friend_info:
            self.try_close()
            return
        self._update_panel()

    def _update_panel(self):
        pnl_bg = self.panel.pnl_bg
        intimacy_type = self._intimacy_type
        friend_info = self._friend_info
        player_info_manager = PlayerInfoManager()
        temp_head = pnl_bg.temp_head
        update_head_info = global_data.message_data.get_role_head_info(self._uid)
        frame = update_head_info.get('head_frame', None)
        photo = update_head_info.get('head_photo', None)
        if frame and photo:
            friend_info['head_frame'] = frame
            friend_info['head_photo'] = photo
        player_info_manager.add_head_item_auto(temp_head, self._uid, 0, friend_info)
        friend_name = str(friend_info[C_NAME])
        temp_head.lab_playername.SetString(friend_name)
        init_intimacy_request_frame(pnl_bg.frame_relationship, intimacy_type)
        init_intimacy_pic(pnl_bg.icon_relationship, intimacy_type)
        intimacy_name = get_text_by_id(INTIMACY_NAME_MAP[intimacy_type])
        color = INTIMACY_COLOR_MAP[intimacy_type]
        color_str = get_color_str(color, str(intimacy_name))
        pnl_bg.lab_relationship.SetString(color_str)
        pnl_bg.lab_introduce.SetString(get_text_by_id(INTIMACY_INTRODUCE_MAP[intimacy_type]))

        def agree_confirm_cb():
            global_data.player.build_relation_agree(self._uid, intimacy_type)

        def agree(btn, touch):
            NormalConfirmUI(None, get_text_by_id(3274, {'name': friend_info[C_NAME],'n': get_text_by_id(INTIMACY_NAME_MAP[intimacy_type])}), 3214, True, agree_confirm_cb)
            return

        pnl_bg.temp_btn_1.btn_common_big.BindMethod('OnClick', agree)

        def refuse_confirm_cb():
            global_data.player.build_relation_refuse(self._uid, intimacy_type)
            self.try_close()

        def refuse(btn, touch):
            NormalConfirmUI(None, get_text_by_id(3275, {'name': friend_info[C_NAME]}), 3214, True, refuse_confirm_cb)
            return

        pnl_bg.temp_btn_2.btn_common_big.BindMethod('OnClick', refuse)
        return

    def msg_finished_callback(self):
        self.showing_msg = False
        msg_data = global_data.player.intimacy_msg_data
        op_fail_msg = msg_data.get(INTIMACY_MSG_TYPE_OPERATION_FAIL, {})
        build_success_msg = msg_data.get(INTIMACY_MSG_TYPE_BUILD_AGREE, {})
        if len(op_fail_msg) == 0 and len(build_success_msg) == 0:
            global_data.emgr.message_refresh_intimacy_msg.emit()
            self.try_close()
        else:
            self.show_msg()

    def show_msg(self):
        friend_info = self._friend_info
        if not friend_info:
            return
        else:
            if not self.panel or not self.panel.isValid() or not self.panel.IsVisible():
                return
            if getattr(self, 'showing_msg', False):
                return
            self.showing_msg = True
            msg_data = global_data.player.intimacy_msg_data
            op_fail_msg = msg_data.get(INTIMACY_MSG_TYPE_OPERATION_FAIL, {})
            key_to_pop = []
            for uid in six.iterkeys(op_fail_msg):
                key_to_pop.append(uid)
                ret_code = op_fail_msg[uid].get('ret_code', None)
                if ret_code in OPERATION_FAIL_TEXT:
                    for key in key_to_pop:
                        op_fail_msg.pop(key)

                    text_id = OPERATION_FAIL_TEXT[ret_code]
                    self.panel.SetTimeOut(0.1, lambda : NormalConfirmUI(None, text_id, 3214, cancel_cb=self.msg_finished_callback))
                    return

            key_to_pop = []
            build_success_msg = msg_data.get(INTIMACY_MSG_TYPE_BUILD_AGREE, {})
            for uid in six.iterkeys(build_success_msg):
                key_to_pop.append(uid)
                intimacy_type = build_success_msg[uid].get('intimacy_type', None)
                if intimacy_type not in INTIMACY_NAME_MAP:
                    continue
                for key in key_to_pop:
                    build_success_msg.pop(key)

                text_id = get_text_by_id(3281, {'name': friend_info.get(C_NAME, get_text_by_id(10259)),'n': get_text_by_id(INTIMACY_NAME_MAP[intimacy_type])})
                self.panel.SetTimeOut(0.1, lambda : NormalConfirmUI(None, text_id, 3214, cancel_cb=self.msg_finished_callback))
                return

            self.showing_msg = False
            return