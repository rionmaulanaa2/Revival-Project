# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaHonourUI.py
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils.mecha_utils import set_mecha_honour_view, get_ex_skin_improve_item_no
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils.mecha_skin_utils import get_mecha_ss_skin_lst
from logic.gcommon.time_utility import get_date_str
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from common.cfg import confmgr

class MechaHonourUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mech_display/open_mech_honour_info'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'img_window_bg.btn_close.OnClick': 'on_click_close_ui'
       }

    def on_click_close_ui(self, *args):
        self.close()

    def set_skin_id(self, temp_skin_id):
        temp_skin_config = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(temp_skin_id))
        skin_id = temp_skin_config.get('base_skin_id', temp_skin_id)
        mecha_skin_kill_cnt = global_data.player.get_mecha_skin_kill_cnt(skin_id)
        img_window_bg = self.panel.img_window_bg
        img_window_bg.lab_title.setString(get_text_by_id(83429))
        img_window_bg.lab_title2.setString(get_text_by_id(83430).format(get_lobby_item_name(temp_skin_id)))
        set_mecha_honour_view(img_window_bg.temp_honour, temp_skin_id)
        img_window_bg.lab_data.setString(get_text_by_id(83431).format(mecha_skin_kill_cnt.get('kill_human', 0)))
        img_window_bg.lab_data2.setString(get_text_by_id(83432).format(mecha_skin_kill_cnt.get('kill_mecha', 0)))
        skin_id_lst = get_mecha_ss_skin_lst(skin_id)
        if len(skin_id_lst) == 1:
            skin_info = global_data.player.get_item_by_no(skin_id)
            honour_skin_id = skin_info.get_weapon_sfx()
        else:
            honour_skin_id = skin_id_lst[1]
        item_info = global_data.player.get_item_by_no(honour_skin_id)
        create_time = item_info.get_create_time()
        date_str = get_date_str('%Y.%m.%d %H:%M:%S', int(create_time))
        img_window_bg.lab_time.setString(get_text_by_id(83433).format(date_str))

        @img_window_bg.btn_setting.unique_callback()
        def OnClick(btn, touch):
            honer_count_item_no, _ = get_ex_skin_improve_item_no(skin_id)
            jump_to_item_book_page(5, honer_count_item_no)
            self.close()