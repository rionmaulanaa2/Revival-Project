# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBuffClient.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.const import PART_WEAPON_POS_MAIN2
import six
import time
import math3d
import game3d
from ..UnitCom import UnitCom
from ...cdata import mecha_status_config
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import buff_const as bconst
from logic.gcommon.common_const.attr_const import ATTR_COL_RADIUS, MECHA_WEAPON_TOTAL_ANGLE_SUB_RATE
from logic.gcommon.common_const.animation_const import FULL_BODY_NODE_NAME
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gcommon.cdata import jump_physic_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.screen_effect_utils import create_screen_effect_directly
from logic.gutils.client_unit_tag_utils import register_unit_tag, preregistered_tags
_HASH_MaskTex = game3d.calc_string_hash('MaskTex')
_HASH_Tex0 = game3d.calc_string_hash('Tex0')
_HASH_DyeColor = game3d.calc_string_hash('DyeColor')
_HASH_DyePart = game3d.calc_string_hash('DyePart')
_HASH_CHANGE_COLOR = game3d.calc_string_hash('u_change_color')
_HASH_xray_color = game3d.calc_string_hash('xray_color')
BUFF_TARGET_TAG_VALUE = register_unit_tag(('LAvatar', 'LPuppet', 'LMechaTrans'))

class ComBuffClient(UnitCom):
    BIND_EVENT = {'E_BUFF_ADD_DATA': ('on_add_buff', -999),
       'E_BUFF_ACT_DATA': ('on_act_buff', -999),
       'E_BUFF_DEL_DATA': ('on_del_buff', -999),
       'E_MODEL_LOADED': 'on_model_loaded',
       'E_HUMAN_MODEL_LOADED': 'on_human_model_loaded',
       'E_DEATH': 'on_death',
       'E_DEFEATED': 'on_death',
       'E_ON_BEING_OBSERVE': 'on_being_observe',
       'G_HAS_BUFF_BY_ID': 'has_buff_by_id',
       'G_IMMOBILIZED': 'on_immobbilized',
       'G_IS_IN_FROZEN': '_get_is_in_frozen',
       'E_UPDATE_DETECTED_MAP_LIST': 'on_update_detected_map_list',
       'E_UPDATE_DETECTED_OUTLINE_LIST': 'on_update_detected_outline_list',
       'E_ANIMATOR_LOADED': '_on_animator_loaded'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComBuffClient, self).init_from_dict(unit_obj, bdict)
        self._dye_buff_count = 0
        self._dye_part_count = [0, 0, 0]
        self._sign_buff_count = 0
        self._xray_model = None
        self._xray_model_loading_task = None
        self._immobiliz_buff_count = 0
        self._body_electricity_count = 0
        self._frozen_buff_count = 0
        self._node_scale = 1
        self._frozen_timer = None
        self._buff_count_dict = {}
        self._wait_buff = []
        self._buff_inf_ui = None
        self._grounded_ui = None
        self.fall_on_immo = False
        self.immo_left_time = 0
        if not self.sd.ref_gravity_scale:
            self.sd.ref_gravity_scale = 1.0
        if not self.sd.ref_gravity:
            self.sd.ref_gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
        self._creator = bdict.get('creator', None)
        self._infrared_detect_timer = 0
        self._infrared_detect_outline_timer = 0
        self._detected_enemies = []
        self._detected_list_map = {}
        self._detected_list_outline = {}
        return

    def on_init_complete(self):
        self.on_battle_info_ui_created()
        global_data.emgr.scene_observed_player_setted_event += (self.on_camera_target_changed,)

    def on_battle_info_ui_created(self):
        buff_data = self.ev_g_get_buff_data()
        for buff_key, buff_info in six.iteritems(buff_data):
            for buff_id, buff_data in six.iteritems(buff_info):
                for buff_idx, data in six.iteritems(buff_data):
                    self.on_add_buff(buff_key, buff_id, buff_idx, data, True)

    def on_being_observe(self, observe):
        if not observe:
            self.clear_infrared_detector()

    def has_buff_by_id(self, buff_id):
        data = self.ev_g_get_buff_data() or {}
        for buff_info in six.itervalues(data):
            if buff_info.get(buff_id):
                return True

        return False

    def is_buff_onwer(self):
        if self.sd.ref_is_agent:
            return True
        else:
            if self.is_unit_obj_type('LAvatar'):
                return global_data.player.id == self.unit_obj.id
            if self.is_unit_obj_type('LMecha'):
                if self.unit_obj.get_owner().is_share():
                    return self.sd.ref_driver_id == global_data.player.id
                if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SNATCHEGG,)):
                    if global_data.player and global_data.player.logic and global_data.cam_lplayer:
                        is_in_spec = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
                        is_in_spec = True
                        if is_in_spec:
                            return global_data.cam_lplayer.id == self._creator
                return self._creator == global_data.player.id
            if self.is_unit_obj_type('LMechaTrans'):
                return self.sd.ref_driver_id == global_data.player.id
            return False

    def on_add_buff(self, buff_key, buff_id, buff_idx, data, is_init=False):
        from logic.gcommon import time_utility
        conf = confmgr.get('c_buff_data', str(buff_id))
        if not conf:
            return
        else:
            for key, value in six.iteritems(conf.get('ExtInfo', {})):
                if key not in data:
                    data[key] = value

            sync_target = conf.get('SyncTarget', bconst.BUFF_SYNC_OWNER)
            if sync_target == bconst.BUFF_SYNC_OWNER and not self.is_buff_onwer():
                return
            overlying = False if is_init else self.ev_g_has_buff(buff_key, buff_id, buff_idx)
            add_time = data['add_time']
            left_time = None
            duration = data.get('duration', 0)
            if duration:
                left_time = add_time + duration - time_utility.get_server_time_battle()
                left_time = duration if left_time > duration else left_time
            if self.unit_obj.MASK & BUFF_TARGET_TAG_VALUE:
                self.send_event('E_GLOBAL_BUFF_ADD', buff_id, left_time, add_time, duration, data)
            else:
                data['buff_idx'] = buff_idx
                self.send_event('E_GLOBAL_MECHA_BUFF_ADD', buff_id, left_time, add_time, duration, data)
            self.send_event('E_ADD_BUFF_SFX', buff_id, data)
            handler = conf.get('BuffHandler', '')
            hdl_name = 'handle_' + handler
            handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
            data['Duration'] = duration
            if handler:
                handler(buff_id, buff_idx, data, left_time, overlying)
            data['BuffId'] = buff_id
            self.send_event('E_HANDLE_ADD_BUFF', hdl_name, data, left_time, overlying)
            return

    def on_act_buff(self, buff_key, buff_id, buff_idx, data):
        from logic.gcommon import time_utility
        conf = confmgr.get('c_buff_data', str(buff_id))
        if not conf:
            return
        else:
            for key, value in six.iteritems(conf.get('ExtInfo', {})):
                if key not in data:
                    data[key] = value

            sync_target = conf.get('SyncTarget', bconst.BUFF_SYNC_OWNER)
            if sync_target == bconst.BUFF_SYNC_OWNER and not self.is_buff_onwer():
                return
            handler = conf.get('BuffActHandler', '')
            hdl_name = 'handle_act_' + handler
            handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
            if handler:
                handler(buff_id, data)
            data['BuffId'] = buff_id
            self.send_event('E_HANDLE_ACT_BUFF', hdl_name, buff_id, data)
            return

    def on_del_buff(self, buff_key, buff_id, buff_idx):
        conf = confmgr.get('c_buff_data', str(buff_id))
        if not conf:
            return
        else:
            sync_target = conf.get('SyncTarget', bconst.BUFF_SYNC_OWNER)
            if sync_target == bconst.BUFF_SYNC_OWNER and not self.is_buff_onwer():
                return
            if self.unit_obj.MASK & BUFF_TARGET_TAG_VALUE:
                self.send_event('E_GLOBAL_BUFF_DEL', buff_id)
            else:
                self.send_event('E_GLOBAL_MECHA_BUFF_DEL', buff_id, buff_idx)
            handler = conf.get('BuffHandler', '')
            hdl_name = 'del_' + handler
            handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
            bf_data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
            if bf_data is None:
                return
            if handler:
                handler(buff_key, buff_id, buff_idx, bf_data)
            self.send_event('E_HANDLE_DEL_BUFF', hdl_name, buff_key, buff_id, buff_idx)
            if buff_id not in self._buff_count_dict or buff_id in self._buff_count_dict and self._buff_count_dict[buff_id] <= 0:
                self.send_event('E_DEL_BUFF_SFX', buff_id)
            return

    def handle_default(self, buff_id, buff_idx, buff_info, left_time, overlying):
        pass

    def del_default(self, buff_key, buff_id, buff_idx, bf_data):
        pass

    def handle_dye(self, buff_id, buff_idx, buff_info, left_time, overlying):
        import render
        if overlying:
            return
        model = self.ev_g_model()
        if not model:
            oprate = (
             self.handle_dye, (buff_info, left_time, overlying))
            self._wait_buff.append(oprate)
            return
        self._dye_buff_count += 1
        if self._dye_buff_count == 1:
            model.all_materials.set_macro('DYE_ENABLE', 'TRUE')
            model.all_materials.rebuild_tech()
            tex_path = 'character/dye_mask.tga'
            texture = render.texture(tex_path, False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
            model.all_materials.set_texture(_HASH_MaskTex, 'MaskTex', texture)
            model.all_materials.set_var(_HASH_DyeColor, 'DyeColor', (0.0, 1.0, 0.0,
                                                                     1.0))
        part_index = buff_info['part'] - 1
        self._dye_part_count[part_index] += 1
        if self._dye_part_count[part_index] == 1:
            part0 = 1.0 if self._dye_part_count[0] > 0 else 0.0
            part1 = 1.0 if self._dye_part_count[1] > 0 else 0.0
            part2 = 1.0 if self._dye_part_count[2] > 0 else 0.0
            model.all_materials.set_var(_HASH_DyePart, 'DyePart', (part0, part1, part2, 1.0))

    def del_dye(self, buff_key, buff_id, buff_idx, bf_data):
        model = self.ev_g_model()
        if not model:
            oprate = (
             self.del_dye, (buff_key, buff_id, buff_idx))
            self._wait_buff.append(oprate)
            return
        self._dye_buff_count -= 1
        if self._dye_buff_count <= 0:
            model.all_materials.set_macro('DYE_ENABLE', 'FALSE')
            model.all_materials.rebuild_tech()
            self._dye_part_count[0] = 0
            self._dye_part_count[1] = 0
            self._dye_part_count[2] = 0
            return
        conf = confmgr.get('c_buff_data', str(buff_id))
        part_index = conf['ExtInfo']['part'] - 1
        self._dye_part_count[part_index] -= 1
        if self._dye_part_count[part_index] == 0:
            part0 = 1.0 if self._dye_part_count[0] > 0 else 0.0
            part1 = 1.0 if self._dye_part_count[1] > 0 else 0.0
            part2 = 1.0 if self._dye_part_count[2] > 0 else 0.0
            model.all_materials.set_var(_HASH_DyePart, 'DyePart', (part0, part1, part2, 1.0))

    def handle_sign(self, buff_id, buff_idx, buff_info, left_time, overlying):
        import world
        from logic.gutils import dress_utils
        if global_data.player.id not in buff_info['visible_target']:
            return
        if overlying:
            return
        model = self.ev_g_model()
        if not model:
            oprate = (
             self.handle_sign, (buff_info, left_time, overlying))
            self._wait_buff.append(oprate)
            return
        self._sign_buff_count += 1
        if self._sign_buff_count == 1:
            role_id = self.ev_g_role_id()
            model_sfx_path = dress_utils.xray_model_path(role_id)
            if not self._xray_model and not self._xray_model_loading_task:
                self._xray_model_loading_task = world.create_model_async(model_sfx_path, self.load_xray_model_callback, model)

    def del_sign(self, buff_key, buff_id, buff_idx, bf_data):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        if not ('visible_target' in buff_info and global_data.player.id in buff_info['visible_target']):
            return
        else:
            model = self.ev_g_model()
            if not model:
                oprate = (
                 self.del_sign, (buff_key, buff_id, buff_idx))
                self._wait_buff.append(oprate)
                return
            self._sign_buff_count -= 1
            if self._sign_buff_count == 0:
                if self._xray_model:
                    self._xray_model.remove_from_parent()
                    self._xray_model = None
                if self._xray_model_loading_task:
                    self._xray_model_loading_task.cancel()
                    self._xray_model_loading_task = None
            return

    def load_xray_model_callback(self, xray_model, parent_model, task):
        import world
        self._xray_model_loading_task = None
        if parent_model.valid:
            self._xray_model = xray_model
            xray_model.set_parent(parent_model)
            xray_model.all_materials.set_var(_HASH_xray_color, 'xray_color', (0.73,
                                                                              0.5,
                                                                              0.14,
                                                                              1.0))
            xray_model.world_transformation = parent_model.world_transformation
            xray_model.follow_same_bone_model(parent_model)
            xray_model.set_rendergroup_and_priority(world.RENDER_GROUP_XRAY)
            xray_model.render_level = -7
            xray_model.lod_config = (500, 500)
            print('handle xray_model finish')
        else:
            xray_model.destroy()
        return

    def on_model_loaded(self, *args):
        if self._wait_buff:
            for operate in self._wait_buff:
                func = operate[0]
                args = operate[1]
                func(*args)

            self._wait_buff = []

    def on_human_model_loaded(self, model, *arg):
        if self._body_electricity_count > 0:
            self.show_emp_effect(True)

    def on_death(self, *arg):
        if self._buff_inf_ui and self._buff_inf_ui.is_valid():
            self._buff_inf_ui.close()
        if self._grounded_ui and self._grounded_ui.is_valid():
            self._grounded_ui.close()

    def handle_emp_immobilized(self, buff_id, buff_idx, buff_info, left_time, overlying):
        if not overlying:
            self._immobiliz_buff_count += 1
            self._body_electricity_count += 1
        self.show_emp_effect(True)
        is_client_owner = True if self.unit_obj and global_data.cam_lplayer and (self.unit_obj.id == global_data.cam_lplayer.id or self.sd.ref_driver_id == global_data.cam_lplayer.id) else False
        if self._immobiliz_buff_count == 1:
            status = buff_info['status']
            resule = self.ev_g_status_try_trans(status)
            self.fall_on_immo = buff_info.get('fall', True)
            self.immo_left_time = left_time
            if is_client_owner:
                self.show_buff_inf_ui(left_time, 'immobilized')
            if self.ev_g_death():
                return
            self.send_event('S_ATTR_SET', 'immo_time', left_time)
            conf = confmgr.get('c_buff_data', str(buff_id))
            handler = conf.get('BuffHandler', '')
            self.send_event('E_IMMOBILIZED', True, self.fall_on_immo, handler == 'emp_immobilized_soft')
        elif is_client_owner:
            self.show_buff_inf_ui(left_time, 'immobilized')

    def on_immobbilized(self):
        return self._immobiliz_buff_count > 0

    def del_emp_immobilized(self, buff_key, buff_id, buff_idx, bf_data):
        self._immobiliz_buff_count -= 1
        self._body_electricity_count -= 1
        if self._body_electricity_count <= 0:
            self.show_emp_effect(False)
        if self._immobiliz_buff_count == 0:
            conf = confmgr.get('c_buff_data', str(buff_id))
            status = conf['ExtInfo']['status']
            resule = self.ev_g_cancel_state(status)
            if global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id:
                self.show_buff_inf_ui(-1)
            if self.ev_g_death():
                return
            self.send_event('S_ATTR_SET', 'immo_time', 0)
            self.send_event('E_IMMOBILIZED', False)

    def show_buff_inf_ui(self, left_time, show_type=None):
        if left_time and left_time > 0 and not self._buff_inf_ui:
            self._buff_inf_ui = global_data.ui_mgr.show_ui('BuffInfoUI', 'logic.comsys.battle')
        if self._buff_inf_ui:
            self._buff_inf_ui.set_cd_time(left_time)
            show_type and self._buff_inf_ui.set_res_path(show_type)

    def handle_mecha_paralyze(self, buff_id, buff_idx, buff_info, left_time, overlying):
        resule = self.ev_g_status_try_trans(mecha_status_config.MC_PARALYZED)
        self.send_event('E_MECHA_PARALYZE', True)

    def del_mecha_paralyze(self, buff_key, buff_id, buff_idx, bf_data):
        self.ev_g_cancel_state(mecha_status_config.MC_PARALYZED)
        self.send_event('E_MECHA_PARALYZE', False)

    def handle_mecha_main_weapon_unable(self, buff_id, buff_idx, buff_info, left_time, overlying):
        from logic.gcommon.common_const.disable_bit_const import DISABLE_MAIN_WEAPON_BY_BUFF
        self.send_event('E_DISABLE_BIT_MAIN_WEAPON', DISABLE_MAIN_WEAPON_BY_BUFF, True)

    def del_mecha_main_weapon_unable(self, buff_key, buff_id, buff_idx, bf_data):
        from logic.gcommon.common_const.disable_bit_const import DISABLE_MAIN_WEAPON_BY_BUFF
        self.send_event('E_DISABLE_BIT_MAIN_WEAPON', DISABLE_MAIN_WEAPON_BY_BUFF, False)

    def handle_mecha_second_weapon_unable(self, buff_id, buff_idx, buff_data, left_time, overlying):
        if buff_data.get('regist_func'):
            return
        is_client_owner = bool(global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id)
        if is_client_owner:

            def disable_mecha_sec_weapon():
                self.send_event('E_DISABLE_SECOND_WEAPON', True)

            disable_mecha_sec_weapon()
            global_data.cam_lplayer.regist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', disable_mecha_sec_weapon)
            buff_data['regist_func'] = disable_mecha_sec_weapon

    def del_mecha_second_weapon_unable(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_DISABLE_SECOND_WEAPON', False)
        call_back_func = bf_data.get('regist_func', None)
        if call_back_func:
            global_data.cam_lplayer.unregist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', call_back_func)
        return

    def handle_mecha_speed_down(self, buff_id, buff_idx, buff_info, left_time, overlying):
        if overlying:
            return
        self.handle_speed_scale(buff_id, buff_idx, buff_info, left_time, overlying)
        if self.unit_obj == global_data.cam_lctarget:
            screen_sfx = buff_info.get('screen_sfx')
            if screen_sfx:
                create_screen_effect_directly(screen_sfx)

    def del_mecha_speed_down(self, buff_key, buff_id, buff_idx, bf_data):
        self.del_speed_scale(buff_key, buff_id, buff_idx, bf_data)

    def handle_optical_buff(self, buff_id, buff_idx, buff_info, left_time, overlying):
        self.send_event('S_SEMI_TRANSPARENT', True)

    def del_optical_buff(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('S_SEMI_TRANSPARENT', False)

    def handle_reinfore_jump(self, buff_id, buff_idx, data, left_time, overlying):
        add_factor = data.get('add_factor', 0.0)
        self.send_event('E_ENABLE_REINFORCE_JUMP', True, add_factor)

    def del_reinfore_jump(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_ENABLE_REINFORCE_JUMP', False)

    def handle_jump_factor(self, buff_id, buff_idx, data, left_time, overlying):
        if not overlying:
            self.send_event('E_JUMP_FACTOR', True, data.get('add_factor', 0.0))

    def del_jump_factor(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_JUMP_FACTOR', False, bf_data.get('add_factor', 0.0))

    def handle_all_around_speed(self, buff_id, buff_idx, data, left_time, overlying):
        self.send_event('E_START_ALL_AROUND_SPEED_BUFF', buff_id, data, left_time)

    def del_all_around_speed(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_STOP_ALL_AROUND_SPEED_BUFF')

    def handle_injury_decrease(self, buff_id, buff_idx, data, left_time, overlying):
        self.send_event('E_SHOW_INJURY_DECREASE_EFFECT', True)

    def del_injury_decrease(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_SHOW_INJURY_DECREASE_EFFECT', False)

    def handle_speed_scale(self, buff_id, buff_idx, data, left_time, overlying):
        spd_type = data.get('spd_type', None)
        if not spd_type:
            log_error('[ComBuffClient] handle_speed_scale spd_type error: %s', spd_type)
            return False
        else:
            spd_val = data.get('spd_val', None)
            if spd_val is None:
                log_error('[ComBuffClient] handle_speed_scale spd_val error: None')
                return False
            tip_id = data.get('tip_id', None)
            if tip_id:
                tip_text = get_text_by_id(tip_id, ['{}%'.format(int(spd_val * 100))])
                global_data.emgr.pve_show_buff_tips.emit(True, buff_id, tip_text)
            self.send_event('E_BUFF_SPD_ADD', buff_id, buff_idx, spd_type, spd_val, data)
            self.send_event('E_SHOW_SPEED_SCALE_INCREASE_EFFECT', True, buff_id)
            if left_time:
                self.send_event('E_SHOW_BUFF_PROGRESS', buff_id, data, left_time)
            return True

    def del_speed_scale(self, buff_key, buff_id, buff_idx, bf_data):
        tip_id = bf_data.get('tip_id', None)
        spd_val = bf_data.get('spd_val', 0)
        if tip_id:
            global_data.emgr.pve_show_buff_tips.emit(False, buff_id, '')
        self.send_event('E_BUFF_SPD_DEL', buff_id, buff_idx)
        self.send_event('E_SHOW_SPEED_SCALE_INCREASE_EFFECT', False, buff_id)
        self.send_event('E_CLOSE_BUFF_PROGRESS')
        return

    def handle_jump_speed_scale(self, buff_id, buff_idx, data, left_time, overlying):
        spd_scale = data.get('scale', 1.0)
        self.send_event('E_BUFF_JUMP_SPD_ADD', spd_scale)

    def del_jump_speed_scale(self, buff_key, buff_id, buff_idx, bf_data):
        spd_scale = -bf_data.get('scale', 1.0)
        self.send_event('E_BUFF_JUMP_SPD_ADD', spd_scale)

    def handle_speed_scale_accumulate(self, buff_id, buff_idx, data, left_time, overlying):
        if not self.handle_speed_scale(buff_id, buff_idx, data, left_time, overlying):
            return
        buff_num = self._buff_count_dict.get(buff_id, 0) + 1
        self._buff_count_dict[buff_id] = buff_num

    def del_speed_scale_accumulate(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_BUFF_SPD_DEL', buff_id, buff_idx)
        buff_num = self._buff_count_dict.get(buff_id, 0)
        if buff_num > 0:
            buff_num -= 1
        self._buff_count_dict[buff_id] = buff_num

    def handle_pve_ice(self, buff_id, buff_idx, data, left_time, overlying):
        if not self.handle_speed_scale(buff_id, buff_idx, data, left_time, overlying):
            return
        buff_num = data.get('layer_num', 1)
        self._buff_count_dict[buff_id] = buff_num
        self.send_event('E_PVE_ICE_CHANGE', buff_num)

    def del_pve_ice(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_BUFF_SPD_DEL', buff_id, buff_idx)
        self._buff_count_dict[buff_id] = 0
        self.send_event('E_PVE_ICE_CHANGE', 0)

    def handle_monster_speed_scale(self, buff_id, buff_idx, data, left_time, overlying):
        spd_val = data.get('spd_val', None)
        if spd_val is None:
            log_error('[ComBuffClient] handle_monster_speed_scale spd_val error: None')
            return False
        else:
            self.send_event('E_MONSTER_SPEED_SCALE', spd_val + 1)
            return True

    def del_monster_speed_scale(self, buff_key, buff_id, buff_idx, bf_data):
        spd_val = bf_data.get('spd_val', None)
        if spd_val is None:
            log_error('[ComBuffClient] del_monster_speed_scale spd_val error: None')
            return False
        else:
            ret_val = 1.0 / (spd_val + 1)
            self.send_event('E_MONSTER_SPEED_SCALE', ret_val)
            return True

    def handle_pve_wind_debuff(self, buff_id, buff_idx, data, left_time, overlying):
        if buff_id in self._buff_count_dict:
            self._buff_count_dict[buff_id] += 1
        else:
            self._buff_count_dict[buff_id] = 1

    def del_pve_wind_debuff(self, buff_key, buff_id, buff_idx, bf_data):
        if buff_id in self._buff_count_dict:
            self._buff_count_dict[buff_id] -= 1
        else:
            self._buff_count_dict[buff_id] = 0

    def handle_mod_bullet_col_radius(self, buff_id, buff_idx, data, left_time, overlying):
        weapon_id = data.get('weapon_id', None)
        radius_rate = data.get('col_radius', 0)
        if not radius_rate:
            return
        else:
            if not isinstance(weapon_id, (list, tuple)):
                weapon_id = [
                 weapon_id]
            for wid in weapon_id:
                self.send_event('E_MOD_ADD_ATTR', ATTR_COL_RADIUS, radius_rate, wid)

            return

    def del_mod_bullet_col_radius(self, buff_key, buff_id, buff_idx, bf_data):
        weapon_id = bf_data.get('weapon_id', None)
        radius_rate = bf_data.get('col_radius', 0)
        if not radius_rate:
            return
        else:
            if not isinstance(weapon_id, (list, tuple)):
                weapon_id = [
                 weapon_id]
            for wid in weapon_id:
                self.send_event('E_MOD_ADD_ATTR', ATTR_COL_RADIUS, -radius_rate, wid)

            return

    def handle_mod_bullet_total_angle(self, buff_id, buff_idx, data, left_time, overlying):
        weapon_id = data.get('weapon_id', None)
        sub_rate = data.get('total_angle_sub_rate', 0)
        if not isinstance(weapon_id, (list, tuple)):
            weapon_id = [
             weapon_id]
        for wid in weapon_id:
            self.send_event('E_MOD_ADD_ATTR', MECHA_WEAPON_TOTAL_ANGLE_SUB_RATE, sub_rate, wid)

        return

    def del_mod_bullet_total_angle(self, buff_key, buff_id, buff_idx, bf_data):
        weapon_id = bf_data.get('weapon_id', None)
        sub_rate = bf_data.get('total_angle_sub_rate', 0)
        if not isinstance(weapon_id, (list, tuple)):
            weapon_id = [
             weapon_id]
        for wid in weapon_id:
            self.send_event('E_MOD_ADD_ATTR', MECHA_WEAPON_TOTAL_ANGLE_SUB_RATE, -sub_rate, wid)

        return

    def handle_acc_mecha_cd(self, buff_id, buff_idx, data, left_time, overlying):
        self.send_event('E_ON_MECHA_CHARGING', True, data)

    def del_acc_mecha_cd(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_ON_MECHA_CHARGING', False, bf_data)

    def handle_add_eagle_flag(self, buff_id, buff_idx, data, *args):
        creator_id = data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            self.send_event('E_ADD_EAGLE_FLAG', creator_id, data.get('flag_type', 'eagle'), False)
        elif self.is_buff_onwer():
            self.send_event('E_ADD_EAGLE_FLAG', creator_id, data.get('flag_type', 'eagle'), True)
        elif data.get('campmate_share', 0):
            creator = EntityManager.getentity(creator_id)
            if creator and creator.logic and global_data.cam_lplayer and creator.logic.ev_g_is_campmate(global_data.cam_lplayer.ev_g_camp_id()):
                self.send_event('E_ADD_EAGLE_FLAG', creator_id, data.get('flag_type', 'eagle'), False)
        return

    def del_add_eagle_flag(self, buff_key, buff_id, buff_idx, bf_data):
        creator_id = bf_data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            self.send_event('E_DEL_EAGLE_FLAG', creator_id, False)
        elif self.is_buff_onwer():
            self.send_event('E_DEL_EAGLE_FLAG', creator_id, True)
        elif global_data.player and global_data.player.logic and (global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()):
            self.send_event('E_DEL_EAGLE_FLAG', creator_id, False)
        elif bf_data.get('campmate_share', 0):
            creator = EntityManager.getentity(creator_id)
            if creator and creator.logic and global_data.cam_lplayer and creator.logic.ev_g_is_campmate(global_data.cam_lplayer.ev_g_camp_id()):
                self.send_event('E_DEL_EAGLE_FLAG', creator_id, False)
        return

    def handle_8023_eagle(self, buff_id, buff_idx, data, *args):
        creator_id = data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            self.send_event('E_ADD_EAGLE_FLAG', creator_id, data.get('flag_type', 'eagle'), False)
            global_data.emgr.add_entity_screen_mark.emit(self.unit_obj.id, 'battle_mech/fight_hit_mech8023_mark', True)
        return

    def del_8023_eagle(self, buff_key, buff_id, buff_idx, bf_data):
        creator_id = bf_data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            self.send_event('E_DEL_EAGLE_FLAG', creator_id, False)
            global_data.emgr.del_entity_screen_mark.emit(self.unit_obj.id)
        elif global_data.player and global_data.player.logic and (global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()):
            self.send_event('E_DEL_EAGLE_FLAG', creator_id, False)
        return

    def handle_add_trace_mark(self, buff_id, buff_idx, data, *args):
        creator_id = data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            self.send_event('E_TRACE_MARK_CHANGED', creator_id, data.get('add_time', time.time()), data.get('duration', 6))
        return

    def del_add_trace_mark(self, buff_key, buff_id, buff_idx, bf_data):
        creator_id = bf_data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            self.send_event('E_TRACE_MARK_CHANGED', creator_id, 0, 0)
        return

    def handle_invincible_boost(self, buff_id, buff_idx, data, *args):
        self.send_event('E_DISABLE_SHOOT_COL')

    def del_invincible_boost(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_RESET_SHOOT_COL')

    def handle_heat_power(self, buff_id, buff_idx, data, left_time, overlying):
        self.send_event('E_ACTIVE_HEAT_SHOCK', True)

    def del_heat_power(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_ACTIVE_HEAT_SHOCK', False)

    def handle_ffa_bloodthirsty(self, *args, **kargs):
        if self.ev_g_is_cam_target():
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ARMRACE):
                msg = {'i_type': battle_const.ARMRACE_BLOODTHIRST_BUFF,'set_attr_dict': {'node_name': 'lab_1','func_name': 'SetString',
                                     'args': (
                                            get_text_by_id(17026),)
                                     }
                   }
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            else:
                msg = {'i_type': battle_const.FFA_BLOODTHIRST_BUFF,'interval_time': 20,
                   'content_txt': get_text_by_id(17027),
                   'show_num': 20,
                   'set_num_func': 'set_show_percent_num',
                   'set_attr_dict': {'node_name': 'lab_3','func_name': 'SetString',
                                     'args': (
                                            get_text_by_id(17026),)
                                     }
                   }
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def del_ffa_bloodthirsty(self, *args, **kargs):
        pass

    def handle_zombieffa_vulnerable(self, *args, **kwargs):
        pass

    def del_zombieffa_vulnerable(self, *args, **kwargs):
        pass

    def handle_gvg_bloodthirsty(self, *args, **kargs):
        if self.ev_g_is_cam_target():
            msg = {'i_type': battle_const.FFA_BLOODTHIRST_BUFF,'content_txt': get_text_by_id(17027),'show_num': 30,
               'set_num_func': 'set_show_percent_num',
               'set_attr_dict': {'node_name': 'lab_3','func_name': 'SetString',
                                 'args': (
                                        get_text_by_id(17029),)
                                 }
               }
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def del_gvg_bloodthirsty(self, *args, **kargs):
        pass

    def handle_enhance_8017_weapon(self, *args, **kwargs):
        self.send_event('E_ENHANCE_MAIN_WEAPON', True)
        from logic.gcommon.cdata.mecha_status_config import MC_FULL_FORCE_SHOOT
        self.send_event('E_SWITCH_ACTION', 'action1', MC_FULL_FORCE_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_FULL_FORCE_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_FULL_FORCE_SHOOT)

    def del_enhance_8017_weapon(self, *args, **kwargs):
        self.send_event('E_ENHANCE_MAIN_WEAPON', False)
        from logic.gcommon.cdata.mecha_status_config import MC_SHOOT
        self.send_event('E_SWITCH_ACTION', 'action1', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_SHOOT)

    def destroy(self):
        global_data.emgr.scene_observed_player_setted_event -= (self.on_camera_target_changed,)
        if self._buff_inf_ui:
            self._buff_inf_ui.close()
        if self._grounded_ui:
            self._grounded_ui.close()
        self._buff_count_dict = {}
        self.clear_infrared_detector()
        self.clear_infrared_detector_outline()
        self._clear_frozen_timer()
        super(ComBuffClient, self).destroy()

    def on_update_detected_map_list(self, detected_list_map):
        self._detected_list_map = detected_list_map
        if len(detected_list_map) > 0:
            self.start_infrared_detector()
        else:
            self.clear_infrared_detector()

    def on_update_detected_outline_list(self, detected_list_outline):
        self._detected_list_outline = detected_list_outline
        if len(detected_list_outline) > 0:
            self.start_infrared_detector_outline()
        else:
            self.clear_infrared_detector_outline()

    def start_infrared_detector(self):
        if self._infrared_detect_timer:
            return
        interval = 0.2
        times = -1
        self.detector_sound_tag = False

        def infrared_detect():
            pos_lst = []
            for eid, pos in six.iteritems(self._detected_list_map):
                vec_pos = math3d.vector(*pos)
                pos_lst.append(vec_pos)

            global_data.emgr.scene_enemy_mark.emit(pos_lst)
            if pos_lst and not self.detector_sound_tag:
                global_data.sound_mgr.post_event_2d_non_opt('Play_useitem_detector_caution', None)
                self.detector_sound_tag = True
            return

        self._infrared_detect_timer = global_data.game_mgr.register_logic_timer(infrared_detect, interval=interval, times=times, mode=2)

    def clear_infrared_detector(self):
        if self._infrared_detect_timer:
            global_data.game_mgr.unregister_logic_timer(self._infrared_detect_timer)
            self._infrared_detect_timer = 0
        self._detected_list_map = {}
        global_data.emgr.scene_enemy_mark.emit([])

    def start_infrared_detector_outline(self):
        if self._infrared_detect_outline_timer:
            return
        interval = 0.2
        times = -1
        self.detector_sound_tag = False

        def infrared_detect():
            detected_enemies = []
            for eid in six.iterkeys(self._detected_list_outline):
                entity = EntityManager.getentity(eid)
                if entity and entity.logic and entity.logic.is_valid():
                    ctrl_target = entity.logic.ev_g_control_target()
                    if ctrl_target and ctrl_target.logic and ctrl_target.logic.is_valid():
                        detected_enemies.append(ctrl_target.logic)

            for last_valid_enemy in self._detected_enemies:
                if last_valid_enemy.is_valid() and last_valid_enemy not in detected_enemies:
                    last_valid_enemy.send_event('E_ENABLE_SEE_THROUGHT', False, 'infrared_detector')

            for cur_valid_enemy in detected_enemies:
                if cur_valid_enemy.is_valid() and cur_valid_enemy not in self._detected_enemies:
                    cur_valid_enemy.send_event('E_ENABLE_SEE_THROUGHT', True, 'infrared_detector')
                    self.send_event('E_CALL_SYNC_METHOD', 'see_through_enemy', (cur_valid_enemy.id,))

            self._detected_enemies = detected_enemies

        self._infrared_detect_outline_timer = global_data.game_mgr.register_logic_timer(infrared_detect, interval=interval, times=times, mode=2)

    def clear_infrared_detector_outline(self):
        if self._infrared_detect_outline_timer:
            global_data.game_mgr.unregister_logic_timer(self._infrared_detect_outline_timer)
            self._infrared_detect_outline_timer = 0
        for enemy in self._detected_enemies:
            if enemy.is_valid():
                enemy.send_event('E_ENABLE_SEE_THROUGHT', False, 'infrared_detector')

        self._detected_enemies = []
        self._detected_list_outline = {}

    @execute_by_mode(True, (game_mode_const.GAME_MODE_SNATCHEGG,))
    def update_observe_cam_eagle_flag(self):
        if not (global_data.player and global_data.player.logic):
            return
        buffs = self.ev_g_get_buff_data() or {}
        for buff_key, buff_key_set in six.iteritems(buffs):
            for buff_id, buff_id_dict in six.iteritems(buff_key_set):
                conf = confmgr.get('c_buff_data', str(buff_id))
                handler = conf.get('BuffHandler', '')
                if handler == 'add_eagle_flag':
                    for buff_idx, buff_data in six.iteritems(buff_id_dict):
                        self.on_del_buff(buff_key, buff_id, buff_idx)
                        creator_id = buff_data.get('creator_id')
                        if creator_id == global_data.player.id:
                            continue
                        self.on_add_buff(buff_key, buff_id, buff_idx, buff_data)

    def handle_infrared_detector(self, buff_id, buff_idx, data, left_time, overlying):
        if left_time > data.get('duration', left_time + 1) - 0.5:
            control_target = self.ev_g_control_target()
            if control_target and control_target.logic:
                model = control_target.logic.ev_g_model()
                global_data.sfx_mgr.create_sfx_for_model('effect/fx/robot/common/saomiao_002.sfx', model)
                global_data.sound_mgr.post_event_2d('Play_useitem_detector', None)
        return

    def del_infrared_detector(self, buff_key, buff_id, buff_idx, bf_data):
        pass

    def handle_mecha_infrared_detector(self, buff_id, buff_idx, data, left_time, overlying):
        if left_time > data.get('duration', left_time + 1) - 0.5:
            control_target = self.ev_g_control_target()
            if control_target and control_target.logic:
                global_data.sfx_mgr.create_sfx_in_scene('effect/fx/robot/common/saomiao_002.sfx', math3d.vector(*list(data['fix_pos'])))
                global_data.sound_mgr.post_event_2d('Play_useitem_detector', None)
        return

    def del_mecha_infrared_detector(self, buff_key, buff_id, buff_idx, bf_data):
        pass

    def handle_monster_wild(self, buff_id, buff_idx, data, left_time, overlying):
        pass

    def del_monster_wild(self, buff_key, buff_id, buff_idx, bf_data):
        pass

    def handle_pve_monster_frozen(self, buff_id, buff_idx, data, left_time, overlying):
        from logic.gcommon.cdata.pve_monster_status_config import MC_FROZEN
        if self.ev_g_death():
            return
        self.ev_g_status_try_trans(MC_FROZEN)
        self._stop_animator()
        self.send_event('E_ON_FROZEN', True)

    def del_pve_monster_frozen(self, buff_key, buff_id, buff_idx, bf_data):
        from logic.gcommon.cdata.pve_monster_status_config import MC_FROZEN
        animator = self.ev_g_animator()
        if animator:
            node = animator.find(FULL_BODY_NODE_NAME)
            if node:
                node_scale = 1 if self._node_scale <= 0 else self._node_scale
                node.timeScale = node_scale
                self._node_scale = 1
        self.ev_g_cancel_state(MC_FROZEN)
        if self.ev_g_death():
            return
        self.send_event('E_ON_FROZEN', False)

    def handle_frozen(self, buff_id, buff_idx, buff_info, left_time, overlying):
        if self.ev_g_death():
            return
        else:
            if not overlying:
                self._frozen_buff_count += 1
            if self._frozen_buff_count == 1 and not overlying:
                if self.ev_g_in_mecha('Mecha') is not False:
                    status = buff_info.get('status_mecha', None)
                else:
                    status = buff_info['status_human']
                self.ev_g_status_try_trans(status)
                self._stop_animator()
                self.send_event('E_ON_FROZEN', True)
            is_client_owner = True if self.unit_obj and global_data.cam_lplayer and (self.unit_obj.id == global_data.cam_lplayer.id or self.sd.ref_driver_id == global_data.cam_lplayer.id) else False
            if is_client_owner:
                self.show_buff_inf_ui(left_time, 'frozen')
            from logic.gcommon.common_const.buff_const import BUFF_ID_PVE_FROZEN
            if buff_id == BUFF_ID_PVE_FROZEN:
                self.send_event('E_PVE_ICE_CHANGE', 999)
            return

    def del_frozen(self, buff_key, buff_id, buff_idx, bf_data):
        if self._frozen_buff_count > 0:
            self._frozen_buff_count -= 1
        if self._frozen_buff_count == 0:
            animator = self.ev_g_animator()
            if animator:
                node = animator.find(FULL_BODY_NODE_NAME)
                if node:
                    node_scale = 1 if self._node_scale <= 0 else self._node_scale
                    node.timeScale = node_scale
                    self._node_scale = 1
            conf = confmgr.get('c_buff_data', str(buff_id))
            if self.ev_g_in_mecha('Mecha') is not False:
                status = conf['ExtInfo']['status_mecha']
            else:
                status = conf['ExtInfo']['status_human']
            ret = self.ev_g_cancel_state(status)
            if global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id:
                self.show_buff_inf_ui(-1)
            if self.ev_g_death():
                return
            self.send_event('E_ON_FROZEN', False)
        from logic.gcommon.cdata import status_config
        from logic.gcommon.common_const.animation_const import STATE_SWIM
        import logic.gcommon.common_const.water_const as water_const
        current_posture_state = self.ev_g_anim_state()
        water_status = self.sd.ref_water_status
        if current_posture_state == STATE_SWIM or water_status == water_const.WATER_DEEP_LEVEL:
            self.ev_g_status_try_trans(status_config.ST_SWIM)
        from logic.gcommon.common_const.buff_const import BUFF_ID_PVE_FROZEN
        if buff_id == BUFF_ID_PVE_FROZEN:
            self.send_event('E_PVE_ICE_CHANGE', -1)

    def _stop_animator(self, *args):
        if self._frozen_buff_count <= 0:
            return
        animator = self.ev_g_animator()
        if animator:
            node = animator.find(FULL_BODY_NODE_NAME)
            if node:
                self._node_scale = node.timeScale if node.timeScale > 0 else 1
                node.timeScale = 0

    def _on_animator_loaded(self, *args):
        if self._frozen_buff_count <= 0:
            return
        self._clear_frozen_timer()
        from common.utils.timer import CLOCK
        self._frozen_timer = global_data.game_mgr.register_logic_timer(self._stop_animator, interval=1.2, times=1, mode=CLOCK)

    def _get_is_in_frozen(self):
        return self._frozen_buff_count > 0

    def _clear_frozen_timer(self):
        if self._frozen_timer:
            global_data.game_mgr.unregister_logic_timer(self._frozen_timer)
            self._frozen_timer = None
        return

    def handle_mod_mp_status(self, buff_id, buff_idx, data, *args):
        from logic.gcommon.cdata import status_config
        mod_st = status_config.desc_2_num.get(data['mod_st']) or mecha_status_config.desc_2_num.get(data['mod_st'])
        if type(data['oper_st']) == list:
            oper_st = set([ status_config.desc_2_num.get(st) or mecha_status_config.desc_2_num.get(st) for st in data['oper_st'] ])
        else:
            oper_st = status_config.desc_2_num.get(data['oper_st']) or mecha_status_config.desc_2_num.get(data['oper_st'])
        self.send_event('E_MOD_MP_ST', data['attr_map'], data['oper'], mod_st, oper_st)

    def del_mod_mp_status(self, buff_key, buff_id, buff_idx, bf_data):
        pass

    def handle_mod_skill_cd_type(self, buff_id, buff_idx, data, *args):
        cd_type = data.get('cd_type', None)
        skill_id = data.get('skill_id', 0)
        if cd_type is None or not skill_id:
            return
        else:
            self.send_event('E_UPDATE_SKILL', skill_id, {'cd_type': cd_type})
            self.send_event('E_RESET_CD_TYPE', skill_id, cd_type)
            self.send_event('E_UPDATE_SKILL_ATTR', skill_id)
            return

    def handle_8015_lightning(self, buff_id, buff_idx, data, left_time, overlying):
        self.send_event('E_SHOW_SPEED_SCALE_INCREASE_EFFECT', True, buff_id)
        pos = self.ev_g_position()
        global_data.sound_mgr.play_sound('m_8015_weapon2_lightning_strike_3p', pos)
        creator_id = data.get('creator_id')
        if creator_id:
            entity_obj = EntityManager.getentity(creator_id)
            if entity_obj and entity_obj.logic:
                mecha = entity_obj.logic.ev_g_bind_mecha_entity()
                if mecha and mecha.logic:
                    mecha.logic.send_event('E_PLAY_CAMERA_TRK', '8015_LIGHTING')
        return True

    def del_8015_lightning(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_SHOW_SPEED_SCALE_INCREASE_EFFECT', False, buff_id)

    def handle_enhance_8015_weapon(self, buff_id, buff_idx, data, left_time, overlying):
        self.send_event('E_CHANGE_ENHANCE_WEAPON_FIRE_8015', True)

    def del_enhance_8015_weapon(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_CHANGE_ENHANCE_WEAPON_FIRE_8015', False)

    def handle_emp_immobilized_soft(self, buff_id, buff_idx, buff_info, left_time, overlying):
        self.handle_emp_immobilized(buff_id, buff_idx, buff_info, left_time, overlying)

    def del_emp_immobilized_soft(self, buff_key, buff_id, buff_idx, bf_data):
        self.del_emp_immobilized(buff_key, buff_id, buff_idx, bf_data)

    def handle_electric_conduction(self, buff_id, buff_idx, buff_info, left_time, overlying):
        if not overlying:
            self._body_electricity_count += 1
        self.show_emp_effect(True)
        self.send_event('E_BODY_ELECTRIC', True)

    def del_electric_conduction(self, buff_key, buff_id, buff_idx, bf_data):
        self._body_electricity_count -= 1
        if self._body_electricity_count <= 0:
            self.show_emp_effect(False)
        self.send_event('E_BODY_ELECTRIC', False)

    def show_emp_effect(self, flag):
        self.send_event('E_SHOW_EMP_EFFECT', flag)

    def handle_thunderbolt_mark(self, buff_id, buff_idx, data, *args):
        self.handle_add_eagle_flag(buff_id, buff_idx, data, *args)
        creator_id = data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            global_data.emgr.scene_add_client_mark.emit(self.unit_obj.id, 2026, self.ev_g_position())
        return

    def del_thunderbolt_mark(self, buff_key, buff_id, buff_idx, bf_data):
        self.del_add_eagle_flag(buff_key, buff_id, buff_idx, bf_data)
        creator_id = bf_data.get('creator_id')
        if creator_id == global_data.player.id or global_data.cam_lplayer is not None and creator_id == global_data.cam_lplayer.id:
            global_data.emgr.scene_del_client_mark.emit(self.unit_obj.id)
        return

    def handle_shadow_killer(self, buff_id, buff_idx, buff_data, *args):
        pass

    def del_shadow_killer(self, buff_key, buff_id, buff_idx, bf_data):
        pass

    def handle_disable_mecha_skill(self, buff_id, buff_idx, buff_data, *args):
        if buff_data.get('regist_func'):
            return

        def disable_mecha_action():
            ctrl_entity = global_data.player.logic.ev_g_control_target()
            if not ctrl_entity or not ctrl_entity.logic:
                return
            ctrl_entity.logic.send_event('TRY_STOP_WEAPON_ATTACK')
            ctrl_entity.logic.send_event('E_SET_ACTIONS_FORBIDDEN', ['action4', 'action6'], True)

        disable_mecha_action()
        regist_event = global_data.player.logic.regist_event
        regist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', disable_mecha_action)
        regist_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE', disable_mecha_action)
        buff_data['regist_func'] = disable_mecha_action

    def del_disable_mecha_skill(self, buff_key, buff_id, buff_idx, bf_data):
        ctrl_entity = global_data.player.logic.ev_g_control_target()
        if not ctrl_entity or not ctrl_entity.logic:
            return
        else:
            ctrl_entity.logic.send_event('E_SET_ACTIONS_FORBIDDEN', ['action4', 'action6'], False)
            call_back_func = bf_data.get('regist_func', None)
            if call_back_func:
                unregist_event = global_data.player.logic.unregist_event
                unregist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', call_back_func)
                unregist_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE', call_back_func)
            return

    def handle_disable_mecha_move_skill(self, buff_id, buff_idx, buff_data, *args):
        if buff_data.get('regist_func'):
            return

        def disable_mecha_action():
            ctrl_entity = global_data.player.logic.ev_g_control_target()
            if not ctrl_entity or not ctrl_entity.logic:
                return
            ctrl_entity.logic.send_event('E_SET_ACTIONS_FORBIDDEN', ['action6'], True)

        disable_mecha_action()
        regist_event = global_data.player.logic.regist_event
        regist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', disable_mecha_action)
        regist_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE', disable_mecha_action)
        buff_data['regist_func'] = disable_mecha_action

    def del_disable_mecha_move_skill(self, buff_key, buff_id, buff_idx, bf_data):
        ctrl_entity = global_data.player.logic.ev_g_control_target()
        if not ctrl_entity or not ctrl_entity.logic:
            return
        else:
            ctrl_entity.logic.send_event('E_SET_ACTIONS_FORBIDDEN', ['action6'], False)
            call_back_func = bf_data.get('regist_func', None)
            if call_back_func:
                unregist_event = global_data.player.logic.unregist_event
                unregist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', call_back_func)
                unregist_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE', call_back_func)
            return

    def handle_disable_mecha_move_skill2(self, buff_id, buff_idx, buff_data, *args):
        if self.unit_obj.__class__.__name__ not in ('LMecha', 'LMechaRobot'):
            return
        else:
            if buff_data.get('regist_func'):
                return
            is_client_owner = bool(global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id)
            if is_client_owner:

                def disable_mecha_move_skill():
                    self.send_event('E_DISABLE_MOVE_SKILL', True)

                disable_mecha_move_skill()
                global_data.cam_lplayer.regist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', disable_mecha_move_skill)
                buff_data['regist_func'] = disable_mecha_move_skill
                cur_time = time.time()
                left_time = buff_data['duration'] - max(cur_time - buff_data['add_time'], 0)
                if not self._grounded_ui:
                    self._grounded_ui = global_data.ui_mgr.show_ui('GroundedUI', 'logic.comsys.battle')
                self._grounded_ui.set_cd_time(left_time)
            else:
                from logic.gcommon.common_const.buff_const import BUFF_ID_8034_GROUNDED
                self.send_event('E_AUTO_AIM_BY_OTHERS', True, BUFF_ID_8034_GROUNDED, None)
            return

    def del_disable_mecha_move_skill2(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_DISABLE_MOVE_SKILL', False)
        call_back_func = bf_data.get('regist_func', None)
        if call_back_func:
            global_data.cam_lplayer.unregist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', call_back_func)
        from logic.gcommon.common_const.buff_const import BUFF_ID_8034_GROUNDED
        self.send_event('E_AUTO_AIM_BY_OTHERS', False, BUFF_ID_8034_GROUNDED, None)
        is_client_owner = bool(global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id)
        if is_client_owner and self._grounded_ui:
            self._grounded_ui.set_cd_time(0)
        return

    def handle_disable_mecha_skill_by_action(self, buff_id, buff_idx, buff_data, *args):

        def disable_mecha_action():
            try:
                ctrl_entity = global_data.player.logic.ev_g_control_target()
                if not ctrl_entity or not ctrl_entity.logic:
                    return
                act_list = buff_data.get('action_list', None)
                if not act_list:
                    return
                ctrl_entity.logic.send_event('E_SET_ACTIONS_FORBIDDEN', act_list, True)
            except:
                pass

            return

        disable_mecha_action()
        regist_event = global_data.player.logic.regist_event
        regist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', disable_mecha_action)
        regist_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE', disable_mecha_action)
        buff_data['regist_func'] = disable_mecha_action

    def del_disable_mecha_skill_by_action(self, buff_key, buff_id, buff_idx, bf_data):
        ctrl_entity = global_data.player.logic.ev_g_control_target()
        if not ctrl_entity or not ctrl_entity.logic:
            return
        else:
            act_list = bf_data.get('action_list', None)
            if not act_list:
                return
            ctrl_entity.logic.send_event('E_SET_ACTIONS_FORBIDDEN', act_list, False)
            call_back_func = bf_data.get('regist_func', None)
            if call_back_func:
                unregist_event = global_data.player.logic.unregist_event
                unregist_event('E_MECHA_CONTROL_MAIN_INIT_COMPLETE', call_back_func)
                unregist_event('E_MECHA_CONTROL_MAIN_REINIT_COMPLETE', call_back_func)
            return

    def handle_gravity_scale(self, buff_id, buff_idx, data, *args):
        if self.unit_obj.MASK & preregistered_tags.HUMAN_TAG_VALUE:
            self.sd.ref_gravity_scale = data.get('human', {}).get('scale', 1.0)
            self.send_event('E_SET_FALL_CALLBACK')
        else:
            self.sd.ref_gravity_scale = data.get('mecha', {}).get('scale', 1.0)
        self.send_event('E_GRAVITY', self.sd.ref_gravity)

    def del_gravity_scale(self, buff_key, buff_id, buff_idx, bf_data):
        self.sd.ref_gravity_scale = 1.0
        if self.unit_obj.MASK & preregistered_tags.HUMAN_TAG_VALUE:
            self.send_event('E_SET_FALL_CALLBACK')
        self.send_event('E_GRAVITY', self.sd.ref_gravity)

    def handle_suicide_dash_8024(self, buff_id, buff_idx, buff_data, *args):
        self.send_event('E_MECHA_UPDATE_SUICIDE_ACTION', True)

    def del_suicide_dash_8024(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_MECHA_UPDATE_SUICIDE_ACTION', False)

    def handle_mod_magzine_conf(self, buff_key, buff_id, buff_data, *args):
        mag_key = buff_data.get('mag_key')
        conf_id = buff_data.get('conf_id', 1)
        if mag_key:
            self.send_event('E_MOD_MAGZINE_CONF', mag_key, conf_id)

    def del_mod_magzine_conf(self, buff_key, buff_id, buff_idx, bf_data):
        mag_key = bf_data.get('mag_key')
        conf_id = bf_data.get('conf_id', 1)
        if mag_key:
            self.send_event('E_MOD_MAGZINE_CONF', mag_key, 1)

    def handle_low_crystal_hp(self, buff_id, buff_idx, data, left_time, overlying):
        from logic.gutils.judge_utils import get_player_group_id
        from logic.gcommon.common_const.battle_const import ADCRYSTAL_TIP_LOW_HP_BUFF_ATK, ADCRYSTAL_TIP_LOW_HP_BUFF_DEF, MAIN_NODE_COMMON_INFO
        from logic.gcommon.common_utils.local_text import get_text_by_id
        return
        if global_data.battle and global_data.battle.get_round_status() == battle_const.ROUND_STATUS_INTERVAL:
            return
        else:
            if self.unit_obj and self.unit_obj.__class__.__name__ == 'LMecha':
                return
            low_hp = data.get('low_hp', 0)
            if global_data.battle:
                if low_hp < global_data.battle.get_last_showed_crystal_hp():
                    global_data.battle.set_last_showed_crystal_hp(low_hp)
                else:
                    return
            low_hp_str = '{}%'.format(int(low_hp * 100))
            power_up = data.get('fight_factor', 0)
            atk_group_id = data.get('atk_group_id', None)
            power_up_str = '{}%'.format(int(power_up * 100))
            if get_player_group_id() == atk_group_id:
                tip_type = ADCRYSTAL_TIP_LOW_HP_BUFF_ATK
                tip_text = get_text_by_id(17501).format(power_up_str)
            else:
                tip_type = ADCRYSTAL_TIP_LOW_HP_BUFF_DEF
                tip_text = get_text_by_id(17500).format(power_up_str)
            set_attr_dict = {'node_name': 'lab_tips',
               'func_name': 'SetString',
               'args': (
                      get_text_by_id(17498).format(low_hp_str),)
               }
            message = {'i_type': tip_type,'content_txt': tip_text,'set_attr_dict': set_attr_dict}
            message_type = MAIN_NODE_COMMON_INFO
            global_data.emgr.show_battle_main_message.emit(message, message_type)
            return

    def handle_weak_power(self, buff_id, buff_idx, buff_info, left_time, overlying):
        self.send_event('E_DEATH_DOOR_WEAK_POWER', buff_info)

    def del_weak_power(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_DEATH_DOOR_WEAK_POWER', None)
        return

    def handle_act_weak_power(self, buff_id, data):
        self.send_event('E_DEATH_DOOR_WEAK_POWER', data)

    def handle_8031_curse(self, buff_key, buff_id, buff_data, *args):
        self.send_event('E_CREATE_REAPER_CURSE_EFFECT', buff_data['mecha_fashion'])

    def handle_act_8031_curse(self, buff_id, data):
        self.send_event('E_REMOVE_REAPER_CURSE_EFFECT', data['mecha_fashion'])

    def del_8031_curse(self, buff_key, buff_id, buff_idx, bf_data):
        self.send_event('E_REMOVE_REAPER_CURSE_EFFECT', None)
        return

    def on_camera_target_changed(self, ltarget):
        if ltarget:
            if global_data.player and global_data.player.logic:
                is_in_spec = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
                if is_in_spec:
                    self.update_observe_cam_eagle_flag()

    def handle_enable_reload_shoot(self, *args):
        self.send_event('E_ENABLE_RELOAD_SHOOT', True)

    def del_enable_reload_shoot(self, *args):
        self.send_event('E_ENABLE_RELOAD_SHOOT', False)

    def handle_enable_through_shield(self, buff_key, buff_id, buff_data, left_time, *args):
        self.send_event('E_ENABLE_THROUGH_SHIELD', True, left_time, buff_data.get('duration', 5.0))

    def del_enable_through_shield(self, *args):
        self.send_event('E_ENABLE_THROUGH_SHIELD', False)

    def handle_add_weapon_custom_attr(self, buff_id, buff_idx, buff_info, left_time, overlying):
        item_ids = buff_info['item_ids']
        effect_config = buff_info['attrs']
        for id in item_ids:
            self.send_event('E_ADD_WP_CUSTOM_PARAM', None, id, effect_config)

        return

    def del_add_weapon_custom_attr(self, buff_key, buff_id, buff_idx, bf_data):
        item_ids = bf_data['item_ids']
        effect_config = bf_data['attrs']
        for id in item_ids:
            self.send_event('E_DEL_WP_CUSTOM_PARAM', None, id, effect_config)

        return

    def handle_enable_sec_jump(self, buff_key, buff_id, buff_data, left_time, *args):
        self.send_event('E_ENABLE_MULTIJUMP', True)

    def del_enable_sec_jump(self, *args):
        self.send_event('E_ENABLE_MULTIJUMP', False)

    def handle_afk_invincible(self, buff_id, buff_idx, data, *args):
        global_data.emgr.battle_afk_invincible_event.emit(True, self.unit_obj.id)

    def del_afk_invincible(self, buff_key, buff_id, buff_idx, bf_data):
        global_data.emgr.battle_afk_invincible_event.emit(False, self.unit_obj.id)
        self.send_event('E_ENABLE_THROUGH_SHIELD', False)

    def handle_lose_fuel(self, buff_id, buff_idx, buff_data, *args):
        self.send_event('E_LOSE_FUEL', buff_data['fuel_amount'], buff_data.get('affect_reg', False))
        self.send_event('E_FORBID_FUEL_RECOVER', True)

    def del_lose_fuel(self, *args):
        self.send_event('E_FORBID_FUEL_RECOVER', False)

    def handle_disable_outline_only(self, buff_id, buff_idx, buff_data, *args):
        self.sd.ref_is_covered = True
        self.send_event('E_UPDATE_CURRENT_MATERIAL_STATUS')

    def del_disable_outline_only(self, *args):
        self.sd.ref_is_covered = False
        self.send_event('E_UPDATE_CURRENT_MATERIAL_STATUS')

    def handle_pve_confuse(self, buff_id, buff_idx, data, *args):
        from logic.gcommon.common_const.buff_const import BUFF_ID_ENSLAVE
        self.send_event('E_AUTO_AIM_BY_OTHERS', True, BUFF_ID_ENSLAVE, data.get('creator_id', None))
        global_data.emgr.pve_monster_confused.emit(self.unit_obj.id, True)
        self.send_event('E_CONFUSED', True)
        return

    def del_pve_confuse(self, buff_key, buff_id, buff_index, data, *args):
        from logic.gcommon.common_const.buff_const import BUFF_ID_ENSLAVE
        self.send_event('E_AUTO_AIM_BY_OTHERS', False, BUFF_ID_ENSLAVE, data.get('creator_id', None))
        global_data.emgr.pve_monster_confused.emit(self.unit_obj.id, False)
        self.send_event('E_CONFUSED', False)
        return