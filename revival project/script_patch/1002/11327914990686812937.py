# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/GlideSceneHelper.py
from common.cfg import confmgr
from ext_package.ext_decorator import has_skin_ext
from logic.gutils import lobby_model_display_utils
import math3d

class GlideSceneHelper(object):

    def __init__(self, camera_key='item_books'):
        self.camera_key = camera_key
        self.skin_id = None
        self._cur_select_glide_effect_id = None
        self.is_role_model_finish = False
        self._has_finished_camera = False
        self._update_timer = None
        self._camera_timer = None
        self.init_yaw = 2.832
        self.init_pitch = 0.436
        return

    def update_init_rotation(self, yaw, pitch):
        self.init_yaw = yaw
        self.init_pitch = pitch

    def destroy(self):
        self.clear()

    def clear(self):
        self.unregister_motion_timer()
        self.unregister_camera_timer()
        self._has_finished_camera = False

    def update_skin_and_glide(self, skin_id, glide_id):
        if self.is_role_model_finish:
            global_data.emgr.add_glide_sfx_for_lobby_model_event.emit(self.skin_id, glide_id, 'glide')
        self.skin_id = skin_id
        self._cur_select_glide_effect_id = glide_id

    def show_player_model(self, skin_no, glide_id, role_id=None):
        self.skin_id = skin_no
        self._cur_select_glide_effect_id = glide_id
        from logic.gcommon.item import item_const
        if not role_id:
            role_id = global_data.player.get_role()
        role_data = global_data.player.get_item_by_no(role_id)
        default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')
        if has_skin_ext():
            fashion_data = role_data.get_fashion() if role_data else {}
            dressed_clothing_id = fashion_data.get(item_const.FASHION_POS_SUIT, default_skin)
            role_head_no = fashion_data.get(item_const.FASHION_POS_HEADWEAR, None)
            bag_id = fashion_data.get(item_const.FASHION_POS_BACK, None)
            suit_id = fashion_data.get(item_const.FASHION_POS_SUIT_2, None)
            other_pendants = [ fashion_data.get(pos) for pos in item_const.FASHION_OTHER_PENDANT_LIST ]
            role_model_data = lobby_model_display_utils.get_lobby_model_data(dressed_clothing_id, is_add_empty=True, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants, lod_level='l')
        else:
            dressed_clothing_id = default_skin
            role_model_data = lobby_model_display_utils.get_lobby_model_data(dressed_clothing_id, is_add_empty=True, lod_level='l')

        def load_role_model_finish(model):
            if self.is_role_model_finish == str(model):
                return
            self.is_role_model_finish = str(model)
            self.init_circular_fail_motion(model)
            global_data.emgr.add_glide_sfx_for_lobby_model_event.emit(skin_no, glide_id, 'glide')

        for data in role_model_data:
            data['model_scale'] = data.get('model_scale', 1.0) * 0.3
            data['show_anim'] = 'glide_move_f'
            data['force_end_ani_loop'] = True
            data['end_anim'] = 'glide_move_f'

        self.is_role_model_finish = None
        global_data.emgr.change_model_display_scene_item.emit(role_model_data, create_callback=load_role_model_finish)
        return

    def init_circular_fail_motion(self, model):
        import world
        self._motion_start_time = global_data.game_time
        self.register_motion_timer()
        self.update_camera_show(model)

    def unregister_camera_timer(self):
        if self._camera_timer:
            global_data.game_mgr.unregister_logic_timer(self._camera_timer)
            self._camera_timer = None
        return

    def update_camera_show(self, model):
        if self._has_finished_camera:
            return
        import common.utils.timer as timer

        def camera_show_helper():
            book_key = self.camera_key
            init_yaw = self.init_yaw
            init_pitch = self.init_pitch
            self._camera_timer = None
            if model and model.valid:
                if model.cur_anim_name == 'glide_move_f':
                    new_y = model.bounding_box.y * 2
                    offset = (new_y - 24) / 2.0
                    self._has_finished_camera = True
                    global_data.emgr.update_display_camera_parameter.emit(book_key, init_yaw, init_pitch, offset, offset)
                else:
                    global_data.emgr.update_display_camera_parameter.emit(book_key, init_yaw, init_pitch, 0, 0)
                    self.unregister_camera_timer()
                    self._camera_timer = global_data.game_mgr.register_logic_timer(camera_show_helper, interval=0.03, times=1, mode=timer.CLOCK)
            return

        camera_show_helper()

    def register_motion_timer(self):
        import common.utils.timer as timer
        self.unregister_motion_timer()
        self._update_timer = global_data.game_mgr.register_logic_timer(self.update_motion_action, interval=1, times=-1, mode=timer.LOGIC, timedelta=True)

    def unregister_motion_timer(self):
        if self._update_timer:
            global_data.game_mgr.unregister_logic_timer(self._update_timer)
            self._update_timer = None
        return

    def update_motion_action(self, dt):
        import math
        radius = 1800
        speed = 0.02

        def get_pos_by_time(t):
            theta = speed * t
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            t = 0
            y = 0
            return (
             x, y, z)

        time_delta = global_data.game_time - self._motion_start_time
        pos_tuple = tuple(get_pos_by_time(time_delta))
        global_data.emgr.change_model_display_off_position.emit(pos_tuple, False)
        theta_total = speed * time_delta % (2 * math.pi)
        global_data.emgr.set_model_display_rotate_euler.emit(math3d.vector(0, math.degrees(-theta_total), 0))
        pos_tuple = (pos_tuple[0], pos_tuple[1] - 15, pos_tuple[2])
        global_data.emgr.update_display_camera_target_position.emit(time_delta, pos_tuple)
        light = global_data.game_mgr.scene.get_light('dir_light')
        if light:
            light.direction = math3d.vector(0.697, -theta_total, -0.536) * math3d.matrix.make_rotation_y(math.pi)