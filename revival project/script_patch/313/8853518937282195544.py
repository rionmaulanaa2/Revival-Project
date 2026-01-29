# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaWidget.py
from __future__ import absolute_import
from logic.gutils.mecha_utils import get_mecha_lst
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils.new_template_utils import SingleChooseWidget

class MechaTypeChooseWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        super(MechaTypeChooseWidget, self).__init__(parent, panel)
        self._mecha_speciality_type = None
        self.all_mecha_lst, _, _ = get_mecha_lst()
        self.sp_type_dict = self.get_sp_type_dict()
        self.all_speciality_type_list = (None, 'spec_burst', 'spec_sustain', 'spec_sinpe',
                                         'spec_strike', 'spec_ranger', 'spec_heavy')
        self.init_list_para()
        self.init_list()
        return

    def init_list_para(self):
        self.list_mecha_choose = self.panel.list_mecha_choose

    def init_list(self):
        self.list_mecha_choose.SetInitCount(len(self.all_speciality_type_list))
        for ind, sp_type in enumerate(self.all_speciality_type_list):
            ui_item = self.list_mecha_choose.GetItem(ind)

            @ui_item.btn_tab.callback()
            def OnClick(btn, touch, sp_type=sp_type):
                global_data.emgr.hide_tech_and_module_choose_widget.emit()
                self.parent.on_switch_sp_type(sp_type)

        self.init_single_choose_widget()
        self.switch_sp_type(self._mecha_speciality_type)

    def destroy(self):
        self.destroy_widget('single_choose_widget')
        self.list_mecha_choose = None
        self.parent = None
        self.panel = None
        return

    @property
    def _mecha_conf(self):
        return confmgr.get('mecha_display', 'HangarConfig', 'Content')

    @property
    def _mecha_desc_conf(self):
        return confmgr.get('mecha_display', 'HangarDescConf', 'Content')

    def on_select_status_ui_update(self, ui_item, is_sel):
        ui_item.btn_tab.SetSelect(is_sel)
        ui_item.img_icon_2.setVisible(not is_sel)
        ui_item.img_icon_0.setVisible(is_sel)

    def on_select_status_change(self, idx, is_sel):
        pass

    def init_single_choose_widget(self):
        self.single_choose_widget = SingleChooseWidget()
        self.single_choose_widget.SetCallbacks(self.on_select_status_change, self.on_select_status_ui_update)
        allItem = self.list_mecha_choose.GetAllItem()
        self.single_choose_widget.init(self.panel, allItem, ui_item_btn_name=None)
        return

    def switch_sp_type(self, new_sp_type):
        self._mecha_speciality_type = new_sp_type
        if self._mecha_speciality_type in self.all_speciality_type_list:
            ind = self.all_speciality_type_list.index(self._mecha_speciality_type)
            self.single_choose_widget.SetSelectedIndex(ind)

    def get_sp_type_dict(self):
        hangar_type_dict = {}
        for mecha_id in self.all_mecha_lst:
            hangar_config = self._mecha_conf[str(mecha_id)]
            speciality_type_list = hangar_config.get('desc_speciality', [])
            for sp_ty in speciality_type_list:
                hangar_type_dict.setdefault(sp_ty, [])
                hangar_type_dict[sp_ty].append(mecha_id)

        return hangar_type_dict

    def get_sp_type_mecha_list(self):
        if self._mecha_speciality_type is None:
            return self.all_mecha_lst
        else:
            return self.sp_type_dict.get(self._mecha_speciality_type, [])
            return