# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/LobbySkinPreViewUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_0, UI_VKB_CLOSE
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_WALL_PICTURE
from logic.gutils.template_utils import init_price_view
from logic.client.const import mall_const
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gutils import dress_utils
from common.cfg import confmgr
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget, PAYMENT_MEOW_COIN
import logic.gcommon.const as gconst
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips
if G_IS_NA_PROJECT:
    TYPE_TO_TEXTID = {L_ITEM_TYPE_LOBBY_SKIN: 18270,L_ITEM_TYPE_MECHA_SP_ACTION: 82225,L_ITEM_TYPE_MUSIC: 12185,
       L_ITEM_TYPE_WALL_PICTURE: 80934
       }
else:
    TYPE_TO_TEXTID = {L_ITEM_TYPE_LOBBY_SKIN: 18270,L_ITEM_TYPE_MECHA_SP_ACTION: 82225,
       L_ITEM_TYPE_MUSIC: 12185
       }

@show_with_japan_shopping_tips
class LobbySkinPreViewUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/lobby_skin_preview'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_0
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_back.OnClick': 'close',
       'btn_left.OnClick': 'btn_left_click',
       'btn_right.OnClick': 'btn_right_click'
       }
    GLOBAL_EVENT = {'housesys_wall_picture_change_success': 'refresh_item_info',
       'miaomiao_lobby_skin_change_success': 'refresh_item_info',
       'lobby_bgm_change_success': 'refresh_item_info',
       'player_item_update_event': '_on_item_update',
       'set_mecha_pose_result_event': '_on_item_update',
       'del_mecha_pose_result_event': '_on_item_update'
       }
    EXCEPTIONS_UI = [
     'LobbyRockerUI', 'MoveRockerUI']

    def on_init_panel(self, item_no, show_types):
        self.item_no_to_goods_id = {}
        self.cache_show_count = {}
        self.item_no = int(item_no)
        if show_types is None:
            if G_IS_NA_PROJECT:
                self.show_types = (
                 L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_WALL_PICTURE)
            else:
                self.show_types = (
                 L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_MUSIC)
        else:
            self.show_types = show_types
        self.item_no_index = -1
        self.hide_main_ui(exceptions=self.EXCEPTIONS_UI)
        self.price_top_widget = None
        self.init_lobby_skin_info()
        self.return_lobby_scene()
        self.refresh_item_info()
        return

    def init_lobby_skin_info(self):
        item_page_conf = confmgr.get('mall_page_config', str(mall_const.MEOW_ID), default={})
        goods_items = item_page_conf.get(mall_const.NONE_ID, [])
        goods_ids = mall_utils.sort_meow_goods_ids(goods_items)
        self.item_ids = []
        for goods_id in goods_ids:
            item_no = mall_utils.get_goods_item_no(goods_id)
            self.item_no_to_goods_id[item_no] = goods_id
            item_type = item_utils.get_lobby_item_type(item_no)
            if item_type in self.show_types:
                self.item_ids.append(item_no)

        if L_ITEM_TYPE_LOBBY_SKIN in self.show_types:
            from logic.gcommon.item import item_const as iconst
            self.item_ids.append(iconst.DEFAULT_LOBBY_SKIN)
        self.goods_id = self.item_no_to_goods_id.get(self.item_no)

    def select_item_no(self, item_no):
        self.item_no = int(item_no)
        self.goods_id = self.item_no_to_goods_id.get(self.item_no)
        self.refresh_item_info()

    def _on_item_update(self, *args):
        self.refresh_item_info(refresh_model=False)

    def refresh_item_info(self, refresh_model=True):
        if not self.item_no:
            return
        if self.item_no_index < len(self.item_ids):
            if self.item_no_index < 0:
                try:
                    self.item_no_index = self.item_ids.index(int(self.item_no))
                except:
                    self.item_no_index = -1

            elif self.item_ids[self.item_no_index] != self.item_no:
                try:
                    self.item_no_index = self.item_ids.index(int(self.item_no))
                except:
                    self.item_no_index = -1

        self.refresh_switch_btn()
        item_type = item_utils.get_lobby_item_type(self.item_no)
        is_owned = mall_utils.item_has_owned_by_item_no(self.item_no)
        can_jump = item_utils.can_jump_to_ui(self.item_no)
        jump_txt = item_utils.get_item_access(self.item_no)
        self.panel.btn_use.setVisible(True)
        self.panel.btn_dismount.setVisible(False)
        self.panel.lab_get_method.setVisible(False)
        self.panel.temp_price.setVisible(False)
        self.panel.btn_use.btn_common.SetEnable(True)
        self.panel.btn_use.btn_common.lab_btn.setVisible(False)
        self.panel.lab_title.SetString(TYPE_TO_TEXTID.get(item_type))
        is_using = False
        if is_owned:
            if item_type == L_ITEM_TYPE_LOBBY_SKIN:
                cur_miaomiao_item_no = global_data.player.get_lobby_skin()
                is_using = cur_miaomiao_item_no == self.item_no
            elif item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
                mecha_pose_data = global_data.player.get_mecha_pose()
                mecha_item_id = item_utils.get_lobby_item_belong_no(self.item_no)
                pose_item_no = mecha_pose_data.get(str(mecha_item_id))
                is_using = pose_item_no == self.item_no
            elif item_type == L_ITEM_TYPE_MUSIC:
                cur_bgm_item_no = global_data.player.get_lobby_bgm()
                is_using = cur_bgm_item_no == self.item_no
            elif item_type == L_ITEM_TYPE_WALL_PICTURE:
                cur_wall_pic_item_no = global_data.player.get_wall_picture()
                is_using = cur_wall_pic_item_no == self.item_no
            self.panel.btn_use.btn_common.lab_btn.setVisible(True)
            if is_using:
                self.panel.btn_dismount.setVisible(True)
                self.panel.btn_use.setVisible(False)
                no_unload = item_type in (L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_WALL_PICTURE)
                self.panel.btn_dismount.btn_common.SetEnable(not no_unload)
                self.panel.btn_dismount.btn_common.SetText(2213 if no_unload else 81247)
            else:
                self.panel.btn_use.btn_common.lab_btn.SetString(80338)
        elif self.goods_id:
            self.panel.temp_price.setVisible(True)
            init_price_view(self.panel, self.goods_id, color=mall_const.DARK_PRICE_COLOR)
        elif can_jump:
            self.panel.btn_use.btn_common.lab_btn.setVisible(True)
            self.panel.btn_use.btn_common.lab_btn.SetString(2222)
            if jump_txt:
                self.panel.lab_get_method.SetString(jump_txt)
                self.panel.lab_get_method.setVisible(True)
        else:
            self.panel.btn_use.setVisible(False)
        self.panel.temp_item.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(self.item_no))
        name_str = item_utils.get_lobby_item_name(self.item_no)
        self.panel.temp_item.lab_name.SetString(name_str)
        self.panel.img_base.setVisible(item_type == L_ITEM_TYPE_MECHA_SP_ACTION)
        if item_type == L_ITEM_TYPE_MUSIC:
            self.panel.txt_song_tltle.setVisible(True)
            self.panel.lab_song_name.setVisible(True)
            self.panel.lab_title.setVisible(False)
            self.panel.lab_skin_name.setVisible(False)
            self.panel.lab_song_name.setVisible(True)
            self.panel.lab_song_name.SetString(name_str)
        else:
            self.panel.txt_song_tltle.setVisible(False)
            self.panel.lab_song_name.setVisible(False)
            self.panel.lab_song_name.setVisible(False)
            self.panel.lab_title.setVisible(True)
            self.panel.lab_skin_name.setVisible(True)
            self.panel.lab_skin_name.SetString(name_str)

        @self.btn_dismount.btn_common.unique_callback()
        def OnClick(btn, touch, item_type=item_type):
            if global_data.player:
                if item_type == L_ITEM_TYPE_LOBBY_SKIN:
                    global_data.player.change_lobby_skin(0)
                elif item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
                    mecha_item_id = item_utils.get_lobby_item_belong_no(self.item_no)
                    global_data.player.try_del_mecha_pose(mecha_item_id)
                elif item_type == L_ITEM_TYPE_MUSIC:
                    pass
                elif item_type == L_ITEM_TYPE_WALL_PICTURE:
                    pass

        @self.btn_use.btn_common.unique_callback()
        def OnClick(btn, touch, is_owned=is_owned, can_jump=can_jump, item_type=item_type):
            if is_owned:
                if global_data.player and self.item_no:
                    if item_type == L_ITEM_TYPE_LOBBY_SKIN:
                        global_data.player.change_lobby_skin(self.item_no)
                    elif item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
                        mecha_item_id = item_utils.get_lobby_item_belong_no(self.item_no)
                        global_data.player.try_set_mecha_pose(mecha_item_id, self.item_no)
                    elif item_type == L_ITEM_TYPE_MUSIC:
                        global_data.player.select_lobby_bgm(self.item_no)
                    elif item_type == L_ITEM_TYPE_WALL_PICTURE:
                        global_data.player.select_wall_picture(self.item_no)
            elif self.goods_id:
                prices = mall_utils.get_mall_item_price(self.goods_id)
                if not prices:
                    return
                price_info = prices[0]
                goods_payment = price_info.get('goods_payment')
                real_price = price_info.get('real_price')
                limit = mall_utils.limite_pay(self.goods_id)
                if limit:
                    return

                def _pay():
                    global_data.player.buy_goods(self.goods_id, 1, goods_payment)
                    global_data.player.sa_log_anniversary_gift_state_buy(self.goods_id)

                if not mall_utils.check_payment(goods_payment, real_price, cb=_pay):
                    return
                from logic.gutils.mall_buy_confirm_func import goods_buy_need_confirm
                if goods_buy_need_confirm(self.goods_id, call_back=_pay):
                    return
                _pay()
            elif can_jump:
                item_utils.jump_to_ui(self.item_no)

        if refresh_model:
            if item_type == L_ITEM_TYPE_LOBBY_SKIN:
                self.restore_model_animation()
                self.restore_lobby_bgm()
                self.restore_wall_pic()
                global_data.emgr.miaomiao_lobby_skin_change_force.emit(self.item_no)
            elif item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
                self.restore_lobby_skin()
                self.restore_lobby_bgm()
                self.restore_wall_pic()
                mecha_item_id = item_utils.get_lobby_item_belong_no(self.item_no)
                mecha_id = dress_utils.mecha_lobby_id_2_battle_id(mecha_item_id)
                dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(mecha_item_id=mecha_item_id)
                if not dressed_clothing_id:
                    dressed_clothing_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_id), 'default_fashion')[0]
                global_data.emgr.preview_change_display_model.emit(mecha_id, dressed_clothing_id, self.item_no)
            elif item_type == L_ITEM_TYPE_MUSIC:
                self.restore_model_animation()
                self.restore_lobby_skin()
                self.restore_wall_pic()
                music = item_utils.get_lobby_item_res_path(self.item_no) or 'bar'
                global_data.sound_mgr.play_music(music)
            elif item_type == L_ITEM_TYPE_WALL_PICTURE:
                self.restore_model_animation()
                self.restore_lobby_skin()
                self.restore_lobby_bgm()
                global_data.emgr.housesys_wall_picture_change.emit(self.item_no)

    def return_lobby_scene(self):
        for i in range(len(global_data.ex_scene_mgr_agent.scene_stack)):
            global_data.emgr.leave_current_scene.emit()

        global_data.emgr.reset_rotate_model_display.emit()

    def on_finalize_panel(self):
        self.recover_ui_show_count()
        self.restore_lobby_skin()
        self.restore_model_animation()
        self.restore_lobby_bgm()
        self.restore_wall_pic()
        self.show_main_ui()
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        return

    def cache_ui_show_count(self):
        for ui_name in self.EXCEPTIONS_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                self.cache_show_count[ui_name] = ui.get_show_count_dict()
                ui.clear_show_count_dict()

    def recover_ui_show_count(self):
        if not self.cache_show_count:
            return
        for ui_name in self.EXCEPTIONS_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                show_count = ui.get_show_count_dict()
                show_count.update(self.cache_show_count.get(ui_name))
                ui.set_show_count_dict(show_count)

        self.cache_show_count = {}

    def do_show_panel(self):
        super(LobbySkinPreViewUI, self).do_show_panel()
        self.return_lobby_scene()
        self.cache_ui_show_count()

    def do_hide_panel(self):
        super(LobbySkinPreViewUI, self).do_hide_panel()
        self.recover_ui_show_count()
        self.restore_lobby_skin()
        self.restore_model_animation()
        self.restore_lobby_bgm()
        self.restore_wall_pic()

    def restore_lobby_skin(self):
        global_data.emgr.miaomiao_lobby_skin_change.emit(-1)

    def restore_model_animation(self):
        global_data.emgr.preview_change_display_model.emit()

    def restore_lobby_bgm(self):
        global_data.emgr.lobby_bgm_change.emit(-1)

    def restore_wall_pic(self):
        global_data.emgr.housesys_wall_picture_change.emit()

    def refresh_switch_btn(self):
        self.panel.btn_left.setVisible(self.item_no_index > 0)
        self.panel.btn_right.setVisible(self.item_no_index >= 0 and self.item_no_index < len(self.item_ids) - 1)

    def btn_left_click(self, *args, **kargs):
        self.item_no_index -= 1
        if self.item_no_index >= 0:
            self.select_item_no(int(self.item_ids[self.item_no_index]))

    def btn_right_click(self, *args, **kargs):
        self.item_no_index += 1
        if self.item_no_index < len(self.item_ids):
            self.select_item_no(int(self.item_ids[self.item_no_index]))