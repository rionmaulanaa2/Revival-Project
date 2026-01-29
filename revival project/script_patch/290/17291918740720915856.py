# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/rogue_utils.py
from __future__ import absolute_import
BRAND_WEAPON_DEALER = 1
BRAND_ENERGY = 2
BRAND_SPORTS = 3
from logic.gcommon.cdata import rogue_gift_config
from logic.gcommon.common_utils.local_text import get_text_by_id

def is_avatar_unit_id(unit_id):
    if global_data.player and global_data.player.logic:
        return global_data.player.logic.id == unit_id
    else:
        return False


def is_observed_unit_id(unit_id):
    if global_data.player and global_data.player.logic:
        return global_data.player.logic.ev_g_spectate_target_id() == unit_id
    else:
        return False


def get_lplayer_gifts(lplayer):
    if not lplayer:
        return []
    else:
        gs = lplayer.ev_g_cur_rogue_gifts()
        if gs is None:
            return []
        return gs
        return


def get_avatar_gifts():
    if global_data.player and global_data.player.logic:
        return get_lplayer_gifts(global_data.player.logic)
    else:
        return []


def get_gift_name_text(gift_id):
    name_id = rogue_gift_config.get_gift_name_text_id(gift_id)
    if name_id is not None:
        return get_text_by_id(name_id)
    else:
        return ''
        return


def wrap_rich_text_color(in_text, color_str):
    return '<color=0x%sff>%s</color>' % (color_str, in_text)


def get_gift_desc_text(gift_id):
    desc_id = rogue_gift_config.get_gift_desc_text_id(gift_id)
    desc_params = rogue_gift_config.get_gift_desc_params(gift_id)
    if desc_id:
        if desc_params:
            return get_text_by_id(desc_id).format(*desc_params)
        else:
            return get_text_by_id(desc_id)

    return ''


def get_gift_brand(gift_id):
    return rogue_gift_config.get_gift_brand(gift_id)


def get_gift_icon(gift_id, big=False):
    return rogue_gift_config.get_gift_icon_path(gift_id, big)


def get_gift_bg(gift_id):
    brand = get_gift_brand(gift_id)
    return 'gui/ui_res_2/battle/rogue/pnl_roguelike_%s.png' % brand


def get_gift_logo(gift_id):
    brand = get_gift_brand(gift_id)
    return 'gui/ui_res_2/battle/rogue/img_logo_%s.png' % brand


_name_color_dict = {BRAND_WEAPON_DEALER: 16740426,
   BRAND_ENERGY: 1043455,
   BRAND_SPORTS: 10221655
   }

def get_brand_name_color(gift_id):
    b = get_gift_brand(gift_id)
    return _name_color_dict.get(b, 16740426)


def get_gift_gray_icon():
    return 'gui/ui_res_2/battle/rogue/icon_sponsor_add.png'


def show_gift_pick_ui(box_id, gift_ids):
    ui = global_data.ui_mgr.show_ui('RogueGiftPickUI', 'logic.comsys.battle')
    ui.set_data(box_id, gift_ids)


def close_gift_pick_ui(box_id):
    global_data.ui_mgr.close_ui('RogueGiftPickUI')


def get_rogue_quality_bg(gift_id):
    return rogue_gift_config.get_gift_quality_bg(gift_id)