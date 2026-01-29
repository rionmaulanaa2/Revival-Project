# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComShockFieldAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils.judge_utils import get_player_group_id
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
SELF_SFX = 'effect/fx/mecha/8033/8033_chuansong_blue.sfx'
ENEMY_SFX = 'effect/fx/mecha/8033/8033_chuansong_red.sfx'
SFX_RADIUS = 25 * NEOX_UNIT_SCALE
WARNING_SOUND_NAME = 'm_8033_bombing_warning_3p'

class ComShockFieldAppearance(UnitCom):

    def __init__(self):
        super(ComShockFieldAppearance, self).__init__()
        self.faction_id = None
        self.sfx_id = None
        self.position = None
        self.shock_range = 0
        self.warning_sound_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComShockFieldAppearance, self).init_from_dict(unit_obj, bdict)
        self.faction_id = bdict.get('faction_id')
        self.position = bdict.get('position')
        self.position = math3d.vector(*self.position)
        self.shock_range = bdict.get('shock_range')
        self.init_sfx()

    def init_sfx(self):
        if self.sfx_id:
            return
        if get_player_group_id() == self.faction_id:
            self.create_shock_sfx(SELF_SFX)
        else:
            self.create_shock_sfx(ENEMY_SFX)

    def create_shock_sfx(self, sfx_path):
        x_scale = self.shock_range / SFX_RADIUS
        z_scale = x_scale
        sfx_scale = math3d.vector(x_scale, 1, z_scale)

        def create_cb(sfx, sfx_scale=sfx_scale):
            sfx.scale = sfx_scale
            self.warning_sound_id = global_data.sound_mgr.play_sound(WARNING_SOUND_NAME, sfx.position)

        self.sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self.position, on_create_func=create_cb)

    def destroy(self):
        super(ComShockFieldAppearance, self).destroy()
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
        if self.warning_sound_id:
            global_data.sound_mgr.stop_playing_id(self.warning_sound_id)
            self.warning_sound_id = None
        return