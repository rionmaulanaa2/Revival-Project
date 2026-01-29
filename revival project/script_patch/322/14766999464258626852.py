# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerMechaMemoryWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from logic.comsys.mecha_display.MechaWidget import MechaTypeChooseWidget
from logic.gutils.mecha_utils import get_mecha_lst
from common.cfg import confmgr
from logic.gutils import dress_utils
from logic.gutils import template_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.mecha_career_utils import MechaMemoryStatWidget, get_career_season_name
SORT_ORDER_PROFICIENCY = 0
SORT_ORDER_GAME_NUM = 1
SORT_ORDER_WIN_RATE = 2
from logic.gcommon.common_const.web_const import MECHA_MEMORY_ALL_SEASON_MODE
sort_info = (
 (
  SORT_ORDER_PROFICIENCY, 83255),
 (
  SORT_ORDER_GAME_NUM, 80072),
 (
  SORT_ORDER_WIN_RATE, 80333))

class PlayerMechaTypeChooseWidget(MechaTypeChooseWidget):

    def on_select_status_ui_update(self, ui_item, is_sel):
        ui_item.btn_tab.SetSelect(is_sel)

    def init_list(self):
        super(PlayerMechaTypeChooseWidget, self).init_list()
        self.list_mecha_choose.SetInitCount(len(self.all_speciality_type_list))
        for ind, sp_type in enumerate(self.all_speciality_type_list):
            ui_item = self.list_mecha_choose.GetItem(ind)
            desc_conf = confmgr.get('mecha_display', 'HangarDescConf', 'Content')
            if sp_type:
                tag_text_id = desc_conf.get(sp_type, {}).get('tag_name_text_id')
                txt = get_text_by_id(tag_text_id)
                ui_item.lab_btn.SetString(txt)
            else:
                ui_item.lab_btn.SetString(868028)


class PlayerMechaMemoryWidget(PlayerTabBaseWidget):
    PANEL_CONFIG_NAME = 'mech_display/career/i_mech_career_mech_main'

    def __init__(self, panel):
        super(PlayerMechaMemoryWidget, self).__init__(panel)
        self.init_parameters()
        self._show_mecha_list = []
        self.init_mecha_list_count()
        self.cur_uid = None
        self.is_mine = True
        self._show_own = False
        self.cur_season_data = {}
        self.received_season_id = None
        self.panel.choose_list_array.setVisible(False)
        self.panel.choose_list_bp.setVisible(False)
        self._cur_battle_season_id = global_data.player.get_battle_season()
        self._show_battle_season_id = self._cur_battle_season_id
        self._sort_order_type = SORT_ORDER_PROFICIENCY
        self.all_mecha_lst, _, _ = get_mecha_lst()
        self.mecha_sp_type_widget = PlayerMechaTypeChooseWidget(self, self.panel)
        self.memory_widget = MechaMemoryStatWidget()
        self.memory_widget.set_data_cb(self.on_received_memory_data)
        self.memory_widget.on_need_show_show_battle_season_id(self._show_battle_season_id)
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
        list_mecha_node = self.panel.list_item
        self._list_sview = InfiniteScrollWidget(list_mecha_node, self.panel, up_limit=500, down_limit=500)
        self._list_sview.set_template_init_callback(self.init_mecha_btn)
        self._list_sview.enable_item_auto_pool(True)
        self.init_choose_list_array()
        self.init_sort_list_array()
        return

    def init_parameters(self):
        from logic.gcommon.common_const.mecha_const import MECHA_TYPE, MECHA_TYPE_ID
        self.MECHA_TYPE = list(MECHA_TYPE)
        self.MECHA_TYPE_ID = list(MECHA_TYPE_ID)

    def init_mecha_list_count(self):
        s = self.panel.nd_list_size.getContentSize()
        row_num = 6
        width = self.panel.list_item.GetCtrlSize().width
        width_indent = self.panel.list_item.GetHorzIndent()
        boarder = self.panel.list_item.GetHorzBorder()
        import math
        count = int(math.floor((s.width + width_indent - 2 * boarder) / float(width + width_indent)))
        if count != self.panel.list_item.GetNumPerUnit():
            if count >= row_num:
                self.panel.list_item.SetNumPerUnit(count)
            else:
                self.panel.list_item.SetNumPerUnit(row_num)

    def on_resolution_changed(self):
        self.init_mecha_list_count()

    def on_switch_sp_type(self, sp_type):
        self.mecha_sp_type_widget.switch_sp_type(sp_type)
        self.refresh_ui_show()

    def destroy(self):
        super(PlayerMechaMemoryWidget, self).destroy()
        if self.mecha_sp_type_widget:
            self.mecha_sp_type_widget.destroy()
            self.mecha_sp_type_widget = None
        if self.memory_widget:
            self.memory_widget.destroy()
            self.memory_widget = None
        return

    def on_refresh_player_detail_inf(self, player_inf):
        from common.const.property_const import U_ID
        new_uid = player_inf[U_ID]
        if self.cur_uid != new_uid:
            self.cur_uid = player_inf[U_ID]
            self.is_mine = self.cur_uid == global_data.player.uid
            if self.memory_widget:
                self.memory_widget.set_uid(self.cur_uid)
                self.memory_widget.refresh()
        elif self.memory_widget:
            self.memory_widget.set_uid(self.cur_uid)
            if self.received_season_id != self._show_battle_season_id:
                self.memory_widget.refresh()

    def refresh_ui_show(self):
        season_data = self.memory_widget.get_season_data()
        if season_data is None:
            self.memory_widget.refresh()
            return
        else:
            _show_mecha_list = self.get_show_data(season_data)
            if _show_mecha_list != self._show_mecha_list:
                self._show_mecha_list = _show_mecha_list
                self._list_sview.update_data_list(self._show_mecha_list)
                self._list_sview.refresh_showed_item()
                self._list_sview.update_scroll_view()
            if not self._show_mecha_list:
                self.panel.nd_empty.setVisible(True)
                if self.is_mine:
                    self.panel.lab_empty.SetString(83352)
                else:
                    self.panel.lab_empty.SetString(83344)
            else:
                self.panel.nd_empty.setVisible(False)
            return

    def get_show_data(self, season_data):
        from logic.gcommon.common_const import web_const
        mecha_order = list(self.mecha_sp_type_widget.get_sp_type_mecha_list())
        get_proficiency = self.get_mecha_season_proficiency
        mecha_proficiency = {mecha_id:get_proficiency(mecha_id, self._show_battle_season_id) for mecha_id in mecha_order}
        mecha_proficiency = {mecha_id:a * 10000 + b for mecha_id, (a, b) in six.iteritems(mecha_proficiency)}
        show_mecha_list = [ m_id for m_id in self.all_mecha_lst if m_id in mecha_order and mecha_proficiency.get(m_id, 0) > 10000 ]
        if self._sort_order_type == SORT_ORDER_GAME_NUM:
            key_func = lambda mecha_id: [season_data.get(str(mecha_id), {}).get(web_const.MECHA_MEMORY_LEVEL_5, 0), 99999 - int(mecha_id)]
            show_mecha_list.sort(key=key_func, reverse=True)
        elif self._sort_order_type == SORT_ORDER_PROFICIENCY:
            key_func = --- This code section failed: ---

 171       0  LOAD_DEREF            0  'mecha_proficiency'
           3  LOAD_ATTR             0  'get'
           6  LOAD_ATTR             1  'int'
           9  CALL_FUNCTION_2       2 
          12  LOAD_CONST            2  99999
          15  LOAD_GLOBAL           1  'int'
          18  LOAD_FAST             0  'mecha_id'
          21  CALL_FUNCTION_1       1 
          24  BINARY_SUBTRACT  
          25  BUILD_LIST_2          2 
          28  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9
            show_mecha_list.sort(key=key_func, reverse=True)
        elif self._sort_order_type == SORT_ORDER_WIN_RATE:

            def _win_rate(mecha_id):
                game_count = max(season_data.get(str(mecha_id), {}).get(web_const.MECHA_MEMORY_LEVEL_5, 0), 1)
                win_count = season_data.get(str(mecha_id), {}).get(web_const.MECHA_MEMORY_LEVEL_2, 0)
                return win_count / float(game_count)

            key_func = lambda mecha_id: [_win_rate(mecha_id), 99999 - int(mecha_id)]
            show_mecha_list.sort(key=key_func, reverse=True)
        return show_mecha_list

    def get_mecha_season_proficiency(self, mecha_id, season):
        mecha_proficiency = self.cur_season_data.get('mecha_proficiency', {}).get(str(mecha_id), [1, 0])
        if self.is_mine and (season == self._cur_battle_season_id or season == MECHA_MEMORY_ALL_SEASON_MODE):
            if global_data.player:
                get_proficiency = global_data.player.get_proficiency if 1 else (lambda _: mecha_proficiency)
                return get_proficiency(mecha_id)
        return mecha_proficiency

    def get_mecha_season_dan(self, mecha_id, season):
        level = self.get_mecha_season_proficiency(mecha_id, season)[0]
        dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        for dan, info in six.iteritems(dan_conf):
            if level < info['max_level']:
                return int(dan)

        return len(dan_conf)

    def get_mecha_season_fashion(self, mecha_id, season=None):
        lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(int(mecha_id))
        origin_dress_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(lobby_mecha_id), 'default_fashion')[0]
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR
        mecha_fashion_dict = self.cur_season_data.get('mecha_fashion', {}).get(str(mecha_id), {}).get('fashion', {})
        mecha_clothing_id = mecha_fashion_dict.get(FASHION_POS_SUIT)
        if self.is_mine:
            dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(mecha_id) or origin_dress_id
            return dressed_clothing_id
        return mecha_clothing_id or origin_dress_id

    def init_mecha_btn(self, ui_item, data):
        from logic.gcommon.common_const.mecha_const import SKIN_RARE_BACKGROUND
        mecha_id = data
        all_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        conf = all_conf.get(str(mecha_id), {})
        mecha_name = conf.get('name_mecha_text_id', '')
        mecha_icon_path = conf.get('icon_mecha_path', [])
        ui_item.lab_mech_name.SetString(mecha_name)
        lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(int(mecha_id))
        path_index = 0
        origin_dress_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(lobby_mecha_id), 'default_fashion')[0]
        dressed_clothing_id = self.get_mecha_season_fashion(mecha_id, self._show_battle_season_id)
        if dressed_clothing_id != origin_dress_id:
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(dressed_clothing_id))
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                ui_item.btn_mech_list_nml.bar_level.nd_cut.setVisible(True)
                ui_item.btn_mech_list_nml.bar_level.nd_cut.img_mech.SetDisplayFrameByPath('', skin_half_imge_path)
            item_conf = confmgr.get('lobby_item', str(dressed_clothing_id))
            rare_degree = item_conf.get('rare_degree', 0)
            background_img = SKIN_RARE_BACKGROUND.get(rare_degree)
            if background_img:
                ui_item.btn_mech_list_nml.bar_level.SetDisplayFrameByPath('', background_img)
        else:
            ui_item.btn_mech_list_nml.frame.setVisible(False)
            ui_item.btn_mech_list_nml.bar_level.nd_cut.setVisible(False)
            ui_item.btn_mech_list_nml.bar_level.SetDisplayFrameByPath('', mecha_icon_path[path_index])
        dan = self.get_mecha_season_dan(mecha_id, self._show_battle_season_id)
        ui_item.img_mech_level.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/img_proficiency_%d_s.png' % (dan - 1))
        if self.memory_widget:
            season_data = self.memory_widget.get_season_data() or {}
            mecha_data = season_data.get(str(mecha_id), {})
            self.set_ui_item_mecha_data(ui_item, mecha_id, mecha_data)

        @ui_item.btn_real.callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_mecha_memory
            jump_to_mecha_memory(mecha_id, is_mine=self.is_mine, data_dict=self.cur_season_data, uid=self.cur_uid)

        return

    def init_choose_list_array(self):
        if not global_data.player:
            return
        from logic.gutils.memory_utils import get_memory_record_start_season
        start_season = get_memory_record_start_season()
        self._history_season_ids = list(range(start_season, self._cur_battle_season_id + 1))
        seasons_list = self._history_season_ids
        if self._cur_battle_season_id not in seasons_list:
            seasons_list.append(self._cur_battle_season_id)
        mode_option = [ {'name': self.get_season_name(s_id),'mode': s_id} for s_id in reversed(seasons_list) ]
        mode_option.append({'name': 83360,'mode': MECHA_MEMORY_ALL_SEASON_MODE})

        def call_back(index):
            option = mode_option[index]
            self.memory_widget.on_need_show_show_battle_season_id(option['mode'])
            self._show_battle_season_id = option['mode']
            self.panel.btn_choose_bp.lab_choose.SetString(option['name'])
            if self.cur_uid:
                self.memory_widget.refresh()

        def close_callback():
            pass

        template_utils.init_common_choose_list_2(self.panel.choose_list_bp, self.panel.btn_choose_bp.icon_arrow, mode_option, call_back, close_cb=close_callback, func_btn=self.panel.btn_choose_bp)
        call_back(0)

    def init_sort_list_array(self):
        mode_option = [ {'name': s_tid,'mode': s_id} for s_id, s_tid in sort_info ]

        def call_back(index):
            option = mode_option[index]
            self.panel.btn_array.SetText(option['name'])
            sort_order = option['mode']
            if sort_order != self._sort_order_type:
                self._sort_order_type = sort_order
                self.refresh_sort_order()

        def close_callback():
            pass

        template_utils.init_common_choose_list_2(self.panel.choose_list_array, self.panel.btn_array.img_icon, mode_option, call_back, close_cb=close_callback, func_btn=self.panel.btn_array)
        call_back(0)

    def get_season_name(self, season_id):
        return get_career_season_name(season_id)

    def refresh_sort_order(self):
        self.refresh_ui_show()
        if self.memory_widget:
            self.memory_widget.refresh()

    def on_received_memory_data(self, season_id, season_data, fake_init=False):
        if season_id != self._show_battle_season_id:
            return
        if fake_init:
            return
        self.cur_season_data = season_data
        self.received_season_id = season_id
        self._show_mecha_list = self.get_show_data(season_data)
        self._list_sview.update_data_list(self._show_mecha_list)
        self._list_sview.refresh_showed_item()
        self._list_sview.update_scroll_view()
        if not self._show_mecha_list:
            self.panel.nd_empty.setVisible(True)
            if self.is_mine:
                self.panel.lab_empty.SetString(get_text_by_id(83352))
            else:
                self.panel.lab_empty.SetString(83344)
        else:
            self.panel.nd_empty.setVisible(False)

    def set_ui_item_mecha_data(self, ui_item, mecha_id, mecha_data):
        from logic.gutils.mecha_career_utils import get_mecha_career_data, init_mecha_career_panel, get_mecha_career_show_num
        key1 = 'mecha_game_num'
        key2 = 'mecha_win_rate'
        mecha_dict, _, _ = get_mecha_career_data(mecha_id, mecha_data)
        ui_item.lab_value.SetString(get_text_by_id(80072) + ':' + get_mecha_career_show_num(key1, mecha_dict))
        ui_item.lab_value2.SetString(get_text_by_id(80333) + ':' + get_mecha_career_show_num(key2, mecha_dict))