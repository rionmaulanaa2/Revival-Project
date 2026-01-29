# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMap.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.battle_const import MARK_DANGER, MARK_GOTO, MARK_NORMAL, MARK_RES, MARK_TYPE_TO_CLASS, MARK_CLASS_RES, MARK_CLASS_WARNING, MARK_CLASS_CNT, MARK_WAY_MAP, MARK_WAY_QUICK, MARK_WAY_DOUBLE_CLICK
from time import time
import math3d
from logic.gutils.map_utils import get_map_pos_from_world
from logic.gcommon.common_const.battle_const import MARK_CLASS_RES
from logic.gutils import map_utils
from common.utils.timer import CLOCK
from logic.gutils.ui_salog_utils import add_uiclick_add_up_salog

class ComMap(UnitCom):
    BIND_EVENT = {'E_TRY_DRAW_MAP_MARK': 'try_draw_map_mark',
       'E_TRY_DRAW_MAP_ROUTE': 'try_draw_map_route',
       'E_DRAW_MAP_ROUTE': 'sync_draw_map_route',
       'E_DRAW_MAP_SCENE_MARK': 'sync_draw_map_mark',
       'E_CLEAR_SCENE_MARK': 'sync_clear_map_mark',
       'E_CLEAR_ONE_SCENE_MARK': 'sync_clear_one_map_mark',
       'E_DRAW_RAY_MARK': 'sync_draw_ray_mark',
       'E_SET_MARK_REACHED': 'set_mark_reached',
       'G_MARK_REACHED': 'get_mark_reached',
       'E_TRY_CLEAR_SELF_MAP_MARK': '_try_clear_marks',
       'G_DRAWN_MAP_MARK': '_get_drawn_map_mark',
       'G_WARNING_DRAWN_MAP_MARK': '_get_warning_draw_map_mark',
       'G_DRAWN_MAP_ROUTE': '_get_drawn_map_route',
       'G_DRAWN_ROUTE_ID': '_get_cnt_route_id',
       'E_DEATH': 'on_death'
       }

    def __init__(self):
        super(ComMap, self).__init__()
        self._map_marks = {}
        self._map_route = ([], 0)
        self._mark_reached = False
        self._route_id = 0
        self._last_area_id = None
        self._area_check_timer = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMap, self).init_from_dict(unit_obj, bdict)
        self.init_mark_dict = bdict.get('mark_dict', {})
        self.init_route = bdict.get('route', None)
        return

    def on_init_complete(self):
        for _, mark_infos in six.iteritems(self.init_mark_dict):
            for mark_info in mark_infos:
                mark_type, lst_map_pos, extra_args, add_time = mark_info
                if lst_map_pos:
                    v3d_map_pos = math3d.vector(*lst_map_pos) if 1 else None
                    self.send_event('E_DRAW_MAP_MARK', self.unit_obj.id, mark_type, v3d_map_pos, extra_args)
                    self.send_event('E_DRAW_MAP_SCENE_MARK', self.unit_obj.id, mark_type, v3d_map_pos, extra_args)

        if self.init_route:
            self.send_event('E_DRAW_MAP_ROUTE', self.unit_obj.id, self.init_route)
        self.init_mark_dict = None
        self.init_route = None
        self._area_check_timer = global_data.game_mgr.register_logic_timer(self.check_player_area, 3, times=-1, mode=CLOCK)
        return

    def destroy(self):
        self.cancel_area_check_timer()
        self.clear_cur()
        self.send_event('E_CLEAR_SELF_MAP_MARK', self.unit_obj.id)
        self.send_event('E_DRAW_MAP_ROUTE', self.unit_obj.id, [])
        super(ComMap, self).destroy()

    def cancel_area_check_timer(self):
        if self._area_check_timer:
            global_data.game_mgr.unregister_logic_timer(self._area_check_timer)

    def check_player_area(self):
        cur_pos = self.ev_g_position()
        if cur_pos is None:
            return
        else:
            area_id = self.scene.get_scene_area_info(cur_pos.x, cur_pos.z)
            if self._last_area_id != area_id:
                self._last_area_id = area_id
                self.send_event('E_CALL_SYNC_METHOD', 'update_area_id', (area_id,))
            return

    def get_mark_reached(self):
        return self._mark_reached

    def set_mark_reached(self, reached):
        self._mark_reached = reached

    def try_draw_map_mark(self, mark_type, v3d_map_pos=None, extra_args=None, mark_way=MARK_WAY_MAP):
        if self.is_unit_obj_type('LAvatar'):
            if mark_way == MARK_WAY_MAP:
                add_uiclick_add_up_salog('located_cnt', 'MARK_WAY_MAP')
            elif mark_way == MARK_WAY_DOUBLE_CLICK:
                add_uiclick_add_up_salog('located_cnt', 'MARK_WAY_DOUBLE_CLICK')
            else:
                add_uiclick_add_up_salog('located_cnt', 'MARK_WAY_QUICK')
        mark_cls = MARK_TYPE_TO_CLASS.get(mark_type)
        lst_map_pos = (v3d_map_pos.x, v3d_map_pos.y, v3d_map_pos.z) if v3d_map_pos else None
        self.send_event('E_CALL_SYNC_METHOD', 'draw_map_mark', (mark_type, lst_map_pos, extra_args, mark_way))
        from logic.gcommon.common_utils import parachute_utils
        if self.sd.ref_parachute_stage in (parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_PLANE):
            follow_id, c_name = self.ev_g_parachute_follow_target(True)
            if follow_id:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                global_data.game_mgr.show_tip(get_text_by_id(13057, {'playername': c_name}))
        return

    def sync_draw_map_mark(self, unit_id, mark_type, v3d_map_pos, extra_args=None):
        if mark_type is not None:
            self.draw_map_mark(mark_type, v3d_map_pos, extra_args)
        return

    def sync_draw_ray_mark(self, unit_id, mark_type, v3d_map_pos):
        map_pos = get_map_pos_from_world(v3d_map_pos)
        if map_pos and mark_type is not None:
            t_map_pos = [
             map_pos.x, map_pos.y]
            self.draw_map_mark(mark_type, v3d_map_pos)
        return

    def save_mark_cache(self, mark_type, v3d_map_pos, extra_args=None):
        map_pos = get_map_pos_from_world(v3d_map_pos)
        if not map_pos:
            return
        map_pos = (
         map_pos.x, map_pos.y)
        self._mark_reached = False
        mark_cls = MARK_TYPE_TO_CLASS.get(mark_type)
        if mark_cls not in self._map_marks:
            self._map_marks[mark_cls] = []
        mark_dict = {'pos': map_pos,'type': mark_type,'v3d_map_pos': v3d_map_pos,'extra_args': extra_args}
        self._map_marks[mark_cls].append(mark_dict)
        return mark_dict

    def draw_map_mark(self, mark_type, v3d_map_pos, extra_args=None):
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            return
        mark_dict = self.save_mark_cache(mark_type, v3d_map_pos, extra_args)
        if not self.scene:
            return
        mark_dict and self.do_draw(mark_dict)

    def try_draw_map_route(self, t_points):
        self.send_event('E_DRAW_MAP_ROUTE', self.unit_obj.id, t_points)
        self.send_event('E_CALL_SYNC_METHOD', 'draw_map_route', (self.unit_obj.id, t_points))

    def sync_draw_map_route(self, unit_id, t_points):
        if t_points:
            from logic.gcommon.common_utils.local_text import get_text_by_id
            self._map_route = (
             t_points, time())
            if global_data.cam_lplayer:
                cam_player = global_data.cam_lplayer
                if self.unit_obj.id != cam_player.id and cam_player.ev_g_is_groupmate(self.unit_obj.id):
                    global_data.player.logic.send_event('E_SHOW_MESSAGE', get_text_by_id(16025))
        else:
            self._map_route = ([], time())

    def _try_clear_marks(self):
        self.send_event('E_CALL_SYNC_METHOD', 'clear_marks', ())

    def sync_clear_map_mark(self):
        self.clear_cur()

    def sync_clear_one_map_mark(self, mark_cls):
        mark_list = self._map_marks.get(mark_cls, [])
        if len(mark_list) == 0:
            return
        mark_dict = self._map_marks[mark_cls].pop(0)
        if not self._map_marks[mark_cls]:
            del self._map_marks[mark_cls]
        self.clear_cur_by_type(mark_dict.get('type'))

    def reset(self):
        pass

    def _get_drawn_map_mark(self):
        return self._map_marks

    def _get_warning_draw_map_mark(self):
        mark_infos = self._map_marks.get(MARK_CLASS_WARNING, [])
        if mark_infos:
            return mark_infos[0]
        return {}

    def _get_drawn_map_route(self):
        return self._map_route

    def _get_cnt_route_id(self):
        return self._route_id

    def clear_cur_by_type(self, mark_type):
        if mark_type == MARK_GOTO:
            self.send_event('E_CLEAR_SELF_MAP_MARK', self.unit_obj.id)
        global_data.emgr.remove_scene_mark_by_type.emit(self.unit_obj.id, mark_type)

    def on_death(self, *args):
        self.clear_cur()
        self.send_event('E_TRY_DRAW_MAP_ROUTE', [])

    def clear_cur(self, *args):
        self.send_event('E_CLEAR_SELF_MAP_MARK', self.unit_obj.id)
        global_data.emgr.remove_scene_mark.emit(self.unit_obj.id)
        self._map_marks = {}

    def do_draw(self, mark_dict):
        v3d_map_pos = mark_dict['v3d_map_pos']
        map_pos = mark_dict['pos']
        i_type = mark_dict['type']
        extra_args = mark_dict['extra_args']
        if extra_args:
            extra_args['is_init'] = False
        map_utils.add_scene_map_mark(self.unit_obj.id, i_type, v3d_map_pos, extra_args)