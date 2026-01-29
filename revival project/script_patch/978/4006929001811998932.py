# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWinterCupReward.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import jump_to_ui_utils
from logic.client.const import mall_const
from logic.gutils import mall_utils
import logic.gcommon.const as gconst
from logic.gutils import template_utils

class ActivityWinterCupReward(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWinterCupReward, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_mall_info()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        task_list = activity_utils.parse_task_list(conf['cTask'])
        self._task_id = task_list[0] if task_list else None
        return

    def init_mall_info(self):
        self._on_player_info_update()
        btn = self.panel.temp_btn_go.btn_major

        @btn.callback()
        def OnClick(_layer, _touch):
            jump_to_ui_utils.jump_to_mall(None, (mall_const.COMPETITION_ID, None))
            return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_btn,
           'receive_task_reward_succ_event': self.refresh_btn,
           'player_money_info_update_event': self._on_player_info_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_player_info_update(self):
        if global_data.ui_mgr.get_ui('ScreenLockerUI'):
            return
        else:
            money_types = mall_utils.get_mall_money_types(mall_const.COMPETITION_ID, None)
            if not global_data.player:
                return
            list_money = self.panel.list_money
            list_money.SetInitCount(len(money_types))
            for i, m_type in enumerate(money_types):
                money_node = list_money.GetItem(i)
                money = mall_utils.get_my_money(m_type)
                item_no = mall_utils.get_payment_item_no(m_type)
                money_node.btn_add.setVisible(False)
                template_utils.init_common_price(money_node, money, m_type)

                @money_node.unique_callback()
                def OnClick(btn, touch, item_no=item_no):
                    wpos = touch.getLocation()
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=wpos)
                    return

            list_money._refreshItemPos(is_cal_scale=True)
            return

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        self.refresh_btn()

    def refresh_btn(self, *args):
        if not self._task_id:
            return
        btn = self.panel.temp_btn.btn_major
        btn.SetEnable(True)
        reward_status = global_data.player.get_task_reward_status(self._task_id)
        if reward_status == ITEM_UNRECEIVED:
            btn.SetText(604030)

            @btn.callback()
            def OnClick(*args):
                global_data.player.receive_task_reward(self._task_id)

        elif reward_status == ITEM_RECEIVED:
            btn.SetText(604029)
            btn.SetEnable(False)

            @btn.callback()
            def OnClick(*args):
                pass

        global_data.emgr.refresh_activity_redpoint.emit()