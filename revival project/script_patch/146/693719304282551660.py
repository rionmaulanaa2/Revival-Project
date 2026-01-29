# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanBadgeSetUI.py
from __future__ import absolute_import
from six.moves import zip
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gutils.template_utils import update_badge_show
from logic.gcommon.common_const.clan_const import unpack_badge, get_default_badge
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
PATH_FORMAT = 'gui/ui_res_2/crew_logo/crew_%d_%04d.png'

class ClanBadgeSetUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'crew/crew_logo_set'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_confirm.btn_common_big.OnClick': 'on_confirm'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': 'close'
       }

    def on_init_panel(self, sel_cb=None, init_badge=get_default_badge()):
        super(ClanBadgeSetUI, self).on_init_panel()
        self._sel_cb = sel_cb
        self._badge = init_badge
        self._init_data()
        self._init_lst()

    def _init_data(self):
        floor, frame, pattern = unpack_badge(self._badge)
        self._sel_info = [
         pattern, frame, floor]
        update_badge_show(pattern, frame, floor, self.panel.temp_crew_logo)
        self._sel_items = [
         None, None, None]
        self._badge_nodes = [self.panel.list_icon, self.panel.list_frame, self.panel.list_bar]
        from common.cfg import confmgr
        self._badge_conf = confmgr.get('clan_badge_conf', default={})
        floor_lst = self._badge_conf.get('floor', [])
        frame_lst = self._badge_conf.get('frame', [])
        pattern_lst = self._badge_conf.get('pattern', [])
        self._lst_infos = [pattern_lst, frame_lst, floor_lst]
        return

    def _init_lst(self):

        def on_create_cb(view_list, idx, ui_item):
            self._init_lst_item(view_list, ui_item, idx)

        for node, lst_info in zip(self._badge_nodes, self._lst_infos):

            def OnScrollingCallback(scroll_node=node):
                scroll_node._testScrollAndLoad()

            node.BindMethod('OnCreateItem', on_create_cb)
            node.OnScrolling = OnScrollingCallback
            node.SetVisibleRange(6, 6)
            node.SetInitCount(0)
            node.SetInitCount(len(lst_info))
            node._refreshItemPos()

    def _init_lst_item(self, lst, ui_item, idx):
        lst_idx = self._badge_nodes.index(lst)
        ui_item.data = (lst_idx, idx)
        path = PATH_FORMAT % (lst_idx + 1, idx + 1)
        ui_item.item.SetDisplayFrameByPath('', path)
        if self._sel_info[lst_idx] == idx + 1:
            self._select_item(ui_item)

        @ui_item.unique_callback()
        def OnClick(item, touch):
            self._select_item(item)
            pattern_id, frame_id, floor_id = self._sel_info
            update_badge_show(pattern_id, frame_id, floor_id, self.panel.temp_crew_logo)

    def _select_item(self, ui_item):
        lst_idx, idx = ui_item.data
        last_sel_item = self._sel_items[lst_idx]
        if last_sel_item and last_sel_item.isValid():
            last_sel_item.img_choose.setVisible(False)
        ui_item.img_choose.setVisible(True)
        self._sel_items[lst_idx] = ui_item
        self._sel_info[lst_idx] = idx + 1

    def on_confirm(self, *args):
        pattern_id, frame_id, floor_id = self._sel_info
        if self._sel_cb:
            self._sel_cb(pattern_id, frame_id, floor_id)
        self.close()

    def on_finalize_panel(self):
        self._sel_cb = None
        return