# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/WidgetExtModelPic.py
from __future__ import absolute_import
from logic.gutils import mall_utils
from logic.gutils import item_utils
from ext_package.ext_decorator import has_skin_ext
from logic.gutils.item_utils import ext_can_show_model
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_YTPE_VEHICLE, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_UNKONW_ITEM

class WidgetExtModelPic(object):

    def __init__(self, panel):
        self.__widget_panel = panel
        self._skin_pic_nd = None
        return

    def ext_not_show_no_model(self):
        if self._skin_pic_nd:
            self._skin_pic_nd.setVisible(False)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def ext_show_item_model(self, in_model_data, in_good_id=None, in_item_id=None, vehicle_scale=1.0, in_load_callback=None):
        if not (self.__widget_panel and self.__widget_panel.isValid()):
            return
        else:
            if not self.__widget_panel.nd_pic:
                return
            if not in_item_id and in_good_id:
                in_item_id = mall_utils.get_goods_item_no(in_good_id)
            if in_item_id:
                item_type = item_utils.get_lobby_item_type(in_item_id)
            else:
                item_type = L_ITEM_TYPE_UNKONW_ITEM
            if not has_skin_ext() and not ext_can_show_model(in_item_id, item_type):
                global_data.emgr.change_model_display_scene_item.emit(None)
                if not self._skin_pic_nd:
                    self._skin_pic_nd = global_data.uisystem.load_template_create('common/i_common_preview_pic', self.__widget_panel.nd_pic)
                self._skin_pic_nd.setVisible(True)
                pic = mall_utils.get_detail_pic_by_item_no(in_item_id)
                self._skin_pic_nd.pic.SetDisplayFrameByPath('', pic)
                if item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN):
                    self._skin_pic_nd.pic.setScale(0.6)
                elif item_type in (L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_YTPE_VEHICLE):
                    self._skin_pic_nd.pic.setScale(vehicle_scale)
                else:
                    self._skin_pic_nd.pic.setScale(1.0)
                global_data.emgr.change_model_display_scene_item.emit(None)
            else:
                if self._skin_pic_nd:
                    self._skin_pic_nd.setVisible(False)
                global_data.emgr.change_model_display_scene_item.emit(in_model_data, load_callback=in_load_callback)
            return

    def destroy(self):
        if self._skin_pic_nd:
            self._skin_pic_nd.Destroy()
            self._skin_pic_nd = None
        self.__widget_panel = None
        return