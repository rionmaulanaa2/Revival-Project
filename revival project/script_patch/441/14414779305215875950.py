# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/PVEBattleCustomButtonUI.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const import ui_operation_const
import common.cfg.confmgr as confmgr
import six.moves.cPickle
import copy
from logic.gutils.custom_ui_utils import get_group_all_node_ids, get_custom_node_conf, get_group_names, check_custom_node_group_setting
from logic.gutils.salog import SALog
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils.pve_utils import get_pve_mecha_id_list
from .BattleCustomButtonUI import BattleCustomButtonUI, CustomPanel, CustomNode
SETTING_NO_TEXT_ID = [
 81101, 81102, 81103]
CUSTOM_PANEL_NAME = 'nd_custom_panel %s %d '
ALL_PAGE_LIST = [
 'pve']
PVE_COMMON_SETTING_NO_LIST = ui_operation_const.PVE_COMMON_SETTING_NO_LIST
from common.const import uiconst

class PVECustomNode(CustomNode):

    def get_group_node_ids(self):
        if self._belong_group:
            cur_group_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOM_NODE_GROUPS, default={})
            cur_id = self._cur_setting_no
            node_id_list = cur_group_conf.get(str(cur_id), {}).get(self._belong_group, [])
            return node_id_list
        else:
            return []

    def update_pos_for_resolution_before_save(self, setting_no=None):
        common_setting_no = global_data.player.get_cur_pve_setting_no()
        from logic.gcommon.common_const import ui_operation_const as uoc
        if setting_no is not None:
            is_common = int(setting_no) in uoc.PVE_COMMON_SETTING_NO_LIST
        else:
            is_common = True
        if not is_common:
            common_width = global_data.player.get_cur_custom_setting_resolution_data(self.belong_page, common_setting_no)
            width = global_data.player.get_cur_custom_setting_resolution_data(self.belong_page, setting_no, default=common_width)
        else:
            width = global_data.player.get_cur_custom_setting_resolution_data(self.belong_page, setting_no)
        real_width = global_data.ui_mgr.design_screen_size.width
        if width != real_width:
            lpos = self.adjust_node.getPosition()
            lpos = self.adjust_node.getParent().convertToWorldSpace(lpos)
            self.update_custom_conf({'pos': {'x': int(lpos.x),'y': int(lpos.y)}})
        return


class PVECustomPanel(CustomPanel):

    def check_page_show(self, new_page, ignore_always_show=False):
        panel_conf = confmgr.get('c_pve_panel_custom_conf', str(self.panel_name))
        cAlwaysShow = panel_conf.get('cAlwaysShow', None)
        if cAlwaysShow and not ignore_always_show:
            return
        else:
            if self.belong_page != new_page:
                self.hide_all_node()
            else:
                self.show_valid_node()
            return

    def init_panel_node(self, is_refresh=False, force_panel_conf=None):
        for set_key in self._keys:
            set_key_conf = self._setting_conf.get(set_key)
            if set_key:
                set_val = global_data.player.get_pve_setting(set_key)
                repr_set_val = str(set_val)
                if set_key in self.set_val_convert_func_dict:
                    repr_set_val = self.set_val_convert_func_dict[set_key](set_val)
            else:
                repr_set_val = ''
            set_val_conf = set_key_conf.get(repr_set_val, {})
            node_id_list = set_val_conf.get(self.node_list_key, [])
            if not node_id_list:
                log_error("Can't find node id list", self.panel_name, set_key, repr_set_val)
            if force_panel_conf is None:
                costom_user_ui_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=self._setting_no)
            else:
                costom_user_ui_conf = force_panel_conf
            if int(self._setting_no) + 100 not in PVE_COMMON_SETTING_NO_LIST and not costom_user_ui_conf:
                common_costom_user_ui_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY)
                costom_user_ui_conf = common_costom_user_ui_conf
            import copy
            panel_user_ui_conf = costom_user_ui_conf.get(self.panel_name, {})
            user_setting_conf = panel_user_ui_conf.get(set_key, {}).get(repr_set_val, {})
            if not is_refresh:
                for node_id in node_id_list:
                    node_custom_conf = get_custom_node_conf(node_id)
                    if node_custom_conf.get('bDisable', False):
                        continue
                    c_node = self.create_custom_node(node_id)
                    if c_node:
                        copy_node_id = node_custom_conf.get('cCopySource', None)
                        if copy_node_id:
                            is_node_conf_empty = [ len(each_node_conf) > 0 for each_node_conf in six.itervalues(user_setting_conf.get(str(node_id), {})) ]
                            if not any(is_node_conf_empty):
                                c_node.hide()
                            else:
                                c_node.come_to_life()
                                c_node.set_is_usable(True)
                                c_node.set_user_config(user_setting_conf.get(str(node_id), {}))
                                if not c_node.should_hide():
                                    c_node.show()
                        else:
                            c_node.set_user_config(user_setting_conf.get(str(node_id), {}))
                        c_node.set_exclude_area_list(self._exclude_area_list)

            else:
                for node_id in node_id_list:
                    c_node = self.custom_node_dict.get(node_id, None)
                    if c_node:
                        copy_node_id = c_node.get_copy_source()
                        if copy_node_id:
                            is_node_conf_empty = [ len(each_node_conf) > 0 for each_node_conf in six.itervalues(user_setting_conf.get(str(node_id), {})) ]
                            if not any(is_node_conf_empty):
                                c_node.hide()
                                c_node.set_is_usable(False)
                            else:
                                if not c_node.is_came_to_life():
                                    c_node.come_to_life()
                                if not c_node.get_is_usable():
                                    c_node.set_is_usable(True)
                                c_node.set_user_config(user_setting_conf.get(str(node_id), {}), is_refresh=True)
                                c_node.show()
                        else:
                            c_node.set_user_config(user_setting_conf.get(str(node_id), {}), is_refresh=True)
                        c_node.set_exclude_area_list(self._exclude_area_list)

        return

    def get_save_info(self):
        custom_conf = {}
        for set_key in self._keys:
            set_key_conf = self._setting_conf.get(set_key)
            if set_key:
                set_val = global_data.player.get_pve_setting(set_key)
                repr_set_val = str(set_val)
                if set_key in self.set_val_convert_func_dict:
                    repr_set_val = self.set_val_convert_func_dict[set_key](set_val)
            else:
                repr_set_val = ''
            set_val_conf = set_key_conf.get(repr_set_val, {})
            node_id_list = set_val_conf.get('arrConfigList', [])
            custom_conf.setdefault(set_key, {})
            custom_conf[set_key].setdefault(repr_set_val, {})
            for node_id in node_id_list:
                nd = self.get_custom_node(node_id)
                if nd:
                    nd_conf = nd.get_save_info()
                    custom_conf[set_key][repr_set_val].update({str(node_id): nd_conf})

        return {self.panel_name: custom_conf}

    def create_custom_node(self, node_id):
        c_node = PVECustomNode(node_id, self.start_nd, self.panel_nd, self.root_nd, self.def_range_node, self.belong_page, self._group_conf, self._setting_no)
        if c_node.is_valid():
            self.custom_node_dict[node_id] = c_node
            return c_node
        else:
            c_node.destroy()
            return None
            return None


class PVEBattleCustomButtonUI(BattleCustomButtonUI):

    def on_init_panel(self, page, **kwargs):
        check_custom_node_group_setting()
        self._cur_mecha_id = None
        self.cur_page = page
        self._mecha_only = False
        self._need_del_cur_mecha_setting_no = False
        self._is_just_reverted = True
        self.all_used_page_set = {self.cur_page}
        self.page_panel_list = []
        self.custom_panel_dict = {}
        self.shadow_panel_dict = {}
        self.mecha_panel_common_setting_no = {}
        self.cur_sel_node = None
        self._temp_touch_node_list = []
        self._multiple_select_index = None
        self.is_multiple_sel = False
        self.has_select_in_this_touch = False
        self._drag_mode = self.NONE_MODE
        from common.utils.cocos_utils import getScreenSize
        self._screen_size = getScreenSize()
        self._node_id_2_node_dict = {}
        self._group_conf = copy.deepcopy(global_data.player.get_pve_setting(ui_operation_const.CUSTOM_NODE_GROUPS, {}))
        self._group_setting_btn = None
        self._has_touch_btn_combine = False
        self._need_check_node_sync = True
        ban_area_bl = self.panel.nd_forbidden_area.ConvertToWorldSpace(0, 0)
        ban_area_rt = self.panel.nd_forbidden_area.ConvertToWorldSpacePercentage(100, 100)
        self._cur_save_list = self.panel.temp_save_list
        open_mecha_list = [ int(x) for x in get_pve_mecha_id_list() ]
        self._common_setting_no_list = [
         0, 1, 2]
        self._setting_no_list = self._common_setting_no_list + list(open_mecha_list)
        self.mecha_id_list = open_mecha_list
        import cc
        self._exclude_area_list = (cc.Rect(ban_area_bl.x, ban_area_bl.y, ban_area_rt.x - ban_area_bl.x, ban_area_rt.y - ban_area_bl.y),)
        self._group_names = get_group_names()
        self._group_dict = {}
        for group_name in self._group_names:
            self._group_dict[group_name] = get_group_all_node_ids(group_name)

        self.init_custom_ui()
        self.hide_main_ui(ui_list=['MainSettingUI'])
        for btn, dir_tuple in [(self.panel.btn_up, (0, 1)), (self.panel.btn_down, (0, -1)),
         (
          self.panel.btn_left, (-1, 0)), (self.panel.btn_right, (1, 0))]:
            self.set_move_press_func(btn, dir_tuple[0], dir_tuple[1])

        self.update_page_related_show()
        return

    def switch_mecha_only_state(self, val):
        self._mecha_only = val
        self.panel.btn_driver.setVisible(False)
        self.panel.btn_mecha.setVisible(False)
        self.panel.btn_switch.setVisible(True)
        self.panel.btn_rename.setVisible(not val)
        self.panel.btn_default.SetText(val or 870054 if 1 else 2339)
        if not self._mecha_only:
            self._need_del_cur_mecha_setting_no = False

    def on_click_jump_mecha_btn(self, *args):
        self.switch_to_page('mecha')

    def on_click_jump_human_btn(self, *args):
        self.switch_to_page('mecha')

    def update_page_related_show(self):
        self.panel.btn_mecha.SetSelect(False)
        self.panel.btn_driver.SetSelect(False)

    def create_custom_panel(self, panel_name, parent_nd, cls, page):
        panel_conf = confmgr.get('c_pve_panel_custom_conf', str(panel_name))
        start_node_name = panel_conf.get('cStartNode')
        start_node = getattr(parent_nd, start_node_name)
        if not start_node:
            log_error('Unexist node! panel name:%s node :%s' % (panel_name, start_node_name))
        c_panel = cls(panel_name, start_node, parent_nd, self.panel, self.panel.def_range_node, page, self._group_conf, self._exclude_area_list, self.get_cur_setting_no())
        return c_panel

    def check_default_setting_no(self):
        if global_data.mecha and global_data.mecha.logic:
            mecha_id = global_data.mecha.share_data.ref_mecha_id
            mecha_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=mecha_id)
            has_value = bool(mecha_conf)
            if has_value:
                setting_no = mecha_id
                self._cur_mecha_id = setting_no
                self.switch_mecha_only_state(True)
                self.all_used_page_set = {self.cur_page}
            else:
                self.all_used_page_set = {
                 self.cur_page}

    def create_custom_panel_page_for_setting_no(self, setting_no=None, page=None):
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        if not page:
            page = self.cur_page
        nd = self.generate_custom_page(page, self.panel.nd_content)
        if not nd:
            log_error("Can't find page setting", page)
        else:
            setattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), nd)
        if page == 'mecha':
            nd.setLocalZOrder(1)
        nd_custom_panel = getattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), None)
        custom_name_list = confmgr.get('c_pve_panel_custom_conf')
        for ui_name, conf in six.iteritems(custom_name_list):
            ui_page = conf['cPage']
            if conf['cIsEnable'] and (page == ui_page or ui_page == ''):
                c_panel = self.create_custom_panel(ui_name, nd_custom_panel, PVECustomPanel, page)
                if setting_no not in self.custom_panel_dict:
                    self.custom_panel_dict[setting_no] = list()
                self.custom_panel_dict[setting_no].append(c_panel)
                self.page_panel_list.append(ui_name)
            if not conf['cIsEnable']:
                panel_conf = confmgr.get('c_pve_panel_custom_conf', str(ui_name))
                start_node_name = panel_conf.get('cStartNode')
                start_node = getattr(nd_custom_panel, start_node_name)
                if start_node:
                    print start_node
                    start_node.setVisible(False)

        self._node_id_2_node_dict.setdefault(setting_no, {})
        panel_list = self.custom_panel_dict.get(setting_no, [])
        for c_panel in panel_list:
            node_ids = c_panel.get_node_ids()
            for node_id in node_ids:
                self._node_id_2_node_dict[setting_no].setdefault(str(node_id), [])
                self._node_id_2_node_dict[setting_no][str(node_id)].append(c_panel.get_custom_node(int(node_id)))

        return

    def save_cur_setting(self):
        if not (self.panel and self.panel.isValid()):
            return
        else:
            if not global_data.player:
                log_error('save_cur_setting:global_data.player is None!')
                return
            global_data.game_mgr.show_tip(get_text_local_content(2003))
            is_modified = self.check_has_modified()
            setting_no = self.get_cur_setting_no()
            self.set_panel_force_setting_no(self.get_cur_setting_no(), None)
            if not is_modified:
                if self._need_del_cur_mecha_setting_no and self._mecha_only:
                    global_data.player.revert_custom_setting_resolution_data(self.get_cur_setting_no(), True)
                    self._need_del_cur_mecha_setting_no = False
                    self.save_custom_ui_config({}, to_custom_setting_no=setting_no)
                return
            if self._is_just_reverted:
                global_data.player.revert_custom_setting_resolution_data(setting_no)
                self._is_just_reverted = False
            self.sync_group_top_node_setting_to_member()
            save_info = {}
            for c_panel in self.custom_panel_dict[setting_no]:
                c_panel.update_pos_for_resolution_before_save(setting_no)
                save_info.update(c_panel.get_save_info())

            for c_panel in self.custom_panel_dict[setting_no]:
                c_panel.on_saved()

            save_info = copy.deepcopy(save_info)
            old_costom_user_ui_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
            self.merge_two_custom_info(old_costom_user_ui_conf, save_info)
            if self._mecha_only and self._need_del_cur_mecha_setting_no:
                save_info = {}
                self._need_del_cur_mecha_setting_no = False
            global_data.player.write_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, save_info, page=list(self.all_used_page_set), to_custom_setting_no=setting_no)
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.BATTLE_CTRL_UI, save_info)
            self.save_custom_ui_config(save_info, to_custom_setting_no=setting_no)
            if is_modified:
                global_data.emgr.ui_change_custom_arrange_event.emit()
            self.refresh_save_list(None)
            return

    def save_custom_ui_config(self, _save_info, to_custom_setting_no=None):
        save_info = copy.deepcopy(_save_info)
        for key, value in six.iteritems(save_info):
            if six.PY2:
                save_info[key] = six.moves.cPickle.dumps(value)
            else:
                save_info[key] = value

        if to_custom_setting_no is not None:
            if str(to_custom_setting_no) in get_pve_mecha_id_list():
                to_custom_setting_no *= 100
            else:
                to_custom_setting_no += 100
        else:
            to_custom_setting_no = global_data.player.get_cur_pve_setting_no() + 100
        global_data.player.save_custom_ui_config(save_info, to_custom_setting_no=to_custom_setting_no)
        return

    def revert_to_default_setting(self, setting_no=None):
        if self._mecha_only:
            self._need_del_cur_mecha_setting_no = True
        else:
            self._is_just_reverted = True
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        if not self._mecha_only:
            for c_panel in self.custom_panel_dict.get(setting_no, []):
                c_panel.revert_to_def_setting()
                c_panel.refresh_page_show(self.cur_page, ignore_always_show=self._mecha_only)

        else:
            mecha_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
            is_modified = bool(mecha_conf)
            common_setting_no = global_data.player.get_cur_pve_setting_no()
            self.set_panel_force_setting_no(setting_no, common_setting_no)
            panel_list = self.custom_panel_dict.get(setting_no, [])
            for c_panel in panel_list:
                c_panel.refresh_panel_node(force_panel_conf={})
                if is_modified:
                    c_panel.set_is_force_modified(is_modified)

        if str(setting_no) in self._group_conf:
            new_setting_no_group_conf = {}
            for group_name, group_node_ids in six.iteritems(self._group_conf.get(str(setting_no), {})):
                new_group_node_ids = get_group_all_node_ids(group_name)
                new_setting_no_group_conf[group_name] = new_group_node_ids

            self._group_conf[str(setting_no)] = new_setting_no_group_conf
        return

    def init_save_list(self, is_refresh=False):
        cur_id = self.get_cur_setting_no()
        nd_list = self.panel.temp_save_list.option_list
        if not is_refresh:
            nd_list.DeleteAllSubItem()
        nd_list.SetInitCount(len(self._setting_no_list))
        for i, _setting_no in enumerate(self._setting_no_list):
            nd = nd_list.GetItem(i)
            if _setting_no in self.mecha_id_list:
                nd.nd_1.setVisible(False)
                nd.nd_2.setVisible(True)
                nd.lab_mecha.SetString(self.get_setting_no_page_name(_setting_no))
                from logic.gutils.item_utils import get_locate_pic_path
                from logic.gcommon.common_const.battle_const import LOCATE_MECHA
                nd.img_mecha.SetDisplayFrameByPath('', get_locate_pic_path(LOCATE_MECHA, None, mecha_id=_setting_no))
                mecha_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=_setting_no)
                nd.lab_type.setVisible(bool(mecha_conf))
                nd.btn_copy.setVisible(_setting_no != cur_id and cur_id in self.mecha_id_list)
            else:
                nd.nd_1.setVisible(True)
                nd.nd_2.setVisible(False)
                nd.lab_content.SetString(self.get_setting_no_page_name(_setting_no))
                nd.btn_copy.setVisible(cur_id not in self.mecha_id_list and _setting_no != cur_id)
            self._register_save_list_item_click(nd.button, _setting_no)

            @nd.btn_copy.callback()
            def OnClick(btn, touch, new_i=_setting_no):
                self.on_copy_between_page(new_i)

        self.panel.btn_save_list.SetText(self.get_setting_no_page_name(cur_id))
        return

    def refresh_save_list(self, setting_no):
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        common_setting_no = global_data.player.get_cur_pve_setting_no()
        for i, _setting_no in enumerate(self._setting_no_list):
            nd = self._cur_save_list.option_list.GetItem(i)
            nd.button.SetSelect(setting_no == _setting_no)
            if _setting_no in self.mecha_id_list:
                nd.btn_copy.setVisible(setting_no != _setting_no and setting_no in self.mecha_id_list)
            else:
                nd.btn_copy.setVisible(setting_no != _setting_no and setting_no in self._common_setting_no_list)
            if common_setting_no == _setting_no and setting_no not in self._common_setting_no_list:
                nd.img_choose.setVisible(True)
            else:
                nd.img_choose.setVisible(False)
            if _setting_no in self.mecha_id_list:
                mecha_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=_setting_no)
                nd.lab_type.setVisible(bool(mecha_conf))

        return

    def on_switch_setting_no(self, old_setting_no, setting_no, is_init=False):
        self.refresh_save_list(setting_no)
        old_mecha_only = self._mecha_only
        if setting_no in self.mecha_id_list:
            self.switch_mecha_only_state(True)
        else:
            self.switch_mecha_only_state(False)
        self._need_del_cur_mecha_setting_no = False
        self._is_just_reverted = False
        if not self._mecha_only:
            global_data.player.set_cur_pve_setting_no(setting_no)
        else:
            self._cur_mecha_id = setting_no
        common_setting_no = global_data.player.get_cur_pve_setting_no()
        self._cur_save_list.setVisible(False)
        self.panel.btn_save_list.SetText(self.get_setting_no_page_name(setting_no))
        all_page_list = [
         self.cur_page]
        for page in all_page_list:
            old_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (page, old_setting_no), None)
            old_nd_custom and old_nd_custom.setVisible(False)

        all_page_list = {
         self.cur_page}
        for page in all_page_list:
            new_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), None)
            if not new_nd_custom:
                self.create_custom_panel_page_for_setting_no(setting_no=setting_no, page=page)
                new_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), None)
                if self._mecha_only:
                    self.mecha_panel_common_setting_no[setting_no] = common_setting_no
            new_nd_custom and new_nd_custom.setVisible(True)

        for c_panel in self.custom_panel_dict.get(setting_no, []):
            c_panel.refresh_page_show(self.cur_page, ignore_always_show=self._mecha_only)

        if self._mecha_only:
            mecha_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
            if not bool(mecha_conf):
                panel_list = self.custom_panel_dict.get(setting_no, [])
                for c_panel in panel_list:
                    c_panel.refresh_panel_node()

                self.mecha_panel_common_setting_no[setting_no] = common_setting_no
        self.select_node(None)
        self.check_save_button_state()
        if not is_init:
            global_data.emgr.ui_change_custom_arrange_event.emit()
        self._need_check_node_sync = True
        self.update_page_related_show()
        self.all_used_page_set = set(all_page_list)
        return

    def on_copy_setting_no(self, from_no, to_no):
        self._cur_save_list.setVisible(False)
        from_user_ui_conf = global_data.player.get_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=from_no)
        conf = copy.deepcopy(from_user_ui_conf)
        all_used_page_set = ALL_PAGE_LIST
        global_data.player.write_pve_setting(ui_operation_const.CUSTOMER_UI_KEY, conf, page=list(all_used_page_set), to_custom_setting_no=to_no)
        for page in all_used_page_set:
            global_data.player.copy_custom_setting_resolution_data(page, from_no, to_no)

        if str(from_no) in self._group_conf:
            self._group_conf[str(to_no)] = copy.deepcopy(self._group_conf[str(from_no)])
        elif not self._mecha_only:
            log_error('group node should have data in it!!!', self._group_conf)
        self.save_custom_ui_config(conf, to_custom_setting_no=to_no)
        panel_list = self.custom_panel_dict.get(to_no, [])
        for c_panel in panel_list:
            c_panel.refresh_panel_node()

        global_data.game_mgr.show_tip(get_text_by_id(860183, {'scheme': self.get_setting_no_page_name(to_no)}))
        self.refresh_save_list(None)
        if to_no in self.mecha_id_list:
            target_mecha_id = None
            if global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_is_mecha:
                target_mecha_id = global_data.cam_lctarget.share_data.ref_mecha_id
            elif global_data.mecha and global_data.mecha.logic:
                target_mecha_id = global_data.mecha.share_data.ref_mecha_id
            if str(target_mecha_id) == str(to_no):
                global_data.emgr.ui_change_custom_arrange_event.emit()
        return

    def get_setting_no_page_name(self, setting_no):
        if int(setting_no) in self.mecha_id_list:
            return get_mecha_name_by_id(setting_no)
        else:
            setting_no = int(setting_no)
            name = global_data.player.get_pve_setting(ui_operation_const.CUSTOM_PAGE_NAME_PREFIX + str(setting_no + 1))
            if not name:
                return get_text_by_id(SETTING_NO_TEXT_ID[setting_no])
            return name

    def change_setting_no_page_name(self, setting_no, name):
        setting_no = int(setting_no)
        global_data.player.write_pve_setting(ui_operation_const.CUSTOM_PAGE_NAME_PREFIX + str(setting_no + 1), name)
        cur_id = self.get_cur_setting_no()
        if str(setting_no) == str(cur_id):
            self.panel.btn_save_list.SetText(self.get_setting_no_page_name(cur_id))
        nd_list = self._cur_save_list.option_list
        nd = nd_list.GetItem(setting_no)
        if nd:
            nd.button.SetText(name)

    def get_cur_setting_no(self):
        if not self._mecha_only and global_data.player:
            return global_data.player.get_cur_pve_setting_no()
        else:
            return self._cur_mecha_id