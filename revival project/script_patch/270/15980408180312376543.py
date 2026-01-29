# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PetSubSkinWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no, check_skin_tag, is_itemtype_in_serving, get_pet_rare_degree_pic_by_item_no, get_item_rare_degree
from common.framework import Functor
from logic.gutils.mall_utils import get_item_money_type, get_my_money, get_payment_item_no
from logic.gutils.template_utils import init_price_template, init_common_price

class PetSubSkinWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.cur_main_skin_id = None
        self.skin_list = None
        self.cur_skin_idx = None
        global_data.emgr.pet_skin_promoted += self.on_pet_skin_promoted
        global_data.emgr.pet_sub_skin_changed += self.on_pet_sub_skin_changed
        return

    def update_skin_id(self, skin_id):
        if skin_id == self.cur_main_skin_id:
            return
        else:
            self.cur_main_skin_id = skin_id
            cur_select_skin_id = skin_id
            if global_data.player:
                cur_select_skin_id = global_data.player.get_pet_sub_skin_choose(skin_id)
            self.cur_skin_idx = 0
            self.skin_list = [skin_id]
            sub_skin_list = confmgr.get('c_pet_info', str(skin_id), 'sub_skin', default=[])
            self.panel.nd_top.setVisible(bool(sub_skin_list))
            self.panel.nd_down.SetContentSize(344, 418 if sub_skin_list else 634)
            self.panel.nd_down.ChildResizeAndPosition()
            if not sub_skin_list:
                self.panel.list_money.setVisible(False)
                return
            for sub_skin in sub_skin_list:
                self.skin_list.append(str(sub_skin))

            self.panel.nd_top.list_skin.SetInitCount(len(self.skin_list))
            last_skin_id = None
            last_owned = False
            for idx, sid in enumerate(self.skin_list):
                item = self.panel.nd_top.list_skin.GetItem(idx)
                own_skin = global_data.player.has_item_by_no(int(sid))
                using = cur_select_skin_id == str(sid)
                temp_card = item.temp_card
                temp_card.img_itm.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(sid))
                temp_card.lab_name.SetString(get_lobby_item_name(sid))
                temp_card.nd_lock.setVisible(not own_skin)
                check_skin_tag(temp_card.temp_level, sid)
                show_new = global_data.lobby_red_point_data.get_rp_by_no(sid)
                temp_card.img_new.setVisible(show_new)
                temp_card.bar.SetDisplayFrameByPath('', get_pet_rare_degree_pic_by_item_no(sid))
                temp_card.btn_choose.BindMethod('OnClick', lambda btn, touch, i=idx, s=sid: self.on_click_sub_skin(i, s))
                temp_card.btn_choose.SetSelect(sid == cur_select_skin_id)
                promote_price = [
                 0, 0]
                if last_skin_id:
                    promote_price = confmgr.get('c_pet_info', str(last_skin_id), 'promote_price', default=None)
                    if promote_price:
                        price_info = {'original_price': promote_price[1],'discount_price': None,
                           'goods_payment': get_item_money_type(promote_price[0])
                           }
                        init_price_template(price_info, item.temp_price, color=['#SS', '#SR', '#BC'])
                if using:
                    self.cur_skin_idx = idx
                self.refresh_btn(item, own_skin, using, last_skin_id is not None, last_owned)
                item.btn_use.BindMethod('OnClick', Functor(self.on_click_use, idx, promote_price))
                item.btn_buy.BindMethod('OnClick', Functor(self.on_click_buy, idx, promote_price))
                last_skin_id = skin_id
                last_owned = own_skin

            self.on_click_sub_skin(self.cur_skin_idx, cur_select_skin_id)
            self.panel.list_money.setVisible(bool(promote_price))
            if promote_price:
                self.panel.list_money.SetInitCount(1)
                self.promote_item = promote_price[0]
                self.refresh_money()
                money_node = self.panel.list_money.GetItem(0)

                @money_node.unique_callback()
                def OnClick(btn, touch):
                    wpos = touch.getLocation()
                    global_data.emgr.show_item_desc_ui_event.emit(self.promote_item, None, directly_world_pos=wpos)
                    return

                self.panel.list_money._refreshItemPos(is_cal_scale=True)
            return

    def refresh_money(self):
        money_node = self.panel.list_money.GetItem(0)
        money = global_data.player.get_item_num_by_no(self.promote_item)
        money_node.btn_add.setVisible(False)
        init_common_price(money_node, money, self.promote_item)

    def refresh_btn(self, item, own_skin, using, show_buy, can_buy):
        item.nd_used.setVisible(using)
        if using:
            item.btn_buy.setVisible(False)
            item.btn_use.setVisible(False)
        elif own_skin:
            item.btn_buy.setVisible(False)
            item.btn_use.setVisible(True)
        else:
            item.btn_buy.setVisible(show_buy)
            item.btn_buy.SetShowEnable(can_buy)
            item.btn_use.setVisible(False)

    def on_click_sub_skin(self, index, skin_id):
        prev_index = self.cur_skin_idx
        self.cur_skin_idx = index
        if prev_index is not None:
            prev_item = self.panel.nd_top.list_skin.GetItem(prev_index)
            if prev_item:
                prev_item.temp_card.btn_choose.SetSelect(False)
        item = self.panel.nd_top.list_skin.GetItem(index)
        if item:
            item.temp_card.btn_choose.SetSelect(True)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            global_data.player and global_data.player.req_del_item_redpoint(skin_id)
            item.temp_card.img_new.setVisible(False)
        self.parent.on_select_sub_skin(self.cur_main_skin_id, skin_id)
        skin_conf = confmgr.get('c_pet_info', str(skin_id), default={})
        add_attr_text = skin_conf.get('add_attr_text', '')
        self.panel.nd_top.lab_info.setVisible(bool(add_attr_text))
        if add_attr_text:
            add_attr = skin_conf.get('add_attr', {})
            self.panel.nd_top.lab_info.SetString(get_text_by_id(add_attr_text, add_attr))
        return

    def on_click_use(self, index, *args):
        skin_id = self.get_skin_id(index)
        if not skin_id:
            return
        global_data.player and global_data.player.set_pet_sub_skin(skin_id)

    def on_pet_sub_skin_changed(self, base_skin, sub_skin_id):
        if str(base_skin) != str(self.cur_main_skin_id):
            return
        if sub_skin_id not in self.skin_list:
            return
        index = self.skin_list.index(sub_skin_id)
        self.on_click_sub_skin(index, sub_skin_id)
        last_owned = False
        for idx, sid in enumerate(self.skin_list):
            item = self.panel.nd_top.list_skin.GetItem(idx)
            if idx == index:
                self.refresh_btn(item, True, True, idx > 0, last_owned)
            else:
                self.refresh_btn(item, global_data.player.has_item_by_no(int(sid)), False, idx > 0, last_owned)
            last_owned = global_data.player.has_item_by_no(int(sid))

    def on_click_buy(self, index, promote_price, btn, touch):
        index -= 1
        if index < 0:
            return
        if not btn.IsEnable():
            global_data.game_mgr.show_tip(608116)
            return
        promote_item, num = promote_price
        has_num = global_data.player.get_item_num_by_no(promote_item)
        if has_num < num:
            global_data.game_mgr.show_tip(860437)
            return
        skin_id = self.get_skin_id(index)
        if not skin_id:
            return
        global_data.player and global_data.player.try_upgrade_pet_skin(skin_id)

    def destroy(self):
        self.panel = None
        self.parent = None
        global_data.emgr.pet_skin_promoted -= self.on_pet_skin_promoted
        global_data.emgr.pet_sub_skin_changed -= self.on_pet_sub_skin_changed
        return

    def get_skin_id(self, index=None):
        if index is None:
            index = self.cur_skin_idx
        if not self.skin_list or index >= len(self.skin_list):
            return
        else:
            return self.skin_list[index]

    def on_pet_skin_promoted(self, *args):
        last_owned = False
        for idx, sid in enumerate(self.skin_list):
            item = self.panel.nd_top.list_skin.GetItem(idx)
            item.temp_card.nd_lock.setVisible(not bool(global_data.player.has_item_by_no(int(sid))))
            item.temp_card.img_new.setVisible(global_data.lobby_red_point_data.get_rp_by_no(sid))
            if idx == self.cur_skin_idx:
                self.refresh_btn(item, True, True, idx > 0, last_owned)
            else:
                self.refresh_btn(item, global_data.player.has_item_by_no(int(sid)), False, idx > 0, last_owned)
            last_owned = global_data.player.has_item_by_no(int(sid))

        self.refresh_money()