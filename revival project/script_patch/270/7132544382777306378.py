# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryScratchListWidget.py
from __future__ import absolute_import
from six.moves import range
import copy
from logic.gcommon.common_const.activity_const import CARD_HEIGHT, CARD_WIDTH, MAX_SELECT_NUM, CARD_SUM
from .LotteryScratchItemWidget import LotteryScratchItemWidget
from logic.gutils.mall_utils import get_lobby_item_pic_by_item_no, get_lottery_preview_data
from logic.gutils.item_utils import get_item_rare_degree
DEGREE_TO_PNL = {1: 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/pnl_jojo_scrawl_0.png',
   2: 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/pnl_jojo_scrawl_1.png',
   3: 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/pnl_jojo_scrawl_2.png',
   4: 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/pnl_jojo_scrawl_3.png'
   }

class LotteryScratchListWidget(object):

    def __init__(self, panel, parent, on_change_show_reward, table_id, lottery_id, scratch_drag_end_callback, show_callback=None, hide_callback=None):
        self.panel = panel
        self.parent = parent
        self.table_id = table_id
        self.lottery_id = lottery_id
        self.scratch_drag_end_callback = scratch_drag_end_callback
        self.show_callback = show_callback
        self.hide_callback = hide_callback
        self.on_change_show_reward = on_change_show_reward
        self.event_processed = False
        self.init_parameters()
        self.on_init_panel()

    def on_init_panel(self):
        self.init_list_item()
        self.process_event(False)

    def init_parameters(self):
        self.card_sum = CARD_SUM
        self.is_drag = False
        self.select_num = 0
        self.select_item_list = []
        self.select_idx_list = []
        self.buy_idx_list = []
        self.open_dict = global_data.player.get_reward_intervene_count(self.table_id) if global_data.player else {}
        preview_data = get_lottery_preview_data(self.lottery_id)
        self.degree_list = preview_data.get('degree_list', [])
        self.core_item_list = preview_data.get('core_item_id_list', [])
        self.is_show_full_tips = False

    def process_event(self, flag):
        if self.event_processed == flag:
            return
        self.event_processed = flag
        emgr = global_data.emgr
        econf = {}
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_list_item(self):
        self.list_item = self.panel.pnl_content.list_item
        self.list_item.BindMethod('OnCreateItem', self.create_scratch_item)
        self.list_item.DeleteAllSubItem()
        self.list_item.SetInitCount(self.card_sum)
        self.list_item.scroll_Load()
        self.panel.pnl_content.nd_touch.BindMethod('OnBegin', self.on_touch_begin)
        self.panel.pnl_content.nd_touch.BindMethod('OnEnd', self.on_touch_end)
        self.panel.pnl_content.nd_touch.BindMethod('OnDrag', self.on_touch_drag)

    def on_touch_begin(self, layer, touch):
        self.is_drag = True
        pos = touch.getLocation()
        self.check_item_select(pos)

    def on_touch_drag(self, layer, touch):
        pos = touch.getLocation()
        self.check_item_select(pos)

    def on_touch_end(self, layer, touch):
        self.is_drag = False
        self.is_show_full_tips = False
        if self.select_num <= 0:
            return
        if not self.panel or not self.panel.isVisible():
            return
        if self.scratch_drag_end_callback:
            self.scratch_drag_end_callback(self.select_idx_list, self.on_cancel_confirm_widget, self.on_confirm_widget)

    def on_cancel_confirm_widget(self):
        self.reset_select_item()

    def on_confirm_widget(self):
        self.reset_select_item()

    def create_scratch_item(self, lv, idx, item):
        self.refresh_scratch_item(idx, item)

    def check_item_select(self, pos):
        for idx in range(self.card_sum):
            item = self.list_item.GetItem(idx)
            if not item:
                continue
            if item.btn_choose.IsPointIn(pos):
                self.on_item_enter(item, idx)

    def refresh_scratch_item(self, idx, item):
        info = self.open_dict.get(str(idx), None)
        if info:
            item_no, item_num, item_idx = info
            item_pic = get_lobby_item_pic_by_item_no(item_no)
            rare_degree = self.degree_list[int(item_idx)] if len(self.degree_list) >= int(item_idx) else 1
            item.img_frame.SetDisplayFrameByPath('', DEGREE_TO_PNL.get(rare_degree, 'ui_res_2/activity/activity_202211/jojo_scrawl/pnl_jojo_scrawl_0.png'))
            item.item.SetDisplayFrameByPath('', item_pic)
            if item_num > 1:
                item.lab_quantity.SetString(str(item_num))
                item.lab_quantity.setVisible(True)
            item.nd_get.setVisible(False)
            if str(idx) in self.buy_idx_list:
                item.nd_get_tips.setVisible(True)
            else:
                item.nd_get_tips.setVisible(False)
            item.btn_choose.SetSwallowTouch(True)
            item.btn_choose.SetEnableTouch(True)
            item.btn_choose.SetShowEnable(False)

            @item.btn_choose.unique_callback()
            def OnClick(btn, touch):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                return

        else:
            item.nd_get.setVisible(False)
            item.btn_choose.SetSwallowTouch(False)
            item.btn_choose.SetEnableTouch(False)
            item.btn_choose.SetShowEnable(True)
        return

    def on_item_enter(self, item, idx):
        if self.select_num >= MAX_SELECT_NUM:
            if not self.is_show_full_tips:
                global_data.game_mgr.show_tip(633891)
                self.is_show_full_tips = True
            return
        if item in self.select_item_list or self.open_dict.get(str(idx)):
            return
        item.btn_choose.SetSelect(True)
        if not self.is_drag:
            return
        self.select_item_list.append(item)
        self.select_idx_list.append(str(idx))
        self.select_num += 1

    def refresh_all_item(self):
        self.open_dict = global_data.player.get_reward_intervene_count(self.table_id) if global_data.player else {}
        for idx in range(self.card_sum):
            item = self.list_item.GetItem(idx)
            if item:
                self.refresh_scratch_item(idx, item)

        self.buy_idx_list = []

    def reset_select_item(self):
        for idx in range(self.select_num):
            self.select_item_list[idx].btn_choose.SetSelect(False)

        self.select_item_list = []
        self.select_idx_list = []
        self.select_num = 0

    def reset_buy_idx_list(self):
        for i in range(len(self.buy_idx_list)):
            idx = int(self.buy_idx_list[i])
            item = self.list_item.GetItem(idx)
            if item:
                item.nd_get_tips.setVisible(False)

    def set_buy_idx_list(self, buy_idx_list):
        self.buy_idx_list = copy.deepcopy(buy_idx_list)
        self.play_item_get_animation()

    def play_item_get_animation(self):
        self.open_dict = global_data.player.get_reward_intervene_count(self.table_id) if global_data.player else {}
        for i in range(len(self.buy_idx_list)):
            idx = int(self.buy_idx_list[i])
            item = self.list_item.GetItem(idx)
            if item:
                self.refresh_scratch_item(idx, item)
                open_info = self.open_dict.get(str(idx))
                if len(self.core_item_list) and open_info and self.core_item_list[0] == open_info[0]:
                    self.parent.PlayAnimation('jojo_show')
                    item.PlayAnimation('chosen_1')
                else:
                    item.PlayAnimation('chosen_2')

    def parent_show(self, goods_id=None):
        self.show()

    def show(self, goods_id=None):
        self.process_event(True)
        self.show_callback and self.show_callback()

    def parent_hide(self):
        self.hide()

    def hide(self):
        self.process_event(False)
        self.hide_callback and self.hide_callback()

    def destroy(self):
        self.process_event(False)