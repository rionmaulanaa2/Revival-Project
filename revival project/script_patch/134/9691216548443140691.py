# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityNewMecha8022Interview.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.advance_utils import set_new_mecha
import game3d
from common.platform.device_info import DeviceInfo

class ActivityNewMecha8022Interview(ActivityBase):

    def on_init_panel(self):
        self.init_status()
        self.panel.list_item.SetInitCount(1)
        node = self.panel.list_item.GetItem(0)
        node.btn_bar.BindMethod('OnClick', self.on_click_play)

    def on_finalize_panel(self):
        pass

    def on_click_play(self, *args):
        self.update_status()
        if not self.is_wifi:

            def cancel_callback():
                pass

            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_by_id(2165), confirm_text=get_text_by_id(2166), cancel_text=get_text_by_id(2176), confirm_callback=lambda : self.play_video(), cancel_callback=cancel_callback)
        else:
            self.play_video()

    def play_video(self):
        from common.platform.dctool import interface
        if interface.is_mainland_package():
            url = 'http://g93-record.fp.ps.netease.com/file/621f18dbf186328f140c1b81AGlSvwBz04'
            from logic.comsys.video.VideoUILogicWidget import VideoUILogicWidget
            widget = VideoUILogicWidget()
            widget.change_fit_method('1w')
            widget.play_vod(url)
        else:
            from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_JA, LANG_KO, LANG_ZHTW, LANG_EN
            lang_dict = {LANG_KO: 'https://www.youtube.com/watch?v=PFTNK24CeOE',LANG_JA: 'https://www.youtube.com/watch?v=J2TgyVwz7kI',
               LANG_ZHTW: 'https://youtu.be/AA57WwUKIY0',
               LANG_CN: 'https://youtu.be/AA57WwUKIY0',
               LANG_EN: 'https://www.youtube.com/watch?v=NL0AUnJvSgg'
               }
            cur_lang = get_cur_text_lang()
            url = lang_dict.get(cur_lang, lang_dict[LANG_EN])
            game3d.open_url(url)

    def init_status(self):
        self.is_wifi = False
        self.update_status()

    def update_status(self):
        device_info = DeviceInfo.get_instance()
        net_work_status = device_info.get_network()
        platform = game3d.get_platform()
        if platform in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS):
            is_wifi = net_work_status == 'wifi'
            if is_wifi != self.is_wifi:
                self.is_wifi = is_wifi
        else:
            self.is_wifi = True