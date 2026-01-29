# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/BattleSettingUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from logic.comsys.setting_ui.SimpleLabelUIBase import SimpleLabelUIBase
from logic.gcommon.common_const import ui_operation_const
from logic.gcommon.common_utils.local_text import get_text_by_id

class BattleSettingUI(SimpleLabelUIBase):
    PANEL_CONFIG_NAME = 'setting/setting'
    DLG_ZORDER = TOP_ZORDER
    LABEL_SENSITY = 2
    LABEL_OCC = 5
    LABEL_SHOT = 6
    LABEL_OTHER = 8
    LABEL_ADD_ITEM = 9
    LABEL_PROFILE = 10
    LABEL_WWISE_PROFILE = 11
    LABEL_VEHICLE_PROFILE = 12
    LABEL_GTRACE = 13
    LABEL_DEFAULT = 1
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'btn_exit.OnClick': 'on_click_exit_btn',
       'btn_input.OnClick': 'on_click_input'
       }

    def on_click_close_btn(self, *args):
        self.close()

    def on_click_exit_btn(self, *args):
        self.close()
        global_data.player.quit_battle()

    def on_click_input(self, *args):
        cmd = self.panel.input.getString()
        if not cmd:
            cmd = ''
        from engine.game import on_debug_input
        on_debug_input(cmd)

    def on_init_panel(self):
        self.init_event()
        self._init_menu()
        global_data.emgr.scene_set_survive_visible_event.emit('BattleSettingUI', False)
        self.show_sst_figure()

    def on_finalize_panel(self):
        self.player = None
        global_data.emgr.scene_set_survive_visible_event.emit('BattleSettingUI', True)
        return

    def init_parameters(self):
        self.player = None
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if player:
            self.on_player_setted(player, False)
        else:
            emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)
        self._timer_graph = False
        self.cur_sel_ope_btn = None
        return

    def on_player_setted(self, player, is_emit=True):
        if is_emit:
            global_data.emgr.scene_player_setted_event -= self.on_player_setted
        self.player = player
        self.init_shot_test()
        self.init_test_event()
        self.init_add_item_panel()

    def init_event(self):
        self.init_parameters()

    def _init_menu(self):
        self.label_data = {BattleSettingUI.LABEL_SENSITY: {'menu': 'SensitySettingUI','text': '\xe7\x81\xb5\xe6\x95\x8f\xe5\xba\xa6\xe6\xb5\x8b\xe8\xaf\x95','path': 'logic.comsys.setting_ui'},BattleSettingUI.LABEL_OCC: {'menu': 'CullingTestUI','text': '\xe5\x8f\xaf\xe8\xa7\x81\xe6\x80\xa7\xe7\x83\x98\xe7\x84\x99\xe6\xb5\x8b\xe8\xaf\x95','path': 'logic.comsys.debug'},BattleSettingUI.LABEL_SHOT: {'node': 'nd_shoot','text': '\xe5\xb0\x84\xe5\x87\xbb\xe6\xb5\x8b\xe8\xaf\x95'},BattleSettingUI.LABEL_OTHER: {'node': 'nd_other','text': '\xe5\x85\xb6\xe4\xbb\x96\xe6\xb5\x8b\xe8\xaf\x95'},BattleSettingUI.LABEL_ADD_ITEM: {'node': 'nd_add_item','text': '\xe5\xa2\x9e\xe5\x8a\xa0\xe7\x89\xa9\xe5\x93\x81'},BattleSettingUI.LABEL_PROFILE: {'show_func': self.profile_show_func,'text': '\xe6\x80\xa7\xe8\x83\xbd\xe6\xb5\x8b\xe8\xaf\x95'},BattleSettingUI.LABEL_WWISE_PROFILE: {'show_func': self.wwise_profile_callback,'text': 'Wwise\xe6\xb5\x8b\xe8\xaf\x95'},BattleSettingUI.LABEL_VEHICLE_PROFILE: {'menu': 'VehicleTestUI','text': '\xe8\xbd\xbd\xe5\x85\xb7\xe5\x8f\x82\xe6\x95\xb0\xe6\xb5\x8b\xe8\xaf\x95','path': 'logic.comsys.debug'}}
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            self.label_data[BattleSettingUI.LABEL_GTRACE] = {'menu': 'GtraceSettingUI','text': 'Gtrace','path': 'logic.comsys.debug'}
        self.label_type = BattleSettingUI.LABEL_DEFAULT
        super(BattleSettingUI, self)._init()

    def profile_show_func(self):
        import world
        pp = world.get_active_scene().get_com('PartProfile')
        pp.create_ui()

    def wwise_profile_callback(self):
        global_data.sound_mgr.start_profiler()

    def init_shot_test(self):
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        show_time = player.get_owner().read_local_setting(ui_operation_const.ONE_SHOT_SHOW_KEY, ui_operation_const.ONE_SHOT_BTN_SHOW_TIME)
        show_time = float(show_time)
        self.one_shot_show_time = show_time
        min_show_time, max_show_time = ui_operation_const.ONE_SHOT_BTN_SHOW_TIME_RANGE

        def set_slider_appear_time_val(val):
            time_percent = (val - min_show_time) / (max_show_time - min_show_time)
            self.panel.slider_appear_time.slider.setPercent(time_percent * 100)
            self.panel.slider_appear_time.tf_value.SetString(str(val))

        set_slider_appear_time_val(show_time)

        @self.panel.slider_appear_time.slider.callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent() / 100.0 * (max_show_time - min_show_time) + min_show_time
            if not self._check_is_valid_one_shot_time(self.one_shot_attack_time, val):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(2151))
                set_slider_appear_time_val(self.one_shot_show_time)
                return
            self.one_shot_show_time = val
            self.write_setting(ui_operation_const.ONE_SHOT_SHOW_KEY, val)
            global_data.emgr.one_shot_change_appear_time_event.emit(val)
            self.panel.slider_appear_time.tf_value.setString(str(val))

        attack_time = player.get_owner().read_local_setting(ui_operation_const.ONE_SHOT_ATTACK_KEY, ui_operation_const.ONE_SHOT_BTN_ATTACK_INTERVAL)
        attack_time = float(attack_time)
        self.one_shot_attack_time = attack_time
        min_attack_time, max_attack_time = ui_operation_const.ONE_SHOT_BTN_ATTACK_TIME_RANGE

        def set_slider_attack_time_val(val):
            attack_percent = (val - min_attack_time) / (max_attack_time - min_attack_time)
            self.panel.slider_attack_time.slider.setPercent(attack_percent * 100)
            self.panel.slider_attack_time.tf_value.SetString(str(val))

        set_slider_attack_time_val(attack_time)

        @self.panel.slider_attack_time.slider.callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent() / 100.0 * (max_attack_time - min_attack_time) + min_attack_time
            if not self._check_is_valid_one_shot_time(val, self.one_shot_show_time):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(2151))
                set_slider_attack_time_val(self.one_shot_attack_time)
                return
            self.one_shot_attack_time = val
            self.write_setting(ui_operation_const.ONE_SHOT_ATTACK_KEY, val)
            global_data.emgr.one_shot_change_attack_time_event.emit(val)

        @self.panel.revert_attack_btn.callback()
        def OnClick(btn, touch):
            if not self._check_is_valid_one_shot_time(ui_operation_const.ONE_SHOT_BTN_ATTACK_INTERVAL, self.one_shot_show_time):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(2151))
                return
            self.one_shot_attack_time = ui_operation_const.ONE_SHOT_BTN_ATTACK_INTERVAL
            set_slider_attack_time_val(ui_operation_const.ONE_SHOT_BTN_ATTACK_INTERVAL)
            self.write_setting(ui_operation_const.ONE_SHOT_ATTACK_KEY, ui_operation_const.ONE_SHOT_BTN_ATTACK_INTERVAL)
            global_data.emgr.one_shot_change_attack_time_event.emit(ui_operation_const.ONE_SHOT_BTN_ATTACK_INTERVAL)

        @self.panel.revert_appear_btn.callback()
        def OnClick(btn, touch):
            if not self._check_is_valid_one_shot_time(self.one_shot_attack_time, ui_operation_const.ONE_SHOT_BTN_SHOW_TIME):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(2151))
                return
            self.one_shot_show_time = ui_operation_const.ONE_SHOT_BTN_SHOW_TIME
            set_slider_appear_time_val(ui_operation_const.ONE_SHOT_BTN_SHOW_TIME)
            self.write_setting(ui_operation_const.ONE_SHOT_SHOW_KEY, ui_operation_const.ONE_SHOT_BTN_SHOW_TIME)
            global_data.emgr.one_shot_change_appear_time_event.emit(ui_operation_const.ONE_SHOT_BTN_SHOW_TIME)

    def _check_is_valid_one_shot_time(self, attack_time, alive_time):
        if alive_time < attack_time:
            return False
        else:
            return True

    def _cal_percent(self, val, range):
        return (val - range[0]) / (range[1] - range[0])

    def init_test_event(self):

        @self.panel.revert_run_btn.callback()
        def OnClick(btn, touch):
            global_data.emgr.rocker_run_span_scale_event.emit(ui_operation_const.MR_DEF_RUN_SPAN_SCALE)
            self.panel.slider_run_scale.slider.setPercent(100 * self._cal_percent(ui_operation_const.MR_DEF_RUN_SPAN_SCALE, ui_operation_const.MR_SPAN_RANGE))
            self.panel.slider_run_scale.tf_value.setString(str(ui_operation_const.MR_DEF_RUN_SPAN_SCALE))

        @self.panel.revert_walk_btn.callback()
        def OnClick(btn, touch):
            global_data.emgr.rocker_walk_span_scale_event.emit(ui_operation_const.MR_DEF_WALK_SPAN_SCALE)
            self.panel.slider_run_scale.slider.setPercent(100 * self._cal_percent(ui_operation_const.MR_DEF_WALK_SPAN_SCALE, ui_operation_const.MR_SPAN_RANGE))
            self.panel.slider_run_scale.tf_value.setString(str(ui_operation_const.MR_DEF_WALK_SPAN_SCALE))

        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        run_scale = player.get_owner().read_local_setting(ui_operation_const.MR_RUN_KEY, ui_operation_const.MR_DEF_RUN_SPAN_SCALE)
        walk_scale = player.get_owner().read_local_setting(ui_operation_const.MR_WALK_KEY, ui_operation_const.MR_DEF_WALK_SPAN_SCALE)
        self._bind_rocker_scale_slider(self.panel.slider_run_scale.slider, run_scale, self.panel.slider_run_scale.tf_value, 'rocker_run_span_scale_event')
        self._bind_rocker_scale_slider(self.panel.slider_walk_scale.slider, walk_scale, self.panel.slider_walk_scale.tf_value, 'rocker_walk_span_scale_event')

        @self.panel.btn_plot.callback()
        def OnClick(btn, touch):
            self._timer_graph = not self._timer_graph
            import profiling
            import game3d
            w, h, _, _, _ = game3d.get_window_size()
            h_3 = int(h / 3)
            profiling.activate_timer_graph(self._timer_graph)
            profiling.set_timer_graph_area(10, h_3, h_3, h_3 * 2)

    def _bind_rocker_scale_slider(self, slider_node, val, val_tf, event_name):
        slider = slider_node
        val_tf.SetString(str(val))
        min_val, max_val = ui_operation_const.MR_SPAN_RANGE
        percent = self._cal_percent(val, ui_operation_const.MR_SPAN_RANGE)
        slider.setPercent(percent * 100)

        @slider.callback()
        def OnPercentageChanged(ctrl, sl):
            val = sl.getPercent() / 100.0 * (max_val - min_val) + min_val
            val_tf.SetString(str(val))
            global_data.emgr.fireEvent(event_name, val)

    def init_add_item_panel(self):
        normal_add_item_list = [
         (
          get_text_by_id(18170).format(num=1), 1002, 1),
         (
          get_text_by_id(18171).format(num=1), 1003, 1),
         (
          get_text_by_id(18172).format(num=30), 1620, 30),
         (
          get_text_by_id(18173).format(num=30), 1621, 30),
         (
          get_text_by_id(18174).format(num=30), 1622, 30),
         (
          get_text_by_id(18175).format(num=30), 1621, 30),
         (
          get_text_by_id(18176).format(num=30), 1623, 30),
         (
          get_text_by_id(18177).format(num=1), 1101, 1),
         (
          get_text_by_id(18178).format(num=1), 1102, 1),
         (
          get_text_by_id(18179).format(num=1), 1103, 1),
         (
          get_text_by_id(18180).format(num=1), 1614, 1),
         (
          get_text_by_id(18181).format(num=5), 1612, 5)]
        self.panel.lv_add_item.SetInitCount(len(normal_add_item_list))
        all_item = self.panel.lv_add_item.GetAllItem()
        for idx, ui_item in enumerate(all_item):
            ui_data = normal_add_item_list[idx]
            text, item_no, num = ui_data
            ui_item.btn_normal.SetText(text)

            @ui_item.btn_normal.unique_callback()
            def OnClick(btn, touch, item_no=item_no, num=num):
                if global_data.player:
                    global_data.player.wiz_command('create_item %d %d' % (item_no, num), True)

    def init_ope_check_btn(self, ui_item, ope_sel, ui_text):
        ui_item.lab_name.SetString(ui_text)
        ui_item.img_selected.setVisible(False)

        @ui_item.btn_selected.unique_callback()
        def OnClick(btn, touch, ui_item=ui_item):
            if self.player:
                global_data.emgr.posture_ope_ui_change_event.emit(ope_sel)
                self.sel_ope_ui_select(ui_item)

    def sel_ope_ui_select(self, ui_item):
        if self.cur_sel_ope_btn:
            self.cur_sel_ope_btn.img_selected.setVisible(False)
            self.cur_sel_ope_btn = None
        if ui_item:
            self.cur_sel_ope_btn = ui_item
            self.cur_sel_ope_btn.img_selected.setVisible(True)
        return

    def show_sst_figure(self):
        from logic.gcommon.common_const import ui_operation_const as uoc
        CAMERA_SST_KEYS = [uoc.SST_SCR_KEY, uoc.SST_AIM_RD_KEY, uoc.SST_AIM_2M_KEY,
         uoc.SST_AIM_4M_KEY, uoc.SST_FROCKER_KEY, uoc.SST_FS_ROCKER_KEY]
        CAMERA_SST_NAMES = ['\xe6\xbb\x91\xe5\xb1\x8f', '\xe7\xba\xa2\xe7\x82\xb9', '2\xe5\x80\x8d', '4\xe5\x80\x8d', '\xe5\xbc\x80\xe7\x81\xab\xe6\x91\x87\xe6\x9d\x86', '\xe8\x87\xaa\xe7\x94\xb1\xe8\xa7\x86\xe8\xa7\x92']
        if global_data.player:
            for idx, sst_key in enumerate(CAMERA_SST_KEYS):
                cur_list = global_data.player.get_setting(sst_key)
                print('\xe7\x81\xb5\xe6\x95\x8f\xe5\xba\xa6', CAMERA_SST_NAMES[idx], cur_list)

    def write_setting(self, key, val):
        if global_data.player:
            global_data.player.write_setting(key, val)