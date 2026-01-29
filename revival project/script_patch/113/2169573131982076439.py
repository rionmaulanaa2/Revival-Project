# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/end_statics_utils.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.gcommon.ctypes.BattleReward import calc_battle_score
from logic.gcommon.common_const.battle_achieve_const import data
from logic.gcommon.common_const import statistics_const as sconst
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.role_head_utils import init_role_head_by_id
from logic.comsys.message import PlayerSimpleInf
import cc
MemNumStyle = {1: {'path': 'gui/ui_res_2/icon/icon_solo.png','text': 19401},2: {'path': 'gui/ui_res_2/common/icon/icon_dou.png','text': 19402},3: {'path': 'gui/ui_res_2/common/icon/icon_squa.png','text': 19403}}
MemNumStyleNew = {1: {'path': 'gui/ui_res_2/role/icon_mode_solo_2.png','text': 19401},2: {'path': 'gui/ui_res_2/role/icon_mode_duo_2.png','text': 19402},4: {'path': 'gui/ui_res_2/role/icon_mode_squad_2.png','text': 19403}}

def init_end_person_statistics(panel, teammate_num, total_fighter_num, settle_dict):
    statistics = settle_dict.get('statistics', {})
    if teammate_num <= 2:
        info = MemNumStyle.get(teammate_num)
    else:
        info = MemNumStyle.get(3)
    panel.lab_mode.SetString(get_text_local_content(info['text']))
    rank = settle_dict.get('rank', 100)
    panel.lab_rank.SetString(str(rank))
    if str(rank) == '1':
        panel.rank_1.setVisible(True)
        panel.rank_others.setVisible(False)
    else:
        panel.rank_1.setVisible(False)
        panel.rank_others.setVisible(True)
    txt = get_text_local_content(19406) if teammate_num > 1 else get_text_local_content(19405)
    txt = txt.format(num=total_fighter_num)
    panel.nd_kill.lab_damage.setString(str(statistics.get(sconst.KILL_HUMAN, 0)))
    panel.nd_mech.lab_mech.setString(str(statistics.get(sconst.KILL_MECHA, 0)))
    damage = statistics.get(sconst.HUMAN_DAMAGE, 0) + statistics.get(sconst.MECHA_DAMAGE, 0)
    damage = int(damage)
    panel.nd_damage.lab_damage.setString(str(damage))


def init_end_teammate_statics--- This code section failed: ---

  65       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'keys'
           6  LOAD_FAST             1  'groupmate_info'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            3  'teammates'

  66      15  BUILD_LIST_0          0 
          18  LOAD_FAST             3  'teammates'
          21  GET_ITER         
          22  FOR_ITER             30  'to 55'
          25  STORE_FAST            4  'v'
          28  LOAD_FAST             4  'v'
          31  LOAD_GLOBAL           2  'global_data'
          34  LOAD_ATTR             3  'player'
          37  LOAD_ATTR             4  'id'
          40  COMPARE_OP            3  '!='
          43  POP_JUMP_IF_FALSE    22  'to 22'
          46  LOAD_FAST             4  'v'
          49  LIST_APPEND           2  ''
          52  JUMP_BACK            22  'to 22'
          55  STORE_FAST            3  'teammates'

  67      58  LOAD_GLOBAL           5  'len'
          61  LOAD_FAST             3  'teammates'
          64  CALL_FUNCTION_1       1 
          67  LOAD_CONST            1  1
          70  COMPARE_OP            0  '<'
          73  POP_JUMP_IF_FALSE    92  'to 92'

  68      76  LOAD_FAST             0  'panel'
          79  LOAD_ATTR             6  'setVisible'
          82  LOAD_GLOBAL           7  'False'
          85  CALL_FUNCTION_1       1 
          88  POP_TOP          
          89  JUMP_FORWARD        257  'to 349'

  71      92  LOAD_FAST             0  'panel'
          95  LOAD_ATTR             6  'setVisible'
          98  LOAD_GLOBAL           8  'True'
         101  CALL_FUNCTION_1       1 
         104  POP_TOP          

  73     105  SETUP_LOOP          241  'to 349'
         108  LOAD_GLOBAL           9  'range'
         111  LOAD_CONST            2  4
         114  CALL_FUNCTION_1       1 
         117  GET_ITER         
         118  FOR_ITER            227  'to 348'
         121  STORE_FAST            5  'i'

  74     124  LOAD_GLOBAL          10  'getattr'
         127  LOAD_GLOBAL           3  'player'
         130  LOAD_FAST             5  'i'
         133  LOAD_CONST            1  1
         136  BINARY_ADD       
         137  BINARY_MODULO    
         138  CALL_FUNCTION_2       2 
         141  STORE_FAST            6  'node'

  76     144  LOAD_FAST             5  'i'
         147  LOAD_GLOBAL           5  'len'
         150  LOAD_FAST             3  'teammates'
         153  CALL_FUNCTION_1       1 
         156  COMPARE_OP            5  '>='
         159  POP_JUMP_IF_FALSE   181  'to 181'

  77     162  LOAD_FAST             6  'node'
         165  LOAD_ATTR             6  'setVisible'
         168  LOAD_GLOBAL           7  'False'
         171  CALL_FUNCTION_1       1 
         174  POP_TOP          

  78     175  CONTINUE            118  'to 118'
         178  JUMP_FORWARD          0  'to 181'
       181_0  COME_FROM                '178'

  79     181  LOAD_FAST             3  'teammates'
         184  LOAD_FAST             5  'i'
         187  BINARY_SUBSCR    
         188  STORE_FAST            7  'mateid'

  80     191  LOAD_FAST             7  'mateid'
         194  LOAD_FAST             1  'groupmate_info'
         197  COMPARE_OP            7  'not-in'
         200  POP_JUMP_IF_FALSE   209  'to 209'

  81     203  CONTINUE            118  'to 118'
         206  JUMP_FORWARD          0  'to 209'
       209_0  COME_FROM                '206'

  82     209  LOAD_FAST             6  'node'
         212  LOAD_ATTR             6  'setVisible'
         215  LOAD_GLOBAL           8  'True'
         218  CALL_FUNCTION_1       1 
         221  POP_TOP          

  83     222  LOAD_FAST             6  'node'
         225  LOAD_ATTR            11  'lab_name'
         228  LOAD_ATTR            12  'setString'
         231  LOAD_FAST             1  'groupmate_info'
         234  LOAD_ATTR            13  'get'
         237  LOAD_FAST             7  'mateid'
         240  CALL_FUNCTION_1       1 
         243  LOAD_ATTR            13  'get'
         246  LOAD_CONST            4  'char_name'
         249  CALL_FUNCTION_1       1 
         252  CALL_FUNCTION_1       1 
         255  POP_TOP          

  84     256  LOAD_FAST             2  'team_settle_info'
         259  LOAD_ATTR            13  'get'
         262  LOAD_FAST             3  'teammates'
         265  LOAD_FAST             5  'i'
         268  BINARY_SUBSCR    
         269  BUILD_MAP_0           0 
         272  CALL_FUNCTION_2       2 
         275  LOAD_ATTR            13  'get'
         278  LOAD_CONST            5  'statistics'
         281  BUILD_MAP_0           0 
         284  CALL_FUNCTION_2       2 
         287  STORE_FAST            8  'statistics'

  85     290  LOAD_FAST             8  'statistics'
         293  LOAD_ATTR            13  'get'
         296  LOAD_GLOBAL          14  'sconst'
         299  LOAD_ATTR            15  'HUMAN_DAMAGE'
         302  LOAD_CONST            6  ''
         305  CALL_FUNCTION_2       2 
         308  STORE_FAST            9  'damage'

  86     311  LOAD_GLOBAL          16  'int'
         314  LOAD_FAST             9  'damage'
         317  CALL_FUNCTION_1       1 
         320  STORE_FAST            9  'damage'

  87     323  LOAD_FAST             6  'node'
         326  LOAD_ATTR            17  'lab_stat_num'
         329  LOAD_ATTR            12  'setString'
         332  LOAD_GLOBAL          18  'str'
         335  LOAD_FAST             9  'damage'
         338  CALL_FUNCTION_1       1 
         341  CALL_FUNCTION_1       1 
         344  POP_TOP          
         345  JUMP_BACK           118  'to 118'
         348  POP_BLOCK        
       349_0  COME_FROM                '105'
       349_1  COME_FROM                '89'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 138


def init_end_person_statistics_new(panel, teammate_num, settle_dict, achievement, total_fighter_num, player_info):
    role_id = player_info.get('role_id')
    clothing_id = player_info.get('clothing_id')
    mecha_id = player_info.get('mecha_id')
    player_char_name = player_info.get('char_name', '')
    head_frame = player_info.get('head_frame')
    self_eid = player_info.get('eid')
    role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
    img_path = role_skin_config.get(str(clothing_id), {}).get('img_role')
    panel.img_role.SetDisplayFrameByPath('', img_path)
    max_team_size = settle_dict.get('max_team_size', -1)
    max_team_size = max_team_size if max_team_size <= 2 else 4
    game_mode_info = MemNumStyleNew.get(max_team_size, {})
    if game_mode_info:
        panel.nd_mode.lab_mode.SetString(game_mode_info['text'])
        panel.nd_mode.img_mode.SetDisplayFrameByPath('', game_mode_info['path'])
    else:
        panel.nd_mode.lab_mode.setVisible(False)
        panel.nd_mode.img_mode.setVisible(False)
    rank = settle_dict.get('rank', 99)
    panel.nd_stat_core.nd_rank.lab_rank.SetString(str(rank))
    panel.nd_stat_core.nd_rank.lab_people_num.SetString('/' + str(total_fighter_num))
    statistics = settle_dict.get('statistics', {})
    panel.nd_stat_core.nd_kill.lab_kill.SetString(str(statistics.get(sconst.KILL_HUMAN, 0)))
    panel.nd_stat_core.nd_kill_mech.lab_kill_mech.SetString(str(statistics.get(sconst.KILL_MECHA, 0)))
    achievement_count = len(achievement.get(self_eid, []))
    if achievement_count > 0:
        achievement_id = achievement[self_eid][0]
        panel.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
    panel.lab_player_name.SetString(player_char_name)
    details = panel.nd_stat_details.list_stat_details
    s_detail = details.GetItem(0)
    init_role_head_by_id(s_detail.temp_role, head_frame, role_id)
    s_detail.lab_name.SetString(player_char_name)
    s_detail.lab_kill.SetString(str(statistics.get(sconst.KILL_HUMAN, 0)))
    s_detail.lab_mech.SetString(str(statistics.get(sconst.KILL_MECHA, 0)))
    damage = statistics.get(sconst.HUMAN_DAMAGE, 0) + statistics.get(sconst.MECHA_DAMAGE, 0) + statistics.get(sconst.MECHA_TRANS_DAMAGE, 0)
    damage = int(damage)
    s_detail.lab_damage.SetString(str(damage))
    survival_min = str(int(statistics.get(sconst.SURVIVAL_TIME, 0)) // 60)
    s_detail.lab_time.SetString(survival_min + 'min')
    if achievement_count >= 1:
        s_detail.temp_achievement.setVisible(True)
        achievement_id = achievement[self_eid][0]
        s_detail.temp_achievement.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
        s_detail.temp_achievement.lab_achievement_shadow.setVisible(False)
        s_detail.btn_more.setVisible(True)
        s_detail.btn_more.lab_num.SetString(str(achievement_count))
        ach_list = s_detail.nd_achievement_list.list_achievement
        for i in range(10):
            ach = ach_list.GetItem(i)
            if i >= achievement_count:
                ach.setVisible(False)
                continue
            else:
                ach.setVisible(True)
            achievement_id = achievement[self_eid][i]
            ach.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
            ach.lab_achievement_shadow.setVisible(False)

        @s_detail.btn_more.unique_callback()
        def OnClick(btn, touch):
            s_detail.nd_achievement_list.setVisible(not s_detail.nd_achievement_list.isVisible())

    else:
        s_detail.temp_achievement.setVisible(False)
        s_detail.btn_more.setVisible(False)

        @s_detail.btn_more.unique_callback()
        def OnClick(btn, touch):
            s_detail.nd_achievement_list.setVisible(not s_detail.nd_achievement_list.isVisible())


def _register_move_achievement_btn_click(detail):

    @detail.btn_more.unique_callback()
    def OnClick(btn, touch):
        detail.nd_achievement_list.setVisible(not detail.nd_achievement_list.isVisible())


def init_end_teammate_statistics_new(panel, groupmate_info, team_settle_info, achievement):
    teammates = six_ex.keys(groupmate_info)
    details = panel.nd_stat_details.list_stat_details
    details.SetInitCount(len(teammates) + 1)
    for i in range(len(teammates)):
        eid = teammates[i]
        detail = details.GetItem(i + 1)
        head_frame = groupmate_info.get(eid, {}).get('head_frame')
        role_id = groupmate_info.get(eid, {}).get('role_id')
        init_role_head_by_id(detail.temp_role, head_frame, role_id)

        @detail.temp_role.unique_callback()
        def OnClick(btn, touch, player_uid=eid):
            on_click_player_head(touch, player_uid)

        detail.lab_name.SetString(groupmate_info.get(eid, {}).get('char_name', ''))
        statistics = team_settle_info.get(eid, {}).get('statistics', {})
        detail.lab_kill.SetString(str(statistics.get(sconst.KILL_HUMAN, 0)))
        detail.lab_mech.SetString(str(statistics.get(sconst.KILL_MECHA, 0)))
        damage = statistics.get(sconst.HUMAN_DAMAGE, 0) + statistics.get(sconst.MECHA_DAMAGE, 0) + statistics.get(sconst.MECHA_TRANS_DAMAGE, 0)
        damage = int(damage)
        detail.lab_damage.SetString(str(damage))
        survival_min = str(int(statistics.get(sconst.SURVIVAL_TIME, 0)) // 60)
        detail.lab_time.SetString(survival_min + 'min')
        achievement_count = len(achievement.get(eid, []))
        if achievement_count >= 1:
            detail.temp_achievement.setVisible(True)
            achievement_id = achievement[eid][0]
            detail.temp_achievement.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
            detail.temp_achievement.lab_achievement_shadow.setVisible(False)
            if achievement_count > 1:
                detail.btn_more.setVisible(True)
                detail.btn_more.lab_num.SetString(str(achievement_count))
            else:
                detail.btn_more.setVisible(False)
            ach_list = detail.nd_achievement_list.list_achievement
            for j in range(10):
                ach = ach_list.GetItem(j)
                if j >= achievement_count:
                    ach.setVisible(False)
                    continue
                else:
                    ach.setVisible(True)
                achievement_id = achievement[eid][j]
                ach.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
                ach.lab_achievement_shadow.setVisible(False)

            _register_move_achievement_btn_click(detail)
        else:
            detail.temp_achievement.setVisible(False)
            detail.btn_more.setVisible(False)


def on_click_player_head(touch, player_uid):
    if not player_uid:
        return
    if not global_data.player:
        return
    if int(player_uid) == global_data.player.uid:
        return
    ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
    if not ui:
        return
    ui.need_close_history_ui = True
    ui.refresh_by_uid(int(player_uid))
    ui.set_position(touch.getLocation(), anchor_point=cc.Vec2(0.5, 0.5))


def init_koth_end_person_statistics_new(panel, teammate_num, group_num, settle_dict, achievement):
    role_id = global_data.player.logic.get_value('G_ROLE_ID')
    panel.img_role.SetDisplayFrameByPath('', 'gui/ui_res_2/pic/role_{}.png'.format(role_id))
    mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
    teammate_num = teammate_num if teammate_num <= 2 else 4
    game_mode_info = MemNumStyleNew.get(teammate_num, {})
    if game_mode_info:
        panel.nd_mode.lab_mode.SetString(game_mode_info['text'])
        panel.nd_mode.img_mode.SetDisplayFrameByPath('', game_mode_info['path'])
    else:
        panel.nd_mode.lab_mode.setVisible(False)
        panel.nd_mode.img_mode.setVisible(False)
    rank = settle_dict.get('rank', 99)
    rank_icon = ['gui/ui_res_2/fight_end/text_rank_1.png',
     'gui/ui_res_2/fight_end/text_rank_2.png',
     'gui/ui_res_2/fight_end/text_rank_3.png']
    panel.nd_stat_koth.nd_rank.lab_rank.SetDisplayFrameByPath('', rank_icon[rank - 1])
    statistics = settle_dict.get('statistics', {})
    self_eid = global_data.player.id
    achievement_count = len(achievement[self_eid])
    details = panel.nd_stat_details.list_stat_details
    s_detail = details.GetItem(0)
    s_detail = s_detail.nd_item
    from common.cfg import confmgr
    icon = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'icon') or ''
    s_detail.temp_role.frame_head.img_head.SetDisplayFrameByPath('', icon)
    s_detail.lab_name.SetString(global_data.player.logic.get_value('G_CHAR_NAME'))
    s_detail.lab_kill.SetString(str(statistics.get(sconst.KILL_HUMAN, 0)))
    s_detail.lab_mech.SetString(str(statistics.get(sconst.KILL_MECHA, 0)))
    s_detail.lab_damage.SetString(str(statistics.get(sconst.DEAD_HUMAN, 0)))
    s_detail.lab_time.SetString(str(statistics.get(sconst.ACHIEVE_SCORE, 0)))
    s_detail.img_self.setVisible(True)
    if achievement_count >= 1:
        s_detail.temp_achievement.setVisible(True)
        achievement_id = achievement[self_eid][0]
        s_detail.temp_achievement.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
        s_detail.btn_more.setVisible(True)
        s_detail.btn_more.lab_num.SetString(str(achievement_count))
        ach_list = s_detail.nd_achievement_list.list_achievement
        for i in range(10):
            ach = ach_list.GetItem(i)
            if i >= achievement_count:
                ach.setVisible(False)
                continue
            else:
                ach.setVisible(True)
            achievement_id = achievement[self_eid][i]
            ach.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))

        @s_detail.btn_more.unique_callback()
        def OnClick(btn, touch):
            s_detail.nd_achievement_list.setVisible(not s_detail.nd_achievement_list.isVisible())

    else:
        s_detail.temp_achievement.setVisible(False)
        s_detail.btn_more.setVisible(False)

        @s_detail.btn_more.unique_callback()
        def OnClick(btn, touch):
            s_detail.nd_achievement_list.setVisible(not s_detail.nd_achievement_list.isVisible())


def init_koth_end_teammate_statistics_new(panel, groupmate_info, team_settle_info, achievement):
    teammates = six_ex.keys(groupmate_info)
    details = panel.nd_stat_details.list_stat_details
    details.SetInitCount(len(teammates) + 1)
    from common.cfg import confmgr
    for i in range(len(teammates)):
        eid = teammates[i]
        detail = details.GetItem(i + 1)
        detail = detail.nd_item
        icon = confmgr.get('role_info', 'RoleInfo', 'Content', str(groupmate_info.get(eid).get('role_id', u'11')), 'icon') or ''
        detail.temp_role.frame_head.img_head.SetDisplayFrameByPath('', icon)
        detail.lab_name.SetString(groupmate_info.get(eid).get('char_name'))
        statistics = team_settle_info.get(eid).get('statistics', {})
        detail.lab_kill.SetString(str(statistics.get(sconst.KILL_HUMAN, 0)))
        detail.lab_mech.SetString(str(statistics.get(sconst.KILL_MECHA, 0)))
        detail.lab_damage.SetString(str(statistics.get(sconst.DEAD_HUMAN, 0)))
        detail.lab_time.SetString(str(statistics.get(sconst.ACHIEVE_SCORE, 0)))
        achievement_count = len(achievement.get(eid, []))
        if achievement_count >= 1:
            detail.temp_achievement.setVisible(True)
            achievement_id = achievement[eid][0]
            detail.temp_achievement.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))
            if achievement_count > 1:
                detail.btn_more.setVisible(True)
                detail.btn_more.lab_num.SetString(str(achievement_count))
            else:
                detail.btn_more.setVisible(False)
            ach_list = detail.nd_achievement_list.list_achievement
            for j in range(10):
                ach = ach_list.GetItem(j)
                if j >= achievement_count:
                    ach.setVisible(False)
                    continue
                else:
                    ach.setVisible(True)
                achievement_id = achievement[eid][j]
                ach.lab_achievement.SetString(get_text_by_id(get_battle_achieve_text_id(achievement_id)))

            @detail.btn_more.unique_callback()
            def OnClick(btn, touch):
                detail.nd_achievement_list.setVisible(not detail.nd_achievement_list.isVisible())

        else:
            detail.temp_achievement.setVisible(False)
            detail.btn_more.setVisible(False)


def init_koth_end_campmate_statistics_new(panel, settle_dict):
    camp_data = settle_dict.get('faction_view', {})
    camp_data_lst = camp_data.get('core_data', [])
    mvp_entity_id = camp_data.get('mvp_of_faction')
    details = panel.list_stat
    details.SetInitCount(len(camp_data_lst))
    entity_id_to_list_index = {}
    from common.cfg import confmgr
    for i, camp_data in enumerate(camp_data_lst):
        entity_id, name, entity_status, kill, mech, die, score, like, role_id = camp_data
        detail = details.GetItem(i)
        entity_id_to_list_index[entity_id] = i
        detail.img_mvp.setVisible(mvp_entity_id == entity_id)
        detail.lab_rank.SetString(str(i + 1))
        icon = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'icon') or ''
        detail.temp_role.frame_head.img_head.SetDisplayFrameByPath('', icon)
        detail.lab_name.SetString(name)
        detail.lab_kill.SetString(str(kill))
        detail.lab_mech.SetString(str(mech))
        detail.lab_die.SetString(str(die))
        detail.lab_score.SetString(str(score))
        detail.lab_like.SetString(str(like))
        is_self = global_data.player and entity_id == global_data.player.id
        is_group_mate = global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_groupmate(entity_id)
        detail.btn_like.setVisible(not is_self)
        detail.img_self.setVisible(is_self)
        detail.img_teammate.setVisible(is_group_mate and not is_self)

        @detail.btn_like.unique_callback()
        def OnClick(btn, touch, entity_id=entity_id):
            global_data.battle and global_data.battle.give_praise_for_player(entity_id)

    return entity_id_to_list_index


def init_end_details_statistics(panel):
    pass


def get_battle_achieve_text_id(achieve_id):
    conf = confmgr.get('battle_achieve_data', str(achieve_id), default={})
    return conf.get('desc_text_id', 0)


def get_battle_achieve_type(achieve_id):
    conf = confmgr.get('battle_achieve_data', str(achieve_id), default={})
    return conf.get('type', None)


def get_battle_achieve_template_path(achieve_id):
    conf = confmgr.get('battle_achieve_data', str(achieve_id), default={})
    return conf.get('template_path', None)


def get_battle_achieve_extra_params(achieve_id):
    conf = confmgr.get('battle_achieve_data', str(achieve_id), default={})
    return conf.get('extra_params', {})