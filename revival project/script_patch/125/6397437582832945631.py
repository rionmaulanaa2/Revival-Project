# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMechaChuChang.py
from __future__ import absolute_import
import game3d
import math3d
import world
import math
from . import ScenePart
from common.cfg import confmgr
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils import item_utils
from common.utils import pc_platform_utils

class PartMechaChuChang(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartMechaChuChang, self).__init__(scene, name, False)
        self.events_binded = False
        self.mecha_skin_id = None
        return

    def on_enter(self):
        self.scene().active_camera.z_range = (1, 100000)
        self.process_event(True)

    def on_exit(self):
        global_data.ui_mgr.close_ui('MechaChuChangUI')
        self.process_event(False)

    def on_pause(self, flag):
        self.process_event(not flag)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'set_mecha_chuchang_data': self.on_set_mecha_chuchang_data,
           'set_mecha_chuchang_trk': self.on_set_mecha_chuchang_trk,
           'get_mecha_chuchang_data': self.on_get_mecha_chuchang_data,
           'lobby_high_model_changed': self.on_load_model_success,
           'try_end_chuchang_scene_directly': self.on_end_chuchang_trk_directly
           }
        if is_bind == self.events_binded:
            return
        self.events_binded = is_bind
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_set_mecha_chuchang_data(self, mecha_skin_id):
        self.mecha_skin_id = mecha_skin_id
        item_type = item_utils.get_lobby_item_type(mecha_skin_id)
        cur_skin_cnf = None
        if item_type == L_ITEM_TYPE_MECHA_SKIN:
            cur_skin_cnf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(mecha_skin_id))
        elif item_type == L_ITEM_TYPE_ROLE_SKIN:
            cur_skin_cnf = confmgr.get('role_info', 'RoleSkin', 'Content', str(mecha_skin_id))
        self.on_set_mecha_chuchang_trk(cur_skin_cnf.get('chuchang_trk'), item_type == L_ITEM_TYPE_MECHA_SKIN and cur_skin_cnf.get('adapt_light'))
        return

    def on_set_mecha_chuchang_trk(self, chuchang_trk, adapt_light=False):
        trk = global_data.track_cache.create_track(chuchang_trk)
        camera = self.scene().active_camera
        if trk.has_fov_info():
            camera.fov = trk.get_fov(0)
        from logic.gutils.CameraHelper import get_left_hand_trans
        transform = get_left_hand_trans(trk.get_transform(0))
        camera.world_rotation_matrix = transform.rotation
        camera.world_position = transform.translation
        if adapt_light:
            last_key_time = trk.get_key_time(trk.get_key_count() - 1)
            last_key_transform = get_left_hand_trans(trk.get_transform(last_key_time))
            light = self.scene().get_light('dir_light')
            new_world_rotation_matrix = last_key_transform.rotation.make_rotation_x(math.pi / 4)
            light.world_rotation_matrix = new_world_rotation_matrix.make_rotation_y(math.pi / 4)

    def on_get_mecha_chuchang_data(self):
        if self.get_scene() == global_data.game_mgr.scene:
            return self.mecha_skin_id
        else:
            return None
            return None

    def on_load_model_success(self, model):
        if model.filename in ('character\\15\\2004\\h.gim', 'character\\15\\2004_skin_s1\\h.gim',
                              'character\\15\\2004_skin_s2\\h.gim'):

            def call_back(model_cb_bear):
                if not model or not model.valid:
                    global_data.model_mgr.remove_model(model_cb_bear)
                    return
                pc_platform_utils.set_model_write_alpha(model_cb_bear, True, 1.0)
                model_cb_bear.world_position = math3d.vector(-9.426, 9.804, 13.916)
                w_rot = math3d.matrix()
                w_rot.set_all(-0.229, -0.952, -0.204, 0.0, -0.845, -0.298, -0.443, 0.0, 0.482, 0.071, -0.873, 0.0, 0.0, 0.0, 0.0, 0.0)
                model_cb_bear.world_rotation_matrix = w_rot

            model_bear = global_data.model_mgr.create_model_in_scene('character/15/2004/parts/bear.gim', on_create_func=call_back)

            def anim_call_back(model, anim_name, key, *args):
                global_data.model_mgr.remove_model_by_id(model_bear)

            model.register_anim_key_event('stand_show_15_2004', 'switch_bear', anim_call_back)
        self.scene().set_vegetation_visible_range(100000)
        item_type = item_utils.get_lobby_item_type(self.mecha_skin_id)
        cur_skin_cnf = None
        if item_type == L_ITEM_TYPE_MECHA_SKIN:
            cur_skin_cnf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(self.mecha_skin_id))
        elif item_type == L_ITEM_TYPE_ROLE_SKIN:
            cur_skin_cnf = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.mecha_skin_id))
        if not cur_skin_cnf:
            return
        else:
            anim_name = cur_skin_cnf.get('chuchang_anim')
            chuchang_trk = cur_skin_cnf.get('chuchang_trk')
            if anim_name:
                if model.has_anim(anim_name):
                    end_event = cur_skin_cnf.get('chuchang_end_event', None)
                    if end_event:
                        model.register_anim_key_event(anim_name, end_event, self.end_show_animation)
                    else:
                        model.register_anim_key_event(anim_name, 'end', self.end_show_animation)
                    global_data.emgr.play_camera_trk_event.emit(chuchang_trk, left_hand_coordinate=False)
                else:
                    self.end_show_animation()
            return

    def end_show_animation(self, *args):
        if self.get_scene() != global_data.game_mgr.scene:
            return
        if not global_data.video_player.is_in_init_state():
            return

        def pass_anim_callback():
            if self.get_scene() == global_data.game_mgr.scene:
                global_data.emgr.end_mecha_chuchang_scene.emit()

        transition_ui = global_data.ui_mgr.get_ui('BlackFadeUI')
        if not transition_ui:
            from logic.comsys.mecha_display.BlackFadeUI import BlackFadeUI
            transition_ui = BlackFadeUI()
        transition_ui.show_transition(pass_anim_callback)

    def on_end_chuchang_trk_directly(self):
        if self.mecha_skin_id:
            if self.get_scene() == global_data.game_mgr.scene:
                global_data.emgr.end_mecha_chuchang_scene.emit()