# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBloodUI.py
from __future__ import absolute_import
from __future__ import print_function
from ..UnitCom import UnitCom
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gcommon.common_const import scene_const
from logic.client.const import game_mode_const
from logic.gcommon import const
from logic.gutils import scene_utils
from common.cfg import confmgr
import weakref
import time
import world
import math3d
import game3d
import render
material_var = [
 '_XBlood', '_YBlood', '_ZBlood', '_X', '_Y', '_Z', '_TexWhite', '_TexBlue', '_TexThird', '_TexBackGround', 'Scale', '_Tex',
 '_Xinterval', '_Emptyinterval', '_IntervalScale', 'ZOffset', 'ZMax', 'ZMin', '_Alpha']
_HASH_DICT = {var:game3d.calc_string_hash(var) for var in material_var}
TEXTURE_PATH = 'model_new/others/xuetiao/'
SUB_NO_BAR = 0
SUB_ICON = 1
SUB_LV = 2
SUB_NO_H_NUM = 3
SUB_NO_L_NUM = 4
FFA_ICON_BIG = 'ffa_icon_big'
FFA_ICON_SMALL = 'ffa_icon_small'

class ComBloodUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_SHOW_HP_OVER_HEAD': '_on_show_hp_info_warpper',
       'E_HEALTH_HP_CHANGE': '_on_hp_change',
       'E_MAX_HP_CHANGED': '_on_hp_max_change',
       'G_IS_SHOWING_BLOOD_UI': '_is_showing_blood_ui',
       'E_UPDATE_BLOOD_SHADER_PARAM': 'update_shader_param'
       }
    NORMAL_HP_TEXTURE = TEXTURE_PATH + 'jijiaxueliangzhengchang.tga'
    HIT_HP_TEXTURE = TEXTURE_PATH + 'jijiaxueliangshouji.tga'
    NORMAL_BAR_TEXTURE = TEXTURE_PATH + 'xuetiaodi.tga'
    DANGER_BAR_TEXTURE = TEXTURE_PATH + 'hongxuediban.tga'
    VISIBLE_TIME = 2
    MODE_DEATH_VISIBLE_TIME = 2
    KEEP_TEX_TIME = 1.5
    MODE_DEATH_KEEP_TEX_TIME = 2.1
    DEAD_ANIMATION = True
    Z_OFFSET = -35
    Z_MAX = 1300
    Z_MIN = 300
    SCALE = 1.0

    def __init__(self):
        super(ComBloodUI, self).__init__()
        self._hp = 0
        self._hp_max = 0
        self._shield = 0
        self._shield_max = 0
        self._outer_shield = 0
        self._temporary_shield = 0
        self._in_danger = False
        self._model = None
        self._sub_model = {}
        self._change_hp_time = 0
        self._hide_time = 0
        self._fighter_id = None
        self._level = -1
        self._showing_model_ui = False
        self.showing_sim_ui = False
        self.play_dead_animation = True
        self._is_ffa_top = False
        self._ffa_top_icon_load = False
        self._hit_hp_texture = self.HIT_HP_TEXTURE
        self._danger_bar_texture = self.DANGER_BAR_TEXTURE
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBloodUI, self).init_from_dict(unit_obj, bdict)
        self._obj_type = self.unit_obj.get_owner().__class__.__name__

    def destroy(self):
        self._hit_hp_texture = None
        self._danger_bar_texture = None
        super(ComBloodUI, self).destroy()
        return

    @property
    def format_shield(self):
        return self._shield

    @property
    def format_shield_max(self):
        return self._shield_max

    def format_other_shield_max(self):
        return self._hp_max + self._shield_max + self._outer_shield + self._temporary_shield - self._hp - self._shield

    def format_other_shield(self):
        return self._outer_shield + self._temporary_shield

    def _is_showing_blood_ui(self):
        return self.showing_model_ui

    def _on_model_loaded(self, model):
        self.need_update = False
        if not model:
            return
        model_path = confmgr.get('script_gim_ref')['xuetiao']
        self.ev_g_load_model(model_path, self._blood_bar_load_callback)
        self._on_model_loaded_simui(model)

    @property
    def showing_model_ui(self):
        return self._showing_model_ui

    @showing_model_ui.setter
    def showing_model_ui(self, value):
        if self._showing_model_ui == value:
            return
        self._showing_model_ui = value
        self.refresh_show_top_icon()

    def refresh_show_top_icon(self):
        pass

    def _on_model_loaded_simui(self, model):
        pass

    def _get_socket(self):
        return ('xuetiao', 0)

    def _get_visible_time(self):
        if const.ROBOT_DEBUG:
            return 3600
        else:
            if global_data.game_mode.is_mode_type(game_mode_const.TDM_HeadBloodUI):
                return self.MODE_DEATH_VISIBLE_TIME
            return self.VISIBLE_TIME

    def _get_keep_tex_time(self):
        if global_data.game_mode.is_mode_type(game_mode_const.TDM_HeadBloodUI):
            return self.MODE_DEATH_KEEP_TEX_TIME
        else:
            return self.KEEP_TEX_TIME

    def get_blood_unit_count(self):
        return scene_const.BLOOD_UNIT

    def update_shader_param(self, param_name, idx, value):
        model = self.get_model()
        print(('test--update_shader_param--model =', model, '--param_name =', param_name, '--idx =', idx, '--value =', value))
        if not model:
            return
        self.set_var(param_name, value, model, idx)

    def _blood_bar_load_callback(self, model, *args):
        if not model:
            return
        if hasattr(model, 'set_inherit_parent_shaderctrl'):
            model.set_inherit_parent_shaderctrl(False)
        self._model = weakref.ref(model)
        obj_model = self.ev_g_model()
        socket, bias = self._get_socket()
        if obj_model:
            obj_model.bind(socket, model)
        model.inherit_flag &= ~world.INHERIT_VISIBLE
        model.position = math3d.vector(0, bias, 0)
        self.showing_model_ui = model.visible = False
        self._hp = self.ev_g_hp()
        self._hp_max = self.ev_g_max_hp()
        self._shield = self.ev_g_shield() or 0
        self._shield_max = self.ev_g_max_shield() or 0
        self._outer_shield = self.ev_g_outer_shield() or 0
        self._temporary_shield = self.ev_g_sum_temporary_shield() or 0
        self.set_texture('_TexWhite', self.NORMAL_HP_TEXTURE, model)
        self.set_var('_XBlood', self._hp, model)
        self.set_var('_X', self._hp, model)
        self.set_var('_YBlood', self.format_shield, model)
        self.set_var('_Y', self.format_shield, model)
        self.set_var('_ZBlood', self.format_other_shield(), model)
        self.set_var('_Z', self.format_other_shield_max(), model)
        self.set_var('_Xinterval', self.get_blood_unit_count(), model)
        self.set_var('_Emptyinterval', 3, model)
        self.set_var('_IntervalScale', 0.0005, model)
        self.set_var('ZOffset', self.Z_OFFSET, model, -1)
        self.set_var('ZMax', self.Z_MAX, model, -1)
        self.set_var('ZMin', self.Z_MIN, model, -1)
        self.set_var('Scale', self.SCALE, model, -1)
        self._fighter_id = self.unit_obj.sd.ref_driver_id or self.unit_obj.id
        model.set_submesh_visible(SUB_ICON, False)
        model.set_submesh_visible(SUB_LV, False)
        model.set_submesh_visible(SUB_NO_H_NUM, False)
        model.set_submesh_visible(SUB_NO_L_NUM, False)
        self._hit_hp_texture = render.texture(self.HIT_HP_TEXTURE)
        self._danger_bar_texture = render.texture(self.DANGER_BAR_TEXTURE)
        if const.ROBOT_DEBUG:
            self._on_show_hp_info_warpper()

    def _on_hp_change(self, hp, mod):
        self._hp = hp
        if self.showing_model_ui:
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                self.set_var('_XBlood', hp, model)
                self.set_var('_X', hp, model)
                self.set_var('_Z', self.format_other_shield_max(), model)
                self.check_in_danger(model)
                if mod < 0:
                    self._change_hp_time or self.set_texture('_TexWhite', self.HIT_HP_TEXTURE, model)
                self._change_hp_time = time.time() + self._get_keep_tex_time()
                if hp <= 0 and self.DEAD_ANIMATION:
                    self.set_var('_Alpha', 0, model)
                    model.set_socket_bound_obj_active('fx_end', 0, True)
        return

    def check_in_danger(self, model=None):
        in_danger = self._hp < self._hp_max * 0.25
        if self._in_danger ^ in_danger:
            self._in_danger = in_danger
            texture = self.DANGER_BAR_TEXTURE if in_danger else self.NORMAL_BAR_TEXTURE
            self.set_texture('_TexBackGround', texture, model)

    def _on_hp_max_change(self, max_hp, hp, *args):
        self._hp_max = max_hp
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            self.set_var('_XBlood', hp, model)
            self.set_var('_X', hp, model)
            self.set_var('_Z', self.format_other_shield_max(), model)
            return

    def _set_shield(self, shield, *args):
        self._shield = shield
        if self.showing_model_ui:
            self.set_var('_YBlood', self.format_shield)
            self.set_var('_Y', self.format_shield)
            self.set_var('_Z', self.format_other_shield_max())
        if shield <= 0:
            model = self._model() if self._model else None
            if model:
                model.set_socket_bound_obj_active('fx_sui', 0, True)
        return

    def _set_shield_max(self, shield_max, *args):
        self._shield_max = shield_max
        self.set_var('_Z', self.format_other_shield_max())

    def _on_outer_shield_changed(self, outer_shield_hp):
        self._outer_shield = outer_shield_hp
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            self.set_var('_ZBlood', self.format_other_shield(), model)
            self.set_var('_Z', self.format_other_shield_max(), model)
            return

    def _on_temporary_shield_changed(self, temporary_shield):
        self._temporary_shield = temporary_shield
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            self.set_var('_ZBlood', self.format_other_shield(), model)
            self.set_var('_Z', self.format_other_shield_max(), model)
            return

    def _on_show_hp_info_warpper(self):
        if self._can_show_hp_info():
            self._on_show_hp_info()

    def _can_show_hp_info(self):
        from logic.gutils import judge_utils
        if judge_utils.is_player_mark_enabled():
            return False
        if self.ev_g_defeated():
            return False
        return True

    def _on_show_hp_info(self):
        pass

    def tick(self, dt):
        if self._model:
            model = self._model() if 1 else None
            return model and model.valid or None
        else:
            if self.showing_model_ui:
                self.tick_model_ui(model)
            if self.showing_sim_ui:
                self.tick_sim_ui(model)
            if not (self.showing_model_ui or self.showing_sim_ui):
                self.need_update = False
            return

    def tick_model_ui(self, model):
        now = time.time()
        if self._hide_time and now > self._hide_time:
            model.visible = False
            self.showing_model_ui = False
            self._hide_time = 0
            if self._change_hp_time:
                self._change_hp_time = now - 1
        if self._change_hp_time and now > self._change_hp_time:
            self._change_hp_time = 0

    def tick_sim_ui(self, model):
        pass

    @execute_by_mode(False, game_mode_const.TDM_HeadBloodUI)
    def show_player_level(self):
        if self._model:
            model = self._model() if 1 else None
            return model or None
        else:
            level = self.ev_g_attr_get('driver_level') or 0
            if level == self._level:
                return
            self._level = level
            if level < 10:
                panel_H_num = level
                panel_H_tex_path = TEXTURE_PATH + 'digit_{}.tga'.format(panel_H_num)
                self.set_texture('_Tex', panel_H_tex_path, model, SUB_NO_H_NUM)
                model.set_submesh_visible(SUB_NO_L_NUM, False)
            else:
                panel_H_num = int(level / 10)
                panel_L_num = int(level % 10)
                print(level)
                print(panel_H_num, panel_L_num)
                panel_H_tex_path = TEXTURE_PATH + 'digit_{}.tga'.format(panel_H_num)
                panel_L_tex_path = TEXTURE_PATH + 'digit_{}.tga'.format(panel_L_num)
                self.set_texture('_Tex', panel_H_tex_path, model, SUB_NO_H_NUM)
                self.set_texture('_Tex', panel_L_tex_path, model, SUB_NO_L_NUM)
                model.set_submesh_visible(SUB_NO_L_NUM, True)
            return

    def set_texture(self, param_name, path, model=None, idx=SUB_NO_BAR):
        if model or self._model:
            model = self._model() if 1 else None
            if not model:
                return
        mat = model.all_materials if idx == -1 else model.get_sub_material(idx)
        mat.set_texture(_HASH_DICT[param_name], param_name, path)
        return

    def set_var(self, param_name, val, model=None, idx=SUB_NO_BAR):
        if not model:
            if self._model:
                model = self._model() if 1 else None
            return model and model.valid or None
        else:
            mat = model.all_materials if idx == -1 else model.get_sub_material(idx)
            mat.set_var(_HASH_DICT[param_name], param_name, float(val))
            return

    def get_var(self, param_name, model, idx=SUB_NO_BAR):
        mat = idx == -1 and model.all_materials if 1 else model.get_sub_material(idx)
        return mat.get_var(param_name)

    def get_model(self):
        if self._model:
            return self._model()
        else:
            return None

    def get_sub_model(self, name):
        if name not in self._sub_model:
            return None
        else:
            return self._sub_model[name]()

    def _is_teammate(self, cam_player):
        controller_eid = self.sd.ref_driver_id if self.sd.ref_is_mecha else self.unit_obj.id
        if cam_player and cam_player.ev_g_is_groupmate(controller_eid):
            return True
        return False