# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_granbelm/ComGranbelmPortalAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.battle_const import GRANBELM_PORTAL_FIRST_TELEPORT, GRANBELM_PORTAL_SECOND_TELEPORT, GRANBELM_PORTAL_TYPE_POISON, GRANBELM_PORTAL_TYPE_PARADROP
import world
import render
from common.uisys.font_utils import GetMultiLangFontFaceName
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr

class ComGranbelmPortalAppearance(UnitCom):
    BIND_EVENT = {'E_UPDATE_DISAPPEAR_TIMESTAMP': '_update_portal_timer'
       }
    HIGHT_OFFSET = 0.5
    SFX_PATH = {0: {GRANBELM_PORTAL_TYPE_POISON: 'effect/fx/scenes/common/manyue/chuansong_red.sfx',
           GRANBELM_PORTAL_TYPE_PARADROP: 'effect/fx/scenes/common/manyue/chuansong_blue.sfx'
           },
       1: {GRANBELM_PORTAL_TYPE_POISON: 'effect/fx/scenes/common/dianziping/dianziping_red.sfx',
           GRANBELM_PORTAL_TYPE_PARADROP: 'effect/fx/scenes/common/dianziping/dianziping_blue.sfx'
           }
       }
    SOUND_MAP = {GRANBELM_PORTAL_TYPE_POISON: 'portal1_loop',
       GRANBELM_PORTAL_TYPE_PARADROP: 'portal2_loop'
       }
    EMPTY_MODEL_PATH = confmgr.get('script_gim_ref')['empty_item_model']

    def __init__(self):
        super(ComGranbelmPortalAppearance, self).__init__()
        self.sfx_id = None
        self.sound_id = None
        self.empty_model = None
        self._simui = None
        self._cd = None
        self._cd_bg = None
        self._cd_txt = None
        self._cd_show_timer = None
        self._cur_cd = None
        self._max_cd = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComGranbelmPortalAppearance, self).init_from_dict(unit_obj, bdict)
        self.init_params(bdict)
        self.init_sfx()
        self.create_sfx_sound()
        self.init_col()
        self.init_empty_model()
        timestamp = bdict.get('disappear_timestamp', None)
        if timestamp:
            self._update_portal_timer(timestamp)
        return

    def init_params(self, bdict):
        self._pos = math3d.vector(*bdict.get('position')) + math3d.vector(0, self.HIGHT_OFFSET * NEOX_UNIT_SCALE, 0)
        self._type = bdict.get('portal_type', GRANBELM_PORTAL_TYPE_POISON)

    def init_sfx(self):
        if not self.sfx_id:
            if not global_data.gran_sur_battle_mgr.is_sub_mode:
                src_path = self.SFX_PATH[0].get(self._type)
            else:
                src_path = self.SFX_PATH[1].get(self._type)
            self.sfx_id = global_data.sfx_mgr.create_sfx_in_scene(src_path, self._pos)

    def create_sfx_sound(self):
        if not self.sound_id:
            sound_map = self.SOUND_MAP.get(self._type)
            self.sound_id = global_data.sound_mgr.play_sound('Play_ui_notice', self._pos, ('ui_notice', sound_map))

    def init_col(self):
        self.send_event('E_ON_PORTAL_SFX_LOADED', self._pos)

    def init_empty_model(self):

        def call_back(model):
            self.empty_model = model

        global_data.model_mgr.create_model_in_scene(self.EMPTY_MODEL_PATH, self._pos, on_create_func=call_back)

    def _update_portal_timer(self, timestamp):
        if not timestamp:
            return
        left_time = timestamp - time_utility.get_server_time()
        if left_time < 0:
            return
        self._cur_cd = left_time
        self._max_cd = left_time
        self.init_cd_simui()
        if self._simui and self._simui.valid:
            self._simui.visible = True
            self.check_update()
            if not self._cd_show_timer:

                def call_back(*args):
                    if not self or not self.is_enable():
                        return
                    else:
                        self._simui.set_imageui_horpercent(self._cd, 0.0, self._cur_cd * 1.0 / self._max_cd)
                        self._simui.set_text(self._cd_txt, ''.join([str(int(math.ceil(self._cur_cd))), 's']))
                        if self._cur_cd <= 0:
                            global_data.game_mgr.get_logic_timer().unregister(self._cd_show_timer)
                            self._cd_show_timer = None
                            self._simui.visible = False
                            self.check_update()
                        self._cur_cd -= 1
                        return

                call_back()
                self._cd_show_timer = global_data.game_mgr.get_logic_timer().register(func=call_back, interval=1, times=-1, mode=CLOCK)

    def init_cd_simui(self):
        if not self.empty_model:
            return
        if self._simui:
            return
        self.scene.simui_enable_post_process(True)
        self._simui = world.simuiobject(render.texture('gui/ui_res_2/simui/sim_item_loading.png'))
        self._cd = self._simui.add_image_ui(0, 14, 80, 14, 0, 0)
        self._cd_bg = self._simui.add_image_ui(0, 0, 80, 14, 0, 0)
        render.create_font('cd_txt', GetMultiLangFontFaceName('FZLanTingHei-R-GBK'), 18, True)
        self._cd_txt = self._simui.add_text_ui('0', 'cd_txt', 0, -19)
        for _id in [self._cd, self._cd_bg, self._cd_txt]:
            self._simui.set_ui_align(_id, 0.5, 0.5)
            self._simui.set_ui_fill_z(_id, True)

        self._simui.set_parent(self.empty_model)
        self._simui.inherit_flag = world.INHERIT_TRANSLATION
        self._simui.position = math3d.vector(0, NEOX_UNIT_SCALE * 1.0, 0)
        self._simui.visible = False

    def check_update(self):
        if self._simui and self._simui.valid and self._simui.visible:
            self.need_update = True
        else:
            self.need_update = False

    def tick(self, delta):
        if self.scene and self.scene.active_camera:
            if self.empty_model:
                pos = self.empty_model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                if self._simui:
                    max_dist = 200
                    scale = max(0.05, (max_dist - dist) * 0.5 / max_dist)
                    self._simui.scale = (scale, scale)

    def destroy(self):
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
            self.sfx_id = None
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
        super(ComGranbelmPortalAppearance, self).destroy()
        return