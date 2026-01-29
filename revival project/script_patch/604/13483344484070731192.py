# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/season_memory/SeasonMemoryCommonWidget.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
import logic.gutils.season_utils as season_utils
from common.utils.cocos_utils import ccp, CCRectZero, CCRect
import cc
from logic.gcommon import time_utility
from logic.gcommon.cdata import season_data
from common.cfg import confmgr
from logic.gutils.dress_utils import get_mecha_dress_clothing_id
from logic.gcommon.common_const import chat_const
from logic.gutils.template_utils import update_badge_node, set_ui_show_picture
import logic.gutils.dress_utils as dress_utils
last_send_time_dict = {}

class SeasonMemoryCommonWidget(object):

    def __init__(self, panel, parent):
        self.panel = panel
        self.parent = parent

    def destroy(self):
        self.panel = None
        self.parent = None
        return

    @staticmethod
    def update_share_panel(chat_data_cb, share_key):

        def on_click_chat_btn(*args):
            global last_send_time_dict
            extra_data = chat_data_cb()
            if not extra_data:
                return
            cur_time = time.time()
            if cur_time - last_send_time_dict.get(share_key, 0) < 20 or cur_time - last_send_time_dict.get('MAINCHAT', 0) < 11:
                cd = 20 - (cur_time - last_send_time_dict.get(share_key, 0))
                cd2 = 10 - (cur_time - last_send_time_dict.get('MAINCHAT', 0))
                global_data.game_mgr.show_tip(get_text_by_id(13081).format(data_time=int(max(cd, cd2))))
                return
            share_ui = global_data.ui_mgr.get_ui('ShareUI')
            if share_ui:
                global_data.game_mgr.show_tip(get_text_by_id(2177))
            last_send_time_dict[share_key] = cur_time
            last_send_time_dict['MAINCHAT'] = cur_time
            global_data.player.send_msg(chat_const.CHAT_WORLD, '', extra=extra_data)

        def on_click_clan_btn(*args):
            extra_data = chat_data_cb()
            if extra_data is None:
                return
            else:
                share_ui = global_data.ui_mgr.get_ui('ShareUI')
                if share_ui:
                    if global_data.player.is_in_clan():
                        global_data.player.send_msg(chat_const.CHAT_CLAN, '', extra=extra_data)
                        global_data.game_mgr.show_tip(get_text_by_id(2177))
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(10329))
                return

        btn_infos = [{'template_name': 'common/i_common_button_2','click_cb': on_click_clan_btn,'btn_name': 'btn_common','btn_text': 13087}, {'template_name': 'common/i_common_button_2','click_cb': on_click_chat_btn,'btn_name': 'btn_common','btn_text': 800150}]

        def init_cb():
            share_ui = global_data.ui_mgr.get_ui('ShareUI')
            if share_ui and share_ui.is_valid():
                share_ui.add_custom_button(btn_infos, is_head=True)

        init_cb()

    @staticmethod
    def init_share_head(nd, uid, name):
        from logic.gutils.share_utils import init_share_person_info
        if nd:
            nd.setVisible(True)
            data = global_data.message_data.get_role_head_info(uid)
            from common.const.property_const import U_ID, C_NAME, HEAD_PHOTO
            photo_no = data.get(HEAD_PHOTO)
            init_share_person_info(nd, name, uid)
            from logic.gutils import role_head_utils
            if global_data.feature_mgr.is_support_share_culling():
                role_head_utils.init_role_head_auto(nd.temp_head, uid)
            else:
                res_path = role_head_utils.get_head_photo_res_path(photo_no)
                nd.img_head.SetDisplayFrameByPath('', res_path)
                nd.temp_head.setVisible(False)
                nd.img_head.setVisible(True)