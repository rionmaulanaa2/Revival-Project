# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerWelfare.py
from __future__ import absolute_import
from logic.gutils import item_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.item import item_const as iconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from cocosui import cc
from common.cfg import confmgr
from logic.gutils import template_utils
from random import randint
REWARD_ITEM_NO_ORDER = [
 50104011, 50301001, 50101208, 50101003]

class ActivitySummerWelfare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySummerWelfare, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_receive_summer_welfare_reward_event': self.on_receive_summer_welfare_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_receive_summer_welfare_reward(self):
        self.update_btn_confirm()
        global_data.emgr.refresh_activity_redpoint.emit()

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        reward_dict = global_data.player.get_summer_welfare_reward_dict()
        if not reward_dict:
            return
        photo_path = 'gui/ui_res_2/activity/activity_202107/weekend_welfare/img_photo%s.png' % randint(1, 4)
        self.panel.img_photo.SetDisplayFrameByPath('', photo_path)
        self.panel.img_photo_01.SetDisplayFrameByPath('', photo_path)
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        action_list.append(cc.DelayTime.create(0.17))
        reward_dict[iconst.ITEM_NO_GOLD] = 1
        if len(reward_dict) == 2:
            self.panel.lab_rich.SetString(get_text_by_id(609692))
        elif len(reward_dict) == 4:
            self.panel.lab_rich.SetString(get_text_by_id(609691))
        self.panel.list_items.SetInitCount(len(reward_dict))
        ordered_rewards = [ (item_no, reward_dict[item_no]) for item_no in REWARD_ITEM_NO_ORDER if item_no in reward_dict ]
        for i, item_pair in enumerate(ordered_rewards):
            item_no, item_num = item_pair
            if item_num <= 0:
                continue
            item_widget = self.panel.list_items.GetItem(i)
            if not item_widget:
                continue
            action_list.append(cc.CallFunc.create(lambda iw=item_widget: iw.PlayAnimation('in')))
            action_list.append(cc.CallFunc.create(lambda iw=item_widget: iw.PlayAnimation('loop')))
            rare_degree = item_utils.get_item_rare_degree(item_no)
            if rare_degree == iconst.RARE_DEGREE_3:
                item_widget.img_bule.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202107/weekend_welfare/pnl_purple.png')
            elif rare_degree == iconst.RARE_DEGREE_2:
                item_widget.img_bule.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202107/weekend_welfare/pnl_blue.png')
            if item_no != iconst.ITEM_NO_GOLD:
                item_widget.lab_num.SetString(str(item_num))
                item_widget.lab_words.SetString(item_utils.get_lobby_item_name(item_no))
                item_widget.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
            else:
                item_widget.img_bule.setVisible(False)
                item_widget.lab_num.setVisible(False)
                item_widget.lab_words.SetString(get_text_by_id(609716))
                item_widget.img_item.setScale(0.45)
                item_widget.img_item.SetPosition('50%0', '50%-16')
                item_widget.img_item.SetDisplayFrameByPath('', 'gui/ui_res_2/item/others/50101200.png')
            if item_no != iconst.ITEM_NO_GOLD:

                @item_widget.btn_choose.unique_callback()
                def OnClick(btn, touch, i_no=item_no, i_num=item_num):
                    x, y = btn.GetPosition()
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(i_no, None, wpos, item_num=i_num)
                    return

        self.panel.runAction(cc.Sequence.create(action_list))
        self.update_btn_confirm()

        @self.panel.btn_confirm.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.get_summer_welfare_reward()

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            conf = confmgr.get('c_activity_config', self._activity_type)
            if not conf:
                return
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(conf.get('cNameTextID', '')), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def update_btn_confirm(self):
        if not global_data.player:
            return
        if global_data.player.get_can_receive_summer_welfare_reward():
            self.panel.btn_confirm.SetText(609690)
            self.panel.btn_confirm.SetEnable(True)
        else:
            self.panel.btn_confirm.SetText(80866)
            self.panel.btn_confirm.SetEnable(False)

    @staticmethod
    def show_tab_rp(activity_id):
        if not global_data.player:
            return False
        return bool(global_data.player.get_can_receive_summer_welfare_reward())