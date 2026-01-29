# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartDetailObjMgr.py
from __future__ import absolute_import
import six
from . import ScenePart

class PartDetailObjMgr(ScenePart.ScenePart):
    INIT_EVENT = {'display_quality_change': '_on_display_quality_changed'
       }

    def __init__(self, scene, name):
        super(PartDetailObjMgr, self).__init__(scene, name)
        self._init_detail_models()

    def on_pre_load(self):
        super(PartDetailObjMgr, self).on_pre_load()
        if global_data.gsetting.quality_value('SCENE_DETAIL'):
            self._show_detail_models()
        else:
            self._hide_detail_models()

    def on_exit(self):
        self._detail_model_list = []
        super(PartDetailObjMgr, self).on_exit()

    def _init_detail_models(self):
        from logic.gcommon.cdata import item_break_data
        self._detail_model_list = []
        for model_name, config in six.iteritems(item_break_data.data):
            map_id_list = config.get('iIgnoreAsDetailMapIds', [])
            if global_data.battle and global_data.battle.map_id in map_id_list:
                self._detail_model_list.append(model_name)

    def _on_display_quality_changed(self, *args, **kwargs):
        if global_data.gsetting.quality_value('SCENE_DETAIL'):
            self._show_detail_models()
        else:
            self._hide_detail_models()

    def _hide_detail_models(self):
        if not hasattr(self.scene(), 'add_ignore_model'):
            return
        for model in self._detail_model_list:
            self.scene().add_ignore_model(model)

    def _show_detail_models(self):
        if not hasattr(self.scene(), 'clear_ignore_models'):
            return
        self.scene().clear_ignore_models()