# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlBtn/MechaControlBtn.py
from __future__ import absolute_import
import six
from six.moves import range
import time
from logic.gutils.rocker_widget_utils import RockerWidget
from logic.gutils import rocker_utils
from logic.gutils import character_ctrl_utils
from logic.gcommon.common_const import mecha_const
from logic.gcommon.common_const import skill_const as sconst
from common.uisys.uielment.CCSprite import CCSprite
from common.cfg import confmgr
import world
import math3d
import sys
from logic.gcommon.utility import dummy_cb
from common.utils.timer import RELEASE
PROGRESS_BAR_LIST = {1: 'battle_mech/i_mech_progress1',
   2: 'battle_mech/i_mech_progress2',
   3: 'battle_mech/i_mech_progress3',
   6: 'battle_mech/i_mech_progress6'
   }
PC_PROGRESS_BAR_LIST = {1: 'battle_mech/i_mech_progress1_pc',
   2: 'battle_mech/i_mech_progress2_pc',
   3: 'battle_mech/i_mech_progress3_pc'
   }
file_list = [
 'MechaWeapon', 'MechaWeaponMovable', 'MechaShootMode', 'MechaActivateHeat', 'MechaActivateHeatPC', 'MechaModule', 'MechaSwordCore', 'MechaOxRush', 'MechaHandyShield', 'MechaSuicideState', 'MechaActivateIgnite', 'MechaActivateIgnitePC']

def _preload():
    for btn_module in file_list:
        mpath = 'logic.comsys.mecha_ui.MechaControlBtn.%s' % btn_module
        mod = sys.modules.get(mpath)
        if not mod:
            mod = __import__(mpath, globals(), locals(), [btn_module])


WEAPON_IDS = ['action1', 'action2', 'action3', 'action4']
DOUBLE_CLICK_THRESHOLD = 0.2
_preload()

class ControlBtnWithCopyFunc(object):

    def __init__(self, _ctrl_btn):
        self._ctrl_btn = _ctrl_btn
        self.another_btn = None
        return

    def set_copy_nd(self, nd):
        self.another_btn = ControlBtn(nd, self._ctrl_btn.action_id, self._ctrl_btn.bind_state_id, self._ctrl_btn.action_info)
        self._ctrl_btn.is_copied = True

    def set_copy_nd_vis(self, vis):
        if self.another_btn:
            self.another_btn.setVisible(vis)

    def get_normal_nd(self):
        return self._ctrl_btn

    def get_copy_nd(self):
        return self.another_btn

    def __getattr__(self, aname):
        attr = getattr(self._ctrl_btn, aname)
        if attr is None:
            raise AttributeError(aname)
        else:
            if not self.another_btn:
                return attr
            if not callable(attr):
                return attr

            def trigger_func(*args, **kwargs):
                ret = attr(*args, **kwargs)
                if self.another_btn:
                    func = getattr(self.another_btn, aname)
                    if func:
                        func(*args, **kwargs)
                return ret

            return trigger_func
        return

    def destroy(self):
        if self.another_btn:
            self.another_btn.destroy()
            self.another_btn = None
        if self._ctrl_btn:
            self._ctrl_btn.destroy()
            self._ctrl_btn = None
        return


class ControlBtn(object):

    def __init__(self, nd, action_id, state_id, action_info):
        self.nd = nd
        self.nd_temp_pc = None
        parent = nd.GetParent()
        if parent:
            self.nd_temp_pc = getattr(parent, 'temp_pc')
        self.action_id = action_id
        self.action_info = action_info
        self.bind_state_id = state_id
        self.skill_id = None
        self.cost = 0
        self.recover = 0
        self.skill_cd_event_registered = False
        self.skill_cd_type = mecha_const.CD_TYPE_COUNTDOWN
        self.sub_skill_id = None
        self.sub_cost = 0
        self.sub_recover = 0
        self.mecha = None
        self.cd_timer = None
        self.last_finger_move_vec = None
        self.progress_bar = None
        self.progress_bar_elem = []
        self.action_ret = False
        self.enable_drag = False
        self.enabled = True
        self.disable_cnt = 0
        self.disable_reason = set()
        self.last_btn = None
        self.last_touch = None
        self.btn_dragged = False
        self.btn_dragged_dir = None
        self.use_drag_helper = True
        self._drag_base_val_specific = None
        self._drag_as_screen = False
        self.begin_func = None
        self.drag_func = None
        self.end_func = None
        bar = self.nd.bar
        btn = self.nd.button
        self.setEnable(True)
        self.nd.img_broken.setVisible(False)
        self.nd.nd_useless.setVisible(False)
        self.repeat_check_timer = None
        self.btn_pushing = False
        self.btn_touch_pushing = False
        bar.SetZoomScale(False)
        self.init_rocker_sensitivity()
        self.rocker = RockerWidget(bar, bar, btn)
        self.rocker.set_begin_callback(self.on_begin)
        self.rocker.set_end_callback(self.on_end)
        self.rocker.set_drag_callback(self.on_drag)
        self.rocker_center_wpos = self.nd.nd_pos.ConvertToWorldSpacePercentage(50, 50)
        icon = action_info.get('action_icon', {}).get(action_id, None)
        if icon and isinstance(self.nd.icon, CCSprite):
            self.nd.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_main/{}.png'.format(icon))
        self.is_select_btn = self.action_id in action_info.get('select_btn', [])
        self.is_selected = False
        self.extend_ui = []
        self.extend(action_info)
        self.last_success_action_time = 0
        self.is_copied = False
        self._press_down_time = 0
        self._press_up_time = 0
        return

    def set_action_show_progress(self, show_progress):
        no_progress_btns = self.action_info.get('no_progress_btn', [])
        if self.action_id in no_progress_btns:
            if show_progress:
                no_progress_btns.remove(self.action_id)
        elif not show_progress:
            no_progress_btns.append(self.action_id)
        self.action_info['no_progress_btn'] = no_progress_btns

    def refresh_action_icon_and_extend_ui(self, action_id, action_info):
        icon = action_info.get('action_icon', {}).get(action_id, None)
        if icon and isinstance(self.nd.icon, CCSprite):
            self.nd.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_main/{}.png'.format(icon))
        if self.extend_ui:
            for ex_btn in self.extend_ui:
                ex_btn.destroy()

        self.extend(action_info)
        return

    def extend(self, action_info):
        self.extend_ui = []
        extend_ui = action_info.get('extend_ui', None)
        if not extend_ui:
            return
        else:
            extend_ui = extend_ui.get(self.action_id, None)
            if not extend_ui:
                return
            for ui_mod, kargs in six.iteritems(extend_ui):
                mpath = 'logic.comsys.mecha_ui.MechaControlBtn.%s' % ui_mod
                mod = sys.modules.get(mpath)
                com = getattr(mod, ui_mod, None)
                self.extend_ui.append(com(self, self.nd, kargs))

            return

    def destroy(self):
        self.mecha = None
        self.begin_func = None
        self.drag_func = None
        self.end_func = None
        self._release_repeat_check_timer()
        if self.rocker:
            self.rocker.destroy()
            self.rocker = None
        if self.progress_bar:
            self.progress_bar.Destroy(True)
            self.progress_bar = None
        for exbtn in self.extend_ui:
            exbtn.destroy()

        self.extend_ui = []
        self.last_btn = None
        self.last_touch = None
        return

    def bind_events(self, mecha, state_id=None, is_init=True):
        self.mecha = mecha
        for extend_ui in self.extend_ui:
            (is_init or getattr(extend_ui, 'force_operate_events_bound', False)) and extend_ui.bind_events(mecha)

        self.init_btn_auto_cd(state_id=state_id, is_init=is_init)
        is_init and self.setSelected(False)

    def unbind_events(self, mecha, is_init=True):
        for extend_ui in self.extend_ui:
            (is_init or getattr(extend_ui, 'force_operate_events_bound', False)) and extend_ui.unbind_events(mecha)

        self.uinit_auto_cd_btn()
        self.mecha = None
        return

    def _release_repeat_check_timer(self):
        if self.repeat_check_timer:
            global_data.game_mgr.unregister_logic_timer(self.repeat_check_timer)
            self.repeat_check_timer = None
        return

    def _register_repeat_check_timer(self):
        self._release_repeat_check_timer()
        self.repeat_check_timer = global_data.game_mgr.register_logic_timer(self.repeat_check, interval=1, times=-1)

    def repeat_check(self):
        if self.mecha and self.enabled:
            self.action_ret = self.mecha.ev_g_action_down(self.action_id)
            if self.action_ret:
                self.last_success_action_time = time.time()
            return RELEASE

    def on_begin(self, btn, touch):
        self.btn_pushing = True
        self.btn_touch_pushing = True
        self.last_btn = btn
        self.last_touch = touch
        last_down_time = self._press_down_time
        now_time = global_data.game_time
        is_double_click = now_time - last_down_time < DOUBLE_CLICK_THRESHOLD
        self._press_down_time = now_time
        if self.begin_func:
            func, args = self.begin_func
            if func:
                func(btn, touch, *args)
        if not global_data.is_key_mocking_ui_event:
            self.nd.PlayAnimation('click')
        self.last_finger_move_vec = None
        ret = False
        if self.mecha:
            if self.enabled:
                ret = self.mecha.ev_g_action_down(self.action_id, is_double_click)
            else:
                self._register_repeat_check_timer()
        if not self.enable_drag and self.rocker:
            self.rocker.enable_drag = False
        self.action_ret = ret
        if self.action_ret:
            self.last_success_action_time = time.time()
        return True

    def on_drag(self, btn, touch):
        if self.mecha and self.enabled:
            self.mecha.send_event('E_ACTION_DRAG', self.action_id)
            self.btn_dragged = True
        if self.drag_func:
            func, args = self.drag_func
            if func:
                func(btn, touch, *args)
        if self.use_drag_helper:
            self.on_btn_drag_helper(touch, self.rocker_center_wpos)

    def on_end(self, btn, touch, end_touch=True):
        if end_touch:
            self.btn_touch_pushing = False
        if not self.btn_pushing:
            return
        else:
            self.btn_pushing = False
            self._release_repeat_check_timer()
            self.last_btn = None
            self.last_touch = None
            if self.end_func:
                func, args = self.end_func
                if func:
                    func(btn, touch, *args)
            if self.is_select_btn and self.action_ret:
                self.is_selected = not self.is_selected
                self.nd.button.SetSelect(self.is_selected)
            if self.enable_drag and self.rocker:
                self.rocker.enable_drag = True
            if self.mecha and (self.enabled or self.mecha.ev_g_action_need_trigger_up_when_forbidden(self.action_id)):
                self.mecha.send_event('E_ACTION_UP', self.action_id)
            if self.btn_dragged:
                x = touch.getLocation().x - self.rocker_center_wpos.x if touch else 0
                z = touch.getLocation().y - self.rocker_center_wpos.y if touch else 0
                self.btn_dragged_dir = math3d.vector(x, 0, z)
                not self.btn_dragged_dir.is_zero and self.btn_dragged_dir.normalize()
                self.btn_dragged = False
            else:
                self.btn_dragged_dir = math3d.vector(0, 0, 0)
            return

    def init_rocker_sensitivity(self):
        from logic.gcommon.common_const import ui_operation_const
        sst_frocker_setting = global_data.player.logic.get_owner().get_setting(ui_operation_const.SST_FROCKER_KEY)
        self.sst_setting = list(sst_frocker_setting)

    def set_drag_base_val_specific(self, base_val):
        self._drag_base_val_specific = base_val

    def set_rocker_as_screen(self, as_screen):
        self._drag_as_screen = as_screen

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

    def start_count_down(self, cd_time, init_time):
        nd_cd = self.nd.nd_useless
        label = nd_cd.lab_cd_time
        progress = nd_cd.progress_cd
        nd_cd.setVisible(True)
        left_time = cd_time - init_time

        def reset():
            self.count_down = 0
            nd_cd.setVisible(False)
            if self.cd_timer:
                nd_cd.stopAction(self.cd_timer)
                self.cd_timer = None
            return

        def cb(dt):
            self.count_down = left_time - dt
            label.SetString('%.1f' % self.count_down)
            percent = self.count_down * 100.0 / cd_time
            progress.SetPercentage(percent)
            if self.count_down <= 0:
                reset()

        if self.cd_timer:
            nd_cd.stopAction(self.cd_timer)
        self.cd_timer = nd_cd.TimerAction(cb, cd_time, reset, interval=0.05)
        self.count_down = left_time
        label.SetString('%.1f' % cd_time)
        progress.SetPercentage(100)
        return True

    def stop_count_down(self):
        nd_cd = self.nd.nd_useless
        nd_cd.setVisible(False)
        if self.cd_timer:
            nd_cd.stopAction(self.cd_timer)
        self.cd_timer = None
        return

    def get_enable_ani_name(self):
        return self.action_info.get(self.action_id, {}).get('action_ani', {}).get('enbale_ani', 'enable')

    def show_count_down(self, nd_cd, percent, recover_rate, force_visible=True, need_play_enable_anim=True):
        label, progress = nd_cd.lab_cd_time, nd_cd.progress_cd
        nd_cd.setVisible(percent < 1 and percent != 0 and force_visible)
        left_time = (1 - percent) / recover_rate
        last_progress = progress.getPercentage()
        now_progress = (1 - percent) * 100
        progress.SetPercentage(now_progress)
        if left_time <= 0:
            left_time = 0
            if last_progress != now_progress and need_play_enable_anim:
                self.nd.PlayAnimation(self.get_enable_ani_name())
        label.SetString('%.1f' % left_time)

    def show_progress(self, percent, cost, need_play_enable_anim=True):
        if percent < 0:
            percent = 0 if 1 else percent
            return self.progress_bar or None
        nd_progress, bar_number = self.progress_bar, self.progress_bar.bar_number
        if bar_number > 1:
            cur_visible_bar = int(percent / cost)
            bar_len = len(self.progress_bar_elem)
            for idx in range(cur_visible_bar):
                if idx >= bar_len:
                    break
                self.progress_bar_elem[idx].setVisible(True)

            for idx in range(cur_visible_bar, bar_number):
                if idx >= bar_len:
                    break
                self.progress_bar_elem[idx].setVisible(False)

        else:
            nd_progress.img_progress_full.setVisible(percent >= 1.0)
        last_progress = nd_progress.progress.getPercentage()
        now_progress = percent * 100
        nd_progress.progress.SetPercentage(now_progress)
        if percent >= 1.0 and last_progress != now_progress and need_play_enable_anim:
            self.nd.PlayAnimation(self.get_enable_ani_name())

    def setup_progress_display(self, skill_id):
        skill_conf = confmgr.get('skill_conf', str(skill_id))
        bar_number = self.mecha.ev_g_energy_segment(skill_id)
        bar_number = bar_number if skill_conf['cost_mp_type'] == sconst.MP_COST_PER_TIMES else 1
        if self.progress_bar and self.progress_bar.bar_number == bar_number:
            return
        else:
            if self.progress_bar:
                self.progress_bar.Destroy(True)
                self.progress_bar = None
            bar_number = bar_number if bar_number in PROGRESS_BAR_LIST else 1
            progress_temp = PROGRESS_BAR_LIST[bar_number]
            self.progress_bar = global_data.uisystem.load_template_create(progress_temp, self.nd.nd_progress)
            self.progress_bar.bar_number = bar_number
            if bar_number > 1:
                self.progress_bar_elem = [ getattr(self.progress_bar, 'img_full{0}_{1}'.format(bar_number, i)) for i in range(1, bar_number + 1) ]
            return

    def on_skill_energy_changed(self, skill_id, percent, force_visible=True, need_play_enable_anim=True):
        if not (self.nd and self.nd.isValid()):
            return
        if skill_id == self.skill_id:
            if self.skill_cd_type == mecha_const.CD_TYPE_PROGRESS:
                self.show_progress(percent, self.cost, need_play_enable_anim=need_play_enable_anim)
            else:
                self.show_count_down(self.nd.nd_useless, percent, self.recover, force_visible=force_visible, need_play_enable_anim=need_play_enable_anim)
        elif skill_id == self.sub_skill_id:
            need_play_enable_anim = need_play_enable_anim and bool(self.mecha and self.mecha.ev_g_can_cast_skill(self.skill_id, show_failed_appearance=False))
            self.show_count_down(self.nd.nd_useless, percent, self.sub_recover, force_visible=force_visible, need_play_enable_anim=need_play_enable_anim)

    def on_skill_attr_updated(self, skill_id, *args):
        if self.skill_id != skill_id:
            return
        if skill_id == self.skill_id:
            if self.skill_cd_type == mecha_const.CD_TYPE_PROGRESS:
                self.setup_progress_display(self.skill_id)
                self.cost = self.mecha.ev_g_energy_cost(self.skill_id)
            else:
                self.recover = self.mecha.ev_g_energy_recover(self.skill_id)
        elif skill_id == self.sub_skill_id:
            self.sub_recover = self.mecha.ev_g_energy_recover(self.sub_skill_id)

    def _register_skill_cd_event(self, flag):
        if self.skill_cd_event_registered ^ flag:
            func = self.mecha.regist_event if flag else self.mecha.unregist_event
            func('E_ENERGY_CHANGE', self.on_skill_energy_changed)
            func('E_UPDATE_SKILL_ATTR', self.on_skill_attr_updated)
            func('E_RESET_CD_TYPE', self.on_skill_cd_reset)
            self.skill_cd_event_registered = flag

    def on_skill_cd_reset(self, skill_id, cd_type):
        if self.skill_id != skill_id:
            return
        if cd_type == mecha_const.CD_TYPE_PROGRESS:
            self.nd.PlayAnimation(self.get_enable_ani_name())
            self.nd.nd_useless.lab_cd_time.SetString('')
        self.skill_cd_type = cd_type

    def init_skill_btn(self, skill_id):
        no_progress_btn = self.action_info.get('no_progress_btn', [])
        if self.action_id in no_progress_btn:
            return
        else:
            percent = self.mecha.ev_g_energy(skill_id)
            recover = self.mecha.ev_g_energy_recover(skill_id)
            cost = self.mecha.ev_g_energy_cost(skill_id)
            skill_conf = confmgr.get('skill_conf', str(skill_id))
            cd_type = self.mecha.ev_g_skill_cd_type(skill_id)
            if cd_type is None:
                cd_type = skill_conf.get('cd_type', mecha_const.CD_TYPE_COUNTDOWN)
            if cd_type == mecha_const.CD_TYPE_PROGRESS:
                self.setup_progress_display(skill_id)
            self.recover = recover
            self.cost = cost
            self.skill_cd_type = cd_type
            self._register_skill_cd_event(True)
            self.on_skill_energy_changed(skill_id, percent)
            self.sub_skill_id = None
            if not self.is_copied:
                self.mecha.send_event('E_SKILL_BUTTON_BOUNDED', skill_id)
            return

    def init_btn_auto_cd(self, shape_id=None, state_id=None, is_init=True):
        regist_func = self.mecha.regist_event
        regist_func('E_IMMOBILIZED', self.on_immobilized)
        regist_func('E_ON_FROZEN', self.on_immobilized)
        if self.mecha.ev_g_immobilized() and is_init:
            self.on_immobilized(True, True, True)
        if self.mecha.ev_g_is_in_frozen() and is_init:
            self.on_immobilized(True)
        shape_id = shape_id or self.mecha.ev_g_shape_id()
        state_id = state_id or character_ctrl_utils.get_bind_state_id(shape_id, self.action_id)
        skill_id = self.mecha.ev_g_bind_skill(state_id)
        if not skill_id:
            self.skill_id = None
            return
        else:
            skill_conf = confmgr.get('skill_conf', str(skill_id))
            if not skill_conf:
                import traceback
                traceback.print_stack()
                log_error('!!!!!!!!!!!!!!!!!!Invalid skill id {0}!!!!!!!!!!!!!!!!!!!!'.format(skill_id))
                return
            self.skill_id = skill_id
            forbid_in_water = not skill_conf.get('ignore_water', 0)
            if forbid_in_water:
                regist_func('E_MECHA_ENTER_DIVING', self.on_add_disable_cnt)
                regist_func('E_MECHA_LEAVE_DIVING', self.on_sub_disable_cnt)
                if self.mecha.ev_g_is_diving():
                    self.on_add_disable_cnt()
            regist_func('E_ADD_SKILL', self.on_add_skill)
            regist_func('E_REMOVE_SKILL', self.on_remove_skill)
            regist_func('E_ENABLE_BY_MODULE_CARD', self.on_enable_skill_by_module)
            regist_func('E_DISABLE_BY_MODULE_CARD', self.on_disable_skill_by_module)
            ignore_auto_btn = skill_conf.get('ext_info', {}).get('ignore_auto_btn', 0)
            if skill_conf.get('max_mp', None) and skill_conf.get('cost_mp', None) and not ignore_auto_btn:
                if self.mecha.ev_g_skill(skill_id):
                    self.init_skill_btn(skill_id)
            return

    def uinit_auto_cd_btn(self):
        if not self.mecha:
            return
        else:
            unregist_func = self.mecha.unregist_event
            unregist_func('E_IMMOBILIZED', self.on_immobilized)
            unregist_func('E_ON_FROZEN', self.on_immobilized)
            unregist_func('E_ADD_SKILL', self.on_add_skill)
            unregist_func('E_REMOVE_SKILL', self.on_remove_skill)
            unregist_func('E_ENABLE_BY_MODULE_CARD', self.on_enable_skill_by_module)
            unregist_func('E_DISABLE_BY_MODULE_CARD', self.on_disable_skill_by_module)
            if self.skill_id:
                skill_conf = confmgr.get('skill_conf', str(self.skill_id))
                if not skill_conf.get('ignore_water', 0):
                    unregist_func('E_MECHA_ENTER_DIVING', self.on_add_disable_cnt)
                    unregist_func('E_MECHA_LEAVE_DIVING', self.on_sub_disable_cnt)
                    if self.mecha.ev_g_is_diving():
                        self.on_sub_disable_cnt()
            self._register_skill_cd_event(False)
            self.nd.nd_useless.setVisible(False)
            if self.progress_bar:
                self.progress_bar.Destroy(True)
                self.progress_bar = None
            return

    def switch_action_bind_skill_id(self, skill_id):
        if not self.mecha:
            return
        else:
            if not self.skill_cd_event_registered:
                return
            if self.skill_id == skill_id:
                return
            skill_obj = self.mecha.ev_g_skill(skill_id)
            self.skill_id = skill_id
            if skill_obj is None:
                self.on_skill_energy_changed(skill_id, 1.0, need_play_enable_anim=False)
                return
            if skill_obj.get_max_mp() > 0:
                self.recover = self.mecha.ev_g_energy_recover(skill_id)
                self.cost = self.mecha.ev_g_energy_cost(skill_id)
                self.on_skill_energy_changed(skill_id, self.mecha.ev_g_energy(skill_id))
            else:
                self.on_skill_energy_changed(skill_id, 1.0, need_play_enable_anim=False)
            return

    def add_action_sub_skill_id(self, sub_skill_id):
        if not sub_skill_id:
            log_error('\xe4\xbc\xa0\xe4\xb8\x80\xe4\xb8\xaa\xe7\xa9\xba\xe7\x9a\x84\xe6\x8a\x80\xe8\x83\xbdID\xe5\xb9\xb2\xe5\x98\x9b\xef\xbc\x9f\xef\xbc\x9f')
            return
        if self.skill_cd_type != mecha_const.CD_TYPE_PROGRESS:
            return
        skill_conf = confmgr.get('skill_conf', str(sub_skill_id))
        cd_type = skill_conf.get('cd_type', mecha_const.CD_TYPE_COUNTDOWN)
        if cd_type != mecha_const.CD_TYPE_COUNTDOWN:
            return
        self.sub_skill_id = sub_skill_id
        self.sub_recover = self.mecha.ev_g_energy_recover(sub_skill_id)
        self.sub_cost = self.mecha.ev_g_energy_cost(sub_skill_id)
        percent = self.mecha.ev_g_energy(sub_skill_id)
        self.on_skill_energy_changed(sub_skill_id, percent, need_play_enable_anim=False)

    def del_action_sub_skill_id(self):
        if not self.sub_skill_id:
            return
        else:
            self.on_skill_energy_changed(self.sub_skill_id, 100, need_play_enable_anim=False)
            self.sub_skill_id = None
            self.sub_recover = 0
            self.sub_cost = 0
            return

    def on_add_skill(self, skill_id, skill_data=None):
        if self.skill_id == skill_id and not self.nd.isVisible():
            self.nd.setVisible(True)
            if self.nd_temp_pc:
                self.nd_temp_pc.setVisible(True)
            skill_conf = confmgr.get('skill_conf', str(skill_id))
            if skill_conf.get('max_mp', None) and skill_conf.get('cost_mp', None):
                self.init_skill_btn(skill_id)
        return

    def on_remove_skill(self, skill_id):
        if self.skill_id == skill_id:
            if self.action_id not in self.action_info['visible_btn']:
                self.nd.setVisible(False)
                if self.nd_temp_pc:
                    self.nd_temp_pc.setVisible(False)

    def on_enable_skill_by_module(self, skill_id, *args):
        self.on_add_skill(skill_id)

    def on_disable_skill_by_module(self, skill_id, *args):
        self.on_remove_skill(skill_id)

    def stop_btn(self):
        self.rocker.stop_btn()

    def on_add_disable_cnt(self):
        self.disable_cnt += 1
        self.setEnable(self.disable_cnt <= 0)
        self.nd.img_broken.setVisible(self.disable_cnt > 0)
        if self.disable_cnt > 0:
            self.stop_btn()

    def on_sub_disable_cnt(self):
        self.disable_cnt -= 1
        self.setEnable(self.disable_cnt <= 0)
        self.nd.img_broken.setVisible(self.disable_cnt > 0)

    def on_immobilized(self, immobilized, fall=False, is_soft=False, *args):
        if is_soft and self.action_id in WEAPON_IDS:
            return
        self.setForbidden(immobilized, 'immobilized')

    def setVisible--- This code section failed: ---

 718       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'True'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     24  'to 24'

 719      12  LOAD_GLOBAL           1  'True'
          15  LOAD_FAST             0  'self'
          18  STORE_ATTR            2  'is_nb_visible'
          21  JUMP_FORWARD          0  'to 24'
        24_0  COME_FROM                '21'

 720      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             3  'nd'
          30  LOAD_ATTR             4  'setVisible'
          33  LOAD_FAST             1  'visible'
          36  JUMP_IF_FALSE_OR_POP    45  'to 45'
          39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             2  'is_nb_visible'
        45_0  COME_FROM                '36'
          45  CALL_FUNCTION_1       1 
          48  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def isVisible(self):
        return self.nd.isVisible()

    def setOffset(self, offset):
        self.nd.SetPosition(offset)

    def enableRocker(self, enable_rocker):
        if self.rocker:
            self.rocker.enable_drag = enable_rocker
        self.enable_drag = enable_rocker

    def resetRocker(self):
        if self.enable_drag and self.rocker:
            self.rocker.enable_drag = self.enable_drag

    def startCountDown(self, cd_time, init_time=0):
        self.start_count_down(cd_time, init_time)

    def stopCountDown(self):
        self.stop_count_down()

    def setEnable(self, enable):
        self.enabled = enable
        if not enable:
            if self.btn_pushing and not self.repeat_check_timer:
                self._register_repeat_check_timer()

    def setForbidden(self, forbidden, reason=None):
        if reason is None:
            self.disable_cnt += 1 if forbidden else -1
        elif forbidden:
            self.disable_reason.add(reason)
        elif reason in self.disable_reason:
            self.disable_reason.remove(reason)
        enable = self.disable_cnt <= 0 and not self.disable_reason
        self.setEnable(enable)
        self.nd.img_broken.setVisible(not enable)
        if self.btn_pushing and not self.enabled:
            self.on_end(self.last_btn, self.last_touch, False)
        if enable and self.mecha and self.btn_touch_pushing:
            self.on_begin(self.last_btn, self.last_touch)
        return

    def setSelected(self, selected):
        self.is_selected = selected
        self.nd.button.SetSelect(self.is_selected)

    def enableCustomState(self, enable):
        self.nd.button.EnableCustomState(enable)

    def setOnBeginCallback(self, func, *args):
        if func:
            self.begin_func = (
             func, args)
        else:
            self.begin_func = None
        return

    def setOnDragCallback(self, func, *args):
        if func:
            self.drag_func = (
             func, args)
        else:
            self.drag_func = None
        return

    def setOnEndCallback(self, func, *args):
        if func:
            self.end_func = (
             func, args)
        else:
            self.end_func = None
        return

    def setSwallowTouch(self, bSwallowTouch):
        self.nd.bar.SetSwallowTouch(bSwallowTouch)

    def setIcon(self, icon_path, show_anim_name=''):
        if self.nd.button.icon.SetDisplayFrameByPath:
            self.nd.button.icon.SetDisplayFrameByPath('', icon_path)
        show_anim_name and self.nd.PlayAnimation(show_anim_name)

    def refresh_rocker(self):
        if self.nd:
            self.rocker_center_wpos = self.nd.nd_pos.ConvertToWorldSpacePercentage(50, 50)
        if self.rocker:
            self.rocker.init_rocker()
        for extend_ui in self.extend_ui:
            if hasattr(extend_ui, 'refresh_rocker') and extend_ui.refresh_rocker:
                extend_ui.refresh_rocker()


class ControlBtnPC(ControlBtn):

    def on_begin(self, btn, touch):
        self.btn_pushing = True
        self.last_btn = btn
        self.last_touch = touch
        last_down_time = self._press_down_time
        now_time = global_data.game_time
        is_double_click = now_time - last_down_time < DOUBLE_CLICK_THRESHOLD
        self._press_down_time = now_time
        if self.begin_func:
            func, args = self.begin_func
            if func:
                func(btn, touch, *args)
        self.nd.PlayAnimation('click')
        if self.action_id != 'action1':
            self.nd.click_vx.SetPosition('50%-9', '50%3')
        self.last_finger_move_vec = None
        ret = False
        if self.mecha and self.enabled:
            ret = self.mecha.ev_g_action_down(self.action_id, is_double_click)
        if not self.enable_drag and self.rocker:
            self.rocker.enable_drag = False
        self.action_ret = ret
        return True

    def setup_progress_display(self, skill_id):
        skill_conf = confmgr.get('skill_conf', str(skill_id))
        bar_number = self.mecha.ev_g_energy_segment(skill_id)
        bar_number = bar_number if skill_conf['cost_mp_type'] == sconst.MP_COST_PER_TIMES else 1
        if self.progress_bar and self.progress_bar.bar_number == bar_number:
            return
        else:
            if self.progress_bar:
                self.progress_bar.Destroy(True)
                self.progress_bar = None
            bar_number = bar_number if bar_number in PC_PROGRESS_BAR_LIST else 1
            progress_temp = PC_PROGRESS_BAR_LIST[bar_number]
            self.progress_bar = global_data.uisystem.load_template_create(progress_temp, self.nd.nd_progress)
            self.progress_bar.bar_number = bar_number
            if bar_number > 1:
                self.progress_bar_elem = [ getattr(self.progress_bar, 'img_full{0}_{1}'.format(bar_number, i)) for i in range(1, bar_number + 1) ]
            return

    def extend(self, action_info):
        self.extend_ui = []
        extend_ui = action_info.get('extend_ui_pc', None)
        if not extend_ui:
            return
        else:
            extend_ui = extend_ui.get(self.action_id, None)
            if not extend_ui:
                return
            for ui_mod, kargs in six.iteritems(extend_ui):
                mpath = 'logic.comsys.mecha_ui.MechaControlBtn.%s' % ui_mod
                mod = sys.modules.get(mpath)
                com = getattr(mod, ui_mod, None)
                self.extend_ui.append(com(self, self.nd, kargs))

            return