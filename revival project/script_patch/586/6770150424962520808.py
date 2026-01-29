# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/MechaRegionRankWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon import const
from logic.comsys.rank.BaseRankWidget import BaseRankWidget
from logic.gcommon.common_const import rank_mecha_const
from logic.gcommon.common_const import rank_const
from logic.gutils import role_head_utils
from logic.gutils import season_utils
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
from cocosui import cc, ccui, ccs
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import follow_utils
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils import locate_utils
FRIEND_RANK = 0
ALL_AREA_RANK = 1
SHOW_LOCATE_DIALOG = True

def show_locate_dialog():
    if not rank_const.is_world_mecha_region_rank():
        from logic.comsys.rank.LocateDialog import LocateDialog
        LocateDialog(None)
    else:
        from logic.comsys.rank.LocateChooseDialog import LocateChooseDialog
        LocateChooseDialog(None)
    return


def conofirm_show_locate_dialog():
    global SHOW_LOCATE_DIALOG

    def _show_func():
        global SHOW_LOCATE_DIALOG
        show_locate_dialog()
        SHOW_LOCATE_DIALOG = False

    if SHOW_LOCATE_DIALOG and not global_data.player.rank_adcode and global_data.player.can_set_rank_adcode():
        from logic.gutils.share_utils import huawei_permission_confirm
        permission = 'android.permission.ACCESS_COARSE_LOCATION'
        huawei_permission_confirm(permission, 635576, _show_func)


def conofirm_do_locate():
    from logic.gutils.share_utils import huawei_permission_confirm
    permission = 'android.permission.ACCESS_COARSE_LOCATION'
    huawei_permission_confirm(permission, 635576, do_locate)


def do_locate():
    if global_data.player.can_set_rank_adcode():
        show_locate_dialog()
    else:
        global_data.game_mgr.show_tip(get_text_by_id(15072))


class MechaRegionRankWidget(BaseRankWidget):

    def __init__(self, parent_panel, nd, template_pos, rank_info, init_mecha_id=None):
        super(MechaRegionRankWidget, self).__init__(rank_info)
        self.parent_panel = parent_panel
        self.nd = nd
        self._template_root = global_data.uisystem.load_template_create('rank/i_rank_mecha_list_cn', parent=nd)
        self._template_root.setPosition(template_pos)
        self.nd_locate = self._template_root.nd_locate
        self.list_rank = self._template_root.list_rank_list
        self._init_mecha_id = init_mecha_id
        self.cur_rank_type = None
        self.cur_rank_area = locate_utils.get_default_area(global_data.player.rank_adcode)
        self.rank_index = None
        self._show_top_rank = False
        if self.is_show_world_mecha:
            self._score_limit_text = {rank_const.REGION_CITY_RANK: 15097,rank_const.REGION_PROVINCE_RANK: 15097,
               rank_const.REGION_COUNTRY_RANK: 15097
               }
        else:
            self._score_limit_text = {rank_const.REGION_CITY_RANK: 15067,rank_const.REGION_PROVINCE_RANK: 15068,
               rank_const.REGION_COUNTRY_RANK: 15069
               }
        self.locate_tabs = []
        self.mecha_id_list = []
        self.init_mecha_id_list()
        self.init_list()
        self.init_top_panel()
        self.init_expire_panel()
        self.refresh_location_panel(is_init=True)
        self.process_event(True)
        return

    def destroy(self):
        super(MechaRegionRankWidget, self).destroy()
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_respond_set_adcode': self.on_respond_set_adcode,
           'message_on_region_my_rank_data': self.on_region_my_rank_data
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_respond_set_adcode(self):
        self.cur_rank_area = locate_utils.get_default_area(global_data.player.rank_adcode)
        self.refresh_location_panel(is_init=True)

    def request_rank_data(self):
        if not global_data.player.rank_adcode:
            global_data.channel.regeo_location()
            self.request_region_my_rank_data()
            return
        super(MechaRegionRankWidget, self).request_rank_data()

    def init_mecha_id_list(self):
        open_mecha_list = global_data.player.read_mecha_open_info()['opened_order']
        self.mecha_id_list = [ str(mecha_id) for mecha_id in open_mecha_list if str(mecha_id) in rank_mecha_const.mecha_rank_list ]

    def init_top_panel(self):
        temp_top = self._template_root.temp_top
        self._template_root.lab_request.SetString('')
        self._template_root.lab_request_num.SetString('')
        temp_top.img_player_mech_head_bg.setVisible(True)
        self._template_root.nd_choose.setVisible(False)

        @temp_top.btn_player_mech_head.unique_callback()
        def OnClick(*args):
            flag = self._template_root.nd_choose.isVisible()
            self._template_root.nd_choose.setVisible(not flag)

        @self._template_root.btn_locate.callback()
        def OnClick(btn, touch):
            conofirm_do_locate()

        @self._template_root.temp_btn_locate.btn_common.unique_callback()
        def OnClick(*args):
            conofirm_do_locate()

        conofirm_show_locate_dialog()
        default_show_idx = 0
        if self._init_mecha_id:
            mecha_id = self._init_mecha_id
        else:
            mecha_id = global_data.achi_mgr.get_cur_user_archive_data(rank_const.RANK_MECHA_READ_RECORD_KEY, default=None)
        if mecha_id != None:
            rank_idx = self.get_rank_idx_by_mecha_battle_id(mecha_id)
            if rank_idx != -1:
                default_show_idx = rank_idx
        self._template_root.list_mech_choose.DeleteAllSubItem()
        for index in range(len(self.mecha_id_list)):
            self.add_mecha_choose_item(index, default_show_idx)

        self._template_root.nd_choose.img_bg.ResizeAndPosition()
        return

    def init_expire_panel(self):

        @self._template_root.nd_idle.btn_idle_question.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(15053), get_text_by_id(15052))

        @self._template_root.temp_top.btn_question.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(15053), get_text_by_id(15052))

        self.parent_panel.temp_nativebest_btn.setVisible(True)
        self.parent_panel.temp_nativebest_btn.lab_nativebest.SetString(611357 if self.is_show_world_mecha else 15071)

        @self.parent_panel.temp_nativebest_btn.btn_nativebest.unique_callback()
        def OnClick(*args):
            from logic.gcommon.cdata import adcode_data
            req_adcode = locate_utils.get_rank_service_code(adcode_data.ADCODE_HEAD, rank_const.REGION_COUNTRY_RANK)
            rank_data = self._message_data.get_region_rank_data(self.cur_rank_type, req_adcode)
            if not rank_data:
                self._show_top_rank = True
                locate_utils.request_region_rank_data(self.cur_rank_type, rank_const.REGION_COUNTRY_RANK, adcode_data.ADCODE_HEAD)
            else:
                self.on_show_top_rank()

    def refresh_location_panel(self, is_init=False):
        text_ids = []
        area_list = [rank_const.REGION_CITY_RANK, rank_const.REGION_PROVINCE_RANK, rank_const.REGION_COUNTRY_RANK]
        for area in area_list:
            text_ids.append(locate_utils.get_rank_area_text(global_data.player.rank_adcode, area))

        self.locate_tabs = [self.nd_locate.btn_locate_1, self.nd_locate.btn_locate_2, self.nd_locate.btn_locate_3]
        if self.is_show_world_mecha:
            btn_size = [
             (135, 45), (218, 45), (218, 45)]
            txt_size = [cc.Size(132, 42), cc.Size(214, 42), cc.Size(214, 42)]
            btn_pos = [('0%0', '50%0'), ('0%0', '50%0'), ('0%218', '50%0')]
        else:
            btn_size = [
             (135, 45), (135, 45), (135, 45)]
            txt_size = [cc.Size(132, 42), cc.Size(132, 42), cc.Size(132, 42)]
            btn_pos = [('0%0', '50%0'), ('0%135', '50%0'), ('0%270', '50%0')]
        do_click = None
        for i, tab in enumerate(self.locate_tabs):
            btn_enbale = bool(text_ids[i])
            tab.SetEnable(btn_enbale)
            tab.SetContentSize(*btn_size[i])
            tab.SetText(text_ids[i], dimensions=txt_size[i])
            tab.SetPosition(*btn_pos[i])

            @tab.callback()
            def OnClick(btn, touch, index=i, is_init=False):
                if global_data.player.rank_adcode and text_ids[index] != '-':
                    self.select_location_tab(index, is_init=is_init)

            if self.cur_rank_area == self.REGION_RANK_TYPES[i]:
                do_click = OnClick

        if is_init and do_click:
            do_click(None, None, is_init=True)
        if is_init and not global_data.player.rank_adcode:
            self.request_region_my_rank_data()
            self.refresh_empty_status(None)
        return

    def select_location_tab(self, index, is_init=False):
        rank_type = self.REGION_RANK_TYPES[index]
        self.cur_rank_area = rank_type
        for i, tab in enumerate(self.locate_tabs):
            tab.SetSelect(i == index)

        self.request_rank_data()
        self.set_limit_score()

    def refresh_top_title(self, mecha_id):
        temp_top = self._template_root.temp_top
        img_path = 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id
        temp_top.btn_player_mech_head.SetFrames('', [img_path, img_path, ''])
        temp_top.lab_player_name.setString(get_mecha_name_by_id(mecha_id))

    def add_mecha_choose_item(self, index, default_show_idx=0):
        panel = self._template_root.list_mech_choose.AddTemplateItem()
        mecha_id = self.mecha_id_list[index]
        img_path = 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id
        panel.mach_head.SetDisplayFrameByPath('', img_path)
        panel.lab_mech_name.setString(get_mecha_name_by_id(mecha_id))
        temp_top = self._template_root.temp_top

        @panel.btn_shose_mech.unique_callback()
        def OnClick(btn, touch, is_init=False):
            if self.rank_index != index:
                self.rank_index = index
                self.cur_rank_type = mecha_id
                global_data.achi_mgr.set_cur_user_archive_data(rank_const.RANK_MECHA_READ_RECORD_KEY, int(mecha_id))
                if not is_init:
                    self.request_rank_data()
                self.refresh_top_title(mecha_id)
            self._template_root.nd_choose.setVisible(False)

        if index == default_show_idx:
            OnClick(None, None, is_init=True)
        return

    def get_rank_idx_by_mecha_battle_id(self, mecha_id):
        if mecha_id is None:
            return -1
        else:
            for idx, info in enumerate(self.mecha_id_list):
                _mecha_id = int(info)
                if mecha_id == _mecha_id:
                    return idx

            return -1

    def set_visible(self, visible):
        super(MechaRegionRankWidget, self).set_visible(visible)
        self.parent_panel.temp_nativebest_btn.setVisible(visible)

    def on_show_top_rank(self):
        from logic.comsys.rank import MechaTopRank
        rank_list = MechaTopRank.get_top_rank_list(self.cur_rank_type)
        if len(rank_list) <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(611346 if self.is_show_world_mecha else 15083))
        else:
            MechaTopRank.MechaTopRank(None, self.cur_rank_type)
        return

    def on_region_rank_data(self, rank_type, rank_area):
        if self._show_top_rank and rank_type == self.cur_rank_type and str(rank_const.REGION_COUNTRY_RANK) != rank_area:
            self._show_top_rank = False
            self.on_show_top_rank()
            return
        super(MechaRegionRankWidget, self).on_region_rank_data(rank_type, rank_area)
        if rank_type != self.cur_rank_type or self.cur_rank_area != rank_area:
            return
        self.set_limit_score()

    def set_limit_score(self):
        limit_score = locate_utils.get_rank_area_to_limit_score(global_data.player.rank_adcode, self.cur_rank_area)
        if limit_score:
            tips = self._score_limit_text.get(self.cur_rank_area, '')
            self._template_root.lab_request.SetString(tips)
            self._template_root.lab_request_num.SetString(str(limit_score))
        else:
            self._template_root.lab_request.SetString('')
            self._template_root.lab_request_num.SetString('')

    def request_region_my_rank_data(self):
        rank_data = global_data.player.get_my_rank_mecha_data(self.cur_rank_type)
        if not rank_data:
            global_data.player.request_my_rank_service_data(self.cur_rank_type)
        else:
            self.on_region_my_rank_data()

    def on_region_my_rank_data(self):
        new_rank = -1
        new_data = [global_data.player.uid, ('', None, None, None), [-1], new_rank]
        self.refresh_my_data(new_data, new_rank)
        return None

    def refresh_my_data(self, data, rank):
        rank_data = global_data.player.get_my_rank_mecha_data(self.cur_rank_type)
        score = rank_data[1][0] if rank_data else 0
        if data[2]:
            data[2][0] = score
        panel = super(MechaRegionRankWidget, self).refresh_my_data(data, rank)
        if not rank_data or rank_data[1][2]:
            panel.lab_number.SetColor('#SR')
            self._template_root.nd_idle.setVisible(True)
        else:
            panel.lab_number.SetColor('#SK')
            self._template_root.nd_idle.setVisible(False)

    def refresh_item(self, panel, data):
        uid = data[0]
        rank = int(data[3] + 1)
        if rank >= 1 and rank <= 3:
            panel.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
            panel.img_rank.setVisible(True)
            panel.lab_rank.setVisible(False)
        else:
            panel.img_rank.setVisible(False)
            panel.lab_rank.setVisible(True)
            panel.lab_rank.setString(str(rank))
        player_info = self._message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
        if not player_info:
            return
        else:
            name = player_info.get('char_name', '')
            panel.lab_player_name.setString(name)
            role_head_utils.init_role_head(panel.player_role_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            if data[2]:
                if data[2][0] >= 0:
                    panel.lab_number.setString(str(data[2][0]))
                else:
                    panel.lab_number.setString('')
            else:
                panel.lab_number.SetString(15051)
            follow_utils.refresh_rank_list_follow_status(panel, uid, name)
            self.add_player_simple_callback(panel.player_role_head, data, self._template_root.img_list_pnl)
            self.add_reques_model_info(panel, uid)
            return