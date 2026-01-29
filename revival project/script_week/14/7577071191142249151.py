# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/SkinDefineDecorationWidget.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils import item_utils, dress_utils
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FPOS_2_TAG_STR, FASHION_POS_HAIR
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
import math3d
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.client.const import mall_const
from logic.gcommon.item import lobby_item_type
from logic.gutils import red_point_utils
TAG_BAG = FASHION_POS_BACK
TAG_HAIR = FASHION_POS_HAIR

class SkinDefineDecorationWidget(BaseUIWidget):

    def __init__(self, parent, panel, deco_type_list):
        self.global_events = {'player_item_update_event_with_id': self.on_buy_good_success,
           'refresh_item_red_point': self.refresh_list_view
           }
        super(SkinDefineDecorationWidget, self).__init__(parent, panel)
        self.deco_type_list = deco_type_list
        self.nonempty_deco_type_list = []
        self.deco_type_dict = {}
        self._is_in_touch = False
        self.deco_type = None
        self.role_id = 0
        self._ui_role_id = 0
        self.top_skin_id = 0
        self.skin_id = self.parent.preview_skin
        self.item_dict = {}
        self.using_no = 0
        self.selected_no = 0
        self.own_items = set()
        self.btn_dict = {}
        self.cur_tag = ''
        self.init_tag_btn()
        return

    def init_tag_btn(self):
        tag_list = self.deco_type_list
        for tag, _, deco_type in self.deco_type_list:
            self.deco_type_dict[tag] = deco_type

        if len(self.deco_type_list) == 1:
            tag, _, deco_type = self.deco_type_list[0]
            self.deco_type = self.deco_type_dict[tag]
            self.cur_tag = tag
            self.panel.img_top_bar.setVisible(True)
            self.panel.bar_tab.setVisible(False)
            return
        self.panel.tab_small.SetInitCount(len(tag_list))
        for i, (tag, text_id, l_item_type) in enumerate(tag_list):
            tag_item = self.panel.tab_small.GetItem(i)
            tag_item.btn.SetText(text_id)
            if len(tag_list) == 2:
                tag_item.setContentSize(cc.Size(147, tag_item.getContentSize().height))
                tag_item.ResizeAndPosition(include_self=False)
            else:
                tag_item.ResizeAndPosition()
            self.btn_dict[tag] = tag_item
            tag_item.btn.BindMethod('OnClick', lambda b, t, tag=tag: self.select_tag(tag))

        self.panel.tab_small.RefreshItemPos()

    def refresh_tag_btn_color(self):
        if not self.top_skin_id or not self.role_id:
            return
        for tag, btn in six.iteritems(self.btn_dict):
            deco_list = dress_utils.get_valid_deco_list_for_skin_id(self.role_id, self.top_skin_id, [FPOS_2_TAG_STR.get(self.deco_type_dict[tag], '')])
            if not deco_list:
                self.nonempty_deco_type_list.append(self.deco_type_dict[tag])

    def select_tag(self, tag):
        if self.cur_tag == tag or tag not in self.deco_type_dict:
            return
        for tag_i, btn in six.iteritems(self.btn_dict):
            if tag_i == tag:
                btn.btn.SetSelect(True)
            else:
                btn.btn.SetShowEnable(self.deco_type_dict[tag_i] not in self.nonempty_deco_type_list)

        self.cur_tag = tag
        self.deco_type = self.deco_type_dict[tag]
        self.refresh_all_content()
        if tag == TAG_BAG:
            global_data.emgr.rotate_model_display_by_euler.emit(math3d.vector(0, 180, 0))
        else:
            global_data.emgr.rotate_model_display_by_euler.emit()

    def show_panel(self, flag):
        if self.panel:
            self.panel.setVisible(flag)

    def on_hide(self):
        self.hide()

    def destroy(self):
        self.item_dict = {}
        self.btn_dict = {}
        super(SkinDefineDecorationWidget, self).destroy()

    def set_role_id(self, role_id, top_skin_id):
        self.role_id = role_id
        self.top_skin_id = top_skin_id
        self.refresh_tag_btn_color()

    def on_parent_hide(self):
        self.on_click_select(self.using_no, False)

    def refresh_all_content(self):
        if not self.cur_tag:
            if self.deco_type_list:
                first_tag, _, _ = self.deco_type_list[0]
                self.select_tag(first_tag)
                return
        self.on_refresh_list()
        skin_id = self.parent.get_preview_skin_id()
        self.on_change_skin_id(skin_id)
        cur_role_skin_decoration = dress_utils.get_role_fashion_decoration_dict(self.role_id, skin_id)
        using_no = cur_role_skin_decoration.get(self.deco_type) or 0
        viewing_no = self.parent.get_preview_decoration_data().get(self.deco_type) or using_no
        self.on_click_choose(using_no)
        self.on_click_select(viewing_no, False)
        self.refresh_model_rot(viewing_no)
        self.set_introduction_and_btn()

    def refresh_model_rot(self, viewing_no):
        euler = confmgr.get('lobby_item', str(viewing_no), 'off_euler_rot')
        if euler:
            global_data.emgr.rotate_model_display_by_euler.emit(math3d.vector(euler[0], euler[1], euler[2]))
        elif self.cur_tag in (TAG_BAG, TAG_HAIR):
            global_data.emgr.rotate_model_display_by_euler.emit(math3d.vector(0, 180, 0))
        else:
            global_data.emgr.rotate_model_display_by_euler.emit(math3d.vector(0, 0, 0))

    def on_dress_change(self, new_skin_id):
        self.refresh_all_content()

    def on_refresh_list(self):
        role_id = self.role_id
        self.own_items = set()
        deco_list = dress_utils.get_valid_deco_list_for_skin_id(role_id, self.top_skin_id, [FPOS_2_TAG_STR.get(self.deco_type, '')])
        deco_list = dress_utils.handle_unusable_dec(deco_list, self.parent.preview_skin)
        own_deco_list = []
        no_own_deco_list = []
        for item_no in deco_list:
            if global_data.player.has_item_by_no(item_no):
                own_deco_list.append(item_no)
            else:
                no_own_deco_list.append(item_no)

        deco_list = own_deco_list + no_own_deco_list
        self.item_dict = {}
        self.panel.list_dec.RecycleAllItem()
        for item_no in deco_list:
            ui_item_head = self.panel.list_dec.ReuseItem(False)
            if not ui_item_head:
                ui_item_head = self.panel.list_dec.AddTemplateItem()
            ui_item = ui_item_head.temp_item_dark
            template_utils.init_tempate_mall_i_simple_item(ui_item, item_no)
            ui_item.nd_using.setVisible(self.using_no == item_no)
            ui_item.btn_choose.SetSelect(self.selected_no == item_no)
            self.item_dict[item_no] = ui_item
            ui_item.lab_name.SetString(self.get_short_show_name(item_utils.get_lobby_item_name(item_no)))
            ui_item.btn_choose.BindMethod('OnBegin', lambda b, t: self.on_begin_touch())
            ui_item.btn_choose.BindMethod('OnEnd', lambda b, t: self.on_end_touch())
            ui_item.btn_choose.BindMethod('OnCancel', lambda b, t: self.on_end_touch())
            if item_no != self.selected_no:
                ui_item.btn_choose.BindMethod('OnClick', lambda b, t, id=item_no: self.on_click_select(id))
            else:
                ui_item.btn_choose.BindMethod('OnClick', lambda b, t: self.on_click_select(0))

        if not deco_list:
            self.panel.img_empty.setVisible(True)
        else:
            self.panel.img_empty.setVisible(False)
        self.refresh_list_view()
        self.panel.lab_equip_applique_num.SetString('%d/%d' % (len(self.own_items), len(self.item_dict)))

    def on_begin_touch(self):
        if self._is_in_touch:
            return False
        self._is_in_touch = True
        return True

    def on_end_touch(self):
        self._is_in_touch = False

    def get_short_show_name(self, name):
        if ']' in name:
            return name[name.index(']') + len(']'):]
        if '\xe3\x80\x91' in name:
            return name[name.index('\xe3\x80\x91') + len('\xe3\x80\x91'):]
        return name

    def on_change_skin_id(self, skin_id):
        for item_no, ui_item in six.iteritems(self.item_dict):
            matched = dress_utils.check_valid_decoration(skin_id, item_no)
            ui_item.nd_forbidden.setVisible(not matched)

        if self.skin_id == skin_id:
            return
        self.skin_id = skin_id
        old_top_skin_od = self.top_skin_id
        self.top_skin_id = dress_utils.get_top_skin_id_by_skin_id(skin_id)
        if old_top_skin_od != self.top_skin_id:
            self.refresh_tag_btn_color()

    def set_item_status(self, item_no, ui_item, own):
        ui_item.nd_lock.setVisible(not own)
        if own:
            self.own_items.add(item_no)
        has_rp = global_data.lobby_red_point_data.get_rp_by_no(item_no)
        red_point_utils.show_red_point_template(ui_item.nd_new, has_rp)

    def refresh_list_view(self):
        has = global_data.player.has_item_by_no if global_data.player else (lambda : False)
        for item_no, ui_item in six.iteritems(self.item_dict):
            self.set_item_status(item_no, ui_item, has(int(item_no)))

        self.refresh_tag_red_point()

    def refresh_tag_red_point(self):
        for tag, btn in six.iteritems(self.btn_dict):
            dec_str = FPOS_2_TAG_STR.get(tag)
            deco_list = dress_utils.get_valid_deco_list_for_skin_id(self.role_id, self.top_skin_id, [dec_str])
            rp_vis = global_data.lobby_red_point_data.get_rp_by_item_no_list(deco_list)
            red_point_utils.show_red_point_template(btn.btn.temp_reddot, rp_vis)

    def set_introduction_and_btn(self):
        item_no = self.selected_no
        cur_item = self.item_dict.get(item_no)
        btn = self.panel.btn_buy.btn_common
        self.panel.temp_price.setVisible(False)
        method_nd = self.panel.lab_get_method
        if not cur_item:
            btn.setVisible(False)
            method_nd.setVisible(False)
            return
        else:
            btn.setVisible(True)
            method_nd.setVisible(True)
            method_nd.SetString(item_utils.get_item_access(item_no))
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
                goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
                price = mall_utils.get_mall_item_price(goods_id)
                if price and not item_utils.is_jump_to_lottery(item_no):
                    unowned_item_nos = mall_utils.get_goods_id_unowned_open_item_nos(goods_id)
                    if not unowned_item_nos:

                        def buy_func(goods_id):
                            if self.parent:
                                self.parent.on_about_to_buy_callback([item_no])
                            groceries_buy_confirmUI(goods_id)

                        template_utils.init_price_view(self.panel.temp_price, goods_id, mall_const.DEF_PRICE_COLOR)
                        self.panel.temp_price.setVisible(True)
                        btn.SetText(get_text_by_id(81710))
                        from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                        btn.BindMethod('OnClick', lambda b, t, id=goods_id: buy_func(id))
                    else:
                        self.panel.temp_price.setVisible(False)
                        btn.SetEnable(False)
                        name_text = item_utils.get_lobby_item_name(unowned_item_nos[0])
                        method_nd.SetString(get_text_by_id(81606, {'skin_name': name_text}))
                        btn.SetText(80828)
                elif not item_utils.can_jump_to_ui(item_no):
                    btn.SetText(80828)
                    btn.SetEnable(False)
            return

    def force_revert(self):
        self.on_click_select(0, False)

    def on_click_select(self, item_no, upload=True):
        item_no = int(item_no)
        if self.selected_no == item_no:
            return
        if item_no != 0:
            self.refresh_model_rot(item_no)
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
        if global_data.player:
            global_data.player.req_del_item_redpoint(item_no)

    def on_buy_good_success(self, item_no):
        self.on_refresh_list()
        self.set_introduction_and_btn()

    def jump_to_item_no(self, item_no):
        from logic.gutils import item_utils
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_no is None:
            self.on_click_select(0, True)
        fashion_pos = dress_utils.get_lobby_type_fashion_pos(item_type)
        if fashion_pos not in six_ex.keys(self.deco_type_dict):
            return
        else:
            self.select_tag(fashion_pos)
            if int(item_no) in self.item_dict:
                self.on_click_select(item_no)
            return

    def revert_choose_by_tag(self, tag):
        if tag in self.deco_type_dict and self.cur_tag == tag:
            self.on_click_choose(0)

    def revert_choose_by_item_no(self, item_no):
        if item_no in self.item_dict:
            self.on_click_choose(0)