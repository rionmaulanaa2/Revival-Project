# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/DIYWidget.py
from __future__ import absolute_import
import six
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
from logic.gutils import dress_utils, item_utils, template_utils, mall_utils
from logic.client.const import mall_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
import cc
from copy import copy
import math3d
from logic.gcommon.item import lobby_item_type
from .VoiceWidget import VoiceWidget
from .DecorationWidget import DecorationWidget
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2
from logic.gcommon.item import lobby_item_type
TAG_VOICE = 'Voice'
TAG_HEAD = FASHION_POS_HEADWEAR
TAG_BAG = FASHION_POS_BACK
TAG_SUIT = FASHION_POS_SUIT_2
TAG_DICT = {TAG_VOICE: (
             'temp_voice', VoiceWidget),
   TAG_HEAD: (
            'temp_head', DecorationWidget),
   TAG_BAG: (
           'temp_bag', DecorationWidget),
   TAG_SUIT: (
            'temp_suit', DecorationWidget)
   }
TAG_LIST = (
 (
  TAG_VOICE, 81227, lobby_item_type.L_ITEM_TYPE_VOICE),
 (
  TAG_HEAD, 81229, lobby_item_type.L_ITEM_TYPE_HEAD),
 (
  TAG_BAG, 81230, lobby_item_type.L_ITEM_TYPE_BODY),
 (
  TAG_SUIT, 81228, lobby_item_type.L_ITEM_TYPE_SUIT))
CONDUCT_EVENT = {TAG_HEAD: 'change_model_display_head',
   TAG_BAG: 'change_model_display_bag',
   TAG_SUIT: 'change_model_display_suit'
   }

class DIYWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'refresh_item_red_point': self.refresh_role_diy_rp
           }
        super(DIYWidget, self).__init__(parent, panel)
        self.role_id = 0
        self.skin_id = 0
        self.chosen_item = {}
        self.preview_item = {}
        self._need_preview_model = False
        self._first_loaded_preview_model = False
        self._ui_role_id = 0
        self.cur_tag = ''
        self.btn_dict = {}
        self.widget_dict = {}
        self.init_tag_btn()

    def init_tag_btn(self):
        self.panel.pnl_list_top_tab.SetInitCount(len(TAG_LIST))
        for i, (tag, text_id, l_item_type) in enumerate(TAG_LIST):
            tag_item = self.panel.pnl_list_top_tab.GetItem(i)
            tag_item.btn_tab.SetText(text_id)
            self.btn_dict[tag] = tag_item
            tag_item.btn_tab.BindMethod('OnClick', lambda b, t, tag=tag: self.select_tag(tag))

    def select_tag(self, tag):
        if self.cur_tag == tag or tag not in TAG_DICT:
            return
        if tag not in self.widget_dict:
            nd_name, widget_cls = TAG_DICT[tag]
            self.widget_dict[tag] = widget_cls(self, getattr(self.panel, nd_name), tag)
            self.widget_dict[tag].set_role_id(self.role_id)
        self.widget_dict[tag].refresh_all_content()
        for tag_i, btn in six.iteritems(self.btn_dict):
            btn.btn_tab.SetSelect(tag_i == tag)

        for tag_i, widget in six.iteritems(self.widget_dict):
            widget.show_panel(tag_i == tag)

        self.cur_tag = tag
        if tag == TAG_BAG:
            global_data.emgr.rotate_model_display_by_euler.emit(math3d.vector(0, 180, 0))
        else:
            global_data.emgr.rotate_model_display_by_euler.emit()

    def show_panel(self, flag):
        self.panel.setVisible(flag)

    def on_hide(self):
        global_data.ui_mgr.close_ui('GameRuleDescUI')
        for widget in six.itervalues(self.widget_dict):
            widget.on_parent_hide()

    def refresh_role_diy_rp(self):
        for i, (tag, text_id, l_item_type) in enumerate(TAG_LIST):
            tag_item = self.panel.pnl_list_top_tab.GetItem(i)
            has_rp = global_data.lobby_red_point_data.get_rp_by_type_and_belong(l_item_type, self.role_id)
            tag_item.img_red_dot.setVisible(has_rp)

    def destroy(self):
        self.btn_dict = {}
        for widget in six.itervalues(self.widget_dict):
            widget.destroy()

        super(DIYWidget, self).destroy()

    def set_role_id(self, role_id):
        self.role_id = role_id
        for widget in six.itervalues(self.widget_dict):
            widget.set_role_id(role_id)

        global_data.ui_mgr.close_ui('GameRuleDescUI')
        self.refresh_role_diy_rp()

    def refresh_all_content(self, update_data_only=False):
        if not self.cur_tag:
            self.select_tag(TAG_VOICE)
        self._ui_role_id = self.role_id
        self.skin_id = self.parent.get_preview_skin_id()
        self.preview_item = self.parent.get_preview_data(self.skin_id)
        self.chosen_item = copy(self.preview_item)
        if not update_data_only:
            self.widget_dict[self.cur_tag].refresh_all_content()

    def on_dress_change(self, new_skin_id):
        self.refresh_all_content()

    def get_preview_skin_id(self):
        return self.parent.get_preview_skin_id()

    def revert_preview_decoration(self, tag):
        if not self.preview_item.get(tag):
            return
        global_data.emgr.emit(CONDUCT_EVENT[tag], 0, int(self.skin_id))
        self.preview_item[tag] = 0

    def revert_choose(self, tag):
        if not self.chosen_item.get(tag):
            return
        self.chosen_item[tag] = 0
        global_data.player.undress_role_fashion(self.role_id, [tag])

    def choose(self, tag, item_no):
        if self.chosen_item.get(tag) == item_no:
            return
        revert_tag = (TAG_HEAD, TAG_BAG) if tag == TAG_SUIT else (TAG_SUIT,)
        for _tag in revert_tag:
            if _tag in self.widget_dict:
                self.widget_dict[_tag].on_click_choose(0)
            else:
                self.revert_choose(_tag)

        self.chosen_item[tag] = item_no
        global_data.player.dress_role_fashion({tag: item_no})

    def _mode_preview_callback(self, model):
        if self._first_loaded_preview_model:
            if self.cur_tag == TAG_BAG:
                global_data.emgr.rotate_model_display_by_euler.emit(math3d.vector(0, 180, 0))
            else:
                global_data.emgr.rotate_model_display_by_euler.emit()
            self._first_loaded_preview_model = False

    def jump_to_item_no(self, need_preview_model, item_no):
        from logic.gutils import item_utils
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type not in [lobby_item_type.L_ITEM_TYPE_HEAD, lobby_item_type.L_ITEM_TYPE_BODY, lobby_item_type.L_ITEM_TYPE_SUIT]:
            return
        self.refresh_all_content(update_data_only=True)
        self._need_preview_model = need_preview_model
        for i, (tag, text_id, l_item_type) in enumerate(TAG_LIST):
            if item_type == l_item_type:
                self.select_tag(tag)
                if self.preview_item.get(tag) != item_no:
                    self.widget_dict[tag].on_click_select(item_no)
                    if self._need_preview_model and not dress_utils.check_valid_decoration(self.skin_id, item_no):
                        self.do_load_preview_model()
                else:
                    self.do_load_preview_model()
                self._need_preview_model = False
                return

        self._need_preview_model = False

    def do_load_preview_model(self):
        self._first_loaded_preview_model = True
        model_data = self.parent.get_preview_model_data(self.preview_item)
        global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=self._mode_preview_callback)

    def change_preview_decoration(self, tag, item_no):
        if self.preview_item.get(tag) == item_no:
            return
        if tag == TAG_SUIT:
            revert_tag = (TAG_HEAD, TAG_BAG) if 1 else (TAG_SUIT,)
            for _tag in revert_tag:
                self.revert_preview_decoration(_tag)
                if _tag in self.widget_dict:
                    self.widget_dict[_tag].force_revert()

            self._need_preview_model or global_data.emgr.emit(CONDUCT_EVENT[tag], int(item_no), int(self.skin_id))
            self.preview_item[tag] = item_no
        else:
            self.preview_item[tag] = item_no
            self.do_load_preview_model()