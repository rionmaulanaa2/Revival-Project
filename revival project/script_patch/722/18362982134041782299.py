# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/FreeRecordUI.py
from __future__ import absolute_import
import cc
import os
import time
from common.utils import timer
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER, UI_VKB_NO_EFFECT, UI_TYPE_SPECIAL
from logic.comsys.video.VideoRecord import VideoRecord
from logic.comsys.video.video_record_utils import FREE_RECORD_PATH
from logic.gcommon.time_utility import get_server_time
from logic.client.path_utils import RECORD_FRAME, RECORDING_FRAME, RECORD_MY_VIDEO_FRAME
STATE_SHOW = 0
STATE_HIDE = 1
MIN_SECONDS = 1.5

class FreeRecordUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_highlight/btn_record'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_SPECIAL
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self._timer = None
        self._timer_time = 0
        self._is_recording = False
        self._recording_path = None
        self.panel.record_num.setVisible(False)
        self._move_start_pos = None
        self._start_pos = None
        self._state = None
        self._init_record_btn()
        return

    def _init_record_btn(self):
        self.panel.lv_btn_list.SetInitCount(1)
        self._record_item = self.panel.lv_btn_list.GetItem(0)
        self._record_item.lab_name.SetString(3138)
        self._record_item.img_icon.SetDisplayFrameByPath('', RECORD_FRAME)
        self._play_show_anim()

        @self._record_item.btn_video.unique_callback()
        def OnClick(btn, touch):
            self._play_show_anim()
            self.panel.lv_btn_list.SetInitCount(1)
            if self._is_recording:
                VideoRecord().stop_free_record()
                self.panel.nd_mask.setVisible(False)
                self.panel.record_num.setVisible(False)
                self._clear_timer()
            else:
                now_time = int(get_server_time())
                self._recording_path = os.path.join(FREE_RECORD_PATH, '{}.mp4'.format(now_time))
                if VideoRecord().free_record(self._recording_path, on_start_cb=self._on_record_start, on_stop_cb=self._on_record_stop):
                    self.panel.nd_mask.setVisible(True)

        @self.nd_drag.unique_callback()
        def OnBegin(layer, touch):
            self.panel.stopAllActions()
            self._play_show_anim(schedule=False)
            self._move_start_pos = touch.getLocation()
            self._start_pos = self.panel.getParent().convertToWorldSpace(self.panel.getPosition())

        @self.nd_drag.unique_callback()
        def OnDrag(layer, touch):
            w_pos = touch.getLocation()
            w_pos.subtract(self._move_start_pos)
            w_pos.add(self._start_pos)
            self.panel.setPosition(self._boundary_check(w_pos))

        @self.nd_drag.unique_callback()
        def OnEnd(layer, touch):
            self._play_show_anim()

    def _boundary_check(self, w_pos):

        def PointCheck(p_node, pt, left_xb, right_xb, bottom_yb, up_yb):
            p = p_node.convertToNodeSpace(pt)
            c_size_node = p_node.getContentSize()
            l_pos_x = max(min(c_size_node.width - right_xb, p.x), left_xb)
            l_pos_y = max(min(c_size_node.height - up_yb, p.y), bottom_yb)
            return cc.Vec2(l_pos_x, l_pos_y)

        sz = self.panel.getContentSize()
        anchor = self.panel.getAnchorPoint()
        left_boundary = sz.width * anchor.x
        right_boundary = sz.width * (1 - anchor.x)
        bottom_boundary = sz.height * anchor.y
        up_boundary = sz.height * (1 - anchor.y)
        node = self.panel.getParent()
        return PointCheck(node, w_pos, left_boundary, right_boundary, bottom_boundary, up_boundary)

    def _on_record_start(self, ret, record_path):
        if record_path != self._recording_path:
            return
        self._is_recording = True
        self._timer_time = time.time()
        self.panel.record_num.setVisible(True)
        self.panel.nd_time.SetString('00:00')
        item = self.panel.lv_btn_list.GetItem(0)
        item.img_icon.SetDisplayFrameByPath('', RECORDING_FRAME)
        self._timer = global_data.game_mgr.register_logic_timer(self._on_timer_update, interval=1, times=-1, mode=timer.CLOCK)

    def _on_record_stop(self, ret, record_path):
        if record_path != self._recording_path:
            return
        self._is_recording = False
        in_battle = global_data.player and global_data.player.is_in_battle()
        item = self.panel.lv_btn_list.GetItem(0)
        item.img_icon.SetDisplayFrameByPath('', RECORD_FRAME)
        if not in_battle and ret:
            self.panel.lv_btn_list.SetInitCount(2)
            item = self.panel.lv_btn_list.GetItem(1)
            item.img_res.setVisible(True)
            item.img_icon.SetDisplayFrameByPath('', RECORD_MY_VIDEO_FRAME)

            @item.btn_video.unique_callback()
            def OnClick(btn, touch, v_item=item):
                from logic.comsys.setting_ui.MyVideoUI import MyVideoUI
                v_item.img_res.setVisible(False)
                MyVideoUI(None, 1)
                return

        text_id = 3139 if ret else 3140
        global_data.game_mgr.show_tip(get_text_by_id(text_id))

    def _on_timer_update(self, *args):
        interval = time.time() - self._timer_time
        minutes = int(interval / 60.0)
        seconds = int(interval - minutes * 60)
        self.panel.nd_mask.setVisible(interval <= MIN_SECONDS)
        self.panel.nd_time.SetString('%02d:%02d' % (minutes, seconds))

    def _schedule_to_hide(self):
        self.panel.stopAllActions()

        def cb(*args):
            self._state = STATE_HIDE
            self.panel.PlayAnimation('hide')

        self.panel.SetTimeOut(2, cb)

    def _play_show_anim(self, schedule=True):
        if self._state == STATE_HIDE:
            self._state = STATE_SHOW
            self.panel.PlayAnimation('show')
        if schedule:
            self._schedule_to_hide()

    def _clear_timer(self):
        self.panel.nd_mask.setVisible(False)
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        return

    def on_finalize_panel(self):
        if self._is_recording:
            VideoRecord().stop_free_record(need_save=False)
        self._clear_timer()