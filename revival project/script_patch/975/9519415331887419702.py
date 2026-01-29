# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlBtn/MechaShootMode.py
from __future__ import absolute_import
from logic.gcommon.common_const.mecha_const import MECHA_SHOOT_NORMAL, MECHA_SHOOT_QUICK
from logic.gcommon.common_utils.local_text import get_text_by_id

class MechaShootMode(object):

    def __init__(self, parent, nd_aprent, kargs):
        self.parent = parent
        self.nd_parent = nd_aprent
        if not parent or not nd_aprent:
            return
        else:
            self.real_parent = self.nd_parent.GetParent().GetParent().nd_rot
            old_temp = self.real_parent.nd_special
            if old_temp:
                pos = old_temp.GetPosition()
                old_temp.Destroy(True)
                new_temp = global_data.uisystem.load_template_create('battle_mech/i_mech8005_switch_btn')
                self.real_parent.AddChild('nd_special', new_temp)
                self.real_parent.nd_special.setVisible(True)
                new_temp.SetPosition(*pos)
                self._init_shoot_mode_btn()
            self.mecha = None
            self.shoot_mode = MECHA_SHOOT_NORMAL
            self.init_custom_com()
            self.force_operate_events_bound = True
            return

    def init_custom_com(self):
        self.panel = self.real_parent.nd_special
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def bind_events(self, mecha):
        global_data.emgr.hot_key_swtich_on_event += self.show_hot_key
        global_data.emgr.hot_key_swtich_off_event += self.show_hot_key
        self.mecha = mecha
        regist_func = mecha.regist_event
        regist_func('E_ON_SHOOT_MODE_CHANGED', self._on_shoot_mode_changed)
        self.shoot_mode = self.mecha.ev_g_shoot_mode()
        self._on_shoot_mode_changed(self.shoot_mode)

    def unbind_events(self, mecha):
        global_data.emgr.hot_key_swtich_on_event -= self.show_hot_key
        global_data.emgr.hot_key_swtich_off_event -= self.show_hot_key
        if not mecha:
            return
        else:
            unregist_func = mecha.unregist_event
            unregist_func('E_ON_SHOOT_MODE_CHANGED', self._on_shoot_mode_changed)
            self.mecha = None
            return

    def _init_shoot_mode_btn(self):
        parent_top = self.real_parent

        @parent_top.nd_special.btn.unique_callback()
        def OnClick(btn, touch):
            click_succ = self._on_shoot_mode_btn_begin()
            if click_succ:
                btn.SetSelect(True) if self.shoot_mode == MECHA_SHOOT_NORMAL else btn.SetSelect(False)
            return click_succ

        @parent_top.nd_special.btn.unique_callback()
        def OnEnd(btn, touch):
            end_succ = self._on_shoot_mode_btn_end()
            if end_succ:
                btn.SetSelect(False) if self.shoot_mode == MECHA_SHOOT_NORMAL else btn.SetSelect(True)
            return end_succ

        self.show_hot_key()

    def show_hot_key(self):
        if global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            from data.hot_key_def import MECHA_SPECIAL_SKILL
            hot_key_func_name = MECHA_SPECIAL_SKILL
            from logic.gutils.hot_key_utils import set_hot_key_common_tip
            self.real_parent.nd_special.temp_pc.setVisible(True)
            set_hot_key_common_tip(self.real_parent.nd_special.temp_pc, hot_key_func_name)
        else:
            self.real_parent.nd_special.temp_pc.setVisible(False)

    def _on_shoot_mode_changed(self, shoot_mode):
        self.shoot_mode = shoot_mode
        if self.real_parent.nd_special.lab_switch:
            mode_btn_selected = False
            if self.shoot_mode == MECHA_SHOOT_NORMAL:
                self.real_parent.nd_special.lab_switch.SetString(get_text_by_id(18703))
            else:
                mode_btn_selected = True
                self.real_parent.nd_special.lab_switch.SetString(get_text_by_id(18704))
            self.real_parent.nd_special.btn.SetSelect(mode_btn_selected)

    def _on_shoot_mode_btn_begin(self):
        if self.mecha:
            return self.mecha.ev_g_action_down('action5')
        else:
            return False

    def _on_shoot_mode_btn_end(self):
        if self.mecha:
            return self.mecha.send_event('E_ACTION_UP', 'action5')
        else:
            return False

    def destroy--- This code section failed: ---

 109       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'real_parent'
           6  LOAD_ATTR             1  'nd_special'
           9  LOAD_ATTR             2  'setVisible'
          12  LOAD_GLOBAL           3  'False'
          15  CALL_FUNCTION_1       1 
          18  POP_TOP          

 110      19  LOAD_CONST            0  ''
          22  LOAD_FAST             0  'self'
          25  STORE_ATTR            5  'panel'

 111      28  LOAD_GLOBAL           6  'hasattr'
          31  LOAD_GLOBAL           1  'nd_special'
          34  CALL_FUNCTION_2       2 
          37  POP_JUMP_IF_FALSE    74  'to 74'
          40  LOAD_FAST             0  'self'
          43  LOAD_ATTR             7  'custom_ui_com'
        46_0  COME_FROM                '37'
          46  POP_JUMP_IF_FALSE    74  'to 74'

 112      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             7  'custom_ui_com'
          55  LOAD_ATTR             8  'destroy'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

 113      62  LOAD_CONST            0  ''
          65  LOAD_FAST             0  'self'
          68  STORE_ATTR            7  'custom_ui_com'
          71  JUMP_FORWARD          0  'to 74'
        74_0  COME_FROM                '71'

 115      74  LOAD_CONST            0  ''
          77  LOAD_FAST             0  'self'
          80  STORE_ATTR            9  'parent'

 116      83  LOAD_CONST            0  ''
          86  LOAD_FAST             0  'self'
          89  STORE_ATTR           10  'nd_parent'
          92  LOAD_CONST            0  ''
          95  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 34