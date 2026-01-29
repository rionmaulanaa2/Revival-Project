# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCalendarBase.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gutils.jump_to_ui_utils import jump_to_activity, jump_to_lottery
from logic.gutils.activity_utils import get_activity_state, get_lottery_state, ACTIVITY_STATE_NOT_OPEN, ACTIVITY_STATE_OPENING, ACTIVITY_STATE_END, get_activity_open_time_format, get_lottery_open_time_format
from logic.gutils import jump_to_ui_utils

class ActivityCalendarBase(object):
    BTN_INFO_LIST = {}
    BTN_INFO_LIST_ALT = {}
    BTN_PREFIX = 'btn_item%d'
    LAB_NAME = 'lab_name%d'
    LAB_TIME = 'lab_time%d'
    ACTIVITY_ID = None
    SHARE_TASK_ID = None
    SHARE_CREATOR = None
    SHARE_NEED_BLACK_BG = True
    SHARE_ARGS = {}

    def __init__(self, panel, jump_cb=None, play_animation=True, accept_event=True, activity_type=None):
        super(ActivityCalendarBase, self).__init__()
        self.panel = panel
        self.jump_cb = jump_cb
        if activity_type:
            self.ACTIVITY_ID = activity_type
        if self.ACTIVITY_ID:
            activity_conf = confmgr.get('c_activity_config', self.ACTIVITY_ID, default={})
            task_id = activity_conf.get('cTask', None)
            if task_id is not None:
                self.SHARE_TASK_ID = task_id
            ui_data = activity_conf.get('cUiData', {})
            btn_info = ui_data.get('btn_info', None)
            if btn_info and isinstance(btn_info, dict):
                for idx, value in six.iteritems(btn_info):
                    if not idx.isdigit():
                        continue
                    self.BTN_INFO_LIST[int(idx)] = value

            btn_info_alt = ui_data.get('btn_info_alt', None)
            if btn_info_alt and isinstance(btn_info_alt, dict):
                for idx, value in six.iteritems(btn_info_alt):
                    if not idx.isdigit():
                        continue
                    self.BTN_INFO_LIST_ALT[int(idx)] = value

        if self.need_alt_btn():
            self.BTN_INFO_LIST.update(self.BTN_INFO_LIST_ALT)
        self.enable_share = hasattr(self.panel, 'nd_share')
        self.share_id = 'activity_' + self.ACTIVITY_ID
        self.refresh_share()
        self.init_panel()
        if play_animation:
            self.play_show_animation()
        accept_event and self.process_event(True)
        return

    def destroy(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if self.enable_share:
            econf.update({'receive_task_reward_succ_event': self.refresh_share
               })
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def need_alt_btn(self):
        return G_IS_NA_PROJECT

    def init_panel(self):
        for idx in six.iterkeys(self.BTN_INFO_LIST):
            self.init_btn_by_idx(idx)

        nd_share = getattr(self.panel, 'nd_share', None)
        if nd_share and nd_share.btn_share:
            nd_share.setVisible(self.enable_share)
            nd_share.btn_share.BindMethod('OnClick', self._share)
        btn_question = getattr(self.panel, 'btn_question', None)
        conf = confmgr.get('c_activity_config', self.ACTIVITY_ID, default={})
        if btn_question and conf:
            btn_question.BindMethod('OnClick', lambda btn, touch: global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui').set_show_rule(int(conf['cNameTextID']), int(conf['cDescTextID']) if conf['cDescTextID'].isdigit() else conf['cDescTextID']))
        return

    def _share(self, *args):
        if not self.enable_share or self.SHARE_CREATOR is None:
            return
        else:
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI(parent=self.panel, need_black_bg=self.SHARE_NEED_BLACK_BG)

            def init_cb():
                if share_ui and share_ui.is_valid():
                    if hasattr(self._share_content, 'get_show_render_texture'):
                        share_ui.set_save_content(self._share_content.get_save_render_texture())
                        share_ui.set_share_content_raw(self._share_content.get_show_render_texture(), need_scale=True, share_content=self._share_content)
                    else:
                        share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

                    def share_inform_func():
                        if global_data.player:
                            global_data.player.share_activity('activity_' + str(self.ACTIVITY_ID))
                            global_data.player.share()
                        self.refresh_share()

                    share_ui.set_share_inform_func(share_inform_func)

            if not getattr(self, '_share_content', None):
                self._share_content = self.SHARE_CREATOR(**self.SHARE_ARGS)
                self._share_content.create(parent=None, init_cb=init_cb)
            else:
                init_cb()
            return

    def refresh_share(self, *args):
        if not self.enable_share:
            return
        if global_data.player.has_unreceived_task_reward(self.SHARE_TASK_ID):
            global_data.player.receive_task_reward(self.SHARE_TASK_ID)
        self._refresh_share_btn(global_data.player.has_receive_reward(self.SHARE_TASK_ID))

    def _refresh_share_btn(self, has_shared):
        lab_share = getattr(self.panel, 'lab_share', None)
        lab_share and lab_share.SetString(603013 if has_shared else 609717)
        return

    def init_btn_by_idx(self, idx):
        btn_item = getattr(self.panel, self.BTN_PREFIX % idx, None)
        if not btn_item:
            return
        else:
            item_info = self.BTN_INFO_LIST[idx]
            name_id = item_info.get('name_id', None)
            activity_id = item_info.get('activity_id', None)
            if not name_id and activity_id:
                name_id = confmgr.get('c_activity_config', str(activity_id), 'cNameTextID', default=None)
                if name_id:
                    name_id = int(name_id)
            lottery_id = item_info.get('lottery_id', None)
            if not name_id and lottery_id:
                name_id = confmgr.get('lottery_page_config', str(lottery_id), 'text_id', default=None)
            lab_name = btn_item.lab_name
            if hasattr(self.panel, self.LAB_NAME % idx):
                lab_name = getattr(self.panel, self.LAB_NAME % idx)
            name_id is not None and lab_name.SetString(name_id)
            date_text = item_info.get('date', None)
            lab_time = btn_item.lab_time
            if hasattr(self.panel, self.LAB_TIME % idx):
                lab_time = getattr(self.panel, self.LAB_TIME % idx)
            if not date_text:
                if activity_id:
                    date_text = get_activity_open_time_format(activity_id)
                elif lottery_id:
                    date_text = get_lottery_open_time_format(lottery_id)
            date_text is not None and lab_time.SetString(date_text)
            btn_state = self.get_item_state(idx)
            self.init_btn_state_by_idx(idx, btn_item, btn_state)
            alt_pic = item_info.get('pic_path', None)
            img_item = getattr(btn_item, 'img_item', None)
            img_item and alt_pic and img_item.SetDisplayFrameByPath('', alt_pic)
            btn_item.BindMethod('OnClick', lambda btn, touch, idx=idx: self.on_btn_item_clicked(btn, touch, idx))
            return (
             btn_item, item_info)

    def init_btn_state_by_idx(self, idx, btn, state):
        if state == ACTIVITY_STATE_END:
            lab_time = btn.lab_time
            if hasattr(self.panel, self.LAB_TIME % idx):
                lab_time = getattr(self.panel, self.LAB_TIME % idx)
            lab_time.SetString(601214)

    def play_show_animation(self):
        self.panel.PlayAnimation('show')

    def on_btn_item_clicked(self, btn, touch, idx):
        activity_state = self.get_item_state(idx)
        if activity_state == ACTIVITY_STATE_NOT_OPEN:
            global_data.game_mgr.show_tip(get_text_by_id(10063))
        elif activity_state == ACTIVITY_STATE_END:
            global_data.game_mgr.show_tip(get_text_by_id(601214))
        elif activity_state == ACTIVITY_STATE_OPENING:
            self.jump_from_item(idx)

    def jump_from_item(self, idx):
        item_info = self.BTN_INFO_LIST[idx]
        jump_func = item_info.get('jump_func', None)
        jump_args = item_info.get('jump_args', [])
        activity_id = item_info.get('activity_id', None)
        lottery_id = item_info.get('lottery_id', None)
        tip_id = item_info.get('click_tip_id', None)
        jump_out = False
        if jump_func:
            func = getattr(jump_to_ui_utils, jump_func)
            if func:
                func(*jump_args)
        elif activity_id:
            jump_to_activity(str(activity_id))
            jump_out = True
        elif lottery_id:
            jump_to_lottery(str(lottery_id))
            jump_out = True
        elif tip_id:
            global_data.game_mgr.show_tip(get_text_by_id(tip_id))
        if jump_out and callable(self.jump_cb):
            self.jump_cb()
        return

    def get_item_state(self, idx):
        item_info = self.BTN_INFO_LIST[idx]
        valid_time = item_info.get('valid_time', None)
        if valid_time:
            from logic.gcommon.time_utility import get_server_time
            cur_time = get_server_time()
            begin_time, end_time = valid_time
            if cur_time < begin_time:
                return ACTIVITY_STATE_NOT_OPEN
            else:
                if cur_time <= end_time:
                    return ACTIVITY_STATE_OPENING
                return ACTIVITY_STATE_END

        activity_id = item_info.get('activity_id', None)
        lottery_id = item_info.get('lottery_id', None)
        if activity_id:
            return get_activity_state(activity_id)
        else:
            if lottery_id:
                return get_lottery_state(lottery_id)
            return ACTIVITY_STATE_NOT_OPEN
            return

    def on_finalize_panel(self):
        self.process_event(False)