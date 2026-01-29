# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComVibrate.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ui_operation_const as uoc
from data.vibrate_key_def import INJURED_VIBRATE_LV, DESTROYED_VIBRATE_LV

class ComVibrate(UnitCom):
    BIND_EVENT = {'E_HITED_SHOW_HURT_DIR': 'show_hurt_dir',
       'E_DEATH': 'on_death',
       'E_DEFEATED': 'on_death'
       }

    def show_hurt_dir(self, unit, pos, damage=0, is_mecha=False):
        if not global_data.player:
            return
        if global_data.player.get_setting(uoc.CONF_SHAKE_KEY_PATTERN % uoc.CONF_SHAKE_INJURE):
            if not global_data.vibrate_mgr:
                from logic.comsys.vibrate.VibrateMgr import VibrateMgr
                VibrateMgr()
            global_data.vibrate_mgr.start_vibrate(INJURED_VIBRATE_LV)

    def on_death(self, *args, **kwargs):
        if not global_data.player:
            return
        if global_data.player.get_setting(uoc.CONF_SHAKE_KEY_PATTERN % uoc.CONF_SHAKE_MECHA_DESTROY):
            if not global_data.vibrate_mgr:
                from logic.comsys.vibrate.VibrateMgr import VibrateMgr
                VibrateMgr()
            global_data.vibrate_mgr.start_vibrate(DESTROYED_VIBRATE_LV)