# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTVAppearance.py
from __future__ import absolute_import
import math3d
import game3d
import math
import world
import time
from common.cfg import confmgr
from .ComBaseModelAppearance import ComBaseModelAppearance
import render
from logic.client.path_utils import DEFAULT_TV_PATH
_HASH = game3d.calc_string_hash('Tex0')
SFX_PLAY_INTERVAL = 5

class ComTVAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ADD_TO_TV_MANAGER': 'on_add_to_tv_manager',
       'E_HIDE_MODEL': '_hide_model',
       'E_SHOW_MODEL': '_show_model',
       'E_SCENE_ADD_TV_ENTITY': '_scene_add_television_entity',
       'E_UPDATE_TV_INFO': '_update_tv_info'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComTVAppearance, self).init_from_dict(unit_obj, bdict)
        self._tv_id = bdict.get('tv_id', 1)
        self._is_client = bdict.get('is_client', False)
        self._cur_scene = bdict.get('scene')
        self._is_show = bdict.get('is_show', True)
        self._show_info = bdict.get('show_info', {})
        self._sub_model_pos_off = bdict.get('sub_model_pos_off', (0, 0, 0))
        self._sub_model_path = bdict.get('sub_model_path')
        self._sub_sfx_path = bdict.get('sub_sfx_path')
        self._model_transparent = bdict.get('model_transparent')
        self._rendergroup_and_priority = bdict.get('rendergroup_and_priority')
        self._channel_id = None
        self._sub_model = None
        self._sub_model_id = None
        self._sub_sfx_id = None
        self._tex = None
        self._last_sfx_time = 0
        self.need_update = False
        return

    def get_model_info(self, unit_obj, bdict):
        if self._is_client:
            tv_e_conf = confmgr.get('tv_conf', 'cl_tv_entity', 'Content', default={})
        else:
            tv_e_conf = confmgr.get('tv_conf', 'tv_entity', 'Content', default={})
        tv_c_conf = confmgr.get('tv_conf', 'tv_channel', 'Content', default={})
        channel_id = tv_e_conf.get(str(self._tv_id), {}).get('channel_id', 1)
        pos = tv_e_conf.get(str(self._tv_id), {}).get('pos', [0, 0, 0])
        rot = tv_e_conf.get(str(self._tv_id), {}).get('rot', [0, 0, 0, 1])
        if rot is None:
            rot = [0, 0, 0, 1] if 1 else rot
            model_path = tv_e_conf.get(str(self._tv_id), {}).get('model_path', '')
            model_path = model_path or tv_c_conf.get(str(channel_id), {}).get('model_path', DEFAULT_TV_PATH)
        model_scale = tv_e_conf.get(str(self._tv_id), {}).get('scale', [1, 1, 1])
        self._tv_sfx_path = tv_c_conf.get(str(channel_id), {}).get('sfx_path')
        self._org_tech = tv_c_conf.get(str(channel_id), {}).get('org_tech')
        return (
         model_path, None, (pos, rot, model_scale, int(channel_id), bdict))

    @property
    def scene(self):
        if self._cur_scene and self._cur_scene():
            return self._cur_scene()
        return global_data.game_mgr.scene

    def on_load_model_complete(self, model, userdata):
        pos, rot, scale, self._channel_id = (
         userdata[0], userdata[1], userdata[2], userdata[3])
        original_pos = math3d.vector(pos[0], pos[1], pos[2])
        model.scale = math3d.vector(scale[0], scale[1], scale[2])
        mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))
        model.world_position = original_pos
        model.rotation_matrix = mat
        if self._rendergroup_and_priority:
            model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, self._rendergroup_and_priority)
        self.model.visible = self._is_show
        if self._model_transparent:
            self.model.enable_prez_transparent(True, self._model_transparent)
        self._scene_add_television_entity()
        real_pos = math3d.vector(pos[0] + self._sub_model_pos_off[0], pos[1] + self._sub_model_pos_off[1], pos[2] + self._sub_model_pos_off[2])
        if self._sub_model_path:

            def create_cb--- This code section failed: ---

  96       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_is_show'
           6  LOAD_FAST             0  'model'
           9  STORE_ATTR            1  'visible'

  97      12  LOAD_FAST             0  'model'
          15  LOAD_DEREF            0  'self'
          18  STORE_ATTR            2  '_sub_model'

  99      21  LOAD_DEREF            0  'self'
          24  LOAD_ATTR             3  '_sub_sfx_path'
          27  POP_JUMP_IF_FALSE   109  'to 109'

 100      30  LOAD_CLOSURE          0  'self'
          36  LOAD_CONST               '<code_object create_sfx_cb>'
          39  MAKE_CLOSURE_0        0 
          42  STORE_FAST            1  'create_sfx_cb'

 102      45  LOAD_DEREF            0  'self'
          48  LOAD_ATTR             4  '_sub_sfx_id'
          51  JUMP_IF_FALSE_OR_POP    72  'to 72'
          54  LOAD_GLOBAL           5  'global_data'
          57  LOAD_ATTR             6  'sfx_mgr'
          60  LOAD_ATTR             7  'remove_sfx_by_id'
          63  LOAD_DEREF            0  'self'
          66  LOAD_ATTR             4  '_sub_sfx_id'
          69  CALL_FUNCTION_1       1 
        72_0  COME_FROM                '51'
          72  POP_TOP          

 103      73  LOAD_GLOBAL           5  'global_data'
          76  LOAD_ATTR             6  'sfx_mgr'
          79  LOAD_ATTR             8  'create_sfx_on_model'
          82  LOAD_DEREF            0  'self'
          85  LOAD_ATTR             3  '_sub_sfx_path'
          88  LOAD_ATTR             2  '_sub_model'
          91  LOAD_CONST            3  'on_create_func'
          94  LOAD_FAST             1  'create_sfx_cb'
          97  CALL_FUNCTION_259   259 
         100  LOAD_DEREF            0  'self'
         103  STORE_ATTR            4  '_sub_sfx_id'
         106  JUMP_FORWARD          0  'to 109'
       109_0  COME_FROM                '106'

Parse error at or near `CALL_FUNCTION_259' instruction at offset 97

            self._sub_model_id and global_data.model_mgr.remove_model_by_id(self._sub_model_id)
            self._sub_model_id = global_data.model_mgr.create_model_in_scene(self._sub_model_path, real_pos, on_create_func=create_cb)
        self.need_update = self._is_show and bool(self._tv_sfx_path)

    def _scene_add_television_entity(self):
        if self._channel_id is None:
            return
        else:
            global_data.emgr.scene_add_television_entity.emit(self.unit_obj, self._channel_id, self._is_show, self._show_info)
            return

    def _on_play_tv_sfx(self):
        if not self.model or not self.model.valid:
            return
        if not self.model.is_visible_in_this_frame() or not self.model.visible:
            return
        if not self._tv_sfx_path:
            return

        def cb(*args):
            if self._tex and self.model and self.model.valid:
                self.model.all_materials.set_technique(1, self._org_tech)
                self.model.all_materials.set_texture(_HASH, 'Tex0', self._tex)

        def cb2(*args):
            if self._tex and self.model and self.model.valid:
                self.model.all_materials.set_texture(_HASH, 'Tex0', self._tex)

        global_data.sfx_mgr.create_sfx_on_model(self._tv_sfx_path, self.model, 'fx_root', on_create_func=cb2, on_remove_func=cb)

    def on_add_to_tv_manager(self, tex):
        self._tex = tex
        self.model.all_materials.set_texture(_HASH, 'Tex0', tex)

    def _show_model(self):
        if self.model and self.model.valid:
            self.model.visible = True
        if self._sub_model:
            self._sub_model.visible = True
        self.need_update = True and bool(self._tv_sfx_path)

    def _hide_model(self):
        if self.model and self.model.valid:
            self.model.visible = False
        if self._sub_model:
            self._sub_model.visible = False
        self.need_update = False

    def _update_tv_info(self, info):
        self._is_show = info.get('is_show', True)
        self._show_info = info.get('show_info', {})
        if self.model:
            self.model.visible = self._is_show
            global_data.emgr.update_tv_channel.emit([(self._channel_id, self._show_info)])
        if self._sub_model:
            self._sub_model.visible = self._is_show
        self.need_update = self._is_show and bool(self._tv_sfx_path)

    def tick(self, delta):
        if time.time() - self._last_sfx_time > SFX_PLAY_INTERVAL:
            self._on_play_tv_sfx()
            self._last_sfx_time = time.time()

    def on_model_destroy(self):
        global_data.emgr.scene_remove_television_entity.emit(self.unit_obj.id)
        self._sub_model_id and global_data.model_mgr.remove_model_by_id(self._sub_model_id)
        self._sub_model_id = None
        self._sub_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
        self._sub_sfx_id = None
        self._sub_model = None
        return