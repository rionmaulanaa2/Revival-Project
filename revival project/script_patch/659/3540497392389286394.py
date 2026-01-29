# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/EntityScanner.py
from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import pkgutil

def _get_module_files(module_dir):
    module_name_set = set()
    try:
        files = os.listdir(module_dir)
    except:
        print('error in generate_module_list  for directory:', module_dir)
        return ()

    for fileName in files:
        list = fileName.split('.')
        if len(list) == 2:
            module_anme = list[0]
            extension = list[1]
            if extension in ('py', 'pyc'):
                module_name_set.add(list[0])

    module_name_set.discard('__init__')
    return module_name_set


def _get_module_list(module_dir):
    import syspathhelper
    module_name_set = _get_module_files(module_dir)
    module_list = []
    syspathhelper.addpath(module_dir)
    for moduleName in module_name_set:
        try:
            mod = __import__(moduleName, fromlist=[''])
            if mod:
                module_list.append(mod)
        except:
            print('error in generate_module_list .', moduleName)
            import traceback
            traceback.print_exc()
            continue

    print('generate_module_list ', module_list)
    return module_list


def _load_all_modules_from_dir(dirname):
    import syspathhelper
    module_set = set()
    syspathhelper.addpath(dirname)
    for importer, package_name, _ in pkgutil.walk_packages([dirname]):
        if package_name not in sys.modules:
            mod = importer.find_module(package_name)
            module = mod.load_module(package_name)
            module_set.add(module)
        else:
            module_set.add(sys.modules[package_name])

    return module_set


def _get_class_list(module, entity_base_class):
    class_list = []
    for name in dir(module):
        attr = getattr(module, name)
        if isinstance(attr, type) and issubclass(attr, entity_base_class):
            class_list.append(attr)

    return class_list


def scan_entity_classes(module_dir, entity_base_class):
    class_dict = {}
    for module in _load_all_modules_from_dir(module_dir):
        clist = _get_class_list(module, entity_base_class)
        for claz in clist:
            class_dict[claz.__name__] = claz

    return class_dict


def walk_packages(path=None, prefix='', pkg_filter=None):

    def seen(p, m={}):
        if p in m:
            return True
        m[p] = True

    for importer, name, ispkg in pkgutil.iter_modules(path, prefix):
        if pkg_filter and not pkg_filter(name):
            continue
        yield (
         importer, name, ispkg)
        if ispkg:
            try:
                __import__(name)
            except ImportError:
                pass
            except Exception:
                raise
            else:
                path = getattr(sys.modules[name], '__path__', None) or []
                path = [ p for p in path if not seen(p) ]
                for item in walk_packages(path, name + '.', pkg_filter):
                    yield item

    return


def _load_all_submodules(package_name):
    import imp
    file_obj, pathname, description = imp.find_module(package_name)
    if file_obj:
        raise ImportError('Not a package: %r', package_name)
    module_set = set()
    name_prefix = package_name + '.'
    for outer_importer in pkgutil.iter_importers():
        module = outer_importer.find_module(package_name)
        if not module:
            continue
        if package_name not in sys.modules:
            outer_importer.find_module(package_name).load_module(package_name)
        for importer, name, _ in walk_packages(outer_importer.path, pkg_filter=lambda n: n.startswith(package_name)):
            if not name.startswith(name_prefix):
                continue
            if name not in sys.modules:
                module = importer.find_module(name).load_module(name)
                module_set.add(module)
            else:
                module_set.add(sys.modules[name])

    return module_set


def scan_entity_package(package_name, entity_base_class):
    class_dict = {}
    for module in _load_all_submodules(package_name):
        clist = _get_class_list(module, entity_base_class)
        for claz in clist:
            class_dict[claz.__name__] = claz

    return class_dict