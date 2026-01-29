# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryMainUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils.mall_utils import get_lottery_widgets_info, get_lottery_table_id_list, get_detail_pic_by_item_no
from .LotteryNew.LotteryArtCollectionWidgetNew import LotteryArtCollectionWidgetNew
from .LotteryCommonTurntableWidget import LotteryCommonTurntableWidget
from .LotteryHistoryWidget import LotteryHistoryWidget
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from .LotteryPageTabWidget import LotteryPageTapWidget
from .LotteryRewardLabelWidget import LotteryRewardLabelWidget
from .LotteryPreviewWidget import LotteryPreviewWidget
from logic.comsys.common_ui.MechaTransformUIWidget import MechaTransformUIWidget
from .LotteryMechaPreviewAdvancedAppearanceWidget import LotteryMechaPreviewAdvancedAppearanceWidget
from logic.gcommon.const import SHOP_PAYMENT_GOLD, SHOP_PAYMENT_DIAMON, SHOP_PAYMENT_YUANBAO, SPECIAL_TICKET_TYPE, NORMAL_TICKET_TYPE, PIECE_TYPE, FLASH_CARD_TYPE, DIANCANG_TICKET_TYPE, ACTIVITY_CARD_TICKET, LOTTERY_POINTS, LOTTERY_EXCHANGE, FLASH_POINT, FLASH_EXCHANGE
from logic.client.const.mall_const import FLASH_EXCHANGE
from logic.gcommon.item.lobby_item_type import MODEL_DISPLAY_TYPE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_EXPERIENCE_CARD, L_ITEM_MECHA_SFX, L_ITEM_YTPE_VEHICLE, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_FACE_DEC, L_ITEM_TYPE_WAIST_DEC, L_ITEM_TYPE_LEG_DEC, L_ITEM_TYPE_ARM_DEC, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, ITEM_TYPE_DEC, L_ITEM_TYPE_HAIR_DEC, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_PET_SKIN
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_GESTURE, L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_use_parms, get_lobby_item_belong_no
from logic.client.const.lobby_model_display_const import LUCKY_HOUSE, LUCKY_HOUSE_SMALL, LUCKY_HOUSE_GUN, FLASH_LUCKY_HOUSE, DEFAULT_LEFT
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
from logic.gutils.lobby_model_display_utils import get_lobby_model_data, get_mecha_sfx_model_data, get_pendant_show_data, is_chuchang_scene
from logic.gutils.dress_utils import get_mecha_model_h_path, get_mecha_model_path, get_skin_default_show_decoration_dict
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gutils.jump_to_ui_utils import jump_to_mall
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_const import scene_const
from logic.gutils import items_book_utils
from common.platform.dctool.interface import is_mainland_package
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import SHOP_PAYMENT_ITEM
from common.cfg import confmgr
from logic.gutils import mecha_skin_utils
import cc
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_MODE_NEAR_HEAD, CAM_MODE_NEAR_LEG, CAM_DISPLAY_PIC
import sys
import copy
from ext_package.ext_decorator import has_skin_ext
from logic.gutils.video_utils import check_play_chuchang_video_with_tag
from .LotteryNew.LotteryVideoController import LotteryVideoController
LOTTERY_SCENE_INFO = {'normal': (
            scene_const.SCENE_LUCKY_HOUSE, LUCKY_HOUSE, None),
   'special': (
             scene_const.SCENE_LUCKY_HOUSE_FLASH, FLASH_LUCKY_HOUSE, None),
   'common': (
            scene_const.SCENE_JIEMIAN_COMMON, LUCKY_HOUSE, scene_const.SCENE_LUCKY_HOUSE_COMMON),
   'art': (
         scene_const.SCENE_JIEMIAN_COMMON, LUCKY_HOUSE, scene_const.SCENE_LUCKY_HOUSE_ART_COLLECTION)
   }
MODEL_OFFSET = [
 -3, 0, 0]

def _preload():
    for lid, info in six.iteritems(confmgr.get('lottery_page_config')):
        class_name = info.get('class_name')
        if class_name is None:
            continue
        mpath = 'logic.comsys.lottery.%s' % class_name
        mod = sys.modules.get(mpath)
        if not mod:
            __import__(mpath, globals(), locals())

    return


_preload()

def get_lottery_cls(lottery_id, cls_name):
    if cls_name is None:
        if lottery_id in confmgr.get('turntable_lottery_custom_conf'):
            return LotteryCommonTurntableWidget
        return LotteryArtCollectionWidgetNew
    else:
        mpath = 'logic.comsys.lottery.%s' % cls_name
        mod = sys.modules.get(mpath)
        cls = None
        if mod:
            cls = getattr(mod, cls_name, None)
        if cls is None:
            log_error('Unexisted lottery class %s' % cls_name)
        return cls


MONEY_STR_PAYMENT_MAP = {'gold': SHOP_PAYMENT_GOLD,
   'diamond': SHOP_PAYMENT_DIAMON,
   'yuanbao': SHOP_PAYMENT_YUANBAO,
   'normal_ticket': NORMAL_TICKET_TYPE,
   'special_ticket': SPECIAL_TICKET_TYPE,
   'piece': PIECE_TYPE,
   'flash_card': FLASH_CARD_TYPE,
   'collection_ticket': DIANCANG_TICKET_TYPE,
   'activity_ticket': ACTIVITY_CARD_TICKET,
   'lottery_points': LOTTERY_POINTS,
   'lottery_exchange': LOTTERY_EXCHANGE,
   'flash_point': FLASH_POINT,
   'flash_exchange': FLASH_EXCHANGE
   }

def get_money_payment--- This code section failed: ---

 106       0  LOAD_GLOBAL           0  'MONEY_STR_PAYMENT_MAP'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  LOAD_ATTR             2  'format'
          12  LOAD_GLOBAL           3  'SHOP_PAYMENT_ITEM'
          15  LOAD_FAST             0  'money_type'
          18  CALL_FUNCTION_2       2 
          21  CALL_FUNCTION_2       2 
          24  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21


HIDE_JUMP_PAYMENT_SET = {
 LOTTERY_POINTS, FLASH_POINT}
ROTATE_FACTOR = 850
ROLE_SCALE_CAM_KEY = {L_ITEM_TYPE_ROLE_SKIN: 'far_cam',
   L_ITEM_TYPE_HEAD: 'head_cam',
   L_ITEM_TYPE_BODY: 'near_cam',
   L_ITEM_TYPE_SUIT: 'far_cam',
   L_ITEM_TYPE_FACE_DEC: 'head_cam',
   L_ITEM_TYPE_WAIST_DEC: 'near_cam',
   L_ITEM_TYPE_LEG_DEC: 'leg_cam',
   L_ITEM_TYPE_ARM_DEC: 'near_cam',
   L_ITEM_TYPE_HAIR_DEC: 'head_cam'
   }

class LotteryMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/lottery_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_model_touch.OnBegin': 'on_begin_drag_model',
       'nd_model_touch.OnDrag': 'on_drag_model',
       'nd_model_touch.OnEnd': 'on_end_drag_model',
       'btn_glass.OnClick': 'on_click_btn_glass'
       }

    @property
    def cur_lottery_id(self):
        if self.page_tap_widget:
            return self.page_tap_widget.cur_lottery_id
        else:
            return None

    def request_reward_display_data(self):
        if not LotteryPreviewWidget.LOTTERY_INFO or global_data.player and global_data.player.check_is_probability_up_data_expired():
            global_data.player.request_reward_display_data(get_lottery_table_id_list())

    def on_init_panel(self, jump_lottery_id=None, force_show_model_id=None, jump_shop_goods_id=None, video_played_tag=False):
        self._skin_pic_nd = None
        self.jump_lottery_id = jump_lottery_id
        self.force_show_model_id = force_show_model_id
        self.jump_shop_goods_id = jump_shop_goods_id
        self.force_label_skin = None
        self.init_parameters()
        self.video_played_tag = video_played_tag
        self.init_sub_panel()
        self.init_ui_click_event()
        self.init_widgets()
        self.panel.PlayAnimation('loop_tap')
        global_data.last_scene_is_lottery = True
        self.hide_main_ui()
        return

    def init_parameters(self):
        self.cur_model_id = None
        self.cur_show_model_id = None
        self.price_top_widget = None
        self.widgets_map, self.widgets_list = get_lottery_widgets_info()
        for info in six.itervalues(self.widgets_map):
            info['core_reward_count'] = len(info['core_item_id_list'])
            for i in range(len(info['show_money_type'])):
                info['show_money_type'][i] = get_money_payment(info['show_money_type'][i])

        self.cur_lottery_widget = None
        self.archive_data = ArchiveManager().get_archive_data(str(global_data.player.uid) + 'enter_lottery')
        self.cur_specific_item_scene_path = ''
        self.cur_scene_owner_id = None
        self.cur_draw_lottery_id = None
        self.cur_draw_lottery_count = 1
        self.cur_cam_mode = CAM_MODE_FAR
        self.cam_pos = {CAM_MODE_FAR: None,
           CAM_MODE_NEAR: None
           }
        self.force_hide_node = set()
        self.video_played_tag = False
        self.chuchang_video_dict = {}
        self.reward_label_visible = True
        self.is_model_loaded = False
        self._lottery_video_controller = LotteryVideoController(self)
        self.is_normal_model_offset = True
        return

    def init_sub_panel(self):
        ui = global_data.ui_mgr.get_ui('LotteryBroadcastUI')
        ui and ui.show()

    def init_ui_click_event(self):
        self.panel.btn_last_reward.setVisible(False)

        @global_unique_click(self.panel.btn_last_reward)
        def OnClick(*args, **kwargs):
            self.on_click_btn_last_reward(*args, **kwargs)

        self.panel.btn_next_reward.setVisible(False)

        @global_unique_click(self.panel.btn_next_reward)
        def OnClick(*args, **kwargs):
            self.on_click_btn_next_reward(*args, **kwargs)

        @global_unique_click(self.panel.btn_exchange)
        def OnClick(*args, **kwargs):
            self.on_click_btn_exchange(*args, **kwargs)

    def play_show_anim(self):
        self.reward_label_widget.set_visible(self.reward_label_visible)
        self.panel.lab_num_times not in self.force_hide_node and self.panel.lab_num_times.setVisible(True)
        self.panel.list_bar not in self.force_hide_node and self.panel.list_bar.setVisible(True)
        self.panel.PlayAnimation('show_mall')

    def set_btn_change_visible(self, is_visible):
        if not is_visible:
            self.panel.StopAnimation('appear_1')
        self.mecha_transform_ui_widget and self.mecha_transform_ui_widget.set_visible(is_visible)
        self.panel.vx_line_light_03.setVisible(is_visible)
        self.panel.vx_xian_02.setVisible(is_visible)
        self.panel.vx_sanjiaoxian_02.setVisible(is_visible)

    def show_btn_change(self):
        self.panel.PlayAnimation('appear_1')
        self.panel.vx_line_light_03.setVisible(True)
        self.panel.vx_xian_02.setVisible(True)
        self.panel.vx_sanjiaoxian_02.setVisible(True)

    def set_mecha_preview_advanced_apperance_widget_visible(self, is_visible):
        if not is_visible:
            self.panel.StopAnimation('appear_2')
        if not self.mecha_preview_advanced_appearance_widget:
            return
        self.mecha_preview_advanced_appearance_widget.set_visible(is_visible)
        inner_visible = self.mecha_preview_advanced_appearance_widget.inner_visible
        self.panel.vx_line_light_01.setVisible(is_visible and inner_visible)
        self.panel.vx_xian_01.setVisible(is_visible and inner_visible)
        self.panel.vx_sanjiaoxian_01.setVisible(is_visible and inner_visible)

    def init_widgets(self):
        self.price_top_widget = PriceUIWidget(self, call_back=self.close, hide_jump_payments=HIDE_JUMP_PAYMENT_SET)
        self.price_top_widget.set_close_btn_visible(False)
        self.init_page_tab_widget()
        self.init_reward_label_widget()
        self.mecha_transform_ui_widget = MechaTransformUIWidget(self, self.panel, show_anim_cb=self.show_btn_change)
        self.set_btn_change_visible(False)
        self.mecha_preview_advanced_appearance_widget = LotteryMechaPreviewAdvancedAppearanceWidget(self, self.panel.btn_splus_ex, False, show_anim_cb=lambda : self.panel.PlayAnimation('appear_2'))
        self.mecha_preview_advanced_appearance_widget.set_need_check_role_decoration(False)
        self.mecha_preview_advanced_appearance_widget.set_equip_check_callback(self.on_equip_check_callback)
        self.set_mecha_preview_advanced_apperance_widget_visible(False)
        self.history_widget = LotteryHistoryWidget(self, self.panel.temp_history)
        self.panel.nd_btn_reward_change.setVisible(False)
        self.panel.list_bar.setVisible(False)
        self.panel.lab_num_times.setVisible(False)
        self.panel.btn_exchange.setVisible(False)
        self.panel.PlayAnimation('loop')
        if 'is_cover_ui' in self.widgets_map[self.cur_lottery_id]:
            self.play_show_anim()
            self.process_event(True)
            self.page_tap_widget.refresh_tab_page()
            self.request_reward_display_data()
        else:
            action_list = [
             cc.DelayTime.create(0.03),
             cc.CallFunc.create(--- This code section failed: ---

 273       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  POP_JUMP_IF_TRUE     19  'to 19'
           9  LOAD_DEREF            0  'self'
          12  LOAD_ATTR             2  'close'
          15  CALL_FUNCTION_0       0 
          18  RETURN_END_IF_LAMBDA
        19_0  COME_FROM                '6'
          19  LOAD_CONST            0  ''
          22  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `RETURN_END_IF_LAMBDA' instruction at offset 18
),
             cc.CallFunc.create(lambda : self.panel and self.process_event(True)),
             cc.CallFunc.create(lambda : self.panel and self.page_tap_widget.refresh_tab_page()),
             cc.CallFunc.create(lambda : self.panel and self.request_reward_display_data()),
             cc.DelayTime.create(0.06),
             cc.CallFunc.create(lambda : self.panel and self.play_show_anim())]
            self.panel.runAction(cc.Sequence.create(action_list))

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'app_resume_event': self.on_app_resume,
           'refresh_switch_core_model_button_visible': self.refresh_switch_core_model_button_visible,
           'set_price_widget_close_btn_visible': self.set_close_btn_visible,
           'hide_lottery_main_ui_elements': self.hide_lottery_main_ui_elements,
           'set_lottery_reward_info_label_visible': self.set_lottery_reward_info_label_visible,
           'set_cur_lucky_draw_info': self.set_cur_lucky_draw_info,
           'get_cur_lucky_draw_info': self.get_cur_lucky_draw_info,
           'receive_lottery_result': self.on_receive_lottery_result,
           'receive_task_reward_succ_event': self.refresh_red_point,
           'message_update_global_reward_receive': self.refresh_red_point,
           'receive_task_prog_reward_succ_event': self.refresh_red_point,
           'task_prog_changed': self.refresh_red_point,
           'on_lottery_ended_event': self.refresh_red_point,
           'set_mecha_preview_advanced_appearance_visible': self.set_mecha_preview_advanced_appearance_visible,
           'set_mecha_translation_widget_visible': self.set_mecha_translation_widget_visible,
           'update_lottery_main_money_types_event': self.update_lottery_main_prices,
           'lottery_video_list_finished': self.on_lottery_video_list_finished
           }
        if is_mainland_package():
            econf['refresh_lottery_limit_count'] = self.refresh_lottery_limit_count
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)
        self.history_widget and self.history_widget.process_event(flag)

    def on_finalize_panel(self):
        self.history_widget.process_event(False)
        self.process_event(False)
        self.panel.stopAllActions()
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()
        if self._skin_pic_nd:
            self._skin_pic_nd.Destroy()
            self._skin_pic_nd = None
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.set_last_chuchang_id.emit(None)
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        self.show_main_ui()
        for widget_info in six.itervalues(self.widgets_map):
            if widget_info.get('widget', None):
                widget_info.get('widget', None) and widget_info['widget'].on_finalize_panel()
                widget_info['widget'] = None

        ui = global_data.ui_mgr.get_ui('LotteryBroadcastUI')
        ui and ui.hide()
        self.widgets_map = None
        self.widgets_list = None
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        self.destroy_widget('mecha_transform_ui_widget')
        self.destroy_widget('mecha_preview_advanced_appearance_widget')
        self.destroy_widget('page_tap_widget')
        self.destroy_widget('history_widget')
        self.cur_lottery_widget = None
        self.archive_data.save()
        self.archive_data = None
        self.cur_specific_item_scene_path = ''
        self.force_hide_node = set()
        self.video_played_tag = False
        self.chuchang_video_dict = {}
        self._lottery_video_controller and self._lottery_video_controller.destroy()
        return

    def do_hide_panel(self):
        super(LotteryMainUI, self).do_hide_panel()
        if self.cur_lottery_widget.panel:
            if hasattr(self.cur_lottery_widget, 'do_hide_panel') and self.cur_lottery_widget.panel.isVisible():
                self.cur_lottery_widget.do_hide_panel()

    def do_show_panel(self):
        super(LotteryMainUI, self).do_show_panel()
        if not self.is_valid():
            return
        else:
            if not self.check_lottery_id_valid(self.cur_lottery_id):
                self.close()
                return
            lottery_result_ui = global_data.ui_mgr.get_ui('LotteryResultUI')
            if lottery_result_ui:
                return
            ui = global_data.ui_mgr.get_ui('LotteryBroadcastUI')
            ui and not ui.isVisible() and ui.show()
            self.cur_scene_owner_id = None
            self.cur_specific_item_scene_path = ''
            if self.jump_lottery_id and self.jump_lottery_id != self.cur_lottery_id:
                self.page_tap_widget.refresh_with_specific_info(self.jump_lottery_id)
            else:
                self.do_switch_scene()
                if self.cur_lottery_widget.panel:
                    if self.cur_lottery_widget.panel.isVisible():
                        self.cur_lottery_widget.show()
            return

    def update_video_played_tag(self, tag):
        self.video_played_tag = tag

    def check_lottery_id_valid(self, lottery_id):
        return self.page_tap_widget.check_jump_lottery_id_valid(lottery_id, show_tips=False)

    def update_jump_info(self, jump_lottery_id, force_show_model_id):
        self.force_show_model_id = force_show_model_id
        if self.check_lottery_id_valid(jump_lottery_id):
            final_lottery_id = jump_lottery_id
            self.jump_lottery_id = final_lottery_id
        else:
            final_lottery_id = self.cur_lottery_id
            self.jump_lottery_id = None
        widget = self.widgets_map[final_lottery_id].get('widget', None)
        if widget:
            widget.hide_preview_widget()
        return

    def jump_to_exchange_shop(self, jump_lottery_id, goods_id, check=True):
        if not self.check_lottery_id_valid(jump_lottery_id):
            return
        else:
            widget = self.widgets_map.get(jump_lottery_id, {}).get('widget', None)
            if not widget:
                return
            widget.jump_to_exchange_shop_widget(goods_id, check)
            return

    def check_jump_to_exchange_shop(self, jump_lottery_id):
        if self.jump_shop_goods_id is None:
            return
        else:
            lottery_info = self.widgets_map.get(jump_lottery_id, {})
            exchange_goods_list = lottery_info.get('exchange_goods_list')
            if str(self.jump_shop_goods_id) not in exchange_goods_list:
                return
            self.jump_to_exchange_shop(jump_lottery_id, str(self.jump_shop_goods_id))
            self.jump_shop_goods_id = None
            return

    def switch_lottery_page_callback(self, lottery_id):
        info = self.widgets_map[lottery_id]
        self.panel.btn_exchange.setVisible('show_flash_exchange_entry' in info)
        self.history_widget.hide()
        self.jump_lottery_id = None
        self.refresh_price_widget(lottery_id)
        self.refresh_lottery_widget(lottery_id)
        new_lottery_widget = self.widgets_map[lottery_id]['widget']
        if self.cur_lottery_widget is not new_lottery_widget and self.cur_lottery_widget.panel:
            self.cur_lottery_widget.hide()
        self.cur_lottery_widget = new_lottery_widget
        if info.get('special_type', None):
            if info['special_type'] == 'limit_time':
                self.archive_data['lottery_%s_rp' % lottery_id] = True
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        ui and ui.update_lottery_red_point()
        self.reward_label_widget.refresh_lottery_id(lottery_id)
        self.price_top_widget.set_close_btn_visible(True)
        self.cur_lottery_widget.show()
        self.do_switch_scene()
        global_data.emgr.refresh_lobby_lottery_flag.emit()
        self.check_jump_to_exchange_shop(lottery_id)
        self.panel.PlayAnimation('show3')
        return

    def init_page_tab_widget(self):
        self.page_tap_widget = LotteryPageTapWidget(self.panel, self.widgets_list, self.jump_lottery_id, switch_callback=self.switch_lottery_page_callback)
        self.jump_lottery_id = None
        lottery_id = self.cur_lottery_id
        cls = get_lottery_cls(lottery_id, self.widgets_map[lottery_id].get('class_name', None))
        widget = cls(self.panel.temp_content, lottery_id, self.widgets_map[lottery_id], self.on_change_show_reward, auto_load_panel=False)
        self.widgets_map[lottery_id]['widget'] = widget
        self.cur_lottery_widget = widget
        return

    def improve_tips_visible_changed_callback(self, visible):
        self.panel.nd_splus_hint.setVisible(visible)
        self.panel.temp_hint.lab_tips.SetString(get_text_by_id(609628))
        if visible:
            self.panel.PlayAnimation('show_hint')
            self.panel.PlayAnimation('show_hint_arrow')
        else:
            self.panel.StopAnimation('show_hint')
            self.panel.StopAnimation('show_hint_arrow')

    def check_show_ex_skin_redpoint_and_bubble(self, item_no):
        ss_or_splus_vis_state = mecha_skin_utils.is_mecha_skin_customable(item_no)
        video_url = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(item_no), 'shiny_weapon_video_website', default=None)
        if ss_or_splus_vis_state and video_url:
            red_point_state = global_data.achi_mgr.get_cur_user_archive_data('ex_skin_display_video' + str(item_no), default=0)
            temp_red = self.reward_label_widget.get_btn_ss_red()
            if temp_red:
                temp_red.setVisible(not bool(red_point_state))
            btn_ss = self.reward_label_widget.get_btn_ss()
            if btn_ss:
                wpos = btn_ss.ConvertToWorldSpacePercentage(50, 50)
                lpos = self.panel.nd_splus_hint.getParent().convertToNodeSpace(wpos)
                self.panel.nd_splus_hint.setPosition(lpos)
            self.panel.nd_splus_hint.setVisible(not bool(red_point_state))
            if not mecha_skin_utils.is_s_skin_that_can_upgrade(item_no):
                self.panel.temp_hint.lab_tips.SetString(get_text_by_id(610693))
            else:
                self.panel.temp_hint.lab_tips.SetString(get_text_by_id(609628))
            if not red_point_state:
                self.panel.PlayAnimation('show_hint')
                self.panel.PlayAnimation('show_hint_arrow')
            else:
                self.panel.StopAnimation('show_hint')
                self.panel.StopAnimation('show_hint_arrow')
        else:
            temp_red = self.reward_label_widget.get_btn_ss_red()
            if temp_red:
                temp_red.setVisible(False)
            self.panel.nd_splus_hint.setVisible(False)
        return

    def init_reward_label_widget(self):
        self.reward_label_widget = LotteryRewardLabelWidget(self.panel, self, self.improve_tips_visible_changed_callback, self.check_show_ex_skin_redpoint_and_bubble)
        self.reward_label_widget.set_visible(False)

    def on_load_scene(self, *args):
        global_data.emgr.check_cur_scene_mirror_model_event.emit()
        if self.cur_lottery_widget.panel:
            force_show_model_id = self.force_show_model_id
            self.force_show_model_id = None
            self.cur_lottery_widget.refresh_show_model(show_model_id=force_show_model_id)
        return

    def on_load_scene_without_refresh_model(self, *args):
        global_data.emgr.check_cur_scene_mirror_model_event.emit()

    def _refresh_lottery_scene(self, need_refresh_model=True):
        lottery_scene_type = self.widgets_map[self.cur_lottery_id]['scene_type']
        scene_background_texture = self.widgets_map[self.cur_lottery_id].get('scene_background_texture', None)
        new_scene_type, display_type, scene_content_type = LOTTERY_SCENE_INFO.get(lottery_scene_type, LOTTERY_SCENE_INFO['normal'])
        finish_callback = self.on_load_scene if need_refresh_model else self.on_load_scene_without_refresh_model
        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, update_cam_at_once=True, finish_callback=finish_callback, belong_ui_name='LotteryMainUI', scene_content_type=scene_content_type, scene_background_texture=scene_background_texture)
        return

    def _get_specific_item_scene_path(self, item_no, item_type=None):
        if item_no is None:
            return
        else:
            if self.cur_lottery_widget.ignore_item_scene:
                return
            item_type = get_lobby_item_type(item_no) if item_type is None else item_type
            scene_path = None
            if item_type == L_ITEM_TYPE_ROLE_SKIN:
                scene_path = confmgr.get('role_info', 'RoleSkin', 'Content', str(item_no), 'zhanshi_scene_path')
            elif item_type == L_ITEM_TYPE_MECHA_SKIN:
                scene_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(item_no), 'zhanshi_scene_path')
            return scene_path

    def do_switch_scene(self):
        ui = global_data.ui_mgr.get_ui('MechaChuChangUI')
        if ui and ui.is_valid():
            return
        else:
            cur_show_model_id = self.force_show_model_id if self.force_show_model_id else self.cur_lottery_widget.get_cur_show_model_id()
            new_specific_scene_path = self._get_specific_item_scene_path(cur_show_model_id)
            if new_specific_scene_path:
                if new_specific_scene_path != self.cur_specific_item_scene_path:
                    if self.cur_scene_owner_id is not None:
                        global_data.emgr.change_model_display_scene_item.emit(None)
                    global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_const.SCENE_SKIN_ZHANSHI, new_specific_scene_path, DEFAULT_LEFT, update_cam_at_once=True, belong_ui_name='LotteryMainUI')
                    self.cur_specific_item_scene_path = new_specific_scene_path
                self.on_load_scene()
            else:
                if self.cur_specific_item_scene_path:
                    cur_scene_type = global_data.emgr.get_lobby_scene_type_event.emit()
                    if cur_scene_type and cur_scene_type[0] == scene_const.SCENE_SKIN_ZHANSHI:
                        global_data.emgr.change_model_display_scene_item.emit(None)
                        global_data.emgr.leave_current_scene.emit()
                elif self.cur_scene_owner_id and self.cur_scene_owner_id == self.cur_lottery_id:
                    self.on_load_scene()
                    return
                self.cur_specific_item_scene_path = ''
                if self.cur_scene_owner_id is not None:
                    global_data.emgr.change_model_display_scene_item.emit(None)
                self._refresh_lottery_scene()
            self.cur_scene_owner_id = self.cur_lottery_id
            return

    def refresh_item_scene(self, item_no, item_type):
        scene_path = self._get_specific_item_scene_path(item_no, item_type)
        if scene_path is not None:
            if scene_path != self.cur_specific_item_scene_path:
                global_data.emgr.change_model_display_scene_item.emit(None)
                global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_const.SCENE_SKIN_ZHANSHI, scene_path, DEFAULT_LEFT, update_cam_at_once=True, belong_ui_name='LotteryMainUI')
                self.cur_specific_item_scene_path = scene_path
        elif self.cur_specific_item_scene_path:
            self.cur_specific_item_scene_path = ''
            self._refresh_lottery_scene(need_refresh_model=False)
        return

    def refresh_lottery_limit_count(self, lottery_id, left_count, color='#SW'):
        if lottery_id != self.cur_lottery_id:
            return
        self.panel.lab_num_times.SetString(get_text_by_id(82034, {'num': str(left_count)}))
        self.panel.lab_num_times.SetColor(color)

    def refresh_price_widget(self, lottery_id):
        self.price_top_widget.refresh_lottery_ticket(lottery_id)
        self.price_top_widget.show_money_types(self.widgets_map[lottery_id]['show_money_type'])

    def refresh_lottery_widget(self, lottery_id):
        widget = self.widgets_map[lottery_id].get('widget', None)
        if not widget:
            cls = get_lottery_cls(lottery_id, self.widgets_map[lottery_id].get('class_name', None))
            widget = cls(self.panel.temp_content, lottery_id, self.widgets_map[lottery_id], self.on_change_show_reward)
            self.widgets_map[lottery_id]['widget'] = widget
        widget.load_panel()
        self.panel.nd_btn_reward_change.setVisible('hide_switch_arrow' not in self.widgets_map[lottery_id])
        self.refresh_widget_data(widget)
        if hasattr(widget, 'set_visible_close'):
            widget.set_visible_close(self.page_tap_widget.is_visible_close(lottery_id))
        return

    def refresh_widget_data(self, widget):
        widget.refresh()

    @staticmethod
    def _get_item_no_and_type(item_no):
        item_type = get_lobby_item_type(item_no)
        if item_type == L_ITEM_TYPE_EXPERIENCE_CARD:
            use_params = get_lobby_item_use_parms(item_no) or {}
            add_item_no = use_params.get('add_item', None)
            if add_item_no:
                item_no = add_item_no
                item_type = get_lobby_item_type(item_no)
        return (
         item_no, item_type)

    def _play_chuchang_video(self, item_id, specific_name, force_show_chuchang, video_path):

        def call_back():
            if not (self.panel and self.panel.isValid()):
                return
            if not self.panel.IsVisible():
                return
            self.on_change_show_reward(item_id, specific_name, force_show_chuchang)
            self.refresh_switch_core_model_button_visible()
            self.panel.nd_display.setVisible(True)

        if not global_data.video_player.is_in_init_state():
            if not global_data.video_player.player:
                global_data.video_player.reset_data()
            else:
                self.chuchang_video_dict[item_id] = True
                self.on_change_show_reward(item_id, specific_name, force_show_chuchang)
                return
        if self.chuchang_video_dict.get(item_id, False):
            self.on_change_show_reward(item_id, specific_name, force_show_chuchang)
            return
        self.panel.nd_display.setVisible(False)
        self.panel.nd_btn_reward_change.setVisible(False)
        video_path = 'video/%s.mp4' % video_path
        global_data.video_player.play_video(video_path, call_back, repeat_time=1, bg_play=True)
        self.chuchang_video_dict[item_id] = True

        @self.panel.layer_video.unique_callback()
        def OnClick(_layer, _touch, *args):
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video()

    def on_equip_check_callback(self, skin_id):
        if str(self.cur_show_model_id) != str(skin_id):
            if self.cur_lottery_widget.panel:
                if self.cur_lottery_widget.__class__.__name__ == 'LotteryCommonMutiTurntableWidget':
                    self.cur_lottery_widget.refresh_show_model(show_model_id=skin_id, skip_list_check=True)

    def on_change_show_reward(self, item_id, specific_name=None, force_show_chuchang=False, force_label_skin=None, pet_level=1):
        self.set_mecha_preview_advanced_apperance_widget_visible(False)
        self.set_btn_change_visible(False)
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        video_path = check_play_chuchang_video_with_tag(item_id, self.video_played_tag)
        if video_path and not self.chuchang_video_dict.get(item_id, False):
            self._play_chuchang_video(item_id, specific_name, force_show_chuchang, video_path)
            self.panel.btn_glass.setVisible(False)
            return
        else:
            self.refresh_switch_core_model_button_visible()
            self.panel.nd_display.setVisible(True)
            item_no = item_id
            self.cur_model_id = item_id
            self.cur_show_model_id = item_id
            self.force_show_model_id = None
            item_no, item_type = self._get_item_no_and_type(item_no)
            show_model = item_type in MODEL_DISPLAY_TYPE or item_type == L_ITEM_TYPE_MECHA_SP_ACTION
            self.force_label_skin = force_label_skin
            if self.force_label_skin:
                label_sp_item_no, label_item_type = self._get_item_no_and_type(self.force_label_skin)
                label_show_model = label_item_type in MODEL_DISPLAY_TYPE or label_item_type == L_ITEM_TYPE_MECHA_SP_ACTION
            else:
                label_show_model = None
                label_sp_item_no = None
                label_item_type = None
            self.panel.nd_splus_hint_vis.setVisible(show_model)
            self.reward_label_widget.refresh_reward_info(item_no, specific_name, show_model)
            if self._skin_pic_nd:
                self._skin_pic_nd.setVisible(False)
            self.panel.btn_glass.setVisible(False)
            if show_model:
                if not has_skin_ext():
                    self._ext_show_org_painting(item_no, item_type)
                    return
                if not self.cur_lottery_widget.ignore_chuchang_anim and global_data.emgr.check_mecha_chuchang.emit(item_id, self.__class__.__name__, force_show_chuchang)[0]:
                    self.mecha_transform_ui_widget.refresh_transform_data_with_lobby_item(item_no, item_type)
                    self.mecha_preview_advanced_appearance_widget.refresh_show_model(item_no, item_type)
                    self.cur_specific_item_scene_path = True
                    global_data.hide_ui_when_show_model_in_lottery and self.do_hide_panel()
                    return
                create_callback = None
                if item_type == L_ITEM_MECHA_SFX:
                    model_data, create_callback = get_mecha_sfx_model_data(item_no)
                elif item_type == L_ITEM_TYPE_GESTURE:
                    model_data = items_book_utils.get_gesture_model_data(item_no)
                elif item_type == L_ITEM_TYPE_EMOTICON:
                    model_data = items_book_utils.get_emoji_model_data(item_no)
                elif item_type in ITEM_TYPE_DEC:
                    model_data = get_pendant_show_data(item_no, is_get_player_data=False, rotate_pendant=True)
                    for data in model_data:
                        if data.get('show_anim') and data.get('end_anim'):
                            data['show_anim'] = data['end_anim']

                elif item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
                    item_info = confmgr.get('lobby_item', str(item_no))
                    mecha_item_id = item_info.get('cDisplayItemId', get_lobby_item_belong_no(item_no))
                    model_data = get_lobby_model_data(mecha_item_id, is_get_player_data=False)
                    submesh_path = get_mecha_model_h_path(None, mecha_item_id)
                    res = confmgr.get('lobby_item', str(item_no), 'res', default='ar_mm_1')
                    for data in model_data:
                        if data.get('show_anim') and data.get('end_anim'):
                            data['show_anim'] = res
                            data['end_anim'] = res

                elif item_type == L_ITEM_TYPE_MECHA_SKIN:
                    model_data = get_lobby_model_data(item_no, is_get_player_data=False)
                elif item_type == L_ITEM_TYPE_ROLE_SKIN:
                    default_show_decoration_dict = get_skin_default_show_decoration_dict(item_no)
                    head_id = default_show_decoration_dict.get(FASHION_POS_HEADWEAR)
                    bag_id = default_show_decoration_dict.get(FASHION_POS_BACK)
                    suit_id = default_show_decoration_dict.get(FASHION_POS_SUIT_2)
                    other_pendants = [ default_show_decoration_dict.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
                    model_data = get_lobby_model_data(item_no, skin_id=item_no, head_id=head_id, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants, is_get_player_data=False)
                elif item_type == L_ITEM_TYPE_PET_SKIN:
                    model_data = get_lobby_model_data(item_no, pet_level=pet_level)
                else:
                    model_data = get_lobby_model_data(item_no, is_get_player_data=False)
                if not model_data:
                    log_error('-----------Lottery-----------Not existed model id')
                    return
                if 'skin_id' in model_data[0]:
                    self.cur_show_model_id = model_data[0]['skin_id']
                if item_type in ITEM_TYPE_DEC:
                    self.refresh_item_scene(self.cur_show_model_id, L_ITEM_TYPE_ROLE_SKIN)
                else:
                    self.refresh_item_scene(item_no, item_type)
                if not self.cur_specific_item_scene_path:
                    new_item_type = get_lobby_item_type(item_no)
                    if model_data[0]['mpath'].find('8001') != -1 or model_data[0]['mpath'].find('8005') != -1:
                        display_type = LUCKY_HOUSE_SMALL
                    elif new_item_type in (L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE, L_ITEM_YTPE_VEHICLE_SKIN):
                        display_type = LUCKY_HOUSE_GUN
                    else:
                        display_type = LUCKY_HOUSE
                else:
                    display_type = global_data.emgr.get_lobby_display_type_event.emit()[0]
                global_data.emgr.set_lobby_scene_display_type.emit(display_type)
                model_offset = self.get_model_offset()
                if model_offset:
                    for info in model_data:
                        info['off_position'] = model_offset

                model_scale = None
                if global_data.lottery_model_scale:
                    model_scale = global_data.lottery_model_offset
                elif self.cur_show_model_id in self.cur_lottery_widget.custom_model_scale:
                    model_scale = self.cur_lottery_widget.custom_model_scale[self.cur_show_model_id]
                elif self.cur_lottery_widget.common_model_scale:
                    model_scale = self.cur_lottery_widget.common_model_scale
                if model_scale:
                    for info in model_data:
                        info['model_scale'] = model_scale

                self.mecha_transform_ui_widget.refresh_transform_data_with_lobby_item(item_no, item_type)
                self.mecha_preview_advanced_appearance_widget.refresh_show_model(item_no, item_type)
                self.is_model_loaded = False

                def on_create_callback(model):
                    if not (self.panel and self.panel.isValid() and self.panel.isVisible()):
                        return
                    if callable(create_callback):
                        create_callback(model)
                    self.set_mecha_preview_advanced_apperance_widget_visible(True)
                    if self.mecha_preview_advanced_appearance_widget and item_type == L_ITEM_TYPE_ROLE_SKIN:
                        need_show = self.mecha_preview_advanced_appearance_widget.is_select() and not self.is_model_loaded
                        if need_show:
                            self.mecha_preview_advanced_appearance_widget.set_select_result(need_show)
                    self.is_model_loaded = True

                need_show = self.mecha_preview_advanced_appearance_widget.is_select()
                if need_show:
                    if item_type == L_ITEM_TYPE_MECHA_SKIN:
                        model_data[0]['shiny_weapon_id'] = mecha_skin_utils.get_mecha_conf_ex_weapon_sfx_id(self.cur_show_model_id)
                global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_create_callback)
                global_data.emgr.reset_rotate_model_display.emit()
                if item_type in ROLE_SCALE_CAM_KEY:
                    role_id = get_lobby_item_belong_no(item_no)
                    self.update_cam_data_with_role_id(role_id, item_type)
                    self.panel.btn_glass.setVisible(True)
                    if item_type in (L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_BODY):
                        self.on_click_btn_glass(cam_mode=CAM_MODE_FAR)
                    else:
                        self.on_click_btn_glass(cam_mode=CAM_MODE_NEAR)
            else:
                if is_chuchang_scene():
                    global_data.emgr.end_mecha_chuchang_scene.emit()
                    global_data.emgr.set_last_chuchang_id.emit(None)
                self.refresh_item_scene(item_no, item_type)
                global_data.emgr.change_model_display_scene_item.emit(None)
                if not self.force_label_skin:
                    self.mecha_transform_ui_widget.refresh_transform_data_with_lobby_item(item_no, item_type)
                    self.mecha_preview_advanced_appearance_widget.refresh_show_model(item_no, item_type)
                else:
                    self.mecha_transform_ui_widget.refresh_transform_data_with_lobby_item(item_no, item_type)
                    self.mecha_preview_advanced_appearance_widget.refresh_show_model(force_label_skin, label_item_type)
            if self.mecha_preview_advanced_appearance_widget.is_visible():
                if force_label_skin is not None:
                    if force_label_skin == self.cur_show_model_id:
                        self.mecha_preview_advanced_appearance_widget.set_select_with_click(bool(force_label_skin))
                    else:
                        self.set_mecha_preview_advanced_apperance_widget_visible(False)
            return

    def get_model_offset(self):
        model_offset = None
        if not self.cur_show_model_id:
            return model_offset
        else:
            if global_data.lottery_model_offset:
                model_offset = global_data.lottery_model_offset
            else:
                if int(self.cur_show_model_id) in self.cur_lottery_widget.custom_model_offset:
                    model_offset = self.cur_lottery_widget.custom_model_offset[int(self.cur_show_model_id)]
                elif self.cur_lottery_widget.common_model_offset:
                    model_offset = self.cur_lottery_widget.common_model_offset
                elif self.cur_specific_item_scene_path:
                    model_offset = MODEL_OFFSET
                if not self.is_normal_model_offset and model_offset and self.cur_cam_mode == CAM_MODE_FAR:
                    preview_offset = copy.deepcopy(model_offset)
                    preview_offset[0] += 8
                    return preview_offset
            return model_offset

    def set_model_offset(self, is_normal, is_slerp=True):
        self.is_normal_model_offset = is_normal
        model_offset = self.get_model_offset()
        if model_offset:
            global_data.emgr.change_model_display_off_position.emit(model_offset, is_slerp)

    def _ext_show_org_painting(self, in_item_id, in_item_type):
        if is_chuchang_scene():
            global_data.emgr.end_mecha_chuchang_scene.emit()
            global_data.emgr.set_last_chuchang_id.emit(None)
        global_data.emgr.change_model_display_scene_item.emit(None)
        if not self._skin_pic_nd:
            self._skin_pic_nd = global_data.uisystem.load_template_create('common/i_common_preview_pic', self.panel.nd_pic)
        self._skin_pic_nd.setVisible(True)
        pic = get_detail_pic_by_item_no(in_item_id)
        self._skin_pic_nd.pic.SetDisplayFrameByPath('', pic)
        if in_item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN):
            self._skin_pic_nd.pic.setScale(0.6)
        elif in_item_type in (L_ITEM_YTPE_VEHICLE_SKIN,):
            self._skin_pic_nd.pic.setScale(1.5)
        else:
            self._skin_pic_nd.pic.setScale(1.0)
        return

    def on_app_resume(self):
        if not self.panel.isVisible():
            return
        if not self.page_tap_widget.try_app_resume_refresh():
            self.close()

    def refresh_switch_core_model_button_visible(self, force_visible=None):
        if self.panel and self.panel.isValid():
            if force_visible is None:
                self.panel.nd_btn_reward_change.setVisible('hide_switch_arrow' not in self.widgets_map[self.cur_lottery_id])
            else:
                self.panel.nd_btn_reward_change.setVisible(force_visible)
        return

    def set_close_btn_visible(self, ui_name, visible):
        if ui_name == self.__class__.__name__:
            self.price_top_widget.set_close_btn_visible(visible)

    def _set_node_visible_by_name(self, nd_name, visible):
        single_name_list = nd_name.split('.')
        nd = getattr(self.panel, single_name_list[0], None)
        nd_level = len(single_name_list)
        for i in range(1, nd_level):
            nd = getattr(nd, single_name_list[i], None)

        if nd:
            nd.setVisible(visible)
            if visible:
                nd in self.force_hide_node and self.force_hide_node.remove(nd)
            else:
                nd not in self.force_hide_node and self.force_hide_node.add(nd)
        return

    def hide_lottery_main_ui_elements(self, hide, extra_element_list=(), need_refresh_scene=False):
        visible = not hide
        if type(extra_element_list) == str:
            extra_element_list = (
             extra_element_list,)
        for extra_element in extra_element_list:
            self._set_node_visible_by_name(extra_element, visible)

        if visible and need_refresh_scene:
            self.do_switch_scene()

    def update_lottery_main_prices(self, money_types):
        if self.price_top_widget:
            self.price_top_widget.show_money_types(money_types)

    def set_cur_lucky_draw_info(self, lottery_id, lottery_count):
        self.cur_draw_lottery_id = lottery_id
        self.cur_draw_lottery_count = lottery_count

    def get_cur_lucky_draw_info(self):
        return (
         self.cur_draw_lottery_id, self.cur_draw_lottery_count)

    def on_receive_lottery_result(self, item_list, origin_list, extra_data, is_10_try=False, extra_info=None):
        if self.cur_draw_lottery_id is None:
            return
        else:
            if self.cur_draw_lottery_id not in self.widgets_map:
                return
            if getattr(self.widgets_map[self.cur_draw_lottery_id]['widget'], 'turntable_widget', None):
                self.widgets_map[self.cur_draw_lottery_id]['widget'].on_receive_lottery_result(item_list, origin_list)
            elif extra_data:
                self.widgets_map[self.cur_draw_lottery_id]['widget'].on_receive_lottery_result(item_list, origin_list, extra_data)
            else:
                is_new_lottery = confmgr.get('lottery_page_config', self.cur_draw_lottery_id, 'is_new_lottery', default=0)
                if is_new_lottery:
                    self._lottery_video_controller.play_lottery_video(item_list, origin_list, extra_info, self.cur_draw_lottery_id)
                else:
                    from logic.comsys.mall_ui.OpenBoxUI import OpenBoxUI
                    open_box_ui = OpenBoxUI()
                    open_box_ui.set_box_items(item_list, origin_list, is_10_try, extra_info)
            global_data.emgr.lottery_data_ready.emit()
            self.cur_draw_lottery_id = None
            return

    def on_lottery_video_list_finished(self):
        pass

    def refresh_red_point(self, *args, **kargs):
        self.page_tap_widget.refresh_red_point()

    def set_lottery_reward_info_label_visible(self, visible):
        self.reward_label_visible = visible
        self.reward_label_widget.set_visible(visible)
        if not visible:
            self.improve_tips_visible_changed_callback(False)

    def set_preview_widget_visible(self, is_visible):
        self.panel.StopAnimation('show_nd_review')
        self.panel.StopAnimation('show_nd_content')
        if is_visible:
            self.panel.PlayAnimation('show_nd_review')
            self.play_lottery_reward_info_label_animation('show_nd_review')
            self.set_model_offset(False)
        else:
            self.panel.PlayAnimation('show_nd_content')
            self.play_lottery_reward_info_label_animation('show_nd_content')
            self.set_model_offset(True)

    def play_lottery_reward_info_label_animation(self, animation_name):
        self.reward_label_widget.play_animation(animation_name)

    def set_mecha_preview_advanced_appearance_visible(self, visible):
        self.set_mecha_preview_advanced_apperance_widget_visible(visible)

    def set_mecha_translation_widget_visible(self, visible):
        self.panel.btn_glass.setVisible(visible)
        self.set_btn_change_visible(visible)

    def on_begin_drag_model(self, *args):
        self.cur_lottery_widget and self.cur_lottery_widget.on_begin_drag_model()

    def on_drag_model(self, layer, touch, *args, **kwargs):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def on_end_drag_model(self, *args):
        self.cur_lottery_widget and self.cur_lottery_widget.on_end_drag_model()

    def on_click_btn_glass(self, *args, **kwargs):
        cam_mode = kwargs.get('cam_mode', None)
        reset = kwargs.get('reset', False)
        if cam_mode is None:
            if self.cur_cam_mode == CAM_MODE_FAR:
                cam_mode = CAM_MODE_NEAR if 1 else CAM_MODE_FAR
            self.cur_cam_mode = cam_mode
            btn_pic = CAM_DISPLAY_PIC[cam_mode]
            self.panel.icon_glass.SetDisplayFrameByPath('', btn_pic)
            cam_pos = reset or self.get_cam_data(cam_mode)
            if cam_pos:
                global_data.emgr.change_model_display_scene_cam_pos.emit(cam_pos, True)
        model_offset = self.get_model_offset()
        if model_offset:
            global_data.emgr.change_model_display_off_position.emit(model_offset, True)
        return

    def on_click_btn_last_reward(self, *args, **kwargs):
        self.cur_lottery_widget and self.cur_lottery_widget.switch_show_model(-1)

    def on_click_btn_next_reward(self, *args, **kwargs):
        self.cur_lottery_widget and self.cur_lottery_widget.switch_show_model(1)

    def on_click_btn_exchange(self, *args, **kwargs):
        jump_to_mall(i_types=(FLASH_EXCHANGE, 0))

    def on_resolution_changed(self):
        for loid, widget in six.iteritems(self.widgets_map):
            print('widget', widget)
            if 'widget' not in widget:
                continue
            if hasattr(widget['widget'], 'on_resolution_changed'):
                widget['widget'].on_resolution_changed()

    def get_cam_data(self, data_key):
        if self.cam_data is None and not self.update_cam_data_with_role_id():
            return
        else:
            return self.cam_data[data_key]

    def update_cam_data_with_role_id(self, role_id=None, dec_type=None):
        if role_id is None:
            role_id = get_lobby_item_belong_no(self.cur_show_model_id)
            dec_type = get_lobby_item_type(self.cur_model_id)
        import world
        cam_ctrl = world.get_active_scene().get_com('PartModelDisplayCamera')
        if not cam_ctrl:
            self.cam_data = None
            return False
        else:
            cam_pos = cam_ctrl.camera_ctrl.target_position
            cam_data = confmgr.get('lobby_model_display_conf', 'SpecialRoleSkinDefineCam', 'Content', str(self.cur_show_model_id))
            if not cam_data:
                cam_data = confmgr.get('lobby_model_display_conf', 'RoleSkinDefineCam', 'Content', str(role_id))
            if not cam_data:
                self.cam_data = None
                return False
            import math3d
            far_cam = math3d.vector(*cam_data['far_cam'])
            near_cam_key = ROLE_SCALE_CAM_KEY[dec_type]
            if near_cam_key == 'far_cam':
                near_cam_key = 'near_cam'
            near_cam = math3d.vector(*cam_data[near_cam_key])
            near_cam = near_cam - far_cam
            self.cam_data = {CAM_MODE_FAR: cam_pos,
               CAM_MODE_NEAR: near_cam + cam_pos
               }
            return True

    def get_page_tab_widget(self):
        return self.page_tap_widget

    def is_valid_lottery_id(self, lottery_id):
        return self.widgets_map and lottery_id in self.widgets_map

    def get_lottery_widget(self, lottery_id):
        return self.widgets_map.get(lottery_id, {}).get('widget')