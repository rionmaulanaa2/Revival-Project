# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLogin3D.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from . import ScenePart
from common.platform.channel import Channel
from logic.comsys.login.LoginHelper import LoginHelper
from common.crashhunter.crashhunter_utils import update_dump_user_info
from logic.comsys.login.MainLoginUI import MainLoginUI
from logic.comsys.login.LoginFunctionUI import LoginFunctionUI
from common.platform.dctool import interface
from logic.comsys.setting_ui.LanguageSettingUI import LanguageSettingUI
from common.framework import Functor
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_const import lang_data
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.common_const.lang_data import LANG_EN
import six.moves.builtins
import game3d
from common.platform.device_info import DeviceInfo

class PartLogin3D(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartLogin3D, self).__init__(scene, name)
        self.signal_count = 1
        self.cnt_signal = 0
        self.bg_music = None
        from logic.vscene import scene_type
        global_data.scene_type = scene_type.SCENE_TYPE_LOGIN
        self.should_hide_main_ui_btn = False
        self._is_need_login_channel = False
        self._is_anim_part1_finished = False
        self._is_exited = False
        self.is_huawei = DeviceInfo().is_huawei_device()
        if global_data.message_data:
            global_data.message_data.reset()
        self.anim_prepare()
        if global_data.is_pc_mode:
            from logic.gutils.pc_utils import init_pc_ctrl_manager
            init_pc_ctrl_manager()
        return

    def reset_login_env(self):
        LoginHelper.finalize()
        update_dump_user_info()

    def on_pre_load(self):
        video_player_instance = global_data.singleton_map.get('VideoPlayer', None)
        if video_player_instance:
            video_player_instance.force_stop_video()
        self.reset_login_env()
        self.init_event()
        self.scene().enable_hdr(True)
        self.scene().set_adapt_factor(0.72)
        self.init_login_env()
        if self.is_huawei:
            global_data.game_mgr.next_exec(self.play_cam_anim)
        return

    def init_login_env(self):
        LoginHelper().get_server_list()
        self.show_oversea_init_setting()
        archive_data = global_data.achi_mgr.get_general_archive_data()
        is_logined_before = archive_data.get_field('sdk_logined', False)
        if is_logined_before and (not global_data.channel.is_pc_netease() or global_data.channel.get_prop_str('JUDGE_PACKAGE') == '1'):
            self.login_channel()
        self.on_enter_login_stage()

    def init_event(self):
        global_data.emgr.request_sdk_login += self.login_channel
        global_data.emgr.on_server_list_refresh_event += self.on_server_list_refreshed
        global_data.emgr.account_request_create_usr += self.on_request_create_usr
        global_data.emgr.should_login_channel_event += self.should_login_channel
        global_data.emgr.app_resume_event += self._load_pipeline

    def unregist_event(self):
        global_data.emgr.request_sdk_login -= self.login_channel
        global_data.emgr.on_server_list_refresh_event -= self.on_server_list_refreshed
        global_data.emgr.account_request_create_usr -= self.on_request_create_usr
        global_data.emgr.should_login_channel_event -= self.should_login_channel
        global_data.emgr.app_resume_event -= self._load_pipeline

    def should_login_channel(self):
        if self._is_need_login_channel:
            self.login_channel()

    def on_request_create_usr(self):
        self.del_login_uis()
        global_data.ui_mgr.close_ui('LoginAnimationUI')

    def on_server_list_refreshed(self, *args):
        print('server list refreshed')
        channel_inst = Channel()
        if not channel_inst.is_valid or channel_inst.is_free_login or channel_inst.is_sdk_login:
            LoginHelper().get_account_data()

    def login_channel(self):
        channel_inst = Channel()
        if channel_inst.is_valid:
            channel_inst.regist_event(channel_inst.LOGIN_OK_EVENT, self.on_sdk_logined_cb)
            channel_inst.login()
            self.should_hide_main_ui_btn = True
        else:
            self.on_sdk_logined_cb()

    def on_sdk_logout_cb(self):
        helper = LoginHelper()
        helper.refresh_match_server_list()
        helper.reset_account_data()
        update_dump_user_info()
        channel_inst = Channel()
        if channel_inst.is_valid:
            channel_inst.unregist_event(channel_inst.LOGIN_OK_EVENT, self.on_sdk_logined_cb)
            channel_inst.regist_event(channel_inst.LOGIN_OK_EVENT, self.on_sdk_logined_cb)

    def on_sdk_logined_cb(self):
        channel_inst = Channel()
        channel_inst.regist_event(channel_inst.LOGOUT_EVENT, self.on_sdk_logout_cb)
        update_dump_user_info()
        helper = LoginHelper()
        helper.refresh_match_server_list()
        if helper.server_list_state == helper.SERVER_LIST_STATE_INITTED and helper.account_state == helper.SERVER_LIST_STATE_UNINITED:
            helper.get_account_data()
        announcement_ver = -1
        announcement_ver_data = ArchiveManager().get_archive_data('announcement_version')
        server_version_ver = LoginHelper().get_real_server_version(True, True)
        if announcement_ver_data:
            announcement_ver = announcement_ver_data.get_field('announcement_version', -1)
        new_package = six.moves.builtins.__dict__.get('NEW_PACKAGE_FLAG', False)
        if announcement_ver != server_version_ver and not new_package:
            if announcement_ver != -1:
                ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
                if ui:
                    ui.request_platform_announce()
            announcement_ver_data['announcement_version'] = server_version_ver
            announcement_ver_data.save(encrypt=True)

    def show_invisible_ui(self):
        from logic.comsys.common_ui.BlankTouchUI import BlankTouchUI
        ui = BlankTouchUI()
        ui.set_touch_callback(self.stop_anim)

    def show_login_ui(self):
        if global_data.channel.is_pc_netease() and not global_data.channel.get_prop_str('JUDGE_PACKAGE') == '1':

            def ok_func():
                game3d.exit()

            second_confirm_ui = SecondConfirmDlg2()
            second_confirm_ui.confirm(content=get_text_by_id(279), confirm_callback=ok_func, click_blank_close=False, cancel_auto_close=False, confirm_auto_close=False)
            second_confirm_ui.panel.temp_second_confirm.temp_btn_1.setVisible(False)
        self.check_show_need_update()
        MainLoginUI()
        LoginFunctionUI()
        self.play_cg_bg()
        self.init_push_service()

    def play_cg_bg(self):
        print('[login3d] play cg bg')

        def video_ready(*args):
            print('[login3d] remove patch ui')
            game3d.delay_exec(2, lambda : global_data.game_mgr.remove_patch_ui())

        if not self.is_huawei:
            from common.cinematic.VideoPlayer import VideoPlayer
            from logic.gutils.video_utils import get_login_video_name
            video_name = get_login_video_name()
            VideoPlayer().play_video(video_name, video_ready, {}, 0, None, True, disable_sound_mgr=False, video_ready_cb=video_ready, force_ignore_volume_setting=True)
        else:
            video_ready()
        game3d.delay_exec(6000, lambda : global_data.game_mgr.remove_patch_ui())
        return

    def show_init_language_setting_ui(self):
        ui = LanguageSettingUI()
        ui.hide_close_btn()

    def show_oversea_init_setting(self):
        if not interface.is_mainland_package():
            if global_data.ui_mgr.read_lang_conf_from_setting(False) is None:
                self.check_default_language()
                return True
        return False

    def check_default_language(self):
        local_language_code = global_data.ui_mgr.get_local_language_code(True)
        if local_language_code is None:
            local_language_code = LANG_EN
        local_lang_data = lang_data.lang_data.get(local_language_code, {})
        lang_enable = local_lang_data.get('cLangEnable', 0) == 1
        if local_language_code is not None and lang_enable:
            global_data.ui_mgr.change_lang(local_language_code)
            context = get_text_by_id(80837, {'lang': lang_data.code_2_showname[local_language_code]})
            global_data.game_mgr.show_tip(context)
        return

    def check_oversea_country(self):
        pass

    def show_svr_list(self):
        from logic.comsys.login.SvrSelectUI import SvrSelectUI
        SvrSelectUI()

    def on_enter(self):
        try:
            print('[login3d] on enter')
            self._is_exited = False
            import game3d
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                import os
                _path = os.path.join(game3d.get_doc_dir(), 'launcher_count_flag')
                if not os.path.exists(_path):
                    f = open(_path, 'w+')
                    f.write('1')
                    f.close()
        except:
            pass

        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def on_exit(self):
        channel_inst = Channel()
        channel_inst.unregist_event(channel_inst.LOGIN_OK_EVENT, self.on_sdk_logined_cb)
        channel_inst.unregist_event(channel_inst.LOGOUT_EVENT, self.on_sdk_logout_cb)
        self.del_login_uis()
        self.unregist_event()
        from logic.comsys.login.LoginHelper import LoginHelper
        LoginHelper().finalize()
        self.anim_exit()
        self._is_exited = True
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(False)

    def del_login_uis(self):
        global_data.ui_mgr.close_ui('MainLoginUI')
        global_data.ui_mgr.close_ui('SvrSelectUI')
        global_data.ui_mgr.close_ui('LoginFunctionUI')
        global_data.ui_mgr.close_ui('AnnouncementUI')
        global_data.ui_mgr.close_ui('CharacterCreatorUINew')
        global_data.ui_mgr.close_ui('LoginAnimationUI')
        from logic.comsys.common_ui.BlankTouchUI import BlankTouchUI
        ui = BlankTouchUI()
        ui.set_touch_callback(None)
        global_data.ui_mgr.close_ui('BlankTouchUI')
        from common.cinematic.VideoPlayer import VideoPlayer
        VideoPlayer().force_stop_video()
        return

    def on_enter_login_stage(self):
        self.show_login_ui()
        if self.should_hide_main_ui_btn:
            self.should_hide_main_ui_btn = False
            global_data.emgr.hide_main_login_btn_event.emit(False)

    def create_track_spline(self):
        import world
        track = world.track(world.TRACK_TYPE_SPLINE)
        return track

    def play_cam_anim(self):
        import math3d
        import world
        scn = world.get_active_scene()
        for m in scn.get_models():
            m.enable_instancing(False)
            for i in range(m.get_socket_count()):
                for bind_obj in m.get_socket_objects(i):
                    if isinstance(bind_obj, world.sfx):
                        bind_obj.render_bias = m.render_level - 1

        import common.cfg.confmgr as confmgr
        login_anim_conf = confmgr.get('login_anim_config', 'enter')
        trk = self.create_track_spline()
        trk.duration = login_anim_conf['duration']
        trk.spline_type = login_anim_conf['spline']
        points = login_anim_conf['points']
        distance = []
        total_d = 0.001
        for i, point in enumerate(points):
            trans = self.scene().get_preset_camera(point)
            if distance:
                distance.append((las_pos - trans.translation).length)
            else:
                distance.append(0)
            las_pos = trans.translation
            total_d += distance[-1]

        current_d = 0
        for i, point in enumerate(points):
            trans = self.scene().get_preset_camera(point)
            current_d += distance[i]
            current_time = int(current_d * 1.0 / total_d * trk.duration)
            trk.set_key_transform(trk.add_key(current_time), trans)

        self._is_anim_part1_finished = False

        def callback():
            self._is_anim_part1_finished = True
            self.play_cam_anim_part2()
            self.init_push_service()

        self.scene().get_com('PartLoginTrkCamera').play_track(trk, callback, time_scale=1.0, mode=login_anim_conf['easing'], mode_arg=login_anim_conf['easing_curve'], fix_forward=math3d.vector(0, 0, 1), fix_up=math3d.vector(0, 1, 0))

    def play_cam_anim_part2(self):
        import math3d
        import common.cfg.confmgr as confmgr
        login_anim_conf = confmgr.get('login_anim_config', 'idle')
        trk = self.create_track_spline()
        trk.duration = login_anim_conf['duration']
        trk.spline_type = login_anim_conf['spline']
        points = login_anim_conf['points']
        distance = []
        total_d = 0.001
        for i, point in enumerate(points):
            trans = self.scene().get_preset_camera(point)
            if distance:
                distance.append((las_pos - trans.translation).length)
            else:
                distance.append(0)
            las_pos = trans.translation
            total_d += distance[-1]

        current_d = 0
        for i, point in enumerate(points):
            trans = self.scene().get_preset_camera(point)
            current_d += distance[i]
            current_time = int(current_d * 1.0 / total_d * trk.duration)
            trk.set_key_transform(trk.add_key(current_time), trans)

        self.scene().get_com('PartLoginTrkCamera').play_track(trk, None, time_scale=1.0, mode=login_anim_conf['easing'], mode_arg=login_anim_conf['easing_curve'], fix_forward=math3d.vector(0, 0, 1), fix_up=math3d.vector(0, 1, 0))
        return

    def anim_prepare(self):
        self._load_pipeline()

    def anim_exit(self):
        pass

    def _load_pipeline(self):
        if self.scene() is None:
            return
        else:
            global_data.display_agent.set_pipeline('common/pipeline/pipeline_login.xml')
            self.scene().enable_hdr(True)
            self.scene().set_adapt_factor(0.72)
            return

    def stop_anim(self, *args):
        if not self._is_anim_part1_finished:
            self.scene().get_com('PartLoginTrkCamera').cancel_track()
            self._is_anim_part1_finished = True
            self.init_login_env()
            self.play_cam_anim_part2()
            self.init_push_service()

    def init_push_service(self):
        from common.platform import is_android, is_ios
        archive_data = global_data.achi_mgr.get_general_archive_data()
        archive_key = 'has_check_read_phone_state_permission'
        has_check = archive_data.get_field(archive_key, False)

        def on_check_read_phone_state_cb(*args):
            from logic.comsys import push
            push.init_push()

        from common.platform.dctool.interface import is_mainland_package
        os_ver_need_show_permission = global_data.channel and global_data.channel.get_os_ver() >= '14.5'
        if is_ios() and os_ver_need_show_permission and not is_mainland_package():
            data = {'methodId': 'fetchIDFAPermission'}
            global_data.channel.extend_func_by_dict(data)
        ignore_phone_state = global_data.channel.get_name() in ('huawei', ) or global_data.is_android_pc
        support_check = hasattr(game3d, 'check_client_permission') and hasattr(game3d, 'check_client_should_request_permission')
        if is_android() and not ignore_phone_state and not has_check and support_check:
            archive_data.set_field(archive_key, True)
            permission = 'android.permission.READ_PHONE_STATE'
            if game3d.check_client_permission(permission, False):
                on_check_read_phone_state_cb()
            else:

                def confirm():
                    game3d.check_client_permission(permission, True)

                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                SecondConfirmDlg2().confirm(content=get_text_by_id(246), confirm_callback=confirm)
        else:
            on_check_read_phone_state_cb()

    def check_show_need_update(self):
        from common.platform.dctool.interface import is_mainland_package
        if is_mainland_package():
            return
        import world
        from logic.gutils.version_utils import get_integer_engine_version
        engine_ver = get_integer_engine_version()
        if engine_ver != 0 and engine_ver < 1189617:

            def goto_download(*args):
                from logic.gutils.activity_utils import goto_package_store
                goto_package_store()
                game3d.exit()

            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            NormalConfirmUI2(content=get_text_by_id(609930), on_confirm=goto_download)