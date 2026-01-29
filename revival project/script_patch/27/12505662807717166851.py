# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathRogueChooseUI.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.cdata.rogue_gift_config import get_gift_data
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import rogue_utils
from logic.gutils import item_utils
from common.const import uiconst

class DeathRogueChooseUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/open_rogue'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    BASE_MECHA_ICON_DIR = 'gui/ui_res_2/main/select_mecha'
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'
       }

    def on_init_panel(self, *args):
        super(DeathRogueChooseUI, self).on_init_panel(*args)
        self.init_rogue_candidates()
        self.init_cursor()

    def init_cursor(self):
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def on_finalize_panel(self):
        super(DeathRogueChooseUI, self).on_finalize_panel()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def init_buy(self, time_key):
        battle_data = global_data.death_battle_data
        if not battle_data.refresh_conf_list:
            self.panel.btn_refresh.setVisible(False)
        else:
            self.panel.btn_refresh.setVisible(True)
            tmp_times = battle_data.rogue_refresh_times.get(global_data.cam_lplayer.id, 0)
            t = min(tmp_times, len(battle_data.refresh_conf_list) - 1)
            lab_price = self.panel.temp_price.temp_price.GetItem(0).lab_price
            player = global_data.cam_lplayer.get_owner()
            if player.id != global_data.player.id:
                return
        diamond = player.get_diamond() - player.get_battle_tmp_consume('diamond')
        consume = battle_data.refresh_conf_list[t]
        lab_price.SetString(str(consume))
        max_times = battle_data.max_refresh_time or 99999
        if diamond < consume:
            lab_price.SetColor('#SR')
        else:
            if tmp_times >= max_times:
                self.panel.nd_price.setVisible(False)
                self.panel.lab_limit.setVisible(True)
                self.panel.btn_refresh.SetEnable(False)

            @self.panel.btn_refresh.unique_callback()
            def OnClick(btn, touch):
                if not global_data.player or not global_data.player.logic:
                    return
                if diamond < consume:
                    global_data.player.notify_client_message((get_text_by_id(19788),))
                elif tmp_times >= max_times:
                    global_data.player.notify_client_message((get_text_by_id(83342),))
                else:
                    global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'refresh_death_rogue_gift', (time_key,))

    def init_rogue_candidates(self):
        player = global_data.cam_lplayer
        if not player or not player.id:
            self.panel.setVisible(False)
            return
        else:
            player_id = player.id
            total_rogue_gift_candidates = global_data.death_battle_data.rogue_gift_candidates.get(player_id, {})
            total_selected_rogue_gifts = global_data.death_battle_data.selected_rogue_gifts.get(player_id, {})
            time_idxs = six_ex.keys(total_rogue_gift_candidates)
            time_idxs.sort()
            target_idx = None
            for idx in time_idxs:
                if idx in total_selected_rogue_gifts:
                    continue
                target_idx = idx
                break

            if not target_idx:
                log_error('invalid rogue gift to choose: total_candidates:%s, total_selected:%s' % (total_rogue_gift_candidates, total_selected_rogue_gifts))
                return
            self.init_buy(target_idx)
            target_candidates = total_rogue_gift_candidates[target_idx]
            total_len = len(target_candidates)
            list_item = self.panel.list_item
            list_item.SetInitCount(total_len)
            for i in range(total_len):
                item_widget = list_item.GetItem(i)
                gift_id = target_candidates[i]
                gift_data = get_gift_data().get(gift_id)
                if not gift_data:
                    continue
                item_widget.lab_name.SetString(get_text_by_id(gift_data['name_id']))
                item_widget.lab_introduce.SetString(rogue_utils.get_gift_desc_text(gift_id))
                item_widget.icon.SetDisplayFrameByPath('', gift_data['icon_path'])
                item_widget.bg.SetDisplayFrameByPath('', rogue_utils.get_rogue_quality_bg(gift_id))
                mecha_id = gift_data.get('mecha_id')
                if not mecha_id:
                    item_widget.img_mecha.setVisible(False)
                    item_widget.lab_mecha.setVisible(False)
                    item_widget.img_tag.setVisible(False)
                else:
                    item_widget.lab_mecha.SetString(item_utils.get_mecha_name_by_id(mecha_id))
                    mecha_path = self.BASE_MECHA_ICON_DIR + '/img_topbar_mecha_%s.png' % mecha_id
                    item_widget.img_mecha.SetDisplayFrameByPath('', mecha_path)

                @item_widget.btn_choose.unique_callback()
                def OnClick(btn, touch, target_idx=target_idx, gift_idx=i):
                    if not global_data.player or not global_data.player.logic:
                        return
                    global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'choose_death_rogue_gift', (target_idx, gift_idx))
                    global_data.emgr.rogue_gift_local_choose.emit()
                    self.close()

            return

    def on_click_btn_close(self, btn, touch):
        self.close()