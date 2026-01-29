# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/MechaSettingWidget.py
from __future__ import absolute_import
import cc
import six
import six_ex
from logic.comsys.accelerometer.AccInput import AccInput
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE, OPEN_CONDITION_OPEN, OPEN_CONDITION_AIM_OPEN
from logic.gcommon.common_const import ui_operation_const as uoc
from .SettingWidgetBase import SettingWidgetBase
from logic.gutils.template_utils import init_radio_group, init_radio_group_new, attach_radio_group_data, set_radio_group_item_select, set_radio_group_item_select_new, set_radio_group_enable_state, init_checkbox_group, attach_checkbox_group_data, set_check_box_group_item_select, set_radio_group_enable_state_new
import game3d
from logic.gutils.setting_utils import SettingTips
FAQ_TITLE_ID = 2293
MECHA_ITEM_PATH = 'setting/i_setting_mecha_item.json'
HEAD_IMG_PATH = 'gui/ui_res_2/mall/10100{}_2.png'

def enable_rush_rocker_drag(enable):
    if global_data.mecha and global_data.mecha.logic:
        global_data.mecha.logic.send_event('E_ENABLE_ROCKER_DRAG', 'action6', enable)


MECHA_SETTING_LIST = {8004: [
        [
         [
          2275, 2282, 2283], {'key': uoc.JUMP_TRIGGER_PRESS_8004,'faq_text_id': 2291,'callback_func': global_data.emgr.update_jump_trigger_press_8004.emit,'flip': True}]],
   8007: [
        [
         [
          2273, 2276, 2277], {'key': uoc.AIM_TRIGGER_PRESS_8007,'faq_text_id': 2285,'flip': True}]],
   8008: [
        [
         [
          2275, 2282, 2283], {'key': uoc.JUMP_TRIGGER_PRESS_8008,'faq_text_id': 2291,'callback_func': global_data.emgr.update_jump_trigger_press_8008.emit,'flip': True}]],
   8009: [
        [
         [
          2398, 80594, 80595], {'key': uoc.WEAPON_FAST_SWITCH_8009,'faq_text_id': 2399,'callback_func': global_data.emgr.update_weapon_fast_switch_8009.emit}]],
   8010: [
        [
         [
          2274, 2282, 2283], {'key': uoc.BOOST_TRIGGER_PRESS_8010,'faq_text_id': 2290,'flip': True}],
        [
         [
          2400, 2401, 2402], {'key': uoc.BOOST_AUTO_CAMERA_8010,'faq_text_id': 2403}]],
   8012: [
        [
         [
          2300, 2282, 2283], {'key': uoc.CONTINUOUSLY_SHOOT_TRIGGER_PRESS_8012,'faq_text_id': 2301,'flip': True}],
        [
         [
          2332, 80594, 80595], {'key': uoc.BOOST_HIT_AUTO_TRIGGER_TRANSFORM_8012,'faq_text_id': 2333}]],
   8013: [
        [
         [
          83575, 80594, 80595], {'key': uoc.WEAKEN_PVE_SFX_TYPE_8013,'faq_text_id': 83576}]],
   8014: [
        [
         [
          83483, 80594, 80595], {'key': uoc.SHOW_SLASH_TYPE_8014,'faq_text_id': 83491,'callback_func': global_data.emgr.update_show_slash_type_8014.emit}]],
   8016: [
        [
         [
          2394, 2395, 2396], {'key': uoc.DASH_CAM_DIR_8016,'faq_text_id': 2397,'callback_func': global_data.emgr.dash_dir_type_8016.emit}]],
   8018: [
        [
         [
          860442, 860443, 860444], {'key': uoc.DRAG_DASH_BTN_8018,'faq_text_id': 860445,'callback_func': enable_rush_rocker_drag}]],
   8019: [
        [
         [
          609980, 80594, 80595], {'key': uoc.DASH_AUTO_DEFEND_8019,'faq_text_id': 609981,'callback_func': global_data.emgr.dash_auto_defend_8019.emit}]],
   8020: [
        [
         [
          83130, 80594, 80595], {'key': uoc.ROCKER_CONTROL_CAMERA_8020,'faq_text_id': 83131,'callback_func': global_data.emgr.enable_rocker_control_camera_8020.emit}]],
   8022: [
        [
         [
          83151, 83152, 83153], {'key': uoc.MAIN_FIRE_ON_RELEASE_8022,'faq_text_id': 2392,'flip': True,'callback_func': global_data.emgr.update_main_fire_on_release_8022.emit}],
        [
         [
          2275, 2282, 2283], {'key': uoc.JUMP_TRIGGER_PRESS_8022,'faq_text_id': 2291,'flip': True,'callback_func': global_data.emgr.update_jump_trigger_press_8022.emit}]],
   8023: [
        [
         [
          605022, 80594, 80595], {'key': uoc.FAST_AIM_FIRE_8023,'faq_text_id': 605023,'callback_func': global_data.emgr.update_fast_aim_fire_8023.emit}],
        [
         [
          605024, 83606, 605026], {'key': uoc.NO_CLOSE_AIM_LOAD_8023,'faq_text_id': 605027,'callback_func': global_data.emgr.update_no_close_aim_load_8023.emit}],
        [
         [
          605028, 80594, 80595], {'key': uoc.AIM_RELOAD_WITHOUT_REOPEN_AIM_8023,'faq_text_id': 605029,'callback_func': global_data.emgr.update_reload_without_reopen_8023.emit}]],
   8026: [
        [
         [
          2360, 2282, 2283], {'key': uoc.SHIELD_TRIGGER_PRESS_8026,'faq_text_id': 2361,'flip': True}],
        [
         [
          860442, 860443, 860444], {'key': uoc.DRAG_DASH_BTN_8026,'faq_text_id': 860445,'callback_func': enable_rush_rocker_drag}]],
   8027: [
        [
         [
          2360, 2380, 2379], {'key': uoc.SUBWEAPON_FIRE_ON_AUTO_8027,'faq_text_id': 2378,'flip': True,'callback_func': global_data.emgr.update_sub_fire_on_auto_8027.emit}],
        [
         [
          860442, 860443, 860444], {'key': uoc.DRAG_DASH_BTN_8027,'faq_text_id': 860445,'callback_func': enable_rush_rocker_drag}]],
   8029: [
        [
         [
          2271, 2371, 2373], {'key': uoc.SHOTGUN_FIRE_ON_NOT_AUTO_8029,'faq_text_id': 2372,'flip': True,'callback_func': global_data.emgr.update_shotgun_fire_not_auto_8029.emit,'combine_with_next': True}],
        [
         [
          None, 2279, 2278], {'key': uoc.SHOTGUN_FIRE_ON_RELEASE_8029,'faq_text_id': 2372,'flip': True,'callback_func': global_data.emgr.update_shotgun_fire_on_release_8029.emit}],
        [
         [
          2374, 2375, 2376], {'key': uoc.TRANSLATION_USE_PHANTOM_FORWARD_8029,'faq_text_id': 2377,'flip': True,'callback_func': global_data.emgr.update_translation_forward_8029.emit}]],
   8030: [
        [
         [
          2381, 80594, 80595], {'key': uoc.ROCKER_JUMP_8030,'faq_text_id': 2382,'callback_func': global_data.emgr.update_rocker_jump_8030.emit}]],
   8034: [
        [
         [
          2274, 2380, 2379], {'key': uoc.DASH_TRIGGER_TYPE_8034,'faq_text_id': 2393,'callback_func': global_data.emgr.update_dash_trigger_type_8034.emit}]]
   }

class MechaSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(MechaSettingWidget, self).__init__(panel, parent)
        self.key_2_choose = {}

    def on_init_panel(self, **kwargs):
        self._init_members()
        total_height = 0
        for setting_list in six.itervalues(MECHA_SETTING_LIST):
            total_height += 64
            total_height += len(setting_list) * 60

        self.panel.SetContentSize(923, total_height + 35)
        self.panel.ResizeAndPosition(False)
        item_cnt = 1
        total_height = 0
        wait_combine_item, wait_combine_kwarg = (None, None)
        mecha_id_list = six_ex.keys(MECHA_SETTING_LIST)
        if global_data.mecha and global_data.mecha.logic:
            mecha_id = global_data.mecha.logic.ev_g_mecha_id()
            mecha_id_list.sort(key=lambda x: (x != mecha_id, x))
        for mecha_id in mecha_id_list:
            setting_list = MECHA_SETTING_LIST[mecha_id]
            is_first = True
            for (setting_name, choose1, choose2), kwargs in setting_list:
                item = global_data.uisystem.load_template_create(MECHA_ITEM_PATH)
                self.panel.nd_tab_mecha.AddChild('choose_{}'.format(item_cnt), item)
                item_cnt += 1
                if is_first:
                    height = 124 if 1 else 60
                    item.SetContentSize('100%', height)
                    item.SetPosition('50%', '100%-{}'.format(total_height))
                    total_height += height
                    item.title.setVisible(is_first)
                    if is_first:
                        item.img_head.SetDisplayFrameByPath('', HEAD_IMG_PATH.format(mecha_id))
                        item.title.SetString(210000 + mecha_id)
                    item.lab_text.setVisible(bool(setting_name))
                    if setting_name:
                        item.lab_text.SetString(setting_name)
                    item.choose_1.text.SetString(choose1)
                    item.choose_2.text.SetString(choose2)
                    if kwargs.get('combine_with_next', False):
                        wait_combine_item = item
                        wait_combine_kwarg = kwargs
                    elif wait_combine_item:
                        self._setup_combine_choose(wait_combine_item, wait_combine_kwarg['key'], wait_combine_kwarg['faq_text_id'], item, kwargs['key'], kwargs['faq_text_id'], wait_combine_kwarg.get('callback_func', None), kwargs.get('callback_func', None), wait_combine_kwarg.get('flip', False))
                        wait_combine_item = wait_combine_kwarg = None
                    else:
                        self._setup_common_choose(item, **kwargs)
                    is_first = False

        return

    def destroy(self):
        self.key_2_choose.clear()
        super(MechaSettingWidget, self).destroy()

    def on_enter_page(self, **kwargs):
        super(MechaSettingWidget, self).on_enter_page()
        size = self.panel.GetContentSize()

    def on_exit_page(self, **kwargs):
        super(MechaSettingWidget, self).on_exit_page()

    def on_recover_default(self, **kwargs):
        default_values = {}
        for key in uoc.ADVANCED_MECHA_SETTINGS:
            value = global_data.player.get_default_setting_2(key)
            global_data.player.write_setting_2(key, value, True)
            default_values[key] = value
            if key in self.key_2_choose:
                set_radio_group_item_select(self.key_2_choose[key], value, True)

    def _init_members(self):
        self._sw_h_maps = {}

    def init_panel(self, page):
        self._refresh_panel(page)

    def _refresh_panel(self, page):
        pass

    def _setup_common_choose(self, choose, key, faq_text_id, callback_func=None, flip=False):
        init_radio_group(choose)
        choose_1 = choose.choose_1
        choose_2 = choose.choose_2
        attach_radio_group_data([choose_1, choose_2], [not flip, flip])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = not flip
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(key, val, True)
                callable(callback_func) and callback_func(val)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = flip
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(key, val, True)
                callable(callback_func) and callback_func(val)

        if global_data.player:
            set_radio_group_item_select(choose, global_data.player.get_setting_2(key), False)

        @choose.lab_text.nd_auto_fit.btn_question.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, faq_text_id, btn)

        self.key_2_choose[key] = choose

    def _setup_combine_choose(self, choose1, key1, faq_text_id1, choose2, key2, faq_text_id2, callback_func1=None, callback_func2=None, flip=False):

        def real_callback(flag):
            set_radio_group_enable_state_new(global_data.player.get_setting_2(key1), global_data.player.get_setting_2(key2), choose2)
            callback_func1 and callback_func1(flag)

        self._setup_common_choose(choose1, key1, faq_text_id1, real_callback, flip)
        self._setup_common_choose(choose2, key2, faq_text_id2, callback_func2, flip)
        set_radio_group_enable_state_new(global_data.player.get_setting_2(key1), global_data.player.get_setting_2(key2), choose2)

    def _on_question_click(self, title_id, content_id, btn=None):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(title_id, content_id)
        if btn is not None:
            lpos = btn.getPosition()
            wpos = btn.getParent().convertToWorldSpace(lpos)
            lpos2 = dlg.panel.nd_game_describe.getParent().convertToNodeSpace(wpos)
            dlg.panel.nd_game_describe.setPosition(cc.Vec2(lpos2.x, lpos2.y + 200))
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
        return