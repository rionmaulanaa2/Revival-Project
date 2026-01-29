# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/pve_proto.py


def play_spot_sfx(synchronizer, ret):
    synchronizer.send_event('E_SPOT_SFX_PLAYER', ret)


def play_spot_sound(synchronizer, ret):
    synchronizer.send_event('E_SPOT_SOUND_PLAYER', ret)


def install_bless_succ(synchronizer, bless_id, add_level):
    synchronizer.send_event('E_CHOOSE_BLESS', bless_id, add_level)


def remove_bless_succ(synchronizer, bless_id):
    synchronizer.send_event('E_REMOVE_BLESS', bless_id)


def random_install_bless_succ(synchronizer, bless_id, add_level):
    synchronizer.send_event('E_RANDOM_CHOOSE_BLESS', bless_id, add_level)


def pve_box_state_change(synchronizer, state):
    synchronizer.send_event('E_SET_BOX_STATE', state)


def pve_shop_state_change(synchronizer, state):
    synchronizer.send_event('E_SET_SHOP_STATE', state)


def pve_mecha_breakthrough_state_change(synchronizer, state):
    synchronizer.send_event('E_SET_MECHA_BREAKTHROUGH_STATE', state)


def on_crystal_stone_update(synchronizer, bag_num, add):
    synchronizer.send_event('E_ON_CRYSTAL_STONE_UPDATE', bag_num, add)


def on_cost_crystal_stone(synchronizer, bag_num):
    synchronizer.send_event('E_ON_COST_CRYSTAL_STONE', bag_num)


def on_crystal_stone_update_debt_limit(synchronizer, debt_limit):
    synchronizer.send_event('E_CRYSTAL_STONE_DEBT_LIMIT', debt_limit)


def on_update_pve_coin(synchronizer, bag_num):
    synchronizer.send_event('E_ON_UPDATE_PVE_COIN', bag_num)


def on_pve_ice_update(synchronizer, ice_cnt):
    synchronizer.send_event('E_ON_UPDATE_PVE_ICE', ice_cnt)


def pve_start_read_dialog(synchronizer, dialog_data):
    global_data.emgr.pve_start_read_dialog_event.emit(synchronizer, dialog_data)


def pve_stop_read_dialog(synchronizer):
    global_data.emgr.pve_stop_read_dialog_event.emit(synchronizer)


def update_pve_item_set(synchronizer, item_set):
    synchronizer.send_event('E_UPDATE_PVE_ITEM_SET', item_set)


def pve_play_sfx_on_model(synchronizer, sfx_path, scale=1.0, rate=1.0):
    model = synchronizer.ev_g_model()
    if model and model.valid:
        global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, 'fx_buff')


def show_effect_entry(synchronizer, effect_type, effect_id, start_time, end_time):
    synchronizer.send_event('E_SHOW_EFFECT_ENTRY', effect_type, effect_id, start_time, end_time)


def clear_effect_entry(synchronizer, effect_type, effect_id):
    synchronizer.send_event('E_CLEAR_EFFECT_ENTRY', effect_type, effect_id)


def pve_notify_donate_bless_info(synchronizer, donate_id, donate_info):
    print (
     'pve_notify_donate_bless_info', donate_id, donate_info)
    teammate_infos = synchronizer.ev_g_teammate_infos()
    if not teammate_infos:
        return
    donator_id = donate_info['donator']
    teammate_info = teammate_infos.get(donator_id)
    if not teammate_info:
        return
    char_name = teammate_info.get('char_name', '')
    donate_info['char_name'] = char_name
    donate_info['donate_id'] = donate_id
    donate_info['donator_id'] = donator_id
    global_data.emgr.on_pve_notify_donate_bless_info.emit(donate_info)


def pve_notify_donate_bless_result(synchronizer, donate_id, donate_info, accepted):
    print (
     'pve_notify_donate_bless_result', donate_id, accepted)
    teammate_infos = synchronizer.ev_g_teammate_infos()
    if not teammate_infos:
        return
    teammate_info = teammate_infos.get(donate_info['acceptor'])
    if not teammate_info:
        return
    char_name = teammate_info.get('char_name', '')
    bless_id = donate_info['bless_id']
    global_data.emgr.on_pve_notify_donate_bless_result.emit(char_name, bless_id, accepted)


def pve_on_use_mecha_reset_item(synchronizer):
    global_data.ui_mgr.show_ui('PVEShopMechaUI', 'logic.comsys.battle.pve')


def pve_notify_reset_mecha(synchronizer, mecha_id):
    global_data.player and global_data.player.set_pve_selected_mecha_id(int(mecha_id))
    global_data.emgr.on_pve_notify_reset_mecha.emit(mecha_id)


def pve_bless_effect(synchronizer, bless_id):
    synchronizer.send_event('E_PVE_BLESS_EFFECT', bless_id)