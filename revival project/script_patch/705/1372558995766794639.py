# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMeowCoin.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.cdata import meow_capacity_config
from logic.gcommon.common_utils.local_text import get_text_by_id

class ComMeowCoin(UnitCom):
    BIND_EVENT = {'E_ON_MEOW_COIN_UPDATE': '_on_update_coin',
       'E_ON_MAIL_MEOW_COIN_RESULT': '_on_mail_coin_result',
       'E_TRY_MAIL_MEOW_COIN': '_try_mail_meow_coin',
       'G_MEOW_BAG_INFO': 'get_bag_info',
       'G_MEOW_SAFE_BOX_INFO': 'get_safe_box_info',
       'G_MEOW_MAIL_BOX_INFO': 'get_mail_box_info',
       'G_MAIL_TOTAL_TIMES': 'get_mail_total_times',
       'G_WEEK_LIMIT_NUM': 'get_week_limit_num',
       'G_HAVE_SENT_MAIL': 'have_sent_mail'
       }

    def __init__(self):
        super(ComMeowCoin, self).__init__(need_update=False)
        self._meow_capacity_lvs = {}
        self._bag_num = 0
        self._mail_total_times = 0
        self._mail_total_num = 0
        self._week_carry_out_num = 0
        self._mail_used_set = set()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMeowCoin, self).init_from_dict(unit_obj, bdict)
        self._meow_capacity_lvs = bdict.get('meow_capacity_lvs', {})
        self._week_carry_out_num = bdict.get('meow_week_carry_num', 0)
        self._bag_num = bdict.get('meow_bag_num', 0)
        self._mail_total_times = bdict.get('meow_mail_total_times', 0)
        self._mail_total_num = bdict.get('meow_mail_total_num', 0)
        mail_used = bdict.get('meow_mail_used_set', [])
        self._mail_used_set = set(mail_used) if mail_used else set()

    def get_meow_capacity_lv(self, capacity_type):
        return self._meow_capacity_lvs.get(capacity_type, meow_capacity_config.capacity_init_lv)

    def get_meow_capacity_size(self, capacity_type):
        lv = self.get_meow_capacity_lv(capacity_type)
        return meow_capacity_config.get_capacity_size(capacity_type, lv)

    def _on_update_coin(self, bag_num, total_mail_times, total_mail_num):
        self._bag_num = bag_num
        self._mail_total_times = total_mail_times
        self._mail_total_num = total_mail_num
        self.send_event('E_MEOW_COIN_CHANGE')

    def _on_mail_coin_result(self, error_code, num, bag_num, total_mail_times, total_mail_num, mail_id):
        if error_code <= 0:
            self._bag_num = bag_num
            self._mail_total_times = total_mail_times
            self._mail_total_num = total_mail_num
            self._mail_used_set.add(mail_id)
            self.send_event('E_MEOW_COIN_CHANGE')
        else:
            global_data.game_mgr.show_tip(get_text_by_id(error_code))

    def _try_mail_meow_coin(self, mailbox_id, num):
        if not self._can_mail_meow_coin(num):
            return
        self.send_event('E_CALL_SYNC_METHOD', 'try_mail_meow_coin', (mailbox_id, num), True, True)

    def have_sent_mail(self, post_box_id):
        return post_box_id and post_box_id in self._mail_used_set

    def _can_mail_meow_coin(self, num):
        if num <= 0:
            return False
        if num > self.get_meow_capacity_size(meow_capacity_config.capacity_type_mail_box):
            return False
        if num > self._bag_num:
            return False
        return True

    def get_mail_total_times(self):
        return self._mail_total_times

    def get_week_limit_num(self):
        return self._mail_total_num + self._week_carry_out_num

    def get_bag_info(self):
        return (
         self._bag_num, self.get_meow_capacity_size(meow_capacity_config.capacity_type_bag))

    def get_safe_box_info(self):
        size = self.get_meow_capacity_size(meow_capacity_config.capacity_type_safe_box)
        return (
         min(self._bag_num, size), size)

    def get_mail_box_info(self):
        return (
         self._mail_total_num, self.get_meow_capacity_size(meow_capacity_config.capacity_type_mail_box), self._mail_total_times)