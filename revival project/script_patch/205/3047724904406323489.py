# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComClusterGrenadeAppearance.py
from __future__ import absolute_import
from .ComGrenadeAppearance import ComGrenadeAppearance
from .ComBaseModelAppearance import ComBaseModelAppearance, RES_TYPE_MODEL, RES_TYPE_SFX
from common.cfg import confmgr
import weakref
import math3d
import world
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path
from logic.gcommon.common_const.weapon_const import WP_RAY_EXPLOSION_WEAPON_LIST
from logic.gutils.trick_bullet_utils import load_trick_bullet, destroy_real_bullet_model
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gcommon.const import HIT_PART_BODY, HIT_PART_TO_SOCKET_INDEX
from logic.gutils import weapon_skin_utils
import random
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils.client_unit_tag_utils import register_unit_tag

class ComClusterGrenadeAppearance(ComGrenadeAppearance):
    BIND_EVENT = ComGrenadeAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW': 'show'
       })

    def on_load_model_complete(self, model, userdata):
        super(ComClusterGrenadeAppearance, self).on_load_model_complete(model, userdata)
        model.visible = False

    def show(self):
        self.model.visible = True

    def _on_pos_changed(self, position):
        super(ComClusterGrenadeAppearance, self)._on_pos_changed(position)