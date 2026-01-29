# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/VehicleSettingWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const import ui_operation_const as uoc
from .SettingWidgetBase import SettingWidgetBase

class VehicleSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(VehicleSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.init_vehicle_setting(self.panel)

    def on_exit_page(self, **kwargs):
        super(VehicleSettingWidget, self).on_exit_page()
        self.sync_setting_data()

    def on_recover_default(self, **kwargs):
        self.recover_drive_setting()

    def sync_setting_data(self):
        if global_data.player:
            global_data.player.save_settings_to_file()

    def init_vehicle_setting(self, page):
        from logic.gutils.template_utils import init_radio_group, attach_radio_group_data, set_radio_group_item_select
        init_radio_group(page)
        sel_list = [uoc.DRIVE_OPE_BUTTON, uoc.DRIVE_OPE_FORWARD, uoc.DRIVE_OPE_ROCKER]
        attach_radio_group_data([page.pnl_1, page.pnl_2, page.pnl_3], sel_list)
        checkbox = page.pnl_1.checkbox
        checkbox.setVisible(not global_data.is_pc_mode)

        def play_pnl_1_animation(pnl=page.pnl_1):
            pnl.StopAnimation('show_1')
            pnl.StopAnimation('show_1_1')
            if page.pnl_1.nd_1.isVisible():
                pnl.RecoverAnimationNodeState('show_1')
                pnl.PlayAnimation('show_1')
            else:
                pnl.RecoverAnimationNodeState('show_1_1')
                pnl.PlayAnimation('show_1_1')

        @checkbox.btn.unique_callback()
        def OnClick(btn, touch, checkbox=checkbox, pnl=page.pnl_1):
            choose = not checkbox.choose.isVisible()
            sel = choose or uoc.DRIVE_OPE_BUTTON_MOVE_LEFT if 1 else uoc.DRIVE_OPE_BUTTON_MOVE_RIGHT
            global_data.emgr.drive_ui_button_ope_change_event.emit(sel)
            checkbox.choose.setVisible(choose)
            pnl.nd_1.setVisible(choose)
            pnl.nd_2.setVisible(not choose)
            if pnl.choose.isVisible():
                play_pnl_1_animation()
            else:
                pnl.StopAnimation('show_1_1')
                pnl.RecoverAnimationNodeState('show_1_1')
                pnl.StopAnimation('show_1')
                pnl.RecoverAnimationNodeState('show_1')

        is_check = global_data.player.get_setting_2(uoc.DRIVE_OPE_BUTTON_DIR_KEY) != uoc.DRIVE_OPE_BUTTON_DEF
        checkbox.choose.setVisible(is_check)
        page.pnl_1.nd_1.setVisible(is_check)
        page.pnl_1.nd_2.setVisible(not is_check)
        page.pnl_1.RecordAnimationNodeState('show_1_1')
        page.pnl_1.RecordAnimationNodeState('show_1')
        page.pnl_2.RecordAnimationNodeState('show_2')
        page.pnl_3.RecordAnimationNodeState('show_3')
        manual_init_node = [page.pnl_2.speed_up, page.pnl_2.stop, page.pnl_2.back]
        for nd in manual_init_node:
            pass

        cur_pnl = [None]
        operation_list = [
         1, 2, 3]
        for operation_index in operation_list:
            pnl = getattr(page, 'pnl_{0}'.format(operation_index))
            if not pnl:
                continue

            @pnl.unique_callback()
            def OnSelect(btn, choose, trigger_event=True, index=operation_index, pnl=pnl, cur_pnl=cur_pnl):
                btn.bg.SetSelect(choose)
                cur_pnl[0] = pnl
                pnl_ani = 'show_{}'.format(index)
                if choose:
                    if index != 1:
                        pnl.PlayAnimation(pnl_ani)
                    else:
                        play_pnl_1_animation()
                elif index == 1:
                    pnl.StopAnimation('show_1')
                    pnl.StopAnimation('show_1_1')
                    pnl.RecoverAnimationNodeState('show_1')
                    pnl.RecoverAnimationNodeState('show_1_1')
                else:
                    pnl.StopAnimation(pnl_ani)
                    pnl.RecoverAnimationNodeState(pnl_ani)
                    if index == 2:
                        for nd in manual_init_node:
                            pass

                if trigger_event and choose:
                    global_data.emgr.drive_ui_ope_change_event.emit(sel_list[index - 1])

        set_radio_group_item_select(page, global_data.player.get_setting_2(uoc.DRIVE_OPE_KEY), False)
        page.pnl_3.setVisible(not global_data.is_pc_mode)
        return

    def recover_drive_setting(self):
        page = self.panel
        from logic.gutils.template_utils import set_radio_group_item_select
        set_radio_group_item_select(page, global_data.player.get_default_setting_2(uoc.DRIVE_OPE_KEY), True)
        default_val = global_data.player.get_default_setting_2(uoc.DRIVE_OPE_BUTTON_DIR_KEY)
        if page.pnl_1.checkbox.choose.isVisible() != False:
            page.pnl_1.checkbox.btn.OnClick(None)
        return