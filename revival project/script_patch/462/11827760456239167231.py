# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAISixBenefits.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.time_utility import get_server_time, get_date_str
from logic.gutils.jump_to_ui_utils import jump_to_activity, jump_to_charge
from logic.client.path_utils import SIX_BENEFITS_NODE_PIC_PATH, SIX_BENEFITS_ITEM_UNOPEN_PIC_PATH, SIX_BENEFITS_ITEM_OPEN_PIC_PATH
from logic.gcommon.time_utility import get_readable_time, ONE_DAY_SECONDS
from logic.gcommon.common_const.activity_const import ACTIVITY_KIZUNA_AI_GIFT
from logic.gutils.task_utils import get_raw_left_open_time
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.timer import CLOCK
from common.cfg import confmgr
import cc
ACTIVITY_LIST = [
 10302, 10303, 10304, 10305, 10306, 10307]
SPECIAL_REWARD_ITEM_ID = 30601408

class ActivityKizunaAISixBenefits(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaAISixBenefits, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_event(True)
        self.panel.RecordAnimationNodeState('loop_emoji')
        self.panel.RecordAnimationNodeState('loop_light')

    def on_init_panel(self):
        self.init_base_info()
        self.init_activity_list()
        self.refresh_special_reward_item()
        self.register_timer()
        self.panel.PlayAnimation('show')

    def refresh_panel(self):
        self.init_base_info()
        self.init_activity_list()
        self.refresh_special_reward_item()
        self.register_timer()

    def init_base_info(self):
        attended_activity_count = len(global_data.player.get_task_content(self.task_id, 'activity', default=[]))
        self.panel.lab_num.SetString('{}/5'.format(attended_activity_count))
        percent = 25 * (attended_activity_count - 1)
        if percent < 0:
            percent = 0
        self.panel.progress_bar.SetPercent(percent)
        self.panel.PlayAnimation('show_ear1')
        self.panel.PlayAnimation('loop_ear1')
        for i in range(attended_activity_count):
            nd = getattr(self.panel, 'img_node_{}'.format(i + 1))
            nd.SetDisplayFrameByPath('', SIX_BENEFITS_NODE_PIC_PATH)
            nd.img_reach.setVisible(True)
            self.panel.PlayAnimation('show_ear{}'.format(i + 1))
            self.panel.PlayAnimation('loop_ear{}'.format(i + 1))
            nd.ChildResizeAndPosition()

    def refresh_special_reward_item(self):
        attended_activity_count = len(global_data.player.get_task_content(self.task_id, 'activity', default=[]))
        if attended_activity_count == 5 and global_data.player.get_item_num_by_no(SPECIAL_REWARD_ITEM_ID) <= 0:
            self.panel.PlayAnimation('loop_emoji')
            self.panel.PlayAnimation('loop_light')
            self.panel.btn_reward.SetEnable(True)

            @self.panel.btn_reward.unique_callback()
            def OnClick(*args):
                global_data.player.receive_task_reward(self.task_id)

        else:
            if global_data.player.get_item_num_by_no(SPECIAL_REWARD_ITEM_ID) > 0:
                self.panel.btn_reward.pnl_get.setVisible(True)
            self.panel.btn_reward.SetEnable(False)
            self.panel.StopAnimation('loop_emoji')
            self.panel.RecoverAnimationNodeState('loop_emoji')
            self.panel.StopAnimation('loop_light')
            self.panel.RecoverAnimationNodeState('loop_light')

    def _get_anim_action(self, item, anim_name):
        return cc.CallFunc.create(lambda : item.PlayAnimation(anim_name))

    def init_activity_list(self):
        cur_time = get_server_time()
        activity_conf = confmgr.get('c_activity_config')
        attended_activity = global_data.player.get_task_content(self.task_id, 'activity', default=[])
        action_list = [cc.DelayTime.create(0.3)]
        for index, activity_id in enumerate(ACTIVITY_LIST):
            item_widget = getattr(self.panel.nd_list, 'temp_{}'.format(index + 1), None)
            if item_widget:
                conf = activity_conf[str(activity_id)]
                if str(activity_id) in attended_activity:
                    item_widget.img_tips.setVisible(True)
                begin_time = conf.get('cBeginTime', 0)
                end_time = conf.get('cEndTime', 0)
                if begin_time == 0:
                    task_id = conf.get('cTask', '')
                    if task_id:
                        task_conf = task_utils.get_task_conf_by_id(task_id)
                        begin_time = task_conf.get('start_time', 0)
                        end_time = task_conf.get('end_time', 0)
                start_date = get_date_str('%m.%d', begin_time)
                finish_date = get_date_str('%m.%d', end_time, ignore_second=18000)
                item_widget.lab_end.SetString('{}-{}'.format(start_date, finish_date))
                if cur_time < begin_time:
                    item_widget.img_unstarted.setVisible(True)
                    item_widget.btn_bar.SetFrames('', [SIX_BENEFITS_ITEM_UNOPEN_PIC_PATH, SIX_BENEFITS_ITEM_UNOPEN_PIC_PATH, SIX_BENEFITS_ITEM_UNOPEN_PIC_PATH], False, None)

                    @item_widget.btn_bar.unique_callback()
                    def OnClick(layer, touch):
                        global_data.game_mgr.show_tip(get_text_by_id(601222))

                elif cur_time > end_time:
                    item_widget.btn_bar.SetFrames('', [SIX_BENEFITS_ITEM_OPEN_PIC_PATH, SIX_BENEFITS_ITEM_OPEN_PIC_PATH, SIX_BENEFITS_ITEM_OPEN_PIC_PATH], False, None)
                    item_widget.img_finish.setVisible(True)
                    item_widget.btn_bar.SetEnable(False)
                else:
                    item_widget.PlayAnimation('loop')
                    item_widget.btn_bar.SetFrames('', [SIX_BENEFITS_ITEM_OPEN_PIC_PATH, SIX_BENEFITS_ITEM_OPEN_PIC_PATH, SIX_BENEFITS_ITEM_OPEN_PIC_PATH], False, None)

                    @item_widget.btn_bar.unique_callback()
                    def OnClick(layer, touch, a_id=activity_id):
                        if str(a_id) == ACTIVITY_KIZUNA_AI_GIFT:
                            from logic.comsys.charge_ui import ChargeUINew
                            jump_to_charge(ChargeUINew.ACTIVITY_KIZUNA_AI_GIFT)
                        else:
                            jump_to_activity(str(a_id))

                item_widget.setVisible(False)
                action_list.append(cc.DelayTime.create(0.08))
                action_list.append(self._get_anim_action(item_widget, 'show'))

        self.panel.runAction(cc.Sequence.create(action_list))
        return

    def refresh_time(self):
        if not self.panel or not self.panel.lab_time:
            return
        left_time = get_raw_left_open_time(self.task_id)
        if left_time > 0:
            self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = ONE_DAY_SECONDS + left_time
            self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(close_left_time)))

    def register_timer(self):
        self.unregister_timer()
        self.refresh_time()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.refresh_time, interval=1, times=-1, mode=CLOCK)

    def unregister_timer(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def init_parameters(self):
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask')
        self.timer_id = None
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.refresh_special_reward_item,
           'receive_task_reward_succ_event': self.on_update_reward,
           'update_task_content_event': self.on_update_task_content
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)

    def on_update_task_content(self, task_id):
        if task_id == self.task_id:
            global_data.player.read_activity_list(self._activity_type)