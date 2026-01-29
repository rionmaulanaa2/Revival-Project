# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/HighLightShareCreator.py
from __future__ import absolute_import
import os
import shutil
from logic.comsys.video.VideoRecord import VideoRecord
from logic.comsys.video import video_record_utils as vru
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class HighLightShareCreator(ShareTemplateBase):
    KIND = 'HIGH_LIGHT_SHARE'

    def __init__(self):
        super(HighLightShareCreator, self).__init__()
        self._save_rt = None
        self._video_info = None
        self._init_cb = None
        self._cover_path = None
        self._cover_info = {}
        return

    def create_panel(self, video_path, init_cb=None, parent=None):
        self._init_cb = init_cb
        self._video_info = video_path
        super(HighLightShareCreator, self).create(parent)
        VideoRecord().set_cover_finish_callback(self._cover_finish_cb)
        if video_path.endswith('.mp4'):
            cover_path = str(video_path[:-3]) + 'png'
        else:
            cover_path = str(video_path) + '.png'
        self._cover_info[cover_path] = video_path
        VideoRecord().create_video_cover(video_path, cover_path, 1)

    def _cover_finish_cb(self, path):
        if path not in self._cover_info:
            return
        else:
            VideoRecord().set_cover_finish_callback(None)
            ret, md5_str_cal = vru.cal_video_md5(path)
            if ret:
                small_file_name, icon_path = vru.get_cover_name_and_path(md5_str_cal)
                try:
                    dir_path = os.path.dirname(icon_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    shutil.copy(path, icon_path)
                    os.remove(path)
                    self._cover_path = icon_path
                    vru.cal_and_set_cover_node(small_file_name, self.panel.pnl_content, vru.SCALE_MODE_FILL, True, self.panel)
                except Exception as e:
                    log_error('[HighLightShareCreator] cover finish cb error: %s' % str(e))

            if self._init_cb:
                self._init_cb()
            return

    def destroy(self):
        if self._cover_path:
            try:
                if os.path.exists(self._cover_path):
                    os.remove(self._cover_path)
            except Exception as e:
                log_error('[HighLightShareCreator] remove [%s] error:[%s]' % (self._cover_path, e))

        VideoRecord().set_cover_finish_callback(None)
        super(HighLightShareCreator, self).destroy()
        return