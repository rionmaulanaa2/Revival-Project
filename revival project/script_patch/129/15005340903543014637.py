# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComArtCheckLodHuman.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import game3d
from logic.gutils.role_skin_utils import clear_editor_model_effect_and_model, load_editor_model_effect_and_model

class ComArtCheckLodHuman(UnitCom):
    BIND_EVENT = {'E_CHARACTER_ATTR': '_change_character_attr',
       'E_HUMAN_MODEL_LOADED': 'on_humman_model_load',
       'E_CHANGE_ANIM_MOVE_DIR': 'change_anim_move_dir',
       'E_CHANGE_MODEL': 'change_model_fashion'
       }

    def __init__(self):
        super(ComArtCheckLodHuman, self).__init__()
        self._lod_level = 'l'
        self._cur_body_res_path = 'character/11/2000/l.gim'
        self._cur_head_res_path = 'character/11/2000/parts/l_head.gim'
        self._last_body_res_path = ''
        self._last_head_res_path = ''
        self.sockets_data = []

    def init_from_dict(self, unit_obj, bdict):
        self._role_id = bdict['role_id']
        if self._role_id == 11:
            self._cur_body_res_path = 'character/11/2000/l.gim'
            self._cur_head_res_path = 'character/11/2000/parts/l_head.gim'
        else:
            self._cur_body_res_path = 'character/12/2000/l.gim'
            self._cur_head_res_path = 'character/12/2000/parts/l_head.gim'
        super(ComArtCheckLodHuman, self).init_from_dict(unit_obj, bdict)

    def _change_character_attr(self, name, *args):
        pass

    def on_humman_model_load(self, is_log=False, *args):
        model = self.ev_g_model()
        if not model:
            return
        self.load_lod_model()

    def change_model_lod(self, lod_level):
        self._lod_level = lod_level

    def change_model_fashion(self, model_data):
        res_path = model_data['m_path']
        lod_level = model_data['lod']
        self.sockets_data = model_data['sockets_data']
        self._cur_head_res_path = res_path.replace('empty.gim', 'parts/{}_head.gim'.format(lod_level))
        self._cur_body_res_path = res_path.replace('empty.gim', '{}.gim'.format(lod_level))
        self.load_lod_model(lod_level)

    def load_lod_model(self, lod_level='l'):
        self._lod_level = lod_level
        clear_editor_model_effect_and_model(self.ev_g_model())
        self.ev_g_load_model(self._cur_body_res_path, self.on_add_fullbody_model, lod_level, sync_priority=game3d.ASYNC_HIGH)

    def on_add_fullbody_model(self, load_model, lod_level, *args):
        model = self.ev_g_model()
        if not model:
            return
        if self._last_body_res_path:
            model.remove_mesh(self._last_body_res_path)
            self.send_event('E_DESTROY_BODY_SOCKET_ANIMATOR')
        self._last_body_res_path = self._cur_body_res_path
        model.add_mesh(self._cur_body_res_path)
        self.send_event('E_INIT_BODY_SOCKET_ANIMATOR')
        self.send_event('E_INIT_SPRING_ANI')
        self.send_event('E_HUMAN_LOD_LOADED', model)
        self.ev_g_load_model(self._cur_head_res_path, self.on_add_head_model, lod_level, sync_priority=game3d.ASYNC_HIGH)

    def on_add_head_model(self, load_model, *args):
        model = self.ev_g_model()
        if not model:
            return
        if self._last_head_res_path:
            model.remove_mesh(self._last_head_res_path)
            self.send_event('E_DESTROY_HAIR_ANIMATOR')
        self._last_head_res_path = self._cur_head_res_path
        model.add_mesh(self._cur_head_res_path)
        self.send_event('E_INIT_HAIR_MODEL')
        self.send_event('E_INIT_SPRING_ANI')
        load_editor_model_effect_and_model(model, self.sockets_data, self._lod_level)

    def change_anim_move_dir(self, dir_x, dir_y, *args):
        pass