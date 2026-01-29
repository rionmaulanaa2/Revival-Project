# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBaseMarkView.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.client.const import mark_const
from common.utils.timer import CLOCK
import weakref
import math3d
import world
import render
from logic.gcommon.common_const import buff_const as bconst
KOTH_PERSON_FEET_MARK = [
 'effect/fx/scenes/common/biaozhi/rw_ring_blue.sfx',
 'effect/fx/scenes/common/biaozhi/rw_ring_red.sfx',
 'effect/fx/scenes/common/biaozhi/rw_ring_orange.sfx']

class ComBaseMarkView(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_MODEL_DESTROY': '_on_model_destroy',
       'E_FEED_SFX_OFFSET': '_on_feed_sfx_offset',
       'E_SHOW_HIT_MARK': '_on_show_hit_mark',
       'E_SHOW_KILL_MARK': '_on_show_kill_mark',
       'G_IS_CAM_PLAYER': '_is_cam_player',
       'E_SHOW_PERSPECTIVE_MARK': '_on_show_perspective_mark',
       'E_HIDE_PERSPECTIVE_MARK': '_on_hide_perspective_mark',
       'E_NBOMB_SHOW_HEAD_MARK': 'update_nbomb_mark_show',
       'E_NBOMB_CLEAR_MARK': 'clear_nbomb_simui'
       }

    def __init__(self):
        super(ComBaseMarkView, self).__init__()
        self.init_parameters()

    def init_from_dict(self, unit_obj, bdict):
        super(ComBaseMarkView, self).init_from_dict(unit_obj, bdict)
        self.tm = global_data.game_mgr.get_logic_timer()

    def init_parameters(self):
        self.feet_mark_sfx_id = None
        self._feed_mark_sfx = None
        self._mark_simui = None
        self.head_mark_id = None
        self.hit_mark_id = None
        self.occupy_mark_id = None
        self.kill_mark_id = None
        self.show_marks = {}
        self.hit_timer = None
        self.perspective_timer = None
        self._nbomb_simui = None
        self._nbomb_simui_core_icon = None
        self._nbomb_simui_device_icon = None
        return

    def get_emgr_events(self):
        return {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'open_mark_tick_switch': self.on_open_tick_switch,
           'scene_camera_target_setted_event': self.on_camera_player_setted
           }
        econf.update(self.get_emgr_events())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_camera_player_setted(self, *args):
        self.update_nbomb_mark_show()

    def on_open_tick_switch(self, is_open):
        self.need_update = is_open

    def _on_model_loaded(self, model):
        global_data.emgr.battle_afk_invincible_event.emit(self.ev_g_has_buff_by_id(bconst.BUFF_ID_AFK_INVINCIBLE), self.unit_obj.id)

    def _is_cam_player(self, entity_id):
        pass

    def creat_marks(self):
        self.clear_marks()
        self.process_event(True)
        model = self.ev_g_model()
        if model and model.valid:
            self.create_battle_mark_sfx(model)
            self.create_mark_simui(model)
            self.update_nbomb_mark_show()
        self.send_event('E_RESET_CAMP_OUTLINE')

    def get_all_marks_id(self):
        return [
         self.head_mark_id, self.hit_mark_id, self.occupy_mark_id, self.kill_mark_id]

    def tick(self, delta):
        model = self.ev_g_model()
        if model and model.valid:
            pos = model.position
            dist = self.scene.active_camera.position - pos
            dist = dist.length / NEOX_UNIT_SCALE
            max_dist = 150
            scale = max((max_dist - dist) * 1.0 / max_dist, 0.3)
            if self._mark_simui and self._mark_simui.valid:
                self._mark_simui.scale = (
                 scale, scale)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def create_battle_mark_sfx(self, model):
        side = self.get_show_side()
        if side is None:
            return
        else:
            self.create_feed_mark_sfx(model, KOTH_PERSON_FEET_MARK[side])
            return

    def get_show_side(self):
        return self.ev_g_camp_show_side()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def create_mark_simui(self, model):
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id):
            return
        else:
            side = self.get_show_side()
            if side is None:
                return
            self.scene.simui_enable_post_process(True)
            self._mark_simui = world.simuiobject(render.texture('gui/ui_res_2/simui/koth_locate_icon.png'))
            w, h = (48, 42)
            self.head_mark_id = self._mark_simui.add_image_ui(side * w, 0, w, h, 0, 0)
            self.hit_mark_id = self._mark_simui.add_image_ui(side * w, h, w, h, 0, -h)
            self.occupy_mark_id = self._mark_simui.add_image_ui(side * w, 2 * h, w, h, 0, 0)
            self.kill_mark_id = self._mark_simui.add_image_ui(side * w, 3 * h, w, h, 0, -h)
            for id in self.get_all_marks_id():
                self._mark_simui.set_ui_align(id, 0.5, 1.0)
                self._mark_simui.set_ui_fill_z(id, True)
                self._mark_simui.set_imageui_horpercent(id, 0.0, 0.0)

            self._mark_simui.set_parent(model)
            self._mark_simui.inherit_flag = world.INHERIT_TRANSLATION
            self._mark_simui.position = self.get_mark_position()
            self._on_add_mark(mark_const.HEAD_MARK)
            self.need_update = True
            return

    def get_mark_position(self):
        return math3d.vector(0, 25, 0)

    def _on_add_mark(self, mark_type):
        if mark_type not in self.show_marks:
            self.show_marks[mark_type] = 1
            self.cal_show_mark()

    def _on_del_mark(self, mark_type):
        if mark_type in self.show_marks:
            del self.show_marks[mark_type]
            self.cal_show_mark()

    def cal_show_mark(self):
        if not (self._mark_simui and self._mark_simui.valid):
            return
        marks = self.get_all_marks_id()
        for mark_id in marks:
            self._mark_simui.set_imageui_horpercent(mark_id, 0.0, 0.0)

        for i_type in mark_const.UP_MARK_RANK:
            if i_type in self.show_marks:
                self._mark_simui.set_imageui_horpercent(marks[i_type], 0.0, 1.0)
                break

        for i_type in mark_const.DOWN_MARK_RANK:
            if i_type in self.show_marks:
                self._mark_simui.set_imageui_horpercent(marks[i_type], 0.0, 1.0)
                break

    def _on_show_perspective_mark(self, interval=3):
        self.clear_perspective_timer()
        self._perspective_all_marks(True)
        if interval > 0:

            def _cb():
                self.perspective_timer = None
                self._perspective_all_marks(False)
                return

            self.perspective_timer = self.tm.register(func=_cb, interval=interval, times=1, mode=CLOCK)

    def _on_hide_perspective_mark(self):
        self.clear_perspective_timer()
        self._perspective_all_marks(False)

    def clear_perspective_timer(self):
        self.perspective_timer and self.tm.unregister(self.perspective_timer)
        self.perspective_timer = None
        return

    def _perspective_all_marks(self, is_perspective):
        marks = self.get_all_marks_id()
        for mark_id in marks:
            if mark_id:
                self._mark_simui.set_ui_fill_z(mark_id, not is_perspective)

    def _on_show_hit_mark(self):
        self.clear_timer()

        def _cb():
            self._on_del_mark(mark_const.HIT_MARK)

        self._on_add_mark(mark_const.HIT_MARK)
        self.hit_timer = self.tm.register(func=_cb, interval=3, times=1, mode=CLOCK)

    def _on_show_kill_mark(self, show):
        if show:
            self._on_add_mark(mark_const.KILL_MARK)
        else:
            self._on_del_mark(mark_const.KILL_MARK)

    def create_feed_mark_sfx(self, model, sfx_path):
        if self.feet_mark_sfx_id:
            return
        pos = math3d.vector(0, 0.5, 0)

        def on_create_func(sfx):
            if self and self.is_valid():
                sfx.inherit_flag = world.INHERIT_TRANSLATION
                self._feed_mark_sfx = sfx

        self.feet_mark_sfx_id = global_data.sfx_mgr.create_sfx_for_model(sfx_path, model, pos, on_create_func=on_create_func)

    def clear_sfx(self):
        self._feed_mark_sfx = None
        if self.feet_mark_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.feet_mark_sfx_id)
        self.feet_mark_sfx_id = None
        return

    def _on_feed_sfx_offset(self, offset):
        if self._feed_mark_sfx:
            self._feed_mark_sfx.position = math3d.vector(0, 0.5, 0) + offset

    def is_camera_target(self):
        self_player = global_data.player
        is_self_player = self_player and self_player.logic and self_player.logic.id == self.unit_obj.id
        is_mecha = global_data.mecha and global_data.mecha.id == self.unit_obj.id
        is_camera = self.ev_g_is_cam_target()
        return is_self_player or is_mecha or is_camera

    def is_core_own(self):
        _core_soul_ids = global_data.nbomb_battle_data.get_nbomb_core_soul_ids()
        return self.unit_obj.id in _core_soul_ids or self.sd.ref_driver_id in _core_soul_ids

    def is_device_own(self):
        _device_soul_ids = global_data.nbomb_battle_data.get_nbomb_installed_soul_ids()
        return self.unit_obj.id in _device_soul_ids or self.sd.ref_driver_id in _device_soul_ids

    def _create_nbomb_mark_ui(self, model):
        if not self._nbomb_simui or not self._nbomb_simui.valid:
            self._nbomb_simui = world.simuiobject(render.texture('gui/ui_res_2/simui/simui_bomb_mark.png'))
            self._nbomb_simui_core_icon = self._nbomb_simui.add_image_ui(7, 5, 36, 38, 0, 0)
            self._nbomb_simui.set_ui_align(self._nbomb_simui_core_icon, 0.5, 1)
            self._nbomb_simui.set_ui_fill_z(self._nbomb_simui_core_icon, True)
            self._nbomb_simui_device_icon = self._nbomb_simui.add_image_ui(45, 5, 36, 38, 0, 0)
            self._nbomb_simui.set_ui_align(self._nbomb_simui_device_icon, 0.5, 1)
            self._nbomb_simui.set_ui_fill_z(self._nbomb_simui_device_icon, True)
            self._nbomb_simui.set_parent(model)
            self._nbomb_simui.visible = True
            self._nbomb_simui.inherit_flag = world.INHERIT_TRANSLATION
        self._nbomb_simui.position = self.get_mark_position()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_NBOMB_SURVIVAL,))
    def update_nbomb_mark_show(self):
        if self.is_camera_target():
            self.hide_nbomb_simui()
            return
        if not global_data.nbomb_battle_data:
            self.hide_nbomb_simui()
            return
        is_core_show = self.is_core_own()
        is_device_show = self.is_device_own()
        model = self.ev_g_model()
        if not model:
            return
        if (is_core_show or is_device_show) and not self._nbomb_simui:
            self._create_nbomb_mark_ui(model)
        if not (self._nbomb_simui and self._nbomb_simui.valid):
            return
        if is_device_show:
            self._nbomb_simui.set_imageui_horpercent(self._nbomb_simui_core_icon, 0.0, 0.0)
            self._nbomb_simui.set_imageui_horpercent(self._nbomb_simui_device_icon, 0.0, 1.0)
        elif is_core_show:
            self._nbomb_simui.set_imageui_horpercent(self._nbomb_simui_core_icon, 0.0, 1.0)
            self._nbomb_simui.set_imageui_horpercent(self._nbomb_simui_device_icon, 0.0, 0.0)
        else:
            self.hide_nbomb_simui()

    def hide_nbomb_simui(self):
        if self._nbomb_simui_core_icon:
            self._nbomb_simui.set_imageui_horpercent(self._nbomb_simui_core_icon, 0.0, 0.0)
        if self._nbomb_simui_device_icon:
            self._nbomb_simui.set_imageui_horpercent(self._nbomb_simui_device_icon, 0.0, 0.0)

    def clear_nbomb_simui(self):
        if self._nbomb_simui and self._nbomb_simui.valid:
            self._nbomb_simui.destroy()
        self._nbomb_simui = None
        self._nbomb_simui_core_icon = None
        self._nbomb_simui_device_icon = None
        return

    def clear_simui(self):
        if self._mark_simui and self._mark_simui.valid:
            self._mark_simui.destroy()
        self._mark_simui = None
        return

    def clear_timer(self):
        self.hit_timer and self.tm.unregister(self.hit_timer)
        self.hit_timer = None
        return

    def clear_marks(self):
        self.clear_sfx()
        self.clear_simui()
        self.clear_timer()
        self.clear_nbomb_simui()
        self.clear_perspective_timer()
        self.need_update = False
        self.process_event(False)
        self.init_parameters()
        self.send_event('E_RESET_CAMP_OUTLINE')

    def _on_model_destroy(self):
        self.clear_marks()

    def destroy(self):
        self.clear_marks()
        super(ComBaseMarkView, self).destroy()