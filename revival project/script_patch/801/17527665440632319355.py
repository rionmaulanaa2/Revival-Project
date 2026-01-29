# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/KizunaBadgeUI.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const, battle_const
import cc
from logic.gcommon import time_utility as tutil
REQUIRED_LV = 5

class KizunaBadgeUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/kizuna_live_medal'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'btn_get.OnClick': 'on_click_btn_get'
       }
    GLOBAL_EVENT = {'player_lv_update_event': 'on_player_lv_update'
       }

    def on_init_panel(self, *args, **kwargs):
        super(KizunaBadgeUI, self).on_init_panel()
        self.hide_main_ui()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self._is_click_get_reward = False
        self.refresh_panel()

    def refresh_panel(self):
        self.init_reward_list()
        if self.get_player_lv() < REQUIRED_LV:
            self.panel.lab_tips.setVisible(True)
        else:
            self.panel.lab_tips.setVisible(False)

    def init_reward_list(self, fake_received=False):
        is_received = fake_received or global_data.player and global_data.player.has_receive_normal_reward
        if is_received:
            self.panel.btn_get.SetEnable(False)
            self.panel.btn_get.SetText(604029)
        from common.cfg import confmgr
        view_rewards = confmgr.get('game_mode/concert/play_data', str('view_rewards'), default=[])
        self.panel.list_item.SetInitCount(0)
        if view_rewards:
            reward_id = view_rewards[0]
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            for reward_item_info in r_list:
                ui_widget = self.panel.list_item.AddTemplateItem()
                if reward_item_info:
                    item_no, item_num = reward_item_info
                    self.init_tempate_mall_i_item(ui_widget, item_no, item_num=item_num, callback=self.on_click_btn_get)
                    is_received = fake_received or global_data.player and global_data.player.has_receive_normal_reward
                    if not is_received:
                        ui_widget.PlayAnimation('get_tips')
                    else:
                        ui_widget.nd_get.setVisible(True)
                        ui_widget.nd_get_tips.setVisible(False)

        if len(view_rewards) > 1:
            lv_required_reward_id = view_rewards[1]
            r_list = confmgr.get('common_reward_data', str(lv_required_reward_id), 'reward_list', default=[])
            for reward_item_info in r_list:
                ui_widget = self.panel.list_item.AddTemplateItem()
                if reward_item_info:
                    item_no, item_num = reward_item_info
                    if self.get_player_lv() < REQUIRED_LV:
                        self.init_tempate_mall_i_item(ui_widget, item_no, item_num=item_num, show_tips=True)
                        ui_widget.nd_lock.setVisible(True)
                    else:
                        self.init_tempate_mall_i_item(ui_widget, item_no, item_num=item_num, callback=self.on_click_btn_get)
                        is_received = fake_received or global_data.player and global_data.player.has_receive_special_reward
                        if not is_received:
                            ui_widget.PlayAnimation('get_tips')
                        else:
                            ui_widget.nd_get.setVisible(True)
                            ui_widget.nd_get_tips.setVisible(False)

    def init_tempate_mall_i_item(self, temp_item_ui, item_id, item_num=0, isget=False, show_rare_degree=True, ignore_improve=False, show_tips=False, callback=None, templatePath=None, show_jump=True, force_rare_degree=None, force_extra_ani=False, show_rare_vx=False, show_all_num=False):
        from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_use_parms, get_lobby_item_name, lobby_item_vx_path
        from logic.gutils.template_utils import REWARD_RARE_ANI
        item_path = get_lobby_item_pic_by_item_no(item_id)
        temp_item_ui.item.SetDisplayFrameByPath('', item_path)
        if show_all_num or item_num > 1:
            temp_item_ui.lab_quantity.setVisible(True)
            temp_item_ui.lab_quantity.SetString(str(item_num))
        else:
            temp_item_ui.lab_quantity.setVisible(False)
        if temp_item_ui.lab_name:
            item_name = get_lobby_item_name(item_id)
            temp_item_ui.lab_name.SetString(item_name)
        temp_item_ui.nd_get.setVisible(isget)
        if show_rare_degree:
            is_use_dark_back = False
            if templatePath:
                is_use_dark_back = '_dark' in templatePath
            from logic.gutils.item_utils import get_lobby_item_rare_degree_pic_by_item_no, get_item_rare_degree
            if force_rare_degree is None:
                rare_degree = get_item_rare_degree(item_id, item_num, ignore_imporve=ignore_improve) if 1 else force_rare_degree
                ani = REWARD_RARE_ANI.get(rare_degree)
                all_ani_names = six_ex.values(REWARD_RARE_ANI)
                for ani_name in all_ani_names:
                    if not temp_item_ui.HasAnimation(ani_name) and temp_item_ui.nd_vx:
                        vx_node = getattr(temp_item_ui.nd_vx, ani_name)
                        if vx_node:
                            vx_node.setVisible(False)
                            lizi_nd = getattr(vx_node, 'lizi')
                            if lizi_nd:
                                lizi_nd.stopSystem()
                            vx_node.StopAnimation(ani_name)

                if ani and (force_extra_ani or not temp_item_ui.HasAnimation(ani) and temp_item_ui.nd_vx):
                    templatePath = 'common/i_item_dark_vx_%s' % ani
                    vx_node = getattr(temp_item_ui.nd_vx, ani)
                    if force_extra_ani or not vx_node:
                        vx_node = global_data.uisystem.load_template_create(templatePath, parent=temp_item_ui.nd_vx, name=ani)
                    if vx_node:
                        vx_node.setVisible(True)
                        lizi_nd = getattr(vx_node, 'lizi')
                        if lizi_nd:
                            lizi_nd.resetSystem()
                        vx_node.PlayAnimation(ani)
                else:
                    temp_item_ui.PlayAnimation(ani)
                item_vx = getattr(temp_item_ui.nd_special_vx, 'temp_vx', None)
                if show_rare_vx:
                    if item_vx is None:
                        item_vx = global_data.uisystem.load_template_create(lobby_item_vx_path, temp_item_ui.nd_special_vx, name='temp_vx')
                    item_vx.PlayAnimation('loop_' + ani)
                item_vx and item_vx.setVisible(show_rare_vx)
        if show_tips:

            @temp_item_ui.btn_choose.unique_callback()
            def OnClick(btn, touch):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True} if show_jump else {'show_jump': False}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=extra_info, item_num=item_num)
                return True

        if callback:
            if callback == False:

                @temp_item_ui.btn_choose.callback()
                def OnClick(btn, touch):
                    pass

                return

            @temp_item_ui.btn_choose.callback()
            def OnClick(btn, touch):
                callback()

            @temp_item_ui.btn_choose.unique_callback()
            def OnBegin(btn, touch):
                return True

            @temp_item_ui.btn_choose.unique_callback()
            def OnEnd(btn, touch):
                return True

        return

    def fake_success_received(self):
        self.init_reward_list(True)

    def on_finalize_panel(self):
        super(KizunaBadgeUI, self).on_finalize_panel()
        if not self._is_click_get_reward:
            global_data.game_mgr.show_tip(get_text_by_id(633940))
            if global_data.player:
                global_data.player.received_concert_reward()
        self.show_main_ui()

    def on_click_close_btn(self, btn, touch):
        self.close()

    def on_click_btn_get(self, *args):
        if global_data.player:
            self._is_click_get_reward = True
            global_data.player.received_concert_reward()
            self.fake_success_received()
            self.panel.btn_get.SetEnable(False)
            self.panel.btn_get.SetText(604029)

    def get_player_lv(self):
        if global_data.player:
            return global_data.player.get_lv()
        else:
            return 0

    def on_player_lv_update(self, data):
        self.refresh_panel()