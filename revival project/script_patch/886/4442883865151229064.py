# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/BaseClientAvatar.py
from __future__ import absolute_import
import time
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Bool, Int, Dict
from mobile.client.ClientEntity import AvatarEntity
from mobile.common.CustomMessageBroker import CustomMessageBroker, CMSG_TYPE_GAME_CRASH
from logic.gcommon.time_utility import get_readable_time

class BaseClientAvatar(AvatarEntity):

    def __init__(self, entityid=None):
        super(BaseClientAvatar, self).__init__(entityid)
        self.logic = None
        self.local_battle = None
        self.new_local_battle = None
        self.lose_conn = False
        self._switch_func = {}
        self._change_to_login_and_restart = True
        self.reset_net_user_callback()
        CustomMessageBroker.register(CMSG_TYPE_GAME_CRASH, self.on_game_crash)
        self.register_switch_func('LagProfile', self._switch_profile_on)
        return

    def set_change_to_login_and_restart(self, flag):
        self._change_to_login_and_restart = flag

    def update_from_dict(self, bdict):
        pass

    def destroy(self):
        CustomMessageBroker.unregister(CMSG_TYPE_GAME_CRASH, self.on_game_crash)
        super(BaseClientAvatar, self).destroy()

    def reset_net_user_callback(self):
        from mobile.client.GateClient import GateClient
        from logic.gutils.ConnectHelper import ConnectHelper
        connect_helper = ConnectHelper()
        connect_helper.clean_service_callback()
        connect_helper.set_service_callback(GateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT, self.reliable_message_cannot_sent_cb)

    def reliable_message_cannot_sent_cb(self, op_code):
        pass

    def on_become_player(self):
        pass

    def tick(self, delta):
        pass

    @rpc_method(CLIENT_STUB, (Str('switch_key'), Str('switch_value'), Bool('show_tip')))
    def client_switch(self, switch_key, switch_value, show_tip):
        if show_tip and global_data.message_data:
            from logic.gcommon.common_const.chat_const import CHAT_SYS
            tip = 'switch: %s, value: %s' % (switch_key, switch_value)
            global_data.game_mgr.show_tip(tip)
            global_data.message_data.add_msg({'chnl': CHAT_SYS,'msg': tip})
        func = self._switch_func.get(switch_key)
        if func:
            try:
                func(switch_key, switch_value)
            except:
                import exception_hook
                exception_hook.traceback_uploader()

    @rpc_method(CLIENT_STUB, (Str('file_name'), Str('hotfix_content'), Str('tip_type')))
    def hotfix(self, file_name, hotfix_content, tip_type):
        compiled_code = compile(hotfix_content, '%s_hotfix' % file_name, 'exec')
        import __main__
        exec (
         compiled_code, __main__.__dict__)
        if tip_type and global_data.message_data:
            from logic.gcommon.common_const.chat_const import CHAT_SYS
            tip = '%s %s_hotfix' % (file_name, tip_type)
            global_data.game_mgr.show_tip(tip)
            global_data.message_data.add_msg({'chnl': CHAT_SYS,'msg': tip})

    def call_server_method(self, methodname, parameters=(), reliable=True):
        if self.local_battle:
            self.handle_local_battle_rpc(methodname, parameters)
            return
        else:
            if self.new_local_battle:
                self.handle_new_local_battle_rpc(methodname, parameters)
                return
            if self.server is None:
                return
            self.server.call_server_method(methodname, parameters, None, reliable)
            return

    def call_soul_method(self, methodname, parameters=(), entityid=None):
        if global_data.player and (global_data.player.is_battle_replaying() or global_data.player.is_in_global_spectate()):
            return
        else:
            if self.local_battle:
                self.handle_local_battle_rpc(methodname, parameters)
                return
            if self.new_local_battle:
                self.handle_new_local_battle_rpc(methodname, parameters)
                return
            if self.battle_server:
                self.battle_server.call_server_method_direct(methodname, parameters, entityid)
                return
            if self.server is not None:
                self.server.call_soul_method(methodname, parameters, entityid)
                return
            return

    def call_misty_soul_method(self, methodname, parameters=(), entityid=None):
        if self.battle_server:
            self.battle_server.call_server_method_direct_misty(methodname, parameters, entityid)
            return
        else:
            if self.server is not None:
                self.server.call_misty_soul_method(methodname, parameters, entityid)
                return
            return

    @rpc_method(CLIENT_STUB, (Str('err_text'),))
    def set_disconnect_error_msg(self, err_text):
        from logic.gutils.ConnectHelper import ConnectHelper
        ConnectHelper().set_service_disconnect_msg(unpack_text(err_text))

    def on_lose_server(self):
        self.lose_conn = True

    @rpc_method(CLIENT_STUB, (Int('reason'), Dict('args')))
    def kicked_off(self, reason, args):
        from mobile.client.GateClient import GateClient
        from logic.gutils.ConnectHelper import ConnectHelper
        from logic.gcommon.time_utility import get_date_str
        if 'id_reason' in args:
            args['id_reason'] = get_text_by_id(args['id_reason'])
        if 'timelen' in args:
            if args['timelen'] < 0:
                args['timelen'] = get_text_by_id(80953)
            else:
                args['timelen'] = get_date_str('%Y.%m.%d', args['timelen'])
        content = get_text_by_id(reason, args)
        connect_helper = ConnectHelper()
        connect_helper.set_service_disconnect_msg(content)
        connect_helper.reset_reconnect_info()
        connect_helper.clean_service_callback()
        connect_helper.set_service_callback(GateClient.CB_ON_DISCONNECTED, lambda : ConnectHelper().pop_failed_confirm_fall_back_server_select())
        connect_helper.disconnect()
        self._change_to_login_and_restart = True

    @rpc_method(CLIENT_STUB, (Bool('service_ceased'),))
    def on_server_maintenance(self, service_ceased):
        import game3d
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2, NormalConfirmUI2
        if service_ceased:
            NormalConfirmUI2(content=get_text_by_id(127))
        else:
            SecondConfirmDlg2().confirm(content=get_text_by_id(166), confirm_callback=lambda : game3d.restart())

    def change_to_login(self):
        if self.server:
            self.server.call_server_method('change_to_login', {}, reliable=False)
        import game3d
        game3d.delay_exec(10, lambda : self._change_to_login_destroy())

    def _change_to_login_destroy(self, disconnect_msg=''):
        from mobile.client.GateClient import GateClient
        from logic.gutils.ConnectHelper import ConnectHelper
        connect_helper = ConnectHelper()
        connect_helper.set_service_disconnect_msg(disconnect_msg)
        connect_helper.reset_reconnect_info()
        connect_helper.clean_service_callback()
        if disconnect_msg:
            disconnect_handle = lambda : connect_helper.pop_failed_confirm_fall_back_server_select()
        else:
            disconnect_handle = lambda : connect_helper.fall_back_to_server_select()
        if connect_helper.is_disconnected():
            disconnect_handle()
        elif connect_helper.is_connected():
            if self._change_to_login_and_restart:
                connect_helper.set_service_callback(GateClient.CB_ON_DISCONNECTED, disconnect_handle)
            else:
                connect_helper.set_service_callback(GateClient.CB_ON_DISCONNECTED, lambda : None)
            connect_helper.disconnect()
        else:
            connect_helper.set_service_callback(GateClient.CB_ON_CONNECT_FAILED, disconnect_handle)
            connect_helper.set_service_callback(GateClient.CB_ON_CONNECT_SUCCESSED, disconnect_handle)
            connect_helper.set_service_callback(GateClient.CB_ON_DISCONNECTED, disconnect_handle)
            connect_helper.disconnect()
        self._change_to_login_and_restart = True

    def on_reconnected(self, extra_msg):
        srv_received_seq = extra_msg['srv_received_seq']
        next_seq = srv_received_seq + 1
        self.server.flush_from_seq(next_seq)
        self.lose_conn = False

    def on_game_crash(self):
        self._change_to_login_destroy(get_text_by_id(195))

    def register_switch_func(self, key, func):
        self._switch_func[key] = func

    def _switch_profile_on(self, key, value):
        import json
        args = json.loads(value)
        perf_sys = global_data.perf_sys
        perf_sys.lag_threadhold = args['lag_threadhold']
        perf_sys.profile_duration = args['profile_duration']
        perf_sys.profile_start_time = args['profile_start_time']
        perf_sys.lag_only = True