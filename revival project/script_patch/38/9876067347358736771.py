# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGroup.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
from logic.units.LAvatar import LAvatar
import weakref
import game3d
import logic.gcommon.const as const
_HASH_xray_color = game3d.calc_string_hash('xray_color')
from ...cdata import status_config
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from time import time
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.common_utils import battle_utils
from logic.gutils import dress_utils
import copy
from logic.gcommon.common_const import attr_const
from logic.gcommon.common_const.voice_const import CLOSE_CHANNEL, TEAM_CHANNEL, GROUP_CHANNEL

class ComGroup(UnitCom):
    BIND_EVENT = {'E_SET_GROUP_ID': '_set_group_id',
       'G_IS_GROUPMATE': '_is_groupmate',
       'G_GROUPMATE': '_groupmates',
       'G_GROUPMATE_TIMESTAMP': '_get_groupmate_timestamp',
       'G_GROUPMATE_UIDS': '_get_groupmate_uids',
       'G_GROUP_ID': '_get_group_id',
       'E_HUMAN_MODEL_LOADED': 'on_human_model_load',
       'E_ANIMATOR_LOADED': ('on_animator_load', 10),
       'E_AGONY': 'on_agony',
       'E_ADD_TEAMMATE_SFX': '_add_teammate_sfx',
       'E_DESTROY_TEAMMATE_SFX': '_destroy_teammate_sfx',
       'E_CLOSE_TEAMMATE_SFX': '_close_teammate_sfx',
       'E_OPEN_TEAMMATE_SFX': '_open_teammate_sfx',
       'E_ADD_TEAMMATE': '_on_add_teammate',
       'E_DELETE_TEAMMATE': 'on_delete_teammate',
       'E_UPDATE_TEAMMATE_INFO': 'on_update_teammate_info',
       'G_CACHED_FORMER_TEAMMATE_SET': 'get_cached_former_teammate_set',
       'G_ALL_GROUPMATES_DEAD': '_get_all_groupmates_dead',
       'G_ALIVE_GROUPMATE_NUM': '_get_alive_groupmate_num',
       'G_HAS_HEALTHY_GROUPMATE': '_has_healthy_groupmate',
       'G_VOICE_BLOCK_MATE': '_get_voice_block_mate',
       'G_TEXT_BLOCK_MATE': '_get_text_block_mate',
       'E_VOICE_BLOCK_MATE': 'set_voice_block_mate',
       'E_TEXT_BLOCK_MATE': 'set_text_block_mate',
       'E_PARACHUTE_FOLLOW_INVITED': 'show_follow_invited_ui',
       'E_SHOW_PARACHUTE_INVITE_RESPOND': 'show_parachute_invite_respond',
       'E_ON_REQUEST_TRANSFER_LEADER': 'show_follow_assign_ui',
       'E_RESPOND_TRANSFER_LEADER': 'show_parachute_assign_respond',
       'E_SET_PARACHUTE_FOLLOW_TARGET': 'set_parachute_follow_target',
       'G_PARACHUTE_FOLLOW_TARGET': 'get_parachute_follow_target',
       'G_PARACHUTE_FOLLOW_TARGET_INDEX': 'get_parachute_follow_target_index',
       'G_HAS_PARACHUTE_FOLLOWER': 'has_parachute_follower',
       'G_PLAYER_ID': 'get_player_uid',
       'E_RESET_SFX_RENDER_STAGE': 'sfx_reset_render_stage',
       'E_DEATH': 'on_death',
       'G_CHAR_NAME': '_get_char_name',
       'G_HEAD_FRAME': '_get_head_frame',
       'G_HEAD_PHOTO': '_get_head_photo',
       'G_DRESSED_CLOTHING_ID': '_get_dressed_clothing_id',
       'G_TEAMMATE_INFOS': 'get_teammate_infos',
       'G_GET_LOBBY_MECHA_ID': 'get_lobby_mecha_id',
       'E_SEND_BATTLE_GROUP_MSG': '_send_battle_group_msg',
       'G_GROUP_COLOR': '_get_group_name_color',
       'G_CONNECT_STATE': '_get_connect_state',
       'E_CONNECT_STATE': '_sync_connect_state',
       'E_OBSERVE_TARGET_LOADED': 'check_observe_target_group_id',
       'G_BATTLE_FLAG': '_get_battle_flag',
       'G_GROUPMATES_ORDER': '_get_groupmates_order',
       'E_REFRESH_GROUP_ORDERS': '_refresh_group_orders',
       'G_TEAMMATE_MECHAS': '_get_teammate_mechas',
       'G_IS_GANG_UP': '_is_gang_up'
       }

    def __init__(self):
        super(ComGroup, self).__init__()
        self._groupmate_uids = []
        self._groupmate_timestamp = 0
        self._groupmate_ids = []
        self._groupmate_ids_set = set()
        self.cur_teammate_sfx_vis = False
        self._is_login_team_ccmini = False
        self._former_groupmate_ids_set = set()

    def init_from_dict(self, unit_obj, bdict):
        super(ComGroup, self).init_from_dict(unit_obj, bdict)
        self._gropumates_info = bdict.get('groupmates_info', {})
        self._gang_up = bdict.get('gang_up', False)
        self._member_order_dict = bdict.get('members_order_dict', {})
        self._group_id = bdict.get('group_id', 0)
        self._char_name = bdict.get('char_name', '')
        self._role_id = bdict.get('role_id', u'11')
        self._head_frame = bdict.get('head_frame', 0)
        self._head_photo = bdict.get('head_photo', 0)
        self._conn_state = bdict.get('conn_state', True)
        self._lobby_mecha_id = bdict.get('lobby_mecha_id', 101008001)
        self.sd.ref_parachute_follow_target = bdict.get('follow_groupmate_id', None)
        self._uid = bdict.get('uid', None)
        self._observe_group_id = None
        self._battle_flag = bdict.get('battle_flag', {})
        self._voice_blocked_mates_ids = set(bdict.get('voice_blocked_mates_ids', set()))
        self._text_blocked_mates_ids = set(bdict.get('text_blocked_mates_ids', set()))
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        self._dressed_clothing_id = bdict.get('fashion', {}).get(FASHION_POS_SUIT)
        if self.is_unit_obj_type('LAvatar') and global_data.player.is_in_global_spectate():
            self._gropumates_info = bdict.get('watch_group_info', {})
            self._observe_group_id = bdict.get('watch_group_id', 0)
        for groupmate_id, groupmate_info in six.iteritems(self._gropumates_info):
            self._groupmate_ids.append(groupmate_id)
            self._groupmate_ids_set.add(groupmate_id)
            self._groupmate_uids.append(groupmate_info['uid'])
            if 'group_cc_eid' in groupmate_info:
                global_data.ccmini_mgr.set_eid_map(groupmate_info['group_cc_eid'], groupmate_info['uid'], session_id=const.TEAM_ALL_SESSION_ID)

        if self.unit_obj.id not in self._groupmate_ids:
            self._groupmate_ids.append(self.unit_obj.id)
            self._groupmate_ids_set.add(self.unit_obj.id)
            self._groupmate_uids.append(self.unit_obj.get_owner().uid)
        self._groupmate_ids.sort()
        self._teammate_sfx = None
        if self.sd.ref_is_avatar:
            if G_POS_CHANGE_MGR:
                self.regist_pos_change(self.on_move, 0.2)
            else:
                self.regist_event('E_POSITION', self.on_move)
            global_data.game_mgr.next_exec(self._notify_groupmates)
        self._groupmate_timestamp = time()
        if len(self._groupmate_ids) > 1:
            self.login_team_ccmini()
        return

    def _set_group_id(self, group_id):
        self.check_send_player_recruit_message()
        self._group_id = group_id
        if self._is_login_team_ccmini:
            global_data.ccmini_mgr.logout_session(const.TEAM_ALL_SESSION_ID)
            self._is_login_team_ccmini = False
        self.check_team_ccmini()

    def check_send_player_recruit_message(self):
        if not self.unit_obj or not self.unit_obj.is_valid():
            return
        if not self.unit_obj.get_owner() or not global_data.cam_lplayer:
            return
        if self.unit_obj.get_owner().id == global_data.cam_lplayer.id:
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_RECRUITMENT, RECRUITMENT_BATTLE_ACCEPT
            from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
            if global_data.battle and get_play_type_by_battle_id(global_data.battle.get_battle_tid()) == PLAY_TYPE_RECRUITMENT and global_data.cam_lplayer:
                global_data.battle.send_player_recruit_message(global_data.cam_lplayer.id, RECRUITMENT_BATTLE_ACCEPT)

    def check_team_ccmini(self):
        if len(self._groupmate_ids) > 1:
            self.login_team_ccmini()

    def _get_groupmate_timestamp(self):
        return self._groupmate_timestamp

    def _get_voice_block_mate(self):
        return self._voice_blocked_mates_ids

    def _get_text_block_mate(self):
        return self._text_blocked_mates_ids

    def set_text_block_mate(self, teammate_id, state):
        if state == True:
            self._text_blocked_mates_ids.add(teammate_id)
        else:
            self._text_blocked_mates_ids.discard(teammate_id)

    def set_voice_block_mate(self, teammate_id, state):
        if state == True:
            self._voice_blocked_mates_ids.add(teammate_id)
        else:
            self._voice_blocked_mates_ids.discard(teammate_id)

    def _on_add_teammate(self, teammate_id, info):
        if teammate_id not in self._groupmate_ids_set:
            self._groupmate_ids.append(teammate_id)
            self._groupmate_ids_set.add(teammate_id)
            self._groupmate_uids.append(info['uid'])
            self._gropumates_info[teammate_id] = info
            self._groupmate_ids.sort()
        self._groupmate_timestamp = time()
        global_data.emgr.scene_on_teammate_change.emit(self.unit_obj.id)
        self.login_team_ccmini()
        if 'group_cc_eid' in info:
            global_data.ccmini_mgr.set_eid_map(info['group_cc_eid'], info['uid'], const.TEAM_ALL_SESSION_ID)
        if global_data.player and self.unit_obj.id == global_data.player.id:
            global_data.ccmini_mgr.set_entityid_map(info['uid'], teammate_id)
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            _teammate = EntityManager.getentity(teammate_id)
            if _teammate and _teammate.logic:
                _teammate.logic.send_event('E_REFRESH_CAMP_SIDE_SHOW')
                control_target = _teammate.logic.ev_g_control_target()
                if control_target and control_target.logic and control_target != _teammate:
                    control_target.logic.send_event('E_REFRESH_CAMP_SIDE_SHOW')

    def on_delete_teammate(self, teammate_id):
        self._former_groupmate_ids_set.add(teammate_id)
        if teammate_id in self._groupmate_ids:
            self._groupmate_ids.remove(teammate_id)
        if teammate_id in self._groupmate_ids_set:
            self._groupmate_ids_set.remove(teammate_id)
        teammate_info = self._gropumates_info.pop(teammate_id, None)
        if teammate_info:
            self._groupmate_uids.remove(teammate_info['uid'])
        self._groupmate_timestamp = time()
        global_data.emgr.scene_on_teammate_change.emit(self.unit_obj.id)
        return

    def _get_groupmates_order(self):
        return self._member_order_dict

    def get_cached_former_teammate_set(self):
        return [ t_id for t_id in self._former_groupmate_ids_set if t_id not in self._groupmate_ids_set ]

    def _get_all_groupmates_dead(self):
        for info in six.itervalues(self._gropumates_info):
            if not info.get('dead', False):
                return False

        return True

    def _get_alive_groupmate_num(self):
        n = 0
        for info in six.itervalues(self._gropumates_info):
            if not info.get('dead', False):
                n += 1

        return n

    def _has_healthy_groupmate(self):
        for mate_id in self._gropumates_info:
            mate = EntityManager.getentity(mate_id)
            if mate and mate.logic.ev_g_healthy():
                return True

        return False

    def login_team_ccmini(self):
        if not self._is_login_team_ccmini and self.unit_obj == global_data.player.logic:
            if global_data.player and global_data.player.get_team_size() > 0:
                team_voice = global_data.message_data.get_seting_inf('ccmini_battle_speaker') or CLOSE_CHANNEL
            else:
                team_voice = global_data.message_data.get_seting_inf('ccmini_battle_group_speaker') or CLOSE_CHANNEL
            if team_voice == GROUP_CHANNEL:
                global_data.player.req_group_login_session_data()
            global_data.ccmini_mgr.create_speaking_list_timer()
            self._is_login_team_ccmini = True

    def _notify_groupmates(self):
        for eid in self._groupmate_ids:
            unit = EntityManager.getentity(eid)
            if not unit or not unit.logic:
                continue
            unit.logic.send_event('E_MARK_GROUPMATE')

    def _unbind_events(self):
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.on_move)
        else:
            self.unregist_event('E_POSITION', self.on_move)

    def on_human_model_load(self, model, *arg):
        global_data.emgr.add_teammate_name_event.emit(self.unit_obj, self._char_name)
        global_data.emgr.on_player_inited_event.emit(self.unit_obj)

    def on_animator_load(self, *args):
        global_data.emgr.on_player_animator_inited_event.emit(self.unit_obj)

    def on_agony(self):
        self.set_team_sfx_vis(False)

    def on_init_complete(self):
        global_data.emgr.add_teammate_blood_event.emit(self.unit_obj)

    def _set_ctrl_target(self, target, ctrl_conf=None):
        pass

    def on_move(self, pos):
        pass

    def _is_groupmate(self, entity_id, include_self=True):
        if not include_self:
            if global_data.cam_lplayer:
                if entity_id == global_data.cam_lplayer.id:
                    return False
                entity = EntityManager.getentity(entity_id)
                if entity and entity.logic.sd.ref_driver_id == global_data.cam_lplayer.id:
                    return False
        if entity_id in self._groupmate_ids_set:
            return True
        entity = EntityManager.getentity(entity_id)
        if not entity or not entity.logic:
            return False
        return entity.logic.sd.ref_driver_id in self._groupmate_ids_set

    def _groupmates(self):
        return list(self._groupmate_ids)

    def _get_groupmate_uids(self):
        return self._groupmate_uids

    def _add_teammate_sfx(self):
        return
        import math3d
        teammate_sfx_path = 'effect\\fx\\scenes\\common\\part\\quan.sfx'
        model_sfx_path = 'character/b_m_2001/b_m_2001_lod_t.gim'
        if self._teammate_sfx:
            return
        else:
            import world
            self._teammate_sfx = world.model(model_sfx_path, world.get_active_scene())
            self._teammate_sfx_loaded_callback(None, self._teammate_sfx)
            return

    def _teammate_sfx_loaded_callback(self, task_id, sfx):
        import world
        model = self.ev_g_model()
        if model:
            sfx.remove_from_parent()
            sfx.set_parent(model)
            sfx.all_materials.enable_copy()
            tuple_color = self._get_sfx_material_color(self.unit_obj.id)
            sfx.all_materials.set_var(_HASH_xray_color, 'xray_color', tuple_color)
            sfx.all_materials.rebuild_tech()
            sfx.world_transformation = model.world_transformation
            sfx.follow_same_bone_model(model)
            self._teammate_sfx = sfx
            self.sfx_reset_render_stage()
            sfx.inherit_flag &= ~world.INHERIT_VISIBLE
            self._open_teammate_sfx()

    def sfx_reset_render_stage(self):
        from logic.gcommon.common_const.scene_const import PENETRATE_RENDER_STAGE
        if self._teammate_sfx:
            self._teammate_sfx.set_render_stage(PENETRATE_RENDER_STAGE)
            self._teammate_sfx.render_level = -7
            self._teammate_sfx.lod_config = (500, 500)
            self.set_team_sfx_vis(self.cur_teammate_sfx_vis)

    def destroy(self):
        if self._is_login_team_ccmini:
            global_data.ccmini_mgr.logout_session(const.TEAM_ALL_SESSION_ID)
            self._is_login_team_ccmini = False
        self._destroy_teammate_sfx()
        global_data.emgr.del_follow_player_event.emit(self.unit_obj)
        self._unbind_events()
        self._member_order_dict = {}
        super(ComGroup, self).destroy()

    def _get_sfx_material_color(self, eid):
        from logic.gcommon.common_const.team_const import TUPLE_COLORS
        COLORS = tuple(TUPLE_COLORS)
        try:
            idx = self._groupmate_ids.index(eid)
            return COLORS[idx]
        except:
            return COLORS[0]

    def on_death(self, *args):
        self.set_team_sfx_vis(False)

    def set_team_sfx_vis(self, is_visit):
        self.cur_teammate_sfx_vis = is_visit
        if self._teammate_sfx and self._teammate_sfx.valid:
            self._teammate_sfx.visible = is_visit

    def show_follow_invited_ui(self, eid):
        if self.unit_obj.id == global_data.player.id:
            if not global_data.ui_mgr.get_ui('ParachuteInviteFollowUI'):
                ui = global_data.ui_mgr.show_ui('ParachuteInviteFollowUI', 'logic.comsys.battle')
                c_name = self._gropumates_info[eid].get('char_name', '???')
                ui.set_invite_follow_info(eid, self._groupmate_ids.index(eid), c_name)

    def show_parachute_invite_respond(self, groupmate_id, agree):
        if groupmate_id not in self._gropumates_info:
            return
        from logic.gcommon.common_utils.local_text import get_text_by_id
        c_name = self._gropumates_info[groupmate_id].get('char_name', '???')
        if agree:
            text = get_text_by_id(13044, {'playername': c_name})
        else:
            text = get_text_by_id(13043, {'playername': c_name})
        global_data.game_mgr.show_tip(text)

    def show_follow_assign_ui(self, eid):
        if self.unit_obj.id == global_data.player.id:
            if not global_data.ui_mgr.get_ui('ParachuteInviteFollowUI'):
                ui = global_data.ui_mgr.show_ui('ParachuteInviteFollowUI', 'logic.comsys.battle')
                c_name = self._gropumates_info[eid].get('char_name', '???')
                ui.set_invite_follow_info(eid, self._groupmate_ids.index(eid), c_name, is_assign=True)

    def show_parachute_assign_respond(self, groupmate_id, agree):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        c_name = self._gropumates_info[groupmate_id].get('char_name', '???')
        if agree:
            text = get_text_by_id(19786, {'playername': c_name})
        else:
            text = get_text_by_id(19785, {'playername': c_name})
        global_data.game_mgr.show_tip(text)

    def set_parachute_follow_target(self, eid):
        if self.sd.ref_is_avatar:
            if global_data.ui_mgr.get_ui('ParachuteInviteFollowUI'):
                global_data.ui_mgr.close_ui('ParachuteInviteFollowUI')
            if eid is not None:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                name = self._gropumates_info[eid].get('char_name', '???')
                global_data.game_mgr.show_tip(get_text_by_id(13100, {'playername': name}))
        self.sd.ref_parachute_follow_target = eid
        return

    def get_parachute_follow_target(self, get_name=False):
        if get_name:
            return (self.sd.ref_parachute_follow_target, self._gropumates_info.get(self.sd.ref_parachute_follow_target, {}).get('char_name', '???'))
        return self.sd.ref_parachute_follow_target

    def get_parachute_follow_target_index(self):
        if self.sd.ref_parachute_follow_target:
            return self._groupmate_ids.index(self.sd.ref_parachute_follow_target)
        else:
            return None

    def has_parachute_follower(self):
        if self.sd.ref_parachute_follow_target:
            return False
        for eid in self._groupmate_ids:
            if eid == self.unit_obj.id:
                continue
            ent = self.battle.get_entity(eid)
            if ent and ent.logic and ent.logic.is_valid():
                lent = ent.logic
                follower = lent.ev_g_parachute_follow_target()
                if follower == self.unit_obj.id:
                    return True

        return False

    def get_player_uid(self):
        return self.unit_obj.id

    def _get_char_name(self):
        return self._char_name

    def _get_role_id(self):
        return self._role_id

    def _get_head_frame(self):
        return self._head_frame

    def _get_head_photo(self):
        return self._head_photo

    def _get_dressed_clothing_id(self):
        return self._dressed_clothing_id

    def _get_battle_flag(self):
        battle_flag = self._battle_flag
        mecha_id = self.ev_g_ctrl_mecha()
        if mecha_id and not self.ev_g_in_mecha('MechaTrans'):
            battle_flag = copy.deepcopy(self._battle_flag)
            mecha = EntityManager.getentity(mecha_id)
            if mecha and mecha.logic:
                mecha_fashion_id = mecha.logic.ev_g_mecha_fashion_id()
                battle_mecha_id = mecha.logic.share_data.ref_mecha_id
                mecha_fashion_id = dress_utils.get_mecha_skin_item_no(battle_mecha_id, mecha_fashion_id)
                battle_flag['skin'] = mecha_fashion_id
        return battle_flag

    def _close_teammate_sfx(self):
        self.set_team_sfx_vis(False)

    def _open_teammate_sfx(self):
        self.set_team_sfx_vis(True)
        model = self.ev_g_model()
        self.sfx_reset_render_stage()

    def get_teammate_infos(self):
        return dict(self._gropumates_info)

    def get_lobby_mecha_id(self):
        return self._lobby_mecha_id

    def _send_battle_group_msg(self, msg, is_system=False):
        self.send_event('E_CALL_SYNC_METHOD', 'battle_group_msg', (msg, is_system), True)
        unit_id = self.unit_obj.id
        unit_name = self.ev_g_char_name()
        dmsg = msg.copy()
        dmsg['unit_id'] = unit_id
        global_data.emgr.add_battle_group_msg_event.emit(unit_id, unit_name, {'msg': dmsg})
        self.send_event('E_ADD_GROUP_HISTORY_MSG', unit_id, unit_name, msg)

    def _get_group_name_color(self, unit_id):
        return battle_utils.get_group_color(self._groupmate_ids, unit_id)

    def _get_group_id(self, exclude_observe=False):
        if exclude_observe:
            return self._group_id
        else:
            if self._observe_group_id is not None:
                return self._observe_group_id
            return self._group_id
            return

    def check_observe_target_group_id(self):
        if not self.ev_g_is_in_spectate():
            print('not in spectate')
            return
        spectate_target = self.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self._observe_group_id = spectate_target.logic.ev_g_group_id()
        else:
            log_error('unable to get observe target player group_id!!!!')

    def _destroy_teammate_sfx(self):
        if self._teammate_sfx and self._teammate_sfx.valid:
            self._teammate_sfx.destroy()
        self._teammate_sfx = None
        return

    def _get_connect_state(self):
        return self._conn_state

    def _sync_connect_state(self, conn_state):
        self._conn_state = conn_state

    def on_update_teammate_info(self, member_id, info):
        if member_id in self._gropumates_info:
            self._gropumates_info[member_id].update(info)
            if 'group_cc_eid' in info:
                uid = self._gropumates_info[member_id]['uid']
                global_data.ccmini_mgr.set_eid_map(info['group_cc_eid'], uid, const.TEAM_ALL_SESSION_ID)

    def _get_teammate_mechas(self):
        return [ data['created_mecha_type'] for data in six.itervalues(self._gropumates_info) if 'created_mecha_type' in data ]

    def _refresh_group_orders(self, member_order_dict, member_id):
        lst_member_order_dict = self._member_order_dict
        self._member_order_dict = member_order_dict
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_RECRUITMENT
        from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
        if global_data.battle and get_play_type_by_battle_id(global_data.battle.get_battle_tid()) == PLAY_TYPE_RECRUITMENT:
            global_data.emgr.scene_on_teammate_change.emit(self.unit_obj.id)
            player_name = self._gropumates_info.get(member_id, {}).get('char_name', '')
            global_data.battle.show_accept_and_leave_message(lst_member_order_dict, member_order_dict, member_id, player_name=player_name)

    def _is_gang_up(self):
        return self._gang_up