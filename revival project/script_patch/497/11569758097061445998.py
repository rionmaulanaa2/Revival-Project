# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/BestMechaModelAppearance.py
from __future__ import absolute_import
import game3d
import math3d
import world
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.mecha_skin_utils import MechaSocketResAgent
from common.framework import Functor
from logic.gcommon.common_utils import decal_utils
from logic.gutils.skin_define_utils import load_model_decal_data, load_model_color_data, get_main_skin_id
from logic.gutils.dress_utils import get_mecha_skin_item_no, get_mecha_model_path, get_mecha_model_lod_path
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from .BestRoleModelAppearance import BaseBestModelAppearance
from logic.gutils import skin_define_utils
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
_HASH_force_sun_shadow = game3d.calc_string_hash('force_sun_shadow')
EMPTY_SUBMESH_NAME = 'empty'

class BestMechaModelAppearance(BaseBestModelAppearance):

    def __init__(self, index, chushegntai_model, force_info_list=None):
        mecha_info_list = force_info_list or global_data.battle.get_top_nb_mecha_info() if 1 else force_info_list
        mecha_info = mecha_info_list[index]
        mecha_id = mecha_info[1]
        dict_data = mecha_info[3]
        fashion_data = dict_data.get('fashion', {})
        clothing_id = fashion_data.get(FASHION_POS_SUIT)
        shiny_weapon_id = fashion_data.get(FASHION_POS_WEAPON_SFX, -1)
        custom_skin_data = dict_data.get('custom_skin', {})
        pose = dict_data.get('pose')
        role_name = mecha_info[2]
        obj_id = mecha_info[0]
        super(BestMechaModelAppearance, self).__init__(index, obj_id, role_name, chushegntai_model)
        self.socket_res_agent = MechaSocketResAgent()
        self.load_model(mecha_id, clothing_id, shiny_weapon_id, custom_skin_data, pose)

    def destroy_model(self):
        self.socket_res_agent.destroy()
        super(BestMechaModelAppearance, self).destroy_model()

    def load_model(self, mecha_id, clothing_id, shiny_weapon_id=-1, custom_skin_data={}, pose=None):
        res_path = get_mecha_model_path(mecha_id, clothing_id)
        data = {'mecha_id': mecha_id,'clothing_id': clothing_id,'shiny_weapon_id': shiny_weapon_id,'pose': pose}
        data.update({'custom_skin_data': custom_skin_data})
        mesh_path = get_mecha_model_lod_path(mecha_id, clothing_id, 0, shiny_weapon_id=shiny_weapon_id)
        self.model_id = global_data.model_mgr.create_model_in_scene(res_path, mesh_path_list=[mesh_path], on_create_func=Functor(self.on_load_model_complete, data))

    def on_load_model_complete(self, data, model, *args):
        if not model or not model.valid:
            return
        if not self._chushegntai_model or not self._chushegntai_model.valid:
            self.destroy_model()
            return
        self.model = model
        scale = 1.2
        model.scale = math3d.vector(scale, scale, scale)
        mecha_id = data['mecha_id']
        clothing_id = data['clothing_id']
        shiny_weapon_id = data['shiny_weapon_id']
        custom_skin_data = data['custom_skin_data']
        pose = data['pose']
        self.socket_res_agent.load_skin_model_and_effect(model, clothing_id, shiny_weapon_id)
        model.all_materials.set_var(_HASH_force_sun_shadow, 'force_sun_shadow', 1.0)
        self.add_model_col(model)
        self.update_pos()
        model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        item_id = get_mecha_skin_item_no(data['mecha_id'], data['clothing_id'])
        anim_name = item_utils.get_lobby_item_res_path(pose, skin_id=get_main_skin_id(item_id)) if pose else self.get_play_idle_anim(item_id)
        is_gesture_pose = skin_define_utils.is_mecha_gesture_pose(pose)
        loop = world.PLAY_FLAG_LOOP if is_gesture_pose else world.PLAY_FLAG_NO_LOOP
        args = [anim_name, -1, world.TRANSIT_TYPE_NONE, 0, loop]
        self.socket_res_agent.play_animation(*args)
        self.load_decal_data(model, clothing_id, custom_skin_data.get('decal', []))
        self.load_color_data(model, clothing_id, custom_skin_data.get('color', {}))

    def get_play_idle_anim(self, item_id):
        item_conf = confmgr.get('lobby_item', str(item_id), default={})
        lobby_ani_name = item_conf.get('lobby_ani_name', [])
        return lobby_ani_name or 'shutdown_01'

    def load_decal_data(self, model, skin_id, decal_list):
        if decal_list and len(decal_list[0]) < 9:
            decal_list = decal_utils.decode_decal_list(decal_list)
        load_model_decal_data(model, skin_id, decal_list, lod_level=0, create_high_quality_decal=True)

    def load_color_data(self, model, skin_id, color_dict):
        if color_dict and isinstance(color_dict, dict):
            color_dict = decal_utils.decode_color(color_dict)
        load_model_color_data(model, skin_id, color_dict)

    def destroy(self):
        super(BestMechaModelAppearance, self).destroy()