# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FightStateUI.py
from __future__ import absolute_import
from common.const.uiconst import HP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.mecha_module_utils import get_module_card_name_and_desc
from logic.gcommon.common_const import mecha_const
from logic.gutils.template_utils import get_module_show_slot_pic
MODULE_TIPS_OFFSET_X = 20
MODULE_TIPS_OFFSET_Y = 55
MODULE_TIPS_OFFSET_Y_2 = -95
from common.const import uiconst

class FightStateBaseUI(MechaDistortHelper, BasePanel):
    DLG_ZORDER = HP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(FightStateBaseUI, self).on_init_panel()
        self._show_panel = False
        self.init_mecha_com()
        self.init_battle_show()
        self.init_custom_com()
        self.init_mecha_tips_com()
        self.init_event()
        self.init_custom_com()

    def do_hide_panel(self):
        BasePanel.do_hide_panel(self)

    def do_show_panel(self):
        BasePanel.do_show_panel(self)

    def init_event(self):
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_player_setted
        global_data.emgr.game_mode_init_complete += self.init_battle_show
        global_data.emgr.settle_stage_event += (self.on_create_settle_stage_ui,)
        global_data.emgr.scene_observed_player_setted_event += self.on_cam_player_setted

    def on_create_settle_stage_ui(self, *args):
        self.switch_to_non_mecha()

    def on_cam_player_setted(self, *args):
        self.on_ctrl_target_changed()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_mecha_com(self):
        from logic.comsys.mecha_ui.MechaModuleGroupWidget import MechaModuleGroupWidget
        self.mecha_com = MechaModuleGroupWidget(self.panel.nd_mech_state)

    def init_mecha_tips_com(self):
        panel_0 = global_data.uisystem.load_template_create('battle_mech/i_fight_module_tips', parent=self.panel.temp_module_tips, name='i_fight_module_tips')
        widget_0 = FightModuleTipsUI(self, panel_0)
        self.mecha_tips_com_0 = widget_0
        self.mecha_tips_com_0.hide()
        panel_1 = global_data.uisystem.load_template_create('battle_mech/i_fight_module_tips', parent=self.panel.temp_module_tips2, name='i_fight_module_tips2')
        widget_1 = FightModuleTipsUI(self, panel_1)
        self.mecha_tips_com_1 = widget_1
        self.mecha_tips_com_1.hide()

    def on_finalize_panel--- This code section failed: ---

  87       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'destroy_widget'
           6  LOAD_CONST            1  'mecha_com'
           9  CALL_FUNCTION_1       1 
          12  POP_TOP          

  88      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             0  'destroy_widget'
          19  LOAD_CONST            2  'koth_money_com'
          22  CALL_FUNCTION_1       1 
          25  POP_TOP          

  89      26  LOAD_GLOBAL           1  'hasattr'
          29  LOAD_GLOBAL           3  'destroy'
          32  CALL_FUNCTION_2       2 
          35  POP_JUMP_IF_FALSE    72  'to 72'
          38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             2  'custom_ui_com'
        44_0  COME_FROM                '35'
          44  POP_JUMP_IF_FALSE    72  'to 72'

  90      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             2  'custom_ui_com'
          53  LOAD_ATTR             3  'destroy'
          56  CALL_FUNCTION_0       0 
          59  POP_TOP          

  91      60  LOAD_CONST            0  ''
          63  LOAD_FAST             0  'self'
          66  STORE_ATTR            2  'custom_ui_com'
          69  JUMP_FORWARD          0  'to 72'
        72_0  COME_FROM                '69'

  92      72  LOAD_FAST             0  'self'
          75  LOAD_ATTR             5  'mecha_tips_com_0'
          78  POP_JUMP_IF_FALSE    97  'to 97'

  93      81  LOAD_FAST             0  'self'
          84  LOAD_ATTR             5  'mecha_tips_com_0'
          87  LOAD_ATTR             3  'destroy'
          90  CALL_FUNCTION_0       0 
          93  POP_TOP          
          94  JUMP_FORWARD          0  'to 97'
        97_0  COME_FROM                '94'

  94      97  LOAD_FAST             0  'self'
         100  LOAD_ATTR             6  'mecha_tips_com_1'
         103  POP_JUMP_IF_FALSE   122  'to 122'

  95     106  LOAD_FAST             0  'self'
         109  LOAD_ATTR             6  'mecha_tips_com_1'
         112  LOAD_ATTR             3  'destroy'
         115  CALL_FUNCTION_0       0 
         118  POP_TOP          
         119  JUMP_FORWARD          0  'to 122'
       122_0  COME_FROM                '119'

  96     122  LOAD_GLOBAL           7  'global_data'
         125  LOAD_ATTR             8  'emgr'
         128  DUP_TOP          
         129  LOAD_ATTR             9  'scene_camera_player_setted_event'
         132  LOAD_FAST             0  'self'
         135  LOAD_ATTR            10  'on_cam_player_setted'
         138  INPLACE_SUBTRACT 
         139  ROT_TWO          
         140  STORE_ATTR            9  'scene_camera_player_setted_event'

  97     143  LOAD_GLOBAL           7  'global_data'
         146  LOAD_ATTR             8  'emgr'
         149  DUP_TOP          
         150  LOAD_ATTR            11  'game_mode_init_complete'
         153  LOAD_FAST             0  'self'
         156  LOAD_ATTR            12  'init_battle_show'
         159  INPLACE_SUBTRACT 
         160  ROT_TWO          
         161  STORE_ATTR           11  'game_mode_init_complete'

  98     164  LOAD_GLOBAL           7  'global_data'
         167  LOAD_ATTR             8  'emgr'
         170  DUP_TOP          
         171  LOAD_ATTR            13  'settle_stage_event'
         174  LOAD_FAST             0  'self'
         177  LOAD_ATTR            14  'on_create_settle_stage_ui'
         180  BUILD_TUPLE_1         1 
         183  INPLACE_SUBTRACT 
         184  ROT_TWO          
         185  STORE_ATTR           13  'settle_stage_event'

  99     188  LOAD_GLOBAL           7  'global_data'
         191  LOAD_ATTR             8  'emgr'
         194  DUP_TOP          
         195  LOAD_ATTR            15  'scene_observed_player_setted_event'
         198  LOAD_FAST             0  'self'
         201  LOAD_ATTR            10  'on_cam_player_setted'
         204  INPLACE_SUBTRACT 
         205  ROT_TWO          
         206  STORE_ATTR           15  'scene_observed_player_setted_event'
         209  LOAD_CONST            0  ''
         212  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 32

    def switch_to_mecha(self):
        if not self._in_mecha_state:
            self.panel.StopAnimation('switch_to_people')
            self.panel.nd_module_group.stopAllActions()
            self.panel.PlayAnimation('switch_to_mech')
        self.panel.nd_custom.setVisible(True)
        self._show_panel = True
        super(FightStateBaseUI, self).switch_to_mecha()

    def switch_to_non_mecha(self):
        if self._in_mecha_state:
            self.panel.StopAnimation('switch_to_mech')
            self.panel.nd_module_group.stopAllActions()
            self.panel.PlayAnimation('switch_to_people')
        self.panel.nd_custom.setVisible(False)
        self._show_panel = False
        super(FightStateBaseUI, self).switch_to_non_mecha()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def init_battle_show(self):
        from logic.comsys.battle.King.KothMoneyWidget import KothMoneyWidget
        self.koth_money_com = KothMoneyWidget(self.panel.nd_special)
        self.koth_money_com.init_widget()

    def show_mecha_module_tips(self, slot_no, item_info, icon_path, click_pos):
        if self.mecha_tips_com_0 is None or self.mecha_tips_com_1 is None:
            return
        else:
            self.mecha_tips_com_0.init_one_module_tip(slot_no, item_info, icon_path, 0)
            self.panel.temp_module_tips.SetPosition(click_pos[0] + MODULE_TIPS_OFFSET_X, click_pos[1] + MODULE_TIPS_OFFSET_Y)
            self.mecha_tips_com_0.show()
            card_ids = item_info.get('card_ids', [])
            if len(card_ids) > 1 and slot_no == mecha_const.SP_MODULE_SLOT:
                self.mecha_tips_com_1.init_one_module_tip(slot_no, item_info, icon_path, 1)
                self.panel.temp_module_tips2.SetPosition(click_pos[0] + MODULE_TIPS_OFFSET_X, click_pos[1] + MODULE_TIPS_OFFSET_Y_2)
                self.mecha_tips_com_1.show()
            return

    def hide_mecha_module_tips(self):
        if self.mecha_tips_com_0:
            self.mecha_tips_com_0.hide()
        if self.mecha_tips_com_1:
            self.mecha_tips_com_1.hide()


class FightModuleTipsUI(BaseUIWidget):
    SLOT_TO_MODULE_TYPE = {1: 'atk',
       2: 'def',
       3: 'spd',
       4: 'sp'
       }

    def __init__(self, parent, panel):
        super(FightModuleTipsUI, self).__init__(parent, panel)

    def init_one_module_tip(self, slot_no, item_info, card_icon_path, tip_no):
        card_lv = item_info.get('card_lv')
        card_ids = item_info.get('card_ids')
        active_card_id = item_info.get('active_card_id')
        if tip_no > 0 and len(card_ids) < 2:
            return
        else:
            real_card_id = card_ids[tip_no]
            if active_card_id is not None:
                if active_card_id != real_card_id:
                    card_lv = None
                    card_icon_path = get_module_show_slot_pic(slot_no, real_card_id, card_lv)
            module_icon_path = self.get_module_icon_path_by_slot_and_lv(slot_no, card_lv)
            self.panel.bar_module.SetDisplayFrameByPath('', module_icon_path)
            self.panel.bar_module.img_module.SetDisplayFrameByPath('', card_icon_path)
            card_name_desc, card_effect_desc = get_module_card_name_and_desc(real_card_id, card_lv)
            self.panel.lab_name.SetString(card_name_desc)
            if card_lv is None:
                self.panel.lab_name.SetColor('#DC')
            else:
                self.panel.lab_name.SetColor('#SW')
            self.panel.lab_details.SetString(card_effect_desc)
            if slot_no == mecha_const.SP_MODULE_SLOT:
                self.panel.bar_module.img_core_num.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_module/icon_module_sp_%d.png' % (tip_no + 1))
                self.panel.bar_module.img_core_num.setVisible(True)
            else:
                self.panel.bar_module.img_core_num.setVisible(False)
            return

    def get_module_icon_path_by_slot_and_lv(self, slot_no, card_lv):
        card_lv_str = card_lv
        if slot_no == mecha_const.SP_MODULE_SLOT:
            card_lv_str = 'gold'
        if card_lv is None:
            card_lv_str = 'empty'
        module_type = FightModuleTipsUI.SLOT_TO_MODULE_TYPE[slot_no]
        return 'gui/ui_res_2/battle/mech_module/big_bar_module_{}_{}.png'.format(module_type, card_lv_str)


class FightStateUI(FightStateBaseUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_state'

    def leave_screen(self):
        super(FightStateUI, self).leave_screen()
        global_data.ui_mgr.close_ui('FightStateUI')