# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ZombieFFA/ZombieFFAEndUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.uisys.uielment.CCRichText import CCRichText
from logic.gcommon.common_utils.local_text import get_text_by_id
from cocosui import cc
from logic.gutils import dress_utils
from logic.gutils import item_utils

class ZombieFFAEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_ffa3'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch_layer.OnClick': 'on_click_next'
       }

    def on_init_panel(self, settle_dict, finish_cb=None, *args, **kwargs):
        super(ZombieFFAEndUI, self).on_init_panel(*args, **kwargs)
        self.finish_cb = finish_cb
        self.settle_dict = settle_dict
        self.begin_show()

    def on_finalize_panel(self):
        self.finish_cb = None
        super(ZombieFFAEndUI, self).on_finalize_panel()
        return

    def begin_show(self):
        result_2_anim_sound = {'win': ('win', 'bt_victory'),
           'draw': ('deuce', 'bt_draw'),
           'defeated': ('defeat', 'bt_failure')
           }
        battle_result = 'win'
        if not self.settle_dict.get('is_win', False):
            battle_result = self.settle_dict.get('is_draw', True) or 'defeated' if 1 else 'draw'
        anim, sound_name = result_2_anim_sound[battle_result]
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.show_win_info()
        self.panel.PlayAnimation('defeat_score')

    def show_win_info(self):
        if self.settle_dict.get('is_draw', False):
            self.panel.nd_win_info.setVisible(False)
            return
        winner_mecha = self.settle_dict.get('winner_mecha_ids', [])
        if not winner_mecha:
            self.panel.nd_win_info.setVisible(False)
            return
        rstr_temp = '<img="{pic_path}", scale=0.6> <color=0xffb22cff>{mecha_name}</color>'
        mecha_rstr_list = []
        for mecha_id in winner_mecha:
            head_photo = 'gui/ui_res_2/mall/{}_2.png'.format(dress_utils.battle_id_to_mecha_lobby_id(mecha_id))
            mecha_name = item_utils.get_mecha_name_by_id(mecha_id)
            mecha_rstr = rstr_temp.format(pic_path=head_photo, mecha_name=mecha_name)
            mecha_rstr_list.append(mecha_rstr)

        win_mecha_str = '  '.join(mecha_rstr_list)
        win_str = get_text_by_id(19779, args=(win_mecha_str,))
        nd_info = CCRichText.Create(win_str, 18, cc.Size(self.panel.nd_win_info.getContentSize().width, 0))
        self.panel.nd_win_info.AddChild('nd_info', nd_info)
        self.panel.nd_win_info.nd_info = nd_info
        nd_bg = self.panel.nd_win_info.nd_rt_bg
        bg_position = nd_bg.getPosition()
        nd_info.setPosition(bg_position)
        nd_info.SetHorizontalAlign(1)
        nd_info.formatText()
        line_width = nd_info.getLineWidths()[0]
        HORIZONTAL_MARGIN = 90
        nd_bg_width, nd_bg_height = nd_bg.GetContentSize()
        nd_bg_width = max(line_width + HORIZONTAL_MARGIN, nd_bg_width)
        nd_bg.SetContentSize(nd_bg_width, nd_bg_height)
        img_bg_width, img_bg_height = nd_bg.img_bg.GetContentSize()
        img_bg_width = max(line_width + HORIZONTAL_MARGIN, img_bg_width)
        nd_bg.img_bg.SetContentSize(img_bg_width, img_bg_height)
        nd_bg.ChildRecursionRePosition()
        nd_info.setVisible(False)
        nd_bg.temp_arrow_left.setVisible(False)
        nd_bg.temp_arrow_right.setVisible(False)
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('info')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('info') / 2),
         cc.CallFunc.create(lambda : nd_info.setVisible(True)),
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(lambda : nd_bg.temp_arrow_left.PlayAnimation('loop_left')),
         cc.CallFunc.create(lambda : nd_bg.temp_arrow_right.PlayAnimation('loop_right')),
         cc.CallFunc.create(lambda : nd_bg.temp_arrow_left.setVisible(True)),
         cc.CallFunc.create(lambda : nd_bg.temp_arrow_right.setVisible(True))]))
        self.panel.PlayAnimation('info')

    def on_click_next(self, *args):
        if self.finish_cb and callable(self.finish_cb):
            self.finish_cb()
        self.close()