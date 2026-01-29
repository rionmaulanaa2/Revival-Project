# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaBloodUI.py
from __future__ import absolute_import
import six
import math3d
import world
from logic.gcommon.component.client.ComBloodUI import ComBloodUI
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gutils import mecha_utils
from logic.gcommon import const
import time
from common.cfg import confmgr
import weakref
from logic.gcommon.common_const.mecha_const import MECHA_MODE_BLOOD_SOCKET_POS_OFFSET
FFA_ICON_BIG = 'ffa_icon_big'
FFA_ICON_SMALL = 'ffa_icon_small'

class ComMechaBloodUI(ComBloodUI):
    BIND_EVENT = ComBloodUI.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SET_SHIELD': '_set_shield',
       'E_SET_SHIELD_MAX': '_set_shield_max',
       'E_OUTER_SHIELD_HP_CHANGED': '_on_outer_shield_changed',
       'E_SET_TEMPORARY_SHIELD': ('on_set_temporary_shield', 100),
       'E_TRANS_TO_BALL_FINISH': '_trans_to_ball',
       'E_TRANS_TO_HUMAN': '_trans_to_mecha',
       'G_GET_SOCKET': '_get_socket',
       'E_ENABLE_HP_UI': 'enable_hp_ui',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_SET_MECAH_MODE': ('refesh_blood_model_pos', 99)
       })
    MECHA = 'mecha'
    BALL = 'ball'
    BALL_BIAS = 35

    def __init__(self):
        super(ComMechaBloodUI, self).__init__()
        self._state = None
        self._enable = True
        return

    def on_init_complete(self):
        self.process_ffa_event(True)

    def destroy(self):
        self.process_ffa_event(False)
        super(ComMechaBloodUI, self).destroy()

    def _blood_bar_load_callback(self, model, *args):
        super(ComMechaBloodUI, self)._blood_bar_load_callback(model, *args)
        self.set_texture('_TexWhite', self.HIT_HP_TEXTURE, model)
        self.refesh_blood_model_pos()

    def _get_socket(self):
        state = self._state or self.ev_g_ball_state()
        if state and state[0] > 0:
            self._state = self.BALL if 1 else self.MECHA
        if self._state == self.BALL:
            return ('shield', self.BALL_BIAS)
        mecha_id = self.ev_g_mecha_id()
        mecha_mode = self.ev_g_mecha_mode()
        pos_offset = MECHA_MODE_BLOOD_SOCKET_POS_OFFSET.get(mecha_id, {}).get(mecha_mode, 0)
        return (
         'xuetiao', pos_offset)

    def _get_visible_time(self):
        if const.ROBOT_DEBUG:
            return 3600
        return self.VISIBLE_TIME

    def _can_show_hp_info(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE):
            return self.unit_obj.__class__.__name__ != 'LMotorcycle'
        return super(ComMechaBloodUI, self)._can_show_hp_info()

    def enable_hp_ui(self, enable):
        self._enable = enable
        model = self._model() if self._model else None
        if model and model.valid:
            model.visible = self.showing_model_ui and self._enable
        return

    def _on_show_hp_info(self):
        if self._model:
            model = self._model() if 1 else None
            return model and model.valid or None
        else:
            if not self.showing_model_ui:
                now = time.time()
                self.set_var('_XBlood', self._hp, model)
                self.set_var('_YBlood', self.format_shield, model)
                self.set_var('_ZBlood', self.format_other_shield(), model)
                self.set_var('_X', self._hp, model)
                self.set_var('_Y', self.format_shield)
                self.set_var('_Z', self.format_other_shield_max())
                self.check_in_danger(model)
                model.visible = self._enable
                self.showing_model_ui = True
                self.need_update = True
            self._hide_time = time.time() + self._get_visible_time()
            return

    def _trans_to_ball(self, need_bcast=False):
        if need_bcast:
            import logic.gcommon.common_utils.bcast_utils as bcast
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_TRANS_TO_BALL_FINISH, ()), True, True, True)
        if self._state == self.BALL:
            return
        self._state = self.BALL
        mecha_model = self.ev_g_model()
        if not mecha_model:
            return
        self._switch_socket('shield', self.BALL_BIAS, mecha_model)
        self.send_event('E_SWITCH_STATE_SOCKET', 'shield', self.BALL_BIAS, mecha_model)

    def _trans_to_mecha(self):
        if self._state == self.MECHA:
            return
        self._state = self.MECHA
        mecha_model = self.ev_g_model()
        if not mecha_model:
            return
        self._switch_socket('xuetiao', 0)
        self.send_event('E_SWITCH_STATE_SOCKET', 'xuetiao', 0)

    def refesh_blood_model_pos(self, *args):
        socket_name, pos_offset = self._get_socket()
        self._switch_socket(socket_name, pos_offset)
        self.send_event('E_SWITCH_STATE_SOCKET', socket_name, pos_offset)

    def _switch_socket(self, socket, bias, mecha_model=None):
        if not mecha_model:
            mecha_model = self.ev_g_model()
            if not mecha_model:
                return
        blood_model = self._model() if self._model else None
        if blood_model:
            mecha_model.unbind(blood_model)
            mecha_model.bind(socket, blood_model)
            blood_model.visible = self.showing_model_ui
            blood_model.position = math3d.vector(0, bias, 0)
            blood_model.inherit_flag &= ~world.INHERIT_VISIBLE
        for sub_model in six.itervalues(self._sub_model):
            sub_model = sub_model()
            if sub_model:
                sub_model.inherit_flag &= ~world.INHERIT_VISIBLE

        return

    def on_set_temporary_shield(self, temporary_shield_map):
        temporary_shield = self.ev_g_sum_temporary_shield()
        self._on_temporary_shield_changed(temporary_shield)

    def get_blood_unit_count(self):
        return mecha_utils.get_mecha_blood_unit_count()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_FFA, game_mode_const.GAME_MODE_ZOMBIE_FFA))
    def process_ffa_event(self, is_init):
        if is_init:
            global_data.emgr.update_top_group_info += self._update_top_group_info
            self._update_top_group_info()
        else:
            global_data.emgr.update_top_group_info -= self._update_top_group_info

    def _update_top_group_info(self, *args):
        player_eid = self.unit_obj.id
        if self.sd.ref_is_mecha:
            player_eid = self.sd.ref_driver_id
        battle_data = global_data.ffa_battle_data or global_data.zombieffa_battle_data
        self._is_ffa_top = battle_data.is_top_1(player_eid) if battle_data else False
        self.refresh_show_top_icon()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_FFA, game_mode_const.GAME_MODE_ZOMBIE_FFA))
    def refresh_show_top_icon(self):
        model = self.get_model()
        if not (model and model.valid):
            return
        big_icon_model = self.get_sub_model(FFA_ICON_BIG)
        small_icon_model = self.get_sub_model(FFA_ICON_SMALL)
        is_teammate = self._is_teammate(global_data.cam_lplayer)
        if big_icon_model:
            big_icon_model.visible = self._is_ffa_top and not self.showing_model_ui and not is_teammate
        if small_icon_model:
            small_icon_model.visible = self._is_ffa_top and self.showing_model_ui and not is_teammate
        if not self._ffa_top_icon_load and self._is_ffa_top:
            self._ffa_top_icon_load = True
            model_path_big = confmgr.get('script_gim_ref')['xuetiao_ffa_ace_128']
            self.ev_g_load_model(model_path_big, self._top_icon_load_callback, FFA_ICON_BIG)
            model_path = confmgr.get('script_gim_ref')['xuetiao_ffa_ace']
            self.ev_g_load_model(model_path, self._top_icon_load_callback, FFA_ICON_SMALL)

    def _top_icon_load_callback(self, model, icon_name, *args):
        if self._model:
            blood_model = self._model() if 1 else None
            return blood_model or None
        else:
            self._sub_model[icon_name] = weakref.ref(model)
            blood_model.bind('icon_ffa_ace', model)
            model.inherit_flag &= ~world.INHERIT_VISIBLE
            self.set_var('ZOffset', self.Z_OFFSET, model, -1)
            self.set_var('ZMax', self.Z_MAX, model, -1)
            self.set_var('ZMin', self.Z_MIN, model, -1)
            self.set_var('Scale', self.SCALE if icon_name == FFA_ICON_SMALL else self.SCALE * 2, model, -1)
            self.refresh_show_top_icon()
            return

    def on_switch_model(self, model):
        if self._model is None:
            return
        else:
            blood_ui_model = self._model()
            old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
            old_model.unbind(blood_ui_model)
            socket, bias = self._get_socket()
            model.bind(socket, blood_ui_model)
            blood_ui_model.visible = self.showing_model_ui
            blood_ui_model.inherit_flag &= ~world.INHERIT_VISIBLE
            return