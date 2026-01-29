# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlBtn/MechaActivateHeat.py
from __future__ import absolute_import

class MechaActivateHeat(object):
    HEAT_TEX = 'gui/ui_res_2/battle/mech_main/mech_progress_heat.png'
    NORM_TEX = 'gui/ui_res_2/battle/mech_main/mech_progress.png'
    PROCESS_TEMP = 'battle_mech/i_mech_progress1'

    def __init__(self, parent, nd_aprent, kargs):
        self.parent = parent
        self.nd_parent = nd_aprent
        self.nd_progress = global_data.uisystem.load_template_create(self.PROCESS_TEMP, self.nd_parent.nd_progress)
        self.activate_heat = False
        if not parent or not nd_aprent:
            return
        self.max_heat_value = 3000

    def bind_events(self, mecha):
        self.init_heat(mecha)
        regist_func = mecha.regist_event
        regist_func('E_SET_HEAT', self.on_heat_change)
        regist_func('E_ACTIVATE_HEAT', self.set_activate_state)

    def unbind_events(self, mecha):
        unregist_func = mecha.unregist_event
        unregist_func('E_SET_HEAT', self.on_heat_change)
        unregist_func('E_ACTIVATE_HEAT', self.set_activate_state)

    def destroy(self):
        self.nd_parent.nd_useless.img_useless.setVisible(True)
        self.nd_parent.nd_useless.progress_cd.setVisible(True)
        self.nd_parent.nd_useless.lab_cd_time.setVisible(True)
        if self.nd_progress:
            self.nd_progress.Destroy(True)
            self.nd_progress = None
        self.parent = None
        self.nd_parent = None
        return

    def init_heat(self, mecha):
        from common.cfg import confmgr
        heat_conf = confmgr.get('mecha_conf', 'HeatEnergyConfig', 'Content').get(str(8004))
        if heat_conf:
            self.max_heat_value = heat_conf.get('heat_cnt')
        heat_info = mecha.ev_g_heat() or (0, 0)
        self.on_heat_change(*heat_info)
        self.nd_progress.img_progress_full.setVisible(False)
        activate = mecha.ev_g_can_trigger_heat()
        self.activate_heat = activate
        if self.activate_heat:
            self.parent.on_add_disable_cnt()
        self.set_activate_state(self.activate_heat, True)
        self.nd_progress.progress.SetProgressTexture(self.HEAT_TEX if activate else self.NORM_TEX)

    def on_heat_change(self, heat, heat_state):
        self.nd_progress.progress.setPercentage(100.0 * heat / self.max_heat_value)

    def set_activate_state(self, flag, force=False):
        if flag == self.activate_heat and not force:
            return
        if flag:
            self.parent.on_sub_disable_cnt()
        else:
            self.parent.on_add_disable_cnt()
        self.nd_parent.nd_useless.setVisible(not flag)
        self.nd_parent.progress_cd.setVisible(flag)
        self.nd_parent.lab_cd_time.setVisible(flag)
        if flag:
            self.nd_parent.PlayAnimation('enable_heat')
            self.nd_progress.progress.SetProgressTexture(self.HEAT_TEX)
        else:
            self.nd_progress.progress.SetProgressTexture(self.NORM_TEX)
            self.nd_parent.StopAnimation('enable_heat')
        self.activate_heat = flag