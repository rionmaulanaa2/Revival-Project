# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonNewRole.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import jump_to_ui_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.activity.widget import widget
from logic.gutils.item_utils import get_mecha_name_by_id, get_lobby_item_name

@widget('AsyncTaskListWidget')
class ActivityCommonNewRole(ActivityBase):

    def on_init_panel(self):
        ui_data = confmgr.get('c_activity_config', self._activity_type, default={}).get('cUiData', {})
        is_mecha = ui_data.get('is_mecha', False)
        is_skin = ui_data.get('is_skin', False)
        if is_mecha:
            self.mecha_id = ui_data.get('role_id', 8001)
            self.panel.lab_name.SetString(get_mecha_name_by_id(self.mecha_id))

            @self.panel.btn_show.unique_callback()
            def OnClick(*args):
                jump_to_ui_utils.jump_to_display_detail_by_goods_id('10100' + str(self.mecha_id))

        elif is_skin:
            self.skin_id = str(ui_data.get('role_id', 8001))
            self.panel.lab_name.SetString(get_lobby_item_name(self.skin_id))

            @self.panel.btn_show.unique_callback()
            def OnClick(*args):
                jump_to_ui_utils.jump_to_display_detail_by_item_no(str(self.skin_id))

        else:
            role_id = str(ui_data.get('role_id', 11))
            role_info = confmgr.get('role_info', 'RoleProfile', 'Content', role_id)
            self.panel.lab_name.SetString(role_info['role_name'])

            @self.panel.btn_show.unique_callback()
            def OnClick(*args):
                jump_to_ui_utils.jump_to_display_detail_by_goods_id(role_id)