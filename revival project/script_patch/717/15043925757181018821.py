# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/game3dex.py
from __future__ import absolute_import
import game3d
from logic.gcommon.common_utils.local_text import get_text_by_id

def check_pick_image_version():
    try:
        v = game3d.get_engine_version()
        v1, v2, v3 = v.split('.')
        v1 = int(v1)
        v2 = int(v2)
        v3 = int(v3)
    except:
        v1, v2, v3 = (1, 0, 0)

    if v1 > 1:
        return True
    if v1 < 1:
        return False
    if v2 > 1:
        return True
    if v2 < 1:
        return False
    if v3 > 0:
        return True
    return False


def init_pick_image():
    if check_pick_image_version():
        return

    def pick_image(small_w, small_h, big_w, big_h, callback):
        from main.comsys.uiutils import tellme
        tellme(get_text_by_id(2122))
        callback(game3d.PICK_CANCEL, '', '')

    game3d.pick_image = pick_image


def init():
    init_pick_image()


def get_doc_dir():
    return game3d.get_doc_dir() + '/'


def get_app_dir():
    return './'