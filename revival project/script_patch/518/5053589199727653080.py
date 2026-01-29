# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComHitFlagAppearance.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
import world
import math3d

class ComHitFlagAppearance(UnitCom):
    BIND_EVENT = {'E_HIT_FLAG_LEVEL_CHANGED': 'on_hit_flag_level_changed',
       'E_MODEL_LOADED': 'on_model_loaded'
       }

    def __init__(self):
        super(ComHitFlagAppearance, self).__init__()
        self._sfx = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHitFlagAppearance, self).init_from_dict(unit_obj, bdict)
        self._sfx_dict = {}
        self._flag_iterids = six.iterkeys(confmgr.get('mecha_conf', 'HitFlagConfig', 'Content'))

    def on_hit_flag_level_changed(self, flag_id, level):
        self.create_sfx(flag_id, level)

    def create_sfx(self, flag_id, level):
        self.destroy_sfx(flag_id)
        sfx_list = confmgr.get('mecha_conf', 'HitFlagConfig', 'Content').get(str(flag_id), {}).get('sfx_list', [])
        if level >= len(sfx_list):
            return
        else:
            show_conf = confmgr.get('mecha_conf', 'ImmoClientConf', 'Content')
            socket = show_conf.get(str(self.sd.ref_mecha_id), {}).get('socket', None)
            model = self.ev_g_model()
            if not model:
                return
            if not socket:
                return

            def create_cb(sfx):
                if self.is_valid():
                    self.destroy_sfx(flag_id)
                    self._sfx_dict[flag_id] = sfx
                else:
                    global_data.sfx_mgr.remove_sfx(sfx)

            _sfx_path = sfx_list[level]
            if _sfx_path:
                global_data.sfx_mgr.create_sfx_on_model(_sfx_path, self.ev_g_model(), socket, world.BIND_TYPE_TRANSLATE, on_create_func=create_cb)
            return

    def destroy_sfx(self, flag_id):
        if flag_id in self._sfx_dict:
            global_data.sfx_mgr.remove_sfx(self._sfx_dict[flag_id])
            self._sfx_dict.pop(flag_id, None)
        return

    def destroy(self):
        for flag_id in self._flag_iterids:
            self.destroy_sfx(flag_id)

        super(ComHitFlagAppearance, self).destroy()

    def on_model_loaded(self, model):
        for flag_id in self._flag_iterids:
            flag_id = int(flag_id)
            self.on_hit_flag_level_changed(flag_id, self.ev_g_hit_flag_level(flag_id))