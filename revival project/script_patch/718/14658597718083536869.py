# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNewbieThirdGuide.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.comsys.guide_ui.GuideUI import GuideUI, LeaveGuideUI, PCGuideUI
from logic.comsys.guide_ui.NewbieStageSideTipUI import NewbieStageSideTipUI
from logic.client.const import game_mode_const
from logic.gutils import newbie_stage_utils, task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gutils.delay as delay
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from data.newbie_stage_config import GetStageThird, GetStageThirdEndHandler
from mobile.common.IdManager import IdManager
import logic.gcommon.const as const
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gcommon.common_const.water_const import WATER_NONE
from logic.gcommon.common_const import mecha_const
import logic.gcommon.time_utility as tutil

class ComNewbieThirdGuide(UnitCom):
    BIND_EVENT = {'E_GUIDE_REGIST_MECHA_DIVING_EVENT': 'regist_mecha_diving_event',
       'E_GUIDE_REGIST_MECHA_DIVING_SHOW_TIP_EVENT': 'regist_mecha_diving_delay_tip_event',
       'E_LOCAL_BATTLE_ESC_3': 'on_click_quit_btn'
       }

    def __init__(self):
        super(ComNewbieThirdGuide, self).__init__()
        self.barrier_center = None
        self.barrier_radius = None
        self.battle_ctrl_ui_btn_visiblity = {}
        self.is_battle_control_ui_event_binded = False
        self.riko_tip_timer = None
        self.check_pos_timer = None
        self.check_human_in_water_timer = None
        self.show_eagle_flag_timer = None
        self.remind_attack_timer = None
        self.remind_transform_timer = None
        self.common_check_pos_timer = None
        self.check_block_timer = None
        self.sfx_map = {}
        self.finished_guides = set()
        self.last_move_timestamp = None
        self.check_block_flag = False
        self.showing_riko_tip_in_water = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComNewbieThirdGuide, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        if not self.battle:
            return
        battle_tid = self.battle.get_battle_tid()
        if battle_tid != game_mode_const.NEWBIE_STAGE_THIRD_BATTLE_TYPE:
            return
        if global_data.ui_mgr.get_ui('BattleLoadingWidget'):
            global_data.emgr.battle_loading_finished_event += self.start_guide_logic
        else:
            self.start_guide_logic(False)

    def destroy(self):
        self.stop_show_eagle_flag()
        self.show_human_tips_destroy()
        self.check_human_in_water_destroy()
        self.check_reach_target_destroy()
        self.delay_remind_attack_destroy()
        self.delay_remind_transform_destroy()
        self.check_reach_target_common_destroy()
        self.check_block_destroy()
        self.process_barrier_boundary_check(self.unit_obj, check=False)
        self.unblock_pc_hot_keys()
        if self.is_battle_control_ui_event_binded:
            self.process_battle_control_ui(False)
        super(ComNewbieThirdGuide, self).destroy()

    @property
    def guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()

    @property
    def side_tip_ui(self):
        return NewbieStageSideTipUI()

    def start_guide_logic(self, event_flag=True):
        if event_flag:
            global_data.emgr.battle_loading_finished_event -= self.start_guide_logic
        self.guide_ui.hide_main_ui()
        self.update_setting_quit_button()
        self.process_barrier_boundary_check(self.unit_obj, check=True)
        newbie_stage_utils.propel_guide(100, self)
        self.init_quit_ui()
        self.process_battle_control_ui(True)
        self.is_battle_control_ui_event_binded = True

    def unblock_pc_hot_keys(self):
        if not global_data.is_pc_mode:
            return
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        from data import hot_key_def
        PCCtrlManager().unblock_hotkey(hot_key_def.SUMMON_CALL_MECHA, 'local_battle_guide')
        PCCtrlManager().unblock_hotkey(hot_key_def.GET_OFF_SKATEBOARD_OR_VEHICLE, 'local_battle_guide')
        PCCtrlManager().unblock_hotkey(hot_key_def.CAR_TRANSFORM, 'local_battle_guide')
        PCCtrlManager().unblock_hotkey(hot_key_def.CAR_RUSH, 'local_battle_guide')
        PCCtrlManager().unblock_hotkey(hot_key_def.SWITCH_BATTLE_BAG, 'local_battle_guide')

    def process_battle_control_ui(self, bind):
        if bind:
            global_data.emgr.battle_control_ui_pc_refresh_event += self.on_battle_control_ui_refresh
        else:
            global_data.emgr.battle_control_ui_pc_refresh_event -= self.on_battle_control_ui_refresh

    def on_battle_control_ui_refresh(self, *args):
        ui = global_data.ui_mgr.get_ui('BattleControlUIPC')
        if not ui:
            return
        for btn_name, visible in six.iteritems(self.battle_ctrl_ui_btn_visiblity):
            ui.set_action_btn_visible_by_name(btn_name, visible)

    def update_setting_quit_button(self):
        self.unit_obj.regist_event('E_GUIDE_OPEN_MAIN_SETTING', self.on_open_main_setting)
        self.unit_obj.regist_event('E_GUIDE_CLOSE_MAIN_SETTING', self.on_close_main_setting)

    def on_open_main_setting(self, setting_ui):
        self.guide_ui.panel.setVisible(False)
        if setting_ui and setting_ui.ref_btn_exit:
            setting_ui.ref_btn_exit.btn.SetText(5030)

    def on_close_main_setting(self, *args):
        self.guide_ui.panel.setVisible(True)

    def init_quit_ui(self):
        if global_data.is_pc_mode:
            return
        self.guide_ui.show_main_ui_by_type('BattleRightTopUI')
        battle_right_top_ui = global_data.ui_mgr.get_ui('BattleRightTopUI')
        if not battle_right_top_ui:
            return
        battle_right_top_ui.show_only_exit_btn()
        battle_right_top_ui.btn_exit.BindMethod('OnClick', self.on_click_quit_btn)

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

    def process_barrier_boundary_check(self, unit_obj, check=False):
        if not unit_obj:
            return
        if not self.battle:
            return
        battle_tid = self.battle.get_battle_tid()
        if battle_tid != game_mode_const.NEWBIE_STAGE_THIRD_BATTLE_TYPE:
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
            if delta_vec.length >= self.barrier_radius - 50:
                self.send_event('E_SHOW_MESSAGE', get_text_by_id(5050))
            return

    def extra_finish_process(self, guide_id):
        if guide_id == 2501:
            battle_type = self.battle.get_battle_tid()
            newbie_stage_utils.finish_local_battle_guide(battle_type)

    def get_guide_data(self, guide_id):
        return GetStageThird().get(guide_id)

    def show_main_ui(self, ui_list):
        if ui_list:
            if isinstance(ui_list, (list, tuple)):
                for key in ui_list:
                    self.guide_ui.show_main_ui_by_type(key)

            else:
                self.guide_ui.show_main_ui_by_type(ui_list)

    def is_finished_guide(self, guide_id):
        return guide_id in self.finished_guides

    def add_finished_guide(self, guide_id):
        self.finished_guides.add(guide_id)

    def empty_guide_holder(self, guide_id, *args):
        newbie_stage_utils.finish_guide(guide_id, self)

    def empty_guide_holder_destroy(self, *args):
        pass

    def equip_weapons(self, guide_id, weapon_dict):
        for weapon_pos, weapon_id in six.iteritems(weapon_dict):
            iMagSize = confmgr.get('firearm_config', str(weapon_id))['iMagSize']
            item_data = {'item_id': weapon_id,'entity_id': IdManager.genid(),'count': 1,'iBulletNum': iMagSize}
            self.send_event('E_PICK_UP_WEAPON', item_data, weapon_pos, False)

        self.send_event('E_SWITCHING', const.PART_WEAPON_POS_MAIN_DF)

    def equip_weapons_destroy(self, *args):
        pass

    def create_items(self, guide_id, item_list):
        global_data.player.local_battle_server.create_items(guide_id, item_list)

    def create_items_destroy(self, *args):
        pass

    def create_building(self, guide_id, building_type, extra_dict):
        global_data.player.local_battle_server.create_building(building_type, extra_dict)

    def create_building_destroy(self, *args):
        pass

    def create_robot(self, guide_id, robot_dict):
        global_data.player.local_battle_server.create_robot(guide_id, robot_dict)
        need_eagle = robot_dict.get('need_eagle', True)
        if not need_eagle:
            return
        self.show_eagle_flag_timer = delay.call(0.5, self.show_eagle_flag)

    def show_eagle_flag(self, *args):
        self.show_eagle_flag_timer = None
        if not global_data.player:
            return
        else:
            if not global_data.player.local_battle_server:
                return
            robot = global_data.player.local_battle_server.get_one_robot()
            if not robot or not robot.logic:
                return
            robot.logic.send_event('E_ADD_EAGLE_FLAG', robot.id, 'gift', False)
            return

    def stop_show_eagle_flag(self, *args):
        if self.show_eagle_flag_timer:
            delay.cancel(self.show_eagle_flag_timer)
            self.show_eagle_flag_timer = None
        return

    def create_robot_destroy(self, *args):
        pass

    def show_little_tips(self, guide_id, text_id, time_out):
        self.guide_ui.show_temp_tips(get_text_by_id(text_id), time_out)

    def show_little_tips_destroy(self, *args):
        self.guide_ui.show_temp_tips_destroy()

    def show_little_tips_pc(self, guide_id, text_id, time_out, hot_key_func_code=None):
        self.guide_ui.show_temp_tips_pc(text_id, time_out, hot_key_func_code)

    def show_little_tips_pc_destroy(self, *args):
        self.guide_ui.show_temp_tips_destroy()

    def show_human_tips(self, guide_id, text_id, time_out, time_before=0, propel_ids=None):
        if time_before == 0:
            self.show_human_tips_imp(guide_id, text_id, time_out, propel_ids)
        else:
            self.riko_tip_timer = delay.call(time_before, lambda gid=guide_id, t_id=text_id, t_out=time_out, p_ids=propel_ids: self.show_human_tips_imp(gid, t_id, t_out, p_ids))

    def show_human_tips_imp(self, guide_id, text_id, time_out, propel_ids):
        self.riko_tip_timer = None
        guide_data = self.get_guide_data(guide_id)
        if guide_data.get('Next', None):
            self.guide_ui.show_human_tips(get_text_by_id(text_id), time_out, lambda g_id=guide_id: newbie_stage_utils.finish_guide(g_id, self))
        elif propel_ids:
            self.guide_ui.show_human_tips(get_text_by_id(text_id), time_out, lambda g_ids=propel_ids: newbie_stage_utils.propel_guide_multiple(g_ids, self))
        else:
            self.guide_ui.show_human_tips(get_text_by_id(text_id), time_out)
        return

    def show_human_tips_destroy(self, *args):
        if self.riko_tip_timer:
            delay.cancel(self.riko_tip_timer)
            self.riko_tip_timer = None
        return

    def show_multi_human_tips(self, guide_id, text_id_list, time_out, propel_ids=None):
        text_list = [ get_text_by_id(text_id) for text_id in text_id_list ]
        self.guide_ui.show_multi_human_tips(text_list, time_out)

    def show_multi_human_tips_destroy(self, *args):
        self.guide_ui.show_multi_human_tips_destroy()

    def show_human_tips_pc(self, guide_id, text_id, time_out, hot_key_func_code=None, propel_ids=None):
        guide_data = self.get_guide_data(guide_id)
        if guide_data.get('Next', None):
            self.guide_ui.show_human_tips_pc(text_id, time_out, hot_key_func_code, lambda g_id=guide_id: newbie_stage_utils.finish_guide(g_id, self))
        elif propel_ids:
            self.guide_ui.show_human_tips_pc(text_id, time_out, hot_key_func_code, lambda g_ids=propel_ids: newbie_stage_utils.propel_guide_multiple(g_ids, self))
        else:
            self.guide_ui.show_human_tips_pc(text_id, time_out, hot_key_func_code)
        return

    def show_human_tips_pc_destroy(self, *args):
        pass

    def show_nd_animation(self, guide_id, layer, animation):
        self.guide_ui.play_nd_animation(layer, animation)

    def show_nd_animation_destroy(self, guide_id, layer, animation):
        self.guide_ui.play_nd_animation_destroy(layer, animation)

    def show_use_drug_tip(self, guide_id, text_id, time_out, hot_key_func_code=None):
        self.guide_ui.show_temp_use_tips(text_id, time_out, hot_key_func_code)

    def show_use_drug_tip_destroy(self, *args):
        self.guide_ui.hide_temp_use_tips()

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
        self.guide_ui.show_locate(target_pos, offset, layer, animation_name)

    def show_locate_ui_destroy(self, guide_id, target_pos, offset, layer, animation_name=None):
        self.guide_ui.show_locate_destroy(layer, animation_name)

    def show_skateboard_sfx(self, guide_id, path):
        if not global_data.player or not global_data.player.local_battle_server:
            return
        target_pos = global_data.player.local_battle_server.get_skateboard_pos_on_ground()
        if not target_pos:
            return
        self.show_target_sfx(guide_id, target_pos, path)

    def show_skateboard_sfx_destroy(self, guide_id, *args):
        self.show_target_sfx_destroy(guide_id)

    def show_chicken_sfx(self, guide_id, path):
        if not global_data.player or not global_data.player.local_battle_server:
            return
        target_pos = global_data.player.local_battle_server.get_chicken_pos_on_ground()
        if not target_pos:
            return
        self.show_target_sfx(guide_id, target_pos, path)

    def show_chicken_sfx_destroy(self, guide_id, *args):
        self.show_target_sfx_destroy(guide_id)

    def show_attachable_ui(self, guide_id, show):
        ui = global_data.ui_mgr.get_ui('AttachableDriveUI')
        ui and ui.set_btn_getoff_skateboard_visible(show)

    def show_attachable_ui_destroy(self, *args):
        pass

    def show_get_off_chicken_btn(self, guide_id, show):
        if global_data.is_pc_mode:
            return
        ui = global_data.ui_mgr.get_ui('MechaTransUI')
        ui and ui.set_btn_get_off_visible(show)
        is_in_water = global_data.player.logic.ev_g_is_in_water_area()
        ui and ui.set_btn_get_off_enable(not is_in_water)

    def show_get_off_chicken_btn_destroy(self, *args):
        pass

    def show_chicken_transform_btn(self, guide_id, show):
        ui = global_data.ui_mgr.get_ui('MechaTransUI')
        ui and ui.set_btn_transform_visible(show)

    def show_chicken_transform_btn_destroy(self, guide_id, show):
        pass

    def show_chicken_speed_btn(self, guide_id, show):
        ui = global_data.ui_mgr.get_ui('MechaTransUI')
        ui and ui.set_btn_speed_visible(show)

    def show_chicken_speed_btn_destroy(self, *args):
        pass

    def wait_guide_handler(self, guide_id, wait_time):
        self.guide_ui.show_empty_tips(wait_time, lambda : newbie_stage_utils.finish_guide(guide_id, self))

    def wait_guide_handler_destroy(self, *args):
        pass

    def check_reach_target(self, guide_id, pos, offset):
        self.check_pos_timer = global_data.game_mgr.register_logic_timer(lambda : self.check_reach_target_imp(guide_id, pos, offset), interval=0.1, mode=CLOCK)

    def check_reach_target_imp(self, guide_id, target_pos, offset):
        if not global_data.player or not global_data.player.logic:
            return
        cur_pos_vec = global_data.player.logic.ev_g_position()
        dist = math3d.vector(*target_pos) - cur_pos_vec
        if dist.length < offset * NEOX_UNIT_SCALE:
            newbie_stage_utils.finish_guide(guide_id, self)

    def check_reach_target_destroy(self, *args):
        if self.check_pos_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_pos_timer)
            self.check_pos_timer = None
        return

    def check_reach_target_common(self, guide_id, pos, offset, callback_name, arg_dict):
        callback = getattr(self, callback_name)
        if not callback or not callable(callback):
            return
        self.common_check_pos_timer = global_data.game_mgr.register_logic_timer(lambda : self.check_reach_target_common_imp(guide_id, pos, offset, callback, arg_dict), interval=0.1, mode=CLOCK)

    def check_reach_target_common_imp(self, guide_id, target_pos, offset, callback, arg_dict):
        if not global_data.player or not global_data.player.logic:
            return
        cur_pos_vec = global_data.player.logic.ev_g_position()
        dist = math3d.vector(*target_pos) - cur_pos_vec
        if dist.length < offset * NEOX_UNIT_SCALE:
            callback(guide_id, arg_dict)

    def check_reach_target_common_destroy(self, *args):
        if self.common_check_pos_timer:
            global_data.game_mgr.unregister_logic_timer(self.common_check_pos_timer)

    def check_human_in_water(self, *args):
        self.check_human_in_water_timer = global_data.game_mgr.register_logic_timer(self.check_human_in_water_imp, interval=0.5, mode=CLOCK)

    def check_human_in_water_imp(self):
        is_in_water = global_data.player.logic.ev_g_is_in_water_area()
        ui = global_data.ui_mgr.get_ui('MechaTransUI')
        ui and ui.set_btn_get_off_visible(not is_in_water)

    def check_human_in_water_destroy(self, *args):
        if self.check_human_in_water_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_human_in_water_timer)
            self.check_human_in_water_timer = None
        return

    def check_block(self, *args):
        self.check_block_timer = global_data.game_mgr.register_logic_timer(self.check_block_imp, interval=2, mode=CLOCK)

    def check_block_imp(self):
        now = tutil.get_time()
        control_target = self.unit_obj.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        if not control_target.logic.ev_g_is_mechatran():
            return
        if control_target.logic.ev_g_pattern() != mecha_const.MECHA_PATTERN_VEHICLE:
            return
        if self.last_move_timestamp and now - self.last_move_timestamp > 10:
            self.guide_ui.show_chicken_deformation_tips(True, 5624)

    def check_block_destroy(self, *args):
        if self.check_block_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_block_timer)
            self.check_block_timer = None
        return

    def clear_call_mecha_cd(self, guide_id, *args):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            ui.clear_mecha_cd_timer()
            ui.on_add_mecha_progress(100)
            ui.get_mecha_count_down = 0
            ui.get_mecha_count_down_progress = 0

    def clear_call_mecha_cd_destroy(self, *args):
        pass

    def delay_remind_attack(self, guide_id, delay_time):
        self.remind_attack_timer = delay.call(delay_time, self.remind_attack)

    def remind_attack(self):
        if not self or not self.is_valid():
            return
        else:
            self.remind_attack_timer = None
            self.guide_ui.play_nd_animation('nd_step_7', 'show_7')
            return

    def delay_remind_attack_destroy(self, *args):
        if self.remind_attack_timer:
            delay.cancel(self.remind_attack_timer)
            self.remind_attack_timer = None
        self.guide_ui.play_nd_animation_destroy('nd_step_8', 'show_8')
        self.guide_ui.show_drag_layer_destroy('temp_move_tips')
        return

    def delay_remind_transform(self, guide_id, delay_time):
        self.remind_transform_timer = delay.call(delay_time, self.remind_transform)

    def remind_transform(self):
        if not self or not self.is_valid():
            return
        else:
            self.remind_transform_timer = None
            self.guide_ui.play_nd_animation('nd_deformation_tips', 'show_deformation')
            self.guide_ui.show_chicken_deformation_tips(True, 5624)
            return

    def delay_remind_transform_destroy(self, *args):
        if self.remind_transform_timer:
            delay.cancel(self.remind_transform_timer)
            self.remind_transform_timer = None
        self.guide_ui.play_nd_animation_destroy('nd_deformation_tips', 'show_deformation')
        return

    def turn_dir_by_target_pos(self, guide_id, pos):
        if not global_data.player or not global_data.player.logic:
            return
        lent = global_data.player.logic
        my_pos = lent.ev_g_position()
        target_pos = math3d.vector(*pos)
        if my_pos and target_pos:
            diff_vec = target_pos - my_pos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                target_pitch = diff_vec.pitch
                cur_yaw = lent.ev_g_yaw() or 0
                cur_pitch = lent.ev_g_pitch() or 0
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(target_yaw, target_pitch, True, 0.5)
                lent.send_event('E_DELTA_YAW', target_yaw - cur_yaw)
                lent.send_event('E_DELTA_PITCH', target_pitch - cur_pitch)

    def turn_dir_by_target_pos_destroy(self, *args):
        pass

    def enable_screen_touch(self, guide_id, enable):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        scene.on_camera_move_enable(enable)

    def enable_screen_touch_destroy(self, *args):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        scene.on_camera_move_enable(True)

    def enable_rocker_move(self, guide_id, enable):
        ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        ui and ui.on_disable_rocker_move(not enable)

    def enable_rocker_move_destroy(self, *args):
        ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        ui and ui.on_disable_rocker_move(False)

    def show_chicken_firerocker_tips(self, guide_id, text_id):
        self.guide_ui.show_chicken_firerocker_tips(True, text_id)

    def show_chicken_firerocker_tips_destroy(self, *args):
        self.guide_ui.show_chicken_firerocker_tips(False)

    def show_chicken_transform_tips(self, guide_id, text_id):
        self.guide_ui.show_chicken_deformation_tips(True, text_id)

    def show_chicken_transform_tips_destroy(self, *args):
        self.guide_ui.show_chicken_deformation_tips(False)

    def init_mecha_call_btn_ban_status(self, guide_id, *args):
        if not global_data.player or not global_data.player.logic:
            return
        control_target = global_data.player.logic.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        if control_target.logic.ev_g_is_mechatran():
            is_in_water = control_target.logic.ev_g_is_diving()
        else:
            is_in_water = global_data.player.logic.ev_g_is_in_water_area()
        if is_in_water:
            self.show_mecha_btn_ban()

    def init_mecha_call_btn_ban_status_destroy(self, *args):
        pass

    def show_side_tip_ui(self, guide_id, visible, text_id):
        self.side_tip_ui.set_tip_visible(visible)
        self.side_tip_ui.set_tip_content(text_id)

    def show_side_tip_ui_destroy(self, *args):
        self.side_tip_ui.set_tip_visible(False)

    def create_end_ui(self, guide_id, *args):
        from logic.comsys.guide_ui.NewbieStageEndUI import NewbieStageEndUI

        def end_ui_cb():
            newbie_stage_utils.finish_guide(guide_id, self)

        NewbieStageEndUI(None, end_ui_cb)
        return

    def create_end_ui_destroy(self, *args):
        pass

    def do_nothing_guide(self, *args):
        pass

    def do_nothing_guide_destroy(self, *args):
        pass

    def block_pc_hot_key(self, guide_id, hot_key_list, is_block):
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        for hot_key in hot_key_list:
            if is_block:
                PCCtrlManager().block_hotkey(hot_key, 'local_battle_guide')
            else:
                PCCtrlManager().unblock_hotkey(hot_key, 'local_battle_guide')

    def block_pc_hot_key_destroy(self, *args):
        pass

    def set_control_btn_visible(self, guide_id, btn_name, visible):
        self.battle_ctrl_ui_btn_visiblity.update({btn_name: visible})
        ui = global_data.ui_mgr.get_ui('BattleControlUIPC')
        if not ui:
            return
        ui.set_action_btn_visible_by_name(btn_name, visible)

    def set_control_btn_visible_destroy(self, *args):
        pass

    def show_summon_mecha_tip(self, guide_id, text_id, hot_key_func_code=None):
        self.guide_ui.show_summon_mecha_tip(text_id, hot_key_func_code)

    def show_summon_mecha_tip_destroy(self, *args):
        self.guide_ui.hide_summon_mecha_tip()

    def register_chicken_block_check(self, *args):
        control_target = self.unit_obj.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        if not control_target.logic.ev_g_is_mechatran():
            return
        self.regist_mecha_check_block_event(control_target.logic, True)

    def register_chicken_block_check_destroy(self, *args):
        control_target = self.unit_obj.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        if not control_target.logic.ev_g_is_mechatran():
            return
        self.regist_mecha_check_block_event(control_target.logic, False)

    def regist_mecha_diving_delay_riko_tip(self, *args):
        pass

    def regist_mecha_diving_delay_riko_tip_destroy(self, *args):
        control_target = self.unit_obj.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        ct_logic_name = control_target.logic.__class__.__name__
        if ct_logic_name != 'LMecha':
            return
        self.regist_mecha_diving_delay_tip_event(control_target.logic, False)

    def remove_sfx_and_locate_ui_by_guide_id(self, guide_id, arg_dict):
        self.check_reach_target_common_destroy()
        sfx_relate_guide_id = arg_dict.get('delete_guide_id', 802)
        if sfx_relate_guide_id in self.sfx_map:
            global_data.sfx_mgr.remove_sfx(self.sfx_map[sfx_relate_guide_id])
            del self.sfx_map[sfx_relate_guide_id]
        layer = arg_dict.get('layer', 'temp_locate')
        animation_name = arg_dict.get('animation_name', 'keep')
        self.guide_ui.show_locate_destroy(layer, animation_name)

    def show_mecha_btn_ban(self):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if not ui or not ui.isPanelVisible():
            return
        ui.set_mecha_btn_ban_img_visible(True)
        self.guide_ui.set_call_mecha_tips_text(5625)

    def hide_mecha_btn_ban(self):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if not ui or not ui.isPanelVisible():
            return
        ui.set_mecha_btn_ban_img_visible(False)
        self.guide_ui.set_call_mecha_tips_text(80116)

    def on_pos_changed(self, pos, *args):
        if self.last_move_timestamp is None:
            self.last_move_timestamp = tutil.get_time()
            return
        else:
            self.guide_ui.show_chicken_deformation_tips(False)
            self.last_move_timestamp = tutil.get_time()
            return

    def process_mecha_tip_in_water(self):
        self.show_mecha_skill_btn_ban_tips(True)
        if self.showing_riko_tip_in_water:
            return
        self.showing_riko_tip_in_water = True
        self.show_human_tips_destroy()
        self.guide_ui.show_human_tips(5230, 7)

    def process_mecha_tip_out_water(self):
        self.show_mecha_skill_btn_ban_tips(False)

    def show_mecha_skill_btn_ban_tips(self, visible):
        self.guide_ui.show_mecha_skill_btn_ban_tips(visible)

    def regist_mecha_diving_event(self, unit_obj, is_regist):
        if is_regist:
            unit_obj.regist_event('E_MECHA_ENTER_DIVING', self.show_mecha_btn_ban)
            unit_obj.regist_event('E_MECHA_LEAVE_DIVING', self.hide_mecha_btn_ban)
        else:
            unit_obj.unregist_event('E_MECHA_ENTER_DIVING', self.show_mecha_btn_ban)
            unit_obj.unregist_event('E_MECHA_LEAVE_DIVING', self.hide_mecha_btn_ban)

    def regist_mecha_check_block_event(self, unit_obj, is_regist):
        if G_POS_CHANGE_MGR:
            if is_regist:
                unit_obj.regist_pos_change(self.on_pos_changed, 1.0)
            else:
                unit_obj.unregist_pos_change(self.on_pos_changed)
        elif is_regist:
            unit_obj.regist_event('E_POSITION', self.on_pos_changed)
        else:
            unit_obj.unregist_event('E_POSITION', self.on_pos_changed)

    def regist_mecha_diving_delay_tip_event(self, unit_obj, is_regist):
        if is_regist:
            unit_obj.regist_event('E_MECHA_ENTER_DIVING', self.process_mecha_tip_in_water)
            unit_obj.regist_event('E_MECHA_LEAVE_DIVING', self.process_mecha_tip_out_water)
        else:
            unit_obj.unregist_event('E_MECHA_ENTER_DIVING', self.process_mecha_tip_in_water)
            unit_obj.unregist_event('E_MECHA_LEAVE_DIVING', self.process_mecha_tip_out_water)

    def on_guide_mecha_change_state(self, *args):
        ui = global_data.ui_mgr.get_ui('StateChangeUI')
        if not ui:
            return
        ui.panel.btn_change_to_human.setVisible(False)
        ui.panel.btn_change_to_mech.setVisible(False)

    def on_guide_mecha_change_show_tips(self, *args):
        self.show_little_tips(None, 5252, 5)
        return

    def on_guide_hide_delay_trans_tip(self, *args):
        self.guide_ui.show_chicken_deformation_tips(False)

    def on_guide_hide_delay_attack_tip(self, *args):
        self.guide_ui.play_nd_animation_destroy('nd_step_7', 'show_7')

    def on_guide_water_status_change(self, water_status, *args):
        if water_status == WATER_NONE:
            self.hide_mecha_btn_ban()
        else:
            self.show_mecha_btn_ban()

    def on_guide_pick_item_event(self, guide_id, item_id):
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_item_use_end(self, item_id):
        item_id_2_guide_id = GetStageThirdEndHandler().get('on_guide_item_use_end', {}).get('handler_params')
        if not item_id_2_guide_id:
            return
        newbie_stage_utils.finish_guide(item_id_2_guide_id.get(item_id), self)

    def on_guide_robot_die(self, guide_id):
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_leave_skateboard(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_leave_skateboard', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_enter_skate_zone(self, *args):
        text_id = 5609 if global_data.is_pc_mode else 5283
        if global_data.is_pc_mode:
            return
        self.guide_ui.show_get_on_skateboard_tips(True, text_id)

    def on_guide_leave_skate_zone(self, *args):
        text_id = 5609 if global_data.is_pc_mode else 5283
        if global_data.is_pc_mode:
            return
        self.guide_ui.show_get_on_skateboard_tips(False, text_id)

    def on_guide_success_board(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_success_board', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_leave_chicken(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_leave_chicken', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_transform_2_vehicle(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_transform_2_vehicle', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_chicken_dash(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_chicken_dash', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_join_mecha_end(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_join_mecha_end', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_join_mecha_end_no_card(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_join_mecha_end_no_card', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)
        if global_data.is_pc_mode:
            return
        self.guide_ui.show_get_on_chicken_tips(False)

    def on_guide_join_mecha_start(self, mecha_eid, mecha_type, *args):
        if mecha_type == mecha_const.MECHA_TYPE_VEHICLE:
            return
        guide_id = GetStageThirdEndHandler().get('on_guide_join_mecha_start', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)

    def on_guide_enter_mecha_zone(self, *args):
        if global_data.is_pc_mode:
            return
        self.guide_ui.show_get_on_chicken_tips(True)

    def on_guide_leave_mecha_zone(self, *args):
        if global_data.is_pc_mode:
            return
        self.guide_ui.show_get_on_chicken_tips(False)

    def on_guide_super_jump_end(self, *args):
        guide_id = GetStageThirdEndHandler().get('on_guide_super_jump_end', {}).get('handler_params')
        newbie_stage_utils.finish_guide(guide_id, self)