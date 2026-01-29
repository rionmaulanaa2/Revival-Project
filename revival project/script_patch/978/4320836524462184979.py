# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapPlayerInfoWidget.py
from __future__ import absolute_import
import six_ex
import six
from logic.comsys.map.map_widget import MapScaleInterface
import math
import math3d
from logic.gcommon.common_const.battle_const import LOCATE_NORMAL, LOCATE_DEAD, LOCATE_RECOURSE, LOCATE_DRIVE, LOCATE_OFFLINE, LOCATE_PARACHUTE, LOCATE_MECHA
from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO
from logic.gutils.item_utils import get_locate_circle_path
from logic.gutils.team_utils import get_teammate_colors, get_teammate_num
from logic.gutils.team_utils import get_mark_pic_path
from logic.gutils.map_utils import get_world_pos_from_map
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
from common.utils.cocos_utils import ccp
from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN, MAP_COL_RED, MAP_COL_YELLOW
from common.uisys.color_table import get_color_val
from common.utils.cocos_utils import ccc3fFromHex
from logic.gcommon.common_utils.parachute_utils import STAGE_PLANE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_NONE
from logic.client.const import game_mode_const
from mobile.common.EntityManager import EntityManager
from common.utils.timer import CLOCK
from time import time
from common.utils.ui_utils import get_vec2_distance_square
from logic.gcommon.common_const.battle_const import MARK_CLASS_WARNING
from logic.gutils import judge_utils
from logic.gcommon.common_const import ui_operation_const as uoc
import cc
from common.utils.time_utils import get_time
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.comsys.battle.NBomb.NBombBattleDefines import CORE_CIRCLE_MAP_FRAME, POWER_CORE_ID_LST
from common.uisys.uielment.CCSprite import CCSprite
MAP_MARK_CACHE = {}
MAP_MINI_MARK_CACHE = {}
DIRECTION_COLOR_DICT = {MAP_COL_BLUE: ccc3fFromHex(get_color_val('#SB')),
   MAP_COL_GREEN: ccc3fFromHex(get_color_val('#DG')),
   MAP_COL_RED: ccc3fFromHex(get_color_val('#SR')),
   MAP_COL_YELLOW: ccc3fFromHex(get_color_val('#SY'))
   }
CAM_PLAYER_UPDATE_INTERVAL = 3
FREEDROP_UPDATE_INTERVAL = 2
OTHER_PLAYER_UPDATE_INTERVAL = 7
NBOMB_EMENY_MARK_ID = 2054
CAMP_MARK_PIC = [
 'gui/ui_res_2/battle/map/icon_revenge_blue.png',
 'gui/ui_res_2/battle/map/icon_revenge_red.png',
 'gui/ui_res_2/battle/map/icon_revenge_purple.png']
LOCATE_PIC = {LOCATE_RECOURSE: 'gui/ui_res_2/battle/map/locate_down.png',
   LOCATE_DEAD: 'gui/ui_res_2/battle/map/locate_dead.png',
   LOCATE_OFFLINE: 'gui/ui_res_2/battle/map/locate_offline.png',
   LOCATE_PARACHUTE: 'gui/ui_res_2/battle/map/locate_grid.png'
   }
LOCATE_TOP_PIC = 'gui/ui_res_2/battle/ffa/icon_ffa_ace.png'
LOCATE_NORMAL_PIC = 'gui/ui_res_2/battle/map/locate_alive.png'

class MapPlayerInfoWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel, parent_nd, inc_mini_map_mark=False):
        super(MapPlayerInfoWidget, self).__init__(parent_nd, panel)
        self.view_range = None
        self.player_ids = []
        self.latest_player_ids = []
        self.unimportant_update_player_ids = []
        self.locate_widgets = {}
        self.death_widgets = []
        self.nbomb_enemy_widgets = []
        self.killer_locate_widget = None
        self._inc_mini_map_mark = inc_mini_map_mark
        from common.uisys.uielment.CCNode import CCNode
        self.timer_nd = CCNode.Create()
        self.parent_nd.AddChild('', self.timer_nd)
        self.timer_nd.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.033),
         cc.CallFunc.create(self.on_update)])))
        self.timer_nd.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(self.on_med_update)])))
        self.timer_nd.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(1),
         cc.CallFunc.create(self.on_slow_update)])))
        self.normal_update_interval = 30
        self.normal_update_count = 0
        self._has_player_ids_changed = False
        self.follow_player_enable = False
        self.update_timer_id_map = []
        self.groupmates = []
        self.colors_info = {}
        self.view_center_in_map = None
        self.cnt_player_pos = None
        self.default_map_content_size = self.map_panel.sv_map.getContentSize()
        self.default_map_inner_size = self.map_panel.sv_map.GetInnerContentSize()
        self.cam_lplayer_id = 0
        self._groupmate_tstmp = 0
        self._show_player_name = False
        self.on_update(True)
        self.on_slow_update()
        self.init_event()
        self.can_rotate_map = global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DEATH, game_mode_const.GAME_MODE_RANDOM_DEATH, game_mode_const.GAME_MODE_FLAG, game_mode_const.GAME_MODE_CROWN, game_mode_const.GAME_MODE_MUTIOCCUPY))
        return

    def set_follow_player_enable(self, enable):
        self.follow_player_enable = enable

    def init_event(self):
        global_data.emgr.update_killer_info += self.update_killer_locate_widget
        global_data.emgr.scene_observed_player_setted_event += self._on_scene_observed_player_setted
        global_data.emgr.judge_global_player_attacking_changed += self.on_player_attacking_changed

    def uninit_event(self):
        global_data.emgr.update_killer_info -= self.update_killer_locate_widget
        global_data.emgr.scene_observed_player_setted_event -= self._on_scene_observed_player_setted
        global_data.emgr.judge_global_player_attacking_changed -= self.on_player_attacking_changed

    def on_player_attacking_changed(self, player_id, is_attacking):
        if not is_attacking:
            return
        if player_id in self.locate_widgets:
            loc_nd = self.locate_widgets[player_id]
            loc_nd and loc_nd.on_player_attacked_state_changed()

    def on_player_revived(self, sub_id):
        locate_wgt = self.get_player_widget(sub_id)
        if locate_wgt is not None:
            locate_wgt.on_revived()
        return

    def force_update(self):
        self.on_slow_update()
        self.on_update(True)

    def on_med_update(self):
        self.unimportant_update_player_ids = list(self.player_ids)

    def on_slow_update(self):
        if not self.map_panel or not self.map_panel._obj.isVisible():
            return
        if judge_utils.is_ob():
            all_player_info = judge_utils.get_all_global_player_info()
            new_player_ids = six_ex.keys(all_player_info)
            new_player_ids = [ pid for pid in new_player_ids if not judge_utils.is_player_dead_or_out(pid) ]
            if global_data.is_in_judge_camera:
                if global_data.player:
                    new_player_ids.append(global_data.player.id)
        else:
            if not global_data.cam_lplayer:
                return
            new_player_ids = global_data.cam_lplayer.ev_g_groupmate()
        if len(self.player_ids) != len(new_player_ids):
            self._has_player_ids_changed = True
        elif sorted(self.player_ids) != sorted(new_player_ids):
            self._has_player_ids_changed = True
        else:
            self._has_player_ids_changed = False
        self.latest_player_ids = new_player_ids
        if global_data.cam_lplayer:
            player_id = global_data.cam_lplayer.id
            self.update_widget_view_center(player_id)
        elif global_data.is_in_judge_camera:
            if global_data.player:
                self.update_widget_view_center(global_data.player.id)
        self.refresh_death_widgets()
        self.update_nbomb_core_enemy_widget()

    def on_update(self, force_update=False):
        if not self.map_panel.isVisible():
            return
        if global_data.cam_lplayer:
            player_id = global_data.cam_lplayer.id
            self.cam_lplayer_id = player_id
        elif global_data.is_in_judge_camera and global_data.player:
            player_id = global_data.player.id
            self.cam_lplayer_id = player_id
        else:
            return
        id_changed = False
        if self._has_player_ids_changed:
            id_changed = self.update_new_player_ids(self.latest_player_ids)
            if id_changed:
                for widget in six.itervalues(self.locate_widgets):
                    widget.on_color_changed()

            else:
                self._has_player_ids_changed = False
        idx = 0
        if self.update_timer_id_map:
            updated_id = self.update_timer_id_map[idx]
            if not id_changed:
                self.locate_widgets[updated_id].on_update()
            else:
                self.locate_widgets[updated_id].on_init_update()
            self.update_timer_id_map.pop(idx)
            self.update_timer_id_map.append(updated_id)
            if updated_id != player_id and player_id in self.locate_widgets:
                self.locate_widgets[player_id].on_update()
        if self.follow_player_enable:
            self.map_follow_player(player_id)
        if self.unimportant_update_player_ids:
            p_id = self.unimportant_update_player_ids.pop()
            if p_id in self.locate_widgets:
                self.locate_widgets[p_id].on_unimportant_update()

    def set_show_player_name(self, enable):
        self._show_player_name = enable
        for pid, locate_widget in six.iteritems(self.locate_widgets):
            locate_widget.set_player_name_show(enable)

    def b_show_player_name(self):
        return self._show_player_name

    def map_follow_player(self, player_id):
        if player_id in self.locate_widgets:
            loc_nd = self.locate_widgets[player_id]
            if not loc_nd.follow_position_changed:
                return
            self.center_map_with_player(player_id)
            loc_nd.follow_position_changed = False

    def update_widget_view_center(self, player_id):
        if player_id in self.locate_widgets:
            loc_nd = self.locate_widgets[player_id]
            pos = loc_nd._nd.getPosition()
            self.view_center_in_map = pos

    def center_map_with_player(self, player_id):
        if player_id in self.locate_widgets:
            loc_nd = self.locate_widgets[player_id]
            pos = loc_nd._nd.getPosition()
            pos_x = pos.x * self.map_panel.cur_map_scale
            pos_y = pos.y * self.map_panel.cur_map_scale
            if self.can_rotate_map and uoc.SMALL_MAP_ROTATE_ENABLE:
                self.map_panel.center_with_pos_by_anchor(pos_x, pos_y)
            else:
                self.map_panel.center_with_pos(pos_x, pos_y)

    def get_player_widget(self, player_id):
        return self.locate_widgets.get(player_id, None)

    def update_new_player_ids(self, new_player_ids):
        old_ids = self.player_ids
        cnt_ids = []
        id_changed = False
        for _old_id in old_ids:
            if _old_id not in new_player_ids:
                self.remove_item(_old_id)
                id_changed = True
            else:
                cnt_ids.append(_old_id)

        for _new_id in new_player_ids:
            if self.add_item(_new_id):
                id_changed = True
                cnt_ids.append(_new_id)
                break

        if id_changed:
            self.groupmates = new_player_ids
            self.colors_info = get_teammate_colors(self.groupmates)
            self.players_num = get_teammate_num(self.groupmates)
        self.player_ids = cnt_ids
        return id_changed

    def remove_item(self, player_id):
        if player_id in self.locate_widgets:
            self.locate_widgets[player_id].destroy()
            del self.locate_widgets[player_id]
            if player_id in self.update_timer_id_map:
                self.update_timer_id_map.remove(player_id)

    def add_item(self, player_id):
        scale = 1
        if player_id not in self.locate_widgets:
            if global_data.game_mode.is_mode_type(game_mode_const.TDM_MapPlayerIcon):
                scale = 0.5
            _cls = MapLocateWidget
            if judge_utils.is_ob():
                if global_data.player and player_id != global_data.player.id:
                    _cls = MapLocateWidgetForJudge
                else:
                    _cls = MapJudgeLocateWidgetForJudge
            locate_widget = _cls(self, self.parent_nd, player_id, scale, inc_mini_map_mark=self._inc_mini_map_mark)
            locate_widget.set_view_range(self.view_range)
            locate_widget.set_player_name_show(self._show_player_name)
            self.locate_widgets[player_id] = locate_widget
            locate_widget.locate_widget_create_callback(player_id)
            self.update_timer_id_map.insert(0, player_id)
            return True
        return False

    def _on_scene_observed_player_setted(self, target):
        self.colors_info = get_teammate_colors(self.groupmates)
        self.players_num = get_teammate_num(self.groupmates)
        if judge_utils.is_ob():
            if target and target.id:
                self.center_map_with_player(target.id)
        for widget in six.itervalues(self.locate_widgets):
            widget.on_color_changed()

        self.refresh_locate_widgets_visible_for_judge()

    def on_map_scale(self, scale):
        pass

    def update_killer_locate_widget(self, kill_id, pos, camp_id):
        if kill_id is None:
            self.destroy_killer_locate_widget()
            return
        else:
            if self.killer_locate_widget and self.killer_locate_widget.kill_id != kill_id:
                self.destroy_killer_locate_widget()
            if not self.killer_locate_widget:
                self.killer_locate_widget = KillerMapMark(self.map_panel.map_nd.nd_scale_up_details, self.map_panel, kill_id)
            self.killer_locate_widget.on_update((pos, camp_id))
            return

    def destroy_killer_locate_widget(self):
        if self.killer_locate_widget:
            self.killer_locate_widget.destroy()
        self.killer_locate_widget = None
        return

    def get_nbomb_core_enemy_ids(self):
        enemy_pos_info = {}
        if not global_data.nbomb_battle_data:
            return enemy_pos_info
        enemy_info = global_data.nbomb_battle_data.get_nbomb_core_enemy_info()
        is_install_nbomb = global_data.nbomb_battle_data.is_install_nbomb()
        if is_install_nbomb:
            return enemy_pos_info
        player_ids = six_ex.keys(enemy_info)
        for player_id in player_ids:
            target = EntityManager.getentity(player_id)
            if not target:
                continue
            ltarget = target.logic
            if not ltarget:
                continue
            info = {'pos': ltarget.ev_g_position() or ltarget.ev_g_model_position(),'player_id': player_id,
               'mark_id': NBOMB_EMENY_MARK_ID,
               'own_config_ids': enemy_info[player_id]
               }
            enemy_pos_info[player_id] = info

        return enemy_pos_info

    @execute_by_mode(True, (game_mode_const.GAME_MODE_NBOMB_SURVIVAL,))
    def update_nbomb_core_enemy_widget(self):
        enemy_pos_info = self.get_nbomb_core_enemy_ids()
        new_nbomb_enemy_widgets = []
        ids = six_ex.keys(enemy_pos_info)
        ids.sort()
        for player_id in ids:
            src_widget = self.get_player_widget(player_id)
            src_widget and src_widget.hide()
            if self.nbomb_enemy_widgets:
                widget = self.nbomb_enemy_widgets.pop(0)
                widget.show()
            else:
                widget = NBombCoreMapMark(self, self.parent_nd, player_id)
            widget.on_update(enemy_pos_info[player_id])
            new_nbomb_enemy_widgets.append(widget)

        for widget in self.nbomb_enemy_widgets:
            widget.hide()

        new_nbomb_enemy_widgets.extend(self.nbomb_enemy_widgets)
        self.nbomb_enemy_widgets = new_nbomb_enemy_widgets

    def destroy_nbomb_enemy_widget(self):
        for widget in self.nbomb_enemy_widgets:
            widget.destroy()

        self.nbomb_enemy_widgets = []

    def destroy(self):
        if self.timer_nd:
            self.timer_nd.stopAllActions()
            self.timer_nd.Destroy()
            self.timer_nd = None
        self.destroy_nbomb_enemy_widget()
        self.update_new_player_ids([])
        self.uninit_event()
        for widget in self.death_widgets:
            widget.destroy()

        self.death_widgets = []
        super(MapPlayerInfoWidget, self).destroy()
        return

    def set_view_range(self, view_range):
        self.view_range = view_range

    def refresh_death_widgets(self):
        if not global_data.cam_lplayer:
            return
        teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
        death_player = {}
        if not teammate_infos:
            return
        for id, info in six.iteritems(teammate_infos):
            if info.get('dead', False):
                death_player[id] = info

        if not death_player:
            return
        new_death_widgets = []
        ids = six_ex.keys(death_player)
        ids.sort()
        for id in ids:
            info = death_player[id]
            widget = self.get_player_widget(id)
            widget and widget.hide()
            if self.death_widgets:
                widget = self.death_widgets.pop(0)
                widget.show()
            else:
                widget = MapLocateDeathWidget(self, self.parent_nd)
            widget.refresh_info(info)
            new_death_widgets.append(widget)

        for widget in self.death_widgets:
            widget.hide()

        new_death_widgets.extend(self.death_widgets)
        self.death_widgets = new_death_widgets

    def set_locate_widgets_visible_for_judge(self, visible):
        if not judge_utils.is_ob():
            return
        ob_target_id = judge_utils.get_ob_target_id()
        if not ob_target_id:
            return
        if global_data.cam_lplayer:
            teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
        else:
            teammate_infos = {}
        for player_id, locate_widget in six.iteritems(self.locate_widgets):
            if visible or player_id == ob_target_id or player_id in teammate_infos:
                locate_widget.show()
            else:
                locate_widget.hide()

    def refresh_locate_widgets_visible_for_judge(self):
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return
        if not judge_utils.is_ob():
            return
        judge_ui = global_data.ui_mgr.get_ui('JudgeObserveUINew')
        if not judge_ui:
            return
        judge_setting_widget = judge_ui.get_judge_setting_widget()
        if not judge_setting_widget:
            return
        hide_others = judge_setting_widget.get_hide_other_locate_widget()
        self.set_locate_widgets_visible_for_judge(not hide_others)


class KillerMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, kill_id):
        super(KillerMapMark, self).__init__(parent_nd)
        self.kill_id = kill_id
        self._nd = global_data.uisystem.load_template_create('map/i_map_loacte_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setScale(1.0 / ctrl_widget.cur_map_scale)

    def on_update(self, data):
        pos, camp_id = data
        pos and self.set_world_position_ex(pos)
        if global_data.king_battle_data:
            camp_data = global_data.king_battle_data.get_camp().get(camp_id)
            side = camp_data.side
        else:
            side = 1
        self._nd.icon_koth_locate.SetDisplayFrameByPath('', CAMP_MARK_PIC[side])


class NBombCoreMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, ctrl_widget, parent_nd, player_id):
        super(NBombCoreMapMark, self).__init__(parent_nd)
        self.player_id = player_id
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_bomb_enemy')
        self.parent_nd.AddChild('', self._nd)
        self._nd.setScale(1.0 / ctrl_widget.map_panel.cur_map_scale)
        self.circle_frame = {}
        self._nd.PlayAnimation('loop')

    def on_update(self, data):
        self.set_world_position(data['pos'])
        self.update_nd_player_yaw(data['player_id'])
        self.update_camp_img(data['mark_id'])
        self.update_circle_frame(data['own_config_ids'])

    def update_circle_frame(self, own_config_ids):
        for config_id in POWER_CORE_ID_LST:
            img_circle = self.circle_frame.get(config_id, None)
            if img_circle:
                img_circle.setVisible(False)

        scales = [
         0.9, 1.1, 1.3]
        idx = 0
        for config_id in POWER_CORE_ID_LST:
            if config_id not in own_config_ids:
                continue
            img_circle = self.circle_frame.get(config_id, None)
            if not img_circle:
                img_circle = CCSprite.Create('', CORE_CIRCLE_MAP_FRAME[config_id])
                img_circle.setAnchorPoint(ccp(0.5, 0.5))
                self._nd.nd_vx.AddChild('', img_circle)
                img_circle.SetPosition('50%', '50%')
                self.circle_frame[config_id] = img_circle
            img_circle.setVisible(True)
            img_circle.setScale(scales[idx])
            idx += 1

        return

    def update_camp_img(self, mark_id):
        from common.cfg import confmgr
        conf = confmgr.get('mark_data', str(mark_id))
        self._nd.bar.SetDisplayFrameByPath('', conf.get('ui_res1'))

    def update_nd_player_yaw(self, target_id):
        is_cam_player = global_data.cam_lplayer and global_data.cam_lplayer.id == target_id and not global_data.is_in_judge_camera
        if is_cam_player:
            yaw = global_data.cam_data.yaw
        else:
            yaw = 0
            target = EntityManager.getentity(target_id)
            if not (target and target.logic):
                return
        ltarget = target.logic
        if ltarget:
            control_target = ltarget.ev_g_control_target()
            if control_target and control_target.logic:
                yaw = control_target.logic.ev_g_yaw()
                model = yaw or control_target.logic.ev_g_model()
                if model:
                    yaw = model.world_transformation.yaw if 1 else 0
        self.on_target_yaw_changed(yaw)

    def on_target_yaw_changed(self, yaw):
        yaw = yaw or 0
        self._nd.nd_dir.setRotation(yaw * 180 / math.pi)


class MapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, locate_widget, include_mini=False):
        super(MapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_mark')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setScale(1.0 / ctrl_widget.map_panel.cur_map_scale)
        self._nd.nd_distance.setVisible(False)
        self.mark_type = None
        self.mark_color = None
        self.cnt_position = None
        self.mark_world_position = None
        self.distance_cache = -100
        self.ditsance_timer = 0
        self._include_mini = include_mini
        if include_mini:
            nd = global_data.uisystem.load_template_create('battle/i_teammate_mark')
            self.parent_nd.AddChild('oov_nd', nd, Z=2)
            nd.setScale(1.0 / ctrl_widget.map_panel.cur_map_scale)
            self._mini_nd = nd
            import weakref
            self._locate_widget_ref = weakref.ref(locate_widget)
        else:
            self._mini_nd = None
            self._locate_widget_ref = None
        return

    def destroy(self):
        if self._mini_nd:
            from common.uisys.uielment.CCNode import CCNode
            if isinstance(self._mini_nd, CCNode):
                self._mini_nd.Destroy()
            else:
                self._mini_nd.removeFromParent()
        self._mini_nd = None
        self._locate_widget_ref = None
        super(MapMark, self).destroy()
        return

    def set_map_mark(self, mark_type, color):
        global MAP_MARK_CACHE
        if self.mark_type == mark_type and self.mark_color == color:
            return
        else:
            pic_path = None
            if (mark_type, color) in MAP_MARK_CACHE:
                pic_path = MAP_MARK_CACHE[mark_type, color]
            else:
                pic_path = get_mark_pic_path(mark_type, color)
                MAP_MARK_CACHE[mark_type, color] = pic_path
            self.mark_color = color
            self.mark_type = mark_type
            self._nd.sp_mark.SetDisplayFrameByPath('', pic_path)
            if self._mini_nd:
                bg_path, icon_path = self._get_mini_pic_paths(mark_type, color)
                self._mini_nd.bar.SetDisplayFrameByPath('', bg_path)
                self._mini_nd.icon.SetDisplayFrameByPath('', icon_path)
            return

    def _get_mini_pic_paths(self, mark_type, color):
        global MAP_MINI_MARK_CACHE
        pic_paths = ('', '')
        if (
         mark_type, color) in MAP_MINI_MARK_CACHE:
            pic_paths = MAP_MINI_MARK_CACHE[mark_type, color]
        else:
            from logic.gutils.team_utils import get_mini_mark_icon_path, get_mini_mark_bg_path
            pic_paths = (
             get_mini_mark_bg_path(color), get_mini_mark_icon_path(mark_type))
            MAP_MINI_MARK_CACHE[mark_type, color] = pic_paths
        return pic_paths

    def update_map_mark(self, mark_type, color, position, distance, is_player=False, in_prepare=False):
        self.set_map_mark(mark_type, color)
        if not (position and self.cnt_position and position.equals(self.cnt_position)):
            self.set_position(position)
            self.cnt_position = position
        is_distance_type = not in_prepare and mark_type in (MARK_GOTO, MARK_NORMAL)
        if is_distance_type and is_player:
            self.update_mark_distance(distance)
        else:
            self._nd.nd_distance.setVisible(False)

    def set_mark_world_position(self, world_pos):
        self.mark_world_position = world_pos
        self.update_mini_mark(world_pos)

    def update_mini_mark(self, world_pos):
        if self._include_mini and self._mini_nd:
            locate_wgt = self._locate_widget_ref() if self._locate_widget_ref else None
            if locate_wgt:
                cc_pos = self.trans_world_position(world_pos)
                is_out_of_boundary, new_cc_cc_pos, rad_in_cc = locate_wgt.check_view_boundary(cc_pos)
                if is_out_of_boundary:
                    self._mini_nd.setVisible(True)
                    self._mini_nd.setPosition(new_cc_cc_pos)
                    self._mini_nd.nd_rotate.setRotation(rad_in_cc * 180.0 / math.pi)
                else:
                    self._mini_nd.setVisible(False)
            else:
                self._mini_nd.setVisible(False)
        return

    def get_mark_world_position(self):
        return self.mark_world_position

    def update_mark_distance(self, distance):
        cnt_time = time()
        new_distance = distance / NEOX_UNIT_SCALE
        if abs(new_distance - self.distance_cache) >= 1 and cnt_time - self.ditsance_timer > 1:
            self.distance_cache = new_distance
            self.ditsance_timer = cnt_time
            nd = self._nd.nd_distance
            nd.setVisible(True)
            nd.lab_distance.SetString('%.0fm' % (distance / NEOX_UNIT_SCALE))


class MapLocateWidget(MapScaleInterface.MapScaleInterface):
    NODE_MARGIN = 24

    def __init__(self, ctrl_widget, parent_nd, target_id, scale=1, inc_mini_map_mark=False):
        super(MapLocateWidget, self).__init__(parent_nd)
        self.view_range = None
        self.view_dir = ccp(0, 1)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_locate')
        if global_data.test_map_locate:
            self._nd.nd_locate.setScale(0.2)
        self._nd.setScale(float(scale) / ctrl_widget.map_panel.cur_map_scale)
        self.ctrl_widget = ctrl_widget
        self._target_id = target_id
        self.locate_type = LOCATE_NORMAL
        self.parent_nd.AddChild('', self._nd, Z=2)
        self.color = None
        self.color_changed = False
        self.circle_path = None
        self.player_num = 0
        self.player_pos = None
        self.update_count = 0
        self.cc_pos = ccp(0, 0)
        self._all_mark_info = {}
        self.is_need_show_light = False
        self.locate_nd_pos_changed_callback = None
        self.mark_nd = {}
        self.mark_direction = None
        self.update_gap = 999
        self._is_nd_out_of_boundary = False
        self._inc_mini_map_mark = inc_mini_map_mark
        self.tm = global_data.game_mgr.get_logic_timer()
        self.hide_timer_id = None
        self.prev_mark_cache = {}
        self.player_parachute_stage = STAGE_NONE
        self.parent_content_size = self.parent_nd.GetContentSize()
        self.follow_position_changed = False
        self.top_player = {}
        self._is_judge = self.is_judge()
        self.init_info()
        self.init_event()
        self.init_show()
        self.init_ui_event()
        self.on_color_changed()
        return

    def show(self):
        super(MapLocateWidget, self).show()
        self._clean_delay_hide_timer()

    def hide(self):
        super(MapLocateWidget, self).hide()
        self._clean_delay_hide_timer()

    def on_init_update(self):
        self.on_update()
        self.on_unimportant_update()

    def on_color_changed(self):
        if self._target_id in self.ctrl_widget.colors_info:
            color_info = self.ctrl_widget.colors_info[self._target_id]
            player_num = self.ctrl_widget.players_num[self._target_id]
            if self.color != color_info:
                self.color = color_info
                self.circle_path = get_locate_circle_path(self.color)
                if not self.is_top_player():
                    self._nd.sp_circle.SetDisplayFrameByPath('', self.circle_path)
                self.player_num = player_num
                self._nd.lab_num.SetString(str(self.player_num))

    def init_show(self):
        if global_data.game_mode.is_mode_type(game_mode_const.TDM_MapPlayerIcon):
            self._nd.sp_locate.setVisible(True)
            self._nd.lab_num.setVisible(False)
            if global_data.player:
                is_spectate_vis = False
                if global_data.player.logic:
                    spectator_id = global_data.player.logic.ev_g_spectate_target_id()
                    is_spectate_vis = spectator_id == self._target_id
                is_vis = global_data.player.id == self._target_id
                self._nd.setVisible(is_vis or is_spectate_vis)
        self._nd.nd_judgement_name.setVisible(False)
        if judge_utils.is_ob():
            group_id = self.get_group_id(self._target_id)
            from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget
            if group_id is not None:
                self._nd.img_team_bg.SetDisplayFrameByPath('', JudgeObservationListWidget.get_team_bg_img_path(group_id, False))
            player_info = judge_utils.get_global_player_info(self._target_id)
            char_name = player_info.get('char_name', '')
            self._nd.lab_name.SetString(char_name)
        return

    def set_player_name_show(self, show):
        self._nd.nd_judgement_name.setVisible(show)

    def init_info(self):
        self._check_visibility()

    def _check_visibility(self, delay_hide=False):
        if self._is_deemed_dead():
            if delay_hide:
                self._delay_hide_locate()
            else:
                self.hide()
        else:
            self.show()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_top_group_info': self.update_top_group_info,
           'on_groupmate_ctrl_target_changed': self.check_nd_type,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_ui_event(self):

        @self._nd.nd_scale.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import judge_utils
            if not judge_utils.is_ob():
                return
            else:
                if self._target_id is not None:
                    judge_utils.try_switch_ob_target(self._target_id)
                return

    def update_top_group_info(self, group_id, soul_data):
        from logic.gutils import judge_utils
        if not judge_utils.is_ob():
            if self._target_id in soul_data and self._target_id not in self.top_player:
                self._nd.sp_circle.SetDisplayFrameByPath('', LOCATE_TOP_PIC)
            elif self._target_id in self.top_player and self._target_id not in soul_data:
                self._nd.sp_circle.SetDisplayFrameByPath('', self.circle_path)
        self.top_player = soul_data

    def check_nd_type(self, target_id):
        if self._target_id != target_id:
            return

    def _on_scene_observed_player_setted(self, target):
        if global_data.game_mode:
            if global_data.game_mode.is_mode_type(game_mode_const.TDM_MapPlayerIcon):
                is_spectate_vis = self._target_id is not None and target is not None and self._target_id == target.id
                is_vis = global_data.player and global_data.player.id == self._target_id
                self._nd.setVisible(is_vis or is_spectate_vis)
        return

    def check_light_widget(self):
        pass

    def check_update_valid(self, target_id):
        if not global_data.cam_lplayer:
            return False
        self.update_gap += 1
        need_update = self.player_parachute_stage in (STAGE_PLANE, STAGE_FREE_DROP)
        update_interval = CAM_PLAYER_UPDATE_INTERVAL if self._target_id == global_data.cam_lplayer.id or need_update else OTHER_PLAYER_UPDATE_INTERVAL
        if self.update_gap >= update_interval:
            self.update_gap = 0
            return True
        return False

    @staticmethod
    def get_group_id(pid):
        p_info = judge_utils.get_global_player_info(pid)
        group_id = p_info.get('group', None)
        return group_id

    def on_update(self):
        if not self.check_update_valid(self._target_id):
            return
        target = EntityManager.getentity(self._target_id)
        if not target:
            return
        target = target.logic
        if not target:
            return
        self.player_pos = target.ev_g_position() or target.ev_g_model_position()
        if self._nd.isVisible():
            is_cam_player = global_data.cam_lplayer and global_data.cam_lplayer.id == self._target_id and not global_data.is_in_judge_camera
            self.follow_position_changed = True
            self.update_nd_player_pos(target.id, is_cam_player)
            self.update_nd_player_yaw(target.id, is_cam_player)
            is_player = global_data.player and global_data.player.id == self._target_id
            if self._all_mark_info and is_player:
                in_prepare = self.player_parachute_stage == STAGE_NONE
                self.update_direction_mark(target, in_prepare, is_player, self.color)

    def on_unimportant_update(self):
        target = EntityManager.getentity(self._target_id)
        if not target:
            teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
            player_info = teammate_infos.get(self._target_id, {})
            color = global_data.cam_lplayer.ev_g_group_color(self._target_id)
            self.init_by_info(player_info, color)
            self.destroy_player_mark()
            return
        target = target.logic
        if not target:
            return
        self.player_parachute_stage = target.share_data.ref_parachute_stage
        if self._nd.isVisible():
            is_cam_player = global_data.cam_lplayer and global_data.cam_lplayer.id == self._target_id and not global_data.is_in_judge_camera
            self.update_light_widget(is_cam_player)
            self.update_nd_type(target)
            self.update_map_locate()
        is_player = global_data.player and global_data.player.id == self._target_id
        self.check_player_mark(target, self.color, is_player)
        if self._is_deemed_dead(target):
            self._delay_hide_locate()

    def check_player_mark--- This code section failed: ---

 969       0  LOAD_GLOBAL           0  'len'
           3  LOAD_FAST             0  'self'
           6  LOAD_ATTR             1  'prev_mark_cache'
           9  CALL_FUNCTION_1       1 
          12  LOAD_CONST            1  50
          15  COMPARE_OP            5  '>='
          18  POP_JUMP_IF_FALSE    33  'to 33'

 970      21  BUILD_MAP_0           0 
          24  LOAD_FAST             0  'self'
          27  STORE_ATTR            1  'prev_mark_cache'
          30  JUMP_FORWARD          0  'to 33'
        33_0  COME_FROM                '30'

 971      33  LOAD_FAST             1  'player'
          36  LOAD_ATTR             2  'ev_g_drawn_map_mark'
          39  CALL_FUNCTION_0       0 
          42  JUMP_IF_TRUE_OR_POP    48  'to 48'
          45  BUILD_MAP_0           0 
        48_0  COME_FROM                '42'
          48  STORE_FAST            4  'all_mark_info'

 972      51  LOAD_FAST             0  'self'
          54  LOAD_ATTR             3  'player_pos'
          57  POP_JUMP_IF_TRUE     64  'to 64'

 973      60  LOAD_CONST            0  ''
          63  RETURN_END_IF    
        64_0  COME_FROM                '57'

 974      64  LOAD_CONST            0  ''
          67  STORE_FAST            5  'cam_pos_without_z'

 975      70  LOAD_GLOBAL           5  'global_data'
          73  LOAD_ATTR             6  'cam_lctarget'
          76  POP_JUMP_IF_FALSE   130  'to 130'

 976      79  LOAD_GLOBAL           5  'global_data'
          82  LOAD_ATTR             6  'cam_lctarget'
          85  LOAD_ATTR             7  'ev_g_position'
          88  CALL_FUNCTION_0       0 
          91  STORE_FAST            5  'cam_pos_without_z'

 977      94  LOAD_FAST             5  'cam_pos_without_z'
          97  POP_JUMP_IF_FALSE   130  'to 130'

 978     100  LOAD_GLOBAL           8  'math3d'
         103  LOAD_ATTR             9  'vector'
         106  LOAD_FAST             5  'cam_pos_without_z'
         109  CALL_FUNCTION_1       1 
         112  STORE_FAST            5  'cam_pos_without_z'

 979     115  LOAD_CONST            2  ''
         118  LOAD_FAST             5  'cam_pos_without_z'
         121  STORE_ATTR           10  'y'
         124  JUMP_ABSOLUTE       130  'to 130'
         127  JUMP_FORWARD          0  'to 130'
       130_0  COME_FROM                '127'

 980     130  LOAD_FAST             0  'self'
         133  LOAD_ATTR            11  '_all_mark_info'
         136  LOAD_FAST             4  'all_mark_info'
         139  COMPARE_OP            2  '=='
         142  POP_JUMP_IF_FALSE   261  'to 261'

 983     145  SETUP_LOOP          109  'to 257'
         148  LOAD_GLOBAL          12  'six'
         151  LOAD_ATTR            13  'itervalues'
         154  LOAD_FAST             0  'self'
         157  LOAD_ATTR            14  'mark_nd'
         160  CALL_FUNCTION_1       1 
         163  GET_ITER         
         164  FOR_ITER             89  'to 256'
         167  STORE_FAST            6  'marks'

 984     170  SETUP_LOOP           80  'to 253'
         173  LOAD_FAST             6  'marks'
         176  GET_ITER         
         177  FOR_ITER             72  'to 252'
         180  STORE_FAST            7  'mark_nd'

 985     183  LOAD_FAST             7  'mark_nd'
         186  LOAD_ATTR            15  'get_mark_world_position'
         189  CALL_FUNCTION_0       0 
         192  STORE_FAST            8  'mark_wpos'

 987     195  LOAD_FAST             8  'mark_wpos'
         198  POP_JUMP_IF_FALSE   177  'to 177'
         201  LOAD_FAST             5  'cam_pos_without_z'
       204_0  COME_FROM                '198'
         204  POP_JUMP_IF_FALSE   177  'to 177'

 988     207  LOAD_FAST             5  'cam_pos_without_z'
         210  LOAD_FAST             8  'mark_wpos'
         213  BINARY_SUBTRACT  
         214  LOAD_ATTR            16  'length'
         217  STORE_FAST            9  'distance'

 989     220  LOAD_FAST             7  'mark_nd'
         223  LOAD_ATTR            17  'update_mark_distance'
         226  LOAD_FAST             9  'distance'
         229  CALL_FUNCTION_1       1 
         232  POP_TOP          

 990     233  LOAD_FAST             7  'mark_nd'
         236  LOAD_ATTR            18  'update_mini_mark'
         239  LOAD_FAST             8  'mark_wpos'
         242  CALL_FUNCTION_1       1 
         245  POP_TOP          
         246  JUMP_BACK           177  'to 177'
         249  JUMP_BACK           177  'to 177'
         252  POP_BLOCK        
       253_0  COME_FROM                '170'
         253  JUMP_BACK           164  'to 164'
         256  POP_BLOCK        
       257_0  COME_FROM                '145'

 991     257  LOAD_CONST            0  ''
         260  RETURN_END_IF    
       261_0  COME_FROM                '142'

 992     261  BUILD_MAP_0           0 
         264  LOAD_FAST             0  'self'
         267  STORE_ATTR           11  '_all_mark_info'

 994     270  SETUP_LOOP          164  'to 437'
         273  LOAD_GLOBAL          12  'six'
         276  LOAD_ATTR            19  'iteritems'
         279  LOAD_FAST             4  'all_mark_info'
         282  CALL_FUNCTION_1       1 
         285  GET_ITER         
         286  FOR_ITER            147  'to 436'
         289  UNPACK_SEQUENCE_2     2 
         292  STORE_FAST           10  'mark_key'
         295  STORE_FAST           11  'mark_infos'

 995     298  LOAD_FAST             0  'self'
         301  LOAD_ATTR            11  '_all_mark_info'
         304  LOAD_ATTR            20  'setdefault'
         307  LOAD_FAST            10  'mark_key'
         310  BUILD_LIST_0          0 
         313  CALL_FUNCTION_2       2 
         316  POP_TOP          

 996     317  SETUP_LOOP          113  'to 433'
         320  LOAD_FAST            11  'mark_infos'
         323  GET_ITER         
         324  FOR_ITER            105  'to 432'
         327  STORE_FAST           12  'mark_dict'

 997     330  BUILD_MAP_0           0 
         333  STORE_FAST           13  'new_mark_info'

 998     336  SETUP_LOOP           70  'to 409'
         339  LOAD_GLOBAL          12  'six'
         342  LOAD_ATTR            19  'iteritems'
         345  LOAD_FAST            12  'mark_dict'
         348  CALL_FUNCTION_1       1 
         351  GET_ITER         
         352  FOR_ITER             53  'to 408'
         355  UNPACK_SEQUENCE_2     2 
         358  STORE_FAST           14  'k'
         361  STORE_FAST           15  'v'

 999     364  LOAD_FAST            15  'v'
         367  LOAD_FAST            13  'new_mark_info'
         370  LOAD_FAST            14  'k'
         373  STORE_SUBSCR     

1000     374  LOAD_FAST            14  'k'
         377  LOAD_CONST            3  'pos'
         380  COMPARE_OP            2  '=='
         383  POP_JUMP_IF_FALSE   352  'to 352'

1001     386  LOAD_GLOBAL          21  'tuple'
         389  LOAD_FAST            15  'v'
         392  CALL_FUNCTION_1       1 
         395  LOAD_FAST            13  'new_mark_info'
         398  LOAD_FAST            14  'k'
         401  STORE_SUBSCR     
         402  JUMP_BACK           352  'to 352'
         405  JUMP_BACK           352  'to 352'
         408  POP_BLOCK        
       409_0  COME_FROM                '336'

1002     409  LOAD_FAST             0  'self'
         412  LOAD_ATTR            11  '_all_mark_info'
         415  LOAD_FAST            10  'mark_key'
         418  BINARY_SUBSCR    
         419  LOAD_ATTR            22  'append'
         422  LOAD_FAST            13  'new_mark_info'
         425  CALL_FUNCTION_1       1 
         428  POP_TOP          
         429  JUMP_BACK           324  'to 324'
         432  POP_BLOCK        
       433_0  COME_FROM                '317'
         433  JUMP_BACK           286  'to 286'
         436  POP_BLOCK        
       437_0  COME_FROM                '270'

1004     437  LOAD_FAST             0  'self'
         440  LOAD_ATTR            23  'player_parachute_stage'
         443  LOAD_GLOBAL          24  'STAGE_NONE'
         446  COMPARE_OP            2  '=='
         449  STORE_FAST           16  'in_prepare'

1005     452  BUILD_MAP_0           0 
         455  STORE_FAST           17  'new_mark_nd'

1006     458  SETUP_LOOP          448  'to 909'
         461  LOAD_GLOBAL          12  'six'
         464  LOAD_ATTR            19  'iteritems'
         467  LOAD_FAST             4  'all_mark_info'
         470  CALL_FUNCTION_1       1 
         473  GET_ITER         
         474  FOR_ITER            431  'to 908'
         477  UNPACK_SEQUENCE_2     2 
         480  STORE_FAST           10  'mark_key'
         483  STORE_FAST           11  'mark_infos'

1007     486  SETUP_LOOP          416  'to 905'
         489  LOAD_FAST            11  'mark_infos'
         492  GET_ITER         
         493  FOR_ITER            408  'to 904'
         496  STORE_FAST           12  'mark_dict'

1008     499  LOAD_FAST            12  'mark_dict'
         502  LOAD_CONST            4  'type'
         505  BINARY_SUBSCR    
         506  STORE_FAST           18  'i_type'

1009     509  LOAD_FAST            18  'i_type'
         512  LOAD_FAST            17  'new_mark_nd'
         515  COMPARE_OP            7  'not-in'
         518  POP_JUMP_IF_FALSE   534  'to 534'

1010     521  BUILD_LIST_0          0 
         524  LOAD_FAST            17  'new_mark_nd'
         527  LOAD_FAST            18  'i_type'
         530  STORE_SUBSCR     
         531  JUMP_FORWARD          0  'to 534'
       534_0  COME_FROM                '531'

1011     534  LOAD_FAST            18  'i_type'
         537  LOAD_FAST             0  'self'
         540  LOAD_ATTR            14  'mark_nd'
         543  COMPARE_OP            6  'in'
         546  POP_JUMP_IF_FALSE   613  'to 613'
         549  LOAD_FAST             0  'self'
         552  LOAD_ATTR            14  'mark_nd'
         555  LOAD_FAST            18  'i_type'
         558  BINARY_SUBSCR    
       559_0  COME_FROM                '546'
         559  POP_JUMP_IF_FALSE   613  'to 613'

1012     562  LOAD_FAST             0  'self'
         565  LOAD_ATTR            14  'mark_nd'
         568  LOAD_FAST            18  'i_type'
         571  BINARY_SUBSCR    
         572  LOAD_ATTR            25  'pop'
         575  LOAD_CONST            2  ''
         578  CALL_FUNCTION_1       1 
         581  STORE_FAST           19  'nd'

1013     584  LOAD_FAST             0  'self'
         587  LOAD_ATTR            14  'mark_nd'
         590  LOAD_FAST            18  'i_type'
         593  BINARY_SUBSCR    
         594  POP_JUMP_IF_TRUE    643  'to 643'

1014     597  LOAD_FAST             0  'self'
         600  LOAD_ATTR            14  'mark_nd'
         603  LOAD_FAST            18  'i_type'
         606  DELETE_SUBSCR    
         607  JUMP_ABSOLUTE       643  'to 643'
         610  JUMP_FORWARD         30  'to 643'

1016     613  LOAD_GLOBAL          26  'MapMark'
         616  LOAD_FAST             0  'self'
         619  LOAD_ATTR            27  'parent_nd'
         622  LOAD_FAST             0  'self'
         625  LOAD_ATTR            28  'ctrl_widget'
         628  LOAD_ATTR             5  'global_data'
         631  LOAD_FAST             0  'self'
         634  LOAD_ATTR            29  '_inc_mini_map_mark'
         637  CALL_FUNCTION_259   259 
         640  STORE_FAST           19  'nd'
       643_0  COME_FROM                '610'

1017     643  LOAD_FAST            17  'new_mark_nd'
         646  LOAD_FAST            18  'i_type'
         649  BINARY_SUBSCR    
         650  LOAD_ATTR            22  'append'
         653  LOAD_FAST            19  'nd'
         656  CALL_FUNCTION_1       1 
         659  POP_TOP          

1019     660  LOAD_FAST            12  'mark_dict'
         663  LOAD_CONST            3  'pos'
         666  BINARY_SUBSCR    
         667  STORE_FAST           20  'pos'

1020     670  LOAD_CONST            0  ''
         673  STORE_FAST           21  'mark_map_pos'

1021     676  LOAD_CONST            0  ''
         679  STORE_FAST           22  'mark_world_pos'

1022     682  LOAD_FAST            20  'pos'
         685  LOAD_FAST             0  'self'
         688  LOAD_ATTR             1  'prev_mark_cache'
         691  COMPARE_OP            6  'in'
         694  POP_JUMP_IF_FALSE   757  'to 757'
         697  LOAD_FAST             0  'self'
         700  LOAD_ATTR             1  'prev_mark_cache'
         703  LOAD_FAST            20  'pos'
         706  BINARY_SUBSCR    
         707  LOAD_CONST            4  'type'
         710  BINARY_SUBSCR    
         711  LOAD_FAST            18  'i_type'
         714  COMPARE_OP            2  '=='
       717_0  COME_FROM                '694'
         717  POP_JUMP_IF_FALSE   757  'to 757'

1023     720  LOAD_FAST             0  'self'
         723  LOAD_ATTR             1  'prev_mark_cache'
         726  LOAD_FAST            20  'pos'
         729  BINARY_SUBSCR    
         730  LOAD_CONST            6  'map_pos'
         733  BINARY_SUBSCR    
         734  STORE_FAST           21  'mark_map_pos'

1024     737  LOAD_FAST             0  'self'
         740  LOAD_ATTR             1  'prev_mark_cache'
         743  LOAD_FAST            20  'pos'
         746  BINARY_SUBSCR    
         747  LOAD_CONST            7  'world_pos'
         750  BINARY_SUBSCR    
         751  STORE_FAST           22  'mark_world_pos'
         754  JUMP_FORWARD         75  'to 832'

1026     757  LOAD_GLOBAL          30  'ccp'
         760  LOAD_FAST            20  'pos'
         763  LOAD_CONST            2  ''
         766  BINARY_SUBSCR    
         767  LOAD_FAST            20  'pos'
         770  LOAD_CONST            8  1
         773  BINARY_SUBSCR    
         774  CALL_FUNCTION_2       2 
         777  STORE_FAST           21  'mark_map_pos'

1027     780  LOAD_GLOBAL          31  'get_world_pos_from_map'
         783  LOAD_FAST            21  'mark_map_pos'
         786  LOAD_FAST             0  'self'
         789  LOAD_ATTR            32  'parent_content_size'
         792  CALL_FUNCTION_2       2 
         795  STORE_FAST           22  'mark_world_pos'

1028     798  BUILD_MAP_3           3 
         801  LOAD_FAST            18  'i_type'
         804  LOAD_CONST            4  'type'
         807  STORE_MAP        
         808  LOAD_FAST            21  'mark_map_pos'
         811  LOAD_CONST            6  'map_pos'
         814  STORE_MAP        
         815  LOAD_FAST            22  'mark_world_pos'
         818  LOAD_CONST            7  'world_pos'
         821  STORE_MAP        
         822  LOAD_FAST             0  'self'
         825  LOAD_ATTR             1  'prev_mark_cache'
         828  LOAD_FAST            20  'pos'
         831  STORE_SUBSCR     
       832_0  COME_FROM                '754'

1029     832  LOAD_FAST             5  'cam_pos_without_z'
         835  LOAD_CONST            0  ''
         838  COMPARE_OP            9  'is-not'
         841  POP_JUMP_IF_FALSE   888  'to 888'

1031     844  LOAD_FAST             5  'cam_pos_without_z'
         847  LOAD_FAST            22  'mark_world_pos'
         850  BINARY_SUBTRACT  
         851  LOAD_ATTR            16  'length'
         854  STORE_FAST            9  'distance'

1032     857  LOAD_FAST            19  'nd'
         860  LOAD_ATTR            33  'update_map_mark'
         863  LOAD_FAST            18  'i_type'
         866  LOAD_FAST             2  'player_color'
         869  LOAD_FAST            21  'mark_map_pos'
         872  LOAD_FAST             9  'distance'
         875  LOAD_FAST             3  'is_player'
         878  LOAD_FAST            16  'in_prepare'
         881  CALL_FUNCTION_6       6 
         884  POP_TOP          
         885  JUMP_FORWARD          0  'to 888'
       888_0  COME_FROM                '885'

1033     888  LOAD_FAST            19  'nd'
         891  LOAD_ATTR            34  'set_mark_world_position'
         894  LOAD_FAST            22  'mark_world_pos'
         897  CALL_FUNCTION_1       1 
         900  POP_TOP          
         901  JUMP_BACK           493  'to 493'
         904  POP_BLOCK        
       905_0  COME_FROM                '486'
         905  JUMP_BACK           474  'to 474'
         908  POP_BLOCK        
       909_0  COME_FROM                '458'

1034     909  LOAD_FAST             0  'self'
         912  LOAD_ATTR            35  'destroy_player_mark'
         915  CALL_FUNCTION_0       0 
         918  POP_TOP          

1035     919  LOAD_FAST            17  'new_mark_nd'
         922  LOAD_FAST             0  'self'
         925  STORE_ATTR           14  'mark_nd'

1036     928  LOAD_FAST             0  'self'
         931  LOAD_ATTR            36  'update_direction_mark'
         934  LOAD_FAST             1  'player'
         937  LOAD_FAST            16  'in_prepare'
         940  LOAD_FAST             3  'is_player'
         943  LOAD_FAST             2  'player_color'
         946  CALL_FUNCTION_4       4 
         949  POP_TOP          
         950  LOAD_CONST            0  ''
         953  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_259' instruction at offset 637

    def update_direction_mark(self, player, in_prepare, is_player, player_color):
        all_mark_info = self._all_mark_info
        cnt_mark_info = all_mark_info.get(MARK_CLASS_WARNING, [])
        if cnt_mark_info:
            cnt_mark_info = cnt_mark_info[0] if 1 else None
            if is_player and not in_prepare and cnt_mark_info and cnt_mark_info['type'] in (MARK_NORMAL, MARK_GOTO):
                if not self.mark_direction:
                    from logic.comsys.map.map_widget.MapMarkDirection import MapMarkDirection
                    self.mark_direction = MapMarkDirection(self.ctrl_widget, DIRECTION_COLOR_DICT[player_color])
                pos = cnt_mark_info['pos']
                if pos in self.prev_mark_cache:
                    map_pos = self.prev_mark_cache[pos]['map_pos']
                else:
                    mark_map_pos = ccp(pos[0], pos[1])
                    map_pos = get_world_pos_from_map(mark_map_pos, self.parent_content_size)
                self.mark_direction.update_direction_pos(player, self._nd.getPosition(), map_pos)
            else:
                self.destroy_player_direction()
        return

    def update_nd_player_yaw(self, target_id, is_cam_player):
        if is_cam_player:
            yaw = global_data.cam_data.yaw
        else:
            yaw = 0
            target = EntityManager.getentity(target_id)
            if not (target and target.logic):
                return
        target = target.logic
        if target:
            control_target = target.ev_g_control_target()
            if control_target and control_target.logic:
                yaw = control_target.logic.ev_g_yaw()
                model = yaw or control_target.logic.ev_g_model()
                if model:
                    yaw = model.world_transformation.yaw if 1 else 0
        if is_cam_player:
            self.on_target_yaw_changed(yaw)
        elif not self._is_nd_out_of_boundary:
            self.on_target_yaw_changed(yaw)

    def update_nd_player_pos(self, target_id, is_cam_player):
        if not self.player_pos:
            return
        self.cc_pos = self.trans_world_position(self.player_pos)
        if self.cc_pos:
            if is_cam_player:
                if self._nd:
                    self._nd.nd_scale.setScale(1.0)
                    self._nd.img_dir.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/locate_dir_jt.png')
                self.set_position(self.cc_pos)
            else:
                is_out_of_boundary, new_pos, new_yaw = self.check_view_boundary(self.cc_pos)
                if is_out_of_boundary:
                    if self._nd:
                        self._is_nd_out_of_boundary = True
                        self._nd.nd_scale.setScale(0.7)
                        self._nd.img_dir.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/locate_dir_outside.png')
                    self.on_target_yaw_changed(new_yaw)
                    self.set_position(new_pos)
                else:
                    if self._nd:
                        self._is_nd_out_of_boundary = False
                        self._nd.nd_scale.setScale(1.0)
                        self._nd.img_dir.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/locate_dir_jt.png')
                    self.set_position(self.cc_pos)

    def is_top_player(self):
        return self._target_id in self.top_player

    def is_judge(self):
        if judge_utils.is_ob():
            if global_data.player:
                return self._target_id == global_data.player.id
        return False

    def update_map_locate(self):
        is_top_player = self.is_top_player()
        if not global_data.game_mode.is_mode_type(game_mode_const.TDM_MapPlayerIcon):
            if self.locate_type in LOCATE_PIC:
                self._nd.sp_locate.setVisible(True and not is_top_player)
                self._nd.sp_locate.SetDisplayFrameByPath('', LOCATE_PIC[self.locate_type])
                self._nd.lab_num.setVisible(False)
            else:
                self._nd.sp_locate.setVisible(False)
                from logic.gutils import judge_utils
                if judge_utils.is_ob():
                    self._nd.lab_num.setVisible(True and not self._is_judge)
                else:
                    self._nd.lab_num.setVisible(True and not is_top_player)
        if self.locate_type == LOCATE_DEAD:
            self._nd.nd_dir.setVisible(False)
        else:
            self._nd.nd_dir.setVisible(True)
            self._nd.img_dir.setVisible(True)

    def update_light_widget(self, is_cam_player):
        vis = False
        if is_cam_player:
            vis = True
        self._nd.light.setVisible(vis)

    def _clean_delay_hide_timer(self):
        if self.hide_timer_id:
            self.tm.unregister(self.hide_timer_id)
        self.hide_timer_id = None
        return

    def destroy(self):
        self._clean_delay_hide_timer()
        self.ctrl_widget = None
        self.destroy_player_mark()
        self.destroy_player_direction()
        self._nd.Destroy()
        self._nd = None
        self.process_event(False)
        super(MapLocateWidget, self).destroy()
        return

    def on_revived(self):
        self._check_visibility()

    def update_nd_position(self, position):
        if not position:
            return
        self.set_world_position(position)

    def on_target_yaw_changed(self, yaw):
        yaw = yaw or 0
        self._nd.nd_dir._obj.setRotation(yaw * 180 / math.pi)

    def set_yaw_visible(self, vis):
        self._nd.nd_dir.setVisible(vis)

    def _is_deemed_dead(self, lplayer=None):
        check_defeated_either = False
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_IMPROVISE):
            check_defeated_either = True
        if lplayer is None:
            teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos() if global_data.cam_lplayer else None
            if teammate_infos:
                player_info = teammate_infos.get(self._target_id, {})
                is_dead = player_info.get('dead', False)
                if is_dead:
                    return True
        unit = None
        if lplayer is None:
            target = EntityManager.getentity(self._target_id)
            if target and target.logic:
                unit = target.logic
        else:
            unit = lplayer
        if unit is not None:
            if check_defeated_either and unit.ev_g_defeated():
                return True
            if unit.ev_g_death():
                return True
        return False

    def update_nd_type(self, player):
        new_type = LOCATE_NORMAL
        parachute_stage = self.player_parachute_stage
        if not player.ev_g_connect_state():
            new_type = LOCATE_OFFLINE
        elif self._is_deemed_dead(player):
            new_type = LOCATE_DEAD
        elif player.ev_g_agony():
            new_type = LOCATE_RECOURSE
        elif parachute_stage in (STAGE_PLANE,):
            new_type = LOCATE_DRIVE
        elif parachute_stage in (STAGE_FREE_DROP, STAGE_PARACHUTE_DROP):
            new_type = LOCATE_PARACHUTE
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
            if new_type == LOCATE_PARACHUTE or global_data.gvg_battle_data.somebody_is_over(player.id):
                new_type = LOCATE_DEAD
        self.locate_type = new_type

    def destroy_player_mark(self):
        for marks in six.itervalues(self.mark_nd):
            for mark_nd in marks:
                mark_nd.destroy()

        self.mark_nd = {}

    def _delay_hide_locate(self):
        if self.hide_timer_id:
            return
        if not self.is_visible():
            return

        def hide_cb():
            self.hide()

        self.hide_timer_id = self.tm.register(func=hide_cb, interval=10, times=1, mode=CLOCK)

    def destroy_player_direction(self):
        if self.mark_direction:
            self.mark_direction.destroy()
            self.mark_direction = None
        return

    def init_by_info(self, info, color):
        dead = info.get('dead', False)
        if dead:
            self.color = color
            self.locate_type = LOCATE_DEAD
            self.update_map_locate()
            self._delay_hide_locate()
        position = info.get('pos', None)
        if position:
            position = math3d.vector(*position)
            self.set_world_position(position)
        return

    def set_view_range(self, view_range):
        self.view_range = view_range

    def check_view_boundary(self, cc_position):
        view_center_in_map = self.ctrl_widget.view_center_in_map
        if not self.view_range or not view_center_in_map or not cc_position:
            return (False, None, None)
        else:
            half_width, half_height = self.view_range
            player_pos = view_center_in_map
            view_left_x = player_pos.x - half_width
            view_right_x = player_pos.x + half_width
            view_upper_y = player_pos.y + half_height
            view_lower_y = player_pos.y - half_height
            if view_left_x <= cc_position.x <= view_right_x and view_lower_y <= cc_position.y <= view_upper_y:
                return (False, None, None)
            margin = MapLocateWidget.NODE_MARGIN
            left_x = view_left_x + margin
            right_x = view_right_x - margin
            upper_y = view_upper_y - margin
            lower_y = view_lower_y + margin
            start_x, start_y = player_pos.x, player_pos.y
            end_x, end_y = cc_position.x, cc_position.y
            x_delta = end_x - start_x
            y_delta = end_y - start_y
            border_x = right_x if x_delta >= 0 else left_x
            bx_delta = border_x - start_x
            x_ratio = bx_delta / x_delta if x_delta != 0 else 0
            border_z = upper_y if y_delta >= 0 else lower_y
            by_delta = border_z - start_y
            z_ratio = by_delta / y_delta if y_delta != 0 else 0
            ratio = min(x_ratio, z_ratio)
            new_position = ccp(start_x + x_delta * ratio, start_y + y_delta * ratio)
            new_position_for_angle = ccp(start_x + x_delta * ratio, start_y + y_delta * ratio)
            new_position_for_angle.subtract(player_pos)
            degree = new_position_for_angle.getAngle(self.view_dir)
            return (
             True, new_position, degree)

    def on_player_attacked_state_changed(self):
        pass

    def locate_widget_create_callback(self, player_id):
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return
        judge_ui = global_data.ui_mgr.get_ui('JudgeObserveUINew')
        if not judge_ui:
            return
        judge_setting_widget = judge_ui.get_judge_setting_widget()
        if not judge_setting_widget:
            return
        hide_others = judge_setting_widget.get_hide_other_locate_widget()
        if not hide_others:
            return
        if not judge_utils.is_ob():
            return
        ob_target_id = judge_utils.get_ob_target_id()
        if not ob_target_id:
            return
        if global_data.cam_lplayer:
            teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
        else:
            teammate_infos = {}
        if player_id != ob_target_id and player_id not in teammate_infos:
            self.hide()


class MapLocateWidgetForJudge(MapLocateWidget):

    def init_info(self):
        super(MapLocateWidgetForJudge, self).init_info()
        self._last_attack_anim_ts = 0

    def on_player_attacked_state_changed(self):
        now = get_time()
        if now - self._last_attack_anim_ts < 1:
            return
        self._nd and self._nd.PlayAnimation('show_locate')
        self._last_attack_anim_ts = now

    def check_update_valid(self, target_id):
        self.update_gap += 1
        pinfo = judge_utils.get_global_player_info(target_id)
        pos = pinfo.get('position', None)
        if pos is None:
            return False
        else:
            if global_data.cam_lplayer:
                cam_id = global_data.cam_lplayer.id
            elif self._is_judge:
                cam_id = self._target_id
            else:
                cam_id = None
            update_interval = CAM_PLAYER_UPDATE_INTERVAL if self._target_id == cam_id else OTHER_PLAYER_UPDATE_INTERVAL
            if self.update_gap >= update_interval:
                self.player_pos = pos
                self.update_gap = 0
                return True
            return False

    def on_update(self):
        pinfo = judge_utils.get_global_player_info(self._target_id)
        is_dead_or_out = pinfo.get('is_dead_or_out', False)
        pos = pinfo.get('position', None)
        if not self.check_update_valid(self._target_id):
            if pos is None:
                self._nd.nd_scale.setVisible(False)
            return
        else:
            if not pinfo:
                info = {'dead': is_dead_or_out,'pos': pos
                   }
                from logic.gcommon.common_const.battle_const import MAP_COL_WHITE
                self.init_by_info(info, MAP_COL_WHITE)
                self.destroy_player_mark()
                self._nd.nd_scale.setVisible(False)
                return
            if pos is not None:
                self._nd.nd_scale.setVisible(True)
            is_ob = judge_utils.is_ob()
            if is_ob:
                if global_data.game_mode and not global_data.game_mode.is_mode_type(game_mode_const.TDM_MapPlayerIcon):
                    group_id = self.get_group_id(self._target_id)
                    self._nd.lab_num.SetString(str(group_id) if group_id is not None else '')
                    from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget
                    if group_id is not None:
                        self._nd.sp_circle.SetDisplayFrameByPath('', JudgeObservationListWidget.get_team_bg_img_path(group_id, True))
            if self._nd.isVisible():
                self.follow_position_changed = True
                is_cam_player = global_data.cam_lplayer and global_data.cam_lplayer.id == self._target_id or self._is_judge
                self.update_light_widget(is_cam_player)
                self.update_map_locate()
                self.update_pos_and_yaw(self._target_id, is_cam_player)
            if is_dead_or_out:
                self._delay_hide_locate()
            return

    def on_unimportant_update(self):
        pass

    def update_pos_and_yaw(self, target_id, is_cam_player):
        pinfo = judge_utils.get_global_player_info(self._target_id)
        if pinfo:
            yaw = pinfo.get('yaw', None)
            if is_cam_player:
                if global_data.cam_lctarget:
                    yaw = global_data.cam_lctarget.ev_g_yaw()
                    if not yaw:
                        model = global_data.cam_lctarget.ev_g_model()
                        if model:
                            yaw = model.world_transformation.yaw if 1 else 0
                if self.player_pos:
                    self.cc_pos = self.trans_world_position(self.player_pos)
                    is_out_of_boundary = False
                    is_out_of_boundary, _, _ = is_cam_player or self.check_view_boundary(self.cc_pos)
                if is_out_of_boundary:
                    if self._nd:
                        self._nd.nd_scale.setVisible(False)
                else:
                    if self._nd:
                        self._nd.nd_scale.setVisible(True)
                        self._nd.nd_scale.setScale(1.0)
                        self._nd.img_dir.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/locate_dir_jt.png')
                    self.update_nd_position(self.player_pos)
                    if yaw is not None:
                        self.set_yaw_visible(True)
                        self.on_target_yaw_changed(yaw)
                    else:
                        self.set_yaw_visible(False)
        return


class MapJudgeLocateWidgetForJudge(MapLocateWidget):

    def on_color_changed(self):
        super(MapJudgeLocateWidgetForJudge, self).on_color_changed()
        if self._is_judge:
            self._nd.sp_circle.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/circle_camera.png')
            self._nd.lab_num.setVisible(False)

    def check_update_valid(self, target_id):
        self.update_gap += 1
        update_interval = CAM_PLAYER_UPDATE_INTERVAL
        if self.update_gap >= update_interval:
            camera = global_data.game_mgr.scene.active_camera
            pos = camera.world_position
            self.player_pos = pos
            self.update_gap = 0
            return True
        return False

    def on_unimportant_update(self):
        pass

    def on_update(self):
        if not self.check_update_valid(self._target_id):
            return
        if self._nd.isVisible():
            is_cam_player = True
            self.follow_position_changed = True
            self.update_nd_player_pos(self._target_id, is_cam_player)
            self.update_nd_player_yaw(self._target_id, is_cam_player)

    def on_target_yaw_changed(self, yaw):
        yaw = yaw or 0
        self._nd.nd_dir._obj.setRotation(yaw * 180 / math.pi)
        self._nd.sp_circle._obj.setRotation(yaw * 180 / math.pi)


class MapLocateDeathWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, ctrl_widget, parent_nd, scale=1):
        super(MapLocateDeathWidget, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_locate')
        self._nd.setScale(float(scale) / ctrl_widget.map_panel.cur_map_scale)
        self.ctrl_widget = ctrl_widget
        self.parent_nd.AddChild('', self._nd, Z=2)

    def init_show(self):
        circle_path = get_locate_circle_path(self.color)
        self._nd.sp_circle.SetDisplayFrameByPath('', circle_path)
        self._nd.sp_locate.setVisible(True)
        self._nd.lab_num.setVisible(False)
        self._nd.nd_judgement_name.setVisible(False)
        self._nd.nd_dir.setVisible(False)
        self._nd.sp_locate.SetDisplayFrameByPath('', LOCATE_PIC[LOCATE_DEAD])
        cc_pos = self.trans_world_position(self.player_pos)
        self.set_position(cc_pos)

    def refresh_info(self, info):
        if not info.get('pos'):
            return
        self.color = info.get('color')
        self.player_pos = math3d.vector(*info.get('pos'))
        self.init_show()