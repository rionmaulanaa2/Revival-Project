# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBaseWidget.py
from __future__ import absolute_import
import six_ex
from common.platform.dctool.interface import is_mainland_package
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.mall_utils import check_lucky_score_rank_likes_red_point

class LotteryBaseWidget(object):

    def __init__(self, parent, lottery_id, data, on_change_show_reward, auto_load_panel=True):
        self.parent = parent
        self.lottery_id = lottery_id
        self.data = data
        self.on_change_show_reward = on_change_show_reward
        self.panel = None
        self.show_model_id = None
        self.ignore_item_scene = False
        self.init_parameters()
        if auto_load_panel:
            self.load_panel()
        return

    def load_panel(self):
        if not self.panel:
            nd_widget_name = 'lucky_house_{}'.format(self.lottery_id)
            path = self.data['template_path']
            self.panel = global_data.uisystem.load_template_create(path, parent=self.parent, name=nd_widget_name)
            self.init_panel()
            self.process_event(True)

    @staticmethod
    def _fix_custom_model_parameters(custom_param):
        keys = six_ex.keys(custom_param)
        for key in keys:
            custom_param[int(key)] = custom_param.pop(key)

    def init_parameters(self):
        conf = confmgr.get('lottery_page_config', default={})
        self.max_lottery_count = conf[self.lottery_id].get('day_limit', 0)
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        self.ignore_chuchang_anim = bool(conf[self.lottery_id].get('ignore_chuchang_anim'))
        self.goods_got_func = conf[self.lottery_id].get('goods_got_func', {})
        offset_scale_conf = conf[self.lottery_id].get('offset_scale_param', {})
        self.common_model_offset = offset_scale_conf.get('common_offset')
        self.custom_model_offset = offset_scale_conf.get('custom_offset', {})
        self._fix_custom_model_parameters(self.custom_model_offset)
        self.common_model_scale = offset_scale_conf.get('common_scale')
        self.custom_model_scale = offset_scale_conf.get('custom_scale', {})
        self._fix_custom_model_parameters(self.custom_model_scale)
        self._is_show_luck_rank_list = 'luck_rank_list' in conf[self.lottery_id]

    def init_panel(self):
        self.refresh_lottery_limit_count()
        if self.panel.btn_rank_lucky:
            self.panel.btn_rank_lucky.setVisible(self._is_show_luck_rank_list)

            @global_unique_click(self.panel.btn_rank_lucky)
            def OnClick(*args, **kwargs):
                self.on_click_btn_rank_lucky(*args, **kwargs)

            self.refresh_rank_likes_red_point()

    def on_click_btn_rank_lucky(self, *args, **kwargs):
        from logic.comsys.lottery.LuckScore.LuckScoreRankListUI import LuckScoreRankListUI
        LuckScoreRankListUI(lottery_id=self.lottery_id)

    def get_event_conf(self):
        return {}

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = self.get_event_conf()
        if is_mainland_package():
            if 'buy_good_success' in econf:
                econf['buy_good_success'] = [
                 self.refresh_lottery_limit_count, econf['buy_good_success']]
            else:
                econf['buy_good_success'] = self.refresh_lottery_limit_count
        if self.goods_got_func:
            econf['buy_good_success_with_list'] = self.on_buy_good_success_with_list
        if self._is_show_luck_rank_list:
            econf['message_on_luck_rank_like_data'] = self.refresh_rank_likes_red_point
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)

    def destroy_widget(self, widget_name):
        widget = getattr(self, widget_name, None)
        if widget:
            widget.destroy()
            setattr(self, widget_name, None)
        return

    def on_finalize_panel(self):
        self.parent = None
        if self.panel:
            self.panel.stopAllActions()
            self.panel = None
        self.data = None
        self.on_change_show_reward = None
        self.process_event(False)
        return

    def check_buy_action_disabled(self, lottery_count):
        if is_mainland_package() and self.cur_lottery_count + lottery_count > self.max_lottery_count:
            global_data.game_mgr.show_tip(get_text_by_id(82040))
            return True
        return False

    def refresh_lottery_limit_count(self):
        if not is_mainland_package() or not global_data.player:
            return
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        global_data.emgr.refresh_lottery_limit_count.emit(self.lottery_id, self.max_lottery_count - self.cur_lottery_count)

    def on_buy_good_success_with_list(self, goods_list):
        if not self.goods_got_func:
            return
        else:
            for goods_id, pay_num, goods_type, need_show, reward_list, reason, payment, lucky_list in goods_list:
                if goods_id in self.goods_got_func:
                    from logic.gutils.item_utils import get_lobby_item_usage, try_use_lobby_item
                    from logic.gutils import mall_utils
                    item_no = mall_utils.get_goods_item_no(goods_id)
                    it = global_data.player.get_item_by_no(item_no)
                    if it:
                        item_data = {'id': it.id,'item_no': it.item_no,
                           'quantity': it.get_current_stack_num()
                           }
                        usage_type = self.goods_got_func.get(str(goods_id), '')
                        usage = get_lobby_item_usage(None, usage_type)
                        if usage:
                            try_use_lobby_item(item_data, usage)
                    else:
                        log_error('goods_got_func:get goods item failed')

            return

    def refresh_rank_likes_red_point(self, *args):
        has_red_point = check_lucky_score_rank_likes_red_point(self.lottery_id)
        btn_rank_lucky = self.panel.btn_rank_lucky
        if btn_rank_lucky:
            btn_rank_lucky.red_point.setVisible(has_red_point)

    def show(self):
        raise NotImplementedError('LotteryBaseWidget::show should be overridden')

    def hide(self):
        raise NotImplementedError('LotteryBaseWidget::hide should be overridden')

    def refresh(self):
        raise NotImplementedError('LotteryBaseWidget::refresh should be overridden')

    def refresh_show_model(self, show_model_id=None):
        raise NotImplementedError('LotteryBaseWidget::refresh_show_model should be overridden')

    def switch_show_model(self, offset):
        pass

    def hide_preview_widget(self):
        pass

    def jump_to_exchange_shop_widget(self, goods_id, check=True):
        pass

    def get_cur_show_model_id(self):
        return self.show_model_id

    def on_begin_drag_model(self):
        pass

    def on_end_drag_model(self):
        pass