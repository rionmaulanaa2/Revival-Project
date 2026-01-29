# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/nile_sdk.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.framework import Singleton
import time
import version
from logic.gutils import item_utils, mall_utils, nile_utils
import logic.gcommon.const as gconst
from NileSDK.Bedrock.NileService import NileService

class NileSDK(Singleton):
    ALIAS_NAME = 'nile_sdk'

    def init(self):
        self._data = {}
        self._is_inited = False
        self._is_inited_user_data = False
        self._is_started = False
        self._is_paused = False
        self._cur_token = None
        self.init_event()
        self.init_sdk()
        return

    def init_sdk(self):
        import cc
        director = cc.Director.getInstance()
        cc_scene = director.getRunningScene()
        from NileSDK.Bedrock.NileService import NileService
        from NileSDK.Bedrock.NileSettings import NileSettings
        if global_data.is_inner_server == 1:
            env = NileSettings.ENV_OFFICE
        elif global_data.is_inner_server == 2:
            env = NileSettings.ENV_TEST
        else:
            env = NileSettings.ENV_PRODUCT
        NileService.GetInstance().Init(cc_scene, env)
        self._is_inited = True

    def on_finalize(self):
        self.process_event(False)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_lv_update_event': self.on_player_lv_update,
           'player_on_change_name': self.on_player_change_name,
           'player_money_info_update_event': self._on_player_money_info_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def logout(self):
        self._is_inited_user_data = False
        self._is_started = False
        self._is_paused = False
        NileService.GetInstance().Logout()

    def is_started(self):
        return self._is_started

    def is_paused(self):
        return self._is_paused

    def start(self):
        if not self._is_inited:
            self.init_sdk()
        if not self._is_inited_user_data:
            self.setup_nile()
        NileService.GetInstance().Start()
        self._is_started = True

    def pause(self):
        NileService.GetInstance().Pause()
        self._is_paused = True

    def resume(self):
        NileService.GetInstance().Resume()
        self._is_paused = False

    def init_data(self):
        from common.platform.dctool import interface
        userData = self._data
        userData['game'] = interface.get_project_id()
        userData['server'] = str(global_data.channel.get_host_num())
        userData['server_version'] = str(global_data.channel.get_host_tag())
        userData['app_ver'] = version.get_server_version()
        userData['app_channel'] = global_data.channel.get_app_channel()
        userData['account_id'] = global_data.channel.get_login_name()
        userData['aid'] = global_data.channel.get_prop_str('USERINFO_AID')
        userData['login_time'] = int(global_data.player.login_time)
        userData['role_id'] = str(global_data.player.uid)
        userData['role_level'] = str(global_data.player.get_lv())
        userData['role_name'] = global_data.player.char_name
        userData['token'] = global_data.player.get_nile_token()
        NileService.GetInstance().SetUserData(userData)

    def setup_callback(self):
        NileService.GetInstance().SetEventDelegate(self.GameProcessEventCallback)
        NileService.GetInstance().SetPlaySoundDelegate(self.GameSoundCallback)
        NileService.GetInstance().SetGetCurrencyDelegate(self.GameGetCurrencyCallback)
        NileService.GetInstance().SetGetItemConfigDelegate(self.GameGetItemConfigCallback)
        NileService.GetInstance().SetGetItemNameDelegate(self.GameGetItemNameCallback)
        NileService.GetInstance().SetGetItemIconDelegate(self.GameGetItemIconCallback)
        NileService.GetInstance().SetRefreshTokenDelegate(self.GameRefreshTokenCallback)

    def setup_nile(self, *args):
        self.init_data()
        self.setup_callback()
        self._cur_token = global_data.player.get_nile_token()
        self._is_inited_user_data = True

    def GameProcessEventCallback(self, eventName, content, activityId):
        if eventName == 'ready':
            game_act_id = nile_utils.nile_id_to_activity_type(activityId)
            global_data.emgr.nile_activity_ready_event.emit(game_act_id)
        elif eventName == 'redDot':
            game_act_id = nile_utils.nile_id_to_activity_type(activityId)
            global_data.emgr.nile_activity_reddot_event.emit(game_act_id)
        elif eventName == 'payOrder':
            if global_data.player and type(content) is dict:
                market_activityId = activityId
                cls_activityId = content.get('activityId')
                orderId = content.get('orderId')
                costId = content.get('costId')
                goodsId = content.get('goodsId')
                global_data.player.nile_pay_order(orderId, market_activityId, cls_activityId, costId, goodsId)
            else:
                log_error('invalid payOrder event', content)

    def GameSoundCallback(self, value):
        if type(value) in [tuple, list]:
            if len(value) == 3:
                global_data.sound_mgr.play_sound_2d(value[0], (value[1], value[2]))
            else:
                log_error('unsupported sound value: ', value)
        elif type(value) in [str, six.text_type]:
            global_data.sound_mgr.play_sound_2d(value)
        else:
            log_error('unsupported sound value: ', value)

    def GameGetCurrencyCallback(self):
        currents = [
         gconst.SHOP_PAYMENT_YUANBAO,
         gconst.SHOP_PAYMENT_DIAMON,
         gconst.SHOP_PAYMENT_GOLD]
        current_dict = {}
        for c in currents:
            current_dict[mall_utils.get_payment_item_no(c)] = mall_utils.get_my_money(c)

        return current_dict

    def GameGetItemNameCallback(self, itemId):
        return item_utils.get_lobby_item_name(itemId)

    def GameGetItemIconCallback(self, itemId):
        return item_utils.get_item_pic_by_item_no(itemId)

    def GameGetItemConfigCallback(self, itemId):
        return {'name': item_utils.get_lobby_item_name(itemId),
           'icon': item_utils.get_item_pic_by_item_no(itemId)
           }

    def GameRefreshTokenCallback(self):
        global_data.player and global_data.player.nile_request_token()

    def on_player_lv_update(self, *args):
        NileService.GetInstance().ExecuteLevelUpMessage(str(global_data.player.get_lv()))

    def on_player_change_name(self, *args):
        pass

    def _on_player_money_info_update(self, *args):
        NileService.GetInstance().ExecuteCurrencyChangeMessage()

    def ForwardServerCommand(self, command):
        NileService.GetInstance().ExecuteServerCommand(command)

    def on_update_state_with_token(self, token):
        if not global_data.player:
            return
        if self.is_started():
            if token != self._cur_token:
                self.setup_nile()
        else:
            self.start()

    def on_pay_result(self, ret, privateparam):
        if privateparam and privateparam.get('market_id') is not None and privateparam.get('order_id') is not None:
            orderId = privateparam.get('order_id')
            market_activity_id = privateparam.get('market_id')
            NileService().GetInstance().Execute('payResult', {'ret': ret,'orderId': orderId}, activityId=market_activity_id)
        return

    def get_activity_reddot(self, activityId):
        if not self.is_started():
            return False
        nile_id = nile_utils.nile_activity_type_to_nile_id(activityId)
        return NileService.GetInstance().GetActivityRedDot(int(nile_id))

    def get_activity_status(self, activityId):
        if not self.is_started():
            return False
        nile_id = nile_utils.nile_activity_type_to_nile_id(activityId)
        status = NileService.GetInstance().GetActivityStatus(int(nile_id))
        return bool(status)

    def get_activity_panel(self, activityId):
        if not self.is_started():
            return None
        else:
            nile_id = nile_utils.nile_activity_type_to_nile_id(activityId)
            panel = NileService.GetInstance().OpenActivityPanel(int(nile_id))
            return panel

    def on_lang_changed(self):
        from logic.gcommon.common_utils.local_text import get_cur_lang_name
        if not NileService.GetInstance().GetUserData():
            return
        NileService.GetInstance().GetUserData().language = get_cur_lang_name()

    def on_notify_enter_lobby(self):
        if not self.is_started():
            return None
        else:
            NileService.GetInstance().Execute('enterLobby', {}, 0)
            return None