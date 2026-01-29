# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComAbsorbShieldCollision.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import RELEASE
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT, GROUP_SHIELD, GROUP_GRENADE
import world
import math3d
import collision
FORWARD_OFFSET = 2.5 * NEOX_UNIT_SCALE

class ComAbsorbShieldCollision(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_ENABLE_ABSORB_SHIELD': 'enable_absorb_shield',
       'E_HIT_ABSORB_SHIELD': 'hit_absorb_shield'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComAbsorbShieldCollision, self).init_from_dict(unit_obj, bdict)
        self.model = None
        if bdict['shield_param']:
            self.shield_width, self.shield_height, self.shield_sockets = bdict['shield_param']
            self.waiting_model_loaded = True
        else:
            self.shield_width = NEOX_UNIT_SCALE
            self.shield_height = NEOX_UNIT_SCALE
            self.shield_sockets = ()
            self.waiting_model_loaded = False
        self.shield_socket_count = len(self.shield_sockets)
        self.shield_timer = -1
        self.shield_col = None
        self.shield_enabled = False
        self.is_avatar = False
        return

    def on_post_init_complete(self, bdict):
        self.is_avatar = self.ev_g_is_avatar()

    def destroy(self):
        super(ComAbsorbShieldCollision, self).destroy()
        if self.shield_enabled:
            self.enable_absorb_shield()
        self.model = None
        return

    def on_model_loaded(self, model):
        self.model = model
        if self.waiting_model_loaded:
            self.enable_absorb_shield(self.shield_width, self.shield_height, self.shield_sockets)
            self.waiting_model_loaded = False

    def _create_shield_timer(self):
        self._release_shield_timer()
        self._update_shield()
        self.shield_timer = global_data.game_mgr.get_post_logic_timer().register(func=self._update_shield, interval=1, times=-1)

    def _release_shield_timer(self):
        if self.shield_timer > -1:
            global_data.game_mgr.get_post_logic_timer().unregister(self.shield_timer)
            self.shield_timer = -1

    def _update_shield(self):
        if not self.shield_col or not self.model or not self.model.valid:
            self.shield_timer = -1
            return RELEASE
        pos = math3d.vector(0, 0, 0)
        for socket_name in self.shield_sockets:
            socket_pos = self.model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD).translation
            pos += socket_pos

        pos *= 1.0 / self.shield_socket_count
        mat = self.model.world_rotation_matrix
        self.shield_col.position = pos + mat.forward * FORWARD_OFFSET
        self.shield_col.rotation_matrix = mat

    def _activate_absorb_shield(self, flag):
        if flag:
            self.scene.scene_col.add_object(self.shield_col)
            global_data.emgr.scene_add_absorb_shield_event.emit(self.shield_col.cid, self.unit_obj)
            self._create_shield_timer()
        else:
            global_data.emgr.scene_remove_absorb_shield_event.emit(self.shield_col.cid)
            self.scene.scene_col.remove_object(self.shield_col)
            self._release_shield_timer()

    def enable_absorb_shield(self, *args):
        flag = len(args) > 0
        if self.shield_enabled == flag:
            return
        else:
            if flag:
                shield_width, shield_height, self.shield_sockets = args
                self.shield_socket_count = len(self.shield_sockets)
                if self.shield_col is None or shield_width != self.shield_width or shield_height != self.shield_width:
                    self.shield_width, self.shield_height = shield_width, shield_height
                    self._reset_shield_col()
            if not self.model:
                self.waiting_model_loaded = flag
                return
            self.shield_enabled = flag
            self._activate_absorb_shield(flag)
            if self.is_avatar:
                self.send_event('E_CALL_SYNC_METHOD', 'wind_dragon_shield', args, True, False, True)
            return

    def _reset_shield_col(self):
        if self.shield_enabled:
            self._activate_absorb_shield(False)
        self.shield_col = collision.col_object(collision.BOX, math3d.vector(self.shield_width, self.shield_height, 1))
        self.shield_col.mask = GROUP_GRENADE
        self.shield_col.group = GROUP_SHOOTUNIT | GROUP_SHIELD

    def hit_absorb_shield(self, hit_pos):
        pos = (hit_pos.x, hit_pos.y, hit_pos.z) if type(hit_pos) == math3d.vector else hit_pos
        rot = math3d.matrix_to_rotation(self.model.world_rotation_matrix)
        rot = (rot.x, rot.y, rot.z, rot.w)
        self.send_event('E_SHOW_ABSORB_SHIELD_HIT_EFFECT', pos, rot)