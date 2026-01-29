# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/LobbyItemDescUI.py
from __future__ import absolute_import
import copy
from common.uisys.basepanel import BasePanel
from cocosui import cc, ccui, ccs
import common.const.uiconst
from logic.comsys.mecha_display.LobbyItemPreviewUI import LobbyItemPreviewUI
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_name, get_lobby_item_desc, get_lobby_item_type_name_by_id
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import career_utils
from logic.gutils.role_utils import get_role_name_id

class LobbyItemDescUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/i_item_describe'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    BORDER_INDENT = 24
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'nd_bg.OnBegin': '_hide_item_desc_info'
       }
    GLOBAL_EVENT = {'receive_reward_info_from_server_event': '_show_item_preview_info',
       'show_item_desc_ui_event': '_show_item_desc_info',
       'hide_item_desc_ui_event': '_hide_item_desc_info'
       }

    def on_init_panel(self, *args, **kwargs):
        self._is_multi_get_way = False
        self._item_no = None
        self.hide()
        self.request_item_id = -1
        return

    def show_jump_to_multi_ui_info(self, item_no):
        jump_to_multi_ui_info = confmgr.get('lobby_item', str(item_no), 'jump_to_multi_ui_info', default=[])
        self._is_multi_get_way = len(jump_to_multi_ui_info) > 0
        if not self._is_multi_get_way:
            return
        self.panel.temp_btn_check.btn_common.SetText(603016)
        self.panel.temp_btn_check.setVisible(self._is_multi_get_way)

        @self.panel.temp_btn_check.btn_common.callback()
        def OnClick(btn, touch):
            global_data.emgr.show_item_obtain_ui_event.emit(item_no, self.panel, jump_to_multi_ui_info)

    def _show_item_preview_info(self):
        use_params = confmgr.get('lobby_item', str(self.request_item_id), default={}).get('use_params', {})
        reward_id = use_params.get('reward_id', -1)
        if self.request_item_id != -1 and global_data.player and global_data.player.get_random_reward_data(reward_id):
            ui = LobbyItemPreviewUI(None, self.request_item_id, True)
            self.request_item_id = -1
        return

    def _show_item_desc_info(self, item_no_or_info_dict, wpos, directly_world_pos=None, extra_info=None, item_num=0):
        use_params = confmgr.get('lobby_item', str(item_no_or_info_dict), default={}).get('use_params', {})
        if use_params.get('need_preview', 0):
            ui = LobbyItemPreviewUI(None, item_no_or_info_dict)
        elif use_params.get('need_probability', 0):
            reward_id = use_params.get('reward_id', -1)
            if global_data.player and global_data.player.get_random_reward_data(reward_id):
                ui = LobbyItemPreviewUI(None, item_no_or_info_dict, True)
                self.request_item_id = -1
            else:
                self.request_item_id = item_no_or_info_dict
        else:
            self._is_multi_get_way = False
            if not type(item_no_or_info_dict) == dict:
                info_dict = {}
                self._item_no = item_no = item_no_or_info_dict
                self.panel.lab_item_name.SetString(get_lobby_item_name(item_no))
                ty = get_lobby_item_type(item_no)
                self.panel.lab_item_sort.SetString(get_lobby_item_type_name_by_id(item_no))
            else:
                info_dict = item_no_or_info_dict
                self._item_no = item_no = info_dict.get('item_no')
                ty = info_dict.get('type')
                name_text = info_dict.get('name_text')
                ty_text = info_dict.get('type_text', '')
                self.panel.lab_item_name.SetString(name_text)
                self.panel.lab_item_sort.SetString(ty_text)
            if extra_info is None:
                extra_info = {}
            if 'name_txt' in extra_info:
                self.panel.lab_item_name.SetString(extra_info['name_txt'])
            need_check_jump = extra_info.get('show_jump', True) if extra_info else True
            btn_func = extra_info.get('btn_func', None) if extra_info else None
            btn_text = extra_info.get('btn_text', None)
            show_tips = extra_info.get('show_tips', None)
            tips_args = extra_info.get('tips_args', [])
            force_rare_degree = extra_info.get('force_rare_degree', None)
            if btn_text != None:
                self.panel.temp_btn_check.btn_common.SetText(btn_text)
            if btn_func:
                btn_enable = extra_info.get('btn_enable', True)
                self.panel.temp_btn_check.btn_common.SetEnable(btn_enable)

                @self.panel.temp_btn_check.btn_common.callback()
                def OnClick(btn, touch):
                    self._hide_item_desc_info()
                    btn_func()

                self.panel.temp_btn_check.setVisible(True)
            elif need_check_jump:
                jump_to_ui_info = confmgr.get('lobby_item_type', str(ty), 'cJumpToUI', default={})
                need_update_args = True
                if not jump_to_ui_info:
                    need_update_args = False
                    jump_to_ui_info = confmgr.get('lobby_item', str(item_no), 'jump_to_ui_info', default={})
                is_can_jump = bool(jump_to_ui_info)
                self.panel.temp_btn_check.setVisible(is_can_jump)
                if is_can_jump:

                    @self.panel.temp_btn_check.btn_common.callback()
                    def OnClick(btn, touch):
                        self._hide_item_desc_info()
                        if need_update_args:
                            new_jump_to_ui_info = copy.deepcopy(jump_to_ui_info)
                            new_jump_to_ui_info.update({'args': [item_no]})
                        else:
                            new_jump_to_ui_info = jump_to_ui_info
                        ui_receive = global_data.ui_mgr.get_ui('ReceiveRewardUI')
                        if ui_receive and ui_receive.isPanelVisible() and ui_receive.is_showing():
                            ui_receive.close()
                        global_data.emgr.close_reward_preview_event.emit()
                        item_utils.exec_jump_to_ui_info(new_jump_to_ui_info)

            else:
                self.panel.temp_btn_check.setVisible(False)
            self.show_jump_to_multi_ui_info(item_no)
            temp_ui_item = self.panel.temp_item.GetItem(0)
            from logic.gutils import template_utils
            is_flag = extra_info.get('is_flag', False)
            self.panel.temp_item.setVisible(not is_flag)
            self.panel.temp_flag.setVisible(is_flag)
            self.panel.lab_tips and self.panel.lab_tips.setVisible(show_tips is not None)
            if len(tips_args) >= 2 and show_tips:
                self.panel.lab_tips and self.panel.lab_tips.setString(get_text_by_id(show_tips).format(get_text_by_id(get_role_name_id(tips_args[0])), tips_args[1]))
            if is_flag:
                career_utils.refresh_badge_item(self.panel.temp_flag, item_no, extra_info.get('level', 1), cp_reward_idx=extra_info.get('cp_reward_idx', None), check_got=False, ban_anim=True)
            elif item_no:
                template_utils.init_tempate_mall_i_item(temp_ui_item, item_no, item_num, force_rare_degree=force_rare_degree)
            if extra_info:
                show_desc = extra_info.get('show_desc', '') if 1 else ''
                if not show_desc:
                    show_desc = get_lobby_item_desc(item_no)
                self.panel.lab_item_describe.SetString(show_desc)
                icon = info_dict.get('icon')
                if icon:
                    temp_ui_item.item.SetDisplayFrameByPath('', icon)
                if extra_info:
                    hide_frame = extra_info.get('hide_frame', False)
                    if hide_frame:
                        temp_ui_item.img_frame.setOpacity(0)
                        temp_ui_item.img_frame.SetEnableCascadeOpacityRecursion(False)
                if not directly_world_pos:
                    self.panel.setAnchorPoint(cc.Vec2(1.06, -0.1))
                    pos = self.panel.GetParent().convertToNodeSpace(wpos)
                else:
                    pos = self.panel.GetParent().convertToNodeSpace(directly_world_pos)
                    cur_screen_size = global_data.ui_mgr.design_screen_size
                    center_x, center_y = cur_screen_size.width / 2, cur_screen_size.height / 2
                    if pos.x < center_x:
                        anchor_x = -0.06
                    else:
                        anchor_x = 1.06
                    if pos.y < center_y:
                        anchor_y = -0.1
                    else:
                        anchor_y = 1.1
                    self.panel.setAnchorPoint(cc.Vec2(anchor_x, anchor_y))
                self.hide_yunbao_details()
                if extra_info and extra_info.get('show_yuanbao', False):
                    self.show_yunbao_details()
            self.panel.setPosition(pos.x, pos.y)
            self.show()
        return

    def _hide_item_desc_info(self, *args):
        self.panel.lab_free_num.setVisible(False)
        self.panel.lab_paid_num.setVisible(False)
        global_data.emgr.hide_item_obtain_ui_event.emit()
        self.hide()

    def show_yunbao_details(self):
        if not G_IS_NA_PROJECT:
            return
        self.panel.lab_free_num.setVisible(True)
        self.panel.lab_paid_num.setVisible(True)
        pay_yuanbao = global_data.player.pay_yuanbao
        free_yuanbao = global_data.player.free_yuanbao
        fine_yuanbao = global_data.player.fine_yuanbao
        if free_yuanbao <= 0 and pay_yuanbao <= 0:
            pay_yuanbao = -fine_yuanbao
        self.panel.lab_paid_num.setString(get_text_by_id(81111, (pay_yuanbao,)))
        self.panel.lab_free_num.setString(get_text_by_id(81112, (free_yuanbao,)))

    def hide_yunbao_details(self):
        if self.panel.lab_free_num.isVisible():
            self.panel.lab_free_num.setVisible(False)
        if self.panel.lab_paid_num.isVisible():
            self.panel.lab_paid_num.setVisible(False)

    def ui_vkb_custom_func(self):
        self._hide_item_desc_info()