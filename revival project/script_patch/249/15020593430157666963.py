# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/BriefRankUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from logic.gcommon import time_utility
import weakref
POINT_BG_PIC = [
 'gui/ui_res_2/battle/point_mode/bar_point_normal.png',
 'gui/ui_res_2/battle/point_mode/bar_point_eliminate.png']
MORE_POINT_BG_PIC = [
 'gui/ui_res_2/battle/point_mode/img_more_normal_.png',
 'gui/ui_res_2/battle/point_mode/img_more_red_.png']
RANK_PIC = [
 'gui/ui_res_2/battle/point_mode/icon_1st.png',
 'gui/ui_res_2/battle/point_mode/icon_2nd.png',
 'gui/ui_res_2/battle/point_mode/icon_3rd.png']

class CListViewMgr:
    UI_MAX_NUM = {'battle_point/i_more_point': 5,'battle_point/i_my_point': 1,
       'battle_point/i_other_point': 10
       }

    def __init__(self, ref_panel):
        self.ref_panel = ref_panel
        self.item_pool = {}
        self.item_conf = {}

    def on_destroy(self):
        for items in six.itervalues(self.item_pool):
            for item in items:
                item.release()

        self.item_pool = {}
        self.item_conf = {}

    def get_free_item(self, uiname, index=None, bRefresh=True):
        panel = self.ref_panel()
        if not panel:
            return
        listobj = panel.point_list
        if uiname in self.item_pool and self.item_pool[uiname]:
            item_widget = self.item_pool[uiname].pop()
            listobj.AddControl(item_widget, index=index, bRefresh=bRefresh)
            item_widget.release()
            return item_widget
        if uiname not in self.item_conf:
            self.item_conf[uiname] = global_data.uisystem.load_template(uiname)
        item_widget = listobj.AddItem(self.item_conf[uiname], index=index, bRefresh=bRefresh)
        item_widget._pick_ui_name = uiname
        return item_widget

    def recycle_item(self):
        panel = self.ref_panel()
        if not panel:
            return
        listobj = panel.point_list
        for item_widget in listobj.GetAllItem():
            if item_widget._pick_ui_name not in self.item_pool:
                self.item_pool[item_widget._pick_ui_name] = []
            if len(self.item_pool[item_widget._pick_ui_name]) < self.UI_MAX_NUM.get(item_widget._pick_ui_name, 50):
                item_widget.retain()
                item_widget.removeFromParent()
                self.item_pool[item_widget._pick_ui_name].append(item_widget)
            else:
                item_widget.Destroy()

        listobj.TransferAllSubItem()


from common.const import uiconst

class BriefRankUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_point/fight_point'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        ui_obj = global_data.ui_mgr.get_ui('RankListUI')
        if ui_obj:
            self.hide()
        self.lview_mgr = CListViewMgr(weakref.ref(self))
        self.lview = self.panel.point_list
        self.lview.setTouchEnabled(False)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.panel.lab_time.StopTimerAction()
        self.is_playanimation = False
        self.in_warning = False

    def init_parameters(self):
        self.in_warning = False
        self.is_playanimation = False
        self.warning_rank = 0
        self.first_score = 0
        self.rank_data = []
        self.cache_ui_pos = {}
        for ui_name in ['nd_time', 'img_warn']:
            ui_obj = getattr(self.panel, ui_name)
            if ui_obj:
                self.cache_ui_pos[ui_name] = ui_obj.GetPosition()

    def init_event(self):
        pass

    def refresh_listview(self, next_stage_timestamp, elimination_data, first_score, rank_data):
        self.lview_mgr.recycle_item()
        self.on_count_down(next_stage_timestamp)
        if elimination_data:
            self.warning_rank, warning_score = elimination_data
        else:
            self.warning_rank, warning_score = (0, 0)
        self.first_score = first_score
        self.rank_data = rank_data
        if not self.rank_data:
            return
        ldatas = []
        fst = self.rank_data[0][0]
        lst = self.rank_data[-1][0]
        if fst > 1:
            ldatas.append([1, -1, self.first_score])
            if fst - 1 > 1:
                if self.warning_rank and self.warning_rank - 1 > 1 or not self.warning_rank:
                    ldatas.append([fst, -1, -1])
        if self.warning_rank and fst > self.warning_rank:
            ldatas.append([self.warning_rank, -1, warning_score])
            if fst - self.warning_rank > 1:
                ldatas.append([fst, -1, -1])
        ldatas.extend(rank_data)
        if self.warning_rank and self.warning_rank > lst:
            if self.warning_rank - lst > 1:
                ldatas.append([self.warning_rank, -1, -1])
            ldatas.append([self.warning_rank, -1, warning_score])
        for data in ldatas:
            self.add_item_elem(data)

        center_index = self.lview.GetItemCount() / 2
        w, _ = self.lview._container.GetContentSize()
        contentSize = self.lview.GetInnerContentSize()
        x_off = max(1.0 * (contentSize.width - w) / 2, 0)
        self.lview.SetContentOffset(ccp(x_off, 0))
        self.adjust_ui_pos(x_off)

    def adjust_ui_pos(self, x_off):
        for ui_name in ['nd_time', 'img_warn']:
            ui_obj = getattr(self.panel, ui_name)
            if ui_obj:
                x, y = self.cache_ui_pos.get(ui_name, (0, 0))
                ui_obj.SetPosition(x + x_off, y)

    def add_item_elem(self, data, is_back_item=False):
        rank, group_id, point = data
        is_my_rank = False
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_group_id() == group_id:
            is_my_rank = True
            if self.warning_rank and rank >= self.warning_rank:
                self.in_warning = True
            else:
                self.in_warning = False
            self.panel.img_warn.setVisible(self.in_warning)
        if point == -1:
            ui = 'battle_point/i_more_point'
        else:
            ui = 'battle_point/i_my_point' if is_my_rank else 'battle_point/i_other_point'
        if is_back_item:
            item_widget = self.lview_mgr.get_free_item(ui)
        else:
            item_widget = self.lview_mgr.get_free_item(ui, 0)
        if point == -1:
            pic_idx = 1 if self.warning_rank and rank > self.warning_rank else 0
            item_widget.img_more.SetDisplayFrameByPath('', MORE_POINT_BG_PIC[pic_idx])
        else:
            item_widget.lab_rank.setString(str(rank))
            item_widget.lab_point.setString(str(point))
            pic_idx = 1 if self.warning_rank and rank >= self.warning_rank else 0
            item_widget.bar_rank.SetDisplayFrameByPath('', POINT_BG_PIC[pic_idx])
            if rank - 1 < 3:
                item_widget.img_rank.SetDisplayFrameByPath('', RANK_PIC[rank - 1])
                item_widget.img_rank.setVisible(True)
            else:
                item_widget.img_rank.isVisible() and item_widget.img_rank.setVisible(False)

    def on_count_down(self, next_stage_timestamp):
        alltime = next_stage_timestamp - time_utility.get_server_time()

        def refresh_time(pass_time):
            lefttime = int(alltime - pass_time)
            if lefttime == 0:
                self._clear_time()
            elif lefttime <= 30:
                if not self.is_playanimation:
                    self.panel.PlayAnimation('eliminate')
                    self.is_playanimation = True
                if self.panel.img_warn.isVisible():
                    self.panel.img_warn.setVisible(False)
                if not self.panel.nd_time.isVisible():
                    self.panel.nd_time.setVisible(True)
            else:
                if self.is_playanimation:
                    self.panel.StopAnimation('eliminate')
                    self.is_playanimation = False
                if self.panel.nd_time.isVisible():
                    self.panel.nd_time.setVisible(False)
            self.panel.lab_time.SetString('%dS' % lefttime)

        def refresh_time_finsh():
            self._clear_time()

        self._clear_time()
        if alltime > 0:
            self.panel.lab_time.TimerAction(refresh_time, alltime, callback=refresh_time_finsh)

    def _clear_time(self):
        self.panel.lab_time.StopTimerAction()
        self.panel.StopAnimation('eliminate')
        self.is_playanimation = False
        if self.panel.nd_time.isVisible():
            self.panel.nd_time.setVisible(False)
        if self.in_warning and not self.panel.img_warn.isVisible():
            self.panel.img_warn.setVisible(True)