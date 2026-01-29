# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankModelControler.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon import const
from logic.gcommon.item import item_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils.lobby_model_display_utils import get_cam_position
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id, get_mecha_default_fashion
from logic.gutils.skin_define_utils import get_main_skin_id
from common.cfg import confmgr

class PVERankModelControler(object):

    def __init__(self, parent):
        self.parent = parent
        self.panel = parent.panel
        self.is_bind = False
        self.init_parameters()
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def pause(self):
        self.process_event(False)

    def resume(self):
        self.process_event(True)
        self.reset_cam_pos()
        self.on_show_cur_model()

    def init_parameters(self):
        self.cur_model = None
        self.pve_mecha_id = None
        self.cur_shiny_weapon_id = None
        self.normal_position = [35, 35, 68]
        self.cur_uid = None
        self.cur_pass_info = None
        self.cur_mecha_item_no = None
        return

    def destroy(self):
        self.parent = None
        self.panel = None
        self.pause()
        return

    def process_event(self, is_bind):
        if is_bind == self.is_bind:
            return
        emgr = global_data.emgr
        econf = {'on_show_pve_rank_model': self.on_request_model_info,
           'on_pve_rank_show_self_model': self.show_self_mecha,
           'on_show_main_rank_cur_model': self.on_show_cur_model
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self.is_bind = is_bind

    def reset_cam_pos(self):
        import math3d
        pos = get_cam_position(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.MAIN_RANK_SCENE)
        global_data.emgr.change_model_display_scene_cam_pos.emit(pos + math3d.vector(*self.normal_position), True)

    def on_request_model_info(self, info):
        if len(info) == 3:
            uid, pve_rank_data_obj, uid_key = info
        else:
            uid, pve_rank_data_obj = info
        self.cur_uid = uid
        if pve_rank_data_obj.get_player_cnt() > 1:
            req_uid_list, return_dict = global_data.message_data.get_pve_team_rank_pass_data(pve_rank_data_obj, uid_key)
        else:
            req_uid_list, return_dict = global_data.message_data.get_pve_rank_pass_data(pve_rank_data_obj, [uid])
        data = return_dict.get(uid, None)
        print ('on_show_pve_rank_model____:', uid, pve_rank_data_obj.get_player_cnt(), pve_rank_data_obj.to_client(), data)
        if data:
            self.on_show_model(uid, data)
        self.panel.temp_title.setVisible(False)
        return

    def on_show_cur_model(self):
        if not self.cur_uid or not self.cur_pass_info:
            return
        self.on_show_model(self.cur_uid, self.cur_pass_info, True)

    def on_show_model(self, uid, pass_info, force=False):
        if not pass_info:
            return
        else:
            self.cur_pass_info = pass_info
            from logic.gutils import lobby_model_display_utils
            shiny_weapon_id = pass_info.get(item_const.MECHA_LOBBY_WP_SFX_KEY, 0)
            if self.cur_uid != uid and not force:
                return
            mecha_item_no = pass_info.get('mecha_skin_id', None)
            if not mecha_item_no:
                mecha_id = pass_info.get('mecha_id', 8001)
                mecha_item_no = get_mecha_default_fashion(mecha_id)
            if mecha_item_no <= 0:
                return
            decal_list = []
            color_dict = {}
            skind_define_data = pass_info.get(item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY, {})
            if skind_define_data:
                decal_list = skind_define_data.get('decal', [])
                color_dict = skind_define_data.get('color', {})
            mecha_model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_no, is_get_player_data=False)
            for data in mecha_model_data:
                data['skin_id'] = mecha_item_no
                data['model_scale'] = data.get('model_scale', 1.0) * const.MECHA_SCALE
                data['off_euler_rot'][1] = const.MECHA_ROTATION_Y
                data['decal_list'] = decal_list
                data['color_dict'] = color_dict
                if shiny_weapon_id > 0:
                    data['shiny_weapon_id'] = shiny_weapon_id

            def on_load_model(model):
                global_data.emgr.reset_rotate_model_display.emit()
                self.cur_model = model
                self.cur_mecha_item_no = mecha_item_no
                self.cur_shiny_weapon_id = shiny_weapon_id
                global_data.emgr.on_pve_main_model_load_complete.emit(self.cur_mecha_item_no)

            global_data.emgr.change_model_display_scene_item.emit(None)
            global_data.emgr.change_model_display_scene_item.emit(mecha_model_data, create_callback=on_load_model)
            self.reset_cam_pos()
            return

    def clear_model(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def show_self_mecha(self):
        from logic.gutils import lobby_model_display_utils
        mecha_id = global_data.player.get_lobby_selected_mecha_id()
        mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
        mecha_item_no = global_data.player.get_mecha_fashion(mecha_item_id)
        if mecha_item_no <= 0:
            return
        else:
            mecha_model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_no, is_get_player_data=True)
            for data in mecha_model_data:
                data['skin_id'] = mecha_item_no
                data['model_scale'] = data.get('model_scale', 1.0) * const.MECHA_SCALE
                data['off_euler_rot'][1] = const.MECHA_ROTATION_Y
                data['decal_list'] = global_data.player.get_mecha_decal().get(str(get_main_skin_id(mecha_item_no)), [])
                data['color_dict'] = global_data.player.get_mecha_color().get(str(mecha_item_no), {})

            def on_load_model(model):
                global_data.emgr.reset_rotate_model_display.emit()
                self.cur_model = model
                self.cur_mecha_item_no = mecha_item_no
                self.cur_shiny_weapon_id = 0
                global_data.emgr.on_pve_main_model_load_complete.emit(self.cur_mecha_item_no)

            global_data.emgr.change_model_display_scene_item.emit(None)
            global_data.emgr.change_model_display_scene_item.emit(mecha_model_data, create_callback=on_load_model)
            self.reset_cam_pos()
            self.panel.temp_title.setVisible(False)
            return