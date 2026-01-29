# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/button_custom_process_func.py
from __future__ import absolute_import

def rocker_preprocess_func(adjust_node, start_node, custom_conf):
    try:
        img_ruler = getattr(start_node, 'img_ruler')
        nd_keep_running_custom = getattr(start_node, 'nd_keep_running_custom')
        rocker = getattr(start_node, 'rocker')
        wpos_1 = nd_keep_running_custom.getParent().convertToWorldSpace(nd_keep_running_custom.getPosition())
        wpos_2 = rocker.getParent().convertToWorldSpace(rocker.getPosition())
        lpos_1 = img_ruler.getParent().convertToNodeSpace(wpos_1)
        lpos_2 = img_ruler.getParent().convertToNodeSpace(wpos_2)
        height = lpos_1.y - lpos_2.y
        old_size = img_ruler.GetContentSize()
        img_ruler.SetContentSize(old_size[0], height - 40)
    except Exception as e:
        log_error('node_name for rocker_preprocess_func unexisted')


def is_enable_left_shot_without_move(custom_id):
    if not global_data.player:
        return False
    import logic.gcommon.common_const.ui_operation_const as uoc
    left_fire_ope, left_fire_ope_move = global_data.player.get_setting(uoc.LF_OPE_KEY)
    if left_fire_ope != uoc.LEFT_FIRE_ALWAYS_CLOSE:
        if left_fire_ope_move == uoc.LF_ONLY_SHOT:
            return True
    elif left_fire_ope == uoc.LEFT_FIRE_ALWAYS_CLOSE:
        return True
    return False


def is_enable_left_shot_with_move(custom_id):
    if not global_data.player:
        return False
    import logic.gcommon.common_const.ui_operation_const as uoc
    left_fire_ope, left_fire_ope_move = global_data.player.get_setting(uoc.LF_OPE_KEY)
    if left_fire_ope != uoc.LEFT_FIRE_ALWAYS_CLOSE:
        if left_fire_ope_move == uoc.LF_SHOT_AND_MOVE:
            return True
    return False