# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComStateSimui.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from ..UnitCom import UnitCom
import math3d
import world
import render
from logic.gcommon.common_const.buff_const import BUFF_ID_KNIGHTTHROWABLE, BUFF_ID_MECHA8015_LIGHTNING, BUFF_ID_ANDROMEDA_IMMOBILIZED, BUFF_ID_MECHA8002_ELECTRIC_ADD_HURT, BUFF_ID_8017_AIM, BUFF_ID_8025_AIM, BUFF_ID_8030_AIM, BUFF_ID_8034_BLIND, BUFF_ID_8034_GROUNDED, BUFF_ID_MECHA_8013_TRACE, BUFF_ID_SHADOW_BLADE_MARK, BUFF_ID_PVE_ELETRIC_MARK
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK
from logic.gutils import mecha_utils
from logic.gcommon.common_const.mecha_const import MECHA_MODE_BLOOD_SOCKET_POS_OFFSET
MEHCA_STATE_SIMUI = {BUFF_ID_KNIGHTTHROWABLE: ('gui/ui_res_2/simui/sim_mech_paralysis.png', 78, 116, 0, 37),
   BUFF_ID_ANDROMEDA_IMMOBILIZED: ('gui/ui_res_2/simui/sim_mech_paralysis.png', 78, 116, 0, 37),
   BUFF_ID_MECHA8015_LIGHTNING: ('gui/ui_res_2/simui/sim_mech_8015.png', 0, 37, 0, 37),
   BUFF_ID_MECHA8002_ELECTRIC_ADD_HURT: ('gui/ui_res_2/simui/sim_mech_paralysis.png', 152, 152, 152, 152),
   BUFF_ID_SHADOW_BLADE_MARK: ('gui/ui_res_2/simui/sim_mech_paralysis_dark.png', 0, 37, 0, 37),
   BUFF_ID_PVE_ELETRIC_MARK: ('gui/ui_res_2/simui/sim_mech_8015.png', 0, 37, 0, 37)
   }
MECHA_FLAG_SIMUI = {BUFF_ID_8017_AIM: ('gui/ui_res_2/simui/sim_mech_8017.png', 0, 0, 44, 44, 0, 0),
   BUFF_ID_8025_AIM: ('gui/ui_res_2/simui/sim_mech_8017.png', 0, 0, 44, 44, 0, 0),
   BUFF_ID_8030_AIM: ('gui/ui_res_2/simui/sim_mech_8030.png', 0, 0, 44, 44, 0, 0),
   BUFF_ID_8034_GROUNDED: ('gui/ui_res_2/battle/mech_attack/mech8034/icon_mech8034_ban.png', 0, 0, 44, 44, 0,
 0),
   BUFF_ID_8034_BLIND: ('gui/ui_res_2/simui/simui_mecha8034_status.png', 0, 0, 45, 45, 0, 0),
   BUFF_ID_8034_BLIND + 1: ('gui/ui_res_2/simui/simui_mecha8034_status.png', 45, 0, 45, 45, 0, 0)
   }
PERCENT_DIR_HORI = 0
PERCENT_DIR_VER = 1
PERCENT_STATE_SIMUI = {BUFF_ID_MECHA_8013_TRACE: (
                            'gui/ui_res_2/simui/sim_mech8013_track.png', 0, 0, 38, 0, 38, 38, PERCENT_DIR_VER)
   }
CREATOR_ONLY = 0
CREATOR_AVATAR = 1
AVATAR_EXCLUDE = 2
ALL = 3
MECHA_FLAG_SIMUI_VISIBLE = {BUFF_ID_8030_AIM: CREATOR_AVATAR,
   BUFF_ID_8034_GROUNDED: ALL,
   BUFF_ID_8034_BLIND: AVATAR_EXCLUDE,
   BUFF_ID_8034_BLIND + 1: AVATAR_EXCLUDE
   }

class ComStateSimui(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_IMMOBILIZED': '_on_immobilized',
       'E_AUTO_AIM_BY_OTHERS': '_on_auto_aim_by_others',
       'E_BODY_ELECTRIC': '_on_electric',
       'E_SHOW_STATE_UI': '_on_show_state_ui',
       'E_HIT_FLAG_LEVEL_CHANGED': 'on_hit_flag_level_changed',
       'E_SWITCH_STATE_SOCKET': '_switch_state_socket',
       'E_TRACE_MARK_CHANGED': 'on_trace_mark_changed',
       'E_CREATE_PERCENT_STATE_UI': '_create_percent_state_ui',
       'E_DEATH': 'on_dead',
       'E_HIDE_ALL_STATE_UI': 'hide_all_ui',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_SET_MECAH_MODE': ('refesh_blood_model_pos', 100),
       'E_HEALTH_HP_EMPTY': 'on_dead'
       }

    def __init__(self):
        super(ComStateSimui, self).__init__()
        self._state_ui = {}
        self._state_bg = {}
        self._state_frame = {}
        self._state_lv_list = {}
        self._state_bg_list = {}
        self._state_running = {}
        self.need_state_ui_update = {}
        self._flag_ui = {}
        self._immo_timer = None
        self.need_hide_all_ui = False
        self._state_default_offset_y = -50
        self._state_list_ui_offset = {}
        self._removed_state_list_ui_offset = {}
        self._mecha_model = None
        self._percent_state_ui_dict = {}
        self._percent_state_cache = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComStateSimui, self).init_from_dict(unit_obj, bdict)
        if self.sd.ref_is_pve_monster:
            self._state_default_offset_y = -80

    def _on_model_loaded(self, model):
        self._need_update = False
        if not model:
            return
        self._on_model_loaded_simui(model)

    def _on_model_loaded_simui(self, model):
        self._mecha_model = model
        for ui_key, args in six.iteritems(self._percent_state_cache):
            self._create_percent_state_ui(ui_key, *args)

        self._percent_state_cache = {}
        for flag_id in six.iterkeys(MEHCA_STATE_SIMUI):
            self._create_state_ui(flag_id)
            self.on_hit_flag_level_changed(flag_id, self.ev_g_hit_flag_level(flag_id))

        self._immo_left_time = self.ev_g_attr_get('immo_time')
        if self._immo_left_time is not None and self._immo_left_time > 0:
            self._on_immobilized(True)
        for flag_id in six.iterkeys(MECHA_FLAG_SIMUI):
            self._create_flag_ui(flag_id)

        return

    def get_cur_state_offset_y(self, except_ui_key=''):
        cur_height = self._state_default_offset_y
        for uk, info in six.iteritems(self._state_list_ui_offset):
            if uk == except_ui_key:
                continue
            cur_height -= info['height']

        return cur_height

    def get_simui_id(self, simui, ui_id):
        return '{}_{}'.format(id(simui), ui_id)

    def set_state_offset(self, ui_key, simui, ui_id, offsetx, height):
        cur_height = self.get_cur_state_offset_y(except_ui_key=ui_key)
        cur_info = self._state_list_ui_offset.get(ui_key, None)
        if not cur_info:
            cur_info = self._removed_state_list_ui_offset.get(ui_key, None)
            if not cur_info:
                cur_info = {'height': height,'ui_ids': {}}
                self._state_list_ui_offset[ui_key] = cur_info
            else:
                self._state_list_ui_offset[ui_key] = cur_info
                del self._removed_state_list_ui_offset[ui_key]
        cur_info['offsety'] = cur_height
        simui_id = self.get_simui_id(simui, ui_id)
        if simui_id not in cur_info['ui_ids']:
            cur_info['ui_ids'][simui_id] = {'offsetx': offsetx,'simui': simui,'ui_id': ui_id}
        simui.set_ui_pos(ui_id, offsetx, cur_height)
        return

    def remove_state_offset(self, ui_key, destroy=False):
        if destroy and ui_key in self._removed_state_list_ui_offset:
            del self._removed_state_list_ui_offset[ui_key]
            return
        if ui_key not in self._state_list_ui_offset:
            return
        del_info = self._state_list_ui_offset[ui_key]
        if not destroy:
            self._removed_state_list_ui_offset[ui_key] = del_info
        del self._state_list_ui_offset[ui_key]
        remove_height = del_info['height']
        remove_offsety = del_info['offsety']
        for uk, info in six.iteritems(self._state_list_ui_offset):
            if info['offsety'] >= remove_offsety:
                continue
            cur_height = info['offsety'] + remove_height
            for _, id_info in six.iteritems(info['ui_ids']):
                id_info['simui'].set_ui_pos(id_info['ui_id'], id_info['offsetx'], cur_height)

            info['offsety'] = cur_height

    def recover_state_offset(self, ui_key):
        if ui_key in self._state_list_ui_offset:
            return
        if ui_key not in self._removed_state_list_ui_offset:
            return
        cur_height = self.get_cur_state_offset_y(except_ui_key=ui_key)
        info = self._removed_state_list_ui_offset.get(ui_key)
        for ui_id, id_info in six.iteritems(info['ui_ids']):
            id_info['simui'].set_ui_pos(id_info['ui_id'], id_info['offsetx'], cur_height)

        info['offsety'] = cur_height
        del self._removed_state_list_ui_offset[ui_key]
        self._state_list_ui_offset[ui_key] = info

    def set_state_visible(self, ui_key, flag):
        if flag:
            self.recover_state_offset(ui_key)
        else:
            self.remove_state_offset(ui_key)

    def get_state_ui_parameters(self, flag_id):
        return (
         38, 44, -20, self._state_default_offset_y)

    def get_xuetiao_socket(self):
        ret = self.ev_g_get_socket()
        if ret:
            return ret
        else:
            return ('xuetiao', 0)

    def _create_state_ui(self, flag_id):
        if not self._mecha_model:
            return
        SIMUI_RES, lv_pos, bg_pos, st_frame, st_bg = MEHCA_STATE_SIMUI.get(flag_id)
        if not SIMUI_RES:
            return
        self._state_ui[flag_id] = world.simuiobject(render.texture(SIMUI_RES))
        state_ui = self._state_ui[flag_id]
        width, height, offsetx, offsety = self.get_state_ui_parameters(flag_id)
        state_bg = state_ui.add_image_ui(st_bg, 0, width, height, offsetx, offsety)
        state_frame = state_ui.add_image_ui(st_frame, 0, width, height, offsetx, offsety)
        state_ui.set_ui_alpha(state_bg, 0)
        state_ui.set_ui_alpha(state_frame, 0)
        self._state_bg[flag_id] = state_bg
        self._state_frame[flag_id] = state_frame
        self.set_state_offset(flag_id, state_ui, state_bg, offsetx, height)
        self.set_state_offset(flag_id, state_ui, state_frame, offsetx, height)
        state_lv_list = []
        state_bg_list = []
        space_off_x = width - 8
        start_offset_x = -self.ev_g_hit_flag_level_num(flag_id) / 2.0 * space_off_x
        for i in range(0, self.ev_g_hit_flag_level_num(flag_id)):
            _offsetx = start_offset_x + i * space_off_x
            bg_ui_id = state_ui.add_image_ui(bg_pos, 0, width, height, _offsetx, offsety)
            lv_ui_id = state_ui.add_image_ui(lv_pos, 0, width, height, _offsetx, offsety)
            self.set_state_offset(flag_id, state_ui, bg_ui_id, _offsetx, height)
            self.set_state_offset(flag_id, state_ui, lv_ui_id, _offsetx, height)
            state_bg_list.append(bg_ui_id)
            state_lv_list.append(lv_ui_id)
            state_ui.set_ui_alpha(bg_ui_id, 0)
            state_ui.set_ui_alpha(lv_ui_id, 0)

        self._state_lv_list[flag_id] = state_lv_list
        self._state_bg_list[flag_id] = state_bg_list
        ui_insts = [
         state_bg,
         state_frame]
        for ui_inst in ui_insts:
            state_ui.set_ui_fill_z(ui_inst, True)

        for ui_inst in state_lv_list:
            state_ui.set_ui_fill_z(ui_inst, True)
            state_ui.set_ui_alpha(ui_inst, 0)

        for ui_inst in state_bg_list:
            state_ui.set_ui_fill_z(ui_inst, True)
            state_ui.set_ui_alpha(ui_inst, 0)

        socket, bias = self.get_xuetiao_socket()
        self._mecha_model.bind(socket, state_ui)
        state_ui.position = math3d.vector(0, bias, 0)
        state_ui.visible = False
        self.set_state_visible(flag_id, False)
        state_ui.inherit_flag &= ~world.INHERIT_VISIBLE

    def on_hit_flag_level_changed(self, flag_id, new_level):
        is_ui_visible = mecha_utils.check_hit_flag_visible(self.unit_obj.id, flag_id)
        if not is_ui_visible:
            self._state_running[flag_id] = False
        state_ui = self._state_ui.get(flag_id)
        if not state_ui or not state_ui.valid:
            return
        state_lv_list = self._state_lv_list.get(flag_id, [])
        state_bg_list = self._state_bg_list.get(flag_id, [])
        if new_level > 0 and is_ui_visible:
            state_ui.visible = not self.need_hide_all_ui
            self.set_state_visible(flag_id, True)
            self.need_state_ui_update[flag_id] = True
            self.update_update_info()
            for index, ui_inst in enumerate(state_bg_list):
                state_ui.set_ui_alpha(ui_inst, 255)

            for index, ui_inst in enumerate(state_lv_list):
                if new_level >= index + 1:
                    state_ui.set_ui_alpha(ui_inst, 255)
                else:
                    state_ui.set_ui_alpha(ui_inst, int(0))

            if flag_id == BUFF_ID_ANDROMEDA_IMMOBILIZED:
                self.set_on_immoblize_state_vis(False)
        else:
            state_running = self._state_running.get(flag_id, False)
            state_ui.visible = not self.need_hide_all_ui and state_running
            self.set_state_visible(flag_id, state_running)
            self.need_state_ui_update[flag_id] = state_running
            self.update_update_info()
            for ui_inst in state_lv_list:
                state_ui.set_ui_alpha(ui_inst, 0)

        for ui_inst in state_bg_list:
            state_ui.set_ui_alpha(ui_inst, 0)

    def _on_immobilized(self, immobilized, *args):
        flag_id = BUFF_ID_ANDROMEDA_IMMOBILIZED
        self._state_running[flag_id] = immobilized
        state_ui = self._state_ui.get(flag_id)
        if state_ui and state_ui.valid:
            state_ui.visible = immobilized
            self.set_state_visible(flag_id, immobilized)
            self.need_state_ui_update[flag_id] = immobilized
            self.update_update_info()
            self.set_on_immoblize_state_vis(immobilized)
            self.on_hit_flag_level_changed(flag_id, 0)
        self._on_electric(self._state_running.get(BUFF_ID_MECHA8002_ELECTRIC_ADD_HURT, False))

    def _on_electric(self, flag, *args):
        flag_id = BUFF_ID_MECHA8002_ELECTRIC_ADD_HURT
        self._state_running[flag_id] = flag
        state_ui = self._state_ui.get(flag_id)
        if state_ui and state_ui.valid:
            visible = False if self._state_running.get(BUFF_ID_ANDROMEDA_IMMOBILIZED, False) else flag
            state_ui.visible = visible
            self.set_state_visible(flag_id, visible)
            self.need_state_ui_update[flag_id] = flag
            self.update_update_info()
            self.set_on_electric_state_vis(visible)
            self.on_hit_flag_level_changed(flag_id, 0)

    def _on_show_state_ui(self, flag_id, show):
        self._state_running[flag_id] = show
        state_ui = self._state_ui.get(flag_id)
        if state_ui and state_ui.valid:
            state_ui.visible = show
            self.set_state_visible(flag_id, show)
            self.need_state_ui_update[flag_id] = show
            self.update_update_info()

    def set_on_immoblize_state_vis(self, vis):
        flag_id = BUFF_ID_ANDROMEDA_IMMOBILIZED
        state_bg = self._state_bg.get(flag_id)
        state_frame = self._state_frame.get(flag_id)
        state_ui = self._state_ui.get(flag_id)
        if not state_ui or not state_bg or not state_frame:
            return
        other_ui_inst = [
         state_bg, state_frame]
        self._cancel_immo_timer()

        def cb():
            speed_frame = 1.0 / self._immo_left_time / 30.0
            self._cur_frame += speed_frame
            if self._cur_frame >= 1.0:
                self._cur_frame = 1.0
                self._cancel_immo_timer()
            state_ui.set_imageui_verpercent(state_frame, self._cur_frame, 1.0)

        if vis:
            self._immo_left_time = self.ev_g_attr_get('immo_time')
            if not self._immo_left_time:
                return
            self._cur_frame = 0.0
            state_ui.set_imageui_verpercent(state_frame, 0.0, 1.0)
            self._immo_timer = global_data.game_mgr.register_logic_timer(func=cb, interval=0.033, times=-1, mode=CLOCK)
        is_avatar = self.ev_g_is_avatar()
        to_alpha = 255 if vis and not is_avatar else 0
        for ui_inst in other_ui_inst:
            state_ui.set_ui_alpha(ui_inst, to_alpha)

    def set_on_electric_state_vis(self, vis):
        flag_id = BUFF_ID_MECHA8002_ELECTRIC_ADD_HURT
        state_bg = self._state_bg.get(flag_id, None)
        state_frame = self._state_frame.get(flag_id, None)
        state_ui = self._state_ui.get(flag_id)
        if not state_ui or not state_bg or not state_frame:
            return
        else:
            other_ui_inst = [
             state_bg, state_frame]
            is_avatar = self.ev_g_is_avatar()
            to_alpha = 255 if vis and not is_avatar else 0
            for ui_inst in other_ui_inst:
                state_ui.set_ui_alpha(ui_inst, to_alpha)

            return

    def _cancel_immo_timer(self):
        if self._immo_timer:
            global_data.game_mgr.unregister_logic_timer(self._immo_timer)
        self._immo_timer = None
        return

    def _create_flag_ui(self, flag_id):
        if not self._mecha_model:
            return
        is_cam_player = self.unit_obj == global_data.cam_lctarget
        pic_path, left, top, w, h, posx, posy = MECHA_FLAG_SIMUI.get(flag_id, MECHA_FLAG_SIMUI[BUFF_ID_8017_AIM])
        posy = self._state_default_offset_y
        flag_ui = world.simuiobject(render.texture(pic_path))
        self._flag_ui[flag_id] = flag_ui
        image = flag_ui.add_image_ui(left, top, w, h, posx, posy)
        self.set_state_offset(flag_id, flag_ui, image, posx, h)
        flag_ui.set_ui_align(image, 0.5, 0)
        flag_ui.set_ui_fill_z(image, True)
        socket, bias = self.get_xuetiao_socket()
        self._mecha_model.bind(socket, flag_ui)
        flag_ui.inherit_flag &= ~world.INHERIT_VISIBLE
        flag_ui.position = math3d.vector(0, bias, 0)
        flag_ui.visible = False
        self.set_state_visible(flag_id, False)

    def _on_auto_aim_by_others(self, flag, buff_id, creator_id):
        if not self._mecha_model:
            return
        if flag:
            visible = MECHA_FLAG_SIMUI_VISIBLE.get(buff_id, CREATOR_ONLY)
            is_avatar = self.unit_obj == global_data.cam_lctarget
            if visible == AVATAR_EXCLUDE and is_avatar:
                return
            is_creator = global_data.cam_lplayer and global_data.cam_lplayer.id == creator_id
            if visible == CREATOR_ONLY and not is_creator:
                return
            if visible == CREATOR_AVATAR and not (is_creator or is_avatar):
                return
        state_ui = self._flag_ui.get(buff_id)
        if state_ui and state_ui.valid:
            state_ui.visible = flag
            self.set_state_visible(buff_id, flag)
            self.need_state_ui_update[buff_id] = flag
            self.update_update_info()

    def on_trace_mark_changed(self, creator_id, start_time, duration):
        self._percent_state_start_time = start_time
        self._percent_state_duration = duration
        self._create_percent_state_ui(BUFF_ID_MECHA_8013_TRACE, start_time, duration)

    def _clear_percent_state_ui(self, ui_key, destroy=False):
        if ui_key not in self._percent_state_ui_dict:
            return
        else:
            percent_state_info = self._percent_state_ui_dict[ui_key]
            if destroy:
                if percent_state_info['state_ui'] and percent_state_info['state_ui'].valid:
                    percent_state_info['state_ui'].destroy()
                percent_state_info['state_ui'] = None
                if percent_state_info['state_bg_ui'] and percent_state_info['state_bg_ui'].valid:
                    percent_state_info['state_bg_ui'].destroy()
                self._percent_state_ui_dict.pop(ui_key)
                self.remove_state_offset(ui_key, destroy=destroy)
            else:
                if percent_state_info['state_ui']:
                    percent_state_info['state_ui'].visible = False
                if percent_state_info['state_bg_ui']:
                    percent_state_info['state_bg_ui'].visible = False
                self.set_state_visible(ui_key, False)
            percent_state_info['start_time'] = 0
            percent_state_info['duration'] = 0
            percent_state_info['need_update'] = False
            self.update_update_info()
            return

    def _create_percent_state_ui(self, ui_key, start_time, duration, revert=False):
        self._clear_percent_state_ui(ui_key)
        if not self._mecha_model:
            self._percent_state_cache[ui_key] = [
             start_time, duration, revert]
            return
        else:
            if duration <= 0:
                return
            if ui_key not in self._percent_state_ui_dict:
                self._percent_state_ui_dict[ui_key] = {}
            percent_state_info = self._percent_state_ui_dict[ui_key]
            percent_state_info['start_time'] = start_time
            percent_state_info['duration'] = duration
            percent_state_info['need_update'] = True
            percent_state_info['revert'] = revert
            self.update_update_info()
            if percent_state_info.get('state_ui', None):
                percent_state_info['state_ui'].visible = True
                percent_state_info['state_bg_ui'].visible = True
                self.set_state_visible(ui_key, True)
                return
            path, left, top, bg_left, bg_top, w, h, dir = PERCENT_STATE_SIMUI[ui_key]
            percent_state_info['direction'] = dir
            percent_state_info['state_bg_ui'] = world.simuiobject(render.texture(path))
            percent_state_info['state_ui'] = world.simuiobject(render.texture(path))
            offsetx, offsety = -20, self._state_default_offset_y
            percent_state_info['state'] = percent_state_info['state_ui'].add_image_ui(left, top, w, h, offsetx, offsety)
            percent_state_info['state_bg'] = percent_state_info['state_bg_ui'].add_image_ui(bg_left, bg_top, w, h, offsetx, offsety)
            self.set_state_offset(ui_key, percent_state_info['state_ui'], percent_state_info['state'], offsetx, h)
            self.set_state_offset(ui_key, percent_state_info['state_bg_ui'], percent_state_info['state_bg'], offsetx, h)
            percent_state_info['state_bg_ui'].set_ui_fill_z(percent_state_info['state_bg'], True)
            percent_state_info['state_bg_ui'].set_ui_alpha(percent_state_info['state_bg'], 255)
            percent_state_info['state_ui'].set_ui_fill_z(percent_state_info['state'], True)
            percent_state_info['state_ui'].set_ui_alpha(percent_state_info['state'], 255)
            flag = ~world.INHERIT_VISIBLE
            socket, bias = self.get_xuetiao_socket()
            self._switch_state_socket(socket, bias, self._mecha_model)
            percent_state_info['state_bg_ui'].visible = True
            percent_state_info['state_bg_ui'].inherit_flag &= flag
            percent_state_info['state_ui'].visible = True
            percent_state_info['state_ui'].inherit_flag &= flag
            return

    def _update_percent_state_ui(self):
        from common.utilities import safe_percent
        from logic.gcommon import time_utility
        now = time_utility.time()
        for ui_key, percent_state_info in six.iteritems(self._percent_state_ui_dict):
            if not percent_state_info['need_update']:
                continue
            left_time = percent_state_info['start_time'] + percent_state_info['duration'] - now
            if left_time <= 0:
                self._clear_percent_state_ui(ui_key)
                continue
            percent = min(max(safe_percent(left_time, percent_state_info['duration']) / 100.0, 0), 1)
            if percent_state_info['revert']:
                percent = 1.0 - percent
            if percent_state_info['direction'] == PERCENT_DIR_HORI:
                percent_state_info['state_ui'].set_imageui_horpercent(percent_state_info['state'], 0.0, percent)
            else:
                percent_state_info['state_ui'].set_imageui_verpercent(percent_state_info['state'], 1.0 - percent, 1.0)

    def on_dead(self):
        self._on_immobilized(False)
        self.hide_all_ui()
        for flag_id in six.iterkeys(MECHA_FLAG_SIMUI):
            self._on_auto_aim_by_others(False, flag_id, None)

        return

    def hide_all_ui(self, hide=True):
        show = not hide
        for flag_id, state_ui in six.iteritems(self._state_ui):
            if state_ui and state_ui.valid:
                state_ui.visible = show

        for percent_state_info in six.itervalues(self._percent_state_ui_dict):
            percent_state_info['state_bg_ui'].visible = percent_state_info['need_update'] and show
            percent_state_info['state_ui'].visible = percent_state_info['need_update'] and show

        self.need_hide_all_ui = hide

    def update_update_info(self):
        need_update = False
        for state_ui_update in six.itervalues(self.need_state_ui_update):
            need_update = need_update | state_ui_update

        for percent_state_info in six.itervalues(self._percent_state_ui_dict):
            need_update = need_update | percent_state_info['need_update']

        self.showing_sim_ui = need_update
        if need_update:
            self.need_update = True

    def tick(self, dt):
        if not (self._mecha_model and self._mecha_model.valid):
            return
        if self.showing_sim_ui:
            self.tick_sim_ui()
        if not self.showing_sim_ui:
            self.need_update = False

    def tick_sim_ui(self):
        pos = self._mecha_model.world_position
        dist = self.scene.active_camera.position - pos
        dist = dist.length / NEOX_UNIT_SCALE
        max_dist = 100
        scale = (max_dist - dist) * 1.0 / max_dist
        scale = max(scale, 0.6)
        for state_ui in six.itervalues(self._state_ui):
            state_ui.scale = (
             scale, scale)

        for flag_ui in six.itervalues(self._flag_ui):
            flag_ui.scale = (
             scale, scale)

        percent_scale = scale * 1.5
        for percent_state_info in six.itervalues(self._percent_state_ui_dict):
            if not percent_state_info['need_update']:
                continue
            percent_state_info['state_bg_ui'].scale = (
             percent_scale, percent_scale)
            percent_state_info['state_ui'].scale = (percent_scale, percent_scale)

        self._update_percent_state_ui()

    def destroy(self):
        self._cancel_immo_timer()
        for ui_key in six_ex.keys(self._percent_state_ui_dict):
            self._clear_percent_state_ui(ui_key, destroy=True)

        for state_ui in six.itervalues(self._state_ui):
            if state_ui and state_ui.valid:
                state_ui.destroy()

        self._state_ui = {}
        for flag_ui in six.itervalues(self._flag_ui):
            if flag_ui and flag_ui.valid:
                flag_ui.destroy()

        self._flag_ui = {}
        self._state_list_ui_offset = {}
        self._removed_state_list_ui_offset = {}
        super(ComStateSimui, self).destroy()

    def refesh_blood_model_pos(self, *args):
        socket_name, pos_offset = self.get_xuetiao_socket()
        self._switch_state_socket(socket_name, pos_offset)

    def _switch_state_socket(self, socket, bias, mecha_model=None):
        if not mecha_model:
            mecha_model = self.ev_g_model()
            if not mecha_model:
                return
        for state_ui in six.itervalues(self._state_ui):
            mecha_model.unbind(state_ui)
            mecha_model.bind(socket, state_ui)
            state_ui.position = math3d.vector(0, bias, 0)
            state_ui.inherit_flag &= ~world.INHERIT_VISIBLE

        for flag_id, flag_ui in six.iteritems(self._flag_ui):
            mecha_model.unbind(flag_ui)
            mecha_model.bind(socket, flag_ui)
            flag_ui.visible = self.need_state_ui_update.get(flag_id, False) and not self.need_hide_all_ui
            flag_ui.position = math3d.vector(0, bias, 0)
            flag_ui.inherit_flag &= ~world.INHERIT_VISIBLE

        for percent_state_info in six.itervalues(self._percent_state_ui_dict):
            mecha_model.unbind(percent_state_info['state_bg_ui'])
            mecha_model.bind(socket, percent_state_info['state_bg_ui'])
            percent_state_info['state_bg_ui'].position = math3d.vector(0, bias, 0)
            percent_state_info['state_bg_ui'].inherit_flag &= ~world.INHERIT_VISIBLE
            mecha_model.unbind(percent_state_info['state_ui'])
            mecha_model.bind(socket, percent_state_info['state_ui'])
            percent_state_info['state_ui'].position = math3d.vector(0, bias, 0)
            percent_state_info['state_ui'].inherit_flag &= ~world.INHERIT_VISIBLE

    def on_switch_model(self, model):
        old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
        socket, bias = self.get_xuetiao_socket()
        for state_id, state_ui in six.iteritems(self._state_ui):
            old_model.unbind(state_ui)
            model.bind(socket, state_ui)
            state_ui.visible = self.need_state_ui_update[state_id] and not self.need_hide_all_ui
            state_ui.position = math3d.vector(0, bias, 0)
            state_ui.inherit_flag &= ~world.INHERIT_VISIBLE

        for flag_id, flag_ui in six.iteritems(self._flag_ui):
            old_model.unbind(flag_ui)
            model.bind(socket, flag_ui)
            flag_ui.visible = self.need_state_ui_update.get(flag_id, False) and not self.need_hide_all_ui
            flag_ui.position = math3d.vector(0, bias, 0)
            flag_ui.inherit_flag &= ~world.INHERIT_VISIBLE

        for percent_state_info in six.itervalues(self._percent_state_ui_dict):
            old_model.unbind(percent_state_info['state_bg_ui'])
            model.bind(socket, percent_state_info['state_bg_ui'])
            percent_state_info['state_bg_ui'].visible = percent_state_info['need_update'] and not self.need_hide_all_ui
            percent_state_info['state_bg_ui'].position = math3d.vector(0, bias, 0)
            percent_state_info['state_bg_ui'].inherit_flag &= ~world.INHERIT_VISIBLE
            old_model.unbind(percent_state_info['state_ui'])
            model.bind(socket, percent_state_info['state_ui'])
            percent_state_info['state_ui'].visible = percent_state_info['need_update'] and not self.need_hide_all_ui
            percent_state_info['state_ui'].position = math3d.vector(0, bias, 0)
            percent_state_info['state_ui'].inherit_flag &= ~world.INHERIT_VISIBLE