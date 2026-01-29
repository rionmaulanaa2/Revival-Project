# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerMiniGame.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from cocosui import cc
from logic.gutils import activity_utils
from logic.gutils.share_utils import share_wx_mini_program, share_qq_mini_program, is_package_name_been_share_platform_verified
from logic.gcommon import time_utility as tutil
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import math
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.comsys.reward.SummerGameRewardUI import SummerGameRewardUI
from logic.client.const import share_const

def is_na():
    return G_IS_NA_PROJECT or global_data.channel.is_steam_channel()


def get_query_url():
    host = is_na() or 'interact2.webapp.163.com' if 1 else 'interact2.webapp.easebar.com'
    url = 'https://%s/g93jump/get_dynamic_url' % host
    return url


def get_mini_game_url():
    is_inner = False
    if not is_na():
        if not is_inner:
            return 'https://smc.163.com/h5/jump/'
        return 'https://test.nie.163.com/test_html/ace/h5/jump/'
    from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_EN, LANG_ZHTW, LANG_JA
    cur_lang = get_cur_text_lang()
    if cur_lang in (LANG_CN, LANG_ZHTW):
        if not is_inner:
            return 'https://www.supermechachampions.tw/h5/jump/'
        return 'https://test.nie.163.com/test_html/supermechachampions.tw/h5/jump/'
    if cur_lang == LANG_JA:
        if not is_inner:
            return 'https://www.supermechachampions.com/h5/jump/jp/'
        return 'https://test.nie.163.com/test_html/supermechachampions/h5/jump/jp/'
    if not is_inner:
        return 'https://www.supermechachampions.com/h5/jump/en/'
    return 'https://test.nie.163.com/test_html/supermechachampions/h5/jump/en/'


def get_share_paltform():
    if not is_na():
        return [share_const.APP_SHARE_WEIXIN, share_const.APP_SHARE_MOBILE_QQ]
    return [share_const.APP_SHARE_TWITTER, share_const.APP_SHARE_LINE, share_const.APP_SHARE_FACEBOOK]


class ActivitySummerMiniGame(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySummerMiniGame, self).__init__(dlg, activity_type)
        self._parent_task_id = None
        self._is_appear_share_btn = False
        self.init_parameters()
        self.init_event()
        return

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self._parent_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.receive_task_prog_reward,
           'app_resume_event': self.on_resume,
           'update_summer_game_task_prog': self.on_task_prog_change
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        global_data.player.call_server_method('req_check_summer_mini_game_state', ())
        global_data.player.call_server_method('client_sa_log', ('SummerGameShare', {'click': '1'}))

        @self.panel.btn_tip.unique_callback()
        def OnClick(btn, touch):
            conf = confmgr.get('c_activity_config', self._activity_type)
            if not conf:
                return
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(conf.get('cNameTextID', '')), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.init_animation()
        self.init_share_btn()
        self.init_rewards()
        self.refresh_time()
        self.panel.lab_name.SetString(global_data.player.get_name())

    def init_animation(self):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop_01')

    def init_rewards(self):
        children_tasks = task_utils.get_children_task(self._parent_task_id)
        has_reward_to_receive = False
        for sub_task_id in children_tasks:
            if self._refresh_reward_widget(sub_task_id):
                has_reward_to_receive = True

        if has_reward_to_receive:
            self.panel.PlayAnimation('loop_02')

    def _refresh_reward_widget(self, task_id):
        if not task_id:
            return set()
        else:
            prog_2_reward_id = task_utils.get_prog_rewards_in_dict(task_id)
            player = global_data.player
            receivable_set = set()
            got_set = set()
            for progress in six_ex.keys(prog_2_reward_id):
                is_received = player.has_receive_prog_reward(task_id, progress)
                if is_received:
                    got_set.add(progress)
                    continue
                can_receive = player.is_prog_reward_receivable(task_id, progress)
                if can_receive:
                    receivable_set.add(progress)

            reward_ids = list(six_ex.values(prog_2_reward_id))
            if reward_ids:
                show_reward_id = reward_ids[0] if 1 else 0
                show_reward_list = confmgr.get('common_reward_data', str(show_reward_id), 'reward_list', default=[])
                if not show_reward_list:
                    return
                prize_type = task_utils.get_task_arg(task_id)
                nd_index = ['4', '3', '2', '1'].index(prize_type)
                nd_reward = getattr(self.panel, 'nd_reward_%s' % (nd_index + 1), None)
                if not nd_reward:
                    return set()
                img_bar = getattr(nd_reward, 'img_bar_%s' % (nd_index + 1), None)
                if not img_bar:
                    return set()
                ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
                score = ui_data.get('score') or [600, 400, 200, 100]
                img_bar.lab_requirement.SetString(get_text_by_id(611486).format(num=score[nd_index]))
                img_bar.lab_got.SetString(get_text_by_id(906606).format(str(len(got_set)), str(len(prog_2_reward_id))))
                receivable_set or img_bar.btn_get.SetEnable(False)
                if player.is_task_finished(task_id):
                    img_bar.btn_get.SetText(get_text_by_id(604029))
            else:
                img_bar.btn_get.SetText(get_text_by_id(910007))
                img_bar.btn_get.SetEnable(True)
                img_bar.btn_get.SetSelect(True)

            @img_bar.btn_get.unique_callback()
            def OnClick(btn, touch, tid=task_id):
                if self._is_invalid(tid, show_tip=True):
                    return
                global_data.player.receive_all_task_prog_reward(tid)

            if img_bar.list_item:
                img_bar.list_item.SetInitCount(len(show_reward_list[:3]))
                for i, reward_data in enumerate(show_reward_list[:3]):
                    sub_item = img_bar.list_item.GetItem(i)
                    if not sub_item:
                        continue
                    item_no, item_num = reward_data
                    template_utils.init_tempate_mall_i_item(sub_item.temp_item, item_no, show_tips=True, show_rare_degree=False)
                    sub_item.PlayAnimation('loop_orange')

                @img_bar.btn_look.unique_callback()
                def OnClick(btn, touch, look_reward_id=show_reward_id):
                    if not look_reward_id:
                        return
                    x, y = btn.GetPosition()
                    wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                    SummerGameRewardUI(reward_id=look_reward_id)

            return receivable_set

    def receive_task_prog_reward(self, task_id, prog):
        children_tasks = task_utils.get_children_task(self._parent_task_id)
        if task_id not in children_tasks:
            return
        self._refresh_reward_widget(task_id)
        global_data.emgr.refresh_activity_redpoint.emit()

    def refresh_time(self):
        lab_time = self.panel.lab_time
        left_time = task_utils.get_raw_left_open_time(self._parent_task_id)
        if left_time > 0:
            if left_time > tutil.ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(tutil.get_readable_time(close_left_time))

    def _is_invalid(self, task_id, show_tip=False):
        is_invalid = False
        if activity_utils.is_activity_finished(self._activity_type):
            is_invalid = True
        if not task_utils.is_task_open(task_id):
            is_invalid = True
        if show_tip and is_invalid:
            global_data.game_mgr.show_tip(607911)
        return is_invalid

    def set_share_btn_vis(self, vis):
        if vis:
            self._is_appear_share_btn = True
            self.panel.StopAnimation('disappear')
            self.panel.PlayAnimation('appear')
        else:
            self._is_appear_share_btn = False
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')

    def get_share_url_param(self):
        player = global_data.player
        if not player:
            return ''
        role_id = player.uid
        server_id = global_data.channel._hostnum
        input_params = {'gameuid': str(role_id),
           'hostnum': str(server_id)
           }
        url_params_str = six.moves.urllib.parse.urlencode(input_params)
        return url_params_str

    def init_share_btn(self):

        @self.panel.btn_get_integral.unique_callback()
        def OnClick(btn, touch):
            self.set_share_btn_vis(not self._is_appear_share_btn)

        from logic.gutils.share_utils import init_platform_list

        def share_cb(share_args):
            self.set_share_btn_vis(False)
            platform = share_args.get('platform_enum', None)
            global_data.player.call_server_method('client_sa_log', ('SummerGameShare', {'platform': platform}))
            self.query_share_url(share_args)
            return

        plat_enum_list = get_share_paltform()
        plat_list = global_data.share_mgr.get_support_platforms_from_enum(plat_enum_list)
        init_platform_list(self.panel.list_share, share_cb, share_type=share_const.TYPE_LINK, force_plat_list=plat_list)

    def on_resume(self):
        global_data.player.call_server_method('req_check_summer_mini_game_state', ())

    def on_task_prog_change(self):
        self.init_rewards()

    def query_share_url(self, share_args):
        import json
        import common.http
        import game3d
        from logic.gutils.share_utils import share_url
        interface_url = get_query_url()

        def http_callback(ret, url, args):
            if ret:
                result = json.loads(ret)
                target_url = result.get('share_url')
                if not target_url:
                    target_url = get_mini_game_url()
            else:
                target_url = get_mini_game_url()
            if '?' not in target_url:
                target_url += '?'
            platform = share_args.get('platform_enum', None)
            if global_data.is_pc_mode or game3d.get_platform() == game3d.PLATFORM_WIN32:
                url_params_str = self.get_share_url_param()
                if platform == share_const.APP_SHARE_WEIXIN:
                    url = target_url + '%s&c=2' % url_params_str
                else:
                    url = target_url + '%s&c=1' % url_params_str
                game3d.open_url(url)
                return
            else:
                if platform and target_url:
                    share_url(target_url, platform, share_title=get_text_by_id(906630), share_message=get_text_by_id(906631), share_inform_text=get_text_by_id(906632))
                return

        if is_na():
            http_callback(None, None, {})
        else:
            common.http.request_v2(interface_url, callback=http_callback)
        return