# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/RecordOpenBoxWidgetNew.py
import six
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.cdata.luck_score_config import NORMAL_LUCK_SCORE_EDGE, MIN_LUCK_SCORE_PERCENT, LOTTERY_COUNT_SHOW_BAODI
from logic.gutils.item_utils import check_skin_tag, get_lobby_item_name, get_lobby_item_type, get_lobby_item_pic_by_item_no, get_item_rare_degree, get_lobby_item_belong_no, REWARD_RARE_COLOR
from logic.gcommon.item.lobby_item_type import L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN
from logic.gcommon.item.item_const import SKATE_LOBBY_ITEM_NO, TRANSFORM_LOBBY_ITEM_NO, AIRCRAFT_SKIN_TYPE, RARE_DEGREE_5, RARE_DEGREE_6, RARE_DEGREE_7
from logic.gutils.template_utils import init_tempate_mall_i_simple_item
import cc
TOTAL_COUNT = 10
TWO_LIST_ITEM_COUNT = 5
BAR_PIC_PATH = 'gui/ui_res_2/lottery/pnl_lottery_lucky_{}.png'
BAR_NAME_PIC_PATH = 'gui/ui_res_2/lottery/bar_lottery_lucky_{}.png'
SHOW_CHIPS_TYPE_NONE = 0
SHOW_CHIPS_TYPE_NORMAL = 1
SHOW_CHIPS_TYPE_ANIM = 2

class RecordOpenBoxWidgetNew(object):

    def __init__(self, panel):
        self.panel = panel
        self._total_count = 0
        self._has_smash_item = False
        self._need_show_anim = False
        self.hide()
        self._init_item_widget_list()
        self.process_event(True)

    def show(self):
        self.panel.setVisible(True)

    def hide(self):
        self.panel.setVisible(False)

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'on_show_record_open_box_widget_event': self.update_ui
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_item_widget_list(self):
        self._item_widget_list = []
        self._item_list_list = []
        self._once_item_list = None
        self._once_item_widget = None
        if getattr(self.panel, 'list_box'):
            self._need_show_anim = False
            list_box = self.panel.list_box
            list_box.DeleteAllSubItem()
            list_box2 = self.panel.list_box2
            list_box2.DeleteAllSubItem()
            self._item_list_list = [list_box, list_box2]
            for i in range(TOTAL_COUNT):
                if list_box2 and i >= TWO_LIST_ITEM_COUNT:
                    item = list_box2.AddTemplateItem()
                else:
                    item = list_box.AddTemplateItem()
                self._item_widget_list.append(item)

        else:
            self._need_show_anim = True
            list_box_once = self.panel.list_box_once
            list_box_once.DeleteAllSubItem()
            self._once_item_list = list_box_once
            self._once_item_widget = list_box_once.AddTemplateItem()
            self._item_list_list = []
            for i in range(TOTAL_COUNT):
                list_box_more = getattr(self.panel, 'list_box_more{}'.format(i + 1))
                list_box_more.DeleteAllSubItem()
                list_box_more.setVisible(False)
                self._item_list_list.append(list_box_more)
                item = list_box_more.AddTemplateItem()
                self._item_widget_list.append(item)

        return

    def update_ui(self, reward_list=None, chips_data=None, extra_info=None, show_chips_type=SHOW_CHIPS_TYPE_NONE):
        if not reward_list:
            return
        self.show()
        self._reward_list = reward_list
        self._total_count = len(reward_list)
        self._chips_data = chips_data
        self._extra_info = extra_info
        self._show_chips_type = show_chips_type
        if self._total_count > TOTAL_COUNT:
            self._total_count = TOTAL_COUNT
            self._reward_list = self._reward_list[:TOTAL_COUNT]
        self._update_reward_item()
        self._update_luck_score_widget()
        if self._has_smash_item:
            global_data.sound_mgr.play_ui_sound('ui_switch_card')

    def _update_reward_item(self):
        if self._total_count == SINGLE_LOTTERY_COUNT:
            for item in self._item_widget_list:
                item.setVisible(False)

            for item_list in self._item_list_list:
                item_list.setVisible(False)

            self._once_item_widget and self._once_item_widget.setVisible(True)
            self._once_item_list and self._once_item_list.setVisible(True)
            self._update_once_item()
            self.panel.HasAnimation('show') and self.panel.StopAnimation('show')
            self.panel.HasAnimation('loop') and self.panel.StopAnimation('loop')
            self.panel.HasAnimation('show_once') and self.panel.PlayAnimation('show_once')
        elif self._total_count == CONTINUAL_LOTTERY_COUNT:
            for item in self._item_widget_list:
                item.setVisible(True)

            for item_list in self._item_list_list:
                item_list.setVisible(True)

            self._once_item_widget and self._once_item_widget.setVisible(False)
            self._once_item_list and self._once_item_list.setVisible(False)
            self._update_item_list()
            self.panel.HasAnimation('show_once') and self.panel.StopAnimation('show_once')
            self.panel.HasAnimation('show') and self.panel.PlayAnimation('show')
            self.panel.HasAnimation('loop') and self.panel.PlayAnimation('loop')

    def _update_once_item(self):
        reward_info = self._reward_list[0]
        chips_info = self._chips_data.get(0)
        self._init_item(self._once_item_widget, reward_info, chips_info)

    def _update_item_list(self):
        for i in range(self._total_count):
            reward_info = self._reward_list[i]
            chips_info = self._chips_data.get(i)
            if not reward_info:
                continue
            item = self._item_widget_list[i]
            self._init_item(item, reward_info, chips_info)

    def _init_item(self, item, reward_info, chips_info):
        item_no, item_count = reward_info
        bar = item.bar
        rare_degree = get_item_rare_degree(item_no, ignore_imporve=True)
        color = REWARD_RARE_COLOR.get(rare_degree, 'orange')
        bar.SetDisplayFrameByPath('', BAR_PIC_PATH.format(color))
        bar.bar_name.SetDisplayFrameByPath('', BAR_NAME_PIC_PATH.format(color))
        img_item = bar.nd_cut.img_item
        img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))
        item_type = get_lobby_item_type(item_no)
        if item_type == L_ITME_TYPE_GUNSKIN or item_type == L_ITEM_YTPE_VEHICLE_SKIN:
            belong_item_no = str(get_lobby_item_belong_no(item_no))
            if belong_item_no == TRANSFORM_LOBBY_ITEM_NO or belong_item_no == AIRCRAFT_SKIN_TYPE:
                img_item.setScale(0.84)
                img_item.setRotation(0)
            else:
                img_item.setScale(0.84)
                img_item.setRotation(54)
        else:
            img_item.setScale(0.46)
            img_item.setRotation(0)
        lab_num = item.lab_num
        lab_num.setVisible(True)
        lab_num.setString(str(item_count))
        bar.bar_name.lab_name.setString(get_lobby_item_name(item_no))
        check_skin_tag(bar.nd_kind, item_no, ignore_improve=True)
        item.StopAnimation('show_blue')
        item.StopAnimation('show_red')
        item.StopAnimation('loop_blue')
        item.StopAnimation('loop_red')
        item.vx_bar_tx_ls.setVisible(False)
        item.vx_bar2_tx_hs.setVisible(False)
        item.spr_lan.setVisible(False)
        item.spr_hong.setVisible(False)
        if self._need_show_anim:
            if rare_degree == RARE_DEGREE_5 or rare_degree == RARE_DEGREE_7:
                item.PlayAnimation('loop_blue')
                item.PlayAnimation('show_blue')
                item.vx_bar_tx_ls.setVisible(True)
                item.spr_lan.setVisible(True)
            elif rare_degree == RARE_DEGREE_6:
                item.PlayAnimation('loop_red')
                item.PlayAnimation('show_red')
                item.vx_bar2_tx_hs.setVisible(True)
                item.spr_hong.setVisible(True)
        nd_smash_item = bar.nd_smash_item
        if chips_info and self._show_chips_type:
            nd_smash_item.setVisible(True)
            nd_smash_item.setScale(1)
            chips_item_no, chips_item_count = chips_info
            init_tempate_mall_i_simple_item(nd_smash_item, chips_item_no, chips_item_count)
            if self._show_chips_type == SHOW_CHIPS_TYPE_ANIM:
                action_list = [cc.DelayTime.create(0.7),
                 cc.CallFunc.create(lambda : item.PlayAnimation('smash_scale'))]
                item.runAction(cc.Sequence.create(action_list))
                self._has_smash_item = True
        else:
            nd_smash_item.setVisible(False)

    def _update_luck_score_widget(self):
        bar_value = self.panel.nd_tips.bar_value
        luck_score = self._extra_info.get('luck_score')
        if self._total_count != CONTINUAL_LOTTERY_COUNT or not luck_score:
            bar_value.setVisible(False)
            return
        luck_score = int(luck_score)
        bar_value.setVisible(True)
        lab_lucky = bar_value.lab_lucky
        lab_lucky.setVisible(True)
        lab_value_lucky = lab_lucky.nd_auto_fit.lab_value_lucky
        lab_value_lucky.setString(str(luck_score))
        lab_value_lucky.SetColor(16772438 if luck_score >= NORMAL_LUCK_SCORE_EDGE else 4650239)
        lab_value_lucky.setVisible(True)
        lab_tips_lottery = bar_value.lab_tips_lottery
        luck_intervene_weight_list = self._extra_info.get('luck_intervene_weight')
        luck_exceed_percent = self._extra_info.get('luck_exceed_percent')
        if luck_intervene_weight_list:
            value = next(iter(luck_intervene_weight_list.values()))
            if value <= LOTTERY_COUNT_SHOW_BAODI:
                lab_tips_lottery.setString(get_text_by_id(634637).format(value))
                lab_tips_lottery.setVisible(True)
            elif value > LOTTERY_COUNT_SHOW_BAODI or luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
                lab_tips_lottery.setString(get_text_by_id(634753).format(luck_exceed_percent))
                lab_tips_lottery.setVisible(True)
            else:
                lab_tips_lottery.setVisible(False)
        elif luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
            lab_tips_lottery.setString(get_text_by_id(634753).format(luck_exceed_percent))
            lab_tips_lottery.setVisible(True)
        else:
            lab_tips_lottery.setVisible(False)

    def destroy(self):
        self.process_event(False)