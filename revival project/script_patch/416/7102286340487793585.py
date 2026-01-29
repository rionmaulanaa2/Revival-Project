# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/GMDecorator.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode import GMUtils
from logic.comsys.guide_ui.GuideSetting import GuideSetting

def execute_by_mode(is_execute, mode_types, in_local=False):

    def decorator(func):

        def wrapper(*args, **kwargs):
            if in_local and global_data.player and global_data.player.in_local_battle():
                return func(*args, **kwargs)
            if not global_data.game_mode:
                return
            mode_type = global_data.game_mode.get_mode_type()
            is_cur_mode_type = False
            for i_mode_type in mode_types:
                if i_mode_type == mode_type:
                    is_cur_mode_type = True
                elif type(i_mode_type) is set or type(i_mode_type) is tuple:
                    if mode_type in i_mode_type:
                        is_cur_mode_type = True

            if is_execute:
                if is_cur_mode_type:
                    return func(*args, **kwargs)
            elif not is_cur_mode_type:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def overload_func(func_name, mode_types_dict):

    def decorator(func):

        def wrapper(*args, **kwargs):
            if not global_data.game_mode:
                return func(*args, **kwargs)
            mode_type = global_data.game_mode.get_mode_type()
            if mode_type in mode_types_dict:
                mode_func_name = mode_types_dict[mode_type]
                new_func = getattr(GMUtils, mode_func_name)
                if new_func:
                    return new_func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def halt_by_create_login(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper