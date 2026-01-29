# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Lib/xml/xmllib.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import re
import string
import warnings
warnings.warn('The xmllib module is obsolete.  Use xml.sax instead.', DeprecationWarning, 2)
del warnings
version = '0.3'

class Error(RuntimeError):
    pass


_S = '[ \t\r\n]+'
_opS = '[ \t\r\n]*'
_Name = '[a-zA-Z_:][-a-zA-Z0-9._:]*'
_QStr = '(?:\'[^\']*\'|"[^"]*")'
illegal = re.compile('[^\t\r\n -~\xa0-\xff]')
interesting = re.compile('[]&<]')
amp = re.compile('&')
ref = re.compile('&(' + _Name + '|#[0-9]+|#x[0-9a-fA-F]+)[^-a-zA-Z0-9._:]')
entityref = re.compile('&(?P<name>' + _Name + ')[^-a-zA-Z0-9._:]')
charref = re.compile('&#(?P<char>[0-9]+[^0-9]|x[0-9a-fA-F]+[^0-9a-fA-F])')
space = re.compile(_S + '$')
newline = re.compile('\n')
attrfind = re.compile(_S + '(?P<name>' + _Name + ')(' + _opS + '=' + _opS + '(?P<value>' + _QStr + '|[-a-zA-Z0-9.:+*%?!\\(\\)_#=~]+))?')
starttagopen = re.compile('<' + _Name)
starttagend = re.compile(_opS + '(?P<slash>/?)>')
starttagmatch = re.compile('<(?P<tagname>' + _Name + ')(?P<attrs>(?:' + attrfind.pattern + ')*)' + starttagend.pattern)
endtagopen = re.compile('</')
endbracket = re.compile(_opS + '>')
endbracketfind = re.compile('(?:[^>\'"]|' + _QStr + ')*>')
tagfind = re.compile(_Name)
cdataopen = re.compile('<!\\[CDATA\\[')
cdataclose = re.compile('\\]\\]>')
_SystemLiteral = '(?P<%s>' + _QStr + ')'
_PublicLiteral = '(?P<%s>"[-\'\\(\\)+,./:=?;!*#@$_%% \n\ra-zA-Z0-9]*"|\'[-\\(\\)+,./:=?;!*#@$_%% \n\ra-zA-Z0-9]*\')'
_ExternalId = '(?:SYSTEM|PUBLIC' + _S + _PublicLiteral % 'pubid' + ')' + _S + _SystemLiteral % 'syslit'
doctype = re.compile('<!DOCTYPE' + _S + '(?P<name>' + _Name + ')(?:' + _S + _ExternalId + ')?' + _opS)
xmldecl = re.compile('<\\?xml' + _S + 'version' + _opS + '=' + _opS + '(?P<version>' + _QStr + ')' + '(?:' + _S + 'encoding' + _opS + '=' + _opS + '(?P<encoding>\'[A-Za-z][-A-Za-z0-9._]*\'|"[A-Za-z][-A-Za-z0-9._]*"))?(?:' + _S + 'standalone' + _opS + '=' + _opS + '(?P<standalone>\'(?:yes|no)\'|"(?:yes|no)"))?' + _opS + '\\?>')
procopen = re.compile('<\\?(?P<proc>' + _Name + ')' + _opS)
procclose = re.compile(_opS + '\\?>')
commentopen = re.compile('<!--')
commentclose = re.compile('-->')
doubledash = re.compile('--')
attrtrans = string.maketrans(' \r\n\t', '    ')
_NCName = '[a-zA-Z_][-a-zA-Z0-9._]*'
ncname = re.compile(_NCName + '$')
qname = re.compile('(?:(?P<prefix>' + _NCName + '):)?(?P<local>' + _NCName + ')$')
xmlns = re.compile('xmlns(?::(?P<ncname>' + _NCName + '))?$')

class XMLParser():
    attributes = {}
    elements = {}
    __accept_unquoted_attributes = 0
    __accept_missing_endtag_name = 0
    __map_case = 0
    __accept_utf8 = 0
    __translate_attribute_references = 1

    def __init__(self, **kw):
        self.__fixed = 0
        if 'accept_unquoted_attributes' in kw:
            self.__accept_unquoted_attributes = kw['accept_unquoted_attributes']
        if 'accept_missing_endtag_name' in kw:
            self.__accept_missing_endtag_name = kw['accept_missing_endtag_name']
        if 'map_case' in kw:
            self.__map_case = kw['map_case']
        if 'accept_utf8' in kw:
            self.__accept_utf8 = kw['accept_utf8']
        if 'translate_attribute_references' in kw:
            self.__translate_attribute_references = kw['translate_attribute_references']
        self.reset()

    def __fixelements(self):
        self.__fixed = 1
        self.elements = {}
        self.__fixdict(self.__dict__)
        self.__fixclass(self.__class__)

    def __fixclass(self, kl):
        self.__fixdict(kl.__dict__)
        for k in kl.__bases__:
            self.__fixclass(k)

    def __fixdict(self, dict):
        for key in dict.keys():
            if key[:6] == 'start_':
                tag = key[6:]
                start, end = self.elements.get(tag, (None, None))
                if start is None:
                    self.elements[tag] = (
                     getattr(self, key), end)
            elif key[:4] == 'end_':
                tag = key[4:]
                start, end = self.elements.get(tag, (None, None))
                if end is None:
                    self.elements[tag] = (
                     start, getattr(self, key))

        return

    def reset(self):
        self.rawdata = ''
        self.stack = []
        self.nomoretags = 0
        self.literal = 0
        self.lineno = 1
        self.__at_start = 1
        self.__seen_doctype = None
        self.__seen_starttag = 0
        self.__use_namespaces = 0
        self.__namespaces = {'xml': None}
        if self.elements is XMLParser.elements:
            self.__fixelements()
        return

    def setnomoretags(self):
        self.nomoretags = self.literal = 1

    def setliteral(self, *args):
        self.literal = 1

    def feed(self, data):
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        self.goahead(1)
        if self.__fixed:
            self.__fixed = 0
            del self.elements

    def translate_references(self, data, all=1):
        if not self.__translate_attribute_references:
            return data
        else:
            i = 0
            while 1:
                res = amp.search(data, i)
                if res is None:
                    return data
                s = res.start(0)
                res = ref.match(data, s)
                if res is None:
                    self.syntax_error("bogus `&'")
                    i = s + 1
                    continue
                i = res.end(0)
                str = res.group(1)
                rescan = 0
                if str[0] == '#':
                    if str[1] == 'x':
                        str = six.int2byte(int(str[2:], 16))
                    else:
                        str = six.int2byte(int(str[1:]))
                    if data[i - 1] != ';':
                        self.syntax_error("`;' missing after char reference")
                        i = i - 1
                elif all:
                    if str in self.entitydefs:
                        str = self.entitydefs[str]
                        rescan = 1
                    elif data[i - 1] != ';':
                        self.syntax_error("bogus `&'")
                        i = s + 1
                        continue
                    else:
                        self.syntax_error("reference to unknown entity `&%s;'" % str)
                        str = '&' + str + ';'
                elif data[i - 1] != ';':
                    self.syntax_error("bogus `&'")
                    i = s + 1
                    continue
                data = data[:s] + str + data[i:]
                if rescan:
                    i = s
                else:
                    i = s + len(str)

            return

    def getnamespace(self):
        nsdict = {}
        for t, d, nst in self.stack:
            nsdict.update(d)

        return nsdict

    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            if i > 0:
                self.__at_start = 0
            if self.nomoretags:
                data = rawdata[i:n]
                self.handle_data(data)
                self.lineno = self.lineno + data.count('\n')
                i = n
                break
            res = interesting.search(rawdata, i)
            if res:
                j = res.start(0)
            else:
                j = n
            if i < j:
                data = rawdata[i:j]
                if self.__at_start and space.match(data) is None:
                    self.syntax_error('illegal data at start of file')
                self.__at_start = 0
                if not self.stack and space.match(data) is None:
                    self.syntax_error('data not in content')
                if not self.__accept_utf8 and illegal.search(data):
                    self.syntax_error('illegal character in content')
                self.handle_data(data)
                self.lineno = self.lineno + data.count('\n')
            i = j
            if i == n:
                break
            if rawdata[i] == '<':
                if starttagopen.match(rawdata, i):
                    if self.literal:
                        data = rawdata[i]
                        self.handle_data(data)
                        self.lineno = self.lineno + data.count('\n')
                        i = i + 1
                        continue
                    k = self.parse_starttag(i)
                    if k < 0:
                        break
                    self.__seen_starttag = 1
                    self.lineno = self.lineno + rawdata[i:k].count('\n')
                    i = k
                    continue
                if endtagopen.match(rawdata, i):
                    k = self.parse_endtag(i)
                    if k < 0:
                        break
                    self.lineno = self.lineno + rawdata[i:k].count('\n')
                    i = k
                    continue
                if commentopen.match(rawdata, i):
                    if self.literal:
                        data = rawdata[i]
                        self.handle_data(data)
                        self.lineno = self.lineno + data.count('\n')
                        i = i + 1
                        continue
                    k = self.parse_comment(i)
                    if k < 0:
                        break
                    self.lineno = self.lineno + rawdata[i:k].count('\n')
                    i = k
                    continue
                if cdataopen.match(rawdata, i):
                    k = self.parse_cdata(i)
                    if k < 0:
                        break
                    self.lineno = self.lineno + rawdata[i:k].count('\n')
                    i = k
                    continue
                res = xmldecl.match(rawdata, i)
                if res:
                    if not self.__at_start:
                        self.syntax_error('<?xml?> declaration not at start of document')
                    version, encoding, standalone = res.group('version', 'encoding', 'standalone')
                    if version[1:-1] != '1.0':
                        raise Error('only XML version 1.0 supported')
                    if encoding:
                        encoding = encoding[1:-1]
                    if standalone:
                        standalone = standalone[1:-1]
                    self.handle_xml(encoding, standalone)
                    i = res.end(0)
                    continue
                res = procopen.match(rawdata, i)
                if res:
                    k = self.parse_proc(i)
                    if k < 0:
                        break
                    self.lineno = self.lineno + rawdata[i:k].count('\n')
                    i = k
                    continue
                res = doctype.match(rawdata, i)
                if res:
                    if self.literal:
                        data = rawdata[i]
                        self.handle_data(data)
                        self.lineno = self.lineno + data.count('\n')
                        i = i + 1
                        continue
                    if self.__seen_doctype:
                        self.syntax_error('multiple DOCTYPE elements')
                    if self.__seen_starttag:
                        self.syntax_error('DOCTYPE not at beginning of document')
                    k = self.parse_doctype(res)
                    if k < 0:
                        break
                    self.__seen_doctype = res.group('name')
                    if self.__map_case:
                        self.__seen_doctype = self.__seen_doctype.lower()
                    self.lineno = self.lineno + rawdata[i:k].count('\n')
                    i = k
                    continue
            elif rawdata[i] == '&':
                if self.literal:
                    data = rawdata[i]
                    self.handle_data(data)
                    i = i + 1
                    continue
                res = charref.match(rawdata, i)
                if res is not None:
                    i = res.end(0)
                    if rawdata[i - 1] != ';':
                        self.syntax_error("`;' missing in charref")
                        i = i - 1
                    if not self.stack:
                        self.syntax_error('data not in content')
                    self.handle_charref(res.group('char')[:-1])
                    self.lineno = self.lineno + res.group(0).count('\n')
                    continue
                res = entityref.match(rawdata, i)
                if res is not None:
                    i = res.end(0)
                    if rawdata[i - 1] != ';':
                        self.syntax_error("`;' missing in entityref")
                        i = i - 1
                    name = res.group('name')
                    if self.__map_case:
                        name = name.lower()
                    if name in self.entitydefs:
                        self.rawdata = rawdata = rawdata[:res.start(0)] + self.entitydefs[name] + rawdata[i:]
                        n = len(rawdata)
                        i = res.start(0)
                    else:
                        self.unknown_entityref(name)
                    self.lineno = self.lineno + res.group(0).count('\n')
                    continue
            elif rawdata[i] == ']':
                if self.literal:
                    data = rawdata[i]
                    self.handle_data(data)
                    i = i + 1
                    continue
                if n - i < 3:
                    break
                if cdataclose.match(rawdata, i):
                    self.syntax_error("bogus `]]>'")
                self.handle_data(rawdata[i])
                i = i + 1
                continue
            else:
                raise Error('neither < nor & ??')
            break

        if i > 0:
            self.__at_start = 0
        if end and i < n:
            data = rawdata[i]
            self.syntax_error("bogus `%s'" % data)
            if not self.__accept_utf8 and illegal.search(data):
                self.syntax_error('illegal character in content')
            self.handle_data(data)
            self.lineno = self.lineno + data.count('\n')
            self.rawdata = rawdata[i + 1:]
            return self.goahead(end)
        else:
            self.rawdata = rawdata[i:]
            if end:
                if not self.__seen_starttag:
                    self.syntax_error('no elements in file')
                if self.stack:
                    self.syntax_error('missing end tags')
                    while self.stack:
                        self.finish_endtag(self.stack[-1][0])

            return

    def parse_comment(self, i):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            raise Error('unexpected call to handle_comment')
        res = commentclose.search(rawdata, i + 4)
        if res is None:
            return -1
        else:
            if doubledash.search(rawdata, i + 4, res.start(0)):
                self.syntax_error("`--' inside comment")
            if rawdata[res.start(0) - 1] == '-':
                self.syntax_error('comment cannot end in three dashes')
            if not self.__accept_utf8 and illegal.search(rawdata, i + 4, res.start(0)):
                self.syntax_error('illegal character in comment')
            self.handle_comment(rawdata[i + 4:res.start(0)])
            return res.end(0)

    def parse_doctype(self, res):
        rawdata = self.rawdata
        n = len(rawdata)
        name = res.group('name')
        if self.__map_case:
            name = name.lower()
        pubid, syslit = res.group('pubid', 'syslit')
        if pubid is not None:
            pubid = pubid[1:-1]
            pubid = ' '.join(pubid.split())
        if syslit is not None:
            syslit = syslit[1:-1]
        j = k = res.end(0)
        if k >= n:
            return -1
        else:
            if rawdata[k] == '[':
                level = 0
                k = k + 1
                dq = sq = 0
                while k < n:
                    c = rawdata[k]
                    if not sq and c == '"':
                        dq = not dq
                    elif not dq and c == "'":
                        sq = not sq
                    else:
                        if sq or dq:
                            pass
                        elif level <= 0 and c == ']':
                            res = endbracket.match(rawdata, k + 1)
                            if res is None:
                                return -1
                            self.handle_doctype(name, pubid, syslit, rawdata[j + 1:k])
                            return res.end(0)
                        if c == '<':
                            level = level + 1
                        elif c == '>':
                            level = level - 1
                            if level < 0:
                                self.syntax_error("bogus `>' in DOCTYPE")
                    k = k + 1

            res = endbracketfind.match(rawdata, k)
            if res is None:
                return -1
            if endbracket.match(rawdata, k) is None:
                self.syntax_error('garbage in DOCTYPE')
            self.handle_doctype(name, pubid, syslit, None)
            return res.end(0)

    def parse_cdata(self, i):
        rawdata = self.rawdata
        if rawdata[i:i + 9] != '<![CDATA[':
            raise Error('unexpected call to parse_cdata')
        res = cdataclose.search(rawdata, i + 9)
        if res is None:
            return -1
        else:
            if not self.__accept_utf8 and illegal.search(rawdata, i + 9, res.start(0)):
                self.syntax_error('illegal character in CDATA')
            if not self.stack:
                self.syntax_error('CDATA not in content')
            self.handle_cdata(rawdata[i + 9:res.start(0)])
            return res.end(0)

    __xml_namespace_attributes = {'ns': None,'src': None,'prefix': None}

    def parse_proc(self, i):
        rawdata = self.rawdata
        end = procclose.search(rawdata, i)
        if end is None:
            return -1
        else:
            j = end.start(0)
            if not self.__accept_utf8 and illegal.search(rawdata, i + 2, j):
                self.syntax_error('illegal character in processing instruction')
            res = tagfind.match(rawdata, i + 2)
            if res is None:
                raise Error('unexpected call to parse_proc')
            k = res.end(0)
            name = res.group(0)
            if self.__map_case:
                name = name.lower()
            if name == 'xml:namespace':
                self.syntax_error('old-fashioned namespace declaration')
                self.__use_namespaces = -1
                if self.__seen_doctype or self.__seen_starttag:
                    self.syntax_error('xml:namespace declaration too late in document')
                attrdict, namespace, k = self.parse_attributes(name, k, j)
                if namespace:
                    self.syntax_error('namespace declaration inside namespace declaration')
                for attrname in attrdict.keys():
                    if attrname not in self.__xml_namespace_attributes:
                        self.syntax_error("unknown attribute `%s' in xml:namespace tag" % attrname)

                if 'ns' not in attrdict or 'prefix' not in attrdict:
                    self.syntax_error('xml:namespace without required attributes')
                prefix = attrdict.get('prefix')
                if ncname.match(prefix) is None:
                    self.syntax_error('xml:namespace illegal prefix value')
                    return end.end(0)
                if prefix in self.__namespaces:
                    self.syntax_error('xml:namespace prefix not unique')
                self.__namespaces[prefix] = attrdict['ns']
            else:
                if name.lower() == 'xml':
                    self.syntax_error('illegal processing instruction target name')
                self.handle_proc(name, rawdata[k:j])
            return end.end(0)

    def parse_attributes(self, tag, i, j):
        rawdata = self.rawdata
        attrdict = {}
        namespace = {}
        while i < j:
            res = attrfind.match(rawdata, i)
            if res is None:
                break
            attrname, attrvalue = res.group('name', 'value')
            if self.__map_case:
                attrname = attrname.lower()
            i = res.end(0)
            if attrvalue is None:
                self.syntax_error("no value specified for attribute `%s'" % attrname)
                attrvalue = attrname
            elif attrvalue[:1] == "'" == attrvalue[-1:] or attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
            elif not self.__accept_unquoted_attributes:
                self.syntax_error("attribute `%s' value not quoted" % attrname)
            res = xmlns.match(attrname)
            if res is not None:
                ncname = res.group('ncname')
                namespace[ncname or ''] = attrvalue or None
                if not self.__use_namespaces:
                    self.__use_namespaces = len(self.stack) + 1
                continue
            if '<' in attrvalue:
                self.syntax_error("`<' illegal in attribute value")
            if attrname in attrdict:
                self.syntax_error("attribute `%s' specified twice" % attrname)
            attrvalue = attrvalue.translate(attrtrans)
            attrdict[attrname] = self.translate_references(attrvalue)

        return (attrdict, namespace, i)

    def parse_starttag(self, i):
        rawdata = self.rawdata
        end = endbracketfind.match(rawdata, i + 1)
        if end is None:
            return -1
        else:
            tag = starttagmatch.match(rawdata, i)
            if tag is None or tag.end(0) != end.end(0):
                self.syntax_error('garbage in starttag')
                return end.end(0)
            nstag = tagname = tag.group('tagname')
            if self.__map_case:
                nstag = tagname = nstag.lower()
            if not self.__seen_starttag and self.__seen_doctype and tagname != self.__seen_doctype:
                self.syntax_error('starttag does not match DOCTYPE')
            if self.__seen_starttag and not self.stack:
                self.syntax_error('multiple elements on top level')
            k, j = tag.span('attrs')
            attrdict, nsdict, k = self.parse_attributes(tagname, k, j)
            self.stack.append((tagname, nsdict, nstag))
            if self.__use_namespaces:
                res = qname.match(tagname)
            else:
                res = None
            if res is not None:
                prefix, nstag = res.group('prefix', 'local')
                if prefix is None:
                    prefix = ''
                ns = None
                for t, d, nst in self.stack:
                    if prefix in d:
                        ns = d[prefix]

                if ns is None and prefix != '':
                    ns = self.__namespaces.get(prefix)
                if ns is not None:
                    nstag = ns + ' ' + nstag
                elif prefix != '':
                    nstag = prefix + ':' + nstag
                self.stack[-1] = (
                 tagname, nsdict, nstag)
            attrnamemap = {}
            for key in attrdict.keys():
                attrnamemap[key] = key

            if self.__use_namespaces:
                nattrdict = {}
                for key, val in attrdict.items():
                    okey = key
                    res = qname.match(key)
                    if res is not None:
                        aprefix, key = res.group('prefix', 'local')
                        if self.__map_case:
                            key = key.lower()
                        if aprefix is not None:
                            ans = None
                            for t, d, nst in self.stack:
                                if aprefix in d:
                                    ans = d[aprefix]

                            if ans is None:
                                ans = self.__namespaces.get(aprefix)
                            if ans is not None:
                                key = ans + ' ' + key
                            else:
                                key = aprefix + ':' + key
                    nattrdict[key] = val
                    attrnamemap[key] = okey

                attrdict = nattrdict
            attributes = self.attributes.get(nstag)
            if attributes is not None:
                for key in attrdict.keys():
                    if key not in attributes:
                        self.syntax_error("unknown attribute `%s' in tag `%s'" % (attrnamemap[key], tagname))

                for key, val in attributes.items():
                    if val is not None and key not in attrdict:
                        attrdict[key] = val

            method = self.elements.get(nstag, (None, None))[0]
            self.finish_starttag(nstag, attrdict, method)
            if tag.group('slash') == '/':
                self.finish_endtag(tagname)
            return tag.end(0)

    def parse_endtag(self, i):
        rawdata = self.rawdata
        end = endbracketfind.match(rawdata, i + 1)
        if end is None:
            return -1
        else:
            res = tagfind.match(rawdata, i + 2)
            if res is None:
                if self.literal:
                    self.handle_data(rawdata[i])
                    return i + 1
                if not self.__accept_missing_endtag_name:
                    self.syntax_error('no name specified in end tag')
                tag = self.stack[-1][0]
                k = i + 2
            else:
                tag = res.group(0)
                if self.__map_case:
                    tag = tag.lower()
                if self.literal:
                    if not self.stack or tag != self.stack[-1][0]:
                        self.handle_data(rawdata[i])
                        return i + 1
                k = res.end(0)
            if endbracket.match(rawdata, k) is None:
                self.syntax_error('garbage in end tag')
            self.finish_endtag(tag)
            return end.end(0)

    def finish_starttag(self, tagname, attrdict, method):
        if method is not None:
            self.handle_starttag(tagname, method, attrdict)
        else:
            self.unknown_starttag(tagname, attrdict)
        return

    def finish_endtag(self, tag):
        self.literal = 0
        if not tag:
            self.syntax_error('name-less end tag')
            found = len(self.stack) - 1
            if found < 0:
                self.unknown_endtag(tag)
                return
        else:
            found = -1
            for i in range(len(self.stack)):
                if tag == self.stack[i][0]:
                    found = i

            if found == -1:
                self.syntax_error('unopened end tag')
                return
        while len(self.stack) > found:
            if found < len(self.stack) - 1:
                self.syntax_error('missing close tag for %s' % self.stack[-1][2])
            nstag = self.stack[-1][2]
            method = self.elements.get(nstag, (None, None))[1]
            if method is not None:
                self.handle_endtag(nstag, method)
            else:
                self.unknown_endtag(nstag)
            if self.__use_namespaces == len(self.stack):
                self.__use_namespaces = 0
            del self.stack[-1]

        return

    def handle_xml(self, encoding, standalone):
        pass

    def handle_doctype(self, tag, pubid, syslit, data):
        pass

    def handle_starttag(self, tag, method, attrs):
        method(attrs)

    def handle_endtag(self, tag, method):
        method()

    def handle_charref(self, name):
        try:
            if name[0] == 'x':
                n = int(name[1:], 16)
            else:
                n = int(name)
        except ValueError:
            self.unknown_charref(name)
            return

        if not 0 <= n <= 255:
            self.unknown_charref(name)
            return
        self.handle_data(six.int2byte(n))

    entitydefs = {'lt': '&#60;','gt': '&#62;',
       'amp': '&#38;',
       'quot': '&#34;',
       'apos': '&#39;'
       }

    def handle_data(self, data):
        pass

    def handle_cdata(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_proc(self, name, data):
        pass

    def syntax_error(self, message):
        raise Error('Syntax error at line %d: %s' % (self.lineno, message))

    def unknown_starttag(self, tag, attrs):
        pass

    def unknown_endtag(self, tag):
        pass

    def unknown_charref(self, ref):
        pass

    def unknown_entityref(self, name):
        self.syntax_error("reference to unknown entity `&%s;'" % name)


class TestXMLParser(XMLParser):

    def __init__(self, **kw):
        self.testdata = ''
        XMLParser.__init__(self, **kw)

    def handle_xml(self, encoding, standalone):
        self.flush()
        print('xml: encoding =', encoding, 'standalone =', standalone)

    def handle_doctype(self, tag, pubid, syslit, data):
        self.flush()
        print('DOCTYPE:', tag, repr(data))

    def handle_data(self, data):
        self.testdata = self.testdata + data
        if len(repr(self.testdata)) >= 70:
            self.flush()

    def flush(self):
        data = self.testdata
        if data:
            self.testdata = ''
            print('data:', repr(data))

    def handle_cdata(self, data):
        self.flush()
        print('cdata:', repr(data))

    def handle_proc(self, name, data):
        self.flush()
        print('processing:', name, repr(data))

    def handle_comment(self, data):
        self.flush()
        r = repr(data)
        if len(r) > 68:
            r = r[:32] + '...' + r[-32:]
        print('comment:', r)

    def syntax_error(self, message):
        print('error at line %d:' % self.lineno, message)

    def unknown_starttag(self, tag, attrs):
        self.flush()
        if not attrs:
            print('start tag: <' + tag + '>')
        else:
            print('start tag: <' + tag, end=' ')
            for name, value in attrs.items():
                print(name + '=' + '"' + value + '"', end=' ')

            print('>')

    def unknown_endtag(self, tag):
        self.flush()
        print('end tag: </' + tag + '>')

    def unknown_entityref(self, ref):
        self.flush()
        print('*** unknown entity ref: &' + ref + ';')

    def unknown_charref(self, ref):
        self.flush()
        print('*** unknown char ref: &#' + ref + ';')

    def close(self):
        XMLParser.close(self)
        self.flush()


def test--- This code section failed: ---

 879       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'sys'
           9  STORE_FAST            1  'sys'
          12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'getopt'
          21  STORE_FAST            2  'getopt'

 880      24  LOAD_CONST            1  ''
          27  LOAD_CONST            2  ('time',)
          30  IMPORT_NAME           2  'time'
          33  IMPORT_FROM           2  'time'
          36  STORE_FAST            3  'time'
          39  POP_TOP          

 882      40  LOAD_FAST             0  'args'
          43  POP_JUMP_IF_TRUE     62  'to 62'

 883      46  LOAD_FAST             1  'sys'
          49  LOAD_ATTR             3  'argv'
          52  LOAD_CONST            3  1
          55  SLICE+1          
          56  STORE_FAST            0  'args'
          59  JUMP_FORWARD          0  'to 62'
        62_0  COME_FROM                '59'

 885      62  LOAD_FAST             2  'getopt'
          65  LOAD_ATTR             1  'getopt'
          68  LOAD_ATTR             4  'TestXMLParser'
          71  CALL_FUNCTION_2       2 
          74  UNPACK_SEQUENCE_2     2 
          77  STORE_FAST            4  'opts'
          80  STORE_FAST            0  'args'

 886      83  LOAD_GLOBAL           4  'TestXMLParser'
          86  STORE_FAST            5  'klass'

 887      89  LOAD_CONST            1  ''
          92  STORE_FAST            6  'do_time'

 888      95  SETUP_LOOP           62  'to 160'
          98  LOAD_FAST             4  'opts'
         101  GET_ITER         
         102  FOR_ITER             54  'to 159'
         105  UNPACK_SEQUENCE_2     2 
         108  STORE_FAST            7  'o'
         111  STORE_FAST            8  'a'

 889     114  LOAD_FAST             7  'o'
         117  LOAD_CONST            5  '-s'
         120  COMPARE_OP            2  '=='
         123  POP_JUMP_IF_FALSE   135  'to 135'

 890     126  LOAD_GLOBAL           5  'XMLParser'
         129  STORE_FAST            5  'klass'
         132  JUMP_BACK           102  'to 102'

 891     135  LOAD_FAST             7  'o'
         138  LOAD_CONST            6  '-t'
         141  COMPARE_OP            2  '=='
         144  POP_JUMP_IF_FALSE   102  'to 102'

 892     147  LOAD_CONST            3  1
         150  STORE_FAST            6  'do_time'
         153  JUMP_BACK           102  'to 102'
         156  JUMP_BACK           102  'to 102'
         159  POP_BLOCK        
       160_0  COME_FROM                '95'

 894     160  LOAD_FAST             0  'args'
         163  POP_JUMP_IF_FALSE   176  'to 176'

 895     166  POP_JUMP_IF_FALSE     1  'to 1'
         169  BINARY_SUBSCR    
         170  STORE_FAST            9  'file'
         173  JUMP_FORWARD          6  'to 182'

 897     176  LOAD_CONST            7  'test.xml'
         179  STORE_FAST            9  'file'
       182_0  COME_FROM                '173'

 899     182  LOAD_FAST             9  'file'
         185  LOAD_CONST            8  '-'
         188  COMPARE_OP            2  '=='
         191  POP_JUMP_IF_FALSE   206  'to 206'

 900     194  LOAD_FAST             1  'sys'
         197  LOAD_ATTR             6  'stdin'
         200  STORE_FAST           10  'f'
         203  JUMP_FORWARD         70  'to 276'

 902     206  SETUP_EXCEPT         19  'to 228'

 903     209  LOAD_GLOBAL           7  'open'
         212  LOAD_FAST             9  'file'
         215  LOAD_CONST            9  'r'
         218  CALL_FUNCTION_2       2 
         221  STORE_FAST           10  'f'
         224  POP_BLOCK        
         225  JUMP_FORWARD         48  'to 276'
       228_0  COME_FROM                '206'

 904     228  DUP_TOP          
         229  LOAD_GLOBAL           8  'IOError'
         232  COMPARE_OP           10  'exception-match'
         235  POP_JUMP_IF_FALSE   275  'to 275'
         238  POP_TOP          
         239  STORE_FAST           11  'msg'
         242  POP_TOP          

 905     243  LOAD_GLOBAL           9  'print'
         246  LOAD_FAST             9  'file'
         249  LOAD_CONST           10  ':'
         252  LOAD_FAST            11  'msg'
         255  CALL_FUNCTION_3       3 
         258  POP_TOP          

 906     259  LOAD_FAST             1  'sys'
         262  LOAD_ATTR            10  'exit'
         265  LOAD_CONST            3  1
         268  CALL_FUNCTION_1       1 
         271  POP_TOP          
         272  JUMP_FORWARD          1  'to 276'
         275  END_FINALLY      
       276_0  COME_FROM                '275'
       276_1  COME_FROM                '225'
       276_2  COME_FROM                '203'

 908     276  LOAD_FAST            10  'f'
         279  LOAD_ATTR            11  'read'
         282  CALL_FUNCTION_0       0 
         285  STORE_FAST           12  'data'

 909     288  LOAD_FAST            10  'f'
         291  LOAD_FAST             1  'sys'
         294  LOAD_ATTR             6  'stdin'
         297  COMPARE_OP            9  'is-not'
         300  POP_JUMP_IF_FALSE   316  'to 316'

 910     303  LOAD_FAST            10  'f'
         306  LOAD_ATTR            12  'close'
         309  CALL_FUNCTION_0       0 
         312  POP_TOP          
         313  JUMP_FORWARD          0  'to 316'
       316_0  COME_FROM                '313'

 912     316  LOAD_FAST             5  'klass'
         319  CALL_FUNCTION_0       0 
         322  STORE_FAST           13  'x'

 913     325  LOAD_FAST             3  'time'
         328  CALL_FUNCTION_0       0 
         331  STORE_FAST           14  't0'

 914     334  SETUP_EXCEPT         76  'to 413'

 915     337  LOAD_FAST             6  'do_time'
         340  POP_JUMP_IF_FALSE   369  'to 369'

 916     343  LOAD_FAST            13  'x'
         346  LOAD_ATTR            13  'feed'
         349  LOAD_FAST            12  'data'
         352  CALL_FUNCTION_1       1 
         355  POP_TOP          

 917     356  LOAD_FAST            13  'x'
         359  LOAD_ATTR            12  'close'
         362  CALL_FUNCTION_0       0 
         365  POP_TOP          
         366  JUMP_FORWARD         40  'to 409'

 919     369  SETUP_LOOP           27  'to 399'
         372  LOAD_FAST            12  'data'
         375  GET_ITER         
         376  FOR_ITER             19  'to 398'
         379  STORE_FAST           15  'c'

 920     382  LOAD_FAST            13  'x'
         385  LOAD_ATTR            13  'feed'
         388  LOAD_FAST            15  'c'
         391  CALL_FUNCTION_1       1 
         394  POP_TOP          
         395  JUMP_BACK           376  'to 376'
         398  POP_BLOCK        
       399_0  COME_FROM                '369'

 921     399  LOAD_FAST            13  'x'
         402  LOAD_ATTR            12  'close'
         405  CALL_FUNCTION_0       0 
         408  POP_TOP          
       409_0  COME_FROM                '366'
         409  POP_BLOCK        
         410  JUMP_FORWARD         78  'to 491'
       413_0  COME_FROM                '334'

 922     413  DUP_TOP          
         414  LOAD_GLOBAL          14  'Error'
         417  COMPARE_OP           10  'exception-match'
         420  POP_JUMP_IF_FALSE   490  'to 490'
         423  POP_TOP          
         424  STORE_FAST           11  'msg'
         427  POP_TOP          

 923     428  LOAD_FAST             3  'time'
         431  CALL_FUNCTION_0       0 
         434  STORE_FAST           16  't1'

 924     437  LOAD_GLOBAL           9  'print'
         440  LOAD_FAST            11  'msg'
         443  CALL_FUNCTION_1       1 
         446  POP_TOP          

 925     447  LOAD_FAST             6  'do_time'
         450  POP_JUMP_IF_FALSE   474  'to 474'

 926     453  LOAD_GLOBAL           9  'print'
         456  LOAD_CONST           11  'total time: %g'
         459  LOAD_FAST            16  't1'
         462  LOAD_FAST            14  't0'
         465  BINARY_SUBTRACT  
         466  BINARY_MODULO    
         467  CALL_FUNCTION_1       1 
         470  POP_TOP          
         471  JUMP_FORWARD          0  'to 474'
       474_0  COME_FROM                '471'

 927     474  LOAD_FAST             1  'sys'
         477  LOAD_ATTR            10  'exit'
         480  LOAD_CONST            3  1
         483  CALL_FUNCTION_1       1 
         486  POP_TOP          
         487  JUMP_FORWARD          1  'to 491'
         490  END_FINALLY      
       491_0  COME_FROM                '490'
       491_1  COME_FROM                '410'

 928     491  LOAD_FAST             3  'time'
         494  CALL_FUNCTION_0       0 
         497  STORE_FAST           16  't1'

 929     500  LOAD_FAST             6  'do_time'
         503  POP_JUMP_IF_FALSE   527  'to 527'

 930     506  LOAD_GLOBAL           9  'print'
         509  LOAD_CONST           11  'total time: %g'
         512  LOAD_FAST            16  't1'
         515  LOAD_FAST            14  't0'
         518  BINARY_SUBTRACT  
         519  BINARY_MODULO    
         520  CALL_FUNCTION_1       1 
         523  POP_TOP          
         524  JUMP_FORWARD          0  'to 527'
       527_0  COME_FROM                '524'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 71


if __name__ == '__main__':
    test()