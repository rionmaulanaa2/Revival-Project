# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaSummonAndChooseSkinUI.py
from __future__ import absolute_import
from logic.comsys.battle.MechaSummonUI import MechaSummonUI
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
from logic.gutils import mecha_skin_utils
import time
import cc
import copy
from common.cfg import confmgr
from logic.gutils import item_utils, dress_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.skin_define_utils import get_main_skin_id, get_group_skin_list
from logic.gcommon.item.item_const import FASHION_POS_WEAPON_SFX, FASHION_POS_SUIT
from logic.gcommon.common_utils import decal_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import PRIV_ENJOY_FREE_TIMES_PER_WEEK
from logic.client.const.game_mode_const import GAME_MODE_RANDOM_DEATH, GAME_MODE_EXERCISE
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
MAX_SECONDARY_SKIN_NUM = 3

class MechaSummonAndChooseSkinUI(MechaSummonUI):
    PANEL_CONFIG_NAME = 'battle_mech/mech_call_clone_2'

    def init_panel(self):
        super(MechaSummonAndChooseSkinUI, self).init_panel()
        self.init_choose_skin_widget()

    def on_finalize_panel(self):
        super(MechaSummonAndChooseSkinUI, self).on_finalize_panel()
        self.destroy_widget('choose_skin_widget')

    def init_choose_skin_widget(self):
        self.choose_skin_widget = MechaSkinChooseWidget(self.panel, self.share_mecha_lst, self.battle_type)

    def set_mecha_btn_select(self, select_id, ui_item):
        super(MechaSummonAndChooseSkinUI, self).set_mecha_btn_select(select_id, ui_item)
        self.choose_skin_widget and self.choose_skin_widget.on_select_mecha(select_id)

    def set_call_btn_enable(self, enable):
        if self.get_mecha_count_down > 0:
            return
        self.set_call_btn_state(enable)
        self.panel.btn_sure.SetEnable(enable)

    def get_chosen_skin_data(self):
        if not self.choose_skin_widget:
            return None
        else:
            skin_data = self.choose_skin_widget.get_select_mecha_fashion()
            if not skin_data:
                return None
            return skin_data


class MechaSkinChooseWidget(object):

    def __init__(self, panel, share_mecha_list, battle_type):
        self.panel = panel
        self.cur_create_skin_index = 0
        self.show_skin_list_cnf = []
        self.list_skin_ui = None
        self.list_container = None
        self.async_action = None
        self.mecha_id = None
        self.lobby_mecha_id = None
        self.selected_skin_index = 0
        self.selected_skin_id = 0
        self.priv_free_mecha_fashions = {}
        self.priv_enjoy_free_cnt = 0
        self.mecha_skin_conf = {}
        self.skin_id_to_ui_state = {}
        self.share_mecha_list = share_mecha_list or []
        self.battle_type = battle_type
        self.hide_skin_tips = False
        self.secondary_skin_index = 0
        self.show_skin_list_display = None
        self.init_parameters()
        self.init_widget()
        self.process_event(True)
        return

    def destroy(self):
        self.list_skin_ui = None
        self.show_skin_list_cnf = []
        if self.list_container:
            self.list_container.release()
            self.list_container = None
        self.clear_async_action()
        self.process_event(False)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'summon_btn_sure_ready_event': self.notify_update_btn_sure_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_select_mecha(self, mecha_id):
        self.mecha_id = mecha_id
        self.lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(self.mecha_id)
        self.show_skin_list_cnf = mecha_skin_utils.get_show_skin_list(mecha_id)
        self.show_skin_list_display = copy.deepcopy(self.show_skin_list_cnf)
        skin_id = dress_utils.get_mecha_dress_clothing_id(mecha_id)
        self.cur_create_skin_index = 0
        self.selected_skin_index = 0
        self.selected_skin_id = self.show_skin_list_cnf[0]
        if skin_id in self.show_skin_list_cnf:
            self.selected_skin_index = self.show_skin_list_cnf.index(skin_id)
            self.selected_skin_id = self.show_skin_list_cnf[self.selected_skin_index]
        self.update_widget()

    def init_parameters(self):
        player = global_data.player
        if player and player.logic:
            self.priv_free_mecha_fashions = player.logic.ev_g_priv_free_mecha_fashions() or {}
            self.priv_enjoy_free_cnt = player.logic.ev_g_priv_enjoy_free_cnt()
        self.mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self.hide_skin_tips = not self.priv_free_mecha_fashions

    def init_widget(self):
        self.list_skin_ui = self.panel.list_skin
        self.list_container = ScaleableHorzContainer(self.list_skin_ui, self.panel.nd_cut, None, self._skin_move_select_callback, self._skin_up_select_callback, self._on_begin_callback)
        self.panel.bar_tips.setVisible(not self.hide_skin_tips)
        return

    def update_widget(self):
        self.panel.nd_skin.setVisible(False)
        self.skin_id_to_ui_state = {}
        self.list_skin_ui.RecycleAllItem()
        self.list_container.clear()
        self.clear_async_action()
        self.start_async_action()

    def create_skin_item(self):
        start_time = time.time()
        while self.cur_create_skin_index < len(self.show_skin_list_cnf):
            skin_item = self.list_skin_ui.ReuseItem()
            if not skin_item:
                skin_item = self.list_skin_ui.AddTemplateItem()
            skin_item.SetClipObjectRecursion(self.panel.nd_cut)
            skin_id = self.show_skin_list_cnf[self.cur_create_skin_index]
            self.init_skin_item(skin_item, skin_id)
            self.cur_create_skin_index += 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        self.panel.nd_skin.setVisible(True)
        self.list_container.init_list()
        self.init_secondary_skin_nodes()
        self.force_select_skin(self.selected_skin_index)

    def init_skin_item(self, ui_item, skin_id):
        player = global_data.player
        name_text = item_utils.get_lobby_item_name(skin_id)
        ui_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(ui_item, skin_id)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(skin_id))
        skin_half_imge_path = skin_cfg.get('half_img_path', None)
        ui_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
        lobby_skin_ids = self.priv_free_mecha_fashions.get('lobby_skin_ids', {})
        is_priv_free = self.is_priv_free_mecha_skin(skin_id)
        ui_item.nd_share.setVisible(is_priv_free and self.priv_enjoy_free_cnt > 0)
        skin_item = player and player.get_item_by_no(skin_id)
        is_default_skin = mecha_skin_utils.is_default_mecha_skin(skin_id, self.lobby_mecha_id)
        is_intimacy_share = is_default_skin and self.mecha_id in self.share_mecha_list
        is_mode_free = not skin_item and is_default_skin and self.battle_type in (GAME_MODE_RANDOM_DEATH, GAME_MODE_EXERCISE)
        is_competition = global_data.battle and global_data.battle.get_is_competition()
        is_competition_free = is_default_skin and is_competition
        is_unlock = skin_item or is_priv_free and skin_id not in lobby_skin_ids and self.priv_enjoy_free_cnt > 0 or is_intimacy_share or is_mode_free or is_competition_free
        ui_item.nd_lock.setVisible(not is_unlock)
        has_wsfx = skin_item and skin_item.get_weapon_sfx()
        free_wsfx_id = self.get_free_wsfx_id(skin_id)
        has_free_wsfx = free_wsfx_id in self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {})
        if has_wsfx:
            weapon_sfx_item = skin_item.get_weapon_sfx()
        elif has_free_wsfx:
            weapon_sfx_item = free_wsfx_id
        else:
            weapon_sfx_item = None
        item_utils.check_skin_tag(ui_item.nd_kind, skin_id, weapon_sfx_item=weapon_sfx_item)
        main_skin_id = get_main_skin_id(skin_id)
        if mecha_skin_utils.is_default_mecha_skin(main_skin_id, self.lobby_mecha_id):
            secondary_skins = get_group_skin_list(skin_id) or []
        else:
            secondary_skins = mecha_skin_utils.get_mecha_ss_skin_lst(skin_id) or []
        self.skin_id_to_ui_state[skin_id] = {'is_priv_free': is_priv_free,'is_lock': not is_unlock,
           'is_intimacy_share': is_intimacy_share,
           'is_mode_free': is_mode_free,
           'is_default_skin': is_default_skin,
           'secondary_skins': secondary_skins
           }
        if len(secondary_skins) > 1:
            for sec_skin_id in secondary_skins:
                if sec_skin_id == skin_id:
                    continue
                self.skin_id_to_ui_state.setdefault(sec_skin_id, {})
                self.skin_id_to_ui_state[sec_skin_id].update({'secondary_skins': secondary_skins})
                self.add_skin_id_to_ui_state(sec_skin_id)

        return

    def start_async_action(self):
        self.async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.create_skin_item),
         cc.DelayTime.create(0.01)])))

    def clear_async_action(self):
        if self.async_action is not None:
            self.panel.stopAction(self.async_action)
            self.async_action = None
        return

    def force_select_skin(self, selected_skin_index):
        if not self.list_container.is_init():
            return
        self.list_container.force_select_clothing(selected_skin_index)
        self._skin_up_select_callback(selected_skin_index, is_force=True)

    def _skin_move_select_callback(self, selected_index):
        self._skin_up_select_callback(selected_index)

    def _skin_up_select_callback(self, selected_index, is_force=False):
        if (selected_index != self.selected_skin_index or is_force) and selected_index < len(self.show_skin_list_cnf):
            origin_skin_id = self.show_skin_list_cnf[selected_index]
            skin_id = self.show_skin_list_display[selected_index]
            self.selected_skin_index = selected_index
            self.selected_skin_id = skin_id
            ui = global_data.ui_mgr.get_ui('MechaSummonAndChooseSkinUI')
            ui and ui.update_mecha_picture(self.mecha_id, skin_id)
            if not self.hide_skin_tips:
                lobby_skin_ids = self.priv_free_mecha_fashions.get('lobby_skin_ids', {})
                if self.is_priv_free_mecha_skin(skin_id) and skin_id in lobby_skin_ids:
                    self.panel.lab_skin_tips.SetString(611576)
                else:
                    self.panel.lab_skin_tips.SetString(get_text_by_id(611575).format(self.priv_enjoy_free_cnt, PRIV_ENJOY_FREE_TIMES_PER_WEEK))
            is_lock = self.skin_id_to_ui_state.get(skin_id, {}).get('is_lock', False)
            ui and ui.set_call_btn_enable(not is_lock)
            self.update_secondary_skin_nodes(skin_id)

    def _on_begin_callback(self):
        pass

    def get_selected_mecha_skin(self):
        return self.selected_skin_id

    def is_priv_free_mecha_skin(self, skin_id):
        mecha_skin_ids = self.priv_free_mecha_fashions.get('mecha_skin_ids', {})
        mecha_wsfx_ids = self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {})
        if mecha_skin_utils.is_default_mecha_skin(skin_id, self.lobby_mecha_id):
            return False
        if skin_id not in mecha_skin_ids:
            return False
        skin_item = global_data.player and global_data.player.get_item_by_no(skin_id)
        if not skin_item:
            return True
        wsfx_id = skin_item.get_weapon_sfx()
        free_wsfx_id = self.get_free_wsfx_id(skin_id)
        has_free_wsfx_id = free_wsfx_id in mecha_wsfx_ids
        if not wsfx_id and has_free_wsfx_id:
            return True
        return False

    def add_skin_id_to_ui_state(self, skin_id):
        player = global_data.player
        if not player:
            return
        skin_item = player and player.get_item_by_no(skin_id)
        is_default_skin = mecha_skin_utils.is_default_mecha_skin(skin_id, self.lobby_mecha_id)
        is_intimacy_share = is_default_skin and self.mecha_id in self.share_mecha_list
        is_mode_free = not skin_item and is_default_skin and self.battle_type in (
         GAME_MODE_RANDOM_DEATH, GAME_MODE_EXERCISE)
        is_competition = global_data.battle and global_data.battle.get_is_competition()
        is_competition_free = is_default_skin and is_competition
        lobby_skin_ids = self.priv_free_mecha_fashions.get('lobby_skin_ids', {})
        is_priv_free = self.is_priv_free_mecha_skin(skin_id)
        is_unlock = skin_item or is_priv_free and skin_id not in lobby_skin_ids and self.priv_enjoy_free_cnt > 0 or is_intimacy_share or is_mode_free or is_competition_free
        self.skin_id_to_ui_state.setdefault(skin_id, {})
        self.skin_id_to_ui_state[skin_id].update({'is_priv_free': is_priv_free,
           'is_lock': not is_unlock,
           'is_intimacy_share': is_intimacy_share,
           'is_mode_free': is_mode_free,
           'is_default_skin': is_default_skin
           })

    def get_free_wsfx_id(self, skin_id):
        free_wsfx_id = None
        shiny_weapon_list = mecha_skin_utils.get_mecha_shiny_weapon_list(skin_id)
        for w_sfx in reversed(shiny_weapon_list):
            if w_sfx in self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {}):
                free_wsfx_id = w_sfx

        return free_wsfx_id

    def get_select_mecha_fashion(self):
        skin_id = self.selected_skin_id
        is_lock = self.skin_id_to_ui_state.get(skin_id, {}).get('is_lock')
        is_priv_free = self.skin_id_to_ui_state.get(skin_id, {}).get('is_priv_free')
        is_intimacy_share = self.skin_id_to_ui_state.get(skin_id, {}).get('is_intimacy_share')
        is_mode_free = self.skin_id_to_ui_state.get(skin_id, {}).get('is_mode_free')
        mecha_wsfx_ids = self.priv_free_mecha_fashions.get('mecha_wsfx_ids', {})
        if is_lock:
            return {}
        else:
            if is_intimacy_share:
                return {}
            if is_mode_free:
                return {}
            if is_priv_free and self.priv_enjoy_free_cnt > 0:
                free_wsfx_id = self.get_free_wsfx_id(skin_id)
                has_free_wsfx_id = free_wsfx_id in mecha_wsfx_ids
                mecha_fashion = {FASHION_POS_SUIT: skin_id
                   }
                if has_free_wsfx_id:
                    mecha_fashion[FASHION_POS_WEAPON_SFX] = free_wsfx_id
                return {'mecha_fashion': mecha_fashion,
                   'is_priv_free': True
                   }
            player = global_data.player
            skin_item = player and player.get_item_by_no(skin_id)
            if not skin_item:
                return {}
            mecha_sfx = skin_item.get_weapon_sfx()
            decal_list = player.get_mecha_decal().get(str(get_main_skin_id(skin_id)), [])
            decal_list = decal_utils.encode_decal_list(decal_list)
            color_dict = player.get_mecha_color().get(str(skin_id), {})
            return {'mecha_fashion': {FASHION_POS_SUIT: skin_id,FASHION_POS_WEAPON_SFX: mecha_sfx},'mecha_custom_skin': {'decal': decal_list,'color': color_dict},'is_priv_free': False
               }

    def notify_update_btn_sure_state(self):
        self._skin_up_select_callback(self.selected_skin_index, is_force=True)

    def on_click_secondary_skin_node(self, idx, skin_id):
        is_lock = self.skin_id_to_ui_state.get(skin_id, {}).get('is_lock', False)
        if is_lock:
            return
        else:
            cur_skin_item = self.list_skin_ui.GetItem(self.selected_skin_index)
            if not cur_skin_item:
                return
            for old_node in self.panel.list_temp_mecha.GetAllItem():
                old_node.img_frame_choose.setVisible(False)

            new_node = self.panel.list_temp_mecha.GetItem(idx)
            new_node.img_frame_choose.setVisible(True)
            skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(skin_id))
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            cur_skin_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
            name_text = item_utils.get_lobby_item_name(skin_id)
            cur_skin_item.lab_skin_name.setString(name_text)
            self.show_skin_list_display[self.selected_skin_index] = skin_id
            self.selected_skin_id = skin_id
            ui = global_data.ui_mgr.get_ui('MechaSummonAndChooseSkinUI')
            ui and ui.update_mecha_picture(self.mecha_id, skin_id)
            ui and ui.set_call_btn_enable(not is_lock)
            if not self.hide_skin_tips:
                lobby_skin_ids = self.priv_free_mecha_fashions.get('lobby_skin_ids', {})
                if self.is_priv_free_mecha_skin(skin_id) and skin_id in lobby_skin_ids:
                    self.panel.lab_skin_tips.SetString(611576)
                else:
                    self.panel.lab_skin_tips.SetString(get_text_by_id(611575).format(self.priv_enjoy_free_cnt, PRIV_ENJOY_FREE_TIMES_PER_WEEK))
            return

    def init_secondary_skin_nodes(self):
        self.panel.list_temp_mecha.setVisible(False)

    def update_secondary_skin_nodes(self, skin_id):
        secondary_skin_nodes = self.panel.list_temp_mecha
        secondary_skin_nodes.setVisible(False)
        secondary_skins = self.skin_id_to_ui_state.get(skin_id, {}).get('secondary_skins')
        if not secondary_skins:
            return
        skin_num = len(secondary_skins)
        if skin_num < 2:
            return
        secondary_skin_nodes.SetInitCount(skin_num)
        for idx, skin_node in enumerate(secondary_skin_nodes.GetAllItem()):
            if idx >= skin_num:
                skin_node.setVisible(False)
                continue
            skin_node.setVisible(True)
            sec_skin_id = secondary_skins[idx]
            skin_node.skin_id = sec_skin_id
            skin_node.img_icon.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(sec_skin_id))
            sec_is_unlock = not self.skin_id_to_ui_state.get(sec_skin_id, {}).get('is_lock', False)
            skin_node.img_mask.setVisible(not sec_is_unlock)
            skin_node.icon_lock.setVisible(not sec_is_unlock)
            skin_node.img_frame_choose.setVisible(False)

            @skin_node.btn_icon.unique_callback()
            def OnClick(btn, touch, _idx=idx, _skin_id=sec_skin_id):
                self.on_click_secondary_skin_node(_idx, _skin_id)

        secondary_skin_nodes.setVisible(True)