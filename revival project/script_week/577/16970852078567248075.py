# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/LobbyItemObtainDescUI.py
from __future__ import absolute_import
import six_ex
import six
import copy
from common.uisys.basepanel import BasePanel
from cocosui import cc, ccui, ccs
import common.const.uiconst
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_name, get_lobby_item_desc, get_lobby_item_type_name_by_id
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import career_utils
from logic.gutils import template_utils
from logic.gutils.mall_utils import get_lottery_widgets_info, get_lottery_table_id_list, get_goods_item_open_date, check_limit_time_lottery_open_info, check_limit_time_lottery_visible_info
from logic.gutils import task_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from common.utils.cocos_utils import ccp
from logic.gutils import loop_lottery_utils
from logic.gcommon import time_utility as tutil
GET_WAY_TYPE_LOTTERY = 1
GET_WAY_TYPE_ACTIVITY = 2
GET_WAY_TYPE_ITEM = 3
VISIBLE_NOT_OPEN = 1
VISIBLE_OPEN = 2
VISIBLE_CLOSE = 3

class LobbyItemObtainDescUI(BasePanel):
    PANEL_CONFIG_NAME = 'role_profile/i_role_gift_obtain'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    BORDER_INDENT = 24
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'show_item_obtain_ui_event': '_show_item_obtain_info',
       'hide_item_obtain_ui_event': '_hide_item_obtain_info'
       }

    def on_init_panel(self, *args, **kwargs):
        self._jump_to_multi_ui_info = []
        self._timer = None
        self._time_down_list = set()
        self.hide()
        widgets_map, widgets_list = get_lottery_widgets_info()
        self.all_lottery_info = {}
        for one_lottery_info in widgets_list:
            self.all_lottery_info[one_lottery_info['lottery_id']] = one_lottery_info

        return

    def on_finalize_panel(self):
        self.unregister_timer()

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def second_callback(self):
        remove_elems = []
        for item_widget, one_jump_to_ui_info in six_ex.values(self._time_down_list):
            left_time = self.refresh_way_time_desc(item_widget, one_jump_to_ui_info)
            if left_time <= 0:
                remove_elems.append((item_widget, one_jump_to_ui_info))

        if remove_elems:
            for one_elem in remove_elems:
                if one_elem in self._time_down_list:
                    self._time_down_list.remove(one_elem)

    def _cb_create_item(self, index, item_widget):
        if not global_data.player:
            return
        one_jump_to_ui_info = self._jump_to_multi_ui_info[index]
        self.update_way_type_desc(item_widget, one_jump_to_ui_info)
        self.update_item_own_num_desc(item_widget, one_jump_to_ui_info)
        self.update_way_time_down_desc(item_widget, one_jump_to_ui_info)
        self.update_btn_go(item_widget, one_jump_to_ui_info)

    def jump_to_ui(self, one_jump_to_ui_info):
        ui_receive = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        if ui_receive and ui_receive.isPanelVisible() and ui_receive.is_showing():
            ui_receive.close()
        global_data.emgr.close_reward_preview_event.emit()
        item_utils.exec_jump_to_ui_info(one_jump_to_ui_info)

    def update_btn_go(self, item_widget, one_jump_to_ui_info):
        way_type = one_jump_to_ui_info['type']
        if way_type == GET_WAY_TYPE_LOTTERY or way_type == GET_WAY_TYPE_ACTIVITY:
            item_widget.btn_go.btn_common.SetText(get_text_by_id(80284))

            @item_widget.btn_go.btn_common.callback()
            def OnClick(btn, touch):
                global_data.emgr.hide_item_desc_ui_event.emit()
                self._hide_item_obtain_info()
                self.jump_to_ui(one_jump_to_ui_info)

        elif way_type == GET_WAY_TYPE_ITEM:
            item_no = int(one_jump_to_ui_info['id'])
            item_num = global_data.player.get_item_num_by_no(int(item_no))
            if item_num > 0:
                item_widget.btn_go.btn_common.SetText(18082)

                @item_widget.btn_go.btn_common.callback()
                def OnClick(btn, touch):
                    global_data.emgr.hide_item_desc_ui_event.emit()
                    self._hide_item_obtain_info()
                    usage = item_utils.get_lobby_item_usage(item_no)
                    item = global_data.player.get_item_by_no(int(item_no))
                    item_data = {'id': item.id,
                       'item_no': item.item_no,
                       'quantity': item.get_current_stack_num()
                       }
                    item_utils.try_use_lobby_item(item_data, usage)

            else:
                item_widget.btn_go.btn_common.SetText(80284)

                @item_widget.btn_go.btn_common.callback()
                def OnClick(btn, touch):
                    global_data.emgr.hide_item_desc_ui_event.emit()
                    self._hide_item_obtain_info()
                    self.jump_to_ui(one_jump_to_ui_info)

    def update_way_type_desc(self, item_widget, one_jump_to_ui_info):
        way_type = one_jump_to_ui_info['type']
        if way_type == GET_WAY_TYPE_LOTTERY:
            lottery_id = str(one_jump_to_ui_info['id'])
            lottery_info = self.all_lottery_info[lottery_id]
            item_widget.lab_obtain_way.SetString(lottery_info['text_id'])
        elif way_type == GET_WAY_TYPE_ACTIVITY:
            activity_type = str(one_jump_to_ui_info['id'])
            name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
            item_widget.lab_obtain_way.SetString(name_id)
        elif way_type == GET_WAY_TYPE_ITEM:
            item_no = int(one_jump_to_ui_info['id'])
            name = get_lobby_item_name(item_no)
            item_widget.lab_obtain_way.SetString(name)

    def update_item_own_num_desc(self, item_widget, one_jump_to_ui_info):
        way_type = one_jump_to_ui_info['type']
        if way_type != GET_WAY_TYPE_ITEM:
            item_widget.lab_num.setVisible(False)
        else:
            item_widget.lab_num.setVisible(True)
            item_no = int(one_jump_to_ui_info['id'])
            item_num = global_data.player.get_item_num_by_no(int(item_no))
            text = get_text_by_id(603018).format(item_num)
            item_widget.lab_num.SetString(text)
            if item_num > 0:
                item_widget.lab_num.SetColor(2566706)
            else:
                item_widget.lab_num.SetColor(16337521)

    def get_lottery_state_and_left_time(self, lottery_id):
        lottery_info = self.all_lottery_info[lottery_id]
        left_time = 0
        tab_state = VISIBLE_CLOSE
        if lottery_info.get('special_type', None):
            if lottery_info['special_type'] == 'limit_time':
                open_date_range = get_goods_item_open_date(lottery_info['single_goods_id'])
                opening, left_time = check_limit_time_lottery_open_info(open_date_range)
                visible_date_range = lottery_info.get('visible_ts', None)
                visible = opening
                if visible_date_range and not opening:
                    visible, left_time = check_limit_time_lottery_visible_info(visible_date_range, open_date_range)
                if visible or opening:
                    if opening:
                        tab_state = VISIBLE_OPEN
                    elif left_time > 0:
                        tab_state = VISIBLE_NOT_OPEN
                    else:
                        tab_state = VISIBLE_CLOSE
                        left_time = -left_time
            elif lottery_info['special_type'] == 'loop_lottery':
                goods_open_info, shop_open_info = loop_lottery_utils.get_loop_lottery_open_info(lottery_id)
                if goods_open_info or shop_open_info:
                    now = tutil.time()
                    if goods_open_info:
                        left_time = now - goods_open_info[2]
                    if shop_open_info and not goods_open_info:
                        left_time = now - shop_open_info[2]
                    if goods_open_info:
                        tab_state = VISIBLE_OPEN
                    else:
                        tab_state = VISIBLE_NOT_OPEN
        return (
         tab_state, left_time)

    def update_way_time_down_desc(self, item_widget, one_jump_to_ui_info):
        way_type = one_jump_to_ui_info['type']
        if way_type == GET_WAY_TYPE_LOTTERY:
            lottery_id = str(one_jump_to_ui_info['id'])
            tab_state, left_time = self.get_lottery_state_and_left_time(lottery_id)
            if tab_state != VISIBLE_CLOSE and left_time > 0:
                self.refresh_way_time_desc(item_widget, one_jump_to_ui_info)
                self._time_down_list.add((item_widget, one_jump_to_ui_info))
                item_widget.lab_last_time.setVisible(True)
            else:
                item_widget.lab_last_time.setVisible(False)
        elif way_type == GET_WAY_TYPE_ACTIVITY:
            activity_type = str(one_jump_to_ui_info['id'])
            task_id = confmgr.get('c_activity_config', activity_type, 'cTask', default='')
            left_time = task_utils.get_raw_left_open_time(task_id)
            if left_time > 0:
                self.refresh_way_time_desc(item_widget, one_jump_to_ui_info)
                self._time_down_list.add((item_widget, one_jump_to_ui_info))
                item_widget.lab_last_time.setVisible(True)
            else:
                item_widget.lab_last_time.setVisible(False)
        elif way_type == GET_WAY_TYPE_ITEM:
            item_widget.lab_last_time.setVisible(False)

    def refresh_way_time_desc(self, item_widget, one_jump_to_ui_info):
        way_type = one_jump_to_ui_info['type']
        left_time = 0
        if way_type == GET_WAY_TYPE_LOTTERY:
            lottery_id = str(one_jump_to_ui_info['id'])
            tab_state, left_time = self.get_lottery_state_and_left_time(lottery_id)
            if tab_state == VISIBLE_CLOSE:
                left_time = 0
        elif way_type == GET_WAY_TYPE_ACTIVITY:
            activity_type = str(one_jump_to_ui_info['id'])
            task_id = confmgr.get('c_activity_config', activity_type, 'cTask', default='')
            left_time = task_utils.get_raw_left_open_time(task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                item_widget.lab_last_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                item_widget.lab_last_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            item_widget.lab_last_time.lab_last_time(False)
        return left_time

    def _show_item_obtain_info(self, item_no, parent, jump_to_multi_ui_info):
        self._jump_to_multi_ui_info = jump_to_multi_ui_info

        @self.panel.list_obtain_way.unique_callback()
        def OnCreateItem(lv, index, item_widget):
            self._cb_create_item(index, item_widget)

        self.panel.list_obtain_way.SetInitCount(len(jump_to_multi_ui_info))
        all_items = self.panel.list_obtain_way.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self._cb_create_item(index, widget)

        self.show()
        wpos = parent.ConvertToWorldSpacePercentage(100, 0)
        self.panel.setAnchorPoint(ccp(0, 0))
        template_utils.set_node_position_in_screen(self.panel, self.panel.GetParent(), wpos)

    def _hide_item_obtain_info(self, *args):
        self.unregister_timer()
        self.hide()

    def ui_vkb_custom_func(self):
        self._hide_item_obtain_info()