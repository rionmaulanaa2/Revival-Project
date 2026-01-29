# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/mecha_module_utils.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const.mecha_const import MODULE_ATTACK_SLOT, MODULE_DEFEND_SLOT, MODULE_MOVE_SLOT, SP_MODULE_SLOT, SP_MODULE_NO_CHOOSE_ITEM_IDS
from logic.gcommon.item import item_const
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import re
from common.cfg import confmgr

def get_module_item_bar_pic(show_slot, card_level, prefix):
    if show_slot == SP_MODULE_SLOT:
        if card_level:
            return 'gui/ui_res_2/battle/mech_module/%sbar_module_sp_gold.png' % prefix
        else:
            return 'gui/ui_res_2/battle/mech_module/%sbar_module_sp_empty.png' % prefix

    else:
        bar_pic = {MODULE_ATTACK_SLOT: 'gui/ui_res_2/battle/mech_module/%sbar_module_atk_%s.png',
           MODULE_DEFEND_SLOT: 'gui/ui_res_2/battle/mech_module/%sbar_module_def_%s.png',
           MODULE_MOVE_SLOT: 'gui/ui_res_2/battle/mech_module/%sbar_module_spd_%s.png'
           }
        postfix = str(card_level) if card_level else 'empty'
        return bar_pic.get(show_slot, bar_pic[MODULE_ATTACK_SLOT]) % (prefix, postfix)


def get_proficiency_level_by_card_id(card_id):
    item_no = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content', str(card_id), 'item_no', default=None)
    if not item_no:
        return
    else:
        proficiency_level = item_utils.get_proficiency_level_by_itemno(item_no)
        return proficiency_level


def init_module_temp_item(ui_temp_item, show_slot, card_id, card_level, prefix=''):
    ui_temp_item.bar_item.SetDisplayFrameByPath('', get_module_item_bar_pic(show_slot, card_level, prefix))
    from logic.gutils import template_utils
    mecha_talent_path = template_utils.get_module_show_slot_pic(show_slot, card_id, card_level)
    ui_temp_item.img_skill.SetDisplayFrameByPath('', mecha_talent_path)


def is_default_module(module_lobby_item_no):
    lobby_mecha_conf = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', default={})
    if not lobby_mecha_conf:
        return False
    else:
        for mecha_lobby_item_id_str, conf in six.iteritems(lobby_mecha_conf):
            default_module_item_nos = conf.get('default_module', None)
            if not default_module_item_nos:
                continue
            for item_no in default_module_item_nos:
                if item_no == module_lobby_item_no:
                    return True

        return False


def get_module_card_slot(card_id):
    TALENT_PATH_PREFIX = 'gui/ui_res_2/battle/mech_module/module_%s.png'
    from common.cfg import confmgr
    cards_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
    from logic.gcommon.common_const import mecha_const
    return cards_conf.get(str(card_id), {}).get('slot', mecha_const.MODULE_ATTACK_SLOT)


def get_module_card_name_and_desc(card_id, level=None, try_brief_desc=False):
    cards_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
    card_conf = cards_conf.get(str(card_id))
    card_name = get_text_by_id(card_conf.get('type_text_id', None))
    if try_brief_desc:
        desc_text_id = card_conf.get('brief_desc_text_id', None)
    else:
        desc_text_id = None
    if desc_text_id is None:
        brief_mode = False
        desc_text_id = card_conf.get('desc_text_id', None)
    else:
        brief_mode = True
    text = get_text_by_id(desc_text_id)
    if not text:
        return (card_name, text)
    else:
        if not brief_mode:
            desc_text_params = card_conf.get('desc_text_params', {})
        else:
            desc_text_params = card_conf.get('brief_desc_text_params', {})
        if not desc_text_params:
            return (card_name, text)
        using_params = []
        for param_text in desc_text_params:
            if type(param_text) is str:
                using_params.append(param_text)
            elif type(param_text) is int:
                using_params.append(get_text_by_id(param_text))
            elif type(param_text) is dict:
                level_text_dict = {}
                for k, v in six.iteritems(param_text):
                    if type(v) is int:
                        level_text_dict[k] = get_text_by_id(v) if 1 else v

                if level:
                    text_to_show = level_text_dict.get(str(level), '')
                else:
                    text_to_show = '/'.join(six.itervalues(level_text_dict))
                using_params.append(text_to_show)

        card_effect_desc = get_text_by_id(desc_text_id).format(*using_params)
        return (
         card_name, card_effect_desc)


SLOT_TO_MODULE_TYPE_NAME_ID = {1: 18197,
   2: 18198,
   3: 18199,
   4: 18200
   }

def get_module_type_name_by_slot(slot_no):
    if slot_no in SLOT_TO_MODULE_TYPE_NAME_ID:
        return get_text_by_id(SLOT_TO_MODULE_TYPE_NAME_ID[slot_no])
    else:
        return ''