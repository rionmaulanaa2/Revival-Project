# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyMusicUI.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, UI_VKB_CLOSE
from logic.client.const import mall_const
from logic.gutils import mall_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MUSIC
from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
from logic.gutils import jump_to_ui_utils
from copy import deepcopy

class LobbyMusicUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/i_setting_music_choose'
    DLG_ZORDER = TOP_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'cancel',
       'btn_cancel.OnClick': 'cancel',
       'btn_confirm.OnClick': 'confirm'
       }
    GLOBAL_EVENT = {'lobby_bgm_change_success': 'refresh_goods_ids',
       'player_item_update_event': 'refresh_goods_ids',
       'refresh_item_red_point': 'refresh_goods_ids'
       }

    def on_init_panel(self):
        self.select_item = None
        self.init_music_info()
        self.refresh_goods_ids(True)
        return

    def sort_item_ids(self, items):

        def my_cmp(x, y):
            owned_x, _ = mall_utils.item_can_use_by_item_no(x)
            owned_y, _ = mall_utils.item_can_use_by_item_no(y)
            self.item_id_to_owned[x] = owned_x
            self.item_id_to_owned[y] = owned_y
            if owned_x and not owned_y:
                return -1
            if not owned_x and owned_y:
                return 1
            sort_key_x = item_utils.get_lobby_item_sort_key(x)
            sort_key_y = item_utils.get_lobby_item_sort_key(y)
            if sort_key_x == sort_key_y:
                return six_ex.compare(x, y)
            return six_ex.compare(sort_key_y, sort_key_x)

        items.sort(key=cmp_to_key(my_cmp))
        return deepcopy(items)

    def init_music_info(self):
        item_page_conf = confmgr.get('mall_page_config', str(mall_const.MEOW_ID), default={})
        goods_items = item_page_conf.get(mall_const.NONE_ID, [])
        self._item_ids = []
        self.item_id_to_goods_id = {}
        for goods_id in goods_items:
            item_no = mall_utils.get_goods_item_no(goods_id)
            self.item_id_to_goods_id[item_no] = goods_id
            item_type = item_utils.get_lobby_item_type(item_no)

        from logic.gutils import items_book_utils
        from logic.client.const import items_book_const
        page_config = items_book_utils.get_items_conf(items_book_const.LOBBY_MUSIC_ID)
        self._item_ids = list((int(i) for i in page_config.keys()))
        self._item_ids.sort()

    def get_rp_by_no(self, item_no):
        if global_data.lobby_red_point_data:
            return global_data.lobby_red_point_data.get_rp_by_no(item_no)
        else:
            return False

    def refresh_goods_ids(self, is_init=False):
        self.item_id_to_owned = {}
        self.item_ids = self.sort_item_ids(self._item_ids)
        if DEFAULT_LOBBY_BGM in self.item_ids:
            self.item_ids.remove(DEFAULT_LOBBY_BGM)
        self.item_ids.insert(0, DEFAULT_LOBBY_BGM)
        cur_bgm_item_no = global_data.player.get_lobby_bgm() or DEFAULT_LOBBY_BGM
        self.cur_bgm = cur_bgm_item_no
        list_item = self.panel.list_item
        allItems = list_item.GetAllItem()
        if len(allItems) != len(self.item_ids):
            list_item.SetInitCount(len(self.item_ids))
        for i, item in enumerate(allItems):
            item_no = self.item_ids[i]
            is_owned, _ = mall_utils.item_can_use_by_item_no(item_no)
            self.item_id_to_owned[item_no] = is_owned
            item.icon_lock.setVisible(not is_owned)
            item.lab_song_name.SetString(item_utils.get_lobby_item_name(item_no))
            item.item_no = item_no
            item.is_owned = is_owned
            if self.select_item and self.select_item == item:
                self.select_item.item_no = item_no
                self.select_item.is_owned = is_owned
            else:
                item.btn_click.SetShowEnable(is_owned)
            item.temp_red.setVisible(self.get_rp_by_no(item_no))
            if is_init:

                @item.btn_click.callback()
                def OnClick(btn, touch, item=item):
                    if self.select_item:
                        self.select_item.icon_audition.setVisible(False)
                        self.select_item.btn_click.SetSelect(False)
                        self.select_item.btn_click.SetShowEnable(self.select_item.is_owned)
                    item.icon_audition.setVisible(True)
                    item.btn_click.SetSelect(True)
                    self.select_item = item
                    music = item_utils.get_lobby_item_res_path(item.item_no) or 'M02_hall_Final'
                    global_data.sound_mgr.play_music(music)
                    self.panel.btn_confirm.SetText(get_text_by_id(80305 if item.is_owned else 80937))
                    if self.get_rp_by_no(item.item_no):
                        global_data.player.req_del_item_redpoint(item.item_no)

                if self.cur_bgm == item_no:
                    item.btn_click.OnClick(None)
                    self.select_item = item
                    list_item.LocatePosByItem(i)

        return

    def cancel(self, *args):
        self.close()
        global_data.emgr.lobby_bgm_change.emit(-1)

    def confirm(self, *args):
        if self.select_item:
            if not self.select_item.is_owned:
                if self.select_item.item_no in self.item_id_to_goods_id:
                    jump_to_ui_utils.jump_to_mall(self.item_id_to_goods_id[self.select_item.item_no])
                else:
                    item_utils.jump_to_ui(self.select_item.item_no)
            elif global_data.player:
                global_data.player.select_lobby_bgm(self.select_item.item_no)
        self.close()
        global_data.emgr.lobby_bgm_change.emit(-1)