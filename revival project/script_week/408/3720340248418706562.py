# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComLocalBattleGuide.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.comsys.guide_ui.GuideUI import GuideUI, LeaveGuideUI, PCGuideUI
from logic.comsys.guide_ui.NewbieStageSideTipUI import NewbieStageSideTipUI
from data.c_guide_data import GetLocalGuide, get_init_guide_data
from data.newbie_stage_config import GetStageHuman, GetStageMecha, GetDoorConfig, GetStageHumanHandler
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.IdManager import IdManager
import logic.gcommon.const as const
import logic.gutils.delay as delay
from data.c_guide_data import get_handler_params
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2, NormalConfirmUI2
from logic.gcommon.const import NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE, PART_WEAPON_POS_MAIN2
from logic.client.const import game_mode_const
from common.utils.timer import CLOCK
from common.cfg import confmgr
from logic.gutils.salog import SALog
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_TUTORIAL_COMPLETION
from logic.gutils import task_utils
from mobile.common.EntityManager import EntityManager

class ComLocalBattleGuide(UnitCom):
    BIND_EVENT = {'E_FINISH_GUIDE': 'finish_guide',
       'E_GUIDE_RESET': 'construct_guide_logic',
       'E_GUIDE_DESTROY': 'destroy_battle_guide',
       'E_GUIDE_POS_CHECK': '_regist_check_pos',
       'G_GUIDE_CONSTRUCT': '_get_guild_construct',
       'E_GUIDE_INIT_WEAPONS': 'pick_up_weapons',
       'G_GUIDE_STATECHANGE_VISIBLE': 'get_state_change_ui_visible_flag',
       'E_LOCAL_BATTLE_ESC_1_2': 'on_click_quit_btn',
       'E_ON_LEAVE_MECHA': 'on_leave_mecha'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComLocalBattleGuide, self).init_from_dict(unit_obj, bdict)
        self._sfx_map = {}
        self._move_timer = None
        self._mecha_charger = None
        self._cur_step = None
        self._delay_call = None
        self._eagle_flag_delay_call = None
        self._locate_sfx_delay_call = None
        self._construct_flag = False
        self._regist_mecha_dash_event_flag = False
        self._has_robot_mecha_lower_hp = False
        self._cur_switch_gun_step = None
        self._visible_to_human = False
        self._visible_to_mecha = False
        self.create_robot_skill_param = None
        self._min_x = None
        self._max_x = None
        self._min_z = None
        self._max_z = None
        self._regist_throw_explosion_event_flag = False
        return

    def on_init_complete(self):
        if not self.battle:
            return
        if global_data.player.in_local_battle() and self.battle.get_battle_tid() in (const.NEWBIE_STAGE_HUMAN_BATTLE, const.NEWBIE_STAGE_MECHA_BATTLE):
            self._guide_ui.hide_main_ui(exceptions=('BattleInfoUI', ))
            if self.battle.get_battle_tid() == const.NEWBIE_STAGE_HUMAN_BATTLE and not global_data.is_pc_mode:
                self._guide_ui.panel.nd_cannot_move.setVisible(True)
            if global_data.ui_mgr.get_ui('BattleLoadingWidget'):
                global_data.emgr.battle_loading_finished_event += self.construct_guide_logic
            else:
                self.construct_guide_logic(False)

    def _get_guild_construct(self):
        return self._construct_flag

    @property
    def _guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()

    @property
    def side_tip_ui(self):
        return NewbieStageSideTipUI()

    def construct_guide_logic(self, event_flag=True):
        if self._construct_flag:
            return
        else:
            self._construct_flag = True
            self.process_throw_item_explosion_event()
            if event_flag:
                global_data.emgr.battle_loading_finished_event -= self.construct_guide_logic
            self.guid_cfg = self.get_guide_config_by_id_func()
            self._guide_ui.hide_main_ui()
            self.unit_obj.regist_event('E_GUIDE_OPEN_MAIN_SETTING', self.guide_open_main_setting)
            self.unit_obj.regist_event('E_GUIDE_CLOSE_MAIN_SETTING', self.guide_close_main_setting)
            global_data.emgr.auto_aim_pos_update += self.update_auto_aim
            guide_id = global_data.player.get_lbs_step()
            global_data.player.need_eject_driver = False
            local_battle = global_data.player.get_battle()
            if local_battle:
                self._min_x, self._max_x, self._min_z, self._max_z = local_battle.get_barrier_range()
            if G_POS_CHANGE_MGR:
                self.unit_obj.regist_pos_change(self._check_pos, 0.1)
            else:
                self.unit_obj.regist_event('E_POSITION', self._check_pos)
            self._guide_ui.show_main_ui_by_type('BattleInfoUI')
            self.init_quit_ui()
            if guide_id is None:
                first_guide_id = self.get_first_guide_id()
                self.propel_guide(first_guide_id)
                self._cur_step = first_guide_id
                self.send_event('E_SET_IS_HAVE_GUN', 0)
                return
            self.show_human_tips_destroy()
            self._cur_step = guide_id
            cfg = self.guid_cfg(guide_id)
            self.init_show_main_ui(guide_id)
            self.init_guide_data(guide_id)
            self.propel_steps(cfg.get('Next', None), cfg.get('NextShowMainUI', None))
            return

    def init_quit_ui(self):
        if global_data.is_pc_mode:
            return
        self._guide_ui.show_main_ui_by_type('BattleRightTopUI')
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

        dlg.confirm(content=tip_text_id, confirm_callback=on_confirm)

    def _regist_check_pos(self, lmecha, flag):
        if G_POS_CHANGE_MGR:
            if flag:
                lmecha.regist_pos_change(self._check_pos, 0.1)
            else:
                lmecha.unregist_pos_change(self._check_pos)
        elif flag:
            lmecha.regist_event('E_POSITION', self._check_pos)
        else:
            lmecha.unregist_event('E_POSITION', self._check_pos)

    def _check_pos(self, pos):
        if self._min_x is None or self._max_x is None or self._min_z is None or self._max_z is None:
            return
        else:
            if not (self._min_x <= pos.x <= self._max_x and self._min_z <= pos.z <= self._max_z):
                self.send_event('E_SHOW_MESSAGE', get_text_local_content(5050))
            return

    def update_auto_aim(self, *_):
        pass

    def guide_open_main_setting(self, ui):
        self._guide_ui.panel.setVisible(False)
        if ui.ref_btn_exit:
            ui.ref_btn_exit.btn.SetText(5030)

    def guide_close_main_setting(self, *_):
        self._guide_ui.panel.setVisible(True)

    def init_show_main_ui(self, guide_id):
        cfg = self.guid_cfg(guide_id)
        prior = cfg.get('Prior', None)
        if prior:
            self.show_main_ui(self.guid_cfg(prior).get('NextShowMainUI', None))
            self.init_show_main_ui(prior)
        return

    def init_guide_data(self, guide_id):
        info = get_init_guide_data(guide_id)
        if info:
            self.init_weapons(info.get('weapons', None))
            self.init_items(info.get('items', None))
            self.init_mecha_progress(info.get('mecha_progress', None))
            self.init_mecha(info.get('mecha', None))
            self.init_hp(info.get('hp', None))
        return

    def init_hp(self, hp):
        if hp:
            self.send_event('S_HP', hp)

    def init_mecha(self, mecha):
        if mecha:
            pos = self.ev_g_position()
            global_data.player._lbs_create_mecha(mecha, (pos.x, pos.y, pos.z))
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
        if weapon_id == 10012:
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

    def get_guide_config_by_id_func(self):
        if not self.battle:
            return
        else:
            battle_type = self.battle.get_battle_tid()
            get_guide_config_func = None
            if battle_type == NEWBIE_STAGE_HUMAN_BATTLE:
                get_guide_config_func = GetStageHuman
            else:
                get_guide_config_func = GetStageMecha

            def get_config_by_guide_id(guide_id):
                return get_guide_config_func()[guide_id]

            return get_config_by_guide_id

    def get_first_guide_id(self):
        if not self.battle:
            return
        else:
            battle_type = self.battle.get_battle_tid()
            if battle_type == NEWBIE_STAGE_HUMAN_BATTLE:
                return 100
            return 100

    def get_final_guide_id(self):
        if not self.battle:
            return
        else:
            battle_type = self.battle.get_battle_tid()
            if battle_type == NEWBIE_STAGE_HUMAN_BATTLE:
                return 1301
            return 1401

    def propel_steps(self, steps, ui_list=None, force=None):
        self.show_main_ui(ui_list)
        if steps:
            if isinstance(steps, (list, tuple)):
                for step in steps:
                    self.propel_guide(step, force)

            else:
                self.propel_guide(steps, force)

    def propel_guide(self, guide_id, force=None):
        cfg = self.guid_cfg(guide_id)
        if global_data.is_pc_mode:
            func_name = cfg.get('PCInterface', cfg.get('Interface', None))
        else:
            func_name = cfg.get('Interface', None)
        if global_data.is_pc_mode:
            func_args = cfg.get('PCArgs', cfg.get('Args', []))
        else:
            func_args = cfg.get('Args', [])
        func_type = cfg.get('InterfaceType', None)
        if func_type is None or func_type == 1 or force:
            if func_name:
                cfg.get('Args', [])
                func = getattr(self, func_name)
                if isinstance(func_args, (list, tuple)):
                    func(guide_id, *func_args)
                else:
                    func(guide_id, func_args)
            if global_data.is_pc_mode:
                event = cfg.get('PCEvent', cfg.get('Event', None))
            else:
                event = cfg.get('Event', None)
            if event:
                self.unit_obj.regist_event(event[0], getattr(self, event[1]))
                if event[1] == 'guide_switch_end_by_guide_id':
                    self._cur_switch_gun_step = guide_id
        return

    def destroy_steps(self, steps, force=None):
        if steps:
            if isinstance(steps, (list, tuple)):
                for step in steps:
                    self.destroy_guide(step, force)

            else:
                self.destroy_guide(steps, force)

    def destroy_guide--- This code section failed: ---

 379       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'guid_cfg'
           6  LOAD_FAST             1  'guide_id'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            3  'cfg'

 380      15  LOAD_GLOBAL           1  'global_data'
          18  LOAD_ATTR             2  'is_pc_mode'
          21  POP_JUMP_IF_FALSE    57  'to 57'

 381      24  LOAD_FAST             3  'cfg'
          27  LOAD_ATTR             3  'get'
          30  LOAD_CONST            1  'PCInterface'
          33  LOAD_FAST             3  'cfg'
          36  LOAD_ATTR             3  'get'
          39  LOAD_CONST            2  'Interface'
          42  LOAD_CONST            0  ''
          45  CALL_FUNCTION_2       2 
          48  CALL_FUNCTION_2       2 
          51  STORE_FAST            4  'func_name'
          54  JUMP_FORWARD         18  'to 75'

 383      57  LOAD_FAST             3  'cfg'
          60  LOAD_ATTR             3  'get'
          63  LOAD_CONST            2  'Interface'
          66  LOAD_CONST            0  ''
          69  CALL_FUNCTION_2       2 
          72  STORE_FAST            4  'func_name'
        75_0  COME_FROM                '54'

 384      75  LOAD_GLOBAL           1  'global_data'
          78  LOAD_ATTR             2  'is_pc_mode'
          81  POP_JUMP_IF_FALSE   117  'to 117'

 385      84  LOAD_FAST             3  'cfg'
          87  LOAD_ATTR             3  'get'
          90  LOAD_CONST            3  'PCArgs'
          93  LOAD_FAST             3  'cfg'
          96  LOAD_ATTR             3  'get'
          99  LOAD_CONST            4  'Args'
         102  BUILD_LIST_0          0 
         105  CALL_FUNCTION_2       2 
         108  CALL_FUNCTION_2       2 
         111  STORE_FAST            5  'func_args'
         114  JUMP_FORWARD         18  'to 135'

 387     117  LOAD_FAST             3  'cfg'
         120  LOAD_ATTR             3  'get'
         123  LOAD_CONST            4  'Args'
         126  BUILD_LIST_0          0 
         129  CALL_FUNCTION_2       2 
         132  STORE_FAST            5  'func_args'
       135_0  COME_FROM                '114'

 388     135  LOAD_FAST             3  'cfg'
         138  LOAD_ATTR             3  'get'
         141  LOAD_CONST            5  'InterfaceType'
         144  LOAD_CONST            0  ''
         147  CALL_FUNCTION_2       2 
         150  STORE_FAST            6  'func_type'

 389     153  LOAD_FAST             6  'func_type'
         156  LOAD_CONST            0  ''
         159  COMPARE_OP            8  'is'
         162  POP_JUMP_IF_TRUE    183  'to 183'
         165  LOAD_FAST             6  'func_type'
         168  LOAD_CONST            6  2
         171  COMPARE_OP            2  '=='
         174  POP_JUMP_IF_TRUE    183  'to 183'
         177  LOAD_FAST             2  'force'
       180_0  COME_FROM                '174'
       180_1  COME_FROM                '162'
         180  POP_JUMP_IF_FALSE   438  'to 438'

 390     183  LOAD_FAST             4  'func_name'
         186  POP_JUMP_IF_FALSE   263  'to 263'

 391     189  LOAD_GLOBAL           5  'getattr'
         192  LOAD_GLOBAL           7  'isinstance'
         195  LOAD_ATTR             6  'format'
         198  LOAD_FAST             4  'func_name'
         201  CALL_FUNCTION_1       1 
         204  CALL_FUNCTION_2       2 
         207  STORE_FAST            7  'func'

 392     210  LOAD_GLOBAL           7  'isinstance'
         213  LOAD_FAST             5  'func_args'
         216  LOAD_GLOBAL           8  'list'
         219  LOAD_GLOBAL           9  'tuple'
         222  BUILD_TUPLE_2         2 
         225  CALL_FUNCTION_2       2 
         228  POP_JUMP_IF_FALSE   247  'to 247'

 393     231  LOAD_FAST             7  'func'
         234  LOAD_FAST             1  'guide_id'
         237  LOAD_FAST             5  'func_args'
         240  CALL_FUNCTION_VAR_1     1 
         243  POP_TOP          
         244  JUMP_ABSOLUTE       263  'to 263'

 395     247  LOAD_FAST             7  'func'
         250  LOAD_FAST             1  'guide_id'
         253  LOAD_FAST             5  'func_args'
         256  CALL_FUNCTION_2       2 
         259  POP_TOP          
         260  JUMP_FORWARD          0  'to 263'
       263_0  COME_FROM                '260'

 397     263  LOAD_GLOBAL           1  'global_data'
         266  LOAD_ATTR             2  'is_pc_mode'
         269  POP_JUMP_IF_FALSE   305  'to 305'

 398     272  LOAD_FAST             3  'cfg'
         275  LOAD_ATTR             3  'get'
         278  LOAD_CONST            8  'PCEvent'
         281  LOAD_FAST             3  'cfg'
         284  LOAD_ATTR             3  'get'
         287  LOAD_CONST            9  'Event'
         290  LOAD_CONST            0  ''
         293  CALL_FUNCTION_2       2 
         296  CALL_FUNCTION_2       2 
         299  STORE_FAST            8  'event'
         302  JUMP_FORWARD         18  'to 323'

 400     305  LOAD_FAST             3  'cfg'
         308  LOAD_ATTR             3  'get'
         311  LOAD_CONST            9  'Event'
         314  LOAD_CONST            0  ''
         317  CALL_FUNCTION_2       2 
         320  STORE_FAST            8  'event'
       323_0  COME_FROM                '302'

 401     323  LOAD_FAST             8  'event'
         326  POP_JUMP_IF_FALSE   368  'to 368'

 402     329  LOAD_FAST             0  'self'
         332  LOAD_ATTR            10  'unit_obj'
         335  LOAD_ATTR            11  'unregist_event'
         338  LOAD_FAST             8  'event'
         341  LOAD_CONST           10  ''
         344  BINARY_SUBSCR    
         345  LOAD_GLOBAL           5  'getattr'
         348  LOAD_FAST             0  'self'
         351  LOAD_FAST             8  'event'
         354  LOAD_CONST           11  1
         357  BINARY_SUBSCR    
         358  CALL_FUNCTION_2       2 
         361  CALL_FUNCTION_2       2 
         364  POP_TOP          
         365  JUMP_FORWARD          0  'to 368'
       368_0  COME_FROM                '365'

 404     368  LOAD_FAST             0  'self'
         371  LOAD_ATTR             0  'guid_cfg'
         374  LOAD_FAST             1  'guide_id'
         377  CALL_FUNCTION_1       1 
         380  STORE_FAST            3  'cfg'

 405     383  LOAD_FAST             3  'cfg'
         386  LOAD_ATTR             3  'get'
         389  LOAD_CONST           12  'Prior'
         392  LOAD_CONST            0  ''
         395  CALL_FUNCTION_2       2 
         398  LOAD_CONST            0  ''
         401  COMPARE_OP            8  'is'
         404  POP_JUMP_IF_FALSE   438  'to 438'

 406     407  LOAD_FAST             0  'self'
         410  LOAD_ATTR            12  'destroy_steps'
         413  LOAD_FAST             3  'cfg'
         416  LOAD_ATTR             3  'get'
         419  LOAD_CONST           13  'Next'
         422  LOAD_CONST            0  ''
         425  CALL_FUNCTION_2       2 
         428  CALL_FUNCTION_1       1 
         431  POP_TOP          
         432  JUMP_ABSOLUTE       438  'to 438'
         435  JUMP_FORWARD          0  'to 438'
       438_0  COME_FROM                '435'
         438  LOAD_CONST            0  ''
         441  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 204

    def show_main_ui(self, ui_list):
        if ui_list:
            if isinstance(ui_list, (list, tuple)):
                for key in ui_list:
                    self._guide_ui.show_main_ui_by_type(key)

            else:
                self._guide_ui.show_main_ui_by_type(ui_list)

    def finish_guide--- This code section failed: ---

 417       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'unit_obj'
           6  LOAD_CONST            0  ''
           9  COMPARE_OP            8  'is'
          12  POP_JUMP_IF_FALSE    19  'to 19'

 418      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

 419      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             2  'guid_cfg'
          25  LOAD_FAST             1  'guide_id'
          28  CALL_FUNCTION_1       1 
          31  STORE_FAST            2  'cfg'

 421      34  LOAD_FAST             2  'cfg'
          37  LOAD_ATTR             3  'get'
          40  LOAD_CONST            1  'Prior'
          43  LOAD_CONST            0  ''
          46  CALL_FUNCTION_2       2 
          49  STORE_FAST            3  'prior'

 422      52  LOAD_FAST             3  'prior'
          55  POP_JUMP_IF_FALSE    95  'to 95'

 423      58  LOAD_FAST             0  'self'
          61  LOAD_ATTR             4  'destroy_steps'
          64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             2  'guid_cfg'
          70  LOAD_FAST             3  'prior'
          73  CALL_FUNCTION_1       1 
          76  LOAD_ATTR             3  'get'
          79  LOAD_CONST            2  'Next'
          82  LOAD_CONST            0  ''
          85  CALL_FUNCTION_2       2 
          88  CALL_FUNCTION_1       1 
          91  POP_TOP          
          92  JUMP_FORWARD         13  'to 108'

 425      95  LOAD_FAST             0  'self'
          98  LOAD_ATTR             5  'destroy_guide'
         101  LOAD_FAST             1  'guide_id'
         104  CALL_FUNCTION_1       1 
         107  POP_TOP          
       108_0  COME_FROM                '92'

 427     108  LOAD_FAST             0  'self'
         111  LOAD_ATTR             6  'propel_steps'
         114  LOAD_FAST             2  'cfg'
         117  LOAD_ATTR             3  'get'
         120  LOAD_CONST            2  'Next'
         123  LOAD_CONST            0  ''
         126  CALL_FUNCTION_2       2 
         129  LOAD_FAST             2  'cfg'
         132  LOAD_ATTR             3  'get'
         135  LOAD_CONST            3  'NextShowMainUI'
         138  LOAD_CONST            0  ''
         141  CALL_FUNCTION_2       2 
         144  CALL_FUNCTION_2       2 
         147  POP_TOP          

 429     148  LOAD_FAST             0  'self'
         151  LOAD_ATTR             7  'battle'
         154  POP_JUMP_IF_TRUE    161  'to 161'

 430     157  LOAD_CONST            0  ''
         160  RETURN_END_IF    
       161_0  COME_FROM                '154'

 431     161  LOAD_FAST             0  'self'
         164  LOAD_ATTR             7  'battle'
         167  LOAD_ATTR             8  'get_battle_tid'
         170  CALL_FUNCTION_0       0 
         173  STORE_FAST            4  'battle_type'

 432     176  LOAD_FAST             3  'prior'
         179  POP_JUMP_IF_FALSE   387  'to 387'

 433     182  LOAD_FAST             1  'guide_id'
         185  LOAD_FAST             0  'self'
         188  STORE_ATTR            9  '_cur_step'

 435     191  LOAD_FAST             1  'guide_id'
         194  LOAD_FAST             0  'self'
         197  LOAD_ATTR            10  'get_final_guide_id'
         200  CALL_FUNCTION_0       0 
         203  COMPARE_OP            2  '=='
         206  POP_JUMP_IF_FALSE   348  'to 348'

 437     209  LOAD_GLOBAL          11  'global_data'
         212  LOAD_ATTR            12  'player'
         215  LOAD_ATTR            13  'clear_local_battle_data'
         218  CALL_FUNCTION_0       0 
         221  POP_TOP          

 438     222  LOAD_GLOBAL          11  'global_data'
         225  LOAD_ATTR            12  'player'
         228  LOAD_ATTR            14  'clear_local_barrier'
         231  CALL_FUNCTION_0       0 
         234  POP_TOP          

 439     235  LOAD_GLOBAL          11  'global_data'
         238  LOAD_ATTR            12  'player'
         241  LOAD_ATTR            15  'local_battle'
         244  POP_JUMP_IF_FALSE   266  'to 266'

 440     247  LOAD_GLOBAL          11  'global_data'
         250  LOAD_ATTR            12  'player'
         253  LOAD_ATTR            15  'local_battle'
         256  LOAD_ATTR            16  'clear_barriers'
         259  CALL_FUNCTION_0       0 
         262  POP_TOP          
         263  JUMP_FORWARD          0  'to 266'
       266_0  COME_FROM                '263'

 441     266  LOAD_GLOBAL          17  'G_POS_CHANGE_MGR'
         269  POP_JUMP_IF_FALSE   294  'to 294'

 442     272  LOAD_FAST             0  'self'
         275  LOAD_ATTR             0  'unit_obj'
         278  LOAD_ATTR            18  'unregist_pos_change'
         281  LOAD_FAST             0  'self'
         284  LOAD_ATTR            19  '_check_pos'
         287  CALL_FUNCTION_1       1 
         290  POP_TOP          
         291  JUMP_FORWARD         22  'to 316'

 444     294  LOAD_FAST             0  'self'
         297  LOAD_ATTR             0  'unit_obj'
         300  LOAD_ATTR            20  'unregist_event'
         303  LOAD_CONST            4  'E_POSITION'
         306  LOAD_FAST             0  'self'
         309  LOAD_ATTR            19  '_check_pos'
         312  CALL_FUNCTION_2       2 
         315  POP_TOP          
       316_0  COME_FROM                '291'

 449     316  LOAD_FAST             0  'self'
         319  LOAD_ATTR            21  'guide_finish'
         322  LOAD_FAST             4  'battle_type'
         325  CALL_FUNCTION_1       1 
         328  POP_TOP          

 452     329  LOAD_GLOBAL          22  'Appsflyer'
         332  CALL_FUNCTION_0       0 
         335  LOAD_ATTR            23  'advert_track_event'
         338  LOAD_GLOBAL          24  'AF_TUTORIAL_COMPLETION'
         341  CALL_FUNCTION_1       1 
         344  POP_TOP          
         345  JUMP_ABSOLUTE       387  'to 387'

 454     348  LOAD_CONST            0  ''
         351  RETURN_VALUE     

 455     352  LOAD_GLOBAL          11  'global_data'
         355  LOAD_ATTR            12  'player'
         358  LOAD_ATTR            25  'save_local_battle_data'
         361  LOAD_CONST            5  '_lbs_step'
         364  LOAD_FAST             1  'guide_id'
         367  CALL_FUNCTION_2       2 
         370  POP_TOP          

 456     371  LOAD_GLOBAL          11  'global_data'
         374  LOAD_ATTR            12  'player'
         377  LOAD_ATTR            26  '_lbs_save_pos'
         380  CALL_FUNCTION_0       0 
         383  POP_TOP          
         384  JUMP_FORWARD          0  'to 387'
       387_0  COME_FROM                '384'
         387  LOAD_CONST            0  ''
         390  RETURN_VALUE     

Parse error at or near `LOAD_GLOBAL' instruction at offset 371

    def guide_finish(self, battle_type):
        if battle_type == game_mode_const.QTE_LOCAL_BATTLE_TYPE:
            from logic.comsys.login.CharacterCreatorUINew import CharacterCreatorUINew
            CharacterCreatorUINew(opt_from='guide_finish')
        elif global_data.player:
            global_data.player.quit_battle()
            assessment_tid = global_data.player.get_assessment_tid()
            global_data.player.call_server_method('finish_assessment_task', (assessment_tid,))

    def empty_guide_holder(self, guide_id, *args):
        self.finish_guide(guide_id)

    def empty_guide_holder_destroy(self, *args):
        pass

    def show_human_tips(self, guide_id, mobile_text_id, pc_text_id, time_out, propel_ids=None):
        cfg = self.guid_cfg(guide_id)
        text_id = pc_text_id if global_data.is_pc_mode else mobile_text_id
        if cfg.get('Next', None):
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out, lambda step=guide_id: self.finish_guide(step))
        elif propel_ids:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out, --- This code section failed: ---

 485       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'propel_steps'
           6  LOAD_ATTR             1  'True'
           9  LOAD_GLOBAL           1  'True'
          12  CALL_FUNCTION_257   257 
          15  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_257' instruction at offset 12
)
        else:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
        return

    def show_human_tips_destroy(self, *_):
        self._guide_ui.show_human_tips_destroy()

    def show_human_tips_pc(self, guide_id, text_id, time_out, hot_key_func_code=None, propel_ids=None):
        cfg = self.guid_cfg(guide_id)
        if cfg.get('Next', None):
            self._guide_ui.show_human_tips_pc(get_text_local_content(text_id), time_out, hot_key_func_code, lambda step=guide_id: self.finish_guide(step))
        elif propel_ids:
            self._guide_ui.show_human_tips_pc(get_text_local_content(text_id), time_out, hot_key_func_code, --- This code section failed: ---

 497       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'propel_steps'
           6  LOAD_ATTR             1  'True'
           9  LOAD_GLOBAL           1  'True'
          12  CALL_FUNCTION_257   257 
          15  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_257' instruction at offset 12
)
        else:
            self._guide_ui.show_human_tips_pc(get_text_local_content(text_id), time_out, hot_key_func_code)
        return

    def show_human_tips_pc_destroy(self, *args):
        self._guide_ui.show_human_tips_destroy()

    def show_multi_human_tips(self, guide_id, text_id_list, time_out, propel_ids=None):
        text_list = [ get_text_local_content(text_id) for text_id in text_id_list ]
        self._guide_ui.show_multi_human_tips(text_list, time_out)

    def show_multi_human_tips_destroy(self, *args):
        self._guide_ui.show_multi_human_tips_destroy()

    def show_multi_human_tips_pc(self, guide_id, text_id_list, time_out, hot_key_func_code_list):
        self._guide_ui.show_multi_human_tips_pc(text_id_list, time_out, hot_key_func_code_list)

    def show_multi_human_tips_pc_destroy(self, *args):
        self._guide_ui.show_multi_human_tips_pc_destroy()

    def show_temp_tips(self, guide_id, text_id, time_out, propel_ids=None):
        self._guide_ui.show_temp_tips(text_id, time_out)
        return
        cfg = self.guid_cfg(guide_id)
        if cfg.get('Next', None):
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out, lambda step=guide_id: self.finish_guide(step))
        elif propel_ids:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out, --- This code section failed: ---

 525       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'propel_steps'
           6  LOAD_ATTR             1  'True'
           9  LOAD_GLOBAL           1  'True'
          12  CALL_FUNCTION_257   257 
          15  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_257' instruction at offset 12
)
        else:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
        return

    def show_temp_tips_destroy(self, *args):
        self._guide_ui.show_temp_tips_destroy()

    def show_temp_tips_pc(self, guide_id, text_id, time_out, hot_key_func_code=None):
        self._guide_ui.show_temp_tips_pc(text_id, time_out, hot_key_func_code)

    def show_temp_tips_pc_destroy(self, *args):
        self._guide_ui.show_temp_tips_destroy()

    def show_drag_layer(self, guide_id, layer, animation_name=None):
        self._guide_ui.show_drag_layer(layer, animation_name)

    def show_drag_layer_destroy(self, guide_id, layer, animation_name=None):
        self._guide_ui.show_drag_layer_destroy(layer, animation_name)

    def mecha_progress(self, *_):
        self.init_mecha_progress(True)

    def show_nd_animation(self, guide_id, layer, animation):
        if layer == 'nd_step_2' and not global_data.is_pc_mode:
            self._guide_ui.panel.nd_cannot_move.setVisible(False)
        self._guide_ui.play_nd_animation(layer, animation)

    def show_nd_animation_destroy(self, guide_id, layer, animation):
        self._guide_ui.play_nd_animation_destroy(layer, animation)

    def check_cur_weapon(self, guide_id, weapon_id):
        weapon = self.sd.ref_wp_bar_cur_weapon
        if weapon and weapon.get_item_id() == weapon_id:
            params = get_handler_params('guide_switch_show')
            self.finish_guide(params)

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

    def show_locate_and_sfx(self, guide_id, position):
        self._locate_sfx_delay_call = None
        self.show_sfx(guide_id, position, 'effect/fx/guide/guide_end.sfx')
        self.show_locate(guide_id, position, 2, 'temp_locate', 'keep')
        if global_data.player.local_npc_mecha_driver and global_data.player.local_npc_mecha_driver[0] and global_data.player.local_npc_mecha_driver[0].logic:
            global_data.player.local_npc_mecha_driver[0].logic.send_event('E_MOVE_ROCK', math3d.vector(0, 0, 0), False)
        return

    def remove_locate_and_sfx(self, guide_id):
        if guide_id in self._sfx_map:
            global_data.sfx_mgr.remove_sfx(self._sfx_map[guide_id])
            del self._sfx_map[guide_id]
        self._guide_ui.show_locate_destroy('temp_locate', 'keep')

    def stop_locate_sfx_delay_call(self):
        if self._locate_sfx_delay_call:
            delay.cancel(self._locate_sfx_delay_call)
            self._locate_sfx_delay_call = None
        return

    def delay_show_locate_and_sfx(self, guide_id, position, delay_time=2):
        self._locate_sfx_delay_call = delay.call(delay_time, lambda : self.show_locate_and_sfx(guide_id, position))

    def delay_show_locate_and_sfx_destroy(self, guide_id, *args):
        self.remove_locate_and_sfx(guide_id)

    def _check_mov(self, guide_id, pos, offset):
        m_pos = global_data.player.logic.ev_g_position()
        dist = math3d.vector(*pos) - m_pos
        if dist.length < offset * NEOX_UNIT_SCALE:
            self.finish_guide(guide_id)

    def check_move_pos(self, guide_id, pos, offset):
        self._move_timer = global_data.game_mgr.register_logic_timer(lambda : self._check_mov(guide_id, pos, offset), interval=0.1, mode=CLOCK)

    def check_move_pos_destroy(self, *_):
        if self._move_timer:
            global_data.game_mgr.unregister_logic_timer(self._move_timer)
            self._move_timer = None
        return

    def pick_up_weapon(self, guide_id, weapon_id):
        self._add_weapon(weapon_id)

    def pick_up_weapon_destroy(self, *_):
        pass

    def pick_up_weapons(self, guide_id, weapon_dict):
        for weapon_pos, weapon_id in six.iteritems(weapon_dict):
            iMagSize = confmgr.get('firearm_config', str(weapon_id))['iMagSize']
            item_data = {'item_id': weapon_id,'entity_id': IdManager.genid(),'count': 1,'iBulletNum': iMagSize}
            self.send_event('E_PICK_UP_WEAPON', item_data, weapon_pos, False)

        self.send_event('E_SWITCHING', const.PART_WEAPON_POS_MAIN_DF)

    def pick_up_weapons_destroy(self, *args):
        pass

    def get_other_items(self, guide_id, item_dict_list):
        for item_dict in item_dict_list:
            init_item_dict = {'item_id': item_dict.get('item_id'),
               'entity_id': IdManager.genid(),
               'count': item_dict.get('count')
               }
            global_data.player._lbs_send_event('E_PICK_UP_OTHERS', init_item_dict)

    def get_other_items_destroy(self, *args):
        pass

    def guide_robot_dead(self, guide_id, interval):
        if interval > 0:
            self._delay_call = delay.call(interval, lambda g=guide_id: self.finish_guide(guide_id))
        else:
            self.finish_guide(guide_id)

    def guide_npc_mecha_dead(self, guide_id, interval, is_driver):
        if is_driver:
            self.finish_guide(guide_id)
        else:
            cfg = self.guid_cfg(guide_id)
            self.propel_steps(cfg.get('Next', None), cfg.get('NextShowMainUI', None))
        return

    def guide_shoot_show(self, is_show):
        if is_show:
            self.show_nd_animation(None, 'nd_step_3', 'show_3')
            self.update_auto_frame()
            self.show_nd_animation(None, 'nd_auto_frame', 'show_auto')
        else:
            self.show_nd_animation_destroy(None, 'nd_step_3', 'show_3')
            self.show_nd_animation_destroy(None, 'nd_auto_frame', 'show_auto')
        return

    def update_auto_frame(self):
        weapon = self.sd.ref_wp_bar_cur_weapon
        aim_args = self.ev_g_at_aim_args_all()
        self._guide_ui.update_auto_frame(weapon, aim_args)

    def guide_pick_show(self, opt):
        if opt == 0:
            self.show_nd_animation_destroy(None, 'nd_step_5', 'show_5')
            self.show_nd_animation_destroy(None, 'nd_step_5_1', 'show_5_1')
            self._guide_ui.deal_human_tips(None)
        elif self._guide_ui.panel.temp_human_tips.isVisible():
            if opt == 1:
                self._guide_ui.deal_human_tips(['nd_step_5', 'show_5'])
            elif opt == 2:
                self._guide_ui.deal_human_tips(['nd_step_5_1', 'show_5_1'])
        elif opt == 1:
            self.show_nd_animation(None, 'nd_step_5', 'show_5')
            self.show_nd_animation_destroy(None, 'nd_step_5_1', 'show_5_1')
        elif opt == 2:
            self.show_nd_animation_destroy(None, 'nd_step_5', 'show_5')
            self.show_nd_animation(None, 'nd_step_5_1', 'show_5_1')
        return

    def guide_switch_end(self, *args, **kwargs):
        params = get_handler_params('guide_switch_show')
        self.finish_guide(params)
        self.enable_human_fire(True)

    def guide_switch_end_by_guide_id(self, *args, **kwargs):
        if self._cur_switch_gun_step is not None:
            self.finish_guide(self._cur_switch_gun_step)
            self._cur_switch_gun_step = None
        return

    def guide_pick_weapon(self, guide_id, weapon_id):
        if str(weapon_id) == '10232':
            self.finish_guide(guide_id)
        if str(weapon_id) in ('10523', '10534'):
            self.finish_guide(guide_id)

    def guide_pick_other_item(self, guide_id, item_id):
        if item_id == 99112:
            global_data.player.logic.send_event('E_MECHA_INSTALL_MODULE_RESULT', True, 4, 1010, 99112)
            mecha = global_data.player.logic.ev_g_control_target()
            if mecha and mecha.logic:
                mecha.logic.send_event('E_PICK_UP_WEAPON', {'item_id': 800103,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}, 2, False)
            self.finish_guide(guide_id)

    def guide_pick_specific_items(self, guide_id):
        self.finish_guide(guide_id)

    def send_firefox_core_module(self, guide_id, module_id):
        other_item_data = {'item_id': module_id,
           'entity_id': IdManager.genid(),
           'count': 1
           }
        global_data.player._lbs_send_event('E_PICK_UP_OTHERS', other_item_data)

    def send_firefox_core_module_destroy(self, *args):
        pass

    def active_firefox_core_module(self, guide_id, *args):
        global_data.player.logic.send_event('E_MECHA_INSTALL_MODULE_RESULT', True, 4, 1010, 99112)
        mecha = global_data.player.logic.ev_g_control_target()
        if mecha and mecha.logic:
            mecha.logic.send_event('E_PICK_UP_WEAPON', {'item_id': 800103,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}, 2, False)
            self.show_get_module_anim(4, 1010, 4)

    def active_firefox_core_module_destroy(self, *args):
        pass

    def guide_try_aim_success(self, *_):
        params = get_handler_params('guide_try_aim_success')
        self.destroy_steps(params[0], force=True)
        self.propel_steps(params[1], force=True)
        global_data.player._lbs_pause_robot()

    def guide_quit_aim_success(self, *_):
        params = get_handler_params('guide_quit_aim_success')
        self.propel_steps(params[0], force=True)
        self.destroy_steps(params[1], force=True)
        global_data.player._lbs_resume_robot()

    def guide_use_end(self, *_):
        params = get_handler_params('guide_use_end')
        self.finish_guide(params)

    def guide_charger_end(self, *_):
        params = get_handler_params('guide_charger_end')
        self.finish_guide(params)

    def check_mecha_charger(self, *_):
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui and ui.can_mecha_call():
            params = get_handler_params('guide_charger_end')
            self.finish_guide(params)

    def guide_mecha_ui_show(self, ui):
        self.show_nd_animation_destroy(None, 'nd_step_13', 'show_13')
        self.unit_obj.regist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)
        return

    def guide_mecha_ui_final(self, *_):
        self.unit_obj.unregist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)
        self.show_nd_animation(None, 'nd_step_13', 'show_13')
        return

    def guide_charger(self, *_):
        params = get_handler_params('guide_charger')
        self.finish_guide(params)
        self.show_human_tips(params, 5011, 5011, 3)

    def guide_call_mecha_end(self, *_):
        self.unit_obj.unregist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)
        if not self.battle:
            return
        battle_type = self.battle.get_battle_tid()
        if battle_type == NEWBIE_STAGE_MECHA_BATTLE:
            if self._cur_step == 100:
                self.finish_guide(204)
            elif self._cur_step == 703:
                self.finish_guide(802)
        ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if ui:
            ui.panel.setVisible(False)

    def guide_leave_mecha_end(self, *args):
        self._guide_ui.hide_leave_mecha_tips()
        if global_data.player and global_data.player.logic:
            cur_wp_pos = global_data.player.logic.share_data.ref_wp_bar_cur_pos
            new_wp_pos = const.PART_WEAPON_POS_MAIN_DF
            if cur_wp_pos == const.PART_WEAPON_POS_MAIN_DF:
                new_wp_pos = const.PART_WEAPON_POS_MAIN1
            self.send_event('E_SWITCHING', cur_wp_pos)

    def on_leave_mecha(self, *args):
        if global_data.player and global_data.player.logic:
            cur_wp_pos = global_data.player.logic.share_data.ref_wp_bar_cur_pos
            self.send_event('E_SWITCHING', cur_wp_pos)

    def mecha_progress_destroy(self, *_):
        pass

    def create_robot(self, guide_id, interval, pos, max_hp, shoot=False):
        global_data.player._lbs_create_robot(guide_id, interval, pos, max_hp, shoot)

    def create_robot_destroy(self, *_):
        global_data.player._lbs_destroy_robot()

    def create_robot_move(self, guide_id, interval, pos_from, next_pos_list, max_hp, shoot=False):
        global_data.player._lbs_create_robot(guide_id, interval, pos_from, max_hp, shoot)
        global_data.player._lbs_move_robot_to(next_pos_list)
        driver = global_data.player.local_robot[0]
        if driver and driver.logic:
            self._eagle_flag_delay_call = delay.call(1, lambda : self.show_eagle_flag(driver))

    def show_eagle_flag(self, driver):
        self._eagle_flag_delay_call = None
        driver.logic.send_event('E_ADD_EAGLE_FLAG', driver.id, 'gift', False)
        return

    def stop_eagle_flag_delay_call(self):
        if self._eagle_flag_delay_call:
            delay.cancel(self._eagle_flag_delay_call)
            self._eagle_flag_delay_call = None
        return

    def create_robot_move_destroy(self, *args):
        global_data.player._lbs_destroy_robot()

    def create_robot_aim(self, guide_id, interval, pos, max_hp):
        global_data.player._lbs_create_robot(guide_id, interval, pos, max_hp, True)

    def create_robot_aim_destroy(self, *_):
        global_data.player._lbs_destroy_robot()

    def create_robot_fire(self, guide_id, interval, pos, max_hp):
        global_data.player._lbs_create_monster(guide_id, interval, pos, max_hp, False)
        global_data.player.local_robot_shoot_num = 5
        global_data.player._lbs_resume_robot_delay()

    def create_robot_fire_destroy(self, *_):
        global_data.player._lbs_destroy_robot()

    def create_robot_skill(self, guide_id, interval, pos, max_hp):
        global_data.player._lbs_create_monster(guide_id, interval, pos, max_hp, False)
        global_data.player.local_robot_shoot_num = 5
        global_data.player.local_robot_skill_hurt = 0
        self.create_robot_skill_param = [guide_id, interval, pos, max_hp]
        global_data.player._lbs_resume_robot_delay()

    def create_robot_skill_destroy(self, *_):
        global_data.player._lbs_destroy_robot()

    def create_robot_mecha(self, guide_id, interval, pos, max_hp, shoot=False):
        global_data.player._lbs_create_robot_mecha(guide_id, interval, pos, max_hp, shoot)

    def create_robot_mecha_destroy(self, *args):
        global_data.player._lbs_destroy_robot()

    def guide_robot_dead_skill(self, guide_id, interval):
        if global_data.player.local_robot_skill_hurt > 0:
            if interval > 0:
                self._delay_call = delay.call(interval, lambda g=guide_id: self.finish_guide(guide_id))
            else:
                self.finish_guide(guide_id)
        else:
            param = self.create_robot_skill_param
            self.create_robot_skill(*param)

    def create_pick_item(self, guide_id, item_no, pos, sub_items):
        global_data.player._lbs_create_pick_item(guide_id, item_no, pos, sub_items)

    def create_pick_item_destroy(self, *_):
        global_data.player._lbs_destroy_item()
        self._guide_ui.deal_human_tips(None)
        return

    def create_items(self, guide_id, item_list):
        global_data.player._lbs_create_items(guide_id, item_list)

    def create_items_destroy(self, *args):
        pass

    def mecha_charger(self, guide_id, npc_id, pos):
        self._mecha_charger = global_data.player._lbs_create_mecha_charger(npc_id, pos)

    def mecha_charger_destroy(self, *_):
        if self._mecha_charger:
            global_data.player.local_battle.destroy_entity(self._mecha_charger.id)
            self._mecha_charger = None
        return

    def guide_quit_aim(self, *_):
        self.send_event('E_QUIT_AIM')

    def guide_close_weapon_choose(self, *args):
        if self._cur_step == 100:
            self.finish_guide(104)

    def enable_human_fire(self, enable, callback=None):
        pass

    def enable_human_fire_destroy(self, *args):
        pass

    def mecha_recovery(self, *_):
        mecha = self.ev_g_bind_mecha_entity()
        if mecha:
            mecha.logic.send_event('E_SET_SHIELD', mecha.logic.ev_g_max_shield())
            mecha.logic.send_event('S_HP', mecha.logic.ev_g_max_hp())

    def destroy_battle_guide(self):
        self.unblock_pc_hot_keys()
        if self._regist_throw_explosion_event_flag:
            global_data.emgr.scene_throw_item_explosion_event -= global_data.player._lbs_update_explosive_item_info
            self._regist_throw_explosion_event_flag = False
        if not self._cur_step:
            return
        else:
            cfg = self.guid_cfg(self._cur_step)
            self._cur_step = None
            self.destroy_steps(cfg.get('Next', None))
            global_data.player._lbs_destroy_mecha()
            global_data.ui_mgr.close_ui('GuideUI')
            global_data.ui_mgr.close_ui('LeaveGuideUI')
            global_data.ui_mgr.close_ui('MechaControlMain')
            self.unit_obj.unregist_event('E_GUIDE_OPEN_MAIN_SETTING', self.guide_open_main_setting)
            self.unit_obj.unregist_event('E_GUIDE_CLOSE_MAIN_SETTING', self.guide_close_main_setting)
            self.unit_obj.unregist_event('E_GUIDE_MECHA_UI_FINAL', self.guide_mecha_ui_final)
            if G_POS_CHANGE_MGR:
                self.unit_obj.unregist_pos_change(self._check_pos)
            else:
                self.unit_obj.unregist_event('E_POSITION', self._check_pos)
            global_data.emgr.auto_aim_pos_update -= self.update_auto_aim
            self._sfx_map = {}
            self._move_timer = None
            self._mecha_charger = None
            self._cur_step = None
            self._delay_call = None
            self.stop_locate_sfx_delay_call()
            self.stop_eagle_flag_delay_call()
            self.create_robot_skill_param = None
            self._construct_flag = False
            return

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

    def create_end_ui(self, guide_id, *args):
        from logic.comsys.guide_ui.NewbieStageEndUI import NewbieStageEndUI

        def end_ui_cb():
            self.finish_guide(guide_id)

        NewbieStageEndUI(None, end_ui_cb)
        return

    def create_end_ui_destroy(self, *args):
        pass

    def create_common_ui(self, guide_id, ui_dict):
        ui_name = ui_dict.get('ui_name', '')
        ui_path = ui_dict.get('ui_path', '')
        if not ui_name or not ui_path:
            return
        ui = global_data.ui_mgr.show_ui(ui_name, ui_path)
        ui and ui.show()

    def create_common_ui_destroy(self, *args):
        pass

    def show_death_rule_tips(self, guide_id, text_id, time_out):
        self._guide_ui.show_death_rule_tips(text_id, time_out)

    def show_death_rule_tips_destroy(self, *args):
        pass

    def create_death_door_col(self, *args):
        if not self.battle:
            return
        battle_type = self.battle.get_battle_tid()
        door_init_data = GetDoorConfig().get(int(battle_type), {}).get('door_init_data', [])
        if not door_init_data:
            return
        from logic.comsys.battle.Death.DeathBattleDoorCol import DeathBattleDoorCol
        DeathBattleDoorCol()
        for door_dict in door_init_data:
            global_data.player._lbs_add_entity('DeathDoor', door_dict)

        from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
        DeathBattleData()
        group_born_dict = GetDoorConfig().get(int(battle_type), {}).get('group_born_data', {})
        born_point_list = []
        global_data.death_battle_data.set_area_id('1')
        global_data.death_battle_data.update_born_point(group_born_dict, born_point_list)

    def create_death_door_col_destroy(self, *args):
        pass

    def trigger_death_door(self, *args):
        global_data.death_battle_door_col.set_col_trigger()

    def trigger_death_door_destroy(self, *args):
        pass

    def create_robot_mecha_by_type(self, guide_id, interval, mecha_dict):
        global_data.player._lbs_create_robot_mecha_by_type(guide_id, interval, mecha_dict)

    def create_robot_mecha_by_type_destroy(self, *args):
        pass

    def create_npc_mecha_by_type(self, guide_id, interval, mecha_dict):
        global_data.player._lbs_create_npc_mecha_by_type(guide_id, interval, mecha_dict)

    def create_npc_mecha_by_type_destroy(self, *args):
        global_data.player._lbs_destroy_npc_mecha()

    def turn_dir_by_target_pos(self, guide_id, pos):
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

    def process_auto_pick(self, guide_id, enable):
        global_data.emgr.player_enable_auto_pick_event.emit(enable)

    def process_auto_pick_destroy(self, *args):
        pass

    def guide_wait_handler(self, guide_id, wait_time):
        self._guide_ui.show_empty_tips(wait_time, lambda : self.finish_guide(guide_id))

    def guide_wait_handler_destroy(self, *args):
        pass

    def set_death_top_score(self, guide_id, score):
        ui = global_data.ui_mgr.get_ui('DeathTopScoreUI')
        ui and ui.set_my_group_score(score)

    def set_death_top_score_destroy(self, *args):
        pass

    def show_robot_flag_ui(self, guide_id, *args):
        driver = global_data.player.get_available_npc_human()
        if driver and driver.logic:
            driver.logic.send_event('E_ADD_EAGLE_FLAG', driver.id, 'gift', False)

    def show_robot_flag_ui_destroy(self, *args):
        driver = global_data.player.get_available_npc_human()
        if driver and driver.logic:
            driver.logic.send_event('E_DEL_EAGLE_FLAG', driver.id, False)

    def guide_robot_stop_move(self, *args):
        pos = global_data.player.get_local_robot_position()
        if not pos:
            return
        path = 'effect/fx/guide/guide_end.sfx'
        self._robot_stop_move_sfx = global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*pos))

    def guide_npc_mecha_driver_on_ground(self, *args):
        pos = global_data.player.get_local_npc_mecha_driver_position()
        if not pos:
            return
        path = 'effect/fx/guide/guide_end.sfx'
        self._robot_on_ground_sfx = global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*pos))

    def set_no_mecha_damage(self, guide_id, flag):
        global_data.player and global_data.player.set_no_mecha_damage_flag(flag)

    def set_no_mecha_damage_destroy(self, *args):
        pass

    def set_state_change_ui_visible_flag(self, guide_id, visible_to_human, visible_to_mecha):
        self._visible_to_human = visible_to_human
        self._visible_to_mecha = visible_to_mecha

    def get_state_change_ui_visible_flag(self):
        return (
         self._visible_to_human, self._visible_to_mecha)

    def set_state_change_ui_visible_flag_destroy(self, *args):
        pass

    def set_state_change_ui_visible(self, guide_id, visible_to_human, visible_to_mecha):
        ui = global_data.ui_mgr.get_ui('StateChangeUI')
        if ui:
            ui.set_change_state_btn_visible(visible_to_human, visible_to_mecha)

    def set_state_change_ui_visible_destroy(self, *args):
        pass

    def set_mecha_button_visible(self, guide_id, action_id, visible, delay_time=0):
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if ui:
            ui.on_set_action_visible(action_id, visible, True)

    def set_mecha_button_visible_destroy(self, *args):
        pass

    def show_get_module_anim(self, slot_pos, card_id, lv):
        from logic.comsys.mecha_ui.MechaModuleGroupWidget import make_msg
        from logic.gcommon.common_const.battle_const import MED_R_NODE_COMMON_INFO
        ui = global_data.ui_mgr.get_ui('BattleMedRCommonInfo')
        if not ui:
            return
        ui.clear_show_count_dict()
        ui._show_count_dict = {'ON_PLAYING': -1,'BattleInfoMessageVisibleUI': 0,'BattleMedRCommonInfo': -1}
        message = make_msg(slot_pos, card_id, lv)
        global_data.emgr.show_battle_med_r_message.emit(message, MED_R_NODE_COMMON_INFO)

    def show_get_module_anim_destroy(self, *args):
        pass

    def show_use_drug_tip(self, guide_id, text_id, time_out, hot_key_func_code=None):
        self._guide_ui.show_temp_use_tips(text_id, time_out, hot_key_func_code)

    def show_use_drug_tip_destroy(self, *args):
        self._guide_ui.hide_temp_use_tips()

    def process_throw_item_explosion_event(self):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        part_throwable_mgr = scene.get_com('PartThrowableManager')
        if not part_throwable_mgr:
            return
        global_data.emgr.scene_throw_item_explosion_event -= part_throwable_mgr.throw_item_explosion
        global_data.emgr.scene_throw_item_explosion_event += global_data.player._lbs_update_explosive_item_info
        global_data.emgr.scene_throw_item_explosion_event += part_throwable_mgr.throw_item_explosion
        self._regist_throw_explosion_event_flag = True

    def process_bgm_event(self):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        part = scene.get_com('PartBgSound')
        if not part:
            return
        part.exit_battle_event()

    def show_side_tip_ui(self, guide_id, visible, text_id):
        self.side_tip_ui.set_tip_visible(visible)
        self.side_tip_ui.set_tip_content(text_id)

    def show_side_tip_ui_destroy(self, *args):
        self.side_tip_ui.set_tip_visible(False)

    def remove_locate_ui(self, guide_id, *args):
        self._guide_ui.show_locate_destroy('temp_locate', 'keep')

    def remove_locate_ui_destroy(self, *args):
        pass

    def set_robot_eject_flag(self, guide_id, eject_flag):
        global_data.player.need_eject_driver = eject_flag

    def set_robot_eject_flag_destroy(self, *args):
        pass

    def do_nothing_guide(self, *args):
        pass

    def do_nothing_guide_destroy(self, *args):
        pass

    def show_select_weapon_tip_pc(self, guide_id, text_id, hot_key_func_code):
        self._guide_ui.show_select_weapon_tip(text_id, hot_key_func_code)

    def show_select_weapon_tip_pc_destroy(self, *args):
        self._guide_ui.hide_select_weapon_tip()

    def show_summon_mecha_tip_pc(self, guide_id, text_id, hot_key_func_code=None):
        self._guide_ui.show_summon_mecha_tip(text_id, hot_key_func_code)

    def show_summon_mecha_tip_pc_destroy(self, *args):
        self._guide_ui.hide_summon_mecha_tip()

    def show_get_off_mecha_tip_pc(self, guide_id, text_id, hot_key_func_code):
        self._guide_ui.show_get_off_mecha_tip(text_id, hot_key_func_code)

    def show_get_off_mecha_tip_pc_destroy(self, *args):
        self._guide_ui.hide_get_off_mecha_tip()

    def show_move_skill_tip_pc(self, guide_id, text_id, hot_key_func_code):
        self._guide_ui.show_move_skill_tip(text_id, hot_key_func_code)

    def show_move_skill_tip_pc_destroy(self, *args):
        self._guide_ui.hide_move_skill_tip()

    def block_pc_hot_key(self, guide_id, hot_key_list, is_block):
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        for hot_key in hot_key_list:
            if is_block:
                PCCtrlManager().block_hotkey(hot_key, 'local_battle_guide')
            else:
                PCCtrlManager().unblock_hotkey(hot_key, 'local_battle_guide')

    def block_pc_hot_key_destroy(self, *args):
        pass

    def register_mecha_dash_event(self, mecha_eid):
        if not mecha_eid:
            cur_mecha_eid = self.unit_obj.ev_g_ctrl_mecha() if 1 else mecha_eid
            return cur_mecha_eid or None
        mecha_obj = EntityManager.getentity(cur_mecha_eid)
        if not mecha_obj or not mecha_obj.logic:
            return
        if self._regist_mecha_dash_event_flag:
            return
        mecha_obj.logic.regist_event('E_DO_SKILL', self.hide_tip_after_dash)

    def hide_tip_after_dash(self, skill_id, *args):
        if skill_id != 800152:
            return
        self._guide_ui.play_nd_animation_destroy('nd_move_skill', 'move_skill')
        mecha_eid = self.unit_obj.ev_g_ctrl_mecha()
        if not mecha_eid:
            return
        mecha_obj = EntityManager.getentity(mecha_eid)
        if not mecha_obj or not mecha_obj.logic:
            return
        if not self._regist_mecha_dash_event_flag:
            return
        self._regist_mecha_dash_event_flag = False
        mecha_obj.logic.unregist_event('E_DO_SKILL', self.hide_tip_after_dash)

    def on_guide_robot_mecha_lower_hp(self):
        if self._has_robot_mecha_lower_hp:
            return
        self._has_robot_mecha_lower_hp = True
        weapon_id = GetStageHumanHandler().get('robot_mecha_lower_hp_weapon_id', {}).get('handler_params', 10544)
        self._add_weapon(weapon_id)
        tip_param = GetStageHumanHandler().get('robot_mecha_lower_hp_tip_param', {}).get('handler_params', {})
        if global_data.is_pc_mode:
            layer = tip_param.get('pc')[0]
            animation = tip_param.get('pc')[1]
        else:
            layer = tip_param.get('mobile')[0]
            animation = tip_param.get('mobile')[1]
        self._guide_ui.play_nd_animation(layer, animation)
        self._guide_ui.show_human_tips(get_text_local_content(5704), 5)

    def on_guide_try_switch(self, weapon_pos, *args, **kwargs):
        if weapon_pos != PART_WEAPON_POS_MAIN2:
            return
        tip_param = GetStageHumanHandler().get('robot_mecha_lower_hp_tip_param', {}).get('handler_params', {})
        if global_data.is_pc_mode:
            layer = tip_param.get('pc')[0]
            animation = tip_param.get('pc')[1]
        else:
            layer = tip_param.get('mobile')[0]
            animation = tip_param.get('mobile')[1]
        self._guide_ui.play_nd_animation_destroy(layer, animation)

    def hide_switch_gun_tip(self, *args):
        pass

    def hide_switch_gun_tip_destroy(self, guide_id, layer, animation):
        self._guide_ui.play_nd_animation_destroy(layer, animation)
        self._guide_ui.show_human_tips_destroy()

    def destroy(self):
        self.destroy_battle_guide()
        super(ComLocalBattleGuide, self).destroy()