# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComQTELocalBattleGuide.py
from __future__ import absolute_import
import math3d
import math
from ..UnitCom import UnitCom
from logic.gutils import qte_guide_utils
from logic.client.const import game_mode_const
from logic.comsys.guide_ui.GuideUI import GuideUI, LeaveGuideUI, PCGuideUI
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.IdManager import IdManager
import logic.gcommon.const as const
from data.c_guide_data import GetQTEGuide
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils.newbie_stage_utils import GUIDE_PROCESS_MODE_ONLY_INIT, GUIDE_PROCESS_MODE_ONLY_DESTROY
from logic.gcommon.cdata import status_config as st_const
from common.cinematic.VideoPlayer import VideoPlayer
from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
from data import hot_key_def
import wwise
import game3d
import logic.gutils.delay as delay

class ComQTELocalBattleGuide(UnitCom):
    BIND_EVENT = {'E_LOCAL_BATTLE_ESC': 'quit_qte_local_battle'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComQTELocalBattleGuide, self).init_from_dict(unit_obj, bdict)
        self._cur_sub_guide_steps = []
        self._key_step_map = {}
        self._sfx_map = {}
        self._all_block_hotkeys = set()
        self.qte_guide_ui = None
        self.summon_timer = None
        return

    def on_init_complete(self):
        battle = self.battle
        battle_tid = battle.get_battle_tid()
        if battle_tid != game_mode_const.QTE_LOCAL_BATTLE_TYPE:
            return
        if global_data.ui_mgr.get_ui('BattleLoadingWidget'):
            global_data.emgr.battle_loading_finished_event += self.battle_loading_finish
        else:
            self.start_qte_guide_logic()

    def destroy(self):
        for sub_step_id in self._cur_sub_guide_steps:
            step_cfg = GetQTEGuide()[sub_step_id]
            self.destroy_step(sub_step_id, step_cfg)

        VideoPlayer().stop_video()
        self._destroy_qte_guide()
        self.guide_ui().close()
        super(ComQTELocalBattleGuide, self).destroy()

    def battle_loading_finish(self):
        global_data.emgr.battle_loading_finished_event -= self.battle_loading_finish
        self.start_qte_guide_logic()

    def guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()

    def start_qte_guide_logic(self):
        global_data.player.local_battle_server and global_data.player.local_battle_server.regist_throw_item_explosion_event()
        global_data.emgr.switch_game_voice.emit(False)
        global_data.sound_mgr.play_music('Tutorial_N_Step1')
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            wwise.SoundEngine.Suspend(True)
            wwise.SoundEngine.WakeupFromSuspend()
        start_step_id = qte_guide_utils.get_lbs_qte_guide_step()
        step_cfg = GetQTEGuide()[start_step_id]
        init_data = step_cfg['InitData']
        self._init_qte_guide(init_data)
        self.execute_step(start_step_id, step_cfg)

    def _init_qte_guide(self, init_data):
        self.guide_ui().hide_main_ui()
        self._bind_check_position_event(is_bind=True)
        self._init_quit_ui()
        if global_data.is_pc_mode:
            self.qte_guide_ui = global_data.ui_mgr.show_ui('PCQTEGuideUI', 'logic.comsys.guide_ui')
        else:
            self.qte_guide_ui = global_data.ui_mgr.show_ui('QTEGuideUI', 'logic.comsys.guide_ui')
        self.qte_guide_ui.panel.setVisible(False)
        show_ui_list = init_data.get('show_ui')
        weapon_id = init_data.get('weapon')
        pre_steps = init_data.get('pre_steps', [])
        show_ui_list and self.show_ui('Init Guide', *show_ui_list)
        weapon_id and self.give_weapon('Init Guide', weapon_id)
        for step_id in pre_steps:
            cfg = GetQTEGuide()[step_id]
            self.execute_step(step_id, cfg)

    def _init_quit_ui(self):
        quit_ui = global_data.ui_mgr.get_ui('BattleRightTopUI')
        if not quit_ui:
            return
        quit_ui.panel.btn_observed and quit_ui.panel.btn_observed.setVisible(False)
        quit_ui.panel.btn_sound and quit_ui.panel.btn_sound.setVisible(False)
        quit_ui.panel.btn_speak and quit_ui.panel.btn_speak.setVisible(False)
        quit_ui.panel.btn_set and quit_ui.panel.btn_set.setVisible(False)
        if quit_ui.panel.btn_exit:
            quit_ui.panel.btn_exit.setVisible(True)
            quit_ui.panel.btn_exit.BindMethod('OnClick', self.quit_qte_local_battle)

    def quit_qte_local_battle(self, *args):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def on_confirm--- This code section failed: ---

 134       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'save_qte_guide_finish'
           6  LOAD_CONST            1  'Force quit qte'
           9  CALL_FUNCTION_1       1 
          12  POP_TOP          

 135      13  LOAD_DEREF            0  'self'
          16  LOAD_ATTR             1  'open_create_role_ui'
          19  LOAD_CONST            1  'Force quit qte'
          22  CALL_FUNCTION_1       1 
          25  POP_TOP          

 136      26  LOAD_DEREF            0  'self'
          29  LOAD_ATTR             2  'quit_qte_battle'
          32  LOAD_CONST            1  'Force quit qte'
          35  CALL_FUNCTION_1       1 
          38  POP_TOP          

 138      39  LOAD_GLOBAL           3  'global_data'
          42  LOAD_ATTR             4  'is_pc_mode'
          45  POP_JUMP_IF_FALSE   119  'to 119'

 139      48  LOAD_GLOBAL           3  'global_data'
          51  LOAD_ATTR             5  'mouse_mgr'
          54  LOAD_ATTR             6  '_mouse_ctrl'
          57  LOAD_ATTR             7  'cancel_force_disable'
          60  CALL_FUNCTION_0       0 
          63  POP_TOP          

 140      64  LOAD_GLOBAL           3  'global_data'
          67  LOAD_ATTR             8  'pc_ctrl_mgr'
          70  LOAD_ATTR             9  '_keyboard_ctrl'
          73  LOAD_ATTR             7  'cancel_force_disable'
          76  CALL_FUNCTION_0       0 
          79  POP_TOP          

 141      80  SETUP_LOOP           36  'to 119'
          83  LOAD_DEREF            0  'self'
          86  LOAD_ATTR            10  '_all_block_hotkeys'
          89  GET_ITER         
          90  FOR_ITER             22  'to 115'
          93  STORE_FAST            0  'key_const'

 142      96  LOAD_GLOBAL           3  'global_data'
          99  LOAD_ATTR             8  'pc_ctrl_mgr'
         102  LOAD_ATTR            11  'unblock_hotkey'
         105  LOAD_ATTR             2  'quit_qte_battle'
         108  CALL_FUNCTION_2       2 
         111  POP_TOP          
         112  JUMP_BACK            90  'to 90'
         115  POP_BLOCK        
       116_0  COME_FROM                '80'
         116  JUMP_FORWARD          0  'to 119'
       119_0  COME_FROM                '80'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 108

        SecondConfirmDlg2().confirm(content=5444, confirm_callback=on_confirm)

    def _destroy_qte_guide(self):
        self._bind_check_position_event(is_bind=False)
        if self.qte_guide_ui:
            self.qte_guide_ui.close()
            self.qte_guide_ui = None
        return

    def _bind_check_position_event(self, is_bind):
        if G_POS_CHANGE_MGR:
            if is_bind:
                self.unit_obj.regist_pos_change(self._check_pos_limit, 0.1)
            else:
                self.unit_obj.unregist_pos_change(self._check_pos_limit)
        elif is_bind:
            self.unit_obj.regist_event('E_POSITION', self._check_pos_limit)
        else:
            self.unit_obj.unregist_event('E_POSITION', self._check_pos_limit)

    def _check_pos_limit(self, pos):
        _range = self.battle.get_barrier_range()
        if any((item is None for item in _range)):
            return
        if pos.x < _range[0] or pos.x > _range[1] or pos.z < _range[2] or pos.z > _range[3]:
            self.send_event('E_SHOW_MESSAGE', get_text_by_id(5050))

    def _extract_step_cfg_info(self, step_cfg):
        func_name = step_cfg.get('Interface', None)
        if global_data.is_pc_mode:
            func_args = step_cfg.get('PCArgs', None) or step_cfg.get('Args', ())
        else:
            func_args = step_cfg.get('Args', ())
        func_type = step_cfg.get('InterfaceType', None)
        event_pair = step_cfg.get('Event', None)
        return (
         func_name, func_args, func_type, event_pair)

    def execute_step(self, step_id, step_cfg):
        if not self.is_valid():
            return
        else:
            func_name, func_args, func_type, event_pair = self._extract_step_cfg_info(step_cfg)
            if not func_name:
                log_error('!!!execute guide step fail(Interface not config), step_id: ', step_id)
                return
            if func_type == GUIDE_PROCESS_MODE_ONLY_DESTROY:
                return
            func = getattr(self, func_name, None)
            if func:
                func(step_id, *func_args)
            if event_pair:
                event_func_name = 'evt_{}'.format(event_pair[1])
                event_bind_func = getattr(self, event_func_name, None)
                if not event_bind_func:
                    origin_func = getattr(self, event_pair[1])
                    if not origin_func:
                        log_error('!!!!Propel event `%s`, func `%s`not define' % event_pair)
                        return

                    def event_bind_func(*args):
                        origin_func(step_id, *args)

                    setattr(self, event_func_name, event_bind_func)
                self.unit_obj.regist_event(event_pair[0], event_bind_func)
            return

    def destroy_step(self, step_id, step_cfg):
        if not self.is_valid():
            return
        else:
            init_func_name, func_args, func_type, event_pair = self._extract_step_cfg_info(step_cfg)
            if not init_func_name:
                return
            if func_type == GUIDE_PROCESS_MODE_ONLY_INIT:
                return
            func_name = '{}_destroy'.format(init_func_name)
            func = getattr(self, func_name, None)
            if func:
                func(step_id, *func_args)
            if event_pair:
                event_func_name = 'evt_{}'.format(event_pair[1])
                event_bind_func = getattr(self, event_func_name, None)
                if not event_bind_func:
                    return
                self.unit_obj.unregist_event(event_pair[0], event_bind_func)
                delattr(self, event_func_name)
            return

    def on_sub_guide_progress(self, step_id, *sub_guide_steps):
        self._key_step_map.clear()
        self._cur_sub_guide_steps = sub_guide_steps
        for step_id in sub_guide_steps:
            step_cfg = GetQTEGuide()[step_id]
            next_step_id = step_cfg.get('Next', None)
            if next_step_id is not None:
                self._key_step_map[step_id] = next_step_id
            self.execute_step(step_id, step_cfg)

        return

    def on_sub_guide_step_finish(self, step_id):
        from logic.gutils.salog import SALog
        salog_writer = SALog.get_instance()
        if salog_writer:
            salog_writer.write(SALog.TUTORIAL, step_id)
        next_sub_guide_step = self._key_step_map.get(step_id)
        if not next_sub_guide_step:
            return
        cur_sub_guide_steps = self._cur_sub_guide_steps
        self._cur_sub_guide_steps = []
        self._key_step_map = {}
        for sub_step_id in cur_sub_guide_steps:
            step_cfg = GetQTEGuide()[sub_step_id]
            self.destroy_step(sub_step_id, step_cfg)

        if self and self.unit_obj:
            cfg = GetQTEGuide()[next_sub_guide_step]
            self.execute_step(next_sub_guide_step, cfg)

    def save_guide_progress(self, step_id, sub_guide_id):
        qte_guide_utils.save_lbs_qte_guide_step(sub_guide_id)

    def show_human_tips(self, step_id, text_id, time_out):
        guide_ui = self.guide_ui()
        timeout_cb = lambda : self.on_sub_guide_step_finish(step_id)
        guide_ui.show_human_tips(get_text_by_id(text_id), time_out, timeout_cb)

    def show_human_tips_destroy(self, step_id, *_):
        guide_ui = self.guide_ui()
        guide_ui.show_human_tips_destroy()

    def show_ui(self, step_id, *ui_list):
        guide_ui = self.guide_ui()
        for key in ui_list:
            guide_ui.show_main_ui_by_type(key)

        self.on_sub_guide_step_finish(step_id)

    def play_guide_ui_animation(self, step_id, anim_nd, anim_name):
        count_down = 5 if anim_nd == 'nd_step_13' else None
        self.guide_ui().play_nd_animation(anim_nd, anim_name, count_down=count_down)
        return

    def play_guide_ui_animation_destroy(self, step_id, anim_nd, anim_name):
        self.guide_ui().play_nd_animation_destroy(anim_nd, anim_name)

    def show_guide_ui_nd(self, step_id, nd_name, nd_anim_name=None):
        self.guide_ui().show_drag_layer(nd_name, nd_anim_name)

    def show_guide_ui_nd_destroy(self, step_id, nd_name, nd_anim_name=None):
        self.guide_ui().show_drag_layer_destroy(nd_name, nd_anim_name)

    def show_sfx(self, step_id, position, sfx_path):

        def _on_target_pos_sfx(sfx):
            if self and self.is_valid():
                self._sfx_map[step_id] = sfx
                self.on_sub_guide_step_finish(step_id)
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(*position), on_create_func=_on_target_pos_sfx)

    def show_route(self, step_id, start_pos, end_position, sfx_path):

        def create_cb(sfx, step_id=step_id, end_position=end_position):
            if self and self.is_valid():
                self._sfx_map[step_id] = sfx
                ex, ey, ez = end_position
                sfx.end_pos = math3d.vector(ex, ey, ez)
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(*start_pos), on_create_func=create_cb)

    def show_sfx_destroy(self, step_id, *_):
        sfx = self._sfx_map.pop(step_id, None)
        if sfx:
            global_data.sfx_mgr.remove_sfx(sfx)
        return

    def show_route_destroy(self, step_id, *_):
        sfx = self._sfx_map.pop(step_id, None)
        if sfx:
            global_data.sfx_mgr.remove_sfx(sfx)
        return

    def show_locate(self, step_id, pos, offset, nd, anim_name=None):
        self.guide_ui().show_locate(pos, offset, nd, anim_name)

    def show_locate_destroy(self, step_id, pos, offset, nd, anim_name=None):
        self.guide_ui().show_locate_destroy(nd, anim_name)

    def check_move_pos(self, step_id, pos, offset):

        def check_move():
            if not global_data.player or not global_data.player.logic:
                return
            m_pos = global_data.player.logic.ev_g_position()
            if not m_pos:
                return
            dist = math3d.vector(*pos) - m_pos
            if dist.length < offset * NEOX_UNIT_SCALE:
                self.on_sub_guide_step_finish(step_id)

        self._move_timer = global_data.game_mgr.register_logic_timer(check_move, interval=0.1, mode=CLOCK)

    def check_move_pos_destroy--- This code section failed: ---

 374       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_move_timer'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 375      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 377      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             1  '_move_timer'
          22  POP_JUMP_IF_FALSE    56  'to 56'

 378      25  LOAD_GLOBAL           2  'global_data'
          28  LOAD_ATTR             3  'game_mgr'
          31  LOAD_ATTR             4  'unregister_logic_timer'
          34  LOAD_FAST             0  'self'
          37  LOAD_ATTR             1  '_move_timer'
          40  CALL_FUNCTION_1       1 
          43  POP_TOP          

 379      44  LOAD_CONST            0  ''
          47  LOAD_FAST             0  'self'
          50  STORE_ATTR            1  '_move_timer'
          53  JUMP_FORWARD          0  'to 56'
        56_0  COME_FROM                '53'
          56  LOAD_CONST            0  ''
          59  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def set_ui_nd_visibility(self, step_id, ui_name, ui_nd_list, is_visible):
        ui = global_data.ui_mgr.get_ui(ui_name)
        if not ui:
            return
        else:
            for nd_name in ui_nd_list:
                nd = getattr(ui, nd_name, None)
                nd and nd.setVisible(is_visible)

            self.on_sub_guide_step_finish(step_id)
            return

    def give_weapon(self, step_id, weapon_id):
        self._give_weapon(weapon_id)
        self.on_sub_guide_step_finish(step_id)

    def shoot_tips_on_aim(self, step_id, nd_name, anim_name):
        self.play_guide_ui_animation_destroy(step_id, nd_name, anim_name)
        self.on_sub_guide_step_finish(step_id)

    def shoot_tips_on_anim_destroy(self, step_id, nd_name, anim_name):
        self.play_guide_ui_animation_destroy(step_id, nd_name, anim_name)

    def create_monster(self, step_id, robot_dict):
        self.send_event('E_CALL_SYNC_METHOD', 'create_monster', (step_id, robot_dict))

    def create_monster_destroy(self, step_id, robot_dict):
        self.send_event('E_CALL_SYNC_METHOD', 'destroy_monster', (step_id, robot_dict))

    def camera_push_forward(self, step_id, *args):
        pass

    def play_video(self, step_id, video_path, *args):

        def finish_cb():
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                wwise.SoundEngine.Suspend(True)
                wwise.SoundEngine.WakeupFromSuspend()
            self.send_event('E_QTE_VIDEO_FINISH')

        def ready_cb():
            global_data.sound_mgr.play_music('Tutorial_N_Step2')
            self.on_sub_guide_step_finish(step_id)

        VideoPlayer().play_video(video_path, finish_cb, disable_sound_mgr=False, can_jump=True, video_ready_cb=ready_cb, clip_enable=False, skip_time=5)

    def disable_mouse_keyboard(self, step_id):
        import game
        KEYS_NEED_UP = [
         game.VK_W, game.VK_S, game.VK_A, game.VK_D]
        global_data.moveKeyboardMgr.stop_move_lock()
        for keycode in KEYS_NEED_UP:
            global_data.moveKeyboardMgr.process_input(keycode, game.MSG_KEY_UP)

        global_data.pc_ctrl_mgr._keyboard_ctrl.force_disable()
        self.on_sub_guide_step_finish(step_id)

    def disable_mouse_keyboard_destroy(self, step_id):
        global_data.pc_ctrl_mgr._keyboard_ctrl.cancel_force_disable()

    def create_ai_mecha(self, step_id, *args):
        params = (
         step_id,) + args
        self.send_event('E_CALL_SYNC_METHOD', 'create_ai_mecha', params)
        self.on_sub_guide_step_finish(step_id)

    def adjust_pos_yaw(self, step_id, pos, yaw):
        self.stop_rocker()
        self.send_event('E_DO_RB_POS', pos)
        cur_yaw = self.ev_g_yaw() or 0
        self.send_event('E_DELTA_YAW', yaw - cur_yaw)
        global_data.emgr.fireEvent('camera_set_yaw_event', yaw)
        global_data.emgr.fireEvent('camera_set_pitch_event', 0)

    def ai_mecha_fire(self, step_id, mecha_step_id):
        self.send_event('E_CALL_SYNC_METHOD', 'ai_mecha_fire', (step_id, mecha_step_id))

    def ai_mecha_fire_finish(self, step_id, finish_time, action_time):
        self.qte_resume_throw_item()

        def delay_finish():
            self.on_sub_guide_step_finish(step_id)

        global_data.game_mgr.delay_exec(finish_time, delay_finish)

        def rate_action():
            global_data.game_mgr.set_global_speed_rate(1.0)

        global_data.game_mgr.delay_exec(action_time, rate_action)
        self.unit_obj.regist_event('E_CTRL_ROLL_END', self._end_roll_631)
        self.qte_guide_ui.panel.setVisible(True)
        self.qte_guide_ui.panel.bg_black.setVisible(False)

    def disable_mouse_ctrl(self, step_id):
        mouse_ctrl = global_data.mouse_mgr._mouse_ctrl
        if mouse_ctrl:
            mouse_ctrl.force_disable()
        global_data.emgr.enable_camera_yaw.emit(False)

    def resume_mouse_ctrl(self, step_id):
        mouse_ctrl = global_data.mouse_mgr._mouse_ctrl
        if mouse_ctrl:
            mouse_ctrl.cancel_force_disable()
        global_data.emgr.enable_camera_yaw.emit(True)

    def disable_camera_yaw(self, step_id):
        global_data.emgr.enable_camera_yaw.emit(False)

    def disable_camera_yaw_destroy(self, step_id):
        global_data.emgr.enable_camera_yaw.emit(True)

    def disable_keyboard_and_mouse_left(self, step_id):
        import game
        KEYS_NEED_UP = [
         game.VK_W, game.VK_S, game.VK_A, game.VK_D]
        global_data.moveKeyboardMgr.stop_move_lock()
        for keycode in KEYS_NEED_UP:
            global_data.moveKeyboardMgr.process_input(keycode, game.MSG_KEY_UP)

        global_data.pc_ctrl_mgr._keyboard_ctrl.force_disable()
        global_data.mecha.logic.send_event('E_ALL_ACTION_UP')
        global_data.mecha.logic.send_event('E_ROCK_STOP')
        self.disable_hotkey(step_id, 'HUMAN_FIRE', 'MECHA_FIRE')

    def disable_keyboard_and_mouse_left_destroy(self, step_id):
        global_data.pc_ctrl_mgr._keyboard_ctrl.cancel_force_disable()
        self.enable_hotkey(step_id, 'HUMAN_FIRE', 'MECHA_FIRE')

    def disable_hotkey(self, step_id, *hotkey_list):
        from data import hot_key_def
        if not global_data.is_pc_mode:
            return
        else:
            for key_const_name in hotkey_list:
                key_const = getattr(hot_key_def, key_const_name, None)
                if key_const:
                    global_data.pc_ctrl_mgr.block_hotkey(key_const, 'local_battle_guide')
                    self._all_block_hotkeys.add(key_const)

            self.on_sub_guide_step_finish(step_id)
            return

    def enable_hotkey(self, step_id, *hotkey_list):
        from data import hot_key_def
        if not global_data.is_pc_mode:
            return
        else:
            for key_const_name in hotkey_list:
                key_const = getattr(hot_key_def, key_const_name, None)
                if key_const:
                    global_data.pc_ctrl_mgr.unblock_hotkey(key_const, 'local_battle_guide')
                    if key_const in self._all_block_hotkeys:
                        self._all_block_hotkeys.remove(key_const)

            self.on_sub_guide_step_finish(step_id)
            return

    def enable_hotkey_core(self, hotkey_list):
        from data import hot_key_def
        if not global_data.is_pc_mode:
            return
        else:
            for key_const_name in hotkey_list:
                key_const = getattr(hot_key_def, key_const_name, None)
                if key_const:
                    global_data.pc_ctrl_mgr.unblock_hotkey(key_const, 'local_battle_guide')
                    if key_const in self._all_block_hotkeys:
                        self._all_block_hotkeys.remove(key_const)

            return

    def _end_roll_631(self):
        self.sd.ref_rocker_dir = math3d.vector(0, 0, 0)
        self.unit_obj.unregist_event('E_CTRL_ROLL_END', self._end_roll_631)
        self.qte_guide_ui.panel.setVisible(False)
        self.qte_guide_ui.panel.bg_black.setVisible(False)

    def qte_break_throw_item(self):
        scene = global_data.game_mgr.scene
        part_throwable_mgr = scene.get_com('PartThrowableManager')
        if part_throwable_mgr and part_throwable_mgr.throw_items:
            throw_items = part_throwable_mgr.throw_items
            from mobile.common.EntityManager import EntityManager
            for uniq_key in throw_items:
                eid = throw_items[uniq_key][0]
                ent = EntityManager.getentity(eid)
                if not ent:
                    continue
                logic = ent.logic._coms['ComGrenadeCollision']
                logic.need_update = False
                logic._spread_radius = 8 * NEOX_UNIT_SCALE
                logic.qte_break_speed()

    def qte_resume_throw_item(self):
        scene = global_data.game_mgr.scene
        part_throwable_mgr = scene.get_com('PartThrowableManager')
        if part_throwable_mgr and part_throwable_mgr.throw_items:
            throw_items = part_throwable_mgr.throw_items
            from mobile.common.EntityManager import EntityManager
            for uniq_key in throw_items:
                eid = throw_items[uniq_key][0]
                ent = EntityManager.getentity(eid)
                logic = ent.logic._coms['ComGrenadeCollision']
                logic.need_update = True
                logic._spread_radius = 8 * NEOX_UNIT_SCALE
                logic.qte_resume_speed()

    def freeze_bullet_tick(self, step_id, delay):
        self.on_sub_guide_step_finish(step_id)

    def resume_bullet_tick(self, step_id):
        self.on_sub_guide_step_finish(step_id)

    def show_qte_ui(self, step_id):
        self.on_sub_guide_step_finish(step_id)

    def rocker_move_left(self, step_id):
        self.send_event('E_ADD_BLACK_STATE', {st_const.ST_RUN, st_const.ST_MOVE, st_const.ST_JUMP_1})

    def rocker_move_left_destroy(self, step_id, *args):
        self.send_event('E_CLEAR_BLACK_STATE')

    def qte_guide_step(self, step_id, text_id, step_name, delay=0):
        self.qte_guide_ui.panel.setVisible(True)
        self.run_lock_forbidden(True)

        def show_step():
            if not self.qte_guide_ui:
                return
            else:
                self.qte_guide_ui.show_human_tips(text_id)
                step_func_name = 'show_{}'.format(step_name)
                func = getattr(self.qte_guide_ui, step_func_name, None)
                if func:
                    func()
                self.on_sub_guide_step_finish(step_id)
                return

        if not delay:
            show_step()
            return
        global_data.game_mgr.delay_exec(delay, show_step)

    def qte_guide_step_destroy(self, step_id, text_id, step_name, delay=0):
        if self.qte_guide_ui and self.qte_guide_ui.panel and self.qte_guide_ui.panel.isValid():
            self.qte_guide_ui.hide_human_tips()
        self.run_lock_forbidden(False)
        step_func_name = 'hide_{}'.format(step_name)
        func = getattr(self.qte_guide_ui, step_func_name, None)
        if func:
            func()
        if self.qte_guide_ui and self.qte_guide_ui.panel and self.qte_guide_ui.panel.isValid():
            self.qte_guide_ui.panel.setVisible(False)
        self.on_sub_guide_step_finish(step_id)
        return

    def click_roll_btn(self, step_id, finish_time, action_time, action_rate):

        def delay_finish():
            self.qte_break_throw_item()
            self.send_event('E_ADD_BLACK_STATE', {st_const.ST_RUN, st_const.ST_MOVE, st_const.ST_JUMP_1})
            self.send_event('E_MOVE_STOP')
            self.send_event('E_PAUSE_ANIM')
            if finish_time >= action_time:
                self.enable_hotkey_core(['HUMAN_ROLL'])

        global_data.game_mgr.delay_exec(finish_time, delay_finish)

        def rate_action():
            global_data.game_mgr.set_global_speed_rate(action_rate)
            if finish_time < action_time:
                self.enable_hotkey_core(['HUMAN_ROLL'])

        global_data.game_mgr.delay_exec(action_time, rate_action)

    def click_roll_btn_destroy(self, step_id, *_):
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_RESUME_ANIM')
        self.sd.ref_rocker_dir = math3d.vector(-1, 0, 0)

    def check_summon_mecha(self, step_id):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if not ui:
            return
        ui.clear_mecha_cd_timer()
        ui.on_add_mecha_progress(100)
        ui.get_mecha_count_down = 0
        ui.get_mecha_count_down_progress = 0
        if not self.summon_timer:
            self.summon_timer = delay.call(5, lambda : delay_summon_mecha())

        def delay_summon_mecha(*args):
            if self.summon_timer:
                self.summon_timer = None
            on_click_summon_mecha(*args)
            return

        def on_click_summon_mecha(*args):
            self.send_event('E_CLICK_SUMMON_MECHA')
            if self.summon_timer:
                delay.cancel(self.summon_timer)
                self.summon_timer = None
            return

        ui.temp_mech_call.btn_mech_call.UnBindMethod('OnClick')
        ui.temp_mech_call.btn_mech_call.BindMethod('OnClick', on_click_summon_mecha)

    def check_summon_mecha_destroy(self, step_id):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if self.summon_timer:
            delay.cancel(self.summon_timer)
            self.summon_timer = None
        if not ui:
            return
        else:
            ui.temp_mech_call.btn_mech_call.UnBindMethod('OnClick')
            ui.temp_mech_call.btn_mech_call.BindMethod('OnClick', ui.on_mecha_call)
            return

    def play_mecha_show_video(self, step_id, video_path_config):
        role_id = self.ev_g_role_id()
        video_path = video_path_config.get(role_id, None)
        if not video_path:
            return
        else:

            def finish_cb():
                if game3d.get_platform() == game3d.PLATFORM_IOS:
                    wwise.SoundEngine.Suspend(True)
                    wwise.SoundEngine.WakeupFromSuspend()
                self.send_event('E_QTE_VIDEO_FINISH')
                ui = global_data.ui_mgr.get_ui('MechaCockpitUI')
                if ui:
                    ui.leave_screen()
                    ui.enter_screen()

            def ready_cb():
                global_data.sound_mgr.play_music('Tutorial_N_Step3')
                self.on_sub_guide_step_finish(step_id)

            VideoPlayer().play_video(video_path, finish_cb, disable_sound_mgr=False, can_jump=True, video_ready_cb=ready_cb, clip_enable=False, skip_time=5)
            return

    def summon_mecha(self, step_id, summon_mecha_config, force_pos, force_yaw):
        from logic.gutils.mecha_utils import CallMecha
        role_id = self.ev_g_role_id()
        mecha_id = summon_mecha_config.get(role_id, None)
        if not mecha_id:
            return
        else:
            res, pos = CallMecha()
            if not res:
                self.adjust_pos_yaw(step_id, force_pos, force_yaw)
                res, pos = CallMecha()
            if not res and force_pos:
                pos = math3d.vector(*force_pos)
            yaw = self.ev_g_yaw()
            self.stop_rocker()
            self.send_event('E_CALL_SYNC_METHOD', 'create_mecha', (mecha_id, (pos.x, pos.y, pos.z), yaw), True)
            self.on_sub_guide_step_finish(step_id)
            return

    def show_mecha_locate(self, step_id, mecha_step_id, offset, nd, anim_name=None):
        if not global_data.player or not global_data.player.local_battle_server:
            return

        def _show_locate(pos):
            self.show_locate(step_id, pos, offset, nd, anim_name)
            self.on_sub_guide_step_finish(step_id)
            self.unit_obj.unregist_event('E_QTE_MECHA_POS', _show_locate)

        self.unit_obj.regist_event('E_QTE_MECHA_POS', _show_locate)
        self.send_event('E_CALL_SYNC_METHOD', 'show_mecha_locate', (mecha_step_id,))

    def show_mecha_locate_destroy(self, step_id, mecha_step_id, offset, nd, anim_name=None):
        self.guide_ui().show_locate_destroy(nd, anim_name)

    def disable_leave_mecha_hotkey(self, step_id):
        self.disable_hotkey(step_id, 'SUMMON_CALL_MECHA')
        self.on_sub_guide_step_finish(step_id)

    def enable_leave_mecha_hotkey(self, step_id):
        self.enable_hotkey(step_id, 'SUMMON_CALL_MECHA')
        self.on_sub_guide_step_finish(step_id)

    def hide_sub_weapon_btn(self, step_id):
        mecha_ctrl_ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not mecha_ctrl_ui:
            return
        mecha_ctrl_ui.panel.nd_action_custom_4.setVisible(False)
        self.on_sub_guide_step_finish(step_id)

    def hide_sub_weapon_btn_destroy(self, step_id):
        mecha_ctrl_ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not mecha_ctrl_ui:
            return
        mecha_ctrl_ui.panel.nd_action_custom_4.setVisible(True)
        mecha_ctrl_ui.panel.action4.PlayAnimation('show')

    def check_sub_weapon_click(self, step_id):
        mecha_ctrl_ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not mecha_ctrl_ui:
            return
        self.stop_rocker()
        sub_weapon_nd = mecha_ctrl_ui.panel.action4.bar
        mecha_ctrl_ui.action_btns['action4'].enableRocker(False)
        sub_weapon_nd.UnBindMethod('OnClick')
        sub_weapon_nd.UnBindMethod('OnBegin')
        sub_weapon_nd.UnBindMethod('OnDrag')
        sub_weapon_nd.UnBindMethod('OnEnd')

        def on_click_sub_weapon(*args):
            self.on_sub_guide_step_finish(step_id)

        sub_weapon_nd.BindMethod('OnBegin', on_click_sub_weapon)

    def play_execute_video(self, step_id, video_conf):
        role_id = self.ev_g_role_id()
        video_path = video_conf.get(role_id, None)
        if not video_path:
            return
        else:

            def finish_cb():
                if game3d.get_platform() == game3d.PLATFORM_IOS:
                    wwise.SoundEngine.Suspend(True)
                    wwise.SoundEngine.WakeupFromSuspend()
                self.on_sub_guide_step_finish(step_id)

            def ready_cb():
                global_data.sound_mgr.play_music('Tutorial_N_Step4')

            VideoPlayer().play_video(video_path, finish_cb, video_ready_cb=ready_cb, disable_sound_mgr=False, can_jump=False, clip_enable=False)
            return

    def save_qte_guide_finish(self, step_id, *_):
        from common.platform.appsflyer import Appsflyer
        from common.platform.appsflyer_const import AF_TUTORIAL_COMPLETION
        from logic.gutils.salog import SALog
        qte_guide_utils.set_qte_guide_finish()
        Appsflyer().advert_track_event(AF_TUTORIAL_COMPLETION)
        salog_writer = SALog.get_instance()
        if salog_writer:
            salog_writer.write(SALog.TUTORIAL, step_id)

    def open_create_role_ui(self, step_id):
        global_data.emgr.switch_game_voice.emit(True)
        global_data.sound_mgr.stop_music()
        from logic.comsys.login.CharacterCreatorUINew import CharacterCreatorUINew
        CharacterCreatorUINew(opt_from='qte_guide_finish')
        global_data.ui_mgr.close_all_ui(exceptions=('CharacterCreatorUINew', 'QTEGuideUI',
                                                    'PCQTEGuideUI', 'WizardTrace'))

    def quit_qte_battle(self, step_id):
        if global_data.player:
            global_data.player.quit_new_local_battle()

    def _give_weapon(self, weapon_id):
        iMagSize = confmgr.get('firearm_config', str(weapon_id))['iMagSize']
        item_data = {'item_id': weapon_id,'entity_id': IdManager.genid(),'count': 1,'iBulletNum': iMagSize}
        self.send_event('E_PICK_UP_WEAPON', item_data, const.PART_WEAPON_POS_MAIN1, True)
        self.send_event('E_SWITCHING', const.PART_WEAPON_POS_MAIN1)

    def stop_rocker(self):
        ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if ui:
            ui.stop_rocker()

    def run_lock_forbidden(self, flag):
        ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if ui:
            ui.forbid_run_lock(flag)

    def guide_shoot_show(self, step_id, is_show):
        if is_show:
            self.play_guide_ui_animation(None, 'nd_step_3', 'show_3')
            self.guide_ui().update_auto_frame(self.sd.ref_wp_bar_cur_weapon, self.ev_g_at_aim_args_all())
            self.play_guide_ui_animation(None, 'nd_auto_frame', 'show_auto')
        else:
            self.play_guide_ui_animation_destroy(None, 'nd_step_3', 'show_3')
            self.play_guide_ui_animation_destroy(None, 'nd_auto_frame', 'show_auto')
        return

    def guide_robot_dead(self, step_id):
        global_data.game_mgr.delay_exec(2.0, lambda : self.on_sub_guide_step_finish(step_id))

    def on_rocker_move_left(self, step_id, direction, *_):
        if direction.is_zero:
            return
        left_vec = math3d.vector(-1, 0, 0)
        cos_v = left_vec.dot(direction) / direction.length
        angle = math.degrees(math.acos(cos_v))
        if angle < 30:
            self.on_sub_guide_step_finish(step_id)

    def on_click_roll(self, step_id):
        self.on_sub_guide_step_finish(step_id)

    def on_click_summon(self, step_id):
        self.on_sub_guide_step_finish(step_id)

    def on_guide_mecha_agony(self, step_id):
        self.on_sub_guide_step_finish(step_id)

    def hide_leave_mecha(self, step_id, *args):
        ui = global_data.ui_mgr.get_ui('StateChangeUI')
        ui.panel.btn_change_to_human.setVisible(False)
        ui.panel.btn_change_to_mech.setVisible(False)
        self.on_sub_guide_step_finish(step_id)

    def on_qte_video_finish(self, step_id, *args):
        self.on_sub_guide_step_finish(step_id)

    def qte_mecha_shoot(self, step_id, mecha_create_step):
        self.send_event('E_CALL_SYNC_METHOD', 'qte_start_mecha_shoot', (step_id, mecha_create_step))

    def qte_mecha_shoot_destroy(self, step_id, mecha_create_step):
        self.send_event('E_CALL_SYNC_METHOD', 'qte_stop_mecha_logic', (step_id, mecha_create_step))