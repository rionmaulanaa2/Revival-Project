# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEMonsterData.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.common_const.pve_const import M_BOSS

class ComPVEMonsterData(UnitCom):
    BIND_EVENT = {'G_MONSTER_NAME': 'get_monster_name',
       'G_NEED_POS_CHECK': 'need_pos_check',
       'G_MOVE_RATIO': 'get_move_ratio'
       }

    def __init__(self):
        super(ComPVEMonsterData, self).__init__()
        self.sd.ref_monster_id = None
        self.sd.ref_monster_type = 1
        self.sd.ref_bias_dur = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEMonsterData, self).init_from_dict(unit_obj, bdict)
        self.monster_id = bdict.get('npc_id', None)
        self.sd.ref_monster_id = self.monster_id
        self.conf = confmgr.get('monster_data', 'Monster', 'Content', str(self.monster_id))
        self.monster_level = bdict.get('pve_monster_level', None)
        self.level_conf = {}
        if self.monster_level:
            self.level_conf = confmgr.get('monster_level_data', str(self.monster_id), 'Content', str(self.monster_level))
        self.monster_name = self.get_level_config_value('NameText')
        self.monster_type = self.conf.get('MType', 1)
        self.sd.ref_monster_type = self.monster_type
        if self.monster_type == M_BOSS:
            global_data.emgr.pve_boss_init.emit(self.unit_obj.id)
            global_data.battle and global_data.battle.set_pve_boss_eid(self.unit_obj.id)
            self.is_boss = True
        else:
            self.is_boss = False
        self.pos_check = not self.conf.get('forbid_poscheck', False)
        self.bias_dur = self.get_level_config_value('Fire_Bias_Dur', 0)
        self.sd.ref_bias_dur = self.bias_dur
        self.move_ratio = self.get_level_config_value('Move_Ratio', None)
        return

    def get_level_config_value(self, key, default=None):
        if self.level_conf:
            ret = self.level_conf.get(key, default)
            if ret:
                return ret
        return self.conf.get(key, default)

    def get_monster_name(self):
        return self.monster_name

    def need_pos_check(self):
        return self.pos_check

    def get_move_ratio(self):
        return self.move_ratio

    def destroy(self):
        if self.monster_type == M_BOSS:
            global_data.emgr.pve_boss_destroy.emit(self.unit_obj.id)
        super(ComPVEMonsterData, self).destroy()