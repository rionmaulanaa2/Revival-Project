# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaDrugWidget.py
from __future__ import absolute_import

class MechaDrugWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self._cur_recommend_drug = None
        self.init_drug_btn()
        self.process_events(True)
        return

    def destroy(self):
        self.process_events(False)
        self.panel = None
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_item_data_changed_event': self.on_item_data_changed,
           'set_drug_shortcut_event': self.set_drug_shortcut
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_item_data_changed(self, item_data):
        if not item_data or item_data['item_id'] == self._cur_recommend_drug:
            self.update_drug_recommend()
            self.check_hide()

    def set_drug_shortcut(self, item_type, need_sync=False):
        self.update_drug_recommend()
        self.check_hide()

    def update_drug_recommend(self):
        if global_data.player and global_data.player.logic:
            drug_id = global_data.player.logic.ev_g_drug_shortcut()
            item_count = global_data.player.logic.ev_g_item_count(drug_id)
            if drug_id and item_count:
                self.set_quick_drug_item({'item_id': drug_id,'num': item_count})
            self._cur_recommend_drug = drug_id

    def set_quick_drug_item(self, drug_data):
        item_no = drug_data.get('item_id')
        num = drug_data.get('num', 0)
        from logic.gutils import item_utils
        pic_path = item_utils.get_item_pic_by_item_no(item_no)
        self.panel.sp_item.SetDisplayFrameByPath('', pic_path)
        self.panel.lab_quantity.setString(str(num))

    def init_drug_btn(self):

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.hide()

        @self.panel.btn_medicine.unique_callback()
        def OnClick(btn, touch):
            if self._cur_recommend_drug:
                self.try_use_medicine(self._cur_recommend_drug)

    def hide(self):
        self.panel.setVisible(False)

    def show(self):
        self.check_show()

    def check_hide(self):
        if not self._cur_recommend_drug:
            self.hide()

    def check_show(self):
        self.update_drug_recommend()
        if self._cur_recommend_drug:
            self.panel.setVisible(True)
        else:
            self.panel.setVisible(False)

    def try_use_medicine(self, drug_item_id):
        player = None
        if global_data.player and global_data.player.logic:
            player = global_data.player.logic
        else:
            return
        from logic.gcommon.cdata.status_config import ST_USE_ITEM
        if not player.ev_g_status_check_pass(ST_USE_ITEM):
            return
        else:
            in_using_drug = player.ev_g_cur_itemuse()
            if in_using_drug and drug_item_id == in_using_drug:
                return
            if in_using_drug:
                player.send_event('E_ITEMUSE_CANCEL', in_using_drug)
            elif drug_item_id:
                player.send_event('E_CTRL_USE_DRUG', drug_item_id)
                player.send_event('E_ITEMUSE_TRY', drug_item_id)
            return