# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/Armor.py
from __future__ import absolute_import
import six
from ..item import item_utility as iutil
from .BaseDataType import BaseDataType
from logic.gcommon import time_utility as tutil

class Armor(BaseDataType):

    def __init__(self, data):
        super(Armor, self).__init__()
        self._data = data
        self._dress_pos = None
        self._conf = {}
        self._skill_set = set()
        self.init()
        return

    def init(self):
        if 'iDur' not in self._data:
            init_dur = self.conf('iDur')
            self.set_max_dur(init_dur)
            self.set_dur(init_dur)
        if 'iRecoverRatio' not in self._data:
            self._data['iRecoverRatio'] = self.conf('iRecoverRatio', 0)
            self._data['iRecoverDelay'] = self.conf('iRecoverDelay', 0)
            self._data['iMinValidDurAfterBroken'] = self.conf('iMinValidDurAfterBroken', 0)
        self._dress_pos = iutil.get_clothing_dress_pos(self.get_item_id())
        self._init_skills()

    def get_config(self):
        item_id = self.get_item_id()
        if G_IS_CLIENT:
            import common.cfg.confmgr as confmgr
            conf = confmgr.get('armor_config', str(item_id))
            return conf
        else:
            import data.armor_data as armor_data
            return armor_data.get_config_by_id(item_id)

        return {}

    def get_key_config_value(self, key, default=None):
        conf = self.get_config()
        if not conf:
            return default
        return conf.get(key, default)

    def conf(self, key, default=None):
        return self.get_key_config_value(key, default)

    def get_data(self):
        return self._data

    def get_item_id(self):
        return self._data.get('item_id')

    def get_entity_id(self):
        return self._data.get('entity_id')

    def get_dur(self):
        return self._data.get('iDur', 0)

    def get_attr(self, attr_name):
        return self.conf(attr_name, None)

    def get_fDmgReduce(self):
        return self.conf('fDmgReduce', 0)

    def get_fMeleeReduce(self):
        return self.conf('fMeleeReduce', 0)

    def get_mpSpecDmgReduce(self):
        return self.conf('mpSpecDmgReduce', 0)

    def get_fSpdRate(self):
        return self.conf('fSpdRate', 0)

    def get_fEffPitch(self):
        return self.conf('fEffPitch', 0)

    def get_fEffYaw(self):
        return self.conf('fEffYaw', 0)

    def get_fEffDistance(self):
        return self.conf('fEffDistance', 0)

    def set_dur(self, iDur):
        if iDur < 0:
            return
        self._data['iDur'] = iDur

    def set_max_dur(self, iDur):
        if iDur < 0:
            return
        self._data['iMaxDur'] = iDur

    def get_pos(self):
        return self._dress_pos

    def get_skill_set(self):
        return self._skill_set

    def sub_dur(self, i):
        self._data['iDur'] = self.get_dur() - int(i)
        if self._data['iDur'] < 0:
            self._data['iDur'] = 0
        return self._data['iDur']

    def repair(self):
        self._data['iDur'] = self.conf('iDur')

    def get_duration_percent(self):
        if self._data.get('recover_st', 0):
            cur_duration = self.get_recovering_hp(self._data, tutil.time())
        else:
            cur_duration = self._data['iDur']
        return float(cur_duration) / self.conf('iDur')

    def get_cur_dur(self):
        if self._data.get('recover_st', 0):
            cur_duration = self.get_recovering_hp(self._data, tutil.time())
        else:
            cur_duration = self._data['iDur']
        return cur_duration

    def get_max_dur(self):
        return self.conf('iDur')

    @staticmethod
    def start_recover--- This code section failed: ---

 165       0  LOAD_FAST             0  'data'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'iRecoverRatio'
           9  LOAD_CONST            2  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            2  'recover_ratio'

 166      18  LOAD_FAST             2  'recover_ratio'
          21  POP_JUMP_IF_TRUE     28  'to 28'

 167      24  LOAD_GLOBAL           1  'False'
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

 168      28  LOAD_FAST             0  'data'
          31  LOAD_ATTR             0  'get'
          34  LOAD_CONST            3  'recover_st'
          37  CALL_FUNCTION_1       1 
          40  LOAD_CONST            2  ''
          43  COMPARE_OP            4  '>'
          46  POP_JUMP_IF_TRUE     85  'to 85'
          49  LOAD_FAST             0  'data'
          52  LOAD_ATTR             0  'get'
          55  LOAD_CONST            4  'iDur'
          58  LOAD_CONST            2  ''
          61  CALL_FUNCTION_2       2 
          64  LOAD_FAST             0  'data'
          67  LOAD_ATTR             0  'get'
          70  LOAD_CONST            5  'iMaxDur'
          73  LOAD_CONST            2  ''
          76  CALL_FUNCTION_2       2 
          79  COMPARE_OP            5  '>='
        82_0  COME_FROM                '46'
          82  POP_JUMP_IF_FALSE    89  'to 89'

 169      85  LOAD_GLOBAL           1  'False'
          88  RETURN_END_IF    
        89_0  COME_FROM                '82'

 170      89  LOAD_FAST             1  't'
          92  LOAD_FAST             0  'data'
          95  LOAD_ATTR             0  'get'
          98  LOAD_CONST            6  'iRecoverDelay'
         101  LOAD_CONST            2  ''
         104  CALL_FUNCTION_2       2 
         107  BINARY_ADD       
         108  BINARY_ADD       
         109  PRINT_ITEM_TO    
         110  PRINT_ITEM_TO    
         111  STORE_SUBSCR     

 171     112  LOAD_GLOBAL           2  'True'
         115  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_ADD' instruction at offset 108

    @staticmethod
    def stop_recover--- This code section failed: ---

 176       0  LOAD_FAST             0  'data'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'iRecoverRatio'
           9  LOAD_CONST            2  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            3  'recover_ratio'

 177      18  LOAD_FAST             3  'recover_ratio'
          21  POP_JUMP_IF_TRUE     28  'to 28'

 178      24  LOAD_GLOBAL           1  'False'
          27  RETURN_END_IF    
        28_0  COME_FROM                '21'

 179      28  LOAD_FAST             0  'data'
          31  LOAD_ATTR             0  'get'
          34  LOAD_CONST            3  'recover_st'
          37  LOAD_CONST            2  ''
          40  CALL_FUNCTION_2       2 
          43  STORE_FAST            4  'recover_st'

 180      46  LOAD_FAST             4  'recover_st'
          49  POP_JUMP_IF_TRUE     56  'to 56'

 181      52  LOAD_GLOBAL           1  'False'
          55  RETURN_END_IF    
        56_0  COME_FROM                '49'

 182      56  LOAD_FAST             2  'cur_hp'
          59  POP_JUMP_IF_TRUE     83  'to 83'

 183      62  LOAD_GLOBAL           2  'Armor'
          65  LOAD_ATTR             3  'get_recovering_hp'
          68  LOAD_FAST             0  'data'
          71  LOAD_FAST             1  't'
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            2  'cur_hp'
          80  JUMP_FORWARD          0  'to 83'
        83_0  COME_FROM                '80'

 184      83  LOAD_FAST             2  'cur_hp'
          86  LOAD_FAST             4  'recover_st'
          89  STORE_SUBSCR     

 185      90  LOAD_FAST             0  'data'
          93  LOAD_ATTR             4  'pop'
          96  LOAD_CONST            3  'recover_st'
          99  LOAD_CONST            2  ''
         102  CALL_FUNCTION_2       2 
         105  POP_TOP          

 186     106  LOAD_GLOBAL           5  'True'
         109  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_SUBSCR' instruction at offset 89

    @staticmethod
    def get_sync_recover_data(data):
        sync_dict = {'iDur': data.get('iDur', 0),
           'recover_st': data.get('recover_st', 0)
           }
        return sync_dict

    @staticmethod
    def get_recovering_hp(data, t):
        recover_ratio = data.get('iRecoverRatio', 0)
        recover_st = data.get('recover_st', 0)
        last_hp = data.get('iDur', 1)
        if not recover_ratio or not recover_st:
            return last_hp
        max_hp = data.get('iMaxDur', 1)
        dt = max(0, t - recover_st - (0.5 if G_IS_CLIENT else 0))
        cur_hp = int(last_hp + dt * recover_ratio)
        if cur_hp < max_hp:
            return cur_hp
        return max_hp

    @staticmethod
    def can_be_equipped--- This code section failed: ---

 213       0  LOAD_CONST            1  'iDur'
           3  LOAD_FAST             0  'data'
           6  COMPARE_OP            7  'not-in'
           9  POP_JUMP_IF_FALSE    16  'to 16'

 214      12  LOAD_GLOBAL           0  'True'
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 215      16  RETURN_VALUE     
          17  RETURN_VALUE     
          18  RETURN_VALUE     
          19  BINARY_SUBSCR    
          20  LOAD_CONST            2  ''
          23  COMPARE_OP            4  '>'
          26  POP_JUMP_IF_FALSE    33  'to 33'

 216      29  LOAD_GLOBAL           0  'True'
          32  RETURN_END_IF    
        33_0  COME_FROM                '26'

 218      33  LOAD_GLOBAL           1  'Armor'
          36  LOAD_ATTR             2  'get_recovering_hp'
          39  LOAD_FAST             0  'data'
          42  LOAD_FAST             1  't'
          45  CALL_FUNCTION_2       2 
          48  STORE_FAST            2  'cur_hp'

 219      51  LOAD_FAST             0  'data'
          54  LOAD_ATTR             3  'get'
          57  LOAD_CONST            3  'iMinValidDurAfterBroken'
          60  LOAD_CONST            4  1
          63  CALL_FUNCTION_2       2 
          66  STORE_FAST            3  'min_valid_hp'

 220      69  LOAD_FAST             2  'cur_hp'
          72  LOAD_FAST             3  'min_valid_hp'
          75  COMPARE_OP            5  '>='
          78  POP_JUMP_IF_FALSE    85  'to 85'

 221      81  LOAD_GLOBAL           0  'True'
          84  RETURN_END_IF    
        85_0  COME_FROM                '78'

 222      85  LOAD_GLOBAL           4  'False'
          88  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 16

    @staticmethod
    def get_recovering_info(data, t):
        recover_st = data.get('recover_st', 0)
        cur_hp = Armor.get_recovering_hp(data, t)
        min_valid_hp = data.get('iMinValidDurAfterBroken', 1)
        max_hp = data.get('iMaxDur', 1)
        return (
         recover_st, data.get('iDur', 0) > 0 or cur_hp >= min_valid_hp, cur_hp, max_hp)

    def get_attachment_conf(self, attachment_id):
        if G_IS_CLIENT:
            import common.cfg.confmgr as confmgr
            conf = confmgr.get('exoskeleton_attachment', str(attachment_id))
            return conf
        else:
            import data.exoskeleton_attachment as exoskeleton_attachment
            return exoskeleton_attachment.get_config_by_id(str(attachment_id))

    def _init_skills(self):
        for att_id, att_data in six.iteritems(self._data.get('attachment', {})):
            conf = self.get_attachment_conf(att_data['item_id'])
            skill = conf.get('skill', 0)
            if skill > 0:
                self._skill_set.add(skill)