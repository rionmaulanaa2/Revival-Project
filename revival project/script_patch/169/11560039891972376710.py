# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapCampInfoWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.map.map_widget import MapScaleInterface
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.client.const import game_mode_const
import math
import math3d
from logic.gutils import judge_utils
CAMP_MARK_PIC = [
 'gui/ui_res_2/battle/map/icon_map_koth_blue.png',
 'gui/ui_res_2/battle/map/icon_map_koth_red.png',
 'gui/ui_res_2/battle/map/icon_map_koth_purple.png']
DEATH_MY_SIDE = [
 'gui/ui_res_2/battle/map/icon_teammate.png', 'gui/ui_res_2/battle/map/icon_teammate.png']
DEATH_OTHER_SIDE = ['gui/ui_res_2/battle/map/icon_enemy.png', 'gui/ui_res_2/battle/map/icon_enemy.png']
DESTROY_TAG = 10001

class EntityMapMark(MapScaleInterface.MapScaleInterface):
    HIDE_TAG = 10001

    def __init__(self, parent_nd, ctrl_widget, scale=1):
        super(EntityMapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/i_map_loacte_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setScale(scale / ctrl_widget.cur_map_scale)
        self.set_show(False)

    def on_update(self, group_id, data):
        aoi_id, position, is_mecha = data
        x, z = position
        tuple_pos = (x, 0, z)
        self.set_world_position_ex(tuple_pos)
        side = self._get_side(group_id, data)
        if side is not None:
            self._nd.icon_koth_locate.SetDisplayFrameByPath('', self.get_side_pic(side, data))
        self._post_update(group_id, data, side)
        return

    def _post_update(self, group_id, data, side):
        if side == game_mode_const.MY_SIDE and not self._nd.isVisible():
            self.set_show(True)

    def _get_side(self, group_id, data):
        group_born_data = global_data.death_battle_data.born_data.get(group_id, None)
        if group_born_data:
            return group_born_data.side
        else:
            return 0
            return

    def get_side_pic(self, side, data):
        aoi_id, position, is_mecha = data
        pic_idx = is_mecha or 0 if 1 else 1
        if side == game_mode_const.MY_SIDE:
            return DEATH_MY_SIDE[pic_idx]
        else:
            return DEATH_OTHER_SIDE[pic_idx]

    def set_show(self, show):
        self._nd.setVisible(show)

    def show_with_time(self, time):
        self.set_show(True)
        self._nd.stopActionByTag(self.HIDE_TAG)
        self._nd.DelayCallWithTag(time, self.set_show, self.HIDE_TAG, False)


class EntityMapMarkForJudge(EntityMapMark):

    def _get_side(self, group_id, data):
        if not global_data.cam_lplayer:
            return
        else:
            if group_id is None:
                return
            cam_group_id = global_data.cam_lplayer.ev_g_group_id()
            if cam_group_id is None:
                return
            if group_id == cam_group_id:
                return game_mode_const.MY_SIDE
            return game_mode_const.E_ONE_SIDE
            return

    def _post_update(self, group_id, data, side):
        self.set_show(side is not None)
        return


class MapEntityInfoWidget:
    HIDE_TAG = 10001

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.camp_entity_widgets = {}
        self.status_dict = {}
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_group_status_event': self.update_nd_status,
           'campmate_make_damage_event': self.show_hit_map_mark
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for widget in six.itervalues(self.camp_entity_widgets):
            widget.destroy()

        self.camp_entity_widgets = {}
        self.status_dict = {}

    def update_nd_status(self):
        status_lst = global_data.death_battle_data.get_show_group_status()
        self._update_nd_status(status_lst)

    def _update_nd_status(self, status_lst):
        old_uids = six_ex.keys(self.camp_entity_widgets)
        new_uids = []
        scale = 1
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
            scale = 0.5
        for group_id, entity_list in six.iteritems(status_lst):
            for data in entity_list:
                aoi_id = data[0]
                new_uids.append(aoi_id)
                if aoi_id not in self.camp_entity_widgets:
                    widget = self._new_entity_map_mark(self.parent_nd, self.map_panel, scale, group_id, data)
                    self.camp_entity_widgets[aoi_id] = widget
                self.camp_entity_widgets[aoi_id].on_update(group_id, data)

        del_lst = set(old_uids) - set(new_uids)
        for id in del_lst:
            if id in self.camp_entity_widgets:
                self.camp_entity_widgets[id].destroy()
                del self.camp_entity_widgets[id]

    def _new_entity_map_mark(self, parent_nd, map_panel, scale, group_id, data):
        return EntityMapMark(self.parent_nd, self.map_panel, scale)

    def show_hit_map_mark(self, entity):
        if not entity:
            return
        battle = global_data.battle
        if not battle:
            return
        aoi_id = battle.get_entity_aoi_id(entity.unit_obj.id)
        if aoi_id not in self.camp_entity_widgets:
            entity_id = entity.sd.ref_driver_id
            aoi_id = battle.get_entity_aoi_id(entity_id)
            if aoi_id in self.camp_entity_widgets:
                self.camp_entity_widgets[aoi_id].show_with_time(3)
        else:
            self.camp_entity_widgets[aoi_id].show_with_time(3)


class MapEntityInfoForJudgeWidget(MapEntityInfoWidget):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_group_status_for_judge': self.update_nd_status
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _new_entity_map_mark(self, parent_nd, map_panel, scale, group_id, data):
        return EntityMapMarkForJudge(self.parent_nd, self.map_panel, scale)

    def update_nd_status(self):
        status_lst = {}
        if global_data.battle:
            all_player_info = judge_utils.get_all_global_player_info()
            for player_id in all_player_info:
                if global_data.cam_lplayer is not None and global_data.cam_lplayer.id == player_id:
                    continue
                result = self._gen_data(player_id)
                if not result or not result[0]:
                    continue
                group_id, aoi_id, position, is_mecha = (
                 result[1], result[2], result[3], result[4])
                if group_id not in status_lst:
                    status_lst[group_id] = []
                status_lst[group_id].append((aoi_id, position, is_mecha))

        self._update_nd_status(status_lst)
        return

    def _gen_data(self, player_id):
        player_info = judge_utils.get_global_player_info(player_id)
        group_id = player_info.get('group', None)
        if group_id is None:
            return False
        else:
            widget_key = player_id
            aoi_id = widget_key
            position = player_info.get('position', None)
            if position is None:
                return False
            position = (
             position.x, position.z)
            in_mecha = player_info.get('in_mecha', False)
            return (
             True, group_id, aoi_id, position, in_mecha)

    def show_hit_map_mark(self, entity):
        pass