# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/mecha_career_utils.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range

def get_mecha_career_data(mecha_id, mecha_mem_dict):
    from common.cfg import confmgr
    from logic.gutils.season_utils import get_func_ret_with_dict
    from collections import OrderedDict
    career_stat = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id), 'career_stat', default=[])
    mecha_list_data = ['mecha_fight_time', 'mecha_kill_num', 'mecha_game_num', 'mecha_MVP', 'mecha_win_rate', 'mecha_damage']
    skill_list_data = []
    if len(career_stat) > 0:
        mecha_list_data = career_stat[0] or mecha_list_data
        skill_list_data = career_stat[1]
    else:
        log_error('\xe6\x9c\xba\xe7\x94\xb2%s \xe7\x9a\x8453\xe5\x8f\xb7\xe8\xa1\xa8\xe7\x9a\x84career_stat\xe6\xb2\xa1\xe5\xa1\xab\xe5\x86\x99\xef\xbc\x8c\xe8\xaf\xb7\xe5\xa1\xab\xe5\x86\x99\xef\xbc\x81\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84215\xe5\x8f\xb7\xe8\xa1\xa8\xe4\xb9\x9f\xe9\x9c\x80\xe8\xa6\x81\xe5\xa1\xab\xe5\x86\x99\xe3\x80\x82')
    if not mecha_mem_dict:
        mecha_dict = OrderedDict()
        skill_dict = OrderedDict()
        for kind in mecha_list_data:
            mecha_dict[kind] = None

        for kind in skill_list_data:
            skill_dict[kind] = None

        return (mecha_dict, skill_dict, {})
    else:
        value_dict = {}
        from logic.gcommon.common_const import web_const
        MAX_ATTR_NUM = 20
        for i in range(0, MAX_ATTR_NUM):
            attr = getattr(web_const, str('MECHA_MEMORY_LEVEL_%s' % i), None)
            if attr:
                value_dict['MML_%s' % i] = mecha_mem_dict.get(attr, None)

        icon_dict = {}

        def get_list_ret(input_list_data):
            valid_dict = OrderedDict()
            valid_icon_dict = {}
            mecha_career_dict = confmgr.get('mecha_memory_conf', 'MechaStatMemoryConf', 'Content', default={})
            for kind in input_list_data:
                stat_conf = mecha_career_dict.get(kind, {})
                if stat_conf:
                    ret_format = stat_conf.get('ret_format', '')
                    kind_value_dict = dict(value_dict)
                    predefine_key_value_map = stat_conf.get('key_value_map', {})
                    if predefine_key_value_map:
                        for _k, _v in six.iteritems(predefine_key_value_map):
                            kind_value_dict[_k] = get_func_ret_with_dict(_v, value_dict)

                    extra_data_dict = stat_conf.get('extra_data', {})
                    kind_value_dict.update(extra_data_dict)
                    val = get_func_ret_with_dict(ret_format, kind_value_dict, None)
                    if val is not None:
                        valid_dict[kind] = val
                    else:
                        valid_dict[kind] = None
                    icon_format = stat_conf.get('icon_format', '')
                    if icon_format:
                        valid_icon_dict[kind] = get_func_ret_with_dict(icon_format, kind_value_dict)

            return (
             valid_dict, valid_icon_dict)

        mecha_dict, mecha_icon_dict = get_list_ret(mecha_list_data)
        skill_dict, skill_icon_dict = get_list_ret(skill_list_data)
        icon_dict.update(mecha_icon_dict)
        icon_dict.update(skill_icon_dict)
        return (
         mecha_dict, skill_dict, icon_dict)


def get_mecha_career_show_num(kind, mecha_ord_dict):
    from common.cfg import confmgr
    kind_dict = confmgr.get('mecha_memory_conf', 'MechaStatMemoryConf', 'Content', str(kind), default={})
    val = mecha_ord_dict.get(kind, None)
    if val is None:
        return '0'
    else:
        show_format = kind_dict.get('show_format', '')
        show_num = show_format.format(val) if show_format else str(val)
        return show_num


def init_mecha_career_panel(mecha_list_nd, skill_list_nd, mecha_ord_dict, skill_ord_dict, shape_id, icon_dict, skill_unlock_levels):
    from common.cfg import confmgr
    mecha_list_nd.SetInitCount(len(mecha_ord_dict))
    for ind, key in enumerate(six_ex.keys(mecha_ord_dict)):
        ui_item = mecha_list_nd.GetItem(ind)
        career_dict = confmgr.get('mecha_memory_conf', 'MechaStatMemoryConf', 'Content', str(key), default={})
        if mecha_ord_dict[key] is not None:
            if type(mecha_ord_dict[key]) in (int, float, six_ex.long_type):
                show_format = career_dict.get('show_format', '')
                show_num = show_format.format(mecha_ord_dict[key]) if show_format else format_career_num(mecha_ord_dict[key])
                ui_item.lab_value.SetString(show_num)
            else:
                ui_item.lab_value.SetString(mecha_ord_dict[key])
        else:
            val = 0
            show_format = career_dict.get('show_format', '')
            show_num = show_format.format(val) if show_format else format_career_num(val)
            ui_item.lab_value.SetString(show_num)
        tid = career_dict.get('lab_tid', '')
        if tid.isdigit():
            text = int(tid) if 1 else tid
            ui_item.lab_title.SetString(text)

    action_config = confmgr.get('mecha_conf', 'ActionConfig', 'Content', str(shape_id))
    skill_list_nd.SetInitCount(len(skill_ord_dict))
    for ind, key in enumerate(six_ex.keys(skill_ord_dict)):
        ui_item = skill_list_nd.GetItem(ind)
        career_dict = confmgr.get('mecha_memory_conf', 'MechaStatMemoryConf', 'Content', str(key), default={})
        if skill_ord_dict[key] is not None:
            show_format = career_dict.get('show_format', '')
            raw_num = skill_ord_dict[key]
            if show_format:
                if type(raw_num) in (int, six_ex.long_type, float):
                    show_num = show_format.format(raw_num)
                else:
                    show_num = raw_num
            elif type(raw_num) in (int, six_ex.long_type, float):
                show_num = format_career_num(skill_ord_dict[key])
            else:
                show_num = raw_num
            ui_item.lab_value.SetString(show_num)
        else:
            val = 0
            show_format = career_dict.get('show_format', '')
            show_num = show_format.format(val) if show_format else format_career_num(val)
            ui_item.lab_value.SetString(show_num)
        tid = career_dict.get('lab_tid', '')
        text = get_text_by_id(int(tid)) if tid.isdigit() else tid
        ui_item.lab_skill_name.SetString(text)
        icon = career_dict.get('icon', '')
        if icon_dict.get(key, None):
            ui_item.icon_skill.SetDisplayFrameByPath('', icon_dict.get(key, None))
        elif icon:
            pic = icon
            if not icon.endswith('png'):
                action_id = icon
                act_icon = action_config.get('action_icon', {}).get(action_id, None)
                if act_icon:
                    pic = 'gui/ui_res_2/battle/mech_main/{}.png'.format(act_icon)
            ui_item.icon_skill.SetDisplayFrameByPath('', pic)
        pic_scale = career_dict.get('pic_scale', None)
        if pic_scale:
            ui_item.icon_skill.setScale(pic_scale)
        else:
            ui_item.icon_skill.setScale(0.7)

    for ind, need_show_lv in enumerate(skill_unlock_levels):
        ui_item = skill_list_nd.GetItem(ind)
        if not ui_item:
            continue
        if need_show_lv is None:
            ui_item.icon_skill.setOpacity(178)
            ui_item.btn.SetShowEnable(True)
            ui_item.lab_skill_name.SetColor(14607359)
            ui_item.lab_lock.setVisible(False)
            ui_item.lab_value.setVisible(True)
        else:
            ui_item = skill_list_nd.GetItem(ind)
            ui_item.icon_skill.setOpacity(77)
            ui_item.btn.SetShowEnable(False)
            ui_item.lab_skill_name.SetColor(10334207)
            ui_item.lab_value.setVisible(False)
            ui_item.lab_lock.SetString(get_text_by_id(83348, {'level': 'Lv.%s' % need_show_lv}))
            ui_item.lab_lock.setVisible(True)

    return


class MechaMemoryStatWidget(object):

    def __init__(self):
        self.mecha_type = None
        self._show_battle_season_id = None
        self._data_update_cb = None
        self._data_modify_cb = None
        self.list_btn = None
        self.list_lab = None
        self.uid = global_data.player.uid
        self.process_event(True)
        return

    def destroy(self):
        self.list_btn = None
        self.list_lab = None
        self._data_update_cb = None
        self._data_modify_cb = None
        self.process_event(False)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_mecha_memory_stat_received_event': self.on_mecha_memory_stat_received
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_mecha_type(self, mecha_type):
        if mecha_type != self.mecha_type:
            self.mecha_type = mecha_type

    def set_data_cb(self, cb):
        self._data_update_cb = cb

    def set_data_modify_cb(self, cb):
        self._data_modify_cb = cb

    def set_node(self, list_lab, list_btn):
        self.list_lab = list_lab
        self.list_btn = list_btn

    def set_uid(self, uid):
        self.uid = uid

    def on_need_show_show_battle_season_id(self, season_id):
        self._show_battle_season_id = season_id

    def refresh(self):
        if not global_data.mecha_memory_stat_mgr:
            from logic.comsys.mecha_display.mecha_memory.MechaMemoryStatMgr import MechaMemoryStatMgr
            MechaMemoryStatMgr()
        if global_data.mecha_memory_stat_mgr:
            data = global_data.mecha_memory_stat_mgr.get_or_request_mecha_memory_data(self.uid, self._show_battle_season_id)
            if data:
                self.update_mecha_memory_pannel(data)
                return
        self.update_mecha_memory_pannel({}, fake_init=True)

    def on_mecha_memory_stat_received(self):
        if global_data.mecha_memory_stat_mgr:
            data = global_data.mecha_memory_stat_mgr.get_or_request_mecha_memory_data(self.uid, self._show_battle_season_id)
            if data:
                self.update_mecha_memory_pannel(data)
                return

    def update_mecha_memory_pannel(self, all_mecha_data, fake_init=False):
        if self.list_btn and self.list_lab:
            mecha_data = all_mecha_data.get(str(self.mecha_type), {})
            mecha_dict, skill_dict, icon_dict = get_mecha_career_data(self.mecha_type, mecha_data)
            if self._data_modify_cb:
                mecha_dict, skill_dict, icon_dict = self._data_modify_cb(self._show_battle_season_id, all_mecha_data, fake_init, mecha_dict, skill_dict, icon_dict)
            level, proficiency = get_mecha_season_proficiency(self.uid, self.mecha_type, self._show_battle_season_id, all_mecha_data)
            skill_unlock_require_level = [5, 15, 35]
            skill_unlock_level = []
            for r_lv in skill_unlock_require_level:
                if level >= r_lv:
                    skill_unlock_level.append(None)
                else:
                    skill_unlock_level.append(r_lv)

            init_mecha_career_panel(self.list_lab, self.list_btn, mecha_dict, skill_dict, self.mecha_type, icon_dict, skill_unlock_level)
        if self._data_update_cb:
            self._data_update_cb(self._show_battle_season_id, all_mecha_data, fake_init)
        return

    def get_season_data(self):
        if not global_data.mecha_memory_stat_mgr:
            return None
        else:
            data = global_data.mecha_memory_stat_mgr.get_or_request_mecha_memory_data(self.uid, self._show_battle_season_id)
            return data


def format_career_num(num):
    K_VALUE = 1000
    M_VALUE = 1000000
    B_VALUE = 1000000000
    if num < K_VALUE:
        return '%d' % num
    if num < M_VALUE:
        if num % K_VALUE == 0:
            return '%dk' % (num / K_VALUE)
        else:
            if float(num) / K_VALUE < 100:
                return ('%.1fk' % (float(num) / K_VALUE)).replace('.0', '')
            return ('%.0fk' % (float(num) / K_VALUE)).replace('.0', '')

    elif num < B_VALUE:
        if num % M_VALUE == 0:
            return '%dm' % (num / M_VALUE)
        else:
            if float(num) / M_VALUE < 100:
                return ('%.1fm' % (float(num) / M_VALUE)).replace('.0', '')
            return ('%.0fm' % (float(num) / M_VALUE)).replace('.0', '')

    else:
        if num % B_VALUE == 0:
            return '%db' % (num / B_VALUE)
        if float(num) / B_VALUE < 100:
            return ('%.1fb' % (float(num) / B_VALUE)).replace('.0', '')
        return ('%.0fb' % (float(num) / B_VALUE)).replace('.0', '')


def init_career_titile(bar_rank, best_rank):
    from logic.gutils.season_utils import get_mecha_best_region_rank
    if best_rank:
        bar_rank.setVisible(True)
        title_type, region_type, mecha_type, rank_adcode, rank, rank_expire = best_rank
        from logic.gutils import locate_utils
        rank_txt = locate_utils.get_rank_title(title_type, [region_type, mecha_type, rank_adcode, rank, rank_expire])
        from logic.gcommon.common_const import rank_const, rank_mecha_const, rank_region_const
        bar_dict = {rank_region_const.REGION_RANK_TYPE_COUNTRY: 'gui/ui_res_2/mech_display/career/bar_mech_career_yellow.png',
           rank_region_const.REGION_RANK_TYPE_PROVINCE: 'gui/ui_res_2/mech_display/career/bar_mech_career_purple.png',
           rank_region_const.REGION_RANK_TYPE_CITY: 'gui/ui_res_2/mech_display/career/bar_mech_career_blue.png'
           }
        bar_pic = bar_dict.get(region_type, 'gui/ui_res_2/mech_display/career/bar_mech_career_yellow.png')
        bar_rank.SetDisplayFrameByPath('', bar_pic)
        bar_rank.lab_rank.SetString(str(rank_txt))
    else:
        bar_rank.setVisible(False)


def get_career_season_name(season_id):
    return 'S' + str(season_id)


def get_mecha_season_proficiency(uid, mecha_id, season, cur_season_data):
    mecha_proficiency = cur_season_data.get('mecha_proficiency', {}).get(str(mecha_id), [1, 0])
    if global_data.player:
        is_mine = uid == global_data.player.uid if 1 else False
        if global_data.player:
            cur_season = global_data.player.get_battle_season()
        else:
            from logic.gcommon.cdata import season_data
            cur_season = season_data.get_cur_battle_season()
        if is_mine and season == cur_season:
            get_proficiency = global_data.player.get_proficiency if global_data.player else (lambda _: mecha_proficiency)
            return get_proficiency(mecha_id)
    return mecha_proficiency