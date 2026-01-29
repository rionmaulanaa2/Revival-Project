# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/WpGunClient.py
from __future__ import absolute_import
import six
from six.moves import range
import math
import time as org_time
from common.cfg import confmgr
from .Weapon import Weapon
from logic.gcommon.const import ATK_GUN
from logic.gcommon import time_utility
from logic.gcommon.common_const import attr_const
from logic.gutils.weapon_utils import fast_aim_and_fire_setting_enable, fast_aim_and_release_fire_setting_enable, auto_fast_aim_and_fire_setting_enable
from logic.gcommon.common_const.ui_operation_const import SHOTGUN_WEAPON_FIRE_RELEASE_KEY, ANTI_MECHA_WEAPON_FIRE_RELEASE_KEY, MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY, SNIPER_RIFLE_FAST_AIM_AND_RELEASE_FIRE_KEY, AUTO_FAST_AIM_AND_FIRE_KEY
from logic.gcommon.common_const.weapon_const import CONTROL_MODEL_WEAPON_TYPE_SHOTGUN, CONTROL_MODEL_END, CONTROL_MODEL_BEGIN, CONTROL_MODEL_WEAPON_TYPE_ANTI_MECHA, CONTROL_WEAPON_MANUAL_SNIPER_RIFLE, CONTROL_WEAPON_FAST_AIM_AND_RELEASE_FIRE, CONTROL_WEAPON_AUTO_FAST_AIM_AND_FIRE
from logic.gutils import mecha_utils
from logic.gcommon.common_const.weapon_const import MAGAZINE_TYPE_NORMAL, ITEM_ID_LIMITED_BULLET, INIT_UZI_WEAPON_ID

class WpGunClient(Weapon):

    def __init__(self, weapon_data):
        super(WpGunClient, self).__init__(weapon_data)
        self._base_type = self._data['item_id']
        self.iType = self._data['item_id']
        self.set_magazine(self._data)
        self.iAtkMode = ATK_GUN
        self._player_attr = {}
        self._host_com = None
        self._owned_by_avatar = False
        self._is_accumulate_gun = False
        self._accumulate_max_time = 0.0
        self._accumulate_level = 0
        self._accumulate_levels = []
        self._accumulate_weapons = []
        self._dec_percent = 0
        self._is_navigate_enabled = confmgr.get('navigate_config', str(self.iType), 'iIsNavigate', default=0)
        self._update_accumulate_info()
        self._last_fire_time = 0
        self._conf_cache = {}
        if self.get_bullet_num() > 0:
            self.set_bolted(1)
        self._init_multi_mode()
        self._fire_cd_pos_factor_name = None
        if self.iType:
            pos = mecha_utils.get_mecha_weapon_pos(self.iType)
            if pos > 0:
                self._fire_cd_pos_factor_name = 'fShootSpeedFactor_pos_{}'.format(pos)
        self.init_equip_func()
        self.heat_magazine = None
        self.interval_factor = 0
        return

    def set_player_attr(self, player_attr):
        if self._player_attr is not player_attr:
            self._player_attr = player_attr
            self.reset_config()

    def set_host_player(self, player_com):
        self._host_com = player_com
        self._owned_by_avatar = False
        if player_com:
            if global_data.player and global_data.player.logic and global_data.player.logic == player_com.unit_obj:
                self._owned_by_avatar = True
        heat_key = self._data.get('heat_key', 0)
        if heat_key and player_com:
            self.heat_magazine = player_com.ev_g_heat_magazine(heat_key)

    def get_attachment_data(self, attachment_id):
        return confmgr.get('firearm_component', str(attachment_id), default=None)

    def get_config(self, weapon_id=None, *args):
        _conf = {}
        wp_type = self.iType if weapon_id is None else weapon_id
        if wp_type in self._conf_cache:
            _conf = self._conf_cache[wp_type]
            if weapon_id is None:
                self._conf = _conf
            return _conf
        else:
            from logic.gutils.weapon_utils import get_weapon_conf
            d = get_weapon_conf(str(wp_type))
            if d:
                _conf.update(d)
            else:
                raise Exception('WpGunClient get_config failed, iType={}'.format(self.iType))
            if not _conf:
                log_error('WpGunClient read config failed iType={}'.format(self.iType))
            _conf = self.load_attachment_conf(_conf)
            self._conf_cache[wp_type] = _conf
            if weapon_id is None:
                self._conf = _conf
            return _conf

    def _update_accumulate_info(self):
        accumulate_config = confmgr.get('accumulate_config', str(self.iType), default=None)
        self._is_accumulate_gun = accumulate_config != None
        if self._is_accumulate_gun:
            self._accumulate_level = accumulate_config['iMaxLevel']
            self._accumulate_levels = [ accumulate_config['fEnergyCD_{}'.format(name_id)] for name_id in range(self._accumulate_level) ]
            self._accumulate_weapons = [ accumulate_config['iItemID_{}'.format(name_id)] for name_id in range(self._accumulate_level) ]
            self._accumulate_max_time = accumulate_config['fMaxCD']
        return

    def reset_config(self):
        self._conf = {}
        self._conf_cache = {}

    def load_attachment_conf(self, _conf):
        fixed_attachment = {}
        for com_id in _conf['arrCom']:
            com_data = self.get_attachment_data(com_id)
            if com_data:
                fixed_attachment[com_data['iPos']] = com_data

        _conf['fixed_attachment'] = fixed_attachment
        attachment = self._data.get('attachment', {})
        modified_attr = {'fCDTime': 'fCDTime',
           'fCDTime2': 'fCDTime2',
           'fReloadTimeEmpty': 'fReloadTimeEmpty',
           'fReloadTimeLeft': 'fReloadTimeLeft',
           'fPellets': 'iPellets',
           'fSprayAngle': 'fSprayAngle',
           'fRecoilUp': 'fRecoilUp',
           'fRecoilLeft': 'fRecoilLeft',
           'fRecoilRight': 'fRecoilRight',
           'fRecoilTime': 'fRecoilTime',
           'fRecoverV': 'fRecoverV',
           'fRecoilDec': 'fRecoilDec',
           'fFirstShotMul': 'fFirstShotMul',
           'fSpreadInc': 'fSpreadInc',
           'fSpreadDec': 'fSpreadDec',
           'fADSStop': 'fADSStop',
           'fADSMove': 'fADSMove',
           'fHIPStandStop': 'fHIPStandStop',
           'fHIPCrouchStop': 'fHIPCrouchStop',
           'fHIPStandMove': 'fHIPStandMove',
           'fHIPCrouchMove': 'fHIPCrouchMove',
           'fHIPJump': 'fHIPJump'
           }
        value_added = {}
        value_modified = {}
        from logic.gcommon.const import ATTACHMENT_POS_LIST
        for pos in ATTACHMENT_POS_LIST:
            attachment_conf = None
            if pos in attachment and attachment[pos]:
                attachment_conf = self.get_attachment_data(attachment[pos]['item_id'])
            if not attachment_conf and pos in fixed_attachment:
                attachment_conf = fixed_attachment[pos]
            if not attachment_conf:
                continue
            for key_attr, value_attr in six.iteritems(modified_attr):
                if key_attr in attachment_conf:
                    value_modified[value_attr] = value_modified.get(value_attr, 1) + attachment_conf[key_attr]

            for attr, value in six.iteritems(attachment_conf['cAttr']):
                if isinstance(value, list):
                    value_added.setdefault(attr, [])
                    value_added[attr].extend(value)
                else:
                    value_added[attr] = value_added.get(attr, 0) + value

            _conf['iMagSize'] += attachment_conf['cMagSize'].get(str(self.iType), 0)

        for attr, value in six.iteritems(self._player_attr):
            value_modified[attr] = value_modified.get(attr, 1) + value

        for key_attr, value_item in six.iteritems(value_modified):
            value = _conf[key_attr] * value_item
            if key_attr[0] == 'i':
                _conf[key_attr] = int(value)
            else:
                _conf[key_attr] = value

        for attr, value in six.iteritems(value_added):
            if isinstance(value, list):
                _conf.setdefault(attr, [])
                _conf[attr].extend(value)
            else:
                _conf[attr] = _conf.get(attr, 0) + value

        return _conf

    def get_last_reloaded_time(self):
        return self._magazine.get('last_reloaded_time')

    def get_kind(self):
        return self.get_effective_value('iKind')

    def get_equip_type(self):
        return self.get_effective_value('iEquipType')

    def get_id(self):
        return self.iType

    def get_item_id(self):
        return self.iType

    def get_attach_buffs(self):
        return tuple(self.conf('cCustomParam').get('attachBuffs', ()))

    def get_sequence_recover_speed(self):
        return self.conf('cCustomParam').get('sequence_recover_speed', 0)

    def get_attach_fields(self):
        return self.conf('cCustomParam').get('attachFields', {})

    def get_one_shoot_bullet_num(self):
        return self.conf('cCustomParam').get('one_shoot_bullet_num', 1)

    def get_custom_direction(self):
        return self.conf('cCustomParam').get('custom_direction', [])

    def get_bullet_type(self):
        if global_data.battle and global_data.battle._carry_bullet_mode and self.iType != INIT_UZI_WEAPON_ID:
            return ITEM_ID_LIMITED_BULLET
        return self.get_effective_value('iBulletType')

    def get_fire_cd(self):
        cd_time = self._data.get('fCDTime') or self.conf('fCDTime')
        factor = self._host_com.ev_g_add_attr(attr_const.ATTR_SHOOTSPEED_FACTOR, self.iType)
        if self._fire_cd_pos_factor_name:
            factor += self._host_com.ev_g_add_attr(self._fire_cd_pos_factor_name)
        if self.heat_magazine:
            factor += self.heat_magazine.get_fire_cd_ratio()
        if factor < -1:
            return cd_time
        cd_time *= 1 / (1 + factor)
        return cd_time

    def get_bullet_pellets(self):
        return self.get_effective_value('iPellets')

    def get_spray_angle(self):
        return self.get_effective_value('fSprayAngle')

    def get_reload_type(self):
        return self.get_effective_value('iReloadType')

    def get_ui_cd(self):
        return self.get_effective_value('fCDTimeUI')

    def get_shot_type(self, custom_dict={}):
        if self._owned_by_avatar:
            cat = self.get_data_by_key('iControlCat')
            maintain_org = False
            right_mode = custom_dict.get('right_mode', False)
            if cat == CONTROL_MODEL_WEAPON_TYPE_SHOTGUN:
                setting_key = SHOTGUN_WEAPON_FIRE_RELEASE_KEY
                release_trigger = global_data.player.get_setting_2(setting_key)
            elif cat == CONTROL_MODEL_WEAPON_TYPE_ANTI_MECHA:
                setting_key = ANTI_MECHA_WEAPON_FIRE_RELEASE_KEY
                release_trigger = global_data.player.get_setting_2(setting_key)
            elif cat == CONTROL_WEAPON_MANUAL_SNIPER_RIFLE and right_mode:
                release_trigger = fast_aim_and_fire_setting_enable()
                setting_key = MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY
                maintain_org = True
            elif cat == CONTROL_WEAPON_FAST_AIM_AND_RELEASE_FIRE and right_mode:
                release_trigger = fast_aim_and_release_fire_setting_enable()
                setting_key = SNIPER_RIFLE_FAST_AIM_AND_RELEASE_FIRE_KEY
                maintain_org = True
            else:
                setting_key = None
                release_trigger = False
            if setting_key is not None:
                if release_trigger:
                    shot_type = CONTROL_MODEL_END
                else:
                    shot_type = maintain_org or CONTROL_MODEL_BEGIN if 1 else self.get_data_by_key('iControl')
                return shot_type
        return self.get_data_by_key('iControl')

    def is_shotgun(self):
        pellets = self.get_bullet_pellets()
        if isinstance(pellets, int) and pellets > 1:
            return True
        return False

    def get_bullet_cap(self):
        return self._magazine.get('iBulletCap', self.get_effective_value('iMagSize'))

    def set_bullet_cap(self, val):
        self._magazine['iBulletCap'] = val

    def get_reload_ratio(self):
        return self.get_effective_value('iReloadRatio', 1)

    def get_cost_ratio(self):
        src_val = self.get_effective_value('iCostRatio', 1)
        if self._host_com:
            ratio = self._host_com.ev_g_add_attr('mul_iCostRatio', self.iType, item_eid=self.get_entity_id())
            pos = mecha_utils.get_mecha_weapon_pos(self.iType)
            ratio += self._host_com.ev_g_add_attr('bullet_cost_ratio_pos_%s' % pos, item_eid=self.get_entity_id())
            src_val *= 1 + ratio
        return max(src_val, 0)

    def get_show_ratio(self):
        r = self.get_effective_value('fShowRatio', 1)
        if r < 0:
            return -1.0 / r
        else:
            if r > 0:
                return r
            return 1

    def get_data_by_key(self, key):
        if global_data.wp_ed_data and 'firearm_config' in global_data.wp_ed_data and str(self.iType) in global_data.wp_ed_data['firearm_config'] and key in global_data.wp_ed_data['firearm_config'][str(self.iType)]:
            return global_data.wp_ed_data['firearm_config'][str(self.iType)][key]
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

    def have_enough_bullet(self, b_num=1):
        need_num = b_num * self.get_cost_ratio()
        if need_num <= self.get_bullet_num():
            return True
        else:
            return False

    def set_bullet_num(self, iNum):
        self._magazine['iBulletNum'] = max(0, min(iNum, self.get_bullet_cap()))
        self.dirty = False

    def get_wind_up_time(self):
        return self.get_effective_value('fWindupTime', 0.0)

    def get_hold_time(self):
        return self.get_effective_value('fHoldTime', 0.0)

    @property
    def dirty(self):
        return self._magazine['dirty']

    @dirty.setter
    def dirty(self, flag):
        self._magazine['dirty'] = flag

    def get_bolted(self):
        return self._data.get('iBolted', 0)

    def set_bolted(self, iBolted=1):
        self._data['iBolted'] = iBolted

    def get_attachment_attr(self, pos):
        self.get_config()
        attachment = self._data.get('attachment', {})
        if pos in attachment and attachment[pos]:
            attachment_attr = confmgr.get('firearm_component', str(attachment[pos]['item_id']), default=None)
            if attachment_attr:
                return attachment_attr
        attachment = self._conf.get('fixed_attachment', {})
        if pos in attachment:
            return attachment[pos]
        else:
            return

    def conf_res(self, key):
        return confmgr.get('firearm_res_config', str(self.iType), str(key))

    def get_bullet_recovery_rate(self):
        return self.get_config().get('cCustomParam', {}).get('iBulletRecoverRate')

    def set_magazine(self, magazine):
        magazine['dirty'] = False
        self._magazine = magazine

    def get_magazine(self):
        return self._magazine

    def get_related_weapon_pos(self):
        return self._magazine.get('related_pos', ())

    def get_check_reload_after_fire(self):
        return self.get_config().get('cCustomParam', {}).get('check_reload_after_fire', True)

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
        if cost_bullet > iCurBulletNum:
            return 0
        self.set_bullet_num(iCurBulletNum - cost_bullet)
        return sub

    def reload(self, ammo_num):
        if ammo_num <= 0:
            return
        bullet_type = self.get_bullet_type()
        if bullet_type == ITEM_ID_LIMITED_BULLET:
            self.cost_carry_bullet(ammo_num)
        add_bullet_num = ammo_num * self.get_reload_ratio()
        iCurBulletNum = self.get_bullet_num()
        self.set_bullet_num(iCurBulletNum + add_bullet_num)
        recovery_rate = self.get_bullet_recovery_rate()
        if not recovery_rate:
            return
        self._magazine['last_reloaded_time'] = time_utility.get_server_time_battle()

    def is_accumulate_gun(self):
        return self._is_accumulate_gun

    def get_accumulate_max_time(self):
        customed_max_time = self._host_com.ev_g_weapon_accumulate_max_time(self.iPos) if self._host_com else None
        if customed_max_time:
            return customed_max_time * (1 - self._dec_percent)
        else:
            return self._accumulate_max_time * (1 - self._dec_percent)

    def set_accumulate_dec_percent(self, dec_percent):
        self._dec_percent += dec_percent * 1.0 / 100

    def get_acc_levels(self):
        if self._host_com:
            customed_level = self._host_com.ev_g_weapon_accumulate_level(self.iPos) if 1 else None
            return customed_level or self._accumulate_levels
        else:
            return customed_level

    def get_accumulate_level(self, energy_cd):
        for index, data in enumerate(self.get_acc_levels()):
            if energy_cd < data * (1 - self._dec_percent):
                return index

        return len(self._accumulate_levels) - 1

    def get_accumulate_weapon_id(self, energy_cd):
        for index, data in enumerate(self.get_acc_levels()):
            if energy_cd < data * (1 - self._dec_percent):
                return int(self._accumulate_weapons[index])

        if self._accumulate_weapons:
            return self._accumulate_weapons[-1]
        return self.iType

    def set_is_navigate_enabled(self, flag):
        self._is_navigate_enabled = flag

    def get_is_navigate_enabled(self):
        return self._is_navigate_enabled

    def get_last_fire_time(self):
        return self._last_fire_time

    def get_fire_use_time(self):
        now = org_time.time()
        t_use = now - self._last_fire_time
        self._last_fire_time = now
        return t_use

    def switch_wp_mode(self, enable):
        wp_mode_id = self.get_multi_item_id()
        if not self.set_multi_mode(enable):
            return False
        self.iType = wp_mode_id if enable else self._base_type
        self._effective_conf = {}
        self._is_navigate_enabled = confmgr.get('navigate_config', str(self.iType), 'iIsNavigate', default=0)
        self._update_accumulate_info()
        return True

    def is_multi_wp(self):
        conf = self.get_config(self._base_type)
        if conf.get('multiMode', None):
            return True
        else:
            return False

    def get_multi_kind(self):
        conf = self.get_config(self._base_type)
        multiMode = conf.get('multiMode', None)
        if multiMode:
            return multiMode[0]
        else:
            return 0

    def get_multi_item_id(self):
        conf = self.get_config(self._base_type)
        multiMode = conf.get('multiMode', None)
        if multiMode:
            return multiMode[1]
        else:
            return

    def is_in_multi_mode(self):
        return self.is_multi_wp() and self._data.get('is_multi_mode', False)

    def _init_multi_mode(self):
        if self.is_in_multi_mode():
            self.switch_wp_mode(True)

    def transfer_weapon(self, original_weapon):
        magazine = original_weapon.get_magazine()
        if magazine.get('magazine_type', MAGAZINE_TYPE_NORMAL) != MAGAZINE_TYPE_NORMAL:
            self.set_magazine(magazine)

    def destroy(self):
        self._host_com = None
        self.heat_magazine = None
        super(WpGunClient, self).destroy()
        return

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