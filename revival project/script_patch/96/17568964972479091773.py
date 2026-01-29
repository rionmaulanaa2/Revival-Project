# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloweenLotteryOpen.py
from __future__ import absolute_import
from six.moves import range
from .SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils, mall_utils, item_utils
from common.cfg import confmgr

class ActivityHalloweenLotteryOpen(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202110/halloween_luck/i_activity_halloween'
    APPEAR_ANIM = 'show'
    LOOP_START_TIME = 0.2
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1

    def on_init_panel(self, *args):
        self.init_skin_name()
        super(ActivityHalloweenLotteryOpen, self).on_init_panel(*args)
        self.panel.PlayAnimation(self.LOOP_ANIM)

        @self.panel.btn_halloween_yellow.unique_callback()
        def OnClick(*args):
            jump_to_ui_utils.jump_to_lottery('66')
            self.close()

        self.panel.lab_introduce.SetString(610082)

    def get_close_node(self):
        return (
         self.panel.btn_halloween_close,)

    def on_anim_finish(self):
        close_node = self.get_close_node()
        for nd in close_node:

            @nd.callback()
            def OnClick(*args):
                if callable(self._close_btn_cb):
                    self._close_btn_cb()
                else:
                    self.close()

    def init_skin_name(self):
        role_ids = [
         11, 12, 13]
        skin_ids = [201001146, 201001244, 201001346]
        role_info = confmgr.get('role_info', 'RoleProfile', 'Content')
        for idx in range(3):
            role_id = role_ids[idx]
            skin_id = skin_ids[idx]
            role_name = role_info[str(role_id)]['role_name']
            skin_name = item_utils.get_lobby_item_name(skin_id)
            lab_role_name_str = 'lab_name_get_0{}'.format(idx + 1)
            lab_name_str = 'lab_name_0{}'.format(idx + 1)
            role_name_node = getattr(self.panel, lab_role_name_str)
            skin_name_node = getattr(self.panel, lab_name_str)
            role_name_node and role_name_node.SetString(role_name)
            skin_name_node and skin_name_node.SetString(skin_name)