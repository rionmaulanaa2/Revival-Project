# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/UnderageHelper.py
from __future__ import absolute_import
from logic.gcommon.common_const import ui_operation_const as uoc

def underage_comfirm_callback(callback):
    if global_data.player:
        old_content = global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY)
        if not bool(old_content):
            from logic.comsys.setting_ui.SettingPasswordUI import SettingPasswordUI
            ui = SettingPasswordUI(None, need_pwd=True, max_word=4, input_type=1)

            def confirm_cb(first_pwd):
                if len(first_pwd) != 4:
                    global_data.game_mgr.show_tip(get_text_by_id(635250))
                    return
                if not str(first_pwd).isdigit():
                    global_data.game_mgr.show_tip(get_text_by_id(635250))
                    return

                def real_confirm_cb(sec_pwd):
                    if str(first_pwd) == str(sec_pwd):
                        global_data.ui_mgr.close_ui('SettingPasswordUI')
                        callback(sec_pwd)
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(635256))
                        return

                _ui = global_data.ui_mgr.get_ui('SettingPasswordUI')
                if _ui:
                    content_dict_again = {'title': 635249,'desc': get_text_by_id(635252),'forget_text': '','confirm_cb': real_confirm_cb}
                    _ui.init_widget(**content_dict_again)

            content_dict = {'title': 635249,'desc': 635250,'forget_text': '','confirm_cb': confirm_cb
               }
            ui.init_widget(**content_dict)
        else:

            def compare_cb(to_check_pwd):
                if str(old_content) == to_check_pwd:
                    global_data.ui_mgr.close_ui('SettingPasswordUI')
                    callback('')
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(635256))
                    return

            def forgot_cb():
                if not global_data.player:
                    return
                else:
                    underage_close_timestamp = global_data.achi_mgr.get_cur_user_archive_data('UNDERAGE_MODE_CLOSE_TIMESTAMP', None) or 0
                    time_delta = underage_close_timestamp - global_data.game_time_server
                    if time_delta > 0:
                        mins = time_delta / 60.0
                        global_data.game_mgr.show_tip(get_text_by_id(635262, ['%d' % mins]))
                        return
                    global_data.game_mgr.show_tip(get_text_by_id(635257))
                    global_data.achi_mgr.set_cur_user_archive_data('UNDERAGE_MODE_CLOSE_TIMESTAMP', global_data.game_time_server + 600)
                    check_underage_mode()
                    global_data.ui_mgr.close_ui('SettingPasswordUI')
                    return

            from logic.comsys.setting_ui.SettingPasswordUI import SettingPasswordUI
            ui = SettingPasswordUI(None, need_pwd=True, max_word=4, input_type=1)
            content_dict = {'title': 635249,'desc': 635255,'forget_text': 635266,
               'confirm_cb': compare_cb,
               'forget_cb': forgot_cb}
            ui.init_widget(**content_dict)
    return


def check_underage_mode():
    if not global_data.player:
        return
    else:
        underage_close_timestamp = global_data.achi_mgr.get_cur_user_archive_data('UNDERAGE_MODE_CLOSE_TIMESTAMP', None) or 0
        if underage_close_timestamp:
            if underage_close_timestamp > global_data.game_time_server:
                time_delta = underage_close_timestamp - global_data.game_time_server
                global_data.game_mgr.delay_exec(time_delta, close_underage_mode)
            else:
                close_underage_mode()
        return


def close_underage_mode():
    if not global_data.player:
        return
    global_data.game_mgr.show_tip(get_text_by_id(635261))
    global_data.player and global_data.player.write_setting_2(uoc.TEAM_ONLY_FRIEND_KEY, False, True)
    global_data.player and global_data.player.write_setting_2(uoc.UNDERAGE_MODE_KEY, '', True)
    global_data.achi_mgr.set_cur_user_archive_data('UNDERAGE_MODE_CLOSE_TIMESTAMP', 0)
    global_data.emgr.update_underage_sub_setting.emit(uoc.UNDERAGE_MODE_KEY, '')
    global_data.emgr.player_underage_mode_changed_event.emit()


def is_in_underage_mode():
    from logic.gcommon.common_const import ui_operation_const as uoc
    content = global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY)
    if content:
        return True
    else:
        return False