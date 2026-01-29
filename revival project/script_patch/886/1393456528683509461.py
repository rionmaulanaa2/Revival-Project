# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/ItemsBookMechaBasicInfoWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.comsys.mecha_display.MechaBasicSkinWidget import MechaBasicSkinWidget

class ItemsBookMechaBasicSkinWidget(MechaBasicSkinWidget):
    pass


class ItemsBookMechaBasicInfoWidget(BaseUIWidget):
    USE_CNT_LIST = [
     1, 2, 5]

    def __init__(self, parent, panel):
        super(ItemsBookMechaBasicInfoWidget, self).__init__(parent, panel)
        self.init_parameters()
        self._basic_skin_widget = None
        self.init_widget()
        return

    def init_widget(self):
        self.panel.btn_click.BindMethod('OnClick', self.on_click_fold)
        self.panel.btn_share.BindMethod('OnClick', self.parent.on_click_btn_share)

    def destroy(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        if self._basic_skin_widget:
            self._basic_skin_widget.destroy()
            self._basic_skin_widget = None
        super(ItemsBookMechaBasicInfoWidget, self).destroy()
        return

    def hide(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()
        super(ItemsBookMechaBasicInfoWidget, self).hide()

    def get_basic_skin_widget(self):
        return self._basic_skin_widget

    def on_switch_to_mecha_type(self, mecha_type):
        if self._cur_mecha_type == mecha_type:
            if self._basic_skin_widget:
                self._basic_skin_widget.on_refresh()
            return
        self._cur_mecha_type = mecha_type
        self.panel.nd_proficiency.setVisible(False)
        self.panel.nd_proficiency_lock.setVisible(False)
        if not self._basic_skin_widget:
            self._basic_skin_widget = ItemsBookMechaBasicSkinWidget(self.parent, self.panel, mecha_type)
        else:
            self._basic_skin_widget.on_switch_mecha_type(mecha_type)

    def on_switch_skin_category(self, skins, clothind_id):
        self.panel.nd_proficiency.setVisible(False)
        self.panel.nd_proficiency_lock.setVisible(False)
        if not self._basic_skin_widget:
            self._basic_skin_widget = ItemsBookMechaBasicSkinWidget(self.parent, self.panel, None)
            self._basic_skin_widget.on_switch_skin_category(skins, clothind_id)
        else:
            self._basic_skin_widget.on_switch_skin_category(skins, clothind_id)
        return

    def init_parameters(self):
        self._cur_mecha_type = None
        return

    def jump_to_skin(self, skin_id):
        if self._basic_skin_widget:
            self._basic_skin_widget.jump_to_skin(skin_id)

    def on_play(self, *args):
        self.parent._on_click_chuchang()

    def on_click_fold(self, *args):
        global_data.emgr.fold_mecha_details_widget.emit()

    def on_resolution_changed(self):
        self._basic_skin_widget and self._basic_skin_widget.on_resolution_changed()