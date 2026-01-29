# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/friend_utils.py
from __future__ import absolute_import
from logic.gutils.ui_salog_utils import add_lobby_uiclick_salog
FRIEND_LOG_KEY_ADD_BIND_FACEBOOK = 'frd_add_bind_facebook'
FRIEND_LOG_KEY_ADD_BIND_TWITTER = 'frd_add_bind_twitter'
FRIEND_LOG_KEY_ADD_BIND_LINEGAME = 'frd_add_bind_linegame'
FRIEND_LOG_KEY_ADD_VIA_FACEBOOK = 'frd_add_via_facebook'
FRIEND_LOG_KEY_ADD_VIA_TWITTER = 'frd_add_via_twitter'
FRIEND_LOG_KEY_ADD_VIA_LINEGAME = 'frd_add_via_linegame'
FRIEND_LOG_KEY_SHARE_VIA_FACEBOOK = 'frd_share_via_facebook'
FRIEND_LOG_KEY_SHARE_VIA_TWITTER = 'frd_share_via_twitter'
FRIEND_LOG_KEY_SHARE_VIA_LINEGAME = 'frd_share_via_linegame'
FRIEND_LOG_KEY_TEAM_INVITE_BIND_FACEBOOK = 'frd_team_bind_facebook'
FRIEND_LOG_KEY_TEAM_INVITE_BIND_TWITTER = 'frd_team_bind_twitter'
FRIEND_LOG_KEY_TEAM_INVITE_BIND_LINEGAME = 'frd_team_bind_linegame'
FRIEND_LOG_KEY_TEAM_INVITE_VIA_FACEBOOK = 'frd_team_invite_via_facebook'
FRIEND_LOG_KEY_TEAM_INVITE_VIA_TWITTER = 'frd_team_invite_via_twitter'
FRIEND_LOG_KEY_TEAM_INVITE_VIA_LINEGAME = 'frd_team_invite_via_linegame'
FRIEND_LOG_KEY_TEAM_SHARE_VIA_FACEBOOK = 'frd_team_share_via_facebook'
FRIEND_LOG_KEY_TEAM_SHARE_VIA_TWITTER = 'frd_team_share_via_twitter'
FRIEND_LOG_KEY_TEAM_SHARE_VIA_MESSENGER = 'frd_team_share_via_messenger'
FRIEND_LOG_KEY_TEAM_SHARE_VIA_LINEGAME = 'frd_team_share_via_linegame'
FRIEND_LOG_KEY_SHARE_VIA_RECRUIT = 'frd_share_via_recruit'

def salog_friend_ui_oper--- This code section failed: ---

  34       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  POP_JUMP_IF_TRUE     13  'to 13'

  35       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

  36      13  LOAD_FAST             0  'friend_log_key'
          16  POP_JUMP_IF_TRUE     33  'to 33'

  37      19  LOAD_GLOBAL           2  'log_error'
          22  LOAD_CONST            1  'friend_utils salog_friend_ui_oper no friend_log_key specified.'
          25  CALL_FUNCTION_1       1 
          28  POP_TOP          

  38      29  LOAD_CONST            0  ''
          32  RETURN_END_IF    
        33_0  COME_FROM                '16'

  39      33  LOAD_FAST             1  'with_store_data'
          36  POP_JUMP_IF_FALSE   121  'to 121'

  40      39  LOAD_GLOBAL           0  'global_data'
          42  LOAD_ATTR             3  'achi_mgr'
          45  LOAD_ATTR             4  'get_user_archive_data'
          48  LOAD_GLOBAL           0  'global_data'
          51  LOAD_ATTR             1  'player'
          54  LOAD_ATTR             5  'uid'
          57  CALL_FUNCTION_1       1 
          60  STORE_FAST            2  'user_arch'

  41      63  LOAD_FAST             2  'user_arch'
          66  LOAD_ATTR             6  'get_field'
          69  LOAD_ATTR             2  'log_error'
          72  CALL_FUNCTION_2       2 
          75  LOAD_CONST            3  1
          78  BINARY_ADD       
          79  STORE_FAST            3  'record_num'

  42      82  LOAD_GLOBAL           7  'add_lobby_uiclick_salog'
          85  LOAD_GLOBAL           4  'get_user_archive_data'
          88  LOAD_GLOBAL           8  'str'
          91  LOAD_FAST             3  'record_num'
          94  CALL_FUNCTION_1       1 
          97  BINARY_ADD       
          98  CALL_FUNCTION_2       2 
         101  POP_TOP          

  43     102  LOAD_FAST             2  'user_arch'
         105  LOAD_ATTR             9  'set_field'
         108  LOAD_FAST             0  'friend_log_key'
         111  LOAD_FAST             3  'record_num'
         114  CALL_FUNCTION_2       2 
         117  POP_TOP          
         118  JUMP_FORWARD         10  'to 131'

  45     121  LOAD_GLOBAL           7  'add_lobby_uiclick_salog'
         124  LOAD_FAST             0  'friend_log_key'
         127  CALL_FUNCTION_1       1 
         130  POP_TOP          
       131_0  COME_FROM                '118'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 72


def del_friend_with_intimacy_confirm(frd_uid):
    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlgWithCalm
    from logic.gcommon.const import FRD_KEY_FRDS
    from logic.gcommon.cdata.intimacy_data import get_intimacy_pt
    intimacy_data = global_data.player.intimacy_data.get(str(frd_uid), None)
    pt = get_intimacy_pt(intimacy_data) if intimacy_data else 0
    if pt >= 100:

        def confirm_callback():
            global_data.player.req_del_from_list(FRD_KEY_FRDS, frd_uid)

        confirm_text = get_text_by_id(633709).format(3)
        SecondConfirmDlgWithCalm().confirm(content=get_text_by_id(633710), confirm_callback=confirm_callback, confirm_text=confirm_text)
    else:
        global_data.player.req_del_from_list(FRD_KEY_FRDS, frd_uid)
    return


def black_friend_with_intimacy_confirm(frd_uid):
    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlgWithCalm
    from logic.gcommon.const import FRD_KEY_BALCLIST
    from logic.gcommon.cdata.intimacy_data import get_intimacy_pt
    intimacy_data = global_data.player.intimacy_data.get(str(frd_uid), None)
    pt = get_intimacy_pt(intimacy_data) if intimacy_data else 0
    if pt >= 100:

        def confirm_callback():
            global_data.player.req_add_to_list(FRD_KEY_BALCLIST, frd_uid)

        confirm_text = get_text_by_id(633709).format(3)
        SecondConfirmDlgWithCalm().confirm(content=get_text_by_id(633710), confirm_callback=confirm_callback, confirm_text=confirm_text)
    else:
        global_data.player.req_add_to_list(FRD_KEY_BALCLIST, frd_uid)
    return