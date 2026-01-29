# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impVisit.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
import random
import math3d
import math
from mobile.common.EntityFactory import EntityFactory
from mobile.common.FilterMessageBroker import FilterMessageBroker
from logic.gcommon.common_const import chat_const
import logic.gcommon.common_const.visit_const as vconst
from mobile.common.EntityManager import EntityManager
from mobile.common.IdManager import IdManager
from ext_package.ext_decorator import get_default_mecha_fashion_decorator, get_default_mecha_shiny
from logic.gcommon import time_utility as tutil
from common.const.property_const import C_NAME, U_ID
import time
from logic.gcommon import const

class impVisit(object):
    LIMIT_VISIT_TIME = 20
    LIMIT_SHARE_TIME = 10
    POS_ARR = (
     (-59.003372, 16.327526, 16.987534),
     (-183.149017, -2.664272, -86.67128),
     (-252.319031, -2.664271, -160.91954))
    MSG_TYPE_OPERATION = {vconst.SYNC_TYPE_INIT: 'on_visit_msg_init',
       vconst.SYNC_TYPE_PLACE: 'on_visit_msg_place',
       vconst.SYMC_TYPE_ROOM_FULL: 'on_visit_room_full',
       vconst.SYNC_TYPE_PERMISSION_DENIED: 'on_visit_denied',
       vconst.SYNC_TYPE_ADD: 'on_visit_msg_add',
       vconst.SYNC_TYPE_DEL: 'on_visit_msg_del',
       vconst.SYNC_TYPE_UPDATE: 'on_visit_msg_update',
       vconst.SYNC_TYPE_TELPORT: 'on_visit_msg_telport',
       vconst.SYNC_TYPE_MOVE: 'on_visit_msg_move',
       vconst.SYNC_TYPE_ACTION: 'on_visit_msg_action',
       vconst.SYNC_TYPE_ADD_TEAMMATE: 'on_visit_msg_add_teammate',
       vconst.SYNC_TYPE_DEL_TEAMMATE: 'on_visit_msg_del_teammate',
       vconst.SYNC_TYPE_UPDATE_TEAMMATE: 'on_visit_msg_update_teammate',
       vconst.SYNC_TYPE_REQ_SHARE_IMAGE: 'on_visit_req_share_image',
       vconst.SYNC_TYPE_SHARE_IMAGE: 'on_visit_share_image',
       vconst.SYNC_TYPE_ACC_SHARE_IMAGE: 'on_visit_acc_share_image',
       vconst.SYNC_TYPE_PET_EVENT: 'on_visit_msg_pet_event'
       }

    def _init_visit_from_dict(self, bdict):
        FilterMessageBroker.register('on_visit_sync', self.on_visit_sync)
        self.visit_player_last_time = 0
        self.share_img_last_time = 0
        self.login_time = tutil.get_server_time() + 10
        self._place = None
        self._place_data = {}
        self._is_visit_ready = False
        self._visit_msg_cache = []
        self._born_position = random.choice(impVisit.POS_ARR)
        self._upload_img = None
        self._upload_img_id = None
        self._upload_img_url = None
        self.share_uid = None
        return

    def _destroy_visit(self):
        FilterMessageBroker.unregister('on_visit_sync', self.on_visit_sync)
        if self._place:
            self._place.destroy()
        self._place = None
        self._is_visit_ready = False
        self._visit_msg_cache = []
        return

    def is_in_visit_mode(self):
        return self._place is not None

    def is_visit_self(self):
        return self._place is not None and self._place.get_owner_uid() == self.uid

    def is_visit_others(self):
        return self._place is not None and self._place.get_owner_uid() != self.uid

    def get_visit_uid(self):
        if self._place:
            return self._place.get_owner_uid()
        else:
            return None
            return None

    def get_visit_name(self):
        if self._place:
            return self._place.get_owner_name()
        else:
            return ''

    def get_visit_priv_lv(self):
        if self._place:
            return self._place.get_owner_priv_lv()
        else:
            return 0

    def get_visit_mecha_info(self):
        if self._place:
            return self._place.get_mecha_info()
        else:
            return {}

    def get_visit_mecha_id(self):
        if self._place:
            return self._place.get_mecha_id()
        else:
            return None
            return None

    def get_visit_mecha_fashion(self, mecha_item_id):
        if self._place:
            return self._place.get_mecha_fashion(mecha_item_id)
        else:
            return None
            return None

    def get_visit_mecha_shiny_weapon_id(self, mecha_item_id):
        if self._place:
            return self._place.get_mecha_shiny_weapon_id(mecha_item_id)
        else:
            return -1

    def get_visit_wall_picture(self):
        if self._place:
            return self._place.get_wall_picture()
        else:
            return None
            return None

    def get_visit_lobby_skin_id(self):
        if self._place:
            return self._place.get_skin_id()
        else:
            return None
            return None

    def get_visit_lobby_bgm(self):
        if self._place:
            return self._place.get_bgm()
        else:
            return None
            return None

    def get_place_puppet(self, uid):
        if self._place:
            return self._place.get_puppet(uid)
        else:
            return None
            return None

    def get_visit_lobby_skybox_id(self):
        if self._place:
            return self._place.get_skybox_id()
        else:
            return None
            return None

    def get_visit_team_members(self):
        if self._place:
            return self._place.get_team_members()
        else:
            return None

    def get_visit_teammate_info(self, teammate_uid):
        if self._place:
            return self._place.get_teammate_data(teammate_uid)
        else:
            return None

    def get_visit_admin_team_idx(self):
        if self._place:
            return self._place.get_owner_team_idx()
        return -1

    def get_all_lobby_puppet(self):
        if self._place:
            return self._place.get_all_puppet()
        return {}

    def on_visit_msg_add_teammate(self, team_dict):
        self._place and self._place.add_teammate(team_dict)

    def on_visit_msg_del_teammate(self, teammate_uid):
        self._place and self._place.del_teammate(teammate_uid)

    def on_visit_msg_update_teammate(self, team_dict):
        self._place and self._place.update_teammate(team_dict)

    def on_visit_req_share_image(self, uid, img_id):
        self.share_uid = uid
        if uid == self.uid:
            return
        visitors = self.get_all_puppet_info()
        if uid not in visitors:
            return

        def _confirm_cb(is_confirm, uid=uid, img_id=img_id):
            if is_confirm:
                self.call_server_method('acc_share_img', (uid, img_id))
                global_data.ui_mgr.close_ui('ShowShareImgUI')
                global_data.ui_mgr.show_ui('ShowShareImgUI', 'logic.comsys.homeland')

        ui = global_data.ui_mgr.show_ui('ImgShareConfirmUI', 'logic.comsys.homeland')
        ui.set_share_info(visitors[uid], _confirm_cb)

    def on_visit_share_image(self, uid, img_id, url):
        if uid == self.uid:
            return
        ui = global_data.ui_mgr.show_ui('ShowShareImgUI', 'logic.comsys.homeland')
        ui.set_img_info(url)

    def on_visit_acc_share_image(self, img_id):
        if not self._upload_img_id or img_id != self._upload_img_id or not self._upload_img:
            return
        self._try_upload_share_image(self._upload_img)

    def on_visit_msg_pet_event(self, uid, args):
        if not self._place:
            return
        self._place.send_puppet_pet_event(uid, *args)

    def try_share_image(self, img_path):
        from logic.gcommon import time_utility
        cur_time = time_utility.time()
        if cur_time - self.share_img_last_time < self.LIMIT_SHARE_TIME:
            global_data.game_mgr.show_tip(get_text_by_id(609379).format(sec=int(math.ceil(self.LIMIT_SHARE_TIME - (cur_time - self.share_img_last_time)))))
            return
        self.share_img_last_time = cur_time
        if not img_path or not self._place:
            return
        self._upload_img = img_path
        self._upload_img_id = str(int(time.time()))
        self.call_server_method('request_share_img', (self._upload_img_id,))

    def _try_upload_share_image(self, img_path):
        self._fs_file_upload_hm_image(img_path, self._upload_img_cb)

    def _upload_img_cb(self, status, error, record_names):
        if not status or not self._upload_img_id:
            return
        self._upload_img_url = six_ex.keys(record_names)[0]
        self.call_server_method('upload_share_img_url', (self._upload_img_id, self._upload_img_url))

    def _fs_file_upload_hm_image(self, img_path, cb):
        file_type = const.FILE_SERVICE_UPLOAD_TYPE_HM_IMG
        function_key = const.FILE_SERVICE_FUNCTION_KEY_HOMELAND_IMG
        with open(img_path, 'rb') as f:
            file_content = f.read()
        self.fs_upload_file(function_key, file_type, file_content, img_path, 600, {}, cb)

    def is_sharer_in_lobby(self):
        visitor = global_data.player.get_all_puppet_info() or {}
        return self.share_uid in visitor

    def request_visit_leader(self):
        self.call_server_method('request_visit_leader', ())

    def request_visit_home(self):
        self.call_server_method('request_visit_home', ())

    def request_visit_player(self, uid):
        from logic.gcommon import time_utility
        cur_time = time_utility.time()
        if cur_time - self.visit_player_last_time > self.LIMIT_VISIT_TIME:
            self.call_server_method('request_visit_player', (uid,))
            self.visit_player_last_time = cur_time
        else:
            global_data.game_mgr.show_tip(get_text_by_id(611564).format(second=int(math.ceil(self.LIMIT_VISIT_TIME - (cur_time - self.visit_player_last_time)))))

    def sync_visit_create(self, request_id):
        visit_dict = {'move_info': {1: self._born_position,2: 0}}
        if global_data.lobby_player:
            move_info = global_data.lobby_player.ev_g_move_info()
            if move_info:
                visit_dict['move_info'] = move_info
        self.call_server_method('sync_visit_create', (request_id, visit_dict))
        is_visit_self = self.is_visit_self()
        global_data.emgr.player_enter_visit_scene_event.emit(is_visit_self)
        self.enter_lobby_to_visit(is_visit_self)

    def sync_visit_move(self, move_info):
        if not self.is_in_visit_mode():
            return
        self.call_server_method('sync_visit_move', (move_info,))

    def sync_visit_action(self, method_name, args):
        if not self.is_in_visit_mode():
            return
        self.call_server_method('sync_visit_action', (method_name, args))

    def sync_visit_pet_event(self, args):
        self.call_server_method('sync_visit_pet_event', (self.uid, args))

    def on_visit_sync(self, data):
        if not self._is_visit_ready:
            self._visit_msg_cache.append(data)
        else:
            mapping = self.MSG_TYPE_OPERATION
            for msg_type, info in six.iteritems(data):
                func_name = mapping[msg_type]
                getattr(self, func_name)(*info)

    def _process_msg_cache(self):
        if self._visit_msg_cache:
            cache = self._visit_msg_cache
            self._visit_msg_cache = []
            for data in cache:
                self.on_visit_sync(data)

    def on_visit_msg_init(self, request_id, entity_dict):
        if self._place:
            self._place.destroy()
        self._place = None
        self._visit_msg_cache = []
        entity_dict['request_id'] = request_id
        entity_type, entity_id = entity_dict['entity_type'], entity_dict['entity_id']
        print('[Visit] on_visit_msg_init, create entiy: ', entity_type)
        self._place = EntityFactory.instance().create_entity(entity_type, entity_id)
        self._place.init_from_dict(entity_dict)
        global_data.emgr.visit_place_change_event.emit()
        return

    def on_visit_room_full(self):
        global_data.game_mgr.show_tip(611600)
        from logic.gcommon import time_utility
        cur_time = time_utility.time()
        self.visit_player_last_time = cur_time - self.LIMIT_VISIT_TIME + 3

    def on_visit_denied(self, flag):
        if flag == vconst.DENIED_TYPE_BLACK_LIST:
            global_data.game_mgr.show_tip(634329)
        elif flag == vconst.DENIED_TYPE_BLOCK_STRANGER:
            global_data.game_mgr.show_tip(634328)
        from logic.gcommon import time_utility
        cur_time = time_utility.time()
        self.visit_player_last_time = cur_time - self.LIMIT_VISIT_TIME + 3

    def on_visit_msg_place(self, place_data):
        if not self._place:
            return
        else:
            update_method = {'char_name': self._place.set_owner_name,
               'wall_picture': self._place.set_wall_picture,
               'lobby_bgm': self._place.set_bgm,
               'lobby_skin_id': self._place.set_skin_id,
               'lobby_skybox_id': self._place.set_skybox_id,
               'lobby_mecha_info': self._place.set_mecha_info,
               'team_members': self._place.set_team_members,
               'display_mecha_info': self._place.set_display_mecha_info,
               'priv_lv': self._place.set_owner_priv_lv
               }
            for attr, value in six.iteritems(place_data):
                method = update_method.get(attr, None)
                method and method(value)

            return

    def get_all_puppet_info(self, with_teamate=True):
        if self._place:
            return self._place.get_all_puppet_info(with_teamate)
        else:
            return None

    def request_kick_visitor(self, uid):
        if not self._place:
            return
        visitors = self._place.get_all_puppet()
        if not visitors:
            return
        data = visitors.get(uid)
        if not data:
            return
        self.call_server_method('request_kick_visitor', (data.binary,))

    def on_visit_msg_add(self, member_dict):
        if not member_dict or not self._place:
            return
        for member_id, member_info in six.iteritems(member_dict):
            member_id = six.ensure_binary(member_id)
            id_obj = IdManager.bytes2id(member_id)
            self._place.create_puppet(IdManager.bytes2id(member_id), member_info)
            cur_time = tutil.get_server_time()
            teams = self.get_visit_team_members() or {}
            uid = member_info.get(U_ID)
            if cur_time > self.login_time and uid not in teams and self.is_visit_self() and uid != self.uid:
                global_data.game_mgr.show_tip(get_text_by_id(611578).format(name=member_info.get(C_NAME, '')))

        global_data.emgr.refresh_visit_player_info_event.emit()

    def on_visit_msg_del(self, member_id):
        member_id = six.ensure_binary(member_id)
        id_obj = IdManager.bytes2id(member_id)
        if id_obj == self.id:
            self.quit_visit()
        elif self._place:
            self._place.remove_puppet(id_obj)
        global_data.emgr.refresh_visit_player_info_event.emit()

    def on_visit_msg_update(self, member_id, update_info):
        member_id = six.ensure_binary(member_id)
        id_obj = IdManager.bytes2id(member_id)
        entity = EntityManager.getentity(id_obj)
        if entity and entity.logic:
            entity.logic.send_event('E_ON_UPDATE_LOBBY_USER_DATA', update_info)
        global_data.emgr.refresh_visit_player_info_event.emit()

    def on_visit_msg_telport(self, member_id, move_info):
        member_id = six.ensure_binary(member_id)
        eid = IdManager.bytes2id(member_id)
        entity = EntityManager.getentity(eid)
        if entity and entity.logic:
            entity.logic.send_event('E_SIMPLE_SYNC_TELPORT', move_info)

    def on_visit_msg_move(self, member_id, move_info):
        member_id = six.ensure_binary(member_id)
        eid = IdManager.bytes2id(member_id)
        entity = EntityManager.getentity(eid)
        if entity and entity.logic:
            entity.logic.send_event('E_SIMPLE_SYNC_MOVE', move_info)

    def on_visit_msg_action(self, member_id, method_name, args):
        member_id = six.ensure_binary(member_id)
        eid = IdManager.bytes2id(member_id)
        entity = EntityManager.getentity(eid)
        method = getattr(entity, method_name, None)
        method and method(*args)
        return

    def on_visit_ready(self):
        self._is_visit_ready = True
        global_data.lobby_player.send_event('E_FOOT_POSITION', math3d.vector(*self._born_position))
        self._process_msg_cache()

    def quit_visit(self):
        if not self._place:
            return
        else:
            is_visit_self = self.is_visit_self()
            self._place.destroy()
            self._place = None
            self._visit_msg_cache = []
            global_data.emgr.player_leave_visit_scene_event.emit()
            from logic.gutils.interaction_utils import clean_lobby_spray
            clean_lobby_spray()
            self.leave_lobby_to_visit(is_visit_self)
            global_data.emgr.visit_place_change_event.emit()
            return

    def _disconnect_visit(self):
        self.quit_visit()