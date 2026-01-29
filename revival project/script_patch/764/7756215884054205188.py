# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartVideoIntro.py
from __future__ import absolute_import
from . import ScenePart
import game3d
from common.cinematic.VideoPlayer import VideoPlayer
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.comsys.archive import archive_key_const
from logic.gutils.salog import SALog
from common.platform.device_info import DeviceInfo
import six.moves.builtins

class PartVideoIntro(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartVideoIntro, self).__init__(scene, name)

    def on_enter(self):
        self.scene().background_color = 0
        game3d.delay_exec(1, self.play_intro_video)

    def play_intro_video(self):
        SALog.get_instance().write(SALog.CG_PLAY_START)
        last_watch_date = ArchiveManager().get_general_archive_data_value(archive_key_const.KEY_LAST_WATCH_INTRO_DATE, '')
        cnt_watch_date = time_utility.get_date_str()
        is_huawei = DeviceInfo().is_huawei_device()
        if six.moves.builtins.__dict__.get('auto_login'):
            from patch import patch_announce
            patch_announce.destroy_patch_announce_instance()
            from logic.comsys.login.LoginHelper import LoginHelper
            if global_data.is_pc_mode:
                from logic.gutils.pc_utils import init_pc_ctrl_manager
                init_pc_ctrl_manager()
            VideoPlayer()
            data = six.moves.builtins.__dict__['auto_login']
            server_list_data, hostnum = data['server'], data['hostnum']
            if 'ui_event' in data:
                global_data.emgr.account_request_create_usr += data['ui_event']
            if 'avt_event' in data:
                global_data.emgr.on_login_success_event += data['avt_event']
            if 'lobby_event' in data:
                global_data.emgr.on_login_enter_lobby += data['lobby_event']
            if 'room_event' in six.moves.builtins.__dict__:
                global_data.emgr.on_login_enter_lobby += six.moves.builtins.__dict__['room_event']
            lh = LoginHelper()
            lh.server_list_data = server_list_data
            lh.parse_server_list_data(server_list_data)
            lh.server_list_state = lh.SERVER_LIST_STATE_INITTED
            lh.account_state = lh.SERVER_LIST_STATE_INITTED
            lh.connect_to_game_server(hostnum)
        elif not is_huawei and last_watch_date != cnt_watch_date:
            global_data.game_mgr.remove_patch_ui(remove_bg=False)
            VideoPlayer().play_video('video/intro_fight.mp4', self.play_intro_video, {}, force_ignore_volume_setting=True)
            ArchiveManager().save_general_archive_data_value(archive_key_const.KEY_LAST_WATCH_INTRO_DATE, cnt_watch_date)
        else:
            self.on_video_finish_cb()

    def on_video_finish_cb(self):
        main_scene = 'Main'
        SALog.get_instance().write(SALog.CG_PLAY_END)
        global_data.game_mgr.load_scene(main_scene, callback=global_data.game_mgr.on_load_main_scene)