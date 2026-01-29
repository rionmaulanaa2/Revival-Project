# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanChangeTitleUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.property_const import *
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import clan_utils
from logic.gutils import template_utils
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class ClanChangeTitleUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'crew/i_crew_change_position'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected'
       }
    OPEN_SOUND_NAME = 'menu_shop'

    def on_init_panel(self, uid=None):
        super(ClanChangeTitleUI, self).on_init_panel()
        self._cur_uid = uid
        self.init_parameters()
        self.init_widget()

    def on_finalize_panel(self):
        pass

    def do_show_panel(self):
        super(ClanChangeTitleUI, self).do_show_panel()

    def _on_login_reconnected(self, *args):
        self.close()

    def init_parameters(self):
        pass

    def init_widget(self):
        from logic.gutils import role_head_utils
        template_utils.init_common_panel(self.panel.temp_bg, 800035, None)
        data = global_data.player.get_member_data(self._cur_uid)
        role_head_utils.init_role_head(self.panel.temp_head, data[HEAD_FRAME], data[HEAD_PHOTO])
        self.panel.lab_name.SetString(data[C_NAME])
        self.panel.lab_position.SetString(clan_utils.get_clan_title_text(data['title']))
        self.panel.lab_week_points.SetString(str(data['week_point']))
        self.panel.lab_season_points.SetString(str(data['season_point']))
        self.show_title_list()
        return

    def show_title_list(self):
        from logic.gcommon.common_const import clan_const
        titles = [
         clan_const.COMMANDER, clan_const.MINISTER, clan_const.ADMIN, clan_const.MASS]
        title_limit = [clan_const.MINISTER, clan_const.ADMIN]
        my_title = clan_utils.get_my_clan_info_by_field('title', default=clan_const.MASS)
        other_title = clan_utils.get_clan_member_info_by_field(self._cur_uid, 'title', default=clan_const.MASS)
        other_name = clan_utils.get_clan_member_info_by_field(self._cur_uid, C_NAME)
        cur_title = [other_title]
        title_list = self.panel.title_list
        title_list.SetInitCount(len(titles))

        def set_title(select_title):
            my_title = clan_utils.get_my_clan_info_by_field('title')
            if my_title > select_title:
                return
            cur_title[0] = select_title
            for i, title in enumerate(titles):
                item_widget = title_list.GetItem(i)
                item_widget.choose.setVisible(cur_title[0] == title)

        titles_count = {}
        for i, title in enumerate(titles):
            item_widget = title_list.GetItem(i)
            title_name = get_text_by_id(clan_utils.get_clan_title_text(title))
            count = clan_utils.get_clan_title_count(title)
            max_count = clan_utils.get_my_clan_title_count_limit(title)
            titles_count[title] = count
            if title in title_limit:
                title_name = '{0} ({1}/{2})'.format(title_name, count, max_count)
            item_widget.text.SetString(title_name)

            @item_widget.btn.unique_callback()
            def OnClick(btn, touch, sel_title=title, count=count, max_count=max_count):
                if sel_title == other_title:
                    set_title(sel_title)
                    return
                if sel_title in title_limit and count >= max_count:
                    global_data.game_mgr.show_tip('{}\xe4\xba\xba\xe5\x91\x98\xe5\xb7\xb2\xe6\xbb\xa1'.format(get_text_by_id(clan_utils.get_clan_title_text(sel_title))))
                    return
                clan_utils.set_permission('appoint_permission_titles', lambda : set_title(sel_title))

        set_title(cur_title[0])

        def do_appoint_title():
            global_data.player.request_appoint_title(self._cur_uid, cur_title[0])
            self.close()

        @self.panel.btn_buy_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            if cur_title[0] == other_title:
                self.close()
                return
            if cur_title[0] == clan_const.COMMANDER:
                content = get_text_by_id(3277)
            elif cur_title[0] < other_title:
                content = get_text_by_id(3278, {'name': other_name,'n': get_text_by_id(clan_utils.get_clan_title_text(cur_title[0]))})
            else:
                content = get_text_by_id(3279, {'name': other_name,'n': get_text_by_id(clan_utils.get_clan_title_text(cur_title[0]))})
            SecondConfirmDlg2().confirm(content=content, confirm_callback=do_appoint_title)