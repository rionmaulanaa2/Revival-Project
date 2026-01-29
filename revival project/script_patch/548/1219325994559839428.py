# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/RankModelControler.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon import const
from logic.gcommon.item import item_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils.lobby_model_display_utils import get_cam_position
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.common_const import rank_const
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils import template_utils
from logic.gutils import skin_define_utils
from logic.gutils import item_utils as iutils

class RankSceneControler(object):

    def __init__(self, parent):
        self.parent = parent
        self.parent_panel = parent.panel
        self.is_bind = False
        self.cur_model = None
        self.cur_show_model_item_no = None
        self.normal_position = [15, 30, 70]
        self.cur_uid = global_data.player.uid
        self.init_event()
        return

    def pause(self):
        self.process_event(False)

    def resume(self):
        self.process_event(True)
        self.reset_cam_pos()
        self.on_reques_model_info(self.cur_uid)

    def init_event(self):
        self.process_event(True)

    def destroy(self):
        self.parent = None
        self.parent_panel = None
        self.pause()
        return

    def process_event(self, is_bind):
        if is_bind == self.is_bind:
            return
        emgr = global_data.emgr
        econf = {'message_on_player_detail_inf': self.on_show_model,
           'on_show_main_rank_cur_model': self.on_show_cur_model,
           'on_show_main_rank_model': self.on_reques_model_info
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

    def on_show_cur_model(self):
        self.on_reques_model_info(self.cur_uid)

    def on_reques_model_info(self, uid):
        if not self.parent_panel:
            return
        else:
            self.cur_uid = uid
            self.cur_show_model_item_no = None
            data = global_data.message_data.get_player_detail_inf(uid)
            if data:
                self.on_show_model(data)
            else:
                self.parent_panel.temp_title.setVisible(False)
            return

    def on_show_model(self, role_info):
        if not role_info:
            return
        else:
            from logic.gutils import lobby_model_display_utils
            uid = role_info.get('uid', 0)
            if self.cur_uid != uid:
                return
            rank_use_title_dict = role_info.get('rank_use_title_dict', {})
            rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
            title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
            template_utils.init_rank_title(self.parent_panel.temp_title, title_type, rank_info)
            is_mine = self.cur_uid == global_data.player.uid
            if is_mine:
                mecha_id = global_data.player.get_lobby_selected_mecha_id()
                mecha_pose_dict = global_data.player.get_mecha_pose()
                is_apply = global_data.player.is_apply_mecha_pose()
                mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
                mecha_item_no = global_data.player.get_mecha_fashion(mecha_item_id)
                mecha_pose = skin_define_utils.get_mecha_gesture_pose(mecha_item_id, is_apply, mecha_pose_dict)
                role_id = global_data.player.get_role()
                item_data = global_data.player.get_item_by_no(role_id)
                fashion_data = item_data.get_fashion()
            else:
                is_apply = role_info.get(item_const.MECHA_LOBBY_POSE_SHOW, False)
                mecha_pose_dict = role_info.get(item_const.MECHA_LOBBY_POSE, {})
                mecha_item_no = role_info.get(item_const.MECHA_LOBBY_FASHION_KEY, None)
                lobby_mecha_id = role_info.get(item_const.MECHA_LOBBY_ID_KEY, 101008001)
                if mecha_item_no is None:
                    mecha_item_no = lobby_mecha_id
                fashion_data = role_info.get(item_const.INF_ROLE_FASHION_KEY, {})
                mecha_pose = skin_define_utils.get_mecha_gesture_pose(lobby_mecha_id, is_apply, mecha_pose_dict)
            role_item_no = fashion_data.get(item_const.FASHION_POS_SUIT, 201001100)
            role_head_no = fashion_data.get(item_const.FASHION_POS_HEADWEAR, None)
            bag_id = fashion_data.get(item_const.FASHION_POS_BACK, None)
            suit_id = fashion_data.get(item_const.FASHION_POS_SUIT_2, None)
            other_pendants = [ fashion_data.get(pos) for pos in item_const.FASHION_OTHER_PENDANT_LIST ]
            if role_item_no <= 0 or mecha_item_no <= 0:
                return
            is_mine = True if self.cur_uid == global_data.player.uid else False
            decal_list = []
            color_dict = {}
            if is_mine:
                decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(mecha_item_no)), [])
                color_dict = global_data.player.get_mecha_color().get(str(mecha_item_no), {})
            else:
                skind_define_data = role_info.get(item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY, {})
                if skind_define_data:
                    decal_list = skind_define_data.get('decal', [])
                    color_dict = skind_define_data.get('color', {})
                if self.cur_show_model_item_no == (role_item_no, mecha_item_no):
                    global_data.emgr.refresh_model_decal_data.emit(decal_list)
                    global_data.emgr.refresh_model_color_data.emit(color_dict)
                    return
            self.cur_show_model_item_no = (role_item_no, mecha_item_no)
            role_model_data = lobby_model_display_utils.get_lobby_model_data(role_item_no, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
            for data in role_model_data:
                data['model_scale'] = data.get('model_scale', 1.0) * const.ROLE_SCALE
                data['off_euler_rot'][1] = const.ROLE_ROTATION_Y
                data['ignore_chuchang_sfx'] = True
                if not is_mine and fashion_data.get(item_const.FASHION_POS_WEAPON_SFX):
                    data['improved_skin_sfx_id'] = fashion_data[item_const.FASHION_POS_WEAPON_SFX]

            pet_id, pet_level = (None, None)
            if is_mine:
                pet_id = global_data.player.get_choosen_pet()
                pet_item = global_data.player.get_item_by_no(pet_id)
                pet_level = pet_item.level if pet_item else 1
            elif 'pet_info' in role_info:
                pet_id = role_info['pet_info'].get('pet_id', None)
                pet_level = role_info['pet_info'].get('level', None)
            if pet_id:
                from common.cfg import confmgr
                pet_model_data = lobby_model_display_utils.get_lobby_model_data(pet_id, pet_level=pet_level)
                for data in pet_model_data:
                    data['model_scale'] = const.PET_SCALE * confmgr.get('c_pet_info', str(pet_id), 'human_scale', default=1.0)
                    data['off_euler_rot'][1] = const.PET_ROTATION_Y
                    data['off_position'] = const.PET_OFF_POSITION

                role_model_data.extend(pet_model_data)
            mecha_model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_no, is_get_player_data=is_mine)
            for data in mecha_model_data:
                data['skin_id'] = mecha_item_no
                if mecha_pose:
                    data['show_anim'] = iutils.get_lobby_item_res_path(mecha_pose, get_main_skin_id(mecha_item_no))
                data['model_scale'] = data.get('model_scale', 1.0) * const.MECHA_SCALE
                data['off_euler_rot'][1] = const.MECHA_ROTATION_Y
                if not is_mine and role_info.get(item_const.MECHA_LOBBY_WP_SFX_KEY, 0) > 0:
                    data['shiny_weapon_id'] = role_info.get(item_const.MECHA_LOBBY_WP_SFX_KEY, 0)
                data['decal_list'] = global_data.player.get_mecha_decal().get(str(get_main_skin_id(mecha_item_no)), []) if is_mine else decal_list
                if is_mine:
                    data['color_dict'] = global_data.player.get_mecha_color().get(str(mecha_item_no), {}) if 1 else color_dict

            global_data.emgr.change_model_display_scene_item_ex.emit(mecha_model_data, role_model_data)
            return