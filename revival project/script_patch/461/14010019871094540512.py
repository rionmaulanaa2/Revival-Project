# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEMechaWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.platform.dctool import interface
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from .PVEMechaChooseWidget import PVEMechaChooseWidget
from .PVESkinChooseWidget import PVESkinChooseWidget
from .PVEMechaInfoWidget import PVEMechaInfoWidget
from .PVEMechaUpgradeWidget import PVEMechaUpgradeWidget
from logic.gutils.template_utils import WindowTopSingleSelectListHelper, init_skin_tags
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id, DEFAULT_CLOTHING_ID
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils.mecha_skin_utils import is_ss_level_skin
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.pve_utils import get_pve_active_mecha_id_list, update_model_and_cam_pos, reset_model_and_cam_pos
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_ITEM_PVE_COIN, SKIN_SHARE_TYPE_PRIV
from logic.gcommon.time_utility import get_server_time
from logic.gutils import item_utils
from common.cfg import confmgr
MECHA_SKIN = 0
MECHA_INFO = 1
MECHA_UPGRADE = 2
NORMAL_POSITION = [
 -132, 0, 0]
OFF_POSITION = [-8, 0, 0]
OFF_MODEL_POSITION = [-15, 0, 0]

class PVEMechaWidgetUI(BasePanel):
    DELAY_CLOSE_TAG = 20231106
    PANEL_CONFIG_NAME = 'pve/mecha/pve_mecha_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }
    GLOBAL_EVENT = {'del_mecha_pose_result_event': 'on_mecha_skin_dress_record_change'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PVEMechaWidgetUI, self).on_init_panel()
        if global_data.player:
            global_data.player.check_pve_selected_mecha_is_available()
        self.init_params()
        self.init_ui()
        self.init_ui_events()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.player_item_update_event,
           'on_pve_mecha_show_changed': self.on_pve_mecha_show_changed,
           'on_pve_mecha_skin_changed': self._update_pve_mecha_skin_item,
           'pay_order_succ_event': self._update_pve_mecha_skin_item,
           'role_fashion_chagne': self._update_pve_mecha_skin_item,
           'on_pve_mecha_changed': self._update_pve_mecha_skin_item,
           'update_skin_share_state': self._update_pve_mecha_skin_item
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def play_anim(self):
        self.show()
        self.panel.PlayAnimation('appear')
        self.hide_main_ui()

    def init_params(self):
        self._disappearing = False
        self.is_fold = False
        self._price_top_widget = None
        self._mecha_choose_widget = None
        self._mecha_choose_widget2 = None
        self._is_in_expand_mode = False
        self._skin_choose_widget = None
        self.ui_cls_list = []
        self._mecha_bar_wrapper = None
        self.tab_widgets = {}
        self.tab_list = [{'index': MECHA_UPGRADE,'text': 423,'widget': self.panel.nd_info_2,'init_func': self._init_mecha_upgrade_widget}, {'index': MECHA_INFO,'text': 421,'widget': self.panel.nd_info_1,'init_func': self._init_mecha_info_widget}, {'index': MECHA_SKIN,'text': 422,'widget': self.panel.bar_skin}]
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._has_change_mecha_skin = False
        self._nd_touch_IDs = []
        return

    def init_ui(self):
        self.panel.PlayAnimation('loop')
        self._mecha_choose_widget = PVEMechaChooseWidget(self, self.panel.list_choose_mecha)
        self._skin_choose_widget = PVESkinChooseWidget(self, self.panel.nd_skin_choose)
        self.panel.bar_skin.setVisible(False)
        self.panel.bar_info.setVisible(False)
        self.panel.nd_btn_left.setVisible(False)
        self._init_money_widget()
        self._init_mecha_bar()
        self._update_pve_mecha_skin_item()

    def init_ui_events(self):

        @self.panel.btn_use.callback()
        def OnClick(btn, touch):
            mecha_id, clothing_id = self.get_current_id()
            top_clothing_id = get_main_skin_id(clothing_id)
            is_share, _ = global_data.player.is_share_mecha_skin(clothing_id)
            if is_share:
                fashion_data = global_data.player.get_share_mecha_fashion_data(clothing_id)
                global_data.player.set_chosen_pve_share_fashion(fashion_data)
                self._update_pve_mecha_skin_item()
            else:
                global_data.player.set_chosen_pve_share_fashion({})
                global_data.player.install_mecha_main_skin_scheme(mecha_id, top_clothing_id, {FASHION_POS_SUIT: clothing_id})
            if mecha_id != global_data.player.get_pve_select_mecha_id():
                global_data.player.pve_select_mecha(mecha_id)
            update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
            if self.is_fold:
                self._on_fold_mecha_details_widget()

        @self.panel.btn_play.callback()
        def OnClick(btn, touch):
            _, clothing_id = self.get_current_id()
            video_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id), 'shiny_weapon_video_website', default=None)
            if video_conf:
                video_url = None
                video_player_type = False
                if interface.is_steam_channel():
                    from logic.gcommon.common_utils.local_text import get_cur_lang_name
                    lang_name = get_cur_lang_name()
                    if lang_name == 'cn':
                        video_url = video_conf.get('cn', None)
                        video_player_type = False
                    else:
                        video_url = video_conf.get('na', None)
                        video_player_type = True
                elif G_IS_NA_USER:
                    video_url = video_conf.get('na', None)
                    video_player_type = True
                else:
                    video_url = video_conf.get('cn', None)
                    video_player_type = False
                if video_player_type:
                    import game3d
                    game3d.open_url(video_url)
                else:

                    def func():
                        from logic.comsys.video.VideoUILogicWidget import VideoUILogicWidget
                        VideoUILogicWidget().play_vod(video_url)
                        player = global_data.video_player.get_player()
                        player.set_volume(0.2)

                    from common.utils import network_utils
                    cur_type = network_utils.g93_get_network_type()
                    if cur_type == network_utils.TYPE_MOBILE:
                        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                        SecondConfirmDlg2().confirm(content=get_text_by_id(607499), confirm_callback=func)
                    else:
                        func()
            else:
                global_data.game_mgr.show_tip(10063)
            return

        @self.panel.btn_click.callback()
        def OnClick(btn, touch):
            self._on_fold_mecha_details_widget()

        @self.panel.btn_left.callback()
        def OnClick(btn, touch):
            self._on_fold_mecha_details_widget()

        @self.panel.btn_last_mech.callback()
        def OnClick(btn, touch):
            open_mecha_list = get_pve_active_mecha_id_list()
            cur_mecha_id, _ = self.get_current_id()
            if cur_mecha_id in open_mecha_list:
                index = open_mecha_list.index(cur_mecha_id)
            else:
                index = 1
            last_index = len(open_mecha_list) - 1 if index == 0 else index - 1
            mecha_id = open_mecha_list[last_index]
            global_data.emgr.on_pve_mecha_show_changed.emit(mecha_id)

        @self.panel.btn_next_mech.callback()
        def OnClick(btn, touch):
            open_mecha_list = get_pve_active_mecha_id_list()
            cur_mecha_id, _ = self.get_current_id()
            if cur_mecha_id in open_mecha_list:
                index = open_mecha_list.index(cur_mecha_id)
            else:
                index = len(open_mecha_list) - 1
            next_index = 0 if index == len(open_mecha_list) - 1 else index + 1
            mecha_id = open_mecha_list[next_index]
            global_data.emgr.on_pve_mecha_show_changed.emit(mecha_id)

        @self.panel.nd_mech_touch.unique_callback()
        def OnBegin(layer, touch):
            if len(self._nd_touch_IDs) > 1:
                return False
            tid = touch.getId()
            if tid not in self._nd_touch_IDs:
                self._nd_touch_IDs.append(tid)
            return True

        @self.panel.nd_mech_touch.unique_callback()
        def OnDrag(layer, touch):
            tid = touch.getId()
            if tid not in self._nd_touch_IDs:
                return
            if len(self._nd_touch_IDs) == 1:
                delta_pos = touch.getDelta()
                global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        @self.panel.nd_mech_touch.unique_callback()
        def OnEnd(layer, touch):
            tid = touch.getId()
            if tid in self._nd_touch_IDs:
                self._nd_touch_IDs.remove(tid)

        @self.panel.btn_show.unique_callback()
        def OnClick(btn, touch):
            if self._is_in_expand_mode:
                self.panel.PlayAnimation('show_less')
            else:
                if not self._mecha_choose_widget2:
                    self._mecha_choose_widget2 = PVEMechaChooseWidget(self, self.panel.list_choose_mecha2)
                self.panel.PlayAnimation('show_more')
            self._is_in_expand_mode = not self._is_in_expand_mode

    def on_force_click_btn_confirm(self, *args):
        update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
        if self.is_fold:
            self._on_fold_mecha_details_widget()

    def on_resolution_changed(self):
        super(PVEMechaWidgetUI, self).on_resolution_changed()

    def do_show_panel(self):
        super(PVEMechaWidgetUI, self).do_show_panel()
        self.process_events(True)
        self.do_switch_scene()
        ui = global_data.ui_mgr.get_ui('PVEMainUI')
        if ui:
            if self._has_change_mecha_skin and self._skin_choose_widget:
                cur_mecha_id, _ = self.get_current_id()
                self._skin_choose_widget.update_nd_skin_choose(cur_mecha_id)
                self._has_change_mecha_skin = False
            else:
                ui.update_shiny_weapon()
            ui.update_model_and_cam_pos()

    def do_switch_scene(self):
        from logic.gcommon.common_const.scene_const import SCENE_PVE_MAIN_UI
        from logic.client.const.lobby_model_display_const import PVE_MAIN_UI
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_PVE_MAIN_UI, PVE_MAIN_UI, belong_ui_name='PVEMainUI')

    def do_hide_panel(self):
        super(PVEMechaWidgetUI, self).do_hide_panel()
        self.process_events(False)

    def _init_mecha_upgrade_widget(self, widget):
        mecha_upgrade_widget = PVEMechaUpgradeWidget(self, widget)
        self.ui_cls_list.append(mecha_upgrade_widget)

    def _init_mecha_info_widget(self, widget):
        mecha_info_widget = PVEMechaInfoWidget(self, widget)
        self.ui_cls_list.append(mecha_info_widget)

    def on_mecha_skin_dress_record_change(self):
        self._has_change_mecha_skin = True

    def close(self, *args):
        if global_data.player:
            global_data.emgr.on_pve_mecha_show_changed.emit(global_data.player.get_pve_select_mecha_id())
        self.play_disappear_anim()

    def player_item_update_event(self):
        self._update_money_widget()
        self._update_pve_mecha_skin_item()

    def _init_money_widget--- This code section failed: ---

 303       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_price_top_widget'
           6  POP_JUMP_IF_FALSE    34  'to 34'

 304       9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             0  '_price_top_widget'
          15  LOAD_ATTR             1  'destroy'
          18  CALL_FUNCTION_0       0 
          21  POP_TOP          

 305      22  LOAD_CONST            0  ''
          25  LOAD_FAST             0  'self'
          28  STORE_ATTR            0  '_price_top_widget'
          31  JUMP_FORWARD          0  'to 34'
        34_0  COME_FROM                '31'

 307      34  LOAD_FAST             0  'self'
          37  LOAD_ATTR             0  '_price_top_widget'
          40  POP_JUMP_IF_TRUE    152  'to 152'

 308      43  LOAD_GLOBAL           3  'PriceUIWidget'
          46  LOAD_GLOBAL           1  'destroy'
          49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             4  'panel'
          55  LOAD_ATTR             5  'list_money'
          58  LOAD_CONST            2  'pnl_title'
          61  LOAD_GLOBAL           6  'False'
          64  CALL_FUNCTION_513   513 
          67  LOAD_FAST             0  'self'
          70  STORE_ATTR            0  '_price_top_widget'

 309      73  LOAD_FAST             0  'self'
          76  LOAD_ATTR             7  'get_current_id'
          79  CALL_FUNCTION_0       0 
          82  UNPACK_SEQUENCE_2     2 
          85  STORE_FAST            1  'mecha_id'
          88  STORE_FAST            2  '_'

 310      91  LOAD_GLOBAL           8  'confmgr'
          94  LOAD_ATTR             9  'get'
          97  LOAD_CONST            3  'mecha_debris_data'
         100  LOAD_GLOBAL          10  'str'
         103  LOAD_FAST             1  'mecha_id'
         106  CALL_FUNCTION_1       1 
         109  LOAD_CONST            4  'ex_cost'
         112  CALL_FUNCTION_3       3 
         115  STORE_FAST            3  'ex_cost_item_no'

 311     118  LOAD_FAST             0  'self'
         121  LOAD_ATTR             0  '_price_top_widget'
         124  LOAD_ATTR            11  'show_money_types'
         127  LOAD_CONST            5  '4_{}'
         130  LOAD_ATTR            12  'format'
         133  LOAD_FAST             3  'ex_cost_item_no'
         136  CALL_FUNCTION_1       1 
         139  LOAD_GLOBAL          13  'SHOP_PAYMENT_ITEM_PVE_COIN'
         142  BUILD_LIST_2          2 
         145  CALL_FUNCTION_1       1 
         148  POP_TOP          
         149  JUMP_FORWARD          0  'to 152'
       152_0  COME_FROM                '149'
         152  LOAD_CONST            0  ''
         155  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_513' instruction at offset 64

    def _update_money_widget(self):
        if self._price_top_widget:
            self._price_top_widget._on_player_info_update()

    def _init_mecha_bar(self):
        list_tab = self.panel.list_tab
        list_tab.DeleteAllSubItem()
        list_tab.SetInitCount(len(self.tab_list))

        def init_btn(node, data):
            btn_tab = node.btn_tab
            btn_tab.SetText(get_text_by_id(data.get('text', '')))
            btn_tab.icon.SetDisplayFrameByPath('', '')

        def btn_click_cb(ui_item, data, *args):
            index = data.get('index')
            self.panel.bar_info.setVisible(index != MECHA_SKIN)
            if index in self.tab_widgets:
                for ind in self.tab_widgets:
                    widget = self.tab_widgets[ind]
                    widget.setVisible(index == ind)

            else:
                widget = data.get('widget')
                init_func = data.get('init_func')
                if widget is None:
                    return
            self.tab_widgets[index] = widget
            for ind in self.tab_widgets:
                cur_widget = self.tab_widgets[ind]
                cur_widget.setVisible(index == ind)
                if index == ind and init_func:
                    init_func(widget)

            return

        self._mecha_bar_wrapper = WindowTopSingleSelectListHelper()
        self._mecha_bar_wrapper.set_up_list(list_tab, self.tab_list, init_btn, btn_click_cb)
        self._mecha_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def on_pve_mecha_show_changed(self, *args):
        self._init_money_widget()
        self._update_pve_mecha_skin_item()

    def _update_pve_mecha_skin_item(self, *args):
        mecha_id, clothing_id = self.get_current_id()
        if not mecha_id or not clothing_id:
            return
        else:
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
            pve_mecha_id = global_data.player.get_pve_select_mecha_id() if global_data.player else None
            pve_mecha_item_id = global_data.player.get_pve_selected_mecha_item_id() if global_data.player else None
            fashion_id = global_data.player.get_pve_using_mecha_skin(pve_mecha_item_id) if global_data.player else DEFAULT_CLOTHING_ID
            is_use = mecha_id == pve_mecha_id and clothing_id == fashion_id
            if global_data.player:
                is_share, share_type = global_data.player.is_share_mecha_skin(clothing_id)
                is_intimacy_share_mecha = global_data.player.is_intimacy_share_mecha(cur_mecha_item_id)
            else:
                is_share, share_type = False, None
                is_intimacy_share_mecha = False
            if is_share and share_type == SKIN_SHARE_TYPE_PRIV:
                is_teammate_lobby_skin = global_data.player.is_teammate_lobby_skin(clothing_id)
                is_share = bool(is_share and not is_teammate_lobby_skin)
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
            clothing_data = global_data.player.get_item_by_no(clothing_id) if global_data.player else None
            is_default_skin = False
            if int(default_skin) == int(clothing_id):
                clothing_id = cur_mecha_item_id
                clothing_data = global_data.player.get_item_by_no(cur_mecha_item_id) if global_data.player else None
                is_default_skin = True
            is_owned_mecha = bool(global_data.player and global_data.player.get_item_by_no(cur_mecha_item_id)) or is_intimacy_share_mecha
            is_owned_skin = bool(clothing_data) or is_share
            is_owned = is_owned_mecha and (is_default_skin or is_owned_skin)
            self.panel.btn_use.setVisible(is_owned and not is_use)
            self.panel.lab_status.setVisible(is_use)
            self.panel.lab_name_info.setString(item_utils.get_lobby_item_name(cur_mecha_item_id))
            self.panel.lab_name_skin.setString(item_utils.get_lobby_item_name(cur_mecha_item_id))
            self.panel.temp_name.bar_name.lab_mecha.setString(item_utils.get_lobby_item_name(cur_mecha_item_id))
            self.panel.lab_name_skin.setString(item_utils.get_lobby_item_name(clothing_id))
            cur_skin_cnf = self._mecha_skin_conf.get(str(clothing_id), {})
            init_skin_tags(self.panel.nd_tags, self.panel.nd_tags_desc, None, cur_skin_cnf.get('skin_tags', []))
            is_ss = is_ss_level_skin(clothing_id)
            self.panel.btn_play.setVisible(is_ss)
            return

    def _on_fold_mecha_details_widget(self):
        if self.panel.IsPlayingAnimation('switch') or self.panel.IsPlayingAnimation('revert'):
            return
        if self.is_fold:
            self.panel.PlayAnimation('revert')
            update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
        else:
            self.panel.PlayAnimation('switch')
            update_model_and_cam_pos(OFF_POSITION, OFF_MODEL_POSITION)
        self.is_fold = not self.is_fold

    def get_current_id(self):
        if self._skin_choose_widget:
            return self._skin_choose_widget.get_current_id()
        else:
            pve_mecha_id = global_data.player.get_pve_select_mecha_id() if global_data.player else None
            pve_mecha_item_id = global_data.player.get_pve_selected_mecha_item_id() if global_data.player else None
            fashion_id = global_data.player.get_pve_using_mecha_skin(pve_mecha_item_id) if global_data.player else DEFAULT_CLOTHING_ID
            return (
             pve_mecha_id, fashion_id)
            return

    def is_priv_free_mecha_skin(self, skin_id):
        if self._skin_choose_widget:
            return self._skin_choose_widget.is_priv_free_mecha_skin(skin_id)
        else:
            return False

    def is_teammate_lobby_skin(self, skin_id):
        if self._skin_choose_widget:
            return self._skin_choose_widget.is_teammate_lobby_skin(skin_id)
        else:
            return True

    def get_priv_fashion_data(self, skin_id):
        if self._skin_choose_widget:
            return self._skin_choose_widget.get_priv_fashion_data(skin_id)
        else:
            return {}

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            global_data.ui_mgr.close_ui(self.get_name())

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    @staticmethod
    def check_red_point():
        return False

    def on_finalize_panel(self):
        self.process_events(False)
        self._disappearing = None
        self._mecha_bar_wrapper = None
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        if self._mecha_choose_widget:
            self._mecha_choose_widget.destroy()
            self._mecha_choose_widget = None
        if self._mecha_choose_widget2:
            self._mecha_choose_widget2.destroy()
            self._mecha_choose_widget2 = None
        if self._skin_choose_widget:
            self._skin_choose_widget.destroy()
            self._skin_choose_widget = None
        for ui_cls in self.ui_cls_list:
            ui_cls.destroy()
            ui_cls = None

        self.show_main_ui()
        reset_model_and_cam_pos()
        super(PVEMechaWidgetUI, self).on_finalize_panel()
        return