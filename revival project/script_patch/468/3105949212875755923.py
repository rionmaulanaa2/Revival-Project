# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/homeland/ShowShareImgUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_TYPE_CONFIRM
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst
from logic.client.const import share_const
from logic.gutils.share_utils import is_share_enable
from logic.gutils.share_utils import confirm_save_to_gallery

class ShowShareImgUI(BasePanel):
    PANEL_CONFIG_NAME = 'share/share_normal'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer',
       'temp_btn_close.btn_back.OnClick': 'on_click_close_btn',
       'pnl_btn_save.btn_common.OnClick': 'on_click_save_btn'
       }
    GLOBAL_EVENT = {'net_reconnect_event': '_on_reconnected'
       }

    def on_resolution_changed(self):
        self.close()

    def on_init_panel(self):
        self.c_path = None
        self.share_type = share_const.TYPE_IMAGE
        self.panel.pnl_btn_save.setVisible(False)
        self.panel.pnl_share_picture.setVisible(False)
        self.panel.temp_login.setVisible(True)
        self.panel.temp_login.PlayAnimation('login')
        if not is_share_enable():
            self.panel.pnl_list_share.setVisible(False)
        self.init_platform_list()
        return

    def init_platform_list(self):
        from logic.comsys.share.ShareManager import ShareManager
        import game3d
        platform_list = ShareManager().get_support_platform(self.share_type)
        share_redbook = 1 if not G_IS_NA_PROJECT and game3d.get_platform() != game3d.PLATFORM_WIN32 and global_data.channel.get_name() not in ('bilibili_sdk', ) else 0
        self.panel.pnl_list_share.SetInitCount(len(platform_list) + share_redbook)
        for idx, pf_info in enumerate(platform_list):
            ui_item = self.panel.pnl_list_share.GetItem(idx)
            if not ui_item:
                continue
            self._init_platform_btn(ui_item, pf_info)

        if share_redbook and not G_IS_NA_PROJECT:
            self._init_red_book_btn(self.panel.pnl_list_share.GetItem(len(platform_list)))

    def _init_red_book_btn(self, item):
        import game3d
        if not item:
            return
        else:
            pic = 'gui/ui_res_2/share/7.png'
            item.btn_share.SetFrames('', [pic, pic, pic], False, None)

            def on_click_rb():
                if not (self.panel and self.panel.isVisible()):
                    return
                if not game3d.open_url('xhsdiscover://webview/www.xiaohongshu.com/fe/growthgame/lottery/homepage?naviHidden=yes&activityVersion=No20221215T1&activityType=jidong2&templateId=lottery&source=openplatform_smc'):
                    game3d.open_url('https://www.xiaohongshu.com/fe/growthgame/lottery/homepage?naviHidden=yes&activityVersion=No20221215T1&activityType=jidong2&templateId=lottery&source=openplatform_smc')
                global_data.player and global_data.player.share()

            @item.btn_share.unique_callback()
            def OnClick(btn, touch):
                on_click_rb()

            return

    def _init_platform_btn(self, nd, data):
        pic = data.get('pic', '')
        share_args = data.get('share_args', ())
        nd.btn_share.SetFrames('', [pic, pic, pic], False, None)

        def on_ready():
            if not (self.panel and self.panel.isVisible()):
                return
            if not self.c_path:
                return
            from logic.comsys.share.ShareManager import ShareManager
            ShareManager().share(share_args, share_const.TYPE_IMAGE, self.c_path)

        @nd.btn_share.unique_callback()
        def OnClick(btn, touch):
            on_ready()

        return

    def set_img_info(self, img_url):
        from common.platform.filePicker import FilePicker
        from logic.comsys.video import video_record_utils as vru
        import os
        import cc

        def down_cb(ret, status_code, content):
            if not (self.panel and self.panel.isValid()):
                return
            from common.utils.path import get_neox_dir
            from patch.patch_path import get_download_target_path
            import C_file
            sprite_path = 'home_land_share.png'
            c_path = get_neox_dir() + '/' + get_download_target_path('res/' + sprite_path)
            index = c_path.rfind('/')
            dirs = c_path[0:index]
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            try:
                with open(c_path, 'wb') as tmp_file:
                    tmp_file.write(content)
                C_file.set_fileloader_enable('patch', True)
                cc.SpriteFrameCache.getInstance().removeUnusedSpriteFrames()
                cc.Director.getInstance().getTextureCache().removeUnusedTextures()
                vru.cal_and_set_cover_node(sprite_path, self.panel.pnl_share_crew, vru.SCALE_MODE_FILL)
                self.c_path = c_path
                self.panel.pnl_btn_save.setVisible(True)
                self.panel.PlayAnimation('appear')
                self.panel.temp_login.setVisible(False)
            except Exception as e:
                global_data.game_mgr.show_tip(get_text_by_id(3131))
                log_error('[cover_down_cb] write to cover error:[%s]' % str(e))
                return

        def cover_down_cb(ret, status_code, content):
            global_data.game_mgr.next_exec(lambda : down_cb(ret, status_code, content))

        FilePicker().download_from_filepicker(str(img_url), callback=cover_down_cb, mode=1)

    def on_click_save_btn(self, btn, touch):
        if not self.c_path:
            return
        confirm_save_to_gallery(self.c_path)

    def on_finalize_panel(self):
        pass

    def on_click_bg_layer(self, btn, touch):
        self.close()

    def on_click_close_btn(self, btn, touch):
        self.close()

    def _on_reconnected(self):
        self.close()