# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/acc_config.py
_reload_all = True
ACC_RATE = {'1': 2.5,'0': 2.5}
NO_DIR_ACC_RATE = 0.5
DEFAULT_ACC_RATE = 2.5

def get_acc_rate(acc_key):
    if global_data.game_mode and global_data.death_battle_data and global_data.death_battle_data.area_id is not None:
        data = global_data.game_mode.get_born_data()
        if global_data.death_battle_data.area_id in data:
            acc_rate = data[global_data.death_battle_data.area_id].get('acc_rate', {}).get(acc_key, DEFAULT_ACC_RATE)
            if acc_rate is not None:
                return acc_rate
    return ACC_RATE.get(acc_key, DEFAULT_ACC_RATE)