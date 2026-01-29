# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/MapBaseUINew.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.uisys.basepanel import BasePanel
import weakref
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.utils.cocos_utils import ccp
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.map.map_widget.MapScaleInterface import CommonMapMark
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gutils import scene_utils
from logic.gutils import map_utils
from logic.gutils import judge_utils
from common.const import uiconst
import cc

class MapBaseUI(BasePanel):
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    TAG = 20210907
    RECONNECT_CHECK_BATTLE = True

    def init(self, parent=None, *arg, **kwargs):
        self.common_marks_animation_flag = False
        super(MapBaseUI, self).init(parent=None, *arg, **kwargs)
        return

    def on_init_panel(self, *args, **kwargs):
        self.scale_event_listener = {}
        self.res_detail_event_listener = {}
        self._timer_running = False
        self._need_place_name = False
        self.map_conf = map_utils.get_map_config()
        self.process_event(True)
        self.init_poison_mgr()
        self.init_map_parameter(self.map_conf)
        self.init_parameters(**kwargs)
        self.init_event()
        self.init_common_marks()
        self.init_client_marks()
        self.panel.sv_map.DisableDefaultMouseEvent()

    def on_init_complete(self):
        pass

    def init_event(self):
        pass

    def init_poison_mgr(self):
        self.poison_mgr = None
        part_battle = self.scene.get_com('PartBattle')
        if not part_battle:
            return
        else:
            poison_mgr = part_battle.get_poison_manager()
            if poison_mgr:
                self.poison_mgr = weakref.ref(poison_mgr)
            return

    def register_on_scale_listener(self, item):
        self.scale_event_listener[id(item)] = item

    def unregister_on_scale_listener(self, item):
        item_id = id(item)
        if item_id in self.scale_event_listener:
            del self.scale_event_listener[item_id]

    def register_on_res_detail_listener(self, item):
        reg_id = id(item)
        self.res_detail_event_listener[reg_id] = item

    def unregister_on_res_detail_listener(self, item):
        item_id = id(item)
        if item_id in self.res_detail_event_listener:
            del self.res_detail_event_listener[item_id]

    def on_finalize_panel(self):
        self.poison_mgr = None
        self.map_nd = None
        self.destroy_widget('map_img')
        self.destroy_widget('route_board')
        self.destroy_widget('airline_widget')
        self.destroy_widget('judge_airline_widget')
        self.destroy_widget('judge_airplane_widget')
        self.destroy_widget('circle_widget')
        self.destroy_widget('fixed_rect_widget')
        self.destroy_widget('move_range_widget')
        self.destroy_widget('player_info_widget')
        self.destroy_widget('poison_direction')
        self.destroy_widget('vehicle_widget')
        self.destroy_widget('enemy_widget')
        self.destroy_widget('mecha_skill_widget')
        self.destroy_widget('occupy_widget')
        self.destroy_widget('muti_occupy_widget')
        self.destroy_widget('train_widget')
        self.destroy_widget('camp_player_info_widget')
        self.destroy_widget('death_entity_info_widget')
        self.destroy_widget('koth_part_info_widget')
        self.destroy_widget('beacon_tower_info_widget')
        self.destroy_widget('death_widget')
        self.destroy_widget('goose_bear_map_widget')
        self.destroy_widget('ffa_entity_info_widget')
        self.destroy_widget('armrace_entity_info_widget')
        self.destroy_widget('zombieffa_entity_info_widget')
        self.destroy_widget('map_place_name_widget')
        self.destroy_widget('granbelm_region_widget')
        self.destroy_widget('gravity_region_widget')
        self.destroy_widget('fire_region_widget')
        self.destroy_widget('start_airline_widget')
        self.destroy_widget('flagbase_pointerline_widget')
        self.destroy_widget('death_blood_bag_widget')
        self.destroy_widget('gulag_area_widget')
        self.process_event(False)
        for key, mark in six.iteritems(self.common_map_marks):
            mark.destroy()

        for key, mark in six.iteritems(self.client_map_marks):
            mark.destroy()

        self.common_map_marks = {}
        self.client_map_marks = {}
        self.distance_map_marks = {}
        super(MapBaseUI, self).on_finalize_panel()
        return

    def init_parameters(self, **kwargs):
        self.map_nd = self.panel.sv_map.GetContainer()
        map_min_scale, map_max_scale = self.map_conf['arrMapScaleRange']
        self.max_map_scale = map_max_scale
        self._res_detail_img_idx = 0
        self.map_pos_range = None
        self.init_map_nd()
        self.min_map_scale = self.get_min_map_scale()
        self.init_map_img(self.map_conf)
        init_map_scale = kwargs.get('scale', self.min_map_scale)
        self.init_map_scale = self.min_map_scale if init_map_scale is None else init_map_scale
        self.cur_map_scale = self.init_map_scale or 1
        self.init_drawboard()
        self.init_airline()
        self.player_info_widget = None
        self.init_player_widget()
        if scene_utils.is_circle_poison():
            self.init_circle()
            self.init_circle_direction()
        if scene_utils.is_fixed_rect_poison():
            self.init_fixed_rect()
        self.init_vehicle_widget()
        self.init_enemy_widget()
        self.init_mecha_skill_widget()
        self.init_occupy_widget()
        self.init_mutioccupy_widget()
        self.init_train_widget()
        self.init_death_widget()
        self.init_goose_bear_map_widget()
        self.init_death_player_widget()
        self.init_koth_part_widget()
        self.init_ffa_player_widget()
        self.init_armrace_player_widget()
        self.init_zombieffa_player_widget()
        self.init_beacon_tower_widget()
        self.init_map_place_name_widget()
        self.init_granbelm_region_widget()
        self.init_gravity_region_widget()
        self.init_fire_region_widget()
        self.init_judge_airline_widget()
        self.init_death_blood_bag_widget()
        self.init_gulag_area_widget()
        self.try_init_judge_airplane_widget()
        self.init_start_airline()
        self.init_flag_base_pointerline()
        self.map_nd.nd_safe_center.setVisible(False)
        self.set_map_scale(self.init_map_scale)
        self.common_map_marks = {}
        self.distance_map_marks = {}
        self.client_map_marks = {}
        return

    def init_map_nd(self):
        map_width, map_height = self.map_conf['arrMapResolution']
        self.map_nd.SetContentSize(map_width, map_height)
        self.map_nd.draw_layer.SetContentSize('100%', '100%')
        self.map_nd.draw_layer.SetPosition('50%', '50%')
        self.map_nd.sp_map_nd.SetContentSize('100%', '100%')
        self.map_nd.sp_map_nd.SetPosition('50%', '50%')
        self.map_nd.nd_scale_up.SetContentSize('100%', '100%')
        self.map_nd.nd_scale_up.SetPosition('50%', '50%')
        self.map_nd.nd_scale_up_details.SetContentSize('100%', '100%')
        self.map_nd.nd_scale_up_details.SetPosition('50%', '50%')
        center_pos = self.map_nd.CalcPosition('50%', '50%')
        self.panel.sv_map.CenterWithPos(center_pos[0], center_pos[1])

    def enable_common_marks_animation(self, flag):
        self.common_marks_animation_flag = flag

    def init_common_marks(self):
        scn = global_data.game_mgr.scene
        part_map = scn.get_com('PartMap')
        common_map_marks = part_map.common_map_marks
        for mark_id, mark_info in six.iteritems(common_map_marks):
            self.add_common_mark(mark_id, mark_info['mark_no'], mark_info['point'], mark_info['is_deep'], mark_info['state'], mark_info['create_timestamp'], mark_info['deep_timestamp'])

        ai_map_marks = part_map.ai_map_marks
        for mark_id, mark_info in six.iteritems(ai_map_marks):
            self.ai_common_mark(mark_id, mark_info['point'], mark_info['state'])

    def init_client_marks(self):
        scn = global_data.game_mgr.scene
        part_map = scn.get_com('PartMap')
        client_map_marks = part_map.client_map_marks
        for mark_id, mark_info in six.iteritems(client_map_marks):
            self.add_client_mark(mark_id, mark_info['mark_no'], mark_info['v3d_pos'])

    def init_normal_map_img(self, map_conf):
        from logic.comsys.map.map_widget.MapImgWidget import MapImgWidget
        map_folder = map_conf['cMapFolder']
        mapCutEdge = map_conf.get('cMapCutEdge', None)
        print('init_normal_map_img', map_conf)
        folder_path = 'gui/ui_res_2/map/' + map_folder
        pic_name_pattern = folder_path + '/' + map_folder + '_%d.png'
        high_res_pic_name = pic_name_pattern % 2048
        mid_res_pic_name = pic_name_pattern % 1024
        low_res_pic_name = pic_name_pattern % 512
        self.map_img = MapImgWidget(self, self.map_nd, [low_res_pic_name, mid_res_pic_name, high_res_pic_name], [
         0.6, 1.2], [1.0, 1.0], cut_edge_list=mapCutEdge)
        return

    def init_map_img(self, map_conf):
        from logic.comsys.map.map_widget.MapImgWidget import MapImgWidget
        if not global_data.game_mode.is_mode_type(game_mode_const.Custom_MapImg):
            self.init_normal_map_img(map_conf)
        else:
            born_data = global_data.game_mode.get_born_data()
            if global_data.death_battle_data.area_id is not None:
                area_data = born_data[global_data.death_battle_data.area_id]
                area_map_img = area_data.get('area_map')
                area_map_rect_info = area_data.get('area_map_rect')
                map_img_scale = area_data.get('map_img_scale', 1.0)
                if area_map_img:
                    lb_x_idx, lb_y_idx, rt_x_idx, rt_y_idx = area_map_rect_info
                    lb_world_pos = ((lb_x_idx - 0.5) * self.TRUNK_SIZE, 0, (lb_y_idx - 0.5) * self.TRUNK_SIZE)
                    rt_world_pos = ((rt_x_idx + 0.5) * self.TRUNK_SIZE, 0, (rt_y_idx + 0.5) * self.TRUNK_SIZE)
                    map_center_pos = (
                     (lb_world_pos[0] + rt_world_pos[0]) / 2.0, 0, (lb_world_pos[2] + rt_world_pos[2]) / 2.0)
                    map_width = (rt_x_idx - lb_x_idx + 1) * self.TRUNK_SIZE
                    map_height = (rt_y_idx - lb_y_idx + 1) * self.TRUNK_SIZE
                    from logic.gutils.map_utils import get_map_uv_ex
                    uv = get_map_uv_ex(map_center_pos)
                    map_pixel_width = self.get_world_distance_in_map(map_width / NEOX_UNIT_SCALE)
                    map_pixel_height = self.get_world_distance_in_map(map_height / NEOX_UNIT_SCALE)
                    area_map_rect_info_in_map = [uv[0], uv[1], map_pixel_width, map_pixel_height]
                    self.map_img = MapImgWidget(self, self.map_nd, [area_map_img, area_map_img], [0.6], [map_img_scale, map_img_scale], area_map_rect_info_in_map)
                    center_pos_x = self.map_pixel_width * uv[0]
                    center_pos_y = self.map_pixel_height * uv[1]
                    range_x = [center_pos_x - map_pixel_width / 2.0 + self.view_dist / 2.0,
                     center_pos_x + map_pixel_width / 2.0 - self.view_dist / 2.0]
                    range_y = [center_pos_y - map_pixel_height / 2.0 + self.view_dist / 2.0,
                     center_pos_y + map_pixel_height / 2.0 - self.view_dist / 2.0]
                    self.map_pos_range = [range_x[0], range_x[1], range_y[0], range_y[1]]
                else:
                    self.init_normal_map_img(map_conf)
            else:
                self.init_normal_map_img(map_conf)
        return

    def center_with_pos(self, x, y):
        if self.map_pos_range:
            x_min, x_max, y_min, y_max = self.map_pos_range
            x = min(max(x, x_min * self.cur_map_scale), x_max * self.cur_map_scale)
            y = min(max(y, y_min * self.cur_map_scale), y_max * self.cur_map_scale)
        self.panel.sv_map.CenterWithPos(x, y)

    def center_with_pos_by_anchor(self, x, y):
        self.panel.sv_map.CenterWithPosByAnchor(x, y)

    def center_map_with_player(self, player_id):
        if player_id is None:
            return
        else:
            from mobile.common.EntityManager import EntityManager
            target = EntityManager.getentity(player_id)
            if not target or not target.logic:
                return
            world_pos = target.logic.ev_g_position() or target.logic.ev_g_model_position()
            if not world_pos:
                return
            cc_pos = self.trans_world_position(world_pos)
            pos_x = cc_pos.x * self.cur_map_scale
            pos_y = cc_pos.y * self.cur_map_scale
            self.center_with_pos(pos_x, pos_y)
            return

    def trans_world_position(self, world_pos):
        from logic.gutils.map_utils import get_map_uv
        uv = get_map_uv(world_pos)
        content_size = self.map_nd.nd_scale_up.GetContentSize()
        from common.utils.cocos_utils import ccp
        return ccp(uv[0] * content_size[0], uv[1] * content_size[1])

    def on_player_setted(self, player):
        pass

    def init_map_parameter(self, map_conf):
        import world
        size = map_conf['arrMapResolution']
        self.map_pixel_height = size[1]
        self.map_pixel_width = size[0]
        scn = world.get_active_scene()
        self.LEFT_TRK_IDX, self.RIGHT_TRK_IDX, self.BOTTOM_TRK_IDX, self.UP_TRK_IDX, self.TRUNK_SIZE = scn.get_safe_scene_map_uv_parameters()
        self.MAP_HEIGHT_DIST = self.TRUNK_SIZE * (self.UP_TRK_IDX - self.BOTTOM_TRK_IDX + 1)
        self.MAP_WIDTH_DIST = self.TRUNK_SIZE * (self.RIGHT_TRK_IDX - self.LEFT_TRK_IDX + 1)
        self.METER_PIXEL_RATIO = self.map_pixel_height / self.MAP_HEIGHT_DIST

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted,
           'scene_observed_player_setted_event': self.on_enter_observe,
           'on_map_res_detail_changed_event': self.on_res_detail_changed,
           'scene_add_mark': self.add_common_mark,
           'scene_del_mark': self.del_common_mark,
           'scene_ai_mark': self.ai_common_mark,
           'scene_deep_mark': self.deep_common_mark,
           'on_scene_poision_mgr_updated': self.init_poison_mgr,
           'draw_airline_event': self._on_draw_airline_event,
           'plane_create_event': self._on_plane_create,
           'plane_destroy_event': self._on_plane_destroy,
           'ob_state_set': self._on_ob_com_inited,
           'update_death_battle_data_area_id': self._on_update_death_battle_data_area_id,
           'player_revived': self._on_player_revived,
           'scene_add_client_mark': self.add_client_mark,
           'scene_del_client_mark': self.del_client_mark,
           'scene_modify_client_mark_pos': self.modify_client_mark_pos
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_update_death_battle_data_area_id(self, area_id):
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
            self.destroy_widget('map_img')
            self.init_map_img(self.map_conf)

    def _on_player_revived(self, sub_id, *args):
        if self.player_info_widget:
            self.player_info_widget.on_player_revived(sub_id)

    def _on_draw_airline_event(self, start_world_pos, end_world_pos):
        if judge_utils.is_ob():
            self._update_judge_airline_widget((start_world_pos, end_world_pos))

    def _update_judge_airline_widget--- This code section failed: ---

 370       0  LOAD_GLOBAL           0  'judge_utils'
           3  LOAD_ATTR             1  'is_ob'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 371      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 374      16  LOAD_FAST             1  'pos'
          19  LOAD_CONST            0  ''
          22  COMPARE_OP            8  'is'
          25  POP_JUMP_IF_FALSE    44  'to 44'

 375      28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             3  'destroy_widget'
          34  LOAD_CONST            1  'judge_airline_widget'
          37  CALL_FUNCTION_1       1 
          40  POP_TOP          
          41  JUMP_FORWARD         91  'to 135'

 378      44  LOAD_GLOBAL           4  'hasattr'
          47  LOAD_GLOBAL           1  'is_ob'
          50  CALL_FUNCTION_2       2 
          53  UNARY_NOT        
          54  POP_JUMP_IF_TRUE     67  'to 67'
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             5  'judge_airline_widget'
          63  UNARY_NOT        
        64_0  COME_FROM                '54'
          64  POP_JUMP_IF_FALSE   119  'to 119'

 379      67  LOAD_CONST            2  ''
          70  LOAD_CONST            3  ('DirectLine',)
          73  IMPORT_NAME           6  'logic.comsys.map.map_widget.MapScaleInterface'
          76  IMPORT_FROM           7  'DirectLine'
          79  STORE_FAST            2  'DirectLine'
          82  POP_TOP          

 380      83  LOAD_FAST             2  'DirectLine'
          86  LOAD_FAST             0  'self'
          89  LOAD_FAST             0  'self'
          92  LOAD_ATTR             8  'map_nd'
          95  LOAD_FAST             0  'self'
          98  LOAD_ATTR             9  'cur_map_scale'
         101  LOAD_CONST            4  'has_tail'
         104  LOAD_GLOBAL          10  'True'
         107  CALL_FUNCTION_259   259 
         110  LOAD_FAST             0  'self'
         113  STORE_ATTR            5  'judge_airline_widget'
         116  JUMP_FORWARD          0  'to 119'
       119_0  COME_FROM                '116'

 382     119  LOAD_FAST             0  'self'
         122  LOAD_ATTR             5  'judge_airline_widget'
         125  LOAD_ATTR            11  'draw'
         128  LOAD_FAST             1  'pos'
         131  CALL_FUNCTION_VAR_0     0 
         134  POP_TOP          
       135_0  COME_FROM                '41'
         135  LOAD_CONST            0  ''
         138  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 50

    def _on_plane_create(self):
        if not judge_utils.is_ob():
            return
        self.try_init_judge_airplane_widget()

    def _on_plane_destroy(self):
        if not judge_utils.is_ob():
            return
        self.destroy_widget('judge_airplane_widget')
        self.destroy_widget('judge_airline_widget')

    def _on_ob_com_inited(self, pid, is_ob):
        self.destroy_widget('death_entity_info_widget')
        self.init_death_player_widget()
        if is_ob:
            self.destroy_widget('route_board')

    def calc_map_scale(self, magnify_value=2.5):
        new_scale = max(min(self.cur_map_scale * magnify_value, self.max_map_scale), self.min_map_scale)
        return new_scale

    def get_world_pos_in_map(self, world_pos):
        if not world_pos:
            return
        else:
            import world
            scn = world.get_active_scene()
            res = scn.get_scene_map_uv_with_checking_script_logic(world_pos.x, world_pos.z)
            if res is not None:
                x, z = res
                return ccp(x * self.map_pixel_width, z * self.map_pixel_height)
            print('no get_world_pos_in_map ->get_scene_map_uv??? ')
            return
            return

    def set_map_scale_with_anchor(self, scale, zoom_anchor_x, zoom_anchor_y):
        self.panel.sv_map.SetContainerScale(scale, zoom_anchor_x, zoom_anchor_y)
        self.cur_map_scale = scale
        self.on_map_scaling(scale)
        for k, v in six.iteritems(self.scale_event_listener):
            v.on_map_scale(scale)

    def set_map_scale(self, scale):
        self.set_map_scale_with_anchor(scale, 0, 0)

    def on_map_scaling(self, map_scale):
        import common.utilities
        nd_name_json = None
        if getattr(self.map_nd.nd_scale_up_details, 'nd_name_json'):
            nd_name_json = self.map_nd.nd_scale_up_details.nd_name_json
        if self.map_nd:
            children = self.map_nd.nd_scale_up.GetChildren()
            for c in children:
                c.setScale(1.0 / map_scale)

            children = self.map_nd.nd_scale_up_details.GetChildren()
            for c in children:
                if c == nd_name_json:
                    continue
                c.setScale(1.0 / map_scale)

            opacity_percent = 1.0 - common.utilities.smoothstep(self.min_map_scale, self.max_map_scale, map_scale) * 0.5
            if nd_name_json:
                children = nd_name_json.nd_name.GetChildren()
                for c in children:
                    c.nd_locate.lab_name.setOpacity(int(opacity_percent * 255))
                    c.setScale(1.0 / map_scale)

        return

    def init_drawboard(self, touch_callback=None):
        if not judge_utils.is_ob():
            from logic.comsys.map.map_widget.MapRouteWidget import MapRouteWidget
            self.route_board = MapRouteWidget(self, self.map_nd.draw_layer, touch_callback)

    def add_common_mark(self, mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp):
        if mark_id in self.common_map_marks:
            self.del_common_mark(mark_id)
        import math3d
        from common.cfg import confmgr
        conf = confmgr.get('mark_data', str(mark_no))
        excluded_battle = conf.get('exclude_battle', ())
        if global_data.game_mode.get_mode_type() in excluded_battle:
            return
        else:
            ui_res1 = conf.get('ui_res1')
            ui_res2 = conf.get('ui_res2')
            state_pics = conf.get('state_pics')
            custom_class = conf.get('custom_class')
            if ui_res1 or ui_res2 or state_pics:
                if not custom_class:
                    common_mark = CommonMapMark(self.map_nd.nd_scale_up_details, mark_no, is_deep, state, parent=self)
                else:

                    def get_cls(cls_path):
                        cls_name = cls_path.split('.')[-1]
                        mod = __import__('logic.comsys.map.map_widget.%s' % cls_path, globals(), locals(), [cls_name])
                        cls = getattr(mod, cls_name, None)
                        return cls

                    cls = get_cls(custom_class)
                    common_mark = cls(self.map_nd.nd_scale_up_details, mark_no, is_deep, state, parent=self)
                v3d_pos = math3d.vector(*point)
                pos = self.get_world_pos_in_map(v3d_pos)
                if not pos:
                    return
                common_mark.set_position(ccp(pos.x, pos.y))
                common_mark.on_map_scale(self.cur_map_scale)
                common_mark.on_set_res_detail_index(self._res_detail_img_idx)
                common_mark.on_set_v3d_pos(v3d_pos)
                self.register_on_res_detail_listener(common_mark)
                self.common_map_marks[mark_id] = common_mark
                if common_mark.get_distance_check():
                    self.distance_map_marks[mark_id] = 1
                    self.start_timer_tick()
                if is_deep:
                    common_mark.check_play_deep(deep_timestamp, need_show_trans_deep_ani=self.common_marks_animation_flag)
                return common_mark
            return

    def start_timer_tick(self, itvl=0.5):
        if self._timer_running:
            return
        self._timer_running = True
        self.panel.stopActionByTag(self.TAG)
        action = cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self._update_mark),
         cc.DelayTime.create(itvl)]))
        action.setTag(self.TAG)
        self.panel.runAction(action)

    def stop_time_tick(self):
        if self.distance_map_marks or self.client_map_marks:
            return
        self._timer_running = False
        self.panel.stopActionByTag(self.TAG)

    def _update_mark(self):
        if not global_data.cam_lplayer:
            return
        pos = global_data.cam_lplayer.ev_g_position()
        if not pos:
            return
        for mark_id in self.distance_map_marks:
            if mark_id not in self.common_map_marks:
                continue
            common_mark = self.common_map_marks[mark_id]
            v3d_pos = common_mark.get_v3d_pos()
            if not v3d_pos:
                continue
            dis_check = common_mark.get_distance_check()
            if not dis_check:
                continue
            dis = (pos - v3d_pos).length
            if dis > dis_check * NEOX_UNIT_SCALE:
                common_mark.set_node_visible(False)
            else:
                common_mark.set_node_visible(True)

        for obj_id, mark_item in six.iteritems(self.client_map_marks):
            if not mark_item.is_follow_model():
                continue
            ent = global_data.battle.get_entity(obj_id)
            if ent and ent.logic and ent.logic.is_valid():
                pos = self.get_world_pos_in_map(ent.logic.ev_g_position())
                if not pos:
                    continue
                mark_item.set_position(ccp(pos.x, pos.y))
                if mark_item.is_show_forward():
                    mark_item.set_forward(ent.logic.ev_g_model_forward())

    def ai_common_mark(self, mark_id, point, state):
        import math3d
        pos = self.get_world_pos_in_map(math3d.vector(*point))
        if mark_id in self.common_map_marks:
            ai_mark = self.common_map_marks[mark_id]
            ai_mark.set_position(ccp(pos.x, pos.y))
        else:
            ai_mark = CommonMapMark(self.map_nd.nd_scale_up_details, 2013, False, 0)
            ai_mark.set_position(ccp(pos.x, pos.y))
            ai_mark.on_map_scale(self.cur_map_scale)
            ai_mark.on_set_res_detail_index(self._res_detail_img_idx)
            self.register_on_res_detail_listener(ai_mark)
            self.common_map_marks[mark_id] = ai_mark
        if ai_mark and ai_mark._nd and ai_mark._nd.lab_num:
            if len(state[0]) > 1:
                ai_mark._nd.lab_num.SetFontSize(16)
            else:
                ai_mark._nd.lab_num.SetFontSize(22)
            ai_mark._nd.lab_num.SetString(state[0])
            ai_mark.set_state(state[1])

    def del_common_mark(self, mark_id):
        if mark_id in self.common_map_marks:
            common_mark = self.common_map_marks[mark_id]
            self.unregister_on_res_detail_listener(common_mark)
            common_mark.destroy()
            del self.common_map_marks[mark_id]
        if mark_id in self.distance_map_marks:
            del self.distance_map_marks[mark_id]
            if not self.distance_map_marks:
                self.stop_time_tick()

    def deep_common_mark(self, mark_id, is_deep, state, deep_timestamp):
        if mark_id in self.common_map_marks:
            common_mark = self.common_map_marks[mark_id]
            common_mark.set_deep(is_deep=is_deep)
            common_mark.set_state(state)
            if is_deep:
                common_mark.check_play_deep(deep_timestamp, need_show_trans_deep_ani=self.common_marks_animation_flag)
            else:
                common_mark.stop_deep()

    def add_client_mark(self, obj_id, mark_no, v3d_pos, require_follow_model=True, kwargs=None):
        kwargs = kwargs or {}
        self.del_client_mark(obj_id)
        import math3d
        from common.cfg import confmgr
        conf = confmgr.get('mark_data', str(mark_no))
        excluded_battle = conf.get('exclude_battle', ())
        if global_data.game_mode.get_mode_type() in excluded_battle:
            return
        else:
            ui_res1 = conf.get('ui_res1')
            ui_res2 = conf.get('ui_res2')
            state_pics = conf.get('state_pics')
            custom_class = conf.get('custom_class')
            if ui_res1 or ui_res2 or state_pics or custom_class:
                if not custom_class:
                    common_mark = CommonMapMark(self.map_nd.nd_scale_up_details, mark_no, False, 0, require_follow_model=require_follow_model, **kwargs)
                else:

                    def get_cls(cls_path):
                        cls_name = cls_path.split('.')[-1]
                        mod = __import__('logic.comsys.map.map_widget.%s' % cls_path, globals(), locals(), [cls_name])
                        cls = getattr(mod, cls_name, None)
                        return cls

                    cls = get_cls(custom_class)
                    common_mark = cls(self.map_nd.nd_scale_up_details, mark_no, False, 0, require_follow_model=require_follow_model, **kwargs)
                pos = self.get_world_pos_in_map(v3d_pos)
                if not pos:
                    return
                common_mark.set_position(ccp(pos.x, pos.y))
                common_mark.on_map_scale(self.cur_map_scale)
                common_mark.on_set_res_detail_index(self._res_detail_img_idx)
                self.register_on_res_detail_listener(common_mark)
                common_mark.on_set_v3d_pos(v3d_pos)
                self.client_map_marks[obj_id] = common_mark
                self.start_timer_tick()
                return common_mark
            return

    def del_client_mark(self, obj_id):
        if obj_id in self.client_map_marks:
            common_mark = self.client_map_marks[obj_id]
            self.unregister_on_res_detail_listener(common_mark)
            common_mark.destroy()
            del self.client_map_marks[obj_id]
            if not self.client_map_marks:
                self.stop_time_tick()

    def modify_client_mark_pos(self, obj_id, v3d_pos):
        if obj_id in self.client_map_marks:
            common_mark = self.client_map_marks[obj_id]
            pos = self.get_world_pos_in_map(v3d_pos)
            if not pos:
                return None
            common_mark.set_position(ccp(pos.x, pos.y))
        return None

    def _get_player_map_locate(self, player_id):
        return self.player_info_widget.get_player_widget(player_id)

    def calc_map_show_scale(self, width_pixel, height_pixel):
        sz = self.panel.sv_map.getContentSize()
        scale = max(float(width_pixel) / sz.width, float(height_pixel) / sz.height)
        return 1.0 / scale

    def get_min_map_scale(self):
        sz = self.panel.sv_map.getContentSize()
        contentsz = self.map_nd.getContentSize()
        return max(sz.width / contentsz.width, sz.height / contentsz.height)

    def get_world_distance_in_map(self, dist):
        return dist * NEOX_UNIT_SCALE * self.METER_PIXEL_RATIO

    def on_enter_observe(self, target):
        self.is_in_spectate = True
        self.on_player_setted(target)

    def init_airline(self):
        from logic.comsys.map.map_widget.MapAirlineWidget import MapAirlineWidget
        self.airline_widget = MapAirlineWidget(self, self.map_nd.draw_layer)

    def init_circle(self, show_effect=True, show_no_signal=False):
        from logic.comsys.map.map_widget.MapPoisonCircleWidget import MapPoisonCircleWidget, MapSignalCircleWidget
        from logic.gcommon.common_utils import battle_utils
        if not battle_utils.is_signal_logic():
            self.circle_widget = MapPoisonCircleWidget(self, self.map_nd, show_effect)
        else:
            self.circle_widget = MapSignalCircleWidget(self, self.map_nd, show_effect, show_no_signal)

    def init_player_widget(self):
        from logic.comsys.map.map_widget.MapPlayerInfoWidget import MapPlayerInfoWidget
        self.player_info_widget = MapPlayerInfoWidget(self, self.map_nd.nd_scale_up_details)

    def init_circle_direction(self):
        from logic.comsys.map.map_widget.MapPoisonDirectionWidget import MapPoisonDirectionWidget
        self.poison_direction = MapPoisonDirectionWidget(self)

    def init_vehicle_widget(self):
        from logic.comsys.map.map_widget.MapVehicleMarkWidget import MapVehicleMarkWidget
        self.vehicle_widget = MapVehicleMarkWidget(self, self.map_nd.nd_scale_up_details)

    def init_fixed_rect(self):
        from logic.comsys.map.map_widget.MapPoisonFixedRectWidget import MapPoisonFixedRectWidget
        self.fixed_rect_widget = MapPoisonFixedRectWidget(self, self.map_nd)

    def init_mecha_skill_widget(self):
        from logic.comsys.map.map_widget.MapMechaSkillInfoWidget import MapMechaSkillInfoWidget
        self.mecha_skill_widget = MapMechaSkillInfoWidget(self, self.map_nd.nd_scale_up_details)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL))
    def init_move_range_rect(self):
        from logic.comsys.map.map_widget.MapMoveRangeRectWidget import MapMoveRangeRectWidget
        self.move_range_widget = MapMoveRangeRectWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_SCORE, game_mode_const.GAME_MODE_NBOMB_SURVIVAL))
    def init_enemy_widget(self):
        from logic.comsys.map.map_widget.MapEnemyInfoWidget import MapEnemyInfoWidget
        self.enemy_widget = MapEnemyInfoWidget(self, self.map_nd.nd_scale_up_details)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_CONTROL,))
    def init_occupy_widget(self):
        from logic.comsys.map.map_widget.MapOccupyInfoWidget import MapOccupyInfoWidget
        self.occupy_widget = MapOccupyInfoWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_MUTIOCCUPY,))
    def init_mutioccupy_widget(self):
        from logic.comsys.map.map_widget.MapMutiOccupyWidget import MapMutiOccupyInfoWidget
        self.muti_occupy_widget = MapMutiOccupyInfoWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_TRAIN,))
    def init_train_widget(self):
        from logic.comsys.map.map_widget.MapTrainWidget import MapTrainWidget
        self.train_widget = MapTrainWidget(self, self.map_nd)

    @execute_by_mode(True, game_mode_const.Show_PlayerIcon)
    def init_death_player_widget(self):
        if judge_utils.is_ob():
            from logic.comsys.map.map_widget.MapCampInfoWidget import MapEntityInfoForJudgeWidget
            self.death_entity_info_widget = MapEntityInfoForJudgeWidget(self, self.map_nd.nd_scale_up_details)
        else:
            from logic.comsys.map.map_widget.MapCampInfoWidget import MapEntityInfoWidget
            self.death_entity_info_widget = MapEntityInfoWidget(self, self.map_nd.nd_scale_up_details)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def init_koth_part_widget(self):
        from logic.comsys.map.map_widget.MapKothPartInfoWidget import MapKothPartInfoWidget
        self.koth_part_info_widget = MapKothPartInfoWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def init_beacon_tower_widget(self):
        from logic.comsys.map.map_widget.MapBeaconTowerMarkWidget import MapBeaconTowerMarkWidget
        self.beacon_tower_info_widget = MapBeaconTowerMarkWidget(self, self.map_nd.nd_scale_up_details)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_DEATHS,))
    def init_death_widget(self):
        from logic.comsys.map.map_widget.MapDeathInfoWidget import MapDeathInfoWidget
        self.death_widget = MapDeathInfoWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GOOSE_BEAR,))
    def init_goose_bear_map_widget(self):
        from logic.comsys.map.map_widget.MapGooseBearMapWidget import MapGooseBearMapWidget
        self.goose_bear_map_widget = MapGooseBearMapWidget(self, self.map_nd)

    @execute_by_mode(True, game_mode_const.GAME_MODE_FFA)
    def init_ffa_player_widget(self):
        from logic.comsys.map.map_widget.MapFFAInfoWidget import MapFFAInfoWidget
        self.ffa_entity_info_widget = MapFFAInfoWidget(self, self.map_nd.nd_scale_up_details)

    @execute_by_mode(True, game_mode_const.GAME_MODE_ARMRACE)
    def init_armrace_player_widget(self):
        from logic.comsys.map.map_widget.MapArmRaceInfoWidget import MapArmRaceInfoWidget
        self.armrace_entity_info_widget = MapArmRaceInfoWidget(self, self.map_nd.nd_scale_up_details)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_ZOMBIE_FFA,))
    def init_zombieffa_player_widget(self):
        from logic.comsys.map.map_widget.MapZombieFFAInfoWidget import MapZombieFFAInfoWidget
        self.zombieffa_entity_info_widget = MapZombieFFAInfoWidget(self, self.map_nd.nd_scale_up_details)

    def init_map_place_name_widget(self):
        if not self._need_place_name:
            return
        from .map_widget.MapPlaceNameInitWidget import MapPlaceNameInitWidget
        self.map_place_name_widget = MapPlaceNameInitWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GRANBELM_SURVIVAL, game_mode_const.GAME_MODE_GRANHACK_SURVIVAL))
    def init_granbelm_region_widget(self):
        from logic.comsys.map.map_widget.MapGranbelmRegionWidget import MapGranbelmRegionWidget
        self.granbelm_region_widget = MapGranbelmRegionWidget(self, self.map_nd)

    @execute_by_mode(True, game_mode_const.Map_GravityRegion)
    def init_gravity_region_widget(self):
        from logic.comsys.map.map_widget.MapGravityRegionWidget import MapGravityRegionWidget
        self.gravity_region_widget = MapGravityRegionWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_FIRE_SURVIVAL,))
    def init_fire_region_widget(self):
        from logic.comsys.map.map_widget.MapFireRegionWidget import MapFireRegionWidget
        self.fire_region_widget = MapFireRegionWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_MAGIC_SURVIVAL,))
    def init_magic_region_widget(self):
        from logic.comsys.map.map_widget.MapMagicRegionWidget import MapMagicRegionWidget
        self.magic_region_widget = MapMagicRegionWidget(self, self.map_nd)

    @execute_by_mode(True, game_mode_const.Map_BloodBagUI)
    def init_death_blood_bag_widget(self):
        from logic.comsys.map.map_widget.MapDeathBloodBagWidget import MapDeathBloodBagWidget
        self.death_blood_bag_widget = MapDeathBloodBagWidget(self, self.map_nd)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_GULAG_SURVIVAL,))
    def init_gulag_area_widget(self):
        from logic.comsys.map.map_widget.MapGulagAreaWidget import MapGulagAreaWidget
        self.gulag_area_widget = MapGulagAreaWidget(self, self.map_nd)

    def init_judge_airline_widget(self):
        if not judge_utils.is_ob():
            return
        if not self.scene:
            return
        lplane = self._get_plane_logic()
        if not lplane:
            return
        if not global_data.battle:
            return
        self._update_judge_airline_widget(global_data.battle.get_airline_pos())

    def _get_plane_logic(self):
        from mobile.common.EntityManager import EntityManager
        planes = EntityManager.get_entities_by_type('Plane')
        if planes:
            if six.PY2:
                plane_ent = next(six.itervalues(planes))
            else:
                plane_ent = next(iter(six.itervalues(planes)))
            if plane_ent.logic:
                return plane_ent.logic
        return None

    def try_init_judge_airplane_widget(self):
        if not judge_utils.is_ob():
            return
        if not hasattr(self, 'judge_airplane_widget') or not self.judge_airplane_widget:
            lplane = self._get_plane_logic()
            if lplane:

                def update_func(MapMoveablePoint_inst):
                    plane_world_pos = None
                    lplane = self._get_plane_logic()
                    if lplane:
                        plane_world_pos = lplane.ev_g_position()
                    MapMoveablePoint_inst.refresh(plane_world_pos)
                    return

                from logic.comsys.map.map_widget.MapScaleInterface import MapMoveablePoint
                self.judge_airplane_widget = MapMoveablePoint(self, self.map_nd, self.cur_map_scale, pic_path='gui/ui_res_2/battle_before/img_map_plane.png', z=100, updater=update_func)

    def on_res_detail_changed(self, map_class_name, img_idx):
        if map_class_name == self.__class__.__name__:
            self._res_detail_img_idx = img_idx
            for k, v in six.iteritems(self.res_detail_event_listener):
                v.on_set_res_detail_index(img_idx)

    @execute_by_mode(True, game_mode_const.GAME_MODE_SURVIVALS)
    def init_start_airline(self):
        from logic.comsys.map.map_widget.MapStartAirlineWidget import MapStartAirlineWidget
        self.start_airline_widget = MapStartAirlineWidget(self)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_FLAG,))
    def init_flag_base_pointerline(self):
        from logic.comsys.map.map_widget.MapFlagBasePointerLineWidget import MapFlagBasePointerLineWidget
        self.flagbase_pointerline_widget = MapFlagBasePointerLineWidget(self)

    def show_signal_tip(self):
        if self.map_nd and self.map_nd.nd_tips:
            self.map_nd.nd_tips.setVisible(True)