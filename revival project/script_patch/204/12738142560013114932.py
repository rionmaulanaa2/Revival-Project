# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Scavenge/ScavengeItemLocateUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.platform.device_info import DeviceInfo
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from common.utils.ui_utils import get_scale
import math3d
import cc
import math
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from math import ceil

class ScavengeItemLocateChildUI(object):
    MAX_SHOW_DIST = 30
    MAX_DIST = 1000
    LEVEL2PANEL = {0: 'battle_pick_up/battle_pick_weapon_reset_tips_green',
       1: 'battle_pick_up/battle_pick_weapon_reset_tips_green',
       2: 'battle_pick_up/battle_pick_weapon_reset_tips_blue',
       3: 'battle_pick_up/battle_pick_weapon_reset_tips_purple',
       4: 'battle_pick_up/battle_pick_weapon_reset_tips_yellow',
       5: 'battle_pick_up/battle_pick_weapon_reset_tips_yellow',
       6: 'battle_pick_up/battle_pick_weapon_reset_tips_yellow'
       }

    def __init__(self, parent, spawn_id, scale, item_quality):
        self.parent = parent
        self.spawn_id = spawn_id
        if item_quality in ScavengeItemLocateChildUI.LEVEL2PANEL:
            self._nd = global_data.uisystem.load_template_create(ScavengeItemLocateChildUI.LEVEL2PANEL[item_quality])
        else:
            return
        self._nd.setVisible(False)
        self._nd.setPosition(0, 0)
        self.space_nd = CCUISpaceNode.Create()
        self.space_nd.AddChild('', self._nd)
        horizontal_margin = 140 * scale
        vertical_margin = 80 * scale
        top_margin = get_scale('40w')
        self.space_nd.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self.space_nd.set_screen_check_margin(0, 0, top_margin, 0)
        self.position = None
        self.weapon_name = None
        self.rebirth_cd = 0
        self.dist = 0
        self.cd_end_time = 0
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self._nd])
        return

    def on_finalize_panel(self):
        self._nd and self._nd.Destroy()
        self._nd = None
        self.space_nd and self.space_nd.Destroy()
        self.space_nd = None
        return

    def update_wrapper(self, pos, rebirth_cd, weapon_name_id):
        if not pos:
            return
        x, y, z = pos
        self.position = math3d.vector(x, y + 10, z)
        self.rebirth_cd = rebirth_cd
        self.space_nd.set_assigned_world_pos(self.position)
        if not self.weapon_name:
            self.weapon_name = get_text_by_id(weapon_name_id)
            self._nd.nd_scale.nd_name.lab_name.SetString(self.weapon_name)

    def check_show(self):
        if not self.position or not self.rebirth_cd:
            return False
        else:
            cam = global_data.game_mgr.scene.active_camera
            if not cam:
                return False
            is_in_screen = self.space_nd.get_is_in_screen()
            if not is_in_screen:
                return False
            dist = cam.position - self.position
            self.dist = dist.length / NEOX_UNIT_SCALE
            if self.dist > self.MAX_SHOW_DIST:
                return False
            rebirth_cd_msg = global_data.death_battle_data.hyper_spawn_data.get(self.spawn_id, None)
            self.cd_end_time = rebirth_cd_msg[1]
            if self.cd_end_time < time_utility.time():
                return False
            return True

    def update_nd_status(self):
        if not self.check_show():
            self._nd.setVisible(False)
            return
        self._nd.setVisible(True)
        scale = max(0.5, (self.MAX_DIST - self.dist) * 1.0 / self.MAX_DIST)
        self._nd.setScale(scale)
        lplayer = global_data.cam_lplayer
        if lplayer:
            left_time = self.cd_end_time - time_utility.time()
            self._nd.nd_scale.nd_locate.lab_time.SetString('%dS' % ceil(left_time))
            if self.rebirth_cd > 0:
                rebirth_cd_percent = 1 - min(left_time / self.rebirth_cd, 1)
            else:
                rebirth_cd_percent = 1
            self._nd.nd_scale.nd_locate.prog.SetPercent(rebirth_cd_percent * 100)


class ScavengeItemLocateUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.panel.setLocalZOrder(1)
        self.init_parameters()
        self.process_event(True)
        self.init_nd()
        self.init_spawn_info()
        self.run_timer = None
        self.update_scavenge_item_locate_ui()
        self.on_tick()
        return

    def on_finalize_panel(self):
        self.clear_run_timer()
        for widget in six.itervalues(self._widgets):
            widget.on_finalize_panel()

        self._widgets = {}
        self.process_event(False)

    def init_parameters(self):
        self._widgets = {}
        self.rebirth_info = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'update_scavenge_item_locate_ui': self.update_scavenge_item_locate_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_spawn_info(self):
        battle = global_data.battle
        if not battle:
            return
        if not global_data.death_battle_data:
            return
        spawn_info = global_data.death_battle_data.spawn_info
        born_data = global_data.game_mode.get_born_data()
        born_spawn_data = global_data.game_mode.get_cfg_data('born_spawn_data')
        spawn_lst = born_data[str(battle.area_id)].get('spawn_lst', [])
        for spawn_id in spawn_lst:
            if str(spawn_id) in born_spawn_data:
                spawn_info[spawn_id] = born_spawn_data[str(spawn_id)]

    def update_scavenge_item_locate_ui(self):
        if not global_data.death_battle_data:
            return
        hyper_spawn_data = global_data.death_battle_data.get_hyper_rebirth_data()
        for k, v in six.iteritems(hyper_spawn_data):
            self.rebirth_info[k] = v
            self.show_widget(k)

    def show_widget(self, spawn_id):
        item_id = global_data.death_battle_data.spawn_info[spawn_id].get('item_id')
        item_name_id = confmgr.get('item', str(item_id), 'name_id')
        item_quality = confmgr.get('item', str(item_id), 'iQuality')
        if spawn_id not in self._widgets:
            self._widgets[spawn_id] = ScavengeItemLocateChildUI(self, spawn_id, self.panel.getScale(), item_quality)
        x, y, z = global_data.death_battle_data.spawn_info[spawn_id].get('pos')
        rebirth_cd = global_data.death_battle_data.spawn_info[spawn_id].get('delay_time')
        self._widgets[spawn_id].update_wrapper((x, y, z), rebirth_cd, item_name_id)

    def del_widget(self, spawn_id):
        if spawn_id in self._widgets:
            self._widgets[spawn_id].on_finalize_panel()
            del self._widgets[spawn_id]

    def _on_scene_observed_player_setted(self, lplayer):
        self.init_nd()

    def init_nd(self):
        for spawn_id in six.iterkeys(self._widgets):
            self.show_widget(spawn_id)

    def update_child_widgets(self):
        hyper_spawn_data = global_data.death_battle_data.hyper_spawn_data
        for spawn_id in six.iterkeys(hyper_spawn_data):
            if spawn_id in self._widgets:
                self._widgets[spawn_id].update_nd_status()

    def on_tick(self):
        self.clear_run_timer()
        self.run_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_child_widgets, interval=1)

    def clear_run_timer(self):
        self.run_timer and global_data.game_mgr.get_logic_timer().unregister(self.run_timer)
        self.run_timer = None
        return