# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/SummerGameRewardUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import UI_TYPE_CONFIRM, NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
from cc import Vec2
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_type, get_lobby_item_name, get_lobby_item_belong_name
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.template_utils import init_tempate_mall_i_item
from common.cfg import confmgr

class SummerGameRewardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/activity_202107/small_game/i_activity_summer_reward_preview'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_TYPE = UI_TYPE_CONFIRM
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, reward_id=0, *args, **kwargs):
        super(SummerGameRewardUI, self).on_init_panel(*args, **kwargs)
        self.init_reward_items(reward_id)
        self.init_scroll_list()

    def on_scroll_btn_clicked(self, to_right):
        pass

    def check_sview(self):
        container_pos_x = -self.scroll_list.getInnerContainer().getPositionX()
        if self.container_max_move == 0:
            return
        ratio = container_pos_x / self.container_max_move
        ratio = min(1.0, max(0.0, ratio))
        slider_pos = self._slider_max_pos * ratio
        self.panel.img_progress.SetPosition(str(slider_pos), '50%0')

    def show_panel(self):
        self.panel.setVisible(True)

    def hide_panel(self):
        self.panel.setVisible(False)

    def init_reward_items(self, reward_id):
        list_reward = self.panel.list_reward
        list_reward.DeleteAllSubItem()
        _reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        for item_no, num in _reward_list:
            nd_item = list_reward.AddTemplateItem()
            nd_item.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))
            item_type = get_lobby_item_type(item_no)
            if item_type in {L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE}:
                if item_type == L_ITEM_TYPE_ROLE:
                    nd_item.lab_name.SetPosition('50%-42', '50%-154')
                nd_item.lab_name.SetString(get_lobby_item_name(item_no))
                nd_item.nd_reward_1.setVisible(True)
                nd_item.nd_reward_2.setVisible(False)
                nd_item.btn_look.setVisible(True)
                if item_type == L_ITEM_TYPE_MECHA_SKIN:
                    belong_name = get_lobby_item_belong_name(item_no)
                    nd_item.lab_name.SetString(belong_name)
                    nd_item.lab_skin.setVisible(True)
                    nd_item.lab_skin.SetString(get_lobby_item_name(item_no))
                else:
                    nd_item.lab_skin.setVisible(False)

                @nd_item.btn_look.unique_callback()
                def OnClick(btn, touch, item_id=item_no):
                    from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                    jump_to_display_detail_by_item_no(item_id)

            else:
                nd_item.btn_look.setVisible(False)
                nd_item.nd_reward_1.setVisible(False)
                nd_item.nd_reward_2.setVisible(True)
                nd_item.list_reward.SetInitCount(1)
                init_tempate_mall_i_item(nd_item.list_reward.GetItem(0), item_no, num)

    def init_scroll_list(self):
        self.scroll_list = self.panel.list_reward
        self.item_count = self.scroll_list.GetItemCount()
        if self.item_count <= 0:
            return
        scroll_list_width = self.scroll_list.GetContentSize()[0]
        container_width = self.scroll_list.getInnerContainer().getContentSize().width
        self.container_max_move = container_width - scroll_list_width
        self.item_width = self.scroll_list.GetTemplateConf()['size']['width']
        self.scroll_list.addEventListener(lambda *args: self.scroll_list.SetTimeOut(0.001, self.check_sview))
        self.panel.img_progress.setAnchorPoint(Vec2(0, 0.5))
        item_per_page = self.scroll_list.GetContentSize()[0] / self.item_width
        ratio = 1.0 * item_per_page / self.item_count
        ratio = min(1.0, max(0.1, ratio))
        bar_width = self.panel.progress_bar.GetContentSize()[0]
        img_width = bar_width * ratio
        img_height = self.panel.img_progress.GetContentSize()[1]
        self.panel.img_progress.SetContentSize(img_width, img_height)
        self._slider_min_pos = 0
        self._slider_max_pos = bar_width - img_width
        self.panel.img_progress.SetPosition('0', '50%0')
        self.panel.btn_right.BindMethod('OnClick', lambda *args: self.panel.list_reward.ScrollToRight(0.5))
        self.panel.btn_left.BindMethod('OnClick', lambda *args: self.panel.list_reward.ScrollToLeft(0.5))