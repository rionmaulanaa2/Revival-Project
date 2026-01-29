# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareUI.py
from __future__ import absolute_import
from six.moves import range
import cc
import game3d
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.client.const import share_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.share_utils import is_share_enable, get_pc_share_save_path
import logic.gutils.delay as delay

class ShareUI(BasePanel):
    PANEL_CONFIG_NAME = 'share/share_normal'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'pnl_btn_save.btn_common.OnClick': 'on_click_save_btn',
       'bg_layer.OnClick': 'on_click_bg_layer',
       'temp_btn_close.btn_back.OnClick': 'on_click_close_btn'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_resolution_changed(self):
        self.close()

    def on_init_panel(self, need_black_bg=True):
        self.panel.PlayAnimation('appear')
        self.content_creator = None
        self._rt = None
        self._save_rt = None
        self._is_in_saving_to_gallery = False
        self._is_in_saving_to_save_path = False
        self._is_file_ready = False
        self._friend_widget = None
        self.share_type = share_const.TYPE_IMAGE
        self.share_func = None
        self._share_inform_func = None
        self._custom_platform_check = None
        self.share_content = None
        self.init_platform_list()
        global_data.emgr.on_write_storage_cb_event += self.on_write_storage_cb
        from logic.comsys.share.ShareManager import ShareManager
        self.SHARE_SAVE_PATH = ShareManager().SHARE_SAVE_PATH
        if not is_share_enable():
            self.panel.pnl_list_share.setVisible(False)
        self.panel.bg_color.setVisible(need_black_bg)
        self._choose_list_func_list = []
        self.rb_timer = None
        self.panel.pnl_btn_save.setVisible(global_data.is_share_show)
        return

    def set_share_func(self, share_type, share_func):
        self.share_type = share_type
        self.share_func = share_func
        if not is_share_enable(self.share_type):
            self.panel.pnl_list_share.setVisible(False)
        else:
            self.panel.pnl_list_share.setVisible(True)
        self.init_platform_list()

    def on_finalize_panel(self):
        self._choose_list_func_list = []
        self.show_main_ui()
        self.share_func = None
        self._share_inform_func = None
        if self._rt and self._rt.isValid():
            self._rt.removeFromParent()
        self._rt = None
        self.content_creator = None
        self.share_content = None
        if self._save_rt and self._save_rt.isValid():
            self._save_rt.removeFromParent()
        self._save_rt = None
        if self.rb_timer:
            delay.cancel(self.rb_timer)
        self.rb_timer = None
        return

    def set_share_content_raw(self, target_nd, parent_node_name='', need_scale=True, share_content=None):
        self.share_content = share_content
        if not hasattr(target_nd, 'saveToFile'):
            log_error('should be a rendetexture!!!!')
            return
        else:
            if self._rt is not None:
                self._rt.removeFromParent()
                self._rt = None
            if parent_node_name:
                parent_node = getattr(self.panel, parent_node_name)
                self.panel.pnl_share_picture.setVisible(False)
            else:
                parent_node = self.panel.pnl_share_picture
            parent_node.setVisible(True)
            parent_node.addChild(target_nd)
            target_nd.getSprite().getTexture().setAntiAliasTexParameters()
            size = parent_node.getContentSize()
            target_nd.setPosition(cc.Vec2(size.width / 2, size.height / 2))
            target_nd.setAnchorPoint(cc.Vec2(0.5, 0.5))
            self._rt = target_nd
            from common.const.neox_cocos_constant import COCOMATE_BLEND_2_HAL_BLEND_FACTOR, BLENDOP_ADD, BLEND_ONE, BLEND_INVSRCALPHA
            sp = self._rt.getSprite()
            if sp and hasattr(sp, 'setBlendState'):
                sp.setBlendState(False, COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_ONE), COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_INVSRCALPHA), BLENDOP_ADD)
            sz = target_nd.getSprite().getContentSize()
            bg_color = getattr(parent_node, 'bg_color')
            if bg_color:
                bg_color.setContentSize(sz)
            if need_scale:
                scale = min(global_data.ui_mgr.design_screen_size.width / sz.width, global_data.ui_mgr.design_screen_size.height / sz.height)
                parent_node.setScale(scale * 0.8)
            return

    def add_custom_button(self, btn_infos, is_head=False):
        if not btn_infos:
            return
        else:
            self.panel.pnl_list_share.setVisible(True)
            for btn_info in btn_infos:
                click_cb = btn_info['click_cb']
                ctr_node = global_data.uisystem.load_template_create(btn_info['template_name'])
                if is_head:
                    btn_node = self.panel.pnl_list_share.AddControl(ctr_node, index=0)
                else:
                    btn_node = self.panel.pnl_list_share.AddControl(ctr_node)
                btn = getattr(btn_node, btn_info['btn_name'])
                btn.SetText(btn_info['btn_text'])
                if click_cb:
                    btn.BindMethod('OnClick', click_cb)
                lab_name = btn_info.get('lab_name', None)
                if lab_name:
                    lab_node = getattr(btn_node, lab_name)
                    if lab_node:
                        lab_node.SetString(btn_info.get('lab_text', ''))

            return

    def set_save_content(self, rt):
        self._save_rt = rt

    def on_saved(self, *args):
        self._is_file_ready = True

    def on_click_save_btn(self, btn, touch):
        if not global_data.is_share_show:
            return
        from logic.gutils.share_utils import huawei_permission_confirm
        permission = 'android.permission.WRITE_EXTERNAL_STORAGE'
        huawei_permission_confirm(permission, 635572, self.do_click_save_btn)

    def do_click_save_btn(self):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            if self.SHARE_SAVE_PATH.endswith('.png'):
                suffix = '.png'
            else:
                suffix = '.jpg'
            file_whole_path = get_pc_share_save_path(suffix)

            def save_callback(rt, file_name):
                global_data.game_mgr.show_tip(get_text_by_id(920706, {'path': file_whole_path}))

            self._save_rt_to_file(file_whole_path, save_callback)
            return
        if self._is_in_saving_to_gallery:
            return
        self._is_in_saving_to_gallery = True

        def on_save_to_document(rt, filename):
            self.on_saved()
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                global_data.game_mgr.show_tip(get_text_by_id(2183))
                self._is_in_saving_to_gallery = False
                return
            self._is_in_saving_to_gallery = False
            self.save_to_gallery()

        self._save_rt_to_file(self.SHARE_SAVE_PATH, on_save_to_document)

    def _save_rt_to_file(self, save_path, cb_func):
        if self._is_in_saving_to_save_path:
            return

        def to_save_path_callback(rt, filename):

            def post_func():
                self._is_in_saving_to_save_path = False
                if self.panel and self.panel.isValid() and rt and rt.isValid():
                    if cb_func:
                        cb_func(rt, filename)
                    if global_data.channel.get_app_channel() == 'steam':
                        image_size = rt.getSprite().getContentSize()
                        json_dict = {'methodId': 'AddScreenshotToLibrary',
                           'filePath': save_path,
                           'imageWidth': int(image_size.width),
                           'imageHeight': int(image_size.height)
                           }
                        global_data.channel.extend_func_by_dict(json_dict)

            global_data.game_mgr.post_exec(post_func)

        rt = self._save_rt if self._save_rt else self._rt
        if rt:
            if save_path.endswith('.png'):
                save_img_type = cc.IMAGE_FORMAT_PNG
            elif save_path.endswith('.jpg'):
                save_img_type = cc.IMAGE_FORMAT_JPG
            else:
                log_error('unsupport image type when _save_rt_to_file')
                save_img_type = cc.IMAGE_FORMAT_UNKOWN
                return
            rt.saveToFile(save_path, save_img_type, False, to_save_path_callback)
            self._is_in_saving_to_save_path = True

    def save_callback(self, ret, red_book_cb=None):
        if ret:
            global_data.game_mgr.show_tip(get_text_by_id(2183))
            if red_book_cb:
                red_book_cb()
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2184))

    def save_to_gallery(self, red_book_cb=None):

        def save_callback(ret, red_book_cb=red_book_cb):
            global_data.game_mgr.post_exec(self.save_callback, ret, red_book_cb)

        share_pic_path = self.SHARE_SAVE_PATH
        img_title = ''
        img_description = ''
        prompt_for_permission = True
        prompt_title = get_text_local_content(3002)
        prompt_msg = get_text_local_content(3003)
        prompt_btn_close = get_text_local_content(3004)
        prompt_btn_setting = get_text_local_content(3005)
        platform = game3d.get_platform()
        if platform == game3d.PLATFORM_ANDROID:
            ret = game3d.save_image_to_gallery(share_pic_path, save_callback, img_title, img_description, prompt_for_permission, prompt_title, prompt_msg, prompt_btn_close, prompt_btn_setting)
            if ret == game3d.SAVE_IMAGE_TO_GALLERY_OK or ret == game3d.SAVE_IMAGE_TO_GALLERY_FAIL:
                save_callback(ret == game3d.SAVE_IMAGE_TO_GALLERY_OK)
        elif platform == game3d.PLATFORM_IOS:
            game3d.save_image_to_gallery(share_pic_path, save_callback, img_title, img_description, prompt_for_permission, prompt_title, prompt_msg, prompt_btn_close, prompt_btn_setting)

    def on_write_storage_cb(self, result_code):
        from patch.patch_utils import show_confirm_box
        if result_code == 2:

            def confirm_go_to_setting():
                game3d.go_to_setting()

            def cancel_go_to_setting():
                pass

            show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, get_text_by_id(3119), get_text_by_id(80284), get_text_by_id(19002))
        elif result_code == 1:
            self.save_to_gallery()
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2184))

    def init_platform_list(self):
        from logic.comsys.share.ShareManager import ShareManager
        platform_list = ShareManager().get_support_platform(self.share_type)
        if self._custom_platform_check and callable(self._custom_platform_check):
            platform_list = self._custom_platform_check(platform_list)
        share_redbook = 1 if not G_IS_NA_PROJECT and game3d.get_platform() != game3d.PLATFORM_WIN32 and global_data.channel.get_name() not in ('bilibili_sdk', ) else 0
        self.panel.pnl_list_share.SetInitCount(len(platform_list) + share_redbook)
        for idx, pf_info in enumerate(platform_list):
            ui_item = self.panel.pnl_list_share.GetItem(idx)
            if not ui_item:
                continue
            self._init_platform_btn(ui_item, pf_info)

        if share_redbook and not G_IS_NA_PROJECT:
            self._init_red_book_btn(self.panel.pnl_list_share.GetItem(len(platform_list)))

    def _init_platform_btn(self, nd, data):
        pic = data.get('pic', '')
        share_args = data.get('share_args', ())
        nd.btn_share.SetFrames('', [pic, pic, pic], False, None)
        platform = share_args.get('platform_enum', None)

        def on_ready():
            from logic.comsys.share.ShareManager import ShareManager
            ShareManager().share(share_args, share_const.TYPE_IMAGE, self.SHARE_SAVE_PATH, share_inform_cb=self._share_inform_func)

        def share_callback(*args):
            self.on_saved()
            on_ready()

        @nd.btn_share.unique_callback()
        def OnClick(btn, touch):
            if self.share_func:
                self.share_func(platform)
                return
            if not self._is_file_ready:
                if self._is_in_saving_to_save_path:
                    global_data.game_mgr.show_tip(get_text_by_id(2182))
                self._save_rt_to_file(self.SHARE_SAVE_PATH, share_callback)
            else:
                on_ready()

        return

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
                if not game3d.open_url('xhsdiscover://webview/fe.xiaohongshu.com/ditto/vincent/a9ee1ef502584c00b6f419c1e10eb156?naviHidden=yes&fullscreen=true&source=splash'):
                    game3d.open_url('https://fe.xiaohongshu.com/ditto/vincent/a9ee1ef502584c00b6f419c1e10eb156?naviHidden=yes&fullscreen=true&source=splash')
                global_data.player and global_data.player.share()
                if self._share_inform_func and callable(self._share_inform_func):
                    self._share_inform_func()

            def share_callback(*args):
                self.on_saved()
                if self._is_in_saving_to_gallery:
                    return
                if game3d.get_platform() == game3d.PLATFORM_WIN32:
                    global_data.game_mgr.show_tip(get_text_by_id(2183))
                    self._is_in_saving_to_gallery = False
                    return
                self._is_in_saving_to_gallery = False
                self.save_to_gallery(on_click_rb)

            @item.btn_share.unique_callback()
            def OnClick(btn, touch):
                if self.share_content:
                    self.share_content.set_qr_code_vis(False)
                    self.share_content.update_render_texture()

                def delay_exec():
                    self.rb_timer = None
                    if self._is_in_saving_to_save_path:
                        global_data.game_mgr.show_tip(get_text_by_id(2182))
                    self._save_rt_to_file(self.SHARE_SAVE_PATH, share_callback)
                    return

                if not self.rb_timer:
                    self.rb_timer = delay.call(0.2, delay_exec)

            return

    def on_click_bg_layer(self, btn, touch):
        self.close()

    def on_click_close_btn(self, btn, touch):
        self.close()

    def close(self, *args):
        super(ShareUI, self).close(*args)
        global_data.emgr.close_share_ui_event.emit()

    def on_click_friend_btn(self, cb_func):
        if self._friend_widget is None:
            from .CommonFriendListWidget import CommonFriendListWidget
            nd = global_data.uisystem.load_template_create('common/i_common_friend_list', parent=self.panel.nd_friend)
            self._friend_widget = CommonFriendListWidget(self, nd)
            self._friend_widget.set_select_friend_cb(cb_func)
            self._friend_widget.panel.nd_content.nd_search.setVisible(False)
        else:
            vis = self._friend_widget.is_visible()
            if vis:
                self._friend_widget.hide()
            else:
                self._friend_widget.show()
        return

    def set_bg_layer_frame(self, file_name):
        from logic.comsys.video.video_record_utils import cal_and_set_cover_node
        cal_and_set_cover_node(file_name, self.panel.bg_layer)

    def set_pnl_share_picture_click_enable(self, enable):
        self.panel.pnl_share_picture.setTouchEnabled(enable)
        self.panel.pnl_share_picture.setSwallowTouches(True)

    def set_save_btn_visible(self, vis):
        self.panel.pnl_btn_save.setVisible(vis)

    def clear_choose_list_func(self):
        self._choose_list_func_list = []
        self.panel.list_btn.SetInitCount(0)

    def append_choose_list_func(self, func_conf):
        self._choose_list_func_list.append(func_conf)
        self.refresh_choose_list_show(len(self._choose_list_func_list) - 1)

    def set_choose_list_fun(self, func_conf_list):
        self._choose_list_func_list = func_conf_list
        self.refresh_choose_list_show(None)
        return

    def refresh_choose_list_show(self, index):
        func_conf_list = self._choose_list_func_list
        if not func_conf_list:
            self.panel.list_btn.setVisible(False)
            return
        else:
            self.panel.list_btn.setVisible(True)
            from logic.gutils.template_utils import init_checkbox_group
            self.panel.list_btn.SetInitCount(len(func_conf_list))
            all_item = self.panel.list_btn.GetAllItem()

            def refresh_func(ui_item, func_conf):
                text = func_conf.get('text', '')
                def_val = func_conf.get('def_val', False)
                func = func_conf.get('func', None)
                ui_item.text.SetString(text)
                init_checkbox_group([ui_item], s_color='#SW', us_color='#SW')
                ui_item.choose.setVisible(def_val)

                @ui_item.unique_callback()
                def OnSelect(btn, choose_value, trigger_event, func=func):
                    if trigger_event:
                        if callable(func):
                            func(choose_value)

                return

            if index is None:
                for i in range(0, len(all_item)):
                    ui_item = all_item[i]
                    func_conf = func_conf_list[i]
                    refresh_func(ui_item, func_conf)

            else:
                ui_item = self.panel.list_btn.GetItem(index)
                if not ui_item:
                    ui_item = self.panel.list_btn.AddTemplateItem()
                func_conf = func_conf_list[index]
                refresh_func(ui_item, func_conf)
            return

    def set_share_inform_func(self, func):
        self._share_inform_func = func
        if global_data.is_pc_mode and func and callable(func):
            self._share_inform_func()

    def set_bg_color_visible(self, flag):
        self.panel.pnl_share_picture.bg_color.setVisible(flag)

    def set_custom_platform_check(self, func):
        self._custom_platform_check = func

    def set_hide_main_ui(self):
        self.hide_main_ui()