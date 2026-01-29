# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMechaSevenDayLogin.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.comsys.activity.widget import widget
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.item.item_const import ITEM_RECEIVED
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gutils.client_utils import post_method

@widget('AsyncTaskListWidget', 'DescribeWidget')
class ActivityMechaSevenDayLogin(ActivityBase):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ActivityMechaSevenDayLogin, self).on_finalize_panel()

    def on_init_panel(self):
        super(ActivityMechaSevenDayLogin, self).on_init_panel()
        self.process_event(True)
        self.panel.btn_see.setVisible(False)
        self._on_update_reward()

    def refresh_panel(self):
        super(ActivityMechaSevenDayLogin, self).refresh_panel()
        self._on_update_reward()

    @post_method
    def _on_update_reward(self, *args):
        if not global_data.player or not self.panel:
            return
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        if 'coupon_task_ids' in conf:
            coupon_9_task_id, coupon_8_task_id, coupon_7_task_id = conf['coupon_task_ids']
            coupon_dict = {coupon_9_task_id: [
                                610209, task_utils.get_task_reward_list(coupon_9_task_id)[0][0]],
               coupon_8_task_id: [
                                610208, task_utils.get_task_reward_list(coupon_8_task_id)[0][0]],
               coupon_7_task_id: [
                                610207, task_utils.get_task_reward_list(coupon_7_task_id)[0][0]]
               }
            max_discount_task = coupon_7_task_id
        else:
            coupon_dict = conf.get('coupon_dict', {})
            max_discount_task = conf.get('max_discount_task', 1410634)
        for task_id in sorted(six_ex.keys(coupon_dict), reverse=True):
            if ITEM_RECEIVED == global_data.player.get_task_reward_status(task_id):
                self.panel.lab_discount.SetString(coupon_dict[task_id][0])
                self.panel.lab_discount.setVisible(True)
                self.panel.lab_get_coupon.setVisible(False)
                show_item_id = coupon_dict[task_id][1]
                break
        else:
            self.panel.lab_get_coupon.SetString(610101)
            self.panel.lab_discount.setVisible(False)
            self.panel.lab_get_coupon.setVisible(True)
            show_item_id = coupon_dict.get(max_discount_task, [610207, 50101173])[1]

        if show_item_id == coupon_dict.get(max_discount_task, [610207, 50101173])[1] and ITEM_RECEIVED == global_data.player.get_task_reward_status(max_discount_task):
            self.panel.btn_coupon.SetShowEnable(False)
        self.panel.btn_coupon.EnableCustomState(True)

        @self.panel.btn_coupon.unique_callback()
        def OnClick(btn, touch):
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            w_pos = btn.ConvertToWorldSpace(x, y)
            extra_info = {'show_jump': True}
            global_data.emgr.show_item_desc_ui_event.emit(show_item_id, None, w_pos, extra_info=extra_info)
            return