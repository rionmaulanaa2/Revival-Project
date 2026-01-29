# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemsBookMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.comsys.items_book_ui.ItemsBookPageTabWidget import PAGE_RP_TYPE
from logic.gcommon.item.lobby_item_type import RP_BELONG_SET
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.client.const import lobby_model_display_const
import logic.gcommon.const as gconst
from logic.client.const import items_book_const
import six_ex
import cc
SHOW_ND_TRANSPARENT_LIST = [
 items_book_const.WEAPON_ID,
 items_book_const.VEHICLE_ID,
 items_book_const.PERSONALIZATION_ID]
ND_TRANSPARENT_POS_DICT = {items_book_const.WEAPON_ID: cc.Vec2(310, 160),
   items_book_const.VEHICLE_ID: cc.Vec2(310, 160),
   items_book_const.PERSONALIZATION_ID: cc.Vec2(310, 110)
   }
SHOW_ND_TRANSPARENT_COUNT = 5

class ItemsBookMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'catalogue/catalogue_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {}
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    NEED_SCROLL_ALWAYS = True

    def on_init_panel(self, item_no=None, page='1'):
        self.init_parameters()
        self._default_page = page
        self._default_item_no = item_no
        self.hide_main_ui()
        self.init_widget()
        self.init_ui_event()
        self.process_events(True)

    def on_finalize_panel(self):
        self.process_events(False)
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        self.page_table_widget and self.page_table_widget.on_finalize_panel()
        self.page_table_widget = None
        self.item_list_widget and self.item_list_widget.destroy()
        self.item_list_widget = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        self.show_main_ui()
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_item_red_point': self.update_nd_transparent_visible
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        self.price_top_widget = None
        self.page_table_widget = None
        self.item_list_widget = None
        return

    def init_widget(self):
        from logic.gcommon.common_const import scene_const
        self.create_all_widget()

        def select_page():
            if not global_data.player:
                self.close()
                return
            self.page_table_widget.select_tab_page_by_item_type(self._default_page)

        def select_item_no():
            if not global_data.player:
                self.close()
                return
            self.select_item(self._default_item_no)

        ac_list = [
         cc.DelayTime.create(0.001),
         cc.CallFunc.create(lambda : select_page())]
        if self._default_item_no:
            ac_list = [cc.DelayTime.create(0.001),
             cc.CallFunc.create(lambda : select_item_no())]
        ac_list.extend([
         cc.DelayTime.create(0.001),
         cc.CallFunc.create(lambda : self.panel and self.panel.PlayAnimation('in'))])
        self.panel.runAction(cc.Sequence.create(ac_list))

    def select_item(self, item_no):
        self.page_table_widget.select_tab_page(item_no)
        self.item_list_widget.jump_to_item_no(item_no)

    def select_item_only(self, item_no):
        self.item_list_widget.jump_to_item_no(item_no)

    def jump_to_page(self, item_type):
        self.page_table_widget.select_tab_page_by_item_type(item_type)

    def create_all_widget--- This code section failed: ---

 128       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('PriceUIWidget',)
           6  IMPORT_NAME           0  'logic.comsys.mall_ui.PriceUIWidget'
           9  IMPORT_FROM           1  'PriceUIWidget'
          12  STORE_FAST            1  'PriceUIWidget'
          15  POP_TOP          

 129      16  LOAD_FAST             1  'PriceUIWidget'
          19  LOAD_FAST             3  'ItemsBookItemLstWidget'
          22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             2  'close'
          28  CALL_FUNCTION_257   257 
          31  LOAD_FAST             0  'self'
          34  STORE_ATTR            3  'price_top_widget'

 131      37  LOAD_CONST            1  ''
          40  LOAD_CONST            4  ('ItemsBookPageTabWidget',)
          43  IMPORT_NAME           4  'logic.comsys.items_book_ui.ItemsBookPageTabWidget'
          46  IMPORT_FROM           5  'ItemsBookPageTabWidget'
          49  STORE_FAST            2  'ItemsBookPageTabWidget'
          52  POP_TOP          

 132      53  LOAD_FAST             2  'ItemsBookPageTabWidget'
          56  LOAD_FAST             0  'self'
          59  CALL_FUNCTION_1       1 
          62  LOAD_FAST             0  'self'
          65  STORE_ATTR            6  'page_table_widget'

 133      68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             6  'page_table_widget'
          74  LOAD_ATTR             7  'init_page_tab'
          77  CALL_FUNCTION_0       0 
          80  POP_TOP          

 135      81  LOAD_CONST            1  ''
          84  LOAD_CONST            5  ('ItemsBookItemLstWidget',)
          87  IMPORT_NAME           8  'logic.comsys.items_book_ui.ItemsBookItemLstWidget'
          90  IMPORT_FROM           9  'ItemsBookItemLstWidget'
          93  STORE_FAST            3  'ItemsBookItemLstWidget'
          96  POP_TOP          

 136      97  LOAD_FAST             3  'ItemsBookItemLstWidget'
         100  LOAD_FAST             0  'self'
         103  CALL_FUNCTION_1       1 
         106  LOAD_FAST             0  'self'
         109  STORE_ATTR           10  'item_list_widget'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 28

    def init_items_list(self, page_index=None):
        if not page_index:
            self.item_list_widget.reset_items_list()
        else:
            self.item_list_widget.init_items_list(page_index)

    def set_selected_page(self, page_index):
        self.price_top_widget.show_money_types([])
        self.init_items_list(page_index)
        self.update_nd_transparent_visible()

    def get_cur_page_index(self):
        return self.item_list_widget.get_cur_page_index()

    def reset_items_list(self):
        self.item_list_widget.reset_items_list()

    def _on_login_reconnected(self, *args):
        self.close()

    def do_show_panel(self):
        super(ItemsBookMainUI, self).do_show_panel()
        self.item_list_widget and self.item_list_widget.do_show_panel()

    def do_hide_panel(self):
        super(ItemsBookMainUI, self).do_hide_panel()
        self.item_list_widget and self.item_list_widget.do_hide_panel()

    def move_out(self):
        self.panel.PlayAnimation('disappear')

    def move_in(self):
        self.panel.PlayAnimation('in')

    def check_can_mouse_scroll(self):
        return self.item_list_widget.check_can_mouse_scroll()

    def on_hot_key_mouse_scroll(self, *args, **kw):
        self.item_list_widget.on_hot_key_mouse_scroll(*args, **kw)

    def update_nd_transparent_visible(self):
        item_no_list = self.get_rp_item_no_list()
        is_show = len(item_no_list) >= SHOW_ND_TRANSPARENT_COUNT and self.get_cur_page_index() in SHOW_ND_TRANSPARENT_LIST
        nd_transparent = self.panel.nd_transparent
        nd_transparent.setVisible(is_show)
        if is_show:
            nd_transparent.setPosition(ND_TRANSPARENT_POS_DICT.get(self.get_cur_page_index()))

    def get_rp_item_no_list(self):
        item_no_list = []
        rp_types = PAGE_RP_TYPE.get(self.get_cur_page_index(), [])
        for i_type in rp_types:
            if i_type in RP_BELONG_SET:
                for rp_data in six_ex.values(global_data.lobby_red_point_data.get_rp_data_by_type(i_type)):
                    item_no_list.extend(six_ex.keys(rp_data))

            else:
                item_no_list.extend(six_ex.keys(global_data.lobby_red_point_data.get_rp_data_by_type(i_type)))

        return item_no_list

    def init_ui_event(self):

        @self.panel.nd_transparent.btn.unique_callback()
        def OnClick(btn, touch):
            item_no_list = self.get_rp_item_no_list()
            global_data.player.req_del_item_redpoint_list(item_no_list)