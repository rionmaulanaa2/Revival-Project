# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEItemWidget.py
from __future__ import absolute_import
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_effect_desc_text, get_effect_desc_text_without_mecha_info, get_bless_can_donate, show_pve_bless_btn_tips, show_pve_break_tips, get_bless_elem_desc, get_bless_elem_attr_conf, get_bless_elem_res, DEFAULT_BLESS_PANEL
from logic.gutils.role_head_utils import init_role_head
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex
import copy

class PVEBreakWidget(object):
    TEMPLATE = 'pve/breakthrough/i_pve_breakthrough_item'

    def __init__(self, panel, show_desc_tips=True):
        self.panel = panel
        self.cur_level = 0
        self.mecha_id = 0
        self.slot_conf = None
        self.show_desc_tips = show_desc_tips
        self.init_params()
        self.init_widget()
        return

    def init_params(self):
        self.widget = None
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)

    def isVisible(self):
        return self.widget and self.widget.isVisible()

    def setVisible(self, visible):
        self.widget and self.widget.setVisible(visible)

    def update_widget(self, mecha_id, slot_id, level, pve_mecha_base_info={}):
        if not self.widget:
            return
        else:
            self.mecha_id = mecha_id
            self.break_conf = confmgr.get('mecha_breakthrough_data', str(mecha_id), default=None)
            self.cur_level = level
            self.slot_conf = self.break_conf[str(slot_id)]
            conf = self.slot_conf[str(level)]
            self.widget.setVisible(True)
            self.widget.img_item.SetDisplayFrameByPath('', conf['icon'])
            self.widget.lab_name.SetString(get_text_by_id(conf['name_id']))
            self.widget.lab_describe.SetString(get_effect_desc_text(conf['desc_id'], conf.get('attr_text_conf', []), pve_mecha_base_info=pve_mecha_base_info))
            self.widget.lab_type.SetString(get_text_by_id(conf['type_text_id']))
            self.widget.list_dot.SetInitCount(5)
            for i, btn in enumerate(self.widget.list_dot.GetAllItem()):
                if i < level:
                    btn.btn_dot.SetSelect(True)
                else:
                    btn.btn_dot.SetSelect(False)

            self.update_show_break_tips()
            return

    def update_show_break_tips(self):
        if not self.show_desc_tips:
            self.widget.btn_describe.setVisible(False)
            return
        show_pve_break_tips(self.widget.btn_describe, self.cur_level, self.slot_conf)

    def clear(self):
        self.widget and self.widget.Destroy()
        self.widget = None
        return

    def destroy(self):
        global_data.ui_mgr.close_ui('PVEDescribeUI')
        self.clear()
        self.init_params()
        self.panel = None
        return


class PVEBlessWidget(object):
    TEMPLATE = 'pve/energy/i_pve_energy_item'
    TEAMMATE_TEMPLATE = 'pve/shop/i_pve_give_choose'

    def __init__(self, panel, show_desc_tips=True):
        self.panel = panel
        self.show_desc_tips = show_desc_tips
        self.init_params()
        self.init_widget()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self.widget = None
        self.teammate_ref = {}
        self.teammate_widget = None
        self.teammate_infos = None
        self.cur_select_bless_id = None
        self.bless_name = None
        self.char_name = None
        self.cur_level = 0
        self.bless_conf = confmgr.get('bless_data', default=None)
        self.bless_donate_left_cnt = 0
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)
        self.teammate_widget = global_data.uisystem.load_template_create(self.TEAMMATE_TEMPLATE, self.widget)
        self.teammate_widget.setVisible(True)

    def isVisible(self):
        return self.widget and self.widget.isVisible()

    def setVisible(self, visible):
        self.widget and self.widget.setVisible(visible)
        if not visible:
            self.teammate_widget and self.teammate_widget.setVisible(False)

    def init_ui_event(self):

        @self.widget.btn_give.unique_callback()
        def OnClick(btn, touch):
            if not self.cur_select_bless_id:
                return
            if not global_data.cam_lplayer:
                return
            if self.bless_donate_left_cnt <= 0:
                global_data.game_mgr.show_tip(get_text_by_id(531))
                return
            if not get_bless_can_donate(self.cur_select_bless_id):
                global_data.game_mgr.show_tip(get_text_by_id(521).format(bless=self.bless_name))
                return
            if not self.has_live_teammate():
                return
            if len(self.teammate_infos) == 1:
                donate_id = list(self.teammate_infos.keys())[0]
                self.char_name = self.teammate_infos[donate_id].get('char_name', '')
                self.donate_bless(donate_id)
            else:
                self.update_teammate_widget()

    def process_events(self, is_bind):
        econf = {'on_pve_notify_donate_bless_result': self.on_pve_notify_donate_bless_result
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def on_pve_notify_donate_bless_result(self, *args):
        self.bless_donate_left_cnt -= 1

    def donate_bless(self, donate_id):
        global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'request_pve_donate_bless', (donate_id, self.cur_select_bless_id))
        self.widget.btn_give.SetShowEnable(self.bless_donate_left_cnt > 0)
        self.setVisible(False)
        global_data.emgr.on_pve_donate_bless.emit(self.char_name)

    def update_teammate_widget(self):
        if not self.teammate_widget or not self.teammate_infos:
            return
        self.teammate_widget.setVisible(True)
        list_item = self.teammate_widget.list_item
        list_item.DeleteAllSubItem()
        list_item.SetInitCount(len(self.teammate_infos))
        for index, teammate_id in enumerate(self.teammate_infos):
            teammate_info = self.teammate_infos[teammate_id]
            item = list_item.GetItem(index)
            btn_give = item.btn_give
            init_role_head(item.temp_role, teammate_info.get('head_frame'), teammate_info.get('head_photo'))
            self.char_name = teammate_info.get('char_name', '')
            item.lab_name.SetString(self.char_name)
            teammate = self.get_entity(teammate_id)
            lab_name2 = item.lab_name2
            if teammate:
                mecha_type = teammate.ev_g_get_bind_mecha_type()
                if mecha_type:
                    lab_name2.SetString(get_lobby_item_name(battle_id_to_mecha_lobby_id(mecha_type)))
                    lab_name2.setVisible(True)
                    btn_give.SetEnable(True)
                else:
                    lab_name2.setVisible(False)
                    btn_give.SetEnable(False)
            else:
                lab_name2.setVisible(False)
                btn_give.SetEnable(False)

            @btn_give.unique_callback()
            def OnClick(btn, touch, teammate_id=teammate_id):
                self.donate_bless(teammate_id)

    def update_show_bless_tips(self):
        if not self.show_desc_tips:
            self.widget.btn_describe.setVisible(False)
            return
        show_pve_bless_btn_tips(self.widget.btn_describe, self.cur_select_bless_id, self.cur_level)

    def update_widget(self, bless_id, bless_level, pve_mecha_base_info={}, bless_donate_left_cnt=0, eid=global_data.player.id):
        if not self.widget:
            return
        else:
            if not global_data.player:
                return
            self.cur_select_bless_id = bless_id
            self.cur_level = bless_level
            self.bless_donate_left_cnt = bless_donate_left_cnt
            if self.bless_donate_left_cnt is None:
                self.bless_donate_left_cnt = 0
            conf = self.bless_conf.get(str(bless_id))
            self.widget.setVisible(True)
            self.bless_name = get_text_by_id(conf['name_id'])
            self.widget.lab_name.SetString(self.bless_name)
            self.widget.img_item.SetDisplayFrameByPath('', conf.get('icon', ''))
            if not global_data.player.logic and not pve_mecha_base_info:
                self.widget.lab_introduce.SetString(get_effect_desc_text_without_mecha_info(conf['desc_id'], conf.get('attr_text_conf', []), bless_level))
            else:
                self.widget.lab_introduce.SetString(get_effect_desc_text(conf['desc_id'], conf.get('attr_text_conf', []), bless_level, pve_mecha_base_info))
            self.update_show_bless_tips()
            max_level = conf.get('max_level', 1)
            if max_level == 1:
                self.widget.list_dot.setVisible(False)
            else:
                self.widget.list_dot.setVisible(True)
                self.widget.list_dot.DeleteAllSubItem()
                self.widget.list_dot.SetInitCount(max_level)
                for i, btn in enumerate(self.widget.list_dot.GetAllItem()):
                    if i < bless_level:
                        btn.btn_dot.SetEnable(True)
                        btn.btn_dot.SetSelect(True)
                    else:
                        btn.btn_dot.SetEnable(True)
                        btn.btn_dot.SetSelect(False)

            elem_id = conf.get('elem_id', None)
            if elem_id:
                self.widget.bar_describe.setVisible(True)
                self.widget.icon_type.setVisible(True)
                if not global_data.player.logic and not pve_mecha_base_info:
                    self.widget.lab_describe.SetString(get_effect_desc_text_without_mecha_info(get_bless_elem_desc(elem_id), get_bless_elem_attr_conf(elem_id), 1))
                else:
                    self.widget.lab_describe.SetString(get_effect_desc_text(get_bless_elem_desc(elem_id), get_bless_elem_attr_conf(elem_id), 1, pve_mecha_base_info))
                _elem_icon, _elem_pnl = get_bless_elem_res(elem_id, ['icon', 'panel'])
                self.widget.icon_type.SetDisplayFrameByPath('', _elem_icon)
                self.widget.bar.SetFrames('', [_elem_pnl, _elem_pnl, _elem_pnl])
            else:
                self.widget.bar_describe.setVisible(False)
                self.widget.icon_type.setVisible(False)
                pic = DEFAULT_BLESS_PANEL
                self.widget.bar.SetFrames('', [pic, pic, pic])
            self.init_bless_donate_widget(eid)
            return

    def init_bless_donate_widget(self, eid):
        btn_give = self.widget.btn_give
        if not global_data.cam_lplayer or not global_data.player:
            btn_give.setVisible(False)
            return
        teammate_count = len(global_data.cam_lplayer.ev_g_teammate_infos())
        is_multi_player_team = teammate_count > 0
        if not global_data.ui_mgr.get_ui('PVEInfoUI') or not global_data.cam_lplayer or not global_data.player or eid != global_data.player.id or not is_multi_player_team:
            btn_give.setVisible(False)
            return
        self.teammate_infos = copy.deepcopy(global_data.cam_lplayer.ev_g_teammate_infos())
        is_mine = global_data.cam_lplayer.id == global_data.player.id
        btn_give.setVisible(is_mine)
        bless_can_donate = get_bless_can_donate(self.cur_select_bless_id)
        has_live_teammate = self.has_live_teammate()
        btn_give.SetShowEnable(bless_can_donate and self.bless_donate_left_cnt > 0 and has_live_teammate)

    def has_live_teammate(self):
        for teammate_id in self.teammate_infos.keys():
            teammate = self.get_entity(teammate_id)
            if teammate:
                mecha_type = teammate.ev_g_get_bind_mecha_type()
                if mecha_type:
                    return True

        return False

    def get_entity(self, tid):
        t_ent = None
        if tid in self.teammate_ref:
            t_ent = self.teammate_ref[tid]()
            if not (t_ent and t_ent.is_valid()):
                del self.teammate_ref[tid]
                t_ent = None
        if not t_ent:
            import weakref
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(tid)
            if ent and ent.logic:
                self.teammate_ref[tid] = weakref.ref(ent.logic)
                t_ent = ent.logic
        return t_ent

    def clear(self):
        self.teammate_widget and self.teammate_widget.Destroy()
        self.teammate_widget = None
        self.widget and self.widget.Destroy()
        self.widget = None
        return

    def destroy(self):
        self.process_events(False)
        self.clear()
        self.init_params()
        self.panel = None
        return


class PVEItemWidget(object):
    TEMPLATE = 'pve/breakthrough/i_pve_breakthrough_item'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()

    def init_params(self):
        self.widget = None
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)

    def isVisible(self):
        return self.widget and self.widget.isVisible()

    def setVisible(self, visible):
        self.widget and self.widget.setVisible(visible)

    def update_widget(self, conf):
        if not self.widget:
            return
        self.widget.setVisible(True)
        self.widget.setVisible(True)
        self.widget.img_item.SetDisplayFrameByPath('', conf['icon'])
        self.widget.lab_name.SetString(get_text_by_id(conf['name_id']))
        if not global_data.player.logic:
            self.widget.lab_describe.SetString(get_effect_desc_text_without_mecha_info(conf['desc_id'], conf.get('attr_text_conf', [])))
        else:
            self.widget.lab_describe.SetString(get_effect_desc_text(conf['desc_id'], conf.get('attr_text_conf', []), pve_mecha_base_info={}))
        self.widget.lab_type.setVisible(False)
        self.widget.list_dot.setVisible(False)

    def clear(self):
        self.widget and self.widget.Destroy()
        self.widget = None
        return

    def destroy(self):
        self.clear()
        self.init_params()
        self.panel = None
        return