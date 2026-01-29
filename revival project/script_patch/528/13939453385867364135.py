# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag2/Flag2MarkWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import time_utility as tutil
import weakref
import math
from common.utils.cocos_utils import getScreenSize
import math3d
import common.utils.timer as timer
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.gcommon.common_const.building_const import FLAG_RECOVER_BY_DROPPING, FLAG_RECOVER_BY_PLANTING, FLAG_RECOVER_BY_TIME_UP, FLAG_RECOVER_BY_INVALID_REGION, FLAG_RECOVER_BY_START
from common.utils.ui_utils import get_scale
from logic.gcommon.common_const import buff_const as bconst
from logic.gcommon.common_const.building_const import FLAG_STATE_NORMAL, FLAG_STATE_LOCK, FLAG_STATE_FIRST_LOCK, FLAG_STATE_PLANTING, FLAG_STATE_DROP, FLAG_STATE_HOLD
import copy

class Flag2MarkWidgetUI(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    SCREEN_MARGIN = get_scale('40w')
    SMALL_MAP_FLAG_NORMAL_ID = 2031
    SMALL_MAP_FLAG_ENEMY_ID = 2049
    SMALL_MAP_FLAG_TEAMMATE_ID = 2048
    ZERO_VECTOR = math3d.vector(0, 0, 0)
    TYPE_TO_BIND_NODE = {'Flag2Building': 'fx_glow',
       'Avatar': 's_xuetiao',
       'Mecha': 'xuetiao',
       'Puppet': 's_xuetiao',
       'PuppetMecha': 'xuetiao',
       'huoLiuXingBall': None,
       'huoLiuXingBallPuppet': None
       }
    TYPE_TO_OFFSET = {'Flag2Building': math3d.vector(0, 7.0 * NEOX_UNIT_SCALE, 0),
       'Avatar': math3d.vector(0, 0, 0),
       'Puppet': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'PuppetMecha': math3d.vector(0, 0, 0),
       'Mecha': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'huoLiuXingBall': math3d.vector(0, 0, 0),
       'huoLiuXingBallPuppet': math3d.vector(0, 75, 0)
       }
    STATE_NOT_SHOW_TIME_BAR = [
     FLAG_STATE_LOCK, FLAG_STATE_NORMAL, FLAG_STATE_PLANTING, FLAG_STATE_FIRST_LOCK]
    ENEMY_FALG_NOT_SHOW_STATES = [FLAG_STATE_LOCK, FLAG_STATE_NORMAL, FLAG_STATE_FIRST_LOCK]
    STATE_NORMAL = [
     FLAG_STATE_LOCK, FLAG_STATE_NORMAL, FLAG_STATE_FIRST_LOCK]
    STATE_HOLDING = [FLAG_STATE_HOLD, FLAG_STATE_PLANTING]
    STATE_DROP = [FLAG_STATE_DROP]
    STATES_LIST = [
     STATE_NORMAL, STATE_HOLDING, STATE_DROP]
    OPC_STATE = [
     [
      (2, 0), (2, 1), (2, 1)],
     [
      (2, 0), (1, 2), (2, 1)],
     [
      (2, 0), (2, 1), (1, 1)]]

    def __init__(self, target_dict, panel):
        self.on_init(target_dict, panel)

    def on_init(self, target_dict, panel):
        self.init_parameters(target_dict, panel)
        self.init_node()
        self.init_event()
        self.init_timer()

    def init_parameters(self, target_dict, panel):
        self.target_dict = copy.deepcopy(target_dict)
        self.panel = panel
        faction_to_flag_base_id = global_data.death_battle_data.faction_to_flag_base_id
        scn = global_data.game_mgr.scene
        self.camera = weakref.ref(scn.active_camera)
        self.space_nodes = None
        self.red_nd = None
        self.blue_nd = None
        self.red_flag_space_node = None
        self.blue_flag_space_node = None
        self.state2bars = {}
        self.point_bars = [[], []]
        self._binded_model_dict = [
         None, None]
        self._binded_socket_dict = [None, None]
        self.pos_node_norm = None
        self.pos_node_blue = None
        self.pos_node_red = None
        self.icon_update_timer = None
        self.change_follow_target_timer = None
        self._last_alarm_time = [None, None]
        self._lock = False
        self._unlock_timers = [None, None]
        self.nd_rotates = [None, None]
        self.flag_state = [
         FLAG_STATE_LOCK, FLAG_STATE_LOCK]
        self.OPC_FUNC_LIST = [
         self.set_node_invisible, self.set_node_delight, self.set_node_highlight]
        return

    def init_timer(self):
        self.process_update_timer(True)

    def update_follow_target(self, eid, faction_id):
        self.target_dict[faction_id] = eid
        self._binded_model_dict = [None, None]
        self._binded_socket_dict = [None, None]
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'flagsnatch_init_flag_state': self.init_flag_state,
           'flagsnatch_flag_recover': self._on_flag_recover,
           'flagsnatch_flag_pick_up': self._on_flag_pick_up,
           'flagsnatch_flag_init_complete': self._on_flag_init_complete,
           'flagsnatch_flag_plant_state_change': self._on_plant_state_change,
           'flagsnatch_flag_plant_point_change': self._on_plant_point_change
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_flag_state(self, faction_id, state):
        idx = self.get_flag_idx(faction_id)
        self.flag_state[idx] = state
        self.switch_flag_active_ui(faction_id, state)

    def init_node(self):
        self.red_flag_space_node = CCUISpaceNode.Create()
        self.blue_flag_space_node = CCUISpaceNode.Create()
        self.red_nd = global_data.uisystem.load_template_create('battle_flagsnatch2/battle_flagsnatch2_mark_red')
        self.blue_nd = global_data.uisystem.load_template_create('battle_flagsnatch2/battle_flagsnatch2_mark')
        self.red_nd.setPosition(0, 0)
        self.blue_nd.setPosition(0, 0)
        self.red_flag_space_node.AddChild('', self.red_nd)
        self.blue_flag_space_node.AddChild('', self.blue_nd)
        self.space_nodes = (self.red_flag_space_node, self.blue_flag_space_node)
        self.nodes = (self.red_nd, self.blue_nd)
        self.flag_idx2faction_id = {0: None,1: None}
        self.init_pos_dict()
        horizontal_margin = 140 * self.panel.getScale()
        vertical_margin = 80 * self.panel.getScale()
        top_margin = self.SCREEN_MARGIN
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__ + 'red', [self.space_nodes[0]])
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__ + 'blue', [self.space_nodes[1]])
        for node in self.space_nodes:
            node.setPosition(0, 0)
            node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
            node.set_screen_check_margin(0, 0, top_margin, 0)

        self.init_flag_ui()
        return

    def init_pos_dict(self):
        self.state2bars = [
         {FLAG_STATE_LOCK: self.red_nd.bar_count,
            FLAG_STATE_NORMAL: self.red_nd.bar_normal,
            FLAG_STATE_HOLD: self.red_nd.bar_state_hold,
            FLAG_STATE_DROP: self.red_nd.bar_state_drop,
            FLAG_STATE_PLANTING: self.red_nd.bar_state_plant
            },
         {FLAG_STATE_LOCK: self.blue_nd.bar_count,
            FLAG_STATE_NORMAL: self.blue_nd.bar_normal,
            FLAG_STATE_HOLD: self.blue_nd.bar_state_hold,
            FLAG_STATE_DROP: self.blue_nd.bar_state_drop,
            FLAG_STATE_PLANTING: self.blue_nd.bar_state_plant
            }]
        self.point_bars = [
         [
          self.red_nd.bar_state_hold.prog_frame, self.red_nd.bar_state_drop.prog_frame, self.red_nd.bar_state_plant.prog_frame],
         [
          self.blue_nd.bar_state_hold.prog_frame, self.blue_nd.bar_state_drop.prog_frame, self.blue_nd.bar_state_plant.prog_frame]]
        self.nd_rotates = [
         self.red_nd.nd_rotate, self.blue_nd.nd_rotate]
        for k in six.iterkeys(global_data.death_battle_data.flag_ent_id_dict):
            if global_data.player and global_data.player.logic and k == global_data.player.logic.ev_g_group_id():
                self.flag_idx2faction_id[0] = k
            else:
                self.flag_idx2faction_id[1] = k

    def _on_flag_init_complete(self, eid, pos, faction_id):
        global_data.emgr.scene_del_client_mark.emit(eid)
        if faction_id == global_data.player.logic.ev_g_group_id():
            global_data.emgr.scene_add_client_mark.emit(eid, self.SMALL_MAP_FLAG_TEAMMATE_ID, pos)
        else:
            global_data.emgr.scene_add_client_mark.emit(eid, self.SMALL_MAP_FLAG_ENEMY_ID, pos)

    def get_flag_idx(self, faction_id):
        if global_data.cam_lplayer and faction_id == global_data.cam_lplayer.ev_g_camp_id():
            return 0
        else:
            return 1

    def get_flag_node(self, faction_id):
        idx = self.get_flag_idx(faction_id)
        return self.nodes[idx]

    def get_flag_space_node(self, faction_id):
        idx = self.get_flag_idx(faction_id)
        return self.space_nodes[idx]

    def switch_flag_active_ui(self, faction_id, state):
        if not faction_id or not self.state2bars:
            return
        flag_idx = self.get_flag_idx(faction_id)
        self.flag_state[flag_idx] = state
        for d_state, d_bar in six.iteritems(self.state2bars[flag_idx]):
            if d_state == state:
                d_bar.setVisible(True)
            else:
                d_bar.setVisible(False)

        if state in self.STATE_NOT_SHOW_TIME_BAR:
            self.nodes[flag_idx].bar_time.setVisible(False)
        else:
            self.nodes[flag_idx].bar_time.setVisible(True)
        red_state = self.flag_state[0]
        blue_state = self.flag_state[1]
        red_idx = 0
        blue_idx = 0
        for idx in range(3):
            if red_state in self.STATES_LIST[idx]:
                red_idx = idx
            if blue_state in self.STATES_LIST[idx]:
                blue_idx = idx

        opc_state_tuple = self.OPC_STATE[red_idx][blue_idx]
        if self.check_self_taking_flag():
            self.set_node_highlight(self.red_nd)
        else:
            self.OPC_FUNC_LIST[opc_state_tuple[0]](self.red_nd)
        self.OPC_FUNC_LIST[opc_state_tuple[1]](self.blue_nd)

    def set_node_invisible(self, node):
        node.setVisible(False)

    def set_node_highlight(self, node):
        node.setVisible(True)
        node.setOpacity(255)

    def set_node_delight(self, node):
        node.setVisible(True)
        node.setOpacity(50)

    def check_self_taking_flag(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.id == self.target_dict.get(global_data.player.logic.ev_g_group_id(), None)
        else:
            return False

    def init_flag_ui(self):
        for dicts in self.state2bars:
            for d_state, d_bar in six.iteritems(dicts):
                d_bar.setVisible(False)

        for node in self.nodes:
            node.bar_time.setVisible(False)
            node.nd_rotate.setVisible(False)
            node.PlayAnimation('loop')

        for node_list in self.point_bars:
            for node in node_list:
                node.SetPercent(0)

    def _on_lock_flag(self, holder_faction):
        self.switch_flag_active_ui(holder_faction, FLAG_STATE_LOCK)
        global_data.death_battle_data.flag_lock_start_time[holder_faction] = tutil.get_time()

    def _on_first_lock_flag(self, holder_faction):
        self.switch_flag_active_ui(holder_faction, FLAG_STATE_LOCK)

    def _on_flag_pick_up(self, picker_id, picker_faction):
        flag_node = self.get_flag_node(picker_faction)
        flag_node.PlayAnimation('get')
        self._change_follow_target_to_player(picker_id, picker_faction)
        self.switch_flag_active_ui(picker_faction, FLAG_STATE_HOLD)
        self._on_update_time()
        self._change_flag_small_map_status(picker_faction)
        if picker_id == global_data.player.id and global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.remove_target_node(self.__class__.__name__ + 'red', [self.space_nodes[0]])
            self.set_node_highlight(self.red_flag_space_node)

    def _on_drop_flag(self, holder_faction):
        self.switch_flag_active_ui(holder_faction, FLAG_STATE_DROP)
        global_data.death_battle_data.flag_reset_start_time[holder_faction] = tutil.time()
        self._on_update_time()

    def _on_flag_recover(self, holder_id, holder_faction, reason):
        self._change_follow_target_to_flag(holder_faction)
        if reason == FLAG_RECOVER_BY_TIME_UP or reason == FLAG_RECOVER_BY_PLANTING or reason == FLAG_RECOVER_BY_INVALID_REGION:
            self._on_lock_flag(holder_faction)
        elif reason == FLAG_RECOVER_BY_DROPPING:
            self._on_drop_flag(holder_faction)
        elif reason == FLAG_RECOVER_BY_START:
            self._on_first_lock_flag(holder_faction)
        else:
            self.switch_flag_active_ui(holder_faction, FLAG_STATE_NORMAL)
        if holder_id == global_data.player.id and global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__ + 'red', [self.space_nodes[0]])
        self._on_update_time()
        self._change_flag_small_map_status(holder_faction)

    def _on_plant_state_change(self, is_start_plant, faction_id, flag_picker_id):
        if is_start_plant:
            self.switch_flag_active_ui(faction_id, FLAG_STATE_PLANTING)
        else:
            flag_idx = self.get_flag_idx(faction_id)
            if self.flag_state[flag_idx] == FLAG_STATE_DROP or self.flag_state[flag_idx] == FLAG_STATE_LOCK:
                return
            self.switch_flag_active_ui(faction_id, FLAG_STATE_HOLD)

    def _on_plant_point_change(self, point, total_point, faction_id, flag_picker_id):
        idx = self.get_flag_idx(faction_id)
        if total_point and total_point > 0:
            percent = point / total_point * 100.0
        else:
            percent = 0
        for node in self.point_bars[idx]:
            node.SetPercent(percent)

    def _change_follow_target_to_flag(self, faction_id):
        for nd_rotate in self.nd_rotates:
            nd_rotate.setVisible(True)

        self.update_follow_target(global_data.death_battle_data.flag_ent_id_dict[faction_id], faction_id)

    def _change_follow_target_to_player(self, picker_id, picker_faction):
        is_visible = self.get_ui_visible(picker_id)
        if not is_visible:
            for nd_rotate in self.nd_rotates:
                nd_rotate.setVisible(False)

        self.update_follow_target(picker_id, picker_faction)

    def _change_flag_small_map_status(self, picker_faction=None):
        if not picker_faction:
            return
        flag_id = global_data.death_battle_data.flag_ent_id_dict[picker_faction]
        flag_ent = global_data.battle.get_entity(flag_id)
        if not flag_ent:
            return
        global_data.emgr.scene_del_client_mark.emit(flag_id)
        tmp_pos = flag_ent.logic.ev_g_position()
        if picker_faction == global_data.player.logic.ev_g_group_id():
            global_data.emgr.scene_add_client_mark.emit(flag_id, self.SMALL_MAP_FLAG_TEAMMATE_ID, tmp_pos)
        else:
            global_data.emgr.scene_add_client_mark.emit(flag_id, self.SMALL_MAP_FLAG_ENEMY_ID, tmp_pos)

    def get_target_type(self, target_ent, ent_id):
        if not target_ent.logic:
            return 'None'
        target_type = target_ent.__class__.__name__
        if target_type == 'Mecha':
            is_ball = target_ent.logic.ev_g_has_buff_by_id(bconst.BUFF_ID_BALL_STATE)
            if global_data.cam_lplayer:
                is_puppet = global_data.cam_lplayer != ent_id
            else:
                is_puppet = global_data.player.id != ent_id
            if is_ball:
                if is_puppet:
                    return 'huoLiuXingBallPuppet'
                else:
                    return 'huoLiuXingBall'

            elif is_puppet:
                return 'PuppetMecha'
            else:
                return 'Mecha'

        return target_type

    def get_ui_visible(self, target_eid):
        if target_eid == global_data.player.id:
            return False
        return True

    def _on_update_ui_state(self):
        self._on_update_pos_and_rot()
        self._on_update_time()

    def _on_update_time(self):
        for flag_idx in range(2):
            node = self.nodes[flag_idx]
            faction_id = self.flag_idx2faction_id[flag_idx]
            if not node.lab_time:
                continue
            tmp_time = tutil.time()
            mod_time = int(tmp_time)
            if self.flag_state[flag_idx] == FLAG_STATE_LOCK or self.flag_state[flag_idx] == FLAG_STATE_FIRST_LOCK:
                flag_lock_start_time = global_data.death_battle_data.flag_lock_start_time.get(faction_id, 0)
                flag_lock_time = global_data.death_battle_data.flag_lock_time
                if not flag_lock_start_time:
                    continue
                res_time = flag_lock_start_time + flag_lock_time - tmp_time
                if res_time <= 0:
                    self.switch_flag_active_ui(faction_id, FLAG_STATE_NORMAL)
                displaied_res_time = int(math.ceil(res_time))
                node.bar_count.lab_count.setString(str(displaied_res_time) + 'S')
            elif self.flag_state[flag_idx] == FLAG_STATE_HOLD:
                flag_reset_start_time = global_data.death_battle_data.flag_reset_start_time.get(faction_id, None)
                flag_refresh_time = global_data.death_battle_data.flag_refresh_time
                if not flag_reset_start_time:
                    continue
                res_time = flag_reset_start_time + flag_refresh_time - tmp_time
                displaied_res_time = int(math.ceil(res_time))
                displaied_res_time = tutil.get_delta_time_str(displaied_res_time)[3:]
                node.bar_time.lab_time.setString(displaied_res_time)
                if mod_time != self._last_alarm_time[flag_idx]:
                    if res_time < 10:
                        node.bar_time.lab_time.SetColor('#SR')
                        if node.bar_time.lab_time_vx:
                            node.bar_time.lab_time_vx.setString(displaied_res_time)
                            if mod_time != self._last_alarm_time[flag_idx]:
                                self.panel.PlayAnimation('alarm')
                    else:
                        node.bar_time.lab_time.SetColor('#SW')
                self._last_alarm_time[flag_idx] = mod_time
            elif self.flag_state[flag_idx] == FLAG_STATE_DROP:
                flag_reset_start_time = global_data.death_battle_data.flag_reset_start_time.get(faction_id, None)
                flag_refresh_time = global_data.death_battle_data.flag_drop_refresh_time
                if not flag_reset_start_time:
                    continue
                res_time = flag_reset_start_time + flag_refresh_time - tmp_time
                displaied_res_time = int(math.ceil(res_time))
                displaied_res_time = tutil.get_delta_time_str(displaied_res_time)[3:]
                node.bar_time.lab_time.setString(displaied_res_time)
                if mod_time != self._last_alarm_time[flag_idx]:
                    if res_time < 10:
                        node.bar_time.lab_time.SetColor('#SR')
                        if node.bar_time.lab_time_vx:
                            node.bar_time.lab_time_vx.setString(displaied_res_time)
                            if mod_time != self._last_alarm_time[flag_idx]:
                                self.panel.PlayAnimation('alarm')
                    else:
                        node.bar_time.lab_time.SetColor('#SW')
                self._last_alarm_time[flag_idx] = mod_time

        return

    def _on_update_pos_and_rot(self):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        lplayer_pos = self.get_target_pos(cam_lplayer)
        self.update_nd_pos_and_rot(self.camera(), cam_lplayer, lplayer_pos)

    def get_target_pos(self, ltarget):
        if ltarget:
            control_target = ltarget.sd.ref_ctrl_target
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
                return pos
        return None

    def update_nd_pos_and_rot(self, camera, cam_lplayer, lplayer_pos):
        for faction_id, target_eid in six.iteritems(self.target_dict):
            target_ent = global_data.battle.get_entity(target_eid)
            if not target_ent:
                return
            ctrl_entity = target_ent.logic.ev_g_control_target() or None
            if ctrl_entity:
                target_type = self.get_target_type(ctrl_entity, target_eid)
                target_model = ctrl_entity.logic.ev_g_model()
            else:
                target_type = self.get_target_type(target_ent, target_eid)
                target_model = target_ent.logic.ev_g_model()
            pos_offset = self.TYPE_TO_OFFSET.get(target_type, math3d.vector(0, 0, 0))
            bind_node = self.TYPE_TO_BIND_NODE.get(target_type, None)
            if not target_model:
                return
            if not lplayer_pos:
                return
            target_position = target_model.world_position
            if not target_position:
                return
            flag_idx = self.get_flag_idx(faction_id)
            flag_space_node = self.get_flag_space_node(faction_id)
            self.try_bind_model(flag_space_node, flag_idx, target_model, pos_offset, bind_node)
            self.update_rot(camera, target_position, flag_idx)

        return

    def update_rot(self, camera, target_position, nd_idx):
        target_camera_pos = camera.world_to_camera(target_position)
        angle = math.atan2(target_camera_pos.y, target_camera_pos.x)
        angle = angle * 180 / math.pi
        if angle < 0:
            angle += 360
        self.nd_rotates[nd_idx].setRotation(-(angle - 90))

    def try_bind_model(self, node, flag_idx, interact_model, pos_offset=None, socket=None):
        if not node:
            return
        if not self._binded_model_dict[flag_idx] or self._binded_model_dict[flag_idx]() != interact_model or self._binded_socket_dict[flag_idx] != socket:
            if socket:
                node.bind_model(interact_model, socket)
                node.set_fix_xz(False)
            else:
                node.bind_space_object(interact_model)
            self._binded_model_dict[flag_idx] = weakref.ref(interact_model)
            self._binded_socket_dict[flag_idx] = socket
            if pos_offset is not self.ZERO_VECTOR:
                node.set_pos_offset(pos_offset)

    def process_update_timer(self, tag=True):
        if tag:
            if not self.icon_update_timer:
                self.icon_update_timer = global_data.game_mgr.register_logic_timer(self._on_update_ui_state, 0.02, mode=timer.CLOCK)
        elif self.icon_update_timer:
            global_data.game_mgr.unregister_logic_timer(self.icon_update_timer)
            self.icon_update_timer = None
        return

    def on_finalize(self):
        self.process_event(False)
        self.process_update_timer(False)
        self.panel = None
        self.nd_rotates = None
        if self.space_nodes:
            for node in self.space_nodes:
                node.Destroy()

        self.pos_offset = None
        if self.change_follow_target_timer:
            global_data.game_mgr.unregister_logic_timer(self.change_follow_target_timer)
        for _unlock_timer in self._unlock_timers:
            if _unlock_timer:
                global_data.game_mgr.unregister_logic_timer(_unlock_timer)

        return