# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGoldeneggAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
from logic.gutils.judge_utils import get_player_group_id
from logic.gcommon.common_const.battle_const import ADCRYSTAL_TIP_SEC_STAGE_ATK, ADCRYSTAL_TIP_SEC_STAGE_DEF, MAIN_NODE_COMMON_INFO, ADCRYSTAL_TIP_POS_CHANGE_ATK, ADCRYSTAL_TIP_POS_CHANGE_DEF
from logic.gcommon.common_utils.local_text import get_text_by_id

class ComGoldeneggAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()

    def __init__(self):
        super(ComGoldeneggAppearance, self).__init__()
        self.egg_pos = None
        self.egg_rot = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComGoldeneggAppearance, self).init_from_dict(unit_obj, bdict)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        self.egg_pos = math3d.vector(pos[0], pos[1], pos[2])
        rot = bdict.get('rot', [0, 0, 0, 1])
        rot = [0, 0, 0, 1] if rot is None else rot
        self.egg_rot = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model_path = 'model_new/scene/huodong/qiangjindan/qiangjindan_egg.gim'
        return (
         model_path, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, user_data):
        model.world_position = self.egg_pos
        model.rotation_matrix = self.egg_rot
        from common.cfg import confmgr
        from logic.gcommon.common_const import weapon_const
        scale = confmgr.get('grenade_res_config', str(weapon_const.SNATCHEGG_THROW_ITEM), 'fBulletSfxScale')
        if scale:
            model.scale = math3d.vector(scale, scale, scale)