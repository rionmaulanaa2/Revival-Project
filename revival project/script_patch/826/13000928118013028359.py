# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayRecommendWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from functools import cmp_to_key
from logic.comsys.mall_ui.MallDisplayItemListWidget import MallDisplayItemListWidget
from common.cfg import confmgr
from logic.gutils.mall_utils import recommend_cmp
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.gcommon.common_const.log_const import RECOMMEND_ITEM_STATE_OPEN, RECOMMEND_ITEM_STATE_CLICK_ITEM

class MallDisplayRecommendWidget(MallDisplayItemListWidget):

    def init_parameters(self):
        super(MallDisplayRecommendWidget, self).init_parameters()
        self._sort_cmp = lambda a, b: recommend_cmp(a, b)
        self._default_banner_index = 0
        self._select_goods_id = 0
        self._mall_banner_widget = None
        self._focus_banner = False
        self._is_show_widget = False
        self._gift_switch_index = -1
        self._select_goods_cb = {}
        self.recommend_log_lst = []
        self._is_disconnected = False
        return

    def on_finalize_panel(self):
        super(MallDisplayRecommendWidget, self).on_finalize_panel()
        if self._mall_banner_widget:
            self._mall_banner_widget.destroy()
        self._mall_banner_widget = None
        list_sort = self.panel.mall_recommend_common_list
        for i in range(list_sort.GetItemCount()):
            item_widget = list_sort.GetItem(i)
            mall_new = getattr(item_widget, 'mall_new', None)
            if mall_new:
                mall_new.setVisible(False)

        player = global_data.player
        if player:
            player.cache_buy_recommend_goods = None
        return

    def do_hide_panel(self):
        self._is_show_widget = False

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self._on_player_info_update,
           'net_disconnect_event': self.on_disconnect,
           'net_reconnect_event': self.on_reconnect,
           'net_login_reconnect_event': self.on_reconnect,
           'mall_new_recommendation_update': self._on_mall_new_recommendation_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_disconnect(self):
        self._is_disconnected = True

    def on_reconnect(self):
        self._is_disconnected = False

    def jump_to_goods_id(self, goods_id):
        if not goods_id:
            return
        banner_items = mall_utils.get_recommend_banner_list()
        if goods_id in banner_items:
            index = banner_items.index(goods_id)
            self._default_banner_index = index
            self._mall_banner_widget and self._mall_banner_widget.select_good(self._default_banner_index)
            return
        items = self.get_mall_items()
        if not items or goods_id not in items:
            return
        self._default_banner_index = -1
        small_items = self.get_mall_items(exception=mall_utils.get_recommend_banner_list())
        index = small_items.index(goods_id)
        self.scroll_to_small_item(index)

    def init_widget(self):
        self.init_buy_confirm()
        self.init_display()
        self.init_switch_detail()
        self.init_switch_gift_view()

    def init_switch_detail(self):

        @self.panel.btn_check.unique_callback()
        def OnClick(btn, touch):
            _, show_goods_id = mall_utils.get_goods_item_show_info(self.select_goods_id, self._gift_switch_index)
            mall_utils.mall_switch_detail(show_goods_id)

    def _check_show_video_btn(self, goods_id):
        from common.platform.dctool import interface
        flag = not interface.is_mainland_package() and (goods_id.startswith('2018010') or goods_id == '101008010')
        self.panel.nd_show_video.setVisible(flag)
        if flag:

            @self.panel.nd_show_video.btn_show_video.unique_callback()
            def OnClick(*args):
                from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_JA
                language = get_cur_text_lang()
                if language == LANG_CN or language == LANG_ZHTW:
                    url = 'https://www.youtube.com/watch?v=NAN5YkTHkT8'
                elif language == LANG_JA:
                    url = 'https://www.youtube.com/watch?v=1nZODb_Waq8'
                else:
                    url = 'https://www.youtube.com/watch?v=HYD6J4_TRkQ'
                import game3d
                game3d.open_url(url)

    def init_switch_gift_view(self):

        @self.panel.btn_change.unique_callback()
        def OnClick(btn, touch):
            self._mall_banner_widget and self._mall_banner_widget.reset_time_count()
            self._gift_switch_index += 1
            show_item_no, show_goods_id = mall_utils.get_goods_item_show_info(self.select_goods_id, self._gift_switch_index)
            model_data = lobby_model_display_utils.get_lobby_model_data(show_item_no)
            if model_data:
                mall_utils.show_model_display_scene(show_goods_id)
                self._check_show_video_btn(show_goods_id)
                self.ext_show_item_model(model_data, show_goods_id, show_item_no)
            else:
                self.ext_not_show_no_model()
            self.refresh_detail_btn()
            _, next_show_goods_id = mall_utils.get_goods_item_show_info(self.select_goods_id, self._gift_switch_index + 1)
            self.panel.lab_change.SetString(3108)

    def scroll_to_small_item(self, index, off_set=None):
        mall_list = self.panel.mall_recommend_common_list
        items = self.get_mall_items()
        index = min(index, len(items) - 1)
        if not off_set:
            mall_list.LocatePosByItem(index)
        else:
            mall_list.SetContentOffset(off_set)
        select_widget = mall_list.GetItem(index)
        if select_widget is None:
            select_widget = mall_list.DoLoadItem(index)
        select_widget and select_widget.bar.OnClick(None)
        return

    def select_goods(self, good_id):
        if good_id in self._select_goods_cb:
            self._select_goods_cb[good_id]()

    def set_touch_widget(self, item_widget, good_id):
        item_no = mall_utils.get_goods_item_no(good_id)
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)

        @item_widget.bar.unique_callback()
        def OnClick(btn, touch, item_widget=item_widget, good_id=good_id, model_data=model_data, item_id=item_no):
            if good_id is None:
                return
            else:
                self.panel.nd_change.setVisible(False)
                player = global_data.player
                if player and self._select_goods_id != good_id:
                    player.sa_log_recommend_item(RECOMMEND_ITEM_STATE_CLICK_ITEM, item_id=int(good_id))
                if model_data:
                    self._select_product(item_widget, good_id)
                    mall_utils.show_model_display_scene(good_id)
                    self._check_show_video_btn(good_id)
                    self.ext_show_item_model(model_data, good_id, item_id)
                else:
                    groceries_buy_confirmUI(good_id)
                self._mall_banner_widget and self._mall_banner_widget.set_focus(False)
                self._select_goods_id = good_id
                mall_utils.read_recommendation(good_id)
                return

        def callback():
            item_widget and item_widget.bar.OnClick(None)
            return

        self._select_goods_cb[good_id] = callback

    def set_touch_banner(self):

        def callback(item_widget, goods_id, is_click=False):
            if self._is_disconnected:
                return
            if self._seleted_mall_widget == item_widget and not is_click:
                return

            def do_callback(goods_id=goods_id, item_widget=item_widget, is_click=is_click):
                self._gift_switch_index = -1
                show_item_no, show_goods_id = mall_utils.get_goods_item_show_info(goods_id)
                model_data = lobby_model_display_utils.get_lobby_model_data(show_item_no)
                show_switch_btn = str(show_goods_id) != str(goods_id)
                self.panel.nd_change.setVisible(show_switch_btn)
                if show_switch_btn:
                    _, next_show_goods_id = mall_utils.get_goods_item_show_info(goods_id, self._gift_switch_index + 1)
                    self.panel.lab_change.SetString(3108)
                if model_data:
                    self._select_product(item_widget, goods_id)
                    if self._is_show_widget:
                        mall_utils.show_model_display_scene(show_goods_id)
                        self._check_show_video_btn(show_goods_id)
                        self.ext_show_item_model(model_data, show_goods_id, show_item_no)
                elif is_click:
                    groceries_buy_confirmUI(goods_id)
                self._mall_banner_widget and self._mall_banner_widget.set_focus(True)
                self._select_goods_id = goods_id

            self._select_goods_cb[goods_id] = do_callback
            do_callback()

        self._mall_banner_widget.set_switch_callback(callback)

    def _on_mall_new_recommendation_update(self):
        self._refresh_all_item_new_icon()

    def _refresh_all_item_new_icon(self, item_list=None):
        small_items = item_list or self.get_mall_items(exception=mall_utils.get_recommend_banner_list())
        list_sort = self.panel.mall_recommend_common_list
        for i, goods_id in enumerate(small_items):
            item_widget = list_sort.GetItem(i)
            self._refresh_item_new_icon(item_widget, goods_id)

    def _refresh_item_new_icon(self, item_widget, goods_id):
        if not getattr(item_widget, 'mall_new', None):
            return
        else:
            has_new = mall_utils.should_recommendation_marked_as_new(goods_id)
            item_widget.mall_new.setVisible(has_new)
            if has_new:
                item_widget.mall_new.PlayAnimation('show')
            else:
                item_widget.mall_new.StopAnimation('show')
            return

    def init_mall_list(self, page_index, sub_page_index=None):
        from logic.comsys.mall_ui.MallBannerWidget import MallBannerWidget
        self._cur_page_index = page_index
        self._cur_sub_page_index = sub_page_index
        self._mall_banner_widget = MallBannerWidget(self.panel.nd_recommend_main)
        self.set_touch_banner()
        small_items = self.get_mall_items(exception=mall_utils.get_recommend_banner_list())
        count = len(small_items)
        list_sort = self.panel.mall_recommend_common_list
        list_sort.SetInitCount(count)
        for i, good_id in enumerate(small_items):
            item_widget = list_sort.GetItem(i)
            if not getattr(item_widget, 'mall_new', None):
                item_widget.mall_new = template_utils.create_and_init_mall_new_icon(item_widget.img_red, 'mall_new')
            template_utils.init_mall_recommend_item2(item_widget, good_id)
            self._refresh_item_new_icon(item_widget, good_id)
            self.set_touch_widget(item_widget, good_id)

        self.reset_mall_list(is_init=True)
        player = global_data.player
        if player:
            new_log_lst = [ int(i) for i in small_items ]
            self.recommend_log_lst = new_log_lst
            player.sa_log_recommend_item(RECOMMEND_ITEM_STATE_OPEN, show_item_list=new_log_lst)
        return

    def reset_mall_list(self, is_init=True):
        self._is_show_widget = True
        self.update_mall_list()
        if int(self._select_goods_id) > 0:
            self.select_goods(self._select_goods_id)
            return
        if self._default_banner_index >= 0:
            self._mall_banner_widget and self._mall_banner_widget.select_good(self._default_banner_index)
            return

    def update_mall_list(self):
        self._mall_banner_widget and self._mall_banner_widget.update_list()
        small_items = self.get_mall_items(exception=mall_utils.get_recommend_banner_list())
        list_sort = self.panel.mall_recommend_common_list
        for i, good_id in enumerate(small_items):
            item_widget = list_sort.GetItem(i)
            template_utils.init_mall_recommend_item2(item_widget, good_id)
            self._refresh_item_new_icon(item_widget, good_id)

    def _select_product(self, mall_widget, goods_id):
        super(MallDisplayRecommendWidget, self).selete_product(mall_widget, goods_id)
        self.show_buy_tips()

    def refresh_detail_btn(self):
        btn_check = self.panel.btn_check
        if not btn_check:
            return
        _, show_goods_id = mall_utils.get_goods_item_show_info(self.select_goods_id, self._gift_switch_index)
        btn_check.setVisible(mall_utils.has_detail_info(show_goods_id))

    def show_buy_tips(self):
        temp_buy_tips = self.panel.temp_buy_tips
        if not temp_buy_tips:
            return
        data = confmgr.get('mall_recommend_conf', str(self.select_goods_id))
        show = False
        if data:
            iTipsID = data.get('iTipsID')
            if iTipsID:
                show = True
                temp_buy_tips.lab_tips.SetString(get_text_by_id(iTipsID))
        temp_buy_tips.setVisible(show)

    def get_mall_items(self, exception=()):
        from logic.gcommon import time_utility
        valid_func = lambda x: mall_utils.is_valid_goods(x) and x not in exception
        ret_items = []
        player = global_data.player
        if player:
            recommend_info = player.get_recommend_shop_list()
            for key in ('mecha', 'mecha_skin', 'role', 'role_skin'):
                sub_info = recommend_info.get(key)
                if not sub_info:
                    continue
                if isinstance(sub_info, int):
                    ret_items.append(sub_info)
                else:
                    ret_items.extend(sub_info)

            ret_items = [ str(item_id) for item_id in ret_items if valid_func(str(item_id)) ]
        top_recommend = []
        other_recommed = []
        items = []
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        if self._cur_sub_page_index is not None:
            items = item_page_conf.get(self._cur_sub_page_index, [])
        else:
            for sub_page_conf in six.itervalues(item_page_conf):
                items.extend(sub_page_conf)

        for goods_id in items:
            if goods_id in exception:
                continue
            if not mall_utils.is_good_opened(goods_id):
                continue
            recommend_conf = confmgr.get('mall_recommend_conf', goods_id, default={})
            if recommend_conf and recommend_conf.get('cNeedNewHint'):
                open_dates = recommend_conf.get('open_timestamp')
                if open_dates and not time_utility.check_in_time_range((open_dates,)):
                    top_recommend.append(goods_id)
                else:
                    other_recommed.append(goods_id)
            else:
                other_recommed.append(goods_id)

        top_recommend = sorted(top_recommend, key=cmp_to_key(self._sort_cmp))
        temp_list = []
        for i in top_recommend:
            if i not in temp_list:
                temp_list.append(i)

        top_recommend = temp_list
        if len(top_recommend) < 4:
            top_recommend.extend(sorted(other_recommed, key=cmp_to_key(self._sort_cmp)))
            temp_list = []
            for i in top_recommend:
                if i not in temp_list:
                    temp_list.append(i)

            top_recommend = temp_list
        ret_items.extend(top_recommend)
        ret_items.extend(other_recommed)
        return ret_items[:4]

    def buy_goods(self):
        player = global_data.player
        if player and int(self.select_goods_id) in self.recommend_log_lst:
            player.cache_buy_recommend_goods = self.select_goods_id
        super(MallDisplayRecommendWidget, self).buy_goods()