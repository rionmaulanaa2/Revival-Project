# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDebrisFusionUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_lobby_utils import init_story_debris_item
from logic.gcommon.common_utils.text_utils import get_color_str
from common.cfg import confmgr
CAN_FUSION_COLOR = '0xFEFFFFFF'
CANT_FUSION_COLOR = '0xF42551FF'

class PVEDebrisFusionUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/fragments/open_pve_fragments_fusion'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_content.pnl_content.btn_close.OnClick': '_on_click_back'
       }

    def on_init_panel(self, chapter_id=1, *args, **kwargs):
        super(PVEDebrisFusionUI, self).on_init_panel()
        self.init_params(chapter_id)
        self.init_panel()
        self.process_events(True)
        self.init_ui_events()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_debris_merge': self._on_pve_debris_merge
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self, chapter_id):
        self._chapter_id = chapter_id
        self._debris_list = []
        self._cur_select_count = 0
        self._cur_select_dict = {}
        self._merge_cost = confmgr.get('story_debris_chapter_data', str(self._chapter_id), 'debris_merge_cost', default=10)
        self._is_check_sview = False
        self._cur_show_index = -1
        story_debris_chapter_data = confmgr.get('story_debris_chapter_data', str(self._chapter_id), default={})
        clue_list = story_debris_chapter_data.get('clue')
        story_debris_clue_data = confmgr.get('story_debris_clue_data', default={})
        self._debris_id_list = []
        for clue_id in clue_list:
            clue_data = story_debris_clue_data.get(str(clue_id), {})
            debris_id_list = clue_data.get('debris', [])
            self._debris_id_list.extend(debris_id_list)

    def init_panel(self):
        self._list_item = self.panel.list_item
        self._init_desc()
        self._update_view()

    def init_ui_events(self):

        @self.panel.btn_fusion.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            if self._cur_select_count == self._merge_cost:
                global_data.player.merge_story_debris(self._cur_select_dict, self._chapter_id)

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(1400037, 1400038)

        @self._list_item.unique_callback()
        def OnScrolling(sender):
            if self._is_check_sview is False:
                self._is_check_sview = True
                self._list_item.SetTimeOut(0.02, self.check_sview)

    def _on_click_back(self, *args):
        self.close()

    def _init_desc(self):
        self.panel.lab_tips.setString(get_text_by_id(1400007).format(self._merge_cost))

    def _update_view(self):
        self._update_list_item()
        self._update_lab_got()

    def _update_list_item(self):
        self._debris_list = []
        self._cur_select_count = 0
        self._cur_select_dict = {}
        for item_no in self._debris_id_list:
            item_no = int(item_no)
            item_num = global_data.player.get_item_num_by_no(item_no) if global_data.player else 0
            if item_num > 1:
                for _ in range(item_num - 1):
                    self._debris_list.append(item_no)
                    if self._cur_select_count < self._merge_cost:
                        self._cur_select_count += 1
                        if not self._cur_select_dict.get(item_no):
                            self._cur_select_dict[item_no] = 0
                        self._cur_select_dict[item_no] += 1

        self.refresh_debris()

    def refresh_debris(self):
        self._list_item.DeleteAllSubItem()
        show_data = self.get_show_data()
        data_count = len(show_data)
        sview_height = self._list_item.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 100:
            if data_count - index <= 0:
                break
            data = show_data[index]
            debris_item = self.add_list_item(data, True, index)
            if index % 5 == 0:
                all_height += debris_item.getContentSize().height
            index += 1

        self._list_item.ScrollToTop()
        self._list_item._container._refreshItemPos()
        self._list_item._refreshItemPos()
        self._cur_show_index = index - 1

    def check_sview(self):
        show_data = self.get_show_data()
        self._cur_show_index = self._list_item.AutoAddAndRemoveItem_MulCol(self._cur_show_index, show_data, len(show_data), self.add_list_item, 400, 500)
        self._is_check_sview = False

    def get_show_data(self):
        return self._debris_list

    def add_list_item(self, item_no, is_back_item, index=-1):
        if is_back_item:
            debris_item = self._list_item.AddTemplateItem(bRefresh=True)
        else:
            debris_item = self._list_item.AddTemplateItem(0, bRefresh=True)
        btn_item = debris_item.btn_item
        btn_item.EnableCustomState(True)
        item_num = 1
        init_story_debris_item(debris_item, item_no, item_num, False)
        if index < self._merge_cost:
            btn_item.SetSelect(True)

        @btn_item.callback()
        def OnClick(btn, touch):
            if not self._cur_select_dict.get(item_no):
                return
            if btn.GetSelect():
                self._cur_select_dict[item_no] -= 1
                if self._cur_select_dict[item_no] == 0:
                    self._cur_select_dict.pop(item_no)
                self._cur_select_count -= 1
                btn.SetSelect(False)
            else:
                if self._cur_select_count == self._merge_cost:
                    return
                if not self._cur_select_dict.get(item_no):
                    self._cur_select_dict[item_no] = 0
                self._cur_select_dict[item_no] += 1
                self._cur_select_count += 1
                btn.SetSelect(True)
            self._update_lab_got()

        return debris_item

    def _update_lab_got(self):
        can_fusion = self._cur_select_count == self._merge_cost
        debris_color = CAN_FUSION_COLOR if can_fusion else CANT_FUSION_COLOR
        debris_color_str = get_color_str(debris_color, self._cur_select_count)
        self.panel.lab_got.setString(get_text_by_id(1400008).format(debris_color_str, self._merge_cost))
        self.panel.btn_fusion.SetEnable(can_fusion)

    def _on_pve_debris_merge(self, *args):
        self._update_view()
        if self._cur_select_count < self._merge_cost:
            self.close()

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVEDebrisFusionUI, self).on_finalize_panel()