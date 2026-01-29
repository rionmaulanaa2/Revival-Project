# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainMove.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
from common.cfg import confmgr
import logic.gcommon.cdata.status_config as status_config
import weakref
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.trk.TrkManager import TrkManager
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const import battle_const
import common.utils.timer as timer
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
UNIT_Y = math3d.vector(0, 1, 0)

class ComTrainMove(UnitCom):
    CHECK_DIS = 12 * NEOX_UNIT_SCALE
    ZERO_VECTOR = math3d.vector(0, 0, 0)
    VALID_SOUND_STATE = ('start', 'run', 'end')
    BIND_EVENT = {'E_COLLSION_LOADED': '_on_col_loaded',
       'E_DO_CARRIAGE_MOVE': '_on_carriage_move',
       'E_PLAYER_ENTER_TRAIN': '_on_player_enter',
       'E_PLAYER_LEAVE_TRAIN': '_on_player_leave',
       'E_CHANGE_CARRIAGE_STATE': '_on_change_carriage_state',
       'G_PACK_CARGO_INFO': 'pack_cargo_info',
       'G_RELATIVE_POS': 'get_relative_pos',
       'G_RAIL_POS_FROM_DIS': 'get_rail_pos_from_dis'
       }

    def __init__(self):
        super(ComTrainMove, self).__init__()
        self._dis = None
        self._trk_manager = None
        self._carriage_length = None
        self._carriage_idx = None
        self._carriage_no = None
        self._model = None
        self._col = None
        self._user_follow_speed = None
        self._user_follow_dir = None
        self._users = None
        self._bac_loc = None
        self._sound_obj_id = None
        self._train_state = None
        self._train_no = None
        self._train_prog_nty_timer = None
        self._user_judge_timer = None
        self._head_dis = None
        self._rail_no = None
        self._nodes_m = []
        self.last_prog = None
        self._rail_length = confmgr.get('rail_data', '1', 'rail_length')
        self._music_player_ids = []
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainMove, self).init_from_dict(unit_obj, bdict)
        self._trk_manager = TrkManager()
        self._carriage_no = bdict.get('carriage_no')
        self._rail_no = bdict.get('rail_no', 1)
        rail_conf = confmgr.get('rail_data')[str(self._rail_no)]
        trk_file_name = rail_conf['file_name']
        rail_length = rail_conf['rail_length']
        is_left_hand = rail_conf['is_left_hand']
        self._trk_manager.load_trk(trk_file_name, rail_length, is_left_hand)
        res_path = confmgr.get('train_res')[str(self._carriage_no)]['res_path']
        self._dis = bdict.get('trk_dis', 0)
        self._carriage_length = bdict.get('carriage_length', 20)
        self._carriage_idx = bdict.get('carriage_idx')
        self._train_state = bdict.get('client_state', battle_const.KD_TRAIN_START_SPEED_REDUCE)
        self._train_no = bdict.get('train_no')
        train_node_data = confmgr.get('train_node_data')
        for key, value in six.iteritems(train_node_data):
            self._nodes_m.append(value.get('track_dis'))

        self._nodes_m.sort()
        self.init_sound()
        self._on_change_carriage_state(self._train_state)

    def init_sound(self):
        if self._sound_obj_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_obj_id)
            self._sound_obj_id = None
        self._sound_obj_id = global_data.sound_mgr.register_game_obj('Train_carriage_' + str(self.unit_obj.id))
        if self._carriage_idx == 1:
            player_id = global_data.sound_mgr.post_event('Play_steamtrain_head', self._sound_obj_id, self.ev_g_position())
            self._music_player_ids.append(player_id)
        else:
            player_id = global_data.sound_mgr.post_event('Play_steamtrain_carriage', self._sound_obj_id, self.ev_g_position())
            self._music_player_ids.append(player_id)
        return

    def show_trk(self, trk, step=3):
        scn = world.get_active_scene()
        obj = world.primitives(scn)
        pts_list = []
        trk_length = trk.trk_length
        for i in range(0, int(trk_length), step):
            tmp_pos = trk.get_pos(i)
            pts_list.append((tmp_pos.x, tmp_pos.y, tmp_pos.z, 16711680))

        obj.create_line_strip(pts_list)

    def _on_col_loaded(self, model, col):
        self._model = model
        self._col = col
        self._on_carriage_move(self._dis, 0, None, self._dis, self._dis)
        return

    def _on_change_carriage_state(self, state):
        if state in self.VALID_SOUND_STATE:
            global_data.sound_mgr.set_switch('fukongdao_steamtrain', state, self._sound_obj_id)
        self._train_state = state

    def _on_carriage_move(self, dis, tmp_speed, delta, head_dis, target_dis):
        if not self._model:
            return
        self._dis = dis
        self._head_dis = head_dis
        pos, rot = self._trk_manager.get_pos_and_rot(self._dis)
        half_length = self._carriage_length / 2
        be_pos, _ = self._trk_manager.get_pos_and_rot(self._dis - half_length)
        af_pos, _ = self._trk_manager.get_pos_and_rot(self._dis + half_length)
        pos = be_pos + af_pos
        pos.x = pos.x / 2
        pos.y = pos.y / 2
        pos.z = pos.z / 2
        dir_vec = af_pos - be_pos
        dir_vec.normalize()
        mat = self.forward_to_matrix(dir_vec)
        player_tmp_pos = self.get_player_pos()
        self._user_follow_dir = self.cal_user_follow_dir(player_tmp_pos, pos, mat)
        self._user_follow_speed = abs(tmp_speed)
        if self._bac_loc:
            self.set_delay_pos_and_rot(self._bac_loc)
        else:
            self.set_delay_pos_and_rot((pos, mat))
        self._bac_loc = (
         pos, mat)
        self.update_prog(head_dis)
        self.do_user_follow(self._user_follow_speed, self._user_follow_dir)
        self.sd.ref_carriage_pos = pos
        self.sd.ref_dis = dis
        self.sd.ref_dir = self._user_follow_dir
        self.sd.ref_speed = tmp_speed
        self.sd.ref_target_dis = target_dis

    def update_prog(self, head_dis):
        if self._carriage_idx == 1:
            prog = self.get_between_nodes_prog(head_dis)
            if self.last_prog and self.last_prog < 0.9 and prog >= 0.9:
                global_data.emgr.on_train_pre_arrival.emit(self.ev_g_position())
            self.last_prog = prog

    def get_between_nodes_prog(self, train_m_pos):
        be_pos = None
        af_pos = None
        for i in range(len(self._nodes_m) - 1):
            if self._nodes_m[i] <= train_m_pos <= self._nodes_m[i + 1]:
                be_pos = train_m_pos - self._nodes_m[i]
                af_pos = self._nodes_m[i + 1] - train_m_pos
                break

        if not be_pos and not af_pos:
            be_pos = train_m_pos - self._nodes_m[len(self._nodes_m) - 1]
            af_pos = self._nodes_m[0] - train_m_pos
            be_pos = be_pos + self._rail_length if be_pos < 0 else be_pos
            af_pos = af_pos + self._rail_length if af_pos < 0 else af_pos
        prog = be_pos / (af_pos + be_pos)
        prog = 1 if prog > 1 else prog
        prog = 0 if prog < 0 else prog
        return prog

    def cal_user_follow_dir(self, user_pos, next_frame_train_pos, next_fram_train_rot_mat):
        if not user_pos:
            return None
        else:
            trans = self._model.world_transformation
            rel_user_pos = self.world_to_relative(user_pos, trans)
            after_trans = self.get_trans(next_frame_train_pos, next_fram_train_rot_mat)
            next_frame_user_pos = self.relative_to_world(rel_user_pos, after_trans)
            follow_dir = next_frame_user_pos - user_pos
            if follow_dir != self.ZERO_VECTOR:
                follow_dir.normalize()
            self.check_is_inside_carriage(user_pos, rel_user_pos, follow_dir)
            return follow_dir

    def get_trans(self, pos, rot_mat):
        be_pos = self._model.world_position
        be_rot_mat = self._model.rotation_matrix
        self._model.world_position = pos
        self._model.rotation_matrix = rot_mat
        trans = self._model.world_transformation
        self._model.world_position = be_pos
        self._model.rotation_matrix = be_rot_mat
        return trans

    def pack_cargo_info(self, world_pos):
        world_pos = math3d.vector(*world_pos)
        if not self._model:
            return None
        else:
            rel_pos = self.world_to_relative(world_pos, self._model.world_transformation)
            rel_pos = [rel_pos.x, rel_pos.y, rel_pos.z]
            cargo_info = {'train_no': self._train_no,
               'train_carriage_id': self.unit_obj.id,
               'rel_pos': rel_pos
               }
            return cargo_info

    def get_relative_pos(self, world_pos):
        rel_pos = self.world_to_relative(world_pos, self._model.world_transformation)
        rel_pos = [rel_pos.x, rel_pos.y, rel_pos.z]
        return rel_pos

    def relative_to_world(self, rel_coor, par_trans):
        return rel_coor * par_trans

    def world_to_relative(self, world_coor, par_trans):
        par_trans.inverse()
        return world_coor * par_trans

    def set_delay_pos_and_rot(self, loc):
        if loc:
            pos, mat = loc
            self._model.world_position = pos
            self._model.rotation_matrix = mat
            self.send_event('E_SET_COL_POS_AND_ROT', pos, mat)
            self.update_sound_pos_value(pos)
            if self._model:
                self.send_event('E_DO_CARGO_MOVE', self._model.world_transformation)

    def update_sound_pos_value(self, pos):
        if not pos:
            return
        global_data.sound_mgr.set_position(self._sound_obj_id, pos)
        if not isinstance(pos, math3d.vector):
            return
        player_pos = global_data.player.logic.ev_g_position()
        if not isinstance(player_pos, math3d.vector):
            return
        dis_vec = player_pos - pos
        dis = dis_vec.length
        global_data.sound_mgr.set_rtpc('carriage', dis, self._sound_obj_id)

    def forward_to_matrix(self, forward):
        right = forward.cross(UNIT_Y)
        right.normalize()
        up = right.cross(forward)
        up.normalize()
        mat = math3d.matrix.make_orient(forward, up)
        return mat

    def get_rail_pos_from_dis(self, dis):
        if not self._trk_manager:
            return [0, 0, 0]
        pos = self._trk_manager.get_pos(dis)
        return [
         pos.x, pos.y, pos.z]

    def do_user_follow(self, speed, dir_vec):
        self.update_player_status()
        if not self._users:
            return
        else:
            if speed == 0:
                self._users.send_event('E_CHARACTER_WALK_TRAIN', math3d.vector(0, 0, 0))
                return
            if speed is None or dir_vec is None:
                return
            speed *= NEOX_UNIT_SCALE
            move_dir = dir_vec
            move_dir *= speed
            self._users.send_event('E_CHARACTER_WALK_TRAIN', move_dir)
            return

    def clear_before_user_status(self):
        if self._users:
            self._users.send_event('E_CHARACTER_WALK_TRAIN', math3d.vector(0, 0, 0))
        self._users = None
        return

    def get_player_pos(self):
        if not global_data.cam_lplayer:
            return None
        else:
            ctrl_target = global_data.cam_lplayer.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                pos = ctrl_target.logic.ev_g_position()
                return pos
            return global_data.cam_lplayer.ev_g_position()
            return None

    def update_player_status(self):
        self.clear_before_user_status()
        rel_id, rel_pos = global_data.carry_mgr.player_rel_info
        if rel_id == self.unit_obj.id:
            ctrl_target = global_data.player.logic.ev_g_control_target()
            self._users = ctrl_target.logic
            self.upadate_train_prog()

    def is_on_carriage(self, pos):
        start = math3d.vector(pos.x, pos.y, pos.z)
        end = math3d.vector(pos.x, pos.y - 8 * NEOX_UNIT_SCALE, pos.z)
        start.y += 0.2 * NEOX_UNIT_SCALE
        ress = global_data.game_mgr.scene.scene_col.hit_by_ray(start, end, -1, -1, collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER, True)
        if ress and ress[0]:
            for res in ress[1]:
                if res[4] == self._col:
                    return True

        return False

    @execute_by_mode(True, (game_mode_const.GAME_MODE_TRAIN,))
    def check_is_inside_carriage(self, user_pos, rel_user_pos, follow_dir):
        if not global_data.battle or not global_data.battle.get_enable_in_train_check():
            return
        if not follow_dir:
            return
        if self._carriage_idx == 2 and abs(rel_user_pos.x) < 20 and abs(rel_user_pos.z) < 80:
            if 10 < rel_user_pos.y < 30:
                if global_data.player and global_data.player.logic:
                    pos = global_data.player.logic.ev_g_position()
                    if not pos:
                        return
                    global_data.player.logic.send_event('E_FOOT_POSITION', math3d.vector(pos.x - follow_dir.x * NEOX_UNIT_SCALE, pos.y, pos.z - follow_dir.z * NEOX_UNIT_SCALE))

    def upadate_train_prog(self):
        if self._users:
            dis = self._head_dis if self._head_dis is not None else self._dis
            global_data.emgr.on_update_train_prog.emit(True, self._train_state, dis, self.unit_obj.id)
        return

    def destroy(self):
        super(ComTrainMove, self).destroy()
        self._users = None
        self._model = None
        self._col = None
        for music_player_id in self._music_player_ids:
            global_data.sound_mgr.stop_playing_id(music_player_id)

        self._music_player_ids = None
        if self._sound_obj_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_obj_id)
            self._sound_obj_id = None
        if self._train_prog_nty_timer:
            global_data.game_mgr.unregister_logic_timer(self._train_prog_nty_timer)
        if self._user_judge_timer:
            global_data.game_mgr.unregister_logic_timer(self._user_judge_timer)
        return