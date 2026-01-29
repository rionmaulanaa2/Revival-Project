# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS2Collect.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, item_utils, template_utils, red_point_utils, mecha_skin_utils, dress_utils, mall_utils
import logic.gcommon.item.lobby_item_type as lobby_item_type

class ActivityS2Collect(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityS2Collect, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.panel = None
        self.process_event(False)
        return

    def init_parameters(self):
        self.collect_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default=None)
        ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.ITEM_IMG_CFG = ui_data.get('item_img', {})
        self.task_conf = task_utils.get_task_conf_by_id(self.collect_task_id)
        self.prog_rewards = self.task_conf.get('prog_rewards', [])
        self.total_prog = task_utils.get_total_prog(self.collect_task_id)
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        return

    def on_init_panel(self):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            player.receive_all_task_prog_reward(self.collect_task_id)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        self.update_skin(True)

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

    def init_clothing_item(self, item_config, clothing_item, clothing_id, item_type):
        item_no = item_config.get('item_no')
        name_text = item_utils.get_lobby_item_name(item_no)
        clothing_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(clothing_item, clothing_id)
        if item_type == lobby_item_type.L_ITEM_TYPE_MECHA_SKIN or item_type == lobby_item_type.L_ITEM_TYPE_MECHA:
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id))
            if skin_cfg:
                item_utils.check_skin_tag(clothing_item.nd_kind, clothing_id)
                skin_half_imge_path = skin_cfg.get('half_img_path', None)
                if skin_half_imge_path != None:
                    clothing_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
        elif item_type == lobby_item_type.L_ITEM_TYPE_ROLE_SKIN or item_type == lobby_item_type.L_ITEM_TYPE_ROLE:
            img_role = mall_utils.get_half_pic_by_item_no(item_no)
            if img_role:
                clothing_item.img_skin.SetDisplayFrameByPath('', img_role)
        template_utils.show_remain_time(clothing_item.nd_time, clothing_item.nd_time.lab_time, clothing_id)
        show_new = False
        red_point_utils.show_red_point_template(clothing_item.nd_new, show_new)
        clothing_data = global_data.player.get_item_by_no(clothing_id)
        collections = global_data.player.get_task_content(self.collect_task_id, 'collections', [])
        if int(item_no) not in collections:
            clothing_item.nd_lock.setVisible(True)
        else:
            clothing_item.nd_lock.setVisible(False)
        return

    def update_skin(self, is_init=False):
        self.panel.list_card.SetInitCount(len(self.ITEM_IMG_CFG))
        for item_no, cfg in six.iteritems(self.ITEM_IMG_CFG):
            index = cfg[0]
            item_nd = self.panel.list_card.GetItem(index)
            clothing_id = int(item_no)
            item_config = confmgr.get('lobby_item', str(clothing_id))
            item_type = item_utils.get_lobby_item_type(item_no)
            lab_role_name = getattr(self.panel, 'lab_role_name' + str(index + 1))
            self.init_clothing_item(item_config, item_nd, clothing_id, item_type)
            name_text = item_utils.get_lobby_item_belong_name(item_no)
            lab_role_name.SetString(name_text)
            if is_init:
                item_nd.PlayAnimation('show_common')

        task_cur_prog = global_data.player.get_task_prog(self.collect_task_id)
        progress_node = self.panel.progress_bar
        percent = task_cur_prog * 100.0 / self.total_prog
        if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
            progress_node.SetPercentage(percent)
        else:
            progress_node.SetPercent(percent)
        self.panel.lab_stage.SetString(get_text_by_id(906593) + '%d/%d' % (task_cur_prog, self.total_prog))
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