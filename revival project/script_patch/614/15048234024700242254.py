# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRogueGift.py
from __future__ import absolute_import
from six.moves import range
from ..UnitCom import UnitCom
from logic.gutils import rogue_utils as r_u
from logic.gcommon.cdata import rogue_gift_config

class ComRogueGift(UnitCom):
    BIND_EVENT = {'E_OPEN_ROGUE_BOX_SUCCESS': '_on_open_box_success',
       'E_CHOOSE_ROGUE_GIFT': '_choose_gift',
       'E_CHOOSE_ROGUE_GIFT_RESULT': '_choose_gift_result',
       'E_CANCEL_CHOOSE_ROGUE_GIFT': '_cancel_choose_gift',
       'G_CUR_ROGUE_GIFTS': '_get_cur_gifts',
       'E_CANCEL_HOLDING_ROGUE_BOX': '_cancel_holding_rogue_box',
       'G_CAN_ADD_MORE_GIFT': '_can_add_more_gift',
       'G_HAS_ROGUE_GIFT': 'has_gift',
       'G_LST_EXCLUSIVE_GIFT': 'get_one_last_exclusive_gift',
       'G_ALL_EXCLUSIVE_MECHA_ID': 'get_all_exclusive_mecha_id',
       'E_CLEAR_ROGUE_GIFTS': 'clear_gifts'
       }

    def __init__(self):
        super(ComRogueGift, self).__init__()
        self._cur_gifts = []

    def init_from_dict(self, unit_obj, bdict):
        super(ComRogueGift, self).init_from_dict(unit_obj, bdict)
        self._cur_gifts = bdict.get('rogue_gifts', [])

    def destroy(self):
        super(ComRogueGift, self).destroy()

    def clear_gifts(self):
        self._cur_gifts = []
        global_data.emgr.global_rogue_gifts_clear.emit()

    def on_post_init_complete(self, bdict):
        super(ComRogueGift, self).on_post_init_complete(bdict)
        is_ava = self.ev_g_is_avatar()
        is_obed = r_u.is_observed_unit_id(self.unit_obj.id)
        if is_ava or is_obed:
            global_data.emgr.global_rogue_gifts_updated.emit(self.unit_obj.id, self._cur_gifts)

    def has_gift(self, gift_id):
        return gift_id in self._cur_gifts

    def _choose_gift(self, box_id, gift_id):
        if self.has_gift(gift_id):
            global_data.game_mgr.show_tip(17055)
            return
        self.send_event('E_CALL_SYNC_METHOD', 'choose_rogue_gift', (box_id, gift_id), True, True)

    def _cancel_choose_gift(self, box_id):
        self.send_event('E_CALL_SYNC_METHOD', 'cancel_choose_rogue_gift', (box_id,), True, True)

    def _choose_gift_result(self, result, gift_id):
        if not result:
            return
        self._cur_gifts.append(gift_id)
        is_ava = self.ev_g_is_avatar()
        is_obed = r_u.is_observed_unit_id(self.unit_obj.id)
        if is_ava or is_obed:
            global_data.emgr.global_rogue_gifts_updated.emit(self.unit_obj.id, self._cur_gifts)
        if is_ava:
            global_data.emgr.global_pick_rogue_gifts_success.emit()
        if global_data.is_inner_server and self.ev_g_is_avatar():
            global_data.game_mgr.show_tip('\xe5\xb7\xb2\xe6\x88\x90\xe5\x8a\x9f\xe6\xbf\x80\xe6\xb4\xbb\xe5\xa4\xa9\xe8\xb5\x8b: ' + str(gift_id) + '-' + r_u.get_gift_name_text(gift_id))

    def _on_open_box_success(self, box_id, gift_list):
        if self.ev_g_is_avatar():
            r_u.show_gift_pick_ui(box_id, gift_list)

    def _get_cur_gifts(self):
        return self._cur_gifts

    def get_all_exclusive_mecha_id(self):
        ids = []
        for gift_id in self._cur_gifts:
            mecha_id = rogue_gift_config.get_gift_exclusive_mecha_id(gift_id)
            mecha_id and ids.append(mecha_id)

        return ids

    def get_one_last_exclusive_gift(self):
        for i in range(len(self._cur_gifts)):
            gift_id = self._cur_gifts[-i - 1]
            gift_data = rogue_gift_config.get_exclusive_gift_data().get(gift_id)
            if gift_data:
                return gift_data

        return None

    def _cancel_holding_rogue_box(self, box_id):
        r_u.close_gift_pick_ui(box_id)

    def _can_add_more_gift(self):
        return len(self._cur_gifts) < rogue_gift_config.ROGUE_PLAYER_CAN_HOLD_MAX_GIFT_NUM