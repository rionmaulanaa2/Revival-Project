# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/str_utils.py
from __future__ import absolute_import
import six
import re

def is_number(num):
    pattern = re.compile('^[-+]?[-0-9]\\d*\\.\\d*|[-+]?\\.?[0-9]\\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def unicode_to_str(data):
    t = type(data)
    if t is str:
        return data
    else:
        if t is six.text_type:
            return data.encode('utf-8')
        if t is dict:
            return {unicode_to_str(k):unicode_to_str(v) for k, v in six.iteritems(data)}
        if t is list or t is tuple:
            return [ unicode_to_str(e) for e in data ]
        return data


def convert_python_tb_to_print(tb_cont):
    import types
    if not isinstance(tb_cont, bytes):
        return ''
    if len(tb_cont) == 0:
        return ''
    return tb_cont.replace('file_name: ', '\t').replace('func_name:', 'in').replace(' line_no: ', ': ').replace('|', '\n')


def convert_python_tb_removing_locals(tb_cont):
    if not isinstance(tb_cont, str):
        return ''
    if len(tb_cont) == 0:
        return ''
    new_tb_str_list = []
    idx = 0
    while idx < len(tb_cont):
        new_idx = tb_cont.find('|', idx)
        if new_idx != -1:
            check_str = tb_cont[idx:new_idx + 1]
        else:
            check_str = tb_cont[idx:]
        new_str = _filter_tb_removing_local(check_str)
        new_tb_str_list.append(new_str)
        if new_idx == -1:
            break
        idx = new_idx + 1

    new_tb_str = '\n'.join(new_tb_str_list)
    return new_tb_str


def convert_python_tb_to_str(t, v, tb, limit=None):
    tbinfo = []
    if tb is None:
        return
    else:
        n = 0
        while tb and (limit is None or n < limit):
            frame = tb.tb_frame
            try:
                local_str = str(frame.f_locals)
            except:
                local_str = 'Cannot print locals'

            if len(local_str) > 5000:
                local_str = 'Exceed max length:' + local_str[:5000]
            script_idx = frame.f_code.co_filename.find('script', 0)
            if script_idx != -1:
                filename = frame.f_code.co_filename[script_idx:]
            line = ['file_name: ' + frame.f_code.co_filename,
             'func_name: ' + frame.f_code.co_name,
             'line_no: ' + str(tb.tb_lineno), 'locals: ' + local_str]
            for idx, item in enumerate(line):
                item = item.replace('|', '^')
                line[idx] = item

            tbinfo.append(' '.join(line))
            tb = tb.tb_next
            n = n + 1

        return '%s|%s|%s' % (str(t), str(v), '|'.join(tbinfo))


def _filter_tb_removing_local--- This code section failed: ---

  95       0  LOAD_FAST             0  'check_str'
           3  STORE_FAST            1  'new_str'

  96       6  LOAD_FAST             0  'check_str'
           9  LOAD_ATTR             0  'find'
          12  LOAD_CONST            1  ' locals:'
          15  CALL_FUNCTION_1       1 
          18  STORE_FAST            2  'idx'

  97      21  LOAD_FAST             2  'idx'
          24  LOAD_CONST            2  -1
          27  COMPARE_OP            3  '!='
          30  POP_JUMP_IF_FALSE    46  'to 46'

  98      33  POP_JUMP_IF_FALSE     3  'to 3'
          36  LOAD_FAST             2  'idx'
          39  SLICE+3          
          40  STORE_FAST            1  'new_str'
          43  JUMP_FORWARD         40  'to 86'

 100      46  LOAD_FAST             0  'check_str'
          49  LOAD_ATTR             0  'find'
          52  LOAD_CONST            4  '|'
          55  CALL_FUNCTION_1       1 
          58  STORE_FAST            2  'idx'

 101      61  LOAD_FAST             2  'idx'
          64  LOAD_CONST            2  -1
          67  COMPARE_OP            3  '!='
          70  POP_JUMP_IF_FALSE    86  'to 86'

 102      73  POP_JUMP_IF_FALSE     3  'to 3'
          76  LOAD_FAST             2  'idx'
          79  SLICE+3          
          80  STORE_FAST            1  'new_str'
          83  JUMP_FORWARD          0  'to 86'
        86_0  COME_FROM                '83'
        86_1  COME_FROM                '43'

 103      86  LOAD_FAST             1  'new_str'
          89  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 33


def get_output_stack_str():
    import inspect
    stack_list = inspect.stack()[1:]
    stack_list.reverse()
    ret_str = '-------CALL BEGIN (%s)--------\n' % stack_list[len(stack_list) - 1][3]
    for idx, item in enumerate(stack_list):
        obj, file, line, func_name, code, num = item
        ret_str += '%2d: %-30s %s::%d' % (idx, 'FUNC:%s(...)\n' % func_name, file, line)

    ret_str += '=======CALL END=========='
    return ret_str