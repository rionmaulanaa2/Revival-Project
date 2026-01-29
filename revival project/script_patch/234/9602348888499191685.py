# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/client/const/key_const.py
from __future__ import absolute_import
import six
from six.moves import range
import game3d
key_config = {'MOUSE_BUTTON_LEFT': 1,
   'MOUSE_BUTTON_RIGHT': 2,
   'MOUSE_BUTTON_MIDDLE': 4,
   'MOUSE_BUTTON_BACK': 5,
   'MOUSE_BUTTON_FORWARD': 6,
   'VK_ENTER': 13,
   'VK_SPACE': 32,
   'VK_ESCAPE': 27,
   'VK_BACKSPACE': 8,
   'VK_TAB': 9,
   'VK_CAPSLOCK': 20,
   'VK_SHIFT': 16,
   'VK_CTRL': 17,
   'VK_ALT': 18,
   'VK_LSHIFT': 160,
   'VK_RSHIFT': 161,
   'VK_LCTRL': 162,
   'VK_RCTRL': 163,
   'VK_LALT': 164,
   'VK_RALT': 165,
   'VK_INSERT': 45,
   'VK_DELETE': 46,
   'VK_HOME': 36,
   'VK_END': 35,
   'VK_PAGEUP': 33,
   'VK_PAGEDOWN': 34,
   'VK_SNAPSHOT': 44,
   'VK_LEFT': 37,
   'VK_UP': 38,
   'VK_RIGHT': 39,
   'VK_DOWN': 40,
   'VK_NUM_1 ': 97,
   'VK_NUM_2 ': 98,
   'VK_NUM_3 ': 99,
   'VK_NUM_4 ': 100,
   'VK_NUM_SUB ': 109,
   'VK_NUM_ENTER ': 13,
   'VK_NUM_ADD ': 107,
   'VK_DEC': 189,
   'VK_ADD': 187,
   'VK_NUMLOCK': 144,
   'VK_NUM0': 96,
   'VK_NUM1': 97,
   'VK_NUM2': 98,
   'VK_NUM3': 99,
   'VK_NUM4': 100,
   'VK_NUM5': 101,
   'VK_NUM6': 102,
   'VK_NUM7': 103,
   'VK_NUM8': 104,
   'VK_NUM9': 105,
   'VK_NUMDOT': 110,
   'VK_NUMDIV': 111,
   'VK_NUMMUL': 106,
   'VK_NUMDEC': 109,
   'VK_NUMADD': 107,
   'VK_TILDE': 192
   }
key_config.update(dict([ ('VK_' + chr(idx), idx) for idx in range(ord('A'), ord('Z') + 1) ]))
key_config.update(dict([ ('VK_F%d' % idx, 111 + idx) for idx in range(1, 13) ]))
key_config.update(dict([ ('VK_' + chr(idx), idx) for idx in range(ord('0'), ord('9') + 1) ]))

def transform_to_android_key_config(value_to_key_config):
    white_list = [
     'MOUSE_BUTTON_LEFT', 'MOUSE_BUTTON_RIGHT', 'MOUSE_BUTTON_MIDDLE', 'VK_SHIFT', 'VK_CTRL', 'VK_ALT']
    from logic.vscene.parts.ctrl.VirtualCodeComplement import MOUSE_BUTTON_BACK, MOUSE_BUTTON_FORWARD
    from logic.vscene.parts.ctrl import VirtualCodeComplement
    other_list = [
     'MOUSE_BUTTON_BACK', 'MOUSE_BUTTON_FORWARD']
    import game
    value_to_key_config_new = {}
    from common.cfg import confmgr
    hot_key_android_key_map = confmgr.get('hot_key_android_key_map')
    hot_key_android_key_map_new = {}
    for key, val in six.iteritems(hot_key_android_key_map):
        hot_key_android_key_map_new[val] = int(key)

    for keycode in list(value_to_key_config.keys()):
        keycode_name = value_to_key_config[keycode]
        if keycode in hot_key_android_key_map_new:
            new_keycode = hot_key_android_key_map_new[keycode]
            value_to_key_config_new[new_keycode] = keycode_name
        elif keycode_name in white_list:
            keycode = getattr(game, keycode_name)
            if keycode:
                value_to_key_config_new[keycode] = keycode_name
        elif keycode_name in other_list:
            keycode = getattr(VirtualCodeComplement, keycode_name)
            if keycode:
                value_to_key_config_new[keycode] = keycode_name
        else:
            log_error("key_const: hot_key_android_key_map doesn't contain key", keycode_name, keycode)

    return value_to_key_config_new


value_to_key_config = {}
for k, v in six.iteritems(key_config):
    if v in value_to_key_config:
        log_error('key_const: key value should be unique!', v, value_to_key_config[v], k)
    value_to_key_config[v] = k

if game3d.get_platform() == game3d.PLATFORM_ANDROID and (global_data.is_android_pc or global_data.is_mumu_pc_control):
    value_to_key_config = transform_to_android_key_config(value_to_key_config)

def hot_key_value_to_hot_key_name--- This code section failed: ---

 140       0  LOAD_GLOBAL           0  'value_to_key_config'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9