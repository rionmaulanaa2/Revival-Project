# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareManager.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import os
import shutil
import game
import game3d
import render
from common.cfg import confmgr
from common.framework import Singleton
from common.platform.dctool import interface
from logic.client.const import share_const
from logic.comsys.share.ShareScreenCaptureUI import ShareScreenCaptureUI
from logic.gcommon.common_utils.local_text import get_text_by_id
import json
import random
from logic.gutils import share_utils
import cc
SHARE_THUMB_ICON_NA = 'gui/ui_res_2/game_cover/img_cover.png'
SHARE_THUMB_ICON = 'gui/ui_res_2/game_cover/img_cover_new.png'
COPY_SHARE_THUMB_ICON_NA = 'gui/ui_res_2/game_cover/copy_img_cover.jpg'
COPY_SHARE_THUMB_ICON = 'gui/ui_res_2/game_cover/copy_img_cover_new.jpg'
SHARE_TEMP_DIR = 'share_temp'

class ShareManager(Singleton):
    ALIAS_NAME = 'share_mgr'

    def init(self):
        self._custom_share_cb = None
        self._share_inform_cb = None
        self._share_inform_text = None
        self._is_saving_file = False
        self._last_share_channel = None
        self._last_message_id = None
        self._save_to_gallery_callback = None
        self.init_platform_list()
        self.init_share_save_path()
        self._has_shared = False
        self.process_event(True)
        return

    def on_finalize(self):
        self.process_event(False)
        self.clear_temp_share_file()
        from logic.comsys.video import video_record_utils as vru
        vru.clear_and_make_path([self.share_temp_dir])

    def init_share_save_path(self):
        from common.utils.path import get_neox_dir, get_share_img_weibo_dir, get_share_img_na_dir
        from patch.patch_path import get_download_target_path
        if not global_data.feature_mgr.is_fix_rt_savefile_png_alpha():
            file_name = 'share.jpg'
        else:
            file_name = 'share.png'
        weibo_dir = get_share_img_weibo_dir()
        if weibo_dir:
            self.SHARE_WEIBO_DIR = weibo_dir
            self.SHARE_WEIBO_FILE_PATH = weibo_dir + file_name
            self.check_dir(self.SHARE_WEIBO_FILE_PATH)
        else:
            self.SHARE_WEIBO_DIR = None
            self.SHARE_WEIBO_FILE_PATH = None
        self.SHARE_SAVE_FILE_NAME = file_name
        self.SHARE_SAVE_PATH = get_neox_dir() + '/res/' + file_name
        self.SHARE_SAVE_ENCRYPTED_PATH = get_neox_dir() + '/' + get_download_target_path('res/' + file_name)
        self.SHARE_SAVE_DIR_NA = get_share_img_na_dir()
        self.check_dir(self.SHARE_SAVE_ENCRYPTED_PATH)
        self.check_dir(self.SHARE_SAVE_PATH)
        from logic.comsys.video import video_record_utils as vru
        self.share_temp_dir = os.path.join(game3d.get_doc_dir(), SHARE_TEMP_DIR)
        vru.clear_and_make_path([self.share_temp_dir])
        self.SHARE_RELATIVE_PATH = file_name
        self.share_temp_files = set()
        return

    def check_dir(self, file_path):
        index = file_path.rfind('/')
        dirs = file_path[0:index]
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def init_platform_list(self):
        self.share_apps_dict = share_const.init_platform_list()

    def share_callback(self, pf, res, err):
        if res == 2:
            pass
        if self._custom_share_cb is not None:
            self._custom_share_cb(pf, res, err)
            self._custom_share_cb = None
            return
        else:
            if res == 0:
                global_data.game_mgr.show_tip(get_text_by_id(2177))
            elif res == 1:
                global_data.game_mgr.show_tip(get_text_by_id(2178))
            else:
                global_data.game_mgr.show_tip(get_text_by_id(2179))
            return

    def process_event(self, is_bind):
        event_mgr = global_data.emgr
        e_event = {'app_resume_event': self.on_app_resume
           }
        if is_bind:
            event_mgr.bind_events(e_event)
        else:
            event_mgr.unbind_events(e_event)

    def get_support_platforms_without_channel(self):
        return self.get_support_platform(channel_related=False)

    def get_support_platform_enums_without_channel(self):
        return self.get_support_platform_enum(channel_related=False)

    def get_support_platform(self, share_type='', channel_related=True):
        if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_google_pc:
            platform_list = []
            return platform_list
        else:
            platform_enums = self.get_support_platform_enum(share_type, channel_related)
            return self.get_support_platforms_from_enum(platform_enums)

    def get_support_platform_enum(self, share_type='', channel_related=True):
        if interface.is_mainland_package():
            cur_support_share_platform_list = [share_const.APP_SHARE_WEIXIN,
             share_const.APP_SHARE_WEIXIN_MOMENT,
             share_const.APP_SHARE_MOBILE_QQ,
             share_const.APP_SHARE_MOBILE_QZONE,
             share_const.APP_SHARE_DOUYIN,
             share_const.APP_SHARE_KUAISHOU,
             share_const.APP_SHARE_GODLIKE]
            cur_support_share_platform_list.append(share_const.APP_SHARE_WEIBO)
        else:
            cur_support_share_platform_list = [share_const.APP_SHARE_FACEBOOK,
             share_const.APP_SHARE_TWITTER]
            if not (share_type != share_const.TYPE_LINK and game3d.get_platform() == game3d.PLATFORM_IOS):
                cur_support_share_platform_list.append(share_const.APP_SHARE_MESSENGER)
            if global_data.feature_mgr.is_share_line_simple_ready():
                cur_support_share_platform_list.append(share_const.APP_SHARE_LINE)
            if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                cur_support_share_platform_list.append(share_const.APP_SHARE_YOUTUBE)
        unsupport_pt_list = []
        for pt in cur_support_share_platform_list:
            share_types = self.share_apps_dict.get(pt, {}).get('share_types')
            if share_types:
                if share_type not in share_types:
                    unsupport_pt_list.append(pt)
                    continue
            check_func = self.share_apps_dict.get(pt, {}).get('check_func')
            if check_func:
                if not check_func(share_type):
                    unsupport_pt_list.append(pt)

        if share_type == share_const.TYPE_VIDEO:
            share_method = self.get_platform_share_method(share_const.APP_SHARE_WEIXIN_MOMENT, share_type)
            if share_method == share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE:
                if share_const.APP_SHARE_WEIXIN_MOMENT not in unsupport_pt_list:
                    unsupport_pt_list.append(share_const.APP_SHARE_WEIXIN_MOMENT)
        cur_support_share_platform_list = [ x for x in cur_support_share_platform_list if x not in unsupport_pt_list ]
        if channel_related:
            if global_data.channel:
                exclude_list = share_const.CHANNEL_SHARE_EXCLUDE_TABLE.get(global_data.channel.get_name(), [])
                if exclude_list == 'all':
                    return []
                else:
                    return [ pt for pt in cur_support_share_platform_list if pt not in exclude_list ]

        return [ pt for pt in cur_support_share_platform_list ]

    def get_support_platforms_from_enum(self, platform_enums):
        return [ self.share_apps_dict[pt] for pt in platform_enums if pt in self.share_apps_dict ]

    def check_can_share(self):
        pass

    def has_share(self, share_args):
        share_platform_str = share_args.get('platform_name', '')
        share_method = share_args.get('method', share_const.SH_METHOD_SOCIAL_CHANNEL)
        if not share_platform_str:
            return True
        print('share_platform_str', share_platform_str, 'share_method', share_method)
        if share_method in [share_const.SH_METHOD_SOCIAL_CHANNEL, share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE]:
            if global_data.channel:
                print('check ng has platform', share_platform_str)
                return global_data.channel.ng_has_platform(share_platform_str)
        ret = False
        return ret

    def share(self, share_args, share_type, image_path, title=None, message=None, desc='', link='', extJson='', share_cb=None, lab=None, videoPath='', UserName='', Path='', MiniProgramType='', otherJsonStr='', share_inform_cb=None, share_inform_text=None):
        if share_type == share_const.TYPE_VIDEO:
            if not global_data.feature_mgr.is_support_video_share():
                log_error('do not support vodeo share, please update engine!')
                return
        if not self.has_share(share_args):
            global_data.game_mgr.show_tip(get_text_by_id(2180))
            return False
        else:
            if title is None:
                if not interface.is_mainland_package():
                    title = get_text_by_id(1009) if 1 else get_text_by_id(1111)
                share_channel = share_args.get('channel', share_const.NT_SHARE_TYPE_FACEBOOK)
                if message is None:
                    message_queue = [
                     1010, 3101, 3102, 3103, 3104, 3105, 3106]
                    message_poll = message_queue
                    if self._last_message_id in message_queue and self._last_share_channel == share_channel:
                        message_poll.remove(self._last_message_id)
                    message_id = random.choice(message_poll)
                    message = get_text_by_id(message_id)
                    self._last_message_id = message_id
                else:
                    self._last_message_id = None
                if lab:
                    message = lab + ' ' + message
                cp_share_thumb_icon = COPY_SHARE_THUMB_ICON_NA if G_IS_NA_USER else COPY_SHARE_THUMB_ICON
                share_thumb_icon = cc.FileUtils.getInstance().isFileExist(cp_share_thumb_icon) or (SHARE_THUMB_ICON_NA if G_IS_NA_USER else SHARE_THUMB_ICON)
            else:
                share_thumb_icon = cp_share_thumb_icon
            if share_type not in share_const.TYPE_IMAGE:
                dst_path = os.path.join(game3d.get_doc_dir(), 'img_cover.jpg')
                if share_thumb_icon:
                    thumb_img_path = share_utils.copy_npk_img_to_document_path(share_thumb_icon, dst_path)
                else:
                    thumb_img_path = share_utils.copy_npk_img_to_document_path(share_thumb_icon, dst_path, need_convert=False)
                if thumb_img_path:
                    self.share_temp_files.add(thumb_img_path)
            else:
                thumb_img_path = ''
            if share_type == share_const.TYPE_IMAGE and share_channel == share_const.NT_SHARE_TYPE_QZONE:
                title = ''
                message = ''
                desc = ''
            if share_channel == share_const.NT_SHARE_TYPE_WEIBO and self.SHARE_WEIBO_DIR:
                if image_path:
                    shutil.copy(image_path, self.SHARE_WEIBO_FILE_PATH)
                    self.share_temp_files.add(self.SHARE_WEIBO_FILE_PATH)
                    image_path = self.SHARE_WEIBO_FILE_PATH
                if thumb_img_path:
                    dst_path = os.path.join(self.SHARE_WEIBO_DIR, 'img_cover.jpg')
                    shutil.copy(thumb_img_path, dst_path)
                    self.share_temp_files.add(dst_path)
                    thumb_img_path = dst_path
            if image_path and 'files/' not in image_path:
                new_image_path = os.path.join(self.SHARE_SAVE_DIR_NA, os.path.basename(image_path))
                shutil.copy(image_path, new_image_path)
                image_path = new_image_path
            if thumb_img_path and 'files/' not in thumb_img_path:
                dst_path = os.path.join(self.SHARE_SAVE_DIR_NA, os.path.basename(thumb_img_path))
                shutil.copy(thumb_img_path, dst_path)
                self.share_temp_files.add(dst_path)
                thumb_img_path = dst_path
            print('share_img_path', image_path)
            self._custom_share_cb = share_cb
            self._share_inform_cb = share_inform_cb
            self._share_inform_text = share_inform_text
            platform_enum = share_args.get('platform_enum', share_const.APP_SHARE_FACEBOOK)
            share_method = self.get_platform_share_method(platform_enum, share_type)
            self._last_share_channel = share_channel
            extJson = ''
            ret = False
            self._has_shared = True
            if share_method == share_const.SH_METHOD_SOCIAL_CHANNEL:
                if global_data.channel:
                    if global_data.channel._channel:
                        global_data.channel._channel.share_callback = self.on_share_finish
                    if global_data.feature_mgr.is_support_share_tag():
                        ret = global_data.channel.ng_share(share_channel, share_type, title, message, desc, link, image_path, thumb_img_path, videoPath, extJson, UserName, Path, MiniProgramType, otherJsonStr)
                    elif global_data.feature_mgr.is_support_mini_program_share():
                        ret = global_data.channel.ng_share(share_channel, share_type, title, message, desc, link, image_path, thumb_img_path, videoPath, extJson, UserName, Path, MiniProgramType)
                    elif global_data.feature_mgr.is_support_video_share():
                        ret = global_data.channel.ng_share(share_channel, share_type, title, message, desc, link, image_path, thumb_img_path, videoPath, extJson)
                    else:
                        ret = global_data.channel.ng_share(share_channel, share_type, title, message, desc, link, image_path, thumb_img_path, extJson)

                    def ios13_success():
                        platform_enum = share_args.get('platform_enum', share_const.APP_SHARE_FACEBOOK)
                        if platform_enum == share_const.APP_SHARE_FACEBOOK and game3d.get_platform() == game3d.PLATFORM_IOS:
                            from common.platform.device_info import DeviceInfo
                            device_info = DeviceInfo.get_instance()
                            os_ver = str(device_info.get_os_ver())
                            if os_ver.startswith('13'):
                                self.on_share_finish(True)

                    ios13_success()
            elif share_method == share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE:
                json_dict = {'methodId': 'ntShare','type': share_type,
                   'shareChannel': share_channel,
                   'image': image_path,
                   'videoUrl': videoPath,
                   'title': title,
                   'desc': desc,
                   'text': message,
                   'link': link,
                   'shareThumb': thumb_img_path
                   }
                global_data.channel.extend_func_by_dict(json_dict)

                def on_share_success():
                    if global_data.share_mgr:
                        self.on_share_success_inform()

                global_data.game_mgr.delay_exec(5.0, on_share_success)
            return ret

    def on_share_success_inform(self):
        if not self._has_shared:
            return
        else:
            self._has_shared = False
            if self._share_inform_cb or global_data.player:
                global_data.player.share()
                if self._share_inform_text:
                    share_text = self._share_inform_text if 1 else get_text_by_id(2177)
                    global_data.game_mgr.show_tip(share_text)
            else:
                self._share_inform_cb()
                self._share_inform_cb = None
                share_text = self._share_inform_text if self._share_inform_text else get_text_by_id(2177)
                global_data.game_mgr.show_tip(share_text)
            return

    def get_share_linegame_limit(self):
        return (40, 1000)

    def share_linegame(self, templateId, users, title, text, link, share_cb=None, a_link_param=''):
        from logic.gcommon import time_utility as tutil
        if not global_data.channel:
            return
        if not global_data.channel.is_bind_linegame():
            return
        linegame_share_last_time = global_data.achi_mgr.get_cur_user_archive_data('linegame_share_last_time', default=0)
        linegame_share_info = global_data.achi_mgr.get_cur_user_archive_data('linegame_share_info', default={})
        now = tutil.get_server_time()
        today_start_time = tutil.get_utc8_day_start_timestamp()
        if today_start_time > linegame_share_last_time:
            linegame_share_info = {}
        friends_limit, total_limit = self.get_share_linegame_limit()
        if sum(six_ex.values(linegame_share_info)) >= total_limit:
            global_data.game_mgr.show_tip(get_text_by_id(609024))
            return
        for user in users:
            if not user:
                continue
            if user not in linegame_share_info:
                if len(linegame_share_info) < friends_limit:
                    linegame_share_info[user] = 1
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(609024))
                    return
            else:
                linegame_share_info[user] += 1

        global_data.achi_mgr.set_cur_user_archive_data('linegame_share_last_time', now)
        global_data.achi_mgr.set_cur_user_archive_data('linegame_share_info', linegame_share_info)
        str_user_list = ','.join(users)
        self._custom_share_cb = share_cb
        self._last_share_channel = share_const.APP_SHARE_LINEGAME
        if global_data.channel._channel:
            global_data.channel._channel.share_callback = self.on_share_finish
        self._has_shared = True
        title_dict = {'paramTitle': title}
        str_title = json.dumps(title_dict)
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            global_data.channel.linegame_share(templateId, str_user_list, str_title, 'paramText={}'.format(text), 'paramLink={}'.format(link), 'param={}'.format(a_link_param), '')
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            global_data.channel.linegame_share(templateId, str_user_list, str_title, 'paramText`{}'.format(text), 'paramLink`{}'.format(link), 'param`{}'.format(a_link_param), '')

    def get_share_app_share_args(self, share_app):
        return self.share_apps_dict.get(share_app, {}).get('share_args', {})

    def get_share_app_info(self, share_app):
        return self.share_apps_dict.get(share_app, {})

    def on_share_finish(self, is_success):
        if not self._has_shared:
            return
        if is_success:
            self.on_share_success_inform()
        else:
            can_fail_as_success = True
            if self._last_share_channel == share_const.NT_SHARE_TYPE_FACEBOOK:
                if global_data.channel.get_prop_int('UNISDK_IS_FB_APP_INSTALLED', 0):
                    fail_msg = global_data.channel.get_prop_str('UNISDK_FB_SHARE_FAILURE_MESSAGE')
                    log_error('on_share_finish, share failed', fail_msg)
            elif self._last_share_channel == share_const.APP_SHARE_LINEGAME:
                code = global_data.channel.get_prop_str('LINE_ERROR_CODE')
                fail_msg = global_data.channel.get_prop_str('LINE_ERROR_MESSAGE')
                log_error('on_share_finish, linegame share failed', code, fail_msg)
            if can_fail_as_success:
                self.on_share_success_inform()
            else:
                global_data.game_mgr.show_tip(get_text_by_id(2179))
        self._has_shared = False
        if self._custom_share_cb:
            self._custom_share_cb(is_success)

    def on_screen_capture(self, image_path, end_callback=None, need_share_capture_ui=True):
        doc_dir = game3d.get_doc_dir()
        if not os.path.exists(doc_dir):
            os.mkdir(doc_dir)

        def share_func(file_path, encrypted_path, related_path):
            self._is_saving_file = False
            if os.path.exists(file_path):
                if need_share_capture_ui:
                    if not global_data.ui_mgr.get_ui('ShareScreenCaptureUI'):
                        return
                    global_data.ui_mgr.get_ui('ShareScreenCaptureUI').on_file_ready()
            if end_callback and callable(end_callback):
                end_callback(file_path, encrypted_path, related_path)

        if not self._is_saving_file:
            self._is_saving_file = True
            save_flags = 0
            render.save_screen_to_file(self.SHARE_SAVE_PATH, render.IFF_PNG, save_flags, True, lambda : share_func(self.SHARE_SAVE_PATH, self.SHARE_SAVE_ENCRYPTED_PATH, self.SHARE_SAVE_FILE_NAME))
        if need_share_capture_ui:
            ShareScreenCaptureUI()

    def capture_screen_to_share(self, end_callback, need_share_capture_ui=True):
        self.on_screen_capture(None, end_callback, need_share_capture_ui)
        return

    def share_screen_capture(self, share_arg, image_path=None):
        if not image_path:
            image_path = self.SHARE_SAVE_PATH
        if not os.path.exists(self.SHARE_SAVE_PATH):
            global_data.game_mgr.show_tip(get_text_by_id(2181))
            return
        self.share(share_arg, share_const.TYPE_IMAGE, image_path)

    def enable_screen_capture_share(self):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and not global_data.is_android_pc:
            permission = 'android.permission.READ_EXTERNAL_STORAGE'
            should_register = True
            if hasattr(game3d, 'check_client_permission') and hasattr(game3d, 'check_client_should_request_permission'):
                if not game3d.check_client_permission(permission, False):
                    achi_mgr = global_data.achi_mgr
                    if achi_mgr:
                        should_register = not achi_mgr.get_general_archive_data_value('has_asked_screen_capture_permission', default=False)
                        achi_mgr.save_general_archive_data_value('has_asked_screen_capture_permission', True)
                    else:
                        should_register = False
            if global_data.channel and should_register:
                global_data.channel.set_enable_screen_capture(True)
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            game.on_app_screen_capture = self.on_screen_capture
            if hasattr(game3d, 'enable_screen_capture_callback'):
                game3d.enable_screen_capture_callback(True)

    def disable_screen_capture_share(self):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if global_data.channel:
                global_data.channel.set_enable_screen_capture(False)
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            game.on_app_screen_capture = None
            if hasattr(game3d, 'enable_screen_capture_callback'):
                game3d.enable_screen_capture_callback(False)
        return

    def save_callback(self, ret):
        if ret:
            global_data.game_mgr.show_tip(get_text_by_id(2183))
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2184))
        from common.utilities import safe_copyfile
        safe_copyfile(self.SHARE_SAVE_PATH, self.SHARE_SAVE_ENCRYPTED_PATH)
        if self._save_to_gallery_callback:
            self._save_to_gallery_callback()

    def save_to_gallery(self, path=None, callback=None):
        self._save_to_gallery_callback = callback

        def save_callback(ret):
            global_data.game_mgr.post_exec(self.save_callback, ret)

        if path:
            share_pic_path = path
        else:
            share_pic_path = self.SHARE_SAVE_PATH
        img_title = ''
        img_description = ''
        prompt_for_permission = True
        prompt_title = get_text_local_content(3002)
        prompt_msg = get_text_local_content(3003)
        prompt_btn_close = get_text_local_content(3004)
        prompt_btn_setting = get_text_local_content(3005)
        platform = game3d.get_platform()
        if platform == game3d.PLATFORM_ANDROID:
            ret = game3d.save_image_to_gallery(share_pic_path, save_callback, img_title, img_description, prompt_for_permission, prompt_title, prompt_msg, prompt_btn_close, prompt_btn_setting)
            if ret == game3d.SAVE_IMAGE_TO_GALLERY_OK or ret == game3d.SAVE_IMAGE_TO_GALLERY_FAIL:
                save_callback(ret == game3d.SAVE_IMAGE_TO_GALLERY_OK)
        elif platform == game3d.PLATFORM_IOS:
            game3d.save_image_to_gallery(share_pic_path, save_callback, img_title, img_description, prompt_for_permission, prompt_title, prompt_msg, prompt_btn_close, prompt_btn_setting)
        elif self._save_to_gallery_callback:
            self._save_to_gallery_callback()

    def save_to_gallery_ex(self, img_path, pc_target_path, width, height, callback=None):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            file_whole_path = pc_target_path
            import os
            if img_path.startswith('gui'):
                file_whole_path = share_utils.copy_npk_img_to_document_path(img_path, file_whole_path)
            else:
                import shutil
                shutil.copy(img_path, file_whole_path)
            if global_data.channel.get_app_channel() == 'steam':
                json_dict = {'methodId': 'AddScreenshotToLibrary','filePath': file_whole_path,
                   'imageWidth': int(width),
                   'imageHeight': int(height)
                   }
                global_data.channel.extend_func_by_dict(json_dict)
            callback()
        else:
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                target_path = self.share_temp_dir + '/share_pic.png'
            else:
                target_path = self.share_temp_dir + '/share_pic.jpg'
            if img_path.startswith('gui'):
                share_utils.copy_npk_img_to_document_path(img_path, target_path)
            else:
                import shutil
                shutil.copy(img_path, target_path)
            self.save_to_gallery(target_path, callback)

    def get_linegame_share_post_data(self, feedNo, title, main_text, post_text, pic_id='', link_url=''):
        if not global_data.channel:
            return (None, None)
        else:
            linegame_auth_token = global_data.channel.get_linegame_auth_token()
            if not linegame_auth_token:
                return (None, None)
            platform = ''
            plat = game3d.get_platform()
            if plat == game3d.PLATFORM_ANDROID:
                platform = 'android'
            elif plat == game3d.PLATFORM_IOS:
                platform = 'iphone'
            if not title:
                title = get_text_by_id(1009)
            channel_conf = confmgr.get('channel_conf', interface.get_game_id())
            linegame_app_id = channel_conf.get('LINEGAME_APP_ID', '')
            header = {'accept': 'application/json',
               'X-Linegame-AppId': linegame_app_id,
               'X-Linegame-UserToken': linegame_auth_token,
               'Content-Type': 'application/json; charset=UTF-8'
               }
            post_data = {'feedNo': feedNo,
               'device': '{}|{}'.format(platform, global_data.channel.get_os_ver()),
               'region': 'JP',
               'postText': post_text,
               'template': {'titleText': title,
                            'mainText': main_text
                            },
               'thumbnail': {'height': 256,
                             'width': 256,
                             'url': 'https://www.supermechachampions.com/pc/gw/20190724131834/img/icon_64087ae.jpg'
                             },
               'url': [
                     {'device': 'WEB',
                        'targetUrl': 'https://www.supermechachampions.com/'
                        },
                     {'device': 'ANDROID',
                        'targetUrl': '{}://'.format(linegame_app_id.lower())
                        },
                     {'device': 'IPHONE',
                        'targetUrl': 'line3rdp.{}://'.format(game3d.get_app_name())
                        }],
               'test': not global_data.channel.get_fee_env()
               }
            if not pic_id:
                post_data['template']['subText'] = ''
            else:
                post_data['obsMedia'] = {'sid': 'linegame',
                   'oid': pic_id,
                   'namespace': 'tl',
                   'width': 16,
                   'height': 9,
                   'mediaType': 'PHOTO'
                   }
            if link_url:
                for info in post_data['url']:
                    info['targetUrl'] = link_url

            return (header, post_data)

    def request_share_linegame_photo(self, feedNo, title, main_text, post_text, pic_path, share_cb=None):
        from common import http
        from logic.gcommon import time_utility as tutil
        if not global_data.channel:
            return
        linegame_auth_token = global_data.channel.get_linegame_auth_token()
        if not linegame_auth_token:
            return
        channel_conf = confmgr.get('channel_conf', interface.get_game_id())
        linegame_app_id = channel_conf.get('LINEGAME_APP_ID', '')
        header = {'X-Obs-Params': 'ewogICJ2ZXIiOiIyLjAiLAogICJ0eXBlIjoiaW1hZ2UiLAogICJuYW1lIjoib2JzLnBuZyIKfQ==',
           'X-Linegame-AppId': linegame_app_id,
           'X-Linegame-TokenType': 0,
           'X-Linegame-UserToken': linegame_auth_token,
           'Content-Type': 'image/jpeg'
           }

        def cb(result, url, args, resbond_obj):
            pic_id = resbond_obj.getheader('x-obs-oid')
            self._share_linegame_timeline(feedNo, title, main_text, post_text, pic_id=pic_id, share_cb=share_cb)

        uid = global_data.player.uid
        now = int(tutil.get_server_time())
        url = 'http://obs.line-apps.com/r/linegame/tl/{}t{}tffffffff'.format(uid, now)
        tmp_file = open(pic_path, 'rb')
        r_data = tmp_file.read()
        tmp_file.close()
        http.request(url, data=r_data, header=header, callback=cb, require_resbond_obj=True)

    def _share_linegame_timeline(self, feedNo, title, main_text, post_text, pic_id='', link_url='', share_cb=None):
        from common import http
        header, post_data = self.get_linegame_share_post_data(feedNo, title, main_text, post_text, pic_id=pic_id, link_url=link_url)
        if not header:
            global_data.game_mgr.show_tip(get_text_by_id(2179))
            return

        def cb(result, url, args):
            global_data.game_mgr.show_tip(get_text_by_id(2177))
            if share_cb:
                share_cb(True)

        url = 'https://game-api-external.gcld-line.com/graph-event/v4.0/timeline'
        http.request(url, data=json.dumps(post_data), header=header, callback=cb)

    def clear_temp_share_file(self):
        import os
        try:
            if not self.share_temp_files:
                return
            for f in self.share_temp_files:
                if os.path.exists(f):
                    os.remove(f)

        except:
            pass

        self.share_temp_files = set()

    def get_platform_share_method(self, platform_enum, share_type):
        if share_type == share_const.TYPE_MINI_PROGRAM:
            return share_const.SH_METHOD_SOCIAL_CHANNEL
        type_share_method = self.share_apps_dict.get(platform_enum, {}).get('type_channel', {}).get(share_type)
        share_args = self.get_share_app_share_args(platform_enum)
        verified_packages_key = share_args.get('verified_packages_key')
        if not type_share_method:
            share_method = share_args.get('method', share_const.SH_METHOD_SOCIAL_CHANNEL) if 1 else type_share_method
            if verified_packages_key:
                verified_packages = share_utils.get_verified_packages(verified_packages_key)
                if game3d.get_app_name() not in verified_packages:
                    share_method = share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE
            share_method = share_utils.is_support_normal_share(game3d.get_app_name(), platform_enum) or share_const.SH_METHOD_SOCIAL_CHANNEL_SIMPLE
        return share_method

    def on_app_resume(self):
        if self._has_shared:
            self.on_share_success_inform()
            self._has_shared = False

    def test_share_video(self):
        from logic.client.const import share_const
        share_args = global_data.share_mgr.get_share_app_share_args(share_const.APP_SHARE_WEIXIN)
        video_url = 'https://fp-dev.webapp.163.com/g93na-record/file/5f914d7e54b2d31bf0c5e628Xug0vgC702'
        global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', videoPath=video_url)

    def test_share_file_video(self):
        from logic.client.const import share_const
        from logic.comsys.archive.archive_manager import ArchiveManager
        from logic.comsys.video import video_record_utils as vru
        file_inf = ArchiveManager().get_archive_data(vru.SETTING_NAME)
        share_args = global_data.share_mgr.get_share_app_share_args(share_const.APP_SHARE_MOBILE_QZONE)
        path_list = six_ex.keys(file_inf)
        if path_list:
            video_url = path_list[0]
            global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', videoPath=video_url)

    def all_test(self):

        def test_share_video(self):
            from logic.client.const import share_const
            share_args = global_data.share_mgr.get_share_app_share_args(share_const.APP_SHARE_WEIXIN)
            video_url = 'https://fp-dev.webapp.163.com/g93na-record/file/5f914d7e54b2d31bf0c5e628Xug0vgC702'
            global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', videoPath=video_url)

        def test_share_file_video(self):
            from logic.client.const import share_const
            from logic.comsys.archive.archive_manager import ArchiveManager
            from logic.comsys.video import video_record_utils as vru
            file_inf = ArchiveManager().get_archive_data(vru.SETTING_NAME)
            share_args = global_data.share_mgr.get_share_app_share_args(share_const.APP_SHARE_MOBILE_QZONE)
            path_list = six_ex.keys(file_inf)
            if path_list:
                video_url = path_list[0]
                global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', videoPath=video_url)

        def test4(self):
            from logic.client.const import share_const
            video_url = 'https://fp-dev.webapp.163.com/g93na-record/file/5f914d7e54b2d31bf0c5e628Xug0vgC702'
            json_dict = {'methodId': 'ntShare',
               'type': share_const.TYPE_VIDEO,
               'shareChannel': share_const.NT_SHARE_TYPE_QQ,
               'image': '',
               'videoUrl': video_url,
               'title': 'SMC',
               'desc': 'SMC DESC',
               'text': 'SMC TEXT',
               'link': '',
               'shareThumb': ''
               }
            global_data.channel.extend_func_by_dict(json_dict)

        def test_local_file(self):
            import game3d
            import os
            import shutil
            from logic.client.const import share_const
            from logic.comsys.archive.archive_manager import ArchiveManager
            from logic.comsys.video import video_record_utils as vru
            file_inf = ArchiveManager().get_archive_data(vru.SETTING_NAME)
            path_list = six_ex.keys(file_inf)
            out_path = os.path.join(game3d.get_doc_dir(), 'video_for_share.mp4')
            if not path_list or not vru.can_record_video():
                return
            try:
                shutil.copy(path_list[0], out_path)
            except Exception:
                log_error('[ShareManager] move video to share path failed', out_path)

            video_url = out_path
            json_dict = {'methodId': 'ntShare',
               'type': share_const.TYPE_VIDEO,
               'shareChannel': share_const.NT_SHARE_TYPE_QZONE,
               'image': '',
               'videoUrl': video_url,
               'title': 'SMC',
               'desc': 'SMC DESC',
               'text': 'SMC TEXT',
               'link': '',
               'shareThumb': ''
               }
            global_data.channel.extend_func_by_dict(json_dict)

        def test_local_file2(self):
            video_url = ''
            json_dict = {'methodId': 'ntShare',
               'type': share_const.TYPE_VIDEO,
               'shareChannel': share_const.NT_SHARE_TYPE_QZONE,
               'image': '',
               'videoUrl': video_url,
               'title': 'SMC',
               'desc': 'SMC DESC',
               'text': 'SMC TEXT',
               'link': '',
               'shareThumb': ''
               }
            global_data.channel.extend_func_by_dict(json_dict)

        def test_douyin():
            import game3d
            import os
            import shutil
            from logic.client.const import share_const
            from logic.comsys.archive.archive_manager import ArchiveManager
            from logic.comsys.video import video_record_utils as vru
            file_inf = ArchiveManager().get_archive_data(vru.SETTING_NAME)
            path_list = six_ex.keys(file_inf)
            out_path = os.path.join(game3d.get_doc_dir(), 'video_for_share.mp4')
            if not path_list or not vru.can_record_video():
                return
            try:
                shutil.copy(path_list[0], out_path)
            except Exception:
                log_error('[ShareManager] move video to share path failed', out_path)

            video_url = out_path
            share_args = global_data.share_mgr.get_share_app_share_args(share_const.APP_SHARE_DOUYIN)
            global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', videoPath=video_url)

    def share_video_url(self, share_platform, video_url, title=None, msg=None):
        from logic.client.const import share_const
        share_args = global_data.share_mgr.get_share_app_share_args(share_platform)
        global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', title, msg, videoPath=video_url)

    def share_local_video(self, share_platform, video_path, title=None, msg=None, tag=''):
        import shutil
        from logic.client.const import share_const
        if share_platform not in [share_const.APP_SHARE_KUAISHOU, share_const.APP_SHARE_FACEBOOK]:
            out_path = os.path.join(self.share_temp_dir, '%s.mp4' % str(title if title else 'video_for_share'))
        else:
            out_path = os.path.join(self.share_temp_dir, '%s.mp4' % str('video_for_share'))
        try:
            shutil.copy(video_path, out_path)
        except Exception as e:
            log_error('[ShareManager] move video to share path failed: %s error:%s' % (video_path, str(e)))

        share_args = global_data.share_mgr.get_share_app_share_args(share_platform)
        if not tag:
            otherJsonStr = json.dumps({'tag': get_text_by_id(1111)})
        else:
            otherJsonStr = ''
        global_data.share_mgr.share(share_args, share_const.TYPE_VIDEO, '', title, msg, videoPath=out_path, otherJsonStr=otherJsonStr)