# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/MPLobby.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.EntityManager import EntityManager
from mobile.client.ClientEntity import ClientEntity
from mobile.common.EntityFactory import EntityFactory
from ext_package.ext_decorator import get_default_mecha_fashion_decorator, get_default_mecha_shiny
from logic.gcommon.common_const.scene_const import SCENE_PVE_MAIN_UI

class MPLobby(ClientEntity):

    def __init__(self, entityid):
        super(MPLobby, self).__init__(entityid)
        self._puppets = {}
        self._puppet_pets = {}
        self._request_id = None
        self._owner_uid = None
        self._owner_name = None
        self._wall_picture = None
        self._lobby_skin_id = None
        self._lobby_skybox_id = None
        self._lobby_bgm = None
        self._lobby_mecha_info = {}
        self._team_members = {}
        return

    def init_from_dict(self, bdict):
        super(MPLobby, self).init_from_dict(bdict)
        self._request_id = bdict.get('request_id', None)
        self._owner_uid = bdict.get('owner_uid', None)
        self._owner_name = bdict.get('char_name', None)
        self._wall_picture = bdict.get('wall_picture', None)
        self._lobby_skin_id = bdict.get('lobby_skin_id', None)
        self._lobby_bgm = bdict.get('lobby_bgm', None)
        self._lobby_mecha_info = bdict.get('lobby_mecha_info', {})
        self._lobby_skybox_id = bdict.get('lobby_skybox_id', None)
        self._team_members = bdict.get('team_members', {})
        self.load_scene(bdict.get('scene_data', None))
        self._owner_priv_lv = bdict.get('priv_lv', 0)
        global_data.emgr.lobby_scene_pause_event += self.on_lobby_scene_pause
        return

    def get_owner_uid(self):
        return self._owner_uid

    def get_mecha_info(self):
        return self._lobby_mecha_info

    def set_owner_name(self, char_name):
        self._owner_name = char_name
        global_data.emgr.refresh_visit_name.emit(char_name)

    def get_owner_name(self):
        return self._owner_name

    def set_owner_priv_lv(self, priv_lv):
        self._owner_priv_lv = priv_lv
        global_data.emgr.refresh_visit_priv_lv.emit(priv_lv)

    def get_owner_priv_lv(self):
        return self._owner_priv_lv

    def set_mecha_info(self, lobby_mecha_info):
        if self._lobby_mecha_info != lobby_mecha_info:
            self._lobby_mecha_info = lobby_mecha_info
            global_data.emgr.lobby_mecha_display_reset.emit(True)

    def set_display_mecha_info(self, display_mecha_info):
        pass

    def get_mecha_id(self):
        return self._lobby_mecha_info.get('lobby_mecha_id', None)

    @get_default_mecha_fashion_decorator
    def get_mecha_fashion(self, mecha_item_id):
        return self._lobby_mecha_info.get('lobby_mecha_fashion_id', None)

    @get_default_mecha_shiny
    def get_mecha_shiny_weapon_id(self, mecha_item_id):
        return self._lobby_mecha_info.get('lobby_mecha_weapon_sfx', -1)

    def get_wall_picture(self):
        return self._wall_picture

    def set_wall_picture(self, wall_picture):
        if self._wall_picture != wall_picture:
            self._wall_picture = wall_picture
            global_data.emgr.housesys_wall_picture_change.emit()

    def get_skin_id(self):
        return self._lobby_skin_id

    def set_skin_id(self, lobby_skin_id):
        if self._lobby_skin_id != lobby_skin_id:
            self._lobby_skin_id = lobby_skin_id
            global_data.emgr.miaomiao_lobby_skin_change.emit()

    def get_bgm(self):
        return self._lobby_bgm

    def set_bgm(self, lobby_bgm):
        if self._lobby_bgm != lobby_bgm:
            self._lobby_bgm = lobby_bgm
            global_data.emgr.lobby_bgm_change.emit()

    def get_skybox_id(self):
        return self._lobby_skybox_id

    def set_skybox_id(self, lobby_skybox_id):
        if self._lobby_skybox_id != lobby_skybox_id:
            self._lobby_skybox_id = lobby_skybox_id
            global_data.emgr.privilege_lobby_skin_change.emit()

    def get_owner_team_idx(self):
        return self._team_members.get(self._owner_uid, {}).get('team_idx', -1)

    def get_team_members(self):
        return self._team_members

    def get_teammate_data(self, teammate_uid):
        return self._team_members.get(teammate_uid, None)

    def set_team_members(self, team_members):
        if self._team_members != team_members:
            self.del_teammate({teammate_uid:1 for teammate_uid in six.iterkeys(self._team_members)})
            self._team_members = team_members
            self.add_teammate(team_members)

    def add_teammate(self, team_dict):
        for teammate_uid, teammate_data in six.iteritems(team_dict):
            self._team_members[teammate_uid] = teammate_data
            if teammate_uid == self._owner_uid:
                continue
            global_data.emgr.visit_player_add_teammate_event.emit(teammate_data)

    def del_teammate(self, team_dict):
        for teammate_uid in six.iterkeys(team_dict):
            self._team_members.pop(teammate_uid, None)
            global_data.emgr.visit_player_del_teammate_event.emit(teammate_uid)

        return

    def update_teammate(self, team_dict):
        for teammate_uid, teammate_data in six.iteritems(team_dict):
            self._team_members.setdefault(teammate_uid, {}).update(teammate_data)
            global_data.emgr.visit_player_teammate_info_update_event.emit(teammate_uid, teammate_data)

    def load_scene(self, scene_data):
        if not scene_data:
            self.load_finish()
        else:
            scene_type = scene_data['scene_type']
            global_data.game_mgr.load_scene(scene_type, scene_data, self.load_finish)

    def load_finish(self, *args):
        if global_data.player and self._request_id:
            global_data.player.sync_visit_create(self._request_id)

    def create_puppet(self, eid, data):
        if EntityManager.getentity(eid):
            return
        puppet = EntityFactory.instance().create_entity('LobbyPuppet', eid)
        if not puppet:
            log_error('[MPLobby] creating MPLobby entity failed: cls - LobbyPuppet, eid - %s', eid)
            return
        puppet.init_from_dict(data)
        puppet.on_add_to_place(self.id)
        self._puppets[puppet.uid] = eid
        global_data.emgr.update_lobby_puppet_count.emit(len(self._puppets))
        self.create_puppet_pet(data)

    def create_puppet_pet(self, data):
        from logic.gcommon.cdata.pet_status_config import PT_IDLE
        from logic.units.LPet import LPet
        if global_data.game_mgr.scene and global_data.game_mgr.scene.scene_type == SCENE_PVE_MAIN_UI:
            return
        else:
            owner_uid = data['uid']
            cur_pet = self._puppet_pets.get(owner_uid)
            cur_pet_skin = cur_pet.ev_g_skin_id() if cur_pet else 0
            pet_info = data.get('pet_info', None)
            if pet_info:
                new_pet_skin = six_ex.keys(pet_info)[0] if 1 else 0
                if cur_pet_skin == new_pet_skin:
                    return
                self.remove_puppet_pet(owner_uid)
                if not new_pet_skin:
                    return
                owner_eid = self._puppets.get(owner_uid)
                if not owner_eid:
                    return
                owner = EntityManager.getentity(owner_eid)
                return owner or None
            new_pet = LPet(owner, None)
            new_pet.init_from_dict({'owner_id': owner_eid,
               'npc_id': 11001,'default_state': PT_IDLE,'pet_id': new_pet_skin,
               'level': pet_info[new_pet_skin].get('level', 1),'in_lobby': True
               })
            self._puppet_pets[owner_uid] = new_pet
            return

    def send_puppet_pet_event(self, uid, event_idx, args=(), kwargs=None):
        from logic.gcommon.common_utils.bcast_utils import idx_2_event_name
        cur_pet = self._puppet_pets.get(uid)
        if not cur_pet:
            return
        event_name = idx_2_event_name(event_idx)
        if kwargs and type(kwargs) is dict:
            cur_pet.send_event(event_name, *args, **kwargs)
        else:
            cur_pet.send_event(event_name, *args)

    def get_puppet(self, uid):
        if uid in self._puppets:
            return EntityManager.getentity(self._puppets[uid])
        else:
            return None
            return None

    def get_puppet_pet(self, uid):
        self._puppet_pets.get(uid, None)
        return

    def get_all_puppet(self):
        return self._puppets

    def get_all_puppet_info(self, with_teamate=True):
        ENTITY = EntityManager.getentity
        puppet_datas = {}
        for uid, eid in six.iteritems(self._puppets):
            if not with_teamate and uid in self._team_members:
                continue
            puppet = ENTITY(eid)
            if puppet and puppet.logic:
                puppet_datas[uid] = puppet.logic.ev_g_lobby_user_data()

        return puppet_datas

    def remove_puppet(self, eid):
        puppet = EntityManager.getentity(eid)
        if puppet:
            uid = puppet.uid
            self._puppets.pop(uid, None)
            puppet.destroy()
            self.remove_puppet_pet(uid)
        global_data.emgr.update_lobby_puppet_count.emit(len(self._puppets))
        return

    def remove_puppet_pet(self, uid):
        if uid in self._puppet_pets:
            pet = self._puppet_pets.pop(uid)
            pet.destroy()

    def clear_all_puppet(self):
        for eid in six.itervalues(self._puppets):
            puppet = EntityManager.getentity(eid)
            puppet and puppet.destroy()

        self._puppets = {}
        global_data.emgr.update_lobby_puppet_count.emit(len(self._puppets))

    def create_all_puppet_pet(self):
        for eid in six.itervalues(self._puppets):
            puppet = EntityManager.getentity(eid)
            if puppet and puppet.logic:
                self.create_puppet_pet(puppet.logic.ev_g_lobby_user_data())

    def clear_all_puppet_pet(self):
        for pet in six.itervalues(self._puppet_pets):
            pet.destroy()

        self._puppet_pets = {}

    def on_lobby_scene_pause(self, flag):
        if flag:
            self.clear_all_puppet_pet()
        else:
            self.create_all_puppet_pet()

    def on_destroy(self):
        self.clear_all_puppet()
        self.clear_all_puppet_pet()
        global_data.emgr.lobby_scene_pause_event -= self.on_lobby_scene_pause
        super(MPLobby, self).on_destroy()