# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/reloadshader.py
from __future__ import absolute_import
import render
import game3d
import time
import os
_previous_scan_time = time.time() - 1.0

def reload_one(path):
    if hasattr(render, 'reload_shader_file_modified'):
        if hasattr(render, 'set_enable_compile_shader_async'):
            render.set_enable_compile_shader_async(False)
        import os.path
        basename = os.path.splitext(path)[0].replace('/', '\\')
        render.reload_shader_file_modified(basename + '_gl.vs')
        render.reload_shader_file_modified(basename + '_gl.ps')


def modified():
    global _previous_scan_time
    shaders = []
    work_dir = os.path.dirname(game3d.get_doc_dir())
    shader_dir = os.path.join(work_dir, 'res/shader')
    prefix_len = len(shader_dir) - 6
    for root, _, files in os.walk(shader_dir):
        for f in files:
            if f.endswith('.nfx'):
                ff = os.path.join(root, f)
                mtime = os.path.getmtime(ff)
                if mtime > _previous_scan_time:
                    shaders.append(ff[prefix_len:])

    _previous_scan_time = time.time()
    return shaders


def reload_all():
    for f in modified():
        reload_one(f)