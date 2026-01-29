# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapPlaceNameInitWidget.py
from __future__ import absolute_import
import six
from logic.comsys.map.map_widget import MapScaleInterface
import cc
from common.cfg import confmgr
from logic.client.const.game_mode_const import GAME_MODE_GULAG_SURVIVAL
HIDE_AREA_BY_MODE = {GAME_MODE_GULAG_SURVIVAL: [
                            19874]
   }

class MapPlaceNameInitWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel, map_nd):
        super(MapPlaceNameInitWidget, self).__init__(map_nd, panel)
        self.init_widget()

    def init_widget(self):
        from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_EN, get_lang_shrink_font_size
        if not global_data.battle:
            return
        map_id = str(global_data.battle.map_id)
        map_data_conf = confmgr.get('map_config', str(map_id), default={})
        map_json_path = map_data_conf.get('cMapNameJson', 'map/ccb_map_bw06_map_names')
        nd_name = self.parent_nd.nd_scale_up_details.nd_name_json
        if nd_name and nd_name.GetTemplatePath() != map_json_path:
            self.parent_nd.nd_scale_up_details.nd_name_json.Destroy()
        nd_name_json = global_data.uisystem.load_template_create(map_json_path, parent=self.parent_nd.nd_scale_up_details, name='nd_name_json')
        nd_name_json.setLocalZOrder(-100)
        scene_name = global_data.battle.get_scene_name()
        area_info_confs = confmgr.get('map_area_conf', scene_name, 'Content')
        rich_info_confs = confmgr.get('map_area_conf', 'MapAreaRichConfig', 'Content')
        if not area_info_confs:
            return
        hide_area = HIDE_AREA_BY_MODE.get(global_data.game_mode.mode_Type, [])
        for rid, area_info in six.iteritems(area_info_confs):
            name_text_id = area_info.get('name_text_id')
            rich_name_text_id = area_info.get('rich_name_text_id', name_text_id)
            nd = getattr(nd_name_json.nd_name, 'name_%d' % name_text_id)
            if not nd:
                nd = getattr(nd_name_json.nd_name, 'name_%d' % rich_name_text_id)
                if not nd:
                    log_error('map name node for area %s not exist!' % rid)
                    continue
            if name_text_id in hide_area:
                nd.setVisible(False)
                continue
            rich_id = area_info.get('rich_id', 1)
            rich_info = rich_info_confs.get(str(rich_id), {})
            if not rich_info:
                continue
            nd.lab_name.SetColor(rich_info.get('text_color'))
            font_size = rich_info.get('font_size', 0)
            if font_size:
                text = '<size=%d>%s</size>' % (get_lang_shrink_font_size(font_size), get_text_local_content(rich_name_text_id))
            else:
                text = get_text_local_content(rich_name_text_id)
            if get_cur_text_lang() == LANG_EN:
                text = '<outline=2 color = 0x233061FF>%s</outline>' % text
            nd.lab_name.SetString(text)

    def destroy(self):
        super(MapPlaceNameInitWidget, self).destroy()

    def on_map_scale(self, map_scale):
        pass