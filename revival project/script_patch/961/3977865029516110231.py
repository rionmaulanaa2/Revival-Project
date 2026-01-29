# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComElasticitySimUI.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
import render
import math
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
from logic.manager_agents.manager_decorators import sync_exec
from common.uisys.font_utils import GetMultiLangFontFaceName
from logic.gcommon.common_const import building_const as b_const
import weakref

class ComElasticitySimUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'G_ELASTICITY_IS_TEAMMATE': '_is_teammate',
       'G_IS_CD': '_is_cd'
       }

    def __init__(self):
        super(ComElasticitySimUI, self).__init__()
        self.player = None
        self._simui = None
        self._forbidden_simui = None
        self._forbidden_bg = None
        self._cd = None
        self._cd_bg = None
        self._cd_txt = None
        self._cd_show_timer = None
        self._cur_cd = 0
        self._max_cd = 0
        self._model_ref = None
        self.process_event(True)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComElasticitySimUI, self).init_from_dict(unit_obj, bdict)
        self._faction_id = bdict.get('faction_id')
        self._building_no = bdict.get('building_no', None)
        return

    def get_player_group_id(self):
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_group_id()

    def _is_teammate(self):
        if not self._faction_id:
            return True
        return self.get_player_group_id() == self._faction_id

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_switch_player_setted_event': self.on_camera_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def cache(self):
        self._clear_ui()
        self._model_ref = None
        super(ComElasticitySimUI, self).cache()
        return

    def _is_cd(self):
        return self._cur_cd > 0

    def get_simui_fill_z(self):
        return True

    def on_model_loaded(self, model):
        self._model_ref = weakref.ref(model)
        self.set_bind_show(True)
        self.on_camera_player_setted()

    def refresh_simui(self):
        if not self._is_teammate():
            self._clear_cd_ui()
            self.on_refresh_item_forbidden()
        else:
            self._clear_forbidden_mark()
            self.on_change_elasticity_use_cd()

    def on_camera_player_setted(self, *args):
        self.refresh_simui()
        self.unregist_player_event()
        if global_data.cam_lplayer:
            target = global_data.cam_lplayer
            self.player = target
            target.regist_event('E_SET_ELASTICITY_USE_CD', self.on_change_elasticity_use_cd, 10)

    def unregist_player_event(self):
        target = self.player
        if target and target.is_valid():
            target.unregist_event('E_SET_ELASTICITY_USE_CD', self.on_change_elasticity_use_cd)
        self.player = None
        return

    def on_change_elasticity_use_cd(self, *args):
        if self._building_no not in b_const.B_TDM_NEUTRAL_BOUNCER_LIST and self._is_teammate():
            use_cd = global_data.cam_lplayer.ev_g_elasticity_use_cd(self.unit_obj.id) if global_data.cam_lplayer else None
            if use_cd:
                self._on_show_item_cd(use_cd)
        return

    def get_model(self):
        if self._model_ref:
            return self._model_ref()
        else:
            return None

    def on_refresh_item_forbidden(self):
        if not (global_data.cam_lplayer and self.get_model()):
            return
        model = self.get_model()
        self._create_forbidden_ui(model)

    def set_bind_show(self, show):
        model = self.get_model()
        if model.has_socket('effect_01'):
            socket_objs = model.get_socket_objects('effect_01')
        else:
            socket_objs = []
        for bind_obj in socket_objs:
            if bind_obj:
                bind_obj.visible = show
                if show:
                    self.send_event('E_DETECT_PLAYER')

    def tick(self, delta):
        if not (self._forbidden_simui or self._simui):
            return
        self.refresh_simui_scale()

    def refresh_simui_scale(self):
        if self.scene and self.scene.active_camera:
            model = self.get_model()
            if model:
                pos = model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                if self._forbidden_simui:
                    max_dist = 100
                    scale = max(0.2, (max_dist - dist) * 1.0 / max_dist)
                    self._forbidden_simui.scale = (scale * 0.8, scale * 0.8)
                if self._simui and self._simui.valid:
                    max_dist = 200
                    scale = max(0.1, (max_dist - dist) * 1.0 / max_dist)
                    self._simui.scale = (scale, scale)

    def _create_forbidden_ui(self, model):
        if not model:
            return
        if self._forbidden_simui:
            return
        self.scene.simui_enable_post_process(True)
        self._forbidden_simui = world.simuiobject(render.texture('gui/ui_res_2/simui/icon_scene_ban.png'))
        self._forbidden_bg = self._forbidden_simui.add_image_ui(0, 0, 64, 64, 0, 0)
        for id in [self._forbidden_bg]:
            self._forbidden_simui.set_ui_align(id, 0.5, 1)
            self._forbidden_simui.set_ui_fill_z(id, self.get_simui_fill_z())

        self._forbidden_simui.set_parent(model)
        self._forbidden_simui.inherit_flag = world.INHERIT_TRANSLATION
        simui_pos = self.get_simui_pos()
        if not simui_pos:
            box = model.bounding_box
            scale_y = model.scale.y
            self._forbidden_simui.position = math3d.vector(0, box.y * 2 * scale_y + 10, 0)
        else:
            self._forbidden_simui.position = simui_pos
        self._forbidden_simui.visible = True
        self.refresh_simui_scale()
        self.check_update()

    def _create_cd_ui(self, model):
        if not model:
            return
        if self._simui:
            return
        self.scene.simui_enable_post_process(True)
        self._simui = world.simuiobject(render.texture('gui/ui_res_2/simui/sim_item_loading.png'))
        self._cd = self._simui.add_image_ui(0, 14, 80, 14, 0, 0)
        self._cd_bg = self._simui.add_image_ui(0, 0, 80, 14, 0, 0)
        render.create_font('cd_txt', GetMultiLangFontFaceName('HYLingXinJ'), 18, True)
        self._cd_txt = self._simui.add_text_ui('0', 'cd_txt', 0, -19)
        for id in [self._cd, self._cd_bg, self._cd_txt]:
            self._simui.set_ui_align(id, 0.5, 0.5)
            self._simui.set_ui_fill_z(id, self.get_simui_fill_z())

        self._simui.set_parent(model)
        self._simui.inherit_flag = world.INHERIT_TRANSLATION
        simui_pos = self.get_simui_pos()
        if not simui_pos:
            box = model.bounding_box
            scale_y = model.scale.y
            self._simui.position = math3d.vector(0, box.y * 2 * scale_y + 10, 0)
        else:
            self._simui.position = simui_pos
        self._simui.visible = False

    def _on_show_item_cd(self, end_time):
        left_time = end_time - time_utility.time()
        if left_time <= 0:
            return
        self._cur_cd = left_time
        self._max_cd = left_time
        model = self.get_model()
        self._create_cd_ui(model)
        if self._simui and self._simui.valid:
            self._simui.visible = True
            self.check_update()
            if not self._cd_show_timer:

                @sync_exec
                def cb(*args):
                    if not self or not self.is_enable():
                        return
                    else:
                        if not (self._simui and self._simui.valid):
                            return
                        self._simui.set_imageui_horpercent(self._cd, 0.0, self._cur_cd * 1.0 / self._max_cd)
                        self._simui.set_text(self._cd_txt, ''.join([str(int(math.ceil(self._cur_cd))), 's']))
                        if self._cur_cd <= 0:
                            global_data.game_mgr.get_logic_timer().unregister(self._cd_show_timer)
                            self._cd_show_timer = None
                            self._simui.visible = False
                            self.set_bind_show(True)
                            self.check_update()
                        self._cur_cd -= 1
                        return

                cb()
                self._cd_show_timer = global_data.game_mgr.get_logic_timer().register(func=cb, interval=1, times=-1, mode=CLOCK)

    def check_update(self):
        need_update = False
        if self._simui and self._simui.valid and self._simui.visible:
            need_update = True
        if self._forbidden_simui and self._forbidden_simui.valid and self._forbidden_simui.visible:
            need_update = True
        self.need_update = need_update
        self.set_bind_show(not need_update)
        self.unit_obj.get_owner().set_dynamic(need_update)

    def get_simui_pos(self):
        pass

    def _clear_ui(self):
        self._clear_cd_ui()
        self._clear_forbidden_mark()

    def _clear_forbidden_mark(self):
        if self._forbidden_simui and self._forbidden_simui.valid:
            try:
                self._forbidden_simui.destroy()
            except:
                pass

            self._forbidden_simui = None
        return

    def _clear_cd_ui(self):
        if self._cd_show_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._cd_show_timer)
            self._cd_show_timer = None
        if self._simui and self._simui.valid:
            try:
                self._simui.destroy()
            except:
                pass

            self._simui = None
        return

    def destroy(self):
        self.process_event(False)
        self.unregist_player_event()
        self._clear_ui()
        super(ComElasticitySimUI, self).destroy()