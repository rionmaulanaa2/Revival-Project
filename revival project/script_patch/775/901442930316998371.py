# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/CorpTaskWidget.py
from __future__ import absolute_import
from six.moves import range
from .CommonTaskWidget import CommonTaskWidget
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from common.framework import Functor
from common.cfg import confmgr
from logic.gutils.template_utils import init_common_reward_list_simple
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils import task_utils
from logic.gcommon import time_utility as tutil
from logic.gutils.new_template_utils import VitalityBoxReward
from logic.gcommon.common_const import task_const
from common.utils.timer import CLOCK
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
import logic.gcommon.const as gconst
from logic.gutils.jump_to_ui_utils import jump_to_charge
from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_CORP_TASK
corp_task_node_cfg = (
 ('nd_middle', 'temp_contrast_middle', 'appear_2', 'disappear2'),
 ('nd_left', 'temp_contrast_left', 'appear_1', 'disappear1'),
 ('nd_right', 'temp_contrast_right', 'appear_3', 'disappear3'))
corp_task_lv_cfg = (
 ('gui/ui_res_2/task/contrast_task/pnl_jonior_contrast.png', 602035, 'gui/ui_res_2/task/contrast_task/progress_bar_jonior.png'),
 ('gui/ui_res_2/task/contrast_task/pnl_general_contrast.png', 602036, 'gui/ui_res_2/task/contrast_task/progress_bar_general.png'),
 ('gui/ui_res_2/task/contrast_task/pnl_senior_contrast.png', 602037, 'gui/ui_res_2/task/contrast_task/progress_bar_senior.png'),
 ('gui/ui_res_2/task/contrast_task/pnl_top_contrast.png', 602038, 'gui/ui_res_2/task/contrast_task/progress_bar_top.png'))

class CorpTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(CorpTaskWidget, self).__init__(parent, panel, task_type, False)
        temp_content = getattr(self.parent.nd_cut, 'temp_content')
        pos = temp_content.GetPosition()
        self.nd_content = global_data.uisystem.load_template_create('task/contrast/i_contrast_main')
        self.panel.nd_cut.AddChild('corp_task', self.nd_content)
        self.nd_content.ResizeAndPosition()
        self.nd_content.SetPosition(*pos)
        self.nd_content.setAnchorPoint(temp_content.getAnchorPoint())
        self._tip_timer = None
        self._day_start_time = tutil.get_utc8_day_start_timestamp()
        self._disappear_timer = None
        return

    def init_event(self):
        super(CorpTaskWidget, self).init_event()
        global_data.emgr.corp_task_changed_event += self.on_corp_task_changed

        @self.nd_content.btn_question.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(602039), get_text_by_id(602040))

    def init_widget--- This code section failed: ---

  66       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'CorpTaskWidget'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'init_widget'
          15  LOAD_FAST             1  'need_hide'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          

  68      22  LOAD_GLOBAL           3  'PriceUIWidget'
          25  LOAD_GLOBAL           1  'CorpTaskWidget'
          28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             4  'panel'
          34  LOAD_ATTR             5  'list_price'
          37  CALL_FUNCTION_257   257 
          40  LOAD_FAST             0  'self'
          43  STORE_ATTR            6  'price_top_widget'

  69      46  LOAD_FAST             0  'self'
          49  LOAD_ATTR             6  'price_top_widget'
          52  LOAD_ATTR             7  'show_money_types'
          55  LOAD_GLOBAL           8  'gconst'
          58  LOAD_ATTR             9  'SHOP_PAYMENT_DIAMON'
          61  LOAD_GLOBAL           8  'gconst'
          64  LOAD_ATTR            10  'SHOP_PAYMENT_YUANBAO'
          67  BUILD_LIST_2          2 
          70  CALL_FUNCTION_1       1 
          73  POP_TOP          

  71      74  LOAD_FAST             0  'self'
          77  LOAD_ATTR            11  'init_task_content'
          80  CALL_FUNCTION_0       0 
          83  POP_TOP          

  72      84  LOAD_FAST             0  'self'
          87  LOAD_ATTR            12  'init_tips'
          90  CALL_FUNCTION_0       0 
          93  POP_TOP          

  73      94  LOAD_FAST             0  'self'
          97  LOAD_ATTR            13  'nd_content'
         100  LOAD_ATTR            14  'PlayAnimation'
         103  LOAD_CONST            2  'show'
         106  CALL_FUNCTION_1       1 
         109  POP_TOP          

  75     110  LOAD_GLOBAL          15  'global_data'
         113  LOAD_ATTR            16  'player'
         116  LOAD_ATTR            17  'read_new_corp_task'
         119  CALL_FUNCTION_0       0 
         122  POP_TOP          

  76     123  LOAD_GLOBAL          15  'global_data'
         126  LOAD_ATTR            18  'ui_mgr'
         129  LOAD_ATTR            19  'get_ui'
         132  LOAD_CONST            3  'LobbyUI'
         135  CALL_FUNCTION_1       1 
         138  STORE_FAST            2  'lobby_ui'

  77     141  LOAD_FAST             2  'lobby_ui'
         144  POP_JUMP_IF_FALSE   160  'to 160'

  78     147  LOAD_FAST             2  'lobby_ui'
         150  LOAD_ATTR            20  'refresh_task_main_redpoint'
         153  CALL_FUNCTION_0       0 
         156  POP_TOP          
         157  JUMP_FORWARD          0  'to 160'
       160_0  COME_FROM                '157'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 37

    def set_visible(self, is_visible):
        self.nd_content.setVisible(is_visible)
        self.price_top_widget.list_money.setVisible(is_visible)

    @staticmethod
    def get_task_ids():
        return global_data.player.get_corp_task_ids()

    def init_task_content(self):
        player = global_data.player
        if not player:
            return
        else:
            self.task_ids = self.get_task_ids()
            self.task_dict = {}
            for idx in range(0, task_const.CORP_TASK_MAX_NUM):
                if idx >= len(self.task_ids):
                    self.set_task_node_template(idx, None)
                else:
                    task_id = self.task_ids[idx]
                    if player.has_receive_reward(task_id):
                        self.set_task_node_template(idx, None)
                    else:
                        self.set_task_node_template(idx, task_id)

            return

    def init_tips(self):
        cap_str = '%s/%s' % (global_data.player.get_corp_task_num(), task_const.CORP_TASK_MAX_NUM)
        self.nd_content.lab_limit.SetString(get_text_by_id(602041).format(cap_str))
        if not global_data.player.is_corp_task_full():
            self.nd_content.lab_next_time.SetString(get_text_by_id(602026))
        elif global_data.player.is_corp_task_full():
            self.nd_content.lab_next_time.SetString(get_text_by_id(602027))

    def _on_receive_reward_succ(self, task_id):
        if task_id not in self.task_ids:
            return
        super(CorpTaskWidget, self)._on_receive_reward_succ(task_id)
        self.init_tips()

    def _get_task_item_by_idx(self, idx):
        nd_name = corp_task_node_cfg[idx][0]
        nd_node = getattr(self.nd_content, nd_name)
        if not nd_node:
            return (None, None)
        else:
            task_node_name = corp_task_node_cfg[idx][1]
            task_item_node = getattr(nd_node, task_node_name)
            return (
             nd_node, task_item_node)

    def init_task_item(self, nd_task_item, task_id):
        super(CorpTaskWidget, self).init_task_item(nd_task_item, task_id)
        self._set_corp_task_level(nd_task_item, task_id)

        def change_task_by_yuanbao(tid):
            from logic.gutils.mall_utils import check_yuanbao
            if check_yuanbao(task_const.CHG_CORP_NEED_YUANBAO):
                global_data.player.change_corp_task(task_const.PAY_CHANGE_CORP_YUANBAO, tid)

        @nd_task_item.btn_refresh.unique_callback()
        def OnClick(btn, touch, tid=task_id):
            if global_data.player.has_receive_reward(task_id):
                return
            if global_data.player.get_free_chg_times() > 0:
                SecondConfirmDlg2().confirm(content=get_text_by_id(602031), confirm_callback=lambda : global_data.player.change_corp_task(task_const.FREE_CHANGE_CORP, tid))
            elif global_data.player.get_diamond() >= task_const.CHG_CORP_NEED_DIAMOND:
                SecondConfirmDlg2().confirm(content=get_text_by_id(602032).format(task_const.CHG_CORP_NEED_DIAMOND), confirm_callback=lambda : global_data.player.change_corp_task(task_const.PAY_CHANGE_CORP, tid))
            else:
                SecondConfirmDlg2().confirm(content=get_text_by_id(12124).format(task_const.CHG_CORP_NEED_YUANBAO), confirm_callback=lambda : change_task_by_yuanbao(tid))

        title = task_utils.get_corp_task_title(task_id)
        nd_task_item.lab_task_title.SetString(title)
        if task_id in global_data.player.get_new_corp_task_ids():
            nd_task_item.temp_new.setVisible(True)
            nd_task_item.temp_new.PlayAnimation('show')

    def set_task_node_template(self, idx, task_id):
        nd_node, task_node = self._get_task_item_by_idx(idx)
        pos = task_node.GetPosition()
        rot = task_node.getRotation()
        task_node_name = corp_task_node_cfg[idx][1]
        if task_id:
            tmpl_name = 'task/contrast/i_contrast_task'
        else:
            tmpl_name = 'task/contrast/i_contrast_task_empty'
        new_task_node = global_data.uisystem.load_template_create(tmpl_name)
        task_node.Destroy()
        nd_node.AddChild(task_node_name, new_task_node)
        new_task_node.ResizeAndPosition()
        new_task_node.SetPosition(*pos)
        new_task_node.setRotation(rot)
        if task_id:
            self.init_task_item(new_task_node, task_id)
        else:
            seq = global_data.player.get_vacancy_seq().index(idx) + 1
            if seq < 1:
                log_error('invalid idx of empty corp task, idx=%s, corp_task_ids=%s, vacancy_seq=%s' % (idx, global_data.player.get_corp_task_ids(), global_data.player.get_vacancy_seq()))
            self.init_empty_task_item(new_task_node, seq)

    def init_empty_task_item(self, nd_empty_task_item, seq):
        next_auto_chg_ts = self._day_start_time + seq * tutil.ONE_DAY_SECONDS + 5 * tutil.ONE_HOUR_SECONS
        now = tutil.time()
        nd_empty_task_item.lab_time.StopTimerAction()
        total_left_time = next_auto_chg_ts - now

        def count_down(pass_time):
            left_time = total_left_time - pass_time
            if left_time >= 0:
                time_str = tutil.get_readable_time_hour_minitue_sec(left_time)
                nd_empty_task_item.lab_time.SetString(time_str)
            else:
                nd_empty_task_item.lab_time.StopTimerAction()

        if total_left_time > 0:
            time_str = tutil.get_readable_time_hour_minitue_sec(total_left_time)
            nd_empty_task_item.lab_time.SetString(time_str)
            nd_empty_task_item.lab_time.TimerAction(count_down, total_left_time, interval=0.2)

    def _confirm_change_task(self, change_type, task_id):
        global_data.player.change_corp_task(change_type, task_id)

    def _set_corp_task_level(self, task_item, task_id):
        corp_lv = global_data.player.get_task_content(task_id, 'corp_lv', 1)
        lv_cfg = corp_task_lv_cfg[corp_lv - 1]
        task_item.img_bg.SetDisplayFrameByPath('', lv_cfg[0])
        task_item.lab_contrast_name.SetString(get_text_by_id(lv_cfg[1]))
        task_item.nd_progress.progress_task.LoadTexture(lv_cfg[2])

    def _set_task_item_progress(self, task_item):
        player = global_data.player
        if not player:
            return
        if not task_item:
            return
        task_id = task_item.task_id
        prog = player.get_task_prog(task_id)
        total_prog = task_utils.get_total_prog(task_id)
        task_item.nd_progress.lab_task_progress.SetString('%s/%s' % (prog, total_prog))
        task_item.nd_progress.progress_task.SetPercent(int(100.0 * prog / total_prog))
        if prog >= total_prog:
            self._set_task_reward_status(task_item)

    def try_auto_change_task(self, task_id):
        if task_id not in self.task_ids:
            return
        else:
            if len(self.task_ids) >= task_const.CORP_TASK_MAX_NUM:
                global_data.player.change_corp_task(task_const.AUTO_CHANGE_CORP, task_id)
            else:
                global_data.player.change_corp_task(task_const.AUTO_CHANGE_CORP, None)
            return

    def on_corp_task_changed(self, old_task_id, new_task_id):
        self.init_tips()
        idx = self.task_ids.index(new_task_id)

        def disappear_cb():
            self._disappear_timer = None
            self.nd_content.StopAnimation(corp_task_node_cfg[idx][3])
            self.set_task_node_template(idx, new_task_id)
            self.nd_content.PlayAnimation(corp_task_node_cfg[idx][2])
            return

        if old_task_id:
            ani_name = corp_task_node_cfg[idx][3]
            self.nd_content.PlayAnimation(ani_name)
            ani_time = self.nd_content.GetAnimationMaxRunTime(ani_name)
            self._disappear_timer = global_data.game_mgr.register_logic_timer(disappear_cb, interval=ani_time, times=1, mode=CLOCK)
        else:
            disappear_cb()

    def _set_task_reward_status(self, task_item):
        super(CorpTaskWidget, self)._set_task_reward_status(task_item)
        if not task_item:
            return
        else:
            task_id = task_item.task_id
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_RECEIVED:
                idx = self.task_ids.index(task_id)
                self.set_task_node_template(idx, None)
            else:
                task_item.btn_refresh.setVisible(True)
            return

    @staticmethod
    def check_red_point():
        if not is_sys_unlocked(SYSTEM_CORP_TASK):
            return False
        for task_id in CorpTaskWidget.get_task_ids():
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                return True

        if global_data.player.get_new_corp_task_ids():
            return True
        return False

    def destroy(self):
        self.price_top_widget.destroy()
        self.price_top_widget = None
        if self._disappear_timer:
            global_data.game_mgr.unregister_logic_timer(self._disappear_timer)
            self._disappear_timer = None
        global_data.emgr.corp_task_changed_event -= self.on_corp_task_changed
        super(CorpTaskWidget, self).destroy()
        return