# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/CertificateMainUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gcommon.const import NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE, NEWBIE_STAGE_THIRD_BATTLE, NEWBIE_STAGE_FOURTH_BATTLE
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED
from common.utils import ui_path_utils
ND_TAG_MAX_LOCAL_Z_ORDER = 4

class CertificateMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_main_all'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = ui_const.UI_VKB_CLOSE
    PASS_BEFORE = False
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close',
       'nd_reward_all.btn_get.OnClick': 'on_click_get_all',
       'btn_share.OnClick': 'on_click_share_btn'
       }
    DELAY_LOOP_TAG = 31415926
    CARD_UNFINISH_DELAY_LOOP_TAG = 31415926
    CARD_PASS_DELAY_BTN_GET_TAG = 31415926

    def on_init_panel(self, *args):
        self._share_content = None
        self._parent_task_id = global_data.player.get_newbie_parent_task_id()
        self.open_bg(True)
        self.init_mode_tab_bkg_img()
        self.init_task_data()
        self.init_cur_idx()
        self.update_tag_content()
        self.bind_event(True)
        self.check_enter_first()
        self.init_final_reward_widget()
        self.panel.RecordAnimationNodeState('ultimate_btnloop')
        node = self.panel
        delay = node.GetAnimationMaxRunTime('show')
        node.PlayAnimation('show')

        def cb():
            node.PlayAnimation('loop')

        node.DelayCallWithTag(delay, cb, self.DELAY_LOOP_TAG)
        return

    def on_finalize_panel(self):
        self.destroy_widget('_share_content')
        self.bind_event(False)
        self.open_bg(False)
        self._nd_tag_list = []

    def bind_event(self, is_bind):
        event_conf = {'receive_task_reward_succ_event': self.update_tag_content,
           'task_prog_changed': self.update_tag_content
           }
        if is_bind:
            global_data.emgr.bind_events(event_conf)
        else:
            global_data.emgr.unbind_events(event_conf)

    def init_task_data(self):
        task_list = task_utils.get_children_task(self._parent_task_id)
        self._child_task_list = []
        self._nd_tag_list = []
        for i in range(4):
            nd = getattr(self.panel, 'mode_' + str(i + 1), None)
            if nd:
                if i >= len(task_list):
                    nd.setVisible(False)
                    continue
                self._child_task_list.append(task_list[i])
                self._nd_tag_list.append(nd)

        return

    def init_final_reward_widget(self):
        init_common_reward_list(self.panel.nd_reward_all.nd_reward, task_utils.get_task_reward(self._parent_task_id))
        self.update_final_reward_btn()

    def init_mode_tab_bkg_img(self):
        self.img_map = []
        self.img_unfinish_bkg = []
        task_list = task_utils.get_children_task(self._parent_task_id)
        for idx, task_id in enumerate(task_list):
            nd = getattr(self.panel, 'mode_' + str(idx + 1), None)
            if not nd:
                continue
            task_args = task_utils.get_task_arg(task_id)
            btn_frames = task_args.get('btn_frames', [])
            if not btn_frames:
                continue
            nd.btn_battle.SetFrames('', btn_frames, False, None)

        for idx, task_id in enumerate(task_list):
            task_args = task_utils.get_task_arg(task_id)
            img_card_path = task_args.get('img_card', ui_path_utils.AUDITION_CERTIFICATE_PRIMARY_PATH)
            img_unfinish_path = task_args.get('img_unfinish', ui_path_utils.AUDITION_AWARD_PRIMARY_PATH)
            self.img_map.append(img_card_path)
            self.img_unfinish_bkg.append(img_unfinish_path)

        return

    def update_final_reward_btn(self):
        can_reveive = global_data.player.is_task_reward_receivable(self._parent_task_id)
        is_finish = global_data.player.is_task_finished(self._parent_task_id)
        self.panel.nd_reward_all.btn_get.SetEnable(can_reveive)
        if can_reveive:
            self.panel.PlayAnimation('ultimate_btnloop')
        else:
            self.panel.StopAnimation('ultimate_btnloop')
            self.panel.RecoverAnimationNodeState('ultimate_btnloop')
        self.panel.nd_reward_all.lab_get_all.setVisible(can_reveive and is_finish)
        self.panel.nd_reward_all.lab_got_all.setVisible(not can_reveive and is_finish)
        self.panel.nd_reward_all.lab_unfinish_all.setVisible(not can_reveive and not is_finish)
        all_items = self.panel.nd_reward.GetAllItem()
        reward_status = global_data.player.get_task_reward_status(self._parent_task_id)
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def init_cur_idx(self):
        self._cur_idx = len(self._child_task_list) - 1
        for i, task_id in enumerate(self._child_task_list):
            if global_data.player.is_task_finished(task_id) and not global_data.player.has_receive_reward(task_id):
                self._cur_idx = i
                return

        for i, task_id in enumerate(self._child_task_list):
            if not global_data.player.is_task_finished(task_id):
                self._cur_idx = i
                return

    def update_tag_content(self, *args):
        for i in range(len(self._child_task_list)):
            task_id = self._child_task_list[i]
            nd_tag = self._nd_tag_list[i]
            task_name_id = confmgr.get('task/task_data', task_id, 'name')
            nd_tag.lab_mode.SetString(task_name_id)
            is_finish = global_data.player.is_task_finished(task_id)
            nd_tag.img_finish.setVisible(bool(is_finish))
            nd_tag.btn_battle.BindMethod('OnClick', lambda b, t, idx=i: self.select_tag(idx))
            if is_finish:
                show_red_point = not global_data.player.has_receive_reward(task_id) if 1 else False
                nd_tag.temp_red.setVisible(show_red_point)

        self.select_tag(self._cur_idx, True)
        self.update_final_reward_btn()

    def select_tag(self, selected_idx, force=False):
        if selected_idx == self._cur_idx and not force:
            return
        self._cur_idx = selected_idx
        for i, nd_tag in enumerate(self._nd_tag_list):
            if not hasattr(nd_tag, '_mark_ani_recover') or not nd_tag._mark_ani_recover:
                nd_tag.RecordAnimationNodeState('choose')
                nd_tag._mark_ani_recover = True
            is_selected = i == self._cur_idx
            if is_selected:
                nd_tag.setLocalZOrder(ND_TAG_MAX_LOCAL_Z_ORDER)
            else:
                order_i = ND_TAG_MAX_LOCAL_Z_ORDER - (i - self._cur_idx + 4) % 4
                nd_tag.setLocalZOrder(order_i)
            nd_tag.btn_battle.SetSelect(is_selected)
            TAB_CHOOSE_DELAY_TAG = 31415926
            if is_selected:
                nd_tag.PlayAnimation('choose')
                t = nd_tag.GetAnimationMaxRunTime('choose')

                def cb(nd_tag=nd_tag):
                    nd_tag.PlayAnimation('choose_loop')

                nd_tag.DelayCallWithTag(t, cb, TAB_CHOOSE_DELAY_TAG)
            else:
                nd_tag.StopAnimation('choose')
                nd_tag.StopAnimation('choose_loop')
                nd_tag.stopActionByTag(TAB_CHOOSE_DELAY_TAG)
                nd_tag.RecoverAnimationNodeState('choose')

        self.update_pass_certificate()
        self.update_unfinish_certificate()
        if self._cur_idx != 0:
            global_data.emgr.certificate_ui_select_tag_event.emit(self._cur_idx)
        else:
            record = global_data.achi_mgr.get_cur_user_archive_data('show_CertificateMainUI', default=0) == 1
            if record:
                global_data.emgr.certificate_ui_select_tag_event.emit(self._cur_idx)

    def update_pass_certificate(self):
        task_id = self._child_task_list[self._cur_idx]
        nd_card = self.panel.card_pass
        if not global_data.player or not global_data.player.is_task_finished(task_id):
            nd_card.setVisible(False)
            nd_card.StopAnimation('get_btnloop')
            self.panel.btn_share.setVisible(False)
            return
        from logic.gutils.new_template_utils import update_newbee_pass_certificate
        update_newbee_pass_certificate(nd_card, task_id, self.img_map[self._cur_idx])
        nd_card.setVisible(True)
        self.panel.btn_share.setVisible(True and global_data.is_share_show)
        is_receive = bool(global_data.player.has_receive_reward(task_id))
        nd_card.btn_get.setVisible(not is_receive)
        if not is_receive:
            nd_card.PlayAnimation('get_btnloop')
        else:
            nd_card.StopAnimation('get_btnloop')
        nd_card.btn_review.setVisible(is_receive)
        nd_card.btn_review.BindMethod('OnClick', lambda b, t, tid=task_id: self.enter_assessment(tid, True))
        nd_card.btn_get.BindMethod('OnClick', lambda b, t, tid=task_id: self._on_card_pass_btn_get_clicked(b, t, tid))
        self.set_reward_data(nd_card.temp_reward, task_id, is_receive)

    def _on_card_pass_btn_get_clicked(self, b, t, tid):
        nd_card = self.panel.card_pass
        if nd_card.IsPlayingAnimation('get_btnclick'):
            return
        delay = nd_card.GetAnimationMaxRunTime('get_btnclick')
        nd_card.PlayAnimation('get_btnclick')

        def cb():
            if not global_data.player:
                return
            global_data.player.receive_task_reward(tid)
            if self._cur_idx < len(self._child_task_list) - 1:
                self.select_tag(self._cur_idx + 1)

        nd_card.DelayCallWithTag(delay, cb, self.CARD_PASS_DELAY_BTN_GET_TAG)

    def update_unfinish_certificate(self):
        if not global_data.player:
            return
        task_id = self._child_task_list[self._cur_idx]
        nd_card = self.panel.card_unfinish
        if global_data.player.is_task_finished(task_id):
            nd_card.setVisible(False)
            nd_card.StopAnimation('begin_btnloop')
            return
        nd_card.setVisible(True)
        task_data = confmgr.get('task/task_data', task_id)
        nd_card.lab_title_mode.SetString(task_data['name'])
        nd_card.lab_describe.SetString(task_data['desc'])
        nd_card.img_card.SetDisplayFrameByPath('', self.img_map[self._cur_idx])
        nd_card.StopAnimation('begin_btnloop')
        delay = nd_card.GetAnimationMaxRunTime('show')
        nd_card.PlayAnimation('show')

        def cb():
            nd_card.PlayAnimation('begin_btnloop')

        nd_card.DelayCallWithTag(delay, cb, self.CARD_UNFINISH_DELAY_LOOP_TAG)
        nd_card.btn_start.BindMethod('OnClick', lambda b, t, tid=task_id: self._on_card_unfinish_btn_start_click(b, t, tid))
        nd_card.nd_reward_unfinish.img_title_reward_unifinish.SetDisplayFrameByPath('', self.img_unfinish_bkg[self._cur_idx])
        self.set_reward_data(nd_card.temp_reward, task_id, False)

    def set_reward_data(self, nd, task_id, isget):
        from logic.gutils.new_template_utils import set_certificate_reward_data
        set_certificate_reward_data(nd, task_id, isget)

    def update_all_content(self, *args):
        self.select_tag(self._cur_idx, True)

    def open_bg(self, flag):
        if flag:
            global_data.ui_mgr.show_ui('CertificateMainUIBg', 'logic.comsys.guide_ui')
        else:
            global_data.ui_mgr.close_ui('CertificateMainUIBg')

    def check_enter_first(self):
        for task_id in self._child_task_list:
            if global_data.player.is_task_finished(task_id):
                return

        record = global_data.achi_mgr.get_cur_user_archive_data('show_CertificateMainUI', default=0) == 1
        if record:
            return
        global_data.achi_mgr.set_cur_user_archive_data('show_CertificateMainUI', 1)
        ui = global_data.ui_mgr.show_ui('GuideTips', 'logic.comsys.guide_ui')
        ui and ui.set_content(5273)

    def _on_card_unfinish_btn_start_click(self, b, t, tid):
        self.panel.card_unfinish.PlayAnimation('begin_btnclick')
        self.enter_assessment(tid, False)

    def enter_assessment(self, tid, pass_before):
        args = task_utils.get_task_arg(tid)
        if not args:
            return
        battle_type = args.get('battle_type')
        if not battle_type:
            return
        if global_data.player:
            self.enter_local_battle(battle_type, tid)
            CertificateMainUI.PASS_BEFORE = pass_before

    def enter_local_battle(self, battle_type, tid):
        if battle_type in (NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE):
            global_data.player.clear_local_battle_data()
            if global_data.player.local_battle:
                global_data.player.local_battle.destroy()
                global_data.player.local_battle = None
            global_data.player.try_start_local_battle(battle_type)
            global_data.player.call_server_method('start_assessment_task', (tid,))
            global_data.player.set_assessment_tid(tid)
        elif battle_type in (NEWBIE_STAGE_THIRD_BATTLE, NEWBIE_STAGE_FOURTH_BATTLE):
            global_data.player.try_start_new_local_battle(battle_type)
            global_data.player.call_server_method('start_assessment_task', (tid,))
        return

    def close(self, *args):
        match_mode_ui = global_data.ui_mgr.get_ui('MatchMode')
        if not match_mode_ui and global_data.player:
            from logic.comsys.lobby.MatchMode import MatchMode
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
            MatchMode(None, play_type=PLAY_TYPE_CHICKEN)
        self.open_bg(False)
        super(CertificateMainUI, self).close(*args)
        return

    def on_click_get_all(self, *args):
        self.panel.PlayAnimation('ultimate_btnclick')
        global_data.player.receive_task_reward(self._parent_task_id)

    def pass_assessment(self):
        tid = None
        if 0 <= self._cur_idx < len(self._child_task_list):
            tid = self._child_task_list[self._cur_idx]
        if not tid:
            return
        else:
            if global_data.player.is_task_finished(tid) and not CertificateMainUI.PASS_BEFORE:
                self.panel.card_pass.PlayAnimation('seal')
            return

    def on_click_share_btn(self, btn, touch):
        from logic.comsys.share.TrainingCertificateShareCreator import TrainingCertificateShareCreator
        if not self._share_content:
            share_creator = TrainingCertificateShareCreator()
            share_creator.create(None)
            self._share_content = share_creator
        task_id = self._child_task_list[self._cur_idx]
        player_name = global_data.player.get_name()
        task_img = self.img_map[self._cur_idx]
        self._share_content.set_info(task_id, player_name, task_img)
        from logic.comsys.share.ShareUI import ShareUI
        ShareUI(parent=self.panel).set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)
        return

    def click_cur_get_reward_btn(self, *args):
        task_id = self._child_task_list[self._cur_idx]
        self._on_card_pass_btn_get_clicked(None, None, task_id)
        return

    def click_cur_start_battle_btn(self, *args):
        task_id = self._child_task_list[self._cur_idx]
        self._on_card_unfinish_btn_start_click(None, None, task_id)
        return

    def get_cur_task_status(self):
        if self._cur_idx is None or not self._child_task_list:
            return -1
        else:
            if self._cur_idx < 0 or self._cur_idx >= len(self._child_task_list):
                return -1
            task_id = self._child_task_list[self._cur_idx]
            if global_data.player:
                return global_data.player.get_task_reward_status(task_id)
            return -1

    def get_cur_task_id(self):
        return self._child_task_list[self._cur_idx]

    def is_third_stage_task(self, task_id):
        return self._child_task_list.index(task_id) == 2

    def get_cur_tag_idx(self):
        return self._cur_idx