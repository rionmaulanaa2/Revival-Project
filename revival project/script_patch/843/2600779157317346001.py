# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/RoleCollectShareCreator.py
from __future__ import absolute_import
import cc
from common.const import uiconst
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.gcommon.item import item_const
from logic.manager_agents.manager_decorators import sync_exec
from common.const.neox_cocos_constant import COCOMATE_BLEND_2_HAL_BLEND_FACTOR, BLENDOP_MIN, BLEND_ONE, BLEND_INVSRCALPHA, BLENDOP_MAX, BLENDOP_ADD, BLENDOP_SUBTRACT, BLENDOP_REVSUBTRACT
import game3d

class RoleCollectShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_ROLE_COLLECT'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(RoleCollectShareCreator, self).create(parent)
        from common.uisys.uielment.CCSprite import CCSprite
        self.panel.nd_bg.AddChild('img_bg', CCSprite.Create(), -1)
        self.panel.img_bg = self.panel.nd_bg.img_bg
        import cc
        self.panel.img_bg.setAnchorPoint(cc.Vec2(0.5, 0.5))

    def get_ui_bg_sprite(self):
        return self.panel.img_bg

    def update_ui_bg_sprite(self):
        from logic.gutils.share_utils import get_share_size
        sz = get_share_size()
        from common.utils.ui_utils import get_scale
        scale = get_scale('1w')
        self.panel.setScale(scale)
        self.panel.setContentSize(global_data.ui_mgr.design_screen_size)
        self.panel.ChildResizeAndPosition()
        self.panel.img_bg.SetPosition('50%', '50%')
        bg_scale = global_data.ui_mgr.design_screen_size.width / self.panel.img_bg.getContentSize().width
        self.panel.img_bg.setScale(bg_scale)

    def destroy(self):
        self.panel.img_bg = None
        super(RoleCollectShareCreator, self).destroy()
        return

    def update_collect_state(self, player_inf):
        self.panel.lab_charm_num.SetString(str(player_inf.get('charm', 0)))
        skin_nodes = [self.panel.nd_mech, self.panel.nd_player, self.panel.nd_others]
        from logic.client.const.role_ui_const import collect_interact_type, collect_skin_item_types
        item_types = collect_skin_item_types
        item_stat = player_inf.get('item_stat', {})
        for idx, skin_node in enumerate(skin_nodes):
            skin_type, s_skin_type = item_types[idx]
            skin_num = item_stat.get(str(skin_type), 0)
            s_skin_num = item_stat.get(str(s_skin_type), 0)
            skin_node.lab_num.setString(str(skin_num))
            skin_node.lab_s_num.setString(str(s_skin_num))

        interact_type = collect_interact_type
        interact_img_name = [
         'graffiti', 'emoji', 'action', 'avatar', 'avatar_frame', 'chat_frame']
        interact_name = [
         81233, 81234, 81235, 81299, 80780, 81159]
        self.panel.list_collect.SetInitCount(len(interact_type))
        for idx, item in enumerate(self.panel.list_collect.GetAllItem()):
            num = item_stat.get(str(interact_type[idx]), 0)
            if interact_type[idx] == item_const.INV_STAT_HEAD_PHOTO and num > 0:
                num -= 1
            path = 'gui/ui_res_2/role/icon_collect_%s.png' % (interact_img_name[idx],)
            item.lab_num.setString(str(num))
            item.name.SetString(interact_name[idx])
            item.img_sort.SetDisplayFrameByPath('', path)

    def get_render_texture(self):
        if not self.panel:
            return
        else:
            import device_compatibility
            render_texture_size, scale = self.get_render_texture_size_scale()
            if not self._rt:
                if game3d.get_render_device() == game3d.DEVICE_METAL:
                    rt = cc.RenderTexture.create(int(render_texture_size[0]), int(render_texture_size[1]), cc.TEXTURE2D_PIXELFORMAT_RGBA8888, uiconst.DEPTH24_STENCIL8_OES, True)
                else:
                    rt = cc.RenderTexture.create(int(render_texture_size[0]), int(render_texture_size[1]), cc.TEXTURE2D_PIXELFORMAT_RGBA8888, uiconst.DEPTH24_STENCIL8_OES)
                if global_data.feature_mgr.is_support_rt_skip_boundingbox_check():
                    rt.setNerverCull(True)
                self._rt = rt
                self._rt.retain()
            self.panel.setAnchorPoint(cc.Vec2(0, 0))
            self.panel.SetPosition(0, 0)
            self.panel.setScale(scale)
            self.update_render_texture()
            if device_compatibility.IS_DX or game3d.get_render_device() == game3d.DEVICE_METAL:
                self._rt.getSprite().setFlippedY(False)
            return self._rt

    @sync_exec
    def update_render_texture(self):
        if not self.panel:
            return None
        else:
            if self._rt and hasattr(self._rt, 'setBlendState'):
                self._rt.setBlendState(True, COCOMATE_BLEND_2_HAL_BLEND_FACTOR(2), COCOMATE_BLEND_2_HAL_BLEND_FACTOR(5), BLENDOP_ADD)
            self._rt.beginWithClear(0, 0, 0, 0)
            if hasattr(self._rt, 'addCommandsForNode'):
                self._rt.addCommandsForNode(self.panel.get())
            else:
                self.panel.visit()
            self._rt.end()
            return None