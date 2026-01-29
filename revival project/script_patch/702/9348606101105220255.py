# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_item/ComPickableState.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.item.item_const import SCENEBOX_ST_OPENED
from logic.gcommon.common_utils import item_config

class ComPickableState(UnitCom):
    BIND_EVENT = {'G_PICK_DATA': 'get_pickobject_detail_conf',
       'E_REMOVE_CHILD_ITEM': 'remove_child_item',
       'E_PICKABLE_ITEM_COUNT': 'set_item_count',
       'E_SCENE_BOX_STAT_CHANGE': 'on_scene_box_stat_change',
       'G_SCENE_BOX_IS_OPEN': 'is_scene_box_open',
       'G_IS_OPENED': 'need_open',
       'G_ITEM_NUM': 'get_item_num',
       'G_OPEN_TIME': 'get_open_time',
       'G_ITEM_ID': 'get_item_id'
       }
    PICK_CONF_PATH = 'item'

    def __init__(self):
        super(ComPickableState, self).__init__()
        self._item_id = None
        self._item_cfg = {}
        self._item_num = 0
        return

    def reuse(self, share_data):
        super(ComPickableState, self).reuse(share_data)
        self._item_id = None
        self._item_cfg = {}
        self._item_num = 0
        return

    def cache(self):
        super(ComPickableState, self).cache()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPickableState, self).init_from_dict(unit_obj, bdict)
        self._item_id = bdict.get('item_id', 1)
        path = 'box_res' if item_utils.is_package_item(self._item_id) else self.PICK_CONF_PATH
        conf = confmgr.get(path, str(self._item_id), default=None)
        if conf is not None:
            self._item_cfg.update(conf)
        self._item_cfg['count'] = bdict.get('count', 1)
        if 'all_item' in bdict:
            self._item_cfg['all_item'] = bdict['all_item']
        if 'attachment' in bdict:
            self._item_cfg['attachment'] = bdict['attachment']
        if 'iDur' in bdict:
            self._item_cfg['iDur'] = bdict['iDur']
        if 'thrower' in bdict:
            self._item_cfg['thrower'] = bdict['thrower']
        if 'status' in bdict:
            self._item_cfg['status'] = bdict['status']
        if 'faction_id' in bdict:
            self._item_cfg['faction_id'] = bdict['faction_id']
        self._item_num = bdict.get('item_num')
        return

    def is_scene_box_open(self):
        return self.get_pickobject_detail_conf().get('status') == SCENEBOX_ST_OPENED

    def need_open(self):
        return self.get_pickobject_detail_conf().get('status', SCENEBOX_ST_OPENED) == SCENEBOX_ST_OPENED

    def get_pickobject_detail_conf(self):
        item_no_conf = {'wid': self.unit_obj.id,'item_id': self._item_cfg['item_no']}
        self._item_cfg.update(item_no_conf)
        return self._item_cfg

    def remove_child_item(self, entity_id):
        self._item_cfg['changed'] = True
        if 'all_item' in self._item_cfg:
            if entity_id in self._item_cfg['all_item']:
                del self._item_cfg['all_item'][entity_id]
        elif 'attachment' in self._item_cfg:
            pos = None
            for attachment_pos, item_data in six.iteritems(self._item_cfg['attachment']):
                if item_data['entity_id'] == entity_id:
                    pos = attachment_pos

            if pos is not None:
                del self._item_cfg['attachment'][pos]
        return

    def set_item_count(self, entity_id, count):
        self._item_cfg['changed'] = True
        if entity_id is None:
            self._item_cfg['count'] = count
        if count <= 0:
            self.remove_child_item(entity_id)
            return
        else:
            if 'all_item' in self._item_cfg:
                if entity_id in self._item_cfg['all_item']:
                    item_conf = self._item_cfg['all_item'][entity_id]
                    if item_conf:
                        item_conf['count'] = count
            return

    def on_scene_box_stat_change(self, status):
        self._item_cfg['status'] = status

    def get_item_num(self):
        return self._item_num

    def get_open_time(self):
        conf = item_config.get_use_by_id(str(self._item_id))
        if not conf:
            return 0
        return conf['fSingTime']

    def get_item_id(self):
        return self._item_id