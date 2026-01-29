# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BattlePassDisplayWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import lobby_model_display_utils
from logic.client.const import lobby_model_display_const
from logic.gcommon.item.lobby_item_type import DISPLAY_SCENE_TYPE_BATTLE_PASS, PENDANT_DISPLAY_TYPE
from logic.gcommon.item.lobby_item_type import MODEL_DISPLAY_TYPE, L_ITEM_TYPE_EXPERIENCE_CARD, L_ITEM_MECHA_SFX, L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_GESTURE, L_ITEM_TYPE_MECHA_GESTURE

class BattlePassDisplayWidget(object):

    def __init__(self, display_cb=None, special_amend_data=None, is_season_pass=True):
        super(BattlePassDisplayWidget, self).__init__()
        self._display_cb = display_cb
        self._is_season_pass = is_season_pass
        self._special_amend_data = special_amend_data
        self._displaying_model_item_no = None
        self._last_display_type = None
        self._custom_display_type = None
        return

    def set_display_type(self, display_type, reset_last=True):
        if reset_last:
            self._last_display_type = None
        self._custom_display_type = display_type
        return

    def get_display_model_item_no(self):
        return self._displaying_model_item_no

    def display_award(self, item_no, reset_display_type=False, show_conf_model=False):
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type == L_ITEM_TYPE_EXPERIENCE_CARD:
            use_params = item_utils.get_lobby_item_use_parms(item_no) or {}
            add_item_no = use_params.get('add_item', None)
            if add_item_no:
                item_no = add_item_no
                item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in MODEL_DISPLAY_TYPE:
            is_model_display = True
            if item_type == L_ITEM_MECHA_SFX:
                item_display_data = confmgr.get('display_enter_effect', 'Content', str(item_no), default={})
                callOutSfxPath = item_display_data.get('lobbyCallOutSfxPath', '')
                cSfxSoundName = item_display_data.get('cSfxSoundName', '')

                def on_finish_create_model(*args):
                    if callOutSfxPath:
                        global_data.emgr.change_model_preview_effect.emit(callOutSfxPath, cSfxSoundName)

                item_no = global_data.player.get_lobby_selected_mecha_item_id()
                clothing_id = global_data.player.get_mecha_fashion(item_no)
                if clothing_id:
                    item_no = clothing_id
                create_callback = on_finish_create_model
            else:
                create_callback = None
            if self._custom_display_type:
                display_type_id = self._custom_display_type
            elif item_type in DISPLAY_SCENE_TYPE_BATTLE_PASS:
                display_type_id = lobby_model_display_const.BATTLE_PASS
            else:
                display_type_id = lobby_model_display_const.BATTLE_PASS_02
            if reset_display_type or display_type_id != self._last_display_type:
                self._last_display_type = display_type_id
                global_data.emgr.set_lobby_scene_display_type.emit(display_type_id)
            if show_conf_model:
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no, is_in_battlepass=True)
            elif item_type == L_ITEM_TYPE_EMOTICON:
                belong_to_role_lst = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(item_no), 'belong_to_role', default=[])
                role_id = belong_to_role_lst[0]
                default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')
                show_anim = 's_emptyhand_idle'
                end_anim = 's_emptyhand_idle'
                model_data = lobby_model_display_utils.get_items_book_interaction_model_data(role_id, default_skin, show_anim, False, end_anim)
                model_data[0]['emoji_id'] = item_no
                model_data[0]['model_scale'] = 0.8
            elif item_type == L_ITEM_TYPE_GESTURE:
                from logic.gutils import items_book_utils
                model_data = items_book_utils.get_gesture_model_data(item_no)
            elif item_type == L_ITEM_TYPE_MECHA_GESTURE:
                from logic.gutils import items_book_utils
                model_data = items_book_utils.get_mecha_gesture_model_data(item_no)
            elif item_type in PENDANT_DISPLAY_TYPE:
                model_data = lobby_model_display_utils.get_pendant_show_data(item_no, is_in_battle_pass=True)
            else:
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no, is_in_battlepass=True)
            if self._special_amend_data:
                model_data[0]['off_position'] = self._special_amend_data.get('off_position', [0, 0, 0])
            self._displaying_model_item_no = item_no
            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=create_callback)
        else:
            is_model_display = False
            self.clear_model_display()
        if self._display_cb:
            self._display_cb(is_model_display, item_no)
        return

    def clear_model_display(self):
        if self._displaying_model_item_no:
            self._displaying_model_item_no = None
            from logic.gcommon.common_const.scene_const import SCENE_SAIJIKA
            if self._is_season_pass:
                if global_data.ex_scene_mgr_agent.is_cur_lobby_relatived_scene(SCENE_SAIJIKA):
                    global_data.emgr.change_model_display_scene_item.emit(None)
            else:
                global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def destroy(self):
        self.clear_model_display()
        self._display_cb = None
        return