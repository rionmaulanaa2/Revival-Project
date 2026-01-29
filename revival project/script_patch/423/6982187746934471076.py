# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESuggestWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const.pve_const import PVE_MECHA_NEW_CACHE
from logic.gutils.template_utils import FrameLoaderTemplate
from logic.gutils.role_head_utils import init_role_head
from logic.gcommon.common_utils.local_text import get_text_by_id
from .PVESuggestReplyUI import PVESuggestReplyUI
from logic.gcommon.common_const.pve_const import PVE_SUGGEST_CACHE
from logic.gutils.custom_ui_utils import get_cut_name
from common.cfg import confmgr
import six_ex
import six

class PVESuggestWidget(object):

    def __init__(self, nd, sheet_id):
        self.init_params(sheet_id)
        self.init_ui(nd)
        self.process_events(True)

    def init_params(self, sheet_id):
        global_data.player.request_suggest_info(sheet_id)
        self._sheet_id = sheet_id
        self._frame_loader_template = None
        self._cur_create_suggest_index = None
        self._archive_data = global_data.achi_mgr.get_general_archive_data()
        self._suggest_id_2_item = {}
        self._suggest_list = []
        self._suggest_conf = confmgr.get('pve_suggest_conf', 'SuggestConf', 'Content')
        for suggest_id, suggest_info in self._suggest_conf.items():
            if suggest_info.get('belong_sheet') == self._sheet_id:
                self._suggest_list.append(suggest_id)

        return

    def init_ui(self, nd):
        self._nd = nd
        self._list_item = nd.list_item
        self._frame_loader_template = FrameLoaderTemplate(self._list_item, len(self._suggest_list), self._init_suggest_item)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_do_like_pve_suggest': self.on_do_like_pve_suggest,
           'message_on_suggest_info': self.message_on_suggest_info
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def show(self):
        self._nd.setVisible(True)

    def hide(self):
        self._nd.setVisible(False)

    def _init_suggest_item(self, suggest_item, cur_index):
        suggest_id = self._suggest_list[cur_index]
        pnl_bg = suggest_item.pnl_bg
        conf = self._suggest_conf.get(suggest_id)
        self._suggest_id_2_item[suggest_id] = suggest_item
        pnl_bg.lab_name.setString(get_text_by_id(conf.get('suggest_player_name')))
        frame_item_no = conf.get('suggest_frame_no')
        photo_no = conf.get('suggest_photo_no')
        init_role_head(pnl_bg.temp_head, frame_item_no, photo_no)
        suggest_str = six.text_type(get_text_by_id(conf.get('suggest_text_id')))
        suggest_str = get_cut_name(suggest_str, 70)
        pnl_bg.lab_content.setString(suggest_str)
        pve_suggest_cache = self._archive_data.get_field(PVE_SUGGEST_CACHE, {})
        pve_sheet_suggest_cache = pve_suggest_cache.get(self._sheet_id, [])
        suggest_item.img_new_tag.setVisible(suggest_id not in pve_sheet_suggest_cache)
        lab_like = suggest_item.pnl_bg.lab_like
        like_item = lab_like.nd_auto_fit.list_icon.GetItem(0)
        btn_icon = like_item.btn_icon
        btn_icon.EnableCustomState(True)
        self._update_like(suggest_item, suggest_id)

        @like_item.btn_icon.callback()
        def OnClick(btn, touch):
            is_like = global_data.player.get_pve_suggest_is_like(self._sheet_id, suggest_id)
            if not is_like:
                global_data.player.do_like_pve_suggest(self._sheet_id, suggest_id)

        @suggest_item.callback()
        def OnClick(btn, touch):
            PVESuggestReplyUI(sheet_id=self._sheet_id, suggest_id=suggest_id)
            suggest_item.img_new_tag.setVisible(False)
            pve_suggest_cache = self._archive_data.get_field(PVE_SUGGEST_CACHE, {})
            if not pve_suggest_cache.get(self._sheet_id):
                pve_suggest_cache[self._sheet_id] = []
            pve_suggest_cache[self._sheet_id].append(suggest_id)
            self._archive_data.set_field(PVE_SUGGEST_CACHE, pve_suggest_cache)

    def _update_like(self, suggest_item, suggest_id):
        lab_like = suggest_item.pnl_bg.lab_like
        lab_like.setString(str(global_data.player.get_pve_suggest_like_count(suggest_id)))
        is_like = global_data.player.get_pve_suggest_is_like(self._sheet_id, suggest_id)
        like_item = lab_like.nd_auto_fit.list_icon.GetItem(0)
        like_item.btn_icon.SetSelect(is_like)

    def message_on_suggest_info(self, sheet_id, data):
        if self._sheet_id == sheet_id:
            for suggest_info in data:
                suggest_id = suggest_info[0]
                self.on_do_like_pve_suggest(self._sheet_id, suggest_id)

    def on_do_like_pve_suggest(self, sheet_id, suggest_id):
        if self._sheet_id == sheet_id:
            suggest_item = self._suggest_id_2_item[suggest_id]
            if suggest_item and suggest_item.isValid():
                self._update_like(suggest_item, suggest_id)

    def destroy(self):
        self.process_events(False)
        self._cur_create_suggest_index = None
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        self._mecha_id_2_item = None
        self._sheet_id = None
        self._cur_create_suggest_index = None
        self._suggest_id_2_item = None
        self._suggest_list = None
        self._suggest_conf = None
        return