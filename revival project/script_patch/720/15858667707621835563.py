# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseDistanceUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
import cc
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.const import cocos_constant
from common.const import uiconst
from logic.gutils.client_unit_tag_utils import register_unit_tag
IGNORE_EXERCISE_DISTANCE_TAG_VALUE = register_unit_tag(('LMechaTrans', 'LAttachable',
                                                        'LMotorcycle'))

class ExerciseDistanceUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_distance'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    UPDATA_TIME_DUR = 0.5
    TAG = 191216
    CLOSE_TIME = 3.0
    is_show_dist = True
    BIND_POINT = {'LAvatar': 's_xuetiao',
       'LPuppet': 's_xuetiao',
       'LMechaTrans': 'xuetiao',
       'LMechaRobot': 'xuetiao',
       'LExerciseTarget': 'xuetiao'
       }
    BIND_POINT_OFFSET = {'LMechaRobot': math3d.vector(0, NEOX_UNIT_SCALE * 1.5, 0),
       'LExerciseTarget': math3d.vector(0, NEOX_UNIT_SCALE, 0)
       }

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseDistanceUI, self).on_init_panel()
        self.process_event(True)
        self.nd_distance.setVisible(False)
        self.lplayer = None
        self.target_dict = {}
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'exercise_show_hit_distance_event': self._show_distance,
           'scene_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_setted(self, lplayer):
        self.lplayer = lplayer

    def _show_distance(self, target):
        if not self.is_show_dist:
            return
        if target.MASK & IGNORE_EXERCISE_DISTANCE_TAG_VALUE:
            return
        target_id = target.id
        if target_id in self.target_dict:
            pos = target.ev_g_position()
            if not pos:
                return
            self._set_distance(target_id, pos)
        else:
            pos = target.ev_g_position()
            if not pos:
                return
            model = target.ev_g_model()
            if not model:
                return
            nd = global_data.uisystem.load_template_create(self.PANEL_CONFIG_NAME)
            nd.setScale(1.0)
            nd.is_play_ani = False
            space_nd = self._create_space_nd(nd, pos)
            self.target_dict[target_id] = [nd, space_nd, target, False]
            self._set_distance(target_id, pos)

    def _create_space_nd(self, nd, v3d_pos):
        space_nd = CCUISpaceNode.Create()
        space_nd.AddChild('', nd)
        nd.setPosition(0, NEOX_UNIT_SCALE * 1.0)

        def vis_callback(last_need_draw, cur_need_draw):
            if nd and nd.isValid():
                nd.setVisible(True if cur_need_draw else False)

        space_nd.set_visible_callback(vis_callback)
        return space_nd

    def _set_distance(self, target_id, target_pos):
        if not self.lplayer:
            return
        pos = self.lplayer.ev_g_position()
        if not pos:
            return
        distance = (target_pos - pos).length
        nd = self.target_dict[target_id][0]
        nd.lab_distance.setString('%dm' % (distance / NEOX_UNIT_SCALE))
        nd.lab_distance.setVisible(True)
        self._reset_timer(target_id)

    def _reset_timer(self, target_id):
        space_nd = self.target_dict[target_id][1]
        target = self.target_dict[target_id][2]
        is_bind = self.target_dict[target_id][3]
        space_nd.stopActionByTag(cocos_constant.TIMER_ACT_TAG)
        if not is_bind:
            bind_point = self.BIND_POINT.get(target.__class__.__name__, None)
            if self._try_bind_model(space_nd, target, bind_point):
                self.target_dict[target_id][3] = True

        def close_act():
            if not space_nd.IsDestroyed():
                space_nd.Destroy()
                if target_id in self.target_dict:
                    self.target_dict.pop(target_id)

        space_nd.DelayCallWithTag(self.CLOSE_TIME, close_act, cocos_constant.TIMER_ACT_TAG)
        return

    def _try_bind_model(self, space_nd, target, socket=None):
        model = target.ev_g_model()
        if model:
            if socket:
                space_nd.bind_model(model, socket)
                return True
            return False
        return False

    def on_finalize_panel(self):
        self.process_event(False)
        super(ExerciseDistanceUI, self).on_finalize_panel()