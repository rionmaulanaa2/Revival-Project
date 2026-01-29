# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/rich_text_utils.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.gutils.rich_text_custom_utils import on_click_show_rank_list_imp
CUSTOM_TYPE_MECHA_RANK = 1

def test(lab):
    txt = '\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\x80\xe4\xb8\x8b\xef\xbc\x9a <node>show_rank_list_imp:titles=["\xe6\x9c\xba\xe7\x94\xb2\xe5\x90\x8d\xe7\xa7\xb0", "\xe5\xb8\x82\xe7\xba\xa7\xe6\x8e\x92\xe5\x90\x8d"]@contents=[1,2]</node>  #SB[{}]\xe7\x82\xb9\xe8\xb5\x9e#SW<img="gui/ui_res_2/common/icon/icon_like2.png">#n[{}]#n ssss'
    a = global_data.ui_mgr.get_ui('MainLoginUI').panel.lab_test
    a.SetString(txt)


rich_text_custom_node_dict = {}

def get_rich_text_custom_node(custom_node):
    return rich_text_custom_node_dict.get(custom_node, None)


rich_text_click_event_dict = {CUSTOM_TYPE_MECHA_RANK: on_click_show_rank_list_imp
   }

def check_has_custom_node(rich_text):
    if '</node>' in rich_text:
        return True


def preprocess_custom_node_text(rich_text):
    START_TOKEN = '<node='
    END_TOKEN = '</node>'
    len_end_token = len(END_TOKEN)
    INSERT_TEXT = '<touch=x%d> </touch>'
    node_index = 0
    mapping_dict = {}
    if START_TOKEN not in rich_text and END_TOKEN not in rich_text:
        return (rich_text, mapping_dict)
    else:
        while True:
            start_idx = rich_text.find(START_TOKEN)
            end_idx = rich_text.find(END_TOKEN)
            if start_idx != -1 and end_idx != -1:
                insert_text = INSERT_TEXT % node_index
                mapping_dict.update({'x%d' % node_index: rich_text[start_idx:end_idx + len_end_token + 1]})
                node_index += 1
                rich_text = rich_text[:start_idx] + insert_text + rich_text[end_idx + len_end_token + 1:]
            else:
                break

        return (
         rich_text, mapping_dict)


def parse_func_param_str_with_dict_with_safe_check(func_str, parameter_sep='@#@'):
    import json
    import re
    func = ''
    param_list = []
    param_dict = {}
    func_sep_index = func_str.find(':')
    if func_sep_index <= 0:
        return (func, param_list, param_dict)
    if func_sep_index > 0:
        func = func_str[:func_sep_index]
        param_list_str = func_str[func_sep_index + 1:]
    else:
        func = ''
        param_list_str = ''
    param_list_str = param_list_str.strip()
    if param_list_str:
        if param_list_str.startswith('['):
            if not param_list_str.endswith(']'):
                log_error('can not find left ]', func, param_list_str)
                return (
                 func, param_list, param_dict)
            param_list = json.loads(param_list_str)
        else:
            at_param_list = param_list_str.split(parameter_sep)
            for i, key_value in enumerate(at_param_list):
                sep_index = key_value.find('=')
                if sep_index <= 0:
                    log_error('invalid custom node syntax', func, key_value)
                    return (
                     func, param_list, param_dict)
                left = key_value[:sep_index]
                right = key_value[sep_index + 1:].strip()
                param_dict[left] = right
                if right[0] == '[' and right[-1] == ']':
                    param_dict[left] = json.loads(right)

    return (
     func, param_list, param_dict)


def generate_custom_node(rich_text):
    from logic.gutils.rich_text_custom_utils import show_rank_list_imp, show_assult_rank_list_imp, show_pve_rank_list_imp, show_pve_mecha_rank_list_imp
    fun_dict = {'show_rank_list': show_rank_list_imp,
       'show_assault_rank_list': show_assult_rank_list_imp,
       'show_pve_rank_list_imp': show_pve_rank_list_imp,
       'show_pve_mecha_rank_list_imp': show_pve_mecha_rank_list_imp
       }
    import re
    START_TOKEN = '<node=([0-9]+)>'
    END_TOKEN = '</node>'
    start_match = re.search(START_TOKEN, rich_text)
    start_idx = -1
    if not start_match:
        return (None, '')
    else:
        start_idx = start_match.start()
        start_len = start_match.end() - start_match.start()
        touch_method_str = str(start_match.groups()[0])
        if touch_method_str == '0':
            touch_method_str = ''
        end_idx = rich_text.find(END_TOKEN)
        txt = rich_text[start_idx + start_len:end_idx]
        _func_str, _param_list, _param_dict = parse_func_param_str_with_dict_with_safe_check(txt, parameter_sep='@#@')
        if _func_str and _func_str in fun_dict:
            func = fun_dict[_func_str]
            if callable(func):
                return (func(*_param_list, **_param_dict), touch_method_str)
            else:
                log_error('unsupported custom func!', _func_str, rich_text)
                return (
                 None, touch_method_str)

        return (None, touch_method_str)


def place_custom_node(rich_text_nd, mapping_dict):
    count = rich_text_nd.getElementCount()
    replace_dict = {}
    for i in range(count):
        nd = rich_text_nd.getElement(i)
        if not nd.isTouchEnabled():
            continue
        ts = nd.getTouchString()
        if ts in mapping_dict:
            replace_dict[i] = mapping_dict[ts]

    if replace_dict:
        for node_index in sorted(six_ex.keys(replace_dict), reverse=True):
            _node, touchstr = generate_custom_node(replace_dict[node_index])
            if _node:
                rich_text_nd.removeElement(node_index)
                import ccui
                custom_node = ccui.RichElementCustomNode.create(_node.get())
                if touchstr:
                    custom_node.setTouchEnabled(True)
                    custom_node.setTouchString('{"link": %s}' % str(touchstr))
                rich_text_nd.insertElement(custom_node, node_index)
                rich_text_custom_node_dict[custom_node] = _node

                def remove_record(custom_node=custom_node):
                    if custom_node in rich_text_custom_node_dict:
                        del rich_text_custom_node_dict[custom_node]

                _node.setBeforeReleaseCallback(remove_record)


def on_custom_chat_link(msg, element, touch, eventTouch):
    import json
    nd_table = get_rich_text_custom_node(element)
    if not nd_table:
        return
    if nd_table.IsDestroyed():
        return
    data_dict = json.loads(msg)
    msg = data_dict.get('link')
    func = rich_text_click_event_dict.get(msg)
    if func:
        func(nd_table, element, touch, eventTouch)