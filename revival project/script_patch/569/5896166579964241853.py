# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/editor.py
from __future__ import absolute_import
from __future__ import print_function
import sys
import game3d
import os
from common.cfg import confmgr
import six
DEBUG_MODE = True
neox_pyqt_path = confmgr.get('editor_path').get('path')
if six.PY2:
    npkimporter = sys.path_hooks.pop()
if not os.path.exists(neox_pyqt_path):
    DEBUG_MODE = False
    neox_pyqt_path = game3d.get_exe_path() + '\\editor'
if six.PY2:
    sys.path_hooks.append(npkimporter)
print('-----------------------------------------------------------------------')
print(neox_pyqt_path + '======================================================')
print('-----------------------------------------------------------------------')
if not os.path.exists(neox_pyqt_path):
    raise ImportError('\xe6\x89\xbe\xe4\xb8\x8d\xe5\x88\xb0\xe7\xbc\x96\xe8\xbe\x91\xe5\x99\xa8\xe7\x9b\xae\xe5\xbd\x95\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe9\x85\x8d\xe7\xbd\xae\xe6\x96\x87\xe4\xbb\xb6editor_path.json\xef\xbc\x8c\xe6\x88\x96\xe8\x81\x94\xe7\xb3\xbb\xe7\xa8\x8b\xe5\xba\x8f')
try:
    game3d.load_plugin('nxqt.dll')
    print('editor mod 1')
    support_nx_qt = True
except ValueError:
    print('editor mode 2')
    support_nx_qt = False

if support_nx_qt:
    path_list = [
     'script/codes', 'script/lib']
else:
    path_list = [
     'script/codes', 'script/lib_with_pyqt']
for path in path_list:
    p = os.path.join(neox_pyqt_path, path)
    if os.path.exists(p):
        if p not in sys.path:
            sys.path.append(p)
            print('append', p)

if not support_nx_qt:
    qt_path = os.path.join(game3d.get_exe_path(), 'platforms')
    if not os.path.exists(qt_path):
        import shutil
        shutil.copytree(os.path.join(neox_pyqt_path, 'python', 'platforms'), qt_path)
if six.PY2:
    npkimporter = sys.path_hooks.pop()
from framework import application
application.init()
from editors import main_window
if global_data.is_local_editor_mode:
    main_window.start_local_editor()
else:
    main_window.start()
if six.PY2:
    sys.path_hooks.append(npkimporter)