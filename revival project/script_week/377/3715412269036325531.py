# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/utility.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from six.moves import map
import hashlib
from random import randint
from mobile.mobilelog.LogManager import LogManager
import six
if six.PY2:
    import new
dummy_cb = lambda *args, **kwargs: None
_logger = LogManager.get_logger('game')

def log_last_except():
    _logger.log_last_except()


def log_error(_fmt, *args):
    _logger.error(_fmt, *args)


def log_warn(_fmt, *args):
    _logger.warn(_fmt, *args)


def log_info(_fmt, *args):
    _logger.info(_fmt, *args)


def log_debug(_fmt, *args):
    _logger.debug(_fmt, *args)


def log_assert(cond, _fmt, *args):
    pass


def init_game_log():
    import six.moves.builtins
    six.moves.builtins.__dict__['log_debug'] = log_debug
    six.moves.builtins.__dict__['log_info'] = log_info
    six.moves.builtins.__dict__['log_warn'] = log_warn
    six.moves.builtins.__dict__['log_error'] = log_error
    six.moves.builtins.__dict__['log_last_except'] = log_last_except
    six.moves.builtins.__dict__['log_stack'] = output_stack
    six.moves.builtins.__dict__['log_assert'] = log_assert


def try_func(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            log_error('func_name: %s, error:%s', func.__name__, str(err))

    return wrapper


def output_stack(title=None, log_func=None):
    import inspect
    stack_list = inspect.stack()[1:]
    stack_list.reverse()
    content = '\n'
    if title is not None:
        content += '****** %s ******\n' % title
    content += '-------CALL BEGIN (%s)--------\n' % stack_list[len(stack_list) - 1][3]
    for idx, item in enumerate(stack_list):
        obj, file, line, func_name, code, num = item
        content += '%2d: %-30s %s::%d\n' % (idx, 'FUNC:%s(...)' % func_name, file, line)

    content += '=======CALL END==========\n'
    if log_func:
        log_func(content)
    else:
        log_error(content)
    return


def get_output_stack_str():
    import inspect
    stack_list = inspect.stack()[1:]
    stack_list = inspect.stack()[1:]
    stack_list.reverse()
    ret_str = '-------CALL BEGIN (%s)--------\n' % stack_list[len(stack_list) - 1][3]
    for idx, item in enumerate(stack_list):
        obj, file, line, func_name, code, num = item
        ret_str += '%2d: %-30s %s::%d' % (idx, 'FUNC:%s(...)\n' % func_name, file, line)

    ret_str += '=======CALL END=========='
    return ret_str


def debug_get_func_info--- This code section failed: ---

  87       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'inspect'
           9  STORE_FAST            1  'inspect'

  88      12  LOAD_FAST             1  'inspect'
          15  LOAD_ATTR             1  'ismethod'
          18  LOAD_FAST             0  'f'
          21  CALL_FUNCTION_1       1 
          24  POP_JUMP_IF_TRUE     42  'to 42'
          27  LOAD_FAST             1  'inspect'
          30  LOAD_ATTR             2  'isfunction'
          33  LOAD_FAST             0  'f'
          36  CALL_FUNCTION_1       1 
        39_0  COME_FROM                '24'
          39  POP_JUMP_IF_FALSE    51  'to 51'

  90      42  LOAD_FAST             0  'f'
          45  STORE_FAST            2  'func'
          48  JUMP_FORWARD         38  'to 89'

  91      51  LOAD_GLOBAL           3  'hasattr'
          54  LOAD_GLOBAL           2  'isfunction'
          57  CALL_FUNCTION_2       2 
          60  POP_JUMP_IF_FALSE    75  'to 75'

  93      63  LOAD_FAST             0  'f'
          66  LOAD_ATTR             4  'fn'
          69  STORE_FAST            2  'func'
          72  JUMP_FORWARD         14  'to 89'

  95      75  LOAD_CONST            3  'UnsupportType: %s'
          78  LOAD_GLOBAL           5  'type'
          81  LOAD_FAST             0  'f'
          84  CALL_FUNCTION_1       1 
          87  BINARY_MODULO    
          88  RETURN_VALUE     
        89_0  COME_FROM                '72'
        89_1  COME_FROM                '48'

  96      89  SETUP_EXCEPT         25  'to 117'

  97      92  LOAD_GLOBAL           6  'str'
          95  LOAD_FAST             1  'inspect'
          98  LOAD_ATTR             7  'getfile'
         101  LOAD_FAST             2  'func'
         104  CALL_FUNCTION_1       1 
         107  CALL_FUNCTION_1       1 
         110  STORE_FAST            3  'trace'
         113  POP_BLOCK        
         114  JUMP_FORWARD         37  'to 154'
       117_0  COME_FROM                '89'

  98     117  DUP_TOP          
         118  LOAD_GLOBAL           8  'Exception'
         121  COMPARE_OP           10  'exception-match'
         124  POP_JUMP_IF_FALSE   153  'to 153'
         127  POP_TOP          
         128  STORE_FAST            4  'e'
         131  POP_TOP          

  99     132  LOAD_CONST            4  'Get trace Error:'
         135  LOAD_GLOBAL           6  'str'
         138  LOAD_FAST             4  'e'
         141  CALL_FUNCTION_1       1 
         144  BUILD_TUPLE_2         2 
         147  STORE_FAST            3  'trace'
         150  JUMP_FORWARD          1  'to 154'
         153  END_FINALLY      
       154_0  COME_FROM                '153'
       154_1  COME_FROM                '114'

 100     154  SETUP_EXCEPT         25  'to 182'

 101     157  LOAD_GLOBAL           6  'str'
         160  LOAD_FAST             1  'inspect'
         163  LOAD_ATTR             9  'getsourcelines'
         166  LOAD_FAST             2  'func'
         169  CALL_FUNCTION_1       1 
         172  CALL_FUNCTION_1       1 
         175  STORE_FAST            5  'trace_line_list'
         178  POP_BLOCK        
         179  JUMP_FORWARD         37  'to 219'
       182_0  COME_FROM                '154'

 102     182  DUP_TOP          
         183  LOAD_GLOBAL           8  'Exception'
         186  COMPARE_OP           10  'exception-match'
         189  POP_JUMP_IF_FALSE   218  'to 218'
         192  POP_TOP          
         193  STORE_FAST            4  'e'
         196  POP_TOP          

 103     197  LOAD_CONST            5  'Get line_no Error:'
         200  LOAD_GLOBAL           6  'str'
         203  LOAD_FAST             4  'e'
         206  CALL_FUNCTION_1       1 
         209  BUILD_TUPLE_2         2 
         212  STORE_FAST            5  'trace_line_list'
         215  JUMP_FORWARD          1  'to 219'
         218  END_FINALLY      
       219_0  COME_FROM                '218'
       219_1  COME_FROM                '179'

 104     219  LOAD_FAST             2  'func'
         222  LOAD_ATTR            10  '__name__'
         225  LOAD_CONST            6  ', Trace:'
         228  BINARY_ADD       
         229  LOAD_FAST             3  'trace'
         232  BINARY_ADD       
         233  LOAD_CONST            7  ',line_no:'
         236  BINARY_ADD       
         237  LOAD_GLOBAL           6  'str'
         240  LOAD_FAST             5  'trace_line_list'
         243  CALL_FUNCTION_1       1 
         246  BINARY_ADD       
         247  STORE_FAST            6  'info'

 105     250  LOAD_FAST             6  'info'
         253  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 57


def convert_python_tb_removing_locals(tb_cont):
    import types
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


def convert_python_tb_to_print(tb_cont):
    if not isinstance(tb_cont, str):
        return ''
    if len(tb_cont) == 0:
        return ''
    return tb_cont.replace('file_name: ', '\t').replace('func_name:', 'in').replace(' line_no: ', ': ').replace('|', '\n')


def convert_python_tb_to_str(t, v, tb, limit=None):
    tbinfo = []
    if tb == None:
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
            line = ['file_name: ' + frame.f_code.co_filename, 'func_name: ' + frame.f_code.co_name,
             'line_no: ' + str(tb.tb_lineno), 'locals: ' + local_str]
            for idx, item in enumerate(line):
                item = item.replace('|', '^')
                line[idx] = item

            tbinfo.append(' '.join(line))
            tb = tb.tb_next
            n = n + 1

        return '%s|%s|%s' % (str(t), str(v), '|'.join(tbinfo))


def _filter_tb_removing_local--- This code section failed: ---

 163       0  LOAD_FAST             0  'check_str'
           3  STORE_FAST            1  'new_str'

 164       6  LOAD_FAST             0  'check_str'
           9  LOAD_ATTR             0  'find'
          12  LOAD_CONST            1  ' locals:'
          15  CALL_FUNCTION_1       1 
          18  STORE_FAST            2  'idx'

 165      21  LOAD_FAST             2  'idx'
          24  LOAD_CONST            2  -1
          27  COMPARE_OP            3  '!='
          30  POP_JUMP_IF_FALSE    46  'to 46'

 166      33  POP_JUMP_IF_FALSE     3  'to 3'
          36  LOAD_FAST             2  'idx'
          39  SLICE+3          
          40  STORE_FAST            1  'new_str'
          43  JUMP_FORWARD         40  'to 86'

 168      46  LOAD_FAST             0  'check_str'
          49  LOAD_ATTR             0  'find'
          52  LOAD_CONST            4  '|'
          55  CALL_FUNCTION_1       1 
          58  STORE_FAST            2  'idx'

 169      61  LOAD_FAST             2  'idx'
          64  LOAD_CONST            2  -1
          67  COMPARE_OP            3  '!='
          70  POP_JUMP_IF_FALSE    86  'to 86'

 170      73  POP_JUMP_IF_FALSE     3  'to 3'
          76  LOAD_FAST             2  'idx'
          79  SLICE+3          
          80  STORE_FAST            1  'new_str'
          83  JUMP_FORWARD          0  'to 86'
        86_0  COME_FROM                '83'
        86_1  COME_FROM                '43'

 171      86  LOAD_FAST             1  'new_str'
          89  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 33


components_relation_path_dict = {}

def meta_component(cls, package, member_name_list):
    import inspect
    import types
    member_list = []
    for m_name in member_name_list:
        mod = __import__(package, globals(), locals(), [m_name])
        mod = getattr(mod, m_name, None)
        member = getattr(mod, m_name, None)
        if member:
            member_list.append(member)
        else:
            raise Exception('[Class %s] member cannot find: %s' % (cls.__name__, m_name))
        if G_IS_SERVER:
            from mobile.distserver.game import GameServerRepo
            if GameServerRepo.is_inner_server() and GameServerRepo.game_server_name == 'game_0':
                cls_path = inspect.getsourcefile(cls)
                if cls_path:
                    cls_path = cls_path[cls_path.rfind('\\logic'):]
                    class_path_name = cls_path + '&' + cls.__name__
                    com_path = inspect.getsourcefile(mod)
                    com_path = com_path[com_path.rfind('\\logic'):]
                    com_path_name = com_path + '&' + m_name
                    components_relation_path_dict.setdefault(com_path_name, [])
                    if class_path_name not in components_relation_path_dict[com_path_name]:
                        components_relation_path_dict[com_path_name].append(class_path_name)

    check_type = (
     int, str, bytes, list,
     dict, tuple, float, set, frozenset)
    for inherit in member_list:
        if six.PY2:
            methods = inspect.getmembers(inherit, inspect.ismethod)
        else:
            methods = inspect.getmembers(inherit, inspect.isfunction)
        for fun_name, fun in methods:
            if hasattr(cls, fun_name):
                raise Exception('[Class %s] function %s has define' % (cls.__name__, fun_name))
            if six.PY2:
                setattr(cls, fun_name, fun.__func__)
            else:
                setattr(cls, fun_name, fun)

        for memb_name, memb in inspect.getmembers(inherit):
            if memb_name in ('__module__', '__doc__', '__name__'):
                continue
            if isinstance(memb, check_type):
                if hasattr(cls, memb_name):
                    raise Exception('[Class %s] member %s has define' % (cls.__name__, memb_name))
                setattr(cls, memb_name, memb)

    return


def meta_class(package, member_name_list):

    def _call_meta_member_func(self, func_name_template, *args, **kwargs):
        cls = self.__class__
        meta_member_func = cls._meta_member_func_dict.get(func_name_template)
        if not meta_member_func:
            meta_member_func = []
            for mem_name in member_name_list:
                mem_part = mem_name[3:].lower()
                func_name = func_name_template.replace('@', mem_part)
                meta_func = getattr(cls, func_name, None)
                if meta_func:
                    meta_member_func.append(meta_func)

            cls._meta_member_func_dict[func_name_template] = meta_member_func
        for meta_func in meta_member_func:
            meta_func(self, *args, **kwargs)

        return

    class Meta(type):

        def __init__--- This code section failed: ---

 260       0  LOAD_GLOBAL           0  'super'
           3  LOAD_DEREF            0  'Meta'
           6  LOAD_FAST             0  'cls'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             1  '__init__'
          15  LOAD_FAST             1  'name'
          18  LOAD_FAST             2  'bases'
          21  LOAD_FAST             3  'dic'
          24  CALL_FUNCTION_3       3 
          27  POP_TOP          

 263      28  LOAD_GLOBAL           2  'setattr'
          31  LOAD_GLOBAL           1  '__init__'
          34  BUILD_MAP_0           0 
          37  CALL_FUNCTION_3       3 
          40  POP_TOP          

 264      41  LOAD_GLOBAL           2  'setattr'
          44  LOAD_GLOBAL           2  'setattr'
          47  LOAD_DEREF            1  '_call_meta_member_func'
          50  CALL_FUNCTION_3       3 
          53  POP_TOP          

 267      54  LOAD_GLOBAL           3  'meta_component'
          57  LOAD_FAST             0  'cls'
          60  LOAD_DEREF            2  'package'
          63  LOAD_DEREF            3  'member_name_list'
          66  CALL_FUNCTION_3       3 
          69  POP_TOP          

Parse error at or near `CALL_FUNCTION_3' instruction at offset 37

    return Meta


def manual_meta_class(member_name_list):

    def _call_meta_member_func(self, func_name_template, *args):
        cls = self.__class__
        meta_member_func = cls._meta_member_func_dict.get(func_name_template)
        if not meta_member_func:
            meta_member_func = []
            for mem_name in member_name_list:
                mem_part = mem_name[3:].lower()
                func_name = func_name_template.replace('@', mem_part)
                meta_func = getattr(cls, func_name, None)
                if meta_func:
                    meta_member_func.append(meta_func)

            cls._meta_member_func_dict[func_name_template] = meta_member_func
        for meta_func in meta_member_func:
            meta_func(self, *args)

        return

    class Meta(type):

        def __init__--- This code section failed: ---

 297       0  LOAD_GLOBAL           0  'super'
           3  LOAD_DEREF            0  'Meta'
           6  LOAD_FAST             0  'cls'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             1  '__init__'
          15  LOAD_FAST             1  'name'
          18  LOAD_FAST             2  'bases'
          21  LOAD_FAST             3  'dic'
          24  CALL_FUNCTION_3       3 
          27  POP_TOP          

 300      28  LOAD_GLOBAL           2  'setattr'
          31  LOAD_GLOBAL           1  '__init__'
          34  BUILD_MAP_0           0 
          37  CALL_FUNCTION_3       3 
          40  POP_TOP          

 301      41  LOAD_GLOBAL           2  'setattr'
          44  LOAD_GLOBAL           2  'setattr'
          47  LOAD_DEREF            1  '_call_meta_member_func'
          50  CALL_FUNCTION_3       3 
          53  POP_TOP          

Parse error at or near `CALL_FUNCTION_3' instruction at offset 37

    return Meta


def enhance_class(cls, enhance_cls):
    import inspect
    set_func_to_class = None
    if hasattr(cls, 'get_dict'):
        _dict = cls.get_dict()

        def _set_func_to_dict(funName, fun):
            _dict[funName] = fun

        set_func_to_class = _set_func_to_dict
    else:
        _dict = cls.__dict__

        def _set_func_to_class(funName, fun):
            setattr(cls, funName, fun)

        set_func_to_class = _set_func_to_class
    for mro in inspect.getmro(cls):
        if mro == cls:
            continue
        methods = inspect.getmembers(mro, inspect.ismethod)
        for funName, fun in methods:
            im_self = getattr(fun, six._meth_self, None)
            if im_self:
                im_func = getattr(fun, six._meth_func, None)
                new_fun = six.create_bound_method(im_func, cls)
                set_func_to_class(funName, new_fun)

    if six.PY2:
        for funName, fun in inspect.getmembers(enhance_cls, inspect.ismethod):
            if fun.__self__:
                new_fun = six.create_bound_method(fun.__func__, cls)
                set_func_to_class(funName, new_fun)
            else:
                set_func_to_class(funName, fun.__func__)

    else:
        for funName, fun in inspect.getmembers(enhance_cls, inspect.ismethod):
            im_func = getattr(fun, six._meth_func, None)
            new_fun = six.create_bound_method(im_func, cls)
            set_func_to_class(funName, new_fun)

    for funName, fun in inspect.getmembers(enhance_cls, inspect.isfunction):
        set_func_to_class(funName, fun)

    return cls


def enum(args, start=0):

    class Enum(object):
        __slots__ = args

        def __init__(self):
            for i, key in enumerate(Enum.__slots__, start):
                setattr(self, key, i)

    return Enum()


def get_class_functions(cls):
    return [ func for func in dir(cls) if not func.startswith('_') and callable(getattr(cls, func)) ]


def convert_uuid_key_to_str_key(dic):
    from mobile.common.IdManager import IdManager
    ret_dic = {}
    for k, v in six.iteritems(dic):
        sk = IdManager.id2str(k)
        ret_dic[sk] = v

    return ret_dic


def convert_str_key_to_uuid_key(dic):
    from mobile.common.IdManager import IdManager
    ret_dic = {}
    for k, v in six.iteritems(dic):
        uuidk = IdManager.str2id(k)
        ret_dic[uuidk] = v

    return ret_dic


def convert_dict_key(obj, convert):
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in six.iteritems(obj):
            new[convert(k)] = convert_dict_key(v, convert)

    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__((convert_dict_key(v, convert) for v in obj))
    else:
        return obj
    return new


def get_next_pow_of_two(n):
    res = 1
    while res <= n:
        res = res << 1

    return res


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


def get_host_ip--- This code section failed: ---

 430       0  LOAD_FAST             0  'ip'
           3  UNARY_NOT        
           4  POP_JUMP_IF_TRUE     22  'to 22'
           7  POP_JUMP_IF_TRUE      1  'to 1'
          10  LOAD_CONST            2  '0.0.0.0'
          13  BUILD_TUPLE_2         2 
          16  COMPARE_OP            6  'in'
        19_0  COME_FROM                '7'
        19_1  COME_FROM                '4'
          19  POP_JUMP_IF_FALSE    62  'to 62'

 431      22  LOAD_CONST            3  ''
          25  LOAD_CONST            0  ''
          28  IMPORT_NAME           0  'socket'
          31  STORE_FAST            1  'socket'

 432      34  LOAD_FAST             1  'socket'
          37  LOAD_ATTR             1  'gethostbyname'
          40  LOAD_FAST             1  'socket'
          43  LOAD_ATTR             2  'getfqdn'
          46  LOAD_FAST             1  'socket'
          49  LOAD_ATTR             3  'gethostname'
          52  CALL_FUNCTION_0       0 
          55  CALL_FUNCTION_1       1 
          58  CALL_FUNCTION_1       1 
          61  RETURN_END_IF    
        62_0  COME_FROM                '19'

 434      62  LOAD_FAST             0  'ip'
          65  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 7


def md5sign(*args):
    import six
    return hashlib.md5(six.ensure_binary(''.join(map(str, args)))).hexdigest()


def calc_capsule_need_coin--- This code section failed: ---

 443       0  LOAD_CONST            1  10
           3  LOAD_CONST            2  5
           6  BINARY_MULTIPLY  
           7  BINARY_ADD       
           8  STORE_FAST            1  'coin'

 444      11  LOAD_GLOBAL           0  'min'
          14  LOAD_FAST             1  'coin'
          17  LOAD_CONST            3  20
          20  CALL_FUNCTION_2       2 
          23  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_ADD' instruction at offset 7


def touch--- This code section failed: ---

 449       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'os'
           9  STORE_FAST            2  'os'

 452      12  LOAD_FAST             0  'path'
          15  POP_JUMP_IF_TRUE     22  'to 22'

 453      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 454      22  LOAD_GLOBAL           1  'str'
          25  LOAD_FAST             0  'path'
          28  CALL_FUNCTION_1       1 
          31  STORE_FAST            0  'path'

 455      34  LOAD_FAST             2  'os'
          37  LOAD_ATTR             2  'path'
          40  LOAD_ATTR             3  'expanduser'
          43  LOAD_FAST             0  'path'
          46  CALL_FUNCTION_1       1 
          49  STORE_FAST            0  'path'

 456      52  LOAD_FAST             2  'os'
          55  LOAD_ATTR             2  'path'
          58  LOAD_ATTR             4  'isabs'
          61  LOAD_FAST             0  'path'
          64  CALL_FUNCTION_1       1 
          67  POP_JUMP_IF_TRUE     91  'to 91'

 457      70  LOAD_FAST             2  'os'
          73  LOAD_ATTR             2  'path'
          76  LOAD_ATTR             5  'abspath'
          79  LOAD_FAST             0  'path'
          82  CALL_FUNCTION_1       1 
          85  STORE_FAST            0  'path'
          88  JUMP_FORWARD          0  'to 91'
        91_0  COME_FROM                '88'

 460      91  LOAD_FAST             2  'os'
          94  LOAD_ATTR             2  'path'
          97  LOAD_ATTR             6  'dirname'
         100  LOAD_FAST             0  'path'
         103  CALL_FUNCTION_1       1 
         106  STORE_FAST            3  'dirname'

 461     109  LOAD_FAST             2  'os'
         112  LOAD_ATTR             2  'path'
         115  LOAD_ATTR             7  'exists'
         118  LOAD_FAST             3  'dirname'
         121  CALL_FUNCTION_1       1 
         124  POP_JUMP_IF_TRUE    143  'to 143'

 462     127  LOAD_FAST             2  'os'
         130  LOAD_ATTR             8  'makedirs'
         133  LOAD_FAST             3  'dirname'
         136  CALL_FUNCTION_1       1 
         139  POP_TOP          
         140  JUMP_FORWARD          0  'to 143'
       143_0  COME_FROM                '140'

 465     143  LOAD_FAST             1  'content'
         146  POP_JUMP_IF_FALSE   186  'to 186'

 466     149  LOAD_GLOBAL           9  'open'
         152  LOAD_GLOBAL           2  'path'
         155  CALL_FUNCTION_2       2 
         158  SETUP_WITH           20  'to 181'
         161  STORE_FAST            4  '_file'

 467     164  LOAD_FAST             4  '_file'
         167  LOAD_ATTR            10  'write'
         170  LOAD_FAST             1  'content'
         173  CALL_FUNCTION_1       1 
         176  POP_TOP          
         177  POP_BLOCK        
         178  LOAD_CONST            0  ''
       181_0  COME_FROM_WITH           '158'
         181  WITH_CLEANUP     
         182  END_FINALLY      
         183  JUMP_FORWARD         46  'to 232'

 469     186  SETUP_EXCEPT         20  'to 209'

 470     189  LOAD_FAST             2  'os'
         192  LOAD_ATTR            11  'utime'
         195  LOAD_FAST             0  'path'
         198  LOAD_CONST            0  ''
         201  CALL_FUNCTION_2       2 
         204  POP_TOP          
         205  POP_BLOCK        
         206  JUMP_FORWARD         23  'to 232'
       209_0  COME_FROM                '186'

 471     209  POP_TOP          
         210  POP_TOP          
         211  POP_TOP          

 472     212  LOAD_GLOBAL           9  'open'
         215  LOAD_GLOBAL           3  'expanduser'
         218  CALL_FUNCTION_2       2 
         221  LOAD_ATTR            13  'close'
         224  CALL_FUNCTION_0       0 
         227  POP_TOP          
         228  JUMP_FORWARD          1  'to 232'
         231  END_FINALLY      
       232_0  COME_FROM                '231'
       232_1  COME_FROM                '206'
       232_2  COME_FROM                '183'
         232  LOAD_CONST            0  ''
         235  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 155


def binary_insert(data_list, insert_data, compare_func=None):
    start_index = 0
    end_index = len(data_list) - 1
    if compare_func is None:
        compare_func = lambda a, b: a > b
    while end_index >= start_index:
        mid_index = (start_index + end_index) / 2
        com_ret = compare_func(insert_data, data_list[mid_index])
        if com_ret:
            start_index = mid_index + 1
        else:
            end_index = mid_index - 1

    data_list.insert(start_index, insert_data)
    return


def rand_by_weight(info):
    if len(info) == 1:
        return six_ex.keys(info)[0]
    else:
        sum_rate = sum(six_ex.values(info))
        if sum_rate < 1:
            return None
        total = 0
        r = randint(1, sum_rate)
        for k, w in six.iteritems(info):
            total += w
            if r <= total:
                return k

        return None


def rand_by_weight_tow(info):
    sum_rate = sum(six_ex.keys(info))
    if sum_rate < 1:
        return None
    else:
        total = 0
        r = randint(1, sum_rate)
        for w, v in six.iteritems(info):
            total += w
            if r <= total:
                return v

        return None


def pnpoly(polygon, pos):
    pt_num = len(polygon)
    if pt_num < 3:
        return False
    x, y = pos
    j = pt_num - 1
    in_range = False
    for i in range(pt_num):
        x1 = polygon[i][0]
        y1 = polygon[i][1]
        x2 = polygon[j][0]
        y2 = polygon[j][1]
        j = i
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            in_range = not in_range

    return in_range


def divide_group(total, max, fix_cnt=0):
    import math
    min = max - 1
    if fix_cnt > 0:
        if total // fix_cnt > 0:
            return {fix_cnt: total // fix_cnt}
        else:
            return {}

    while min >= 1:
        cnt = total / min
        left = total - cnt * min
        extra_cnt = 0
        group_dict = {min: cnt}
        if cnt == 0 or int(math.ceil(left * 1.0 / cnt)) + min > max:
            min -= 1
            continue
        else:
            makeup = left // cnt
            group_dict.pop(min, 0)
            group_dict[min + makeup] = cnt
            finally_left = left % cnt
            if finally_left > 0:
                group_dict[min + makeup] = cnt - finally_left
                group_dict[min + makeup + 1] = finally_left
            return group_dict

    return {}


key_set = [
 'total_game_time', 'season_id', 'battle_6_kill_monster', 'battle_42_kill_mecha', 'battle_42_max_kill_human', 'battle_42_max_survival', 'battle_4_first_blood', 'battle_42_get_mvp', 'battle_6_save', 'battle_42_mecha_damage', 'achieve_1_get_mvp', 'battle_6_mecha_cure', 'con_first_13', 'battle_6_mecha_hurt', 'battle_4_survival', 'battle_42_win_cnt', 'battle_6_top5_cnt', 'battle_4_top5_cnt', 'battle_6_win_cnt', 'battle_42_goal_poacher', 'battle_6_fight_back', 'battle_6_terminator', 'battle_42_fight_back', 'battle_4_max_kill_human', 'battle_42_kill', 'battle_4_goal_poacher', 'battle_6_mecha_damage', 'battle_4_assist_mecha', 'battle_6_survival', 'battle_42_max_kill_mecha', 'con_first_1', 'con_first_2', 'battle_4_max_kill_mecha', 'battle_4_move_dist', 'con_first_9', 'battle_6_human_kill_mecha', 'battle_6_max_kill_mecha', 'battle_42_assist_mecha', 'battle_6_right_on_target', 'escape_cnt', 'battle_42_kill_monster', 'battle_6_perfect_atk', 'achieve_2_get_mvp', 'battle_4_kill_mecha', 'con_victory_13', 'battle_4_total_cnt', 'battle_4_win_cnt', 'battle_4_terminator', 'battle_42_mecha_cure', 'battle_4_fight_back', 'battle_6_move_dist', 'likenum', 'battle_42_mecha_hurt', 'battle_6_max_survival', 'battle_4_damage', 'battle_4_human_kill_mecha', 'battle_4_mecha_cure', 'battle_42_save', 'battle_4_kill_monster', 'battle_4_save', 'battle_42_right_on_target', 'battle_6_assist_mecha', 'con_mvp_13', 'battle_6_max_kill_human', 'battle_42_damage', 'battle_6_first_blood', 'battle_42_terminator', 'battle_42_move_dist', 'con_victory_2', 'con_victory_1', 'battle_6_get_mvp', 'con_victory_9', 'battle_42_human_kill_mecha', 'battle_42_first_blood', 'battle_4_right_on_target', 'battle_42_top5_cnt', 'battle_42_perfect_atk', 'battle_4_max_survival', 'battle_6_kill', 'battle_4_mecha_damage', 'battle_4_kill', 'battle_42_survival', 'battle_6_goal_poacher', 'battle_4_perfect_atk', 'battle_6_total_cnt', 'battle_6_damage', 'battle_4_mecha_hurt', 'battle_42_total_cnt', 'con_mvp_2', 'battle_6_kill_mecha', 'con_mvp_9', 'battle_4_get_mvp', 'con_mvp_1']

def get_useful_cache_stat(stat):
    new_stat = {}
    for key in key_set:
        if key in stat:
            new_stat[key] = stat[key]

    return new_stat


def recursive_update(orig_dict, new_dict):
    for k, v in six_ex.items(new_dict):
        if isinstance(v, dict):
            orig_dict[k] = recursive_update(orig_dict.get(k, {}), v)
        else:
            orig_dict[k] = v

    return orig_dict


def nested_dict_add(d1, d2):
    result = dict(d1)
    for key, value in d2.items():
        if key in result and isinstance(value, dict) and isinstance(result[key], dict):
            result[key] = nested_dict_add(result[key], value)
        elif key in result:
            result[key] += value
        else:
            result[key] = value

    return result