# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.cocos_utils import getScreenSize
from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
from common.utils.ui_utils import get_scale
from logic.gutils import screen_utils
from common.utils.timer import CLOCK
from common.cfg import confmgr
import math3d
import cc
import math
from common.platform.device_info import DeviceInfo
from common.const import uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.hot_key_utils import get_cur_key_name_by_func_code
from logic.gcommon.common_utils import battle_utils
UIClassToModulePath = {'BagUI': 'logic.comsys.common_ui ',
   'FireRockerUI': 'logic.comsys.control_ui'
   }

class GuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_human'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'death_weapon_choose_btn_visibility_change': '_on_death_weapon_choose_btn_visibility_change'
       }

    def on_init_panel(self):
        self.locate_timer = None
        self.remote_timer = {}
        self.tips_index = 0
        self.normal_index = 0
        self.deal_info = None
        self.panel.temp_human_tips.setVisible(False)
        self.panel.temp_hint.setVisible(False)
        self.guild_blackboards = {}
        self.stop_showing_multi_human_tips = False
        self._external_req_show_death_weapon_change = False
        self.init_screen_adapt()
        width, height = self.panel.GetContentSize()
        x_fov = confmgr.get('camera_config', THIRD_PERSON_MODEL, POSTURE_STAND, 'fov', default=80)
        d = width / 2.0 / math.tan(math.radians(x_fov / 2.0))
        cell = 30
        y_fov = math.atan(cell / 2.0 / d) * 180 / math.pi * 2.0
        self.frame_scale = cell / y_fov
        if global_data.is_pc_mode:
            return
        else:
            self.on_change_ui()
            global_data.emgr.ui_change_custom_arrange_event += self.on_change_ui
            return

    def init_screen_adapt(self):
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_size = getScreenSize()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('40w'), get_scale('120w')),
           'scale_low': (
                       get_scale('220w'), get_scale('220w'))
           }

    def on_change_ui(self):
        names = [
         'MoveRockerUI', 'FireRockerUI', 'FightLeftShotUI']
        for name in names:
            ui = global_data.ui_mgr.get_ui(name)
            if ui:
                param = ui.change_ui_data()
                if isinstance(param, (list, tuple)) and len(param) == 4 and isinstance(param[3], (list, tuple)):
                    self.on_change_ui_inform_guide_layer(param[0], param[1], param[3])
                    self.on_change_ui_inform_guide(param[0], param[1], param[2])
                elif isinstance(param, (list, tuple)) and len(param) == 5 and isinstance(param[4], (list, tuple)):
                    self.on_change_ui_inform_guide_layer(param[0], param[1], param[4])
                    self.on_change_ui_inform_guide(param[0], param[1], param[2], param[3])
                else:
                    self.on_change_ui_inform_guide(*param)

        names = [
         'PickUI', 'AimRockerUI', 'HpInfoUI', 'SmallMapUI']
        for name in names:
            ui = global_data.ui_mgr.get_ui(name)
            if ui:
                param = ui.change_ui_data()
                self.on_change_ui_inform_guide_layer(*param)

        names = ['WeaponBarSelectUI', 'MechaControlMain', 'DeathWeaponChooseBtn', 'PostureControlUI', 'AttachableDriveUI', 'MechaTransUI', 'SceneInteractionUI', 'MechaUI']
        for name in names:
            ui = global_data.ui_mgr.get_ui(name)
            if not ui:
                continue
            param = ui.change_ui_data()
            scale_type_adjust_list = param.get('scale_type', [])
            for adjust_data in scale_type_adjust_list:
                self.on_change_ui_inform_guide(*adjust_data)

            pos_type_adjust_list = param.get('pos_type', [])
            for adjust_data in pos_type_adjust_list:
                self.on_change_ui_inform_guide_layer(*adjust_data)

        names = ['DrugUI']
        for name in names:
            ui = global_data.ui_mgr.get_ui(name)
            if not ui:
                continue
            pos_type_adjust_list = ui.change_ui_data()
            for adjust_data in pos_type_adjust_list:
                self.on_change_ui_inform_guide_layer(*adjust_data)

        names = ['AimRockerUI', 'HpInfoUI']
        for name in names:
            ui = global_data.ui_mgr.get_ui(name)
            if ui:
                param = ui.change_ui_data_three()
                self.on_change_ui_inform_guide(*param)

    def update_guide_ui_pos(self, node, w_pos):
        if node is None:
            return
        else:
            pos = node.getParent().convertToNodeSpace(w_pos)
            node.setPosition(pos)
            return pos

    def on_change_ui_inform_guide_layer(self, w_pos, scale, name):
        if isinstance(name, (list, tuple)):
            for node_name in name:
                layer = getattr(self.panel, node_name)
                self.update_guide_ui_pos(layer, w_pos)

        else:
            if name == 'i_guide_carrier':
                layer = self.panel.nd_carrier.i_guide_carrier.nd_carrier
            else:
                layer = getattr(self.panel, name)
            self.update_guide_ui_pos(layer, w_pos)

    def on_change_ui_inform_guide(self, w_pos, scale, name, node_name=None):
        if not isinstance(name, str):
            return
        else:
            layer = getattr(self.panel, name)
            if layer is None:
                return
            if node_name is None:
                nd_scale = layer.nd_scale
            else:
                if not isinstance(node_name, str):
                    return
                nd_scale = getattr(layer, node_name)
            pos = self.update_guide_ui_pos(nd_scale, w_pos)
            if scale:
                nd_scale.setScaleX(scale)
                nd_scale.setScaleY(scale)
                nd_pos = getattr(layer, 'nd_pos')
                if not nd_pos:
                    return
                if name in self.guild_blackboards:
                    w, h = self.guild_blackboards['nd_step_2']
                else:
                    size = nd_pos.getContentSize()
                    self.guild_blackboards['nd_step_2'] = [size.width, size.height]
                    w, h = size.width, size.height
                w = w * scale
                h = h * scale
                nd_pos.setContentSize(cc.Size(w, h))
                nd_pos.setPosition(pos)
                nd_pos.ChildResizeAndPosition()
                if name == 'nd_step_2':
                    old_sz = nd_pos.nd_tips.bar_lab.getPreferredSize()
                    new_sz = cc.Size(old_sz.width, nd_pos.nd_tips.lab_tips.getTextContentSize().height + 10)
                    nd_pos.nd_tips.bar_lab.setPreferredSize(new_sz)
            return

    def on_change_ui_inform_guide_mixed(self, adjust_dict):
        scale_type_adjust_list = adjust_dict.get('scale_type', [])
        for adjust_data in scale_type_adjust_list:
            self.on_change_ui_inform_guide(*adjust_data)

        pos_type_adjust_list = adjust_dict.get('pos_type', [])
        for adjust_data in pos_type_adjust_list:
            self.on_change_ui_inform_guide_layer(*adjust_data)

    def on_finalize_panel(self):
        if self.locate_timer:
            global_data.game_mgr.unregister_logic_timer(self.locate_timer)
            self.locate_timer = None
        if self.remote_timer:
            for ent_type in self.remote_timer:
                global_data.game_mgr.unregister_logic_timer(self.remote_timer[ent_type])

            self.remote_timer.clear()
        self.show_main_ui()
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_DESTROY_REMOTE_GUIDE')
        self.guild_blackboards.clear()
        if global_data.is_pc_mode:
            return
        else:
            global_data.emgr.ui_change_custom_arrange_event -= self.on_change_ui
            return

    def _hide_human_tips(self, index, callback):
        if index == self.tips_index:
            self.panel.temp_human_tips.setVisible(False)
            if callback:
                callback()
        if self.deal_info:
            layer = getattr(self.panel, self.deal_info[0], None)
            if layer:
                if not layer.isVisible():
                    layer.setVisible(True)
                    self.panel.PlayAnimation(self.deal_info[1])
            self.deal_info = None
        return

    def show_human_tips(self, text, time_out, cb=None):
        global_data.emgr.show_human_tips.emit(text, time_out, cb=cb)

    def do_show_human_tips(self, text, time_out, cb=None):
        self.panel.temp_human_tips.setVisible(True)
        self.panel.temp_human_tips.lab_tips.SetString(text)
        self.tips_index += 1
        self.panel.temp_human_tips.SetTimeOut(time_out, lambda i=self.tips_index, c=cb: self._hide_human_tips(i, c))

    def deal_human_tips(self, info):
        self.deal_info = info

    def show_human_tips_destroy(self):
        self.panel.temp_human_tips.setVisible(False)

    def show_multi_human_tips(self, text_list, time_out, cb=None):
        if len(text_list) <= 0:
            return
        self.panel.temp_human_tips.setVisible(True)
        self.panel.temp_human_tips.lab_tips.SetString(text_list[0])
        self.tips_index += 1
        self.panel.temp_human_tips.SetTimeOut(time_out, lambda tip_idx=self.tips_index, next_text_list=text_list[1:], next_time_out=time_out: self.hide_multi_human_tips(tip_idx, next_text_list, next_time_out))

    def hide_multi_human_tips(self, tip_index, text_list, time_out):
        if tip_index != self.tips_index:
            return
        self.panel.temp_human_tips.setVisible(False)
        if len(text_list) <= 0:
            return
        self.show_multi_human_tips(text_list, time_out)

    def show_multi_human_tips_destroy(self):
        self.stop_showing_multi_human_tips = True
        self.panel.temp_human_tips.setVisible(False)

    def show_temp_tips(self, text, time_out, cb=None):
        self.panel.temp_hint.setVisible(True)
        self.panel.temp_hint.lab_tips.SetString(text)
        self.panel.temp_hint.SetTimeOut(time_out, lambda c=cb: self.hide_temp_tips(c))

    def hide_temp_tips(self, callback):
        self.panel.temp_hint.setVisible(False)
        if callback:
            callback()

    def is_showing_temp_tips(self):
        return self.panel.temp_hint.isVisible()

    def show_temp_tips_destroy(self):
        self.panel.temp_hint.setVisible(False)

    def show_empty_tips(self, time_out, callback):
        if callback:
            self.panel.nd_empty_tips.SetTimeOut(time_out, callback)

    def show_drag_layer(self, layer_name, animation_name=None):
        layer = getattr(self.panel, layer_name, None)
        if layer:
            layer.setVisible(True)
        if animation_name:
            layer.PlayAnimation(animation_name)
        return

    def show_drag_layer_destroy(self, layer_name, animation_name=None):
        layer = getattr(self.panel, layer_name, None)
        if layer:
            layer.setVisible(False)
            if animation_name:
                layer.StopAnimation(animation_name)
        return

    def play_nd_animation(self, layer_name, animation_name, tip_text_id=None, count_down=None):
        if layer_name == 'nd_step_13':
            ui = global_data.ui_mgr.get_ui('MechaUI')
            if count_down and ui:
                ui.panel.temp_mech_call.nd_tips.setVisible(True)
                ui.panel.temp_mech_call.lab_tips.SetString(get_text_local_content(83518).format(str(count_down)))

                def refresh_time(pass_time, ui=ui, revive_time=count_down):
                    if not ui:
                        return
                    left_time = int(math.ceil(revive_time - pass_time))
                    ui.panel.temp_mech_call.lab_tips.SetString(get_text_local_content(83518).format(str(left_time)))
                    if left_time <= 0:
                        ui.StopTimerAction()
                        return

                ui.StopTimerAction()
                ui.TimerAction(refresh_time, 5, interval=1)
            else:
                self._show_mecha_call_tips(80116, play_animation=True)
            return
        else:
            layer = getattr(self.panel, layer_name, None)
            if layer:
                layer.setVisible(True)
            if layer_name == 'nd_step_3':
                if not tip_text_id:
                    tip_text_id = 80455
                self.panel.nd_step_3.nd_scale.bar_lab.lab_tips.SetString(get_text_local_content(tip_text_id))
            if animation_name:
                self.panel.PlayAnimation(animation_name)
            return

    def play_nd_animation_destroy(self, layer_name, animation_name):
        if layer_name == 'nd_step_13':
            self._hide_mecha_call_tips()
            return
        else:
            layer = getattr(self.panel, layer_name, None)
            if layer:
                layer.setVisible(False)
            if self.panel:
                self.panel.StopAnimation(animation_name)
            return

    def calc_nd_pos(self, layer, position, scale_limit):
        camera = global_data.game_mgr.scene.active_camera
        if not camera:
            return
        else:
            layer.setVisible(True)
            nd_lab = layer.nd_lab
            if nd_lab is None:
                log_error('guide ui calc_nd_pos error !!!')
                return
            is_in_screen, pos, angle = screen_utils.world_pos_to_screen_pos(nd_lab, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
            if is_in_screen:
                m_pos = global_data.player.logic.ev_g_position()
                dist = m_pos - position
                nd_lab.setPosition(pos)
                nd_lab.nd_arrows.setVisible(False)
                nd_lab.lab_text.setVisible(True)
                nd_lab.lab_distance.setVisible(True)
                nd_lab.lab_distance.SetString(str(int(dist.length / NEOX_UNIT_SCALE)))
            else:
                nd_lab.setPosition(pos)
                nd_lab.nd_arrows.setVisible(True)
                nd_lab.lab_text.setVisible(False)
                nd_lab.lab_distance.setVisible(False)
                nd_lab.nd_arrows.setRotation(-angle)
            return

    def show_locate(self, pos, offset, layer_name, animation_name=None):
        layer = getattr(self.panel, layer_name, None)
        if layer:
            layer.setVisible(True)
        if animation_name:
            layer.PlayAnimation(animation_name)
        pos = math3d.vector(*pos)
        pos.y += NEOX_UNIT_SCALE * offset
        if self.locate_timer:
            global_data.game_mgr.unregister_logic_timer(self.locate_timer)
        self.locate_timer = global_data.game_mgr.register_logic_timer(lambda n=layer, p=pos: self.calc_nd_pos(n, p, offset), interval=1)
        return

    def show_locate_destroy(self, layer_name, animation_name=None):
        layer = getattr(self.panel, layer_name, None)
        if layer:
            layer.setVisible(False)
            if animation_name:
                layer.StopAnimation(animation_name)
        if self.locate_timer:
            global_data.game_mgr.unregister_logic_timer(self.locate_timer)
            self.locate_timer = None
        return

    def update_auto_frame(self, weapon, aim_args):
        center_pos = self.panel.nd_auto_frame.center.getPosition()
        conf = weapon.conf
        pitch = conf('fAutoAimPitch', None)
        yaw = conf('fAutoAimYaw', None)
        if pitch is None or yaw is None:
            return
        else:
            pitch *= aim_args['aim_y']
            yaw *= aim_args['aim_x']
            offset_list = [
             (
              self.panel.nd_auto_frame.frame_left_up, (-yaw, pitch)),
             (
              self.panel.nd_auto_frame.frame_right_up, (yaw, pitch)),
             (
              self.panel.nd_auto_frame.frame_left_down, (-yaw, -pitch)),
             (
              self.panel.nd_auto_frame.frame_right_down, (yaw, -pitch))]
            for node, offset in offset_list:
                node.stopAllActions()
                x_offset, y_offset = offset
                pos = cc.Vec2(center_pos.x + x_offset * self.frame_scale, center_pos.y + y_offset * self.frame_scale)
                node.setPosition(pos)

            return

    def show_remote_guide_parachute(self, text_id_1, text_id_2, time_out_1, time_out_2):
        layer_drag = self.panel.temp_move_tips
        layer_drag.setVisible(True)
        layer_drag.lab_tips.SetString(get_text_local_content(text_id_1))
        layer_drag.PlayAnimation('show')

        def stage_1():
            layer_drag.setVisible(False)
            layer_move = self.panel.nd_step_2
            layer_move.setVisible(True)
            layer_move.nd_pos.nd_tips.lab_tips.SetString(get_text_local_content(text_id_2))
            old_sz = layer_move.nd_pos.nd_tips.bar_lab.getPreferredSize()
            new_sz = cc.Size(old_sz.width, layer_move.nd_pos.nd_tips.lab_tips.getTextContentSize().height)
            layer_move.nd_pos.nd_tips.bar_lab.setPreferredSize(new_sz)
            self.panel.PlayAnimation('show_2')

            def stage_2():
                layer_move.setVisible(False)

            layer_move.SetTimeOut(time_out_2, stage_2)

        layer_drag.SetTimeOut(time_out_1, stage_1)

    def show_remote_guide_move(self, text_id, time_out):
        layer = self.panel.nd_step_2
        layer.setVisible(True)
        layer.nd_pos.nd_tips.lab_tips.SetString(get_text_local_content(text_id))
        old_sz = layer.nd_pos.nd_tips.bar_lab.getPreferredSize()
        new_sz = cc.Size(old_sz.width, layer.nd_pos.nd_tips.lab_tips.getTextContentSize().height)
        layer.nd_pos.nd_tips.bar_lab.setPreferredSize(new_sz)
        self.panel.PlayAnimation('show_2')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_flight_boost_move(self, text_id, time_out):
        layer = self.panel.nd_step_2
        layer.setVisible(True)
        layer.nd_scale.nd_circle.setVisible(False)
        layer.nd_pos.nd_tips.lab_tips.SetString(get_text_local_content(text_id))
        old_sz = layer.nd_pos.nd_tips.bar_lab.getPreferredSize()
        new_sz = cc.Size(old_sz.width, layer.nd_pos.nd_tips.lab_tips.getTextContentSize().height)
        layer.nd_pos.nd_tips.bar_lab.setPreferredSize(new_sz)
        layer.nd_pos.img_hand.setVisible(not global_data.is_pc_mode)
        self.panel.PlayAnimation('show_2')

        def hide():
            layer.nd_scale.nd_circle.setVisible(True)
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_suicide_state(self, text_id, time_out):
        layer = self.panel.nd_skill_tips
        layer.setVisible(True)
        layer.nd_pos.lab_tips.SetString(get_text_local_content(text_id))
        old_sz = layer.nd_pos.lab_tips.nd_auto_fit.bar_lab.getPreferredSize()
        new_sz = cc.Size(old_sz.width, layer.nd_pos.lab_tips.getTextContentSize().height)
        layer.nd_pos.lab_tips.nd_auto_fit.bar_lab.setPreferredSize(new_sz)
        self.panel.PlayAnimation('show_skill')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def destroy_remote_guide_collect(self, *args):
        layer = self.panel.temp_hint
        layer.setVisible(False)
        global_data.player.logic.unregist_event('E_PICK_UP_SUCC', self.destroy_remote_guide_collect)

    def show_remote_guide_collect(self, text_id, time_out):
        layer = self.panel.temp_hint
        self.set_temp_hint_str(layer, text_id)
        self.panel.PlayAnimation('show_hint')
        global_data.player.logic.regist_event('E_PICK_UP_SUCC', self.destroy_remote_guide_collect)

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_guide_escape(self, text_id, time_out):
        layer = self.panel.temp_map_tips
        layer.setVisible(True)
        self.set_temp_hint_str(layer.temp_hint, text_id)
        layer.PlayAnimation('show')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_small_map_overview_tip(self, time_out):
        layer = self.panel.temp_map_tips
        layer.setVisible(True)
        layer.temp_hint.setVisible(False)
        layer.PlayAnimation('show')

        def hide():
            layer.setVisible(False)
            layer.temp_hint.setVisible(True)

        layer.SetTimeOut(time_out, hide)

    def destroy_remote_guide_mecha(self, *_):
        global_data.player.logic.unregist_event('E_GUIDE_MECHA_UI_SHOW', self.destroy_remote_guide_mecha)
        if self.panel is None:
            return
        else:
            layer = self.panel.nd_step_13
            layer.setVisible(False)
            return

    def show_remote_guide_mecha(self, text_id, time_out):
        ui = global_data.ui_mgr.get_ui('MechaSummonUI')
        if ui and ui.panel.isVisible():
            return
        layer = self.panel.nd_step_13
        layer.setVisible(True)
        layer.nd_pos.nd_lab.bar_lab.lab_tips.SetString(text_id)
        self.panel.PlayAnimation('show_13')
        global_data.player.logic.regist_event('E_GUIDE_MECHA_UI_SHOW', self.destroy_remote_guide_mecha)

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_nd_change_mode(self, text_id, time_out):
        layer = self.panel.nd_change_mode
        layer.setVisible(True)
        layer.nd_pos.nd_lab.lab_tips.SetString(text_id)
        self.panel.PlayAnimation('change_mode')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_nd_signal_tips(self, text_id, time_out):
        layer = self.panel.nd_signal_tips
        layer.setVisible(True)
        layer.nd_pos.lab_tips.SetString(text_id)

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_nd_weapon_1(self, text_id, time_out):
        layer = self.panel.nd_weapon_1
        layer.setVisible(True)
        layer.nd_pos.nd_tips.lab_tips.SetString(text_id)
        self.panel.PlayAnimation('weapon_1')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_nd_weapon_2(self, text_id, time_out):
        layer = self.panel.nd_weapon_2
        layer.setVisible(True)
        layer.nd_pos.nd_tips.lab_tips.SetString(text_id)
        self.panel.PlayAnimation('weapon_2')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_nd_weapon_3(self, text_id, time_out):
        layer = self.panel.nd_weapon_3
        layer.setVisible(True)
        layer.nd_pos.nd_tips.lab_tips.SetString(text_id)
        self.panel.PlayAnimation('weapon_3')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_temp_use_tips(self, text_id, time_out, hot_key_func_code=None):
        layer = self.panel.temp_use_tips
        layer.setVisible(True)
        layer.nd_lab.lab_tips.SetString(get_text_local_content(text_id))
        layer.PlayAnimation('show')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def hide_temp_use_tips(self):
        self.panel.temp_use_tips.setVisible(False)

    def show_temp_use_more_tips(self, w_pos):
        layer = self.panel.nd_use_small_tips
        layer.setVisible(False)
        layer = self.panel.temp_use_more_tips
        self.update_guide_ui_pos(layer, w_pos)
        from data.c_guide_data import get_remote_guide_params
        guide = 'remote_mecha_die_accelerator'
        text_id, time_out = get_remote_guide_params(guide)
        layer.setVisible(True)
        layer.nd_lab.lab_tips.SetString(get_text_local_content(text_id))
        layer.PlayAnimation('show')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_nd_use_small_tips(self, text_id, time_out):
        layer = self.panel.nd_use_small_tips
        layer.setVisible(True)
        layer.nd_lab.lab_tips.SetString(get_text_local_content(text_id))
        layer.PlayAnimation('show')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_guide_entity(self, offset, time_out, text_id, sfx, ent_type, ent):
        layer = self.panel.temp_locate
        layer.setVisible(True)
        self.panel.PlayAnimation('keep')
        tips = self.panel.temp_hint
        self.set_temp_hint_str(tips, text_id)
        self.panel.PlayAnimation('show_hint')

        def hide():
            self.show_locate_destroy('temp_locate')
            self.panel.StopAnimation('keep')
            tips.setVisible(False)
            global_data.sfx_mgr.remove_sfx(sfx)
            if ent_type in self.remote_timer:
                global_data.game_mgr.unregister_logic_timer(self.remote_timer[ent_type])
                del self.remote_timer[ent_type]

        layer.SetTimeOut(time_out, hide)
        if ent_type in self.remote_timer:
            global_data.game_mgr.unregister_logic_timer(self.remote_timer[ent_type])
        self.remote_timer[ent_type] = global_data.game_mgr.register_logic_timer(lambda n=ent, s=sfx: self.check_remote_guide_ent(n, sfx, offset, layer), interval=1)

    def check_remote_guide_ent(self, ent, sfx, offset, layer):
        if self.panel is None:
            return
        else:
            if ent and ent.logic:
                pos = ent.logic.ev_g_position()
                sfx.position = pos
                pos.y += NEOX_UNIT_SCALE * offset
                self.calc_nd_pos(layer, pos, offset)
            return

    def show_remote_guide_poison(self, text_id, time_out):
        layer = self.panel.temp_hint
        self.set_temp_hint_str(layer, text_id)
        self.panel.PlayAnimation('show_hint')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def set_temp_hint_str(self, layer, text_id):
        layer.lab_tips.SetString(get_text_local_content(text_id))
        old_width, _ = layer.bar_hint.GetContentSize()
        layer.lab_tips.formatText()
        new_sz = cc.Size(old_width, layer.lab_tips.getVirtualRendererSize().height + 30)
        layer.bar_hint.setPreferredSize(new_sz)
        layer.bar_hint.ChildResizeAndPosition()

    def show_remote_shield(self, text_id, time_out):
        layer = self.panel.nd_shield
        layer.setVisible(True)
        layer.i_guide_shield.PlayAnimation('show_shield')
        layer.i_guide_shield.bar_lab.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_carrier(self, text_id, time_out):
        layer = self.panel.nd_carrier
        layer.setVisible(True)
        layer.i_guide_carrier.PlayAnimation('show_carrier')
        layer.i_guide_carrier.nd_carrier.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_call_mecha(self, text_id, time_out):
        self.panel.setVisible(True)
        layer = self.panel.nd_mech_fuel
        layer.setVisible(True)
        layer.i_guide_mech_fuel.PlayAnimation('show_fuel')
        layer.i_guide_mech_fuel.bar_lab.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_destroy_mecha(self, text_id, time_out):
        layer = self.panel.nd_mech_destroy
        layer.setVisible(True)
        layer.i_guide_mech_destroy.PlayAnimation('show_mech')
        layer.i_guide_mech_destroy.bar_lab.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_helmet(self, text_id, time_out):
        layer = self.panel.nd_helmet
        layer.setVisible(True)
        layer.i_guide_helmet.PlayAnimation('show_helmet')
        layer.i_guide_helmet.nd_pos.nd_lab.bar_lab.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_remote_normal(self, text_id, time_out):
        layer = self.panel.temp_hint
        layer.setVisible(True)
        self.panel.PlayAnimation('show_hint')
        layer.lab_tips.SetString(get_text_local_content(text_id))
        layer.lab_tips.formatText()
        old_sz = layer.bar_hint.getPreferredSize()
        new_sz = cc.Size(old_sz.width, layer.lab_tips.getTextContentSize().height + 30)
        layer.bar_hint.setPreferredSize(new_sz)
        self.normal_index += 1

        def hide(i):
            if self.normal_index == i:
                layer.setVisible(False)

        layer.SetTimeOut(time_out, lambda i=self.normal_index: hide(i))

    def set_temp_bar_lab_str(self, bar_lab, text_id):
        bar_lab.lab_tips.SetString(get_text_local_content(text_id))
        old_width, _ = bar_lab.GetContentSize()
        bar_lab.lab_tips.formatText()
        new_sz = cc.Size(old_width, bar_lab.lab_tips.getVirtualRendererSize().height + 30)
        bar_lab.setPreferredSize(new_sz)
        bar_lab.ChildResizeAndPosition()

    DEATH_GUIDE_AUTO_HIDE_ACTION_TAG = 233

    def show_death_choose_weapon(self, text_id, time_out):
        layer = self.panel.nd_weapon_entry
        inst = global_data.ui_mgr.get_ui('DeathWeaponChooseBtn')
        if inst and inst.isPanelVisible():
            layer.setVisible(True)
        self._external_req_show_death_weapon_change = True
        bar_lab = layer.nd_pos.bar_lab
        self.set_temp_bar_lab_str(bar_lab, text_id)

        def hide():
            layer.setVisible(False)
            self._external_req_show_death_weapon_change = False

        layer.SetTimeOut(time_out, hide, tag=self.DEATH_GUIDE_AUTO_HIDE_ACTION_TAG)

    def hide_death_choose_weapon(self):
        self.stopActionByTag(self.DEATH_GUIDE_AUTO_HIDE_ACTION_TAG)
        self.panel.nd_weapon_entry.setVisible(False)
        self._external_req_show_death_weapon_change = False

    def _on_death_weapon_choose_btn_visibility_change(self, visible):
        if not self.panel or not self.panel.isValid():
            return
        wp_node = self.panel.nd_weapon_entry
        if not wp_node or not wp_node.isValid():
            return
        if visible:
            if self._external_req_show_death_weapon_change:
                wp_node.setVisible(True)
        elif not self._external_req_show_death_weapon_change:
            wp_node.setVisible(False)

    def show_death_play_rule(self, text_id, time_out, params):
        layer = self.panel.nd_top_score
        layer.setVisible(True)
        layer.i_guide_top_score.PlayAnimation('show_top_score')
        bar_lab = layer.i_guide_top_score.nd_tips.bar_lab
        self.set_temp_bar_lab_str(bar_lab, text_id)

        def hide():
            self.show_death_play_rule_detail(*params)

        layer.SetTimeOut(time_out, hide)

    def show_death_play_rule_detail(self, text_id, time_out):
        layer = self.panel.nd_top_score
        layer.setVisible(True)
        bar_lab = layer.i_guide_top_score.nd_tips.bar_lab
        self.set_temp_bar_lab_str(bar_lab, text_id)

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_death_rule_tips(self, text_id, time_out):
        layer = self.panel.nd_top_score
        layer.setVisible(True)
        layer.i_guide_top_score.PlayAnimation('show_top_score')
        bar_lab = layer.i_guide_top_score.nd_tips.bar_lab
        bar_lab.setVisible(False)

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_use_drug_tips(self, text_id, time_out):
        layer = self.panel.nd_carrier
        layer.setVisible(True)
        layer.i_guide_carrier.PlayAnimation('show_carrier')
        layer.i_guide_carrier.nd_carrier.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            if layer and layer.isValid():
                layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def hide_use_drug_tips(self):
        if self.panel.nd_carrier:
            self.panel.nd_carrier.setVisible(False)

    def show_special_call_mecha(self, text_id, time_out):
        layer = self.panel.nd_quick_call_mech
        layer.setVisible(True)
        layer.i_quick_call_mech.PlayAnimation('show_quick_call')
        layer.i_quick_call_mech.nd_lab.bar_lab.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_special_double_click(self, text_id, time_out):
        layer = self.panel.nd_double_click
        layer.setVisible(True)
        layer.i_guide_double_click.setVisible(True)
        layer.i_guide_double_click.RecordAnimationNodeState('double_click')
        layer.i_guide_double_click.PlayAnimation('double_click')
        layer.i_guide_double_click.bar_lab.lab_tips.SetString(get_text_local_content(text_id))

        def hide():
            layer.i_guide_double_click.StopAnimation('double_click')
            layer.i_guide_double_click.RecoverAnimationNodeState('double_click')
            layer.i_guide_double_click.setVisible(False)
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def hide_leave_mecha_tips(self):
        self.panel.nd_getoff_mech.setVisible(False)

    def show_get_on_skateboard_tips(self, visible, text_id=None):
        self.panel.nd_get_on_tips.setVisible(visible)
        if visible:
            if text_id is not None:
                self.panel.nd_get_on_tips.nd_pos.bar_lab.lab_tips.SetString(get_text_local_content(text_id))
            self.panel.PlayAnimation('show_get_on')
        return

    def show_get_on_chicken_tips(self, visible):
        self.panel.nd_get_on_tips_1.setVisible(visible)
        if visible:
            self.panel.PlayAnimation('show_get_on_1')

    def show_chicken_firerocker_tips(self, visible, text_id=None):
        layer = self.panel.nd_step_3
        if not layer:
            return
        else:
            layer.setVisible(visible)
            if text_id is not None and visible:
                layer.nd_scale.bar_lab.lab_tips.SetString(get_text_local_content(text_id))
            return

    def show_chicken_deformation_tips(self, visible, text_id=None):
        layer = self.panel.nd_deformation_tips
        if not layer:
            return
        else:
            layer.setVisible(visible)
            if text_id is not None and visible:
                layer.nd_pos.lab_tips.SetString(get_text_local_content(text_id))
                self.panel.PlayAnimation('show_deformation')
            return

    def set_call_mecha_tips_text(self, text_id):
        self._show_mecha_call_tips(text_id)

    def _show_mecha_call_tips(self, text_id, play_animation=False):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            ui.panel.temp_mech_call.lab_tips.SetString(get_text_local_content(text_id))
            ui.panel.temp_mech_call.nd_tips.setVisible(True)
            if play_animation:
                ui.panel.temp_mech_call.PlayAnimation('tips')

    def _hide_mecha_call_tips(self):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            ui.panel.temp_mech_call.nd_tips.setVisible(False)
            ui.panel.temp_mech_call.StopAnimation('tips')

    def show_mecha_skill_btn_ban_tips(self, visible):
        self.panel.nd_step_16.setVisible(visible)
        self.panel.nd_step_17.setVisible(visible)
        self.panel.nd_step_17.nd_pos.setVisible(False)
        self.panel.nd_step_17.nd_scale.nd_attack_tips.line.setVisible(False)
        if visible:
            self.panel.nd_step_16.nd_pos.bar_lab.lab_tips.SetString(860213)
            self.panel.PlayAnimation('show_16')
            self.panel.PlayAnimation('show_17')


class PCGuideUI(GuideUI):
    PANEL_CONFIG_NAME = 'guide/guide_pc'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    GLOBAL_EVENT = {'death_weapon_choose_btn_visibility_change': '_on_death_weapon_choose_btn_visibility_change'
       }

    def play_nd_animation(self, layer_name, animation_name, tip_text_id=None, count_down=None):
        if layer_name == 'nd_step_13':
            ui = global_data.ui_mgr.get_ui('MechaUI')
            if count_down and ui:
                ui.panel.temp_mech_call.nd_tips.setVisible(True)
                ui.panel.temp_mech_call.lab_tips.SetString(get_text_local_content(920859).format(str(count_down)))

                def refresh_time(pass_time, ui=ui, revive_time=count_down):
                    if not ui:
                        return
                    left_time = int(math.ceil(revive_time - pass_time))
                    ui.panel.temp_mech_call.lab_tips.SetString(get_text_local_content(920859).format(str(left_time)))
                    if left_time <= 0:
                        ui.StopTimerAction()
                        return

                ui.StopTimerAction()
                ui.TimerAction(refresh_time, 5, interval=1)
            else:
                self._show_mecha_call_tips(920839, play_animation=True)
            return
        if layer_name == 'nd_step_2':
            self.panel.nd_step_2.nd_pos.nd_tips.lab_tips.SetString(get_text_local_content(5113))
        else:
            if layer_name == 'nd_auto_frame':
                self.show_human_tips(5115, 3)
                return
            if layer_name == 'nd_step_5':
                layer = self.panel.temp_hint
                self.set_temp_hint_str(layer, 5116)
                self.panel.PlayAnimation('show_hint')
            else:
                if layer_name == 'nd_step_6':
                    self.panel.nd_step_6.nd_pos_weapon.lab_tips.SetString(get_text_local_content(5117))
                elif layer_name == 'nd_step_7':
                    self.show_human_tips(5118, 3)
                    return
                if layer_name == 'nd_step_8':
                    self.show_human_tips(5119, 3)
                    return
            if layer_name == 'nd_step_16':
                self.show_human_tips(5121, 3)
                return
        if layer_name == 'nd_tep_17':
            self.panel.nd_step_17.nd_attack_tips.bar_lab.lab_tips.SetString(get_text_local_content(920840))
        super(PCGuideUI, self).play_nd_animation(layer_name, animation_name, tip_text_id)

    def play_nd_animation_destroy(self, layer_name, animation_name):
        if layer_name == 'nd_step_2':
            layer_drag = self.panel.temp_move_tips
            layer_drag.setVisible(False)
        else:
            if layer_name == 'nd_auto_frame':
                self.show_human_tips_destroy()
                return
            if layer_name == 'nd_step_5':
                layer = self.panel.temp_hint
                layer.setVisible(False)
            else:
                if layer_name == 'nd_step_6':
                    pass
                elif layer_name == 'nd_step_7':
                    self.show_human_tips_destroy()
                    return
                if layer_name == 'nd_step_8':
                    self.show_human_tips_destroy()
                    return
            if layer_name == 'nd_step_16':
                self.show_human_tips_destroy()
                return
        if layer_name == 'nd_tep_17':
            pass
        super(PCGuideUI, self).play_nd_animation_destroy(layer_name, animation_name)

    def destroy_adjust_mecha_call(self, *_):
        global_data.player.logic.unregist_event('E_GUIDE_MECHA_UI_SHOW', self.destroy_adjust_mecha_call)
        self._hide_mecha_call_tips()

    def adjust_mecha_call(self, item_id, time_out):
        global_data.player.logic.regist_event('E_GUIDE_MECHA_UI_SHOW', self.destroy_adjust_mecha_call)
        self._show_mecha_call_tips(item_id, play_animation=True)

        def hide():
            self.destroy_adjust_mecha_call()

        self.panel.SetTimeOut(time_out, hide)

    def adjust_nd_weapon_1(self, item_id):
        index = -1
        wp_dict = global_data.player.logic.share_data.ref_wp_bar_mp_weapons
        if wp_dict:
            for pos, wp in six.iteritems(wp_dict):
                if wp.get_id() == item_id:
                    index = pos
                    break

        if index == -1:
            return
        else:
            ui = global_data.ui_mgr.get_ui('WeaponBarSelectUIPC')
            if ui:
                if index == 1:
                    nd = ui.panel.nd_weapon_1
                elif index == 2:
                    nd = ui.panel.nd_weapon_2
                elif index == 3:
                    nd = ui.panel.nd_weapon_3
                else:
                    nd = None
                if nd:
                    w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
                    nd = self.panel.nd_step_6.nd_pos_weapon
                    pos = nd.getParent().convertToNodeSpace(w_pos)
                    nd.setPosition(pos)
            return

    def show_nd_weapon(self, item_id, text_id, time_out):
        layer = self.panel.nd_step_6

        def show():
            self.adjust_nd_weapon_1(item_id)
            layer.nd_pos_weapon.lab_tips.SetString(get_text_local_content(text_id))
            layer.setVisible(True)
            self.panel.PlayAnimation('show_6')

        layer.SetTimeOut(1.0, show)

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out + 1.0, hide)

    def show_nd_step_18(self, text_id, time_out):
        layer = self.panel.nd_step_18
        layer.nd_attack_tips.bar_lab.lab_tips.SetString(get_text_local_content(text_id))
        layer.setVisible(True)
        self.panel.PlayAnimation('show_18')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)

    def show_temp_use_tips(self, text_id, time_out, hot_key_func_code=None):
        layer = self.panel.nd_use_tips
        layer.setVisible(True)
        self.panel.PlayAnimation('show_use_tips')
        if hot_key_func_code is not None:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            layer.nd_medicine_tips.bar_lab.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        else:
            layer.nd_medicine_tips.bar_lab.lab_tips.SetString(get_text_by_id(text_id))

        def hide():
            if layer and layer.isValid():
                layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)
        return

    def hide_temp_use_tips(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.nd_use_tips.setVisible(False)

    def show_temp_tips_pc(self, text_id, time_out, hot_key_func_code=None, cb=None):
        self.panel.temp_hint.setVisible(True)
        if hot_key_func_code is None:
            self.panel.temp_hint.lab_tips.SetString(get_text_by_id(text_id))
        else:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            self.panel.temp_hint.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        self.panel.temp_hint.SetTimeOut(time_out, lambda c=cb: self.hide_temp_tips(c))
        return

    def show_summon_mecha_tip(self, text_id, hot_key_func_code):
        self._show_mecha_call_tips(text_id, play_animation=True)
        if hot_key_func_code is not None:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            self.panel.nd_step_13.nd_pos.nd_lab.bar_lab.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        return

    def hide_summon_mecha_tip(self):
        if not self.panel or not self.panel.isValid():
            return
        self._hide_mecha_call_tips()

    def show_select_weapon_tip(self, text_id, hot_key_func_code):
        self.panel.nd_step_entry.setVisible(True)
        self.panel.PlayAnimation('show_entry')
        if hot_key_func_code is not None:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            self.panel.nd_step_entry.nd_attack_tips.bar_lab.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        return

    def hide_select_weapon_tip(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.nd_step_entry.setVisible(False)
        self.panel.StopAnimation('show_entry')

    def show_get_off_mecha_tip(self, text_id, hot_key_func_code):
        self.panel.nd_get_off_mech.setVisible(True)
        self.panel.PlayAnimation('show_get_off_mech')
        if hot_key_func_code is not None:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            self.panel.nd_get_off_mech.nd_get_off_tips.bar_lab.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        return

    def hide_get_off_mecha_tip(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.nd_get_off_mech.setVisible(False)
        self.panel.StopAnimation('show_get_off_mech')

    def hide_leave_mecha_tips(self):
        self.panel.nd_get_off_mech.setVisible(False)

    def show_move_skill_tip(self, text_id, hot_key_func_code):
        self.panel.nd_step_17.setVisible(True)
        self.panel.PlayAnimation('show_17')
        if hot_key_func_code is not None:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            self.panel.nd_step_17.nd_attack_tips.bar_lab.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        return

    def hide_move_skill_tip(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.nd_step_17.setVisible(False)
        self.panel.StopAnimation('show_17')

    def show_human_tips_pc(self, text_id, time_out, hot_key_func_code=None, cb=None):
        global_data.emgr.show_human_tips.emit(text_id, time_out, hot_key_func_code=hot_key_func_code, cb=cb)

    def do_show_human_tips_pc(self, text_id, time_out, hot_key_func_code=None, cb=None):
        self.panel.temp_human_tips.setVisible(True)
        if hot_key_func_code is None:
            self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(text_id))
        else:
            hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code)
            self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(text_id).format(hot_key_display_name))
        self.tips_index += 1
        self.panel.temp_human_tips.SetTimeOut(time_out, lambda i=self.tips_index, c=cb: self._hide_human_tips(i, c))
        return

    def show_multi_human_tips_pc(self, text_id_list, time_out, hot_key_func_code_list):
        if len(text_id_list) <= 0 or len(hot_key_func_code_list) <= 0:
            return
        else:
            self.panel.temp_human_tips.setVisible(True)
            if hot_key_func_code_list[0] is None:
                self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(text_id_list[0]))
            else:
                hot_key_display_name = get_cur_key_name_by_func_code(hot_key_func_code_list[0])
                self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(text_id_list[0]).format(hot_key_display_name))
            self.tips_index += 1
            self.panel.temp_human_tips.SetTimeOut(time_out, lambda tip_idx=self.tips_index, next_text_id_list=text_id_list[1:], next_time_out=time_out, next_hot_key_func_code_list=hot_key_func_code_list[1:]: self.hide_multi_human_tips_pc(tip_idx, next_text_id_list, next_time_out, next_hot_key_func_code_list))
            return

    def hide_multi_human_tips_pc(self, tip_index, text_id_list, time_out, hot_key_func_code_list):
        if tip_index != self.tips_index:
            return
        self.panel.temp_human_tips.setVisible(False)
        if len(text_id_list) <= 0 or len(hot_key_func_code_list) <= 0:
            return
        self.show_multi_human_tips_pc(text_id_list, time_out, hot_key_func_code_list)

    def show_multi_human_tips_pc_destroy(self):
        self.panel.temp_human_tips.setVisible(False)

    def show_mecha_skill_btn_ban_tips(self, visible):
        pass

    def show_remote_suicide_state(self, text_id, time_out):
        layer = self.panel.nd_skill_tips_pc
        layer.setVisible(True)
        layer.nd_pos.lab_tips.SetString(get_text_local_content(text_id))
        old_sz = layer.nd_pos.lab_tips.nd_auto_fit.bar_lab.getPreferredSize()
        new_sz = cc.Size(old_sz.width, layer.nd_pos.lab_tips.getTextContentSize().height)
        layer.nd_pos.lab_tips.nd_auto_fit.bar_lab.setPreferredSize(new_sz)
        self.panel.PlayAnimation('show_skill_pc')

        def hide():
            layer.setVisible(False)

        layer.SetTimeOut(time_out, hide)


class LeaveGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_finish_back_lobby'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_btn_back.btn_common.OnClick': 'on_click_btn_back'
       }

    def on_init_panel(self):
        self._count = 300
        self.panel.temp_btn_back.btn_common.SetText('')
        self.panel.temp_btn_back.btn_common.lab_btn.setVisible(True)
        self._timer = global_data.game_mgr.register_logic_timer(self.count_down, interval=1, mode=CLOCK)
        self.count_down()

    def on_finalize_panel(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def count_down(self):
        self._count -= 1
        if self._count >= 0:
            self.panel.temp_btn_back.btn_common.lab_btn.SetString(get_text_by_id(5032).format(self._count))
        else:
            self.on_close()

    def on_click_btn_back(self, *_):
        self.on_close()

    def on_close(self):
        self.close()
        global_data.player.quit_battle()