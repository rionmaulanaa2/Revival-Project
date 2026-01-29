# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ClanShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.clan.ClanCardWidget import ClanCardWidget
from logic.manager_agents.manager_decorators import sync_exec
import game3d

class ClanShareCreator(ShareTemplateBase):
    KIND = 'CLAN_CARD_SHARE'

    def get_share_info(self):
        return (
         self._clan_widget.get_clan_info(), self._clan_widget.get_clan_commander_info())

    def __init__(self):
        super(ClanShareCreator, self).__init__()
        self._clan_id = -1
        self._init_cb = None
        self._save_rt = None
        return

    @async_disable_wrapper
    def create(self, clan_id, init_cb=None, parent=None, tmpl=None):
        self._clan_id = clan_id
        self._init_cb = init_cb
        super(ClanShareCreator, self).create(parent)
        self._init_clan_card(clan_id, init_cb)

    def recreate_panel(self):
        if self._clan_widget:
            self._clan_widget.destroy()
        self._clan_widget = None
        self.destroy_panel()
        self.create(self._clan_id, init_cb=self._init_cb, tmpl=self._tmpl)
        return

    def _init_clan_card(self, clan_id, init_cb=None):
        if not global_data.feature_mgr.is_support_share_culling():
            self.panel.pnl_bg.temp_crew_card.temp_crew_logo.nd_bar_cut.setVisible(False)
        self._clan_widget = ClanCardWidget(self, self.panel.pnl_bg.temp_crew_card, clan_id, init_cb=init_cb, need_anim=False)

    def get_show_render_texture(self):
        self.panel.pnl_content.setVisible(False)
        return self.get_render_texture()

    def get_save_render_texture(self):
        import device_compatibility
        self.panel.pnl_content.setVisible(True)
        if not self.panel:
            return
        else:
            from cocosui import cc, ccui, ccs
            size = self.panel.getContentSize()
            from logic.gutils.share_utils import get_share_size
            target_sz = get_share_size()
            if not global_data.feature_mgr.is_support_rt_skip_boundingbox_check():
                scale = min(target_sz.width / size.width, target_sz.height / size.height)
            else:
                scale = max(target_sz.width / size.width, target_sz.height / size.height)
            render_texture_size = (
             size.width * scale, size.height * scale)
            if not self._save_rt:
                from common.const import uiconst
                if game3d.get_render_device() == game3d.DEVICE_METAL:
                    rt = cc.RenderTexture.create(int(render_texture_size[0]), int(render_texture_size[1]), cc.TEXTURE2D_PIXELFORMAT_RGBA8888, uiconst.DEPTH24_STENCIL8_OES, True)
                else:
                    rt = cc.RenderTexture.create(int(render_texture_size[0]), int(render_texture_size[1]), cc.TEXTURE2D_PIXELFORMAT_RGBA8888, uiconst.DEPTH24_STENCIL8_OES)
                self._save_rt = rt
                self._save_rt.retain()
            self.panel.setAnchorPoint(cc.Vec2(0, 0))
            self.panel.SetPosition(0, 0)
            self.panel.setScale(scale)
            self.update_clan_share_rt()
            if device_compatibility.IS_DX or game3d.get_render_device() == game3d.DEVICE_METAL:
                self._save_rt.getSprite().setFlippedY(False)
            return self._save_rt

    def destroy(self):
        self._init_cb = None
        if self._clan_widget:
            self._clan_widget.destroy()
        self._clan_widget = None
        if self._save_rt:
            self._save_rt.release()
        self._save_rt = None
        super(ClanShareCreator, self).destroy()
        return

    @sync_exec
    def update_clan_share_rt(self):
        if not self.panel:
            return None
        else:
            self._save_rt.beginWithClear(0, 0, 0, 0)
            if hasattr(self._save_rt, 'addCommandsForNode'):
                self._save_rt.addCommandsForNode(self.panel.get())
            else:
                self.panel.visit()
            self._save_rt.end()
            return None