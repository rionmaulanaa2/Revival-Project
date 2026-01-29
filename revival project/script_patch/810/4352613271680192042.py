# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMecha.py
from __future__ import absolute_import
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.mecha_skin_utils import get_mecha_base_skin_id
from logic.gcommon.common_const import mecha_const
from logic.gutils.charm_utils import show_charm_up_tips_and_update_charm_value, show_charm_tips
from logic.gcommon import time_utility as tutil
from logic.gutils import skin_define_utils
from logic.gutils import dress_utils
from logic.gcommon.common_utils import decal_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils.local_text import get_text_by_id

class impMecha(object):

    def _init_mecha_from_dict(self, bdict):
        self.usual_mecha_ids = bdict.get('usual_mecha_ids', [])
        self._sss_fashion = bdict.get('sss_fashion') or {}
        self.mecha_use_time = {mecha_id:t for mecha_id, t in bdict.get('mecha_use_time', [])}
        self.mecha_main_skin_scheme = {}
        self.mecha_decal = decal_utils.decode_decal_dict(bdict.get('mecha_decal', {}))
        self.mecha_color = decal_utils.decode_color_dict(bdict.get('mecha_color', {}))
        self.mecha_sub_skin = bdict.get('mecha_sub_skin', {})
        self._mecha_custom_skin_open = bdict.get('mecha_custom_skin_open', False)
        self._last_share_mecha_skin_time = bdict.get('last_share_mecha_time', 0)
        self._last_share_mecha_skin_time_frd = 0
        self._is_apply_mecha_pose = bdict.get('apply_mecha_pose_show', 0)
        self._pve_selected_mecha_item_id = bdict.get('pve_mecha_id')
        if self._pve_selected_mecha_item_id is None:
            self._pve_selected_mecha_item_id = 101008001
        self._pve_selected_mecha_id = dress_utils.mecha_lobby_id_2_battle_id(self._pve_selected_mecha_item_id)
        self.lock_decal = False
        self.lock_color = False
        self.need_update_skin_define = False
        self.mecha_pose = bdict.get('mecha_pose', {})
        self.mecha_skin_kill_cnt = bdict.get('mecha_skin_kill_cnt', {})
        self.mecha_skin_dress_record = bdict.get('mecha_skin_dress_record', {})
        return

    def get_mecha_fashion(self, mecha_id):
        item = self.get_item_by_no(mecha_id)
        if not item:
            return DEFAULT_CLOTHING_ID
        fashion = item.get_fashion()
        return fashion.get(FASHION_POS_SUIT, DEFAULT_CLOTHING_ID)

    def get_replace_clothing_id(self, base_skin_id):
        if str(base_skin_id) in self._sss_fashion:
            return self._sss_fashion[str(base_skin_id)]
        return base_skin_id

    def get_lobby_mecha_skin(self):
        mecha_item_id = self.get_lobby_selected_mecha_item_id()
        return self.get_mecha_fashion(mecha_item_id)

    def get_mecha_skin_kill_cnt(self, mecha_skin_id):
        mecha_skin_kill_cnt = self.mecha_skin_kill_cnt.get(str(mecha_skin_id), {})
        return mecha_skin_kill_cnt.copy()

    def dress_mecha_fashion(self, fashion_parts):
        if FASHION_POS_SUIT in fashion_parts:
            skin_id = fashion_parts.get(FASHION_POS_SUIT)
            base_skin_id = get_mecha_base_skin_id(skin_id)
            if base_skin_id:
                self.select_sss_fashion(base_skin_id, skin_id)
        self.call_server_method('dress_mecha_fashion', (fashion_parts,))

    def try_set_mecha_sfx(self, mecha_id, sfx_id):
        self.call_server_method('set_mecha_sfx', (mecha_id, sfx_id))

    def try_set_mecha_action(self, mecha_id, action_id):
        self.call_server_method('set_mecha_action', (mecha_id, action_id))

    def install_mecha_main_skin_scheme(self, mecha_id, main_skin_id, fashion_parts):
        if self.check_need_request_mecha_main_skin_scheme(mecha_id):
            log_error('try to install_mecha_main_skin_scheme but fashion scheme is not request in advance')
            return
        fashion_scheme = self.mecha_main_skin_scheme.get(str(mecha_id), {})
        data = fashion_scheme.get(str(main_skin_id), {})
        data.update(fashion_parts)
        self.upload_mecha_main_skin_scheme(mecha_id, main_skin_id, data)
        self.dress_mecha_fashion(fashion_parts)

    def check_need_request_mecha_main_skin_scheme(self, mecha_id):
        return False

    def upload_mecha_main_skin_scheme(self, mecha_id, main_skin_id, scheme):
        cur_skin_id = scheme.get(FASHION_POS_SUIT, None)
        if cur_skin_id:
            self.set_mecha_sub_skin(cur_skin_id)
        global_data.emgr.mecha_main_skin_scheme_change_event.emit(mecha_id, main_skin_id, scheme)
        return

    def request_mecha_main_skin_scheme(self, mecha_id):
        pass

    def check_is_current_in_use_main_skin(self, mecha_id, main_skin_id):
        mecha_skin = dress_utils.get_mecha_dress_clothing_id(mecha_id)
        main_skin = skin_define_utils.get_main_skin_id(mecha_skin)
        if main_skin == main_skin_id:
            return True
        return False

    def set_usual_mecha(self, usual_mecha_ids):
        if usual_mecha_ids is not None:
            self.call_server_method('set_usual_mecha', (usual_mecha_ids,))
        return

    @rpc_method(CLIENT_STUB, (Bool('result'), List('usual_mecha_ids'), Bool('notify')))
    def on_usual_mecha_result(self, result, usual_mecha_ids, notify=True):
        self.usual_mecha_ids = usual_mecha_ids
        global_data.emgr.on_set_usual_mecha_result.emit(result, notify)

    def get_usual_mecha_ids(self):
        if self.usual_mecha_ids:
            return [ x for x in self.usual_mecha_ids ]
        default_ids = [
         8001, 8005, 8006]
        if not global_data.player:
            return default_ids
        if global_data.player.in_local_battle():
            return [8001]
        if global_data.player.in_new_local_battle():
            return global_data.player.get_new_local_battle_mecha_ids()
        uid = global_data.player.uid
        player_info = global_data.message_data.get_player_detail_inf(uid) or {}
        top_mecha_info = player_info.get('top_mechas', [])
        top_mecha_ids = [ mecha_id for mecha_id, mecha_lv in top_mecha_info ]
        if not top_mecha_ids:
            return default_ids
        need_max_num = mecha_const.MECHA_USUAL_USE_MECHA_MAX_SET_NUM
        if len(top_mecha_ids) < need_max_num:
            for mecha_id in default_ids:
                if mecha_id not in top_mecha_ids and len(top_mecha_ids) < need_max_num:
                    top_mecha_ids.append(mecha_id)

        elif len(top_mecha_ids) > need_max_num:
            top_mecha_ids = top_mecha_ids[:need_max_num]
        return top_mecha_ids

    def select_sss_fashion(self, base_fashion_id, cur_fashion_id):
        self.call_server_method('select_sss_fashion', (base_fashion_id, cur_fashion_id))

    def try_upgrade_mecha_fashion(self, fashion_id):
        self.call_server_method('try_upgrade_mecha_fashion', (fashion_id,))

    def try_equip_mecha_shiny_weapon(self, equip_dict):
        self.call_server_method('try_equip_mecha_weapon_sfx', (equip_dict,))

    @rpc_method(CLIENT_STUB, (Int('fashion_no'), List('geted_item_list')))
    def on_upgrade_mecha_fashion(self, fashion_no, geted_item_list):
        for item_no in geted_item_list:
            if get_lobby_item_type(item_no) != L_ITEM_TYPE_MECHA_SKIN:
                continue
            if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
            global_data.emgr.show_new_model_item.emit(item_no)

        if geted_item_list:
            show_charm_up_tips_and_update_charm_value([(geted_item_list[0], 1)])

    def set_sss_base_fashion_info(self, base_fashion_id, cur_fashion_id):
        self._sss_fashion[str(base_fashion_id)] = cur_fashion_id

    @rpc_method(CLIENT_STUB, (List('mecha_ids'),))
    def update_mecha_use_time(self, mecha_ids):
        now = tutil.get_server_time()
        for mecha_id in mecha_ids:
            self.mecha_use_time[int(mecha_id)] = now

    def get_mecha_use_time(self):
        return self.mecha_use_time

    def get_mecha_decal(self):
        return self.mecha_decal

    def get_mecha_color(self):
        return self.mecha_color

    def get_lock_color(self):
        return self.lock_color

    def get_lock_decal(self):
        return self.lock_decal

    def get_need_update_skin_define(self):
        return self.need_update_skin_define

    def set_need_update_skin_define(self, is_need):
        self.need_update_skin_define = is_need

    def get_mecha_sub_skin(self):
        return self.mecha_sub_skin

    def set_mecha_sub_skin(self, skin_id):
        main_skin_id = skin_define_utils.get_main_skin_id(skin_id)
        self.mecha_sub_skin[str(main_skin_id)] = skin_id
        self.call_server_method('set_mecha_sub_skin', (skin_id,))

    def add_mecha_decal(self, skin_id, decal_list):
        self.lock_decal = True
        decal_list = decal_utils.encode_decal_list(decal_list)
        ori_decal_list = self.mecha_decal.get(str(skin_id), [])
        ori_num = len(ori_decal_list)
        self.call_server_method('add_mecha_decal', (skin_id, ori_num, decal_list))

    @rpc_method(CLIENT_STUB, (Int('result'), Int('skin_id'), List('decal_list')))
    def add_mecha_decal_result(self, result, skin_id, decal_list):
        self.lock_decal = False
        if result and not self.lock_color:
            global_data.emgr.skin_define_batch_buy_event.emit()
        if result:
            data = self.mecha_decal.setdefault(str(skin_id), [])
            data += decal_utils.decode_decal_list(decal_list)
            global_data.emgr.add_mecha_decal_result_event.emit()

    def mod_mecha_decal(self, skin_id, index, decal):
        decal = decal_utils.encode(*decal)
        self.call_server_method('mod_mecha_decal', (skin_id, index, decal))

    @rpc_method(CLIENT_STUB, (Int('result'), Int('skin_id'), Int('index'), List('decal')))
    def mod_mecha_decal_result(self, result, skin_id, index, decal):
        if result:
            data = self.mecha_decal.get(str(skin_id))
            if not data:
                return
            data[index] = decal_utils.decode(*decal)

    def del_mecha_decal(self, skin_id, index):
        ori_decal_list = self.mecha_decal.get(str(skin_id), [])
        ori_num = len(ori_decal_list)
        self.call_server_method('del_mecha_decal', (skin_id, ori_num, index))

    @rpc_method(CLIENT_STUB, (Int('result'), Int('skin_id'), Int('index')))
    def del_mecha_decal_result(self, result, skin_id, index):
        if result:
            data = self.mecha_decal.get(str(skin_id))
            if not data or not 0 <= index < len(data):
                return
            if len(data) == 1:
                del self.mecha_decal[str(skin_id)]
            else:
                data.pop(index)
            global_data.emgr.del_mecha_decal_result_event.emit()

    def set_mecha_color(self, skin_id, color):
        self.lock_color = True
        ori_color = self.mecha_color.get(str(skin_id), {})
        diff_color = decal_utils.cal_diff_color(ori_color, color)
        diff_color = decal_utils.encode_color(diff_color)
        self.call_server_method('set_mecha_color', (skin_id, diff_color))

    @rpc_method(CLIENT_STUB, (Int('result'), Int('skin_id'), Dict('color')))
    def set_mecha_color_result(self, result, skin_id, color):
        self.lock_color = False
        if result and not self.lock_decal:
            global_data.emgr.skin_define_batch_buy_event.emit()
        if result:
            color = decal_utils.decode_color(color)
            self.mecha_color.setdefault(str(skin_id), {}).update(color)
            global_data.emgr.set_mecha_color_result_event.emit()

    def mecha_custom_skin_open(self):
        return self._mecha_custom_skin_open

    def share_mecha_custom_skin(self, title, skin_id, frd_uid, head_info):
        now = tutil.get_server_time()
        if frd_uid > 0:
            if now < self._last_share_mecha_skin_time_frd + chat_const.WORLD_SHARE_SKIN_INTERVAL_FRD:
                global_data.game_mgr.show_tip(get_text_by_id(81968))
                return False
            self._last_share_mecha_skin_time_frd = now
        else:
            if now < self._last_share_mecha_skin_time + chat_const.WORLD_SHARE_SKIN_INTERVAL:
                global_data.game_mgr.show_tip(get_text_by_id(81968))
                return False
            self._last_share_mecha_skin_time = now
        self.call_server_method('share_mecha_skin', (title, skin_id, frd_uid, head_info))
        global_data.game_mgr.show_tip(get_text_by_id(81969))
        return True

    def get_mecha_pose(self):
        return self.mecha_pose

    def try_set_mecha_pose(self, mecha_id, pose_id):
        self.call_server_method('set_mecha_pose', (mecha_id, pose_id))

    @rpc_method(CLIENT_STUB, (Dict('mecha_pose'),))
    def set_mecha_pose_result(self, mecha_pose):
        self.mecha_pose = mecha_pose
        global_data.emgr.set_mecha_pose_result_event.emit()

    def try_del_mecha_pose(self, mecha_id):
        self.call_server_method('del_mecha_pose', (mecha_id,))

    @rpc_method(CLIENT_STUB, (Dict('mecha_pose'),))
    def del_mecha_pose_result(self, mecha_pose):
        self.mecha_pose = mecha_pose
        global_data.emgr.del_mecha_pose_result_event.emit()

    def is_apply_mecha_pose(self):
        return bool(self._is_apply_mecha_pose)

    @rpc_method(CLIENT_STUB, (Int('is_apply'),))
    def reply_apply_mecha_pose_show(self, is_apply):
        self._is_apply_mecha_pose = is_apply
        global_data.emgr.set_mecha_pose_apply_event.emit()

    def set_apply_mecha_pose_show(self, is_apply):
        self.call_server_method('set_apply_mecha_pose_show', (is_apply,))

    @rpc_method(CLIENT_STUB, (Dict('change_details'),))
    def on_mecha_skin_kill_count_change(self, change_details):
        self.mecha_skin_kill_cnt.update(change_details)

    @rpc_method(CLIENT_STUB, (Dict('change_details'),))
    def on_mecha_skin_dress_record_change(self, change_details):
        global_data.emgr.del_mecha_pose_result_event.emit()

    @rpc_method(CLIENT_STUB, (Int('mecha_id'),))
    def on_pve_mecha_changed(self, pve_mecha_id):
        self._pve_selected_mecha_item_id = pve_mecha_id
        self._pve_selected_mecha_id = dress_utils.mecha_lobby_id_2_battle_id(pve_mecha_id)
        global_data.emgr.on_pve_mecha_changed.emit(self._pve_selected_mecha_id)
        self.mecha_skin_share_on_pve_mecha_change()

    def pve_select_mecha(self, mecha_id):
        if not self._pve_selected_mecha_id:
            self._pve_selected_mecha_id = dress_utils.mecha_lobby_id_2_battle_id(self._pve_selected_mecha_item_id)
        if self._pve_selected_mecha_id == mecha_id:
            return
        pve_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(mecha_id)
        if not pve_mecha_id:
            return
        self.call_server_method('pve_select_mecha', (pve_mecha_id,))

    def get_pve_select_mecha_id(self):
        if not self._pve_selected_mecha_id:
            self._pve_selected_mecha_id = dress_utils.mecha_lobby_id_2_battle_id(self._pve_selected_mecha_item_id)
        return self._pve_selected_mecha_id

    def get_pve_selected_mecha_item_id(self):
        return self._pve_selected_mecha_item_id

    def set_pve_selected_mecha_id(self, mecha_id):
        self._pve_selected_mecha_id = mecha_id
        self._pve_selected_mecha_item_id = dress_utils.battle_id_to_mecha_lobby_id(mecha_id)
        global_data.emgr.on_pve_mecha_changed_in_battle.emit(self._pve_selected_mecha_id)

    def check_pve_selected_mecha_is_available(self):
        self.call_server_method('pve_select_mecha', (self._pve_selected_mecha_item_id,))

    def fix_shiny_weapon_id_error(self):
        item = self.get_item_by_no(101008026)
        if not item:
            return
        else:
            fashion = item.get_fashion()
            if fashion.get(FASHION_POS_SUIT, 0) == 201802652:
                sfx_id = fashion.get(FASHION_POS_WEAPON_SFX, 0)
                if sfx_id and sfx_id != 201802662:
                    self.try_equip_mecha_shiny_weapon({201802652: None
                       })
            return