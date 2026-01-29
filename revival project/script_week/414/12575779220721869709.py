# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/GameFeedbackUI.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import micro_webservice_utils
import logic.comsys.common_ui.InputBox as InputBox
from common.const import uiconst
ISSUE_BTN_SHOW_SETTINGS = [{'text_id': 83551,'key': '1'}, {'text_id': 83552,'key': '2'}, {'text_id': 83553,'key': '3'}, {'text_id': 83554,'key': '4'}, {'text_id': 83555,'key': '5'}, {'text_id': 83556,'key': '6'}, {'text_id': 83557,'key': '7'}, {'text_id': 83558,'key': '8'}, {'text_id': 83559,'key': '9'}]
ACCOUNT_BTN_SHOW_SETTINGS = [{'text_id': 83561,'key': '101'}, {'text_id': 83562,'key': '102'}, {'text_id': 83563,'key': '103'}, {'text_id': 83564,'key': '104'}, {'text_id': 83565,'key': '105'}]
RELEASE_SERVER_LIST = [
 'https://g93na.update.easebar.com/serverlist.txt',
 'https://g93na.update.easebar.com/serverlist.txt',
 'https://g93.update.netease.com/serverlist.txt']

def is_release_env():
    return True
    import game3d
    from common.platform.dctool import interface
    serverlist_URL = interface.get_serverlist_URL()
    IS_RELEASE = game3d.is_release_version()
    if serverlist_URL in RELEASE_SERVER_LIST and IS_RELEASE:
        return True
    return False


class GameFeedbackUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/i_setting_feedback_collection'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'pnl_content'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'btn_other.OnClick': 'on_click_other_issue',
       'temp_btn_1.btn_common_big.OnClick': 'on_click_commit_btn',
       'temp_btn_2.btn_common_big.OnClick': 'on_click_help_btn'
       }

    def on_init_panel(self):
        super(GameFeedbackUI, self).on_init_panel()
        hostnum = global_data.channel.get_host_num()
        self.account_issue_btns = []
        self.sel_issue_idxs = {}
        self.sel_account_idx = None
        self.init_issue_list()
        self.init_account_list()
        self.init_input_ui()
        self.init_help_btn_show()
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def init_help_btn_show(self):
        host_num = global_data.channel.get_host_num()
        self.panel.temp_btn_2.btn_common_big.setVisible(host_num > 0)

    def init_input_ui(self):
        panel = self.panel
        TEXT_MAX_LEN_JUDGEMENT = 150

        def send_cb(*args, **kwargs):
            pass

        def max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        self._input_box = InputBox.InputBox(self.temp_input, max_length=TEXT_MAX_LEN_JUDGEMENT, max_input_cb=max_input_cb, send_callback=send_cb, detach_after_enter=False, placeholder=get_text_by_id(83567))
        self._input_box.set_rise_widget(self.panel)
        self._input_box.enable_input(False)

    def on_click_close_btn(self, *args):
        self.close()

    def hide_close_btn(self):
        self.panel.pnl_content.btn_close.setVisible(False)

    def init_issue_list(self):
        SETTING_CONFIG = ISSUE_BTN_SHOW_SETTINGS
        cnt = len(SETTING_CONFIG)
        list_table = self.nd_sys.list_check_box
        list_table.SetInitCount(cnt)
        for i in range(cnt):
            item = list_table.GetItem(i)
            data = SETTING_CONFIG[i]
            item.text.SetString(get_text_by_id(data.get('text_id')))
            item.choose.setVisible(False)
            self.sel_issue_idxs[i] = False

            @item.btn.callback()
            def OnClick(btn, touch, idx=i, _item=item):
                is_show = not _item.choose.isVisible()
                _item.choose.setVisible(is_show)
                self.sel_issue_idxs[idx] = is_show

    def init_account_list(self):

        def set_group_check(item):
            for _item in self.account_issue_btns:
                _item.choose.setVisible(item == _item)

        self.account_issue_btns = []
        SETTING_CONFIG = ACCOUNT_BTN_SHOW_SETTINGS
        cnt = len(SETTING_CONFIG)
        list_table = self.nd_account.list_check_box
        list_table.SetInitCount(cnt)
        for i in range(cnt):
            item = list_table.GetItem(i)
            data = SETTING_CONFIG[i]
            item.text.SetString(get_text_by_id(data.get('text_id')))
            item.choose.setVisible(False)
            self.account_issue_btns.append(item)

            @item.btn.callback()
            def OnClick(btn, touch, idx=i, _item=item):
                self.sel_account_idx = idx
                set_group_check(_item)

    def get_commit_data(self):
        issue_type = []
        issue_type_text = []
        for idx, value in six_ex.items(self.sel_issue_idxs):
            if value:
                config = ISSUE_BTN_SHOW_SETTINGS[idx]
                issue_type.append(config.get('key'))
                issue_type_text.append(get_text_by_id(config.get('text_id')))

        account_type = ''
        account_type_text = ''
        if self.sel_account_idx is not None:
            config = ACCOUNT_BTN_SHOW_SETTINGS[self.sel_account_idx]
            account_type = config.get('key')
            account_type_text = get_text_by_id(config.get('text_id'))
        other_issue = self._input_box.get_text()
        return (
         issue_type, account_type, other_issue)

    def on_click_other_issue(self, *args):
        global_data.ui_mgr.show_ui('CommonInputUI', 'logic.comsys.setting_ui')
        ui = global_data.ui_mgr.get_ui('CommonInputUI')
        other_issue = self._input_box.get_text()
        ui.configure_panel(self.on_other_issue_confirm, title=get_text_by_id(83566), content=other_issue)

    def on_other_issue_confirm(self, content):
        self._input_box.set_text(content)

    def get_host_num(self):
        if is_release_env():
            return 10000
        return 230

    def get_login_info(self):
        last_login_info = global_data.achi_mgr.get_login_account_data_value('login_history', {})
        hostnum = self.get_host_num()
        role_id = global_data.player.uid if global_data.player else last_login_info.get('uid', 0)
        character_name = global_data.player.char_name if global_data.player else last_login_info.get('char_name', '')
        return (
         hostnum, role_id, character_name)

    def on_click_commit_btn(self, *args):
        import time
        import version
        import game3d
        issue_type_lst, account_type, other_issue = self.get_commit_data()
        if not account_type and len(issue_type_lst) <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(83573))
            return
        else:
            url_hostnum, role_id, character_name = self.get_login_info()
            platform = game3d.get_platform()
            device_info = global_data.deviceinfo
            engine_v = game3d.get_engine_version()
            engine_svn = game3d.get_engine_svn_version()
            device_id = global_data.channel.get_udid()
            app_channel = global_data.channel.get_app_channel()
            dict_hostnum = self.get_host_num()
            data = {'issuses': issue_type_lst,
               'account_channel': account_type,
               'content': other_issue,
               'create_at_stamp': int(time.time()),
               'os_name': device_info.get_os_name(),
               'device_id': device_id,
               'network': device_info.get_network(),
               'device_model': device_info.get_device_model(),
               'app_channel': app_channel,
               'udid': device_id,
               'engine_version': version.get_engine_version(),
               'script_version': version.get_script_version(),
               'engine_svn': engine_svn,
               'role_id': role_id,
               'character_name': character_name,
               'os_ver': device_info.get_os_ver()
               }
            if dict_hostnum:
                data['hostnum'] = dict_hostnum
            micro_service_url = None if is_release_env() else 'http://10.149.22.102:43040'
            micro_webservice_utils.micro_service_post('CSQuestionaire', data, None, url_hostnum, role_id, token='', micro_service_url=micro_service_url)
            global_data.game_mgr.show_tip(get_text_by_id(860470))
            self.close()
            return

    def on_click_help_btn(self, *args):
        import game3d
        if hasattr(game3d, 'open_gm_web_view'):
            global_data.player.get_custom_service_token()
            game3d.open_gm_web_view('')
        else:
            data = {'methodId': 'ntOpenGMPage',
               'refer': ''
               }
            global_data.channel.extend_func_by_dict(data)