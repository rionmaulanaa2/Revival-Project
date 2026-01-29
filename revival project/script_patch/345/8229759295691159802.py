# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeixinBinding.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils.share_utils import share_wx_mini_program
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.comsys.activity.TeachingStepsUI import TeachingStepsUI
from logic.comsys.activity.WeixinBindingCodeUI import WeixinBindingCodeUI
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.platform.dctool import interface
import hashlib
SIGN_KEY = '8x1d76p5fc6e41b'
GRAY_BTN_ICON = 'gui/ui_res_2_cn/activity/activity_202012/weibo_btn02.png'

class ActivityWeixinBinding(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWeixinBinding, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.user_name = 'gh_192ff7bcf5f9'
        self.player_name_need_escape = True
        self.player_name_in_sign_need_escape = False
        self.mini_program_path = self.get_mini_program_path()
        self.mini_program_type = global_data.player.get_mini_program_type()

    def on_init_panel(self):
        self.init_reward_widget()
        self.update_reward_widget()
        self.init_all_btns()
        self.update_all_btn_visible()
        self.process_event(True)
        self.panel.PlayAnimation('appear')
        global_data.player.call_server_method('req_check_wechat_bind_state', ())

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_update_task_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_reward_widget(self):
        reward_id = task_utils.get_task_reward(self.task_id)
        init_common_reward_list(self.panel.list_award, reward_id)

    def init_all_btns(self):

        @self.panel.btn_auto.unique_callback()
        def OnClick(btn, touch):
            self.mini_program_path = self.get_mini_program_path()
            share_wx_mini_program(self.user_name, self.mini_program_path, self.mini_program_type)

        @self.panel.btn_manual.unique_callback()
        def OnClick(btn, touch):
            if global_data.player:
                global_data.player.call_server_method('req_wechat_bind_code', ())
            WeixinBindingCodeUI()

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
            TeachingStepsUI(content_dict=ui_data)

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_task_reward(self.task_id)

    def update_all_btn_visible(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        self.panel.btn_auto.setVisible(reward_status != ITEM_UNRECEIVED)
        self.panel.btn_manual.setVisible(reward_status != ITEM_UNRECEIVED)
        self.panel.btn_get.setVisible(reward_status == ITEM_UNRECEIVED)
        self.panel.btn_get.SetEnable(reward_status == ITEM_UNRECEIVED)
        if reward_status == ITEM_UNRECEIVED:
            self.panel.btn_get.SetText(get_text_by_id(80248))
        if reward_status == ITEM_RECEIVED:
            self.panel.btn_auto.SetText(get_text_by_id(606302))
            self.panel.btn_manual.SetText(get_text_by_id(606303))
            self.panel.btn_auto.SetFrames('', [GRAY_BTN_ICON, GRAY_BTN_ICON, GRAY_BTN_ICON], False, None)
            self.panel.btn_manual.SetFrames('', [GRAY_BTN_ICON, GRAY_BTN_ICON, GRAY_BTN_ICON], False, None)
        return

    def update_reward_widget(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if not (self.panel and self.panel.isValid()):
            return
        all_items = self.panel.list_award.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def on_update_task_progress(self, *args):
        self.update_all_btn_visible()
        self.update_reward_widget()

    def set_username(self, name):
        self.user_name = name

    def set_mini_program_path(self, path):
        self.mini_program_path = path

    def set_mini_program_type(self, type):
        self.mini_program_type = type

    def get_mini_program_path(self):
        if not global_data.player:
            return ''
        player = global_data.player
        if self.player_name_in_sign_need_escape:
            player_name_in_sign = player.get_name().encode('unicode-escape')
        else:
            player_name_in_sign = player.get_name()
        input_params = {'role_id': player.uid,
           'role_name': player_name_in_sign,
           'role_avatar_url': player.get_head_photo_url(),
           'server': interface.get_server_name(),
           'server_id': global_data.channel._hostnum
           }
        path_sign = self.get_mini_program_path_sign(input_params, SIGN_KEY)
        if self.player_name_need_escape:
            player_name = player.get_name().encode('unicode-escape')
        else:
            player_name = player.get_name()
        return 'pages/main/main?role_id={role_id}&role_name={role_name}&role_avatar_url={role_avatar_url}&server={server}&server_id={server_id}&key={key}'.format(role_id=player.uid, role_name=player_name, role_avatar_url=player.get_head_photo_url(), server=interface.get_server_name(), server_id=global_data.channel._hostnum, key=path_sign)

    @staticmethod
    def get_mini_program_path_sign(input_params, key):
        sign_string = []
        for k, v in sorted(six_ex.items(input_params)):
            sign_string.append(str(k))
            sign_string.append(str(v).decode('utf-8').encode('utf-8'))

        sign_string.append(key)
        sign_md5 = hashlib.md5()
        import six
        sign_md5.update(six.ensure_binary(''.join(sign_string)))
        sign = sign_md5.hexdigest().upper()
        return sign