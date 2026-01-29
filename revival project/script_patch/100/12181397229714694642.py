# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapPoisonSignalWidget.py
from __future__ import absolute_import
from six.moves import zip
from logic.comsys.map.map_widget import MapScaleInterface
import cc
import math
from logic.gutils.map_utils import get_map_uv, get_map_dist, get_map_pos_from_world, get_map_config
import math3d
import weakref
from common import utilities
from common.utils.cocos_utils import ccc4fFromHex
import world
from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_NONE
SIGNAL_TAG = 201111

class MapPoisonSignalWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel, map_nd):
        super(MapPoisonSignalWidget, self).__init__(map_nd, panel)
        self.is_nd_need_remove = False
        self._nd = self.map_panel.map_nd.nd_nosignal
        self.init_outer_signal_pos()
        self.sync_signal_nd_pos()
        self.check_poison_signal()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)
        global_data.emgr.scene_poison_updated_event += self.on_posion_changed
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect

    def on_login_reconnect(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)

    def on_update(self):
        self.sync_signal_nd_pos()

    def destroy(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = 0
        global_data.emgr.scene_poison_updated_event -= self.on_posion_changed
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnect
        super(MapPoisonSignalWidget, self).destroy()
        self.outer_signal_wpos_list = []

    def on_map_scale(self, map_scale):
        s = 1.0 / self.map_panel.map_nd.clip_circle.getScale()
        final_scale = 1.0 / map_scale * s
        self._nd.signal_1.setScale(final_scale)
        self._nd.signal_2.setScale(final_scale)
        self._nd.signal_3.setScale(final_scale)

    def init_outer_signal_pos(self):
        wpos_list = []
        children = self.map_panel.nd_nosignal.GetChildren()
        for c in children:
            wpos_list.append(c.getParent().convertToWorldSpace(c.getPosition()))

        children = self._nd.GetChildren()
        self.outer_signal_wpos_list = list(zip(children, wpos_list))

    def sync_signal_nd_pos(self):
        for nd, wpos in self.outer_signal_wpos_list:
            lpos = nd.getParent().convertToNodeSpace(wpos)
            nd.setPosition(lpos)

    def on_posion_changed(self, force=False):
        self.check_poison_signal()

    def check_poison_signal(self):
        nd = self._nd
        nd.setVisible(False)
        poison_mgr = self.map_panel.poison_mgr()
        if not poison_mgr:
            return
        cnt_circle_data = poison_mgr.get_cnt_circle_info()
        if cnt_circle_data and cnt_circle_data['state'] and cnt_circle_data['state'] != POISON_CIRCLE_STATE_NONE:
            nd.setVisible(True)
        else:
            nd.setVisible(False)