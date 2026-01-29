# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/ChangeRolePhotoWidget.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item import item_const as iconst
from logic.gutils import role_head_utils
from logic.comsys.battle.Death.TabBaseWidget import TabBaseWidget
from common.cfg import confmgr
import cc
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_HEAD_PHOTO
from logic.gutils import item_utils
from logic.gutils import red_point_utils
tag_info = {0: 80451,
   1: 80684,
   2: 28000,
   3: 80914
   }

class ChangeRolePhotoWidget(TabBaseWidget):

    def __init__(self, panel, rise_panel):
        super(ChangeRolePhotoWidget, self).__init__(panel)
        self.lview = self.panel.list_profile_photo
        self._my_uid = global_data.player.uid
        self.using_photo = 0
        self.selected_item = 0
        self.id_2_item = {}
        self.tag_list = []
        self.cur_tag_idx = 0
        self.load_config()
        self.init_own_photos()
        self.init_tag()
        self.refresh()
        self.init_event(True)

    def load_config(self):
        self._all_photos = set()
        self.categories = {}
        head_frame_config = confmgr.get('head_photo_config')
        for item_id, item_conf in six.iteritems(head_frame_config):
            category = item_conf.get('iType', 0)
            if not category:
                continue
            server_range = item_conf.get('cServer')
            if server_range:
                if not global_data.is_inner_server and global_data.channel.get_login_host() not in server_range:
                    continue
            self.categories.setdefault(category, []).append(int(item_id))
            self._all_photos.add(int(item_id))

    def init_own_photos(self):
        head_frame_list = global_data.player.get_view_item_list(iconst.INV_VIEW_HEAD_PHOTO)
        self.own_photos = {item.get_item_no() for item in head_frame_list if item.get_item_no() in self._all_photos}
        self.categories[0] = list(self.own_photos)
        self.categories[0].sort()
        self.using_photo = self.check_using_photo(global_data.player.get_head_photo())
        self.selected_item = 0

    def init_event(self, bind):
        econf = {'message_on_player_role_head_photo': self.on_change_role_head_photo,
           'add_item_red_point': self.unlock_photo
           }
        global_data.emgr.bind_events(econf) if bind else global_data.emgr.unbind_events(econf)

    def refresh(self):
        using_frame = global_data.player.get_head_frame()
        role_head_utils.set_role_head_frame(self.panel.nd_photo_confirm.temp_head_now_photo, using_frame)
        self.select_tag(0, True)
        self.on_click_photo(self.using_photo)

    def on_finalize_panel(self):
        self.init_event(False)
        self.id_2_item = {}
        self.del_all_red_point()

    def init_tag(self):
        tag_list = six_ex.keys(tag_info)
        tag_list.sort()
        self.tag_list = [ tag for tag in tag_list if self.categories.get(tag) ]
        self.panel.pnl_list_top_tab.SetInitCount(len(self.tag_list))
        for i, tag in enumerate(self.tag_list):
            tag_item = self.panel.pnl_list_top_tab.GetItem(i)
            tag_item.btn_tab.SetText(tag_info[tag])
            tag_item.btn_tab.BindMethod('OnClick', lambda b, t, idx=i: self.select_tag(idx))

    def select_tag(self, tag_idx, force_change=False):
        if tag_idx == self.cur_tag_idx and not force_change:
            return
        self.cur_tag_idx = tag_idx
        tag = self.tag_list[tag_idx]
        for i, tag_item in enumerate(self.panel.pnl_list_top_tab.GetAllItem()):
            if i == tag_idx:
                tag_item.btn_tab.SetSelect(True)
                tag_item.img_vx.setVisible(True)
                tag_item.PlayAnimation('click')
            else:
                tag_item.btn_tab.SetSelect(False)
                tag_item.PlayAnimation('unclick')
                tag_item.img_vx.setVisible(False)

        item_list = list(self.categories[tag] if tag > 0 else self.own_photos)
        real_item_list = []
        for item_id in item_list:
            if confmgr.get('head_photo_config', str(item_id), 'iShowOwn', default=0) and item_id not in self.own_photos:
                continue
            real_item_list.append(item_id)

        real_item_list.sort()
        new_photos = global_data.lobby_red_point_data.get_item_list_by_type(L_ITEM_TYPE_HEAD_PHOTO) if tag == 0 else ()
        self.lview.SetInitCount(len(real_item_list))
        self.id_2_item = {}
        for i, item_id in enumerate(real_item_list):
            item = self.lview.GetItem(i)
            self.id_2_item[item_id] = item
            res_path = item_utils.get_lobby_item_pic_by_item_no(item_id)
            item.img_role.SetDisplayFrameByPath('', res_path)
            item.nd_lock.setVisible(item_id not in self.own_photos)
            red_point_utils.show_red_point_template(item.nd_red, item_id in new_photos)
            item.nd_using.setVisible(False)
            item.img_choose.setVisible(False)
            item.nd_choose.BindMethod('OnClick', lambda b, t, item_no=item_id: self.on_click_photo(item_no))

        item = self.id_2_item.get(self.using_photo)
        item and item.nd_using.setVisible(True)
        item = self.id_2_item.get(self.selected_item)
        item and item.img_choose.setVisible(True)

    def on_change_role_head_photo(self, update_list):
        if self._my_uid not in update_list:
            return
        else:
            if not self.lview:
                return
            item_no = update_list[self._my_uid]
            if self.using_photo is not None:
                old_item = self.id_2_item.get(self.using_photo)
                if old_item:
                    old_item.nd_using.setVisible(False)
            self.using_photo = self.check_using_photo(item_no)
            new_item = self.id_2_item.get(self.using_photo)
            if new_item:
                new_item.nd_using.setVisible(True)
            self.set_equip_btn_state()
            return

    def on_click_photo(self, item_no, force=False):
        if self.selected_item == item_no and not force:
            return
        old_item = self.id_2_item.get(self.selected_item)
        if old_item:
            old_item.img_choose.setVisible(False)
        self.selected_item = item_no
        item = self.id_2_item.get(item_no)
        if item:
            item.img_choose.setVisible(True)
            if global_data.player:
                red_point_utils.show_red_point_template(item.nd_red, False)
                global_data.player.req_del_item_redpoint(item_no)
        role_head_utils.set_role_head_photo(self.panel.nd_photo_confirm.temp_head_now_photo, item_no)
        name_desc, photo_desc, unlock_desc = role_head_utils.get_head_photo_desc(item_no)
        self.panel.nd_photo_confirm.lab_photo_name.setVisible(True if name_desc else False)
        self.panel.nd_photo_confirm.photo_name_bg.setVisible(True if name_desc else False)
        self.panel.nd_photo_confirm.lab_photo_desc.setVisible(True if photo_desc else False)
        self.panel.nd_photo_confirm.btn_go.setVisible(True if unlock_desc else False)
        if name_desc:
            self.panel.nd_photo_confirm.lab_photo_name.SetString(name_desc)
        if photo_desc:
            self.panel.nd_photo_confirm.lab_photo_desc.SetString(photo_desc)
        if unlock_desc:
            self.panel.nd_photo_confirm.btn_go.lab_go.SetString(unlock_desc)

            @self.panel.nd_photo_confirm.btn_go.callback()
            def OnClick(btn, touch, go_item_no=item_no):
                item_utils.jump_to_ui(go_item_no)

        self.set_equip_btn_state()

    def set_equip_btn_state(self):
        item_no = self.selected_item
        btn = self.panel.nd_photo_confirm.btn_change_photo
        btn.setVisible(True)
        self.panel.nd_photo_confirm.nd_lock.setVisible(False)
        if item_no == self.using_photo:
            btn.btn_common.SetText(2219)
            btn.btn_common.SetEnable(False)
        elif item_no in self.own_photos:
            btn.btn_common.SetText(2220)
            btn.btn_common.SetEnable(True)

            @btn.btn_common.callback()
            def OnClick(btn, touch, item_no=item_no):
                global_data.player.update_head_photo(item_no, True)

        else:
            btn.btn_common.SetText(2220)
            btn.btn_common.SetEnable(False)

    def unlock_photo(self, item_no):
        item = self.id_2_item.get(item_no)
        if not item:
            return
        item.nd_lock.setVisible(False)
        red_point_utils.show_red_point_template(item.nd_red, True)
        if item_no == self.selected_item:
            global_data.game_mgr.post_exec(self.on_click_photo, item_no, True)

    def check_using_photo(self, item_no):
        if item_no not in self._all_photos:
            return iconst.DEFAULT_HEAD_PHOTO
        return item_no

    def del_all_red_point(self):
        if not global_data.player or not self.really_shown:
            return
        for item_id in self.own_photos:
            global_data.player.req_del_item_redpoint(item_id)

    def select_item_by_item_no(self, item_no):
        self.on_click_photo(item_no)