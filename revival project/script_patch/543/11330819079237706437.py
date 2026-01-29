# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMechaSkinShare.py
from __future__ import absolute_import
import six
from logic.gutils.item_utils import get_item_rare_degree
from logic.gutils.mecha_skin_utils import get_mecha_base_skin_id, is_default_mecha_skin, get_mecha_shiny_weapon_list, get_skin_lst
from logic.gcommon.item import item_const as iconst
from logic.gutils.mecha_utils import get_own_mecha_lst, get_mecha_lst
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from logic.gcommon.const import SKIN_SHARE_TYPE_INTIMACY, SKIN_SHARE_TYPE_PRIV
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, get_mecha_item_default_fashion
from logic.gutils.item_utils import get_lobby_item_belong_no
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict

class impMechaSkinShare(object):

    def _init_mechaskinshare_from_dict(self, bdict):
        self.priv_mecha_fashion_dict = {}
        self.intimacy_share_mechas = []
        self.chosen_pve_share_skin = {}
        self.register_mecha_skin_share_team_event()

    def register_mecha_skin_share_team_event(self):
        global_data.emgr.player_add_teammate_event += self.on_mechaskinshare_add_teammate
        global_data.emgr.player_del_teammate_event += self.on_mechaskinshare_del_teammate
        global_data.emgr.player_teammate_info_update_event += self.on_mechaskinshare_update_teammate
        global_data.emgr.player_join_team_event += self.on_mechaskinshare_add_teammate
        global_data.emgr.player_leave_team_event += self.on_mechaskinshare_del_teammate

    def on_mechaskinshare_add_teammate(self, *args):
        self.priv_mecha_fashion_dict = self.calc_priv_share_skins()
        self.intimacy_share_mechas = self.calc_intimacy_share_mechas()
        global_data.emgr.refresh_share_skin_event.emit()
        global_data.emgr.update_skin_share_state.emit()

    def on_mechaskinshare_del_teammate(self, *args):
        if not self.is_in_team():
            self.priv_mecha_fashion_dict = {}
            self.intimacy_share_mechas = []
        else:
            self.priv_mecha_fashion_dict = self.calc_priv_share_skins()
            self.intimacy_share_mechas = self.calc_intimacy_share_mechas()
        skin_id = self.chosen_pve_share_skin.get('mecha_fashion', {}).get(FASHION_POS_SUIT)
        lobby_mecha_id = self.get_pve_selected_mecha_item_id()
        battle_mecha_id = self.get_pve_select_mecha_id()
        available_skins = self.priv_mecha_fashion_dict.get('mecha_skin_ids', {})
        right_mecha_id = True
        if not self.get_item_by_no(lobby_mecha_id) and battle_mecha_id not in self.intimacy_share_mechas:
            self.set_chosen_pve_share_fashion({})
            clothing_id = get_mecha_item_default_fashion(101008001)
            global_data.player.install_mecha_main_skin_scheme(101008001, clothing_id, {FASHION_POS_SUIT: clothing_id})
            if not self.is_in_battle():
                global_data.emgr.on_pve_mecha_show_changed.emit(8001)
            right_mecha_id = False
        elif skin_id and not self.get_item_by_no(skin_id) and skin_id not in available_skins:
            self.set_chosen_pve_share_fashion({})
            global_data.emgr.undress_priv_skin_event.emit(self.get_pve_select_mecha_id())
            global_data.game_mgr.show_tip(get_text_by_id(83531))
            ui = global_data.ui_mgr.get_ui('PVELevelWidgetUI')
            if not (ui and ui.is_showing_skin_choose_widget()):
                global_data.emgr.refresh_share_mecha_skin.emit(self.get_pve_select_mecha_id())
        global_data.emgr.update_skin_share_state.emit()
        if right_mecha_id and not self.is_in_battle():
            global_data.emgr.on_pve_mecha_show_changed.emit(battle_mecha_id)
        ui = global_data.ui_mgr.get_ui('PVELevelWidgetUI')
        if ui and ui.is_showing_skin_choose_widget():
            from logic.gutils.pve_utils import update_model_and_cam_pos
            from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVESelectLevelMechaWidget import OFF_MODEL_POSITION, OFF_POSITION
            update_model_and_cam_pos(OFF_POSITION, OFF_MODEL_POSITION)

    def on_mechaskinshare_update_teammate(self, uid, uinfo):
        if not uinfo:
            return
        if 'priv_mecha_fashions' in uinfo or 'priv_share_setting' in uinfo or 'priv_share_lobby_setting' in uinfo:
            self.priv_mecha_fashion_dict = self.calc_priv_share_skins()

    def calc_priv_share_skins(self):
        if not self.is_in_team():
            return {}
        team_info = self.get_team_info() or {}
        members = team_info.get('members', {})
        if not members:
            return {}
        mecha_fashion_dict = {}
        for uid, info in six.iteritems(members):
            if not info.get('priv_mecha_fashions'):
                continue
            if not info.get('priv_share_setting', False):
                continue
            priv_mecha_fashions = info.get('priv_mecha_fashions', {})
            lobby_mecha_skin = info.get('lobby_mecha_info', {}).get('lobby_mecha_fashion_id', 0)
            if not info.get('priv_share_lobby_setting', False):
                if lobby_mecha_skin:
                    priv_mecha_fashions['lobby_skin_ids'] = [
                     lobby_mecha_skin]
                    if get_item_rare_degree(lobby_mecha_skin) in (iconst.RARE_DEGREE_5,):
                        base_skin_id = get_mecha_base_skin_id(lobby_mecha_skin)
                        if base_skin_id != lobby_mecha_skin:
                            priv_mecha_fashions['lobby_skin_ids'].append(base_skin_id)
            else:
                priv_mecha_fashions['lobby_skin_ids'] = []
            if not mecha_fashion_dict:
                mecha_fashion_dict.update(priv_mecha_fashions)
            else:
                skin_ids = mecha_fashion_dict.get('mecha_skin_ids', {})
                skin_ids.update(priv_mecha_fashions.get('mecha_skin_ids', {}))
                wsfx_ids = mecha_fashion_dict.get('mecha_wsfx_ids', {})
                wsfx_ids.update(priv_mecha_fashions.get('mecha_wsfx_ids', {}))
                lobby_skin_ids = mecha_fashion_dict.get('lobby_skin_ids', [])
                cur_lobby_skin_ids = priv_mecha_fashions.get('lobby_skin_ids', [])
                lobby_skin_ids.extend(cur_lobby_skin_ids)
                mecha_fashion_dict['lobby_skin_ids'] = list(set(lobby_skin_ids))

        return mecha_fashion_dict

    def calc_intimacy_share_mechas(self):
        if not self.is_in_team():
            return []
        team_info = self.get_team_info() or {}
        members = team_info.get('members', {})
        if not members:
            return {}
        share_mechas = []
        own_mechas = get_own_mecha_lst()
        for uid, info in six.iteritems(members):
            teammate_mecha_ids = list(info.get('mecha_dict', {}).keys())
            if not teammate_mecha_ids:
                continue
            if not self.is_mecha_share_friend(uid):
                continue
            cur_share_mechas = list(set(teammate_mecha_ids).difference(set(own_mechas)))
            if cur_share_mechas:
                share_mechas.extend(cur_share_mechas)

        return share_mechas

    def set_chosen_pve_share_fashion(self, skin_data):
        self.chosen_pve_share_skin = skin_data
        self.call_server_method('set_chosen_pve_share_skin', (skin_data,))

    @rpc_method(CLIENT_STUB, (Dict('skin_data'),))
    def on_set_chosen_pve_share_fashion(self, skin_data):
        self.chosen_pve_share_skin = skin_data

    def get_pve_using_mecha_skin(self, lobby_mecha_id):
        battle_mecha_id = mecha_lobby_id_2_battle_id(lobby_mecha_id)
        if not self.chosen_pve_share_skin:
            if self.is_in_battle():
                _, _, share_mechas = get_mecha_lst()
            else:
                share_mechas = self.intimacy_share_mechas
            if battle_mecha_id in share_mechas:
                return get_mecha_item_default_fashion(lobby_mecha_id)
            else:
                return self.get_mecha_fashion(lobby_mecha_id)

        else:
            share_skin = self.chosen_pve_share_skin.get('mecha_fashion', {}).get(FASHION_POS_SUIT)
            cur_mecha_skin_list = get_skin_lst(battle_mecha_id)
            if share_skin not in cur_mecha_skin_list:
                if battle_mecha_id in self.intimacy_share_mechas:
                    return get_mecha_item_default_fashion(lobby_mecha_id)
                else:
                    return self.get_mecha_fashion(lobby_mecha_id)

            else:
                return self.chosen_pve_share_skin.get('mecha_fashion', {}).get(FASHION_POS_SUIT)

    def get_share_mecha_fashion_data(self, skin_id):
        if self.is_intimacy_share(skin_id):
            return {}
        if self.is_priv_share(skin_id):
            mecha_fashion = {FASHION_POS_SUIT: skin_id}
            free_wsfx_id = self.get_free_wsfx_id(skin_id)
            mecha_wsfx_ids = self.priv_mecha_fashion_dict.get('mecha_wsfx_ids', {})
            has_free_wsfx_id = free_wsfx_id in mecha_wsfx_ids
            if has_free_wsfx_id:
                mecha_fashion[FASHION_POS_WEAPON_SFX] = free_wsfx_id
            return {'mecha_fashion': mecha_fashion,
               'is_priv_free': True
               }
        return {}

    def is_share_mecha_skin(self, skin_id):
        if self.is_intimacy_share(skin_id):
            return (True, SKIN_SHARE_TYPE_INTIMACY)
        else:
            if self.is_priv_share(skin_id):
                return (True, SKIN_SHARE_TYPE_PRIV)
            return (False, None)

    def is_priv_share(self, skin_id):
        if self.get_priv_enjoy_free_cnt() <= 0:
            return False
        lobby_mecha_id = get_lobby_item_belong_no(skin_id)
        if is_default_mecha_skin(skin_id, lobby_mecha_id):
            return False
        mecha_skin_ids = self.priv_mecha_fashion_dict.get('mecha_skin_ids', {})
        mecha_wsfx_ids = self.priv_mecha_fashion_dict.get('mecha_wsfx_ids', {})
        if skin_id not in mecha_skin_ids:
            return False
        skin_item = self.get_item_by_no(skin_id)
        if not skin_item:
            return True
        wsfx_id = skin_item.get_weapon_sfx()
        if wsfx_id:
            return False
        free_wsfx_id = self.get_free_wsfx_id(skin_id)
        has_free_wsfx_id = free_wsfx_id in mecha_wsfx_ids
        if has_free_wsfx_id:
            return True
        return False

    def is_intimacy_share(self, skin_id):
        lobby_mecha_id = get_lobby_item_belong_no(skin_id)
        if is_default_mecha_skin(skin_id, lobby_mecha_id):
            battle_mecha_id = mecha_lobby_id_2_battle_id(lobby_mecha_id)
            if battle_mecha_id in self.intimacy_share_mechas:
                return True
        return False

    def mecha_skin_share_on_pve_mecha_change(self):
        ui = global_data.ui_mgr.get_ui('PVELevelWidgetUI')
        if ui and ui.is_showing_skin_choose_widget():
            from logic.gutils.pve_utils import update_model_and_cam_pos
            from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVESelectLevelMechaWidget import OFF_MODEL_POSITION, OFF_POSITION
            update_model_and_cam_pos(OFF_POSITION, OFF_MODEL_POSITION)

    def get_free_wsfx_id(self, skin_id):
        free_wsfx_id = None
        shiny_weapon_list = get_mecha_shiny_weapon_list(skin_id)
        for w_sfx in reversed(shiny_weapon_list):
            if w_sfx in self.priv_mecha_fashion_dict.get('mecha_wsfx_ids', {}):
                free_wsfx_id = w_sfx

        return free_wsfx_id

    def is_teammate_lobby_skin(self, skin_id):
        lobby_skin_ids = self.priv_mecha_fashion_dict.get('lobby_skin_ids', {})
        return skin_id in lobby_skin_ids

    def is_intimacy_share_mecha(self, lobby_mecha_id):
        battle_mecha_id = mecha_lobby_id_2_battle_id(lobby_mecha_id)
        return battle_mecha_id in self.intimacy_share_mechas