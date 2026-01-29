# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeixinRedEnvelopes.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils.share_utils import share_wx_mini_program, get_mini_program_path_sign
from logic.gcommon import const
from common.platform.dctool import interface
from logic.gcommon import time_utility as tutil
from logic.gutils import role_head_utils
from logic.gutils.live_utils import format_one_line_text
from logic.gcommon.common_const import activity_const as acconst
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import time
SIGN_KEY = '3d95d926-ba78-42d1-b3a9-a5cdbd6c0e06'

class ActivityWeixinRedEnvelopes(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWeixinRedEnvelopes, self).__init__(dlg, activity_type)
        self.user_name = 'gh_0b25d6343035'
        self.mini_program_path = self.get_mini_program_path()
        self.mini_program_type = '0'
        self.process_event(True)

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}

    def on_init_panel(self):
        player = global_data.player
        if player:
            red_envelope_teammate_uids, _, _ = player.get_red_envelope_state()
            global_data.player.request_players_detail_inf(red_envelope_teammate_uids)
        self.panel.PlayAnimation('show')
        self.init_parameters()
        self.init_btns()

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        self.register_timer()
        self._timer_cb[0] = lambda : self.refresh_spring_envelope_time()
        self.refresh_spring_envelope_time()
        self._timer_cb[1] = lambda : self.refresh_red_envelope_time()
        self.refresh_red_envelope_time()
        self.panel.list_head.SetInitCount(3)
        self.update_spring_envelope()
        self.update_red_envelope()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        del_keys = []
        for key, cb in six.iteritems(self._timer_cb):
            result = cb()
            if result == -1:
                del_keys.append(key)

        for key in del_keys:
            del self._timer_cb[key]

    def get_spring_envelope_left_time(self):
        player = global_data.player
        if not player:
            return (-1, -1)
        return player.get_spring_envelope_left_time()

    def refresh_spring_envelope_time(self):
        start_left_time, end_left_time = self.get_spring_envelope_left_time()
        if start_left_time > 0:
            self.panel.btn_open1.lab_time_limit1.setVisible(True)
            self.panel.btn_open1.lab_time_limit1.SetString(tutil.get_readable_time_2(start_left_time))
        elif end_left_time > 0:
            if not self.panel.btn_open1.btn_common.IsEnable():
                self.panel.btn_open1.lab_time_limit1.setVisible(False)
                self.update_spring_envelope()
        else:
            self.panel.btn_open1.lab_time_limit1.setVisible(False)
            self.update_spring_envelope()
            return -1

    def get_red_envelope_left_time(self):
        player = global_data.player
        if not player:
            return (-1, -1)
        return player.get_red_envelope_left_time()

    def refresh_red_envelope_time(self):
        start_left_time, end_left_time = self.get_red_envelope_left_time()
        if start_left_time > 0:
            self.panel.btn_open2.lab_time_limit1.setVisible(True)
            self.panel.btn_open2.lab_time_limit1.SetString(tutil.get_readable_time_2(start_left_time))
        elif end_left_time > 0:
            self.panel.btn_open2.lab_time_limit1.setVisible(True)
            self.panel.btn_open2.lab_time_limit1.SetString(tutil.get_readable_time_2(end_left_time))
            if not self.panel.btn_open2.btn_common.IsEnable():
                self.update_red_envelope()
        else:
            self.panel.btn_open2.lab_time_limit1.setVisible(False)
            self.update_red_envelope()
            return -1

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_red_envelope_state_event': self.update_red_envelope,
           'set_spring_envelope_state_event': self.update_spring_envelope,
           'message_on_players_detail_inf': self.update_red_envelope
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def get_mini_program_path(self):
        player = global_data.player
        if not player:
            return ''
        role_id = player.uid
        role_name = player.get_name()
        server = interface.get_server_name()
        server_id = global_data.channel._hostnum
        lv = player.get_lv()
        input_params = {'role_id': str(role_id),
           'role_name': role_name,
           'server': server,
           'server_id': str(server_id)
           }
        path_sign = get_mini_program_path_sign(input_params, SIGN_KEY)
        input_params['lv'] = lv
        input_params['key'] = path_sign
        url_params_str = six.moves.urllib.parse.urlencode(input_params)
        return 'pages/hb/hb?%s' % url_params_str

    def init_btns(self):
        self.panel.btn_open1.btn_common.SetEnable(False)
        self.panel.btn_open2.btn_common.SetEnable(False)

        @self.panel.btn_open1.btn_common.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            if player.get_lv() < 10:
                global_data.game_mgr.show_tip(get_text_by_id(607931))
            else:
                player.receive_spring_red_envelope()

        @self.panel.btn_open2.btn_common.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            create_time = player.get_create_time()
            now_stamp = tutil.get_server_time()
            left_time = now_stamp - create_time
            red_envelope_teammate_uids, _, _ = player.get_red_envelope_state()
            if left_time > 0 and left_time < 3 * tutil.ONE_DAY_SECONDS and len(red_envelope_teammate_uids) <= 1:
                global_data.game_mgr.show_tip(get_text_by_id(607932).format(tutil.get_simply_time(3 * tutil.ONE_DAY_SECONDS - left_time)))
            else:
                print('ActivityWeixinRedEnvelopes==============mini_program_path============', self.mini_program_path)
                share_wx_mini_program(self.user_name, self.mini_program_path, self.mini_program_type)

    def update_spring_envelope(self):
        player = global_data.player
        if not player:
            return
        spring_envelope_state = player.get_spring_envelope_state()
        btn_open1 = self.panel.btn_open1.btn_common
        btn_open1.SetEnable(False)
        start_left_time, end_left_time = self.get_spring_envelope_left_time()
        self.panel.btn_open1.img_red.setVisible(False)
        if start_left_time > 0:
            btn_open1.SetEnable(False)
            btn_open1.SetText(19825)
        elif end_left_time > 0:
            if spring_envelope_state:
                btn_open1.SetEnable(False)
                if player.is_spring_envelope_last_day():
                    btn_open1.SetText(607911)
                else:
                    btn_open1.SetText(606046)
            else:
                btn_open1.SetEnable(True)
                if player.get_lv() < 10:
                    btn_open1.SetText(607930)
                else:
                    self.panel.btn_open1.img_red.setVisible(True)
                    btn_open1.SetText(607908)
        else:
            btn_open1.SetEnable(False)
            btn_open1.SetText(607911)
        if self.panel.btn_open1.lab_time_limit1.isVisible():
            btn_open1.SetTextOffset({'x': '50%','y': '50%20'})
        else:
            btn_open1.SetTextOffset({'x': '50%','y': '50%'})
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_red_envelope(self, *args):
        player = global_data.player
        if not player:
            return
        start_left_time, end_left_time = self.get_red_envelope_left_time()
        red_envelope_teammate_uids, _, red_envelope_state = player.get_red_envelope_state()
        for i, item_widget in enumerate(self.panel.list_head.GetAllItem()):
            is_self = False
            team_num = len(red_envelope_teammate_uids)
            if team_num == 0 and i == 0:
                has_teammate = True
                head_frame = player.get_head_frame()
                head_photo = player.get_head_photo()
                lv = player.get_lv()
                name = player.get_name()
                is_self = True
            else:
                has_teammate = i < team_num
                if has_teammate:
                    uid = red_envelope_teammate_uids[i]
                    player_info = global_data.message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
                    if player.uid == uid:
                        head_frame = player.get_head_frame()
                        head_photo = player.get_head_photo()
                        lv = player.get_lv()
                        name = player.get_name()
                        is_self = True
                    else:
                        head_frame = player_info.get('head_frame')
                        head_photo = player_info.get('head_photo')
                        lv = player_info.get('lv')
                        name = player_info.get('char_name')
            item_widget.btn_empty.setVisible(not has_teammate)
            item_widget.temp_head.setVisible(has_teammate)
            if has_teammate:
                if is_self:
                    role_head_utils.init_role_head(item_widget.temp_head, head_frame, head_photo)
                else:
                    role_head_utils.init_role_head_auto(item_widget.temp_head, player_info.get('uid'), 0, player_info, show_tips=True)
                item_widget.lab_lv_red.SetString('LV.%d' % lv)
                item_widget.img_tick.setVisible(lv >= 20)
                formated_name = format_one_line_text(item_widget.lab_name, name, 80)
                item_widget.lab_name.SetString(formated_name)
            else:
                item_widget.btn_empty.SetEnable(start_left_time < 0 and end_left_time > 0)

                @item_widget.btn_empty.unique_callback()
                def OnClick(btn, touch):
                    self.panel.btn_open2.btn_common.OnClick(None)
                    return

        btn_open2 = self.panel.btn_open2.btn_common
        self.panel.btn_open2.img_red.setVisible(False)
        self.panel.lab_get.setVisible(False)
        if start_left_time > 0:
            btn_open2.SetEnable(False)
            btn_open2.SetText(19825)
        elif end_left_time > 0:
            btn_open2.SetEnable(True)
            if red_envelope_state == acconst.RED_ENVELOP_NOTFULL:
                btn_open2.SetText(608177)
            elif red_envelope_state == acconst.RED_ENVELOP_FULL:
                btn_open2.SetText(607910)
            elif red_envelope_state == acconst.RED_ENVELOP_REACH:
                btn_open2.SetText(607908)
                self.panel.btn_open2.img_red.setVisible(True)
            elif red_envelope_state in [acconst.RED_ENVELOP_OPEN, acconst.RED_ENVELOP_WITHDRAW]:
                btn_open2.SetText(80821)
                self.panel.lab_get.setVisible(True)
            else:
                btn_open2.SetEnable(False)
                btn_open2.SetText(19825)
        else:
            btn_open2.SetEnable(False)
            btn_open2.SetText(607911)
        if self.panel.btn_open2.lab_time_limit1.isVisible():
            btn_open2.SetTextOffset({'x': '50%','y': '50%15'})
        else:
            btn_open2.SetTextOffset({'x': '50%','y': '50%'})
        global_data.emgr.refresh_activity_redpoint.emit()