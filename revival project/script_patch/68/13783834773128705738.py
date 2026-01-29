# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/FightLocateUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SCALE_PLATE_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.const import cocos_constant
from common.utils.cocos_utils import cocos_screen_pos_to_cocos_design_pos
import math3d
import weakref
import cc
from logic.gcommon.common_const.battle_const import MARK_RES, MARK_GATHER
from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN, MAP_COL_RED, MAP_COL_YELLOW
from logic.gutils.team_utils import get_mark_pic_path, get_teammate_colors, get_color_pic_path, get_teammate_num
from logic.gutils.item_utils import get_item_name
INIT_TAG = 10000
DESTROY_TAG = 10001
QUALITY_2_COLOR = (
 None, MAP_COL_GREEN, MAP_COL_BLUE, MAP_COL_RED, MAP_COL_YELLOW)
from common.const import uiconst

class FightLocateUI(BasePanel):
    PANEL_CONFIG_NAME = 'map/fight_locate_scene'
    DLG_ZORDER = SCALE_PLATE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    HEIGHT_OFF_SET = math3d.vector(0, 2.0 * NEOX_UNIT_SCALE, 0)
    SCALE_MAX_DIS = 0
    SCALE_MIN_DIS = 1500 * NEOX_UNIT_SCALE
    SCALE_DIS_LEN = SCALE_MIN_DIS - SCALE_MAX_DIS
    SCALE_MAX = 1.0
    SCALE_MIN = 0.5
    OPACITY_RANGE = (255, int(127.5))
    OPACITY_DENOMINATOR = (SCALE_MAX - SCALE_MIN) * (OPACITY_RANGE[0] - OPACITY_RANGE[1])

    def on_init_panel(self, player=None):
        self.panel.img_locate.setVisible(False)
        self.panel.img_locate_02.setVisible(False)
        self.cam = None
        self.player = None
        self.mp_team_marks = {}
        self._timer_running = False
        self.on_player_setted(player)
        self.init_event()
        if self.player:
            self.start_timer_tick()
        return

    def cal_opacity(self, scale):
        scale = max(min(scale - self.SCALE_MIN, 1), 0)
        opacity = scale / FightLocateUI.OPACITY_DENOMINATOR + FightLocateUI.OPACITY_RANGE[1]
        return int(opacity)

    def on_finalize_panel(self):
        eids = six_ex.keys(self.mp_team_marks)
        for eid in eids:
            self.on_del_player_mark(eid)

        global_data.emgr.scene_camera_player_setted_event -= self.on_cam_lplayer_setted
        global_data.emgr.add_scene_mark -= self.on_add_player_mark
        global_data.emgr.remove_scene_mark -= self.on_del_player_mark
        global_data.emgr.remove_scene_mark_by_type -= self.do_del_player_mark_by_type
        self.unbind_event(self.player)

    def init_event(self):
        global_data.cam_lplayer and self.on_player_setted(global_data.cam_lplayer)
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        global_data.emgr.add_scene_mark += self.on_add_player_mark
        global_data.emgr.remove_scene_mark += self.on_del_player_mark
        global_data.emgr.remove_scene_mark_by_type += self.do_del_player_mark_by_type
        self.bind_event(self.player)

    def do_hide_panel(self):
        super(FightLocateUI, self).do_hide_panel()
        self.set_space_mark_visible(False)

    def set_space_mark_visible(self, vis):
        for eid, mark_info in six.iteritems(self.mp_team_marks):
            for mark_type, infos in six.iteritems(mark_info):
                for info in infos:
                    nd, space_node, v3d_pos, extra_args = info
                    space_node.setVisible(vis)

    def do_show_panel(self):
        super(FightLocateUI, self).do_show_panel()
        self.set_space_mark_visible(True)

    def on_cam_lplayer_setted(self):
        global_data.cam_lplayer and self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        if player is None:
            self.close()
        self.player = player
        scn = global_data.game_mgr.scene
        self.cam = weakref.ref(scn.active_camera)
        return

    def bind_event(self, target):
        if target:
            regist_func = target.regist_event
            regist_func('E_DEATH', self.close)

    def unbind_event(self, target):
        if target:
            unregist_func = target.unregist_event
            unregist_func('E_DEATH', self.close)

    def start_timer_tick(self, itvl=0.5):
        if self._timer_running:
            return
        self._timer_running = True
        self.panel.stopActionByTag(cocos_constant.TIMER_ACT_TAG)
        action = cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self._update_pos),
         cc.DelayTime.create(itvl)]))
        action.setTag(cocos_constant.TIMER_ACT_TAG)
        self.panel.runAction(action)

    def on_add_player_mark(self, eid, mark_type, v3d_pos, extra_args=None):
        from logic.gutils.template_utils import get_item_quality
        if not v3d_pos:
            self.do_del_player_mark_by_type(eid, mark_type)
            return
        else:
            if eid in self.mp_team_marks:
                self.do_del_player_mark_by_type(eid, mark_type, v3d_pos)
            group_ids = self.player.ev_g_groupmate()
            if not group_ids:
                return
            if eid not in group_ids:
                return
            player_color = get_teammate_colors(group_ids)[eid] if group_ids else MAP_COL_BLUE
            nd = global_data.uisystem.load_template_create(self.PANEL_CONFIG_NAME)
            nd.setScale(1.0)
            nd.is_play_ani = False
            if mark_type == MARK_RES:
                item_id = extra_args and extra_args.get('item_id', None)
                mark_color = MAP_COL_BLUE
                if item_id is not None:
                    quality = get_item_quality(item_id)
                    quality = min(max(1, quality), len(QUALITY_2_COLOR) - 1)
                    mark_color = QUALITY_2_COLOR[quality]
                path_mark_pic = get_mark_pic_path(mark_type, mark_color)
                nd.nd_locate.setVisible(True)
                path_circle_pic = get_color_pic_path('gui/ui_res_2/battle/map/circle_', player_color)
                mark_index = get_teammate_num(group_ids)[eid]
                nd.sp_circle.SetDisplayFrameByPath(None, path_circle_pic)
                nd.lab_num.SetString(str(mark_index))
            elif mark_type == MARK_GATHER:
                path_mark_pic = 'gui/ui_res_2/battle/map/mark_gather.png'
            else:
                mark_color = player_color
                path_mark_pic = get_mark_pic_path(mark_type, mark_color)
            nd.img_locate.SetDisplayFrameByPath(None, path_mark_pic)
            nd.vx_img_locate.SetDisplayFrameByPath(None, path_mark_pic)
            nd.vx_tubiao.SetDisplayFrameByPath(None, path_mark_pic)
            pos = self.player.ev_g_position()
            if pos:
                dis = (pos - v3d_pos).length
                nd.lab_distance.setString('{:.0f}m'.format(dis / NEOX_UNIT_SCALE))
            space_node = self.setup_nd_space_node(nd, v3d_pos + self.HEIGHT_OFF_SET)
            if eid not in self.mp_team_marks:
                self.mp_team_marks[eid] = {}
            if mark_type not in self.mp_team_marks[eid]:
                self.mp_team_marks[eid][mark_type] = []
            self.mp_team_marks[eid][mark_type].append((nd, space_node, v3d_pos, extra_args))
            space_node.setVisible(self.panel.isVisible())
            self.start_timer_tick()
            self.play_show_ani(nd)
            return

    def setup_nd_space_node(self, nd, v3d_pos):
        from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
        space_node = CCUISpaceNode.Create()
        space_node.AddChild('', nd)
        nd.setPosition(0, 0)
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [nd])

        def vis_callback(last_need_draw, cur_need_draw):
            if nd and nd.isValid():
                nd.setVisible(True if cur_need_draw else False)

        space_node.set_assigned_world_pos(v3d_pos)
        space_node.set_visible_callback(vis_callback)
        return space_node

    def do_del_player_mark_by_type(self, eid, mark_type, v3d_pos=None):
        if eid not in self.mp_team_marks:
            return
        if mark_type not in self.mp_team_marks[eid]:
            return
        for info in self.mp_team_marks[eid][mark_type]:
            nd, space_node, pos, _ = info
            if v3d_pos and v3d_pos == pos:
                return
            space_node.Destroy()

        del self.mp_team_marks[eid][mark_type]
        if not self.mp_team_marks[eid]:
            del self.mp_team_marks[eid]

    def on_del_player_mark(self, eid):
        if eid in self.mp_team_marks:
            for infos in six.itervalues(self.mp_team_marks[eid]):
                for info in infos:
                    nd, space_node, _, _ = info
                    space_node.Destroy()

            del self.mp_team_marks[eid]
        if not self.mp_team_marks:
            self.close()

    def _update_pos(self):
        if not self.cam:
            return
        else:
            cam = self.cam()
            if not cam:
                return
            pos = self.player.ev_g_position()
            if not pos:
                return
            for eid, mark_info in six.iteritems(self.mp_team_marks):
                for mark_type, infos in six.iteritems(mark_info):
                    for info in infos:
                        nd, space_node, v3d_pos, extra_args = info
                        dis = (pos - v3d_pos).length
                        if dis > FightLocateUI.SCALE_MIN_DIS:
                            scale = FightLocateUI.SCALE_MIN
                        elif dis > 0:
                            scale = FightLocateUI.SCALE_MAX - dis / FightLocateUI.SCALE_DIS_LEN * FightLocateUI.SCALE_MIN
                        else:
                            scale = FightLocateUI.SCALE_MAX
                        nd.lab_distance.setString('{:.0f}m'.format(dis / NEOX_UNIT_SCALE))
                        nd.img_locate.setScale(scale)
                        nd.img_locate_02.setScale(scale)
                        lpos = nd.img_locate.getPosition()
                        wpos = nd.img_locate.getParent().convertToWorldSpace(lpos)
                        nw, nh = nd.img_locate.GetContentSize()
                        from common.utils.cocos_utils import getScreenSize
                        screen_size = getScreenSize()
                        if screen_size:
                            w, h = screen_size.width, screen_size.height
                            x, y = cocos_screen_pos_to_cocos_design_pos(w * 0.5, h * 0.5)
                            nx, ny = wpos.x, wpos.y
                            if abs(x - nx) < nw * 0.5 and abs(y - ny) < nh * 0.5 and extra_args:
                                item_id = extra_args.get('item_id')
                                if item_id is not None:
                                    from logic.gutils.item_utils import get_item_name
                                    nd.lab_name.SetString(get_item_name(item_id))

                                    def _hide_nd(nd=nd):
                                        nd.PlayAnimation('hide')
                                        nd.is_play_ani = False

                                    if nd.is_play_ani:
                                        nd.stopActionByTag(DESTROY_TAG)
                                        nd.DelayCallWithTag(1.2, _hide_nd, DESTROY_TAG)

            return

    def play_show_ani(self, nd):
        nd.PlayAnimation('appear')
        nd.stopActionByTag(DESTROY_TAG)

        def loop(nd=nd):
            nd.PlayAnimation('loop')

        nd.DelayCallWithTag(0.5, loop, INIT_TAG)
        nd.is_play_ani = True