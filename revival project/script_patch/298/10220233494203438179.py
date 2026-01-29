# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/new_template_utils.py
from __future__ import absolute_import
from functools import cmp_to_key
import logic.gcommon.item.item_const as item_const
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const

def is_mecha_related_item(item_id):
    from common.cfg import confmgr
    item_conf = confmgr.get('item', str(item_id), default={})
    return item_conf.get('iStype', None) in [item_const.MEHCA_ITEM, item_const.HUMAN_MEHCA_ITEM]


def is_human_mecha_item(item_id):
    from common.cfg import confmgr
    item_conf = confmgr.get('item', str(item_id), default={})
    return item_conf.get('iStype', None) == item_const.HUMAN_MEHCA_ITEM


class CommonLeftTabList(object):

    def __init__(self, nd, tab_info_list, ret_func, btn_func):
        self.init_tab_list(nd.nd_tab_list, tab_info_list, btn_func)
        self._cur_sel_index = None
        self._nd = nd
        self._btn_func = btn_func
        return

    def destroy(self):
        self._nd = None
        self._btn_func = None
        return

    def init_tab_list(self, nd_list, tab_info_list, btn_func):
        tab_num = len(tab_info_list)
        nd_list.tab_list.SetInitCount(tab_num)
        all_item = nd_list.tab_list.GetAllItem()
        for idx, tab_item in enumerate(all_item):
            info = tab_info_list[idx]
            self.init_one_tab(tab_item, info, btn_func, idx)

        inner_sz = nd_list.tab_list.GetInnerContentSize()
        sz = nd_list.tab_list.getContentSize()
        if inner_sz.height > sz.height:
            nd_list.tab_list.setTouchEnabled(True)
        else:
            nd_list.tab_list.setTouchEnabled(False)

    def init_one_tab(self, tab_item, info, btn_func, idx):
        text = info.get('text', '')
        frame = info.get('frame')
        frame_bar = info.get('frame_bar')
        from common.uisys.uielment.CCSprite import CCSprite
        if frame_bar:
            if tab_item.nd_img.img_frame_bar:
                tab_item.nd_img.img_frame.SetDisplayFrameByPath('', frame_bar)
            else:
                tab_item.nd_img.AddChild('img_frame_bar', CCSprite.Create('', frame_bar))
                tab_item.nd_img.img_frame_bar.setAnchorPoint(tab_item.nd_img.getAnchorPoint())
                tab_item.nd_img.img_frame_bar.SetPosition(0, '50%')
        if frame:
            if tab_item.nd_img.img_frame:
                tab_item.nd_img.img_frame.SetDisplayFrameByPath('', frame)
            else:
                tab_item.nd_img.AddChild('img_frame', CCSprite.Create('', frame))
                tab_item.nd_img.img_frame.setAnchorPoint(tab_item.nd_img.getAnchorPoint())
                tab_item.nd_img.img_frame.SetPosition(0, '50%')
        self.set_btn_text(tab_item, text)
        tab_item.btn.EnableCustomState(True)
        tab_item.btn.idx = idx

        @tab_item.btn.unique_callback()
        def OnClick(btn, touch):
            self.select_tab_btn(btn.idx)

    def set_btn_text(self, tab_item, text):
        if tab_item.lab_main:
            tab_item.lab_main.setVisible(True)
            tab_item.lab_main.SetString(text)
            tab_item.btn.SetText('')
        else:
            tab_item.lab_main.setVisible(False)
            tab_item.btn.SetText(text)

    def show_tab(self, idx, is_show):
        if idx < self._nd.nd_tab_list.tab_list.GetItemCount():
            item = self._nd.nd_tab_list.tab_list.GetItem(idx)
            item.setVisible(is_show)
            self._nd.nd_tab_list.tab_list.GetContainer()._refreshItemPos(is_cal_visible=True)

    def delete_one_tab(self, idx):
        self._nd.nd_tab_list.tab_list.DeleteItemIndex(idx)
        self._nd.nd_tab_list.tab_list._refreshItemPos()
        all_item = self._nd.nd_tab_list.tab_list.GetAllItem()
        for new_idx, tab_item in enumerate(all_item):
            tab_item.btn.idx = new_idx

    def select_tab_btn(self, index):
        if self._cur_sel_index == index:
            return
        if self._btn_func and callable(self._btn_func):
            if self._btn_func(index):
                self.set_tab_selected(index)

    def set_tab_selected(self, index):
        if self._cur_sel_index is not None:
            cur_item = self._nd.tab_list.GetItem(self._cur_sel_index)
            if cur_item:
                cur_item.StopAnimation('continue')
                cur_item.RecoverAnimationNodeState('continue')
                cur_item.btn.SetSelect(False)
                if cur_item.lab_main:
                    cur_item.lab_main.SetColor(12433625)
                if cur_item.nd_img.img_frame_bar:
                    cur_item.nd_img.img_frame_bar.setVisible(True)
        if self._cur_sel_index != index:
            item = self._nd.tab_list.GetItem(index)
            if item:
                item.PlayAnimation('click')
                item.btn.SetSelect(True)
                if item.nd_img.img_frame_bar:
                    item.nd_img.img_frame_bar.setVisible(False)
                item.RecordAnimationNodeState('continue')
                item.PlayAnimation('continue')
                if item.lab_main:
                    item.lab_main.SetColor('#SW')
            self._cur_sel_index = index
        return

    def get_select_tab_btn_idx(self):
        return self._cur_sel_index


def init_top_tab_list(nd_list, data_list, click_cb):
    nd_list.DeleteAllSubItem()
    nd_list.SetInitCount(len(data_list))
    for idx, item in enumerate(nd_list.GetAllItem()):
        info = data_list[idx]
        text = info.get('text', '')
        if text:
            item.btn_tab.SetText(text)
        item.btn_tab.EnableCustomState(True)

        @item.btn_tab.callback()
        def OnClick(btn, touch, item=item, idx=idx):
            click_cb(item, idx)
            for _idx, _item in enumerate(nd_list.GetAllItem()):
                if _idx != idx:
                    _item.btn_tab.SetSelect(False)
                    if _item.img_vx:
                        _item.StopAnimation('click')
                        _item.PlayAnimation('unclick')
                        _item.img_vx.setVisible(False)
                else:
                    _item.btn_tab.SetSelect(True)
                    if _item.img_vx:
                        _item.StopAnimation('unclick')
                        _item.img_vx.setVisible(True)
                        _item.PlayAnimation('click')


def init_activity_top_tab(nd_list, data_list, click_cb=None):
    nd_list.DeleteAllSubItem()
    nd_list.SetInitCount(len(data_list))
    for idx, item in enumerate(nd_list.GetAllItem()):
        info = data_list[idx]
        text = info.get('text', '')
        item.btn_top.SetText(text)
        item.btn_top.EnableCustomState(True)

        @item.btn_top.callback()
        def OnClick(btn, touch, item=item, idx=idx):
            ret = True
            if click_cb:
                ret = click_cb(item, idx)
            if not ret:
                return
            for _idx, _item in enumerate(nd_list.GetAllItem()):
                if _idx != idx:
                    _item.btn_top.SetSelect(False)
                else:
                    _item.btn_top.SetSelect(True)


class MultiChooseWidget(object):
    FAIL_SURPASS_MAX_SEL = 1
    FAIL_SMALL_MIN_SEL = 2

    def __init__(self):
        pass

    def destroy(self):
        self.panel = None
        self.ui_item_list = []
        self.sel_list = []
        self.sel_falled_cb = None
        self.sel_status_change_cb = None
        self.sel_ui_update_cb = None
        return

    def init(self, panel, ui_item_list, sel_list, max_sel_num=None, min_sel_num=None):
        self.panel = panel
        self.ui_item_list = ui_item_list
        self.sel_list = sel_list
        self.sel_status_change_cb = None
        self.sel_falled_cb = None
        self.sel_ui_update_cb = self._default_sel_ui_update_func
        if max_sel_num is None:
            max_sel_num = len(self.ui_item_list)
        if min_sel_num is None:
            min_sel_num = 0
        self.min_sel_num = min_sel_num
        self.max_sel_num = max_sel_num
        self._update_selections()
        self._init_items()
        return

    def _default_sel_ui_update_func(self, ui_item, vis):
        ui_item.choose.setVisible(vis)

    def SetCallbacks(self, sel_status_change_cb, sel_ui_update_cb):
        self.sel_status_change_cb = sel_status_change_cb
        if sel_ui_update_cb is None:
            self.sel_ui_update_cb = self._default_sel_ui_update_func
        else:
            self.sel_ui_update_cb = sel_ui_update_cb
        return

    def _init_items(self):
        for idx, ui_item in enumerate(self.ui_item_list):

            @ui_item.btn.callback()
            def OnClick(btn, touch, idx=idx, ui_item=ui_item):
                is_old_sel = idx in self.sel_list
                new_sel = not is_old_sel
                if new_sel and len(self.sel_list) + 1 > self.max_sel_num:
                    self.on_sel_fail(idx, self.FAIL_SURPASS_MAX_SEL)
                    return
                if is_old_sel and len(self.sel_list) - 1 < self.min_sel_num:
                    self.on_sel_fail(idx, self.FAIL_SMALL_MIN_SEL)
                    return
                if is_old_sel:
                    if idx in self.sel_list:
                        self.sel_list.remove(idx)
                elif idx not in self.sel_list:
                    self.sel_list.append(idx)
                self.sel_ui_update_cb(ui_item, not is_old_sel)
                if self.sel_status_change_cb:
                    self.sel_status_change_cb(idx, not is_old_sel)

    def on_sel_fail(self, idx, reason):
        if self.sel_falled_cb:
            self.sel_falled_cb(idx, reason)

    def _update_selections(self):
        if not self.sel_ui_update_cb:
            log_error('sel_ui_update_cb not callable')
            return
        for idx, ui_item in enumerate(self.ui_item_list):
            if idx in self.sel_list:
                self.sel_ui_update_cb(ui_item, True)
            else:
                self.sel_ui_update_cb(ui_item, False)

    def SetSelectedItems(self, sel_list):
        self.sel_list = sel_list
        self._update_selections()

    def GetSelects(self):
        return self.sel_list


class VitalityBoxReward(object):

    def __init__(self, nd, lv, btn_func):
        self.btn_func = btn_func
        self.nd = nd
        self.lv = lv

        @nd.callback()
        def OnClick(btn, touch):
            if self.btn_func:
                self.btn_func(btn, touch, lv)

    def update_score(self, score):
        self.nd.lab_score.SetString(str(score))

    def update_vitality_point(self, point):
        self.nd.lab_liveness.SetString(str(point))

    def update_reward_status(self, reward_st, show_get_img=True):
        from logic.gcommon.item import item_const
        if self.nd:
            if reward_st == item_const.ITEM_RECEIVED:
                self.nd.nd_get.setVisible(True)
                if show_get_img:
                    self.nd.img_box_get.setVisible(True)
                    self.nd.img_box.setVisible(False)
            else:
                self.nd.nd_get.setVisible(False)
                if show_get_img:
                    self.nd.img_box_get.setVisible(False)
                    self.nd.img_box.setVisible(True)
            if reward_st == item_const.ITEM_UNRECEIVED:
                self.nd.PlayAnimation('get_tips')
                self.nd.nd_get_tips.setVisible(True)
            else:
                self.nd.StopAnimation('get_tips')
                self.nd.nd_get_tips.setVisible(False)


class GlActiveBoxReward(object):

    def __init__(self, nd, click_cb, reward_id, data):
        self.nd = nd
        self.data = data
        self.stat = ITEM_UNGAIN
        self.click_cb = click_cb
        self.reward_id = reward_id
        self.init_gl_reward_item()

    def init_gl_reward_item(self):
        from common.cfg import confmgr
        from logic.gutils import item_utils
        reward_conf = confmgr.get('common_reward_data', str(self.reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        self.nd.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        if item_num > 1:
            self.nd.lab_quantity.setString(str(item_num))
            self.nd.lab_quantity.setVisible(True)

        @self.nd.callback()
        def OnClick(btn, touch):
            if self.click_cb:
                self.click_cb(btn, touch, self.data)
            if self.stat == ITEM_UNRECEIVED:
                return
            else:
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return

    def update_state(self, stat):
        self.stat = stat
        if not self.nd:
            return
        if stat == ITEM_UNGAIN:
            self.nd.StopAnimation('show_light')
            self.nd.nd_get.setVisible(False)
            self.nd.nd_get_tips.setVisible(False)
            self.nd.btn_reward.SetSelect(False)
        elif stat == ITEM_UNRECEIVED:
            self.nd.nd_get.setVisible(False)
            self.nd.nd_get_tips.setVisible(True)
            self.nd.btn_reward.SetSelect(True)
            self.nd.PlayAnimation('show_light')
        elif stat == ITEM_RECEIVED:
            self.nd.nd_get.setVisible(True)
            self.nd.nd_get_tips.setVisible(False)
            self.nd.btn_reward.SetSelect(False)
            self.nd.StopAnimation('show_light')

    def destroy(self):
        self.nd = None
        self.data = None
        self.click_cb = None
        self.reward_id = None
        return


class CommonItemReward(object):

    def __init__(self, nd, reward_id, click_cb, args, need_lock=True):
        self.nd = nd
        self.stat = ITEM_UNGAIN
        self.click_cb = click_cb
        self.reward_id = reward_id
        self.init_reward_item()
        self.args = args
        self.need_lock = need_lock

    def init_reward_item(self):
        from common.cfg import confmgr
        reward_conf = confmgr.get('common_reward_data', str(self.reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        from logic.gutils.template_utils import init_tempate_mall_i_item
        init_tempate_mall_i_item(self.nd, item_no, item_num)

        @self.nd.btn_choose.unique_callback()
        def OnClick(btn, touch):
            if self.stat == ITEM_UNRECEIVED:
                if self.click_cb:
                    self.click_cb(*self.args)
                return
            else:
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return

    def update_state(self, stat):
        self.stat = stat
        if not self.nd:
            return
        self.nd.nd_lock.setVisible(False)
        self.nd.nd_get_tips.setVisible(False)
        self.nd.nd_get.setVisible(False)
        if stat == ITEM_UNGAIN:
            self.nd.StopAnimation('get_tips')
            self.need_lock and self.nd.nd_lock.setVisible(True)
        elif stat == ITEM_UNRECEIVED:
            self.nd.PlayAnimation('get_tips')
            self.nd.nd_get_tips.setVisible(True)
        elif stat == ITEM_RECEIVED:
            self.nd.StopAnimation('get_tips')
            self.nd.nd_get.setVisible(True)
            self.nd.nd_lock.setVisible(True)

    def destroy(self):
        self.nd = None
        self.data = None
        self.click_cb = None
        self.reward_id = None
        return


class GranbelmItemReward(CommonItemReward):

    def init_reward_item(self):
        from common.cfg import confmgr
        reward_conf = confmgr.get('common_reward_data', str(self.reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        from logic.gutils.template_utils import init_tempate_mall_i_item
        init_tempate_mall_i_item(self.nd, item_no, item_num)

        @self.nd.btn_choose.unique_callback()
        def OnClick(btn, touch):
            if self.click_cb:
                position = touch.getLocation()
                self.click_cb(item_no, position, *self.args)

    def update_nd_lock_state(self, visible):
        if not self.nd:
            return
        self.nd.nd_lock.setVisible(visible)

    def update_nd_get_tips_state(self, visible):
        if not self.nd:
            return
        if visible:
            self.nd.PlayAnimation('get_tips')
        else:
            self.nd.StopAnimation('get_tips')
        self.nd.nd_get_tips.setVisible(visible)

    def update_nd_get_state(self, visible):
        if not self.nd:
            return
        if visible:
            self.nd.StopAnimation('get_tips')
        self.nd.nd_get.setVisible(visible)


class ModeSatSurveyButtonWidget(object):

    def __init__(self, button):
        self._button = button
        self.update_state()

        @self._button.callback()
        def OnClick(btn, touch):
            self.on_click_btn_comment(btn, touch)

        global_data.emgr.on_mode_sat_survey_setted_event += self.update_state

    def update_state(self):
        state = self.check_can_commit()
        self._button.SetShowEnable(state)

    def destroy(self):
        self._button = None
        global_data.emgr.on_mode_sat_survey_setted_event -= self.update_state
        return

    def get_battle_context(self):
        if not global_data.player:
            return None
        else:
            bat = global_data.player.get_battle()
            if bat:
                battle_context = {'battle_type': bat.get_battle_tid(),'battle_id': str(bat.id)}
                return battle_context
            return None

    def check_can_commit(self):
        battle_context = self.get_battle_context()
        if global_data.player:
            flag = not global_data.player.is_committed_mode_sat_survey(battle_context)
        else:
            flag = False
        return battle_context and flag

    def on_click_btn_comment(self, btn, touch):
        if not self.check_can_commit():
            global_data.game_mgr.show_tip(get_text_by_id(850020))
            return
        else:
            from logic.comsys.survey.ModeSatisfactionSurveyUI import ModeSatisfactionSurveyUI
            battle_context = self.get_battle_context()
            ui_inst = ModeSatisfactionSurveyUI(None, battle_context)
            return


class SingleChooseWidget(object):

    def __init__(self):
        self.sel_idx = None
        self.sel_status_change_cb = None
        self.sel_ui_update_cb = None
        return

    def destroy(self):
        self.panel = None
        self.ui_item_list = []
        self.sel_idx = None
        self.sel_status_change_cb = None
        self.sel_ui_update_cb = None
        return

    def init(self, panel, ui_item_list, ui_item_btn_name):
        self.panel = panel
        self.ui_item_list = ui_item_list
        self.ui_item_btn_name = ui_item_btn_name
        self._update_selections()
        self._init_items()

    def SetSelectedIndex(self, sel_idx):
        self.sel_idx = sel_idx
        self._update_selections()

    def GetSelect(self):
        return self.sel_idx

    def SetCallbacks(self, sel_status_change_cb, sel_ui_update_cb):
        self.sel_status_change_cb = sel_status_change_cb
        if sel_ui_update_cb is None:
            self.sel_ui_update_cb = self._default_ui_update_func
        else:
            self.sel_ui_update_cb = sel_ui_update_cb
        return

    def _default_ui_update_func(self, ui_item, vis):
        ui_item.choose.setVisible(vis)

    def _init_items(self):
        if self.ui_item_btn_name is None:
            return
        else:
            for idx, ui_item in enumerate(self.ui_item_list):
                if self.ui_item_btn_name:
                    btn = getattr(ui_item, self.ui_item_btn_name)
                else:
                    btn = ui_item

                @btn.callback()
                def OnClick(btn, touch, idx=idx, ui_item=ui_item):
                    if self.sel_idx == idx:
                        if self.sel_idx is not None:
                            self._update_ui_item_selection(self.sel_idx, False)
                        else:
                            self._update_ui_item_selection(idx, True)
                    else:
                        if self.sel_idx is not None:
                            self._update_ui_item_selection(self.sel_idx, False)
                        if idx is not None:
                            self._update_ui_item_selection(idx, True)
                    return

            return

    def _update_ui_item_selection(self, idx, is_sel):
        if idx < len(self.ui_item_list):
            ui_item = self.ui_item_list[idx]
            self.sel_ui_update_cb(ui_item, is_sel)
            if is_sel:
                self.sel_idx = idx
            elif self.sel_idx == idx:
                self.sel_idx = None
        return

    def set_ui_item_select_status_by_idx(self, idx, is_sel):
        if self.sel_idx == idx:
            if self.sel_idx is not None:
                self._update_ui_item_selection(self.sel_idx, is_sel)
        else:
            if self.sel_idx is not None:
                self._update_ui_item_selection(self.sel_idx, False)
            if idx is not None:
                self._update_ui_item_selection(idx, is_sel)
        return

    def set_ui_item_select_status_by_ui_item(self, ui_item, is_sel):
        if ui_item in self.ui_item_list:
            idx = self.ui_item_list.index(ui_item)
            self.set_ui_item_select_status_by_idx(idx, is_sel)

    def _update_selections(self):
        for idx, ui_item in enumerate(self.ui_item_list):
            if idx == self.sel_idx:
                self.sel_ui_update_cb(ui_item, True)
            else:
                self.sel_ui_update_cb(ui_item, False)


class DiscardWidget(object):

    def __init__(self, panel, nd_drag_item, nd_discard):
        self.panel = panel
        self.nd_drag_item = nd_drag_item
        self.nd_discard = nd_discard
        from common.utils.ui_utils import get_scale
        self._init_dist = get_scale('30w')
        self._enable = True

    def set_enable(self, enable):
        self._enable = enable

    def destroy(self):
        self.panel = None
        self.nd_drag_item = None
        self.nd_discard = None
        return

    def show_drag_item(self, item_id):
        import cc
        from logic.gutils import item_utils
        self.nd_drag_item.setVisible(True)
        item_icon = self.nd_drag_item.drag_item_icon
        item_icon.SetDisplayFrameByPath('', item_utils.get_item_pic_by_item_no(item_id))
        item_icon.SetPosition(30, 30)
        item_icon.stopAllActions()
        target_pos = cc.Vec2(30, 60)
        item_icon.runAction(cc.MoveTo.create(0.2, target_pos))

    def check_discard(self, wpos, item_no, item_count, non_discard_list):
        from logic.gcommon import const
        from logic.gutils import item_utils
        from logic.gcommon.cdata.status_config import ST_SWIM, ST_PARACHUTE
        if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_CONCERT:
            return
        NOT_THROW_ITEM_STATE = [
         ST_SWIM, ST_PARACHUTE]

        def callback(num):
            if not (global_data.player and global_data.player.logic):
                return
            else:
                lplayer = global_data.player.logic
                if not lplayer.ev_g_can_throw_item():
                    return
                item_list = lplayer.ev_g_itme_list_by_id(item_no)
                if item_list:
                    item_data = item_list[0]
                    item_utils.throw_item(lplayer, const.BACKPACK_PART_OTHERS, item_data['entity_id'], num, None)
                return

        if self.check_is_discard(wpos, non_discard_list):
            self.discard_item(callback, item_count)

    def discard_item(self, callback, max_count):
        from logic.gcommon.cdata.status_config import ST_SWIM, ST_PARACHUTE
        if max_count <= 1:
            callback(max_count)
            return
        if not (global_data.player and global_data.player.logic):
            return
        if not global_data.player.logic.ev_g_can_throw_item():
            return
        from logic.gutils.template_utils import init_common_discard
        init_common_discard(self.nd_discard, max_count, callback)

    def check_is_discard(self, wpos, non_discard_list):
        for nd in non_discard_list:
            if nd.IsPointIn(wpos):
                return False

        return True

    def init_btn(self, btn, is_scrollable=True):
        if not self._enable:
            return
        if is_scrollable:
            btn.SetSwallowTouch(False)
            btn.SetNoEventAfterMove(False, '5w')

    def OnDrag(self, btn, touch, item_no, non_discard_list, is_scrollable=True):
        if not self._enable:
            return
        DRAG_DELTA = 3
        DRAG_TAN = 1
        if not item_no:
            return
        if not self.nd_drag_item.isVisible() and (is_scrollable and not btn.GetSwallowTouch() or not is_scrollable):
            pos = touch.getLocation()
            beg_pos = touch.getStartLocation()
            dx = pos.x - beg_pos.x
            dy = pos.y - beg_pos.y
            if btn.GetMovedDistance() > self._init_dist:
                return
            if abs(dx) + abs(dy) < DRAG_DELTA:
                return
            if abs(dx) * DRAG_TAN >= abs(dy):
                if is_scrollable:
                    btn.SetSwallowTouch(True)
                self.show_drag_item(item_no)
            else:
                return
        wpos = touch.getLocation()
        if is_scrollable:
            if not btn.GetSwallowTouch() and not self.check_is_discard(wpos, non_discard_list):
                btn.SetSwallowTouch(True)
        if self.nd_drag_item.isVisible():
            lpos = self.nd_drag_item.getParent().convertToNodeSpace(wpos)
            self.nd_drag_item.setPosition(lpos)

    def OnEnd(self, btn, touch, item_no, item_count, non_discard_list, is_scrollable=True):
        if not self._enable:
            return
        if self.nd_drag_item.isVisible():
            self.nd_drag_item.setVisible(False)
            if is_scrollable:
                btn.SetSwallowTouch(False)
            if item_no:
                self.check_discard(touch.getLocation(), item_no, item_count, non_discard_list)


def update_newbee_pass_certificate(nd_card, task_id, task_img):
    nd_card.setVisible(True)
    from common.cfg import confmgr
    import logic.gcommon.time_utility as t_util
    task_data = confmgr.get('task/task_data', task_id)
    nd_card.lab_title_mode.SetString(task_data['name'])
    nd_card.lab_describe.SetString(task_data['desc'])
    nd_card.img_card.SetDisplayFrameByPath('', task_img)
    number = global_data.player.get_task_content(task_id, 'number', '00000000000000')
    nd_card.lab_no.SetString(number)
    timestamp = global_data.player.get_task_content(task_id, 'finish_time', 0)
    date_time = t_util.get_date_str('%Y.%m.%d', timestamp)
    nd_card.lab_date.SetString(date_time)
    is_receive = bool(global_data.player.has_receive_reward(task_id))
    set_certificate_reward_data(nd_card.temp_reward, task_id, is_receive)


def set_certificate_reward_data(nd, task_id, isget):
    from common.cfg import confmgr
    from logic.gutils import task_utils
    from logic.gutils import template_utils
    reward_id = task_utils.get_task_reward(task_id)
    reward_conf = confmgr.get('common_reward_data', str(reward_id))
    reward_list = reward_conf.get('reward_list', [])
    reward_info = reward_list[0]
    template_utils.init_tempate_mall_i_item(nd, reward_info[0], reward_info[1], isget)


def get_show_uid(uid):
    show_id = int(uid)
    show_id -= global_data.uid_prefix
    return str(show_id)


def set_mecha_combat_capacity(list_node, mecha_id):
    from common.cfg import confmgr
    spec_list = confmgr.get('mecha_display', 'HangarConfig', 'Content', str(mecha_id), 'desc_speciality', default=[])
    list_tab = list_node
    if spec_list:
        mecha_desc_conf = confmgr.get('mecha_display', 'HangarDescConf', 'Content')
        list_tab.setVisible(True)
        list_tab.DeleteAllSubItem()
        for spec in spec_list:
            panel = list_tab.AddTemplateItem()
            from logic.gutils.mecha_utils import MECHA_TYPE_SMALL_ICON
            tag_icon_path = MECHA_TYPE_SMALL_ICON[spec]
            panel.img_tab.SetDisplayFrameByPath('', tag_icon_path)
            spec_param = mecha_desc_conf.get(spec, {})
            panel.lab_text.SetString(get_text_by_id(spec_param.get('tag_name_text_id')))
            panel.setVisible(True)

    else:
        list_tab.setVisible(False)


class TaskListWidget(object):

    def __init__(self, nd_task_list, task_ids, check_open_func=None):
        from logic.gutils import task_utils
        self._list_task = nd_task_list.list_task
        self._task_ids = task_ids
        self._task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        self._task_dict = {}
        self._check_open_func = check_open_func
        self.init_tasks()
        self.process_event(True)

    def init_tasks(self):
        self._list_task.DeleteAllSubItem()
        self._list_task.SetInitCount(len(self._task_ids))
        for i, task_id in enumerate(self._task_ids):
            self._init_task_item(self._list_task.GetItem(i), task_id)

    def setVisible(self, visible):
        self._list_task.setVisible(visible)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_task
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_task_item(self, nd_task_item, task_id):
        from logic.gutils import task_utils
        from logic.gutils.template_utils import init_common_reward_list_simple
        from logic.gutils.item_utils import exec_jump_to_ui_info
        task_conf = task_utils.get_task_conf_by_id(task_id)
        nd_task_item.lab_name.SetString(task_utils.get_task_name(task_id))
        self._task_dict[task_id] = nd_task_item
        nd_task_item.task_id = task_id
        self.refresh_task_progress(task_id)
        reward_id = task_conf.get('reward', None)
        init_common_reward_list_simple(nd_task_item.list_reward, reward_id)
        self.refresh_task_reward_st(task_id)

        @nd_task_item.temp_btn_get.btn_common.unique_callback()
        def OnClick(btn, touch, task_id=task_id):
            if not global_data.player:
                return
            status = global_data.player.get_task_reward_status(nd_task_item.task_id)
            if status == item_const.ITEM_UNGAIN:
                jump_conf = task_utils.get_jump_conf(task_id)
                exec_jump_to_ui_info(jump_conf)
            elif status == item_const.ITEM_UNRECEIVED:
                global_data.player.receive_task_reward(task_id)

        nd_task_item.pnl_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_common/pnl_activity_common_light_color2.png')
        return

    def refresh_task_progress(self, task_id):
        if task_id not in self._task_dict:
            return
        task_item = self._task_dict[task_id]
        player = global_data.player
        if not player:
            return
        from logic.gutils import task_utils
        prog = player.get_task_prog(task_id)
        total_prog = task_utils.get_total_prog(task_id)
        task_item.lab_num.SetString('%s/%s' % (prog, total_prog))

    def refresh_task_reward_st(self, task_id):
        if task_id not in self._task_dict:
            return
        else:
            player = global_data.player
            if not player:
                return
            nd_task_item = self._task_dict[task_id]
            nd_task_item.nd_get.setVisible(False)
            nd_task_item.lab_progress.setVisible(False)
            from logic.gutils import task_utils
            btn = nd_task_item.temp_btn_get.btn_common
            if self._check_open_func and not self._check_open_func(task_id):
                btn.setVisible(True)
                btn.SetTextColor('#SK', '#SK', '#SK')
                btn.SetEnable(False)
                btn.SetText(870022)
                return
            PIC0 = 'gui/ui_res_2/common/button/btn_secondary_middle.png'
            PIC1 = 'gui/ui_res_2/common/button/btn_secondary_major.png'
            PIC2 = 'gui/ui_res_2/common/button/btn_secondary_useless.png'
            status = global_data.player.get_task_reward_status(nd_task_item.task_id)
            if status == item_const.ITEM_UNGAIN:
                jump_conf = task_utils.get_jump_conf(task_id)
                if jump_conf:
                    btn.setVisible(True)
                    btn.SetText(80284)
                    btn.SetTextColor('#SK', '#SK', '#SK')
                    btn.SetFrames('', [PIC0, PIC0, PIC2], False, None)
                    btn.SetEnable(True)
                else:
                    btn.setVisible(False)
                    nd_task_item.lab_progress.setVisible(True)
            elif status == item_const.ITEM_UNRECEIVED:
                btn.setVisible(True)
                btn.SetTextColor('#SK', '#SK', '#SK')
                btn.SetFrames('', [PIC1, PIC1, PIC2], False, None)
                btn.SetEnable(True)
                btn.SetText(604030)
            elif status == item_const.ITEM_RECEIVED:
                nd_task_item.nd_get.setVisible(True)
                btn.setVisible(False)
            return

    def _on_update_task(self, task_id):
        if task_id not in self._task_dict:
            return
        self.refresh_task_progress(task_id)
        self.refresh_task_reward_st(task_id)
        self._dynamic_ajust_task_list(self._list_task, self._task_ids, task_id)

    def _dynamic_ajust_task_list(self, list_task, task_ids, task_id):
        from logic.gutils import task_utils
        old_idx = task_ids.index(task_id)
        if list_task.GetItem(0).task_id not in task_ids:
            return
        start_idx = task_ids.index(list_task.GetItem(0).task_id)
        task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        list_num = list_task.GetItemCount()
        new_idx = task_ids.index(task_id)
        if old_idx == new_idx:
            return
        if start_idx <= old_idx < start_idx + list_num:
            del_item = list_task.GetItem(old_idx - start_idx)
            self._task_dict.pop(del_item.task_id)
            list_task.DeleteItemIndex(old_idx - start_idx)
            new_start_idx = task_ids.index(list_task.GetItem(0).task_id)
            if new_idx < new_start_idx:
                nd_task_item = list_task.AddTemplateItem(0)
                self._init_task_item(nd_task_item, task_ids[new_start_idx - 1])
            elif new_idx < new_start_idx + list_num:
                nd_task_item = list_task.AddTemplateItem(new_idx - new_start_idx)
                self._init_task_item(nd_task_item, task_id)
            else:
                nd_task_item = list_task.AddTemplateItem(list_num - 1)
                self._init_task_item(nd_task_item, task_ids[new_start_idx + list_num - 1])
        elif start_idx <= new_idx < start_idx + list_num:
            del_item = list_task.GetItem(list_num - 1)
            self._task_dict.pop(del_item.task_id)
            list_task.DeleteItemIndex(list_num - 1)
            nd_task_item = list_task.AddTemplateItem(new_idx - start_idx)
            self._init_task_item(nd_task_item, task_id)

    def destroy(self):
        self.process_event(False)
        self._list_task = None
        self._task_ids = None
        self._task_dict = {}
        return


class GoldTaskListWidget(TaskListWidget):

    def __init__(self, nd_task_list, task_ids, check_open_func=None):
        self.sview_content_height = 0
        self.sview_index = 0
        self.is_check_sview = False
        super(GoldTaskListWidget, self).__init__(nd_task_list, task_ids, check_open_func)

    def init_tasks(self):
        self._list_task.DeleteAllSubItem()
        sview_height = self._list_task.getContentSize().height
        vert_indent = self._list_task.GetVertIndent()
        index = 0
        task_num = len(self._task_ids)
        while self.sview_content_height <= sview_height and index < task_num:
            task_id = self._task_ids[index]
            nd_task_item = self.add_task_data(task_id, True)
            item_height = nd_task_item.getContentSize().height
            self.sview_content_height += item_height + vert_indent
            index += 1

        self.sview_index = index - 1
        self._list_task.addEventListener(self.scroll_callback)

    def _on_update_task(self, task_id):
        if task_id not in self._task_dict:
            return
        self.refresh_task_progress(task_id)
        self.refresh_task_reward_st(task_id)
        self._dynamic_ajust_task_list(self._list_task, self._task_ids, task_id)
        self.sview_index = self._task_ids.index(self._list_task.GetItem(-1).task_id)

    def scroll_callback(self, *args):
        if not self.is_check_sview:
            self.is_check_sview = True
            if self._list_task:
                self._list_task.SetTimeOut(0.021, self.check_sview)

    def destroy(self):
        self._list_task.stopAllActions()
        super(GoldTaskListWidget, self).destroy()

    def check_sview(self):
        task_num = len(self._task_ids)
        self.sview_index = self._list_task.AutoAddAndRemoveItem_MulCol(self.sview_index, self._task_ids, task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_check_sview = False

    def on_del_task_item(self, task_item, index):
        if task_item.task_id in self._task_dict:
            self._task_dict.pop(task_item.task_id)

    def add_task_data(self, task_id, is_back_item=True, index=-1):
        view_list = self._list_task
        if is_back_item:
            nd_task_item = view_list.AddTemplateItem(bRefresh=True)
        else:
            nd_task_item = view_list.AddTemplateItem(0, bRefresh=True)
        if not nd_task_item:
            return None
        else:
            self._init_task_item(nd_task_item, task_id)
            return nd_task_item

    def refresh_task_reward_st(self, task_id):
        if task_id not in self._task_dict:
            return
        else:
            player = global_data.player
            if not player:
                return
            nd_task_item = self._task_dict[task_id]
            nd_task_item.nd_get.setVisible(False)
            nd_task_item.lab_progress.setVisible(False)
            from logic.gutils import task_utils
            btn = nd_task_item.temp_btn_get.btn_common
            PIC0 = 'gui/ui_res_2/common/button/btn_secondary_middle.png'
            PIC1 = 'gui/ui_res_2/common/button/btn_secondary_major.png'
            PIC2 = 'gui/ui_res_2/common/button/btn_secondary_useless.png'
            status = global_data.player.get_task_reward_status(nd_task_item.task_id)
            if status == item_const.ITEM_UNGAIN:
                jump_conf = task_utils.get_jump_conf(task_id)
                if jump_conf:
                    btn.SetText(80284)
                    btn.SetFrames('', [PIC0, PIC0, PIC2], False, None)
                    btn.SetEnable(True)
                else:
                    btn.SetText(604031)
                    btn.SetEnable(False)
            elif status == item_const.ITEM_UNRECEIVED:
                btn.SetFrames('', [PIC1, PIC1, PIC2], False, None)
                btn.SetText(604030)
                btn.SetEnable(True)
            elif status == item_const.ITEM_RECEIVED:
                btn.SetText(604029)
                btn.SetEnable(False)
            return


def update_task_list_btn(nd_btn, status, extra_args=None):
    status_dict = {1: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_major.png','text_color': 7616256,'btn_text': 604030},2: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_major.png','text_color': 7616256,'btn_text': 80149},3: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_major.png','text_color': 7616256,'btn_text': 607056},4: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','text_color': 14674164,'btn_text': 604031,'enable': False},5: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','show_nd_get': True,'enable': False},6: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','show_nd_exchange': True,'enable': False},7: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','show_nd_unlock': True,'enable': False},8: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_middle.png','text_color': 2369169,'btn_text': 19850},9: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','text_color': 14674164,'btn_text': 607056,'enable': False},10: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','text_color': 14674164,'btn_text': 610813,'enable': False}}
    if status not in status_dict:
        return
    else:
        if not extra_args:
            extra_args = {}
        text_color = status_dict[status].get('text_color')
        extra_btn_text = extra_args.get('btn_text', '')
        btn_text = extra_btn_text if extra_btn_text else status_dict[status].get('btn_text', '')
        nd_btn.btn_common.SetText(btn_text)
        text_color and nd_btn.btn_common.SetTextColor(text_color, text_color, text_color)
        btn_frame = status_dict[status]['btn_frame']
        nd_btn.btn_common.SetFrames('', [btn_frame, btn_frame, btn_frame], False, None)
        extra_enable = extra_args.get('enable')
        if extra_enable is not None:
            nd_btn.btn_common.SetEnable(extra_enable)
        else:
            nd_btn.btn_common.SetEnable(status_dict[status].get('enable', True))
        show_nd_get = status_dict[status].get('show_nd_get')
        if show_nd_get:
            nd_btn.btn_common.SetText('')
            nd_btn.nd_get.setVisible(True)
        else:
            nd_btn.nd_get.setVisible(False)
        show_nd_exchange = status_dict[status].get('show_nd_exchange')
        if show_nd_exchange:
            nd_btn.btn_common.SetText('')
            nd_btn.nd_exchange.setVisible(True)
        else:
            nd_btn.nd_exchange.setVisible(False)
        show_nd_unlock = status_dict[status].get('show_nd_unlock')
        if show_nd_unlock:
            nd_btn.btn_common.SetText('')
            nd_btn.nd_unlock.setVisible(True)
        else:
            nd_btn.nd_unlock.setVisible(False)
        return


class SkinCategoryWidget(object):

    def __init__(self):
        self._skin_categories = []

    def destroy(self):
        self._skin_categories = []

    def set_skin_categories(self, skin_categories):
        self._skin_categories = skin_categories

    def get_skin_categories(self):
        return self._skin_categories

    def get_skin_category_index(self, item_no):
        from logic.gutils.item_utils import get_lobby_item_type
        from logic.gutils.items_book_utils import transform_mecha_skin_id_to_show_one
        from logic.gutils import dress_utils
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN
        for outer_idx, skins_info in enumerate(self._skin_categories):
            title, skins = skins_info
            if item_no in skins:
                return (outer_idx, skins.index(item_no))
            if skins:
                one_skin = skins[0]
                item_type = get_lobby_item_type(one_skin)
                if item_type == L_ITEM_TYPE_MECHA_SKIN:
                    main_item_no = transform_mecha_skin_id_to_show_one(item_no, {})
                    for idx, skin in enumerate(skins):
                        main_skin = transform_mecha_skin_id_to_show_one(skin, {})
                        if main_skin == main_item_no:
                            return (outer_idx, idx)

                elif item_type == L_ITEM_TYPE_ROLE_SKIN:
                    main_item_no = dress_utils.get_top_skin_id_by_skin_id(item_no)
                    for idx, skin in enumerate(skins):
                        main_skin = dress_utils.get_top_skin_id_by_skin_id(skin)
                        if main_skin == main_item_no:
                            return (outer_idx, idx)

        return (0, 0)

    def get_show_skin_category(self, item_no):
        out_idx, in_idx = self.get_skin_category_index(item_no)
        return self._skin_categories[out_idx]


def init_player_loading_card(panel, player_eid, player_info, ui_item, my_player_eid, on_click_player_card_func, default_show_role, no_anim=False):
    from logic.gcommon.const import PRIV_SHOW_BADGE
    from logic.gutils.item_utils import get_lobby_item_name, get_skin_rare_path_by_rare, get_item_rare_degree, get_lobby_item_belong_no
    from logic.gutils.role_head_utils import init_role_head, set_role_dan, init_privilege_badge, get_head_photo_res_path
    from logic.gcommon.common_const import rank_const
    from random import randint
    from logic.gutils import role_skin_utils, mecha_skin_utils
    from common.cfg import confmgr
    from logic.gutils.template_utils import init_rank_title, set_ui_show_picture
    from logic.gutils.intimacy_utils import get_intimacy_icon_by_type
    from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
    from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME, RARE_DEGREE_1
    CHARM_RANK_LV_ICON = ('gui/ui_res_2/battle_before/hot_ranking/img_star_rank_1.png',
                          'gui/ui_res_2/battle_before/hot_ranking/img_star_rank_2.png',
                          'gui/ui_res_2/battle_before/hot_ranking/img_star_rank_3.png')
    head_photo = player_info.get('head_photo')
    head_frame = player_info.get('head_frame')
    init_role_head(ui_item.temp_head, head_frame, head_photo)
    dan_info = player_info.get('dan_info')
    set_role_dan(ui_item.temp_tier, dan_info)
    char_name = player_info.get('char_name')
    ui_item.lab_name.SetString(char_name)
    ui_item.bar_name.setVisible(player_eid == my_player_eid)
    priv_lv = player_info.get('priv_lv') or 0
    priv_settings = player_info.get('priv_settings', {}) or {}
    show_badge = priv_settings.get(PRIV_SHOW_BADGE, False)
    if priv_lv > 0 and show_badge:
        init_privilege_badge(ui_item.temp_badge, priv_lv, show_badge)
        ui_item.temp_badge.setVisible(True)
    else:
        ui_item.temp_badge.setVisible(False)
    rank_use_title_dict = player_info.get('rank_use_title_dict') or {}
    rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
    rank_title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
    init_rank_title(ui_item.temp_title, rank_title_type, rank_info, icon_scale=0.5)

    def hide_title():
        if not panel or not panel.isValid():
            return
        if not ui_item or not ui_item.isValid():
            return
        if not ui_item.temp_title and not ui_item.temp_title.isValid():
            return
        ui_item.PlayAnimation('hide_title')

    if rank_info and rank_title_type:
        ui_item.temp_title.SetTimeOut(10, hide_title)
    role_skin = player_info.get('role_skin')
    mecha_skin = player_info.get('mecha_skin')
    ui_item.img_role.SetDisplayFrameByPath('', 'gui/ui_res_2/item/driver_skin/{}.png'.format(role_skin))
    ui_item.img_mecha.SetDisplayFrameByPath('', 'gui/ui_res_2/item/mecha_skin/{}.png'.format(mecha_skin))
    role_id = get_lobby_item_belong_no(role_skin)
    lobby_mecha_id = get_lobby_item_belong_no(mecha_skin)
    if role_id and role_skin_utils.is_default_role_skin(role_skin, role_id):
        role_skin_name = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id), 'role_name')
        role_skin_name = get_text_by_id(role_skin_name)
    else:
        role_skin_name = get_lobby_item_name(role_skin)
    ui_item.lab_role_skin_name.SetString(role_skin_name)
    if lobby_mecha_id and mecha_skin_utils.is_default_mecha_skin(mecha_skin, lobby_mecha_id):
        battle_mecha_id = mecha_lobby_id_2_battle_id(lobby_mecha_id)
        if battle_mecha_id == lobby_mecha_id:
            mecha_skin_name = ''
        else:
            mecha_skin_name = confmgr.get('mecha_display', 'HangarConfig', 'Content', str(battle_mecha_id), 'name_mecha_text_id', default='')
    else:
        mecha_skin_name = get_lobby_item_name(mecha_skin)
    ui_item.lab_mecha_skin_name.SetString(mecha_skin_name)
    role_skin_weapon_sfx = player_info.get('role_skin_weapon_sfx', 0)
    mecha_skin_weapon_sfx = player_info.get('mecha_skin_weapon_sfx', 0)
    role_skin_rare_degree = get_item_rare_degree(role_skin, weapon_sfx_item=role_skin_weapon_sfx)
    mecha_skin_rare_degree = get_item_rare_degree(mecha_skin, weapon_sfx_item=mecha_skin_weapon_sfx)
    if role_skin_rare_degree <= RARE_DEGREE_1:
        ui_item.temp_level_role.setVisible(False)
    else:
        role_skin_lv_icon = get_skin_rare_path_by_rare(role_skin_rare_degree)
        ui_item.temp_level_role.setVisible(True)
        ui_item.temp_level_role.bar_level.SetDisplayFrameByPath('', role_skin_lv_icon)
    if mecha_skin_rare_degree <= RARE_DEGREE_1:
        ui_item.temp_level_mecha.setVisible(False)
    else:
        mecha_skin_lv_icon = get_skin_rare_path_by_rare(mecha_skin_rare_degree)
        ui_item.temp_level_mecha.setVisible(True)
        ui_item.temp_level_mecha.bar_level.SetDisplayFrameByPath('', mecha_skin_lv_icon)
    battle_frame = player_info.get('battle_flag_frame') or DEFAULT_FLAG_FRAME()
    ui_item.img_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/battle_loading/bar/{}.png'.format(battle_frame))
    ui_item.img_front.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/battle_loading/bar/front_{}.png'.format(battle_frame))
    ui_item.frame_basic.setVisible(battle_frame == DEFAULT_FLAG_FRAME())
    role_charm_rank = player_info.get('role_charm_rank', -1)
    mecha_charm_rank = player_info.get('mecha_charm_rank', -1)
    if 0 <= role_charm_rank < len(CHARM_RANK_LV_ICON):
        ui_item.img_role_charm_level.SetDisplayFrameByPath('', CHARM_RANK_LV_ICON[role_charm_rank])
    else:
        ui_item.nd_charm_role.setVisible(False)
    if 0 <= mecha_charm_rank < len(CHARM_RANK_LV_ICON):
        ui_item.img_mecha_charm_level.SetDisplayFrameByPath('', CHARM_RANK_LV_ICON[mecha_charm_rank])
    else:
        ui_item.nd_charm_mecha.setVisible(False)
    intimacy_type = player_info.get('intimacy_type')
    intimacy_lv = player_info.get('intimacy_lv')
    if intimacy_lv and intimacy_type:
        ui_item.icon_relation.SetDisplayFrameByPath('', get_intimacy_icon_by_type(intimacy_type))
        ui_item.lab_value.SetString(str(intimacy_lv))
        ui_item.nd_relation.setVisible(True)
    else:
        ui_item.nd_relation.setVisible(False)

    @ui_item.unique_callback()
    def OnClick(*args):
        role_visible = not ui_item.nd_role_locate.isVisible()
        mecha_visible = not role_visible
        on_click_player_card_func(ui_item, role_visible, mecha_visible)

    on_click_player_card_func(ui_item, default_show_role, not default_show_role)
    if not no_anim:
        if player_eid == my_player_eid:
            ui_item.PlayAnimation('show_me')
        else:
            ui_item.PlayAnimation('show_team')