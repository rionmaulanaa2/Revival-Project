# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/ai_log_proto.py
from __future__ import absolute_import
from logic.gcommon.const import USE_FLOAT_REDUCE
import logic.gcommon.common_utils.float_reduce_util as fl_reduce
import math3d
import logic.gcommon.common_const.animation_const as animation_const

def notify_send_aicollect_log(synchronizer, step):
    synchronizer.send_event('E_DO_NOTIFIED_AI_LOG_COLLECT', step)


def sunshine_set_ai_name(synchronizer, eid, ai_name):
    if global_data.sunshine_editor:
        global_data.sunshine_editor.teldrassil_plugin.GetServer().SetAIName(str(eid), ai_name)


def sunshine_push_debug_info(synchronizer, debugInfo):
    if global_data.sunshine_editor:
        global_data.sunshine_editor.teldrassil_plugin.GetServer().PushDebugInfo(debugInfo)


def sunshine_synchronize_state(synchronizer, state):
    if global_data.sunshine_editor:
        global_data.sunshine_editor.teldrassil_plugin.GetServer().SynchronizeState(state)


def sunshine_get_test_result(synchronizer, aiName, data):
    if global_data.sunshine_editor:
        global_data.sunshine_editor.teldrassil_plugin.GetServer().AIProfileResult(aiName, data)