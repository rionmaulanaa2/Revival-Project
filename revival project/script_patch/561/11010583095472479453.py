# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_logic/ComRemoteControlHuman.py
from __future__ import absolute_import
import math3d
import math
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon import time_utility
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import ai_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from random import uniform, choice
from logic.gcommon.common_const import collision_const
import collision
from logic.gutils.mecha_utils import get_mecha_call_pos
from logic.gcommon.cdata import status_config as st_const
from logic.gutils.character_ctrl_utils import try_jump, try_stand_to_squat, try_squat_to_stand
from common.utils.timer import CLOCK
from logic.gcommon.cdata import status_config
import logic.gcommon.common_const.animation_const as animation_const
ST_ACTION_NONE = 0
ST_ACTION_PARA = 1

class ComRemoteControlHuman(UnitCom):
    BIND_EVENT = {'E_CTRL_FOOT_POSITION': 'ctrl_foot_position',
       'E_CTRL_EJECT': 'eject',
       'E_HEALTH_HP_EMPTY': 'on_die',
       'E_AFTER_EJECT_PARACHUTE': '_on_after_eject_parachute',
       'E_LAND': '_on_land',
       'E_CTRL_ACTION_START': '_on_ctrl_action_start',
       'E_CTRL_REMOTE_FIRE': 'ctrl_remote_fire',
       'E_CTRL_SKATE_BOARD': 'ctrl_skate_board',
       'E_CTRL_DO_ATTACH': 'ctrl_do_attach',
       'E_ON_LEAVE_MECHA': 'on_leave_mecha',
       'E_ROBOT_CALL_MECHA_POS': '_robot_get_call_mecha_pos',
       'E_CANCEL_AGENT': ('on_cancel_agent', 999),
       'E_BEGIN_AGENT_AI': ('on_cancel_agent', 999)
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_JUMP: 'E_CTRL_JUMP',
       ai_const.CTRL_ACTION_RUSH: 'E_CTRL_ROLL'
       }

    def __init__(self):
        super(ComRemoteControlHuman, self).__init__()
        self._st_action = None
        self._para_que = []
        self._to_add_yaw = 0
        self._cur_add_yaw = 0
        self._dt_add_yaw = 0
        self._target_land_pos = None
        self._para_prepare_data = None
        self._skate_board = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControlHuman, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComRemoteControlHuman, self).destroy()

    def get_poison_mgr(self):
        scene = self.scene
        if not scene:
            return None
        else:
            part_battle = scene.get_com('PartBattle')
            if not part_battle:
                return None
            mgr = part_battle.get_poison_manager()
            return mgr

    def _gen_safer_para_data(self, m_pos):
        mgr = self.get_poison_mgr()
        if not mgr:
            return
        else:
            info = mgr.get_cnt_circle_info()
            harm_center = info.get('harm_center', None)
            safe_r = info.get('harm_radius', None)
            if not harm_center or not safe_r:
                return
            m_pos = math3d.vector(m_pos.x, 0, m_pos.z)
            c_pos = math3d.vector(harm_center.x, 0, harm_center.z)
            m = 120 * NEOX_UNIT_SCALE
            dis = (m_pos - c_pos).length
            data = {}
            data['que_action'] = []
            direction = c_pos - m_pos
            if direction.is_zero:
                data['to_yaw'] = self.ev_g_yaw() or 0
                return data
            yaw = direction.yaw
            if safe_r < m or dis > safe_r - m:
                alpha = uniform(-math.pi, math.pi)
                x = c_pos.x + safe_r / 2.0 * math.cos(alpha)
                z = c_pos.z + safe_r / 2.0 * math.sin(alpha)
                data['target_xz'] = (x, 0, z)
                self._target_land_pos = math3d.vector(x, 0, z)
                diff = self._target_land_pos - m_pos
                if not diff.is_zero:
                    yaw = diff.yaw
                self._dt_add_yaw = 0.2
            elif dis > safe_r + m:
                pass
            elif dis > safe_r:
                c = (safe_r + m - dis) / m
                yaw = uniform(-math.pi / 3 * c, math.pi / 3 * c) + yaw
            else:
                return
            data['to_yaw'] = yaw
            return data

    def _gen_para_data(self, data):
        para_type = data['para_type']
        para_target_id = data['para_target_id']
        para_target_pos = data['para_target_pos']
        shake_yaw = data.get('shake_yaw', False)
        pos_m = self.ev_g_position()
        if not pos_m:
            return
        else:
            data = self._gen_safer_para_data(pos_m)
            if data:
                return (data['to_yaw'], data['que_action'])
            direction = None
            if para_target_id:
                killer = EntityManager.getentity(para_target_id)
                if killer and killer.logic:
                    pos_k = killer.logic.ev_g_position()
                    if pos_k and pos_m:
                        direction = pos_m - pos_k
            if not direction and para_target_pos:
                direction = math3d.vector(*para_target_pos) - pos_m
            if direction:
                to_yaw = direction.yaw
            else:
                to_yaw = self.ev_g_yaw() or 0
            if shake_yaw:
                shake_yaw = uniform(*ai_const.AI_EJECT_PARA_SHAKE_YAW)
            else:
                shake_yaw = 0
            que_action = []
            para_conf = ai_const.AI_EJECT_PARA_CONFIG.get(para_type, ())
            first_dir = choice((1, -1))
            for i, step in enumerate(para_conf):
                rad_raw = step['rad']
                rad = uniform(*rad_raw)
                radius_raw = step['radius']
                radius = uniform(*radius_raw)
                t = rad * radius / 22
                rad *= first_dir
                first_dir *= -1
                dt_rad = rad / (t * 30)
                que_action.append((rad, radius, dt_rad, t))

            return (
             to_yaw + shake_yaw, que_action)

    def _cal_target_dy_yaw(self):
        cur_pos = self.ev_g_position()
        if not cur_pos:
            return None
        else:
            cur_yaw = self.ev_g_yaw()
            if not cur_yaw:
                return None
            cur_pos = math3d.vector(cur_pos.x, 0, cur_pos.z)
            diff = self._target_land_pos - cur_pos
            if diff.is_zero:
                return None
            t_yaw = diff.yaw
            to_add_yaw = t_yaw - cur_yaw
            if to_add_yaw:
                to_yaw = to_add_yaw / abs(to_add_yaw) * self._dt_add_yaw + cur_yaw
                return to_yaw
            return None
            return None

    def _tick_para(self, dt):
        if self._target_land_pos:
            to_yaw = self._cal_target_dy_yaw()
            if to_yaw is not None:
                self.send_event('E_ACTION_SET_YAW', to_yaw)
            return
        else:
            if not self._para_que and not self._to_add_yaw:
                self._st_action = ST_ACTION_NONE
                return
            if not self._to_add_yaw:
                rad, radius, dt_rad, t = self._para_que.pop(0)
                self._to_add_yaw = rad
                self._dt_add_yaw = dt_rad
            else:
                yaw = self.ev_g_yaw()
                if yaw is None:
                    return
            dt_yaw = self._dt_add_yaw
            yaw += dt_yaw
            self._cur_add_yaw += dt_yaw
            self.send_event('E_ACTION_SET_YAW', yaw)
            if abs(self._cur_add_yaw / self._to_add_yaw) > 1:
                self._to_add_yaw = 0
                self._cur_add_yaw = 0
            return

    def _clear_para(self):
        self._st_action = ST_ACTION_NONE
        self._para_running_data = None
        return

    def eject(self, data):
        data['timestamp'] = time_utility.time()
        self._para_prepare_data = data
        self.send_event('E_CLEAR_MOVE_TO_POS')
        self.send_event('E_STOP_MOVE_TO')
        ctrl_mecha = self.ev_g_control_target()
        if ctrl_mecha and ctrl_mecha.logic:
            to_yaw = ctrl_mecha.logic.sd.ref_logic_trans.yaw_target
            if to_yaw:
                self.send_event('E_ACTION_SET_YAW', to_yaw)
        from logic.gcommon.common_const.collision_const import MECHA_STAND_HEIGHT
        off_pos = self.ev_g_position() + math3d.vector(0, MECHA_STAND_HEIGHT / 3, 0)
        arg = {'reset_pos': off_pos,'use_phys': 0}
        self.send_event('E_SET_CONTROL_TARGET', None, arg)

        def _():
            if self.is_valid():
                self.send_event('E_EJECT')

        global_data.game_mgr.register_logic_timer(lambda : _(), interval=1.0, mode=CLOCK, times=1)
        return

    def _on_after_eject_parachute(self):
        vertical_speed = self.ev_g_vertical_speed()
        if vertical_speed > 16.0:
            self.send_event('E_VERTICAL_SPEED', 16.0)
        if not self._para_prepare_data:
            return
        else:
            self._target_land_pos = None
            if self._para_prepare_data.get('to_yaw', None):
                to_yaw, que_action = self._para_prepare_data['to_yaw'], self._para_prepare_data['que_action']
                target_land_pos = self._para_prepare_data.get('target_land_pos', None)
                if target_land_pos:
                    self._target_land_pos = math3d.vector(*target_land_pos)
                self._dt_add_yaw = self._para_prepare_data.get('dt_add_yaw', 0.2)
            else:
                to_yaw, que_action = self._gen_para_data(self._para_prepare_data)
            self.send_event('E_ACTION_SET_YAW', to_yaw)
            self.send_event('E_CHANGE_PARACHUTE_MIN_PITCH', -0.8)
            self.send_event('E_ENABLE_ADJUST_MODEL_YAW', False)
            self._para_que = que_action
            self._st_action = ST_ACTION_PARA
            self.need_update = True
            self.send_event('E_MOVE', math3d.vector(0, 0, 1))
            return

    def _on_land(self, *args):
        self._clear_para()

    def tick(self, dt):
        if self._st_action == ST_ACTION_PARA:
            self._tick_para(dt)

    def on_die(self, *args):
        self.need_update = False

    def _on_ctrl_action_start(self, action_type, *args):
        if action_type == ai_const.CTRL_ACTION_RUSH:
            return self.ev_g_status_check_pass(status_config.ST_ROLL) or None
        if self.ev_g_is_equip_rush_bone():
            evt = 'E_CTRL_RUSH' if 1 else 'E_CTRL_ROLL'
            self.send_event(evt, *args)
        elif action_type == ai_const.CTRL_ACTION_JUMP:
            if self.battle.is_battle_prepare_stage():
                waiting_active = self.ev_g_char_waiting()
                if waiting_active:
                    char = self.unit_obj._coms['ComCharacter']
                    char.resume_gravity()
            try_jump(self)
        elif action_type == ai_const.CTRL_ACTION_EXT:
            if self.ev_g_is_stand():
                try_stand_to_squat(self)
            else:
                try_squat_to_stand(self)

    def _check_future_pos(self):
        scene = self.scene
        if not scene:
            return False
        else:
            cur_pos = self.ev_g_position()
            if not cur_pos:
                return False
            w_dir = self.ev_g_get_walk_direction()
            if not w_dir:
                return False
            if w_dir.is_zero:
                yaw = self.ev_g_yaw()
                if yaw is None:
                    return False
                w_dir = math3d.matrix.make_rotation_y(yaw).forward
            w_dir.normalize()
            start_pos = cur_pos + w_dir * 8 * NEOX_UNIT_SCALE + math3d.vector(0, 20 * NEOX_UNIT_SCALE, 0)
            end_pos = start_pos + math3d.vector(0, -80 * NEOX_UNIT_SCALE, 0)
            group = collision_const.GROUP_CHARACTER_EXCLUDE & ~collision_const.GROUP_SHOOTUNIT
            result = scene.scene_col.hit_by_ray(start_pos, end_pos, 0, group, group, collision.INCLUDE_FILTER)
            if result[0]:
                obj = result[5]
                if obj and obj.group == collision_const.WATER_GROUP:
                    return False
            return True

    def ctrl_remote_fire(self, wp_id, target_id, target_pos):
        cur_wp = self.sd.ref_wp_bar_cur_weapon
        if cur_wp is None:
            return
        else:
            if cur_wp.get_id() != wp_id:
                return
            self.send_event('E_SET_AI_DATA', 'enemy_id', target_id)
            self.send_event('E_GUN_ATTACK')
            self.send_event('E_ATTACK_START')
            self.send_event('E_REMOTE_FIRE')
            return

    def ctrl_skate_board(self):
        if self._skate_board:
            return
        else:
            self.send_event('E_CTRL_MOVE_STOP')
            item_id = 1666
            start_time = 0
            import logic.gcommon.common_utils.item_config as item_conf
            conf = item_conf.get_use_by_id(item_id)
            t_singing = conf['fSingTime']
            action_id = conf.get('iAction', None)
            self.send_event('E_ITEMUSE_PRE', item_id, t_singing, start_time, action_id)
            self._skate_board = global_data.game_mgr.delay_exec(t_singing, self.skate_board_callback)
            return

    def skate_board_callback(self):
        self._skate_board = None
        if not self.sd.ref_is_agent:
            return
        else:
            self.send_event('E_TRY_SERVER_ACTION', 'E_ITEMUSE_DO', 1666, 0, None)
            self.ev_g_cancel_state(st_const.ST_USE_ITEM)
            self.send_event('E_ITEMUSE_END', 1666)
            return

    def ctrl_do_attach(self, atch_data):
        self.ev_g_do_attach(atch_data)

    def on_leave_mecha(self, *_):
        self.send_event('E_STOP_MOVE_TO')
        self.ev_g_char_resume_col()

    def _robot_get_call_mecha_pos(self):
        m_pos = self.ev_g_position()
        yaw = self.ev_g_yaw() or 0
        forward = math3d.matrix.make_rotation_y(yaw).forward
        res, pos = get_mecha_call_pos(m_pos, None, False, forward)
        if res:
            self.send_event('E_SYNC_STATE_DATA', 'call_mecha_pos', [pos.x, pos.y, pos.z])
        else:
            self.send_event('E_SYNC_STATE_DATA', 'call_mecha_pos', -1)
        return