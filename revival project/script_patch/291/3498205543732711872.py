# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryArtCollectionWidgetNew.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.lottery.LotteryBaseWidget import LotteryBaseWidget
from logic.comsys.lottery.LotteryBuyWidget import LotteryBuyWidget
from .LotteryNewPreviewWidgetV2 import LotteryNewPreviewWidgetV2
from logic.gutils.item_utils import check_skin_tag, get_lobby_item_name, get_item_rare_degree, get_lobby_item_belong_name, check_is_improvable_skin, REWARD_RARE_COLOR, update_limit_btn, check_is_improvable_splus_mecha_skin, check_is_improvable_sp_mecha_skin, get_lobby_item_pic_by_item_no, get_lobby_item_type, check_bar_level_tag, get_rare_degree_name
from logic.gutils.mall_utils import get_lottery_exchange_list, get_cur_lottery_state, remind_second_confirm_lottery_goods, init_reward_pool_template, all_half_price_art_collection_lottery_valid, get_special_price_info_for_half_art_collection_single_lottery, special_buy_logic_for_half_art_collection_single_lottery, get_goods_item_open_date, check_limit_time_lottery_open_info, check_limit_time_lottery_visible_info
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.item.item_const import RARE_DEGREE_5, RARE_DEGREE_6, RARE_DEGREE_7
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.comsys.lobby.EntryWidget.ArtCollectionActivityEntryWidget import ArtCollectionActivityEntryWidget
from common.utils.timer import CLOCK
import time
import cc
from logic.client.const.mall_const import LOTTERY_ST_OPEN_ONLY_EXCHANGE, SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, REVIEW_TAB_INDEX, SHOP_TAB_INDEX, LUCK_SCORE_TAB_INDEX
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GESTURE
BANNER_BIG_TEMPLATE_PATH = 'mall/i_lottery_ss_banner_new_big'
BANNER_TEMPLATE_PATH = 'mall/i_lottery_ss_banner_new'
BANNER_SCROLL_INTERVAL = 4.0
BANNER_TEX_PATH = 'gui/ui_res_2/lottery/img_ss_banner_%d.png'
DEFAULT_BANNER_TEX_PATH = 'gui/ui_res_2/lottery/img_ss_banner_201800251.png'
PROGRESS_TEXTURE_PATH = 'gui/ui_res_2/common/progress/blue_progress.png'
DEFAULT_ICON_PATH = 'gui/ui_res_2/lottery/icon_lottery_gift.png'
DEFAULT_TXT_COLOR = 16776169
DEFAULT_OUT_LINE = 9048633
DELAY_SHOW_TAG = 20240528

class LotteryArtCollectionWidgetNew(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryArtCollectionWidgetNew, self).init_parameters()
        self.preview_widget = None
        self.preview_widget_visible = False
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
        self._conf = confmgr.get('lottery_page_config', self.lottery_id, default={})
        self.max_lottery_count = self._conf.get('day_limit', 0)
        self.activity_type = self._conf.get('activity_type')
        self.single_goods_id = self._conf.get('single_goods_id')
        self.visible_ts = self._conf.get('visible_ts')
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        self.half_price_lottery_valid = all_half_price_art_collection_lottery_valid(self.lottery_id)
        self.tips_anim_timer = None
        self._activity_list_map = {}
        self.remain_time = 0
        self.title_timer = None
        self._showing_review_anim = False
        return

    def init_panel(self):
        super(LotteryArtCollectionWidgetNew, self).init_panel()
        self._list_sview = None
        self.panel.btn_shop.EnableCustomState(False)
        self.panel.red_point.setVisible(False)
        self.panel.PlayAnimation('loop_gift')
        self.panel.PlayAnimation('show_nd_content')
        self.panel.red_point.setVisible(False)
        self.panel.lab_free_time.setVisible(False)
        self.panel.nd_review.setVisible(False)
        extra_data = self.data.get('extra_data', {})
        txt_color = eval(extra_data.get('text_color', DEFAULT_TXT_COLOR)) if extra_data else DEFAULT_TXT_COLOR
        out_line = eval(extra_data.get('out_line', DEFAULT_OUT_LINE)) if extra_data else DEFAULT_OUT_LINE
        act_txt_id = extra_data.get('act_text_id', None)
        shop_txt_id = extra_data.get('shop_text_id', None)
        gift_tip_txt_id = extra_data.get('gift_tip_text_id', None)
        activity_lab_btn_text = self.panel.btn_activity.nd_activity.lab_btn_text
        activity_lab_btn_text.SetColor(txt_color)
        act_txt_id and activity_lab_btn_text.SetString(act_txt_id)
        shop_txt_id and self.panel.btn_shop.nd_activity.lab_btn_text.SetString(shop_txt_id)
        shop_txt_id and self.panel.list_tab_top2.GetItem(1).lab_btn.SetString(shop_txt_id)

        @global_unique_click(self.panel.btn_describe)
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            title, content = self.data.get('rule_desc', [608106, 608107])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.btn_shop)
        def OnClick(*args):
            self._set_preview_widget_visible(True, SHOP_TAB_INDEX)

        @global_unique_click(self.panel.list_tab_top.GetItem(0).btn_tab)
        def OnClick(*args):
            self._set_preview_widget_visible(True, REVIEW_TAB_INDEX)

        @global_unique_click(self.panel.list_tab_top.GetItem(1).btn_tab)
        def OnClick(*args):
            self._set_preview_widget_visible(True, LUCK_SCORE_TAB_INDEX)

        @global_unique_click(self.panel.btn_switch)
        def OnClick(*args):
            self._set_preview_widget_visible(True)

        @global_unique_click(self.panel.btn_switch2)
        def OnClick(*args):
            self._set_preview_widget_visible(False)

        @global_unique_click(self.panel.btn_lottery)
        def OnClick(*args):
            self._set_preview_widget_visible(False)

        nd_rank_history = self.panel.nd_rank_history

        @global_unique_click(nd_rank_history.btn_hide)
        def OnClick(*args):
            self._set_preview_widget_visible(False)

        self._init_title()
        self._init_time_label()
        self._init_scroll_banner()
        self._init_buy_widget()
        self._init_rule_tag_list()
        self._update_buy_widget_state()
        if self.panel.lab_tips:
            self.panel.lab_tips.setVisible(True)
            txt_id = self.data.get('show_tip')
            txt = ''
            if txt_id:
                txt = get_text_by_id(txt_id)
            self.panel.lab_tips.SetString(txt)
        self.init_temporary_activity_entrance()
        self.init_extra_activity_entrance()
        self.update_half_price_lottery_tips()
        return

    def jump_to_exchange_shop_widget(self, goods_id, check=True):
        exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
        if self.lottery_id not in lottery_exchange_goods:
            global_data.game_mgr.show_tip(get_text_by_id(12128))
            return
        if not check or self.panel.mall_box_buy.isVisible() or get_cur_lottery_state(self.single_goods_id, self.visible_ts) == LOTTERY_ST_OPEN_ONLY_EXCHANGE:
            self._set_preview_widget_visible(True, SHOP_TAB_INDEX, goods_id)

    def set_visible_close(self, is_visible_close):
        self.is_visible_close = is_visible_close

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
           'lottery_open_box_result': self._on_lottery_open_box_result
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
        self._list_sview = InfiniteScrollWidget(self.panel.list_banner, self.panel, up_limit=10000, down_limit=10000, get_tempate_path_func=self.get_tempate_path_func)
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

    def get_tempate_path_func(self, data):
        item_id, index = data
        degree = get_item_rare_degree(item_id, ignore_imporve=True)
        if degree == RARE_DEGREE_5 or degree == RARE_DEGREE_6 or degree == RARE_DEGREE_7:
            return BANNER_BIG_TEMPLATE_PATH
        else:
            return BANNER_TEMPLATE_PATH

    def request_members_data(self):
        pass

    def update_one_banner(self, nd_banner, data):
        banner_id, index = data

        @global_unique_click(nd_banner.btn_banner)
        def OnClick(*args):
            self.select_banner(index)

        item_id = banner_id
        template_path = self.get_tempate_path_func(data)
        is_big = template_path == BANNER_BIG_TEMPLATE_PATH
        rare_degree = get_item_rare_degree(item_id, ignore_imporve=True)
        color = REWARD_RARE_COLOR.get(rare_degree, 'orange')
        name = get_lobby_item_name(banner_id)
        nd_banner.lab_name.SetString(name)
        if is_big:
            big_state = 'big' if 1 else 'small'
            frame_path = 'gui/ui_res_2/lottery/frame_lottery_item_{}_{}.png'.format(big_state, color)
            nd_banner.btn_banner.SetFrames('', [frame_path, frame_path, ''])
            img_banner = nd_banner.img_banner
            path = get_lobby_item_pic_by_item_no(item_id)
            img_banner.SetDisplayFrameByPath('', path)
            item_type = get_lobby_item_type(item_id)
            if is_big and (item_type == L_ITEM_TYPE_MECHA_SKIN or item_type == L_ITEM_TYPE_ROLE_SKIN):
                img_banner.SetPosition('50%0', '50%104')
                img_banner.setScale(0.88)
            elif item_type == L_ITME_TYPE_GUNSKIN or item_type == L_ITEM_YTPE_VEHICLE_SKIN:
                img_banner.SetPosition('50%0', '50%90')
                img_banner.setScale(0.7)
            else:
                img_banner.SetPosition('50%0', '50%67')
                img_banner.setScale(0.52)
        elif item_type == L_ITEM_TYPE_MECHA_SKIN or item_type == L_ITEM_TYPE_ROLE_SKIN:
            img_banner.SetPosition('50%0', '50%85')
            img_banner.setScale(0.88)
        elif item_type == L_ITME_TYPE_GUNSKIN or item_type == L_ITEM_YTPE_VEHICLE_SKIN:
            img_banner.SetPosition('50%0', '50%82')
            img_banner.setScale(0.64)
        else:
            img_banner.SetPosition('50%0', '50%46')
            img_banner.setScale(0.36)
        check_bar_level_tag(nd_banner.bar_level, item_id)
        check_skin_tag(nd_banner.nd_kind, item_id, ignore_improve=True)
        self._item_id_2_ui_item[item_id] = nd_banner
        self.refresh_items_own_status([item_id])
        big_state = '_big' if is_big else ''
        pic = 'gui/ui_res_2/lottery/img_banner_{}{}.png'.format(color, big_state)
        nd_banner.img_level.SetDisplayFrameByPath('', pic)
        update_limit_btn(banner_id, nd_banner.temp_limit, nd_banner.temp_limit.nd_limit_describe, clip_object=self.panel.list_banner, is_corner=True, from_part='lottery')

    def refresh_items_own_status(self, item_ids):
        if not global_data.player or not item_ids:
            return
        for item_id in item_ids:
            if item_id <= 0:
                continue
            nd_banner = self._item_id_2_ui_item.get(item_id)
            if not nd_banner or not nd_banner.isValid() or not hasattr(nd_banner, 'nd_got'):
                continue
            if global_data.player.get_item_by_no(item_id):
                nd_banner.nd_got.setVisible(True)
            else:
                role_improve = check_is_improvable_skin(item_id)
                mecha_improve_splus = check_is_improvable_splus_mecha_skin(item_id)
                mecha_improve_sp = check_is_improvable_sp_mecha_skin(item_id)

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

    def _init_title(self):
        self.panel.lab_title.SetString(get_text_by_id(self._conf.get('text_id')))

    def _init_time_label(self):
        self.panel.lab_tips_time.SetString('')
        if self.is_visible_close:
            self.remain_time = int(self.visible_ts[1] - tutil.get_server_time())
        else:
            open_date_range = get_goods_item_open_date(self.single_goods_id)
            _, left_time = check_limit_time_lottery_open_info(open_date_range)
            self.remain_time = int(left_time)
        if self.remain_time > 0:
            self.title_timer = global_data.game_mgr.get_logic_timer().register(func=self._update_title_timer, interval=1, mode=CLOCK)

    def _release_title_timer(self):
        if self.title_timer:
            global_data.game_mgr.unregister_logic_timer(self.title_timer)
            self.title_timer = None
        return

    def _update_title_timer(self):
        self.remain_time = self.remain_time - 1
        if self.remain_time < 0:
            self._release_title_timer()
            self._update_buy_widget_state()
            return
        time_str = tutil.get_simply_readable_time(self.remain_time)
        if self.is_visible_close:
            self.panel.lab_tips_time.SetString('{}{}'.format(get_text_by_id(82134), time_str))
        else:
            self.panel.lab_tips_time.SetString(get_text_by_id(19446).format(time_str))

    def _update_buy_widget_state(self):
        self.panel.nd_buy_1.setVisible(not self.is_visible_close)
        self.panel.nd_buy_10.setVisible(not self.is_visible_close)

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

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func)

    def _init_preview_widget(self, default_tab_index):

        def show_callback():
            self.panel.bar_review.setVisible(True)
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def hide_callback():
            self.panel.bar_review.setVisible(False)

        def close_callback():
            self.refresh_show_model()
            global_data.emgr.refresh_switch_core_model_button_visible.emit(True)

        self.preview_widget = LotteryNewPreviewWidgetV2(self.panel.nd_review, self.panel, self.lottery_id, self.on_change_show_reward, show_callback=show_callback, hide_callback=hide_callback, close_callback=close_callback, data=self.data, default_tab_index=default_tab_index)

    def _init_rule_tag_list(self):
        from common.cfg import confmgr
        from common.utilities import safe_percent
        tag_list = self.panel.list_tag
        rule_tag_list = self.data.get('rule_tag_list', [])
        rule_tag_conf = confmgr.get('lottery_rule_config', default={})

        def init_item(item, rule_conf):
            tag_text = rule_conf.get('tag_text')
            category = rule_conf.get('guarantee_category')
            total, line_no = self.data.get('category_floor', {}).get(str(category), [0, 0])
            cur = global_data.player.get_reward_category_floor(self.data['table_id'], line_no) if global_data.player else 0
            item.lab_tag_num.SetString(get_text_by_id(tag_text).format(cur, total))
            rare_degree_name = get_rare_degree_name(category)
            item.lab_title.SetString(get_text_by_id(860454).format(rare_degree_name))

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
        self.tips_anim_timer = None
        return

    def play_show_nd_review_anim(self):
        if self._showing_review_anim:
            return
        self._showing_review_anim = True

        def delay_call(*args):
            self._showing_review_anim = False
            self.preview_widget.show_panel()

        self.panel.StopAnimation('show_nd_review')
        anim_time = self.panel.GetAnimationMaxRunTime('show_nd_review')
        self.panel.DelayCallWithTag(anim_time, delay_call, DELAY_SHOW_TAG)
        self.panel.PlayAnimation('show_nd_review')
        self.preview_widget.panel.bar_review.setVisible(True)

    def _set_preview_widget_visible(self, is_visible, default_tab_index=None, init_goods_id=None, force_refresh=False):
        if default_tab_index is None:
            if self.is_visible_close:
                default_tab_index = SHOP_TAB_INDEX
            else:
                default_tab_index = REVIEW_TAB_INDEX
        if not self.preview_widget:
            self._init_preview_widget(default_tab_index)
        if is_visible:
            if not self.preview_widget_visible or force_refresh:
                self.play_show_nd_review_anim()
                self.preview_widget.set_show_data()
                self.preview_widget.set_node_click(default_tab_index, init_goods_id)
                self.preview_widget_visible = True
                ui = global_data.ui_mgr.get_ui('LotteryMainUI')
                if ui:
                    ui.set_preview_widget_visible(True)
            else:
                self.preview_widget.show()
                self.preview_widget.set_node_click(default_tab_index, init_goods_id)
        else:
            self.preview_widget.hide()
            self.panel.nd_rank_history.setVisible(False)
            self.panel.PlayAnimation('show_nd_content')
            self.preview_widget_visible = False
            ui = global_data.ui_mgr.get_ui('LotteryMainUI')
            if ui:
                ui.set_preview_widget_visible(False)
            self.refresh_show_model()
            self.panel.btn_shop.setVisible(True)
            self._update_buy_widget_state()
        return

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
        self.panel.PlayAnimation('appear_2')
        action_list = [
         cc.DelayTime.create(0.4),
         cc.CallFunc.create(self._play_flash_anim)]
        self.panel.runAction(cc.Sequence.create(action_list))
        self._release_tips_anim_timer()
        self._release_title_timer()
        self._init_time_label()
        self._update_buy_widget_state()
        if get_cur_lottery_state(self.single_goods_id, self.visible_ts) == LOTTERY_ST_OPEN_ONLY_EXCHANGE:
            self._set_preview_widget_visible(True, SHOP_TAB_INDEX, force_refresh=True)
        elif self.preview_widget:
            self._set_preview_widget_visible(self.preview_widget_visible, self.preview_widget.get_cur_select_tab_index(), force_refresh=True)
        else:
            ui = global_data.ui_mgr.get_ui('LotteryMainUI')
            ui and ui.set_preview_widget_visible(False)

    def hide(self):
        self._release_tips_anim_timer()
        self._release_title_timer()
        self.panel.setVisible(False)
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)
        ui = global_data.ui_mgr.get_ui('LotteryMainUI')
        ui and ui.set_preview_widget_visible(False)

    def do_hide_panel(self):
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)

    def on_finalize_panel(self):
        self._activity_list_map = None
        super(LotteryArtCollectionWidgetNew, self).on_finalize_panel()
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        self.destroy_widget('preview_widget')
        self.destroy_widget('buy_widget')
        self.destroy_widget('activity_button_widget')
        self._release_tips_anim_timer()
        self._release_title_timer()
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
        self.refresh_lottery_limit_count()

    def on_lottery_ended(self):
        if self.half_price_lottery_valid:
            self.update_half_price_lottery_tips()
        self._init_rule_tag_list()

    def _on_lottery_open_box_result(self, item_ids):
        if not global_data.player or not item_ids:
            return
        self.refresh_items_own_status(item_ids)

    def is_banner_list_show(self):
        return self.panel.nd_main.isVisible() and self.panel.mall_box_buy.isVisible()

    def refresh_show_model(self, show_model_id=None):
        lottery_result_ui = global_data.ui_mgr.get_ui('LotteryResultUI')
        if lottery_result_ui:
            return
        if self.is_banner_list_show():
            if show_model_id:
                index = self.get_banner_id_index(show_model_id)
                self.select_banner(index, True)
                self.panel.list_banner.LocatePosByItem(index)
            elif self.preview_widget_visible:
                self.preview_widget.refresh_show_model()
            else:
                self.select_banner(self.selected_banner_index, True)

    def switch_show_model(self, offset):
        new_index = self.selected_banner_index
        new_index += offset
        banner_id_list = self.data.get('banner_id_list', [])
        if new_index < 0:
            new_index = len(banner_id_list) - 1
        elif new_index >= len(banner_id_list):
            new_index = 0
        self.select_banner(new_index)
        self.panel.list_banner.LocatePosByItem(new_index)

    def hide_preview_widget--- This code section failed: ---

 675       0  LOAD_GLOBAL           0  'getattr'
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

 676      28  LOAD_GLOBAL           4  'False'
          31  LOAD_FAST             0  'self'
          34  STORE_ATTR            5  'preview_widget_visible'
          37  LOAD_CONST            0  ''
          40  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9