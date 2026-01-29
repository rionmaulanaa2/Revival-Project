# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/RoleBattleShareCreator.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
import cc
from common.const import uiconst
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.manager_agents.manager_decorators import sync_exec
from common.const.neox_cocos_constant import COCOMATE_BLEND_2_HAL_BLEND_FACTOR, BLENDOP_MIN, BLEND_ONE, BLEND_INVSRCALPHA, BLENDOP_MAX, BLENDOP_ADD, BLENDOP_SUBTRACT, BLENDOP_REVSUBTRACT
import game3d

class RoleBattleShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_ROLE_BATTLE'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(RoleBattleShareCreator, self).create(parent)
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
        self.panel.img_bg.setScale(global_data.ui_mgr.design_screen_size.width / self.panel.img_bg.getContentSize().width)

    def destroy(self):
        self.panel.img_bg = None
        super(RoleBattleShareCreator, self).destroy()
        return

    def refresh_player_stat_inf(self, rank, battle_mode_str, battle_data):
        self.panel.img_rank.SetDisplayFrameByPath('', 'gui/ui_res_2/share/img_share_%s.png' % rank.lower())
        self.panel.lab_rank.SetString(get_text_by_id(609720, (battle_mode_str,)))
        self.panel.nd_data_1.SetInitCount(3)
        self.panel.nd_data_2.SetInitCount(3)
        total_cnt, win_cnt, kill_mecha_cnt, kill_human_cnt, avg_kda, win_rate = battle_data
        ls_1_data = [
         str(total_cnt), str(win_cnt), str(kill_mecha_cnt)]
        for ind in range(self.panel.nd_data_1.GetItemCount()):
            nd = self.panel.nd_data_1.GetItem(ind)
            nd.lab_data.SetString(ls_1_data[ind])

        ls_2_data = [str(kill_human_cnt), str(avg_kda), str(win_rate)]
        for ind in range(self.panel.nd_data_2.GetItemCount()):
            nd = self.panel.nd_data_2.GetItem(ind)
            nd.lab_data.SetString(ls_2_data[ind])

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