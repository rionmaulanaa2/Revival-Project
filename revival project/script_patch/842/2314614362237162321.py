# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComItemUseClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.time_utility as t_util
from ...cdata import status_config as st_const
from logic.gcommon.item.backpack_item_type import B_ITEM_MECHATRAN_ID, B_ITEM_ICEWALL_ID, B_ITEM_TYPE_BACK_HOME_ID, B_ITEM_BOUNCING_PLAT, B_ITEM_BOUNCING_PLAT_9927, B_ITEM_BOUNCING_PLAT_PVE, B_ITEM_ICEWALL_ID_PVE
from logic.gcommon.common_const.collision_const import MECHA_TRANS_HEIGHT
import world
from logic.gcommon.item import client_item_check_handler, client_item_use_handler
import logic.gcommon.common_utils.item_config as item_conf
import math3d
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.mecha_utils import CallMecha
from logic.gcommon.item import item_utility
from logic.gutils.client_unit_tag_utils import preregistered_tags
MP_ITEMS = {}
HUMAN_SUMMON_ICEWALL_DISTANCE = 2.5 * NEOX_UNIT_SCALE
MECHA_SUMMON_ICEWALL_DISTANCE = 5.5 * NEOX_UNIT_SCALE

class ComItemUseClient(UnitCom):
    BIND_EVENT = {'E_ITEMUSE_TRY': '_try_use',
       'E_ITEMUSE_DO': '_do_use',
       'E_ITEMUSE_CANCEL': '_cancel_use',
       'E_ITEMUSE_ON': '_on_used',
       'E_SET_ITEM_CD': '_set_item_cd',
       'E_ITEMUSE_TRY_RET': '_on_try_ret',
       'G_CUR_ITEMUSE': '_get_cur_use',
       'E_ITEMUSE_CANCEL_RES': '_cancel_use_res',
       'E_SET_CONTROL_TARGET': '_set_control_target',
       'G_CUR_SINGING_ID': '_get_cur_singing_id',
       'G_USE_ITEM_CD': '_get_use_item_cd',
       'G_BELOW_USE_ITEM_LIMIT': '_check_below_item_limit',
       'G_USE_ITEM_COST_TIME_FACTOR': 'get_item_use_sing_time_factor',
       'E_TRY_USE_STATUS_SUC': 'on_try_use_status_suc',
       'E_TRY_USE_STATUS_FAILED': 'on_try_use_status_failed',
       'E_SHOW_USE_PROGRESS': 'on_show_use_progress',
       'E_SET_ELASTICITY_USE_CD': ('set_elasticity_use_cd', -99),
       'G_ELASTICITY_USE_CD': 'get_elasticity_use_cd',
       'E_REFRESH_ITEM_LIMIT': 'refresh_item_limit',
       'E_CLEAR_ITEM_USE_STATUS': '_clear_item_use_status'
       }

    def __init__(self):
        super(ComItemUseClient, self).__init__()
        self._cur_singing_id = 0
        self.is_register_drug_use_event = False
        self._ctrl_target = None
        self._start_use_pos = None
        self._use_item_cd = {}
        self._use_item_limit = {}
        self._elasticity_use_cd = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComItemUseClient, self).init_from_dict(unit_obj, bdict)
        self._cur_singing_id = bdict.get('last_try_item', None)
        self.last_try_time = bdict.get('last_try_time', None)
        self._use_item_cd = bdict.get('use_item_cd', {})
        self._use_item_limit = bdict.get('use_item_limit', {})
        self._elasticity_use_cd = bdict.get('elasticity_use_cd', 0)
        return

    def on_post_init_complete(self, bdict):
        global_data.game_mgr.next_exec(self.on_init_drug_item)

    def on_init_drug_item(self):
        self._init_ctrl_target()
        self.restore_from_reconnect(self._cur_singing_id, self.last_try_time)

    def _init_ctrl_target(self):
        target = self.ev_g_control_target()
        self._set_control_target(target)

    def reset(self):
        self._cur_singing_id = 0

    def _get_cur_singing_id(self):
        return self._cur_singing_id

    def _check_use(self, item_id):
        if self._cur_singing_id == item_id:
            return False
        if self._cur_singing_id and self._cur_singing_id != item_id:
            self.send_event('E_ITEMUSE_CANCEL', self._cur_singing_id)
            return False
        count = self.ev_g_item_count(item_id)
        if count <= 0:
            return False
        if not self.ev_g_status_try_trans(st_const.ST_USE_ITEM):
            return False
        return True

    def _try_use(self, item_id):
        conf = item_conf.get_use_by_id(item_id)
        if conf:
            check_handler_name = conf.get('cClientCheckHandler')
            check_args = conf.get('cClientCheckArgs', {})
            if check_handler_name:
                check_handler = getattr(client_item_check_handler, check_handler_name)
                if callable(check_handler):
                    ret, msg_id = check_handler(self.unit_obj, item_id, check_args)
                    if not ret:
                        if msg_id:
                            msg = get_text_by_id(msg_id)
                            global_data.emgr.battle_show_message_event.emit(msg)
                        return
        if not self._check_use(item_id):
            return
        self._cur_singing_id = item_id
        self._sync_try_use(item_id)

    def _on_try_ret(self, item_id, ret):
        if not ret:
            self._on_try_failed(item_id)
        else:
            self._on_try_success(item_id)

    def _on_try_failed(self, item_id):
        self.ev_g_cancel_state(st_const.ST_USE_ITEM)
        self._cur_singing_id = 0
        if item_utility.is_mecha_battery(item_id):
            self.send_event('E_SHOW_MESSAGE', get_text_by_id(83452))

    def get_item_use_sing_time_factor(self, item_id):
        import logic.gcommon.common_utils.item_config as item_conf
        item_confs = item_conf.get_by_id(item_id)
        item_type = item_confs.get('type', 1)
        common_item_sing_time_factor = self.ev_g_add_attr('item_sing_time_factor')
        item_type_sing_time_factor = self.ev_g_add_attr('item_type_sing_time_factor_{}'.format(item_type))
        return common_item_sing_time_factor + item_type_sing_time_factor

    def _on_try_success(self, item_id, start_time=0):
        import logic.gcommon.common_utils.item_config as item_conf
        conf = item_conf.get_use_by_id(item_id)
        if not conf:
            self._do_use(item_id)
        t_singing = conf['fSingTime'] * (1 + self.get_item_use_sing_time_factor(item_id))
        if t_singing <= start_time:
            self._do_use(item_id)
            return
        else:
            action_id = conf.get('iAction', None)
            self.send_event('E_ITEMUSE_PRE', item_id, t_singing, start_time, action_id)
            return

    def on_try_use_status_suc(self, item_id, t_singing, start_time):
        self.send_event('E_SHOW_USE_PROGRESS', item_id, t_singing, start_time)

    def on_try_use_status_failed(self, item_id, t_singing, start_time):
        self.send_event('E_ITEMUSE_CANCEL', self._cur_singing_id)

    def on_show_use_progress(self, item_id, t_singing, start_time):
        from data.item_use_var import ALL_USABLE_ID_LIST
        if item_id in ALL_USABLE_ID_LIST:
            self._register_drug_use_cancel_event()
        from logic.gutils import item_utils

        def cancel_callback(*args):
            if not self.is_enable():
                return
            self.ev_g_cancel_state(st_const.ST_USE_ITEM)
            self.send_event('E_ITEMUSE_CANCEL', self._cur_singing_id)

        def finish_callback--- This code section failed: ---

 201       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'is_enable'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 202      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 203      16  RETURN_VALUE     
          17  RETURN_VALUE     
          18  RETURN_VALUE     
          19  BINARY_SUBSCR    
          20  STORE_FAST            1  'item_id'

 205      23  LOAD_FAST             1  'item_id'
          26  LOAD_GLOBAL           1  'B_ITEM_MECHATRAN_ID'
          29  COMPARE_OP            2  '=='
          32  POP_JUMP_IF_FALSE   264  'to 264'

 206      35  LOAD_DEREF            0  'self'
          38  LOAD_ATTR             2  'ev_g_human_col_id'
          41  CALL_FUNCTION_0       0 
          44  STORE_FAST            2  'exclude_ids'

 207      47  LOAD_DEREF            0  'self'
          50  LOAD_ATTR             3  'ev_g_position'
          53  CALL_FUNCTION_0       0 
          56  STORE_FAST            3  'pos'

 208      59  LOAD_GLOBAL           4  'world'
          62  LOAD_ATTR             5  'get_active_scene'
          65  CALL_FUNCTION_0       0 
          68  STORE_FAST            4  'scn'

 209      71  LOAD_FAST             2  'exclude_ids'
          74  POP_JUMP_IF_FALSE   186  'to 186'
          77  LOAD_FAST             3  'pos'
          80  POP_JUMP_IF_FALSE   186  'to 186'
          83  LOAD_FAST             4  'scn'
        86_0  COME_FROM                '80'
        86_1  COME_FROM                '74'
          86  POP_JUMP_IF_FALSE   186  'to 186'

 210      89  LOAD_DEREF            1  'item_utils'
          92  LOAD_ATTR             6  'check_use_mechatran_card_valid'
          95  LOAD_FAST             4  'scn'
          98  LOAD_FAST             3  'pos'
         101  LOAD_FAST             2  'exclude_ids'
         104  CALL_FUNCTION_3       3 
         107  UNPACK_SEQUENCE_2     2 
         110  STORE_FAST            5  'is_valid'
         113  STORE_FAST            3  'pos'

 211     116  LOAD_FAST             5  'is_valid'
         119  POP_JUMP_IF_TRUE    186  'to 186'

 212     122  LOAD_DEREF            0  'self'
         125  LOAD_ATTR             7  'send_event'
         128  LOAD_CONST            2  'E_SHOW_MESSAGE'
         131  LOAD_GLOBAL           8  'get_text_by_id'
         134  LOAD_CONST            3  18225
         137  CALL_FUNCTION_1       1 
         140  CALL_FUNCTION_2       2 
         143  POP_TOP          

 213     144  LOAD_DEREF            0  'self'
         147  LOAD_ATTR             9  'ev_g_cancel_state'
         150  LOAD_GLOBAL          10  'st_const'
         153  LOAD_ATTR            11  'ST_USE_ITEM'
         156  CALL_FUNCTION_1       1 
         159  POP_TOP          

 214     160  LOAD_DEREF            0  'self'
         163  LOAD_ATTR             7  'send_event'
         166  LOAD_CONST            4  'E_ITEMUSE_CANCEL'
         169  LOAD_DEREF            0  'self'
         172  LOAD_ATTR            12  '_cur_singing_id'
         175  CALL_FUNCTION_2       2 
         178  POP_TOP          

 215     179  LOAD_CONST            0  ''
         182  RETURN_END_IF    
       183_0  COME_FROM                '119'
         183  JUMP_FORWARD          0  'to 186'
       186_0  COME_FROM                '183'

 216     186  LOAD_DEREF            0  'self'
         189  LOAD_ATTR             9  'ev_g_cancel_state'
         192  LOAD_GLOBAL          10  'st_const'
         195  LOAD_ATTR            11  'ST_USE_ITEM'
         198  CALL_FUNCTION_1       1 
         201  POP_TOP          

 217     202  LOAD_GLOBAL          13  'MECHA_TRANS_HEIGHT'
         205  LOAD_CONST            5  2.0
         208  BINARY_DIVIDE    
         209  STORE_FAST            6  'half_height'

 218     212  LOAD_DEREF            0  'self'
         215  LOAD_ATTR            14  '_do_use'
         218  LOAD_FAST             1  'item_id'
         221  LOAD_CONST            6  'extra_data'
         224  BUILD_MAP_1           1 
         227  LOAD_FAST             3  'pos'
         230  LOAD_ATTR            15  'x'
         233  LOAD_FAST             3  'pos'
         236  LOAD_ATTR            16  'y'
         239  LOAD_FAST             6  'half_height'
         242  BINARY_SUBTRACT  
         243  LOAD_FAST             3  'pos'
         246  LOAD_ATTR            17  'z'
         249  BUILD_TUPLE_3         3 
         252  LOAD_CONST            7  'position'
         255  STORE_MAP        
         256  CALL_FUNCTION_257   257 
         259  POP_TOP          

 219     260  LOAD_CONST            0  ''
         263  RETURN_END_IF    
       264_0  COME_FROM                '32'

 220     264  LOAD_FAST             1  'item_id'
         267  LOAD_GLOBAL          18  'B_ITEM_ICEWALL_ID'
         270  LOAD_GLOBAL          19  'B_ITEM_ICEWALL_ID_PVE'
         273  BUILD_LIST_2          2 
         276  COMPARE_OP            6  'in'
         279  POP_JUMP_IF_FALSE   504  'to 504'

 222     282  LOAD_GLOBAL          20  'global_data'
         285  LOAD_ATTR            21  'cam_lctarget'
         288  LOAD_ATTR            22  'sd'
         291  LOAD_ATTR            23  'ref_is_mecha'
         294  POP_JUMP_IF_FALSE   303  'to 303'
         297  LOAD_GLOBAL          24  'MECHA_SUMMON_ICEWALL_DISTANCE'
         300  JUMP_FORWARD          3  'to 306'
         303  LOAD_GLOBAL          25  'HUMAN_SUMMON_ICEWALL_DISTANCE'
       306_0  COME_FROM                '300'
         306  STORE_FAST            7  'near'

 223     309  LOAD_CONST            8  ''
         312  STORE_FAST            8  'yaw'

 224     315  LOAD_DEREF            0  'self'
         318  LOAD_ATTR            26  'scene'
         321  LOAD_ATTR            27  'get_com'
         324  LOAD_CONST            9  'PartCamera'
         327  CALL_FUNCTION_1       1 
         330  STORE_FAST            9  'com_camera'

 225     333  LOAD_FAST             9  'com_camera'
         336  POP_JUMP_IF_FALSE   354  'to 354'

 226     339  LOAD_FAST             9  'com_camera'
         342  LOAD_ATTR            28  'get_yaw'
         345  CALL_FUNCTION_0       0 
         348  STORE_FAST            8  'yaw'
         351  JUMP_FORWARD          0  'to 354'
       354_0  COME_FROM                '351'

 227     354  LOAD_GLOBAL          29  'CallMecha'
         357  LOAD_FAST             7  'near'
         360  CALL_FUNCTION_1       1 
         363  UNPACK_SEQUENCE_2     2 
         366  STORE_FAST           10  'res'
         369  STORE_FAST            3  'pos'

 228     372  LOAD_DEREF            0  'self'
         375  LOAD_ATTR             9  'ev_g_cancel_state'
         378  LOAD_GLOBAL          10  'st_const'
         381  LOAD_ATTR            11  'ST_USE_ITEM'
         384  CALL_FUNCTION_1       1 
         387  POP_TOP          

 229     388  LOAD_FAST            10  'res'
         391  POP_JUMP_IF_FALSE   460  'to 460'

 230     394  LOAD_DEREF            0  'self'
         397  LOAD_ATTR            14  '_do_use'
         400  LOAD_FAST             1  'item_id'
         403  LOAD_CONST            6  'extra_data'
         406  BUILD_MAP_2           2 
         409  LOAD_FAST             3  'pos'
         412  LOAD_ATTR            15  'x'
         415  LOAD_FAST             3  'pos'
         418  LOAD_ATTR            16  'y'
         421  LOAD_FAST             3  'pos'
         424  LOAD_ATTR            17  'z'
         427  BUILD_TUPLE_3         3 
         430  LOAD_CONST            7  'position'
         433  STORE_MAP        
         434  LOAD_FAST             8  'yaw'
         437  LOAD_CONST            8  ''
         440  LOAD_CONST            8  ''
         443  LOAD_CONST            8  ''
         446  BUILD_TUPLE_4         4 
         449  LOAD_CONST           10  'rot'
         452  STORE_MAP        
         453  CALL_FUNCTION_257   257 
         456  POP_TOP          
         457  JUMP_ABSOLUTE       704  'to 704'

 232     460  LOAD_GLOBAL          20  'global_data'
         463  LOAD_ATTR            30  'player'
         466  LOAD_ATTR            31  'logic'
         469  LOAD_ATTR             7  'send_event'
         472  LOAD_CONST            2  'E_SHOW_MESSAGE'
         475  LOAD_GLOBAL           8  'get_text_by_id'
         478  LOAD_CONST           11  18144
         481  CALL_FUNCTION_1       1 
         484  CALL_FUNCTION_2       2 
         487  POP_TOP          

 233     488  LOAD_DEREF            0  'self'
         491  LOAD_ATTR            32  '_cancel_use'
         494  LOAD_FAST             1  'item_id'
         497  CALL_FUNCTION_1       1 
         500  POP_TOP          
         501  JUMP_FORWARD        200  'to 704'

 236     504  LOAD_FAST             1  'item_id'
         507  LOAD_GLOBAL          33  'B_ITEM_BOUNCING_PLAT'
         510  LOAD_GLOBAL          34  'B_ITEM_BOUNCING_PLAT_9927'
         513  LOAD_GLOBAL          35  'B_ITEM_BOUNCING_PLAT_PVE'
         516  BUILD_TUPLE_3         3 
         519  COMPARE_OP            6  'in'
         522  POP_JUMP_IF_FALSE   704  'to 704'

 237     525  LOAD_GLOBAL          20  'global_data'
         528  LOAD_ATTR            21  'cam_lctarget'
         531  POP_JUMP_IF_TRUE    538  'to 538'

 238     534  LOAD_CONST            0  ''
         537  RETURN_END_IF    
       538_0  COME_FROM                '531'

 239     538  LOAD_GLOBAL          20  'global_data'
         541  LOAD_ATTR            21  'cam_lctarget'
         544  LOAD_ATTR            22  'sd'
         547  LOAD_ATTR            23  'ref_is_mecha'
         550  POP_JUMP_IF_FALSE   559  'to 559'
         553  LOAD_GLOBAL          24  'MECHA_SUMMON_ICEWALL_DISTANCE'
         556  JUMP_FORWARD          3  'to 562'
         559  LOAD_GLOBAL          25  'HUMAN_SUMMON_ICEWALL_DISTANCE'
       562_0  COME_FROM                '556'
         562  STORE_FAST            7  'near'

 240     565  LOAD_GLOBAL          29  'CallMecha'
         568  LOAD_FAST             7  'near'
         571  CALL_FUNCTION_1       1 
         574  UNPACK_SEQUENCE_2     2 
         577  STORE_FAST           10  'res'
         580  STORE_FAST            3  'pos'

 241     583  LOAD_DEREF            0  'self'
         586  LOAD_ATTR             9  'ev_g_cancel_state'
         589  LOAD_GLOBAL          10  'st_const'
         592  LOAD_ATTR            11  'ST_USE_ITEM'
         595  CALL_FUNCTION_1       1 
         598  POP_TOP          

 242     599  LOAD_FAST            10  'res'
         602  POP_JUMP_IF_FALSE   659  'to 659'

 243     605  LOAD_DEREF            0  'self'
         608  LOAD_ATTR            14  '_do_use'
         611  LOAD_FAST             1  'item_id'
         614  LOAD_CONST            6  'extra_data'
         617  BUILD_MAP_2           2 
         620  LOAD_FAST             3  'pos'
         623  LOAD_ATTR            15  'x'
         626  LOAD_FAST             3  'pos'
         629  LOAD_ATTR            16  'y'
         632  LOAD_FAST             3  'pos'
         635  LOAD_ATTR            17  'z'
         638  BUILD_TUPLE_3         3 
         641  LOAD_CONST            7  'position'
         644  STORE_MAP        
         645  LOAD_CONST           13  (0.0, 0.0, 0.0, 1.0)
         648  LOAD_CONST           10  'rot'
         651  STORE_MAP        
         652  CALL_FUNCTION_257   257 
         655  POP_TOP          
         656  JUMP_FORWARD         41  'to 700'

 245     659  LOAD_GLOBAL          20  'global_data'
         662  LOAD_ATTR            30  'player'
         665  LOAD_ATTR            31  'logic'
         668  LOAD_ATTR             7  'send_event'
         671  LOAD_CONST            2  'E_SHOW_MESSAGE'
         674  LOAD_GLOBAL           8  'get_text_by_id'
         677  LOAD_CONST           11  18144
         680  CALL_FUNCTION_1       1 
         683  CALL_FUNCTION_2       2 
         686  POP_TOP          

 246     687  LOAD_DEREF            0  'self'
         690  LOAD_ATTR            32  '_cancel_use'
         693  LOAD_FAST             1  'item_id'
         696  CALL_FUNCTION_1       1 
         699  POP_TOP          
       700_0  COME_FROM                '656'

 247     700  LOAD_CONST            0  ''
         703  RETURN_END_IF    
       704_0  COME_FROM                '522'
       704_1  COME_FROM                '501'

 249     704  LOAD_DEREF            0  'self'
         707  LOAD_ATTR             9  'ev_g_cancel_state'
         710  LOAD_GLOBAL          10  'st_const'
         713  LOAD_ATTR            11  'ST_USE_ITEM'
         716  CALL_FUNCTION_1       1 
         719  POP_TOP          

 250     720  LOAD_DEREF            0  'self'
         723  LOAD_ATTR            14  '_do_use'
         726  LOAD_FAST             1  'item_id'
         729  CALL_FUNCTION_1       1 
         732  POP_TOP          

Parse error at or near `RETURN_VALUE' instruction at offset 16

        from common.cfg import confmgr
        icon_path = confmgr.get('item_use', str(item_id), 'cSpItem', default=None)
        if item_id in (9902, 9904):
            self.send_event('E_SHOW_PROGRESS', t_singing, item_id, get_text_by_id(10145), lambda : finish_callback(item_id), cancel_callback, start_time, icon_path)
        elif item_id == B_ITEM_TYPE_BACK_HOME_ID:
            self.send_event('E_SHOW_PROGRESS', t_singing, item_id, get_text_by_id(19716), lambda : finish_callback(item_id), cancel_callback, start_time, icon_path)
        else:
            name = item_utils.get_item_name(item_id)
            self.send_event('E_SHOW_PROGRESS', t_singing, item_id, get_text_by_id(18071).format(name=name), lambda : finish_callback(item_id), cancel_callback, start_time, icon_path)
        return

    def _do_use(self, item_id, extra_data=None):
        if not self.is_enable():
            return
        if item_id != self._cur_singing_id:
            return
        self._sync_do_use(item_id, extra_data)
        if self._cur_singing_id != 0:
            self.ev_g_cancel_state(st_const.ST_USE_ITEM)
            self.send_event('E_ITEMUSE_END', self._cur_singing_id)
            self._cur_singing_id = 0

    def _cancel_use(self, item_id=None, is_sync=True, new_state=None):
        from data.item_use_var import ALL_USABLE_ID_LIST
        if item_id in ALL_USABLE_ID_LIST or item_id is None:
            self._unregister_drug_use_cancel_event()
        if is_sync:
            self._sync_cancel_use(self._cur_singing_id)
            self._cur_singing_id = 0
            return
        else:
            self.ev_g_cancel_state(st_const.ST_USE_ITEM)
            self.send_event('E_ITEMUSE_END', self._cur_singing_id, new_state)
            self._cur_singing_id = 0
            return

    def _cancel_use_res(self, item_id=None):
        self._cancel_use(item_id, False)
        if self._cur_singing_id:
            self.ev_g_cancel_state(st_const.ST_USE_ITEM)
            self.send_event('E_ITEMUSE_END', self._cur_singing_id)
            self._cur_singing_id = 0

    def _set_control_target(self, target, *args):
        if self._ctrl_target and self._ctrl_target.logic:
            if G_POS_CHANGE_MGR:
                self._ctrl_target.logic.unregist_pos_change(self.item_use_move_helper)
            else:
                self._ctrl_target.logic.unregist_event('E_POSITION', self.item_use_move_helper)
            self._interrupt_drug_use()
        if target and target.logic and target.logic.MASK & preregistered_tags.VEHICLE_TAG_VALUE:
            if G_POS_CHANGE_MGR:
                target.logic.regist_pos_change(self.item_use_move_helper, 0.1)
            else:
                target.logic.regist_event('E_POSITION', self.item_use_move_helper)
        self._ctrl_target = target

    def _on_used(self, item_id, item_cd=None, item_limit=None):
        from data.item_use_var import ALL_USABLE_ID_LIST
        self.send_event('E_ITEMUSE_END', item_id)
        if item_id in ALL_USABLE_ID_LIST:
            self._unregister_drug_use_cancel_event()
        import logic.gcommon.common_utils.item_config as item_conf
        conf = item_conf.get_use_by_id(str(item_id))
        if not conf:
            return
        else:
            use_handler_name = conf.get('cClientUseHandler')
            use_args = conf.get('cClientUseArg', {})
            if use_handler_name:
                use_handler = getattr(client_item_use_handler, use_handler_name)
                if callable(use_handler):
                    use_handler(self.unit_obj, item_id, use_args)
            if item_id == B_ITEM_TYPE_BACK_HOME_ID:
                global_data.emgr.on_apply_suicide_back_home_event.emit()
                return
            sfx_res = conf.get('cRes', None)
            if sfx_res:
                import math3d
                size = global_data.really_sfx_window_size
                scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)

                def create_cb(sfx):
                    sfx.scale = scale

                global_data.sfx_mgr.create_sfx_in_scene(sfx_res, on_create_func=create_cb)
            if item_cd is not None:
                self._use_item_cd[item_id] = item_cd
                global_data.emgr.scene_refresh_use_item_cd.emit()
            if item_limit is not None:
                self._use_item_limit[item_id] = item_limit
            on_used_sound = conf.get('cOnUsedSound', None)
            if on_used_sound:
                self.send_event('E_PLAY_ON_USED_SOUND', item_id, on_used_sound)
            return

    def _set_item_cd(self, item_id, item_cd):
        if item_cd is not None:
            self._use_item_cd[item_id] = item_cd
            global_data.emgr.scene_refresh_use_item_cd.emit()
        return

    def refresh_item_limit(self, item_id, cnt):
        self._use_item_limit[item_id] = cnt

    def _get_use_item_cd(self, item_id):
        return self._use_item_cd.get(item_id)

    def _get_cur_use(self):
        return self._cur_singing_id

    def destroy(self):
        self._set_control_target(None)
        super(ComItemUseClient, self).destroy()
        return

    def _sync_try_use(self, item_id):
        self.send_event('E_CALL_SYNC_METHOD', 'item_use_try', (item_id,), False, False, False)

    def _sync_do_use(self, item_id, extra_data):
        cur_pos = self.ev_g_position()
        area_id = self.scene.get_scene_area_info(cur_pos.x, cur_pos.z)
        self.send_event('E_CALL_SYNC_METHOD', 'item_use_do', (item_id, area_id, extra_data), False, True, True)

    def _sync_cancel_use(self, item_id):
        self.send_event('E_CALL_SYNC_METHOD', 'item_use_cancel', (item_id,), False, False, False)

    def _register_drug_use_cancel_event(self):
        if self.is_register_drug_use_event:
            return
        self.is_register_drug_use_event = True
        self._start_use_pos = self.ev_g_position()
        regist_event = self.regist_event
        regist_event('E_TRY_FIRE', self.item_use_interrupt_helper)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.item_use_move_helper)
        else:
            regist_event('E_POSITION', self.item_use_move_helper)
        regist_event('E_START_FIRE_ROCKER', self.item_use_interrupt_helper)
        regist_event('E_START_AUTO_FIRE', self.item_use_interrupt_helper)
        regist_event('E_TRY_AIM', self.item_use_interrupt_helper)
        regist_event('E_TRY_SWITCH', self.item_use_try_switch_helper)
        regist_event('E_TRY_RELOAD', self.item_use_interrupt_helper)
        regist_event('E_TRY_SWITCH_DOOR_STATE', self.item_use_interrupt_helper)
        regist_event('E_DEATH', self.item_use_interrupt_helper)
        regist_event('E_AGONY', self.item_use_interrupt_helper)
        regist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
        regist_event('E_ON_LEAVE_MECHA_START', self.item_use_interrupt_helper)
        regist_event('E_CHANGE_PASSENGER', self.item_use_interrupt_helper)
        global_data.emgr.scene_pick_obj_event += self.item_use_interrupt_helper

    def _unregister_drug_use_cancel_event(self):
        if not self.is_register_drug_use_event:
            return
        else:
            self.is_register_drug_use_event = False
            self._start_use_pos = None
            unregist_event = self.unregist_event
            unregist_event('E_TRY_FIRE', self.item_use_interrupt_helper)
            if G_POS_CHANGE_MGR:
                self.unregist_pos_change(self.item_use_move_helper)
            else:
                unregist_event('E_POSITION', self.item_use_move_helper)
            unregist_event('E_START_FIRE_ROCKER', self.item_use_interrupt_helper)
            unregist_event('E_START_AUTO_FIRE', self.item_use_interrupt_helper)
            unregist_event('E_TRY_AIM', self.item_use_interrupt_helper)
            unregist_event('E_TRY_SWITCH', self.item_use_try_switch_helper)
            unregist_event('E_TRY_RELOAD', self.item_use_interrupt_helper)
            unregist_event('E_TRY_SWITCH_DOOR_STATE', self.item_use_interrupt_helper)
            unregist_event('E_DEATH', self.item_use_interrupt_helper)
            unregist_event('E_AGONY', self.item_use_interrupt_helper)
            unregist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
            unregist_event('E_ON_LEAVE_MECHA_START', self.item_use_interrupt_helper)
            unregist_event('E_CHANGE_PASSENGER', self.item_use_interrupt_helper)
            global_data.emgr.scene_pick_obj_event -= self.item_use_interrupt_helper
            return

    def item_use_try_switch_helper(self, weapon_pos, switch_status=True, is_init=False):
        if switch_status:
            self._interrupt_drug_use()

    def item_use_move_helper(self, new_pos, interrupt_dist=30):
        control_target = self.ev_g_control_target()
        if not control_target:
            return
        target_type = control_target.logic.__class__.__name__
        if target_type != 'LMechaTrans' and target_type != 'LMotorcycle':
            return
        if target_type == 'LMechaTrans' and control_target.logic.ev_g_shape_shift():
            return
        if not self.is_register_drug_use_event:
            return
        if not self._cur_singing_id:
            return
        if self._start_use_pos:
            if (new_pos - self._start_use_pos).length > interrupt_dist:
                self._interrupt_drug_use()
        else:
            self._start_use_pos = new_pos

    def item_use_interrupt_helper(self, *arg, **kwargs):
        self._interrupt_drug_use()

    def _interrupt_drug_use(self):
        if self._cur_singing_id:
            self.send_event('E_ITEMUSE_CANCEL', self._cur_singing_id)

    def restore_from_reconnect(self, last_sing_id, last_try_time):
        if not last_sing_id or not last_try_time:
            return
        from logic.gcommon.time_utility import time
        passed_time = time() - last_try_time
        self._on_try_success(last_sing_id, passed_time)

    def on_item_data_changed(self, item_data):
        if self._cur_singing_id:
            count = self.ev_g_item_count(self._cur_singing_id)
            if count <= 0:
                self._interrupt_drug_use()
                return False

    def _check_below_item_limit(self, item_id):
        conf = item_conf.get_use_by_id(item_id)
        if conf:
            iUseLimit = conf.get('iUseLimit')
            if not iUseLimit or item_id not in self._use_item_limit:
                return True
            return self._use_item_limit.get(item_id) > 0

    def set_elasticity_use_cd(self, elasticity_use_cd):
        self._elasticity_use_cd = elasticity_use_cd

    def get_elasticity_use_cd(self, npc_eid):
        return self._elasticity_use_cd

    def _clear_item_use_status(self):
        self._cur_singing_id = 0
        self.last_try_time = None
        self._use_item_cd = {}
        self._use_item_limit = {}
        self._elasticity_use_cd = 0
        return