# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SoundVisibleUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import BASE_LAYER_ZORDER_1
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero
import logic.gcommon.const as const
import common.utilities
import math
import game3d
import world
import time
from collections import defaultdict
from common.cfg import confmgr
import math3d
from logic.client.const import camera_const
from logic.client.const.game_mode_const import GAME_MODE_NIGHT_SURVIVAL
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from logic.gcommon.common_const import attr_const
r45 = math.pi / 4.0
R_A_RATE = 180 / math.pi
SOUND_TYPE_FOOTSTEP = const.SOUND_TYPE_FOOTSTEP
SOUND_TYPE_FIRE = const.SOUND_TYPE_FIRE
SOUND_TYPE_CAR = const.SOUND_TYPE_CAR
SOUND_TYPE_SLOW_FOOTSTEP = const.SOUND_TYPE_SLOW_FOOTSTEP
SOUND_TYPE_SILENCER_FIRE = const.SOUND_TYPE_SILENCER_FIRE
SOUND_TYPE_MECHA_FIRE = const.SOUND_TYPE_MECHA_FIRE
SOUND_TYPE_MECHA_FOOTSTEP = const.SOUND_TYPE_MECHA_FOOTSTEP
ITEM_STATE_HIDE = 0
ITEM_STATE_SHOW = 1
ITEM_STATE_FADE = 2
SHOW_LAST_TIME = 1500
ITEM_CACHE_MAX_COUNT = 3
from common.const import uiconst

class SoundVisibleUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/sound_main'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.visible_dis = []
        self.visible_opacity = []
        self.visible_weight = []
        self.visible_pic = []
        self.human_visible_dis = []
        self.mecha_visible_dis = []
        self.ace_human_visible_dis = []
        self.ace_mecha_visible_dis = []
        global_sound_visible_rate = 0.6 if CGameModeManager().get_mode_type() == GAME_MODE_NIGHT_SURVIVAL else 1
        dis_inf = (
         (
          'human_visible_dis', self.human_visible_dis), ('mecha_visible_dis', self.mecha_visible_dis), ('ace_human_visible_dis', self.ace_human_visible_dis), ('ace_mecha_visible_dis', self.ace_mecha_visible_dis))
        for index in range(const.SOUND_TYPE_MAX_COUNT):
            data = confmgr.get('sound_visible_conf', str(index))
            for key, visible_dis in dis_inf:
                dis_data = []
                for dis in data[key]:
                    dis_data.append((dis * const.NEOX_UNIT_SCALE * global_sound_visible_rate) ** 2)

                visible_dis.append(dis_data)

            self.visible_opacity.append(data['visible_opacity'])
            self.visible_weight.append(data['visible_weight'])
            self.visible_pic.append(data['visible_icon'])

        self.visible_dis = self.human_visible_dis
        conf = confmgr.get('sound_visible_const')
        self.max_visible_item_count = conf['max_visible_item_count']
        self.visible_item_min_angle = conf['visible_item_min_angle']
        self._show_entity = {}
        self._panel_items = []
        item_conf = global_data.uisystem.load_template('battle/sound_item')
        for index in range(self.max_visible_item_count):
            item = global_data.uisystem.create_item(item_conf, parent=self.panel)
            item.setAnchorPoint(ccp(0.5, 0))
            self._panel_items.append(item)

        for item in self._panel_items:
            item.SetEnableCascadeOpacityRecursion(True)
            item.setVisible(False)
            item.entity = None
            item.sound_type = 0
            item.action_time = 0

        self.enable = True
        from logic.gcommon.common_const.ui_operation_const import SOUND_VISIBLE_3D_KEY
        self.is_open_sound_visible3d = global_data.player.get_setting(SOUND_VISIBLE_3D_KEY)
        self.sound_mgr = global_data.sound_mgr
        self._scene = world.get_active_scene()
        self._player = None
        self.enable_player_or_mecha = None
        self._is_in_mecha = False
        self._is_ace_time = False
        if self._scene:
            self.player_change(self._scene.get_player())
        self._is_run = True
        self._end_action_item = self.panel.itemtemp
        self._end_action_item.SetEnableCascadeOpacityRecursion(True)
        self._end_action_item.setVisible(False)
        self._add_entity = []
        self._is_remove_old_entity = False
        self._time_index = 0
        self._is_in_aim = False
        self.init_event()
        return

    def on_finalize_panel(self):
        global_data.emgr.sound_visible_add -= self.on_add_visible_elem
        global_data.emgr.camera_transformation_change -= self.on_camera
        global_data.emgr.scene_player_setted_event -= self.on_player_setted
        global_data.emgr.scene_observed_player_setted_event -= self.on_enter_observe
        global_data.emgr.scene_sound_visible -= self.setEnable
        global_data.emgr.scene_hide_sound_visible -= self.set_hide
        global_data.emgr.player_open_sound_visible3d -= self.on_open_sound_visible3d
        global_data.emgr.camera_switch_to_state_event -= self.on_camera_state
        global_data.emgr.battle_into_ace_stage_event -= self.change_visible_dis
        self._is_run = False

    def init_event(self):
        global_data.emgr.scene_hide_sound_visible += self.set_hide
        global_data.emgr.scene_sound_visible += self.setEnable
        global_data.emgr.sound_visible_add += self.on_add_visible_elem
        global_data.emgr.camera_transformation_change += self.on_camera
        global_data.emgr.scene_player_setted_event += self.on_player_setted
        global_data.emgr.scene_observed_player_setted_event += self.on_enter_observe
        global_data.emgr.player_open_sound_visible3d += self.on_open_sound_visible3d
        global_data.emgr.camera_switch_to_state_event += self.on_camera_state
        global_data.emgr.battle_into_ace_stage_event += self.change_visible_dis

    def on_open_sound_visible3d(self, *args):
        from logic.gcommon.common_const.ui_operation_const import SOUND_VISIBLE_3D_KEY
        self.is_open_sound_visible3d = global_data.player.get_setting(SOUND_VISIBLE_3D_KEY)

    def change_visible_dis(self):
        self._is_in_mecha = self._player and self._player.ev_g_in_mecha()
        self._is_ace_time = global_data.battle and global_data.battle.is_ace_time()
        if self._is_ace_time:
            self.visible_dis = self.ace_mecha_visible_dis if self._is_in_mecha else self.ace_human_visible_dis
        else:
            self.visible_dis = self.mecha_visible_dis if self._is_in_mecha else self.human_visible_dis

    def on_player_setted(self, player):
        self.player_change(player)

    def on_enter_observe(self, lplayer):
        self.player_change(lplayer)

    def player_change(self, lplayer):
        if self._player:
            self._player.unregist_event('E_ON_JOIN_MECHA', self.on_control_target_change)
            self._player.unregist_event('E_ON_LEAVE_MECHA', self.on_control_target_change)
        self._player = lplayer
        if not self._player:
            for item in self._panel_items:
                item.setVisible(False)

        else:
            self._player.regist_event('E_ON_JOIN_MECHA', self.on_control_target_change)
            self._player.regist_event('E_ON_LEAVE_MECHA', self.on_control_target_change)
            self.on_control_target_change()

    def on_control_target_change(self, *args):
        self._is_in_mecha = self._player.ev_g_in_mecha()
        self.change_visible_dis()
        self.enable_player_or_mecha = self._player.ev_g_control_target().logic if self._is_in_mecha else self._player

    def del_visible_elem(self, entity, sound_type, time_index):
        if entity in self._show_entity:
            entity_inf = self._show_entity[entity]
            if entity_inf['time_index'] > time_index:
                return
            type_dic = entity_inf['type_dic']
            type_dic[sound_type] -= 1
            if not self.is_elment_enable(type_dic):
                del self._show_entity[entity]
                self._is_remove_old_entity = True
            if type_dic[sound_type] <= 0 and self._is_run:
                self.refresh_visible()

    def del_visible_elem_ex(self, entity):
        if entity in self._show_entity:
            del self._show_entity[entity]
            self._is_remove_old_entity = True

    def on_add_visible_elem(self, entity, pos, sound_type, distance_sqr, driver_id=None):
        if self.is_open_sound_visible3d and not self._is_in_aim:
            return
        if not global_data.cam_lplayer or not self.enable:
            return
        listen_factor = global_data.cam_lplayer.ev_g_add_attr(attr_const.ATTR_LISTEN_RANGE_FACTOR)
        listen_dis = self.visible_dis[sound_type][-1] * (1 + listen_factor) ** 2
        if distance_sqr > listen_dis:
            return
        if global_data.cam_lplayer.ev_g_is_campmate(entity.ev_g_camp_id()):
            return
        if self._is_in_mecha and not self._is_ace_time and (sound_type == SOUND_TYPE_FOOTSTEP or sound_type == SOUND_TYPE_SLOW_FOOTSTEP):
            return
        if not self.enable_player_or_mecha:
            return
        is_refresh = False
        player_pos = self.enable_player_or_mecha.ev_g_model_position()
        if not player_pos:
            return
        length_sqr = (pos - player_pos).length_sqr
        weight = self.get_weight(sound_type, length_sqr)
        if entity not in self._show_entity:
            if len(self._show_entity) > self.max_visible_item_count:
                min_entity, min_weight = self.get_min_weight_entity()
                if weight < min_weight:
                    return
                del self._show_entity[min_entity]
                self._is_remove_old_entity = True
            self._show_entity[entity] = {'pos': pos,'weight': weight,'length_sqr': length_sqr,'type_dic': defaultdict(int),'time_index': self._time_index}
            is_refresh = True
            self._add_entity.append(entity)
            if sound_type == SOUND_TYPE_FOOTSTEP or sound_type == SOUND_TYPE_SLOW_FOOTSTEP:
                global_data.emgr.play_tips_voice.emit('enemy_nearby', entity_id=entity.id)
            elif sound_type == SOUND_TYPE_MECHA_FOOTSTEP:
                global_data.emgr.play_tips_voice.emit('tips_03', entity_id=entity.id)
            elif sound_type == SOUND_TYPE_FIRE or sound_type == SOUND_TYPE_MECHA_FIRE:
                global_data.emgr.play_tips_voice.emit('tips_04', entity_id=entity.id)
        entity_inf = self._show_entity[entity]
        if entity_inf['pos'] != pos:
            entity_inf['pos'] = pos
            is_refresh = True
        type_dic = entity_inf['type_dic']
        if type_dic[sound_type] == 0:
            is_refresh = True
        elif type_dic[sound_type] >= ITEM_CACHE_MAX_COUNT:
            return
        type_dic[sound_type] += 1
        if entity_inf['length_sqr'] != length_sqr:
            entity_inf['length_sqr'] = length_sqr
            is_refresh = True
        if sound_type == SOUND_TYPE_FIRE or sound_type == SOUND_TYPE_SILENCER_FIRE:
            entity_inf['action'] = True
            is_refresh = True
        else:
            entity_inf['action'] = False
        game3d.delay_exec(SHOW_LAST_TIME, self.del_visible_elem, (entity, sound_type, self._time_index))
        if is_refresh:
            self.refresh_visible()
        self._time_index += 1

    def get_min_weight_entity(self):
        min_entity = None
        min_weight = 0
        for entity, entity_inf in six.iteritems(self._show_entity):
            if min_entity == None:
                min_entity = entity
                min_weight = entity_inf['weight']
            elif min_weight > entity_inf['weight']:
                min_entity = entity
                min_weight = entity_inf['weight']

        return (
         min_entity, min_weight)

    def get_weight(self, sound_type, length_sqr):
        weight_rate = self.visible_weight[sound_type]
        if length_sqr == 0.0:
            weight = weight_rate
        else:
            weight = weight_rate / length_sqr
        return weight

    def on_camera(self, *args):
        if self.enable and self._show_entity:
            self.refresh_visible()

    def get_disable_panel_item(self):
        for item in self._panel_items:
            if not item.isVisible():
                return item

        return None

    def refresh_visible(self):
        if not self.enable_player_or_mecha:
            return
        else:
            if self._is_remove_old_entity:
                for item in self._panel_items:
                    if item.isVisible():
                        if item.entity not in self._show_entity:
                            item.setVisible(False)
                            item.entity = None
                            self.play_end_action(item)

                self._is_remove_old_entity = False
            if self._add_entity:
                for entity in self._add_entity:
                    panel_item = self.get_disable_panel_item()
                    if panel_item:
                        panel_item.entity = entity
                        panel_item.setVisible(True)

                self._add_entity = []
            player_pos = self.enable_player_or_mecha.ev_g_model_position()
            if player_pos is None:
                return
            listener_look_at = self.sound_mgr.get_listener_look_at()
            cur_time = time.time()
            save_panel_item_dict = {}
            for panel_item in self._panel_items:
                if panel_item.isVisible():
                    entity = panel_item.entity
                    entity_inf = self._show_entity[entity]
                    vect = entity_inf['pos'] - player_pos
                    entity_length_sqr = vect.length_sqr
                    sound_type = self.get_best_sound_type(entity_inf['type_dic'])
                    panel_item.sound_type = sound_type
                    panel_item.img_sound.SetDisplayFrameByPath('', self.visible_pic[sound_type])
                    angle = common.utilities.vect2d_radian(vect, listener_look_at) * R_A_RATE
                    panel_item.setRotation(angle)
                    opacity_index = 0
                    distance_list = self.visible_dis[sound_type]
                    for i in range(len(distance_list)):
                        listen_factor = global_data.cam_lplayer.ev_g_add_attr(attr_const.ATTR_LISTEN_RANGE_FACTOR)
                        if entity_length_sqr < distance_list[i] * (1 + listen_factor) ** 2:
                            opacity_index = i
                            break
                    else:
                        opacity_index = len(distance_list) - 1

                    opacity = self.visible_opacity[sound_type][opacity_index] * 255 // 100
                    panel_item.setOpacity(opacity)
                    if entity_inf['action'] and cur_time - panel_item.action_time > 1.2:
                        entity_inf['action'] = False
                        panel_item.action_time = cur_time
                    del_flag = True
                    if save_panel_item_dict:
                        del_entity = []
                        del_save_panel_item = []
                        for save_panel_item, save_item_angle in six.iteritems(save_panel_item_dict):
                            if abs(angle - save_item_angle) < self.visible_item_min_angle:
                                if entity_inf['weight'] > self._show_entity[save_panel_item.entity]['weight']:
                                    save_panel_item.setOpacity(0)
                                    save_panel_item.setVisible(False)
                                    del_entity.append(save_panel_item.entity)
                                    del_save_panel_item.append(save_panel_item)
                                else:
                                    panel_item.setOpacity(0)
                                    panel_item.setVisible(False)
                                    del_entity.append(entity)
                                    del_flag = False

                        for entity in del_entity:
                            self.del_visible_elem_ex(entity)

                        for save_panel in del_save_panel_item:
                            if save_panel in save_panel_item_dict:
                                del save_panel_item_dict[save_panel]

                    if del_flag:
                        save_panel_item_dict[panel_item] = angle

            return

    def get_best_sound_type(self, type_dic):
        best_weight = 0
        best_type = 0
        for sound_type, value in six.iteritems(type_dic):
            if value > 0:
                weight = self.visible_weight[sound_type]
                if best_weight == 0:
                    best_weight = weight
                    best_type = sound_type
                elif weight > best_weight:
                    best_weight = weight
                    best_type = sound_type

        return best_type

    def is_elment_enable(self, type_dic):
        for sound_type, value in six.iteritems(type_dic):
            if value > 0:
                return True

        return False

    def play_end_action(self, item):
        opacity = item.getOpacity()
        if opacity == 0:
            return
        action_item = self._end_action_item
        if not self._end_action_item.isVisible():
            action_item.setVisible(True)
            angle = item.getRotation()
            action_item.setRotation(angle)
            act = cc.FadeTo.create(0.3, 0)
            action_item.setOpacity(opacity)
            action_item.runAction(act)
            action_item.img_sound.SetDisplayFrameByPath('', self.visible_pic[item.sound_type])

            def callback():
                action_item.setVisible(False)

            action_item.SetTimeOut(0.35, callback)

    def setEnable(self, flag):
        self.enable = flag

    def set_hide(self, flag):
        self.panel.setVisible(not flag)

    def on_camera_state(self, state, *args):
        self._is_in_aim = state in [camera_const.AIM_MODE, camera_const.RIGHT_AIM_MODE]