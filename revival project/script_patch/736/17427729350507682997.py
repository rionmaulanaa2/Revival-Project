# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PetLevelWidget.py
from __future__ import absolute_import
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, check_skin_tag
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.item.item_const import ITEM_NO_PET_PROF_CARD_LIST
from logic.gutils.items_book_utils import get_items_skin_conf
from logic.client.const.items_book_const import PET_ID
from common.utils.timer import CLOCK
from common.cfg import confmgr
TIMER_INTER = 0.025

class PetLevelWidget(object):

    def __init__(self, panel, on_click_level_btn=None):
        self.panel = panel
        self.init_params(on_click_level_btn)
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self, on_click_level_btn):
        self._on_click_level_btn = on_click_level_btn
        self._data_dict = confmgr.get('c_pet_info', default={})
        self._skin_config_dict = get_items_skin_conf(PET_ID)
        self._cur_show_level = 0
        self._cur_show_exp = 0
        self._target_exp = 0
        self._exp_change_spd = 0
        self._prog_timer_id = None
        return

    def init_ui(self):
        self._use_item_widget = PetProficiencyUseItemWidget(self.panel)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pet_info_updated': self._update_level_widget
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui_event(self):

        @self.panel.btn_add.unique_callback()
        def OnClick(btn, touch):
            self._on_show_add_proficiency(True)

        @self.panel.nd_add_proficiency.nd_close.unique_callback()
        def OnClick(*args):
            self._on_show_add_proficiency(False)

    def _on_show_add_proficiency(self, show, *args):
        skin_id = self._cur_skin_id
        skin_owned = global_data.player.has_item_by_no(int(skin_id))
        self.panel.nd_add_proficiency.setVisible(show and skin_owned)
        self._use_item_widget and self._use_item_widget.set_skin_id(skin_id)

    def update_skin_id(self, skin_id):
        self._cur_skin_id = skin_id
        self._max_level = self._data_dict[str(skin_id)].get('max_level', 6)
        self.panel.bar_level.lab_name.SetString(get_lobby_item_name(skin_id))
        check_skin_tag(self.panel.temp_kind, skin_id)
        self._update_level_widget(skin_changed=True)

    def _update_level_widget(self, skin_changed=False):
        skin_id = self._cur_skin_id
        pet_item = global_data.player and global_data.player.get_item_by_no(int(skin_id))
        skin_owned = pet_item is not None
        level_title_list = self._skin_config_dict[str(skin_id)].get('level_title', [])
        skin_level = 0
        self.panel.nd_info.setVisible(skin_owned)
        self.panel.lab_not_have.setVisible(not skin_owned)
        self.panel.lab_name.SetPosition('50%-100', '50%16' if skin_owned else '50%9')
        if skin_owned:
            base_skin = self._data_dict.get(str(skin_id), {}).get('base_skin', skin_id)
            base_pet_item = global_data.player and global_data.player.get_item_by_no(int(base_skin))
            skin_level = base_pet_item.level
            exp = base_pet_item.exp
            self._set_show_exp(exp, skin_changed)
        if self._on_click_level_btn:
            self.panel.list_tab.SetInitCount(self._max_level)
            for i in range(self._max_level):
                item = self.panel.list_tab.GetItem(i)
                unlock = i < skin_level
                item.btn_unlock.setVisible(unlock)
                item.btn_lock.setVisible(not unlock)
                item.lab_lv.SetString(get_text_by_id(17248).format(i + 1))
                if i < len(level_title_list):
                    title = level_title_list[i] if 1 else ''
                    item.btn_lock.lab_title.SetString(title)
                    item.btn_unlock.lab_title.SetString(title)
                    item.btn_unlock.BindMethod('OnClick', lambda btn, touch, lv=i: self._on_click_level_btn(lv))
                    item.btn_lock.BindMethod('OnClick', lambda btn, touch, lv=i: self._on_click_level_btn(lv))

            if skin_changed:
                self._on_click_level_btn(max(skin_level - 1, 0))
        return

    def _set_show_exp(self, exp, no_ani):
        self.panel.prog.StopPercentageAni()
        if no_ani:
            self._cur_show_exp = self._target_exp = exp
            self._update_prog()
            self._destroy_prog_timer()
        else:
            self._target_exp = exp
            exp_diff = exp - self._cur_show_exp
            self._exp_change_spd = max(exp_diff / 0.5, 30)
            if not self._prog_timer_id:
                self._prog_timer_id = global_data.game_mgr.register_logic_timer(self._update_prog, interval=TIMER_INTER, times=-1, mode=CLOCK, timedelta=True)
                self._update_prog()

    def _update_prog(self, delta=0):
        if not self.panel:
            return
        else:
            if delta > 0:
                self._cur_show_exp += self._exp_change_spd * delta
                if self._cur_show_exp >= self._target_exp:
                    self._cur_show_exp = self._target_exp
                    self._destroy_prog_timer()
            exp_info = confmgr.get('c_pet_exp')._conf
            exp_roof = 0
            cur_level = 1
            for cur_level in range(1, self._max_level + 1):
                exp_roof = exp_info.get(str(cur_level + 1), None)
                if not exp_roof:
                    break
                exp_roof = exp_roof['exp']
                if self._cur_show_exp < exp_roof:
                    break

            if self._on_click_level_btn:
                if self._cur_show_level != cur_level:
                    self._on_click_level_btn(cur_level - 1)
                    self._cur_show_level = cur_level
            if not self.panel:
                return
            self.panel.lab_lv.SetString(get_text_by_id(17248, (cur_level,)))
            self.panel.bar_level.nd_info.lab_exp.SetString('{}/{}'.format(int(self._cur_show_exp), exp_roof))
            self.panel.prog.SetPercentage(int(self._cur_show_exp * 100.0 / exp_roof) if exp_roof else 100)
            is_lv_max = cur_level >= self._max_level
            self.panel.btn_add.setVisible(not is_lv_max)
            if is_lv_max:
                self.panel.bar_level.nd_info.lab_exp.SetString(870055)
                self.panel.prog.SetPercentage(100)
                self._destroy_prog_timer()
            return

    def _destroy_prog_timer(self):
        if self._prog_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._prog_timer_id)
        self._prog_timer_id = None
        return

    def destroy(self):
        self.panel = None
        self.process_events(False)
        self._use_item_widget.destroy()
        self._use_item_widget = None
        self._destroy_prog_timer()
        return


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