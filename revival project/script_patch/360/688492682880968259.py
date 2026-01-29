# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBase.py
from __future__ import absolute_import
import six
from mobile.common.RpcMethodArgs import Str, Dict, Int, List, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon import const
import logic.gutils.lv_template_utils as lv_template_utils
from logic.gcommon.common_const import statistics_const as stat_const
import time
LOG_INTERVAL = 60

class impBase(object):

    def _init_base_from_dict(self, bdict):
        self.create_time = bdict.get('create_time', 0)
        self.user_name = bdict['user_name']
        self.urs = bdict.get('urs', '')
        self.char_name = bdict.get('char_name', '')
        self.region_tag = bdict.get('region_tag', 0)
        self.intro = bdict.get('intro', '')
        self.gold = int(bdict.get('gold', 0))
        self.diamond = int(bdict.get('diamond', 0))
        self.yuanbao = int(bdict.get('yuanbao', 0))
        self.fine_yuanbao = int(bdict.get('fine_yuanbao', 0))
        self.pay_yuanbao = int(bdict.get('pay_yuanbao', 0))
        self.free_yuanbao = int(bdict.get('free_yuanbao', 0))
        self.sex = bdict.get('sex', const.AVATAR_SEX_NONE)
        self.last_set_sex_time = bdict.get('sex_time', 0)
        self.login_country = bdict.get('login_country', '')
        self.game_ver = bdict.get('game_ver', 0)
        self.server_ver = bdict.get('server_ver', 0)
        self.fashion_value = bdict.get('fashion_value', 0)
        self.log_info = {}
        self.battle_tmp_consume = {}
        try:
            if 'ui_lang' in bdict and global_data.ui_mgr:
                global_data.ui_mgr.change_lang(*bdict['ui_lang'])
        except:
            pass

    def get_urs(self):
        return self.urs

    def get_create_time(self):
        return self.create_time

    def get_region(self):
        return self.region_tag

    def get_name(self):
        return self.char_name

    def get_intro(self):
        return self.intro

    def set_name(self, new_name):
        self.char_name = new_name

    def set_intro(self, intro):
        self.intro = intro

    def set_sex(self, sex, change_time):
        self.sex = sex
        self.last_set_sex_time = change_time

    def get_sex(self):
        return self.sex

    def get_gold(self):
        return self.gold

    def get_diamond(self):
        return self.diamond

    def get_yuanbao(self):
        return self.yuanbao

    def get_item_money(self, itemno):
        return global_data.player.get_item_num_by_no(itemno)

    def get_fashion_value(self):
        return self.fashion_value

    def get_login_country(self):
        return self.login_country

    def get_battle_tmp_consume(self, coin_type):
        return self.battle_tmp_consume.get(coin_type, 0)

    @rpc_method(CLIENT_STUB, (Dict('update_info'),))
    def sync_battle_consume(self, update_info):
        self.battle_tmp_consume.update(update_info)

    @rpc_method(CLIENT_STUB, (Str('content'),))
    def show_msg(self, content):
        self.show_msg_imp(content)

    def show_msg_imp(self, content):
        real_content = unpack_text(content)
        global_data.emgr.battle_show_message_event.emit(real_content)

    @rpc_method(CLIENT_STUB, (Str('content'),))
    def notify_client_message(self, content):
        global_data.game_mgr.show_tip(content, True)

    def set_born_date(self, born_date):
        self.call_server_method('set_born_date', (born_date,))

    def has_enough_gold(self, gold_need):
        if gold_need < 0:
            return False
        return self.gold >= gold_need

    def has_enough_diamond(self, diamond_need):
        if diamond_need < 0:
            return False
        return self.diamond >= diamond_need

    def show_exp_or_level_up(self, old_lv, new_lv, old_exp, add_exp):

        def callback():
            ui = global_data.ui_mgr.show_ui('EndLevelUI', 'logic.comsys.battle.Settle')
            if ui:
                show_data = {'old_lv': old_lv,'new_lv': new_lv or self.lv,'old_exp': old_exp,'add_exp': add_exp}
                ui.play_animation(show_data)

        self.add_advance_callback('EndLevelUI', callback)
        if not self.is_running_show_advance():
            self.start_show_advance()

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def update_player_info(self, data):
        extra_data = data.pop('extra_data', {})
        is_emit_money_update = False
        MONEY_KEY = {'gold': 0,'diamond': 0,'yuanbao': 0,'fine_yuanbao': 0,'free_yuanbao': 0,'pay_yuanbao': 0}
        is_add_card_attr_update = False
        ADD_CARD_KEY = {'duo_exp_timestamp': 0,'duo_exp_point': 0,'duo_prof_timestamp': 0,'duo_prof_point': 0}
        new_lv = data.get('lv', None)
        old_lv = global_data.player.get_lv()
        need_lv_update = False
        in_battle = global_data.player.is_in_battle()
        if new_lv and new_lv != self.lv and not in_battle:
            need_lv_update = True
            old_exp = global_data.player.get_exp()
            add_exp = lv_template_utils.get_add_exp_by_lv_range(old_lv, old_exp, new_lv, data.get('exp', 0))
            self.show_exp_or_level_up(old_lv, new_lv, old_exp, add_exp)
        elif extra_data.get('need_show_exp', False) and not in_battle:
            old_exp = global_data.player.get_exp()
            new_lv = global_data.player.get_lv()
            add_exp = lv_template_utils.get_add_exp_by_lv_range(old_lv, old_exp, new_lv, data.get('exp', 0))
            self.show_exp_or_level_up(old_lv, new_lv, old_exp, add_exp)
        for k, v in six.iteritems(data):
            setattr(self, k, v)
            if k in MONEY_KEY:
                is_emit_money_update = True
            if k in ADD_CARD_KEY:
                is_add_card_attr_update = True

        if need_lv_update:
            global_data.emgr.player_lv_update_event.emit(data)
            if global_data.channel:
                global_data.channel.on_user_lv_update()
        global_data.emgr.player_info_update_event.emit()
        lv_change = new_lv and old_lv != new_lv
        if lv_change:
            global_data.new_sys_open_mgr.level_check(old_lv, new_lv)
            if not in_battle:
                global_data.new_sys_open_mgr.check_show_ui()
            global_data.sys_unlock_mgr.level_check(old_lv, new_lv)
            if not in_battle:
                global_data.sys_unlock_mgr.check_show_ui()
        if is_emit_money_update:
            global_data.emgr.player_money_info_update_event.emit()
        if is_add_card_attr_update:
            global_data.emgr.role_add_card_attr_update_event.emit()
        return

    @rpc_method(CLIENT_STUB, (Dict('reward_dict'), Str('reason'), Bool('ignore_in_battle')))
    def offer_reward(self, reward_dict, reason, ignore_in_battle):
        self.offer_reward_imp(reward_dict, reason, ignore_in_battle)

    def offer_reward_imp(self, reward_dict, reason, ignore_in_battle=True):
        items = reward_dict.get('item_dict', {})
        chips = reward_dict.get('chips_source', {})
        from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
        ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        if ignore_in_battle or not ui and not global_data.player.is_in_battle():
            ReceiveRewardUI()
        global_data.emgr.receive_award_succ_event.emit(items, chips, reason)

    @rpc_method(CLIENT_STUB, (Str('token'),))
    def get_custom_service_token_callback(self, token):
        import game3d
        if hasattr(game3d, 'open_gm_web_view'):
            game3d.set_gmbridge_token(token)
        else:
            data = {'methodId': 'ntSetGenTokenResponse',
               'response': token
               }
            global_data.channel.extend_func_by_dict(data)

    @rpc_method(CLIENT_STUB, (Str('msg'),))
    def gm_open_custom_service(self, msg):
        import game3d
        if global_data.player:
            if hasattr(game3d, 'open_gm_web_view'):
                game3d.show_gm_float_button(True, str(global_data.player.id), msg)
            else:
                data = {'methodId': 'ntReceiveMessage',
                   'message': msg
                   }
                global_data.channel.extend_func_by_dict(data)

    @rpc_method(CLIENT_STUB, ())
    def gm_upload_client_log(self):
        from common.crashhunter import crashhunter_utils
        crashhunter_utils.upload_client_log()

    def request_player_simple_inf(self, uid):
        self.request_player_info(const.PLAYER_INFO_BRIEF, uid)

    def request_player_detail_inf(self, uid):
        self.request_player_info(const.PLAYER_INFO_DETAIL, uid)

    def generate_my_info(self):
        bp_lv, bp_point = self.get_battlepass_info()
        data = {'lv': self.get_lv(),
           'char_name': self.get_name(),
           'role_id': self.get_role(),
           'role_fashion': self.get_item_by_no(self.get_role()).get_fashion(),
           'uid': self.uid,
           'exp': self.get_exp(),
           'intro': self.get_intro(),
           'head_frame': self.get_head_frame(),
           'head_photo': self.get_head_photo(),
           'dan_info': self.get_dan_info(),
           'battlepass_lv': bp_lv,
           'battlepass_types': self.get_battlepass_types(),
           'fans_count': self.get_fans_count(),
           'history_max_dan': self.get_history_max_dan(),
           'total_game_time': self.get_stat(stat_const.TOTAL_GAME_TIME, 0),
           'item_stat': self.inventory.get_stat_dict(),
           'top_mechas': self.get_top_mechas(),
           'last_season': self.get_battle_season(),
           'clan_info': {'clan_id': self.get_clan_id(),
                         'clan_name': self.get_clan_name(),'lv': self.get_clan_lv(),
                         'badge': self.get_clan_badge()},
           'sex': self.get_sex(),
           'charm': self.get_charm_value(),
           'rank_adcode': self.rank_adcode,
           'rank_use_title_dict': self.rank_use_title_dict,
           'intimacy_data': self.intimacy_data
           }
        return data

    def request_player_info(self, info_type, uid, force=False):
        if not force and uid == self.uid:
            data = self.generate_my_info()
            self.reply_player_info((info_type, data))
        else:
            self.call_server_method('request_player_info', (info_type, uid))

    @rpc_method(CLIENT_STUB, (Int('info_type'), Dict('data')))
    def reply_player_info(self, info_type, data):
        global_data.message_data.set_player_inf(info_type, data)

    def request_players_simple_inf(self, uidlist):
        self.request_players_info(const.PLAYER_INFO_BRIEF, uidlist)

    def request_players_detail_inf(self, uidlist):
        self.request_players_info(const.PLAYER_INFO_DETAIL, uidlist)

    def request_players_info(self, info_type, uidlist):
        self.call_server_method('request_players_info', (info_type, uidlist))

    @rpc_method(CLIENT_STUB, (Int('info_type'), List('datas')))
    def reply_players_info(self, info_type, datas):
        for data in datas:
            global_data.message_data.set_player_inf(info_type, data)

        global_data.emgr.message_on_players_detail_inf.emit(datas)

    def notify_text_lang(self, lang):
        self.call_server_method('set_text_lang', (lang,))

    @rpc_method(CLIENT_STUB, ())
    def gm_show_scene_collision(self):
        from logic.gutils import scene_utils
        scene_utils.show_scene_collision()

    @rpc_method(CLIENT_STUB, ())
    def gm_show_hit_box(self):
        from logic.gcommon import const
        const.HIT_MODEL_VISIBLE = True
        PartShootManager = global_data.game_mgr.scene.get_com('PartShootManager')
        if PartShootManager:
            for human in six.itervalues(PartShootManager.shoot_humans):
                model = human.ev_g_model()
                if model:
                    model.set_submesh_visible('hit', const.HIT_MODEL_VISIBLE)

            for mecha in six.itervalues(PartShootManager.shoot_mecha):
                model = mecha.ev_g_model()
                if model:
                    model.set_submesh_visible('hit', const.HIT_MODEL_VISIBLE)

    def can_send_general_log(self, entity_id, log_key):
        if not log_key:
            return False
        else:
            entity_info = self.log_info.get(entity_id, None)
            if not entity_info:
                return True
            last_time = entity_info.get(log_key, 0)
            pass_time = time.time() - last_time
            return pass_time >= LOG_INTERVAL

    def upload_general_log(self, entity_id, log_key, param_dict):
        if not log_key:
            return
        entity_info = self.log_info.setdefault(entity_id, {})
        entity_info[log_key] = time.time()
        self.call_server_method('save_general_log', (log_key, param_dict))