# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryRewardLabelWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_belong_name, get_lobby_item_desc, get_lobby_item_type, check_skin_tag, check_is_improvable_skin, check_show_skin_improve_tips, check_improvable_skin_diff_appearance
from logic.gutils.mecha_skin_utils import is_s_skin_that_can_upgrade
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_HEAD_PHOTO, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SP_ACTION
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.jump_to_ui_utils import jump_to_skin_improve_ui
from logic.gutils.lobby_click_interval_utils import global_unique_click
from .SkinCustomJumpEntryWidget import SkinCustomJumpEntryWidget
DEFAULT_TEMPLATE_PATH = 'mall/lottery_reward_label/i_default_reward_label'

class LotteryRewardLabelWidget(object):

    def __init__(self, panel, parent, improve_tips_visible_changed_callback, check_show_ex_skin_red_point_and_bubble_callback):
        self.panel = panel
        self.parent = parent
        self.improve_tips_visible_changed_callback = improve_tips_visible_changed_callback
        self.check_show_ex_skin_red_point_and_bubble_callback = check_show_ex_skin_red_point_and_bubble_callback
        self.cur_template_path = None
        self.nd_parent = None
        self.nd_common_reward = None
        self.nd_special_reward = None
        self.lottery_id_to_template_path_map = {}
        self.template_path_to_node_map = {}
        self.lottery_conf = confmgr.get('lottery_page_config')
        self.skin_custom_jump_widget = None
        self.hide_btn_ss = False
        self.visible = True
        self.cur_item_no = None
        return

    def destroy(self):
        self.panel = None
        self.parent = None
        self.improve_tips_visible_changed_callback = None
        self.check_show_ex_skin_red_point_and_bubble_callback = None
        self.nd_parent = None
        self.nd_common_reward = None
        self.nd_special_reward = None
        self.lottery_id_to_template_path_map = {}
        self.template_path_to_node_map = {}
        self.lottery_conf = None
        return

    def set_visible(self, visible):
        if self.visible ^ visible:
            self.visible = visible
            self.nd_parent and self.nd_parent.setVisible(visible)

    def play_animation(self, animation_name):
        if self.nd_parent and self.nd_parent.HasAnimation(animation_name):
            self.nd_parent.PlayAnimation(animation_name)

    def _set_label_node_visible(self, visible):
        self.nd_common_reward.setVisible(visible)
        self.nd_special_reward.setVisible(visible)

    def refresh_lottery_id(self, lottery_id):
        if lottery_id not in self.lottery_id_to_template_path_map:
            template_path = self.lottery_conf.get(lottery_id, {}).get('reward_info_label_template_path', DEFAULT_TEMPLATE_PATH)
            self.lottery_id_to_template_path_map[lottery_id] = template_path
        template_path = self.lottery_id_to_template_path_map[lottery_id]
        if self.cur_template_path:
            self._set_label_node_visible(False)
        self.cur_template_path = template_path
        need_bind_ui_event = False
        if template_path not in self.template_path_to_node_map:
            nd = global_data.uisystem.load_template_create(template_path, self.panel.nd_display)
            self.template_path_to_node_map[template_path] = nd
            need_bind_ui_event = True
        nd = self.template_path_to_node_map[template_path]
        nd.setVisible(self.visible)
        self.nd_parent = nd
        self.nd_common_reward = nd.nd_common_reward
        self.nd_special_reward = nd.nd_special_reward
        self.hide_btn_ss = self.lottery_conf.get(lottery_id, {}).get('hide_btn_ss', False)
        self.show_btn_pet = self.lottery_conf.get(lottery_id, {}).get('extra_data', {}).get('show_btn_pet', 0)
        self.pet_skin_no = self.lottery_conf.get(lottery_id, {}).get('extra_data', {}).get('pet_skin_no', '')
        self._set_label_node_visible(True)
        btn_ss = self.get_btn_ss()
        if btn_ss:
            if not self.skin_custom_jump_widget:
                self.skin_custom_jump_widget = SkinCustomJumpEntryWidget(self.parent, btn_ss)
            else:
                self.skin_custom_jump_widget.switch_panel(btn_ss)
        if need_bind_ui_event:
            btn_s_plus = self.get_btn_s_plus()
            if btn_s_plus:

                @global_unique_click(btn_s_plus)
                def OnClick(*args, **kwargs):
                    cur_show_model_id = self.parent.cur_show_model_id
                    if check_is_improvable_skin(cur_show_model_id):
                        jump_to_skin_improve_ui(int(cur_show_model_id))
                        self.improve_tips_visible_changed_callback(False)
                    elif is_s_skin_that_can_upgrade(cur_show_model_id):
                        from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                        jump_to_display_detail_by_item_no(cur_show_model_id)

            get_btn_diy = self.get_btn_diy()
            if get_btn_diy:

                @global_unique_click(get_btn_diy)
                def OnClick(*args, **kwargs):
                    from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                    jump_to_display_detail_by_item_no(self.cur_item_no)

        btn_pet = self.get_btn_pet()
        if btn_pet:
            btn_pet.temp_red.setVisible(False)
            if self.show_btn_pet:
                btn_pet.setVisible(True)
            else:
                btn_pet.setVisible(False)
        if self.show_btn_pet:
            if btn_pet:

                @global_unique_click(btn_pet)
                def OnClick(*args, **kwargs):
                    self.on_click_btn_pet()

    def _check_show_improve_s_plus_btn(self, item_no):
        restrict_info = confmgr.get('pendant', 'SkinRestrict', str(item_no), default={})
        unusable_skin_list = set(restrict_info.get('unusable_skin_list', []))
        usable_skin_list = set(restrict_info.get('usable_skin_list', []))
        need_consider_skins = usable_skin_list - unusable_skin_list
        for consider_skin in need_consider_skins:
            if not check_is_improvable_skin(consider_skin):
                continue
            top_skin = confmgr.get('role_info', 'RoleSkin', 'Content', str(consider_skin), 'belonging_top_skin_id', default=None)
            if not top_skin:
                continue
            improve_collected_items = confmgr.get('role_info', 'RoleSkin', 'Content', str(top_skin), 'skin_improve_collected_items', default=[])
            if int(item_no) not in improve_collected_items:
                continue
            item_no = consider_skin
            break

        btn_s_plus = self.get_btn_s_plus()
        if btn_s_plus:
            btn_s_plus.setVisible(check_is_improvable_skin(item_no))
        nd_diff_text = self.get_nd_s_plus_skin_diff_appearance()
        if nd_diff_text:
            nd_diff_text.setVisible(check_improvable_skin_diff_appearance(item_no))
        show_improve_tips = check_show_skin_improve_tips(item_no)
        self.improve_tips_visible_changed_callback(show_improve_tips)
        return

    def _check_show_mecha_s_plus_btn(self, item_no):
        if check_is_improvable_skin(item_no):
            return
        btn_s_plus = self.get_btn_s_plus()
        if btn_s_plus:
            btn_s_plus.setVisible(is_s_skin_that_can_upgrade(item_no))

    def _check_show_diy_btn(self, item_no=None):
        btn_diy = self.get_btn_diy()
        if not btn_diy:
            return
        else:
            if item_no is None:
                item_no = self.cur_item_no
            if item_no is None:
                btn_diy.setVisible(False)
                return
            if check_is_improvable_skin(item_no):
                btn_diy.setVisible(False)
                return
            if item_no is not None:
                item_type = get_lobby_item_type(item_no) if 1 else None
                is_role_skin = item_type == L_ITEM_TYPE_ROLE_SKIN
                is_role_skin or btn_diy.setVisible(False)
                return
            from logic.gutils.item_utils import get_lobby_item_belong_no
            belong_item_no = get_lobby_item_belong_no(item_no)
            if belong_item_no is None:
                btn_diy.setVisible(False)
                return
            from logic.gcommon.item.item_utility import is_role_item
            if is_role_item(belong_item_no):
                role_item_no = belong_item_no
            else:
                role_item_no = None
            if role_item_no is None:
                btn_diy.setVisible(False)
                return
            from logic.gutils.dress_utils import role_skin_should_show_custom
            btn_diy.setVisible(bool(role_skin_should_show_custom(role_item_no, item_no)))
            return

    def refresh_reward_info(self, item_no, specific_name, show_model):
        self.nd_common_reward.setVisible(not show_model)
        self.nd_special_reward.setVisible(show_model)
        self.cur_item_no = item_no
        if show_model:
            if specific_name:
                item_name = specific_name if 1 else get_lobby_item_name(item_no)
                self.nd_special_reward.lab_name.SetString(item_name)
                self.nd_special_reward.lab_name.ChildResizeAndPosition()
                belong_name = get_lobby_item_belong_name(item_no)
                belong_name = belong_name or 18801
            if str(item_no) == '98':
                belong_name = 495075
            self.nd_special_reward.lab_role_name.SetString(belong_name)
            self.nd_special_reward.lab_role_name.ChildResizeAndPosition()
            check_skin_tag(self.nd_special_reward.lab_name.nd_kind, item_no, ignore_improve=True)
            if self.skin_custom_jump_widget:
                self.skin_custom_jump_widget.set_item(item_no)
            self._check_show_improve_s_plus_btn(item_no)
            self._check_show_mecha_s_plus_btn(item_no)
            self._check_show_diy_btn(item_no)
            self.check_show_ex_skin_red_point_and_bubble_callback(item_no)
        else:
            check_skin_tag(self.nd_common_reward.nd_kind, item_no, ignore_improve=True)
            self.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))
            item_name = get_lobby_item_name(item_no)
            item_type = get_lobby_item_type(item_no)
            special_prefix_dic = {L_ITEM_TYPE_HEAD_PHOTO: 81299,
               L_ITEM_TYPE_MECHA_SP_ACTION: 906651
               }
            if item_type in special_prefix_dic:
                item_name = '[%s] ' % get_text_by_id(special_prefix_dic[item_type]) + item_name
            self.nd_common_reward.lab_name.SetString(item_name)
            self.nd_common_reward.lab_describe.SetString(get_lobby_item_desc(item_no))
            self.nd_common_reward.setVisible(bool(item_no))
        if self.show_btn_pet:
            ui = global_data.ui_mgr.get_ui('MainChat')
            ui and ui.do_hide_panel()
        show_btn_pet = bool(show_model and self.pet_skin_no and self.pet_skin_no == str(item_no))
        btn_pet = self.get_btn_pet()
        btn_pet and btn_pet.setVisible(show_btn_pet)

    def get_btn_s_plus(self):
        if self.nd_special_reward and self.nd_special_reward.lab_name and self.nd_special_reward.lab_name.btn_s_plus:
            return self.nd_special_reward.lab_name.btn_s_plus
        else:
            return None

    def get_btn_diy(self):
        if self.nd_special_reward and self.nd_special_reward.lab_name and self.nd_special_reward.lab_name.btn_diy:
            return self.nd_special_reward.lab_name.btn_diy
        else:
            return None

    def get_nd_s_plus_skin_diff_appearance(self):
        if self.nd_special_reward and self.nd_special_reward.lab_role_name and self.nd_special_reward.lab_role_name.lab_info:
            return self.nd_special_reward.lab_role_name.lab_info
        else:
            return None

    def get_btn_ss(self):
        if self.hide_btn_ss:
            return None
        else:
            if self.nd_special_reward:
                lab_name = getattr(self.nd_special_reward, 'lab_name')
                if lab_name:
                    return getattr(lab_name, 'btn_ss')
            return None

    def get_btn_ss_red(self):
        btn_ss = self.get_btn_ss()
        if btn_ss:
            return getattr(btn_ss, 'temp_red')
        else:
            return None

    def get_btn_pet(self):
        if self.nd_special_reward:
            lab_name = getattr(self.nd_special_reward, 'lab_name')
            if lab_name:
                return getattr(lab_name, 'btn_pet')
        return None

    def on_click_btn_pet(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_to_pet_main
        jump_to_pet_main(self.pet_skin_no)