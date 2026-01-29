# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/action_proto.py
from __future__ import absolute_import
from logic.gcommon.const import USE_FLOAT_REDUCE
import logic.gcommon.common_utils.float_reduce_util as fl_reduce
import math3d
import logic.gcommon.common_const.animation_const as animation_const

def on_sync_agl(synchronizer, t, agl_v3d, agl_vel, agl_acc):
    synchronizer.send_event('E_ACTION_SYNC_RC_AGL', t, agl_v3d, agl_vel, agl_acc)


def on_sync_euler3(synchronizer, yaw, pitch, roll):
    synchronizer.send_event('E_ACTION_SYNC_RC_EULER', yaw, pitch, roll)


def acc_dir(synchronizer, lst_pd_pos, lst_dir, i_move_type):
    v3d_pos = math3d.vector(*lst_pd_pos)
    synchronizer.send_event('E_ACTION_SYNC_RC_DIR', v3d_pos, i_move_type)


def acc_yaw(synchronizer, f_yaw, f_dt=0):
    synchronizer.send_event('E_ACTION_SYNC_RC_YAW', f_yaw, f_dt)


def force_yaw(synchronizer, f_yaw):
    synchronizer.send_event('E_ACTION_SYNC_RC_FORCE_YAW', f_yaw)


def force_avatar_yaw(synchronizer, f_yaw):
    if synchronizer.ev_g_is_avatar():
        cur_yaw = synchronizer.ev_g_yaw() or 0
        global_data.emgr.fireEvent('camera_set_yaw_event', f_yaw)
        global_data.emgr.fireEvent('camera_set_pitch_event', 0)
        synchronizer.send_event('E_DELTA_YAW', f_yaw - cur_yaw)


def trigger_head_pitch(synchronizer, f_head_pitch):
    if f_head_pitch is None:
        return
    else:
        synchronizer.send_event('E_ACTION_SYNC_RC_HEAD_PITCH', f_head_pitch)
        return


def rb_pos(synchronizer, lst_pos, i_reason=None):
    if not lst_pos:
        return
    else:
        synchronizer.send_event('E_ACTION_SYNC_RB_POS', lst_pos, i_reason)
        owner = synchronizer.unit_obj.get_owner()
        if owner and owner.__class__.__name__ == 'Avatar':
            owner.do_sync_time() if owner else None
        global_data.ui_mgr.close_ui('GMHelperUI')
        return


def acc_cam_yaw(synchronizer, f_yaw, f_yaw_speed):
    synchronizer.send_event('E_ACTION_SYNC_RC_CAM_YAW', f_yaw, f_yaw_speed)


def acc_cam_pitch(synchronizer, f_pitch, f_dt):
    synchronizer.send_event('E_ACTION_SYNC_RC_CAM_PITCH', f_pitch, f_dt)


def move_sync_all(synchronizer, t, idx, lst_pos, lst_vel, acc):
    if USE_FLOAT_REDUCE:
        lst_pos = fl_reduce.i3_to_f3(*lst_pos)
        lst_vel = fl_reduce.i3_to_f3(*lst_vel)
    v3d_pos = math3d.vector(*lst_pos)
    v3d_vel = math3d.vector(*lst_vel)
    v3d_acc = math3d.vector(0, acc, 0)
    synchronizer.send_event('E_ACTION_SYNC_RC_ALL', t, idx, v3d_pos, v3d_vel, v3d_acc)


def move_sync_rel(synchronizer, t, idx, rel_ent_id, lst_rel_pos, lst_vel):
    if USE_FLOAT_REDUCE and lst_rel_pos:
        lst_rel_pos = fl_reduce.i3_to_f3(*lst_rel_pos)
        v3d_rel_pos = math3d.vector(*lst_rel_pos)
    else:
        v3d_rel_pos = None
    v3d_vel = math3d.vector(*lst_vel)
    synchronizer.send_event('E_ACTION_SYNC_RC_REL', t, idx, rel_ent_id, v3d_rel_pos, v3d_vel)
    return


def move_sync_teleport(synchronizer, t, idx, lst_pos, lst_vel, acc):
    if USE_FLOAT_REDUCE:
        lst_pos = fl_reduce.i3_to_f3(*lst_pos)
        lst_vel = fl_reduce.i3_to_f3(*lst_vel)
    v3d_pos = math3d.vector(*lst_pos)
    v3d_vel = math3d.vector(*lst_vel)
    v3d_acc = math3d.vector(0, acc, 0)
    synchronizer.send_event('E_ACTION_SYNC_RC_TELEPORT', t, idx, v3d_pos, v3d_vel, v3d_acc)


def cam_state(synchronizer, cam_state):
    synchronizer.send_event('E_ACTION_SYNC_CAM_STATE', cam_state)


def move_path(synchronizer, start_timestamp, speed, acc, start_point, end_point):
    synchronizer.send_event('E_MOVE_PATH', start_timestamp, speed, acc, start_point, end_point)


def swt_act_st(synchronizer, status):
    synchronizer.send_event('E_ACTION_SYNC_RC_STATUS', status)


def mv_act_jump(synchronizer, jump_state):
    synchronizer.send_event('E_ACTION_SYNC_RC_JUMP', jump_state)


def mv_act_roll(synchronizer):
    synchronizer.send_event('E_CTRL_ROLL')


def do_climb(synchronizer, climb_type, lst_pos, climb_rotation):
    synchronizer.send_event('E_ACTION_SYNC_RC_CLIMB', climb_type, lst_pos, climb_rotation)


def move_on_ground(synchronizer, f_vert_vel):
    synchronizer.send_event('E_ACTION_SYNC_GROUND', f_vert_vel)


def action_sync_forawrd(synchronizer, lst_dir):
    synchronizer.send_event('E_ACTION_SYNC_FORWARD', lst_dir)


def action_sync_attr(synchronizer, key, val):
    synchronizer.send_event('E_ACTION_SYNC_RC_ATTR', key, val)


def sync_move_state(synchronizer, i_state):
    synchronizer.send_event('E_MOVE_STATE', i_state)
    if i_state in (animation_const.MOVE_STATE_WALK, animation_const.MOVE_STATE_RUN):
        import math3d
        synchronizer.send_event('E_ACTION_MOVE', math3d.vector(0, 0, 1))


def robot_use_phys(synchronizer):
    synchronizer.send_event('E_ROBOT_USE_PHYS')


def set_control_target_none_with_pos(synchronizer, lst_pos):
    import math3d
    synchronizer.send_event('E_SET_CONTROL_TARGET', None, {'reset_pos': math3d.vector(*lst_pos)})
    return


def on_sync_anim_rate(synchronizer, part_of_body, f_rate):
    synchronizer.send_event('E_ANIM_RATE', part_of_body, f_rate)


def on_attr_change_msg(synchronizer, source_info, attr, pre_value, cur_value):
    from logic.client.const.game_mode_const import Hide_EquipmentMsg
    if global_data.game_mode.is_mode_type(Hide_EquipmentMsg):
        return
    else:
        if source_info:
            from logic.gcommon.common_const import attr_const
            from logic.gcommon.common_const import battle_const
            from logic.gcommon.item import item_utility as iutil
            from logic.gutils import template_utils
            from common.cfg import confmgr
            msg_type, item_id = source_info
            if msg_type not in [attr_const.ATTR_CHANGE_SOURCE_ARMOR]:
                return
            item_id = source_info[1]
            item_pos = iutil.get_clothing_dress_pos(item_id)
            attr_dict = confmgr.get('attr_config', attr, default={})
            txt_id = attr_dict.get('cDescID')
            name_id = attr_dict.get('name_id', None)
            plus_icon_path = attr_dict.get('icon_path', '')
            lv = confmgr.get('item', str(item_id), default={}).get('level', 0)
            bar_base_path = 'gui/ui_res_2/battle/notice/battle_get_tip/frame_reward_%s_pnl.png'
            bar_path = template_utils.get_quality_pic_path_ext(bar_base_path, lv)
            from logic.comsys.battle.BattleMedRCommonInfo import BattleMedRCommonInfo
            weak = synchronizer.ev_g_in_mecha_only()
            msg = {}
            if weak:
                i_t = battle_const.MED_R_EQUIPMENT_INFO_WEAK
                from logic.gutils.item_utils import get_item_name
                content = BattleMedRCommonInfo.get_weak_content_text(lv, get_item_name(item_id))
            else:
                i_t = battle_const.MED_R_EQUIPMENT_INFO
                from logic.gcommon.common_utils.local_text import get_text_by_id
                content = get_text_by_id(txt_id) if txt_id else ''
                name_text = get_text_by_id(name_id) if name_id else ''
                if name_text:
                    plus = name_text + ' '
                else:
                    plus = ''
                plus += '+%d' % int(cur_value * 100)
                msg['plus_text'] = plus
                msg['plus_icon_path'] = plus_icon_path
            msg.update({'i_type': i_t,
               'content_txt': content,
               'item_pos': item_pos,
               'bar_path': bar_path,
               'in_anim': BattleMedRCommonInfo.get_anim_name('show', lv),
               'out_anim': BattleMedRCommonInfo.get_anim_name('hide', lv),
               'hide_nodes': [
                            'bar_module']
               })
            if item_id:
                msg['item_id'] = item_id
            global_data.emgr.show_battle_med_r_message.emit(msg, battle_const.MED_R_NODE_COMMON_INFO)
        return


def on_show_fix_stuck_btn(synchronizer, show):
    if show and not global_data.ui_mgr.get_ui('GMHelperUI'):
        from logic.comsys.control_ui.GMHelperUIFactory import GMHelperUIFactory
        import logic.gcommon.common_const.battle_const as battle_const
        if synchronizer.ev_g_is_avatar() and synchronizer.ev_g_is_cam_target():
            GMHelperUIFactory.create_gm_helper_ui(reason=battle_const.TRY_TELE_POS_REASON_HMAP)
    elif not show and global_data.ui_mgr.get_ui('GMHelperUI'):
        global_data.ui_mgr.close_ui('GMHelperUI')


def rc_offset(synchronizer, tp_off):
    if not tp_off:
        synchronizer.send_event('E_CLEAR_RC_OFFSET')
    else:
        synchronizer.send_event('E_RC_OFFSET', tp_off)


def sync_yaw(synchronizer, yaw, dt):
    synchronizer.send_event('E_SYNC_YAW', yaw, dt)


def sync_pitch(synchronizer, pitch, dt):
    synchronizer.send_event('E_SYNC_PITCH', pitch, dt)


def sync_rtt(synchronizer, rtt):
    synchronizer.send_event('E_SYNC_RTT', rtt)


def kongdao_fall_stage(synchronizer, stage, *args):
    synchronizer.send_event('E_KONGDAO_FALL_STAGE', stage, *args)