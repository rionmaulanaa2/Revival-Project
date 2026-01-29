# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/ClanTaskWidget.py
from __future__ import absolute_import
from logic.comsys.clan.ClanTaskBase import ClanTaskBase

class ClanTaskWidget(ClanTaskBase):

    def __init__(self, parent, panel, task_type):
        super(ClanTaskWidget, self).__init__(parent, panel, task_type, False)
        temp_content = getattr(self.parent.nd_cut, 'temp_content')
        pos = temp_content.GetPosition()
        crew_task_temp = global_data.uisystem.load_template_create('task/i_crew_task_temp')
        self.nd_content = crew_task_temp.temp_task_crew
        self.panel.nd_cut.AddChild('clan_task', crew_task_temp)
        crew_task_temp.ResizeAndPosition()
        crew_task_temp.SetPosition(*pos)
        crew_task_temp.setAnchorPoint(temp_content.getAnchorPoint())
        self.on_init_panel()

    def _init_get_all(self):

        @self.nd_content.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            can_receive_task = self._get_all_receivable_tasks()
            for task_id in can_receive_task:
                global_data.player.receive_task_reward(task_id)

            can_receivable_lv_lst = self._get_week_receivable_lv()
            for lv in can_receivable_lv_lst:
                global_data.player.receive_week_clan_point_reward(lv)

    def _on_task_update(self, *args):
        can_receive_task = self._get_all_receivable_tasks()
        can_receivable_lv_lst = self._get_week_receivable_lv()
        can_receive = True if can_receive_task or can_receivable_lv_lst else False
        self.nd_content.temp_get_all.setVisible(can_receive)
        self.nd_content.pnl_get_all.setVisible(can_receive)

    @staticmethod
    def check_red_point():
        if not global_data.player:
            return False
        from logic.gutils import clan_utils
        task_ids = clan_utils.get_clan_task_ids()
        for task_id in task_ids:
            from logic.gcommon.item.item_const import ITEM_UNRECEIVED
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                return True

        return False