# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/setting_utils.py
from __future__ import absolute_import

class SettingTips(object):

    def __init__(self, archive_key, template_path, target_nd, show_func, parent, panel):
        self._archive_key = archive_key
        self._template_path = template_path
        self.target_nd = target_nd
        self._show_func = show_func
        self._guide_panel = None
        self.parent = parent
        self.panel = panel
        self._time_limit = 0
        return

    def destroy(self):
        self._archive_key = ''
        self._template_path = ''
        self.target_nd = None
        self._show_func = None
        if self._guide_panel and self._guide_panel.isValid():
            self._guide_panel.Destroy()
        self._guide_panel = None
        self.parent = None
        self.panel = None
        return

    def check_show_tips(self):
        if not global_data.achi_mgr.get_cur_user_archive_data(self._archive_key, 0):
            self.show_guide_setting_tips()
            global_data.achi_mgr.set_cur_user_archive_data(self._archive_key, 1)

    def show_guide_setting_tips(self):
        import logic.gcommon.time_utility as time_utils
        panel = self._guide_panel
        if panel is None:
            panel = global_data.uisystem.load_template_create(self._template_path, parent=self.parent.panel)
            self._guide_panel = panel
            if self._show_func:

                def time_func():
                    return time_utils.time() - self._time_limit > 1

                self._show_func(self._guide_panel, time_func)
        self._time_limit = time_utils.time()
        return


def init_one_setting_list_choose(ui_list_item, index, key, select_cb=None, upload=True):
    from logic.gutils.template_utils import init_radio_group, init_radio_group_new
    choose = ui_list_item.GetItem(index)
    choose_1, choose_2 = init_radio_group_new(choose)

    @choose_1.unique_callback()
    def OnSelect(btn, choose, trigger_event):
        if choose and trigger_event:
            global_data.player and global_data.player.write_setting_2(key, True, upload)
            select_cb and select_cb(key, True)

    @choose_2.unique_callback()
    def OnSelect(btn, choose, trigger_event):
        if choose and trigger_event:
            global_data.player and global_data.player.write_setting_2(key, False, upload)
            select_cb and select_cb(key, False)

    if global_data.player.get_setting_2(key):
        choose_1.btn_choose.OnClick(None, False)
    else:
        choose_2.btn_choose.OnClick(None, False)
    return