# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefinePoseWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import skin_define_utils, item_utils, red_point_utils
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_GESTURE
import math3d
import copy
import world

class SkinDefinePoseWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_id):
        self.global_events = {'player_item_update_event': self._on_buy_goods_success,
           'set_mecha_pose_result_event': self._on_set_mecha_pose,
           'set_mecha_pose_apply_event': self._on_update_mecha_pose_show,
           'del_mecha_pose_result_event': self._on_del_mecha_pose
           }
        super(SkinDefinePoseWidget, self).__init__(parent, panel)
        self.init_params()
        self.parent.pose_widget = self

    def init_params(self):
        self.selected_idx = -1
        self.pose_id_2_ui_idx = {}

    def show(self):
        pass

    def hide(self):
        pass

    def do_show_widget(self):
        global_data.emgr.bind_events(self.global_events)
        self.update_widget(True)

    def do_hide_widget(self):
        global_data.emgr.unbind_events(self.global_events)

    def update_widget(self, is_show):
        if is_show:
            self.init_ui_events()
            self.update_mecha_info()
            self.update_pose_scene()
            self.update_pose_list()
            self.init_apply_mecha_pose_show_btn()
        else:
            self.exit_pose_scene()

    def get_animate_kwargs(self):
        kwargs = {'anim_arg': [0, -1, 0, world.PLAY_FLAG_LOOP, 1.0]}
        return kwargs

    def update_mecha_info(self):
        if not self.parent:
            return
        else:
            self.skin_id = self.parent.model_id
            self.mecha_id = self.parent.mecha_id
            self.pose_conf = skin_define_utils.get_mecha_pose_conf(self.mecha_id) or []
            self.pose_show_list = []
            for pose_item_no in self.pose_conf:
                if not item_utils.can_open_show(pose_item_no, owned_should_show=True):
                    continue
                self.pose_show_list.append(pose_item_no)

            self.pose_dict = global_data.player.get_mecha_pose()
            self.ori_pose = self.pose_dict.get(str(battle_id_to_mecha_lobby_id(self.mecha_id)), None)
            self.cur_pose = copy.deepcopy(self.ori_pose)
            return

    def update_pose_scene(self):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if not camera_ctrl:
            return
        else:
            anim = item_utils.get_lobby_item_res_path(self.cur_pose, skin_id=get_main_skin_id(self.skin_id))
            if not anim:
                anim = skin_define_utils.get_default_skin_define_anim(self.parent.model_id)
            kwargs = self.get_animate_kwargs()
            global_data.emgr.handle_skin_define_model.emit(anim, 0, **kwargs)
            y = 10
            y_offset = confmgr.get('skin_define_camera').get(str(self.parent.mecha_id), {}).get('iYOffset', None)
            if not y_offset:
                log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
            else:
                y = y_offset
            pos = math3d.vector(0, y, 0)
            camera_ctrl.decal_camera_ctrl.center_pos = pos
            camera_ctrl.decal_camera_ctrl._is_active = True
            return

    def exit_pose_scene(self):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if camera_ctrl:
            camera_ctrl.decal_camera_ctrl._is_active = False

    def init_ui_events(self):
        if not self.panel:
            return
        self.panel.nd_in.lab_number.setVisible(False)
        self.panel.nd_in.lab_fx_name.setVisible(False)
        self.panel.nd_in.lab_get_method.setVisible(False)
        self.panel.nd_in.temp_btn_use.setVisible(False)

    def on_resolution_changed(self):
        pass

    def update_pose_list(self):
        if not self.panel:
            return
        if not self.pose_show_list:
            self.panel.img_empty.setVisible(True)
            return
        self.panel.img_empty.setVisible(False)
        self.panel.nd_in.list_fx.DeleteAllSubItem()
        self.panel.nd_in.list_fx.SetInitCount(len(self.pose_show_list))
        for index, ui_item in enumerate(self.panel.nd_in.list_fx.GetAllItem()):
            item_id = self.pose_show_list[index]
            ui_item.img_fx.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_id))
            ui_item.img_base.setVisible(True)
            if self.ori_pose and item_id == self.ori_pose:
                ui_item.nd_using.setVisible(True)
                self.selected_idx = index
                ui_item.btn_choose.SetSelect(True)
                self.update_status(item_id)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_id)
            red_point_utils.show_red_point_template(ui_item.nd_new, show_new)
            if global_data.player:
                has = global_data.player.has_item_by_no if 1 else (lambda : False)
                is_owned = has(int(item_id))
                ui_item.nd_lock.setVisible(not is_owned)
                self.pose_id_2_ui_idx[item_id] = index

                @ui_item.btn_choose.unique_callback()
                def OnClick(_btn, _touch, _idx=index, _item_id=item_id, _ui_item=ui_item, _show_new=show_new):
                    self._on_click_pose(_idx, _item_id)
                    if _show_new:
                        global_data.player.req_del_item_redpoint(_item_id)
                        red_point_utils.show_red_point_template(_ui_item.nd_new, False)

    def _on_click_pose(self, idx, item_id):
        self._switch_list_item(idx)
        pose = skin_define_utils.get_mecha_pose_anim(item_id, skin_id=get_main_skin_id(self.skin_id))
        kwargs = self.get_animate_kwargs()
        global_data.emgr.handle_skin_define_model.emit(pose, 0, **kwargs)
        self.cur_pose = item_id
        self.update_status(item_id)
        self._on_update_mecha_pose_show()

    def init_apply_mecha_pose_show_btn(self):
        self._on_update_mecha_pose_show()

        @self.panel.temp_setting.btn.callback()
        def OnClick(btn, touch):
            is_select = btn.GetSelect()
            global_data.player.set_apply_mecha_pose_show(int(not is_select))

    def _on_update_mecha_pose_show(self):
        is_apply = global_data.player.is_apply_mecha_pose()
        item_type = item_utils.get_lobby_item_type(self.cur_pose)
        is_show = item_type == L_ITEM_TYPE_MECHA_GESTURE
        self.panel.temp_setting.setVisible(is_show)
        self.panel.temp_setting.btn.SetSelect(is_apply)
        self.panel.temp_setting.btn.bar.choose.setVisible(is_apply)

    def _switch_list_item(self, idx):
        if self.selected_idx != -1:
            self.panel.nd_in.list_fx.GetItem(self.selected_idx).btn_choose.SetSelect(False)
        self.selected_idx = idx
        if idx != -1:
            self.panel.nd_in.list_fx.GetItem(idx).btn_choose.SetSelect(True)

    def update_status(self, item_id):
        self.panel.lab_fx_name.setVisible(True)
        self.panel.lab_fx_name.SetString(item_utils.get_lobby_item_name(item_id))
        has = global_data.player.has_item_by_no if global_data.player else (lambda : False)
        is_owned = has(int(item_id))
        is_owned_mecha = has(int(battle_id_to_mecha_lobby_id(self.mecha_id)))
        if is_owned:
            self.panel.lab_get_method.setVisible(False)
            if self.ori_pose == item_id:
                text = get_text_by_id(608105)
                enable_btn = True
            elif is_owned_mecha:
                text = get_text_by_id(2212)
                enable_btn = True
            else:
                text = get_text_by_id(81030)
                enable_btn = False
        else:
            self.panel.lab_get_method.setVisible(True)
            self.panel.lab_get_method.SetString(item_utils.get_item_access(item_id))
            if item_utils.can_jump_to_ui(item_id):
                text = get_text_by_id(2222)
                enable_btn = True
            else:
                text = get_text_by_id(80828)
                enable_btn = False
        self.panel.temp_btn_use.setVisible(True)
        self.panel.temp_btn_use.btn_common.SetText(text)
        self.panel.temp_btn_use.btn_common.SetShowEnable(enable_btn)
        self.panel.temp_btn_use.btn_common.SetEnable(enable_btn)
        if enable_btn:

            @self.panel.temp_btn_use.btn_common.unique_callback()
            def OnClick(_btn, _touch, _own=is_owned, _item_id=item_id):
                self._on_click_btn_use(_own, _item_id)

    def _on_click_btn_use(self, own, item_id):
        if own:
            mecha_id = int(battle_id_to_mecha_lobby_id(self.mecha_id))
            if self.ori_pose == item_id:
                global_data.player.try_del_mecha_pose(mecha_id)
            else:
                pose_id = item_id
                global_data.player.try_set_mecha_pose(mecha_id, pose_id)
        else:
            item_utils.jump_to_ui(item_id)

    def _on_set_mecha_pose(self):
        mecha_pose_data = global_data.player.get_mecha_pose()
        self.ori_pose = copy.deepcopy(mecha_pose_data.get(str(battle_id_to_mecha_lobby_id(self.mecha_id)), None))
        self.update_pose_list()
        if self.ori_pose and self.ori_pose == self.cur_pose:
            self.update_status(self.cur_pose)
        return

    def _on_del_mecha_pose(self):
        mecha_pose_data = global_data.player.get_mecha_pose()
        self.ori_pose = copy.deepcopy(mecha_pose_data.get(str(battle_id_to_mecha_lobby_id(self.mecha_id)), None))
        anim = skin_define_utils.get_default_skin_define_anim(self.parent.model_id)
        kwargs = self.get_animate_kwargs()
        global_data.emgr.handle_skin_define_model.emit(anim, 0, **kwargs)
        self.update_pose_list()
        self.init_ui_events()
        return

    def _on_buy_goods_success(self):
        self.update_mecha_info()
        self.init_ui_events()
        self.selected_idx = -1
        self.update_pose_list()

    @staticmethod
    def check_red_point():
        return False