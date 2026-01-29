# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryPetDragonWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryNewPreviewWidget import LotteryNewPreviewWidget
from .LotteryShopWidget import LotteryShopWidget
from .LotteryBuyWidget import LotteryBuyWidget
from logic.gutils.item_utils import check_skin_tag, get_lobby_item_name, get_item_rare_degree, get_lobby_item_belong_name, check_is_improvable_skin, REWARD_RARE_COLOR, update_limit_btn, check_is_improvable_splus_mecha_skin, check_is_improvable_sp_mecha_skin
from logic.gutils.mall_utils import get_lottery_exchange_list, get_cur_lottery_state, remind_second_confirm_lottery_goods, init_reward_pool_template, all_half_price_art_collection_lottery_valid, get_special_price_info_for_half_art_collection_single_lottery, special_buy_logic_for_half_art_collection_single_lottery, get_special_price_info_with_slot_machine_ten, check_payment, get_total_ticket_count_need, get_mall_item_price, lottery_calculate_money_need_spent, get_special_price_info_with_slot_machine_single, pet_dragon_lottery_calculate_money_need_spent
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
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no, get_skin_rare_degree_icon
from logic.comsys.lottery.LotterySlotMachineUI import LotterySlotMachineUI
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.task_utils import get_task_reward
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
BANNER_SCROLL_INTERVAL = 4.0
BANNER_TEX_PATH = 'gui/ui_res_2/lottery/img_ss_banner_%d.png'
DEFAULT_BANNER_TEX_PATH = 'gui/ui_res_2/lottery/img_ss_banner_201800251.png'
PROGRESS_TEXTURE_PATH = 'gui/ui_res_2/common/progress/blue_progress.png'
DEFAULT_ICON_PATH = 'gui/ui_res_2/lottery/icon_lottery_gift.png'
DEFAULT_TXT_COLOR = 16776169
DEFAULT_OUT_LINE = 9048633
SHOW_TIP_KEY = 'lottery_turntable_tip_{}'

class LotteryPetDragonNewPreviewWidget(LotteryNewPreviewWidget):
    ITEM_TEMPLATE = 'mall/i_collection_activity/cswz_pet/i_cswz_lottery_review_list_group_item'
    TITLE_TEMPLATE = 'mall/i_collection_activity/cswz_pet/i_cswz_lottery_review_list_group_title'


class LotteryPetDragonWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryPetDragonWidget, self).init_parameters()
        self.preview_widget = None
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
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        self.half_price_lottery_valid = all_half_price_art_collection_lottery_valid(self.lottery_id)
        self.tips_anim_timer = None
        self._activity_list_map = {}
        return

    def init_panel(self):
        super(LotteryPetDragonWidget, self).init_panel()
        self._list_sview = None
        self.shop_widget = None
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
        shop_txt_id and self.panel.btn_shop.lab_shop_title.SetString(shop_txt_id)
        gift_tip_txt_id and self.panel.lab_tips_activity.SetString(gift_tip_txt_id)

        @global_unique_click(self.panel.btn_change)
        def OnClick(*args):
            self.preview_widget.show()

        @global_unique_click(self.panel.temp_btn_close.btn_back)
        def OnClick(*args):
            self.preview_widget.hide()

        @global_unique_click(self.panel.btn_question)
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            title, content = self.data.get('rule_desc', [608106, 608107])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.btn_shop)
        def OnClick(*args):
            if not self.shop_widget:
                return
            exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
            if self.lottery_id not in lottery_exchange_goods:
                global_data.game_mgr.show_tip(get_text_by_id(12128))
                return
            if self.panel.mall_box_buy.isVisible():
                self.shop_widget.parent_show()
            else:
                self.shop_widget.parent_hide()

        @global_unique_click(self.panel.nd_shop.temp_btn_close.btn_back)
        def OnClick(*args):
            self.shop_widget and self.shop_widget.parent_hide()

        from common.cfg import confmgr
        ui_args = confmgr.get('lottery_page_config', str(self.lottery_id), 'advance_args', default=[])
        self.panel.btn_view.setVisible(bool(ui_args))

        @global_unique_click(self.panel.btn_view)
        def OnClick(btn, touch, ui_args=ui_args):
            if ui_args:
                global_data.ui_mgr.show_ui(*ui_args)

        @global_unique_click(self.panel.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        self._init_scroll_banner()
        self._init_buy_widget()
        self._init_preview_widget()
        self._init_shop_widget()
        self._init_rule_tag_list()
        self._init_discount_widget()
        self._init_head_gift_widget()
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
        if not self.shop_widget:
            return
        exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
        if self.lottery_id not in lottery_exchange_goods:
            global_data.game_mgr.show_tip(get_text_by_id(12128))
            return
        if not check or self.panel.mall_box_buy.isVisible() or get_cur_lottery_state(self.single_goods_id, self.visible_ts) == LOTTERY_ST_OPEN_ONLY_EXCHANGE:
            self.shop_widget.parent_show(goods_id)

    def set_visible_close(self, is_visible_close):
        self.is_visible_close = is_visible_close

    def check_show_shop(self):
        if self.is_visible_close and self.data.get('show_shop', False):
            self.shop_widget and self.shop_widget.parent_show()
            self.panel.nd_granbelm.setVisible(False)
            self.panel.nd_shop.temp_btn_close.setVisible(False)
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
           'lottery_ten_try_update': self.refresh_10_try_entrance,
           'receive_task_reward_succ_event': self.refresh_task_reward_status
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
        self.selected_banner_index = index
        banner_id_list = self.data.get('banner_id_list', [])
        banner_id = banner_id_list[index]
        self.on_change_show_reward(banner_id)
        self.show_model_id = banner_id

    def _init_scroll_banner(self):
        banner_id_list = self.data.get('banner_id_list', [])
        reward_items = [
         self.panel.temp_item_1,
         self.panel.temp_item_2,
         self.panel.temp_item_3,
         self.panel.temp_item_4,
         self.panel.temp_item_5]
        for index, item_no in enumerate(banner_id_list):
            reward_item = reward_items[index]
            name = get_lobby_item_name(item_no)
            item_path = get_lobby_item_pic_by_item_no(item_no)
            rare_icon = get_skin_rare_degree_icon(item_no)
            reward_item.img_item.SetDisplayFrameByPath('', item_path)
            reward_item.lab_name.SetString(name)
            reward_item.temp_kind.bar_level.SetDisplayFrameByPath('', rare_icon)

            @global_unique_click(reward_item.btn_item)
            def OnClick(btn, touch, idx=index):
                self.select_banner(idx)

    def _init_buy_widget(self):

        def update_price_info_callback(nd, lottery_count):
            pass

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == SINGLE_LOTTERY_COUNT:
                return get_special_price_info_with_slot_machine_single(self.lottery_id, price_info, self.data['ticket_goods_id'], self.data['ticket_item_id'], lottery_count)
            if lottery_count == CONTINUAL_LOTTERY_COUNT:
                return get_special_price_info_with_slot_machine_ten(self.lottery_id, price_info, self.data['ticket_goods_id'], self.data['ticket_item_id'], lottery_count)
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

        def special_calculate_money_need_spent(lottery_id, lottery_goods_id, ticket_goods_id, ticket_item_id):
            return pet_dragon_lottery_calculate_money_need_spent(lottery_id, lottery_goods_id, ticket_goods_id, ticket_item_id)

        def buying_callback(lottery_count):
            self.preview_widget.hide()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, update_price_info_callbacks={SINGLE_LOTTERY_COUNT: update_price_info_callback,
           CONTINUAL_LOTTERY_COUNT: update_price_info_callback
           }, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback, special_money_need_spent_func=special_calculate_money_need_spent)

    def _init_preview_widget(self):

        def show_callback():
            self.refresh_preview()
            if self.panel.nd_main_content.isVisible():
                self.panel.PlayAnimation('appear')
            self.panel.lab_change.SetString(80566)
            self.panel.bar_review.setVisible(True)
            self.panel.nd_main_content.setVisible(False)
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def hide_callback():
            self.panel.lab_change.SetString(81213)
            self.panel.bar_review.setVisible(False)
            self.panel.nd_main_content.setVisible(True)

        def close_callback():
            self.refresh_show_model()
            global_data.emgr.refresh_switch_core_model_button_visible.emit(True)

        self.preview_widget = LotteryPetDragonNewPreviewWidget(self.panel.nd_review, self.panel, self.lottery_id, self.on_change_show_reward, show_callback=show_callback, hide_callback=hide_callback, close_callback=close_callback)

    def _init_shop_widget(self):

        def show_callback():
            if self.panel.mall_box_buy.isVisible():
                self.panel.PlayAnimation('shop_in')
            self.panel.btn_shop.SetSelect(True)
            self.panel.mall_box_buy.setVisible(False)
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def hide_callback():
            if not self.panel.mall_box_buy.isVisible():
                self.panel.PlayAnimation('shop_out')
            self.panel.btn_shop.SetSelect(False)
            self.panel.mall_box_buy.setVisible(True)
            if self.panel.bar_review.isVisible():
                self.preview_widget.parent_show()
            else:
                self.refresh_show_model()
                global_data.emgr.refresh_switch_core_model_button_visible.emit(True)

        self.shop_widget = LotteryShopWidget(self.panel.nd_shop, self.panel, self.on_change_show_reward, self.lottery_id, show_callback=show_callback, hide_callback=hide_callback)

    def _init_rule_tag_list(self):
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

    def _init_discount_widget(self):
        archive_key_rp = 'slot_machine_rp_clicked_{}'.format(self.lottery_id)

        @global_unique_click(self.panel.btn_discount)
        def OnClick(*args):
            LotterySlotMachineUI(lottery_id=self.lottery_id)
            if global_data.achi_mgr:
                global_data.achi_mgr.set_cur_user_archive_data(archive_key_rp, True)
                self.panel.btn_discount.temp_red.setVisible(False)

        if global_data.achi_mgr and not global_data.achi_mgr.get_cur_user_archive_data(archive_key_rp, default=False):
            is_visible = True
        else:
            is_visible = False
        self.panel.btn_discount.temp_red.setVisible(is_visible)
        archive_key_open = 'opened_lottery_{}'.format(self.lottery_id)
        if global_data.achi_mgr and not global_data.achi_mgr.get_cur_user_archive_data(archive_key_open, default=False):
            is_first = True
        else:
            is_first = False
        if is_first:
            LotterySlotMachineUI(lottery_id=self.lottery_id)

    def _init_head_gift_widget(self):
        self.show_tip_key = SHOW_TIP_KEY.format(self.lottery_id)
        self.text_id_map = {ITEM_UNGAIN: self.data.get('extra_data', {}).get('left_top_text_id', 609866),
           ITEM_UNRECEIVED: 81708,
           ITEM_RECEIVED: 80866
           }
        self.panel.RecordAnimationNodeState('bones_get')
        if 'bind_task_id' in self.data:
            self.refresh_task_reward_status(self.data['bind_task_id'])

            @global_unique_click(self.panel.btn_reward)
            def OnClick(btn, touch):
                self.panel.nd_tips.setVisible(False)
                global_data.achi_mgr.set_cur_user_archive_data(self.show_tip_key, 0)
                task_id = self.data['bind_task_id']
                task_reward_status = global_data.player.get_task_reward_status(task_id)
                if task_reward_status == ITEM_UNRECEIVED:
                    global_data.player.receive_task_reward(task_id)
                    self.panel.btn_reward.red_point.setVisible(False)
                else:
                    reward_list = confmgr.get('common_reward_data', str(get_task_reward(task_id)), 'reward_list', default=None)
                    reward_item, num = reward_list[0]
                    bind_item_no = self.data.get('extra_data', {}).get('btn_reward_bind_item_no')
                    if bind_item_no and reward_item == bind_item_no:
                        dlg = GameRuleDescUI()
                        title_text_id = self.data.get('extra_data', {}).get('btn_reward_title_text_id')
                        content_text_id = self.data.get('extra_data', {}).get('btn_reward_content_text_id')
                        dlg.set_show_rule(title_text_id, content_text_id)
                        dlg.set_node_pos(btn.getPosition(), cc.Vec2(-0.1, 1.1))
                    else:
                        global_data.emgr.show_item_desc_ui_event.emit(reward_item, None, btn.getPosition(), item_num=num)
                return

            show_tip = global_data.achi_mgr.get_cur_user_archive_data(self.show_tip_key, default=1)
            self.panel.nd_tips.setVisible(bool(show_tip))
            if show_tip:
                self.panel.runAction(cc.Sequence.create([
                 cc.DelayTime.create(30),
                 cc.CallFunc.create(lambda : self.panel.nd_tips.setVisible(False))]))
        if 'exclusive_gift' in self.data:
            self.refresh_task_reward_status(None)

            @global_unique_click(self.panel.btn_bones)
            def OnClick(btn, touch):
                self.panel.nd_tips.setVisible(False)
                global_data.achi_mgr.set_cur_user_archive_data(self.show_tip_key, 0)
                from logic.comsys.lottery.LotteryExclusiveGiftUI import LotteryExclusiveGiftUI
                gift_template = self.data['exclusive_gift'].get('gift_template', '')
                LotteryExclusiveGiftUI(None, self.data['exclusive_gift'], gift_template=gift_template)
                return

            show_tip = global_data.achi_mgr.get_cur_user_archive_data(self.show_tip_key, default=1)
            self.panel.nd_tips.setVisible(bool(show_tip))
            if show_tip:
                self.panel.runAction(cc.Sequence.create([
                 cc.DelayTime.create(30),
                 cc.CallFunc.create(lambda : self.panel.nd_tips.setVisible(False))]))
        return

    def refresh_task_reward_status(self, task_id):
        if 'bind_task_id' in self.data:
            if task_id != self.data['bind_task_id']:
                return
            task_reward_status = global_data.player.get_task_reward_status(self.data['bind_task_id'])
            self.panel.lab_btn_bones_name.SetString(self.text_id_map[task_reward_status])
            self.panel.btn_reward.red_point.setVisible(task_reward_status == ITEM_UNRECEIVED)
            self.panel.btn_reward.img_got_mask.setVisible(task_reward_status == ITEM_RECEIVED)
            if task_reward_status == ITEM_UNRECEIVED:
                self.panel.PlayAnimation('bones_get')
            else:
                self.panel.StopAnimation('bones_get')
                self.panel.RecoverAnimationNodeState('bones_get')
        if 'exclusive_gift' in self.data:
            task_list = self.data['exclusive_gift'].get('task_list', [])
            self.panel.btn_bones.red_point.setVisible(False)
            for task_id in task_list:
                task_reward_status = global_data.player.get_task_reward_status(task_id)
                if task_reward_status == ITEM_UNRECEIVED:
                    self.panel.btn_bones.red_point.setVisible(True)
                    return

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
        if not self.panel.mall_box_buy.isVisible():
            self.shop_widget.parent_show()
        else:
            self.preview_widget.parent_show()
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
        action_list = [
         cc.DelayTime.create(0.4),
         cc.CallFunc.create(self._play_flash_anim)]
        self.panel.runAction(cc.Sequence.create(action_list))
        self._release_tips_anim_timer()
        if not self.check_show_shop():
            self.tips_anim_timer = global_data.game_mgr.register_logic_timer(self._show_shop, interval=0.2, times=1, mode=CLOCK)
        global_data.emgr.set_lottery_reward_info_label_visible.emit(True)

    def hide(self):
        self._release_tips_anim_timer()
        self.panel.setVisible(False)
        self.shop_widget and self.shop_widget.process_event(False)
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)

    def do_hide_panel(self):
        self.shop_widget and self.shop_widget.process_event(False)
        global_data.message_data.set_seting_inf('show_half_price_lottery_tips_guide', False)
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)

    def on_finalize_panel(self):
        self._activity_list_map = None
        super(LotteryPetDragonWidget, self).on_finalize_panel()
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        self.destroy_widget('preview_widget')
        self.destroy_widget('buy_widget')
        self.destroy_widget('shop_widget')
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
        return self.panel.nd_main_content.isVisible() and self.panel.mall_box_buy.isVisible()

    def refresh_show_model(self, show_model_id=None):
        if self.is_banner_list_show():
            if show_model_id:
                index = self.get_banner_id_index(show_model_id)
                self.select_banner(index, True)
            else:
                self.select_banner(self.selected_banner_index, True)
        elif not self.panel.mall_box_buy.isVisible():
            self.shop_widget and self.shop_widget.refresh_show_model()

    def switch_show_model(self, offset):
        new_index = self.selected_banner_index
        new_index += offset
        banner_id_list = self.data.get('banner_id_list', [])
        if new_index < 0:
            new_index = len(banner_id_list) - 1
        elif new_index >= len(banner_id_list):
            new_index = 0
        self.select_banner(new_index)

    def hide_preview_widget--- This code section failed: ---

 737       0  LOAD_GLOBAL           0  'getattr'
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

    def custom_get_special_price_info(self):

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == SINGLE_LOTTERY_COUNT:
                return get_special_price_info_with_slot_machine_single(self.lottery_id, price_info, self.data['ticket_goods_id'], self.data['ticket_item_id'], lottery_count)
            if lottery_count == CONTINUAL_LOTTERY_COUNT:
                return get_special_price_info_with_slot_machine_ten(self.lottery_id, price_info, self.data['ticket_goods_id'], self.data['ticket_item_id'], lottery_count)
            return False

        return get_special_price_info

    def custom_money_need_spent_func(self):
        from logic.gutils.mall_utils import pet_dragon_lottery_calculate_money_need_spent
        return pet_dragon_lottery_calculate_money_need_spent