# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KingOccupyUI.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref
import math3d
import math
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id
from .KothOccupyProgressUI import KothOccupyProgressUI
from common.utils.ui_utils import get_scale
PIC_ARROW_NONE = 'gui/ui_res_2/battle/koth/arrow_destination_gray.png'
PIC_DESTINATION_NONE = 'gui/ui_res_2/battle/koth/icon_destination_gray.png'
PIC_VX_DESTINATION_NONE = 'gui/ui_res_2/battle/koth/vx_destination_gray.png'
PIC_ARROW = [
 'gui/ui_res_2/battle/koth/arrow_destination_blue.png',
 'gui/ui_res_2/battle/koth/arrow_destination_red.png',
 'gui/ui_res_2/battle/koth/arrow_destination_purple.png']
PIC_DESTINATION = ['gui/ui_res_2/battle/koth/icon_destination_blue.png',
 'gui/ui_res_2/battle/koth/icon_destination_red.png',
 'gui/ui_res_2/battle/koth/icon_destination_purple.png']
PIC_VX_DESTINATION = ['gui/ui_res_2/battle/koth/vx_destination_blue.png',
 'gui/ui_res_2/battle/koth/vx_destination_red.png',
 'gui/ui_res_2/battle/koth/vx_destination_purple.png']
CAMP_PROGRESS_BAR = [
 'gui/ui_res_2/battle/koth/icon_destination_blue.png',
 'gui/ui_res_2/battle/koth/icon_destination_red.png',
 'gui/ui_res_2/battle/koth/icon_destination_purple.png']

class OccupyLocateUI(object):
    TAG_DEFENDING = 19011401
    TAG_FIGHTING = 19011402

    def __init__(self, parent, occupy_id):
        self.parent = parent
        self.occupy_id = occupy_id
        self._nd = global_data.uisystem.load_template_create('battle_koth/koth_destination')
        self.setup_spacenode()
        self.init_parameters()

    def setup_spacenode(self):
        from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
        space_node = CCUISpaceNode.Create()
        space_node.AddChild('', self._nd)
        self._nd.setPosition(0, 0)
        self._space_node = space_node
        margin = get_scale('20w')
        show_margin = get_scale('45w')
        space_node.set_enable_limit_in_screen(True, show_margin, show_margin, show_margin, show_margin)
        space_node.set_screen_check_margin(margin, margin, margin, margin)

    def init_parameters(self):
        self.cfg = global_data.game_mode.get_cfg_data('play_data')
        self.occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        self.occupy_radius = self.occupy_cfg.get(str(self.occupy_id), {}).get('range')
        self.range_center = self.occupy_cfg.get(str(self.occupy_id), {}).get('center')
        x, y, z = self.range_center
        self.range_center_position = math3d.vector(x, y, z)
        self.occupy_position = math3d.vector(*self.occupy_cfg.get(str(self.occupy_id), {}).get('position')) + math3d.vector(0, 36, 0)
        self.max_grap_point = float(self.occupy_cfg.get(str(self.occupy_id), {}).get('grap_point'))
        self._fraction_info = {}
        self._control_camp_id = None
        self._old_control_camp_id = None
        self._old_grap_camp_id = None
        self._grap_camp_id = None
        self._grap_point = 0
        self._old_grap_point = 0
        self._to_circle_dist = 0
        self._nd.setVisible(bool(self.range_center))
        self.screen_size = getScreenSize()
        self.position = None
        self.reward_group_id = None
        self.side = None
        self.control_side = None
        self.group_points = None
        self.update_act = None
        self.camp_ani_status = {}
        self._inside_camp_ids = []
        self.is_in_this_zone = False
        show_text_id = self.occupy_cfg.get(str(self.occupy_id), {}).get('show_text_id', '')
        self._nd.destination.lab_num.SetString(show_text_id)
        self._nd.destination.down.SetDisplayFrameByPath('', PIC_ARROW_NONE)
        self._nd.destination.icon_destination.SetDisplayFrameByPath('', PIC_DESTINATION_NONE)
        self._nd.destination.vx.SetDisplayFrameByPath('', PIC_VX_DESTINATION_NONE)
        self._nd.destination.progress.SetPercentage(0)
        self._nd.destination.PlayAnimation('small')
        self._nd.destination.RecordAnimationNodeState('fighting')
        self._nd.destination.RecordAnimationNodeState('defending')
        self._nd.destination.RecordAnimationNodeState('directing')
        self._has_show_occupy_progess = False
        self._space_node.set_assigned_world_pos(self.occupy_position)
        return

    def on_finalize_panel(self):
        self.update_act and self._nd.stopAction(self.update_act)
        self.update_act = None
        self._nd and self._nd.Destroy()
        self._nd = None
        if self._space_node:
            self._space_node.Destroy()
        self._space_node = None
        return

    def show(self):
        self._space_node.setVisible(True)

    def hide(self):
        self._space_node.setVisible(False)

    def update_wrapper(self):
        self.update_data()
        self.check_visibility()
        if self._nd.isVisible():
            self.update_show()
            self.update_nd_pos()

    def update_nd_pos(self):
        if not self.range_center_position:
            return
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        if not self._nd.isVisible():
            return
        position = self.occupy_position
        is_in_screen = self._space_node.get_is_in_screen()
        if is_in_screen:
            self._nd.destination.nd_direction.setVisible(False)
        else:
            cam_lpos = cam.world_to_camera(position)
            angle = math.atan2(cam_lpos.y, cam_lpos.x)
            angle = angle * 180 / math.pi
            if angle < 0:
                angle += 360
            self._nd.destination.nd_direction.setVisible(True)
            self._nd.destination.nd_direction.setRotation(-(angle + 90))
        self.update_distance()

    def on_tick(self):
        if self.update_act:
            return
        self.update_act = self._nd.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_nd_pos),
         cc.DelayTime.create(0.1)])))

    def update_data(self):
        if not global_data.king_battle_data:
            return
        else:
            occupy_status_data = global_data.king_battle_data.get_occupy_zone_status_data(self.occupy_id)
            if not occupy_status_data:
                return
            self._fraction_info = occupy_status_data.fraction_info
            self._old_control_camp_id = self._control_camp_id
            self._control_camp_id = occupy_status_data.control_camp_id
            old_grap_camp_id = self._grap_camp_id
            self._old_grap_camp_id = old_grap_camp_id
            self._grap_camp_id = occupy_status_data.grap_camp_id
            self._old_grap_point = self._grap_point
            self._grap_point = occupy_status_data.grap_point
            if self._grap_camp_id != old_grap_camp_id:
                self._old_grap_point = 0
            self._inside_camp_ids = six_ex.keys(self._fraction_info)
            cur_in_zone = []
            if global_data.cam_lplayer:
                cur_in_zone = global_data.cam_lplayer.ev_g_cur_in_occupy_zone_list() or []
            is_in_this_occupy_zone = str(self.occupy_id) in cur_in_zone
            self.update_in_out_zone(is_in_this_occupy_zone)
            if self._old_control_camp_id != self._control_camp_id:
                if self._control_camp_id == None:
                    self._nd.destination.down.SetDisplayFrameByPath('', PIC_ARROW_NONE)
                    self._nd.destination.icon_destination.SetDisplayFrameByPath('', PIC_DESTINATION_NONE)
                else:
                    show_side = global_data.king_battle_data.get_side_by_faction_id(self._control_camp_id)
                    self._nd.destination.down.SetDisplayFrameByPath('', PIC_ARROW[show_side])
                    self._nd.destination.icon_destination.SetDisplayFrameByPath('', PIC_DESTINATION[show_side])
            return

    def update_in_out_zone(self, is_in_this_occupy_zone):
        if self.is_in_this_zone:
            if not is_in_this_occupy_zone:
                self._nd.destination.StopAnimation('show')
                self._nd.destination.PlayAnimation('small')
        elif is_in_this_occupy_zone:
            self._nd.destination.StopAnimation('small')
            self._nd.destination.PlayAnimation('show')
        self.is_in_this_zone = is_in_this_occupy_zone

    def check_visibility(self):
        if self.is_my_side_camp() or self.is_in_this_zone:
            self._nd.setVisible(True)
        else:
            self._nd.setVisible(False)

    def update_distance(self):
        if global_data.cam_lctarget:
            pos = global_data.cam_lctarget.ev_g_position()
            if not pos:
                return
            dist = pos - self.occupy_position
            dist.y = 0
            world_dist = dist.length / NEOX_UNIT_SCALE
            to_circle_dist = int(max(world_dist - self.occupy_radius, 0))
            self._nd.destination.lab_distance.SetString(get_text_by_id(18140, {'distance': to_circle_dist}))
            self._to_circle_dist = to_circle_dist

    def update_direction_ani(self, is_in_this_occupy_zone):
        if is_in_this_occupy_zone and not self.is_my_side_camp():
            self._nd.destination.PlayAnimation('directing')
        elif self._nd.destination.IsPlayingAnimation('directing'):
            self._nd.destination.StopAnimation('directing')
            self._nd.destination.RecoverAnimationNodeState('directing')

    def update_on_zone_fight_status(self, is_in_this_occupy_zone):
        if not self.is_my_side_camp() and self.is_in_my_camp_fight_status():
            self._nd.destination.PlayAnimation('fighting')
        else:
            self._nd.destination.StopAnimation('fighting')

    def update_on_zone_defending_status(self):
        if self.is_my_side_camp() and self.is_in_my_camp_fight_status():
            if not self._nd.destination.IsPlayingAnimation('defending'):
                self._nd.destination.PlayAnimation('defending')
        else:
            self._nd.destination.StopAnimation('defending')

    def update_show(self):

        def stop_defending():
            self._nd.destination.StopAnimation('defending')
            self.camp_ani_status['defending'] = False
            self._nd.destination.RecoverAnimationNodeState('defending')

        def stop_fighting():
            self._nd.destination.StopAnimation('fighting')
            self.camp_ani_status['fighting'] = False
            self._nd.destination.RecoverAnimationNodeState('fighting')

        should_play_defend = False
        should_play_fight = False
        if self.is_my_side_camp():
            if self.is_in_my_camp_fight_status():
                if not self._nd.destination.IsPlayingAnimation('defending'):
                    should_play_defend = True
        elif self.is_in_my_camp_fight_status():
            if not self._nd.destination.IsPlayingAnimation('fighting'):
                should_play_fight = True
        if should_play_defend:
            self._nd.stopActionByTag(self.TAG_DEFENDING)
            if self._inside_camp_ids:
                enemy_camp_id = self._inside_camp_ids[0]
                if enemy_camp_id == self._control_camp_id:
                    enemy_camp_id = self._inside_camp_ids[1]
                defend_show_side = global_data.king_battle_data.get_side_by_faction_id(enemy_camp_id)
                self._nd.destination.vx.SetDisplayFrameByPath('', PIC_VX_DESTINATION[defend_show_side])
            else:
                self._nd.destination.vx.SetDisplayFrameByPath('', PIC_VX_DESTINATION_NONE)
            self._nd.destination.PlayAnimation('defending')
            self.camp_ani_status['defending'] = True
        elif self.camp_ani_status.get('defending') and self._nd.destination.IsPlayingAnimation('defending'):
            self._nd.SetTimeOut(5.0, stop_defending, tag=self.TAG_DEFENDING)
            self.camp_ani_status['defending'] = False
        if should_play_fight:
            self._nd.stopActionByTag(self.TAG_FIGHTING)
            self._nd.destination.PlayAnimation('fighting')
            self.camp_ani_status['fighting'] = True
        elif self.camp_ani_status.get('fighting') and self._nd.destination.IsPlayingAnimation('fighting'):
            self._nd.SetTimeOut(5.0, stop_fighting, tag=self.TAG_FIGHTING)
            self.camp_ani_status['fighting'] = False
        self.update_direction_ani(self.is_in_this_zone)
        self.update_on_occupying_info()

    def is_my_side_camp(self):
        return self._control_camp_id == global_data.king_battle_data.my_camp_id

    def is_in_my_camp_fight_status(self):
        if global_data.king_battle_data.my_camp_id in self._inside_camp_ids and len(self._inside_camp_ids) >= 2:
            return True
        else:
            return False

    def update_on_occupying_info(self):
        if self._grap_camp_id is not None and self.is_in_this_zone:
            show_grab_camp_id = global_data.king_battle_data.get_side_by_faction_id(self._grap_camp_id)
            if show_grab_camp_id < len(CAMP_PROGRESS_BAR):
                self._nd.destination.progress.SetProgressTexture(CAMP_PROGRESS_BAR[show_grab_camp_id])
            start_percent = self._old_grap_point / self.max_grap_point * 100
            predict_percent = 20
            percent = min(self._grap_point / self.max_grap_point * 100 + predict_percent, 100)
            if self._nd.destination.progress.getPercentage() - start_percent > 20:
                self._nd.destination.progress.SetPercentage(start_percent)
            action = cc.ProgressTo.create(1, percent)
            self._nd.destination.progress.stopAllActions()
            self._nd.destination.progress.runAction(action)
            if self._grap_camp_id in self._fraction_info:
                occuppy_person_num = self._fraction_info.get(self._grap_camp_id, 0)
                item_num = min(occuppy_person_num / 2, 3)
                self._has_show_occupy_progess = True
                KothOccupyProgressUI().set_occupy_info(self._grap_camp_id, start_percent, percent, 1.0, item_num)
        elif self._has_show_occupy_progess:
            KothOccupyProgressUI().end_occupy_progress()
            self._nd.destination.progress.stopAllActions()
            self._nd.destination.progress.SetPercentage(0)
            self._has_show_occupy_progess = False
        return

    def get_show_camp_pic(self, show_camp_id):
        if show_camp_id in CAMP_PROGRESS_BAR:
            progress_bar = CAMP_PROGRESS_BAR[show_camp_id]
        else:
            progress_bar = 'gui/ui_res_2/battle/koth/bar_normal.png'
        return progress_bar


from common.const import uiconst

class KingOccupyUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    ACT_TAG = 19011501

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        for locate_ui in six.itervalues(self.occupy_locate_uis):
            locate_ui and locate_ui.on_finalize_panel()

        self.occupy_locate_uis = {}

    def init_parameters(self):
        self.occupy_locate_uis = {}

    def init_event(self):
        emgr = global_data.emgr
        econf = {'update_camp_occupy_info': self.update_occupy_info,
           'on_be_hit_event': self.on_fight_state,
           'on_hit_other_event': self.on_fight_state,
           'on_observer_fire': self.on_fight_state,
           'on_non_human_observer_fire_event': self.on_fight_state
           }
        emgr.bind_events(econf)

    def on_fight_state(self, *args):
        self.hide()
        self.panel.SetTimeOut(2.0, lambda : self.show(), tag=self.ACT_TAG)

    def do_show_panel(self):
        super(KingOccupyUI, self).do_show_panel()
        for oid, nd_wrapper in six.iteritems(self.occupy_locate_uis):
            nd_wrapper.show()

    def do_hide_panel(self):
        super(KingOccupyUI, self).do_hide_panel()
        for oid, nd_wrapper in six.iteritems(self.occupy_locate_uis):
            nd_wrapper.hide()

    def update_occupy_info(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        occupy_ids = cfg.get('king_point_list', [])
        for occupy_id in occupy_ids:
            if occupy_id not in self.occupy_locate_uis:
                self.occupy_locate_uis[occupy_id] = OccupyLocateUI(self, occupy_id)
                self.occupy_locate_uis[occupy_id].on_tick()
            self.occupy_locate_uis[occupy_id].update_wrapper()