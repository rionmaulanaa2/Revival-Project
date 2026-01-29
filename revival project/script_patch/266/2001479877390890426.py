# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonPassRetrospectUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from logic.client.const import lobby_model_display_const
from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils, task_utils, template_utils
import logic.gutils.season_utils as season_utils
from common.const import uiconst
import time
from logic.gutils.advance_utils import create_black_canvas
from common.cfg import confmgr
from logic.gutils.template_utils import init_tempate_mall_i_item
from .SeasonBaseUIWidget import SeasonBaseUIWidget
from .BattlePassDisplayWidget import BattlePassDisplayWidget
from logic.gutils import item_utils
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO, SHOP_PAYMENT_ITEM
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_const.scene_const import SCENE_JIEMIAN_COMMON, SCENE_SAIJIKA
from logic.gutils.client_utils import post_ui_method
BASE_TASK = 1
ADVANCED_TASK = 2
ULTIMATE_TASK = 3
NA_SEASON_DIFF = 5

class SeasonPassRetrospectChooseUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/bp_retrospect/open_bp_retrospect'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close',
       'btn_describe.OnClick': 'show_describe'
       }
    GLOBAL_EVENT = {'retrospect_season_unlocked': 'update_season_list',
       'player_money_info_update_event': 'update_season_list',
       'buy_good_success': ('update_season_list', 'on_buy_succeed'),
       'receive_task_reward_succ_event': 'update_season_list',
       'receive_task_prog_reward_succ_event': 'update_season_list',
       'retrospect_task_unlocked': 'update_season_list',
       'task_prog_changed': 'update_season_list'
       }

    def do_show_panel(self):
        super(SeasonPassRetrospectChooseUI, self).do_show_panel()
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, lobby_model_display_const.BATTLE_PASS, scene_content_type=SCENE_SAIJIKA, scene_background_texture=self.background_texture, change_saijika_background=True)

    def on_init_panel(self, close_callback, *args):
        self.close_cb = close_callback
        self.init_parameters()
        self.init_season_list()
        self.init_price_widget()
        self._init_season_time()
        self.enter_retrospect_system()

    def init_parameters(self):
        conf = confmgr.get('season_retrospect_info')
        self.open_season = conf.get('open_season', [])
        self.act_item = conf.get('act_item', None)
        self.goods_id = conf.get('goods_id', None)
        self.act_num = conf.get('act_num', 2)
        self.background_texture = conf.get('background_texture', 'model_new/xuanjue/xuanjue_new/textures/zhanshi_pifu_sshuoliuxing.tga')
        self.season_dict = {}
        for season in self.open_season:
            self.season_dict[season] = confmgr.get('season_retrospect_{}'.format(season))

        return

    def init_season_list(self):
        season_list = self.panel.list_item
        season_list.SetInitCount(len(self.open_season))
        for idx, item in enumerate(season_list.GetAllItem()):
            season_title = self.season_dict[self.open_season[idx]].get('season_title')
            season_describe = self.season_dict[self.open_season[idx]].get('season_describe')
            item.lab_title.SetString(get_text_by_id(season_title).format(G_IS_NA_PROJECT or self.open_season[idx] if 1 else self.open_season[idx] + NA_SEASON_DIFF))
            item.list_content.SetInitCount(1)
            item.list_content.GetItem(0).lab_describe.SetString(get_text_by_id(season_describe))
            img_path = 'gui/ui_res_2/battle_pass/retrospect/main/icon_retrospect_s{}_{}.png'.format(self.open_season[idx], self.open_season[idx] + NA_SEASON_DIFF)
            item.img_logo.SetDisplayFrameByPath('', img_path)

        self.update_season_list()

    def init_price_widget(self):
        self.price_widget = PriceUIWidget(self.panel, call_back=None, list_money_node=self.panel.list_money)
        self.price_widget.set_exchange_item_dict({self.act_item: self.goods_id})
        self.price_widget.show_money_types([SHOP_PAYMENT_YUANBAO, '{}_{}'.format(SHOP_PAYMENT_ITEM, self.act_item)])
        return

    def _init_season_time(self):
        from logic.gcommon.cdata import season_data
        from logic.gcommon import time_utility
        cur_season = global_data.player.get_battle_season()
        start_timestamp = season_data.get_start_timestamp(cur_season)
        end_timestamp = season_data.get_end_timestamp(cur_season)
        now = time_utility.time()
        if now < start_timestamp:
            self.panel.lab_tips_time.SetString(608052)
        elif now > end_timestamp:
            self.panel.lab_tips_time.SetString(608051)
        else:
            day, _, _, _ = time_utility.get_day_hour_minute_second(end_timestamp - now)
            self.panel.lab_tips_time.SetString(get_text_by_id(608050).format(day))

    def enter_retrospect_system(self):
        player = global_data.player
        if player:
            player.on_enter_retrospect_system()

    def on_buy_succeed(self):
        global_data.game_mgr.show_tip(get_text_by_id(81001))

    @post_ui_method
    def update_season_list(self, *args):
        for idx, item in enumerate(self.panel.list_item.GetAllItem()):
            money_type = mall_utils.get_item_money_type(int(self.act_item))
            coin_num = mall_utils.get_my_money(money_type)
            if self.act_num > coin_num:
                num_text = '<color=0xe0382fff>{}</color>' if 1 else '{}'
                item.nd_btn.nd_cost.lab_num.SetString(num_text.format(self.act_num))
                img_path = item_utils.get_money_icon(money_type)
                item.nd_btn.nd_cost.icon.SetDisplayFrameByPath('', img_path)
                prog, total = global_data.player.get_retrospect_prog(self.open_season[idx])
                item.lab_prog.SetString(get_text_by_id(634998).format(prog, total))
                if not global_data.player.is_season_retrospect_unlocked(self.open_season[idx]):
                    item.temp_btn_1.btn_common.SetText(get_text_by_id(634482))
                    item.temp_btn_1.btn_common.SetSelect(False)

                    @item.temp_btn_1.btn_common.unique_callback()
                    def OnClick(btn, touch, idx=idx, season=self.open_season[idx]):
                        coin_num = mall_utils.get_my_money(money_type)
                        if coin_num < self.act_num:
                            from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
                            GroceriesBuyConfirmUI(goods_id=self.goods_id, init_quantity=self.act_item - coin_num)
                        else:

                            def confirm_callback():
                                global_data.player.unlock_retrospect_season(season)

                            NormalConfirmUI2(on_confirm=confirm_callback, content=get_text_by_id(634502).format('"' + item_utils.get_lobby_item_pic_by_item_no(self.act_item) + '"', self.act_num), cancel_text=get_text_by_id(90005))

                else:
                    item.nd_btn.nd_cost.setVisible(False)
                    if global_data.player.is_retrospect_season_finished(self.open_season[idx]):
                        item.temp_btn_1.btn_common.SetText(get_text_by_id(634500))
                        item.temp_btn_1.btn_common.SetEnable(False)
                        item.temp_btn_1.img_num.setVisible(False)
                    else:
                        item.temp_btn_1.btn_common.SetText(get_text_by_id(634483))
                        item.temp_btn_1.btn_common.SetSelect(True)
                        item.temp_btn_1.btn_common.SetEnable(True)
                        cnt = global_data.player.get_unreceived_task_cnt(self.open_season[idx])
                        if cnt > 0:
                            item.temp_btn_1.img_num.setVisible(True)
                            item.temp_btn_1.img_num.lab_num.SetString(str(cnt))
                        else:
                            item.temp_btn_1.img_num.setVisible(False)

                        @item.temp_btn_1.btn_common.unique_callback()
                        def OnClick(btn, touch, idx=idx):
                            self.hide()
                            RetroSpectMainUI(None, self.season_dict[self.open_season[idx]], self.open_season[idx], self.ui_close_callback, True, self.act_item, self.goods_id)
                            return

                @item.btn_show.unique_callback()
                def OnClick(btn, touch, idx=idx):
                    self.hide()
                    RetroSpectMainUI(None, self.season_dict[self.open_season[idx]], self.open_season[idx], self.ui_close_callback, False, self.act_item, self.goods_id)
                    return

    def ui_close_callback(self):
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, lobby_model_display_const.BATTLE_PASS, scene_content_type=SCENE_SAIJIKA, scene_background_texture=self.background_texture, change_saijika_background=True)
        self.show()

    def show_describe(self, *args):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(634473, 634999)

    def on_close(self, *args):
        self.close_cb()
        self.close()


class RetroSpectMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/bp_retrospect/open_bp_retrospect_switch'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'retrospect_season_unlocked': 'switch_to_task',
       'task_prog_changed': 'update_panel',
       'receive_task_reward_succ_event': 'update_panel',
       'receive_task_prog_reward_succ_event': 'update_panel'
       }

    def do_show_panel(self):
        super(RetroSpectMainUI, self).do_show_panel()
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, lobby_model_display_const.BATTLE_PASS, scene_content_type=SCENE_SAIJIKA, scene_background_texture=self.background_texture, change_saijika_background=True)
        self.reward_widget.reset_display_type = True
        self.task_widget.reset_display_type = True

    def on_init_panel(self, reward_info, season, close_callback, hide_reward, act_item, act_goods):
        self.close_cb = close_callback
        self.season = season
        self.reward_widget = RetrospectRewardPreviewWidget(self, self.panel.temp_reward_show, reward_info, season, lambda : self.switch_widget(True))
        self.task_widget = RetrospectTaskWidget(self, self.panel.temp_task, reward_info, season, lambda : self.switch_widget(False))
        self.reward_info = reward_info
        self._task_unlock_coin = reward_info.get('task_unlock_coin', None)
        self.goods_id = reward_info.get('goods_id', None)
        self._u_task_unlock_coin = reward_info.get('u_task_unlock_coin', None)
        self.u_goods_id = reward_info.get('u_goods_id', None)
        self.all_task = reward_info.get('base_task', []) + reward_info.get('advanced_task', []) + reward_info.get('ultimate_task', [])
        self.panel.btn_close.BindMethod('OnClick', self.on_click_close)
        self.background_texture = reward_info.get('background_texture', 'model_new/xuanjue/xuanjue_new/textures/zhanshi_pifu_sxxxkt.tga')
        self.act_item = act_item
        self.act_goods = act_goods
        self.init_panel()
        self._init_ui_event()
        self.switch_widget(hide_reward)
        self.init_price_widget()
        self.update_panel()
        return

    def init_panel(self):
        img_path = 'gui/ui_res_2/battle_pass/retrospect/main/icon_retrospect_s{}_{}.png'.format(self.season, self.season + NA_SEASON_DIFF)
        self.panel.icon_season.SetDisplayFrameByPath('', img_path)
        self.panel.lab_title.SetString(get_text_by_id(self.reward_info.get('season_title')).format(G_IS_NA_PROJECT or self.season if 1 else self.season + NA_SEASON_DIFF))

    def init_price_widget(self):
        self.price_widget = PriceUIWidget(self.panel, call_back=None, list_money_node=self.panel.list_money)
        exc_dict = {self._task_unlock_coin: self.goods_id,self._u_task_unlock_coin: self.u_goods_id,self.act_item: self.act_goods}
        self.price_widget.set_exchange_item_dict(exc_dict)
        self.price_widget.show_money_types([SHOP_PAYMENT_YUANBAO, '{}_{}'.format(SHOP_PAYMENT_ITEM, self._task_unlock_coin), '{}_{}'.format(SHOP_PAYMENT_ITEM, self._u_task_unlock_coin), '{}_{}'.format(SHOP_PAYMENT_ITEM, self.act_item)])
        return

    def update_panel(self, *args):
        finished_task_cnt = 0
        for task_id in self.all_task:
            if global_data.player.is_retrospect_task_finished(task_id):
                finished_task_cnt += 1

        self.panel.lab_prog.SetString(get_text_by_id(634495).format(finished_task_cnt, len(self.all_task)))

    def _init_ui_event(self):
        from logic.gcommon.common_const.battlepass_const import ROTATE_FACTOR

        def on_model_drag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        self.panel.nd_special_reward.BindMethod('OnDrag', on_model_drag)

    def switch_widget(self, hide_reward):
        from logic.gcommon.common_const.scene_const import SCENE_SAIJIKA
        if global_data.ex_scene_mgr_agent.is_cur_lobby_relatived_scene(SCENE_SAIJIKA):
            global_data.emgr.change_model_display_scene_item.emit(None)
        if hide_reward:
            self.reward_widget.hide()
            self.task_widget.show()
        else:
            self.reward_widget.show()
            self.task_widget.hide()
        return

    def switch_to_task(self):
        self.switch_widget(True)

    def on_click_close(self, btn, touch):
        self.close_cb()
        self.close()

    def on_finalize_panel(self):
        self.destroy_widget('reward_widget')
        self.destroy_widget('task_widget')
        super(RetroSpectMainUI, self).on_finalize_panel()


class RetrospectRewardPreviewWidget(SeasonBaseUIWidget):

    def __init__(self, parent, panel, reward_info, season, close_callback, *args):
        super(RetrospectRewardPreviewWidget, self).__init__(parent, panel)
        self.parent = parent
        self.panel = panel
        self.season = season
        self.close_cb = close_callback
        self.reward_info = reward_info
        self._select_item = None
        self._displaying_item_no = None
        self.reset_display_type = True
        self._display_widget = BattlePassDisplayWidget(display_cb=self._display_cb)
        global_data.emgr.retrospect_season_unlocked += self.update_btn
        global_data.emgr.receive_task_reward_succ_event += self.update_preivew_reward
        global_data.emgr.receive_task_prog_reward_succ_event += self.update_preivew_reward
        self._init_panel()
        return

    def _init_panel(self):
        self._low_core_award_lst = []
        self._high_core_award_lst = []
        self.panel.btn_close.BindMethod('OnClick', self.on_switch_to_task)
        self.init_reward_list()
        self.update_btn()

    def init_reward_list(self):
        advanced_task = self.reward_info.get('advanced_task', [])
        ultimate_task = self.reward_info.get('ultimate_task', [])
        reward_lst_nodes = [self.panel.list_basis_award, self.panel.list_advanced_award]
        for reward_lst in reward_lst_nodes:
            if reward_lst == self.panel.list_basis_award:
                self._low_core_award_lst = self._get_item_info_lst(advanced_task)
                cap = len(self._low_core_award_lst)
            else:
                self._high_core_award_lst = self._get_item_info_lst(ultimate_task)
                cap = len(self._high_core_award_lst)
            reward_lst.BindMethod('OnCreateItem', self._on_create_callback)
            reward_lst.SetInitCount(cap)

    @post_ui_method
    def update_btn(self):
        is_season_retrospect_unlocked = global_data.player and global_data.player.is_season_retrospect_unlocked(self.season)
        self.panel.btn_close.setVisible(is_season_retrospect_unlocked)
        self.panel.nd_btn.setVisible(not is_season_retrospect_unlocked)
        conf = confmgr.get('season_retrospect_info')
        act_item = conf.get('act_item', None)
        act_num = conf.get('act_num', 2)
        money_type = mall_utils.get_item_money_type(int(act_item))
        coin_num = mall_utils.get_my_money(money_type)
        img_path = item_utils.get_money_icon(money_type)
        self.panel.bar_cost.icon.SetDisplayFrameByPath('', img_path)
        self.panel.bar_cost.lab_num.SetString(str(act_num))
        self.panel.temp_btn_1.btn_common.SetText(get_text_by_id(634482))
        if coin_num < act_num:
            self.panel.temp_btn_1.btn_common.SetEnable(False)
        else:
            self.panel.temp_btn_1.btn_common.SetEnable(True)

            @self.panel.temp_btn_1.btn_common.unique_callback()
            def OnClick(btn, touch, season=self.season):

                def confirm_callback():
                    global_data.player.unlock_retrospect_season(season)

                NormalConfirmUI2(on_confirm=confirm_callback, content=get_text_by_id(634502).format('"' + item_utils.get_lobby_item_pic_by_item_no(act_item) + '"', act_num), cancel_text=get_text_by_id(90005))

        return

    def update_preivew_reward(self, *args):
        for idx, item in enumerate(self.panel.list_basis_award.GetAllItem()):
            if len(self._low_core_award_lst) > idx and hasattr(item, 'nd_get'):
                item.nd_get.setVisible(global_data.player.has_item_by_no(self._low_core_award_lst[idx][0]))

        for idx, item in enumerate(self.panel.list_advanced_award.GetAllItem()):
            if len(self._high_core_award_lst) > idx and hasattr(item, 'nd_get'):
                item.nd_get.setVisible(global_data.player.has_item_by_no(self._high_core_award_lst[idx][0]))

    def on_switch_to_task(self, btn, touch):
        self.parent.switch_widget(True)

    def _get_item_info_lst(self, task_list):
        ret = []
        for task_id in task_list:
            reward_id = task_utils.get_task_reward(task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id_lst = reward_conf.get('reward_list', [])
            for reward in item_id_lst:
                ret.append(reward)

        return ret

    def _on_create_callback(self, lv, idx, ui_item):
        if lv == self.panel.list_basis_award:
            item_no, item_num = self._low_core_award_lst[idx]
        else:
            item_no, item_num = self._high_core_award_lst[idx]
        if idx + 1 == len(lv.GetAllItem()) and lv == self.panel.list_advanced_award:
            ui_item.img_tag_prize.setVisible(True)
        elif idx + 1 == len(lv.GetAllItem()) - len(self.reward_info.get('extra_task', [])) and lv == self.panel.list_basis_award:
            ui_item.img_tag_prize.setVisible(True)

        def on_click_callback(sel_item=ui_item, data=item_no):
            self._displaying_item_no = data
            self._display_widget.display_award(data, self.reset_display_type)
            if self._select_item and self._select_item.isValid():
                self._select_item.btn_choose.SetSelect(False)
            self._select_item = sel_item
            self._select_item.btn_choose.SetSelect(True)

        init_tempate_mall_i_item(ui_item, item_no, item_num=item_num, isget=global_data.player.has_item_by_no(item_no), callback=on_click_callback)

    def _display_cb(self, is_model, item_no):
        super(RetrospectRewardPreviewWidget, self)._display_cb(is_model, item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        item_desc = item_utils.get_lobby_item_desc(item_no)
        if is_model:
            self.parent.panel.nd_special_reward.img_bar.lab_name.SetString(item_name)
            self.parent.panel.nd_special_reward.img_bar.lab_describe.SetString(item_desc)
            self.parent.panel.nd_special_reward.img_bar.lab_name.setVisible(True)
            self.reset_display_type = False
        else:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            self.parent.panel.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', pic_path)
            self.parent.panel.nd_common_reward.lab_name.SetString(item_name)
            self.parent.panel.nd_common_reward.lab_describe.SetString(item_desc)
        self.parent.panel.nd_special_reward.setVisible(is_model)
        self.parent.panel.nd_common_reward.setVisible(not is_model)

    def on_click_close(self, *args):
        if self._display_widget:
            self._display_widget.clear_model_display()
        self.close_cb()
        self.close()

    def show(self):
        super(RetrospectRewardPreviewWidget, self).show()
        self.reset_display_type = True
        first_item = self.panel.list_advanced_award.GetItem(0)
        if not first_item:
            first_item = self.panel.list_basis_award.GetItem(0)
        first_item and first_item.btn_choose.OnClick(None)
        return

    def hide(self):
        super(RetrospectRewardPreviewWidget, self).hide()

    def destroy(self):
        self.destroy_widget('_display_widget')
        super(RetrospectRewardPreviewWidget, self).destroy()


class RetrospectTaskWidget(SeasonBaseUIWidget):

    def __init__(self, parent, panel, task_info, season, preview_cb, *args):
        super(RetrospectTaskWidget, self).__init__(parent, panel)
        self.parent = parent
        self.panel = panel
        self.season = season
        self.preview_cb = preview_cb
        self.task_info = task_info
        self._select_item = None
        self.reset_display_type = True
        self._displaying_item_no = None
        self._base_task = task_info.get('base_task', [])
        self._advanced_task = task_info.get('advanced_task', [])
        self._ultimate_task = task_info.get('ultimate_task', [])
        self._extra_task = task_info.get('extra_task', [])
        self._goods_id = task_info.get('goods_id', None)
        self._u_goods_id = task_info.get('u_goods_id', None)
        self._display_widget = BattlePassDisplayWidget(display_cb=self._display_cb)
        global_data.emgr.retrospect_task_unlocked += self.update_task_list
        global_data.emgr.task_prog_changed += self.update_task_list
        global_data.emgr.receive_task_reward_succ_event += self.update_task_list
        global_data.emgr.receive_task_prog_reward_succ_event += self.update_task_list
        global_data.emgr.player_money_info_update_event += self.update_task_list
        global_data.emgr.buy_good_success += self.update_task_list
        self._init_panel()
        return

    def _init_panel(self):
        self.panel.btn_show.BindMethod('OnClick', self.on_preview_reward)
        self.init_task_list()

    def init_task_list(self):
        task_list = self.panel.list_task
        task_list.SetInitCount(len(self._base_task) + len(self._advanced_task) + len(self._ultimate_task))
        self.update_task_list()

    def on_preview_reward(self, btn, touch):
        self.parent.switch_widget(False)

    @post_ui_method
    def update_task_list(self, *args):
        task_list = []
        can_receive_tasks = []
        for task_id in self._base_task:
            task_list.append(task_id)

        for task_id in self._advanced_task:
            task_list.append(task_id)

        for task_id in self._ultimate_task:
            task_list.append(task_id)

        sorted_list = sorted(task_list, key=cmp_to_key(self.cmp_task))
        for idx in range(len(sorted_list)):
            task_id = sorted_list[idx]
            reward_id = task_utils.get_task_reward(task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            item = self.panel.list_task.GetItem(idx)
            item.lab_task_name.SetString(task_utils.get_task_name(task_id))
            prog = global_data.player.get_task_prog(task_id)
            total_prog = task_utils.get_total_prog(task_id)
            item.lab_task_progress.SetString('{}/{}'.format(prog, total_prog))
            item.progress_task.SetPercentage(100.0 * prog / total_prog)
            item.list_award.SetInitCount(len(reward_list))
            is_unlocked = global_data.player and global_data.player.is_retrospect_task_unlocked(task_id)
            can_unlock = self.can_task_unlock(task_id, task_list)
            task_status = global_data.player.get_task_reward_status(task_id)
            task_type = self.get_task_type(task_id)
            is_prize = False
            if task_type == ADVANCED_TASK:
                item.lab_tag.setVisible(True)
                if self._advanced_task.index(task_id) + 1 == len(self._advanced_task) - len(self._extra_task):
                    is_prize = True if 1 else False
                    lv = self._advanced_task.index(task_id) + 1
                    item.lab_tag.SetString(get_text_by_id(634493).format(lv))
                    item.bar_tag.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_pass/retrospect/task/img_retrospect_task_tag_blue.png')
                    if task_id in self._extra_task:
                        lv = self._extra_task.index(task_id) + 1
                        item.lab_tag.SetString(get_text_by_id(634567).format(lv))
                elif task_type == ULTIMATE_TASK:
                    item.lab_tag.setVisible(True)
                    is_prize = True if self._ultimate_task.index(task_id) + 1 == len(self._ultimate_task) else False
                    lv = self._ultimate_task.index(task_id) + 1
                    item.lab_tag.SetString(get_text_by_id(634494).format(lv))
                    item.bar_tag.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_pass/retrospect/task/img_retrospect_task_tag_purple.png')
                else:
                    item.bar_tag.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_pass/retrospect/task/img_retrospect_task_tag_blue.png')
                    item.lab_tag.setVisible(False)
                item.lab_task_name.setVisible(True)
                item.lab_task_name.SetColor('#SK')
                item.lab_task_progress.setVisible(True)
                if not is_unlocked and not global_data.player.is_retrospect_task_finished(task_id):
                    item.lab_task_progress.setVisible(False)
                    item.lab_task_name.SetColor('#SH')
                    can_unlock or item.nd_get.setVisible(False)
                    item.lab_working.setVisible(False)
                    item.temp_btn_go.setVisible(False)
                    item.temp_btn_get.setVisible(False)
                    item.temp_btn_lock.setVisible(False)
                    item.lab_tips.SetString(get_text_by_id(634481))
                    item.lab_tips.setVisible(True)
                    item.lab_task_name.setVisible(False)
                else:
                    item.nd_get.setVisible(False)
                    item.lab_working.setVisible(False)
                    item.temp_btn_go.setVisible(False)
                    item.temp_btn_get.setVisible(False)
                    item.temp_btn_lock.setVisible(True)
                    item.lab_tips.setVisible(False)
                    item.temp_btn_lock.btn_common.SetEnable(True)
                    task_conf = task_utils.get_task_conf_by_id(task_id)
                    unlock_item = task_conf.get('retrospect_arg', {}).get('unlock_item', {})
                    unlock_num = 0
                    unlock_coin = None
                    for k, v in six.iteritems(unlock_item):
                        money_type = mall_utils.get_item_money_type(int(k))
                        coin_num = mall_utils.get_my_money(money_type)
                        img_path = item_utils.get_money_icon(money_type)
                        item.temp_btn_lock.icon.SetDisplayFrameByPath('', img_path)
                        unlock_num = v
                        unlock_coin = k
                        if unlock_num > coin_num:
                            num_text = '<color=0xe0382fff>{}</color>' if 1 else '{}'
                            item.temp_btn_lock.lab_num.SetString(num_text.format(str(v)))

                    @item.temp_btn_lock.btn_common.unique_callback()
                    def OnClick(btn, touch, task_id=task_id, season=self.season, task_type=task_type):
                        coin_num = mall_utils.get_my_money(money_type)
                        if coin_num >= unlock_num:

                            def confirm_callback():
                                global_data.player.unlock_retrospect_task(task_id, season)

                            NormalConfirmUI2(on_confirm=confirm_callback, content=get_text_by_id(634501).format('"' + item_utils.get_lobby_item_pic_by_item_no(unlock_coin) + '"', unlock_num), cancel_text=get_text_by_id(90005))
                        else:
                            from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
                            import logic.gcommon.const as gconst
                            from logic.client.const import mall_const
                            if task_id in self._extra_task:
                                ExchangeUI(from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=gconst.DEC_COIN_TICKET, buy_goods_id=mall_const.DEC_COIN_GIFT, keyboard_for_from_payment=False)
                            else:
                                g_id = self._goods_id if task_type == ADVANCED_TASK else self._u_goods_id
                                GroceriesBuyConfirmUI(goods_id=g_id, init_quantity=unlock_num - coin_num)

            elif task_status == ITEM_RECEIVED or global_data.player.is_retrospect_task_finished(task_id):
                item.nd_get.setVisible(True)
                item.lab_working.setVisible(False)
                item.temp_btn_go.setVisible(False)
                item.temp_btn_get.setVisible(False)
                item.temp_btn_lock.setVisible(False)
                item.lab_tips.setVisible(False)
            elif task_status == ITEM_UNGAIN:
                item.nd_get.setVisible(False)
                item.lab_working.setVisible(True)
                item.temp_btn_go.setVisible(False)
                item.temp_btn_get.setVisible(False)
                item.temp_btn_lock.setVisible(False)
                item.lab_tips.setVisible(False)
            else:
                item.nd_get.setVisible(False)
                item.lab_working.setVisible(False)
                item.temp_btn_go.setVisible(False)
                item.temp_btn_get.setVisible(True)
                item.temp_btn_lock.setVisible(False)
                item.lab_tips.setVisible(False)
                can_receive_tasks.append(str(task_id))

                @item.temp_btn_get.btn_common.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    global_data.player.receive_task_reward(task_id)

            for item_idx, reward_item in enumerate(item.list_award.GetAllItem()):
                self.create_item(item_idx, reward_item, reward_list, is_prize)

            if len(reward_list) <= 0:
                return
            item_no, item_num = reward_list[0]

            @item.btn_choose.unique_callback()
            def OnClick(btn, touch, sel_item=item, data=item_no, *args):
                self._displaying_item_no = data
                self._display_widget.display_award(data, self.reset_display_type)
                if self._select_item and self._select_item.isValid():
                    self._select_item.btn_choose.SetSelect(False)
                self._select_item = sel_item
                self._select_item.btn_choose.SetSelect(True)

            if self._displaying_item_no == item_no:
                if self._select_item and self._select_item.isValid():
                    self._select_item.btn_choose.SetSelect(False)
                self._select_item = item
                item.btn_choose.SetSelect(True)
            elif self.panel.isVisible() and self._displaying_item_no == None:
                item.btn_choose.OnClick(None)

        task_num = len(can_receive_tasks)
        if task_num > 1:
            self.panel.temp_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(task_num))

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_tasks_reward(can_receive_tasks)

        else:
            self.panel.temp_get_all.setVisible(False)
        return

    def can_task_unlock(self, task_id, task_list):
        if task_id not in task_list or not global_data.player:
            return False
        idx = task_list.index(task_id)
        for i in range(idx):
            if not global_data.player.is_retrospect_task_unlocked(task_list[i]) and not global_data.player.is_retrospect_task_finished(task_list[i]):
                return False

        return True

    def cmp_task(self, task_id1, task_id2):
        has_receive1 = global_data.player.is_retrospect_task_finished(task_id1)
        has_receive2 = global_data.player.is_retrospect_task_finished(task_id2)
        if has_receive1 != has_receive2:
            if has_receive1:
                return 1
            if has_receive2:
                return -1
        total_times_1 = task_utils.get_total_prog(task_id1)
        cur_times_1 = global_data.player.get_task_prog(task_id1)
        total_times_2 = task_utils.get_total_prog(task_id2)
        cur_times_2 = global_data.player.get_task_prog(task_id2)
        not_finished_a = cur_times_1 < total_times_1
        not_finished_b = cur_times_2 < total_times_2
        if not_finished_a != not_finished_b:
            if not_finished_a:
                return 1
            if not_finished_b:
                return -1
        task_type_1 = self.get_task_type(task_id1)
        task_type_2 = self.get_task_type(task_id2)
        if task_type_1 > task_type_2:
            return 1
        if task_type_1 < task_type_2:
            return -1
        if task_id1 > task_id2:
            return 1
        if task_id2 > task_id1:
            return -1
        return 0

    def get_task_type(self, task_id):
        if task_id in self._base_task:
            return BASE_TASK
        else:
            if task_id in self._advanced_task:
                return ADVANCED_TASK
            if task_id in self._ultimate_task:
                return ULTIMATE_TASK
            return 0

    def create_item(self, idx, ui_item, reward_list, is_prize=False):
        item_no, item_num = reward_list[idx]
        item_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        ui_item.item.SetDisplayFrameByPath('', item_path)
        if item_num > 1:
            ui_item.lab_quantity.setVisible(True)
            ui_item.lab_quantity.SetString(str(item_num))
        else:
            ui_item.lab_quantity.setVisible(False)
        ui_item.img_tag_prize.setVisible(is_prize)
        ui_item.img_frame.SetDisplayFrameByPath('', item_utils.get_lobby_item_rare_degree_pic_by_item_no(item_no, item_num))

    def _display_cb(self, is_model, item_no):
        super(RetrospectTaskWidget, self)._display_cb(is_model, item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        item_desc = item_utils.get_lobby_item_desc(item_no)
        if is_model:
            self.parent.panel.nd_special_reward.img_bar.lab_name.SetString(item_name)
            self.parent.panel.nd_special_reward.img_bar.lab_describe.SetString(item_desc)
            self.parent.panel.nd_special_reward.img_bar.lab_name.setVisible(True)
            self.reset_display_type = False
        else:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            self.parent.panel.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', pic_path)
            self.parent.panel.nd_common_reward.lab_name.SetString(item_name)
            self.parent.panel.nd_common_reward.lab_describe.SetString(item_desc)
        self.parent.panel.nd_special_reward.setVisible(is_model)
        self.parent.panel.nd_common_reward.setVisible(not is_model)

    def show(self):
        super(RetrospectTaskWidget, self).show()
        self.reset_display_type = True
        for task_item in self.panel.list_task.GetAllItem():
            if task_item:
                task_item.btn_choose.OnClick(None)
                return

        self.parent.panel.nd_special_reward.setVisible(False)
        self.parent.panel.nd_common_reward.setVisible(False)
        return

    def hide(self):
        super(RetrospectTaskWidget, self).hide()

    def destroy(self):
        self.destroy_widget('_display_widget')
        super(RetrospectTaskWidget, self).destroy()