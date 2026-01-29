# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/DanRankWidget.py
from __future__ import absolute_import
from logic.comsys.rank.BaseRankWidget import BaseRankWidget
from logic.gcommon.common_const import rank_const
from logic.gutils import role_head_utils
from logic.gutils import season_utils
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
from cocosui import cc, ccui, ccs
from logic.gcommon.common_const import friend_const, chat_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gcommon import time_utility
from common.utils import time_utils
import common.utils.timer as timer
import game3d
from logic.gutils import follow_utils
DOWN_COUNT_REFRESH_INTERVAL = 1.0
SUMMARY_LAST_TIME = 180

class DanRankWidget(BaseRankWidget):

    def __init__(self, parent_panel, nd, template_pos, rank_info):
        super(DanRankWidget, self).__init__(rank_info)
        self.parent_panel = parent_panel
        self.nd = nd
        self._template_root = global_data.uisystem.load_template_create('rank/i_rank_tier_list', parent=nd)
        self._template_root.setPosition(template_pos)
        self.list_rank = self._template_root.list_rank_list
        self.cur_rank_type = rank_const.RANK_TYPE_DAN_SURVIVAL
        self.cur_rank_area = None
        self.down_count_timer = None
        self.delay_exe_id = None
        self.init_list()
        self.init_rank_area_choose()
        self.init_refresh_time_lab()
        return

    def request_rank_data(self):
        super(DanRankWidget, self).request_rank_data()
        if self.cur_rank_area == rank_const.LINE_FRIEND_RANK:
            self._template_root.lab_player_level.SetString(81240)
            self._template_root.lab_score.SetString(15027)
        else:
            self._template_root.lab_player_level.SetString(81243)
            self._template_root.lab_score.SetString(15028)

    def init_refresh_time_lab(self):
        now = time_utility.time()
        if now <= time_utility.get_utc8_day_start_timestamp() + 5 * time_utility.ONE_HOUR_SECONS:
            self.down_count = time_utility.get_utc8_day_start_timestamp() + 5 * time_utility.ONE_HOUR_SECONS - time_utility.time()
        else:
            self.down_count = time_utility.get_utc8_day_start_timestamp() + time_utility.ONE_DAY_SECONDS + 5 * time_utility.ONE_HOUR_SECONS - time_utility.time()
        if self.down_count < 0.0:
            return
        else:
            self.delay_exe_id = None

            def refresh_lab--- This code section failed: ---

  66       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'down_count'
           6  LOAD_GLOBAL           1  'SUMMARY_LAST_TIME'
           9  COMPARE_OP            0  '<'
          12  POP_JUMP_IF_FALSE   126  'to 126'

  67      15  LOAD_DEREF            0  'self'
          18  LOAD_ATTR             2  '_template_root'
          21  LOAD_ATTR             3  'lab_count_down'
          24  LOAD_ATTR             4  'setString'
          27  LOAD_GLOBAL           5  'get_text_by_id'
          30  LOAD_CONST            1  15055
          33  CALL_FUNCTION_1       1 
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          

  69      40  LOAD_DEREF            0  'self'
          43  LOAD_ATTR             0  'down_count'
          46  LOAD_GLOBAL           1  'SUMMARY_LAST_TIME'
          49  UNARY_NEGATIVE   
          50  COMPARE_OP            0  '<'
          53  POP_JUMP_IF_FALSE   204  'to 204'

  70      56  LOAD_DEREF            0  'self'
          59  LOAD_ATTR             6  'down_count_timer'
          62  POP_JUMP_IF_FALSE    96  'to 96'

  71      65  LOAD_GLOBAL           7  'global_data'
          68  LOAD_ATTR             8  'game_mgr'
          71  LOAD_ATTR             9  'unregister_logic_timer'
          74  LOAD_DEREF            0  'self'
          77  LOAD_ATTR             6  'down_count_timer'
          80  CALL_FUNCTION_1       1 
          83  POP_TOP          

  72      84  LOAD_CONST            0  ''
          87  LOAD_DEREF            0  'self'
          90  STORE_ATTR            6  'down_count_timer'
          93  JUMP_FORWARD          0  'to 96'
        96_0  COME_FROM                '93'

  73      96  LOAD_GLOBAL          11  'game3d'
          99  LOAD_ATTR            12  'delay_exec'
         102  LOAD_CONST            2  1
         105  LOAD_DEREF            0  'self'
         108  LOAD_ATTR            13  'init_refresh_time_lab'
         111  CALL_FUNCTION_2       2 
         114  LOAD_DEREF            0  'self'
         117  STORE_ATTR           14  'delay_exe_id'
         120  JUMP_ABSOLUTE       204  'to 204'
         123  JUMP_FORWARD         78  'to 204'

  76     126  LOAD_GLOBAL          15  'time_utility'
         129  LOAD_ATTR            16  'get_day_hour_minute_second'
         132  LOAD_DEREF            0  'self'
         135  LOAD_ATTR             0  'down_count'
         138  CALL_FUNCTION_1       1 
         141  UNPACK_SEQUENCE_4     4 
         144  STORE_FAST            0  'day'
         147  STORE_FAST            1  'hour'
         150  STORE_FAST            2  'minute'
         153  STORE_FAST            3  'second'

  77     156  LOAD_FAST             1  'hour'
         159  LOAD_FAST             3  'second'
         162  BINARY_MULTIPLY  
         163  INPLACE_ADD      
         164  STORE_FAST            1  'hour'

  79     167  LOAD_DEREF            0  'self'
         170  LOAD_ATTR             2  '_template_root'
         173  LOAD_ATTR             3  'lab_count_down'
         176  LOAD_ATTR             4  'setString'
         179  LOAD_GLOBAL           5  'get_text_by_id'
         182  LOAD_CONST            4  15054
         185  LOAD_FAST             1  'hour'
         188  LOAD_FAST             2  'minute'
         191  LOAD_FAST             3  'second'
         194  BUILD_TUPLE_3         3 
         197  CALL_FUNCTION_2       2 
         200  CALL_FUNCTION_1       1 
         203  POP_TOP          
       204_0  COME_FROM                '123'
         204  LOAD_CONST            0  ''
         207  RETURN_VALUE     

Parse error at or near `INPLACE_ADD' instruction at offset 163

            def tick():
                self.down_count -= DOWN_COUNT_REFRESH_INTERVAL
                refresh_lab()

            refresh_lab()
            self.down_count_timer = global_data.game_mgr.register_logic_timer(tick, interval=DOWN_COUNT_REFRESH_INTERVAL, times=-1, mode=timer.CLOCK)
            return

    def refresh_item(self, panel, data):
        rank = int(data[3] + 1)
        if rank >= 1 and rank <= 3:
            panel.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
            panel.img_rank.setVisible(True)
            panel.lab_rank.setVisible(False)
        else:
            panel.img_rank.setVisible(False)
            panel.lab_rank.setVisible(True)
            panel.lab_rank.setString(str(rank))
        if rank == 0:
            panel.lab_rank.SetString(15051)
        panel.lab_player_name.setString(str(data[1][0]))
        role_head_utils.init_role_head(panel.player_role_head, data[1][2], data[1][3])
        follow_utils.refresh_rank_list_follow_status(panel, data[0], str(data[1][0]))
        desc_content = ''
        if data[2]:
            panel.temp_tier.setVisible(True)
            panel.icon_star.setVisible(True)
            panel.lab_star_number.setVisible(True)
            dan_info = {'dan': data[2][0],'lv': data[2][1]}
            role_head_utils.set_role_dan(panel.icon_tier, dan_info)
            desc_content = season_utils.get_dan_lv_name(data[2][0], data[2][1])
            panel.lab_star_number.setString('\xc3\x97{}'.format(data[2][2]))
            panel.icon_star.SetDisplayFrameByPath('', role_head_utils.get_star_path(data[2][0]))
            panel.temp_tier.img_tier.SetDisplayFrameByPath('', role_head_utils.get_dan_path(data[2][0], data[2][1]))
        else:
            panel.temp_tier.setVisible(False)
            panel.icon_star.setVisible(False)
            panel.lab_star_number.setVisible(False)
            desc_content = 15051
        social_friend = self._message_data.get_social_friend_by_uid(friend_const.SOCIAL_ID_TYPE_LINEGAME, data[0])
        if self.cur_rank_area == rank_const.LINE_FRIEND_RANK and social_friend and data[0] != global_data.player.uid:
            panel.temp_tier.setScaleX(1.0)
            panel.temp_tier.setScaleY(1.0)
            panel.temp_tier.SetPosition('100%-102', '50%10')
            panel.lab_star_number.SetPosition('100%-93', '50%-15')
            icon = '<img="{}",scale=0.65>'.format(chat_const.LINE_ICON)
            desc_content = '#SW{}#n#DG{}#n'.format(icon, self._message_data.get_line_friend_name(social_friend.get('social_id')))
            panel.lab_model.SetPosition('7', '50%-16')
        else:
            panel.temp_tier.setScaleX(0.8)
            panel.temp_tier.setScaleY(0.8)
            panel.lab_model.SetPosition('32', '50%-16')
            panel.temp_tier.SetPosition('6.15%', '28.33%')
            panel.lab_star_number.SetPosition('100%-93', '50%0')
        panel.lab_model.SetString(desc_content)
        self.add_player_simple_callback(panel.player_role_head, data, self._template_root.img_list_pnl)
        self.add_reques_model_info(panel, data[0])

    def destroy(self):
        if self.down_count_timer:
            global_data.game_mgr.unregister_logic_timer(self.down_count_timer)
            self.down_count_timer = None
        if self.delay_exe_id:
            game3d.cancel_delay_exec(self.delay_exe_id)
        super(DanRankWidget, self).destroy()
        return