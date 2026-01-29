# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESelectLevelArchiveWidget.py
from __future__ import absolute_import
from six.moves import range
import game3d
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import check_pve_key_enouth, update_price_list, check_read_archive_cost
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, HARD_DIFFICUTY, HELL_DIFFICUTY, DIFFICUTY_LIST, PVE_DIFFICULTY_CACHE, PVE_ENTER_KEY_COUNT, DIFFICULTY_TEXT_LIST, DIFFICULTY_COLOR_LIST, get_read_archive_cost
from logic.gcommon.const import SHOP_PAYMENT_ITEM_PVE_KEY
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.text_utils import get_color_str
from ..PVEEndUI import TIME_COLOR
import logic.gcommon.time_utility as tutils
import six_ex
from logic.gutils.template_utils import FrameLoaderTemplate
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from logic.gutils.pve_utils import get_archive_key, get_bless_elem_res, DEFAULT_BLESS_BAR

class PVESelectLevelArchiveWidget(object):
    PANEL_PIC = 'gui/ui_res_2/pve/end/data/pnl_pve_data_file.png'

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.init_ui_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_item_update
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self):
        self.widget = None
        self.screen_capture_helper = None
        self.settle_dict = {}
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create('pve/end/open_pve_end_file', self.panel.nd_file)

    def init_ui_event(self):

        @self.widget.btn_back.unique_callback()
        def OnClick(layer, touch, *args):
            self.panel.nd_file.setVisible(False)
            self.panel.nd_main.setVisible(True)
            if global_data.player:
                global_data.emgr.on_pve_mecha_changed.emit(global_data.player.get_pve_select_mecha_id())

        def share_cb(*args):
            self.widget.btn_again.setVisible(True)
            self.widget.btn_share.setVisible(True and global_data.is_share_show)
            self.panel.temp_tips_test.setVisible(True)

        @self.widget.btn_share.unique_callback()
        def OnClick(btn, touch):
            self.widget.btn_again.setVisible(False)
            self.widget.btn_share.setVisible(False)
            self.panel.temp_tips_test.setVisible(False)
            if not self.screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self.screen_capture_helper = ScreenFrameHelper()
            self.screen_capture_helper.take_screen_shot([
             self.parent.__class__.__name__], self.panel, custom_cb=share_cb, head_nd_name='nd_player_info_1')

        @self.widget.btn_again.unique_callback()
        def OnClick(_layer, _touch, *args):
            if global_data.player and global_data.player.is_in_team():
                global_data.game_mgr.show_tip(get_text_by_id(452))
                return
            chapter_id, cur_select_difficulty, cur_player_cnt = self.parent._level_widget.get_current_chapter_info()
            if self.check_read_archive_cost(chapter_id, cur_select_difficulty, cur_player_cnt):
                global_data.player.start_pve_battle(chapter_id, cur_select_difficulty, use_archive=True, player_size=cur_player_cnt)
                global_data.enter_pve_with_archive = True
            else:
                global_data.ui_mgr.show_ui('PVEKeyBuyUI', 'logic.comsys.battle.pve.PVEMainUIWidgetUI')
                global_data.game_mgr.show_tip(get_text_by_id(405))

    def init_archive(self):
        archive_data = global_data.player.get_pve_archive()
        if not self.parent._level_widget:
            return
        chapter_id, cur_select_difficulty, cur_player_cnt = self.parent._level_widget.get_current_chapter_info()
        search_key = get_archive_key(chapter_id, cur_select_difficulty, cur_player_cnt)
        if search_key in archive_data:
            read_data = global_data.player.get_pve_archive_read_data()
            read_count = read_data.get(search_key, 0)
            self.widget.btn_again.lab_tips_file.SetString(get_text_by_id(467).format(str(read_count)))
            price_info = [
             {'original_price': get_read_archive_cost(read_count + 1),
                'goods_payment': SHOP_PAYMENT_ITEM_PVE_KEY,
                'discount_price': get_read_archive_cost(read_count + 1)
                }]
            update_price_list(price_info, self.widget.btn_again, self.widget.btn_again.lab_again)
            self.settle_dict = archive_data[search_key]
            self._init_bg()
            self._init_name_widget()
            self._init_title_widget()
            self._init_data_widget()

    def check_read_archive_cost(self, chapter_id, cur_select_difficulty, cur_player_cnt):
        return check_read_archive_cost(chapter_id, cur_select_difficulty, cur_player_cnt)

    def on_item_update(self):
        self.init_archive()

    def _init_bg(self):
        self.widget.bar_data.SetDisplayFrameByPath('', self.PANEL_PIC)

    def _init_name_widget(self):
        mecha_id = self.settle_dict.get('soul_archive').get('mecha_id')
        mecha_name = item_utils.get_mecha_name_by_id(mecha_id)
        self.widget.temp_name.lab_mecha.setString(mecha_name)

    def _init_title_widget(self):
        self.widget.nd_title_file.setVisible(True)
        chapter = self.settle_dict.get('chapter')
        conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
        chapter_str = get_text_by_id(conf.get('title_text'))
        sub_level_str = get_text_by_id(conf.get('sub_title_text'))
        self.widget.lab_level.setString('{}:{}'.format(chapter_str, sub_level_str))

    def _init_data_widget(self):
        self._init_list_info_data()
        self._init_list_merge()

    def _init_list_info_data(self):
        list_info_data = self.widget.list_info_data
        list_info_data.RecycleAllItem()
        saved_statistics = self.settle_dict.get('soul_archive', {}).get('statistics', {})
        statistics = saved_statistics
        item = list_info_data.AddTemplateItem()
        difficulty = self.settle_dict.get('difficulty', 1)
        bar_content = item.bar_content
        bar_content.lab_info.setString(get_text_by_id(464))
        chapter = self.settle_dict.get('chapter')
        conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
        chapter_str = get_text_by_id(conf.get('title_text'))
        difficulty_str = get_color_str(DIFFICULTY_COLOR_LIST[difficulty], get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
        teammate_str = str(self.settle_dict.get('player_size_mode', 1))
        bar_content.lab_data.setString(get_text_by_id(635283).format(chapter_str, difficulty_str, teammate_str))
        item = list_info_data.AddTemplateItem()
        bar_content = item.bar_content
        bar_content.lab_info.setString(get_text_by_id(393))
        time_str = get_color_str(TIME_COLOR, tutils.get_delta_time_str(statistics.get('survival', 0)))
        bar_content.lab_data.setString(time_str)
        item = list_info_data.AddTemplateItem()
        bar_content = item.bar_content
        bar_content.lab_info.setString(get_text_by_id(395))
        bar_content.lab_data.setString(str(statistics.get('kill_monster', 0)))
        item = list_info_data.AddTemplateItem()
        bar_content = item.bar_content
        bar_content.lab_info.setString(get_text_by_id(394))
        bar_content.lab_data.setString(str(int(statistics.get('total_damage', 0))))

    def _init_list_merge(self):
        soul_archive = self.settle_dict.get('soul_archive', {})
        self._chossed_breakthrough = soul_archive.get('chossed_breakthrough', {})
        self._choosed_energy = soul_archive.get('choosed_blesses', {})
        list_merge = self.widget.list_merge
        list_merge.RecycleAllItem()
        list_merge.SetInitCount(1)
        list_merge_item = list_merge.GetItem(0)
        list_merge_breakthrough = list_merge_item.list_breakthrough
        list_merge_breakthrough.RecycleAllItem()
        if self._chossed_breakthrough:
            list_merge_breakthrough.SetInitCount(1)
            self._list_breakthrough = list_merge_breakthrough.GetItem(0).bar_breakthrough.list_breakthrough
            self._init_list_breakthrough()
        list_merge_energy = list_merge_breakthrough.nd_auto_fit.list_energy
        list_merge_energy.RecycleAllItem()
        if self._choosed_energy:
            list_merge_energy.SetInitCount(1)
            self._list_energy = list_merge_energy.GetItem(0).bar_energy.list_energy
            self._init_list_energy()

    def _init_list_breakthrough(self):
        self._list_breakthrough.RecycleAllItem()
        mecha_id = self.settle_dict.get('soul_archive').get('mecha_id')
        break_conf = confmgr.get('mecha_breakthrough_data', str(mecha_id), default=None)
        for slot, level in six_ex.items(self._chossed_breakthrough):
            item = self._list_breakthrough.AddTemplateItem()
            conf = break_conf[str(slot)][str(level)]
            item.nd_skill.setVisible(True)
            item.nd_empty.setVisible(False)
            item.lab_name_skill.SetString(get_text_by_id(conf['name_id']))
            item.img_item.SetDisplayFrameByPath('', conf['icon'])
            for i, btn in enumerate(item.list_dot.GetAllItem()):
                if i < level:
                    btn.SetSelect(True)
                else:
                    break

        return

    def _init_list_energy(self):
        self._energy_list = [ (energy_id, energy_level) for energy_id, energy_level in six_ex.items(self._choosed_energy)
                            ]
        self._frame_loader_template = FrameLoaderTemplate(self._list_energy, len(self._energy_list), self.init_energy_item)

    def init_energy_item(self, item, cur_index):
        bar = item.bar
        energy_id, energy_level = self._energy_list[cur_index]
        bless_conf = confmgr.get('bless_data', str(energy_id), default=None)
        if not bless_conf:
            print self._list_energy
            self._list_energy.RecycleItem(item)
            return
        else:
            item.lab_name.setString(get_text_by_id(bless_conf['name_id']))
            item.btn_energy.img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
            max_level = bless_conf.get('max_level', 1)
            if max_level == 1:
                item.lab_level.setVisible(False)
                item.icon.setVisible(True)
            else:
                item.lab_level.setVisible(True)
                item.icon.setVisible(False)
                item.lab_level.SetString(str(energy_level))
            elem_id = bless_conf.get('elem_id', None)
            if elem_id:
                elem_icon, elem_pnl = get_bless_elem_res(elem_id, ['icon', 'bar'])
                item.icon.SetDisplayFrameByPath('', elem_icon)
                item.bar.SetDisplayFrameByPath('', elem_pnl)
            else:
                item.bar.SetDisplayFrameByPath('', DEFAULT_BLESS_BAR)
            return

    def refresh_model(self):
        if self.settle_dict:
            mecha_id = self.settle_dict.get('soul_archive').get('mecha_id', None)
            skin_id = self.settle_dict.get('soul_archive').get('mecha_fashion').get(FASHION_POS_SUIT, None)
            shiny_weapon_id = self.settle_dict.get('soul_archive').get('mecha_fashion').get(FASHION_POS_WEAPON_SFX, None)
            if mecha_id and skin_id:
                global_data.emgr.on_pve_mecha_skin_changed.emit(skin_id, shiny_weapon_id)
        return

    def destroy(self):
        self.screen_capture_helper and self.screen_capture_helper.destroy()
        self.init_params()
        self.process_event(False)