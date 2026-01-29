# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDebrisDecomposeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_lobby_utils import init_story_debris_item
from logic.gcommon.common_utils.text_utils import get_color_str
from logic.gcommon.common_const.pve_const import PVE_STORY_DECOMPOSE_COUNT
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
from common.cfg import confmgr

class PVEDebrisDecomposeUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/fragments/open_pve_fragments_recycle'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_content.pnl_content.btn_close.OnClick': 'close'
       }

    def on_init_panel(self, chapter_id=1, *args, **kwargs):
        super(PVEDebrisDecomposeUI, self).on_init_panel()
        self.init_params(chapter_id)
        self.init_panel()
        self.process_events(True)
        self.init_ui_events()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_debris_decompose': self.on_pve_debris_decompose
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self, chapter_id):
        self._chapter_id = chapter_id
        self._debris_list = []
        self._cur_select_count = 0
        self._cur_select_item_dict = {}
        self._cur_select_index_list = []
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
        self._update_view()

    def init_ui_events(self):

        @self.panel.btn_recycle.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            if self._cur_select_count > 0:
                global_data.player.decompose_story_debris(self._cur_select_item_dict, self._chapter_id)

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(1400073, 1400076)

        @self._list_item.unique_callback()
        def OnScrolling(sender):
            if self._is_check_sview is False:
                self._is_check_sview = True
                self._list_item.SetTimeOut(0.02, self.check_sview)

    def _update_view(self):
        self._update_list_item()
        self._update_lab_num()

    def _update_list_item(self):
        self._debris_list = []
        self._cur_select_count = 0
        self._cur_select_item_dict = {}
        for item_no in self._debris_id_list:
            item_no = int(item_no)
            item_num = global_data.player.get_item_num_by_no(item_no) if global_data.player else 0
            if item_num > 1:
                for _ in range(item_num - 1):
                    self._debris_list.append(item_no)
                    self._cur_select_index_list.append(self._cur_select_count)
                    self._cur_select_count += 1
                    if not self._cur_select_item_dict.get(item_no):
                        self._cur_select_item_dict[item_no] = 0
                    self._cur_select_item_dict[item_no] += 1

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
            all_height += debris_item.getContentSize().height
            index += 1

        self._list_item.ScrollToTop()
        self._list_item._container._refreshItemPos()
        self._list_item._refreshItemPos()
        self._cur_show_index = index - 1

    def check_sview(self):
        show_data = self.get_show_data()
        self._cur_show_index = self._list_item.AutoAddAndRemoveItem(self._cur_show_index, show_data, len(show_data), self.add_list_item)
        self._is_check_sview = False

    def get_show_data(self):
        return self._debris_list

    def add_list_item(self, item_no, is_back_item, index=-1):
        if is_back_item:
            debris_item = self._list_item.AddTemplateItem(bRefresh=True)
        else:
            debris_item = self._list_item.AddTemplateItem(0, bRefresh=True)
        debris_item.lab_title.setString(get_lobby_item_name(item_no))
        debris_item.lab_describe.setString(get_lobby_item_desc(item_no))
        btn_info = debris_item.btn_info
        btn_info.EnableCustomState(True)
        item_num = 1
        init_story_debris_item(debris_item.temp_item, item_no, item_num, False)
        btn_info.SetSelect(index in self._cur_select_index_list)

        @btn_info.callback()
        def OnClick(btn, touch):
            if btn.GetSelect():
                self._cur_select_item_dict[item_no] -= 1
                if self._cur_select_item_dict[item_no] == 0:
                    self._cur_select_item_dict.pop(item_no)
                self._cur_select_count -= 1
                btn.SetSelect(False)
                self._cur_select_index_list.remove(index)
            else:
                if not self._cur_select_item_dict.get(item_no):
                    self._cur_select_item_dict[item_no] = 0
                self._cur_select_item_dict[item_no] += 1
                self._cur_select_count += 1
                btn.SetSelect(True)
                self._cur_select_index_list.append(index)
            self._update_lab_num()

        return debris_item

    def _update_lab_num(self):
        decompose_count = self._cur_select_count * PVE_STORY_DECOMPOSE_COUNT
        self.panel.lab_num.setString(get_text_by_id(1400068).format(decompose_count))
        self.panel.btn_recycle.SetEnable(self._cur_select_count > 0)

    def on_pve_debris_decompose(self):
        self._update_view()

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVEDebrisDecomposeUI, self).on_finalize_panel()