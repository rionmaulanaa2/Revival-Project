# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/Product.py
from __future__ import absolute_import
from .Item import Item

class Product(Item):
    __slots__ = ('contact', )

    def __init__(self, item_id=None, create_time=None):
        super(Product, self).__init__(item_id, create_time)
        self.contact = None
        return

    def get_persistent_dict(self):
        d = super(Product, self).get_persistent_dict()
        d['contact'] = self.contact
        return d

    def get_client_dict(self):
        d = super(Product, self).get_client_dict()
        d['contact'] = self.contact
        return d

    def set_contact(self, contact):
        self.contact = contact

    def can_use(self, sex, lv):
        if not super(Product, self).can_use(sex, lv):
            return False
        else:
            return self.contact is None