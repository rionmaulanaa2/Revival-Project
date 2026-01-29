# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/lib/collections_org.py
__all__ = ['Counter', 'deque', 'defaultdict', 'namedtuple', 'OrderedDict']
from _abcoll import *
import _abcoll
__all__ += _abcoll.__all__
from _collections import deque, defaultdict
from operator import itemgetter as _itemgetter, eq as _eq
from keyword import iskeyword as _iskeyword
import sys as _sys
import heapq as _heapq
from itertools import repeat as _repeat, chain as _chain, starmap as _starmap
from itertools import imap as _imap
try:
    from thread import get_ident as _get_ident
except ImportError:
    from dummy_thread import get_ident as _get_ident

class OrderedDict(dict):

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = []
            root[:] = [
             root, root, None]
            self.__map = {}

        self.__update(*args, **kwds)
        return

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        return dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        dict_delitem(self, key)
        link_prev, link_next, _ = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reversed__(self):
        root = self.__root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    def clear(self):
        root = self.__root
        root[:] = [root, root, None]
        self.__map.clear()
        dict.clear(self)
        return

    def keys(self):
        return list(self)

    def values(self):
        return [ self[key] for key in self ]

    def items(self):
        return [ (key, self[key]) for key in self ]

    def iterkeys(self):
        return iter(self)

    def itervalues(self):
        for k in self:
            yield self[k]

    def iteritems(self):
        for k in self:
            yield (k, self[k])

    update = MutableMapping.update
    __update = update
    __marker = object()

    def pop(self, key, default=__marker):
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return default

    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        key = next(reversed(self) if last else iter(self))
        value = self.pop(key)
        return (
         key, value)

    def __repr__(self, _repr_running={}):
        call_key = (
         id(self), _get_ident())
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())
        finally:
            del _repr_running[call_key]

    def __reduce__(self):
        items = [ [k, self[k]] for k in self ]
        inst_dict = vars(self).copy()
        for k in vars(OrderedDict()):
            inst_dict.pop(k, None)

        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        else:
            return (
             self.__class__, (items,))

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        self = cls()
        for key in iterable:
            self[key] = value

        return self

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(_imap(_eq, self, other))
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

    def viewkeys(self):
        return KeysView(self)

    def viewvalues(self):
        return ValuesView(self)

    def viewitems(self):
        return ItemsView(self)


_class_template = "class {typename}(tuple):\n    '{typename}({arg_list})'\n\n    __slots__ = ()\n\n    _fields = {field_names!r}\n\n    def __new__(_cls, {arg_list}):\n        'Create new instance of {typename}({arg_list})'\n        return _tuple.__new__(_cls, ({arg_list}))\n\n    @classmethod\n    def _make(cls, iterable, new=tuple.__new__, len=len):\n        'Make a new {typename} object from a sequence or iterable'\n        result = new(cls, iterable)\n        if len(result) != {num_fields:d}:\n            raise TypeError('Expected {num_fields:d} arguments, got %d' % len(result))\n        return result\n\n    def __repr__(self):\n        'Return a nicely formatted representation string'\n        return '{typename}({repr_fmt})' % self\n\n    def _asdict(self):\n        'Return a new OrderedDict which maps field names to their values'\n        return OrderedDict(zip(self._fields, self))\n\n    def _replace(_self, **kwds):\n        'Return a new {typename} object replacing specified fields with new values'\n        result = _self._make(map(kwds.pop, {field_names!r}, _self))\n        if kwds:\n            raise ValueError('Got unexpected field names: %r' % kwds.keys())\n        return result\n\n    def __getnewargs__(self):\n        'Return self as a plain tuple.  Used by copy and pickle.'\n        return tuple(self)\n\n    __dict__ = _property(_asdict)\n\n    def __getstate__(self):\n        'Exclude the OrderedDict from pickling'\n        pass\n\n{field_defs}\n"
_repr_template = '{name}=%r'
_field_template = "    {name} = _property(_itemgetter({index:d}), doc='Alias for field number {index:d}')\n"

def namedtuple--- This code section failed: ---

 314       0  LOAD_NAME             0  'isinstance'
           3  LOAD_FAST             1  'field_names'
           6  LOAD_NAME             1  'basestring'
           9  CALL_FUNCTION_2       2 
          12  POP_JUMP_IF_FALSE    42  'to 42'

 315      15  LOAD_FAST             1  'field_names'
          18  LOAD_ATTR             2  'replace'
          21  LOAD_CONST            1  ','
          24  LOAD_CONST            2  ' '
          27  CALL_FUNCTION_2       2 
          30  LOAD_ATTR             3  'split'
          33  CALL_FUNCTION_0       0 
          36  STORE_FAST            1  'field_names'
          39  JUMP_FORWARD          0  'to 42'
        42_0  COME_FROM                '39'

 316      42  LOAD_NAME             4  'map'
          45  LOAD_NAME             5  'str'
          48  LOAD_FAST             1  'field_names'
          51  CALL_FUNCTION_2       2 
          54  STORE_FAST            1  'field_names'

 317      57  LOAD_NAME             5  'str'
          60  LOAD_FAST             0  'typename'
          63  CALL_FUNCTION_1       1 
          66  STORE_FAST            0  'typename'

 318      69  LOAD_FAST             3  'rename'
          72  POP_JUMP_IF_FALSE   231  'to 231'

 319      75  LOAD_NAME             6  'set'
          78  CALL_FUNCTION_0       0 
          81  STORE_FAST            4  'seen'

 320      84  SETUP_LOOP          144  'to 231'
          87  LOAD_NAME             7  'enumerate'
          90  LOAD_FAST             1  'field_names'
          93  CALL_FUNCTION_1       1 
          96  GET_ITER         
          97  FOR_ITER            127  'to 227'
         100  UNPACK_SEQUENCE_2     2 
         103  STORE_FAST            5  'index'
         106  STORE_FAST            6  'name'

 321     109  LOAD_NAME             8  'all'
         112  LOAD_GENEXPR             '<code_object <genexpr>>'
         115  MAKE_FUNCTION_0       0 
         118  LOAD_FAST             6  'name'
         121  GET_ITER         
         122  CALL_FUNCTION_1       1 
         125  CALL_FUNCTION_1       1 
         128  UNARY_NOT        
         129  POP_JUMP_IF_TRUE    194  'to 194'

 322     132  LOAD_NAME             9  '_iskeyword'
         135  LOAD_FAST             6  'name'
         138  CALL_FUNCTION_1       1 
         141  POP_JUMP_IF_TRUE    194  'to 194'

 323     144  LOAD_FAST             6  'name'
         147  UNARY_NOT        
         148  POP_JUMP_IF_TRUE    194  'to 194'

 324     151  LOAD_FAST             6  'name'
         154  LOAD_CONST            4  ''
         157  BINARY_SUBSCR    
         158  LOAD_ATTR            10  'isdigit'
         161  CALL_FUNCTION_0       0 
         164  POP_JUMP_IF_TRUE    194  'to 194'

 325     167  LOAD_FAST             6  'name'
         170  LOAD_ATTR            11  'startswith'
         173  LOAD_CONST            5  '_'
         176  CALL_FUNCTION_1       1 
         179  POP_JUMP_IF_TRUE    194  'to 194'

 326     182  LOAD_FAST             6  'name'
         185  LOAD_FAST             4  'seen'
         188  COMPARE_OP            6  'in'
       191_0  COME_FROM                '179'
       191_1  COME_FROM                '164'
       191_2  COME_FROM                '148'
       191_3  COME_FROM                '141'
       191_4  COME_FROM                '129'
         191  POP_JUMP_IF_FALSE   211  'to 211'

 327     194  LOAD_CONST            6  '_%d'
         197  LOAD_FAST             5  'index'
         200  BINARY_MODULO    
         201  LOAD_FAST             1  'field_names'
         204  LOAD_FAST             5  'index'
         207  STORE_SUBSCR     
         208  JUMP_FORWARD          0  'to 211'
       211_0  COME_FROM                '208'

 328     211  LOAD_FAST             4  'seen'
         214  LOAD_ATTR            12  'add'
         217  LOAD_FAST             6  'name'
         220  CALL_FUNCTION_1       1 
         223  POP_TOP          
         224  JUMP_BACK            97  'to 97'
         227  POP_BLOCK        
       228_0  COME_FROM                '84'
         228  JUMP_FORWARD          0  'to 231'
       231_0  COME_FROM                '84'

 329     231  SETUP_LOOP          161  'to 395'
         234  LOAD_FAST             0  'typename'
         237  BUILD_LIST_1          1 
         240  LOAD_FAST             1  'field_names'
         243  BINARY_ADD       
         244  GET_ITER         
         245  FOR_ITER            146  'to 394'
         248  STORE_FAST            6  'name'

 330     251  LOAD_NAME            13  'type'
         254  LOAD_FAST             6  'name'
         257  CALL_FUNCTION_1       1 
         260  LOAD_NAME             5  'str'
         263  COMPARE_OP            3  '!='
         266  POP_JUMP_IF_FALSE   284  'to 284'

 331     269  LOAD_NAME            14  'TypeError'
         272  LOAD_CONST            7  'Type names and field names must be strings'
         275  CALL_FUNCTION_1       1 
         278  RAISE_VARARGS_1       1 
         281  JUMP_FORWARD          0  'to 284'
       284_0  COME_FROM                '281'

 332     284  LOAD_NAME             8  'all'
         287  LOAD_GENEXPR             '<code_object <genexpr>>'
         290  MAKE_FUNCTION_0       0 
         293  LOAD_FAST             6  'name'
         296  GET_ITER         
         297  CALL_FUNCTION_1       1 
         300  CALL_FUNCTION_1       1 
         303  POP_JUMP_IF_TRUE    325  'to 325'

 333     306  LOAD_NAME            15  'ValueError'
         309  LOAD_CONST            9  'Type names and field names can only contain alphanumeric characters and underscores: %r'

 334     312  LOAD_FAST             6  'name'
         315  BINARY_MODULO    
         316  CALL_FUNCTION_1       1 
         319  RAISE_VARARGS_1       1 
         322  JUMP_FORWARD          0  'to 325'
       325_0  COME_FROM                '322'

 335     325  LOAD_NAME             9  '_iskeyword'
         328  LOAD_FAST             6  'name'
         331  CALL_FUNCTION_1       1 
         334  POP_JUMP_IF_FALSE   356  'to 356'

 336     337  LOAD_NAME            15  'ValueError'
         340  LOAD_CONST           10  'Type names and field names cannot be a keyword: %r'

 337     343  LOAD_FAST             6  'name'
         346  BINARY_MODULO    
         347  CALL_FUNCTION_1       1 
         350  RAISE_VARARGS_1       1 
         353  JUMP_FORWARD          0  'to 356'
       356_0  COME_FROM                '353'

 338     356  LOAD_FAST             6  'name'
         359  LOAD_CONST            4  ''
         362  BINARY_SUBSCR    
         363  LOAD_ATTR            10  'isdigit'
         366  CALL_FUNCTION_0       0 
         369  POP_JUMP_IF_FALSE   245  'to 245'

 339     372  LOAD_NAME            15  'ValueError'
         375  LOAD_CONST           11  'Type names and field names cannot start with a number: %r'

 340     378  LOAD_FAST             6  'name'
         381  BINARY_MODULO    
         382  CALL_FUNCTION_1       1 
         385  RAISE_VARARGS_1       1 
         388  JUMP_BACK           245  'to 245'
         391  JUMP_BACK           245  'to 245'
         394  POP_BLOCK        
       395_0  COME_FROM                '231'

 341     395  LOAD_NAME             6  'set'
         398  CALL_FUNCTION_0       0 
         401  STORE_FAST            4  'seen'

 342     404  SETUP_LOOP           99  'to 506'
         407  LOAD_FAST             1  'field_names'
         410  GET_ITER         
         411  FOR_ITER             91  'to 505'
         414  STORE_FAST            6  'name'

 343     417  LOAD_FAST             6  'name'
         420  LOAD_ATTR            11  'startswith'
         423  LOAD_CONST            5  '_'
         426  CALL_FUNCTION_1       1 
         429  POP_JUMP_IF_FALSE   458  'to 458'
         432  LOAD_FAST             3  'rename'
         435  UNARY_NOT        
       436_0  COME_FROM                '429'
         436  POP_JUMP_IF_FALSE   458  'to 458'

 344     439  LOAD_NAME            15  'ValueError'
         442  LOAD_CONST           12  'Field names cannot start with an underscore: %r'

 345     445  LOAD_FAST             6  'name'
         448  BINARY_MODULO    
         449  CALL_FUNCTION_1       1 
         452  RAISE_VARARGS_1       1 
         455  JUMP_FORWARD          0  'to 458'
       458_0  COME_FROM                '455'

 346     458  LOAD_FAST             6  'name'
         461  LOAD_FAST             4  'seen'
         464  COMPARE_OP            6  'in'
         467  POP_JUMP_IF_FALSE   489  'to 489'

 347     470  LOAD_NAME            15  'ValueError'
         473  LOAD_CONST           13  'Encountered duplicate field name: %r'
         476  LOAD_FAST             6  'name'
         479  BINARY_MODULO    
         480  CALL_FUNCTION_1       1 
         483  RAISE_VARARGS_1       1 
         486  JUMP_FORWARD          0  'to 489'
       489_0  COME_FROM                '486'

 348     489  LOAD_FAST             4  'seen'
         492  LOAD_ATTR            12  'add'
         495  LOAD_FAST             6  'name'
         498  CALL_FUNCTION_1       1 
         501  POP_TOP          
         502  JUMP_BACK           411  'to 411'
         505  POP_BLOCK        
       506_0  COME_FROM                '404'

 351     506  LOAD_NAME            16  '_class_template'
         509  LOAD_ATTR            17  'format'
         512  LOAD_CONST           14  'typename'

 352     515  LOAD_CONST           15  'field_names'

 353     518  LOAD_NAME            18  'tuple'
         521  LOAD_FAST             1  'field_names'
         524  CALL_FUNCTION_1       1 
         527  LOAD_CONST           16  'num_fields'

 354     530  LOAD_NAME            19  'len'
         533  LOAD_FAST             1  'field_names'
         536  CALL_FUNCTION_1       1 
         539  LOAD_CONST           17  'arg_list'

 355     542  LOAD_NAME            20  'repr'
         545  LOAD_NAME            18  'tuple'
         548  LOAD_FAST             1  'field_names'
         551  CALL_FUNCTION_1       1 
         554  CALL_FUNCTION_1       1 
         557  LOAD_ATTR             2  'replace'
         560  LOAD_CONST           18  "'"
         563  LOAD_CONST           19  ''
         566  CALL_FUNCTION_2       2 
         569  LOAD_CONST           20  1
         572  LOAD_CONST           21  -1
         575  SLICE+3          
         576  LOAD_CONST           22  'repr_fmt'

 356     579  LOAD_CONST           23  ', '
         582  LOAD_ATTR            21  'join'
         585  LOAD_GENEXPR             '<code_object <genexpr>>'
         588  MAKE_FUNCTION_0       0 

 357     591  LOAD_FAST             1  'field_names'
         594  GET_ITER         
         595  CALL_FUNCTION_1       1 
         598  CALL_FUNCTION_1       1 
         601  LOAD_CONST           25  'field_defs'

 358     604  LOAD_CONST           26  '\n'
         607  LOAD_ATTR            21  'join'
         610  LOAD_GENEXPR             '<code_object <genexpr>>'
         613  MAKE_FUNCTION_0       0 

 359     616  LOAD_NAME             7  'enumerate'
         619  LOAD_FAST             1  'field_names'
         622  CALL_FUNCTION_1       1 
         625  GET_ITER         
         626  CALL_FUNCTION_1       1 
         629  CALL_FUNCTION_1       1 
         632  CALL_FUNCTION_1536  1536 
         635  STORE_FAST            7  'class_definition'

 361     638  LOAD_FAST             2  'verbose'
         641  POP_JUMP_IF_FALSE   652  'to 652'

 362     644  LOAD_FAST             7  'class_definition'
         647  PRINT_ITEM       
         648  PRINT_NEWLINE_CONT
         649  JUMP_FORWARD          0  'to 652'
       652_0  COME_FROM                '649'

 366     652  LOAD_NAME            22  'dict'
         655  LOAD_CONST           28  '_itemgetter'
         658  LOAD_NAME            23  '_itemgetter'
         661  LOAD_CONST           29  '__name__'
         664  LOAD_CONST           30  'namedtuple_%s'
         667  LOAD_FAST             0  'typename'
         670  BINARY_MODULO    
         671  LOAD_CONST           31  'OrderedDict'

 367     674  LOAD_NAME            24  'OrderedDict'
         677  LOAD_CONST           32  '_property'
         680  LOAD_NAME            25  'property'
         683  LOAD_CONST           33  '_tuple'
         686  LOAD_NAME            18  'tuple'
         689  CALL_FUNCTION_1280  1280 
         692  STORE_FAST            8  'namespace'

 368     695  SETUP_EXCEPT         12  'to 710'

 369     698  LOAD_FAST             7  'class_definition'
         701  LOAD_FAST             8  'namespace'
         704  DUP_TOP          
         705  EXEC_STMT        
         706  POP_BLOCK        
         707  JUMP_FORWARD         42  'to 752'
       710_0  COME_FROM                '695'

 370     710  DUP_TOP          
         711  LOAD_NAME            26  'SyntaxError'
         714  COMPARE_OP           10  'exception-match'
         717  POP_JUMP_IF_FALSE   751  'to 751'
         720  POP_TOP          
         721  STORE_FAST            9  'e'
         724  POP_TOP          

 371     725  LOAD_NAME            26  'SyntaxError'
         728  LOAD_FAST             9  'e'
         731  LOAD_ATTR            27  'message'
         734  LOAD_CONST           34  ':\n'
         737  BINARY_ADD       
         738  LOAD_FAST             7  'class_definition'
         741  BINARY_ADD       
         742  CALL_FUNCTION_1       1 
         745  RAISE_VARARGS_1       1 
         748  JUMP_FORWARD          1  'to 752'
         751  END_FINALLY      
       752_0  COME_FROM                '751'
       752_1  COME_FROM                '707'

 372     752  LOAD_FAST             8  'namespace'
         755  LOAD_FAST             0  'typename'
         758  BINARY_SUBSCR    
         759  STORE_FAST           10  'result'

 378     762  SETUP_EXCEPT         37  'to 802'

 379     765  LOAD_NAME            28  '_sys'
         768  LOAD_ATTR            29  '_getframe'
         771  LOAD_CONST           20  1
         774  CALL_FUNCTION_1       1 
         777  LOAD_ATTR            30  'f_globals'
         780  LOAD_ATTR            31  'get'
         783  LOAD_CONST           29  '__name__'
         786  LOAD_CONST           35  '__main__'
         789  CALL_FUNCTION_2       2 
         792  LOAD_FAST            10  'result'
         795  STORE_ATTR           32  '__module__'
         798  POP_BLOCK        
         799  JUMP_FORWARD         23  'to 825'
       802_0  COME_FROM                '762'

 380     802  DUP_TOP          
         803  LOAD_NAME            33  'AttributeError'
         806  LOAD_NAME            15  'ValueError'
         809  BUILD_TUPLE_2         2 
         812  COMPARE_OP           10  'exception-match'
         815  POP_JUMP_IF_FALSE   824  'to 824'
         818  POP_TOP          
         819  POP_TOP          
         820  POP_TOP          

 381     821  JUMP_FORWARD          1  'to 825'
         824  END_FINALLY      
       825_0  COME_FROM                '824'
       825_1  COME_FROM                '799'

 383     825  LOAD_FAST            10  'result'
         828  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1536' instruction at offset 632


class Counter(dict):

    def __init__(self, iterable=None, **kwds):
        super(Counter, self).__init__()
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        if n is None:
            return sorted(self.iteritems(), key=_itemgetter(1), reverse=True)
        else:
            return _heapq.nlargest(n, self.iteritems(), key=_itemgetter(1))

    def elements(self):
        return _chain.from_iterable(_starmap(_repeat, self.iteritems()))

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError('Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        if iterable is not None:
            if isinstance(iterable, Mapping):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count

                else:
                    super(Counter, self).update(iterable)
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1

        if kwds:
            self.update(kwds)
        return

    def subtract(self, iterable=None, **kwds):
        if iterable is not None:
            self_get = self.get
            if isinstance(iterable, Mapping):
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count

            else:
                for elem in iterable:
                    self[elem] = self_get(elem, 0) - 1

        if kwds:
            self.subtract(kwds)
        return

    def copy(self):
        return self.__class__(self)

    def __reduce__(self):
        return (
         self.__class__, (dict(self),))

    def __delitem__(self, elem):
        if elem in self:
            super(Counter, self).__delitem__(elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = count + other[elem]
            if newcount > 0:
                result[elem] = newcount

        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count

        return result

    def __sub__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount

        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = 0 - count

        return result

    def __or__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = other_count if count < other_count else count
            if newcount > 0:
                result[elem] = newcount

        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count

        return result

    def __and__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
            if newcount > 0:
                result[elem] = newcount

        return result


if __name__ == '__main__':
    from cPickle import loads, dumps
    Point = namedtuple('Point', 'x, y', True)
    p = Point(x=10, y=20)

    class Point(namedtuple('Point', 'x y')):
        __slots__ = ()

        @property
        def hypot(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5

        def __str__(self):
            return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)


    for p in (Point(3, 4), Point(14, 5 / 7.0)):
        print p

    class Point(namedtuple('Point', 'x y')):
        __slots__ = ()
        _make = classmethod(tuple.__new__)

        def _replace(self, _map=map, **kwds):
            return self._make(_map(kwds.get, ('x', 'y'), self))


    print Point(11, 22)._replace(x=100)
    Point3D = namedtuple('Point3D', Point._fields + ('z',))
    print Point3D.__doc__
    import doctest
    TestResults = namedtuple('TestResults', 'failed attempted')
    print TestResults(*doctest.testmod())