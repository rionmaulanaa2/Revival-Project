# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/RankContentWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.role_head_utils import init_role_head
from logic.gutils import role_head_utils
from logic.gutils import season_utils
from logic.gcommon.cdata import dan_data
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
RANK_SHOW_TYPE_COMMON = 0
RANK_SHOW_TYPE_PERCENT = 1
RANK_SHOW_TYPE_SECOND_TO_MINUTE = 2
RANK_SHOW_TYPE_HIDE = 3
SUB_PAGE_ITEM_COUNT = 10
DAN_LIST_PATH = 'rank/rank_list_tier'
DAN_TITLE_PATH = 'rank/rank_title_tier'

class RankContentWidget(object):

    def __init__(self, parent_panel, panel, *args, **kargs):
        self.panel = panel
        self.parent_panel = parent_panel
        self._rank_sview = self.panel.rank_list
        self._rank_sview_height = self._rank_sview.getContentSize().height
        self._rank_sview_slider = self.panel.nd_slider.img_slider
        self._slider_min_percent = 5.0
        self._slider_max_percent = 95.0
        self._is_dan_rank = False
        self._max_rank = 1
        self._rank_data = []
        self._sview_index = 0
        self._is_check_sview = False
        self.check_sview_callback = None
        self._rank_data_type = [RANK_SHOW_TYPE_COMMON, RANK_SHOW_TYPE_COMMON, RANK_SHOW_TYPE_COMMON]

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.panel.SetTimeOut(0.021, self.check_sview)

        self._rank_sview.addEventListener(scroll_callback)
        return

    def set_sview_update_callback(self, callback):
        self.check_sview_callback = callback

    def set_is_dan_rank(self, flag):
        self._is_dan_rank = flag

    def check_sview(self):
        msg_count = len(self._rank_data)
        self._sview_index = self._rank_sview.AutoAddAndRemoveItem(self._sview_index, self._rank_data, msg_count, self.add_rank_elem, 300, 300)
        if self._rank_sview.GetItemCount() > 0:
            unit_height = self._rank_sview.GetItem(0).getContentSize().height
            unit_index = -self._rank_sview.getInnerContainer().getPositionY() / unit_height
            bottom_show_rank = self._sview_index - unit_index + 1
            percent = 1.0
            if self._max_rank != 10:
                percent = 1.0 * (self._max_rank - bottom_show_rank) / (self._max_rank - 10)
            percent = self._slider_min_percent + (self._slider_max_percent - self._slider_min_percent) * percent
            if percent < self._slider_min_percent:
                percent = self._slider_min_percent
            if percent > self._slider_max_percent:
                percent = self._slider_max_percent
            self._rank_sview_slider.SetPosition('50%', '{}%'.format(percent))
        self._is_check_sview = False
        if self.check_sview_callback:
            self.check_sview_callback(self._sview_index, msg_count)

    def add_rank_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            if self._is_dan_rank:
                panel = global_data.uisystem.load_template_create(DAN_LIST_PATH)
                self._rank_sview.AddControl(panel, bRefresh=True)
            else:
                panel = self._rank_sview.AddTemplateItem(bRefresh=True)
        elif self._is_dan_rank:
            panel = global_data.uisystem.load_template_create(DAN_LIST_PATH)
            self._rank_sview.AddControl(panel, 0, bRefresh=True)
        else:
            panel = self._rank_sview.AddTemplateItem(0, bRefresh=True)
        if (data[3] + 1) % 2:
            panel.img_bg.setVisible(False)
        if global_data.player and global_data.player.uid == data[0]:
            panel.img_bg_self.setVisible(True)
            panel.img_bg.setVisible(False)
        else:
            panel.img_bg_self.setVisible(False)
        self._refresh_item_rank_data(panel, data, False)

        @panel.temp_head.unique_callback()
        def OnClick(btn, *args):
            if global_data.player and data[0] == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.del_btn(BTN_TYPE_TEAM)
                ui.hide_btn_chat()
                ui.refresh_by_uid(data[0])
                pos = self.panel.nd_content.ConvertToWorldSpacePercentage(100, 50)
                pos.x -= 345
                pos.y += 215
                ui.nd_tips.SetPosition(pos.x, pos.y)

        @panel.callback()
        def OnClick(btn, *args):
            if global_data.player and data[0] == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.del_btn(BTN_TYPE_TEAM)
                ui.hide_btn_chat()
                ui.refresh_by_uid(data[0])
                pos = self.panel.nd_content.ConvertToWorldSpacePercentage(100, 50)
                pos.x -= 345
                pos.y += 215
                ui.nd_tips.SetPosition(pos.x, pos.y)

        return panel

    def get_show_text(self, data, show_type):
        if data == rank_const.RANK_DATA_NONE:
            return '-'
        if show_type == RANK_SHOW_TYPE_PERCENT:
            text = '%.2f' % (float(data) * 100) + '%'
        elif show_type == RANK_SHOW_TYPE_SECOND_TO_MINUTE:
            text = '%.2f' % float(data / 60.0)
        elif show_type == RANK_SHOW_TYPE_HIDE:
            text = ''
        elif isinstance(data, float):
            text = '%.2f' % data
        else:
            text = str(data)
        return text

    def refresh_rank_content(self, rank_data):
        self._rank_sview.DeleteAllSubItem()
        self._max_rank = max(rank_data.get('max_count', 0), len(rank_data))
        if self._max_rank == 0:
            self._max_rank = 1
        ratio = 1.0 * SUB_PAGE_ITEM_COUNT / self._max_rank
        if ratio < 0.1:
            ratio = 0.1
        else:
            if ratio > 1.0:
                ratio = 1.0
            ratio = int(ratio * 100) / 100.0
            slider_height = 100 * ratio
            self._rank_sview_slider.SetContentSize(4, '{}%'.format(slider_height))
            self._slider_min_percent = slider_height / 2
            self._slider_max_percent = 100 - self._slider_min_percent
            self.refresh_self_rank_data(rank_data['player_rank'], rank_data['player_data'])
            self._rank_data = rank_data['rank_list']
            data_count = len(self._rank_data)
            self._sview_index = 0
            all_height = 0
            index = 0
            while all_height < self._rank_sview_height + 100 and index < data_count:
                data = self._rank_data[index]
                panel = self.add_rank_elem(data)
                all_height += panel.getContentSize().height
                index += 1

        self._sview_index = index - 1

    def refresh_rank_title(self, title_inf):
        nd = self.panel
        dan_rank_title = getattr(nd.nd_content, 'dan_rank_title', None)
        rank_title = nd.rank_title
        if dan_rank_title:
            dan_rank_title.setVisible(self._is_dan_rank)
        rank_title.setVisible(not self._is_dan_rank)
        if not self._is_dan_rank:
            rank_title.lab_content1.setString(get_text_by_id(title_inf[0]))
            self._rank_data_type[0] = self.get_show_type(title_inf[0])
            rank_title.lab_content2.setString(get_text_by_id(title_inf[1]))
            self._rank_data_type[1] = self.get_show_type(title_inf[1])
            rank_title.lab_content3.setString(get_text_by_id(title_inf[2]))
            self._rank_data_type[2] = self.get_show_type(title_inf[2])
        elif not dan_rank_title:
            dan_rank_title = global_data.uisystem.load_template_create(DAN_TITLE_PATH, name='dan_rank_title', parent=nd.nd_content)
            dan_rank_title.setPosition(rank_title.getPosition())
        return

    def refresh_self_rank_data(self, player_rank, player_data):
        nd = self.panel
        dan_rank_player = getattr(nd.nd_content, 'dan_rank_player', None)
        rank_player = nd.rank_player
        if dan_rank_player:
            dan_rank_player.setVisible(self._is_dan_rank)
        rank_player.setVisible(not self._is_dan_rank)
        if self._is_dan_rank:
            if not dan_rank_player:
                dan_rank_player = global_data.uisystem.load_template_create(DAN_LIST_PATH, name='dan_rank_player', parent=nd.nd_content)
                dan_rank_player.setPosition(rank_player.getPosition())
            nd_player = dan_rank_player
        else:
            nd_player = rank_player
        self._refresh_item_rank_data(nd_player, player_data, True, player_rank)
        return

    def _refresh_item_rank_data(self, nd_item, data, is_self_rank=False, player_rank=None):
        if is_self_rank:
            if player_rank == rank_const.RANK_DATA_OUTSIDE:
                text = get_text_by_id(15016)
            elif player_rank == rank_const.RANK_DATA_NONE:
                text = '-'
            else:
                text = str(player_rank)
            head_frame = global_data.player.get_head_frame()
            head_photo = global_data.player.get_head_photo()
            init_role_head(nd_item.temp_head, head_frame, head_photo)
            nd_item.lab_name.setString(global_data.player.get_name() if global_data.player else '')
            nd_item.lab_rank.setString(text)
        else:
            char_name, role_id, head_frame, head_photo = data[1]
            init_role_head(nd_item.temp_head, head_frame, head_photo)
            nd_item.lab_name.setString(str(char_name))
            nd_item.lab_rank.setString(str(data[3] + 1))
        if not self._is_dan_rank:
            player_data_count = len(data[2])
            while player_data_count < 3:
                data[2].insert(0, None)
                player_data_count += 1

            nd_content_list = [nd_item.lab_content1, nd_item.lab_content2, nd_item.lab_content3]
            for i in range(player_data_count):
                _data = data[2][i]
                text = self.get_show_text(_data, self._rank_data_type[i])
                nd_content_list[i].setString(text)

        else:
            if is_self_rank:
                nd_item.img_bg_player.setVisible(True)
                nd_item.img_bg.setVisible(False)
            dan, lv, star = data[2]
            nd_item.temp_tier.img_tier.SetDisplayFrameByPath('', role_head_utils.get_dan_path(dan, lv))
            nd_item.lab_tier.SetString(season_utils.get_dan_lv_name(dan, lv))
            nd_item.img_star.SetDisplayFrameByPath('', role_head_utils.get_star_path(dan))
            nd_item.lab_star_num.SetString(str(star))
        return

    def get_show_type(self, text_id):
        if text_id == 15008:
            return RANK_SHOW_TYPE_PERCENT
        else:
            if text_id == 15011:
                return RANK_SHOW_TYPE_SECOND_TO_MINUTE
            if text_id is None:
                return RANK_SHOW_TYPE_HIDE
            return RANK_SHOW_TYPE_COMMON
            return

    def destroy(self):
        self.panel = None
        self.parent_panel = None
        self._rank_sview = None
        self._rank_sview_slider = None
        return