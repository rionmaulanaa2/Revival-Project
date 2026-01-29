# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/GetWeaponDisplayUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.gcommon.common_const.scene_const import SCENE_GET_WEAPON_DISPLAY
from logic.client.const.lobby_model_display_const import GET_WEAPON_DISPLAY
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_name, get_lobby_item_belong_no
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_weapon_skin_res
from logic.gutils.item_utils import get_item_rare_degree, get_rare_degree_name
from logic.gcommon.item import item_utility
from logic.gcommon.item.item_const import RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4, RARE_DEGREE_6
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from logic.gcommon.item.item_const import WEAPON_FASHION_PART_SUIT
import game3d
from ext_package.ext_decorator import has_skin_ext

class GetWeaponDisplayUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/get_item/get_weapon_fg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    GLOBAL_EVENT = {}
    UI_ACTION_EVENT = {'temp_close.btn_back.OnClick': '_on_click_back',
       'temp_use.btn_common_big.OnClick': '_on_click_use',
       'temp_share.btn_common_big.OnClick': 'on_click_btn_share'
       }
    BG_SHOW_ANIM = {RARE_DEGREE_2: 'show_b',
       RARE_DEGREE_3: 'show_a',
       RARE_DEGREE_4: 'show_s',
       RARE_DEGREE_6: 'show_s'
       }
    BG_LOOP_ANIM = {RARE_DEGREE_2: 'loop_b',
       RARE_DEGREE_3: 'loop_a',
       RARE_DEGREE_4: 'loop_s',
       RARE_DEGREE_6: 'loop_s'
       }
    FG_TITLE_ND = {RARE_DEGREE_2: 'b',
       RARE_DEGREE_3: 'a',
       RARE_DEGREE_4: 's',
       RARE_DEGREE_6: 's'
       }
    IOS_RES_REPLACE = {'show_b': 'show_a',
       'loop_b': 'loop_a'
       }
    FG_LABEL_IC = 'gui/ui_res_2/reward/img_%s01.png'
    FG_LABEL_IC_SPLUS = 'gui/ui_res_2/reward/img_s_plus.png'
    FG_LABEL_PNL = 'gui/ui_res_2/reward/get_weapon/%s/pnl_%s_level.png'
    LANG_RANGE = ('cn', 'jp', 'tw', 'en')
    DELAY_TAG = 20201222
    DELAY_TAG_2 = 20230116

    def on_init_panel(self, *args, **kwargs):
        super(GetWeaponDisplayUI, self).on_init_panel()
        self.init_params()
        self.process_events(True)
        self._screen_capture_helper = None
        global_data.emgr.show_new_weapon_skin += self.on_show_new_weapon
        self.hide()
        self.panel.temp_share.setVisible(global_data.is_share_show)
        return

    def init_params(self):
        self.item_no = None
        self.close_cb = None
        self.model = None
        self.model_2 = None
        self.is_used = False
        self.loaded_tag = False
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'close_share_ui_event': self.on_use_item_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def do_show_panel(self):
        super(GetWeaponDisplayUI, self).do_show_panel()
        self.process_events(True)

    def do_hide_panel(self):
        super(GetWeaponDisplayUI, self).do_hide_panel()
        self.process_events(False)

    def reset_use_item_state(self):
        self.is_used = False
        self.panel.temp_use.setVisible(True)
        self.panel.temp_share.btn_common_big.SetText(633911)

    def on_back(self):
        self._on_click_back()

    def on_use_item_success(self):
        if self.is_used:
            return
        self.is_used = True
        self.panel.temp_use.setVisible(False)
        self.panel.temp_share.btn_common_big.SetText(3155)
        global_data.game_mgr.show_tip(633912)
        self.panel.DelayCallWithTag(5, self.on_back, self.DELAY_TAG_2)

    def on_show_new_weapon(self, item_no, close_cb=None, *args, **kwargs):
        self.loaded_tag = False
        self.reset_use_item_state()
        self.item_no = item_no
        self.close_cb = close_cb
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        self.panel.PlayAnimation('appear')
        self.show()
        self.do_switch_scene()

    def do_switch_scene(self):
        new_scene_type = SCENE_GET_WEAPON_DISPLAY
        display_type = GET_WEAPON_DISPLAY

        def on_load_scene(*args):
            self.set_up_bg()
            self.set_up_title()
            self.set_up_fg()
            self.init_model(self.item_no)

        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name='GetWeaponDisplayUI')
        global_data.emgr.shutdown_box_opened_sfx.emit()

    def set_up_bg(self):
        global_data.emgr.scene_switch_background.emit('GetWeaponDisplayBG')
        bgUI = global_data.scene_background.get_ui('GetWeaponDisplayBG')
        quality = get_item_rare_degree(self.item_no)
        bgUI.panel.real_screen.nd_s.vx.setVisible(False)
        bgUI.panel.real_screen.nd_a.vx.setVisible(False)
        bgUI.panel.real_screen.nd_b.vx.setVisible(False)
        show_anim = self.BG_SHOW_ANIM.get(quality)
        loop_anim = self.BG_LOOP_ANIM.get(quality)
        show_anim = self.IOS_RES_REPLACE.get(show_anim, show_anim)
        loop_anim = self.IOS_RES_REPLACE.get(loop_anim, loop_anim)
        bgUI.play_anim(show_anim, loop_anim)
        bgUI.start_render()

    def set_up_title(self):
        cur_lang = get_cur_lang_name()
        if cur_lang not in self.LANG_RANGE:
            cur_lang = 'en'
        self.nd_lang = getattr(self.panel, 'nd_%s' % cur_lang)
        self.nd_lang.setVisible(True)
        quality = get_item_rare_degree(self.item_no)
        self.nd_title = getattr(self.nd_lang, self.FG_TITLE_ND.get(quality))
        self.nd_title.setVisible(True)
        self.nd_title.PlayAnimation('show')
        self.nd_title.PlayAnimation('loop_liz')

    def set_up_fg(self):
        quality = get_item_rare_degree(self.item_no)
        quality = self.FG_TITLE_ND.get(quality)
        self.nd_fg = global_data.uisystem.load_template_create('common/get_item/i_%s_fg' % quality, self.panel.vx_loop)
        self.nd_fg.PlayAnimation('loop')

    def init_model(self, item_no):

        def do_show_model():
            if self.model and self.model.valid:
                self.model.visible = True
            if self.model_2 and self.model_2.valid:
                self.model_2.visible = True
            self.loaded_tag = True

        def on_load_model(model, *args):
            if not self.model:
                self.model = model
                self.set_up_lable()
                global_data.sound_mgr.play_ui_sound('luckball_show')
            else:
                self.model_2 = model
            model.visible = False
            self.panel.DelayCallWithTag(0.3, do_show_model, self.DELAY_TAG)

        item_type = get_lobby_item_type(item_no)
        if not has_skin_ext():
            self.loaded_tag = True
        b_show_model = item_type in (L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN)
        if b_show_model and item_type in [L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN]:
            model_data = get_lobby_model_data(item_no, is_get_player_data=False)
            for data in model_data:
                scl = data['model_scale']
                data['model_scale'] = scl * 1.2

            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_load_model)
        else:
            self.loaded_tag = True

    def use_item(self):
        if not self.item_no:
            return
        fashion_dict = {WEAPON_FASHION_PART_SUIT: self.item_no}
        belong_no = get_lobby_item_belong_no(self.item_no)
        global_data.player and global_data.player.try_dress_battle_item_fashion(str(belong_no), fashion_dict)

    def set_up_lable(self):
        quality = get_item_rare_degree(self.item_no)
        if quality == RARE_DEGREE_6:
            quality = self.FG_TITLE_ND.get(quality)
            icon_path = self.FG_LABEL_IC_SPLUS
        else:
            quality = self.FG_TITLE_ND.get(quality)
            icon_path = self.FG_LABEL_IC % quality
        panel_path = self.FG_LABEL_PNL % (quality, quality)
        self.panel.nd_label.img_level.SetDisplayFrameByPath('', icon_path)
        self.panel.nd_label.lab_text.nd_auto_fit.img_bar.SetDisplayFrameByPath('', panel_path)
        item_type = get_lobby_item_type(self.item_no)
        skin_items = global_data.player.get_items_by_type_list([L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN])
        rare_degree = get_item_rare_degree(self.item_no)
        target_skins = item_utility.get_item_rare_degree_count(skin_items, target_rare_degrees=[rare_degree])
        rare_degree_name = get_rare_degree_name(rare_degree)
        self.panel.lab_item_info.SetString(get_text_by_id(83212, {'num': len(target_skins),'level': rare_degree_name}))
        belong_id = get_lobby_item_belong_no(self.item_no)
        belong_name = get_lobby_item_name(belong_id)
        name = get_lobby_item_name(self.item_no)
        self.panel.nd_label.lab_text.SetString(belong_name + '\xc2\xb7' + name)
        self.panel.PlayAnimation('show')

    def _on_click_use(self, *args):
        self.use_item()
        self.on_use_item_success()

    def _on_click_back(self, *args):
        if not self.loaded_tag:
            return
        self.hide()

        def cache_specific_reward_showed_callback():
            global_data.emgr.change_model_display_control_type.emit(None)
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            self.show_main_ui()
            if self.close_cb:
                func = self.close_cb
                self.close_cb = None
                func()
            else:
                from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
                ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
                if not ui and not (global_data.player and global_data.player.is_in_battle()):
                    ReceiveRewardUI()
                global_data.emgr.show_cache_generic_reward.emit()
            global_data.emgr.leave_get_model_display_ui.emit()
            return

        from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
        ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        if not ui and not (global_data.player and global_data.player.is_in_battle()):
            ReceiveRewardUI()
        global_data.emgr.show_cache_specific_reward.emit(self.item_no, cache_specific_reward_showed_callback)
        self.init_params()
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.panel.stopActionByTag(self.DELAY_TAG_2)

    def on_finalize_panel(self):
        self.init_params()
        self.process_events(False)
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.panel.stopActionByTag(self.DELAY_TAG_2)
        self.destroy_widget('_screen_capture_helper')
        if global_data.scene_background:
            bgUI = global_data.scene_background.get_ui('GetWeaponDisplayBG')
            bgUI and bgUI.stop_render()
        super(GetWeaponDisplayUI, self).on_finalize_panel()

    def on_click_btn_share(self, btn, touch):
        if not self.loaded_tag:
            return
        if not self._screen_capture_helper:
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            self._screen_capture_helper = ScreenFrameHelper()
        name_list = [
         self.__class__.__name__, 'GetWeaponDisplayBG']
        if self._screen_capture_helper:

            def custom_cb(*args):
                self.use_item()
                self.panel.nd_func.setVisible(True)

            self.panel.nd_func.setVisible(False)
            bgUI = global_data.scene_background.get_ui('GetWeaponDisplayBG')
            if bgUI:
                ani_names = bgUI.panel.GetAnimationNameList()
                for ani_name in ani_names:
                    if bgUI.panel.IsPlayingAnimation(ani_name):
                        bgUI.panel.FastForwardToAnimationTime(ani_name, bgUI.panel.GetAnimationMaxRunTime(ani_name))

            if self.nd_title:
                self.nd_title.FastForwardToAnimationTime('show', self.nd_title.GetAnimationMaxRunTime('show'))
            self._screen_capture_helper.take_screen_shot(name_list, self.panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1')