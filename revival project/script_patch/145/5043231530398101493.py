# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/PveWpGunServer.py
from __future__ import absolute_import
import six
import math
from Weapon import Weapon
from WpGunServer import WpGunServer
from logic.gcommon.const import ATK_GUN
from logic.gcommon.common_const.weapon_const import MAGAZINE_TYPE_NORMAL, MAGAZINE_TYPE_HEAT
from logic.gcommon import time_utility as tutil
from data import s_energy_cd_mapping
import data.gun_args as gun_args
import data.gun_attachment as gun_attachment
from logic.gcommon.common_const import attr_const
from data import mecha_conf, limited_bullet_weapon_config
from data.gun_args import get_weapon_type_by_item_id
from logic.gutils.anticheat.shoot_detect import ShootCheck
from logic.gcommon.common_utils import weapon_utils
from data.gun_args import get_base_mag_size
from logic.gcommon.common_const.weapon_const import ITEM_ID_LIMITED_BULLET, INIT_UZI_WEAPON_ID
from data.pve.weapon_bonus_data import get_random_bonus

class PveWpGunServer(WpGunServer):

    def __init__(self, weapon_data):
        super(PveWpGunServer, self).__init__(weapon_data)
        self._quality = weapon_data.get('quality', 'D')
        self._bonus = []
        self._fire_no_cost_record = {}

    def get_bonus_id(self, bonus_idx):
        return self._bonus[bonus_idx]

    def get_bonus(self):
        return self._bonus

    def generate_bonus(self, cnt=3):
        bonus = get_random_bonus(cnt, self._bonus)
        self._bonus.extend(bonus)

    def cost_bullet(self, sub):
        if not self.is_enable():
            return 0
        if sub <= 0:
            return 0
        if self.get_bullet_cap() == 0:
            return sub
        cost_ratio = self.get_cost_ratio()
        if cost_ratio <= 0:
            return sub
        iCurBulletNum = self.get_bullet_num()
        cost_bullet = sub * cost_ratio
        if self.check_no_cost:
            cost_bullet = 0
        if cost_bullet > iCurBulletNum:
            return 0
        self.set_bullet_num(iCurBulletNum - cost_bullet)
        return sub

    def check_no_cost(self):
        no_cost = False
        for fire_cnt, now_cnt in six.iteritems(self._fire_no_cost_record):
            now_cnt += 1
            if now_cnt >= fire_cnt:
                self._fire_no_cost_record[fire_cnt] = 0
                no_cost = True

        return no_cost