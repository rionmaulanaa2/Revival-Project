# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PlayIntroduceUI.py
from __future__ import absolute_import
import six
import six_ex
import copy
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils import battle_utils
from common.const.uiconst import NORMAL_LAYER_ZORDER, NORMAL_LAYER_ZORDER_1
import math
import ccui
import cc
from common.cfg import confmgr
from common.utils.timer import CLOCK
from common.utils.cocos_utils import ccp
from logic.gcommon.common_const import battle_const
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
LEFT = 0
RIGHT = 1
REFRESH_INTERVAL = 3.0

class PlayIntroduceUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'introduce/introduce_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'temp_bg'
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *play_tips_id):
        super(PlayIntroduceUI, self).on_init_panel()
        self.init_parameters(play_tips_id)
        self.init_widgets()
        self.init_ui_event()
        self.hide_main_ui()
        if not G_IS_NA_PROJECT:
            for item in self.panel.list_banner.GetAllItem():
                if item.lab_time:
                    item.lab_time.setVisible(False)

    def init_parameters(self, play_tips_id):
        self.play_tips_id = list(copy.deepcopy(play_tips_id))
        tips_id = battle_const.PLAY_TYPE_CHIKEN_SIGNAL_PLAY_TIPS_ID
        if tips_id in self.play_tips_id and not battle_utils.is_signal_logic():
            self.play_tips_id.remove(tips_id)
        self._last_offset = 0
        self._scroll_direction = RIGHT
        self._cur_idx = 0
        self.sub_panel = self.panel.list_banner
        self.nd_list_top_tab = self.panel.nd_list_top_tab
        self.cur_tab_index = None
        self.introduce_data_conf = [ confmgr.get('battle_introduce', str(tip_id), default={}) for tip_id in self.play_tips_id
                                   ]
        return

    def init_widgets(self):
        if len(self.introduce_data_conf) == 1:
            self.nd_list_top_tab.setVisible(False)
        else:
            self.nd_list_top_tab.setVisible(True)
        tab_list = self.nd_list_top_tab.list_top_tab
        tab_list.DeleteAllSubItem()
        tab_list.SetInitCount(len(self.introduce_data_conf))
        select_index = 0
        for index, introduce_data in enumerate(self.introduce_data_conf):
            tab_item = tab_list.GetItem(index)
            tab_text_id = introduce_data.get('tab_id', '')
            tab_item.nd_multilang_btn.btn_tab.SetText(tab_text_id)
            tab_item.btn_tab.BindMethod('OnClick', lambda b, t, index=index: self.select_tab(index))
            if introduce_data.get('is_default'):
                select_index = index

        _, height = tab_list.GetContentSize()
        width, _ = self.panel.list_banner.GetContentSize()
        tab_list.SetContentSize(width, height)
        self.select_tab(select_index)
        self._timer = global_data.game_mgr.register_logic_timer(self.tick, interval=REFRESH_INTERVAL, times=-1, mode=CLOCK)

    def set_panel_custom_by_other_panel(self):
        self.panel.temp_bg.SetSwallowTouch(False)
        self.panel.temp_bg.btn_close.setVisible(False)
        for item in self.panel.list_banner.GetAllItem():
            if item.lab_time:
                item.lab_time.setVisible(False)

    def select_tab(self, index):
        tab_list = self.nd_list_top_tab.list_top_tab
        num = tab_list.GetItemCount()
        if index >= num:
            index = 0
        if self.cur_tab_index == index:
            return
        else:
            container = self.sub_panel.GetInnerContainer()
            if container:
                container.stopAllActions()
            if self.cur_tab_index is not None:
                tab = tab_list.GetItem(self.cur_tab_index)
                tab.PlayAnimation('unclick')
                tab.btn_tab.SetSelect(False)
            tab = tab_list.GetItem(index)
            tab.btn_tab.SetSelect(True)
            tab.PlayAnimation('click')
            self.cur_tab_index = index
            self.init_banner()
            self.check_show_weapon_list()
            return

    def get_introduce_list(self):
        return self.introduce_data_conf[self.cur_tab_index]['introduce_list']

    def get_play_type(self):
        return self.introduce_data_conf[self.cur_tab_index]['play_type']

    def init_banner(self):
        introduce_list = self.get_introduce_list()
        self.panel.list_num.SetInitCount(len(introduce_list))
        self.panel.list_num.setVisible(len(introduce_list) > 1)
        self.panel.list_banner.DeleteAllSubItem()
        for i, introduce_data in enumerate(introduce_list):
            json_path = introduce_data['json']
            template_ui = global_data.uisystem.load_template_create(json_path)
            self.panel.list_banner.AddControl(template_ui, None, True)
            play_type_id = self.get_play_type()
            if play_type_id == 1001 or play_type_id == 1002:
                template_ui.nd_introduce.lab_introduce.SetString(introduce_data['desc_id'])
            time_text_id = introduce_data.get('time_text_id', 0)
            if template_ui.lab_time:
                has_text_id = time_text_id > 0
                template_ui.lab_time.setVisible(has_text_id)
                template_ui.lab_time.SetString(time_text_id)
            if template_ui.nd_locate:
                self.reset_panel_size_and_position(template_ui)
            if template_ui.lab_introduce:
                size = template_ui.lab_introduce.getTextContentSize()
                min_size = (0, 0)
                width = max(size.width, min_size[0])
                height = max(size.height, min_size[1])
                template_ui.lab_introduce.ChildResizeAndPositionWithSize(width, height)

        num = self.sub_panel.GetItemCount()
        self.sub_panel.setTouchEnabled(num > 1)
        self.update_cur_idx(0)
        return

    def reset_panel_size_and_position(self, node):
        if node.lab_1.__class__.__name__ == 'CCRichText':
            node.lab_1.formatText()
        if node.lab_1.getTextContentSize:
            t_w = node.lab_1.getTextContentSize().width
        else:
            t_w, _ = node.lab_1.GetContentSize()
        _, h = node.nd_locate.GetContentSize()
        node.nd_locate.SetContentSize(t_w, h)
        node.nd_locate.ResizeAndPosition(include_self=False)

    def init_ui_event(self):
        num = self.sub_panel.GetItemCount()
        self.sub_panel.setTouchEnabled(num > 1)
        self.sub_panel.BindMethod('OnScrolling', self._on_scrolling)
        self.sub_panel.addTouchEventListener(self._on_normal_touch)
        self.sub_panel.setInertiaScrollEnabled(False)
        self.panel.btn_left.BindMethod('OnClick', self._on_click_btn_left)
        self.panel.btn_right.BindMethod('OnClick', self._on_click_btn_right)
        self.panel.temp_weapon_bg.btn_close.BindMethod('OnClick', self.on_click_wepaon_bg_close)
        self.panel.btn_weapon.BindMethod('OnClick', self.on_click_btn_weapon)

    def _on_normal_touch(self, widget, event):
        num = self.sub_panel.GetItemCount()
        if num <= 1:
            return
        if event in (ccui.WIDGET_TOUCHEVENTTYPE_ENDED, ccui.WIDGET_TOUCHEVENTTYPE_CANCELED):
            idx_item = self.update_now_idx()
            self.update_cur_idx(idx_item)
            self.sub_panel.LocatePosByItem(idx_item)
            if not self._timer:
                self._timer = global_data.game_mgr.register_logic_timer(self.tick, interval=REFRESH_INTERVAL, times=-1, mode=CLOCK)

    def _on_scrolling(self, *args):
        num = self.sub_panel.GetItemCount()
        if num <= 1:
            return
        else:
            if self._timer:
                global_data.game_mgr.unregister_logic_timer(self._timer)
                self._timer = None
            off_set_now = self.sub_panel.GetContentOffset()
            self._scroll_direction = RIGHT if off_set_now.x - self._last_offset <= 0 else LEFT
            self._last_offset = off_set_now.x
            now_idx = self.update_now_idx()
            if now_idx != self._cur_idx:
                self.panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
                self.panel.list_num.GetItem(now_idx).btn_icon_choose.SetSelect(True)
                self.update_cur_idx(now_idx)
            return

    def _on_click_btn_left(self, *args):
        if self._cur_idx - 1 >= 0:
            self._on_click_choose_banner(self._cur_idx - 1)

    def _on_click_btn_right(self, *args):
        introduce_list = self.get_introduce_list()
        if self._cur_idx + 1 < len(introduce_list):
            self._on_click_choose_banner(self._cur_idx + 1)

    def _on_click_choose_banner(self, index):
        self.sub_panel.LocatePosByItem(index)
        self.panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
        self.panel.list_num.GetItem(index).btn_icon_choose.SetSelect(True)
        self.update_cur_idx(index)
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def update_now_idx(self):
        ctrl_size = self.sub_panel.GetCtrlSize()
        off_set_now = self.sub_panel.GetContentOffset()
        off_num = abs(off_set_now.x / ctrl_size.width)
        if self._scroll_direction == RIGHT:
            idx_item = int(math.ceil(off_num))
        else:
            idx_item = int(math.floor(off_num))
        introduce_list = self.get_introduce_list()
        leng = len(introduce_list)
        idx_max = leng - 1 if leng > 0 else 0
        idx_item = max(min(idx_item, idx_max), 0)
        return idx_item

    def tick(self):
        num = self.sub_panel.GetItemCount()
        if num <= 1:
            return
        next_idx = 0 if self._cur_idx + 1 >= num else self._cur_idx + 1
        container = self.sub_panel.GetInnerContainer()
        container.stopAllActions()

        def scroll_end():
            self.sub_panel.LocatePosByItem(next_idx)
            self.panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
            self.panel.list_num.GetItem(next_idx).btn_icon_choose.SetSelect(True)
            self.update_cur_idx(next_idx)

        ctrl_size = self.sub_panel.GetCtrlSize()
        container.runAction(cc.Sequence.create([
         cc.MoveTo.create(0.3, ccp(ctrl_size.width * next_idx * -1, container.getPosition().y)),
         cc.CallFunc.create(scroll_end)]))

    def on_finalize_panel(self):
        self.show_main_ui()
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def update_cur_idx(self, index):
        introduce_list = self.get_introduce_list()
        if self._cur_idx != index and self._cur_idx < self.panel.list_num.GetItemCount():
            self.panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
        self._cur_idx = index
        self.panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(True)
        self.panel.btn_left.setVisible(True if self._cur_idx - 1 >= 0 else False)
        self.panel.btn_right.setVisible(True if self._cur_idx + 1 < len(introduce_list) else False)

    def on_click_wepaon_bg_close(self, btn, touch):
        self.panel.nd_weapon_show.setVisible(False)

    def on_click_btn_weapon(self, btn, touch):
        self.panel.nd_weapon_show.setVisible(not self.panel.nd_weapon_show.isVisible())
        if self.panel.nd_weapon_show.isVisible():
            self.refresh_weapon_list()

    def refresh_weapon_list(self):
        cur_intro_data = self.introduce_data_conf[self.cur_tab_index]
        weapon_map_id = cur_intro_data.get('weapon_map_id')
        if weapon_map_id:
            all_weapon_kind_dict = self.get_all_weapon_kind_dict()
            avail_weapons = self.get_available_weapon_list(weapon_map_id)
            self.panel.list_weapon.SetInitCount(len(all_weapon_kind_dict))
            all_item = self.panel.list_weapon.GetAllItem()
            kinds = sorted(six_ex.keys(all_weapon_kind_dict), key=lambda x: (x not in avail_weapons, x))
            for idx, ui_item in enumerate(all_item):
                lobby_item_no = all_weapon_kind_dict[kinds[idx]]
                self.init_weapon_item(ui_item, kinds[idx], lobby_item_no, kinds[idx] in avail_weapons)

    def init_weapon_item(self, ui_item, icon_no, lobby_item_no, usable):
        ui_item.img_weapon_on.setVisible(usable)
        ui_item.img_weapon_off.setVisible(not usable)
        from logic.gutils.item_utils import get_lobby_item_name, get_item_pic_by_icon_no
        ui_item.lab_weapon.SetString(get_lobby_item_name(lobby_item_no))
        if usable:
            ui_item.img_weapon_on.SetDisplayFrameByPath('', get_item_pic_by_icon_no(icon_no))
            ui_item.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/introduce/weapon_pool/pnl_highl.png')
        else:
            OUTLINE_PIC_PATH = 'gui/ui_res_2/catalogue/outline/208%s.png'
            icon_path = OUTLINE_PIC_PATH % str(lobby_item_no)[3:]
            ui_item.img_weapon_off.SetDisplayFrameByPath('', icon_path)
            ui_item.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/introduce/weapon_pool/pnl_grey.png')

    def check_show_weapon_list(self):
        cur_play_tips_id = self.play_tips_id[self.cur_tab_index]
        cur_intro_data = self.introduce_data_conf[self.cur_tab_index]
        weapon_map_id = cur_intro_data.get('weapon_map_id')
        if weapon_map_id:
            self.panel.btn_weapon.setVisible(True)
        else:
            self.panel.btn_weapon.setVisible(False)
        if weapon_map_id and self.panel.nd_weapon_show.isVisible():
            self.refresh_weapon_list()

    def get_available_weapon_list(self, map_id):
        from logic.client.const import game_mode_const
        map_data_conf = confmgr.get('map_config', str(map_id), default={})
        map_path = map_data_conf['cCModeCfgName'] if 'cCModeCfgName' in map_data_conf else map_data_conf.get('cCMode', game_mode_const.GAME_MODE_NORMAL)
        sub_name = map_data_conf.get('cName', game_mode_const.GAME_MODE_NORMAL)
        output_dict = confmgr.get('game_mode/%s/%s/item_rate' % (map_path, sub_name), default={})
        battle_weapon_icon_list = []
        for k in six_ex.keys(output_dict):
            icon_no = int(confmgr.get('item', str(k), default={}).get('iShader', str(k)))
            if icon_no not in battle_weapon_icon_list:
                battle_weapon_icon_list.append(icon_no)

        return sorted(battle_weapon_icon_list)

    def get_all_weapon_kind_dict(self):
        DEFAULT_WEAPON = '1051011'
        from logic.gutils import items_book_utils
        from logic.client.const import items_book_const
        weapon_config = items_book_utils.get_items_conf(items_book_const.WEAPON_ID)
        battle_weapon_dict = {}
        for lobby_item_no, info_dict in six.iteritems(weapon_config):
            if lobby_item_no == DEFAULT_WEAPON:
                continue
            battle_item_nos = info_dict.get('battle_item_no', [])
            if battle_item_nos:
                item_id = battle_item_nos[0]
                icon_no = confmgr.get('item', str(item_id), default={}).get('iShader', str(item_id))
                if icon_no not in battle_weapon_dict:
                    battle_weapon_dict[icon_no] = lobby_item_no

        return battle_weapon_dict