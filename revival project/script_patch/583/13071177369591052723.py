# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareTemplateBase.py
from __future__ import absolute_import
from __future__ import print_function
import time
import cc
from logic.gutils.share_utils import init_share_person_info, get_share_qr_code_pic_path
from common.cfg import confmgr
from logic.manager_agents.manager_decorators import sync_exec
from common.const.neox_cocos_constant import COCOMATE_BLEND_2_HAL_BLEND_FACTOR, BLENDOP_ADD, BLEND_ONE, BLEND_INVSRCALPHA
from logic.gutils.share_utils import get_share_size
from common.const import uiconst
import game3d
template_hide_count = 0

def async_disable_wrapper(func):

    def func_wrapper(*args, **kwargs):
        global template_hide_count
        global_data.temporary_force_image_sync = True
        if template_hide_count < 0:
            template_hide_count = 0
        template_hide_count += 1
        if func:
            func(*args, **kwargs)
        template_hide_count -= 1
        if template_hide_count <= 0:
            global_data.temporary_force_image_sync = False

    return func_wrapper


class ShareTemplateBase(object):
    KIND = ''

    def __init__(self):
        self.panel = None
        self.data = None
        self._rt = None
        self._tmpl = None
        self._last_update_render_texture_time = 0
        self.init_event()
        return

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        conf = confmgr.get('c_share_template_info', self.KIND, default={})
        if tmpl is None:
            tmpl = conf.get('cTemplate', '')
        self._tmpl = tmpl
        if self.panel:
            if self.panel.GetTemplatePath() != tmpl:
                self.panel.release()
                self.panel = None
        if not self.panel:
            self.panel = global_data.uisystem.load_template_create(tmpl, None)
            self.panel.retain()
        base_node_name = conf.get('cBaseNode', '')
        if not base_node_name:
            base_node = self.panel
        else:
            base_node = getattr(self.panel, base_node_name)
        self.base_node = base_node
        self.head_node_name = conf.get('cPersonNode', '')
        self.base_init_head(conf.get('cPersonNode', ''))
        self.init_download_qr_code(base_node)
        if global_data.is_pc_mode:
            global_data.player.call_server_method('share_succ')
        return

    def recreate_panel(self):
        self.destroy_panel()
        self.create(tmpl=self._tmpl)

    def hide_all_player_head_nodes(self):
        if self.base_node:
            name_nodes = ['nd_player_info_1', 'nd_player_info_2']
            for name_nd in name_nodes:
                nd = getattr(self.base_node, name_nd)
                if nd:
                    nd.setVisible(False)

    def __del__(self):
        self.destroy()

    @async_disable_wrapper
    def base_init_head(self, head_node_name):
        self.hide_all_player_head_nodes()
        if not self.base_node:
            return
        nd_name = head_node_name
        if nd_name:
            nd = getattr(self.base_node, nd_name)
            if nd and global_data.player:
                nd.setVisible(True)
                init_share_person_info(nd, global_data.player.get_name(), global_data.player.uid)
                from logic.gutils import role_head_utils
                if global_data.feature_mgr.is_support_share_culling():
                    pl = global_data.player
                    role_head_utils.init_role_head(nd.temp_head, pl.get_head_frame(), pl.get_head_photo())
                else:
                    res_path = role_head_utils.get_head_photo_res_path(global_data.player.get_head_photo())
                    nd.img_head.SetDisplayFrameByPath('', res_path)
                    nd.temp_head.setVisible(False)
                    nd.img_head.setVisible(True)

    def init_download_qr_code(self, base_nd):
        img_path = get_share_qr_code_pic_path()
        print('img_path', img_path)
        if base_nd and base_nd.img_qr_bg:
            if img_path:
                base_nd.img_qr_bg.setVisible(True)
                base_nd.img_qr_code.SetDisplayFrameByPath('', img_path)
            else:
                base_nd.img_qr_bg.setVisible(False)
        elif base_nd and base_nd.img_qr_code:
            if img_path:
                base_nd.img_qr_code.setVisible(True)
                base_nd.img_qr_code.SetDisplayFrameByPath('', img_path)
            else:
                base_nd.img_qr_code.setVisible(False)

    def set_qr_code_vis(self, vis):
        base_nd = self.base_node
        if base_nd and base_nd.img_qr_bg:
            base_nd.img_qr_bg.setVisible(vis)

    def set_head_nd_vis(self, vis):
        if not self.base_node:
            return
        if not vis:
            self.hide_all_player_head_nodes()
        else:
            self.base_init_head(self.head_node_name)

    def check_need_show_text(self):
        from common.cfg import confmgr
        return confmgr.get('c_share_template_info', self.KIND, default={}).get('iShowText', 0)

    def destroy_panel(self):
        if self.panel:
            self.panel.release()
        self.panel = None
        if self._rt:
            self._rt.release()
        self._rt = None
        return

    def destroy(self):
        self.destroy_panel()
        self.data = None
        return

    def get_render_texture_size_scale(self):
        size = self.panel.getContentSize()
        target_sz = get_share_size()
        if not global_data.feature_mgr.is_support_rt_skip_boundingbox_check():
            scale = min(target_sz.width / size.width, target_sz.height / size.height)
        else:
            scale = max(target_sz.width / size.width, target_sz.height / size.height)
        return ((size.width * scale, size.height * scale), scale)

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

    def init_event(self):
        global_data.emgr.resolution_changed += self.on_resolution_changed

    @sync_exec
    def on_resolution_changed(self):
        self.recreate_panel()

    @sync_exec
    def update_render_texture(self):
        if not self.panel or not self._rt:
            return None
        else:
            if self._rt and hasattr(self._rt, 'setBlendState'):
                self._rt.setBlendState(True, COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_ONE), COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_INVSRCALPHA), BLENDOP_ADD)
            self._rt.beginWithClear(0, 0, 0, 0)
            if hasattr(self._rt, 'addCommandsForNode'):
                self._rt.addCommandsForNode(self.panel.get())
            else:
                self.panel.visit()
            self._rt.end()
            return None

    def get_module_show_slot_pic(self, called_mecha_type):
        sprite_path = 'gui/ui_res_2/share/mech_%s.png' % str(called_mecha_type)
        import cc
        if cc.FileUtils.getInstance().isFileExist(sprite_path):
            return sprite_path
        if global_data.uisystem.GetSpriteFramePlistByPath(sprite_path):
            return sprite_path
        return 'gui/ui_res_2/share/mech_8001.png'

    def get_prefer_mecha_type(self):
        called_mecha_type = None
        if global_data.player:
            if global_data.player.logic:
                called_mecha_type = global_data.player.logic.ev_g_get_bind_mecha_type()
            if not called_mecha_type:
                called_mecha_type = global_data.player.get_lobby_selected_mecha_id()
        if not called_mecha_type:
            called_mecha_type = 8001
        return called_mecha_type

    def update_mecha_sprite_bg(self, mecha_type=None):
        if not mecha_type:
            mecha_type = self.get_prefer_mecha_type()
        base_node = self.base_node
        mecha_sprite = self.get_module_show_slot_pic(mecha_type)
        if base_node:
            base_node.img_bg.SetDisplayFrameByPath('', mecha_sprite)

    def get_ui_bg_sprite(self):
        return None