# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/__init__.py
from __future__ import absolute_import

def init_platform():
    import six.moves.builtins
    from .common_utils import local_text as ltext
    try:
        import world
        import version
        import game3d
        six.moves.builtins.__dict__['G_IS_CLIENT'] = 1
        six.moves.builtins.__dict__['G_IS_SERVER'] = 0
        six.moves.builtins.__dict__['G_TRUNK_PC'] = version.get_tag() == 'trunk' and game3d.get_platform() == game3d.PLATFORM_WIN32
        six.moves.builtins.__dict__['G_CLIENT_DEBUG'] = version.get_tag() == 'trunk'
        six.moves.builtins.__dict__['G_CLIENT_TRUNK'] = version.get_tag() == 'trunk'
        six.moves.builtins.__dict__['G_TEXT_LANG'] = 0
        six.moves.builtins.__dict__['pack_text'] = ltext.pack_text
        six.moves.builtins.__dict__['unpack_text'] = ltext.unpack_text
        six.moves.builtins.__dict__['unpack_text_data'] = ltext.unpack_text_data
        six.moves.builtins.__dict__['get_text_local_content'] = ltext.get_text_local_content
        six.moves.builtins.__dict__['get_text_by_id'] = ltext.get_text_by_id
        six.moves.builtins.__dict__['G_POS_CHANGE_MGR'] = 1
        six.moves.builtins.__dict__['G_CLIENT_ABTEST'] = 0
    except Exception as e:
        six.moves.builtins.__dict__['G_IS_CLIENT'] = 0
        six.moves.builtins.__dict__['G_IS_SERVER'] = 1
        six.moves.builtins.__dict__['pack_text'] = ltext.pack_text
        six.moves.builtins.__dict__['G_CLIENT_DEBUG'] = 0
        six.moves.builtins.__dict__['G_CLIENT_TRUNK'] = 0
        six.moves.builtins.__dict__['G_POS_CHANGE_MGR'] = 0
        six.moves.builtins.__dict__['G_CLIENT_ABTEST'] = 0


init_platform()