# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNewbieFourGuide.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.gutils import newbie_stage_utils, task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import math3d
from data.newbie_stage_config import GetStageFour
from logic.comsys.guide_ui.GuideUI import GuideUI, LeaveGuideUI, PCGuideUI
from logic.comsys.guide_ui.NewbieStageSideTipUI import NewbieStageSideTipUI
from data.c_guide_data import GetLocalGuide, get_init_guide_data
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.IdManager import IdManager
import logic.gcommon.const as const
import logic.gutils.delay as delay
from logic.client.const import game_mode_const
from common.utils.timer import CLOCK
from common.cfg import confmgr
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import mecha_const as mconst
from logic.gcommon import time_utility as tutil
import random
from logic.gutils.mecha_utils import get_mecha_call_pos
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.item import item_const
from logic.gcommon.item.item_utility import is_deadbox, is_scenebox

class ComNewbieFourGuide(UnitCom):
    BIND_EVENT = {'E_FINISH_GUIDE': 'finish_guide',
       'E_GUIDE_DESTROY': 'destroy_battle_guide',
       'G_GUIDE_CAN_MOVE': '_can_move',
       'E_GUIDE_POS_CHECK': '_regist_check_pos',
       'E_LOCAL_BATTLE_ESC_4': 'on_click_quit_btn'
       }

    def __init__(self):
        super(ComNewbieFourGuide, self).__init__()
        self.barrier_center = None
        self.barrier_radius = None
        self.riko_tip_timer = None
        self.hint_tip_timer = None
        self._move_timer = None
        self._check_leave_timer = None
        self._move_enable = True
        self._sfx_map = {}
        self._robot_dead_delay_call = None
        self._poison_refresh_delay_call = None
        self._poison_reduce_delay_call = None
        self._signal_delay_call = None
        self._signal_repeat_timer = None
        self._lock_move_delay_call = None
        self._call_mecha_pos_valid = False
        self._robot_statistic_guide_id = -1
        self._need_robot_num = 0
        self.finished_guides = set()
        self._use_drug_guide_id = 0
        self._call_mecha_guide_id = 0
        self._destroy_mecha_guide_id = 0
        self._delay_show_side_ui_guide_id = 0
        self._has_enter_guide = False
        self._ace_start_point = 0
        self._driver_level = 0
        self._pick_animation_guide_id = None
        self._pick_items_has_show = False
        self._regist_throw_explosion_event_flag = False
        self._locale_battle_server = None
        self._intro_step_guide_id = 0
        self._scene_box_pick_guide_id = 0
        self._is_reducing_poison = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComNewbieFourGuide, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        if not self.battle:
            return
        battle_tid = self.battle.get_battle_tid()
        if battle_tid != game_mode_const.NEWBIE_STAGE_FOURTH_BATTLE_TYPE:
            return
        global_data.emgr.scene_pick_show_item_list += self.on_show_pick_ui_items
        global_data.emgr.scene_update_pick_info_event += self.scene_update_pick_info
        global_data.emgr.show_big_map_ui_event += self.on_big_map_show
        if global_data.ui_mgr.get_ui('BattleLoadingWidget'):
            global_data.emgr.battle_loading_finished_event += self.start_guide_logic
        else:
            self.start_guide_logic(False)

    def _can_move(self):
        return self._move_enable

    @property
    def _guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()

    @property
    def side_tip_ui(self):
        return NewbieStageSideTipUI()

    def is_finished_guide(self, guide_id):
        return guide_id in self.finished_guides

    def add_finished_guide(self, guide_id):
        self.finished_guides.add(guide_id)

    def start_guide_logic(self, event_flag=True):
        if event_flag:
            global_data.emgr.battle_loading_finished_event -= self.start_guide_logic
        self._guide_ui.hide_main_ui()
        self.init_quit_ui()
        self.update_setting_quit_button()
        guide_id = 100
        newbie_stage_utils.propel_guide(guide_id, self)
        self._has_enter_guide = True
        self._need_robot_num = 0
        self._robot_statistic_guide_id = -1
        self._need_robot_num = 0
        self.unit_obj.regist_event('E_PICK_UP_OTHERS', self.on_pick_up_others)
        self.unit_obj.regist_event('E_GUIDE_PICK_UNROLL_PACKAGE', self.on_pick_unroll_package)
        self.process_barrier_boundary_check(self.unit_obj, check=True)
        self.process_throw_item_explosion_event()

    def process_barrier_boundary_check(self, unit_obj, check=False):
        if not unit_obj:
            return
        if not self.battle:
            return
        battle_tid = self.battle.get_battle_tid()
        if battle_tid != game_mode_const.NEWBIE_STAGE_FOURTH_BATTLE_TYPE:
            return
        self.barrier_center, self.barrier_radius = self.battle.get_barrier_range()
        if G_POS_CHANGE_MGR:
            if check:
                unit_obj.regist_pos_change(self.check_pos, 0.1)
            else:
                unit_obj.unregist_pos_change(self.check_pos)
        elif check:
            unit_obj.regist_event('E_POSITION', self.check_pos)
        else:
            unit_obj.unregist_event('E_POSITION', self.check_pos)

    def check_pos(self, pos):
        if self.barrier_center is None or self.barrier_radius is None:
            return
        else:
            delta_vec = math3d.vector(pos.x, 0, pos.z) - math3d.vector(self.barrier_center.x, 0, self.barrier_center.z)
            if delta_vec.length >= self.barrier_radius - 60:
                self.send_event('E_SHOW_MESSAGE', get_text_by_id(5200))
            return

    def init_quit_ui(self):
        if global_data.is_pc_mode:
            return
        self._guide_ui.show_main_ui_by_type('BattleRightTopUI')
        battle_right_top_ui = global_data.ui_mgr.get_ui('BattleRightTopUI')
        if not battle_right_top_ui:
            return
        battle_right_top_ui.show_only_exit_btn()

        def on_click_quit_btn(*args):
            if not self.battle:
                return
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            dlg = SecondConfirmDlg2()
            battle_type = self.battle.get_battle_tid()
            assessment_tid = task_utils.get_certificate_task_id_by_battle_type(battle_type)
            if global_data.player.is_task_finished(assessment_tid):
                tip_text_id = 5017
            else:
                tip_text_id = 607241

            def on_confirm():
                dlg.close()
                global_data.player.quit_battle()

            dlg.confirm(content=get_text_by_id(tip_text_id), confirm_callback=on_confirm)

        battle_right_top_ui.btn_exit.BindMethod('OnClick', on_click_quit_btn)

    def on_click_quit_btn(self, *args):
        if not self.battle:
            return
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        dlg = SecondConfirmDlg2()
        battle_type = self.battle.get_battle_tid()
        assessment_tid = task_utils.get_certificate_task_id_by_battle_type(battle_type)
        if global_data.player.is_task_finished(assessment_tid):
            tip_text_id = 5017
        else:
            tip_text_id = 607241

        def on_confirm():
            dlg.close()
            global_data.player.quit_battle()

        dlg.confirm(content=get_text_by_id(tip_text_id), confirm_callback=on_confirm)

    def init_guide_data(self, guide_id):
        info = get_init_guide_data(guide_id)
        if info:
            self.init_weapons(info.get('weapons', None))
            self.init_items(info.get('items', None))
            self.init_mecha_progress(info.get('mecha_progress', None))
            self.init_mecha(info.get('mecha', None))
            self.init_hp(info.get('hp', None))
        return

    def init_show_main_ui(self, guide_id):
        cfg = self.get_guide_data(guide_id)
        prior = cfg.get('Prior', None)
        if prior:
            self.show_main_ui(self.guid_cfg(prior).get('NextShowMainUI', None))
            self.init_show_main_ui(prior)
        return

    def init_hp(self, hp):
        if hp:
            self.send_event('S_HP', hp)

    def init_mecha(self, mecha):
        if mecha:
            pos = self.ev_g_position()
            self._get_lbs()._lbs_create_mecha(mecha, (pos.x, pos.y, pos.z))
            ui = global_data.ui_mgr.get_ui('PostureControlUI')
            if ui:
                ui.panel.setVisible(False)

    def init_mecha_progress(self, progress):
        if progress:
            ui = global_data.ui_mgr.get_ui('MechaUI')
            if ui:
                ui.clear_mecha_cd_timer()
                ui.on_add_mecha_progress(100)
                ui.get_mecha_count_down = 0
                ui.get_mecha_count_down_progress = 0

    def init_weapons(self, weapons):
        if weapons:
            if isinstance(weapons, (list, tuple)):
                for weapon in weapons:
                    self._add_weapon(weapon)

            else:
                self._add_weapon(weapons)

    def _add_weapon(self, weapon_id):
        iMagSize = confmgr.get('firearm_config', str(weapon_id))['iMagSize']
        item_data = {'item_id': weapon_id,'entity_id': IdManager.genid(),'count': 1,'iBulletNum': iMagSize}
        if weapon_id == 1011:
            self.send_event('E_PICK_UP_WEAPON', item_data, const.PART_WEAPON_POS_MAIN_DF, False)
            if not self.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN1):
                self.send_event('E_SWITCHING', const.PART_WEAPON_POS_MAIN_DF)
        else:
            self.send_event('E_PICK_UP_WEAPON', item_data, -1)
            if not self.ev_g_weapon_data(const.PART_WEAPON_POS_MAIN_DF):
                self.send_event('E_SWITCHING', const.PART_WEAPON_POS_MAIN1)

    def add_weapon_by_pos(self, weapon_id, weapon_pos):
        iMagSize = confmgr.get('firearm_config', str(weapon_id))['iMagSize']
        item_data = {'item_id': weapon_id,'entity_id': IdManager.genid(),'count': 1,'iBulletNum': iMagSize}
        self.send_event('E_PICK_UP_WEAPON', item_data, weapon_pos, False)

    def init_items(self, items):
        if items:
            for item_id, count in six.iteritems(items):
                self._add_item(item_id, count)

    def _add_item(self, item_id, count):
        item_data = {'item_id': item_id,'entity_id': IdManager.genid(),'count': count}
        self.send_event('E_PICK_UP_OTHERS', item_data)

    def update_setting_quit_button(self):
        self.unit_obj.regist_event('E_GUIDE_OPEN_MAIN_SETTING', self.on_open_main_setting)
        self.unit_obj.regist_event('E_GUIDE_CLOSE_MAIN_SETTING', self.on_close_main_setting)

    def on_open_main_setting(self, setting_ui):
        self._guide_ui.panel.setVisible(False)
        if setting_ui and setting_ui.ref_btn_exit:
            setting_ui.ref_btn_exit.btn.SetText(5030)

    def on_close_main_setting(self, *args):
        self._guide_ui.panel.setVisible(True)

    def extra_finish_process(self, guide_id):
        if guide_id == 1604:
            battle_type = self.battle.get_battle_tid()
            newbie_stage_utils.finish_local_battle_guide(battle_type)

    def get_guide_data(self, guide_id):
        return GetStageFour()[guide_id]

    def show_main_ui(self, ui_list):
        if ui_list:
            if isinstance(ui_list, (list, tuple)):
                for key in ui_list:
                    self._guide_ui.show_main_ui_by_type(key)

            else:
                self._guide_ui.show_main_ui_by_type(ui_list)

    def _regist_check_pos(self, lmecha, flag):
        pass

    def empty_guide_holder(self, guide_id, *args):
        newbie_stage_utils.finish_guide(guide_id, self)

    def highlight_parachute_launch(self, guid_id, *args):
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed

    def on_player_parachute_stage_changed(self, stage):
        if stage == parachute_utils.STAGE_LAUNCH_PREPARE:
            prepare_ui = global_data.ui_mgr.get_ui('PrepareUI')
            if prepare_ui:
                prepare_ui.high_light_btn_launch()

    def empty_guide_holder_destroy(self, *args):
        pass

    def show_intro_steps(self, guide_id, ui_name, ui_path):
        global_data.ui_mgr.show_ui(ui_name, ui_path)
        self._intro_step_guide_id = guide_id

    def guide_close_intro_steps(self, *args):
        if self._intro_step_guide_id > 0:
            self.finish_guide(self._intro_step_guide_id)

    def show_intro_steps_destroy(self, guide_id, *_):
        self._intro_step_guide_id = 0

    def create_items(self, guide_id, item_list):
        self._get_lbs()._lbs_create_items(guide_id, item_list)

    def create_items_destroy(self, *args):
        pass

    def create_pick_item(self, guide_id, item_no, pos, sub_items):
        self._get_lbs()._lbs_create_pick_item(guide_id, item_no, pos, sub_items)
        if is_scenebox(item_no):
            self._scene_box_pick_guide_id = guide_id
        target_pos = math3d.vector(*pos)
        lplayer = global_data.player.logic
        if not lplayer:
            return
        lpos = lplayer.ev_g_position()
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = lplayer.ev_g_yaw() or 0
                global_data.emgr.camera_set_yaw_event.emit(target_yaw)
                global_data.emgr.camera_set_pitch_event.emit(0)
                lplayer.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def create_pick_item_destroy(self, *_):
        self._get_lbs()._lbs_destroy_item()
        self._guide_ui.deal_human_tips(None)
        self._scene_box_pick_guide_id = 0
        return

    def change_player_head(self, guide_id, target_pos):
        lplayer = global_data.player.logic
        if not lplayer:
            return
        target_pos = math3d.vector(*target_pos)
        lpos = lplayer.ev_g_position()
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = lplayer.ev_g_yaw() or 0
                global_data.emgr.camera_set_yaw_event.emit(target_yaw)
                global_data.emgr.camera_set_pitch_event.emit(0)
                lplayer.send_event('E_DELTA_YAW', target_yaw - cur_yaw)
        newbie_stage_utils.finish_guide(guide_id, self)

    def change_player_head_destroy(self, guide_id, *args):
        pass

    def _check_mov(self, guide_id, pos, offset):
        m_pos = global_data.player.logic.ev_g_position()
        dist = math3d.vector(*pos) - m_pos
        if dist.length < offset * NEOX_UNIT_SCALE:
            newbie_stage_utils.finish_guide(guide_id, self)

    def check_move_pos(self, guide_id, pos, offset):
        self._move_timer = global_data.game_mgr.register_logic_timer(lambda : self._check_mov(guide_id, pos, offset), interval=0.1, mode=CLOCK)

    def check_move_pos_destroy(self, *_):
        if self._move_timer:
            global_data.game_mgr.unregister_logic_timer(self._move_timer)
            self._move_timer = None
        return

    def _check_leave_area(self, guide_id, pos, offset):
        m_pos = global_data.player.logic.ev_g_position()
        dist = math3d.vector(*pos) - m_pos
        if dist.length > offset * NEOX_UNIT_SCALE:
            newbie_stage_utils.finish_guide(guide_id, self)

    def check_leave_area(self, guide_id, pos, offset):
        self._check_leave_timer = global_data.game_mgr.register_logic_timer(lambda : self._check_leave_area(guide_id, pos, offset), interval=0.1, mode=CLOCK)

    def check_leave_area_destroy(self, *_):
        if self._check_leave_timer:
            global_data.game_mgr.unregister_logic_timer(self._check_leave_timer)
            self._check_leave_timer = None
        return

    def guide_pick_specific_items(self, guide_id):
        newbie_stage_utils.finish_guide(guide_id, self)

    def guide_pick_other_item(self, guide_id, item_id):
        newbie_stage_utils.finish_guide(guide_id, self)

    def show_sfx(self, guide_id, position, path):

        def _on_target_pos_sfx(sfx):
            if self and self.is_valid():
                self._sfx_map[guide_id] = sfx
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*position), on_create_func=_on_target_pos_sfx)

    def show_sfx_destroy(self, guide_id, *_):
        if guide_id in self._sfx_map:
            global_data.sfx_mgr.remove_sfx(self._sfx_map[guide_id])
            del self._sfx_map[guide_id]

    def show_locate(self, guide_id, pos, offset, layer, animation_name=None):
        self._guide_ui.show_locate(pos, offset, layer, animation_name)

    def show_locate_destroy(self, guide_id, pos, offset, layer, animation_name=None):
        self._guide_ui.show_locate_destroy(layer, animation_name)

    def show_riko_tips(self, guide_id, text_id, time_out, time_before=0, propel_ids=None, pc_text_id=0):
        if global_data.is_pc_mode and pc_text_id > 0:
            text_id = pc_text_id
        if propel_ids is None or propel_ids <= 0:
            propel_ids = None
        if time_before == 0:
            self.show_riko_tips_imp(guide_id, text_id, time_out, propel_ids)
        else:
            self.riko_tip_timer = delay.call(time_before, lambda gid=guide_id, t_id=text_id, t_out=time_out, p_ids=propel_ids: self.show_riko_tips_imp(gid, t_id, t_out, p_ids))
        return

    def show_riko_tips_imp(self, guide_id, text_id, time_out, propel_ids):
        self.riko_tip_timer = None
        guide_data = self.get_guide_data(guide_id)
        if guide_data.get('Next', None):
            self._guide_ui.show_human_tips(get_text_by_id(text_id), time_out, lambda g_id=guide_id: newbie_stage_utils.finish_guide(g_id, self))
        elif propel_ids:
            self._guide_ui.show_human_tips(get_text_by_id(text_id), time_out, lambda g_ids=propel_ids: newbie_stage_utils.propel_guide_multiple(g_ids, self))
        else:
            self._guide_ui.show_human_tips(get_text_by_id(text_id), time_out)
        return

    def show_riko_tips_destroy(self, *args):
        if self.riko_tip_timer:
            delay.cancel(self.riko_tip_timer)
            self.riko_tip_timer = None
        return

    def show_temp_tips(self, guide_id, text_id, time_out, propel_ids=None, pc_text_id=None):
        if global_data.is_pc_mode and pc_text_id > 0:
            text_id = pc_text_id
        if propel_ids is None or propel_ids <= 0:
            propel_ids = None
        cfg = self.get_guide_data(guide_id)
        if cfg.get('Next', None):
            self._guide_ui.show_temp_tips(get_text_local_content(text_id), time_out, lambda step=guide_id: self.finish_guide(step))
        elif propel_ids:
            self._guide_ui.show_temp_tips(get_text_local_content(text_id), time_out, --- This code section failed: ---

 507       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'propel_steps'
           6  LOAD_ATTR             1  'True'
           9  LOAD_GLOBAL           1  'True'
          12  CALL_FUNCTION_257   257 
          15  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_257' instruction at offset 12
)
        else:
            self._guide_ui.show_temp_tips(get_text_local_content(text_id), time_out)
        return

    def show_temp_tips_destroy(self, *args):
        self._guide_ui.show_temp_tips_destroy()

    def show_target_sfx(self, guide_id, target_pos, path):

        def create_func(sfx):
            if self and self.is_valid():
                self.sfx_map[guide_id] = sfx
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*target_pos), on_create_func=create_func)

    def show_target_sfx_destroy(self, guide_id, *args):
        if guide_id in self.sfx_map:
            global_data.sfx_mgr.remove_sfx(self.sfx_map[guide_id])
            del self.sfx_map[guide_id]

    def show_locate_ui(self, guide_id, target_pos, offset, layer, animation_name=None):
        self._guide_ui.show_locate(target_pos, offset, layer, animation_name)

    def show_locate_ui_destroy(self, guide_id, target_pos, offset, layer, animation_name=None):
        self._guide_ui.show_locate_destroy(layer, animation_name)

    def destroy_steps(self, steps, force=None):
        if steps:
            if isinstance(steps, (list, tuple)):
                for step in steps:
                    self.destroy_guide(step, force)

            else:
                self.destroy_guide(steps, force)

    def show_main_ui(self, ui_list):
        if ui_list:
            if isinstance(ui_list, (list, tuple)):
                for key in ui_list:
                    self._guide_ui.show_main_ui_by_type(key)

            else:
                self._guide_ui.show_main_ui_by_type(ui_list)

    def guide_shoot_show(self, is_show):
        if is_show:
            self.show_nd_animation(None, 'nd_step_3', 'show_3')
            if not global_data.is_pc_mode:
                self.update_auto_frame()
            self.show_nd_animation(None, 'temp_move_tips', 'show')
            self.show_nd_animation(None, 'nd_auto_frame', 'show_auto')
        else:
            self.show_nd_animation_destroy(None, 'nd_step_3', 'show_3')
            self.show_nd_animation_destroy(None, 'nd_auto_frame', 'show_auto')
            self.show_nd_animation_destroy(None, 'temp_move_tips', 'show')
        return

    def update_auto_frame(self):
        weapon = self.sd.ref_wp_bar_cur_weapon
        aim_args = self.ev_g_at_aim_args_all()
        self._guide_ui.update_auto_frame(weapon, aim_args)

    def show_nd_animation(self, guide_id, layer, animation):
        if global_data.is_pc_mode and layer in {'temp_use_tips', 'nd_step_3', 'nd_auto_frame'}:
            return
        else:
            tip_text_id = None
            if layer == 'nd_step_3':
                tip_text_id = 5198
            self._guide_ui.play_nd_animation(layer, animation, tip_text_id)
            return

    def show_nd_animation_destroy(self, guide_id, layer, animation):
        if global_data.is_pc_mode and layer in {'temp_use_tips', 'nd_step_3', 'nd_auto_frame'}:
            return
        self._guide_ui.play_nd_animation_destroy(layer, animation)

    def create_robot(self, guide_id, interval, pos, max_hp, shoot=False):
        self._get_lbs()._lbs_create_robot(guide_id, interval, pos, max_hp, shoot)

    def create_robot_destroy(self, *_):
        self._get_lbs()._lbs_destroy_robot()

    def create_end_ui(self, guide_id, *args):
        from logic.comsys.guide_ui.NewbieStageEndUI import NewbieStageEndUI

        def end_ui_cb():
            self.unregist_throw_item_explosion_event()
            newbie_stage_utils.finish_guide(guide_id, self)

        NewbieStageEndUI(None, end_ui_cb)
        return

    def create_end_ui_destroy(self, *args):
        pass

    def finish_guide(self, guide_id):
        newbie_stage_utils.finish_guide(guide_id, self)

    def create_items_destroy(self, *args):
        pass

    def refresh_poison_circle(self, guid_id, delay_time, state, last_time, level, poison_point, safe_point, reduce_type):
        from logic.gcommon import time_utility as tutil
        if delay_time > 0:
            self._poison_refresh_delay_call = delay.call(delay_time, lambda : self._delay_refresh_poison_circle(guid_id, state, last_time, level, poison_point, safe_point, reduce_type))
        else:
            self._get_lbs()._lbs_refresh_poison_circle(guid_id, state, tutil.get_time(), last_time, level, poison_point, safe_point, reduce_type)

    def _delay_refresh_poison_circle(self, guide_id, state, last_time, level, poison_point, safe_point, reduce_type):
        from logic.gcommon import time_utility as tutil
        self._poison_refresh_delay_call = None
        self._get_lbs()._lbs_refresh_poison_circle(guide_id, state, tutil.get_time(), last_time, level, poison_point, safe_point, reduce_type)
        return

    def refresh_poison_circle_destroy(self, *args):
        if self._poison_refresh_delay_call:
            delay.cancel(self._poison_refresh_delay_call)
            self._poison_refresh_delay_call = None
        return

    def reduce_poison_circle(self, guide_id, delay_time, state, last_time, reduce_type):
        from logic.gcommon import time_utility as tutil
        refresh_time = tutil.get_time()
        if delay_time > 0:
            self._poison_reduce_delay_call = delay.call(delay_time, lambda : self._delay_reduce_poison_circle(guide_id, state, refresh_time, last_time, reduce_type))
        else:
            self._get_lbs()._lbs_reduce_poison_circle(guide_id, state, refresh_time, last_time, reduce_type)
            self._show_map_signal_tip()

    def _delay_reduce_poison_circle(self, guide_id, state, reduce_type, refresh_time, last_time):
        self._poison_reduce_delay_call = None
        self._get_lbs()._lbs_reduce_poison_circle(guide_id, state, reduce_type, refresh_time, last_time)
        self._show_map_signal_tip()
        return

    def _show_map_signal_tip(self):
        self._is_reducing_poison = True
        global_data.emgr.scene_show_big_map_event.emit()

    def on_big_map_show(self):
        if not self._is_reducing_poison:
            return
        map = global_data.ui_mgr.get_ui('BigMapUI')
        if not map:
            return
        try:
            guide_data = self.get_guide_data(906)
            guide_args = guide_data.get('Args', []) if guide_data else []
            if not guide_args or len(guide_args) < 3:
                return
            poison_circle_center = tuple(guide_args[2])
            map.show_signal_tip()
            map.on_scale_callback(100)
            map.mark_ctrl_widget.move_to_locate(poison_circle_center)
            self._is_reducing_poison = False
        except Exception as e:
            log_error('ComNewbieFourGuide on_big_map_show exception=%s', e)

    def reduce_poison_circle_destroy(self, *args):
        if self._poison_reduce_delay_call:
            delay.cancel(self._poison_reduce_delay_call)
            self._poison_reduce_delay_call = None
        self._is_reducing_poison = False
        return

    def clear_poison_circle_destroy(self, guide_id, *args):
        pass

    def clear_poison_circle(self, guide_id):
        self._get_lbs()._lbs_clear_poison()
        newbie_stage_utils.finish_guide(guide_id, self)

    def reduce_avatar_signal(self, guide_id, to_percent):
        if not battle_utils.is_battle_signal_open():
            return
        reduce_amount = global_data.player.logic.ev_g_signal() - global_data.player.logic.ev_g_max_signal() * to_percent
        if reduce_amount > 0:
            global_data.player.logic.ev_g_sub_signal(reduce_amount)
            newbie_stage_utils.finish_guide(guide_id, self)

    def reduce_avatar_signal_destroy(self, guide_id, *args):
        pass

    def tick_avatar_signal(self, guide_id, delay_time, reduce_rate, safe_point, offset):
        if not battle_utils.is_battle_signal_open():
            return
        if delay_time > 0:
            self._signal_delay_call = delay.call(delay_time, lambda : self._tick_avatar_signal(guide_id, reduce_rate, safe_point, offset))
        else:
            self._tick_avatar_signal(guide_id, reduce_rate, safe_point, offset)

    def tick_avatar_signal_destroy(self, guide_id, *args):
        pass

    def destroy_signal(self):
        if self._signal_delay_call:
            delay.cancel(self._signal_delay_call)
            self._signal_delay_call = None
        if self._signal_repeat_timer:
            global_data.game_mgr.unregister_logic_timer(self._signal_repeat_timer)
            self._signal_repeat_timer = None
        return

    def _tick_avatar_signal(self, guide_id, reduce_rate, safe_point, offset):
        self._signal_delay_call = None
        self._signal_repeat_timer = global_data.game_mgr.register_logic_timer(lambda : self._check_reduce_signal(guide_id, reduce_rate, safe_point, offset), interval=0.5, mode=CLOCK)
        guide_data = self.get_guide_data(guide_id)
        newbie_stage_utils.propel_guide_multiple(guide_data.get('Next'), self, guide_data.get('NextShowMainUI'))
        return

    def _check_reduce_signal(self, guide_id, reduce_rate, safe_point, offset):
        m_pos = global_data.player.logic.ev_g_position()
        dist = math3d.vector(*[safe_point[0], 0, safe_point[2]]) - math3d.vector(*[m_pos.x, 0, m_pos.z])
        is_in_mecha = global_data.player.logic.ev_g_in_mecha('Mecha')
        if dist.length > offset * NEOX_UNIT_SCALE:
            if not global_data.player.logic.ev_g_signal_in_poison():
                self._guide_ui.show_temp_tips(5254, 1)
            global_data.player.logic.send_event('E_IN_POISON', True)
            global_data.player.logic.send_event('E_SIGNAL_RATE_CHANGE', True, reduce_rate)
            if is_in_mecha:
                mecha = global_data.player.logic.ev_g_control_target().logic
                if mecha and mecha.ev_g_hp() > 1:
                    mecha.ev_g_damage(reduce_rate * 2)
            elif global_data.player.logic.ev_g_signal() > 10:
                global_data.player.logic.ev_g_sub_signal(reduce_rate * 2)
        else:
            global_data.player.logic.send_event('E_IN_POISON', False)
            if global_data.player.logic.ev_g_signal_percent() < 1.0:
                global_data.player.logic.send_event('E_RECOVER_SIGNAL', reduce_rate)
            if is_in_mecha:
                mecha = global_data.player.logic.ev_g_control_target().logic
                if mecha and not mecha.ev_g_full_hp():
                    mecha.send_event('S_HP', mecha.ev_g_hp() + reduce_rate)

    def show_multi_human_tips(self, guide_id, text_id_list, time_out, propel_ids=None):
        text_list = [ get_text_local_content(text_id) for text_id in text_id_list ]
        self._guide_ui.show_multi_human_tips(text_list, time_out)

    def show_multi_human_tips_destroy(self, *args):
        self._guide_ui.show_multi_human_tips_destroy()

    def lock_move(self, guide_id, last_time):
        self._move_enable = False
        self._lock_move_delay_call = delay.call(last_time, lambda : self._enable_move(guide_id))

    def _enable_move(self, guide_id):
        self._lock_move_delay_call = None
        self._move_enable = True
        newbie_stage_utils.finish_guide(guide_id, self)
        return

    def lock_move_destroy(self, *args):
        if self._lock_move_delay_call:
            delay.cancel(self._lock_move_delay_call)
            self._lock_move_delay_call = None
        return

    def show_use_drug_tip(self, guide_id, text_id, time_out):
        self._guide_ui.show_temp_use_tips(text_id, time_out)
        self._use_drug_guide_id = guide_id

    def show_use_drug_tip_destroy(self, *args):
        self._guide_ui.hide_temp_use_tips()

    def get_other_items(self, guide_id, item_dict_list):
        for item_dict in item_dict_list:
            init_item_dict = {'item_id': item_dict.get('item_id'),
               'entity_id': IdManager.genid(),
               'count': item_dict.get('count')
               }
            self._get_lbs()._lbs_send_event('E_PICK_UP_OTHERS', init_item_dict)

    def get_other_items_destroy(self, *args):
        pass

    def guide_signal_full_recover(self):
        self.finish_guide(self._use_drug_guide_id)

    def guide_mecha_ui_show(self, ui):
        self.unit_obj.regist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)

    def guide_mecha_ui_final(self, *_):
        self.unit_obj.unregist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)

    def mecha_progress(self, guide_id):
        self.init_mecha_progress(True)
        self._call_mecha_guide_id = guide_id

    def init_mecha_progress(self, progress):
        if progress:
            ui = global_data.ui_mgr.get_ui('MechaUI')
            if ui:
                ui.clear_mecha_cd_timer()
                ui.on_add_mecha_progress(100)
                ui.get_mecha_count_down = 0
                ui.get_mecha_count_down_progress = 0

    def guide_call_mecha_end(self, *_):
        global_data.player.logic.send_event('E_SWITCHING', 0)
        mecha = global_data.player.logic.ev_g_ctrl_mecha_obj()
        mecha.logic and mecha.logic.send_event('S_HP', 1)
        self.finish_guide(self._call_mecha_guide_id)

    def mecha_progress_destroy(self, *_):
        pass

    def enter_ace_stage(self, guide_id):
        self._get_lbs()._lbs_enter_ace_stage()
        self.finish_guide(guide_id)

    def enter_ace_stage_destroy(self, *args):
        pass

    def create_robot_mecha_by_type(self, guide_id, interval, mecha_dict):
        self._get_lbs()._lbs_create_robot_mecha_by_type(guide_id, interval, mecha_dict)

    def create_robot_mecha_by_type_destroy(self, *args):
        pass

    def guide_robot_dead(self, guide_id, interval):
        if self._robot_statistic_guide_id > 0 and self._need_robot_num > 0:
            self._need_robot_num -= 1
            global_data.emgr.update_alive_player_num_event.emit(self._need_robot_num + 1)
            if self._need_robot_num <= 0:
                self.finish_guide(self._robot_statistic_guide_id)
            return
        if interval > 0:
            self._robot_dead_delay_call = delay.call(interval, lambda g=guide_id: self._delay_robot_dead_call(g))
        else:
            self.finish_guide(guide_id)
        self.guide_shoot_show(False)

    def _delay_robot_dead_call(self, guide_id):
        self._robot_dead_delay_call = None
        self.finish_guide(guide_id)
        return

    def cancel_robot_dead_delay_call(self):
        if self._robot_dead_delay_call:
            delay.cancel(self._robot_dead_delay_call)
            self._robot_dead_delay_call = None
        return

    def destroy_mecha(self, guide_id):
        pass

    def destroy_mecha_destroy(self, *args):
        pass

    def guide_on_player_damage(self, *args):
        is_in_mecha = global_data.player.logic.ev_g_in_mecha('Mecha')
        mecha = global_data.player.logic.ev_g_ctrl_mecha_obj()
        if is_in_mecha:
            position = global_data.player.logic.ev_g_position()
            if not position and mecha and mecha.logic:
                position = mecha.logic.get_value('G_POSITION')
            off_point = (
             position.x, position.y + 50, position.z)
            global_data.player.logic.send_event('E_ON_LEAVE_MECHA_START', off_point, tutil.get_time(), True, False)
            global_data.player.logic.send_event('E_STATE_CHANGE_CD', mconst.RECOVER_CD_TYPE_DISABLE, 0, 0)
        if mecha and mecha.logic:
            mecha.logic.send_event('E_REMOVE_PASSENGER', global_data.player.id)
            mecha.logic.send_event('E_SECKILL')
            global_data.player.logic.send_event('E_SHOW_MODEL')

    def on_set_control_target(self, target, *args):
        pass

    def on_recovered_human_com(self, *args):
        last_pos = global_data.player.logic.ev_g_last_weapon_pos()
        if not last_pos:
            last_pos = PART_WEAPON_POS_MAIN1
        global_data.player.logic.send_event('E_SWITCHING', last_pos)
        global_data.player.logic.send_event('E_SHOW_MODEL')
        self.finish_guide(self._destroy_mecha_guide_id)
        global_data.player.logic.regist_event('E_GUIDE_ROBOT_DEAD', self.guide_robot_dead)
        ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if ui:
            ui.panel.setVisible(True)

    def after_mecha_die(self, guide_id):
        self._destroy_mecha_guide_id = guide_id
        self.send_event('E_STATE_CHANGE_CD', mconst.RECOVER_CD_TYPE_DISABLE, 0, 0)

    def after_mecha_die_destroy(self, guide_id):
        self._destroy_mecha_guide_id = 0

    def create_robot(self, guide_id, interval, pos, max_hp, shoot=False, role_id='11', role_random=False, eagle_flag=False):
        if role_random:
            role_config = confmgr.get('role_info', 'RoleInfo', 'Content')
            role_list = []
            for k, v in six.iteritems(role_config):
                goods_id = v.get('goods_id', None)
                if not goods_id:
                    continue
                role_list.append(k)

            role_id_list = random.sample(role_list, 1)
            role_id = role_id_list[0] if role_id_list else '11'
        self._get_lbs()._lbs_create_robot(guide_id, interval, pos, max_hp, shoot, role_id, eagle_flag)
        return

    def create_robot_destroy(self, *_):
        if self._robot_statistic_guide_id > 0:
            return
        self._get_lbs()._lbs_destroy_robot()

    def statistic_kill_robot(self, guide_id, robot_num):
        self._robot_statistic_guide_id = guide_id
        self._need_robot_num = robot_num

    def statistic_kill_robot_destroy(self, *args):
        self._robot_statistic_guide_id = -1
        self._need_robot_num = 0
        self._get_lbs()._lbs_destroy_robot()

    def update_alive_num(self, guide_id, num):
        global_data.emgr.update_alive_player_num_event.emit(num)

    def update_alive_num_destroy(self, *args):
        pass

    def _get_lbs(self):
        return global_data.player.get_local_battle_server()

    def _check_call_mecha_pos(self, guide_id, invalid_pos_tip_id, valid_tip_id):
        is_in_mecha = global_data.player.logic.ev_g_in_mecha('Mecha')
        if is_in_mecha:
            self.finish_guide(guide_id)
            return
        else:
            m_pos = global_data.player.logic.ev_g_position()
            res, pos = get_mecha_call_pos(m_pos, None, True)
            if not res:
                if self._call_mecha_pos_valid:
                    self._guide_ui.show_temp_tips(invalid_pos_tip_id, 2)
                    self._call_mecha_pos_valid = False
            else:
                self._call_mecha_pos_valid = True
                self._guide_ui.show_temp_tips(valid_tip_id, 2)
            return

    def show_side_tip_ui(self, guide_id, visible, text_id):
        self.side_tip_ui.set_tip_visible(visible)
        self.side_tip_ui.set_tip_content(text_id)

    def show_side_tip_ui_destroy(self, *args):
        self.side_tip_ui.set_tip_visible(False)

    def destroy_battle_guide(self):
        if not self._has_enter_guide:
            return
        self._has_enter_guide = False
        global_data.player._lbs_destroy_robot()
        global_data.ui_mgr.close_ui('GuideUI')
        global_data.ui_mgr.close_ui('LeaveGuideUI')
        global_data.ui_mgr.close_ui('MechaControlMain')
        self.unit_obj.unregist_event('E_GUIDE_OPEN_MAIN_SETTING', self.on_open_main_setting)
        self.unit_obj.unregist_event('E_GUIDE_CLOSE_MAIN_SETTING', self.on_close_main_setting)
        self.unit_obj.unregist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)
        self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.on_pick_up_others)
        self.unit_obj.unregist_event('E_GUIDE_PICK_UNROLL_PACKAGE', self.on_pick_unroll_package)
        self.unit_obj.unregist_event('E_GUIDE_ROBOT_DEAD', self.guide_robot_dead)
        self.unit_obj.unregist_event('E_GUIDE_PICKED_SPECIFIC_ITEMS', self.guide_pick_specific_items)
        global_data.emgr.scene_pick_show_item_list -= self.on_show_pick_ui_items
        global_data.emgr.scene_update_pick_info_event -= self.scene_update_pick_info
        global_data.emgr.show_big_map_ui_event -= self.on_big_map_show
        self.destroy_signal()
        self.check_move_pos_destroy()
        self.show_riko_tips_destroy()
        self.lock_move_destroy()
        self.cancel_robot_dead_delay_call()
        self.refresh_poison_circle_destroy()
        self.reduce_poison_circle_destroy()
        self.process_barrier_boundary_check(self.unit_obj, check=False)
        if global_data.is_pc_mode:
            from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
            from data import hot_key_def
            PCCtrlManager().unblock_hotkey(hot_key_def.SUMMON_CALL_MECHA, 'local_battle_guide')
        self.unregist_throw_item_explosion_event()

    def destroy(self):
        self.destroy_battle_guide()
        super(ComNewbieFourGuide, self).destroy()

    def on_pick_up_others(self, item_data):
        if not item_data:
            return
        item_id = item_data.get('item_id', 0)
        item_count = item_data.get('count', 0)
        if item_id <= 0 or item_count <= 0:
            return
        if item_id == item_const.ITEM_NO_ACE_STAR:
            self._ace_start_point += item_count
            if self._ace_start_point >= 2:
                self._driver_level = 1
                cur_max_hp = global_data.player.logic.ev_g_max_hp()
                self.send_event('E_SET_MAX_HP', cur_max_hp + 5)
            self.send_event('E_PLAYER_LEVEL_UP', self._driver_level, self._ace_start_point)
            self.send_event('S_ATTR_SET', 'driver_level', self._driver_level)
            self.send_event('S_ATTR_SET', 'star_point', self._ace_start_point)

    def show_pick_animation(self, guide_id, layer, animation):
        self._pick_animation_guide_id = guide_id

    def show_pick_animation_destroy(self, guide_id, layer, animation):
        self._stop_all_pick_animation()
        self._pick_animation_guide_id = None
        self._pick_items_has_show = False
        return

    def on_show_pick_ui_items(self, showing):
        if self._pick_animation_guide_id is None or self._pick_animation_guide_id <= 0:
            return
        else:
            if not showing:
                self._stop_all_pick_animation()
            return

    def _stop_all_pick_animation(self):
        self._guide_ui.play_nd_animation_destroy('nd_step_5', 'show_5')
        if global_data.is_pc_mode:
            self._guide_ui.play_nd_animation_destroy('nd_step_5_2', 'show_5_2')
        else:
            self._guide_ui.play_nd_animation_destroy('nd_step_5_1', 'show_5_1')

    def on_pick_unroll_package(self):
        if self._scene_box_pick_guide_id > 0:
            self.finish_guide(self._scene_box_pick_guide_id)
            return
        else:
            if self._pick_animation_guide_id is None or self._pick_animation_guide_id <= 0:
                return
            self._guide_ui.play_nd_animation_destroy('nd_step_5', 'show_5')
            if global_data.is_pc_mode:
                self._guide_ui.play_nd_animation('nd_step_5_2', 'show_5_2')
            else:
                self._guide_ui.play_nd_animation('nd_step_5_1', 'show_5_1')
            return

    def scene_update_pick_info(self, pickable_info_list):
        if self._pick_animation_guide_id is None or self._pick_animation_guide_id <= 0:
            return
        else:
            guide_data = self.get_guide_data(self._pick_animation_guide_id)
            func_args = guide_data.get('Args', [])
            if not func_args:
                return
            layer, animation = func_args
            if pickable_info_list:
                self._guide_ui.play_nd_animation(layer, animation)
            return

    def delay_show_tip_ui(self, guide_id, *args):
        self._delay_show_side_ui_guide_id = guide_id

    def delay_show_tip_ui_destroy(self, *args):
        self._delay_show_side_ui_guide_id = 0

    def on_top_five_widget_destroy(self):
        if self._delay_show_side_ui_guide_id > 0:
            self.finish_guide(self._delay_show_side_ui_guide_id)

    def pick_up_weapon(self, guide_id, weapon_id):
        self._add_weapon(weapon_id)

    def pick_up_weapon_destroy(self, *_):
        pass

    def process_throw_item_explosion_event(self):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        part_throwable_mgr = scene.get_com('PartThrowableManager')
        if not part_throwable_mgr:
            return
        self._locale_battle_server = global_data.player.get_local_battle_server()
        global_data.emgr.scene_throw_item_explosion_event -= part_throwable_mgr.throw_item_explosion
        global_data.emgr.scene_throw_item_explosion_event += self._locale_battle_server.lbs_update_explosive_item_info
        global_data.emgr.scene_throw_item_explosion_event += part_throwable_mgr.throw_item_explosion
        self._regist_throw_explosion_event_flag = True

    def unregist_throw_item_explosion_event(self):
        if self._regist_throw_explosion_event_flag:
            global_data.emgr.scene_throw_item_explosion_event -= self._locale_battle_server.lbs_update_explosive_item_info
            self._regist_throw_explosion_event_flag = False
            self._locale_battle_server = None
        return

    def show_mecha_call_disable_tips(self, guide_id, text_id, duration):
        ui = global_data.ui_mgr.get_ui('StateChangeUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('StateChangeUI', 'logic.comsys.battle')
        if ui:
            ui.show_guide_mecha_call_disable_tip()

    def show_mecha_call_disable_tips_destroy(self, *args):
        ui = global_data.ui_mgr.get_ui('StateChangeUI')
        if ui:
            ui.hide_guide_mecha_call_disable_tip()

    def set_robot_mecha_hp_lock(self, guide_id, flag):
        self._locale_battle_server = global_data.player.get_local_battle_server()
        if self._locale_battle_server:
            self._locale_battle_server.set_robot_mecha_hp_lock(flag)

    def set_robot_mecha_hp_lock_destroy(self, guide_id, flag):
        self.set_robot_mecha_hp_lock(guide_id, not flag)