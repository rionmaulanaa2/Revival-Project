# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/PetSkinListWidget.py
import six
import six_ex
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.PetSkinGetUseBuyWidget import PetSkinGetUseBuyWidget
from logic.gutils.items_book_utils import get_filter_item_show_name_with_left_time, get_items_skin_conf, get_item_fashion_no, get_sorted_item_list
from logic.client.const.items_book_const import PET_ID
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, get_lobby_item_pic_by_item_no, check_skin_tag, check_skin_bg_tag, is_itemtype_in_serving
from common.framework import Functor
from logic.gutils.template_utils import init_tempate_mall_i_item, show_remain_time
from logic.gutils import lobby_model_display_utils, red_point_utils
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
from logic.gcommon.item.item_const import ITEM_NO_PET_PROF_CARD_LIST
from logic.gcommon.common_const.shop_const import PET_DAILY_EXP
from logic.gcommon.common_const.ui_operation_const import ENABLE_PET_TRANSPARENT, ENABLE_PET_INTERACT_IN_BATTLE
ROTATE_FACTOR = 850
PET_ITEM_NO = 11001
PET_OFF_POS = [-4, 0, 0]
SPEC_ANIM_TAG = 99
TIMER_INTER = 0.025

class PetSkinListWidget(WidgetExtModelPic):

    def __init__(self, parent, panel):
        super(PetSkinListWidget, self).__init__(panel)
        self.parent = parent
        self.panel = panel
        self.panel_hide = False
        self.daily_state = global_data.player.get_pet_daily_state()
        self.data_dict = confmgr.get('c_pet_info', default={})
        self.skin_config_dict = get_items_skin_conf(PET_ID)
        self.cur_model_skin_id = None
        self.cur_skin_id = None
        self.cur_skin_list = None
        self.cur_skin_idx = 0
        self.cur_skin_level = 0
        self.cur_special_anim_name = None
        self.special_anim_inter = 5
        self.cur_show_level = 0
        self.max_level = 6
        self.prog_timer_id = None
        self.cur_show_exp = 0
        self.target_exp = 0
        valid_skin_list = []
        inner_skin_list = []
        for skin_id in six_ex.keys(self.data_dict):
            if not is_itemtype_in_serving(skin_id):
                continue
            base_skin = self.data_dict.get(str(skin_id), {}).get('base_skin', skin_id)
            if str(base_skin) != str(skin_id):
                continue
            if global_data.player:
                skin_id = global_data.player.get_pet_sub_skin_choose(skin_id)
            if self.skin_config_dict.get(skin_id, {}).get('inner_skin', 0):
                inner_skin_list.append(skin_id)
            else:
                valid_skin_list.append(skin_id)

        self.skin_list = valid_skin_list
        self.owned_skin_list = []
        self.init_scene()
        self.init_widget()
        self.init_event(True)
        return

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def init_event(self, bind):
        func = global_data.emgr.bind_events if bind else global_data.emgr.unbind_events
        func({'pet_daily_state_changed': self.on_pet_daily_state_changed,
           'pet_choosen_changed': self.on_pet_choosen_changed,
           'pet_info_updated': self.update_level_widget,
           'display_model_end_show_anim': self.model_end_show_anim
           })

    def init_widget(self):
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn)
        self._skin_get_use_buy_widget = PetSkinGetUseBuyWidget(self, self.panel.btn_buy_1, self.panel.btn_use, self.panel.btn_cancel, self.panel.btn_go, self.panel.temp_price, self.panel.lab_get_method)
        self._skin_list_widget = SkinItemListWidget(self, self.panel.list_skin, self.on_create_skin_item, 6)
        self._use_item_widget = PetProficiencyUseItemWidget(self.panel)
        self.panel.nd_touch.BindMethod('OnDrag', self.on_drag_touch_layer)
        self.panel.btn_add.BindMethod('OnClick', Functor(self.on_show_add_proficiency, True))
        self.panel.nd_add_proficiency.nd_close.BindMethod('OnClick', Functor(self.on_show_add_proficiency, False))
        self.panel.btn_free.lab_exp.SetString('+{}'.format(PET_DAILY_EXP))
        self.panel.btn_free.setVisible(False)

        @self.panel.btn_free.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            NormalConfirmUI2(content=get_text_by_id(634881, (get_lobby_item_name(self.cur_skin_id), PET_DAILY_EXP, PET_DAILY_EXP)), cancel_text=19002, on_confirm=callback)

        def callback():
            if global_data.player:
                self.panel.btn_free.SetEnable(False)
                global_data.player.get_pet_daily_reward(self.cur_skin_id)

        self.panel.nd_interact.setVisible(False)
        self.panel.nd_transparent.setVisible(False)
        self.panel.nd_enemy_visible.setVisible(False)

        @self.panel.nd_interact.btn.callback()
        def OnClick(btn, touch):
            self.panel.nd_interact.choose.setVisible(not self.panel.nd_interact.choose.isVisible())
            global_data.player.write_setting(ENABLE_PET_INTERACT_IN_BATTLE, not self.panel.nd_interact.choose.isVisible(), True)

        self.panel.nd_interact.choose.setVisible(not bool(global_data.player.get_setting(ENABLE_PET_INTERACT_IN_BATTLE)))

        @self.panel.nd_transparent.btn.callback()
        def OnClick(btn, touch):
            self.panel.nd_transparent.choose.setVisible(not self.panel.nd_transparent.choose.isVisible())
            global_data.player.write_setting(ENABLE_PET_TRANSPARENT, self.panel.nd_transparent.choose.isVisible(), True)

        self.panel.nd_transparent.choose.setVisible(bool(global_data.player.get_setting(ENABLE_PET_TRANSPARENT)))

        @self.panel.nd_enemy_visible.btn.callback()
        def OnClick(btn, touch):
            self.panel.nd_enemy_visible.choose.setVisible(not self.panel.nd_enemy_visible.choose.isVisible())
            global_data.player.set_pet_enemy_visible(not self.panel.nd_enemy_visible.choose.isVisible())

        self.panel.nd_enemy_visible.choose.setVisible(not global_data.player.get_pet_enemy_visible())
        self.refresh_owned_skin_list()
        self.update_collect_data()
        self.cur_skin_list = self.owned_skin_list if self._own_widget.get_own_switch() else self.skin_list
        choosen_pet = global_data.player and global_data.player.get_choosen_pet()
        self.cur_skin_idx = self.cur_skin_list.index(choosen_pet) if choosen_pet in self.cur_skin_list else 0
        self._skin_list_widget.update_skin_data(self.cur_skin_list, init_index=self.cur_skin_idx)

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.cur_skin_list)
        if valid:
            skin_no = self.cur_skin_list[index]
            item_widget.nd_content.setVisible(True)
            item_widget.item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(get_lobby_item_name(skin_no))
            item_widget.choose.setVisible(False)
            item_fashion_no = global_data.player and global_data.player.get_choosen_pet()
            item_widget.img_using.setVisible(item_fashion_no == int(skin_no))
            item_widget.img_lock.setVisible(not self._own_widget.has_item(skin_no))
            check_skin_tag(item_widget.nd_kind, skin_no)
            check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            prev_index = self.cur_skin_idx
            self.cur_skin_idx = index
            skin_no = self.cur_skin_id = self.cur_skin_list[index]
            self.max_level = self.data_dict[skin_no].get('max_level', 6)
            skin_item = global_data.player.get_item_by_no(int(skin_no))
            item_widget = self.panel.list_skin.GetItem(index)
            self.panel.nd_setting.setVisible(bool(skin_item))
            self.panel.btn_free.setVisible(False)
            prev_item = self.panel.list_skin.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            goods_id = self.skin_config_dict[skin_no].get('goods_id', None)
            item_widget.choose.setVisible(True)
            self._skin_get_use_buy_widget.update_target_item_no(PET_ITEM_NO, skin_no, goods_id)
            self.panel.lab_name.SetString(get_filter_item_show_name_with_left_time(PET_ITEM_NO, skin_no, 0))
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            if show_new:
                global_data.player.req_del_item_redpoint(skin_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(skin_no)
            self.update_level_widget(skin_changed=True)
            return

    def update_level_widget(self, skin_changed=False):
        skin_id = self.cur_skin_id
        pet_item = global_data.player.get_item_by_no(int(skin_id))
        skin_owned = pet_item is not None
        level_title_list = self.skin_config_dict[skin_id].get('level_title', [])
        skin_level = 0
        self.panel.bar_level.setVisible(False)
        if skin_owned:
            skin_level = pet_item.level
            exp = pet_item.exp
            self.set_show_exp(exp, skin_changed)
        self.panel.list_tab.setVisible(False)
        self.panel.list_tab.SetInitCount(self.max_level)
        for i in range(self.max_level):
            item = self.panel.list_tab.GetItem(i)
            unlock = i < skin_level
            item.btn_unlock.setVisible(unlock)
            item.btn_lock.setVisible(not unlock)
            item.lab_lv.SetString(get_text_by_id(17248).format(i + 1))
            if i < len(level_title_list):
                title = level_title_list[i] if 1 else ''
                item.btn_lock.lab_title.SetString(title)
                item.btn_unlock.lab_title.SetString(title)
                item.btn_unlock.BindMethod('OnClick', lambda btn, touch, lv=i: self.on_click_level_btn(lv))
                item.btn_lock.BindMethod('OnClick', lambda btn, touch, lv=i: self.on_click_level_btn(lv))

        if skin_changed:
            self.on_click_level_btn(max(skin_level - 1, 0))
        return

    def set_show_exp(self, exp, no_ani):
        self.panel.prog.StopPercentageAni()
        if no_ani:
            self.cur_show_exp = self.target_exp = exp
            self.update_prog()
            self.destroy_prog_timer()
        else:
            self.target_exp = exp
            exp_diff = exp - self.cur_show_exp
            self.exp_change_spd = max(exp_diff / 0.5, 30)
            if not self.prog_timer_id:
                self.prog_timer_id = global_data.game_mgr.register_logic_timer(self.update_prog, interval=TIMER_INTER, times=-1, mode=CLOCK, timedelta=True)
                self.update_prog()

    def update_prog(self, delta=0):
        if delta > 0:
            self.cur_show_exp += self.exp_change_spd * delta
            if self.cur_show_exp >= self.target_exp:
                self.cur_show_exp = self.target_exp
                self.destroy_prog_timer()
        exp_info = confmgr.get('c_pet_exp')._conf
        exp_roof = 0
        cur_level = 1
        for cur_level in range(1, 7):
            exp_roof = exp_info.get(str(cur_level + 1), None)
            if not exp_roof:
                break
            exp_roof = exp_roof['exp']
            if self.cur_show_exp < exp_roof:
                break

        if self.cur_show_level != cur_level:
            self.on_click_level_btn(cur_level - 1)
            self.cur_show_level = cur_level
        self.panel.lab_lv.SetString(get_text_by_id(17248, (cur_level,)))
        self.panel.bar_level.lab_exp.SetString('{}/{}'.format(int(self.cur_show_exp), exp_roof))
        self.panel.prog.SetPercentage(int(self.cur_show_exp * 100.0 / exp_roof) if exp_roof else 100)
        is_lv_max = cur_level >= self.max_level
        self.panel.btn_add.setVisible(not is_lv_max)
        if is_lv_max:
            self.panel.bar_level.lab_exp.SetString(870055)
            self.panel.prog.SetPercentage(100)
            self.destroy_prog_timer()
        return

    def destroy_prog_timer(self):
        if self.prog_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.prog_timer_id)
        self.prog_timer_id = None
        return

    def on_click_level_btn(self, level):
        skin_id = self.cur_skin_id
        if not skin_id:
            return
        else:
            skin_config = self.data_dict.get(skin_id, {})
            anim_name = self.skin_config_dict[skin_id].get('spec_show_anim', {}).get(str(level + 1), None)
            if anim_name is None and level > 0:
                for i in range(1, 4):
                    anim_info = skin_config.get('interact_anim{}'.format(i), {})
                    if not anim_info:
                        break
                    unlock_level = anim_info[2].get('level', 1)
                    if level + 1 == unlock_level:
                        anim_name = anim_info[0]
                        break

            if self.cur_model_skin_id == self.cur_skin_id and self.cur_skin_level == level + 1:
                if anim_name:
                    global_data.emgr.change_model_display_anim_directly.emit(anim_name, is_back_to_end_show_anim=True, anim_arg=[0])
                return
            if self.cur_skin_level > 0:
                item = self.panel.list_tab.GetItem(self.cur_skin_level - 1)
                if item:
                    item.btn_unlock.SetSelect(False)
                    item.btn_lock.SetSelect(False)
            self.cur_skin_level = level + 1
            item = self.panel.list_tab.GetItem(level)
            if item:
                item.btn_unlock.SetSelect(True)
                item.btn_lock.SetSelect(True)
            self.show_model(skin_id, spec_anim=anim_name)
            return

    def show_model(self, skin_no, spec_anim=None):
        skin_conf = self.data_dict.get(skin_no, {})
        if not skin_conf:
            return
        else:
            replaced_spec_anim = skin_conf['idle_anim2'][0] if spec_anim is None else spec_anim
            self.cur_special_anim_name = replaced_spec_anim = self.skin_config_dict[skin_no].get('anim_replace', {}).get(replaced_spec_anim, replaced_spec_anim)
            self.special_anim_inter = self.skin_config_dict[str(skin_no)].get('anim_inter', 5)
            self.panel.stopActionByTag(SPEC_ANIM_TAG)
            prev_skin_id = self.cur_model_skin_id
            self.cur_model_skin_id = skin_no
            model_data = lobby_model_display_utils.get_lobby_model_data(skin_no, pet_level=self.cur_skin_level)
            model_data[0]['can_rotate_on_show'] = True
            model_data[0]['off_position'] = PET_OFF_POS
            if prev_skin_id == skin_no:
                model_data[0]['show_anim'] = '' if spec_anim is None else replaced_spec_anim
            model_data[0]['end_anim'] = skin_conf['idle_anim'][0]
            self.ext_show_item_model(model_data, in_item_id=skin_no)
            return

    def model_end_show_anim(self, *args):
        if self.panel_hide:
            return
        self.panel.SetTimeOut(self.special_anim_inter, Functor(global_data.emgr.change_model_display_anim_directly.emit, self.cur_special_anim_name, is_back_to_end_show_anim=True, anim_arg=[0]), SPEC_ANIM_TAG)

    def update_collect_data(self):
        all_skin_cnt = len(self.skin_list)
        own_skin_cnt = len(self.owned_skin_list)
        self.panel.nd_sort.lab_collect.SetString('{}/{}'.format(own_skin_cnt, all_skin_cnt))
        self.panel.temp_prog.lab_got.SetString('%d/%d' % (own_skin_cnt, all_skin_cnt))
        self.panel.temp_prog.prog.SetPercentage(int(own_skin_cnt / float(all_skin_cnt) * 100))

    def on_click_own_btn(self, *args):
        self.cur_skin_list = self.owned_skin_list if self._own_widget.get_own_switch() else self.skin_list
        if self.cur_skin_id in self.cur_skin_list:
            self.cur_skin_idx = self.cur_skin_list.index(self.cur_skin_id)
        else:
            self.cur_skin_idx = 0
            self.cur_skin_id = self.cur_skin_list[0] if self.cur_skin_list else None
        self._skin_list_widget.update_skin_data(self.cur_skin_list, is_init=False, init_index=self.cur_skin_idx)
        return

    def refresh_owned_skin_list(self):
        self.skin_list = get_sorted_item_list(self.skin_list, sort_by_can_use=True)
        origin_owned_skin_list = self.owned_skin_list
        self.owned_skin_list = self._own_widget.get_data_has_own(self.skin_list)
        return origin_owned_skin_list != self.owned_skin_list

    def on_drag_touch_layer(self, btn, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def on_show_add_proficiency(self, show, *args):
        skin_id = self.cur_skin_id
        skin_owned = self._own_widget.has_item(skin_id)
        self.panel.nd_add_proficiency.setVisible(show and skin_owned)
        self._use_item_widget and self._use_item_widget.set_skin_id(skin_id)

    def on_pet_daily_state_changed(self, state):
        if self.daily_state ^ state:
            self.daily_state = state
            self.panel.btn_free.SetEnable(True)
            self.panel.btn_free.setVisible(False)

    def on_pet_choosen_changed(self, choosen_pet_id):
        self._skin_get_use_buy_widget.refresh_widget()
        for i, pet_id in enumerate(self.cur_skin_list):
            self.panel.list_skin.GetItem(i).img_using.setVisible(int(pet_id) == choosen_pet_id)

    def jump_to_item_no(self, item_no):
        item_no = str(item_no)
        if item_no in self.cur_skin_list:
            self.on_click_skin_item(self.cur_skin_list.index(item_no))

    def refresh_widget(self):
        if self.panel_hide:
            self.init_scene()
            self.show_model(self.cur_skin_id)
            self.panel_hide = False
        elif self.refresh_owned_skin_list():
            self.on_click_own_btn()

    def do_hide_panel(self):
        self.panel_hide = True

    def destroy(self):
        super(PetSkinListWidget, self).destroy()
        self.init_event(False)
        self._use_item_widget.destroy()
        self._use_item_widget = None
        self.destroy_prog_timer()
        return

    @staticmethod
    def get_widget_red_points():
        if not global_data.player:
            return False
        for pet_id, pet_info in six.iteritems(confmgr.get('c_pet_info')._conf):
            if global_data.lobby_red_point_data.get_rp_by_no(pet_id):
                return True

        return False


class PetProficiencyUseItemWidget(object):
    USE_CNT_LIST = [
     1, 2, 5]

    def __init__(self, nd):
        self.init_parameters()
        self.panel = nd
        self.skin_id = None
        self.skin_item = None
        self.skin_max_level = 6
        self.init_add_prof_item_list()
        self.init_event(True)
        return

    def set_skin_id(self, skin_id):
        self.skin_id = skin_id
        self.skin_item = global_data.player.get_item_by_no(int(skin_id))
        self.skin_max_level = confmgr.get('c_pet_info', str(skin_id), 'max_level', default=6)

    def init_parameters(self):
        self._prof_conf = confmgr.get('c_pet_exp')._conf
        self._dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        self._reward_levels = confmgr.get('proficiency_config', 'RewardLevels')
        self._max_dan_lv = len(self._dan_conf)
        self._max_level = len(self._prof_conf)
        self._cur_mecha_type = None
        self._reward_item_dict = None
        self._card_item_dict = {}
        self._cnt_timer = None
        self._use_cnt_idx = 0
        self._use_timer = None
        self._can_use = True
        self._cur_select_reward_btn = None
        return

    def init_event(self, bind):
        func = global_data.emgr.bind_events if bind else global_data.emgr.unbind_events
        func({'on_lobby_bag_item_changed_event': self.on_card_num_changed
           })

    def destroy(self):
        self.cancel_cnt_timer()
        self.cancel_use_timer()
        self.panel = None
        self._cur_mecha_type = None
        self._prof_conf = {}
        self._dan_conf = {}
        self._max_level = 0
        self._max_dan_lv = 0
        self.init_event(False)
        return

    def init_add_prof_item_list(self):
        nd = self.panel
        list_item = nd.nd_add_proficiency.list_item
        list_item.SetInitCount(len(ITEM_NO_PET_PROF_CARD_LIST))
        for i, item_no in enumerate(ITEM_NO_PET_PROF_CARD_LIST):
            nd_item = list_item.GetItem(i)
            nd_item.lab_name.SetString(get_lobby_item_name(item_no))
            nd_item.lab_describe.SetString(get_lobby_item_desc(item_no))
            item_num = global_data.player.get_item_num_by_no(item_no)
            init_tempate_mall_i_item(nd_item.temp_item, item_no, item_num, show_all_num=True)
            if item_num <= 0:
                nd_item.nd_get.setVisible(True)
            else:
                nd_item.nd_get.setVisible(False)
            nd_item.btn_add.item_no = item_no
            nd_item.btn_add.item_num = item_num
            self._card_item_dict[item_no] = nd_item

            @nd_item.btn_add.unique_callback()
            def OnBegin(btn, touch):
                if self._use_timer:
                    return False
                self._use_cnt_idx = 0
                if self.use_card(btn.item_no):
                    btn.use_card = True
                    self._cnt_timer = global_data.game_mgr.register_logic_timer(self.on_add_use_cnt, 2, mode=CLOCK)
                    self._use_timer = global_data.game_mgr.register_logic_timer(self.use_card, 0.3, (btn.item_no,), mode=CLOCK)
                return True

            @nd_item.btn_add.unique_callback()
            def OnClick(btn, touch):
                item_num = global_data.player.get_item_num_by_no(btn.item_no)
                if not btn.use_card and item_num == 0:
                    from logic.gutils.jump_to_ui_utils import jump_to_mall
                    from logic.gutils.mall_utils import limite_pay
                    goods_id_dict = {'71700008': '701700116','71700009': '701700117' if limite_pay('701700118') else '701700118'}
                    jump_to_mall(goods_id_dict[str(btn.item_no)])
                btn.use_card = False
                return True

            @nd_item.btn_add.unique_callback()
            def OnEnd(btn, touch):
                self.cancel_cnt_timer()
                self.cancel_use_timer()
                self._use_cnt_idx = 0
                self._can_use = True
                return True

    def use_card(self, item_no):
        if not self._can_use:
            return False
        if self.skin_item.level >= self.skin_max_level:
            global_data.game_mgr.show_tip(634882)
            return False
        item = global_data.player.get_item_by_no(item_no)
        item_num = global_data.player.get_item_num_by_no(item_no)
        use_cnt = min(item_num, self.USE_CNT_LIST[self._use_cnt_idx])
        if use_cnt > 0:
            global_data.player.use_item(item.get_id(), use_cnt, {'pet_id': int(self.skin_id)})
            self._can_use = False
            return True
        return False

    def on_add_use_cnt(self):
        self._use_cnt_idx += 1
        if self._use_cnt_idx == len(self.USE_CNT_LIST) - 1:
            self.cancel_cnt_timer()

    def cancel_cnt_timer(self):
        if self._cnt_timer:
            global_data.game_mgr.unregister_logic_timer(self._cnt_timer)
        self._cnt_timer = None
        return

    def cancel_use_timer(self):
        if self._use_timer:
            global_data.game_mgr.unregister_logic_timer(self._use_timer)
        self._use_timer = None
        return

    def on_card_num_changed(self):
        for item_no in ITEM_NO_PET_PROF_CARD_LIST:
            nd_item = self._card_item_dict.get(item_no, None)
            if not nd_item:
                continue
            new_item_num = global_data.player.get_item_num_by_no(item_no)
            if new_item_num < nd_item.btn_add.item_num:
                self._can_use = True
            nd_item.btn_add.item_num = new_item_num
            nd_item.temp_item.lab_quantity.setVisible(new_item_num > 0)
            nd_item.temp_item.lab_quantity.SetString(str(new_item_num))
            if new_item_num <= 0:
                nd_item.nd_get.setVisible(True)
            else:
                nd_item.nd_get.setVisible(False)

        return