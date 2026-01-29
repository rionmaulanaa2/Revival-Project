# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveSteamMainUI.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon import time_utility
from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
from logic.gcommon.common_const.liveshow_const import TAG_ALL, TAG_FOLLOW, TAG_PLATFORM_LABEL
from logic.gcommon.common_const import liveshow_const
from logic.vscene.part_sys.live.LiveSpriteManager import LiveSpriteManager
from common.cfg import confmgr
import game3d
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.comsys.lobby.EntryWidget.LotterySummerPeakLiveEntryWidget import check_show_entry
from logic.comsys.lobby.EntryWidget.LobbyWinterOutsideLiveEntryWidget import check_winter_outside_live_show_entry

class LiveChannelDesc(object):

    def __init__(self, type, name, data=None):
        self.type = type
        self.data = data
        self.name = name

    def __repr__(self):
        return str(self.name) + str(self.type)


class LiveSteamMainWidget(BaseUIWidget):
    EACH_SHOW_NUM = 15

    def __init__(self, panel_cls, ui_panel, *args, **kwargs):
        super(LiveSteamMainWidget, self).__init__(panel_cls, ui_panel, *args, **kwargs)
        self.on_init_panel()

    def on_init_panel(self):
        self._platform_channels = []
        self._cur_platform = None
        self._cur_platform_channel = None
        self.process_event(True)
        self.init_scroll_view()
        self.panel.btn_live.BindMethod('OnClick', self.on_click_start_live)
        self._in_require_page_info = None
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.clear_scroll_view()
        LiveSpriteManager().ClearCache()
        self._in_require_page_info = None
        return

    def destroy(self):
        self.on_finalize_panel()
        super(LiveSteamMainWidget, self).destroy()

    def init_one_cc_live_template(self, node, data):
        from logic.gutils.live_utils import format_one_line_text, format_view_person
        nickname = data.get('nickname', '')
        title = data.get('title', '') or ''
        hot_score = data.get('hot_score', 0)
        mobile_url = data.get('mobile_url', None)
        islive = data.get('islive', False) or mobile_url
        islive = True if islive else False
        need_request = data.get('need_request', False)
        follow_uid = str(data.get('follow_uid', None))
        uid = data.get('uid', None)
        cover = data.get('cover', None)
        if title is None:
            log_error('init_one_cc_live_template', data)
        formated_title = format_one_line_text(node.lab_title, title, node.lab_title.nd_max_length.getContentSize().width)
        node.lab_title.SetString(formated_title)
        formated_name = format_one_line_text(node.lab_name, nickname, node.lab_name.nd_name_max_length.getContentSize().width)
        node.lab_name.SetString(formated_name)
        node.lab_pop.SetString(format_view_person(hot_score))
        sp_name = '%s_%s' % (str(self._cur_platform.get_type()), str(uid))
        if cover:
            LiveSpriteManager().SetSpriteByLink(node.pic_live, cover, sp_name)
        head_img = data.get('head')
        sp_head_name = '%s_%s_head' % (str(self._cur_platform.get_type()), str(uid))
        if head_img:
            LiveSpriteManager().SetSpriteByLink(node.img_head, head_img, sp_head_name)
        else:
            print('no head', head_img, data)
        self.update_node_follow_show(node, follow_uid)
        node.lab_islive.setVisible(not bool(cover))
        node.lab_pop.setVisible(islive)
        node.nd_live.setVisible(bool(cover))
        node.data = data
        labels = data.get('label', [])
        if len(labels) > 0:
            node.lab_label.setVisible(True)
            first_label = labels[0]
            labelid = first_label.get('labelid', None)
            text = first_label.get('text', '')
            label_conf = dict(confmgr.get('live_label_conf'))
            if str(labelid) in label_conf:
                label_bg = label_conf[str(labelid)].get('label_bg')
            else:
                label_bg = 'gui/ui_res_2/live/bar_live_white.png'
            node.img_bar_label.SetDisplayFrameByPath('', label_bg)
        else:
            node.lab_label.setVisible(False)

        @node.btn_show.unique_callback()
        def OnClick(btn, touch, islive=islive):
            self.open_room_live_ui_with_check(islive, need_request, data)

        @node.btn_follow.callback()
        def OnClick(btn, touch):
            follow_uid = str(data.get('follow_uid', None))
            live_type = self._cur_platform.get_type()
            if not follow_uid:
                return
            else:
                from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
                is_follow = LivePlatformManager().get_cur_platform().check_is_anchor_followed(follow_uid)
                if is_follow:
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

                    def follow_func():
                        LivePlatformManager().require_unfollow_anchor(live_type, follow_uid)

                    SecondConfirmDlg2().confirm(content=15850, confirm_callback=follow_func)
                elif not LivePlatformManager().check_is_follow_list_full(live_type):
                    LivePlatformManager().require_follow_anchor(live_type, follow_uid, data)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(15854))
                return

        return

    def open_room_live_ui_with_check(self, islive, need_request, data):
        if islive or need_request:

            def confirm_callback():
                from logic.comsys.live.LiveTVUI import LiveTVUI
                ui_inst = LiveTVUI()
                ui_inst.set_play_data(self._cur_platform.get_type(), data)

            from common.platform.device_info import DeviceInfo
            platform = game3d.get_platform()
            device_info = DeviceInfo.get_instance()
            net_work_status = device_info.get_network()
            if platform in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS):
                is_wifi = net_work_status == 'wifi'
                if not is_wifi:
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                    SecondConfirmDlg2().confirm(content=get_text_by_id(2165), confirm_text=get_text_by_id(2166), confirm_callback=confirm_callback)
                    return
            confirm_callback()
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2167))

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_info = {'receive_live_platform_channels_event': self.refresh_platform_channel_bar,
           'notify_platform_live_list_update_event': self.update_live_show_data,
           'notify_follow_anchor_change_event': self.on_follow_anchor_changed,
           'live_platform_inited_event': self.on_platform_inited,
           'notify_platform_anchor_list_update_event': self.on_anchor_live_list_update
           }
        if is_bind:
            emgr.bind_events(event_info)
        else:
            emgr.unbind_events(event_info)

    def set_select_platform(self, platform_type):
        if self._cur_platform and self._cur_platform.get_type() == platform_type:
            return
        if self._cur_platform:
            platform_changed = platform_type != self._cur_platform.get_type()
        else:
            platform_changed = True
        LivePlatformManager().select_platform(platform_type)
        self._cur_platform = LivePlatformManager().get_cur_platform()
        self.init_platform_channels_data()
        if not self._cur_platform_channel:
            self.init_platform_channel_bar()
        else:
            self.update_cur_select_channel()
            if platform_changed:
                self.clear_live_list()
                self.require_remain_platform_channel_data(self._cur_platform.get_start_page())
        self.panel.btn_live.setVisible(self._cur_platform.is_support_live_broadcast())

    def require_remain_platform_channel_data(self, page=None):
        if self._cur_platform and self._cur_platform_channel:
            if self._cur_platform_channel.type == TAG_ALL:
                self._in_require_page_info = (
                 self._cur_platform.get_type(), TAG_ALL, page)
                self._cur_platform.request_all_live_list(page)
            elif self._cur_platform_channel.type == TAG_FOLLOW:
                self._in_require_page_info = (
                 self._cur_platform.get_type(), TAG_FOLLOW, page)
                self._cur_platform.request_follow_anchor_live_list(page)
            else:
                self._in_require_page_info = (
                 self._cur_platform.get_type(), self._cur_platform_channel.data, page)
                self._cur_platform.request_channel_live_list(self._cur_platform_channel.data, page)

    def clear_platform_channel_data(self):
        if self._cur_platform and self._cur_platform_channel:
            if self._cur_platform_channel.type == TAG_ALL:
                if not self._cur_platform.is_support_expired_time():
                    self._cur_platform.clear_all_live_cache()
            elif self._cur_platform_channel.type == TAG_FOLLOW:
                self._cur_platform.clear_follow_live_cache()
            elif not self._cur_platform.is_support_expired_time():
                self._cur_platform.clear_tag_channel_cache()

    def refresh_platform_channel_data(self):
        self.clear_platform_channel_data()
        if self._cur_platform.is_inited():
            self.require_remain_platform_channel_data(self._cur_platform.get_start_page())

    def update_cur_select_channel(self):
        if self._cur_platform_channel:
            if self._cur_platform_channel.type != TAG_PLATFORM_LABEL:
                if self._cur_platform_channel not in self._platform_channels:
                    for channel_desc in self._platform_channels:
                        if channel_desc.type == self._cur_platform_channel.type:
                            self._cur_platform_channel = channel_desc
                            return

                return
        if self._platform_channels and not self._cur_platform_channel:
            self._cur_platform_channel = self._platform_channels[0]

    def init_platform_channel_bar(self):
        from logic.gutils.template_utils import WindowTopSingleSelectListHelper
        self.is_first_red_dot = True

        def init_channel_btn(node, channel_desc):
            node.btn_tab.SetText(channel_desc.name)

        def channel_btn_click_cb(ui_item, channel_desc, idx):
            self.set_select_channel(channel_desc)

        self._channel_bar_wrapper = WindowTopSingleSelectListHelper()
        self._channel_bar_wrapper.set_up_list(self.panel.list_tab_2, self._show_platform_channels, init_channel_btn, channel_btn_click_cb)
        if not self._cur_platform_channel:
            self._channel_bar_wrapper.set_node_click(self.panel.list_tab_2.GetItem(0))
        elif self._cur_platform_channel in self._show_platform_channels:
            idx = self._show_platform_channels.index(self._cur_platform_channel)
            if idx is not None and idx >= 0:
                self._channel_bar_wrapper.set_node_select(self.panel.list_tab_2.GetItem(idx))
        elif self._cur_platform_channel.type == TAG_FOLLOW:
            self._channel_bar_wrapper.set_node_select(None)
        return

    def init_platform_channels_data(self):
        self._platform_channels = []
        self._show_platform_channels = []
        if self._cur_platform:
            support_channels = self._cur_platform.get_support_channels()
            for channel in support_channels:
                channel_desc = LiveChannelDesc(channel['type'], channel['name'], channel['data'])
                self._platform_channels.append(channel_desc)
                self._show_platform_channels.append(channel_desc)

    def refresh_platform_channel_bar(self, platform_type, labels):
        if self._cur_platform:
            if platform_type == self._cur_platform.get_type():
                self.init_platform_channels_data()
                self.update_cur_select_channel()
                self.init_platform_channel_bar()

    def set_select_channel(self, channel_desc):
        if channel_desc != self._cur_platform_channel:
            self.clear_live_list()
            self._cur_platform_channel = channel_desc
            self.require_remain_platform_channel_data(self._cur_platform.get_start_page())

    def init_scroll_view(self):
        self.live_show_list = []
        self._cur_live_page = -1
        self._page_sizes = {}
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget

        def require_data_callback():
            if self.check_has_enough_live_list():
                self.append_scroll_show_live_list()
            elif self.check_channel_require_cd():
                self.require_remain_platform_channel_data(self._cur_live_page + 1)
            else:
                global_data.game_mgr.show_tip(get_text_by_id(2169))

        def refresh_callback():
            if self.check_channel_require_cd():
                self.refresh_platform_channel_data()
            else:
                global_data.game_mgr.show_tip(get_text_by_id(2169))

        self._sview = InfiniteScrollWidget(self.panel.live_list, self.panel.nd_tv, up_limit=600, down_limit=600)
        self._sview.set_require_data_callback(require_data_callback)
        self._sview.set_refresh_callback(refresh_callback)
        self._sview.set_template_init_callback(self.init_one_cc_live_template)
        self._sview.enable_item_auto_pool(True)

    def check_has_enough_live_list(self):
        cur_sview_data_len = self._sview.get_data_list_len()
        return cur_sview_data_len + self.EACH_SHOW_NUM <= len(self.live_show_list)

    def append_scroll_show_live_list(self):
        cur_sview_data_len = self._sview.get_data_list_len()
        if cur_sview_data_len + self.EACH_SHOW_NUM < len(self.live_show_list):
            self._sview.on_receive_data(self.live_show_list[cur_sview_data_len:cur_sview_data_len + self.EACH_SHOW_NUM])
        elif cur_sview_data_len < len(self.live_show_list):
            self._sview.on_receive_data(self.live_show_list[cur_sview_data_len:])
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2170))
            self._sview.on_receive_data([])

    def clear_scroll_view(self):
        if self._sview:
            self._sview.destroy()
            self._sview = None
        return

    def update_live_show_data(self, platform_type):
        if self._cur_platform and self._cur_platform_channel:
            self._in_require_page_info or log_error('informing update but has no require info')
            return
        else:
            live_type, tag, next_page = self._in_require_page_info
            if live_type != self._cur_platform.get_type() or live_type != platform_type:
                return
            if next_page is None:
                if self._cur_live_page < 0:
                    next_page = self._cur_platform.get_start_page() if 1 else self._cur_live_page + 1
                if self._cur_platform_channel.type == TAG_ALL:
                    new_live_list = self._cur_platform.get_all_live_list(next_page)
                elif self._cur_platform_channel.type == TAG_FOLLOW:
                    new_live_list = self._cur_platform.get_follow_live_list(next_page)
                else:
                    new_live_list = self._cur_platform.get_label_live_list(self._cur_platform_channel.data.get('labelid', 1), next_page)
                if not new_live_list:
                    new_live_list = []
                old_page_size = self._page_sizes.get(next_page, 0)
                old_live_list_size = len(self.live_show_list)
                self._page_sizes[next_page] = len(new_live_list)
                if old_page_size > 0:
                    self.live_show_list = self.live_show_list[:old_live_list_size - old_page_size]
                is_first_show = old_live_list_size == 0
                if new_live_list:
                    self.live_show_list.extend(new_live_list)
                    self._cur_live_page = next_page
                if check_show_entry() or check_winter_outside_live_show_entry():

                    def top_list_node--- This code section failed: ---

 436       0  LOAD_GLOBAL           0  'liveshow_const'
           3  LOAD_ATTR             1  'SUMMER_FINAL_URL_DICT'
           6  LOAD_ATTR             2  'get'
           9  LOAD_DEREF            0  'platform_type'
          12  LOAD_CONST            1  ''
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            1  'platform_nickname'

 437      21  SETUP_LOOP          179  'to 203'
          24  LOAD_GLOBAL           3  'range'
          27  LOAD_GLOBAL           4  'len'
          30  LOAD_FAST             0  'show_list'
          33  CALL_FUNCTION_1       1 
          36  CALL_FUNCTION_1       1 
          39  GET_ITER         
          40  FOR_ITER            159  'to 202'
          43  STORE_FAST            2  'idx'

 438      46  LOAD_FAST             0  'show_list'
          49  LOAD_FAST             2  'idx'
          52  BINARY_SUBSCR    
          53  STORE_FAST            3  'live_data'

 439      56  LOAD_FAST             3  'live_data'
          59  LOAD_ATTR             2  'get'
          62  LOAD_CONST            2  'nickname'
          65  LOAD_CONST            1  ''
          68  CALL_FUNCTION_2       2 
          71  STORE_FAST            4  'nickname'

 440      74  LOAD_FAST             3  'live_data'
          77  LOAD_ATTR             2  'get'
          80  LOAD_CONST            3  'mobile_url'
          83  LOAD_CONST            0  ''
          86  CALL_FUNCTION_2       2 
          89  STORE_FAST            5  'mobile_url'

 441      92  LOAD_GLOBAL           6  'bool'
          95  LOAD_FAST             3  'live_data'
          98  LOAD_ATTR             2  'get'
         101  LOAD_CONST            4  'islive'
         104  LOAD_GLOBAL           7  'False'
         107  CALL_FUNCTION_2       2 
         110  JUMP_IF_TRUE_OR_POP   116  'to 116'
         113  LOAD_FAST             5  'mobile_url'
       116_0  COME_FROM                '110'
         116  CALL_FUNCTION_1       1 
         119  STORE_FAST            6  'is_live'

 442     122  LOAD_FAST             3  'live_data'
         125  LOAD_ATTR             2  'get'
         128  LOAD_CONST            5  'need_request'
         131  LOAD_GLOBAL           7  'False'
         134  CALL_FUNCTION_2       2 
         137  STORE_FAST            7  'need_request'

 444     140  LOAD_FAST             7  'need_request'
         143  UNARY_NOT        
         144  POP_JUMP_IF_FALSE   160  'to 160'
         147  LOAD_FAST             6  'is_live'
         150  UNARY_NOT        
       151_0  COME_FROM                '144'
         151  POP_JUMP_IF_FALSE   160  'to 160'

 445     154  CONTINUE             40  'to 40'
         157  JUMP_FORWARD          0  'to 160'
       160_0  COME_FROM                '157'

 446     160  LOAD_FAST             4  'nickname'
         163  LOAD_FAST             1  'platform_nickname'
         166  COMPARE_OP            2  '=='
         169  POP_JUMP_IF_FALSE    40  'to 40'

 448     172  LOAD_FAST             0  'show_list'
         175  LOAD_FAST             2  'idx'
         178  BINARY_SUBSCR    
         179  BINARY_SUBSCR    
         180  DELETE_SUBSCR    
         181  DELETE_SUBSCR    
         182  BINARY_SUBSCR    
         183  ROT_TWO          
         184  ROT_TWO          
         185  DELETE_SUBSCR    
         186  DELETE_SUBSCR    
         187  STORE_SUBSCR     
         188  LOAD_FAST             0  'show_list'
         191  LOAD_FAST             2  'idx'
         194  STORE_SUBSCR     

 449     195  BREAK_LOOP       
         196  JUMP_BACK            40  'to 40'
         199  JUMP_BACK            40  'to 40'
         202  POP_BLOCK        
       203_0  COME_FROM                '21'
         203  LOAD_CONST            0  ''
         206  RETURN_VALUE     

Parse error at or near `BINARY_SUBSCR' instruction at offset 179

                    if is_first_show and old_page_size <= 0:
                        top_list_node(self.live_show_list)
                    else:
                        top_list_node(new_live_list)
                if is_first_show and old_page_size <= 0:
                    self._sview.on_receive_data(self.live_show_list)
                else:
                    self._sview.on_receive_update_tail_data(max(old_live_list_size - old_page_size, 0), new_live_list)
                if not new_live_list:
                    pass
            if not self.live_show_list:
                self.show_lab_tips()
            else:
                self.panel.lab_tips.setVisible(False)
            return

    def show_lab_tips(self):
        size = self.panel.live_list.GetConfSize()
        self.panel.live_list.setInnerContainerSize(size)
        self.panel.live_list.setContentSize(size)
        self.panel.lab_tips.setVisible(True)
        self.panel.lab_tips.ReConfPosition()

    def clear_live_list(self):
        self.live_show_list = []
        self._cur_live_page = -1
        self._page_sizes = {}
        self._sview.clear()

    def on_follow_anchor_changed(self, platform_type=None, follow_uid=None, is_follow=True):
        if self._cur_platform and platform_type:
            if platform_type != self._cur_platform.get_type():
                return
            if follow_uid is None:
                for ind, data in enumerate(self.live_show_list):
                    follow_uid = data.get('follow_uid')
                    node = self._sview.get_list_item(ind)
                    if not node:
                        continue
                    self.update_node_follow_show(node, follow_uid)

            else:
                self.update_follow_show(follow_uid)
            if is_follow is False:
                global_data.game_mgr.show_tip(get_text_by_id(15851))
        return

    def update_follow_show(self, follow_uid):
        target_ind = None
        for ind, data in enumerate(self.live_show_list):
            if str(data.get('follow_uid')) == str(follow_uid):
                target_ind = ind

        node = None
        if target_ind is not None:
            node = self._sview.get_list_item(target_ind)
        if not node:
            return
        else:
            self.update_node_follow_show(node, follow_uid)
            return

    def update_node_follow_show(self, node, follow_uid):
        if follow_uid:
            node.btn_follow.setVisible(True)
            is_follow = self._cur_platform.check_is_anchor_followed(follow_uid)
            node.img_follow_0.setVisible(not is_follow)
            node.img_follow_1.setVisible(is_follow)
        else:
            node.btn_follow.setVisible(False)

    def on_platform_inited(self, plat_type):
        if plat_type == self._cur_platform.get_type():
            self.refresh_platform_channel_data()

    def check_channel_require_cd(self):
        if self._cur_platform and self._cur_platform_channel:
            if self._cur_platform_channel.type == TAG_ALL:
                return self._cur_platform.check_all_channel_require_data_cd()
            else:
                if self._cur_platform_channel.type == TAG_FOLLOW:
                    return self._cur_platform.check_anchor_channel_require_data_cd()
                return self._cur_platform.check_tag_channel_require_data_cd(self._cur_platform_channel.data.get('labelid', 1))

        return False

    def on_click_start_live(self, btn, touch):
        if self._cur_platform.is_support_live_broadcast():
            global_data.game_mgr.show_tip(get_text_by_id(609395))
            global_data.game_mgr.show_tip(get_text_by_id(609396))
            self._cur_platform.start_live_broadcast()

    def on_anchor_live_list_update(self, platform_type):
        if self._cur_platform and self._cur_platform_channel:
            if self._cur_platform_channel.type != TAG_FOLLOW:
                return
            if self._cur_platform.get_type() == platform_type:
                self.update_live_show_data(platform_type)

    def test(self):
        import objgraph
        print(objgraph.by_type('KuaishouLivePlatform')[0]._all_channel._all_live_cache._page_expire_time_dict)