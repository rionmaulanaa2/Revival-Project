# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPreview.py
from __future__ import absolute_import
import six_ex
from . import ScenePart
from common.cfg import confmgr
import logic.units.LDoll as LDoll

class DummyEntity(object):

    def __init__(self, id):
        super(DummyEntity, self).__init__()
        self.id = id


class DummyBattle(object):

    def __init__(self, scn):
        super(DummyBattle, self).__init__()
        self.scn = scn

    def get_scene(self):
        return self.scn


class PartPreview(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartPreview, self).__init__(scene, name)
        self.player = None
        self._dummy_battle = None
        return

    def get_init_position(self):
        return self.scene().get_preset_camera('cam').translation

    def get_doll_data(self, model_id=None):
        conf = confmgr.get('action_preview')
        conf = conf.get('ModelConfig', {}).get('Content', {})
        model_path = None
        if not model_id:
            model_id = sorted(six_ex.keys(conf))[0]
        model_path = conf.get(model_id).get('model_path')
        return (
         model_id, model_path)

    def get_animator_path(self):
        return 'animator_conf/mecha/common.xml'

    def bind_camera(self, unit):
        global_data.emgr.scene_camera_player_setted_event.emit(unit)

    def unbind_camera(self, unit):
        global_data.emgr.scene_camera_player_setted_event.emit(None)
        return

    def bind_ctrl(self, unit):
        global_data.emgr.scene_player_setted_event.emit(unit)

    def unbind_ctrl(self, unit):
        global_data.emgr.scene_player_setted_event.emit(None)
        return

    def clear_player(self):
        if self.player:
            self.unbind_camera(self.player)
            self.unbind_ctrl(self.player)
            self.player.destroy()
            self.player = None
        return

    def reload_player(self, model_id=None):
        model_id, model_path = self.get_doll_data(model_id)
        self.clear_player()
        self.player = LDoll.LDoll(DummyEntity(0), self._dummy_battle)
        dict_data = {'model_id': model_id,
           'model': model_path,
           'animator': self.get_animator_path(),
           'use_phys': 1,
           'position': (15235, 350, 2342)
           }
        self.player.regist_event('E_HUMAN_MODEL_LOADED', self.on_model_loaded)
        self.player.init_from_dict(dict_data)

    def on_model_loaded(self, model, *args):
        self.bind_camera(self.player)
        self.bind_ctrl(self.player)
        global_data.ui_mgr.show_ui('ActionPreviewUI', 'logic.comsys.action_preview')

    def on_enter(self):
        self.process_bind_events(True)
        scn = self.scene()
        self._dummy_battle = DummyBattle(scn)
        self.reload_player()

    def on_exit(self):
        self.clear_player()
        self.process_bind_events(False)

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'change_model_preview': self.on_change_model
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_change_model(self, model_id):
        self.reload_player(model_id)