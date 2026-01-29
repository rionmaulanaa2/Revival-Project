# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryCommonBingoWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from .LotteryBaseWidget import LotteryBaseWidget
from logic.comsys.lobby.EntryWidget.ArtCollectionActivityEntryWidget import ArtCollectionActivityEntryWidget
from .LotteryBingoWidget import LotteryBingoWidget
from .LotteryBuyWidget import LotteryBuyWidget
from .LotteryShopWidget import LotteryShopWidget
from .LotteryTicketChargeUI import LotteryTicketChargeUI
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, DARK_PRICE_COLOR, LOTTERY_ST_OPEN_ONLY_EXCHANGE
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.mall_utils import get_lottery_preview_data, get_lottery_exchange_list, get_cur_lottery_state
from logic.gutils.template_utils import init_tempate_mall_i_simple_item
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.cocos_utils import ccc4FromHex
from common.cfg import confmgr
from logic.gutils import task_utils, template_utils
DEFAULT_ICON_PATH = 'gui/ui_res_2/lottery/icon_lottery_gift.png'
DEFAULT_TXT_COLOR = 16776169
DEFAULT_OUT_LINE = 9048633
CONNECT_LINE_TASK_ID = '1420077'

class LotteryCommonBingoWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryCommonBingoWidget, self).init_parameters()
        self.ignore_item_scene = True
        self.is_visible_close = False
        self.skip_anim_archive_data = ArchiveManager().get_archive_data('lottery_turntable_skip_anim')
        self.need_skip_anim = self.skip_anim_archive_data.get(self.lottery_id, False)
        self.guarantee_count = get_lottery_preview_data(self.lottery_id)['guarantee_count']

    def on_set_skip_anim_flag(self, btn):
        btn.SetSelect(self.need_skip_anim)
        btn.img_skip and btn.img_skip.setVisible(self.need_skip_anim)

    def init_panel(self):
        super(LotteryCommonBingoWidget, self).init_panel()

        @global_unique_click(self.panel.btn_reward)
        def OnClick(*args):
            self.panel.bar_list.setVisible(not self.panel.bar_list.isVisible())

        conf = get_lottery_preview_data(self.lottery_id)
        core_reward_id_list = conf['core_rewards']
        self.panel.list_reward.SetInitCount(len(core_reward_id_list))
        for i in range(len(core_reward_id_list)):
            init_tempate_mall_i_simple_item(self.panel.list_reward.GetItem(i), core_reward_id_list[i], show_tips=True)

        @global_unique_click(self.panel.btn_reward)
        def OnClick(*args):
            visible = not self.panel.list_reward.isVisible()
            self.panel.list_reward.setVisible(visible)
            self.panel.btn_reward.lab_name.SetString(860007 if visible else 80765)

        self.panel.list_reward.setVisible(True)
        OnClick()

        @global_unique_click(self.panel.btn_question)
        def OnClick(btn, touch):
            dlg = GameRuleDescUI()
            title, content = self.data.get('rule_desc', [608080, 608081])
            dlg.set_lottery_rule(title, content)

        if self.panel.btn_skip:

            @global_unique_click(self.panel.btn_skip)
            def OnClick(btn, touch):
                self.need_skip_anim = not self.need_skip_anim
                self.on_set_skip_anim_flag(btn)

            self.on_set_skip_anim_flag(self.panel.btn_skip)

        @global_unique_click(self.panel.btn_shop)
        def OnClick(*args):
            if not self.shop_widget:
                return
            exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
            if self.lottery_id not in lottery_exchange_goods:
                global_data.game_mgr.show_tip(get_text_by_id(12128))
                return
            if self.panel.nd_content.isVisible():
                self.shop_widget.parent_show()
            else:
                self.shop_widget.parent_hide()

        @global_unique_click(self.panel.nd_shop.temp_btn_close.btn_back)
        def OnClick(*args):
            self.shop_widget and self.shop_widget.parent_hide()

        self.panel_valid_anim = []
        anim_names = ('show', 'loop')
        for anim_name in anim_names:
            self.panel.HasAnimation(anim_name) and self.panel_valid_anim.append(anim_name)

        if self.panel.HasAnimation('btn_loop'):
            self.panel_valid_anim.append('btn_loop')
            self.panel.RecordAnimationNodeState('btn_loop')
        self.panel.nd_tips.setVisible(False)
        self.panel.lab_btn_text.SetString(601227)
        extra_data = self.data.get('extra_data', {})
        icon_path = extra_data.get('icon_path', DEFAULT_ICON_PATH) if extra_data else DEFAULT_ICON_PATH
        txt_color = eval(extra_data.get('text_color', DEFAULT_TXT_COLOR)) if extra_data else DEFAULT_TXT_COLOR
        out_line = eval(extra_data.get('out_line', DEFAULT_OUT_LINE)) if extra_data else DEFAULT_OUT_LINE
        self.panel.btn_activity.SetFrames('', [icon_path, icon_path, icon_path], False, None)
        self.panel.lab_btn_text.SetColor(txt_color)
        self.panel.lab_btn_text.EnableOutline(ccc4FromHex(out_line), 1)
        self.init_temporary_activity_entrance()
        self.init_bingo_widget()
        self.init_buy_widget()
        self.init_shop_widget()
        self.check_show_shop()
        self.init_connect_line_task_widget()
        return

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended
           }
        return econf

    def init_temporary_activity_entrance(self):
        if 'remind_jump_ui' in self.data:
            conf = confmgr.get('c_activity_config', str(self.data.get('charge_activity')), default={})
            template = conf.get('cUiTemplate', None).strip()
            ui_class = conf.get('cUiClass', None)
            LotteryTicketChargeUI.set_ui_info(template, ui_class, self.data.get('charge_activity'))
            self.activity_button_widget = ArtCollectionActivityEntryWidget(self.panel, self.panel, self.data.get('activity_type'), self.data['remind_jump_ui'][0], self.data['remind_jump_ui'][1], 'btn_activity')
        else:
            self.activity_button_widget = None
        return

    def init_bingo_widget(self):
        self.bingo_widget = LotteryBingoWidget(self, self.panel, self.lottery_id, self.on_change_show_reward, six_ex.keys(global_data.player.get_reward_intervene_count(self.data['table_id'])), self.panel.list_item, self.panel.list_reward_v, self.panel.list_reward_h, self.panel.temp_reward_h, self.panel.temp_reward_v)

    def _play_buy_button_loop_anim(self):
        self.panel.PlayAnimation('btn_loop')

    def _stop_buy_button_loop_anim(self):
        self.panel.StopAnimation('btn_loop')
        self.panel.RecoverAnimationNodeState('btn_loop')

    def buying_callback(self, lottery_count):
        self._stop_buy_button_loop_anim()

    def lottery_data_ready_callback(self, bought_successfully):
        if not bought_successfully:
            self._play_buy_button_loop_anim()

    def init_buy_widget(self):
        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_repeat
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once.temp_price,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_repeat.temp_price
           }, price_color=DARK_PRICE_COLOR)

    def set_visible_close(self, is_visible_close):
        self.is_visible_close = is_visible_close

    def check_show_shop(self):
        if self.is_visible_close and self.data.get('show_shop', False):
            self.shop_widget and self.shop_widget.parent_show()
            self.panel.nd_granbelm.setVisible(False)
            self.panel.nd_shop.temp_btn_close.setVisible(False)
            return True
        return False

    def set_shop_visible(self, visible):
        self.panel.nd_shop.setVisible(visible)
        self.panel.nd_content.setVisible(not visible)
        self.panel.nd_prog_line.setVisible(not visible)
        self.panel.btn_shop.SetSelect(visible)

    def shop_show_callback(self):
        self.set_shop_visible(True)
        self.panel.PlayAnimation('shop_in')

    def shop_hide_callback(self):
        self.set_shop_visible(False)
        self.panel.PlayAnimation('shop_out')
        self.refresh_show_model()

    def init_shop_widget(self):
        self.shop_widget = LotteryShopWidget(self.panel.nd_shop, self.panel, self.on_change_show_reward, self.lottery_id, show_callback=self.shop_show_callback, hide_callback=self.shop_hide_callback)

    def on_finalize_panel(self):
        super(LotteryCommonBingoWidget, self).on_finalize_panel()
        if self.activity_button_widget:
            self.activity_button_widget.destroy()
            self.activity_button_widget = None
        if self.bingo_widget:
            self.bingo_widget.destroy()
            self.bingo_widget = None
        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        if self.shop_widget:
            self.shop_widget.destroy()
            self.shop_widget = None
        self.skip_anim_archive_data[self.lottery_id] = self.need_skip_anim
        self.skip_anim_archive_data.save()
        self.skip_anim_archive_data = None
        return

    def play_panel_show_anim(self, flag):
        func = self.panel.PlayAnimation if flag else self.panel.StopAnimation
        for anim_name in self.panel_valid_anim:
            func(anim_name)

    def _show_shop(self):
        if not self.panel.nd_content.isVisible():
            self.shop_widget.parent_show()

    def show(self):
        self.panel.setVisible(True)
        self.play_panel_show_anim(True)
        if not self.check_show_shop():
            self._show_shop()

    def hide(self):
        self.panel.setVisible(False)
        self.play_panel_show_anim(False)
        self.shop_widget and self.shop_widget.process_event(False)

    def do_hide_panel(self):
        self.shop_widget and self.shop_widget.process_event(False)

    def refresh(self):
        self.update_lucky_value()

    def refresh_show_model(self, show_model_id=None):
        if self.panel.nd_shop.isVisible() and not self.panel.IsPlayingAnimation('shop_out'):
            self.shop_widget and self.shop_widget.refresh_show_model()
        else:
            self.bingo_widget.refresh_show_model(show_model_id)

    def update_lucky_value(self):
        cur_lucky_value = global_data.player.get_reward_count(self.data['table_id'])
        self.panel.lab_lucky_value.SetString('{}/{}'.format(cur_lucky_value, self.guarantee_count))
        self.panel.progress.SetPercent(100.0 * cur_lucky_value / self.guarantee_count)

    def on_receive_lottery_result(self, item_list, origin_list, extra_data):
        if not extra_data:
            log_error('bingo\xe6\x8a\xbd\xe5\xa5\x96\xe4\xb8\x8d\xe5\x8f\x91\xe4\xb8\x8b\xe6\xa0\x87\xef\xbc\x8c\xe6\x83\xb3\xe5\xb9\xb2\xe5\x98\x9b')
            return
        self.bingo_widget.set_bingo_opened(item_list, origin_list, extra_data)

    def on_lottery_ended(self):
        if not self.panel.isVisible():
            return
        self._play_buy_button_loop_anim()
        self.update_lucky_value()
        self.update_list_core_reward()

    def jump_to_exchange_shop_widget(self, goods_id, check=True):
        if not self.shop_widget:
            return
        exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
        if self.lottery_id not in lottery_exchange_goods:
            global_data.game_mgr.show_tip(get_text_by_id(12128))
            return
        if not check or self.panel.nd_content.isVisible() or get_cur_lottery_state(self.data['single_goods_id'], self.data['visible_ts']) == LOTTERY_ST_OPEN_ONLY_EXCHANGE:
            self.shop_widget.parent_show(goods_id)

    def init_connect_line_task_widget(self):
        list_core_reward = self.panel.list_core_reward
        task_reward_list = task_utils.get_prog_rewards(CONNECT_LINE_TASK_ID)
        list_core_reward_len = 5
        task_progress = global_data.player.get_task_prog(CONNECT_LINE_TASK_ID)
        total_progress = task_utils.get_total_prog(CONNECT_LINE_TASK_ID)
        self.panel.nd_prog_line.vx_progress_line.progress_line.SetPercent(100.0 * task_progress / total_progress)
        num_item = list_core_reward.__getattribute__('temp_data_%d' % (list_core_reward_len - 1))
        num_item.setVisible(False)
        num_item.lab_num.SetString(str(task_progress))
        num_item.lab_name.SetString(610286)
        list_core_reward.temp_data_0.img_lock.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202112/christmas/bingo/bar_christmas_lock2.png')
        list_core_reward.temp_data_0.bar_item.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202112/christmas/bingo/bar_christmas_item_top.png')
        for index, task_reward in enumerate(task_reward_list):
            reward_list = confmgr.get('common_reward_data', str(task_reward[1]), 'reward_list', default=[])
            reward_item_id = reward_list[0][0]
            reward_item_cnt = reward_list[0][1]
            btn_index = list_core_reward_len - 2 - index
            list_item = list_core_reward.__getattribute__('temp_data_%d' % btn_index)
            list_item.setVisible(False)
            list_item.lab_name.SetString(get_text_by_id(610287).format(task_reward[0]))
            template_utils.init_tempate_mall_i_item(list_item.temp_item, reward_item_id, reward_item_cnt, show_tips=False)
            if global_data.player.has_receive_prog_reward(CONNECT_LINE_TASK_ID, task_reward[0]):
                list_item.nd_got.setVisible(True)
                list_item.img_light.setVisible(False)
                btn = list_item.temp_item.btn_choose
                btn.SetSelect(False)
            if task_progress >= task_reward[0] and not global_data.player.has_receive_prog_reward(CONNECT_LINE_TASK_ID, task_reward[0]):
                list_item.img_light.setVisible(True)

            @list_item.temp_item.btn_choose.unique_callback()
            def OnClick(btn, touch, btn_index=btn_index, reward_prog=task_reward[0], reward_item_id=reward_item_id, reward_item_cnt=reward_item_cnt):
                task_progress = global_data.player.get_task_prog(CONNECT_LINE_TASK_ID)
                if task_progress >= reward_prog and not global_data.player.has_receive_prog_reward(CONNECT_LINE_TASK_ID, reward_prog):
                    btn.SetSelect(False)
                    item = list_core_reward.__getattribute__('temp_data_%d' % btn_index)
                    item.nd_got.setVisible(True)
                    item.img_light.setVisible(False)
                    global_data.player.receive_task_prog_reward(CONNECT_LINE_TASK_ID, reward_prog)
                elif reward_item_id == 201800144:
                    self.on_change_show_reward(str(reward_item_id))
                else:
                    x, y = btn.GetPosition()
                    w, h = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(reward_item_id, None, wpos, item_num=reward_item_cnt)
                return

        self.show_next_animation(list_core_reward_len - 1)
        if task_progress == total_progress and not global_data.player.has_receive_prog_reward(CONNECT_LINE_TASK_ID, total_progress):
            global_data.player.receive_task_prog_reward(CONNECT_LINE_TASK_ID, task_progress)
            list_item = list_core_reward.__getattribute__('temp_data_0')
            list_item.nd_got.setVisible(True)
            list_item.img_light.setVisible(False)

    def update_list_core_reward(self):
        list_core_reward = self.panel.list_core_reward
        list_core_reward_len = 5
        task_progress = global_data.player.get_task_prog(CONNECT_LINE_TASK_ID)
        total_progress = task_utils.get_total_prog(CONNECT_LINE_TASK_ID)
        if task_progress == total_progress:
            global_data.player.receive_task_prog_reward(CONNECT_LINE_TASK_ID, task_progress)
            lst_item = list_core_reward.__getattribute__('temp_data_0')
            lst_item.nd_got.setVisible(True)
            lst_item.img_light.setVisible(False)
            return
        task_reward_list = task_utils.get_prog_rewards(CONNECT_LINE_TASK_ID)
        self.panel.nd_prog_line.vx_progress_line.progress_line.SetPercent(100.0 * task_progress / total_progress)
        list_core_reward.__getattribute__('temp_data_%d' % (list_core_reward_len - 1)).lab_num.SetString(str(task_progress))
        for index, task_reward in enumerate(task_reward_list):
            reward_prog = task_reward[0]
            if task_progress >= reward_prog:
                if not global_data.player.has_receive_prog_reward(CONNECT_LINE_TASK_ID, reward_prog):
                    self.panel.list_core_reward.__getattribute__('temp_data_%d' % (list_core_reward_len - 2 - index)).img_light.setVisible(True)
            else:
                break

    def show_next_animation(self, index):
        if index < 0:
            return
        import cc
        item = self.panel.nd_prog_line.list_core_reward.__getattribute__('temp_data_%d' % index)
        item.setVisible(True)
        item.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : item.PlayAnimation('show')),
         cc.DelayTime.create(item.GetAnimationMaxRunTime('show')),
         cc.DelayTime.create(0.04),
         cc.CallFunc.create(lambda : self.show_next_animation(index - 1))]))