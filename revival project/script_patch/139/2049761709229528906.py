# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBlessConfUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_CLOSE
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_NO_CRYSTAL_STONE
from logic.gutils.pve_utils import get_effect_desc_text, is_pve_ori_mecha_alive, show_pve_bless_btn_tips, get_bless_elem_desc, get_bless_elem_attr_conf, get_bless_elem_res, DEFAULT_BLESS_PANEL, stop_movement
from logic.gutils.template_utils import init_common_price, init_price_template
from logic.client.const import mall_const
from logic.gutils.item_utils import get_item_pic_by_item_no
from mobile.common.EntityManager import EntityManager
from logic.gcommon.time_utility import get_server_time
BLESS_GET = 0
BLESS_UP = 1
BLESS_REPLACE = 2

class PVEBlessConfUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/energy/pve_energy_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    BASE_MECHA_ICON_DIR = 'gui/ui_res_2/main/select_mecha'
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close',
       'btn_show.OnClick': 'on_show_bag',
       'btn_fresh.OnClick': 'on_fresh_bless'
       }
    REFRESH_DUR = 0.5

    def on_init_panel(self, *args):
        super(PVEBlessConfUI, self).on_init_panel(*args)
        self.init_params()
        self.init_ui()
        self.process_events(True)
        self.handle_cursor(True)
        self.panel.PlayAnimation('appear')
        stop_movement()

    def init_params(self):
        self.bless_list = []
        self.refresh_ts = 0

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pve_cost_crystal_stone': self.init_crystone_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_ui(self):
        self.panel.lab_title.SetString(get_text_by_id(380))
        self.panel.lab_tips.SetString(get_text_by_id(383))

    def on_finalize_panel(self):
        self.init_params()
        self.process_events(False)
        self.handle_cursor(False)
        super(PVEBlessConfUI, self).on_finalize_panel()

    def init_bless(self, confirm_id, bless_list, extra_data):
        self.confirm_id = confirm_id
        self.bless_list = bless_list
        self.box_entity_id = extra_data.get('box_ent_id', None)
        self.refresh_price = extra_data.get('refresh_price', 70)
        player = global_data.cam_lplayer
        if not player or not player.id:
            self.close()
            return
        else:
            self.init_panel()
            self.init_refresh()
            return

    def init_panel(self):
        self.init_crystone_widget()
        list_item = self.panel.nd_content.list_item
        list_item.SetInitCount(len(self.bless_list))
        for idx, bless_id in enumerate(self.bless_list):
            ui_item = list_item.GetItem(idx)
            cur_level = global_data.cam_lplayer.ev_g_bless_level(bless_id)
            self.init_bless_card(ui_item, bless_id)

            @ui_item.bar.unique_callback()
            def OnClick(_btn, _touch, _bless_id=bless_id):
                self.try_get_bless(_bless_id)

            show_pve_bless_btn_tips(ui_item.btn_describe, bless_id, cur_level)

    def init_crystone_widget(self):
        self.panel.list_money.SetInitCount(1)
        price_widget = self.panel.list_money.GetItem(0)
        crystone_cnt = global_data.player.logic.ev_g_crystal_stone()
        crystone_cnt = crystone_cnt if crystone_cnt is not None else 0
        price_widget.btn_add.setVisible(False)
        init_common_price(price_widget, crystone_cnt, '4_%s' % ITEM_NO_CRYSTAL_STONE)
        return

    def init_bless_card(self, ui_item, bless_id):
        bless_conf = confmgr.get('bless_data', str(bless_id), default=None)
        if not bless_conf:
            return
        else:
            ui_item.lab_name.SetString(bless_conf['name_id'])
            ui_item.img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
            max_level = bless_conf.get('max_level', 1)
            cur_level = global_data.cam_lplayer.ev_g_bless_level(bless_id)
            desc_id = bless_conf['desc_id']
            attr_conf = bless_conf.get('attr_text_conf', [])
            ui_item.lab_introduce.SetString(get_effect_desc_text(desc_id, attr_conf, min(max_level, cur_level + 1)))
            if max_level == 1:
                ui_item.list_dot.setVisible(False)
            else:
                ui_item.list_dot.setVisible(True)
                ui_item.list_dot.DeleteAllSubItem()
                ui_item.list_dot.SetInitCount(max_level)
                for i, btn in enumerate(ui_item.list_dot.GetAllItem()):
                    if i < cur_level:
                        btn.btn_dot.SetEnable(True)
                        btn.btn_dot.SetSelect(True)
                    elif i == cur_level:
                        btn.btn_dot.SetEnable(False)
                    else:
                        btn.btn_dot.SetEnable(True)
                        btn.btn_dot.SetSelect(False)

            elem_id = bless_conf.get('elem_id', None)
            if elem_id:
                ui_item.bar_describe.setVisible(True)
                elem_desc_id = get_bless_elem_desc(elem_id)
                elem_attr_conf = get_bless_elem_attr_conf(elem_id)
                ui_item.bar_describe.lab_describe.SetString(get_effect_desc_text(elem_desc_id, elem_attr_conf, 1))
                elem_icon, elem_pnl_icon = get_bless_elem_res(elem_id, ['icon', 'panel'])
                ui_item.icon_type.SetDisplayFrameByPath('', elem_icon)
                ui_item.bar.SetFrames('', [elem_pnl_icon, elem_pnl_icon, elem_pnl_icon])
                ui_item.icon_type.setVisible(True)
            else:
                ui_item.bar_describe.setVisible(False)
                ui_item.icon_type.setVisible(False)
                pic = DEFAULT_BLESS_PANEL
                ui_item.bar.SetFrames('', [pic, pic, pic])
            return

    def try_get_bless(self, bless_id):
        if not global_data.cam_lplayer:
            return
        if not is_pve_ori_mecha_alive():
            return
        cur_level = global_data.cam_lplayer.ev_g_bless_level(bless_id)
        max_level = confmgr.get('bless_data', str(bless_id), default={}).get('max_level', 1)
        if cur_level + 1 > max_level:
            return
        self.get_bless(bless_id)

    def get_bless(self, bless_id):
        global_data.battle.on_client_confirm(self.confirm_id, bless_id)
        self.on_close()

    def init_refresh(self):
        item_widget = self.panel.btn_fresh.temp_price.temp_price.GetItem(0)
        price_info = {'original_price': self.refresh_price,
           'goods_payment': '4_%s' % ITEM_NO_CRYSTAL_STONE
           }
        init_price_template(price_info, item_widget, adjust_pos=False)

        @self.panel.btn_fresh.unique_callback()
        def OnClick(_btn, _touch):
            self.on_fresh_bless()

    def on_fresh_bless(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            if global_data.player.logic.ev_g_crystal_stone() < self.refresh_price:
                return
            ts = get_server_time()
            if ts - self.refresh_ts > self.REFRESH_DUR:
                self.refresh_ts = ts
            else:
                global_data.game_mgr.show_tip(get_text_by_id(503))
                return
            box = EntityManager.getentity(self.box_entity_id)
            if box and box.logic:
                box.logic.send_event('E_CALL_SYNC_METHOD', 'refresh_pve_bless', (global_data.player.id,))
                global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_shop_refresh', None)
            return

    def on_close(self, *args):
        self.panel.PlayAnimation('disappear')
        delay = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.SetTimeOut(delay, lambda : self.close())

    def handle_cursor(self, ret):
        if global_data.mouse_mgr:
            if ret:
                global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
            else:
                global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def on_show_bag(self, *args):
        ui = global_data.ui_mgr.get_ui('PVEInfoUI')
        ui and ui.close()
        global_data.ui_mgr.show_ui('PVEInfoUI', 'logic.comsys.control_ui')