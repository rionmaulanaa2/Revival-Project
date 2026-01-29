# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_model/ComBaseModel.py
from __future__ import absolute_import
import math3d
import world
from logic.gutils import item_utils
from logic.gcommon.component.UnitCom import UnitCom

class ComBaseModel(UnitCom):
    BIND_EVENT = {'G_MODEL': '_get_model',
       'G_MODEL_POSITION': '_get_model_pos',
       'G_POSITION': '_get_model_pos',
       'E_POSITION': '_set_model_pos',
       'E_SHOW_MODEL': '_show_model',
       'E_HIDE_MODEL': '_hide_model'
       }
    ExtendFuncNames = [
     'is_model_valid',
     'get_model_obj',
     'set_model_attr',
     'get_model_attr',
     'call_model_func',
     'set_model_destroy_handler']

    def __init__(self):
        super(ComBaseModel, self).__init__()
        self._registered_events = {}
        self._imp_init()
        self._clear_socket = True

    def init_from_dict(self, unit_obj, bdict):
        super(ComBaseModel, self).init_from_dict(unit_obj, bdict)
        self.item_id = bdict.get('item_id', -1)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._set_model_pos)

    def reuse(self, share_data):
        super(ComBaseModel, self).reuse(share_data)
        self._imp_init()

    def cache(self):
        self._destroy_model()
        super(ComBaseModel, self).cache()

    def register_single_event(self, event_key, func):
        emgr = global_data.emgr
        econf = {event_key: func
           }
        emgr.bind_events(econf)
        self._registered_events[event_key] = func

    def unregister_all_events(self):
        emgr = global_data.emgr
        if self._registered_events:
            emgr.unbind_events(self._registered_events)
        self._registered_events = {}

    def on_camera_player_setted(self, *args):
        self.refresh_dogtab_visible()

    def on_post_init_complete(self, bdict):
        super(ComBaseModel, self).on_post_init_complete(bdict)
        if item_utils.is_dogtag_by_item_id(self.item_id):
            self.register_single_event('scene_camera_switch_player_setted_event', self.on_camera_player_setted)
        if self.ev_g_is_pve_item():
            self._clear_socket = False
        model_path, mesh_path_list = self.unit_obj.get_model_file_config()

        def create_cb(model, use_idx):
            if not self.is_enable(use_idx):
                global_data.model_mgr.remove_model(model, self._clear_socket)
                return
            self._on_model_created(model)

        func = lambda model, use_idx=self.use_idx, *args: create_cb(model, use_idx)
        global_data.model_mgr.create_model(model_path, mesh_path_list, on_create_func=func)

    def destroy(self):
        self.unregister_all_events()
        self._destroy_model()
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._set_model_pos)
        super(ComBaseModel, self).destroy()

    def _get_model(self):
        return self._model

    def _get_model_pos(self):
        if self._model and self._model.valid:
            return self._model.world_position
        else:
            return self._model_pos

    def _set_model_pos(self, pos):
        self._model_pos = pos
        if self._model and self._model.valid:
            self._model.world_position = pos

    def refresh_dogtab_visible(self):
        if not global_data.cam_lplayer or not self._model or not item_utils.is_dogtag_by_item_id(self.item_id):
            return
        pickable_item_data = self.ev_g_pick_data()
        faction_id = pickable_item_data.get('faction_id', -1)
        self._dogtag_visible = faction_id < 0 or global_data.cam_lplayer.ev_g_is_campmate(faction_id)
        self._model.visible = self._model_visible and self._dogtag_visible

    def _show_model(self, key='__default__', count=1):
        if self._model:
            self._model_visible = True
            self._model.visible = self._model_visible and self._dogtag_visible

    def _hide_model(self, key='__default__', count=1):
        if self._model:
            self._model_visible = False
            self._model.visible = self._model_visible

    def is_model_valid(self):
        return self._model and self._model.valid

    def get_model_obj(self):
        return self._model

    def set_model_attr(self, name, value):
        if self._model and self._model.valid:
            setattr(self._model, name, value)

    def get_model_attr(self, name):
        if self._model and self._model.valid:
            return getattr(self._model, name)

    def call_model_func(self, name, *args, **kwargs):
        if self._model and self._model.valid:
            return getattr(self._model, name)(*args, **kwargs)

    def set_model_destroy_handler(self, func):
        self._destroy_handler = func

    def _imp_init(self):
        self._model = None
        self._model_pos = math3d.vector(0, 0, 0)
        self._model_show_dict = {}
        self._destroy_handler = None
        self._dogtag_visible = True
        self._model_visible = True
        return

    def _on_model_created(self, model):
        scene = world.get_active_scene()
        if not scene:
            return
        scene.add_object(model)
        self._model = model
        if hasattr(model, 'decal_recievable'):
            model.decal_recievable = False
        self.refresh_dogtab_visible()
        self.send_event('E_MODEL_LOADED', model)

    def _destroy_model(self):
        self.send_event('E_BEFORE_DESTROY_MODEL', self._model)
        if self._model:
            if self._destroy_handler:
                self._destroy_handler(self._model)
            else:
                global_data.model_mgr.remove_model(self._model, self._clear_socket)
        self._model = None
        return