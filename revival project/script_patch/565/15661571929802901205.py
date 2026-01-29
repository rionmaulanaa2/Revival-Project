# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/LoginFunctionUI.py
from __future__ import absolute_import
from __future__ import print_function
import C_file
import game3d
from common.uisys.basepanel import BasePanel
from common.platform.channel import Channel
from logic.gutils.salog import SALog
from logic.comsys.feedback import echoes
from logic.comsys.feedback.echoes import LOGIN
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from patch import revert
from logic.gutils.ConnectHelper import ConnectHelper
from common.cinematic.VideoPlayer import VideoPlayer
from common.platform.dctool import interface
from common.const import uiconst

class LoginFunctionUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'login/login_function'
    UI_ACTION_EVENT = {'btn_account.OnClick': 'on_click_account_btn',
       'btn_switch.OnClick': 'on_click_sw_account_btn',
       'btn_agreement.OnClick': 'on_click_agreement_btn',
       'btn_feedback.OnClick': 'on_click_feedback_btn',
       'btn_repair.OnClick': 'on_click_repair_btn',
       'btn_announce.OnClick': 'on_click_announce_btn',
       'btn_scan.OnClick': 'on_click_scan_btn',
       'btn_language.OnClick': 'on_click_lang_btn',
       'btn_play.OnClick': 'on_click_play_video',
       'btn_quit.OnClick': 'on_click_quit',
       'btn_retrieve.OnClick': 'on_click_findaccount_btn'
       }
    GLOBAL_EVENT = {'guest_login_state_changed': '_on_guest_login_state_updated'
       }
    FIND_ACCOUNT_TOKEN = '3d9650227e56184bab33c59b1e257ca2'
    FIND_ACCOUNT_URL_TEST = 'http://10.246.44.115:555/api/get_url/get_url'
    FIND_ACCOUNT_URL = 'https://qaaccount.netease.com:20001/api/get_url/get_url'

    def is_myapp(self):
        return global_data.channel.get_name() == 'myapp'

    def on_init_panel(self, **kwargs):
        self.playing_video = False
        self.use_normal_find_account_url = True
        self._is_account_btn_as_guest_btn = self._get_is_account_btn_as_guest_btn()
        self._init_function_btn_poses()
        self.init_event()
        salog_writer = SALog.get_instance()
        salog_writer.check_update_log()
        salog_writer.write(SALog.LOGINUI)
        self._refresh_account_btn_vis()
        self._refresh_account_btn_text()
        if global_data.channel.get_name() == 'netease':
            self.check_show_red_point()
        if game3d.get_platform() != game3d.PLATFORM_WIN32 and global_data.use_scan_pay:
            if interface.is_mainland_package():
                self.panel.btn_scan.setVisible(True)
        self.panel.btn_switch.setVisible(global_data.channel.has_standalone_sw_user() or self.is_myapp())
        self.panel.btn_language.setVisible(not interface.is_mainland_package())
        self.panel.btn_quit.setVisible(game3d.get_platform() == game3d.PLATFORM_WIN32)
        self.panel.btn_retrieve.setVisible(interface.is_mainland_package() and game3d.get_platform() != game3d.PLATFORM_WIN32)
        self._refresh_function_btns_pos()
        if interface.is_global_package() and game3d.get_platform() == game3d.PLATFORM_WIN32 and not interface.is_steam_channel():
            ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
            if ui:
                ui.request_platform_announce()
        if interface.is_global_package() and global_data.channel.get_app_channel() == 'oppo_sea':
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            from logic.gutils import jump_to_ui_utils
            cb = lambda : jump_to_ui_utils.jump_to_website('https://go.onelink.me/HThl/d65e665b')
            SecondConfirmDlg2().confirm(content=get_text_by_id(609747), confirm_callback=cb)

    def _init_function_btn_poses(self):
        self._btn_poses = []
        for child in self.panel.function.GetChildren():
            self._btn_poses.append(child.GetPosition())

    def _restore_function_btn_position(self):
        for child in self.panel.function.GetChildren():
            child.ReConfPosition()

    def _refresh_function_btns_pos(self):
        pos_i = 0
        for child in self.panel.function.GetChildren():
            if child.isVisible():
                child.SetPosition(*self._btn_poses[pos_i])
                pos_i += 1

    def check_show_red_point(self):
        sdk_uid = global_data.channel.get_sdk_uid()
        if not sdk_uid:
            return
        self.set_red_point(flag=False)
        if global_data.channel.get_name() == 'netease':
            if global_data.achi_mgr.is_show_netease_daren_red_point(sdk_uid):
                self.set_red_point(flag=True)

    def set_red_point(self, flag=True):
        self.panel.function.btn_account.img_red_point.setVisible(flag)

    def on_channel_login(self):
        pass

    def on_channel_logout(self):
        pass

    def init_event(self):
        pass

    def _get_is_account_btn_as_guest_btn(self):
        channel_name = global_data.channel.get_app_channel()
        return channel_name == 'huawei'

    def _refresh_account_btn_vis(self):
        if self._is_account_btn_as_guest_btn:
            vis = not global_data.channel.is_guest_blocked()
        else:
            vis = global_data.channel.has_builtin_user_center()
        self.panel.btn_account.setVisible(vis)
        self._refresh_function_btns_pos()

    def _refresh_account_btn_text(self, is_guest=None):
        if self._is_account_btn_as_guest_btn:
            if is_guest is None:
                is_guest = global_data.channel.is_guest()
            if is_guest:
                ac_btn_text = 82054
            else:
                ac_btn_text = 82050
        else:
            ac_btn_text = 80457
        self.panel.btn_account.text.SetString(ac_btn_text)
        return

    def on_click_account_btn(self, *args):
        if self._is_account_btn_as_guest_btn:
            if global_data.channel.is_guest():
                global_data.channel.logout()
            else:
                global_data.channel.guest_login()
        elif global_data.channel.get_app_channel() == 'netease_global' and global_data.deviceinfo.get_os_name() == 'windows' and not global_data.channel.is_free_login and not global_data.channel.is_sdk_login:
            from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
            trigger_ui_btn_event('MainLoginUI', 'btn_login', need_check_vis=False)
            return
        Channel().open_manager()
        self.set_red_point(flag=False)
        if global_data.channel.get_name() == 'netease':
            sdk_uid = global_data.channel.get_sdk_uid()
            if sdk_uid:
                global_data.achi_mgr.save_netease_daren_red_point(sdk_uid, 0)

    def on_click_sw_account_btn(self, *args):
        if self.is_myapp():
            global_data.channel.logout()
            global_data.game_mgr.show_tip(get_text_by_id(860394))
        else:
            global_data.channel.switch_account()

    def on_click_agreement_btn(self, *args):
        Channel().show_compact_view()

    def on_click_feedback_btn(self, *args):
        echoes.show_feedback_view(LOGIN)

    def on_click_repair_btn(self, *args):
        if ConnectHelper().is_connected() or ConnectHelper().is_connecting():
            return

        def clear_patch():
            import package_utils
            package_utils.reset_package_info()
            global_data.game_mgr.try_restart_app()

        SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(19050), confirm_callback=clear_patch)

    def on_click_announce_btn(self, *args):
        import version
        cnt_version = int(version.get_script_version())
        if cnt_version == 0:
            self.test_ui()
        else:
            ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
            if ui:
                ui.request_platform_announce()

    def on_click_scan_btn(self, *args):
        from logic.gutils.share_utils import huawei_permission_confirm
        permission = 'android.permission.CAMERA'
        huawei_permission_confirm(permission, 635574, self.do_btn_scan)

    def do_btn_scan(self, *args):

        def callback(*args):
            pass

        global_data.channel.present_qrcode_scanner('', 0, callback)

    def on_click_lang_btn(self, *args):
        if revert.REVERTING:
            return
        from logic.comsys.setting_ui.LanguageSettingUI import LanguageSettingUI
        LanguageSettingUI()

    def on_video_over_callback(self, *args):
        self.playing_video = False
        is_huawei = global_data.deviceinfo.is_huawei_device()
        if not is_huawei:
            from logic.gutils.video_utils import get_login_video_name
            video_name = get_login_video_name()
            VideoPlayer().play_video(video_name, None, {}, 0, None, True, disable_sound_mgr=False, force_ignore_volume_setting=True)
        return

    def on_click_play_video(self, *args):
        if self.playing_video:
            return
        self.playing_video = True
        VideoPlayer().stop_video()
        VideoPlayer().play_video('video/intro_fight.mp4', self.on_video_over_callback, {}, force_ignore_volume_setting=True)

    def on_click_quit(self, *args):
        from logic.manager_agents.EscapeManagerAgent import EscapeManagerAgent
        EscapeManagerAgent.show_exit_game_confirm_dialog()

    def on_click_findaccount_btn(self, *args):
        import json
        import common.http
        channel_name = global_data.channel.get_app_channel()
        child_channel = game3d.get_app_name()
        data_value = '{"token":"%s","udid":"%s"}' % (self.FIND_ACCOUNT_TOKEN, global_data.channel.get_udid())
        _fields = {'data': data_value
           }

        def _callback(ret, *args):
            try:
                ret = json.loads(ret)
                url = ret.get('url')
                url = '{}&channel={}&child_channel={}'.format(url, channel_name, child_channel)
                game3d.open_url(url)
            except Exception as e:
                log_error('on_click_findaccount fail ret %s, error %s', ret, str(e))

        find_account_url = self.FIND_ACCOUNT_URL if self.use_normal_find_account_url else self.FIND_ACCOUNT_URL_TEST
        common.http.request(find_account_url, callback=_callback, fields=_fields)

    def _on_guest_login_state_updated(self, is_guest):
        if not self._is_account_btn_as_guest_btn:
            return
        self._refresh_account_btn_text(is_guest)

    def on_resolution_changed(self):
        self._restore_function_btn_position()
        self._init_function_btn_poses()
        self._refresh_function_btns_pos()

    def test_ui--- This code section failed: ---

 304       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'cocosui'
           9  STORE_FAST            1  'cocosui'

 305      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'gc'
          21  STORE_FAST            2  'gc'

 306      24  LOAD_FAST             2  'gc'
          27  LOAD_ATTR             2  'collect'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

 307      34  LOAD_GLOBAL           3  'print'
          37  LOAD_CONST            2  'enable_ui_add_image_async'
          40  LOAD_GLOBAL           4  'global_data'
          43  LOAD_ATTR             5  'enable_ui_add_image_async'
          46  CALL_FUNCTION_2       2 
          49  POP_TOP          

 308      50  LOAD_GLOBAL           3  'print'
          53  LOAD_CONST            3  'is_support csb'
          56  LOAD_GLOBAL           4  'global_data'
          59  LOAD_ATTR             6  'feature_mgr'
          62  LOAD_ATTR             7  'is_support_cocos_csb'
          65  CALL_FUNCTION_0       0 
          68  CALL_FUNCTION_2       2 
          71  POP_TOP          

 313      72  LOAD_CONST            1  ''
          75  LOAD_CONST            0  ''
          78  IMPORT_NAME           8  'time'
          81  STORE_FAST            3  'time'

 314      84  LOAD_CONST            1  ''
          87  LOAD_CONST            4  ('TOP_ZORDER', 'UI_VKB_NO_EFFECT')
          90  IMPORT_NAME           9  'common.const.uiconst'
          93  IMPORT_FROM          10  'TOP_ZORDER'
          96  STORE_FAST            4  'TOP_ZORDER'
          99  IMPORT_FROM          11  'UI_VKB_NO_EFFECT'
         102  STORE_FAST            5  'UI_VKB_NO_EFFECT'
         105  POP_TOP          

 315     106  LOAD_CONST            1  ''
         109  LOAD_CONST            0  ''
         112  IMPORT_NAME          12  'cc'
         115  STORE_FAST            6  'cc'

 317     118  LOAD_GLOBAL           3  'print'
         121  LOAD_CONST            5  'before test ui'
         124  LOAD_FAST             6  'cc'
         127  LOAD_ATTR            13  'Director'
         130  LOAD_ATTR            14  'getInstance'
         133  CALL_FUNCTION_0       0 
         136  LOAD_ATTR            15  'getTextureCache'
         139  CALL_FUNCTION_0       0 
         142  LOAD_ATTR            16  'getCachedTextureInfo'
         145  CALL_FUNCTION_0       0 
         148  CALL_FUNCTION_2       2 
         151  POP_TOP          

 318     152  LOAD_GLOBAL          17  'hasattr'
         155  LOAD_GLOBAL           6  'feature_mgr'
         158  CALL_FUNCTION_2       2 
         161  POP_JUMP_IF_TRUE    176  'to 176'

 319     164  BUILD_LIST_0          0 
         167  LOAD_FAST             0  'self'
         170  STORE_ATTR           18  '_ui_list'
         173  JUMP_FORWARD          0  'to 176'
       176_0  COME_FROM                '173'

 320     176  LOAD_FAST             3  'time'
         179  LOAD_ATTR             8  'time'
         182  CALL_FUNCTION_0       0 
         185  STORE_FAST            7  'start_t'

 321     188  LOAD_FAST             0  'self'
         191  LOAD_ATTR            18  '_ui_list'
         194  POP_JUMP_IF_FALSE   239  'to 239'

 322     197  SETUP_LOOP           27  'to 227'
         200  LOAD_FAST             0  'self'
         203  LOAD_ATTR            18  '_ui_list'
         206  GET_ITER         
         207  FOR_ITER             16  'to 226'
         210  STORE_FAST            8  'ui'

 323     213  LOAD_FAST             8  'ui'
         216  LOAD_ATTR            19  'close'
         219  CALL_FUNCTION_0       0 
         222  POP_TOP          
         223  JUMP_BACK           207  'to 207'
         226  POP_BLOCK        
       227_0  COME_FROM                '197'

 324     227  BUILD_LIST_0          0 
         230  LOAD_FAST             0  'self'
         233  STORE_ATTR           18  '_ui_list'
         236  JUMP_FORWARD          0  'to 239'
       239_0  COME_FROM                '236'

 326     239  LOAD_CONST            7  'lobby/lobby_new'
         242  LOAD_CONST            8  'chat/main_chat'
         245  LOAD_CONST            9  'common/speaker_tips'
         248  LOAD_CONST           10  'common/screen_touch_effect'

 327     251  LOAD_CONST           11  'mall/i_item_describe'
         254  LOAD_CONST           12  'role_profile/i_role_gift_obtain'
         257  LOAD_CONST           13  'common/i_common_describe'

 328     260  LOAD_CONST           14  'task/i_reward_preview'
         263  LOAD_CONST           15  'battle_pass/get_award'
         266  LOAD_CONST           16  'common/lottery_get_tips'

 329     269  LOAD_CONST           17  'mall/get_model_display'
         272  LOAD_CONST           18  'mall/get_model_display_before'
         275  LOAD_CONST           19  'common/get_item/get_weapon_fg'
         278  LOAD_CONST           20  'common/network_loading'

 330     281  LOAD_CONST           21  'room/room_main_new'
         284  BUILD_LIST_15        15 
         287  STORE_FAST            9  'template_paths'

 337     290  SETUP_LOOP           35  'to 328'
         293  LOAD_FAST             9  'template_paths'
         296  GET_ITER         
         297  FOR_ITER             27  'to 327'
         300  STORE_FAST           10  'tmp_path'

 338     303  LOAD_GLOBAL           4  'global_data'
         306  LOAD_ATTR            20  'ui_mgr'
         309  LOAD_ATTR            21  'create_simple_dialog'
         312  LOAD_FAST            10  'tmp_path'
         315  LOAD_FAST             4  'TOP_ZORDER'
         318  CALL_FUNCTION_2       2 
         321  STORE_FAST            8  'ui'
         324  JUMP_BACK           297  'to 297'
         327  POP_BLOCK        
       328_0  COME_FROM                '290'

 348     328  LOAD_GLOBAL           3  'print'
         331  LOAD_CONST           22  'USED time '
         334  LOAD_FAST             3  'time'
         337  LOAD_ATTR             8  'time'
         340  CALL_FUNCTION_0       0 
         343  LOAD_FAST             7  'start_t'
         346  BINARY_SUBTRACT  
         347  CALL_FUNCTION_2       2 
         350  POP_TOP          

 349     351  LOAD_GLOBAL           3  'print'
         354  LOAD_CONST           23  'after test ui'
         357  LOAD_FAST             6  'cc'
         360  LOAD_ATTR            13  'Director'
         363  LOAD_ATTR            14  'getInstance'
         366  CALL_FUNCTION_0       0 
         369  LOAD_ATTR            15  'getTextureCache'
         372  CALL_FUNCTION_0       0 
         375  LOAD_ATTR            16  'getCachedTextureInfo'
         378  CALL_FUNCTION_0       0 
         381  CALL_FUNCTION_2       2 
         384  POP_TOP          

 350     385  LOAD_FAST             2  'gc'
         388  LOAD_ATTR             2  'collect'
         391  CALL_FUNCTION_0       0 
         394  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 158