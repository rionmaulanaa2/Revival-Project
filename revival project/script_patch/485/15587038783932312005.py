# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/FileWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils import bond_utils

class FileWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'bond_update_role_level': self.on_bond_udpate,
           'bond_update_role_level': self.refresh_redpoint,
           'bond_diary_changed': self.refresh_redpoint,
           'refresh_item_red_point': self.refresh_redpoint
           }
        super(FileWidget, self).__init__(parent, panel)
        self.role_id = 0
        self._ui_role_id = 0
        self._hide_info_tag_indexes = []
        img_path = [
         'weight', 'birthday', 'gen', 'id', 'own_mech', 'cv']
        lab_info = list(confmgr.get('role_info', 'TagConfig', 'Content', 'file_data', 'text_id'))
        douyin_remove_tag = 'cv'
        if global_data.channel.get_name() in ('toutiao_sdk', ):
            if douyin_remove_tag in img_path:
                self._hide_info_tag_indexes.append(img_path.index(douyin_remove_tag))
        show_file_data = [ _fd for index, _fd in enumerate(lab_info) if index not in self._hide_info_tag_indexes ]
        self.panel.list_info.SetInitCount(len(show_file_data))
        for i, info_item in enumerate(self.panel.list_info.GetAllItem()):
            if i in self._hide_info_tag_indexes:
                continue
            info_item.lab_info.SetString(get_text_by_id(show_file_data[i]))
            info_item.img_tag.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_%s.png' % img_path[i])

        @self.panel.btn_check.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('DairyLog', 'logic.comsys.role_profile')
            if ui:
                ui.set_role_id(self.role_id)

        self._shown_role_id_set = set()

    def show_panel(self, flag):
        self.panel.setVisible(flag)

    def on_hide(self):
        pass

    def destroy(self):
        super(FileWidget, self).destroy()
        self.clear_all_redpoint()

    def set_role_id(self, role_id):
        self.role_id = role_id

    def refresh_all_content(self):
        if self._ui_role_id == self.role_id:
            return
        self._ui_role_id = self.role_id
        self._shown_role_id_set.add(self.role_id)
        role_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(self.role_id))
        file_data = role_info['file_data']
        show_file_data = [ _fd for index, _fd in enumerate(file_data) if index not in self._hide_info_tag_indexes ]
        for i, info_item in enumerate(self.panel.list_info.GetAllItem()):
            if i in self._hide_info_tag_indexes:
                continue
            if i >= len(show_file_data):
                info_item.setVisible(False)
                continue
            info_item.setVisible(True)
            info_item.lab_value.SetString(get_text_by_id(show_file_data[i]))

        role_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(self.role_id))
        if not role_info.get('log'):
            self.panel.temp_story.setVisible(False)
        else:
            self.panel.temp_story.setVisible(True)
        self.panel.img_role.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_role%d.png' % role_info['mecha_id'])
        self.panel.lab_declaration.SetString(role_info['declaration'])
        self.panel.img_role.SetDisplayFrameByPath('', 'gui/ui_res_2/item/driver/%d.png' % self.role_id)
        self.refresh_redpoint()

    def on_bond_udpate(self, role_id, event_info):
        if self.role_id == role_id:
            self.refresh_redpoint()

    def refresh_redpoint(self, *args):
        role_profile_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(self.role_id))
        if not bond_utils.is_open_bond_sys():
            return
        count = bond_utils.get_unread_bond_diary(self.role_id)
        from logic.gutils import red_point_utils
        red_point_utils.show_red_point_template(self.panel.img_red, count > 0)

    def on_dress_change(self, new_skin_id):
        pass

    def clear_all_redpoint(self):
        for role_id in self._shown_role_id_set:
            log_list = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id), 'log', default=[])
            for log_id in log_list:
                bond_utils.set_bond_diary_readed(log_id)

        self._shown_role_id_set = set