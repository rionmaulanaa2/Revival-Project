# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVERightTipsWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_item_name
from common.cfg import confmgr
from logic.gutils.screen_effect_utils import create_screen_effect_directly
EFFECT_PATH = 'effect/fx/pingmu/acetime_pm_{}.sfx'
SHOW_ANIM = 'show_{}'
HIDE_ANIM = 'hide_{}'
STORY_DEBRIS_ICON_PATH = 'gui/ui_res_2/item/9301.png'
MECHA_DEBRIS_ICON_PATH = 'gui/ui_res_2/item/{}.png'

class PVERightTipsWidget(object):
    TEMPLATE = 'battle_tips/pve/i_pve_tips_get_item'
    DUR = 3
    INVERVAL = 0.5

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.process_events(True)

    def init_params(self):
        self.widget = None
        self._break_sfx_id = None
        self._bless_sfx_id = None
        self._item_sfx_id = None
        self._anim_list = []
        self._is_animing = False
        self.bless_conf = confmgr.get('bless_data', default=None)
        self.item_conf = confmgr.get('pve_shop_data', default=None)
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)

    def process_events(self, is_bind):
        econf = {'pve_get_story_debris': self.show_story_debris_tip,
           'pve_get_mecha_debris': self.show_mecha_debris_tip,
           'pve_update_break_event': self.show_break_tip,
           'pve_update_bless_event': self.show_energy_tip,
           'pve_update_item_set': self.show_item_tip
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        self.clear_break_sfx()
        self.clear_bless_sfx()
        self.clear_item_sfx()
        self.widget and self.widget.Destroy()
        self.widget = None
        self._anim_list = []
        self._is_animing = False
        return

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def show_tip_anim(self, color, text, icon_path, need_append=True):
        if need_append:
            self._anim_list.append((color, text, icon_path))
        if self._is_animing:
            return

        def show_delay_call--- This code section failed: ---

  78       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'widget'
           6  POP_JUMP_IF_FALSE   142  'to 142'
           9  LOAD_DEREF            0  'self'
          12  LOAD_ATTR             0  'widget'
          15  LOAD_ATTR             1  'isValid'
          18  CALL_FUNCTION_0       0 
        21_0  COME_FROM                '6'
          21  POP_JUMP_IF_FALSE   142  'to 142'

  79      24  LOAD_DEREF            0  'self'
          27  LOAD_ATTR             2  '_anim_list'
          30  LOAD_ATTR             3  'pop'
          33  LOAD_CONST            1  ''
          36  CALL_FUNCTION_1       1 
          39  STORE_FAST            0  'anim_data'

  80      42  LOAD_GLOBAL           4  'HIDE_ANIM'
          45  LOAD_ATTR             5  'format'
          48  LOAD_ATTR             1  'isValid'
          51  BINARY_SUBSCR    
          52  CALL_FUNCTION_1       1 
          55  STORE_FAST            1  'hide_anim_name'

  81      58  LOAD_GLOBAL           6  'float'
          61  LOAD_DEREF            0  'self'
          64  LOAD_ATTR             0  'widget'
          67  LOAD_ATTR             7  'GetAnimationMaxRunTime'
          70  LOAD_FAST             1  'hide_anim_name'
          73  CALL_FUNCTION_1       1 
          76  CALL_FUNCTION_1       1 
          79  LOAD_DEREF            0  'self'
          82  LOAD_ATTR             8  'INVERVAL'
          85  BINARY_ADD       
          86  STORE_FAST            2  'hide_anim_time'

  82      89  LOAD_DEREF            0  'self'
          92  LOAD_ATTR             0  'widget'
          95  LOAD_ATTR             9  'PlayAnimation'
          98  LOAD_FAST             1  'hide_anim_name'
         101  CALL_FUNCTION_1       1 
         104  POP_TOP          

  84     105  LOAD_CLOSURE          0  'self'
         111  LOAD_CONST               '<code_object hide_delay_call>'
         114  MAKE_CLOSURE_0        0 
         117  STORE_FAST            3  'hide_delay_call'

  90     120  LOAD_DEREF            0  'self'
         123  LOAD_ATTR             0  'widget'
         126  LOAD_ATTR            10  'DelayCall'
         129  LOAD_FAST             2  'hide_anim_time'
         132  LOAD_FAST             3  'hide_delay_call'
         135  CALL_FUNCTION_2       2 
         138  POP_TOP          
         139  JUMP_FORWARD          0  'to 142'
       142_0  COME_FROM                '139'

Parse error at or near `BINARY_SUBSCR' instruction at offset 51

        if self.widget and self.widget.isValid():
            show_anim_name = SHOW_ANIM.format(color)
            show_anim_time = float(self.widget.GetAnimationMaxRunTime(show_anim_name)) + self.DUR
            self._is_animing = True
            self.widget.lab_1.SetString(text)
            self.widget.icon.SetDisplayFrameByPath('', icon_path)
            self.widget.setVisible(True)
            self.widget.PlayAnimation(show_anim_name)
            self.widget.DelayCall(show_anim_time, show_delay_call)

    def show_story_debris_tip(self):
        color = 'green'
        text = get_text_by_id(1400039)
        icon_path = STORY_DEBRIS_ICON_PATH
        self.show_tip_anim(color, text, icon_path)

    def show_mecha_debris_tip(self, item_id):
        color = 'purple'
        text = get_text_by_id(1400051).format(get_item_name(item_id))
        icon_path = MECHA_DEBRIS_ICON_PATH.format(item_id)
        self.show_tip_anim(color, text, icon_path)

    def show_break_tip(self, state_dict):
        if not global_data.player:
            return
        else:
            color = 'blue'
            slot = list(state_dict.keys())[0]
            level = state_dict[slot]
            break_conf = confmgr.get('mecha_breakthrough_data', str(global_data.player.get_pve_select_mecha_id()), default=None)
            conf = break_conf[str(slot)][str(level)]
            text = get_text_by_id(1400051).format(get_text_by_id(conf['name_id']))
            icon_path = conf['icon']
            self.show_tip_anim(color, text, icon_path)
            self.clear_break_sfx()
            sfx_path = EFFECT_PATH.format(color)
            self._break_sfx_id = create_screen_effect_directly(sfx_path)
            return

    def show_energy_tip(self, energy_id):
        color = tip_anim = 'blue'
        conf = self.bless_conf.get(str(energy_id))
        elem_id = conf.get('elem_id', None)
        if elem_id:
            elem_data = confmgr.get('bless_element_data', str(elem_id), default={})
            color = elem_data.get('color', color)
            tip_anim = elem_data.get('tip_anim', color)
        text = get_text_by_id(1400051).format(get_text_by_id(conf['name_id']))
        icon_path = conf.get('icon', '')
        self.show_tip_anim(tip_anim, text, icon_path)
        sfx_path = EFFECT_PATH.format(color)
        self.clear_bless_sfx()
        self._bless_sfx_id = create_screen_effect_directly(sfx_path)
        return

    def show_item_tip(self, new_item_no):
        color = 'purple'
        conf = self.item_conf.get(str(new_item_no), {})
        text = get_text_by_id(1400051).format(get_text_by_id(conf['name_id']))
        icon_path = conf['icon']
        self.show_tip_anim(color, text, icon_path)
        sfx_path = EFFECT_PATH.format(color)
        self.clear_item_sfx()
        self._item_sfx_id = create_screen_effect_directly(sfx_path)

    def clear_break_sfx(self):
        if self._break_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._break_sfx_id)
        self._break_sfx_id = None
        return

    def clear_bless_sfx(self):
        if self._bless_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._bless_sfx_id)
        self._bless_sfx_id = None
        return

    def clear_item_sfx(self):
        if self._item_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._item_sfx_id)
        self._item_sfx_id = None
        return