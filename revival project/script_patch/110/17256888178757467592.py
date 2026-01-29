# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ctrl/KeyboardMouseOperations.py
from __future__ import absolute_import
import six_ex
from common.framework import Functor
from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event, trigger_ui_btn_event_compatible
import functools
import cc
from data.hot_key_def import MOVE_FORWARD, MOVE_BACKWARD, MOVE_LEFT, MOVE_RIGHT
ALL = 0
HUMAN = 1
MECHA = 2
MECHA_TRANS = 3
MOTORCYCLE = 4
TV_MISSILE_LAUNCHER = 5
MAINSETTING_UI_UNSHIELD_HOT_KEYS = (
 MOVE_FORWARD, MOVE_BACKWARD, MOVE_LEFT, MOVE_RIGHT)

class KeyboardMouseOperations(object):

    def __init__--- This code section failed: ---

  30       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'init_parameters'
           6  CALL_FUNCTION_0       0 
           9  POP_TOP          

  31      10  LOAD_GLOBAL           1  'set'
          13  LOAD_GLOBAL           2  'six_ex'
          16  LOAD_ATTR             3  'keys'
          19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             4  'conf'
          25  CALL_FUNCTION_1       1 
          28  CALL_FUNCTION_1       1 
          31  STORE_FAST            1  'all_short_name'

  32      34  SETUP_LOOP          146  'to 183'
          37  LOAD_FAST             1  'all_short_name'
          40  GET_ITER         
          41  FOR_ITER            138  'to 182'
          44  STORE_FAST            2  'name'

  33      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             5  'process_binding_func'
          53  LOAD_FAST             0  'self'
          56  LOAD_ATTR             4  'conf'
          59  LOAD_FAST             2  'name'
          62  BINARY_SUBSCR    
          63  LOAD_CONST            1  1
          66  BINARY_SUBSCR    
          67  CALL_FUNCTION_1       1 
          70  STORE_FAST            3  'func'

  34      73  LOAD_FAST             0  'self'
          76  LOAD_ATTR             4  'conf'
          79  LOAD_FAST             2  'name'
          82  BINARY_SUBSCR    
          83  LOAD_CONST            2  ''
          86  BINARY_SUBSCR    
          87  STORE_FAST            4  'entity_type_list'

  35      90  LOAD_FAST             3  'func'
          93  LOAD_FAST             4  'entity_type_list'
          96  LOAD_FAST             0  'self'
          99  LOAD_ATTR             4  'conf'
         102  LOAD_FAST             2  'name'
         105  BINARY_SUBSCR    
         106  LOAD_CONST               '<code_object final_func>'
         109  MAKE_FUNCTION_3       3 
         112  STORE_FAST            5  'final_func'

  59     115  LOAD_GLOBAL           6  'setattr'
         118  LOAD_GLOBAL           4  'conf'
         121  LOAD_FAST             2  'name'
         124  BINARY_ADD       
         125  LOAD_GLOBAL           7  'functools'
         128  LOAD_ATTR             8  'partial'
         131  LOAD_FAST             5  'final_func'
         134  LOAD_FAST             5  'final_func'
         137  LOAD_CONST            2  ''
         140  CALL_FUNCTION_258   258 
         143  CALL_FUNCTION_3       3 
         146  POP_TOP          

  60     147  LOAD_GLOBAL           6  'setattr'
         150  LOAD_GLOBAL           6  'setattr'
         153  LOAD_FAST             2  'name'
         156  BINARY_ADD       
         157  LOAD_GLOBAL           7  'functools'
         160  LOAD_ATTR             8  'partial'
         163  LOAD_FAST             5  'final_func'
         166  LOAD_FAST             5  'final_func'
         169  LOAD_CONST            1  1
         172  CALL_FUNCTION_258   258 
         175  CALL_FUNCTION_3       3 
         178  POP_TOP          
         179  JUMP_BACK            41  'to 41'
         182  POP_BLOCK        
       183_0  COME_FROM                '34'

Parse error at or near `CALL_FUNCTION_258' instruction at offset 140

    def process_binding_func(self, node_conf):
        if type(node_conf) in (tuple, list):
            ty = node_conf[0]
            if ty == 'btn':
                if len(node_conf) == 4:
                    _, ui_name, ui_node_list, check_vis = node_conf
                    click_func = ('OnBegin', 'OnEnd')
                else:
                    _, ui_name, ui_node_list, check_vis, kwargs = node_conf
                    click_func = kwargs.get('click_func', ('OnBegin', 'OnEnd'))

                def func_down():
                    global_data.is_key_mocking_ui_event = True
                    trigger_ui_btn_event(ui_name, ui_node_list, click_func[0], need_check_vis=check_vis)
                    global_data.is_key_mocking_ui_event = False

                def func_up():
                    global_data.is_key_mocking_ui_event = True
                    trigger_ui_btn_event(ui_name, ui_node_list, click_func[1], need_check_vis=check_vis)
                    global_data.is_key_mocking_ui_event = False

                return (
                 func_down, func_up)
            if ty == 'func':
                _, func_name, func_args = node_conf
                func = getattr(self, func_name, None)
                if func:

                    def func_func_up():
                        func(*func_args)

                    return (
                     lambda : None, func_func_up)
                log_error('binding func %s not found! ' % func_name)
        return

    def get_binding_func(self, short_name, is_press_down=True):
        mid_fix = 'press_' if is_press_down else 'release_'
        func_name = 'ctrl_' + mid_fix + short_name
        func = getattr(self, func_name, None)
        if func:
            return func
        else:
            log_error('func name %s of KeyboardMouseOperations is not found ' % func_name)
            import traceback
            traceback.print_stack()
            return lambda : None
            return

    def init_parameters(self):
        self.conf = {'human_aim': (
                       [
                        HUMAN], ('btn', 'AimRockerUI', 'aim_button', False)),
           'summon_call_mecha': (
                               [
                                HUMAN, MECHA, MECHA_TRANS], ('func', 'summon_or_call_mecha_func', [])),
           'mecha_fire': (
                        [
                         MECHA, MECHA_TRANS, MOTORCYCLE, TV_MISSILE_LAUNCHER], ('btn', 'MechaControlMain', 'action1.bar', False)),
           'mecha_aim': (
                       [
                        MOTORCYCLE], ('btn', 'MechaControlMain', 'action4.bar', False)),
           'mecha_sub': (
                       [
                        MECHA, MECHA_TRANS], ('btn', 'MechaControlMain', 'action4.bar', False)),
           'mecha_rush': (
                        [
                         MECHA, MECHA_TRANS], ('btn', 'MechaControlMain', 'action6.bar', False)),
           'mecha_jump': (
                        [
                         MECHA, MECHA_TRANS], ('btn', 'MechaControlMain', 'action5.bar', False)),
           'mecha_reload': (
                          [
                           MECHA, MECHA_TRANS], ('btn', 'MechaControlMain', 'action8.bar', False)),
           'mecha_extra_skill': (
                               [
                                MECHA, MECHA_TRANS], ('btn', 'MechaControlMain', 'action7.bar', False))
           }

    def destroy(self):
        pass

    def summon_or_call_mecha_func(self):
        from logic.client.const import game_mode_const
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_PURE_MECHA):
            return
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_PVES):
            return
        ui_mecha = global_data.ui_mgr.get_ui('MechaUIPC')
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH) and ui_mecha and ui_mecha.is_in_quick_call_mode():
            return
        if global_data.player and global_data.player.logic:
            if global_data.player.logic:
                if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                    from logic.gutils.hot_key_utils import check_player_in_land_or_island_state
                    if not check_player_in_land_or_island_state():
                        return
                if not global_data.player.logic.ev_g_get_bind_mecha_type():
                    if global_data.ui_mgr.get_ui('MechaSummonUI'):
                        global_data.ui_mgr.close_ui('MechaSummonUI')
                    else:
                        global_data.is_key_mocking_ui_event = True
                        trigger_ui_btn_event_compatible('MechaUI', 'temp_mech_call.btn_mech_call', 'OnClick')
                        global_data.is_key_mocking_ui_event = False
                else:
                    mecha = global_data.mecha
                    if mecha and mecha.logic:
                        mecha_type = mecha.logic.__class__.__name__
                        if mecha_type == 'LMecha':
                            global_data.is_key_mocking_ui_event = True
                            trigger_ui_btn_event_compatible('StateChangeUI', 'btn_change_to_human', 'OnClick')
                            global_data.is_key_mocking_ui_event = False
                        elif mecha_type in ('LMechaTrans', 'LMotorcycle'):
                            global_data.is_key_mocking_ui_event = True
                            trigger_ui_btn_event_compatible('StateChangeUI', 'btn_change_to_mech', 'OnClick')
                            global_data.is_key_mocking_ui_event = False
                    else:
                        global_data.is_key_mocking_ui_event = True
                        trigger_ui_btn_event_compatible('StateChangeUI', 'btn_change_to_mech', 'OnClick')
                        global_data.is_key_mocking_ui_event = False

    def parse_general_imp_func(self, conf):
        from logic.gutils import hot_key_utils
        usage = conf.get('cHotKeyImp')
        if usage not in ('general_imp', 'general_imp_ex'):
            return
        else:
            imp_func_name = conf.get('cImpFuncName')
            imp_func_args = conf.get('cImpFuncArgs')
            check_func_name = conf.get('cCheckFuncName')
            check_func_args = conf.get('cCheckFuncArgs')
            check_func = None
            event_func = None
            if check_func_name:
                check_func = getattr(hot_key_utils, check_func_name, None)
            if imp_func_name:
                event_func = getattr(hot_key_utils, imp_func_name, None)

            def process_func(key_code, msg, usage=usage):
                if not can_respond_to_key(key_code, msg):
                    return False
                if check_func:
                    if check_func_args:
                        if not check_func(*check_func_args):
                            return False
                    elif not check_func():
                        return False
                if event_func:
                    if usage == 'general_imp':
                        if imp_func_args:
                            return event_func(*imp_func_args)
                        else:
                            return event_func()

                    elif imp_func_args:
                        return event_func(key_code, msg, *imp_func_args)
                    else:
                        return event_func(key_code, msg)

            return process_func


def can_respond_to_key(key_code, msg):
    from logic.gutils import hot_key_utils
    import game
    if key_code != game.VK_ESCAPE:
        except_key_codes = []
        for hot_key_func in MAINSETTING_UI_UNSHIELD_HOT_KEYS:
            hot_key = hot_key_utils.hot_key_func_to_hot_key(hot_key_func)
            except_key_codes.append(hot_key)

        if key_code in except_key_codes:
            return True
        if global_data.ui_mgr.get_ui('MainSettingUI'):
            return False
    return True