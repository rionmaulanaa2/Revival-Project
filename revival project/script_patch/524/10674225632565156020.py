# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/DecorationWidget.py
from __future__ import absolute_import
import six
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils import item_utils, dress_utils
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
TYPE_2_STR = {FASHION_POS_HEADWEAR: 'Head',
   FASHION_POS_BACK: 'Bag',
   FASHION_POS_SUIT_2: 'PendantSuit'
   }
TYPE_2_LAB = {FASHION_POS_HEADWEAR: 81232,
   FASHION_POS_BACK: 81285,
   FASHION_POS_SUIT_2: 81286
   }
TYPE_2_RULE = {FASHION_POS_HEADWEAR: (81254, 81252),
   FASHION_POS_BACK: (81289, 81287),
   FASHION_POS_SUIT_2: (81290, 81288)
   }

class DecorationWidget(BaseUIWidget):

    def __init__(self, parent, panel, deco_type):
        self.global_events = {'player_item_update_event_with_id': self.on_buy_good_success,
           'refresh_item_red_point': self.refresh_list_view
           }
        super(DecorationWidget, self).__init__(parent, panel)
        self.deco_type = deco_type
        self.role_id = 0
        self._ui_role_id = 0
        self.skin_id = 0
        self.item_dict = {}
        self.using_no = 0
        self.selected_no = 0
        self.own_items = set()

        @self.panel.btn_describe.callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, rule = TYPE_2_RULE.get(self.deco_type) or (81254, 81252)
            dlg.set_show_rule(get_text_local_content(title), get_text_local_content(rule))

    def show_panel(self, flag):
        if self.panel:
            self.panel.setVisible(flag)
        if not flag:
            global_data.ui_mgr.close_ui('GameRuleDescUI')

    def destroy(self):
        self.item_dict = {}
        super(DecorationWidget, self).destroy()

    def set_role_id(self, role_id):
        self.role_id = role_id

    def on_parent_hide(self):
        self.on_click_select(self.using_no)

    def refresh_all_content(self):
        self.on_change_role_id(self.role_id)
        skin_id = self.parent.get_preview_skin_id()
        self.on_change_skin_id(skin_id)
        using_no = dress_utils.get_role_decroation_id(self.role_id, skin_id, self.deco_type) or 0
        self.on_click_choose(using_no)
        self.on_click_select(using_no)
        self.set_introduction_and_btn()

    def on_change_role_id(self, role_id):
        if self._ui_role_id == role_id:
            return
        self._ui_role_id = role_id
        self.own_items = set()
        deco_list = dress_utils.get_valid_deco_list_for_skin_id(role_id, TYPE_2_STR.get(self.deco_type, ''))
        self.item_dict = {}
        self.panel.list_deco.DeleteAllSubItem()
        for item_no in deco_list:
            ui_item = self.panel.list_deco.AddTemplateItem()
            self.item_dict[item_no] = ui_item
            res_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            ui_item.img_fx.SetDisplayFrameByPath('', res_path)
            ui_item.btn_choose.BindMethod('OnClick', lambda b, t, id=item_no: self.on_click_select(id))

        self.refresh_list_view()
        self.panel.lab_title.SetString('%s %d/%d' % (get_text_by_id(TYPE_2_LAB.get(self.deco_type)), len(self.own_items), len(self.item_dict)))

    def on_change_skin_id(self, skin_id):
        if self.skin_id == skin_id:
            return
        self.skin_id = skin_id
        for item_no, ui_item in six.iteritems(self.item_dict):
            matched = dress_utils.check_valid_decoration(skin_id, item_no)
            ui_item.nd_forbidden.setVisible(not matched)

    def set_item_status(self, item_no, ui_item, own):
        ui_item.nd_lock.setVisible(not own)
        if own:
            self.own_items.add(item_no)
        has_rp = global_data.lobby_red_point_data.get_rp_by_no(item_no)
        ui_item.nd_new.setVisible(has_rp)

    def refresh_list_view(self):
        has = global_data.player.has_item_by_no if global_data.player else (lambda : False)
        for item_no, ui_item in six.iteritems(self.item_dict):
            self.set_item_status(item_no, ui_item, has(int(item_no)))

    def set_introduction_and_btn(self):
        item_no = self.selected_no
        cur_item = self.item_dict.get(item_no)
        btn = self.panel.temp_btn_use.btn_common
        name_nd = self.panel.lab_fx_name
        method_nd = self.panel.lab_get_method
        if not cur_item:
            btn.setVisible(False)
            name_nd.setVisible(False)
            method_nd.setVisible(False)
            return
        else:
            btn.setVisible(True)
            name_nd.setVisible(True)
            method_nd.setVisible(True)
            if global_data.player:
                own = global_data.player.has_item_by_no(item_no) if 1 else False
                btn.SetEnable(True)
                if own:
                    role_data = global_data.player.get_item_by_no(self.role_id)
                    matched = dress_utils.check_valid_decoration(self.skin_id, item_no)
                    matched or btn.SetEnable(False)
                    btn.SetText(18143)
                elif role_data is None:
                    btn.SetEnable(False)
                    btn.SetText(2215)
                elif item_no == self.using_no:
                    btn.SetText(81247)
                    btn.BindMethod('OnClick', lambda b, t, id=0: self.on_click_choose(id))
                else:
                    btn.SetText(2220)
                    btn.BindMethod('OnClick', lambda b, t, id=item_no: self.on_click_choose(id))
            else:
                btn.SetText(2222)
                btn.BindMethod('OnClick', lambda b, t, id=item_no: item_utils.jump_to_ui(id))
            method_nd.SetString(item_utils.get_item_access(item_no))
            name_nd.SetString(item_utils.get_lobby_item_name(item_no))
            size = name_nd.getTextContentSize()
            name_nd.bar.SetContentSize(size.width, size.height + 10)
            name_nd.bar.setAnchorPoint(cc.Vec2(0.5, 0.5))
            name_nd.bar.SetPosition('50%', '50%')
            return

    def force_revert(self):
        self.on_click_select(0, False)

    def on_click_select(self, item_no, upload=True):
        item_no = int(item_no)
        if self.selected_no == item_no:
            return
        ori_item = self.item_dict.get(self.selected_no)
        if ori_item:
            ori_item and ori_item.btn_choose.SetSelect(False)
            ori_item.btn_choose.BindMethod('OnClick', lambda b, t, id=self.selected_no: self.on_click_select(id))
            if not item_no and upload:
                self.parent.revert_preview_decoration(self.deco_type)
        self.selected_no = item_no
        cur_item = self.item_dict.get(item_no)
        if cur_item:
            cur_item.btn_choose.SetSelect(True)
            cur_item.btn_choose.BindMethod('OnClick', lambda *args: self.on_click_select(0))
            if dress_utils.check_valid_decoration(self.skin_id, item_no):
                self.parent.change_preview_decoration(self.deco_type, item_no)
            else:
                tip_text = get_text_by_id(81351).format('#DB' + item_utils.get_lobby_item_name(self.skin_id) + '#SW')
                global_data.game_mgr.show_tip(tip_text)
        self.set_introduction_and_btn()
        if global_data.player:
            global_data.player.req_del_item_redpoint(item_no)

    def on_click_choose(self, item_no):
        if self.using_no == item_no:
            return
        ori_item = self.item_dict.get(self.using_no)
        if ori_item:
            ori_item.nd_using.setVisible(False)
            if not item_no:
                self.parent.revert_choose(self.deco_type)
                self.on_click_select(0)
        self.using_no = item_no
        cur_item = self.item_dict.get(item_no)
        if cur_item:
            cur_item.nd_using.setVisible(True)
            self.parent.choose(self.deco_type, item_no)
        self.set_introduction_and_btn()

    def on_buy_good_success(self, item_no):
        if item_no in self.item_dict:
            ui_item = self.item_dict[item_no]
            self.set_item_status(item_no, ui_item, True)
            self.set_introduction_and_btn()
        self.panel.lab_title.SetString('%s %d/%d' % (get_text_by_id(TYPE_2_LAB.get(self.deco_type)), len(self.own_items), len(self.item_dict)))