# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/BattleConsume.py
from __future__ import absolute_import
import six

class Consume(object):

    def __init__(self):
        self.gold = 0
        self.diamond = 0
        self.yuanbao = 0
        self.items = {}

    def init_from_dict(self, consume_dict):
        self.gold = consume_dict.get('gold', 0)
        self.diamond = consume_dict.get('diamond', 0)
        self.yuanbao = consume_dict.get('yuanbao', 0)
        self.items = consume_dict.get('items', [])

    def settle(self, battle, soul_dict):
        pass

    def do_consume(self, avatar, reason, ext_data=None):
        pass

    def get_persistent_dict(self):
        persistent_dict = {}
        if self.gold != 0:
            persistent_dict['gold'] = self.gold
        if self.diamond != 0:
            persistent_dict['diamond'] = self.diamond
        if self.yuanbao != 0:
            persistent_dict['yuanbao'] = self.yuanbao
        if self.items:
            persistent_dict['items'] = self.items
        return persistent_dict

    def consume_gold(self, gold):
        if gold <= 0:
            return
        self.gold += int(gold)

    def consume_diamond(self, diamond):
        if diamond <= 0:
            return
        self.diamond += int(diamond)

    def consume_yuanbao(self, yuanbao):
        if yuanbao <= 0:
            return
        self.yuanbao += int(yuanbao)

    def consume_item(self, item_no, count):
        if count <= 0:
            return
        self.items[item_no] = self.items.get(item_no, 0) + int(count)


class GoldConsume(Consume):

    def settle(self, battle, soul_dict):
        if battle is None:
            return
        else:
            gold = soul_dict.get('gold_consume', 0)
            self.consume_gold(gold)
            return

    def do_consume(self, avatar, reason, ext_data=None):
        if not self.gold:
            return
        own_gold = avatar.get_gold()
        if own_gold < self.gold:
            log_error('[BattleConsume-do_gold_consume] consume greater than own: consume(%s), own(%s)', self.gold, own_gold)
            self.gold = max(0, own_gold)
        avatar.cost_gold(self.gold, reason)


class DiamondConsume(Consume):

    def settle(self, battle, soul_dict):
        if battle is None:
            return
        else:
            diamond = soul_dict.get('diamond_consume', 0)
            self.consume_diamond(diamond)
            return

    def do_consume(self, avatar, reason, ext_data=None):
        if not self.diamond:
            return
        own_diamond = avatar.get_diamond()
        if own_diamond < self.diamond:
            log_error('[BattleConsume-do_diamond_consume] consume greater than own: consume(%s), own(%s)', self.diamond, own_diamond)
            self.diamond = max(0, own_diamond)
        avatar.cost_diamond(self.diamond, reason)


class YuanbaoConsume(Consume):

    def settle(self, battle, soul_dict):
        if battle is None:
            return
        else:
            yuanbao = soul_dict.get('yuanbao_consume', 0)
            self.consume_yuanbao(yuanbao)
            return

    def do_consume(self, avatar, reason, ext_data=None):
        from logic.appplatform.PlatformUtils import UseType
        if not self.yuanbao:
            return
        own_yuanbao = avatar.get_yuanbao()
        if own_yuanbao < self.yuanbao:
            log_error('[BattleConsume-do_yuanbao_consume] consume greater than own: consume(%s), own(%s)', self.yuanbao, own_yuanbao)
            self.yuanbao = max(0, own_yuanbao)
        avatar.cost_yuanbao(self.yuanbao, UseType.UT_OTHER, reason)


class BattleConsume(Consume):
    GOLD_CONSUME = '1'
    DIAMOND_CONSUME = '2'
    YUANBAO_CONSUME = '3'

    def __init__(self):
        super(BattleConsume, self).__init__()
        self._consumes = {BattleConsume.GOLD_CONSUME: GoldConsume(),
           BattleConsume.DIAMOND_CONSUME: DiamondConsume(),
           BattleConsume.YUANBAO_CONSUME: YuanbaoConsume()
           }

    def init_from_dict(self, bdict):
        for consume_type, consume_dict in six.iteritems(bdict):
            consume_obj = self._consumes.get(consume_type, None)
            if not consume_obj:
                continue
            consume_obj.init_from_dict(consume_dict)

        return

    def settle(self, battle, soul_dict):
        for consume in six.itervalues(self._consumes):
            consume.settle(battle, soul_dict)

    def get_persistent_dict(self):
        persistent_dict = {}
        for consume_type, consume in six.iteritems(self._consumes):
            consume_dict = consume.get_persistent_dict()
            if consume_dict:
                persistent_dict[consume_type] = consume_dict

        return persistent_dict

    def do_consume(self, avatar, reason, ext_data=None):
        for consume_obj in six.itervalues(self._consumes):
            consume_obj.do_consume(avatar, reason, ext_data)