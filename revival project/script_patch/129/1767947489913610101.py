# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaModuleGroupWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from logic.gutils import template_utils
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import mecha_const
from logic.gutils.mecha_module_utils import get_module_item_bar_pic, init_module_temp_item, get_module_card_name_and_desc

def make_dogtag_msg():
    from logic.gutils import item_utils
    from logic.gcommon.item import item_const
    item_id = item_const.ITEM_NO_DOGTAG
    i_type = battle_const.MED_R_EQUIPMENT_INFO_OLD
    lv = 4
    bar_base_path = 'gui/ui_res_2/battle/notice/bar_equipment'
    vx_base_path = 'gui/ui_res_2/battle/notice/vx_equipment'
    bar_path = template_utils.get_quality_pic_path(bar_base_path, lv)
    vx_path = template_utils.get_quality_pic_path(vx_base_path, lv)
    name_text = item_utils.get_item_name(item_id)
    effect_text = item_utils.get_item_desc(item_id)
    text_format_str = '<fontname="{part_1_font_name}"><size={part_1_font_size}><color={part_1_color}>{part_1_text}</color></size></fontname>\n<fontname="{part_2_font_name}"><size={part_2_font_size}><color={part_2_color}>{part_2_text}</color></size></fontname>'
    text_args = {'part_1_font_name': 'gui/fonts/fzdys.ttf',
       'part_1_font_size': 20,
       'part_1_color': '0XFFFFFFFF',
       'part_1_text': get_text_by_id(19203).format(skill_name=name_text),
       'part_2_font_name': 'gui/fonts/fzy4jw.ttf',
       'part_2_font_size': 18,
       'part_2_color': '0XFFFFFFFF',
       'part_2_text': effect_text
       }
    context_txt = text_format_str.format(**text_args)
    msg = {'i_type': i_type,'item_id': item_id,
       'content_txt': context_txt,
       'bar_path': bar_path,
       'set_attr_dict': {'node_name': 'glow','func_name': 'SetDisplayFrameByPath',
                         'args': (
                                '', vx_path)
                         }
       }
    return msg


def make_weak_msg--- This code section failed: ---

  54       0  LOAD_CONST            1  'gui/ui_res_2/battle/notice/battle_get_tip/frame_reward_%s_pnl.png'
           3  STORE_FAST            2  'bar_base_path'

  55       6  LOAD_GLOBAL           0  'template_utils'
           9  LOAD_ATTR             1  'get_quality_pic_path_ext'
          12  LOAD_FAST             2  'bar_base_path'
          15  LOAD_FAST             1  'lv'
          18  CALL_FUNCTION_2       2 
          21  STORE_FAST            3  'bar_path'

  57      24  LOAD_CONST            2  ''
          27  LOAD_CONST            3  ('BattleMedRCommonInfo',)
          30  IMPORT_NAME           2  'logic.comsys.battle.BattleMedRCommonInfo'
          33  IMPORT_FROM           3  'BattleMedRCommonInfo'
          36  STORE_FAST            4  'BattleMedRCommonInfo'
          39  POP_TOP          

  58      40  LOAD_CONST            2  ''
          43  LOAD_CONST            4  ('get_item_name',)
          46  IMPORT_NAME           4  'logic.gutils.item_utils'
          49  IMPORT_FROM           5  'get_item_name'
          52  STORE_FAST            5  'get_item_name'
          55  POP_TOP          

  59      56  LOAD_FAST             4  'BattleMedRCommonInfo'
          59  LOAD_ATTR             6  'get_weak_content_text'
          62  LOAD_FAST             1  'lv'
          65  LOAD_FAST             5  'get_item_name'
          68  LOAD_FAST             0  'item_id'
          71  CALL_FUNCTION_1       1 
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            6  'content'

  60      80  BUILD_MAP_7           7 

  61      83  LOAD_FAST             6  'content'
          86  LOAD_CONST            5  'content_txt'
          89  STORE_MAP        

  62      90  LOAD_GLOBAL           7  'battle_const'
          93  LOAD_ATTR             8  'MED_R_MODUL_INFO_WEAK'
          96  LOAD_CONST            6  'i_type'
          99  STORE_MAP        

  63     100  STORE_MAP        
         101  STORE_MAP        
         102  STORE_MAP        
         103  STORE_MAP        

  64     104  LOAD_FAST             3  'bar_path'
         107  LOAD_CONST            8  'bar_path'
         110  STORE_MAP        

  65     111  LOAD_FAST             4  'BattleMedRCommonInfo'
         114  LOAD_ATTR             9  'get_anim_name'
         117  LOAD_CONST            9  'show'
         120  LOAD_FAST             1  'lv'
         123  CALL_FUNCTION_2       2 
         126  LOAD_CONST           10  'in_anim'
         129  STORE_MAP        

  66     130  LOAD_FAST             4  'BattleMedRCommonInfo'
         133  LOAD_ATTR             9  'get_anim_name'
         136  LOAD_CONST           11  'hide'
         139  LOAD_FAST             1  'lv'
         142  CALL_FUNCTION_2       2 
         145  LOAD_CONST           12  'out_anim'
         148  STORE_MAP        

  67     149  LOAD_CONST           13  'bar_module'
         152  BUILD_LIST_1          1 
         155  LOAD_CONST           14  'hide_nodes'
         158  STORE_MAP        
         159  STORE_FAST            7  'msg'

  70     162  LOAD_FAST             7  'msg'
         165  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_MAP' instruction at offset 100


def make_msg--- This code section failed: ---

  73       0  LOAD_CONST            1  'gui/ui_res_2/battle/notice/battle_get_tip/frame_reward_%s_pnl.png'
           3  STORE_FAST            3  'bar_base_path'

  74       6  LOAD_GLOBAL           0  'template_utils'
           9  LOAD_ATTR             1  'get_quality_pic_path_ext'
          12  LOAD_FAST             3  'bar_base_path'
          15  LOAD_FAST             2  'lv'
          18  CALL_FUNCTION_2       2 
          21  STORE_FAST            4  'bar_path'

  76      24  LOAD_GLOBAL           2  'get_module_item_bar_pic'
          27  LOAD_FAST             0  'slot_pos'
          30  LOAD_FAST             2  'lv'
          33  LOAD_CONST            2  ''
          36  CALL_FUNCTION_3       3 
          39  STORE_FAST            5  'bar_module_path'

  77      42  LOAD_GLOBAL           0  'template_utils'
          45  LOAD_ATTR             3  'get_module_show_slot_pic'
          48  LOAD_FAST             0  'slot_pos'
          51  LOAD_FAST             1  'card_id'
          54  LOAD_FAST             2  'lv'
          57  CALL_FUNCTION_3       3 
          60  STORE_FAST            6  'icon_module_path'

  78      63  LOAD_GLOBAL           4  'get_module_card_name_and_desc'
          66  LOAD_FAST             1  'card_id'
          69  LOAD_FAST             2  'lv'
          72  LOAD_CONST            3  'try_brief_desc'
          75  LOAD_GLOBAL           5  'True'
          78  CALL_FUNCTION_258   258 
          81  UNPACK_SEQUENCE_2     2 
          84  STORE_FAST            7  'name_text'
          87  STORE_FAST            8  'effect_text'

  80      90  LOAD_CONST            4  '<fontname="{part_1_font_name}"><size={part_1_font_size}><color={part_1_color}>{part_1_text}</color></size></fontname>\n<fontname="{part_2_font_name}"><color={part_2_color}>{part_2_text}</color></fontname>'
          93  STORE_FAST            9  'text_format_str'

  82      96  BUILD_MAP_7           7 

  83      99  LOAD_CONST            5  'gui/fonts/fzdys.ttf'
         102  LOAD_CONST            6  'part_1_font_name'
         105  STORE_MAP        

  84     106  LOAD_CONST            7  20
         109  LOAD_CONST            8  'part_1_font_size'
         112  STORE_MAP        

  85     113  LOAD_CONST            9  '0XFFFFFFFF'
         116  LOAD_CONST           10  'part_1_color'
         119  STORE_MAP        

  86     120  LOAD_GLOBAL           6  'get_text_by_id'
         123  LOAD_CONST           11  19203
         126  CALL_FUNCTION_1       1 
         129  LOAD_ATTR             7  'format'
         132  LOAD_CONST           12  'skill_name'
         135  LOAD_FAST             7  'name_text'
         138  CALL_FUNCTION_256   256 
         141  LOAD_CONST           13  'part_1_text'
         144  STORE_MAP        

  87     145  LOAD_CONST           14  'gui/fonts/fzy4jw.ttf'
         148  LOAD_CONST           15  'part_2_font_name'
         151  STORE_MAP        

  88     152  LOAD_CONST            9  '0XFFFFFFFF'
         155  LOAD_CONST           16  'part_2_color'
         158  STORE_MAP        

  89     159  LOAD_FAST             8  'effect_text'
         162  LOAD_CONST           17  'part_2_text'
         165  STORE_MAP        
         166  STORE_FAST           10  'text_args'

  91     169  LOAD_FAST             9  'text_format_str'
         172  LOAD_ATTR             7  'format'
         175  LOAD_FAST            10  'text_args'
         178  CALL_FUNCTION_KW_0     0 
         181  STORE_FAST           11  'context_txt'

  92     184  LOAD_CONST           18  ''
         187  LOAD_CONST           19  ('BattleMedRCommonInfo',)
         190  IMPORT_NAME           8  'logic.comsys.battle.BattleMedRCommonInfo'
         193  IMPORT_FROM           9  'BattleMedRCommonInfo'
         196  STORE_FAST           12  'BattleMedRCommonInfo'
         199  POP_TOP          

  93     200  BUILD_MAP_8           8 

  94     203  LOAD_FAST            11  'context_txt'
         206  LOAD_CONST           20  'content_txt'
         209  STORE_MAP        

  95     210  LOAD_GLOBAL          10  'battle_const'
         213  LOAD_ATTR            11  'MED_R_MODUL_INFO'
         216  LOAD_CONST           21  'i_type'
         219  STORE_MAP        

  96     220  STORE_MAP        
         221  INPLACE_MODULO   
         222  INPLACE_MODULO   
         223  STORE_MAP        

  97     224  LOAD_FAST             4  'bar_path'
         227  LOAD_CONST           23  'bar_path'
         230  STORE_MAP        

  98     231  LOAD_FAST             5  'bar_module_path'
         234  LOAD_CONST           24  'bar_module_path'
         237  STORE_MAP        

  99     238  LOAD_FAST             6  'icon_module_path'
         241  LOAD_CONST           25  'icon_path'
         244  STORE_MAP        

 100     245  LOAD_FAST            12  'BattleMedRCommonInfo'
         248  LOAD_ATTR            12  'get_anim_name'
         251  LOAD_CONST           26  'show'
         254  LOAD_FAST             2  'lv'
         257  CALL_FUNCTION_2       2 
         260  LOAD_CONST           27  'in_anim'
         263  STORE_MAP        

 101     264  LOAD_FAST            12  'BattleMedRCommonInfo'
         267  LOAD_ATTR            12  'get_anim_name'
         270  LOAD_CONST           28  'hide'
         273  LOAD_FAST             2  'lv'
         276  CALL_FUNCTION_2       2 
         279  LOAD_CONST           29  'out_anim'
         282  STORE_MAP        
         283  STORE_FAST           13  'msg'

 104     286  LOAD_FAST            13  'msg'
         289  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_MAP' instruction at offset 220


class MechaModuleGroupWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self._module_slot_to_ui_item_dict = {}
        self._module_slot_to_item_info_dict = {}
        self.process_event(True)

    def destroy(self):
        self.process_event(False)
        global_data.ui_mgr.close_ui('MechaModuleSpSelectUI')
        self._module_slot_to_ui_item_dict = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'observer_module_changed_event': self.refresh_modules,
           'observer_install_module_result_event': self.on_installed,
           'scene_camera_player_setted_event': self.on_player_setted,
           'battle_add_buff': self.add_player_buff
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_event(self):
        if global_data.cam_lplayer:
            self.init_modules()
            self.refresh_modules()

    def on_player_setted(self):
        self.init_module_slot_item_info()
        self.init_event()

    def init_modules(self):
        if not global_data.cam_lplayer:
            return
        max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
        self.panel.list_module.SetInitCount(max_module_num)
        all_item = self.panel.list_module.GetAllItem()
        for index, ui_item in enumerate(all_item):
            self.module_item_click(ui_item, index + 1)

    def refresh_modules(self):
        if not global_data.cam_lplayer:
            return
        self._module_slot_to_ui_item_dict = {}
        cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
        max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
        for show_slot in range(1, max_module_num + 1):
            item_idx = show_slot - 1
            ui_item = self.panel.list_module.GetItem(item_idx)
            if ui_item:
                card_id, item_id = cur_module_config.get(show_slot, (-1, -1))
                _, card_lv = global_data.cam_lplayer.ev_g_module_item_slot_lv(item_id)
                self.init_module_item(ui_item, card_id, show_slot, card_lv)
                self._module_slot_to_ui_item_dict[show_slot] = ui_item
                if self._module_slot_to_item_info_dict:
                    self._module_slot_to_item_info_dict[show_slot].update({'card_lv': card_lv,'active_card_id': card_id})

    def init_module_item(self, ui_item, card_id, show_slot, card_lv):
        self.init_module_temp_item(ui_item, show_slot, card_id, card_lv)
        ui_item.img_module.setVisible(False)

    def _get_mecha_ui_item_by_install_slot(self, install_slot):
        return self._module_slot_to_ui_item_dict.get(install_slot, None)

    def add_player_buff(self, buff_id, remain_time, add_time, duration, buff_data):
        from logic.gcommon.common_const import battle_const
        if buff_id == 480 and global_data.cam_lplayer:
            msg = make_dogtag_msg()
            global_data.cam_lplayer.send_event('E_SHOW_MED_R_BATTLE_MESSAGE', msg, battle_const.MED_R_NODE_COMMON_INFO)

    def on_installed(self, result, slot_pos, card_id, item_id):
        if not result:
            return
        else:
            from logic.gcommon.common_utils.local_text import get_text_by_id
            from common.cfg import confmgr
            cards_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
            card_conf = cards_conf.get(str(card_id))
            if card_id:
                ui_item = self._get_mecha_ui_item_by_install_slot(slot_pos)
                if ui_item:
                    module_id = item_id
                    from logic.gutils.item_utils import get_item_pic_by_item_no
                    ui_item.img_module.SetDisplayFrameByPath('', get_item_pic_by_item_no(module_id))
            if global_data.cam_lplayer:
                from common.cfg import confmgr
                lv = confmgr.get('item', str(item_id), default={}).get('level', 0)
                weak = not bool(card_id)
                if weak:
                    from logic.client.const.game_mode_const import GAME_MODE_GVG, GAME_MODE_DUEL
                    if global_data.game_mode and global_data.game_mode.is_mode_type((GAME_MODE_GVG, GAME_MODE_DUEL)):
                        msg = None
                    else:
                        msg = make_weak_msg(item_id, lv)
                else:
                    msg = make_msg(slot_pos, card_id, lv)
                if msg is not None:
                    global_data.cam_lplayer.send_event('E_SHOW_MED_R_BATTLE_MESSAGE', msg, battle_const.MED_R_NODE_COMMON_INFO)
            return

    def init_module_temp_item(self, ui_temp_item, show_slot, card_id, card_level):
        mecha_talent_path = template_utils.get_module_show_slot_pic(show_slot, None, card_level)
        init_module_temp_item(ui_temp_item, show_slot, card_id, card_level, 'small_')
        if card_level:
            ui_temp_item.img_skill.setVisible(True)
        need_show_card_index = False
        if card_id > 0 and card_level and show_slot == mecha_const.SP_MODULE_SLOT:
            if global_data.player:
                lplayer = global_data.player.logic if 1 else None
                if lplayer and lplayer.ev_g_get_bind_mecha():
                    sp_card_plan = lplayer.ev_g_mecha_module_sp_slot_plan() or []
                    if card_id in sp_card_plan:
                        card_index = sp_card_plan.index(card_id)
                        ui_temp_item.img_core_num.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_module/icon_module_sp_%d.png' % (card_index + 1))
                        ui_temp_item.img_core_num.setVisible(True)
                        need_show_card_index = True
            need_show_card_index or ui_temp_item.img_core_num.setVisible(False)
        return

    def init_module_slot_item_info(self):
        if not global_data.cam_lplayer:
            return
        else:
            all_module_config = global_data.cam_lplayer.ev_g_replicate_module_plans()
            if not all_module_config:
                return
            mecha_id = global_data.cam_lplayer.ev_g_get_bind_mecha_type()
            if mecha_id is None:
                return
            module_config = all_module_config.get(mecha_id, {})
            if not module_config:
                return
            for slot_pos, slot_info in six.iteritems(module_config):
                self._module_slot_to_item_info_dict[slot_pos] = {'card_ids': slot_info}

            return

    def module_item_click(self, module_item, slot_no):

        @module_item.bar_item.btn.unique_callback()
        def OnBegin(btn, touch):
            if not self._module_slot_to_item_info_dict:
                return
            fight_state_ui = global_data.ui_mgr.get_ui('FightStateUI')
            if fight_state_ui:
                icon_path = module_item.img_skill.GetDisplayFramePath()
                pos = module_item.GetPosition()
                if slot_no not in six_ex.keys(self._module_slot_to_item_info_dict):
                    return
                fight_state_ui.show_mecha_module_tips(slot_no, self._module_slot_to_item_info_dict[slot_no], icon_path, pos)

        @module_item.bar_item.btn.unique_callback()
        def OnDrag(btn, touch):
            pass

        @module_item.bar_item.btn.unique_callback()
        def OnEnd(btn, touch):
            fight_state_ui = global_data.ui_mgr.get_ui('FightStateUI')
            if fight_state_ui:
                fight_state_ui.hide_mecha_module_tips()