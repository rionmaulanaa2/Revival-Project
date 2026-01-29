# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/video_utils.py
from __future__ import absolute_import
from logic.gutils.mall_utils import get_lottery_widgets_info, check_lottery_visible
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr

def check_play_lottery_video(end_callback=None, lottery_id=None, end_callback_arg=()):
    if not global_data.video_player.is_in_init_state():
        global_data.video_player.stop_video(ignore_cb=True)
        return False
    else:
        widgets_info, widgets_list = get_lottery_widgets_info()
        if not lottery_id:
            info = None
            if widgets_list:
                for cur_info in widgets_list:
                    lottery_id = cur_info.get('lottery_id', None)
                    if not lottery_id or not check_lottery_visible(lottery_id):
                        continue
                    else:
                        info = cur_info
                        break

        else:
            info = widgets_info.get(lottery_id, None)
        if info:
            video_tag = info.get('video_path', None)
            if video_tag:
                day = global_data.player.get_setting(video_tag, -1)
                today = int(tutil.get_date_str('%Y%m%d'))
                if day != today or global_data.tplv:
                    global_data.player.write_setting(video_tag, today)
                    global_data.player.save_settings_to_file()
                    global_data.video_player.play_video('video/%s.mp4' % video_tag, end_callback, {}, cb_args=end_callback_arg)
                    return video_tag
        return False


has_cn_ver = {
 201011152}

def check_play_chuchang_video(skin_id):
    conf = confmgr.get('display_video_conf', 'VideoTag', 'Content').get(str(skin_id), None)
    return conf is not None


def get_chuchang_video_path(skin_id):
    video_path = confmgr.get('display_video_conf', 'VideoTag', 'Content', str(skin_id), 'video_path', default='')
    if not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel() and skin_id in has_cn_ver:
        video_path += '_cn'
    return video_path


def get_relative_video_skin_list(skin_id):
    conf = confmgr.get('display_video_conf', 'VideoTag', 'Content').get(str(skin_id), {})
    rel_skins = conf.get('rel_skins', [])
    if rel_skins:
        return rel_skins
    return [skin_id]


def check_play_chuchang_video_with_tag(skin_id, played_tag):
    conf = confmgr.get('display_video_conf', 'VideoTag', 'Content').get(str(skin_id), None)
    if conf is None:
        return False
    else:
        video_path = conf.get('video_path', None)
        if video_path is None:
            return False
        if video_path != played_tag:
            return get_chuchang_video_path(skin_id)
        return False
        return


def get_login_video_name():
    import C_file
    video_path = confmgr.get('display_video_conf', 'VideoPlayScene', 'Content', 'login', 'video_path')
    if video_path and C_file.find_res_file(video_path, ''):
        return video_path
    else:
        from common.const.common_const import LOGIN_BK_VIDEO_NAME
        return LOGIN_BK_VIDEO_NAME