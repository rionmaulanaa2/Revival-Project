# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/SvrSelectUI.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
from common.framework import Functor
from logic.comsys.login.LoginHelper import LoginHelper
from logic.gcommon.common_const.login_const import SVR_STATE_RES_MAP
import common.const.uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.platform.dctool import interface
import game3d
import os
DISPLAY_RECOMMEND_SERVERS = 0
DISPLAY_ALL_SERVERS = 1
DISPLAY_MOBILE_SERVERS = 2
DISPLAY_PLATFROM_ALL_SERVERS = 3
from common.const import uiconst

class SvrSelectUI(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    PANEL_CONFIG_NAME = 'login/server'
    UI_ACTION_EVENT = {'bg_panel.btn_close.OnClick': 'on_click_close_btn'
       }
    UI_EFFECT_LIST = [{'node': 'bg_panel','anim': 'in','time': 0}]
    CONTENT_NODES = [
     'list_node']

    def on_init_panel(self, **kwargs):
        SvrSelectUI.DELAY_TIME = 0.5
        self.panel.bg_panel.list_tab.setVisible(False)
        self.magic_count = 0

    def on_delay_init_panel(self, **kwargs):
        self.recommend_list.setVisible(False)
        self.all_svr_list.setVisible(True)
        self.display_state = DISPLAY_PLATFROM_ALL_SERVERS if global_data.is_pc_mode else DISPLAY_MOBILE_SERVERS
        if global_data.channel.is_steam_channel():
            self.display_state = DISPLAY_ALL_SERVERS
        self.init_event()
        self.init_tab_head()
        self.on_click_tab(self.display_state)
        self.init_ios_magic()

    def magic_click_function(self, item, touch):
        pos = touch.getStartLocation()
        print('magic_click_function', pos)
        self.magic_count += 1
        if self.magic_count == 10:
            doc_dir = game3d.get_doc_dir()
            filename = 'ios_debug.txt'
            try:
                filepath = os.path.join(doc_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write('ok')
            except Exception as e:
                print('except', str(e))

            self.close()

    def init_ios_magic(self):
        print('init_ios_magic')
        try:
            if True or game3d.get_platform() == game3d.PLATFORM_IOS:
                print('init_ios_magic 1')
                item = self.panel.bg_panel
                item.SetEnableTouch(True)
                item.BindMethod('OnBegin', self.magic_click_function)
                print('init_ios_magic 2')
        except Exception as e:
            print('excetion', str(e))
            return

    def init_event(self):
        global_data.emgr.registed_account_updated_event += self.update_svr_list
        global_data.emgr.on_server_list_refresh_event += self.update_svr_list
        global_data.emgr.on_delay_refreshed_event += self.update_svr_list

    def on_click_close_btn(self, *args):
        global_data.ui_mgr.close_ui(self)

    def on_finalize(self, *args):
        super(SvrSelectUI, self).on_finalize()

    def update_svr_list(self, *args):
        self.update_all_servers()

    def set_visible_server_list(self):
        all_server_visible = self.display_state == DISPLAY_ALL_SERVERS
        self.all_svr_list.setVisible(all_server_visible)

    def add_list_header(self, head_str, container_list, temp='login/server_title'):
        head_item = global_data.uisystem.load_template_create(temp)
        head_item.txt_head.SetString(head_str)
        container_list.AddControl(head_item, bRefresh=True)
        return head_item

    def update_all_servers(self):
        svr_list = LoginHelper().server_list
        list_container = self.panel.all_svr_list
        self.update_server_list(list_container, svr_list)

    def filter_server_list(self, svr_list):
        display_idx = self.display_state
        tab_index = self.display_tab_dict[display_idx]
        filter_data = self.tab_data[tab_index][2]
        ret_list = []
        for info in svr_list:
            if info['svr_platform'] not in filter_data:
                continue
            ret_list.append(info)

        def svr_cmp--- This code section failed: ---

 134       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_GLOBAL           2  'int'
           9  LOAD_GLOBAL           1  'compare'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_1       1 
          16  LOAD_GLOBAL           2  'int'
          19  LOAD_FAST             1  'b'
          22  LOAD_CONST            1  'svr_num'
          25  BINARY_SUBSCR    
          26  CALL_FUNCTION_1       1 
          29  CALL_FUNCTION_2       2 
          32  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 29

        ret_list.sort(key=cmp_to_key(svr_cmp))
        return ret_list

    def update_server_list(self, ui_list, data_list):
        ui_list.DeleteAllSubItem()
        data_list = self.filter_server_list(data_list)
        len_list = len(data_list)
        ui_list.SetInitCount(len_list)
        items = ui_list.GetAllItem()
        for idx, item in enumerate(items):
            self.update_svr_item_data(item, idx, data_list[idx])

    def update_svr_item_data(self, item, idx, server_info):
        helper = LoginHelper()
        svr_name = helper.get_svr_text_from_ext_info(server_info, 'svr_id') or server_info['svr_name']
        item.lab_server.SetString('%s' % svr_name if svr_name and svr_name != 'unknown' else server_info['svr_ip_port'])
        has_role = server_info['svr_num'] in LoginHelper().registed_host_num_role_dict
        head_visible = has_role
        item.img_head.setVisible(head_visible)
        item.img_new.setVisible(False and not head_visible and server_info['svr_new_state'] == 1)
        item.img_state.SetDisplayFrameByPath('', SVR_STATE_RES_MAP[server_info['svr_state']])
        delay_exist = False
        delay_num = 1000
        if not head_visible:
            delay_exist, delay_num = helper.get_cluster_delay_info(server_info['svr_type'])
        item.lab_delay.setVisible(not head_visible and delay_exist)
        if delay_exist:
            delay_num = int(delay_num)
            delay_text_pattern = '(%dms)'
            if delay_num >= 300:
                item.lab_delay.SetColor('#SR')
            elif 300 > delay_num >= 120:
                item.lab_delay.SetColor('#BO')
            else:
                item.lab_delay.SetColor('#BG')
            delay_text = delay_text_pattern % delay_num
            item.lab_delay.SetString(delay_text)
        func = Functor(self.on_click_item, server_info['svr_num'])
        item.BindMethod('OnClick', func)

    def on_get_template_name(self):
        return 'login/server'

    def on_click_item(self, idx, *args):
        from .LoginHelper import LoginHelper
        login_helper = LoginHelper()
        if login_helper.server_list:
            from logic.comsys.login.MainLoginUI import MainLoginUI
            MainLoginUI().set_select_host_num(idx)
            self.on_click_close_btn()

    def on_click_tab(self, display_idx, *args):
        self.display_state = display_idx
        tab_idx = self.display_tab_dict[self.display_state]
        self.update_svr_list()
        tabs = self.panel.bg_panel.list_tab
        tabs_count = tabs.GetItemCount()
        for i in range(0, tabs_count):
            sub_tab = tabs.GetItem(i)
            sub_tab.btn_window_tab._updateCurState(1 if tab_idx == i else 0)

    def refresh_tab_head(self):
        tabs = self.panel.bg_panel.list_tab
        tabs.setVisible(True)

    def OnClickTab(self, data, *args):
        self.on_click_tab(data[0])

    def init_tab_head(self):
        tabs = self.panel.bg_panel.list_tab
        tabs.setVisible(True)
        init_data = [
         (
          DISPLAY_MOBILE_SERVERS, 609365, ['mobile']),
         (
          DISPLAY_PLATFROM_ALL_SERVERS, 609366, ['all']),
         (
          DISPLAY_ALL_SERVERS, 12013, ['mobile', 'all', 'match'])]
        if global_data.is_pc_mode:
            init_data = [(DISPLAY_PLATFROM_ALL_SERVERS, 609366, ['all', 'win32']),
             (
              DISPLAY_ALL_SERVERS, 12013, ['mobile', 'all', 'win32', 'match'])]
        if not interface.is_mainland_package():
            if not global_data.is_pc_mode:
                init_data = [(DISPLAY_MOBILE_SERVERS, 609365, ['mobile']),
                 (
                  DISPLAY_ALL_SERVERS, 12013, ['mobile', 'all', 'match'])]
        if global_data.channel.is_steam_channel():
            init_data = [(DISPLAY_ALL_SERVERS, 12013, ['all', 'steam', 'match'])]
        tab_count = len(init_data)
        tabs.SetInitCount(tab_count)
        self.tab_data = init_data
        self.display_tab_dict = {}
        for i in range(tab_count):
            sub_tab = tabs.GetItem(i)
            btn_data = init_data[i]
            sub_tab.btn_window_tab.SetText(btn_data[1])
            sub_tab.btn_window_tab.BindMethod('OnClick', Functor(self.OnClickTab, btn_data))
            self.display_tab_dict[btn_data[0]] = i