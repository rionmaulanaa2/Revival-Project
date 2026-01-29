# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBeacon8031Appearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gutils.dress_utils import get_mecha_model_path, DEFAULT_CLOTHING_ID
from logic.gcommon.item.item_const import MECHA_FASHION_KEY
from logic.gutils.mecha_skin_utils import get_accurate_mecha_skin_info_from_fasion_data
from logic.gcommon.common_const.mecha_const import BEACON_8031_Y_OFFSET
from logic.gcommon.common_const.skill_const import SKILL_8031_BEACON
from ext_package.ext_decorator import has_skin_ext
from common.cfg import confmgr
import math3d
import world
BEACON_SOCKET_EFFECT_ID = '107'
BEACON_GUIDE_EFFECT_ID = '108'
ENEMY_BEACON_GUIDE_EFFECT_ID = '111'

class ComBeacon8031Appearance(ComBaseModelAppearance):

    def init_from_dict(self, unit_obj, bdict):
        super(ComBeacon8031Appearance, self).init_from_dict(unit_obj, bdict)
        self.owner_id = bdict.get('owner_eid', None)
        mecha_fashion = bdict.get(MECHA_FASHION_KEY, {})
        self.skin_id, self.shiny_weapon_id = get_accurate_mecha_skin_info_from_fasion_data(8031, mecha_fashion)
        self.yaw = bdict.get('yaw', 0)
        self.pos = math3d.vector(*bdict.get('position', (0, 0, 0)))
        self.sd.ref_root_position = math3d.vector(self.pos)
        self.sd.ref_root_position.y -= BEACON_8031_Y_OFFSET
        self.guide_sfx_id = None
        return

    def destroy(self):
        if self.guide_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.guide_sfx_id)
            self.guide_sfx_id = None
        super(ComBeacon8031Appearance, self).destroy()
        return

    def get_model_info(self, unit_obj, bdict):
        if has_skin_ext():
            mecha_model_path = get_mecha_model_path(8031, self.skin_id)
        else:
            mecha_model_path = get_mecha_model_path(8031, DEFAULT_CLOTHING_ID)
        path = mecha_model_path.replace('empty.gim', '/part/gj_xinbiao.gim')
        return (
         path, None, (self.pos, path))

    def _try_create_beacon_sfx(self):
        mecha = self.battle.get_entity(self.owner_id)
        if mecha and mecha.logic:
            mecha_model = mecha.logic.ev_g_model()
            if mecha_model:
                model = self.ev_g_model()
                readonly_effect = mecha.logic.ev_g_mecha_readonly_effect_info()
                for effect_info in readonly_effect[BEACON_SOCKET_EFFECT_ID]:
                    socket_sfx_path = effect_info['final_correspond_path']
                    for socket in effect_info['socket_list']:
                        global_data.sfx_mgr.create_sfx_on_model(socket_sfx_path, model, socket)

                def create_cb(sfx):
                    if mecha_model.valid:
                        sfx.endpos_attach(mecha_model, 'part_point1', True)

                if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self.ev_g_camp_id()):
                    effect_id = BEACON_GUIDE_EFFECT_ID
                else:
                    effect_id = ENEMY_BEACON_GUIDE_EFFECT_ID
                guide_sfx_path = readonly_effect[effect_id][0]['final_correspond_path']
                guide_sfx_socket = readonly_effect[effect_id][0]['socket_list'][0]
                self.guide_sfx_id = global_data.sfx_mgr.create_sfx_on_model(guide_sfx_path, model, guide_sfx_socket, on_create_func=create_cb)
                self.send_event('E_SHOW_BLOOD_SIM_UI')
                return True
        return False

    def on_load_model_complete(self, model, user_data):
        super(ComBeacon8031Appearance, self).on_load_model_complete(model, user_data)
        ext_info = confmgr.get('skill_conf', str(SKILL_8031_BEACON), 'ext_info', default={})
        scale = ext_info.get('beacon_model_scale', 2.0)
        model.scale = math3d.vector(scale, scale, scale)
        socket_matrix = model.get_socket_matrix('fx_xb', world.SPACE_TYPE_LOCAL)
        if socket_matrix:
            socket_offset = socket_matrix.translation
        else:
            socket_offset = math3d.vector(0, 22.5, 0)
        position = self.pos + socket_offset - socket_offset * scale
        self.send_event('E_HUMAN_MODEL_LOADED', model, None)
        model.rotation_matrix = math3d.matrix.make_rotation_y(self.yaw)
        if not self._try_create_beacon_sfx():
            self.need_update = True
        model.play_animation('beacon_open')
        model.position = position
        return

    def tick(self, dt):
        if self._try_create_beacon_sfx():
            self.need_update = False