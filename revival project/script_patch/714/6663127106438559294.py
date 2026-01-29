# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/announcement/AnnouncementUI.py
from __future__ import absolute_import
import game3d
import common.const.uiconst
from cocosui import cc
from common.cfg import confmgr
from common.platform.dctool import interface
from common.uisys.basepanel import BasePanel
from common.platform.orbit_utils import OrbitHelper
from common.uisys.uielment.CCRichText import CCRichText
from logic.gcommon.common_utils.local_text import get_cur_lang_name, get_lang_code_by_lang_name
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.salog import SALog
from common.uisys.uielment.CCNode import hash_mod
import six
PLATFORM_ANNOUNCE_TYPE = 0
WEEK_ANNOUNCE_TYPE = 1
REQUEST_ID = 0
ANNOUNCEMENT_SHOWED = False
from logic.comsys.chat import chat_link

class AnnouncementUI(WindowMediumBase):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    PANEL_CONFIG_NAME = 'login/announce'
    UI_ACTION_EVENT = {}
    TEMPLATE_NODE_NAME = 'bg_panel'
    SHOW_CONTENT_ANIM_TAG = hash_mod('show_content_233_internal_use')

    def on_init_panel(self, *args, **kargs):
        global ANNOUNCEMENT_SHOWED
        super(AnnouncementUI, self).on_init_panel()
        self._msg = None
        self._msg_width = self.panel.nd_content.scroll_view.getContentSize().width
        self._requresting = False
        self._first_show = not ANNOUNCEMENT_SHOWED
        ANNOUNCEMENT_SHOWED = True
        self.hide_main_ui(['SvrSelectUI'])
        self.cb = kargs.get('cb', None)
        return

    def close(self):
        self.show_main_ui()
        if self._first_show:
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.FIRST_CLOSE_NOTICE)
        global_data.emgr.check_first_choosing_svr_event.emit()
        super(AnnouncementUI, self).close()
        self.cb and self.cb()

    def show_content(self, title, msg):
        self.panel.bg_panel.lab_title.SetString(title)
        self._msg = '<color=0x18192EFF>%s</color>' % msg
        self.refresh_data()

    def request_platform_announce(self):
        self.request_data()

    def on_data_response_callback(self, ret, url=None, *args):
        ret = six.ensure_str(ret)
        self._requresting = False
        self._msg = '<color=0x18192EFF>%s</color>' % ret
        self.refresh_data()

    def on_data_response_callback_win32(self, ret, url=None, *args):
        if ret:
            ret = six.ensure_str(ret)
            self._requresting = False
            self._msg = '<color=0x18192EFF>%s</color>' % ret
            self.refresh_data()
        else:
            url = self.get_announcement_url(game3d.PLATFORM_ANDROID)
            common.http.request(url, None, callback=self.on_data_response_callback)
        return

    def request_data(self):
        global REQUEST_ID
        import common.http
        if self._requresting:
            return
        else:
            self._requresting = True
            url = self.get_announcement_url(game3d.get_platform())
            if not global_data.channel.is_downloader_enable():
                common.http.request(url, None, callback=self.on_data_response_callback_win32)
            else:
                OrbitHelper().add_request(url, 'anouncement_%d.txt' % REQUEST_ID, self.on_data_response_callback)
                REQUEST_ID += 1
            return

    def get_announcement_url(self, cur_platform):
        game_id = interface.get_game_id()
        if game_id == 'g93':
            platform_map = {game3d.PLATFORM_IOS: 'ios',game3d.PLATFORM_ANDROID: 'android',
               game3d.PLATFORM_WIN32: 'win32'
               }
            platform_type = platform_map.get(cur_platform)
            url_conf = confmgr.get('server', 'notice_platform')[game_id][platform_type]
            url = url_conf['cn']
        else:
            lang_name = get_cur_lang_name()
            if global_data.channel and global_data.channel.is_steam_channel():
                platform_type = 'win32_steam'
            elif cur_platform in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID):
                platform_type = 'mobile'
            else:
                platform_type = 'win32'
            url_conf = confmgr.get('server', 'notice_platform')[game_id][platform_type]
            if lang_name in url_conf:
                url = url_conf[lang_name]
            else:
                url = url_conf['en']
        return url

    def get_announcement_lang(self):
        game_id = interface.get_game_id()
        if game_id == 'g93':
            return 'cn'
        else:
            lang_name = get_cur_lang_name()
            if global_data.channel and global_data.channel.is_steam_channel():
                platform_type = 'win32_steam'
            elif game3d.get_platform() in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID):
                platform_type = 'mobile'
            else:
                platform_type = 'win32'
            url_conf = confmgr.get('server', 'notice_platform')[game_id][platform_type]
            if lang_name in url_conf:
                return lang_name
            return 'en'

    def refresh_data(self):
        if not self.panel:
            return
        if not self._msg:
            return
        self.panel.nd_content.scroll_view.DeleteAllSubItem()
        content = chat_link.linkstr_to_richtext(self._msg)

        def touch_callback(msg, ele, touch, touch_event):
            chat_link.link_touch_callback(msg)

        panel = self.panel.nd_content.scroll_view.AddTemplateItem()
        rt_msg = CCRichText.Create('', 24, cc.Size(self._msg_width, 0))
        lang_name = self.get_announcement_lang()
        lang_code = get_lang_code_by_lang_name(lang_name)
        from common.cfg import confmgr
        conf = confmgr.get('lang_conf', str(lang_code), default={})
        rt_msg.SetString(content)
        rt_msg.setLineBreakWithoutSpace(not bool(conf.get('bDefLineBreak', 1)))
        rt_msg.SetCallback(touch_callback)
        rt_msg.setAnchorPoint(cc.Vec2(0.0, 1.0))
        rt_msg.setHorizontalAlign(0)
        rt_msg.formatText()
        size = rt_msg.getVirtualRendererSize()
        rt_msg.setPosition(cc.Vec2(0, size.height))
        panel.setContentSize(size)
        panel.AddChild('msg', rt_msg)
        rt_msg.setVisible(False)
        action_list = []
        action_list.append(cc.DelayTime.create(0.5))

        def _cc_show_rt_msg():
            rt_msg.setVisible(True)

        action_list.append(cc.CallFunc.create(_cc_show_rt_msg))
        seq = cc.Sequence.create(action_list)
        seq.setTag(self.SHOW_CONTENT_ANIM_TAG)
        self.panel.stopActionByTag(self.SHOW_CONTENT_ANIM_TAG)
        self.panel.runAction(seq)
        self.panel.nd_content.scroll_view._container._refreshItemPos()
        self.panel.nd_content.scroll_view._refreshItemPos()