# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ScreenFrameHelper.py
from __future__ import absolute_import
import game3d

class ScreenFrameHelper(object):

    def __init__(self):
        self._share_content = None
        self._is_custom_share_content = False
        self._hidden_names = []
        self._share_ui = None
        self._share_custom_btns = None
        self._share_custom_btn_is_head = False
        return

    def destroy(self):
        if not self._is_custom_share_content:
            if self._share_content:
                self._share_content.destroy()
                self._share_content = None
        self._hidden_names = []
        return

    def get_share_content(self):
        return self._share_content

    def set_custom_share_button(self, btn_infos, is_head):
        self._share_custom_btn_is_head = is_head
        self._share_custom_btns = btn_infos

    def set_custom_share_content(self, share_content):
        self._is_custom_share_content = True
        self._share_content = share_content

    def take_screen_shot(self, ui_list, panel, add_watermark=True, custom_cb=None, head_nd_name='', need_share_ui=True, share_inform_func=None, **kwargs):
        if self._is_custom_share_content:
            pass
        elif not self._share_content:
            from logic.comsys.share.PersonRoleInfoShareCreator import PersonRoleInfoShareCreator
            share_creator = PersonRoleInfoShareCreator()
            share_creator.create()
            self._share_content = share_creator

        def cb():
            if not (panel and panel.isValid()):
                return
            self.take_screen_shot_helper(ui_list, panel, add_watermark, custom_cb, head_nd_name, need_share_ui, share_inform_func, **kwargs)

        has_fastforward_ani = False
        if panel and kwargs.get('FastForwardAnim', True):
            ani_names = panel.GetAnimationNameList()
            for ani_name in ani_names:
                if panel.IsPlayingAnimation(ani_name) and panel.GetAnimationPlayTimes(ani_name) < 3:
                    panel.FastForwardToAnimationTime(ani_name, panel.GetAnimationMaxRunTime(ani_name))
                    has_fastforward_ani = True

        if kwargs.get('ToEndAnim', True):
            from logic.gutils import lobby_model_display_utils
            if lobby_model_display_utils.is_chuchang_scene():
                global_data.emgr.try_end_chuchang_scene_directly.emit()
                if kwargs.get('HidePanelAfterEndChuChang', False):
                    if panel and panel.isValid():
                        panel.setVisible(False)
                global_data.game_mgr.delay_exec(0.4, cb)
            else:
                global_data.emgr.to_model_display_end_anim_directly.emit(None, is_back_to_end_show_anim=True)
                global_data.game_mgr.delay_exec(0.05, cb)
        else:
            has_fastforward_ani or cb() if 1 else global_data.game_mgr.delay_exec(0.05, cb)
        return

    def take_screen_shot_helper(self, ui_list, panel, add_watermark=True, custom_cb=None, head_nd_name='', need_share_ui=True, share_inform_func=None, **kwargs):
        from logic.comsys.share.PersonRoleInfoShareCreator import PersonRoleInfoShareCreator
        if self._is_custom_share_content:
            pass
        else:
            if not self._share_content:
                share_creator = PersonRoleInfoShareCreator()
                share_creator.create()
                self._share_content = share_creator
            if self._share_content:
                self._share_content.set_watermark(add_watermark)
                if head_nd_name:
                    self._share_content.base_init_head(head_nd_name)
                white_lab = kwargs.get('white_lab', False)
                if white_lab:
                    self._share_content.set_white_lab_color_and_outline()
                item_detail_no = kwargs.get('item_detail_no', None)
                if item_detail_no:
                    is_get = kwargs.get('item_detail_no_is_get', True)
                    self._share_content.show_share_detail(item_detail_no, is_get)
                self._share_content.set_show_record(False)
        if not panel or not self._share_content or not self._share_content.panel:
            return
        else:

            def callback():
                if not panel or not self._share_content or not self._share_content.panel:
                    return
                else:
                    self._share_content.update_ui_bg_sprite()
                    need_draw_rt = kwargs.get('need_draw_rt', True)
                    if need_draw_rt:
                        rt = self._share_content.get_render_texture()
                    else:
                        rt = None
                    if need_share_ui:
                        from logic.comsys.share.ShareUI import ShareUI
                        share_ui = ShareUI()
                        self._share_ui = share_ui
                        if share_inform_func:
                            share_ui.set_share_inform_func(share_inform_func)
                        share_ui.add_custom_button(self._share_custom_btns, self._share_custom_btn_is_head)
                        share_ui.set_share_content_raw(rt, share_content=self._share_content)
                    if custom_cb:
                        custom_cb(rt)
                    return

            if not global_data.try_screen_capture_share:
                from logic.comsys.common_ui.SceneSnapShotUI import ScreenSnapShotUI
                from logic.gutils.share_utils import get_share_size
                sz = get_share_size()
                ui_inst = ScreenSnapShotUI(None, sz.width, sz.height)
                ui_inst.take_screen_snapshot(self._share_content.get_ui_bg_sprite(), callback, ui_list)
                ui_inst.close()
            else:

                def cb1(file_path, encrypted_file_path, related_path):
                    if not ui_list:
                        global_data.ui_mgr.set_all_ui_visible(True)
                    else:
                        global_data.ui_mgr.revert_hide_all_ui_by_key_action(self.__class__.__name__, self._hidden_names)
                        self._hidden_ui_names = []
                    if not self._share_content:
                        return
                    import shutil
                    try:
                        shutil.copyfile(file_path, encrypted_file_path)
                    except:
                        log_error('copyfile Fail! ', file_path, encrypted_file_path)
                        global_data.game_mgr.show_tip(get_text_by_id(90056))

                    import cc
                    cc.Director.getInstance().getTextureCache().reloadTexture(related_path)
                    sprite = self._share_content.get_ui_bg_sprite()
                    if not sprite:
                        return
                    sprite.SetDisplayFrameByPath('', related_path)
                    callback()

                if not ui_list:
                    global_data.ui_mgr.set_all_ui_visible(False)
                else:
                    self._hidden_names = global_data.ui_mgr.hide_all_ui_by_key(self.__class__.__name__, [], ui_list + ('BattleMatchUI',
                                                                                                                       'HangUpUI'))
                from logic.comsys.share.ShareManager import ShareManager
                ShareManager().capture_screen_to_share(cb1, False)
            return

    def take_screen_shot_without_share(self, custom_cb=None):
        from logic.comsys.share.ShareManager import ShareManager
        ShareManager().capture_screen_to_share(custom_cb)

    def modify_share_content_by_func(self, func):
        if callable(func):
            func(self._share_content)

    def get_share_ui(self):
        return self._share_ui