# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/json_tools/check_json_csb_diff.py
import cc
import ccui
import json
import os
type_factory = {}
from common.uisys.uielment.CCNode import CCNode
EPSILON = 1e-05

def equals--- This code section failed: ---

  56       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'equals'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    25  'to 25'

  57      12  LOAD_FAST             0  'var1'
          15  LOAD_ATTR             1  'equals'
          18  LOAD_FAST             1  'var2'
          21  CALL_FUNCTION_1       1 
          24  RETURN_END_IF    
        25_0  COME_FROM                '9'

  58      25  LOAD_GLOBAL           2  'isinstance'
          28  LOAD_FAST             0  'var1'
          31  LOAD_GLOBAL           3  'cc'
          34  LOAD_ATTR             4  'Vec3'
          37  CALL_FUNCTION_2       2 
          40  POP_JUMP_IF_FALSE    95  'to 95'

  59      43  LOAD_FAST             0  'var1'
          46  LOAD_ATTR             5  'x'
          49  LOAD_FAST             1  'var2'
          52  LOAD_ATTR             5  'x'
          55  COMPARE_OP            2  '=='
          58  JUMP_IF_FALSE_OR_POP    94  'to 94'
          61  LOAD_FAST             0  'var1'
          64  LOAD_ATTR             6  'y'
          67  LOAD_FAST             1  'var2'
          70  LOAD_ATTR             6  'y'
          73  COMPARE_OP            2  '=='
          76  JUMP_IF_FALSE_OR_POP    94  'to 94'
          79  LOAD_FAST             0  'var1'
          82  LOAD_ATTR             7  'z'
          85  LOAD_FAST             1  'var2'
          88  LOAD_ATTR             7  'z'
          91  COMPARE_OP            2  '=='
        94_0  COME_FROM                '76'
        94_1  COME_FROM                '58'
          94  RETURN_END_IF    
        95_0  COME_FROM                '40'

  60      95  LOAD_GLOBAL           2  'isinstance'
          98  LOAD_FAST             0  'var1'
         101  LOAD_GLOBAL           3  'cc'
         104  LOAD_ATTR             8  'Color3B'
         107  CALL_FUNCTION_2       2 
         110  POP_JUMP_IF_FALSE   165  'to 165'

  61     113  LOAD_FAST             0  'var1'
         116  LOAD_ATTR             9  'r'
         119  LOAD_FAST             1  'var2'
         122  LOAD_ATTR             9  'r'
         125  COMPARE_OP            2  '=='
         128  JUMP_IF_FALSE_OR_POP   164  'to 164'
         131  LOAD_FAST             0  'var1'
         134  LOAD_ATTR            10  'g'
         137  LOAD_FAST             1  'var2'
         140  LOAD_ATTR            10  'g'
         143  COMPARE_OP            2  '=='
         146  JUMP_IF_FALSE_OR_POP   164  'to 164'
         149  LOAD_FAST             0  'var1'
         152  LOAD_ATTR            11  'b'
         155  LOAD_FAST             1  'var2'
         158  LOAD_ATTR            11  'b'
         161  COMPARE_OP            2  '=='
       164_0  COME_FROM                '146'
       164_1  COME_FROM                '128'
         164  RETURN_END_IF    
       165_0  COME_FROM                '110'

  63     165  LOAD_GLOBAL          12  'type'
         168  LOAD_FAST             0  'var1'
         171  CALL_FUNCTION_1       1 
         174  LOAD_GLOBAL          13  'float'
         177  BUILD_TUPLE_1         1 
         180  COMPARE_OP            6  'in'
         183  POP_JUMP_IF_FALSE   206  'to 206'

  64     186  LOAD_GLOBAL          14  'abs'
         189  LOAD_FAST             0  'var1'
         192  LOAD_FAST             1  'var2'
         195  BINARY_SUBTRACT  
         196  CALL_FUNCTION_1       1 
         199  LOAD_GLOBAL          15  'EPSILON'
         202  COMPARE_OP            0  '<'
         205  RETURN_END_IF    
       206_0  COME_FROM                '183'

  66     206  LOAD_FAST             0  'var1'
         209  LOAD_FAST             1  'var2'
         212  COMPARE_OP            2  '=='
         215  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


class UIObjectMeta(type):

    def __init__(cls, name, bases, dic):
        super(UIObjectMeta, cls).__init__(name, bases, dic)
        if name != 'UIObjectBaseCreator':
            type_factory[cls.COM_NAME] = cls


class UIObjectBaseCreator(object):
    __metaclass__ = UIObjectMeta
    COM_NAME = 'UIObjectBase'


class CCNodeCreator(UIObjectBaseCreator):
    COM_NAME = 'CCNode'
    ATTR_DEFINE = [
     (
      'name', lambda nd: nd.GetName()),
     (
      'zorder', lambda nd: nd.getLocalZOrder()),
     (
      'pos', lambda nd: nd.getPosition()),
     (
      'hide', lambda nd: nd.isVisible()),
     (
      'ignorAnchor', lambda nd: nd.isIgnoreAnchorPointForPosition()),
     (
      'anchor', lambda nd: nd.getAnchorPoint()),
     (
      'rotation', lambda nd: nd.getRotation()),
     (
      'skew', lambda nd: [nd.getSkewX(), nd.getSkewY()]),
     (
      'scale', lambda nd: [nd.getScaleX(), nd.getScaleY()]),
     (
      'size', lambda nd: nd.getContentSize()),
     (
      'opacity', lambda nd: nd.getOpacity()),
     (
      'rotation3D', lambda nd: nd.getRotation3D()),
     (
      'pos_z', lambda nd: nd.getPositionZ())]

    @staticmethod
    def check_json_normal_but_csb_ext_data(nd, ext_key, default=None):
        if nd.IsCSBNode():
            from common.uisys.cocomate import get_ext_data
            return get_ext_data(nd, ext_key, default=default)
        else:
            return get_real_conf(nd).get(ext_key, default)


class CCLayerCreator(CCNodeCreator):
    COM_NAME = 'CCLayer'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'touchEnabled', lambda nd: nd.isTouchEnabled()),
     (
      'swallow', lambda nd: nd.isSwallowTouches()),
     (
      'noEventAfterMove', lambda nd: nd._bNoEventAfterMove),
     (
      'move_dist', lambda nd: nd._nNoEventMoveDist),
     (
      'forceHandleTouch', lambda nd: nd.isForceHandleTouch())]


class CCLayerColorCreator(CCLayerCreator):
    COM_NAME = 'CCLayerColor'
    ATTR_DEFINE = CCLayerCreator.ATTR_DEFINE + [
     (
      'color', lambda nd: nd.getColor())]


class CCLayerGradientCreator(CCLayerCreator):
    COM_NAME = 'CCLayerGradient'
    ATTR_DEFINE = CCLayerCreator.ATTR_DEFINE + [
     ('startColor', 16711680),
     ('endColor', 65280),
     ('startOpacity', 255),
     ('endOpacity', 255),
     (
      'vector', {'x': 1,'y': 0})]

    def check_attr(self, nd, attr):
        if type(nd) in [cc.LayerGradient]:
            attr_map = {'startColor': nd.getStartColor(),'endColor': nd.getEndColor(),
               'startOpacity': nd.getStartOpacity(),
               'endOpacity': nd.getEndOpacity(),
               'vector': nd.getVector()
               }
            return attr_map[attr]
        else:
            attr_map = {'startColor': nd.getBackGroundStartColor(),
               'endColor': nd.getBackGroundEndColor(),
               'startOpacity': nd.getStartOpacity(),
               'endOpacity': nd.getEndOpacity(),
               'vector': nd.getBackGroundColorVector()
               }
            return attr_map[attr]


class CCUILayoutCreator(CCNodeCreator):
    COM_NAME = 'CCUILayout'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'scale9Enabled', lambda nd: nd.isBackGroundImageScale9Enabled()),
     (
      'capInsets', lambda nd: nd.getBackGroundImageCapInsets()),
     (
      'bgColorType', lambda nd: nd.getBackGroundColorType()),
     (
      'bgColor', lambda nd: nd.getBackGroundColor()),
     (
      'bgOpacity', lambda nd: nd.getBackGroundColorOpacity()),
     (
      'startColor', lambda nd: nd.getBackGroundStartColor()),
     (
      'endColor', lambda nd: nd.getBackGroundEndColor()),
     (
      'vector', lambda nd: nd.getBackGroundColorVector()),
     (
      'clippingEnable', lambda nd: nd.isClippingEnabled())]


class CCSpriteCreator(CCNodeCreator):
    COM_NAME = 'CCSprite'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'displayFrame', lambda nd: nd.getTexture().getTextureFileName()),
     (
      'color', lambda nd: nd.getColor()),
     (
      'blendFun', lambda nd: nd.getBlendFunc()),
     (
      'shaderName', lambda nd: CCSpriteCreator.get_shader_name(nd)),
     (
      'flipX', lambda nd: nd.isFlippedX()),
     (
      'flipY', lambda nd: nd.isFlippedY()),
     (
      'psBlendMode', lambda nd: CCSpriteCreator.get_ps_blend_name(nd))]

    @staticmethod
    def get_shader_name(nd):
        if nd.IsCSBNode():
            from common.uisys.cocomate import get_ext_data, com_attr_name, key_splendor_filename
            com_attr = nd.getComponent(com_attr_name)
            if com_attr:
                splendor_filename = com_attr.getString(key_splendor_filename, '')
                return splendor_filename
        else:
            return get_real_conf(nd).get('shaderName', '')

    @staticmethod
    def get_ps_blend_name--- This code section failed: ---

 230       0  LOAD_FAST             0  'nd'
           3  LOAD_ATTR             0  'IsCSBNode'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_FALSE    53  'to 53'

 231      12  LOAD_CONST            1  -1
          15  LOAD_CONST            2  ('get_ext_data', 'com_attr_name', 'key_splendor_texturekey')
          18  IMPORT_NAME           1  'common.uisys.cocomate'
          21  IMPORT_FROM           2  'get_ext_data'
          24  STORE_FAST            1  'get_ext_data'
          27  IMPORT_FROM           3  'com_attr_name'
          30  STORE_FAST            2  'com_attr_name'
          33  IMPORT_FROM           4  'key_splendor_texturekey'
          36  STORE_FAST            3  'key_splendor_texturekey'
          39  POP_TOP          

 232      40  LOAD_FAST             1  'get_ext_data'
          43  LOAD_FAST             3  'key_splendor_texturekey'
          46  LOAD_CONST            0  ''
          49  CALL_FUNCTION_3       3 
          52  RETURN_END_IF    
        53_0  COME_FROM                '9'

 234      53  LOAD_GLOBAL           6  'get_real_conf'
          56  LOAD_FAST             0  'nd'
          59  CALL_FUNCTION_1       1 
          62  LOAD_ATTR             7  'get'
          65  LOAD_CONST            3  'psBlendMode'
          68  LOAD_CONST            0  ''
          71  CALL_FUNCTION_2       2 
          74  RETURN_VALUE     
          75  LOAD_CONST            0  ''
          78  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 49


class UIImageViewCreator(CCNodeCreator):
    COM_NAME = 'CCScale9Sprite'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'spriteFrame', lambda nd: nd.getTextureFilename()),
     (
      'capInsets', lambda nd: nd.getCapInsets()),
     (
      'color', lambda nd: nd.getColor()),
     (
      'blendFun', lambda nd: nd.getVirtualRenderer().getBlendFunc()),
     (
      'flipX', lambda nd: nd.isFlippedX()),
     (
      'flipY', lambda nd: nd.isFlippedY()),
     (
      'psBlendMode', lambda nd: CCSpriteCreator.get_ps_blend_name(nd))]


class CCProgressTimerCreator(CCNodeCreator):
    COM_NAME = 'CCProgressTimer'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'displayFrame', lambda nd: nd.getSprite().getTexture().getTextureFileName() if nd.getSprite() else None),
     (
      'color', lambda nd: nd.getColor()),
     (
      'midPoint', lambda nd: nd.getMidpoint()),
     (
      'type', lambda nd: nd.getType()),
     (
      'percentage', lambda nd: nd.getPercentage()),
     (
      'barChangeRate', lambda nd: nd.getBarChangeRate()),
     (
      'reverse', lambda nd: nd.isReverseDirection())]


def labelatlas_texturepath(nd):
    if nd.getVirtualRenderer().getTexture():
        return nd.getVirtualRenderer().getTexture().getTextureFileName()
    else:
        if not nd.IsCSBNode():
            print (
             'texturePath', get_real_conf(nd).get('texturePath'))
        return None


class CCLabelAtlasCreator(CCNodeCreator):
    COM_NAME = 'CCLabelAtlas'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'text', lambda nd: nd.getString()),
     (
      'color', lambda nd: nd.getColor()),
     (
      'texturePath', labelatlas_texturepath)]


class CCButtonCreator(CCNodeCreator):
    COM_NAME = 'CCButton'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      '9sprite', True),
     (
      'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
     ('frame1', 'gui/ui_res_2/default/img_useless.png'),
     ('frame2', 'gui/ui_res_2/default/img_useless.png'),
     ('frame3', ''),
     (
      'enableText', True),
     ('text', ''),
     ('fontName', 'gui/fonts/fzy4jw.ttf'),
     (
      'bEnableStateFontSize', False),
     ('fontSize', 24),
     ('fontSize1', 24),
     ('fontSize2', 24),
     ('textColor1', '#SW'),
     ('textColor2', '#SW'),
     ('textColor3', '#SW'),
     (
      'isEnabled', True),
     (
      'dimensions', {'width': 0,'height': 0})]

    def check_attr_enableText(self, json_node, csb_node):
        from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED, STATE_MOUSE_HOVER
        if json_node._text and csb_node._text:
            attr_test = [('text', lambda nd: nd._text.getString()),
             (
              'fontName', lambda nd: nd._text.getFontName()),
             (
              'textOffset', lambda nd: nd._text.getPosition()),
             (
              'textSkew', lambda nd: [nd._text.getSkewX(), nd._text.getSkewY()]),
             (
              'enableTextShadow', lambda nd: nd._text.getShadowEnable()),
             (
              'textShadow1', lambda nd: nd.getTitleNormalShadowColor() if json_node != nd else nd._display_textsShadows.get(STATE_NORMAL)),
             (
              'textShadow2', lambda nd: nd.getTitlePressedShadowColor() if json_node != nd else nd._display_textsShadows.get(STATE_SELECTED)),
             (
              'textShadow3', lambda nd: nd.getTitleDisableShadowColor() if json_node != nd else nd._display_textsShadows.get(STATE_DISABLED)),
             (
              'shadowOffset', lambda nd: nd._text.getShadowOffset()),
             (
              'hAlign', lambda nd: nd._text.getHorizontalAlign()),
             (
              'vAlign', lambda nd: nd._text.getVerticalAlign()),
             (
              'dimensions', lambda nd: nd._text.getDimensions())]
            for te in attr_test:
                attr, method = te
                if equals(method(json_node), method(csb_node)):
                    return True
                print ('attr check failed', attr, method(json_node), method(csb_node))

        elif json_node.IsEnableText() == False:
            return True

    def check_attr_isEnabled(self, json_node, csb_node):
        if json_node.IsEnable():
            attr_test = [('isEnabled', lambda nd: nd.IsEnable()),
             (
              'zoomScale', lambda nd: nd._zoomScale),
             (
              'swallow', lambda nd: nd.isSwallowTouches()),
             (
              'noEventAfterMove', lambda nd: nd._bNoEventAfterMove()),
             (
              'customClickZone', lambda nd: nd.getCustomClickZoneEnable()),
             (
              'clickZoneOffset', lambda nd: nd.getCustomClickZoneNode().getPosition()),
             (
              'clickZoneSize', lambda nd: nd.getCustomClickZoneNode().getContentSize())]
            for te in attr_test:
                attr, method = te
                if equals(method(json_node), method(csb_node)):
                    return True
                print ('attr check failed', attr, method(json_node), method(csb_node))

        elif json_node.IsEnable() == False:
            return True

    def check_attr(self, nd, attr):
        from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED, STATE_MOUSE_HOVER
        if not nd._is_created_from_conf:
            attr_map = {'9sprite': lambda nd: nd.isScale9Enabled(),'capInsets': lambda nd: nd.getCapInsetsNormalRenderer(),
               'frame1': lambda nd: nd.getTextureFilenameNormal(),
               'frame2': lambda nd: nd.getTextureFilenamePressed(),
               'frame3': lambda nd: nd.getTextureFilenameDisabled(),
               'bEnableStateFontSize': lambda nd: nd.getEnableStateFontSize(),
               'fontSize': lambda nd: nd.getTitleNormalFontSize(),
               'fontSize1': lambda nd: nd.getTitlePressedFontSize(),
               'fontSize2': lambda nd: nd.getTitleDisableFontSize(),
               'textColor1': lambda nd: nd.getTitleNormalTextColor(),
               'textColor2': lambda nd: nd.getTitlePressedTextColor(),
               'textColor3': lambda nd: nd.getTitleDisableTextColor(),
               'textOffset': lambda nd: nd._text.getPosition()
               }
            if attr not in attr_map:
                return True
            return attr_map[attr](nd)
        else:
            attr_map = {'9sprite': nd._bUse9Spt,
               'capInsets': nd._9rect if len(nd._display_spts.values()) > 0 else None,
               'frame1': nd._paths[0] if 0 < len(nd._paths) else '',
               'frame2': nd._paths[1] if 1 < len(nd._paths) else '',
               'frame3': nd._paths[2] if 2 < len(nd._paths) else '',
               'bEnableStateFontSize': nd._bEnableStateFontSize,
               'fontSize': nd._display_textsFontSize.get(STATE_NORMAL),
               'fontSize1': nd._display_textsFontSize.get(STATE_SELECTED),
               'fontSize2': nd._display_textsFontSize.get(STATE_DISABLED),
               'textColor1': nd._display_textsColors.get(STATE_NORMAL),
               'textColor2': nd._display_textsColors.get(STATE_SELECTED),
               'textColor3': nd._display_textsColors.get(STATE_DISABLED)
               }
            if attr not in attr_map:
                return True
            return attr_map[attr]
            return


class CCCheckButtonCreator(CCButtonCreator):
    COM_NAME = 'CCCheckButton'
    ATTR_DEFINE = CCButtonCreator.ATTR_DEFINE + [
     (
      'check', lambda nd: CCCheckButtonCreator.get_check(nd))]

    @staticmethod
    def get_check(nd):
        if nd.IsCSBNode():
            return nd.isSelected()
        else:
            return nd.GetCheck()


class CCRichTextCreator(CCNodeCreator):
    COM_NAME = 'CCRichText'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'fontName', lambda nd: nd.getFontName()),
     (
      'fontSize', lambda nd: nd.getFontSize()),
     (
      'dimensions', {'width': 0,'height': 0}),
     (
      'hAlign', lambda nd: nd.getHorizontalAlign()),
     (
      'vAlign', lambda nd: nd.getVerticalAlign()),
     (
      'text', lambda nd: nd.getString()),
     (
      'color', lambda nd: nd.getColor()),
     (
      'addition_spacing', lambda nd: nd.getVerticalSpace()),
     (
      'shadowColor', lambda nd: nd.getOutlineColor()),
     (
      'shadowWidth', lambda nd: nd.getOutlineSize()),
     (
      'bEnableShadow', lambda nd: nd.getShadowEnable()),
     (
      'shadowColor1', lambda nd: nd.getShaodwColor()),
     (
      'shadowOpacity', lambda nd: nd.getShaodwColor()),
     (
      'shadowOffset', lambda nd: nd.getShadowOffset())]


class UITextCreator(CCNodeCreator):
    COM_NAME = 'CCLabel'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'fontName', lambda nd: nd.getFontName()),
     (
      'fontSize', lambda nd: nd.getFontSize()),
     (
      'dimensions', lambda nd: nd.getTextAreaSize()),
     (
      'hAlign', lambda nd: nd.getTextHorizontalAlignment()),
     (
      'vAlign', lambda nd: nd.getTextVerticalAlignment()),
     (
      'text', lambda nd: nd.getString()),
     (
      'color', lambda nd: nd.getColor()),
     (
      'spacing', lambda nd: nd.getLineHeight()),
     ('bEnableOutline', None),
     ('shadowColor', None),
     ('outlineOpacity', None),
     ('shadowWidth', 2),
     (
      'bEnableShadow', lambda nd: nd.getVirtualRenderer().getShadowEnable()),
     (
      'shadowColor1', lambda nd: nd.getVirtualRenderer().getShaodwColor()),
     (
      'shadowOpacity', lambda nd: nd.getVirtualRenderer().getShadowOpacity()),
     (
      'shadowOffset', lambda nd: nd.getVirtualRenderer().getShadowOffset()),
     (
      'additionalKerning', lambda nd: nd.getKerning())]


class CCSkeletonNodeCreator(CCNodeCreator):
    COM_NAME = 'CCSkeletonNode'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + []


def check_loadingbar_texture(nd):
    if nd.getVirtualRenderer().getSprite():
        return nd.getVirtualRenderer().getSprite().getTexture().getTextureFileName()
    else:
        if not nd.IsCSBNode():
            print (
             'displayFrame', get_real_conf(nd).get('displayFrame'))
        return None
        return None


class CCLoadingBarCreator(CCNodeCreator):
    COM_NAME = 'CCLoadingBar'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      '9sprite', lambda nd: nd.isScale9Enabled()),
     (
      'capInsets', lambda nd: nd.getCapInsets()),
     (
      'displayFrame', check_loadingbar_texture),
     (
      'direction', lambda nd: nd.getDirection()),
     (
      'percentage', lambda nd: nd.getPercent())]


class CCSliderCreator(CCNodeCreator):
    COM_NAME = 'CCSlider'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'capInsets', lambda nd: nd.getCapInsetsBarRenderer()),
     (
      'capInsetsProgress', lambda nd: nd.getCapInsetsProgressBarRebderer()),
     (
      'barTex', lambda nd: nd.getVirtualRenderer().getSprite().getTexture().getTextureFileName()),
     (
      'percentage', lambda nd: nd.getPercent()),
     (
      'scale9Enabled', lambda nd: nd.isScale9Enabled())]


class CCLabelBMFontCreator(CCNodeCreator):
    COM_NAME = 'CCLabelBMFont'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'texturePath', lambda nd: nd.getFntFile()),
     (
      'text', lambda nd: nd.getString()),
     (
      'color', lambda nd: nd.getColor())]


class CCParticleSystemQuadCreator(CCNodeCreator):
    COM_NAME = 'CCParticleSystemQuad'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'particleFile', lambda nd: CCParticleSystemQuadCreator.check_pppp(nd)),
     (
      'stop', lambda nd: nd.isActive())]

    @staticmethod
    def check_pppp(nd):
        if not nd.IsCSBNode():
            print (
             'particleFile', get_real_conf(nd).get('particleFile'))
        if nd.getTexture():
            return nd.getTexture().getTextureFileName()
        else:
            return None
            return None


class CCScrollViewCreator(CCNodeCreator):
    COM_NAME = 'CCScrollView'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'direction', lambda nd: nd.getDirection()),
     (
      'bounces', lambda nd: nd.isBounceEnabled())]

    def check_attr_container(self, json_node, csb_node):
        return check_node_diff_start(json_node, csb_node)


class CCEditBoxExtCreator(CCNodeCreator):
    COM_NAME = 'CCEditBoxExt'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'text', lambda nd: nd.getString()),
     (
      'fontName', lambda nd: nd.getFontName()),
     (
      'colText', lambda nd: nd.getTextColor()),
     (
      'placeHolder', lambda nd: nd.getPlaceHolder()),
     (
      'colPlaceHolder', lambda nd: nd.getColorSpaceHolder()),
     (
      'fontSize', lambda nd: nd.getFontSize()),
     (
      'nMaxLength', lambda nd: nd.getMaxLength()),
     (
      'hAlign', lambda nd: nd.getVirtualRenderer.getHorizontalAlignment()),
     (
      'vAlign', lambda nd: nd.getVirtualRenderer.getVerticalAlignment())]


class CCClippingNodeCreator(CCNodeCreator):
    COM_NAME = 'CCClippingNode'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'displayFrame', lambda nd: CCClippingNodeCreator.check_stencil(nd)),
     (
      'alphaThreshold', lambda nd: nd.getAlphaThreshold()),
     (
      'inverted', lambda nd: nd.isInverted())]

    @staticmethod
    def check_stencil(nd):
        nd_stencil = nd.getStencil()
        if hasattr(nd_stencil, 'getTexture'):
            return nd_stencil.getTexture().getTextureFileName()
        return ''


class CCHorzAsyncListCreator(CCNodeCreator):
    COM_NAME = 'CCHorzAsyncList'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'numPerUnit', lambda nd: nd.GetNumPerUnit()),
     (
      'horzBorder', lambda nd: nd.GetHorzBorder()),
     (
      'vertBorder', lambda nd: nd.GetVertBorder()),
     (
      'horzIndent', lambda nd: nd.GetHorzIndent()),
     (
      'vertIndent', lambda nd: nd.GetVertIndent()),
     (
      'initCount', lambda nd: nd.GetItemCount()),
     (
      'bounces', lambda nd: nd.isBounceEnabled()),
     (
      'fadeInOut', --- This code section failed: ---

 654       0  LOAD_GLOBAL           0  'CCNodeCreator'
           3  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           6  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9
),
     (
      'fadeInStartPoint', --- This code section failed: ---

 655       0  LOAD_GLOBAL           0  'CCNodeCreator'
           3  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           6  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9
),
     (
      'fadeInEndPoint', --- This code section failed: ---

 656       0  LOAD_GLOBAL           0  'CCNodeCreator'
           3  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           6  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9
),
     (
      'fadeOutStartPoint', --- This code section failed: ---

 657       0  LOAD_GLOBAL           0  'CCNodeCreator'
           3  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           6  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9
),
     (
      'fadeOutEndPoint', --- This code section failed: ---

 658       0  LOAD_GLOBAL           0  'CCNodeCreator'
           3  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           6  LOAD_ATTR             1  'check_json_normal_but_csb_ext_data'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9
)]


class CCVerAsyncListCreator(CCHorzAsyncListCreator):
    COM_NAME = 'CCVerAsyncList'


class CCHorzContainerCreator(CCNodeCreator):
    COM_NAME = 'CCHorzContainer'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'numPerUnit', lambda nd: nd.GetNumPerUnit()),
     (
      'horzBorder', lambda nd: nd.GetHorzBorder()),
     (
      'vertBorder', lambda nd: nd.GetVertBorder()),
     (
      'horzIndent', lambda nd: nd.GetHorzIndent()),
     (
      'vertIndent', lambda nd: nd.GetVertIndent()),
     (
      'initCount', lambda nd: nd.GetItemCount())]


class CCVerContainerCreator(CCHorzContainerCreator):
    COM_NAME = 'CCVerContainer'


class CCHorzTemplateListCreator(CCHorzContainerCreator):
    COM_NAME = 'CCHorzTemplateList'
    ATTR_DEFINE = CCHorzContainerCreator.ATTR_DEFINE + [
     (
      'bounces', lambda nd: nd.isBounceEnabled())]


class CCVerTemplateListCreator(CCHorzTemplateListCreator):
    COM_NAME = 'CCVerTemplateList'


class CCBFileCreator(CCNodeCreator):
    COM_NAME = 'CCBFile'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + []


def get_real_type_name(nd):
    type_name = nd.GetTypeName()
    if str(type_name) != str('CCBFile'):
        return type_name
    else:
        return nd.__class__.__name__


def get_real_conf(nd):
    type_name = nd.GetTypeName()
    if str(type_name) != str('CCBFile'):
        return nd.GetConf()
    else:
        return nd.GetConf().get('__template__', {})


def get_checker_by_raw_node(json_nd):
    from common.uisys.ui_proxy import ProxyClass, trans2ProxyObj
    if not isinstance(json_nd, CCNode):
        json_nd_trans = trans2ProxyObj(json_nd)
        name = get_real_type_name(json_nd_trans)
    else:
        name = get_real_type_name(json_nd)
    print (
     'name', name, json_nd)
    if name in type_factory:
        return type_factory[name]
    else:
        if name == 'CCUIText':
            return UITextCreator
        return None


def check_diff_use_checker(json_nd, csb_nd, checker):
    print '___________________'
    from common.uisys.ui_proxy import ProxyClass, trans2ProxyObj
    from common.uisys.cocomate import wrap_cocos_node
    if hasattr(checker, 'check_attr'):
        check_attr_func = getattr(checker, 'check_attr')
    else:
        check_attr_func = None
    for attr in checker.ATTR_DEFINE:
        if True:
            attr_name, method = attr
            if hasattr(checker, 'check_attr_%s' % attr_name):
                attr_checker_method = getattr(checker, 'check_attr_%s' % attr_name)
            else:
                attr_checker_method = None
            if attr_checker_method:
                if not attr_checker_method(json_nd, csb_nd):
                    print (
                     'attr checker failed!', attr_name, json_nd, csb_nd)
            elif not callable(method) and check_attr_func:
                json_value = check_attr_func(json_nd, attr_name)
                csb_value = check_attr_func(csb_nd, attr_name)
                if not equals(json_value, csb_value):
                    json_value = check_attr_func(json_nd, attr_name)
                    csb_value = check_attr_func(csb_nd, attr_name)
                    print ('ERROR has differ in json and csb', json_nd, csb_nd, attr_name, json_value, csb_value)
            elif callable(method):
                json_value = method(json_nd)
                csb_value = method(csb_nd)
                if not equals(json_value, csb_value):
                    json_value = method(json_nd)
                    csb_value = method(csb_nd)
                    print ('ERROR has differ in json and csb', json_nd, csb_nd, attr_name, json_value, csb_value)
            else:
                print (
                 'attr_name with checker!!!!', attr_name, method, json_nd, csb_nd)

    return


def check_node_diff_start(json_node_start, csb_node_start):
    from common.uisys.ui_proxy import ProxyClass, trans2ProxyObj
    print (
     'check_node_diff_start', json_node_start, csb_node_start)

    def check_node_diff(json_nd, csb_nd):
        if json_nd and not json_nd.GetConf():
            raise ValueError('invalid json nd')
        print ('check_node_diff', json_nd, csb_nd, json_nd.GetName(), csb_nd.GetName())
        json_type_name = get_real_type_name(json_nd)
        csb_type_name = get_real_type_name(csb_nd)
        if json_type_name != csb_type_name:
            if not json_type_name == 'CCBFile':
                raise ValueError('unmatched type name', json_type_name, csb_type_name)
        if json_nd._is_created_from_conf:
            checker = get_checker_by_raw_node(json_nd)
            if checker is None:
                raise ValueError('check_diff_between_json_and_csb failed', json_nd)
            else:
                check_diff_use_checker(json_nd, csb_nd, checker())
        else:
            return True
        return

    check_node_diff(json_node_start, csb_node_start)
    json_type_name = get_real_type_name(json_node_start)
    csb_type_name = get_real_type_name(csb_node_start)
    if json_node_start.GetName() == 'btn_back':
        a = 1
    json_children = json_node_start.GetChildren()
    csb_children = csb_node_start.GetChildren()
    if json_type_name in ('CCButton', 'CCCheckButton'):
        if json_node_start._text in json_children:
            json_children.remove(json_node_start._text)
        if json_node_start._custom_click_zone in json_children:
            json_children.remove(json_node_start._custom_click_zone)
        for spt in json_node_start._display_spts.itervalues():
            if spt in json_children:
                json_children.remove(spt)

    if csb_type_name in ('CCButton', 'CCCheckButton'):
        if csb_node_start._text in csb_children:
            csb_children.remove(csb_node_start._text)
        custom_node = csb_node_start.getCustomClickZoneNode()
        if custom_node:
            custom_node_proxy = trans2ProxyObj(custom_node)
            if custom_node_proxy in csb_children:
                csb_children.remove(custom_node_proxy)
                print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        for spt in csb_node_start._display_spts.itervalues():
            if spt in csb_children:
                csb_children.remove(spt)

    list_type = ['CCScrollView',
     'CCHorzContainer',
     'CCVerContainer',
     'CCHorzTemplateList',
     'CCVerTemplateList',
     'CCHorzScrollPage',
     'CCHorzAsyncList',
     'CCVerAsyncList']
    remove_names = [
     'second_pass_node']
    for child in json_children:
        if child.GetName() in remove_names:
            json_children.remove(child)

    for child in csb_children:
        if child.GetName() in remove_names:
            csb_children.remove(child)

    if json_type_name in list_type:
        json_children = []
        for child in json_node_start.GetChildren():
            if child.widget_name != '_container' and child.widget_name != '_nodeContainer':
                json_children.append(child)

    if csb_type_name in list_type and csb_type_name not in ('CCHorzContainer', 'CCVerContainer'):
        csb_children = csb_node_start.GetScollViewChildren()
    if len(json_children) != len(csb_children):
        print (
         'children count is not equal!!!', json_children, csb_children)
        return False
    for idx, child in enumerate(json_children):
        try:
            if not check_node_diff_start(child, csb_children[idx]):
                return False
        except ValueError as e:
            raise ValueError('invalid json child', json_node_start.GetName(), csb_node_start.GetName(), idx, str(e))

    if json_type_name in list_type and json_type_name != 'CCScrollView':
        json_items = json_node_start.GetAllItem()
        csb_items = csb_node_start.GetAllItem()
        if len(json_items) != len(csb_items):
            print (
             'init count diff!!!!!', len(json_items), len(csb_items))
            return False
        for idx_j, item_json_node in enumerate(json_items):
            try:
                item_csb_node = csb_items[idx_j]
                if not check_node_diff_start(item_json_node, item_csb_node):
                    return False
            except:
                raise ValueError('invalid json items ', json_node_start.GetName(), csb_node_start.GetName(), idx_j)

    return True


def check_diff_between_json_and_csb--- This code section failed: ---

 905       0  LOAD_CONST            1  'check_diff_between_json_and_csb'
           3  LOAD_FAST             0  'relative_path'
           6  BUILD_TUPLE_2         2 
           9  PRINT_ITEM       
          10  PRINT_NEWLINE_CONT

 906      11  SETUP_EXCEPT         46  'to 60'

 907      14  LOAD_GLOBAL           0  'global_data'
          17  LOAD_ATTR             1  'uisystem'
          20  LOAD_ATTR             2  'load_template_create'
          23  LOAD_ATTR             2  'load_template_create'
          26  LOAD_GLOBAL           3  'True'
          29  CALL_FUNCTION_257   257 
          32  STORE_FAST            1  'json_tree'

 908      35  LOAD_GLOBAL           0  'global_data'
          38  LOAD_ATTR             1  'uisystem'
          41  LOAD_ATTR             2  'load_template_create'
          44  LOAD_ATTR             2  'load_template_create'
          47  LOAD_GLOBAL           4  'False'
          50  CALL_FUNCTION_257   257 
          53  STORE_FAST            2  'csb_tree'
          56  POP_BLOCK        
          57  JUMP_FORWARD         19  'to 79'
        60_0  COME_FROM                '11'

 909      60  POP_TOP          
          61  POP_TOP          
          62  POP_TOP          

 910      63  LOAD_CONST            3  'failed to load path '
          66  LOAD_FAST             0  'relative_path'
          69  BUILD_TUPLE_2         2 
          72  PRINT_ITEM       
          73  PRINT_NEWLINE_CONT

 911      74  LOAD_CONST            0  ''
          77  RETURN_VALUE     
          78  END_FINALLY      
        79_0  COME_FROM                '78'
        79_1  COME_FROM                '57'

 916      79  LOAD_GLOBAL           3  'True'
          82  POP_JUMP_IF_FALSE   104  'to 104'

 917      85  LOAD_GLOBAL           5  'check_node_diff_start'
          88  LOAD_FAST             1  'json_tree'
          91  LOAD_FAST             2  'csb_tree'
          94  CALL_FUNCTION_2       2 
          97  STORE_FAST            3  'ret'

 918     100  LOAD_FAST             3  'ret'
         103  RETURN_END_IF    
       104_0  COME_FROM                '82'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 29


def test():
    if not global_data.enable_cocos_csb:
        raise 'enable_cocos_csb is false!'
    global_data.enable_ui_add_image_async = False
    if True:
        if check_diff_between_json_and_csb('activity\\activity_main_2'):
            print "finish 'battle_before\\i_tdm_settlement_chart_item'"
    else:

        def cb(path):
            if 'gui\\template\\' in path:
                path = path[path.index('template') + len('template') + 1:]
            check_diff_between_json_and_csb(path)

        traversal_all_template(cb)


def traversal_all_template(parse_func):
    import logic

    def walk_dir(path, res_path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.json'):
                    full_path = os.path.join(root, name)
                    relative_path = os.path.relpath(full_path, res_path)
                    relative_path = relative_path[:len(relative_path) - len('.json')]
                    parse_func(relative_path)

    for res_path_name in ['res', 'res_cn']:
        res_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + res_path_name)
        walk_dir(res_path + '/gui/template', res_path)