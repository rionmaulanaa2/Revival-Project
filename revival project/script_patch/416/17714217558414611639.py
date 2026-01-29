# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/cython/Cython/Shadow.py
from __future__ import absolute_import
__version__ = '0.25.1'
try:
    from __builtin__ import basestring
except ImportError:
    basestring = str

class _ArrayType(object):
    is_array = True
    subtypes = ['dtype']

    def __init__(self, dtype, ndim, is_c_contig=False, is_f_contig=False, inner_contig=False, broadcasting=None):
        self.dtype = dtype
        self.ndim = ndim
        self.is_c_contig = is_c_contig
        self.is_f_contig = is_f_contig
        self.inner_contig = inner_contig or is_c_contig or is_f_contig
        self.broadcasting = broadcasting

    def __repr__(self):
        axes = [
         ':'] * self.ndim
        if self.is_c_contig:
            axes[-1] = '::1'
        elif self.is_f_contig:
            axes[0] = '::1'
        return '%s[%s]' % (self.dtype, ', '.join(axes))


def index_type--- This code section failed: ---

  44       0  LOAD_CONST            1  'InvalidTypeSpecification'
           3  LOAD_GLOBAL           0  'Exception'
           6  BUILD_TUPLE_1         1 
           9  LOAD_CONST               '<code_object InvalidTypeSpecification>'
          12  MAKE_FUNCTION_0       0 
          15  CALL_FUNCTION_0       0 
          18  BUILD_CLASS      
          19  STORE_DEREF           0  'InvalidTypeSpecification'

  47      22  LOAD_CLOSURE          0  'InvalidTypeSpecification'
          28  LOAD_CONST               '<code_object verify_slice>'
          31  MAKE_CLOSURE_0        0 
          34  STORE_FAST            2  'verify_slice'

  53      37  LOAD_GLOBAL           1  'isinstance'
          40  LOAD_FAST             1  'item'
          43  LOAD_GLOBAL           2  'tuple'
          46  CALL_FUNCTION_2       2 
          49  POP_JUMP_IF_FALSE   232  'to 232'

  54      52  LOAD_CONST            0  ''
          55  STORE_FAST            3  'step_idx'

  55      58  SETUP_LOOP          118  'to 179'
          61  LOAD_GLOBAL           4  'enumerate'
          64  LOAD_FAST             1  'item'
          67  CALL_FUNCTION_1       1 
          70  GET_ITER         
          71  FOR_ITER            104  'to 178'
          74  UNPACK_SEQUENCE_2     2 
          77  STORE_FAST            4  'idx'
          80  STORE_FAST            5  's'

  56      83  LOAD_FAST             2  'verify_slice'
          86  LOAD_FAST             5  's'
          89  CALL_FUNCTION_1       1 
          92  POP_TOP          

  57      93  LOAD_FAST             5  's'
          96  LOAD_ATTR             5  'step'
          99  POP_JUMP_IF_FALSE   151  'to 151'
         102  LOAD_FAST             3  'step_idx'
         105  POP_JUMP_IF_TRUE    136  'to 136'
         108  LOAD_FAST             4  'idx'
         111  LOAD_CONST            4  ''
         114  LOAD_GLOBAL           6  'len'
         117  LOAD_FAST             1  'item'
         120  CALL_FUNCTION_1       1 
         123  LOAD_CONST            5  1
         126  BINARY_SUBTRACT  
         127  BUILD_TUPLE_2         2 
         130  COMPARE_OP            7  'not-in'
       133_0  COME_FROM                '105'
       133_1  COME_FROM                '99'
         133  POP_JUMP_IF_FALSE   151  'to 151'

  58     136  LOAD_DEREF            0  'InvalidTypeSpecification'

  59     139  LOAD_CONST            6  'Step may only be provided once, and only in the first or last dimension.'
         142  CALL_FUNCTION_1       1 
         145  RAISE_VARARGS_1       1 
         148  JUMP_FORWARD          0  'to 151'
       151_0  COME_FROM                '148'

  62     151  LOAD_FAST             5  's'
         154  LOAD_ATTR             5  'step'
         157  LOAD_CONST            5  1
         160  COMPARE_OP            2  '=='
         163  POP_JUMP_IF_FALSE    71  'to 71'

  63     166  LOAD_FAST             4  'idx'
         169  STORE_FAST            3  'step_idx'
         172  JUMP_BACK            71  'to 71'
         175  JUMP_BACK            71  'to 71'
         178  POP_BLOCK        
       179_0  COME_FROM                '58'

  65     179  LOAD_GLOBAL           7  '_ArrayType'
         182  LOAD_FAST             0  'base_type'
         185  LOAD_GLOBAL           6  'len'
         188  LOAD_FAST             1  'item'
         191  CALL_FUNCTION_1       1 
         194  LOAD_CONST            7  'is_c_contig'

  66     197  LOAD_FAST             3  'step_idx'
         200  LOAD_GLOBAL           6  'len'
         203  LOAD_FAST             1  'item'
         206  CALL_FUNCTION_1       1 
         209  LOAD_CONST            5  1
         212  BINARY_SUBTRACT  
         213  COMPARE_OP            2  '=='
         216  LOAD_CONST            8  'is_f_contig'

  67     219  LOAD_FAST             3  'step_idx'
         222  LOAD_CONST            4  ''
         225  COMPARE_OP            2  '=='
         228  CALL_FUNCTION_514   514 
         231  RETURN_END_IF    
       232_0  COME_FROM                '49'

  68     232  LOAD_GLOBAL           1  'isinstance'
         235  LOAD_FAST             1  'item'
         238  LOAD_GLOBAL           8  'slice'
         241  CALL_FUNCTION_2       2 
         244  POP_JUMP_IF_FALSE   282  'to 282'

  69     247  LOAD_FAST             2  'verify_slice'
         250  LOAD_FAST             1  'item'
         253  CALL_FUNCTION_1       1 
         256  POP_TOP          

  70     257  LOAD_GLOBAL           7  '_ArrayType'
         260  LOAD_GLOBAL           5  'step'
         263  LOAD_CONST            7  'is_c_contig'
         266  LOAD_GLOBAL           9  'bool'
         269  LOAD_FAST             1  'item'
         272  LOAD_ATTR             5  'step'
         275  CALL_FUNCTION_1       1 
         278  CALL_FUNCTION_258   258 
         281  RETURN_END_IF    
       282_0  COME_FROM                '244'

  74     282  LOAD_GLOBAL          10  'array'
         285  LOAD_FAST             0  'base_type'
         288  LOAD_FAST             1  'item'
         291  CALL_FUNCTION_2       2 
         294  POP_TOP          
         295  LOAD_CONST            0  ''
         298  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_258' instruction at offset 278


compiled = False
_Unspecified = object()

def _empty_decorator(x):
    return x


def locals():
    return _empty_decorator


def test_assert_path_exists(*paths):
    return _empty_decorator


def test_fail_if_path_exists(*paths):
    return _empty_decorator


class _EmptyDecoratorAndManager(object):

    def __call__(self, x):
        return x

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class _Optimization(object):
    pass


cclass = ccall = cfunc = _EmptyDecoratorAndManager()
returns = wraparound = boundscheck = initializedcheck = nonecheck = overflowcheck = embedsignature = cdivision = cdivision_warnings = always_allows_keywords = profile = linetrace = infer_type = unraisable_tracebacks = freelist = lambda arg: _EmptyDecoratorAndManager()
optimization = _Optimization()
overflowcheck.fold = optimization.use_switch = optimization.unpack_method_calls = lambda arg: _EmptyDecoratorAndManager()
final = internal = type_version_tag = no_gc_clear = no_gc = _empty_decorator
_cython_inline = None

def inline(f, *args, **kwds):
    global _cython_inline
    if isinstance(f, basestring):
        if _cython_inline is None:
            from Cython.Build.Inline import cython_inline as _cython_inline
        return _cython_inline(f, *args, **kwds)
    else:
        return f
        return


def compile(f):
    from Cython.Build.Inline import RuntimeCompiledFunction
    return RuntimeCompiledFunction(f)


def cdiv(a, b):
    q = a / b
    if q < 0:
        q += 1


def cmod(a, b):
    r = a % b
    if a * b < 0:
        r -= b
    return r


def cast--- This code section failed: ---

 158       0  LOAD_FAST             2  'kwargs'
           3  LOAD_ATTR             0  'pop'
           6  LOAD_CONST            1  'typecheck'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  POP_TOP          

 160      16  LOAD_GLOBAL           2  'hasattr'
          19  LOAD_GLOBAL           2  'hasattr'
          22  CALL_FUNCTION_2       2 
          25  POP_JUMP_IF_FALSE    38  'to 38'

 161      28  LOAD_FAST             0  'type'
          31  LOAD_FAST             1  'args'
          34  CALL_FUNCTION_VAR_0     0 
          37  RETURN_END_IF    
        38_0  COME_FROM                '25'

 163      38  LOAD_FAST             1  'args'
          41  LOAD_CONST            3  ''
          44  BINARY_SUBSCR    
          45  RETURN_VALUE     
          46  LOAD_CONST            0  ''
          49  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 22


def sizeof(arg):
    return 1


def typeof(arg):
    return arg.__class__.__name__


def address(arg):
    return pointer(type(arg))([arg])


def declare--- This code section failed: ---

 176       0  LOAD_FAST             0  'type'
           3  LOAD_CONST            0  ''
           6  LOAD_GLOBAL           1  'object'
           9  BUILD_TUPLE_2         2 
          12  COMPARE_OP            7  'not-in'
          15  POP_JUMP_IF_FALSE    62  'to 62'
          18  LOAD_GLOBAL           2  'hasattr'
          21  LOAD_GLOBAL           1  'object'
          24  CALL_FUNCTION_2       2 
        27_0  COME_FROM                '15'
          27  POP_JUMP_IF_FALSE    62  'to 62'

 177      30  LOAD_FAST             1  'value'
          33  LOAD_GLOBAL           3  '_Unspecified'
          36  COMPARE_OP            9  'is-not'
          39  POP_JUMP_IF_FALSE    52  'to 52'

 178      42  LOAD_FAST             0  'type'
          45  LOAD_FAST             1  'value'
          48  CALL_FUNCTION_1       1 
          51  RETURN_END_IF    
        52_0  COME_FROM                '39'

 180      52  LOAD_FAST             0  'type'
          55  CALL_FUNCTION_0       0 
          58  RETURN_VALUE     
          59  JUMP_FORWARD          4  'to 66'

 182      62  LOAD_FAST             1  'value'
          65  RETURN_VALUE     
        66_0  COME_FROM                '59'
          66  LOAD_CONST            0  ''
          69  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 24


class _nogil(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_class, exc, tb):
        return exc_class is None


nogil = _nogil()
gil = _nogil()
del _nogil

class CythonMetaType(type):

    def __getitem__(type, ix):
        return array(type, ix)


CythonTypeObject = CythonMetaType('CythonTypeObject', (object,), {})

class CythonType(CythonTypeObject):

    def _pointer(self, n=1):
        for i in range(n):
            self = pointer(self)

        return self


class PointerType(CythonType):

    def __init__(self, value=None):
        if isinstance(value, (ArrayType, PointerType)):
            self._items = [ cast(self._basetype, a) for a in value._items ]
        elif isinstance(value, list):
            self._items = [ cast(self._basetype, a) for a in value ]
        elif value is None or value == 0:
            self._items = []
        else:
            raise ValueError
        return

    def __getitem__(self, ix):
        if ix < 0:
            raise IndexError('negative indexing not allowed in C')
        return self._items[ix]

    def __setitem__(self, ix, value):
        if ix < 0:
            raise IndexError('negative indexing not allowed in C')
        self._items[ix] = cast(self._basetype, value)

    def __eq__(self, value):
        if value is None and not self._items:
            return True
        else:
            if type(self) != type(value):
                return False
            return not self._items and not value._items
            return

    def __repr__(self):
        return '%s *' % (self._basetype,)


class ArrayType(PointerType):

    def __init__(self):
        self._items = [
         None] * self._n
        return


class StructType(CythonType):

    def __init__(self, cast_from=_Unspecified, **data):
        if cast_from is not _Unspecified:
            if len(data) > 0:
                raise ValueError('Cannot accept keyword arguments when casting.')
            if type(cast_from) is not type(self):
                raise ValueError('Cannot cast from %s' % cast_from)
            for key, value in cast_from.__dict__.items():
                setattr(self, key, value)

        else:
            for key, value in data.items():
                setattr(self, key, value)

    def __setattr__(self, key, value):
        if key in self._members:
            self.__dict__[key] = cast(self._members[key], value)
        else:
            raise AttributeError("Struct has no member '%s'" % key)


class UnionType(CythonType):

    def __init__(self, cast_from=_Unspecified, **data):
        if cast_from is not _Unspecified:
            if len(data) > 0:
                raise ValueError('Cannot accept keyword arguments when casting.')
            if isinstance(cast_from, dict):
                datadict = cast_from
            elif type(cast_from) is type(self):
                datadict = cast_from.__dict__
            else:
                raise ValueError('Cannot cast from %s' % cast_from)
        else:
            datadict = data
        if len(datadict) > 1:
            raise AttributeError('Union can only store one field at a time.')
        for key, value in datadict.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key in '__dict__':
            CythonType.__setattr__(self, key, value)
        elif key in self._members:
            self.__dict__ = {key: cast(self._members[key], value)}
        else:
            raise AttributeError("Union has no member '%s'" % key)


def pointer(basetype):

    class PointerInstance(PointerType):
        _basetype = basetype

    return PointerInstance


def array(basetype, n):

    class ArrayInstance(ArrayType):
        _basetype = basetype
        _n = n

    return ArrayInstance


def struct():

    class StructInstance(StructType):
        _members = members

    for key in members:
        setattr(StructInstance, key, None)

    return StructInstance


def union():

    class UnionInstance(UnionType):
        _members = members

    for key in members:
        setattr(UnionInstance, key, None)

    return UnionInstance


class typedef(CythonType):

    def __init__(self, type, name=None):
        self._basetype = type
        self.name = name

    def __call__(self, *arg):
        value = cast(self._basetype, *arg)
        return value

    def __repr__(self):
        return self.name or str(self._basetype)

    __getitem__ = index_type


class _FusedType(CythonType):
    pass


def fused_type(*args):
    if not args:
        raise TypeError('Expected at least one type as argument')
    rank = -1
    for type in args:
        if type not in (py_int, py_long, py_float, py_complex):
            break
        if type_ordering.index(type) > rank:
            result_type = type
    else:
        return result_type

    return _FusedType()


def _specialized_from_args(signatures, args, kwargs):
    raise Exception('yet to be implemented')


py_int = typedef(int, 'int')
try:
    py_long = typedef(long, 'long')
except NameError:
    py_long = typedef(int, 'long')

py_float = typedef(float, 'float')
py_complex = typedef(complex, 'double complex')
int_types = [
 'char', 'short', 'Py_UNICODE', 'int', 'Py_UCS4', 'long', 'longlong', 'Py_ssize_t', 'size_t']
float_types = ['longdouble', 'double', 'float']
complex_types = ['longdoublecomplex', 'doublecomplex', 'floatcomplex', 'complex']
other_types = ['bint', 'void']
to_repr = {'longlong': 'long long',
   'longdouble': 'long double',
   'longdoublecomplex': 'long double complex',
   'doublecomplex': 'double complex',
   'floatcomplex': 'float complex'
   }.get
gs = globals()
try:
    import __builtin__ as builtins
except ImportError:
    import builtins

gs['unicode'] = typedef(getattr(builtins, 'unicode', str), 'unicode')
del builtins
for name in int_types:
    reprname = to_repr(name, name)
    gs[name] = typedef(py_int, reprname)
    if name not in ('Py_UNICODE', 'Py_UCS4') and not name.endswith('size_t'):
        gs['u' + name] = typedef(py_int, 'unsigned ' + reprname)
        gs['s' + name] = typedef(py_int, 'signed ' + reprname)

for name in float_types:
    gs[name] = typedef(py_float, to_repr(name, name))

for name in complex_types:
    gs[name] = typedef(py_complex, to_repr(name, name))

bint = typedef(bool, 'bint')
void = typedef(int, 'void')
for t in int_types + float_types + complex_types + other_types:
    for i in range(1, 4):
        gs['%s_%s' % ('p' * i, t)] = globals()[t]._pointer(i)

void = typedef(None, 'void')
NULL = globals()['p_void'](0)
integral = floating = numeric = _FusedType()
type_ordering = [
 py_int, py_long, py_float, py_complex]

class CythonDotParallel(object):
    __suppress_warning__ = [
     'parallel', 'prange', 'threadid']
    __all__ = __suppress_warning__

    def parallel(self, num_threads=None):
        return nogil

    def prange(self, start=0, stop=None, step=1, schedule=None, nogil=False):
        if stop is None:
            stop = start
            start = 0
        return range(start, stop, step)

    def threadid(self):
        return 0


import sys
sys.modules['cython.parallel'] = CythonDotParallel()
del sys