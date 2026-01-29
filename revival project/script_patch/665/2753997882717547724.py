# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/WpGunServer.py
from __future__ import absolute_import
import six_ex
import math
from .Weapon import Weapon
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

class WpGunServer(Weapon):

    def __init__(self, weapon_data, battle):
        super(WpGunServer, self).__init__(weapon_data)
        self.iType = self._data['item_id']
        self.iAtkMode = ATK_GUN
        self._host_com = None
        self._carry_bullet_mode = False
        self._is_pve = battle.is_pve()
        gun_args.fill_gun_bullets(self._data, self._is_pve)
        limited_bullet_weapon_config.fill_gun_carry_bullet(self._data, self._is_pve)
        self.set_magazine(self._data)
        self._start_reload_time = 0
        self._is_in_reload = False
        if self.get_bullet_num() > 0:
            self.set_bolted(1)
        self._accumulate_guns = None
        self._accumulate_energys = None
        self._init_accumulate()
        self._cd_check_cnt = 0
        self._cd_used = 0
        self._cd_tlrc = 0
        self._continuous_laser_time = 0
        self._shoot_checker = ShootCheck()
        self._fire_cd_pos_factor_name = None
        if self.iType:
            pos = mecha_conf.get_mecha_weapon_pos(self.iType)
            if pos > 0:
                self._fire_cd_pos_factor_name = 'fShootSpeedFactor_pos_{}'.format(pos)
        self.first_shoot = True
        self.init_equip_func()
        return

    def destroy(self):
        self._host_com = None
        super(WpGunServer, self).destroy()
        return

    def set_multi_mode(self, enable):
        ret = super(WpGunServer, self).set_multi_mode(enable)
        if ret:
            self.reset_config()
        return ret

    def set_host_player(self, player_com):
        self._host_com = player_com
        if self._host_com:
            self._carry_bullet_mode = self._host_com.get_carry_bullet_mode()
        mag_key = player_com.ev_g_add_heat_magazine(self.iType, self._data.get('heat_info'))
        if mag_key:
            self._data['heat_key'] = mag_key
            mag = player_com.ev_g_heat_magazine(mag_key)
            if mag:
                self.set_magazine(mag)

    def get_config(self, *args):
        if self._conf:
            return self._conf
        _conf = {}
        iType = self.iType
        d = gun_args.get_config_by_type(self.iType, self._is_pve)
        if self.is_multi_mode():
            iType = d['multiMode'][1]
            d = gun_args.get_config_by_type(iType, self._is_pve)
        if d:
            _conf.update(d)
        if not _conf:
            log_error('WpGunServer read config failed iType={}'.format(iType))
        self._conf = _conf
        return self._conf

    def reset_config(self):
        self._conf = {}

    def init_from_dict(self, bdict):
        super(WpGunServer, self).init_from_dict(bdict)

    def get_last_reloaded_time(self):
        return self._magazine.get('last_reloaded_time')

    def get_kind(self):
        return self.conf('iKind')

    def get_equip_type(self):
        return self.conf('iEquipType')

    def get_id(self):
        return self.iType

    def get_exclude_lv_id(self):
        if gun_args.is_human_weapon(self.iType):
            return self.iType / 10
        else:
            return None
            return None

    def get_effective_conf(self, key):
        if key in self._effective_conf:
            return self._effective_conf[key]
        return self.conf(key)

    def get_attach_buffs(self):
        return tuple(self.conf('cCustomParam').get('attachBuffs', ()))

    def get_attach_fields(self):
        return self.conf('cCustomParam').get('attachFields', {})

    def get_bullet_type(self):
        if self._carry_bullet_mode and self.iType != INIT_UZI_WEAPON_ID:
            return ITEM_ID_LIMITED_BULLET
        return self.conf('iBulletType')

    def get_fire_cd(self):
        cd_time = self._data.get('cd_time') or self.conf('fCDTime')
        pos_factor = 0
        if self._fire_cd_pos_factor_name:
            pos_factor = self._host_com.ev_g_add_attr(self._fire_cd_pos_factor_name)
        common_factor = self._host_com.ev_g_add_attr(attr_const.ATTR_SHOOTSPEED_FACTOR, self.iType)
        if pos_factor + common_factor < -1:
            return cd_time
        cd_time *= 1 / (1 + pos_factor + common_factor)
        return max(cd_time, 0.01)

    def check_cd(self, t_use):
        cnt = self.get_bullet_pellets_cnt()
        self._cd_check_cnt += 1
        self._cd_used += t_use
        if self._cd_check_cnt >= cnt:
            normal_cd = self.get_fire_cd()
            exp_cd = normal_cd * 0.9
            max_tlrc = max(normal_cd * 1.5, 0.5)
            if self._cd_used > exp_cd:
                self._cd_tlrc = min(max_tlrc, self._cd_tlrc + (self._cd_used - exp_cd))
            if self._cd_used < exp_cd:
                self._cd_tlrc = self._cd_tlrc - (exp_cd - self._cd_used)
                if self._cd_tlrc < 0:
                    self._cd_tlrc = 0
                    return False
            self._cd_used = 0
            self._cd_check_cnt = 0
        return True

    def in_continuous_laser_interval(self):
        normal_cd = self.get_fire_cd()
        now = tutil.get_time()
        if now < self._continuous_laser_time + normal_cd * 2:
            return True
        return False

    def set_continuous_laser_check_time(self):
        self._continuous_laser_time = tutil.get_time()

    def start_reload(self):
        self._start_reload_time = tutil.get_time()
        self._is_in_reload = True

    def get_reload_time(self):
        if self._start_reload_time:
            return tutil.get_time() - self._start_reload_time
        return 0

    def get_bullet_pellets(self):
        return self._effective_conf.get('iPellets', self.conf('iPellets'))

    def get_bullet_pellets_cnt(self):
        pellets = self.get_bullet_pellets()
        if isinstance(pellets, int):
            return pellets
        else:
            return sum(pellets['bullets'])

    def get_bullet_cap(self):
        return self._magazine.get('iBulletCap', 0)

    def set_bullet_cap(self, val):
        self._magazine['iBulletCap'] = val

    def get_base_bullet_cap(self):
        return get_base_mag_size(self.iType)

    def set_first_shoot(self, val):
        self.first_shoot = val

    def get_first_shoot(self):
        return self.first_shoot

    def on_load(self):
        base_mag_size = self.get_base_bullet_cap()
        cur_bullet_num = self.get_bullet_num()
        self.set_bullet_cap(base_mag_size)
        if cur_bullet_num > base_mag_size:
            self.set_bullet_num(base_mag_size)

    def get_reload_ratio(self):
        return self.conf('iReloadRatio', 1)

    def get_cost_ratio(self):
        src_val = self.conf('iCostRatio', 1)
        if self._host_com:
            return self._host_com.ev_g_addition_effect(src_val, self.iType, key='iCostRatio', item_eid=self.get_entity_id())
        return src_val

    def get_data_by_key(self, key):
        return self._effective_conf.get(key, self.conf(key))

    def get_reload_num(self):
        bullet_cap = self.get_bullet_cap()
        bullet_num = self.get_bullet_num()
        if self.get_bullet_type() == ITEM_ID_LIMITED_BULLET:
            reload_num = math.ceil(float(bullet_cap - bullet_num))
        else:
            reload_ratio = self.get_reload_ratio()
            reload_num = int(math.ceil(float(bullet_cap - bullet_num) / reload_ratio))
        return max(0, reload_num)

    def is_bullet_full(self):
        return self.get_bullet_cap() == self.get_bullet_num()

    def is_bullet_empty(self):
        return self.get_bullet_num() == 0

    def get_bullet_num(self):
        return self._magazine.get('iBulletNum', 0)

    def set_bullet_num(self, iNum):
        self._magazine['iBulletNum'] = max(0, min(iNum, self.get_bullet_cap()))

    def get_buff_keep_bullet(self):
        self._magazine.get('keep_bullet') or (0, 0)

    def set_buff_keep_bullet(self, iNum, next_time):
        self._magazine['keep_bullet'] = (
         iNum, next_time)

    def get_bolted(self):
        return self._data.get('iBolted', 0)

    def set_bolted(self, iBolted=1):
        self._data['iBolted'] = iBolted

    def get_attachment_attr(self, pos):
        return None

    def get_bullet_recovery_rate(self):
        return self.get_config().get('cCustomParam', {}).get('iBulletRecoverRate')

    def set_magazine(self, magazine):
        if not magazine:
            return
        if 'iBulletCap' not in magazine:
            magazine['iBulletCap'] = self.conf('iMagSize')
        self._magazine = magazine

    def get_magazine(self):
        return self._magazine

    def is_normal_magazine(self):
        return self._magazine is self._data

    def is_heat_weapon(self):
        return self._magazine.get('magazine_type', MAGAZINE_TYPE_NORMAL) == MAGAZINE_TYPE_HEAT

    def get_heat_key(self):
        return self._data.get('heat_key', 0)

    def cost_bullet(self, sub):
        if not self.is_enable() and not self.conf('iForcePellets', False):
            return 0
        if sub <= 0:
            return 0
        if self.get_bullet_cap() == 0:
            magazine_type = self._magazine.get('magazine_type', 0)
            cost_handler = weapon_utils.COST_BULLET_HANDLER.get(magazine_type)
            if cost_handler:
                return cost_handler(self._magazine, sub)
            return sub
        cost_ratio = self.get_cost_ratio()
        if cost_ratio <= 0:
            return sub
        iCurBulletNum = self.get_bullet_num()
        cost_bullet = sub * cost_ratio
        if cost_bullet > iCurBulletNum:
            return 0
        self.set_bullet_num(iCurBulletNum - cost_bullet)
        self._host_com.send_event('E_COST_BULLET', self, cost_bullet)
        return sub

    def reload(self, ammo_num):
        if ammo_num <= 0:
            return
        if self.get_bullet_type() == ITEM_ID_LIMITED_BULLET:
            add_bullet_num = ammo_num
        else:
            add_bullet_num = ammo_num * self.get_reload_ratio()
        iCurBulletNum = self.get_bullet_num()
        self.set_bullet_num(iCurBulletNum + add_bullet_num)
        self.set_first_shoot(False)
        self._start_reload_time = 0
        self._is_in_reload = False
        recovery_rate = self.get_bullet_recovery_rate()
        if not recovery_rate:
            return
        self._magazine['last_reloaded_time'] = tutil.get_time()

    def is_in_reload(self):
        return self._is_in_reload

    def _init_accumulate(self):
        info = s_energy_cd_mapping.data.get(self.iType)
        if info is None:
            return
        else:
            self._accumulate_energys = sorted(six_ex.keys(info))
            self._accumulate_guns = []
            for energy in self._accumulate_energys:
                self._accumulate_guns.append(info[energy])

            return

    def get_accumulate_gun_by_energy_cd(self, energy):
        if self._accumulate_energys is None:
            return (None, None)
        else:
            for i, f_cmp_cd in enumerate(self._accumulate_energys):
                if f_cmp_cd < energy:
                    continue
                return (
                 self._accumulate_guns[i], i)
            else:
                return (
                 self._accumulate_guns[i], i)

            return

    def mod_accumulate_energy(self, rate):
        if self._accumulate_energys is None:
            return
        else:
            for i, energy in enumerate(self._accumulate_energys):
                self._accumulate_energys[i] = energy * (1 + rate)

            return

    def restore_accumulate_energy(self):
        if self._accumulate_energys is None:
            return
        else:
            info = s_energy_cd_mapping.data.get(self.iType)
            if info is None:
                self._accumulate_energys = None
            self._accumulate_energys = sorted(six_ex.keys(info))
            return

    def _continue_fire_add(self, fire_cnt):
        continue_fire_param = self._data.get('continue_fire_param', None)
        if continue_fire_param:
            continue_fire_cnt = min(fire_cnt, continue_fire_param.get('max_cnt', 0))
            if continue_fire_cnt > 0:
                base_power_factor = continue_fire_cnt * continue_fire_param.get('ratio_per_cnt', 0)
                return (
                 base_power_factor, continue_fire_cnt)
        return (0, 0)

    def get_bullet_shoot_once(self):
        pellets = self.get_bullet_pellets()
        if self.get_kind() == 10:
            return 1
        else:
            if self.get_cost_ratio() > 1:
                return self.get_cost_ratio()
            if isinstance(pellets, int):
                return pellets
            return sum(pellets['bullets'])

    def do_one_shoot(self, t_use):
        fire_cd = self.get_fire_cd()
        pellet = self.get_bullet_pellets_cnt()
        cr, sr = self._shoot_checker.do_one_shoot(t_use, fire_cd, pellet)
        if cr and self._host_com:
            self._host_com.send_event('E_REPORT_SHOOT_SPEED', self.iType, cr, sr)

    def transfer_weapon(self, original_weapon, info):
        magazine = original_weapon.get_magazine()
        if magazine.get('magazine_type', MAGAZINE_TYPE_NORMAL) != MAGAZINE_TYPE_NORMAL:
            self.set_magazine(magazine)
        if not info:
            info = {}
        if info.get('sync_bullet', False):
            self.set_bullet_num(magazine.get('iBulletNum', 0))
        if info.get('transfer_attr', False):
            self._host_com.send_event('E_TRANSFER_WP_ATTR', original_weapon.get_id(), [self.iType])
        elif info.get('transfer_attr_energy_cd', False):
            old_weapon_itype = original_weapon.get_id()
            new_weapon_itype = self.get_id()
            transfer_from_weapon_ids = [ x for x in six_ex.values(s_energy_cd_mapping.data.get(old_weapon_itype, {})) ]
            transfer_to_weapon_ids = [ x for x in six_ex.values(s_energy_cd_mapping.data.get(new_weapon_itype, {})) ]
            if transfer_from_weapon_ids and len(transfer_from_weapon_ids) == len(transfer_to_weapon_ids):
                for i, from_weapon_id in enumerate(transfer_from_weapon_ids):
                    to_weapon_id = transfer_to_weapon_ids[i]
                    if from_weapon_id != to_weapon_id:
                        self._host_com.send_event('E_TRANSFER_WP_ATTR', from_weapon_id, [to_weapon_id])

    def get_carry_bullet_num(self):
        return self._magazine.get('iCarryBulletNum', 0)

    def get_carry_bullet_cap(self):
        return self._magazine.get('iCarryBulletCap', 0)

    def set_carry_bullet_num(self, iNum):
        self._magazine['iCarryBulletNum'] = max(0, min(iNum, self.get_carry_bullet_cap()))
        self.dirty = False

    def cost_carry_bullet(self, iNum):
        if iNum <= 0:
            return
        self.set_carry_bullet_num(max(self.get_carry_bullet_num() - iNum, 0))