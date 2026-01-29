# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIExchange.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.gutils.template_utils import init_price_view
from logic.gcommon.time_utility import get_readable_time
from logic.client.const import mall_const
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils import mall_utils
from common.cinematic.VideoPlayer import VideoPlayer
from logic.gutils.activity_utils import get_left_time
from common.utils.timer import CLOCK
from common.cfg import confmgr
from logic.gcommon.item import item_const
VIDEO_PATH = [
 'video/fireworks/primary_firework.mp4',
 'video/fireworks/middle_firework.mp4',
 'video/fireworks/high_firework_1.mp4',
 'video/fireworks/high_firework_2.mp4',
 'video/fireworks/high_firework_3.mp4',
 'video/fireworks/high_firework_4.mp4']

class ActivityKizunaAIExchange(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaAIExchange, self).__init__(dlg, activity_type)
        self._need_bg = False
        self.init_parameters()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        self.stop_video()
        self.unregister_timer()

    def on_init_panel(self):
        self.refresh_panel()
        conf = confmgr.get('c_activity_config', self._activity_type)
        self.register_timer()

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = conf.get('cDescTextID', '')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        @self.panel.btn_change.unique_callback()
        def OnClick(btn, touch):
            if self.select_index != 2:
                return
            self.sub_index += 1
            self.sub_index %= 4
            self._play_video(self.select_index + self.sub_index)

        self.panel.PlayAnimation('show')

    def init_parameters(self):
        self.primary_firework = '1059960'
        self.middle_firework = '1059961'
        self.discount_high_firework = '105996501'
        self.high_firework = '1059965'
        self.all_item_ids = ['1059960', '1059961', '1059962', '1059964', '1059963', '1059965']
        self.high_firework_item_ids = ['1059962', '1059964', '1059963', '1059965']
        self.select_index = 0
        self._video_play_widget = None
        self.sub_index = 0
        self.timer_id = None
        self.cur_video = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self._on_item_update,
           'buy_good_success': self._on_buy_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_time(self):
        left_time = get_left_time(self._activity_type)
        self.panel.lab_time.setVisible(left_time >= 0)
        self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))

    def register_timer(self):
        self.unregister_timer()
        self.refresh_time()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.refresh_time, interval=1, times=-1, mode=CLOCK)

    def unregister_timer(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return

    def _on_item_update(self, *args):
        player = global_data.player
        if not player.requested_buy_goods:
            self.refresh_panel()

    def _on_buy_success(self, *args, **kargs):
        player = global_data.player
        if player.requested_buy_goods:
            self.refresh_panel()

    def refresh_panel(self):
        list_node = self.panel.list_item
        list_node.SetInitCount(3)
        limite_by_day, _, _ = mall_utils.buy_num_limite_by_day(self.discount_high_firework)
        if limite_by_day:
            high_firework = self.high_firework
        else:
            high_firework = self.discount_high_firework
        for index, item in enumerate(list_node.GetAllItem()):
            if index == 0:
                goods_id = self.primary_firework
                item_num = global_data.player.get_item_num_by_no(int(self.primary_firework))
            elif index == 1:
                goods_id = self.middle_firework
                item_num = global_data.player.get_item_num_by_no(int(self.middle_firework))
            else:
                goods_id = high_firework
                item_num = 0
                for item_id in self.high_firework_item_ids:
                    item_num += global_data.player.get_item_num_by_no(int(item_id))

            item.temp_item.item.SetDisplayFrameByPath('', mall_utils.get_goods_pic_path(goods_id))
            item.lab_name.SetString(mall_utils.get_goods_name(goods_id))
            init_price_view(item.temp_price, goods_id, color=mall_const.DARK_PRICE_COLOR)
            item.lab_num.SetString(get_text_by_id(907101).format(item_num))
            item.PlayAnimation('loop_btn')

            @item.btn_buy.unique_callback()
            def OnClick(btn, touch, goods=goods_id):
                GroceriesBuyConfirmUI(goods_id=goods, need_show=item_const.ITEM_SHOW_TYPE_ITEM)

            @item.btn_choose.unique_callback()
            def OnClick(btn, touch, index=index):
                self.select_index = index
                self.sub_index = 0
                self.refresh_select_item()

        self.refresh_select_item()

    def refresh_select_item(self):
        self._play_video(self.select_index)
        list_node = self.panel.list_item
        for index, item in enumerate(list_node.GetAllItem()):
            selected = index == self.select_index
            item.btn_choose.SetSelect(selected)
            item_nd = getattr(self.panel, 'nd_levle_%d' % (index + 1))
            item_nd and item_nd.setVisible(selected)

    def stop_video(self):
        self.panel.nd_content.stopAllActions()
        ui = global_data.ui_mgr.get_ui('ActivityKizunaAIConcertMainUI')
        ui and ui.panel.nd_video_bg.setVisible(True)
        VideoPlayer().stop_video()

    def _play_video(self, index):
        if index < len(self.all_item_ids):
            pic_path = get_lobby_item_pic_by_item_no(self.all_item_ids[index])
            self.panel.temp_item.item.SetDisplayFrameByPath('', pic_path)
        video_path = VIDEO_PATH[index]
        if video_path == self.cur_video:
            return
        else:

            def _cb():
                if self.panel and self.panel.isValid():

                    def _hide():
                        ui = global_data.ui_mgr.get_ui('ActivityKizunaAIConcertMainUI')
                        ui and ui.panel.nd_video_bg.setVisible(False)

                    self.panel.nd_content.SetTimeOut(0.1, _hide)

            self.stop_video()
            self.cur_video = video_path
            VideoPlayer().play_video(VIDEO_PATH[index], None, {}, 0, None, True, video_ready_cb=_cb)
            return