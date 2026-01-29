# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSpecialBattleGuide.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.comsys.guide_ui.GuideUI import GuideUI
from logic.client.const import game_mode_const
from data.c_guide_data import GetSpecialGuide, get_special_guide_params
from logic.gcommon import time_utility as tutil
from common.utils.timer import CLOCK

class ComSpecialBattleGuide(UnitCom):
    BIND_EVENT = {'E_DESTROY_REMOTE_GUIDE': 'destroy_special_guide',
       'E_DEATH': 'destroy_special_guide'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpecialBattleGuide, self).init_from_dict(unit_obj, bdict)
        self._special_double_click_timer = None
        return

    @property
    def _guide_ui(self):
        return GuideUI()

    def on_init_complete--- This code section failed: ---

  27       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            2  'player'

  28       9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             2  'can_init_guild'
          15  LOAD_FAST             2  'player'
          18  CALL_FUNCTION_1       1 
          21  POP_JUMP_IF_TRUE     28  'to 28'

  29      24  LOAD_CONST            0  ''
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

  31      28  LOAD_GLOBAL           3  'GetSpecialGuide'
          31  CALL_FUNCTION_0       0 
          34  STORE_FAST            3  'info'

  32      37  SETUP_LOOP           54  'to 94'
          40  LOAD_FAST             3  'info'
          43  GET_ITER         
          44  FOR_ITER             46  'to 93'
          47  STORE_FAST            4  'handler_name'

  33      50  LOAD_GLOBAL           4  'getattr'
          53  LOAD_GLOBAL           1  'player'
          56  LOAD_ATTR             5  'format'
          59  LOAD_FAST             4  'handler_name'
          62  CALL_FUNCTION_1       1 
          65  CALL_FUNCTION_2       2 
          68  STORE_FAST            5  'func'

  34      71  LOAD_FAST             5  'func'
          74  POP_JUMP_IF_FALSE    44  'to 44'

  35      77  LOAD_FAST             5  'func'
          80  LOAD_FAST             2  'player'
          83  CALL_FUNCTION_1       1 
          86  POP_TOP          
          87  JUMP_BACK            44  'to 44'
          90  JUMP_BACK            44  'to 44'
          93  POP_BLOCK        
        94_0  COME_FROM                '37'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 65

    def can_init_guild(self, player):
        if global_data.is_pc_mode:
            return False
        if player.in_local_battle():
            return False
        if player.is_in_global_spectate():
            return False
        if self.ev_g_is_outsider():
            return False
        if self.ev_g_is_in_spectate():
            return False
        return True

    def init_special_call_mecha(self, player):
        key = 'special_call_mecha'
        flag = player.read_guide_data(key)
        if flag:
            return
        check_key = 'remote_guide_mecha'
        check_flag = player.read_guide_data(check_key)
        if not check_flag:
            return
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            self.unit_obj.regist_event('E_GUIDE_CHARGER_END', self.special_call_mecha)

    def special_call_mecha(self, *args):
        guide = 'special_call_mecha'
        global_data.player.write_guide_data(guide, 1)
        self.unit_obj.unregist_event('E_GUIDE_CHARGER_END', self.special_call_mecha)
        param = get_special_guide_params(guide)
        self._guide_ui.show_special_call_mecha(*param)

    def init_special_double_click(self, player):
        key = 'special_double_click'
        flag = player.read_guide_data(key)
        if flag:
            return
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            self.unit_obj.regist_event('E_SEND_BATTLE_GROUP_MSG', self.special_double_click)

    def special_double_click(self, *args):
        self.unit_obj.unregist_event('E_SEND_BATTLE_GROUP_MSG', self.special_double_click)

        def _check_big_map_closed():
            ui = global_data.ui_mgr.get_ui('BigMapUI')
            if not ui:
                return True

        def _tick--- This code section failed: ---

  95       0  LOAD_DEREF            0  '_check_big_map_closed'
           3  CALL_FUNCTION_0       0 
           6  POP_JUMP_IF_FALSE    90  'to 90'

  96       9  LOAD_CONST            1  'special_double_click'
          12  STORE_FAST            0  'guide'

  97      15  LOAD_GLOBAL           0  'global_data'
          18  LOAD_ATTR             1  'player'
          21  LOAD_ATTR             2  'write_guide_data'
          24  LOAD_ATTR             2  'write_guide_data'
          27  CALL_FUNCTION_2       2 
          30  POP_TOP          

  98      31  LOAD_GLOBAL           3  'get_special_guide_params'
          34  LOAD_FAST             0  'guide'
          37  CALL_FUNCTION_1       1 
          40  STORE_FAST            1  'param'

  99      43  LOAD_DEREF            1  'self'
          46  LOAD_ATTR             4  '_guide_ui'
          49  LOAD_ATTR             5  'show_special_double_click'
          52  LOAD_FAST             1  'param'
          55  CALL_FUNCTION_VAR_0     0 
          58  POP_TOP          

 100      59  LOAD_GLOBAL           0  'global_data'
          62  LOAD_ATTR             6  'game_mgr'
          65  LOAD_ATTR             7  'unregister_logic_timer'
          68  LOAD_DEREF            1  'self'
          71  LOAD_ATTR             8  '_special_double_click_timer'
          74  CALL_FUNCTION_1       1 
          77  POP_TOP          

 101      78  LOAD_CONST            0  ''
          81  LOAD_DEREF            1  'self'
          84  STORE_ATTR            8  '_special_double_click_timer'
          87  JUMP_FORWARD          4  'to 94'

 103      90  LOAD_CONST            0  ''
          93  RETURN_VALUE     
        94_0  COME_FROM                '87'
          94  LOAD_CONST            0  ''
          97  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 27

        self._special_double_click_timer = global_data.game_mgr.register_logic_timer(lambda : _tick(), interval=5, mode=CLOCK)

    def destroy_special_guide(self, *_):
        if self._special_double_click_timer:
            global_data.game_mgr.unregister_logic_timer(self._special_double_click_timer)
            self._special_double_click_timer = None
        if self.unit_obj:
            self.unit_obj.unregist_event('E_SEND_BATTLE_GROUP_MSG', self.special_double_click)
        return

    def destroy(self):
        self.destroy_special_guide()
        super(ComSpecialBattleGuide, self).destroy()