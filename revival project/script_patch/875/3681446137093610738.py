# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/RewardListUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from common.const import uiconst
from logic.gutils.new_template_utils import init_top_tab_list
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.gutils import item_utils

class RewardListUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202206/weekend_login/open_activity_weekend_preview'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        super(RewardListUI, self).on_init_panel()
        self._reward_click_callback = None
        self._list_sview = InfiniteScrollWidget(self.panel.list_item, self.panel)
        self._list_sview.set_template_init_callback(self.init_preview_item)
        self._list_sview.enable_item_auto_pool(True)
        self._list_sview.refresh_showed_item()
        self._list_sview.update_scroll_view()
        return

    def set_reward_data(self, reward_data):
        self._list_sview.update_data_list(reward_data)
        self._list_sview.update_scroll_view()

    def set_reward_click_callback(self, cb):
        self._reward_click_callback = cb

    def on_finalize_panel(self):
        self._list_sview.destroy()
        self._list_sview = None
        return

    def init_preview_item(self, item_widget, item_info):
        from logic.gutils import mall_utils
        if item_info is None:
            item_widget.nd_content.setVisible(False)
            return
        else:
            if type(item_info) in (list, tuple) and len(item_info) == 2:
                item_no, item_num = item_info
            else:
                item_no = item_info
                item_num = 1
            item_widget.nd_content.setVisible(True)
            item_widget.choose.setVisible(False)
            item_widget.have.setVisible(mall_utils.item_has_owned_by_item_no(item_no))
            item_widget.item.SetDisplayFrameByPath('', mall_utils.get_lobby_item_pic_by_item_no(item_no))
            item_utils.check_skin_tag(item_widget.nd_kind, item_no, None, is_show_kind=False)
            item_name = item_utils.get_lobby_item_name(item_no)
            item_widget.lab_name.SetString(item_name)
            item_widget.lab_num.SetString('x%d' % item_num)

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, _item_no=item_no, _item_num=item_num):
                if self._reward_click_callback and callable(self._reward_click_callback):
                    self._reward_click_callback(_item_no, _item_num, btn)

            return

    def on_click_close_btn(self, btn, touch):
        self.close()