# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplaySkinDefineWidget.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from logic.client.const import mall_const
from logic.gutils import lobby_model_display_utils
from logic.gutils import jump_to_ui_utils
from logic.gutils import mall_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gutils import dress_utils
from ext_package.ext_decorator import has_skin_ext
ROTATE_FACTOR = 850
MIN_LIST_NUM = 6
LOOP_TAG = 200824

class MallDisplaySkinDefineWidget(object):

    def __init__(self, dlg):
        self.panel = dlg
        self.init_parameters()
        self.init_event()
        self.init_widget()
        self.panel.PlayAnimation('appear')

        def func():
            self.panel.PlayAnimation('loop')

        self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('appear'), lambda : func())

    def on_finalize_panel(self):
        self.process_event(False)
        player = global_data.player
        if player:
            player.cache_buy_recommend_collocation_goods = []

    def set_show(self, show):
        self.panel.setVisible(show)
        if show:
            self.choose_recommend_index(self._collocation_index)

    def do_show_panel(self):
        self.init_display()

    def do_hide_panel(self):
        self.stop_loop_action()

    def init_parameters(self):
        self._rec_collocation = mall_utils.get_recommend_collocation_conf()
        self._collocation_index = 0
        self.goods_price_infos = {}

    def init_event(self):
        self.process_event(True)
        self.panel.btn_item_bar.BindMethod('OnClick', self.on_click_all_skin_define)
        self.panel.temp_btn_buy.btn_major.BindMethod('OnClick', self.on_click_buy_this_set)

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        @self.panel.nd_touch_whole.unique_callback()
        def OnBegin(btn, touch):
            self.stop_loop_action()
            return True

        @self.panel.nd_touch_whole.unique_callback()
        def OnEnd(btn, touch):
            self.set_loop_action()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self._on_player_info_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self.init_recommend_list_show()

    def init_display(self):
        self.choose_recommend_index(self._collocation_index)

    def _on_player_info_update(self, *args):
        pass

    def init_recommend_list_show(self):
        self._coll_node_list = [
         self.panel.btn_recommend_1, self.panel.btn_recommend_2, self.panel.btn_recommend_3]
        self._coll_red_node_list = [self.panel.temp_red_1, self.panel.temp_red_2, self.panel.temp_red_3]

        def click_fun(ind):
            dec_set = self._rec_collocation[ind]
            mall_utils.remove_dec_set_recommend_red_point(dec_set)
            red_node = self._coll_red_node_list[ind]
            red_node.setVisible(False)
            self.choose_recommend_index(ind)

        for ind, node in enumerate(self._coll_node_list):
            node.BindMethod('OnClick', lambda btn, touch, ind=ind: click_fun(ind))

        global_data.player and global_data.player.sa_log_recommend_collocation_open()

    def set_loop_action(self):
        import cc
        self.panel.stopActionByTag(LOOP_TAG)
        action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(10),
         cc.CallFunc.create(self.on_goto_next)])))
        action.setTag(LOOP_TAG)

    def stop_loop_action(self):
        self.panel.stopActionByTag(LOOP_TAG)

    def on_goto_next(self):
        if self.panel.IsVisible():
            self.choose_recommend_index((self._collocation_index + 1) % len(self._coll_node_list))

    def choose_recommend_index(self, index):
        old_btn_node = self._coll_node_list[self._collocation_index]
        old_btn_node.SetSelect(False)
        self._collocation_index = index
        btn_node = self._coll_node_list[self._collocation_index]
        btn_node.SetSelect(True)
        self.cal_show_preview_info()
        self.show_recommend_collocation()
        self.set_loop_action()
        self.check_status()

    def cal_show_preview_info(self):
        self._all_set_item_no = self._rec_collocation[self._collocation_index][1]
        self._top_skin_id = self._rec_collocation[self._collocation_index][0]
        self._preview_skin = self._top_skin_id

    def show_recommend_collocation(self):
        self.refresh_relatived_scene(self._preview_skin)
        if has_skin_ext():
            self.panel.lab_ext.setVisible(False)
            model_data = self.get_preview_model_data(self._top_skin_id, self._all_set_item_no)
            global_data.emgr.change_model_display_scene_item.emit(model_data)
        else:
            global_data.emgr.change_model_display_scene_item.emit(None)
            self.panel.lab_ext.setVisible(True)
            self.panel.lab_ext.SetString(344)
        return

    def refresh_relatived_scene(self, preview_skin):
        from logic.gcommon.common_const import scene_const
        from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_DISPLAY_PIC, DEFAULT_LEFT_NEAR, DEFAULT_LEFT, DEFAULT_RIGHT
        display_type = DEFAULT_RIGHT
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, str(display_type), scene_content_type=scene_const.SCENE_MALL)

    def get_preview_model_data(self, top_skin_id, all_preview_list):
        fashion_dict = dress_utils.collocation_list_to_fashion_dict(all_preview_list)
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
        skin_id = fashion_dict.get(FASHION_POS_SUIT) or top_skin_id
        role_id = item_utils.get_lobby_item_belong_no(skin_id)
        item_no = dress_utils.get_role_item_no(role_id, skin_id)
        if skin_id is not None:
            head_id = fashion_dict.get(FASHION_POS_HEADWEAR)
            bag_id = fashion_dict.get(FASHION_POS_BACK)
            suit_id = fashion_dict.get(FASHION_POS_SUIT_2)
            other_pendants = [ fashion_dict.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
            model_data = lobby_model_display_utils.get_lobby_model_data(item_no, skin_id=skin_id, head_id=head_id, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
            return model_data
        else:
            return

    def init_mall_list(self, page_index, sub_page_index=None):
        self._cur_page_index = page_index
        self._cur_sub_page_index = sub_page_index
        goods_items = []
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        if self._cur_sub_page_index is not None:
            goods_items = item_page_conf.get(self._cur_sub_page_index, [])
        else:
            for sub_page_conf in six.itervalues(item_page_conf):
                goods_items.extend(sub_page_conf)

        self.goods_price_infos = {}
        cur_host_num = global_data.channel.get_host_num()
        self.alter_goods_info = {}
        for goods_id in goods_items:
            goods_conf = confmgr.get('mall_config', str(goods_id), default={})
            open_hosts = goods_conf.get('open_hosts', [])
            alter_cond = goods_conf.get('alter_cond')
            if open_hosts and cur_host_num not in open_hosts:
                continue
            if alter_cond:
                self.alter_goods_info[goods_id] = alter_cond
                continue
            self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

        self.reset_mall_list(is_init=True)
        return

    def alter_goods_price_info(self):
        for goods_id, conf in six.iteritems(self.alter_goods_info):
            cond_func = conf.get('func')
            param = conf.get('param')
            alter_goods_id = conf.get('alter_goods')
            if alter_goods_id not in self.goods_price_infos:
                continue
            cond_func = getattr(mall_utils, cond_func)
            if cond_func(**param):
                self.goods_price_infos.pop(alter_goods_id)
                self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

    def reset_mall_list(self, is_init=False):
        self.alter_goods_price_info()
        self.goods_items = self.get_mall_items()
        show_count = len(self.goods_items)
        for index, goods_id in enumerate(self.goods_items):
            btn_box = getattr(self.panel, 'btn_box_%s' % (index + 1))
            if btn_box:
                self.init_goods_ui_item(index, btn_box)

        self.refresh_rp()

    def init_goods_ui_item(self, index, item_widget):
        goods_id = self.goods_items[index]
        extra_info = {}
        self.init_mall_item(item_widget, goods_id, is_show_kind=False, extra_info=extra_info)
        limite_by_day, _, _ = mall_utils.buy_num_limite_by_day(goods_id)
        limite_by_week, _, _ = mall_utils.buy_num_limite_by_week(goods_id)
        price_list = self.goods_price_infos.get(goods_id)
        item_widget.lab_free.setVisible(False)
        for price in price_list:
            if price.get('real_price', None) == 0:
                item_widget.lab_free.setVisible(True)

        if not (limite_by_day or limite_by_week):
            self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('appear'), lambda : item_widget.PlayAnimation('loop'))
        else:
            item_widget.StopAnimation('loop')
        item_widget.nd_sold_out.setVisible(limite_by_day or limite_by_week)
        if goods_id is None:
            item_widget.SetEnable(False)
        else:
            item_widget.SetEnable(True)

            @item_widget.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id):
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    return
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(goods_id)

        return

    def init_mall_item(self, item_widget, goods_id, is_show_kind=True, extra_info=None):
        from logic.gutils.template_utils import init_price_view, show_remain_time
        from logic.gutils import mall_utils
        from logic.gcommon import time_utility
        item_widget.img_price.setVisible(not mall_utils.item_has_owned_by_goods_id(goods_id))
        money_icon_scale = extra_info or None if 1 else extra_info.get('money_icon_scale', None)
        init_price_view(item_widget.temp_price, goods_id, color=mall_const.NO_RED_PRICE_COLOR, money_icon_scale=money_icon_scale)
        item_widget.img_box.SetDisplayFrameByPath('', mall_utils.get_goods_pic_path(goods_id))
        item_widget.lab_name.SetString(mall_utils.get_goods_name(goods_id))
        item_widget.temp_red and item_widget.temp_red.setVisible(goods_id in mall_utils.get_red_point_goods_id())
        limite_by_day, _, _ = mall_utils.buy_num_limite_by_day(goods_id)
        limite_by_week, _, _ = mall_utils.buy_num_limite_by_week(goods_id)
        item_widget.nd_sold_out.setVisible(limite_by_day or limite_by_week)
        if goods_id is None:
            item_widget.SetEnable(False)
        else:
            item_widget.SetEnable(True)

            @item_widget.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id):
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    return
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(goods_id)

        return

    def get_mall_items(self):
        items = six_ex.keys(self.goods_price_infos)

        def my_cmp(x, y):
            item_no_x = mall_utils.get_goods_item_no(x)
            item_no_y = mall_utils.get_goods_item_no(y)
            sort_key_x = item_utils.get_lobby_item_sort_key(item_no_x)
            sort_key_y = item_utils.get_lobby_item_sort_key(item_no_y)
            if sort_key_x == sort_key_y:
                return six_ex.compare(item_no_x, item_no_y)
            return six_ex.compare(sort_key_y, sort_key_x)

        items.sort(key=cmp_to_key(my_cmp))
        LAST_GOOD = '50500067'
        if LAST_GOOD in items:
            items.remove(LAST_GOOD)
            items.append(LAST_GOOD)
        return items

    def check_status(self):
        self.update_money_type()
        own_list, no_own_list, can_buy_list, no_can_buy_list = dress_utils.get_item_no_list_buy_info(self._all_set_item_no)
        if not can_buy_list:
            self.panel.temp_btn_buy.btn_major.SetText(81801)
            self.panel.temp_btn_buy.btn_major.SetEnable(False)
        else:
            self.panel.temp_btn_buy.btn_major.SetText(81777)
            self.panel.temp_btn_buy.btn_major.SetEnable(True)
        role_name = item_utils.get_lobby_item_belong_name(self._preview_skin)
        skin_name = item_utils.get_lobby_item_name(self._preview_skin)
        self.panel.lab_name.SetString(get_text_by_id(81778, {'role_name': role_name,'skin_name': skin_name}))

    def update_money_type(self):
        new_money_types_list = dress_utils.get_fashion_unowned_money_type(self._all_set_item_no)
        mall_main_ui = global_data.ui_mgr.get_ui('MallMainUI')
        if mall_main_ui:
            mall_main_ui.set_mall_main_show_money_type(new_money_types_list)

    def on_click_all_skin_define(self, btn, touch):
        from logic.comsys.mall_ui.RoleSkinDecorationStoreUI import RoleSkinDecorationStoreUI
        RoleSkinDecorationStoreUI()

    def on_click_buy_this_set(self, btn, touch):
        belong_no = item_utils.get_lobby_item_belong_no(self._preview_skin)
        role_item_data = global_data.player.get_item_by_no(belong_no)
        has_role = role_item_data is not None
        if not has_role:

            def confirm_callback():
                jump_to_ui_utils.jump_to_display_detail_by_item_no(belong_no)
                role_ui = global_data.ui_mgr.get_ui('RoleInfoUI')
                if role_ui:
                    role_ui.click_buy_btn()

            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(title=get_text_by_id(867008), content=get_text_by_id(80967), confirm_callback=confirm_callback)
            return
        else:
            from logic.comsys.common_ui.CommonBuyListUI import CommonBuyListUI
            all_item_list = list(self._all_set_item_no)
            if self._preview_skin not in all_item_list:
                all_item_list.append(self._preview_skin)
            own_list, no_own_list, can_buy_list, no_can_buy_list = dress_utils.get_item_no_list_buy_info(all_item_list)
            show_buy_item_data_list = []
            if no_own_list:
                for item_no in no_own_list:
                    show_buy_item_data_list.append({'item_no': item_no,'quantity': 1})

            if show_buy_item_data_list:
                ui = CommonBuyListUI()
                if ui:
                    ui.init_buy_list_item(show_buy_item_data_list)
                player = global_data.player
                if player and all_item_list:
                    player.cache_buy_recommend_collocation_goods = [ dress_utils.get_goods_id_of_role_dress_related_item_no(item_no) for item_no in all_item_list ]
            return

    def check_dec_set_recommend_red_point(self, coll_index):
        return False

    def refresh_rp(self):
        self.panel.btn_item_bar.img_new.setVisible(mall_utils.has_unseen_new_arrivals(self._cur_page_index, self._cur_sub_page_index))
        for ind, _ in enumerate(self._coll_node_list):
            need_red = self.check_dec_set_recommend_red_point(ind)
            red_node = self._coll_red_node_list[ind]
            red_node.setVisible(need_red)