# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCreatorDisplay.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.activity.ActivityCollect import ActivityBase
from common.cfg import confmgr
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.comsys.video.VideoUILogicWidget import VideoUILogicWidget
from common.utils import network_utils
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.gutils import micro_webservice_utils
from logic.gcommon import time_utility
from logic.gutils.role_head_utils import init_role_head
from common.utils import timer
from logic.comsys.video.VideoWindowCtrlUI import VideoWindowCtrlUI
from logic.gcommon.const import ACTIVITY_CREATOR_DISPLAY_KEY
import cc
ARCI_PRE_FIX = 'CREATORDISPLAY_{0}_{1}'
VIDEO_TIME_INTERVAL = 5
CIRCULATE_PLAY_TIME = 1
CIRCULATE_TIMES = 4

class ActivityCreatorDisplay(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCreatorDisplay, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self.init_panel()
        self.process_events(True)
        self.write_local_data()

    def init_parameters(self):
        self.video_url = ''
        self.show_idx = 0
        self.show_uid = 0
        self.last_show_idx = 0
        self.like_num_dict = {}
        self.reorder_list = []
        self.creator_info = confmgr.get('c_creator_display', 'CreatorInfo', 'Content')
        self.container = self.panel.list_lab
        self.reorder_show_list()
        self.last_play_time = {}
        self.drag_show_idx = 0
        self.btn_play_dict = {}
        self.play_video_url = None
        self.drag_selected_change = False
        self.is_hold_btn_play = False
        self.is_hold_btn_like = False
        self.is_play_video = False
        self.can_drag_container = True
        self.on_hold_show_idx = 0
        self.drag_container_direction = 0
        self.video_player_widget = None
        self.start_count = 0
        self.circulate_timer = global_data.game_mgr.register_logic_timer(self.circulate_display_page, interval=CIRCULATE_PLAY_TIME, times=-1, mode=timer.CLOCK)
        return

    def init_panel(self):
        self.switch_creator_page(0)

    def reorder_show_list(self):
        if not self.creator_info:
            return
        order_idx_list = []
        for uid, info in six.iteritems(self.creator_info):
            if info.get('is_skip', 0) == 1:
                continue
            order_idx_list.append(info.get('order', 0))
            self.reorder_list.append(uid)

        def cfunc(elem):
            return self.creator_info.get(elem, {}).get('order', 0)

        self.reorder_list.sort(key=cfunc)
        self.panel.list_dot.SetInitCount(len(self.reorder_list))
        self.container.SetInitCount(len(self.reorder_list))
        item = self.container.GetItem(0)
        self.item_width, self.item_height = item.GetContentSize()

    def write_local_data(self):
        global_data.achi_mgr.get_general_archive_data().set_field(ACTIVITY_CREATOR_DISPLAY_KEY, self.reorder_list)
        global_data.emgr.refresh_activity_redpoint.emit()

    def init_creator_page(self, idx):
        uid = self.reorder_list[idx]
        infos = self.creator_info.get(str(uid), None)
        if not infos:
            return
        else:
            item = self.container.GetItem(idx)
            item.btn_play.setVisible(True)
            if self.check_display_video(idx):
                item.lab_describe.SetString('')
                item.img_cover.setVisible(True)
                item.img_cover.SetDisplayFrameByPath('', infos.get('user_video_logo', ''))
            else:
                item.img_cover.setVisible(False)
                item.lab_describe.SetString(infos.get('user_text_id', 0))
                item.lab_describe.formatText()
            self.btn_play_dict[idx] = item.btn_play
            return

    def switch_creator_page(self, idx):
        self.btn_play_dict[idx].setVisible(True)
        self.panel.btn_close.setVisible(False)
        self.show_idx = idx
        self.drag_show_idx = idx
        fixed_x, fixed_y = self.container.GetPosition()
        select_item_center_x = self.show_idx * self.item_width + 0.5 * self.item_width
        fixed_x = 0.5 * self.item_width - select_item_center_x
        self.container.SetPosition(fixed_x, fixed_y)
        self.can_drag_container = True
        self.btn_play_dict[self.show_idx].setVisible(True)
        self.panel.btn_close.setVisible(False)
        self.refresh_page_info()

    def refresh_page_info(self):
        uid = self.reorder_list[self.show_idx]
        self.show_uid = uid
        infos = self.creator_info.get(str(uid), None)
        if not infos:
            return
        else:
            now_dot = self.panel.list_dot.GetItem(self.last_show_idx)
            now_dot.btn_dot.SetEnable(True)
            last_dot = self.panel.list_dot.GetItem(self.show_idx)
            last_dot.btn_dot.SetEnable(False)
            init_role_head(self.panel.temp_head, None, infos.get('user_head', 30290006))
            self.last_show_idx = self.show_idx
            self.panel.lab_name.SetString(infos.get('user_name', ''))
            self.panel.nd_progress.setVisible(not self.check_display_video())
            self.panel.img_progress.SetPosition('50%', '100%')
            intro_item = self.panel.list_introduce.GetItem(0)
            intro_item.lab_describe.SetString(infos.get('work_introduce', ''))
            intro_item.lab_describe.formatText()
            sz = intro_item.lab_describe.GetTextContentSize()
            sz.height += 20
            old_sz = intro_item.getContentSize()
            intro_item.setContentSize(cc.Size(old_sz.width, sz.height))
            intro_item.RecursionReConfPosition()
            old_inner_size = self.panel.list_introduce.GetInnerContentSize()
            self.panel.list_introduce.SetInnerContentSize(old_inner_size.width, sz.height)
            self.panel.list_introduce.GetContainer()._refreshItemPos()
            self.panel.list_introduce._refreshItemPos()
            self.panel.list_introduce.jumpToTop()
            self.update_btn_like_state()
            self.update_like_num(uid)
            return

    def init_event(self):
        self.panel.btn_like.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_like())
        self.panel.btn_like.BindMethod('OnBegin', lambda btn, touch: self.on_hold_btn_like())
        self.panel.btn_like.BindMethod('OnEnd', lambda btn, touch: self.on_end_btn_like())
        self.panel.btn_question.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_question())
        self.panel.nd_drag.BindMethod('OnDrag', lambda btn, touch: self.on_drag_container(btn, touch))
        self.panel.nd_drag.BindMethod('OnEnd', lambda btn, touch: self.on_drag_end(btn, touch))
        self.panel.btn_close.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_close_read())
        for idx in range(len(self.reorder_list)):
            item = self.panel.list_dot.GetItem(idx)
            item.btn_dot.SetEnable(True)
            self.init_creator_page(idx)
            self.btn_play_dict[idx].BindMethod('OnClick', lambda btn, touch, idx=idx: self.on_click_btn_play(idx))
            self.btn_play_dict[idx].BindMethod('OnBegin', lambda btn, touch, idx=idx: self.on_hold_btn_play())
            self.btn_play_dict[idx].BindMethod('OnEnd', lambda btn, touch, idx=idx: self.on_end_btn_play())

    def process_events(self, is_bind):
        e_conf = {}
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def on_hold_btn_play(self):
        self.is_hold_btn_play = True

    def on_end_btn_play(self):
        self.is_hold_btn_play = False

    def on_hold_btn_like(self):
        self.is_hold_btn_like = True

    def on_end_btn_like(self):
        self.is_hold_btn_like = False

    def on_click_btn_play(self, idx):
        if self.show_idx != idx or not self.panel:
            return
        else:
            if not self.check_display_video(idx):
                self.can_drag_container = False
                self.btn_play_dict[idx].setVisible(False)
                self.panel.btn_close.setVisible(True)
                self.panel.nd_progress.setVisible(True)
            else:
                uid = self.reorder_list[idx]
                infos = self.creator_info.get(str(uid), None)
                self.video_url = infos.get('user_video', None)
                if self.video_url == None:
                    return
            self.is_play_video = True

            def func():
                if not self.video_url or self.video_player_widget is not None:
                    return
                else:
                    item = self.container.GetItem(idx)
                    item.img_cover.setVisible(False)
                    self.play_video_url = self.video_url
                    self.video_player_widget = VideoWindowCtrlUI(nd_video=self.panel.nd_video)
                    self.video_player_widget.set_end_cb(lambda item=item: self.on_close_video_play(item))
                    self.video_player_widget.set_close_cb(lambda item=item: self.on_close_video_play(item))
                    self.video_player_widget.play_vod(self.video_url)
                    return

            cur_type = network_utils.g93_get_network_type()
            if cur_type == network_utils.TYPE_MOBILE:
                SecondConfirmDlg2().confirm(content=get_text_by_id(607499), confirm_callback=func)
            else:
                func()
            last_time = self.last_play_time.get(self.show_uid, -1)
            if last_time == -1 or time_utility.get_server_time() - last_time > VIDEO_TIME_INTERVAL:
                self.last_play_time[last_time] = time_utility.get_server_time()
                micro_webservice_utils.micro_service_request('CreatorVideoService', {'req_type': 3,'video_id': self.show_uid}, None)
            return

    def update_like_num(self, uid, doc=None, cache_data=None):
        if not self.panel or not self.panel.isValid():
            return
        else:
            old_like_num = self.like_num_dict.get(str(uid), None)
            if old_like_num is None and doc is None:
                self.like_num_dict[str(uid)] = 0
                micro_webservice_utils.micro_service_request('CreatorVideoService', {'req_type': 2,'video_id': uid}, lambda doc, cache_data, uids=uid: self.update_like_num(uids, doc, cache_data))
            elif doc:
                self.like_num_dict[str(uid)] = int(doc.get('data', 0))
            self.panel.lab_like_num.SetString(str(self.like_num_dict[str(uid)]))
            return

    def update_btn_like_state(self):
        can_click = global_data.achi_mgr.get_cur_user_archive_data(ARCI_PRE_FIX.format(self.show_uid, global_data.player.id), False)
        if can_click:
            self.is_hold_btn_like = False
            self.panel.btn_like.SetEnable(False)
        else:
            self.panel.btn_like.SetEnable(True)

    def on_click_btn_like(self):
        if self.drag_selected_change or not self.panel:
            return
        else:
            self.like_num_dict[str(self.show_uid)] += 1
            global_data.achi_mgr.set_cur_user_archive_data(ARCI_PRE_FIX.format(self.show_uid, global_data.player.id), True)
            self.panel.btn_like.SetEnable(False)
            self.update_like_num(self.show_uid)
            micro_webservice_utils.micro_service_request('CreatorVideoService', {'req_type': 1,'video_id': self.show_uid}, None)
            return

    def on_click_btn_question(self):
        desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

    def on_click_btn_close_read(self):
        if not self.panel:
            return
        self.can_drag_container = True
        self.btn_play_dict[self.show_idx].setVisible(True)
        self.panel.btn_close.setVisible(False)
        self.panel.nd_progress.setVisible(False)

    def on_drag_end(self, layer, touch):
        if self.can_drag_container:
            start_pos = touch.getStartLocation()
            end_pos = touch.getLocation()
            self.drag_container_direction = end_pos.x - start_pos.x
            self.check_up_selected()

    def on_drag_container(self, layer, touch):
        if self.is_hold_btn_play or self.is_hold_btn_like or self.is_play_video:
            return
        self.drag_selected_change = True
        delta = touch.getDelta()
        if self.can_drag_container:
            cur_x, cur_y = self.container.GetPosition()
            new_x = cur_x + delta.x
            self.container.SetPosition(new_x, cur_y)
            start_pos = touch.getStartLocation()
            end_pos = touch.getLocation()
            self.drag_container_direction = end_pos.x - start_pos.x
            self.update_list_layout()
        else:
            text_item = self.container.GetItem(self.show_idx)
            parent_size = text_item.getContentSize()
            text_size = text_item.lab_describe.GetTextContentSize()
            per_percent_size = (text_size.height - parent_size.height) / 100.0
            if per_percent_size <= 0:
                return
            cur_x, cur_y = text_item.lab_describe.GetPosition()
            new_pos = cc.Vec2(cur_x, cur_y + delta.y)
            if new_pos.y < parent_size.height:
                new_pos.y = parent_size.height
            if new_pos.y > text_size.height:
                new_pos.y = text_size.height
            text_item.lab_describe.setPosition(new_pos)
            cur_offset = new_pos.y
            max_offset = text_size.height
            x, y = self.panel.img_progress.GetPosition()
            y = (1.0 - (cur_offset - parent_size.height) / max_offset) * 50 + 50
            self.panel.img_progress.SetPosition(x, '%f%%' % y)

    def on_drag_slider(self, ctrl, slider):
        pass

    def check_up_selected(self):
        if self.drag_show_idx != self.show_idx:
            if self.drag_show_idx >= len(self.reorder_list):
                return
            self.show_idx = self.drag_show_idx
        self.scroll_to_selected_item()

    def scroll_to_selected_item(self):
        self.drag_selected_change = True
        fixed_x, fixed_y = self.container.GetPosition()
        select_item_center_x = self.show_idx * self.item_width + 0.5 * self.item_width
        fixed_x = 0.5 * self.item_width - select_item_center_x
        self.container.stopAllActions()

        def scroll_end():
            if self.panel and self.panel.isValid():
                self.update_list_layout()
                self.refresh_page_info()
                self.drag_selected_change = False

        self.container.runAction(cc.Sequence.create([cc.MoveTo.create(0.5, cc.Vec2(fixed_x, fixed_y)), cc.CallFunc.create(scroll_end)]))

    def update_list_layout(self, is_drag=False):
        cur_x, cur_y = self.container.GetPosition()
        item_list = self.container.GetAllItem()
        min_dis_x = None
        for index, item in enumerate(item_list):
            item = self.container.GetItem(index)
            if self.drag_container_direction <= 0:
                dis_x = abs(cur_x + item.getPosition().x - self.item_width * item.getAnchorPoint().x + self.item_width / 8.0)
            else:
                dis_x = abs(cur_x + item.getPosition().x - self.item_width * item.getAnchorPoint().x + 7.0 * self.item_width / 8.0)
            if dis_x < self.item_width:
                min_dis_x = dis_x
                self.drag_show_idx = index

        self.container._refreshItemPos()
        return

    def check_display_video(self, idx=None):
        if not idx:
            idx = self.show_idx
        uid = self.reorder_list[idx]
        infos = self.creator_info.get(str(uid), None)
        if not infos:
            return False
        else:
            return 'user_video' in infos

    def check_can_circulate_page(self):
        return self.can_drag_container and not self.drag_selected_change and not self.is_hold_btn_play and not self.is_hold_btn_like and not self.is_play_video

    def circulate_display_page(self):
        if not self.container or self.container.IsDestroyed():
            return
        if not self.check_can_circulate_page():
            self.start_count = 0
            return
        self.start_count += 1
        if not self.start_count >= 4:
            return
        self.start_count = 0
        self.drag_show_idx += 1
        if self.drag_show_idx >= len(self.reorder_list):
            self.drag_show_idx = 0
        self.check_up_selected()

    def on_close_video_play(self, item):
        if item and item.isValid():
            item.img_cover.setVisible(True)
        self.is_play_video = False
        if self.video_player_widget:
            self.video_player_widget.close()
        self.video_player_widget = None
        return

    def on_finalize_panel(self):
        if self.video_player_widget:
            self.video_player_widget.close()
        self.panel = None
        self.process_events(False)
        self.btn_play_dict = {}
        self.last_play_time = {}
        self.like_num_dict = {}
        self.reorder_list = []
        self.video_url = None
        global_data.game_mgr.unregister_logic_timer(self.circulate_timer)
        if global_data.video_player.hashed_video_path == self.play_video_url:
            global_data.video_player.stop_video()
        return