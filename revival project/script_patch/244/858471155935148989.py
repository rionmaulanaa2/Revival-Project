# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/housesys/MainHouseUI.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
import time
import common.const.uiconst
from cocosui import cc, ccui, ccs
from common.const.property_const import *
from common.cfg import confmgr
import logic.comsys.message.message_data as message_data
from common.uisys.uielment.CCRichText import CCRichText
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.team_const import TEAM_SUMMON_VALID_TIME
import render
from logic.gcommon.item import item_const as iconst
from logic.gutils.item_utils import jump_to_ui, get_item_access, can_jump_to_ui
import game3d
from logic.gutils.share_utils import get_pc_share_save_fold
from common.const import uiconst
from logic.manager_agents.manager_decorators import sync_exec
from common.utils.timer import CLOCK
import device_compatibility

class MainHouseUI(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'poster/poster_main'
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_close',
       'btn_display.btn_common.OnClick': 'on_display',
       'btn_unlock.btn_common.OnClick': 'on_unlock',
       'btn_using.btn_common.OnClick': 'on_using',
       'btn_save.btn_common.OnClick': 'on_save'
       }

    def on_init_panel(self, *args, **kargs):
        self.sync_timer = None
        self._gaussian_blur = True
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        wall_picture = global_data.player.get_view_item_list(iconst.INV_VIEW_HOUSE_WALL_PICTURE)
        self._wall_picture_ids = set([ item.get_item_no() for item in wall_picture ])
        self._cur_wall_picture = global_data.player.get_wall_picture()
        self._choose_panle = None
        self._choose_wall_picture_id = None
        self._photo_scale_x = self.panel.img_poster.getScaleX()
        self._photo_scale_y = self.panel.img_poster.getScaleY()
        self._rt = None
        self.img_panel = None
        self.img_panel_scale_x = 1.0
        self.img_panel_scale_y = 1.0
        self._is_saving = False
        self.init_photolist()
        if self._cur_wall_picture is not None:
            self.refresh_main_photo(self._cur_wall_picture)
        self.hide_main_ui()
        self.panel.btn_share.setVisible(False)
        self.init_event()
        return

    def init_event(self):
        global_data.emgr.housesys_wall_picture_change_success += self.on_picture_change
        global_data.emgr.on_lobby_bag_item_changed_event += self._refresh_all_photolist
        global_data.emgr.check_apply_postprocess += self._refresh_gaussian_blur

    def init_photolist(self):
        all_data = confmgr.get('house_photo')
        self._choose_panle = None

        def cmp_func(a, b):
            a_weight = 0
            b_weight = 0
            if int(a) in self._wall_picture_ids:
                a_weight = 1
            if int(b) in self._wall_picture_ids:
                b_weight = 1
            if a_weight > b_weight:
                return 1
            else:
                return -1

        all_keys = six_ex.keys(all_data)
        all_keys.remove('__doc__')
        sort_data_list = sorted(all_keys, key=cmp_to_key(cmp_func), reverse=True)
        data_count = len(sort_data_list)
        list_node = self.panel.temp_left_tab.tab_list
        count = list_node.GetItemCount()
        if count >= data_count:
            list_node.SetInitCount(count)
        cur_pic_index = sort_data_list.index(str(self._cur_wall_picture))
        self.init_touch = True

        def _init_item(item_id, all_data, panel):
            photo_data = all_data[item_id]
            show_flag = False
            if self._choose_wall_picture_id is None:
                if self.init_touch and (self._cur_wall_picture == int(item_id) or not self._cur_wall_picture):
                    self.init_touch = False
                    show_flag = True
            elif self.init_touch and self._choose_wall_picture_id == int(item_id):
                self.init_touch = False
                show_flag = True
            self.add_photo(panel, photo_data, show_flag)
            return

        for index, panel in enumerate(list_node.GetAllItem()):
            item_id = sort_data_list[index]
            _init_item(item_id, all_data, panel)

        self.clear_timer()
        self._sync_index = count
        add_count = data_count - count
        if add_count > 0:

            def _sync_add():
                if not (self.panel and self.panel.isValid()):
                    self.clear_timer()
                    return
                item_id = sort_data_list[self._sync_index]
                panel = list_node.AddTemplateItem()
                _init_item(item_id, all_data, panel)
                self._sync_index += 1

            self.sync_timer = global_data.game_mgr.get_logic_timer().register(func=_sync_add, mode=CLOCK, interval=0.01, times=add_count)
        return

    def clear_timer(self):
        if self.sync_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.sync_timer)
        self.sync_timer = None
        return

    def add_photo(self, panel, photo_data, show_flag):
        scale_x = panel.img_poster.getScaleX()
        scale_y = panel.img_poster.getScaleY()
        panel.lab_name.setString(get_text_by_id(photo_data['cName']))

        def cb():
            if panel and panel.isValid():
                size = panel.img_poster.getContentSize()
                panel.img_poster.setScale(1024 / size.width * scale_x, 1024 / size.height * scale_y)

        panel.img_poster.SetDisplayFrameByPath('', photo_data['cRes'], callback=cb)
        if photo_data['iId'] in self._wall_picture_ids:
            panel.img_shield.setVisible(False)
        else:
            panel.img_shield.setVisible(True)

        @panel.btn_choose.callback()
        def OnClick(*args):
            if self._choose_panle:
                self._choose_panle.img_choose.setVisible(False)
            self._choose_panle = panel
            self._choose_panle.img_choose.setVisible(True)
            self._choose_wall_picture_id = photo_data['iId']
            self.refresh_main_photo(photo_data['iId'])

        if show_flag:
            OnClick()

    def refresh_main_photo(self, photo_id):
        photo_data = confmgr.get('house_photo', str(photo_id))
        self.panel.img_poster.SetDisplayFrameByPath('', photo_data['cRes'])
        size = self.panel.img_poster.getContentSize()
        self.panel.img_poster.setScale(1024 / size.width * self._photo_scale_x, 1024 / size.height * self._photo_scale_y)
        self.panel.lab_details.SetString(get_text_by_id(photo_data['cDes']))
        detail_size = self.panel.lab_details.getTextContentSize()
        self.panel.btn_display.setVisible(False)
        self.panel.btn_unlock.setVisible(False)
        self.panel.btn_using.setVisible(False)
        self.panel.btn_using.btn_common.SetShowEnable(False)
        if photo_data['iId'] in self._wall_picture_ids:
            self.panel.img_shield.setVisible(False)
            if photo_data['iId'] == self._cur_wall_picture:
                self.panel.btn_using.setVisible(True)
            else:
                self.panel.btn_display.setVisible(True)
            self.panel.btn_save.setVisible(True)
        else:
            self.panel.img_shield.setVisible(True)
            if can_jump_to_ui(photo_id):
                self.panel.btn_unlock.setVisible(True)
            access_text = get_item_access(photo_id)
            if access_text:
                self.panel.img_shield.lab_unlock.setVisible(True)
                self.panel.img_shield.lab_unlock.setString(access_text)
            else:
                self.panel.img_shield.lab_unlock.setVisible(False)
            self.panel.btn_save.setVisible(False)

    def on_picture_change(self):
        self._cur_wall_picture = global_data.player.get_wall_picture()
        if self._choose_wall_picture_id is not None:
            self.refresh_main_photo(self._choose_wall_picture_id)
        return

    def on_close(self, *args):
        self.close()

    def on_display(self, *args):
        if self._choose_wall_picture_id is not None:
            global_data.player.select_wall_picture(self._choose_wall_picture_id)
        return

    def on_unlock(self, *args):
        jump_to_ui(self._choose_wall_picture_id)

    def on_using(self, *args):
        pass

    def on_save(self, *args):
        self.save_pic_gallery()

    def do_hide_panel(self):
        super(MainHouseUI, self).do_hide_panel()
        self._gaussian_blur = False
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def do_show_panel(self):
        super(MainHouseUI, self).do_show_panel()
        self._gaussian_blur = True

    def _refresh_gaussian_blur(self):
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', self._gaussian_blur)

    def on_finalize_panel(self):
        self.clear_timer()
        global_data.emgr.housesys_wall_picture_change_success -= self.on_picture_change
        global_data.emgr.on_lobby_bag_item_changed_event -= self._refresh_all_photolist
        global_data.emgr.check_apply_postprocess -= self._refresh_gaussian_blur
        self._gaussian_blur = False
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()
        if self._rt:
            self._rt.release()
        if self.img_panel:
            self.img_panel.release()

    @sync_exec
    def save_pic_gallery(self):
        if self._is_saving:
            return
        else:
            self._is_saving = True
            if not self._rt:
                from common.const import uiconst
                if game3d.get_render_device() == game3d.DEVICE_METAL:
                    self._rt = cc.RenderTexture.create(1024, 576, cc.TEXTURE2D_PIXELFORMAT_RGBA8888, uiconst.DEPTH24_STENCIL8_OES, True)
                else:
                    self._rt = cc.RenderTexture.create(1024, 576, cc.TEXTURE2D_PIXELFORMAT_RGBA8888, uiconst.DEPTH24_STENCIL8_OES)
                self._rt.retain()
                self.img_panel = global_data.uisystem.load_template_create('poster/save_img', None)
                if device_compatibility.IS_DX or game3d.get_render_device() == game3d.DEVICE_METAL:
                    self.img_panel.setFlippedY(True)
                self.img_panel.retain()
                self.img_panel_scale_x = self.img_panel.getScaleX()
                self.img_panel_scale_y = self.img_panel.getScaleY()
            photo_data = confmgr.get('house_photo', str(self._choose_wall_picture_id))
            self.img_panel.SetDisplayFrameByPath('', photo_data['cRes'])
            size = self.img_panel.getContentSize()
            self.img_panel.setScale(1024.0 / size.width, 576.0 / size.height)
            self._rt.begin()
            if hasattr(self._rt, 'addCommandsForNode'):
                self._rt.addCommandsForNode(self.img_panel.get())
            else:
                self.img_panel.visit()
            self._rt.end()
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                path = get_pc_share_save_fold() + '/%s.%s' % (str(self._choose_wall_picture_id), 'png')
            else:
                path = game3d.get_doc_dir() + '/%s.%s' % (str(self._choose_wall_picture_id), 'png')

            def save_to_file_callback(rt, filename):

                def save_to_gallery_callback():
                    self._is_saving = False

                global_data.game_mgr.post_exec(lambda : global_data.share_mgr.save_to_gallery(path, save_to_gallery_callback))

            self._rt.saveToFile(path, cc.IMAGE_FORMAT_PNG, False, save_to_file_callback)
            return

    def _refresh_all_photolist(self):
        wall_picture = global_data.player.get_view_item_list(iconst.INV_VIEW_HOUSE_WALL_PICTURE)
        wall_picture_ids = set([ item.get_item_no() for item in wall_picture ])
        if wall_picture_ids != self._wall_picture_ids:
            self._wall_picture_ids = wall_picture_ids
            self.init_photolist()