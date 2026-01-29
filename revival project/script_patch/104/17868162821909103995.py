# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAdvance.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
import sys
from exception_hook import dump_exception_hook
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil
from logic.gutils import advance_utils

class AdvanceCallback(object):

    def __init__(self, ui_name, func):
        self._cb = func
        self.ui_name = ui_name
        self.hide_lobby_ui = True

    def call(self):
        return self._cb()

    def set_hide_lobby_ui(self, hide_lobby_ui):
        self.hide_lobby_ui = hide_lobby_ui


class impAdvance(object):

    def _init_advance_from_dict(self, bdict):
        self._advance_version = bdict.get('advance_version', {})
        self._advance_list = bdict.get('advance_seq', None)
        self._cur_ui_name = None
        self._cur_ui_id = None
        self._cur_advance_cb = None
        self._finish_advance_cb_list = []
        return

    def _on_login_advance_success(self):
        if self._advance_list is None:
            self._advance_list = self.get_advance_seq()
        return

    def has_advance_list(self):
        return bool(self._advance_list)

    def add_advance_finish_func(self, callback):
        self._finish_advance_cb_list.append(callback)

    def _destroy_advance(self):
        self.clear_advance_sequence()

    def clear_advance_sequence(self):
        self._advance_list = []
        if self._cur_ui_name:
            global_data.ui_mgr.close_ui(self._cur_ui_name)

    def on_close_ui(self, ui_name):
        if ui_name != self._cur_ui_name:
            return
        else:
            if self._cur_ui_id:
                self.call_server_method('on_show_advance', (self._cur_ui_id,))
            if self._cur_advance_cb:
                if not self._cur_advance_cb.hide_lobby_ui:
                    ui = global_data.ui_mgr.get_ui('LobbyUI')
                    if ui is not None:
                        ui.add_hide_count(self.__class__.__name__)
            self._cur_ui_name = None
            self._cur_ui_id = None
            self._cur_advance_cb = None
            self.show_next_advance()
            return

    def add_advance_ids(self, ids):
        self._advance_list.extend(ids)

    def remove_advance_by_ui_name(self, ui_name):
        remove_indexes = []
        for idx, advance in enumerate(self._advance_list):
            advance_id = None
            if isinstance(advance, (int, str)):
                advance_id, advance_data = advance, None
            elif isinstance(advance, (list, tuple)):
                advance_id, advance_data = advance
            elif isinstance(advance, AdvanceCallback):
                if advance.ui_name == ui_name:
                    remove_indexes.append(idx)
                continue
            if advance_id:
                advance_conf = confmgr.get('advance_config', str(advance_id), default={})
                adv_ui_name, ui_path = advance_conf['ui_name']
                if adv_ui_name == ui_name:
                    remove_indexes.append(idx)

        for idx in sorted(remove_indexes, reverse=True):
            self._advance_list.pop(idx)

        return

    def add_advance_callback(self, ui_name, callback, **kw):

        def wrapper():
            callback()
            self._cur_ui_name = ui_name

        inst = AdvanceCallback(ui_name, wrapper)
        if 'hide_lobby_ui' in kw:
            inst.set_hide_lobby_ui(kw['hide_lobby_ui'])
        if 'advance_first' in kw:
            self._advance_list.insert(0, inst)
        else:
            self._advance_list.append(inst)

    def has_advance_callback(self, ui_name):
        if self._advance_list is None:
            return False
        else:
            for advance in self._advance_list:
                if isinstance(advance, AdvanceCallback):
                    if advance.ui_name == ui_name:
                        return True

            return False

    def is_running_show_advance(self):
        return self._cur_ui_name is not None

    def start_show_advance(self):
        if not self._advance_list:
            global_data.player and global_data.emgr.show_cache_generic_reward.emit()
            self.check_show_lobby_newbie_guide_ui()
            self.try_send_priv_red_packet()
            return
        else:
            if self._cur_ui_name:
                log_error('[Advance] start_show_advance, cur_ui_name = %s', self._cur_ui_name)
                return
            ui = global_data.ui_mgr.get_ui('LobbyUI')
            if ui is not None:
                ui.add_hide_count(self.__class__.__name__)
            global_data.emgr.ui_close_event += self.on_close_ui
            self.show_next_advance()
            return

    def on_finish_advance(self):
        global_data.emgr.ui_close_event -= self.on_close_ui
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        if ui is not None:
            ui.add_show_count(self.__class__.__name__)
            ui.check_auto_open_answer_ui()
        self.check_show_newbie_mecha_advance()
        global_data.player and global_data.player.show_afk_confirmUI()
        global_data.career_badge_prompt_mgr.play()
        if ui is not None:
            ui.check_newbie_assessment_redpoint()
        self.check_show_lobby_newbie_guide_ui()
        global_data.emgr.finish_advance_ui_list_event.emit()
        global_data.emgr.show_cache_specific_reward.emit('TASK_REWARD_1421057')
        global_data.emgr.show_cache_specific_reward.emit('TASK_REWARD_1421058')
        if self._finish_advance_cb_list:
            for cb in self._finish_advance_cb_list:
                if callable(cb):
                    cb()

            self._finish_advance_cb_list = []
        self.try_send_priv_red_packet()
        return

    def show_next_advance(self):
        while 1:
            if self._advance_list:
                advance = self._advance_list.pop(0)
                advance_id, advance_data = (0, None)
                if isinstance(advance, (int, str)):
                    advance_id, advance_data = advance, None
                elif isinstance(advance, (list, tuple)):
                    advance_id, advance_data = advance
                else:
                    if callable(advance):
                        advance()
                        return
                    if isinstance(advance, AdvanceCallback):
                        advance.call()
                        self._cur_advance_cb = advance
                        if not advance.hide_lobby_ui:
                            ui = global_data.ui_mgr.get_ui('LobbyUI')
                            if ui is not None:
                                ui.add_show_count(self.__class__.__name__)
                        return
                advance_conf = confmgr.get('advance_config', str(advance_id), default={})
                if not advance_conf:
                    continue
                if not self.check_open(advance_id, advance_conf):
                    continue
                ui_name, ui_path = advance_conf['ui_name']
                try:
                    ui = global_data.ui_mgr.show_ui(ui_name, ui_path)
                except:
                    dump_exception_hook(*sys.exc_info())
                    ui = None

                if not ui:
                    pass
                continue
            self._cur_ui_name = ui_name
            self._cur_ui_id = advance_id
            show_func_name = advance_conf.get('show_func', '')
            if show_func_name:
                show_func = getattr(advance_utils, show_func_name, None)
                if show_func:
                    custom_data = advance_conf.get('custom_params', {})
                    if advance_data:
                        custom_data.update(advance_data)
                    show_func(ui, custom_data)
            return

        self.on_finish_advance()
        return

    def get_advance_seq(self):
        total_num = 6
        video_num = 1
        advance_conf = confmgr.get('advance_config', default={})
        tmp_ad = six_ex.keys(advance_conf)
        if tmp_ad:
            tmp_ad.sort(key=cmp_to_key(lambda x, y: six_ex.compare(int(x), int(y))), reverse=True)
        normal_ad = []
        force_ad = []
        for aid in tmp_ad:
            info = advance_conf[aid]
            if 'priority' not in info:
                continue
            if not self.check_open(aid, info):
                continue
            show_type = info.get('show_type')
            if show_type == advance_utils.SHOW_TYPE_FORCE:
                force_ad.append(aid)
                continue
            if show_type == advance_utils.SHOW_TYPE_VIDEO:
                if not video_num:
                    continue
                video_num -= 1
            normal_ad.append(aid)

        if len(force_ad) >= total_num:
            advance_ids = list(force_ad)
        else:
            advance_ids = force_ad + normal_ad
            if len(advance_ids) > total_num:
                advance_ids = advance_ids[0:total_num]
        advance_ids.sort(key=cmp_to_key(lambda x, y: six_ex.compare(advance_conf[x]['priority'], advance_conf[y]['priority'])))
        return advance_ids

    def check_show_newbie_mecha_advance(self):
        from logic.comsys.guide_ui.GuideSetting import GuideSetting
        is_create_login = GuideSetting()._create_login
        is_battled_once = global_data.player and global_data.player.get_total_cnt() == 1
        if global_data.achi_mgr.get_cur_user_archive_data('showed_newbie_mecha_advance', default=0) == 1:
            return
        if is_create_login and is_battled_once:
            global_data.ui_mgr.show_ui('NewMechaNewbieGuideUI', 'logic.comsys.guide_ui')
            global_data.achi_mgr.set_cur_user_archive_data('showed_newbie_mecha_advance', 1)
            self.call_server_method('on_show_advance', ('62', ))

    def check_show_lobby_newbie_guide_ui(self):
        from logic.gutils.guide_utils import is_quality_level_initial
        from logic.comsys.guide_ui.LobbyNewbieGuideUI import LobbyNewbieGuideMgr
        LobbyNewbieGuideMgr().start_show_guide()
        if is_quality_level_initial():
            global_data.emgr.begin_guide_after_advance_event.emit()

    def check_open(self, advance_id, advance_conf=None):
        if advance_conf is None:
            advance_conf = confmgr.get('advance_config', str(advance_id), default={})
        from logic.comsys.guide_ui.GuideSetting import GuideSetting
        if not advance_conf.get('ignore_create_login', 0) and GuideSetting()._create_login:
            return False
        else:
            newbie_date = advance_conf.get('newbie_date', None)
            if newbie_date is not None:
                if self.get_create_time() < newbie_date:
                    return False
            level = advance_conf.get('level', 0)
            if level and self.get_lv() < level:
                return False
            now = tutil.get_server_time()
            if not advance_conf.get('start_time', 0) < now < advance_conf.get('end_time', now + 1):
                return False
            server_list = advance_conf.get('server_list', None)
            if server_list and global_data.channel.get_host_num() not in server_list:
                return False
            close_server_list = advance_conf.get('close_server_list', None)
            if close_server_list and global_data.channel.get_host_num() in close_server_list:
                return False
            close_package_list = advance_conf.get('close_package_list', None)
            if close_package_list and global_data.channel.get_name() in close_package_list:
                return False
            a_type = advance_conf.get('type', 0)
            if a_type:
                num = self._advance_version.get(advance_id, 0)
                if num >= advance_conf.get('count', 1):
                    return False
            check_func_name = advance_conf.get('check_func', '')
            if check_func_name:
                check_func = getattr(advance_utils, check_func_name, None)
                if not check_func:
                    return False
                custom_data = advance_conf.get('custom_params', {})
                if not check_func(self, custom_data):
                    return False
            return True