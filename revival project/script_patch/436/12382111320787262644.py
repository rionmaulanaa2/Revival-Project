# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEPassDetailInfoUIBase.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from common.const.uiconst import UI_VKB_CLOSE
from logic.gcommon.common_const.pve_const import DIFFICUTY_LIST, DIFFICULTY_TEXT_LIST
from logic.gcommon.time_utility import get_readable_time
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.comsys.battle.pve.PVEItemWidget import PVEBreakWidget, PVEBlessWidget
import cc
import six_ex
import time
from logic.gutils.pve_utils import get_bless_elem_res, DEFAULT_BLESS_BAR
from logic.gcommon.common_const.pve_const import PVE_RANK_SPEED_PERSONAL, PVE_RANK_MECHA
from logic.gcommon.common_const.rank_const import NOT_FRESH, MONTH_REFRESH
from logic.gcommon.common_const.pve_const import EMPTY_WIDGET_PATH
from logic.gutils.template_utils import set_ui_show_picture
PVE_DETAIL_PROP_ICON_PATH = 'gui/ui_res_2/pve/mecha/icon_pve_mecha_info_{}.png'

class PVEPassDetailInfoUIBase(BasePanel):
    PANEL_CONFIG_NAME = 'pve/rank/pve_rank_info'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def __init__(self):
        super(PVEPassDetailInfoUIBase, self).__init__()
        self.init_params()

    def on_init_panel(self, *args):
        super(PVEPassDetailInfoUIBase, self).on_init_panel(*args)
        self.init_params()
        self.init_widget()

    def on_finalize_panel(self):
        self.break_widget and self.break_widget.destroy()
        self.bless_widget and self.bless_widget.destroy()
        self.clear_async_action()
        super(PVEPassDetailInfoUIBase, self).on_finalize_panel()

    def init_params(self):
        self._async_action = None
        self.bless_data = {}
        self.bless_keys = []
        self.mecha_id = None
        self._mecha_info_conf = confmgr.get('mecha_init_data', default={})
        self.bless_conf = confmgr.get('bless_data', default=None)
        self.break_data = {}
        self.break_conf = confmgr.get('mecha_breakthrough_data', default=None)
        return

    def init_widget(self):
        self.empty_widget = global_data.uisystem.load_template_create(EMPTY_WIDGET_PATH, self.panel)

        @self.empty_widget.nd_empty.unique_callback()
        def OnClick(*args):
            self.on_click_empty(*args)

        self.empty_widget.nd_empty.set_sound_enable(False)
        self.break_widget = PVEBreakWidget(self.panel, False)
        self.break_widget.setVisible(False)
        self.bless_widget = PVEBlessWidget(self.panel, False)
        self.bless_widget.setVisible(False)
        self.init_btn_share()

    def on_click_empty(self, *args):
        self.break_widget and self.break_widget.setVisible(False)
        self.bless_widget and self.bless_widget.setVisible(False)

    def show_player_info(self, uid, rank_page_key, rank_key, rank, pass_info, player_info):
        from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
        level_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        data_obj = PVERankDataObj(rank_key)
        chapter = data_obj.get_chapter()
        difficulty = data_obj.get_difficulty()
        player_cnt = data_obj.get_player_cnt()
        self.pass_info = pass_info
        self.mecha_id = pass_info.get('mecha_id', None)
        pve_mecha_lv = pass_info.get('choosed_mecha_level', 1)
        self.mecha_conf = self._mecha_info_conf.get(str(self.mecha_id))
        self.panel.lab_time.SetString(get_readable_time(pass_info.get('clear_time', 0)))
        self.update_rank_num(rank)
        conf = level_conf.get(str(chapter), {})
        chapter_text = get_text_by_id(conf.get('title_text'))
        place_text = get_text_by_id(conf.get('sub_title_text'))
        self.panel.lab_chapter.setString('{}:{}'.format(chapter_text, place_text))
        self.show_player_name(player_info.get('char_name', ''))
        self.panel.lab_num_people.SetString(get_text_by_id(481).format(player_cnt))
        self.panel.lab_difficulty.SetString(get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
        self.panel.lab_name_mecha.SetString(get_mecha_name_by_id(self.mecha_id))
        self.panel.lab_mecha_level.SetString('Lv{}'.format(pve_mecha_lv))
        mecha_skin_id = player_info.get('mecha_skin_id', 0)
        self.update_mecha_pic(self.mecha_id, mecha_skin_id)
        self.init_mecha_prop()
        self.break_data = pass_info.get('chossed_breakthrough', {})
        self.update_break_info()
        self.bless_data = pass_info.get('choosed_blesses', {})
        self.bless_keys = list(self.bless_data.keys())
        self.bless_keys.sort()
        self.update_bless_info()
        return

    def show_player_name(self, name):
        self.panel.lab_name.SetString(name)

    def update_rank_num(self, rank):
        text = ''
        if rank > 0:
            text = get_text_by_id(635394, (rank,))
        else:
            text = get_text_by_id(635395)
        self.panel.lab_rank.SetString(text)

    def update_rank_type_title(self, rank_page_type, rank_type):
        text = ''
        if rank_page_type == PVE_RANK_SPEED_PERSONAL:
            refresh_type = ''
            if rank_type == MONTH_REFRESH:
                refresh_type = get_text_by_id(635372)
            elif rank_type == NOT_FRESH:
                refresh_type = get_text_by_id(635371)
            text = get_text_by_id(635392, {'refresh_type': refresh_type})
        elif rank_page_type == PVE_RANK_MECHA:
            text = get_text_by_id(635393)
        self.panel.lab_type_title.SetString(text)

    def update_mecha_pic(self, mecha_id, mecha_skin_id):
        from logic.gutils import dress_utils
        lobby_select_id = dress_utils.battle_id_to_mecha_lobby_id(mecha_id)
        default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(lobby_select_id), 'default_fashion')
        lobby_item_id = mecha_skin_id if mecha_skin_id else default_skin[0]
        set_ui_show_picture(lobby_item_id, None, self.panel.temp_pic)
        return

    def init_mecha_prop(self):
        self.init_priority_list_widget()
        self._update_mecha_basic_prop()
        self._update_top_prop_info()

    def init_priority_list_widget(self):
        self.normal_priority_list = None
        return

    def _update_mecha_basic_prop(self):
        if not self.normal_priority_list:
            return
        from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVEMechaInfoWidget import NORMAL_PRIORITY_INFO
        list_info = self.normal_priority_list
        list_info.DeleteAllSubItem()
        for priority_name, info in six_ex.items(NORMAL_PRIORITY_INFO):
            item = list_info.AddTemplateItem()
            item.lab_title.setString(get_text_by_id(info.get('title')))
            item.icon.SetDisplayFrameByPath('', PVE_DETAIL_PROP_ICON_PATH.format(info.get('icon')))
            lab_data = item.lab_data
            init_num = self.mecha_conf.get(priority_name)
            is_percent = info.get('is_percent')
            if is_percent:
                lab_data.SetString('{}%'.format(int(init_num * 100)))
            elif info.get('is_decimals'):
                lab_data.SetString('%.1f' % init_num)
            else:
                lab_data.SetString(str(int(init_num)))

    def _update_top_prop_info(self):
        pass

    def update_bless_info(self):
        ui_list = self.panel.list_energy
        ui_list.RecycleAllItem()
        self._create_idx = 0
        self._async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.create_bless_item)])))

    def clear_async_action(self):
        self._create_idx = 0
        if self._async_action is not None:
            self.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def create_bless_item(self):
        start_time = time.time()
        while self._create_idx < len(self.bless_keys):
            bless_id = self.bless_keys[self._create_idx]
            bless_conf = self.bless_conf.get(str(bless_id))
            if not bless_conf:
                self._create_idx += 1
                continue
            bless_item = self.panel.list_energy.ReuseItem(bRefresh=True)
            if not bless_item:
                bless_item = self.panel.list_energy.AddTemplateItem(bRefresh=True)
            bless_item.lab_name.SetString(get_text_by_id(bless_conf['name_id']))
            bless_item.img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
            cur_level = self.bless_data.get(bless_id, 1)
            max_level = bless_conf.get('max_level', 1)
            if max_level == 1:
                bless_item.lab_level.setVisible(False)
                bless_item.icon.setVisible(True)
            else:
                bless_item.lab_level.setVisible(True)
                bless_item.icon.setVisible(False)
                bless_item.lab_level.SetString(str(cur_level))
            elem_id = bless_conf.get('elem_id', None)
            if elem_id:
                elem_icon, elem_pnl = get_bless_elem_res(elem_id, ['icon', 'bar'])
                bless_item.icon.SetDisplayFrameByPath('', elem_icon)
                bless_item.bar.SetDisplayFrameByPath('', elem_pnl)
            else:
                bless_item.bar.SetDisplayFrameByPath('', DEFAULT_BLESS_BAR)

            @bless_item.btn_energy.unique_callback()
            def OnClick(_layer, _touch, _bless_id=bless_id, cur_level=cur_level):
                print 'bless click'
                if not self.bless_widget:
                    return
                if self.break_widget.isVisible():
                    self.break_widget.setVisible(False)
                self.bless_widget.setVisible(True)
                self.bless_widget.update_widget(_bless_id, cur_level, {}, 0)

            self._create_idx += 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        return

    def update_break_info(self):
        break_conf = self.break_conf.get(str(self.mecha_id), None)
        ui_list = self.panel.list_breakthrough
        ui_list.DeleteAllSubItem()
        ui_list.SetInitCount(len(break_conf))
        break_data = self.break_data
        break_slot_list = list(break_data.keys())
        for idx, ui_item in enumerate(ui_list.GetAllItem()):
            if idx < len(break_data):
                ui_item.nd_skill.setVisible(True)
                ui_item.nd_empty.setVisible(False)
                slot = break_slot_list[idx]
                level = break_data[slot]
                slot_conf = break_conf[str(slot)]
                conf = slot_conf[str(level)]
                ui_item.img_item.SetDisplayFrameByPath('', conf['icon'])
                ui_item.lab_name_skill.SetString(get_text_by_id(conf['name_id']))
                for i, btn in enumerate(ui_item.list_dot.GetAllItem()):
                    if i < level:
                        btn.SetSelect(True)
                    else:
                        break

                @ui_item.bar.unique_callback()
                def OnClick(_layer, _touch, _slot=slot, _level=level):
                    print 'break click'
                    if not self.break_widget:
                        return
                    if self.bless_widget.isVisible():
                        self.bless_widget.setVisible(False)
                    self.break_widget.setVisible(True)
                    self.break_widget.update_widget(self.mecha_id, _slot, _level, [])

            else:
                ui_item.nd_skill.setVisible(False)
                ui_item.nd_empty.setVisible(True)

        return

    def init_btn_share(self):
        pass