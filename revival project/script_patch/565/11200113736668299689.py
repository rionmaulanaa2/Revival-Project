# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_0, UI_VKB_CUSTOM, UI_TYPE_MESSAGE
from logic.gcommon.common_const.scene_const import SCENE_PVE_MAIN_UI
from logic.client.const.lobby_model_display_const import PVE_MAIN_UI
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data, get_cam_position
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path, battle_id_to_mecha_lobby_id, DEFAULT_CLOTHING_ID
from logic.gutils.skin_define_utils import get_main_skin_id
from .PVELeftTopWidget import PVELeftTopWidget
from .PVELeftButtonWidget import PVELeftButtonWidget
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_ITEM_PVE_KEY, SHOP_PAYMENT_ITEM_PVE_COIN
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, MATCH_AGAIN_TYPE_NONE
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.gutils.pve_utils import update_model_and_cam_pos
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
import math3d
import six_ex
import cc
MAX_MECHA_CLICK_DIST = 30
CURRENT_DEBRIS_COLOR = '<size=29><color=0x00DFFFFF>{}/</color></size>'
FINISH_ALL_DEBRIS_COLOR = '<size=18><color=0x00DFFFFF>{}</color></size>'
NORMAL_ALL_DEBRIS_COLOR = '<size=18><color=0x939494FF>{}</color></size>'

def get_cls(cls_name, module_path):
    mconf = __import__(module_path, globals(), locals(), [cls_name], 0)
    if not mconf:
        raise Exception('no such ui dialog class %s in %s' % (cls_name, module_path))
    module = getattr(mconf, cls_name, None)
    dlg_cls = getattr(module, cls_name, None)
    return dlg_cls


class PVEMainUI(BasePanel):
    DELAY_CLOSE_TAG = 20231127
    PANEL_CONFIG_NAME = 'pve/pve_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'btn_close.OnClick': 'ui_vkb_custom_func'
       }
    GLOBAL_EVENT = {'on_pve_mecha_changed': 'on_pve_mecha_changed',
       'on_pve_mecha_skin_changed': 'on_pve_mecha_skin_changed',
       'refresh_share_mecha_skin': 'on_pve_mecha_changed',
       'on_get_pve_unreceived_story_debris_update': 'check_show_red_point',
       'player_join_team_event': 'update_teammate_state',
       'player_leave_team_event': 'update_teammate_state',
       'player_add_teammate_event': 'update_teammate_state',
       'player_del_teammate_event': 'update_teammate_state',
       'pve_battle_info_change_event': 'update_teammate_state'
       }
    START_FIGHT_INDEX = 0
    STATIC_TABLE_BTN_CLS = None
    STATIC_WIDGET_UI_DATA = [
     {'cls_name': 'PVELevelWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'tag_name': 'level',
        'ui_item_name': 'temp_tab_1',
        'normal_position': [
                          -130, 0, 0],
        'anim_name': 'loop'
        },
     {'cls_name': 'PVEMechaWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'tag_name': 'mecha',
        'ui_item_name': 'temp_tab_2',
        'normal_position': [
                          -132, 0, 0]
        },
     {'cls_name': 'PVEPetWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'tag_name': 'pet',
        'ui_item_name': 'temp_tab_3',
        'anim_name': 'loop'
        },
     {'cls_name': 'PVETalentWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'tag_name': 'talent',
        'ui_item_name': 'temp_tab_4'
        },
     {'cls_name': 'PVEEquipWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'tag_name': 'equip',
        'ui_item_name': 'temp_tab_5',
        'is_open': False
        },
     {'cls_name': 'PVEBattleShopWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'tag_name': 'battleshop',
        'ui_item_name': 'temp_tab_6',
        'is_open': False
        }]
    STATIC_LEFT_BTN_CLS = None
    STATIC_LEFT_UI_CONFIG = [
     {'cls_name': 'PVECareerWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'icon': 'gui/ui_res_2/pve/main/icon_pve_main_rank_ac.png',
        'label_id': 80627,
        'tag_name': 'achievement'
        },
     {'cls_name': 'PVEBookWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'icon': 'gui/ui_res_2/pve/main/icon_pve_main_catalogue.png',
        'label_id': 390,
        'tag_name': 'book'
        },
     {'cls_name': 'PVEDebrisWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'icon': 'gui/ui_res_2/pve/main/icon_pve_main_story.png',
        'label_id': 389,
        'tag_name': 'story'
        },
     {'cls_name': 'PVEWeekTaskWidgetUI',
        'module_path': 'logic.comsys.battle.pve.PVEMainUIWidgetUI',
        'icon': 'gui/ui_res_2/pve/main/icon_pve_main_task.png',
        'label_id': 80841,
        'tag_name': 'task',
        'jump_func': 'jump_to_pve_task'
        },
     {'cls_name': 'ActivityPVEScoreRank',
        'module_path': 'logic.comsys.activity.Activity202404',
        'icon': 'gui/ui_res_2/pve/main/icon_pve_main_activity.png',
        'label_id': 80914,
        'tag_name': 'score_rank',
        'jump_func': 'jump_to_pve_score_rank_activity',
        'show_func': 'is_show_pve_score_rank_activity'
        }]

    @staticmethod
    def get_active_STATIC_LEFT_BTN_UI_CONFIG():
        left_ui_config = []
        for ui_config in PVEMainUI.STATIC_LEFT_UI_CONFIG:
            show_func = ui_config.get('show_func')
            if not show_func:
                left_ui_config.append(ui_config)
                continue
            show_func = getattr(PVEMainUI, show_func)
            if show_func and callable(show_func):
                if show_func():
                    left_ui_config.append(ui_config)

        return left_ui_config

    @staticmethod
    def get_STATIC_LEFT_BTN_CLS--- This code section failed: ---

 197       0  LOAD_GLOBAL           0  'PVEMainUI'
           3  LOAD_ATTR             1  'STATIC_LEFT_BTN_CLS'
           6  POP_JUMP_IF_TRUE     57  'to 57'

 198       9  BUILD_LIST_0          0 
          12  LOAD_GLOBAL           0  'PVEMainUI'
          15  LOAD_ATTR             2  'get_active_STATIC_LEFT_BTN_UI_CONFIG'
          18  CALL_FUNCTION_0       0 
          21  GET_ITER         
          22  FOR_ITER             23  'to 48'
          25  STORE_FAST            0  'config'
          28  LOAD_GLOBAL           3  'get_cls'
          31  LOAD_GLOBAL           1  'STATIC_LEFT_BTN_CLS'
          34  BINARY_SUBSCR    
          35  BINARY_SUBSCR    
          36  BINARY_SUBSCR    
          37  BINARY_SUBSCR    
          38  BINARY_SUBSCR    
          39  CALL_FUNCTION_2       2 
          42  LIST_APPEND           2  ''
          45  JUMP_BACK            22  'to 22'
          48  LOAD_GLOBAL           0  'PVEMainUI'
          51  STORE_ATTR            1  'STATIC_LEFT_BTN_CLS'
          54  JUMP_FORWARD          0  'to 57'
        57_0  COME_FROM                '54'

 199      57  LOAD_GLOBAL           0  'PVEMainUI'
          60  LOAD_ATTR             1  'STATIC_LEFT_BTN_CLS'
          63  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 35

    def on_init_panel(self, need_play_video=False, *args, **kwargs):
        super(PVEMainUI, self).on_init_panel()
        if global_data.player:
            global_data.player.check_pve_selected_mecha_is_available()
        self.init_params()
        self.init_ui()
        self.init_ui_events()
        if need_play_video:
            self.hide()
        else:
            self.init_show_panel()
        global_data.refresh_pve_settle_tag = False
        global_data.enter_pve_with_archive = False

    def init_show_panel(self):
        global_data.emgr.on_open_pve_main_ui.emit()
        self.hide_main_ui(exceptions=['MainChat'], exception_types=(UI_TYPE_MESSAGE,))
        self.show()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_player_item_update_event
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self):
        self._disappearing = False
        self.cur_model = None
        self.cur_model_id = None
        self.cur_shiny_weapon_id = None
        self.cur_choosen_pet = None
        self.normal_position = [-7, 0, 0]
        self._price_top_widget = None
        self._pve_left_top_widget = None
        self._pve_left_button_widget = None
        self._cur_show_ui_name_list = []
        self.tag_btn_dict = {}
        self._nd_touch_IDs = []
        self._total_drag = 0.0
        self._is_init = True
        return

    def init_ui(self):
        self.init_widget_ui()
        self.init_left_btns()
        self.init_select_level_tab()

    def init_widget_ui(self):
        for idx, ui_config in enumerate(PVEMainUI.STATIC_WIDGET_UI_DATA):
            tag = ui_config['tag_name']
            ui_data = PVEMainUI.STATIC_WIDGET_UI_DATA[idx]
            ui_item = getattr(self.panel, ui_data.get('ui_item_name'))
            anim_name = ui_data.get('anim_name')
            if anim_name:
                ui_item.PlayAnimation(anim_name)
            tag_btn = ui_item.btn_tab
            ui_cls = get_cls(ui_data['cls_name'], ui_data['module_path'])
            self.tag_btn_dict[tag] = [tag_btn, ui_cls]

            @tag_btn.unique_callback()
            def OnClick(_btn, _touch, _idx=idx, *args):
                self.on_click_temp_btn(_idx)

        self._pve_left_top_widget = PVELeftTopWidget(self, self.panel)
        self._pve_left_button_widget = PVELeftButtonWidget(self, self.panel)

    def on_click_temp_btn(self, index):
        ui_data = PVEMainUI.STATIC_WIDGET_UI_DATA[index]
        self._on_click_btn(ui_data)

    def init_left_btns(self):
        ui_config = PVEMainUI.get_active_STATIC_LEFT_BTN_UI_CONFIG()
        self.panel.list_btn_left.SetInitCount(len(ui_config))
        for index, item in enumerate(self.panel.list_btn_left.GetAllItem()):
            data = ui_config[index]
            item.icon.SetDisplayFrameByPath('', data['icon'])
            item.lab_btn.setString(get_text_by_id(data['label_id']))
            tag_btn = item.btn

            @tag_btn.unique_callback()
            def OnClick(_btn, _touch, _idx=index):
                ui_data = ui_config[_idx]
                self._on_click_btn(ui_data)

        @self.panel.btn_arrow.unique_callback()
        def OnClick(btn, touch):
            if self.is_playing_show_list_ani:
                return
            self._is_playing_select_anim = True
            self.left_btn_ani = 'show_list' if self.left_btn_ani == 'hide_list' else 'hide_list'
            self.panel.PlayAnimation(self.left_btn_ani)
            max_time = self.panel.GetAnimationMaxRunTime(self.left_btn_ani)
            self.panel.DelayCall(max_time, self._playing_left_btn_anim_end)

    def _on_click_btn(self, ui_data):
        if ui_data.get('jump_func'):
            jump_func = getattr(self, ui_data['jump_func'])
            if jump_func and callable(jump_func):
                jump_func()
                return
        if not ui_data.get('is_open', True):
            global_data.game_mgr.show_tip(get_text_by_id(391))
            return
        ui_cls = get_cls(ui_data['cls_name'], ui_data['module_path'])
        self.play_disappear_anim(ui_cls)
        normal_position = ui_data.get('normal_position')
        if normal_position:
            update_model_and_cam_pos(normal_position, normal_position)
            self.normal_position = normal_position

    def _playing_left_btn_anim_end(self):
        self.is_playing_show_list_ani = False
        rotation = 180 if self.left_btn_ani == 'hide_list' else 0
        self.panel and self.panel.icon_arrow.setRotation(rotation)

    def _reset_left_btn_ani(self):
        DEFAULT_ANI = 'show_list'
        self.left_btn_ani = DEFAULT_ANI
        self.panel.FastForwardToAnimationTime(DEFAULT_ANI, self.panel.GetAnimationMaxRunTime(DEFAULT_ANI))
        self._playing_left_btn_anim_end()

    def _update_left_btn_contant_size(self):
        if self.is_in_team():
            self.nd_left_mid.SetPosition(0, '50%-121')
            self.list_btn_left.SetContentSize(90, 'i480')
        else:
            self.nd_left_mid.SetPosition(0, '50%-1')
            self.list_btn_left.SetContentSize(90, 'i352')

    def play_disappear_anim(self, ui_cls):
        if self._disappearing:
            return
        if not ui_cls:
            return
        ui = ui_cls()
        ui.hide()
        self._cur_show_ui_name_list.append(ui.get_name())
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disapper')

        def delay_call(*args):
            self._disappearing = False
            if hasattr(ui, 'play_anim'):
                ui.play_anim()
            else:
                ui.show()

        self.panel.StopAnimation('disapper')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disapper')

    def init_money_widget--- This code section failed: ---

 370       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_price_top_widget'
           6  POP_JUMP_IF_TRUE     64  'to 64'

 371       9  LOAD_GLOBAL           1  'PriceUIWidget'
          12  LOAD_GLOBAL           1  'PriceUIWidget'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'list_money'
          24  LOAD_CONST            2  'pnl_title'
          27  LOAD_GLOBAL           4  'False'
          30  CALL_FUNCTION_513   513 
          33  LOAD_FAST             0  'self'
          36  STORE_ATTR            0  '_price_top_widget'

 372      39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             0  '_price_top_widget'
          45  LOAD_ATTR             5  'show_money_types'
          48  LOAD_GLOBAL           6  'SHOP_PAYMENT_ITEM_PVE_KEY'
          51  LOAD_GLOBAL           7  'SHOP_PAYMENT_ITEM_PVE_COIN'
          54  BUILD_LIST_2          2 
          57  CALL_FUNCTION_1       1 
          60  POP_TOP          
          61  JUMP_FORWARD         13  'to 77'

 374      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             0  '_price_top_widget'
          70  LOAD_ATTR             8  '_on_player_info_update'
          73  CALL_FUNCTION_0       0 
          76  POP_TOP          
        77_0  COME_FROM                '61'

Parse error at or near `CALL_FUNCTION_513' instruction at offset 30

    def init_ui_events(self):

        @self.panel.nd_mech_touch.unique_callback()
        def OnBegin(layer, touch):
            if len(self._nd_touch_IDs) > 1:
                return False
            tid = touch.getId()
            if tid not in self._nd_touch_IDs:
                self._nd_touch_IDs.append(tid)
            self._total_drag = 0.0
            return True

        @self.panel.nd_mech_click.unique_callback()
        def OnClick(layer, touch):
            if self._total_drag >= MAX_MECHA_CLICK_DIST:
                return
            ui_data = PVEMainUI.STATIC_WIDGET_UI_DATA[1]
            ui_cls = get_cls(ui_data['cls_name'], ui_data['module_path'])
            self.play_disappear_anim(ui_cls)

        @self.panel.nd_mech_touch.unique_callback()
        def OnDrag(layer, touch):
            tid = touch.getId()
            if tid not in self._nd_touch_IDs:
                return
            if len(self._nd_touch_IDs) == 1:
                delta_pos = touch.getDelta()
                global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)
            self._total_drag += abs(touch.getDelta().x) + abs(touch.getDelta().y)

        @self.panel.nd_mech_touch.unique_callback()
        def OnEnd(layer, touch):
            tid = touch.getId()
            if tid in self._nd_touch_IDs:
                self._nd_touch_IDs.remove(tid)

    def ui_vkb_custom_func(self, *args):
        if self.panel.IsVisible() and not self._disappearing:
            from common.cinematic.VideoPlayer import VideoPlayer
            from logic.gcommon.common_const.pve_const import PVE_MAIN_UI_LEAVE_RES
            VideoPlayer().play_video(PVE_MAIN_UI_LEAVE_RES, lambda : self.close(), repeat_time=1, can_jump=False)
            return True
        return False

    def on_resolution_changed(self):
        super(PVEMainUI, self).on_resolution_changed()
        global_data.emgr.on_open_pve_main_ui.emit()

    def do_show_panel(self):
        super(PVEMainUI, self).do_show_panel()
        self.process_events(True)
        self.normal_position = [-7, 0, 0]
        self._update_panel()
        self.init_model()
        ui = global_data.ui_mgr.get_ui('MainChat')
        if ui:
            ui.clear_show_count_dict()
            ui.show()
        else:
            global_data.ui_mgr.show_ui('MainChat', 'logic.comsys.chat')

    def do_hide_panel(self):
        super(PVEMainUI, self).do_hide_panel()
        self.process_events(False)

    def on_player_item_update_event(self):
        self.init_money_widget()

    def _update_panel(self):
        self.do_switch_scene()
        self._play_animation()
        self._update_panel_info()

    def _play_animation(self):
        if self._is_init:
            self.panel.PlayAnimation('appear_full')
            self._is_init = False
        else:
            self.panel.PlayAnimation('apper')

    def _update_panel_info(self):
        global_data.player and global_data.player.request_unreceived_story_debris()
        self.init_money_widget()
        self.init_select_level_tab()
        self.check_show_red_point()
        self.init_story_debris_tab()
        self._reset_left_btn_ani()
        self.check_show_left_red_point()

    def do_switch_scene(self):

        def on_load_scene(*args):
            if self.cur_model:
                return
            camera_ctrl = global_data.game_mgr.scene.get_com('PartModelDisplayCamera')
            if not camera_ctrl:
                return
            self.init_model()

        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_PVE_MAIN_UI, PVE_MAIN_UI, finish_callback=on_load_scene, update_cam_at_once=self._is_init, belong_ui_name='PVEMainUI')

    def init_model(self, *args):
        pve_mecha_id = global_data.player.get_pve_selected_mecha_item_id() if global_data.player else None
        model_id = global_data.player.get_pve_using_mecha_skin(pve_mecha_id) if global_data.player else DEFAULT_CLOTHING_ID
        choosen_pet = global_data.player.pve_choosen_pet if global_data.player else None
        shiny_weapon_id = self.get_shiny_weapon_id(model_id)
        self._update_model(model_id, choosen_pet=choosen_pet, shiny_weapon_id=shiny_weapon_id)
        return

    def _update_model(self, model_id, choosen_pet, model_pos=None, shiny_weapon_id=None):
        if not global_data.ui_mgr.get_ui('PVEMainUI'):
            return
        if not model_pos:
            model_pos = self.normal_position
        if self.cur_model_id == model_id and self.cur_shiny_weapon_id == shiny_weapon_id and self.cur_choosen_pet == choosen_pet:
            return

        def on_load_model(model):
            global_data.emgr.reset_rotate_model_display.emit()
            self.cur_model = model
            self.cur_model_id = model_id
            self.cur_shiny_weapon_id = shiny_weapon_id
            global_data.emgr.on_pve_main_model_load_complete.emit(self.cur_model_id)

        item_type = get_lobby_item_type(model_id)
        b_show_model = item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN)
        if b_show_model and item_type == L_ITEM_TYPE_MECHA_SKIN:
            model_data = get_lobby_model_data(model_id, is_get_player_data=False, consider_second_model=False)
            mecha_scale = 1.0
            for data in model_data:
                mecha_scale = data['model_scale']
                data['decal_list'] = global_data.player.get_mecha_decal().get(str(get_main_skin_id(model_id)), []) if global_data.player else []
                data['color_dict'] = global_data.player.get_mecha_color().get(str(model_id), {}) if global_data.player else {}
                data['off_position'] = model_pos
                data['show_anim_ban_rotate'] = False
                if shiny_weapon_id:
                    data['shiny_weapon_id'] = shiny_weapon_id

            pet_level = 1
            pet_item = global_data.player.get_item_by_no(choosen_pet)
            if pet_item:
                pet_level = pet_item.level
            self.cur_choosen_pet = choosen_pet
            if choosen_pet:
                pet_scale = mecha_scale * confmgr.get('c_pet_info', str(choosen_pet), 'mecha_scale', default=1.0)
                pet_model_data = get_lobby_model_data(choosen_pet, pet_level=pet_level, is_get_player_data=False, consider_second_model=False)
                for data in pet_model_data:
                    data['off_position'] = model_pos
                    data['model_scale'] = pet_scale
                    data['follow_center_pos'] = (-10 / pet_scale, -20 / pet_scale, 0)
                    data['show_anim_ban_rotate'] = False
                    data['ignore_shadow_down_offset'] = True

                model_data.extend(pet_model_data)
            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_load_model)

    def on_pve_mecha_changed(self, mecha_id):
        pve_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
        model_id = global_data.player.get_pve_using_mecha_skin(pve_mecha_id) if global_data.player else DEFAULT_CLOTHING_ID
        shiny_weapon_id = self.get_shiny_weapon_id(model_id)
        self.on_pve_mecha_skin_changed(model_id, shiny_weapon_id)

    def on_pve_mecha_skin_changed(self, model_id, shiny_weapon_id=None):
        if self.cur_model_id == model_id and self.cur_shiny_weapon_id == shiny_weapon_id:
            return
        part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
        if not part_md:
            return
        model_list = part_md.get_cur_model_list()
        model_pos = self.normal_position
        if model_list:
            lobby_model = model_list[0]
            if lobby_model:
                if lobby_model.last_model_pos != lobby_model.model_pos:
                    model_pos = [lobby_model.model_pos.x, lobby_model.model_pos.y, lobby_model.model_pos.z]
                else:
                    ref_model = lobby_model.get_model()
                    if ref_model:
                        model_pos = [
                         ref_model.position.x, ref_model.position.y, ref_model.position.z]
        self._update_model(model_id, self.cur_choosen_pet, model_pos, shiny_weapon_id)

    def update_shiny_weapon(self, *args):
        model_data = get_lobby_model_data(self.cur_model_id, consider_second_model=False)
        shiny_weapon_id = None
        if model_data and model_data[0]:
            shiny_weapon_id = model_data[0].get('shiny_weapon_id')
        if self.cur_shiny_weapon_id != shiny_weapon_id:
            self.on_pve_mecha_skin_changed(self.cur_model_id, shiny_weapon_id)
        return

    def get_shiny_weapon_id(self, model_id):
        shiny_weapon_id = None
        model_data = get_lobby_model_data(model_id, consider_second_model=False)
        if model_data and model_data[0]:
            shiny_weapon_id = model_data[0].get('shiny_weapon_id')
        return shiny_weapon_id

    def update_model_and_cam_pos(self, *args):
        update_model_and_cam_pos(self.normal_position, self.normal_position)

    def init_select_level_tab(self):
        cur_chapter = global_data.player.get_last_pve_chapter() if global_data.player else 1
        cur_difficulty = global_data.player.get_last_pve_difficulty() if global_data.player else NORMAL_DIFFICUTY
        self.update_select_level_tab(cur_chapter, cur_difficulty)
        self.update_teammate_state()

    def update_select_level_tab(self, chapter, difficulty):
        conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
        btn_tab = self.panel.temp_tab_1.btn_tab
        btn_tab.lab_title.setString('{} {}'.format(get_text_by_id(conf.get('title_text')), get_text_by_id(conf.get('sub_title_text'))))
        icon_pic_list = conf.get('icon')
        icon_pic = icon_pic_list[difficulty - 1]
        btn_tab.frame_pic.nd_cut.img_pic.SetDisplayFrameByPath('', icon_pic)

    def is_in_team(self):
        return global_data.enable_pve_team and global_data.player.is_in_team()

    def update_teammate_state(self, *args):
        if not global_data.player:
            return
        lab_fight = self.panel.temp_tab_1.btn_tab.lab_fight
        if self.is_in_team():
            lab_fight.setString(get_text_by_id(498))
        else:
            lab_fight.setString(get_text_by_id(499))
        self._update_left_btn_contant_size()
        self.on_pve_battle_info_change_event()

    def on_pve_battle_info_change_event(self, *args):
        if not global_data.player:
            return
        cur_chapter = global_data.player.get_last_pve_chapter()
        cur_difficulty = global_data.player.get_last_pve_difficulty()
        if global_data.enable_pve_team and global_data.player.is_in_team():
            pve_battle_info = global_data.player.get_pve_battle_info()
            if pve_battle_info:
                cur_chapter = pve_battle_info.get('chapter')
                cur_difficulty = pve_battle_info.get('difficulty')
        self.update_select_level_tab(cur_chapter, cur_difficulty)

    def init_story_debris_tab(self):
        btn_tab = self.panel.temp_tab_6.btn_tab
        cur_chapter = global_data.player.get_last_pve_chapter() if global_data.player else 1
        chapter_debris_conf = confmgr.get('story_debris_chapter_data')
        debris_clue_conf = confmgr.get('story_debris_clue_data')
        chapter_debris_conf = chapter_debris_conf.get(str(cur_chapter), {})
        clue_list = chapter_debris_conf.get('clue', [])
        finish_debris_count = 0
        all_debris_count = 0
        for clue_id in clue_list:
            clue_conf = debris_clue_conf.get(str(clue_id))
            debris_list = clue_conf.get('debris', [])
            for debris_no in debris_list:
                all_debris_count += 1
                has_item = bool(global_data.player.get_item_by_no(debris_no)) if global_data.player else False
                if has_item:
                    finish_debris_count += 1

        all_debris_color = FINISH_ALL_DEBRIS_COLOR if finish_debris_count == all_debris_count else NORMAL_ALL_DEBRIS_COLOR
        debris_str = CURRENT_DEBRIS_COLOR.format(finish_debris_count)
        all_debris_str = all_debris_color.format(all_debris_count)
        btn_tab.lab_prog.setString('{}{}'.format(debris_str, all_debris_str))

    def jump_to_pve_task(self):
        from logic.gutils.jump_to_ui_utils import jump_to_task_ui
        from logic.gcommon.common_const.task_const import TASK_TYPE_WEEKLY_PVE
        jump_to_task_ui(TASK_TYPE_WEEKLY_PVE)

    def jump_to_pve_score_rank_activity(self):
        from logic.gutils.jump_to_ui_utils import jump_to_activity
        from logic.gcommon.common_const.activity_const import ACTIVITY_PVE_SCORE_RANK
        jump_to_activity(ACTIVITY_PVE_SCORE_RANK)

    @staticmethod
    def is_show_pve_score_rank_activity():
        from logic.gutils.activity_utils import is_activity_in_limit_time
        from logic.gcommon.common_const.activity_const import ACTIVITY_PVE_SCORE_RANK
        return is_activity_in_limit_time(ACTIVITY_PVE_SCORE_RANK)

    def check_show_red_point(self):
        for tag, info in six_ex.items(self.tag_btn_dict):
            btn = info[0]
            ui_cls = info[1]
            if ui_cls.check_red_point():
                btn.temp_red.setVisible(ui_cls.check_red_point())
            else:
                btn.temp_red.setVisible(False)

    def check_show_left_red_point(self):
        cls_list = PVEMainUI.get_STATIC_LEFT_BTN_CLS()
        for index, item in enumerate(self.panel.list_btn_left.GetAllItem()):
            ui_cls = cls_list[index]
            if hasattr(ui_cls, 'check_red_point') and ui_cls.check_red_point():
                item.temp_red.setVisible(ui_cls.check_red_point())
            else:
                item.temp_red.setVisible(False)

    @staticmethod
    def check_red_point--- This code section failed: ---

 731       0  LOAD_GLOBAL           0  'PVEMainUI'
           3  LOAD_ATTR             1  'STATIC_TABLE_BTN_CLS'
           6  POP_JUMP_IF_TRUE     54  'to 54'

 732       9  BUILD_LIST_0          0 
          12  LOAD_GLOBAL           0  'PVEMainUI'
          15  LOAD_ATTR             2  'STATIC_WIDGET_UI_DATA'
          18  GET_ITER         
          19  FOR_ITER             23  'to 45'
          22  STORE_FAST            0  'config'
          25  LOAD_GLOBAL           3  'get_cls'
          28  LOAD_GLOBAL           1  'STATIC_TABLE_BTN_CLS'
          31  BINARY_SUBSCR    
          32  BINARY_SUBSCR    
          33  BINARY_SUBSCR    
          34  BINARY_SUBSCR    
          35  BINARY_SUBSCR    
          36  CALL_FUNCTION_2       2 
          39  LIST_APPEND           2  ''
          42  JUMP_BACK            19  'to 19'
          45  LOAD_GLOBAL           0  'PVEMainUI'
          48  STORE_ATTR            1  'STATIC_TABLE_BTN_CLS'
          51  JUMP_FORWARD          0  'to 54'
        54_0  COME_FROM                '51'

 733      54  SETUP_LOOP           33  'to 90'
          57  LOAD_GLOBAL           0  'PVEMainUI'
          60  LOAD_ATTR             1  'STATIC_TABLE_BTN_CLS'
          63  GET_ITER         
          64  FOR_ITER             22  'to 89'
          67  STORE_FAST            1  'ui_cls'

 734      70  LOAD_FAST             1  'ui_cls'
          73  LOAD_ATTR             4  'check_red_point'
          76  CALL_FUNCTION_0       0 
          79  POP_JUMP_IF_FALSE    64  'to 64'

 735      82  LOAD_GLOBAL           5  'True'
          85  RETURN_END_IF    
        86_0  COME_FROM                '79'
          86  JUMP_BACK            64  'to 64'
          89  POP_BLOCK        
        90_0  COME_FROM                '54'

 738      90  LOAD_GLOBAL           0  'PVEMainUI'
          93  LOAD_ATTR             6  'get_STATIC_LEFT_BTN_CLS'
          96  CALL_FUNCTION_0       0 
          99  STORE_FAST            2  'cls_list'

 739     102  SETUP_LOOP           45  'to 150'
         105  LOAD_FAST             2  'cls_list'
         108  GET_ITER         
         109  FOR_ITER             37  'to 149'
         112  STORE_FAST            1  'ui_cls'

 740     115  LOAD_GLOBAL           7  'hasattr'
         118  LOAD_FAST             1  'ui_cls'
         121  LOAD_CONST            3  'check_red_point'
         124  CALL_FUNCTION_2       2 
         127  POP_JUMP_IF_FALSE   109  'to 109'
         130  LOAD_FAST             1  'ui_cls'
         133  LOAD_ATTR             4  'check_red_point'
         136  CALL_FUNCTION_0       0 
       139_0  COME_FROM                '127'
         139  POP_JUMP_IF_FALSE   109  'to 109'

 741     142  LOAD_GLOBAL           5  'True'
         145  RETURN_END_IF    
       146_0  COME_FROM                '139'
         146  JUMP_BACK           109  'to 109'
         149  POP_BLOCK        
       150_0  COME_FROM                '102'

 742     150  LOAD_GLOBAL           8  'False'
         153  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 32

    def on_finalize_panel(self):
        self.process_events(False)
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        if self._pve_left_top_widget:
            self._pve_left_top_widget.destroy()
            self._pve_left_top_widget = None
        if self._pve_left_button_widget:
            self._pve_left_button_widget.destroy()
            self._pve_left_button_widget = None
        self._disappearing = None
        self.cur_model = None
        self.cur_model_id = None
        self.cur_shiny_weapon_id = None
        self.tag_btn_dict = {}
        self._nd_touch_IDs = []
        self._total_drag = 0.0
        self._is_init = True
        for ui_name in self._cur_show_ui_name_list:
            global_data.ui_mgr.close_ui(ui_name)

        self._cur_show_ui_name_list = []
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.on_close_pve_main_ui.emit()
        self.show_main_ui()
        super(PVEMainUI, self).on_finalize_panel()
        return