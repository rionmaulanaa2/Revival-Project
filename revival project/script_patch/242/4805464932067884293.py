# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ctrl/GamePyHook.py
from __future__ import absolute_import
import six_ex
import six
from game import _default_on_key_msg, key_states, MSG_KEY_UP
import game
from logic.vscene.parts.ctrl.VirtualCodeComplement import MOUSE_BUTTON_BACK, MOUSE_BUTTON_FORWARD
ANY_KEY = -2

def set_key_states(msg, key_code):
    if key_code not in game.key_states:
        game.key_states[key_code] = False
    if msg == game.MSG_KEY_UP:
        game.key_states[key_code] = False
    else:
        game.key_states[key_code] = True


PC_HOTKEY_CUSTOM_CACHE_UNBIND_STR_VAL = 'UNBOUND'
PC_HOTKEY_CUSTOM_CACHE_UNBIND_INT_VAL = -1
PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST = [PC_HOTKEY_CUSTOM_CACHE_UNBIND_INT_VAL]

def release_all_keys():
    for vk_code, state in six.iteritems(key_states.copy()):
        if state:
            _default_on_key_msg(MSG_KEY_UP, vk_code)


def release_key(vk_code):
    if not is_vk_code_valid(vk_code):
        return
    if vk_code in key_states:
        state = key_states[vk_code]
        if state:
            _default_on_key_msg(MSG_KEY_UP, vk_code)


if not global_data.is_android_pc:
    black_list = ('VK_NUM_ENTER', )
else:
    black_list = tuple()
vk_code_to_vk_name_dict = {}
vk_name_to_vk_code_dict = {}
name_transfer_dict = {'VK_ALT': 'VK_LALT',
   'VK_VK_CTRL': 'VK_LCTRL',
   'VK_NUMADD': 'VK_NUM_ADD',
   'VK_NUMDEC': 'VK_NUM_SUB',
   'VK_SHIFT': 'VK_LSHIFT'
   }
for var_name in dir(game):
    if not hasattr(game, var_name):
        continue
    val = getattr(game, var_name)
    if var_name.startswith('VK_'):
        if var_name in black_list:
            continue
        vk_name_to_vk_code_dict[var_name] = val
        if val in vk_code_to_vk_name_dict:
            if var_name not in name_transfer_dict:
                vk_code_to_vk_name_dict[val] = var_name
            else:
                vk_code_to_vk_name_dict[val] = name_transfer_dict[var_name]
        else:
            vk_code_to_vk_name_dict[val] = var_name

from logic.vscene.parts.ctrl import VirtualCodeComplement
for var_name in dir(VirtualCodeComplement):
    if not hasattr(VirtualCodeComplement, var_name):
        continue
    val = getattr(VirtualCodeComplement, var_name)
    if var_name.startswith('VK_'):
        if var_name in black_list:
            continue
        vk_code_to_vk_name_dict[val] = var_name

vk_code_to_vk_name_dict[game.MOUSE_BUTTON_LEFT] = 'MOUSE_BUTTON_LEFT'
vk_code_to_vk_name_dict[game.MOUSE_BUTTON_RIGHT] = 'MOUSE_BUTTON_RIGHT'
vk_code_to_vk_name_dict[game.MOUSE_BUTTON_MIDDLE] = 'MOUSE_BUTTON_MIDDLE'
vk_code_to_vk_name_dict[MOUSE_BUTTON_BACK] = 'MOUSE_BUTTON_BACK'
vk_code_to_vk_name_dict[MOUSE_BUTTON_FORWARD] = 'MOUSE_BUTTON_FORWARD'
vk_code_to_vk_name_dict[ANY_KEY] = 'ANY_KEY'
vk_code_to_vk_name_dict[PC_HOTKEY_CUSTOM_CACHE_UNBIND_INT_VAL] = PC_HOTKEY_CUSTOM_CACHE_UNBIND_STR_VAL
vk_name_to_vk_code_dict.update({vk_name:vk_code for vk_code, vk_name in six.iteritems(vk_code_to_vk_name_dict)})

def vk_code_to_vk_name--- This code section failed: ---

 140       0  LOAD_GLOBAL           0  'vk_code_to_vk_name_dict'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9


def get_all_vk_codes():
    return six_ex.keys(vk_code_to_vk_name_dict)


def is_vk_code_valid(vk_code):
    return vk_code in vk_code_to_vk_name_dict


def get_vk_code(vk_name):
    return vk_name_to_vk_code_dict.get(vk_name, None)


hook_key_msg_map = {}
hook_key_states = {}
hook_full_handler = []

def _key_handler(msg, key_code):
    global hook_full_handler
    global hook_key_msg_map
    if global_data.test_pc_mode:
        if global_data.is_android_pc or global_data.is_mumu_pc_control:
            from logic.client.const.key_const import hot_key_value_to_hot_key_name
            hot_key_name = hot_key_value_to_hot_key_name(key_code)
            print ('_key_handler', msg, key_code, 'name', hot_key_name)
    if key_code not in hook_key_states:
        hook_key_states[key_code] = False
    if msg == MSG_KEY_UP:
        hook_key_states[key_code] = False
    else:
        hook_key_states[key_code] = True
    try:
        handler = hook_key_msg_map[msg][key_code]
    except KeyError:
        pass
    else:
        handler(msg, key_code)

    for handler in hook_full_handler:
        handler(msg, key_code)


game.add_key_handler(None, None, _key_handler)

def add_key_handler(msg, key_codes, handler):
    if msg is None or key_codes is None:
        hook_full_handler.append(handler)
    else:
        kdict = hook_key_msg_map.setdefault(msg, {})
        for key in key_codes:
            kdict[key] = handler

    return


def remove_key_handler(msg, key_codes, handler):
    if msg is None or key_codes is None:
        hook_full_handler.remove(handler)
    else:
        kdict = hook_key_msg_map.setdefault(msg, {})
        for key in key_codes:
            try:
                del kdict[key]
            except KeyError:
                pass

    return


def is_key_down(keycode):
    return hook_key_states.get(keycode, False)


def set_hot_key_code_map(code_map):
    import game
    game.set_hot_key_code_map(code_map)