# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/check_aim_ui_sprite_color.py
import json
import os.path
import re
import threading

def check_aim_sprite_color():
    from common.uisys.basepanel import MECHA_AIM_UI_LSIT
    from logic.gutils.rgb_hsb_utils import get_hsv_color_list
    hsv_color_dict = get_hsv_color_list()
    from common.uisys.uielment.CCSprite import CCSprite
    from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
    import os.path
    import logic
    res_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'res')
    need_changed_path = set()
    for name in MECHA_AIM_UI_LSIT:
        m = __import__('logic.comsys.mecha_ui.' + name, fromlist=[name])
        panel_config_name = getattr(m, name).PANEL_CONFIG_NAME
        print ('check panel_config_name', panel_config_name)
        panel = global_data.uisystem.load_template_create(panel_config_name)
        nd_list = [panel]
        has_changed = [False]

        def check_node--- This code section failed: ---

  26       0  LOAD_CONST            1  ''
           3  STORE_FAST            1  'png_path'

  27       6  LOAD_GLOBAL           0  'type'
           9  LOAD_FAST             0  'nd'
          12  CALL_FUNCTION_1       1 
          15  LOAD_DEREF            0  'CCSprite'
          18  LOAD_DEREF            1  'CCScale9Sprite'
          21  BUILD_LIST_2          2 
          24  COMPARE_OP            7  'not-in'
          27  POP_JUMP_IF_FALSE    34  'to 34'

  28      30  LOAD_CONST            0  ''
          33  RETURN_END_IF    
        34_0  COME_FROM                '27'

  29      34  LOAD_GLOBAL           1  'hasattr'
          37  LOAD_GLOBAL           2  '_cur_path'
          40  CALL_FUNCTION_2       2 
          43  POP_JUMP_IF_FALSE    67  'to 67'
          46  LOAD_FAST             0  'nd'
          49  LOAD_ATTR             2  '_cur_path'
        52_0  COME_FROM                '43'
          52  POP_JUMP_IF_FALSE    67  'to 67'

  30      55  LOAD_FAST             0  'nd'
          58  LOAD_ATTR             2  '_cur_path'
          61  STORE_FAST            1  'png_path'
          64  JUMP_FORWARD          0  'to 67'
        67_0  COME_FROM                '64'

  31      67  LOAD_GLOBAL           1  'hasattr'
          70  LOAD_GLOBAL           3  '_cur_target_path'
          73  CALL_FUNCTION_2       2 
          76  POP_JUMP_IF_FALSE   100  'to 100'
          79  LOAD_FAST             0  'nd'
          82  LOAD_ATTR             3  '_cur_target_path'
        85_0  COME_FROM                '76'
          85  POP_JUMP_IF_FALSE   100  'to 100'

  32      88  LOAD_FAST             0  'nd'
          91  LOAD_ATTR             3  '_cur_target_path'
          94  STORE_FAST            1  'png_path'
          97  JUMP_FORWARD          0  'to 100'
       100_0  COME_FROM                '97'

  33     100  LOAD_FAST             1  'png_path'
         103  LOAD_DEREF            2  'need_changed_path'
         106  COMPARE_OP            6  'in'
         109  POP_JUMP_IF_FALSE   126  'to 126'

  34     112  LOAD_GLOBAL           4  'True'
         115  LOAD_DEREF            3  'has_changed'
         118  LOAD_CONST            4  ''
         121  STORE_SUBSCR     

  35     122  LOAD_CONST            0  ''
         125  RETURN_END_IF    
       126_0  COME_FROM                '109'

  36     126  LOAD_FAST             1  'png_path'
         129  POP_JUMP_IF_TRUE    136  'to 136'

  37     132  LOAD_CONST            0  ''
         135  RETURN_END_IF    
       136_0  COME_FROM                '129'

  38     136  LOAD_DEREF            4  'res_path'
         139  LOAD_CONST            5  '/'
         142  BINARY_ADD       
         143  LOAD_FAST             1  'png_path'
         146  BINARY_ADD       
         147  STORE_FAST            2  'whole_path'

  39     150  LOAD_GLOBAL           5  'check_sprite_between_white_and_black'
         153  LOAD_FAST             2  'whole_path'
         156  LOAD_DEREF            5  'hsv_color_dict'
         159  CALL_FUNCTION_2       2 
         162  POP_JUMP_IF_TRUE    191  'to 191'

  40     165  LOAD_DEREF            2  'need_changed_path'
         168  LOAD_ATTR             6  'add'
         171  LOAD_FAST             1  'png_path'
         174  CALL_FUNCTION_1       1 
         177  POP_TOP          

  41     178  LOAD_GLOBAL           4  'True'
         181  LOAD_DEREF            3  'has_changed'
         184  LOAD_CONST            4  ''
         187  STORE_SUBSCR     
         188  JUMP_FORWARD          0  'to 191'
       191_0  COME_FROM                '188'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 40

        def check_re(c):
            check_node(c)
            for c_child in c.GetChildren():
                check_re(c_child)

        for nd in nd_list:
            check_re(nd)

        if has_changed[0]:
            import re
            content = ''
            f_name = res_path + '/gui/template/battle_mech/' + panel_config_name[panel_config_name.index('/') + 1:] + '.json'
            with open(f_name, 'r') as f:
                content = f.read()
            f_dic = json.loads(content)

            def check_json_node--- This code section failed: ---

  59       0  LOAD_CONST            1  -1
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'copy'
           9  STORE_FAST            1  'copy'

  60      12  LOAD_FAST             1  'copy'
          15  LOAD_ATTR             1  'deepcopy'
          18  LOAD_FAST             0  'nd_dict'
          21  CALL_FUNCTION_1       1 
          24  STORE_FAST            2  'copyed_nd_dict'

  61      27  LOAD_FAST             2  'copyed_nd_dict'
          30  LOAD_ATTR             2  'update'
          33  BUILD_MAP_1           1 
          36  BUILD_LIST_0          0 
          39  LOAD_CONST            2  'child_list'
          42  STORE_MAP        
          43  CALL_FUNCTION_1       1 
          46  POP_TOP          

  62      47  LOAD_GLOBAL           3  'json'
          50  LOAD_ATTR             4  'dumps'
          53  LOAD_FAST             2  'copyed_nd_dict'
          56  CALL_FUNCTION_1       1 
          59  STORE_FAST            3  'str_json'

  63      62  SETUP_LOOP          103  'to 168'
          65  LOAD_DEREF            0  'need_changed_path'
          68  GET_ITER         
          69  FOR_ITER             95  'to 167'
          72  STORE_FAST            4  'path'

  64      75  LOAD_FAST             4  'path'
          78  LOAD_FAST             3  'str_json'
          81  COMPARE_OP            6  'in'
          84  POP_JUMP_IF_FALSE    69  'to 69'

  65      87  LOAD_FAST             0  'nd_dict'
          90  LOAD_ATTR             5  'get'
          93  LOAD_CONST            3  'userData'
          96  BUILD_MAP_0           0 
          99  CALL_FUNCTION_2       2 
         102  LOAD_ATTR             5  'get'
         105  LOAD_CONST            4  'color_exclude'
         108  LOAD_CONST            5  ''
         111  CALL_FUNCTION_2       2 
         114  POP_JUMP_IF_FALSE   123  'to 123'

  66     117  CONTINUE             69  'to 69'
         120  JUMP_ABSOLUTE       164  'to 164'

  68     123  LOAD_FAST             0  'nd_dict'
         126  LOAD_ATTR             6  'setdefault'
         129  LOAD_CONST            3  'userData'
         132  BUILD_MAP_0           0 
         135  CALL_FUNCTION_2       2 
         138  POP_TOP          

  69     139  POP_TOP          
         140  PRINT_ITEM_TO    
         141  PRINT_ITEM_TO    
         142  BINARY_SUBSCR    
         143  LOAD_ATTR             2  'update'
         146  BUILD_MAP_1           1 
         149  LOAD_CONST            6  1
         152  LOAD_CONST            4  'color_exclude'
         155  STORE_MAP        
         156  CALL_FUNCTION_1       1 
         159  POP_TOP          

  70     160  BREAK_LOOP       
         161  JUMP_BACK            69  'to 69'
         164  JUMP_BACK            69  'to 69'
         167  POP_BLOCK        
       168_0  COME_FROM                '62'

Parse error at or near `POP_TOP' instruction at offset 139

            def check_json_node_re(nd_dict):
                check_json_node(nd_dict)
                child_list = nd_dict.get('child_list', [])
                for c in child_list:
                    check_json_node_re(c)

            check_json_node_re(f_dic)
            with open(f_name, 'w') as f:
                s = json.dumps(f_dic, indent=4, separators=(',', ':'))
                s = s.replace('    ', '\t')
                f.write(s)


def check_sprite_between_white_and_black(path, hsv_color_dict):
    import os.path
    if not os.path.isabs(path):
        import logic
        res_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'res')
        path = res_path + '/' + path
    import subprocess
    from logic.gutils.rgb_hsb_utils import get_hsv_color_name, rgb_2_hsb
    import tools
    cmd = 'python %s\\get_main_color.py %s' % (tools.__path__[0], path)
    c = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    c.wait()
    color = c.stdout.read()
    if color:
        r = compile('color=%s' % color, '<string>', 'exec')
        exec r
        if type(color) is tuple:
            hsv_color = rgb_2_hsb([color[0] / 255.0, color[1] / 255.0, color[2] / 255.0])
            color_name = get_hsv_color_name(hsv_color, hsv_color_dict)
            if color_name in ('white', 'black', 'gray'):
                print (
                 "It's white ", color, color_name)
                return True
        print (
         'Not whilte', path, color)
        return False
    else:
        print (
         'path failed!', path)
        return True


def check_aim_sprite_color():
    from common.uisys.basepanel import MECHA_AIM_UI_LSIT
    from logic.gutils.rgb_hsb_utils import get_hsv_color_list
    hsv_color_dict = get_hsv_color_list()
    from common.uisys.uielment.CCSprite import CCSprite
    from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
    import os.path
    import logic
    res_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'res')
    need_changed_path = set()
    for name in MECHA_AIM_UI_LSIT:
        m = __import__('logic.comsys.mecha_ui.' + name, fromlist=[name])
        panel_config_name = getattr(m, name).PANEL_CONFIG_NAME
        print ('check panel_config_name', panel_config_name)
        panel = global_data.uisystem.load_template_create(panel_config_name)
        nd_list = [panel]
        has_changed = [False]

        def check_node--- This code section failed: ---

 146       0  LOAD_CONST            1  ''
           3  STORE_FAST            1  'png_path'

 147       6  LOAD_GLOBAL           0  'type'
           9  LOAD_FAST             0  'nd'
          12  CALL_FUNCTION_1       1 
          15  LOAD_DEREF            0  'CCSprite'
          18  LOAD_DEREF            1  'CCScale9Sprite'
          21  BUILD_LIST_2          2 
          24  COMPARE_OP            7  'not-in'
          27  POP_JUMP_IF_FALSE    34  'to 34'

 148      30  LOAD_CONST            0  ''
          33  RETURN_END_IF    
        34_0  COME_FROM                '27'

 149      34  LOAD_GLOBAL           1  'hasattr'
          37  LOAD_GLOBAL           2  '_cur_path'
          40  CALL_FUNCTION_2       2 
          43  POP_JUMP_IF_FALSE    67  'to 67'
          46  LOAD_FAST             0  'nd'
          49  LOAD_ATTR             2  '_cur_path'
        52_0  COME_FROM                '43'
          52  POP_JUMP_IF_FALSE    67  'to 67'

 150      55  LOAD_FAST             0  'nd'
          58  LOAD_ATTR             2  '_cur_path'
          61  STORE_FAST            1  'png_path'
          64  JUMP_FORWARD          0  'to 67'
        67_0  COME_FROM                '64'

 151      67  LOAD_GLOBAL           1  'hasattr'
          70  LOAD_GLOBAL           3  '_cur_target_path'
          73  CALL_FUNCTION_2       2 
          76  POP_JUMP_IF_FALSE   100  'to 100'
          79  LOAD_FAST             0  'nd'
          82  LOAD_ATTR             3  '_cur_target_path'
        85_0  COME_FROM                '76'
          85  POP_JUMP_IF_FALSE   100  'to 100'

 152      88  LOAD_FAST             0  'nd'
          91  LOAD_ATTR             3  '_cur_target_path'
          94  STORE_FAST            1  'png_path'
          97  JUMP_FORWARD          0  'to 100'
       100_0  COME_FROM                '97'

 153     100  LOAD_FAST             1  'png_path'
         103  LOAD_DEREF            2  'need_changed_path'
         106  COMPARE_OP            6  'in'
         109  POP_JUMP_IF_FALSE   126  'to 126'

 154     112  LOAD_GLOBAL           4  'True'
         115  LOAD_DEREF            3  'has_changed'
         118  LOAD_CONST            4  ''
         121  STORE_SUBSCR     

 155     122  LOAD_CONST            0  ''
         125  RETURN_END_IF    
       126_0  COME_FROM                '109'

 156     126  LOAD_FAST             1  'png_path'
         129  POP_JUMP_IF_TRUE    136  'to 136'

 157     132  LOAD_CONST            0  ''
         135  RETURN_END_IF    
       136_0  COME_FROM                '129'

 158     136  LOAD_DEREF            4  'res_path'
         139  LOAD_CONST            5  '/'
         142  BINARY_ADD       
         143  LOAD_FAST             1  'png_path'
         146  BINARY_ADD       
         147  STORE_FAST            2  'whole_path'

 159     150  LOAD_GLOBAL           5  'check_sprite_between_white_and_black'
         153  LOAD_FAST             2  'whole_path'
         156  LOAD_DEREF            5  'hsv_color_dict'
         159  CALL_FUNCTION_2       2 
         162  POP_JUMP_IF_TRUE    191  'to 191'

 160     165  LOAD_DEREF            2  'need_changed_path'
         168  LOAD_ATTR             6  'add'
         171  LOAD_FAST             1  'png_path'
         174  CALL_FUNCTION_1       1 
         177  POP_TOP          

 161     178  LOAD_GLOBAL           4  'True'
         181  LOAD_DEREF            3  'has_changed'
         184  LOAD_CONST            4  ''
         187  STORE_SUBSCR     
         188  JUMP_FORWARD          0  'to 191'
       191_0  COME_FROM                '188'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 40

        def check_re(c):
            check_node(c)
            for c_child in c.GetChildren():
                check_re(c_child)

        for nd in nd_list:
            check_re(nd)

        if has_changed[0]:
            import re
            content = ''
            f_name = res_path + '/gui/template/battle_mech/' + panel_config_name[panel_config_name.index('/') + 1:] + '.json'
            with open(f_name, 'r') as f:
                content = f.read()
            f_dic = json.loads(content)

            def check_json_node--- This code section failed: ---

 179       0  LOAD_CONST            1  -1
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'copy'
           9  STORE_FAST            1  'copy'

 180      12  LOAD_FAST             1  'copy'
          15  LOAD_ATTR             1  'deepcopy'
          18  LOAD_FAST             0  'nd_dict'
          21  CALL_FUNCTION_1       1 
          24  STORE_FAST            2  'copyed_nd_dict'

 181      27  LOAD_FAST             2  'copyed_nd_dict'
          30  LOAD_ATTR             2  'update'
          33  BUILD_MAP_1           1 
          36  BUILD_LIST_0          0 
          39  LOAD_CONST            2  'child_list'
          42  STORE_MAP        
          43  CALL_FUNCTION_1       1 
          46  POP_TOP          

 182      47  LOAD_GLOBAL           3  'json'
          50  LOAD_ATTR             4  'dumps'
          53  LOAD_FAST             2  'copyed_nd_dict'
          56  CALL_FUNCTION_1       1 
          59  STORE_FAST            3  'str_json'

 183      62  SETUP_LOOP          103  'to 168'
          65  LOAD_DEREF            0  'need_changed_path'
          68  GET_ITER         
          69  FOR_ITER             95  'to 167'
          72  STORE_FAST            4  'path'

 184      75  LOAD_FAST             4  'path'
          78  LOAD_FAST             3  'str_json'
          81  COMPARE_OP            6  'in'
          84  POP_JUMP_IF_FALSE    69  'to 69'

 185      87  LOAD_FAST             0  'nd_dict'
          90  LOAD_ATTR             5  'get'
          93  LOAD_CONST            3  'userData'
          96  BUILD_MAP_0           0 
          99  CALL_FUNCTION_2       2 
         102  LOAD_ATTR             5  'get'
         105  LOAD_CONST            4  'color_exclude'
         108  LOAD_CONST            5  ''
         111  CALL_FUNCTION_2       2 
         114  POP_JUMP_IF_FALSE   123  'to 123'

 186     117  CONTINUE             69  'to 69'
         120  JUMP_ABSOLUTE       164  'to 164'

 188     123  LOAD_FAST             0  'nd_dict'
         126  LOAD_ATTR             6  'setdefault'
         129  LOAD_CONST            3  'userData'
         132  BUILD_MAP_0           0 
         135  CALL_FUNCTION_2       2 
         138  POP_TOP          

 189     139  POP_TOP          
         140  PRINT_ITEM_TO    
         141  PRINT_ITEM_TO    
         142  BINARY_SUBSCR    
         143  LOAD_ATTR             2  'update'
         146  BUILD_MAP_1           1 
         149  LOAD_CONST            6  1
         152  LOAD_CONST            4  'color_exclude'
         155  STORE_MAP        
         156  CALL_FUNCTION_1       1 
         159  POP_TOP          

 190     160  BREAK_LOOP       
         161  JUMP_BACK            69  'to 69'
         164  JUMP_BACK            69  'to 69'
         167  POP_BLOCK        
       168_0  COME_FROM                '62'

Parse error at or near `POP_TOP' instruction at offset 139

            def check_json_node_re(nd_dict):
                check_json_node(nd_dict)
                child_list = nd_dict.get('child_list', [])
                for c in child_list:
                    check_json_node_re(c)

            check_json_node_re(f_dic)
            with open(f_name, 'w') as f:
                s = json.dumps(f_dic, indent=4, separators=(',', ':'))
                s = s.replace('    ', '\t')
                f.write(s)