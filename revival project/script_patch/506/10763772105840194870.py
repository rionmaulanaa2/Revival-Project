# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNile/ActivityBingoLianliankanTaskPanelUI.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_raw_left_open_time
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info, get_lobby_item_type, get_lobby_item_reward_id
from common.cfg import confmgr
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
import cc
from logic.gcommon.time_utility import get_simply_time, get_time_string
from common.utils.timer import CLOCK
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item, get_reward_list_by_reward_id
from ..ActivityNewLianLianKan import ActivityNewLianLianKan
from logic.gcommon.item.lobby_item_type import L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GIFTPACKAGE, L_ITME_TYPE_GUNSKIN
import six_ex
from logic.gutils import task_utils
from logic.gutils import activity_utils
from logic.gutils import item_utils
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE

class ActivityBingoLianliankanTaskPanelUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202401/bingo_lianliankan/open_bingo_task'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    GLOBAL_EVENT = {'receive_task_reward_succ_event': 'receive_task_reward_succ'
       }

    def on_init_panel(self):
        self.task_id = None
        self.panel.setVisible(False)

        @self.panel.nd_touch.callback()
        def OnClick(btn, touch):
            self.panel.setVisible(False)

        return

    def receive_task_reward_succ(self, *args):
        self.update_task_id(self._activity_type, self.task_id)

    def init_buy_show(self, task_id):
        from logic.gcommon.const import SHOP_PAYMENT_ITEM
        from logic.gutils.template_utils import init_tempate_reward, init_price_template
        task_data = confmgr.get('task/task_data', str(task_id))
        cost_common_task_card = task_data.get('cost_common_task_card')
        if cost_common_task_card:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNGAIN:
                self.panel.temp_btn_2.btn_common.SetEnable(True)
                self.panel.temp_btn_2.btn_common.SetText('')
                self.panel.temp_price.setVisible(True)
                cost_item_no, cost_item_num = cost_common_task_card
                goodsPayment = '{}_{}'.format(SHOP_PAYMENT_ITEM, cost_item_no)
                price_info = {'goods_payment': goodsPayment,
                   'original_price': cost_item_num,
                   'real_price': cost_item_num
                   }
                from logic.client.const.mall_const import DARK_PRICE_COLOR, DEF_PRICE_COLOR
                init_price_template(price_info, self.panel.temp_price, color=DARK_PRICE_COLOR)

                @self.panel.temp_btn_2.btn_common.callback()
                def OnClick(btn, touch):
                    items = global_data.player.get_items_by_no(cost_item_no)
                    for item in items:
                        item_num = item.get_current_stack_num()
                        if item_num < cost_item_num:
                            continue
                        else:
                            global_data.player.use_item(item.get_id(), cost_item_num, {'task_id': str(task_id)})
                            break

            elif status != ITEM_UNGAIN:
                self.panel.temp_price.setVisible(False)
                self.panel.temp_btn_2.btn_common.SetText(634330)
                self.panel.temp_btn_2.btn_common.SetEnable(False)
                self.panel.temp_btn_2.btn_common.SetEnable(False)
        else:
            self.panel.temp_price.setVisible(False)
            self.panel.lab_tips.SetString(634285)
            self.panel.temp_btn_2.btn_common.SetText(634330)
            self.panel.temp_btn_2.btn_common.SetEnable(False)

    def update_task_id(self, _activity_type, task_id):
        self._activity_type = _activity_type
        self.task_id = task_id
        self.panel.lab_task.SetString(get_task_name(self.task_id))
        self.init_task_temp(task_id)
        self.init_buy_show(task_id)

    def set_position(self, parent_panel, wpos, anchor_point=None):
        from logic.gutils import template_utils
        if anchor_point:
            self.panel.setAnchorPoint(anchor_point)
        template_utils.set_node_position_in_screen(self.panel, parent_panel, wpos, BORDER_INDENT=24, right_cut=130)

    def hide_panel(self):
        self.panel.setVisible(False)

    def show_panel(self):
        self.panel.setVisible(True)

    def init_task_temp(self, task_id):
        reward_item_no = None
        if task_id:
            reward_list = task_utils.get_task_reward_list(task_id)
            reward_item_no, item_num = reward_list[0]
            from logic.gutils.template_utils import init_tempate_mall_i_simple_item
            init_tempate_mall_i_simple_item(self.panel.temp_item, reward_item_no, item_num)
        if task_id:
            status = global_data.player.get_task_reward_status(task_id)
        else:
            status = None
        if reward_item_no:
            total_times = task_utils.get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            progress_txt = ''.join(('', str('%s/%s' % (cur_times, total_times))))
            self.panel.lab_task.SetString(task_utils.get_task_name(task_id))
            self.panel.lab_prog.SetString(progress_txt)
            self.update_receive_btn(status, self.panel.temp_btn_1.btn_common)

            @self.panel.temp_btn_1.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id, _cur_prog=cur_times, _total_prog=total_times, _max_prog=total_times):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                if _cur_prog < _total_prog:
                    jump_conf = task_utils.get_jump_conf(_task_id)
                    item_utils.exec_jump_to_ui_info(jump_conf)
                else:
                    global_data.player.receive_task_reward(_task_id)
                    if _max_prog == _total_prog:
                        btn.SetText(80866)
                        btn.SetEnable(False)

        return

    def update_receive_btn(self, status, btn_receive):
        btn_receive.EnableCustomState(True)
        if status == ITEM_RECEIVED:
            btn_receive.SetText(906668)
            btn_receive.SetEnable(False)
        elif status == ITEM_UNGAIN:
            btn_receive.SetText(604031)
            btn_receive.SetEnable(True)
        elif status == ITEM_UNRECEIVED:
            btn_receive.SetText(80930)
            btn_receive.SetSelect(True)
            btn_receive.SetEnable(True)