# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/ChangeHeadFrameWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon.item import item_const as iconst
from logic.gutils import role_head_utils
from logic.comsys.battle.Death.TabBaseWidget import TabBaseWidget
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.comsys.effect.ui_effect import set_gray
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_HEAD_FRAME
from logic.gutils import red_point_utils
tag_info = {0: 80451,
   1: 28000,
   2: 80914,
   3: 23014,
   4: 81083,
   5: 80684
   }

class ChangeHeadFrameWidget(TabBaseWidget):

    def __init__(self, panel, rise_panel):
        super(ChangeHeadFrameWidget, self).__init__(panel)
        self.lview = self.panel.list_frame
        self._my_uid = global_data.player.uid
        self.using_frame = 0
        self.selected_item = 0
        self.id_2_item = {}
        self.tag_list = []
        self.cur_tag_idx = 0
        self.init_head_frame_config()
        self.init_own_frames()
        self.init_tag()
        self.refresh()
        self.init_event()

    def init_head_frame_config(self):
        self.all_pic_frames = {}
        self.categories = {}
        head_frame_config = confmgr.get('head_frame_config')
        for item_id, item_conf in six.iteritems(head_frame_config):
            server_range = item_conf.get('cServer')
            if server_range and not global_data.is_inner_server and global_data.channel.get_login_host() not in server_range:
                continue
            self.all_pic_frames[item_id] = item_conf
            category = item_conf.get('iType', 0)
            if category:
                self.categories.setdefault(category, []).append(int(item_id))

    def init_own_frames(self):
        head_frame_list = global_data.player.get_view_item_list(iconst.INV_VIEW_HEAD_FRAME)
        self.own_frames = {item.get_item_no() for item in head_frame_list}
        self.categories[0] = list(self.own_frames)
        self.using_frame = global_data.player.get_head_frame()
        self.selected_item = 0

    def init_tag(self):
        tag_list = six_ex.keys(tag_info)
        tag_list.sort()
        self.tag_list = [ tag for tag in tag_list if self.categories.get(tag) ]
        self.panel.pnl_list_top_tab.SetInitCount(len(self.tag_list))
        for i, tag in enumerate(self.tag_list):
            tag_item = self.panel.pnl_list_top_tab.GetItem(i)
            tag_item.btn_tab.SetText(tag_info[tag])
            tag_item.btn_tab.BindMethod('OnClick', lambda b, t, idx=i: self.select_tag(idx))

    def init_event(self):
        using_photo = global_data.player.get_head_photo()
        role_head_utils.init_role_head(self.panel.nd_confirm.temp_head_now, self.using_frame, using_photo)
        global_data.emgr.message_on_player_role_head += self.on_change_role_head
        global_data.emgr.message_on_player_role_head_photo += self.on_change_role_head_photo

    def refresh(self):
        self.select_tag(0, True)
        self.on_click_select_item(self.using_frame)

    def on_finalize_panel(self):
        global_data.emgr.message_on_player_role_head -= self.on_change_role_head
        global_data.emgr.message_on_player_role_head_photo -= self.on_change_role_head_photo
        self.id_2_item = {}
        self.del_all_red_point()

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

        container_count = self.lview.GetItemCount()
        self.id_2_item = {}
        i = 0
        item_list = self.categories.get(tag, [])
        new_frames = global_data.lobby_red_point_data.get_item_list_by_type(L_ITEM_TYPE_HEAD_FRAME) if tag == 0 else ()
        for item_id in item_list:
            info = self.all_pic_frames.get(str(item_id)) or {}
            if info.get('iShowOwn') and item_id not in self.own_frames:
                continue
            res_path = item_utils.get_lobby_item_pic_by_item_no(item_id, -1)
            if res_path == -1:
                continue
            if i < container_count:
                item = self.lview.GetItem(i) if 1 else self.lview.AddTemplateItem(bRefresh=False)
                i += 1
                self.id_2_item[item_id] = item
                item.img_head.SetDisplayFrameByPath('', res_path)
                item.img_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/item/ui_item/bar%d.png' % info.get('iClip', 30110621))
                item.img_bar.setScale(0.5)
                item.nd_using.setVisible(item_id == self.using_frame)
                item.img_choose.setVisible(item_id == self.selected_item)
                self.set_item_status(item_id, item)
                red_point_utils.show_red_point_template(item.nd_red, item_id in new_frames)
                item.nd_choose.BindMethod('OnClick', lambda b, t, id=item_id: self.on_click_select_item(id))

        while i < container_count:
            container_count -= 1
            self.lview.DeleteItemIndex(container_count, False)

        self.lview.GetContainer()._refreshItemPos()
        self.lview._refreshItemPos()

    def set_item_status(self, item_id, item_nd):
        not_own = item_id not in self.own_frames
        set_gray(item_nd.img_head, not_own)
        set_gray(item_nd.img_bar, not_own)
        item_nd.img_bar.setOpacity(192 if not_own else 255)

    def on_change_role_head(self, update_list):
        if self._my_uid not in update_list:
            return
        item_id = update_list[self._my_uid]
        last_item = self.id_2_item.get(self.using_frame)
        if last_item:
            last_item.nd_using.setVisible(False)
        self.using_frame = item_id
        item = self.id_2_item.get(item_id)
        if item:
            item.nd_using.setVisible(True)
        self.update_equip_btn_state()

    def on_change_role_head_photo(self, update_list):
        if self._my_uid not in update_list:
            return
        item_no = update_list[self._my_uid]
        role_head_utils.set_role_head_photo(self.panel.nd_confirm.temp_head_now, item_no)

    def on_click_select_item(self, item_id):
        if self.selected_item == item_id:
            return
        last_item = self.id_2_item.get(self.selected_item)
        if last_item:
            last_item.img_choose.setVisible(False)
        self.selected_item = item_id
        item = self.id_2_item.get(item_id)
        if not item:
            return
        item.img_choose.setVisible(True)
        role_head_utils.set_role_head_frame(self.panel.nd_confirm.temp_head_now, item_id)
        self.panel.nd_confirm.lab_frame_name.SetString(item_utils.get_lobby_item_name(item_id))
        desc = item_utils.get_lobby_item_desc(item_id)
        if desc:
            self.panel.nd_confirm.lab_frame_desc.setVisible(True)
            self.panel.nd_confirm.lab_frame_desc.SetString(desc)
        else:
            self.panel.nd_confirm.lab_frame_desc.setVisible(False)
        self.update_equip_btn_state()
        if global_data.player:
            red_point_utils.show_red_point_template(item.nd_red, False)
            global_data.player.req_del_item_redpoint(item_id)

    def select_item_by_item_no(self, item_no):
        item_type = confmgr.get('head_frame_config', str(item_no), 'iType')
        if item_type in self.tag_list:
            tab_idx = self.tag_list.index(item_type)
            self.select_tag(tab_idx)
        self.on_click_select_item(item_no)

    def update_equip_btn_state(self):
        item_id = self.selected_item
        btn = self.panel.nd_confirm.btn_change
        btn.setVisible(True)
        self.panel.nd_confirm.nd_lock.setVisible(False)
        btn.btn_common.SetEnable(False)
        if item_id == self.using_frame:
            btn.btn_common.SetText(2219)
        elif item_id in self.own_frames:
            btn.btn_common.SetText(2220)
            btn.btn_common.SetEnable(True)
            btn.btn_common.BindMethod('OnClick', lambda b, t, id=item_id: global_data.player.dress_head_frame(id, True))
        else:
            btn.btn_common.SetText(2220)
        can_jump = item_utils.can_jump_to_ui(item_id)
        jump_txt = item_utils.get_item_access(item_id)
        self.panel.btn_go.lab_go.SetString(jump_txt or '')
        self.panel.btn_go.setVisible(can_jump)
        self.panel.btn_go.BindMethod('OnClick', lambda b, t, id=item_id: item_utils.jump_to_ui(id))

    def del_all_red_point(self):
        if not global_data.player or not self.really_shown:
            return
        for item_id in self.own_frames:
            global_data.player.req_del_item_redpoint(item_id)