# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/VideoShareWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six
import cc
from logic.gcommon.common_const import chat_const
from logic.comsys.video import video_record_utils as vru
from logic.comsys.archive.archive_manager import ArchiveManager

class VideoShareWidget(object):

    def __init__(self, in_lobby=True, *args, **kwargs):
        super(VideoShareWidget, self).__init__(*args, **kwargs)
        self._is_in_lobby = in_lobby
        self._share_ui = None
        self._share_content = None
        self._video_info = None
        self._in_game_btn_widget = None
        self._archive_data = ArchiveManager().get_archive_data(vru.SHARE_SETTING_NAME)
        self._btn_info = (
         (
          chat_const.CHAT_WORLD, 11004, self._on_click_share_in_game),
         (
          chat_const.CHAT_TEAM, 11005, self._on_click_share_in_game),
         (
          chat_const.CHAT_CLAN, 800001, self._on_click_share_in_game),
         (
          None, 10259, self._on_click_share_friend))
        return

    def show_video_share_ui(self, video_info):
        self._video_info = video_info
        from logic.comsys.share.ShareUI import ShareUI
        if self._share_ui:
            self._share_ui.close()
        self._share_ui = ShareUI()
        self._share_ui.set_pnl_share_picture_click_enable(True)
        self._share_ui.set_save_btn_visible(False)
        from logic.client.const import share_const
        self._share_ui.set_share_func(share_const.TYPE_VIDEO, self._on_click_platform_share)
        from logic.client.path_utils import SHARE_BG_FRAME
        self._share_ui.set_bg_layer_frame(SHARE_BG_FRAME)

        def on_click_in_game_btn(btn, touch):
            if self._in_game_btn_widget is None:
                from logic.comsys.share.ShareInGameWidget import ShareInGameWidget
                nd = global_data.uisystem.load_template_create('share/share_ingame_btn_list', parent=self._share_ui.panel)
                self._in_game_btn_widget = ShareInGameWidget(self, nd)
                self._in_game_btn_widget.init_btn_lst(self._btn_info)
                h = btn.getContentSize().height
                w_pos = btn.getParent().convertToWorldSpace(btn.getPosition())
                pos = nd.getParent().convertToNodeSpace(w_pos)
                nd.setPosition(cc.Vec2(pos.x, pos.y + h * 0.5))
            else:
                vis = self._in_game_btn_widget.is_visible()
                if vis:
                    self._in_game_btn_widget.hide()
                else:
                    self._in_game_btn_widget.show()
            return

        btn_info_lst = [
         {'template_name': 'share/share_ingame_btn',
            'click_cb': on_click_in_game_btn,
            'btn_name': 'btn_ingame',
            'btn_text': '',
            'lab_name': 'lab_ingame',
            'lab_text': 11004
            }]

        def cb(*args):
            if self._share_ui and self._share_ui.is_valid():
                self._share_ui.set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)

        from logic.comsys.share.HighLightShareCreator import HighLightShareCreator
        if self._share_content:
            self._share_content.destroy()
        self._share_content = HighLightShareCreator()
        video_path = video_info['path']
        self._share_content.create_panel(video_path, init_cb=cb)

    def _on_click_platform_share(self, platform):
        from logic.gutils.share_utils import check_video_share_support_local_file
        is_local_video = check_video_share_support_local_file(platform)
        video_name = self._video_info.get('name', '')
        video_key = self._video_info.get('key', '')
        if not video_name:
            video_name = vru.get_video_default_name(video_key, True)
        if is_local_video:
            video_path = self._video_info.get('path', '')
            if video_path:
                global_data.share_mgr.share_local_video(platform, video_path, title=video_name)
                vru.upload_share_suc_info_to_sa(video_key, str(platform))
            else:
                global_data.game_mgr.show_tip(get_text_by_id(2179))
        else:

            def cb(ret, record_names, msg, share_platform=platform):
                from logic.gcommon.const import FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_IMG, FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_VIDEO
                if not ret:
                    global_data.game_mgr.show_tip(get_text_by_id(2179))
                    return
                video_url = ''
                for url, up_type in six.iteritems(record_names):
                    if up_type == FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_VIDEO:
                        video_url = url

                if not video_url:
                    global_data.game_mgr.show_tip(get_text_by_id(2179))
                    return
                vru.upload_share_suc_info_to_sa(video_key, str(platform))
                global_data.share_mgr.share_video_url(share_platform, video_url, title=video_name, msg=str(msg))

            from logic.comsys.share.VideoShareConfirmUI import VideoShareConfirmUI
            ui = VideoShareConfirmUI()
            ui.init_video_info(self._video_info, cb)

    def _on_click_share_in_game(self, chat_channel):

        def channel_can_share(channel=chat_channel):
            if channel == chat_const.CHAT_TEAM:
                if not global_data or not global_data.player.get_team_info():
                    global_data.game_mgr.show_tip(get_text_by_id(11019))
                    return False
            elif channel == chat_const.CHAT_CLAN:
                if not global_data.player or not global_data.player.is_in_clan():
                    global_data.game_mgr.show_tip(get_text_by_id(800046))
                    return False
            return True

        def cb(ret, record_names, msg, channel=chat_channel):
            if not channel_can_share(channel):
                return
            extra_data = self._get_and_save_chat_data(ret, record_names, msg)
            if not extra_data:
                return
            self._share_ui.close()
            if self._is_in_lobby:
                from logic.comsys.video.video_record_utils import send_video_msg_to_world
                send_video_msg_to_world(channel, '', extra_data)
            else:
                from logic.comsys.video.VideoRecord import VideoRecord
                VideoRecord().add_chat_msg(channel, '', extra_data)
            global_data.game_mgr.show_tip(get_text_by_id(2177))

        if not channel_can_share():
            return
        from logic.comsys.share.VideoShareConfirmUI import VideoShareConfirmUI
        ui = VideoShareConfirmUI()
        ui.init_video_info(self._video_info, cb)

    def _on_click_share_friend(self, *args):
        self._in_game_btn_widget.hide()
        if self._share_ui:
            self._share_ui.on_click_friend_btn(self._on_click_friend)

    def _on_click_friend(self, f_data):

        def cb(ret, record_names, msg, friend_info=f_data):
            extra_data = self._get_and_save_chat_data(ret, record_names, msg, True)
            if global_data.is_inner_server:
                print('[VideoShareWidget] extra data:', extra_data)
                print('[VideoShareWidget] record_names:', record_names)
            if not extra_data:
                return
            self._share_ui.close()
            if self._is_in_lobby:
                from logic.comsys.video.video_record_utils import send_video_msg_to_friend
                send_video_msg_to_friend(f_data, '', extra_data)
            else:
                from logic.comsys.video.VideoRecord import VideoRecord
                VideoRecord().add_friend_msg(f_data, '', extra_data)
            global_data.game_mgr.show_tip(get_text_by_id(2177))

        from logic.comsys.share.VideoShareConfirmUI import VideoShareConfirmUI
        ui = VideoShareConfirmUI()
        ui.init_video_info(self._video_info, cb)

    def _get_and_save_chat_data(self, ret, upload_info, msg='', is_friend=False):
        if not ret:
            global_data.game_mgr.show_tip(get_text_by_id(2179))
            return
        else:
            from logic.gcommon.const import FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_IMG, FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_VIDEO
            video_url = ''
            cover_url = ''
            for url, up_type in six.iteritems(upload_info):
                if up_type == FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_VIDEO:
                    video_url = url
                elif up_type == FILE_SERVICE_UPLOAD_TYPE_HIGHLIGHT_IMG:
                    cover_url = url

            if not video_url or not cover_url:
                global_data.game_mgr.show_tip(get_text_by_id(2179))
                return
            video_md5 = self._video_info.get('md5_str', '')
            cover_info = self._video_info.get(vru.SMALL_COVER_KEY, None)
            if cover_info:
                cover_name, cover_path, cover_md5 = cover_info
            else:
                cover_name, cover_path, cover_md5 = ('', '', '')
            from logic.gcommon.time_utility import get_server_time
            self._archive_data[video_url] = {'local': True,'is_friend': is_friend,
               'md5_str': video_md5,
               'path': self._video_info.get('path', ''),
               'cover_info': (
                            cover_name, cover_path, cover_md5),
               'cover_url': str(cover_url),
               'time': get_server_time()
               }
            self._archive_data.save()
            data = {'type': chat_const.MSG_TYPE_VIDEO_SHARE,
               'video_url': video_url,
               'cover_url': cover_url,
               'video_md5': video_md5,
               'cover_md5': cover_md5,
               'msg': msg
               }
            return data

    def destroy(self):
        if self._in_game_btn_widget:
            self._in_game_btn_widget.destroy()
            self._in_game_btn_widget = None
        if self._share_ui and self._share_ui.is_valid():
            self._share_ui.close()
        self._share_ui = None
        if self._share_content:
            self._share_content.destroy()
        self._share_content = None
        return