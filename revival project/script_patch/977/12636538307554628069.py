# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/RoleSkinListWidget.py
from __future__ import absolute_import
import six
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
from logic.comsys.items_book_ui.SkinListWidget import SkinListWidget, VIEW_BY_HUMAN_KIND, VIEW_BY_DEGREE, VIEW_BY_SERIES, SORT_BY_DEFAULT

class RoleSkinListWidget(SkinListWidget):

    def __init__(self, parent, panel):
        super(RoleSkinListWidget, self).__init__(parent, panel)

    def init_data(self):
        super(RoleSkinListWidget, self).init_data()
        self.data_dict = {}
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        self.data_dict['skins'] = self.get_player_skin_dict()
        class_list = (VIEW_BY_HUMAN_KIND, VIEW_BY_DEGREE, VIEW_BY_SERIES)
        self.class_option_list = [ {'name': self.view_text_dict[i],'index': i} for i in class_list ]
        role_config = confmgr.get('role_info', 'RoleProfile', 'Content')
        self.role_order = self.get_role_show_order()

        def get_role_head(role_id):
            role_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id))
            return 'gui/ui_res_2/mech_display/icon_role%d.png' % role_info['mecha_id']

        self._mecha_role_option_list = [ {'name': role_config[str(i)]['role_name'],'index': str(i),'icon': get_role_head(i),'icon_scale': 0.7,'item_no': str(i)} for i in self.role_order
                                       ]
        self._mecha_role_option_list.insert(0, {'name': 80566,'index': -1,'icon': 'gui/ui_res_2/catalogue/common/icon_catalogue_common_choose_all.png','icon_scale': 0
           })

    def sort_by_default(self, kind, kind_skin_list):
        if self._chose_class not in [VIEW_BY_HUMAN_KIND]:
            if self._chose_class == VIEW_BY_SERIES:
                if kind.startswith('belong_set_season'):
                    season = kind.split('-')[1]
                    return '#-belong_set_season' + '%03d' % (1000 - int(season))
            return kind
        else:
            return self.role_order.index(int(kind))

    def get_role_show_order(self):
        role_id_list = global_data.player.get_role_open_seq()
        role_id_list_owned = []
        role_id_list_not_owned = []
        for role_id in role_id_list:
            role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'goods_id')
            if not role_goods_id:
                continue
            role_id = int(role_id)
            role_data = global_data.player.get_item_by_no(role_id)
            has_role = role_data is not None
            if has_role:
                role_id_list_owned if 1 else role_id_list_not_owned.append(role_id)

        role_id_list = role_id_list_owned + role_id_list_not_owned
        return role_id_list

    def get_player_skin_dict(self):
        role_info = confmgr.get('role_info', 'RoleInfo', 'Content')
        showed_skin_dict = {}
        for role_id, role_id_info in six.iteritems(role_info):
            role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'goods_id')
            if not role_goods_id:
                continue
            _top_skin_list = role_id_info.get('skin_list', [])
            top_skin_list = []
            all_skin_list = []
            for item_id in _top_skin_list:
                if item_utils.can_open_show(item_id, owned_should_show=True):
                    top_skin_list.append(item_id)

            for top in top_skin_list:
                group_skin_list = dress_utils.get_role_top_skin_owned_second_skin_list(top)
                all_skin_list.extend(group_skin_list)

            showed_skin_dict[role_id] = all_skin_list

        return showed_skin_dict

    def init_skin_item(self, skin_item, item_no, index):
        item_utils.update_limit_btn(item_no, skin_item.temp_limit)
        name_text = item_utils.get_lobby_item_name(item_no)
        skin_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(skin_item, item_no)
        skin_item.nd_choose.setVisible(False)
        skin_cfg = self.role_skin_config.get(str(item_no))
        if skin_cfg:
            item_utils.check_skin_tag(skin_item.nd_kind, item_no)
            skin_half_imge_role = skin_cfg.get('half_img_role')
            if skin_half_imge_role is not None:
                skin_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_role)
        template_utils.show_remain_time(skin_item.nd_time, skin_item.nd_time.lab_time, item_no)
        own = global_data.player.has_item_by_no(item_no) if global_data.player else False
        skin_item.nd_lock.setVisible(not own)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
        red_point_utils.show_red_point_template(skin_item.nd_new, show_new)
        skin_item.nd_card.BindMethod('OnClick', Functor(self.on_click_skin_item, index, item_no))
        return

    def on_click_skin_item(self, index, item_no, *args):
        target_skin_list = self.details_sorted_title_kind_skin_list
        if not target_skin_list:
            return
        if not self.panel:
            return
        super(RoleSkinListWidget, self).on_click_skin_item(index, item_no, *args)
        from logic.comsys.role_profile.ItemsBookRoleInfoUI import ItemsBookRoleInfoUI
        ItemsBookRoleInfoUI()
        ui = global_data.ui_mgr.get_ui('ItemsBookRoleInfoUI')
        if ui:
            showed_sorted_title_kind_skin_list = [ (title, self.fit_skin_list_to_only_base_one(skin_list)) for title, skin_list in target_skin_list ]
            if showed_sorted_title_kind_skin_list:
                skins_index = 0
                for idx, skins_info in enumerate(self.details_sorted_title_kind_skin_list):
                    title, skin_list = skins_info
                    if item_no in skin_list:
                        skins_index = idx
                        break

                ui.show_skin_details_with_list(item_no, showed_sorted_title_kind_skin_list, skins_index)
            else:
                raise ValueError('Invalid convert result: %s', str(target_skin_list))

    def transform_skin_id_to_show_one(self, skin_id):
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(skin_id)
        return top_skin_id

    def fit_skin_list_to_only_base_one(self, skin_list):
        final_skin_list = []
        search_set = set()
        for skin_id in skin_list:
            show_skin_id = self.transform_skin_id_to_show_one(skin_id)
            if show_skin_id not in search_set:
                final_skin_list.append(show_skin_id)
                search_set.add(show_skin_id)

        return final_skin_list