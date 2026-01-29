# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ArmorBuffWidget.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.item import item_const
from logic.gcommon.common_const.buff_const import COMMON_BUFF
from logic.gcommon.item import item_utility as iutil
ARMOR_BUFF_PRIORITY_LIST = {item_const.DRESS_POS_MASK: 0,
   item_const.DRESS_POS_HEAD: 0,
   item_const.DRESS_POS_ARMOR: 1,
   item_const.DRESS_POS_LEG: 2
   }
QUALITY_PIC = {item_const.NORMAL_GREEN: 'gui/ui_res_2/battle/buff/defend_bar_green.png',
   item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle/buff/defend_bar_blue.png',
   item_const.EPIC_PURPLE: 'gui/ui_res_2/battle/buff/defend_bar_purple.png'
   }

class ArmorBuffWidget(object):

    def __init__(self, panel, custom_event=False):
        self.armor_dict = {}
        self.panel = panel
        self.armor_inited = False
        self.cur_cam_target_id = None
        for i in range(4):
            panel = self.panel.list_armor.GetItem(i)
            if panel:
                panel.buff_bar.setVisible(False)
                panel.quality_bar.setVisible(False)

        if not custom_event:
            self.init_event()
            self.on_camera_player_setted()
        return

    def init_event(self):
        econf = {'player_destroy_event': self.remove_all_buff,
           'player_armor_changed': self.on_armor_changed,
           'scene_camera_player_setted_event': self.on_camera_player_setted,
           'scene_player_setted_event': self.on_player_setted
           }
        emgr = global_data.emgr
        emgr.bind_events(econf)

    def destroy(self):
        self.remove_all_buff()
        self.panel = None
        self.armor_dict = {}
        return

    def on_player_setted(self, *args):
        self.cur_cam_target_id = None
        return

    def on_armor_changed(self, pos, armor):
        if pos not in six.iterkeys(ARMOR_BUFF_PRIORITY_LIST):
            return
        if not armor:
            insert_idx = self.get_armor_insert_idx(pos)
            self.del_armor(insert_idx)
            uiobj = self.panel.list_armor.GetItem(insert_idx)
            if uiobj:
                self.show_empty_armor(pos, uiobj)
            return
        uiobj = self.get_armor(pos, armor)
        self.update_armor_data(pos, armor, uiobj)

    def update_armor_data(self, pos, armor, uiobj, level_up=0):
        armor_level = armor.conf('iLevel')
        item_id = armor.conf('iID')
        from logic.gutils.template_utils import get_armor_buff_pic
        buff_pic = get_armor_buff_pic(pos, armor_level + level_up)
        if buff_pic:
            uiobj.buff_bar.SetDisplayFrameByPath('', buff_pic)
        uiobj.buff_bar.setVisible(True)
        item_conf = iutil.get_backpack_item_data(item_id)
        if not item_conf:
            return
        iQuality = QUALITY_PIC.get(item_conf['iQuality'])
        if iQuality:
            uiobj.quality_bar.SetDisplayFrameByPath('', iQuality)
            uiobj.quality_bar.setVisible(True)

    def show_empty_armor(self, pos, uiobj):
        from logic.gutils.template_utils import get_armor_empty_buff_pic
        buff_pic = get_armor_empty_buff_pic(pos)
        if buff_pic:
            uiobj.buff_bar.SetDisplayFrameByPath('', buff_pic)
        uiobj.buff_bar.setVisible(True)

    def get_armor(self, pos, armor):
        insert_idx = self.get_armor_insert_idx(pos)
        if insert_idx not in self.armor_dict:
            self.armor_dict[insert_idx] = (
             self.panel.list_armor.GetItem(insert_idx), armor)
            show_level_up_anim = self.armor_inited
        else:
            uiobj, old_armor = self.armor_dict[insert_idx]
            self.armor_dict[insert_idx] = (uiobj, armor)
            show_level_up_anim = self.armor_inited and old_armor.conf('iLevel') < armor.conf('iLevel')
        return self.armor_dict[insert_idx][0]

    def get_armor_insert_idx(self, pos):
        return ARMOR_BUFF_PRIORITY_LIST[pos]

    def del_armor(self, pos):
        if pos in self.armor_dict:
            armor_item, _ = self.armor_dict[pos]
            armor_item.buff_bar.setVisible(False)
            armor_item.quality_bar.setVisible(False)
            self.armor_dict[pos] = None
            del self.armor_dict[pos]
        return

    def remove_all_buff(self):
        all_pos = six_ex.keys(self.armor_dict)
        for pos in all_pos:
            self.del_armor(pos)

    def on_camera_player_setted(self, *args):
        if global_data.cam_lplayer is None:
            self.remove_all_buff()
        elif global_data.cam_lplayer.id != self.cur_cam_target_id:
            self.remove_all_buff()
            self.cur_cam_target_id = global_data.cam_lplayer.id
            self.update_armor_info()
            self.armor_inited = True
        return

    def update_armor_info(self):
        if not global_data.cam_lplayer:
            return
        for armor_pos in six.iterkeys(ARMOR_BUFF_PRIORITY_LIST):
            armor = global_data.cam_lplayer.ev_g_amror_by_pos(armor_pos)
            self.on_armor_changed(armor_pos, armor)