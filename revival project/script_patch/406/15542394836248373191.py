# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/Item.py
from __future__ import absolute_import
import six
from mobile.common.IdManager import IdManager
from .. import time_utility as tutil
from . import item_const as iconst
from . import lobby_item_type as litem_type

class Item(object):
    __slots__ = ('__dict__', 'id', 'item_no', 'name', 'type', 'rare_degree', 'discardable',
                 'desc', 'use_lv', 'use_sex', 'tradeable', 'create_time', 'current_stack_num',
                 'max_stack_num', 'unlock_time', 'timeliness', 'expire_time', 'sort_key',
                 'rp', 'forbid_charm')

    def __init__(self, item_id=None, create_time=None):
        super(Item, self).__init__()
        self.id = str(IdManager.genid()) if item_id is None else item_id
        self.item_no = 0
        self.name = ''
        self.type = litem_type.L_ITEM_TYPE_UNKONW_ITEM
        self.rare_degree = -1
        self.discardable = True
        self.desc = ''
        self.use_lv = None
        self.use_sex = None
        self.tradeable = False
        self.create_time = create_time
        self.current_stack_num = 1
        self.max_stack_num = 1
        self.unlock_time = 0
        self.timeliness = 0
        self.expire_time = -1
        self.sort_key = 0
        self.rp = False
        self.forbid_charm = False
        return

    def init_from_dict(self, pdict):
        for key, val in six.iteritems(pdict):
            setattr(self, key, val)

    def __str__(self):
        return 'Item {id=%s no=%s type=%s}' % (self.id, self.item_no, self.type)

    def is_valid(self):
        if self.current_stack_num <= 0:
            return False
        if self.max_stack_num == 1 and self.current_stack_num > 1:
            return False
        return True

    def get_persistent_dict(self):
        pdict = {'id': self.id,
           'item_no': self.item_no,
           'unlock_time': self.unlock_time,
           'current_stack_num': self.current_stack_num,
           'expire_time': self.expire_time,
           'create_time': self.create_time
           }
        if self.rp:
            pdict['rp'] = self.rp
        return pdict

    def get_client_dict(self):
        cdict = {'id': self.id,
           'item_no': self.item_no,
           'unlock_time': self.unlock_time,
           'current_stack_num': self.current_stack_num,
           'expire_time': self.expire_time,
           'create_time': self.create_time
           }
        if self.rp:
            cdict['rp'] = self.rp
        return cdict

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_degree(self):
        return self.rare_degree

    def get_item_no(self):
        return self.item_no

    def get_desc(self):
        return self.desc

    def get_create_time(self):
        return self.create_time

    def get_current_stack_num(self):
        return self.current_stack_num

    def set_stack_num(self, current_num):
        self.current_stack_num = max(0, current_num)

    def increase_stack_num(self, inc_num):
        if self.current_stack_num + inc_num > self.max_stack_num:
            return False
        if inc_num <= 0:
            return False
        self.current_stack_num += inc_num
        self.create_time = tutil.time()
        return True

    def reduce_stack_num(self, reduce_num):
        if reduce_num < 0:
            return False
        else:
            if self.current_stack_num > reduce_num:
                self.current_stack_num -= reduce_num
                return True
            if self.current_stack_num < reduce_num:
                return False
            return False

    def can_discard(self):
        return self.discardable

    def can_stack(self):
        return self.max_stack_num > 1

    def can_trade(self):
        return self.tradeable

    def can_use(self, sex, lv):
        if self.is_expire():
            return False
        return True

    def can_use_recycle(self):
        return True

    def is_unknow_item(self):
        return self.type == litem_type.L_ITEM_TYPE_UNKONW_ITEM

    def is_icon_item(self):
        return self.type == litem_type.L_ITEM_TYPE_ICON

    def is_illegal_item(self):
        return self.type == litem_type.L_ITEM_TYPE_UNKONW_ITEM or self.type == litem_type.L_ITEM_TYPE_ICON

    def is_knapsack_item(self):
        return self.type in litem_type.ITEM_TYPE_KNAPSACK

    def is_bodice_item(self):
        return False

    def is_bottoms_item(self):
        return False

    def is_head_item(self):
        return False

    def is_head_frame(self):
        return self.type == litem_type.L_ITEM_TYPE_HEAD_FRAME

    def is_head_photo(self):
        return self.type == litem_type.L_ITEM_TYPE_HEAD_PHOTO

    def is_chat_item(self):
        return self.type == litem_type.L_ITEM_TYPE_TALKING

    def is_timeliness_item(self):
        return self.timeliness

    def is_permanent_item(self):
        return self.get_expire_time() < 0

    def is_skin_item(self):
        return self.type in litem_type.ITEM_TYPE_SKIN

    def is_mecha_skin_item(self):
        return self.type == litem_type.L_ITEM_TYPE_MECHA_SKIN

    def is_role_skin_item(self):
        return self.type == litem_type.L_ITEM_TYPE_ROLE_SKIN

    def is_emoticon_item(self):
        return self.type == litem_type.L_ITEM_TYPE_EMOTICON

    def is_spray_item(self):
        return self.type == litem_type.L_ITEM_TYPE_SPRAY

    def is_gesture_item(self):
        return self.type == litem_type.L_ITEM_TYPE_GESTURE

    def is_forbid_charm(self):
        return self.forbid_charm

    def set_lock(self, time):
        pass

    def is_lock(self):
        return tutil.time() < self.unlock_time

    def get_unlock_time(self):
        return self.unlock_time

    def is_expire(self):
        if not self.is_timeliness_item():
            return False
        return 0 <= self.expire_time < tutil.time()

    def set_expire_time(self, expire_time):
        if not self.is_timeliness_item():
            return
        self.expire_time = expire_time

    def add_expire_time(self, expire_time):
        if not self.is_timeliness_item():
            return
        else:
            expire_time = expire_time if expire_time is not None else tutil.ONE_WEEK_SECONDS
            if expire_time < 0 or self.expire_time < 0:
                self.set_expire_time(-1)
            else:
                if self.is_expire():
                    self.expire_time = tutil.time()
                self.expire_time = int(self.expire_time + expire_time)
            return

    def get_expire_time(self):
        if not self.is_timeliness_item():
            return -1
        return self.expire_time

    def check_circulation_type(self, circulation_type):
        if circulation_type == iconst.ITEM_CIRCULATION_UNLIMIT:
            return True
        if circulation_type == iconst.ITEM_CIRCULATION_TRADE:
            return self.can_trade() and not self.is_lock()
        if circulation_type == iconst.ITEM_CIRCULATION_LOCK:
            return self.can_trade() and self.is_lock()
        if circulation_type == iconst.ITEM_CIRCULATION_UNTRADE:
            return not self.can_trade()
        return False

    def set_rp_state(self, state):
        self.rp = state

    def get_rp_state(self):
        return self.rp

    def update_degree(self):
        pass