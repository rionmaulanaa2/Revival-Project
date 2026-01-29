# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/ItemsBookWardrobeWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import common.utilities
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
from logic.gutils import bond_utils
from logic.gutils import dress_utils, item_utils, template_utils, mall_utils, role_utils
from logic.client.const import mall_const
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, check_is_improvable_skin
from logic.gutils import red_point_utils
import cc
LEVEL_ALL = 10000

class ItemsBookWardrobeWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'player_item_update_event_with_id': self.on_buy_good_success,
           'weapon_sfx_change': self.weapon_sfx_change
           }
        super(ItemsBookWardrobeWidget, self).__init__(parent, panel)
        self.role_id = 0
        self.chosen_item = 0
        self.preview_item = 0
        self._ui_role_id = 0
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        self.list_container = ScaleableHorzContainer(self.panel.list_skin, self.panel.nd_cut, self.panel.list_skin_dot, self._skin_move_select_callback, self._skin_up_select_callback)
        self._skin_list = None
        self._top_skin_list = None
        self._level_skin_list = {}
        self._level_skin_count = []
        self._cur_level = -1
        self._show_skin_list = []
        self._show_top_skin_list = []
        self._skin_id_to_item = {}
        self._selected_index = 0
        self._create_skin_index = 0
        self._async_action = None
        self.group_clothing_selected_index = 0
        self.panel.temp_btn_buy.btn_common.BindMethod('OnClick', self._on_click_dress_skin)
        self.panel.btn_set.BindMethod('OnClick', self._on_click_btn_set)
        self.panel.btn_s_plus.BindMethod('OnClick', self._on_click_btn_set)
        self.panel.btn_click.BindMethod('OnClick', self.on_click_fold)
        self.panel.btn_share.BindMethod('OnClick', self.parent.on_click_btn_share)
        self.panel.nd_role_level.setVisible(False)
        self.panel.nd_level_lock.setVisible(False)

        @self.panel.btn_tags_desc_close.unique_callback()
        def OnBegin(btn, touch):
            nd_tags_desc = self.panel.nd_tags_desc
            if nd_tags_desc.isVisible():
                nd_tags_desc.setVisible(False)

        self.btn_share = self.panel.btn_share
        return

    def on_buy_good_success(self, item_no):
        if item_no in self._skin_id_to_item:
            skin_item = self._skin_id_to_item[item_no]
            template_utils.show_remain_time(skin_item.nd_time, skin_item.nd_time.lab_time, item_no)
            self.init_dress_item(skin_item, item_no)
        self.update_btn_buy()
        self.refresh_own_count()
        self.update_bond_level()

    def weapon_sfx_change(self, item_no, value):
        if item_no in self._skin_id_to_item:
            skin_item = self._skin_id_to_item[item_no]
            template_utils.show_remain_time(skin_item.nd_time, skin_item.nd_time.lab_time, item_no)
            self.init_dress_item(skin_item, item_no)

    def show_panel(self, flag):
        self.panel.setVisible(flag)

    def on_hide(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()

    def destroy(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        if self.list_container:
            self.list_container.release()
            self.list_container = None
        super(ItemsBookWardrobeWidget, self).destroy()
        return

    def set_role_id(self, role_id):
        if self.role_id == role_id:
            return
        self.role_id = role_id

    def fix_group_clothing_selected_index(self, skin_id, force_group_skin_id=None):
        self.group_clothing_selected_index = 0
        skin_id = dress_utils.get_top_skin_id_by_skin_id(skin_id) or skin_id
        dressed_clothing_id = dress_utils.get_top_skin_clothing_id(self.role_id, skin_id)
        force_clothing_id = force_group_skin_id or dressed_clothing_id
        group_skin_list = dress_utils.get_role_top_skin_owned_second_skin_list(skin_id)
        if group_skin_list and force_clothing_id in group_skin_list:
            self.group_clothing_selected_index = group_skin_list.index(force_clothing_id)

    def use_default_skin(self):
        chosen_item = dress_utils.get_role_dress_clothing_id(self.role_id, check_default=True)
        self.group_clothing_selected_index = 0
        if chosen_item in self._show_skin_list:
            self._selected_index = self._show_skin_list.index(chosen_item)
            self.fix_group_clothing_selected_index(chosen_item)

    def try_on_skin(self, skin_id, force_group_skin=None):
        if self.preview_item == skin_id and not force_group_skin:
            return False
        self.preview_item = skin_id
        self.parent.change_preview_skin(force_group_skin or skin_id)
        self.req_del_item_redpoint(skin_id)
        return True

    def refresh_all_content(self):
        if self._ui_role_id != self.role_id:
            self._ui_role_id = self.role_id
            self._top_skin_list, self._skin_list = self.get_player_skin_list()
            self._cur_level = LEVEL_ALL
            self.refresh_own_count()
            self.update_clothing_by_role(LEVEL_ALL)
            self.update_bond_level()
            self.use_default_skin()
        self._skin_move_select_callback(self._selected_index)
        self.show_skills()
        item_no, _, _ = self.get_rel_clothing()
        self.parent.change_preview_skin(item_no)
        crossover_info = role_utils.get_crossover_info(self.role_id)
        if crossover_info and crossover_info.get('pic'):
            self.panel.img_tag_kizunaai.SetDisplayFrameByPath('', crossover_info.get('pic'))
            self.panel.img_tag_kizunaai.setVisible(True)
        else:
            self.panel.img_tag_kizunaai.setVisible(False)

    def get_player_skin_list(self):
        print('self.role_id', self.role_id)
        _top_skin_list = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'skin_list')
        top_skin_list = []
        for item_id in _top_skin_list:
            if item_utils.can_open_show(item_id):
                top_skin_list.append(item_id)

        showed_skin_list = dress_utils.get_top_skin_clothing_id_list(self.role_id, top_skin_list)
        return (
         top_skin_list, showed_skin_list)

    def update_clothing_by_role(self, level):
        self._cur_level = level
        self._show_skin_list = self._level_skin_list[level]
        self._show_top_skin_list = self._level_top_skin_list[level]
        self._skin_id_to_item = {}
        self.panel.list_skin.RecycleAllItem()
        self.list_container.clear()
        self._create_skin_index = 0
        self.clear_async_action()
        self._async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.create_skin_item)])))

    def clear_async_action(self):
        if self._async_action is not None:
            self.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def create_skin_item(self):
        import time
        start_time = time.time()
        while self._create_skin_index < len(self._show_skin_list):
            skin_item = self.panel.list_skin.ReuseItem(bRefresh=False)
            if not skin_item:
                skin_item = self.panel.list_skin.AddTemplateItem(bRefresh=False)
                skin_item.SetClipObjectRecursion(self.panel.nd_cut)
            item_no = self._show_skin_list[self._create_skin_index]
            item_config = confmgr.get('lobby_item', str(item_no))
            self._skin_id_to_item[item_no] = skin_item
            self._create_skin_index += 1
            self.init_dress_item(skin_item, item_no)
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        self.panel.list_skin_dot.SetInitCount(len(self._show_skin_list))
        self.list_container.init_list()
        if self._selected_index != 0:
            self.list_container.force_select_clothing(self._selected_index)

    def init_dress_item(self, skin_item, item_no):
        item_utils.update_limit_btn(item_no, skin_item.temp_limit)
        name_text = item_utils.get_lobby_item_name(item_no)
        skin_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(skin_item, item_no)
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
        return

    def refresh_all_items_rp(self):
        for item_no, item_widget in six.iteritems(self._skin_id_to_item):
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            item_widget and red_point_utils.show_red_point_template(item_widget.nd_new, show_new)

    def refresh_all_rp(self):
        self.refresh_all_items_rp()
        self.refresh_btn_set_rp()

    def refresh_btn_set_rp(self):
        all_valid_dec_item_no = dress_utils.get_valid_deco_list_for_skin_id(self.role_id, self.preview_item)
        dec_rp = global_data.lobby_red_point_data.get_rp_by_item_no_list(all_valid_dec_item_no)
        skin_list = dress_utils.get_role_top_skin_owned_second_skin_list(self.preview_item)
        is_btn_set_red = dec_rp or global_data.lobby_red_point_data.get_rp_by_item_no_list(skin_list)
        red_point_utils.show_red_point_template(self.panel.btn_set.img_red, is_btn_set_red)

    def jump_to_skin(self, skin_id):
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(skin_id)
        if top_skin_id not in self._show_top_skin_list:
            self.update_clothing_by_role(LEVEL_ALL)
        if top_skin_id not in self._show_top_skin_list:
            return
        clothing_selected_index = self._show_top_skin_list.index(top_skin_id)
        self._skin_up_select_callback(clothing_selected_index, skin_id)
        if self.list_container.is_init():
            self.list_container.force_select_clothing(clothing_selected_index)

    def _skin_move_select_callback(self, selected_index):
        self._skin_up_select_callback(selected_index)

    def get_rel_clothing(self):
        skin_list = self._show_skin_list
        clothing_id = skin_list[self._selected_index]
        top_clothing_id = dress_utils.get_top_skin_id_by_skin_id(clothing_id) or clothing_id
        group_skin_list = dress_utils.get_role_top_skin_owned_second_skin_list(top_clothing_id)
        if group_skin_list:
            clothing_id = group_skin_list[self.group_clothing_selected_index]
        return (clothing_id, top_clothing_id, group_skin_list)

    def _skin_up_select_callback(self, selected_index, force_group_skin=None):
        skin_id = self._show_skin_list[selected_index]
        if force_group_skin:
            top_clothing_id = dress_utils.get_top_skin_id_by_skin_id(skin_id) or skin_id
            group_skin_list = dress_utils.get_role_top_skin_owned_second_skin_list(top_clothing_id)
            if force_group_skin not in group_skin_list:
                force_group_skin = None
        from logic.gutils.item_utils import update_limit_btn, get_item_need_corner_limited_tag
        if hasattr(self.panel, 'nd_logo') and get_item_need_corner_limited_tag(skin_id):
            update_limit_btn(skin_id, self.panel.nd_logo, is_corner=True)
        else:
            self.panel.nd_logo.setVisible(False)
        self.try_on_skin(skin_id, force_group_skin)
        self._selected_index = selected_index
        self.group_clothing_selected_index = 0
        self.fix_group_clothing_selected_index(skin_id, force_group_skin)
        self.update_clothing_status()
        return

    def update_clothing_status(self):
        self.update_btn_buy()
        self.update_btn_set()
        clothing_id, top_clothing_id, group_skin_list = self.get_rel_clothing()
        list_mecha_nd = self.panel.list_temp_mecha
        skin_num = len(group_skin_list)
        self.panel.nd_mecha_list.setVisible(skin_num > 1)
        if skin_num > 1:
            list_mecha_nd.SetInitCount(skin_num)
            for i, item in enumerate(list_mecha_nd.GetAllItem()):
                skin_id = group_skin_list[i]
                item.img_icon.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(skin_id))
                self.group_item_select(item, False)

                @item.btn_icon.unique_callback()
                def OnClick(_btn, _touch, _index=i, _cid=skin_id):
                    list_mecha_nd = self.panel.list_temp_mecha
                    old_item = list_mecha_nd.GetItem(self.group_clothing_selected_index)
                    self.group_item_select(old_item, False)
                    cur_item = list_mecha_nd.GetItem(_index)
                    self.group_item_select(cur_item, True)
                    self.group_clothing_selected_index = _index
                    self.parent.change_preview_skin(_cid)
                    self.update_btn_buy()

            first_item = list_mecha_nd.GetItem(self.group_clothing_selected_index)
            list_mecha_nd.LocatePosByItem(self.group_clothing_selected_index)
            self.group_item_select(first_item, True)
            if skin_num == 2:
                cur_w, h = list_mecha_nd.GetContentSize()
                new_w = list_mecha_nd.GetChildren()[0].GetContentSize()[0]
                diff_w = new_w - cur_w
                list_mecha_nd.SetContentSize(new_w, h)
                cur_w, h = self.panel.nd_mecha_list.GetContentSize()
                self.panel.nd_mecha_list.SetContentSize(cur_w + diff_w, h)
            else:
                self.panel.nd_mecha_list.InitConfContentSize()
                list_mecha_nd.InitConfContentSize()
        self.nd_set_adapted()

    def group_item_select(self, item, select):
        if item:
            item.img_frame_choose.setVisible(select)
            item.img_mask.setVisible(not select)

    def nd_set_adapted(self):
        if self.panel.btn_s_plus.isVisible():
            nd_list = [
             self.panel.btn_s_plus, self.panel.nd_mecha_list]
        else:
            nd_list = [
             self.panel.btn_set, self.panel.nd_mecha_list]
        x_off = 0
        for nd in nd_list:
            if nd.isVisible():
                X, Y = nd.GetPosition()
                nd.SetPosition(x_off, Y)
                x_off += nd.GetContentSize()[0]

        nd_set = self.panel.nd_set
        W, H = nd_set.GetContentSize()
        nd_set.SetContentSize(x_off, H)
        X, Y = nd_set.GetPosition()
        nd_set.SetPosition('50%' if self.panel.nd_mecha_list.isVisible() else '50%10', Y)

    def req_del_item_redpoint(self, skin_id):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            global_data.player.req_del_item_redpoint(skin_id)

    def update_btn_buy(self):
        item_no, _, _ = self.get_rel_clothing()
        template_utils.init_role_buy_btn(self.panel, item_no, self.role_id)
        template_utils.init_skin_tags(self.panel.nd_tags, self.panel.nd_tags_desc, self.panel.bar_tags, self.role_skin_config.get(str(item_no), {}).get('skin_tags', []))

    def update_btn_set(self):
        need_btn_set = dress_utils.role_skin_should_show_custom(self.role_id, self.preview_item)
        if need_btn_set:
            self.panel.btn_set.setVisible(True)
            if self.preview_item == 201001162:
                state = global_data.achi_mgr.get_cur_user_archive_data('ningning_speacial_skin' + str(global_data.player.uid), default=True)
                self.panel.nd_tips.setVisible(state)
                self.panel.temp_hint.lab_tips.SetString(get_text_by_id(610837))
                self.panel.PlayAnimation('show_tips')
            else:
                self.panel.nd_tips.setVisible(False)
            self.refresh_btn_set_rp()
        else:
            self.panel.btn_set.setVisible(False)
            self.panel.nd_tips.setVisible(False)
        self.panel.btn_s_plus.setVisible(False)
        if self.panel.btn_set.isVisible():
            if check_is_improvable_skin(self.preview_item):
                self.panel.btn_set.setVisible(False)
                self.panel.btn_s_plus.setVisible(True)
                self.panel.btn_s_plus.setPosition(self.panel.btn_set.getPosition())

    def _on_click_dress_skin(self, *args):
        clothing_id, top_clothing_id, group_skin_list = self.get_rel_clothing()
        rel_clothing_id = clothing_id
        default_val = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'default_skin')[0]
        goods_id = self.role_skin_config.get(str(clothing_id), {}).get('goods_id')
        is_default_skin = False
        crossover_role = role_utils.get_crossover_role_id(self.role_id)
        if int(clothing_id) == int(default_val) and not crossover_role:
            clothing_id = self.role_id
            is_default_skin = True
        skin_data = global_data.player.get_item_by_no(clothing_id)
        role_data = global_data.player.get_item_by_no(self.role_id)
        if skin_data is not None and role_data is None:
            goods_id = self.role_skin_config.get(str(default_val), {}).get('goods_id')
            self.buy_skin(is_default_skin, default_val, None, None, goods_id)
        else:
            self.buy_skin(is_default_skin, rel_clothing_id, top_clothing_id, skin_data, goods_id)
        return

    def buy_skin(self, is_default_skin, clothing_id, top_clothing_id, skin_data, goods_id):
        if is_default_skin:
            is_owned = skin_data and skin_data.get_expire_time() < 0
        else:
            is_owned = skin_data
        if not is_owned:
            price = mall_utils.get_mall_item_price(goods_id)
            if price:
                default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'default_skin', default=[])
                if clothing_id in default_skin:
                    global_data.ui_mgr.close_ui('RoleAndSkinBuyConfirmUI')
                    from logic.comsys.mall_ui.RoleAndSkinBuyConfirmUI import RoleAndSkinBuyConfirmUI
                    ui = RoleAndSkinBuyConfirmUI(goods_id=str(self.role_id))
                    ui.set_buttom_ui_price_nd(self.parent.panel.list_price)
                else:
                    ui = role_or_skin_buy_confirmUI(goods_id)
                    ui.set_buttom_ui_price_nd(self.parent.panel.list_price)
            elif item_utils.can_jump_to_ui(clothing_id):
                item_utils.jump_to_ui(clothing_id)
        else:
            global_data.player.dress_role_top_skin_fashion(clothing_id)
            global_data.player.install_role_top_skin_scheme(self.role_id, top_clothing_id, {FASHION_POS_SUIT: clothing_id})
            global_data.player.try_set_role(self.role_id)

    def _on_click_btn_set(self, btn, touch):
        global_data.ui_mgr.close_ui('RoleSkinDefineUI')
        from logic.comsys.role_profile.RoleSkinDefineUI import RoleSkinDefineUI
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(self.preview_item)
        if not top_skin_id:
            raise ValueError('Top skin id is None', self.preview_item)
        ui = RoleSkinDefineUI()
        ui.set_role_top_skin(self.role_id, top_skin_id)
        if self.preview_item == 201001162:
            global_data.achi_mgr.set_cur_user_archive_data('ningning_speacial_skin' + str(global_data.player.uid), False)
            self.panel.nd_tips.setVisible(False)

    def on_dress_change(self, new_skin_id):
        belong_no = item_utils.get_lobby_item_belong_no(new_skin_id)
        if str(belong_no) != str(self.role_id):
            return
        self.chosen_item = new_skin_id
        if new_skin_id != self.preview_item:
            self.jump_to_skin(new_skin_id)
            _, show_skin_list = self.get_player_skin_list()
            if show_skin_list != self._skin_list:
                self.update_skin_list(show_skin_list)
        self.update_btn_buy()

    def update_skin_list(self, new_skin_list):
        if new_skin_list == self._skin_list:
            return
        else:
            for idx, new_skin_id in enumerate(new_skin_list):
                old_skin_id = self._skin_list[idx]
                if new_skin_id != old_skin_id:
                    ui_item = self._skin_id_to_item.get(old_skin_id, None)
                    if ui_item:
                        self.init_dress_item(ui_item, new_skin_id)
                        self._skin_id_to_item[new_skin_id] = ui_item
                        if old_skin_id in self._show_skin_list:
                            index = self._show_skin_list.index(old_skin_id)
                            self._show_skin_list[index] = new_skin_id
                        del self._skin_id_to_item[old_skin_id]

            self._skin_list = new_skin_list
            self.refresh_own_count()
            return

    def refresh_own_count(self):
        has_func = global_data.player.has_item_by_no if global_data.player else (lambda : 0)
        self._level_skin_list = {}
        self._level_top_skin_list = {}
        skin_count = {}
        for idx, item_no in enumerate(self._skin_list):
            rare_degree = item_utils.get_item_rare_degree(item_no)
            own = has_func(item_no)
            for degree in (rare_degree, LEVEL_ALL):
                if degree:
                    self._level_skin_list.setdefault(degree, []).append(item_no)
                    self._level_top_skin_list.setdefault(degree, []).append(self._top_skin_list[idx])
                    skin_count.setdefault(degree, 0)
                    if own:
                        skin_count[degree] += 1

        degree_keys = six_ex.keys(skin_count)
        degree_keys.sort(reverse=True)
        self._level_skin_count = []
        for degree in degree_keys:
            if degree == LEVEL_ALL:
                name = get_text_by_id(608138) if 1 else get_text_by_id(81364).format(item_utils.get_rare_degree_name(degree))
                name = [
                 name, '%d/%d' % (skin_count[degree], len(self._level_skin_list[degree]))]
                self._level_skin_count.append({'rare_degree': degree,'name': name})

    def on_bond_udpate(self, role_id, event_info):
        if self.role_id == role_id:
            self.update_bond_level()

    def on_bond_reward(self, role_id):
        if self.role_id == role_id:
            pass

    def on_ret_bond_keepsake_oper(self, oper_type, role_id, role_keepsakes):
        role_id = int(role_id)
        if self.role_id == role_id:
            self.show_skills()

    def on_bond_driver_gift_change(self, *args):
        self.show_skills()

    def update_bond_level(self):
        return
        from logic.gcommon.cdata import bond_config
        from logic.gutils import system_unlock_utils
        if not bond_utils.is_open_bond_sys():
            return
        nd_role_level = self.panel.nd_role_level
        nd_level_lock = self.panel.nd_level_lock
        nd_role_level.setVisible(False)
        nd_level_lock.setVisible(False)
        has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_BOND)
        if not has_unlock:
            nd_level_lock.setVisible(True)
            _, lv = system_unlock_utils.get_sys_unlock_level(system_unlock_utils.SYSTEM_BOND)
            nd_level_lock.lab_detail.SetString(get_text_by_id(603010, [lv]))
            return
        item_data = global_data.player.get_item_by_no(self.role_id)
        if not item_data:
            nd_level_lock.setVisible(True)
            nd_level_lock.lab_detail.SetString(870037)
            return
        nd_role_level.setVisible(True)

        @nd_role_level.btn_details.unique_callback()
        def OnClick(layer, touch, *args):
            self.parent.jump_to_bond()

        @nd_role_level.btn_tips.unique_callback()
        def OnClick(layer, touch, *args):
            print('>>>> btn_tips')

        level, cur_exp = global_data.player.get_bond_data(self.role_id)
        nxt_level, nxt_exp = bond_config.get_nxt_bond_level_strength(level)
        is_max_lv = False
        if level >= bond_config.get_bond_max_level():
            is_max_lv = True
        nd_role_level.nd_level.lab_top.setVisible(is_max_lv)
        nd_role_level.nd_level.lab_num.setVisible(not is_max_lv)
        nd_role_level.nd_level.lab_level.SetString('Lv.{}'.format(level))
        percent = is_max_lv or common.utilities.safe_percent(cur_exp, nxt_exp) if 1 else 100
        nd_role_level.nd_level.nd_layout.progress_exp.setPercent(percent)
        nd_role_level.nd_level.lab_num.SetString('{}/{}'.format(cur_exp, nxt_exp))
        self.show_skills()

    def on_role_top_skin_scheme_changed(self, role_id, top_skin_id):
        if role_id == self.role_id:
            _, show_skin_list = self.get_player_skin_list()
            _, show_skin_list = self.get_player_skin_list()
            if show_skin_list != self._skin_list:
                self.update_skin_list(show_skin_list)
            if dress_utils.get_top_skin_id_by_skin_id(self.preview_item) == top_skin_id:
                self.jump_to_skin(dress_utils.get_top_skin_clothing_id(role_id, top_skin_id))
            self.update_btn_buy()

    def on_click_fold(self, *args):
        global_data.emgr.fold_mecha_details_widget.emit()

    def show_skills(self):
        pass

    def on_resolution_changed(self):
        self.list_container.force_select_clothing(self._selected_index)