# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryExclusiveGiftUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from logic.gutils import mall_utils
from common.cfg import confmgr
from logic.gutils import jump_to_ui_utils
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils import task_utils

class LotteryExclusiveGiftUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202209/head_gift/open_activity_head_gift'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    DELAY_CLOSE_TAG = 31417926
    FLY_OUT_ANIM_TAG = 31418927
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': '_on_click_close_btn'
       }

    def on_custom_template_create(self, *arg, **kwargs):
        super(LotteryExclusiveGiftUI, self).on_custom_template_create()
        default_template = 'activity/activity_202209/head_gift/open_activity_head_gift'
        if kwargs.get('gift_template', ''):
            self.PANEL_CONFIG_NAME = kwargs.get('gift_template', default_template)
        else:
            self.PANEL_CONFIG_NAME = default_template

    def on_init_panel(self, gift_dict=None, *args, **kwargs):
        self.bind_event(True)
        self.hide_main_ui()
        if not gift_dict:
            log_error('LotteryExclusiveGiftUI can not init without parameters gift_dict ')
            return
        else:
            self._wait_for_charge_result = None
            self.task_list = gift_dict.get('task_list', [])
            self.goods_id = str(gift_dict.get('goods_id', None))
            self.goods_func_str = gift_dict.get('goods_func_str', None)
            self.goods_tag = gift_dict.get('goods_tag', 0)
            name = gift_dict.get('name', '')
            if name:
                self.panel.lab_name.SetString(name)
            lotteryname = gift_dict.get('lotteryname', '')
            if lotteryname:
                self.panel.lab_title.SetString(lotteryname)
            if self.goods_tag > 0:
                self.panel.lab_price.SetString(str(self.goods_tag) + '%')
            self.task_btns = [self.panel.temp_btn_1, self.panel.temp_btn_2]
            self.is_pc_global_pay = mall_utils.is_pc_global_pay()
            self.refresh_btns()
            if self.panel.btn_share:

                @self.panel.btn_share.callback()
                def OnClick(btn, touch):
                    if len(self.task_list) > 1:
                        task_id = self.task_list[1]
                        jump_conf = task_utils.get_jump_conf(task_id)
                        if jump_conf:
                            task_utils.try_do_jump(task_id)

            return

    def refresh_btns(self):
        for idx, task_id in enumerate(self.task_list):
            item_widget = self.task_btns[idx]
            self.update_task_list_btn(item_widget, self.get_receive_btn_status(task_id))

            @item_widget.btn_common.callback()
            def OnClick(btn, touch, task_id=task_id):
                self.on_click_receive_btn(task_id)

        if self.goods_id:
            self.refresh_goods_reward()

    def update_one_item_widget(self, item_widget, goods_id, func_list):
        reward_id = mall_utils.get_goods_item_reward_id(goods_id)
        if reward_id:
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            if not reward_conf:
                return
        has_bought = mall_utils.limite_pay(goods_id)
        if has_bought:
            item_widget.btn_common_big.SetEnable(False)
            item_widget.btn_common_big.SetText(get_text_by_id(12014))
        else:
            goods_info = global_data.lobby_mall_data.get_activity_sale_info(func_list)
            if not goods_info:
                item_widget.btn_common_big.SetEnable(False)
                item_widget.btn_common_big.SetText('******')
            else:
                item_widget.btn_common_big.SetEnable(True)
                if self.is_pc_global_pay or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(goods_info)
                else:
                    key = goods_info['goodsid']
                    price_txt = mall_utils.get_charge_price_str(key)
                item_widget.btn_common_big.SetText(mall_utils.adjust_price(str(price_txt)))

                @item_widget.btn_common_big.callback()
                def OnClick(btn, touch, _goods_info=goods_info):
                    self._wait_for_charge_result = _goods_info
                    if self.is_pc_global_pay:
                        jump_to_ui_utils.jump_to_web_charge()
                    elif _goods_info:
                        global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

    def refresh_goods_reward(self):
        self._wait_for_charge_result = None
        self.update_one_item_widget(self.panel.temp_btn_3, self.goods_id, self.goods_func_str)
        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def buy_good_fail(self):
        if self._wait_for_charge_result is None:
            return
        else:
            fail_ui = global_data.ui_mgr.show_ui('ChargeGiftBoxFailUI', 'logic.comsys.common_ui')
            fail_ui.show_panel(str(self.goods_id), self.goods_func_str, self.goods_tag, global_data.lobby_mall_data.get_activity_sale_info(self.goods_func_str))
            self._wait_for_charge_result = None
            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def on_click_receive_btn(self, task_id):
        if global_data.player is None:
            return
        else:
            jump_conf = task_utils.get_jump_conf(task_id)
            if not jump_conf:
                if not global_data.player.get_lv() >= 10:
                    global_data.game_mgr.show_tip(get_text_by_id(82172))
                    return
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNGAIN:
                jump_conf = task_utils.get_jump_conf(task_id)
                if jump_conf:
                    task_utils.try_do_jump(task_id)
                return
            global_data.player.receive_task_reward(task_id)
            return

    def get_receive_btn_status(self, task_id):
        from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_GO, BTN_ST_SHARE
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_RECEIVED:
            return BTN_ST_RECEIVED
        if status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_id)
            if jump_conf:
                return BTN_ST_SHARE
            else:
                return BTN_ST_CAN_RECEIVE

        elif status == ITEM_UNRECEIVED:
            return BTN_ST_CAN_RECEIVE

    def bind_event(self, bind):
        e_conf = {'receive_task_reward_succ_event': self._on_update_reward,
           'task_prog_changed': self._on_update_reward,
           'buy_good_success': self.refresh_goods_reward,
           'buy_good_fail': self.buy_good_fail
           }
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def on_finalize_panel(self):
        super(LotteryExclusiveGiftUI, self).on_finalize_panel()
        self.show_main_ui()
        self.bind_event(False)

    def _on_update_reward(self, *args):
        self.refresh_btns()

    def _on_click_close_btn(self, btn, touch):
        self.close()

    def update_task_list_btn(self, nd_btn, status, extra_args=None):
        status_dict = {1: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_minor.png','text_color': 15523828,'btn_text': 604030
               },
           2: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_minor.png','text_color': 15523828,'btn_text': 80149
               },
           3: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_minor.png','text_color': 15523828,'btn_text': 607056
               },
           4: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','text_color': 13623804,'btn_text': 604031,
               'enable': False},
           5: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','show_nd_get': True,'btn_text': 604029,'enable': False
               },
           6: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','show_nd_exchange': True,'enable': False
               },
           7: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','show_nd_unlock': True,'enable': False
               },
           8: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_middle.png','text_color': 2369169,'btn_text': 19850
               },
           9: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','text_color': 13623804,'btn_text': 607056,
               'enable': False},
           10: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','text_color': 13623804,'btn_text': 610813,
                'enable': False}
           }
        if status not in status_dict:
            return
        else:
            if not extra_args:
                extra_args = {}
            text_color = status_dict[status].get('text_color')
            extra_btn_text = extra_args.get('btn_text', '')
            btn_text = extra_btn_text if extra_btn_text else status_dict[status].get('btn_text', '')
            nd_btn.btn_common.SetText(btn_text)
            text_color and nd_btn.btn_common.SetTextColor(text_color, text_color, text_color)
            btn_frame = status_dict[status]['btn_frame']
            nd_btn.btn_common.SetFrames('', [btn_frame, btn_frame, btn_frame], False, None)
            return