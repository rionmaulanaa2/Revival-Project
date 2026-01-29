# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/weapon_proto.py


def weapon_bullet_change(synchronizer, weapon_pos, cur_bullet_cnt):
    synchronizer.send_event('E_WEAPON_BULLET_CHG', weapon_pos, cur_bullet_cnt)


def weapon_bullet_max_change(synchronizer, weapon_pos, cur_bullet_cnt):
    synchronizer.send_event('E_WEAPON_BULLET_MAX_CHG', weapon_pos, cur_bullet_cnt)


def switch_weapon(synchronizer, pos1, pos2):
    synchronizer.send_event('E_SWITCH_WEAPON', pos1, pos2)


def switch_weapon_mode(synchronizer, pos, enable):
    synchronizer.send_event('E_SWITCHING_WP_MODE', pos, enable)


def on_wpbar_switch(synchronizer, cur_pos):
    synchronizer.send_event('E_SWITCHING', cur_pos)


def on_set_empty_hand(synchronizer):
    pass


def change_scope_times(synchronizer, scope_id, value):
    synchronizer.send_event('E_CHANGE_SCOPE_TIMES', scope_id, value)


def add_heat_magazine(synchronizer, magazine_key, data):
    pass


def reduce_magazine_heat(synchronizer, magazine_key, mod):
    synchronizer.send_event('E_DEC_MAGAZINE_HEAT', magazine_key, mod)