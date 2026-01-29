# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivitySpringFestivalCollect.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.comsys.archive.archive_manager import ArchiveManager

class ActivitySpringFestivalCollect(ActivityBase):
    ITEM_IMG_CFG = {201801141: [
                 1, 'fengmolong', 431141, 601177],
       201001148: [
                 2, 'img_ning', 441148, 601178],
       201001547: [
                 3, 'img_mila', 441547, 601177],
       201800543: [
                 4, 'img_xiaoxiong', 430543, 601177]
       }

    def __init__(self, dlg, activity_type):
        super(ActivitySpringFestivalCollect, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.panel = None
        self.process_event(False)
        return

    def init_parameters(self):
        self.collect_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default=None)
        self.task_conf = task_utils.get_task_conf_by_id(self.collect_task_id)
        self.prog_rewards = self.task_conf.get('prog_rewards', [])
        self.total_prog = task_utils.get_total_prog(self.collect_task_id)
        return

    def loop_anim(self):
        if self.panel:
            self.panel.PlayAnimation('loop_03')

    def on_init_panel(self):
        self.panel.DelayCall(1.5, self.loop_anim)

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            player.receive_all_task_prog_reward(self.collect_task_id)

        @self.panel.btn_help.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(81753), get_text_by_id(int(desc_id)))

        if not self.update_skin(True):
            self.panel.PlayAnimation('show')

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.receive_task_prog_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def receive_task_prog_reward(self, task_id, prog):
        if task_id != self.collect_task_id:
            return
        self.update_skin()
        global_data.emgr.refresh_activity_redpoint.emit()

    def on_task_updated(self, task_id, *args):
        if task_id != self.collect_task_id:
            return
        self.update_skin()
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_skin(self, is_init=False):
        activation_anim_played = False
        current_collections = ArchiveManager().get_cur_user_archive_data('collections_spring_2021', [])
        collections = global_data.player.get_task_content(self.collect_task_id, 'collections', [])
        for item_no, cfg in six.iteritems(self.ITEM_IMG_CFG):
            item_nd = getattr(self.panel, 'temp_pic_{}'.format(cfg[0]))
            item_name_nd = getattr(self.panel, 'temp_name_{}'.format(cfg[0]))

            def f(item_no, cfg):

                def g():
                    return (
                     item_no, cfg)

                return g

            def set_icon_visible(info=f(item_no, cfg)):
                if not self.panel:
                    return
                item_no, cfg = info()
                item_nd = getattr(self.panel, 'temp_pic_{}'.format(cfg[0]))
                item_name_nd = getattr(self.panel, 'temp_name_{}'.format(cfg[0]))
                item_nd.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202101/lottery/center/{}1.png'.format(cfg[1]))
                item_name_nd.setVisible(False)
                if item_no == 201800543:
                    item_nd.img_fire.setVisible(True)

            if item_no in collections:
                if item_no not in current_collections:
                    self.panel.PlayAnimation('activation_0{}'.format(cfg[0]))
                    item_nd.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202101/lottery/center/{}2.png'.format(cfg[1]))
                    self.panel.DelayCall(0.5, set_icon_visible)
                    current_collections.append(item_no)
                    ArchiveManager().set_cur_user_archive_data('collections_spring_2021', current_collections)
                    activation_anim_played = True
                else:
                    set_icon_visible()
            else:
                item_nd.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202101/lottery/center/{}2.png'.format(cfg[1]))
                item_name_nd.setVisible(True)
            item_name_nd.btn_detail.item_no = item_no
            item_name_nd.lab_skin.SetString(get_text_by_id(cfg[2]))
            item_name_nd.lab_way.SetString(get_text_by_id(cfg[3]))

            @item_name_nd.btn_detail.unique_callback()
            def OnClick(btn, touch):
                from logic.gutils import jump_to_ui_utils
                jump_to_ui_utils.jump_to_display_detail_by_item_no(btn.item_no, {})
                return True

        task_cur_prog = global_data.player.get_task_prog(self.collect_task_id)
        progress_node = self.panel.progress_bar
        percent = (task_cur_prog - 1) * 100.0 / (self.total_prog - 1)
        percent = 0 if percent < 0 else percent
        if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
            progress_node.SetPercentage(percent)
        else:
            progress_node.SetPercent(percent)
        self.panel.lab_stage.SetString('%s\xef\xbc\x9a%d/%d' % (get_text_by_id(601197), task_cur_prog, self.total_prog))
        is_receivable_result = False
        for i, prog_reward in enumerate(self.prog_rewards):
            prog, reward_id = prog_reward
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if not reward_list:
                continue
            nd_item = getattr(self.panel, 'item%d' % (i + 1))
            is_receivable = False
            show_tips = True
            has_receive = global_data.player.has_receive_prog_reward(self.collect_task_id, prog)
            nd_item.btn.UnBindMethod('OnClick')
            if has_receive:
                pass
            elif global_data.player.is_prog_reward_receivable(self.collect_task_id, prog):
                is_receivable = True
                show_tips = False
                nd_item.btn.BindMethod('OnClick', lambda b, t, tid=self.collect_task_id, prog=prog: global_data.player.receive_task_prog_reward(tid, prog))
            reward_info = reward_list[0]
            item_no, item_num = reward_info[0], reward_info[1]
            template_utils.init_tempate_mall_i_item(nd_item, item_no, item_num=item_num, show_rare_degree=True, show_tips=show_tips)
            nd_item.nd_get.setVisible(has_receive)
            nd_item.nd_get.img_get_bar.setVisible(has_receive)
            nd_item.nd_get_tips.setVisible(is_receivable)
            if is_receivable:
                nd_item.PlayAnimation('get_tips')
            else:
                nd_item.StopAnimation('get_tips')
            is_receivable_result = is_receivable_result or is_receivable

        self.panel.btn_get.SetEnable(is_receivable_result)
        self.panel.btn_get.img_btn_light.setVisible(is_receivable_result)
        self.panel.btn_get.vx_btn.setVisible(is_receivable_result)
        return activation_anim_played