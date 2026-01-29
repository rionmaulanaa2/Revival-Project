# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/MagicSurvivalBattle.py
from __future__ import absolute_import
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.common_const.battle_const import MAGIC_MONSTER_TIP, MAGIC_ACHIEVE, MAIN_NODE_COMMON_INFO

class MagicSurvivalBattle(SurvivalBattle):

    def init_from_dict(self, bdict):
        super(MagicSurvivalBattle, self).init_from_dict(bdict)
        self.magic_region_refresh_timestamp = bdict.get('magic_region_refresh_timestamp', None)
        self.start_region_refresh_countdown()
        return

    @rpc_method(CLIENT_STUB, (Dict('region_dict'),))
    def init_magic_region(self, region_dict):
        self.on_init_magic_region({'magic_region': region_dict})

    def on_init_magic_region(self, region_dict):
        global_data.magic_sur_battle_mgr.update_magic_regions(region_dict)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        super(MagicSurvivalBattle, self).fight_stage((stage_dict,))
        magic_region_dict = stage_dict.get('magic_region_dict')
        self.on_init_magic_region(magic_region_dict)

    @rpc_method(CLIENT_STUB, (Int('level'),))
    def create_magic_region_tip(self, level):
        if level == 1:
            global_data.emgr.show_human_tips.emit(get_text_by_id(17870), 5)
        else:
            global_data.emgr.show_battle_main_message.emit({'i_type': MAGIC_MONSTER_TIP,
               'content_txt': get_text_by_id(17871),
               'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_monster_1.png'
               }, MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, ())
    def remove_magic_region_tip(self):
        pass

    @rpc_method(CLIENT_STUB, ())
    def on_show_magic_achievement(self):
        global_data.emgr.show_battle_main_message.emit({'i_type': MAGIC_ACHIEVE}, MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Float('init_timestamp'),))
    def first_magic_region_refresh_tip(self, init_timestamp):
        self.magic_region_refresh_timestamp = init_timestamp
        self.start_region_refresh_countdown()

    def start_region_refresh_countdown(self):
        from logic.gcommon.time_utility import get_server_time
        cur_time = get_server_time()
        if cur_time >= self.magic_region_refresh_timestamp:
            return
        global_data.emgr.update_magic_region_timestamp.emit(self.magic_region_refresh_timestamp)