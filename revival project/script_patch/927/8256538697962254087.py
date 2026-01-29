# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/Lottery2024SpringArtCollectionWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryNewPreviewWidget import LotteryNewPreviewWidget
from .LotteryShopWidget import LotteryShopWidget
from .LotteryBuyWidget import LotteryBuyWidget
from logic.gutils.item_utils import check_skin_tag, get_lobby_item_name, get_item_rare_degree, get_lobby_item_belong_name, check_is_improvable_skin, REWARD_RARE_COLOR, update_limit_btn, check_is_improvable_splus_mecha_skin, check_is_improvable_sp_mecha_skin
from logic.gutils.mall_utils import get_lottery_exchange_list, get_cur_lottery_state, remind_second_confirm_lottery_goods, init_reward_pool_template, all_half_price_art_collection_lottery_valid, get_special_price_info_for_half_art_collection_single_lottery, special_buy_logic_for_half_art_collection_single_lottery
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.item.item_const import RARE_DEGREE_5
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.comsys.lobby.EntryWidget.ArtCollectionActivityEntryWidget import ArtCollectionActivityEntryWidget
from common.utils.timer import CLOCK
import time
import cc
from logic.client.const.mall_const import LOTTERY_ST_OPEN_ONLY_EXCHANGE, SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from .LotteryExchangeRewardWidget import LotteryExchangeRewardWidget
from logic.gutils import mall_utils
import six
from logic.client.const.mall_const import DARK_PRICE_COLOR, USE_TEMPLATE_COLOR
BANNER_SCROLL_INTERVAL = 4.0
BANNER_TEX_PATH = 'gui/ui_res_2/lottery/img_ss_banner_%d.png'
DEFAULT_BANNER_TEX_PATH = 'gui/ui_res_2/lottery/img_ss_banner_201800251.png'
PROGRESS_TEXTURE_PATH = 'gui/ui_res_2/common/progress/blue_progress.png'
DEFAULT_ICON_PATH = 'gui/ui_res_2/lottery/icon_lottery_gift.png'
DEFAULT_TXT_COLOR = 16776169
DEFAULT_OUT_LINE = 9048633

class Lottery2024SpriteNewPreviewWidget(LotteryNewPreviewWidget):
    ITEM_TEMPLATE = 'mall/i_collection_activity/spring_lottery_2024/i_ss_lottery_review_list_group_item_spring2024'
    TITLE_TEMPLATE = 'mall/i_collection_activity/spring_lottery_2024/i_spring2024_ss_lottery_review_list_title'


class Lottery2024SpringExchangeRewardWidget(LotteryExchangeRewardWidget):

    def tab_click_cb(self, item, idx):
        super(Lottery2024SpringExchangeRewardWidget, self).tab_click_cb(item, idx)
        fir_item = self.panel.list_tab.GetItem(0)
        sec_item = self.panel.list_tab.GetItem(1)
        if idx == 0:
            sec_item and sec_item.PlayAnimation('loop')
            fir_item and fir_item.StopAnimation('loop')
        elif idx == 1:
            sec_item and sec_item.StopAnimation('loop')
            fir_item and fir_item.PlayAnimation('loop')
        else:
            sec_item and sec_item.PlayAnimation('loop')
            fir_item and fir_item.PlayAnimation('loop')


class Lottery2024SpringArtCollectionWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(Lottery2024SpringArtCollectionWidget, self).init_parameters()
        self.preview_widget = None
        self.main_buy_widget = None
        self._item_id_2_ui_item = {}
        self.limit_time_lottery_count_down = 0
        self.limit_time_lottery_timer = None
        self.selected_banner_index = 0
        banner_id_list = self.data.get('banner_id_list', [])
        self.show_model_id = banner_id_list[0] if banner_id_list else None
        self.flash_anim_banner_list = []
        for banner_id in banner_id_list:
            rare_degree = get_item_rare_degree(banner_id, ignore_imporve=True)
            if rare_degree == RARE_DEGREE_5:
                self.flash_anim_banner_list.append(banner_id)

        self.is_visible_close = False
        conf = confmgr.get('lottery_page_config', default={})
        self.max_lottery_count = conf[self.lottery_id].get('day_limit', 0)
        self.activity_type = conf[self.lottery_id].get('activity_type')
        self.single_goods_id = conf[self.lottery_id].get('single_goods_id')
        self.visible_ts = conf[self.lottery_id].get('visible_ts')
        self.exchange_reward_tab_list = conf[self.lottery_id].get('extra_data', {}).get('exchange_reward_tab_list', [])
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        self.half_price_lottery_valid = all_half_price_art_collection_lottery_valid(self.lottery_id)
        self.tips_anim_timer = None
        self._activity_list_map = {}
        return

    def init_panel(self):
        super(Lottery2024SpringArtCollectionWidget, self).init_panel()
        self._list_sview = None
        self.panel.btn_shop.EnableCustomState(False)
        self.panel.lab_free_time.setVisible(False)
        self.panel.nd_review.setVisible(False)
        extra_data = self.data.get('extra_data', {})
        icon_path = extra_data.get('icon_path', DEFAULT_ICON_PATH) if extra_data else DEFAULT_ICON_PATH
        txt_color = eval(extra_data.get('text_color', DEFAULT_TXT_COLOR)) if extra_data else DEFAULT_TXT_COLOR
        out_line = eval(extra_data.get('out_line', DEFAULT_OUT_LINE)) if extra_data else DEFAULT_OUT_LINE
        act_txt_id = extra_data.get('act_text_id', None)
        shop_txt_id = extra_data.get('shop_text_id', None)
        gift_tip_txt_id = extra_data.get('gift_tip_text_id', None)
        self.panel.btn_activity.SetFrames('', [icon_path, icon_path, icon_path], False, None)
        self.panel.lab_btn_text.SetColor(txt_color)
        act_txt_id and self.panel.lab_btn_text.SetString(act_txt_id)
        shop_txt_id and self.panel.btn_shop.lab_shop_title.SetString(shop_txt_id)
        gift_tip_txt_id and self.panel.lab_tips_activity.SetString(gift_tip_txt_id)

        @global_unique_click(self.panel.temp_main.btn_describe)
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, content = self.data.get('rule_desc', [608080, 608081])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.temp_main.btn_change)
        def OnClick(*args):
            self.preview_widget.show()
            self.preview_widget.jump_to_preview_rare_degree(RARE_DEGREE_5)

        @global_unique_click(self.panel.temp_btn_close.btn_back)
        def OnClick(*args):
            self.preview_widget.hide()

        @global_unique_click(self.panel.btn_shop)
        def OnClick(btn, touch):
            if not self.exchange_reward_widget:
                self._init_exchange_reward_widget()
            self.exchange_reward_widget.visible = True

        @global_unique_click(self.panel.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        self.exchange_reward_widget = None
        self._init_buy_widget()
        self._init_preview_widget()
        self._init_rule_tag_list()
        self._init_main_widget()
        if self.panel.lab_tips:
            self.panel.lab_tips.setVisible(True)
            txt_id = self.data.get('show_tip')
            txt = ''
            if txt_id:
                txt = get_text_by_id(txt_id)
            self.panel.lab_tips.SetString(txt)
        self.init_temporary_activity_entrance()
        self.init_extra_activity_entrance()
        self.refresh_10_try_entrance()
        self.check_show_shop()
        self.update_half_price_lottery_tips()
        return

    def jump_to_exchange_shop_widget(self, goods_id, check=True):
        if not self.exchange_reward_widget:
            self._init_exchange_reward_widget()
        if not self.exchange_reward_widget:
            return
        exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
        if self.lottery_id not in lottery_exchange_goods:
            global_data.game_mgr.show_tip(get_text_by_id(12128))
            return
        if not check or self.panel.mall_box_buy.isVisible() or get_cur_lottery_state(self.single_goods_id, self.visible_ts) == LOTTERY_ST_OPEN_ONLY_EXCHANGE:
            self.exchange_reward_widget.set_show_goods_id(goods_id)
            self.exchange_reward_widget.visible = True

    def set_visible_close(self, is_visible_close):
        self.is_visible_close = is_visible_close

    def check_show_shop(self):
        if self.is_visible_close and self.data.get('show_shop', False):
            self.panel.nd_granbelm.setVisible(False)
            self.panel.nd_shop.btn_close.setVisible(False)
            return True
        return False

    def init_temporary_activity_entrance(self):
        self.activity_button_widget = ArtCollectionActivityEntryWidget(self.panel, self.panel, self.data.get('activity_type'), self.data.get('remind_jump_ui')[0], self.data.get('remind_jump_ui')[1])

    def init_extra_activity_entrance(self):
        extra_data = self.data.get('extra_data', {})
        joint_btn_info = extra_data.get('joint_btn', {})
        if joint_btn_info:
            self.panel.btn_extral_gift.setVisible(True)

            @global_unique_click(self.panel.btn_extral_gift)
            def OnClick(*args):
                func_name = joint_btn_info.get('func')
                func_args = joint_btn_info.get('args', [])
                if func_name:
                    from logic.gutils import jump_to_ui_utils
                    func = getattr(jump_to_ui_utils, func_name)
                    func and func(*func_args)

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,'refresh_lottery_limited_guarantee_round': self._init_rule_tag_list,
           'lottery_open_box_result': self._on_lottery_open_box_result,
           'lottery_ten_try_update': self.refresh_10_try_entrance
           }
        return econf

    def get_banner_id_index(self, banner_id):
        banner_id_list = self.data.get('banner_id_list', [])
        for index, one_banner_id in enumerate(banner_id_list):
            if one_banner_id == banner_id:
                return index

        return 0

    def _load_banner(self):
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self._list_sview = InfiniteScrollWidget(self.panel.list_banner, self.panel, up_limit=10000, down_limit=10000)
        self._list_sview.set_template_init_callback(self.update_one_banner)
        banner_id_list = self.data.get('banner_id_list', [])
        data_list = []
        for index, banner_id in enumerate(banner_id_list):
            one_data = (
             banner_id, index)
            data_list.append(one_data)

        self._list_sview.update_data_list(data_list)
        self._list_sview.update_scroll_view()
        self._list_sview.set_require_data_callback(self.request_members_data)
        return

    def request_members_data(self):
        pass

    def update_one_banner(self, nd_banner, data):
        banner_id, index = data
        update_limit_btn(banner_id, nd_banner.temp_limit, nd_banner.temp_limit.nd_limit_describe, clip_object=self.panel.list_banner, is_corner=True, from_part='lottery')

        @global_unique_click(nd_banner.btn_banner)
        def OnClick(*args):
            self.select_banner(index)

        item_id = banner_id
        multiple = self.data.get('percent_up_item_id_dict', {}).get(item_id, None)
        nd_banner.nd_rate.setVisible(multiple is not None)
        name = get_lobby_item_name(banner_id)
        nd_banner.lab_name.SetString(name)
        belong_name = get_lobby_item_belong_name(banner_id)
        nd_banner.lab_role_name.SetString(belong_name)
        check_skin_tag(nd_banner.nd_kind, banner_id, ignore_improve=True)
        path = BANNER_TEX_PATH % banner_id
        if not cc.FileUtils.getInstance().isFileExist(path):
            global_data.uisystem.post_wizard_trace("cann't find " + path, None, path)
            path = DEFAULT_BANNER_TEX_PATH
        nd_banner.img_banner.SetDisplayFrameByPath('', path)
        rare_degree = get_item_rare_degree(item_id, ignore_imporve=True)
        self._item_id_2_ui_item[item_id] = nd_banner
        self.refresh_items_own_status([item_id])
        color = REWARD_RARE_COLOR.get(rare_degree, 'orange')
        pic = 'gui/ui_res_2/lottery/img_banner_%s.png' % color
        nd_banner.img_level.SetDisplayFrameByPath('', pic)
        return

    def refresh_items_own_status(self, item_ids):
        if not global_data.player or not item_ids:
            return
        for item_id in item_ids:
            if item_id <= 0:
                continue
            nd_banner = self._item_id_2_ui_item.get(item_id)
            if not nd_banner or not nd_banner.isValid() or not hasattr(nd_banner, 'nd_get'):
                continue
            if global_data.player.get_item_by_no(item_id):
                nd_banner.nd_get.setVisible(True)
                nd_banner.nd_splus.setVisible(False)
            else:
                role_improve = check_is_improvable_skin(item_id)
                mecha_improve_splus = check_is_improvable_splus_mecha_skin(item_id)
                mecha_improve_sp = check_is_improvable_sp_mecha_skin(item_id)
                show_nd_splus = role_improve or mecha_improve_splus or mecha_improve_sp
                if mecha_improve_sp:
                    improve_text_id = 635131 if 1 else 610959
                    nd_banner.nd_get.setVisible(False)
                    nd_banner.nd_splus.setVisible(show_nd_splus)
                    nd_banner.nd_splus.lab_s.SetString(improve_text_id)

    def select_banner(self, index, force_update=False):
        if self.selected_banner_index == index and not force_update:
            return
        if not self._list_sview:
            return
        self.selected_banner_index = index
        banner_id_list = self.data.get('banner_id_list', [])
        nd_banner = self._list_sview.get_list_item(index)
        if not nd_banner:
            self._list_sview.center_with_index(index, self.update_one_banner)
            nd_banner = self._list_sview.get_list_item(index)
            self.panel.list_banner.LocatePosByItem(index)
        banner_id = banner_id_list[index]
        self.on_change_show_reward(banner_id)
        self.show_model_id = banner_id
        for one_banner in self.panel.list_banner.GetAllItem():
            if nd_banner == one_banner:
                continue
            one_banner.btn_banner.SetSelect(False)

        nd_banner.btn_banner.SetSelect(True)

    def _init_scroll_banner(self):
        if self.data.get('banner_id_list', None):
            self.panel.list_banner.DeleteAllSubItem()
            self.banner_count = len(self.data['banner_id_list'])
            self._load_banner()
            if not len(self.data['banner_id_list']) > 1:
                return
            self.is_scrolling = False
            self.scroll_clock = time.time()
            self.per_scroll_dist = self.panel.list_banner.GetItem(0).getContentSize().height
            self.scroll_bottom_y = -self.per_scroll_dist / 2.0
            self.scroll_offset = self.per_scroll_dist * len(self.data['banner_id_list'])
        return

    def _init_buy_widget(self):

        def update_price_info_callback(nd, lottery_count):
            pass

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == SINGLE_LOTTERY_COUNT:
                return get_special_price_info_for_half_art_collection_single_lottery(self.lottery_id, price_info)
            return False

        def special_buy_logic_func(price_info, lottery_count):
            if lottery_count == CONTINUAL_LOTTERY_COUNT and global_data.player.determine_lottery_10_try(self.lottery_id, True):
                from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
                ScreenLockerUI(None, False)
                return True
            else:
                if not remind_second_confirm_lottery_goods(self.panel, self.lottery_id, self.data, price_info, lambda : self.buy_widget and self.buy_widget.do_buy_lottery(price_info, lottery_count)):
                    if lottery_count == SINGLE_LOTTERY_COUNT:
                        extra_info = {'lottery_id': self.lottery_id}
                        return special_buy_logic_for_half_art_collection_single_lottery(self.lottery_id, self.panel, price_info, lambda : self.buy_widget and self.buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count), extra_info)
                    return False
                return

        def buying_callback(lottery_count):
            if self.preview_widget:
                self.preview_widget.hide()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.nd_buy_1.price,
           CONTINUAL_LOTTERY_COUNT: self.panel.nd_buy_10.price
           }, price_color=USE_TEMPLATE_COLOR, update_price_info_callbacks={SINGLE_LOTTERY_COUNT: update_price_info_callback,
           CONTINUAL_LOTTERY_COUNT: update_price_info_callback
           }, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback)

    def _init_preview_widget(self):

        def show_callback():
            self.refresh_preview()
            if self.panel.nd_main_content.isVisible():
                self.panel.PlayAnimation('appear')
            self.panel.bar_review.setVisible(True)
            self.panel.nd_main_content.setVisible(False)
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def hide_callback():
            self.panel.bar_review.setVisible(False)
            self.panel.nd_main_content.setVisible(True)

        def close_callback():
            self.refresh_show_model()
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        self.preview_widget = Lottery2024SpriteNewPreviewWidget(self.panel.nd_review, self.panel, self.lottery_id, self.on_change_show_reward, show_callback=show_callback, hide_callback=hide_callback, close_callback=close_callback)

    def set_exchange_reward_widget_visible_callback(self, flag):
        global_data.emgr.refresh_switch_core_model_button_visible.emit(False)
        extra_data = self.data.get('extra_data', {})
        exchange_money_type = extra_data.get('exchange_money_type', [])
        if exchange_money_type:
            if flag:
                from logic.comsys.lottery.LotteryMainUI import get_money_payment
                exchange_money_type_show = [ get_money_payment(m) for m in exchange_money_type ]
                global_data.emgr.update_lottery_main_money_types_event.emit(exchange_money_type_show)
            else:
                global_data.emgr.update_lottery_main_money_types_event.emit(self.data.get('show_money_type', []))

    def _init_exchange_reward_widget(self):
        tab_func = self.get_exchange_tab_goods_list if self.exchange_reward_tab_list else None
        self.exchange_reward_widget = Lottery2024SpringExchangeRewardWidget(self, self.panel.nd_shop, self.panel.nd_shop, self.panel.mall_box_buy, self.lottery_id, self.on_change_show_reward, nd_kind='', nd_lab_name='', nd_btn_detail='', nd_visibility_opposite_relatively=(), tab_func=tab_func)
        return

    def get_exchange_tab_goods_list(self, goods_list):
        tab_list = []
        for tab_txt in self.exchange_reward_tab_list:
            tab_list.append({'exchange_goods_big_list': [],'exchange_goods_small_list': [],'text': tab_txt})

        for goods_id in goods_list:
            main_type, stype = mall_utils.get_mall_type_stype(goods_id)
            if stype:
                stype = int(stype)
            if int(stype) >= len(tab_list):
                global_data.uisystem.post_wizard_trace_inner_server('\xe5\x95\x86\xe5\x93\x81%s\xe4\xbd\x8d\xe4\xba\x8eExchangeReward\xe6\xa0\x8f\xe4\xbd\x8d%s, \xe4\xbd\x86\xe8\xaf\xa5\xe6\xa0\x8f\xe4\xbd\x8d\xe6\xb2\xa1\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x8c\xe5\x9b\xa0\xe6\xad\xa4\xe4\xb8\x8d\xe4\xbc\x9a\xe6\x98\xbe\xe7\xa4\xba' % (goods_id, stype))
            elif str(main_type) == str(1000):
                tab_list[stype]['exchange_goods_big_list'].append(goods_id)
            else:
                tab_list[stype]['exchange_goods_small_list'].append(goods_id)

        return tab_list

    def _init_rule_tag_list(self):
        self._init_main_rule_tag_list()
        return
        from common.cfg import confmgr
        from common.utilities import safe_percent
        tag_list = self.panel.list_tag
        rule_tag_list = self.data.get('rule_tag_list', [])
        rule_tag_conf = confmgr.get('lottery_rule_config', default={})

        def init_item(item, rule_conf):
            tag_text = rule_conf.get('tag_text')
            desc_text = rule_conf.get('desc_text')
            icon_path = rule_conf.get('icon')
            item.lab_tag.SetString(tag_text)
            item.img_class.setVisible(bool(icon_path))
            item.img_class.SetDisplayFrameByPath('', icon_path)
            if item.nd_prog:
                category = rule_conf.get('guarantee_category')
                item.nd_prog.setVisible(category is not None)
                total, line_no = self.data.get('category_floor', {}).get(str(category), [0, 0])
                cur = global_data.player.get_reward_category_floor(self.data['table_id'], line_no) if global_data.player else 0
                item.prog_tag.SetPercent(safe_percent(cur, total))
                item.lab_tag.SetString(609507)
                item.lab_tag_num.SetString(get_text_by_id(609508).format(cur, total))
                item.nd_tag.BindMethod('OnBegin', lambda t, b: self.show_reward_pool(category, cur))
                item.nd_tag.BindMethod('OnEnd', lambda t, b: self.hide_reward_pool())
                item.nd_tag.BindMethod('OnCancel', lambda t, b: self.hide_reward_pool())
            return

        tag_list.SetInitCount(len(rule_tag_list))
        for i, item in enumerate(tag_list.GetAllItem()):
            rule_id = rule_tag_list[i]
            rule_conf = rule_tag_conf.get(str(rule_id), {})
            init_item(item, rule_conf)

    def show_reward_pool(self, rare_degree, cur_count):
        self.panel.nd_quality_tips.setVisible(True)
        init_reward_pool_template(self.panel.nd_quality_tips, self.lottery_id, rare_degree, self.data.get('percent_up_item_id_dict', {}), cur_count)

    def hide_reward_pool(self):
        self.panel.nd_quality_tips.setVisible(False)

    def _release_tips_anim_timer(self):
        if self.tips_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.tips_anim_timer)
            self.tips_anim_timer = None
        return

    def tips_anim_end_callback(self):
        self.panel.StopAnimation('tips_loop')
        self.panel.nd_tips.setVisible(False)
        self.tips_anim_timer = None
        return

    def _show_shop(self):
        self.panel.nd_tips.setVisible(True)
        self.panel.PlayAnimation('tips_show')
        self.panel.PlayAnimation('tips_loop')
        self.tips_anim_timer = global_data.game_mgr.register_logic_timer(self.tips_anim_end_callback, interval=8.0, times=1, mode=CLOCK)

    def _play_flash_anim(self):
        for banner_id in self.flash_anim_banner_list:
            if banner_id in self._item_id_2_ui_item:
                self._item_id_2_ui_item[banner_id].PlayAnimation('show4')

    def show(self):
        self.panel.setVisible(True)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('change')
        self.panel.StopAnimation('begin')
        self.panel.PlayAnimation('end')
        self.panel.temp_main.PlayAnimation('loop')
        action_list = [
         cc.DelayTime.create(0.4),
         cc.CallFunc.create(self._play_flash_anim)]
        self.panel.runAction(cc.Sequence.create(action_list))
        self._release_tips_anim_timer()
        if not self.check_show_shop():
            self.tips_anim_timer = global_data.game_mgr.register_logic_timer(self._show_shop, interval=0.2, times=1, mode=CLOCK)

    def hide(self):
        self._release_tips_anim_timer()
        self.panel.setVisible(False)
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)

    def do_hide_panel(self):
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)

    def on_finalize_panel(self):
        self._activity_list_map = None
        super(Lottery2024SpringArtCollectionWidget, self).on_finalize_panel()
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        self.destroy_widget('preview_widget')
        self.destroy_widget('buy_widget')
        self.destroy_widget('main_buy_widget')
        self.destroy_widget('exchange_reward_widget')
        self.destroy_widget('activity_button_widget')
        self._release_tips_anim_timer()
        self.selected_banner_index = 0
        self._item_id_2_ui_item = None
        return

    def update_half_price_lottery_tips(self):
        self.half_price_lottery_valid = all_half_price_art_collection_lottery_valid(self.lottery_id)
        if self.half_price_lottery_valid:
            cur_week_day = tutil.get_utc8_weekday()
            data = ArchiveManager().get_archive_data('last_close_half_art_collection_tips_info')
            data['week_day'] = cur_week_day
            data.save()
            flag = True
        else:
            flag = False
        self.panel.lab_activity_tips.setVisible(flag)
        self.panel.nd_buy_1.img_red.setVisible(flag)
        self.show_half_price_lottery_tips_guide(flag)

    def show_half_price_lottery_tips_guide(self, is_show=False):
        show_guide = global_data.message_data.get_seting_inf('show_half_price_lottery_tips_guide')
        if show_guide is None:
            show_guide = True
        is_show = is_show and show_guide
        from logic.gutils import template_utils
        template_path = 'common/i_guide_left_top'
        node = self.panel.nd_buy_1
        tips_node = node.half_price_lottery_guide_tpis
        if node and not tips_node and is_show:
            wpos = node.ConvertToWorldSpacePercentage(50, 50)
            tips_node = template_utils.init_guide_temp(node, wpos, text_id=633832, name='half_price_lottery_guide_tpis', temp_path=template_path)
        tips_node and tips_node.setVisible(is_show)
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)
        return

    def refresh(self):
        self.buy_widget.refresh()
        if self.main_buy_widget:
            self.main_buy_widget.refresh()
        self.refresh_lottery_limit_count()

    def on_lottery_ended(self):
        if self.half_price_lottery_valid:
            self.update_half_price_lottery_tips()
        self._init_rule_tag_list()

    def _on_lottery_open_box_result(self, item_ids):
        if not global_data.player or not item_ids:
            return
        self.refresh_items_own_status(item_ids)

    def refresh_preview(self):
        self.preview_widget.refresh_preview_list(self.lottery_id, self.data.get('limited_item_id_list', None), self.data.get('percent_up_item_id_dict', {}))
        return

    def is_banner_list_show(self):
        return self.panel.mall_box_buy.isVisible()

    def refresh_show_model(self, show_model_id=None):
        if self.is_banner_list_show():
            if self.panel.nd_review.isVisible():
                self.preview_widget and self.preview_widget.parent_show()
            else:
                self.on_change_show_reward(None)
                global_data.emgr.refresh_switch_core_model_button_visible.emit(False)
        elif not self.panel.mall_box_buy.isVisible():
            if self.exchange_reward_widget.visible:
                self.exchange_reward_widget and self.exchange_reward_widget.refresh_show_model(show_model_id)
        return

    def switch_show_model(self, offset):
        new_index = self.selected_banner_index
        new_index += offset
        banner_id_list = self.data.get('banner_id_list', [])
        if new_index < 0:
            new_index = len(banner_id_list) - 1
        elif new_index >= len(banner_id_list):
            new_index = 0
        banner_id = banner_id_list[new_index]
        self.selected_banner_index = new_index
        self.on_change_show_reward(banner_id)

    def hide_preview_widget--- This code section failed: ---

 647       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  JUMP_IF_FALSE_OR_POP    27  'to 27'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'preview_widget'
          21  LOAD_ATTR             3  'hide'
          24  CALL_FUNCTION_0       0 
        27_0  COME_FROM                '12'
          27  POP_TOP          
          28  LOAD_CONST            0  ''
          31  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def refresh_10_try_entrance(self):
        gift_obj = global_data.player.get_lottery_10_try_gift() if global_data.player else None
        if gift_obj and gift_obj.wait_pay(self.lottery_id):
            if '10_try' not in self._activity_list_map:
                widget_conf = global_data.uisystem.load_template('lobby/i_lobby_btn_gifts')
                widget = self.panel.list_activity.AddItem(widget_conf)
                self._activity_list_map['10_try'] = widget
            widget = self._activity_list_map['10_try']
            widget.img_discount_bar.setVisible(False)
            widget.PlayAnimation('loop_charge')
            widget.lab_gifts_name.SetString(610826)

            @global_unique_click(widget.btn_click)
            def OnClick(*args):
                gift_obj = global_data.player.get_lottery_10_try_gift() if global_data.player else None
                gift_obj and gift_obj.preview_reward(False)
                return

            def refresh_time():
                if global_data.player:
                    gift_obj = global_data.player.get_lottery_10_try_gift() if 1 else None
                    return gift_obj or None
                else:
                    left_time = gift_obj.get_left_time()
                    from logic.gcommon.time_utility import get_day_hour_minute_second
                    day, hour, minute, second = get_day_hour_minute_second(left_time)
                    text = '%d:%02d:%02d' % (hour, minute, second)
                    widget.lab_time.SetString(text)
                    return

            act = cc.RepeatForever.create(cc.Sequence.create([
             cc.DelayTime.create(1.0),
             cc.CallFunc.create(refresh_time)]))
            widget.runAction(act)
            gift_obj = global_data.player.get_lottery_10_try_gift() if global_data.player else None
            if gift_obj:
                gift_obj.show_result_tips(widget.temp_tips)
            self.buy_widget.set_force_text(610825, price_info=([], False), specific_lottery_count=CONTINUAL_LOTTERY_COUNT)
        else:
            widget = self._activity_list_map.pop('10_try', None)
            if widget:
                self.panel.list_activity.DeleteItem(widget)
            self.buy_widget.set_force_text('', price_info=None, specific_lottery_count=CONTINUAL_LOTTERY_COUNT)
        self.panel.list_activity.setVisible(bool(self._activity_list_map))
        return

    def _init_main_widget(self):

        def _init_buy_widget():

            def update_price_info_callback(nd, lottery_count):
                pass

            def get_special_price_info(price_info, lottery_count):
                if lottery_count == SINGLE_LOTTERY_COUNT:
                    return get_special_price_info_for_half_art_collection_single_lottery(self.lottery_id, price_info)
                return False

            def special_buy_logic_func(price_info, lottery_count):
                if lottery_count == CONTINUAL_LOTTERY_COUNT and global_data.player.determine_lottery_10_try(self.lottery_id, True):
                    from logic.comsys.common_ui.ScreenLockerUI import ScreenLockerUI
                    ScreenLockerUI(None, False)
                    return True
                else:
                    if not remind_second_confirm_lottery_goods(self.panel, self.lottery_id, self.data, price_info, lambda : self.main_buy_widget and self.main_buy_widget.do_buy_lottery(price_info, lottery_count)):
                        if lottery_count == SINGLE_LOTTERY_COUNT:
                            extra_info = {'lottery_id': self.lottery_id}
                            return special_buy_logic_for_half_art_collection_single_lottery(self.lottery_id, self.panel, price_info, lambda : self.main_buy_widget and self.main_buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count), extra_info)
                        return False
                    return

            def buying_callback(lottery_count):
                pass

            self.main_buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.temp_main.btn_once,
               CONTINUAL_LOTTERY_COUNT: self.panel.temp_main.btn_more
               }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.temp_main.btn_once.temp_price,
               CONTINUAL_LOTTERY_COUNT: self.panel.temp_main.btn_more.temp_price
               }, update_price_info_callbacks={SINGLE_LOTTERY_COUNT: update_price_info_callback,
               CONTINUAL_LOTTERY_COUNT: update_price_info_callback
               }, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback)

        _init_buy_widget()
        from logic.gcommon.item.item_const import RARE_DEGREE_6, RARE_DEGREE_1, RARE_DEGREE_4, RARE_DEGREE_3, RARE_DEGREE_2
        TEMP_CLICK_MAP = {'temp_item_1': RARE_DEGREE_5,
           'temp_item_2': RARE_DEGREE_4,
           'temp_item_6': RARE_DEGREE_3,
           'temp_item_5': RARE_DEGREE_3,
           'temp_item_4': RARE_DEGREE_2,
           'temp_item_3': RARE_DEGREE_2
           }
        for nd_name, rare_degree in six.iteritems(TEMP_CLICK_MAP):
            nd = getattr(self.panel.temp_main, nd_name)

            @nd.nd_click.callback()
            def OnClick(btn, touch, rare_degree=rare_degree):
                if self.preview_widget:
                    self.preview_widget.show()
                    self.preview_widget.jump_to_preview_rare_degree(rare_degree)

        @global_unique_click(self.panel.temp_main.btn_click)
        def OnClick(btn, touch):
            if not self.exchange_reward_widget:
                self._init_exchange_reward_widget()
            self.exchange_reward_widget.visible = True

        if global_data.feature_mgr.is_support_spine_3_8():
            self.panel.temp_main.nd_pic.setVisible(False)
            self.panel.temp_main.vx_spine.setVisible(True)
            if global_data.feature_mgr.is_support_spine_unleak():
                self.panel.temp_main.vx_spine.setVisible(True)
                self.panel.temp_main.nd_pic.setVisible(False)
            else:
                self.panel.temp_main.vx_spine.Destroy()
                self.panel.temp_main.nd_pic.setVisible(True)
        else:
            self.panel.temp_main.nd_pic.setVisible(True)
            self.panel.temp_main.vx_spine.setVisible(False)

    def _init_main_rule_tag_list(self):
        from common.cfg import confmgr
        from common.utilities import safe_percent
        tag_list = [
         self.panel.temp_main.temp_item_1, self.panel.temp_main.temp_item_2]
        rule_tag_list = self.data.get('rule_tag_list', [])
        rule_tag_conf = confmgr.get('lottery_rule_config', default={})

        def init_item(item, rule_conf):
            tag_text = rule_conf.get('tag_text')
            desc_text = rule_conf.get('desc_text')
            icon_path = rule_conf.get('icon')
            item.lab_tag.SetString(tag_text)
            item.img_class.setVisible(bool(icon_path))
            item.img_class.SetDisplayFrameByPath('', icon_path)
            if item.nd_prog:
                category = rule_conf.get('guarantee_category')
                item.nd_prog.setVisible(category is not None)
                total, line_no = self.data.get('category_floor', {}).get(str(category), [0, 0])
                cur = global_data.player.get_reward_category_floor(self.data['table_id'], line_no) if global_data.player else 0
                item.prog.SetPercent(safe_percent(cur, total))
                item.lab_tag.SetString(609507)
                item.lab_tag_num.SetString(get_text_by_id(609508).format(cur, total))
            return

        for i, item in enumerate(tag_list):
            rule_id = rule_tag_list[i]
            rule_conf = rule_tag_conf.get(str(rule_id), {})
            init_item(item, rule_conf)