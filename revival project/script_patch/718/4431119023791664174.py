# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCRichText.py
from __future__ import absolute_import
from six.moves import range
import six
from common.uisys.ui_proxy import ProxyClass
from common.utils.cocos_utils import ccc4FromHex, CCSize
from cocosui import cc, ccui
import common.input.touch
from .CCNode import CCNodeCreator
from .CCUIWidget import CCUIWidget
from common.cfg import confmgr
from common.utils.ui_utils import get_scale, calc_pos
from common.uisys.color_table import get_color_val
from logic.gcommon.common_utils.local_text import get_cur_lang_shrink_setting, get_lang_shrink_font_size, get_extra_vertical_space, get_enable_def_linebreak
from common.uisys.font_utils import GetMultiLangFontName
from logic.client.const.ui_const import TH_SEP_UTF_8
import re
from logic.gutils.rich_text_utils import check_has_custom_node, preprocess_custom_node_text, place_custom_node
ColorDict = {'w': '<color=0xf3fafeff>',
   'r': '<color=0xe0382fff>',
   'g': '<color=0x12ff00ff>',
   'zy': '<color=0x0bb103ff>',
   'bl': '<color=0x8da5c3ff>',
   'y': '<color=0xffea00ff>',
   'b': '<color=0x009cffff>',
   'p': '<color=0xf223ffff>',
   'c': '<color=0x03f0ffff>',
   'b2': '<color=0x85feffff>',
   'j': '<color=0xff4223ff>',
   'o': '<color=0xff9c00ff>',
   'a': '<color=0xce6912ff>',
   'd': '<color=0x10868aff>',
   'n': '</color>'
   }
from data import c_color_table
ColorDict.update([ (shorthand.lower(), '<color=0x%06xff>' % color_val) for shorthand, color_val in six.iteritems(c_color_table.data) ])

def get_color_text--- This code section failed: ---

  57       0  LOAD_GLOBAL           0  'min'
           3  LOAD_GLOBAL           1  'len'
           6  LOAD_FAST             0  'smsg'
           9  CALL_FUNCTION_1       1 
          12  LOAD_CONST            1  2
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'max_length'

  58      21  SETUP_LOOP           80  'to 104'
          24  LOAD_GLOBAL           2  'range'
          27  LOAD_FAST             1  'max_length'
          30  LOAD_CONST            2  ''
          33  LOAD_CONST            3  -1
          36  CALL_FUNCTION_3       3 
          39  GET_ITER         
          40  FOR_ITER             60  'to 103'
          43  STORE_FAST            2  'i'

  59      46  STORE_FAST            2  'i'
          49  LOAD_FAST             2  'i'
          52  SLICE+3          
          53  STORE_FAST            3  'key'

  60      56  LOAD_GLOBAL           3  'ColorDict'
          59  LOAD_ATTR             4  'get'
          62  LOAD_FAST             3  'key'
          65  LOAD_ATTR             5  'lower'
          68  CALL_FUNCTION_0       0 
          71  LOAD_CONST            0  ''
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            4  'color'

  61      80  LOAD_FAST             4  'color'
          83  POP_JUMP_IF_FALSE    40  'to 40'

  62      86  LOAD_FAST             4  'color'
          89  LOAD_FAST             0  'smsg'
          92  LOAD_FAST             2  'i'
          95  SLICE+1          
          96  BUILD_TUPLE_2         2 
          99  RETURN_END_IF    
       100_0  COME_FROM                '83'
         100  JUMP_BACK            40  'to 40'
         103  POP_BLOCK        
       104_0  COME_FROM                '21'

  63     104  LOAD_CONST            0  ''
         107  LOAD_FAST             0  'smsg'
         110  BUILD_TUPLE_2         2 
         113  RETURN_VALUE     

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
                str_list.append(str1)
            else:
                str_list.append('#')
        str_list.append(str2)

    mstr = ''.join(str_list)
    new_richtext = mstr
    relink = '<size=(.*?)>'
    item_msg = re.findall(relink, mstr)
    for msgs in item_msg:
        try:
            size = int(msgs)
        except:
            size = 30

        if size < 1 or size > 50:
            size = max(min(size, 1), 50)
            new_str = '<size=%d>' % size
            old_str = '<size=%s>' % msgs
            new_richtext = new_richtext.replace(old_str, new_str)

    return new_richtext


def richtext_to_str--- This code section failed: ---

 109       0  LOAD_FAST             0  'text'
           3  STORE_FAST            1  'rich_text'

 110       6  LOAD_CONST            1  '#g<touch=(.*?)>(.*?)</touch>#n'
           9  STORE_FAST            2  'relink'

 111      12  LOAD_GLOBAL           0  're'
          15  LOAD_ATTR             1  'findall'
          18  LOAD_FAST             2  'relink'
          21  LOAD_FAST             1  'rich_text'
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            3  'arg_list'

 112      30  SETUP_LOOP          144  'to 177'
          33  LOAD_FAST             3  'arg_list'
          36  GET_ITER         
          37  FOR_ITER            136  'to 176'
          40  STORE_FAST            4  'arg'

 113      43  LOAD_FAST             1  'rich_text'
          46  LOAD_ATTR             2  'replace'
          49  LOAD_CONST            2  '#g<touch=%s>'
          52  LOAD_FAST             4  'arg'
          55  LOAD_CONST            3  ''
          58  BINARY_SUBSCR    
          59  BINARY_MODULO    
          60  LOAD_CONST            4  '['
          63  CALL_FUNCTION_2       2 
          66  STORE_FAST            1  'rich_text'

 114      69  LOAD_FAST             1  'rich_text'
          72  LOAD_ATTR             2  'replace'
          75  LOAD_CONST            5  '</touch>#n'
          78  LOAD_CONST            6  ']'
          81  CALL_FUNCTION_2       2 
          84  STORE_FAST            1  'rich_text'

 115      87  LOAD_CONST            7  '<u=(.*?)>(.*?)</u>'
          90  STORE_FAST            2  'relink'

 116      93  LOAD_GLOBAL           0  're'
          96  LOAD_ATTR             1  'findall'
          99  LOAD_FAST             2  'relink'
         102  LOAD_FAST             4  'arg'
         105  LOAD_CONST            8  1
         108  BINARY_SUBSCR    
         109  CALL_FUNCTION_2       2 
         112  STORE_FAST            5  'text_list'

 117     115  SETUP_LOOP           55  'to 173'
         118  LOAD_FAST             5  'text_list'
         121  GET_ITER         
         122  FOR_ITER             47  'to 172'
         125  STORE_FAST            0  'text'

 118     128  LOAD_FAST             1  'rich_text'
         131  LOAD_ATTR             2  'replace'
         134  LOAD_CONST            9  '<u=%s>'
         137  LOAD_CONST            3  ''
         140  BINARY_SUBSCR    
         141  BINARY_MODULO    
         142  LOAD_CONST           10  ''
         145  CALL_FUNCTION_2       2 
         148  STORE_FAST            1  'rich_text'

 119     151  LOAD_FAST             1  'rich_text'
         154  LOAD_ATTR             2  'replace'
         157  LOAD_CONST           11  '</u>'
         160  LOAD_CONST           10  ''
         163  CALL_FUNCTION_2       2 
         166  STORE_FAST            1  'rich_text'
         169  JUMP_BACK           122  'to 122'
         172  POP_BLOCK        
       173_0  COME_FROM                '115'
         173  JUMP_BACK            37  'to 37'
         176  POP_BLOCK        
       177_0  COME_FROM                '30'

 120     177  LOAD_FAST             1  'rich_text'
         180  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 145


def get_emote_text--- This code section failed: ---

 124       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'emote'
           9  LOAD_CONST            1  'emote'
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'emote_dict'

 125      18  LOAD_GLOBAL           2  'min'
          21  LOAD_GLOBAL           3  'len'
          24  LOAD_FAST             0  'smsg'
          27  CALL_FUNCTION_1       1 
          30  LOAD_CONST            2  3
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            2  'max_length'

 126      39  SETUP_LOOP           74  'to 116'
          42  LOAD_GLOBAL           4  'range'
          45  LOAD_FAST             2  'max_length'
          48  LOAD_CONST            3  ''
          51  LOAD_CONST            4  -1
          54  CALL_FUNCTION_3       3 
          57  GET_ITER         
          58  FOR_ITER             54  'to 115'
          61  STORE_FAST            3  'i'

 127      64  STORE_FAST            3  'i'
          67  LOAD_FAST             3  'i'
          70  SLICE+3          
          71  STORE_FAST            4  'key'

 128      74  LOAD_FAST             1  'emote_dict'
          77  LOAD_ATTR             1  'get'
          80  LOAD_FAST             4  'key'
          83  LOAD_CONST            0  ''
          86  CALL_FUNCTION_2       2 
          89  STORE_FAST            5  'num'

 129      92  LOAD_FAST             5  'num'
          95  POP_JUMP_IF_FALSE    58  'to 58'

 130      98  LOAD_FAST             5  'num'
         101  LOAD_FAST             0  'smsg'
         104  LOAD_FAST             3  'i'
         107  SLICE+1          
         108  BUILD_TUPLE_2         2 
         111  RETURN_END_IF    
       112_0  COME_FROM                '95'
         112  JUMP_BACK            58  'to 58'
         115  POP_BLOCK        
       116_0  COME_FROM                '39'

 131     116  LOAD_CONST            0  ''
         119  LOAD_FAST             0  'smsg'
         122  BUILD_TUPLE_2         2 
         125  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 64


hAlign_anchor_dict = {ccui.RICHTEXT_HORIZONTAL_ALIGN_TYPE_LEFT: 0,
   ccui.RICHTEXT_HORIZONTAL_ALIGN_TYPE_CENTER: 0.5,
   ccui.RICHTEXT_HORIZONTAL_ALIGN_TYPE_RIGHT: 1
   }

@ProxyClass(ccui.RichText)
class CCRichText(CCUIWidget):

    def __init__(self, node):
        super(CCRichText, self).__init__(node)
        self._rstr = ''
        self._fontSize = 25
        self._size = cc.Size(0, 0)
        self._fontFile = 'gui/fonts/fzy4jw.ttf'
        self._callback = None
        self._align = None
        self._text_color = None
        self._needUpdate = False
        return

    @classmethod
    def Create(cls, rstr, fontSize, size, fontFile='gui/fonts/fzy4jw.ttf', color4b=None, callback=None, fontTrans=True, addition_spacing=0):
        rstr = CCRichText.GetMultiLangString(rstr)
        rstr = format_richtext(rstr)
        real_rstr = rstr
        if check_has_custom_node(rstr):
            rstr, mapping_dict = preprocess_custom_node_text(rstr)
        else:
            mapping_dict = {}
        fontSize = get_lang_shrink_font_size(fontSize)
        fontFile = GetMultiLangFontName(fontFile.lower(), fontTrans)
        if not color4b:
            self = cls(cls.create(rstr, fontFile, fontSize, size))
        else:
            self = cls(cls.create(rstr, fontFile, fontSize, size, color4b))
        self.SetCallback(callback)
        CCRichText.RecordRichTextSprite(self, rstr)
        extra_spacing = get_extra_vertical_space()
        self._vertical_spacing = addition_spacing + extra_spacing
        if self._vertical_spacing != 0:
            self.setVerticalSpace(self._vertical_spacing)
        if not get_enable_def_linebreak():
            self.setLineBreakWithoutSpace(True)
        self._rstr = real_rstr
        self._fontSize = fontSize
        self._size = size
        self._fontFile = fontFile
        self._text_color = color4b
        self._callback = callback
        if self.CheckAutoShrinkFont():
            if not global_data.feature_mgr.is_support_boundary_word() and not get_enable_def_linebreak():
                rstr = re.sub(TH_SEP_UTF_8, '', rstr)
            self.setString(rstr)
            self._needUpdate = False
        if mapping_dict:
            place_custom_node(self, mapping_dict)
        return self

    def csb_init(self):
        super(CCRichText, self).csb_init()
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self._minFontSize = lang_shrink_setting.iMinFontSize
        if not get_enable_def_linebreak():
            self.setLineBreakWithoutSpace(True)
        self._vertical_spacing = self.getVerticalSpace()
        self.CheckAutoShrinkFont()

    def GetString(self):
        return self._rstr

    def SetString(self, rstr, need_update_child=True):
        rstr = CCRichText.GetMultiLangString(rstr)
        rstr = format_richtext(rstr)
        if not global_data.feature_mgr.is_support_boundary_word() and not get_enable_def_linebreak():
            rstr = re.sub(TH_SEP_UTF_8, '', rstr)
        CCRichText.RecordRichTextSprite(self, rstr)
        old_has_custom = check_has_custom_node(self._rstr)
        if not check_has_custom_node(rstr):
            self._obj.setString(rstr)
            self._rstr = rstr
        else:
            show_rich_text, mapping_dict = preprocess_custom_node_text(rstr)
            self._obj.setString(show_rich_text)
            self._rstr = rstr
            place_custom_node(self, mapping_dict)
        if old_has_custom:
            self.formatText()
        self._needUpdate = False
        if need_update_child:
            self.UpdateAutoFitChild()

    def GetTextContentSize(self):
        extra_spacing = get_extra_vertical_space()
        sz = self.getTextContentSize()
        heights = self.getLineHeights()
        sz.height += len(heights) * self._vertical_spacing
        return sz

    def SetCallback(self, callback):
        if callback:

            def testTouch(element, touch, eventTouch):
                if eventTouch.getEventCode() == common.input.touch.TOUCH_EVENT_ENDED:
                    callback(element.getTouchString(), element, touch, eventTouch)

            self.setTouchEnabled(True)
            self.setSwallowTouches(False)
            self.addElementTouchEventListener(testTouch)

    def SetHorizontalAlign(self, align):
        self._align = align
        self.setHorizontalAlign(align)

    def GetRichTextColor(self, color_str, opacity):
        global ColorDict
        opacity_str = '%X' % opacity
        color_str = ColorDict.get(color_str, color_str)
        return '0x' + color_str + opacity_str

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color_val = get_color_val(color)
        else:
            color_val = color
        color4b = ccc4FromHex(color_val, 255)
        self.setTextColor(color4b)

    def EnableOutline(self, enable, color, opacity, width):
        if enable:
            if isinstance(color, (str, six.text_type)):
                color = get_color_val(color)
            color4b = ccc4FromHex(color, opacity)
            self.enableOutline(color4b, width)
        else:
            self.enableOutline(ccc4FromHex(0), -1)
        self._needUpdate = True

    def EnableShadow(self, enable, color, opacity, size):
        if isinstance(color, (str, six.text_type)):
            color = get_color_val(color)
        color4b = ccc4FromHex(color, opacity)
        self.enableShadow(enable, color4b, size)
        self._needUpdate = True

    @staticmethod
    def GetMultiLangString(text):
        if isinstance(text, int):
            text_id = text
            text = get_text_local_content(text_id)
        return text

    def CheckAutoShrinkFont(self):
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self.setEnableFontSizeAutoShrink(lang_shrink_setting.bEnableShrink, lang_shrink_setting.iMinFontSize)
        return lang_shrink_setting.bEnableShrink

    def IsNeedUpdate(self):
        return self._needUpdate

    def SetStringWithAdapt(self, s, min_size=(0, 0)):
        self.SetString(s, False)
        self.formatText()
        size = self.getTextContentSize()
        width = max(size.width, min_size[0])
        height = max(size.height, min_size[1])
        self.ChildResizeAndPositionWithSize(width, height)

    def SetStringWithAutoFitAdapt(self, s, min_size=(0, 0)):
        self.SetString(s)
        self.UpdateAutoFitChild(min_size)

    def UpdateAutoFitChild--- This code section failed: ---

 334       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'GetChildren'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  'children'

 335      12  LOAD_FAST             2  'children'
          15  POP_JUMP_IF_TRUE     22  'to 22'

 336      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 337      22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             1  'formatText'
          28  CALL_FUNCTION_0       0 
          31  POP_TOP          

 338      32  LOAD_GLOBAL           2  'getattr'
          35  LOAD_GLOBAL           1  'formatText'
          38  CALL_FUNCTION_2       2 
          41  POP_JUMP_IF_FALSE    65  'to 65'
          44  LOAD_FAST             0  'self'
          47  LOAD_ATTR             3  'nd_auto_fit'
        50_0  COME_FROM                '41'
          50  POP_JUMP_IF_FALSE    65  'to 65'

 339      53  LOAD_FAST             0  'self'
          56  LOAD_ATTR             3  'nd_auto_fit'
          59  STORE_FAST            3  'nd_auto_fit'
          62  JUMP_FORWARD          6  'to 71'

 341      65  LOAD_CONST            0  ''
          68  STORE_FAST            3  'nd_auto_fit'
        71_0  COME_FROM                '62'

 342      71  SETUP_LOOP          293  'to 367'
          74  LOAD_FAST             2  'children'
          77  GET_ITER         
          78  FOR_ITER            285  'to 366'
          81  STORE_FAST            4  'child'

 343      84  LOAD_FAST             3  'nd_auto_fit'
          87  LOAD_FAST             4  'child'
          90  COMPARE_OP            3  '!='
          93  POP_JUMP_IF_FALSE   109  'to 109'

 344      96  LOAD_FAST             4  'child'
          99  LOAD_ATTR             5  'ResizeAndPosition'
         102  CALL_FUNCTION_0       0 
         105  POP_TOP          
         106  JUMP_BACK            78  'to 78'

 346     109  LOAD_FAST             0  'self'
         112  LOAD_ATTR             6  'GetTextContentSize'
         115  CALL_FUNCTION_0       0 
         118  STORE_FAST            5  'size'

 347     121  LOAD_FAST             0  'self'
         124  LOAD_ATTR             7  'getContentSize'
         127  CALL_FUNCTION_0       0 
         130  STORE_FAST            6  'parent_sz'

 348     133  LOAD_FAST             0  'self'
         136  LOAD_ATTR             8  '_align'
         139  LOAD_CONST            0  ''
         142  COMPARE_OP            8  'is'
         145  POP_JUMP_IF_FALSE   166  'to 166'

 349     148  LOAD_FAST             0  'self'
         151  LOAD_ATTR             9  'getHorizontalAlign'
         154  CALL_FUNCTION_0       0 
         157  LOAD_FAST             0  'self'
         160  STORE_ATTR            8  '_align'
         163  JUMP_FORWARD          0  'to 166'
       166_0  COME_FROM                '163'

 350     166  LOAD_FAST             0  'self'
         169  LOAD_ATTR             8  '_align'
         172  STORE_FAST            7  'hAlign'

 351     175  LOAD_GLOBAL          10  'hAlign_anchor_dict'
         178  LOAD_ATTR            11  'get'
         181  LOAD_FAST             7  'hAlign'
         184  LOAD_CONST            2  ''
         187  CALL_FUNCTION_2       2 
         190  STORE_FAST            8  'x_anchor'

 352     193  LOAD_FAST             0  'self'
         196  LOAD_ATTR            12  'getAnchorPoint'
         199  CALL_FUNCTION_0       0 
         202  LOAD_ATTR            13  'y'
         205  STORE_FAST            9  'y_anchor'

 353     208  LOAD_FAST             6  'parent_sz'
         211  LOAD_ATTR            14  'width'
         214  LOAD_FAST             8  'x_anchor'
         217  BINARY_MULTIPLY  
         218  STORE_FAST           10  'x_pos'

 354     221  LOAD_FAST             6  'parent_sz'
         224  LOAD_ATTR            15  'height'
         227  LOAD_FAST             9  'y_anchor'
         230  BINARY_MULTIPLY  
         231  STORE_FAST           11  'y_pos'

 355     234  LOAD_FAST             3  'nd_auto_fit'
         237  LOAD_ATTR            16  'setAnchorPoint'
         240  LOAD_GLOBAL          17  'cc'
         243  LOAD_ATTR            18  'Vec2'
         246  LOAD_FAST             8  'x_anchor'
         249  LOAD_FAST             9  'y_anchor'
         252  CALL_FUNCTION_2       2 
         255  CALL_FUNCTION_1       1 
         258  POP_TOP          

 356     259  LOAD_FAST             3  'nd_auto_fit'
         262  LOAD_ATTR            19  'setPosition'
         265  LOAD_GLOBAL          17  'cc'
         268  LOAD_ATTR            18  'Vec2'
         271  LOAD_FAST            10  'x_pos'
         274  LOAD_FAST            11  'y_pos'
         277  CALL_FUNCTION_2       2 
         280  CALL_FUNCTION_1       1 
         283  POP_TOP          

 357     284  LOAD_GLOBAL          20  'max'
         287  LOAD_FAST             5  'size'
         290  LOAD_ATTR            14  'width'
         293  LOAD_FAST             1  'min_size'
         296  LOAD_CONST            2  ''
         299  BINARY_SUBSCR    
         300  CALL_FUNCTION_2       2 
         303  STORE_FAST           12  'width'

 358     306  LOAD_GLOBAL          20  'max'
         309  LOAD_FAST             5  'size'
         312  LOAD_ATTR            15  'height'
         315  LOAD_FAST             1  'min_size'
         318  LOAD_CONST            3  1
         321  BINARY_SUBSCR    
         322  CALL_FUNCTION_2       2 
         325  STORE_FAST           13  'height'

 359     328  LOAD_FAST             3  'nd_auto_fit'
         331  LOAD_ATTR            21  'setContentSize'
         334  LOAD_GLOBAL          17  'cc'
         337  LOAD_ATTR            22  'Size'
         340  LOAD_FAST            12  'width'
         343  LOAD_FAST            13  'height'
         346  CALL_FUNCTION_2       2 
         349  CALL_FUNCTION_1       1 
         352  POP_TOP          

 360     353  LOAD_FAST             3  'nd_auto_fit'
         356  LOAD_ATTR            23  'ChildResizeAndPosition'
         359  CALL_FUNCTION_0       0 
         362  POP_TOP          
         363  JUMP_BACK            78  'to 78'
         366  POP_BLOCK        
       367_0  COME_FROM                '71'
         367  LOAD_CONST            0  ''
         370  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 38

    def ResizeAndPosition(self, include_self=True):
        if include_self:
            self.ResizeAndPositionSelf()
        self.UpdateAutoFitChild()

    def SeFullBgMode(self):
        super(CCRichText, self).SeFullBgMode()
        self.SetString(self._rstr)

    @staticmethod
    def RecordRichTextSprite(obj, string):
        if not global_data.is_low_mem_mode and global_data.uisystem._can_collect_sprite_usage:
            pat = 'gui.*\\.png'
            rets = re.findall(pat, string)
            for msgs in rets:
                global_data.uisystem.RecordSpriteUsage('', msgs, obj)


class CCRichTextCreator(CCNodeCreator):
    COM_NAME = 'CCRichText'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('fontName', 'gui/fonts/fzy4jw.ttf'),
     (
      'fontTrans', True),
     ('fontSize', 24),
     (
      'dimensions', {'width': 0,'height': 0}),
     (
      'hAlign', ccui.RICHTEXT_HORIZONTAL_ALIGN_TYPE_LEFT),
     (
      'vAlign', ccui.RICHTEXT_VERTICAL_ALIGN_TYPE_TOP),
     ('text', ''),
     ('color', '#SW'),
     ('addition_spacing', 0),
     (
      'bEnableOutline', False),
     ('shadowColor', '#SK'),
     ('outlineOpacity', 255),
     ('shadowWidth', 2),
     (
      'bEnableShadow', False),
     ('shadowColor1', '#SK'),
     ('shadowOpacity', 255),
     (
      'shadowOffset', {'width': 2,'height': -2})]
    ATTR_INIT = CCNodeCreator.ATTR_INIT

    @staticmethod
    def create(parent, root, fontSize, dimensions, hAlign, vAlign, text, color, opacity, fontName, bEnableOutline, shadowColor, outlineOpacity, shadowWidth, bEnableShadow, shadowColor1, shadowOpacity, shadowOffset, scale, addition_spacing, fontTrans):
        if parent:
            width, height = parent.GetContentSize()
        else:
            wsize = global_data.ui_mgr.design_screen_size
            width, height = wsize.width, wsize.height
        w = calc_pos(dimensions['width'], width, get_scale(scale['x']))
        h = calc_pos(dimensions['height'], height, get_scale(scale['y']))
        color = get_color_val(color)
        obj = CCRichText.Create(text, fontSize, CCSize(w, h), fontName, ccc4FromHex(color), fontTrans=fontTrans, addition_spacing=addition_spacing)
        obj.SetHorizontalAlign(hAlign)
        obj.setVerticalAlign(vAlign)
        obj.setOpacity(opacity)
        if bEnableOutline:
            obj.EnableOutline(bEnableOutline, shadowColor, outlineOpacity, shadowWidth)
        if bEnableShadow:
            obj.EnableShadow(bEnableShadow, shadowColor1, shadowOpacity, CCSize(shadowOffset['width'], shadowOffset['height']))
        if obj.IsNeedUpdate():
            obj.SetString(text)
        return obj

    @staticmethod
    def set_attr_group_size(obj, parent, root, size):
        pass

    @staticmethod
    def set_attr_group_created(obj, parent, root):
        obj.UpdateAutoFitChild()