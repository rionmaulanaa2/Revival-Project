# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanCardWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.template_utils import update_badge_node
from logic.gutils.role_head_utils import get_head_frame_res_path, get_head_photo_res_path

class ClanCardWidget(BaseUIWidget):

    def get_clan_info(self):
        return self._clan_info

    def get_clan_commander_info(self):
        return self._commander_info

    def __init__(self, panel_cls, ui_panel, clan_id, init_cb=None, need_anim=True):
        self.global_events = {'global_message_on_query_clan_info': self._update_clan_info,
           'message_on_player_simple_inf': self._update_clan_commander
           }
        super(ClanCardWidget, self).__init__(panel_cls, ui_panel)
        self._clan_id = clan_id
        self._commander_id = None
        self._clan_info = None
        self._commander_info = None
        self._init_cb = init_cb
        self._need_anim = need_anim
        self._init_panel()
        global_data.player.query_clan_info(self._clan_id)
        return

    def _init_panel(self):
        self.panel.setVisible(False)
        self.panel.bar1.nd_middle.nd_leader.setVisible(False)

    def _update_clan_info(self, clan_id, clan_info):
        self._clan_info = clan_info
        self.panel.setVisible(True)
        if self._need_anim:
            self.panel.PlayAnimation('show')
        if clan_id != self._clan_id:
            return
        self._commander_id = clan_info['commander_uid']
        nd_left = self.panel.bar1.nd_left
        nd_middle = self.panel.bar1.nd_middle
        clan_lv = clan_info.get('lv', 1)
        nd_left.lab_level.setString('LV.{}'.format(clan_lv))
        clan_badge = clan_info.get('badge', 0)
        update_badge_node(clan_badge, self.panel.temp_crew_logo)
        clan_id = clan_info.get('clan_id', '')
        nd_left.lab_id.setString('ID.{}'.format(clan_id))
        clan_name = clan_info.get('clan_name', '')
        nd_left.lab_name.setString(str(clan_name))
        from common.cfg import confmgr
        member_num = clan_info.get('member_num', 0)
        max_member_num = confmgr.get('clan_lv_data', str(clan_lv), 'iMember')
        nd_middle.img_member.nd_member.nd_auto_fit.lab_member.SetString('{0}/{1}'.format(member_num, max_member_num))
        if G_IS_NA_USER:
            from logic.gcommon.common_const.lang_data import code_2_showname
            lang_code = clan_info.get('lang', -1)
            lang_name = code_2_showname.get(lang_code, get_text_by_id(860016))
            lang_font = confmgr.get('lang_conf', str(lang_code), default={}).get('bShowFont', 'gui/fonts/fzdys.ttf')
            nd_middle.img_language.lab_language.SetString(str(lang_name))
            nd_middle.img_language.lab_language.SetFontName(lang_font)
        else:
            nd_middle.img_language.setVisible(False)
        lv_limit = clan_info.get('apply_lv_limit', 0)
        if lv_limit > 0:
            text = 'LV.{}'.format(lv_limit)
        else:
            text = get_text_by_id(860018)
        nd_middle.img_limited_level.lab_limited_level.SetString(str(text))
        from logic.gcommon.cdata import dan_data
        apply_dan_limit = clan_info.get('apply_dan_limit', -1)
        text_id = dan_data.data.get(apply_dan_limit, {}).get('name', 860017)
        nd_middle.ikg_limited_tier.lab_limited_tier.SetString(text_id)
        clan_intro = clan_info.get('intro', '')
        self.panel.bar2.lab_announce.setString(str(clan_intro))
        sp_point = clan_info.get('season_point', 0)
        nd_middle.lab_season_point.SetString(str(sp_point))
        player_inf = global_data.message_data.get_player_simple_inf(self._commander_id)
        if player_inf:
            self._init_clan_owner_info(player_inf)

    def _init_clan_owner_info(self, info):
        self._commander_info = info
        from logic.gcommon.cdata.dan_data import get_dan_name_id, BROZE
        from logic.gutils.role_head_utils import set_role_dan, init_role_head_auto
        nd_middle = self.panel.bar1.nd_middle
        nd_leader = nd_middle.nd_leader
        nd_leader.setVisible(True)
        commander_name = info.get('char_name', '')
        dan_info = info['dan_info']
        lv = info['lv']
        dan = dan_info.get('survival_dan', {}).get('dan', BROZE)
        dan_name = get_text_by_id(get_dan_name_id(dan))
        nd_leader.lab_crew_leader_tier.SetString(dan_name)
        nd_leader.lab_crew_leader_name.setString(str(commander_name))
        nd_leader.lab_crew_leader_level.SetString('LV.{0}'.format(lv))
        set_role_dan(nd_leader.temp_leader_tier, dan_info)
        frame_path = get_head_frame_res_path(info['head_frame'])
        nd_leader.temp_crew_leader.img_head_frame.SetDisplayFrameByPath('', frame_path)
        head_path = get_head_photo_res_path(info['head_photo'])
        nd_leader.temp_crew_leader.img_head.SetDisplayFrameByPath('', head_path)

        @nd_leader.temp_crew_leader.unique_callback()
        def OnClick(*args):
            if int(info['uid']) == global_data.player.uid:
                return
            global_data.ui_mgr.close_ui('PlayerSimpleInf')
            import cc
            pos_x, pos_y = nd_leader.temp_crew_leader.GetPosition()
            world_pos = nd_leader.temp_crew_leader.ConvertToWorldSpace(pos_x, pos_y)
            size = nd_leader.temp_crew_leader.getContentSize()
            show_pos_x = world_pos.x + size.width
            show_pos_y = world_pos.y + size.height
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(info['uid']))
            ui.set_position(cc.Vec2(show_pos_x, show_pos_y))

        @self.panel.btn_report.unique_callback()
        def OnClick(*args):
            self.on_click_report_btn()

        if self._init_cb and callable(self._init_cb):
            self._init_cb()
            self._init_cb = None
        return

    def _update_clan_commander(self, info):
        if info['uid'] == self._commander_id and self._commander_info is None:
            self._init_clan_owner_info(info)
        return

    def on_click_report_btn(self, *args):
        from logic.gutils import jump_to_ui_utils
        clan_info = self._clan_info or {}
        if not clan_info:
            return
        jump_to_ui_utils.jump_to_clan_report({'clan_id': clan_info.get('clan_id', -1),
           'clan_name': clan_info.get('clan_name', ''),
           'clan_intro': clan_info.get('intro', '')
           })

    def destroy(self):
        self._init_cb = None
        super(ClanCardWidget, self).destroy()
        return