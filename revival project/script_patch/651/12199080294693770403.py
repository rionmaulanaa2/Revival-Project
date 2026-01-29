# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComThrowableDriver.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import time as org_time
from logic.gcommon import time_utility as t_util
from common.cfg import confmgr
from logic.gcommon.common_const.weapon_const import WP_NAVIGATE_GUN
from logic.gcommon.common_const import attr_const

class ComThrowableDriver(UnitCom):
    BIND_EVENT = {'E_THROW_EXPLOSIVE_ITEM': 'add_throw_explosive_item',
       'E_SHOOT_EXPLOSIVE_ITEM': 'add_shoot_explosive_item',
       'E_MOD_EXPLOSIVE_ITEM_ATTR': '_mod_addition_attr',
       'E_SET_MISSILE_LOCK_TARGET': 'set_missile_lock_target',
       'G_GET_MISSILE_LOCK_TARGET': 'get_missile_lock_target'
       }
    STAND_THROW_ACTION_NAME = 'stand.throw_out'
    CRAWL_THROW_ACTION_NAME = 'crawl.throw_out'

    def __init__(self):
        super(ComThrowableDriver, self).__init__()
        self._addition_attr = {}
        self._missile_lock_target_id = None
        self._last_shoot_start = {}
        self._special_exec = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComThrowableDriver, self).init_from_dict(unit_obj, bdict)
        self._missile_lock_target_id = bdict.get('missile_lock', None)
        return

    def _mod_addition_attr(self, item_id, attr, mod):
        self._addition_attr.setdefault(item_id, {})
        self._addition_attr[item_id].setdefault(attr, 0.0)
        self._addition_attr[item_id][attr] += mod

    def add_throw_explosive_item(self, info):
        info['begin_time'] = t_util.time()
        self._explosive_item_to_scene(info)

    def _explosive_item_to_scene(self, data):
        data['throw_speed_add_rate'] = self.ev_g_add_attr(attr_const.ATTR_THROW_SPEED_ADD_FACTOR, data.get('item_itype'))
        data['owner_id'] = self.unit_obj.id
        data['trigger_id'] = self.unit_obj.id
        data['faction_id'] = self.ev_g_camp_id()
        global_data.emgr.scene_add_throw_item_event.emit(data)

    def add_shoot_explosive_item(self, info, need_sync_server=False):
        now = org_time.time()
        wp_pos = info.get('wp_pos', 0)
        last_shoot_start = self._last_shoot_start.get(wp_pos, 0)
        delta_itvl = now - last_shoot_start
        self._last_shoot_start[wp_pos] = now
        info['t_cd'] = delta_itvl
        if need_sync_server:
            info['call_sync_id'] = global_data.battle_idx
            sync_data = {}
            sync_data.update(info)
            self.send_event('E_CALL_SYNC_METHOD', 'shoot_explosive_item', (sync_data,), True)
        s_item_id = str(info['item_itype'])
        conf = confmgr.get('grenade_config', s_item_id)
        info['speed'] = info.get('fSpeed', conf['fSpeed'])
        info['mass'] = conf['fMass']
        info['last_time'] = conf['fTimeFly']
        info['gravity'] = conf['fGravity']
        if confmgr.get('firearm_config', s_item_id, 'iKind') == WP_NAVIGATE_GUN:
            info['speed'] = confmgr.get('navigate_config', s_item_id, 'fSpeedInit')
        info['begin_time'] = t_util.time()
        if self._special_exec:
            self._special_exec(info)
        self._explosive_item_to_scene(info)

    def set_missile_lock_target(self, id_target):
        self._missile_lock_target_id = id_target
        self.send_event('E_ON_MISSILE_LOCK_TARGET_CHANGE', id_target)

    def get_missile_lock_target(self):
        return self._missile_lock_target_id