# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/framework.py
from __future__ import absolute_import
import six_ex
from functools import partial
import weakref
from copy import copy
import six

class SingletonBase(object):

    def __init__(self, *arg, **kwargs):
        pass

    def init(self):
        pass

    @classmethod
    def finalize--- This code section failed: ---

  25       0  LOAD_FAST             0  'cls'
           3  LOAD_ATTR             0  'get_instance'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            1  'inst'

  26      12  LOAD_FAST             1  'inst'
          15  POP_JUMP_IF_FALSE   121  'to 121'

  27      18  LOAD_FAST             1  'inst'
          21  LOAD_ATTR             1  'on_finalize'
          24  CALL_FUNCTION_0       0 
          27  POP_TOP          

  28      28  LOAD_GLOBAL           2  'global_data'
          31  LOAD_ATTR             3  'singleton_map'
          34  STORE_FAST            2  'smap'

  29      37  LOAD_GLOBAL           2  'global_data'
          40  LOAD_ATTR             4  'alias_map'
          43  STORE_FAST            3  'amap'

  30      46  LOAD_GLOBAL           5  'getattr'
          49  LOAD_GLOBAL           1  'on_finalize'
          52  LOAD_CONST            0  ''
          55  CALL_FUNCTION_3       3 
          58  STORE_FAST            4  'alias_name'

  31      61  LOAD_FAST             4  'alias_name'
          64  POP_JUMP_IF_FALSE   108  'to 108'

  32      67  LOAD_FAST             3  'amap'
          70  LOAD_FAST             4  'alias_name'
          73  DELETE_SUBSCR    

  33      74  LOAD_FAST             4  'alias_name'
          77  LOAD_GLOBAL           2  'global_data'
          80  LOAD_ATTR             7  '__dict__'
          83  COMPARE_OP            6  'in'
          86  POP_JUMP_IF_FALSE   108  'to 108'

  34      89  LOAD_GLOBAL           8  'delattr'
          92  LOAD_GLOBAL           2  'global_data'
          95  LOAD_FAST             4  'alias_name'
          98  CALL_FUNCTION_2       2 
         101  POP_TOP          
         102  JUMP_ABSOLUTE       108  'to 108'
         105  JUMP_FORWARD          0  'to 108'
       108_0  COME_FROM                '105'

  36     108  LOAD_FAST             2  'smap'
         111  LOAD_FAST             0  'cls'
         114  LOAD_ATTR             9  '__name__'
         117  DELETE_SUBSCR    
         118  JUMP_FORWARD          0  'to 121'
       121_0  COME_FROM                '118'
         121  LOAD_CONST            0  ''
         124  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 55

    def on_finalize(self):
        pass

    def __new__--- This code section failed: ---

  42       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'singleton_map'
           6  STORE_FAST            3  'smap'

  43       9  LOAD_GLOBAL           0  'global_data'
          12  LOAD_ATTR             2  'alias_map'
          15  STORE_FAST            4  'amap'

  44      18  LOAD_FAST             3  'smap'
          21  LOAD_ATTR             3  'get'
          24  LOAD_FAST             0  'cls'
          27  LOAD_ATTR             4  '__name__'
          30  LOAD_CONST            0  ''
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            5  'inst'

  46      39  LOAD_FAST             5  'inst'
          42  LOAD_CONST            0  ''
          45  COMPARE_OP            8  'is'
          48  POP_JUMP_IF_FALSE   141  'to 141'

  47      51  LOAD_GLOBAL           6  'object'
          54  LOAD_ATTR             7  '__new__'
          57  LOAD_FAST             0  'cls'
          60  CALL_FUNCTION_1       1 
          63  STORE_FAST            5  'inst'

  48      66  LOAD_FAST             5  'inst'
          69  LOAD_FAST             3  'smap'
          72  LOAD_FAST             0  'cls'
          75  LOAD_ATTR             4  '__name__'
          78  STORE_SUBSCR     

  49      79  LOAD_GLOBAL           8  'getattr'
          82  LOAD_GLOBAL           1  'singleton_map'
          85  LOAD_CONST            0  ''
          88  CALL_FUNCTION_3       3 
          91  STORE_FAST            6  'alias_name'

  50      94  LOAD_FAST             6  'alias_name'
          97  POP_JUMP_IF_FALSE   113  'to 113'

  51     100  LOAD_FAST             5  'inst'
         103  LOAD_FAST             4  'amap'
         106  LOAD_FAST             6  'alias_name'
         109  STORE_SUBSCR     
         110  JUMP_FORWARD          0  'to 113'
       113_0  COME_FROM                '110'

  52     113  LOAD_FAST             5  'inst'
         116  LOAD_ATTR             9  'init'
         119  LOAD_FAST             1  'args'
         122  LOAD_FAST             2  'kwargs'
         125  CALL_FUNCTION_VAR_KW_0     0 
         128  POP_TOP          

  53     129  LOAD_GLOBAL          10  'True'
         132  LOAD_FAST             5  'inst'
         135  STORE_ATTR           11  '_is_new_instance'
         138  JUMP_FORWARD          9  'to 150'

  56     141  LOAD_GLOBAL          12  'False'
         144  LOAD_FAST             5  'inst'
         147  STORE_ATTR           11  '_is_new_instance'
       150_0  COME_FROM                '138'

  58     150  LOAD_FAST             5  'inst'
         153  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 88

    @classmethod
    def get_instance(cls):
        smap = global_data.singleton_map
        return smap.get(cls.__name__, None)


class Singleton(SingletonBase):

    def __new__(cls, *args, **kwargs):
        inst = SingletonBase.__new__(cls, *args, **kwargs)
        if inst._is_new_instance:
            inst._is_new_instance = False
        return inst


class Swallower(object):

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __add__(self, other):
        return 0

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        return 1

    def __div__(self, other):
        return 1


class NonexistentSwallower(Swallower):

    def __nonzero__(self):
        return False


class ArgObj(object):

    def __init__(self, **kwargs):
        super(ArgObj, self).__init__()
        self.from_dict(kwargs)

    def __contains__(self, key):
        return hasattr(self, str(key))

    def __getitem__(self, key):
        return getattr(self, str(key))

    def __delitem__(self, key):
        del self.__dict__[key]

    def __setitem__(self, key, value):
        setattr(self, str(key), value)

    def keys(self):
        return six_ex.keys(self.__dict__)

    def values(self):
        return six_ex.values(self.__dict__)

    def update(self, obj):
        if isinstance(obj, dict):
            self.__dict__.update(obj)
        elif isinstance(obj, ArgObj):
            self.__dict__.update(obj.to_dict())
        else:
            raise 'ArgObj not know how to update?? %s' % repr(obj)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def pop(self, key):
        if key in self.__dict__:
            self.__dict__.pop(key)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __cmp__(self, other):
        is_equal = 0
        if other is None:
            return -1
        else:
            if len(self.__dict__) != len(other.__dict__):
                is_equal = -1
                return is_equal
            for k, v in six.iteritems(self.__dict__):
                v2 = other.__dict__.get(k)
                if v != v2:
                    is_equal = -1
                    break

            return is_equal

    def iteritems(self):
        return six.iteritems(self.__dict__)

    def items(self):
        return six_ex.items(self.__dict__)

    def from_dict(self, d):
        for k, v in six.iteritems(d):
            if isinstance(v, dict):
                o = ArgObj()
                o.from_dict(v)
                setattr(self, k, o)
            else:
                setattr(self, k, v)

    def to_dict(self):
        _d = self.__dict__
        ret = {}
        for k, v in six.iteritems(_d):
            if isinstance(v, ArgObj):
                ret[k] = v.to_dict()
            else:
                ret[k] = v

        return ret

    def copy(self):
        return ArgObj(**self.to_dict())


Functor = partial

class FastFunctor(object):

    def __init__(self, fn, *args, **kwargs):
        super(FastFunctor, self).__init__()
        self.fn = partial(fn, *args, **kwargs)

    def __call__(self, *args):
        return self.fn()


class WeakMethod2(object):
    REF_TYPE_NORMAL = 1
    REF_TYPE_SINGLETON = 2
    REF_TYPE_CC_NODE = 3

    def __init__(self, item, callback=None):
        self.method = None
        self.instance = None
        self.reference = None
        self.deleted = False
        im_func = getattr(item, six._meth_func, None)
        im_self = getattr(item, six._meth_self, None)
        if callback:
            release_callback = partial(callback, self)
        else:
            release_callback = None
        if im_func and im_self:
            from common.uisys.uielment.CCNode import CCNode
            import cc
            self.method = weakref.ref(im_func)
            self.instance = weakref.ref(im_self, release_callback)
            if isinstance(self.instance(), Singleton):
                self.ref_type = self.REF_TYPE_SINGLETON
            elif isinstance(self.instance(), (CCNode, cc.Node)):
                self.ref_type = self.REF_TYPE_CC_NODE
            else:
                self.ref_type = self.REF_TYPE_NORMAL
        else:
            self.reference = weakref.ref(item, release_callback)
        return

    def release(self):
        self.deleted = True
        self.reference = None
        self.instance = None
        self.method = None
        return

    def __str__(self):
        if self.deleted:
            return 'deleted handler'
        else:
            if self.reference:
                return str(self.reference())
            return 'rinst:%s, func: %s' % (str(self.instance()), str(self.method()))

    def __call__(self, *args, **keywargs):
        if self.reference:
            func = self.reference()
            if not func:
                return None
            return func(*args, **keywargs)
        else:
            if not self.instance or not self.method:
                return None
            inst = self.instance()
            func = self.method()
            if not inst or not func:
                return None
            if self.ref_type == self.REF_TYPE_SINGLETON:
                robj = inst.get_instance()
                if robj is not inst:
                    return None
            elif self.ref_type == self.REF_TYPE_CC_NODE:
                if not inst.isValid():
                    return None
            return func(inst, *args, **keywargs)
            return None

    def is_valid(self):
        if self.deleted:
            return False
        else:
            if self.reference:
                func = self.reference()
                if not func:
                    return False
                return True
            if not self.instance or not self.method:
                return False
            inst = self.instance()
            func = self.method()
            if not inst or not func:
                return False
            if self.ref_type == self.REF_TYPE_SINGLETON:
                robj = inst.get_instance()
                if robj is not inst:
                    return False
            elif self.ref_type == self.REF_TYPE_CC_NODE:
                if not inst.isValid():
                    return False
            return True

    def __ne__(self, item):
        return not self == item

    def __eq__(self, item):
        if item is None:
            return not self.is_valid()
        else:
            if self.reference:
                func = self.reference()
                if isinstance(item, WeakMethod2) and item.reference:
                    item_func = item.reference()
                    return item_func is func
                return func is item
            im_func = getattr(item, 'im_func', None)
            im_self = getattr(item, 'im_self', None)
            inst = self.instance()
            func = self.method()
            return im_func is func and inst is im_self
            return