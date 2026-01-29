# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MechaSkinListWidget.py
from __future__ import absolute_import
from logic.gutils import mall_utils
from common.cfg import confmgr
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
from common.utils.timer import RELEASE
from logic.gutils import red_point_utils
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
import time
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id, get_mecha_dress_clothing_id
from logic.gcommon.item import item_const
from logic.gcommon.common_utils import text_utils
from logic.gutils import dress_utils
from logic.comsys.items_book_ui.SkinListWidget import SkinListWidget, VIEW_BY_MECHA_KIND, VIEW_BY_DEGREE, VIEW_BY_SERIES
from logic.gutils import mecha_skin_utils
from logic.gutils import skin_define_utils

class MechaSkinListWidget(SkinListWidget):

    def __init__(self, parent, panel):
        super(MechaSkinListWidget, self).__init__(parent, panel)

    def init_data(self):
        super(MechaSkinListWidget, self).init_data()
        self.data_dict = {}
        self.data_dict['skins'] = self.get_mecha_skin_dict()
        class_list = (VIEW_BY_MECHA_KIND, VIEW_BY_DEGREE, VIEW_BY_SERIES)
        self.class_option_list = [ {'name': self.view_text_dict[i],'index': i} for i in class_list ]
        self.mecha_order = self.get_mecha_order()
        from logic.gutils.item_utils import get_locate_icon_bg_path, get_locate_pic_path
        from logic.gcommon.common_const.battle_const import LOCATE_MECHA
        mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._mecha_role_option_list = [ {'name': mecha_conf[str(i)]['name_mecha_text_id'],'index': i,'icon': get_locate_pic_path(LOCATE_MECHA, None, mecha_id=i),'item_no': battle_id_to_mecha_lobby_id(i)} for i in self.mecha_order
                                       ]
        self._mecha_role_option_list.insert(0, {'name': 80566,'index': -1,'icon': 'gui/ui_res_2/common/icon/icon_mecha.png',
           'icon_scale': 0})
        return

    def get_mecha_order(self):
        _mecha_open_info = global_data.player.read_mecha_open_info()
        mecha_order = list(_mecha_open_info['opened_order'])
        own_func = lambda : False
        if global_data.player:
            own_func = lambda mecha_id: global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id))
        own_mecha_ids = []
        not_own_mecha_ids = []
        for mecha_id in mecha_order:
            if own_func(mecha_id):
                own_mecha_ids.append(mecha_id)
            else:
                not_own_mecha_ids.append(mecha_id)

        return own_mecha_ids + not_own_mecha_ids

    def sort_by_default(self, kind, kind_skin_list):
        if self._chose_class not in [VIEW_BY_MECHA_KIND]:
            if self._chose_class == VIEW_BY_SERIES:
                if kind.startswith('belong_set_season'):
                    season = kind.split('-')[1]
                    return '#-belong_set_season' + '%03d' % (1000 - int(season))
            return kind
        else:
            return self.mecha_order.index(kind)

    def get_mecha_skin_dict(self):
        showed_skin_dict = {}
        open_mecha_list = global_data.player.read_mecha_open_info()['opened_order']
        for mecha_id in open_mecha_list:
            org_skin_list = mecha_skin_utils.get_show_skin_list(mecha_id)
            final_skin_list = []
            for skin_id in org_skin_list:
                all_related_skin = []
                group_skin_list = skin_define_utils.get_group_skin_list(skin_id)
                all_related_skin.extend(group_skin_list)
                _skin_id_lst = mecha_skin_utils.get_mecha_ss_skin_lst(skin_id)
                for sid in _skin_id_lst:
                    if sid not in all_related_skin:
                        all_related_skin.append(sid)

                final_skin_list.extend(all_related_skin)

            showed_skin_dict[mecha_id] = final_skin_list

        return showed_skin_dict

    def init_skin_item(self, clothing_item, clothing_id, index):
        name_text = item_utils.get_lobby_item_name(clothing_id)
        clothing_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(clothing_item, clothing_id)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id))
        if skin_cfg:
            item_utils.check_skin_tag(clothing_item.nd_kind, clothing_id)
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                clothing_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
        red_point_utils.show_red_point_template(clothing_item.nd_new, show_new)
        clothing_data = global_data.player.get_item_by_no(clothing_id) if global_data.player else None
        if clothing_data is None:
            clothing_item.nd_lock.setVisible(True)
        else:
            clothing_item.nd_lock.setVisible(False)
        clothing_item.nd_card.BindMethod('OnClick', Functor(self.on_click_skin_item, index, clothing_id))
        return

    def on_click_skin_item(self, index, item_no, *args):
        target_skin_list = self.details_sorted_title_kind_skin_list
        if not target_skin_list:
            return
        if not self.panel:
            return
        super(MechaSkinListWidget, self).on_click_skin_item(index, item_no, *args)
        from logic.comsys.mecha_display.ItemsBookMechaDetails import ItemsBookMechaDetails
        ItemsBookMechaDetails()
        ui = global_data.ui_mgr.get_ui('ItemsBookMechaDetails')
        if ui:
            base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(item_no)
            if base_skin_id:
                replace_dict = {base_skin_id: item_no}
            else:
                replace_dict = {}
            showed_sorted_title_kind_skin_list = [ (title, self.fit_skin_list_to_only_base_one(skin_list, replace_dict)) for title, skin_list in self.details_sorted_title_kind_skin_list
                                                 ]
            skins_index = 0
            for idx, skins_info in enumerate(self.details_sorted_title_kind_skin_list):
                title, skin_list = skins_info
                if item_no in skin_list:
                    skins_index = idx
                    break

            ui.show_skin_details_with_list(item_no, showed_sorted_title_kind_skin_list, skins_index)

    def fit_skin_list_to_only_base_one(self, skin_list, replace_dict):
        final_skin_list = []
        search_set = set()
        mecha_sub_skin_dict = global_data.player.get_mecha_sub_skin()
        for skin_id in skin_list:
            show_skin_id = items_book_utils.transform_mecha_skin_id_to_show_one(skin_id, mecha_sub_skin_dict)
            if show_skin_id not in search_set:
                search_set.add(show_skin_id)
                from logic.gutils import mecha_skin_utils
                base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(show_skin_id)
                if base_skin_id in replace_dict:
                    show_skin_id = replace_dict[base_skin_id]
                final_skin_list.append(show_skin_id)

        return final_skin_list