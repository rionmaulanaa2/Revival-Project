# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/lobby_answering_system_utils.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from logic.gutils.task_utils import get_task_conf_by_id
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon import time_utility
ALL_SUPPORT_LANG_NAME = {
 'cn', 'en', 'tw', 'jp'}
SCORE_PIC_DIR_PATH = 'gui/ui_res_2/txt_pic/text_pic_{}/answer/'
SCORE_PIC_NAME = 'txt_answer_score_0{}.png'
SCORE_BG_PIC_PATH = 'gui/ui_res_2/answer/bar_answer_score_0{}.png'
MAX_INDEX = 5
ANSWER_TASK_ID = '1440200'
ANSWER_UI_OPEN_KEY = 'LobbyASMainUI'

def can_open_answer_ui():
    if not global_data.player:
        return False
    question_count = len(global_data.player.get_cur_question())
    answered_count = len(global_data.player.get_cur_answers())
    if question_count == answered_count and not global_data.player.is_prog_reward_receivable(ANSWER_TASK_ID, 0):
        return False
    return True


def is_today_open_answer_ui():
    if not global_data.player:
        return True
    archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
    open_time = archive_data.get_field(ANSWER_UI_OPEN_KEY, '')
    server_time = time_utility.get_server_time()
    today_date_desc = time_utility.get_date_str(timestamp=server_time)
    return open_time == today_date_desc


def update_open_answer_ui_time():
    if not global_data.player:
        return
    server_time = time_utility.get_server_time()
    today_date_desc = time_utility.get_date_str(timestamp=server_time)
    archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
    archive_data.set_field(ANSWER_UI_OPEN_KEY, today_date_desc)


def clear_open_answer_ui_time():
    archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
    archive_data.set_field(ANSWER_UI_OPEN_KEY, '')


def get_question_count():
    if global_data.player:
        return len(global_data.player.get_cur_question())
    return 0


def get_right_answer_count():
    if not global_data.player:
        return 0
    question_list = global_data.player.get_cur_question()
    answered_info = global_data.player.get_cur_answers()
    conf = confmgr.get('question_system_config', 'QuestionsConfig', 'Content')
    right_answer_count = 0
    for question_id in question_list:
        true_answer = conf[question_id]['answer']
        if answered_info[question_id] == true_answer:
            right_answer_count += 1

    return right_answer_count


def get_score_pic(right_answer_count=None):
    if right_answer_count is None:
        right_answer_count = get_right_answer_count()
    cur_lang_name = get_cur_lang_name()
    if cur_lang_name not in ALL_SUPPORT_LANG_NAME:
        dir_path = SCORE_PIC_DIR_PATH.format('en')
    else:
        dir_path = SCORE_PIC_DIR_PATH.format(cur_lang_name)
    pic_index = get_question_count() - right_answer_count + 1
    if pic_index > MAX_INDEX:
        pic_index = MAX_INDEX
    return (dir_path + SCORE_PIC_NAME.format(pic_index), SCORE_BG_PIC_PATH.format(pic_index))


def refresh_reward_info(nd_list, prog=None):
    reward_info = {}
    task_conf = get_task_conf_by_id(ANSWER_TASK_ID)
    reward_conf = confmgr.get('common_reward_data')
    prog_rewards = task_conf.get('prog_rewards', [])
    if prog is None:
        prog = task_conf.get('total_prog', 4)
    for i in range(prog + 1):
        _, reward_id = prog_rewards[i]
        for item_id, count in reward_conf.get(str(reward_id), {}).get('reward_list', []):
            if item_id not in reward_info:
                reward_info[item_id] = count
            else:
                reward_info[item_id] += count

        nd_list.SetInitCount(len(reward_info))

    for index, (item_id, count) in enumerate(six.iteritems(reward_info)):
        nd_item = nd_list.GetItem(index)
        if nd_item.temp_item:
            nd_item = nd_item.temp_item
        init_tempate_mall_i_item(nd_item, item_id, count, show_tips=True)

    return


def check_auto_receive_lobby_answering_system_reward():
    if not global_data.player:
        return
    if not global_data.player.get_cur_answers():
        return
    if len(global_data.player.get_cur_answers()) == len(global_data.player.get_cur_question()):
        if global_data.player.is_prog_reward_receivable(ANSWER_TASK_ID, 0):
            global_data.player.receive_all_task_prog_reward(ANSWER_TASK_ID)