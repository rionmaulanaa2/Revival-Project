# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/client/ClientEntity.py
from __future__ import absolute_import
import six
from ..common.IdManager import IdManager
from ..mobilelog.LogManager import LogManager
from ..common.EntityManager import Dynamic, EntityManager
from ..common.RpcIndex import RpcIndexer
from ..common.rpcdecorator import rpc_method, CLIENT_STUB
from ..common.RpcMethodArgs import Str, Dict

class ClientEntity(object):

    def __init__(self, entityid=None):
        super(ClientEntity, self).__init__()
        self.id = entityid == None and IdManager.genid() or entityid
        self.logger = LogManager.get_logger('ClientEntity.' + self.__class__.__name__)
        EntityManager.addentity(self.id, self, False)
        self.server = None
        self.data = None
        self.skip_dt = 0
        self.pingpong_update = -1
        self.is_entity_mark = False
        self.is_valid = True
        return

    def _set_id(self, entityid):
        if self.id is not None:
            EntityManager.delentity(self.id)
        self.id = entityid
        if self.id is not None:
            EntityManager.addentity(self.id, self, False)
        return

    def is_cacheable(self):
        return False

    def reuse(self, entityid):
        self._set_id(entityid)
        self.is_valid = True

    def cache(self):
        self._set_id(None)
        self.skip_dt = 0
        self.is_valid = False
        return

    def is_dynamic(self):
        return False

    def set_dynamic(self, flag):
        EntityManager.setdynamic(self.id, flag)

    def set_server(self, server):
        self.server = server

    def on_entity_creation(self):
        pass

    def on_lose_server(self):
        pass

    def on_destroy(self):
        pass

    def init_from_dict(self, bdict):
        pass

    def update_data_from_dict(self, bdict):
        self.data = bdict

    @rpc_method(CLIENT_STUB, (Str('s'),))
    def set_send_rpc_salt(self, salt):
        self._send_rpc_salt = salt
        RpcIndexer.set_send_rpc_salt(salt)

    @rpc_method(CLIENT_STUB, (Str('content'),))
    def show_client_notice(self, content):
        content = unpack_text(content)
        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        NormalConfirmUI2().init_widget(content=content)

    def destroy(self):
        self.is_valid = False
        self.on_destroy()
        self.logger = None
        if self.server:
            self.server.destroy()
            self.server = None
        if self.id:
            EntityManager.delentity(self.id)
        return

    def on_reconnected(self, extramsg):
        pass


class AvatarEntity(ClientEntity):

    def __init__(self, entityid=None):
        super(AvatarEntity, self).__init__(entityid)
        self.battle_server = None
        return

    @rpc_method(CLIENT_STUB, ())
    def become_player(self):
        self.on_become_player()

    def on_become_player(self):
        pass

    def set_battle_server(self, server):
        self.battle_server = server

    def destroy(self):
        super(AvatarEntity, self).destroy()
        if self.battle_server:
            self.battle_server.close()
            self.battle_server = None
        return


from logic.gcommon.common_const.ui_operation_const import SETTING_CONF

@Dynamic
class ArtTestAvatar(ClientEntity):

    def __init__(self, entityid=None):
        super(ArtTestAvatar, self).__init__(entityid)
        self.logic = None
        self._user_default_setting_dict = {}
        self.init_camera_sst_from_conf(True)
        return

    def tick(self, delta):
        if self.logic:
            self.logic.tick(delta)

    def get_setting(self, key, default=None, from_local=False, from_custom_setting_no=None):
        if key in self._user_default_setting_dict:
            return self._user_default_setting_dict[key]
        return SETTING_CONF.get(key, default)

    def get_setting_2(self, key):
        return SETTING_CONF.get(key, None)

    def is_share(self):
        return False

    def is_in_battle(self):
        return False

    def in_local_battle(self):
        return True

    def is_in_judge_ob(self):
        return False

    def get_all_puppet_info(self, state):
        pass

    def init_camera_sst_from_conf(self, is_pc=False):
        from common.cfg import confmgr
        from logic.gcommon.common_const.ui_operation_const import SST_TYPE_CENTER_TYPE, SST_TYPE_SCREEN_TYPE
        def_settings = {}
        if not is_pc:
            sst_conf = confmgr.get('sst_config')
        else:
            sst_conf = confmgr.get('pc_sst_config')
        for sst_model, sst_content in six.iteritems(sst_conf):
            if isinstance(sst_content, str):
                continue
            sst_model_type = sst_content.get('iSSTType')
            if sst_model_type == SST_TYPE_CENTER_TYPE:
                sst_def_setting = [sst_content['fBaseMultiple'],
                 sst_content['fUpMultiple'],
                 sst_content['fDownMultiple'],
                 sst_content['fLeftMultiple'],
                 sst_content['fRightMultiple']]
            elif sst_model_type == SST_TYPE_SCREEN_TYPE:
                sst_def_setting = [sst_content['fBaseMultiple'],
                 sst_content['fUpMultiple'],
                 sst_content['fDownMultiple'],
                 sst_content['fLeftScreenHorMultiple'],
                 sst_content['fRightScreenHorMultiple']]
            else:
                sst_def_setting = []
            def_settings[sst_model] = sst_def_setting

        self._user_default_setting_dict.update(def_settings)