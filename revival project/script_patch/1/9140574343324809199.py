# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/MainSettingUI.py
from __future__ import absolute_import
import game3d
import six
from six.moves import range
import ccui
from logic.gutils import red_point_utils
import render
import version
import six.moves.builtins
import device_compatibility
import logic.gcommon.time_utility as time_utils
from logic.client.const import game_mode_const
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg3
from logic.comsys.common_ui.WindowCommonComponent import WindowCommonComponent
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI
from common.cfg import confmgr
from common.const import uiconst
from common.platform.dctool import interface
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from common.utils import package_type
from logic.gcommon.common_const import lang_data
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import PRIVILEGE_LEVEL_TO_SETTING, PRIVILEGE_SETTING_TO_RED_POINT
from logic.gcommon.common_const import activity_const
from logic.gutils.activity_utils import is_activity_finished
from logic.gcommon.common_const.custom_battle_const import CUSTOM_SETTING_BATTLE_CHECK_TITLE
from logic.gutils.pve_utils import is_pve_multi_player_team
TAB_TEMPLATE_MAP = {'BaseSettingWidget': 'setting/setting_tab_1',
   'AdvancedSettingWidget': 'setting/setting_tab_1_1',
   'SensitivitySettingWidget': 'setting/setting_tab_2',
   'MechaSensitivitySettingWidget': 'setting/setting_tab_2_1',
   'MouseKeyboardSettingWidget': 'setting/setting_tab_pc_custom',
   'OperationSettingWidget': 'setting/setting_tab_3',
   'VehicleSettingWidget': 'setting/setting_tab_4',
   'QualitySettingWidget': 'setting/setting_tab_5',
   'SoundSettingWidget': 'setting/setting_tab_6',
   'BusiniessLawSettingWidget': 'setting/setting_tab_7',
   'HighLightSettingWidget': 'setting/setting_tab_8',
   'CustomBattleSettingInfoWidget': 'room/i_room_custom_setting',
   'MechaSettingWidget': 'setting/setting_tab_1_2',
   'ParentCareSettingWidget': 'setting/i_setting_pa_minor',
   'PrivacySettingWidget': 'setting/setting_tab_10'
   }
SH_IN_NON_BATTLE = 0
SH_IN_BATTLE = 1
SHOW_SLIDER_MIN_LEN = 25

class MainSettingUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    MOUSE_CURSOR_TRIGGER_SHOW = True
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'update_death_come_home_time': 'refresh_btn_come_home',
       'enable_battle_surrender': 'refresh_btn_surrender',
       'left_ten_second_event': 'update_function_buttons',
       'update_setting_btn_red_point': 'update_setting_red_point',
       'lobby_bgm_change_success': 'refresh_lobby_bgm',
       'refresh_item_red_point': 'update_setting_red_point'
       }

    def get_version_content(self):
        try:
            c_package = 'na' if six.moves.builtins.__dict__.get('G_IS_NA_PROJECT', False) else 'cn'
            c_engine_ver = version.get_engine_svn()
            c_script_ver = version.get_script_version()
            c_server_ver = version.get_server_version()
            s_game = global_data.connect_helper.get_reconnect_game().replace('game_', '')
            s_server_ver = global_data.player.server_ver if global_data.player else -1
            s_game_ver = global_data.player.game_ver if global_data.player else -1
            version_content = '%s-%s-%s-%s | %s-%s-%s-%s' % (c_package, c_engine_ver, c_script_ver, c_server_ver, interface.get_server_name(), s_game, s_game_ver, s_server_ver)
            if global_data.battle and global_data.battle.server_name:
                s_battle = global_data.battle.server_name.replace('battle_', '')
                s_battle_ver = global_data.battle.game_ver
                version_content = '%s | %s-%s' % (version_content, s_battle, s_battle_ver)
            is_release = version.get_tag() == 'release'
            if package_type.is_inner_package() or not is_release:
                from common.utils.time_utils import get_timezone
                version_content += ' | %s' % get_timezone()
        except:
            version_content = ''

        return version_content

    def _update_sub_tabs(self, main_idx, sub_pages_conf):
        if not sub_pages_conf:
            self.panel.nd_tab.setVisible(False)
            return
        else:
            self.panel.nd_tab.setVisible(True)
            cnt = len(sub_pages_conf)
            self.panel.list_tab.SetInitCount(cnt)
            self.panel.img_underline.ResizeAndPositionSelf()
            cur_sub_idx = self._get_cur_sub_idx(main_idx)
            for i in range(cnt):
                conf = sub_pages_conf[i]
                text_id = conf.get('tab_text_id', None)
                item = self.panel.list_tab.GetItem(i)
                if text_id is None:
                    item.setVisible(False)
                    continue
                item.setVisible(True)
                sel = i == cur_sub_idx
                item.btn_tab.SetSelect(sel)
                if sel:
                    anim = 'click'
                else:
                    anim = 'unclick'
                item.PlayAnimation(anim)
                item.btn_tab.SetText(text_id)

                @item.btn_tab.unique_callback()
                def OnClick(btn, touch, _main_idx=main_idx, _sub_idx=i):
                    return self._on_sub_tab_selected(_main_idx, _sub_idx)

            return

    def _on_sub_tab_selected(self, main_idx, sub_idx):
        sub_page_confs = self._get_sub_pages_conf(main_idx)
        if not (sub_idx >= 0 and sub_idx < len(sub_page_confs)):
            return
        else:
            page_conf = sub_page_confs[sub_idx]
            prev_page = self._get_cur_page()
            page = self._get_sub_page(main_idx, sub_idx)
            if page is None:
                cls_name = page_conf.get('widget')
                tab_text_id = page_conf.get('tab_text_id')
                if cls_name not in TAB_TEMPLATE_MAP:
                    return
                page = self._new_setting_widget(cls_name, tab_text_id)
                if main_idx not in self.page_list:
                    self.page_list[main_idx] = {}
                self.page_list[main_idx][sub_idx] = page
            self._sub_page_cur_indices[main_idx] = sub_idx
            cnt = self.panel.list_tab.GetItemCount()
            for i in range(cnt):
                item = self.panel.list_tab.GetItem(i)
                sel = sub_idx == i
                item.btn_tab.SetSelect(sel)
                if sel:
                    anim = 'click'
                else:
                    anim = 'unclick'
                item.PlayAnimation(anim)

            if prev_page:
                prev_page.on_exit_page()
            self._on_setting_widget_selected(page)
            return

    def on_resolution_changed(self):
        self.clear_show_count_dict()
        if self.page_list:
            for index, pages in six.iteritems(self.page_list):
                for main_idx in pages:
                    page_wrapper = pages[main_idx]
                    print page_wrapper
                    page_wrapper.on_resolution_changed()

    def on_init_panel(self, init_tab_widget_classname=None):
        self.cur_btn = {}
        self.tab_common_component = WindowCommonComponent(self.panel.content_bar)
        self.tab_common_component.init_common_panel(None, self.on_click_close_btn)
        if global_data.reshow_settings_after_reload:
            init_tab_widget_classname = 'QualitySettingWidget'
            global_data.reshow_settings_after_reload = False
        tab_text_id_list = []
        tab_text_id_list.extend(({'text_id': 606306}, {'text_id': 2267}, {'text_id': 2298}, {'text_id': 82281}, {'text_id': 2008}))
        if global_data.is_pc_mode:
            tab_text_id_list.extend(({'text_id': 920730},))
        if not global_data.is_pc_mode:
            tab_text_id_list.extend(({'text_id': 2009},))
        tab_text_id_list.extend(({'text_id': 2010}, {'text_id': 2020}, {'text_id': 2202}))
        self.page_conf_list = []
        self.page_conf_list.extend(({'widget': 'AdvancedSettingWidget'}, {'widget': 'MechaSettingWidget'}, {'widget': 'BaseSettingWidget'}, {'widget': 'PrivacySettingWidget'}, ({'widget': 'SensitivitySettingWidget','tab_text_id': 920731}, {'widget': 'MechaSensitivitySettingWidget','tab_text_id': 28000})))
        if global_data.is_pc_mode:
            self.page_conf_list.extend(({'widget': 'MouseKeyboardSettingWidget'},))
        if not global_data.is_pc_mode:
            self.page_conf_list.extend(({'widget': 'OperationSettingWidget'},))
        self.page_conf_list.extend(({'widget': 'VehicleSettingWidget'}, {'widget': 'QualitySettingWidget'}, {'widget': 'SoundSettingWidget'}))
        self._mouse_keyboard_setting_idx = self._get_widget_main_idx('MouseKeyboardSettingWidget')
        self.tab_red_point_func = {'QualitySettingWidget': self.check_quality_red_point,
           'PrivacySettingWidget': self.check_privilege_setting_red_point,
           'SoundSettingWidget': self.check_sound_setting_red_point
           }
        if get_cur_lang_name() == lang_data.code_2_shorthand.get(lang_data.LANG_JA, 'jp'):
            tab_text_id_list.append({'text_id': 2231})
            self.page_conf_list.append({'widget': 'BusiniessLawSettingWidget'})
        from logic.comsys.video.video_record_utils import is_high_light_support
        in_battle = not global_data.player or global_data.player.is_in_battle()
        if is_high_light_support() and not in_battle:
            tab_text_id_list.append({'text_id': 2254})
            self.page_conf_list.append({'widget': 'HighLightSettingWidget'})
            self.tab_red_point_func['HighLightSettingWidget'] = self._check_high_light_red_point
        if global_data.battle and global_data.battle.is_customed_battle():
            tab_text_id_list.append({'text_id': CUSTOM_SETTING_BATTLE_CHECK_TITLE})
            self.page_conf_list.append({'widget': 'CustomBattleSettingInfoWidget'})

            def check_red_point():
                return False

            self.tab_red_point_func['CustomBattleSettingInfoWidget'] = check_red_point
        if global_data.channel and global_data.channel.get_name() in ('netease', ''):
            tab_text_id_list.append({'text_id': 635265})
            self.page_conf_list.append({'widget': 'ParentCareSettingWidget'})
        self._btn_exit_text_id = None
        self.page_list = {}
        self._sub_page_cur_indices = {}
        self.tab_common_component.init_tab_list(tab_text_id_list, self.on_tab_selected, before_tab_selected_func=self._before_tab_selected_func)
        self._cur_index = None
        self.panel.btn_apply_pc.setVisible(True)
        self.panel.btn_apply_pc.SetInitCount(1)
        self._apply_btn = self.panel.btn_apply_pc.GetItem(0).btn
        self._apply_btn.SetText(19529)

        @self._apply_btn.unique_callback()
        def OnClick(btn, touch):
            page = self._get_cur_page()
            if page:
                on_apply = getattr(page, 'on_apply')
                if callable(on_apply):
                    page.on_apply()

        def OnScrollEvent(scrollview, event):
            content_bar = self.panel.content_bar
            if event == ccui.SCROLLVIEW_EVENT_SCROLLING:
                content_bar.img_tips_up.setVisible(True)
                content_bar.img_tips_down.setVisible(True)
            elif event == ccui.SCROLLVIEW_EVENT_SCROLL_TO_TOP:
                content_bar.img_tips_up.setVisible(False)
                content_bar.img_tips_down.setVisible(True)
            elif event == ccui.SCROLLVIEW_EVENT_SCROLL_TO_BOTTOM:
                content_bar.img_tips_down.setVisible(False)
                content_bar.img_tips_up.setVisible(True)

        self.panel.content_bar.list_tab.addEventListener(OnScrollEvent)
        self._is_account_btn_as_guest_bind = self._check_is_account_btn_as_guest_bind()
        self._is_account_btn_as_logout = self._check_is_account_btn_as_logout()
        version_content = self.get_version_content()
        self.panel.lab_version.SetString(version_content)
        self.new_weapon_bar_ope_sel = None
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)
        self.panel.nd_scroll_pc.setVisible(global_data.is_pc_mode)
        self.ref_btn_exit = None
        self.refresh_tab_red_point()
        self.init_widget(init_tab_widget_classname)
        self.fb_item = None
        global_data.emgr.main_setting_ui_open_event.emit()
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_GUIDE_OPEN_MAIN_SETTING', self)
            logic.send_event('E_OPEN_MAIN_SETTING', self)
        self.register_mouse_scroll_event()
        self.init_custom_btns()
        self.init_privacy_btns()
        return

    def _get_sub_pages_conf(self, main_idx):
        if main_idx >= len(self.page_conf_list) or main_idx < 0:
            return []
        else:
            confs = self.page_conf_list[main_idx]
            if isinstance(confs, tuple) or isinstance(confs, list):
                ret = []
                for conf in confs:
                    if 'available_plats' in conf:
                        plats = conf['available_plats']
                        if global_data.is_pc_mode:
                            target_str = 'pc'
                        else:
                            target_str = 'mobile'
                        if target_str not in plats:
                            continue
                    ret.append(conf)

                return ret
            return []

    def _get_cur_page(self):
        return self._get_page(self._cur_index)

    def _get_page(self, main_idx):
        cur_sub_idx = self._get_cur_sub_idx(main_idx)
        return self._get_sub_page(main_idx, cur_sub_idx)

    def _get_sub_page(self, main_idx, sub_idx):
        if sub_idx == -1:
            return
        else:
            pages = self.page_list.get(main_idx, None)
            return pages.get(sub_idx, None)
            return

    def _get_cur_sub_idx(self, main_idx):
        return self._sub_page_cur_indices.get(main_idx, -1)

    def do_hide_panel(self):
        super(MainSettingUI, self).do_hide_panel()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)

    def do_show_panel(self):
        super(MainSettingUI, self).do_show_panel()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def on_finalize_panel(self):
        if self.tab_common_component:
            self.tab_common_component.destroy()
            self.tab_common_component = None
        if self.page_list:
            for index, pages in six.iteritems(self.page_list):
                for main_idx in pages:
                    page_wrapper = pages[main_idx]
                    page_wrapper.destroy()

        self.page_list = {}
        self._sub_page_cur_indices.clear()
        self.tab_red_point_func = {}
        self.fb_item = None
        global_data.ui_mgr.close_ui('BattleCustomButtonUI')
        global_data.ui_mgr.close_ui('LanguageSettingUI')
        global_data.ui_mgr.close_ui('NormalConfirmUI')
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)
        if not global_data.player:
            return
        else:
            if self.new_weapon_bar_ope_sel is not None:
                global_data.emgr.weapon_bar_ui_ope_change_event.emit(self.new_weapon_bar_ope_sel)
            global_data.player.save_settings_to_file()
            self.ref_btn_exit = None
            logic = global_data.player.logic
            if logic:
                logic.send_event('E_GUIDE_CLOSE_MAIN_SETTING')
            if not global_data.player.is_in_battle():
                self.on_click_update_btn_without_jump()
            return

    def init_widget(self, init_tab_widget_classname=None):
        if self.tab_common_component:
            idx = 0
            init_tab_idx = self._get_widget_main_idx(init_tab_widget_classname)
            if init_tab_idx != -1:
                idx = init_tab_idx
            if idx != self._cur_index:
                self.tab_common_component.on_jump_to_index(idx)

    def on_fb_bind_success_func(self):
        if self.fb_item:
            self.fb_item.lab.SetString(get_text_by_id(81024))
            self.fb_item.img_bind.setVisible(True)
            self.fb_item.img_reward.setVisible(False)

    def on_click_close_btn(self, *args, **kwargs):
        self.close()

    def close(self):
        if self._cur_index is not None:
            self.on_close_tab(self._cur_index)
        super(MainSettingUI, self).close()
        return

    def on_close_tab(self, index):
        self.on_tab_selected(None)
        return

    def _before_tab_selected_func(self, index, resume_cb):
        if self._cur_index == self._mouse_keyboard_setting_idx:
            widget = self._get_page(self._mouse_keyboard_setting_idx)
            if widget is None:
                return True
            else:
                from logic.comsys.setting_ui.SettingWidget.MouseKeyboardSettingWidget import MouseKeyboardSettingWidget
                if isinstance(widget, MouseKeyboardSettingWidget) and widget.have_pending_key_bindings():
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                    SecondConfirmDlg2().confirm(content=get_text_by_id(920742), confirm_callback=resume_cb)
                    return False
                return True

        else:
            return True
        return

    def jump_to_tab(self, index):
        self.tab_common_component.jump_to_index(index)

    def jump_to_switch_lobby_music(self, music_idx=None):
        idx = self._get_widget_main_idx('SoundSettingWidget')
        if idx < 0:
            return
        self.jump_to_tab(idx)
        page = self._get_page(idx)
        page.jump_to_switch_lobby_music(music_idx)

    def jump_to_underage_mode(self):
        idx = self._get_widget_main_idx('BaseSettingWidget')
        if idx < 0:
            return
        self.jump_to_tab(idx)
        page = self._get_page(idx)
        page.jump_to_underage_mode()

    def on_tab_selected(self, index):
        page = self._get_cur_page()
        if page:
            page.on_exit_page()
        last_index = self._cur_index
        if index is None or index >= len(self.page_conf_list) or index >= len(TAB_TEMPLATE_MAP):
            page_conf = None
        else:
            page_conf = self.page_conf_list[index]
        new_page = self._get_page(index)
        if new_page is not None:
            self._on_setting_widget_selected(new_page)
        else:
            if page_conf is None:
                self._cur_index = index
                return
            if isinstance(page_conf, tuple) or isinstance(page_conf, list):
                page_confs = page_conf
            else:
                page_confs = (
                 page_conf,)
            cur_sub_idx = self._get_cur_sub_idx(index)
            if cur_sub_idx == -1:
                new_sub_idx = 0
            else:
                new_sub_idx = cur_sub_idx
            if new_sub_idx < 0 or new_sub_idx >= len(page_confs):
                page_conf = None
            else:
                page_conf = page_confs[new_sub_idx]
            if page_conf is None:
                self._cur_index = index
                return
            cls_name = page_conf.get('widget')
            tab_text_id = page_conf.get('tab_text_id')
            if cls_name not in TAB_TEMPLATE_MAP:
                self._cur_index = index
                return
            page = self._new_setting_widget(cls_name, tab_text_id)
            if index not in self.page_list:
                self.page_list[index] = {}
            self.page_list[index][new_sub_idx] = page
            self._sub_page_cur_indices[index] = new_sub_idx
            self._on_setting_widget_selected(page)
        self._cur_index = index
        self._update_sub_tabs(index, self._get_sub_pages_conf(index))
        self.check_tab_red_point(last_index, self._cur_index)
        return

    def _on_setting_widget_selected(self, page):
        page_panel = page.get_page_panel()
        if page_panel:
            self.panel.content_bar.page.SetContainer(page_panel)
            self.panel.content_bar.page.ScrollToTop()
            self.adjust_container_pos()
            if global_data.is_pc_mode:
                self.init_pc_scroll_bar()
        page.on_enter_page()
        self.update_function_buttons(page)
        self.refresh_sync_server_btn_enable(page)

    def _new_setting_widget(self, cls_name, tab_text_id=None):
        mod = __import__('logic.comsys.setting_ui.SettingWidget.%s' % cls_name, globals(), locals(), [cls_name])
        cls = getattr(mod, cls_name, None)
        template = TAB_TEMPLATE_MAP[cls_name]
        page_panel = global_data.uisystem.load_template_create(template, None)
        page = cls(page_panel, self)
        if tab_text_id is not None:
            page.set_tab_text_id(tab_text_id)
        page.on_init_panel()
        return page

    def set_apply_btn_enabled(self, enabled):
        self._apply_btn.SetEnable(enabled)

    def adjust_container_pos(self):
        container = self.panel.content_bar.page.GetContainer()
        view_size = self.panel.content_bar.page.GetContentSize()
        inner_size = container.getContentSize()
        container = self.panel.content_bar.page.GetContainer()
        if view_size[1] > inner_size.height:
            container = self.panel.content_bar.page.GetContainer()
            container.SetPosition(container.getPosition().x, view_size[1] - inner_size.height)

    def keep_unchanged_view_target(self, change_func, offset=0):
        container = self.panel.content_bar.page.GetContainer()
        view_size = self.panel.content_bar.page.GetContentSize()
        curr_page_offset = self.panel.content_bar.page.GetContentOffset()
        inner_size = container.getContentSize()
        if change_func:
            change_func()
        new_inner_size = container.getContentSize()
        self.panel.content_bar.page.setInnerContainerSize(new_inner_size)
        height_change_val = new_inner_size.height - inner_size.height
        curr_page_offset.y -= height_change_val
        curr_page_offset.y -= offset
        self.panel.content_bar.page.SetContentOffsetInDuration(curr_page_offset, bound_check=True)

    def _get_widget_main_idx(self, widget_class_name):
        if widget_class_name is None:
            return -1
        else:
            idx = -1
            for idx, ele in enumerate(self.page_conf_list):
                if isinstance(ele, tuple) or isinstance(ele, list):
                    eles = ele[:]
                else:
                    eles = (
                     ele,)
                for e in eles:
                    if e.get('widget') == widget_class_name:
                        return idx

            return -1

    def on_click_account_btn(self, *args):
        if self._is_account_btn_as_guest_bind:
            global_data.channel.guest_bind()
        elif self._is_account_btn_as_logout:
            global_data.channel.logout()
        else:
            global_data.channel.open_manager()
            if global_data.channel.get_name() == 'netease':
                sdk_uid = global_data.channel.get_sdk_uid()
                if sdk_uid:
                    global_data.achi_mgr.save_netease_daren_red_point(sdk_uid, 0)

    def on_click_sw_account_btn(self, *args):
        global_data.channel.switch_account()

    def check_show_red_point(self, ui_item):
        if global_data.channel.get_name() != 'netease':
            return False
        else:
            skd_uid = global_data.channel.get_sdk_uid()
            if not skd_uid:
                return False
            if global_data.achi_mgr.is_show_netease_daren_red_point(skd_uid):
                return True
            return False

    def check_show_update_red_point(self, ui_item):
        if not global_data.player:
            return
        has_remote_new_package = global_data.player.has_remote_new_package()
        cur_remote_version = global_data.player.get_cur_remote_version()
        showed_remote_version = global_data.achi_mgr.get_cur_user_archive_data('main_setting_btn_update', default=0)
        show_red_point = cur_remote_version > showed_remote_version and has_remote_new_package
        ui_item and ui_item.red_dot.setVisible(show_red_point)
        try:
            activity_id = getattr(activity_const, 'ACTIVITY_UPDATE_HOLDPACKAGE')
            if not activity_id:
                return
            conf = confmgr.get('c_activity_config', activity_id, default={})
            if not conf:
                return
            if is_activity_finished(activity_id):
                return
            task_id = conf.get('cTask')
            if not task_id:
                return
            if global_data.player.has_receive_reward(task_id):
                return
            ui_item and ui_item.temp_tips.setVisible(show_red_point)
            ui_item and ui_item.temp_tips.PlayAnimation('show')
        except:
            log_error('check_show_update_red_point reward_tip error')

    def on_click_lang_btn(self, btn, touch):
        from logic.comsys.setting_ui.LanguageSettingUI import LanguageSettingUI
        LanguageSettingUI()

    def on_click_feedback_btn(self, btn, touch):
        from logic.comsys.feedback import echoes
        if global_data.player and global_data.player.is_in_battle():
            echoes.show_feedback_view(echoes.BATTLE)
        else:
            echoes.show_feedback_view(echoes.LOBBY)

    def on_click_new_feedback_btn(self, *args):
        global_data.ui_mgr.show_ui('GameFeedbackUI', 'logic.comsys.setting_ui')

    def on_click_exit_game_btn(self, btn, touch):
        from logic.manager_agents.EscapeManagerAgent import EscapeManagerAgent
        EscapeManagerAgent.show_exit_game_confirm_dialog()

    def on_click_update_btn(self, *args):
        import game3d
        self.on_click_update_btn_without_jump()
        game3d.open_url('https://adl.netease.com/d/g/ace/c/gw')

    def on_click_update_btn_without_jump(self):
        import game3d
        if not global_data.channel.get_name() == 'netease':
            return
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            return
        if not global_data.player:
            return
        cur_remote_version = global_data.player.get_cur_remote_version()
        global_data.achi_mgr.set_cur_user_archive_data('main_setting_btn_update', cur_remote_version)

    def on_click_help_btn(self, *args):
        self.open_help()

    def open_help(self):
        import game3d
        if hasattr(game3d, 'open_gm_web_view'):
            global_data.player.get_custom_service_token()
            game3d.open_gm_web_view('')
        else:
            data = {'methodId': 'ntOpenGMPage',
               'refer': ''
               }
            global_data.channel.extend_func_by_dict(data)

    def on_click_bind_btn(self, *args):
        pass

    def on_click_gift_btn(self, *args):
        from logic.comsys.lobby.CDKeyGiftUI import CDKeyGiftUI
        CDKeyGiftUI()

    def on_click_sprite_btn(self, *args):
        if global_data.player:
            data = {'methodId': 'ntOpenGMPage','refer': '/sprite/index'
               }
            global_data.channel.extend_func_by_dict(data)

    def _check_is_account_btn_as_guest_bind(self):
        return global_data.channel.get_name() == 'huawei'

    def _check_is_account_btn_as_logout(self):
        s = {
         'fanyou', 'kuchang', 'juefeng'}
        return global_data.channel.get_name() in s

    def on_bind_email(self):
        from logic.comsys.activity.EmailBindUI import EmailBindUI
        from logic.comsys.activity.EmailUnBindUI import EmailUnBindUI
        cur_email = global_data.player.get_cur_bind_email()
        if cur_email is None or cur_email == '':
            EmailBindUI(self.panel)
        else:
            EmailUnBindUI(self.panel, cur_email)
        return

    def on_bind_mobile(self):
        from logic.gcommon.common_const.activity_const import ACTIVITY_BIND_MOBILE
        from logic.comsys.activity.PhoneBindUI import PhoneBindUI
        from logic.comsys.activity.PhoneUnBindUI import PhoneUnBindUI
        global_data.player.read_activity_list(ACTIVITY_BIND_MOBILE)
        cur_phone = global_data.player.get_cur_bind_phone()
        if global_data.player.has_activity(ACTIVITY_BIND_MOBILE):
            PhoneBindUI(self.panel, cur_phone)
        elif cur_phone is None or cur_phone == '':
            PhoneBindUI(self.panel)
        else:
            PhoneUnBindUI(self.panel, cur_phone)
        return

    def init_bind_btn(self, ui_item):
        ui_item.lab.SetString(get_text_by_id(80047))

    def btn_language_check(self):
        return not interface.is_mainland_package()

    def btn_account_show_check(self):
        if self._is_account_btn_as_guest_bind:
            return not global_data.channel.is_guest_blocked()
        else:
            if self._is_account_btn_as_logout:
                return True
            return global_data.channel.has_builtin_user_center()

    def btn_sw_account_show_check(self):
        return global_data.channel.has_standalone_sw_user()

    def btn_help_show_check(self):
        import game3d
        if interface.is_mainland_package():
            return False
        if game3d.get_app_name() == 'com.netease.g93natw':
            return False
        if global_data.is_google_pc:
            return False
        return True

    def btn_bind_show_check(self):
        return False

    def btn_update_show_check(self):
        if not global_data.player:
            return False
        return global_data.player.has_remote_new_package()

    def btn_feedback_new_check(self):
        from common.platform.dctool import interface
        return interface.is_mainland_package()

    def btn_feedback_check(self):
        from common.platform.dctool import interface
        if interface.is_mainland_package():
            return False
        in_battle = global_data.player.is_in_battle()
        if global_data.channel and global_data.channel.is_china_server() and not in_battle:
            return False
        return True

    def btn_exit_game_show_check(self):
        return global_data.is_pc_mode

    def btn_bind_fb_show_check(self):
        return False

    def btn_gift_show_check(self):
        if not global_data.player:
            return False
        return global_data.player.has_enable_cdkey_gift()

    def btn_sprite_show_check(self):
        if G_IS_NA_USER:
            return False
        app_channel = global_data.channel.get_app_channel()
        if app_channel in frozenset(['oppo', 'huawei']):
            return False
        return True

    def get_upgrade_package_visible(self, in_battle, index):
        if in_battle or index != 4:
            return False
        package_quality = device_compatibility.get_package_quality()
        support_astc = render.is_android_support_astc()
        return support_astc and package_quality != device_compatibility.PACKAGE_QUALITY_HIGH_END

    def btn_sync_server_show_check(self):
        return global_data.is_pc_mode

    def btn_upgrade_show_check(self):
        if not global_data.player:
            return False
        in_battle = global_data.player.is_in_battle()
        return self.get_upgrade_package_visible(in_battle, self._cur_index)

    def btn_agreement_show_check(self):
        return interface.is_mainland_package()

    def on_click_agreement_btn(self, *args):
        from common.platform.channel import Channel
        Channel().show_compact_view()

    def on_click_bind_fb_btn(self, *args):
        if global_data.channel.is_bind_facebook():
            global_data.game_mgr.show_tip(get_text_by_id(81024))
        else:
            global_data.channel.bind_facebook()

    def init_bind_fb_btn(self, ui_item):
        self.fb_item = ui_item
        if global_data.channel.is_bind_facebook():
            ui_item.lab.SetString(get_text_by_id(81024))
            ui_item.img_bind.setVisible(True)
        else:
            ui_item.lab.SetString(get_text_by_id(81046))
            ui_item.img_reward.setVisible(True)

    def on_announce(self, *args):
        ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
        if ui:
            ui.request_platform_announce()

    def init_custom_btns(self):
        func_list = [self.on_click_custom_btn, self.on_click_pve_custom_btn]
        text_list = [606304, 18901]
        self.panel.list_custom.SetInitCount(len(func_list))
        for idx, func in enumerate(func_list):
            ui_item = self.panel.list_custom.GetItem(idx)
            if ui_item:
                btn_common = ui_item.btn_common
                btn_common.SetText(text_list[idx])
                btn_common.BindMethod('OnClick', func)

    def init_privacy_btns(self):
        privacy_btn_dict = {634648: {'func': self.on_click_collected_personal_info_btn,'check_func': self.check_show_collected_personal_info},634649: {'func': self.on_click_third_party_shared_personal_info,'check_func': self.check_show_collected_personal_info},634647: {'func': self.on_click_privacy_policy,'check_func': self.check_show_collected_personal_info}}
        for text_id, func_dict in six.iteritems(privacy_btn_dict):
            check_func = func_dict.get('check_func')
            if check_func and callable(check_func) and check_func():
                ui_item = self.panel.list_btn_privacy.AddTemplateItem()
                btn_common = ui_item.btn_common
                btn_common.SetText(text_id)
                func = func_dict.get('func')
                if func and callable(func):
                    btn_common.BindMethod('OnClick', func)

    def on_click_custom_btn(self, *args):
        if not global_data.player:
            return
        else:
            from logic.comsys.setting_ui.BattleCustomButtonUI import BattleCustomButtonUI
            BattleCustomButtonUI(None, 'human')
            return

    def on_click_mecha_custom_btn(self, btn, touch):
        if not global_data.player:
            return
        else:
            from logic.comsys.setting_ui.BattleCustomButtonUI import BattleCustomButtonUI
            BattleCustomButtonUI(None, 'mecha', mecha_only=True)
            return

    def on_click_pve_custom_btn(self, *args):
        if not global_data.player:
            return
        else:
            from logic.comsys.setting_ui.PVEBattleCustomButtonUI import PVEBattleCustomButtonUI
            PVEBattleCustomButtonUI(None, 'pve', mecha_only=True)
            return

    def on_click_upgrade_package(self, *args):
        import package_utils
        package_utils.reset_package_info()
        npk_size = device_compatibility.get_high_end_package_size() * 1.0 / 1048576.0
        txt_content = get_text_by_id(90058).format(npk_size)

        def on_confirm(*args):
            device_compatibility.set_package_info_quality(device_compatibility.PACKAGE_QUALITY_HIGH_END)
            import game3d
            game3d.exit()

        def on_cancel(*args):
            pass

        SecondConfirmDlg2().confirm(content=txt_content, cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=lambda *args: None)

    def on_click_exit_btn(self, *args):
        from logic.gutils.judge_utils import is_ob, is_in_competition_battle
        if is_in_competition_battle():
            if not is_ob():
                global_data.game_mgr.show_tip(get_text_by_id(19438))
                return
        mode_type = global_data.game_mode.get_mode_type()
        is_battle_exercise = True if mode_type == game_mode_const.GAME_MODE_EXERCISE else False
        need_quit_to_lobby_directly = True if mode_type == game_mode_const.GAME_MODE_CONCERT else False
        is_pve = global_data.game_mode.is_pve()

        def on_confirm():
            self.close()
            player = global_data.player
            if player:
                if player.is_creator_local_battle():
                    global_data.player.save_local_battle_data('_lbs_finish_guide', 1)
                    global_data.player.clear_local_battle_data()
                    global_data.player.logic.send_event('E_GUIDE_DESTROY')
                    from logic.comsys.login.CharacterCreatorUINew import CharacterCreatorUINew
                    CharacterCreatorUINew(no_finish=True, opt_from='MainSettingUI')
                else:
                    bat = global_data.player.get_battle()
                    if bat and bat.is_in_settle_celebrate_stage():
                        global_data.emgr.end_celebrate_win_state_event.emit()
                    else:
                        from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE, STAGE_ISLAND
                        if player.logic and player.logic.share_data.ref_parachute_stage in (STAGE_NONE, STAGE_ISLAND, STAGE_MECHA_READY, STAGE_PLANE):
                            player.quit_battle(True)
                        else:
                            player.quit_battle()
                    global_data.ui_mgr.close_ui('GuideUI')

        txt_id = 125
        is_spectate = lambda : global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_in_spectate()
        is_prepare_stage = lambda : global_data.battle and global_data.battle.is_battle_prepare_stage()
        is_in_settle_celebrate_stage = global_data.battle and global_data.battle.is_in_settle_celebrate_stage()
        if not is_spectate() and not is_prepare_stage() and not is_in_settle_celebrate_stage and mode_type in game_mode_const.GAME_MODE_SURVIVALS and global_data.battle:
            battle_tid = global_data.battle.get_battle_tid()
            team_size_conf = confmgr.get('battle_config', str(battle_tid), 'cTeamNum')
            txt_id = 233 if team_size_conf > 1 else 232
        if self.is_in_spectate() and global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
            txt_id = 19492
        if is_battle_exercise:

            def on_confirm_quit_exercise():
                self.close()
                if global_data.player and global_data.player.logic:
                    global_data.player.logic.send_event('E_QUIT_EXERCISE_FIELD')

            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(862009), confirm_callback=on_confirm_quit_exercise)
        elif need_quit_to_lobby_directly:

            def on_confirm_quit():
                self.close()
                if global_data.player and global_data.player.logic:
                    global_data.player.quit_battle(True)

            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(82357), confirm_callback=on_confirm_quit)
        elif is_pve:
            if not global_data.battle:
                return
            win_ret = global_data.battle.get_pve_win_ret()
            if win_ret:
                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(83510), confirm_callback=on_confirm)
            elif is_pve_multi_player_team():
                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(txt_id), confirm_callback=on_confirm)
            else:

                def on_confirm_pve_quit():
                    on_confirm()

                def on_confirm_pve_save():
                    if global_data.player and global_data.player.logic:
                        global_data.player.save_pve_archive()
                    on_confirm()

                SecondConfirmDlg3(parent=self.panel).confirm(content=get_text_by_id(txt_id), confirm_text=get_text_by_id(466), confirm_callback=on_confirm_pve_quit, confirm_text_2=get_text_by_id(465), confirm_callback_2=on_confirm_pve_save)
        else:
            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(txt_id), confirm_callback=on_confirm)

    def is_in_spectate(self):
        return global_data.player and not global_data.player.is_in_global_spectate() and global_data.player.logic and global_data.player.logic.ev_g_is_in_spectate()

    def do_show_btn_surrender(self):
        battle = global_data.battle
        if not battle:
            return False
        player = global_data.player
        if not player or player.is_battle_replaying() or player.is_in_global_spectate():
            return False
        return battle.is_support_surrender()

    def refresh_btn_surrender(self):
        self.init_btn_surrender(self.cur_btn.get('btn_surrender'))

    def init_btn_surrender(self, ui_item):
        if not ui_item:
            return
        else:
            battle = global_data.battle
            if not battle:
                return
            btn = ui_item.btn
            if battle.is_enable_surrender():
                surrender_data = battle.get_surrender_data()
                vote_timestamp = surrender_data.get('vote_timestamp', None)
                if vote_timestamp is not None:
                    btn.SetShowEnable(False)
                else:
                    now = time_utils.get_server_time()
                    enable_timestamp = surrender_data.get('enable_timestamp', 0)
                    enable_time = enable_timestamp - now

                    def refresh_time(pass_time):
                        left_time = int(enable_time - pass_time) + 1
                        btn.SetText(''.join([get_text_by_id(634272), '(%ds)' % left_time]))

                    def refresh_time_finsh():
                        btn.SetText(get_text_by_id(634272))
                        btn.SetShowEnable(True)

                    btn.StopTimerAction()
                    if enable_time <= 0:
                        refresh_time_finsh()
                    else:
                        refresh_time(0)
                        btn.SetShowEnable(False)
                        btn.TimerAction(refresh_time, enable_time, callback=refresh_time_finsh, interval=1)
            else:
                btn.SetShowEnable(False)
            return

    def on_click_surrender(self, btn, touch):
        battle = global_data.battle
        if not battle or not battle.is_enable_surrender():
            global_data.game_mgr.show_tip(get_text_by_id(634274))
            return
        player = global_data.player
        if not player or player.is_battle_replaying() or player.is_in_global_spectate():
            global_data.game_mgr.show_tip(get_text_by_id(634274))
            return
        if btn.IsEnable():
            battle.initiate_surrender()
            self.close()
        else:
            global_data.game_mgr.show_tip(get_text_by_id(634274))

    def refresh_btn_come_home(self):
        self.init_btn_come_home(self.cur_btn.get('btn_come_home'))

    def init_btn_come_home(self, ui_item):
        if not ui_item:
            return
        else:
            player = global_data.player
            if not player:
                return
            bat = player.get_battle() or player.get_joining_battle()
            if not (bat and hasattr(bat, 'get_suicide_timestamp')):
                return
            suicide_timestamp = bat.get_suicide_timestamp()
            btn = ui_item.btn
            revive_time = 0
            if suicide_timestamp is not None:
                revive_time = suicide_timestamp - time_utils.get_server_time()

            def refresh_time(pass_time):
                left_time = int(revive_time - pass_time) + 1
                btn.SetText(''.join([get_text_by_id(18811), '(%ds)' % left_time]))

            def refresh_time_finsh():
                btn.SetText(get_text_by_id(18811))
                btn.SetEnable(True)

            btn.StopTimerAction()
            if revive_time <= 0:
                refresh_time_finsh()
                return
            refresh_time(0)
            btn.SetEnable(False)
            btn.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=1)
            return

    def on_click_come_home(self, btn, touch):
        player = global_data.player
        if not player or not player.logic:
            return
        if player.is_battle_replaying() or player.is_in_global_spectate():
            return
        bat = player.get_battle() or player.get_joining_battle()
        if not (bat and hasattr(bat, 'start_suicide')):
            return
        control_target = player.logic.ev_g_control_target()
        if control_target:
            target_type = control_target.logic.__class__.__name__
            if target_type == 'LMecha':
                from logic.gcommon.cdata import mecha_status_config
                if not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_USE_ITEM):
                    self.close()
                    return
        player.logic.send_event('E_ITEMUSE_TRY', 9935)
        self.close()

    def on_click_recover_btn(self, *args):
        page = self._get_cur_page()
        if page:
            confirm_img_path = 'gui/ui_res_2/common/button/btn_secondary_minor.png'
            cancel_img_path = 'gui/ui_res_2/common/button/btn_secondary_major.png'
            confirm_ui = NormalConfirmUI(None, get_text_by_id(633826), show_cancel_btn=True, confirm_cb=page.on_recover_default)
            btn_cancel = confirm_ui.btn_1.btn_common
            btn_confirm = confirm_ui.btn_2.btn_common
            btn_confirm.SetTextColor(color1='#SW', color2='#SW', color3='#SW')
            btn_confirm.SetFrames('', [confirm_img_path, confirm_img_path, confirm_img_path])
            btn_cancel.SetTextColor(color1=7616256, color2=7616256, color3=7616256)
            btn_cancel.SetFrames('', [cancel_img_path, cancel_img_path, cancel_img_path])
        return

    def on_click_apply_all_btn(self, *args):
        page = self._get_cur_page()
        if page:
            page.on_apply_all()

    def on_click_sync_server_btn(self, *args):
        page = self._get_cur_page()
        if page:

            def cancel():
                global_data.ui_mgr.close_ui('SecondConfirmDlg2')

            def confirm(page=page):
                if page:
                    page.on_sync_to_server()
                    global_data.game_mgr.show_tip(920764)

            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_by_id(920765), confirm_text=get_text_by_id(80306), confirm_callback=confirm, cancel_text=get_text_by_id(80295), cancel_callback=cancel, click_blank_close=False)

    def _get_account_btn_text_id(self):
        if self._is_account_btn_as_guest_bind:
            return 82052
        else:
            if self._is_account_btn_as_logout:
                return 220
            return 80458

    def update_function_buttons(self, page=None):
        small_btn_list = [
         'btn_language', 'btn_user', 'btn_sw_user', 'btn_help', 'btn_feedback_new', 'btn_feedback',
         'btn_bind', 'btn_bind_fb', 'btn_announce', 'btn_agreement', 'btn_exit_game', 'btn_update',
         'btn_gift', 'btn_sprite']
        small_btn_show_settings = {'btn_language': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_language_check},'btn_user': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_account_show_check},'btn_sw_user': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_sw_account_show_check},'btn_help': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_help_show_check},'btn_bind_fb': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_bind_fb_show_check},'btn_bind': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_bind_show_check},'btn_announce': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE]},'btn_update': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_update_show_check},'btn_feedback': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_BATTLE, SH_IN_NON_BATTLE],'check_func': self.btn_feedback_check},'btn_feedback_new': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_feedback_new_check},'btn_agreement': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_agreement_show_check},'btn_exit_game': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_BATTLE, SH_IN_NON_BATTLE],'check_func': self.btn_exit_game_show_check},'btn_gift': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_gift_show_check},'btn_sprite': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_sprite_show_check}}
        small_btn_settings = {'btn_language': {'img': 'gui/ui_res_2/common/icon/icon_language.png','text': 80467,'func': self.on_click_lang_btn},'btn_user': {'img': 'gui/ui_res_2/common/icon/icon_user_center.png','text': self._get_account_btn_text_id(),'func': self.on_click_account_btn,
                        'init_func': self.check_show_red_point},
           'btn_sw_user': {'img': 'gui/ui_res_2/common/icon/icon_switch.png','text': 3108,'func': self.on_click_sw_account_btn},'btn_bind': {'img': 'gui/ui_res_2/common/icon/icon_bind.png','text': 80047,'func': self.on_click_bind_btn,'init_func': self.init_bind_btn
                        },
           'btn_bind_fb': {'img': 'gui/ui_res_2/icon/icon_btn_fb.png','text': 81046,'func': self.on_click_bind_fb_btn,'init_func': self.init_bind_fb_btn
                           },
           'btn_announce': {'img': 'gui/ui_res_2/common/icon/icon_announce.png','text': 80161,'func': self.on_announce},'btn_help': {'img': 'gui/ui_res_2/common/icon/icon_customer_serve.png','text': 80231,'func': self.on_click_help_btn},'btn_feedback': {'img': 'gui/ui_res_2/common/icon/icon_feedback.png','text': 80140,'func': self.on_click_feedback_btn},'btn_feedback_new': {'img': 'gui/ui_res_2/common/icon/icon_feedback.png','text': 80140,'func': self.on_click_new_feedback_btn},'btn_agreement': {'img': 'gui/ui_res_2/common/icon/icon_agreement.png','text': 80422,'func': self.on_click_agreement_btn},'btn_exit_game': {'img': 'gui/ui_res_2/common/icon/icon_quit_game.png','text': 80375,'func': self.on_click_exit_game_btn},'btn_update': {'img': 'gui/ui_res_2/common/icon/icon_update.png','text': 609139,'func': self.on_click_update_btn,'init_func': self.check_show_update_red_point},'btn_gift': {'img': 'gui/ui_res_2/main/icon_redeem.png','text': 635680,'func': self.on_click_gift_btn},'btn_sprite': {'img': 'gui/ui_res_2/main/icon_sprite.png','text': 635681,'func': self.on_click_sprite_btn}}
        big_btn_list = [
         'btn_upgrade', 'btn_exit', 'btn_sync_server', 'btn_surrender', 'btn_recover', 'btn_come_home', 'btn_apply_all', 'btn_my_video']
        big_btn_show_settings = {'btn_surrender': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget'],'show_set': [SH_IN_BATTLE],'check_func': self.do_show_btn_surrender},'btn_recover': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget', 'MechaSettingWidget', 'SensitivitySettingWidget', 'MechaSensitivitySettingWidget', 'MouseKeyboardSettingWidget', 'OperationSettingWidget', 'VehicleSettingWidget', 'QualitySettingWidget', 'SoundSettingWidget', 'PrivacySettingWidget'],'show_set': [SH_IN_NON_BATTLE, SH_IN_BATTLE]},'btn_sync_server': {'page': ['SensitivitySettingWidget', 'MouseKeyboardSettingWidget', 'QualitySettingWidget'],'show_set': [SH_IN_NON_BATTLE, SH_IN_BATTLE],'check_func': self.btn_sync_server_show_check},'btn_upgrade': {'page': ['QualitySettingWidget'],'show_set': [SH_IN_NON_BATTLE],'check_func': self.btn_upgrade_show_check},'btn_exit': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget'],'show_set': [SH_IN_BATTLE],'check_func': self.do_show_exit_btn},'btn_come_home': {'page': ['BaseSettingWidget', 'AdvancedSettingWidget'],'show_set': [SH_IN_BATTLE],'check_func': self.do_show_come_home_btn},'btn_apply_all': {'page': ['MechaSensitivitySettingWidget'],'show_set': [SH_IN_NON_BATTLE, SH_IN_BATTLE]},'btn_my_video': {'page': ['HighLightSettingWidget'],'show_set': [SH_IN_NON_BATTLE]}}
        btn_exit_text_id = 80374 if self._btn_exit_text_id is None else self._btn_exit_text_id
        big_btn_settings = {'btn_surrender': {'text': 634272,'func': self.on_click_surrender,'init_func': self.init_btn_surrender},'btn_recover': {'text': 80190,'func': self.on_click_recover_btn},'btn_sync_server': {'text': 920763,'func': self.on_click_sync_server_btn},'btn_upgrade': {'text': 90059,'func': self.on_click_upgrade_package},'btn_exit': {'text': btn_exit_text_id,'func': self.on_click_exit_btn,'template': 'setting/i_setting_main_exit_btn'},'btn_come_home': {'text': 18811,'func': self.on_click_come_home,'init_func': self.init_btn_come_home},'btn_apply_all': {'text': 2240,'func': self.on_click_apply_all_btn},'btn_my_video': {'text': 2292,'func': self._show_my_video}}
        small_final_list = self._get_show_button_list(small_btn_list, small_btn_show_settings, page)
        self._init_small_show_button(small_final_list, small_btn_settings)
        big_final_list = self._get_show_button_list(big_btn_list, big_btn_show_settings, page)
        self._init_big_show_button(big_final_list, big_btn_settings)
        self._refresh_apply_btn(page)
        return

    def check_show_collected_personal_info(self):
        import game3d
        if not interface.is_mainland_package():
            return False
        if game3d.get_platform() not in [game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID]:
            return False
        if not global_data.channel:
            return False
        return global_data.channel.has_feature('MODE_HAS_PERSONALINFOLIST')

    def personal_info_extend_func_callback(self, json_dict):
        if json_dict.get('respMsg', '') not in ('', 'success'):
            log_error('failed to get personal info list, respMsg: %s' % json_dict.get('respMsg', ''))

    def on_click_collected_personal_info_btn(self, *args):
        data = {'methodId': 'showPersonalInfoList',
           'channel': 'personal_info_list'
           }
        if global_data.channel:
            global_data.channel.register_extend_callback_function(self.__class__.__name__, 'showPersonalInfoList', self.personal_info_extend_func_callback)
            global_data.channel.extend_func_by_dict(data)

    def get_platform_shorthand(self):
        platform_dict = {game3d.PLATFORM_IOS: 'i',
           game3d.PLATFORM_ANDROID: 'a',
           game3d.PLATFORM_WIN32: 'p',
           game3d.PLATFORM_MAC: 'm'
           }
        return platform_dict.get(game3d.get_platform(), 'a')

    def open_privacy_info_url(self, prefix):
        import base64
        import json
        app_channel = global_data.channel.get_prop_str('APP_CHANNEL')
        jf_gameid = global_data.channel.get_prop_str('JF_GAMEID')
        data = {'gameid': jf_gameid,'app_channel': app_channel,'platform': self.get_platform_shorthand()}
        dict_json = json.dumps(data)
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            safeurl_base64_data = base64.urlsafe_b64encode(six.ensure_binary(dict_json.rstrip('=')))
        else:
            safeurl_base64_data = base64.urlsafe_b64encode(six.ensure_binary(dict_json))
        url = prefix + six.ensure_str(safeurl_base64_data)
        if global_data.channel:
            global_data.channel.open_unisdk_web_view(url)

    def on_click_third_party_shared_personal_info(self, *args):
        prefix = 'https://protocol.unisdk.netease.com/tpsl/html/sdk_list.html?data='
        self.open_privacy_info_url(prefix)

    def on_click_privacy_policy(self, *args):
        prefix = 'https://protocol.unisdk.netease.com/api/template/v90/latest.html?data='
        self.open_privacy_info_url(prefix)

    def _refresh_apply_btn(self, page=None):
        if page is None:
            page = self._get_cur_page()
        show = page.has_apply_btn() if page else False
        self._apply_btn.setVisible(show)
        return

    def _get_show_button_list(self, btn_show_list, btn_show_settings, page=None):
        final_show_list = []
        if not global_data.player:
            return final_show_list
        else:
            cur_battle_status = SH_IN_BATTLE if global_data.player.is_in_battle() else SH_IN_NON_BATTLE
            if page is None:
                page = self._get_cur_page()
            for btn in btn_show_list:
                btn_show_setting = btn_show_settings.get(btn)
                if btn_show_setting:
                    show_page = btn_show_setting.get('page', [])
                    show_set = btn_show_setting.get('show_set', [])
                    check_func = btn_show_setting.get('check_func')
                    if (not show_page or page is not None and page.__class__.__name__ in show_page) and cur_battle_status in show_set:
                        if check_func and not check_func():
                            continue
                        final_show_list.append(btn)

            return final_show_list

    def _init_small_show_button(self, show_list, btn_settings):
        self.panel.list_small_btn.DeleteAllSubItem()
        for idx, _ in enumerate(show_list):
            btn_name = show_list[idx]
            btn_set = btn_settings.get(btn_name)
            if not btn_set:
                continue
            else:
                template = btn_set.get('template', '')
                if not template:
                    ui_item = self.panel.list_small_btn.AddTemplateItem(idx)
                    ui_item.img_reward.setVisible(False)
                    ui_item.img_bind.setVisible(False)
                    ui_item.red_dot.setVisible(False)
                    img = btn_set.get('img', '')
                    text = btn_set.get('text', '')
                    ui_item.img.SetDisplayFrameByPath('', img)
                    ui_item.lab.SetString(text)
                else:
                    print template
                    ui_item = global_data.uisystem.load_template_create(template)
                    self.panel.list_small_btn.AddControl(ui_item)
                func = btn_set.get('func')
                init_func = btn_set.get('init_func')
                if init_func:
                    init_func(ui_item)

                @ui_item.btn.callback()
                def OnClick(btn, touch, ui_item=ui_item, func=func):
                    ui_item.red_dot.setVisible(False)
                    func(btn, touch)

    def do_show_exit_btn(self):
        game_mode = global_data.game_mode
        if not game_mode:
            return True
        return not game_mode.is_mode_type(game_mode_const.Hide_ExitBtn)

    def _show_my_video(self, btn, touch):
        page = self._get_cur_page()
        if page:
            page.save_setting()
        global_data.ui_mgr.show_ui('MyVideoUI', 'logic.comsys.setting_ui')

    def do_show_come_home_btn(self):
        game_mode = global_data.game_mode
        if not game_mode:
            return False
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            if game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
                return False
        if global_data.battle and hasattr(global_data.battle, 'settle_timestamp'):
            settle_timestamp = global_data.battle.settle_timestamp
            if settle_timestamp:
                revive_time = settle_timestamp - time_utils.get_server_time()
                if revive_time <= 10:
                    return False
        return game_mode.is_mode_type(game_mode_const.Show_ComeHome)

    def _init_big_show_button(self, show_list, btn_settings):
        self.panel.list_big_btn.DeleteAllSubItem()
        all_item = self.panel.list_big_btn.GetAllItem()
        self.cur_btn = {}
        for idx, btn_name in enumerate(show_list):
            btn_set = btn_settings.get(btn_name)
            template = btn_set.get('template')
            if template:
                ui_item = global_data.uisystem.load_template_create(template)
                self.panel.list_big_btn.AddControl(ui_item)
            else:
                ui_item = self.panel.list_big_btn.AddTemplateItem()
            if not btn_set:
                ui_item.setVisible(False)
            else:
                text = btn_set.get('text', '')
                func = btn_set.get('func')
                init_func = btn_set.get('init_func')
                ui_item.btn.SetText(text)
                if init_func:
                    init_func(ui_item)

                @ui_item.btn.callback()
                def OnClick(btn, touch, ui_item=ui_item, func=func):
                    func(btn, touch)

                if btn_name == 'btn_exit':
                    self.ref_btn_exit = ui_item
            self.cur_btn[btn_name] = ui_item

    def get_big_func_btn(self, btn_name):
        ui_item = self.cur_btn.get(btn_name, None)
        if not ui_item:
            return
        else:
            return getattr(ui_item, 'btn', None)

    def refresh_sync_server_btn_enable(self, page=None):
        sync_btn = self.get_big_func_btn('btn_sync_server')
        if not sync_btn:
            return
        cur_page = page or self._get_cur_page() if 1 else page
        en = cur_page.should_btn_sync_server_enabled() if cur_page else False
        sync_btn.SetEnable(en)

    def check_tab_red_point(self, last_index, cur_index):
        tab_red_point_func = self.tab_red_point_func
        ui_item = self.panel.content_bar.list_tab.GetItem(cur_index)
        if ui_item:
            ui_item.img_hint.setVisible(False)
        if last_index is not None:
            conf = self.page_conf_list[last_index]
            if isinstance(conf, tuple) or isinstance(conf, list):
                confs = conf[:]
            else:
                confs = (
                 conf,)
            for c in confs:
                last_widget_name = c['widget']
                func = tab_red_point_func.get(last_widget_name, None)
                if func:
                    self.panel.content_bar.list_tab.GetItem(last_index).img_hint.setVisible(func())

        return

    def refresh_tab_red_point(self):
        tab_red_point_func = self.tab_red_point_func
        for idx, widget_conf in enumerate(self.page_conf_list):
            if isinstance(widget_conf, tuple) or isinstance(widget_conf, list):
                confs = widget_conf[:]
            else:
                confs = (
                 widget_conf,)
            for conf in confs:
                widget_name = conf['widget']
                if widget_name in self.tab_red_point_func:
                    func = tab_red_point_func.get(widget_name, None)
                    self.panel.content_bar.list_tab.GetItem(idx).img_hint.setVisible(func())

        return

    def check_quality_red_point(self):
        return bool(global_data.achi_mgr.get_cur_user_archive_data('setting_red_point_frame_rate'))

    def _check_high_light_red_point(self):
        return not bool(global_data.achi_mgr.get_cur_user_archive_data('setting_red_point_high_light', default=0))

    def check_privilege_setting_red_point(self):
        from logic.gutils.red_point_utils import get_priv_setting_rp
        new_setting = get_priv_setting_rp()
        return new_setting

    def check_sound_setting_red_point(self):
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MUSIC
        if global_data.lobby_red_point_data:
            return global_data.lobby_red_point_data.get_rp_by_type(L_ITEM_TYPE_MUSIC)
        else:
            return False

    def update_setting_red_point(self):
        self.refresh_tab_red_point()
        self.refresh_lobby_bgm()

    def refresh_lobby_bgm(self):
        page = self._get_cur_page()
        if page and hasattr(page, 'refresh_cur_bgm'):
            page.refresh_cur_bgm()

    def init_pc_scroll_bar(self):
        inner_size = self.panel.content_bar.page.GetInnerContentSize()
        view_size = self.panel.content_bar.page.GetContentSize()
        self._init_page_offset_y = self.panel.content_bar.page.GetContentOffset().y
        self._max_page_move_dist = abs(self._init_page_offset_y)
        if self._max_page_move_dist <= SHOW_SLIDER_MIN_LEN:
            self.panel.nd_scroll_pc.setVisible(False)
            return
        btn_scroll_bar = self.panel.nd_scroll_pc.scroll_bar_bg.btn_scroll_bar
        self.panel.nd_scroll_pc.setVisible(True)
        h = float(view_size[1] / inner_size.height) * 100.0
        w = btn_scroll_bar.GetContentSize()[0]
        btn_scroll_bar.SetContentSize(w, '{}%'.format(h))
        btn_scroll_bar.SetPosition('50%1', '100%0')
        self._btn_scroll_bar_begin_pos_y = btn_scroll_bar.GetPosition()[1]
        self._btn_scroll_bar_end_pos_y = h / 100.0 * self._btn_scroll_bar_begin_pos_y
        self._max_scroll_bar_move_dist = self._btn_scroll_bar_begin_pos_y - self._btn_scroll_bar_end_pos_y
        self._scroll_bar_page_move_ratio = self._max_page_move_dist / self._max_scroll_bar_move_dist if self._max_scroll_bar_move_dist else 1
        btn_scroll_bar.BindMethod('OnDrag', self.on_drag_scroll_bar)
        self.panel.content_bar.page.BindMethod('OnScrolling', self.on_page_scrolling)

    def on_drag_scroll_bar(self, btn, touch, *args):
        btn_scroll_bar = self.panel.nd_scroll_pc.scroll_bar_bg.btn_scroll_bar
        if not btn_scroll_bar.isVisible() or self._max_page_move_dist <= 0:
            return
        curr_scroll_bar_pos = btn_scroll_bar.GetPosition()
        dy = touch.getDelta().y * uoc.SST_MAIN_SETTING_DRAG_SCROLL_BAR
        btn_scroll_bar_offset_y = curr_scroll_bar_pos[1] + dy
        if btn_scroll_bar_offset_y < self._btn_scroll_bar_end_pos_y:
            btn_scroll_bar_offset_y = self._btn_scroll_bar_end_pos_y
        if btn_scroll_bar_offset_y > self._btn_scroll_bar_begin_pos_y:
            btn_scroll_bar_offset_y = self._btn_scroll_bar_begin_pos_y
        btn_scroll_bar.SetPosition(curr_scroll_bar_pos[0], btn_scroll_bar_offset_y)
        curr_page_offset = self.panel.content_bar.page.GetContentOffset()
        curr_page_offset.y -= dy * self._scroll_bar_page_move_ratio
        if curr_page_offset.y > 0:
            curr_page_offset.y = 0
        if curr_page_offset.y < self._init_page_offset_y:
            curr_page_offset.y = self._init_page_offset_y
        self.panel.content_bar.page.SetContentOffset(curr_page_offset)

    def on_page_scrolling(self, *args):
        if not self.panel.nd_scroll_pc.scroll_bar_bg.btn_scroll_bar.isVisible() or self._max_page_move_dist <= 0:
            return
        curr_page_offset = self.panel.content_bar.page.GetContentOffset()
        page_offset_y = curr_page_offset.y - self._init_page_offset_y
        move_percentage = page_offset_y / self._max_page_move_dist
        if move_percentage < 0.0 or move_percentage > 1.0:
            return
        btn_scroll_bar_offset_y = self._btn_scroll_bar_begin_pos_y - move_percentage * (self._btn_scroll_bar_begin_pos_y - self._btn_scroll_bar_end_pos_y)
        self.panel.nd_scroll_pc.scroll_bar_bg.btn_scroll_bar.SetPosition('50%1', btn_scroll_bar_offset_y)

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        curr_page_offset = self.panel.content_bar.page.GetContentOffset()
        curr_page_offset.y -= delta * uoc.SST_MAIN_SETTING_MOUSE_WHEEL
        if curr_page_offset.y > 0.0:
            curr_page_offset.y = 0.0
        if curr_page_offset.y < self._init_page_offset_y:
            curr_page_offset.y = self._init_page_offset_y
        self.panel.content_bar.page.SetContentOffset(curr_page_offset)
        self.on_page_scrolling()

    def check_can_mouse_scroll(self):
        if global_data.is_pc_mode and self.HOT_KEY_NEED_SCROLL_SUPPORT and global_data.player:
            return True
        return False

    def set_btn_exit_text_id(self, text_id):
        self._btn_exit_text_id = text_id
        if self.ref_btn_exit and self.ref_btn_exit.btn:
            self.ref_btn_exit.btn.SetText(text_id)