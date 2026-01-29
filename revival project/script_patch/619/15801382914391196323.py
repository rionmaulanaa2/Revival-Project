# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLineBinding.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
REWARD_ST_2_TEXT_ID = {ITEM_RECEIVED: 80866,
   ITEM_UNRECEIVED: 80248,
   ITEM_UNGAIN: 80540
   }

class ActivityLineBinding(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityLineBinding, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def on_init_panel(self):
        global_data.achi_mgr.set_cur_user_archive_data('ACTIVITY_BINDING_LINE_RP', 1)
        self.init_reward_widget()
        self.init_art_text()
        self.update_btn()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_widget,
           'on_bind_channel_event': self.on_bind_linegame_succ
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_reward_widget(self):
        reward_id = task_utils.get_task_reward(self.task_id)
        init_common_reward_list(self.panel.list_items, reward_id)
        self.update_widget()
        self.on_bind_linegame_succ()

        @self.panel.btn_yellow.unique_callback()
        def OnClick(*args):
            self.on_click_btn()

    def init_art_text(self):
        login_country = global_data.player.get_login_country()
        if login_country == 'TH':
            tips_pic = 'gui/ui_res_2/txt_pic/text_pic_th/activity_202107/img_smalltext.png'
            title_pic = 'gui/ui_res_2/txt_pic/text_pic_th/activity_202107/img_title.png'
            btn_pic = 'gui/ui_res_2/txt_pic/text_pic_th/activity_202107/btn_line_point.png'
        elif login_country == 'ID':
            tips_pic = 'gui/ui_res_2/txt_pic/text_pic_in/activity202107/img_smalltext.png'
            title_pic = 'gui/ui_res_2/txt_pic/text_pic_in/activity202107/img_title.png'
            btn_pic = 'gui/ui_res_2/txt_pic/text_pic_in/activity202107/btn_line_point.png'
        else:
            tips_pic = 'gui/ui_res_2/txt_pic/text_pic_th/activity_202107/img_smalltext.png'
            title_pic = 'gui/ui_res_2/txt_pic/text_pic_th/activity_202107/img_title.png'
            btn_pic = 'gui/ui_res_2/txt_pic/text_pic_th/activity_202107/btn_line_point.png'
        self.panel.img_tips.SetDisplayFrameByPath('', tips_pic)
        self.panel.img_title.SetDisplayFrameByPath('', title_pic)
        self.panel.btn_yellow.SetFrames('', [btn_pic, btn_pic, btn_pic], False, None)
        return

    def update_widget(self, *args):
        self.update_reward()
        self.update_btn()

    def update_reward(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if not (self.panel and self.panel.isValid()):
            return
        all_items = self.panel.list_items.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def update_btn(self):
        pass

    def on_click_btn(self, *args):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if reward_status == ITEM_UNGAIN:
            global_data.channel.bind_linegame()
        elif reward_status == ITEM_UNRECEIVED:
            global_data.player.receive_task_reward(self.task_id)
        elif reward_status == ITEM_RECEIVED:
            pass

    def on_bind_linegame_succ(self, *args):
        is_bind = global_data.channel.is_bind_linegame()
        if is_bind:
            global_data.player.call_server_method('bind_linegame', ())