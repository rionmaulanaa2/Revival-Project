# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanBloodUI.py
from __future__ import absolute_import
import math3d
import world
import render
from ..UnitCom import UnitCom
from logic.gutils import template_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.component.client.ComBloodUI import ComBloodUI, SUB_LV, SUB_ICON, SUB_NO_L_NUM, SUB_NO_H_NUM
from logic.gcommon.common_const.animation_const import STATE_SQUAT, STATE_CRAWL, STATE_SQUAT_HELP, STATE_SWIM, STATE_ROLL, STATE_JUMP
import weakref
import time
from common.uisys.font_utils import GetMultiLangFontFaceName
from common.cfg import confmgr
TEXTURE_PATH = 'model_new/others/xuetiao/'
FFA_ICON_BIG = 'ffa_icon_big'
FFA_ICON_SMALL = 'ffa_icon_small'

class ComHumanBloodUI(ComBloodUI):
    BIND_EVENT = ComBloodUI.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SET_CONTROL_TARGET': '_set_control_target',
       'E_AGONY': '_on_agony',
       'E_ON_SAVED': '_on_saved',
       'E_REVIVE': '_on_saved',
       'E_AGONY_HP': 'on_agony_hp_change',
       'E_SWITCH_STATUS': 'on_switch_animation',
       'E_SET_SHIELD': '_set_shield',
       'E_SET_SHIELD_MAX': '_set_shield_max',
       'E_SET_TEMPORARY_SHIELD': ('on_set_temporary_shield', 100),
       'G_GET_SOCKET': '_get_socket'
       })
    NORMAL_HP_TEXTURE = TEXTURE_PATH + 'jijiaxueliangshouji.tga'
    VISIBLE_TIME = 1
    MODE_DEATH_VISIBLE_TIME = 2
    KEEP_TEX_TIME = 0.5
    MODE_DEATH_KEEP_TEX_TIME = 2.1
    DEAD_ANIMATION = False
    Z_OFFSET = -12
    Z_MAX = 910
    Z_MIN = 100
    Z_AIM_MIN = 300
    SCALE = 0.35
    STATE_TO_BIAS = {STATE_JUMP: 6,
       STATE_SQUAT: -7,
       STATE_ROLL: -5,
       STATE_CRAWL: -6,
       STATE_SQUAT_HELP: -6,
       STATE_SWIM: 6
       }

    def __init__(self):
        super(ComHumanBloodUI, self).__init__()
        self.force_hide = False
        self._is_in_agony = False
        self._target_bias = 0
        self._cur_bias = 0
        self._agony_dirty = False
        self._agony_hp = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanBloodUI, self).init_from_dict(unit_obj, bdict)
        self.init_ui_event()

    def init_ui_event(self):
        global_data.emgr.ui_enter_aim += self._try_aim
        global_data.emgr.ui_leave_aim += self._quit_aim

    def _blood_bar_load_callback(self, model, *args):
        super(ComHumanBloodUI, self)._blood_bar_load_callback(model, *args)
        self.show_capacity(model)

    def show_capacity(self, model):
        if not global_data.game_mode:
            return
        if G_IS_NA_PROJECT and not global_data.game_mode.is_mode_type(game_mode_const.Hide_HeadCapacity) or global_data.game_mode.is_neutral_shop_env():
            model.set_submesh_visible(SUB_ICON, True)
            model.set_submesh_visible(SUB_LV, True)
            model.set_submesh_visible(SUB_NO_H_NUM, True)
            model.set_submesh_visible(SUB_NO_L_NUM, True)

    def on_init_complete(self):
        self.process_armrace_event(True)

    def _get_socket(self):
        return ('s_xuetiao', 0)

    def tick(self, dt):
        super(ComHumanBloodUI, self).tick(dt)
        self.show_player_level()

    def tick_model_ui(self, model):
        super(ComHumanBloodUI, self).tick_model_ui(model)
        if not self.showing_model_ui:
            return
        delta = self._target_bias - self._cur_bias
        if delta == 0:
            return
        if delta > 0:
            self._cur_bias += 1
        else:
            self._cur_bias -= 1
        model.position = math3d.vector(0, self._cur_bias, 0)

    def _try_aim(self, *args):
        model = self.get_model()
        if not model:
            return
        self.set_var('ZMin', self.Z_AIM_MIN, model, -1)

    def _quit_aim(self, *args):
        model = self.get_model()
        if not model:
            return
        self.set_var('ZMin', self.Z_MIN, model, -1)

    def _on_show_hp_info(self):
        if self.force_hide:
            return
        else:
            if not global_data.cam_lplayer or self.unit_obj.id == global_data.cam_lplayer.id:
                return
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                self.showing_model_ui or self.set_hp_shield()
                self.check_in_danger(model)
                anim_state = self.ev_g_anim_state()
                self.on_switch_animation(anim_state)
                if self._cur_bias != self._target_bias:
                    self._cur_bias = self._target_bias
                    model.position = math3d.vector(0, self._cur_bias, 0)
                self.showing_model_ui = model.visible = True
                self.need_update = True
            self._hide_time = time.time() + self._get_visible_time()
            return

    def set_hp_shield(self):
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            cur_hp = 0.0
            max_hp = 0.0
            cur_shield = 0.0
            max_shield = 0.0
            _shield_max = self._shield_max + self._temporary_shield
            _shield = self._shield + self._temporary_shield
            if _shield_max <= 0 or _shield <= 0:
                cur_hp = self.get_show_hp()
                max_hp = self._hp_max
            elif self._hp + _shield < self._hp_max:
                cur_hp = self.get_show_hp()
                max_hp = self._hp
                cur_shield = _shield
                max_shield = self._hp_max - self._hp
            else:
                cur_hp = self.get_show_hp()
                max_hp = cur_hp
                cur_shield = _shield
                max_shield = cur_shield
            self.set_var('_XBlood', cur_hp, model)
            self.set_var('_X', max_hp, model)
            self.set_var('_YBlood', cur_shield, model)
            self.set_var('_Y', max_shield, model)
            self.set_var('_ZBlood', 0, model)
            self.set_var('_Z', 0, model)
            return

    def _set_shield(self, shield, *args):
        self._shield = shield
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            self.set_hp_shield()
            return

    def _set_shield_max(self, shield_max, *args):
        self._shield_max = shield_max
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            self.set_hp_shield()
            return

    def _on_hp_change(self, hp, mod):
        self._hp = hp
        if self.showing_model_ui:
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                self.set_hp_shield()
                self.check_in_danger(model)
                if mod < 0:
                    self._change_hp_time or self.set_texture('_TexWhite', self.HIT_HP_TEXTURE, model)
                self._change_hp_time = time.time() + self._get_keep_tex_time()
                if hp <= 0 and self.DEAD_ANIMATION:
                    self.set_var('_Alpha', 0, model)
                    model.set_socket_bound_obj_active('fx_end', 0, True)
        return

    def check_in_danger(self, model=None):
        in_danger = self._hp < self._hp_max * 0.25 or self._is_in_agony
        if self._in_danger ^ in_danger:
            self._in_danger = in_danger
            texture = self.DANGER_BAR_TEXTURE if in_danger else self.NORMAL_BAR_TEXTURE
            self.set_texture('_TexBackGround', texture, model)

    def get_show_hp(self):
        if self._is_in_agony:
            return self._agony_hp
        else:
            return self._hp

    def set_hp_shield(self):
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            cur_hp = 0.0
            max_hp = 0.0
            cur_shield = 0.0
            max_shield = 0.0
            if self._shield_max <= 0 or self._shield <= 0:
                cur_hp = self._hp
                max_hp = self._hp_max
            elif self._hp + self._shield < self._hp_max:
                cur_hp = self._hp
                max_hp = self._hp
                cur_shield = self._shield
                max_shield = self._hp_max - self._hp
            else:
                cur_hp = self._hp
                max_hp = cur_hp
                cur_shield = self._shield
                max_shield = cur_shield
            self.set_var('_XBlood', cur_hp, model)
            self.set_var('_X', max_hp, model)
            self.set_var('_YBlood', cur_shield, model)
            self.set_var('_Y', max_shield, model)
            self.set_var('_ZBlood', 0, model)
            self.set_var('_Z', 0, model)
            return

    def _on_hp_change(self, hp, mod):
        self._hp = hp
        if self.showing_model_ui:
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                self.set_hp_shield()
                self.check_in_danger(model)
                if mod < 0:
                    self._change_hp_time or self.set_texture('_TexWhite', self.HIT_HP_TEXTURE, model)
                self._change_hp_time = time.time() + self._get_keep_tex_time()
                if hp <= 0 and self.DEAD_ANIMATION:
                    self.set_var('_Alpha', 0, model)
                    model.set_socket_bound_obj_active('fx_end', 0, True)
        return

    def on_switch_animation(self, status, is_sync=True):
        self._target_bias = self.STATE_TO_BIAS.get(status, 0)

    def hide_hp(self):
        self.force_hide = True
        if self.showing_model_ui:
            self._hide_time = time.time() - 1
            self.tick(0)

    def _on_saved(self):
        self.force_hide = False
        self._is_in_agony = False
        self._agony_dirty = False

    def _set_control_target(self, target, *args):
        if target:
            self.hide_hp()
            self._on_join_mecha()
        else:
            self.force_hide = False
            self._on_leave_mecha()

    def _on_join_mecha(self, *args, **kargs):
        self.showing_sim_ui = False

    def _on_leave_mecha(self, *args, **kargs):
        pass

    def destroy(self):
        self.process_armrace_event(False)
        super(ComHumanBloodUI, self).destroy()

    def on_agony_hp_change(self, hp):
        self._agony_hp = hp
        if self.showing_model_ui:
            if self._model:
                model = self._model() if 1 else None
                return model or None
            self.set_var('_XBlood', hp, model)
            self.set_var('_X', hp, model)
            self.set_var('_Y', max(self._hp_max - hp, 0), model)
            self.check_in_danger(model)
            if self._agony_dirty:
                self.set_texture('_TexWhite', self.HIT_HP_TEXTURE, model)
                self._agony_dirty = False
            self._change_hp_time = 0
        return

    def _on_agony(self):
        self._is_in_agony = True
        self._agony_hp = self.ev_g_agony_hp()
        self._agony_dirty = True

    def on_set_temporary_shield(self, temporary_shield_map):
        temporary_shield = self.ev_g_sum_temporary_shield()
        self._on_temporary_shield_changed(temporary_shield)

    def _on_temporary_shield_changed(self, temporary_shield):
        self._temporary_shield = temporary_shield
        self.set_hp_shield()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_ARMRACE,))
    def process_armrace_event(self, is_init):
        if is_init:
            global_data.emgr.update_top_group_info += self._update_top_group_info
            self._update_top_group_info()
        else:
            global_data.emgr.update_top_group_info -= self._update_top_group_info
            self._update_top_group_info()

    def _update_top_group_info(self, *args):
        player_eid = self.unit_obj.id
        if self.sd.ref_is_mecha:
            player_eid = self.sd.ref_driver_id
        battle_data = global_data.armrace_battle_data
        self._is_ffa_top = battle_data.is_top_1(player_eid) if battle_data else False
        self.refresh_show_top_icon()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_ARMRACE,))
    def refresh_show_top_icon(self):
        model = self.get_model()
        if not (model and model.valid):
            return
        big_icon_model = self.get_sub_model(FFA_ICON_BIG)
        small_icon_model = self.get_sub_model(FFA_ICON_SMALL)
        is_teammate = self._is_teammate(global_data.cam_lplayer)
        if big_icon_model:
            big_icon_model.visible = self._is_ffa_top and not self.showing_model_ui and not is_teammate and self.ev_g_healthy()
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