# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComLiftAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
import six
from common.cfg import confmgr
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT, GROUP_GRENADE
from logic.gcommon.common_const import collision_const

class ComLiftAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_LIFT_SPEED': '_get_lift_speed',
       'E_LIFT_SPEED': '_set_lift_speed',
       'E_MACHINE_MOVING': '_set_lift_target',
       'G_COL_ID': '_get_col_id',
       'G_LIFT_ENABLE': '_get_lift_enable',
       'E_MACHINE_MODIF_TIME': '_set_modif_time'
       })

    def __init__(self):
        super(ComLiftAppearance, self).__init__()
        self.sfx_ids = {}
        self.lift_enbale = True
        self.collison_enbale = True
        self.trk_smooth_info = None
        self._time_offset = 0
        self._cur_time = None
        return

    def _set_modif_time(self, delta_time):
        self._time_offset = delta_time

    def destroy(self):
        super(ComLiftAppearance, self).destroy()
        for sfx_id in six.itervalues(self.sfx_ids):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.sfx_ids = {}
        for obj_name, s_obj in six.iteritems(self._sound_ids):
            global_data.sound_mgr.stop_playing_id_fadeout(s_obj)
            self._sound_ids[obj_name] = None

        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComLiftAppearance, self).init_from_dict(unit_obj, bdict)
        self.res_id = bdict.get('res_id', 0)
        self.npc_id = bdict.get('npc_id', 0)
        self._lift_sound_obj_ids = {'lift_%d' % int(self.npc_id): global_data.sound_mgr.register_game_obj('lift_%d' % int(self.npc_id)),'lift_point_%d' % int(self.npc_id): global_data.sound_mgr.register_game_obj('lift_point_%d' % int(self.npc_id))
           }
        self._sound_ids = {'lift_%d' % int(self.npc_id): None,'lift_point_%d' % int(self.npc_id): None
           }
        self.res_conf = confmgr.get('machine_art_config', str(self.res_id), default={})
        self.machine_conf = confmgr.get('machine_config', str(self.npc_id), default={})
        self.param_action = self.machine_conf.get('param_action')
        self._cur_start_pos = math3d.vector(*bdict.get('cur_pos', [100, 240, 100]))
        self.action_start_time = bdict.get('cur_idx_0_start_time', 0)
        self._cur_pos = self._cur_start_pos
        self.need_update = True
        cur_start = math3d.vector(*bdict.get('cur_start', [0, 0, 0]))
        self._cur_target_pos = math3d.vector(*bdict.get('cur_dest', [0, 0, 0]))
        self._cur_start_time = bdict.get('cur_start_time', 0)
        target_dir = self._cur_target_pos - self._cur_pos
        dual_time = bdict.get('cur_period', 0)
        self.cur_speed = target_dir * (1.0 / dual_time)
        self._reach_target = False
        self.move_index = bdict.get('cur_idx', 0)
        self.action_state = []
        now = get_server_time()
        self._cur_time = now
        run_time = now - self.action_start_time
        if self.param_action:
            for i, actions in enumerate(self.param_action):
                play_once, frame_time = actions[-2:]
                if frame_time < run_time and play_once == 1:
                    self.action_state.append(1)
                else:
                    self.action_state.append(0)

        return

    def _get_col_id(self):
        if not self._model:
            return None
        else:
            return self._model.get_col_id()

    def get_model_info(self, unit_obj, bdict):
        res_path = self.res_conf.get('res_path', '')
        return (
         res_path, None, self._cur_pos)

    def _get_lift_speed(self):
        return self.cur_speed

    def _set_lift_speed(self, value):
        if isinstance(value, math3d):
            self.cur_speed = value

    def _set_lift_target(self, target_pos, t_start, dual_time, move_index):
        self.move_index = move_index
        self._reach_target = False
        self._cur_pos = self._cur_target_pos if self._cur_target_pos else self._cur_pos
        self._cur_start_pos = self._cur_pos
        target_dir = target_pos - self._cur_pos
        self.cur_speed = target_dir * (1.0 / dual_time)
        self.send_event('E_UPDATE_LIFT_SPEED', self.cur_speed)
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(self._cur_pos, True)
        else:
            self.send_event('E_POSITION', self._cur_pos)
        self._cur_start_time = t_start
        self._cur_time = self._cur_start_time
        self._cur_target_pos = target_pos
        if self.move_index == 0:
            self.action_start_time = t_start
            self.action_state = []
            if self.param_action:
                for i in range(len(self.param_action)):
                    self.action_state.append(0)

            for obj_name, s_obj in six.iteritems(self._sound_ids):
                global_data.sound_mgr.stop_playing_id_fadeout(s_obj)
                self._sound_ids[obj_name] = None

        return

    def _get_lift_enable(self):
        return self.lift_enbale

    def on_load_model_complete(self, model, user_data):
        rot_lst = self.res_conf.get('rot')
        if rot_lst:
            model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot_lst[0] / 180, math.pi * rot_lst[1] / 180, math.pi * rot_lst[2] / 180))
        model.position = self._cur_pos
        model.scale = math3d.vector(1, 1, 1)
        model.set_col_group_mask(-1, -1)
        model.active_collision = self.collison_enbale
        for sound_data in self.res_conf.get('sound', []):
            ani_name = sound_data['ani_name']
            event = sound_data['event']
            sound_name = sound_data['sound_name']
            is_immediate = sound_data['is_immediate'] == 1
            model.register_anim_key_event(ani_name, event, self.on_animate_sound, [sound_name, is_immediate])

    def on_animate_sound(self, model, anima, enent, data):
        sound_name = data[0]
        is_immediate = data[1]
        obj_name = 'lift_%d' % int(self.npc_id)
        lift_sound = self._lift_sound_obj_ids[obj_name]
        if not lift_sound:
            return
        if not self._cur_pos:
            return
        if self._sound_ids[obj_name]:
            global_data.sound_mgr.stop_playing_id_fadeout(self._sound_ids[obj_name])
        if not is_immediate:
            self._sound_ids[obj_name] = global_data.sound_mgr.post_event(sound_name, lift_sound, self._cur_pos)
        else:
            self._sound_ids[obj_name] = global_data.sound_mgr.post_event_non_optimization(sound_name, lift_sound, self._cur_pos)

    def tick(self, dt):
        if not self._cur_start_time:
            return
        if not self._cur_time:
            return
        self._cur_time += dt
        now = self._cur_time
        if not self._reach_target:
            cur_dir = self.cur_speed * (now - self._cur_start_time)
            new_pos = self._cur_start_pos + cur_dir
            if (self._cur_target_pos.y - self._cur_pos.y) * (self._cur_target_pos.y - new_pos.y) <= 0:
                self._cur_pos = self._cur_target_pos
                self._reach_target = True
            else:
                self._cur_pos = new_pos
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(self._cur_pos)
            else:
                self.send_event('E_POSITION', self._cur_pos)
            s_obj_name = 'lift_%d' % int(self.npc_id)
            if self._lift_sound_obj_ids[s_obj_name]:
                global_data.sound_mgr.set_position(self._lift_sound_obj_ids[s_obj_name], self._cur_pos)
        if self.param_action and self.action_start_time:
            now = get_server_time()
            run_time = now - self.action_start_time + self._time_offset
            for i, actions in enumerate(self.param_action):
                frame_time = actions[-1]
                need_run = False
                if frame_time <= run_time:
                    need_run = self.action_state[i] == 0
                if need_run:
                    self.action_state[i] = self.run_action(actions)

            if self.trk_smooth_info and global_data.cam_lplayer:
                trk_name, trk_range = self.trk_smooth_info
                dist = global_data.cam_lplayer.ev_g_position() - self._cur_pos
                dist = dist.length
                scale = 1 - 1.0 * min(dist, trk_range) / trk_range
                trks = global_data.emgr.camera_get_added_trk_event.emit(trk_name)
                if trks:
                    for trk in trks[0]:
                        trk.set_player_scale(scale, scale)

    def run_action(self, actions):
        func_name = actions[0][0]
        func_obj = getattr(self, func_name)
        if not func_obj:
            return 0
        return func_obj(actions)

    def play_ani(self, actions):
        model = self.ev_g_model()
        if not model:
            return 0
        func_name, ani_name, lift_time = actions[0]
        model.play_animation(ani_name)
        return 1

    def enable_lift(self, actions):
        model = self.ev_g_model()
        if not model:
            return 0
        func_name, enable = actions[0]
        self.lift_enbale = enable == 1
        self.send_event('E_LIFT_ENABLE', self.lift_enbale)
        return 1

    def enable_collision(self, actions):
        model = self.ev_g_model()
        if not model:
            return 0
        func_name, enable = actions[0]
        self.collison_enbale = enable == 1
        model.active_collision = self.collison_enbale
        return 1

    def create_sfx(self, actions):
        model = self.ev_g_model()
        if not model:
            return 0
        func_name, sfx_name, sfx_path, socket = actions[0]
        is_bind_model = type(socket) is str
        if sfx_name in self.sfx_ids:
            sfx_id = self.sfx_ids.get(sfx_name)
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
        if is_bind_model:
            self.sfx_ids[sfx_name] = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket)
        else:
            self.sfx_ids[sfx_name] = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(*socket))
        return 1

    def del_sfx(self, actions):
        func_name, sfx_name = actions[0]
        sfx_id = self.sfx_ids.get(sfx_name)
        if sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
            del self.sfx_ids[sfx_name]
        return 1

    def show_riko_tips(self, actions):
        func_name, text_id, delay_time = actions[0]
        from logic.gcommon.common_const.battle_const import UP_NODE_COMMON_RIKO_TIPS
        message_data = {'content_txt': get_text_by_id(text_id),'delay_time': delay_time,'template_scale': [1, 1]}
        global_data.emgr.battle_event_message.emit(message_data, message_type=UP_NODE_COMMON_RIKO_TIPS)
        return 1

    def play_camera_trk(self, actions):
        func_name, trk_name, trk_range = actions[0]
        self.trk_smooth_info = (trk_name, trk_range)
        global_data.emgr.camera_play_added_trk_event.emit(trk_name)
        return 1

    def stop_camera_trk(self, actions):
        func_name, trk_name = actions[0]
        self.trk_smooth_info = ()
        global_data.emgr.camera_cancel_added_trk_event.emit(trk_name)
        return 1

    def set_model_visible(self, actions):
        model = self.ev_g_model()
        if not model:
            return 0
        func_name, visible = actions[0]
        model.visible = visible == 1
        return 1

    def play_sound(self, actions):
        func_name, obj_name, sound_name, pos, is_immediate = actions[0]
        if obj_name not in self._lift_sound_obj_ids:
            return 0
        if not self._lift_sound_obj_ids[obj_name]:
            return 0
        if self._sound_ids[obj_name]:
            global_data.sound_mgr.stop_playing_id_fadeout(self._sound_ids[obj_name])
        if not is_immediate:
            self._sound_ids[obj_name] = global_data.sound_mgr.post_event(sound_name, self._lift_sound_obj_ids[obj_name], math3d.vector(*pos))
        else:
            self._sound_ids[obj_name] = global_data.sound_mgr.post_event_non_optimization(sound_name, self._lift_sound_obj_ids[obj_name], math3d.vector(*pos))
        return 1

    def stop_sound(self, actions):
        func_name, obj_name = actions[0]
        if obj_name not in self._lift_sound_obj_ids:
            return 0
        else:
            if not self._lift_sound_obj_ids[obj_name]:
                return 0
            if self._sound_ids[obj_name]:
                global_data.sound_mgr.stop_playing_id_fadeout(self._sound_ids[obj_name])
            self._sound_ids[obj_name] = None
            return 1