# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrackMissileCore.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
import collision
from common.utils.timer import CLOCK
from logic.gutils.pve_utils import get_aim_pos
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gcommon.const import NEOX_UNIT_SCALE
TRACK_MISSILE_TAG = register_unit_tag('LTrackMissile')

class ComTrackMissileCore(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'E_COL_LOADED': 'on_col_loaded',
       'E_TRACK_MISSILE_EXPLODE': 'on_explode'
       }
    UP_VECTOR = math3d.vector(0, 1, 0)
    UP_DUR = 0.1

    def init_from_dict(self, unit, bdict):
        self.master_id = bdict.get('master_id')
        self.master = None
        self.camp_id = None
        self.handle_master(self.master_id)
        self.agent_id = bdict.get('agent_id', None)
        self.item_id = bdict.get('robot_no', 90151031)
        self.model = None
        self.conf = confmgr.get('explosive_robot_conf', 'RobotConfig', 'Content', str(self.item_id))
        self.target_pos = bdict.get('target_pos', None)
        if self.target_pos:
            self.target_pos = math3d.vector(*self.target_pos)
        self.target_id = bdict.get('target_id', None)
        self.track_ratio = bdict.get('track_ratio', 0.3)
        self.ori_pos = bdict.get('position', (0, 0, 0))
        self.ori_dir = bdict.get('dir', (0, 0, 1))
        self.col = None
        self.col_size = None
        self.speed = self.conf.get('walk')
        self.ts = 0
        self.col_ids = []
        self.update_col_ids()
        self.up_timer = None
        super(ComTrackMissileCore, self).init_from_dict(unit, bdict)
        return

    def cache(self):
        super(ComTrackMissileCore, self).cache()

    def destroy(self):
        super(ComTrackMissileCore, self).destroy()

    def on_model_load_complete(self, model):
        self.model = model

    def on_col_loaded(self, col):
        self.col = col
        self.col.is_explodable = True
        self.scene.scene_col.add_object(self.col)
        self.col.mass = 100
        self.col.disable_gravity(True)
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        self.col_size = self.ev_g_col_size()
        pos = math3d.vector(*self.ori_pos)
        dire = math3d.vector(*self.ori_dir)
        dire.normalize()
        self.init_missile(pos, dire)
        self.need_update = True

    def init_missile(self, pos, direction):
        self.col.position = pos
        self.col.rotation_matrix = math3d.matrix.make_orient(direction, self.UP_VECTOR)
        self.reset_up_timer()
        self.up_timer = global_data.game_mgr.register_logic_timer(self.upload_pos, interval=self.UP_DUR, mode=CLOCK)

    def tick_missile(self, dt):
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        tar_dir = target_pos - self.get_position()
        tar_dir.normalize()
        forward = self.col.rotation_matrix.forward
        forward.normalize()
        tar_forward = math3d.vector(0, 0, 0)
        tar_forward.intrp(forward, tar_dir, self.track_ratio)
        tar_forward.normalize()
        self.col.position += tar_forward * self.speed * dt
        rot_matrix = math3d.matrix.make_orient(tar_forward, self.UP_VECTOR)
        self.col.rotation_matrix = rot_matrix
        self.model.rotation_matrix = rot_matrix

    def check_contact(self):
        forward = self.col.rotation_matrix.forward
        forward.normalize()
        start_pos = self.col.position
        end_pos = self.col.position + forward * self.col_size * NEOX_UNIT_SCALE * 0.75
        result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
        if result[0]:
            for t in result[1]:
                if t[4].cid in self.col_ids:
                    continue
                if t[4].cid == self.col.cid:
                    continue
                hit_target = global_data.emgr.scene_find_unit_event.emit(t[4].cid)[0]
                if hit_target and hit_target.MASK & TRACK_MISSILE_TAG:
                    continue
                self.upload_explode()
                break

    def tick(self, dt):
        if not self.col:
            self.need_update = False
            return
        if not self.col.valid:
            return
        if not self.model or not self.model.valid:
            self.need_update = False
            return
        self.check_contact()
        self.tick_missile(dt)
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(self.col.position)
        else:
            self.send_event('E_POSITION', self.col.position)

    def on_explode(self, ret):
        if self.model and self.model.valid:
            self.model.visible = False
        else:
            return
        if ret:
            sfx_res = self.conf.get('sfx')
            sfx_scl = self.conf.get('sfx_scale')
            event = self.conf.get('explosive_event')
        else:
            sfx_res = self.conf.get('death_sfx')
            sfx_scl = self.conf.get('death_sfx_scale')
            event = self.conf.get('destroy_event')
        scale = math3d.vector(sfx_scl, sfx_scl, sfx_scl)

        def create_cb(sfx):
            sfx.scale = scale

        global_data.sfx_mgr.create_sfx_in_scene(sfx_res, self.model.position, duration=0.5, on_create_func=create_cb)
        global_data.sound_mgr.play_event(event, self.model.position)

    def upload_explode(self):
        self.need_update = False
        self.send_event('E_CALL_SYNC_METHOD', 'trackmissile_explode', (
         (
          self.col.position.x, self.col.position.y, self.col.position.z),), True)

    def upload_pos(self):
        self.send_event('E_CALL_SYNC_METHOD', 'update_trackmissile_position', (global_data.player.id, (self.col.position.x, self.col.position.y, self.col.position.z)), True)

    def reset_up_timer(self):
        if self.up_timer:
            global_data.game_mgr.unregister_logic_timer(self.up_timer)
            self.up_timer = None
        return

    def get_position(self):
        if self.col and self.col.valid:
            return self.col.position

    def handle_master(self, master_id=None):
        if master_id:
            self.master = EntityManager.getentity(master_id)
            if self.master:
                self.master = self.master.logic
                self.camp_id = self.master.ev_g_camp_id()
        else:
            self.master = None
        return

    def update_col_ids(self):
        if self.master:
            self.col_ids = self.master.ev_g_human_col_id()
            shield_id = self.master.share_data.ref_mecha_shield_col_id
            if shield_id:
                self.col_ids.append(shield_id)
            relative_ids = self.master.share_data.ref_mecha_relative_cols
            if relative_ids:
                self.col_ids.extend(relative_ids)
        else:
            self.col_ids = []