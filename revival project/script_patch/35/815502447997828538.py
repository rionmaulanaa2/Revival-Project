# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRemoteBattleGuide.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.gcommon.common_utils import battle_utils
from logic.comsys.guide_ui.GuideUI import GuideUI, PCGuideUI
from logic.gcommon.common_utils.parachute_utils import STAGE_PARACHUTE_DROP, STAGE_LAND
from mobile.common.IdManager import IdManager
from data.c_guide_data import GetRemoteGuide, get_remote_guide_params
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK
from logic.gcommon.item import item_const
from logic.gcommon.common_const import mecha_const as mconst
from logic.client.const import game_mode_const
from logic.gcommon.common_const.guide_const import COMBAT_JUNIOR, COMBAT_MIDDLE
from logic.gutils.mecha_utils import get_percent

class ComRemoteBattleGuide(UnitCom):
    BIND_EVENT = {'E_DESTROY_REMOTE_GUIDE': 'destroy_remote_guide',
       'E_DEATH': 'destroy_remote_guide',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteBattleGuide, self).init_from_dict(unit_obj, bdict)
        self._remote_battle_key = None
        self._remote_battle_value = None
        self._collect_timer = None
        self._call_mecha_timer = None
        self._guide_entitys = {}
        self._entity_timer = None
        self._in_remote_guide = False
        self._poison_timer = None
        return

    @property
    def _guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()

    def tick(self, delta):
        if self.ev_g_in_mecha():
            mecha = self.sd.ref_ctrl_target or 0
            cur_hp = mecha.logic.share_data.ref_hp or 0
            max_hp = mecha.logic.share_data.ref_max_hp or 0
            if cur_hp < max_hp * 0.6:
                self.send_event('E_MEHCA_HP_LOW_60')
        else:
            cur_hp = self.sd.ref_hp or 0
            max_hp = self.sd.ref_max_hp or 0
            if cur_hp < max_hp * 0.85:
                self.send_event('E_HP_LOW_85')
        cur_signal = self.sd.ref_cur_signal or 0
        max_signal = self.sd.ref_max_signal or 0
        if cur_signal < max_signal * 0.6:
            self.send_event('E_SIGNAL_LOW_60')
        if cur_signal < max_signal * 0.85:
            self.send_event('E_SIGNAL_LOW_85')
        percent = get_percent(self)
        if percent == 100:
            self.send_event('E_MECHA_ENERGY_100')

    def on_init_complete(self, *_):
        global_data.emgr.on_battle_status_changed += self.construct_guide_logic
        if self.battle.battle_status == 3:
            self.construct_guide_logic(2)

    def construct_guide_logic(self, status):
        if status != 2:
            return
        else:
            global_data.emgr.on_battle_status_changed -= self.construct_guide_logic
            player = global_data.player
            if not self.can_init_guild(player):
                return
            total_cnt = player.get_total_cnt()
            data = player.get_remote_battle_data()
            if player._combat_lv == COMBAT_JUNIOR:
                cnt_limit = 5
            elif player._combat_lv == COMBAT_MIDDLE:
                cnt_limit = 3
            else:
                cnt_limit = 1
            if total_cnt < cnt_limit:
                if not self._guide_ui:
                    return
                self._in_remote_guide = True
                self.need_update = True
                self.construct_guide_logic_data(player)
                self.init_remote_guide()
                self.init_special_remote_guide()
            else:
                self.construct_guide_logic_data(player)
                self.init_special_remote_guide(True)
                player.save_remote_battle_data(None)
            return

    def construct_guide_logic_data(self, player):
        data = player.get_remote_battle_data()
        key = IdManager.id2str(player.battle_id)
        self._remote_battle_key = key
        if data is None or key not in data:
            data = {key: []}
        self._remote_battle_value = data
        return

    def can_init_guild(self, player):
        if player.remote_guide_flag:
            return False
        if player.in_local_battle() or player.in_new_local_battle():
            return False
        if player.is_in_global_spectate():
            return False
        if self.ev_g_is_outsider():
            return False
        if self.ev_g_is_in_spectate():
            return False
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            return False
        return True

    def init_remote_guide--- This code section failed: ---

 155       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'is_pc_mode'
           6  POP_JUMP_IF_FALSE    51  'to 51'

 157       9  LOAD_CONST            1  'remote_mecha_accelerator'

 158      12  LOAD_CONST            2  'remote_mecha_die_accelerator'

 159      15  LOAD_CONST            3  'remote_mecha_thunder'

 160      18  LOAD_CONST            4  'remote_froze_weapon'

 161      21  LOAD_CONST            5  'remote_binder'

 163      24  LOAD_CONST            6  'remote_mecha_energy'

 164      27  LOAD_CONST            7  'remote_ace_time'

 165      30  LOAD_CONST            8  'remote_mecha_stamina_60'

 166      33  LOAD_CONST            9  'remote_stamina_85'

 167      36  LOAD_CONST           10  'remote_signal_85'

 169      39  LOAD_CONST           11  'remote_guide_escape'
          42  BUILD_LIST_11        11 
          45  STORE_FAST            1  'info'
          48  JUMP_FORWARD          9  'to 60'

 172      51  LOAD_GLOBAL           2  'GetRemoteGuide'
          54  CALL_FUNCTION_0       0 
          57  STORE_FAST            1  'info'
        60_0  COME_FROM                '48'

 173      60  SETUP_LOOP          277  'to 340'
          63  LOAD_FAST             1  'info'
          66  GET_ITER         
          67  FOR_ITER            269  'to 339'
          70  STORE_FAST            2  'handler_name'

 174      73  LOAD_FAST             2  'handler_name'
          76  LOAD_CONST           12  'remote_guide_entity'
          79  COMPARE_OP            2  '=='
          82  POP_JUMP_IF_FALSE   271  'to 271'

 175      85  LOAD_GLOBAL           3  'get_remote_guide_params'
          88  LOAD_FAST             2  'handler_name'
          91  CALL_FUNCTION_1       1 
          94  STORE_FAST            3  'param'

 176      97  SETUP_LOOP           76  'to 176'
         100  LOAD_FAST             3  'param'
         103  GET_ITER         
         104  FOR_ITER             68  'to 175'
         107  STORE_FAST            4  'ent_type'

 177     110  LOAD_CONST           13  'remote_guide_entity_{}'
         113  LOAD_ATTR             4  'format'
         116  LOAD_FAST             4  'ent_type'
         119  CALL_FUNCTION_1       1 
         122  STORE_FAST            2  'handler_name'

 178     125  LOAD_FAST             2  'handler_name'
         128  LOAD_FAST             0  'self'
         131  LOAD_ATTR             5  '_remote_battle_value'
         134  LOAD_FAST             0  'self'
         137  LOAD_ATTR             6  '_remote_battle_key'
         140  BINARY_SUBSCR    
         141  COMPARE_OP            6  'in'
         144  POP_JUMP_IF_FALSE   153  'to 153'

 179     147  CONTINUE            104  'to 104'
         150  JUMP_FORWARD          0  'to 153'
       153_0  COME_FROM                '150'

 180     153  LOAD_GLOBAL           7  'set'
         156  BUILD_LIST_0          0 
         159  CALL_FUNCTION_1       1 
         162  LOAD_FAST             0  'self'
         165  LOAD_ATTR             8  '_guide_entitys'
         168  LOAD_FAST             4  'ent_type'
         171  STORE_SUBSCR     
         172  JUMP_BACK           104  'to 104'
         175  POP_BLOCK        
       176_0  COME_FROM                '97'

 181     176  LOAD_FAST             0  'self'
         179  LOAD_ATTR             8  '_guide_entitys'
         182  POP_JUMP_IF_FALSE   336  'to 336'

 182     185  LOAD_FAST             0  'self'
         188  LOAD_ATTR             9  'unit_obj'
         191  LOAD_ATTR            10  'regist_event'
         194  LOAD_CONST           14  'E_GUIDE_ADD_ENTITY'
         197  LOAD_FAST             0  'self'
         200  LOAD_ATTR            11  'add_guide_entity'
         203  CALL_FUNCTION_2       2 
         206  POP_TOP          

 183     207  LOAD_FAST             0  'self'
         210  LOAD_ATTR             9  'unit_obj'
         213  LOAD_ATTR            10  'regist_event'
         216  LOAD_CONST           15  'E_GUIDE_DEL_ENTITY'
         219  LOAD_FAST             0  'self'
         222  LOAD_ATTR            12  'del_guide_entity'
         225  CALL_FUNCTION_2       2 
         228  POP_TOP          

 184     229  LOAD_GLOBAL           0  'global_data'
         232  LOAD_ATTR            13  'game_mgr'
         235  LOAD_ATTR            14  'register_logic_timer'
         238  LOAD_FAST             0  'self'
         241  LOAD_ATTR            15  'check_guide_entity'
         244  LOAD_CONST           16  'interval'
         247  LOAD_CONST           17  1
         250  LOAD_CONST           18  'mode'
         253  LOAD_GLOBAL          16  'CLOCK'
         256  CALL_FUNCTION_513   513 
         259  LOAD_FAST             0  'self'
         262  STORE_ATTR           17  '_entity_timer'
         265  JUMP_ABSOLUTE       336  'to 336'
         268  JUMP_BACK            67  'to 67'

 186     271  LOAD_FAST             2  'handler_name'
         274  LOAD_FAST             0  'self'
         277  LOAD_ATTR             5  '_remote_battle_value'
         280  LOAD_FAST             0  'self'
         283  LOAD_ATTR             6  '_remote_battle_key'
         286  BINARY_SUBSCR    
         287  COMPARE_OP            6  'in'
         290  POP_JUMP_IF_FALSE   299  'to 299'

 187     293  CONTINUE             67  'to 67'
         296  JUMP_FORWARD          0  'to 299'
       299_0  COME_FROM                '296'

 188     299  LOAD_GLOBAL          18  'getattr'
         302  LOAD_GLOBAL          19  'emgr'
         305  LOAD_ATTR             4  'format'
         308  LOAD_FAST             2  'handler_name'
         311  CALL_FUNCTION_1       1 
         314  CALL_FUNCTION_2       2 
         317  STORE_FAST            5  'func'

 189     320  LOAD_FAST             5  'func'
         323  POP_JUMP_IF_FALSE    67  'to 67'

 190     326  LOAD_FAST             5  'func'
         329  CALL_FUNCTION_0       0 
         332  POP_TOP          
         333  JUMP_BACK            67  'to 67'
         336  JUMP_BACK            67  'to 67'
         339  POP_BLOCK        
       340_0  COME_FROM                '60'

 191     340  LOAD_GLOBAL           0  'global_data'
         343  LOAD_ATTR            19  'emgr'
         346  DUP_TOP          
         347  LOAD_ATTR            20  'settle_stage_event'
         350  LOAD_FAST             0  'self'
         353  LOAD_ATTR            21  'destroy_remote_guide'
         356  INPLACE_ADD      
         357  ROT_TWO          
         358  STORE_ATTR           20  'settle_stage_event'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 314

    def init_special_remote_guide--- This code section failed: ---

 195       0  LOAD_CONST            1  'remote_guide_poison'
           3  BUILD_LIST_1          1 
           6  STORE_FAST            2  'info'

 197       9  SETUP_LOOP           79  'to 91'
          12  LOAD_FAST             2  'info'
          15  GET_ITER         
          16  FOR_ITER             71  'to 90'
          19  STORE_FAST            3  'handler_name'

 198      22  LOAD_FAST             3  'handler_name'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             0  '_remote_battle_value'
          31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             1  '_remote_battle_key'
          37  BINARY_SUBSCR    
          38  COMPARE_OP            6  'in'
          41  POP_JUMP_IF_FALSE    50  'to 50'

 199      44  CONTINUE             16  'to 16'
          47  JUMP_FORWARD          0  'to 50'
        50_0  COME_FROM                '47'

 200      50  LOAD_GLOBAL           2  'getattr'
          53  LOAD_GLOBAL           2  'getattr'
          56  LOAD_ATTR             3  'format'
          59  LOAD_FAST             3  'handler_name'
          62  CALL_FUNCTION_1       1 
          65  CALL_FUNCTION_2       2 
          68  STORE_FAST            4  'func'

 201      71  LOAD_FAST             4  'func'
          74  POP_JUMP_IF_FALSE    16  'to 16'

 202      77  LOAD_FAST             4  'func'
          80  CALL_FUNCTION_0       0 
          83  POP_TOP          
          84  JUMP_BACK            16  'to 16'
          87  JUMP_BACK            16  'to 16'
          90  POP_BLOCK        
        91_0  COME_FROM                '9'

 203      91  LOAD_FAST             1  'destroy'
          94  POP_JUMP_IF_FALSE   121  'to 121'

 204      97  LOAD_GLOBAL           4  'global_data'
         100  LOAD_ATTR             5  'emgr'
         103  DUP_TOP          
         104  LOAD_ATTR             6  'settle_stage_event'
         107  LOAD_FAST             0  'self'
         110  LOAD_ATTR             7  'destroy_remote_guide'
         113  INPLACE_ADD      
         114  ROT_TWO          
         115  STORE_ATTR            6  'settle_stage_event'
         118  JUMP_FORWARD          0  'to 121'
       121_0  COME_FROM                '118'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 65

    def save_remote_guide(self, guide):
        self._remote_battle_value[self._remote_battle_key].append(guide)
        global_data.player and global_data.player.save_remote_battle_data(self._remote_battle_value)

    def init_remote_guide_parachute(self):
        self.unit_obj.regist_event('E_PARACHUTE_STATUS_CHANGED', self.remote_guide_parachute)

    def remote_guide_parachute(self, stage):
        if stage == STAGE_PARACHUTE_DROP:
            self.unit_obj.unregist_event('E_PARACHUTE_STATUS_CHANGED', self.remote_guide_parachute)
            guide = 'remote_guide_parachute'
            param = get_remote_guide_params(guide)
            self._guide_ui.show_remote_guide_parachute(*param)
            self.save_remote_guide(guide)

    def init_remote_guide_collect(self):
        self.unit_obj.regist_event('E_PARACHUTE_STATUS_CHANGED', self._trigger_remote_guide_collect)

    def _trigger_remote_guide_collect(self, stage):
        if stage == STAGE_LAND:
            self.unit_obj.unregist_event('E_PARACHUTE_STATUS_CHANGED', self._trigger_remote_guide_collect)
            self.unit_obj.regist_event('E_PICK_UP_SUCC', self.remote_guide_collect)

            def _():
                guide = 'remote_guide_collect'
                param = get_remote_guide_params(guide)
                self._guide_ui.show_remote_guide_collect(*param)
                self.save_remote_guide(guide)
                self._collect_timer = None
                return

            self._collect_timer = global_data.game_mgr.register_logic_timer(lambda : _(), interval=20, times=1, mode=CLOCK)

    def remote_guide_collect(self, *args):
        if self._collect_timer:
            global_data.game_mgr.unregister_logic_timer(self._collect_timer)
            self._collect_timer = None
        self.unit_obj.unregist_event('E_PICK_UP_SUCC', self.remote_guide_collect)
        return

    def init_remote_guide_escape(self):
        global_data.emgr.scene_refresh_poison_circle_event += self.remote_guide_escape

    def remote_guide_escape(self, *_):
        global_data.emgr.scene_refresh_poison_circle_event -= self.remote_guide_escape
        guide = 'remote_guide_escape'
        param = get_remote_guide_params(guide)
        if global_data.is_pc_mode:
            PCGuideUI().show_human_tips_pc(*param)
        else:
            self._guide_ui.show_remote_guide_escape(*param)
        self.save_remote_guide(guide)

    def init_remote_guide_mecha(self):
        check_key = 'remote_guide_mecha'
        flag = self.unit_obj.get_owner().read_guide_data(check_key)
        if flag:
            return
        self.unit_obj.regist_event('E_GUIDE_CHARGER_END', self.remote_guide_mecha)

    def remote_guide_mecha(self):
        self.unit_obj.unregist_event('E_GUIDE_CHARGER_END', self.remote_guide_mecha)
        guide = 'remote_guide_mecha'
        param = get_remote_guide_params(guide)
        self._guide_ui.show_remote_guide_mecha(*param)
        self.save_remote_guide(guide)
        self.unit_obj.get_owner().write_guide_data(guide, 1)

    def add_guide_entity(self, ent_type, ent):
        if ent_type in self._guide_entitys:
            self._guide_entitys[ent_type].add(ent)

    def del_guide_entity(self, ent_type, ent):
        if ent_type in self._guide_entitys:
            if ent in self._guide_entitys[ent_type]:
                self._guide_entitys[ent_type].remove(ent)

    def check_guide_entity(self):
        m_pos = self.ev_g_position()
        del_ent_type = []
        for ent_type in self._guide_entitys:
            for ent in self._guide_entitys[ent_type]:
                c_pop = ent.logic.ev_g_position() if ent.logic else None
                if c_pop:
                    dist = c_pop - m_pos
                    if dist.length < 30 * NEOX_UNIT_SCALE:
                        self.remote_guide_entity(ent_type, ent)
                        del_ent_type.append(ent_type)
                        break

        for ent_type in del_ent_type:
            if ent_type in self._guide_entitys:
                del self._guide_entitys[ent_type]

        if not self._guide_entitys and self._entity_timer:
            self.unit_obj.unregist_event('E_GUIDE_ADD_ENTITY', self.add_guide_entity)
            self.unit_obj.unregist_event('E_GUIDE_DEL_ENTITY', self.del_guide_entity)
            global_data.game_mgr.unregister_logic_timer(self._entity_timer)
        return

    def remote_guide_entity(self, ent_type, ent):

        def _on_sfx(sfx):
            guide = 'remote_guide_entity'
            offset, text_id, time_out = get_remote_guide_params(guide)[ent_type]
            self._guide_ui.show_remote_guide_entity(offset, time_out, text_id, sfx, ent_type, ent)
            self.save_remote_guide('remote_guide_entity_{}'.format(ent_type))

        path = 'effect/fx/guide/guide_end.sfx'
        position = ent.logic.ev_g_position()
        global_data.sfx_mgr.create_sfx_in_scene(path, position, on_create_func=_on_sfx)

    def init_remote_guide_poison(self, *_):
        self.unit_obj.regist_event('E_GUIDE_POISON', self.remote_guide_poison)

    def _show_remote_guide_poison(self):
        self._poison_timer = None
        if not self.is_valid():
            return
        else:
            self.unit_obj.unregist_event('E_GUIDE_POISON', self.remote_guide_poison)
            guide = 'remote_guide_poison'
            if not battle_utils.is_signal_logic():
                text_id, time_out = (5462, 5)
            else:
                text_id, time_out = (5401, 5)
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
            self.save_remote_guide(guide)
            return

    def remote_guide_poison(self, flag):
        if flag:
            self._poison_timer = global_data.game_mgr.register_logic_timer(self._show_remote_guide_poison, interval=5, mode=CLOCK, times=1)
        elif self._poison_timer:
            global_data.game_mgr.unregister_logic_timer(self._poison_timer)
            self._poison_timer = None
        return

    def init_remote_shield(self):
        global_data.emgr.player_armor_changed += self.remote_shield

    def remote_shield(self, pos, armor):
        if pos == item_const.DRESS_POS_SHIELD:
            if armor:
                global_data.emgr.player_armor_changed -= self.remote_shield
                global_data.emgr.player_armor_changed += self.destroy_remote_shield
                guide = 'remote_shield'
                param = get_remote_guide_params(guide)
                self._guide_ui.show_remote_shield(*param)
                self.save_remote_guide(guide)

    def destroy_remote_shield(self, pos, armor):
        if pos == item_const.DRESS_POS_SHIELD:
            if not armor:
                global_data.emgr.player_armor_changed -= self.destroy_remote_shield
                self._guide_ui.panel.nd_shield.setVisible(False)

    def init_remote_carrier(self):
        self.unit_obj.regist_event('E_PICK_UP_OTHERS', self.remote_carrier)

    def remote_carrier(self, item_data):
        if self.ev_g_in_mecha():
            return
        item_id = item_data.get('item_id', 0)
        if item_id == 1667:
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_carrier)
            guide = 'remote_carrier'
            param = get_remote_guide_params(guide)
            self._guide_ui.show_remote_carrier(*param)
            self.save_remote_guide(guide)

    def init_remote_mecha_accelerator(self):
        self.unit_obj.regist_event('E_PICK_UP_OTHERS', self.remote_mecha_accelerator, 99)

    def remote_mecha_accelerator(self, item_data):
        item_id = item_data.get('item_id', 0)
        if item_id == 9906:
            percent = get_percent(self)
            if percent < 90 and self.ev_g_mecha_recall_times() == 0:
                ui = global_data.ui_mgr.get_ui('DrugUI')
                if ui:
                    self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_mecha_accelerator)
                    guide = 'remote_mecha_accelerator'
                    param = get_remote_guide_params(guide)
                    if global_data.is_pc_mode:
                        PCGuideUI().show_temp_use_tips(5410, 3.5)
                    elif ui.is_cur_drug_item(9906):
                        self._guide_ui.show_temp_use_tips(*param)
                    else:
                        ui.special_item_id = 9906
                        self._guide_ui.show_nd_use_small_tips(*param)
                    self.save_remote_guide(guide)

    def init_remote_mecha_die_accelerator(self):
        self.unit_obj.regist_event('E_EJECT', self.remote_mecha_die_accelerator_1, 99)
        self.unit_obj.regist_event('E_PICK_UP_OTHERS', self.remote_mecha_die_accelerator_2, 99)

    def remote_mecha_die_accelerator(self):
        ui = global_data.ui_mgr.get_ui('DrugUI')
        if ui:
            self.unit_obj.unregist_event('E_EJECT', self.remote_mecha_die_accelerator_1)
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_mecha_die_accelerator_2)
            guide = 'remote_mecha_die_accelerator'
            param = get_remote_guide_params(guide)
            if global_data.is_pc_mode:
                PCGuideUI().show_temp_use_tips(5411, 3.5)
            elif ui.is_cur_drug_item(9906):
                self._guide_ui.show_temp_use_tips(*param)
            else:
                ui.special_item_id = 9906
                self._guide_ui.show_nd_use_small_tips(*param)
            self.save_remote_guide(guide)

    def remote_mecha_die_accelerator_1(self, *_):
        if self.ev_g_item_count(9906) > 0:
            self.remote_mecha_die_accelerator()

    def remote_mecha_die_accelerator_2(self, item_data):
        item_id = item_data.get('item_id', 0)
        if item_id == 9906:
            percent = get_percent(self)
            if percent < 90 and self.ev_g_mecha_recall_times() == 1:
                self.remote_mecha_die_accelerator()

    def init_remote_binder(self):
        self.unit_obj.regist_event('E_PICK_UP_OTHERS', self.remote_binder)

    def remote_binder(self, item_data):
        from logic.gcommon.common_utils import battle_utils
        item_id = item_data.get('item_id', 0)
        if item_id == 1612:
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_binder)
            guide = 'remote_binder'
            param = get_remote_guide_params(guide)
            if global_data.is_pc_mode:
                text_id = 5414 if battle_utils.is_signal_logic() else 5515
                PCGuideUI().show_temp_use_tips(text_id, 3.5)
            else:
                self._guide_ui.show_remote_guide_poison(*param)
            self.save_remote_guide(guide)

    def init_remote_call_mecha(self):
        self.unit_obj.regist_event('E_GUIDE_MECHA_FUEL', self.remote_call_mecha)

    def remote_call_mecha(self, opt):
        if opt:
            self.unit_obj.unregist_event('E_GUIDE_MECHA_FUEL', self.remote_call_mecha)
            self.unit_obj.regist_event('E_GUIDE_MECHA_FUEL', self.destroy_remote_call_mecha)
            guide = 'remote_call_mecha'
            param = get_remote_guide_params(guide)
            self._guide_ui.show_remote_call_mecha(*param)
            self.save_remote_guide(guide)

    def destroy_remote_call_mecha(self, opt):
        if opt is False:
            self.unit_obj.unregist_event('E_GUIDE_MECHA_FUEL', self.destroy_remote_call_mecha)
            self._guide_ui.panel.nd_mech_fuel.setVisible(False)

    def init_remote_destroy_mecha(self):
        self.unit_obj.regist_event('E_STATE_CHANGE_CD', self.remote_destroy_mecha)

    def remote_destroy_mecha(self, cd_type, *_):
        if cd_type == mconst.RECALL_CD_TYPE_DIE:
            self.unit_obj.unregist_event('E_STATE_CHANGE_CD', self.remote_destroy_mecha)
            guide = 'remote_destroy_mecha'
            param = get_remote_guide_params(guide)
            self._guide_ui.show_remote_destroy_mecha(*param)
            self.save_remote_guide(guide)

    def init_remote_helmet(self):
        self.unit_obj.regist_event('E_PICK_UP_CLOTHING', self.remote_helmet)

    def remote_helmet(self, item_data, *_):
        if self.ev_g_in_mecha():
            return
        item_id = item_data.get('item_id', 0)
        if item_id == 16541 or item_id == 16542 or item_id == 16543:
            self.unit_obj.unregist_event('E_PICK_UP_CLOTHING', self.remote_helmet)
            guide = 'remote_helmet'
            param = get_remote_guide_params(guide)
            self._guide_ui.show_remote_helmet(*param)
            self.save_remote_guide(guide)

    def init_remote_board(self):
        self.unit_obj.regist_event('E_SUCCESS_BOARD', self.remote_board)

    def remote_board(self, *_):
        self.unit_obj.unregist_event('E_SUCCESS_BOARD', self.remote_board)
        guide = 'remote_board'
        param = get_remote_guide_params(guide)
        self._guide_ui.show_remote_normal(*param)
        self.save_remote_guide(guide)

    def init_remote_weapon_missile(self):
        self.unit_obj.regist_event('E_PICK_UP_WEAPON', self.remote_weapon_missile, 99)

    def remote_weapon_missile(self, item_data, *_):
        if self.ev_g_in_mecha():
            return
        item_id = item_data.get('item_id', 0)
        if item_id == 10544 or item_id == 10543 or item_id == 10542:
            self.unit_obj.unregist_event('E_PICK_UP_WEAPON', self.remote_weapon_missile)
            guide = 'remote_weapon_missile'
            param = get_remote_guide_params(guide)
            text_id, time_out = param
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
            self.save_remote_guide(guide)

    def init_remote_mecha_thunder(self):
        self.unit_obj.regist_event('E_PICK_UP_WEAPON', self.remote_mecha_thunder, 99)

    def remote_mecha_thunder(self, item_data, *_):
        if self.ev_g_in_mecha():
            return
        item_id = item_data.get('item_id', 0)
        if item_id == 10561 or item_id == 10562 or item_id == 10563:
            wp_index = -1
            wp_dict = self.sd.ref_wp_bar_mp_weapons
            if wp_dict:
                for pos, wp in six.iteritems(wp_dict):
                    if wp.get_id() == item_id:
                        wp_index = pos
                        break

            if wp_index == -1:
                return
            self.unit_obj.unregist_event('E_PICK_UP_WEAPON', self.remote_mecha_thunder)
            guide = 'remote_mecha_thunder'
            param = get_remote_guide_params(guide)
            self.save_remote_guide(guide)
            if global_data.is_pc_mode:
                PCGuideUI().show_nd_weapon(item_id, 5412, 3.5)
            elif wp_index == 1:
                self._guide_ui.show_nd_weapon_1(*param)
            elif wp_index == 2:
                self._guide_ui.show_nd_weapon_2(*param)
            elif wp_index == 3:
                self._guide_ui.show_nd_weapon_3(*param)

    def init_remote_froze_weapon(self):
        self.unit_obj.regist_event('E_TRY_SWITCH', self.remote_froze_weapon, 99)

    def remote_froze_weapon(self, switch_pos, switch_status=True, is_init=False):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(switch_pos)
        if weapon is None:
            return
        else:
            item_id = weapon.get_item_id()
            if item_id == 10624 or item_id == 10623:
                self.unit_obj.unregist_event('E_TRY_SWITCH', self.remote_froze_weapon)
                guide = 'remote_froze_weapon'
                param = get_remote_guide_params(guide)
                if global_data.is_pc_mode:
                    PCGuideUI().show_nd_step_18(5416, 3.5)
                else:
                    self._guide_ui.show_nd_change_mode(*param)
                self.save_remote_guide(guide)
            return

    def init_remote_leave_mecha(self):
        self.unit_obj.regist_event('E_ON_LEAVE_MECHA', self.remote_leave_mecha)

    def remote_leave_mecha(self, *_):
        self.unit_obj.unregist_event('E_ON_LEAVE_MECHA', self.remote_leave_mecha)
        guide = 'remote_leave_mecha'
        param = get_remote_guide_params(guide)
        self._guide_ui.show_remote_normal(*param)
        self.save_remote_guide(guide)

    def init_remote_board_water(self):
        self.unit_obj.regist_event('E_GUIDE_MOVE_TO_WATER_SURFACE', self.remote_board_water)

    def remote_board_water(self):
        self.unit_obj.unregist_event('E_GUIDE_MOVE_TO_WATER_SURFACE', self.remote_board_water)
        guide = 'remote_board_water'
        param = get_remote_guide_params(guide)
        self._guide_ui.show_remote_normal(*param)
        self.save_remote_guide(guide)

    def init_remote_mecha_dun(self):
        self.unit_obj.regist_event('E_GUIDE_MECHA_STATE_LEAVE', self.remote_mecha_dun)

    def remote_mecha_dun(self):
        if self.ev_g_ctrl_mecha():
            self.unit_obj.unregist_event('E_GUIDE_MECHA_STATE_LEAVE', self.remote_mecha_dun)
            guide = 'remote_mecha_dun'
            param = get_remote_guide_params(guide)
            self._guide_ui.show_remote_normal(*param)
            self.save_remote_guide(guide)

    def init_remote_signal_60(self):
        self.unit_obj.regist_event('E_SIGNAL_LOW_60', self.remote_signal_60)

    def remote_signal_60(self):
        self.unit_obj.unregist_event('E_SIGNAL_LOW_60', self.remote_signal_60)
        guide = 'remote_signal_60'
        param = get_remote_guide_params(guide)
        self._guide_ui.show_nd_signal_tips(*param)
        self.save_remote_guide(guide)

    def init_remote_mecha_stamina_60(self):
        self.unit_obj.regist_event('E_MEHCA_HP_LOW_60', self.remote_mecha_stamina_60)

    def remote_mecha_stamina_60(self):
        self.unit_obj.unregist_event('E_MEHCA_HP_LOW_60', self.remote_mecha_stamina_60)
        guide = 'remote_mecha_stamina_60'
        param = get_remote_guide_params(guide)
        text_id, time_out = param
        if global_data.is_pc_mode:
            PCGuideUI().show_human_tips_pc(5417, time_out)
            PCGuideUI().show_temp_use_tips(5417, 3.5)
            PCGuideUI().hide_temp_use_tips()
        else:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
        self.save_remote_guide(guide)

    def init_remote_stamina_85(self):
        self.unit_obj.regist_event('E_HP_LOW_85', self.remote_stamina_85)

    def remote_stamina_85(self):
        self.unit_obj.unregist_event('E_HP_LOW_85', self.remote_stamina_85)
        guide = 'remote_stamina_85'
        param = get_remote_guide_params(guide)
        text_id, time_out = param
        if global_data.is_pc_mode:
            PCGuideUI().show_human_tips_pc(5404, time_out)
        else:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
        self.save_remote_guide(guide)

    def init_remote_signal_85(self):
        self.unit_obj.regist_event('E_SIGNAL_LOW_85', self.remote_signal_85)

    def remote_signal_85(self):
        self.unit_obj.unregist_event('E_SIGNAL_LOW_85', self.remote_signal_85)
        guide = 'remote_signal_85'
        param = get_remote_guide_params(guide)
        text_id, time_out = param
        if global_data.is_pc_mode:
            PCGuideUI().show_human_tips_pc(5405, time_out)
        else:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
        self.save_remote_guide(guide)

    def init_remote_ace_time(self):
        global_data.emgr.battle_into_ace_stage_event += self.remote_ace_time

    def remote_ace_time(self):
        global_data.emgr.battle_into_ace_stage_event -= self.remote_ace_time
        guide = 'remote_ace_time'
        param = get_remote_guide_params(guide)
        text_id, time_out = param
        if global_data.is_pc_mode:
            PCGuideUI().show_human_tips_pc(5402, time_out)
        else:
            self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
        self.save_remote_guide(guide)

    def init_remote_mecha_energy(self):
        self.unit_obj.regist_event('E_MECHA_ENERGY_100', self.remote_mecha_energy)

    def remote_mecha_energy(self):
        if self.ev_g_mecha_recall_times() == 0:
            self.unit_obj.unregist_event('E_MECHA_ENERGY_100', self.remote_mecha_energy)
            self.unit_obj.regist_event('E_HEALTH_HP_CHANGE', self.on_remote_mecha_energy)

            def _():
                self._call_mecha_timer = None
                self.on_remote_mecha_energy(0, -1)
                return

            self._call_mecha_timer = global_data.game_mgr.register_logic_timer(lambda : _(), interval=30, times=1, mode=CLOCK)

    def on_remote_mecha_energy(self, hp=0, mod=0):
        if mod < 0 and self.ev_g_mecha_recall_times() == 0:
            percent = get_percent(self)
            if percent == 100:
                if self._call_mecha_timer:
                    global_data.game_mgr.unregister_logic_timer(self._call_mecha_timer)
                    self._call_mecha_timer = None
                self.unit_obj.unregist_event('E_HEALTH_HP_CHANGE', self.on_remote_mecha_energy)
                guide = 'remote_mecha_energy'
                param = get_remote_guide_params(guide)
                text_id, time_out = param
                if global_data.is_pc_mode:
                    PCGuideUI().show_human_tips_pc(5400, time_out)
                    PCGuideUI().adjust_mecha_call(5107, time_out)
                else:
                    self._guide_ui.show_human_tips(get_text_local_content(text_id), time_out)
                    self._guide_ui.show_remote_guide_mecha(80116, time_out)
                self.save_remote_guide(guide)
        return

    def init_remote_module_guide(self):
        total_cnt = global_data.player.get_total_cnt()
        if total_cnt < 2:
            global_data.emgr.switch_control_target_event += self.remote_module_guide

    def remote_module_guide(self, *_):
        if not self.ev_g_in_mecha('Mecha'):
            return
        module = self.ev_g_mecha_all_installed_module()
        if not module:
            return
        ui = global_data.ui_mgr.get_ui('FightStateUI')
        if not ui:
            return
        ui.panel.nd_tip.setVisible(True)
        ui.panel.PlayAnimation('show_tip')
        guide = 'remote_module_guide'
        text_id, timeout = get_remote_guide_params(guide)
        self._guide_ui.show_human_tips(text_id, timeout)

        def _close():
            if ui.panel:
                ui.panel.nd_tip.setVisible(False)
                ui.panel.StopAnimation('show_tip')

        global_data.game_mgr.delay_exec(timeout, _close)
        global_data.emgr.switch_control_target_event -= self.remote_module_guide

    def destroy_remote_guide(self, *_):
        if self._collect_timer:
            global_data.game_mgr.unregister_logic_timer(self._collect_timer)
            self._collect_timer = None
        if self._call_mecha_timer:
            global_data.game_mgr.unregister_logic_timer(self._call_mecha_timer)
            self._call_mecha_timer = None
        if self._entity_timer:
            global_data.game_mgr.unregister_logic_timer(self._entity_timer)
            self._entity_timer = None
        if self._poison_timer:
            global_data.game_mgr.unregister_logic_timer(self._poison_timer)
            self._poison_timer = None
        global_data.emgr.on_battle_status_changed -= self.construct_guide_logic
        if self._in_remote_guide:
            self._in_remote_guide = False
            self.need_update = False
            global_data.emgr.settle_stage_event -= self.destroy_remote_guide
            global_data.emgr.scene_refresh_poison_circle_event -= self.remote_guide_escape
            global_data.emgr.player_armor_changed -= self.remote_shield
            global_data.emgr.player_armor_changed -= self.destroy_remote_shield
            global_data.emgr.switch_control_target_event -= self.remote_module_guide
            self.unit_obj.unregist_event('E_PARACHUTE_STATUS_CHANGED', self.remote_guide_parachute)
            self.unit_obj.unregist_event('E_PARACHUTE_STATUS_CHANGED', self._trigger_remote_guide_collect)
            self.unit_obj.unregist_event('E_PICK_UP_SUCC', self.remote_guide_collect)
            self.unit_obj.unregist_event('E_GUIDE_CHARGER_END', self.remote_guide_mecha)
            self.unit_obj.unregist_event('E_GUIDE_ADD_ENTITY', self.add_guide_entity)
            self.unit_obj.unregist_event('E_GUIDE_DEL_ENTITY', self.del_guide_entity)
            self.unit_obj.unregist_event('E_GUIDE_POISON', self.remote_guide_poison)
            self.unit_obj.unregist_event('E_GUIDE_MECHA_FUEL', self.remote_call_mecha)
            self.unit_obj.unregist_event('E_PICK_UP_CLOTHING', self.remote_helmet)
            self.unit_obj.unregist_event('E_STATE_CHANGE_CD', self.remote_destroy_mecha)
            self.unit_obj.unregist_event('E_GUIDE_MECHA_FUEL', self.destroy_remote_call_mecha)
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_carrier)
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_mecha_accelerator)
            self.unit_obj.unregist_event('E_EJECT', self.remote_mecha_die_accelerator_1)
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_mecha_die_accelerator_2)
            self.unit_obj.unregist_event('E_PICK_UP_OTHERS', self.remote_binder)
            self.unit_obj.unregist_event('E_PICK_UP_WEAPON', self.remote_weapon_missile)
            self.unit_obj.unregist_event('E_PICK_UP_WEAPON', self.remote_mecha_thunder)
            self.unit_obj.unregist_event('E_TRY_SWITCH', self.remote_froze_weapon)
            self.unit_obj.unregist_event('E_ON_LEAVE_MECHA', self.remote_leave_mecha)
            self.unit_obj.unregist_event('E_GUIDE_MECHA_STATE_LEAVE', self.remote_mecha_dun)
            self.unit_obj.unregist_event('E_GUIDE_MOVE_TO_WATER_SURFACE', self.remote_board_water)
            self.unit_obj.unregist_event('E_SUCCESS_BOARD', self.remote_board)
            self.unit_obj.unregist_event('E_SIGNAL_LOW_60', self.remote_signal_60)
            self.unit_obj.unregist_event('E_MEHCA_HP_LOW_60', self.remote_mecha_stamina_60)
            self.unit_obj.unregist_event('E_HP_LOW_85', self.remote_stamina_85)
            self.unit_obj.unregist_event('E_SIGNAL_LOW_85', self.remote_signal_85)
            self.unit_obj.unregist_event('E_MECHA_ENERGY_100', self.remote_mecha_energy)
            self.unit_obj.unregist_event('E_HEALTH_HP_CHANGE', self.on_remote_mecha_energy)
        return

    def destroy(self):
        self.destroy_remote_guide()
        super(ComRemoteBattleGuide, self).destroy()