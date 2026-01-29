# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/ar/ARMainUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
__author__ = 'lincaizhao'
import os
import world
import render
import math3d
import game3d
from cocosui import cc, ccui
import ar
import C_file
SHADER_VS = 'common/shader/cocosui/positiontexturecolor_nomvp.vs'
SHADER_PS_IOS = 'common/shader/cocosui/positiontexturecolor_nomvp_y_cbcr.ps'
SHADER_PS_ANDROID = 'common/shader/cocosui/positiontexturecolor_nomvp_yuv.ps'
APPKEY = 'AR0-84582cc5d96718ad31f3035ae4f1ba5af8daf4e94a9ee244bc86afc29945dcdc'
SECRET = '491f7022a315f81164623119dc72e8450abe9d6c1137886f9333b73610d3d5b3'
CONFIG = 'ar_scenes/0502/config'
ASSETS = 'ar_scenes/0502/assets'
CONFIGS = [
 ('2DMarker', 'ar_scenes/0502/config', 'ar_scenes/0502/assets')]
MODEL_PATH = 'character/11/2000/l.gim'
BACKGROUND_UI_PATH = 'gui/ui_res_2/ar/bg.png'
GESTURES = ('FIST', 'THUMB', 'INDEX', 'LSHAPE', 'VSHAPE', 'OK', 'PALM', 'HEART', 'ROCK',
            'DHEART')
MAP_PATH = 'ar_map'
CHECK_FILE_DICT = {'assets/device_android_calib.json': 'assets/device_Android_calib.json',
   'assets/device_ios_calib.json': 'assets/device_iOS_calib.json',
   'assets/voc_orb1.yaml': '',
   'assets/voc_orb2.yaml': '',
   'config/config.json': '',
   'readme.txt': ''
   }

class TGame(object):

    def __init__(self):
        pass

    def copy_npk_file_to_document_path(self):
        from common.utils.path import copy_res_file_to_document
        dir_path = 'ar_scenes/0502/'
        file_path = dir_path + '/config/config.json'
        if not C_file.find_res_file(file_path, ''):
            for src_path, dest_path in six_ex.items(CHECK_FILE_DICT):
                if not dest_path:
                    dest_path = src_path
                one_src_file_path = dir_path + '/' + src_path
                one_dest_file_path = dir_path + '/' + dest_path
                copy_res_file_to_document(one_src_file_path, one_dest_file_path)

    def setup(self):
        self.copy_npk_file_to_document_path()
        render.set_background_color(4284506208L)
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        self.log('GL View Size: %s', view.getVisibleSize())
        designSize = view.getDesignResolutionSize()
        self.view_w = designSize.width
        self.view_h = designSize.height
        self.view_center = cc.Vec2(self.view_w / 2, self.view_h / 2)
        self.touch_simulate = [
         (5, 5),
         (
          5, self.view_h - 5),
         (
          self.view_w - 5, 5),
         (
          self.view_w - 5, self.view_h - 5),
         (
          self.view_center.x, self.view_center.y),
         (
          self.view_center.x / 2.0, self.view_center.y / 2.0)]
        self.touch_index = 0
        self.cc_scene = director.getRunningScene()
        director.setDisplayStats(True)
        self.cc_display_layer = ccui.Widget.create()
        self.cc_scene.addChild(self.cc_display_layer)
        self.cc_cover_layer = ccui.Widget.create()
        self.cc_scene.addChild(self.cc_cover_layer)
        self.cc_operate_layer = ccui.Widget.create()
        self.cc_scene.addChild(self.cc_operate_layer)
        self.plane_dict = {}
        self.model_dict = {}
        self.point_pool = []
        self.point_used = 0
        self.bg_sprite = cc.Sprite.create(BACKGROUND_UI_PATH)
        size = self.bg_sprite.getContentSize()
        self.bg_sprite.setScale(self.view_w / size.width, self.view_h / size.height)
        self.bg_sprite.setPosition(self.view_center)
        self.cc_display_layer.addChild(self.bg_sprite)
        self.add_touch_event()
        self.cached_tex = None
        self.point_cloud_idx = 0
        self.face_coord = None
        self.session = None
        self.ar_type = None
        self.ar_width = 0
        self.ar_height = 0
        self.camera = None
        self.hit_model = None
        self.face_rect = cc.DrawNode.create()
        self.cc_cover_layer.addChild(self.face_rect)
        self.gesture_rect = cc.DrawNode.create()
        self.cc_cover_layer.addChild(self.gesture_rect)
        self.gesture_text = cc.Label.createWithSystemFont('?', 'Arial', 30)
        self.cc_cover_layer.addChild(self.gesture_text)
        self.gesture_text.setPosition(self.view_center)
        self.gesture_text.setTextColor(cc.Color4B(0, 255, 0, 255))
        self.platform = game3d.get_platform()
        self.is_support = ar.is_support_ar()
        self.log('Check AR Support: %s', self.is_support)
        self.init_buttons()
        self.scn = None
        return

    def get_program(self):
        if self.platform == game3d.PLATFORM_ANDROID:
            SHADER_PS = SHADER_PS_ANDROID
        elif self.platform == game3d.PLATFORM_IOS:
            SHADER_PS = SHADER_PS_IOS
        else:
            return
        program = cc.GLProgram.createWithFilenames(SHADER_VS, SHADER_PS)
        return cc.GLProgramState.create(program)

    def init_buttons(self):
        for idx, config in enumerate(CONFIGS):
            name, path, asset = config
            v_btn = ccui.Button.create()
            v_btn.setTitleFontSize(30)
            v_btn.setTitleText(name)
            self.cc_operate_layer.addChild(v_btn)
            v_btn.setPosition(cc.Vec2(100, 150 + idx * 60))
            self.add_btn_click_event(v_btn, lambda p=path, a=asset: self.start_config(p, a))

        btn = ccui.Button.create()
        btn.setTitleFontSize(30)
        btn.setTitleText('SaveMap')
        self.cc_operate_layer.addChild(btn)
        btn.setPosition(cc.Vec2(500, 150))
        self.add_btn_click_event(btn, lambda : self.do_save_map())
        btn = ccui.Button.create()
        btn.setTitleFontSize(30)
        btn.setTitleText('LoadMap')
        self.cc_operate_layer.addChild(btn)
        btn.setPosition(cc.Vec2(500, 210))
        self.add_btn_click_event(btn, lambda : self.do_load_map())

    def start_config(self, config_path, asset_path):
        global CONFIG
        global ASSETS
        CONFIG = config_path
        ASSETS = asset_path
        self.log('start_config...')
        if self.session is not None:
            self.stop_ar()
        self.init_ar()
        return

    def init_ar(self):
        if not self.is_support:
            return
        if not ar.check_and_request_permission():
            return
        self.log('Start ARSession...')
        self.session = ar.ar_session()
        self.log('Register: %s %s', APPKEY, SECRET)
        self.session.register(APPKEY, SECRET)
        self.log('Setup Callbacks...')
        self.session.on_frame_callback = self.on_frame_cb
        self.session.on_error_callback = self.on_error_cb
        self.session.on_anchor_added_callback = self.on_anchor_added_cb
        self.session.on_anchor_updated_callback = self.on_anchor_updated_cb
        self.session.on_anchor_removed_callback = self.on_anchor_removed_cb
        self.session.on_face_callback = self.on_face_cb
        self.session.on_gesture_callback = self.on_gesture_cb
        self.session.on_save_map_callback = self.on_save_map_cb
        self.session.on_load_map_callback = self.on_load_map_cb
        if False and self.platform == game3d.PLATFORM_IOS:
            abs_config = os.path.join(game3d.get_doc_dir(), CONFIG)
            abs_assets = os.path.join(game3d.get_doc_dir(), ASSETS)
        else:
            abs_config = os.path.abspath(CONFIG)
            abs_assets = os.path.abspath(ASSETS)
        self.log('Init ARSession Config Path: %s %s', abs_config, abs_assets)
        self.session.init(abs_config, abs_assets)

    def stop_ar(self):
        self.log('Stop ARSession...')
        self.session.stop()
        self.session = None
        self.log('Clear Camera Texture & Scene Texture...')
        self.cc_display_layer.removeChild(self.cc_sprite)
        self.cc_sprite = None
        self.cc_display_layer.removeChild(self.cc_scn_sprite)
        self.cc_scn_sprite = None
        if self.cached_tex:
            for tex in self.cached_tex:
                tex.release()

        self.cached_tex = None
        self.log('Clear AR Scene...')
        render.render = None
        self.face_rect.clear()
        self.gesture_rect.clear()
        for plane in six.itervalues(self.plane_dict):
            self.scn.remove_object(plane)

        for model in six.itervalues(self.model_dict):
            self.scn.remove_object(model)

        if self.hit_model:
            self.scn.remove_object(self.hit_model)
        self.camera = None
        self.scn = None
        return

    def hit_test(self, x, z):
        anchor_data = self.session.get_hit_test_result(x, z)
        self.log('Get Hit Test Result: (%s,%s) %s', x, z, anchor_data)
        if anchor_data is not None:
            self.log('hit_test: %s, %s, %s, %s', anchor_data.identifier, anchor_data.type, anchor_data.alignment, anchor_data.is_valid)
            self.log('hit_test.transform: %s', anchor_data.transform)
            self.log('hit_test.rotation: %s', anchor_data.rotation)
            self.log('hit_test.center: %s', anchor_data.center)
            self.log('hit_test.extent: %s', anchor_data.extent)
            pos = self.get_hittest_pos(anchor_data)
            if self.hit_model is None:
                self.hit_model = world.model(MODEL_PATH, self.scn)
                self.hit_model.scale = math3d.vector(0.005, 0.005, 0.005)
            self.hit_model.position = pos
        return

    def do_save_map(self):
        if self.session is None:
            return
        else:
            if CONFIG != CONFIGS[6][1]:
                return
            map_path = self.get_map_path()
            self.session.save_map_data(map_path)
            return

    def do_load_map(self):
        if self.session is None:
            return
        else:
            if CONFIG != CONFIGS[7][1]:
                return
            map_path = self.get_map_path()
            if False and not os.path.exists(map_path):
                print('Map Path does not exisit')
                return
            self.session.load_map_data(map_path)
            return

    def get_map_path(self):
        if self.platform == game3d.PLATFORM_IOS:
            abs_path = os.path.join(game3d.get_doc_dir(), MAP_PATH)
        else:
            abs_path = os.path.abspath(MAP_PATH)
        self.log('Map Path: %s', abs_path)
        print('Map Path: ', abs_path)
        return abs_path

    def setup_ar_scene(self):
        self.log('Setup AR Scene...')
        self.ar_type = self.session.get_current_ar_type()
        if self.ar_type == ar.AR_INSIGHT:
            self.log('Current AR Type: InsightAR')
        elif self.ar_type == ar.AR_ARCORE:
            self.log('Current AR Type: ARCore')
        elif self.ar_type == ar.AR_ARKIT:
            self.log('Current AR Type: ARKit')
        else:
            self.log('Current AR Type: Unknown')
        self.log('Setup Camera Texture...')
        self.setup_cam_texture()
        if self.ar_width == 0 or self.ar_height == 0:
            return
        else:
            w, h = self.ar_width, self.ar_height
            self.log('Setup AR Scene RenderTarget...')
            nx_scn_tex = render.texture.create_empty(w, h, render.PIXEL_FMT_A8R8G8B8, True)
            self.log('Create Scene Tex Size: %s', nx_scn_tex.size)
            self.scene_rt = render.create_render_target(nx_scn_tex, None, render.PIXEL_FMT_D24S8, 0, 0)
            self.log('Create Scene RenderTarget: %s', self.scene_rt)
            cc_scn_tex = cc.Texture2D.createWithITexture(nx_scn_tex)
            self.cc_scn_sprite = cc.Sprite.createWithTexture(cc_scn_tex)
            self.cc_display_layer.addChild(self.cc_scn_sprite)
            if self.platform == game3d.PLATFORM_IOS:
                self.cc_scn_sprite.setScale(1, -1)
            else:
                self.cc_scn_sprite.setScale(1, -1)
            self.cc_scn_sprite.setPosition(self.view_center)
            self.log('Create AR Scene and Render to RenderTarget...')
            self.scn = world.scene()
            self.scn.background_color = 0
            self.camera = self.scn.create_camera(True)
            render.set_render(self.scn_render)
            return

    def setup_cam_texture(self):
        if self.platform == game3d.PLATFORM_ANDROID:
            self.setup_cam_texture_android()
        elif self.platform == game3d.PLATFORM_IOS:
            self.setup_cam_texture_ios()
        else:
            return

    def setup_cam_texture_android(self):
        data_provider = self.session.fetch_cam_data_provider()
        if data_provider is None:
            self.log('Error: fetch camera data provider failed.')
            return
        else:
            nx_tex = render.texture('', False, False, 0, False, None, None, 0, 0, False, data_provider)
            self.log('Camera Tex Size: %s', nx_tex.size)
            cc_tex = cc.Texture2D.createWithITexture(nx_tex)
            self.cc_sprite = cc.Sprite.createWithTexture(cc_tex)
            self.cc_sprite.setPosition(self.view_center)
            self.cc_display_layer.addChild(self.cc_sprite)
            if self.ar_type == ar.AR_INSIGHT:
                content_size = self.cc_sprite.getContentSize()
            elif self.ar_type == ar.AR_ARCORE:
                content_size = self.cc_sprite.getContentSize()
                self.cc_sprite.setScale(-1, -1)
                state = self.get_program()
                self.cc_sprite.setGLProgramState(state)
            else:
                self.log('Unknown AR Type: %s', ar_type)
                return
            self.ar_width = data_provider.size[0]
            self.ar_height = data_provider.size[1]
            return

    def setup_cam_texture_ios(self):
        y_provider = self.session.fetch_cam_y_data_provider()
        uv_provider = self.session.fetch_cam_uv_data_provider()
        if y_provider is None or uv_provider is None:
            self.log('Error: fetch camera data provider failed.')
            return
        else:
            nx_y_tex = render.texture('', False, False, 0, False, None, None, 0, 0, False, y_provider)
            self.log('Camera Y Tex Size: %s', nx_y_tex.size)
            nx_uv_tex = render.texture('', False, False, 0, False, None, None, 0, 0, False, uv_provider)
            self.log('Camera UV Tex Size: %s', nx_uv_tex.size)
            cc_y_tex = cc.Texture2D.createWithITexture(nx_y_tex)
            cc_uv_tex = cc.Texture2D.createWithITexture(nx_uv_tex)
            self.cc_sprite = cc.Sprite.createWithTexture(cc_y_tex)
            state = self.get_program()
            state.setUniformTexture('CC_Texture0', cc_y_tex)
            state.setUniformTexture('CC_Texture2', cc_uv_tex)
            cc_y_tex.retain()
            cc_uv_tex.retain()
            self.cached_tex = (cc_y_tex, cc_uv_tex)
            self.cc_sprite.setGLProgramState(state)
            self.cc_display_layer.addChild(self.cc_sprite)
            self.cc_sprite.setPosition(self.view_center)
            self.cc_sprite.setContentSize(cc.Size(nx_y_tex.size[0], nx_y_tex.size[1]))
            self.cc_sprite.setTextureRect(cc.Rect(0, 0, nx_y_tex.size[0], nx_y_tex.size[1]))
            content_size = self.cc_sprite.getContentSize()
            self.ar_width = y_provider.size[0]
            self.ar_height = y_provider.size[1]
            return

    def scn_render(self):
        self.log('scn_render...')
        self.scn.render(self.scene_rt)

    def on_frame_cb(self, session, state, reason, timestamp, cam_pose, cam_param):
        self.log('on_frame_cb: %s %s %s', state, reason, timestamp)
        self.log('on_frame_cb.cam_pose: %s %s', cam_pose.center, cam_pose.quaternion)
        if (state == ar.STATE_DETECTING or state == ar.STATE_TRACKING) and self.camera is None:
            self.setup_ar_scene()
            if self.camera is not None:
                self.setup_camera_param(cam_param)
            coord = self.make_coord_axis()
            coord.position = math3d.vector(0, 0, 0)
        if self.camera is None:
            return
        else:
            if state != ar.STATE_TRACKING and state != ar.STATE_TRACK_LIMITED:
                return
            camera_pos = math3d.vector(*cam_pose.center)
            camera_rot = math3d.rotation(*cam_pose.quaternion)
            self.camera.set_placement(camera_pos, camera_rot.get_forward(), camera_rot.get_up())
            self.log('Camera LookAt: %s %s', camera_rot.get_forward(), camera_rot.get_up())
            return

    def setup_camera_param(self, cam_param):
        import math
        if self.ar_type == ar.AR_ARCORE:
            proj_mtx = cam_param.proj_mtx
            fov_y = math.degrees(math.atan(1.0 / proj_mtx[5])) * 2
            aspect = proj_mtx[5] / proj_mtx[0]
            z_min = proj_mtx[14] / (proj_mtx[10] - 1)
            z_max = proj_mtx[14] / (proj_mtx[10] + 1)
        elif self.ar_type == ar.AR_ARKIT:
            focal = 0.5 / math.tan(math.radians(cam_param.fov[0] / 2.0)) * self.ar_width
            fov_y = math.degrees(math.atan(0.5 / focal * self.ar_height)) * 2
            aspect = 1.0 * self.ar_width / self.ar_height
            z_min = 0.01
            z_max = 100.0
            self.log('Camera focal: %s, %s', focal, cam_param.focal_length)
        else:
            fov_y = cam_param.fov[1]
            aspect = 1.0 * self.ar_width / self.ar_height
            z_min = 0.01
            z_max = 100.0
        self.log('Camera Param: %s, %s, %s, %s', fov_y, aspect, z_min, z_max)
        self.camera.set_perspect(fov_y, aspect, z_min, z_max)

    def on_error_cb(self, session, err_code, err_msg):
        self.log('on_error_cb: %s, %s', err_code, err_msg)

    def on_anchor_added_cb(self, session, anchor_data):
        self.log('on_anchor_added_cb: %s, %s, %s, %s', anchor_data.identifier, anchor_data.type, anchor_data.alignment, anchor_data.is_valid)
        self.log('on_anchor_added_cb.transform: %s', anchor_data.transform)
        self.log('on_anchor_added_cb.rotation: %s', anchor_data.rotation)
        self.log('on_anchor_added_cb.center: %s', anchor_data.center)
        self.log('on_anchor_added_cb.extent: %s', anchor_data.extent)
        if anchor_data.type == ar.ANCHOR_PLANE:
            pos, rot = self.get_plane_pos_rot(anchor_data)
            plane = self.make_plane(anchor_data.extent[0], anchor_data.extent[2])
            plane.position = pos
            if self.ar_type == ar.AR_ARCORE:
                plane.rotation_matrix = rot
            elif self.ar_type == ar.AR_ARKIT:
                plane.rotation_matrix = rot
            self.plane_dict[anchor_data.identifier] = plane
            self.log('[==TEST==] Plane Added: %s, %s', pos, rot)
        elif anchor_data.type == ar.ANCHOR_MARKER_2D:
            pos, rot = self.get_anchor_pos_rot(anchor_data)
            model = world.model(MODEL_PATH, self.scn)
            model.scale = math3d.vector(0.0005, 0.0005, 0.0005)
            model.position = math3d.vector(pos)
            model.rotation_matrix = rot
            self.model_dict[anchor_data.identifier] = model

    def on_anchor_updated_cb(self, session, anchor_data):
        self.log('on_anchor_updated_cb: %s, %s, %s, %s', anchor_data.identifier, anchor_data.type, anchor_data.alignment, anchor_data.is_valid)
        self.log('on_anchor_updated_cb.center: %s', anchor_data.center)
        self.log('on_anchor_updated_cb.extent: %s', anchor_data.extent)
        self.log('on_anchor_updated_cb.transform: %s', anchor_data.transform)
        self.log('on_anchor_updated_cb.rotation: %s', anchor_data.rotation)
        if anchor_data.type == ar.ANCHOR_PLANE:
            if anchor_data.identifier not in self.plane_dict:
                return
            pos, rot = self.get_plane_pos_rot(anchor_data)
            plane = self.plane_dict[anchor_data.identifier]
            plane.position = pos
            if self.ar_type == 2:
                plane.rotation_matrix = rot
            elif self.ar_type == 4:
                plane.rotation_matrix = rot
            w = anchor_data.extent[0]
            h = anchor_data.extent[2]
            vertex = [
             (
              -0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0),
             (
              -0.5 * w, 0, 0.5 * h, 4294901760L, 0, 0),
             (
              0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0),
             (
              0.5 * w, 0, -0.5 * h, 4278255360L, 0, 0),
             (
              -0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0),
             (
              0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0)]
            for i, v in enumerate(vertex):
                plane.set_vert(i, v[0], v[1], v[2], v[3], v[4], v[5])

            self.log('[==TEST==] Plane Updated: %s, %s', pos, rot)
        if anchor_data.type == ar.ANCHOR_MARKER_2D:
            if anchor_data.identifier not in self.model_dict:
                return
            pos, rot = self.get_anchor_pos_rot(anchor_data)
            model = self.model_dict[anchor_data.identifier]
            model.position = pos
            model.rotation_matrix = rot

    def on_anchor_removed_cb(self, session, anchor_data):
        self.log('on_anchor_removed_cb: %s', anchor_data.identifier)
        if anchor_data.type == ar.ANCHOR_PLANE:
            if anchor_data.identifier not in self.plane_dict:
                return
            plane = self.plane_dict.pop(anchor_data.identifier, None)
            self.scn.remove_object(plane)
        if anchor_data.type == ar.ANCHOR_MARKER_2D:
            if anchor_data.identifier not in self.model_dict:
                return
            model = self.model_dict.pop(anchor_data.identifier, None)
            self.scn.remove_object(model)
        return

    def on_face_cb(self, session, statu, count, faces):
        self.log('on_face_cb: %s %s', statu, count)
        self.face_rect.clear()
        if statu == 1 and count > 0:
            x, y, w, h = faces[0].rect
            self.log('on_face_size: %s', faces[0].rect)
            w_pos = self.cc_sprite.convertToWorldSpace(cc.Vec2(x, self.ar_height - y))
            x = w_pos.x
            y = w_pos.y
            self.face_rect.drawRect(cc.Vec2(x, y), cc.Vec2(x + w, y), cc.Vec2(x + w, y - h), cc.Vec2(x, y - h), cc.Color4F(1.0, 0, 0, 1.0))
            loc_str = faces[0].loc
            point_list = loc_str.split(';')
            for point_str in point_list:
                x_str, y_str = point_str.split(',')
                x = float(x_str)
                y = float(y_str)
                w_pos = self.cc_sprite.convertToWorldSpace(cc.Vec2(x, self.ar_height - y))
                self.face_rect.drawDot(w_pos, 2, cc.Color4F(0, 0, 1.0, 1.0))

            if self.face_coord is None:
                self.face_coord = self.make_coord_axis()
            pos, rot = self.get_pose_pos_rot(faces[0].pose, self.camera.transformation)
            self.face_coord.position = pos
            self.face_coord.rotation_matrix = rot
            self.log('Face Pose: %s %s', pos, rot)
        return

    def on_gesture_cb(self, session, statu, count, gestures):
        self.log('on_gesture_cb: %s %s', statu, count)
        self.gesture_rect.clear()
        self.gesture_text.setString('?')
        if statu == 1 and count > 0:
            self.gesture_text.setString(GESTURES[gestures[0].class_id])
            x, y, w, h = gestures[0].rect
            w_pos = self.cc_sprite.convertToWorldSpace(cc.Vec2(x, self.ar_height - y))
            x = w_pos.x
            y = w_pos.y
            self.gesture_rect.drawRect(cc.Vec2(x, y), cc.Vec2(x + w, y), cc.Vec2(x + w, y - h), cc.Vec2(x, y - h), cc.Color4F(0, 1.0, 0, 1.0))

    def on_save_map_cb(self, session, result, path):
        self.log('on_save_map_cb: %s %s', result, path)
        print('on_save_map_cb:', result, path)

    def on_load_map_cb(self, session, result, path):
        self.log('on_load_map_cb: %s %s', result, path)
        print('on_load_map_cb:', result, path)

    def show_point_cloud(self):
        if self.session is None:
            return
        else:
            if CONFIG != CONFIGS[1][1]:
                return
            if self.camera is None:
                return
            points = self.session.get_point_cloud()
            if points is None:
                self.log('Get Point Cloud Failed.')
                print('Get Point Cloud Failed')
                return
            if self.point_cloud_idx > 0:
                self.point_cloud_idx -= 1
                return
            self.point_cloud_idx = 10
            len_point = len(points) / 3
            pool_size = len(self.point_pool)
            if pool_size < len_point:
                for i in range(0, len_point - pool_size):
                    coord = self.make_point_coord()
                    self.point_pool.append(coord)

            for i in range(len_point):
                self.point_pool[i].position = self.get_point_cloud_pos(points, i)

            if self.point_used < len_point:
                for i in range(self.point_used, len_point):
                    self.point_pool[i].visible = True

            else:
                for i in range(len_point, self.point_used):
                    self.point_pool[i].visible = False

            self.point_used = len_point
            return

    def get_hittest_pos(self, anchor_data):
        transform = anchor_data.transform
        if self.ar_type == ar.AR_INSIGHT:
            return math3d.vector(transform[12], transform[13], transform[14])
        if self.ar_type == ar.AR_ARCORE:
            return math3d.vector(transform[12], transform[13], transform[14])
        if self.ar_type == ar.AR_ARKIT:
            return math3d.vector(transform[12], transform[13], transform[14])

    def get_plane_pos_rot(self, anchor_data):
        return (
         math3d.vector(*anchor_data.center), math3d.rotation(*anchor_data.rotation))

    def get_anchor_pos_rot(self, anchor_data):
        return (
         math3d.vector(*anchor_data.center), math3d.rotation(*anchor_data.rotation))

    def get_pose_pos_rot(self, pose, cam_mtx):
        quaternion = pose[:4]
        position = pose[4:]
        pos = math3d.vector(*position)
        rot = math3d.rotation(*quaternion)
        matrix = math3d.rotation_to_matrix(rot)
        matrix.translation = pos
        matrix = matrix * cam_mtx
        return (
         matrix.translation, matrix.rotation)

    def make_model(self):
        pass

    def make_plane(self, w, h):
        plane = world.primitives(self.scn)
        vetex = [
         (
          (
           -0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0),
          (
           -0.5 * w, 0, 0.5 * h, 4294901760L, 0, 0),
          (
           0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0)),
         (
          (
           0.5 * w, 0, -0.5 * h, 4278255360L, 0, 0),
          (
           -0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0),
          (
           0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0))]
        plane.create_poly3(vetex)
        plane.set_texture(0, render.texture(BACKGROUND_UI_PATH))
        return plane

    def make_coord_axis(self):
        coord = world.primitives(self.scn)
        vertex = [
         (
          (0, 0, 0, 4294901760L, 0, 0),
          (1.0, 0, 0, 4294901760L, 0, 0)),
         (
          (0, 0, 0, 4278255360L, 0, 0),
          (0, 1.0, 0, 4278255360L, 0, 0)),
         (
          (0, 0, 0, 4278190335L, 0, 0),
          (0, 0, 1.0, 4278190335L, 0, 0))]
        coord.create_line(vertex)
        coord.set_texture(0, render.texture(BACKGROUND_UI_PATH))
        return coord

    def make_point_coord(self):
        coord = world.primitives(self.scn)
        vertex = [
         (
          (0, 0, 0, 4278190080L, 0, 0),
          (1.0, 0, 0, 4278190080L, 0, 0)),
         (
          (0, 0, 0, 4278190080L, 0, 0),
          (0, 1.0, 0, 4278190080L, 0, 0)),
         (
          (0, 0, 0, 4278190080L, 0, 0),
          (0, 0, 1.0, 4278190080L, 0, 0))]
        coord.create_line(vertex)
        coord.set_texture(0, render.texture(BACKGROUND_UI_PATH))
        coord.scale = math3d.vector(0.01, 0.01, 0.01)
        coord.visible = False
        return coord

    def add_touch_event(self):
        listener = cc.EventListenerTouchOneByOne.create()
        listener.setOnTouchBeganCallback(self.on_touch_began)
        listener.setOnTouchMovedCallback(self.on_touch_moved)
        listener.setOnTouchEndedCallback(self.on_touch_ended)
        listener.setOnTouchCancelledCallback(self.on_touch_cancelled)
        listener.setSwallowTouches(True)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.cc_display_layer)

    def on_touch_began(self, touch, event):
        return True

    def on_touch_moved(self, touch, event):
        return True

    def on_touch_ended(self, touch, event):
        if self.session is None:
            return True
        else:
            if False and self.touch_index < len(self.touch_simulate):
                x, z = self.touch_simulate[self.touch_index]
                self.touch_index += 1
            else:
                location = touch.getLocation()
                location = self.cc_sprite.convertToNodeSpace(location)
                x = location.x
                z = location.y
            self.log('Touch Convert: x: %s, z: %s', x, z)
            if x < 0 or z < 0 or x > self.ar_width or z > self.ar_height:
                return
            z = self.ar_height - z
            self.log('Touch Ended: x: %s, z: %s', x, z)
            print('[NxAR-Python] Touch Ended', x, z)
            x *= 667.0 / self.ar_width
            z *= 375.0 / self.ar_height
            self.hit_test(x, z)
            return True

    def on_touch_cancelled(self, touch, event):
        return True

    def add_btn_click_event(self, btn, func):

        def _handler(widget, event):
            if event == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
                func()

        btn.addTouchEventListener(_handler)

    def cleanup(self):
        pass

    def update(self, *args):
        if self.scn:
            self.scn.update()

    def get_point_cloud_pos(self, points, i):
        return math3d.vector(points[i * 3], points[i * 3 + 1], points[i * 3 + 2])

    def on_key_msg(self, msg, key_code):
        pass

    def log(self, msg, *args):
        print('[NxAR-Python] %s' % (msg % args,))