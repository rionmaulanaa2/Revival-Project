# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/EntityManager.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from ..mobilelog.LogManager import LogManager
from .mobilecommon import singleton
from .IdManager import IdManager

def _static(*args, **kwargs):
    return False


def _dynamic(*args, **kwargs):
    return True


def Dynamic(klass):
    klass.is_dynamic = _dynamic
    return klass


class EntityIdOrLocalId(object):
    entityid_localids = {}
    localid_entityids = {}
    localid_sync = set()

    @staticmethod
    def clear():
        EntityIdOrLocalId.entityid_localids = {}
        EntityIdOrLocalId.localid_entityids = {}
        EntityIdOrLocalId.localid_sync.clear()

    @staticmethod
    def clear_localid_sync(entityid):
        EntityIdOrLocalId.localid_sync.discard(entityid)

    @staticmethod
    def set_entityid_localid(entityid, localid):
        if localid > 0:
            EntityIdOrLocalId.entityid_localids[entityid] = localid
            EntityIdOrLocalId.localid_entityids[localid] = entityid

    @staticmethod
    def raw_encode--- This code section failed: ---

  54       0  LOAD_GLOBAL           0  'EntityIdOrLocalId'
           3  LOAD_ATTR             1  'entityid_localids'
           6  LOAD_ATTR             2  'get'
           9  LOAD_ATTR             1  'entityid_localids'
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'localid'

  55      18  LOAD_FAST             1  'localid'
          21  LOAD_CONST            1  -1
          24  COMPARE_OP            2  '=='
          27  POP_JUMP_IF_FALSE    40  'to 40'

  56      30  LOAD_FAST             0  'entityid'
          33  LOAD_FAST             1  'localid'
          36  BUILD_TUPLE_2         2 
          39  RETURN_END_IF    
        40_0  COME_FROM                '27'

  58      40  LOAD_FAST             0  'entityid'
          43  LOAD_GLOBAL           0  'EntityIdOrLocalId'
          46  LOAD_ATTR             3  'localid_sync'
          49  COMPARE_OP            6  'in'
          52  POP_JUMP_IF_FALSE    61  'to 61'
          55  LOAD_CONST            2  ''
          58  JUMP_FORWARD          3  'to 64'
          61  LOAD_FAST             0  'entityid'
        64_0  COME_FROM                '58'
          64  STORE_FAST            2  'reteid'

  59      67  LOAD_FAST             2  'reteid'
          70  LOAD_FAST             1  'localid'
          73  BUILD_TUPLE_2         2 
          76  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

    @staticmethod
    def raw_decode--- This code section failed: ---

  63       0  LOAD_FAST             1  'localid'
           3  LOAD_CONST            1  -1
           6  COMPARE_OP            2  '=='
           9  POP_JUMP_IF_FALSE    22  'to 22'

  64      12  LOAD_FAST             0  'entityid'
          15  LOAD_FAST             1  'localid'
          18  BUILD_TUPLE_2         2 
          21  RETURN_END_IF    
        22_0  COME_FROM                '9'

  65      22  LOAD_FAST             0  'entityid'
          25  LOAD_CONST            0  ''
          28  COMPARE_OP            8  'is'
          31  POP_JUMP_IF_TRUE     43  'to 43'
          34  POP_JUMP_IF_TRUE      2  'to 2'
          37  COMPARE_OP            2  '=='
        40_0  COME_FROM                '34'
        40_1  COME_FROM                '31'
          40  POP_JUMP_IF_FALSE    90  'to 90'

  66      43  LOAD_GLOBAL           1  'EntityIdOrLocalId'
          46  LOAD_ATTR             2  'localid_entityids'
          49  LOAD_ATTR             3  'get'
          52  LOAD_FAST             1  'localid'
          55  LOAD_CONST            2  ''
          58  CALL_FUNCTION_2       2 
          61  STORE_FAST            0  'entityid'

  67      64  LOAD_GLOBAL           1  'EntityIdOrLocalId'
          67  LOAD_ATTR             4  'localid_sync'
          70  LOAD_ATTR             5  'add'
          73  LOAD_FAST             0  'entityid'
          76  CALL_FUNCTION_1       1 
          79  POP_TOP          

  68      80  LOAD_FAST             0  'entityid'
          83  LOAD_FAST             1  'localid'
          86  BUILD_TUPLE_2         2 
          89  RETURN_END_IF    
        90_0  COME_FROM                '40'

  69      90  LOAD_GLOBAL           1  'EntityIdOrLocalId'
          93  LOAD_ATTR             2  'localid_entityids'
          96  LOAD_ATTR             3  'get'
          99  LOAD_FAST             1  'localid'
         102  LOAD_CONST            2  ''
         105  CALL_FUNCTION_2       2 
         108  STORE_FAST            0  'entityid'

  70     111  LOAD_FAST             0  'entityid'
         114  LOAD_FAST             1  'localid'
         117  BUILD_TUPLE_2         2 
         120  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 34

    @staticmethod
    def destroy--- This code section failed: ---

  74       0  SETUP_EXCEPT         19  'to 22'

  75       3  LOAD_GLOBAL           0  'IdManager'
           6  LOAD_ATTR             1  'id2bytes'
           9  LOAD_FAST             0  'entityid'
          12  CALL_FUNCTION_1       1 
          15  STORE_FAST            0  'entityid'
          18  POP_BLOCK        
          19  JUMP_FORWARD          8  'to 30'
        22_0  COME_FROM                '0'

  76      22  POP_TOP          
          23  POP_TOP          
          24  POP_TOP          

  77      25  LOAD_CONST            0  ''
          28  RETURN_VALUE     
          29  END_FINALLY      
        30_0  COME_FROM                '29'
        30_1  COME_FROM                '19'

  78      30  LOAD_GLOBAL           2  'EntityIdOrLocalId'
          33  LOAD_ATTR             3  'entityid_localids'
          36  LOAD_ATTR             4  'get'
          39  LOAD_ATTR             1  'id2bytes'
          42  CALL_FUNCTION_2       2 
          45  STORE_FAST            1  'localid'

  79      48  LOAD_FAST             1  'localid'
          51  LOAD_CONST            2  ''
          54  COMPARE_OP            4  '>'
          57  POP_JUMP_IF_FALSE   113  'to 113'

  80      60  SETUP_EXCEPT         40  'to 103'

  81      63  LOAD_GLOBAL           2  'EntityIdOrLocalId'
          66  LOAD_ATTR             5  'localid_sync'
          69  LOAD_ATTR             6  'discard'
          72  LOAD_FAST             0  'entityid'
          75  CALL_FUNCTION_1       1 
          78  POP_TOP          

  82      79  LOAD_GLOBAL           2  'EntityIdOrLocalId'
          82  LOAD_ATTR             3  'entityid_localids'
          85  LOAD_FAST             0  'entityid'
          88  DELETE_SUBSCR    

  83      89  LOAD_GLOBAL           2  'EntityIdOrLocalId'
          92  LOAD_ATTR             7  'localid_entityids'
          95  LOAD_FAST             1  'localid'
          98  DELETE_SUBSCR    
          99  POP_BLOCK        
         100  JUMP_ABSOLUTE       113  'to 113'
       103_0  COME_FROM                '60'

  84     103  POP_TOP          
         104  POP_TOP          
         105  POP_TOP          

  85     106  JUMP_ABSOLUTE       113  'to 113'
         109  END_FINALLY      
       110_0  COME_FROM                '109'
         110  JUMP_FORWARD          0  'to 113'
       113_0  COME_FROM                '110'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 42

    @staticmethod
    def decode--- This code section failed: ---

  89       0  LOAD_FAST             1  'localid'
           3  LOAD_CONST            1  -1
           6  COMPARE_OP            2  '=='
           9  POP_JUMP_IF_FALSE    22  'to 22'

  90      12  LOAD_FAST             0  'entityid'
          15  LOAD_FAST             1  'localid'
          18  BUILD_TUPLE_2         2 
          21  RETURN_END_IF    
        22_0  COME_FROM                '9'

  91      22  LOAD_FAST             0  'entityid'
          25  LOAD_CONST            0  ''
          28  COMPARE_OP            3  '!='
          31  POP_JUMP_IF_FALSE    72  'to 72'
          34  POP_JUMP_IF_FALSE     2  'to 2'
          37  COMPARE_OP            3  '!='
        40_0  COME_FROM                '31'
          40  POP_JUMP_IF_FALSE    72  'to 72'

  92      43  LOAD_FAST             1  'localid'
          46  LOAD_GLOBAL           1  'EntityIdOrLocalId'
          49  LOAD_ATTR             2  'entityid_localids'
          52  LOAD_FAST             0  'entityid'
          55  STORE_SUBSCR     

  93      56  LOAD_FAST             0  'entityid'
          59  LOAD_GLOBAL           1  'EntityIdOrLocalId'
          62  LOAD_ATTR             3  'localid_entityids'
          65  LOAD_FAST             1  'localid'
          68  STORE_SUBSCR     
          69  JUMP_FORWARD          0  'to 72'
        72_0  COME_FROM                '69'

  94      72  LOAD_GLOBAL           1  'EntityIdOrLocalId'
          75  LOAD_ATTR             3  'localid_entityids'
          78  LOAD_ATTR             4  'get'
          81  LOAD_FAST             1  'localid'
          84  LOAD_FAST             0  'entityid'
          87  CALL_FUNCTION_2       2 
          90  LOAD_FAST             1  'localid'
          93  BUILD_TUPLE_2         2 
          96  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 34

    @staticmethod
    def encode--- This code section failed: ---

  98       0  LOAD_GLOBAL           0  'EntityIdOrLocalId'
           3  LOAD_ATTR             1  'entityid_localids'
           6  LOAD_ATTR             2  'get'
           9  LOAD_ATTR             1  'entityid_localids'
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'localid'

  99      18  LOAD_FAST             1  'localid'
          21  LOAD_CONST            1  -1
          24  COMPARE_OP            2  '=='
          27  POP_JUMP_IF_FALSE    37  'to 37'

 100      30  POP_JUMP_IF_FALSE     1  'to 1'
          33  BUILD_TUPLE_2         2 
          36  RETURN_END_IF    
        37_0  COME_FROM                '30'
        37_1  COME_FROM                '27'

 101      37  LOAD_CONST            2  ''
          40  LOAD_FAST             1  'localid'
          43  BUILD_TUPLE_2         2 
          46  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12


@singleton
class EntityMark(object):

    def __init__(self):
        self.is_entity_mark = True

    def tick(self, *args):
        pass


ENTITY_MARK = EntityMark()

class EntityManager(object):
    _logger = LogManager.get_logger('server.EntityManager')
    _entities = {}
    _update_entities = {}
    _add_update_entity_marks = set()
    _del_update_entity_marks = set()
    _entitySetChangeListener = None
    _editEntityKey = None
    _edit_entities = {}

    @staticmethod
    def entitynumber(dt):
        return len(EntityManager._entities)

    @staticmethod
    def hasentity(entityid):
        return entityid in EntityManager._entities

    @staticmethod
    def getentity(entityid):
        return EntityManager._entities.get(entityid, None)

    @staticmethod
    def get_all_entity_keys():
        return six_ex.keys(EntityManager._entities)

    @staticmethod
    def setdynamic(entityid, flag):
        try:
            entity = EntityManager._entities[entityid]
            is_dynamic = entity.is_dynamic()
            if is_dynamic == flag:
                return
            if flag:
                entity.is_dynamic = _dynamic
                EntityManager._del_update_entity_marks.discard(entityid)
                EntityManager._add_update_entity_marks.add(entityid)
            else:
                entity.is_dynamic = _static
                EntityManager._del_update_entity_marks.add(entityid)
                EntityManager._add_update_entity_marks.discard(entityid)
        except:
            pass

    @staticmethod
    def delentity(entityid):
        if entityid in EntityManager._update_entities:
            EntityManager._update_entities[entityid] = ENTITY_MARK
            EntityManager._del_update_entity_marks.add(entityid)
        if entityid in EntityManager._add_update_entity_marks:
            EntityManager._add_update_entity_marks.remove(entityid)
        try:
            del EntityManager._entities[entityid]
        except KeyError:
            pass

        if global_data.use_sunshine:
            EntityManager.DelEntitySunshine(entityid)

    @staticmethod
    def addentity(entityid, entity, override=False):
        if entity.__class__.__name__ == 'Avatar':
            pass
        if entityid in EntityManager._entities:
            if not override:
                return
        EntityManager._entities[entityid] = entity
        if entity.is_dynamic():
            EntityManager._add_update_entity_marks.add(entityid)
        if global_data.use_sunshine:
            EntityManager.AddEntitySunshine(entityid, entity)

    @staticmethod
    def clear():
        for entity in six_ex.values(EntityManager._entities):
            entity.destroy()

        EntityManager._update_entities = {}
        EntityManager._add_update_entity_marks.clear()
        EntityManager._del_update_entity_marks.clear()
        EntityManager._editEntityKey = None
        EntityManager._edit_entities = {}
        return

    @staticmethod
    def get_entities_by_type(ent_type):
        target_ents = {}
        for e_id, ent in six.iteritems(EntityManager._entities):
            if ent.__class__.__name__ == ent_type:
                target_ents[e_id] = ent

        return target_ents

    @staticmethod
    def AddEntitySunshine(eid, entity, *args):
        from sunshine.SunshineSDK.Meta import ClassMetaManager
        if EntityManager._entitySetChangeListener:
            objMeta = ClassMetaManager.GetClassMeta(entity.__class__.__name__)
            if not objMeta:
                return
            data = objMeta.SerializeData(entity)
            EntityManager._edit_entities[eid] = entity
            if 'Edit' not in data:
                editComponent = EntityManager.GetEntityEditComponent(eid)
                if editComponent is not None:
                    editComponent.SetEditName(entity.__class__.__name__)
                    data['Edit'] = editComponent.ConvertToDict()
            print('Sunshine-----addentity type: ', entity.__class__.__name__, ' objMeta: ', objMeta, ' data: ', data)
            EntityManager._entitySetChangeListener.AddEntity(eid, data)
        return

    @staticmethod
    def DelEntitySunshine(eid):
        if eid in EntityManager._edit_entities:
            if EntityManager._editEntityKey == eid:
                firstKey = None
                for firstKey in EntityManager._edit_entities:
                    break

                EntityManager._editEntityKey = firstKey
                if EntityManager._entitySetChangeListener:
                    EntityManager._entitySetChangeListener.SetEditEntity(firstKey)
            if EntityManager._entitySetChangeListener:
                EntityManager._entitySetChangeListener.DelEntity(eid)
        return

    @staticmethod
    def AddEntitySetChangeListener(entitySetChangeListener):
        EntityManager._entitySetChangeListener = entitySetChangeListener

    @staticmethod
    def SetEditEntity(eid, triggerEvent=True):
        if eid in EntityManager._edit_entities:
            EntityManager._editEntityKey = eid
            if triggerEvent and EntityManager._entitySetChangeListener:
                EntityManager._entitySetChangeListener.SetEditEntity(eid)

    @staticmethod
    def GetEntityEditComponent(eid):
        entity = EntityManager.getentity(eid)
        if not entity:
            return None
        else:
            return EntityManager.GetEntityEditComponentFromEntity(entity)

    @staticmethod
    def GetEntityEditComponentFromEntity--- This code section failed: ---

 295       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('Class2EditClass', 'EntityEditComponent')
           6  IMPORT_NAME           0  'sunshine.Editor.Component.EntityEditComponent'
           9  IMPORT_FROM           1  'Class2EditClass'
          12  STORE_FAST            1  'Class2EditClass'
          15  IMPORT_FROM           2  'EntityEditComponent'
          18  STORE_FAST            2  'EntityEditComponent'
          21  POP_TOP          

 297      22  LOAD_GLOBAL           3  'getattr'
          25  LOAD_GLOBAL           3  'getattr'
          28  LOAD_CONST            0  ''
          31  CALL_FUNCTION_3       3 
          34  STORE_FAST            3  'editComponent'

 298      37  LOAD_FAST             3  'editComponent'
          40  POP_JUMP_IF_FALSE    47  'to 47'

 299      43  LOAD_FAST             3  'editComponent'
          46  RETURN_END_IF    
        47_0  COME_FROM                '40'

 301      47  LOAD_FAST             1  'Class2EditClass'
          50  LOAD_ATTR             5  'get'
          53  LOAD_GLOBAL           6  'type'
          56  LOAD_FAST             0  'entity'
          59  CALL_FUNCTION_1       1 
          62  CALL_FUNCTION_1       1 
          65  STORE_FAST            4  'editCls'

 302      68  LOAD_FAST             4  'editCls'
          71  LOAD_CONST            0  ''
          74  COMPARE_OP            8  'is'
          77  POP_JUMP_IF_FALSE    89  'to 89'

 303      80  LOAD_FAST             2  'EntityEditComponent'
          83  STORE_FAST            4  'editCls'
          86  JUMP_FORWARD          0  'to 89'
        89_0  COME_FROM                '86'

 305      89  LOAD_FAST             4  'editCls'
          92  LOAD_FAST             0  'entity'
          95  CALL_FUNCTION_1       1 
          98  STORE_FAST            3  'editComponent'

 306     101  LOAD_FAST             3  'editComponent'
         104  LOAD_FAST             0  'entity'
         107  STORE_ATTR            7  '_editComponent'

 307     110  LOAD_FAST             3  'editComponent'
         113  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 31


class EntitySetChangeListener(object):

    def AddEntity(self, eid, data, addUndoState=False):
        raise NotImplementedError

    def DelEntity(self, eid):
        raise NotImplementedError

    def SetEditEntity(self, eid):
        raise NotImplementedError