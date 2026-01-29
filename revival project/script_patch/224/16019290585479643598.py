# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_richtext.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from cocosui import ccui
TOUCH_EVENT_ENDED = 2
ColorDict = {'w': '<color=0xf3fafeff>',
   'r': '<color=0xe0382fff>','g': '<color=0x12ff00ff>','zy': '<color=0x0bb103ff>',
   'bl': '<color=0x8da5c3ff>','y': '<color=0xffea00ff>','b': '<color=0x009cffff>',
   'p': '<color=0xf223ffff>','c': '<color=0x03f0ffff>','b2': '<color=0x85feffff>',
   'j': '<color=0xff4223ff>','o': '<color=0xff9c00ff>','a': '<color=0xce6912ff>',
   'd': '<color=0x10868aff>','n': '</color>'}
c_color_table = {'SW': 16711679,
   'SC': 6320260,'SQ': 2962499,'SD': 13030107,'SH': 8688543,'SB': 46078,'SG': 1897083,'SL': 12713760,
   'SY': 16764224,'PY': 16757003,'SO': 16747047,'SR': 16000337,'SP': 16538819,'SS': 1645604,'SK': 1645604,
   'BW': 16711679,'BC': 3882828,'BQ': 49870,'BD': 6320260,'BH': 8688543,'BB': 2059438,'BS': 49870,
   'BG': 2144644,'BY': 16764224,'BO': 16745242,'BR': 13710422,'BP': 8006542,'BK': 1645604,'DW': 16777215,
   'DC': 13030107,'DQ': 16711679,'DD': 9017770,'DH': 6320260,'DB': 1176831,'DS': 4034515,'DG': 2144644,
   'DY': 16496384,'DO': 16749338,'DR': 13710422,'DP': 11950008,'DK': 1645604,'FA': 10136520,'FB': 13164751,
   'FC': 13030364,'FD': 15659007,'FE': 3217799,'FF': 2840501,'FG': 4225460,'FH': 626679,'FI': 851963,
   'FP': 8212187,'FK': 6701681,'FL': 12525312,'FM': 16724627,'FN': 16711931,'FO': 16770050,'FR': 14417151,
   'FS': 2369887}
ColorDict.update([ (shorthand.lower(), '<color=0x%06xff>' % color_val) for shorthand, color_val in six.iteritems(c_color_table) ])
try:
    if six.PY3:
        import json as json2
    else:
        import json2
    import C_file
    s = C_file.get_res_file('confs/emote.json', '')
    emot_dict = json2.loads(s)
    EMOT_CONF = emot_dict['emote']
except Exception as e:
    print('[patch rich text] read emot exception:', str(e))
    EMOT_CONF = {}

def get_color_text--- This code section failed: ---

  51       0  LOAD_GLOBAL           0  'min'
           3  LOAD_GLOBAL           1  'len'
           6  LOAD_FAST             0  'smsg'
           9  CALL_FUNCTION_1       1 
          12  LOAD_CONST            1  2
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'max_length'

  52      21  SETUP_LOOP           80  'to 104'
          24  LOAD_GLOBAL           2  'range'
          27  LOAD_FAST             1  'max_length'
          30  LOAD_CONST            2  ''
          33  LOAD_CONST            3  -1
          36  CALL_FUNCTION_3       3 
          39  GET_ITER         
          40  FOR_ITER             60  'to 103'
          43  STORE_FAST            2  'i'

  53      46  STORE_FAST            2  'i'
          49  LOAD_FAST             2  'i'
          52  SLICE+3          
          53  STORE_FAST            3  'key'

  54      56  LOAD_GLOBAL           3  'ColorDict'
          59  LOAD_ATTR             4  'get'
          62  LOAD_FAST             3  'key'
          65  LOAD_ATTR             5  'lower'
          68  CALL_FUNCTION_0       0 
          71  LOAD_CONST            0  ''
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            4  'color'

  55      80  LOAD_FAST             4  'color'
          83  POP_JUMP_IF_FALSE    40  'to 40'

  56      86  LOAD_FAST             4  'color'
          89  LOAD_FAST             0  'smsg'
          92  LOAD_FAST             2  'i'
          95  SLICE+1          
          96  BUILD_TUPLE_2         2 
          99  RETURN_END_IF    
       100_0  COME_FROM                '83'
         100  JUMP_BACK            40  'to 40'
         103  POP_BLOCK        
       104_0  COME_FROM                '21'

  57     104  LOAD_CONST            0  ''
         107  LOAD_FAST             0  'smsg'
         110  BUILD_TUPLE_2         2 
         113  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 46


def get_emote_text--- This code section failed: ---

  61       0  LOAD_GLOBAL           0  'min'
           3  LOAD_GLOBAL           1  'len'
           6  LOAD_FAST             0  'smsg'
           9  CALL_FUNCTION_1       1 
          12  LOAD_CONST            1  3
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'max_length'

  62      21  SETUP_LOOP           74  'to 98'
          24  LOAD_GLOBAL           2  'range'
          27  LOAD_FAST             1  'max_length'
          30  LOAD_CONST            2  ''
          33  LOAD_CONST            3  -1
          36  CALL_FUNCTION_3       3 
          39  GET_ITER         
          40  FOR_ITER             54  'to 97'
          43  STORE_FAST            2  'i'

  63      46  STORE_FAST            2  'i'
          49  LOAD_FAST             2  'i'
          52  SLICE+3          
          53  STORE_FAST            3  'key'

  64      56  LOAD_GLOBAL           3  'EMOT_CONF'
          59  LOAD_ATTR             4  'get'
          62  LOAD_FAST             3  'key'
          65  LOAD_CONST            0  ''
          68  CALL_FUNCTION_2       2 
          71  STORE_FAST            4  'num'

  65      74  LOAD_FAST             4  'num'
          77  POP_JUMP_IF_FALSE    40  'to 40'

  66      80  LOAD_FAST             4  'num'
          83  LOAD_FAST             0  'smsg'
          86  LOAD_FAST             2  'i'
          89  SLICE+1          
          90  BUILD_TUPLE_2         2 
          93  RETURN_END_IF    
        94_0  COME_FROM                '77'
          94  JUMP_BACK            40  'to 40'
          97  POP_BLOCK        
        98_0  COME_FROM                '21'

  67      98  LOAD_CONST            0  ''
         101  LOAD_FAST             0  'smsg'
         104  BUILD_TUPLE_2         2 
         107  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 46


def format_richtext(mstr):
    textlist = mstr.split('#')
    str_list = []
    str_list.append(textlist[0])
    for smsg in textlist[1:]:
        if len(smsg) == 0:
            str_list.append('#')
            continue
        str1, str2 = get_color_text(smsg)
        if str1:
            str_list.append(str1)
        else:
            str1, str2 = get_emote_text(smsg)
            if str1:
                pass
            else:
                str_list.append('#')
        str_list.append(str2)

    mstr = ''.join(str_list)
    return mstr


def richtext(rstr, fontSize, size, fontFile='gui/fonts/fzy4jw.ttf', callback=None):
    try:
        rstr = format_richtext(rstr)
        from patch.patch_lang import get_multi_lang_instane
        fontFile = get_multi_lang_instane().get_multi_lang_font_name(fontFile)
        rt = ccui.RichText.create(rstr, fontFile, fontSize, size)
        if callback:

            def testTouch(element, touch, eventTouch):
                if eventTouch.getEventCode() == TOUCH_EVENT_ENDED:
                    callback(element.getTouchString())

            rt.setTouchEnabled(True)
            rt.setSwallowTouches(False)
            rt.addElementTouchEventListener(testTouch)
        return rt
    except Exception as e:
        print('[patch rich text] richtext create exception:', str(e))
        return None

    return None


# global ColorDict ## Warning: Unused global