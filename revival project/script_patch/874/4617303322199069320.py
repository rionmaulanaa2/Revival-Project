# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/MainRank.py
from __future__ import absolute_import
import six
import cc
import game3d
import common.const.uiconst
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from logic.gcommon import const
from logic.gcommon.item import item_const
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_const import rank_career_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.comsys.rank.BaseRankWidget import SLIDER_BTN_SIZE_BIG, SLIDER_BTN_SIZE_NORMAL
from logic.comsys.rank.MechaRankWidget import MechaRankWidget
from logic.comsys.rank.MechaRegionRankWidget import MechaRegionRankWidget
from logic.comsys.rank.DanRankWidget import DanRankWidget
from logic.comsys.rank.FashionRankWidget import FashionRankWidget
from logic.comsys.rank.CareerRankWidget import CareerRankWidget
from logic.comsys.rank.CharmRankWidget import CharmRankWidget
from logic.comsys.rank.SeasonRankWidget import SeasonRankWidget
from logic.comsys.rank.ScoreRankWidget import ScoreRankWidget, SCORE_RANK_WIDGET_TYPE_NORMAL, SCORE_RANK_WIDGET_TYPE_TDM, SCORE_RANK_WIDGET_TYPE_GVG
from logic.comsys.rank.DuelRankWidget import DuelRankWidget
from logic.comsys.rank.AssaultRankWidget import AssaultRankWidget
from logic.gcommon.common_const.pve_const import PVE_RANK_SPEED_PERSONAL, PVE_RANK_MECHA
from logic.comsys.battle.pve.rank.PVERankSpeedPageProxyUI import PVERankSpeedPageProxyUI
from logic.comsys.battle.pve.rank.PVERankMechaPageUI import PVERankMechaPageUI
from logic.comsys.rank.RankModelControler import RankSceneControler
from logic.comsys.battle.pve.rank.PVERankModelControler import PVERankModelControler
from logic.gutils import locate_utils
from logic.gutils import mouse_scroll_utils
ROTATE_FACTOR = 850
TAB_CAREER_BATTLE = 1
TAB_CAREER_MECHA = 2
TAB_MECHA_LOCATION = 3
MAIN_RANK_DEFAULT_TEXTURE = 'model_new/xuanjue/xuanjue_new/textures/geren_dibiao_011.tga'
PVE_RANK_TEXTURE = 'model_new/xuanjue/xuanjue_new/textures/pve_rank_bg.tga'
RANK_INFOS = [
 (
  15029, DanRankWidget, None, (15031, 15030), {})]
if locate_utils.is_open_location():
    if rank_const.is_world_mecha_region_rank():
        dec_txt = 15098
    else:
        dec_txt = 15064
    mecha_info = (
     15022, MechaRegionRankWidget, None, (dec_txt, 15046), {'subpage': TAB_MECHA_LOCATION})
else:
    mecha_info = (
     15022, MechaRankWidget, None, (15026, 15046), {})
RANK_INFOS.append(mecha_info)
pve_rank_info = [
 (
  635369,
  (
   (
    635370, PVERankSpeedPageProxyUI, None, (635410, 635409), {'is_pve': True,'rank_type': PVE_RANK_SPEED_PERSONAL,'scene_bg': PVE_RANK_TEXTURE,'model_ctrl': rank_const.PVE_RANK_MODEL_CTRL,'par_name': 'panel'}),
   (
    635373, PVERankMechaPageUI, None, (635412, 635411), {'is_pve': True,'rank_type': PVE_RANK_MECHA,'scene_bg': PVE_RANK_TEXTURE,'model_ctrl': rank_const.PVE_RANK_MODEL_CTRL,'par_name': 'panel'})))]
if locate_utils.is_open_location():
    RANK_INFOS.extend(pve_rank_info)
other_info = [
 (
  15002,
  (
   (
    10297, ScoreRankWidget, SCORE_RANK_WIDGET_TYPE_NORMAL, (15033, 15032), {}),
   (
    10296, ScoreRankWidget, SCORE_RANK_WIDGET_TYPE_TDM, (15044, 15045), {}),
   (
    15061, ScoreRankWidget, SCORE_RANK_WIDGET_TYPE_GVG, (15063, 15062), {}))),
 (
  15060,
  (
   (
    15059, CharmRankWidget, None, (15058, 15057), {}),
   (
    15018, FashionRankWidget, None, (15020, 15021), {}))),
 (
  81608,
  (
   (
    81609, CareerRankWidget, rank_career_const.RANK_TYPE_CAREER_BATTLE, (910009, 910008), {'subpage': TAB_CAREER_BATTLE}),
   (
    81610, CareerRankWidget, rank_career_const.RANK_TYPE_CAREER_MECHA, (910011, 910010), {'subpage': TAB_CAREER_MECHA}))),
 (
  15047, SeasonRankWidget, None, (15050, 15048), {}),
 (
  930013, DuelRankWidget, None, (930017, 930016), {}),
 (
  18000,
  (
   (
    18363, AssaultRankWidget, rank_const.RANK_TYPE_ASSAULT_KPM, (15099, 15100), {}),
   (
    18365, AssaultRankWidget, rank_const.RANK_TYPE_ASSAULT_DPM, (15099, 15100), {})))]
RANK_INFOS.extend(other_info)

class MainRank(BasePanel):
    PANEL_CONFIG_NAME = 'rank/rank_main'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_close_btn'
       }
    DEFAULT_SCENE_BG_TEXTURE = 'activity_leichong_sfx'
    DELAY_TIME = 0.3
    OPEN_SOUND_NAME = 'leaderboard'
    SUB_RANK_NUM = 3
    HOT_KEY_NEED_SCROLL_SUPPORT = True

    def on_init_panel(self, init_rank_tab=None, init_mecha_id=None):
        self.left_tab_list = self.panel.tab_list.tab_list
        self.cur_rank_panel = None
        self.cur_sub_panel = None
        self.left_sub_tab_list = None
        self._init_rank_tab = init_rank_tab
        self._init_mecha_id = init_mecha_id
        self.temp_list = None
        self.temp_position = self.panel.nd_list.temp_list.getPosition()
        self.panel.nd_list.temp_list.Destroy()
        self._panel_dict = {}
        self.cache_panel = {}
        self.cur_model_controler = None
        self.model_controler = {rank_const.MAIN_RANK_MODEL_CTRL: RankSceneControler(self),
           rank_const.PVE_RANK_MODEL_CTRL: PVERankModelControler(self)
           }
        self.delay_exec_id = None
        self._need_show_scene = False
        self.cur_bg_texture = None
        global_data.player.request_friend_rank_data()
        ac_list = [
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(lambda : self._show_scene(MAIN_RANK_DEFAULT_TEXTURE)),
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self._on_init_panel)]
        self.panel.runAction(cc.Sequence.create(ac_list))
        self.panel.temp_nativebest_btn.setVisible(False)
        self.panel.temp_title.setVisible(False)
        return

    def _on_init_panel(self):
        self._need_show_scene = True
        self.init_left_panel()
        self.hide_main_ui()
        global_data.emgr.leave_current_scene += self.on_leave_current_scene
        global_data.emgr.on_follow_result += self.on_follow_result
        global_data.emgr.on_undo_follow_result += self.on_undo_follow_result
        self.init_scroll()

    def jump_to_tab(self, page_tab):
        panel = self._panel_dict[page_tab]
        panel.btn.OnClick(None)
        return

    def _get_idx_by_rank_tab(self, rank_tab):
        for i, rank_data in enumerate(RANK_INFOS):
            rank_template = rank_data[1]
            if isinstance(rank_template, tuple):
                rank_data_tuple = rank_template
                for j, _rank_data in enumerate(rank_data_tuple):
                    _rank_tab = _rank_data[4].get('subpage', None)
                    if _rank_tab == rank_tab:
                        return (i, j)

            else:
                _rank_tab = rank_data[4].get('subpage', None)
                if _rank_tab == rank_tab:
                    return (i, -1)

        return (-1, -1)

    def do_show_panel(self):
        super(MainRank, self).do_show_panel()
        if self._need_show_scene:
            self._show_scene(MAIN_RANK_DEFAULT_TEXTURE)
            self._show_model()

    def on_resolution_changed(self):
        super(MainRank, self).on_resolution_changed()
        template_root = self.temp_list.get_template_root()
        template_root and template_root.SetPosition(233, '50%5')

    def on_leave_current_scene(self, *args):
        self.cur_bg_texture = None
        return

    def _show_scene(self, bg_texture):
        from logic.gcommon.common_const import scene_const
        from logic.client.const import lobby_model_display_const
        if bg_texture == self.cur_bg_texture:
            return
        self.cur_bg_texture = bg_texture
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.MAIN_RANK_SCENE, scene_content_type=scene_const.SCENE_MAIN_RANK, scene_background_texture=bg_texture)

    def _show_model(self):
        global_data.emgr.on_show_main_rank_cur_model.emit()

    def on_finalize_panel(self):
        global_data.emgr.leave_current_scene -= self.on_leave_current_scene
        global_data.emgr.on_follow_result -= self.on_follow_result
        global_data.emgr.on_undo_follow_result -= self.on_undo_follow_result
        super(MainRank, self).on_finalize_panel()
        self._panel_dict = {}
        if self.temp_list:
            self.temp_list.destroy()
            self.temp_list = None
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
        self.cur_model_controler = None
        for rank_widget in six.itervalues(self.model_controler):
            rank_widget.destroy()

        self.model_controler = {}
        for rank_widget in six.itervalues(self.cache_panel):
            rank_widget.destroy()

        self.cache_panel = {}
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        return

    def init_left_panel(self):
        self.i_second_tab_list_item = global_data.uisystem.load_template('common/i_left_second_tab_dark_list')
        self.cur_rank_panel = None
        self.left_tab_list.DeleteAllSubItem()
        m_idx, s_idx = self._get_idx_by_rank_tab(self._init_rank_tab)
        init_m_idx = 0 if m_idx == -1 else m_idx
        init_s_idx = 0 if s_idx == -1 else s_idx
        for index, rank_data in enumerate(RANK_INFOS):
            panel = self.add_left_panel(index, rank_data)
            if index == init_m_idx:

                def callback(_panel=panel):
                    if _panel and _panel.isValid() and _panel.isVisible() and global_data.player:
                        _panel.btn.OnClick(None, init_s_idx=init_s_idx)
                    self.delay_exec_id = None
                    return

                self.delay_exec_id = game3d.delay_exec(1, callback)

        return

    def add_left_panel(self, index, rank_data):
        panel = self.left_tab_list.AddTemplateItem(index)
        self._panel_dict[index] = panel
        panel.lab_main.SetString(get_text_by_id(rank_data[0]))
        panel.lab_main.setVisible(True)
        rank_temple = rank_data[1]
        panel.btn_arrow.setVisible(isinstance(rank_temple, tuple))
        panel.btn.EnableCustomState(True)

        @panel.btn.unique_callback()
        def OnClick(*args, **kw):
            old_rank_panel = self.cur_rank_panel
            if self.cur_rank_panel != panel:
                if self.cur_rank_panel:
                    self.cur_rank_panel.btn.SetSelect(False)
                    self.cur_rank_panel.StopAnimation('continue')
                    self.cur_rank_panel.RecoverAnimationNodeState('continue')
                self.cur_rank_panel = panel
                self.cur_rank_panel.btn.SetSelect(True)
                self.cur_rank_panel.PlayAnimation('click')
                self.cur_rank_panel.RecordAnimationNodeState('continue')
                self.cur_rank_panel.PlayAnimation('continue')
            if isinstance(rank_temple, tuple):
                self.on_open_sub_panel(panel, old_rank_panel, rank_temple, kw.get('init_s_idx', 0))
            else:
                self.on_close_sub_panel(old_rank_panel)
                self.on_rank_touch(rank_data)

        return panel

    def on_open_sub_panel(self, cur_panel, old_rank_panel, rank_datas, init_s_idx=0):
        is_sub_list = bool(self.left_sub_tab_list)
        self.on_close_sub_panel(old_rank_panel)
        if cur_panel != old_rank_panel or cur_panel == old_rank_panel and not is_sub_list:
            parent_index = self.left_tab_list.getIndexByItem(cur_panel)
            self.left_sub_tab_list = self.left_tab_list.AddItem(self.i_second_tab_list_item, parent_index + 1)
            self.left_sub_tab_list.DeleteAllSubItem()
            for index, rank_data in enumerate(rank_datas):
                panel = self.add_left_sub_panel(index, rank_data)
                if index == init_s_idx:
                    panel.button.OnClick()
                panel.PlayAnimation('show')

            self.left_sub_tab_list.img_bar.ResizeAndPosition()
            self.left_tab_list._container._refreshItemPos()
            self.left_tab_list._refreshItemPos()
            cur_panel.btn_arrow.setRotation(180)

    def on_close_sub_panel(self, old_rank_panel):
        if self.left_sub_tab_list:
            index = self.left_tab_list.getIndexByItem(self.left_sub_tab_list)
            self.left_tab_list.DeleteItemIndex(index)
            self.left_sub_tab_list = None
            old_rank_panel.btn_arrow.setRotation(0)
            self.cur_sub_panel = None
        return

    def add_left_sub_panel(self, index, rank_data):
        panel = self.left_sub_tab_list.AddTemplateItem(index)
        panel.button.SetText(get_text_by_id(rank_data[0]))

        @panel.button.unique_callback()
        def OnClick(*args):
            if self.cur_sub_panel != panel:
                if self.cur_sub_panel:
                    self.cur_sub_panel.button.SetSelect(False)
                self.cur_sub_panel = panel
                self.cur_sub_panel.button.SetSelect(True)
                self.cur_sub_panel.PlayAnimation('click')
                self.on_rank_touch(rank_data)

        return panel

    def on_rank_touch(self, rank_data):
        if self.temp_list:
            self.temp_list.set_visible(False)
        extra_data = rank_data[4]
        cache_rank = self.cache_panel.get(rank_data[0], None)
        if cache_rank:
            cache_rank.set_visible(True)
            self.temp_list = cache_rank
        else:
            RankWidget = rank_data[1]
            par_name = extra_data.get('par_name', 'nd_list')
            is_pve = extra_data.get('is_pve', False)
            par_node = self.panel if par_name == 'panel' else getattr(self.panel, par_name)
            if self._init_mecha_id:
                self.temp_list = RankWidget(self, par_node, self.temp_position, rank_data, init_mecha_id=self._init_mecha_id)
                self._init_mecha_id = None
            else:
                self.temp_list = RankWidget(self, par_node, self.temp_position, rank_data)
            if self.temp_list and not is_pve:
                btn_question = self.temp_list.get_question_btn()

                @btn_question.unique_callback()
                def OnClick(*args):
                    from logic.gutils.pve_rank_utils import show_role_tips
                    content, title = rank_data[3]
                    show_role_tips(title, content)

            self.cache_panel[rank_data[0]] = self.temp_list
        scene_bg = extra_data.get('scene_bg', MAIN_RANK_DEFAULT_TEXTURE)
        self._show_scene(scene_bg)
        self.active_model_ctrl(self.temp_list)
        return

    def active_model_ctrl(self, page_panel):
        if self.cur_model_controler:
            self.cur_model_controler.pause()
        self.cur_model_controler = self.model_controler[page_panel.get_page_model_ctrl_key()]
        self.cur_model_controler.resume()

    def on_click_close_btn(self, *args):
        if self.temp_list:
            self.temp_list.destroy()
            self.temp_list = None
        self.close()
        return

    def on_follow_result(self, uid):
        if self.temp_list and hasattr(self.temp_list, 'on_follow_result'):
            self.temp_list.on_follow_result(uid)

    def on_undo_follow_result(self, uid):
        if self.temp_list and hasattr(self.temp_list, 'on_undo_follow_result'):
            self.temp_list.on_undo_follow_result(uid)

    def init_scroll(self):
        if global_data.is_pc_mode:
            self.register_mouse_scroll_event()
            if global_data.feature_mgr.is_support_pc_mouse_hover():
                pass
            else:
                listener = cc.EventListenerMouse.create()
                listener.setOnMouseMoveCallback(self._on_mouse_move)
                cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.panel.get())

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        rank_list = self.temp_list.get_list_rank()
        if not rank_list:
            return
        if rank_list.GetItemCount() == 0:
            return
        mouse_scroll_utils.sview_scroll_by_mouse_wheel_dynamic(self.temp_list, rank_list, delta, uoc.SST_TASK_MAIN_MOUSE_WHEEL)
        self.temp_list.check_sview()

    def check_can_mouse_scroll(self):
        if global_data.is_pc_mode and self.HOT_KEY_NEED_SCROLL_SUPPORT and global_data.player:
            return True
        return False

    def _on_mouse_move(self, event):
        if self.temp_list is None:
            return
        else:
            slider_btn = self.temp_list.get_slider_btn()
            if slider_btn is None:
                return
            wpos = event.getLocationInView()
            from common.utils.cocos_utils import neox_pos_to_cocos
            wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
            if slider_btn.IsPointIn(wpos):
                self._on_hover_slider(slider_btn, True)
            else:
                self._on_hover_slider(slider_btn, False)
            return

    def _on_hover_slider(self, btn, enter):
        old_size = btn.GetContentSize()
        if enter:
            btn.SetContentSize(SLIDER_BTN_SIZE_BIG[0], old_size[1])
        else:
            btn.SetContentSize(SLIDER_BTN_SIZE_NORMAL[0], old_size[1])