# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/DairyLog.py
from __future__ import absolute_import
import common.const.uiconst
import common.utilities
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils import bond_utils, role_utils
from logic.gutils import red_point_utils
UNLOCK_TYPE_NONE = 0
UNLOCK_TYPE_BOND_LEVEL = 1

class DairyLog(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role_profile/profile_story_new_2'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_window_small'
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'bond_update_role_level': 'on_bond_udpate',
       'bond_diary_changed': 'refresh_list_redpoint'
       }

    def on_init_panel(self, *args, **kargs):
        super(DairyLog, self).on_init_panel()
        self.log_info = confmgr.get('role_info', 'Story', 'Content')
        self.role_info = None
        self.selected_index = -1
        self.role_id = 0
        return

    def on_finalize_panel(self):
        pass

    def get_role_list(self):
        if not self.role_info:
            return []
        log_list = self.role_info.get('log', [])
        if log_list and not role_utils.is_role_publish(self.role_id):
            log_list = log_list[:1]
        return log_list

    def set_role_id(self, role_id):
        self.role_id = role_id
        self.role_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id))
        name_title = get_text_by_id(80986).format(get_text_by_id(self.role_info['role_name']))
        self.panel.temp_window_small.lab_title.SetString(name_title)
        log_list = self.get_role_list()
        self.panel.tab_list.DeleteAllSubItem()
        for index, log_id in enumerate(log_list):
            item = self.panel.tab_list.AddTemplateItem()
            title_id = self.log_info.get(str(log_id), {}).get('title_id', 65117)
            item.btn.SetText(get_text_by_id(title_id))

            @item.btn.callback()
            def OnClick(b, t, idx=index):
                self.refresh_log(idx)

            if index > 0 and not bond_utils.is_open_bond_sys():
                item.setVisible(False)

        self.refresh_unlock_state()
        self.refresh_list_redpoint()
        self.refresh_log(0)

    def refresh_unlock_state(self, *args):
        log_list = self.get_role_list()
        for index, log_id in enumerate(log_list):
            item = self.panel.tab_list.GetItem(index)
            is_unlocked = self.is_unlocked(log_id)
            item.nd_lock.setVisible(not is_unlocked)

    def refresh_list_redpoint(self, *args):
        if not bond_utils.is_open_bond_sys():
            return
        if not self.role_info:
            return
        cur_bond_level, _ = global_data.player.get_bond_data(self.role_id)
        log_list = self.get_role_list()
        count = self.panel.tab_list.GetItemCount()
        for index, log_id in enumerate(log_list):
            if index >= count:
                continue
            item = self.panel.tab_list.GetItem(index)
            red_point_utils.show_red_point_template(item.img_red, not bond_utils.is_readed_bond_diary(self.role_id, log_id))

    def on_bond_udpate(self, role_id, event_info):
        if self.role_id != role_id:
            return
        self.refresh_unlock_state()
        self.refresh_list_redpoint()

    def refresh_log(self, index):
        if self.selected_index == index:
            return
        if self.selected_index >= 0:
            pre_item = self.panel.tab_list.GetItem(self.selected_index)
            if pre_item:
                pre_item.btn.SetSelect(False)
                pre_item.btn.SetColor('#DD')
                pre_item.img_white.setVisible(False)
                pre_item.img_black.setVisible(True)
        self.selected_index = index
        cur_item = self.panel.tab_list.GetItem(self.selected_index)
        if cur_item:
            cur_item.btn.SetSelect(True)
            cur_item.btn.SetColor('#SW')
            cur_item.img_white.setVisible(True)
            cur_item.img_black.setVisible(False)
        for i, item in enumerate(self.panel.tab_list.GetAllItem()):
            item.img_choose.setVisible(i == index)

        log_id = self.role_info.get('log', [])[index]
        is_unlocked = self.is_unlocked(log_id)
        self.show_log(log_id, is_unlocked)
        self.show_locked_log(log_id, is_unlocked)

    def show_log(self, log_id, is_unlocked=None):
        if is_unlocked is None:
            is_unlocked = self.is_unlocked(log_id)
        if not is_unlocked:
            self.panel.nd_unlock.setVisible(False)
            return
        else:
            self.panel.nd_unlock.setVisible(True)
            bond_utils.set_bond_diary_readed(log_id)
            log_data = self.log_info.get(str(log_id), {})
            roll_container = self.panel.nd_content
            log_item = roll_container.GetItem(0)
            content = log_data.get('content_id', 65114)
            if isinstance(content, int):
                log_item.lab_content.SetString(log_data.get('content_id', 65114))
            else:
                content = '\n'.join([ get_text_by_id(text_id) for text_id in content ])
                log_item.lab_content.SetString(content)
            log_item.lab_content.formatText()
            text_size = log_item.lab_content.GetTextContentSize()
            log_item.SetContentSize(text_size.width + 15, text_size.height)
            log_item.lab_content.SetPosition('50%', '100%')
            roll_container.GetContainer()._refreshItemPos()
            roll_container._refreshItemPos()
            roll_container.UnBindMethod('OnScrolling')
            self.panel.nd_slider.setVisible(False)
            min_offset = roll_container.MinContainerOffset()
            if abs(min_offset.y) > 1:
                slider = self.panel.nd_slider
                slider.setVisible(True)
                container_height = roll_container.GetContentSize()[1]
                content_height = text_size.height
                k = container_height / content_height
                shadow_len = 5
                max_slider_offset = self.panel.nd_slider.GetContentSize()[1] * (1 - k) + shadow_len
                slider.img_slider.SetContentSize(6, k * slider.GetContentSize()[1])

                @roll_container.callback()
                def OnScrolling(*args):
                    cur_offset = roll_container.GetContentOffset()
                    self.panel.img_slider.SetPosition('50%', '0%%%f' % (max_slider_offset * cur_offset.y / min_offset.y - shadow_len))

                OnScrolling()
            return

    def show_locked_log(self, log_id, is_unlocked=None):
        if is_unlocked is None:
            is_unlocked = self.is_unlocked(log_id)
        if is_unlocked:
            self.panel.nd_lock.setVisible(False)
            return
        else:
            self.panel.nd_lock.setVisible(True)
            unlock_param = self.log_info.get(str(log_id), {}).get('unlock_param', {})
            unlock_type = unlock_param.get('type', 0)
            if unlock_type == UNLOCK_TYPE_BOND_LEVEL:
                level = unlock_param.get('level', 1)
                bond_level, cur_exp = global_data.player.get_bond_data(self.role_id)
                self.panel.lab_lock.SetString(get_text_by_id(870033).format(level))
                self.panel.lab_tips.SetString(get_text_by_id(870034).format(bond_level, level))
            return

    def is_unlocked(self, log_id):
        unlock_param = self.log_info.get(str(log_id), {}).get('unlock_param', {})
        unlock_type = unlock_param.get('type', 0)
        if unlock_type == UNLOCK_TYPE_NONE:
            return True
        if unlock_type == UNLOCK_TYPE_BOND_LEVEL:
            item_id = unlock_param.get('item', 0)
            return global_data.player.has_item_by_no(item_id)
        return True