# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAICollectLogMecha.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.common_utils import status_utils
from logic.gcommon.cdata.mecha_status_config import MC_DASH, MC_FLIGHT_BOOST, MC_CAST_SKILL

class ComAICollectLogMecha(UnitCom):
    BIND_EVENT = {'E_FIRE': '_on_fire',
       'E_DO_SKILL': '_do_skill'
       }

    def __init__(self):
        super(ComAICollectLogMecha, self).__init__()
        self.is_open_aicollectlog = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComAICollectLogMecha, self).init_from_dict(unit_obj, bdict)
        if global_data.battle and getattr(global_data.battle, 'is_open_aicollectlog', False):
            self.is_open_aicollectlog = True

    def _on_fire(self, *arg, **kwargs):
        if not self.is_open_aicollectlog:
            return
        if global_data.player and global_data.player.logic:
            is_sub_fire = False
            if arg and len(arg) >= 2:
                weapon_pos = arg[1]
                mecha_id = self.ev_g_mecha_id()
                mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id))
                weapon_conf = confmgr.get('mecha_conf', 'WeaponPosConf', 'Content', str(mecha_id))
                gun_list = mecha_conf.get('guns', [])
                if 0 < weapon_pos <= len(gun_list):
                    gun_id = gun_list[weapon_pos - 1]
                    if gun_id in weapon_conf.get('second_weapon', []):
                        is_sub_fire = True
            if is_sub_fire:
                global_data.player.logic.send_event('E_RECORD_SUB_FIRE')
            else:
                global_data.player.logic.send_event('E_RECORD_FIRE')

    def _do_skill(self, skill_id, *args):
        if not self.is_open_aicollectlog:
            return
        if global_data.player and global_data.player.logic:
            mecha_id = self.ev_g_mecha_id()
            if mecha_id:
                weapon_conf = confmgr.get('mecha_conf', 'WeaponPosConf', 'Content', str(mecha_id))
                data = status_utils.get_behavior_config(str(mecha_id))
                behavior_info = data.get_behavior(str(mecha_id))
                if skill_id in weapon_conf.get('second_weapon', []):
                    global_data.player.logic.send_event('E_RECORD_SUB_FIRE')