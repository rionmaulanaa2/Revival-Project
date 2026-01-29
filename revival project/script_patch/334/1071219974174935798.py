# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/SpringShoutFriendsRewardPreviewUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
import cc
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from logic.gutils.new_template_utils import init_top_tab_list
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.gutils import item_utils

class SpringShoutFriendsRewardPreviewUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202201/spring_shout_friends/open_acticity_preview'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        super(SpringShoutFriendsRewardPreviewUI, self).on_init_panel()
        data_list = []
        data_list.append({'text': get_text_by_id(610538)})
        data_list.append({'text': get_text_by_id(610539)})
        self._list_sview = InfiniteScrollWidget(self.panel.list_item, self.panel)
        self._list_sview.set_template_init_callback(self.init_preview_item)
        self._list_sview.enable_item_auto_pool(True)

        def click_cb(item, idx):
            print('idx', idx)
            items = self.get_preview_items(idx)
            self._list_sview.update_data_list(items)
            self._list_sview.refresh_showed_item()
            self._list_sview.update_scroll_view()

        init_top_tab_list(self.panel.list_btn, data_list, click_cb)
        self.panel.list_btn.GetItem(0).btn_tab.OnClick(None)
        return

    def on_finalize_panel(self):
        self._list_sview.destroy()
        self._list_sview = None
        return

    def init_preview_item(self, item_widget, item_no):
        from logic.gutils import mall_utils
        if item_no is None:
            item_widget.nd_content.setVisible(False)
            return
        else:
            item_widget.nd_content.setVisible(True)
            item_widget.choose.setVisible(False)
            item_widget.have.setVisible(mall_utils.item_has_owned_by_item_no(item_no))
            item_widget.item.SetDisplayFrameByPath('', mall_utils.get_lobby_item_pic_by_item_no(item_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_belong_name(item_no))
            item_utils.check_skin_tag(item_widget.nd_kind, item_no, None, is_show_kind=True)
            item_name = item_utils.get_lobby_item_name(item_no)
            item_widget.lab_name_skin.SetString(item_name)
            return

    def on_click_close_btn(self, btn, touch):
        self.close()

    def get_preview_items(self, idx):
        good_rewards = [
         201001148,
         201001241,
         201001441,
         201001341,
         208100222,
         208100121,
         208200326,
         208106123,
         208102321,
         208105422]
        normal_rewards = [
         201800336,
         201801632,
         208200121,
         208200227,
         208100115,
         208100211,
         208102111,
         208103113,
         208106112,
         208106512,
         208200321,
         208102311,
         208105612,
         208100113,
         208200112,
         208100118,
         208100214,
         208105615]
        if idx == 0:
            return normal_rewards
        else:
            return good_rewards