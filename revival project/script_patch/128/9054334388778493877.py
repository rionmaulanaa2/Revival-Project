# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCScale9Sprite.py
from __future__ import absolute_import
import six
import ccui
from common.uisys.ui_proxy import ProxyClass
from .CCNode import CCNode, CCNodeCreator
from common.utils.cocos_utils import ccc3FromHex, CCRect, CCRectZero
from common.uisys.color_table import get_color_val

class SecondPassNode(object):

    def SetFlippedX(self, flpped):
        self.setFlippedX(flpped)
        self._second_pass_node and self._second_pass_node.SetFlippedX(flpped)

    def SetFlippedY(self, flpped):
        self.setFlippedY(flpped)
        self._second_pass_node and self._second_pass_node.SetFlippedY(flpped)

    def SetCascadeOpacityEnabled(self, bEnable):
        super(SecondPassNode, self).SetCascadeOpacityEnabled(bEnable)
        from common.utils.cocos_ps_blend_mode_utils import update_second_pass_opacity
        self._second_pass_node and update_second_pass_opacity(self, self._second_pass_node)

    def SetOpacity(self, opacity):
        super(SecondPassNode, self).SetOpacity(opacity)
        from common.utils.cocos_ps_blend_mode_utils import update_second_pass_opacity
        self._second_pass_node and update_second_pass_opacity(self, self._second_pass_node)

    def set_ps_blend_mode(self, ps_blend_mode):
        return self._set_ps_blend_mode(ps_blend_mode)

    def _set_ps_blend_mode(self, ps_blend_mode):
        if not global_data.feature_mgr.is_scale9sprite_scripting_blendable():
            return
        else:
            from common.utils import cocos_ps_blend_mode_utils as ps_blend_utils
            factors_list = ps_blend_utils.get_ps_blend_factors_list(ps_blend_mode)
            if factors_list is None:
                return
            if ps_blend_mode == ps_blend_utils.PS_BLEND_NONE:
                self.SetBlendFunc(factors_list[0])
                self.restore_default_shader(self)
            elif ps_blend_mode == ps_blend_utils.PS_BLEND_MULTIPLY:
                self.SetBlendFunc(factors_list[0])
                ps_blend_utils.replace_multiply_shader(self)
            elif ps_blend_mode == ps_blend_utils.PS_BLEND_SCREEN:
                if len(factors_list) > 1:
                    self.SetBlendFunc(factors_list[0])
                    ps_blend_utils.replace_screen_first_pass_shader(self)
                    self._enable_second_pass_node()
                    if self._second_pass_node:
                        self._second_pass_node.setBlendFunc(factors_list[1])
                        self.restore_default_shader(self._second_pass_node)
            elif ps_blend_mode == ps_blend_utils.PS_BLEND_LINEAR_DODGE_ADD_APPROX:
                self.SetBlendFunc(factors_list[0])
                self.restore_default_shader(self)
            else:
                self.SetBlendFunc(factors_list[0])
                self.restore_default_shader(self)
            need_second_pass = ps_blend_mode == ps_blend_utils.PS_BLEND_SCREEN
            self._second_pass_node and self._second_pass_node.setVisible(need_second_pass)
            return

    def _enable_second_pass_node(self):
        if self._second_pass_node is None:
            if self.isScale9Enabled():
                obj = CCScale9Sprite.Create(self._cur_target_plist, self._cur_target_path, self._rect)
            else:
                obj = CCScale9Sprite.Create(self._cur_target_plist, self._cur_target_path, CCRectZero)
            obj.SetColor(16777215)
            from common.utils.cocos_ps_blend_mode_utils import update_second_pass_opacity
            update_second_pass_opacity(self, obj)
            obj.setFlippedX(self.isFlippedX())
            obj.setFlippedY(self.isFlippedY())
            if not self.isScale9Enabled():
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


@ProxyClass(ccui.Scale9Sprite)
class CCScale9Sprite(SecondPassNode, CCNode):

    def __init__(self, node):
        super(CCScale9Sprite, self).__init__(node)
        self._cur_path = None
        self._cur_target_plist = None
        self._cur_target_path = None
        self._rect = CCRectZero
        self._second_pass_node = None
        return

    @classmethod
    def CreateWithSpriteFrame(cls, frame, rect=CCRectZero):
        obj = cls(cls.createWithSpriteFrame(frame, rect))
        obj._rect = rect
        return obj

    @classmethod
    def Create(cls, plist, path, rect=CCRectZero):
        if False:
            obj = global_data.uisystem.CreateSpriteFrameByPathAsync(path, '', cls, ccui.Scale9Sprite, True)
        else:
            frame = global_data.uisystem.GetSpriteFrameByPath(path)
            obj = cls(cls.createWithSpriteFrame(frame, rect))
        obj._cur_path = path
        obj._cur_target_plist = plist
        obj._cur_target_path = path
        obj._rect = rect
        global_data.uisystem.RecordSpriteUsage(plist, path, obj)
        return obj

    def Destroy(self, is_remove=True):
        self._second_pass_node = None
        super(CCScale9Sprite, self).Destroy(is_remove)
        return

    def SetContentSize(self, sw, sh):
        size = self.CalcSize(sw, sh)
        self.setPreferredSize(size)
        self._second_pass_node and self._second_pass_node.SetContentSize(sw, sh)
        return size

    def GetContentSize(self):
        size = self.getPreferredSize()
        return (
         size.width, size.height)

    def SetDisplayFrameByPath(self, plist, path, callback=None, force_sync=False):
        if path == self._cur_path:
            if callback:
                callback()
            return
        w, h = self.GetContentSize()
        oldCapInsets = self.getCapInsets()
        self._cur_target_plist = plist
        self._cur_target_path = path

        def _cb(frame):
            if self.get():
                self.setSpriteFrame(frame)
            self.setCapInsets(oldCapInsets)
            self.SetContentSize(w, h)
            self._cur_path = path
            if callback:
                callback()
            global_data.uisystem.RecordSpriteUsage(plist, path, self)

        if global_data.enable_ui_add_image_async and not force_sync and not global_data.temporary_force_image_sync:
            global_data.uisystem.GetSpriteFrameByPathAsync(path, '', lambda frame: _cb(frame))
        else:
            frame = global_data.uisystem.GetSpriteFrameByPath(path, plist)
            _cb(frame)
        self._second_pass_node and self._second_pass_node.SetDisplayFrameByPath(plist, path, callback, force_sync)

    def GetDisplayFramePath(self):
        return self._cur_path

    def SetColor(self, color):
        if isinstance(color, (str, six.text_type)):
            color = get_color_val(color)
        self.setColor(ccc3FromHex(color))

    SetPath = SetDisplayFrameByPath

    def SetBlendFunc(self, blend):
        self.setBlendFunc(blend)


if not global_data.enable_ccuiimageview:

    class CCScale9SpriteCreator(CCNodeCreator):
        COM_NAME = 'CCScale9Sprite'
        ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
         (
          'spriteFrame', {'plist': '','path': 'gui/default/bg_common_c.png'}),
         (
          'capInsets', {'x': 0,'y': 0,'width': 0,'height': 0}),
         ('color', '#SW'),
         (
          'flipX', False),
         (
          'flipY', False),
         ('psBlendMode', None)]

        @staticmethod
        def create(parent, root, spriteFrame, capInsets, color, opacity, flipX, flipY, psBlendMode):
            capInsets = CCRect(capInsets['x'], capInsets['y'], capInsets['width'], capInsets['height'])
            obj = CCScale9Sprite.Create(spriteFrame['plist'], spriteFrame['path'], capInsets)
            obj.SetOpacity(opacity)
            obj.SetColor(color)
            obj.setFlippedX(flipX)
            obj.setFlippedY(flipY)
            if psBlendMode is not None:
                obj.set_ps_blend_mode(psBlendMode)
            return obj