# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerBattleFlagWidget.py
from __future__ import absolute_import
import six
from logic.gutils import battle_flag_utils
from logic.gutils import career_utils
from logic.gutils import item_utils
from logic.gutils import locate_utils
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME
from logic.gutils.template_utils import set_ui_show_picture
from logic.comsys.role.BattleFlagChooseWidget import BattleFlagChooseWidget
from logic.comsys.role.BattleFlagBgChooseWidget import BattleFlagBgChooseWidget
from logic.gutils import role_head_utils
from common.uisys.BaseUIWidget import BaseUIWidget
TAB_UI_BATTLE_FLAG = 2
TAB_TITLE = 3

class PlayerBattleFlagWidget(BaseUIWidget):
    PANEL_CONFIG_NAME = 'battle_flag/i_flag_main'

    def __init__(self, parent_cls, parent_panel):
        panel = global_data.uisystem.load_template_create(self.PANEL_CONFIG_NAME, parent_panel)
        super(PlayerBattleFlagWidget, self).__init__(parent_cls, panel)
        self._share_content = None
        self._tab_info = [{'cls': BattleFlagBgChooseWidget,'tab_name': 860067,'tips': 860130,'tab_id': TAB_UI_BATTLE_FLAG}]
        if locate_utils.is_open_location():
            from logic.comsys.role.BattleFlagLocationWidget import BattleFlagLocationWidget
            self._tab_info.append({'cls': BattleFlagLocationWidget,'tab_name': 10372,'tips': 10373,'tab_id': TAB_TITLE})
        from logic.comsys.share.ShareTipsWidget import ShareTipsWidget
        self.panel.nd_share.setVisible(global_data.is_share_show)
        self._share_tips_widget = ShareTipsWidget(self, self.panel, self.panel.btn_share, pos=('50%',
                                                                                               '100%'))
        self._cur_tab_id = 0
        self._jump_to_item_no = None
        self._cur_tab_widget = None
        self._cur_tab_btn = None
        self.last_battle_frame = None
        self.init_panel()
        return

    def init_event(self):
        super(PlayerBattleFlagWidget, self).init_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'set_battle_flag_frame_event': self.refresh_flag_frame,
           'message_on_set_rank_title': self.refresh_rank_title,
           'message_on_player_role_head_photo': self.on_change_role_head_photo,
           'message_on_player_role_head': self.on_change_role_head_frame
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_effect_gaosi(self):
        pass

    def close_effect_gaosi--- This code section failed: ---

  74       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_effect_gaosi'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

  75      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

  76      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             1  '_effect_gaosi'
          22  JUMP_IF_FALSE_OR_POP    37  'to 37'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             1  '_effect_gaosi'
          31  LOAD_ATTR             2  'destroy'
          34  CALL_FUNCTION_0       0 
        37_0  COME_FROM                '22'
          37  POP_TOP          

  77      38  LOAD_CONST            0  ''
          41  LOAD_FAST             0  'self'
          44  STORE_ATTR            1  '_effect_gaosi'
          47  LOAD_CONST            0  ''
          50  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def init_panel(self):
        self.panel.RecordAnimationNodeState('loop')
        self.panel.RecordAnimationNodeState('show_change')

        @self.panel.btn_set.btn_common_big.callback()
        def OnClick(btn, touch):
            self.panel.PlayAnimation('show_change')
            global_data.emgr.on_notify_guide_event.emit('battle_flag_guide_finish')

        @self.panel.nd_change.nd_touch.callback()
        def OnClick(btn, touch):
            self.panel.PlayAnimation('disappear_change')
            self.refresh_flag_frame()

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.BattleFlagShareCreator import BattleFlagShareCreator
            role_visible = self.panel.temp_flag.nd_role_locate.isVisible()
            share_creator = BattleFlagShareCreator()
            share_creator.create(is_role=role_visible)
            self._share_content = share_creator
            from logic.comsys.share.ShareUI import ShareUI
            ShareUI(parent=self.panel).set_share_content_raw(self._share_content.get_render_texture(), 'pnl_share_crew', share_content=self._share_content)

        self.refresh_rank_title()
        self.refresh_flag_frame(False)
        self.hide_medals_explain()
        self.refresh_shadow()
        self.show_effect_gaosi()
        tab_nd = self.panel.nd_change.temp_tab
        tab_lst = tab_nd.list_right
        tab_lst.SetInitCount(len(self._tab_info))

        @tab_lst.unique_callback()
        def OnCreateItem(lv, index, item_widget):
            self.cb_create_item(index, item_widget)

        all_items = tab_lst.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.cb_create_item(index, widget)

    def refresh_rank_title(self):
        battle_flag_utils.init_battle_flag_template_new(battle_flag_utils.get_battle_info_by_player(global_data.player), self.panel.temp_flag)
        battle_flag_utils.init_battle_flag_template_new(battle_flag_utils.get_battle_info_by_player(global_data.player), self.panel.temp_flag_small, enable_click=False)

    def refresh_flag_frame(self, need_refresh_frame=True, battle_frame=None):
        if battle_frame or global_data.player:
            battle_frame = global_data.player.get_battle_flag_frame() if 1 else DEFAULT_FLAG_FRAME()
        self.panel.lab_frame_name.SetString(item_utils.get_lobby_item_name(battle_frame))
        battle_flag_utils.refresh_battle_frame(battle_frame, self.panel.img_frame)
        battle_flag_utils.refresh_battle_front_frame(battle_frame, self.panel.img_front_frame)
        if str(battle_frame) != str(self.last_battle_frame):
            if need_refresh_frame:
                self.panel.PlayAnimation('change')
                self.panel.temp_flag.PlayAnimation('change')
            self.last_battle_frame = battle_frame
        need_refresh_frame and battle_flag_utils.refresh_battle_frame(battle_frame, self.panel.temp_flag.img_bar)
        need_refresh_frame and battle_flag_utils.refresh_battle_front_frame(battle_frame, self.panel.temp_flag.img_front)
        need_refresh_frame and self.show_effect_gaosi()
        need_refresh_frame and self.refresh_shadow(battle_frame)

    def refresh_medals(self, need_refresh_medal=True):
        flag_num = battle_flag_utils.MAX_MEDAL_NUM
        task_ids = global_data.player.get_battle_flag_medal() if global_data.player else []
        self.panel.nd_medal_explain.setVisible(bool(task_ids))
        self.panel.list_explain.SetInitCount(min(len(task_ids), flag_num))
        all_items = self.panel.list_explain.GetAllItem()
        for index, item_widget in enumerate(all_items):
            show = index < len(task_ids)
            item_widget.setVisible(show)
            if show:
                medal_task_id = str(task_ids[index])
                level = career_utils.get_badge_level(medal_task_id)
                cp_reward_idx = career_utils.get_badge_got_cp_reward_idx(medal_task_id)
                career_utils.refresh_badge_item(item_widget.temp_life_icon, medal_task_id, level, cp_reward_idx=cp_reward_idx, check_got=False, ban_anim=True)
                item_widget.lab_life_icon_name.SetString(career_utils.get_badge_name_text(medal_task_id))
                item_widget.lab_title.SetString(get_text_by_id(860113).format(num=index + 1))

        need_refresh_medal and battle_flag_utils.refresh_medals(task_ids, self.panel.temp_flag)
        need_refresh_medal and self.show_effect_gaosi()
        need_refresh_medal and self.refresh_shadow()

    def hide_medals_explain(self):
        self.panel.nd_medal_explain.setVisible(False)
        self.panel.list_explain.setVisible(False)

    def refresh_shadow(self, battle_frame=None):
        battle_flag_info = battle_flag_utils.get_battle_info_by_player(global_data.player)
        clothing_id = battle_flag_info.get('skin')
        if not battle_frame:
            battle_frame = battle_flag_info.get('frame', DEFAULT_FLAG_FRAME())
        medal = battle_flag_info.get('medal', [])
        set_ui_show_picture(clothing_id, self.panel.img_role, self.panel.img_mech)
        battle_flag_utils.refresh_battle_frame(battle_frame, self.panel.img_bar)
        battle_flag_utils.refresh_battle_front_frame(battle_frame, self.panel.img_front)
        for item in self.panel.list_achi.GetAllItem():
            item.setOpacity(100)

    def cb_create_item(self, index, tab_item):
        tab_info = self._tab_info[index]
        tab_item.btn.SetText(tab_info['tab_name'])

        @tab_item.btn.callback()
        def OnClick(btn, touch, index=index):
            self._cur_tab_id = index
            tab_info = self._tab_info[index]
            if self._cur_tab_widget:
                self._cur_tab_widget.destroy()
            temp_nd = self.panel.nd_change
            self._cur_tab_widget = tab_info['cls'](temp_nd)
            temp_nd.nd_tips.SetString(get_text_by_id(tab_info.get('tips')))
            if self._cur_tab_btn:
                self._cur_tab_btn.SetSelect(False)
            self._cur_tab_btn = btn
            self._cur_tab_btn.SetSelect(True)

        if index == self._cur_tab_id:
            tab_item.btn.OnClick(tab_item.btn)
            if self._cur_tab_widget and self._jump_to_item_no is not None:
                if hasattr(self._cur_tab_widget, 'set_item_selected'):
                    self._cur_tab_widget.set_item_selected(self._jump_to_item_no)
                    self._jump_to_item_no = None
        return

    def on_appear(self):
        if self.panel:
            self.panel.StopAnimation('loop')
            self.panel.RecoverAnimationNodeState('loop')
            self.panel.PlayAnimation('in')
            self.panel.temp_flag.PlayAnimation('in')
            delay = self.panel.GetAnimationMaxRunTime('in')
            self.panel.SetTimeOut(delay, lambda : self.panel.PlayAnimation('loop'))

    def on_disappear(self):
        pass

    def on_select(self, *args):
        pass

    def on_reset_states(self):
        pass

    def on_player_stat_inf(self, stat_inf):
        pass

    def on_refresh_player_detail_inf(self, player_inf):
        pass

    def destroy(self):
        self.destroy_widget('_share_content')
        self.destroy_widget('_share_tips_widget')
        self.process_event(False)
        if self._cur_tab_widget:
            self._cur_tab_widget.destroy()
        self._cur_tab_widget = None
        super(PlayerBattleFlagWidget, self).destroy()
        return

    def _get_item_by_tab(self, tab):
        item_idx = -1
        for idx, info in enumerate(self._tab_info):
            tab_id = info.get('tab_id', None)
            if tab is None:
                continue
            if tab == tab_id:
                item_idx = idx
                break

        return item_idx

    def jump_to_tab(self, tab, item_no=None):
        self.panel.btn_set.btn_common_big.OnClick(None)
        idx = self._get_item_by_tab(tab)
        if idx == -1:
            return
        else:
            if idx != self._cur_tab_id:
                tab_nd = self.panel.nd_change.temp_tab
                tab_lst = tab_nd.list_right
                if not tab_lst.GetItem(idx):
                    self._cur_tab_id = idx
                    self._jump_to_item_no = item_no
                else:
                    tab_item = tab_lst.GetItem(idx)
                    tab_item.btn.OnClick(tab_item.btn)
                    if self._cur_tab_widget and self._jump_to_item_no is not None:
                        if hasattr(self._cur_tab_widget, 'set_item_selected'):
                            self._cur_tab_widget.set_item_selected(self._jump_to_item_no)
            elif self._cur_tab_widget and item_no is not None:
                if hasattr(self._cur_tab_widget, 'set_item_selected'):
                    self._cur_tab_widget.set_item_selected(item_no)
            else:
                self._cur_tab_id = idx
                self._jump_to_item_no = item_no
            return

    @staticmethod
    def should_have_tab(tab):
        if tab == TAB_TITLE:
            return locate_utils.is_open_location()
        return True

    @staticmethod
    def can_jump_to_tab(tab):
        return PlayerBattleFlagWidget.should_have_tab(tab)

    def on_change_role_head_photo(self, update_list):
        if global_data.player and global_data.player.uid in update_list:
            role_head_utils.set_role_head_photo(self.panel.temp_flag.temp_head, update_list[global_data.player.uid])

    def on_change_role_head_frame(self, update_list):
        if global_data.player and global_data.player.uid in update_list:
            role_head_utils.set_role_head_frame(self.panel.temp_flag.temp_head, update_list[global_data.player.uid])