# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivitySpringCustomsShare.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
import logic.gcommon.const as gconst
from logic.gutils import item_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
import logic.gcommon.time_utility as tutil
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW

class ActivitySpringCustomsShare(ActivityBase):

    def on_init_panel(self):
        self._act_ind = -1
        self.panel.btn_tips.BindMethod('OnClick', self.on_click_btn_tips)
        self.panel.btn_sendcard.btn_common.BindMethod('OnClick', self.on_click_sendcard_btn)
        self.panel.btn_download.BindMethod('OnClick', self.on_click_download_btn)
        conf = confmgr.get('c_activity_config', self._activity_type)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%m.%d', conf.get('cEndTime', 0))
        self.panel.lab_time.SetString(get_text_by_id(82193))
        self._last_open_activity = 0
        self.update_activity_show()
        self.set_cur_card(self._last_open_activity)
        photo_panel = self.panel.list_photo.GetContainer()
        ui_item = getattr(photo_panel, 'temp_card_%d' % (self._last_open_activity + 1))
        if ui_item:
            self.panel.list_photo.CenterWithNode(ui_item)
        self.init_task()
        self.process_event(True)
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(0.1, lambda : self.panel.PlayAnimation('loop'))

    def on_finalize_panel(self):
        super(ActivitySpringCustomsShare, self).on_finalize_panel()
        self.process_event(False)

    def update_activity_show(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        activity_list = conf.get('activity_list', [])
        photo_panel = self.panel.list_photo.GetContainer()
        act_len = len(activity_list)
        now = self.get_today()
        for i in range(0, 10):
            ui_item = getattr(photo_panel, 'temp_card_%d' % (i + 1))
            if i >= act_len:
                if ui_item:
                    ui_item.setVisible(False)
            else:
                act = activity_list[i]
                ui_item.img_card.SetDisplayFrameByPath('', act.get('pic', ''))
                begin_date = tutil.time_str_to_datetime(act.get('begin_date'), '%Y/%m/%d-%H:%M')
                is_open = now >= begin_date
                if not is_open:
                    if get_cur_text_lang() in (LANG_CN, LANG_ZHTW):
                        open_str = get_text_by_id(82199, {'date_name': get_text_by_id(act.get('date_name', '')),'hour': '%02d' % begin_date.hour,'min': '%02d' % begin_date.minute})
                    else:
                        open_str = get_text_by_id(82194, {'month': begin_date.month,'day': begin_date.day,'hour': '%02d' % begin_date.hour,
                           'min': '%02d' % begin_date.minute
                           })
                    ui_item.lab_empty.SetString(open_str)
                    ui_item.img_frame_3.setVisible(True)
                    ui_item.img_lock_3.setVisible(True)
                    ui_item.nd_empty.setVisible(True)
                    ui_item.img_bg_1.setVisible(False)
                    ui_item.img_bg_2.setVisible(False)
                    ui_item.img_frame_1.setVisible(False)
                    ui_item.lab_card_name.setVisible(False)

                    @ui_item.btn_card.callback()
                    def OnClick(btn, touch, act_ind=i):
                        global_data.game_mgr.show_tip(get_text_by_id(82195))

                else:
                    self._last_open_activity = i
                    ui_item.lab_card_name.SetString(act.get('name', ''))
                    ui_item.img_frame_3.setVisible(False)
                    ui_item.img_lock_3.setVisible(False)
                    ui_item.nd_empty.setVisible(False)
                    ui_item.img_bg_1.setVisible(True)
                    ui_item.img_bg_2.setVisible(False)
                    ui_item.img_frame_1.setVisible(True)
                    ui_item.lab_card_name.setVisible(True)

                    @ui_item.btn_card.callback()
                    def OnClick(btn, touch, act_ind=i):
                        self.set_cur_card(act_ind)

    def get_today(self):
        return tutil.get_utc8_datetime()

    def on_click_btn_tips(self, btn, touch):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        title, content = 860166, 860167
        dlg.set_show_rule(title, content)
        import cc
        dlg.set_node_pos(touch.getLocation(), cc.Vec2(0, 1))

    def get_open_card_list(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        activity_list = conf.get('activity_list', [])
        now = self.get_today()
        open_list = []
        for act in activity_list:
            begin_date = tutil.time_str_to_datetime(act.get('begin_date'), '%Y/%m/%d-%H:%M')
            is_open = now >= begin_date
            if is_open:
                open_list.append(act)

        return open_list

    def get_postmark_list(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        postmarks = conf.get('postmarks', [])
        return postmarks

    def on_click_sendcard_btn(self, btn, touch):
        from logic.comsys.activity.SpringFestival.SpringCardUI import SpringCardUI
        open_list = self.get_open_card_list()
        if not open_list:
            global_data.game_mgr.show_tip(get_text_by_id(82195))
            return
        ui = SpringCardUI()
        if ui:
            ui.set_postmark_list(self.get_postmark_list())
            ui.set_card_list(open_list)
            ui.set_card_index(self._act_ind)

    def on_click_download_btn(self, btn, touch):
        from logic.comsys.share.ShareManager import ShareManager
        from logic.gutils.share_utils import get_pc_share_save_path
        img_path = self.panel.img_card.GetDisplayFramePath()
        sz = self.panel.img_card.getContentSize()
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            pc_file_whole_path = get_pc_share_save_path()
        else:
            pc_file_whole_path = None

        def callback():
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                global_data.game_mgr.show_tip(get_text_by_id(920706, {'path': pc_file_whole_path}))

        ShareManager().save_to_gallery_ex(img_path, pc_file_whole_path, sz.width, sz.height, callback)
        return

    def set_cur_card(self, act_ind):
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        activity_list = conf.get('activity_list', [])
        if act_ind >= len(activity_list):
            return
        act = activity_list[act_ind]
        self.set_photo_item_sel(self._act_ind, False)
        self._act_ind = act_ind
        pic_path = act.get('pic', '')
        pic_path = pic_path.replace('_small_0', '_big')
        self.panel.img_card.SetDisplayFrameByPath('', pic_path)
        self.panel.lab_card_name.SetString(act.get('name', ''))
        self.set_photo_item_sel(self._act_ind, True)

    def set_photo_item_sel(self, ind, sel):
        photo_panel = self.panel.list_photo.GetContainer()
        ui_item = getattr(photo_panel, 'temp_card_%d' % (ind + 1))
        if ui_item:
            ui_item.img_bg_2.setVisible(sel)
            ui_item.img_bg_1.setVisible(not sel)

    def init_task(self):
        task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.task_id = task_id
        self.init_ui_event()
        self.update_reward()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_task_updated
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_ui_event(self):

        @self.panel.temp_reward.btn_choose.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if player.has_unreceived_task_reward(self.task_id):
                player.receive_task_reward(self.task_id)
            elif not player.has_receive_reward(self.task_id):
                from logic.gutils import task_utils
                x, y = btn.GetPosition()
                wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                reward_id = task_utils.get_task_reward(self.task_id)
                reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)
            elif player.has_receive_reward(self.task_id):
                global_data.game_mgr.show_tip(get_text_by_id(606046))

    def on_task_updated(self, task_id, *args):
        if task_id != self.task_id:
            return
        self.update_reward()
        player = global_data.player
        if player.has_unreceived_task_reward(self.task_id):
            player.receive_task_reward(self.task_id)

    def update_reward(self):
        player = global_data.player
        if not player:
            return
        if player.has_receive_reward(self.task_id):
            self.panel.temp_reward.nd_get.setVisible(True)
            self.panel.temp_reward.nd_get_tips.setVisible(False)
        else:
            self.panel.temp_reward.nd_get.setVisible(False)
            if player.has_unreceived_task_reward(self.task_id):
                self.panel.temp_reward.nd_get_tips.setVisible(True)
            else:
                self.panel.temp_reward.nd_get_tips.setVisible(False)