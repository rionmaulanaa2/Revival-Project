# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleReportParser.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const import battle_const as bconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import game_mode_const
from logic.gcommon.common_const import ui_operation_const as uoc
import pickle

class BattleReportParser(object):

    def parse_battle_report(self, report_dict):
        player = global_data.cam_lplayer
        from logic.gcommon import const
        from common.cfg import confmgr
        headshot_pic = 'gui/ui_res_2/battle/notice/icon_critl.png'
        event_type = report_dict['event_type']
        injured_name = report_dict.get('injured_name')
        injured_id = report_dict.get('injured_id')
        killer_name, killer_id, killer_weap_id, bleed_damage_type, killer_damage_type, trigger_parts, mecha_id, damage_type, trigger_other_info = self._parse_report_data(report_dict)
        if type(killer_name) not in [str, six.text_type]:
            log_error('malformat battle report ', report_dict)
        trigger_part_str = ''
        is_in_killer_team = False
        is_self_kill = False
        is_in_injured_team = False
        if player:
            if killer_id:
                is_in_killer_team = player.ev_g_is_groupmate(killer_id)
                is_self_kill = player.id == killer_id
            if injured_id:
                is_in_injured_team = player.ev_g_is_groupmate(injured_id)
        teammate_kill_color = '#DB'
        self_kill_color = '#SG'
        enemy_color = '#SR'
        color = '#SW'
        if is_self_kill:
            color = self_kill_color
        elif is_in_killer_team:
            color = teammate_kill_color
        elif is_in_injured_team:
            color = enemy_color
        has_killer = killer_id != None
        mecha_pic_str = ''
        if trigger_parts and const.HIT_PART_HEAD in trigger_parts:
            trigger_part_str = self._get_richtext_pic(headshot_pic, 1.0)
        scale = confmgr.get('death_notice_detail', str(damage_type), default={}).get('iNoticeScale', 1.0)
        if event_type == bconst.FIGHT_EVENT_KILL_GROUP:
            event_type = bconst.FIGHT_EVENT_DEATH
        if mecha_id is None:
            damage_pic = self.get_damage_type_pic(damage_type, killer_weap_id)
            if damage_type in [bconst.FIGHT_INJ_SHOOT, bconst.FIGHT_INJ_BOMB, bconst.FIGHT_INJ_MELEE]:
                msg_key = '%d_%d' % (event_type, damage_type)
                damage_pic_str = self._get_richtext_pic(damage_pic, scale)
            elif damage_type == bconst.FIGHT_INJ_BLEED:
                msg_key = '%d_%d' % (event_type, bleed_damage_type)
                damage_pic = self.get_damage_type_pic(bleed_damage_type, killer_weap_id)
                scale = confmgr.get('death_notice_detail', str(bleed_damage_type), default={}).get('iNoticeScale', 1.0)
                damage_pic_str = self._get_richtext_pic(damage_pic, scale)
            elif damage_type in [bconst.FIGHT_INJ_POISON, bconst.FIGHT_INJ_SIGNAL]:
                msg_key = '%d_%d' % (event_type, killer_damage_type)
                damage_pic = self.get_damage_type_pic(killer_damage_type, killer_weap_id)
                scale = confmgr.get('death_notice_detail', str(killer_damage_type), default={}).get('iNoticeScale', 1.0)
                damage_pic_str = self._get_richtext_pic(damage_pic, scale)
            else:
                msg_key = '%d_%d' % (event_type, damage_type)
                damage_pic_str = self._get_richtext_pic(damage_pic, scale)
        elif damage_type == bconst.FIGHT_INJ_THUNDER:
            damage_pic = self.get_damage_type_pic(damage_type, killer_weap_id)
            damage_pic_str = ''
            mecha_pic_str = self._get_richtext_pic(damage_pic, scale)
            msg_key = '%d_%d' % (event_type, bconst.FIGHT_INJ_MECHA_RELATED)
        else:
            damage_pic_str = ''
            msg_key = '%d_%d' % (event_type, bconst.FIGHT_INJ_MECHA_RELATED)
            from logic.gutils.item_utils import get_mecha_type_pic
            mecha_pic_str = self._get_richtext_pic(get_mecha_type_pic(mecha_id), scale)
        dead_notice_content = confmgr.get('death_notice', msg_key, default={})
        if has_killer:
            raw_msg = self.get_text_with_checking(dead_notice_content.get('cOwnStruct'))
        else:
            raw_msg = self.get_text_with_checking(dead_notice_content.get('cNoOwnStruct'))
        if not raw_msg:
            log_error('unsupport dead notice ', msg_key)
        verb_str = ''
        if event_type == bconst.FIGHT_EVENT_BLEED:
            verb_str = self._get_richtext_pic('gui/ui_res_2/battle/notice/icon_fall_down.png', 1.0)
        elif event_type == bconst.FIGHT_EVENT_MECHA_DEATH:
            verb_str = self._get_richtext_pic('gui/ui_res_2/battle/notice/icon_destroy_mecha.png', 1.0)
        if killer_name is not None and isinstance(killer_name, str):
            killer_name = killer_name + ' '
        all_msg = raw_msg.format(**{'killer': self._get_richtext_name(killer_name, color),
           'verb': verb_str,
           'injured': self._get_richtext_name(injured_name, color),
           'damage_type_pic': damage_pic_str,
           'mecha_type_pic': mecha_pic_str,
           'critic': trigger_part_str
           })
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_KING):
            if is_self_kill:
                color = self_kill_color
            else:
                _, death_trigger_dict = report_dict.get('death_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
                trigger_faction = death_trigger_dict.get('trigger_faction', None)
                side = global_data.king_battle_data.get_side_by_faction_id(trigger_faction)
                if side == game_mode_const.MY_SIDE:
                    color = '#SB'
                elif side == game_mode_const.E_TWO_SIDE:
                    color = '#SO'
                elif side == game_mode_const.E_ONE_SIDE:
                    color = '#SR'
        return (
         all_msg, color, trigger_other_info)

    def _parse_report_data(self, report_dict):
        event_type = report_dict['event_type']
        bleed_damage_type = bconst.FIGHT_INJ_UNKNOWN

        def get_source_info(damage_type, dict):
            name = unpack_text(dict.get('trigger_name'))
            _id = dict.get('trigger_id')
            _weap_id = dict.get('item_id')
            trigger_parts = dict.get('trigger_parts')
            mecha_id = dict.get('mecha_id')
            tigger_other_info = {}
            if 'skin_id' in dict:
                tigger_other_info['skin_id'] = dict.get('skin_id')
                enable_ss_str = dict.get('enable_ss_skin_broadcast')
                if enable_ss_str is not None:
                    enable_ss_str = six.ensure_binary(enable_ss_str)
                    enable_ss = pickle.loads(enable_ss_str)
                else:
                    enable_ss = enable_ss_str
                tigger_other_info['enable_ss_skin_broadcast'] = enable_ss
                if tigger_other_info['enable_ss_skin_broadcast'] is None:
                    tigger_other_info['enable_ss_skin_broadcast'] = uoc.SETTING_CONF.get(uoc.SS_SKIN_BATTLE_MSG_SHOW)
            return (
             name, _id, _weap_id, damage_type, trigger_parts, mecha_id, tigger_other_info)

        if event_type == bconst.FIGHT_EVENT_BLEED:
            damage_type, trigger_dict = report_dict.get('bleed_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            killer_name = unpack_text(trigger_dict.get('trigger_name'))
            killer_id = trigger_dict.get('trigger_id')
            trigger_parts = trigger_dict.get('trigger_parts')
            killer_weap_id = trigger_dict.get('item_id')
            mecha_id = trigger_dict.get('mecha_id')
            tigger_other_info = {}
            if 'skin_id' in trigger_dict:
                tigger_other_info['skin_id'] = trigger_dict.get('skin_id')
                enable_ss_str = trigger_dict.get('enable_ss_skin_broadcast')
                if enable_ss_str is not None:
                    enable_ss_str = six.ensure_binary(enable_ss_str)
                    enable_ss = pickle.loads(enable_ss_str)
                else:
                    enable_ss = enable_ss_str
                tigger_other_info['enable_ss_skin_broadcast'] = enable_ss
                if tigger_other_info['enable_ss_skin_broadcast'] is None:
                    tigger_other_info['enable_ss_skin_broadcast'] = uoc.SETTING_CONF.get(uoc.SS_SKIN_BATTLE_MSG_SHOW)
            killer_damage_type = damage_type
            if global_data.cam_lplayer:
                if killer_id and killer_id == global_data.cam_lplayer.id:
                    global_data.emgr.play_game_voice.emit('down')
                else:
                    injured_id = report_dict.get('injured_id')
                    if injured_id and injured_id == global_data.cam_lplayer.id:
                        global_data.emgr.play_game_voice.emit('ground')
        else:
            bleed_damage_type, bleed_trigger_dict = report_dict.get('bleed_source') or (
             bconst.FIGHT_INJ_UNKNOWN, {})
            damage_type, death_trigger_dict = report_dict.get('death_source') or (
             bconst.FIGHT_INJ_UNKNOWN, {})
            if not self.check_is_system_kill(damage_type):
                killer_name, killer_id, killer_weap_id, killer_damage_type, trigger_parts, mecha_id, tigger_other_info = get_source_info(damage_type, death_trigger_dict)
            elif self.check_is_system_kill(damage_type):
                if bleed_damage_type:
                    if self.check_is_system_kill(bleed_damage_type):
                        killer_name, killer_id, killer_weap_id, killer_damage_type, trigger_parts, mecha_id, tigger_other_info = get_source_info(damage_type, death_trigger_dict)
                    else:
                        killer_name, killer_id, killer_weap_id, killer_damage_type, trigger_parts, mecha_id, tigger_other_info = get_source_info(bleed_damage_type, bleed_trigger_dict)
                else:
                    killer_name, killer_id, killer_weap_id, killer_damage_type, trigger_parts, mecha_id, tigger_other_info = get_source_info(damage_type, death_trigger_dict)
            else:
                killer_name, killer_id, killer_weap_id, killer_damage_type, trigger_parts, mecha_id, tigger_other_info = get_source_info(bleed_damage_type, bleed_trigger_dict)
        return (
         killer_name, killer_id, killer_weap_id, bleed_damage_type, killer_damage_type, trigger_parts,
         mecha_id, damage_type, tigger_other_info)

    def get_damage_type_pic(self, damage_type, weap_id=None):
        from logic.gcommon.common_const import battle_const as bconst
        from logic.gutils.item_utils import get_gun_kill_pic_by_item_id
        from common.cfg import confmgr
        res_path = 'gui/ui_res_2/battle/notice/'
        if damage_type in [bconst.FIGHT_INJ_SHOOT, bconst.FIGHT_INJ_BOMB]:
            if damage_type == bconst.FIGHT_TYPE_SHOOT:
                weap_fiream_res_conf = confmgr.get('firearm_res_config', str(weap_id), default={})
                notice_icon = weap_fiream_res_conf.get('cNoticeIcon', '')
                if notice_icon:
                    pic = res_path + notice_icon
                else:
                    pic = get_gun_kill_pic_by_item_id(weap_id)
            else:
                pic = get_gun_kill_pic_by_item_id(weap_id)
        else:
            pic_name = confmgr.get('death_notice_detail', str(damage_type), default={}).get('cNoticeIcon', '')
            if pic_name:
                pic = res_path + pic_name
            else:
                pic = ''
        return pic

    def _get_richtext_name(self, name_str, color_str='#SW'):
        return '%(name)s' % {'name': name_str}

    def _get_richtext_pic(self, pic_path, pic_scale=1.0):
        return '<img="%s", scale=%0.1f>' % (pic_path, pic_scale)

    def check_is_system_kill(self, damage_type):
        from logic.gcommon.common_const import battle_const as bconst
        if damage_type in [bconst.FIGHT_INJ_POISON, bconst.FIGHT_INJ_FALLING, bconst.FIGHT_INJ_BLEED]:
            return True
        else:
            return False

    def get_text_with_checking(self, raw_msg_id):
        if raw_msg_id:
            return get_text_by_id(int(raw_msg_id))
        else:
            return ''