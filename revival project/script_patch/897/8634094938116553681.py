# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Avatar.py
from __future__ import absolute_import
from __future__ import print_function
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict
from mobile.common.EntityManager import Dynamic
from logic.gcommon.utility import manual_meta_class
from logic.entities.BaseClientAvatar import BaseClientAvatar
from logic.gutils.ConnectHelper import ConnectHelper
from logic.comsys.feedback import echoes
import six
MEMBER_PACKAGE = 'logic.entities.avatarmembers'
MEMBER_NAME_LST = ('impBase', 'impLevel', 'impTime', 'impSoul', 'impBattle', 'impLobby',
                   'impUserSetting', 'impTeam', 'impFriend', 'impStat', 'impPlayer',
                   'impChat', 'impConfirm', 'impPay', 'impShop', 'impProficiency',
                   'impItem', 'impClothing', 'impMail', 'impCCMini', 'impRank', 'impCustomRoom',
                   'impAttendance', 'impRole', 'impBindMobile', 'impActivity', 'impAdvance',
                   'impGameSprite', 'impVisit', 'impAchievement', 'impNgPush', 'impLive',
                   'impShare', 'impBattleReplay', 'impBindReminder', 'impLocalBattleServer',
                   'impSurvey', 'impRoleHead', 'impMecha', 'impBattleSeason', 'impNewbiePass',
                   'impMechaModule', 'impHouseSys', 'impBattleItem', 'impTask', 'impDayTask',
                   'impAssessTask', 'impWeekTask', 'impYueka', 'impReport', 'impNotice',
                   'impVitality', 'impCommentGuide', 'impWeeklyCard', 'impBattlePass',
                   'impSeasonTask', 'impDan', 'impSpectate', 'impFollow', 'impClan',
                   'impClanPoint', 'impClanRank', 'impAFK', 'impReward', 'impTwitterReward',
                   'impEnlist', 'impFriendHelp', 'impInteraction', 'impCharm', 'impCredit',
                   'impReturn', 'impPlace', 'impTown', 'impBond', 'impAnticheat',
                   'impCorpTask', 'impThirdPartyApp', 'impCDKey', 'impTriggerGift',
                   'impTitle', 'impBattleFlag', 'impCareer', 'impNewSysPrompt', 'impGuide',
                   'impInscription', 'impSysUnlock', 'impRealName', 'impAntiAddiction',
                   'impLocalBattle', 'impFileService', 'impBindWechat', 'impFestival',
                   'impSecretOrder', 'impRandomTask', 'impGoldGift', 'impCheckUpdate',
                   'impVeteran', 'impChanceGift', 'impMeow', 'impIntimacy', 'impSummer',
                   'impQuestion', 'impSpecEnlist', 'impPrivilege', 'impWebapp', 'impVerifyCode',
                   'impBrandLevel', 'impUdataGift', 'impOnlineState', 'impCompetition',
                   'impWebToken', 'impHomeland', 'impSettings', 'impIMT', 'impConcert',
                   'impGlobalLottery', 'impVote', 'impNile', 'impRedPacket', 'impMigrateAccount',
                   'impDuelStat', 'impLuckScore', 'impNewbieEnlist', 'impPickableItem',
                   'impBet', 'impProjectionKill', 'impYuanbaoStrike', 'impLoginRecord',
                   'impGlideEffect', 'impPet', 'impPveTalent', 'impPve', 'impPVEMechaDevelopment',
                   'impPVEStory', 'impPveClearTime', 'impPveClearTimeTeam', 'impMultiRank',
                   'impSlotMachine', 'impMechaSkinShare', 'impGuangmu')
DUA_TIME = 0.02

def post_meta_class_generator():
    import inspect
    import types
    import time
    cls = Avatar
    member_list = []
    b_time = time.time()
    for m_name in MEMBER_NAME_LST:
        mod = __import__(MEMBER_PACKAGE, globals(), locals(), [m_name])
        mod = getattr(mod, m_name, None)
        member = getattr(mod, m_name, None)
        if member:
            member_list.append(member)
        else:
            raise Exception('[Class %s] member cannot find: %s' % (cls.__name__, m_name))
        if time.time() - b_time > DUA_TIME:
            yield False
            b_time = time.time()

    check_type = (
     int, int, bytes, list,
     dict, tuple, float, set, frozenset)
    for inherit in member_list:
        if six.PY2:
            methods = inspect.getmembers(inherit, inspect.ismethod)
        else:
            methods = inspect.getmembers(inherit, inspect.isfunction)
        for fun_name, fun in methods:
            if hasattr(cls, fun_name):
                raise Exception('[Class %s] function %s has define' % (cls.__name__, fun_name))
            if six.PY2:
                setattr(cls, fun_name, fun.__func__)
            else:
                setattr(cls, fun_name, fun)

        for member_name, mem_object in inspect.getmembers(inherit):
            if member_name in ('__module__', '__doc__', '__name__'):
                continue
            if isinstance(mem_object, check_type):
                if hasattr(cls, member_name):
                    raise Exception('[Class %s] member %s has define' % (cls.__name__, member_name))
                setattr(cls, member_name, mem_object)

        if time.time() - b_time > DUA_TIME:
            yield False
            b_time = time.time()

    yield True
    return


@Dynamic
class Avatar(six.with_metaclass(manual_meta_class(MEMBER_NAME_LST), BaseClientAvatar)):

    def __init__(self, entityid=None):
        if global_data.use_sunshine:
            from sunshine.Editor.Meta.AvatarMeta import InitAvatarMetaLink
            InitAvatarMetaLink(self)
        super(Avatar, self).__init__(entityid)

    def init_from_dict(self, bdict):
        if bdict.get('accountname', None):
            ConnectHelper().set_reconnect_info(bdict['accountname'], bdict['reconnect_token'], bdict.get('reconnect_game', None))
        self.uid = bdict['uid']
        global_data.abtest_group = bdict.get('abtest_group', False)
        self.hosttag = bdict.get('hosttag', '')
        self._call_meta_member_func('_init_@_from_dict', bdict)
        global_data.baisc_mgr_agent.set_window_title(bdict)
        global_data.emgr.app_resume_event += (self.on_resume,)
        global_data.emgr.app_background_event += (self.on_background,)
        global_data.server_enable_low_fps = bdict.get('enable_low_fps', True)
        global_data.ccmini_mgr.set_entityid_map(self.uid, self.id)
        switch_data = bdict.get('swtich_data', {})
        if switch_data.get('peppa_pig', False):
            import six.moves.builtins
            six.moves.builtins.__dict__['G_CLIENT_ABTEST'] = 1
            global_data.enable_split_script = True
            global_data.enable_ray_test_eye_adapt = True
        global_data.need_replay = switch_data.get('need_replay', False)
        global_data.server_enable_vlm = switch_data.get('enable_vlm', True)
        global_data.enable_collect_ui = switch_data.get('enable_collect_ui', False)
        global_data.enable_clan_quit_advise = switch_data.get('enable_clan_quit_advise', True)
        global_data.enable_battle_oodle = switch_data.get('enable_battle_oodle', False)
        global_data.enable_pve = switch_data.get('enable_pve', False)
        global_data.enable_pve_team = switch_data.get('enable_pve_team', False)
        global_data.pve_max_chapter = switch_data.get('pve_max_chapter', 1)
        global_data.enable_pve_breakable = switch_data.get('enable_pve_breakable', 0)
        if global_data.enable_battle_oodle:
            self.try_init_oodle_dict()
        if switch_data.get('profile_rat', 0):
            import json
            self._switch_profile_on('', json.dumps({'lag_threadhold': 100,
               'profile_duration': 1200,
               'profile_start_time': 10
               }))
        global_data.enable_check_lottery = switch_data.get('enable_check_lottery', False)
        from common.platform.dctool.interface import is_mainland_package
        if not is_mainland_package():
            global_data.enable_check_lottery = False
        global_data.micro_service_url = bdict.get('micro_service_url', '')
        return

    def try_init_oodle_dict(self):
        if global_data.feature_mgr.is_support_oodle_v2():
            import threading
            import os
            import game3d
            import asiocore

            def init_oodle_dict():
                import C_file
                import zlib
                oodnet_dict_path = 'confs/oodle_dict'
                path_list = []
                for srv_type in ['battle']:
                    for route_type in ['server_to_client', 'client_to_server']:
                        compressed_file = os.path.join(oodnet_dict_path, srv_type, route_type + '.zlib')
                        print('enable_oodle: find_compressed_file ', compressed_file, C_file.find_res_file(compressed_file, ''))
                        if C_file.find_res_file(compressed_file, ''):
                            data = C_file.get_res_file(compressed_file, '')
                            decompressed_data = zlib.decompressobj(15).decompress(data)
                            dict_path = os.path.join(game3d.get_doc_dir(), 'oodle_dict', srv_type)
                            if not os.path.exists(dict_path):
                                os.makedirs(dict_path)
                            mdic_path = os.path.join(dict_path, route_type + '.mdic')
                            path_list.append(mdic_path)
                            with open(mdic_path, 'wb') as fin:
                                fin.write(decompressed_data)

                asiocore.init_oodle_dict(tuple(path_list))
                print('init_oodle_dict_succ')

            t = threading.Thread(target=init_oodle_dict)
            t.setDaemon(True)
            t.start()

    @rpc_method(CLIENT_STUB, (Str('tb_cont'),))
    def report_traceback(self, tb_cont):
        self.on_report_traceback(tb_cont)

    def on_report_traceback(self, tb_cont):
        from common.utils.str_utils import convert_python_tb_removing_locals
        new_tb_cont = convert_python_tb_removing_locals(tb_cont)
        from common.uisys.UIManager import UIManager
        ui = UIManager().get_ui('WizardTrace')
        if ui:
            ui.send_message(new_tb_cont)
        log_error('================server traceback==============\n%s', new_tb_cont)

    def bind_guest(self, bind_info):
        self.call_server_method('bind_guest', (bind_info,))

    @rpc_method(CLIENT_STUB, (Dict('bind_ret_info'),))
    def bind_guest_ret(self, bind_ret_info):
        global_data.channel.guset_bind_after_jf(bind_ret_info)

    def wiz_command(self, cmd, is_soul=False):
        method = is_soul and self.call_soul_method if 1 else self.call_server_method
        method('wiz_command', (cmd,))

    @rpc_method(CLIENT_STUB, (Str('content'),))
    def wiz_reply(self, content):
        self.logger.critical('\n%s', content)

    def on_become_player(self):
        if global_data.player:
            global_data.player.destroy()
        global_data.player = self
        log_error('AAA on_become_player', global_data.player)
        global_data.owner_entity = self
        super(Avatar, self).on_become_player()
        global_data.emgr.on_login_success_event.emit()
        from logic.comsys.login.LoginSetting import LoginSetting
        LoginSetting().update_local_server_lst()
        if global_data.message_data:
            global_data.message_data.read_local_data()
        from common.crashhunter.crashhunter_utils import update_dump_user_info
        update_dump_user_info()
        global_data.channel.set_user_info()
        global_data.emgr.avatar_finish_create_event.emit()
        global_data.emgr.avatar_finish_create_event_global.emit()
        global_data.channel.query_linegame_third_cred()
        self._call_meta_member_func('_on_login_@_success')
        self.start_game_sync_time()
        connect_using_secs, reconnect_from = ConnectHelper().get_reconnnect_using_time_info()
        if connect_using_secs:
            global_data.player.call_server_method('reconnect_using_time', (reconnect_from, connect_using_secs))
        try:
            echoes.write_last_login_info(global_data.player.uid, global_data.player.get_name())
        except:
            pass

        global_data.channel.set_roleinfo()

    def on_destroy(self):
        global_data.channel.on_user_leave_server()
        self._call_meta_member_func('_destroy_@')
        global_data.emgr.app_resume_event -= (self.on_resume,)
        global_data.emgr.app_background_event -= (self.on_background,)
        global_data.mecha = None
        global_data.player = None
        log_error('AAA on_destroy', global_data.player)
        import traceback
        global_data.last_avatar_destroy_stack = str(traceback.format_stack())
        global_data.owner_entity = None
        return

    def on_reconnected(self, extra_msg):
        super(Avatar, self).on_reconnected(extra_msg)
        global_data.emgr.net_reconnect_event.emit()
        import logic.gcommon.time_utility as t_util
        t_util.clear_logic_update()
        self.start_game_sync_time()
        self.query_cur_network_type()
        self.clear_mp_lag_trigger_cnt()

    def on_lose_server(self):
        super(Avatar, self).on_lose_server()
        self._call_meta_member_func('_disconnect_@')

    def on_resume(self):
        if self.logic:
            self.logic.send_event('E_CALL_SYNC_METHOD', 'resume_game', (), True)
        self.locally_refresh_battle_open_time()

    def on_background(self):
        if self.logic:
            self.logic.send_event('E_CALL_SYNC_METHOD', 'client_background', (), True)

    def tick(self, delta):
        if self.logic:
            self.logic.tick(delta)