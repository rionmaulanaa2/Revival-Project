# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impRole.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.item.Fashion import Fashion
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, List, Dict
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE
from logic.gcommon.item.item_const import FASHION_POS_SUIT

class impRole(object):

    def _init_role_from_dict(self, bdict):
        self.role_id = bdict.get('role_id', None)
        self.fashion_scheme = {}
        self.role_top_skin_scheme = {}
        self._need_set_role_top_skin_id = None
        self._already_request_role_id_list = set()
        self.role_open_seq = bdict.get('role_open_seq', [])
        return

    def get_role(self):
        return self.role_id

    def get_role_open_seq(self):
        return self.role_open_seq

    def get_role_sex(self, role_id=None):
        from common.cfg import confmgr
        role_id = role_id or self.role_id
        return confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'sex')

    def get_role_list(self):
        items = self.get_items_by_type(L_ITEM_TYPE_ROLE)
        role_list = []
        for item in items:
            if item.can_use(self.sex, self.get_lv()):
                role_list.append(item.item_no)

        return role_list

    def has_role(self, role_id):
        return self.can_use_item_by_no(role_id)

    def has_permanent_role(self, role_id):
        if not role_id:
            return False
        item = self.get_item_by_no(role_id)
        if not item or not item.is_permanent_item():
            return False
        return True

    @rpc_method(CLIENT_STUB, (Int('role_id'),))
    def set_role(self, role_id):
        self.role_id = role_id
        global_data.emgr.update_role_id.emit(role_id)
        if global_data.lobby_player:
            global_data.lobby_player.send_event('E_REFRESH_LOBBY_PLAYER_MODEL')

    def try_set_role(self, role_id):
        self.call_server_method('set_role', (role_id,))

    def dress_role_fashion(self, fashion_parts):
        self.call_server_method('dress_role_fashion', (fashion_parts,))

    def dress_role_top_skin_fashion(self, skin_id):
        from logic.gutils import item_utils
        role_id = item_utils.get_lobby_item_belong_no(skin_id)
        if self.check_need_request_role_top_skin_scheme(role_id):
            self._need_set_role_top_skin_id = (
             role_id, skin_id)
            self.request_role_skin_scheme(role_id)
        else:
            self._set_role_top_skin_id(role_id, skin_id)

    def _set_role_top_skin_id(self, role_id, skin_id):
        item_data = global_data.player.get_item_by_no(role_id)
        if not item_data:
            return
        from logic.gutils import dress_utils
        skin_scheme = global_data.player.get_role_top_skin_scheme_br_role_and_skin(role_id, skin_id)
        new_scheme = dict(skin_scheme)
        for pos in six.iterkeys(new_scheme):
            if not new_scheme.get(pos):
                new_scheme.pop(pos)

        fashion_data = item_data.get_fashion()
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        undress_part = [ pos for pos in six.iterkeys(fashion_data) if pos != FASHION_POS_SUIT and pos not in new_scheme and bool(fashion_data[pos]) ]
        new_scheme.update({FASHION_POS_SUIT: skin_id})
        self.dress_role_fashion(new_scheme)
        if undress_part:
            self.undress_role_fashion(role_id, undress_part)

    def undress_role_fashion(self, role_id, parts_list):
        self.call_server_method('undress_role_fashion', (role_id, parts_list))

    def sa_log_buy_confirm(self, log_info):
        self.call_server_method('client_sa_log', ('BuyConformInMall', log_info))

    def try_equip_role_sfx(self, equip_dict):
        self.call_server_method('try_equip_role_sfx', (equip_dict,))

    def try_set_voice_item_use_state(self, voice_item_id, state):
        self.call_server_method('try_set_voice_item_use_state', (voice_item_id, state))

    def upload_fashion_scheme(self, fashion_id, scheme):
        fashion_id = str(fashion_id)
        self.fashion_scheme[fashion_id] = scheme
        self.call_server_method('upload_fashion_scheme', (fashion_id, scheme))

    def request_fashion_scheme(self, fashion_id):
        fashion_id = str(fashion_id)
        self.call_server_method('request_fashion_scheme', (fashion_id,))

    @rpc_method(CLIENT_STUB, (Str('fashion_id'), List('scheme')))
    def respon_fashion_scheme(self, fashion_id, scheme):
        self.fashion_scheme[fashion_id] = scheme
        global_data.emgr.response_fashion_scheme_event.emit(fashion_id)

    def get_fashion_scheme(self, fashion_id):
        return self.fashion_scheme.get(str(fashion_id), None)

    def upload_role_skin_scheme(self, role_id, fashion_id, scheme, change_sec_skin=False):
        from logic.gutils import dress_utils
        fashion_scheme = self.role_top_skin_scheme.setdefault(str(role_id), {})
        fashion_scheme[str(fashion_id)] = scheme
        skin_plan = dress_utils.fashion_dict_to_skin_plan(scheme)
        self.check_skin_plan(role_id, skin_plan)
        new_settings = {'version': self.settings_version,'fashion_scheme_settings.{}.{}'.format(role_id, fashion_id): skin_plan}
        if change_sec_skin:
            top_skin_id = dress_utils.get_top_skin_id_by_skin_id(fashion_id)
            top_skin_scheme = fashion_scheme.setdefault(str(top_skin_id), {})
            top_skin_scheme[FASHION_POS_SUIT] = scheme.get(FASHION_POS_SUIT, top_skin_id)
            top_skin_plan = dress_utils.fashion_dict_to_skin_plan(top_skin_scheme)
            new_settings.update({'fashion_scheme_settings.{}.{}'.format(role_id, top_skin_id): top_skin_plan})
        self.update_data(new_settings)
        global_data.emgr.role_top_skin_scheme_change_event.emit(role_id, int(fashion_id), scheme)

    def check_skin_plan(self, role_id, skin_plan):
        from logic.gutils import item_utils
        for i in range(1, len(skin_plan)):
            if skin_plan[i] and item_utils.get_lobby_item_belong_no(skin_plan[i]) != role_id:
                skin_plan[i] = 0

    def request_role_skin_scheme(self, role_id):
        if role_id not in self._already_request_role_id_list:
            self._already_request_role_id_list.add(int(role_id))
            fashion_scheme_setting = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('fashion_scheme_settings', {}).get(str(role_id), {})
            global_data.game_mgr.next_exec(self.imp_respon_role_fashion_scheme, role_id, fashion_scheme_setting)

    @rpc_method(CLIENT_STUB, (Int('role_id'), Dict('role_fashion_scheme')))
    def respon_role_fashion_scheme(self, role_id, role_fashion_scheme):
        self.imp_respon_role_fashion_scheme(role_id, role_fashion_scheme)

    def imp_respon_role_fashion_scheme(self, role_id, role_fashion_scheme):
        from logic.gutils import dress_utils
        role_skin = dress_utils.get_role_dress_clothing_id(role_id, check_default=True)
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(role_skin)
        from logic.gcommon.item.item_const import FASHION_DRESS_PARTS
        self.role_top_skin_scheme[str(role_id)] = {}
        for k, v in six.iteritems(role_fashion_scheme):
            self.check_skin_plan(role_id, v)
            fashion_dict, _ = dress_utils.skin_plan_to_fashion_dict(v)
            if str(k) == str(role_skin):
                role_decoration_data = dress_utils.get_role_fashion_data(role_id, role_skin, FASHION_DRESS_PARTS) or {}
                fashion_dict.update(role_decoration_data)
            self.role_top_skin_scheme[str(role_id)][str(k)] = fashion_dict

        self.check_skin_scheme_special_action(role_id)
        self.__check_top_skin_default_dec(role_id)
        global_data.emgr.response_role_top_skin_scheme_event.emit(role_id)
        if self._need_set_role_top_skin_id:
            role_id, skin_id = self._need_set_role_top_skin_id
            self._set_role_top_skin_id(role_id, skin_id)
            self._need_set_role_top_skin_id = None
        return

    def check_need_request_role_top_skin_scheme(self, role_id):
        return str(role_id) not in self.role_top_skin_scheme

    def get_or_request_role_top_skin_scheme(self, role_id):
        role_top_skin_scheme = self.role_top_skin_scheme.get(str(role_id), None)
        if role_top_skin_scheme is None:
            self.request_role_skin_scheme(role_id)
            return
        else:
            return role_top_skin_scheme
            return

    def get_role_top_skin_scheme_br_role_and_skin(self, role_id, top_skin_id):
        return self.role_top_skin_scheme.get(str(role_id), {}).get(str(top_skin_id), {})

    def check_has_set_skin_scheme(self, role_id, skin_id):
        has_set = self.role_top_skin_scheme.get(str(role_id), {}).get(str(skin_id), None)
        if has_set is None:
            return False
        else:
            return True
            return

    def install_role_skin_scheme(self, role_id, top_skin, preview_skin, fashion_parts):
        if self.check_need_request_role_top_skin_scheme(role_id):
            log_error('try to install_role_skin_scheme but fashion scheme is not request in advance')
            return
        else:
            fashion_scheme = self.role_top_skin_scheme.get(str(role_id), {})
            change_sec_skin = FASHION_POS_SUIT in fashion_parts and preview_skin != top_skin
            data = fashion_scheme.get(str(preview_skin), {})
            data.update(fashion_parts)
            self.upload_role_skin_scheme(role_id, preview_skin, data, change_sec_skin)
            if self.check_is_current_in_use_skin(role_id, preview_skin):
                self.dress_role_fashion(fashion_parts)
            elif self.check_is_current_in_use_top_skin(role_id, top_skin) and FASHION_POS_SUIT in fashion_parts:
                from logic.gutils import dress_utils
                from logic.gcommon.item.item_const import FASHION_DRESS_PARTS
                role_skin = dress_utils.get_role_dress_clothing_id(role_id, check_default=True)
                item_data = global_data.player.get_item_by_no(role_id)
                ori_fashion_data = item_data.get_fashion()
                real_undress_part_list = []
                for part in ori_fashion_data:
                    if not data.get(part, None):
                        real_undress_part_list.append(part)

                if real_undress_part_list:
                    self.undress_role_fashion(role_id, real_undress_part_list)
                if data:
                    self.dress_role_fashion(data)
            return

    def check_is_current_in_use_skin(self, role_id, cur_skin):
        from logic.gutils import dress_utils
        role_skin = dress_utils.get_role_dress_clothing_id(role_id, check_default=True)
        if role_skin == cur_skin:
            return True
        return False

    def check_is_current_in_use_top_skin(self, role_id, top_skin):
        from logic.gutils import dress_utils
        role_skin = dress_utils.get_role_dress_clothing_id(role_id, check_default=True)
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(role_skin)
        if top_skin_id == top_skin:
            return True
        return False

    def uninstall_role_skin_scheme(self, role_id, top_skin, preview_skin, fashion_part_list):
        if self.check_need_request_role_top_skin_scheme(role_id):
            log_error('try to uninstall_role_fashion_top_skin_scheme but fashion scheme is not request in advance')
            return
        fashion_scheme = self.role_top_skin_scheme.get(str(role_id), {})
        data = fashion_scheme.get(str(preview_skin), {})
        for p in fashion_part_list:
            if p in data:
                data.pop(p)

        from logic.gutils import dress_utils
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        sec_skin_id = data.get(FASHION_POS_SUIT, top_skin)
        completion_dec_dict = dress_utils.get_top_skin_need_completion_dec_dict(role_id, top_skin, data, sec_skin_id)
        data.update(completion_dec_dict)
        self.upload_role_skin_scheme(role_id, preview_skin, data)
        if self.check_is_current_in_use_skin(role_id, preview_skin):
            real_undress_part_list = []
            redress_dict = {}
            for part in fashion_part_list:
                if data.get(part):
                    redress_dict[part] = data[part]
                else:
                    real_undress_part_list.append(part)

            if real_undress_part_list:
                self.undress_role_fashion(role_id, real_undress_part_list)
            if redress_dict:
                self.dress_role_fashion(redress_dict)

    def get_role_dress_clothing_id(self, role_id):
        from logic.gutils import dress_utils
        from common.cfg import confmgr
        chosen_item = dress_utils.get_role_dress_clothing_id(role_id)
        if chosen_item is None:
            return confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
        else:
            return chosen_item

    def check_is_valid_skin_scheme(self, role_id, top_skin, fashion_parts):
        from logic.gutils import dress_utils
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, REPEL_FASHION
        fashion_item_no = fashion_parts.get(FASHION_POS_SUIT)
        skin_id = fashion_item_no if fashion_item_no else top_skin
        for pos, item_no in six.iteritems(fashion_parts):
            if not item_no:
                continue
            if not self.has_item_by_no(item_no):
                log_error('try to use item no that was not owned !!!!', item_no)
                return False
            if not dress_utils.check_valid_decoration(skin_id, item_no):
                log_error('try to use incompatible item !!!!', item_no, skin_id)
                return False
            repel_pos_list = REPEL_FASHION.get(pos, [])
            for r_pos in repel_pos_list:
                if fashion_parts.get(r_pos):
                    log_error('try to use incompatible decorations together !!!!', fashion_parts)
                    return False

        return True

    def check_skin_scheme_special_action(self, role_id):
        from common.cfg import confmgr
        top_skin_list = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'skin_list')
        for top_skin_id in top_skin_list:
            self.check_default_decoration_action_for_skin(top_skin_id)

    def check_default_decortion_action_for_dec(self, item_no):
        from logic.gcommon.item import lobby_item_type
        from logic.gutils import item_utils
        role_id = item_utils.get_lobby_item_belong_no(item_no)
        if role_id:
            self.check_skin_scheme_special_action(role_id)

    def check_default_decoration_action_for_skin(self, top_skin_id):
        from common.cfg import confmgr
        if not confmgr.get('lobby_item_with_reward', str(top_skin_id), 'extra_reward_id', default=None):
            return
        else:
            if not global_data.player.has_item_by_no(top_skin_id):
                return
            from logic.gutils import item_utils
            from logic.gutils import dress_utils
            from logic.gcommon.item import lobby_item_type
            role_id = item_utils.get_lobby_item_belong_no(top_skin_id)
            if self.check_need_request_role_top_skin_scheme(role_id):
                self.request_role_skin_scheme(role_id)
                return
            has_set = self.check_has_set_skin_scheme(role_id, top_skin_id)
            if has_set:
                return
            reward_dec_dict = {}
            extra_reward_id = confmgr.get('lobby_item', str(top_skin_id), 'extra_reward_id', default=None)
            if extra_reward_id:
                reward_ls = confmgr.get('common_reward_data', str(extra_reward_id), 'reward_list', default=[])
                for item_no, item_num in reward_ls:
                    l_item_type = item_utils.get_lobby_item_type(item_no)
                    if l_item_type in lobby_item_type.ITEM_TYPE_DEC:
                        fashion_pos = dress_utils.get_lobby_type_fashion_pos(l_item_type)
                        if fashion_pos is not None:
                            reward_dec_dict[fashion_pos] = item_no

            for reward_item_no in six.itervalues(reward_dec_dict):
                if not global_data.player.has_item_by_no(reward_item_no):
                    log_error('has Skin ', top_skin_id, 'but not reward id', reward_item_no)
                    return

            if reward_dec_dict:
                self.install_role_skin_scheme(role_id, top_skin_id, top_skin_id, reward_dec_dict)
            return

    def __check_top_skin_default_dec(self, role_id):
        from common.cfg import confmgr
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        top_skin_list = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'skin_list')
        sec_skin_conf = confmgr.get('top_role_skin_conf', default={})
        for top_skin_id in top_skin_list:
            for sec_skin_id in sec_skin_conf.get(str(top_skin_id), []):
                from logic.gutils import dress_utils
                current_dict = self.role_top_skin_scheme.get(str(role_id), {}).get(str(sec_skin_id), {})
                completion_dec_dict = dress_utils.get_top_skin_need_completion_dec_dict(role_id, top_skin_id, current_dict, sec_skin_id)
                if completion_dec_dict:
                    self.install_role_skin_scheme(role_id, top_skin_id, sec_skin_id, completion_dec_dict)