# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/redpoint_info.py
_reload_all = True
from common.utils.redpoint_check_func import *
all_elem_datas = {'1': {'cProjectName': 'friend/main_friend',
         'cCheckEvent': ('message_receive_friend_msg', 'message_receive_friend_msg_read'),
         'check_func': check_func_friend_msg
         },
   '2': {'cProjectName': 'friend/main_friend',
         'cCheckEvent': ('message_refresh_friend_apply', ),
         'check_func': check_func_add_friend
         },
   '3': {'cProjectName': 'friend/main_friend',
         'cCheckEvent': ('message_refresh_friends', 'message_refresh_contact_group'),
         'check_func': check_func_recruit
         },
   '4': {'cProjectName': 'friend/main_friend',
         'cCheckEvent': ('message_refresh_friend_apply', 'message_refresh_friends'),
         'check_func': check_func_apply_friend
         },
   '5': {'cProjectName': 'lobby/lobby_new',
         'cRedPointPath': 'btn_friends.red_point',
         'cChildIds': ('1', '2', '3', '4', '12')
         },
   '6': {'cProjectName': 'mail/mail_main',
         'cCheckEvent': ('message_read_email', 'message_refresh_email_list', 'message_get_reward', 'player_lv_update_event',
 'message_on_friend_gold_gift', 'message_recv_friend_gold_gift'),
         'check_func': check_func_sys_mail
         },
   '7': {'cProjectName': 'lobby/lobby_new',
         'cRedPointPath': 'btn_mail.red_point',
         'cChildIds': ('6', ),
         'check_hide_func': check_hide_func_lobby_red_dot
         },
   '8': {'cProjectName': 'mech_display/inscription/inscription_main',
         'cCheckEvent': ('mecha_component_update_event', 'mecha_component_slot_unlocked_event', 'mecha_component_change_active_page'),
         'check_func': has_mecha_can_install_tech
         },
   '9': {'cProjectName': 'mech_display/inscription/inscription_main',
         'cCheckEvent': ('mecha_component_store_rp_event', 'player_money_info_update_event'),
         'check_func': check_inscription_store_red_point
         },
   '11': {'cProjectName': 'mech_display/inscription/inscription_main',
          'cCheckEvent': ('update_proficiency_reward_event', 'update_mecha_module_plan_result_event', 'on_update_mecha_module_plans',
 'del_item_red_point', 'del_item_red_point_list', 'refresh_red_point'),
          'check_func': check_inscription_all_mecha_module_red_point
          },
   '12': {'cProjectName': 'friend/main_friend',
          'cCheckEvent': ('message_refresh_friends', 'message_refresh_contact_group', 'message_refresh_intimacy_msg',
 'message_on_intimacy_event'),
          'check_func': check_func_intimacy_tab
          },
   '13': {'cProjectName': 'friend/main_friend',
          'cCheckEvent': ('message_refresh_intimacy_msg', ),
          'check_func': check_func_intimacy_build
          },
   '14': {'cProjectName': 'friend/main_friend',
          'cCheckEvent': ('message_refresh_intimacy_msg', ),
          'check_func': check_func_intimacy_delete
          },
   '15': {'cProjectName': 'pve/pve_main',
          'cRedPointPath': 'btn_friends.red_point',
          'cChildIds': ('1', '2', '3', '4', '12')
          },
   '16': {'cProjectName': 'pve/pve_main',
          'cRedPointPath': 'btn_mail.red_point',
          'cChildIds': ('6', ),
          'check_hide_func': check_hide_func_lobby_red_dot
          },
   '17': {'cProjectName': 'pve/select_level_new/select_level_main',
          'cRedPointPath': 'btn_friends.red_point',
          'cChildIds': ('1', '2', '3', '4', '12')
          },
   '18': {'cProjectName': 'pve/select_level_new/select_level_main',
          'cRedPointPath': 'btn_mail.red_point',
          'cChildIds': ('6', ),
          'check_hide_func': check_hide_func_lobby_red_dot
          }
   }
project_redpoint_ids = {'mail/mail_main': ('6', ),
   'mech_display/inscription/inscription_main': ('8', '9', '11'),
   'pve/pve_main': ('15', '16'),
   'pve/select_level_new/select_level_main': ('17', '18'),
   'lobby/lobby_new': ('5', '7'),
   'friend/main_friend': ('1', '2', '3', '4', '12', '13', '14')
   }