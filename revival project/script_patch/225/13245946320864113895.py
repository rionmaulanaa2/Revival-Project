# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivitySpringSign.py
from __future__ import absolute_import
from logic.gutils import template_utils
from logic.gutils import task_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
import logic.gcommon.const as gconst
from logic.gutils import item_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.comsys.activity.ActivityTemplate import ActivityBase
import cc
BTN_NORMAL = 'gui/ui_res_2/activity/activity_202101/activity_eight_sign/pnl_springlog_gift_02.png'
BTN_SELECT = 'gui/ui_res_2/activity/activity_202101/activity_eight_sign/pnl_springlog_gift_01.png'
BTN_DISABLE = 'gui/ui_res_2/activity/activity_202101/activity_eight_sign/pnl_springlog_gift_03.png'
BOX_NORMAL = 'gui/ui_res_2/activity/activity_202101/activity_eight_sign/btn_get4.png'
BOX_SELECT = 'gui/ui_res_2/activity/activity_202101/activity_eight_sign/btn_get3.png'
BOX_DISABLE = 'gui/ui_res_2/activity/activity_202101/activity_eight_sign/btn_get5.png'

def can_receive_reward():
    from logic.gcommon.common_const.activity_const import ACTIVITY_SPRING_SIGN
    conf = confmgr.get('c_activity_config', ACTIVITY_SPRING_SIGN)
    task_list = activity_utils.parse_task_list(conf['cTask'])
    if len(task_list) <= 0:
        return False
    parent_task_id = int(task_list[0])
    children_tasks = task_utils.get_children_task(parent_task_id)
    count = len(children_tasks)
    received_count = 0
    for i, task_id in enumerate(children_tasks):
        receive_state = global_data.player.get_task_reward_status(task_id)
        if receive_state == ITEM_RECEIVED:
            received_count += 1
        elif receive_state == ITEM_UNRECEIVED:
            return True

    receive_state = global_data.player.get_task_reward_status(parent_task_id)
    if received_count >= count and receive_state != ITEM_RECEIVED:
        return True
    return False


class SpringSignBase(object):

    def __init__(self, *args, **kwargs):
        self._panel_alone = True

    def _init_panel(self):
        self._parent_task_id = 0
        self._children_tasks = []
        self.process_event(True)
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_title_down.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        import logic.gcommon.time_utility as tutil
        start_date = tutil.get_date_str('%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%m.%d', conf.get('cEndTime', 0), ignore_second=21600)
        self.panel.lab_sub_title.SetString('{}-{}'.format(start_date, finish_date))
        self.show_rewards()
        self.panel.PlayAnimation('show')

    def _finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.refresh_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_rewards(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self._parent_task_id = int(task_list[0])
        task_list = task_utils.get_children_task(self._parent_task_id)
        self._children_tasks = task_list
        count = len(task_list)
        list_items = self.panel.list_content
        list_items.DeleteAllSubItem()
        list_items.SetInitCount(count)
        for i, task_id in enumerate(task_list):
            item_widget = list_items.GetItem(i)
            reward_id = task_utils.get_task_reward(task_id)
            item_no, item_cnt = confmgr.get('common_reward_data', str(reward_id), 'reward_list')[0]
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            item_widget.img_item.SetDisplayFrameByPath('', pic_path)
            if item_cnt > 1:
                item_widget.lab_num.setVisible(True)
                item_widget.lab_num.SetString('x' + str(item_cnt))
            else:
                item_widget.lab_num.setVisible(False)
            item_widget.lab_day.SetString(get_text_by_id(604004, [i + 1]))
            name = item_utils.get_lobby_item_name(item_no)
            item_widget.lab_name.SetString(name)

        self.refresh_list(show_anim=True)

    def refresh_list(self, *args, **kwarg):
        if not self._parent_task_id:
            return
        else:
            global_data.player.read_activity_list(self._activity_type)
            show_anim = kwarg.get('show_anim', False)
            activity_type = self._activity_type
            conf = confmgr.get('c_activity_config', activity_type)
            act_name_id = conf['cNameTextID']
            count = len(self._children_tasks)
            cur_day = global_data.player.get_task_prog(self._parent_task_id)
            received_count = 0
            can_receive_list = []
            list_items = self.panel.list_content
            for i, task_id in enumerate(self._children_tasks):
                item_widget = list_items.GetItem(i)
                reward_id = task_utils.get_task_reward(task_id)
                item_no, item_cnt = confmgr.get('common_reward_data', str(reward_id), 'reward_list')[0]
                item_widget.lab_name.setOpacity(255)
                item_widget.img_get.setVisible(False)
                can_receive = False
                receive_state = global_data.player.get_task_reward_status(task_id)
                if receive_state == ITEM_RECEIVED:
                    received_count += 1
                    item_widget.img_get.setVisible(True)
                    item_widget.btn_item.SetFrames('', [BTN_DISABLE, BTN_DISABLE, BTN_DISABLE], False, None)
                    item_widget.lab_day.SetColor(1581368)
                    item_widget.lab_num.SetColor(1581368)
                    item_widget.lab_name.SetColor(5120805)
                    item_widget.lab_name.setOpacity(150)
                elif receive_state == ITEM_UNRECEIVED:
                    can_receive = True
                    can_receive_list.append(task_id)
                    item_widget.btn_item.SetFrames('', [BTN_SELECT, BTN_SELECT, BTN_SELECT], False, None)
                    item_widget.lab_day.SetColor(16742704)
                    item_widget.lab_num.SetColor(16742704)
                    item_widget.lab_name.SetColor(16772800)
                else:
                    item_widget.btn_item.SetFrames('', [BTN_NORMAL, BTN_NORMAL, BTN_NORMAL], False, None)
                    item_widget.lab_day.SetColor(14636368)
                    item_widget.lab_num.SetColor(14636368)
                    item_widget.lab_name.SetColor(5120805)
                if show_anim:

                    def callback(_item_widget=item_widget):
                        _item_widget.PlayAnimation('show1')

                    item_widget.SetTimeOut(0.09 * i, callback)
                if can_receive:

                    @item_widget.btn_item.unique_callback()
                    def OnClick(btn, touch, _task_id=task_id, _can_receive=can_receive):
                        if _can_receive:
                            global_data.player.receive_task_reward(_task_id)

                else:

                    @item_widget.btn_item.callback()
                    def OnClick(layer, touch, item_no=item_no):
                        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=touch.getLocation())
                        return

            @self.panel.btn_get_more.btn_common.unique_callback()
            def OnClick(btn, touch):
                if can_receive_list:
                    for _task_id in can_receive_list:
                        global_data.player.receive_task_reward(_task_id)

            if can_receive_list:
                enalbe = True if 1 else False
                self.panel.btn_get_more.btn_common.SetEnable(enalbe)
                if enalbe:
                    self.panel.btn_get_more.btn_common.SetText(80906)
                else:
                    self.panel.btn_get_more.btn_common.SetText(604010)
                self.panel.prog_top.SetPercent(float(received_count) / count * 100)
                receive_state = global_data.player.get_task_reward_status(self._parent_task_id)

                def extra_gift():
                    if received_count >= count and receive_state != ITEM_RECEIVED:
                        global_data.player.receive_task_reward(str(self._parent_task_id))
                    else:
                        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                        dlg.set_show_rule(601167, 500320)
                        x, y = self.panel.btn_gift.GetPosition()
                        wpos = self.panel.btn_gift.GetParent().ConvertToWorldSpace(x, y)
                        dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                        template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

                @self.panel.btn_gift.unique_callback()
                def OnClick(btn, touch):
                    extra_gift()

                @self.panel.btn_box.unique_callback()
                def OnClick(btn, touch):
                    extra_gift()

                self.panel.btn_box.SetText(601167)
                self.panel.StopAnimation('box_loop')
                self.panel.img_box.SetColor('#SW')
                self.panel.img_light.setVisible(False)
                self.panel.img_box_get.setVisible(False)
                if receive_state == ITEM_RECEIVED:
                    self.panel.img_box.SetColor('#BD')
                    self.panel.img_box_get.setVisible(True)
                    self.panel.btn_box.SetFrames('', [BOX_DISABLE, BOX_DISABLE, BOX_DISABLE], False, None)
                    self.panel.btn_box.SetEnable(False)
                elif received_count >= count:
                    self.panel.btn_box.SetText(80930)
                    self.panel.PlayAnimation('box_loop')
                    self.panel.btn_box.SetFrames('', [BOX_NORMAL, BOX_NORMAL, BOX_NORMAL], False, None)
                else:
                    self.panel.btn_box.SetFrames('', [BOX_NORMAL, BOX_NORMAL, BOX_NORMAL], False, None)
                show_anim or global_data.player.read_activity_list(self._activity_type)
            return


class ActivitySpringSign(ActivityBase, SpringSignBase):

    def on_init_panel(self):
        self._panel_alone = False
        self._init_panel()

    def on_finalize_panel(self):
        self._finalize_panel()