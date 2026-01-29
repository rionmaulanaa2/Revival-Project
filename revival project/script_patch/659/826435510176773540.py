# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/BountySurvivalBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gutils import bounty_mode_utils

class BountySurvivalBattle(SurvivalBattle):

    def __init__(self, entityid):
        super(BountySurvivalBattle, self).__init__(entityid)
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'resolution_changed': self.on_resolution_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def recruit_valid(self):
        return False

    def destroy(self, clear_cache=True):
        super(BountySurvivalBattle, self).destroy(clear_cache=clear_cache)
        self.process_event(False)

    def load_finish(self):
        super(BountySurvivalBattle, self).load_finish()
        self.reconnect_handle_bounty_timestamp()

    def init_from_dict(self, bdict):
        self.reconnect_handle_data(bdict)
        super(BountySurvivalBattle, self).init_from_dict(bdict)
        self._timestamp_cache_bounty = 0
        self._timestamp_cache_prey = 0
        self._cache_valid_bounty = False
        self._cache_valid_prey = False

    def on_resolution_changed(self):
        if self._cache_valid_bounty:
            global_data.emgr.update_bounty_region_timestamp.emit(self._timestamp_cache_bounty, bounty_mode_utils.BOUNTY_TYPE)
        if self._cache_valid_prey:
            global_data.emgr.update_bounty_region_timestamp.emit(self._timestamp_cache_prey, bounty_mode_utils.PREY_TYPE)

    @rpc_method(CLIENT_STUB, (Int('bounty_time'),))
    def be_hunter(self, bounty_time):
        self._cache_valid_bounty = True
        self._timestamp_cache_bounty = bounty_time
        self.update_bounty_region_timestamp(bounty_time, bounty_mode_utils.BOUNTY_TYPE)
        if bounty_time != 0:
            self.notify_bounty_tips(19885)
            global_data.sound_mgr.play_sound_2d('Play_ui_target')

    @rpc_method(CLIENT_STUB, (Int('prey_time'), Int('prey_type')))
    def be_prey(self, prey_time, prey_type):
        self._cache_valid_prey = True
        self._timestamp_cache_prey = prey_time
        self.update_bounty_region_timestamp(prey_time, bounty_mode_utils.PREY_TYPE)
        if prey_time != 0:
            if prey_type == 1:
                self.notify_bounty_tips(19886)
            elif prey_type == 0:
                self.notify_bounty_tips(19960)
            global_data.sound_mgr.play_sound_2d('Play_ui_gain')

    @rpc_method(CLIENT_STUB, (Int('tip_type'),))
    def bounty_tip(self, tip_type):
        tips_dict = bounty_mode_utils.BOUNTY_TIPS_DICT[tip_type]
        if tips_dict:
            self.notify_bounty_tips(tips_dict[0])
            global_data.sound_mgr.play_sound_2d(tips_dict[1])

    def reconnect_handle_data(self, bdict):
        self.reconnect_data = {bounty_mode_utils.PREY_TYPE: bdict.get('be_prey', 0),
           bounty_mode_utils.BOUNTY_TYPE: bdict.get('be_hunter', 0)
           }

    def reconnect_handle_bounty_timestamp(self):
        prey_timestamp = self.reconnect_data[bounty_mode_utils.PREY_TYPE]
        bounty_timestamp = self.reconnect_data[bounty_mode_utils.BOUNTY_TYPE]
        self.update_bounty_region_timestamp(prey_timestamp, bounty_mode_utils.PREY_TYPE)
        self.update_bounty_region_timestamp(bounty_timestamp, bounty_mode_utils.BOUNTY_TYPE)

    def update_bounty_region_timestamp(self, timestamp, show_type):
        global_data.emgr.update_bounty_region_timestamp.emit(timestamp, show_type)

    def notify_bounty_tips(self, text_id):
        from logic.gcommon.common_const.battle_const import BOUNTY_CENTER_TIPS, MAIN_NODE_COMMON_INFO
        message = {'i_type': BOUNTY_CENTER_TIPS,'content_txt': text_id,'extra_disappear_time': 3}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)