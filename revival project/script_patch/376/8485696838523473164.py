# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/BigMapLegendWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import map
import cc
import world
from common.utils.cocos_utils import ccp
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils.local_text import get_text_by_id

class BigMapLegendWidget(object):

    def __init__(self, panel):
        super(BigMapLegendWidget, self).__init__()
        self.map_panel = panel
        self.init_legend()

    def destroy(self):
        self.map_panel = None
        return

    def init_legend(self):
        legend_conf = confmgr.get('map_legend_conf', 'MapLegend', 'Content')
        lids = sorted(map(int, six_ex.keys(legend_conf)))
        lids = list(map(str, lids))
        valid_lids = []
        cur_game_mode = global_data.game_mode.get_mode_type()
        cur_env = global_data.game_mode.get_enviroment()
        cur_map = global_data.game_mode.get_map_name()
        for idx, lid in enumerate(lids):
            conf = legend_conf[lid]
            use_modes = conf.get('use_modes', [])
            use_maps = conf.get('use_maps', [])
            use_env = conf.get('use_env', [])
            if use_env:
                if cur_env not in use_env:
                    continue
            if not use_modes:
                valid_lids.append(lid)
            elif cur_game_mode in use_modes or cur_map in use_maps:
                valid_lids.append(lid)
            else:
                continue

        lids = valid_lids
        self.map_panel.panel.list_example.SetInitCount(len(lids))
        all_items = self.map_panel.panel.list_example.GetAllItem()
        for idx, lid in enumerate(lids):
            conf = legend_conf[lid]
            name_id = conf.get('name_id', '')
            small_icon = conf.get('small_icon', '')
            small_icon_text = conf.get('small_icon_text', '')
            big_icon = conf.get('big_icon', '')
            ui_item = all_items[idx]
            if ui_item:
                ui_item.lab_example.SetString(name_id)
                ui_item.icon_small_text.SetString(small_icon_text)
                ui_item.icon_small.SetDisplayFrameByPath('', small_icon)
                ui_item.icon_big.SetDisplayFrameByPath('', big_icon)
                ui_item.icon_small.setVisible(True if small_icon else False)
                ui_item.icon_big.setVisible(True if big_icon else False)

        self.map_panel.panel.nd_coordinate.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.update_area)])))
        self.update_area()

    def update_area(self):
        if not global_data.cam_lplayer:
            return
        else:
            pos = global_data.cam_lplayer.ev_g_position()
            if not pos:
                return
            area_id = world.get_active_scene().get_scene_area_info(pos.x, pos.z)
            scene_name = global_data.battle.get_scene_name()
            area_name_id = confmgr.get('map_area_conf', scene_name, 'Content', str(area_id), 'name_text_id')
            if area_name_id is None:
                self.map_panel.lab_area.SetString('')
            else:
                area_name = get_text_by_id(area_name_id)
                self.map_panel.lab_area.SetString(19714, args={'name': area_name})
            return