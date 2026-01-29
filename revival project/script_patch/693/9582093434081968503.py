# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComElasticity.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
import weakref
from logic.gcommon.common_const.building_const import AREA_SHAPE_FAN, AREA_SHAPE_CONVEXES
import logic.gcommon.common_utils.bcast_utils as bcast
import math
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly

class ComElasticity(UnitCom):
    BIND_EVENT = {'E_COLLSION_LOADED': '_on_col_loaded',
       'E_BUILDING_DONE': '_on_build_done',
       'E_SPRING_EFFECT': '_on_spring_effect',
       'E_DETECT_PLAYER': '_on_detect_player',
       'E_SUPER_JUMP_SUCCESS': 'on_super_jump_success',
       'E_SET_CUSTOM_SHAPE_CHECK': 'set_custom_shape_check',
       'E_SET_ENABLE_BOUNCING': 'set_enable_bouncing'
       }

    def __init__(self):
        super(ComElasticity, self).__init__()
        self.is_super_jump = False
        self._enable_bouncing = True

    def init_from_dict(self, unit_obj, bdict):
        super(ComElasticity, self).init_from_dict(unit_obj, bdict)
        self.info = bdict
        self._model = None
        self.listen_target = None
        self.custom_shape = None
        self.custom_shape_args = []
        self.exclude_area_lst = []
        self._building_no = bdict.get('building_no', None)
        self._faction_id = bdict.get('faction_id')
        global_data.emgr.after_observe_target_changed += self._spectate_obj_changed
        return

    def _on_col_loaded(self, m, col):
        import collision
        pos, rot = col.position, col.rotation_matrix
        col.car_undrivable = True
        from common.cfg import confmgr
        building_conf = confmgr.get('c_building_res', str(self._building_no))
        extinfo = building_conf.get('ExtInfo', {})
        scale = extinfo.get('scale_range', 1)
        box = m.bounding_box * math3d.vector(scale, 1, scale)
        self._model = weakref.ref(m)
        self._col = collision.col_object(collision.BOX, box)
        self._pos = pos
        self._trigger_dis = (box.x + box.z) * 1.2 * 3 / 2
        status = self.info.get('status', None)
        from logic.gcommon.common_const import building_const
        if status and status == building_const.BUILDIND_ST_DONE:
            self._enable_functional()
        scene = global_data.game_mgr.get_cur_scene()
        scene.scene_col.add_object(self._col)
        self._col.position = m.position + math3d.vector(0, 5, 0)
        return

    def _on_build_done(self):
        self._enable_functional()
        if not global_data.player or not global_data.player.logic:
            return
        self.detect_player(global_data.player.logic.ev_g_position())

    def _on_detect_player(self):
        if not global_data.player or not global_data.player.logic:
            return
        self.detect_player(global_data.player.logic.ev_g_position())

    def _enable_functional(self):
        if not global_data.player or not global_data.player.logic:
            return
        target = global_data.player.logic
        if target.ev_g_is_in_spectate() or target.ev_g_death():
            return
        self.register_events()

    def _spectate_obj_changed(self, spectate_id):
        if not spectate_id:
            self.unregister_events()
            self.register_events()

    def register_events(self):
        if not global_data.player or not global_data.player.logic:
            return
        target = global_data.player.logic
        target.regist_event('E_ON_JOIN_MECHA', self.on_ctrl_target_changed, 10)
        target.regist_event('E_ON_LEAVE_MECHA', self.on_ctrl_target_changed, 10)
        target.regist_event('E_ON_JOIN_MECHA_START', self.on_ctrl_target_changed, 10)
        target.regist_event('E_ON_LEAVE_MECHA_START', self.on_ctrl_target_changed, 10)
        ctrl_target = target.ev_g_control_target()
        if ctrl_target and ctrl_target.logic:
            if G_POS_CHANGE_MGR:
                ctrl_target.logic.regist_pos_change(self.update_player_pos, 0.15)
            else:
                ctrl_target.logic.regist_event('E_POSITION', self.update_player_pos)
            ctrl_target.logic.regist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            self.listen_target = ctrl_target.logic

    def unregister_events(self):
        target = global_data.player.logic if global_data.player else None
        if target and target.is_valid():
            target.unregist_event('E_ON_JOIN_MECHA', self.on_ctrl_target_changed)
            target.unregist_event('E_ON_LEAVE_MECHA', self.on_ctrl_target_changed)
            target.unregist_event('E_ON_JOIN_MECHA_START', self.on_ctrl_target_changed)
            target.unregist_event('E_ON_LEAVE_MECHA_START', self.on_ctrl_target_changed)
            ctrl_target = target.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                if G_POS_CHANGE_MGR:
                    ctrl_target.logic.unregist_pos_change(self.update_player_pos)
                else:
                    ctrl_target.logic.unregist_event('E_POSITION', self.update_player_pos)
                ctrl_target.logic.unregist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
                self.listen_target = None
        return

    def detect_player(self, pos):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            if pos is None:
                return
            if not self._enable_bouncing:
                return
            if not self.ev_g_elasticity_is_teammate():
                return
            if self.ev_g_is_cd():
                return
            if not self.custom_shape:
                dist = self._pos - pos
                if dist.length > self._trigger_dis:
                    return
                start = self._pos
                end = math3d.vector(start)
                end.y += 4 * NEOX_UNIT_SCALE
                scn = global_data.game_mgr.get_cur_scene()
                interact_list = scn.scene_col.sweep_intersect(self._col, start, end, -1, -1, collision.INCLUDE_FILTER)
                if not interact_list:
                    return
                target = global_data.player.logic.ev_g_control_target()
                if not target or not target.logic:
                    return
                col_id = target.logic.ev_g_human_col_id()
                for col_obj in interact_list:
                    if col_obj.cid in col_id:
                        self.is_super_jump = True
                        target.logic.send_event('E_CALL_SYNC_METHOD', 'try_use_jump_building', (self.unit_obj.id,), True)
                        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SPRING_EFFECT, ()], True)
                        self._on_spring_effect(True)
                        break

            else:
                ret = self.area_shape_checker(pos)
                if ret:
                    target = global_data.player.logic.ev_g_control_target()
                    if not target or not target.logic:
                        return
                    self.is_super_jump = True
                    target.logic.send_event('E_CALL_SYNC_METHOD', 'try_use_jump_building', (self.unit_obj.id, True), True)
                    self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SPRING_EFFECT, ()], True)
                    self._on_spring_effect(True)
            return

    def on_super_jump_success(self):
        if not global_data.player or not global_data.player.logic:
            return
        if not self.is_super_jump:
            return
        target = global_data.player.logic.ev_g_control_target()
        if not target or not target.logic:
            return
        target.logic.send_event('E_CALL_SYNC_METHOD', 'use_jump_building_start', (self.unit_obj.id,), True)
        self.is_super_jump = False

    def destroy(self):
        self.custom_shape = None
        self.custom_shape_args = []
        self.unregister_events()
        global_data.emgr.after_observe_target_changed -= self._spectate_obj_changed
        if self._col:
            scene = global_data.game_mgr.get_cur_scene()
            scene.scene_col.remove_object(self._col)
            self._col = None
        self.info = None
        super(ComElasticity, self).destroy()
        return

    def update_player_pos(self, pos):
        self.detect_player(pos)

    def on_touch_ground(self, *args):

        def delay_detect():
            if self and self.is_valid():
                if self.listen_target:
                    pos = self.listen_target.ev_g_position()
                    self.update_player_pos(pos)

        delay_detect()
        global_data.game_mgr.delay_exec(0.1, delay_detect)

    def _on_spring_effect(self, local=False):
        pass

    def on_ctrl_target_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        ctrl_target = global_data.player.logic.ev_g_control_target()
        if not ctrl_target or not ctrl_target.logic:
            return
        if self.listen_target and self.listen_target != ctrl_target.logic:
            if G_POS_CHANGE_MGR:
                self.listen_target.unregist_pos_change(self.update_player_pos)
                ctrl_target.logic.regist_pos_change(self.update_player_pos, 0.15)
            else:
                self.listen_target.unregist_event('E_POSITION', self.update_player_pos)
                ctrl_target.logic.regist_event('E_POSITION', self.update_player_pos)
            self.listen_target.unregist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            ctrl_target.logic.regist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            self.listen_target = ctrl_target.logic

    def set_custom_shape_check(self, shape, shape_args, exclude_area_lst=None):
        self.custom_shape = shape
        self.custom_shape_args = shape_args
        self.exclude_area_lst = exclude_area_lst or []

    def area_shape_checker(self, lpos):
        if self.custom_shape == AREA_SHAPE_FAN:
            center, angle_range, radius_range = self.custom_shape_args
            center_p_vec = (lpos.x - center[0], lpos.z - center[1])
            dist_squared = center_p_vec[0] * center_p_vec[0] + center_p_vec[1] * center_p_vec[1]
            if not radius_range[0] * radius_range[0] < dist_squared < radius_range[1] * radius_range[1]:
                return False
            angle = math.atan2(center_p_vec[1], center_p_vec[0])
            if not angle_range[0] < angle < angle_range[1]:
                return False
            for area_pos_lst in self.exclude_area_lst:
                if pnpoly(len(area_pos_lst), area_pos_lst, (lpos.x, lpos.z)):
                    return False

            return True
        if self.custom_shape == AREA_SHAPE_CONVEXES:
            is_in = False
            for convexes in self.custom_shape_args:
                if pnpoly(len(convexes), convexes, (lpos.x, lpos.z)):
                    is_in = True
                    break

            for area_pos_lst in self.exclude_area_lst:
                if pnpoly(len(area_pos_lst), area_pos_lst, (lpos.x, lpos.z)):
                    return False

            return is_in
        log_error('area_shape_checker error, unsupported shape ', self.shape)
        return False

    def set_enable_bouncing(self, val):
        self._enable_bouncing = val