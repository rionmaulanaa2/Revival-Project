# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_granbelm/ComGranbelmRuneClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.client.const import game_mode_const

class ComGranbelmRuneClient(UnitCom):
    BIND_EVENT = {'E_UPDATE_RUNE_COUNT': '_on_update_rune_count',
       'E_UPDATE_RUNE_ID': '_on_update_rune_id',
       'E_UPDATE_REGION_TAG': '_on_update_region_tag',
       'G_GRANBELM_RUNE_COUNT': '_get_rune_count',
       'G_GRANBELM_RUNE_ID': '_get_rune_id',
       'G_GRANBELM_REGION_TAG': '_get_region_tag',
       'G_GRANBELM_RUNE_DATA': '_get_data'
       }

    def __init__(self):
        super(ComGranbelmRuneClient, self).__init__()
        self.rune_count = 0
        self.rune_id = None
        self.region_tag = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComGranbelmRuneClient, self).init_from_dict(unit_obj, bdict)
        if not global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GRANBELM_SURVIVAL, game_mode_const.GAME_MODE_GRANHACK_SURVIVAL)):
            return
        else:
            rune_count = bdict.get('rune_count', 0)
            rune_id = bdict.get('rune_id', None)
            region_tag = bdict.get('rune_region_tag', False)
            self.rune_count = rune_count
            self.rune_id = rune_id
            self.region_tag = region_tag
            self._on_update_rune_count(rune_count, True)
            self._on_update_rune_id(rune_id)
            self._on_update_region_tag(region_tag)
            return

    def _on_update_rune_count(self, rune_count, is_self_inc):
        self.rune_count = rune_count
        self.send_event('E_NOTIFY_UPDATE_RUNE_COUNT', rune_count, is_self_inc)

    def _on_update_rune_id(self, rune_id):
        self.rune_id = rune_id
        self.send_event('E_NOTIFY_UPDATE_RUNE_ID', rune_id)

    def _on_update_region_tag(self, tag):
        self.region_tag = tag
        self.send_event('E_NOTIFY_UPDATE_REGION_TAG', tag)

    def _get_rune_count(self):
        return self.rune_count

    def _get_rune_id(self):
        return self.rune_id

    def _get_region_tag(self):
        return self.region_tag

    def _get_data(self):
        return (
         self.rune_count, self.rune_id, self.region_tag)

    def destroy(self):
        super(ComGranbelmRuneClient, self).destroy()