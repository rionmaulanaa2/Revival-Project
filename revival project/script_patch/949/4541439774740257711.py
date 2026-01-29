# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/LiveSpriteManager.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from common.platform.dctool import interface

class LiveSpriteManager(Singleton):

    def init(self):
        self._live_sprite_cache = {}

    def ClearCache(self):
        self._live_sprite_cache = {}

    def AddCache(self, url, image_data):
        self._live_sprite_cache[url] = image_data

    def SetSpriteByLink(self, sprite_nd, url, uid):
        if url in self._live_sprite_cache:
            self.SetSpriteByImageData(sprite_nd, self._live_sprite_cache[url], str(uid))
            return
        else:
            url = six.ensure_str(url)
            User_Agent = interface.get_project_id()
            import common.http
            sprite_nd.setVisible(False)

            def callback(ret, url, args):
                if ret:
                    msg = ret
                    self.AddCache(url, msg)
                    self.SetSpriteByImageData(sprite_nd, msg, str(uid))

            header = {'User-Agent': User_Agent}
            common.http.request_v2(url, None, header, callback)
            return

    def SetSpriteByImageData(self, sprite_nd, image_data, image_name):
        if not (sprite_nd and sprite_nd.isValid()):
            return
        from common.uisys.uielment.CCSprite import CCSprite
        from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
        from common.uisys.uielment.CCUIImageView import CCUIImageView
        import cc
        image = cc.Image.create()
        ret = image.initWithPyImageData(image_data)
        if not ret:
            log_error('SetSpriteByImageData failed! Unsupported image format! ', image_name)
            return
        tex = cc.Texture2D.create()
        tex.initWithImage(image)
        sprite_nd.setVisible(True)
        tex_size = tex.getContentSize()
        if isinstance(sprite_nd, CCSprite):
            sprite_nd.setSpriteFrame(cc.SpriteFrame.createWithTexture(tex, cc.Rect(0, 0, tex_size.width, tex_size.height)))
        elif isinstance(sprite_nd, CCScale9Sprite):
            old_size = sprite_nd.getPreferredSize()
            sprite_nd.setSpriteFrame(cc.SpriteFrame.createWithTexture(tex, cc.Rect(0, 0, tex_size.width, tex_size.height)))
            sprite_nd.setCapInsets(cc.Rect(0, 0, tex_size.width, tex_size.height))
            sprite_nd.setPreferredSize(old_size)
        elif isinstance(sprite_nd, CCUIImageView):
            old_size = sprite_nd.getVirtualRenderer().getPreferredSize()
            sprite_nd.getVirtualRenderer().setSpriteFrame(cc.SpriteFrame.createWithTexture(tex, cc.Rect(0, 0, tex_size.width, tex_size.height)))
            sprite_nd.getVirtualRenderer().setCapInsets(cc.Rect(0, 0, tex_size.width, tex_size.height))
            sprite_nd.getVirtualRenderer().setPreferredSize(old_size)