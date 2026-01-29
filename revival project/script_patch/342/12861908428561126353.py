# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinImproveWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import math3d
import cc
from common.cfg import confmgr
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gutils import mecha_skin_utils
from logic.gutils.template_utils import init_price_template
from logic.gutils import lobby_model_display_utils
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.archive.archive_manager import ArchiveManager
from common.platform.dctool import interface
from logic.gcommon.const import SHOP_PAYMENT_SS_SKIN_CHIP, SHOP_PAYMENT_SPLUS_SKIN_CHIP, EX_SKIN_IMPROVE_RED_POINT_KEY
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from logic.gutils.mecha_utils import ProjectionKillModel, get_ex_skin_improve_item_no
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.gcommon.const import SHOP_PAYMENT_DIANCANG_TICKET_INHERIT
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
MECHA_PREVIEW = 0
HONER_COUNT = 1
PROJECTION_KILL = 2
AILAND_SUMMON = 3

class SkinImproveWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, select_cb, close_cb, glass_cb, show_cb, init_cam_offset_dist):
        self.global_events = {'player_item_update_event_with_id': self._on_buy_good_success,
           'role_fashion_chagne': self._on_role_fashion_change
           }
        super(SkinImproveWidget, self).__init__(parent_ui, panel)
        self._parent_ui = parent_ui
        self._select_callback = select_cb
        self._close_cb = close_cb
        self._glass_cb = glass_cb
        self._show_cb = show_cb
        self._previewing_id = None
        self._cur_clothing_id = None
        self._selected_item = None
        self._using_item = None
        self._mecha_id = None
        self._is_previewing = False
        self._is_equip_shiny = False
        self._archive_data = ArchiveManager().get_archive_data('guide')
        self._can_ex_improve = False
        self._honer_count_item_no = None
        self._projection_kill_item_no = None
        self._nd_tab = panel.nd_tab
        self._ex_skin_id_list = []
        self._tab_btn_list = []
        self._tab_list = {MECHA_PREVIEW: {'text': 83413,'unlock_text': '','tips_text': '','tips_text2': ''},HONER_COUNT: {'text': 83414,'unlock_text': 83415,'tips_text': 83423,'tips_text2': 83426},PROJECTION_KILL: {'text': 83416,'unlock_text': 83417,'tips_text': 83424,'tips_text2': 83427},AILAND_SUMMON: {'text': 83418,'unlock_text': 83419,'tips_text': 83425,'tips_text2': 83428}}
        self._current_select_index = None
        self._selected_ex_index = None
        self._archive_data = global_data.achi_mgr.get_general_archive_data()
        self._projection_kill_model = None
        self._cam_postiion_bounds = (None, None, 0.0)
        self._double_touch_prev_len = 0.0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self._cur_cam_offset_distance = init_cam_offset_dist
        self._has_done_first_scene_thing = False
        self._video_url = None
        self._video_player_type = False
        self.is_s_upgradable = False
        self.panel.setVisible(True)
        self.panel.RecordAnimationNodeState('ex')
        self.panel.RecordAnimationNodeState('ex_before')
        self.panel.RecordAnimationNodeState('appear')
        self.on_init_panel()
        self.is_ex_step_promote = False
        self.ex_step_widget = None
        self.init_ex_step()
        return

    def set_closing_id(self, mecha_id, clothing_id):
        self._mecha_id = mecha_id
        self._previewing_id = clothing_id
        self._cur_clothing_id = clothing_id
        self._is_previewing = False
        self._is_equip_shiny = False
        self._skin_id_lst = mecha_skin_utils.get_mecha_ss_skin_lst(self._previewing_id)
        is_s_upgradable = mecha_skin_utils.is_s_skin_that_can_upgrade(self._previewing_id)
        self.is_s_upgradable = is_s_upgradable
        if not is_s_upgradable:
            money_type_lst = [
             mall_utils.get_item_money_type(SHOP_PAYMENT_SS_SKIN_CHIP)]
            self.panel.nd_improve.nd_ex.lab_title.SetString(608114)
            self.panel.temp_ex.img_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/img_ex.png')
        else:
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(self._cur_clothing_id))
            required_item, _ = skin_cfg.get('required_item')
            money_type_lst = [mall_utils.get_item_money_type(required_item)]
            self._skin_id_lst = [self._previewing_id]
            self.panel.nd_improve.nd_ex.lab_title.SetString(611293)
            self.panel.temp_ex.img_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_s_plus.png')
        self.price_top_widget.show_money_types(money_type_lst)
        if not self.panel.isVisible():
            self.panel.RecoverAnimationNodeState('appear')
            self.panel.PlayAnimation('appear')
        self.panel.setVisible(True)
        self._disappearing = False
        self.is_sp = len(self._skin_id_lst) == 2
        self.panel.nd_card_sp.setVisible(self.is_sp)
        self.panel.nd_card.setVisible(not self.is_sp)
        self.init_ex_skin_improve()
        self.init_ex_step()
        self._re_init_panel()
        self.refresh_model_show()
        self.init_mecha_name()
        self.refresh_btn_show_state()

    def refresh_model_show(self):
        if self._mecha_id and self._previewing_id:
            if self._is_previewing:
                shiny_id = self.get_preview_shiny_id(self._previewing_id)
            else:
                shiny_id = None
            self._select_callback(self._mecha_id, self._previewing_id, shiny_id, is_refresh=True)
            if self._can_ex_improve:
                self._update_list_tab()
        return

    def get_preview_shiny_id(self, cid):
        if not self.is_ex_step_promote:
            shiny_id = self.mecha_skin_conf.get(str(cid), {}).get('weapon_sfx_id')
        else:
            shiny_id = 0
            if self.ex_step_widget:
                shiny_id = self.ex_step_widget.get_preview_shiny_id(cid)
        return shiny_id

    def on_init_panel--- This code section failed: ---

 166       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'mecha_conf'
           9  LOAD_CONST            2  'SkinConfig'
          12  LOAD_CONST            3  'Content'
          15  CALL_FUNCTION_3       3 
          18  LOAD_FAST             0  'self'
          21  STORE_ATTR            2  'mecha_skin_conf'

 167      24  LOAD_GLOBAL           3  'PriceUIWidget'
          27  LOAD_GLOBAL           4  'panel'
          30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             4  'panel'
          36  LOAD_ATTR             5  'list_price'
          39  CALL_FUNCTION_257   257 
          42  LOAD_FAST             0  'self'
          45  STORE_ATTR            6  'price_top_widget'

 169      48  LOAD_FAST             0  'self'
          51  LOAD_ATTR             7  '_init_ui_event'
          54  CALL_FUNCTION_0       0 
          57  POP_TOP          

 170      58  LOAD_FAST             0  'self'
          61  LOAD_ATTR             8  'init_btn_glass'
          64  CALL_FUNCTION_0       0 
          67  POP_TOP          

 171      68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             9  'init_btn_show'
          74  CALL_FUNCTION_0       0 
          77  POP_TOP          

 173      78  LOAD_FAST             0  'self'
          81  LOAD_ATTR            10  'init_temp_btn_show'
          84  CALL_FUNCTION_0       0 
          87  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 39

    def destroy(self):
        self._parent_ui = None
        self.panel.setVisible(False)
        self.panel = None
        self._close_cb = None
        self._glass_cb = None
        self._mecha_id = None
        self._using_item = None
        self._selected_item = None
        self._previewing_id = None
        self._select_callback = None
        self._can_ex_improve = None
        self._honer_count_item_no = None
        self._projection_kill_item_no = None
        self._nd_tab = None
        self._ex_skin_id_list = None
        self._tab_btn_list = None
        self._tab_list = None
        self._current_select_index = None
        self._selected_ex_index = None
        self._archive_data = None
        if self._projection_kill_model:
            self._projection_kill_model.destroy()
            self._projection_kill_model = None
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        self._video_url = None
        self.ex_step_widget and self.ex_step_widget.destroy()
        self.ex_step_widget = None
        super(SkinImproveWidget, self).destroy()
        return

    def _re_init_panel(self):
        self._is_equip_shiny = False
        for skin_id in self._skin_id_lst:
            shiny_id = mecha_skin_utils.get_mecha_skin_shiny_id(skin_id)
            if shiny_id:
                self._is_equip_shiny = True
                break

        for idx, c_id in enumerate(self._skin_id_lst):
            self._init_card_with_ss(c_id, idx)

        for idx in range(len(self._skin_id_lst), 3):
            self._init_card_with_no_ss(idx)

        self._init_shiny_weapon_status()
        cur_mecha_item_id = dress_utils.battle_id_to_mecha_lobby_id(self._mecha_id)
        mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
        self._set_previewing_node(self._previewing_id)
        if mecha_item_data is not None:
            fashion_data = mecha_item_data.get_fashion()
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            self._set_using_node(dressed_clothing_id)
        self.update_ex_step_widget()
        return

    def _get_nd_card(self):
        if self.is_sp:
            return self.panel.nd_card_sp
        return self.panel.nd_card

    def _get_skin_node(self, c_id):
        idx = self._skin_id_lst.index(c_id)
        card_node = getattr(self._get_nd_card(), 'temp_card_%s' % (idx + 1))
        return card_node

    def _init_card_with_ss(self, c_id, idx):
        card_node = getattr(self._get_nd_card(), 'temp_card_%s' % (idx + 1))
        if not card_node:
            return
        else:
            card_node.temp_card.nd_card.c_id = c_id
            item_utils.init_skin_card(card_node.temp_card, c_id)
            if self.is_s_upgradable:
                card_node.temp_card.img_ex.setVisible(False)
            else:
                card_node.temp_card.img_ex.setVisible(True)
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(c_id))
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                card_node.temp_card.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
            name_text = item_utils.get_lobby_item_name(c_id)
            card_node.temp_card.lab_skin_name.setString(name_text)
            item_utils.check_skin_tag(card_node.temp_card.nd_kind, c_id)
            self._update_status(idx, card_node, c_id)
            return

    def _init_card_with_no_ss(self, idx):
        base_skin_id = self._skin_id_lst[0]
        if self.is_s_upgradable:
            base_skin_id = self._previewing_id
        card_node = getattr(self._get_nd_card(), 'temp_card_%s' % (idx + 1))
        if not card_node:
            return
        else:
            item_utils.set_skin_card_frame(base_skin_id, card_node.temp_card)
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(base_skin_id))
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                card_node.temp_card.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
            card_node.temp_btn_use.setVisible(False)
            card_node.lab_no_upgrade.setVisible(True)
            card_node.icon_ban.setVisible(True)
            card_node.temp_card.img_skin.SetColor('#SK')
            card_node.temp_card.nd_kind.setVisible(False)
            card_node.temp_card.lab_skin_name.setVisible(False)
            card_node.lab_get_method.setVisible(False)
            img_arrow_node = getattr(self._get_nd_card(), 'img_arrow%s' % idx)
            if img_arrow_node:
                img_arrow_node.setVisible(False)
            card_node.temp_card.nd_card.UnBindMethod('OnClick')
            return

    def _update_status(self, idx, c_node, c_id):
        clothing_data = global_data.player.get_item_by_no(c_id)
        btn_use = c_node.temp_btn_use
        c_node.lab_title.setString(get_text_by_id(608108).format(idx + 1))
        c_node.temp_card.nd_card.BindMethod('OnClick', self._on_click_card)
        c_node.btn_go.SetEnable(False)
        c_node.btn_go.setVisible(False)
        if clothing_data is None:
            btn_use.setVisible(True)
            c_node.nd_get.setVisible(False)
            c_node.lab_get_method.setVisible(True)
            c_node.temp_card.nd_lock.setVisible(True)
            btn_use.btn_common.SetEnable(True)
            if idx > 0 and not self.is_s_upgradable:
                if self.is_sp:
                    c_node.lab_get_method.setString(get_text_by_id(635125))
                else:
                    c_node.lab_get_method.setString(get_text_by_id(608109).format(idx))
                before_cid = self._skin_id_lst[idx - 1]
                info = global_data.player.get_item_by_no(before_cid)
                btn_use.btn_common.SetEnable(False)
                btn_use.temp_cost.setVisible(True)
                btn_use.btn_common.SetText('')
                required_item, required_num = self._init_price(before_cid, btn_use.temp_cost)
                if info:
                    btn_use.btn_common.SetEnable(True)

                    @btn_use.btn_common.unique_callback()
                    def OnClick(btn, touch, c_id=c_id, before_cid=before_cid, pay_item=required_item, pay_num=required_num):
                        if global_data.player and mall_utils.check_item_money(pay_item, pay_num, pay_tip=False):
                            if not self.is_ex_step_promote:
                                global_data.player.try_upgrade_mecha_fashion(before_cid)
                            else:
                                from logic.gcommon.common_const.mecha_const import EX_REFINE_UPGRADE_TYPE_COLOR
                                base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(before_cid)
                                global_data.player.call_server_method('try_refined_upgrade_mecha_fashion', (base_skin_id, EX_REFINE_UPGRADE_TYPE_COLOR, c_id))
                        else:
                            self._jump_to_lottery(required_item, required_num)

                else:
                    c_node.btn_go.SetEnable(True)
                    c_node.btn_go.setVisible(True)

                    @c_node.btn_go.unique_callback()
                    def OnClick(*args):
                        global_data.game_mgr.show_tip(get_text_by_id(608116))

            else:
                jump_txt = item_utils.get_item_access(str(c_id))
                c_node.lab_get_method.SetString(jump_txt)
                btn_use.temp_cost.setVisible(False)
                if item_utils.can_jump_to_ui(str(c_id)):
                    btn_use.btn_common.SetText(get_text_by_id(2222))
                    btn_use.btn_common.SetEnable(True)

                    @btn_use.btn_common.unique_callback()
                    def OnClick(btn, touch, clothing_id=c_id):
                        item_utils.jump_to_ui(str(clothing_id))

                else:
                    btn_use.btn_common.SetText(get_text_by_id(80828))
                    btn_use.btn_common.SetEnable(False)
        else:
            btn_use.setVisible(False)
            c_node.nd_get.setVisible(True)
            c_node.lab_get_method.setVisible(False)
            c_node.temp_card.nd_lock.setVisible(False)
        return

    def _init_shiny_weapon_status(self):
        if not self.is_ex_step_promote:
            self._is_previewing = False
        else:
            preview_shiny_id = self.parent.get_shiny_id()
            if self._is_previewing and preview_shiny_id:
                preview_shiny_rarity = mecha_skin_utils.get_shiny_rarity_with_same_group_skin(self._cur_clothing_id, preview_shiny_id)
                cur_equip = mecha_skin_utils.get_mecha_skin_shiny_id(self._previewing_id)
                equip_shiny_rarity = mecha_skin_utils.get_shiny_rarity_with_same_group_skin(self._cur_clothing_id, cur_equip)
                self._is_previewing = preview_shiny_rarity != equip_shiny_rarity
            else:
                self._is_previewing = False
        before_cid = self._skin_id_lst[-1]
        nd_activate = self.panel.nd_improve.nd_ex.nd_activate
        btn_use = nd_activate.temp_btn_use
        first_shiny_weapon_id = self.mecha_skin_conf.get(str(self._skin_id_lst[0]), {}).get('weapon_sfx_id')
        self.panel.nd_improve.nd_ex.nd_ex.nd_using.setVisible(False)
        self.panel.nd_improve.nd_ex.nd_ex.nd_choose.setVisible(False)
        nd_activate.btn_go.SetEnable(False)
        nd_activate.btn_go.setVisible(False)
        if not global_data.player or not global_data.player.get_item_by_no(first_shiny_weapon_id):
            nd_activate.setVisible(True)
            self.panel.nd_improve.nd_ex.nd_get.setVisible(False)
            self.panel.nd_improve.nd_ex.nd_ex.nd_lock.setVisible(True)
            self.panel.nd_improve.nd_ex.nd_ex.nd_view.setVisible(True)
            btn_use.temp_cost.setVisible(True)
            btn_use.btn_major.SetText('')
            pay_item, pay_num = self._init_price(before_cid, btn_use.temp_cost)
            if pay_item == SHOP_PAYMENT_SS_SKIN_CHIP:
                if self.is_sp:
                    nd_activate.lab_get_method.SetString(635135)
                else:
                    nd_activate.lab_get_method.SetString(633730)
            else:
                nd_activate.lab_get_method.SetString('')
            info = global_data.player.get_item_by_no(before_cid)
            if info:
                enable_btn = True if 1 else False
                btn_use.btn_major.SetEnable(enable_btn)
                if enable_btn:

                    @btn_use.btn_major.unique_callback()
                    def OnClick(*args):
                        if global_data.player and mall_utils.check_item_money(pay_item, pay_num, pay_tip=False):
                            global_data.player.try_upgrade_mecha_fashion(before_cid)
                        else:
                            self._jump_to_lottery(pay_item, pay_num)

                info or nd_activate.btn_go.SetEnable(True)
                nd_activate.btn_go.setVisible(True)

                @nd_activate.btn_go.unique_callback()
                def OnClick(*args):
                    if not self.is_s_upgradable:
                        global_data.game_mgr.show_tip(get_text_by_id(608118))
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(611300))

            @self.panel.nd_improve.nd_ex.nd_ex.unique_callback()
            def OnClick(*args):
                self.try_preview()

        else:
            nd_activate.setVisible(False)
            self.panel.nd_improve.nd_ex.nd_get.setVisible(True)
            self.panel.nd_improve.nd_ex.nd_ex.nd_lock.setVisible(False)
            self.panel.nd_improve.nd_ex.nd_ex.nd_view.setVisible(False)
            self.panel.nd_improve.nd_ex.nd_ex.nd_using.setVisible(self._is_equip_shiny)
            self._play_animation(self._is_equip_shiny)

            @self.panel.nd_improve.nd_ex.nd_ex.unique_callback()
            def OnClick(*args):
                if not self.try_equip_shiny(None):
                    self.try_preview()
                return

    def try_equip_shiny(self, ex_rarity):
        if not global_data.player:
            return
        else:
            if self.is_ex_step_promote:
                if ex_rarity is None:
                    log_error('ex_step promote should enter with ex_rarity !!!')
            from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._mecha_id)
            has_mecha = global_data.player and global_data.player.get_item_by_no(cur_mecha_item_id)
            if has_mecha:
                skin_info = global_data.player.get_item_by_no(self._skin_id_lst[0])
                print('skin_info', skin_info)
                return skin_info or False
            if skin_info.get_weapon_sfx():
                self._is_equip_shiny = True if 1 else False
                if not self.is_ex_step_promote:
                    equip_info_dict = self.get_equip_shiny_dict_helper(not self._is_equip_shiny, ex_rarity)
                else:
                    _, base_weapon_sfx_ex_rarity = mecha_skin_utils.get_base_skin_equiped_ex_rarity(self._cur_clothing_id)
                    old_ex_rarity = base_weapon_sfx_ex_rarity
                    if old_ex_rarity != ex_rarity:
                        if ex_rarity and ex_rarity > 0:
                            _is_equip_shiny = True if 1 else False
                        else:
                            _is_equip_shiny = not self._is_equip_shiny
                        _is_equip_shiny = ex_rarity and ex_rarity > 0 or False
                    equip_info_dict = self.get_equip_shiny_dict_helper(_is_equip_shiny, ex_rarity)
                if not self._is_equip_shiny:
                    print('_using_item', self._using_item)
                    if self._using_item is None:
                        self._selected_item.OnClick(None)
                print('equip_info_dict', equip_info_dict)
                global_data.player.try_equip_mecha_shiny_weapon(equip_info_dict)
                return True
            return False

    def get_equip_shiny_dict_helper(self, is_equip_shiny, ex_rarity):
        equip_info_dict = {}
        if not is_equip_shiny:
            for idx, c_id in enumerate(self._skin_id_lst):
                equip_info_dict[c_id] = None

        else:
            for idx, c_id in enumerate(self._skin_id_lst):
                if not self.is_ex_step_promote:
                    shiny_id = self.mecha_skin_conf.get(str(c_id), {}).get('weapon_sfx_id')
                else:
                    shiny_weapon_info = mecha_skin_utils.get_mecha_shiny_weapon_info(c_id)
                    shiny_id = None
                    for _shiny_id, _shiny_rarity in shiny_weapon_info.items():
                        if _shiny_rarity == ex_rarity:
                            shiny_id = int(_shiny_id)
                            break

                equip_info_dict[c_id] = shiny_id

        return equip_info_dict

    def try_preview(self):
        if self.is_ex_step_promote:
            log_error('ex_step promote should not enter!!!')
        self.on_ex_improve_preview()
        if self._is_previewing:
            self.panel.nd_improve.nd_ex.nd_ex.nd_choose.setVisible(False)
            self._is_previewing = False
            shiny_id = self.mecha_skin_conf.get(str(self._previewing_id), {}).get('weapon_sfx_id')
            global_data.emgr.show_shiny_weapon_sfx.emit(self._previewing_id, None, shiny_id)
            self.parent.set_shiny_id(None)
        else:
            self.panel.nd_improve.nd_ex.nd_ex.nd_choose.setVisible(True)
            self._is_previewing = True
            shiny_id = self.mecha_skin_conf.get(str(self._previewing_id), {}).get('weapon_sfx_id')
            if shiny_id:
                global_data.emgr.show_shiny_weapon_sfx.emit(self._previewing_id, shiny_id, self.parent.get_shiny_id())
                self.parent.set_shiny_id(shiny_id)
        return

    def on_ex_improve_preview(self):
        if self._can_ex_improve:
            self._selected_ex_index = AILAND_SUMMON
            if self._current_select_index != 0:
                self.on_click_ex_tab(0)
            else:
                self._update_honour_tips()

    def _play_animation(self, is_equip_shiny):
        play_anim_name = 'ex' if is_equip_shiny else 'ex_before'
        stop_anim_name = 'ex_before' if is_equip_shiny else 'ex'
        if self.panel.IsPlayingAnimation(stop_anim_name):
            self.panel.StopAnimation(stop_anim_name)
            self.panel.RecoverAnimationNodeState(stop_anim_name)
        base_skin_id = self._skin_id_lst[0]
        base_skin_lst_equipped_shiny = self._archive_data.get_field('base_skin_lst_equipped_shiny', [])
        if play_anim_name == 'ex_before':
            if base_skin_id not in base_skin_lst_equipped_shiny:
                self.panel.PlayAnimation(play_anim_name)
        else:
            self.panel.PlayAnimation(play_anim_name)
            if base_skin_id not in base_skin_lst_equipped_shiny:
                base_skin_lst_equipped_shiny.append(base_skin_id)
                self._archive_data.set_field('base_skin_lst_equipped_shiny', base_skin_lst_equipped_shiny)

    def _on_buy_good_success(self, item_id):
        self._re_init_panel()
        if self._skin_id_lst:
            skin_id = self._skin_id_lst[-1]
            if self.is_ex_step_promote:
                base_skin_id = self._skin_id_lst[0]
                shiny_weapon_info = mecha_skin_utils.get_mecha_shiny_weapon_info(base_skin_id)
                if str(item_id) in shiny_weapon_info:
                    ex_rarity = shiny_weapon_info[str(item_id)]
                    self.try_equip_shiny(ex_rarity=ex_rarity)
                    self.on_show_buy_ex_improve_tips(item_id)
            elif not self._is_equip_shiny:
                ex_rarity = None
                _weapon_sfx_id = self.get_preview_shiny_id(skin_id)
                if _weapon_sfx_id == item_id:
                    self.try_equip_shiny(ex_rarity=ex_rarity)
                self.on_show_buy_ex_improve_tips(item_id)
        if self.is_ex_step_promote:
            if self.ex_step_widget:
                relative_sfx_sets = set()
                for _skin_id in self._skin_id_lst:
                    shiny_weapon_info = mecha_skin_utils.get_mecha_shiny_weapon_info(_skin_id)
                    for shiny_id in shiny_weapon_info.keys():
                        relative_sfx_sets.add(shiny_id)

                if item_id in self._skin_id_lst or str(item_id) in relative_sfx_sets:
                    self.panel.SetTimeOut(0.1, lambda : self.ex_step_widget.check_shiny_weapon_equip_status(), tag=240402)
        return

    def on_show_buy_ex_improve_tips(self, item_id):
        try:
            index = self._ex_skin_id_list.index(item_id)
        except ValueError:
            index = -1

        if index > 0:
            text_list = [
             83420, 83421, 83422]
            global_data.game_mgr.show_tip(get_text_by_id(text_list[index - 1]))
            self.on_click_ex_tab(0)

    def _on_role_fashion_change(self, item_no, fashion_data):
        old_is_equip = self._is_equip_shiny
        from logic.gutils import item_utils
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA
        lobby_item_type = item_utils.get_lobby_item_type(item_no)
        if lobby_item_type != L_ITEM_TYPE_MECHA:
            return
        from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
        mecha_id = mecha_lobby_id_2_battle_id(item_no)
        if mecha_id != self._mecha_id:
            return
        dressed_skin_id = fashion_data.get(FASHION_POS_SUIT)
        is_dress_changed = self._cur_clothing_id != dressed_skin_id
        need_update_preview = self._previewing_id != self.parent.get_clothing_id()
        is_diff = dressed_skin_id in self._skin_id_lst and (is_dress_changed or need_update_preview)
        if is_diff:
            if not global_data.ui_mgr.get_ui('MechaDetails'):
                dress_utils.show_change_fashion_tips(fashion_data, dressed_skin_id)
            self._previewing_id = dressed_skin_id
            self._cur_clothing_id = dressed_skin_id
        self._re_init_panel()
        if not self.panel.isVisible():
            return
        if dressed_skin_id in self._skin_id_lst:
            now_equip_shiny_id = fashion_data.get(FASHION_POS_WEAPON_SFX)
            is_shiny_changed = bool(now_equip_shiny_id != self.get_parent_shiny_id()) or old_is_equip != self._is_equip_shiny
            if is_diff or not self.is_ex_step_promote or is_shiny_changed:
                preview_shiny_id = self.get_preview_shiny_id(self._previewing_id) if self._is_previewing else 0
                shiny_id = preview_shiny_id or mecha_skin_utils.get_mecha_skin_shiny_id(self._previewing_id)
                self._select_callback(self._mecha_id, self._previewing_id, shiny_id, is_refresh=True)
            if self.is_ex_step_promote:
                self.ex_step_widget and self.ex_step_widget.on_role_fashion_changed()

    def _init_price(self, c_id, node):
        if not self.is_ex_step_promote:
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(c_id))
            required_item, required_num = skin_cfg.get('required_item')
        else:
            base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(c_id)
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(base_skin_id))
            required_item, required_num = skin_cfg.get('refine_ex_required_item')
        price_info = {'original_price': required_num,'discount_price': None,
           'goods_payment': mall_utils.get_item_money_type(required_item)
           }
        init_price_template(price_info, node, color=['#SS', '#SR', '#BC'])
        return (
         required_item, required_num)

    def _on_click_card(self, layer, touche):
        if not global_data.player:
            return
        else:
            c_id = layer.c_id
            clothing_data = global_data.player.get_item_by_no(c_id)
            cur_mecha_item_id = dress_utils.battle_id_to_mecha_lobby_id(self._mecha_id)
            mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
            if mecha_item_data and clothing_data:
                if layer != self._using_item or layer != self._selected_item:
                    global_data.player.dress_mecha_fashion({FASHION_POS_SUIT: c_id})
                self._set_using_node(c_id)
                self._set_previewing_node(c_id)
            else:
                self._set_previewing_node(c_id)
                if self._select_callback:
                    if self._is_previewing:
                        shiny_id = self.get_preview_shiny_id(c_id)
                    else:
                        shiny_id = None
                    self._select_callback(self._mecha_id, c_id, shiny_id)
            return

    def _set_previewing_node(self, c_id):
        has_changed = self._previewing_id != c_id
        self._previewing_id = c_id
        card_node = self._get_skin_node(c_id)
        if not card_node:
            return
        else:
            nd_card_item = card_node.temp_card.nd_card
            if nd_card_item != self._selected_item:
                nd_card_item.nd_above.nd_choose.setVisible(True)
                if self._selected_item:
                    self._selected_item.nd_above.nd_choose.setVisible(False)
                self._selected_item = nd_card_item
            shiny_icon = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(c_id), 'shiny_weapon_icon', default=None)
            if shiny_icon and not self.is_ex_step_promote:
                self.panel.nd_improve.nd_ex.nd_ex.img_ex.SetDisplayFrameByPath('', shiny_icon)
            if self._can_ex_improve and has_changed:
                index = self._skin_id_lst.index(c_id)
                self._selected_ex_index = index
                if self._current_select_index != 0:
                    self.on_click_ex_tab(0)
                else:
                    self._update_honour_tips()
            self.update_ex_step_widget()
            return

    def _set_using_node(self, c_id):
        if c_id not in self._skin_id_lst:
            if self._using_item:
                self._using_item.nd_above.nd_using.setVisible(False)
            return
        card_node = self._get_skin_node(c_id)
        if not card_node:
            return
        nd_card_item = card_node.temp_card.nd_card
        nd_card_item.nd_above.nd_using.setVisible(True)
        if nd_card_item == self._using_item:
            return
        if self._using_item:
            self._using_item.nd_above.nd_using.setVisible(False)
        self._using_item = nd_card_item

    def _jump_to_lottery(self, required_item, required_num):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            from logic.gutils.jump_to_ui_utils import jump_to_lottery, jump_to_mall
            from logic.client.const.mall_const import MODE_SPECIAL, MODE_SPECIAL_2
            from logic.gutils.mall_utils import check_lottery_visible
            lottery_page_conf = confmgr.get('lottery_page_config', default={})
            sorted_keys = sorted(six_ex.keys(lottery_page_conf))
            sorted_keys.reverse()
            for idx in sorted_keys:
                if not check_lottery_visible(idx):
                    continue
                money_types = lottery_page_conf[idx].get('show_money_type', [])
                if not self.is_s_upgradable:
                    if 'collection_ticket' in money_types or 'lottery_points' in money_types or str(SHOP_PAYMENT_DIANCANG_TICKET_INHERIT) in money_types or '71700031' in money_types:
                        jump_to_lottery(idx)
                        return
                elif str(required_item) in money_types:
                    jump_to_lottery(idx)
                    return

            if not self.is_s_upgradable:
                goods_id = '690116231'
                jump_to_mall(goods_id=goods_id)
            else:
                item_utils.jump_to_ui(required_item)

        if not self.is_s_upgradable:
            SecondConfirmDlg2().confirm(content=get_text_by_id(608117), confirm_callback=confirm_callback)
        else:
            from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
            real_price_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>' % get_lobby_item_pic_by_item_no(required_item)
            content = get_text_by_id(870063, args={'item': real_price_txt})
            SecondConfirmDlg2().confirm(content=content, confirm_callback=confirm_callback)

    def on_load_scene(self):
        self.update_cam_position(is_slerp=False)

    def _check_do_first_scene_thing(self):
        if not self._has_done_first_scene_thing:
            if self.update_cam_position(is_slerp=False):
                self._has_done_first_scene_thing = True
        return self._has_done_first_scene_thing

    def refresh_btn_show_state(self):
        self._video_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(self._skin_id_lst[0]), 'shiny_weapon_video_website', default=None)
        self.panel.temp_btn_show.btn_major.SetText(get_text_by_id(610692))
        self.panel.temp_btn_show.setVisible(bool(self._video_conf))
        self.panel.btn_show_effect.setVisible(bool(self._video_conf))
        if not self._video_conf:
            self.panel.lab_get_method.SetPosition('50%-124', self.panel.lab_get_method.getPositionY())
            self.panel.temp_btn_use.SetPosition('50%-124', self.panel.temp_btn_use.getPositionY())
            self.panel.btn_go.SetPosition('50%-124', self.panel.btn_go.getPositionY())
            self.panel.nd_get.SetPosition('50%', self.panel.nd_get.getPositionY())
        else:
            self.panel.temp_btn_use.SetPosition('50%', self.panel.temp_btn_use.getPositionY())
            self.panel.btn_go.SetPosition('50%', self.panel.btn_go.getPositionY())
            if interface.is_steam_channel():
                from logic.gcommon.common_utils.local_text import get_cur_lang_name
                lang_name = get_cur_lang_name()
                if lang_name == 'cn':
                    self._video_url = self._video_conf.get('cn', None)
                    self._video_player_type = False
                else:
                    self._video_url = self._video_conf.get('na', None)
                    self._video_player_type = True
            elif G_IS_NA_USER:
                self._video_url = self._video_conf.get('na', None)
                self._video_player_type = True
            else:
                self._video_url = self._video_conf.get('cn', None)
                self._video_player_type = False
            red_point_state = global_data.achi_mgr.get_cur_user_archive_data('ex_skin_display_video' + str(self._previewing_id), default=0)
            self.panel.temp_btn_show.temp_red.setVisible(not bool(red_point_state))
        return

    def _init_ui_event(self):

        @self.panel.temp_btn_back.btn_back.unique_callback()
        def OnClick(*args):
            if self._disappearing:
                return
            self._disappearing = True
            anim_time = self.panel.GetAnimationMaxRunTime('disappear')

            def finished(*args):
                self._disappearing = False
                self.panel.setVisible(False)
                if self._close_cb:
                    self._close_cb(self._mecha_id)
                    if self._is_previewing:
                        self._is_previewing = False
                        shiny_id = self.mecha_skin_conf.get(str(self._previewing_id), {}).get('weapon_sfx_id')
                        if shiny_id:
                            global_data.emgr.show_shiny_weapon_sfx.emit(self._previewing_id, None, shiny_id)
                return

            self.panel.StopAnimation('disappear')
            self.panel.SetTimeOut(anim_time, finished)
            self.panel.PlayAnimation('disappear')

        @self.panel.nd_mech_touch.unique_callback()
        def OnBegin(layer, touch):
            if len(self._nd_touch_IDs) >= 2:
                return False
            tid = touch.getId()
            touch_wpos = touch.getLocation()
            if tid not in self._nd_touch_IDs:
                self._nd_touch_poses[tid] = touch_wpos
                self._nd_touch_IDs.append(tid)
            if len(self._nd_touch_IDs) >= 2:
                pts = six_ex.values(self._nd_touch_poses)
                from common.utils.cocos_utils import ccp
                self._double_touch_prev_len = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
            return True

        @self.panel.nd_mech_touch.unique_callback()
        def OnDrag(layer, touch):
            tid = touch.getId()
            touch_wpos = touch.getLocation()
            if tid not in self._nd_touch_IDs:
                return
            if self._current_select_index == PROJECTION_KILL:
                return
            if len(self._nd_touch_IDs) == 1:
                delta_pos = touch.getDelta()
                global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)
            elif len(self._nd_touch_IDs) >= 2:
                self._nd_touch_poses[tid] = touch_wpos
                pts = six_ex.values(self._nd_touch_poses)
                vec = cc.Vec2(pts[0])
                vec.subtract(pts[1])
                cur_dist = vec.getLength()
                delta = cur_dist - self._double_touch_prev_len
                self._double_touch_prev_len = cur_dist
                from logic.comsys.mecha_display.MechaDetails import MechaDetails
                delta = delta / MechaDetails.CAM_SCALE_TOUCH_SEN_FACTOR
                self._on_cam_pos_scroll_delta(delta)

        @self.panel.nd_mech_touch.unique_callback()
        def OnEnd(layer, touch):
            tid = touch.getId()
            if tid in self._nd_touch_IDs:
                self._nd_touch_IDs.remove(tid)
                del self._nd_touch_poses[tid]

        @self.panel.btn_info.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(608114, 608115)

        @self.panel.btn_describe.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(608111, 608112)

    def init_btn_glass(self):
        self.panel.btn_glass.BindMethod('OnClick', self._glass_cb)

    def init_btn_show(self):
        self.panel.btn_show.BindMethod('OnClick', self._show_cb)

    def init_btn_play(self):

        @self.panel.btn_play.unique_callback()
        def OnClick(*args):
            import game3d
            video_url = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(self._previewing_id), 'shiny_weapon_video_website', default=None)
            if video_url:
                game3d.open_url(video_url)
            else:
                global_data.game_mgr.show_tip(10063)
            return

    def init_mecha_name(self):
        mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        conf = mecha_conf[str(self._mecha_id)]
        mecha_name = conf.get('name_mecha_text_id', '')
        self.panel.nd_content.lab_title.SetString(mecha_name)

    def init_temp_btn_show(self):

        @self.panel.temp_btn_show.btn_major.unique_callback()
        def OnClick(*args):
            self.play_video()

        @self.panel.btn_show_effect.unique_callback()
        def OnClick(*args):
            self.play_video()

    def play_video(self):
        if not self._video_url:
            return
        from logic.gcommon.common_utils.local_text import get_cur_lang_name, get_default_lang_name
        lang_name = get_cur_lang_name()
        if self._video_player_type:
            import game3d
            game3d.open_url(self._video_url)
        else:

            def func():
                if not self._video_url:
                    return
                from logic.comsys.video.VideoUILogicWidget import VideoUILogicWidget
                VideoUILogicWidget().play_vod(self._video_url)
                player = global_data.video_player.get_player()
                player.set_volume(0.2)

            from common.utils import network_utils
            cur_type = network_utils.g93_get_network_type()
            if cur_type == network_utils.TYPE_MOBILE:
                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                SecondConfirmDlg2().confirm(content=get_text_by_id(607499), confirm_callback=func)
            else:
                func()
        global_data.achi_mgr.set_cur_user_archive_data('ex_skin_display_video' + str(self._previewing_id), 1)
        self.refresh_btn_show_state()

    def update_cam_data(self, cam_data, cur_scene_content_type):
        far_display_type = str(cam_data['far_cam'])
        near_display_type = str(cam_data['near_cam'])
        far_pos = lobby_model_display_utils.get_cam_position(cur_scene_content_type, far_display_type)
        near_pos = lobby_model_display_utils.get_cam_position(cur_scene_content_type, near_display_type)
        self._cam_postiion_bounds = (far_pos, near_pos, (far_pos - near_pos).length)
        self._check_do_first_scene_thing()

    def reset_cur_cam_offset_dist(self):
        self._cur_cam_offset_distance = 0.0
        self._sync_mecha_details_distance()
        self.update_cam_position(False)

    def _get_cam_position(self, offset_dist):
        far, near, length = self._cam_postiion_bounds
        if far is None or near is None:
            return
        else:
            diff = near - far
            if diff.length_sqr < offset_dist * offset_dist:
                return math3d.vector(near)
            if offset_dist < 0:
                return math3d.vector(far)
            direction = math3d.vector(diff)
            direction.normalize()
            offset = direction * offset_dist
            return far + offset
            return

    def _modify_cur_cam_offset_dist(self, offset):
        far, near, length = self._cam_postiion_bounds
        dst_offset_dist = self._cur_cam_offset_distance + offset
        dst_offset_dist = min(length, max(0, dst_offset_dist))
        self._cur_cam_offset_distance = dst_offset_dist
        self._sync_mecha_details_distance()

    def _sync_mecha_details_distance(self):
        ui = global_data.ui_mgr.get_ui('MechaDetails')
        if ui:
            ui.set_cam_offset_dist(self._cur_cam_offset_distance)

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        if self._current_select_index == PROJECTION_KILL:
            return
        from logic.comsys.mecha_display.MechaDetails import MechaDetails
        delta = delta / MechaDetails.CAM_SCALE_MOUSE_SEN_FACTOR
        self._on_cam_pos_scroll_delta(delta)

    def _on_cam_pos_scroll_delta(self, delta):
        self._modify_cur_cam_offset_dist(delta)
        self.update_cam_position(is_slerp=True)

    def update_cam_position(self, is_slerp):
        pos = self._get_cam_position(self._cur_cam_offset_distance)
        if pos is not None:
            global_data.emgr.change_model_display_scene_cam_pos.emit(pos, is_slerp=is_slerp)
            return True
        else:
            return False
            return

    def init_ex_skin_improve(self):
        skin_id = self._skin_id_lst[0]
        self._honer_count_item_no, self._projection_kill_item_no = get_ex_skin_improve_item_no(skin_id)
        if self._honer_count_item_no is None or self._projection_kill_item_no is None:
            self._can_ex_improve = False
            self._nd_tab.setVisible(False)
            return
        else:
            self._can_ex_improve = True
            self._nd_tab.setVisible(True)
            self._ex_skin_id_list = self._skin_id_lst[:]
            if len(self._ex_skin_id_list) == 2:
                self._ex_skin_id_list.append(self._skin_id_lst[-1])
            first_shiny_weapon_id = mecha_skin_utils.get_mecha_conf_ex_weapon_sfx_id(self._skin_id_lst[0])
            self._ex_skin_id_list.append(first_shiny_weapon_id)
            if len(self._ex_skin_id_list) == 2:
                self._ex_skin_id_list.extend([first_shiny_weapon_id] * 2)
            self._init_list_tab()
            self._update_red_point()
            return

    def _init_list_tab(self):
        list_tab = self._nd_tab.list_tab
        list_tab.DeleteAllSubItem()
        self._tab_btn_list = []
        for i in self._tab_list:
            item = list_tab.AddTemplateItem()
            btn_title = item.btn_title
            btn_title.EnableCustomState(True)
            btn_title.BindMethod('OnClick', lambda btn, touch, i=i: self.on_click_ex_tab(i))
            btn_title.SetText(self._tab_list[i]['text'])
            if len(self._skin_id_lst) == 1 and i > 0:
                item.lab_title.SetString(get_text_by_id(83419))
            elif len(self._skin_id_lst) == 2 and (i == 1 or i == 2):
                item.lab_title.SetString(get_text_by_id(635126))
            else:
                item.lab_title.SetString(get_text_by_id(self._tab_list[i]['unlock_text']))
            if i == 0:
                item.img_line_0.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/ex/icon_ex_line_up.png')
            elif i == len(self._tab_list) - 1:
                item.img_line_1.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/ex/icon_ex_line_down.png')
            self._tab_btn_list.append(item)

    def _update_list_tab(self):
        if self._current_select_index is None:
            self.on_click_ex_tab(0)
        else:
            self.on_click_ex_tab(self._current_select_index)
        return

    def on_click_ex_tab(self, index):
        ui = global_data.ui_mgr.get_ui('GetModelDisplayUI')
        if ui and ui.isPanelVisible():
            return
        else:
            self._current_select_index = index
            for i in range(len(self._tab_btn_list)):
                btn_icon = self._tab_btn_list[i].btn_icon
                btn_title = self._tab_btn_list[i].btn_title
                if i == self._current_select_index:
                    btn_title.SetSelect(True)
                    btn_title.temp_red.setVisible(False)
                    had_read_list = self._archive_data.get_field(EX_SKIN_IMPROVE_RED_POINT_KEY.format(self._skin_id_lst[0]), [])
                    if i not in had_read_list:
                        had_read_list.append(i)
                        self._archive_data.set_field(EX_SKIN_IMPROVE_RED_POINT_KEY.format(self._skin_id_lst[0]), had_read_list)
                else:
                    btn_title.SetSelect(False)
                has_item = bool(global_data.player.get_item_by_no(self._ex_skin_id_list[i]))
                if i == 0 or has_item:
                    btn_icon.SetShowEnable(True)
                    if i == self._current_select_index:
                        btn_icon.SetSelect(True)
                    else:
                        btn_icon.SetSelect(False)
                else:
                    btn_icon.SetShowEnable(False)
                if has_item:
                    self._tab_btn_list[i].lab_title.setVisible(False)
                else:
                    self._tab_btn_list[i].lab_title.setVisible(True)

            if index == MECHA_PREVIEW:
                if self._selected_item:
                    self._selected_item.nd_above.nd_choose.setVisible(True)
            elif self._selected_item:
                self._selected_item.nd_above.nd_choose.setVisible(False)
            if index == HONER_COUNT:
                global_data.emgr.change_model_display_scene_tag_effect.emit(None)
                self._parent_ui.set_btn_visible(False)
                self._parent_ui.set_mecha_emoji()
            elif index == PROJECTION_KILL:
                self._projection_kill_model = ProjectionKillModel(self._projection_kill_item_no, self._previewing_id, 0.6)
                self._parent_ui.set_btn_visible(False)
            else:
                self._parent_ui.on_reset_lobby_model()
                self._parent_ui.set_btn_visible(True)
            self.reset_cur_cam_offset_dist()
            self._update_honour_tips()
            self._update_common_tips()
            self._update_red_point()
            return

    def _update_honour_tips(self):
        lab_tips_honour = self._nd_tab.lab_tips_honour
        current_select_index = self._current_select_index
        selected_ex_index = self._selected_ex_index or 0
        has_item = bool(global_data.player.get_item_by_no(self._ex_skin_id_list[selected_ex_index]))
        if current_select_index != MECHA_PREVIEW or selected_ex_index == MECHA_PREVIEW or has_item:
            lab_tips_honour.setVisible(False)
        elif len(self._skin_id_lst) == 2:
            lab_tips_honour.setVisible(False)
        else:
            lab_tips_honour.setVisible(True)
        if len(self._skin_id_lst) == 1:
            lab_tips_honour.SetString(get_text_by_id(83453))
        else:
            lab_tips_honour.SetString(get_text_by_id(self._tab_list[selected_ex_index]['tips_text']))
        btn_honour = lab_tips_honour.nd_auto_fit.btn_honour

        @btn_honour.unique_callback()
        def OnClick(btn, touch):
            self.on_click_ex_tab(self._selected_ex_index)

    def _update_common_tips(self):
        index = self._current_select_index
        lab_tips_common = self._nd_tab.lab_tips_common
        btn_skip = lab_tips_common.nd_auto_fit.btn_skip
        if index == MECHA_PREVIEW:
            lab_tips_common.setVisible(False)
        else:
            lab_tips_common.setVisible(True)
            lab_tips_common.SetString(get_text_by_id(self._tab_list[index]['tips_text2']))
            has_item = bool(global_data.player.get_item_by_no(self._ex_skin_id_list[index])) if index != AILAND_SUMMON else False
            btn_skip.setVisible(has_item)

        @btn_skip.unique_callback()
        def OnClick(btn, touch):
            if self._current_select_index == HONER_COUNT:
                ui = global_data.ui_mgr.get_ui('ItemsBookMainUI')
                if ui:
                    ui.close()
                jump_to_item_book_page(5, self._honer_count_item_no)
            elif self._current_select_index == PROJECTION_KILL:
                ui = global_data.ui_mgr.get_ui('ItemsBookMainUI')
                if ui:
                    ui.close()
                jump_to_item_book_page(5, self._projection_kill_item_no)

        btn_tips = lab_tips_common.nd_auto_fit.btn_tips

        @btn_tips.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(634906), get_text_by_id(634907))

    def _update_red_point(self):
        had_read_list = self._archive_data.get_field(EX_SKIN_IMPROVE_RED_POINT_KEY.format(self._skin_id_lst[0]), [])
        for i in range(len(self._tab_btn_list)):
            has_item = bool(global_data.player.get_item_by_no(self._ex_skin_id_list[i]))
            btn_title = self._tab_btn_list[i].btn_title
            if i not in had_read_list and has_item == True:
                btn_title.temp_red.setVisible(True)
            else:
                btn_title.temp_red.setVisible(False)

    def init_ex_step(self):
        ex_step_info = mecha_skin_utils.get_mecha_shiny_weapon_info(self._cur_clothing_id)
        self.is_ex_step_promote = len(ex_step_info) > 1

    def update_ex_step_widget(self):
        self.init_ex_step()
        if self.is_ex_step_promote:
            self.panel.nd_improve.nd_ex.setVisible(False)
            self.panel.nd_improve.nd_ex_new.setVisible(True)
            from logic.comsys.mecha_display.SkinImproveExStepWidget import SkinImproveExStepWidget
            if not self.ex_step_widget:
                self.ex_step_widget = SkinImproveExStepWidget(self, self.panel.nd_improve.nd_ex_new)
            self.ex_step_widget.set_clothing_id(self._cur_clothing_id)
        else:
            self.panel.nd_improve.nd_ex.setVisible(True)
            self.panel.nd_improve.nd_ex_new.setVisible(False)

    def set_parent_shiny_id(self, shiny_id):
        self.parent.set_shiny_id(shiny_id)

    def get_parent_shiny_id(self):
        return self.parent.get_shiny_id()

    def get_preview_id(self):
        return self._previewing_id

    def get_is_preview(self):
        return self._is_previewing

    def set_is_preview(self, is_preview):
        self._is_previewing = is_preview