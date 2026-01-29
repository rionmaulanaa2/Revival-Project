# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryPromareWidget.py
from __future__ import absolute_import
from logic.gutils.lobby_click_interval_utils import global_unique_click
from .LotteryArtCollectionWidget import LotteryArtCollectionWidget
from .LotterySelectRewardsWidget import LotteryPromareSelectRewardsWidget
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
ULTRA_SKIN = 201801151
SUB_SKIN = (201802151, 201001943)

class LotteryPromareWidget(LotteryArtCollectionWidget):

    def init_parameters(self):
        super(LotteryPromareWidget, self).init_parameters()
        self.nd_banner_top = None
        self.nd_banner_sub = []
        self.need_top_vx = False
        self.btn_exchange = None
        self.select_rewards_widget = None
        self.select_rewards_widget_opened_record_data = ArchiveManager().get_archive_data('select_rewards_widget_opened')
        self.selected_item_id = None
        for item_id in global_data.player.get_reward_choose_list(self.data['table_id']):
            self.selected_item_id = item_id

        self.force_select_rewards = not self.selected_item_id and not self.select_rewards_widget_opened_record_data.get(self.lottery_id)
        self.can_select_rewards = global_data.player.is_reward_choose_valid(self.data['table_id'])
        self.continue_to_buy_lottery_count = None
        return

    def _show_select_rewards_tips(self, parent):
        nd = global_data.uisystem.load_template_create('mall/i_lottery_tag_tips', parent=self.panel, name='nd_select_rewards_tips')
        pos = parent.getParent().convertToWorldSpace(parent.getPosition())
        pos = self.panel.convertToNodeSpace(pos)
        nd.setPosition(pos)
        nd.nd_splus_hint.setVisible(True)
        nd.PlayAnimation('show_hint')
        nd.PlayAnimation('show_hint_arrow')

    def _hide_select_rewards_tips(self):
        nd = getattr(self.panel, 'nd_select_rewards_tips', None)
        if nd:
            nd.nd_splus_hint.setVisible(False)
            nd.StopAnimation('show_hint')
            nd.StopAnimation('show_hint_arrow')
        return

    def init_panel(self):
        super(LotteryPromareWidget, self).init_panel()
        if self.force_select_rewards:
            self._show_select_rewards_tips(self.panel.list_tag.GetItem(0).img_class)

    def on_finalize_panel(self):
        super(LotteryPromareWidget, self).on_finalize_panel()
        self.select_rewards_widget_opened_record_data.save()
        self.select_rewards_widget_opened_record_data = None
        if self.select_rewards_widget:
            self.select_rewards_widget.close()
            self.select_rewards_widget = None
        return

    def check_item_got_func(self, item_id):
        return global_data.player.get_item_num_by_no(int(item_id)) > 0

    def select_rewards_callback(self, new_selected_item_id):
        self.selected_item_id = new_selected_item_id
        global_data.player.request_choose_reward(self.data['table_id'], (new_selected_item_id,))

    def hide_callback(self):
        if self.continue_to_buy_lottery_count is None:
            return
        else:
            self.buy_widget.on_click_btn_buy(self.continue_to_buy_lottery_count)
            self.continue_to_buy_lottery_count = None
            return

    def show_select_rewards_widget(self):
        if not self.select_rewards_widget:
            self.select_rewards_widget = LotteryPromareSelectRewardsWidget(None, SUB_SKIN, self.selected_item_id, self.check_item_got_func, self.select_rewards_callback, self.hide_callback)
        self.select_rewards_widget.show(self.selected_item_id)
        self.select_rewards_widget_opened_record_data[self.lottery_id] = True
        self._hide_select_rewards_tips()
        return

    def special_buy_logic_func(self, price_info, lottery_count):
        if self.force_select_rewards and not self.select_rewards_widget_opened_record_data.get(self.lottery_id):
            self.continue_to_buy_lottery_count = lottery_count
            self.show_select_rewards_widget()
            return True
        return super(LotteryPromareWidget, self).special_buy_logic_func(price_info, lottery_count)

    def update_one_banner(self, nd_banner, data):
        super(LotteryPromareWidget, self).update_one_banner(nd_banner, data)
        banner_id, index = data
        if banner_id == ULTRA_SKIN:
            self.nd_banner_top = nd_banner
            nd_banner.setLocalZOrder(2)
            if not global_data.player.get_item_num_by_no(banner_id):
                self.need_top_vx = True
                self.btn_exchange = global_data.uisystem.load_template_create('activity/activity_202203/promare/exchange/i_promare_exchange_tag.json', nd_banner.temp_limit, name='btn_exchange')

                @self.btn_exchange.btn_jump.callback()
                def OnClick(*args):
                    global_data.ui_mgr.show_ui('ActivityPromareExchange', 'logic.comsys.activity.ActivityPromare')

                self.btn_exchange.SetPosition('50%-7', '50%')
                self.update_btn_exchange()
        elif banner_id in SUB_SKIN:
            self.nd_banner_sub.append(nd_banner)

    def show(self):
        self.panel.setVisible(True)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('change')
        self.panel.StopAnimation('begin')
        self.panel.PlayAnimation('end')
        self.need_top_vx = self.need_top_vx and global_data.achi_mgr.get_cur_user_archive_data('promare_lottery_vx', default=0) == 0
        self.nd_banner_top.temp_limit.setVisible(not self.need_top_vx)
        if self.need_top_vx:

            def sub_banner_flash():
                for sub_banner in self.nd_banner_sub:
                    sub_banner.PlayAnimation('shinning')

            action_list = [cc.DelayTime.create(1),
             cc.CallFunc.create(lambda : self.nd_banner_top.temp_limit.setVisible(True)),
             cc.CallFunc.create(lambda : self.nd_banner_top.temp_limit.btn_exchange.PlayAnimation('lock')),
             cc.DelayTime.create(1),
             cc.CallFunc.create(lambda : self.nd_banner_top.PlayAnimation('shinning')),
             cc.DelayTime.create(0.4),
             cc.CallFunc.create(lambda : self.nd_banner_top.PlayAnimation('trail')),
             cc.DelayTime.create(0.6),
             cc.CallFunc.create(sub_banner_flash),
             cc.DelayTime.create(0.4),
             cc.CallFunc.create(lambda : global_data.achi_mgr.set_cur_user_archive_data('promare_lottery_vx', 1))]
        else:
            action_list = [
             cc.DelayTime.create(0.4),
             cc.CallFunc.create(self._play_flash_anim)]
        self.panel.runAction(cc.Sequence.create(action_list))
        self._release_tips_anim_timer()
        from common.utils.timer import CLOCK
        if not self.check_show_shop():
            self.tips_anim_timer = global_data.game_mgr.register_logic_timer(self._show_shop, interval=0.2, times=1, mode=CLOCK)

    def _init_rule_tag_list(self):
        from common.cfg import confmgr
        from common.utilities import safe_percent
        tag_list = self.panel.list_tag
        rule_tag_list = self.data.get('rule_tag_list', [])
        rule_tag_conf = confmgr.get('lottery_rule_config', default={})

        def init_item(item, rule_conf):
            tag_text = rule_conf.get('tag_text')
            desc_text = rule_conf.get('desc_text')
            icon_path = rule_conf.get('icon')
            item.lab_tag.SetString(tag_text)
            item.img_class.setVisible(bool(icon_path))
            item.img_class.SetDisplayFrameByPath('', icon_path)
            if item.nd_prog:
                category = rule_conf.get('guarantee_category')
                item.nd_prog.setVisible(category is not None)
                total, line_no = self.data.get('category_floor', {}).get(str(category), [0, 0])
                cur = global_data.player.get_reward_category_floor(self.data['table_id'], line_no)
                item.prog_tag.SetPercent(safe_percent(cur, total))
                item.lab_tag.SetString(609507)
                item.lab_tag_num.SetString(get_text_by_id(609508).format(cur, total))
            return

        tag_list.SetInitCount(len(rule_tag_list))
        for i, item in enumerate(tag_list.GetAllItem()):
            rule_id = rule_tag_list[i]
            rule_conf = rule_tag_conf.get(str(rule_id), {})
            init_item(item, rule_conf)

        self.can_select_rewards = global_data.player.is_reward_choose_valid(self.data['table_id'])

        @global_unique_click(tag_list.GetItem(0).nd_tag)
        def OnClick(*args):
            if not self.can_select_rewards:
                global_data.game_mgr.show_tip(get_text_by_id(611453))
                return
            for item_id in SUB_SKIN:
                if global_data.player.get_item_num_by_no(item_id) > 0:
                    global_data.game_mgr.show_tip(get_text_by_id(611453))
                    return

            self.show_select_rewards_widget()

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,
           'refresh_lottery_limited_guarantee_round': self._init_rule_tag_list,
           'lottery_open_box_result': self._on_lottery_open_box_result,
           'lottery_ten_try_update': self.refresh_10_try_entrance,
           'player_item_update_event_with_id': self.item_update
           }
        return econf

    def item_update(self, item_id):
        if item_id in SUB_SKIN:
            self.update_btn_exchange()
        if item_id == ULTRA_SKIN:
            self.refresh_items_own_status([item_id])
            self.btn_exchange.setVisible(False)

    def update_btn_exchange(self):
        if not self.btn_exchange:
            return
        can_exchange = True
        for sub_skin in SUB_SKIN:
            if not global_data.player.get_item_num_by_no(sub_skin):
                can_exchange = False
                break

        self.btn_exchange.lab_exchange.SetString(610783 if can_exchange else 610782)
        if can_exchange:
            self.btn_exchange.icon_type.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202203/promare/exchange/btn_promare_go.png')