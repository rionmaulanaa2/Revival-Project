# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/GiftBoxBattlePassUI.py
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
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang, LANG_CN, LANG_ZHTW
from logic.gutils.fly_out_animation import FlyOutMotion
import cc
from logic.gutils.reward_item_ui_utils import refresh_item_info, play_item_appear_to_idle_animation
from logic.client.const import mall_const
from common.cfg import confmgr
from logic.gutils import jump_to_ui_utils
import math

class GiftBoxBattlePassUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/battle_pass_recommend'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    DELAY_CLOSE_TAG = 31417926
    FLY_OUT_ANIM_TAG = 31418927
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_click_close_btn',
       'btn_go.OnClick': '_on_click_go'
       }

    def on_init_panel(self, gift_info, from_battle_pass, *args, **kwargs):
        self.init_parameters(gift_info, from_battle_pass)
        self.init_widget()
        self.bind_event(True)
        self.panel.lab_info.SetString(610035)
        self.panel.PlayAnimation('show')

    def init_parameters(self, gift_info, from_battle_pass):
        self._gift_info = gift_info
        self._from_battle_pass = from_battle_pass
        self._cash_only = False
        self._gift_level = self._gift_info.get('gift_level', 0)
        self._card_template = [self.panel.temp_card_left, self.panel.temp_card_mid, self.panel.temp_card_right]
        self._left_time_widget = None
        self._closing = False
        self._fly_node = self.panel.nd_content_big
        self._fly_src_wpos = self._fly_node.getParent().convertToWorldSpace(cc.Vec2(*self._fly_node.GetPosition()))
        self._fly_ref_node_wpos = self._fly_src_wpos
        return

    def bind_event(self, bind):
        e_conf = {}
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def on_finalize_panel(self):
        super(GiftBoxBattlePassUI, self).on_finalize_panel()
        self.bind_event(False)
        self._gift_info = None
        if self._left_time_widget:
            self._left_time_widget.destroy()
            self._left_time_widget = None
        return

    def init_widget(self):
        self._init_left_time_widget()
        if self._gift_info.get('opened', 0) > 0:
            self._on_choose_card(1)
            self.panel.lab_info.setVisible(False)
        else:
            for index, template in enumerate(self._card_template):

                @template.img_unlock_card.btn_click.unique_callback()
                def OnClick(btn, touch, card_index=index):
                    self._on_choose_card(card_index)
                    if global_data.player:
                        global_data.player.open_chance_gift(self._gift_info.get('id'))

        if self._from_battle_pass:
            self.panel.btn_close.setVisible(False)
            self.panel.btn_go.setVisible(False)
            self.panel.nd_normal.setVisible(False)
            self.panel.nd_quit.setVisible(True)
            self.panel.PlayAnimation('btn_quite')
            discount = self._gift_info.get('discount', 0)
            reduce_value = 1488 - int(math.floor(1488 * discount))
            if reduce_value > 0:
                self.panel.lab_cancle_tips.SetString(get_text_by_id(610038).format(str(reduce_value)))

            @self.panel.btn_quit.unique_callback()
            def OnClick(btn, touch):
                global_data.ui_mgr.close_ui('BuySeasonCardUI')
                self._quit_close()

            @self.panel.btn_cancel.unique_callback()
            def OnClick(btn, touch):
                self._quit_close()

        for animation_name in trigger_gift_utils.get_gift_ui_animation_names(False, True):
            self.panel.PlayAnimation(animation_name)

    def _init_left_time_widget(self):
        expire_time = self._gift_info.get('expire_time', 0)
        if expire_time > tutil.get_server_time():
            self._left_time_widget = LeftTimeCountDownWidget(self.panel, self.panel.lab_time, lambda timestamp: get_text_by_id(610034).format(tutil.get_readable_time_2(timestamp)))
            self._left_time_widget.begin_count_down_time(expire_time, self._time_up_callback, use_big_interval=True)

    def _on_choose_card(self, card_index):
        self.panel.lab_info.setVisible(False)
        for index, template in enumerate(self._card_template):
            if index != card_index:
                template.img_mask.setVisible(True)
                template.setLocalZOrder(0)
            else:
                template.setLocalZOrder(1)
            template.img_unlock_card.btn_click.SetEnable(False)

        self.panel.nd_normal.setVisible(True)
        animations = ['open_left', 'open_mid', 'open_right']
        card_animation = 'open_extra' if self._gift_level > 0 else 'open'
        ac_list = []
        if self._gift_info.get('opened', 0) <= 0:
            ac_list.extend([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('btn_normal')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation(animations[card_index])),
             cc.DelayTime.create(0.2),
             cc.CallFunc.create(lambda : self._card_template[card_index].PlayAnimation(card_animation))])
        else:
            if self._from_battle_pass:
                self.panel.temp_card_left.setVisible(False)
                self.panel.temp_card_right.setVisible(False)
            ac_list.extend([
             cc.DelayTime.create(0.6),
             cc.CallFunc.create(lambda : self._card_template[card_index].PlayAnimation(card_animation))])
        virtual_discount = self._get_valid_virtual_discount()
        if virtual_discount and not self._from_battle_pass:
            ac_list.append(cc.DelayTime.create(self._card_template[card_index].GetAnimationMaxRunTime(card_animation) * 0.75))
            for index, template in enumerate(self._card_template):
                if index == card_index:
                    continue
                ac_list.append(cc.CallFunc.create(lambda i=index: self._card_template[i].PlayAnimation('open_flip')))

        self.panel.runAction(cc.Sequence.create(ac_list))
        show_discount = self._gift_info.get('show_discount', None)
        if show_discount is not None:
            discount_text = trigger_gift_utils.get_gift_discount_text(show_discount, get_cur_text_lang())
        else:
            discount_text = trigger_gift_utils.get_gift_discount_text(self._gift_info.get('discount', 0), get_cur_text_lang())
        self._card_template[card_index].lab_num_discount.SetString(str(discount_text))
        discount_unit = '\xe6\x8a\x98' if get_cur_text_lang() in {LANG_CN, LANG_ZHTW} else 'off'
        self._card_template[card_index].nd_open_card_discount.lab_word.SetString(discount_unit)
        if self._gift_level > 0:
            self._card_template[card_index].nd_open_card_level.lab_word.SetString(get_text_by_id(610049))
        if self._gift_level > 0:
            self._card_template[card_index].lab_num.SetString(str(self._gift_level))
        if virtual_discount and not self._from_battle_pass:
            dis_index = 0
            for index, template in enumerate(self._card_template):
                if index == card_index:
                    continue
                self._card_template[index].nd_open_card_discount.lab_word.SetString(discount_unit)
                discount_text = trigger_gift_utils.get_gift_discount_text(virtual_discount[dis_index], get_cur_text_lang())
                self._card_template[index].lab_num_discount.SetString(str(discount_text))
                dis_index += 1

        return

    def _get_valid_virtual_discount(self):
        virtual_discount = self._gift_info.get('virtual_discount', [])
        if virtual_discount and len(virtual_discount) >= len(self._card_template) - 1:
            return virtual_discount
        return []

    def _time_up_callback(self):
        if global_data.player:
            global_data.player.on_trigger_gift_expire(self._gift_info.get('id'))
        self.close()

    def _on_click_go(self, btn, touch):
        self._quit_close()
        from logic.gutils.jump_to_ui_utils import jump_to_buy_season_pass_card
        jump_to_buy_season_pass_card(from_battle_pass_gift=True)

    def _quit_close(self):
        if self._gift_info and self._gift_info.get('expire_time', 0) > tutil.get_server_time():
            global_data.emgr.lobby_add_giftbox_entry.emit(self._gift_info)
        self.close()

    def _on_confirm_close(self):
        if not self._gift_info:
            self.close()
            return
        if self._gift_info.get('expire_time', 0) > tutil.get_server_time():
            global_data.emgr.lobby_add_giftbox_entry.emit(self._gift_info)
        else:
            self._time_up_callback()
        self._try_close()

    def _on_click_close_btn(self, *args):
        if not self._cash_only:
            left_time_stamp = self._gift_info.get('expire_time') - tutil.get_server_time()
            left_time_str = tutil.get_readable_time(left_time_stamp)
            SecondConfirmDlg2().confirm(content=get_text_by_id(608308).format(left_time_str), confirm_callback=self._on_confirm_close)
        else:
            self._on_confirm_close()

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
            ref_dst_wpos = cc.Vec2(ui.get_trigger_gift_cocos_wpos(template_name='temp_btn_gifts_02'))
            if not ref_dst_wpos:
                return (None, None)
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