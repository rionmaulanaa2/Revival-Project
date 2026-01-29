# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/GoldenEggThrowUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gutils.rocker_widget_utils import RockerWidget
import math3d
import world
from common.cfg import confmgr
from logic.gutils.mecha_utils import get_fire_end_posiiton
import common.utils.timer as timer
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon import time_utility as t_util
import game
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'
GLODEN_EGG_WEAPON = 10601

def cal_fire_direction(position):
    if not (global_data.mecha and global_data.mecha.logic):
        import world
        return world.get_active_scene().active_camera.forward
    end_pos = get_fire_end_posiiton(global_data.mecha.logic)
    direction = end_pos - position
    if not direction.is_zero:
        direction.normalize()
    return direction


def get_fire_pos(_fire_socket):
    if not (global_data.mecha and global_data.mecha.logic):
        return None
    else:
        model = global_data.mecha.logic.ev_g_model()
        if not model or not model.valid:
            return None
        socket_matrix = model.get_socket_matrix(_fire_socket, world.SPACE_TYPE_WORLD)
        if not socket_matrix:
            return None
        return socket_matrix.translation


class WeaponTrackHelper(object):

    def __init__(self):
        self.weapon_iType = GLODEN_EGG_WEAPON
        self._timer_id = None
        self.last_finger_move_vec = None
        self._drag_base_val_specific = None
        self._drag_as_screen = False
        self.init_rocker_sensitivity()
        return

    def init_rocker_sensitivity(self):
        from logic.gcommon.common_const import ui_operation_const
        sst_frocker_setting = global_data.player.logic.get_owner().get_setting(ui_operation_const.SST_FROCKER_KEY)
        self.sst_setting = list(sst_frocker_setting)
        from logic.gutils import mecha_utils
        if global_data.mecha and global_data.mecha.logic:
            mecha_id = global_data.mecha.logic.ev_g_shape_id()
            btn_drag_base_val_spec = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SUB_WEAPON_STICK_MECHA_VAL_KEY)
            btn_rocker_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
            self._drag_base_val_specific = btn_drag_base_val_spec
            self._drag_as_screen = btn_rocker_as_screen

    def set_drag_base_val_specific(self, base_val):
        self._drag_base_val_specific = base_val

    def on_btn_drag_helper(self, touch, center_wpos):
        scene = world.get_active_scene()
        ctrl = scene.get_com('PartCtrl')
        if not ctrl:
            return
        else:
            pt = touch.getLocation()
            move_delta = self.smooth_touch_vec(touch.getDelta())
            if move_delta.length() <= 0:
                return
            sense_args = {'center_pos': center_wpos,'base_val': self._drag_base_val_specific,'setting': self.sst_setting,'as_screen': self._drag_as_screen}
            ctrl.on_touch_slide(move_delta.x, move_delta.y, None, pt, True, kwargs=sense_args)
            return

    def smooth_touch_vec(self, move_delta):
        if move_delta.length() > 0:
            if self.last_finger_move_vec is None:
                move_delta.normalize()
            self.last_finger_move_vec = move_delta
        return move_delta

    def destroy(self):
        self.unregister_timer()

    def register_timer(self):
        self.unregister_timer()
        self._timer_id = global_data.game_mgr.register_logic_timer(self.tick, interval=1, times=-1, mode=timer.LOGIC)

    def unregister_timer(self):
        if self._timer_id:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def show_weapon_track(self):
        if not (global_data.mecha and global_data.mecha.logic):
            return
        else:
            weapon_iType = self.weapon_iType
            conf = confmgr.get('grenade_config', str(weapon_iType))
            self._speed = conf['fSpeed']
            self._g = -conf.get('fGravity', 98)
            self._up_angle = conf.get('fUpAngle', 0)
            fire_sockets = None
            self._fire_socket = 'xuetiao'
            position = get_fire_pos(self._fire_socket)
            if not position:
                return
            direction = cal_fire_direction(position)
            global_data.mecha.logic.send_event('E_SHOW_PARABOLA_TRACK', END_STRIP_SFX, position, self._speed, self._g, self._up_angle, direction=direction)
            self.is_show = True
            self.register_timer()
            return

    def tick(self, *args):
        if not (global_data.mecha and global_data.mecha.logic):
            return None
        else:
            position = get_fire_pos(self._fire_socket)
            if not position:
                return None
            direction = cal_fire_direction(position)
            global_data.mecha.logic.send_event('E_UPDATE_PARABOLA_TRACK', position, direction)
            return None

    def stop_weapon_track(self):
        if not (global_data.mecha and global_data.mecha.logic):
            return None
        else:
            self.is_show = False
            self.unregister_timer()
            global_data.mecha.logic.send_event('E_HIDE_PARABOLA_TRACK')
            return None


class GoldenEggThrowUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_goldenegg_throw'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'snatchegg_egg_pick_up': '_on_egg_pick_up',
       'snatchegg_egg_drop': '_on_egg_recover',
       'flagsnatch_flag_init_complete': '_on_flag_init_complete',
       'snatchegg_round_stop_event': '_on_round_stop',
       'update_battle_data': 'process_vis'
       }
    HOT_KEY_FUNC_MAP = {'throw_golden_egg.DOWN_UP': 'keyboard_throw_egg'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'throw_golden_egg': {'node': 'nd_action_custom_2.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(GoldenEggThrowUI, self).on_init_panel()
        self.custom_ui_com = None
        self._rocker_widget = None
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})
        self.track_widget = WeaponTrackHelper()
        self.init_rocker()
        self.process_vis()
        return

    def keyboard_throw_egg(self, msg, keycode):
        if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
            self.on_throw_begin()
        else:
            self.on_throw_end()

    def process_vis(self):
        if self.get_vis():
            self.add_show_count('EGG')
        else:
            self.add_hide_count('EGG')

    def _on_egg_pick_up(self, *args):
        self.process_vis()

    def _on_egg_recover(self, *args):
        self.process_vis()

    def _on_flag_init_complete(self, *args):
        self.process_vis()

    def _on_round_stop(self, *args):
        self.process_vis()

    def get_vis(self):
        if not (global_data.player and global_data.player.logic):
            return False
        if not global_data.death_battle_data:
            return False
        mid = global_data.player.logic.id
        for holder_id, egg_id in six.iteritems(global_data.death_battle_data.egg_picker_dict):
            if str(mid) == str(holder_id):
                if global_data.death_battle_data.egg_throw_dict.get(holder_id) == egg_id:
                    return False
                else:
                    return True

        return False

    def on_change_ui_custom_data(self):
        if self._rocker_widget:
            self._rocker_widget.init_rocker()

    def init_rocker(self):
        nd = self.panel.action2
        bar = nd.bar
        btn = nd.button
        self._rocker_widget = RockerWidget(bar, btn, btn)
        self._rocker_widget.enable_drag = True
        self._rocker_widget.set_begin_callback(self.on_throw_begin)
        self._rocker_widget.set_drag_callback(self.on_throw_drag)
        self._rocker_widget.set_end_callback(self.on_throw_end)
        self.btn_dragged = False
        self.btn_dragged_dir = None
        return

    def on_finalize_panel(self):
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        if self._rocker_widget:
            self._rocker_widget.destroy()
            self._rocker_widget = None
        if self.track_widget:
            self.track_widget.destroy()
            self.track_widget = None
        return

    def check_can_throw(self):
        return True

    def on_throw_begin(self, *args):
        if self.track_widget:
            self.track_widget.show_weapon_track()
        if not global_data.ui_mgr.get_ui('MechaCancelUI'):
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.end_button_down, True)
        return True

    def on_throw_drag(self, btn, touch):
        self.btn_dragged = True
        if self.track_widget:
            self.track_widget.on_btn_drag_helper(touch, self._rocker_widget.rocker_center)

    def end_button_down(self, *args):
        if self.track_widget:
            self.track_widget.stop_weapon_track()
        if not (global_data.mecha and global_data.mecha.logic):
            return

    def on_throw_end(self, *args):
        if self.track_widget:
            self.track_widget.stop_weapon_track()
        if not (global_data.mecha and global_data.mecha.logic):
            return
        else:
            if not global_data.player:
                return
            if global_data.player.id not in global_data.death_battle_data.egg_picker_dict:
                return
            if not global_data.battle:
                return
            from logic.gcommon.common_const.idx_const import ExploderID
            from logic.gcommon.common_const.weapon_const import WP_SUMMON_GRENADES_GUN
            cancel_ui = global_data.ui_mgr.get_ui('MechaCancelUI')
            if cancel_ui:
                if cancel_ui.get_cancel_callback() == self.end_button_down:
                    global_data.ui_mgr.close_ui('MechaCancelUI')
            conf = confmgr.get('firearm_res_config', str(GLODEN_EGG_WEAPON))
            _fire_socket = 'xuetiao'
            position = get_fire_pos(_fire_socket)
            if not position:
                return
            direction = cal_fire_direction(position)
            egg_eid = global_data.death_battle_data.egg_picker_dict.get(global_data.player.id)
            egg_entity = global_data.battle.get_entity(egg_eid)
            if not (egg_entity and egg_entity.logic):
                return
            throw_item = {'egg_eid': egg_eid,
               'throw_soul_id': global_data.player.id,
               'uniq_key': ExploderID.gen(global_data.battle_idx),
               'item_itype': GLODEN_EGG_WEAPON,
               'item_kind': WP_SUMMON_GRENADES_GUN,
               'position': (
                          position.x, position.y, position.z),
               'm_position': None,
               'dir': (
                     direction.x, direction.y, direction.z)
               }
            from logic.gcommon.time_utility import get_server_time
            now = get_server_time()
            need_sync_server = True
            if need_sync_server:
                throw_item['call_sync_id'] = global_data.battle_idx
                sync_data = {}
                sync_data.update(throw_item)
                global_data.mecha.logic.send_event('E_CALL_SYNC_METHOD', 'thorw_explosive_item', (sync_data,), True)
            info = throw_item
            s_item_id = str(info['item_itype'])
            conf = confmgr.get('grenade_config', s_item_id)
            info['speed'] = info.get('fSpeed', conf['fSpeed'])
            info['mass'] = conf['fMass']
            info['last_time'] = conf['fTimeFly']
            info['gravity'] = conf['fGravity']
            info['begin_time'] = t_util.time()
            egg_entity and egg_entity.logic and egg_entity.logic.send_event('E_TRY_THROW_EGG')
            global_data.mecha.logic.send_event('E_THROW_EXPLOSIVE_ITEM', throw_item)
            global_data.emgr.snatchegg_egg_throw_event.emit(global_data.player.id, egg_eid)
            self.process_vis()
            return