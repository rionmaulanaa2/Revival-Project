# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyRemoveList.py
from __future__ import absolute_import
import six
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.const import INTIMACY_MSG_TYPE_DELETE_RECV, INTIMACY_NAME_MAP, IDX_INTIMACY_TYPE
from common.const.property_const import *
from logic.gutils.intimacy_utils import init_intimacy_request_item
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI

class IntimacyRemoveList(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/intimacy_remove_list'
    TEMPLATE_NODE_NAME = 'temp_window'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {'message_refresh_intimacy_msg': 'init_apply_list'
       }

    def on_init_panel(self, *args, **kwargs):
        super(IntimacyRemoveList, self).on_init_panel(*args, **kwargs)
        self.init_apply_list()

    def init_apply_list(self, *args):
        msg_dict = global_data.player.intimacy_msg_data.get(INTIMACY_MSG_TYPE_DELETE_RECV, {})
        if len(msg_dict) == 0:
            self.panel.nd_content.setVisible(False)
            self.panel.nd_empty.setVisible(True)
            return
        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.nd_content.setVisible(True)
            list_apply = self.panel.nd_content.list_apply
            list_apply.RecycleAllItem()
            friend_dict = global_data.message_data.get_friends()
            intimacy_data = global_data.player.intimacy_data
            for uid, msg_data in six.iteritems(msg_dict):
                intimacy_info = intimacy_data.get(str(uid), None)
                if intimacy_info is None:
                    continue
                intimacy_type = intimacy_info[IDX_INTIMACY_TYPE]
                try:
                    uid = int(uid)
                except ValueError:
                    continue

                friend_info = friend_dict.get(uid, None)
                if not friend_info:
                    continue
                item = list_apply.AddTemplateItem()

                def accept():
                    NormalConfirmUI(None, 3227, 3214, True, lambda : global_data.player.delete_intimacy_agree(uid, msg_data['intimacy_type']))
                    return

                def delete_refuse():
                    global_data.player.delete_relation_refuse(uid, msg_data['intimacy_type'])
                    global_data.game_mgr.show_tip(get_text_by_id(3280, {'name': friend_info[C_NAME]}))

                def refuse():
                    NormalConfirmUI(None, get_text_by_id(3276, {'name': friend_info[C_NAME]}), 3214, True, delete_refuse)
                    return

                init_intimacy_request_item(item, uid, friend_info, intimacy_info, accept, refuse, {'m_type': INTIMACY_MSG_TYPE_DELETE_RECV})

            return