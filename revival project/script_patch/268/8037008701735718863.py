# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/SkinDefineImproveWidget.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_pic_by_item_no, get_lobby_item_rare_degree_pic_by_item_no, get_item_rare_degree, check_play_skin_improve_tips_anim, get_lobby_item_name, check_improvable_skin_diff_appearance
from logic.gutils.role_skin_utils import get_skin_improved_sfx_item_id
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN
from common.cfg import confmgr
VX_SKIN_ITEM_ND_NAMES = [ 'vx_items_{}'.format(i) for i in range(1, 4) ]
VX_DECORATION_ITEM_ND_NAMES = [ 'vx_items_{}'.format(i) for i in range(4, 12) ]
IMPROVED_SKIN_SFX_PIC_PATH_FORMAT = 'gui/ui_res_2/item/interaction/{}.png'

class SkinDefineImproveWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'weapon_sfx_change': self.weapon_sfx_change,
           'player_item_update_event_with_id': self.on_buy_good_success
           }
        super(SkinDefineImproveWidget, self).__init__(parent, panel)
        self.role_id = 0
        self.top_skin_id = 0
        self.all_collect_items = []
        self.collect_item_total_count = 0
        self.improved_skin_sfx_item = None
        self.previewing_skin_sfx = False
        self.all_skin_items = []
        self.all_decoration_items = []
        self.panel.btn_equip.setVisible(False)
        self.panel.btn_lock.setVisible(False)
        return

    def _init_item(self, nd, item_id):
        path = get_lobby_item_pic_by_item_no(item_id)
        nd.item.SetDisplayFrameByPath('', path)
        rare_degree = get_item_rare_degree(item_id, ignore_imporve=True)
        nd.img_frame.SetDisplayFrameByPath('', get_lobby_item_rare_degree_pic_by_item_no(item_id, 1, is_use_dark_back=True, force_rare_degree=rare_degree))

        @nd.btn_choose.unique_callback()
        def OnClick(btn, touch):
            position = touch.getLocation()
            show_jump = global_data.player.get_item_num_by_no(item_id) <= 0
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position, extra_info={'show_jump': show_jump,
               'force_rare_degree': rare_degree})
            return

    def on_buy_good_success(self, item_no):
        if item_no in self.all_collect_items:
            self.refresh_all_content()

    def _init_all_content(self):
        skin_count = len(self.all_skin_items)
        self.panel.list_skin.SetInitCount(skin_count)
        for index, item_id in enumerate(self.all_skin_items):
            nd_item = self.panel.list_skin.GetItem(index)
            self._init_item(nd_item, item_id)

        for i, nd_name in enumerate(VX_SKIN_ITEM_ND_NAMES):
            nd = getattr(self.panel, nd_name, None)
            nd and nd.setVisible(i < skin_count)

        decoration_count = len(self.all_decoration_items)
        self.panel.list_decoration.SetInitCount(decoration_count)
        for index, item_id in enumerate(self.all_decoration_items):
            nd_item = self.panel.list_decoration.GetItem(index)
            self._init_item(nd_item, item_id)

        for i, nd_name in enumerate(VX_DECORATION_ITEM_ND_NAMES):
            nd = getattr(self.panel, nd_name, None)
            nd and nd.setVisible(i < decoration_count)

        @self.panel.nd_item_content.unique_callback()
        def OnClick(*args):
            unlocked = global_data.player.get_item_num_by_no(self.improved_skin_sfx_item) > 0
            preview_skin_id = self.parent.get_preview_skin_id()
            if unlocked:
                skin_item = global_data.player.get_item_by_no(preview_skin_id)
                equip_dict = {}
                if skin_item and skin_item.get_weapon_sfx():
                    equip_dict[preview_skin_id] = None
                else:
                    self.panel.PlayAnimation('click')
                    equip_dict[preview_skin_id] = get_skin_improved_sfx_item_id(preview_skin_id)
                global_data.player.try_equip_role_sfx(equip_dict)
            else:
                self.previewing_skin_sfx = not self.previewing_skin_sfx
                global_data.emgr.show_skin_improved_sfx.emit(self.previewing_skin_sfx)
                from logic.gutils.role_skin_utils import check_update_improve_skin_decs
                check_update_improve_skin_decs(self.previewing_skin_sfx, self.parent.get_preview_skin_decoration(), self.parent.get_preview_skin_id())
                self.panel.img_frame.setVisible(self.previewing_skin_sfx)
            return

        self.panel.lab_item_name.SetString(get_lobby_item_name(self.improved_skin_sfx_item))
        self.panel.img_item.SetDisplayFrameByPath('', IMPROVED_SKIN_SFX_PIC_PATH_FORMAT.format(get_skin_improved_sfx_item_id(self.top_skin_id)))
        self.panel.lab_info.setVisible(check_improvable_skin_diff_appearance(self.top_skin_id))
        self.refresh_all_content()
        return

    def set_role_id(self, role_id, top_skin_id):
        self.role_id = role_id
        self.top_skin_id = top_skin_id
        conf = confmgr.get('role_info', 'RoleSkin', 'Content', str(top_skin_id))
        self.all_collect_items = conf['skin_improve_collected_items']
        self.collect_item_total_count = len(self.all_collect_items)
        self.improved_skin_sfx_item = conf['improved_skin_sfx_item']
        self.all_skin_items = []
        self.all_decoration_items = []
        for item_id in self.all_collect_items:
            if get_lobby_item_type(item_id) == L_ITEM_TYPE_ROLE_SKIN:
                self.all_skin_items.append(item_id)
            else:
                self.all_decoration_items.append(item_id)

        self._init_all_content()

    def show_panel(self, flag):
        if self.panel:
            self.panel.setVisible(flag)

    def on_hide(self):
        self.hide()

    def _refresh_collected_progress(self):
        collected_item_count = 0
        for item_id in self.all_collect_items:
            if global_data.player.get_item_num_by_no(item_id) > 0:
                collected_item_count += 1

        self.panel.lab_equip_applique_num.SetString('{}/{}'.format(collected_item_count, self.collect_item_total_count))

    def _refresh_item_got(self):
        get_item_num_by_no = global_data.player.get_item_num_by_no
        for index, item_id in enumerate(self.all_skin_items):
            nd_item = self.panel.list_skin.GetItem(index)
            nd_item.nd_lock.setVisible(get_item_num_by_no(item_id) <= 0)

        for index, item_id in enumerate(self.all_decoration_items):
            nd_item = self.panel.list_decoration.GetItem(index)
            nd_item.nd_lock.setVisible(get_item_num_by_no(item_id) <= 0)

    def _refresh_sfx_item_state(self):
        unlocked = global_data.player.get_item_num_by_no(self.improved_skin_sfx_item) > 0
        self.panel.nd_lcok.setVisible(not unlocked)
        if unlocked:
            skin_item = global_data.player.get_item_by_no(self.parent.get_preview_skin_id())
            equipped = True if skin_item and skin_item.get_weapon_sfx() else False
            self.panel.img_frame.setVisible(equipped)
            self.panel.img_get_tick.setVisible(equipped)
        else:
            self.panel.img_frame.setVisible(self.previewing_skin_sfx)

    def refresh_all_content(self):
        self._refresh_collected_progress()
        self._refresh_item_got()
        self._refresh_sfx_item_state()

    def weapon_sfx_change(self, item_id, value):
        if item_id != self.parent.get_preview_skin_id():
            return
        self._refresh_sfx_item_state()
        skin_item = global_data.player.get_item_by_no(self.parent.get_preview_skin_id())
        equipped = skin_item and skin_item.get_weapon_sfx()
        global_data.emgr.show_skin_improved_sfx.emit(equipped)
        from logic.gutils.role_skin_utils import check_update_improve_skin_decs
        check_update_improve_skin_decs(equipped, self.parent.get_preview_skin_decoration(), self.parent.get_preview_skin_id())

    def check_play_unlock_anim(self):
        if check_play_skin_improve_tips_anim(self.improved_skin_sfx_item):
            self.panel.PlayAnimation('show')

    def on_dress_change(self, new_skin_id):
        pass