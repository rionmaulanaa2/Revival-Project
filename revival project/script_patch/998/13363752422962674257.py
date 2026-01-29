# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/CharacterCreatorUINew.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.text_utils import generate_random_name, preload_random_name_confs, unload_random_name_confs
from logic.comsys.common_ui.InputBox import InputBox
from common.const.uiconst import BG_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils.salog import SALog
from common.utils.timer import CLOCK
from logic.entities.CharacterSelect import CharacterSelect
from logic.gcommon.const import SEX_FEMALE, SEX_MALE

class CharacterCreatorUINew(BasePanel):
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'common/common_empty_container'
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    MOUSE_CURSOR_TRIGGER_SHOW = True
    DELAY_EXIT_TAG = 31415926

    def on_init_panel(self, **kwargs):
        preload_random_name_confs()
        self.hide_main_ui()
        self._input_box = None
        self._opt_from = kwargs.get('opt_from', 'error')
        self.init_sex()
        self._cnt_text = ''
        self._used_name_idx = 0
        self._used_us_name_idx = 0
        self._is_creating = False
        self._confirm = False
        self._over_timer = None
        self._tutorial_log_21 = False
        self._panel = None
        self._init_view()
        if 'no_finish' in kwargs:
            self.finish_mv_end()
        else:
            self.finish_mv()
        global_data.sound_mgr.play_ui_sound('enter_name')
        return

    def on_finalize_panel(self):
        unload_random_name_confs()
        super(CharacterCreatorUINew, self).on_finalize_panel()
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self.show_main_ui()
        global_data.emgr.on_used_name_updated_event -= self.on_used_name_update
        global_data.emgr.on_login_failed_event -= self.on_login_failed
        global_data.emgr.net_disconnect_event -= self.on_login_failed
        global_data.emgr.net_login_reconnect_event -= self.on_login_failed
        global_data.emgr.on_random_name_updated_event -= self.on_random_name_update
        self.clear_over_time()
        dlg = global_data.ui_mgr.get_ui('SecondConfirmDlg2')
        if dlg:
            dlg.close()
        return

    def _init_view(self):
        if self.selected_sex == SEX_FEMALE:
            template_name = 'guide/give_name_ningning'
        else:
            template_name = 'guide/give_name_rom'
        self._panel = global_data.uisystem.load_template_create(template_name, parent=self.panel)
        self._panel.RecordAnimationNodeState('button_show')
        self._panel.RecordAnimationNodeState('button_loop')
        self._panel.RecordAnimationNodeState('enter_loop')
        self.highlight_btn_create(False)

    def init_ui_event(self):
        if not self._panel:
            return
        self._panel.btn_sure.BindMethod('OnClick', self.on_click_btn_create)
        self._panel.btn_random.BindMethod('OnClick', self.on_click_btn_random)

    def highlight_btn_create(self, show):
        if show:
            self._panel.PlayAnimation('button_show')
            self._panel.PlayAnimation('button_loop')
        else:
            self._panel.StopAnimation('button_show')
            self._panel.RecoverAnimationNodeState('button_show')
            self._panel.StopAnimation('button_loop')
            self._panel.RecoverAnimationNodeState('button_loop')

    def init_sex(self):
        self.selected_sex = self.get_gender()

    def get_gender(self):
        from logic.gutils import qte_guide_utils
        role_id = qte_guide_utils.get_qte_chosen_role_id()
        if role_id is not None:
            if role_id == '11':
                return SEX_FEMALE
            else:
                return SEX_MALE

        else:
            return SEX_FEMALE
        return

    def finish_mv(self):
        self.finish_mv_end()

    def finish_mv_end(self):
        self._panel.PlayAnimation('show')
        self._panel.DelayCall(40.0 / 30.0, lambda : self.delay_init())

    def delay_init(self):
        self.init_widget()
        self.init_ui_event()
        self.init_event()
        self._panel.PlayAnimation('enter_loop')
        from logic.gutils.template_utils import show_account_find_dialog
        show_account_find_dialog()

    def on_input_callback(self, *_):
        if self._input_box.get_text() and self._confirm is False:
            self._confirm = True
            self.highlight_btn_create(True)
            return
        if not self._input_box.get_text() and self._confirm is True:
            self._confirm = False
            self.highlight_btn_create(False)
            return
        if self._input_box.get_text() and self._confirm is True:
            pass
        if self._tutorial_log_21 is False:
            salog_writer = SALog.get_instance()
            if salog_writer:
                salog_writer.write(SALog.TUTORIAL, 21)
            self._tutorial_log_21 = True

    def init_widget(self):
        if global_data.is_pc_mode:
            send_cb = self.on_click_btn_create
            detach_after_enter = False
        else:
            send_cb = self.on_input_callback
            detach_after_enter = None
        input_bar = self._get_input_bar_node()

        def start_input_cb():
            if self._panel:
                self._panel.StopAnimation('enter_loop')
                self._panel.RecoverAnimationNodeState('enter_loop')

        kw = {'max_length': 8,'cancel_callback': self.on_input_callback,
           'placeholder': input_bar.input_box.getPlaceHolder(),
           'send_callback': send_cb,
           'input_callback': self.on_input_callback,
           'start_input_cb': start_input_cb
           }
        if detach_after_enter:
            kw['detach_after_enter'] = detach_after_enter
        self._input_box = InputBox(input_bar, **kw)
        self._input_box.set_rise_widget(self.panel)
        self.generate_used_name()
        if global_data.owner_entity and isinstance(global_data.owner_entity, CharacterSelect):
            global_data.owner_entity.request_us_random_name(self.selected_sex)
        return

    def init_event(self):
        global_data.emgr.on_used_name_updated_event += self.on_used_name_update
        global_data.emgr.on_login_failed_event += self.on_login_failed
        global_data.emgr.net_disconnect_event += self.on_login_failed
        global_data.emgr.net_login_reconnect_event += self.on_login_failed
        global_data.emgr.on_random_name_updated_event += self.on_random_name_update

    def on_used_name_update(self):
        if not self._cnt_text:
            self._used_name_idx = 0
            self.generate_used_name()

    def on_random_name_update(self):
        if not self._cnt_text:
            self._used_us_name_idx = 0
            self.generate_random_name_by_us()

    def on_login_failed(self, *_, **kwargs):
        if self._is_creating:
            self.on_input_callback()
        self._is_creating = False
        self.clear_over_time()

    def generate_used_name(self):
        if not global_data.owner_entity:
            return False
        if not isinstance(global_data.owner_entity, CharacterSelect):
            return False
        name_list = global_data.owner_entity.name_list
        if not name_list:
            return False
        if self._used_name_idx >= len(name_list):
            return False
        name = name_list[self._used_name_idx]
        self._used_name_idx += 1
        self._input_box.set_text(name)
        self._cnt_text = name
        self.on_input_callback()
        return True

    def generate_random_name_by_us(self):
        if not global_data.owner_entity:
            return False
        if not isinstance(global_data.owner_entity, CharacterSelect):
            return False
        name_list = global_data.owner_entity.us_random_name_list
        if not name_list:
            return False
        if self._used_us_name_idx >= len(name_list):
            return False
        name = name_list[self._used_us_name_idx]
        self._used_us_name_idx += 1
        self._input_box.set_text(name)
        self._cnt_text = name
        self.on_input_callback()
        return True

    def on_click_btn_random(self, *_):
        if self.generate_used_name():
            return
        if self.generate_random_name_by_us():
            return
        name = generate_random_name(self.selected_sex + 1)
        self._input_box.set_text(name)
        self._cnt_text = name
        self.on_input_callback()

    def _get_input_bar_node(self):
        return self._panel.temp_input_box

    def on_click_btn_create(self, *_):
        if self._is_creating:
            return
        self._cnt_text = self._get_input_bar_node().input_box.getString()
        if not self._cnt_text:
            self._panel.PlayAnimation('warning')
            return
        if self._panel.IsPlayingAnimation('exit'):
            return
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        if not ui_utils.check_nick_name(self._cnt_text):
            return
        delay = self._panel.GetAnimationMaxRunTime('exit')
        self._panel.PlayAnimation('exit')
        self._panel.DelayCallWithTag(delay, lambda : self._do_create(), self.DELAY_EXIT_TAG)

    def _do_create(self):
        if global_data.owner_entity is None or not isinstance(global_data.owner_entity, CharacterSelect):
            salog_writer = SALog.get_instance()
            if salog_writer:
                salog_writer.write(SALog.TUTORIAL, 'error_{}'.format(self._opt_from))
            import logic.gutils.ConnectHelper as cnhp
            ins = cnhp.ConnectHelper()
            if ins.is_connected():
                ins.disconnect()
            return
        else:
            self._is_creating = True
            from logic.comsys.guide_ui.GuideSetting import GuideSetting
            from logic.gcommon.common_const.guide_const import COMBAT_JUNIOR
            local_battle_data = GuideSetting().local_battle_data
            level = local_battle_data.get('_lbs_combat_level', COMBAT_JUNIOR)
            global_data.owner_entity.create_character(self._cnt_text, self.selected_sex, level)
            GuideSetting()._create_login = True
            salog_writer = SALog.get_instance()
            if salog_writer:
                salog_writer.write(SALog.TUTORIAL, 22)
            self._over_timer = global_data.game_mgr.register_logic_timer(self.create_over_time, interval=3, mode=CLOCK)
            return

    def create_over_time(self):
        self.clear_over_time()
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        dlg = SecondConfirmDlg2()

        def on_confirm():
            dlg.close()
            import logic.gutils.ConnectHelper as cnhp
            ins = cnhp.ConnectHelper()
            if ins.is_connected():
                ins.disconnect()

        dlg.confirm(content=get_text_local_content(195), confirm_callback=on_confirm, cancel_callback=on_confirm, unique_callback=on_confirm)

    def clear_over_time(self):
        if self._over_timer:
            global_data.game_mgr.unregister_logic_timer(self._over_timer)
            self._over_timer = None
        return

    def on_resolution_changed(self):
        if self._panel:
            self._panel.PlayAnimation('show')
            self._panel.StopAnimation('show', finish_ani=True)