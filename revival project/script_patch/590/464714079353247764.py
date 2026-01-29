# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineDecalWidget.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.BaseUIWidget import BaseUIWidget
import cc
import math3d
from common.cfg import confmgr
import copy
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.FullScreenBackUI import FullScreenBackUI
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from logic.gutils import item_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.gutils.skin_define_utils import get_main_skin_id, get_decal_path_by_item_id, get_default_skin_define_anim, get_decal_text_by_item_id
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_utils.decal_utils import MAX_DECAL_NUM
import time
from logic.comsys.mecha_display.SkinDefineShareUI import SkinDefineShareUI
from logic.comsys.mecha_display.SkinDefineBuyDecalBoxUI import SkinDefineBuyDecalBoxUI
FORBID_MECHA = ()
FORBID_SKINS_PROMARE = (201801151, 201802151)

class SkinDefineDecalWidget(BaseUIWidget):
    ACCESS_BUY = 1
    ACCESS_LOTTERY = 2
    ACCESS_OTHER = 3
    DELAY_TAG = 20200601
    selected_item_idx = -1
    TAB_PREVIEW_TEXT = 81605
    TAB_EQUIPED_TEXT = 81604
    selected_tab_idx = -1
    MAX_ANGLE = 28
    MIN_ANGLE = -28
    MAX_ROT = 180.0
    MIN_ROT = -180.0
    TIPS_SCALE = 1.8
    UNSELECT_LAB_COLOR = '#DC'
    SELECT_LAB_COLOR = '#SW'
    selected_decal_idx = -1
    MINI_DIS = 1
    MINI_MAX_SPEED = 25

    def __init__(self, parent, panel):
        self.global_events = {'set_preview_ui_by_param': self.reset_decal_ui_param,
           'player_item_update_event': self._on_buy_goods_success,
           'upload_decal_data': self.on_upload_decal_data,
           'del_mecha_decal_result_event': self.on_del_mecha_decal,
           'add_mecha_decal_result_event': self.on_add_mecha_decal,
           'skin_define_batch_buy_event': self.on_batch_buy_update
           }
        super(SkinDefineDecalWidget, self).__init__(parent, panel)
        self.is_guided = global_data.achi_mgr.get_cur_user_archive_data('skin_define_decal')
        self.is_list_guided = global_data.achi_mgr.get_cur_user_archive_data('skin_define_decal_list')
        self.init_params()
        self.init_conf()
        self.update_conf()
        self.parent.decal_widget = self
        self.init_tab()
        self.init_ui_events()
        self.check_forbid()

    def init_params(self):
        self.first_enter_tag = True
        self._scan_item_idx = 0
        self._create_item_idx = 0
        self._async_action = None
        self.offset_pos = cc.Vec2(0, 0)
        self.default_pos = self.panel.convertToWorldSpace(self.panel.nd_applique.getPosition())
        self.show_equiped_tag = False
        self.show_applique_tag = False
        self.can_move_tag = False
        self.ori_decal_data = []
        self.cur_decal_data = []
        self.pre_decal_data = []
        self.update_decal_data = []
        self.slider_value_rot = None
        self.slider_value_scl = None
        self.decal_idx_item_id_dict = {}
        self.new_decal_tag = True
        nd = self.panel.nd_range
        pos = nd.getPosition()
        csize = nd.getContentSize()
        self.MAX_POS_X = pos.x + csize.width * 0.5
        self.MAX_POS_Y = pos.y + csize.height * 0.5
        self.MIN_POS_X = pos.x - csize.width * 0.5
        self.MIN_POS_Y = pos.y - csize.height * 0.5
        self.forbid_tag = False
        self.forbid_text = None
        return

    def check_forbid(self):
        if self.parent.mecha_id in FORBID_MECHA:
            self.forbid_tag = True
            self.forbid_text = 634011
        elif self.parent.model_id in FORBID_SKINS_PROMARE:
            self.forbid_tag = True
            self.forbid_text = 611460
        else:
            self.forbid_text = 860152
        self.panel.img_empty.setVisible(self.forbid_tag)
        self.panel.lab_empty.SetString(self.forbid_text)

    def init_conf(self):
        self.decal_conf = confmgr.get('skin_define_decal')._conf

    def update_conf(self):
        mecha_decal_data = global_data.player.get_mecha_decal()
        self.ori_decal_data = copy.deepcopy(mecha_decal_data.get(str(get_main_skin_id(self.parent.model_id)), []))
        self.cur_decal_data = copy.deepcopy(self.ori_decal_data)

    def init_tab(self):
        self.panel.tab_small.SetInitCount(2)
        self.btn_tab_preview = self.panel.tab_small.GetItem(0).btn
        self.btn_tab_equiped = self.panel.tab_small.GetItem(1).btn
        self.btn_tab_preview.SetText(get_text_by_id(self.TAB_PREVIEW_TEXT))
        self.btn_tab_equiped.SetText(get_text_by_id(self.TAB_EQUIPED_TEXT))

        @self.btn_tab_preview.unique_callback()
        def OnClick(_btn, _touch, _idx=0, *args):
            self._on_click_tab(_idx)

        @self.btn_tab_equiped.unique_callback()
        def OnClick(_btn, _touch, _idx=1, *args):
            self._on_click_tab(_idx)

        self.btn_tab_preview.OnClick(TouchMock())

    def _on_click_tab(self, idx):
        if idx == self.selected_tab_idx:
            return
        if self.show_applique_tag:
            self.panel.btn_cancel.OnClick(TouchMock())
        self._switch_tab(idx)
        self.update_decal_list()

    def _switch_tab(self, idx):
        if idx != self.selected_tab_idx:
            if self.selected_tab_idx != -1:
                ui_item = self.panel.tab_small.GetItem(self.selected_tab_idx)
                ui_item.btn.SetSelect(False)
            self.selected_tab_idx = idx
            if idx != -1:
                ui_item = self.panel.tab_small.GetItem(idx)
                ui_item.btn.SetSelect(True)

    def show(self):
        pass

    def hide(self):
        pass

    def do_show_widget(self):
        self.check_need_guide()

    def update_widget(self, is_show):
        if is_show:
            self.update_item_list()
            self.update_decal_scene()
            self.update_decal_count()
            self.update_decal_price_btn()
            self.check_need_guide()
        else:
            if self.show_applique_tag:
                self.panel.btn_cancel.OnClick(TouchMock())
            self.selected_item_idx = -1
            self.selected_decal_idx = -1
            self.exit_decal_scene()

    def check_need_guide(self):
        if not self.is_guided:
            if self.selected_item_idx == -1:

                def delay_call_decal():
                    ui_item = self.panel.list_applique.GetItem(0)
                    if not ui_item:
                        return
                    ui_item.temp_item_dark.btn_choose.OnClick(TouchMock())
                    global_data.ui_mgr.show_ui('SkinDefineGuideDecalUI', 'logic.comsys.mecha_display')
                    self.is_guided = True

                self.panel.DelayCallWithTag(0.06, delay_call_decal, 20200922)

    def check_need_list_guide(self):
        if not self.is_list_guided:
            if not self.panel.nd_equiped.list_equiped_applique.GetAllItem():
                return
            if self.selected_decal_idx == -1:

                def delay_call_decal():
                    self.panel.list_equiped_applique.GetItem(0).btn.OnClick(TouchMock())

                self.panel.DelayCallWithTag(0.06, delay_call_decal, 20200930)
            global_data.ui_mgr.show_ui('SkinDefineGuideDecalListUI', 'logic.comsys.mecha_display')
            self.is_list_guided = True

    def check_preview_new_decal(self):
        self.cur_decal_data = copy.deepcopy(global_data.emgr.get_decal_data.emit()[0])
        preview_start_idx = len(self.ori_decal_data)
        self.pre_decal_data = copy.deepcopy(self.cur_decal_data[preview_start_idx:])
        pre_decal_count = len(self.pre_decal_data)
        return pre_decal_count

    def check_preview_new_decal_dict(self):
        self.check_preview_new_decal()
        new_decal_dict = {}
        new_decal_idx_dict = {}
        if self.pre_decal_data:
            for idx, decal_data in enumerate(self.pre_decal_data):
                item_id = decal_data[0]
                if item_id not in new_decal_dict:
                    new_decal_dict[item_id] = 1
                    new_decal_idx_dict[item_id] = [idx]
                else:
                    new_decal_dict[item_id] += 1
                    new_decal_idx_dict[item_id].append(idx)

        return (
         new_decal_dict, new_decal_idx_dict)

    def update_item_list(self):
        self._item_id_to_ui_item = {}
        self.panel.list_applique.RecycleAllItem()
        self._scan_item_idx = 0
        self._create_item_idx = 0
        self.clear_async_action()
        if self.forbid_tag:
            return
        self._async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.create_list_item)])))

    def clear_async_action(self):
        if self._async_action is not None:
            self.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def create_list_item(self):
        start_time = time.time()
        while self._scan_item_idx < len(self.decal_conf):
            item_conf = self.decal_conf[str(self._scan_item_idx + 1)]
            item_no = item_conf.get('iItemID')
            own = global_data.player.get_item_num_by_no(item_no)
            if not own:
                self._scan_item_idx += 1
                continue
            list_item = self.panel.list_applique.ReuseItem(bRefresh=True)
            if not list_item:
                list_item = self.panel.list_applique.AddTemplateItem(bRefresh=True)
            list_item.temp_item_dark.btn_choose.SetSelect(False)
            self._item_id_to_ui_item[item_no] = list_item
            self.init_list_item(list_item, self._scan_item_idx, self._create_item_idx)
            self._create_item_idx += 1
            self._scan_item_idx += 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        if self.selected_item_idx != -1:
            item = self.panel.list_applique.GetItem(self.selected_item_idx)
            if hasattr(item, 'temp_item_dark'):
                item.temp_item_dark.btn_choose.SetSelect(True)
        is_empty = True if self._create_item_idx <= 0 else False
        self.panel.list_applique.setVisible(not is_empty)
        self.panel.img_empty.setVisible(is_empty)

    def init_list_item(self, list_item, scan_idx, create_idx):
        item_conf = self.decal_conf[str(scan_idx + 1)]
        res_path = item_conf.get('cResPath')
        list_item.temp_item_dark.item.SetDisplayFrameByPath('', res_path)
        item_id = item_conf.get('iItemID')
        item_count = global_data.player.get_item_num_by_no(item_id)
        list_item.temp_item_dark.lab_quantity.setVisible(True)
        list_item.temp_item_dark.lab_quantity.SetString(str(item_count))
        text_id = get_decal_text_by_item_id(item_id)
        list_item.lab_name.SetString(get_text_by_id(text_id))
        list_item.temp_item_dark.img_frame.SetDisplayFrameByPath('', item_utils.get_lobby_item_rare_degree_pic_by_item_no(str(item_id), 1, True))

        @list_item.temp_item_dark.btn_choose.unique_callback()
        def OnClick(_btn, _touch, _idx=create_idx, _path=res_path, *args):
            self._on_click_list_item(_idx, _path, *args)

    def _on_click_list_item(self, idx, res_path, *args):
        if not self.new_decal_tag:
            self.panel.btn_cancel.OnClick(TouchMock())
            self.panel.DelayCall(0.06, self._on_begin_preview_new_decal, idx, res_path, *args)
        else:
            self._on_begin_preview_new_decal(idx, res_path, *args)

    def _on_begin_preview_new_decal(self, idx, res_path, *args):
        if idx == self.selected_item_idx:
            self.panel.PlayAnimation('tips_appliquev')
            self.panel.nd_applique.setVisible(True)
            return
        self.can_move_tag = False
        self.panel.stopActionByTag(self.DELAY_TAG)
        self._switch_list_item(idx)
        self._init_decal(res_path)
        global_data.emgr.decal_image_change.emit(res_path)

        def delay_call():
            if not self.show_applique_tag:
                self.panel.PlayAnimation('show_applique')
                self.show_applique_tag = True
                self.panel.PlayAnimation('loop')
                self.panel.PlayAnimation('loop_rotate')
                self.panel.PlayAnimation('loop_scale')
            self.panel.btn_sure.SetEnable(True)
            self.panel.btn_cancel.SetEnable(True)
            self.can_move_tag = True
            self.panel.PlayAnimation('tips_appliquev')
            self.panel.nd_applique.setVisible(True)

        self.new_decal_tag = True
        self.panel.DelayCallWithTag(0.2, delay_call, self.DELAY_TAG)

    def _switch_list_item(self, idx):
        if idx != self.selected_item_idx:
            if self.selected_item_idx != -1:
                item = self.panel.list_applique.GetItem(self.selected_item_idx)
                if hasattr(item, 'temp_item_dark'):
                    item.temp_item_dark.btn_choose.SetSelect(False)
            self.selected_item_idx = idx
            if idx != -1:
                self.panel.list_applique.GetItem(idx).temp_item_dark.btn_choose.SetSelect(True)
            self.update_decal_price_btn()

    def update_decal_price_btn(self):
        self.panel.btn_buy.setVisible(False)
        self.panel.temp_price.setVisible(False)
        self.panel.lab_get_method.setVisible(False)
        self.panel.lab_choose_tips.setVisible(False)
        self.panel.btn_buy_gift.setVisible(True)

        @self.panel.btn_buy_gift.unique_callback()
        def OnClick(_btn, _touch, *args):
            self._on_click_buy_box()

    def _on_click_btn_buy(self, item_id):
        if item_id:
            if item_utils.can_jump_to_ui(str(item_id)):
                item_utils.jump_to_ui(str(item_id))
                self.panel.stopActionByTag(self.DELAY_TAG)
            else:
                goods_id = item_id
                groceries_buy_confirmUI(str(goods_id))
                self.parent.clear_buy_reward_blocking()

    def _on_click_buy_box(self, *args):
        ui = global_data.ui_mgr.get_ui('SkinDefineBuyDecalBoxUI')
        if ui:
            ui.close()
        ui = SkinDefineBuyDecalBoxUI()

    def reset_sliders(self):
        self.panel.progress_rotate.setPercentage(50.0)
        self.panel.progress_scale.setPercentage(50.0)
        self.panel.nd_rotate_btn.setRotation(0)
        self.panel.nd_scale_btn.setRotation(0)
        self.slider_value_rot = 0.5
        self.slider_value_scl = 0.5

    def update_sliders(self):
        self.cur_decal_data = copy.deepcopy(global_data.emgr.get_decal_data.emit()[0])
        data = None
        if self.selected_decal_idx != -1:
            if self.selected_tab_idx == 0:
                decal_idx = self.selected_decal_idx + len(self.ori_decal_data)
            elif self.selected_tab_idx == 1:
                decal_idx = self.selected_decal_idx
            else:
                return
            try:
                data = self.cur_decal_data[decal_idx]
            except IndexError:
                print('xxxxxxxxxxxxxx, wrong decal index :', self.selected_decal_idx, decal_idx)

        else:
            return
        if not data:
            return
        else:
            rot = data[6]
            scl = data[7]
            self.slider_value_rot = (rot - self.MIN_ROT) / (self.MAX_ROT - self.MIN_ROT)
            self.slider_value_scl = (scl - self.parent.MIN_SCL) / (self.parent.MAX_SCL - self.parent.MIN_SCL)
            _angle = self.MIN_ANGLE + self.slider_value_rot * (self.MAX_ANGLE - self.MIN_ANGLE)
            self.panel.nd_rotate_btn.setRotation(_angle)
            self.panel.progress_rotate.setPercentage(self.slider_value_rot * 100.0)
            _angle = self.MAX_ANGLE - self.slider_value_scl * (self.MAX_ANGLE - self.MIN_ANGLE)
            self.panel.nd_scale_btn.setRotation(_angle)
            self.panel.progress_scale.setPercentage(self.slider_value_scl * 100.0)
            return

    def bind_sliders_event(self):

        @self.panel.btn_rotate.unique_callback()
        def OnBegin(_btn, _touch, *args):
            self.panel.PlayAnimation('loop_rotate', scale=3.0)

        @self.panel.btn_rotate.unique_callback()
        def OnDrag(_btn, _touch, *args):
            delta = _touch.getDelta()
            ratio = delta.y / 399.0
            self.slider_value_rot += ratio
            if self.slider_value_rot > 1.0:
                self.slider_value_rot = 1.0
            elif self.slider_value_rot < 0.0:
                self.slider_value_rot = 0.0
            _angle = self.MIN_ANGLE + self.slider_value_rot * (self.MAX_ANGLE - self.MIN_ANGLE)
            self.panel.nd_rotate_btn.setRotation(_angle)
            self.panel.progress_rotate.setPercentage(self.slider_value_rot * 100.0)
            self._on_slider_rotate_change(None)
            return

        @self.panel.btn_rotate.unique_callback()
        def OnEnd(_btn, _touch, *args):
            self.panel.PlayAnimation('loop_rotate', scale=1.0)

        @self.panel.btn_scale.unique_callback()
        def OnBegin(_btn, _touch, *args):
            self.panel.PlayAnimation('loop_scale', scale=2.0)

        @self.panel.btn_scale.unique_callback()
        def OnDrag(_btn, _touch, *args):
            delta = _touch.getDelta()
            ratio = delta.y / 399.0
            self.slider_value_scl += ratio
            if self.slider_value_scl > 1.0:
                self.slider_value_scl = 1.0
            elif self.slider_value_scl < 0.0:
                self.slider_value_scl = 0.0
            _angle = self.MAX_ANGLE - self.slider_value_scl * (self.MAX_ANGLE - self.MIN_ANGLE)
            self.panel.nd_scale_btn.setRotation(_angle)
            self.panel.progress_scale.setPercentage(self.slider_value_scl * 100.0)
            self._on_slider_scale_change(None)
            return

        @self.panel.btn_scale.unique_callback()
        def OnEnd(_btn, _touch, *args):
            self.panel.PlayAnimation('loop_scale', scale=1.0)

    def update_decal_scene(self):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if not camera_ctrl:
            return
        else:
            anim = get_default_skin_define_anim(self.parent.model_id)
            global_data.emgr.handle_skin_define_model.emit(anim, 0)
            y = 10
            y_offset = confmgr.get('skin_define_camera').get(str(self.parent.mecha_id), {}).get('iYOffset', None)
            if not y_offset:
                log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
            else:
                y = y_offset
            pos = math3d.vector(0, y, 0)
            camera_ctrl.decal_camera_ctrl.center_pos = pos
            camera_ctrl.decal_camera_ctrl._is_active = True
            target_m = global_data.emgr.get_target_model.emit()[0]
            if target_m != self.parent.cur_model:
                global_data.emgr.set_decal_model.emit(self.parent.cur_model, self.parent.model_id)
            if self.first_enter_tag:
                data = copy.deepcopy(global_data.player.get_mecha_decal().get(str(get_main_skin_id(self.parent.model_id)), []))
                global_data.emgr.set_default_decal_data.emit(data)
                self.first_enter_tag = False
            return

    def exit_decal_scene(self):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if camera_ctrl:
            camera_ctrl.decal_camera_ctrl._is_active = False

    def update_decal_count(self):
        self.cur_decal_data = copy.deepcopy(global_data.emgr.get_decal_data.emit()[0])
        decal_count = len(self.cur_decal_data)
        self.panel.lab_equip_applique_num.setString(get_text_by_id(860129) + ' %d / %d' % (decal_count, MAX_DECAL_NUM))
        self.panel.btn_equiped.lab_applique_quantity.setString(' %d / %d' % (decal_count, MAX_DECAL_NUM))

    def init_ui_events(self):

        @self.panel.btn_clear.unique_callback()
        def OnClick(_btn, _touch, *args):
            if self.parent.widgets_helper.get_cur_widget() != self:
                return
            if self.show_applique_tag:
                self.panel.btn_cancel.OnClick(TouchMock())
            self._on_click_clear_decal()

        @self.panel.btn_equiped.btn_common.unique_callback()
        def OnClick(_btn, _touch, *args):
            if self.show_equiped_tag:
                return
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.panel.PlayAnimation('show_equiped')
            self.parent.PlayAnimation('show_equiped')
            self.show_equiped_tag = True
            self.update_decal_list()
            self.check_need_list_guide()

        @self.panel.btn_equiped_close.unique_callback()
        def OnClick(_btn, _touch, *args):
            if not self.show_equiped_tag:
                return
            self.panel.PlayAnimation('disappear_equiped')
            self.parent.PlayAnimation('disappear_equiped')
            self.show_equiped_tag = False

        @self.panel.nd_applique.unique_callback()
        def OnBegin(nd, _touch, *args):
            if not self.can_move_tag:
                return
            self._on_decal_begin(_touch)

        @self.panel.nd_applique.unique_callback()
        def OnDrag(nd, _touch, *args):
            if not self.can_move_tag:
                return
            self._on_decal_drag(_touch)

        @self.panel.btn_sure.unique_callback()
        def OnClick(btn, touch, *args):
            self.cur_decal_data = copy.deepcopy(global_data.emgr.get_decal_data.emit()[0])
            decal_count = len(self.cur_decal_data)
            if self.new_decal_tag:
                if decal_count >= MAX_DECAL_NUM:
                    global_data.game_mgr.show_tip(get_text_by_id(81905))
                    return
            self.panel.PlayAnimation('diappear_applique')
            self.panel.StopAnimation('tips_appliquev')
            self.panel.nd_applique.setVisible(False)
            self.panel.btn_sure.SetEnable(False)
            self.panel.btn_cancel.SetEnable(False)
            self.show_applique_tag = False
            self.panel.StopAnimation('loop')
            self.panel.StopAnimation('loop_rotate')
            self.panel.StopAnimation('loop_scale')
            self._confirm_decal()
            self._switch_list_item(-1)
            self.update_decal_count()
            if not self.show_equiped_tag:
                self.panel.PlayAnimation('show_equiped')
                self.parent.PlayAnimation('show_equiped')
                self.show_equiped_tag = True
            self.update_decal_list()

        @self.panel.btn_cancel.unique_callback()
        def OnClick(btn, touch, *args):
            self.panel.PlayAnimation('diappear_applique')
            self.panel.StopAnimation('tips_appliquev')
            self.panel.nd_applique.setVisible(False)
            self.panel.btn_sure.SetEnable(False)
            self.panel.btn_cancel.SetEnable(False)
            self.show_applique_tag = False
            self.panel.StopAnimation('loop')
            self.panel.StopAnimation('loop_rotate')
            self.panel.StopAnimation('loop_scale')
            self._cancel_decal()
            self._switch_list_item(-1)
            self.update_decal_list()

        @self.panel.btn_up.unique_callback()
        def OnClick(_btn, _touch, *args):
            self._mini_move(up_down=1)

        @self.panel.btn_down.unique_callback()
        def OnClick(_btn, _touch, *args):
            self._mini_move(up_down=-1)

        @self.panel.btn_left.unique_callback()
        def OnClick(_btn, _touch, *args):
            self._mini_move(left_right=1)

        @self.panel.btn_right.unique_callback()
        def OnClick(_btn, _touch, *args):
            self._mini_move(left_right=-1)

        self.panel.btn_up.SetPressEnable(True)
        self.panel.btn_up.SetPressNeedTime(0.1)

        @self.panel.btn_up.unique_callback()
        def OnPressedWithNum(_btn, _num, *args):
            self._mini_move(up_down=1, speed_num=_num)

        self.panel.btn_down.SetPressEnable(True)
        self.panel.btn_down.SetPressNeedTime(0.1)

        @self.panel.btn_down.unique_callback()
        def OnPressedWithNum(_btn, _num, *args):
            self._mini_move(up_down=-1, speed_num=_num)

        self.panel.btn_left.SetPressEnable(True)
        self.panel.btn_left.SetPressNeedTime(0.1)

        @self.panel.btn_left.unique_callback()
        def OnPressedWithNum(_btn, _num, *args):
            self._mini_move(left_right=1, speed_num=_num)

        self.panel.btn_right.SetPressEnable(True)
        self.panel.btn_right.SetPressNeedTime(0.1)

        @self.panel.btn_right.unique_callback()
        def OnPressedWithNum(_btn, _num, *args):
            self._mini_move(left_right=-1, speed_num=_num)

        @self.panel.btn_full_screen.unique_callback()
        def OnClick(_btn, _touch, *args):
            if self.parent.widgets_helper.get_cur_widget() != self:
                return
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.parent.PlayAnimation('disappear')
            if self.show_applique_tag:
                self.panel.btn_cancel.OnClick(TouchMock())
            ui = FullScreenBackUI(need_guide_action=True)
            if ui:
                ui.setBackFunctionCallback(self.quit_full_screen)
                ui.set_zoom_btn_visible(False)
                ui.set_action_list_vis(True)
                ui.set_mecha_info(self.parent.mecha_id, self.parent.model_id)

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch, *args):
            if self.parent.widgets_helper.get_cur_widget() != self:
                return
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.parent.PlayAnimation('disappear')
            if self.show_applique_tag:
                self.panel.btn_cancel.OnClick(TouchMock())
            ui = SkinDefineShareUI()
            if ui:
                ui.setBackFunctionCallback(self.quit_share)
                mecha_text = confmgr.get('mecha_display', 'HangarConfig', 'Content').get(str(self.parent.mecha_id), {}).get('name_mecha_text_id', '')
                skin_text = item_utils.get_lobby_item_name(self.parent.model_id)
                ui.set_mecha_info(self.parent.mecha_id, self.parent.model_id, mecha_text, skin_text)

    def on_resolution_changed(self):
        if self.parent.widgets_helper.get_cur_widget() != self:
            return
        if global_data.ui_mgr.get_ui('SkinDefineShareUI') or global_data.ui_mgr.get_ui('FullScreenBackUI'):
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.parent.PlayAnimation('disappear')
            if self.show_applique_tag:
                self.panel.btn_cancel.OnClick(TouchMock())
        self.default_pos = self.panel.convertToWorldSpace(self.panel.nd_applique.getPosition())
        self.panel.DelayCall(0.1, self.cancel_decal)

    def cancel_decal(self):
        self.panel.btn_cancel.OnClick(TouchMock())

    def quit_full_screen(self):
        if self.parent:
            self.parent.PlayAnimation('appear')
        if self.panel and self.panel.isValid():
            self.panel.PlayAnimation('appear')
        if self.show_equiped_tag:
            self.panel.PlayAnimation('show_equiped')

    def quit_share(self):
        self.quit_full_screen()

    def update_decal_list(self):
        self.panel.nd_equiped.list_equiped_applique.DeleteAllSubItem()
        self.selected_decal_idx = -1
        self.panel.btn_delete.setVisible(False)
        if self.selected_tab_idx == -1:
            return
        if self.selected_tab_idx == 0:
            self.update_preview_decal_list()
        elif self.selected_tab_idx == 1:
            self.update_equiped_decal_list()

    def update_preview_decal_list(self):
        new_decal_count = self.check_preview_new_decal()
        if new_decal_count:
            self.panel.nd_equiped.list_equiped_applique.SetInitCount(new_decal_count)
            for idx, ui_item in enumerate(self.panel.nd_equiped.list_equiped_applique.GetAllItem()):
                decal_data = self.pre_decal_data[idx]
                item_id = decal_data[0]
                res_path = get_decal_path_by_item_id(item_id)
                text_id = get_decal_text_by_item_id(item_id)
                ui_item.temp_applique.temp_item_dark.item.SetDisplayFrameByPath('', res_path)
                ui_item.lab_name.SetString(get_text_by_id(text_id))
                ui_item.temp_applique.temp_item_dark.img_frame.SetDisplayFrameByPath('', item_utils.get_lobby_item_rare_degree_pic_by_item_no(str(item_id), 1, True))

                @ui_item.btn.unique_callback()
                def OnClick(_btn, _touch, _idx=idx, *args):
                    self._on_click_preview_decal(_idx)

            self.panel.btn_delete.setVisible(True)

            @self.panel.btn_delete.unique_callback()
            def OnClick(_btn, _touch, *args):
                self._on_click_delete_decal()

        else:
            self.panel.btn_delete.setVisible(False)
        self._update_delete_btn_vis()

    def update_equiped_decal_list(self):
        decal_count = len(self.ori_decal_data)
        if decal_count:
            self.panel.nd_equiped.list_equiped_applique.SetInitCount(decal_count)
            for idx, ui_item in enumerate(self.panel.nd_equiped.list_equiped_applique.GetAllItem()):
                decal_data = self.ori_decal_data[idx]
                item_id = decal_data[0]
                res_path = get_decal_path_by_item_id(item_id)
                text_id = get_decal_text_by_item_id(item_id)
                ui_item.temp_applique.temp_item_dark.item.SetDisplayFrameByPath('', res_path)
                ui_item.lab_name.SetString(get_text_by_id(text_id))
                ui_item.temp_applique.temp_item_dark.img_frame.SetDisplayFrameByPath('', item_utils.get_lobby_item_rare_degree_pic_by_item_no(str(item_id), 1, True))

                @ui_item.btn.unique_callback()
                def OnClick(_btn, _touch, _idx=idx, *args):
                    self._on_click_preview_decal(_idx)

            self.panel.btn_delete.setVisible(True)

            @self.panel.btn_delete.unique_callback()
            def OnClick(_btn, _touch, *args):
                self._on_click_delete_decal()

        else:
            self.panel.btn_delete.setVisible(False)
        self._update_delete_btn_vis()

    def _on_click_preview_decal(self, idx):
        if self.selected_tab_idx == -1:
            return
        if idx == self.selected_decal_idx:
            self.panel.PlayAnimation('tips_appliquev')
            self.panel.nd_applique.setVisible(True)
            return
        if self.selected_tab_idx == 0:
            decal_idx = idx + len(self.ori_decal_data)
        elif self.selected_tab_idx == 1:
            decal_idx = idx
        global_data.emgr.select_preview_decal.emit(decal_idx)
        self._switch_preview_decal_item(idx)
        if not self.show_applique_tag:
            self.panel.PlayAnimation('show_applique')
            self.show_applique_tag = True
            self.panel.PlayAnimation('loop')
            self.panel.PlayAnimation('loop_rotate')
            self.panel.PlayAnimation('loop_scale')
        self._switch_list_item(-1)
        self.update_sliders()
        self.bind_sliders_event()
        self.panel.btn_sure.SetEnable(True)
        self.panel.btn_cancel.SetEnable(True)
        self.can_move_tag = True
        self.new_decal_tag = False
        self.panel.PlayAnimation('tips_appliquev')
        self.panel.nd_applique.setVisible(True)
        self._update_delete_btn_vis()

    def _switch_preview_decal_item(self, idx):
        if idx != self.selected_decal_idx:
            if self.selected_decal_idx != -1:
                ui_item = self.panel.nd_equiped.list_equiped_applique.GetItem(self.selected_decal_idx)
                ui_item.temp_applique.temp_item_dark.btn_choose.SetSelect(False)
                ui_item.lab_name.SetColor(self.UNSELECT_LAB_COLOR)
            self.selected_decal_idx = idx
            if idx != -1:
                ui_item = self.panel.nd_equiped.list_equiped_applique.GetItem(idx)
                ui_item.temp_applique.temp_item_dark.btn_choose.SetSelect(True)
                ui_item.lab_name.SetColor(self.SELECT_LAB_COLOR)

    def _on_click_delete_decal(self):
        if self.selected_tab_idx == -1:
            return
        if self.selected_decal_idx != -1:
            if self.selected_tab_idx == 0:
                decal_idx = self.selected_decal_idx + len(self.ori_decal_data)
                global_data.emgr.select_preview_decal.emit(decal_idx)
                global_data.emgr.del_preview_decal.emit()
                self._after_delete_decal()
                return
            if self.selected_tab_idx == 1:
                decal_idx = self.selected_decal_idx

                def on_confirm_delete():
                    main_skin_id = get_main_skin_id(self.parent.model_id)
                    global_data.player.del_mecha_decal(main_skin_id, self.selected_decal_idx)
                    global_data.emgr.select_preview_decal.emit(decal_idx)
                    global_data.emgr.del_preview_decal.emit()
                    self._after_delete_decal()

                def on_cancel():
                    pass

                ui = SecondConfirmDlg2(parent=self.panel)
                ui.confirm(content=get_text_by_id(81907), confirm_callback=on_confirm_delete, cancel_callback=on_cancel)
                ui.panel.setVisible(True)

    def _after_delete_decal(self):
        self.update_decal_list()
        self.selected_decal_idx = -1
        self._update_delete_btn_vis()
        self.update_decal_count()
        if self.show_applique_tag:
            self.panel.PlayAnimation('diappear_applique')
            self.panel.StopAnimation('tips_appliquev')
            self.panel.nd_applique.setVisible(False)
            self.show_applique_tag = False
            self.panel.StopAnimation('loop')
            self.panel.StopAnimation('loop_rotate')
            self.panel.StopAnimation('loop_scale')
            self.new_decal_tag = True
        self.parent.check_mecha_status()

    def _update_delete_btn_vis(self):
        if self.selected_decal_idx != -1:
            self.panel.btn_delete.setVisible(True)
        else:
            self.panel.btn_delete.setVisible(False)

    def _init_decal(self, tex_path):
        global_data.emgr.add_preview_decal.emit(tex_path)
        lpos = self.panel.nd_applique.getParent().convertToNodeSpace(self.default_pos)
        self.panel.nd_applique.setPosition(lpos)
        init_wpos = self.default_pos
        global_data.emgr.decal_position_change.emit(init_wpos.x, init_wpos.y)
        global_data.emgr.decal_rotation_change.emit(0)
        scale = (self.parent.MAX_SCL + self.parent.MIN_SCL) * 0.5
        global_data.emgr.decal_size_change.emit(scale)
        self.panel.nd_applique.setScaleX(scale * self.TIPS_SCALE)
        self.panel.nd_applique.setScaleY(scale * self.TIPS_SCALE)
        self.reset_sliders()
        self.bind_sliders_event()

    def _on_decal_begin(self, touch):
        nd_decal = self.panel.nd_applique
        touch_pos = touch.getLocation()
        lpos_touch = nd_decal.getParent().convertToNodeSpace(touch.getLocation())
        lpos_nd = self.panel.nd_applique.getPosition()
        self.offset_pos = cc.Vec2(lpos_nd.x - lpos_touch.x, lpos_nd.y - lpos_touch.y)

    def _on_decal_drag(self, touch):
        nd_decal = self.panel.nd_applique
        lpos = nd_decal.getParent().convertToNodeSpace(touch.getLocation())
        pos_x, pos_y = lpos.x + self.offset_pos.x, lpos.y + self.offset_pos.y
        if pos_x <= self.MIN_POS_X:
            pos_x = self.MIN_POS_X
        elif pos_x >= self.MAX_POS_X:
            pos_x = self.MAX_POS_X
        if pos_y <= self.MIN_POS_Y:
            pos_y = self.MIN_POS_Y
        elif pos_y >= self.MAX_POS_Y:
            pos_y = self.MAX_POS_Y
        nd_decal.setPosition(pos_x, pos_y)
        wpos = nd_decal.getParent().convertToWorldSpace(cc.Vec2(pos_x, pos_y))
        global_data.emgr.decal_position_change.emit(wpos.x, wpos.y)

    def _on_slider_rotate_change(self, slider_val):
        if slider_val:
            angle = self.MIN_ROT + slider_val * (self.MAX_ROT - self.MIN_ROT)
        else:
            angle = self.MIN_ROT + self.slider_value_rot * (self.MAX_ROT - self.MIN_ROT)
        global_data.emgr.decal_rotation_change.emit(angle)

    def _on_slider_scale_change(self, slider_val):
        if slider_val:
            scale = self.parent.MIN_SCL + slider_val * (self.parent.MAX_SCL - self.parent.MIN_SCL)
        else:
            scale = self.parent.MIN_SCL + self.slider_value_scl * (self.parent.MAX_SCL - self.parent.MIN_SCL)
        global_data.emgr.decal_size_change.emit(scale)
        self.panel.nd_applique.setScaleX(scale * self.TIPS_SCALE)
        self.panel.nd_applique.setScaleY(scale * self.TIPS_SCALE)

    def on_camera_scl(self):
        if self.show_applique_tag:
            self._on_slider_scale_change(None)
        return

    def _confirm_decal(self):
        global_data.emgr.save_preview_decal.emit()
        self.parent.check_mecha_status()
        if self.selected_decal_idx != -1 and self.selected_tab_idx == 1:
            self.cur_decal_data = copy.deepcopy(global_data.emgr.get_decal_data.emit()[0])
            if self.selected_decal_idx >= len(self.cur_decal_data):
                return
            modified_decal_data = self.cur_decal_data[self.selected_decal_idx]
            main_skin_id = get_main_skin_id(self.parent.model_id)
            global_data.player.mod_mecha_decal(main_skin_id, self.selected_decal_idx, modified_decal_data)

    def _cancel_decal(self):
        if self.new_decal_tag:
            global_data.emgr.del_preview_decal.emit()
        elif self.selected_decal_idx != -1:
            if self.selected_tab_idx == -1:
                return
            if self.selected_tab_idx == 0:
                global_data.emgr.revert_preview_decal.emit(self.selected_decal_idx + len(self.ori_decal_data))
            elif self.selected_tab_idx == 1:
                global_data.emgr.revert_preview_decal.emit(self.selected_decal_idx)

    def _reset_decal(self):
        lpos = self.panel.nd_applique.getParent().convertToNodeSpace(self.default_pos)
        self.panel.nd_applique.setPosition(lpos)
        init_wpos = self.default_pos
        global_data.emgr.decal_position_change.emit(init_wpos.x, init_wpos.y)
        global_data.emgr.decal_rotation_change.emit(0)
        scale = (self.parent.MAX_SCL + self.parent.MIN_SCL) * 0.5
        global_data.emgr.decal_size_change.emit(scale)
        self.panel.nd_applique.setScaleX(scale * self.TIPS_SCALE)
        self.panel.nd_applique.setScaleY(scale * self.TIPS_SCALE)
        self.reset_sliders()
        self.bind_sliders_event()

    def _mini_move(self, up_down=None, left_right=None, speed_num=1):
        up_dir, left_dir = (0, 0)
        if up_down:
            up_dir = 1 if up_down > 0 else -1
        if left_right:
            left_dir = -1 if left_right > 0 else 1
        nd_decal = self.panel.nd_applique
        pos = nd_decal.getPosition()
        if speed_num >= self.MINI_MAX_SPEED:
            speed_num = self.MINI_MAX_SPEED
        pos_x = pos.x + left_dir * self.MINI_DIS * speed_num
        pos_y = pos.y + up_dir * self.MINI_DIS * speed_num
        if pos_x <= self.MIN_POS_X:
            pos_x = self.MIN_POS_X
        elif pos_x >= self.MAX_POS_X:
            pos_x = self.MAX_POS_X
        if pos_y <= self.MIN_POS_Y:
            pos_y = self.MIN_POS_Y
        elif pos_y >= self.MAX_POS_Y:
            pos_y = self.MAX_POS_Y
        nd_decal.setPosition(pos_x, pos_y)
        wpos = nd_decal.getParent().convertToWorldSpace(cc.Vec2(pos_x, pos_y))
        global_data.emgr.decal_position_change.emit(wpos.x, wpos.y)

    def reset_decal_ui_param(self, pos, rot, scale):
        posx, posy = pos
        lpos = self.panel.nd_applique.getParent().convertToNodeSpace(cc.Vec2(posx, posy))
        self.panel.nd_applique.setPosition(lpos)
        global_data.emgr.decal_position_change.emit(posx, posy)
        self.rotate_angle = rot
        global_data.emgr.decal_rotation_change.emit(rot)
        self.decal_scale = scale
        global_data.emgr.decal_size_change.emit(scale)
        self.panel.nd_applique.setScaleX(scale * self.TIPS_SCALE)
        self.panel.nd_applique.setScaleY(scale * self.TIPS_SCALE)

    def _on_click_clear_decal(self):
        if not self.check_preview_new_decal():
            return

        def on_cancel():
            pass

        SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(81934), confirm_callback=self._do_clear_preview_decal, cancel_callback=on_cancel)

    def _do_clear_preview_decal(self):
        if self.pre_decal_data:
            for idx, decal_data in enumerate(self.pre_decal_data):
                decal_idx = len(self.ori_decal_data)
                global_data.emgr.select_preview_decal.emit(decal_idx)
                global_data.emgr.del_preview_decal.emit()

        self._after_delete_decal()

    def _on_buy_goods_success(self):
        lock_color = global_data.player.get_lock_color()
        lock_decal = global_data.player.get_lock_decal()
        if lock_color or lock_decal:
            return
        self.update_item_list()
        self.update_decal_price_btn()

    def on_upload_decal_data(self, decal_idx_list):
        decal_idx_list.sort()
        upload_decal_data = []
        update_decal_data = []
        for idx in decal_idx_list:
            if idx > len(self.pre_decal_data):
                break
            decal_data = self.pre_decal_data[idx]
            upload_decal_data.append(decal_data)

        for idx, data in enumerate(self.pre_decal_data):
            if idx not in decal_idx_list:
                update_decal_data.append(data)

        self.update_decal_data = copy.deepcopy(update_decal_data)
        main_skin_id = get_main_skin_id(self.parent.model_id)
        global_data.player.add_mecha_decal(main_skin_id, upload_decal_data)

    def on_del_mecha_decal(self):
        mecha_decal_data = global_data.player.get_mecha_decal()
        self.ori_decal_data = copy.deepcopy(mecha_decal_data.get(str(get_main_skin_id(self.parent.model_id)), []))
        self.update_decal_list()

    def on_add_mecha_decal(self):
        if self.update_decal_data:
            data = copy.deepcopy(global_data.player.get_mecha_decal().get(str(get_main_skin_id(self.parent.model_id)), []))
            data.extend(self.update_decal_data)
            global_data.emgr.set_default_decal_data.emit(data, self.on_add_mecha_decal_finish)
            self.update_decal_data = []
        else:
            self.on_add_mecha_decal_finish()

    def on_add_mecha_decal_finish(self):
        mecha_decal_data = global_data.player.get_mecha_decal()
        self.ori_decal_data = copy.deepcopy(mecha_decal_data.get(str(get_main_skin_id(self.parent.model_id)), []))
        if self.update_decal_data:

            def delay_call_decal():
                global_data.emgr.add_preview_decal.emit('gui/ui_res_2/icon/icon_empty.png')

            self.panel.DelayCallWithTag(0.06, delay_call_decal, 20201012)
        self.update_decal_count()
        self.update_decal_list()
        self.parent.check_mecha_status()

    def on_batch_buy_update(self):
        self._on_buy_goods_success()

    def destroy(self):
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.first_enter_tag = True
        self._scan_item_idx = 0
        self._create_item_idx = 0
        self._async_action = None
        self.offset_pos = cc.Vec2(0, 0)
        self.selected_item_idx = -1
        self.show_equiped_tag = False
        self.show_applique_tag = False
        self.can_move_tag = False
        self.selected_decal_idx = -1
        self.ori_decal_data = []
        self.cur_decal_data = []
        self.pre_decal_data = []
        self.update_decal_data = []
        self.slider_value_rot = None
        self.slider_value_scl = None
        self.decal_idx_item_id_dict = {}
        super(SkinDefineDecalWidget, self).destroy()
        return

    @staticmethod
    def check_red_point():
        return False