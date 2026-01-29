# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/RegionSelectUI.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.framework import Functor
from common.platform import region_utils

class RegionSelectUI(BasePanel):
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/region_choose'

    def on_init_panel(self, **kwargs):
        self.init_data()
        self.init_cluster_tab()

    def init_data(self):
        from common.cfg import confmgr
        conf = confmgr.get('region_config', 'RegionDefine', 'Content', default={})
        region_keys = [ int(k) for k in six_ex.keys(conf) ]
        region_keys.sort()
        self.data = {}
        for k in region_keys:
            data = conf[str(k)]
            cluster_id = data['cluster_id']
            cluster_name_id = data['cluster_name_id']
            if cluster_id not in self.data:
                self.data[cluster_id] = {'cluster_name_id': cluster_name_id,'regions': []}
            self.data[cluster_id]['regions'].append(data)

        self.selected_cluster_item = None
        return

    def update_regions(self, cluster_idx):
        regions_data = self.data[cluster_idx]['regions']
        init_count = len(regions_data)
        region_list = self.panel.region_list
        region_list.SetInitCount(init_count)
        items = region_list.GetAllItem()
        for idx, item in enumerate(items):
            self.update_region_widget(regions_data[idx], item)

    def update_region_widget(self, region_data, item):
        item.img_new.setVisible(False)
        item.img_head.setVisible(False)
        item.lab_server.SetString(region_data['name_id'])
        item.BindMethod('OnClick', Functor(self.on_click_region, region_data['battle_region_id']))

    def on_click_region(self, region_id, *args):
        print('click region_id', region_id)
        region_utils.save_selected_region_code(region_id)
        self.close()

    def on_click_cluster_tab(self, idx, cluster_idx, item, *args):
        item.SetSelect(True)
        if self.selected_cluster_item:
            self.selected_cluster_item.SetSelect(False)
        self.selected_cluster_item = item
        self.update_regions(cluster_idx)

    def update_cluster_item(self, idx, cluster_idx, item):
        item.btn_window_tab.BindMethod('OnClick', Functor(self.on_click_cluster_tab, idx, cluster_idx))
        item.btn_window_tab.SetText(self.data[cluster_idx]['cluster_name_id'])
        item.btn_window_tab.EnableCustomState(True)

    def init_cluster_tab(self):
        tab_widget = self.panel.bg_panel.list_tab
        init_count = len(self.data)
        tab_widget.SetInitCount(init_count)
        items = tab_widget.GetAllItem()
        cluster_idx_list = six_ex.keys(self.data)
        cluster_idx_list.sort()
        for idx, item in enumerate(items):
            self.update_cluster_item(idx, cluster_idx_list[idx], item)

        if init_count > 0:
            self.on_click_cluster_tab(0, cluster_idx_list[0], items[0].btn_window_tab)