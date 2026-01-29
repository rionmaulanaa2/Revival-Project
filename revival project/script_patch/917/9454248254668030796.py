# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/MechaRegionTitleUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gutils import dress_utils
from logic.gutils import locate_utils
from logic.gutils import template_utils
import common.const.uiconst as ui_const
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_const import rank_region_const
BAR_BG = [
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_big_1.png',
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_big_2.png',
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_big_3.png',
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_big_4.png']
BAR_MASK = [
 'gui/ui_res_2/title/title_lobby_pop/pnl_title_lobby_pop_big_1.png',
 'gui/ui_res_2/title/title_lobby_pop/pnl_title_lobby_pop_big_2.png',
 'gui/ui_res_2/title/title_lobby_pop/pnl_title_lobby_pop_big_3.png',
 'gui/ui_res_2/title/title_lobby_pop/pnl_title_lobby_pop_big_4.png']
TITLE_BG = [
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_small_1.png',
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_small_2.png',
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_small_3.png',
 'gui/ui_res_2/title/title_lobby_pop/bar_title_lobby_pop_small_4.png']
LIGHT_ANIM = [
 [
  'show_orange', 'loop_orange'],
 [
  'show_purple', 'loop_purple'],
 [
  'show_blue', 'loop_blue'],
 [
  'show_green', 'loop_green']]

class MechaRegionTitleUI(BasePanel):
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = ui_const.UI_VKB_CLOSE
    PANEL_CONFIG_NAME = 'title/title_lobby_pop'
    UI_ACTION_EVENT = {'btn_back.OnClick': 'close',
       'btn_set.btn_common_big.OnClick': 'on_jump',
       'btn_share.btn_common_big.OnClick': 'on_share'
       }

    def on_init_panel(self, **kwarg):
        self._screen_capture_helper = None
        self.is_show_world_mecha = rank_const.is_world_mecha_region_rank()
        settle_title = kwarg.get('settle_title', None)
        self.title_data = locate_utils.get_rank_title_list(rank_const.RANK_TITLE_MECHA_REGION, custom_title_dict=settle_title)
        self.show_title_list()
        self.show_total_titles()
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(0.1, lambda : self.panel.PlayAnimation('loop'))
        return

    def get_rank_data_level(self, rank_data):
        title_type, region_type, mecha_type, rank_adcode, rank, rank_expire = rank_data
        if self.is_show_world_mecha:
            if region_type == rank_region_const.REGION_RANK_TYPE_COUNTRY:
                return 0
            return 1
        if region_type == rank_region_const.REGION_RANK_TYPE_COUNTRY:
            if rank <= 10:
                return 0
            else:
                return 1

        else:
            if region_type == rank_region_const.REGION_RANK_TYPE_PROVINCE:
                return 2
            if region_type == rank_region_const.REGION_RANK_TYPE_CITY:
                return 3
        return 3

    def show_title_list(self):
        from logic.gutils import mecha_skin_utils
        count = len(self.title_data)
        title_list = self.panel.temp_content
        title_list.SetInitCount(count)
        for i in range(count):
            item_widget = title_list.GetItem(i)
            rank_data = self.title_data[i]
            title_type, region_type, mecha_type, rank_adcode, rank, rank_expire = rank_data
            template_utils.init_rank_title(item_widget, title_type, rank_data[1:])
            level = self.get_rank_data_level(rank_data)
            item_widget.temp_card.img_bar.SetDisplayFrameByPath('', BAR_BG[level])
            item_widget.temp_card.img_mask.SetDisplayFrameByPath('', BAR_MASK[level])
            item_widget.temp_card.img_mask.SetDisplayFrameByPath('', BAR_MASK[level])
            item_widget.img_bg.SetDisplayFrameByPath('', TITLE_BG[level])
            item_widget.lab_rank.SetString(get_text_by_id(15087, {'rank': rank}))
            clothing_id = mecha_skin_utils.get_cur_skin_id(mecha_type)
            item_widget.temp_card.img_mech.SetDisplayFrameByPath('', mecha_skin_utils.get_mecha_pic_path(clothing_id))
            item_widget.temp_card.vx_nd_mech.vx_nd_mech02.SetMaskFrameByPath('', mecha_skin_utils.get_mecha_pic_path(clothing_id))
            conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')[str(mecha_type)]
            mecha_name = conf.get('name_mecha_text_id', '')
            item_widget.temp_card.lab_mech.SetString(mecha_name)
            item_widget.setVisible(False)

            def delay(item_widget, level):

                def cb2():
                    item_widget.PlayAnimation(LIGHT_ANIM[level][1])

                def cb1():
                    item_widget.setVisible(True)
                    item_widget.PlayAnimation(LIGHT_ANIM[level][0])
                    item_widget.temp_card.PlayAnimation('show_orange')
                    item_widget.SetTimeOut(0.5, cb2)

                return cb1

            item_widget.SetTimeOut(0.03 * i, delay(item_widget, level))

        arrow_right = self.panel.img_arrow
        arrow_left = self.panel.img_arrow2
        if count <= 4:
            arrow_right.setVisible(False)
            title_list.setBounceEnabled(False)
            offset_x = 40 - (268 * count + 15 * (count - 1)) * 0.5
            title_list.SetPosition('50%%%d' % offset_x, '50%30')
        else:
            title_list.SetPosition('50%-509', '50%30')
            title_list.setBounceEnabled(True)
            outer_size = title_list.getContentSize()
            inner_size = title_list.getInnerContainerSize()
            right_pos = outer_size.width - inner_size.width

            def OnScrolling--- This code section failed: ---

 156       0  LOAD_DEREF            0  'title_list'
           3  LOAD_ATTR             0  'inner_container'
           6  LOAD_ATTR             1  'getPosition'
           9  CALL_FUNCTION_0       0 
          12  LOAD_ATTR             2  'x'
          15  STORE_FAST            0  'cur_pos_x'

 157      18  LOAD_DEREF            1  'arrow_left'
          21  LOAD_ATTR             3  'setVisible'
          24  LOAD_ATTR             1  'getPosition'
          27  COMPARE_OP            0  '<'
          30  CALL_FUNCTION_1       1 
          33  POP_TOP          

 158      34  LOAD_DEREF            2  'arrow_right'
          37  LOAD_ATTR             3  'setVisible'
          40  LOAD_FAST             0  'cur_pos_x'
          43  LOAD_DEREF            3  'right_pos'
          46  COMPARE_OP            4  '>'
          49  CALL_FUNCTION_1       1 
          52  POP_TOP          

Parse error at or near `COMPARE_OP' instruction at offset 27

            title_list.OnScrolling = OnScrolling
            OnScrolling()
            arrow_left.setVisible(False)

    def show_total_titles(self):
        title_nums = {i:0 for i in range(4)}
        if self.is_show_world_mecha:
            title_type = [
             611309, 611308, 611308, 611308]
        else:
            title_type = [
             15088, 15089, 15090, 15091]
        for i, rank_data in enumerate(self.title_data):
            level = self.get_rank_data_level(rank_data)
            title_nums[level] += 1

        title_num_list = []
        for i, num in six.iteritems(title_nums):
            if num > 0:
                title_num_list.append([i, num])

        total_list = self.panel.temp_sum
        total_list.SetInitCount(len(title_num_list))
        for i, info in enumerate(title_num_list):
            item_widget = total_list.GetItem(i)
            index, num = info
            icon_index = 4 - index
            if self.is_show_world_mecha:
                if icon_index == 3:
                    icon_index = 5
            item_widget.img_icon.SetDisplayFrameByPath('', 'gui/ui_res_2/rank/title/icon_badge0{}.png'.format(icon_index))
            item_widget.lab_title.SetString(get_text_by_id(title_type[index], {'num': num}))

    def on_jump(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_tp_battle_flag
        from logic.comsys.role.PlayerBattleFlagWidget import TAB_TITLE
        jump_tp_battle_flag(flag_tab=TAB_TITLE)
        self.close()

    def on_share(self, *args):
        if not global_data.video_player.is_in_init_state():
            global_data.game_mgr.show_tip(get_text_by_id(82150))
            return
        if not self._screen_capture_helper:
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            from logic.comsys.share.SpringBenefitsShareCreator import SpringBenefitsShareCreator
            self._screen_capture_helper = ScreenFrameHelper()
            share_creator = SpringBenefitsShareCreator()
            share_creator.create()
            share_content = share_creator
            self._screen_capture_helper.set_custom_share_content(share_content)
        if self._screen_capture_helper:

            def custom_cb(*args):
                self.panel.btn_set.setVisible(True)
                self.panel.btn_share.setVisible(True and global_data.is_share_show)

            self.panel.btn_set.setVisible(False)
            self.panel.btn_share.setVisible(False)
            self._screen_capture_helper.take_screen_shot(['MechaRegionTitleUI'], self.panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1')