# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComAttachHolder.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
import math3d

class ComAttachHolder(UnitCom):
    BIND_EVENT = {'G_DO_ATTACH': '_do_attach',
       'G_DO_DETACH': '_do_detach',
       'G_ALL_ATTACHABLE': 'get_all_attachable',
       'G_ATTACHABLE_BY_ID': 'get_attachable_by_id'
       }

    def __init__(self):
        super(ComAttachHolder, self).__init__()
        self._mp_attachables = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComAttachHolder, self).init_from_dict(unit_obj, bdict)
        self._mp_attachables = bdict.get('attachables', self._mp_attachables)

    def on_init_complete(self):
        self.send_event('E_ATTACHABLE_INIT')

    def get_client_dict(self):
        cdict = {'attachables': self._mp_attachables
           }
        return cdict

    def get_all_attachable(self):
        return self._mp_attachables

    def get_attachable_by_id(self, atch_id):
        for entity_id, data in six.iteritems(self._mp_attachables):
            if atch_id == data.get('atch_id'):
                return data

    def _do_attach(self, atch_data):
        entity_id = atch_data['entity_id']
        if entity_id in self._mp_attachables:
            log_error('ComAttachHolder: attach reduplicative entity - %s', entity_id)
            self.send_event('E_ON_ATTACHED_FAIL')
            return
        self.sd.ref_skate_appearance_agent.set_cur_skate_entity_id(entity_id)
        self._mp_attachables[entity_id] = atch_data
        self.send_event('E_ON_ATTACHED', atch_data)

    def _do_detach(self, entity_id, broken=False):
        if entity_id not in self._mp_attachables:
            return
        else:
            atch_data = self._mp_attachables.pop(entity_id)
            self.send_event('E_ON_DETACHED', entity_id, broken)
            self.sd.ref_skate_appearance_agent.set_cur_skate_entity_id(None)
            return atch_data