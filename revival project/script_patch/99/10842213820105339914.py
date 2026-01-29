# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKaixue/ActivityKaixueComicShare.py
from __future__ import absolute_import
import six
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
import cc
OPEN_SAVE_KEY = [
 '2021_kaixue_comic_0', '2021_kaixue_comic_1', '2021_kaixue_comic_2', '2021_kaixue_comic_3']
IMG_BOOK_OPEN_PRE = 'gui/ui_res_2/activity/activity_202109/i_activity_term/book/'
IMG_BOOK_UNOPEN = 'gui/ui_res_2/activity/activity_202109/i_activity_term/book/img_cover1.png'

class ActivityKaixueComicShare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKaixueComicShare, self).__init__(dlg, activity_type)
        self.parent_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.children_task_list = task_utils.get_children_task(self.parent_task_id)
        self.ui_data = confmgr.get('c_activity_config', activity_type).get('cUiData')
        self._timer = 0
        self._timer_cb = {}
        self.register_timer()

    def on_init_panel(self):
        self.process_event(True)
        self.init_time_widget()
        for idx in range(4):
            self.init_comic_widget(idx)

        self.init_nd_riko()
        self.reorder_comic_zorder()

    def on_finalize_panel(self):
        self.process_event(False)
        self.children_task_list = []
        self.unregister_timer()

    def set_show(self, show, is_init=False):
        super(ActivityKaixueComicShare, self).set_show(show, is_init)
        self.panel.PlayAnimation('show')
        if self.is_all_book_shared():
            self.panel.PlayAnimation('tips')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'comic_book_ui_close_event': self.on_close_comic_book_ui,
           'receive_task_reward_succ_event': self.update_comic_widget,
           'task_prog_changed': self.on_update_panel
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=5, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def refresh_time(self):
        lab_time = self.panel.nd_middle.nd_title.vx_mask_04.lab_time.lab_time_02
        left_time = task_utils.get_raw_left_open_time(self.parent_task_id)
        day, hour, minute, second = tutil.get_day_hour_minute_second(left_time)
        if left_time > 0:
            if day > 0:
                lab_time.SetString(get_text_by_id(907135).format(day))
            elif hour > 0:
                lab_time.SetString(get_text_by_id(609895).format(n=hour))
            else:
                lab_time.SetString(get_text_by_id(609895).format(n=1))
        else:
            lab_time.SetString(lab_time.SetString(get_text_by_id(609895).format(n=0)))

    def on_update_panel(self, *args):
        for idx in range(4):
            self.update_comic_widget(self.children_task_list[idx])

        self.init_nd_riko()

    def init_time_widget(self):
        self._timer_cb[0] = lambda : self.refresh_time()
        self.refresh_time()

    def init_comic_widget(self, idx):
        task_id = self.children_task_list[idx]
        is_in_time = task_utils.is_task_open(task_id)
        is_opened = global_data.achi_mgr.get_cur_user_archive_data(OPEN_SAVE_KEY[idx], default=0) == 1
        is_shared = global_data.player.is_task_finished(task_id)
        img_book_open = IMG_BOOK_OPEN_PRE + self.ui_data.get('img_book')[idx]
        img_book = img_book_open if is_opened else IMG_BOOK_UNOPEN
        open_time = task_utils.get_task_start_time_str(task_id)
        comic_node = getattr(self.panel.nd_middle, 'temp_book_0%s' % (idx + 1))
        btn_book = comic_node.btn_book
        btn_book.nd_comic.setVisible(is_opened)
        btn_book.nd_bookcover.img_bookcover.SetDisplayFrameByPath('', img_book)
        btn_book.nd_bookcover.lab_num_01.SetString('0%s' % (idx + 1))
        btn_book.nd_comic.nd_low.lab_num_02.SetString('0%s' % (idx + 1))
        btn_book.nd_bookcover.setVisible(not is_opened)
        btn_book.nd_tips.img_tips_unlock.setVisible(not is_in_time)
        btn_book.nd_tips.img_tips_activate.setVisible(is_in_time and not is_shared)
        btn_book.nd_tips.img_box.setVisible(not is_shared)
        btn_book.nd_tips.lab_share.setVisible(not is_shared)
        share_text = is_in_time or open_time if 1 else 907133
        btn_book.nd_tips.lab_share.SetString(share_text)
        if is_in_time and not is_shared:
            comic_node.PlayAnimation('loop')
        else:
            comic_node.StopAnimation('loop')

        @btn_book.unique_callback()
        def OnClick(btn, touch, _idx=idx, _task_id=task_id, _node=comic_node):
            self.on_click_btn_book(_idx, _task_id, _node)

    def update_comic_widget(self, task_id):
        if task_id not in self.children_task_list:
            return
        is_in_time = task_utils.is_task_open(task_id)
        idx = self.children_task_list.index(task_id)
        is_opened = global_data.achi_mgr.get_cur_user_archive_data(OPEN_SAVE_KEY[idx], default=0) == 1
        is_shared = global_data.player.is_task_finished(task_id)
        img_book_open = IMG_BOOK_OPEN_PRE + self.ui_data.get('img_book')[idx]
        img_book = img_book_open if is_opened else IMG_BOOK_UNOPEN
        comic_node = getattr(self.panel.nd_middle, 'temp_book_0%s' % (idx + 1))
        btn_book = comic_node.btn_book
        btn_book.nd_comic.setVisible(is_opened)
        btn_book.nd_bookcover.img_bookcover.SetDisplayFrameByPath('', img_book)
        btn_book.nd_bookcover.setVisible(not is_opened)
        btn_book.nd_tips.img_tips_unlock.setVisible(not is_in_time)
        btn_book.nd_tips.img_tips_activate.setVisible(is_in_time and not is_shared)
        btn_book.nd_tips.img_box.setVisible(not is_shared)
        btn_book.nd_tips.lab_share.setVisible(not is_shared)
        open_time = task_utils.get_task_start_time_str(task_id)
        share_text = is_in_time or open_time if 1 else 907133
        btn_book.nd_tips.lab_share.SetString(share_text)
        if is_in_time and not is_shared:
            comic_node.PlayAnimation('loop')
        else:
            comic_node.StopAnimation('loop')
        self.init_nd_riko()
        self.reorder_comic_zorder()

    def on_close_comic_book_ui(self, task_id):
        self.update_comic_widget(task_id)

    def init_nd_riko(self):
        if self.is_all_book_shared():
            self.panel.nd_middle.nd_riko.setVisible(True)
            self.panel.nd_middle.nd_riko.setLocalZOrder(5)
        else:
            self.panel.nd_middle.nd_riko.setVisible(False)

    def on_click_btn_book(self, idx, task_id, node):
        node.PlayAnimation('click')
        if not task_utils.is_task_open(task_id):
            open_time = task_utils.get_task_start_time_str(task_id)
            global_data.game_mgr.show_tip(get_text_by_id(607967).format(open_time))
            return
        ui = global_data.ui_mgr.show_ui('ComicBookUI', 'logic.comsys.activity.ActivityKaixue')
        ui.set_book_content(idx, task_id)
        global_data.achi_mgr.set_cur_user_archive_data(OPEN_SAVE_KEY[idx], 1)

    def reorder_comic_zorder(self):

        def cmp_func(task_id_a, task_id_b):
            in_time_a = task_utils.is_task_open(task_id_a)
            in_time_b = task_utils.is_task_open(task_id_b)
            if in_time_a != in_time_b:
                if in_time_a:
                    return -1
                if in_time_b:
                    return 1
            shared_a = global_data.player.is_task_finished(task_id_a)
            shared_b = global_data.player.is_task_finished(task_id_b)
            if shared_a != shared_b:
                if not shared_a:
                    return -1
                if not shared_b:
                    return 1
            return 0

        sorted_tasks = sorted(self.children_task_list, key=cmp_to_key(cmp_func))
        for idx in range(4):
            comic_node = getattr(self.panel.nd_middle, 'temp_book_0%s' % (idx + 1))
            task_id = self.children_task_list[idx]
            z_order = 4 - sorted_tasks.index(task_id)
            comic_node.setLocalZOrder(z_order)

    def is_all_book_shared(self):
        return global_data.player and global_data.player.is_task_finished(self.parent_task_id)