# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETipsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT, BASE_LAYER_ZORDER_1
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.pve_const import TARGET_TYPE_SURVIVE
from logic.gutils.pve_utils import get_mission_text
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.screen_utils import world_pos_to_screen_pos
from common.utils.cocos_utils import getScreenSize
from math import atan, pi
from common.platform.device_info import DeviceInfo
from common.utils.ui_utils import get_scale
from common.utils.timer import CLOCK
from logic.gcommon.time_utility import get_server_time
from .PVESurviveWidget import PVESurviveWidget
from .PVEMonsterMarkWidget import PVEMonsterMarkWidget
from .PVEMonsterBloodWidget import PVEMonsterBloodWidget
from .PVEBossBloodWidget import PVEBossBloodWidget
from .PVEMonsterIconWidget import PVEMonsterIconWidget
from .PVEBoxMarkWidget import PVEBoxMarkWidget
from .PVEShopMarkWidget import PVEShopMarkWidget
from .PVEMonsterHPWidget import PVEMonsterHPWidget
import six

class PVETipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tips/pve/i_guide_task_tips'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(PVETipsUI, self).on_init_panel(*args, **kwargs)
        self.init_params()
        self.process_events(True)
        self.init_survive_widget()
        self.init_monster_mark_widget()
        self.init_monster_hp_widget()
        self.init_boss_blood_widget()
        self.init_box_mark_widget()
        self.init_shop_mark_widget()
        self.init_custom_com()
        self.init_mgr()

    def init_params(self):
        self.dest_guide_widgets = {}
        self.locate_timers = {}
        self.init_locate_params()
        self.survive_timer = None
        self.survive_total = 0
        self.survive_count = 0
        self.survive_10s_tag = False
        self.survive_widget = None
        self.monster_mark_widget = None
        self.monster_hp_widget = None
        self.boss_blood_widget = None
        self.box_mark_widget = None
        self.shop_mark_widget = None
        self.target_monsters = []
        self.panel.bar_prog.setVisible(False)
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'battle_switch_scene_event': self.clear_all,
           'scene_player_setted_event': self.init_all,
           'pve_boss_init': self.on_boss_init,
           'pve_boss_destroy': self.on_boss_destroy
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.clear_all()
        self.process_events(False)
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        if global_data.pve_tips_mgr:
            global_data.pve_tips_mgr.finalize()
        self.destroy_widget('survive_widget')
        self.destroy_widget('monster_mark_widget')
        self.destroy_widget('monster_hp_widget')
        self.destroy_widget('boss_blood_widget')
        self.destroy_widget('box_mark_widget')
        self.destroy_widget('shop_mark_widget')
        self.init_params()
        super(PVETipsUI, self).on_finalize_panel()
        return

    def clear_all(self):
        self.clear_all_locate()
        self.reset_survive_timer()
        self.survive_widget and self.survive_widget.clear()
        self.monster_mark_widget and self.monster_mark_widget.clear()
        self.monster_hp_widget and self.monster_hp_widget.clear()
        self.boss_blood_widget and self.boss_blood_widget.clear()
        self.box_mark_widget and self.box_mark_widget.clear()
        self.shop_mark_widget and self.shop_mark_widget.clear()
        global_data.pve_tips_mgr and global_data.pve_tips_mgr.clear()

    def init_all(self, *args):
        self.clear_all_locate()
        self.set_mission(global_data.battle.mission_data)
        for guide_id, guide_pos in six.iteritems(global_data.battle.guide_data):
            self.set_guide_pos(guide_id, guide_pos)

    def set_mission(self, mission_data):
        if not mission_data:
            return
        mission_type = mission_data['target_type']
        if mission_type == TARGET_TYPE_SURVIVE:
            self.set_survive_timer(mission_data)
            return
        self.panel.bar_prog.setVisible(False)
        self.reset_survive_timer()
        text = get_mission_text(mission_data)
        if text:
            self.show_mission(text)
        else:
            self.set_mission_visible(False)
        self.target_monsters = mission_data.get('target_monsters', [])
        if self.target_monsters:
            global_data.emgr.pve_set_target_monsters.emit(self.target_monsters)

    def show_mission(self, text):
        self.panel.nd_task_tips.lab_task.SetString(text)
        self.set_mission_visible(True)

    def set_mission_visible(self, visible):
        self.panel.nd_task_tips.setVisible(visible)

    def init_survive_widget(self):
        self.survive_widget = PVESurviveWidget(self.panel)

    def set_survive_timer(self, data):
        self.reset_survive_timer()
        self.survive_total = data['total_prog']
        text_id = get_mission_text(data)
        self.show_mission(get_text_by_id(text_id))
        cur_time = get_server_time()
        end_ts = data['end_ts']
        self.panel.bar_prog.setVisible(True)
        self.survive_10s_tag = False
        self.survive_count = int(end_ts - cur_time)
        self.survive_timer = global_data.game_mgr.register_logic_timer(self.tick_survive, 1, mode=CLOCK)
        self.survive_widget and self.survive_widget.set_visible(True)

    def reset_survive_timer(self):
        if self.survive_timer:
            global_data.game_mgr.unregister_logic_timer(self.survive_timer)
            self.survive_timer = None
        self.survive_widget and self.survive_widget.set_visible(False)
        return

    def tick_survive(self, *args):
        self.survive_count -= 1
        s_prog = self.survive_count / self.survive_total * 100.0
        s_lab = '%ss' % self.survive_count
        self.panel.bar_prog.prog.SetPercentage(s_prog)
        self.survive_widget and self.survive_widget.set_prog(s_prog, s_lab)
        self.panel.bar_prog.lab_countdown.SetString(s_lab)
        if self.survive_count <= 10 and not self.survive_10s_tag:
            ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
            ui.on_delay_close(10)
            global_data.sound_mgr.play_sound('Play_time_countdown')
            self.survive_10s_tag = True
        if self.survive_count <= 0:
            self.panel.bar_prog.setVisible(False)
            self.reset_survive_timer()

    def init_locate_params(self):
        self.screen_size = getScreenSize()
        self.screen_angle_limit = atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / pi
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('40w'), get_scale('120w')),
           'scale_low': (
                       get_scale('220w'), get_scale('220w'))
           }

    def init_guide_widget(self, g_id):
        if g_id in self.dest_guide_widgets:
            self.clear_locate(g_id)
        widget = global_data.uisystem.load_template_create('battle_tips/pve/i_guide_locate', self.panel)
        widget.setVisible(False)
        self.dest_guide_widgets[g_id] = widget

    def set_guide_pos(self, g_id, pos):
        self.show_locate(g_id, pos, 2.0)

    def clear_guide_pos(self, g_id):
        self.clear_locate(g_id)

    def show_locate(self, g_id, pos, offset):
        self.init_guide_widget(g_id)
        widget = self.dest_guide_widgets[g_id]
        widget.setVisible(True)
        widget.PlayAnimation('keep')
        pos = math3d.vector(*pos)
        pos.y += NEOX_UNIT_SCALE * offset
        self.reset_locate_timer(g_id)
        self.locate_timers[g_id] = global_data.game_mgr.register_logic_timer(lambda g=g_id, p=pos: self.calc_nd_pos(g, p), interval=1)

    def clear_locate(self, g_id):
        widget = self.dest_guide_widgets.get(g_id, None)
        if widget:
            widget.setVisible(False)
            widget.StopAnimation('keep')
            widget.Destroy()
            self.dest_guide_widgets.pop(g_id)
        self.reset_locate_timer(g_id)
        return

    def clear_all_locate(self):
        for i in self.dest_guide_widgets:
            widget = self.dest_guide_widgets[i]
            if widget:
                widget.setVisible(False)
                widget.StopAnimation('keep')
                widget.Destroy()

        self.dest_guide_widgets = {}
        for i in self.locate_timers:
            timer = self.locate_timers[i]
            if timer:
                global_data.game_mgr.unregister_logic_timer(timer)

        self.locate_timers = {}

    def reset_locate_timer(self, g_id):
        timer = self.locate_timers.get(g_id, None)
        if timer:
            global_data.game_mgr.unregister_logic_timer(timer)
            self.locate_timers.pop(g_id)
        return

    def calc_nd_pos(self, g_id, position):
        camera = global_data.game_mgr.scene.active_camera
        if not camera:
            return
        if not global_data.cam_lctarget:
            return
        widget = self.dest_guide_widgets[g_id]
        nd_lab = widget.nd_lab
        is_in_screen, pos, angle = world_pos_to_screen_pos(nd_lab, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        if is_in_screen:
            m_pos = global_data.cam_lctarget.ev_g_position()
            dist = m_pos - position
            dist = max(0, int(dist.length / NEOX_UNIT_SCALE) - 2)
            nd_lab.setPosition(pos)
            nd_lab.nd_arrows.setVisible(False)
            nd_lab.lab_distance.setVisible(True)
            nd_lab.lab_distance.SetString(get_text_by_id(157).format(str(dist)))
        else:
            nd_lab.setPosition(pos)
            nd_lab.nd_arrows.setVisible(True)
            nd_lab.lab_distance.setVisible(False)
            nd_lab.nd_arrows.setRotation(angle)

    def init_monster_mark_widget(self):
        self.monster_mark_widget = PVEMonsterMarkWidget(self.panel)

    def init_monster_blood_widget(self):
        self.monster_blood_widget = PVEMonsterBloodWidget(self.panel, self)

    def init_boss_blood_widget(self):
        self.boss_blood_widget = PVEBossBloodWidget(self.panel)

    def on_boss_init(self, eid):
        self.boss_blood_widget and self.boss_blood_widget.init_boss(eid)

    def on_boss_destroy(self, eid):
        self.boss_blood_widget and self.boss_blood_widget.destroy_boss(eid)

    def init_monster_icon_widget(self):
        self.monster_icon_widget = PVEMonsterIconWidget(self.panel, self)

    def init_box_mark_widget(self):
        self.box_mark_widget = PVEBoxMarkWidget(self.panel)

    def init_shop_mark_widget(self):
        self.shop_mark_widget = PVEShopMarkWidget(self.panel)

    def init_monster_hp_widget(self):
        self.monster_hp_widget = PVEMonsterHPWidget(self.panel, self)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_mgr(self):
        if not global_data.pve_tips_mgr:
            from .PVETipsMgr import PVETipsMgr
            PVETipsMgr()