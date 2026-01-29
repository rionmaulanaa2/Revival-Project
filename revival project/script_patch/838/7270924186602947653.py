# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/skill_proto.py


def add_skill(synchronizer, skill_id, skill_data):
    synchronizer.send_event('E_ADD_SKILL', skill_id, skill_data)


def remote_do_skill(synchronizer, skill_id, skill_args=None):
    if skill_args is None:
        skill_args = ()
    synchronizer.send_event('E_REMOTE_DO_SKILL', skill_id, skill_args)
    return


def update_skill(synchronizer, skill_id, skill_data):
    synchronizer.send_event('E_UPDATE_SKILL', skill_id, skill_data)


def mod_skill(synchronizer, skill_id, skill_data):
    synchronizer.send_event('E_MOD_SKILL', skill_id, skill_data)


def skill_mp_change(synchronizer, skill_id, cur_mp):
    synchronizer.send_event('E_SKILL_MP_CHANGE', skill_id, cur_mp)


def skill_add_mp(synchronizer, skill_id, add_mp):
    synchronizer.send_event('E_SKILL_ADD_MP', skill_id, add_mp)


def remove_skill(synchronizer, skill_id):
    synchronizer.send_event('E_REMOVE_SKILL', skill_id)


def sync_do_skill(synchronizer, target_ids, start_pos, skill_id):
    synchronizer.send_event('E_SYNC_DO_SKILL', target_ids, start_pos, skill_id)


def begin_recover_mp(synchronizer, skill_id, skill_args=()):
    synchronizer.send_event('E_BEGIN_RECOVER_MP', skill_id, skill_args)


def mod_left_cast_cnt(synchronizer, skill_id, delta_cnt):
    synchronizer.send_event('E_MOD_SKILL_LEFT_CNT', skill_id, delta_cnt)


def set_left_cast_cnt(synchronizer, skill_id, cnt):
    synchronizer.send_event('E_SET_SKILL_LEFT_CNT', skill_id, cnt)


def disable_skill_by_module_card(synchronizer, skill_id, card_id):
    synchronizer.send_event('E_DISABLE_BY_MODULE_CARD', skill_id, card_id)


def enable_skill_by_module_card(synchronizer, skill_id, card_id, client_dict):
    synchronizer.send_event('E_ENABLE_BY_MODULE_CARD', skill_id, card_id, client_dict)


def sync_skill_fuel(synchronizer, skill_id, new_fuel):
    synchronizer.send_event('E_SYNC_SKILL_FUEL_CHANGE', skill_id, new_fuel)