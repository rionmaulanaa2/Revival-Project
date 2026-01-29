# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComStateTrkCamSimple.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.gcommon.component.UnitCom import UnitCom
SCR_TRK_LV_1 = 'SML'
SCR_TRK_LV_2 = 'BIG'
GUN_EF_LV_1 = 1
GUN_EF_LV_2 = 2
GUN_EF_LV_3 = 3
import math
from common.cfg import confmgr

class ComStateTrkCamSimple(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': ('_on_model_loaded', 10)
       }

    def __init__(self):
        super(ComStateTrkCamSimple, self).__init__()
        self.is_binded_event = False

    def _on_model_loaded(self, *args):
        self.process_mecha_ani_trk_event(True)

    def destroy(self):
        self.process_mecha_ani_trk_event(False)
        super(ComStateTrkCamSimple, self).destroy()

    def _do_animate_trigger(self, ani_id):
        trk_conf = confmgr.get('camera_trk_sfx_conf_simple')
        row_conf = trk_conf.get(str(ani_id), {})
        trk_path = row_conf.get('trk_path', '')
        offset_scale = row_conf.get('offset_mul', 1.0)
        rot_scale = row_conf.get('rot_mul', 1.0)
        is_plot = row_conf.get('is_plot', False)
        global_data.emgr.play_preset_trk_animation_simple_event.emit(trk_path, offset_scale, rot_scale, is_plot)

    def process_mecha_ani_trk_event(self, is_register):
        trk_conf = confmgr.get('camera_trk_sfx_conf_simple')
        print('process_mecha_ani_trk_event', dict(trk_conf))
        for aid, row_conf in six.iteritems(trk_conf):
            anim_name = row_conf.get('anim_name', '')
            trigger = row_conf.get('trigger', '')
            trk_path = row_conf.get('trk_path', '')
            if not (anim_name and trigger and trk_path):
                continue
            if is_register:
                self.send_event('E_REGISTER_ANIMATOR_EVENT', anim_name, trigger, self._do_animate_trigger, aid)
            else:
                self.send_event('E_UNREGISTER_ANIMATOR_EVENT', anim_name, trigger, self._do_animate_trigger)