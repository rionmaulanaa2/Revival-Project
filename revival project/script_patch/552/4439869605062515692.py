# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPet.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
import six
from mobile.common.RpcMethodArgs import List, Str, Float, Int, Dict, Bool
from logic.gutils.client_utils import post_method
import copy
from common.cfg import confmgr

class impPet(object):

    def _init_pet_from_dict(self, bdict):
        self.daily_state = bdict.get('daily_state', False)
        self.choosen_pet = bdict.get('choosen_pet', None)
        self.pet_enemy_visible = bdict.get('pet_enemy_visible', False)
        self.pve_choosen_pet = bdict.get('pve_choosen_pet', 0)
        self.pve_backup_pet_list = bdict.get('pve_backup_pet_list')
        if not self.pve_backup_pet_list:
            self.pve_backup_pet_list = [
             0, 0]
        sub_skin_choose_dict = bdict.get('pet_sub_skin_choose_dict', None) or {}
        self.sub_skin_choose_dict = {str(base_skin):str(sub_skin) for base_skin, sub_skin in six.iteritems(sub_skin_choose_dict)}
        return

    def get_choosen_pet(self):
        return self.choosen_pet

    def get_pet_sub_skin_choose(self, base_skin):
        base_skin = str(base_skin)
        if not self.sub_skin_choose_dict:
            return base_skin
        return self.sub_skin_choose_dict.get(base_skin, base_skin)

    def get_pet_daily_state(self):
        return self.daily_state

    def get_pet_enemy_visible(self):
        return self.pet_enemy_visible

    def get_pve_choosen_pet(self):
        return self.pve_choosen_pet

    def get_pve_backup_pet_pet_list(self):
        return copy.deepcopy(self.pve_backup_pet_list)

    def get_pve_pet_dict(self):
        if not self.pve_choosen_pet:
            self.pve_choosen_pet = 0
        if not self.pve_backup_pet_list:
            self.pve_backup_pet_list = [
             0, 0]
        pet_dict = {}
        pet_dict[0] = self.pve_choosen_pet
        pet_dict[1] = self.pve_backup_pet_list[0]
        pet_dict[2] = self.pve_backup_pet_list[1]
        return pet_dict

    def get_pet_daily_reward(self, pet_id):
        self.call_server_method('get_pet_daily_reward', (int(pet_id),))

    def set_choosen_pet(self, pet_id):
        self.call_server_method('set_choosen_pet', (pet_id,))

    def set_pet_sub_skin(self, pet_id):
        pet_id = str(pet_id)
        base_skin = str(confmgr.get('c_pet_info', pet_id, 'base_skin', default=pet_id))
        self.sub_skin_choose_dict[base_skin] = pet_id
        self.call_server_method('change_pet_sub_skin', (pet_id,))
        global_data.emgr.pet_sub_skin_changed.emit(base_skin, pet_id)

    def reset_choosen_pet(self):
        self.call_server_method('reset_choosen_pet', (0, ))

    def set_pet_enemy_visible(self, flag):
        self.pet_enemy_visible = flag
        self.call_server_method('set_pet_enemy_visible', (flag,))

    def set_pve_choosen_pet(self, pet_id):
        print (
         'set_pve_choosen_pet', pet_id)
        self.call_server_method('set_pve_choosen_pet', (pet_id,))

    def set_pve_backup_pet_list(self, backup_pet_list):
        print (
         'set_pve_backup_pet_list', backup_pet_list)
        self.call_server_method('set_pve_backup_pet_list', (backup_pet_list,))

    def try_upgrade_pet_skin(self, pet_id):
        self.call_server_method('try_upgrade_pet_skin', (int(pet_id),))

    @rpc_method(CLIENT_STUB, (Bool('state'),))
    def on_pet_daily_state(self, state):
        if self.daily_state ^ state:
            self.daily_state = state
            global_data.emgr.pet_daily_state_changed.emit(state)

    @rpc_method(CLIENT_STUB, (Int('choosen_pet'),))
    def choose_pet_res(self, choosen_pet):
        if self.choosen_pet != choosen_pet:
            self.choosen_pet = choosen_pet
            global_data.emgr.pet_choosen_changed.emit(choosen_pet)

    @rpc_method(CLIENT_STUB, ())
    def update_pet_info(self):
        global_data.emgr.pet_info_updated.emit()

    @rpc_method(CLIENT_STUB, (Int('choosen_pet'),))
    def choose_pve_pet_res(self, choosen_pet):
        if self.pve_choosen_pet != choosen_pet:
            self.pve_choosen_pet = choosen_pet
            global_data.emgr.pve_pet_choosen_changed.emit(choosen_pet)

    @rpc_method(CLIENT_STUB, (List('backup_pet_list'),))
    def choose_pve_backup_pet_list_res(self, backup_pet_list):
        if self.pve_backup_pet_list != backup_pet_list:
            self.pve_backup_pet_list = backup_pet_list
            global_data.emgr.pve_pet_backup_changed.emit(backup_pet_list)

    @rpc_method(CLIENT_STUB, (Int('origin_skin_id'), List('promote_skin_id_list')))
    def on_upgrade_pet_skin(self, origin_skin_id, promote_skin_id_list):
        global_data.emgr.pet_skin_promoted.emit()
        if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
            global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
        global_data.emgr.show_new_model_item.emit(promote_skin_id_list[0])