# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoRank.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from logic.comsys.common_ui import CommonInfoUtils
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
import cc

class BattleInfoRank(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_tips_main'
    UI_TYPE = UI_TYPE_MESSAGE

    @execute_by_mode(False, (game_mode_const.GAME_MODE_EXERCISE,))
    def process_one_message(self, message, finish_cb):
        msg_dict = message[0]
        show_num = msg_dict.get('show_num')
        i_type = msg_dict.get('i_type')
        if show_num not in (10, 20, 50):
            finish_cb()
            return
        else:
            panel_var_name = self.get_panel_var_name()
            cur_panel = self._panel_map.get(panel_var_name, None)
            if cur_panel and cur_panel.isValid():
                CommonInfoUtils.destroy_ui(cur_panel)
            self.set_panel_map(panel_var_name, None)
            cur_panel = CommonInfoUtils.create_ui(i_type, self.panel.nd_tips)
            self.set_panel_map(panel_var_name, cur_panel)
            if not cur_panel:
                finish_cb()
                return
            pic_folder = 'gui/ui_res_2/battle/battle_tips/battle_rank_tips/'
            cur_panel.vx_xuying_da.SetDisplayFrameByPath('', '%simg_battle_ranking%d_pnl04.png' % (pic_folder, show_num))
            cur_panel.vx_xuying_xiao.SetDisplayFrameByPath('', '%simg_battle_ranking%d_pnl05.png' % (pic_folder, show_num))
            cur_panel.glow.SetDisplayFrameByPath('', '%simg_battle_ranking%d_pnl02.png' % (pic_folder, show_num))
            cur_panel.icon.SetDisplayFrameByPath('', '%simg_battle_ranking%d_02.png' % (pic_folder, show_num))
            img_num_pic = '%simg_battle_ranking%d_text03.png' % (pic_folder, show_num)
            cur_panel.img_num.SetDisplayFrameByPath('', img_num_pic)
            cur_panel.vx_img_num.SetDisplayFrameByPath('', img_num_pic)

            def finish_cd_wrapper(panel_var_name=panel_var_name):
                cur_panel = self._panel_map.get(panel_var_name, None)
                if cur_panel and cur_panel.isValid():
                    CommonInfoUtils.destroy_ui(cur_panel)
                self.set_panel_map(panel_var_name, None)
                finish_cb()
                return

            ani_idx = 1
            if show_num > 10:
                ani_idx += 1
                if show_num > 20:
                    ani_idx += 1
            ani_idx = str(ani_idx)
            kwargs = {'in_ani': 'show_0' + ani_idx,
               'out_ani': 'disappear_0' + ani_idx
               }
            self.message_ani(finish_cd_wrapper, cur_panel, **kwargs)
            is_binding = CommonInfoUtils.VISIBLE_SPECIAL_SETTING.get(i_type, True)
            if is_binding:
                self.check_visible('BattleInfoMessageVisibleUI')
            else:
                self.remove_visible('BattleInfoMessageVisibleUI')
            if show_num is not None:
                if show_num <= 10:
                    global_data.emgr.play_virtual_anchor_voice.emit('vo2_3')
                else:
                    global_data.emgr.play_virtual_anchor_voice.emit('vo2_2')
            return