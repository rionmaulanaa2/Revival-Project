# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FactionDanmuController.py
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.team_utils import get_teammate_num
MSG_FORMAT = [
 '#DB{0}.\xe3\x80\x90{1}\xe3\x80\x91#n\xef\xbc\x9a{2}',
 '#SG{0}.\xe3\x80\x90{1}\xe3\x80\x91#n\xef\xbc\x9a{2}',
 '#PY{0}.\xe3\x80\x90{1}\xe3\x80\x91#n\xef\xbc\x9a{2}',
 '#SP{0}.\xe3\x80\x90{1}\xe3\x80\x91#n\xef\xbc\x9a{2}']

class FactionDanmuController(object):

    def __init__(self):
        self.process_event(True)

    def destroy(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'add_battle_group_msg_event': self.on_add_battle_group_msg_event
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_add_battle_group_msg_event(self, unit_id, char_name, data):
        is_role_voice = data.get('is_role_voice_msg', False)
        if is_role_voice:
            return
        else:
            role_id = data.get('role_id', None)
            if role_id:
                dmsg = data.get('msg', {'role_id': role_id})
            else:
                dmsg = data.get('msg', {})
            dmsg['unit_id'] = unit_id
            if 'text' not in dmsg:
                return
            from logic.gutils import chat_utils
            chat_utils.format_msg_data(dmsg)
            head_pic = self.get_danmu_head_pic(unit_id, role_id, dmsg.get('head_photo'))
            team_idx = self.get_team_idx(unit_id)
            team_idx = team_idx % len(MSG_FORMAT)
            msg = MSG_FORMAT[team_idx].format(team_idx, char_name, dmsg['text'])
            global_data.emgr.on_recv_danmu_msg.emit(msg, 1, head_pic)
            return

    def get_danmu_head_pic(self, eid, role_id, head_photo):
        from logic.gutils import role_head_utils
        if head_photo:
            return role_head_utils.get_head_res_path_by_abs_id(head_photo)
        player = global_data.player
        is_my = eid == player.id if player else False
        danmu_show_default_head = player.get_setting(uoc.DANMU_SHOW_DEFAULT_HEAD) if player else True
        if is_my and not danmu_show_default_head:
            if player:
                abs_id = player.get_head_photo() if 1 else 30200011
                return role_head_utils.get_head_res_path_by_abs_id(abs_id)
            role_id = role_id or 11
        if str(role_id) == '111':
            abs_id = 30201111
        else:
            abs_id = 30200000 + role_id
        return role_head_utils.get_head_res_path_by_abs_id(abs_id)

    def get_team_idx(self, unit_id):
        battle = global_data.battle
        if not battle:
            return 0
        else:
            lplayer = global_data.cam_lplayer
            if not lplayer:
                return 0
            my_faction = lplayer.ev_g_camp_id()
            if not my_faction:
                return 0
            players_pos_info = battle.get_custom_faction_members(my_faction)
            if not players_pos_info:
                return 0
            new_faction_players = set(players_pos_info.keys())
            faction_player_nos = get_teammate_num(list(new_faction_players))
            if unit_id in new_faction_players:
                return faction_player_nos[unit_id]
            return 0