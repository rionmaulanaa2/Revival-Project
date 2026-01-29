# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateWidget/TeammateWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const import ui_battle_const as ubc
from logic.gcommon.common_const.battle_const import LOCATE_NORMAL, LOCATE_DEAD, LOCATE_RECOURSE, LOCATE_DRIVE, LOCATE_PARACHUTE, LOCATE_OFFLINE, LOCATE_MECHA, LOCATE_PARACHUTE_PREPARE, LOCATE_FOLLOW, LOCATE_MECHA_TRANS, LOCATE_SKATE, LOCATE_COCKPIT
from logic.gutils import template_utils
from logic.gcommon.common_utils.parachute_utils import STAGE_PLANE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND, STAGE_LAUNCH_PREPARE, STAGE_MECHA_READY, STAGE_NONE, STAGE_ISLAND
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const import mecha_const
from logic.gutils.team_utils import get_team_bottom_pic_path
from logic.client.const import game_mode_const
from logic.gutils import mecha_utils
from logic.gutils.item_utils import get_locate_circle_path
from logic.gcommon.common_const.battle_const import MARK_NORMAL
from logic.gcommon.common_const.team_const import NAME_COLOR
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_NO_ATTACHABLE
import cc

class TeammateBloodBarUI(object):

    def __init__(self, nd_bloodbar):
        self.nd_bloodbar = nd_bloodbar
        self.cur_status = None
        self.need_check_mecha_shield = False
        return

    percent_dict = {ubc.HP_BAR_MECHA: 'gui/ui_res_2/battle/progress/locate_hp_blue.png',
       ubc.HP_BAR_NORMAL_PERCENT: 'gui/ui_res_2/battle/progress/locate_hp_white.png',
       ubc.HP_BAR_DANGER_PERCENT: 'gui/ui_res_2/battle/progress/locate_hp_red.png'
       }

    def get_bar_status(self, teammate):
        if teammate:
            is_dying = teammate.ev_g_agony()
            is_die = teammate.ev_g_death()
            is_in_mecha = teammate.ev_g_in_mecha()
        else:
            is_die = True
            is_dying = False
            is_in_mecha = False
        is_mecha_shield = False
        if is_die:
            percent = 0
        elif is_dying:
            percent = teammate.ev_g_agony_hp_percent() * 100
        elif is_in_mecha:
            mecha = teammate.ev_g_control_target()
            percent = 100
            if mecha and mecha.logic and mecha.__class__.__name__ == 'Mecha':
                if self.need_check_mecha_shield:
                    percent = mecha.logic.ev_g_shield_percent() * 100
                    if percent > 0:
                        is_mecha_shield = True
                    else:
                        percent = mecha.logic.ev_g_health_percent() * 100
                        percent = 99.9 if percent >= 100 else percent
                else:
                    percent = mecha.logic.ev_g_health_percent() * 100
                    percent = 99.9 if percent >= 100 else percent
        else:
            percent = teammate.ev_g_health_percent() * 100
        if is_mecha_shield:
            bar_status = ubc.HP_BAR_SHIELD
        elif is_dying:
            bar_status = ubc.HP_BAR_DANGER_PERCENT
        else:
            bar_status = self.get_hp_bar_status(percent, is_in_mecha)
        pic = self.percent_dict.get(bar_status)
        return (
         pic, percent)

    def update_health(self, teammate):
        if not self.nd_bloodbar:
            return
        pic, percent = self.get_bar_status(teammate)
        if self.cur_status != pic:
            self.switch_texture(pic)
            self.cur_status = pic
        self.setPercent(percent)

    def switch_texture(self, pic):
        self.nd_bloodbar.hp_progress.SetProgressTexture(pic)

    def setPercent(self, percent):
        self.nd_bloodbar.hp_progress.SetPercentage(percent)

    def get_hp_bar_status(self, percent, in_mecha):
        if in_mecha:
            return ubc.HP_BAR_MECHA
        else:
            if percent >= ubc.HP_BAR_WARNING_PERCENT:
                return ubc.HP_BAR_NORMAL_PERCENT
            return ubc.HP_BAR_DANGER_PERCENT

    def destroy(self):
        self.nd_bloodbar = None
        return

    def init_by_teammate_dict(self, info):
        self._info = dict(info)
        dead = self._info.get('dead', False)
        if dead:
            percent = 0
            is_in_mecha = False
            percent_status = self.get_hp_bar_status(percent, is_in_mecha)
            pic = self.percent_dict.get(percent_status)
            self.switch_texture(pic)


class TeammateBloodBarUI2(TeammateBloodBarUI):
    percent_dict = {ubc.HP_BAR_NORMAL_PERCENT: 'gui/ui_res_2/battle/progress/hp_teammate_100.png',
       ubc.HP_BAR_WARNING_PERCENT: 'gui/ui_res_2/battle/progress/hp_teammate_75.png',
       ubc.HP_BAR_DANGER_PERCENT: 'gui/ui_res_2/battle/progress/hp_teammate_25.png'
       }

    def __init__(self, nd_bloodbar, color):
        super(TeammateBloodBarUI2, self).__init__(nd_bloodbar)
        self.is_ui_grayed = None
        self._color = color
        self.mecha_in_danger = False
        self.update_unit_width(mecha_utils.get_mecha_blood_unit_count())
        self.pure_mecha_mode = global_data.game_mode.is_mode_type(game_mode_const.TeamBloodUI_PURE_MECHA)

        @self.nd_bloodbar.hp_progress.unique_callback()
        def OnSetPercentage(pr, percent):
            self.nd_bloodbar.img_hp_danger.setVisible(percent <= ubc.HP_BAR_WARNING_PERCENT)
            if percent > ubc.HP_BAR_WARNING_PERCENT:
                pic_path = 'gui/ui_res_2/battle/progress/hp_teammate_top.png'
            else:
                pic_path = 'gui/ui_res_2/battle/progress/hp_teammate_top_25.png'
            self.nd_bloodbar.hp_head.SetDisplayFrameByPath('', pic_path)
            sz = self.nd_bloodbar.hp_head.getParent().getContentSize()
            self.nd_bloodbar.hp_head.setPositionX(sz.width * percent / 100)

        return

    def update_unit_width(self, v):
        self.unit_width = v
        self.set_unit_params(self.nd_bloodbar.hp_mech_progress, v)

    def set_unit_params(self, nd, unit, scalar=0.5, gap_unit=None):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_Xinterval', unit / 2)
        programState.setUniformFloat('_Yinterval', 0)
        programState.setUniformFloat('_Scalar', scalar)
        if gap_unit is not None:
            programState.setUniformFloat('_Emptyinterval', gap_unit)
        return

    def set_progress_params(self, nd, hp, shield, other_shield):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_XBlood', hp)
        programState.setUniformFloat('_YBlood', shield)
        programState.setUniformFloat('_ZBlood', other_shield)

    def set_ratio_params(self, nd, max_hp, max_shield, other_shield, ratio=0.5):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_X', max_hp)
        programState.setUniformFloat('_Y', max_shield)
        programState.setUniformFloat('_Z', other_shield)

    def get_hp_bar_status(self, percent, in_mecha):
        if in_mecha:
            return ubc.HP_BAR_MECHA
        else:
            if percent >= ubc.HP_BAR_NORMAL_PERCENT:
                return ubc.HP_BAR_NORMAL_PERCENT
            if percent >= ubc.HP_BAR_WARNING_PERCENT:
                return ubc.HP_BAR_WARNING_PERCENT
            return ubc.HP_BAR_DANGER_PERCENT

    def update_health(self, teammate):
        if not self.nd_bloodbar:
            return
        if teammate and teammate.is_valid():
            is_dying = teammate.ev_g_agony()
            is_die = teammate.ev_g_death()
            is_online = teammate.ev_g_connect_state()
            is_in_mecha = teammate.ev_g_in_mecha()
            is_in_summon_mecha = teammate.ev_g_in_mecha('Mecha')
            if self.pure_mecha_mode:
                if not is_in_summon_mecha:
                    is_die = True
        else:
            is_die = True
            is_dying = False
            is_online = False
            is_in_mecha = False
            is_in_summon_mecha = False
        self.switch_ui_gray(is_die)
        self.switch_hp_nd(is_in_summon_mecha)
        if is_in_summon_mecha:
            mecha = teammate.ev_g_control_target()
            self.update_mecha_health(mecha)
            return
        if is_die:
            percent = 0
            self.nd_bloodbar.hp_shield.setVisible(False)
        elif is_dying:
            percent = teammate.ev_g_agony_hp_percent() * 100
            self.nd_bloodbar.hp_shield.setVisible(False)
        else:
            max_hp = teammate.ev_g_max_hp()
            cur_hp = teammate.ev_g_hp()
            temporary_shield = teammate.ev_g_sum_temporary_shield() or 0
            max_shield = teammate.ev_g_max_shield() + temporary_shield
            cur_shield = teammate.ev_g_shield() + temporary_shield
            percent = template_utils.get_human_cur_hp_percent(cur_hp, max_hp, cur_shield, max_shield)
            self.nd_bloodbar.hp_shield.setVisible(cur_shield > 0)
            if cur_shield > 0:
                shield_percent = template_utils.get_human_cur_shield_percent(cur_hp, max_hp, cur_shield, max_shield)
                self.nd_bloodbar.hp_shield.SetPercentage(shield_percent)
        percent_status = self.get_hp_bar_status(percent, False)
        if self.cur_status != (is_dying, percent_status):
            pic = self.percent_dict.get(percent_status)
            if is_dying:
                self.nd_bloodbar.hp_progress.SetProgressTexture('gui/ui_res_2/battle/progress/hp_teammate_0.png')
            else:
                self.nd_bloodbar.hp_progress.SetProgressTexture(pic)
            self.cur_status = (is_dying, percent_status)
        self.nd_bloodbar.hp_progress.SetPercentage(percent)

    def switch_ui_gray(self, is_die):
        from logic.comsys.effect import ui_effect
        if self.is_ui_grayed is None or is_die != self.is_ui_grayed:
            if is_die:
                if self.nd_bloodbar.sp_locate:
                    ui_effect.set_gray(self.nd_bloodbar.sp_locate, True)
                if self.nd_bloodbar.teamate_name:
                    self.nd_bloodbar.teamate_name.SetColor('#DC')
            else:
                if self.nd_bloodbar.sp_locate:
                    ui_effect.set_gray(self.nd_bloodbar.sp_locate, False)
                if self.nd_bloodbar.teamate_name:
                    self.nd_bloodbar.teamate_name.SetColor('#DW')
            self.is_ui_grayed = is_die
        return

    def switch_hp_nd(self, is_mecha):
        is_mecha = bool(is_mecha)
        self.nd_bloodbar.hp_progress.setVisible(not is_mecha)
        self.nd_bloodbar.hp_mech_progress.setVisible(is_mecha)
        self.nd_bloodbar.img_hp_danger.setVisible(not is_mecha)
        self.nd_bloodbar.hp_head.setVisible(not is_mecha)

    def update_mecha_health(self, mecha):
        if not (mecha and mecha.logic):
            return
        mecha = mecha.logic
        Value = mecha.get_value
        hp_max = Value('G_MAX_HP')
        hp = Value('G_HP')
        if hp > hp_max:
            hp = hp_max
        shield = Value('G_SHIELD')
        shield_max = Value('G_MAX_SHIELD')
        outer_shield = Value('G_OUTER_SHIELD') or 0
        temporary_shield = Value('G_SUM_TEMPORARY_SHIELD') or 0
        other_shield = outer_shield + temporary_shield
        if shield > shield_max:
            shield = shield_max
        mecha_in_danger = hp < hp_max * 0.25
        if self.mecha_in_danger ^ mecha_in_danger:
            self.nd_bloodbar.hp_mech_progress.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/mech_main/hp_mech_25.png')
        else:
            self.nd_bloodbar.hp_mech_progress.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/mech_main/hp_mech_100.png')
        self.mecha_in_danger = mecha_in_danger
        self.set_ratio_params(self.nd_bloodbar.hp_mech_progress, hp, shield, hp_max + shield_max + other_shield - hp - shield)
        self.set_progress_params(self.nd_bloodbar.hp_mech_progress, hp, shield, other_shield)


class TeammateStatusUI(object):
    DELAY_TAG = 10001
    ID_PIC_PATH = [
     'gui/ui_res_2/battle/icon/icon_teammate_num_blue.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_green.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_yellow.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_red.png']

    def __init__(self, status_nd, color, player_num=None):
        self._nd = status_nd
        self._color = color
        self.is_play_fire_ani = False
        self._binded_events = {}
        self.nd_type = None
        self.follow_id = None
        self._mecha_id = None
        self._entity_id = None
        if player_num != None:
            status_nd.lab_num.SetString(str(player_num))
            pic_path = get_locate_circle_path(color)
            status_nd.hp_progress.SetDisplayFrameByPath('', pic_path)
        self.pure_mecha_mode = global_data.game_mode.is_mode_type(game_mode_const.TeamBloodUI_PURE_MECHA)
        return

    def destroy(self):
        if self._nd and self._nd.isValid():
            self._nd.stopActionByTag(self.DELAY_TAG)
        self._nd = None
        return

    def on_fire(self):
        if not self._nd.IsPlayingAnimation('fire'):
            self.is_play_fire_ani = True
            if self._nd.img_fire:
                self._nd.img_fire.setVisible(True)
            self.show_state_icon()
            self._nd.PlayAnimation('fire')
            self._nd.stopActionByTag(self.DELAY_TAG)
            delay = self._nd.GetAnimationMaxRunTime('fire')

            def _finshed():
                self.is_play_fire_ani = False
                if self._nd.img_fire:
                    self._nd.img_fire.setVisible(False)
                self.show_state_icon()

            self._nd.DelayCallWithTag(delay, lambda : _finshed(), self.DELAY_TAG)

    def refresh_mvp(self):
        self.show_state_icon()

    def update_teammate_status(self, teammate):
        self._entity_id = teammate.id
        is_online = teammate.ev_g_connect_state()
        if not is_online:
            return LOCATE_OFFLINE
        else:
            is_death = teammate.ev_g_death()
            if is_death:
                return LOCATE_DEAD
            is_dying = teammate.ev_g_agony()
            if is_dying:
                return LOCATE_RECOURSE
            is_mecha = teammate.ev_g_in_mecha('Mecha')
            if is_mecha:
                self._mecha_id = teammate.ev_g_get_bind_mecha_type()
                return LOCATE_MECHA
            if self.pure_mecha_mode:
                return LOCATE_DEAD
            self._mecha_id = None
            is_mecha_trans = teammate.ev_g_in_mecha('MechaTrans')
            if is_mecha_trans:
                return LOCATE_MECHA_TRANS
            is_skateboard = teammate.ev_g_attachable_by_id(ITEM_NO_ATTACHABLE)
            if is_skateboard:
                return LOCATE_SKATE
            is_following = self.check_show_follow(teammate)
            is_cockpit = self.check_is_in_cockpit(teammate)
            if is_cockpit:
                return LOCATE_COCKPIT
            is_driving = self.check_is_in_drive(teammate)
            if is_driving:
                return LOCATE_DRIVE
            is_in_parachute = self.check_is_in_parachute(teammate)
            if is_in_parachute:
                return LOCATE_PARACHUTE
            return LOCATE_NORMAL

    def check_show_follow(self, lteammate):
        if lteammate.is_valid():
            stage = lteammate.share_data.ref_parachute_stage
            flag = stage in (STAGE_MECHA_READY, STAGE_PLANE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAUNCH_PREPARE, STAGE_NONE, STAGE_ISLAND)
            self.follow_id = lteammate.ev_g_parachute_follow_target()
            return flag and self.follow_id is not None
        else:
            self.follow_id = None
            return False

    def check_is_in_drive(self, lteammate):
        if lteammate.is_valid():
            is_in_vehicle = lteammate.ev_g_is_in_any_state((
             status_config.ST_MECHA_DRIVER, status_config.ST_MECHA_PASSENGER, status_config.ST_VEHICLE_GUNNER, status_config.ST_VEHICLE_PASSENGER))
            if is_in_vehicle:
                return True
        return False

    def check_is_in_cockpit(self, lteammate):
        if lteammate.is_valid():
            if lteammate.share_data.ref_parachute_stage in (STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE, STAGE_LAUNCH_PREPARE, STAGE_FREE_DROP):
                return True
        return False

    def check_is_in_parachute(self, lteammate):
        if lteammate.is_valid():
            if lteammate.share_data.ref_parachute_stage in (STAGE_PARACHUTE_DROP,):
                return True
        return False

    def set_teammate_icon(self, new_type):
        from logic.gutils.item_utils import get_locate_icon_bg_path, get_locate_pic_path
        player_node = self._nd
        player_color = self._get_player_color_name()
        bg_path = get_locate_icon_bg_path(player_color)
        icon_path = get_locate_pic_path(new_type, player_color, self._mecha_id)
        if player_node.sp_locate:
            player_node.sp_locate.SetDisplayFrameByPath('', bg_path)
        if player_node.img_locate:
            player_node.img_locate.SetDisplayFrameByPath('', icon_path)
        if player_node.img_jump:
            show_img_jump = new_type in (LOCATE_COCKPIT, LOCATE_PARACHUTE)
            player_node.img_jump.setVisible(show_img_jump)
            show_img_jump and player_node.img_jump.SetDisplayFrameByPath('', icon_path)
        if player_node.img_follow:
            if self.follow_id and global_data.cam_lplayer:
                idx = global_data.cam_lplayer.ev_g_groupmate().index(self.follow_id)
                if idx is not None:
                    player_node.img_follow.setVisible(True)
                    player_node.img_follow.SetDisplayFrameByPath('', self.ID_PIC_PATH[idx])
                else:
                    player_node.img_follow.setVisible(False)
            else:
                player_node.img_follow.setVisible(False)
        self.nd_type = new_type
        self.show_state_icon()
        return

    def show_state_icon(self):
        if not self._nd.img_locate:
            return
        else:
            self._nd.img_locate.setVisible(self.nd_type not in (LOCATE_NORMAL, LOCATE_COCKPIT, LOCATE_PARACHUTE))
            if self._nd.nd_mvp:
                self.refresh_show_mvp()
            sort_list = [
             self._nd.img_jump, self._nd.nd_mvp, self._nd.img_locate, self._nd.nd_mech, self._nd.img_fire]
            cur_pos = None
            for nd_state in sort_list:
                if not nd_state:
                    continue
                cur_pos = nd_state.getPosition()
                break

            if cur_pos:
                for nd_state in sort_list:
                    if not nd_state:
                        continue
                    if nd_state.isVisible():
                        nd_state.setPosition(cur_pos)
                        cur_pos.x += 41

            return

    def refresh_show_mvp(self):
        if not global_data.battle:
            return
        if not global_data.cam_lplayer:
            return
        self._nd.nd_mvp.setVisible(False)
        mvp_id = global_data.battle.get_mvp_id()
        if mvp_id and self._entity_id != global_data.cam_lplayer.id and mvp_id == self._entity_id:
            self._nd.nd_mvp.setVisible(True)

    def _get_player_color_name(self):
        return self._color

    def update_status(self, teammate):
        if teammate:
            status = self.update_teammate_status(teammate)
        else:
            status = LOCATE_DEAD
        self.set_teammate_icon(status)
        return status

    def init_by_teammate_dict(self, info):
        self._info = dict(info)
        dead = self._info.get('dead', False)
        if dead:
            self.set_teammate_icon(LOCATE_DEAD)


class TeammateStatusUI2(TeammateStatusUI):

    def update_status(self, teammate):
        status = super(TeammateStatusUI2, self).update_status(teammate)
        if status == LOCATE_RECOURSE:
            self._nd.PlayAnimation('down')
        else:
            self._nd.StopAnimation('down')


from logic.gcommon.common_const import mecha_const as mconst

class JudgeTeammateStatusUI(TeammateStatusUI2):

    def update_status(self, teammate, pid):
        super(JudgeTeammateStatusUI, self).update_status(teammate)
        from logic.gutils import judge_utils
        player_info = judge_utils.get_global_player_info(pid)
        banned = self._refresh_mech_node(self._nd.nd_mech, player_info.get('in_mecha_type', mconst.MECHA_TYPE_NONE) == mconst.MECHA_TYPE_NORMAL, player_info.get('mecha_id', 0), player_info.get('recall_cd_type', mconst.RECALL_CD_TYPE_NORMAL), player_info.get('recall_cd', 0), player_info.get('recall_cd_end_ts', 0))
        if not banned:
            if self._nd.img_locate.isVisible():
                self._nd.nd_mech.setVisible(False)

    def _refresh_mech_node(self, mech_node, in_mecha, mecha_id, mecha_recall_cd_type, mecha_recall_cd, mecha_recall_cd_end_ts):
        show_cd = False
        banned = False
        if not mecha_id:
            show_mech_node = False
        elif in_mecha:
            show_mech_node = True
        else:
            show_mech_node = False
            if mecha_recall_cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
                show_mech_node = True
                banned = True
            elif mecha_recall_cd_type == mconst.RECALL_CD_TYPE_NORMAL or mecha_recall_cd_type == mconst.RECALL_CD_TYPE_DIE:
                from logic.gcommon.time_utility import get_server_time_battle
                left_time = mecha_recall_cd_end_ts - get_server_time_battle()
                if left_time > 0:
                    show_mech_node = True
                    show_cd = True
        if show_mech_node:
            mech_node.setVisible(True)
            from logic.gcommon.common_const.battle_const import LOCATE_MECHA
            from logic.gutils.item_utils import get_locate_pic_path
            mech_node.img_mech.SetDisplayFrameByPath('', get_locate_pic_path(LOCATE_MECHA, None, mecha_id))
            mech_node.nd_ban.setVisible(banned)
            if show_cd:
                mech_node.nd_cd.setVisible(True)

                def refresh_count_down(dt, _left_time=left_time):
                    if _left_time <= 0:
                        return
                    _left_time -= dt
                    if _left_time > 0:
                        mech_node.nd_cd.lab_cd.SetString('%.1f' % _left_time)
                    else:
                        banned = self._refresh_mech_node(mech_node, in_mecha, mecha_id, mecha_recall_cd_type, mecha_recall_cd, 0)
                        if not banned:
                            if self._nd:
                                if self._nd.img_locate.isVisible():
                                    self._nd.nd_mech.setVisible(False)

                mech_node.nd_cd.TimerAction(refresh_count_down, left_time, interval=0.05)
                refresh_count_down(0.0)
            else:
                mech_node.nd_cd.setVisible(False)
                mech_node.nd_cd.StopTimerAction()
        else:
            mech_node.setVisible(False)
        return banned

    def set_teammate_icon(self, new_type):
        from logic.gutils.item_utils import get_locate_pic_path
        from logic.gcommon.common_const.battle_const import MAP_COL_WHITE
        player_node = self._nd
        icon_path = get_locate_pic_path(new_type, MAP_COL_WHITE, self._mecha_id)
        if player_node.img_locate:
            player_node.img_locate.SetDisplayFrameByPath('', icon_path)
        self.nd_type = new_type
        self.show_state_icon()


class TeammateFullStatusUI(TeammateStatusUI):

    def __init__(self, status_nd, color):
        super(TeammateFullStatusUI, self).__init__(status_nd, color)
        self.nd_normal_visible = False

    def update_teammate_status(self, teammate):
        return super(TeammateFullStatusUI, self).update_teammate_status(teammate)

    def set_teammate_icon(self, new_type):
        super(TeammateFullStatusUI, self).set_teammate_icon(new_type)
        if self.nd_type == LOCATE_NORMAL:
            self._nd.setVisible(self.nd_normal_visible)
        else:
            self._nd.setVisible(True)

    def set_nd_normal_visible(self, is_vis):
        self.nd_normal_visible = is_vis
        self._nd.setVisible(is_vis)


class TeammateParachuteStatusUI(object):

    def __init__(self, status_nd):
        self._nd = status_nd
        self.nd_type = LOCATE_NORMAL

    def destroy(self):
        self._nd = None
        return

    def update_status(self, teammate):
        if teammate:
            status = self.update_teammate_status(teammate)
        else:
            status = LOCATE_DEAD
        self.set_teammate_icon(status)
        return status

    def update_teammate_status(self, teammate):
        parachute_stage = teammate.share_data.ref_parachute_stage
        is_on_drop = parachute_stage in (STAGE_FREE_DROP, STAGE_PARACHUTE_DROP)
        is_on_land = parachute_stage == STAGE_LAND
        is_on_prepare = parachute_stage == STAGE_LAUNCH_PREPARE
        if is_on_drop:
            return LOCATE_PARACHUTE
        else:
            if is_on_land:
                return LOCATE_NORMAL
            if is_on_prepare:
                return LOCATE_PARACHUTE_PREPARE
            return None
            return None

    def set_teammate_icon(self, new_type):
        if new_type == self.nd_type:
            return
        self.nd_type = new_type
        if new_type == LOCATE_PARACHUTE:
            self._nd.prog_launch.stopAllActions()
            self._nd.prog_launch.SetPercent(100)
            self._nd.img_parachute.setVisible(False)
            self._nd.prog_launch.SetPercent(0)
        elif new_type == LOCATE_NORMAL:
            self._nd.prog_launch.stopAllActions()
            self._nd.prog_launch.SetPercent(100)
            self._nd.img_parachute.setVisible(False)
        elif new_type == LOCATE_PARACHUTE_PREPARE:
            self._nd.prog_launch.SetPercent(0)
            self._nd.prog_launch.SetPercent(100, 1.3)
            self._nd.PlayAnimation('launch')
        else:
            self._nd.prog_launch.stopAllActions()
            self._nd.prog_launch.SetPercent(0)
            self._nd.img_parachute.setVisible(False)


class TeammateFollowInfoUI(object):
    ID_PIC_PATH = [
     'gui/ui_res_2/battle/icon/icon_teammate_num_blue.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_green.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_yellow.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_red.png']
    BTN_FOLLOW_STATUS_NONE = 0
    BTN_FOLLOW_STATUS_CANCEL = 1
    BTN_FOLLOW_STATUS_FOLLOW = 2
    BTN_FOLLOW_STATUS_ASSIGN = 3
    ASSIGN_TIMER_TAG = 202010

    def __init__(self, nd_follow, has_teammate, self_id, eid_to_id_dict):
        self._nd = nd_follow
        self._follow_set = None
        self._eid = self_id
        self._following_id = -1
        self._btn_follow_status = self.BTN_FOLLOW_STATUS_NONE
        self._assign_count_down = 5
        self.eid_to_id_dict = eid_to_id_dict
        self._nd.nd_follow_set.setVisible(False)
        self._nd.nd_follow_set.setOpacity(0)
        if has_teammate:
            if self._eid != self.get_cur_watching_target_eid():
                self._follow_set = self._nd.nd_follow_set

                @self._follow_set.btn_follow.unique_callback()
                def OnClick(*args):
                    if not self._nd:
                        return
                    else:
                        if self._btn_follow_status == self.BTN_FOLLOW_STATUS_ASSIGN:
                            assign_id = self._eid
                            if global_data.cam_lplayer:
                                global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'request_transfer_parachute_leader', (assign_id,))
                            elif global_data.player and global_data.player.logic:
                                global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'request_transfer_parachute_leader', (assign_id,))
                            self._nd.btn_follow.SetEnable(False)
                            self._assign_count_down = 5
                            self._nd.btn_follow.stopActionByTag(self.ASSIGN_TIMER_TAG)
                            self._nd.btn_follow.SetText('5s')
                            action = cc.RepeatForever.create(cc.Sequence.create([
                             cc.DelayTime.create(1),
                             cc.CallFunc.create(self._update_assign_count_down)]))
                            action.setTag(self.ASSIGN_TIMER_TAG)
                            self._nd.btn_follow.runAction(action)
                        else:
                            if self._btn_follow_status == self.BTN_FOLLOW_STATUS_CANCEL:
                                cur_eid, c_name = self.get_cur_watching_target_following_eid(True)
                                c_name and global_data.game_mgr.show_tip(get_text_by_id(13045, {'playername': c_name}))
                                follow_id = None
                            else:
                                follow_id = self._eid
                            if global_data.cam_lplayer:
                                global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'follow_parachute', (follow_id,))
                            elif global_data.player and global_data.player.logic:
                                global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'follow_parachute', (follow_id,))
                        return

                @self._follow_set.btn_invite.unique_callback()
                def OnClick(*args):
                    if global_data.cam_lplayer:
                        global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'invite_parachute', (self._eid,))
                    elif global_data.player and global_data.player.logic:
                        global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'invite_parachute', (self._eid,))

        return

    def init_by_teammate(self, teammate):
        pass

    def _update_assign_count_down(self):
        self._assign_count_down -= 1
        if self._nd:
            if self._assign_count_down != 0:
                self._nd.btn_follow.SetText('{}s'.format(self._assign_count_down))
            elif self._btn_follow_status == self.BTN_FOLLOW_STATUS_ASSIGN:
                self._nd.btn_follow.SetText(get_text_by_id(19783))
                self._nd.btn_follow.SetEnable(True)
                self._nd.btn_follow.stopActionByTag(self.ASSIGN_TIMER_TAG)

    def get_cur_watching_target_eid(self):
        player_id = None
        if global_data.cam_lplayer:
            player_id = global_data.cam_lplayer.ev_g_player_id()
        if not player_id and global_data.player:
            player_id = global_data.player.id
        return player_id

    def get_cur_watching_target_following_eid(self, get_name=False):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer
        else:
            player = global_data.player.logic if global_data.player else None
        if player:
            return player.ev_g_parachute_follow_target(get_name)
        else:
            if get_name:
                return (None, None)
            return

    def update_follow_note(self, teammate):
        follow_target = teammate.ev_g_parachute_follow_target()
        if follow_target == self._following_id:
            return
        self._following_id = follow_target
        idx = self.eid_to_id_dict.get(self._following_id, -1)
        if self._following_id and idx >= 0:
            pic_path = self.ID_PIC_PATH[idx]
            self._nd.temp_status.img_follow.setVisible(True)
            self._nd.temp_status.img_follow.SetDisplayFrameByPath('', pic_path)
        else:
            self._nd.temp_status.img_follow.setVisible(False)

    def update_follow_btn(self, teammate):
        cur_watching_id = self.get_cur_watching_target_eid()
        if self._eid == cur_watching_id:
            return
        else:
            if teammate and teammate.is_valid():
                if teammate.share_data.ref_parachute_stage not in [STAGE_NONE, STAGE_PLANE, STAGE_ISLAND]:
                    self._follow_set.setVisible(False)
            cur_watching_target_following_eid = self.get_cur_watching_target_following_eid()
            if self._eid == cur_watching_target_following_eid:
                if self._btn_follow_status == self.BTN_FOLLOW_STATUS_CANCEL:
                    return
                self._nd.btn_follow.stopActionByTag(self.ASSIGN_TIMER_TAG)
                self._btn_follow_status = self.BTN_FOLLOW_STATUS_CANCEL
                self._nd.btn_follow.SetText(get_text_by_id(19002))
                self._nd.btn_follow.SetEnable(True)
                self._nd.btn_invite.SetEnable(False)
            elif self._following_id == cur_watching_id and cur_watching_target_following_eid is None:
                if self._btn_follow_status == self.BTN_FOLLOW_STATUS_ASSIGN:
                    return
                self._nd.btn_follow.stopActionByTag(self.ASSIGN_TIMER_TAG)
                self._btn_follow_status = self.BTN_FOLLOW_STATUS_ASSIGN
                self._nd.btn_follow.SetText(get_text_by_id(19783))
                self._nd.btn_follow.SetEnable(True)
                self._nd.btn_invite.SetEnable(False)
            else:
                if self._btn_follow_status != self.BTN_FOLLOW_STATUS_FOLLOW:
                    self._nd.btn_follow.stopActionByTag(self.ASSIGN_TIMER_TAG)
                    self._nd.btn_follow.SetText(get_text_by_id(13040))
                    self._btn_follow_status = self.BTN_FOLLOW_STATUS_FOLLOW
                if self._following_id and self._following_id == cur_watching_target_following_eid:
                    flag = False
                else:
                    flag = True
                self._nd.btn_follow.SetEnable(flag)
                self._nd.btn_invite.SetEnable(flag)
            return

    def update_status(self, teammate):
        if teammate:
            self.update_follow_note(teammate)
        self.update_follow_btn(teammate)

    def destroy(self):
        self._nd = None
        return

    def set_follow_btn(self, teammate):
        if self._follow_set:
            if teammate and teammate.is_valid() and teammate.share_data.ref_parachute_stage in [STAGE_NONE, STAGE_PLANE, STAGE_ISLAND]:
                self._follow_set.setVisible(True)
                if self._follow_set.getOpacity() == 0:
                    self._nd.StopAnimation('shouqi')
                    self._nd.PlayAnimation('zhankai')

    def hide_follow_btn(self):
        if self._follow_set:
            if self._follow_set.getOpacity() == 255:
                self._nd.StopAnimation('zhankai')
                self._nd.PlayAnimation('shouqi')


class TeammateSignalBarUI(object):

    def __init__(self, nd_signal_bar, color):
        self.nd_signal_bar = nd_signal_bar
        self.cur_status = None
        self._color = color
        return

    percent_dict = {ubc.SIGNAL_BAR_NORMAL_PERCENT: 'gui/ui_res_2/battle/progress/prog_signal_team.png',
       ubc.SIGNAL_BAR_WARNING_PERCENT: 'gui/ui_res_2/battle/progress/prog_signal_team.png',
       ubc.SIGNAL_BAR_DANGER_PERCENT: 'gui/ui_res_2/battle/progress/prog_signal_team.png'
       }

    def get_bar_status(self, teammate):
        if teammate and teammate.is_valid():
            is_dying = teammate.ev_g_agony()
            is_die = teammate.ev_g_death()
        else:
            is_die = True
            is_dying = False
        is_in_mecha = False
        if is_die:
            percent = 0
        else:
            percent = teammate.ev_g_signal_percent() * 100
        if is_dying:
            bar_status = ubc.SIGNAL_BAR_DANGER_PERCENT
        else:
            bar_status = self.get_hp_bar_status(percent, is_in_mecha)
        pic = self.percent_dict.get(bar_status)
        return (
         pic, percent)

    def update_signal(self, teammate):
        if not self.nd_signal_bar:
            return
        pic, percent = self.get_bar_status(teammate)
        if self.cur_status != pic:
            self.switch_texture(pic)
            self.cur_status = pic
        self.setPercent(percent)

    def switch_texture(self, pic):
        self.nd_signal_bar.progress_signal.SetProgressTexture(pic)

    def setPercent(self, percent):
        self.nd_signal_bar.progress_signal.SetPercentage(percent)

    def get_hp_bar_status(self, percent, in_mecha):
        if in_mecha:
            return ubc.SIGNAL_BAR_MECHA
        else:
            if percent >= ubc.SIGNAL_BAR_WARNING_PERCENT:
                return ubc.SIGNAL_BAR_NORMAL_PERCENT
            return ubc.SIGNAL_BAR_DANGER_PERCENT

    def destroy(self):
        self.nd_signal_bar = None
        return

    def init_by_teammate_dict(self, info):
        self._info = dict(info)
        dead = self._info.get('dead', False)
        if dead:
            percent = 0
            is_in_mecha = False
            percent_status = self.get_hp_bar_status(percent, is_in_mecha)
            pic = self.percent_dict.get(percent_status)
            self.switch_texture(pic)