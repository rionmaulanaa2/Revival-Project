# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/debug/async_test.py
from __future__ import absolute_import
import six.moves.builtins
import game3d
import world
s_delay_model_time = 1000
s_delay_sfx_time = 1000
create_model_async_org = None
create_sfx_async_org = None
if not create_model_async_org:
    create_model_async_org = world.create_model_async
if not create_sfx_async_org:
    create_sfx_async_org = world.create_sfx_async

def create_model_async_for_delay_test(filename, callback, user_data=None, priority=game3d.ASYNC_MID, merge_config=None):

    def delay_callback(model, user_data, current_task):
        callback(model, user_data, current_task)

    def async_callback(model, user_data, current_task):
        global s_delay_model_time
        game3d.delay_exec(s_delay_model_time, delay_callback, (model, user_data, current_task))

    return create_model_async_org(filename, async_callback, user_data, priority, merge_config)


def create_sfx_async_for_delay_test(filename, callback, user_data=None, priority=game3d.ASYNC_MID, post_command=None):

    def delay_callback(sfx, user_data, current_task):
        callback(sfx, user_data, current_task)

    def async_callback(sfx, user_data, current_task):
        global s_delay_sfx_time
        game3d.delay_exec(s_delay_sfx_time, delay_callback, (sfx, user_data, current_task))

    return create_sfx_async_org(filename, async_callback, user_data, priority, post_command)


def enable_async_delay_test(enable, delay_model_time=1000, delay_sfx_time=1000):
    global s_delay_sfx_time
    global s_delay_model_time
    if enable:
        world.create_model_async = create_model_async_for_delay_test
        world.create_sfx_async = create_sfx_async_for_delay_test
    else:
        world.create_model_async = create_model_async_org
        world.create_sfx_async = create_sfx_async_org
    s_delay_model_time = delay_model_time
    s_delay_sfx_time = delay_sfx_time


if game3d.get_platform() == game3d.PLATFORM_WIN32:
    six.moves.builtins.__dict__['enable_async_delay_test'] = enable_async_delay_test