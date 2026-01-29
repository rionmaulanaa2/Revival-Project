# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crystal/CrystalMarkUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from common.platform.device_info import DeviceInfo
from logic.gutils import screen_utils
from common.utils import timer
import math
import math3d
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from logic.gcommon.common_const import battle_const as bconst
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import getScreenSize
from logic.gutils.judge_utils import get_player_group_id
from logic.comsys.battle import BattleUtils

class CrystalMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.mark_widgets = {}
        self.mark_widget_buff_cnt = {}
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        for group_id in six.iterkeys(self.mark_widgets):
            self.del_mark_widget(group_id)

        self.mark_widgets = {}
        self.mark_widget_buff_cnt = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'do_update_crystal_hp': self.update_crystal_hp,
           'player_around_crystal_change_event': self.update_crystal_buff_cnt
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_crystal_hp(self, group_id, hp_percent):
        mark_widget = self.mark_widgets.get(group_id)
        if not mark_widget:
            return
        mark_widget.update_left_hp(hp_percent)

    def update_crystal_buff_cnt(self, group_id, player_cnt):
        self.mark_widget_buff_cnt[group_id] = player_cnt
        mark_widget = self.mark_widgets.get(group_id)
        if not mark_widget:
            return
        mark_widget.update_buff_cnt(player_cnt)

    def get_mark_widget(self, group_id):
        return self.mark_widgets.get(group_id)

    def add_mark_widget(self, group_id, cover_id, model):
        self.del_mark_widget(group_id)
        player_group_id = get_player_group_id()
        if player_group_id == group_id:
            mark_type = bconst.CRYSTAL_BATTLE_CRYSTAL_MARK_BLUE
        else:
            mark_type = bconst.CRYSTAL_BATTLE_CRYSTAL_MARK_RED
        self.mark_widgets[group_id] = CrystalMarkWidget(cover_id, mark_type, self.panel)
        self.mark_widgets[group_id].try_bind_model(model)
        self.mark_widgets[group_id].update_buff_cnt(self.mark_widget_buff_cnt.get(group_id, 0))

    def del_mark_widget(self, group_id):
        old_mark = self.mark_widgets.get(group_id)
        old_mark and old_mark.destroy()
        self.mark_widgets[group_id] = None
        return


class CrystalMarkWidget(object):

    def __init__(self, cover_id, mark_type, panel):
        self.cover_id = cover_id
        self.space_node = None
        self.mark_node = None
        self.mark_type = mark_type
        self.parent = panel
        self.is_bind = False
        self.update_timer = None
        self.cover_position = None
        self.screen_size = None
        self.is_can_full_screen = False
        self.scale_data = None
        self.init_width = None
        self.init_height = None
        self.init_widget()
        return

    def init_widget(self):
        self.init_screen_parameter()
        self.init_space_node()

    def init_space_node(self):
        self.space_node = CCUISpaceNode.Create()
        self.mark_node = CommonInfoUtils.create_ui(self.mark_type, self.space_node, False, False)
        self.mark_node.setPosition(0, 0)
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self.mark_node])
        horizontal_margin = 140 * self.parent.getScale()
        vertical_margin = 80 * self.parent.getScale()
        screen_margin = get_scale('40w')
        top_margin = screen_margin
        self.space_node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self.space_node.set_screen_check_margin(0, 0, top_margin, 0)
        self.init_width, self.init_height = self.mark_node.prog_time.GetContentSize()
        self.mark_node.img_timebg.setVisible(False)
        self.mark_node.list_buff.SetInitCount(3)
        for buff_ui_item in self.mark_node.list_buff.GetAllItem():
            buff_ui_item.setVisible(False)

    def init_screen_parameter(self):
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_size = getScreenSize()
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

    def try_bind_model(self, cover_model=None):
        if self.is_bind:
            return
        if not cover_model:
            cover = global_data.battle.get_entity(self.cover_id)
            if not cover:
                self.mark_node.setVisible(False)
                return
            cover_model = cover.logic.ev_g_model()
            if not cover_model:
                self.mark_node.setVisible(False)
                return
        self.cover_position = cover_model.world_position
        self.space_node.bind_model(cover_model, 'fx_glow')
        self.space_node.set_fix_xz(False)
        self.space_node.set_pos_offset(math3d.vector(0, 110, 0))
        self.is_bind = True
        self.mark_node.setVisible(True)
        self.update_timer = global_data.game_mgr.register_logic_timer(self.update_rotation, 0.05, mode=timer.CLOCK)
        global_data.emgr.ask_update_crystal_hp.emit()

    def update_rotation(self):
        camera = global_data.game_mgr.scene.active_camera
        if not camera:
            return
        x, y = camera.world_to_screen(self.cover_position)
        new_x, new_y = screen_utils.limit_pos_in_screen_normal(self.screen_size, self.is_can_full_screen, x, y, self.scale_data)
        in_screen = new_x == x and new_y == y
        target_camera_pos = camera.world_to_camera(self.cover_position)
        angle = math.atan2(target_camera_pos.y, target_camera_pos.x)
        angle = angle * 180 / math.pi
        if angle < 0:
            angle += 360
        self.mark_node.nd_rotate.setRotation(-(angle - 90))
        self.mark_node.nd_rotate.setVisible(not in_screen)

    def update_left_hp(self, left_hp_percent):
        self.mark_node.prog_time.SetContentSize(self.init_width, self.init_height * left_hp_percent)
        hp_percent = int(min(math.ceil(100.0 * left_hp_percent), 100))
        hp_percent_str = '{}%'.format(str(hp_percent))
        self.mark_node.lab_time.SetString(hp_percent_str)
        self.mark_node.img_timebg.setVisible(True)

    def update_buff_cnt(self, player_cnt):
        for idx, buff_ui_item in enumerate(self.mark_node.list_buff.GetAllItem()):
            if idx + 1 <= player_cnt:
                buff_ui_item.setVisible(True)
            else:
                buff_ui_item.setVisible(False)

    def destroy(self):
        if self.update_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_timer)
            self.update_timer = None
        CommonInfoUtils.destroy_ui(self.mark_node)
        self.space_node and self.space_node.Destroy()
        self.space_node = None
        self.mark_node = None
        self.parent = None
        self.is_bind = False
        self.cover_position = None
        self.screen_size = None
        self.is_can_full_screen = False
        self.scale_data = None
        return