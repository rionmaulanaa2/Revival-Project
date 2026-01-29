# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCUIImageView.py
from __future__ import absolute_import
import ccui
import cc
from .CCNode import CCNodeCreator
from .CCScale9Sprite import SecondPassNode
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode
from common.utils.cocos_utils import CCRect, CCRectZero
from common.utils.cocos_utils import BlendValue, BlendFactorMap

@ProxyClass(ccui.ImageView)
class CCUIImageView(SecondPassNode, CCNode):

    def __init__(self, node):
        super(CCUIImageView, self).__init__(node)
        self.splendor_texs = []
        self._texture_infos = {}
        self._cur_path = None
        self._cur_target_plist = None
        self._cur_target_path = None
        self._loaded_callbacks = []
        self._rect = CCRectZero
        self._second_pass_node = None
        self._has_blend_func = None
        return

    @classmethod
    def CreateWithSpriteFrame(cls, frame, rect=CCRectZero):
        obj = cls(cls.create())
        obj.getVirtualRenderer().setSpriteFrame(frame)
        obj._rect = rect
        obj.setScale9Enabled(True)
        obj.setCapInsets(rect)
        return obj

    @classmethod
    def Create(cls, plist=None, path=None, rect=CCRectZero):
        if not path:
            nd = cls.create()
            return cls(nd)
        else:
            obj = cls(cls.create())
            obj.setScale9Enabled(True)
            obj.setCapInsets(rect)
            obj._rect = rect
            obj._cur_target_plist = plist
            obj._cur_target_path = path

            def _cb(path, plist, obj):
                if obj and obj.get():
                    obj.loadTexture(path, ccui.WIDGET_TEXTURERESTYPE_PLIST if plist else ccui.WIDGET_TEXTURERESTYPE_LOCAL)
                    obj.setCapInsets(rect)
                    obj._cur_path = path
                    for wait_cb in obj._loaded_callbacks:
                        wait_cb()

                    obj._loaded_callbacks = []
                    global_data.uisystem.RecordSpriteUsage(obj._cur_target_plist, obj._cur_target_path, obj)

            def _cb_async(new_path, new_plist, from_path, new_obj):
                if from_path != new_obj._cur_target_path:
                    return
                _cb(new_path, new_plist, new_obj)
                new_obj.setOpacity(new_obj.getOpacity())

            if global_data.enable_ui_add_image_async and not global_data.temporary_force_image_sync:
                global_data.uisystem.GetSpritePathAndPlistAsync(path, plist, lambda path, plist, _obj=obj, from_path=path: _cb_async(path, plist, from_path, _obj))
            else:
                path, plist = global_data.uisystem.GetSpritePathAndPlist(path, plist)
                global_data.uisystem.RecordSpriteUsage(plist, path, obj)
                obj.loadTexture(path, ccui.WIDGET_TEXTURERESTYPE_PLIST if plist else ccui.WIDGET_TEXTURERESTYPE_LOCAL)
                obj.setCapInsets(rect)
                obj._cur_path = path
                for wait_cb in obj._loaded_callbacks:
                    wait_cb()

                obj._loaded_callbacks = []
            return obj

    def csb_init(self):
        super(CCUIImageView, self).csb_init()
        self._cur_path = self.getTextureFilename()

    def SetDisplayFrameByPath(self, plist, path, callback=None, force_sync=False):
        if path == '' or path == self._cur_target_path:
            if callback:
                callback()
            return
        self._cur_target_plist = plist
        self._cur_target_path = path

        def _cb(new_path, new_plist):
            sz = self.getContentSize()
            oldCapInsets = self.getCapInsets()
            self.loadTexture(new_path, ccui.WIDGET_TEXTURERESTYPE_PLIST if new_plist else ccui.WIDGET_TEXTURERESTYPE_LOCAL)
            self.setCapInsets(oldCapInsets)
            self.setContentSize(sz)
            self._cur_path = path
            if callback:
                callback()
            if self._loaded_callbacks:
                for wait_cb in self._loaded_callbacks:
                    wait_cb()

                self._loaded_callbacks = []
            global_data.uisystem.RecordSpriteUsage(self._cur_target_plist, self._cur_target_path, self)

        def _cb_async(new_path, new_plist, from_path):
            if from_path != self._cur_target_path:
                return
            _cb(new_path, new_plist)
            self.setOpacity(self.getOpacity())

        if global_data.enable_ui_add_image_async and not force_sync and not global_data.temporary_force_image_sync:
            if global_data.feature_mgr.is_support_cocos_csb():
                self.setTextureInfo(path, plist or '')
            global_data.uisystem.GetSpritePathAndPlistAsync(path, plist, lambda o_path, o_plist: _cb_async(o_path, o_plist, path))
        else:
            path, plist = global_data.uisystem.GetSpritePathAndPlist(path, plist)
            _cb(path, plist)
        self._second_pass_node and self._second_pass_node.SetDisplayFrameByPath(plist, path, callback, force_sync)

    def Destroy(self, is_remove=True):
        self._second_pass_node = None
        self._texture_infos.clear()
        for tex2d in self.splendor_texs:
            tex2d.release()

        self.splendor_texs = []
        self._loaded_callbacks = []
        super(CCUIImageView, self).Destroy(is_remove)
        return

    def SetContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setContentSize(size)
        self._second_pass_node and self._second_pass_node.SetContentSize(sw, sh)
        return size

    def GetDisplayFramePath(self):
        return self._cur_path

    SetPath = SetDisplayFrameByPath

    def SetBlendFunc(self, blend):
        if self._has_blend_func is None:
            self._has_blend_func = hasattr(self.getVirtualRenderer(), 'setBlendFunc')
        if self._has_blend_func:
            self.getVirtualRenderer().setBlendFunc(blend)
        return

    def WaitOnSpriteLoaded(self, callback):
        if self._cur_target_path == self._cur_path:
            if callback:
                callback()
            return
        self._loaded_callbacks.append(callback)

    def SetUniformTexture(self, tex_name, tex_path):
        self._texture_infos[tex_name] = tex_path
        if global_data.enable_ui_add_image_async and not global_data.temporary_force_image_sync:
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
        if tex2d:
            programState = self.getGLProgramState()
            programState.setUniformTexture(tex_name, tex2d)
            tex2d.retain()
            self.splendor_texs.append(tex2d)

    def getPreferredSize(self):
        return self.getContentSize()

    def setPreferredSize(self, sz):
        self.setContentSize(sz)


if global_data.enable_ccuiimageview:

    class UIImageViewCreator(CCNodeCreator):
        COM_NAME = 'CCScale9Sprite'
        ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
         (
          'spriteFrame', {'plist': '','path': 'gui/default/bg_common_c.png'}),
         (
          'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
         ('color', '#SW'),
         (
          'blendFun', {'src': BlendValue['BLEND_ONE'],'dst': BlendValue['BLEND_INVSRCALPHA']}),
         (
          'flipX', False),
         (
          'flipY', False),
         ('psBlendMode', None)]

        @staticmethod
        def create(parent, root, spriteFrame, capInsets, color, opacity, blendFun, flipX, flipY, psBlendMode):
            capInsets = CCRect(capInsets['x'], capInsets['y'], capInsets['width'], capInsets['height'])
            obj = CCUIImageView.Create(spriteFrame['plist'], spriteFrame['path'], capInsets)
            obj.SetOpacity(opacity)
            obj.SetColor(color)
            obj.SetBlendFunc((blendFun['src'], blendFun['dst']))
            obj.setFlippedX(flipX)
            obj.setFlippedY(flipY)
            if psBlendMode is not None:
                obj.set_ps_blend_mode(psBlendMode)
            return obj

        @staticmethod
        def check_config--- This code section failed: ---

 238       0  LOAD_FAST             0  'conf'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'blendFun'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'blendConf'

 239      18  LOAD_FAST             1  'blendConf'
          21  POP_JUMP_IF_FALSE    64  'to 64'

 240      24  BUILD_MAP_2           2 
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