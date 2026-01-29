# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_portal/ComSimplePortalAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.battle_const import PORTAL_TYPE_DEATH, PORTAL_TYPE_PVE, PORTAL_TYPE_PVE_BOSS
import world
import render
from common.uisys.font_utils import GetMultiLangFontFaceName
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr

class ComSimplePortalAppearance(UnitCom):
    BIND_EVENT = {'G_CAMP_ID': '_get_camp_id',
       'G_PORTAL_TYPE': '_get_type'
       }
    HIGHT_OFFSET = 0.05
    SFX_PATH = {PORTAL_TYPE_DEATH: [
                         'effect/fx/scenes/common/sidou/sd_chuansongmen_up_blue.sfx',
                         'effect/fx/scenes/common/sidou/sd_chuansongmen_down_blue.sfx'],
       PORTAL_TYPE_PVE: [
                       'effect/fx/scenes/common/pve/pve_chuansongmen.sfx'],
       PORTAL_TYPE_PVE_BOSS: [
                            'effect/fx/scenes/common/pve/pve_chuansongmen_cheng.sfx']
       }
    SOUND_MAP = {PORTAL_TYPE_DEATH: 'portal1_loop',
       PORTAL_TYPE_PVE: 'portal2_loop',
       PORTAL_TYPE_PVE_BOSS: 'portal2_loop'
       }
    EMPTY_MODEL_PATH = confmgr.get('script_gim_ref')['empty_item_model']

    def __init__(self):
        super(ComSimplePortalAppearance, self).__init__()
        self.sfx_id_list = []
        self.sound_id = None
        self.empty_model = None
        self._simui = None
        self._cd = None
        self._cd_bg = None
        self._cd_txt = None
        self._cd_show_timer = None
        self._cur_cd = None
        self._max_cd = None
        self._type = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSimplePortalAppearance, self).init_from_dict(unit_obj, bdict)
        self.init_params(bdict)
        self.init_sfx()
        self.create_sfx_sound()
        self.init_col()
        self.init_empty_model()

    def init_params(self, bdict):
        self._pos = math3d.vector(*bdict.get('position')) + math3d.vector(0, self.HIGHT_OFFSET * NEOX_UNIT_SCALE, 0)
        self._type = bdict.get('portal_type', PORTAL_TYPE_DEATH)
        self.faction_id = bdict.get('faction_id', 0)

    def _get_type(self):
        return self._type

    def init_sfx(self):
        if not self.sfx_id_list:
            src_paths = self.SFX_PATH.get(self._type, [])
            for src_path in src_paths:
                sfx = world.sfx(src_path, scene=self.scene)
                sfx.world_position = self._pos
                self.sfx_id_list.append(sfx)

    def create_sfx_sound(self):
        if not self.sound_id:
            sound_map = self.SOUND_MAP.get(self._type)
            self.sound_id = global_data.sound_mgr.play_sound('Play_ui_notice', self._pos, ('ui_notice', sound_map))

    def init_col(self):
        self.send_event('E_ON_SIMPLE_PORTAL_SFX_LOADED', self._pos)

    def init_empty_model(self):

        def call_back(model):
            self.empty_model = model

        global_data.model_mgr.create_model_in_scene(self.EMPTY_MODEL_PATH, self._pos, on_create_func=call_back)

    def destroy(self):
        if self.sfx_id_list:
            for sfx_id in self.sfx_id_list:
                sfx_id.destroy()

            self.sfx_id_list = []
        if self.sound_id:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        if self._cd_show_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._cd_show_timer)
            self._cd_show_timer = None
        if self._simui and self._simui.valid:
            try:
                self._simui.destroy()
            except:
                pass

            self._simui = None
        if self.empty_model:
            global_data.model_mgr.remove_model(self.empty_model)
            self.empty_model = None
        super(ComSimplePortalAppearance, self).destroy()
        return

    def cache(self):
        if self.sfx_id_list:
            for sfx_id in self.sfx_id_list:
                sfx_id.destroy()

            self.sfx_id_list = []
        if self.sound_id:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        if self._cd_show_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._cd_show_timer)
            self._cd_show_timer = None
        if self._simui and self._simui.valid:
            try:
                self._simui.destroy()
            except:
                pass

            self._simui = None
        if self.empty_model:
            global_data.model_mgr.remove_model(self.empty_model)
            self.empty_model = None
        super(ComSimplePortalAppearance, self).cache()
        return

    def _get_camp_id(self):
        return self.faction_id