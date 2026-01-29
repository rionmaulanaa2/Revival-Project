# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComAtAim.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom

class ComAtAim(UnitCom):
    BIND_EVENT = {'E_CHANGE_AT_AIM_ARGS': 'change_at_aim_args',
       'E_SET_AT_AIM_ARGS': 'set_at_aim_args_all',
       'G_AT_AIM_ARGS_BY_KEY': '_get_at_aim_args',
       'G_AT_AIM_ARGS_ALL': '_get_at_aim_all_args',
       'E_BUFF_A_MOD_AIM': '_on_buff_mod_aim',
       'E_BUFF_D_MOD_AIM': '_restore_buff_mod_aim',
       'E_ARMOR_DATA_CHANGED': '_on_armor_data_change',
       'G_AT_AIM_PCNT_Y': '_get_pcnt_y',
       'G_AT_AIM_PCNT_X': '_get_pcnt_x'
       }
    KEY_PREFIX_ARMOR = 'am_'
    KEY_PREFIX_WEAPON = 'wp_'
    KEY_PREFIX_BUFF = 'bf_'

    def __init__(self):
        super(ComAtAim, self).__init__()
        self._f_aim_x = 1.0
        self._f_aim_y = 1.0
        self._f_aim_r = 1.0
        self._mp_ad_aim = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComAtAim, self).init_from_dict(unit_obj, bdict)
        self._f_aim_x = bdict.get('aim_x', 1.0)
        self._f_aim_y = bdict.get('aim_y', 1.0)
        self._f_aim_r = bdict.get('aim_r', 1.0)
        self._buff = None
        return

    def get_client_dict(self):
        return {'aim_x': self._f_aim_x,
           'aim_y': self._f_aim_y,
           'aim_r': self._f_aim_r
           }

    def _get_at_aim_args(self, key):
        attr_name = '_f_{}'.format(key)
        if not hasattr(self, attr_name):
            return None
        else:
            return getattr(self, attr_name)
            return None

    def _get_at_aim_all_args(self):
        return self.get_client_dict()

    def _get_pcnt_y(self):
        return self._f_aim_y

    def _get_pcnt_x(self):
        return self._f_aim_x

    def change_at_aim_args(self, f_aim_x, f_aim_y, f_aim_r):
        self.set_at_aim_args_all(f_aim_x, f_aim_y, f_aim_r)
        self.sync()

    def sync(self):
        if G_IS_CLIENT:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'change_at_aim_args', (self._f_aim_x, self._f_aim_y, self._f_aim_r), False, True, False)

    def set_at_aim_args_all(self, f_aim_x, f_aim_y, f_aim_r):
        if f_aim_x == self._f_aim_x and f_aim_y == self._f_aim_y and f_aim_r == self._f_aim_r:
            return
        self._f_aim_x = f_aim_x
        self._f_aim_y = f_aim_y
        self._f_aim_r = f_aim_r
        self.send_event('E_ON_AT_AIM_ARGS_CHANGED')

    def _restore_buff_mod_aim(self, buff_id):
        self._on_buff_mod_aim(0, 0, dis=0, buff_id=buff_id)

    def _on_buff_mod_aim(self, yaw, pitch, dis=0, buff_id=0):
        key = self.KEY_PREFIX_BUFF + str(buff_id)
        self._change_at_aim_map(key, pitch, yaw, dis)

    def _on_armor_data_change(self, i_pos, obj_armor):
        f_pcnt_pitch = obj_armor.get_fEffPitch() if obj_armor else 0
        f_pcnt_yaw = obj_armor.get_fEffYaw() if obj_armor else 0
        f_pcnt_dis = obj_armor.get_fEffDistance() if obj_armor else 0
        key = self.KEY_PREFIX_ARMOR + str(i_pos)
        self._change_at_aim_map(key, f_pcnt_pitch, f_pcnt_yaw, f_pcnt_dis)

    def _change_at_aim_map(self, key, f_pcnt_pitch, f_pcnt_yaw, f_pcnt_dis):
        if not f_pcnt_pitch and not f_pcnt_yaw and not f_pcnt_dis:
            if key in self._mp_ad_aim:
                self._mp_ad_aim.pop(key)
                self._refresh_at_aim_addition()
            return
        self._mp_ad_aim[key] = (f_pcnt_pitch, f_pcnt_yaw, f_pcnt_dis)
        self._refresh_at_aim_addition()

    def _refresh_at_aim_addition(self):
        _f_ad_aim_y = 0
        _f_ad_aim_x = 0
        _f_ad_aim_r = 0
        for k, v in six.iteritems(self._mp_ad_aim):
            f_pcnt_pitch, f_pcnt_yaw, f_pcnt_dis = v
            _f_ad_aim_y += f_pcnt_pitch
            _f_ad_aim_x += f_pcnt_yaw
            _f_ad_aim_r += f_pcnt_dis

        self._f_aim_x = 1.0 + _f_ad_aim_x
        self._f_aim_y = 1.0 + _f_ad_aim_y
        self._f_aim_r = 1.0 + _f_ad_aim_r
        self.sync()