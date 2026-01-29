# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Granbelm/GranbelmRuneListUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import GRANBELM_MAX_RUNE_COUNT
from logic.gutils import granbelm_utils
from common.const import uiconst

class GranbelmRuneListUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_moon/battle_talent_choose_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_click_close',
       'nd_close.OnClick': '_on_click_close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(GranbelmRuneListUI, self).on_init_panel()
        self.init_params()
        self.process_events(True)
        self.init_list()
        rune_count = global_data.cam_lplayer.ev_g_granbelm_rune_count()
        self.update_rune_count(rune_count, True)
        self.panel.PlayAnimation('appear')

    def init_params(self):
        self._rune_ability_count = 5

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_granbelm_rune_count': self.update_rune_count
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_list(self):
        ui_list = self.panel.nd_content.nd_shop.list_item
        ui_list.SetInitCount(self._rune_ability_count)
        for index, ui_item in enumerate(ui_list.GetAllItem()):
            conf = granbelm_utils.get_rune_ability_display_dict(index)
            name = conf.get('name')
            path = conf.get('path')
            desc = conf.get('desc')
            ui_item.lab_sort.SetString(get_text_by_id(name))
            ui_item.nd_item.img_talent.SetDisplayFrameByPath('', path)
            ui_item.lab_describe.SetString(get_text_by_id(desc))
            rune_id = conf.get('id')

            @ui_item.btn_choose.unique_callback()
            def OnClick(_btn, _touch, _id=rune_id):
                self._try_apply_rune_ability(_id)

    def update_rune_count(self, rune_count, is_self_inc):
        self.panel.lab_num.SetString(str(rune_count) + '/200')

    def _try_apply_rune_ability(self, rune_id):
        if not global_data.cam_lplayer:
            self.close()
            return
        rune_count = global_data.cam_lplayer.ev_g_granbelm_rune_count()
        if rune_count < GRANBELM_MAX_RUNE_COUNT:
            if global_data.gran_sur_battle_mgr.is_sub_mode:
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19817))
            else:
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19630))
        else:
            cur_rune_id = global_data.player.logic.ev_g_granbelm_rune_id()
            if cur_rune_id:
                return
            global_data.player.get_battle().call_soul_method('apply_rune_ability', ({'rune_id': rune_id},))
            self.close()

    def _on_click_close(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.process_events(False)
        super(GranbelmRuneListUI, self).on_finalize_panel()