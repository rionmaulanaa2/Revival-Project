# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBreakConfUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_CLOSE
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_effect_desc_text, show_pve_break_tips, stop_movement
from logic.gutils.template_utils import set_ui_show_picture
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id

class PVEBreakConfUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/breakthrough/pve_breakthrough_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close',
       'btn_show.OnClick': 'on_show_info'
       }

    def on_init_panel(self, *args):
        super(PVEBreakConfUI, self).on_init_panel(*args)
        self.init_params()
        self.process_events(True)
        self.handle_cursor(True)
        self.panel.PlayAnimation('appear')
        self.init_ui()
        stop_movement()

    def init_params(self):
        self.mecha_id = 8001
        if global_data.player and global_data.player.logic:
            self.mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
        self.mecha_item_id = battle_id_to_mecha_lobby_id(self.mecha_id)
        self.skin_id = global_data.player.get_pve_using_mecha_skin(self.mecha_item_id)
        self.conf = confmgr.get('mecha_breakthrough_data', str(self.mecha_id), default=None)
        self.confirm_id = None
        return

    def init_ui(self):
        self.panel.lab_title.SetString(get_text_by_id(381))
        self.panel.lab_tips.SetString(get_text_by_id(382))
        set_ui_show_picture(self.skin_id, mecha_nd=self.panel.temp_pic)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_events(False)
        self.handle_cursor(False)
        super(PVEBreakConfUI, self).on_finalize_panel()

    def init_break(self, confirm_id, break_list, extra_data):
        if not global_data.player or not global_data.player.logic:
            return
        self.confirm_id = confirm_id
        cur_data = global_data.player.logic.ev_g_mecha_breakthrough_data()
        self.panel.list_item.SetInitCount(len(break_list))
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            slot = break_list[idx]
            ori_level = cur_data.get(str(slot), 0)
            cur_level = ori_level + 1
            conf = self.conf.get(str(slot), {})
            ori_conf = conf.get(str(ori_level), {})
            cur_conf = conf.get(str(cur_level), {})
            is_level_max = False
            ret_conf = cur_conf
            if not cur_conf:
                ret_conf = ori_conf
                is_level_max = True
            name_text = get_text_by_id(ret_conf['name_id'])
            desc_text = get_effect_desc_text(ret_conf['desc_id'], ret_conf.get('attr_text_conf', []))
            type_text = get_text_by_id(ret_conf['type_text_id'])
            ui_item.lab_name.SetString(name_text)
            ui_item.lab_describe.SetString(desc_text)
            ui_item.lab_type.SetString(type_text)
            ui_item.list_dot.DeleteAllSubItem()
            ui_item.list_dot.SetInitCount(len(conf))
            for i, btn in enumerate(ui_item.list_dot.GetAllItem()):
                if i + 1 <= ori_level:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(True)
                elif i + 1 == cur_level:
                    btn.btn_dot.SetEnable(False)
                else:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(False)

            ui_item.img_item.SetDisplayFrameByPath('', ret_conf['icon'])
            show_pve_break_tips(ui_item.btn_describe, ori_level, conf)

            @ui_item.bar.unique_callback()
            def OnClick(_layer, _touch, _slot=slot, _is_max=is_level_max):
                if _is_max:
                    global_data.game_mgr.show_tip(get_text_by_id(83492))
                    return
                break_id = int(_slot)
                if global_data.battle:
                    global_data.battle.on_client_confirm(self.confirm_id, break_id)
                self.on_close()

        if not break_list:
            self.panel.nd_content.nd_get_all.setVisible(True)
        else:
            self.panel.nd_content.nd_get_all.setVisible(False)
        self.init_ui()

    def on_close(self, *args):
        self.panel.PlayAnimation('disappear')
        delay = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.SetTimeOut(delay, lambda : self.close())

    def on_show_info(self, *args):
        ui = global_data.ui_mgr.get_ui('PVEInfoUI')
        ui and ui.close()
        global_data.ui_mgr.show_ui('PVEInfoUI', 'logic.comsys.control_ui')

    def handle_cursor(self, ret):
        if global_data.mouse_mgr:
            if ret:
                global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
            else:
                global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)