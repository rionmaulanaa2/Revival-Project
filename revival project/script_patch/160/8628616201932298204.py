# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/season_utils.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import six
from common import utilities
from common.cfg import confmgr
from logic.gcommon.cdata import dan_data
from logic.gcommon.cdata import season_data
from logic.gcommon import time_utility
import logic.gcommon.const as gconst
import logic.gutils.item_utils as item_utils
from logic.client.const import game_mode_const

def get_dan_type(cCMode):
    dan_type_map = {game_mode_const.GAME_MODE_DEATH: dan_data.DAN_DEATH
       }
    return dan_type_map.get(cCMode, dan_data.DAN_SURVIVAL)


def get_dan_template(dan):
    return 'rank/i_tier_%d' % dan


def get_dan_list():
    return sorted(six_ex.keys(dan_data.data))


def get_dan_lv_name(dan, lv=None):
    dan_name = get_text_by_id(dan_data.get_dan_name_id(dan))
    if lv == None:
        return dan_name
    else:
        if dan_data.get_lv_num(dan) <= 1:
            return dan_name
        return '{0} {1}'.format(dan_name, utilities.get_rome_num(lv))


def get_todo_dan_task(season, dan):
    min_task_id = ''
    cur_min_dan = 9999
    confs = confmgr.get('task/dan_task_data')
    for key, conf in six.iteritems(confs):
        if conf['season'] == season and dan <= conf['dan'] <= cur_min_dan:
            min_task_id = conf['task_id']
            cur_min_dan = conf['dan']

    return (
     min_task_id, cur_min_dan)


def get_dan_task(season, dan):
    confs = confmgr.get('task/dan_task_data')
    for key, conf in six.iteritems(confs):
        if conf['season'] == season and conf['dan'] == dan:
            return conf['task_id']

    return ''


def get_dan_task_list(season):
    task_list = []
    confs = confmgr.get('task/dan_task_data')
    for key, conf in six.iteritems(confs):
        if conf['season'] == season:
            task_list.append({'task_id': conf['task_id'],'dan': conf['dan']})

    return task_list


def get_dan_task_can_reward_count(season):
    count = 0
    task_list = []
    confs = confmgr.get('task/dan_task_data')
    for key, conf in six.iteritems(confs):
        task_id = conf.get('task_id', '')
        if conf['season'] == season and task_id:
            if global_data.player.has_unreceived_task_reward(task_id):
                count += 1

    return count


def get_season_reward--- This code section failed: ---

  75       0  LOAD_GLOBAL           0  'dan_data'
           3  LOAD_ATTR             1  'data'
           6  LOAD_ATTR             2  'get'
           9  LOAD_FAST             1  'dan'
          12  BUILD_MAP_0           0 
          15  CALL_FUNCTION_2       2 
          18  STORE_FAST            2  'dan_info'

  76      21  LOAD_FAST             2  'dan_info'
          24  LOAD_ATTR             2  'get'
          27  LOAD_CONST            1  'season_reward'
          30  BUILD_MAP_0           0 
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            3  'season_rewards'

  77      39  LOAD_GLOBAL           3  'str'
          42  LOAD_FAST             3  'season_rewards'
          45  LOAD_ATTR             2  'get'
          48  LOAD_ATTR             2  'get'
          51  CALL_FUNCTION_2       2 
          54  CALL_FUNCTION_1       1 
          57  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 51


def get_season_timestamp(season):
    start_timestamp = season_data.get_start_timestamp(season)
    end_timestamp = season_data.get_end_timestamp(season)
    return (
     start_timestamp, end_timestamp)


def get_season_datetime(season):
    start_timestamp, end_timestamp = get_season_timestamp(season)
    return (
     time_utility.get_utc8_datetime(timestamp=start_timestamp), time_utility.get_utc8_datetime(timestamp=end_timestamp))


def calc_dan_score--- This code section failed: ---

  89       0  LOAD_CONST            1  ''
           3  STORE_FAST            4  'total_score'

  90       6  SETUP_LOOP          233  'to 242'
           9  LOAD_GLOBAL           0  'range'
          12  LOAD_CONST            2  1
          15  LOAD_CONST            2  1
          18  BINARY_ADD       
          19  CALL_FUNCTION_2       2 
          22  GET_ITER         
          23  FOR_ITER            215  'to 241'
          26  STORE_FAST            5  'i'

  91      29  LOAD_FAST             5  'i'
          32  LOAD_GLOBAL           1  'dan_data'
          35  LOAD_ATTR             2  'LEGEND'
          38  COMPARE_OP            2  '=='
          41  POP_JUMP_IF_FALSE    62  'to 62'
          44  LOAD_FAST             5  'i'
          47  LOAD_FAST             0  'dan'
          50  COMPARE_OP            3  '!='
        53_0  COME_FROM                '41'
          53  POP_JUMP_IF_FALSE    62  'to 62'

  92      56  CONTINUE             23  'to 23'
          59  JUMP_FORWARD          0  'to 62'
        62_0  COME_FROM                '59'

  93      62  LOAD_GLOBAL           1  'dan_data'
          65  LOAD_ATTR             3  'get_lv_num'
          68  LOAD_FAST             5  'i'
          71  CALL_FUNCTION_1       1 
          74  STORE_FAST            6  'max_lv'

  94      77  LOAD_FAST             5  'i'
          80  LOAD_FAST             0  'dan'
          83  COMPARE_OP            2  '=='
          86  POP_JUMP_IF_FALSE    95  'to 95'
          89  LOAD_FAST             1  'lv'
          92  JUMP_FORWARD          3  'to 98'
          95  LOAD_CONST            2  1
        98_0  COME_FROM                '92'
          98  STORE_FAST            7  'min_lv'

  95     101  SETUP_LOOP          134  'to 238'
         104  LOAD_GLOBAL           0  'range'
         107  LOAD_FAST             6  'max_lv'
         110  LOAD_FAST             7  'min_lv'
         113  LOAD_CONST            2  1
         116  BINARY_SUBTRACT  
         117  LOAD_CONST            3  -1
         120  CALL_FUNCTION_3       3 
         123  GET_ITER         
         124  FOR_ITER            110  'to 237'
         127  STORE_FAST            8  'j'

  96     130  LOAD_FAST             5  'i'
         133  LOAD_FAST             0  'dan'
         136  COMPARE_OP            2  '=='
         139  POP_JUMP_IF_FALSE   167  'to 167'
         142  LOAD_FAST             8  'j'
         145  LOAD_FAST             1  'lv'
         148  COMPARE_OP            2  '=='
       151_0  COME_FROM                '139'
         151  POP_JUMP_IF_FALSE   167  'to 167'

  97     154  LOAD_FAST             2  'star'
         157  LOAD_CONST            2  1
         160  BINARY_SUBTRACT  
         161  STORE_FAST            9  'max_star'
         164  JUMP_FORWARD         39  'to 206'

  99     167  LOAD_GLOBAL           1  'dan_data'
         170  LOAD_ATTR             4  'get_star_num'
         173  LOAD_FAST             5  'i'
         176  CALL_FUNCTION_1       1 
         179  STORE_FAST            9  'max_star'

 100     182  LOAD_FAST             9  'max_star'
         185  LOAD_CONST            0  ''
         188  COMPARE_OP            3  '!='
         191  POP_JUMP_IF_FALSE   200  'to 200'
         194  LOAD_FAST             9  'max_star'
         197  JUMP_FORWARD          3  'to 203'
         200  LOAD_FAST             2  'star'
       203_0  COME_FROM                '197'
         203  STORE_FAST            9  'max_star'
       206_0  COME_FROM                '164'

 101     206  LOAD_CONST            1  ''
         209  STORE_FAST           10  'min_star'

 102     212  LOAD_FAST             4  'total_score'
         215  LOAD_CONST            4  100
         218  LOAD_FAST             9  'max_star'
         221  LOAD_CONST            2  1
         224  BINARY_ADD       
         225  LOAD_FAST            10  'min_star'
         228  BINARY_SUBTRACT  
         229  BINARY_MULTIPLY  
         230  INPLACE_ADD      
         231  STORE_FAST            4  'total_score'
         234  JUMP_BACK           124  'to 124'
         237  POP_BLOCK        
       238_0  COME_FROM                '101'
         238  JUMP_BACK            23  'to 23'
         241  POP_BLOCK        
       242_0  COME_FROM                '6'

 110     242  LOAD_FAST             4  'total_score'
         245  LOAD_FAST             3  'score'
         248  INPLACE_ADD      
         249  STORE_FAST            4  'total_score'

 112     252  LOAD_FAST             4  'total_score'
         255  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 19


def dan_compare(dan, lv, star, score, dan_2, lv_2, star_2, score_2):
    if dan != dan_2:
        return six_ex.compare(dan, dan_2)
    if lv != lv_2:
        return six_ex.compare(lv_2, lv)
    if star != star_2:
        return six_ex.compare(star, star_2)
    if score != score_2:
        return six_ex.compare(score, score_2)
    return 0


def get_head_frame_info_list():
    ret_list = []
    for k, v in six.iteritems(dan_data.data):
        if 'head_frame' not in v:
            ret_list.append({'dan': k,'info': None})
            continue
        ret_list.append({'dan': k,'info': v})

    return ret_list


def get_dan_frame_reward_redpoint():
    red_point_map = global_data.achi_mgr.get_cur_user_archive_data('dan_frame_reward_red_point_map', default={})
    return red_point_map


def clear_dan_frame_reward_redpoint():
    global_data.achi_mgr.set_cur_user_archive_data('dan_frame_reward_red_point_map', {})
    global_data.emgr.dan_head_frame_reward.emit()


def check_dan_frame_reward(dan_change_info):
    old_dan, new_dan = dan_change_info.get('dan')
    if old_dan == new_dan:
        return
    if 'head_frame' not in dan_data.data[new_dan]:
        return
    red_point_map = global_data.achi_mgr.get_cur_user_archive_data('dan_frame_reward_red_point_map', default={})
    for dan in six_ex.keys(red_point_map):
        if int(dan) > int(new_dan):
            del red_point_map[dan]

    red_point_map[new_dan] = True
    global_data.achi_mgr.set_cur_user_archive_data('dan_frame_reward_red_point_map', red_point_map)
    global_data.emgr.dan_head_frame_reward.emit()


def set_season_finish_ui_title(nd_lab, target_sub_str, target_sub_str_fixed, size, fontname, color):
    title = nd_lab.GetString()
    if type(title) == six.text_type:
        title = title.encode('utf-8')
    index = title.find(target_sub_str)
    if index != -1:
        pre, end = ('', '')
        if index != 0:
            pre += title[0:index - 1]
        end = title[index + 2:]
        title = pre + '<size=%s><fontname="%s"><color=%s>%s </color></fontname></size>' % (size, fontname, color, target_sub_str_fixed) + end
        title = '<align=0>' + title + '</align>'
        nd_lab.SetString(title)


def play_season_ui_sound(sound_name):
    return global_data.sound_mgr.play_ui_sound(sound_name)


def dan_lv_num_to_dan_info(total_lv, dan_len=3):
    used_lv_num = 0
    cur_dan = dan_data.BROZE
    cur_lv = dan_data.get_lv_num(cur_dan)
    for d in range(dan_data.BROZE, dan_data.LEGEND):
        lv_num = dan_data.get_lv_num(d)
        if used_lv_num + lv_num > total_lv:
            break
        used_lv_num += lv_num
        cur_dan = d + 1

    lv_num = dan_data.get_lv_num(cur_dan)
    left_lv = total_lv - used_lv_num
    cur_lv = lv_num - left_lv
    cur_star = 0
    if dan_len == 3:
        return [cur_dan, cur_lv, cur_star]
    return [cur_dan, cur_lv]


def dan_star_num_to_dan_info(total_star):
    used_star_num = 0
    cur_dan = dan_data.BROZE
    cur_lv = dan_data.get_lv_num(cur_dan)
    cur_star = 0
    for d in range(dan_data.BROZE, dan_data.LEGEND):
        lv_num = dan_data.get_lv_num(d)
        star_num = dan_data.get_star_num(d)
        if used_star_num + lv_num * (star_num + 1) > total_star:
            break
        used_star_num += lv_num * (star_num + 1)
        cur_dan = d + 1

    lv_num = dan_data.get_lv_num(cur_dan)
    star_num = dan_data.get_star_num(cur_dan)
    left_star = total_star - used_star_num
    if star_num is not None:
        got_lv_up = int(left_star / (star_num + 1))
        cur_lv = lv_num - got_lv_up
        cur_star = left_star - got_lv_up * (star_num + 1)
        return [
         cur_dan, cur_lv, cur_star]
    else:
        cur_lv = 1
        cur_star = left_star
        return [
         cur_dan, cur_lv, cur_star]
        return


def check_var_replacement--- This code section failed: ---

 242       0  LOAD_GLOBAL           0  'type'
           3  LOAD_FAST             0  'p'
           6  CALL_FUNCTION_1       1 
           9  LOAD_GLOBAL           1  'six'
          12  LOAD_ATTR             2  'text_type'
          15  LOAD_GLOBAL           3  'str'
          18  BUILD_LIST_2          2 
          21  COMPARE_OP            6  'in'
          24  POP_JUMP_IF_FALSE    95  'to 95'

 243      27  LOAD_FAST             0  'p'
          30  LOAD_ATTR             4  'startswith'
          33  LOAD_CONST            1  '$'
          36  CALL_FUNCTION_1       1 
          39  POP_JUMP_IF_FALSE    95  'to 95'

 244      42  POP_JUMP_IF_FALSE     2  'to 2'
          45  SLICE+1          
          46  STORE_FAST            0  'p'

 245      49  LOAD_FAST             0  'p'
          52  LOAD_FAST             1  'key_value_dict'
          55  COMPARE_OP            6  'in'
          58  POP_JUMP_IF_FALSE    69  'to 69'

 246      61  LOAD_FAST             1  'key_value_dict'
          64  LOAD_FAST             0  'p'
          67  BINARY_SUBSCR    
          68  RETURN_END_IF    
        69_0  COME_FROM                '58'

 248      69  LOAD_GLOBAL           5  'log_error'
          72  LOAD_CONST            3  'cannot find key %s in key value map!'
          75  LOAD_FAST             0  'p'
          78  BINARY_MODULO    
          79  LOAD_FAST             2  'func_str'
          82  LOAD_FAST             1  'key_value_dict'
          85  CALL_FUNCTION_3       3 
          88  POP_TOP          
          89  JUMP_ABSOLUTE        95  'to 95'
          92  JUMP_FORWARD          0  'to 95'
        95_0  COME_FROM                '92'

 249      95  LOAD_FAST             0  'p'
          98  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 42


def parse_func_param_str_with_dict(func_str, key_value_dict=None):
    if not key_value_dict:
        key_value_dict = {}
    import json
    func = ''
    param_list = []
    param_dict = {}
    split_str = func_str.split(':')
    len_split_str = len(split_str)
    if len_split_str <= 0:
        return (
         func, param_list, param_dict)
    if len_split_str == 1:
        if split_str[0].find('=') >= 0:
            param_list_str = split_str[0]
        else:
            func = split_str[0]
            param_list_str = ''
    elif len_split_str == 2:
        func = split_str[0]
        param_list_str = split_str[1]
    else:
        func = ''
        param_list_str = ''
    param_list_str = param_list_str.strip()
    if param_list_str:
        if param_list_str.startswith('['):
            if not param_list_str.endswith(']'):
                log_error('can not find left ]', func, param_list_str)
                return (
                 func, param_list, param_dict)
            param_list_str = param_list_str[1:-1]
            param_list = param_list_str.split(',')
            for i, param in enumerate(param_list):
                param_list[i] = param.strip()

        else:
            at_param_list = param_list_str.split('@')
            for i, key_value in enumerate(at_param_list):
                s = key_value.split('=')
                k = s[0].strip()
                param_dict[k] = s[1].strip()
                if param_dict[k][0] == '[' and param_dict[k][-1] == ']':
                    param_dict[k] = json.loads(param_dict[k])

    for idx, p in enumerate(param_list):
        out_p = check_var_replacement(p, key_value_dict, func_str)
        if out_p != p:
            param_list[idx] = out_p

    for k in list(six_ex.keys(param_dict)):
        p = param_dict[k]
        out_p = check_var_replacement(p, key_value_dict, func_str)
        if out_p != p:
            param_dict[k] = out_p

    return (func, param_list, param_dict)


def get_func_ret_with_dict(func_str, key_value_dict=None, default=None):
    if not func_str.startswith('$'):
        _func_str, _param_list, _param_dict = parse_func_param_str_with_dict(func_str, key_value_dict)
        if _func_str:
            from logic.gutils import season_memory_utils
            func = getattr(season_memory_utils, _func_str)
            if callable(func):
                return func(*_param_list, **_param_dict)
        return default
    else:
        return check_var_replacement(func_str, key_value_dict)


def get_season_memory_info(check_type, season_data, in_key_value_map=None, text_key_val_dict=None):
    can_show_achievements = {}
    day_dict = {}
    text_dict = {}
    if not text_key_val_dict:
        text_key_val_dict = {}
    for key, key_conf in six.iteritems(check_type):
        if key not in season_data and not key_conf.get('ret_format'):
            continue
        new_keys = key_conf.get('new_keys', [])
        if new_keys:
            if any([ new_key in season_data for new_key in new_keys ]):
                continue
        key_data = season_data.get(key)
        key_value_map = {'uid_v': key_data,'dict_v': season_data}
        if in_key_value_map:
            key_value_map.update(in_key_value_map)
        predefine_key_value_map = key_conf.get('key_value_map', '')
        if predefine_key_value_map:
            for _k, _v in six.iteritems(predefine_key_value_map):
                key_value_map[_k] = get_func_ret_with_dict(_v, key_value_map)

        ret_format = key_conf.get('ret_format')
        if ret_format:
            ret_val = get_func_ret_with_dict(ret_format, key_value_map)
        else:
            ret_val = key_data
        key_value_map['ret_v'] = ret_val
        day_format = key_conf.get('day_format')
        if day_format:
            day_dict[key] = get_func_ret_with_dict(day_format, key_value_map, 0)
        min_val = None
        min_format = key_conf.get('min_format')
        require_min_value = key_conf.get('min_value')
        ty = key_conf['ty']
        can_show_achievements.setdefault(ty, [])
        if require_min_value is not None:
            if min_format:
                min_val = get_func_ret_with_dict(min_format, key_value_map)
            else:
                min_val = ret_val
            if min_val >= require_min_value - 1e-05:
                can_show_achievements[ty].append(key)
        else:
            can_show_achievements[ty].append(key)
        txt_fillup = key_conf.get('txt_fillup')
        achi_desc = key_conf.get('achieve_tid')
        if txt_fillup:
            text_parameters = [ get_func_ret_with_dict(i, key_value_map) for i in txt_fillup ]
            try:
                txt = get_text_by_id(achi_desc).format(*text_parameters, **text_key_val_dict)
            except:
                log_error('failed to format tid:', achi_desc, text_parameters, text_key_val_dict)
                txt = ''

            text_dict[key] = txt
        else:
            try:
                txt = get_text_by_id(achi_desc).format(*[ret_val if min_val is None else min_val], **text_key_val_dict)
            except:
                log_error('failed to format tid:', achi_desc, [ret_val if min_val is None else min_val], text_key_val_dict)
                txt = ''

            text_dict[key] = txt

    return (can_show_achievements, day_dict, text_dict)


def filter_and_sort_season_memory(check_type_table, can_show_achievements, day_dict, max_count=6, require_day_gap=3):
    filtered_data = []
    for ty in sorted(six.iterkeys(can_show_achievements)):
        key_list = can_show_achievements[ty]
        if key_list:
            min_key = min(key_list, key=lambda x: check_type_table[x].get('sort_id'))
            filtered_data.append(min_key)

    sorted_one = sorted(filtered_data, key=lambda x: [check_type_table[x].get('ty'), check_type_table[x].get('sort_id')])
    return sorted_one[:max_count]


def get_mecha_best_region_rank(mecha_id):
    from logic.gcommon.common_const import rank_const
    from logic.gcommon.common_const import rank_region_const
    from logic.gutils import locate_utils
    title_data_list = locate_utils.get_rank_title_list(rank_const.RANK_TITLE_MECHA_REGION)
    target_title_data_list = []
    if title_data_list:
        for title_data in title_data_list:
            title_type, region_type, mecha_type, rank_adcode, rank, rank_expire = title_data
            if str(mecha_id) == str(mecha_type):
                target_title_data_list.append(title_data)

        if target_title_data_list:
            return target_title_data_list[0]
        else:
            return None

    else:
        return None
    return None


class SeasonMemoryListTabWidget(object):

    def __init__(self, list_tab, ui_class_name):
        self.single_choose_widget = None
        self.list_tab = list_tab
        self._is_for_season_pass = False
        self._ui_class_name = ui_class_name
        self.init_list()
        return

    def set_is_for_season_pass(self):
        self._is_for_season_pass = True
        self.init_list()

    def destroy(self):
        self.list_tab = None
        return

    def init_list(self):
        show_list_dict = self.get_show_list()
        show_list = six_ex.keys(show_list_dict)
        if self._ui_class_name in show_list_dict:
            idx = show_list.index(self._ui_class_name)
            if idx > (global_data.max_season_mem_show_index or 0):
                global_data.max_season_mem_show_index = idx
        self.init_single_choose_widget(show_list_dict)
        if self._ui_class_name in show_list_dict:
            idx = show_list.index(self._ui_class_name)
            ui_item = self.list_tab.GetItem(idx)
            if ui_item:
                ui_item.btn_choose.SetSelect(True)

    def init_single_choose_widget(self, show_list_dict):
        show_list = six_ex.keys(show_list_dict)
        if not self._is_for_season_pass:
            self.list_tab.SetInitCount(len(show_list[:(global_data.max_season_mem_show_index or 0) + 1]))
        else:
            self.list_tab.SetInitCount(len(show_list))
        for idx in range(len(show_list)):
            ui_item = self.list_tab.GetItem(idx)
            if ui_item:
                ui_item.btn_choose.SetSelect(False)

                @ui_item.btn_choose.callback()
                def OnClick(btn, touch, key=show_list[idx]):
                    if key == self._ui_class_name:
                        return
                    func = show_list_dict[key]
                    if func:
                        global_data.ui_mgr.close_ui(self._ui_class_name)
                        func()

    def get_show_list(self):
        from collections import OrderedDict
        if not (global_data.player and global_data.player.season_stat):
            return OrderedDict()

        def open_1(_is_for_season_pass=self._is_for_season_pass):
            from logic.comsys.battle_pass.season_memory.SeasonAchievementMemoryUI import SeasonAchievementMemoryUI
            ui = SeasonAchievementMemoryUI()
            if ui and _is_for_season_pass:
                ui.play_for_SeasonPassUI()

        def open_2(_is_for_season_pass=self._is_for_season_pass):
            from logic.comsys.battle_pass.season_memory.SeasonMechaMemoryUI import SeasonMechaMemoryUI
            ui = SeasonMechaMemoryUI()
            if ui and _is_for_season_pass:
                ui.play_for_SeasonPassUI()

        def open_3(_is_for_season_pass=self._is_for_season_pass):
            from logic.comsys.battle_pass.season_memory.SeasonFriendMemoryUI import SeasonFriendMemoryUI
            ui = SeasonFriendMemoryUI()
            if ui and _is_for_season_pass:
                ui.play_for_SeasonPassUI()

        show_list_dict = OrderedDict()
        season_stat = global_data.player.season_stat
        if season_stat.get('sst_day_dan', []):
            show_list_dict['SeasonAchievementMemoryUI'] = open_1
        if season_stat.get('sst_mecha_stat'):
            show_list_dict['SeasonMechaMemoryUI'] = open_2
        if sum([ i.get('sst_frd_game_cnt', 0) for i in six.itervalues(season_stat.get('sst_frd_stat', {})) ]) >= 5:
            show_list_dict['SeasonFriendMemoryUI'] = open_3
        return show_list_dict

    @staticmethod
    def has_all_showed--- This code section failed: ---

 535       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'ui_mgr'
           6  LOAD_ATTR             2  'get_ui'
           9  LOAD_CONST            1  'SeasonPassUI'
          12  CALL_FUNCTION_1       1 
          15  POP_JUMP_IF_FALSE    22  'to 22'

 536      18  LOAD_GLOBAL           3  'True'
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 537      22  LOAD_CONST            2  ''
          25  STORE_FAST            0  'count'

 538      28  LOAD_GLOBAL           0  'global_data'
          31  LOAD_ATTR             4  'player'
          34  LOAD_ATTR             5  'season_stat'
          37  STORE_FAST            1  'season_stat'

 539      40  LOAD_FAST             1  'season_stat'
          43  LOAD_ATTR             6  'get'
          46  LOAD_CONST            3  'sst_day_dan'
          49  BUILD_LIST_0          0 
          52  CALL_FUNCTION_2       2 
          55  POP_JUMP_IF_FALSE    68  'to 68'

 540      58  POP_JUMP_IF_FALSE     4  'to 4'
          61  INPLACE_ADD      
          62  STORE_FAST            0  'count'
          65  JUMP_FORWARD          0  'to 68'
        68_0  COME_FROM                '65'

 541      68  LOAD_FAST             1  'season_stat'
          71  LOAD_ATTR             6  'get'
          74  LOAD_CONST            5  'sst_mecha_stat'
          77  CALL_FUNCTION_1       1 
          80  POP_JUMP_IF_FALSE    93  'to 93'

 542      83  POP_JUMP_IF_FALSE     4  'to 4'
          86  INPLACE_ADD      
          87  STORE_FAST            0  'count'
          90  JUMP_FORWARD          0  'to 93'
        93_0  COME_FROM                '90'

 543      93  LOAD_GLOBAL           7  'sum'
          96  BUILD_LIST_0          0 
          99  LOAD_GLOBAL           8  'six'
         102  LOAD_ATTR             9  'itervalues'
         105  LOAD_FAST             1  'season_stat'
         108  LOAD_ATTR             6  'get'
         111  LOAD_CONST            6  'sst_frd_stat'
         114  BUILD_MAP_0           0 
         117  CALL_FUNCTION_2       2 
         120  CALL_FUNCTION_1       1 
         123  GET_ITER         
         124  FOR_ITER             24  'to 151'
         127  STORE_FAST            2  'i'
         130  LOAD_FAST             2  'i'
         133  LOAD_ATTR             6  'get'
         136  LOAD_CONST            7  'sst_frd_game_cnt'
         139  LOAD_CONST            2  ''
         142  CALL_FUNCTION_2       2 
         145  LIST_APPEND           2  ''
         148  JUMP_BACK           124  'to 124'
         151  CALL_FUNCTION_1       1 
         154  LOAD_CONST            8  5
         157  COMPARE_OP            5  '>='
         160  POP_JUMP_IF_FALSE   173  'to 173'

 544     163  POP_JUMP_IF_FALSE     4  'to 4'
         166  INPLACE_ADD      
         167  STORE_FAST            0  'count'
         170  JUMP_FORWARD          0  'to 173'
       173_0  COME_FROM                '170'

 545     173  LOAD_GLOBAL           0  'global_data'
         176  LOAD_ATTR            10  'max_season_mem_show_index'
         179  JUMP_IF_TRUE_OR_POP   185  'to 185'
         182  LOAD_CONST            2  ''
       185_0  COME_FROM                '179'
         185  LOAD_CONST            4  1
         188  BINARY_SUBTRACT  
         189  COMPARE_OP            5  '>='
         192  STORE_FAST            3  'is_all_showed'

 546     195  LOAD_FAST             3  'is_all_showed'
         198  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 58


def nd_touch_direction_helper(nd_touch, left_func=None, right_func=None, up_func=None, down_func=None):

    @nd_touch.callback()
    def OnEnd(btn, touch):
        start_wpos = touch.getStartLocation()
        wpos = touch.getLocation()
        dx = wpos.x - start_wpos.x
        dy = wpos.y - start_wpos.y
        if abs(dx) > 15 and abs(dx) > 2 * abs(dy):
            if dx > 0:
                if left_func:
                    left_func()
            elif right_func:
                right_func()
        elif abs(dy) > 15 and abs(dy) > 2 * abs(dx):
            if dy > 0:
                if up_func:
                    up_func()
            elif down_func:
                down_func()


def get_season_memory_other_achievement(mecha_data, mecha_id, max_count=6, require_day_gap=3):
    check_type_table = confmgr.get('season_memory_conf', 'MechaMemoryConf', 'Content', default={})
    name_dict = {'mechaname': item_utils.get_mecha_name_by_id(mecha_id)}
    mecha_memory, day_dict, text_dict = get_season_memory_info(check_type_table, mecha_data, {'mecha_id': mecha_id}, name_dict)
    other_achievements = filter_and_sort_season_memory(check_type_table, mecha_memory, day_dict, max_count, require_day_gap)
    return (
     other_achievements, day_dict, text_dict)