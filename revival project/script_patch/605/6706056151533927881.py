# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaInscriptionBagWidget.py
from __future__ import absolute_import
import six
import six_ex
import render
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
EXCEPT_HIDE_UI_LIST = []
from common.const import uiconst
from logic.gutils import item_utils, inscription_utils
import logic.gcommon.item.item_const as item_const
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gutils import mall_utils
from logic.comsys.common_ui.WindowCommonComponent import WindowCommonComponent
from logic.gcommon.cdata.mecha_component_data import COMPONENT_ATK, COMPONENT_DEFENSE
from logic.gcommon.item.item_const import INSCR_ATK, INSCR_FAULT_TOL, INSCR_SURVIVAL, INSCR_MOB, INSCR_RECOVER
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.gcommon.cdata.mecha_component_data import get_component_list_by_type, get_component_all_list
import logic.gcommon.const as gconst
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.template_utils import init_common_choose_list_2
from logic.gutils.new_template_utils import init_top_tab_list
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from common.utils.redpoint_check_func import check_inscription_store_red_point

class MechaInscriptionBagWidget(BaseUIWidget):

    def __init__--- This code section failed: ---

  35       0  BUILD_MAP_2           2 

  37       3  LOAD_FAST             0  'self'
           6  LOAD_ATTR             0  'on_buy_good_success'
           9  LOAD_CONST            1  'mecha_component_purchase_success'
          12  STORE_MAP        

  39      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             1  'on_player_updated'
          19  LOAD_CONST            2  'player_lv_update_event'
          22  STORE_MAP        
          23  LOAD_FAST             0  'self'
          26  STORE_ATTR            2  'global_events'

  41      29  LOAD_GLOBAL           3  'super'
          32  LOAD_GLOBAL           4  'MechaInscriptionBagWidget'
          35  LOAD_FAST             0  'self'
          38  CALL_FUNCTION_2       2 
          41  LOAD_ATTR             5  '__init__'
          44  LOAD_FAST             1  'parent'
          47  LOAD_FAST             2  'panel'
          50  LOAD_FAST             3  'mecha_type'
          53  CALL_FUNCTION_3       3 
          56  POP_TOP          

  42      57  LOAD_GLOBAL           6  'PriceUIWidget'
          60  LOAD_GLOBAL           3  'super'
          63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             7  'panel'
          69  LOAD_ATTR             8  'list_money'
          72  CALL_FUNCTION_257   257 
          75  LOAD_FAST             0  'self'
          78  STORE_ATTR            9  'price_top_widget'

  44      81  LOAD_CONST            4  '%d_%d'
          84  LOAD_GLOBAL          10  'gconst'
          87  LOAD_ATTR            11  'SHOP_PAYMENT_ITEM'
          90  LOAD_GLOBAL          10  'gconst'
          93  LOAD_ATTR            12  'REFORM_GEAR'
          96  BUILD_TUPLE_2         2 
          99  BINARY_MODULO    
         100  BUILD_LIST_1          1 
         103  LOAD_FAST             0  'self'
         106  STORE_ATTR           13  'money_type_list'

  45     109  LOAD_FAST             0  'self'
         112  LOAD_ATTR             9  'price_top_widget'
         115  LOAD_ATTR            14  'show_money_types'
         118  LOAD_FAST             0  'self'
         121  LOAD_ATTR            13  'money_type_list'
         124  CALL_FUNCTION_1       1 
         127  POP_TOP          

  50     128  LOAD_CONST            0  ''
         131  LOAD_FAST             0  'self'
         134  STORE_ATTR           16  '_com_type_filter'

  51     137  LOAD_CONST            0  ''
         140  LOAD_FAST             0  'self'
         143  STORE_ATTR           17  '_com_inscr_type_filter'

  52     146  LOAD_CONST            0  ''
         149  LOAD_FAST             0  'self'
         152  STORE_ATTR           18  '_selected_list_item_info'

  54     155  LOAD_GLOBAL          19  'False'
         158  LOAD_FAST             0  'self'
         161  STORE_ATTR           20  '_only_unowned'

  56     164  LOAD_FAST             0  'self'
         167  LOAD_ATTR            21  'precal_inscr_type'
         170  CALL_FUNCTION_0       0 
         173  POP_TOP          

  60     174  BUILD_LIST_0          0 
         177  STORE_FAST            4  'tab_text_id_list'

  61     180  LOAD_FAST             4  'tab_text_id_list'
         183  LOAD_ATTR            22  'extend'
         186  BUILD_MAP_1           1 
         189  LOAD_CONST            5  80566
         192  LOAD_CONST            6  'text'
         195  STORE_MAP        
         196  BUILD_MAP_1           1 
         199  LOAD_CONST            7  81802
         202  LOAD_CONST            6  'text'
         205  STORE_MAP        
         206  BUILD_MAP_1           1 
         209  LOAD_CONST            8  81803
         212  LOAD_CONST            6  'text'
         215  STORE_MAP        
         216  BUILD_TUPLE_3         3 
         219  CALL_FUNCTION_1       1 
         222  POP_TOP          

  63     223  BUILD_MAP_6           6 

  64     226  LOAD_CONST            5  80566
         229  LOAD_CONST            0  ''
         232  STORE_MAP        

  65     233  LOAD_CONST            9  81783
         236  LOAD_GLOBAL          23  'INSCR_ATK'
         239  STORE_MAP        

  66     240  LOAD_CONST           10  81784
         243  LOAD_GLOBAL          24  'INSCR_FAULT_TOL'
         246  STORE_MAP        

  67     247  LOAD_CONST           11  81785
         250  LOAD_GLOBAL          25  'INSCR_SURVIVAL'
         253  STORE_MAP        

  68     254  LOAD_CONST           12  81786
         257  LOAD_GLOBAL          26  'INSCR_RECOVER'
         260  STORE_MAP        

  69     261  LOAD_CONST           13  81787
         264  LOAD_GLOBAL          27  'INSCR_MOB'
         267  STORE_MAP        
         268  LOAD_FAST             0  'self'
         271  STORE_ATTR           28  '_com_inscr_type_filter_list_dict'

  71     274  LOAD_CONST            0  ''
         277  LOAD_GLOBAL          29  'COMPONENT_ATK'
         280  LOAD_GLOBAL          30  'COMPONENT_DEFENSE'
         283  BUILD_TUPLE_3         3 
         286  LOAD_FAST             0  'self'
         289  STORE_ATTR           31  '_com_type_filter_list'

  72     292  LOAD_CONST            0  ''
         295  LOAD_GLOBAL          23  'INSCR_ATK'
         298  LOAD_GLOBAL          24  'INSCR_FAULT_TOL'
         301  LOAD_GLOBAL          25  'INSCR_SURVIVAL'
         304  LOAD_GLOBAL          27  'INSCR_MOB'
         307  LOAD_GLOBAL          26  'INSCR_RECOVER'
         310  BUILD_TUPLE_6         6 
         313  LOAD_FAST             0  'self'
         316  STORE_ATTR           32  '_all_com_inscr_type_filter_list'

  73     319  LOAD_GLOBAL          33  'init_top_tab_list'
         322  LOAD_FAST             0  'self'
         325  LOAD_ATTR             7  'panel'
         328  LOAD_ATTR            34  'list_tab'
         331  LOAD_FAST             4  'tab_text_id_list'
         334  LOAD_FAST             0  'self'
         337  LOAD_ATTR            35  'on_tab_selected'
         340  CALL_FUNCTION_3       3 
         343  POP_TOP          

  74     344  LOAD_FAST             0  'self'
         347  LOAD_ATTR            36  'refresh_type_tab'
         350  CALL_FUNCTION_0       0 
         353  POP_TOP          

  78     354  LOAD_FAST             0  'self'
         357  LOAD_ATTR            37  'refresh_com_no_usage'
         360  CALL_FUNCTION_0       0 
         363  POP_TOP          

  79     364  LOAD_CONST            0  ''
         367  LOAD_FAST             0  'self'
         370  STORE_ATTR           38  '_usage_item_node'

  80     373  LOAD_GLOBAL          39  'InfiniteScrollWidget'
         376  LOAD_FAST             0  'self'
         379  LOAD_ATTR             7  'panel'
         382  LOAD_ATTR            40  'list_inscription'
         385  LOAD_FAST             0  'self'
         388  LOAD_ATTR             7  'panel'
         391  LOAD_CONST           14  'up_limit'
         394  LOAD_CONST           15  500
         397  LOAD_CONST           16  'down_limit'
         400  LOAD_CONST           15  500
         403  CALL_FUNCTION_514   514 
         406  LOAD_FAST             0  'self'
         409  STORE_ATTR           41  '_list_sview'

  81     412  LOAD_FAST             0  'self'
         415  LOAD_ATTR            41  '_list_sview'
         418  LOAD_ATTR            42  'set_template_init_callback'
         421  LOAD_FAST             0  'self'
         424  LOAD_ATTR            43  'init_component_item'
         427  CALL_FUNCTION_1       1 
         430  POP_TOP          

  82     431  LOAD_FAST             0  'self'
         434  LOAD_ATTR            41  '_list_sview'
         437  LOAD_ATTR            44  'enable_item_auto_pool'
         440  LOAD_GLOBAL          45  'True'
         443  CALL_FUNCTION_1       1 
         446  POP_TOP          

  83     447  LOAD_FAST             0  'self'
         450  LOAD_ATTR             7  'panel'
         453  LOAD_ATTR            34  'list_tab'
         456  LOAD_ATTR            46  'GetItem'
         459  LOAD_CONST           17  ''
         462  CALL_FUNCTION_1       1 
         465  LOAD_ATTR            47  'btn_tab'
         468  LOAD_ATTR            48  'OnClick'
         471  LOAD_CONST            0  ''
         474  CALL_FUNCTION_1       1 
         477  POP_TOP          

  84     478  LOAD_FAST             0  'self'
         481  LOAD_ATTR            35  'on_tab_selected'
         484  LOAD_CONST            0  ''
         487  LOAD_CONST           17  ''
         490  CALL_FUNCTION_2       2 
         493  POP_TOP          

  85     494  LOAD_FAST             0  'self'
         497  LOAD_ATTR            49  'init_own_check'
         500  CALL_FUNCTION_0       0 
         503  POP_TOP          

  86     504  LOAD_FAST             0  'self'
         507  LOAD_ATTR            50  'refresh_data'
         510  CALL_FUNCTION_0       0 
         513  POP_TOP          

  87     514  LOAD_FAST             0  'self'
         517  LOAD_ATTR            51  'init_ui_show'
         520  CALL_FUNCTION_0       0 
         523  POP_TOP          
         524  LOAD_CONST            0  ''
         527  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_257' instruction at offset 72

    def destroy(self):
        self.price_top_widget and self.price_top_widget.destroy()
        self.price_top_widget = None
        self._usage_item_node = None
        self._lv_btn_list = []
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        super(MechaInscriptionBagWidget, self).destroy()
        return

    def init_own_check(self):
        from logic.gutils.template_utils import init_common_single_choose
        init_common_single_choose(self.panel.temp_have, self.set_own_enable, self._only_unowned)

    def set_own_enable(self, is_enable):
        self._only_unowned = is_enable
        self.refresh_data()
        self.refresh_ui_show()
        self.check_purchasable_readed()

    def refresh_data(self):
        from logic.gcommon.cdata.mecha_component_data import get_com_unlock_lv
        from logic.gcommon.cdata.mecha_component_conf import lv_give_com_data, get_give_com_level
        give_coms = set(six_ex.values(lv_give_com_data))
        inscr_type_filter = [self._com_inscr_type_filter] if self._com_inscr_type_filter else None
        items = inscription_utils.get_player_component_list_by_type(self._com_type_filter, inscr_type_filter)
        if self._com_type_filter is not None:
            all_list = get_component_list_by_type(self._com_type_filter)
        else:
            all_list = get_component_all_list()
        all_list = inscription_utils.filter_list_by_plan(all_list)
        if inscr_type_filter:
            all_list = inscription_utils.filter_item_nos_by_inscr_type(all_list, inscr_type_filter)
        unown_list, own_list = inscription_utils.get_merged_item_no_all_list(items, all_list)
        own_list = sorted(own_list)
        BIG_NUM = 10000

        def sort_key(component_no):
            has_own = global_data.player.get_item_by_no(component_no)
            if component_no in give_coms:
                unlock_lv = get_give_com_level(component_no)
            else:
                unlock_lv = None
            return (
             not has_own, unlock_lv if unlock_lv else BIG_NUM, component_no)

        unown_list = sorted(unown_list, key=lambda x: sort_key(x))
        all_data_list = []
        if not self._only_unowned:
            for idx, item_no in enumerate(own_list):
                all_data_list.append(item_no)

        for item_no in unown_list:
            all_data_list.append(item_no)

        self._all_data_list = all_data_list
        return

    def init_ui_show(self):
        all_data_list = self._all_data_list
        self._list_sview.update_data_list(all_data_list)
        self._list_sview.update_scroll_view()

    def refresh_ui_show(self):
        if len(self._all_data_list) <= 0:
            self.panel.nd_empty.setVisible(True)
            self.panel.list_inscription.setVisible(False)
        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.list_inscription.setVisible(True)
            self._list_sview.update_data_list(self._all_data_list)
            self._list_sview.refresh_showed_item()

    def check_purchasable_readed(self):
        if check_inscription_store_red_point():
            import time
            achi_mgr = global_data.achi_mgr
            if achi_mgr:
                achi_mgr.set_cur_user_archive_data('inscription_store_open_time', time.time())
            global_data.emgr.mecha_component_store_rp_event.emit()

    def init_type_tab(self, com_inscr_type_filter_list):
        self._com_inscr_type_filter_list = com_inscr_type_filter_list
        type_list = [ get_text_by_id(self._com_inscr_type_filter_list_dict[inscr_type]) for inscr_type in self._com_inscr_type_filter_list ]
        if self._com_inscr_type_filter not in self._com_inscr_type_filter_list:
            self._com_inscr_type_filter = self._com_inscr_type_filter_list[0]
        self.panel.btn_sort.SetText(type_list[self._com_inscr_type_filter_list.index(self._com_inscr_type_filter)])
        type_info_list = []
        for ty_name in type_list:
            type_info_list.append({'name': ty_name})

        def call_back(index):
            new_com_inscr_type_filter = self._com_inscr_type_filter_list[index]
            if new_com_inscr_type_filter == self._com_inscr_type_filter:
                return
            self._com_inscr_type_filter = new_com_inscr_type_filter
            self.panel.btn_sort.SetText(type_list[index])
            self.refresh_data()
            self.refresh_ui_show()

        init_common_choose_list_2(self.panel.nd_sort_list, self.panel.btn_sort.img_icon, type_info_list, call_back, func_btn=self.panel.btn_sort)

    def precal_inscr_type(self):
        from logic.gcommon.cdata.mecha_component_data import get_inscs_of_component_client
        from logic.gcommon.cdata.mecha_component_data import type_com_dict
        com_type_2_inscrt_type = {}
        for com_type, com_type_list in six.iteritems(type_com_dict):
            com_type_2_inscrt_type.setdefault(com_type, {})
            for com_no in com_type_list:
                insc_list = get_inscs_of_component_client(com_no)
                for _, inscr_id, _ in insc_list:
                    inscr_conf = confmgr.get('inscription_data', str(inscr_id), default={})
                    weightKind = inscr_conf.get('weightKind', 1)
                    com_type_2_inscrt_type[com_type].setdefault(com_no, [])
                    com_type_2_inscrt_type[com_type][com_no].append(weightKind)

        self.tab_2_inscr_type_filter_dict = com_type_2_inscrt_type

    def refresh_type_tab(self):
        if self._com_type_filter is not None:
            cur_com_no_and_weight_kind = self.tab_2_inscr_type_filter_dict[self._com_type_filter]
            valid_com_nos = inscription_utils.filter_list_by_plan(six_ex.keys(cur_com_no_and_weight_kind))
            valid_inscr_type_set = set()
            for com_no in valid_com_nos:
                weight_types = cur_com_no_and_weight_kind[com_no]
                for weight_ty in weight_types:
                    valid_inscr_type_set.add(weight_ty)

            valid_inscr_type_list = sorted(list(valid_inscr_type_set))
            valid_inscr_type_list.insert(0, None)
            self.init_type_tab(valid_inscr_type_list)
        else:
            self.init_type_tab(self._all_com_inscr_type_filter_list)
        return

    def on_tab_selected(self, ui_item, index):
        new_com_type_filter = self._com_type_filter_list[index]
        if new_com_type_filter == self._com_type_filter:
            return
        self._com_type_filter = new_com_type_filter
        self.refresh_type_tab()
        self.refresh_data()
        self.refresh_ui_show()

    def init_component_item(self, ui_item, data):
        component_no = data
        inscription_utils.init_component_bag_temp(ui_item, component_no)

        @ui_item.callback()
        def OnClick(btn, touch):
            wpos = touch.getLocation()
            from logic.comsys.mecha_display.LobbyItemInscrDescUI import LobbyItemInscrDescUI
            ui = LobbyItemInscrDescUI()
            if ui:
                ui.show_item_desc_info(component_no, None, directly_world_pos=wpos)
            global_data.emgr.on_notify_guide_event.emit('inscr_guide_bag_finish')
            return

    def on_buy_good_success(self, item_no):
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_NEW_MECHA_COMPONENT
        if item_utils.get_lobby_item_type(item_no) == L_ITEM_TYPE_NEW_MECHA_COMPONENT:
            self.refresh_data()
            self.refresh_ui_show()

    def on_switch_to_mecha_type(self, mecha_type):
        self.refresh_com_no_usage()
        self.refresh_all_item_equip_mech()

    def jump_to_tab(self, com_type, inscr_type=-1, only_unowned=False):
        self._only_unowned = only_unowned
        self.panel.temp_have.choose.setVisible(self._only_unowned)
        if self._only_unowned:
            self.check_purchasable_readed()
        if inscr_type in self._com_inscr_type_filter_list:
            self._com_inscr_type_filter = inscr_type
        if com_type != self._com_type_filter and com_type in self._com_type_filter_list:
            index = self._com_type_filter_list.index(com_type)
            self.panel.list_tab.GetItem(index).btn_tab.OnClick(None)
        else:
            self.refresh_type_tab()
            self.refresh_data()
            self.refresh_ui_show()
        return

    def get_mecha_open_list(self):
        from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
        _open_mecha_lst = []
        mecha_open_info = global_data.player.read_mecha_open_info()
        if mecha_open_info['opened_order']:
            for mecha_id in mecha_open_info['opened_order']:
                if global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id)):
                    _open_mecha_lst.append(mecha_id)

        return _open_mecha_lst

    def refresh_com_no_usage(self):
        self._com_no_usage_dict = {}
        _open_mecha_lst = self.get_mecha_open_list()
        for mecha_id in _open_mecha_lst:
            cur_page = global_data.player.get_mecha_cur_page_index(mecha_id)
            page_content = global_data.player.get_mecha_component_page_content_conf(mecha_id, cur_page)
            used_item_id_list = []
            for _, item_id_list in six.iteritems(page_content):
                used_item_id_list.extend([ str(item_id) for item_id in item_id_list if item_id is not None ])

            for item_id in used_item_id_list:
                self._com_no_usage_dict.setdefault(item_id, [])
                self._com_no_usage_dict[item_id].append(mecha_id)

        return

    def refresh_all_item_equip_mech(self):
        self._list_sview.refresh_showed_item(refresh_func=self.refresh_one_equip_mech_show)

    def refresh_one_equip_mech_show(self, ui_item, data, index):
        component_no = data
        mecha_list = self._com_no_usage_dict.get(str(component_no))
        if mecha_list:
            ui_item.nd_equip.setVisible(True)
            ui_item.lab_num.SetString('X%d' % len(mecha_list))

            @ui_item.nd_equip.callback()
            def OnClick(btn, touch):
                if not self._usage_item_node:
                    self._usage_item_node = global_data.uisystem.load_template_create('mech_display/inscription/i_inscription_equip_list', parent=self.panel)
                self._usage_item_node.setVisible(True)
                lpos = self._usage_item_node.getParent().convertToNodeSpace(touch.getLocation())
                self._usage_item_node.setPosition(lpos)
                self._usage_item_node.lab_equip_num.SetString(get_text_by_id(81875) % len(mecha_list))
                self._usage_item_node.list_mech.SetInitCount(len(mecha_list))
                mech_items = self._usage_item_node.list_mech.GetAllItem()
                for idx, mech_item in enumerate(mech_items):
                    mecha_id = mecha_list[idx]
                    mech_item.item.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech%s.png' % mecha_id)

                @self._usage_item_node.nd_close.callback()
                def OnClick(btn, t):
                    if self._usage_item_node:
                        self._usage_item_node.setVisible(False)

        else:
            ui_item.nd_equip.setVisible(False)

    def on_player_updated(self, *args):
        self.refresh_ui_show()