# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/GiftBoxItemUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil
from logic.gutils import trigger_gift_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
import logic.gcommon.const as gconst
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang
from logic.gutils.fly_out_animation import FlyOutMotion
import cc
from logic.gutils.reward_item_ui_utils import play_item_appear_to_idle_animation

class GiftBoxItemUI(BasePanel):
    PANEL_CONFIG_NAME = 'charge/charge_gift_box'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    DELAY_CLOSE_TAG = 31415926
    FLY_OUT_ANIM_TAG = 31415927
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': '_on_click_close_btn',
       'btn_buy.OnClick': '_on_click_buy'
       }

    def on_init_panel(self, gift_info, **kwargs):
        self.init_parameters(gift_info)
        self.init_widget()
        self.bind_event(True)

    def init_parameters(self, gift_info):
        self._gift_info = gift_info
        self._goods_list = self._gift_info.get('goods_list', [])
        self._left_time_widget = None
        self._closing = False
        self._fly_node = self.panel.nd_content_big
        self._fly_src_wpos = self._fly_node.getParent().convertToWorldSpace(cc.Vec2(*self._fly_node.GetPosition()))
        self._fly_ref_node_wpos = self._fly_src_wpos
        self._item_animation_index = -1
        return

    def bind_event(self, bind):
        e_conf = {'buy_good_success_with_list': self._on_buy_good_success_with_list
           }
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def on_finalize_panel(self):
        super(GiftBoxItemUI, self).on_finalize_panel()
        self.bind_event(False)
        self._gift_info = None
        if self._left_time_widget:
            self._left_time_widget.destroy()
            self._left_time_widget = None
        return

    def init_widget(self):
        self._init_left_time_widget()
        self._init_ui_text()
        self._init_gift_goods_items()
        for animation_name in trigger_gift_utils.get_gift_ui_animation_names(False, True):
            self.panel.PlayAnimation(animation_name)

        self._play_item_color_animation()

    def _init_left_time_widget(self):
        expire_time = self._gift_info.get('expire_time', 0)
        if expire_time > tutil.get_server_time():
            self._left_time_widget = LeftTimeCountDownWidget(self.panel, self.panel.lab_time, lambda timestamp: tutil.get_delta_time_str(timestamp))
            self._left_time_widget.begin_count_down_time(expire_time, self._time_up_callback, use_big_interval=False)

    def _init_ui_text(self):
        discount_text = trigger_gift_utils.get_gift_discount_text(self._gift_info.get('discount', 0), get_cur_text_lang())
        if discount_text:
            self.panel.lab_discount.SetString(discount_text)
            self.panel.lab_discount.setVisible(True)
        else:
            self.panel.lab_discount.setVisible(False)
        intro_params = [ param for param in self._gift_info.get('intro_params', []) ]
        intro_text = trigger_gift_utils.get_gift_intro_text(intro_params)
        if intro_text:
            self.panel.lab_tips.SetString(intro_text)
            self.panel.lab_tips.setVisible(True)
        else:
            self.panel.lab_tips.setVisible(False)

    def _init_gift_goods_items(self):
        goods_list = self._gift_info.get('goods_list')
        if not goods_list:
            return
        if len(goods_list) <= 3:
            self.panel.list_item_1.setVisible(True)
            self.panel.list_item_2.setVisible(False)
            list_item = self.panel.list_item_1
        else:
            self.panel.list_item_1.setVisible(False)
            self.panel.list_item_2.setVisible(True)
            list_item = self.panel.list_item_2
        list_item.DeleteAllSubItem()
        list_item.SetInitCount(len(goods_list))
        for i, goods_id in enumerate(goods_list):
            ui_item = list_item.GetItem(i)
            item_no = mall_utils.get_goods_item_no(goods_id)
            item_num = mall_utils.get_goods_num(goods_id)
            template_utils.init_tempate_mall_i_item(ui_item.temp_reward, item_no, item_num=item_num, show_tips=True)

        price_info = {'original_price': self._gift_info.get('original_price', 0),'discount_price': self._gift_info.get('discount_price', 0),
           'goods_payment': gconst.SHOP_PAYMENT_YUANBAO
           }
        COLOR = [
         '#SW', '#SR', '#BC']
        template_utils.init_price_template(price_info, self.panel.temp_price, color=COLOR)

    def get_ui_item_list(self):
        if len(self._goods_list) <= 3:
            return self.panel.list_item_1
        else:
            return self.panel.list_item_2

    def _time_up_callback(self):
        if global_data.player:
            global_data.player.on_trigger_gift_expire(self._gift_info.get('id'))
        self.close()

    def _on_click_buy(self, btn, touch):
        if global_data.player:
            global_data.player.buy_trigger_gift(self._gift_info.get('id'))

    def _on_confirm_close(self):
        if self._closing:
            return
        if self._gift_info.get('expire_time', 0) > tutil.get_server_time():
            global_data.emgr.lobby_add_giftbox_entry.emit(self._gift_info)
        else:
            self._time_up_callback()
        self._try_close()

    def _on_click_close_btn(self, *args):
        left_time_stamp = self._gift_info.get('expire_time') - tutil.get_server_time()
        left_time_str = tutil.get_readable_time(left_time_stamp)
        SecondConfirmDlg2().confirm(content=get_text_by_id(608308).format(left_time_str), confirm_callback=self._on_confirm_close)

    def _on_buy_good_success_with_list(self, goods_list):
        if not global_data.player or not goods_list:
            return
        self.close()

    def _try_close(self):
        if self._closing:
            return
        self._closing = True
        for animation_name in trigger_gift_utils.get_gift_ui_animation_names(False, True):
            self.panel.StopAnimation(animation_name)

        dst_wpos, motion = self._get_fly_animation_params()
        if dst_wpos and motion:
            close_animation_name = trigger_gift_utils.get_gift_ui_animation_names(False, False)
            self.panel.PlayAnimation(close_animation_name)
            delay_close_time = self.panel.GetAnimationMaxRunTime(close_animation_name)
            self._play_fly_animation(self._fly_src_wpos, dst_wpos, motion)

            def cb():
                self.close()

            self.DelayCallWithTag(delay_close_time, cb, self.DELAY_CLOSE_TAG)
        else:
            self.close()

    def on_click_close_btn(self):
        self._try_close()

    def _play_fly_animation(self, src_wpos, dst_wpos, motion):
        import time
        start_t = time.time()

        def update_motion(_, prev_t=[
 start_t]):
            cur_time = time.time()
            delta = cur_time - prev_t[0]
            motion.update(delta)
            node = self._fly_node
            wpos = motion.get_pos()
            lpos = node.getParent().convertToNodeSpace(wpos)
            node.setPosition(lpos)
            prev_t[0] = cur_time

        self.panel.StopTimerActionByTag(self.FLY_OUT_ANIM_TAG)
        duration = motion.get_max_time()
        self.panel.TimerActionByTag(self.FLY_OUT_ANIM_TAG, update_motion, duration)

    def _get_fly_animation_params(self):
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        if ui is not None:
            ref_dst_wpos = cc.Vec2(ui.get_trigger_gift_cocos_wpos())
            diff_vec = cc.Vec2(ref_dst_wpos)
            diff_vec.subtract(self._fly_ref_node_wpos)
            dst_wpos = cc.Vec2(self._fly_src_wpos)
            dst_wpos.add(diff_vec)
            motion = FlyOutMotion(self._fly_src_wpos, dst_wpos)
            return (
             dst_wpos, motion)
        else:
            return (None, None)
            return

    def _play_item_color_animation(self):

        def show_animation():
            self._item_animation_index = (self._item_animation_index + 1) % len(self._goods_list)
            goods_id = self._goods_list[self._item_animation_index]
            ui_item_list = self.get_ui_item_list()
            ui_item = ui_item_list.GetItem(self._item_animation_index)
            item_no = mall_utils.get_goods_item_no(goods_id)
            item_num = mall_utils.get_goods_num(goods_id)
            play_item_appear_to_idle_animation(ui_item, item_no, item_num, show_animation, callback_advance_rate=0.8)

        show_animation()