# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbySceneSwitch.py
from __future__ import absolute_import
import six
from . import ScenePart
from common.cfg import confmgr
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils import item_utils
from logic.gutils.dress_utils import get_skin_default_wear_decoration_dict
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR
from ext_package.ext_decorator import has_skin_ext

class PartLobbySceneSwitch(ScenePart.ScenePart):
    INIT_EVENT = {'show_mecha_chuchang_scene': 'on_show_mecha_chuchang_scene',
       'end_mecha_chuchang_scene': 'on_end_mecha_chuchang_scene',
       'forbid_mecha_chuchang_scene': 'on_forbid_mecha_chuchang_scene',
       'show_lobby_relatived_scene': 'on_show_lobby_relatived_scene',
       'show_disposable_lobby_relatived_scene': 'on_show_disposable_lobby_relatived_scene',
       'set_lobby_scene_display_type': 'on_set_lobby_scene_display_type',
       'leave_current_scene': 'leave_current_scene',
       'release_current_scene': 'release_current_scene',
       'get_lobby_scene_type_event': 'get_scene_type',
       'get_lobby_display_type_event': 'get_display_type',
       'is_forbid_mecha_chuchang_scene': 'is_forbid_mecha_chuchang_scene'
       }

    def __init__(self, scene, name):
        super(PartLobbySceneSwitch, self).__init__(scene, name, False)
        self._scene_type = ''
        self._display_type = ''
        self._disposable_scene_type = None
        self._mecha_chuchang_belong_ui = None
        self.forbid_chuchang_scene = False
        return

    def on_pause(self, flag):
        if not flag and global_data.lobby_player:
            global_data.lobby_player.send_event('E_REFRESH_LOBBY_PLAYER_MODEL')
            global_data.emgr.lobby_mecha_display_reset.emit()
            if global_data.player:
                visitors = global_data.player.get_all_puppet_info(True)
                if visitors:
                    for key, data in six.iteritems(visitors):
                        entity = global_data.player.get_place_puppet(key)
                        if entity and entity.logic:
                            entity.logic.send_event('E_REFRESH_LOBBY_PLAYER_MODEL')

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def get_display_type(self):
        return self._display_type

    def get_scene_type(self):
        return self._scene_type

    def leave_current_scene(self):
        if self._disposable_scene_type is not None:
            self._disposable_scene_type = None
            global_data.ex_scene_mgr_agent.return_scene(True)
        else:
            global_data.ex_scene_mgr_agent.return_scene()
        global_data.emgr.check_cur_scene_mirror_model_event.emit()
        return

    def release_current_scene(self):
        global_data.ex_scene_mgr_agent.return_scene(True)

    def on_show_mecha_chuchang_scene(self, skin_id, belong_ui_name=None):
        if self.forbid_chuchang_scene:
            return
        else:
            self._mecha_chuchang_belong_ui = belong_ui_name
            item_type = item_utils.get_lobby_item_type(skin_id)
            cur_skin_cnf = None
            if item_type == L_ITEM_TYPE_MECHA_SKIN:
                cur_skin_cnf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(skin_id))
            elif item_type == L_ITEM_TYPE_ROLE_SKIN:
                cur_skin_cnf = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id))
            model_data = lobby_model_display_utils.get_lobby_model_data(skin_id, consider_second_model=False)
            for data in model_data:
                data['skin_id'] = skin_id
                data['by_mecha_chuchang'] = True
                data['show_anim'] = cur_skin_cnf.get('chuchang_anim')
                data['end_anim'] = None
                data['chuchang_trk'] = None

            scene_type = scene_const.SCENE_MECHA_CHUCHANG
            scene_path = cur_skin_cnf.get('chuchang_scene_path', None)
            if scene_path is None:
                scene_path = confmgr.get('script_gim_ref', 'default_chuchang_scene_path')
            display_type = lobby_model_display_const.MECHA_CHUCHANG
            self.on_show_disposable_lobby_relatived_scene(scene_type, scene_path, display_type, belong_ui_name=belong_ui_name)
            global_data.emgr.set_mecha_chuchang_data.emit(skin_id)
            global_data.emgr.change_model_display_scene_item.emit(model_data)
            return

    def on_forbid_mecha_chuchang_scene(self, forbid):
        if not has_skin_ext():
            self.forbid_chuchang_scene = True
        else:
            self.forbid_chuchang_scene = forbid

    def is_forbid_mecha_chuchang_scene(self):
        if not has_skin_ext():
            return True
        else:
            return self.forbid_chuchang_scene

    def on_end_mecha_chuchang_scene(self):
        if self.forbid_chuchang_scene:
            return
        ui = global_data.ui_mgr.get_ui(self._mecha_chuchang_belong_ui)
        if ui and ui.get_show():
            if hasattr(ui, 'do_show_panel_ex'):
                ui.do_show_panel_ex('mecha_chuchang_scene')
            else:
                ui.do_show_panel()

    def on_set_lobby_scene_display_type(self, display_type, is_slerp=False, update_cam_at_once=False):
        if display_type is not None:
            self._display_type = display_type
            scene_data = lobby_model_display_utils.get_display_scene_data(display_type)
            global_data.emgr.change_model_display_scene_info.emit(scene_data)
            global_data.emgr.change_model_display_scene_cam.emit(scene_data.get('cam_key'), is_slerp, update_cam_at_once)
        return

    def on_show_lobby_relatived_scene(self, scene_type, display_type=None, update_cam_at_once=False, finish_callback=None, belong_ui_name=None, scene_content_type=None, scene_background_texture=None, finish_callback_ex=None, sfx_list=None, is_slerp=False, change_saijika_background=False):
        global_data.emgr.close_special_lobby_scene_event.emit()
        if global_data.battle and global_data.battle.is_start_battle and not global_data.is_local_editor_mode:
            return
        else:
            if global_data.use_artist_test_scne and scene_content_type:
                scene_type = scene_content_type
                scene_content_type = None
            self._scene_type = scene_type

            def on_load_complete(c_scene_type, new_scene):
                self.on_set_lobby_scene_display_type(display_type, is_slerp=is_slerp, update_cam_at_once=update_cam_at_once)
                global_data.emgr.change_scene_event.emit(new_scene, c_scene_type)
                if finish_callback:
                    finish_callback(c_scene_type)
                if finish_callback_ex:
                    finish_callback_ex(new_scene, c_scene_type)

            self.clear_disposable_scene()
            new_scene = global_data.ex_scene_mgr_agent.add_lobby_relatived_scene(scene_type, on_load_complete, belong_ui_name=belong_ui_name, scene_content_type=scene_content_type, scene_background_texture=scene_background_texture, sfx_list=sfx_list, change_saijika_background=change_saijika_background)
            is_reflect = lobby_model_display_utils.is_scene_surpport_reflect(scene_type)
            if not is_reflect:
                new_scene = None
            if scene_content_type and not lobby_model_display_utils.is_scene_surpport_reflect(scene_content_type):
                new_scene = None
            global_data.emgr.change_scene_event.emit(new_scene, scene_type)
            return

    def on_show_disposable_lobby_relatived_scene(self, scene_type, scene_path, display_type=None, update_cam_at_once=False, belong_ui_name=None, use_scene_type=False, scene_background_texture='', bg_model_name=''):
        self.clear_disposable_scene()
        self._disposable_scene_type = scene_type
        self._scene_type = scene_type
        scene_data = None
        if not use_scene_type:
            scene_data = {}
            scene_data['scene_path'] = scene_path
            scene_data['bg_model_name'] = bg_model_name
            scene_data['scene_background_texture'] = scene_background_texture
        new_scene = global_data.ex_scene_mgr_agent.add_disposable_lobby_relatived_scene(scene_type, scene_data, belong_ui_name)
        global_data.emgr.change_scene_event.emit(new_scene, scene_type)
        self.on_set_lobby_scene_display_type(display_type, update_cam_at_once=update_cam_at_once)
        return

    def clear_disposable_scene(self):
        if self._disposable_scene_type is not None:
            self._disposable_scene_type = None
            global_data.ex_scene_mgr_agent.return_scene(True, False)
        return