# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEBookMonsterWidget.py
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gutils.pve_lobby_utils import check_chapter_difficulty_monster_book_redpoint, check_chapter_monster_book_redpoint
from logic.gcommon.common_const.scene_const import SCENE_PVE_BOOK_WIDGET_UI
from logic.client.const.lobby_model_display_const import PVE_BOOK_WIDGET_UI
from logic.gcommon.common_const.pve_const import DIFFICULTY_TEXT_LIST, NORMAL_DIFFICUTY, DIFFICUTY_LIST, PVE_BOOK_KEY, PVE_BOOK_DEFAULT_BG_PATH
from .PVEMonsterAttributesUI import PVEMonsterAttributesUI
from .PVEBookCommonWidget import PVEBookCommonWidget
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex
import copy
DIFFICULTY_TAB_PATH = 'gui/ui_res_2/pve/catalogue/monster/btn_pve_catalogue_difficulty_{}.png'
ROTATE_FACTOR = 850

class PVEBookMonsterWidget(PVEBookCommonWidget):

    def init_params(self):
        self._cur_select_tab = None
        self._cur_select_chapter = 1
        self._cur_select_difficulty = NORMAL_DIFFICUTY
        self._cur_select_difficulty_tab = None
        self._chapter_list = []
        self._difficulty_list = []
        all_monster_conf = copy.deepcopy(confmgr.get('pve_catalogue_conf', 'MonsterBookConf', 'Content', default={}))
        self._monster_conf = {}
        self._own_monster_conf = {}
        self._is_showing_own = False
        self._all_count = 0
        self._own_count = 0
        self._cur_bg_path = PVE_BOOK_DEFAULT_BG_PATH
        self._load_model_completed = True
        self._load_scene_completed = True
        self._show_weakness = False
        book_local_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_BOOK_KEY, [])
        for conf_id, monster_conf in six_ex.items(all_monster_conf):
            if monster_conf.get('is_inner', 0) == 1 and not G_CLIENT_TRUNK:
                continue
            self._all_count += 1
            belong_chapter = monster_conf.get('belong_chapter', 1)
            belong_difficulty = monster_conf.get('belong_difficulty', 1)
            if belong_chapter not in self._chapter_list:
                self._chapter_list.append(belong_chapter)
            if belong_difficulty not in self._difficulty_list:
                self._difficulty_list.append(belong_difficulty)
            if not self._monster_conf.get(belong_chapter):
                self._monster_conf[belong_chapter] = {}
            if not self._monster_conf[belong_chapter].get(belong_difficulty):
                self._monster_conf[belong_chapter][belong_difficulty] = []
            self._monster_conf[belong_chapter][belong_difficulty].append(monster_conf)
            monster_id = monster_conf.get('monster_id')
            has_unlock = global_data.player and global_data.player.has_unlock_monster_book(monster_id)
            if has_unlock:
                monster_conf['has_unlock'] = True
                if not self._own_monster_conf.get(belong_chapter):
                    self._own_monster_conf[belong_chapter] = {}
                if not self._own_monster_conf[belong_chapter].get(belong_difficulty):
                    self._own_monster_conf[belong_chapter][belong_difficulty] = []
                self._own_monster_conf[belong_chapter][belong_difficulty].append(monster_conf)
            has_unlock_difficulty = global_data.player and global_data.player.has_unlock_difficulty_monster_book(belong_difficulty, monster_id)
            if has_unlock_difficulty:
                monster_conf['has_unlock_difficulty'] = True
                self._own_count += 1
                book_cache_key_str = '%s_%s_%s' % (monster_id, belong_chapter, belong_difficulty)
                if book_cache_key_str not in book_local_cache:
                    monster_conf['first_unlock_key'] = book_cache_key_str

        self._chapter_list.sort()
        self._difficulty_list.sort()

        def sort_function(x):
            degree = x.get('degree', 0)
            return degree

        for chapter, difficulties in six_ex.items(self._monster_conf):
            for difficulty, monster_conf in six_ex.items(difficulties):
                monster_conf.sort(key=lambda x: sort_function(x), reverse=True)

        for chapter, difficulties in six_ex.items(self._own_monster_conf):
            for difficulty, monster_conf in six_ex.items(difficulties):
                monster_conf.sort(key=lambda x: sort_function(x), reverse=True)

        for difficulty in DIFFICUTY_LIST:
            unlock_monster_info = self._own_monster_conf.get(1, {}).get(difficulty, [])
            if unlock_monster_info:
                first_unlock_monster_info = unlock_monster_info[0]
                if first_unlock_monster_info.get('has_unlock_difficulty'):
                    self._cur_select_difficulty = difficulty
                    break

        self._chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        self._monster_tag_conf = confmgr.get('pve_catalogue_conf', 'MonsterTagConf', 'Content')
        self._cur_monster_model = None
        self._is_draging_model = False
        self._rotate_timer = None
        return

    def init_ui(self):
        super(PVEBookMonsterWidget, self).init_ui()
        self._init_chapter_bar()
        self._init_difficulty_bar()
        self._init_rotate_timer()

    def init_ui_event(self):
        super(PVEBookMonsterWidget, self).init_ui_event()

        @self._panel.btn_info.unique_callback()
        def OnClick(btn, touch):
            chapter_id = self._cur_select_chapter
            if self._cur_monster_conf and chapter_id:
                PVEMonsterAttributesUI(chapter_id=chapter_id, monster_conf=self._cur_monster_conf)

        @self._panel.nd_touch.unique_callback()
        def OnBegin(btn, touch):
            self._is_draging_model = True

        @self._panel.nd_touch.unique_callback()
        def OnDrag(layer, touch):
            self._on_rotate_drag(layer, touch)

        @self._panel.nd_touch.unique_callback()
        def OnEnd(btn, touch):
            self._is_draging_model = False

        self._panel.icon_check.SetEnable(False)

        @self._panel.nd_checkbox.unique_callback()
        def OnClick(btn, touch):
            from logic.gcommon.const import MECHA_PART_MAP, MECHA_PART_NONE, MECHA_PART_HEAD
            if not self._show_weakness:
                global_data.emgr.reset_rotate_model_display.emit()
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_HEAD]})
                self._panel.icon_check.SetSelect(True)
            else:
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_NONE]})
                self._panel.icon_check.SetSelect(False)
            self._show_weakness = not self._show_weakness

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_refresh_pve_book_redpoint': self._update_chapter_btn_redpoint
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def _init_chapter_bar(self):
        list_tab = self._panel.list_tab

        def _init_chapter_btn(node, chapter_id):
            conf = self._chapter_conf.get(str(chapter_id), {})
            node.btn_tab.SetText(get_text_by_id(conf.get('title_text', '')))
            self._update_chapter_btn_redpoint(node, chapter_id)

        def _chapter_btn_click_cb(btn_tab, chapter_id, index):
            if not self._load_scene_completed or not self._load_model_completed:
                self._cur_select_tab and self._chapter_bar_wrapper.set_node_select(self._cur_select_tab)
                return
            self._cur_select_tab and self._update_chapter_btn_redpoint(self._cur_select_tab, self._cur_select_chapter)
            self._cur_select_tab = btn_tab
            self._cur_select_chapter = chapter_id
            self._cur_select_index = 0
            self._update_select()
            self._panel.list_item.ScrollToTop()
            global_data.emgr.on_refresh_pve_book_redpoint.emit()

        self._chapter_bar_wrapper = WindowTopSingleSelectListHelper()
        self._chapter_bar_wrapper.set_up_list(list_tab, self._chapter_list, _init_chapter_btn, _chapter_btn_click_cb)
        self._chapter_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def _update_chapter_btn_redpoint(self, btn_tab=None, chapter=None):
        if not btn_tab:
            btn_tab = self._cur_select_tab
        if not chapter:
            chapter = self._cur_select_chapter
        btn_tab.temp_red.setVisible(check_chapter_monster_book_redpoint(chapter))

    def _init_difficulty_bar(self):
        list_difficulty = self._panel.list_difficulty

        def _difficulty_btn_click_cb(btn_tab, difficulty, index):
            if self._cur_select_difficulty_tab:
                self._cur_select_difficulty_tab.SetShowEnable(False)
            self._cur_select_difficulty_tab = btn_tab.btn
            path = DIFFICULTY_TAB_PATH.format(difficulty - 1)
            self._cur_select_difficulty_tab.SetFrames('', [path, path, None])
            self._cur_select_difficulty_tab.SetShowEnable(True)
            self._cur_select_difficulty = difficulty
            self._update_select()
            return

        self._difficulty_bar_wrapper = WindowTopSingleSelectListHelper(btn_tab_name='btn')
        self._difficulty_bar_wrapper.set_up_list(list_difficulty, self._difficulty_list, None, _difficulty_btn_click_cb)
        self._difficulty_bar_wrapper.set_node_click(list_difficulty.GetItem(self._cur_select_difficulty - 1))
        return

    def _update_difficulty_btn(self):
        if not self._cur_conf_list:
            return
        for index, item in enumerate(self._panel.list_difficulty.GetAllItem()):
            btn = item.btn
            lab_lock = item.lab_lock
            difficulty = index + 1
            cur_conf_list = self._monster_conf.get(self._cur_select_chapter, {}).get(difficulty, {})
            cur_conf = cur_conf_list[self._cur_select_index]
            has_unlock_difficulty = cur_conf.get('has_unlock_difficulty')
            if has_unlock_difficulty:
                lab_lock.setVisible(False)
                btn.SetText(get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
            else:
                lab_lock.setVisible(True)
                lab_lock.setString(get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
                btn.SetText('')
            monster_id = cur_conf.get('monster_id')
            chapter = self._cur_select_chapter
            btn.temp_red.setVisible(check_chapter_difficulty_monster_book_redpoint(monster_id, chapter, difficulty))

    def _update_select(self):
        chapter = self._cur_select_chapter
        difficulty = self._cur_select_difficulty
        if self._is_showing_own:
            monster_conf = self._own_monster_conf if 1 else self._monster_conf
            self._cur_conf_list = monster_conf.get(chapter, {}).get(difficulty, {})
            self._update_list_item()
            self._update_difficulty_btn()
            self._cur_select_tab and self._update_chapter_btn_redpoint(self._cur_select_tab, self._cur_select_chapter)
            global_data.emgr.on_refresh_pve_book_redpoint.emit()
            self._cur_conf_list or self._panel.lab_name.setString('\xef\xbc\x9f\xef\xbc\x9f\xef\xbc\x9f')
            self._show_empty_widget()

    def _on_click_btn_choose(self, cur_index, item):
        if not self._load_scene_completed or not self._load_model_completed:
            return
        self._cur_monster_conf = self._cur_conf_list[cur_index]
        self._update_cur_select_item(item)
        self._update_monster_info()
        self._update_difficulty_btn()
        self._panel.nd_checkbox.setVisible(self._cur_monster_conf.get('has_unlock', False))

    def _update_monster_info(self):
        has_unlock_difficulty = self._cur_monster_conf.get('has_unlock_difficulty', False)
        if has_unlock_difficulty:
            monster_id = self._cur_monster_conf.get('monster_id')
            self._panel.lab_name.SetString(get_text_by_id(self._cur_monster_conf.get('name_id')))
            self._panel.lab_describe.SetString(get_text_by_id(self._cur_monster_conf['desc_id']))
            self._panel.img_item.setVisible(False)
            list_data = self._panel.list_data
            list_data.DeleteAllSubItem()
            item = list_data.AddTemplateItem(0)
            item.lab_title.SetString(get_text_by_id(860372))
            kill_monster_cnt = global_data.player.get_kill_monster_cnt(self._cur_select_difficulty, monster_id) if global_data.player else 0
            item.lab_data.SetString(str(kill_monster_cnt))
            for tag_info in self._cur_monster_conf.get('tag_list', []):
                item = list_data.AddTemplateItem()
                tag_conf = self._monster_tag_conf.get(str(tag_info[0]))
                item.lab_title.SetString(get_text_by_id(tag_conf['tag_text']))
                tag_conf = self._monster_tag_conf.get(str(tag_info[1]))
                item.lab_data.SetString(get_text_by_id(tag_conf['tag_text']))

            self._panel.btn_info.setVisible(True)
            self._update_background_texture()
        else:
            self._panel.lab_name.SetString('\xef\xbc\x9f\xef\xbc\x9f\xef\xbc\x9f')
            self._panel.lab_describe.SetString('\xef\xbc\x9f\xef\xbc\x9f\xef\xbc\x9f')
            img_item = self._panel.img_item
            img_item.SetDisplayFrameByPath('', self._cur_monster_conf.get('monster_icon'))
            node_pos = self._cur_monster_conf.get('node_pos')
            img_item.SetPosition(node_pos[0], node_pos[1])
            node_scale = self._cur_monster_conf.get('node_scale')
            img_item.setScale(node_scale)
            img_item.setVisible(True)
            list_data = self._panel.list_data
            list_data.DeleteAllSubItem()
            item = list_data.AddTemplateItem(0)
            item.lab_title.SetString(get_text_by_id(860372))
            item.lab_data.SetString('\xef\xbc\x9f\xef\xbc\x9f\xef\xbc\x9f')
            for tag_info in self._cur_monster_conf.get('tag_list', []):
                item = list_data.AddTemplateItem()
                tag_conf = self._monster_tag_conf.get(str(tag_info[0]))
                item.lab_title.SetString(get_text_by_id(tag_conf['tag_text']))
                tag_conf = self._monster_tag_conf.get(str(tag_info[1]))
                item.lab_data.SetString('\xef\xbc\x9f\xef\xbc\x9f\xef\xbc\x9f')

            self._show_empty_widget()

    def _update_background_texture(self):

        def on_load_scene(*args):
            self._load_scene_completed = True
            self._show_model()

        scene_background_texture = self._cur_monster_conf.get('background_path', PVE_BOOK_DEFAULT_BG_PATH)
        if scene_background_texture != self._cur_bg_path:
            self._cur_bg_path = scene_background_texture
            self._load_scene_completed = False
            global_data.emgr.show_lobby_relatived_scene.emit(SCENE_PVE_BOOK_WIDGET_UI, PVE_BOOK_WIDGET_UI, finish_callback=on_load_scene, update_cam_at_once=True, belong_ui_name='PVEBookWidgetUI', scene_content_type=SCENE_PVE_BOOK_WIDGET_UI, scene_background_texture=scene_background_texture)
        else:
            self._show_model()

    def _show_model(self):

        def on_load_model(model):
            self._load_model_completed = True
            self._cur_monster_model = model
            from logic.gcommon.const import MECHA_PART_MAP, MECHA_PART_NONE, MECHA_PART_HEAD
            if self._show_weakness:
                global_data.emgr.reset_rotate_model_display.emit()
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_HEAD]})
                self._panel.icon_check.SetSelect(True)
            else:
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_NONE]})
                self._panel.icon_check.SetSelect(False)

        data = {}
        data['mpath'] = self._cur_monster_conf.get('res_path', '')
        data['model_scale'] = self._cur_monster_conf.get('model_scale', 0.15)
        data['show_anim'] = self._cur_monster_conf.get('show_anim', 'idle')
        data['end_anim'] = 'idle'
        data['force_end_ani_loop'] = True
        data['off_position'] = self._cur_monster_conf.get('off_position', [-7, 10, 0])
        data['can_rotate_on_show'] = True
        data['show_sfx_model'] = True
        model_data = [
         data]
        self._load_model_completed = False
        global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_load_model)

    def _show_empty_widget(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        self._panel.btn_info.setVisible(False)
        return

    def _init_rotate_timer(self):
        self._rotate_timer = global_data.game_mgr.get_logic_timer().register(func=self._update_monster_rotate, interval=0.1, mode=CLOCK)

    def _update_monster_rotate(self):
        if self._cur_monster_model and not self._is_draging_model:
            global_data.emgr.rotate_model_display.emit(0.003)

    def show(self):
        self._update_select()
        self._panel.setVisible(True)

    def hide(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        self._panel.setVisible(False)
        return

    def destroy(self):
        super(PVEBookMonsterWidget, self).destroy()
        if self._rotate_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._rotate_timer)
            self._rotate_timer = None
        return