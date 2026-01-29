# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/CharacterSelect.py
from __future__ import absolute_import
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Bool, Int, Dict, List
from logic.entities.BaseClientAvatar import BaseClientAvatar
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_COMPLETE_REGISTRATION
from logic.gcommon.common_const import guide_const
from logic.gcommon.time_utility import get_readable_time
from common.cinematic.VideoPlayer import VideoPlayer
from common.cfg import confmgr
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
import game3d
import six.moves.builtins

class CharacterSelect(BaseClientAvatar):

    def init_from_dict(self, bdict):
        self.character_dict = None
        self.name_list = None
        self.us_random_name_list = None
        self.select_character_idx = None
        self.anti_addiction_msg = None
        self._show_birthday_tip = False
        self.skip_antiaddiction_notification = bdict.get('skip_antiaddiction_notification', False)
        return

    def on_become_player(self):
        self.reset_net_user_callback()
        global_data.player = None
        log_error('AAA CharacterSelect on_become_player', global_data.player)
        global_data.owner_entity = self
        super(CharacterSelect, self).on_become_player()
        return

    def on_destroy(self):
        pass

    def load_finish(self):
        global_data.emgr.camera_inited_event.emit()

    @rpc_method(CLIENT_STUB, (Dict('char_dict'), Int('show_index'), Int('max_char'), Bool('first_created')))
    def update_character(self, char_dict, show_index, max_char, first_created=False):
        self.character_dict = char_dict
        self.select_character_idx = show_index
        self.max_char = max_char
        if len(self.character_dict) > 0:
            local_battle = global_data.player.local_battle if global_data.player else None
            if local_battle:
                global_data.player.local_battle.destroy()
            global_data.ui_mgr.close_ui('CharacterCreatorUINew')
            select_character_idx = six_ex.keys(self.character_dict)[0]
            if first_created:
                Appsflyer().advert_track_event(AF_COMPLETE_REGISTRATION)
                if global_data.channel:
                    global_data.channel.on_character_created()
            self.select_character(select_character_idx)
        else:
            self.check_anti_addiction_before_create_role()
        return

    @rpc_method(CLIENT_STUB, (Str('msg'),))
    def on_anti_addiction_msg(self, msg):
        self.anti_addiction_msg = msg

    @rpc_method(CLIENT_STUB, ())
    def show_birthday_tip(self):
        self._show_birthday_tip = True

    def check_anti_addiction_before_create_role(self):
        if not self.anti_addiction_msg:
            self.create_role_logic()
            return

        def _confirm(*args):
            if self._show_birthday_tip:
                NormalConfirmUI2(on_confirm=self.create_role_logic).set_content_string(82113)
                return
            self.create_role_logic()

        NormalConfirmUI2(on_confirm=_confirm).set_content_string(self.anti_addiction_msg)

    def create_role_logic(self):
        global_data.emgr.account_request_create_usr.emit()
        if 'auto_login' in six.moves.builtins.__dict__:
            return
        from logic.comsys.login.CharacterCreatorUINew import CharacterCreatorUINew
        from logic.gutils import qte_guide_utils
        if global_data.channel and global_data.channel._hostnum in (78, 54, 9002):
            CharacterCreatorUINew(no_finish=True, opt_from='update_character')
            return
        if qte_guide_utils.is_finish_qte_guide():
            CharacterCreatorUINew(no_finish=True, opt_from='update_character')
        elif qte_guide_utils.get_qte_chosen_role_id():
            self.start_newbie_qte_guide(qte_guide_utils.get_qte_chosen_role_id())
        else:
            dialog_config = confmgr.get('video_dialog_conf', 'IntroConfig', 'Content')
            if not global_data.deviceinfo.is_huawei_device():
                cb = lambda : True
                VideoPlayer().play_video('video/intro.mp4', self.open_select_ui, dialog_config)
            else:
                self.open_select_ui()

    def open_select_ui(self):
        from logic.comsys.login.CharacterSelectUINew import CharacterSelectUINew
        CharacterSelectUINew()

    def start_newbie_qte_guide(self, role_id):
        from mobile.common.EntityFactory import EntityFactory
        from mobile.common.IdManager import IdManager
        from logic.client.const.game_mode_const import QTE_LOCAL_BATTLE_TYPE
        local_avatar_id = IdManager.genid()
        local_avatar = EntityFactory.instance().create_entity('Avatar', local_avatar_id)
        bdict = {'uid': IdManager.id2str(local_avatar_id),
           'user_name': IdManager.id2str(local_avatar_id),
           'role_id': role_id,
           'role_list': [
                       role_id],
           'mecha_open': {'opened_order': [
                                         8001, 8002]
                          }
           }
        local_avatar.init_from_dict(bdict)
        global_data.player = local_avatar
        log_error('AAA start_newbie_qte_guide', global_data.player)
        local_avatar.try_start_new_local_battle(QTE_LOCAL_BATTLE_TYPE)

    @rpc_method(CLIENT_STUB, (List('name_list'),))
    def update_name(self, name_list):
        for idx, name in enumerate(name_list):
            if type(name).__name__ == 'unicode':
                try:
                    name_list[idx] = name.encode('utf-8')
                except Exception:
                    name_list[idx] = ''

        self.name_list = name_list
        global_data.emgr.on_used_name_updated_event.emit()

    def request_us_random_name(self, sex):
        self.call_server_method('request_us_random_name', (sex,))

    @rpc_method(CLIENT_STUB, (List('name_list'),))
    def request_us_random_name_ret(self, name_list):
        for idx, name in enumerate(name_list):
            if type(name).__name__ == 'unicode':
                try:
                    name_list[idx] = name.encode('utf-8')
                except Exception:
                    name_list[idx] = ''

        self.us_random_name_list = name_list
        global_data.emgr.on_random_name_updated_event.emit()

    def create_character(self, char_name, sex, combat_lv):
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        self.call_server_method('create_character', {'char_name': char_name,'sex': sex,'combat_lv': combat_lv,'lang': get_cur_text_lang()})

    def select_character(self, idx):
        self.select_character_idx = idx
        self.call_server_method('select_character', {'idx': idx})

    @rpc_method(CLIENT_STUB, (Str('reason'),))
    def verify_lock_status_failed(self, reason):
        global_data.game_mgr.show_tip(reason, True)

    @rpc_method(CLIENT_STUB, (Int('reason'), Dict('args')))
    def notified_fail_message(self, reason, args):
        if 'auto_login' in six.moves.builtins.__dict__:
            global_data.emgr.account_request_create_usr.emit()
            return
        from logic.gcommon.time_utility import get_date_str
        from logic.comsys.feedback import echoes
        from logic.comsys.feedback.echoes import LOGIN, LOBBY
        global_data.emgr.on_login_failed_event.emit(reason, 'CharacterSelect failed: %s' % reason)
        if 'id_reason' in args:
            args['id_reason'] = get_text_by_id(args['id_reason'])
        if 'timelen' in args:
            if args['timelen'] < 0:
                args['timelen'] = get_text_by_id(80953)
            else:
                args['timelen'] = get_date_str('%Y.%m.%d', args['timelen'])
        content = get_text_by_id(reason, args)
        if args.get('customer_service', 0):
            if global_data.is_pc_mode:
                from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2

                def confirm_callback():
                    game3d.exit()

                NormalConfirmUI2(on_confirm=confirm_callback, confirm_text=get_text_by_id(140), content=content)
            elif game3d.get_app_name() == 'com.netease.g93natw':

                def cancel_callback():
                    if args.get('uid') and args.get('char_name'):
                        echoes.show_tw_customer_service_view(LOBBY, args)
                    else:
                        echoes.show_tw_customer_service_view(LOGIN)

                def confirm_callback():
                    game3d.exit()

                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                SecondConfirmDlg2().confirm(title=get_text_by_id(605003), content=content, cancel_auto_close=False, confirm_auto_close=False, confirm_text=get_text_by_id(140), cancel_text=get_text_by_id(605004), cancel_callback=cancel_callback, confirm_callback=confirm_callback, click_blank_close=False)
            elif args.get('uid') and args.get('char_name'):

                def cancel_callback():
                    self.get_custom_service_token(args.get('uid'), args.get('char_name'))

                def confirm_callback():
                    game3d.exit()

                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                SecondConfirmDlg2().confirm(title=get_text_by_id(605003), content=content, cancel_auto_close=False, confirm_auto_close=False, confirm_text=get_text_by_id(140), cancel_text=get_text_by_id(605004), cancel_callback=cancel_callback, confirm_callback=confirm_callback, click_blank_close=False)
            else:
                from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2

                def confirm_callback():
                    game3d.exit()

                NormalConfirmUI2(on_confirm=confirm_callback, confirm_text=get_text_by_id(140), content=content)
        else:
            global_data.game_mgr.show_tip(content, True)

    def get_custom_service_token(self, uid, char_name):
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        self.call_server_method('get_custom_service_token', (uid, char_name, get_cur_text_lang()))

    @rpc_method(CLIENT_STUB, (Str('token'),))
    def get_custom_service_token_callback(self, token):
        import game3d
        from logic.gcommon.common_utils import local_text
        from logic.gcommon.common_const.lang_data import LANG_JA
        if hasattr(game3d, 'open_gm_web_view'):
            game3d.set_gmbridge_token(token)
        else:
            data = {'methodId': 'ntSetGenTokenResponse',
               'response': token
               }
            global_data.channel.extend_func_by_dict(data)
        lang = local_text.get_cur_text_lang()
        if G_IS_NA_USER:
            sid = 247 if lang == LANG_JA else 210
            refer = '/kefu/osgm/%d' % sid
        else:
            sid = 3859
            refer = '/zq/add/%d' % sid
        data = {'methodId': 'ntOpenGMPage','refer': refer}
        global_data.channel.extend_func_by_dict(data)

    def realname_callback(self, *args, **kwargs):
        global_data.emgr.on_login_failed_event.emit()
        self.change_to_login()

    def regist_realname(self, realname, id_num, region_id):
        self.call_server_method('regist_realname', (realname, id_num, region_id))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Str('msg')))
    def regist_realname_ret(self, ret, msg):
        global_data.emgr.regist_realname_result.emit(ret, msg)