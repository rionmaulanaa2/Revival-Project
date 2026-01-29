# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Magic/MagicRuneListUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.item_utils import get_item_pic_by_item_no
from logic.gcommon.item.item_const import ITEM_NO_MAGIC_COIN
from common.const import uiconst
MAGIC_ITEMS = ('9952', '9953', '9954', '9955')

class MagicRuneListUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_hunter/battle_talent_choose_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_click_close',
       'nd_close.OnClick': '_on_click_close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(MagicRuneListUI, self).on_init_panel()
        self.process_events(True)
        self.init_list()
        self.panel.PlayAnimation('appear')
        self.panel.lab_title.SetString(17867)
        self.update_coin_count(auto_close=False)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_hunter_coin_count': self.update_coin_count,
           'on_magic_exchange_times_change': self.update_coin_count
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_list(self):
        ui_list = self.panel.nd_content.nd_shop.list_item
        ui_list.SetInitCount(len(MAGIC_ITEMS))
        for index, ui_item in enumerate(ui_list.GetAllItem()):
            item_id = MAGIC_ITEMS[index]
            conf = confmgr.get('item', item_id, default=None)
            if not conf:
                continue
            ui_item.lab_sort.SetString(conf['name_id'])
            ui_item.nd_item.img_talent.SetDisplayFrameByPath('', get_item_pic_by_item_no(item_id))
            ui_item.lab_describe.SetString(conf['desc_id'])

            @ui_item.btn_choose.unique_callback()
            def OnClick(_btn, _touch, _id=item_id):
                self._try_buy_magic(_id)

        return

    def update_coin_count(self, *args, **kwargs):
        exchanged_times = global_data.cam_lplayer.ev_g_magic_exchange_times()
        coin_cnt, per_magic_item_cost = global_data.cam_lplayer.ev_g_magic_coin_cnt()
        unuse_cnt = coin_cnt - per_magic_item_cost * exchanged_times
        if kwargs.get('auto_close', True) and unuse_cnt < per_magic_item_cost:
            self.close()
            return
        change_color = unuse_cnt > per_magic_item_cost
        self.panel.lab_num.SetString('{}{}{}/{}'.format('<color=0XFF0000FF>' if change_color else '', str(unuse_cnt), '</color>' if change_color else '', str(per_magic_item_cost)))

    def _try_buy_magic(self, item_id):
        if not global_data.cam_lplayer:
            return
        exchanged_times = global_data.cam_lplayer.ev_g_magic_exchange_times()
        coin_cnt, per_magic_item_cost = global_data.cam_lplayer.ev_g_magic_coin_cnt()
        unuse_cnt = coin_cnt - per_magic_item_cost * exchanged_times
        if unuse_cnt < per_magic_item_cost:
            global_data.game_mgr.show_tip(17875)
            return
        global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'try_exchange_magic_item', (int(item_id),), False, False, False)

    def _on_click_close(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.process_events(False)
        super(MagicRuneListUI, self).on_finalize_panel()