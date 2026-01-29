# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainBattleMgr.py
from __future__ import absolute_import
from six.moves import range
import six
from common.utils.timer import CLOCK
import math
import math3d
import world
import collision
from common.framework import Singleton
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_const.collision_const as collision_const
from common.cfg import confmgr
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
from logic.gutils.screen_effect_utils import create_screen_effect_directly
SWIM_UI_LIST = [
 'FireRockerUI', 'PostureControlUI', 'BattleControlUIPC', 'ThrowRockerUI', 'BulletReloadUI']

class TrainAroundChecker(object):

    def __init__(self):
        self._timer_id = None
        play_data = global_data.game_mode.get_cfg_data('play_data')
        self.train_check_range = play_data.get('train_check_range', 30) * NEOX_UNIT_SCALE
        self.train_check_height = play_data.get('train_check_height', 30) * NEOX_UNIT_SCALE
        self.train_check_offset = math3d.vector(*play_data.get('train_check_offset', [0, 0, 0])) * NEOX_UNIT_SCALE
        return

    def init_timer(self):
        self._timer_id = global_data.game_mgr.register_logic_timer(self.check_logic, interval=0.5, times=-1, mode=CLOCK)

    def check_logic(self):
        train_carriage = global_data.train_battle_mgr.get_train_carriage()
        player = global_data.player and global_data.player.logic
        battle = global_data.battle
        if not player or not train_carriage or not battle:
            return
        pos_player = global_data.player.logic.ev_g_position()
        if train_carriage.sd.ref_carriage_pos and pos_player:
            pos_train = train_carriage.sd.ref_carriage_pos + self.train_check_offset
            length = math.sqrt(pow(pos_train.x - pos_player.x, 2) + pow(pos_train.z - pos_player.z, 2))
            if abs(pos_train.y - pos_player.y) <= self.train_check_height / 2.0 and length <= self.train_check_range:
                return True
        return False

    def destroy(self):
        global_data.game_mgr.unregister_logic_timer(self._timer_id)
        self._timer_id = None
        return


class TrainBattleData(DeathBattleData):

    def init_parameters(self):
        super(TrainBattleData, self).init_parameters()
        self.is_revive = False

    def set_is_revive(self, is_revive):
        self.is_revive = is_revive

    def get_is_revive(self):
        return self.is_revive

    def check_pos(self):

        def on_check():
            if global_data.game_mode.mode and global_data.game_mode.mode.game_over:
                return
            if not (global_data.player and global_data.player.logic):
                return
            lpos = global_data.player.logic.ev_g_position()
            if not lpos:
                return
            is_in_base_part = False
            born_range_data = global_data.game_mode.get_cfg_data('born_range_data')
            for idx, range_data in six.iteritems(born_range_data):
                y_range = range_data.get('y_range')
                if lpos.y < y_range[0] or lpos.y > y_range[1]:
                    continue
                pos_lst = range_data.get('pos_lst', [])
                if pnpoly(len(pos_lst), pos_lst, (lpos.x, lpos.z)):
                    is_in_base_part = True

            if is_in_base_part != self.is_in_base_part:
                self.is_in_base_part = is_in_base_part
                global_data.emgr.death_in_base_part_change.emit()
                if is_in_base_part:
                    self.show_swim_ui_list(SWIM_UI_LIST, True)

        self.check_pos_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_pos_timer)
        self.check_pos_timer = global_data.game_mgr.get_logic_timer().register(func=on_check, mode=CLOCK, interval=1)
        global_data.emgr.death_in_base_part_change.emit()


class TrainBattleMgr(Singleton):
    ALIAS_NAME = 'train_battle_mgr'

    def init(self):
        self.init_parameters()
        self.init_station_node()

    def init_parameters(self):
        self.train_checker = None
        self.model_list = []
        self.station_node = {}
        self.station_route_sfx_list = {'1': [],'2': []}
        self.heal_screen_sfx_id = None
        self.damage_screen_sfx_id = None
        self.skill_data = global_data.game_mode.get_cfg_data('train_skill_data')
        self.train_mode_data = global_data.game_mode.get_born_data()[str(global_data.battle.area_id)]
        rail_data = confmgr.get('rail_data', str(self.train_mode_data.get('rail_idx', '1')))
        self.rail_length = rail_data.get('rail_length')
        self.station_list = rail_data.get('station_list')
        self.station_offset = rail_data.get('station_offset')
        self.max_length = 0
        self.station_lengths = []
        return

    def init_station_node(self):
        train_id = self.train_mode_data.get('train_id')
        train_station_node = confmgr.get('train_node_data')
        self.stop_nodes = confmgr.get('train_data', str(train_id), 'stop_nodes')
        last_station = None
        for i in range(len(self.stop_nodes)):
            data = train_station_node[str(self.stop_nodes[i])]
            if last_station:
                last_dist = last_station.get('track_dis')
                now_dist = data.get('track_dis')
                if now_dist < last_dist:
                    station_length = int(self.rail_length - last_dist + now_dist)
                    self.max_length += station_length
                    self.station_lengths.append(station_length)
                else:
                    station_length = int(now_dist - last_dist)
                    self.max_length += station_length
                    self.station_lengths.append(station_length)
            last_station = data
            self.station_node[i + 1] = data

        self.max_length = float(self.max_length)
        return

    def get_station_lengths(self):
        return self.station_lengths

    def get_stop_nodes(self):
        return self.stop_nodes

    def get_skill_data(self):
        return self.skill_data

    def get_rail_length(self):
        return self.rail_length

    def get_all_station_node(self):
        return self.station_node

    def get_station_node(self, idx):
        return self.station_node.get(idx)

    def get_mode_max_length(self):
        return self.max_length

    def get_station_offset(self):
        return self.station_offset

    def create_extra_model_in_scene(self):
        model_list = self.train_mode_data.get('model_list', [])
        if model_list:
            scene = world.get_active_scene()
            model_data = global_data.game_mode.get_cfg_data('train_extra_model_data')
            for idx in range(len(model_list)):
                data = model_data.get(str(idx + 1), {})
                pos = data.get('c_pos', [0, 0, 0])
                scale = data.get('c_scale', [1, 1, 1])
                yaw = data.get('c_yaw', 0)
                m_path = data.get('m_path', '')
                model = world.model(m_path, scene)
                model.world_position = math3d.vector(*pos)
                model.scale = math3d.vector(*scale)
                model.rotation_matrix = math3d.matrix.make_rotation_y(yaw * math.pi / 180.0)
                model.active_collision = True
                model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
                model.all_materials.rebuild_tech()
                self.model_list.append(model)

    def update_route_sfx_state(self, station_idx):
        if not self.station_route_sfx_list.get(str(station_idx)):
            return
        for idx, data in six.iteritems(self.station_route_sfx_list):
            visible_state = station_idx == int(idx)
            for sfx_id in data:
                sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                if sfx:
                    sfx.visible = visible_state

    def update_train_range_sfx_state(self, num_atk, num_def):
        carriage = self.get_train_carriage()
        if not carriage:
            return
        show_idx = 0
        if not num_atk and not num_def:
            show_idx = 0
        elif num_atk and num_def and num_atk == num_def:
            show_idx = 3
        elif global_data.battle and global_data.battle.get_atk_group_id() == global_data.battle.get_my_group_id():
            if num_atk > num_def:
                show_idx = 2
            else:
                show_idx = 1
        elif num_atk > num_def:
            show_idx = 1
        else:
            show_idx = 2
        carriage.logic.send_event('E_UPDATE_RANGE_SFX_STATE', show_idx)

    def update_train_skill_screen_sfx(self, players):
        if not global_data.cam_lplayer or global_data.cam_lplayer.id not in players or not global_data.battle or not (global_data.mecha and global_data.mecha.logic):
            self.clear_all_screen_sfx()
            return
        else:
            carriage = self.get_train_carriage()
            if not carriage:
                return
            heal_group = carriage.sd.ref_heal_group
            if heal_group == global_data.battle.get_my_group_id():
                heal_state = carriage.sd.ref_heal_state
                if not heal_state and self.heal_screen_sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self.heal_screen_sfx_id)
                    self.heal_screen_sfx_id = None
                elif heal_state and not self.heal_screen_sfx_id:
                    self.heal_screen_sfx_id = create_screen_effect_directly('effect/fx/pingmu/renwuzhiliaofankuismall.sfx')
            damage_group = carriage.sd.ref_damage_group
            if damage_group == global_data.battle.get_my_group_id():
                damage_state = carriage.sd.ref_damage_state
                if not damage_state and self.damage_screen_sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self.damage_screen_sfx_id)
                    self.damage_screen_sfx_id = None
                elif damage_state and not self.damage_screen_sfx_id:
                    self.damage_screen_sfx_id = create_screen_effect_directly('effect/fx/duquan/duquanfankui.sfx')
            return

    def clear_all_screen_sfx(self):
        if self.heal_screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.heal_screen_sfx_id)
        if self.damage_screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.damage_screen_sfx_id)
        self.heal_screen_sfx_id = None
        self.damage_screen_sfx_id = None
        return

    def get_train_carriage(self):
        if not global_data.carry_mgr or not global_data.battle:
            return None
        else:
            train_carridges = global_data.carry_mgr.get_train_ids()
            if not train_carridges:
                return None
            return global_data.battle.get_entity(train_carridges[-1])

    def get_real_train_last_length(self, last_dis):
        if last_dis == -1:
            return self.max_length
        if not last_dis:
            return 0
        if last_dis >= self.station_node[1].get('track_dis'):
            move_length = self.rail_length - last_dis
        else:
            move_length = self.rail_length - self.station_node[1].get('track_dis') + last_dis
        return self.max_length - move_length

    def get_look_at_nearlist_station(self, pos):
        min_dis = 10000000
        min_idx = 1
        for idx, data in six.iteritems(self.station_node):
            station_pos = data.get('station_pos')
            station_pos = math3d.vector(*station_pos)
            distance = pos - station_pos
            if distance.length < min_dis:
                min_dis = distance.length
                min_idx = idx

        if global_data.battle:
            if global_data.battle.get_atk_group_id() == global_data.battle.get_my_group_id():
                return self.station_node.get(min_idx + 1, {}).get('station_pos', [0, 0, 0])
            else:
                return self.station_node.get(min_idx - 1, {}).get('station_pos', [0, 0, 0])

        return self.station_node.get(1, {}).get('station_pos', [0, 0, 0])

    def clear_all_sfx_and_extra_model(self):
        if self.model_list:
            for model in self.model_list:
                if model and model.valid:
                    model.destroy()
                    del model

            self.model_list = []
        if self.station_route_sfx_list:
            for idx, sfx_list in six.iteritems(self.station_route_sfx_list):
                for sfx_id in sfx_list:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.station_route_sfx_list = {'1': [],'2': []}
        self.clear_all_screen_sfx()

    def on_finalize(self):
        if self.train_checker:
            self.train_checker.destroy()
            self.train_checker = None
        self.clear_all_sfx_and_extra_model()
        return