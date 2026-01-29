# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlMainPC.py
from __future__ import absolute_import
from six.moves import range
from .MechaControlMain import MechaControlMain
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from common.cfg import confmgr
from logic.gutils import pc_utils
from logic.gutils.client_unit_tag_utils import preregistered_tags
from .MechaBulletWidget import MechaBulletWidgetPC, MechaEnergyWidgetPC
import time
import sys
ALL_ACTION_NUMBER = 8
EXT_SKIL_BTNS = ['action7']
MECHA_UI_MPATH = 'logic.comsys.mecha_ui.%s'
CACHE_MECHA_UI_INFO = {}
ENERGY_BULLET_TYPE_MECHA_IDS = {
 8002}

class MechaControlMainPC(MechaControlMain):
    PANEL_CONFIG_NAME = 'battle_mech/mech_control_main_pc'
    UI_ACTION_EVENT = {}
    HOT_KEY_FUNC_MAP = {'mecha_special_skill.DOWN_UP': 'keyboard_use_special_skill'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'mecha_fire': {'node': 'nd_action_custom_1.temp_pc'},'mecha_sub': {'node': 'nd_action_custom_4.temp_pc'},'mecha_rush': {'node': 'nd_action_custom_6.temp_pc'},'mecha_extra_skill': {'node': 'nd_action_custom_7.temp_pc'},'mecha_aim': {'node': 'nd_action_custom_4.temp_pc'}}
    UNAVAILABLE_ACTION_IDS = ()
    DEFAULT_ACT_TEMPLATE = {'action1': 'i_mech_fire_pc',
       'action2': 'i_mech_fire_pc',
       'action3': 'i_mech_fire_pc',
       'action4': 'i_mech_sub_skill_pc',
       'action5': 'i_mech_posture',
       'action6': 'i_mech_posture',
       'action7': 'i_mech_sub_skill_pc',
       'action8': 'i_mech_posture'
       }
    GLOBAL_EVENT = MechaControlMain.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({'refresh_action467_position': 'refresh_action467_position'
       })

    def on_init_panel(self):
        super(MechaControlMainPC, self).on_init_panel()
        self.bullet_widget = None
        self._timer = 0
        self.last_pass_time = 0
        self.reload_cost_time = 0
        self.reload_pass_time = 0
        self._reload_time_scale = 0.0
        self._last_hide_name_list = []
        return

    def on_finalize_panel(self):
        super(MechaControlMainPC, self).on_finalize_panel()
        self.unregister_timer()
        self.bullet_widget and self.bullet_widget.destroy()

    def on_mecha_setted(self, mecha):
        super(MechaControlMainPC, self).on_mecha_setted(mecha)
        self.init_bullet_widget(mecha)
        if mecha:
            if mecha.MASK & preregistered_tags.VEHICLE_TAG_VALUE:
                if mecha.__class__.__name__ not in self._last_hide_name_list:
                    self._last_hide_name_list.append(mecha.__class__.__name__)
                self.add_hide_count(mecha.__class__.__name__)
            else:
                for hide_name in self._last_hide_name_list:
                    self.add_show_count(hide_name)

                self._last_hide_name_list = []
        else:
            for hide_name in self._last_hide_name_list:
                self.add_show_count(hide_name)

            self._last_hide_name_list = []

    @staticmethod
    def get_weapon_info--- This code section failed: ---

  95       0  LOAD_FAST             0  'mecha_aim_ui_name_list'
           3  POP_JUMP_IF_TRUE     10  'to 10'

  96       6  BUILD_MAP_0           0 
           9  RETURN_END_IF    
        10_0  COME_FROM                '3'

  97      10  LOAD_GLOBAL           0  'MECHA_UI_MPATH'
          13  LOAD_GLOBAL           1  'sys'
          16  BINARY_SUBSCR    
          17  BINARY_MODULO    
          18  STORE_FAST            1  'mpath'

  98      21  LOAD_GLOBAL           1  'sys'
          24  LOAD_ATTR             2  'modules'
          27  LOAD_ATTR             3  'get'
          30  LOAD_FAST             1  'mpath'
          33  CALL_FUNCTION_1       1 
          36  STORE_FAST            2  'mod'

  99      39  LOAD_FAST             2  'mod'
          42  POP_JUMP_IF_TRUE     88  'to 88'

 100      45  LOAD_GLOBAL           4  '__import__'
          48  LOAD_FAST             1  'mpath'
          51  LOAD_GLOBAL           5  'globals'
          54  CALL_FUNCTION_0       0 
          57  LOAD_GLOBAL           6  'locals'
          60  CALL_FUNCTION_0       0 
          63  CALL_FUNCTION_3       3 
          66  POP_TOP          

 101      67  LOAD_GLOBAL           1  'sys'
          70  LOAD_ATTR             2  'modules'
          73  LOAD_ATTR             3  'get'
          76  LOAD_FAST             1  'mpath'
          79  CALL_FUNCTION_1       1 
          82  STORE_FAST            2  'mod'
          85  JUMP_FORWARD          0  'to 88'
        88_0  COME_FROM                '85'

 102      88  LOAD_FAST             2  'mod'
          91  POP_JUMP_IF_FALSE   199  'to 199'

 103      94  LOAD_GLOBAL           7  'getattr'
          97  LOAD_FAST             2  'mod'
         100  LOAD_FAST             1  'mpath'
         103  BINARY_SUBSCR    
         104  LOAD_CONST            0  ''
         107  CALL_FUNCTION_3       3 
         110  STORE_FAST            3  'ui_class'

 104     113  LOAD_FAST             3  'ui_class'
         116  POP_JUMP_IF_FALSE   199  'to 199'

 105     119  LOAD_GLOBAL           9  'global_data'
         122  LOAD_ATTR            10  'game_mode'
         125  POP_JUMP_IF_FALSE   180  'to 180'
         128  LOAD_GLOBAL           9  'global_data'
         131  LOAD_ATTR            10  'game_mode'
         134  LOAD_ATTR            11  'is_pve'
         137  CALL_FUNCTION_0       0 
       140_0  COME_FROM                '125'
         140  POP_JUMP_IF_FALSE   180  'to 180'

 106     143  LOAD_GLOBAL           7  'getattr'
         146  LOAD_FAST             3  'ui_class'
         149  LOAD_CONST            2  'PVE_WEAPON_INFO'
         152  LOAD_CONST            0  ''
         155  CALL_FUNCTION_3       3 
         158  STORE_FAST            4  'pve_weapon_info'

 107     161  LOAD_FAST             4  'pve_weapon_info'
         164  LOAD_CONST            0  ''
         167  COMPARE_OP            9  'is-not'
         170  POP_JUMP_IF_FALSE   180  'to 180'

 108     173  LOAD_FAST             4  'pve_weapon_info'
         176  RETURN_END_IF    
       177_0  COME_FROM                '170'
         177  JUMP_FORWARD          0  'to 180'
       180_0  COME_FROM                '177'

 109     180  LOAD_GLOBAL           7  'getattr'
         183  LOAD_FAST             3  'ui_class'
         186  LOAD_CONST            3  'WEAPON_INFO'
         189  BUILD_MAP_0           0 
         192  CALL_FUNCTION_3       3 
         195  RETURN_END_IF    
       196_0  COME_FROM                '116'
         196  JUMP_FORWARD          0  'to 199'
       199_0  COME_FROM                '196'

 110     199  BUILD_MAP_0           0 
         202  RETURN_VALUE     

Parse error at or near `BINARY_MODULO' instruction at offset 17

    def init_bullet_widget(self, mecha):
        if not mecha:
            return
        mecha_id = mecha.share_data.ref_mecha_id
        if mecha_id not in CACHE_MECHA_UI_INFO:
            mecha_aim_ui_name_list = confmgr.get('mecha_conf', 'UIConfig', 'Content', str(mecha_id), 'append_ui')
            CACHE_MECHA_UI_INFO[mecha_id] = self.get_weapon_info(mecha_aim_ui_name_list)
        weapon_info = CACHE_MECHA_UI_INFO[mecha_id]
        if not weapon_info:
            if self.bullet_widget:
                self.bullet_widget.destroy()
                self.bullet_widget.show_nd_bullet(False)
            self.panel.nd_bullet.setVisible(False)
            return
        if mecha_id in ENERGY_BULLET_TYPE_MECHA_IDS:
            self.bullet_widget = MechaEnergyWidgetPC(self.panel, weapon_info)
        else:
            self.bullet_widget = MechaBulletWidgetPC(self.panel, weapon_info)
        if self.bullet_widget:
            self.bullet_widget.on_mecha_setted(mecha)
            self.bullet_widget.show_nd_bullet(True)

    def init_parameters(self):
        super(MechaControlMainPC, self).init_parameters()
        self.record_button_init_pos()

    def refresh_temp_pc_show(self, act_id=None):
        if not global_data.is_pc_control_enable:
            return
        else:
            if act_id is not None and act_id not in self.UNAVAILABLE_ACTION_IDS:
                nd = getattr(self.panel, act_id)
                parent = nd.GetParent()
                nd_temp_pc = getattr(parent, 'temp_pc')
                if nd_temp_pc:
                    nd_temp_pc.setVisible(nd.isVisible())
                return
            for i in range(1, ALL_ACTION_NUMBER + 1):
                action_id = 'action{}'.format(i)
                if action_id in self.UNAVAILABLE_ACTION_IDS:
                    continue
                nd = getattr(self.panel, action_id)
                parent = nd.GetParent()
                nd_temp_pc = getattr(parent, 'temp_pc')
                if nd_temp_pc:
                    nd_temp_pc.setVisible(nd.isVisible())

            return

    def on_change_ui_custom_data(self):
        if self.mecha:
            if self.mecha.__class__.__name__ != 'LMechaTrans':
                UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def on_hot_key_state_opened(self):
        self.refresh_temp_pc_show()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        pass

    def check_hot_key_shoot_buttons_show(self):
        pass

    def get_bullet_widget(self):
        return self.bullet_widget

    def set_bullet_icon(self, icon_path):
        self.panel.nd_bullet.img_bullet.SetDisplayFrameByPath('', icon_path)

    def on_reload_bullet(self, reload_time, *args):
        if not global_data.cam_lplayer:
            return
        self.last_pass_time = time.time()
        self.reload_cost_time = reload_time
        self.reload_pass_time = 0
        self.panel.action1.nd_useless.setVisible(True)
        self.panel.action1.progress_cd.setVisible(True)
        self.panel.action1.lab_cd_time.setVisible(True)
        self.register_timer()

    def on_cancel_reload(self, *args):
        if not global_data.cam_lplayer:
            return
        self.unregister_timer()
        self.panel.action1.nd_useless.setVisible(False)
        self.panel.action1.progress_cd.setVisible(False)
        self.panel.action1.lab_cd_time.setVisible(False)
        self.panel.action1.progress_cd.SetPercentage(100)

    def set_main_weapon_reload_process(self):
        from common import utilities
        now = time.time()
        pass_time = (now - self.last_pass_time) * (1.0 + self._reload_time_scale)
        self.last_pass_time = now
        self.reload_pass_time += pass_time
        left_time = self.reload_cost_time - self.reload_pass_time
        left_time = max(0, left_time)
        self.panel.action1.progress_cd.SetPercentage(utilities.safe_percent(left_time, self.reload_cost_time))
        self.panel.action1.lab_cd_time.SetString('%.1f' % left_time)
        if left_time <= 0:
            self.on_cancel_reload()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=lambda : self.set_main_weapon_reload_process(), interval=0.033, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def init_event(self, mecha=None):
        super(MechaControlMainPC, self).init_event(mecha)
        if self.mecha:
            self.refresh_action467_position()

    def on_switch_behavior(self, shape_id, *args):
        super(MechaControlMainPC, self).on_switch_behavior(shape_id, *args)
        self.refresh_action467_position()

    def refresh_action467_position(self):
        pos_index = 0
        for nd_index, act_id in enumerate(self.action467_btn_tags):
            if act_id in self.action_btns and self.action_btns[act_id].isVisible():
                self.action467_btn_nodes[nd_index].SetPosition(*self.action467_btn_pos_list[pos_index])
                pos_index += 1

    def on_set_action_visible(self, action_id, visible, force=False):
        if action_id in self.action_btns:
            self.action_btns[action_id].setVisible(visible)
            self.refresh_temp_pc_show(action_id)
        if action_id in self.action467_btn_tags:
            self.refresh_action467_position()

    def record_button_init_pos(self):
        self.action467_btn_tags = ['action4', 'action6', 'action7']
        self.action467_btn_nodes = [
         self.panel.nd_action_custom_4,
         self.panel.nd_action_custom_6,
         self.panel.nd_action_custom_7]
        self.action467_btn_pos_list = [ nd.GetPosition() for nd in self.action467_btn_nodes ]