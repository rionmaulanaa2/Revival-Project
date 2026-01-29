# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgeWallConfigUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from six.moves import filter
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils import career_utils
from logic.gcommon import time_utility
from common.uisys.basepanel import BasePanel
from logic.comsys.career.CareerBadgeWallInfoUI import BadgeWallBadgeData
from logic.gcommon.common_const.rank_career_const import MAIN_BRANCH_BATTLE, MAIN_BRANCH_MECHA
from logic.gcommon.common_const.rank_career_const import BADGE_BRONZE_LV, BADGE_SILVER_LV, BADGE_GOLD_LV
QUICK_CAT_ALL = 1
QUICK_CAT_BATTLE = 2
QUICK_CAT_MECHA = 3
QUICK_TAG_UI_CONF = {QUICK_CAT_ALL: ('gui/ui_res_2/life/display_wall/btn_life_tab_all_2.png', 80566),
   QUICK_CAT_BATTLE: ('gui/ui_res_2/life/btn_life_tab_battle_2.png', 80481),
   QUICK_CAT_MECHA: ('gui/ui_res_2/life/btn_life_tab_mech_2.png', 80204)
   }

class CareerBadgeWallConfigUI(BasePanel):
    PANEL_CONFIG_NAME = 'life/display_wall/display_wall'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': '_close_click',
       'btn_tips_left.OnClick': '_tips_btn_clicked',
       'btn_clean.OnClick': '_btn_clean_clicked',
       'nd_bg.OnClick': '_nd_bg_clicked',
       'btn_select_mode.OnClick': '_btn_select_mode_clicked',
       'btn_select_mode_back.OnClick': '_btn_select_mode_back_clicked',
       'nd_block_right_after.OnClick': '_nd_block_right_after_clicked',
       'btn_close_quick.OnClick': '_close_quick_clicked',
       'btn_tips_quick.OnClick': '_btn_tips_quick_clicked',
       'btn_select_medal_type.OnClick': '_btn_select_medal_type_clicked'
       }
    GLOBAL_EVENT = {'on_wall_badge_set': '_on_wall_badge_set'
       }
    SLOT_CNT = 8
    QUICK_SEL_MAX_CNT = 8

    def on_init_panel(self, *args, **kwargs):
        super(CareerBadgeWallConfigUI, self).on_init_panel()
        self._init_members()
        self._init_views()
        self._init_ui_events()
        self.panel.PlayAnimation('in')
        self.panel.PlayAnimation('before_in')
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.show_main_ui()
        self._badge_tips_wgt.on_finalize_panel()
        self._badge_tips_wgt = None
        super(CareerBadgeWallConfigUI, self).on_finalize_panel()
        return

    def _init_members(self):
        self._owned_badge_ids = None
        self._editing_badge_data_dict = {}
        self._right_list_filter = None
        self._right_badge_data_list = []
        self._in_edit_mode = False
        self._left_selected_idx = -1
        self._right_selected_idx = -1
        self._left_list_node = self.panel.list_medal_left
        self._right_list_node = self.panel.list_medal_right
        self._right_tab_btn_map = {MAIN_BRANCH_BATTLE: self.panel.btn_battle_right,
           MAIN_BRANCH_MECHA: self.panel.btn_mecha_right
           }
        self._in_quick_sel_mode = False
        self._cur_quick_cat = None
        self._quick_badge_data_list = []
        self._quick_sel_map = {}
        self._quick_sel_rev_map = {}
        self._quick_lv_filters = set()
        self._gold_lv_filters = self._gen_is_lv_filter(BADGE_GOLD_LV)
        self._silber_lv_filters = self._gen_is_lv_filter(BADGE_SILVER_LV)
        self._bronze_lv_filters = self._gen_is_lv_filter(BADGE_BRONZE_LV)
        self.filter_ui_map = {self._gold_lv_filters: self.panel.btn_gold,
           self._silber_lv_filters: self.panel.btn_silver,
           self._bronze_lv_filters: self.panel.btn_copper
           }
        self._quick_list_node = self.panel.list_medal_quick
        from logic.comsys.career.CareerBadgeTipsWidget import CareerBadgeTipsWidget
        self._badge_tips_wgt = CareerBadgeTipsWidget(self.panel.temp_medal_tips_right)
        self._badge_tips_wgt.on_init_panel()
        return

    def _drop_editing_badge(self, idx):
        if idx in self._editing_badge_data_dict:
            del self._editing_badge_data_dict[idx]
            self._request_sync()
            self._refresh_left_side_list()

    def _get_right_selected_badge_data(self):
        return self._get_right_list_badge_data(self._right_selected_idx)

    def _init_views(self):
        self._init_left_list()
        quick_cat_node_conf = {QUICK_CAT_ALL: (
                         self.panel.btn_all_quick,),
           QUICK_CAT_BATTLE: (
                            self.panel.btn_battle_quick,),
           QUICK_CAT_MECHA: (
                           self.panel.btn_mecha_quick,)
           }
        for quick_cat, conf in six.iteritems(quick_cat_node_conf):
            btn_node = conf[0]

            @btn_node.callback()
            def OnClick(btn, touch, quick_cat=quick_cat):
                self._sel_quick_cat(quick_cat)

            def state_cb(state, btn_node=btn_node):
                from common.uisys.uielment.CCButton import STATE_SELECTED
                seled = state == STATE_SELECTED
                btn_node.icon_btn.SetSelect(seled)

            btn_node.set_state_changed_cb(state_cb)

        self._init_badge_cnt_by_lv()
        self._editing_badge_data_dict = career_utils.get_my_c_wall_dict()
        self._refresh_left_side_list()
        self._select_right_filter(MAIN_BRANCH_BATTLE)
        for ftr in self.filter_ui_map:
            btn = self.filter_ui_map[ftr]

            @btn.callback()
            def OnClick(btn, touch, ftr=ftr):
                self._change_quick_lv_filter(ftr, not self._is_quick_lv_filter_applied(ftr))
                self._update_quick_badge_data_list()

        self._change_quick_lv_filter(self._gold_lv_filters, True)
        self._change_quick_lv_filter(self._silber_lv_filters, True)
        self._change_quick_lv_filter(self._bronze_lv_filters, True)
        self._sel_quick_cat(QUICK_CAT_ALL)

    def _init_left_list(self):
        self._left_list_node.SetInitCount(self.SLOT_CNT)
        cnt = self._left_list_node.GetItemCount()
        for i in range(cnt):
            item = self._left_list_node.GetItem(i)
            item.temp_medal_wall.nd_display_wall.setVisible(True)

            @item.btn_medal.callback()
            def OnClick(btn, touch, idx=i, ele_node=item):
                if self._in_edit_mode:
                    if self._left_selected_idx != -1:
                        if self._left_selected_idx == idx:
                            self._exit_edit_mode()
                        else:
                            prev_data = self._get_editing_badge_data(self._left_selected_idx)
                            new_data = self._get_editing_badge_data(idx)
                            prev_node = self._get_left_list_ele_node(self._left_selected_idx)
                            if prev_data is None:
                                if idx in self._editing_badge_data_dict:
                                    del self._editing_badge_data_dict[idx]
                            else:
                                self._editing_badge_data_dict[idx] = prev_data
                            if new_data is None:
                                if self._left_selected_idx in self._editing_badge_data_dict:
                                    del self._editing_badge_data_dict[self._left_selected_idx]
                            else:
                                self._editing_badge_data_dict[self._left_selected_idx] = new_data
                            self._request_sync()
                            self._clear_left_selected_idx()
                            self._refresh_left_side_list()
                            if prev_node and new_data:
                                prev_node.PlayAnimation('in')
                            if prev_data:
                                ele_node.PlayAnimation('in')
                    else:
                        r_data = self._get_right_selected_badge_data()
                        if r_data is not None:
                            self._prune_editing_duplicates(r_data)
                            self._editing_badge_data_dict[idx] = r_data
                            self._request_sync()
                            self._clear_left_selected_idx()
                            self._refresh_left_side_list()
                            ele_node.PlayAnimation('in')
                            self._clear_right_selected_idx()
                        else:
                            self._left_selected_idx = idx
                            data = self._get_editing_badge_data(idx)
                            self._play_badge_node_select(ele_node.temp_medal_wall, True, data.sub_branch if data else None)
                else:
                    self._left_selected_idx = idx
                    self._enter_edit_mode()
                    data = self._get_editing_badge_data(idx)
                    self._play_badge_node_select(ele_node.temp_medal_wall, True, data.sub_branch if data else None)
                return

            @item.btn_close.callback()
            def OnClick(btn, touch, idx=i):
                data = self._get_editing_badge_data(idx)
                if data is None:
                    return
                else:
                    self._clear_left_selected_idx()
                    self._drop_editing_badge(idx)
                    return

    def _init_ui_events(self):
        for main_br in self._right_tab_btn_map:
            btn = self._right_tab_btn_map[main_br]

            @btn.btn_battle.callback()
            def OnClick(btn, touch, main_br=main_br):
                self._select_right_filter(main_br)

    def _close_click(self, *args, **kw):
        self.close()

    def _tips_btn_clicked(self, *args, **kw):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(81618, 81619)

    def _btn_clean_clicked(self, *args, **kw):
        self._exit_edit_mode()
        self._editing_badge_data_dict.clear()
        self._refresh_left_side_list()
        self._request_sync()
        if self._in_quick_sel_mode:
            self._quick_sel_map.clear()
            self._quick_sel_rev_map.clear()
            self._update_quick_badge_data_list()

    def _nd_bg_clicked(self, *args, **kw):
        self._exit_edit_mode()

    def _btn_select_mode_clicked(self, *args, **kw):
        self._enter_quick_sel_mode()

    def _btn_select_mode_back_clicked(self, *args, **kw):
        self._exit_quick_sel_mode()

    def _nd_block_right_after_clicked(self, *args, **kw):
        self._exit_quick_sel_mode()

    def _close_quick_clicked(self, *args, **kw):
        self._exit_quick_sel_mode()

    def _btn_tips_quick_clicked(self, *args, **kw):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(910021, 910022)

    def _btn_select_medal_type_clicked(self, *args, **kw):
        self._toggle_quick_category()

    def _on_wall_badge_set(self, c_wall_dict):
        self._editing_badge_data_dict = c_wall_dict
        self._refresh_left_side_list()

    def _refresh_left_side_list(self):
        badge_data_dict = self._editing_badge_data_dict
        cnt = self._left_list_node.GetItemCount()
        for i in range(cnt):
            item = self._left_list_node.GetItem(i)
            if i in badge_data_dict:
                data = badge_data_dict[i]
                sub_branch = data.sub_branch
                lv = data.lv
                max_cur_prog = data.max_cur_prog
                item.nd_medal_name.setVisible(True)
                item.temp_medal_wall.nd_content.setVisible(True)
                item.img_shadow.setVisible(False)
                item.img_shadow.SetDisplayFrameByPath('', self._get_left_side_bg_path(sub_branch))
                badge_item = item.temp_medal_wall
                career_utils.refresh_badge_item(badge_item, sub_branch, lv, check_got=False)
                item.lab_medal.SetString(career_utils.get_badge_name_text(sub_branch))
                item.lab_medal_times.SetString(career_utils.get_badge_b_max_cur_prog_desc_text(sub_branch, max_cur_prog))
            else:
                item.nd_medal_name.setVisible(False)
                item.temp_medal_wall.nd_content.setVisible(False)
                item.img_shadow.setVisible(True)
                item.img_shadow.SetDisplayFrameByPath('', 'gui/ui_res_2/life/display_wall/pnl_medalwall_medalbottom_plus_1.png')

    def _get_left_side_bg_path(self, sub_branch):
        d = {MAIN_BRANCH_BATTLE: 'gui/ui_res_2/life/display_wall/pnl_medalwall_medalbottom_1.png',MAIN_BRANCH_MECHA: 'gui/ui_res_2/life/display_wall/pnl_square_medalwall_medalbottom_1.png'
           }
        return d.get(career_utils.get_main_branch(sub_branch), '')

    def _select_right_filter(self, main_branch):
        if main_branch == self._right_list_filter:
            return
        else:
            if self._right_list_filter is not None:
                self._exit_edit_mode()
            self._right_list_filter = main_branch
            for main_br in self._right_tab_btn_map:
                btn = self._right_tab_btn_map[main_br]
                btn.btn_battle.SetSelect(main_br == main_branch)
                btn.StopAnimation('click')
                btn.StopAnimation('unclick')
                if main_br == main_branch:
                    btn.PlayAnimation('click')
                else:
                    btn.PlayAnimation('unclick')

            self._right_badge_data_list = self._get_owned_badge_data_list(main_branch)
            self._refresh_right_side_list()
            return

    def _is_equipped(self, sub_branch):
        for idx in self._editing_badge_data_dict:
            badge_data = self._editing_badge_data_dict[idx]
            if badge_data.sub_branch == sub_branch:
                return True

        return False

    def _refersh_right_list_equipped(self):
        list_node = self._right_list_node
        cnt = list_node.GetItemCount()
        for i in range(cnt):
            item = list_node.GetItem(i)
            data = item._usr_data
            sub_branch = data.sub_branch
            lv = data.lv
            badge_item = item.temp_icon
            is_equipped = self._is_equipped(sub_branch)
            career_utils.refresh_badge_item(badge_item, sub_branch, lv, check_got=False, darken=is_equipped)
            career_utils.set_badge_item_cut_selected(badge_item, is_equipped)

    def _refresh_right_side_list(self):
        badge_data_list = self._right_badge_data_list
        cnt = len(badge_data_list) if badge_data_list else 0
        list_node = self._right_list_node
        list_node.SetInitCount(cnt)
        for i in range(cnt):
            item = list_node.GetItem(i)
            data = badge_data_list[i]
            sub_branch = data.sub_branch
            lv = data.lv
            max_cur_prog = data.max_cur_prog
            is_equipped = self._is_equipped(sub_branch)
            item._usr_data = data
            badge_item = item.temp_icon
            badge_item.nd_display_wall.setVisible(True)
            career_utils.refresh_badge_item(badge_item, sub_branch, lv, check_got=False, darken=is_equipped)
            item.lab_medal.SetString(career_utils.get_badge_name_text(sub_branch))
            item.lab_medal_times.SetString(career_utils.get_badge_b_max_cur_prog_desc_text(sub_branch, max_cur_prog))
            career_utils.set_badge_item_cut_selected(badge_item, is_equipped)

            @item.btn_click.callback()
            def OnClick(btn, touch, data=data, ele_node=item, idx=i):
                if self._in_edit_mode:
                    if self._right_selected_idx != -1:
                        if self._right_selected_idx == idx:
                            self._exit_edit_mode()
                        else:
                            self._clear_right_selected_idx()
                            self._select_right_ele_by_idx(idx, ele_node, data.sub_branch)
                    elif self._left_selected_idx != -1:
                        left_node = self._get_left_list_ele_node(self._left_selected_idx)
                        self._prune_editing_duplicates(data)
                        self._editing_badge_data_dict[self._left_selected_idx] = data
                        self._request_sync()
                        self._clear_left_selected_idx()
                        self._refresh_left_side_list()
                        if left_node:
                            left_node.PlayAnimation('in')
                        self._clear_right_selected_idx()
                    else:
                        self._select_right_ele_by_idx(idx, ele_node, data.sub_branch)
                else:
                    self._right_selected_idx = idx
                    self._enter_edit_mode()
                    r_data = self._get_right_list_badge_data(idx)
                    self._play_badge_node_select(ele_node.temp_icon, True, r_data.sub_branch if r_data else None)
                return

        self.panel.img_empty_right.setVisible(cnt == 0)

    def _select_right_ele_by_idx(self, idx, ele_node, sub_branch):
        self._right_selected_idx = idx
        self._play_badge_node_select(ele_node.temp_icon, True, sub_branch)

    def _get_owned_badge_data_list(self, main_branch):
        if self._owned_badge_ids is None:
            self._owned_badge_ids = career_utils.get_owned_badge_ids()
        sub_brs = self._owned_badge_ids
        return [ BadgeWallBadgeData(sub_br, career_utils.get_badge_level(sub_br), career_utils.get_badge_ongoing_max_cur_prog(sub_br)) for sub_br in sub_brs if career_utils.get_main_branch(sub_br) == main_branch or main_branch is None ]

    def _enter_edit_mode(self):
        if self._in_edit_mode:
            return
        self._in_edit_mode = True
        cnt = self._left_list_node.GetItemCount()
        for i in range(cnt):
            item = self._left_list_node.GetItem(i)
            item.StopAnimation('edit_out')
            item.PlayAnimation('edit')

        self.panel.StopAnimation('edit_out')
        self.panel.PlayAnimation('edit')

    def _get_editing_badge_data(self, idx):
        return self._editing_badge_data_dict.get(idx, None)

    def _get_right_list_badge_data(self, idx):
        cnt = len(self._right_badge_data_list)
        if idx >= 0 and idx < cnt:
            return self._right_badge_data_list[idx]
        else:
            return None

    def _clear_left_selected_idx(self):
        if self._left_selected_idx != -1:
            ele_node = self._get_left_list_ele_node(self._left_selected_idx)
            data = self._get_editing_badge_data(self._left_selected_idx)
            if ele_node:
                self._play_badge_node_select(ele_node.temp_medal_wall, False, data.sub_branch if data else None)
        self._left_selected_idx = -1
        return

    def _clear_right_selected_idx(self):
        if self._right_selected_idx != -1:
            ele_node = self._get_right_list_ele_node(self._right_selected_idx)
            data = self._get_right_list_badge_data(self._right_selected_idx)
            if ele_node:
                self._play_badge_node_select(ele_node.temp_icon, False, data.sub_branch if data else None)
        self._right_selected_idx = -1
        return

    def _exit_edit_mode(self):
        if not self._in_edit_mode:
            return
        self._in_edit_mode = False
        self._clear_left_selected_idx()
        self._clear_right_selected_idx()
        cnt = self._left_list_node.GetItemCount()
        for i in range(cnt):
            item = self._left_list_node.GetItem(i)
            item.StopAnimation('edit')
            item.PlayAnimation('edit_out')

        self.panel.StopAnimation('edit')
        self.panel.PlayAnimation('edit_out')

    def _get_left_list_ele_node(self, idx):
        cnt = self._left_list_node.GetItemCount()
        if idx >= 0 and idx < cnt:
            return self._left_list_node.GetItem(idx)
        else:
            return None

    def _get_right_list_ele_node(self, idx):
        cnt = self._right_list_node.GetItemCount()
        if idx >= 0 and idx < cnt:
            return self._right_list_node.GetItem(idx)
        else:
            return None

    def _play_badge_node_select(self, inner_badge_node, sel, sub_branch):
        if sub_branch == None:
            main_br = MAIN_BRANCH_BATTLE
        else:
            main_br = career_utils.get_main_branch(sub_branch)
        d = {MAIN_BRANCH_BATTLE: ('select_battle', 'unselect_battle'),MAIN_BRANCH_MECHA: ('select_mecha', 'unselect_mecha')
           }
        for m_br in d:
            anims = d[m_br]
            if main_br == m_br:
                if sel:
                    inner_badge_node.StopAnimation(anims[1])
                    inner_badge_node.PlayAnimation(anims[0])
                else:
                    inner_badge_node.StopAnimation(anims[0])
                    inner_badge_node.PlayAnimation(anims[1])
            else:
                inner_badge_node.StopAnimation(anims[0])
                inner_badge_node.PlayAnimation(anims[1])
                inner_badge_node.StopAnimation(anims[1], finish_ani=True)

        return

    def _enter_quick_sel_mode(self):
        if self._in_quick_sel_mode:
            return
        self._in_quick_sel_mode = True
        self._quick_sel_map = dict(self._editing_badge_data_dict)
        self._quick_sel_rev_map = {badge_data.sub_branch:wall_idx for wall_idx, badge_data in six.iteritems(self._quick_sel_map)}
        self._exit_edit_mode()
        self._update_quick_badge_data_list()
        self.panel.StopAnimation('before_in')
        self.panel.StopAnimation('after_out')
        self.panel.PlayAnimation('after_in')
        self.panel.PlayAnimation('before_out')

    def _exit_quick_sel_mode(self):
        if not self._in_quick_sel_mode:
            return
        self._in_quick_sel_mode = False
        self._quick_sel_map.clear()
        self._quick_sel_rev_map.clear()
        self.panel.StopAnimation('after_in')
        self.panel.StopAnimation('before_out')
        self.panel.PlayAnimation('before_in')
        self.panel.PlayAnimation('after_out')

    def _toggle_quick_category(self):
        self.set_quick_cat_vis(not self.get_quick_cat_vis())

    def set_quick_cat_vis(self, show):
        self.panel.btn_select_medal_type.img_bg.setVisible(show)
        self.panel.btn_select_medal_type.img_arrow.setScaleY(-1 if show else 1)

    def get_quick_cat_vis(self):
        return self.panel.btn_select_medal_type.img_bg.isVisible()

    def _sel_quick_cat(self, quick_cat):
        if quick_cat is None:
            return
        else:
            if self._cur_quick_cat == quick_cat:
                self.set_quick_cat_vis(False)
                return
            self._cur_quick_cat = quick_cat
            ui_conf = QUICK_TAG_UI_CONF.get(quick_cat, None)
            if ui_conf is not None:
                self.panel.btn_select_medal_type.SetText(ui_conf[1])
                self.panel.btn_select_medal_type.img_icon.SetDisplayFrameByPath('', ui_conf[0])
            self.set_quick_cat_vis(False)
            self._update_quick_badge_data_list()
            return

    def _update_quick_badge_data_list(self):
        quick_cat = self._cur_quick_cat
        main_br = self._get_main_br_by_quick_cat(quick_cat)
        lst = self._get_owned_badge_data_list(main_br)
        lst = self._apply_lv_filters(lst)
        self._quick_badge_data_list = lst
        sub_brs_of_type = career_utils.get_badge_ids_by_type(main_br)
        self.panel.lab_unlock_num.SetString('%s/%s' % (len(lst), len(sub_brs_of_type)))
        self._refresh_quick_list(lst)

    def _apply_lv_filters(self, badge_data_list):

        def actual_filter(badge_data):
            for ftr in self._quick_lv_filters:
                if ftr(badge_data):
                    return True

            return False

        return list(filter(actual_filter, badge_data_list))

    def _init_badge_cnt_by_lv(self):
        self.panel.btn_gold.SetText(str(len(career_utils.get_owned_badge_ids_by_lv(BADGE_GOLD_LV))))
        self.panel.btn_silver.SetText(str(len(career_utils.get_owned_badge_ids_by_lv(BADGE_SILVER_LV))))
        self.panel.btn_copper.SetText(str(len(career_utils.get_owned_badge_ids_by_lv(BADGE_BRONZE_LV))))

    def _refresh_quick_ele_sel(self, ele_node, main_br, sel, wall_idx):
        d = {MAIN_BRANCH_BATTLE: 'img_select_battle',
           MAIN_BRANCH_MECHA: 'img_select_mecha'
           }
        for _main_br in d:
            if _main_br != main_br:
                _sel = False
            else:
                _sel = sel
            sel_node_name = d[_main_br]
            if hasattr(ele_node, sel_node_name):
                sel_node = getattr(ele_node, sel_node_name) if 1 else None
                if sel_node is None:
                    pass
                continue
            sel_node.setVisible(_sel)
            if _sel:
                if sel_node.lab_num:
                    sel_node.lab_num.SetString(str(wall_idx + 1))

        return

    def _get_next_wall_sel_idx(self):
        for i in range(self.QUICK_SEL_MAX_CNT):
            if i not in self._quick_sel_map:
                return i

        return -1

    def _refresh_quick_list(self, badge_data_list):
        cnt = len(badge_data_list) if badge_data_list else 0
        list_node = self._quick_list_node
        list_node.SetInitCount(cnt)
        for i in range(cnt):
            item = list_node.GetItem(i)
            data = badge_data_list[i]
            sub_branch = data.sub_branch
            lv = data.lv
            max_cur_prog = data.max_cur_prog
            badge_item = item.temp_icon
            career_utils.refresh_badge_item(badge_item, sub_branch, lv, check_got=False)
            item.lab_medal.SetString(career_utils.get_badge_name_text(sub_branch))
            item.lab_medal_times.SetString(career_utils.get_badge_b_max_cur_prog_desc_text(sub_branch, max_cur_prog))
            wall_idx = self._quick_sel_rev_map.get(sub_branch, -1)
            main_br = career_utils.get_main_branch(sub_branch)
            self._refresh_quick_ele_sel(item, main_br, wall_idx != -1, wall_idx)

            @item.btn_click.callback()
            def OnClick(btn, touch, item=item, data=data, main_br=main_br):
                if self._badge_tips_wgt.isVisible():
                    return
                sub_branch = data.sub_branch
                lv = data.lv
                max_cur_prog = data.max_cur_prog
                wall_idx = self._quick_sel_rev_map.get(sub_branch, -1)
                if wall_idx != -1:
                    if wall_idx in self._editing_badge_data_dict:
                        del self._editing_badge_data_dict[wall_idx]
                        self._request_sync()
                        self._refresh_left_side_list()
                    if wall_idx in self._quick_sel_map:
                        del self._quick_sel_map[wall_idx]
                    if sub_branch in self._quick_sel_rev_map:
                        del self._quick_sel_rev_map[sub_branch]
                    self._refresh_quick_ele_sel(item, main_br, False, -1)
                else:
                    next_idx = self._get_next_wall_sel_idx()
                    if next_idx != -1:
                        self._editing_badge_data_dict[next_idx] = data
                        self._request_sync()
                        self._refresh_left_side_list()
                        self._quick_sel_map[next_idx] = data
                        self._quick_sel_rev_map[sub_branch] = next_idx
                        self._refresh_quick_ele_sel(item, main_br, True, next_idx)
                    else:
                        global_data.game_mgr.show_tip(910023)

            item.btn_click.SetPressEnable(True)

            @item.btn_click.callback()
            def OnPressed(btn, data=data):
                wpos = btn.getParent().convertToWorldSpace(btn.getPosition())
                self._badge_tips_wgt.show_badge_tips(wpos, data)

        self.panel.img_empty_quick.setVisible(cnt == 0)

    def _get_main_br_by_quick_cat(self, quick_tag):
        d = {QUICK_CAT_ALL: None,
           QUICK_CAT_BATTLE: MAIN_BRANCH_BATTLE,
           QUICK_CAT_MECHA: MAIN_BRANCH_MECHA
           }
        return d.get(quick_tag, None)

    @staticmethod
    def _gen_is_lv_filter(lv):

        def lv_filter(badge_data):
            return lv == badge_data.lv

        return lv_filter

    def _change_quick_lv_filter(self, ftr, add):
        if add:
            self._quick_lv_filters.add(ftr)
        elif ftr in self._quick_lv_filters:
            self._quick_lv_filters.remove(ftr)
        node = self.filter_ui_map.get(ftr, None)
        if node is not None:
            node.SetSelect(add)
        return

    def _is_quick_lv_filter_applied(self, ftr):
        return ftr in self._quick_lv_filters

    def _prune_editing_duplicates(self, data):
        if data is None:
            return
        else:
            for key in six_ex.keys(self._editing_badge_data_dict):
                _d = self._editing_badge_data_dict[key]
                if _d.sub_branch == data.sub_branch:
                    del self._editing_badge_data_dict[key]

            return

    def _request_sync(self):
        self._refersh_right_list_equipped()
        if not global_data.player:
            return
        global_data.player.request_set_career_badge_wall(self._editing_badge_data_dict)