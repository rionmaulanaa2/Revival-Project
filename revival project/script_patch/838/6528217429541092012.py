# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_item/ComPickableSimUI.py
from __future__ import absolute_import
import math3d
import world
import render
import math
from logic.gcommon.component.UnitCom import UnitCom
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.uisys.font_utils import GetMultiLangFontFaceName
from logic.gcommon import time_utility
from logic.gutils import item_utils
import weakref
from logic.manager_agents.manager_decorators import sync_exec

class ComPickableSimUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_REFRESH_ITEM_CD': 'on_refresh_item_cd',
       'G_IS_TEAMMATE_ITEM': '_is_teammate'
       }

    def __init__(self):
        super(ComPickableSimUI, self).__init__()
        self._simui = None
        self._forbidden_simui = None
        self._recede_simui = None
        self._cd = None
        self._cd_bg = None
        self._cd_txt = None
        self._forbidden_bg = None
        self._recede_txt = None
        self._cd_show_timer = None
        self._cur_cd = 0
        self._max_cd = 0
        self._model_ref = None
        self._item_id = None
        self._recede_rate = 0
        self.process_event(True)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPickableSimUI, self).init_from_dict(unit_obj, bdict)
        self._item_id = bdict.get('item_id')
        self._faction_id = bdict.get('faction_id')
        self.spawn_id = bdict.get('spawn_id')
        born_spawn_data = global_data.game_mode.get_cfg_data('born_spawn_data') or {}
        self.born_idx = born_spawn_data.get(str(self.spawn_id), {}).get('born_idx', -1)

    def get_player_group_id(self):
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_group_id()

    def _is_teammate(self):
        if not self._faction_id:
            return True
        return self.get_player_group_id() == self._faction_id

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_switch_player_setted_event': self.on_camera_player_setted,
           'update_spawn_recede': self.update_spawn_recede
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def cache(self):
        self._clear_ui()
        self._model_ref = None
        super(ComPickableSimUI, self).cache()
        return

    def get_simui_fill_z(self):
        return True

    def on_model_loaded(self, model):
        self._model_ref = weakref.ref(model)
        self.refresh_simui()

    def refresh_simui(self):
        if self._is_teammate():
            self._clear_forbidden_mark()
            self.on_refresh_item_cd()
            if self.born_idx != -1:
                self.on_refresh_recede()
        else:
            self._clear_cd_ui()
            self._clear_recede_ui()
            if item_utils.is_dogtag_by_item_id(self._item_id):
                return
            self.on_refresh_item_forbidden()

    def on_camera_player_setted(self, *args):
        self.refresh_simui()

    def get_model(self):
        if self._model_ref:
            return self._model_ref()
        else:
            return None

    def on_refresh_item_forbidden(self):
        if not (global_data.cam_lplayer and self.get_model()):
            return
        if self._item_id:
            model = self.get_model()
            self._create_forbidden_ui(model)

    def on_refresh_item_cd(self):
        if not (global_data.cam_lplayer and self.get_model()):
            return
        if not self._is_teammate():
            return
        if self._item_id:
            import logic.gcommon.common_utils.item_config as item_conf
            conf = item_conf.get_use_by_id(str(self._item_id))
            if not conf:
                return
            has_cd = bool(conf.get('fUseCD'))
            if has_cd:
                end_time = global_data.cam_lplayer.ev_g_use_item_cd(self._item_id)
                end_time and self._on_show_item_cd(end_time)

    def on_refresh_recede(self):
        if not global_data.death_battle_data:
            return
        if not (global_data.cam_lplayer and self.get_model()):
            return
        if not self._is_teammate():
            return
        if self._item_id:
            model = self.get_model()
            self._create_recede_ui(model)
            _recede_rate = global_data.death_battle_data.get_spawn_recede_rate()
            self.update_spawn_recede(_recede_rate)

    def update_spawn_recede(self, recede_rate):
        self._recede_rate = recede_rate
        if self._recede_simui and self._recede_simui.valid:
            self.check_update()
            if self._recede_txt:
                self._recede_simui.set_text(self._recede_txt, ''.join(['\xe2\x96\xbc', str(recede_rate), '%']))

    def on_hide_sim_ui(self):
        self._simui.visible = False
        self._forbidden_simui.visible = False
        self._recede_simui.visible = False

    def tick(self, delta):
        if not (self._forbidden_simui or self._simui or self._recede_simui):
            return
        self.refresh_simui_scale()

    def refresh_simui_scale(self):
        if self.scene and self.scene.active_camera:
            model = self.get_model()
            if model:
                pos = model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                if self._simui and self._simui.valid:
                    max_dist = 200
                    scale = max(0.1, (max_dist - dist) * 1.0 / max_dist)
                    self._simui.scale = (scale, scale)
                if self._forbidden_simui and self._forbidden_simui.valid:
                    max_dist = 100
                    scale = max(0.2, (max_dist - dist) * 1.0 / max_dist)
                    self._forbidden_simui.scale = (scale * 0.8, scale * 0.8)
                if self._recede_simui and self._recede_simui.valid:
                    max_dist = 100
                    if self._recede_txt and dist > 75:
                        alpha = max(0, (max_dist - dist) * 1.0 / 25)
                        color = (int(255 * alpha), 255, 255, 0)
                        self._recede_simui.set_ui_color(self._recede_txt, color)

    def _on_show_item_cd(self, end_time):
        left_time = end_time - time_utility.time()
        if left_time <= 0:
            if self._simui and self._simui.valid:
                self._simui.visible = False
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
                            self.check_update()
                        self._cur_cd -= 1
                        return

                cb()
                self._cd_show_timer = global_data.game_mgr.get_logic_timer().register(func=cb, interval=1, times=-1, mode=CLOCK)

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

        if model.has_socket('jinzhi'):
            model.bind('jinzhi', self._forbidden_simui)
        else:
            self._forbidden_simui.set_parent(model)
            simui_pos = self.get_simui_pos()
            if not simui_pos:
                box = model.bounding_box
                scale_y = model.scale.y
                self._forbidden_simui.position = math3d.vector(0, box.y * 2 * scale_y + 10, 0)
            else:
                self._forbidden_simui.position = simui_pos
        self._forbidden_simui.inherit_flag = world.INHERIT_TRANSLATION
        self._forbidden_simui.visible = True
        self.refresh_simui_scale()
        self.check_update()

    def refresh_recede_visible(self):
        show_recede_simui = True
        if self._simui and self._simui.valid and self._simui.visible:
            show_recede_simui = False
        if self._forbidden_simui and self._forbidden_simui.valid and self._forbidden_simui.visible:
            show_recede_simui = False
        if self._recede_simui and self._recede_simui.valid:
            self._recede_simui.visible = show_recede_simui and bool(self._recede_rate) and self.born_idx != -1

    def check_update(self):
        self.refresh_recede_visible()
        need_update = False
        if self._simui and self._simui.valid and self._simui.visible:
            need_update = True
        if self._forbidden_simui and self._forbidden_simui.valid and self._forbidden_simui.visible:
            need_update = True
        if self._recede_simui and self._recede_simui.valid and self._recede_simui.visible:
            need_update = True
        self.need_update = need_update
        self.unit_obj.get_owner().set_dynamic(need_update)

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

    def _create_recede_ui(self, model):
        if not model:
            return
        if self._recede_simui:
            return
        self.scene.simui_enable_post_process(True)
        self._recede_simui = world.simuiobject(render.texture(''))
        render.create_font('cd_txt', GetMultiLangFontFaceName('FZLanTingHei-R-GBK'), 18, True)
        self._recede_txt = self._recede_simui.add_text_ui('0', 'cd_txt', 0, -10)
        self._recede_simui.set_ui_align(self._recede_txt, 0.5, 0.5)
        self._recede_simui.set_ui_fill_z(self._recede_txt, self.get_simui_fill_z())
        color = (255, 255, 255, 0)
        self._recede_simui.set_ui_color(self._recede_txt, color)
        self._recede_simui.set_parent(model)
        self._recede_simui.inherit_flag = world.INHERIT_TRANSLATION
        simui_pos = self.get_simui_pos()
        if not simui_pos:
            box = model.bounding_box
            scale_y = model.scale.y
            self._recede_simui.position = math3d.vector(0, box.y * 2 * scale_y + 10, 0)
        else:
            self._recede_simui.position = simui_pos
        self._recede_simui.visible = False

    def get_simui_pos(self):
        pass

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

    def _clear_recede_ui(self):
        if self._recede_simui and self._recede_simui.valid:
            try:
                self._recede_simui.destroy()
            except:
                pass

        self._recede_simui = None
        return

    def _clear_forbidden_mark(self):
        if self._forbidden_simui and self._forbidden_simui.valid:
            try:
                self._forbidden_simui.destroy()
            except:
                pass

        self._forbidden_simui = None
        return

    def _clear_ui(self):
        self._clear_cd_ui()
        self._clear_forbidden_mark()
        self._clear_recede_ui()

    def destroy(self):
        self.process_event(False)
        self._clear_ui()
        super(ComPickableSimUI, self).destroy()