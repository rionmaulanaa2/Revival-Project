# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivityTenBenefits.py
from __future__ import absolute_import
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
import logic.gcommon.time_utility as tutil
from common.cfg import confmgr
import logic.gcommon.const as gconst
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import jump_to_ui_utils
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.comsys.activity.ActivityTemplate import ActivityBase
BAR_BEFORE = 'gui/ui_res_2/activity/activity_202101/ten_benefits/img_springgift_redbag_03.png'
BAR_AFTER = 'gui/ui_res_2/activity/activity_202101/ten_benefits/img_springgift_redbag_01.png'
BAR_TITLE_BEFORE = 'gui/ui_res_2/activity/activity_202101/ten_benefits/img_springgift_redbag_04.png'
BAR_TITLE_AFTER = 'gui/ui_res_2/activity/activity_202101/ten_benefits/img_springgift_redbag_02.png'
NA_ACTIVITIES = [
 10106, 10110, 10112, 10105, 10104, 10101, 10115, 10108]
CH_ACTIVITIES = [10106, 10111, 10117, 10112, 10105, 10114, 10104, 10101, 10115, 10108]

def goto_free_ticket--- This code section failed: ---

  26       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('MODE_SPECIAL',)
           6  IMPORT_NAME           0  'logic.client.const.mall_const'
           9  IMPORT_FROM           1  'MODE_SPECIAL'
          12  STORE_FAST            0  'MODE_SPECIAL'
          15  POP_TOP          

  27      16  LOAD_GLOBAL           2  'G_IS_NA_PROJECT'
          19  POP_JUMP_IF_TRUE     41  'to 41'

  28      22  LOAD_GLOBAL           3  'jump_to_ui_utils'
          25  LOAD_ATTR             4  'jump_to_lottery'
          28  LOAD_CONST            3  'lottery_id'
          31  LOAD_FAST             0  'MODE_SPECIAL'
          34  CALL_FUNCTION_256   256 
          37  POP_TOP          
          38  JUMP_FORWARD         19  'to 60'

  30      41  LOAD_GLOBAL           3  'jump_to_ui_utils'
          44  LOAD_ATTR             4  'jump_to_lottery'
          47  LOAD_CONST            3  'lottery_id'
          50  LOAD_CONST            4  'show_model_id'
          53  LOAD_CONST            5  201001148
          56  CALL_FUNCTION_512   512 
          59  POP_TOP          
        60_0  COME_FROM                '38'

Parse error at or near `CALL_FUNCTION_512' instruction at offset 56


def goto_spring_ticket():
    from logic.client.const.mall_const import MODE_SPRING_FESTIVAL_2021
    jump_to_ui_utils.jump_to_lottery(lottery_id=MODE_SPRING_FESTIVAL_2021)


def can_show_open_ui():
    if G_IS_NA_PROJECTC:
        activities = NA_ACTIVITIES
    else:
        activities = CH_ACTIVITIES
    now = tutil.get_server_time()
    shown_activities = global_data.achi_mgr.get_cur_user_archive_data('spring_ten_benefits_shown_acts', default=[])
    open_activities = []
    for i, a_id in enumerate(activities):
        conf = confmgr.get('c_activity_config', str(a_id), default=None)
        if not conf:
            continue
        begin_time = conf.get('cBeginTime', 0)
        end_time = conf.get('cEndTime', 0)
        if begin_time == 0:
            task_id = conf.get('cTask', '')
            if task_id:
                task_conf = task_utils.get_task_conf_by_id(task_id)
                begin_time = task_conf.get('start_time', 0)
                end_time = task_conf.get('end_time', 0)
        if begin_time <= now <= end_time:
            open_activities.append(a_id)

    new_list = list(set(open_activities) - set(shown_activities))
    if new_list:
        shown_activities.extend(new_list)
        global_data.achi_mgr.set_cur_user_archive_data('spring_ten_benefits_shown_acts', shown_activities)
        return True
    else:
        return False


class TenBenefitsBase(object):

    def __init__(self, *args, **kwargs):
        self._panel_alone = True

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.refresh_share
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _finalize_panel(self):
        self.process_event(False)

    def _on_resolution_changed(self):
        self._root_panel.PlayAnimation('show')

    def _init_panel(self, root_panel=None):
        if not root_panel:
            self._root_panel = self.panel
        else:
            self._root_panel = root_panel
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self._share_task_id = '1411371'
        self._specail_jump = {}
        if G_IS_NA_PROJECT:
            self._root_panel.img_title.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/activity_2021_spring_festival/txt_eight_benefits.png')
            self._root_panel.img_title_01.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/activity_2021_spring_festival/txt_eight_benefits.png')
            self._activities = NA_ACTIVITIES
            self._activitie_text = [601205, 601212, 601208, 601209, 601211, 601101, 606321, 601107]
            self._specail_jump[1] = goto_free_ticket
            self._specail_jump[6] = goto_spring_ticket
        else:
            self._activities = CH_ACTIVITIES
            self._activitie_text = [601205, 601210, 601207, 601208, 601209, 601206, 601211, 601101, 606321, 601107]
            self._specail_jump[8] = goto_spring_ticket
        cur_date = tutil.get_date_str('%m.%d', tutil.get_server_time())
        self._root_panel.lab_time_num.SetString(cur_date)
        self._screen_capture_helper = None
        self.show_activities(do_init=True)

        @self._root_panel.btn_share.unique_callback()
        def OnClick(btn, touch):
            self._on_click_btn_share()

        self._root_panel.PlayAnimation('show')
        self.refresh_share()
        self.process_event(True)
        return

    def refresh_share(self, *args, **kwarg):

        @self._root_panel.btn_gift.unique_callback()
        def OnClick(btn, touch):
            reward_id = task_utils.get_task_reward(self._share_task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            item_no, item_num = reward_list[0]
            global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=touch.getLocation())
            return

        enable = not global_data.player.has_receive_reward(self._share_task_id)
        if enable:
            self._root_panel.img_gift.setOpacity(255)
            self._root_panel.img_gift.SetColor('#SW')
        else:
            self._root_panel.img_gift.setOpacity(200)
            self._root_panel.img_gift.SetColor(10976391)
        self._root_panel.img_tick.setVisible(not enable)
        if global_data.player.has_unreceived_task_reward(self._share_task_id):
            global_data.player.receive_task_reward(self._share_task_id)

    def show_activities(self, now=None, do_init=False):
        nd_list = self._root_panel.nd_list
        if now == None:
            now = tutil.get_server_time()
        for i, a_id in enumerate(self._activities):
            item_widget = getattr(nd_list, 'temp_{}'.format(i + 1))
            conf = confmgr.get('c_activity_config', str(a_id), default=None)
            if not conf:
                item_widget.setVisible(False)
                continue
            item_widget.lab_content.SetString(self._activitie_text[i])
            begin_time = conf.get('cBeginTime', 0)
            end_time = conf.get('cEndTime', 0)
            if begin_time == 0:
                task_id = conf.get('cTask', '')
                if task_id:
                    task_conf = task_utils.get_task_conf_by_id(task_id)
                    begin_time = task_conf.get('start_time', 0)
                    end_time = task_conf.get('end_time', 0)
            if now > end_time:
                item_widget.lab_end.setVisible(True)
                item_widget.img_mask.setVisible(True)
                item_widget.btn_bar_title.SetText('')
                item_widget.lab_content.SetColor(0)
            else:
                item_widget.lab_end.setVisible(False)
                item_widget.img_mask.setVisible(False)
                item_widget.lab_content.SetColor(8728866)
                start_date = tutil.get_date_str('%m.%d', begin_time)
                finish_date = tutil.get_date_str('%m.%d', end_time, ignore_second=18000)
                item_widget.btn_bar_title.SetText('{}-{}'.format(start_date, finish_date))
            opened = begin_time <= now <= end_time
            if opened:
                item_widget.btn_bar.SetFrames('', [BAR_AFTER, BAR_AFTER, BAR_AFTER], False, None)
                item_widget.btn_bar_title.SetTextColor(color1=14111571, color2=14111571, color3=14111571)
                item_widget.btn_bar_title.SetFrames('', [BAR_TITLE_AFTER, BAR_TITLE_AFTER, BAR_TITLE_AFTER], False, None)
                item_widget.img_tips.setVisible(True)
            else:
                item_widget.btn_bar.SetFrames('', [BAR_BEFORE, BAR_BEFORE, BAR_BEFORE], False, None)
                item_widget.btn_bar_title.SetTextColor(color1=16311524, color2=16311524, color3=16311524)
                item_widget.btn_bar_title.SetFrames('', [BAR_TITLE_BEFORE, BAR_TITLE_BEFORE, BAR_TITLE_BEFORE], False, None)
                item_widget.img_tips.setVisible(False)

            @item_widget.btn_bar.callback()
            def OnClick(layer, touch, _a_id=a_id, _index=i, _opened=opened, _begin_time=begin_time, _now=now, _end_time=end_time):
                if _opened:
                    if self._panel_alone:
                        self.close()
                    if _index in self._specail_jump:
                        self._specail_jump[_index]()
                        return
                    jump_to_ui_utils.jump_to_activity(str(_a_id))
                elif _now > _end_time:
                    global_data.game_mgr.show_tip(81796)
                else:
                    global_data.game_mgr.show_tip(601222)

            def callback(_item_widget=item_widget, _opened=opened):
                _item_widget.setVisible(True)
                if _opened:
                    _item_widget.PlayAnimation('openable')
                else:
                    _item_widget.PlayAnimation('show')

            if do_init:
                item_widget.setVisible(False)
                if G_IS_NA_PROJECT:
                    item_widget.SetTimeOut(0.03 * (i % 4), callback)
                else:
                    item_widget.SetTimeOut(0.03 * (i % 5), callback)

        return

    def _on_click_btn_share(self):
        if not global_data.video_player.is_in_init_state():
            global_data.game_mgr.show_tip(get_text_by_id(82150))
            return
        if not self._screen_capture_helper:
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            from logic.comsys.share.SpringBenefitsShareCreator import SpringBenefitsShareCreator
            self._screen_capture_helper = ScreenFrameHelper()
            share_creator = SpringBenefitsShareCreator()
            share_creator.create()
            share_content = share_creator
            self._screen_capture_helper.set_custom_share_content(share_content)
        if self._screen_capture_helper:

            def share_inform_func():
                if global_data.player:
                    global_data.player.share_activity('activity_10109')

            def custom_cb(*args):
                self._root_panel.btn_share.setVisible(True)
                if not self._panel_alone:
                    self._root_panel.nd_content.SetPosition('50%0', '50%0')
                    self._root_panel.GetParent().GetParent().temp_btn_close.setVisible(True)
                self.show_activities()
                global_data.emgr.show_activity_tab_list.emit(True)

            self._root_panel.btn_share.setVisible(False)
            if not self._panel_alone:
                self._root_panel.nd_content.SetPosition('50%-108', '50%0')
                self._root_panel.GetParent().GetParent().temp_btn_close.setVisible(False)
            self.show_activities(now=-1)
            global_data.emgr.show_activity_tab_list.emit(False)
            if not self._panel_alone:
                self._screen_capture_helper.take_screen_shot(['ActivitySpringFestivalMainUI'], self._root_panel, custom_cb=custom_cb, share_inform_func=share_inform_func, head_nd_name='nd_player_info_1')
            else:
                self._screen_capture_helper.take_screen_shot(['TenBenefitsUI'], self._root_panel, custom_cb=custom_cb, share_inform_func=share_inform_func, head_nd_name='nd_player_info_1')


class ActivityTenBenefits(ActivityBase, TenBenefitsBase):

    def on_init_panel(self):
        self._panel_alone = False
        self._init_panel()

    def on_finalize_panel(self):
        self._finalize_panel()

    def on_resolution_changed(self):
        self._on_resolution_changed()

    @staticmethod
    def get_custom_template_info():
        if G_IS_NA_PROJECT:
            return {'nd_list': {'ccbFile': 'activity/activity_202101/i_activity_ten_benefits_item_overseas'}}
        else:
            return None