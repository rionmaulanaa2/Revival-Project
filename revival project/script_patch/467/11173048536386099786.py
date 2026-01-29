# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/MiddleBattleReportParser.py
from __future__ import absolute_import
from logic.gcommon.common_const import battle_const as bconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.ctypes.FightData import is_system_maker
from logic.gutils import judge_utils

class MiddleBattleReportParser(object):

    def __init__(self):
        self._is_judge_ob = judge_utils.is_ob()

    def parse_self_dead_battle_report(self, report_dict, player_id, cur_survive_num):
        if not global_data.cam_lplayer:
            return (None, None, None, None, None, None)
        else:
            from logic.gcommon import const
            event_type = report_dict['event_type']
            if event_type == bconst.FIGHT_EVENT_KILL_GROUP:
                is_defeated_valid = report_dict.get('is_defeated_valid', True)
                if is_defeated_valid:
                    event_type = bconst.FIGHT_EVENT_DEFEAT if 1 else bconst.FIGHT_EVENT_DEATH
                injured_name = report_dict.get('injured_name')
                injured_id = report_dict.get('injured_id')
                killer_assisters_server = report_dict.get('killer_assisters', [])
                _, death_trigger_dict = report_dict.get('death_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
                if death_trigger_dict:
                    is_sys_maker = is_system_maker(death_trigger_dict.get('maker_type', None))
                else:
                    _, bleed_dict = report_dict.get('bleed_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
                    is_sys_maker = is_system_maker(bleed_dict.get('maker_type', None))
                killer_id, killer_name, killer_damage_type, killer_weap_id, killer_mecha_id, assist_id, assist_name, assist_damage_type, assist_weap_id, assist_mecha_id = self.parse_dead_battle_report_data(report_dict)
                from common.cfg import confmgr
                remain_str = ''
                raw_msg = ''
                has_killer = killer_id is not None
                is_killer = global_data.cam_lplayer.ev_g_is_groupmate(killer_id)
                is_injured = injured_id == player_id
                is_killer_teammate = is_killer and killer_id != player_id
                is_injured_teammate = global_data.cam_lplayer.ev_g_is_groupmate(injured_id)
                is_assist = assist_id == player_id and assist_id != killer_id and assist_id != injured_id
                is_assist_server = global_data.cam_lplayer.id in killer_assisters_server
                weapon = ''
                dead_notice_content = {}
                if not (is_killer or is_injured or is_assist or is_injured_teammate):
                    return (None, None, None, None, None, None)
                if is_injured and is_killer:
                    msg_key = '%d_%d' % (event_type, killer_damage_type)
                    dead_notice_content = confmgr.get('death_notice', msg_key, default={})
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfHarmStruct'))
                    killer_name = self.get_show_name(killer_name, is_killer_teammate)
                elif is_killer and not is_assist_server:
                    killer_name = self.get_show_name(killer_name, is_killer_teammate)
                    if assist_id is not None and assist_id != killer_id:
                        msg_key = '%d_%d' % (event_type, killer_damage_type)
                        dead_notice_content = confmgr.get('death_notice', msg_key, default={})
                        raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfIndirectKillStruct'))
                    else:
                        if killer_mecha_id:
                            killer_damage_type = bconst.FIGHT_INJ_MECHA_RELATED
                        msg_key = '%d_%d' % (event_type, killer_damage_type)
                        dead_notice_content = confmgr.get('death_notice', msg_key, default={})
                        raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDirectKillStruct'))
                elif is_injured:
                    if not self._is_judge_ob:
                        injured_name = get_text_by_id(18535)
                    msg_key = '%d_%d' % (event_type, killer_damage_type)
                    dead_notice_content = confmgr.get('death_notice', msg_key, default={})
                    if has_killer:
                        raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDirectKillStruct'))
                    else:
                        raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDeadNoOwnerStruct'))
                elif is_injured_teammate:
                    msg_key = '%d_%d' % (event_type, killer_damage_type)
                    dead_notice_content = confmgr.get('death_notice', msg_key, default={})
                    if has_killer:
                        if not is_sys_maker:
                            killer_name = ' '.join((get_text_by_id(18541), killer_name))
                        raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDirectKillStruct'))
                    else:
                        raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDeadNoOwnerStruct'))
                elif is_assist_server:
                    if assist_mecha_id:
                        assist_damage_type = bconst.FIGHT_INJ_MECHA_RELATED
                    msg_key = '%d_%d' % (event_type, killer_damage_type)
                    dead_notice_content = confmgr.get('death_notice', msg_key, default={})
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfAssistStruct'))
                from logic.gutils import item_utils
                if is_assist:
                    if assist_mecha_id:
                        weapon = self.get_mecha_name_by_id(assist_mecha_id)
                    else:
                        weapon = self.get_weapon_name_by_type(assist_damage_type)
                        if not weapon:
                            if assist_weap_id:
                                weapon = item_utils.get_item_name(str(assist_weap_id))
                    trigger_parts = death_trigger_dict.get('trigger_parts')
                    if assist_id == player_id:
                        assist_name = self._is_judge_ob or get_text_by_id(18535)
            else:
                if killer_mecha_id:
                    weapon = self.get_mecha_name_by_id(killer_mecha_id)
                else:
                    weapon = self.get_weapon_name_by_type(killer_damage_type)
                    if not weapon:
                        if killer_weap_id:
                            weapon = item_utils.get_item_name(str(killer_weap_id))
                trigger_parts = death_trigger_dict.get('trigger_parts')
            killer_teammate = get_text_by_id(18546) if is_killer_teammate else ''
            ope_str = self.get_text_with_checking(dead_notice_content.get('cOpeVerb'))
            remain_str = get_text_by_id(18537, (cur_survive_num - 1,))
            if is_killer:
                if injured_name:
                    injured_name = '#SB' + injured_name + '#n'
            elif killer_name:
                killer_name = '#SR' + killer_name + '#n'
            if not raw_msg or not dead_notice_content:
                log_error('unsupported self dead notice ', report_dict)
            msg = raw_msg.format(**{'killer': killer_name,'killer_teammate': killer_teammate,
               'ope_str': ope_str,
               'weapon': weapon,
               'assistor': assist_name,
               'verb': self.get_text_with_checking(dead_notice_content.get('cVerb')),
               'critic': get_text_by_id(18538) if trigger_parts and const.HIT_PART_HEAD in trigger_parts else '',
               'injured': injured_name,
               'survive': remain_str
               })
            is_critic = True if trigger_parts and const.HIT_PART_HEAD in trigger_parts else False
            return (
             msg, is_killer_teammate, is_killer, is_assist_server, is_critic, killer_id)

    def get_text_with_checking(self, raw_msg_id):
        if raw_msg_id:
            return get_text_by_id(int(raw_msg_id))
        else:
            return ''

    def parse_dead_battle_report_data(self, report_dict):
        injured_id = report_dict.get('injured_id')
        bleed_damage_type, bleed_trigger_dict = report_dict.get('bleed_source') or (
         bconst.FIGHT_INJ_UNKNOWN, {})
        death_damage_type, death_trigger_dict = report_dict.get('death_source') or (
         bconst.FIGHT_INJ_UNKNOWN, {})

        def get_source_info(dict):
            name = unpack_text(dict.get('trigger_name'))
            _id = dict.get('trigger_id')
            _weap_id = dict.get('item_id')
            mecha_id = dict.get('mecha_id')
            return (
             name, _id, _weap_id, mecha_id)

        if bleed_damage_type:
            killer_name, killer_id, killer_weap_id, killer_mecha_id = get_source_info(bleed_trigger_dict)
            _, assist_id, assist_weap_id, assist_mecha_id = get_source_info(death_trigger_dict)
            assist_damage_type = death_damage_type
            killer_damage_type = bleed_damage_type
            is_sys_maker = is_system_maker(bleed_trigger_dict.get('maker_type', None))
            if not killer_id or killer_id == injured_id or is_sys_maker:
                killer_name, killer_id, killer_weap_id, killer_mecha_id = get_source_info(death_trigger_dict)
                assist_id = None
                assist_weap_id = None
                assist_damage_type = None
                assist_mecha_id = None
                killer_damage_type = death_damage_type
        else:
            killer_name, killer_id, killer_weap_id, killer_mecha_id = get_source_info(death_trigger_dict)
            assist_id = None
            assist_weap_id = None
            assist_damage_type = None
            assist_mecha_id = None
            killer_damage_type = death_damage_type
        assist_name = unpack_text(death_trigger_dict.get('trigger_name'))
        return (
         killer_id, killer_name, killer_damage_type, killer_weap_id, killer_mecha_id,
         assist_id, assist_name, assist_damage_type, assist_weap_id, assist_mecha_id)

    def parse_self_bleed_battle_report(self, report_dict, player_id):
        if not player_id:
            return (None, None, None, None)
        else:
            if not global_data.cam_lplayer:
                return (None, None, None, None)
            from logic.gcommon.common_const import battle_const as bconst
            from logic.gcommon import const
            from common.cfg import confmgr
            event_type = report_dict['event_type']
            injured_name = report_dict.get('injured_name')
            injured_id = report_dict.get('injured_id')
            killer_assisters_server = report_dict.get('killer_assisters', [])
            damage_type, trigger_dict = report_dict.get('bleed_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            killer_name = unpack_text(trigger_dict.get('trigger_name'))
            is_sys_maker = is_system_maker(trigger_dict.get('maker_type', None))
            killer_id = trigger_dict.get('trigger_id')
            trigger_parts = trigger_dict.get('trigger_parts')
            killer_weap_id = trigger_dict.get('item_id')
            mecha_id = trigger_dict.get('mecha_id')
            if mecha_id:
                damage_type = bconst.FIGHT_INJ_MECHA_RELATED
            msg_key = '%d_%d' % (event_type, damage_type)
            dead_notice_content = confmgr.get('death_notice', msg_key, default={})
            if damage_type == bconst.FIGHT_INJ_FALLING and not killer_id:
                killer_id = player_id
            from common.cfg import confmgr
            raw_msg = ''
            weapon = ''
            has_killer = killer_id is not None
            is_killer = global_data.cam_lplayer.ev_g_is_groupmate(killer_id)
            is_injured = injured_id == player_id
            is_injured_teammate = global_data.cam_lplayer.ev_g_is_groupmate(injured_id)
            is_killer_teammate = is_killer and killer_id != player_id
            is_assist = global_data.cam_lplayer.id in killer_assisters_server
            if not (is_killer or is_injured or is_injured_teammate):
                return (None, None, None, None)
            if is_injured and is_killer:
                raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfHarmStruct'))
                killer_name = self.get_show_name(killer_name, is_killer_teammate)
                if not self._is_judge_ob:
                    injured_name = get_text_by_id(18535)
            elif is_killer:
                killer_name = self.get_show_name(killer_name, is_killer_teammate)
                if is_assist:
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfAssistStruct'))
                else:
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDirectKillStruct'))
            elif is_injured:
                if not self._is_judge_ob:
                    injured_name = get_text_by_id(18535)
                if has_killer:
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDirectKillStruct'))
                else:
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDeadNoOwnerStruct'))
            elif is_injured_teammate:
                if has_killer:
                    if not is_sys_maker:
                        killer_name = ' '.join((get_text_by_id(18541), killer_name))
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDirectKillStruct'))
                else:
                    raw_msg = self.get_text_with_checking(dead_notice_content.get('cSelfDeadNoOwnerStruct'))
            from logic.gutils import item_utils
            weapon = self.get_weapon_name_by_type(damage_type)
            if not weapon:
                if mecha_id:
                    weapon = self.get_mecha_name_by_id(mecha_id)
                elif killer_weap_id:
                    weapon = item_utils.get_item_name(str(killer_weap_id))
            if is_killer_teammate:
                killer_teammate = get_text_by_id(18546) if 1 else ''
                ope_str = self.get_text_with_checking(dead_notice_content.get('cOpeVerb'))
                raw_msg or log_error('unsupported self bleed notice ', msg_key)
            if is_killer:
                if injured_name:
                    injured_name = '#SB' + injured_name + '#n'
            elif killer_name:
                killer_name = '#SR' + killer_name + '#n'
            msg = raw_msg.format(**{'killer': killer_name,'killer_teammate': killer_teammate,
               'ope_str': ope_str,
               'weapon': weapon,
               'verb': self.get_text_with_checking(dead_notice_content.get('cVerb')),
               'critic': get_text_by_id(18538) if trigger_parts and const.HIT_PART_HEAD in trigger_parts else '',
               'injured': injured_name
               })
            is_teammate = is_killer_teammate
            return (
             msg, is_teammate, is_killer, is_assist)

    def get_weapon_name_by_type(self, damage_type):
        from common.cfg import confmgr
        weapon_id = confmgr.get('death_notice_detail', str(damage_type), default={}).get('cNoticeWeapon', '')
        if weapon_id:
            weapon = get_text_by_id(weapon_id)
        else:
            weapon = ''
        return weapon

    def get_mecha_name_by_id(self, mecha_id):
        from common.cfg import confmgr
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        mecha_name = get_text_by_id(mecha_conf.get(mecha_id, {}).get('name_text_id', 28001))
        return mecha_name

    def check_is_system_kill(self, damage_type):
        from logic.gcommon.common_const import battle_const as bconst
        if damage_type in [bconst.FIGHT_INJ_POISON, bconst.FIGHT_INJ_FALLING, bconst.FIGHT_INJ_BLEED]:
            return True
        else:
            return False

    def get_bleed_prefix(self):
        return get_text_by_id(18503)

    def get_dead_prefix(self, player_id):
        from logic.gcommon.common_utils.battle_utils import get_player_kill_num
        kill_person_num, kill_mecha_num = get_player_kill_num(player_id)
        return (
         kill_person_num, kill_mecha_num)

    def get_show_name(self, name, is_teammate):
        if self._is_judge_ob:
            return name
        if not is_teammate:
            return get_text_by_id(18535)
        return name

    def parse_mecha_dead_battle_report(self, report_dict, player_id):
        if not global_data.cam_lplayer or not global_data.cam_lctarget:
            return (None, None, None, None, None, None, None)
        else:
            from logic.gcommon.common_utils.battle_utils import parse_battle_report_mecha_death
            killer_id, injured_id = parse_battle_report_mecha_death(report_dict)
            killer_assisters_server = report_dict.get('killer_assisters', [])
            damage_type, death_trigger_dict = report_dict.get('death_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            killer_name = unpack_text(death_trigger_dict.get('trigger_name'))
            has_killer = killer_id is not None
            is_killer = global_data.cam_lplayer.ev_g_is_groupmate(killer_id)
            is_injured = global_data.cam_lplayer.ev_g_is_groupmate(injured_id)
            is_killer_teammate = is_killer and killer_id != player_id
            is_assist = global_data.cam_lplayer.id in killer_assisters_server
            killer_teammate = get_text_by_id(18546) if is_killer_teammate else ''
            is_mecha_being_kill = False
            if is_killer:
                mecha_id = report_dict.get('mecha_id')
                injured_mecha_name = get_text_by_id(self.get_injured_mecha_name(mecha_id))
                if injured_mecha_name:
                    injured_mecha_name = '#SB' + injured_mecha_name + '#n'
                killer_name = self.get_show_name(killer_name, is_killer_teammate)
                hint_text_id = 19780 if is_assist else 18539
                msg = get_text_by_id(hint_text_id).format(**{'killer_teammate': killer_teammate,
                   'killer': killer_name,
                   'mechaname': injured_mecha_name
                   })
            else:
                msg = None
                enemy_mecha_id = death_trigger_dict.get('mecha_id', None)
                if enemy_mecha_id and global_data.cam_lctarget.id == injured_id:
                    mecha_name = get_text_by_id(self.get_injured_mecha_name(enemy_mecha_id))
                    if mecha_name:
                        is_mecha_being_kill = True
                        mecha_name = '#SB' + mecha_name + '#n'
                        msg = get_text_by_id(18555).format(**{'mechaname': mecha_name
                           })
            from logic.gcommon import const
            trigger_parts = death_trigger_dict.get('trigger_parts')
            is_critic = True if trigger_parts and const.HIT_PART_HEAD in trigger_parts else False
            return (
             msg, is_killer_teammate, is_killer, is_critic, killer_id, is_assist, is_mecha_being_kill)

    def get_injured_mecha_name(self, mecha_id):
        from common.cfg import confmgr
        mecha_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        mecha_conf = mecha_conf.get(str(mecha_id), {})
        name_text_id = mecha_conf.get('name_text_id', None)
        if name_text_id is None:
            return ''
        else:
            if isinstance(name_text_id, list) and len(name_text_id) > 0:
                name_text_id = name_text_id[0]
            return name_text_id