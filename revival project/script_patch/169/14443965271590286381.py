# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/lobby_item_use_handler.py
from __future__ import absolute_import
from six.moves import range
from data import lobby_item_use_conf
from data.lobby_item_data import get_item_use_type, get_item_use_parms
import sys
from logic.gcommon import const
from . import item_utility as iutil
from data.lobby_item_data import get_recycle_gain_item_list
import logic.gcommon.time_utility as tutil
import logic.gcommon.cdata.bond_config as bond_conf
from logic.gcommon.common_const import rank_const as rconst

def do_item_use_hander(owner, item_no, cnt, params=None):
    use_type = get_item_use_type(item_no)
    if not use_type:
        log_error('do_item_use_hander, use_type not exist! item_no=%s', item_no)
        return False
    else:
        use_conf = lobby_item_use_conf.GetUseConf().get(use_type, {})
        if not use_conf:
            log_error('do_item_use_hander, use_conf not exist! use_type=%s', use_type)
            return False
        func_name = use_conf.get('FuncName')
        mod = sys.modules[__name__]
        if hasattr(mod, func_name):
            if params is None:
                params = {}
            params.update(get_item_use_parms(item_no, {}))
            ret = getattr(mod, func_name)(owner, item_no, cnt, params)
            if ret not in [True, False]:
                log_error('Please return True or False in handler! func_name=%s', func_name)
                return True
            return ret
        log_error('do_item_use_hander, hander not exist! hander=%s', func_name)
        return False
        return


def experience_card(avatar, item_no, cnt, ext_info):
    add_item_no = ext_info['add_item']
    add_time = ext_info['time']
    if not iutil.is_item_timeliness(add_item_no):
        return False
    cur_item = avatar.get_item_by_no(add_item_no)
    if cur_item and cur_item.get_expire_time() < 0:
        gain_item_list = get_recycle_gain_item_list(item_no, [])
        item_dict = {}
        for gain_item_no, gain_cnt in gain_item_list:
            item_dict[gain_item_no] = gain_cnt * cnt

        avatar.offer_reward_by_dict({'item_dict': item_dict}, const.ITEM_RECYCLE_REASON)
        return True
    avatar.offer_reward_by_dict({'expire_item': {add_item_no: add_time * cnt}}, const.EXPIRE_ITEM_USE_REASON)
    return True


def add_exp(avatar, item_no, cnt, ext_info):
    exp = ext_info['exp'] * cnt
    avatar.add_exp(exp, 'USE-ITEM-%s' % item_no, True)
    return True


def add_duo_exp_time(avatar, item_no, cnt, ext_info):
    day = ext_info.get('day', 0) * cnt
    hour = ext_info.get('hour', 0) * cnt
    time_change = day * tutil.ONE_DAY_SECONDS + hour * tutil.ONE_HOUR_SECONS
    avatar.add_duo_exp_time(time_change, 'USE_ITEM_%s' % item_no, {item_no: cnt})
    return True


def add_duo_exp_point(avatar, item_no, cnt, ext_info):
    point = ext_info['point'] * cnt
    avatar.add_duo_exp_point(point, 'USE_ITEM_%s' % item_no, {item_no: cnt})
    return True


def proficiency_card(avatar, item_no, cnt, ext_info):
    prof = ext_info['prof'] * cnt
    mecha_type = ext_info['mecha_type']
    avatar.add_proficiency(mecha_type, prof, 'USE_ITEM_%s' % item_no, {item_no: cnt})
    return True


def add_duo_prof_time(avatar, item_no, cnt, ext_info):
    day = ext_info.get('day', 0) * cnt
    hour = ext_info.get('hour', 0) * cnt
    time_change = day * tutil.ONE_DAY_SECONDS + hour * tutil.ONE_HOUR_SECONS
    avatar.add_duo_prof_time(time_change, 'USE_ITEM_%s' % item_no, {item_no: cnt})
    return True


def add_duo_prof_point(avatar, item_no, cnt, ext_info):
    point = ext_info['point'] * cnt
    avatar.add_duo_prof_point(point, 'USE_ITEM_%s' % item_no, {item_no: cnt})
    return True


def give_reward(avatar, item_no, cnt, ext_info):
    reward_id = ext_info['reward_id']
    cur_cnt = 0
    while cur_cnt < cnt:
        reward_dict, reason = avatar.offer_reward_by_id(reward_id)
        if reward_dict is None:
            return False
        cur_cnt += 1

    return True


def give_gift_reward(avatar, item_no, cnt, ext_info):
    reward_id = ext_info['reward_id']
    if not reward_id or cnt <= 0:
        return False
    reward_ids = [ reward_id for i in range(cnt) ]
    avatar.offer_reward_by_ids(reward_ids)
    return True


def give_lv_gift_reward(avatar, item_no, cnt, ext_info):
    lv_reward_id = ext_info['lv_reward_id']
    if not lv_reward_id or cnt <= 0:
        return False
    lv = avatar.get_lv()
    for reward_lv, reward_id in lv_reward_id:
        if lv <= reward_lv:
            break

    reward_ids = [ reward_id for i in range(cnt) ]
    avatar.offer_reward_by_ids(reward_ids)
    return True


def register_contact(avatar, item_no, cnt, ext_info):
    contact = ext_info.get('contact', None)
    if not contact or not isinstance(contact, (tuple, list)) or len(contact) != 6:
        avatar.logger.error('[Avatar %s] register contact error: %s', avatar.uid, contact)
        return False
    else:
        item = ext_info['item']
        item.set_contact(contact)
        avatar.sa_log_product_use(item.id, item_no, contact)
        title = pack_text(601200)
        content = pack_text(601201, (','.join([ str(c) for c in contact ]),))
        sender = pack_text(864000)
        avatar.send_mail(title, content, sender, reason='REG_CONTACT_%s' % item_no)
        return True


def use_task_card(avatar, item_no, cnt, ext_info):
    task_id = ext_info.get('task_id', None)
    if not task_id:
        return False
    else:
        avatar._task_prog_statistics.set_task_finished(task_id)
        avatar.receive_reward_by_id(task_id)
        return True


def select_rewards(avatar, item_no, cnt, ext_info):
    select = ext_info.get('select', 0)
    reward_list = ext_info.get('reward_list', ())
    len_rewardlist = len(reward_list)
    selection = ext_info.get('selection', ())
    if not selection or len(selection) != select or not select or select > len_rewardlist:
        return False
    real_rewardlist = []
    for i in range(cnt):
        filter_set = set([])
        for idx in selection:
            if idx >= len_rewardlist or idx < 0 or idx in filter_set:
                return False
            filter_set.add(idx)
            real_rewardlist.append(reward_list[idx])

    reason_str = '%s_%s' % (const.ITEM_USE_REASON, item_no)
    avatar.offer_reward_by_ids(real_rewardlist, reason_str)
    return True


def select_multi_rewards(avatar, item_no, cnt, ext_info):
    reward_list = ext_info.get('reward_list', ())
    len_reward_list = len(reward_list)
    selection = ext_info.get('selection', ())
    try:
        real_reward_list = []
        reward_num = 0
        for idx, num in selection:
            reward_num += num
            real_reward_list.extend([reward_list[idx]] * num)

    except:
        log_error('[Avatar %s-%s] multi_select_rewards, item_no = %s, cnt = %s, selections = %s', avatar.uid, avatar.id, item_no, cnt, selection)
        return False

    reason_str = '%s_%s' % (const.ITEM_USE_REASON, item_no)
    avatar.offer_reward_by_ids(real_reward_list, reason_str)
    return True


def select_single_reward(avatar, item_no, cnt, ext_info):
    reward_list = ext_info.get('reward_list', ())
    select_reward_id = ext_info.get('select_reward_id', 0)
    if select_reward_id not in reward_list:
        log_error('[Avatar %s-%s] select_single_rewards, item_no = %s, cnt = %s, select_reward_id = %s', avatar.uid, avatar.id, item_no, cnt, select_reward_id)
        return False
    reason_str = '%s_%s' % (const.ITEM_USE_REASON, item_no)
    avatar.offer_reward_by_id(select_reward_id, reason_str)
    return True


def settle_item_title(avatar, item_no, cnt, ext_info):
    expire_time = ext_info.get('expire_time', -1)
    title_id = str(item_no)
    if expire_time >= 0:
        now = tutil.get_time()
        title_expire = avatar.get_rank_title_data(rconst.RANK_TITLE_ITEM, title_id)
        if title_expire is None or now > title_expire:
            expire_time = now + expire_time
        else:
            expire_time = title_expire + expire_time
    else:
        expire_time = ext_info.get('expire_date_time', -1)
    avatar.settle_rank_title(rconst.RANK_TITLE_ITEM, {title_id: expire_time})
    return True


def use_bond_item(avatar, item_no, cnt, ext_info):
    role_id = ext_info['role_id']
    role_id = int(role_id)
    bond_value = bond_conf.get_bond_gain_effect(item_no, role_id) * cnt
    avatar.add_role_bond(role_id, bond_value, 'USE_ITEM_%s' % item_no, {item_no: cnt})
    return True


def use_bond_gift_upgrade_item(avatar, item_no, cnt, ext_info):
    gift_id = ext_info['gift_id']
    return avatar.upgrade_role_bond_gift(gift_id, item_no, cnt)


def use_intimacy_gift(avatar, item_no, cnt, ext_info):
    return avatar.process_intimacy_lv_by_intimacy_gift(item_no, cnt, ext_info)