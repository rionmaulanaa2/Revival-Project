# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/text_utils.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_cur_name_path
import re
import six
import compat_py2_py3
SAFE_FORMAT_FIELD_PATTERN = re.compile('(\\w+):')

def check_emoji_name(name):
    import re
    if six.PY2 and not isinstance(name, six.text_type):
        try:
            name = name.decode('utf-8')
        except:
            global_data.game_mgr.show_tip(get_text_by_id(10020), True)
            return True

    regex = re.compile(compat_py2_py3.text_utils_emoji_pattern)
    flag = regex.search(name)
    if flag:
        global_data.game_mgr.show_tip(get_text_by_id(191), True)
        return True
    regex = re.compile(compat_py2_py3.text_utils_control_pattern)
    flag = regex.search(name)
    if flag:
        global_data.game_mgr.show_tip(get_text_by_id(190), True)
        return True
    regex = re.compile(compat_py2_py3.text_utils_space_pattern)
    flag = regex.search(name)
    if flag:
        global_data.game_mgr.show_tip(get_text_by_id(10020), True)
        return True
    regex = re.compile(compat_py2_py3.text_utils_other_pattern)
    flag = regex.search(name)
    if flag:
        global_data.game_mgr.show_tip(get_text_by_id(10020), True)
        return True
    return False


def check_review_name(text):
    import game3d
    import json
    if six.PY2 and not isinstance(text, six.text_type):
        try:
            text = text.decode('utf-8')
        except:
            return False

    result = game3d.env_review_nickname(text)
    result = json.loads(result)
    if result['code'] == 200:
        return True
    if result['code'] == 100 and game3d.get_platform() == game3d.PLATFORM_WIN32:
        return True
    return False


ignore_list = [
 '#10', '#23', '#244', '#257', '#37', '#103', '#250']

def check_review_words--- This code section failed: ---

  93       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'game3d'
           9  STORE_FAST            1  'game3d'

  94      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'json'
          21  STORE_FAST            2  'json'

  96      24  LOAD_GLOBAL           2  'six'
          27  LOAD_ATTR             3  'PY2'
          30  POP_JUMP_IF_FALSE    91  'to 91'
          33  LOAD_GLOBAL           4  'isinstance'
          36  LOAD_FAST             0  'text'
          39  LOAD_GLOBAL           2  'six'
          42  LOAD_ATTR             5  'text_type'
          45  CALL_FUNCTION_2       2 
          48  UNARY_NOT        
        49_0  COME_FROM                '30'
          49  POP_JUMP_IF_FALSE    91  'to 91'

  97      52  SETUP_EXCEPT         19  'to 74'

  98      55  LOAD_FAST             0  'text'
          58  LOAD_ATTR             6  'decode'
          61  LOAD_CONST            2  'utf-8'
          64  CALL_FUNCTION_1       1 
          67  STORE_FAST            0  'text'
          70  POP_BLOCK        
          71  JUMP_ABSOLUTE        91  'to 91'
        74_0  COME_FROM                '52'

  99      74  POP_TOP          
          75  POP_TOP          
          76  POP_TOP          

 100      77  LOAD_GLOBAL           7  'False'
          80  LOAD_CONST            3  ''
          83  BUILD_TUPLE_2         2 
          86  RETURN_VALUE     
          87  END_FINALLY      
        88_0  COME_FROM                '87'
          88  JUMP_FORWARD          0  'to 91'
        91_0  COME_FROM                '88'

 102      91  LOAD_FAST             0  'text'
          94  LOAD_ATTR             8  'find'
          97  LOAD_CONST            4  '#$'
         100  CALL_FUNCTION_1       1 
         103  LOAD_CONST            5  -1
         106  COMPARE_OP            3  '!='
         109  POP_JUMP_IF_FALSE   122  'to 122'

 103     112  LOAD_GLOBAL           7  'False'
         115  LOAD_CONST            3  ''
         118  BUILD_TUPLE_2         2 
         121  RETURN_END_IF    
       122_0  COME_FROM                '109'

 105     122  LOAD_GLOBAL           9  'richtext_check'
         125  LOAD_FAST             0  'text'
         128  CALL_FUNCTION_1       1 
         131  UNPACK_SEQUENCE_2     2 
         134  STORE_FAST            3  'flag'
         137  STORE_FAST            0  'text'

 106     140  LOAD_FAST             3  'flag'
         143  POP_JUMP_IF_TRUE    156  'to 156'

 107     146  LOAD_GLOBAL           7  'False'
         149  LOAD_CONST            3  ''
         152  BUILD_TUPLE_2         2 
         155  RETURN_END_IF    
       156_0  COME_FROM                '143'

 109     156  RETURN_VALUE     
         157  PRINT_ITEM_TO    
         158  PRINT_ITEM_TO    
         159  COMPARE_OP            2  '=='
         162  POP_JUMP_IF_FALSE   175  'to 175'

 110     165  LOAD_GLOBAL          10  'True'
         168  LOAD_FAST             0  'text'
         171  BUILD_TUPLE_2         2 
         174  RETURN_END_IF    
       175_0  COME_FROM                '162'

 112     175  LOAD_FAST             1  'game3d'
         178  LOAD_ATTR            11  'env_review_words'
         181  LOAD_GLOBAL          12  'str'
         184  LOAD_CONST            6  1
         187  CALL_FUNCTION_1       1 
         190  LOAD_GLOBAL          12  'str'
         193  LOAD_CONST            6  1
         196  CALL_FUNCTION_1       1 
         199  LOAD_FAST             0  'text'
         202  CALL_FUNCTION_3       3 
         205  STORE_FAST            4  'result'

 113     208  LOAD_FAST             2  'json'
         211  LOAD_ATTR            13  'loads'
         214  LOAD_FAST             4  'result'
         217  CALL_FUNCTION_1       1 
         220  STORE_FAST            4  'result'

 115     223  LOAD_FAST             4  'result'
         226  LOAD_CONST            7  'code'
         229  BINARY_SUBSCR    
         230  LOAD_CONST            8  200
         233  COMPARE_OP            2  '=='
         236  POP_JUMP_IF_FALSE   311  'to 311'

 117     239  LOAD_GLOBAL          14  'global_data'
         242  LOAD_ATTR            15  'player'
         245  POP_JUMP_IF_FALSE   301  'to 301'
         248  LOAD_GLOBAL          14  'global_data'
         251  LOAD_ATTR            15  'player'
         254  LOAD_ATTR            16  'in_speech_control'
         257  CALL_FUNCTION_0       0 
       260_0  COME_FROM                '245'
         260  POP_JUMP_IF_FALSE   301  'to 301'

 118     263  SETUP_LOOP           35  'to 301'
         266  LOAD_GLOBAL          17  'ignore_list'
         269  GET_ITER         
         270  FOR_ITER             24  'to 297'
         273  STORE_FAST            5  'ignore_msg'

 119     276  LOAD_FAST             0  'text'
         279  LOAD_ATTR            18  'replace'
         282  LOAD_FAST             5  'ignore_msg'
         285  LOAD_CONST            3  ''
         288  CALL_FUNCTION_2       2 
         291  STORE_FAST            0  'text'
         294  JUMP_BACK           270  'to 270'
         297  POP_BLOCK        
       298_0  COME_FROM                '263'
         298  JUMP_FORWARD          0  'to 301'
       301_0  COME_FROM                '263'

 121     301  LOAD_GLOBAL          10  'True'
         304  LOAD_FAST             0  'text'
         307  BUILD_TUPLE_2         2 
         310  RETURN_END_IF    
       311_0  COME_FROM                '236'

 123     311  LOAD_GLOBAL           7  'False'
         314  LOAD_CONST            3  ''
         317  BUILD_TUPLE_2         2 
         320  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 156


CHECK_WORDS_NO_PASS = 0
CHECK_WORDS_PASS = 1
CHECK_WORDS_ONLY_SELF = 2

def check_review_words_chat--- This code section failed: ---

 139       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'game3d'
           9  STORE_FAST            2  'game3d'

 140      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'json'
          21  STORE_FAST            3  'json'

 142      24  LOAD_GLOBAL           2  'six'
          27  LOAD_ATTR             3  'PY2'
          30  POP_JUMP_IF_FALSE    94  'to 94'
          33  LOAD_GLOBAL           4  'isinstance'
          36  LOAD_FAST             0  'text'
          39  LOAD_GLOBAL           2  'six'
          42  LOAD_ATTR             5  'text_type'
          45  CALL_FUNCTION_2       2 
          48  UNARY_NOT        
        49_0  COME_FROM                '30'
          49  POP_JUMP_IF_FALSE    94  'to 94'

 143      52  SETUP_EXCEPT         19  'to 74'

 144      55  LOAD_FAST             0  'text'
          58  LOAD_ATTR             6  'decode'
          61  LOAD_CONST            2  'utf-8'
          64  CALL_FUNCTION_1       1 
          67  STORE_FAST            0  'text'
          70  POP_BLOCK        
          71  JUMP_ABSOLUTE        94  'to 94'
        74_0  COME_FROM                '52'

 145      74  POP_TOP          
          75  POP_TOP          
          76  POP_TOP          

 146      77  LOAD_CONST            3  1
          80  LOAD_GLOBAL           7  'CHECK_WORDS_NO_PASS'
          83  LOAD_CONST            4  ''
          86  BUILD_TUPLE_3         3 
          89  RETURN_VALUE     
          90  END_FINALLY      
        91_0  COME_FROM                '90'
          91  JUMP_FORWARD          0  'to 94'
        94_0  COME_FROM                '91'

 148      94  LOAD_FAST             1  'need_check_richtext'
          97  POP_JUMP_IF_FALSE   174  'to 174'

 149     100  LOAD_FAST             0  'text'
         103  LOAD_ATTR             8  'find'
         106  LOAD_CONST            5  '#$'
         109  CALL_FUNCTION_1       1 
         112  LOAD_CONST            6  -1
         115  COMPARE_OP            3  '!='
         118  POP_JUMP_IF_FALSE   134  'to 134'

 150     121  LOAD_CONST            7  2
         124  LOAD_GLOBAL           7  'CHECK_WORDS_NO_PASS'
         127  LOAD_CONST            4  ''
         130  BUILD_TUPLE_3         3 
         133  RETURN_END_IF    
       134_0  COME_FROM                '118'

 152     134  LOAD_GLOBAL           9  'richtext_check'
         137  LOAD_FAST             0  'text'
         140  CALL_FUNCTION_1       1 
         143  UNPACK_SEQUENCE_2     2 
         146  STORE_FAST            4  'flag'
         149  STORE_FAST            0  'text'

 153     152  LOAD_FAST             4  'flag'
         155  POP_JUMP_IF_TRUE    174  'to 174'

 154     158  LOAD_CONST            8  3
         161  LOAD_GLOBAL           7  'CHECK_WORDS_NO_PASS'
         164  LOAD_CONST            4  ''
         167  BUILD_TUPLE_3         3 
         170  RETURN_END_IF    
       171_0  COME_FROM                '155'
         171  JUMP_FORWARD          0  'to 174'
       174_0  COME_FROM                '171'

 156     174  JUMP_FORWARD          4  'to 181'
         177  COMPARE_OP            2  '=='
         180  POP_JUMP_IF_FALSE   196  'to 196'

 157     183  LOAD_CONST            9  4
         186  LOAD_GLOBAL          10  'CHECK_WORDS_PASS'
         189  LOAD_FAST             0  'text'
         192  BUILD_TUPLE_3         3 
         195  RETURN_END_IF    
       196_0  COME_FROM                '180'

 159     196  LOAD_FAST             2  'game3d'
         199  LOAD_ATTR            11  'env_review_words'
         202  LOAD_GLOBAL          12  'str'
         205  LOAD_CONST            3  1
         208  CALL_FUNCTION_1       1 
         211  LOAD_GLOBAL          12  'str'
         214  LOAD_CONST            3  1
         217  CALL_FUNCTION_1       1 
         220  LOAD_FAST             0  'text'
         223  CALL_FUNCTION_3       3 
         226  STORE_FAST            5  'result'

 160     229  LOAD_FAST             3  'json'
         232  LOAD_ATTR            13  'loads'
         235  LOAD_FAST             5  'result'
         238  CALL_FUNCTION_1       1 
         241  STORE_FAST            5  'result'

 161     244  LOAD_FAST             5  'result'
         247  LOAD_CONST           10  'code'
         250  BINARY_SUBSCR    
         251  STORE_FAST            6  'result_code'

 162     254  LOAD_FAST             5  'result'
         257  LOAD_CONST           11  'message'
         260  BINARY_SUBSCR    
         261  STORE_FAST            7  'result_msg'

 163     264  LOAD_FAST             5  'result'
         267  LOAD_ATTR            14  'get'
         270  LOAD_CONST           12  'regularId'
         273  LOAD_CONST            0  ''
         276  CALL_FUNCTION_2       2 
         279  JUMP_IF_TRUE_OR_POP   297  'to 297'
         282  LOAD_FAST             5  'result'
         285  LOAD_ATTR            14  'get'
         288  LOAD_CONST           13  'regularIds'
         291  LOAD_CONST            0  ''
         294  CALL_FUNCTION_2       2 
       297_0  COME_FROM                '279'
         297  STORE_FAST            8  'result_reg_id'

 165     300  LOAD_FAST             6  'result_code'
         303  LOAD_CONST           14  200
         306  COMPARE_OP            2  '=='
         309  POP_JUMP_IF_FALSE   387  'to 387'

 166     312  LOAD_GLOBAL          16  'global_data'
         315  LOAD_ATTR            17  'player'
         318  POP_JUMP_IF_FALSE   374  'to 374'
         321  LOAD_GLOBAL          16  'global_data'
         324  LOAD_ATTR            17  'player'
         327  LOAD_ATTR            18  'in_speech_control'
         330  CALL_FUNCTION_0       0 
       333_0  COME_FROM                '318'
         333  POP_JUMP_IF_FALSE   374  'to 374'

 167     336  SETUP_LOOP           35  'to 374'
         339  LOAD_GLOBAL          19  'ignore_list'
         342  GET_ITER         
         343  FOR_ITER             24  'to 370'
         346  STORE_FAST            9  'ignore_msg'

 168     349  LOAD_FAST             0  'text'
         352  LOAD_ATTR            20  'replace'
         355  LOAD_FAST             9  'ignore_msg'
         358  LOAD_CONST            4  ''
         361  CALL_FUNCTION_2       2 
         364  STORE_FAST            0  'text'
         367  JUMP_BACK           343  'to 343'
         370  POP_BLOCK        
       371_0  COME_FROM                '336'
         371  JUMP_FORWARD          0  'to 374'
       374_0  COME_FROM                '336'

 169     374  LOAD_FAST             6  'result_code'
         377  LOAD_GLOBAL          10  'CHECK_WORDS_PASS'
         380  LOAD_FAST             0  'text'
         383  BUILD_TUPLE_3         3 
         386  RETURN_END_IF    
       387_0  COME_FROM                '309'

 170     387  LOAD_FAST             6  'result_code'
         390  LOAD_CONST           15  206
         393  COMPARE_OP            2  '=='
         396  POP_JUMP_IF_FALSE   418  'to 418'

 171     399  LOAD_FAST             7  'result_msg'
         402  STORE_FAST            0  'text'

 172     405  LOAD_FAST             6  'result_code'
         408  LOAD_GLOBAL          10  'CHECK_WORDS_PASS'
         411  LOAD_FAST             0  'text'
         414  BUILD_TUPLE_3         3 
         417  RETURN_END_IF    
       418_0  COME_FROM                '396'

 173     418  LOAD_FAST             6  'result_code'
         421  LOAD_CONST           16  201
         424  COMPARE_OP            2  '=='
         427  POP_JUMP_IF_FALSE   443  'to 443'

 174     430  LOAD_FAST             6  'result_code'
         433  LOAD_GLOBAL          21  'CHECK_WORDS_ONLY_SELF'
         436  LOAD_FAST             0  'text'
         439  BUILD_TUPLE_3         3 
         442  RETURN_END_IF    
       443_0  COME_FROM                '427'

 177     443  LOAD_FAST             6  'result_code'
         446  LOAD_GLOBAL           7  'CHECK_WORDS_NO_PASS'
         449  LOAD_CONST            4  ''
         452  BUILD_TUPLE_3         3 
         455  RETURN_VALUE     

Parse error at or near `COMPARE_OP' instruction at offset 177


richtext_pattern = re.compile('<(.*?)>')
enable_patterns = [
 re.compile('<size=\\d{1,3}>'),
 re.compile('<align=\\d>'),
 re.compile('<shadow=\\d>'),
 re.compile('<color=0[Xx][\\dabcefABCDEF]{8,8}>'),
 re.compile('<u=0[Xx][\\dabcefABCDEF]{8,8}>'),
 re.compile('<outline=\\d,color=0[Xx][\\dabcefABCDEF]{8,8}>'),
 re.compile('</size>'),
 re.compile('</align>'),
 re.compile('</shadow>'),
 re.compile('</outline>'),
 re.compile('</color>'),
 re.compile('</u>')]
enable_jing_patterns = re.compile('#\\d{1,4}')

def richtext_check(text):
    replace_strs = []
    replace_jing_strs = []
    replace_jin_strs = text.split('#')
    for msg in replace_jin_strs[1:]:
        new_msg = '#' + msg
        if enable_jing_patterns.match(new_msg) is not None:
            replace_jing_strs.append(msg)

    text = text.replace('<', '\xef\xbc\x9c')
    text = text.replace('>', '\xef\xbc\x9e')
    text = text.replace('#', '\xef\xbc\x83')
    for rp_str in replace_strs:
        old_str = '\xef\xbc\x9c' + rp_str + '\xef\xbc\x9e'
        new_str = '<' + rp_str + '>'
        text = text.replace(old_str, new_str)

    for rp_str in replace_jing_strs:
        old_str = '\xef\xbc\x83' + rp_str
        new_str = '#' + rp_str
        text = text.replace(old_str, new_str)

    new_richtext = text
    relink = '<size=(.*?)>'
    item_msg = re.findall(relink, text)
    for msgs in item_msg:
        try:
            size = int(msgs)
        except:
            return (
             False, '')

        if size < 1:
            size = 1
        elif size > 50:
            size = 50
        new_str = '<size=%d>' % size
        old_str = '<size=%s>' % msgs
        new_richtext = new_richtext.replace(old_str, new_str)

    return (True, new_richtext)


def check_text_length--- This code section failed: ---

 252       0  SETUP_EXCEPT         44  'to 47'

 253       3  LOAD_GLOBAL           0  'len'
           6  LOAD_GLOBAL           1  'six'
           9  LOAD_ATTR             2  'text_type'
          12  LOAD_ATTR             1  'six'
          15  CALL_FUNCTION_2       2 
          18  LOAD_ATTR             3  'encode'
          21  LOAD_CONST            2  'gbk'
          24  CALL_FUNCTION_1       1 
          27  CALL_FUNCTION_1       1 
          30  STORE_FAST            2  'len_text'

 254      33  LOAD_FAST             2  'len_text'
          36  LOAD_FAST             1  'length_limit'
          39  COMPARE_OP            1  '<='
          42  RETURN_VALUE     
          43  POP_BLOCK        
          44  JUMP_FORWARD         18  'to 65'
        47_0  COME_FROM                '0'

 255      47  POP_TOP          
          48  POP_TOP          
          49  POP_TOP          

 256      50  LOAD_GLOBAL           4  'log_error'
          53  LOAD_CONST            3  'check text length failed'
          56  CALL_FUNCTION_1       1 
          59  POP_TOP          

 257      60  LOAD_GLOBAL           5  'False'
          63  RETURN_VALUE     
          64  END_FINALLY      
        65_0  COME_FROM                '64'
        65_1  COME_FROM                '44'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15


def get_name_item(sex, conf_name):
    from common.cfg import confmgr
    import random
    name_conf_folder = get_cur_name_path()
    name_list = confmgr.get('%s%s' % (name_conf_folder, conf_name))
    len_names = len(name_list)
    if not name_list:
        return ''
    while name_list and True:
        name_idx = random.randint(0, len_names - 1)
        name_item = name_list[name_idx]
        if int(name_item.get('iGender', 3)) & sex == sex:
            return name_item.get('cName', '')

    return ''


def generate_random_name--- This code section failed: ---

 281       0  LOAD_GLOBAL           0  'get_name_item'
           3  LOAD_GLOBAL           1  'random'
           6  CALL_FUNCTION_2       2 
           9  STORE_FAST            1  'name_item'

 282      12  LOAD_GLOBAL           0  'get_name_item'
          15  LOAD_GLOBAL           2  'shuffle'
          18  CALL_FUNCTION_2       2 
          21  STORE_FAST            2  'title1_item'

 283      24  LOAD_GLOBAL           0  'get_name_item'
          27  LOAD_GLOBAL           3  'choice'
          30  CALL_FUNCTION_2       2 
          33  STORE_FAST            3  'title2_item'

 284      36  LOAD_GLOBAL           0  'get_name_item'
          39  LOAD_GLOBAL           4  'join'
          42  CALL_FUNCTION_2       2 
          45  STORE_FAST            4  'sp_char_item'

 285      48  LOAD_FAST             2  'title1_item'
          51  LOAD_FAST             3  'title2_item'
          54  LOAD_FAST             4  'sp_char_item'
          57  LOAD_FAST             1  'name_item'
          60  BUILD_LIST_4          4 
          63  STORE_FAST            5  'item_list'

 286      66  LOAD_CONST            5  ''
          69  LOAD_CONST            0  ''
          72  IMPORT_NAME           1  'random'
          75  STORE_FAST            6  'random'

 287      78  LOAD_FAST             6  'random'
          81  LOAD_ATTR             2  'shuffle'
          84  LOAD_FAST             5  'item_list'
          87  CALL_FUNCTION_1       1 
          90  POP_TOP          

 288      91  LOAD_FAST             6  'random'
          94  LOAD_ATTR             3  'choice'
          97  LOAD_CONST            5  ''
         100  LOAD_CONST            6  1
         103  LOAD_CONST            7  2
         106  BUILD_LIST_3          3 
         109  CALL_FUNCTION_1       1 
         112  STORE_FAST            7  'idx'

 289     115  LOAD_FAST             5  'item_list'
         118  LOAD_FAST             7  'idx'
         121  SLICE+1          
         122  STORE_FAST            5  'item_list'

 290     125  LOAD_CONST            8  ''
         128  LOAD_ATTR             4  'join'
         131  LOAD_FAST             5  'item_list'
         134  CALL_FUNCTION_1       1 
         137  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def preload_random_name_confs():
    preload_random_name_conf('name')
    preload_random_name_conf('title1')
    preload_random_name_conf('title2')
    preload_random_name_conf('char')


def preload_random_name_conf(conf_name):
    name_conf_folder = get_cur_name_path()
    from common.cfg import confmgr
    confmgr.preload('%s%s' % (name_conf_folder, conf_name))


def unload_random_name_confs():
    unload_random_name_conf('name')
    unload_random_name_conf('title1')
    unload_random_name_conf('title2')
    unload_random_name_conf('char')


def unload_random_name_conf(conf_name):
    name_conf_folder = get_cur_name_path()
    from common.cfg import confmgr
    confmgr.unload('%s%s' % (name_conf_folder, conf_name))


def parse_safe_dict(format_str):
    m = re.findall(SAFE_FORMAT_FIELD_PATTERN, format_str)
    safe_dict = {key:0 for key in m}
    return safe_dict


def safe_format(format_str, data_dict):
    m = re.findall(SAFE_FORMAT_FIELD_PATTERN, format_str)
    safe_dict = {key:data_dict.get(key, 0) for key in m}
    return format_str.format(**safe_dict)


def get_color_str(color, str):
    color_str = '<color={}>{}</color>'
    return color_str.format(color, str)


def remove_rich_tags(text):
    import re
    pattern = re.compile('<[^>]+>')
    return pattern.sub('', text)