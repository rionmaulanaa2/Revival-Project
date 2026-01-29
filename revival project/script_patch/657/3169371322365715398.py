# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFlagUI.py
from __future__ import absolute_import
import six
import six_ex
import math
import math3d
import world
import render
from ..UnitCom import UnitCom
import common.utilities
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref
import game3d
import common.utils.timer as timer
from logic.client.const import game_mode_const
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
OUTLINE_ALPHA = 0.3333
EAGLE_TYPE = 'eagle'
EYE_TYPE = 'sinper'
GIFT_TYPE = 'gift'
THUNDER_TYPE = 'thunder'
FLAG_PATH = {GIFT_TYPE: 'effect/fx/renwu/rw_sx_biaoji.sfx',
   THUNDER_TYPE: 'gui/ui_res_2/simui/sim_five_thunder.png'
   }
BIND_PART = {GIFT_TYPE: {'human_socket': 'hit','mecha_socket': 'part_point1','mechatran_socket': 'seat_1'}}

class ComFlagUI(UnitCom):
    BIND_EVENT = {'E_ADD_EAGLE_FLAG': 'on_add_eagle_flag',
       'E_DEL_EAGLE_FLAG': 'on_del_eagle_flag',
       'E_MODEL_LOADED': 'on_model_load_complete',
       'E_ON_ACTION_MECHA_FINISH': 'on_enter_mecha_action_end',
       'E_BLOCK_FLAG': 'on_block_flag',
       'E_SHOW_BATTLE_BROADCAST': 'on_show_battle_broadcast'
       }

    def __init__(self):
        super(ComFlagUI, self).__init__()
        self._block = False
        self._attacked_sfx = None
        self._attacked_sfx_id = None
        self._attacked_flag_ui = None
        self._attacked_flag_bg = None
        self._attacked_flag_type = None
        self._creators = {}
        self._save_outline_flag = False
        self._scale_factor = [
         0.07, 0.008]
        self._scale_range = [0 * NEOX_UNIT_SCALE, 120 * NEOX_UNIT_SCALE]
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlagUI, self).init_from_dict(unit_obj, bdict)

    def on_model_load_complete(self, model):
        for creator_id, flag_type in six.iteritems(self._creators):
            if flag_type in FLAG_PATH:
                self._try_create_attacked_flag(creator_id, flag_type)
            else:
                self.set_is_outline(True)

        if self.ev_g_is_mechatran():
            self._scale_factor = [
             0.09, 0.01]
            self._scale_range = [0 * NEOX_UNIT_SCALE, 120 * NEOX_UNIT_SCALE]
        elif self.sd.ref_is_mecha:
            self._scale_factor = [
             0.18, 0.02]
            self._scale_range = [0 * NEOX_UNIT_SCALE, 200 * NEOX_UNIT_SCALE]
        else:
            self._scale_factor = [
             0.07, 0.008]
            self._scale_range = [0 * NEOX_UNIT_SCALE, 120 * NEOX_UNIT_SCALE]

    def tick(self, delta):
        if self._attacked_flag_ui:
            model = self.ev_g_model()
            if model:
                pos = model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                max_dist = 300
                scale = (max_dist - dist) * 1.0 / max_dist
                self._attacked_flag_ui.scale = (scale, scale)
        if self._attacked_sfx and self._attacked_sfx.valid:
            model = self.ev_g_model()
            if model:
                pos = model.world_position
                sfx_width = 5.0
                dist = self.scene.active_camera.position - pos
                dist_length = dist.length
                h_fov = self.scene.active_camera.fov * 0.5
                tan_h_fov = math.tan(h_fov / 180.0 * math.pi)
                total_width = dist_length * tan_h_fov * 2.0
                if total_width < 0.001:
                    perspect_scale = 1.0
                else:
                    perspect_scale = sfx_width / total_width
                factor = common.utilities.smoothstep(self._scale_range[0], self._scale_range[1], dist_length)
                custom_factor = common.utilities.lerp(self._scale_factor[0], self._scale_factor[1], factor)
                scale = 1.0 / perspect_scale * custom_factor
                self._attacked_sfx.scale = math3d.vector(scale, scale, scale)

    def _try_create_attacked_flag(self, creator_id, flag_type):
        self._attacked_flag_type = flag_type
        self._create_attacked_flag()

    def _create_attacked_flag(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            box = model.bounding_box
            scale_y = model.scale.y
            res_path = FLAG_PATH.get(self._attacked_flag_type, EAGLE_TYPE)
            if res_path.endswith('sfx'):
                if self.sd.ref_is_mecha:
                    socket = BIND_PART.get(self._attacked_flag_type, {}).get('mecha_socket', '')
                elif self.ev_g_is_mechatran():
                    socket = BIND_PART.get(self._attacked_flag_type, {}).get('mechatran_socket', '')
                else:
                    socket = BIND_PART.get(self._attacked_flag_type, {}).get('human_socket', '')
                if socket:
                    if self._attacked_sfx_id:
                        global_data.sfx_mgr.remove_sfx_by_id(self._attacked_sfx_id)
                    self._attacked_sfx = None

                    def on_create_sfx(sfx, *args):
                        self._attacked_sfx = sfx
                        sfx.restart()

                    self._attacked_sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket, type=world.BIND_TYPE_TRANSLATE, on_create_func=on_create_sfx)
            elif res_path.endswith('png'):
                if not self._attacked_flag_ui or not self._attacked_flag_ui.valid:
                    self._attacked_flag_ui = world.simuiobject(render.texture(res_path))
                    self._attacked_flag_bg = self._attacked_flag_ui.add_image_ui(0, 0, 64, 64, 0, 0)
                    self._attacked_flag_ui.set_ui_align(self._attacked_flag_bg, 0.5, 1)
                    self._attacked_flag_ui.set_ui_fill_z(self._attacked_flag_bg, True)
                    self._attacked_flag_ui.set_parent(model)
                    self._attacked_flag_ui.visible = True
                    self._attacked_flag_ui.inherit_flag = world.INHERIT_TRANSLATION
                self._attacked_flag_ui.position = math3d.vector(0, box.y * scale_y + 20, 0)
            if box.y == 0:
                global_data.game_mgr.next_exec(self._create_attacked_flag)
            self.need_update = True
            return

    def _del_attacked_flag(self):
        if self._attacked_flag_ui and self._attacked_flag_ui.valid:
            self._attacked_flag_ui.destroy()
        if self._attacked_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._attacked_sfx_id)
        self._attacked_sfx_id = None
        self._attacked_sfx = None
        self._attacked_flag_ui = None
        self._attacked_flag_bg = None
        self.need_update = False
        return

    def destroy(self):
        self._del_attacked_flag()
        self._creators = {}
        super(ComFlagUI, self).destroy()

    def on_add_eagle_flag(self, creator_id, flag_type, is_client_owner):
        if is_client_owner:
            return
        if creator_id in self._creators:
            return
        self._creators[creator_id] = flag_type
        if self._block:
            return
        if flag_type in FLAG_PATH:
            self._try_create_attacked_flag(creator_id, flag_type)
        elif not self.set_is_outline(True):
            self._creators.pop(creator_id)

    def set_is_outline(self, flag):
        self.send_event('E_DISABLE_TRANSPARENT', flag)
        model = self.ev_g_model()
        if not self.scene:
            log_error('[ComFlagUI]scene is unvalid!!!!!')
            return False
        if not self.unit_obj:
            log_error('[ComFlagUI]unit_obj is unvalid!!!')
            return False
        if model and model.valid:
            if self.ev_g_is_pause_outline():
                return False
            self._save_outline_flag = flag
            if flag:
                self.send_event('E_ADD_MATERIAL_STATUS', 'ComFlag_see_through_outline', param={'status_type': 'SEE_THROUGH_OUTLINE',
                   'outline_alpha': OUTLINE_ALPHA,
                   'update_interval': 0.5,
                   'on_update': lambda _: self.tick_set_render_group()
                   })
            else:
                self.send_event('E_DEL_MATERIAL_STATUS', 'ComFlag_see_through_outline')
        return True

    def on_enter_mecha_action_end(self, *args):
        model = self.ev_g_model()
        if model and model.valid and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            if self._save_outline_flag:
                model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', OUTLINE_ALPHA)

    def tick_set_render_group(self):
        model = self.ev_g_model()
        if model and model.valid:
            model.set_rendergroup_and_priority(3, 0)

    def on_del_eagle_flag(self, creator_id, is_client_owner):
        flag_type = self._creators.get(creator_id, None)
        if flag_type is None:
            return
        else:
            del self._creators[creator_id]
            if flag_type in FLAG_PATH:
                self._del_attacked_flag()
            else:
                self.set_is_outline(False)
            return

    def on_block_flag(self, block):
        self._block = block
        if block:
            creator_ids = six_ex.keys(self._creators)
            for creator_id in creator_ids:
                self.on_del_eagle_flag(creator_id, None)

        return

    def on_show_battle_broadcast(self, *args):
        global_data.emgr.battle_broadcast_event.emit(*args)