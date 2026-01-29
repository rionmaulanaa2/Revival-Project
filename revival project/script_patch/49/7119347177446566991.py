# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/MechaTransMoveHelperUI.py
from __future__ import absolute_import
import world
from common.const.uiconst import ROCKER_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils import rocker_utils
from logic.gcommon.common_const import mecha_const as mconst
from logic.gutils import hot_key_utils
from data import hot_key_def
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from common.const import uiconst

class MechaTransMoveHelperUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty_touchable'
    DLG_ZORDER = ROCKER_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'check_drive_control_continue_event': 'check_drive_control_continue',
       'mecha_trans_pattern_handle_event': 'check_mecha_trans_pattern',
       'drive_ui_ope_change_event': 'on_switch_car_ope',
       'on_touch_drive_ui_event': 'on_touch_drive_ui',
       'on_touch_move_rocker_event': 'on_touch_drive_ui'
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.setLocalZOrder(1)
        self.install()
        self.is_in_touch = False
        self.need_transfer = False
        self.has_begin_transfer = False
        if global_data.mecha and global_data.mecha.logic:
            self._pattern = global_data.mecha.logic.ev_g_pattern()
        else:
            self._pattern = None
        self.cur_drive_ope_sel = global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY)
        self.move_vec = ccp(0, 0)
        self.touch_begin_pos = ccp(0, 0)
        self.touch_move_pos = ccp(0, 0)
        self.force_move_direction = None
        self._cur_touch_id = None
        return

    def install(self):
        self.panel.BindMethod('OnBegin', self.on_touch_begin)
        self.panel.BindMethod('OnDrag', self.on_touch_move)
        self.panel.BindMethod('OnEnd', self.on_touch_end)
        self.panel.BindMethod('OnCancel', self.on_touch_canceled)

    def uninstall(self):
        self.panel.UnBindMethod('OnBegin')
        self.panel.UnBindMethod('OnDrag')
        self.panel.UnBindMethod('OnEnd')
        self.panel.UnBindMethod('OnCancel')

    def on_finalize_panel(self):
        if self.is_in_touch:
            self.check_end()

    def on_touch_begin(self, btn, touch):
        self.is_in_touch = True
        return True

    def on_touch_drive_ui(self, touch):
        if self.is_in_touch:
            cur_touch_id = touch.getId()
            self._cur_touch_id = cur_touch_id
            self.panel.SetPassedTouchId(cur_touch_id)
            self.move_vec = ccp(0, 0)
            self.touch_begin_pos = touch.getStartLocation()

    def on_touch_move(self, btn, touch):
        self.touch_move_pos = touch.getLocation()
        if self.need_transfer:
            start_location = self.touch_begin_pos
            cnt_location = self.touch_move_pos
            self.move_vec = ccp(cnt_location.x - start_location.x, cnt_location.y - start_location.y)
            self.on_transfer_move()

    def on_touch_end(self, btn, touch):
        self.check_end()

    def on_touch_canceled(self, btn, touch):
        self.check_end()

    def check_end(self):
        if self.need_transfer:
            self.on_transfer_end()
        self.is_in_touch = False
        self.need_transfer = False
        self.has_begin_transfer = False
        self._cur_touch_id = None
        self.panel.SetPassedTouchId(None)
        return

    def check_mecha_trans_pattern(self, pattern, *args, **kwargs):
        self._pattern = pattern
        self.force_move_direction = None
        if self.cur_drive_ope_sel in [uoc.DRIVE_OPE_BUTTON]:
            if pattern == mconst.MECHA_PATTERN_NORMAL:
                ui = global_data.ui_mgr.get_ui('DriveUI')
                if ui:
                    move_dir = ui.get_move_direction()
                    if move_dir:
                        self.force_move_direction = ccp(-self.move_vec.x, move_dir * 50)
            else:
                import math
                ui = global_data.ui_mgr.get_ui('MoveRockerUI')
                if ui:
                    cur_rocker_dir = ui.get_move_dir()
                    if cur_rocker_dir:
                        self.force_move_direction = ccp(-self.move_vec.x, (-1 if cur_rocker_dir.z < 0 else 1) * 50)
        if self.cur_drive_ope_sel in [uoc.DRIVE_OPE_FORWARD]:
            self.force_move_direction = ccp(-self.move_vec.x, 0)
        return

    def check_drive_control_continue(self):
        if self.cur_drive_ope_sel == uoc.DRIVE_OPE_ROCKER:
            return
        else:
            if self.is_in_touch and self._cur_touch_id is not None:
                self.has_begin_transfer = False
                self.need_transfer = True
                start_location = self.touch_begin_pos
                cnt_location = self.touch_move_pos
                self.move_vec = ccp(cnt_location.x - start_location.x, cnt_location.y - start_location.y)
                self.on_continue_move()
            return

    def on_switch_car_ope(self, new_ope):
        self.cur_drive_ope_sel = new_ope
        self.force_move_direction = None
        if self.is_in_touch and self.need_transfer:
            self.on_transfer_end()
            self.panel.SetEnableTouch(False)
            self.panel.SetEnableTouch(True)
        return

    def get_target_ui(self):
        if self._pattern == mconst.MECHA_PATTERN_VEHICLE:
            return global_data.ui_mgr.get_ui('DriveUI')
        else:
            if self._pattern == mconst.MECHA_PATTERN_NORMAL:
                return global_data.ui_mgr.get_ui('MoveRockerUI')
            return None
            return None

    def on_transfer_begin(self, move_vec):
        ui = self.get_target_ui()
        if ui:
            return ui.on_received_begin_command(move_vec)

    def on_continue_move(self):
        self.on_transfer_move()

    def on_transfer_move(self):
        if self.force_move_direction:
            real_move = ccp(self.move_vec.x + self.force_move_direction.x, self.move_vec.y + self.force_move_direction.y)
        else:
            real_move = self.move_vec
        if not self.has_begin_transfer:
            if self.on_transfer_begin(real_move):
                self.has_begin_transfer = True
        if self.has_begin_transfer:
            ui = self.get_target_ui()
            if ui:
                ui.on_received_move_command(real_move)

    def on_transfer_end(self):
        ui = self.get_target_ui()
        if ui:
            ui.on_received_end_command()