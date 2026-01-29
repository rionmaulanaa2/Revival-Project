# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KingBattleData.py
from __future__ import absolute_import
import six
from six.moves import range
from common.framework import Singleton
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.client.const import game_mode_const
import cc
E_SIDES = [
 game_mode_const.E_ONE_SIDE, game_mode_const.E_TWO_SIDE]

class CCampData(object):

    def __init__(self, camp_id):
        self.camp_id = camp_id
        self.init_parameters()

    def init_parameters(self):
        self.point = 0
        self.side = game_mode_const.E_ONE_SIDE
        self.occupy_num = 0

    def set_point(self, point):
        self.point = point

    def set_side(self, side):
        self.side = side


class COccupyData(object):

    def __init__(self, occupy_id):
        self.occupy_id = occupy_id
        self.init_parameters()

    def init_parameters(self):
        self.fraction_info = {}
        self.control_camp_id = None
        self.grap_camp_id = None
        self.grap_point = 0
        return

    def set_info(self, data):
        _, self.fraction_info, self.control_camp_id, self.grap_camp_id, self.grap_point = data


class KingBattleData(Singleton):
    ALIAS_NAME = 'king_battle_data'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.camp_status = {}
        self.my_camp_status = []
        self.camp = {}
        self.occupy = {}
        self.my_camp_id = 1
        self.member_money_dict = {}
        self.member_shop_cd_dict = {}
        self.camp_occupy_info = []
        self.beacon_tower_dict = {}
        self.rank_data = {}
        self.end_likes = {}
        self._king_point_enemy_data = None
        return

    def on_finalize(self):
        self.init_parameters()

    def set_my_camp_id(self, camp_id):
        self.my_camp_id = camp_id

    def init_camps(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        camp_num = cfg.get('camp_num', 0)
        e_side = 0
        for i in range(camp_num):
            camp_id = i + 1
            self.camp[camp_id] = CCampData(camp_id)
            if self.my_camp_id == camp_id:
                side = game_mode_const.MY_SIDE
            else:
                side = E_SIDES[e_side % len(E_SIDES)]
                e_side += 1
            self.camp[camp_id].set_side(side)

    def init_occupys(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        occupy_ids = cfg.get('king_point_list', [])
        for id in occupy_ids:
            self.occupy[id] = COccupyData(id)

    def update_camp_point(self, faction_id, faction_point):
        camp = self.camp.get(faction_id)
        if not camp:
            return
        camp.set_point(faction_point)
        global_data.emgr.update_camp_point.emit(faction_id)

    def update_camp_status(self, faction_status_dict):
        battle = global_data.battle
        self.camp_status = faction_status_dict
        my_faction_id = None
        self.my_camp_status = []
        if global_data.player and global_data.player.logic:
            my_faction_id = global_data.player.logic.ev_g_camp_id()
            groupmate_uids = set(global_data.player.logic.ev_g_groupmate_uids())
            faction_status = faction_status_dict.get(my_faction_id)
            if faction_status:
                for status in faction_status:
                    if not status:
                        continue
                    entity = battle.get_entity_by_aoi_id(status[0])
                    if not entity or entity and entity.uid not in groupmate_uids:
                        self.my_camp_status.append(status)

        global_data.emgr.update_camp_status.emit()
        for faction_id, faction_status in six.iteritems(faction_status_dict):
            if my_faction_id == faction_id:
                continue
            for enemy_info in faction_status:
                sync_id = enemy_info[0]
                enemy = battle.get_entity_by_aoi_id(sync_id)
                if not enemy or not enemy.logic:
                    continue
                enemy.logic.send_event('E_SHOW_PERSPECTIVE_MARK')

        return

    def update_occupy_status(self, king_status_list):
        self.camp_occupy_info = king_status_list
        for data_info in king_status_list:
            point_id = data_info[0]
            if point_id in self.occupy:
                self.occupy[point_id].set_info(data_info)

        self.update_camp_occupy_num()
        global_data.emgr.update_camp_occupy_info.emit()

    def update_camp_occupy_num(self):
        camp_occupy_num = {}
        for occupy_id, occupy_data in six.iteritems(self.occupy):
            if occupy_data.control_camp_id is not None:
                camp_occupy_num.setdefault(occupy_data.control_camp_id, 0)
                camp_occupy_num[occupy_data.control_camp_id] += 1

        for cam_id, occup_data in six.iteritems(self.camp):
            occup_data.occupy_num = camp_occupy_num.get(cam_id, 0)

        return

    def get_occupy_zone_status_data(self, point_id):
        return self.occupy.get(point_id, None)

    def update_beacon_tower_info(self, beacon_tower_dict):
        for beacon_tower_id, beacon_tower_info in six.iteritems(beacon_tower_dict):
            self.beacon_tower_dict.setdefault(beacon_tower_id, {})
            self.beacon_tower_dict[beacon_tower_id] = beacon_tower_info

    def update_rank_data(self, data):
        self.rank_data = data
        global_data.emgr.update_rank_data.emit(self.rank_data)

    def get_camp_status(self):
        return self.camp_status

    def get_my_camp_status(self):
        return self.my_camp_status

    def get_camp(self):
        return self.camp

    def set_money_info(self, entity_id, money_dict):
        self.member_money_dict[entity_id] = money_dict

    def get_money_info(self, entity_id):
        return self.member_money_dict.get(entity_id, {})

    def set_shop_bullet_cd(self, entity_id, cd):
        self.member_shop_cd_dict[entity_id] = cd

    def get_shop_bullet_cd(self, entity_id):
        return self.member_shop_cd_dict.get(entity_id, 0)

    def is_in_camp(self, player_pos, camp_id):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        key = 'camp0%d_base_center' % camp_id
        base_center_pos = cfg.get(key)
        base_half_length = cfg.get('camp0%d_base_length' % camp_id)
        base_half_width = cfg.get('camp0%d_base_width' % camp_id)
        if player_pos and base_center_pos:
            x_diff = abs(player_pos.x - base_center_pos[0])
            z_diff = abs(player_pos.z - base_center_pos[2])
            if x_diff <= base_half_length and z_diff <= base_half_width:
                return True
        return False

    def get_side_by_faction_id(self, faction_id):
        camp = self.camp.get(faction_id, None)
        if camp:
            return camp.side
        else:
            return game_mode_const.NONE_SIDE

    def get_occupy_camp_id(self, occupy_id):
        if occupy_id in self.occupy:
            return self.occupy[occupy_id].control_camp_id

    def get_occupy_camp_side(self, occupy_id):
        if occupy_id not in self.occupy:
            return game_mode_const.NONE_SIDE
        control_camp_id = self.occupy[occupy_id].control_camp_id
        if control_camp_id:
            return self.get_side_by_faction_id(control_camp_id)
        return game_mode_const.NONE_SIDE

    def get_rank_data(self):
        return self.rank_data

    def update_like_data(self, to_entity_id, praised_num):
        self.end_likes[to_entity_id] = praised_num

    def update_king_point_area(self, point_id, enemy_data):
        self._king_point_enemy_data = (
         point_id, enemy_data)

    def get_king_point_area_data(self):
        return self._king_point_enemy_data