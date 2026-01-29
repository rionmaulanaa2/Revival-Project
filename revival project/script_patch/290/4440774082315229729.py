# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/GenericSettleWidgets.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import text_utils
from logic.gutils.settle_scene_utils import ROLE_NAME_HEIGHT_OFFSET, RANK_WIDGET_PATH, RANK_MODEL_NAME, ZOMGIEFFA_RESULT_WIDGET_PATH, PLAYER_NAME_WIDGET_PATH, ROLE_BOX_NAME, MECHA_BOX_NAME, ROLE_NAME_HEIGHT, MECHA_NAME_HEIGHT, MECHA_NAME_HEIGHT_OFFSET, get_rank_tail_icon_path
from logic.comsys.battle.Settle.SettleInteractionUI import SettleInteractionUI
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.const import PRIV_SHOW_PURPLE_ID
from logic.gcommon.cdata.privilege_data import COLOR_NAME
import world
import math3d
import cc

class SettleRankWidget(object):

    def __init__(self, parent, rank, total_num):
        self.parent = parent
        self.rank_widget = global_data.uisystem.load_template_create(RANK_WIDGET_PATH, parent=self.parent.panel)
        self.rank_widget.lab_rank.SetString(str(rank))
        self.rank_widget.img_tail.SetDisplayFrameByPath('', get_rank_tail_icon_path(rank))
        self.rank_widget.lab_all.SetString(get_text_by_id(3120).format(total_num))
        vis_img_win = True if rank <= 5 and not G_IS_NA_PROJECT else False
        self.rank_widget.img_win.setVisible(vis_img_win)
        self.rank_widget.lab_rank.ChildResizeAndPosition()
        self.rank_widget.ChildResizeAndPosition()

    def reset_position_and_show(self):
        scn = world.get_active_scene()
        rank_model = scn.get_model(RANK_MODEL_NAME)
        if rank_model and rank_model.valid:
            x, y = scn.active_camera.world_to_screen(rank_model.world_position)
            x, y = neox_pos_to_cocos(x, y)
            pos = self.parent.panel.convertToNodeSpace(cc.Vec2(x, y))
            self.rank_widget.SetPosition(pos.x, pos.y)
            self.rank_widget.setVisible(True)
            self.rank_widget.PlayAnimation('show_rank')

    def destroy(self):
        self.parent = None
        self.rank_widget = None
        return

    def set_visible(self, vis):
        self.rank_widget.setVisible(vis)


class SettleWinWidget(object):

    def __init__(self, parent, is_win, is_draw):
        self.parent = parent
        self.rank_widget = global_data.uisystem.load_template_create(ZOMGIEFFA_RESULT_WIDGET_PATH, parent=self.parent.panel)
        pic_path = 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png'
        if is_draw or is_win:
            pic_path = 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png' if 1 else 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png'
        self.rank_widget.img_title.SetDisplayFrameByPath('', pic_path)
        self.rank_widget.img_title.ChildResizeAndPosition()
        self.rank_widget.ChildResizeAndPosition()

    def reset_position_and_show(self):
        scn = world.get_active_scene()
        rank_model = scn.get_model(RANK_MODEL_NAME)
        if rank_model and rank_model.valid:
            x, y = scn.active_camera.world_to_screen(rank_model.world_position)
            x, y = neox_pos_to_cocos(x, y)
            pos = self.parent.panel.convertToNodeSpace(cc.Vec2(x, y))
            self.rank_widget.SetPosition(pos.x, pos.y)
            self.rank_widget.setVisible(True)
            self.rank_widget.PlayAnimation('show_rank')

    def destroy(self):
        self.parent = None
        self.rank_widget = None
        return

    def set_visible(self, vis):
        self.rank_widget.setVisible(vis)


class SettleNameWidget(object):

    def __init__(self, eid_list, name_str_list, uid_list=None, mvp_list=None, lose=False, mecha_id_list=None, is_ob=False, extra_info={}):
        self.name_space_nodes = list()
        self.name_widgets = list()
        self.eid_to_name_widget = dict()
        self.is_ob = is_ob
        if uid_list is None:
            uid_list = [ None for i in range(len(name_str_list)) ]
        if mvp_list is None:
            mvp_list = [ False for i in range(len(name_str_list)) ]
        self.mecha_id_list = mecha_id_list
        priv_settings_list = extra_info.get('priv_settings_list', [])
        if not priv_settings_list:
            priv_settings_list = [ {} for i in range(len(name_str_list)) ]
        for i in range(len(name_str_list)):
            self._load_name_widget(eid_list[i], name_str_list[i], uid_list[i], mvp_list[i], lose, uid_list, priv_settings_list[i])

        return

    def _load_name_widget(self, eid, name_str, uid, is_mvp, lose, uid_list, priv_settings):
        from logic.gutils.intimacy_utils import init_intimacy_icon_with_uid, init_intimacy_icon_with_uid_list
        nd_name = global_data.uisystem.load_template_create(PLAYER_NAME_WIDGET_PATH)
        nd_name.lab_name.SetString(name_str)
        if is_mvp:
            if lose:
                nd_name.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/bar_mvp_lose.png')
            nd_name.img_mvp.setVisible(True)
        space_node = CCUISpaceNode.Create()
        space_node.AddChild('', nd_name)
        nd_name.setPosition(0, 0)
        if not self.is_ob:
            if eid == global_data.player.id:
                init_intimacy_icon_with_uid_list(nd_name.temp_intimacy, uid_list)
            else:
                init_intimacy_icon_with_uid(nd_name.temp_intimacy, uid)
        self.name_widgets.append(nd_name)
        self.name_space_nodes.append(space_node)
        self.eid_to_name_widget[eid] = nd_name
        space_node.setVisible(False)
        nd_name.setVisible(False)
        self.set_privilege_state(nd_name, uid, priv_settings)

    def reset_position_and_show(self, name_on_role=True, height=None):
        display_count = len(self.name_widgets)
        scn = world.get_active_scene()
        box_name = ROLE_BOX_NAME if name_on_role else MECHA_BOX_NAME
        name_height = ROLE_NAME_HEIGHT if name_on_role else MECHA_NAME_HEIGHT
        if height is not None:
            name_height = height
        for i in range(display_count):
            m_box = scn.get_model(box_name[display_count][i])
            if not m_box:
                continue
            box_pos = math3d.vector(m_box.world_position)
            if name_on_role:
                box_pos.y += name_height + ROLE_NAME_HEIGHT_OFFSET[display_count][i]
            else:
                box_pos.y += name_height + MECHA_NAME_HEIGHT_OFFSET.get(self.mecha_id_list[i], 0.0)
            self.name_space_nodes[i].set_assigned_world_pos(box_pos)
            self.name_space_nodes[i].setVisible(True)
            self.name_widgets[i].setVisible(True)

        return

    def set_visible(self, flag):
        for name_widget in self.name_widgets:
            name_widget.setVisible(flag)

    def set_sub_widget_scale_by_eid(self, eid, scale):
        self.eid_to_name_widget[eid].setScale(scale)

    def set_privilege_state(self, nd_name, uid, priv_settings):
        if not global_data.player:
            return
        is_me = uid == global_data.player.uid
        if is_me:
            priv_data = global_data.player.get_privilege_data()
            real_priv_settings = priv_data.get('priv_settings', {})
            priv_purple_id = priv_data.get('priv_purple_id', False)
        else:
            priv_purple_id = True
            real_priv_settings = priv_settings
        if real_priv_settings.get(PRIV_SHOW_PURPLE_ID, False) and priv_purple_id:
            nd_name.lab_name.SetColor(COLOR_NAME)

    def destroy(self):
        self.name_widgets = None
        for space_node in self.name_space_nodes:
            space_node.Destroy()

        self.name_space_nodes = None
        self.eid_to_name_widget = None
        return


class SettleInputWidget(object):

    def __init__(self, parent, btn_chat, btn_send, display_count):
        if global_data.is_pc_mode:
            send_callback = self.on_edit_box_send_callback
        else:
            send_callback = None
        self.input_widget = InputBox(btn_chat, input_callback=self.on_edit_box_changed_callback, send_callback=send_callback)
        self.input_widget.set_rise_widget(parent.panel)
        self.input_widget.set_enable_pop_up_keyboard(False)

        @btn_send.unique_callback()
        def OnClick(*args):
            self.on_edit_box_send_callback()

        return

    def on_edit_box_send_callback(self):
        msg = self.input_widget.get_text()
        if not msg:
            return
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return False
        check_code, flag, msg = text_utils.check_review_words_chat(msg)
        if flag != text_utils.CHECK_WORDS_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            return
        if not global_data.player:
            return
        global_data.player.send_danmu_after_settle(msg)
        self.input_widget.set_text('')

    def on_edit_box_changed_callback(self, text):
        if text.endswith('\n') or text.endswith('\r'):
            text = text.rstrip('\n')
            text = text.rstrip('\r')
            self.input_widget.set_text(text)
            self.input_widget.detachWithIME()

    def destroy(self):
        self.input_widget = None
        return


class SettleInteractionWidget(object):

    def __init__(self, btn_emote, on_begin_cb=None, on_end_cb=None):
        self.on_begin_cb = on_begin_cb
        self.on_end_cb = on_end_cb
        self.interaction_widget = SettleInteractionUI()
        self._emote_begin_location = None
        self._selecting_emote = False
        self.up_vec2 = cc.Vec2(0, 1)
        btn_emote.BindMethod('OnBegin', self.on_begin_btn_emote)
        btn_emote.BindMethod('OnDrag', self.on_drag_btn_emote)
        btn_emote.BindMethod('OnEnd', self.on_end_btn_emote)
        return

    def on_begin_btn_emote(self, btn, touch):
        self._emote_begin_location = touch.getLocation()
        self._selecting_emote = True
        self.interaction_widget.show()
        self.on_begin_cb and callable(self.on_begin_cb) and self.on_begin_cb()
        return True

    def on_drag_btn_emote(self, btn, touch):
        if self._selecting_emote and self._emote_begin_location:
            cur_touch_pos = touch.getLocation()
            cur_touch_pos.subtract(self._emote_begin_location)
            touch_angle = cur_touch_pos.getAngle(self.up_vec2)
            if cur_touch_pos.length() > 3:
                self.interaction_widget.try_select_action(touch_angle)
        return True

    def on_end_btn_emote(self, btn, touch):
        self._emote_begin_location = None
        self._selecting_emote = False
        self.interaction_widget.try_action()
        self.interaction_widget.hide()
        self.on_end_cb and callable(self.on_end_cb) and self.on_end_cb()
        return True

    def destroy(self):
        self.interaction_widget.close()
        self.interaction_widget = None
        self.on_begin_cb = None
        self.on_end_cb = None
        return

    @property
    def selecting_emote(self):
        return self._selecting_emote