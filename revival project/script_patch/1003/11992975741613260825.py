# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESkinChooseWidget.py
from __future__ import absolute_import
from logic.gutils.dress_utils import get_mecha_dress_clothing_id, battle_id_to_mecha_lobby_id
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mecha_skin_utils, skin_define_utils, item_utils, red_point_utils
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
from logic.gutils.mecha_skill_utils import get_mecha_speciality_desc_str
from logic.gutils.jump_to_ui_utils import jump_to_skin_define
from logic.gutils.template_utils import show_remain_time, splice_price
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.comsys.mecha_display.SkinImproveWidgetUI import SkinImproveWidgetUI
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.gutils.mall_utils import get_mall_item_price
from logic.gcommon.time_utility import get_server_time
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gcommon.const import PRIV_ENJOY_FREE_TIMES_PER_WEEK, SKIN_SHARE_TYPE_PRIV
from logic.gcommon.item.item_const import FASHION_POS_WEAPON_SFX, FASHION_POS_SUIT
from common.cfg import confmgr
import time
import cc
USE_SAME_PIC_CLOTHING_IDS = {
 201800651, 201800652, 201800653}
CARD_SS_FRAME_TEMPLATE = 'role_profile/i_card_skin_frame_ss'

class PVESkinChooseWidget(object):

    def __init__(self, parent, panel):
        self._parent = parent
        self._panel = panel
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._lobby_mecha_config = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content')
        self._async_action = None
        self._cur_mecha_id = None
        self._cur_lobby_mecha_id = None
        self._cur_clothing_id = None
        self._clothing_selected_index = None
        self._group_clothing_selected_index = None
        self._cur_create_skin_index = None
        self.show_skin_list_cnf = None
        self.nd_mecha_list = None
        self.list_mecha_nd = None
        self._clothing_id_2_item = {}
        if global_data.is_pc_mode:
            self.show_ss_card_effect = False
        else:
            self.show_ss_card_effect = True
        return

    def init_ui(self):
        self._init_nd_skin_choose()

    def init_ui_event(self):
        nd_set = self._panel.nd_set

        @nd_set.btn_ss.unique_callback()
        def OnClick(btn, touch):
            self._on_show_skin_improve()
            global_data.emgr.set_last_chuchang_id.emit(self._cur_clothing_id)

        @nd_set.btn_s_plus.unique_callback()
        def OnClick(btn, touch):
            self._on_show_skin_improve()
            global_data.emgr.set_last_chuchang_id.emit(self._cur_clothing_id)

        @nd_set.btn_set.unique_callback()
        def OnClick(btn, touch):
            jump_to_skin_define(self._cur_mecha_id, self._cur_clothing_id)

        @self._panel.nd_get.btn_get.unique_callback()
        def OnClick(btn, touch):
            is_owned = self.get_current_skin_is_own()
            goods_id = self._mecha_skin_conf.get(str(self._cur_clothing_id), {}).get('goods_id')
            if not is_owned:
                is_default_skin, _ = self.get_current_skin_is_default()
                if is_default_skin:
                    ui = global_data.ui_mgr.show_ui('MechaDetails', 'logic.comsys.mecha_display')
                    ui.show_mecha_details(self._cur_mecha_id)
                elif item_utils.can_jump_to_ui(str(self._cur_clothing_id)):
                    from logic.gutils.mall_utils import get_mall_item_price
                    price_list = get_mall_item_price(goods_id)
                    if price_list:
                        ui = role_or_skin_buy_confirmUI(goods_id)
                    else:
                        item_utils.jump_to_ui(str(self._cur_clothing_id))
                else:
                    ui = role_or_skin_buy_confirmUI(goods_id)

    def _on_show_skin_improve(self):
        ui = global_data.ui_mgr.get_ui('SkinImproveWidgetUI')
        if not ui:
            ui = SkinImproveWidgetUI(None)
        if ui:
            ui.on_show_skin_improve(self._cur_mecha_id, self._cur_clothing_id)
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self._on_buy_good_success,
           'pay_order_succ_event': self._on_buy_good_success,
           'on_pve_mecha_show_changed': self.update_nd_skin_choose,
           'refresh_share_skin_event': self._on_add_teammate,
           'undress_priv_skin_event': self._on_undress_priv_skin,
           'update_skin_share_state': self._on_update_priv_free_mecha_fashions
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _init_nd_skin_choose(self):
        nd_cut = self._panel.nd_list_skin.nd_cut
        self.list_skin_ui = nd_cut.list_skin
        self.nd_mecha_list = self._panel.nd_set.nd_mecha_list
        self.list_mecha_nd = self.nd_mecha_list.list_temp_mecha
        self.list_container = ScaleableHorzContainer(self.list_skin_ui, nd_cut, None, self._skin_move_select_callback, self._skin_up_select_callback, self._on_begin_callback)
        current_mecha_id = global_data.player.get_pve_select_mecha_id() if global_data.player else 8001
        self.update_nd_skin_choose(current_mecha_id)
        return

    def _skin_move_select_callback(self, selected_index):
        self._skin_up_select_callback(selected_index)

    def _skin_up_select_callback(self, selected_index):
        if selected_index != self._clothing_selected_index:
            skin_list = self.show_skin_list_cnf
            skin_id = skin_list[selected_index]
            self._clothing_selected_index = selected_index
            dressed_clothing_id = global_data.player.get_pve_using_mecha_skin(self._cur_lobby_mecha_id)
            self._group_clothing_selected_index = 0
            group_skin_list = skin_define_utils.get_group_skin_list(skin_id)
            if group_skin_list:
                if dressed_clothing_id in group_skin_list:
                    self._group_clothing_selected_index = group_skin_list.index(dressed_clothing_id)
                elif skin_id in group_skin_list:
                    self._group_clothing_selected_index = group_skin_list.index(skin_id)
            self.req_del_item_redpoint(skin_id, selected_index)
            self.update_clothing_status()

    def _on_begin_callback(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()

    def req_del_item_redpoint(self, skin_id, selected_index):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            if global_data.player:
                global_data.player.req_del_item_redpoint(skin_id)
            item = self.list_skin_ui.GetItem(selected_index)
            red_point_utils.show_red_point_template(item.nd_new, False)

    def req_del_group_item_redpoint(self, skin_id, selected_index):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            if global_data.player:
                global_data.player.req_del_item_redpoint(skin_id)
            item = self.list_mecha_nd.GetItem(selected_index)
            red_point_utils.show_red_point_template(item.temp_red, False)

    def update_clothing_status(self):
        self._cur_clothing_id, group_skin_list = self.get_rel_clothing()
        self.update_mecha_view(self._cur_clothing_id)
        list_mecha_nd = self.list_mecha_nd
        skin_num = len(group_skin_list)
        self.nd_mecha_list.setVisible(skin_num > 1)
        if skin_num > 1:
            list_mecha_nd.SetInitCount(skin_num)
            for i, item in enumerate(list_mecha_nd.GetAllItem()):
                skin_id = group_skin_list[i]
                item.skin_id = skin_id
                item.img_icon.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_id))
                show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
                red_point_utils.show_red_point_template(item.temp_red, show_new)
                if global_data.player:
                    clothing_data = global_data.player.get_item_by_no(skin_id) if 1 else None
                    item.img_mask.setVisible(clothing_data is None)
                    self.group_item_select(item, False)

                    @item.btn_icon.unique_callback()
                    def OnClick(btn, touch, index=i, clothing_id=skin_id):
                        self._cur_clothing_id = clothing_id
                        list_mecha_nd = self.list_mecha_nd
                        old_item = list_mecha_nd.GetItem(self._group_clothing_selected_index)
                        self.group_item_select(old_item, False)
                        cur_item = list_mecha_nd.GetItem(index)
                        self.group_item_select(cur_item, True)
                        self._group_clothing_selected_index = index
                        self.update_mecha_view(clothing_id)
                        self.req_del_group_item_redpoint(clothing_id, index)
                        self.update_nd_get()

            first_item = list_mecha_nd.GetItem(self._group_clothing_selected_index)
            list_mecha_nd.LocatePosByItem(self._group_clothing_selected_index)
            self.group_item_select(first_item, True)
            if skin_num == 2:
                cur_w, h = list_mecha_nd.GetContentSize()
                new_w = list_mecha_nd.GetChildren()[0].GetContentSize()[0]
                diff_w = new_w - cur_w
                list_mecha_nd.SetContentSize(new_w, h)
                cur_w, h = self.nd_mecha_list.GetContentSize()
                self.nd_mecha_list.SetContentSize(cur_w + diff_w, h)
            else:
                self.nd_mecha_list.InitConfContentSize()
                list_mecha_nd.InitConfContentSize()
        clothing_item = self._clothing_id_2_item.get(self._cur_clothing_id)
        if clothing_item and clothing_item.isValid():
            item_config = confmgr.get('lobby_item', str(self._cur_clothing_id))
            self.init_clothing_item(item_config, clothing_item, self._cur_clothing_id)
        self._update_btn_state()
        self.nd_set_adapted()
        self.update_nd_get()
        self.update_priv_status(self._cur_clothing_id)
        return

    def update_priv_status(self, skin_id):
        is_priv_free = global_data.player.is_priv_share(skin_id)
        self._parent.panel.bar_tips.setVisible(is_priv_free)
        if is_priv_free:
            self._panel.nd_get.setVisible(False)
        if is_priv_free and global_data.player.is_teammate_lobby_skin(skin_id):
            self._parent.panel.lab_skin_tips.SetString(611576)
        else:
            cur_cnt = global_data.player.get_priv_enjoy_free_cnt()
            self._parent.panel.lab_skin_tips.SetString(get_text_by_id(611575).format(cur_cnt, PRIV_ENJOY_FREE_TIMES_PER_WEEK))

    def update_mecha_view(self, skin_id):
        model_data = get_lobby_model_data(skin_id, consider_second_model=False)
        shiny_weapon_id = None
        if model_data and model_data[0]:
            shiny_weapon_id = model_data[0].get('shiny_weapon_id')
        global_data.emgr.on_pve_mecha_skin_changed.emit(skin_id, shiny_weapon_id)
        return

    def get_rel_clothing(self):
        clothing_id = self.show_skin_list_cnf[self._clothing_selected_index]
        group_skin_list = skin_define_utils.get_group_skin_list(clothing_id)
        if group_skin_list:
            clothing_id = group_skin_list[self._group_clothing_selected_index]
        return (clothing_id, group_skin_list)

    def group_item_select(self, item, select):
        if item:
            item.img_frame_choose.setVisible(select)

    def nd_set_adapted(self):
        nd_set = self._panel.nd_set
        nd_list = [nd_set.btn_ss, nd_set.btn_s_plus, nd_set.btn_set, nd_set.nd_mecha_list]
        x_off = 0
        for nd in nd_list:
            if nd.isVisible():
                X, Y = nd.GetPosition()
                nd.SetPosition(x_off, Y)
                x_off += nd.GetContentSize()[0]

        W, H = nd_set.GetContentSize()
        X, Y = nd_set.GetPosition()
        nd_set.SetContentSize(x_off, H)
        nd_set.SetPosition('50%', Y)

    def _update_btn_state(self):
        nd_set = self._panel.nd_set
        is_ss = mecha_skin_utils.is_ss_level_skin(self._cur_clothing_id)
        nd_set.btn_ss.setVisible(is_ss)
        is_s_upgradable = mecha_skin_utils.is_s_skin_that_can_upgrade(self._cur_clothing_id)
        nd_set.btn_s_plus.setVisible(is_s_upgradable)
        is_open = skin_define_utils.is_open_by_clothing_id(self._cur_clothing_id)
        nd_set.btn_set.SetEnable(is_open)

    def update_nd_skin_choose(self, cur_mecha_id):
        self._cur_mecha_id = cur_mecha_id
        self._cur_lobby_mecha_id = battle_id_to_mecha_lobby_id(cur_mecha_id)
        self.list_skin_ui.RecycleAllItem()
        self._clothing_selected_index = 0
        self._group_clothing_selected_index = 0
        self._cur_create_skin_index = 0
        self.show_skin_list_cnf = mecha_skin_utils.get_show_skin_list(cur_mecha_id)
        nd_name = self._panel.nd_name
        if nd_name:
            nd_name.lab_name_skin.setString(item_utils.get_mecha_name_by_id(cur_mecha_id))
            nd_name.lab_mech_type.setString(get_mecha_speciality_desc_str(cur_mecha_id))
        dressed_clothing_id = global_data.player.get_pve_using_mecha_skin(self._cur_lobby_mecha_id)
        if dressed_clothing_id is not None and dressed_clothing_id in self.show_skin_list_cnf:
            self._clothing_selected_index = self.show_skin_list_cnf.index(dressed_clothing_id)
            self._group_clothing_selected_index = 0
            group_skin_list = skin_define_utils.get_group_skin_list(dressed_clothing_id)
            if group_skin_list:
                self._group_clothing_selected_index = group_skin_list.index(dressed_clothing_id)
        self._panel.setVisible(False)
        self.clear_async_action()
        self._async_action = self._parent.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.create_skin_item),
         cc.DelayTime.create(0.01)])))
        self.update_clothing_status()
        return

    def create_skin_item(self):
        start_time = time.time()
        while self._cur_create_skin_index < len(self.show_skin_list_cnf):
            clothing_id = self.show_skin_list_cnf[self._cur_create_skin_index]
            item_config = confmgr.get('lobby_item', str(self._cur_clothing_id))
            if item_config is not None:
                clothing_item = self.list_skin_ui.ReuseItem()
                if not clothing_item:
                    clothing_item = self.list_skin_ui.AddTemplateItem()
                clothing_item.SetClipObjectRecursion(self._panel.nd_list_skin.nd_cut)
            else:
                clothing_item = self.list_skin_ui.AddTemplateItem()
                log_error('clothing_id has not conf', self._cur_clothing_id)
            self.init_clothing_item(item_config, clothing_item, clothing_id)
            self._clothing_id_2_item[clothing_id] = clothing_item
            base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(clothing_id)
            if base_skin_id is None:
                base_skin_id = clothing_id
            self._cur_create_skin_index = self._cur_create_skin_index + 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        self._panel.setVisible(True)
        self.list_container.init_list()
        if self._clothing_selected_index != 0:
            self.list_container.force_select_clothing(self._clothing_selected_index)
        return

    def init_clothing_item(self, item_config, clothing_item, clothing_id):
        item_no = item_config.get('item_no')
        name_text = item_utils.get_lobby_item_name(clothing_id)
        clothing_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(clothing_item, clothing_id)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id))
        if skin_cfg:
            item_utils.check_skin_tag(clothing_item.nd_kind, clothing_id)
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                clothing_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
            if mecha_skin_utils.is_ss_level_skin(clothing_id) and self.check_has_ss_card_effect_res(clothing_id):
                self.attach_effect_to_ss_card(clothing_item, clothing_id)
            else:
                self.detach_effect_to_ss_card(clothing_item)
        show_remain_time(clothing_item.nd_time, clothing_item.nd_time.lab_time, clothing_id)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
        red_point_utils.show_red_point_template(clothing_item.nd_new, show_new)
        self.init_clothing_item_lock(clothing_id, clothing_item)
        return

    def init_clothing_item_lock(self, clothing_id, clothing_item):
        player = global_data.player
        clothing_data = player.get_item_by_no(clothing_id) if player else None
        if player:
            is_share, share_type = player.is_share_mecha_skin(clothing_id)
        else:
            is_share, share_type = False, None
        is_priv_free = is_share and share_type == SKIN_SHARE_TYPE_PRIV
        if is_priv_free:
            is_teammate_lobby_skin = player.is_teammate_lobby_skin(clothing_id)
            is_share = bool(is_share and not is_teammate_lobby_skin)
        is_unlock = clothing_data is not None or is_share
        clothing_item.nd_lock.setVisible(not is_unlock)
        clothing_item.nd_share.setVisible(is_priv_free)
        return

    def update_nd_get(self):
        nd_get = self._panel.nd_get
        is_owned = self.get_current_skin_is_own()
        if is_owned:
            nd_get.setVisible(False)
            return
        nd_get.setVisible(True)
        btn_get = nd_get.btn_get
        access_txt = item_utils.get_item_access(str(self._cur_clothing_id))
        if access_txt:
            nd_get.lab_get.setString(access_txt)
        else:
            nd_get.lab_get.setString('')
        if item_utils.can_jump_to_ui(str(self._cur_clothing_id)):
            btn_get.SetEnable(True)
            btn_get.SetText(get_text_by_id(82290))
            nd_get.temp_price.setVisible(False)
        else:
            goods_id = self._mecha_skin_conf.get(str(self._cur_clothing_id), {}).get('goods_id')
            price_list = get_mall_item_price(goods_id)
            from logic.gutils.mall_utils import get_goods_item_open_date, check_limit_time_lottery_open_info
            open_date_range = get_goods_item_open_date(goods_id)
            opening, _ = check_limit_time_lottery_open_info(open_date_range)
            if price_list and opening:
                cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
                default_skin = self._lobby_mecha_config.get(str(cur_mecha_item_id)).get('default_fashion')[0]
                if int(default_skin) == int(self._cur_clothing_id):
                    text_id = 82290
                else:
                    text_id = 81807
                btn_get.SetEnable(True)
                btn_get.SetText(get_text_by_id(text_id))
                nd_get.temp_price.setVisible(True)
                splice_price(nd_get.temp_price, price_list)
            else:
                btn_get.SetEnable(False)
                btn_get.SetText(get_text_by_id(80828))
                nd_get.temp_price.setVisible(False)

    def get_current_skin_is_default(self):
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        clothing_id = self._cur_clothing_id
        default_skin = self._lobby_mecha_config.get(str(cur_mecha_item_id)).get('default_fashion')[0]
        is_default_skin = False
        if int(default_skin) == int(self._cur_clothing_id):
            clothing_id = cur_mecha_item_id
            is_default_skin = True
        return (is_default_skin, clothing_id)

    def get_current_skin_is_own(self):
        is_default_skin, clothing_id = self.get_current_skin_is_default()
        if global_data.player:
            clothing_data = global_data.player.get_item_by_no(clothing_id) if 1 else None
            is_owned = False
            if is_default_skin:
                if clothing_data and (clothing_data.get_expire_time() == -1 or clothing_data.get_expire_time() > get_server_time()):
                    is_owned = True
        else:
            is_owned = clothing_data
        if global_data.player:
            is_share, share_type = global_data.player.is_share_mecha_skin(clothing_id)
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
            is_intimacy_share_mecha = global_data.player.is_intimacy_share_mecha(cur_mecha_item_id)
        else:
            is_share, share_type = False, None
            is_intimacy_share_mecha = False
        return bool(is_owned or is_intimacy_share_mecha)

    def check_has_ss_card_effect_res(self, skin_id):
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(skin_id)
        light_template_path = 'mech_display/i_light_%s_1' % base_skin_id
        find_res = global_data.uisystem.CheckHasTemplate(light_template_path)
        return find_res

    def attach_effect_to_ss_card(self, ui_item, skin_id):
        ui_item.img_frame.setVisible(False)
        if self.show_ss_card_effect:
            ui_item.img_skin_0.setVisible(True)
            img_1 = 'gui/ui_res_2/item/mecha_skin/%s_1.png' % skin_id
            if skin_id in USE_SAME_PIC_CLOTHING_IDS or not cc.FileUtils.getInstance().isFileExist(img_1):
                ui_item.img_skin_0.SetDisplayFrameByPath('', 'gui/ui_res_2/item/mecha_skin/%s.png' % skin_id)
            else:
                ui_item.img_skin_0.SetDisplayFrameByPath('', img_1)

        def add_func(cache_ui_item):
            if cache_ui_item:
                ui_item.nd_frame_ss.AddChild('temp_ss_frame', cache_ui_item)

        check_has_node = hasattr(ui_item.nd_frame_ss, 'temp_ss_frame') and ui_item.nd_frame_ss.temp_ss_frame and ui_item.nd_frame_ss.temp_ss_frame.getParent()
        if not check_has_node:
            cache_ret = global_data.item_cache_without_check.pop_item_by_json(CARD_SS_FRAME_TEMPLATE, add_func)
            if cache_ret:
                item_widget = cache_ret
            else:
                item_widget = global_data.uisystem.load_template_create(CARD_SS_FRAME_TEMPLATE)
                add_func(item_widget)
            item_widget.SetPosition('50%', '50%')
            item_widget.img_frame_ss.getGLProgramState().setUniformFloat('Hue', 0.0)
        if not self.show_ss_card_effect:
            return
        check_has_light = hasattr(ui_item.temp_light, 'nd_light') and ui_item.temp_light.nd_light and ui_item.temp_light.nd_light.getParent()
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(skin_id)
        light_template_path = 'mech_display/i_light_%s_1' % base_skin_id

    def detach_effect_to_ss_card(self, ui_item):
        ui_item.img_frame.setVisible(True)
        ui_item.img_skin_0.setVisible(False)
        item_cache = global_data.item_cache_without_check
        if hasattr(ui_item.nd_frame_ss, 'temp_ss_frame'):
            temp_ss_frame = ui_item.nd_frame_ss.temp_ss_frame
            if temp_ss_frame:
                if item_cache.check_can_put_back(temp_ss_frame, CARD_SS_FRAME_TEMPLATE):
                    item_cache.put_back_item_to_cache(temp_ss_frame, CARD_SS_FRAME_TEMPLATE)
        if hasattr(ui_item.temp_light, 'nd_light'):
            nd_light = ui_item.temp_light.nd_light
            if nd_light:
                if item_cache.check_can_put_back(nd_light, nd_light._ccb_template_path):
                    item_cache.put_back_item_to_cache(nd_light, nd_light._ccb_template_path)

    def _on_buy_good_success(self, *args):
        self.update_clothing_status()

    def clear_async_action(self):
        if self._async_action is not None:
            self._parent.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def get_current_id(self):
        return (
         self._cur_mecha_id, self._cur_clothing_id)

    def destroy(self):
        self.process_events(False)
        self.clear_async_action()
        if self.list_container:
            self.list_container.release()
            self.list_container = None
        self._mecha_skin_conf = None
        self._cur_mecha_id = None
        self._cur_clothing_id = None
        self._clothing_selected_index = None
        self._group_clothing_selected_index = None
        self._cur_create_skin_index = None
        self.nd_mecha_list = None
        self.list_mecha_nd = None
        self._clothing_id_2_item = {}
        self.show_skin_list_cnf = None
        self.show_ss_card_effect = None
        return

    def get_free_wsfx_id(self, skin_id):
        free_wsfx_id = None
        shiny_weapon_list = mecha_skin_utils.get_mecha_shiny_weapon_list(skin_id)
        for w_sfx in reversed(shiny_weapon_list):
            if w_sfx in self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {}):
                free_wsfx_id = w_sfx

        return free_wsfx_id

    def is_priv_free_mecha_skin(self, skin_id):
        mecha_skin_ids = self.priv_free_mecha_fashions.get('mecha_skin_ids', {})
        mecha_wsfx_ids = self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {})
        if global_data.player and global_data.player.get_priv_enjoy_free_cnt() <= 0:
            return False
        if mecha_skin_utils.is_default_mecha_skin(skin_id, self._cur_lobby_mecha_id):
            return False
        if skin_id not in mecha_skin_ids:
            return False
        skin_item = global_data.player and global_data.player.get_item_by_no(skin_id)
        if not skin_item:
            return True
        wsfx_id = skin_item.get_weapon_sfx()
        if wsfx_id:
            return False
        free_wsfx_id = self.get_free_wsfx_id(skin_id)
        has_free_wsfx_id = free_wsfx_id in mecha_wsfx_ids
        if has_free_wsfx_id:
            return True
        return False

    def is_teammate_lobby_skin(self, skin_id):
        lobby_skin_ids = self.priv_free_mecha_fashions.get('lobby_skin_ids', {})
        return skin_id in lobby_skin_ids

    def get_priv_fashion_data(self, skin_id):
        if not self.is_priv_free_mecha_skin(skin_id):
            return {}
        mecha_wsfx_ids = self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {})
        free_wsfx_id = self.get_free_wsfx_id(skin_id)
        has_free_wsfx_id = free_wsfx_id in mecha_wsfx_ids
        mecha_fashion = {FASHION_POS_SUIT: skin_id
           }
        if has_free_wsfx_id:
            mecha_fashion[FASHION_POS_WEAPON_SFX] = free_wsfx_id
        return {'mecha_fashion': mecha_fashion,
           'is_priv_free': True
           }

    def _on_add_teammate(self, *args):
        self.update_clothing_status()

    def _on_undress_priv_skin(self, *args):
        self._skin_up_select_callback(0)
        self.list_container.force_select_clothing(self._clothing_selected_index)

    def _on_update_priv_free_mecha_fashions(self, *args):
        self._cur_clothing_id, group_skin_list = self.get_rel_clothing()
        clothing_item = self._clothing_id_2_item.get(self._cur_clothing_id)
        if clothing_item and clothing_item.isValid():
            self.init_clothing_item_lock(self._cur_clothing_id, clothing_item)
            self.update_nd_get()
            self.update_priv_status(self._cur_clothing_id)