# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyPhoneBindingWidget.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from common.const import uiconst
from logic.gutils.template_utils import init_tempate_mall_i_item
import json
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
VERIFY = 1
UPDATE = 2
STATUS = 3
FORCEUPDATE = 4
LOGINUPDATE = 5

class LobbyPhoneBindingWidget(object):

    def __init__(self, parent_ui, panel):
        self.panel = panel
        super(LobbyPhoneBindingWidget, self).__init__()
        self._has_bind = False
        if LobbyPhoneBindingWidget.check_shown():
            self.panel.btn_phone.setVisible(True)
            self.process_event(True)
        else:
            self.panel.btn_phone.setVisible(False)

    def process_event(self, is_bind):
        if self._has_bind == is_bind:
            return
        self._has_bind = is_bind
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_btn_phone_visible
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    @staticmethod
    def on_click_bind_mobile(*args):
        from logic.gcommon.common_const.activity_const import ACTIVITY_COMMUNITY_WELFARE
        from logic.gutils.jump_to_ui_utils import jump_to_activity
        jump_to_activity(ACTIVITY_COMMUNITY_WELFARE)

    def update_btn_phone_visible(self, *args):
        vis = LobbyPhoneBindingWidget.check_shown()
        self.panel.btn_phone.setVisible(vis)
        self.process_event(vis)

    @staticmethod
    def check_shown(*args):
        from logic.gutils import task_utils
        from logic.gcommon.common_const.activity_const import ACTIVITY_COMMUNITY_WELFARE
        from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
        global_data.player.read_activity_list(ACTIVITY_COMMUNITY_WELFARE)
        if global_data.channel.get_name() == 'netease':
            if global_data.player.has_activity(ACTIVITY_COMMUNITY_WELFARE):
                task_id = confmgr.get('c_activity_config', ACTIVITY_COMMUNITY_WELFARE, 'cTask', default='')
                children_task_id_list = task_utils.get_children_task(task_id)
                task_id = children_task_id_list[0]
                reward_status = global_data.player.get_task_reward_status(task_id)
                if reward_status != ITEM_RECEIVED:
                    return True
        return False

    def destroy(self):
        self.process_event(False)
        self.panel = None
        return