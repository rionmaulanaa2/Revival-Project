# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/ui_utils.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from cocosui import cc
import re

def get_screen_size():
    return cc.Director.getInstance().getOpenGLView().getFrameSize()


def get_visible_size():
    win_size = get_screen_size()
    from common.platform.device_info import DeviceInfo
    if not DeviceInfo().is_can_full_screen():
        margins_conf = DeviceInfo().get_screen_adapt_margins()
        WIDTH_EDGE_OFFSET = int(win_size.width * margins_conf.get('WIDTH_EDGE_OFFSET', 0))
        BOTTOM_EDGE_OFFSET = int(win_size.height * margins_conf.get('BOTTOM_EDGE_OFFSET', 0))
        TOP_EDGE_OFFSET = int(win_size.height * margins_conf.get('TOP_EDGE_OFFSET', 0))
        return cc.Size(win_size.width - WIDTH_EDGE_OFFSET * 2, win_size.height - BOTTOM_EDGE_OFFSET - TOP_EDGE_OFFSET)
    else:
        return win_size


def clear_ui_all_cache():
    print('clear_ui_all_cache...')
    if global_data.item_cache_without_check:
        global_data.item_cache_without_check.clear_cache()
    if global_data.uisystem:
        global_data.uisystem.clear_template_cache()


s_winSize = cc.Director.getInstance().getOpenGLView().getFrameSize()
s_visibleSize = get_visible_size()
s_designWidth = 1334
s_designHeight = 750
s_fixDesignResolution = False
s_designSize = cc.Size(s_designWidth, s_designHeight)
s_viewport_scale = 1.0
s_showDesignSize = cc.Size(s_winSize.width / s_viewport_scale, s_designHeight)
s_minRate = min(s_visibleSize.width / s_designWidth, s_visibleSize.height / s_designHeight)
s_maxRate = max(s_visibleSize.width / s_designWidth, s_visibleSize.height / s_designHeight)
s_xRate = s_visibleSize.width / s_designWidth
s_yRate = s_visibleSize.height / s_designHeight
s_scale = 2
s_bg_minRate = min(s_winSize.width / s_designWidth, s_winSize.height / s_designHeight)
s_bg_maxRate = max(s_winSize.width / s_designWidth, s_winSize.height / s_designHeight)
s_bg_xRate = s_winSize.width / s_designWidth
s_bg_yRate = s_winSize.height / s_designHeight
mate_utils = cc.MateUtils.getInstance()
mate_utils.initSizes(s_winSize, s_visibleSize, s_designSize)

def tonumber(num):
    if isinstance(num, int) or isinstance(num, float):
        return num
    if isinstance(num, six.string_types):
        try:
            return float(num)
        except:
            pass


def get_scale(s):
    if isinstance(s, int) or isinstance(s, float):
        return s
    else:
        return mate_utils.calcVisibleScale(s)


default_cancel_dist = get_scale('10w')

def get_scale_old--- This code section failed: ---

  84       0  LOAD_GLOBAL           0  'tonumber'
           3  LOAD_FAST             0  's'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            1  'ret'

  85      12  LOAD_FAST             1  'ret'
          15  LOAD_CONST            0  ''
          18  COMPARE_OP            9  'is-not'
          21  POP_JUMP_IF_FALSE    28  'to 28'

  86      24  LOAD_FAST             1  'ret'
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

  88      28  LOAD_GLOBAL           0  'tonumber'
          31  LOAD_GLOBAL           1  'None'
          34  LOAD_CONST            2  -1
          37  SLICE+3          
          38  CALL_FUNCTION_1       1 
          41  STORE_FAST            2  'pre'

  89      44  LOAD_FAST             2  'pre'
          47  LOAD_CONST            0  ''
          50  COMPARE_OP            8  'is'
          53  POP_JUMP_IF_FALSE    60  'to 60'

  90      56  LOAD_CONST            0  ''
          59  RETURN_END_IF    
        60_0  COME_FROM                '53'

  92      60  RETURN_VALUE     
          61  RETURN_VALUE     
          62  RETURN_VALUE     
          63  BINARY_SUBSCR    
          64  STORE_FAST            3  'last'

  94      67  LOAD_FAST             3  'last'
          70  LOAD_CONST            3  'w'
          73  COMPARE_OP            2  '=='
          76  POP_JUMP_IF_TRUE     91  'to 91'
          79  LOAD_FAST             3  'last'
          82  LOAD_CONST            4  's'
          85  COMPARE_OP            2  '=='
        88_0  COME_FROM                '76'
          88  POP_JUMP_IF_FALSE    99  'to 99'

  96      91  LOAD_FAST             2  'pre'
          94  LOAD_GLOBAL           2  's_minRate'
          97  BINARY_MULTIPLY  
          98  RETURN_END_IF    
        99_0  COME_FROM                '88'

  97      99  LOAD_FAST             3  'last'
         102  LOAD_CONST            5  'q'
         105  COMPARE_OP            2  '=='
         108  POP_JUMP_IF_FALSE   119  'to 119'

  99     111  LOAD_FAST             2  'pre'
         114  LOAD_GLOBAL           3  's_maxRate'
         117  BINARY_MULTIPLY  
         118  RETURN_END_IF    
       119_0  COME_FROM                '108'

 100     119  LOAD_FAST             3  'last'
         122  LOAD_CONST            6  'k'
         125  COMPARE_OP            2  '=='
         128  POP_JUMP_IF_FALSE   139  'to 139'

 102     131  LOAD_FAST             2  'pre'
         134  LOAD_GLOBAL           4  's_xRate'
         137  BINARY_MULTIPLY  
         138  RETURN_END_IF    
       139_0  COME_FROM                '128'

 103     139  LOAD_FAST             3  'last'
         142  LOAD_CONST            7  'g'
         145  COMPARE_OP            2  '=='
         148  POP_JUMP_IF_FALSE   159  'to 159'

 105     151  LOAD_FAST             2  'pre'
         154  LOAD_GLOBAL           5  's_yRate'
         157  BINARY_MULTIPLY  
         158  RETURN_END_IF    
       159_0  COME_FROM                '148'
         159  LOAD_CONST            0  ''
         162  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 38


def get_scale_split--- This code section failed: ---

 109       0  LOAD_GLOBAL           0  'isinstance'
           3  LOAD_FAST             0  's'
           6  LOAD_GLOBAL           1  'int'
           9  CALL_FUNCTION_2       2 
          12  POP_JUMP_IF_TRUE     30  'to 30'
          15  LOAD_GLOBAL           0  'isinstance'
          18  LOAD_FAST             0  's'
          21  LOAD_GLOBAL           2  'float'
          24  CALL_FUNCTION_2       2 
        27_0  COME_FROM                '12'
          27  POP_JUMP_IF_FALSE    34  'to 34'

 110      30  LOAD_FAST             0  's'
          33  RETURN_END_IF    
        34_0  COME_FROM                '27'

 111      34  RETURN_VALUE     
          35  RETURN_VALUE     
          36  RETURN_VALUE     
          37  COMPARE_OP            2  '=='
          40  POP_JUMP_IF_TRUE     52  'to 52'
          43  POP_JUMP_IF_TRUE      2  'to 2'
          46  COMPARE_OP            2  '=='
        49_0  COME_FROM                '43'
        49_1  COME_FROM                '40'
          49  POP_JUMP_IF_FALSE    56  'to 56'

 113      52  LOAD_GLOBAL           3  's_minRate'
          55  RETURN_END_IF    
        56_0  COME_FROM                '49'

 114      56  RETURN_VALUE     
          57  PRINT_ITEM_TO    
          58  PRINT_ITEM_TO    
          59  COMPARE_OP            2  '=='
          62  POP_JUMP_IF_FALSE    69  'to 69'

 116      65  LOAD_GLOBAL           4  's_maxRate'
          68  RETURN_END_IF    
        69_0  COME_FROM                '62'

 117      69  RETURN_VALUE     
          70  RETURN_VALUE     
          71  RETURN_VALUE     
          72  COMPARE_OP            2  '=='
          75  POP_JUMP_IF_FALSE    82  'to 82'

 119      78  LOAD_GLOBAL           5  's_xRate'
          81  RETURN_END_IF    
        82_0  COME_FROM                '75'

 120      82  RETURN_VALUE     
          83  INPLACE_POWER    
          84  INPLACE_POWER    
          85  COMPARE_OP            2  '=='
          88  POP_JUMP_IF_FALSE    95  'to 95'

 122      91  LOAD_GLOBAL           6  's_yRate'
          94  RETURN_END_IF    
        95_0  COME_FROM                '88'

Parse error at or near `RETURN_VALUE' instruction at offset 34


def get_bg_scale(s):
    if isinstance(s, int) or isinstance(s, float):
        return s
    else:
        return mate_utils.calcWinScale(s)


def get_bg_scale_old--- This code section failed: ---

 133       0  LOAD_GLOBAL           0  'tonumber'
           3  LOAD_FAST             0  's'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            1  'ret'

 134      12  LOAD_FAST             1  'ret'
          15  LOAD_CONST            0  ''
          18  COMPARE_OP            9  'is-not'
          21  POP_JUMP_IF_FALSE    28  'to 28'

 135      24  LOAD_FAST             1  'ret'
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

 137      28  LOAD_GLOBAL           0  'tonumber'
          31  LOAD_GLOBAL           1  'None'
          34  LOAD_CONST            2  -1
          37  SLICE+3          
          38  CALL_FUNCTION_1       1 
          41  STORE_FAST            2  'pre'

 138      44  LOAD_FAST             2  'pre'
          47  LOAD_CONST            0  ''
          50  COMPARE_OP            8  'is'
          53  POP_JUMP_IF_FALSE    60  'to 60'

 139      56  LOAD_CONST            0  ''
          59  RETURN_END_IF    
        60_0  COME_FROM                '53'

 141      60  RETURN_VALUE     
          61  RETURN_VALUE     
          62  RETURN_VALUE     
          63  BINARY_SUBSCR    
          64  STORE_FAST            3  'last'

 143      67  LOAD_FAST             3  'last'
          70  LOAD_CONST            3  'w'
          73  COMPARE_OP            2  '=='
          76  POP_JUMP_IF_TRUE     91  'to 91'
          79  LOAD_FAST             3  'last'
          82  LOAD_CONST            4  's'
          85  COMPARE_OP            2  '=='
        88_0  COME_FROM                '76'
          88  POP_JUMP_IF_FALSE    99  'to 99'

 145      91  LOAD_FAST             2  'pre'
          94  LOAD_GLOBAL           2  's_bg_minRate'
          97  BINARY_MULTIPLY  
          98  RETURN_END_IF    
        99_0  COME_FROM                '88'

 146      99  LOAD_FAST             3  'last'
         102  LOAD_CONST            5  'q'
         105  COMPARE_OP            2  '=='
         108  POP_JUMP_IF_FALSE   119  'to 119'

 148     111  LOAD_FAST             2  'pre'
         114  LOAD_GLOBAL           3  's_bg_maxRate'
         117  BINARY_MULTIPLY  
         118  RETURN_END_IF    
       119_0  COME_FROM                '108'

 149     119  LOAD_FAST             3  'last'
         122  LOAD_CONST            6  'k'
         125  COMPARE_OP            2  '=='
         128  POP_JUMP_IF_FALSE   139  'to 139'

 151     131  LOAD_FAST             2  'pre'
         134  LOAD_GLOBAL           4  's_bg_xRate'
         137  BINARY_MULTIPLY  
         138  RETURN_END_IF    
       139_0  COME_FROM                '128'

 152     139  LOAD_FAST             3  'last'
         142  LOAD_CONST            7  'g'
         145  COMPARE_OP            2  '=='
         148  POP_JUMP_IF_FALSE   159  'to 159'

 154     151  LOAD_FAST             2  'pre'
         154  LOAD_GLOBAL           5  's_bg_yRate'
         157  BINARY_MULTIPLY  
         158  RETURN_END_IF    
       159_0  COME_FROM                '148'
         159  LOAD_CONST            0  ''
         162  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 38


def calc_pos(s, parent_length, self_scale=1.0):
    if isinstance(s, (int, float)):
        return s
    else:
        return mate_utils.calcPosition(s, parent_length, self_scale)


def calc_pos_old(s, parent_length, self_scale=None):
    ret = tonumber(s)
    if ret is not None:
        return ret
    else:
        m = re.match('([0-9.-]*)([%\\$]?)(i?)([0-9.-]*)(x?)', s)
        p1, p2, p3, p4, p5 = (
         m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
        offset = 0
        ret = 0
        if p2 == '':
            if p5 == 'x':
                if p3 == 'i':
                    offset = tonumber(p4) * 2
                else:
                    offset = tonumber(p1) * 2
            elif p3 == 'i':
                offset = tonumber(p4)
            else:
                offset = tonumber(p1)
            if p3 == 'i':
                offset = parent_length - offset
        else:
            if p2 == '%':
                ret = parent_length * tonumber(p1) / 100
            elif p2 == '$':
                ret = parent_length * tonumber(p1) / (100 * self_scale)
            if p4 != '':
                if p5 == 'x':
                    offset = tonumber(p4) * 2
                else:
                    offset = tonumber(p4)
                if p3 == 'i':
                    offset = parent_length - offset
        return ret + offset


def pos_need_parent(s):
    return isinstance(s, six.string_types) and re.search('[i\\$%]', s) is not None


def is_raw_ui_object(obj):
    if isinstance(obj, cc.Node):
        return obj.isValid()
    else:
        return False


def is_ui_object(obj):
    from common.uisys.uielment.CCNode import CCNode
    return isinstance(obj, CCNode) and is_raw_ui_object(obj.get())


_plist_table_cache = {}

def GetPlistConf(_plist):
    if not re.search('\\.plist$', _plist):
        return
    else:
        conf = _plist_table_cache.get(_plist)
        if conf is not None:
            return conf
        dict_ = cc.FileUtils.getInstance().getValueMapFromFile(_plist)
        conf = []
        if dict_.get('frames'):
            conf = [ x for x in sorted(six_ex.keys(dict_['frames'])) ]
        _plist_table_cache[_plist] = conf
        return conf


def get_vec2_distance_square(vec2_0, vec2_1):
    x1, y1, x2, y2 = (
     vec2_0.x, vec2_0.y, vec2_1.x, vec2_1.y)
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


def on_window_size_changed():
    global s_visibleSize
    global s_fixDesignResolution
    global s_winSize
    s_winSize = cc.Director.getInstance().getOpenGLView().getFrameSize()
    if global_data.deviceinfo:
        global_data.deviceinfo.refresh_screen_margin_info()
    s_visibleSize = get_visible_size()
    switch_resolution_policy(s_fixDesignResolution)


def switch_resolution_policy(is_fix_design):
    global s_designHeight
    global s_minRate
    global s_yRate
    global s_viewport_scale
    global s_bg_minRate
    global s_fixDesignResolution
    global default_cancel_dist
    global s_designWidth
    global s_showDesignSize
    global s_bg_yRate
    global s_xRate
    global s_bg_maxRate
    global s_bg_xRate
    global s_maxRate
    if is_fix_design:
        s_fixDesignResolution = True
        s_viewport_scale = float(s_winSize.height) / s_designHeight
        mate_utils = cc.MateUtils.getInstance()
        s_winSizeScript = cc.Size(s_winSize.width / s_viewport_scale, s_winSize.height / s_viewport_scale)
        s_visibleSizeScript = cc.Size(s_visibleSize.width / s_viewport_scale, s_visibleSize.height / s_viewport_scale)
        mate_utils.initSizes(s_winSizeScript, s_visibleSizeScript, s_designSize)
    else:
        s_fixDesignResolution = False
        s_viewport_scale = 1.0
        mate_utils = cc.MateUtils.getInstance()
        mate_utils.initSizes(s_winSize, s_visibleSize, s_designSize)
    s_showDesignSize = cc.Size(s_winSize.width / s_viewport_scale, s_designHeight)
    s_minRate = min(s_visibleSize.width / s_designWidth, s_visibleSize.height / s_designHeight) / s_viewport_scale
    s_maxRate = max(s_visibleSize.width / s_designWidth, s_visibleSize.height / s_designHeight) / s_viewport_scale
    s_xRate = s_visibleSize.width / s_designWidth / s_viewport_scale
    s_yRate = s_visibleSize.height / s_designHeight / s_viewport_scale
    s_bg_minRate = min(s_winSize.width / s_designWidth, s_winSize.height / s_designHeight) / s_viewport_scale
    s_bg_maxRate = max(s_winSize.width / s_designWidth, s_winSize.height / s_designHeight) / s_viewport_scale
    s_bg_xRate = s_winSize.width / s_designWidth / s_viewport_scale
    s_bg_yRate = s_winSize.height / s_designHeight / s_viewport_scale
    default_cancel_dist = get_scale('10w')


switch_resolution_policy(True)