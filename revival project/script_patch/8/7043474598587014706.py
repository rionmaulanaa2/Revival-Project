# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCareer.py
from __future__ import absolute_import
import six_ex
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Bool
from logic.gcommon.ctypes.CareerRecord import CareerRecord
from logic.gutils import career_utils
from logic.gutils import task_utils
from logic.gcommon.common_const import rank_career_const

class impCareer(object):

    def _init_career_from_dict(self, bdict):
        self.career_record = CareerRecord(bdict)
        self._career_badge_wall = {int(wall_idx):task_id for wall_idx, task_id in six.iteritems(bdict.get('career_badge_wall', {}))}
        from logic.comsys.career.CareerBadgePromptMgr import CareerBadgePromptMgr
        CareerBadgePromptMgr()
        global_data.emgr.task_max_prog_changed += self.on_task_max_prog_changed

    def _destroy_career(self):
        global_data.emgr.task_max_prog_changed -= self.on_task_max_prog_changed

    def request_receive_career_point(self, task_id):
        self.call_server_method('request_receive_career_point', (task_id,))

    @rpc_method(CLIENT_STUB, (Str('task_id'), Int('point_idx')))
    def respon_receive_career_point(self, task_id, point_idx):
        prev = self.career_record.get_point_idx(task_id)
        self.career_record.set_point_idx(task_id, point_idx)
        cp_reward_idx = point_idx
        sub_branch = task_id
        got_pts = career_utils.cal_cp_diff(task_id, prev, point_idx)
        global_data.emgr.received_cp_pts.emit(sub_branch, cp_reward_idx, got_pts)

    def get_ongoing_career_point_idx(self, task_id):
        return self.career_record.get_point_idx(task_id)

    def get_badge_level(self, task_id):
        return self.career_record.get_badge_level(task_id)

    def has_got_badge(self, task_id, lv):
        return self.career_record.has_got_badge(task_id, lv)

    def request_receive_career_badge(self, task_id, badge_idx):
        self.call_server_method('request_receive_career_badge', (task_id, badge_idx))

    @rpc_method(CLIENT_STUB, (Str('task_id'), Int('badge_idx'), Int('timestamp')))
    def respon_receive_career_badge(self, task_id, badge_idx, timestamp):
        prev_lv = self.get_badge_level(task_id)
        self.career_record.set_badge_timestamp(task_id, badge_idx, timestamp)
        now_lv = self.get_badge_level(task_id)
        sub_branch = task_id
        is_medal = career_utils.is_medal_badge(sub_branch)
        if is_medal:
            if now_lv > prev_lv:
                from logic.comsys.career.CareerBadgePromptUI import BadgePromptData
                msg = [
                 BadgePromptData(sub_branch, now_lv)]
                global_data.career_badge_prompt_mgr.push(msg)
                self._on_check_badge_prompt_play()
                if global_data.channel.get_app_channel() == 'steam':
                    conf = task_utils.get_task_conf_by_id(task_id)
                    badge_steam_api_name = conf.get('badge_steam_api_name', None)
                    if badge_steam_api_name:
                        global_data.channel.SetSteamAchievement(badge_steam_api_name)
                        global_data.channel.DoSteamStoreStats()
        global_data.emgr.received_career_badge.emit(sub_branch, badge_idx, timestamp)
        return

    def on_task_max_prog_changed(self, changes):
        msg = []
        has_new_steam_achievement = False
        for change in changes:
            task_id, old, cur = change.task_id, change.pre_val, change.cur_val
            sub_branch = task_id
            if not career_utils.is_badge(sub_branch):
                continue
            prev_lv = career_utils.get_badge_lv_by_prog(sub_branch, old)
            cur_lv = career_utils.get_badge_lv_by_prog(sub_branch, cur)
            got, _ = self.has_got_badge(sub_branch, cur_lv)
            if not got and prev_lv < cur_lv:
                from logic.comsys.career.CareerBadgePromptUI import BadgePromptData
                msg.append(BadgePromptData(sub_branch, cur_lv))
                if global_data.channel.get_app_channel() == 'steam':
                    conf = task_utils.get_task_conf_by_id(task_id)
                    badge_steam_api_name = conf.get('badge_steam_api_name', None)
                    if badge_steam_api_name:
                        has_new_steam_achievement = True
                        global_data.channel.SetSteamAchievement(badge_steam_api_name)

        if has_new_steam_achievement:
            global_data.channel.DoSteamStoreStats()
        if msg:
            from logic.gutils import system_unlock_utils
            has_m = system_unlock_utils.has_sys_unlock_mechanics(system_unlock_utils.SYSTEM_CAREER)
            has_u = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_CAREER)
            if not has_m or has_u:
                global_data.career_badge_prompt_mgr.push(msg)
                self._on_check_badge_prompt_play()
        return

    def _on_check_badge_prompt_play(self):
        from mobile.common.EntityManager import EntityManager
        entitys = EntityManager.get_entities_by_type('Lobby')
        entity = None
        if entitys:
            for _, e in six.iteritems(entitys):
                entity = e
                break

        if not entity:
            return
        else:
            lobby = entity
            if not lobby.is_lobby_loaded():
                return
            open_box_ui = global_data.ui_mgr.get_ui('OpenBoxUI')
            if open_box_ui and not open_box_ui.get_can_close():
                return
            if global_data.player and global_data.player.get_requesting_lucky_goods():
                return
            if global_data.player and global_data.player.is_running_show_advance():
                return
            global_data.career_badge_prompt_mgr.play()
            return

    def get_career_badge_wall(self):
        wall_dict = {}
        for wall_idx, task_id in six.iteritems(self._career_badge_wall):
            progress = self.get_task_max_prog(task_id)
            badge_lv = self.get_badge_level(task_id)
            wall_dict[wall_idx] = (task_id, badge_lv, progress)

        return wall_dict

    def request_set_career_badge_wall(self, c_badge_wall_dict):
        if c_badge_wall_dict is None:
            return
        else:
            c_wall_dict = dict(c_badge_wall_dict)
            for wall_idx in six_ex.keys(c_wall_dict):
                badge_data = c_wall_dict[wall_idx]
                if wall_idx < 0 or wall_idx >= rank_career_const.CAREER_BADGE_WALL_CNT:
                    del c_wall_dict[wall_idx]
                    continue
                has, lv = career_utils.has_badge(badge_data.sub_branch)
                if not has or lv != badge_data.lv:
                    del c_wall_dict[wall_idx]

            proto_wall_dict = {wall_idx:badge_data.sub_branch for wall_idx, badge_data in six.iteritems(c_wall_dict)}
            self._career_badge_wall = proto_wall_dict
            self.call_server_method('request_set_career_badge_wall', (proto_wall_dict,))
            global_data.emgr.on_wall_badge_set.emit(c_wall_dict)
            return