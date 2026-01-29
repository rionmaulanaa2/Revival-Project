# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/MechaTopRank.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import cc
import time
import game3d
from common.cfg import confmgr
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from logic.gcommon import const
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_const import rank_mecha_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
from logic.gutils import follow_utils
from logic.gutils import locate_utils
from logic.gutils import role_head_utils
from logic.gutils.template_utils import set_sex_node_img
from logic.gutils.lv_template_utils import init_lv_template
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
TOTAL = 10
ROTATE_FACTOR = 850

def get_top_rank_list(rank_type):
    from logic.gcommon.cdata import adcode_data
    rank_list = []
    req_adcode = locate_utils.get_rank_service_code(adcode_data.ADCODE_HEAD, rank_const.REGION_COUNTRY_RANK)
    rank_data = global_data.message_data.get_region_rank_data(rank_type, req_adcode)
    if not rank_data:
        return rank_list
    raw_rank_list = rank_data['rank_list']
    for rank_info in raw_rank_list:
        if rank_info[2][0] < rank_mecha_const.MECHA_RANK_SUPER_SCORE or len(rank_list) >= TOTAL:
            break
        rank_list.append(rank_info)

    return rank_list


class MechaTopRank(BasePanel):
    PANEL_CONFIG_NAME = 'rank/rank_nativebest'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, rank_type):
        self.rank_type = rank_type
        self._need_show_scene = False
        self.cur_rank_list = []
        self.is_show_world_mecha = rank_const.is_world_mecha_region_rank()
        self.panel.lab_title.SetString(611357 if self.is_show_world_mecha else 15071)
        self._message_data = global_data.message_data
        global_data.player.request_friend_rank_data()
        ac_list = [
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self._show_scene),
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self._on_init_panel),
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self._show_model)]
        self.panel.runAction(cc.Sequence.create(ac_list))
        widget_list = self.panel.nd_content
        widget_list.DeleteAllSubItem()
        widget_list.SetInitCount(TOTAL)
        for i in range(TOTAL):
            item_widget = widget_list.GetItem(i)
            item_widget.setVisible(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_follow_result': self.refresh_rank_list,
           'on_undo_follow_result': self.refresh_rank_list,
           'message_on_region_rank_data': self.on_region_rank_data,
           'message_on_players_detail_inf': self.on_players_detail_inf
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_init_panel(self):
        self._need_show_scene = True
        self.hide_main_ui()
        self.process_event(True)
        self.init_model_control()
        mecha_id = int(self.rank_type)
        mecha_name = confmgr.get('mecha_display', 'HangarConfig', 'Content', str(mecha_id), 'name_mecha_text_id', default='')
        self.panel.lab_mecha_name.SetString(mecha_name)
        self.panel.lab_request_rank.SetString(611358 if self.is_show_world_mecha else 15066)
        self.panel.lab_request_rank_num.SetString(str(rank_mecha_const.MECHA_RANK_SUPER_SCORE))
        self.request_region_rank_data()

    def do_show_panel(self):
        super(MechaTopRank, self).do_show_panel()
        if self._need_show_scene:
            self._show_scene()
            self._show_model()

    def _show_scene(self):
        from logic.gcommon.common_const import scene_const
        from logic.client.const import lobby_model_display_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.TOP_NATIVE_SCENE, scene_content_type=scene_const.SCENE_TOP_NATIVE)

    def _show_model(self):
        from logic.gutils import lobby_model_display_utils
        mecha_id = int(self.rank_type)
        mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
        mecha_item_no = global_data.player.get_mecha_fashion(mecha_item_id)
        if mecha_item_no <= 0:
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_id), 'default_fashion')
            default_skin_id = default_skin[0]
            mecha_item_no = default_skin_id
        decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(mecha_item_no)), [])
        color_dict = global_data.player.get_mecha_color().get(str(mecha_item_no), {})
        global_data.emgr.refresh_model_decal_data.emit(decal_list)
        global_data.emgr.refresh_model_color_data.emit(color_dict)
        mecha_model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_no, is_get_player_data=True, consider_second_model=False)
        for data in mecha_model_data:
            data['skin_id'] = mecha_item_no
            data['model_scale'] = data.get('model_scale', 1.0) * const.MECHA_SCALE * 0.4
            data['off_euler_rot'][1] = const.MECHA_ROTATION_Y
            data['decal_list'] = decal_list
            data['color_dict'] = color_dict

        global_data.emgr.change_model_display_scene_item.emit(mecha_model_data)

    def on_finalize_panel(self):
        super(MechaTopRank, self).on_finalize_panel()
        self.process_event(False)
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()

    def on_click_close_btn(self, *args):
        self.close()
        self.show_main_ui()

    def make_ui_list(self, total_count, rank_list):
        cols = 2
        rows = total_count // cols
        real_count = len(rank_list)
        ret_list = [ None for i in range(total_count) ]
        for i in range(rows):
            for j in range(cols):
                widget_index = i * cols + j
                real_index = j * rows + i
                if real_index > real_count - 1:
                    continue
                ret_list[widget_index] = rank_list[real_index]

        return ret_list

    def show_rank_list2(self):
        widget_list = self.panel.nd_content

        def anim2(item_widget):
            return lambda : item_widget.PlayAnimation('loop_me')

        def anim1(item_widget, is_me=False):

            def cb():
                item_widget.setVisible(True)
                item_widget.PlayAnimation('show')
                if is_me:
                    max_time = item_widget.GetAnimationMaxRunTime('show')
                    item_widget.SetTimeOut(max_time, anim2(item_widget))

            return cb

        rank_list = range(10)
        for i, data in enumerate(rank_list):
            item_widget = widget_list.GetItem(i)
            item_widget.SetTimeOut(i * 0.033, anim1(item_widget))

    def show_rank_list(self):
        from logic.gcommon.cdata import adcode_data
        rank_list = get_top_rank_list(self.rank_type)
        self.panel.lab_mecha_rank.setVisible(False)
        self.panel.lab_mecha_rank_num.setVisible(False)
        if rank_list:
            min_rank = rank_list[-1]
            min_score = min_rank[2][0]
            self.panel.lab_mecha_rank.setVisible(True)
            self.panel.lab_mecha_rank_num.setVisible(True)
            self.panel.lab_mecha_rank_num.SetString(str(min_score))
        rank_list = self.make_ui_list(TOTAL, rank_list)
        self.cur_rank_list = rank_list
        widget_list = self.panel.nd_content

        def anim2(item_widget):
            return lambda : item_widget.PlayAnimation('loop_me')

        def anim1(item_widget, is_me=False):

            def cb():
                item_widget.setVisible(True)
                item_widget.PlayAnimation('show')
                if is_me:
                    max_time = item_widget.GetAnimationMaxRunTime('show')
                    item_widget.SetTimeOut(max_time, anim2(item_widget))

            return cb

        for i, data in enumerate(rank_list):
            item_widget = widget_list.GetItem(i)
            if data == None:
                item_widget.setVisible(False)
                continue
            uid = data[0]
            item_widget.SetTimeOut(i * 0.033, anim1(item_widget, is_me=global_data.player.uid == uid))
            player_info = self._message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid) or {}
            name = player_info.get('char_name', '')
            item_widget.lab_player_name.SetString(name)
            if global_data.player.uid == uid:
                item_widget.lab_player_name.SetColor(14931454)
            role_head_utils.init_role_head(item_widget.temp_player_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            init_lv_template(item_widget.temp_level, player_info.get('lv', 1))
            sex = player_info.get('sex', const.AVATAR_SEX_NONE)
            set_sex_node_img(item_widget.img_gender, sex)
            addr_name = locate_utils.get_adcode_region_name(player_info.get('rank_adcode', ''))
            item_widget.lab_locate.SetString(addr_name)
            if global_data.player.uid == uid:
                item_widget.lab_locate.SetColor(13422078)
                item_widget.img_locate.SetDisplayFrameByPath('', 'gui/ui_res_2/rank/icon_nativebest_list_01.png')
            self.add_player_simple_callback(item_widget.temp_player_head, uid, item_widget.temp_player_head)
            if global_data.player.uid == uid:
                btn_playse_list = item_widget.btn_playse_list_me
                item_widget.btn_playse_list_other.setVisible(False)
            else:
                btn_playse_list = item_widget.btn_playse_list_other
                item_widget.btn_playse_list_me.setVisible(False)
            btn_playse_list.setVisible(True)

            @btn_playse_list.unique_callback()
            def OnClick(*args):
                pass

        self.refresh_rank_list()
        return

    def refresh_rank_list(self, *argv):
        if not self.cur_rank_list:
            return
        else:
            widget_list = self.panel.nd_content
            for i, data in enumerate(self.cur_rank_list):
                item_widget = widget_list.GetItem(i)
                if data == None:
                    continue
                uid = data[0]
                player_info = self._message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
                if player_info:
                    name = player_info.get('char_name', '')
                    follow_utils.refresh_rank_list_follow_status(item_widget, uid, name)

            return

    def add_player_simple_callback(self, panel, uid, pos_panel):

        @panel.unique_callback()
        def OnClick(*args):
            from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
            if global_data.player and uid == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.del_btn(BTN_TYPE_TEAM)
                ui.hide_btn_chat()
                ui.refresh_by_uid(uid)
                w, h = pos_panel.GetContentSize()
                pos = pos_panel.ConvertToWorldSpace(w + 50, h)
                ui.set_position(cc.Vec2(pos.x, pos.y), cc.Vec2(0.0, 1.0))

    def init_model_control(self):

        @self.panel.nd_clicks.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def on_region_rank_data(self, rank_type, rank_area):
        print('>>> on_region_rank_data', rank_type, rank_area, self.rank_type)
        if rank_type != self.rank_type or rank_const.REGION_COUNTRY_RANK != rank_area:
            return
        self.request_players_info()

    def on_players_detail_inf(self, *argv):
        self.show_rank_list()

    def request_region_rank_data(self):
        from logic.gcommon.cdata import adcode_data
        req_adcode = locate_utils.get_rank_service_code(adcode_data.ADCODE_HEAD, rank_const.REGION_COUNTRY_RANK)
        rank_data = self._message_data.get_region_rank_data(self.rank_type, req_adcode)
        if rank_data and time.time() - rank_data['save_time'] < rank_const.RANK_DATA_CACHE_MAX_TIME:
            self.request_players_info()
        else:
            locate_utils.request_region_rank_data(self.rank_type, rank_const.REGION_COUNTRY_RANK, adcode_data.ADCODE_HEAD)

    def request_players_info(self):
        from logic.gcommon.cdata import adcode_data
        req_adcode = locate_utils.get_rank_service_code(adcode_data.ADCODE_HEAD, rank_const.REGION_COUNTRY_RANK)
        rank_data = self._message_data.get_region_rank_data(self.rank_type, req_adcode)
        print('>>> request_players_info', rank_data)
        if not rank_data:
            return
        rank_list = rank_data['rank_list']
        count = 0
        r_uid_list = []
        for i, rank_info in enumerate(rank_list):
            uid = rank_info[0]
            if not self._message_data.has_player_inf(uid):
                r_uid_list.append(uid)
                count += 1

        if count > 0:
            global_data.player.request_players_detail_inf(r_uid_list)
        else:
            self.show_rank_list()