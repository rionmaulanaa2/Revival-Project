# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCSprite.py
from __future__ import absolute_import
import six
import cc
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from common.utils.cocos_utils import BlendValue, BlendFactorMap, ccc3FromHex
from common.uisys.color_table import get_color_val

@ProxyClass(cc.Sprite)
class CCSprite(CCNode):

    def __init__(self, node):
        super(CCSprite, self).__init__(node)
        self.splendor_texs = []
        self._cur_path = None
        self._cur_target_plist = None
        self._cur_target_path = None
        self._texture_infos = {}
        self._second_pass_node = None
        self._is_splendor_shader = False
        self._loaded_callbacks = []
        return

    @classmethod
    def CreateWithSpriteFrame(cls, frame):
        if frame is None:
            frame = global_data.uisystem.GetSpriteFrameByPath(global_data.uisystem.fallback_sprite, '')
        if frame:
            obj = cls(cls.createWithSpriteFrame(frame))
        else:
            obj = cls(cls.create())
        return obj

    def csb_init--- This code section failed: ---

  41       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'CCSprite'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'csb_init'
          15  CALL_FUNCTION_0       0 
          18  POP_TOP          

  43      19  LOAD_CONST            1  ''
          22  LOAD_CONST            2  ('get_ext_data', 'com_attr_name', 'key_splendor_filename')
          25  IMPORT_NAME           3  'common.uisys.cocomate'
          28  IMPORT_FROM           4  'get_ext_data'
          31  STORE_FAST            1  'get_ext_data'
          34  IMPORT_FROM           5  'com_attr_name'
          37  STORE_FAST            2  'com_attr_name'
          40  IMPORT_FROM           6  'key_splendor_filename'
          43  STORE_FAST            3  'key_splendor_filename'
          46  POP_TOP          

  46      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             7  'getComponent'
          53  LOAD_FAST             2  'com_attr_name'
          56  CALL_FUNCTION_1       1 
          59  STORE_FAST            4  'com_attr'

  47      62  LOAD_FAST             4  'com_attr'
          65  POP_JUMP_IF_FALSE   104  'to 104'

  48      68  LOAD_FAST             4  'com_attr'
          71  LOAD_ATTR             8  'getString'
          74  LOAD_FAST             3  'key_splendor_filename'
          77  LOAD_CONST            3  ''
          80  CALL_FUNCTION_2       2 
          83  STORE_FAST            5  'splendor_filename'

  49      86  LOAD_GLOBAL           9  'bool'
          89  LOAD_FAST             5  'splendor_filename'
          92  CALL_FUNCTION_1       1 
          95  LOAD_FAST             0  'self'
          98  STORE_ATTR           10  '_is_splendor_shader'
         101  JUMP_FORWARD          0  'to 104'
       104_0  COME_FROM                '101'

  50     104  LOAD_FAST             0  'self'
         107  LOAD_ATTR            10  '_is_splendor_shader'
         110  POP_JUMP_IF_TRUE    156  'to 156'

  51     113  LOAD_FAST             1  'get_ext_data'
         116  LOAD_FAST             4  'com_attr'
         119  CALL_FUNCTION_2       2 
         122  STORE_FAST            6  'psBlendMode'

  52     125  LOAD_FAST             6  'psBlendMode'
         128  LOAD_CONST            0  ''
         131  COMPARE_OP            9  'is-not'
         134  POP_JUMP_IF_FALSE   156  'to 156'

  53     137  LOAD_FAST             0  'self'
         140  LOAD_ATTR            12  'set_ps_blend_mode'
         143  LOAD_FAST             6  'psBlendMode'
         146  CALL_FUNCTION_1       1 
         149  POP_TOP          
         150  JUMP_ABSOLUTE       156  'to 156'
         153  JUMP_FORWARD          0  'to 156'
       156_0  COME_FROM                '153'
         156  LOAD_CONST            0  ''
         159  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 119

    @classmethod
    def Create(cls, plist=None, path=None, force_sync=False):
        if path is None:
            nd = cls.create()
            return cls(nd)
        else:
            if global_data.enable_ui_add_image_async and not force_sync and not global_data.temporary_force_image_sync:
                obj = global_data.uisystem.CreateSpriteFrameByPathAsync(path, '', cls, cc.Sprite, False)
            else:
                frame = global_data.uisystem.GetSpriteFrameByPath(path, plist)
                obj = cls(cls.createWithSpriteFrame(frame))
                global_data.uisystem.RecordSpriteUsage(plist, path, obj)
            obj._cur_path = path
            obj.TriggerAndClearLoaderCallback()
            obj._cur_target_plist = plist
            obj._cur_target_path = path
            global_data.uisystem.RecordSpriteUsage(plist, path, obj)
            return obj
            return

    @classmethod
    def CreateWithTexture(cls, texture):
        return cls(cls.createWithTexture(texture))

    def Destroy(self, is_remove=True):
        self._second_pass_node = None
        self._texture_infos.clear()
        self._loaded_callbacks = []
        for tex2d in self.splendor_texs:
            tex2d.release()

        self.splendor_texs = []
        super(CCSprite, self).Destroy(is_remove)
        return

    def SetContentSize(self, w, h):
        if global_data.enable_ui_add_image_async:
            if self.getContentSize().width > 0:
                return
            super(CCSprite, self).SetContentSize(w, h)
        return self.getContentSize()

    def SetSpriteFrame(self, plist, path):
        self._cur_target_plist = plist
        self._cur_target_path = path
        self.setSpriteFrame(path)

    def SetDisplayFrameByPath(self, plist, path, callback=None, force_sync=False):
        if self._is_splendor_shader:
            force_sync = True
        if path == '' or path == self._cur_path:
            if callback:
                callback()
            return
        self._cur_target_plist = plist
        self._cur_target_path = path

        def _cb(frame, path):
            if self.get():
                old_size = self.getContentSize()
                self.setSpriteFrame(frame)
                new_size = self.getContentSize()
                if old_size.width <= 0 or old_size.height <= 0 or old_size.width != new_size.width or old_size.height != new_size.height:
                    self.ChildResizeAndPosition()
                    if self._second_pass_node:
                        self._second_pass_node.SetPosition('50%', '50%')
            self._cur_path = path
            self.TriggerAndClearLoaderCallback()
            if callback:
                callback()
            global_data.uisystem.RecordSpriteUsage(plist, path, self)

        if global_data.enable_ui_add_image_async and not force_sync and not global_data.temporary_force_image_sync:

            def _cb_async(frame, path):
                if path != self._cur_target_path:
                    return
                _cb(frame, path)

            if global_data.feature_mgr.is_support_cocos_csb():
                self.setTextureInfo(path, plist or '')
            global_data.uisystem.GetSpriteFrameByPathAsync(path, plist, lambda _frame, _path=path: _cb_async(_frame, _path))
        else:
            frame = global_data.uisystem.GetSpriteFrameByPath(path, plist)
            _cb(frame, path)
        self._second_pass_node and self._second_pass_node.SetDisplayFrameByPath(plist, path, callback, force_sync)

    def GetDisplayFramePath(self):
        return self._cur_path

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color = get_color_val(color)
        self.setColor(ccc3FromHex(color))

    def SetUniformTexture(self, tex_name, tex_path):
        if tex_name in self._texture_infos and self._texture_infos[tex_name] == tex_path:
            return
        self._texture_infos[tex_name] = tex_path
        if global_data.enable_ui_add_image_async and not global_data.temporary_force_image_sync:
            if global_data.is_inner_server:
                if cc.ResManager.getInstance().getImgPlistPath(tex_path):
                    log_error('when in plist, callback will not be called!', tex_path)
            cc.Director.getInstance().getTextureCache().addImageAsync(tex_path, lambda tex2d, tex_name=tex_name: self.OnSetUniformTexture(tex2d, tex_name))
        else:
            programState = self.getGLProgramState()
            tex2d = cc.Director.getInstance().getTextureCache().addImage(tex_path)
            if tex2d:
                programState.setUniformTexture(tex_name, tex2d)
                tex2d.retain()
                self.splendor_texs.append(tex2d)
        if global_data.is_inner_server:
            global_data.uisystem.RecordSpriteUsage('', tex_path, self)

    def OnSetUniformTexture(self, tex2d, tex_name):
        if self.IsDestroyed():
            return
        if tex2d:
            programState = self.getGLProgramState()
            programState.setUniformTexture(tex_name, tex2d)
            tex2d.retain()
            self.splendor_texs.append(tex2d)

    def SetFlippedX(self, flpped):
        self.setFlippedX(flpped)
        self._second_pass_node and self._second_pass_node.SetFlippedX(flpped)

    def SetFlippedY(self, flpped):
        self.setFlippedY(flpped)
        self._second_pass_node and self._second_pass_node.SetFlippedY(flpped)

    def SetCascadeOpacityEnabled(self, bEnable):
        super(CCSprite, self).SetCascadeOpacityEnabled(bEnable)
        from common.utils.cocos_ps_blend_mode_utils import update_second_pass_opacity
        self._second_pass_node and update_second_pass_opacity(self, self._second_pass_node)

    def SetOpacity(self, opacity):
        super(CCSprite, self).SetOpacity(opacity)
        from common.utils.cocos_ps_blend_mode_utils import update_second_pass_opacity
        self._second_pass_node and update_second_pass_opacity(self, self._second_pass_node)

    def set_ps_blend_mode(self, ps_blend_mode):
        return self._set_ps_blend_mode(ps_blend_mode)

    def _set_ps_blend_mode(self, ps_blend_mode):
        from common.utils import cocos_ps_blend_mode_utils as ps_blend_utils
        factors_list = ps_blend_utils.get_ps_blend_factors_list(ps_blend_mode)
        if factors_list is None:
            return
        else:
            if ps_blend_mode == ps_blend_utils.PS_BLEND_NONE:
                self.setBlendFunc(factors_list[0])
                self.restore_default_shader(self)
            elif ps_blend_mode == ps_blend_utils.PS_BLEND_MULTIPLY:
                self.setBlendFunc(factors_list[0])
                ps_blend_utils.replace_multiply_shader(self)
            elif ps_blend_mode == ps_blend_utils.PS_BLEND_SCREEN:
                if len(factors_list) > 1:
                    self.setBlendFunc(factors_list[0])
                    ps_blend_utils.replace_screen_first_pass_shader(self)
                    self._enable_second_pass_node()
                    if self._second_pass_node:
                        self._second_pass_node.setBlendFunc(factors_list[1])
                        self.restore_default_shader(self._second_pass_node)
            elif ps_blend_mode == ps_blend_utils.PS_BLEND_LINEAR_DODGE_ADD_APPROX:
                self.setBlendFunc(factors_list[0])
                self.restore_default_shader(self)
            else:
                self.setBlendFunc(factors_list[0])
                self.restore_default_shader(self)
            need_second_pass = ps_blend_mode == ps_blend_utils.PS_BLEND_SCREEN
            self._second_pass_node and self._second_pass_node.setVisible(need_second_pass)
            return

    def _enable_second_pass_node(self):
        if self._second_pass_node is None:
            obj = CCSprite.Create(self._cur_target_plist, self._cur_target_path)
            obj.SetColor(16777215)
            from common.utils.cocos_ps_blend_mode_utils import update_second_pass_opacity
            update_second_pass_opacity(self, obj)
            obj.setFlippedX(self.isFlippedX())
            obj.setFlippedY(self.isFlippedY())
            for tex_name, tex_path in six.iteritems(self._texture_infos):
                obj.SetUniformTexture(tex_name, tex_path)

            self.AddChild('second_pass_node', obj, Z=0)
            from common.utils.cocos_utils import ccp
            obj.setAnchorPoint(ccp(0.5, 0.5))
            obj.SetPosition('50%', '50%')
            self._second_pass_node = obj
            children = self.GetChildren()
            smallest_ooa = None
            for child in children:
                ooa = child.getOrderOfArrival()
                if smallest_ooa is None or ooa < smallest_ooa:
                    smallest_ooa = ooa

            if smallest_ooa:
                self._second_pass_node.setOrderOfArrival(smallest_ooa - 1)
        return

    @classmethod
    def restore_default_shader(cls, node):
        from common.utils import cocos_utils
        state = cocos_utils.create_program_state_by_path('common/shader/cocosui', 'positiontexturecolor_nomvp')
        node.setGLProgramState(state)

    def SetBlendFunc(self, blend):
        self.setBlendFunc(blend)

    def WaitOnSpriteLoaded(self, callback):
        if self._cur_target_path == self._cur_path:
            if callback:
                callback()
            return
        self._loaded_callbacks.append(callback)

    def TriggerAndClearLoaderCallback(self):
        for wait_cb in self._loaded_callbacks:
            wait_cb()

        self._loaded_callbacks = []


class CCSpriteCreator(CCNodeCreator):
    COM_NAME = 'CCSprite'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     (
      'displayFrame', {'plist': '','path': 'gui/default/default_sprite.png'}),
     ('color', '#SW'),
     (
      'blendFun', {'src': BlendValue['BLEND_ONE'],'dst': BlendValue['BLEND_INVSRCALPHA']}),
     ('shaderName', ''),
     (
      'textures', {}),
     (
      'flipX', False),
     (
      'flipY', False),
     ('psBlendMode', None)]

    @staticmethod
    def create(parent, root, displayFrame, color, opacity, blendFun, shaderName, textures, flipX, flipY):
        need_get_frame = False
        if global_data.is_32bit:
            if displayFrame['path']:
                need_get_frame = True
            if displayFrame['plist']:
                need_get_frame = False
        else:
            need_get_frame = displayFrame['path'] or displayFrame['plist']
        if need_get_frame:
            if global_data.enable_ui_add_image_async and not global_data.temporary_force_image_sync:

                def _cb(frame, obj, _path):
                    if _path != obj._cur_target_path:
                        return
                    if obj and obj.get() and frame:
                        old_size = obj.getContentSize()
                        obj.setSpriteFrame(frame)
                        obj._cur_path = obj._cur_target_path
                        obj.TriggerAndClearLoaderCallback()
                        new_size = obj.getContentSize()
                        if old_size.width <= 0 or old_size.height <= 0 or old_size.width != new_size.width or old_size.height != new_size.height:
                            obj.ChildResizeAndPosition()
                    elif obj and obj.get():
                        obj.TriggerAndClearLoaderCallback()
                    global_data.uisystem.RecordSpriteUsage(displayFrame['plist'], displayFrame['path'], obj)

                obj = CCSprite.Create()
                obj._cur_target_plist = displayFrame['plist']
                obj._cur_target_path = displayFrame['path']
                global_data.uisystem.GetSpriteFrameByPathAsync(displayFrame['path'], displayFrame['plist'], lambda _frame, _obj=obj, _path=displayFrame['path']: _cb(_frame, _obj, _path))
            else:
                frame = global_data.uisystem.GetSpriteFrameByPath(displayFrame['path'], displayFrame['plist'])
                obj = CCSprite.CreateWithSpriteFrame(frame)
                obj._cur_target_plist = displayFrame['plist']
                obj._cur_target_path = displayFrame['path']
                obj._cur_path = displayFrame['path']
                obj.TriggerAndClearLoaderCallback()
                global_data.uisystem.RecordSpriteUsage(displayFrame['plist'], displayFrame['path'], obj)
        else:
            obj = CCSprite.Create()
        obj.SetColor(color)
        obj.SetOpacity(opacity)
        obj.setBlendFunc((blendFun['src'], blendFun['dst']))
        obj.setFlippedX(flipX)
        obj.setFlippedY(flipY)
        use_splendor = False
        if shaderName and len(shaderName) > 4:
            use_splendor = True
            prefix = shaderName[:-4] + '.spx'
            program = cc.GLProgram.createWithEffectFile(prefix)
            if not program:
                log_error('INVALID SPRITE SHADER:%s' % shaderName)
                return obj
            obj.setGLProgram(program)
            obj._is_splendor_shader = True
            if type(textures) == dict:
                for tex_name, tex_path in six.iteritems(textures):
                    obj.SetUniformTexture(tex_name, tex_path)

        return obj

    @staticmethod
    def set_attr_group_created(obj, parent, root, psBlendMode):
        if not obj._is_splendor_shader:
            if psBlendMode is not None:
                obj.set_ps_blend_mode(psBlendMode)
        return

    @staticmethod
    def check_config--- This code section failed: ---

 412       0  LOAD_FAST             0  'conf'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'blendFun'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'blendConf'

 413      18  LOAD_FAST             1  'blendConf'
          21  POP_JUMP_IF_FALSE    64  'to 64'

 414      24  BUILD_MAP_2           2 
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