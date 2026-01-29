# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSettle.py
from __future__ import absolute_import
import six
import world
from . import ScenePart
from logic.gutils.scene_utils import UI_SCENE_BOX_PREFIX
from logic.gcommon.const import DEFAULT_ROLE_ID
from logic.gcommon.item.item_const import LOD_L

class PartSettle(ScenePart.ScenePart):

    def on_pre_load(self):
        self._model_num = 0
        self._avatar_models = []
        self._avatar_dressers = []
        self._max_index = 3

    def on_enter(self):
        scene = self.scene()
        cam = scene.active_camera
        cam.transformation = scene.get_preset_camera('cam_ziji')

    def on_exit(self):
        global_data.ui_mgr.close_ui('EndEntireTeamUI')
        for model in self._avatar_models:
            if model and model.valid:
                model.destroy()

        self._avatar_models = None
        self._avatar_dressers = None
        return

    def add_avatar_model(self, role=DEFAULT_ROLE_ID, dress_dict={}):
        self._model_num += 1
        index = self._model_num
        from logic.gutils import dress_utils
        from logic.gcommon.item.item_const import DRESS_POS_FACE
        path = dress_utils.get_dress_path_by_item_no_and_part_id(dress_dict.get(DRESS_POS_FACE), DRESS_POS_FACE, role, lod=LOD_L)
        world.create_model_async(path, self._on_model_loaded, (index, role, dress_dict))

    def _on_model_loaded(self, model, udata, current_task):
        index, role, clothing_dict = udata
        scene = self.scene()
        if not scene or not scene.valid:
            return
        else:
            scene.add_object(model)
            self._avatar_models.append(model)
            pos_model = scene.get_model('%s%d' % (UI_SCENE_BOX_PREFIX, index))
            model.transformation = pos_model.transformation
            model.play_animation('s_emptyhand_idle', -1.0, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)
            from logic.gutils import dress_utils
            from logic.gcommon.item.item_const import DRESS_POS_FACE
            dress_dict = {}
            for dress_pos, item_no in six.iteritems(clothing_dict):
                dress_dict[dress_pos] = {'item_id': item_no}

            suit_id = dress_utils.get_suit_id_by_clothing(dress_dict, role)
            dresser = dress_utils.DresserModel(model, role, lod=LOD_L, dress_dict={DRESS_POS_FACE: None}, suit_id=suit_id)
            model.visible = False

            def callback(*args):
                model.visible = True

            dresser.dress(dress_dict, callback)
            self._avatar_dressers.append(dresser)
            return