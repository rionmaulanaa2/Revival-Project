# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/MechaCardHandler.py
from __future__ import absolute_import
from collections import defaultdict

class MechaCardHandler(object):

    def __init__(self):
        super(MechaCardHandler, self).__init__()
        self._handler_data_cache = defaultdict(dict)
        self.mecha = None
        return

    def set_mecha_obj(self, mecha_obj):
        self.mecha = mecha_obj

    def can_handle_card(self):
        return self.mecha and self.mecha.logic

    def _get_effect_cached_data(self, card_id, effect_info):
        if not card_id or not effect_info:
            return
        else:
            effect_id = effect_info.get('effect_id', None)
            if card_id in self._handler_data_cache and effect_id in self._handler_data_cache[card_id]:
                return self._handler_data_cache[card_id][effect_id]
            return

    def _remove_effect_cached_data(self, card_id, effect_info):
        if not card_id or not effect_info:
            return
        else:
            effect_id = effect_info.get('effect_id', None)
            if card_id in self._handler_data_cache and effect_id in self._handler_data_cache[card_id]:
                del self._handler_data_cache[card_id][effect_id]
            else:
                log_error('MechaCardHanlder _remove_effect_cached_data failed to remove cached data with card_id=%s', card_id)
            return

    def handler_add_weapon_custom_param(self, card_id, item_id, config_param):
        self.mecha.logic.send_event('E_ADD_WP_CUSTOM_PARAM', card_id, item_id, config_param)

    def undo_handler_add_weapon_custom_param(self, card_id, item_id, config_param):
        self.mecha.logic.send_event('E_DEL_WP_CUSTOM_PARAM', card_id, item_id, config_param)

    def handler_enable_aim_help(self, card_id, item_id, config_param):
        self.mecha.logic.send_event('E_ACTIVATE_FLIGHT_AIM_HELPER', True)

    def undo_handler_enable_aim_help(self, card_id, item_id, config_param):
        self.mecha.logic.send_event('E_ACTIVATE_FLIGHT_AIM_HELPER', False)