# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCUIText.py
from __future__ import absolute_import
from __future__ import print_function
import six
import cc
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNodeCreator
from .CCUIWidget import CCUIWidget
from common.utils.cocos_utils import CCSizeZero, ccc4aFromHex, CCSize, CCPointZero, ccc4FromHex
from common.utils.ui_utils import get_scale, calc_pos
from logic.gcommon.common_utils.local_text import get_text_by_id, get_lang_shrink_font_size, get_cur_lang_shrink_setting, get_extra_vertical_space, get_enable_def_linebreak
from common.utils.cocos_utils import ccc3FromHex
from common.uisys.color_table import get_color_val, format_color_replace
from common.uisys.font_utils import GetMultiLangFontName
import re
from logic.client.const.ui_const import UNCOUNT_CHAR_UNICODE, TH_SEP_UTF_8
from common.utils.cocos_utils import BlendValue, BlendFactorMap
hAlign_anchor_dict = {cc.TEXTHALIGNMENT_LEFT: 0,
   cc.TEXTHALIGNMENT_CENTER: 0.5,
   cc.TEXTHALIGNMENT_RIGHT: 1
   }
vAlign_anchor_dict = {cc.TEXTVALIGNMENT_BOTTOM: 0,
   cc.TEXTVALIGNMENT_CENTER: 0.5,
   cc.TEXTVALIGNMENT_TOP: 1
   }

@ProxyClass(ccui.Text)
class CCUIText(CCUIWidget):

    @classmethod
    def Create(cls, text='', fontSize=25, szDemensions=None, hAlign=cc.TEXTHALIGNMENT_LEFT, vAlign=cc.TEXTVALIGNMENT_TOP, fontName='gui/fonts/fzy4jw.ttf', fontTrans=True):
        fontName = GetMultiLangFontName(fontName.lower(), fontTrans)
        if szDemensions is None:
            szDemensions = CCSize(0, 0)
        text_id = None
        if isinstance(text, int):
            text_id = text
            text = get_text_by_id(text_id)
        _fontsz = get_lang_shrink_font_size(fontSize)
        self = cls(cls.create('', fontName, _fontsz))
        self._fontsz = _fontsz
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self._minFontSize = lang_shrink_setting.iMinFontSize
        if not get_enable_def_linebreak():
            if self.getVirtualRenderer():
                self.getVirtualRenderer().setLineBreakWithoutSpace(True)
        if not global_data.feature_mgr.is_richtext_for_Japanese_fixed():
            if szDemensions.height > 0 and szDemensions.height < self.getLineHeight():
                szDemensions.height = self.getLineHeight()
        extra_spacing = get_extra_vertical_space()
        if extra_spacing:
            self.setLineHeight(self.getLineHeight() + extra_spacing)
        self.setTextHorizontalAlignment(hAlign)
        self.setTextVerticalAlignment(vAlign)
        self.CheckAutoShrinkFont()
        self.setTextAreaSize(szDemensions)
        self._text_id = text_id
        self.SetString(text)
        self._fontName = fontName
        self._fontTrans = fontTrans
        self._text = text
        self._text_args = None
        self._is_rich_mode = False
        self._nOutLineWidth = 0
        self._bEnableSoftShadow = False
        self._softShadowEffect = None
        self._soft_shadow_label = None
        return self

    def csb_init(self):
        super(CCUIText, self).csb_init()
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self._minFontSize = lang_shrink_setting.iMinFontSize
        if not get_enable_def_linebreak():
            if self.getVirtualRenderer():
                self.getVirtualRenderer().setLineBreakWithoutSpace(True)
        self.CheckAutoShrinkFont()

    def Destroy(self, is_remove=True):
        if self._softShadowEffect:
            self._softShadowEffect.destroy()
            self._softShadowEffect = None
        if self._soft_shadow_label:
            self._soft_shadow_label.release()
            self._soft_shadow_label = None
        super(CCUIText, self).Destroy(is_remove)
        return

    def SetContentSize(self, w, h):
        return self.getContentSize()

    def SetFontSize(self, fontSize):
        self._fontsz = get_lang_shrink_font_size(fontSize)
        self.setFontSize(int(self._fontsz))

    def SetString(self, s, args=None, need_update_child=True):
        if isinstance(s, int):
            self._text_id = s
            s = get_text_by_id(s, args)
        if not global_data.feature_mgr.is_support_boundary_word() and not get_enable_def_linebreak():
            s = re.sub(TH_SEP_UTF_8, '', s)
        self._text = s
        if s == self._obj.getString():
            return s
        if self._is_rich_mode:
            s = format_color_replace(s)
        self._obj.setString(s)
        area_size = self.getTextAreaSize()
        if not get_enable_def_linebreak() and area_size.width > 0 and area_size.height > 0:
            show_font_sz = self.getVirtualRenderer().getShowFontSize()
            count = self.getVirtualRenderer().getLetterCount()
            remove_string = UNCOUNT_CHAR_UNICODE
            new_string = re.sub('[%s]' % remove_string, '', six.text_type(self._text))
            text_len = len(new_string)
            if count != text_len and text_len > 0 and count > 0:
                scale = float(count) / text_len
                if scale < 1.1:
                    new_font_sz = max(int(scale * show_font_sz), self._minFontSize)
                    self.setFontSize(new_font_sz)
        self.CheckStringFullyShow(s)
        if need_update_child:
            self.UpdateAutoFitChild()
        if self._bEnableSoftShadow:
            self._soft_shadow_label.setString(self.getString())
            self.UpdateSoftShadowEffect()
        return s

    def SetStringWithChildRefresh(self, s, args=None):
        self.SetString(s, args, need_update_child=False)
        self.ChildResizeAndPosition()

    def SetStringWithAdapt(self, s, args=None, min_size=(0, 0)):
        self.SetString(s, args, need_update_child=False)
        self.RefreshChildByRealSize(min_size)

    def RefreshChildByRealSize(self, min_size=(0, 0)):
        size = self.getTextContentSize()
        width = max(size.width, min_size[0])
        height = max(size.height, min_size[1])
        self.ChildResizeAndPositionWithSize(width, height)

    @staticmethod
    def GetMultiLangString(text):
        if isinstance(text, int):
            text_id = text
            text = get_text_by_id(text_id)
        return text

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color_val = get_color_val(color)
        else:
            color_val = color
        self.setColor(ccc3FromHex(color_val))

    def RefreshString(self):
        if self._text_id != None:
            s = get_text_by_id(self._text_id, self._text_args)
            if s == self.getString():
                return s
            self.setString(s)
        return

    def GetString(self):
        return self.getString()

    def SetOutLineColor(self, color):
        cc_color = ccc4FromHex(get_color_val(color), self._outLineColor.a)
        self.EnableOutline(cc_color, self._nOutLineWidth)

    def EnableOutline(self, color, width):
        self._nOutLineWidth = width
        self._outLineColor = color
        self.enableOutline(color, width)
        if not global_data.feature_mgr.is_richtext_for_Japanese_fixed():
            old_size = self.getTextAreaSize()
            cur_line_height = self.getLineHeight()
            if old_size.height > 0 and old_size.height < cur_line_height:
                self.setTextAreaSize(cc.Size(old_size.width, cur_line_height))

    def EnableShadow(self, shadowColor1, shadowOpacity, shadowOffset):
        self.enableShadow(ccc4aFromHex((shadowOpacity << 24) + get_color_val(shadowColor1)), CCSize(shadowOffset['width'], shadowOffset['height']), 0)

    def SetRichMode(self, rich_mode):
        self._is_rich_mode = rich_mode
        self.setRichMode(rich_mode)
        if rich_mode:
            new_s = format_color_replace(self._text)
            if self._text == new_s:
                return
            self.SetString(new_s)

    def CheckAutoShrinkFont(self):
        lang_shrink_setting = get_cur_lang_shrink_setting()
        self.setEnableFontSizeAutoShrink(lang_shrink_setting.bEnableShrink, lang_shrink_setting.iMinFontSize)
        return lang_shrink_setting.bEnableShrink

    def ResetNodeConfAttr(self, repos=True, resize=True):
        super(CCUIText, self).ResetNodeConfAttr(repos, resize)
        conf = self._conf
        if conf is None:
            return
        else:
            text = self._conf['text']
            self.SetString(text)
            return

    def RecordNodeConfAttr(self):
        super(CCUIText, self).RecordNodeConfAttr()
        if self._conf and 'text' not in self._conf:
            self._conf['text'] = self.getString()

    def SetFontName(self, fontName):
        self.setFontName(GetMultiLangFontName(fontName))

    def CheckStringFullyShow(self, string):
        if global_data.is_inner_server and global_data.enable_text_check:
            import re
            count = self.getVirtualRenderer().getLetterCount()
            remove_string = UNCOUNT_CHAR_UNICODE
            pattern = '[' + remove_string + ']'
            new_string = re.sub(pattern, '', six.text_type(string))
            text_len = len(new_string)
            if count < text_len:
                tips = '\xe6\x98\xbe\xe7\xa4\xba\xe4\xb8\x8d\xe5\x85\xa8 =%d\xef\xbc\x8c\xe5\xae\x9e\xe9\x99\x85=%d str=%s ' % (text_len, count, string)
                if self._text_id:
                    tips += ' id=%d' % self._text_id
                template_list = self.GetNodeBelongingTemplate()
                if template_list:
                    tips += ' template_list = %s' % str(template_list)
                print('CheckStringFullyShow ', tips)
                global_data.game_mgr.show_tip(tips)

    def SetStringWithAutoFitAdapt(self, s, min_size=(0, 0)):
        self.SetString(s, need_update_child=False)
        self.UpdateAutoFitChild(min_size)

    def UpdateAutoFitChild--- This code section failed: ---

 258       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'GetChildren'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  'children'

 259      12  LOAD_FAST             2  'children'
          15  POP_JUMP_IF_TRUE     22  'to 22'

 260      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 261      22  LOAD_GLOBAL           1  'getattr'
          25  LOAD_GLOBAL           1  'getattr'
          28  CALL_FUNCTION_2       2 
          31  POP_JUMP_IF_FALSE    55  'to 55'
          34  LOAD_FAST             0  'self'
          37  LOAD_ATTR             2  'nd_auto_fit'
        40_0  COME_FROM                '31'
          40  POP_JUMP_IF_FALSE    55  'to 55'

 262      43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             2  'nd_auto_fit'
          49  STORE_FAST            3  'nd_auto_fit'
          52  JUMP_FORWARD          6  'to 61'

 264      55  LOAD_CONST            0  ''
          58  STORE_FAST            3  'nd_auto_fit'
        61_0  COME_FROM                '52'

 265      61  SETUP_LOOP          278  'to 342'
          64  LOAD_FAST             2  'children'
          67  GET_ITER         
          68  FOR_ITER            270  'to 341'
          71  STORE_FAST            4  'child'

 266      74  LOAD_FAST             3  'nd_auto_fit'
          77  LOAD_FAST             4  'child'
          80  COMPARE_OP            3  '!='
          83  POP_JUMP_IF_FALSE    99  'to 99'

 267      86  LOAD_FAST             4  'child'
          89  LOAD_ATTR             4  'ResizeAndPosition'
          92  CALL_FUNCTION_0       0 
          95  POP_TOP          
          96  JUMP_BACK            68  'to 68'

 269      99  LOAD_FAST             0  'self'
         102  LOAD_ATTR             5  'getTextContentSize'
         105  CALL_FUNCTION_0       0 
         108  STORE_FAST            5  'size'

 270     111  LOAD_FAST             0  'self'
         114  LOAD_ATTR             6  'getContentSize'
         117  CALL_FUNCTION_0       0 
         120  STORE_FAST            6  'parent_sz'

 271     123  LOAD_FAST             0  'self'
         126  LOAD_ATTR             7  'getTextHorizontalAlignment'
         129  CALL_FUNCTION_0       0 
         132  STORE_FAST            7  'hAlign'

 272     135  LOAD_FAST             0  'self'
         138  LOAD_ATTR             8  'getTextVerticalAlignment'
         141  CALL_FUNCTION_0       0 
         144  STORE_FAST            8  'vAlign'

 273     147  LOAD_GLOBAL           9  'hAlign_anchor_dict'
         150  LOAD_ATTR            10  'get'
         153  LOAD_FAST             7  'hAlign'
         156  LOAD_CONST            2  ''
         159  CALL_FUNCTION_2       2 
         162  STORE_FAST            9  'x_anchor'

 274     165  LOAD_GLOBAL          11  'vAlign_anchor_dict'
         168  LOAD_ATTR            10  'get'
         171  LOAD_FAST             8  'vAlign'
         174  LOAD_CONST            2  ''
         177  CALL_FUNCTION_2       2 
         180  STORE_FAST           10  'y_anchor'

 275     183  LOAD_FAST             6  'parent_sz'
         186  LOAD_ATTR            12  'width'
         189  LOAD_FAST             9  'x_anchor'
         192  BINARY_MULTIPLY  
         193  STORE_FAST           11  'x_pos'

 276     196  LOAD_FAST             6  'parent_sz'
         199  LOAD_ATTR            13  'height'
         202  LOAD_FAST            10  'y_anchor'
         205  BINARY_MULTIPLY  
         206  STORE_FAST           12  'y_pos'

 277     209  LOAD_FAST             3  'nd_auto_fit'
         212  LOAD_ATTR            14  'setAnchorPoint'
         215  LOAD_GLOBAL          15  'cc'
         218  LOAD_ATTR            16  'Vec2'
         221  LOAD_FAST             9  'x_anchor'
         224  LOAD_FAST            10  'y_anchor'
         227  CALL_FUNCTION_2       2 
         230  CALL_FUNCTION_1       1 
         233  POP_TOP          

 278     234  LOAD_FAST             3  'nd_auto_fit'
         237  LOAD_ATTR            17  'setPosition'
         240  LOAD_GLOBAL          15  'cc'
         243  LOAD_ATTR            16  'Vec2'
         246  LOAD_FAST            11  'x_pos'
         249  LOAD_FAST            12  'y_pos'
         252  CALL_FUNCTION_2       2 
         255  CALL_FUNCTION_1       1 
         258  POP_TOP          

 279     259  LOAD_GLOBAL          18  'max'
         262  LOAD_FAST             5  'size'
         265  LOAD_ATTR            12  'width'
         268  LOAD_FAST             1  'min_size'
         271  LOAD_CONST            2  ''
         274  BINARY_SUBSCR    
         275  CALL_FUNCTION_2       2 
         278  STORE_FAST           13  'width'

 280     281  LOAD_GLOBAL          18  'max'
         284  LOAD_FAST             5  'size'
         287  LOAD_ATTR            13  'height'
         290  LOAD_FAST             1  'min_size'
         293  LOAD_CONST            3  1
         296  BINARY_SUBSCR    
         297  CALL_FUNCTION_2       2 
         300  STORE_FAST           14  'height'

 281     303  LOAD_FAST             3  'nd_auto_fit'
         306  LOAD_ATTR            19  'setContentSize'
         309  LOAD_GLOBAL          15  'cc'
         312  LOAD_ATTR            20  'Size'
         315  LOAD_FAST            13  'width'
         318  LOAD_FAST            14  'height'
         321  CALL_FUNCTION_2       2 
         324  CALL_FUNCTION_1       1 
         327  POP_TOP          

 282     328  LOAD_FAST             3  'nd_auto_fit'
         331  LOAD_ATTR            21  'ChildResizeAndPosition'
         334  CALL_FUNCTION_0       0 
         337  POP_TOP          
         338  JUMP_BACK            68  'to 68'
         341  POP_BLOCK        
       342_0  COME_FROM                '61'
         342  LOAD_CONST            0  ''
         345  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 28

    def EnableSoftShadow(self, is_enable, color='#SW', sample_step=1.0, need_update=False):
        if not global_data.feature_mgr.is_support_render_texture_blend_state_1_0():
            return
        self._bEnableSoftShadow = is_enable
        if is_enable:
            if not self._soft_shadow_label:
                show_font_sz = self.getVirtualRenderer().getShowFontSize()
                self._soft_shadow_label = ccui.Text.create(self.getString(), self.getFontName(), show_font_sz)
                ss_obj = self._soft_shadow_label
                ss_obj.setKerning(self.getKerning())
                ss_obj.setLineHeight(ss_obj.getLineHeight())
                ss_obj.setTextHorizontalAlignment(self.getTextHorizontalAlignment())
                ss_obj.setTextVerticalAlignment(self.getTextVerticalAlignment())
                ss_obj.setTextAreaSize(self.getTextAreaSize())
                self._soft_shadow_label.retain()
            if not self._softShadowEffect:
                from logic.comsys.effect.ui_effect import OpacityGaussianEffect
                self._softShadowEffect = OpacityGaussianEffect(self._soft_shadow_label, self)
            self._softShadowEffect.set_render_color(color)
            self._softShadowEffect.set_sample_step(sample_step)
            self._softShadowEffect.SetVisible(True)
            if need_update:
                self.UpdateSoftShadowEffect()
        elif self._softShadowEffect:
            self._softShadowEffect.SetVisible(False)

    def SetSoftShadowParameter(self, softShadowOpacity, ssBlurAlphaFactor, softShadowBlendFun, softShadowScale, softShadowOffset):
        if not self._bEnableSoftShadow:
            return
        self._softShadowEffect.set_render_result_parameter(softShadowOpacity, ssBlurAlphaFactor, softShadowBlendFun, softShadowScale, softShadowOffset)

    def UpdateSoftShadowEffect(self):
        if not self._bEnableSoftShadow:
            return
        self._softShadowEffect.start()

    def ResizeAndPosition(self, include_self=True):
        if include_self:
            self.ResizeAndPositionSelf()
        self.UpdateAutoFitChild()


class UITextCreator(CCNodeCreator):
    COM_NAME = 'CCLabel'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('fontName', 'gui/fonts/fzy4jw.ttf'),
     (
      'fontTrans', True),
     ('fontSize', 24),
     (
      'dimensions', {'width': 0,'height': 0}),
     (
      'hAlign', cc.TEXTHALIGNMENT_LEFT),
     (
      'vAlign', cc.TEXTVALIGNMENT_TOP),
     ('text', ''),
     ('color', '#SW'),
     ('spacing', 0),
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
      'shadowOffset', {'width': 2,'height': -2}),
     ('additionalKerning', 0),
     (
      'richMode', False),
     (
      'bEnableGlow', False),
     ('glowColor', '#SK'),
     (
      'bEnableSoftShadow', False),
     ('ssBlurSampleStep', 1.0),
     ('ssBlurAlphaFactor', 1.0),
     ('softShadowColor', '#SK'),
     ('softShadowOpacity', 255),
     (
      'softShadowBlendFun', {'src': BlendValue['BLEND_ONE'],'dst': BlendValue['BLEND_INVSRCALPHA']}),
     (
      'softShadowScale', {'x': 1,'y': 1}),
     (
      'softShadowOffset', {'width': 0,'height': 0})]

    @staticmethod
    def create(parent, root, fontSize, dimensions, hAlign, vAlign, text, color, opacity, fontName, bEnableOutline, shadowColor, outlineOpacity, shadowWidth, bEnableShadow, shadowColor1, shadowOpacity, shadowOffset, scale, spacing, additionalKerning, richMode, bEnableGlow, glowColor, fontTrans):
        if parent:
            width, height = parent.GetContentSize()
        else:
            w_size = global_data.ui_mgr.design_screen_size
            width, height = w_size.width, w_size.height
        w = calc_pos(dimensions['width'], width, get_scale(scale['x']))
        h = calc_pos(dimensions['height'], height, get_scale(scale['y']))
        obj = CCUIText.Create(text, fontSize, CCSize(w, h), hAlign, vAlign, fontName, fontTrans)
        obj.setKerning(additionalKerning)
        obj.SetColor(color)
        obj.setOpacity(opacity)
        if bEnableOutline:
            obj.EnableOutline(ccc4aFromHex((outlineOpacity << 24) + get_color_val(shadowColor)), shadowWidth)
        if bEnableShadow:
            obj.enableShadow(ccc4aFromHex((shadowOpacity << 24) + get_color_val(shadowColor1)), CCSize(shadowOffset['width'], shadowOffset['height']), 0)
        if spacing != 0:
            obj.setLineHeight(spacing + obj.getLineHeight())
        if richMode:
            obj.SetRichMode(richMode)
        return obj

    @staticmethod
    def set_attr_group_created(obj, parent, root, bEnableSoftShadow, ssBlurSampleStep, ssBlurAlphaFactor, softShadowColor, softShadowOpacity, softShadowBlendFun, softShadowScale, softShadowOffset):
        if bEnableSoftShadow:
            obj.EnableSoftShadow(True, softShadowColor, sample_step=ssBlurSampleStep, need_update=False)
            softShadowScale_t = (get_scale(softShadowScale['x']), get_scale(softShadowScale['y']))
            obj.SetSoftShadowParameter(softShadowOpacity, ssBlurAlphaFactor, (softShadowBlendFun['src'], softShadowBlendFun['dst']), softShadowScale_t, CCSize(softShadowOffset['width'], softShadowOffset['height']))
            obj.UpdateSoftShadowEffect()
        obj.UpdateAutoFitChild()

    @staticmethod
    def check_config--- This code section failed: ---

 417       0  LOAD_FAST             0  'conf'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'softShadowBlendFun'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'blendConf'

 418      18  LOAD_FAST             1  'blendConf'
          21  POP_JUMP_IF_FALSE    64  'to 64'

 419      24  BUILD_MAP_2           2 
          27  LOAD_GLOBAL           2  'BlendFactorMap'
          30  LOAD_FAST             1  'blendConf'
          33  LOAD_CONST            2  'src'
          36  BINARY_SUBSCR    
          37  BINARY_SUBSCR    
          38  LOAD_CONST            2  'src'
          41  STORE_MAP        
          42  LOAD_GLOBAL           2  'BlendFactorMap'
          45  LOAD_FAST             1  'blendConf'
          48  LOAD_CONST            3  'dst'
          51  BINARY_SUBSCR    
          52  BINARY_SUBSCR    
          53  LOAD_CONST            3  'dst'
          56  STORE_MAP        
          57  STORE_MAP        
          58  STORE_MAP        
          59  STORE_MAP        
          60  STORE_SUBSCR     
          61  JUMP_FORWARD          0  'to 64'
        64_0  COME_FROM                '61'
          64  LOAD_CONST            0  ''
          67  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 57