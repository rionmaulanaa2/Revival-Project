# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/action_preview/ActionPreviewUI.py
from __future__ import absolute_import
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.cfg import confmgr
from common.const import uiconst

class ActionPreviewUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/action_preview'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'reload_btn.OnClick': 'on_click_reload_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        self._seleted_package_item_widget = None
        self._seleted_model_widget = None
        conf = confmgr.get('action_preview')
        conf = conf.get('ModelConfig', {}).get('Content', {})
        self.panel.model_list.SetInitCount(len(conf))
        all_items = self.panel.model_list.GetAllItem()
        index = 0
        for model_id in sorted(six_ex.keys(conf)):
            item_widget = all_items[index]
            index += 1
            if item_widget:
                item_widget.name.SetString(model_id)
                item_widget.details.SetString('')
                item_widget.btn_bar.SetSwallowTouch(False)
                item_widget.btn_bar.SetNoEventAfterMove(False, '5w')

                @item_widget.btn_bar.unique_callback()
                def OnClick(btn, touch, index=index, item_widget=item_widget, model_id=model_id):
                    self.change_model_choose(True, item_widget, model_id)

                if index == 1:
                    self.change_model_choose(False, item_widget, model_id)

        return

    def change_model_choose(self, emit_change, choose_item_widget=None, model_id=None):
        if self._seleted_model_widget:
            choose = getattr(self._seleted_model_widget, 'choose')
            if choose:
                choose.setVisible(False)
            self._seleted_model_widget = False
        if choose_item_widget:
            self._seleted_model_widget = choose_item_widget
            choose = getattr(choose_item_widget, 'choose')
            if choose:
                choose.setVisible(True)
        self.update_action_list(model_id)
        if emit_change:
            global_data.emgr.change_model_preview.emit(model_id)

    def update_action_list(self, model_id):
        conf = confmgr.get('action_preview')
        conf = conf.get(model_id, {}).get('Content', {})
        self.panel.item_list.SetInitCount(len(conf))
        all_items = self.panel.item_list.GetAllItem()
        index = 0
        for action_id in sorted(six_ex.keys(conf)):
            item_widget = all_items[index]
            index += 1
            if item_widget:
                item_widget.name.SetString('id:' + action_id)
                item_widget.details.SetString('')
                item_widget.btn_bar.SetSwallowTouch(False)
                item_widget.btn_bar.SetNoEventAfterMove(False, '5w')

                @item_widget.btn_bar.unique_callback()
                def OnClick(btn, touch, index=index, item_widget=item_widget, action_id=action_id):
                    self.change_action_choose(True, item_widget, action_id)

                if index == 1:
                    self.change_action_choose(False, item_widget, action_id)

    def change_action_choose(self, emit_change, choose_item_widget=None, action_id=None):
        if self._seleted_package_item_widget:
            choose = getattr(self._seleted_package_item_widget, 'choose')
            if choose:
                choose.setVisible(False)
            self._seleted_package_item_widget = False
        if choose_item_widget:
            self._seleted_package_item_widget = choose_item_widget
            choose = getattr(choose_item_widget, 'choose')
            if choose:
                choose.setVisible(True)
        if emit_change:
            global_data.emgr.change_action_preview.emit(action_id)

    def on_click_reload_btn(self, *args):
        import os
        last_work_path = os.getcwd()
        from common.cfg import confmgr
        excel_tool_path = confmgr.get('action_preview_setting', 'excel_tool_path')
        os.chdir(excel_tool_path)
        os.system('gen_code.exe')
        os.chdir(last_work_path)
        confmgr.exit()
        self.on_init_panel()