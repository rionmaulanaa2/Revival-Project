# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8014LockedUI.py
from __future__ import absolute_import
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER, SHOW_SLASH_TYPE_8014
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import RELEASE
from common.utils.cocos_utils import neox_pos_to_cocos
import world
import cc
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
MAX_DIST = 55
MIN_DIST = 15
MAX_SCALE = 1.0
MIN_SCALE = 0.5
RATIO = (MAX_SCALE - MIN_SCALE) / (MAX_DIST - MIN_DIST)
ACTIVATION_SKILL_ID = 801456
MAX_SLASH_ENERGY_PERCENT = 88
MIN_SLASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_SLASH_ENERGY_PERCENT - MIN_SLASH_ENERGY_PERCENT
from common.const import uiconst

class Mecha8014LockedUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8014_2'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.nd_auto_aim.setVisible(False)
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.panel.RecordAnimationNodeState('show_auto')
        self.panel.RecordAnimationNodeState('disappear_auto')
        self.init_parameters()
        self.init_slash_activate_widget()
        self.hide_main_ui(ASSOCIATE_UI_LIST)

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        self.mecha = None
        self._release_locked_timer()
        self._release_slash_activate_timer()
        self._release_slash_type_timer()
        global_data.emgr.camera_switch_to_state_event -= self.on_camera_switch_to_state
        global_data.emgr.update_show_slash_type_8014 -= self.on_show_slash_type_8014_changed
        return

    def init_slash_activate_widget(self):
        self.slash_activate_widget = global_data.uisystem.load_template_create('battle_mech/fight_hit_mech8014_3', parent=self.panel)
        self.slash_activate_widget.nd_jet.setVisible(False)
        self.slash_activate_widget.nd_skill_cd.setVisible(False)

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.locked_target = None
        self.locked_timer = None
        self.slash_activate_timer = None
        self.slash_activated_timestamp = 0.0
        self.slash_activate_duration = 0.0
        self.slash_recovering = False
        self.slash_type_timer = None
        self.slash_type_record_time = 0.0
        self.slash_type_left_duration = 0.0
        if global_data.player:
            self.need_show_slash_type = global_data.player.get_setting_2(SHOW_SLASH_TYPE_8014)
        else:
            self.need_show_slash_type = False
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'update_show_slash_type_8014': self.on_show_slash_type_8014_changed
           }
        emgr.bind_events(econf)
        return

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_LOCKED_TARGET_CHANGED', self.locked_target_changed)
            regist_func('E_SLASH_ACTIVATED', self.on_slash_activated)
            regist_func('E_ENERGY_FULL', self.slash_energy_full)
            regist_func('E_UPDATE_SLASH_TYPE', self.update_slash_type)
            skill_obj = mecha.ev_g_skill(ACTIVATION_SKILL_ID)
            self.slash_recovering = True
            if skill_obj and skill_obj.on_check_cast_skill():
                self.slash_recovering = False
                if mecha.sd.ref_locked_target_finder.is_cur_target_valid():
                    self.locked_target_changed(mecha.sd.ref_locked_target_finder.cur_target)
            else:
                self.slash_recovering = False

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_LOCKED_TARGET_CHANGED', self.locked_target_changed)
            unregist_func('E_SLASH_ACTIVATED', self.on_slash_activated)
            unregist_func('E_ENERGY_FULL', self.slash_energy_full)
            unregist_func('E_UPDATE_SLASH_TYPE', self.update_slash_type)
        self.mecha = None
        return

    def _update_locked_target_pos(self):
        if self.locked_target and self.locked_target.is_valid() and (self.locked_target.sd.ref_hp or 0) > 0:
            model = self.locked_target.ev_g_model()
            cam = global_data.game_mgr.scene.active_camera
            if model and cam:
                socket_matrix = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
                if socket_matrix is None:
                    import exception_hook
                    err_msg = 'Mecha8014LockedUI -- locked_target model socket matrix is None !!\n'
                    err_msg += 'locked_target: {}\n'.format(self.locked_target)
                    err_msg += 'model: {}'.format(model.filename)
                    exception_hook.post_error(err_msg)
                    return
                position = socket_matrix.translation
                dist = (cam.position - position).length / NEOX_UNIT_SCALE
                if dist < MIN_DIST:
                    scale = MAX_SCALE
                elif dist > MAX_DIST:
                    scale = MIN_SCALE
                else:
                    scale = MAX_SCALE - (dist - MIN_DIST) * RATIO
                self.panel.nd_locate.setScale(scale)
                x, y = cam.world_to_screen(position)
                x, y = neox_pos_to_cocos(x, y)
                pos = self.panel.nd_auto_aim.convertToNodeSpace(cc.Vec2(x, y))
                self.panel.nd_locate.SetPosition(pos.x, pos.y)
        else:
            self.locked_target_changed(None)
        return

    def _release_locked_timer(self):
        if self.locked_timer:
            global_data.game_mgr.unregister_logic_timer(self.locked_timer)
            self.locked_timer = None
        return

    def locked_target_changed(self, new_target, force=False):
        if new_target is self.locked_target and not force:
            return
        self.locked_target = new_target
        self._release_locked_timer()
        if new_target:
            if self.slash_recovering:
                return
            self._update_locked_target_pos()
            self.panel.StopAnimation('disappear_auto')
            self.panel.RecoverAnimationNodeState('disappear_auto')
            self.panel.PlayAnimation('show_auto')
            self.locked_timer = global_data.game_mgr.register_logic_timer(self._update_locked_target_pos, interval=1, times=-1)
        else:
            self.panel.StopAnimation('show_auto')
            self.panel.RecoverAnimationNodeState('show_auto')
            self.panel.PlayAnimation('disappear_auto')

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def _update_slash_activate_progress(self):
        cur_timestamp = global_data.game_time
        passed_time = cur_timestamp - self.slash_activated_timestamp
        if passed_time > self.slash_activate_duration:
            passed_time = self.slash_activate_duration
        self.slash_activate_widget.prog_jet.setPercentage(MIN_SLASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * (1.0 - passed_time / self.slash_activate_duration))

    def _release_slash_activate_timer(self):
        if self.slash_activate_timer is not None:
            global_data.game_mgr.unregister_logic_timer(self.slash_activate_timer)
            self.slash_activate_timer = None
        return

    def on_slash_activated(self, flag, duration=0.0):
        self.slash_activate_widget.nd_jet.setVisible(flag)
        if flag:
            self.slash_activated_timestamp = global_data.game_time
            self.slash_activate_duration = duration
            self.slash_activate_widget.prog_jet.setPercentage(MAX_SLASH_ENERGY_PERCENT)
            self.slash_activate_timer = global_data.game_mgr.register_logic_timer(self._update_slash_activate_progress, interval=1, times=-1)
        else:
            self._release_slash_activate_timer()
            if not global_data.no_cd:
                self.slash_recovering = True
                self.locked_target_changed(None)
        return

    def slash_energy_full(self, skill_id):
        if skill_id != ACTIVATION_SKILL_ID:
            return
        self.slash_recovering = False
        if self.mecha.sd.ref_locked_target_finder.is_cur_target_valid():
            self.locked_target_changed(self.mecha.sd.ref_locked_target_finder.cur_target, force=True)

    def on_show_slash_type_8014_changed(self, flag):
        self.need_show_slash_type = flag

    def _update_slash_type_keep_time(self):
        cur_timestamp = global_data.game_time
        passed_time = cur_timestamp - self.slash_type_record_time
        if passed_time > self.slash_type_left_duration:
            passed_time = self.slash_type_left_duration
        percent = (1.0 - passed_time / self.slash_type_left_duration) * 100
        self.slash_activate_widget.nd_skill_cd.bar_prog.prog.setPercentage(percent)
        if percent <= 0:
            self.slash_activate_widget.nd_skill_cd.lab_num.SetString('x1')
            self.slash_activate_widget.nd_skill_cd.setVisible(False)
            self.slash_type_timer = None
            return RELEASE
        else:
            return

    def _release_slash_type_timer(self):
        if self.slash_type_timer:
            global_data.game_mgr.unregister_logic_timer(self.slash_type_timer)
            self.slash_type_timer = None
        return

    def update_slash_type(self, slash_type, keep_time):
        if not self.need_show_slash_type:
            return
        self._release_slash_type_timer()
        self.slash_activate_widget.nd_skill_cd.lab_num.SetString('x{}'.format(slash_type + 1))
        self.slash_activate_widget.nd_skill_cd.bar_prog.prog.setPercentage(100)
        self.slash_activate_widget.nd_skill_cd.setVisible(True)
        self.slash_type_record_time = global_data.game_time
        self.slash_type_left_duration = keep_time
        self.slash_type_timer = global_data.game_mgr.register_logic_timer(self._update_slash_type_keep_time, interval=1, times=-1)