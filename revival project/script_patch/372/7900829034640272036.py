# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gutils import mall_utils
from logic.client.const import mall_const
import cc

class MallMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/mall_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {}

    def on_init_panel(self, goods_id=None, i_types=None, iTypeIdx=None):
        self._default_goods_id = goods_id
        self._default_iTypeIdx = iTypeIdx
        self._default_types = i_types
        self.is_bind = False
        self.hide_main_ui()
        self.init_parameters()
        self.init_event()
        self.init_widget()
        global_data.sound_mgr.play_music('shop')

    def init_event(self):
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        self.page_table_widget and self.page_table_widget.on_finalize_panel()
        self.page_table_widget = None
        self.item_list_widget and self.item_list_widget.on_finalize_panel()
        self.item_list_widget = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        self.show_main_ui()
        global_data.emgr.lobby_bgm_change.emit(-1)
        return

    def process_event(self, is_bind):
        if is_bind == self.is_bind:
            return
        emgr = global_data.emgr
        econf = {'player_item_update_event': self._on_item_update,
           'buy_good_success': self._on_buy_success,
           'select_mall_goods': self._on_select_mall_goods
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self.is_bind = is_bind

    def init_parameters(self):
        self.price_top_widget = None
        self.page_table_widget = None
        self.item_list_widget = None
        return

    def init_widget(self):
        from logic.gcommon.common_const import scene_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.DEFAULT_RIGHT, scene_content_type=scene_const.SCENE_MALL)
        self.create_all_widget()
        ac_list = [
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(lambda : self.select_goods_item(self._default_goods_id, self._default_types, self._default_iTypeIdx)),
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_mall'))]
        self.panel.runAction(cc.Sequence.create(ac_list))

    def create_all_widget--- This code section failed: ---

  93       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('PriceUIWidget',)
           6  IMPORT_NAME           0  'logic.comsys.mall_ui.PriceUIWidget'
           9  IMPORT_FROM           1  'PriceUIWidget'
          12  STORE_FAST            1  'PriceUIWidget'
          15  POP_TOP          

  94      16  LOAD_FAST             1  'PriceUIWidget'
          19  LOAD_FAST             3  'MallItemLstWidget'
          22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             2  'close'
          28  CALL_FUNCTION_257   257 
          31  LOAD_FAST             0  'self'
          34  STORE_ATTR            3  'price_top_widget'

  96      37  LOAD_CONST            1  ''
          40  LOAD_CONST            4  ('MallPageTabWidget',)
          43  IMPORT_NAME           4  'logic.comsys.mall_ui.MallPageTabWidget'
          46  IMPORT_FROM           5  'MallPageTabWidget'
          49  STORE_FAST            2  'MallPageTabWidget'
          52  POP_TOP          

  97      53  LOAD_FAST             2  'MallPageTabWidget'
          56  LOAD_FAST             0  'self'
          59  CALL_FUNCTION_1       1 
          62  LOAD_FAST             0  'self'
          65  STORE_ATTR            6  'page_table_widget'

  98      68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             6  'page_table_widget'
          74  LOAD_ATTR             7  'init_page_tab'
          77  CALL_FUNCTION_0       0 
          80  POP_TOP          

 100      81  LOAD_CONST            1  ''
          84  LOAD_CONST            5  ('MallItemLstWidget',)
          87  IMPORT_NAME           8  'logic.comsys.mall_ui.MallItemLstWidget'
          90  IMPORT_FROM           9  'MallItemLstWidget'
          93  STORE_FAST            3  'MallItemLstWidget'
          96  POP_TOP          

 101      97  LOAD_FAST             3  'MallItemLstWidget'
         100  LOAD_FAST             0  'self'
         103  CALL_FUNCTION_1       1 
         106  LOAD_FAST             0  'self'
         109  STORE_ATTR           10  'item_list_widget'

 102     112  LOAD_FAST             0  'self'
         115  LOAD_ATTR            11  'init_mall_list'
         118  CALL_FUNCTION_0       0 
         121  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 28

    def select_goods_item(self, goods_id=None, i_types=None, iTypeIdx=None):
        if i_types:
            self.page_table_widget.select_tab_page_by_type(*i_types)
        else:
            self.page_table_widget.select_tab_page(goods_id, iTypeIdx)
            self.item_list_widget.jump_to_goods_id(goods_id)

    def init_mall_list(self, page_index=None, sub_page_index=None):
        if not page_index:
            self.item_list_widget.reset_mall_list()
        else:
            self.item_list_widget.init_mall_list(page_index, sub_page_index)

    def set_selected_page(self, page_index, sub_page_index):
        if not self.price_top_widget:
            return
        self.price_top_widget.show_money_types(mall_utils.get_mall_money_types(page_index, sub_page_index))
        self.init_mall_list(page_index, sub_page_index)
        if page_index == mall_const.RECOMMEND_ID:
            mall_utils.set_mall_red_point(page_index, sub_page_index, 0)

    def set_mall_main_show_money_type(self, money_types):
        self.price_top_widget.show_money_types(money_types)

    def _on_select_mall_goods(self, goods_id):
        pass

    def get_cur_page_index(self):
        return self.item_list_widget.get_cur_page_index()

    def get_cur_sub_page_index(self):
        return self.item_list_widget.get_cur_sub_page_index()

    def reset_mall_list(self):
        self.page_table_widget.on_red_point_update()
        self.item_list_widget.reset_mall_list()

    def _on_item_update(self, *args):
        player = global_data.player
        if not player.requested_buy_goods:
            self.reset_mall_list()

    def _on_buy_success(self, *args, **kargs):
        player = global_data.player
        if player.requested_buy_goods:
            self.reset_mall_list()

    def _on_login_reconnected(self, *args):
        self.close()

    def do_show_panel(self):
        super(MallMainUI, self).do_show_panel()
        from common.platform.appsflyer import Appsflyer
        from common.platform.appsflyer_const import AF_SHOPCLICK
        Appsflyer().advert_track_event(AF_SHOPCLICK)
        self.item_list_widget and self.item_list_widget.do_show_panel()
        self.process_event(True)
        self.reset_mall_list()

    def do_hide_panel(self):
        super(MallMainUI, self).do_hide_panel()
        from common.platform.appsflyer import Appsflyer
        from common.platform.appsflyer_const import AF_SHOPCLICK
        Appsflyer().advert_track_event(AF_SHOPCLICK)
        self.item_list_widget and self.item_list_widget.do_hide_panel()
        self.process_event(False)