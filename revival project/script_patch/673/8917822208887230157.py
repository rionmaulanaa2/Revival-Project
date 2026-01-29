# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLocalBattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_const.battle_const import COMBAT_STATE_NONE, FIGHT_EVENT_DEATH
from logic.client.const import game_mode_const
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from data.c_guide_data import get_init_guide_pos
from logic.gutils import newbie_stage_utils
from logic.client.const.game_mode_const import NEWBIE_STAGE_THIRD_BATTLE_TYPE, NEWBIE_STAGE_FOURTH_BATTLE_TYPE, QTE_LOCAL_BATTLE_TYPE
from mobile.common.RpcMethodArgs import Int

class impLocalBattle(object):

    def _init_localbattle_from_dict(self, bdict):
        self.local_battle_server = None
        self.new_local_battle = None
        self.local_battle_data = None
        return

    def _destroy_localbattle(self):
        self.local_battle_server = None
        self.new_local_battle = None
        self.local_battle_data = None
        return

    def try_start_new_local_battle(self, battle_type):
        if battle_type == game_mode_const.QTE_LOCAL_BATTLE_TYPE:
            self._start_new_local_battle(battle_type)
        else:
            self.call_server_method('try_start_local_battle', (battle_type,))

    @rpc_method(CLIENT_STUB, (Int('battle_type'),))
    def do_start_new_local_battle(self, battle_type):
        self._start_new_local_battle(battle_type)

    def _start_new_local_battle(self, battle_type):
        SvrType, CliType = game_mode_const.get_local_battle_svr_cli_by_type(battle_type)
        if not (SvrType and CliType):
            return False
        else:
            if self.local_battle_server:
                self.local_battle_server.destroy()
                self.local_battle_server = None
            self.local_battle_server = EntityFactory.instance().create_entity(SvrType, IdManager.genid())
            server_init_dict = self._get_local_battle_server_init_dict(battle_type)
            self.local_battle_server.init_from_dict(server_init_dict)
            if self.new_local_battle:
                self.new_local_battle.destroy()
                self.new_local_battle = None
            client_init_dict = self.local_battle_server.get_client_dict()
            self.new_local_battle = EntityFactory.instance().create_entity(CliType, IdManager.genid())
            self.new_local_battle.init_from_dict(client_init_dict)
            self.local_battle_server.set_local_battle(self.new_local_battle)
            return True

    def quit_new_local_battle(self):
        cur_battle_type = None
        if self.local_battle_server:
            self.local_battle_server.destroy()
            self.local_battle_server = None
        if self.new_local_battle:
            cur_battle_type = self.new_local_battle.get_battle_tid()
            self.new_local_battle.destroy()
            self.new_local_battle = None
        self.notify_server_local_battle_finish(cur_battle_type)
        is_from_newbie_stage = self.get_is_from_newbie_stage(cur_battle_type)
        if self.lobby:
            self.lobby.init_from_dict({'is_login': False,'combat_state': COMBAT_STATE_NONE,'from_newbie_stage': is_from_newbie_stage})
        return

    def notify_server_local_battle_finish(self, battle_type):
        if battle_type is None:
            self.call_server_method('finish_local_battle', (battle_type, True))
        else:
            if battle_type == QTE_LOCAL_BATTLE_TYPE:
                return
            if battle_type in (NEWBIE_STAGE_THIRD_BATTLE_TYPE, NEWBIE_STAGE_FOURTH_BATTLE_TYPE):
                self.call_server_method('finish_local_battle', (battle_type, True))
            else:
                log_error('impLocalBattle - notify_server_local_battle_finish: unexpected battle_type ', battle_type)
        return

    def get_is_from_newbie_stage(self, battle_type):
        return battle_type in (NEWBIE_STAGE_THIRD_BATTLE_TYPE, NEWBIE_STAGE_FOURTH_BATTLE_TYPE)

    def _get_local_battle_server_init_dict(self, battle_type):
        if battle_type == game_mode_const.QTE_LOCAL_BATTLE_TYPE:
            return {}
        return {'battle_type': battle_type}

    def handle_new_local_battle_rpc(self, method_name, params):
        if not self.local_battle_server:
            log_error('handle_local_battle_rpc error!!! There is not local battle')
            return
        else:
            handler_name = self.local_battle_server.RPC_HANDLER.get(method_name)
            if handler_name is None:
                return
            handler_func = getattr(self.local_battle_server, handler_name, None)
            if handler_func is None:
                return
            handler_func(*params)
            return

    def call_new_local_battle_rpc_method(self, method_name, params):
        if self.new_local_battle is None:
            return
        else:
            method = getattr(self.new_local_battle, method_name, None)
            if method is None:
                return
            method(params)
            return

    def call_new_local_battle_method_direct(self, method_name, params):
        if self.new_local_battle is None:
            return
        else:
            method = getattr(self.new_local_battle, method_name, None)
            if method is None:
                return
            method(*params)
            return

    def call_local_avatar_rpc_method(self, method_name, params):
        method = getattr(self, method_name, None)
        if method is None:
            return
        else:
            method(params)
            return

    def get_local_battle_server(self):
        return self.local_battle_server

    def get_new_local_battle(self):
        return self.new_local_battle

    def in_local_battle(self):
        if self.in_new_local_battle():
            return True
        info = self._get_local_battle_data()
        return info.get('_lbs_in_battle', 0)

    def in_new_local_battle(self):
        return self.new_local_battle is not None

    def get_new_local_battle_mecha_ids(self):
        if self.local_battle_server is None:
            return [8001]
        else:
            return self.local_battle_server.get_usual_mecha_ids()