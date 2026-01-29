# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAttachClient.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
import math3d
import time
import logic.gcommon.cdata.status_config as status_config

class ComAttachClient(UnitCom):
    BIND_EVENT = {'E_TRY_ATTACH': '_try_attach',
       'E_ON_ATTACHED': '_on_attached',
       'E_ON_ATTACHED_FAIL': '_on_attached_fail',
       'E_TRY_DETACH': '_try_detach',
       'E_ON_DETACHED': '_on_detached',
       'E_ATTACHABLE_ON_DAMAGE': '_on_damage',
       'E_ATTACHABLE_INIT': '_on_init',
       'G_ATTACHABLE_HP': 'get_hp',
       'G_ATTACHABLE_MAX_HP': 'get_max_hp',
       'G_IS_ATTACH': 'is_wait_attach'
       }

    def __init__(self):
        super(ComAttachClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        self._max_hp = -1
        self._cur_hp = 0
        self._wait_attach = False
        self._wait_attach_start_time = 0
        super(ComAttachClient, self).init_from_dict(unit_obj, bdict)

    def get_client_dict(self):
        cdict = {}
        return cdict

    def get_hp(self):
        return self._cur_hp

    def get_max_hp(self):
        return self._max_hp

    def _on_init(self):
        mp_attach = self.ev_g_all_attachable()
        for entity_id, data in six.iteritems(mp_attach):
            self._on_attached(data)

    def is_wait_attach(self):
        if self._wait_attach:
            cur_time = time.time()
            pass_time = cur_time - self._wait_attach_start_time
            if pass_time >= 2:
                self._wait_attach = False
        return self._wait_attach

    def _try_attach(self, entity_id):
        self._wait_attach_start_time = time.time()
        self._wait_attach = True
        self.send_event('E_CALL_SYNC_METHOD', 'try_attach', (entity_id,), True)

    def _try_detach(self, entity_id, lst_pos, lst_rotation=(0, 0, 0, 1)):
        if type(lst_rotation) not in (tuple, list) or len(lst_rotation) != 4:
            log_error('lst_rotation must be 4 elmt list.')
            return
        self.send_event('E_ACTION_CHECK_POS', stop=True)
        if self.ev_g_get_state(status_config.ST_HELP):
            self.send_event('E_CANCEL_RESCUE')
        self.send_event('E_CALL_SYNC_METHOD', 'try_detach', (entity_id, lst_pos, lst_rotation), True)

    def _on_attached_fail(self):
        self._wait_attach = False

    def _on_attached(self, atch_data):
        self._wait_attach = False
        entity_id = atch_data['entity_id']
        table_id = atch_data['atch_id']
        hp = atch_data['hp']
        self._max_hp = atch_data.get('max_hp', hp)
        self.send_event('E_SUCCESS_BOARD', entity_id, table_id)
        self._cur_hp = hp
        self.send_event('E_ATTACHABLE_ON_HP_CHANGE', (hp, self._max_hp))

    def _on_detached(self, entity_id, broken=False):
        entity_id = self.ev_g_attachable_entity_id()
        if not entity_id:
            return
        self.send_event('E_CANCEL_SKATE_STATE')
        if broken:
            self.send_event('E_ATTACHABLE_ON_BROKEN', entity_id)

    def _on_damage(self, entity_id, cur_hp):
        position = self.ev_g_model_position()
        global_data.sound_mgr.play_sound('Play_bullet_hit', position, ('bullet_hit_material',
                                                                       'metal'))
        mp_attach = self.ev_g_all_attachable()
        if not mp_attach:
            return
        atch_data = mp_attach.get(entity_id)
        if not atch_data:
            return
        atch_data['hp'] = cur_hp
        self._cur_hp = cur_hp
        self.send_event('E_ATTACHABLE_ON_HP_CHANGE', (cur_hp, self._max_hp))