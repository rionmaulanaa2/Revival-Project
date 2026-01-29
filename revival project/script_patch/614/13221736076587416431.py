# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/loading/pve_loading.py
from __future__ import absolute_import
from six.moves import range
from .battle_loading import BattleLoadingWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from random import randint
from common.cfg import confmgr

class PVELoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'pve/pve_loading'
    IS_FULLSCREEN = False
    PROG_DUR = 100
    PROG_OFF = 2
    ICONS = {0: [
         'gui/ui_res_2/pve/loading/icon_pve_loading_monster_0.png',
         'gui/ui_res_2/pve/loading/icon_pve_loading_monster_2.png'],
       1: [
         'gui/ui_res_2/pve/loading/icon_pve_loading_boss_0.png',
         'gui/ui_res_2/pve/loading/icon_pve_loading_boss_2.png']
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_conf()
        super(PVELoadingWidget, self).on_init_panel(*args, **kwargs)
        self.init_level()

    def init_conf(self):
        self.tips_conf = confmgr.get('pve_loading_tips', 'Tips', 'Content', '1')
        self.level_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')

    def init_tips(self, map_id):
        self.tips_range = self.tips_conf['TextRange']
        self.extra_tips = self.tips_conf['ExtraText']
        super(PVELoadingWidget, self).init_tips(map_id)

    def get_random_tips(self):
        text_id = randint(self.tips_range[0], self.tips_range[1] + len(self.extra_tips))
        if text_id > self.tips_range[1]:
            text_id = self.extra_tips[text_id - self.tips_range[1] - 1]
        return get_text_by_id(text_id)

    def init_level(self):
        if not global_data.battle:
            return
        else:
            level = global_data.battle.get_cur_pve_level()
            if not level:
                return
            main_level, sub_level = level
            if not main_level and not sub_level:
                return
            conf = self.level_conf.get(str(main_level), None)
            if not conf:
                print (
                 conf, '\xe5\x85\xb3\xe5\x8d\xa1\xe4\xbf\xa1\xe6\x81\xaf\xe9\x94\x99\xe8\xaf\xaf\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5')
                return
            self.panel.nd_file.setVisible(global_data.enter_pve_with_archive)
            level_key = '%s-%s' % (str(main_level), str(sub_level))
            main_text = conf.get('main_text')
            sub_text = conf.get('sub_text')
            loading_pic_list = conf.get('loading_pic')
            loading_pic = loading_pic_list[randint(0, len(loading_pic_list) - 1)]
            self.panel.lab_map.SetString(get_text_by_id(main_text))
            self.panel.lab_mode.SetString(get_text_by_id(sub_text))
            self.bg_ui.img_bg.SetDisplayFrameByPath('', loading_pic, force_sync=True)
            self.panel.lab_level.SetString(level_key)
            max_level = global_data.battle.get_max_level()
            self.panel.list_icon.DeleteAllSubItem()
            self.panel.list_prog.DeleteAllSubItem()
            self.panel.list_icon.SetInitCount(max_level)
            self.panel.list_prog.SetInitCount(max_level - 1)
            for idx, ui_item in enumerate(self.panel.list_icon.GetAllItem()):
                if idx < max_level - 1:
                    if idx <= sub_level - 1:
                        ui_item.img_icon.SetDisplayFrameByPath('', self.ICONS[0][1])
                        if idx == sub_level - 1:
                            ui_item.img_icon.nd_vx.setVisible(True)
                            ui_item.PlayAnimation('icon_glows')
                        else:
                            ui_item.img_icon.nd_vx.setVisible(False)
                    else:
                        ui_item.img_icon.SetDisplayFrameByPath('', self.ICONS[0][0])
                        ui_item.img_icon.nd_vx.setVisible(False)
                elif idx == max_level - 1:
                    if idx == sub_level - 1:
                        ui_item.img_icon.SetDisplayFrameByPath('', self.ICONS[1][1])
                        ui_item.img_icon.nd_vx.setVisible(True)
                        ui_item.PlayAnimation('icon_glows')
                    else:
                        ui_item.img_icon.SetDisplayFrameByPath('', self.ICONS[1][0])
                        ui_item.img_icon.nd_vx.setVisible(False)

            for idx, ui_item in enumerate(self.panel.list_prog.GetAllItem()):
                if idx <= sub_level - 2:
                    ui_item.setVisible(True)
                else:
                    ui_item.setVisible(False)

            return

    def _show_map_mode_tips(self, map_id):
        if not map_id or map_id < 0:
            self.panel.nd_mode.setVisible(False)
            return