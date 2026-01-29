# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/report/UserReportUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gutils import template_utils
from logic.gutils.new_template_utils import MultiChooseWidget
import logic.gcommon.time_utility as t_util
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import log_const
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class UserReportUI(WindowMediumBase):
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    PANEL_CONFIG_NAME = 'chat/i_chat_report'
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'report_window'
    SEND_CD = 1
    MIN_REPORT_LV = 3
    UI_ACTION_EVENT = {'btn_confirm.btn_common.OnClick': 'on_confirm_report'
       }
    GLOBAL_EVENT = {'on_report_result_event': 'on_report_send_ret',
       'on_report_times_change_event': 'on_report_times_change'
       }

    def on_init_panel(self, *args):
        super(UserReportUI, self).on_init_panel()
        self.show_reason_list = []
        self.report_class = None
        self._input_box = None
        self._extra_info_dict = {}
        self._additional_info_dict = {}
        self._close_callback = None
        self._settle_info = {}
        self._selected_player_info = {}
        self._report_ddl_ts = None
        self._nd_content = self.panel.list_content.GetContainer()
        self.panel.list_content.SetTouchEnabled(False)
        self.init_remain_times()
        self.set_custom_close_func(self.on_click_close_btn)
        return

    def init_remain_times(self):
        player = global_data.player
        if not player:
            self.panel.lab_remain.setVisible(False)
            return
        self.panel.lab_remain.setVisible(True)
        times = player.get_report_player_times()
        self.panel.lab_remain.SetString(get_text_by_id(606034, (times, log_const.REPORT_PLAYER_DAY_LIMIT)))

    def update_battle_status(self):
        in_battle = not global_data.player or global_data.player.is_in_battle()
        from_way = self._extra_info_dict.get('from', -1)
        in_histroy = from_way == log_const.REPORT_FROM_TYPE_BATTLE_HISTORY
        show_sign = not in_battle and not in_histroy
        self._nd_content.nd_player_info.nd_player_sign.setVisible(show_sign)
        if not show_sign:
            origin_pos = self._nd_content.nd_report_content.GetPosition()
            origin_pos_line = self._nd_content.img_line.GetPosition()
            self._nd_content.nd_report_content.SetPosition(origin_pos[0], origin_pos[1] + 100)
            self._nd_content.img_line.SetPosition(origin_pos_line[0], origin_pos_line[1] + 100)

    def on_finalize_panel(self):
        self.destroy_widget('multiChooseWidget')
        self.destroy_widget('name_widget')
        self.destroy_widget('intro_widget')
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def set_close_callback(self, callback):
        self._close_callback = callback

    def on_click_close_btn(self, *args):
        if self._close_callback and callable(self._close_callback):
            self._close_callback()
        self.close()

    def set_report_player(self, player_data):
        name = player_data.get('name', '')
        intro = player_data.get('intro', '')
        self._selected_player_info = player_data
        self._nd_content.lab_player_name.SetString(name)
        self._nd_content.btn_player_list.SetText(name)
        self._nd_content.lab_player_sign.SetString(intro)

    def set_report_ddl(self, ts):
        self._report_ddl_ts = ts

    def check_name_postfix(self, player_data):
        uid = player_data.get('uid')
        eid = player_data.get('eid')
        name = player_data.get('name', '')
        name_post_fix = ''
        if eid:
            is_killer = self.check_is_killer(eid)
            is_teammate = self.check_is_teammate(eid)
            if is_killer:
                name_post_fix = '(%s)' % get_text_local_content(80889)
            elif is_teammate:
                name_post_fix = '(%s)' % get_text_local_content(80890)
        return name + name_post_fix

    def set_extra_report_info(self, channel, chat_content, from_way):
        self._extra_info_dict = {'channel': channel,'chat': chat_content,'from': from_way}
        self.update_battle_status()

    def set_hm_extra_report_info(self, msg_content, from_way):
        self._extra_info_dict = {'chat': msg_content,'from': from_way}

    def set_additional_report_info(self, additional_info_dict):
        if additional_info_dict:
            self._additional_info_dict = additional_info_dict

    def set_settle_info(self, info):
        self._settle_info = info

    def set_report_class(self, report_class):
        self.report_class = report_class
        self.init_report_reasons()
        self.init_report_reason_player_name()
        self.init_report_reason_player_intro()

    def check_is_killer(self, eid):
        if global_data.player and global_data.player.logic:
            if global_data.player.logic.ev_g_killer_id() == eid:
                return True
        return False

    def check_is_teammate(self, eid):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_is_groupmate(eid, False)
        return False

    def check_user_lv_can_report(self):
        if global_data.player:
            if global_data.player.get_lv() < self.MIN_REPORT_LV:
                global_data.game_mgr.show_tip(get_text_by_id(80894, {'lv': int(self.MIN_REPORT_LV)}))
                return False
        return True

    def check_report_ddl(self):
        if self._report_ddl_ts and t_util.get_server_time() > self._report_ddl_ts:
            global_data.game_mgr.show_tip(get_text_by_id(900026))
            return False
        return True

    def check_send_cd(self):
        if global_data._last_report_send_timestamp:
            cur_time = t_util.get_server_time()
            if cur_time - global_data._last_report_send_timestamp < self.SEND_CD:
                second_later = global_data._last_report_send_timestamp + self.SEND_CD - cur_time + 1
                global_data.game_mgr.show_tip(get_text_by_id(80895, {'time': int(second_later)}))
                return False
        return True

    def check_is_selection_valid(self):
        OTHER_SELECTION = 8
        selections = self.multiChooseWidget.GetSelects()
        name_selection = self.name_widget.GetSelects()
        intro_selection = self.intro_widget.GetSelects()
        if len(selections) <= 0 and len(name_selection) <= 0 and len(intro_selection) <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(80891))
            return False
        for sel in selections:
            reason = self.show_reason_list[sel]
            if str(reason.get('report_id')) == str(log_const.REPORT_REASON_OTHERS):
                input_txt = self._input_box.get_text()
                if input_txt == '':
                    global_data.game_mgr.show_tip(get_text_by_id(80892))
                    return False

        return True

    def report_battle_users(self, user_info_list, enable_teammates=False, enable_killer=False):
        user_ids = [ user_info.get('eid') for user_info in user_info_list ]
        extra_list = UserReportUI.get_possible_report_targets(enable_teammates, enable_killer)
        for member_info in extra_list:
            if member_info:
                mem_id = member_info.get('eid', None)
                if mem_id not in user_ids:
                    user_info_list.append(member_info)

        self._set_report_users(user_info_list)
        return

    def _set_report_users(self, user_info_list):
        self._nd_content.temp_list.setVisible(False)
        if len(user_info_list) > 1:
            self._nd_content.btn_player_list.setVisible(True)
            self._nd_content.lab_player_name.setVisible(False)
            self._nd_content.img_name_bg_1.setVisible(False)
        else:
            self._nd_content.btn_player_list.setVisible(False)
            self._nd_content.lab_player_name.setVisible(True)
            self._nd_content.img_name_bg_1.setVisible(True)
        if len(user_info_list) <= 0:
            log_error("Can't find report target!!!")
            return
        for user_info in user_info_list:
            user_info.update({'name': self.check_name_postfix(user_info)})

        self.set_report_player(user_info_list[0])
        if len(user_info_list) > 1:

            def callback(index):
                self._nd_content.temp_list.setVisible(False)
                if index < len(user_info_list):
                    self.set_report_player(user_info_list[index])

            template_utils.init_common_choose_list(self._nd_content.temp_list, user_info_list, callback)

        @self._nd_content.btn_player_list.callback()
        def OnClick(btn, touch):
            self._nd_content.temp_list.setVisible(not self._nd_content.temp_list.isVisible())

    def report_users(self, user_info_list):
        self._set_report_users(user_info_list)

    def init_report_reasons(self):
        from common.cfg import confmgr
        report_conf = confmgr.get('user_report_conf', 'ReportConfig', 'Content')
        int_keys = [ int(k) for k in six_ex.keys(report_conf) ]
        reason_uids = sorted(int_keys)
        reason_info_list = []
        for uid in reason_uids:
            if uid in (log_const.REPORT_REASON_ILLEGAL_NAME,):
                continue
            uid = str(uid)
            dic = dict(report_conf[uid])
            dic.update({'report_id': uid})
            reason_info_list.append(dic)

        res_list = [ x for x in reason_info_list if self.report_class in x.get('iClass', []) ]
        common_report_container = self._nd_content.nd_report_content.report_container
        common_report_container.SetInitCount(len(res_list))
        self.show_reason_list = res_list
        all_item = common_report_container.GetAllItem()
        for idx, ui_item in enumerate(all_item):
            data = self.show_reason_list[idx]
            ui_item.text.SetString(data.get('cReportText'), '')

        self.multiChooseWidget = MultiChooseWidget()
        self.multiChooseWidget.init(self.panel, all_item, [])
        self.multiChooseWidget.SetCallbacks(self.OnSelItem, None)
        import logic.comsys.common_ui.InputBox as InputBox
        if global_data.is_pc_mode:
            send_callback = self._on_confirm_report
        else:
            send_callback = None
        self._input_box = InputBox.InputBox(self._nd_content.input_box, send_callback=send_callback)
        self._input_box.set_rise_widget(self.panel)
        return

    def init_report_reason_player_name(self):
        name_container = self._nd_content.nd_player_info.nd_player.report_container
        name_container.SetInitCount(1)
        name_items = name_container.GetAllItem()
        self.name_widget = MultiChooseWidget()
        self.name_widget.init(self.panel, name_items, [])
        self.name_widget.SetCallbacks(None, None)
        return

    def init_report_reason_player_intro(self):
        intro_container = self._nd_content.nd_player_info.nd_player_sign.report_container_sign
        intro_container.SetInitCount(1)
        intro_items = intro_container.GetAllItem()
        self.intro_widget = MultiChooseWidget()
        self.intro_widget.init(self.panel, intro_items, [])

    def OnSelItem(self, idx, is_sel):
        if idx < len(self.show_reason_list):
            reason = self.show_reason_list[idx]
            if reason.get('report_id') == str(log_const.REPORT_REASON_OTHERS):
                in_battle = not global_data.player or global_data.player.is_in_battle()
                from_way = self._extra_info_dict.get('from', -1)
                if in_battle or from_way == log_const.REPORT_FROM_TYPE_BATTLE_HISTORY:
                    return
                if is_sel:
                    self.panel.list_content.ScrollToBottom()
                    self.panel.list_content.SetTouchEnabled(True)
                else:
                    self.panel.list_content.ScrollToTop()
                    self.panel.list_content.SetTouchEnabled(False)

    def sel_index_to_select_report_reasons(self, sel_index_list):
        reason_list = []
        for sel_idx in sel_index_list:
            if sel_idx < len(self.show_reason_list):
                reason = self.show_reason_list[sel_idx]
                reason_list.append(int(reason.get('report_id')))

        return reason_list

    def on_confirm_report(self, btn, touch):
        return self._on_confirm_report()

    def _on_confirm_report(self):
        if not self.check_user_lv_can_report():
            return
        else:
            if not self.check_report_ddl():
                self.close()
                return
            if not self.check_send_cd():
                return
            if not self.check_is_selection_valid():
                return
            report_reasons = self.sel_index_to_select_report_reasons(self.multiChooseWidget.GetSelects())
            if self.name_widget.GetSelects():
                report_reasons.append(log_const.REPORT_REASON_ILLEGAL_NAME)
            if self.intro_widget.GetSelects():
                report_reasons.append(log_const.REPORT_REASON_ILLEGAL_PLAYER_INTRO)
            if global_data.player and self._selected_player_info:
                from_way = self._extra_info_dict.get('from', log_const.REPORT_FROM_TYPE_BATTLE_END)
                if log_const.REPORT_REASON_OTHERS in report_reasons:
                    content = self._input_box.get_text()
                else:
                    content = ''
                if self.report_class == log_const.REPORT_CLASS_BATTLE:
                    if from_way == log_const.REPORT_FROM_TYPE_BATTLE_HISTORY:
                        target_uid = self._selected_player_info.get('uid')
                        global_data.player.report_someone_from_battle_history(from_way, target_uid, report_reasons, content)
                        game_id = self._additional_info_dict.get('game_id', None)
                        group_id = self._additional_info_dict.get('group_id', None)
                        battle_server_name = self._additional_info_dict.get('battle_server_name', None)
                        if game_id and group_id:
                            param = {'game_id': game_id,'group_id': group_id,
                               'from_way': log_const.REPORT_FROM_TYPE_BATTLE_HISTORY,
                               'battle_server_name': battle_server_name
                               }
                            global_data.player.credit_report(target_uid, param)
                    else:
                        target_id = self._selected_player_info.get('eid')
                        global_data.player.report_someone_in_battle(from_way, target_id, report_reasons, content)
                        credit_afk_stub = self._settle_info.get('credit_afk_stub', None)
                        if credit_afk_stub:
                            param = {'game_id': self._settle_info['game_id'],'group_id': self._settle_info['group_id'],
                               'credit_afk_stub': credit_afk_stub
                               }
                            uid = self._selected_player_info.get('uid', None)
                            if uid is None:
                                from mobile.common.EntityManager import EntityManager
                                entity = EntityManager.getentity(target_id)
                                if entity and hasattr(entity, 'uid') and entity.uid:
                                    uid = entity.uid
                            if uid:
                                global_data.player.credit_report(uid, param)
                else:
                    target_uid = self._selected_player_info.get('uid')
                    chat_content = self._extra_info_dict.get('chat', '')
                    chat_channel = self._extra_info_dict.get('channel', '')
                    global_data.player.report_someone_chat(from_way, target_uid, chat_content, chat_channel, report_reasons, content)
                self.close()
            return

    def on_click_player_list(self, btn, touch):
        self.panel.temp_list.setVisible(not self.panel.temp_list.isVisible())

    def on_report_send_ret(self, ret):
        if ret == log_const.REPORT_RESULT_OK:
            self.close()

    def on_report_times_change(self, type, times):
        if type != log_const.REPORT_PLAYER_TIMES:
            return
        if not self.panel or not self.panel.isValid():
            return
        if not self.panel.lab_remain:
            return
        self.panel.lab_remain.SetString(get_text_by_id(606034, (times, log_const.REPORT_PLAYER_DAY_LIMIT)))

    @staticmethod
    def get_player_battle_teammates():
        if global_data.player and global_data.player.logic:
            teammates_infos = global_data.player.logic.ev_g_teammate_infos()
            member_list = [ {'eid': member_id,'name': member_info.get('char_name', ''),'uid': member_info.get('uid', None)} for member_id, member_info in six.iteritems(teammates_infos) if member_id != global_data.player.id
                          ]
            return member_list
        else:
            return []

    @staticmethod
    def get_player_battle_killer--- This code section failed: ---

 429       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  POP_JUMP_IF_FALSE    75  'to 75'
           9  LOAD_GLOBAL           0  'global_data'
          12  LOAD_ATTR             1  'player'
          15  LOAD_ATTR             2  'logic'
        18_0  COME_FROM                '6'
          18  POP_JUMP_IF_FALSE    75  'to 75'

 430      21  LOAD_GLOBAL           0  'global_data'
          24  LOAD_ATTR             1  'player'
          27  LOAD_ATTR             2  'logic'
          30  LOAD_ATTR             3  'ev_g_killer_id_name'
          33  CALL_FUNCTION_0       0 
          36  UNPACK_SEQUENCE_2     2 
          39  STORE_FAST            0  'kid'
          42  STORE_FAST            1  'kname'

 431      45  LOAD_FAST             0  'kid'
          48  POP_JUMP_IF_FALSE    75  'to 75'
          51  LOAD_FAST             1  'kname'
        54_0  COME_FROM                '48'
          54  POP_JUMP_IF_FALSE    75  'to 75'

 432      57  BUILD_MAP_2           2 
          60  BUILD_MAP_1           1 
          63  STORE_MAP        
          64  LOAD_FAST             1  'kname'
          67  LOAD_CONST            2  'name'
          70  STORE_MAP        
          71  RETURN_END_IF    
        72_0  COME_FROM                '54'
          72  JUMP_FORWARD          0  'to 75'
        75_0  COME_FROM                '72'

 433      75  LOAD_CONST            0  ''
          78  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 63

    @staticmethod
    def get_possible_report_targets(enable_killer=True, enable_teammates=True):
        extra_list = []
        if enable_killer:
            killer_info = UserReportUI.get_player_battle_killer()
            if killer_info:
                extra_list.append(killer_info)
        if enable_teammates:
            extra_list.extend(UserReportUI.get_player_battle_teammates())
        return extra_list