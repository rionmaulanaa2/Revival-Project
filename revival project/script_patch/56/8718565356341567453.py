# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FrontSightUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.cfg import confmgr
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import neox_pos_to_cocos
import game3d
import time
from common.const import uiconst
import cc
from logic.gcommon.common_const import weapon_const
import math

class FrontSightUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/front_sight'
    DLG_ZORDER = BASE_LAYER_ZORDER
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}
    AUTO_AIM_SIZE = 140.0
    SCALE_1 = 60 / AUTO_AIM_SIZE
    SCALE_2 = 80 / AUTO_AIM_SIZE
    FIRE_POS_COLLISION_TAG = 0

    def on_init_panel(self):
        for child in self.panel.zhunxin.GetChildren():
            child.SetEnableCascadeColorRecursion(True)

        self.panel.zhunxin.point.SetEnableCascadeColorRecursion(False)
        self.panel.zhunxin.normal.SetEnableCascadeColorRecursion(False)
        self.panel.zhunxin.nd_remaining_curve.SetEnableCascadeColorRecursion(False)
        self.panel.zhunxin.nd_remaining_line.SetEnableCascadeColorRecursion(False)
        self._cur_zhunxin = None
        self._zhunxin_key = None
        self._auto_aim_range = 10
        self._auto_aim_distance = 0
        self.is_player_first_setted = True
        self._auto_aim_pnl = self.panel.zhunxin.auto
        self._auto_aim_pnl_visible = False
        self._aim_auto_move = False
        self._is_free_camera_state = False
        self.shake_scale = False
        self._silence_auto_aim = False
        self.lmg_scale_range = []
        self._lmg_timer = 0
        self.lmg_cur_offset = 0
        self.lmg_target_offset = 0
        self.lmg_force_timer = False
        self.panel.zhunxin.SetEnableCascadeOpacityRecursion(True)
        self._aim_pnl = self.panel.zhunxin.aim_pnl
        self._aim_target = None
        self._is_aim_on_target = False
        from common.cfg import confmgr
        from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
        import math
        width, height = self.panel.GetContentSize()
        x_fov = confmgr.get('camera_config', THIRD_PERSON_MODEL, POSTURE_STAND, 'fov', default=80)
        self.cnt_yaw = 0
        self.cnt_pitch = 0
        self._lock_time = 3
        d = width / 2.0 / math.tan(math.radians(x_fov / 2.0))
        cell = 30
        y_fov = math.atan(cell / 2.0 / d) * 180 / math.pi * 2.0
        self._scale_value = cell / y_fov
        self.cur_auto_aim_scale_target = None
        self.cur_sec_auto_aim_scale_target = None
        self.last_pos = None
        self._spectate = False
        self._firegun_delay_hid = None
        self._aim_normal_color = '#SW'
        fire_aim_style_conf = confmgr.get('fire_aim_style', default={})
        self._aim_anim_dict = {}
        for zhunxin_key, aim_conf in six.iteritems(fire_aim_style_conf):
            if zhunxin_key != '__doc__':
                self._aim_anim_dict[zhunxin_key] = aim_conf['anim']
                self.panel.zhunxin.RecordAnimationNodeState(aim_conf['anim'])

        self._aim_bullet_style = None
        self.init_event()
        return

    def init_event(self):
        self.player = None
        player = None
        if global_data.player:
            player = global_data.player.logic
        self.panel.setVisible(False)
        spectate_target = None
        if player:
            spectate_target = player.ev_g_spectate_target()
            self._spectate = player.ev_g_is_in_spectate()
        if spectate_target and spectate_target.logic:
            self._on_scene_camera_target_setted(spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        emgr = global_data.emgr
        econf = {'switch_to_aim_camera_event': self._switch_to_aim_camera,
           'switch_to_last_camera_state_event': self._switch_to_last_camera_state,
           'scene_player_setted_event': self.on_player_setted,
           'scene_camera_target_setted_event': self._on_set_scene_camera_target,
           'on_observer_aim_spread_changed': self._on_spread,
           'camera_switch_to_state_event': self.on_camera_state_change,
           'change_aim_color_event': self.on_update_aim_color,
           'on_observer_weapon_bullet_num_changed': self.on_weapon_bullet_num_changed
           }
        emgr.bind_events(econf)
        self.init_visible_event()
        return

    def on_update_aim_color(self):
        if global_data.player:
            from logic.gcommon.common_const import ui_operation_const as uoc
            cur_color_val = global_data.player.get_setting(uoc.AIM_COLOR_VAL)
            self._aim_normal_color = cur_color_val
            for child in self.panel.zhunxin.GetChildren():
                child.SetColor(self._aim_normal_color)

            self.update_normal_circle_color()

    def close_auto_aim(self):
        if self._auto_aim_pnl_visible:
            self.panel.zhunxin.PlayAnimation('disappear_auto')

        def _cc_init_auto_aim():
            self.init_auto_aim(True)

        self.panel.zhunxin.SetTimeOut(0.3, _cc_init_auto_aim)

    def init_auto_aim(self, init=False):
        if not self.panel:
            return
        else:
            if self._spectate:
                self._auto_aim_pnl_visible = False
                self._auto_aim_pnl.setVisible(False)
                return
            if global_data.is_pc_mode:
                if self.player:
                    weapon = self.player.share_data.ref_wp_bar_cur_weapon if 1 else None
                    if weapon:
                        kind = weapon.get_kind()
                        from logic.gcommon.common_const.weapon_const import HUMAN_BAN_AUTO_AIM_IN_PC_MODE_WP_TYPE_SET
                        if kind in HUMAN_BAN_AUTO_AIM_IN_PC_MODE_WP_TYPE_SET:
                            if self.player and not self.player.ev_g_auto_aim_open_value() if 1 else True:
                                self._auto_aim_pnl_visible = False
                                self._auto_aim_pnl.setVisible(False)
                                return
                    self._auto_aim_pnl_visible = False
                    self._auto_aim_pnl.setVisible(False)
                    scale = self._scale_value
                    return self.player or None
                weapon = self.player.share_data.ref_wp_bar_cur_weapon
                aim_args = self.player.ev_g_at_aim_args_all()
                is_in_aim = self.player.sd.ref_in_aim
                if not weapon or not aim_args or is_in_aim:
                    return
                conf = weapon.conf
                pitch = conf('fAutoAimPitch', None)
                yaw = conf('fAutoAimYaw', None)
                distance = conf('fAutoAimDistance', 0)
                from logic.gcommon.common_const.weapon_const import AUTO_AIM_WEAPON_LIST
                if pitch is None or yaw is None:
                    return
                force_aim_kind = conf('iForceAutoAimKind', None)
                if force_aim_kind == 0:
                    return
                if force_aim_kind is None and conf('iKind') not in AUTO_AIM_WEAPON_LIST:
                    return
                from math import radians, sqrt
                self._auto_aim_range = radians(sqrt(yaw * yaw + pitch * pitch))
                self._auto_aim_pnl_visible = True
                self._silence_auto_aim or self._auto_aim_pnl.setVisible(True)
            from common.cfg import confmgr
            self._lock_time = confmgr.get('navigate_config', str(weapon.iType), 'fTimeLock', default=3)
            pitch *= aim_args['aim_y']
            yaw *= aim_args['aim_x']
            self._auto_aim_distance = int(distance * aim_args['aim_r'])
            zhunxin = self.panel.zhunxin
            center_pos = self._auto_aim_pnl.frame.center.getPosition()
            offset_list = [
             (
              zhunxin.frame_left_up, (-yaw, pitch)),
             (
              zhunxin.frame_right_up, (yaw, pitch)),
             (
              zhunxin.frame_left_down, (-yaw, -pitch)),
             (
              zhunxin.frame_right_down, (yaw, -pitch)),
             (
              zhunxin.frame_left, (-yaw, 0)),
             (
              zhunxin.frame_right, (yaw, 0))]
            import cc
            init_scale = scale * 0.4
            for node, offset in offset_list:
                node.stopAllActions()
                x_offset, y_offset = offset
                if init:
                    node.SetPosition(center_pos.x + x_offset * init_scale, center_pos.y + y_offset * init_scale)
                pos = cc.Vec2(center_pos.x + x_offset * scale, center_pos.y + y_offset * scale)
                node.runAction(cc.Sequence.create([cc.MoveTo.create(0.3, pos),
                 cc.CallFunc.create(lambda node=node, pos=pos: node.setPosition(pos))]))

            zhunxin.PlayAnimation('sample_visable_auto')
            self.cnt_yaw = yaw * scale
            self.cnt_pitch = pitch * scale
            global_data.emgr.auto_aim_pos_update.emit()
            return

    def begin_right_aim(self, *args, **kwargs):
        if self._zhunxin_key == 'laser':
            self._cur_zhunxin.frame_left.SetPosition('50%-7', '50%')
            self._cur_zhunxin.frame_right.SetPosition('50%7', '50%')
        else:
            self._on_spread(*args)

    def quit_right_aim(self, *args, **kwargs):
        if self._zhunxin_key == 'laser':
            self._cur_zhunxin.frame_left.SetPosition('50%-26', '50%')
            self._cur_zhunxin.frame_right.SetPosition('50%26', '50%')
        else:
            self._on_spread(*args)

    def _switch_to_aim_camera(self, *args, **kwargs):
        if self._cur_zhunxin and self._zhunxin_key != 'blast':
            self._cur_zhunxin.setVisible(False)
        if self._auto_aim_pnl_visible:
            self._auto_aim_pnl_visible = False
            self._auto_aim_pnl.setVisible(False)
        self.panel.zhunxin.point.setVisible(False)

    def _switch_to_last_camera_state(self, *args):
        self._ctrl_point()
        if self._cur_zhunxin:
            self._cur_zhunxin.setVisible(True)
            global_data.game_mgr.post_exec(self._on_spread)
            self.init_auto_aim()
            self._on_spread()

    def on_player_setted(self, player):
        self.unregister_lgm_timer()
        self.bind_aim_event(self.player, False)
        if not player:
            self._set_aim_target(None)
        self.player = player
        if player:
            if self.is_player_first_setted:
                self.is_player_first_setted = False
                self.panel.setVisible(True)
                if global_data.player and global_data.player.logic:
                    self._spectate = global_data.player.logic.ev_g_is_in_spectate()
            self.bind_aim_event(self.player, True)
            self.check_camera_state()
            global_data.game_mgr.delay_exec(0.2, self.init_auto_aim, True)
            self.init_auto_aim(True)
        self.on_update_aim_color()
        return

    def _on_breath(self, *args):
        pass

    def _on_stop_breath(self, *args):
        pass

    def _on_enter_state(self, new_state):
        from logic.gcommon.cdata.status_config import ST_STAND
        if new_state == ST_STAND:
            if self._cur_zhunxin:
                self._cur_zhunxin.SetTimeOut(0.0333, self._on_spread)

    def _on_spread(self, *args):
        if not self.player or not self._zhunxin_key or self._cur_zhunxin is None or not self._cur_zhunxin.isVisible():
            return
        else:
            spread_values = self.player.ev_g_spread_values()
            if not spread_values:
                return
            spread_base, spread_value, recover_time = spread_values
            if spread_base < 0.01:
                return
            import cc
            if self._zhunxin_key == 'shotgun':
                center_x, center_y = self._cur_zhunxin.shotgun_circle.GetPosition()
                scale1 = self._scale_value * spread_value * 0.5
                scale2 = self._scale_value * spread_base * 0.5
                if self.cur_auto_aim_scale_target == scale1 and self.cur_sec_auto_aim_scale_target == scale2:
                    return
                self._cur_zhunxin.shotgun_left.stopAllActions()
                self._cur_zhunxin.shotgun_right.stopAllActions()
                self._cur_zhunxin.shotgun_left.runAction(cc.Sequence.create([
                 cc.MoveTo.create(0.1, cc.Vec2(center_x - scale1, center_y)),
                 cc.MoveTo.create(0.1, cc.Vec2(center_x - scale2, center_y))]))
                self._cur_zhunxin.shotgun_right.runAction(cc.Sequence.create([
                 cc.MoveTo.create(0.1, cc.Vec2(center_x + scale1, center_y)),
                 cc.MoveTo.create(0.1, cc.Vec2(center_x + scale2, center_y))]))
                self.cur_auto_aim_scale_target = scale1
                self.cur_sec_auto_aim_scale_target = scale2
                return
            if self._zhunxin_key == 'sniper':
                spread_value_info = (
                 spread_value, 0.1, True)
                self.spread_size(self._cur_zhunxin.sniper_circle, None, spread_value_info)
                return
            if self._zhunxin_key == 'lmg':
                self.lmg_spread_size(self._cur_zhunxin)
                return
            scale_value = self._scale_value * 2 / self.AUTO_AIM_SIZE
            scale1 = scale_value * spread_value
            scale2 = scale_value * spread_base
            aim_circle = getattr(self.panel.zhunxin, '{}_circle'.format(self._zhunxin_key))
            if not aim_circle:
                return
            if self.cur_auto_aim_scale_target != scale1 or self.cur_sec_auto_aim_scale_target != scale2:
                self.cur_auto_aim_scale_target = scale1
                self.cur_sec_auto_aim_scale_target = scale2
                aim_circle.stopAllActions()

                def _opacity_callback():
                    self._set_auto_opacity(aim_circle, self._zhunxin_key)

                aim_circle.runAction(cc.Sequence.create([
                 cc.ScaleTo.create(0.1, scale1),
                 cc.CallFunc.create(_opacity_callback),
                 cc.ScaleTo.create(0.1, scale2),
                 cc.CallFunc.create(_opacity_callback)]))
            return

    def spread_size(self, aim_node, spread_base_info=None, spread_value_info=None):
        import cc
        aim_node.stopAllActions()
        o_size, _ = aim_node.GetContentSize()
        interval_time = 0.033
        act_lst = []
        if spread_value_info:
            spread_value, delay_time, need_ani = spread_value_info
            n_size = spread_value * self.AUTO_AIM_SIZE / 2.0
            if need_ani:
                off_size = (n_size - o_size) / (delay_time / interval_time)

                def check_end(pass_time, o_size=o_size, off_size=off_size):
                    size = o_size + pass_time / interval_time * off_size
                    aim_node.SetContentSize(size, size)
                    aim_node.ResizeAndPosition(include_self=False)

                def run_end_ac(n_size=n_size):
                    aim_node.SetContentSize(n_size, n_size)
                    aim_node.ResizeAndPosition(include_self=False)

                act = cc.CallFunc.create(lambda : aim_node.TimerAction(check_end, delay_time, callback=run_end_ac, interval=interval_time))
            else:
                aim_node.SetContentSize(n_size, n_size)
                aim_node.ResizeAndPosition(include_self=False)
                act = cc.DelayTime.create(delay_time)
            act and act_lst.append(act)
        if spread_base_info:
            spread_base, base_delay_time, base_need_ani = spread_base_info
            n_base_size = spread_base * self.AUTO_AIM_SIZE / 2.0
            if base_need_ani:
                off_base_size = (n_base_size - o_size) / (base_delay_time / interval_time)

                def check_base_end(pass_time, o_size=o_size, off_base_size=off_base_size):
                    base_size = o_size + pass_time / interval_time * off_base_size
                    aim_node.SetContentSize(base_size, base_size)
                    aim_node.ResizeAndPosition(include_self=False)

                def run_base_end_ac(n_base_size=n_base_size):
                    aim_node.SetContentSize(n_base_size, n_base_size)
                    aim_node.ResizeAndPosition(include_self=False)

                act = cc.CallFunc.create(lambda : aim_node.TimerAction(check_base_end, base_delay_time, callback=run_base_end_ac, interval=interval_time))
            else:
                aim_node.SetContentSize(n_base_size, n_base_size)
                aim_node.ResizeAndPosition(include_self=False)
                act = cc.DelayTime.create(base_delay_time)
            act and act_lst.append(act)
        act_lst and aim_node.runAction(cc.Sequence.create(act_lst))

    def unregister_lgm_timer(self):
        self.lmg_pass_time = 0
        if self._lmg_timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._lmg_timer)
        self._lmg_timer = 0

    def lmg_spread_min_anim(self, aim_node, _offset):
        _offset *= 0.85
        time = 0.1
        x, y = aim_node.lmg_circle.left.CalcPosition('50%{}'.format(-_offset), '50%')
        aim_node.lmg_circle.left.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))
        x, y = aim_node.lmg_circle.right.CalcPosition('50%{}'.format(_offset), '50%')
        aim_node.lmg_circle.right.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))
        x, y = aim_node.lmg_circle.up.CalcPosition('50%', '50%{}'.format(_offset))
        aim_node.lmg_circle.up.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))
        x, y = aim_node.lmg_circle.down.CalcPosition('50%', '50%{}'.format(-_offset))
        aim_node.lmg_circle.down.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))

    def lmg_spread_normal_anim(self, aim_node, _offset):
        old_offset = _offset
        _offset *= 0.9
        time = 0.15
        aim_node.lmg_circle.left.SetPosition('50%{}'.format(-_offset), '50%')
        aim_node.lmg_circle.right.SetPosition('50%{}'.format(_offset), '50%')
        aim_node.lmg_circle.up.SetPosition('50%', '50%{}'.format(_offset))
        aim_node.lmg_circle.down.SetPosition('50%', '50%{}'.format(-_offset))
        x, y = aim_node.lmg_circle.left.CalcPosition('50%{}'.format(-old_offset), '50%')
        aim_node.lmg_circle.left.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))
        x, y = aim_node.lmg_circle.right.CalcPosition('50%{}'.format(old_offset), '50%')
        aim_node.lmg_circle.right.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))
        x, y = aim_node.lmg_circle.up.CalcPosition('50%', '50%{}'.format(old_offset))
        aim_node.lmg_circle.up.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))
        x, y = aim_node.lmg_circle.down.CalcPosition('50%', '50%{}'.format(-old_offset))
        aim_node.lmg_circle.down.runAction(cc.MoveTo.create(time, cc.Vec2(x, y)))

    def lmg_spread_size(self, aim_node, delay_time=0):
        import common.utilities
        from logic.gcommon.cdata.status_config import ST_JUMP_1, ST_JUMP_2, ST_RIGHT_AIM, ST_SHOOT
        from common.utils.timer import CLOCK
        spread_values = self.player.ev_g_spread_values()
        if not spread_values:
            return
        spread_base, spread_value, recover_time = spread_values
        is_first = False
        offset_range = [
         23, 60]
        if not self.lmg_scale_range:
            is_first = True
            weapon = self.player.share_data.ref_wp_bar_cur_weapon
            min_spread = weapon.get_effective_value('fAimMinSpread', default=0)
            ss_spread = weapon.get_effective_value('fHIPStandStop', default=0)
            max_spread = weapon.get_effective_value('fMaxSpread', default=0)
            self.lmg_scale_range = [min_spread + ss_spread, max_spread + ss_spread]
        scale = float(spread_value - self.lmg_scale_range[0]) / float(self.lmg_scale_range[1] - self.lmg_scale_range[0])
        offset = common.utilities.lerp(offset_range[0], offset_range[1], scale)
        offset = max(offset_range[0], offset)

        def set_offset(_offset):
            if _offset == None:
                return
            else:
                self.lmg_cur_offset = _offset
                aim_node.lmg_circle.left.SetPosition('50%{}'.format(-_offset), '50%')
                aim_node.lmg_circle.right.SetPosition('50%{}'.format(_offset), '50%')
                aim_node.lmg_circle.up.SetPosition('50%', '50%{}'.format(_offset))
                aim_node.lmg_circle.down.SetPosition('50%', '50%{}'.format(-_offset))
                return

        if not self.lmg_force_timer and (is_first or self.player.ev_g_is_in_any_state([ST_SHOOT])):
            set_offset(offset)
            self.lmg_target_offset = offset
            if self.lmg_target_offset == offset_range[0] and self.lmg_cur_offset == self.lmg_target_offset:
                self.lmg_spread_min_anim(aim_node, offset)
            else:
                self.lmg_spread_normal_anim(aim_node, offset)
            self.unregister_lgm_timer()
            return
        self.lmg_force_timer = False

        def get_cur_recover_offset():
            spread_values = self.player.ev_g_spread_values()
            if not spread_values:
                return None
            else:
                spread_base, spread_value, recover_time = self.player.ev_g_spread_values()
                scale = float(spread_value - self.lmg_scale_range[0]) / float(self.lmg_scale_range[1] - self.lmg_scale_range[0])
                target_offset = common.utilities.lerp(offset_range[0], offset_range[1], scale)
                return target_offset

        step_time = 0.1

        def update(dt):
            if not self.panel or not self.panel.isValid():
                self.unregister_lgm_timer()
                return
            self.lmg_pass_time += dt
            if self.lmg_pass_time > step_time * 3 or not self.player:
                self.unregister_lgm_timer()
                set_offset(get_cur_recover_offset())
                return
            if self.lmg_pass_time > step_time and self.player.ev_g_is_in_any_state([ST_JUMP_1, ST_JUMP_2]):
                self.unregister_lgm_timer()
                return
            if self.lmg_pass_time <= step_time:
                self.lmg_cur_offset = common.utilities.lerp(self.lmg_cur_offset, self.lmg_target_offset, self.lmg_pass_time / step_time)
            else:
                target_offset = offset_range[1]
                if self.player.sd.ref_in_aim or self.player.sd.ref_in_right_aim:
                    target_offset = get_cur_recover_offset()
                    if not target_offset:
                        return
                self.lmg_cur_offset = common.utilities.lerp(self.lmg_cur_offset, target_offset, (self.lmg_pass_time - step_time) / step_time)
            set_offset(self.lmg_cur_offset)

        self.unregister_lgm_timer()
        self._lmg_timer = global_data.game_mgr.get_logic_timer().register(func=update, interval=0.03, mode=CLOCK, timedelta=True)
        self.lmg_target_offset = offset

    def on_camera_state_change(self, state, *args):
        from logic.client.const.camera_const import FREE_CAMERA_LIST
        if state in FREE_CAMERA_LIST:
            self._is_free_camera_state = True
            self.panel.zhunxin.ban.setVisible(False)
        else:
            self._is_free_camera_state = False
        from data.camera_state_const import OBSERVE_FREE_MODE
        if state is OBSERVE_FREE_MODE:
            self.add_hide_count('OBSERVE_FREE')
        else:
            self.add_show_count('OBSERVE_FREE')
        if self._spectate:
            from data.camera_state_const import AIM_MODE
            if global_data.cam_data and global_data.cam_data.camera_state_type != AIM_MODE:
                self._switch_to_last_camera_state()

    def do_show_panel(self):
        super(FrontSightUI, self).do_show_panel()
        self._on_spread()

    def _on_aim_spread(self, spread_base, spread_value, delay_time, recover_time, weapon_pos=None):
        if not self.player or not self._cur_zhunxin or not self._cur_zhunxin.isVisible() or not self._zhunxin_key:
            return
        import cc
        if self._zhunxin_key == 'shotgun':
            center_x, center_y = self._cur_zhunxin.shotgun_circle.GetPosition()
            scale1 = self._scale_value * spread_value * 0.5
            scale2 = self._scale_value * spread_base * 0.5
            self.cur_auto_aim_scale_target = scale1
            self.cur_sec_auto_aim_scale_target = scale2
            self._cur_zhunxin.shotgun_left.stopAllActions()
            self._cur_zhunxin.shotgun_right.stopAllActions()
            self._cur_zhunxin.shotgun_left.SetPosition(center_x - scale1, center_y)
            self._cur_zhunxin.shotgun_right.SetPosition(center_x + scale1, center_y)
            self._cur_zhunxin.shotgun_left.runAction(cc.Sequence.create([
             cc.MoveTo.create(0.1, cc.Vec2(center_x - scale2, center_y))]))
            self._cur_zhunxin.shotgun_right.runAction(cc.Sequence.create([
             cc.MoveTo.create(0.1, cc.Vec2(center_x + scale2, center_y))]))
            return
        if self._zhunxin_key == 'sniper':
            if spread_value < 0.01:
                return
            spread_base_info = (
             spread_base, 0.1, True)
            spread_value_info = (spread_value, delay_time, False)
            self.spread_size(self._cur_zhunxin.sniper_circle, spread_base_info, spread_value_info)
            return
        if self._zhunxin_key == 'lmg':
            self.lmg_spread_size(self._cur_zhunxin, delay_time=delay_time)
            return
        aim_circle = getattr(self.panel.zhunxin, '{}_circle'.format(self._zhunxin_key))
        if not aim_circle:
            return
        cur_scale = aim_circle.getScale()
        scale_value = self._scale_value * 2 / self.AUTO_AIM_SIZE
        next_scale = scale_value * spread_value
        aim_circle.stopAllActions()
        self._set_auto_opacity(aim_circle, self._zhunxin_key)

        def _opacity_callback():
            self._set_auto_opacity(aim_circle, self._zhunxin_key)

        if self.shake_scale:
            over_scale = next_scale + 0.05 if next_scale > cur_scale else next_scale - 0.05
            aim_circle.runAction(cc.Sequence.create([
             cc.ScaleTo.create(0.05, over_scale),
             cc.ScaleTo.create(0.05, next_scale),
             cc.DelayTime.create(delay_time),
             cc.ScaleTo.create(0.1, scale_value * spread_base),
             cc.CallFunc.create(_opacity_callback)]))
        else:
            aim_circle.setScale(next_scale)
            aim_circle.runAction(cc.Sequence.create([
             cc.DelayTime.create(delay_time),
             cc.ScaleTo.create(0.1, scale_value * spread_base),
             cc.CallFunc.create(_opacity_callback)]))

    def _on_fire_pos_collision(self, pos, delay=2, flag=False):
        if not flag:
            return
        import world
        if self._is_free_camera_state:
            return
        if self._zhunxin_key == 'grenade':
            self.panel.zhunxin.ban.setVisible(False)
            return
        camera = world.get_active_scene().active_camera
        x, y = camera.world_to_screen(pos)
        pos = self._convert_to_aim_pos(x, y)
        pos = self.panel.zhunxin.convertToNodeSpace(pos)
        ban = self.panel.zhunxin.ban
        ban.setVisible(True)

        def hide():
            ban.setVisible(False)

        ban.SetTimeOut(delay, hide, self.FIRE_POS_COLLISION_TAG)

    def _set_auto_opacity(self, aim_circle, key):
        scale = aim_circle.getScale()
        scale = min(max(scale, self.SCALE_1), self.SCALE_2)
        opacity = int((scale - self.SCALE_1) / (self.SCALE_2 - self.SCALE_1) * 255)
        img_60 = getattr(aim_circle, '{}_60'.format(key))
        img_140 = getattr(aim_circle, '{}_140'.format(key))
        if img_60:
            img_60.setOpacity(255 - opacity)
        if img_140:
            img_140.setOpacity(opacity)

    def _set_aim_target(self, aim_target):
        if self.player is None or aim_target is self._aim_target or self._spectate:
            return
        else:
            from common.cfg import confmgr
            if self._aim_target is not None:
                if self._aim_target.unregist_event:
                    if G_POS_CHANGE_MGR:
                        self._aim_target.unregist_pos_change(self._refresh_target)
                    else:
                        self._aim_target.unregist_event('E_POSITION', self._refresh_target)
                self.player.unregist_event('E_DELTA_PITCH', self._refresh_target)
                self.player.unregist_event('E_DELTA_YAW', self._refresh_target)
                if aim_target is None:
                    if G_POS_CHANGE_MGR:
                        self.player.unregist_pos_change(self._refresh_target)
                    else:
                        self.player.unregist_event('E_POSITION', self._refresh_target)
                    self.panel.zhunxin.stopAllActions()

                    def cb():
                        if self._cur_zhunxin:
                            self._cur_zhunxin.setOpacity(255)

                    self._aim_to_center(confmgr.get('aim_helper_conf', 'AIM_CENTER_DURATION', default=0.2), cb)
                    if self._zhunxin_key == 'normal':
                        self.panel.zhunxin.normal_aim_60.setVisible(False)
                        self.panel.zhunxin.normal_aim_140.setVisible(False)
                    if self._zhunxin_key == 'rocket':
                        pass
                    else:
                        self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_1.png')
            elif aim_target:
                self.panel.zhunxin.stopAllActions()
                if self._zhunxin_key == 'rocket':
                    global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                           'locked_target'))

                    def aimed():
                        if self._aim_target:
                            self.panel.zhunxin.PlayAnimation('auto_lock')
                            self._auto_aim_pnl.nd_lock.setVisible(True)
                            img_lock_path = 'gui/ui_res_2/battle/attack/auto_frame_sniper.png'
                            self._auto_aim_pnl.nd_lock.img_lock.SetDisplayFrameByPath('', img_lock_path)
                            self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_2.png')
                        else:
                            self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_1.png')

                    self.panel.zhunxin.SetTimeOut(self._lock_time, aimed)
                elif not self._silence_auto_aim:
                    self.panel.zhunxin.PlayAnimation('auto_lock')
                    self._auto_aim_pnl.nd_lock.setVisible(True)
                    img_lock_path = 'gui/ui_res_2/battle/attack/auto_frame_normal.png'
                    self._auto_aim_pnl.nd_lock.img_lock.SetDisplayFrameByPath('', img_lock_path)
                    self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_2.png')
            self._aim_target = aim_target
            if aim_target:
                if not self._silence_auto_aim and self._cur_zhunxin:
                    self._cur_zhunxin.setVisible(False)
                self._aim_to_target(confmgr.get('aim_helper_conf', 'AIM_TARGET_DURATION', default=0.2), self._refresh_target)
                if G_POS_CHANGE_MGR:
                    aim_target.regist_pos_change(self._refresh_target, 0.1)
                    self.player.regist_pos_change(self._refresh_target, 0.1)
                else:
                    aim_target.regist_event('E_POSITION', self._refresh_target, 10)
                    self.player.regist_event('E_POSITION', self._refresh_target, 10)
                self.player.regist_event('E_DELTA_PITCH', self._refresh_target, 10)
                self.player.regist_event('E_DELTA_YAW', self._refresh_target, 10)
            elif self._cur_zhunxin and self._auto_aim_pnl_visible:
                self._cur_zhunxin.setVisible(True)
                self._cur_zhunxin.setOpacity(255)
                self._is_aim_on_target = False
                self.update_normal_circle_color()
            return

    def _point_to_target(self, target):
        if self._aim_target:
            return
        if target:
            self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_2.png')
        else:
            self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_1.png')

    def _convert_to_aim_pos(self, x, y):
        import cc
        x, y = neox_pos_to_cocos(x, y)
        pos = cc.Vec2(x, y)
        return pos

    def _refresh_target(self, *args):
        if self._aim_auto_move:
            return
        else:
            if not self._cur_zhunxin or not self._cur_zhunxin.isValid():
                return
            if self._aim_target is None:
                self._cur_zhunxin.setOpacity(255)
                return
            import world
            from logic.gcommon.const import NEOX_UNIT_SCALE
            camera = world.get_active_scene().active_camera
            weapon = self.player.share_data.ref_wp_bar_cur_weapon
            aim_args = self.player.ev_g_at_aim_args_all()
            if weapon:
                auto_aim_dis = weapon.conf('fAutoAimDistance') if 1 else None
                if not auto_aim_dis or not aim_args:
                    if weapon:
                        log_error("weapon's fAutoAimDistance is None", auto_aim_dis, weapon.get_config())
                    return
                auto_aim_dis = auto_aim_dis * aim_args['aim_r']
                old_aim_on_target = self._is_aim_on_target
                if self._zhunxin_key != 'rocket' and camera and weapon and self._aim_target.ev_g_model_hit_ray(camera.position, camera.rotation_matrix.forward * auto_aim_dis * NEOX_UNIT_SCALE):
                    pos = self._auto_aim_pnl.getPosition()
                    self._is_aim_on_target = True
                    if self._is_aim_on_target != old_aim_on_target:
                        self.update_normal_circle_color()
                else:
                    self._is_aim_on_target = False
                    if self._is_aim_on_target != old_aim_on_target:
                        self.update_normal_circle_color()
                    pos = self._aim_target.ev_g_aim_position()
                    if not pos:
                        self._cur_zhunxin.setOpacity(255)
                        return
                    self.last_pos = pos
                    from math import sqrt
                    x, y = camera.world_to_screen(pos)
                    pos = self._convert_to_aim_pos(x, y)
                    pos = self.panel.zhunxin.convertToNodeSpace(pos)
                self._silence_auto_aim or self._cur_zhunxin.SetPosition(pos.x, pos.y)
            self._auto_aim_pnl.nd_lock.SetPosition(pos.x, pos.y)
            return

    def _aim_to_target(self, duration, callback):
        if not self._cur_zhunxin or not self._cur_zhunxin.isValid() or not self._cur_zhunxin.isVisible():
            callback()
            return
        else:
            if self._aim_target is None:
                self._cur_zhunxin.setOpacity(255)
                callback()
                return
            pos = self._aim_target.ev_g_aim_position()
            if not pos:
                self._cur_zhunxin.setOpacity(255)
                callback()
                return
            if self._silence_auto_aim:
                return
            import world
            camera = world.get_active_scene().active_camera
            x, y = camera.world_to_screen(pos)
            pos = self._convert_to_aim_pos(x, y)
            pos = self.panel.zhunxin.convertToNodeSpace(pos)
            self._aim_move_to(pos, duration, callback)
            return

    def _aim_to_center(self, duration, callback):
        if not self._cur_zhunxin or not self._cur_zhunxin.isValid():
            callback()
            return
        self._auto_aim_pnl.nd_lock.setVisible(False)
        if self._silence_auto_aim:
            return
        pos = self._auto_aim_pnl.getPosition()
        self._aim_move_to(pos, duration, callback)

    def _aim_move_to(self, pos, duration, callback):
        x, y = self._cur_zhunxin.GetPosition()
        dx = (pos.x - x) / 4
        dy = (pos.y - y) / 4
        delta_time = duration / 10
        seq = []
        import cc
        for i in range(1, 5):
            seq.append(cc.MoveTo.create(delta_time * i, cc.Vec2(x + dx * i, y + dy * i)))

        def cb(pos=pos):
            self._aim_auto_move = False
            self._cur_zhunxin.setPosition(pos)
            callback()

        seq.append(cc.CallFunc.create(cb))
        self._aim_auto_move = True
        self._cur_zhunxin.runAction(cc.Sequence.create(seq))

    def stop_zhunxin_action(self):
        if self._cur_zhunxin:
            self._cur_zhunxin.stopAllActions()
            self._cur_zhunxin.setOpacity(255)
            self._cur_zhunxin.ReConfPosition()
        self._aim_auto_move = False

    def change_cur_pos(self, weapon_pos):
        self.close_auto_aim()
        self.unregister_lgm_timer()
        if self._cur_zhunxin:
            self._cur_zhunxin.setVisible(False)
            self.stop_zhunxin_action()
            self._cur_zhunxin = None
        if not self.player:
            return
        else:
            from logic.gcommon import const
            if weapon_pos in const.MAIN_WEAPON_LIST:
                cur_weapon = self.player.share_data.ref_wp_bar_cur_weapon
                if cur_weapon:
                    self._zhunxin_key = confmgr.get('firearm_res_config', str(cur_weapon.iType), 'cAimIcon')
                    self._cur_zhunxin = getattr(self.panel.zhunxin, self._zhunxin_key or 'normal')
            elif weapon_pos in [const.PART_WEAPON_POS_COLD, const.PART_WEAPON_POS_BOMB, const.PART_WEAPON_POS_NONE]:
                self._cur_zhunxin = self.panel.zhunxin.throw_near
                self._zhunxin_key = None
            else:
                self._cur_zhunxin = None
                self._zhunxin_key = None
            self.shake_scale = False
            self._silence_auto_aim = False
            if self._zhunxin_key == 'normal':
                self.panel.zhunxin.normal_aim_60.setVisible(False)
                self.panel.zhunxin.normal_aim_140.setVisible(False)
            elif self._zhunxin_key == 'blast':
                self._silence_auto_aim = True
                self.shake_scale = True
            self._ctrl_point()
            if self._cur_zhunxin:
                self._cur_zhunxin.setVisible(True)
                self._cur_zhunxin.setOpacity(255)
                atk = getattr(self.panel.zhunxin, '{}_atk'.format(self._zhunxin_key))
                if atk:
                    atk.setVisible(False)
                self._on_spread()
                if self._zhunxin_key == 'firegun':
                    self._cur_zhunxin.nd_fire_bullet.setVisible(False)
                elif self._zhunxin_key == 'lmg':
                    self._cur_zhunxin.setOpacity(203)
                elif self._zhunxin_key == 'laser':
                    self._cur_zhunxin.frame_left.SetPosition('50%-26', '50%')
                    self._cur_zhunxin.frame_right.SetPosition('50%26', '50%')
            self.panel.zhunxin.point.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/atk_gun_1.png')
            self.panel.zhunxin.point.SetColor(self._aim_normal_color)
            self.on_switch_aim_bullet_node()
            return

    def on_bullet_num_change(self, *args):
        if self._zhunxin_key == 'firegun':
            if not self.player:
                return
            panel = self._cur_zhunxin
            panel.nd_fire_bullet.setVisible(True)
            cur_weapon = self.player.share_data.ref_wp_bar_cur_weapon
            if cur_weapon:
                cap = cur_weapon.get_bullet_cap()
                num = cur_weapon.get_bullet_num()
                panel.nd_fire_bullet.lab_bullet.SetString('%d/%d' % (num, cap))
                panel.nd_fire_bullet.prog_bullet.SetPercentage(67 + int(float(num) / cap * 16))
            if self._firegun_delay_hid:
                game3d.cancel_delay_exec(self._firegun_delay_hid)
                self._firegun_delay_hid = None

            def callback():
                self._firegun_delay_hid = None
                if panel and panel.nd_fire_bullet:
                    panel.nd_fire_bullet.setVisible(False)
                return

            self._firegun_delay_hid = game3d.delay_exec(2000, callback)
        return

    def on_finalize_panel(self):
        self.unregister_lgm_timer()
        self.on_player_setted(None)
        return

    def _ctrl_point(self):
        if self._zhunxin_key in ('grenade', 'firegun', 'snow_ball', 'muti_rocket') and self._cur_zhunxin:
            self.panel.zhunxin.point.setVisible(False)
        else:
            self.panel.zhunxin.point.setVisible(True)

    def bind_aim_event(self, target, bind):
        if bind:
            zhunxin = self.panel.zhunxin
            for node in zhunxin.GetChildren():
                node.setVisible(False)

        if not target or not target.is_valid():
            return
        event_lst = [
         [
          'E_WPBAR_SWITCHED', self.change_cur_pos, 1],
         [
          'E_SWITCHED_WP_MODE', self.change_cur_pos, 1],
         [
          'E_CUR_BULLET_NUM_CHG', self.on_bullet_num_change, 0],
         [
          'E_ON_AT_AIM_ARGS_CHANGED', self.init_auto_aim, 0],
         [
          'E_SUCCESS_RIGHT_AIM', self.begin_right_aim, 0],
         [
          'E_FINISH_QUIT_RIGHT_AIM', self.quit_right_aim, 0],
         [
          'E_ACTION_MOVE', self._on_spread, 1],
         [
          'E_ACTION_MOVE', self._on_breath, 1],
         [
          'E_ACTION_MOVE_STOP', self._on_spread, 1],
         [
          'E_ACTION_MOVE_STOP', self._on_stop_breath, 1],
         [
          'E_JUMP', self._on_spread, 1],
         [
          'E_JUMP', self._on_breath, 1],
         [
          'E_GROUND', self._on_spread, 1],
         [
          'E_ENTER_STATE', self._on_enter_state, 1],
         [
          'E_SQUAT', self._on_spread, 1],
         [
          'E_STAND', self._on_spread, 1],
         [
          'E_STAND', self._on_stop_breath, 1],
         [
          'E_SWITCHED', self._on_spread, 1],
         [
          'E_AIM_TARGET', self._set_aim_target, 0],
         [
          'E_AIM_SPREAD', self._on_aim_spread, 0],
         [
          'E_CLOTHING_CHANGED', self._on_spread, 0],
         [
          'E_IS_POINTING_TARGET', self._point_to_target, 0],
         [
          'E_FIRE_POS_COLLISION', self._on_fire_pos_collision, 0],
         [
          'E_ON_ENABLE_AUTO_AIM_ON_CONDITION', self._on_enable_auto_aim_on_condition, 0],
         [
          'E_ON_DISABLE_AUTO_AIM_ON_CONDITION', self._on_disable_auto_aim_on_condition, 0]]
        if bind:
            self.change_cur_pos(target.share_data.ref_wp_bar_cur_pos)
            regist_event = target.regist_event
            for event_name, func, priority in event_lst:
                regist_event(event_name, func, priority)

        else:
            unregist_event = target.unregist_event
            for event_name, func, priority in event_lst:
                unregist_event(event_name, func)

    def init_visible_event(self):
        if global_data.ui_mgr.get_ui('BigMapUI'):
            self.add_hide_count('BigMapUI')

    def show_sideways_direction(self, sideways_dir_list):
        from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
        posture_to_ui_dir = {POSTURE_UP_SIDEWAYS: self._auto_aim_pnl.frame.turn_up,
           POSTURE_LEFT_SIDEWAYS: self._auto_aim_pnl.frame.turn_left,
           POSTURE_RIGHT_SIDEWAYS: self._auto_aim_pnl.frame.turn_right
           }
        for nd in six_ex.values(posture_to_ui_dir):
            nd.setVisible(False)

        if not sideways_dir_list:
            return
        for sideways_dir in sideways_dir_list:
            cur_show_dir = posture_to_ui_dir.get(sideways_dir, self._auto_aim_pnl.frame.turn_right)
            if cur_show_dir:
                cur_show_dir.setVisible(True)

    def check_camera_state(self):
        from data.camera_state_const import AIM_MODE
        scene = global_data.game_mgr.scene
        cam = scene.get_com('PartCamera')
        if cam:
            if cam.get_cur_camera_state_type() == AIM_MODE:
                self._switch_to_aim_camera()
            else:
                self._switch_to_last_camera_state()

    def _on_set_scene_camera_target(self):
        self._on_scene_camera_target_setted(global_data.cam_lplayer)

    def _on_scene_camera_target_setted(self, ltarget):
        self.on_player_setted(global_data.cam_lplayer)
        if ltarget:
            self.check_camera_state()

    def on_gun_loading(self):
        if not self.player:
            return
        if self._zhunxin_key != 'sniper':
            return
        MIN_PERCENT = 0
        MAX_PERCENT = 100
        weapon = self.player.share_data.ref_wp_bar_cur_weapon
        loading_time = weapon.conf('fCDTime2') * (1 - weapon.factor)
        circle_nd = self._cur_zhunxin.sniper_circle
        circle_nd.nd_bolt_right.setVisible(True)
        progress_start_time = time.time()
        circle_nd.nd_bolt_right.progress_bolt_right.SetPercent(MIN_PERCENT)

        def finish():
            circle_nd.StopTimerAction()
            circle_nd.nd_bolt_right.setVisible(False)

        def update_progress_time(dt):
            cur_time = time.time()
            cur_local_time = loading_time + progress_start_time - cur_time
            if cur_local_time < 0:
                finish()
                return
            cur_percent = min((cur_time - progress_start_time) / float(loading_time), 1)
            show_percent = cur_percent * (MAX_PERCENT - MIN_PERCENT) + MIN_PERCENT
            circle_nd.nd_bolt_right.progress_bolt_right.SetPercent(show_percent)

    def on_cancel_gun_loading(self, *args):
        if self._zhunxin_key != 'sniper' or not self._cur_zhunxin:
            return
        circle_nd = self._cur_zhunxin.sniper_circle
        circle_nd.nd_bolt_right.StopTimerAction()
        circle_nd.nd_bolt_right.setVisible(False)

    def update_normal_circle_color(self):
        if self._zhunxin_key == 'normal' and self._cur_zhunxin:
            circle_nd = self._cur_zhunxin.normal_circle
            color = '#SR' if self._is_aim_on_target else self._aim_normal_color
            circle_nd.normal_60.normal_circle_60.SetColor(color)
            circle_nd.normal_140.normal_circle_140.SetColor(color)
            self.panel.zhunxin.point.SetColor(color)

    def on_switch_aim_bullet_node(self):

        def clear_aim_bullet_style():
            if self._aim_bullet_style is not None:
                if self.panel.zhunxin.IsPlayingAnimation(self._aim_bullet_style):
                    self.panel.zhunxin.StopAnimation(self._aim_bullet_style)
                self.panel.zhunxin.RecoverAnimationNodeState(self._aim_bullet_style)
                self._aim_bullet_style = None
            return

        if not self._zhunxin_key:
            self.panel.zhunxin.nd_remaining_line.setVisible(False)
            self.panel.zhunxin.nd_remaining_curve.setVisible(False)
            clear_aim_bullet_style()
        else:
            weapon_object = self.player.share_data.ref_wp_bar_cur_weapon if self.player else None
            itype = weapon_object.iType if weapon_object else None
            new_bullet_style = self._aim_anim_dict.get(str(itype)) or self._aim_anim_dict.get(self._zhunxin_key)
            clear_aim_bullet_style()
            self.panel.zhunxin.PlayAnimation(new_bullet_style)
            self._aim_bullet_style = new_bullet_style
            self.panel.SetTimeOut(0.001, lambda : self.on_weapon_bullet_num_changed([]), tag=210628)
        return

    def on_weapon_bullet_num_changed(self, pos_or_pos_list):
        weapon_object = self.player.share_data.ref_wp_bar_cur_weapon if self.player else None
        if weapon_object:
            if self._zhunxin_key == 'laser':
                cap = weapon_object.get_bullet_cap()
                num = weapon_object.get_bullet_num()
                self._cur_zhunxin.prog_laser.SetPercentage(52 + 21.0 * num / cap)
            else:
                self.update_bullet_info(weapon_object)
        return

    def update_bullet_info(self, wp):
        if not wp:
            return
        max_bullet = wp.get_bullet_cap()
        show_ratio = wp.get_show_ratio()
        weapon_data = wp.get_data()
        cur_bullet_num = weapon_data.get('iBulletNum', 0)
        iReloadRatio = wp.get_reload_ratio()
        bullet_type = wp.get_bullet_type()
        bullet_color = False
        if 1 <= cur_bullet_num < math.ceil(max_bullet * 0.4):
            bullet_color = True
        elif cur_bullet_num < 1:
            bullet_color = True
        if bullet_type in [weapon_const.ITEM_ID_INFINITE_BULLET, weapon_const.ITEM_ID_LIMITED_BULLET]:
            show_bullet_num = max_bullet
        else:
            show_bullet_num = self.get_bag_bullet_num(bullet_type) * iReloadRatio
        if show_bullet_num * show_ratio > 0:
            percent = int(cur_bullet_num * show_ratio) / float(show_bullet_num * show_ratio)
        else:
            percent = 0
        if self.panel.zhunxin.nd_remaining_curve.isVisible():
            nd = self.panel.zhunxin.nd_remaining_curve
            nd.prog_remaining.SetPercentage(percent * 25 + 50)
            if not bullet_color:
                nd.prog_remaining.SetProgressTexture('gui/ui_res_2/battle/progress/progress_remaining_1.png')
                nd.prog_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/progress/progress_remaining_1_bar.png')
            else:
                nd.prog_remaining.SetProgressTexture('gui/ui_res_2/battle/progress/progress_remaining_1_r.png')
                nd.prog_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/progress/progress_remaining_1_bar_r.png')
        if self.panel.zhunxin.nd_remaining_line.isVisible():
            nd = self.panel.zhunxin.nd_remaining_line
            nd.prog_remaining.SetPercentage(percent * 100)
            if not bullet_color:
                nd.prog_remaining.LoadTexture('gui/ui_res_2/battle/progress/progress_remaining.png')
                nd.prog_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/progress/progress_remaining_bar.png')
            else:
                nd.prog_remaining.LoadTexture('gui/ui_res_2/battle/progress/progress_remaining_r.png')
                nd.prog_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/progress/progress_remaining_bar_r.png')

    def _on_enable_auto_aim_on_condition(self):
        if self._spectate:
            return
        self.init_auto_aim(False)

    def _on_disable_auto_aim_on_condition(self):
        if self._spectate:
            return
        if self._auto_aim_pnl_visible:
            self._auto_aim_pnl_visible = False
            self._auto_aim_pnl.setVisible(False)