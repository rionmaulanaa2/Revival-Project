# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/tracebackturbo.py
from __future__ import absolute_import
import six_ex
import six
import linecache
import sys
import types
__all__ = [
 'extract_stack', 'extract_tb', 'format_exception',
 'format_exception_only', 'format_list', 'format_stack',
 'format_tb', 'print_exc', 'format_exc', 'print_exception',
 'print_last', 'print_stack', 'print_tb', 'tb_lineno',
 'print_vars', 'format_vars']
MAX_WIDTH = 255

def _print(file, str='', terminator='\n'):
    file.write(str + terminator)


def print_vars(vars, width=MAX_WIDTH, file=None):
    if file is None:
        file = sys.stderr
    for key, value in vars:
        var = '\t  '
        if isinstance(value, str):
            value = '"' + value.encode('string_escape') + '"'
        if isinstance(value, six.text_type):
            value = 'u"' + value.encode(sys.getdefaultencoding(), 'replace').encode('string_escape') + '"'
        try:
            var += '%s = %s' % (key, value)
        except Exception as e:
            var += '%s = %s' % (key, type(value))

        if len(var) > width:
            var = var[:width - 3] + '...'
        _print(file, var)

    return


def format_vars(vars, width=MAX_WIDTH):
    result = ''
    for key, value in vars:
        var = '\t  '
        if isinstance(value, str):
            value = '"' + value.encode('string_escape') + '"'
        if isinstance(value, six.text_type):
            value = 'u"' + value.encode(sys.getdefaultencoding(), 'replace').encode('string_escape') + '"'
        try:
            var += '%s = %s' % (key, value)
        except:
            var += '%s = %s' % (key, type(value))

        if len(var) > width:
            var = var[:width - 3] + '...'
        result += var + '\n'

    return result


def print_list(extracted_list, file=None, with_vars=True):
    if file is None:
        file = sys.stderr
    for filename, lineno, name, line, locals in extracted_list:
        _print(file, '===> File "%s", line %d, in %s' % (filename, lineno, name))
        if with_vars:
            _print(file, '\tLocal variables:')
            print_vars(sorted(locals), file=file)
        if line:
            _print(file, '\t%s' % line.strip())

    return


def format_list(extracted_list, with_vars=True):
    list = []
    for filename, lineno, name, line, locals in extracted_list:
        item = '====> File "%s", line %d, in %s\n' % (filename, lineno, name)
        if with_vars:
            item += '\tLocal variables:\n'
            item += format_vars(sorted(locals))
        if line:
            item = item + '\t%s\n' % line.strip()
        list.append(item)

    return list


def print_tb(tb, limit=None, file=None, with_vars=True):
    if file is None:
        file = sys.stderr
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        _print(file, '====> File "%s", line %d, in %s' % (filename, lineno, name))
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        locals = six_ex.items(f.f_locals)
        if with_vars:
            _print(file, '\tLocal variables:')
            print_vars(sorted(locals), file=file)
        if line:
            _print(file, '\t' + line.strip())
        tb = tb.tb_next
        n = n + 1

    return


def format_tb(tb, limit=None, with_vars=True):
    return format_list(extract_tb(tb, limit), with_vars)


def extract_tb(tb, limit=None):
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    list = []
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        if line:
            line = line.strip()
        else:
            line = None
        locals = six_ex.items(f.f_locals)
        list.append((filename, lineno, name, line, locals))
        tb = tb.tb_next
        n = n + 1

    return list


def print_exception(etype, value, tb, limit=None, file=None, with_vars=True):
    if file is None:
        file = sys.stderr
    if tb:
        _print(file, 'Traceback Turbo (most recent call last):')
        print_tb(tb, limit, file, with_vars)
    lines = format_exception_only(etype, value)
    for line in lines:
        _print(file, line, '')

    return


def format_exception(etype, value, tb, limit=None, with_vars=True):
    if tb:
        list = [
         'Traceback Turbo (most recent call last):\n']
        list = list + format_tb(tb, limit, with_vars)
    else:
        list = []
    list = list + format_exception_only(etype, value)
    return list


def format_exception_only(etype, value):
    if isinstance(etype, BaseException) or isinstance(etype, types.InstanceType) or etype is None or type(etype) is str:
        return [_format_final_exc_line(etype, value)]
    else:
        stype = etype.__name__
        if not issubclass(etype, SyntaxError):
            return [_format_final_exc_line(stype, value)]
        lines = []
        try:
            msg, (filename, lineno, offset, badline) = value.args
        except Exception:
            pass
        else:
            filename = filename or '<string>'
            lines.append('====> File "%s", line %d\n' % (filename, lineno))
            if badline is not None:
                lines.append('\t%s\n' % badline.strip())
                if offset is not None:
                    caretspace = badline.rstrip('\n')
                    offset = min(len(caretspace), offset) - 1
                    caretspace = caretspace[:offset].lstrip()
                    caretspace = (c.isspace() and c or ' ' for c in caretspace)
                    lines.append('\t%s^\n' % ''.join(caretspace))
            value = msg

        lines.append(_format_final_exc_line(stype, value))
        return lines


def _format_final_exc_line(etype, value):
    valuestr = _some_str(value)
    if value is None or not valuestr:
        line = '%s\n' % etype
    else:
        line = '%s: %s\n' % (etype, valuestr)
    return line


def _some_str(value):
    try:
        return str(value)
    except Exception:
        pass

    try:
        value = six.text_type(value)
        return value.encode('ascii', 'backslashreplace')
    except Exception:
        pass

    return '<unprintable %s object>' % type(value).__name__


def print_exc(limit=None, file=None):
    if file is None:
        file = sys.stderr
    try:
        etype, value, tb = sys.exc_info()
        print_exception(etype, value, tb, limit, file)
    finally:
        etype = value = tb = None

    return


def format_exc(limit=None, with_vars=True):
    try:
        etype, value, tb = sys.exc_info()
        return ''.join(format_exception(etype, value, tb, limit, with_vars))
    finally:
        etype = value = tb = None

    return


def print_last(limit=None, file=None):
    if not hasattr(sys, 'last_type'):
        raise ValueError('no last exception')
    if file is None:
        file = sys.stderr
    print_exception(sys.last_type, sys.last_value, sys.last_traceback, limit, file)
    return


def print_stack(f=None, limit=None, file=None, with_vars=True):
    if f is None:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            f = sys.exc_info()[2].tb_frame.f_back

    print_list(extract_stack(f, limit), file, with_vars)
    return


def format_stack(f=None, limit=None, with_vars=True):
    if f is None:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            f = sys.exc_info()[2].tb_frame.f_back

    return format_list(extract_stack(f, limit), with_vars)


def extract_stack(f=None, limit=None):
    if f is None:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            f = sys.exc_info()[2].tb_frame.f_back

    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    list = []
    n = 0
    while f is not None and (limit is None or n < limit):
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        if line:
            line = line.strip()
        else:
            line = None
        locals = six_ex.items(f.f_locals)
        list.append((filename, lineno, name, line, locals))
        f = f.f_back
        n = n + 1

    list.reverse()
    return list


def tb_lineno(tb):
    return tb.tb_lineno