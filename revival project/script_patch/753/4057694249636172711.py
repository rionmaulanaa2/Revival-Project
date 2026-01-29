# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/buff_proto.py


def add_buff(synchronizer, buff_key, buff_id, buff_idx, data):
    from common.cfg import confmgr
    from mobile.common.EntityManager import EntityManager
    synchronizer.send_event('E_BUFF_ADD_DATA', buff_key, buff_id, buff_idx, data)
    if confmgr.get('c_buff_data', str(buff_id), 'ExtInfo', 'inform_creator', default=False):
        creator_id = data.get('creator_id', None)
        creator = EntityManager.getentity(creator_id)
        if creator and creator.logic:
            creator.logic.send_event('E_BUFF_FROM_ME_TO_TARGET', synchronizer, buff_key, buff_id, buff_idx, data)
    return


def act_buff(synchronizer, buff_key, buff_id, buff_idx, data):
    synchronizer.send_event('E_BUFF_ACT_DATA', buff_key, buff_id, buff_idx, data)


def del_buff(synchronizer, buff_key, buff_id, buff_idx):
    synchronizer.send_event('E_BUFF_DEL_DATA', buff_key, buff_id, buff_idx)


def detector_mark(synchronizer, enemy_list):
    synchronizer.send_event('E_UPDATE_DETECTED_LIST', enemy_list)


def sync_blind(synchronizer, blind_detail):
    synchronizer.send_event('E_SYNC_BLIND', blind_detail)
    ctrl_target = synchronizer.ev_g_control_target()
    if ctrl_target and ctrl_target.logic and ctrl_target.__class__.__name__ == 'Mecha':
        ctrl_target.logic.send_event('E_SYNC_BLIND', blind_detail)


def detector_mark_map(synchronizer, enemy_list):
    synchronizer.send_event('E_UPDATE_DETECTED_MAP_LIST', enemy_list)


def detector_mark_outline(synchronizer, enemy_list):
    synchronizer.send_event('E_UPDATE_DETECTED_OUTLINE_LIST', enemy_list)