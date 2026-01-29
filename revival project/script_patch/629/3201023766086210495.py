# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyRedPointData.py
from __future__ import absolute_import
import six_ex
import six
from common.framework import Singleton
from logic.gutils import item_utils
from logic.gutils import bond_utils
from logic.gutils import system_unlock_utils
from logic.gcommon.cdata import bond_gift_config
from logic.gcommon.item import item_const as iconst
from logic.gcommon.item import lobby_item_type
from logic.gutils.dress_utils import check_dec_hide_rp
from logic.gutils import red_point_utils

class LobbyRedPointData(Singleton):
    ALIAS_NAME = 'lobby_red_point_data'
    ITEM_BOOK_NEW_ITEM_TIP_RECORD_KEY = 'item_book_new_item_tip_record'

    def init(self):
        self.btn_clicked = {}
        self._item_type_click_time_func = {}
        self.init_data()
        self.process_event(True)

    def init_parameters(self):
        self.rp_data = {}
        self._item_book_info_tip_record = {}
        if global_data.player and global_data.player.uid:
            user_arch = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
            self._item_book_info_tip_record = user_arch.get_field(LobbyRedPointData.ITEM_BOOK_NEW_ITEM_TIP_RECORD_KEY, {})
        if not self._item_type_click_time_func:
            for item_type in six.iterkeys(lobby_item_type.ITEM_TYPE_CLICK_TYPE_FUNC):
                custom_func_info = lobby_item_type.ITEM_TYPE_CLICK_TYPE_FUNC[item_type]
                category, set_category_clicktime_f_name, get_category_clicktime_f_name = custom_func_info
                self._item_type_click_time_func[item_type] = [category,
                 getattr(red_point_utils, set_category_clicktime_f_name),
                 getattr(red_point_utils, get_category_clicktime_f_name)]

    def on_finalize(self):
        self.init_parameters()
        self._item_type_click_time_func = {}
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'add_item_red_point': self.add_item_rp,
           'del_item_red_point': self.del_item_rp,
           'del_item_red_point_list': self.del_item_list_rp,
           'avatar_finish_create_event': self.init_data
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_data(self):
        if not global_data.player:
            return
        self.init_parameters()
        items = global_data.player.get_view_item_list(iconst.INV_VIEW_RED_POINT_ITEM)
        for item in items:
            if item and item.get_rp_state():
                self.add_item_rp(item.get_item_no())

        from logic.gutils.role_utils import get_show_role_id_list
        self._role_id_list = get_show_role_id_list()
        global_data.emgr.refresh_item_red_point.emit()

    def add_item_rp(self, item_no):
        item_no = int(item_no)
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type not in lobby_item_type.REDPOINT_ITEM_TYPE:
            return
        if item_type in lobby_item_type.RP_ROLE_DEC_SET:
            if check_dec_hide_rp(item_no):
                return
        if item_type not in self.rp_data:
            self.rp_data[item_type] = {}
        if item_type in lobby_item_type.RP_BELONG_SET:
            belong_no = item_utils.get_lobby_item_belong_no(item_no)
            if not belong_no:
                return
            belong_no = int(belong_no)
            if belong_no not in self.rp_data[item_type]:
                self.rp_data[item_type][belong_no] = {}
            self.rp_data[item_type][belong_no][item_no] = True
        else:
            self.rp_data[item_type][item_no] = True
        global_data.emgr.refresh_item_red_point.emit()

    def del_item_rp(self, item_no):
        self.del_item_rp_data(item_no)
        global_data.emgr.refresh_item_red_point.emit()

    def del_item_list_rp(self, item_no_list):
        for item_no in item_no_list:
            self.del_item_rp_data(item_no)

        global_data.emgr.refresh_item_red_point.emit()

    def del_item_rp_data(self, item_no):
        item_no = int(item_no)
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type not in lobby_item_type.REDPOINT_ITEM_TYPE:
            return
        if item_type not in self.rp_data:
            return
        if item_type in lobby_item_type.RP_BELONG_SET:
            belong_no = item_utils.get_lobby_item_belong_no(item_no)
            if not belong_no:
                return
            belong_no = int(belong_no)
            if belong_no in self.rp_data[item_type]:
                if item_no in self.rp_data[item_type][belong_no]:
                    del self.rp_data[item_type][belong_no][item_no]
                if not self.rp_data[item_type][belong_no]:
                    del self.rp_data[item_type][belong_no]
        elif item_no in self.rp_data[item_type]:
            del self.rp_data[item_type][item_no]
        if not self.rp_data[item_type]:
            del self.rp_data[item_type]

    def get_rp_by_type(self, rp_type):
        return rp_type in self.rp_data

    def get_rp_by_type_with_click_time_check(self, rp_type):
        if rp_type in self._item_type_click_time_func:
            return self.check_item_type_click_time_red_point(rp_type)
        else:
            return rp_type in self.rp_data

    def get_rp_data_by_type(self, rp_type):
        return self.rp_data.get(rp_type, {})

    def get_rp_by_no(self, item_no):
        item_no = int(item_no)
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type not in self.rp_data:
            return False
        else:
            if item_type in lobby_item_type.RP_BELONG_SET:
                belong_no = item_utils.get_lobby_item_belong_no(item_no)
                if not belong_no:
                    return False
                belong_no = int(belong_no)
                return item_no in self.rp_data[item_type].get(belong_no, {})
            return item_no in self.rp_data[item_type]

    def get_rp_by_belong_no(self, belong_no):
        if self.get_skin_rp_by_belong_no(belong_no):
            return True
        if self.get_diy_rp_by_belong_no(belong_no):
            return True
        if self.get_dec_rp_by_belong_no(belong_no):
            return True
        return False

    def get_diy_rp_by_belong_no(self, belong_no):
        belong_no = int(belong_no)
        for item_type in lobby_item_type.RP_ROLE_DIY:
            if item_type not in self.rp_data:
                continue
            if belong_no in self.rp_data[item_type]:
                return True

        return False

    def get_dec_rp_by_belong_no(self, belong_no):
        belong_no = int(belong_no)
        for item_type in lobby_item_type.RP_ROLE_DEC_SET:
            if item_type not in self.rp_data:
                continue
            if belong_no in self.rp_data[item_type]:
                return True

        return False

    def get_skin_rp_by_belong_no(self, belong_no):
        belong_no = int(belong_no)
        item_type = item_utils.get_lobby_item_type(belong_no)
        rp_type = lobby_item_type.ROLE_TO_SKIN.get(item_type)
        if rp_type not in self.rp_data:
            return False
        if rp_type in lobby_item_type.RP_SKIN_TYPE:
            return belong_no in self.rp_data[rp_type]
        return False

    def get_rp_by_type_and_belong(self, item_type, belong_no):
        if item_type not in self.rp_data:
            return False
        belong_map = self.rp_data[item_type]
        if belong_no not in belong_map:
            return False
        return True

    def get_item_list_by_type(self, item_type):
        return self.rp_data.get(item_type, {})

    def get_rp_by_gift_type_and_belong(self, belong_no, gift_type):
        return False

    def get_rp_by_gift_type(self, gift_type):
        has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_BOND)
        if not has_unlock:
            return False
        rp_data = self.rp_data.get(lobby_item_type.L_ITEM_TYPE_BOND_GIFT_ACTIVATE)
        if not rp_data:
            return False
        for item_no in rp_data:
            rp_gift_id = bond_utils.get_gift_id_by_itemno(item_no)
            rp_gift_type = bond_utils.get_gift_type(rp_gift_id)
            if rp_gift_type == gift_type:
                return True

        return False

    def has_remind_item_book_new_item(self, item_no):
        item_no = str(item_no)
        return item_no in self._item_book_info_tip_record

    def mark_item_book_new_item_reminded(self, item_no):
        item_no = str(item_no)
        self._item_book_info_tip_record[item_no] = True
        user_arch = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
        user_arch.set_field(LobbyRedPointData.ITEM_BOOK_NEW_ITEM_TIP_RECORD_KEY, self._item_book_info_tip_record)

    def get_rp_by_item_no_list(self, item_no_list):
        for item_no in item_no_list:
            if self.get_rp_by_no(item_no):
                return True

        return False

    def get_rp_by_item_type_list(self, item_type_list, belong_no):
        for item_type in item_type_list:
            if self.get_rp_by_type_and_belong(item_type, belong_no):
                return True

        return False

    def check_main_rp(self, field):
        from logic.gutils.red_point_utils import check_dict_addition
        rp_dict = global_data.achi_mgr.get_cur_user_archive_data(field, default={})
        item_type_list = lobby_item_type.MAIN_RP_TYPE.get(field, ())
        for item_type in item_type_list:
            if check_dict_addition(rp_dict, {item_type: self.rp_data.get(item_type, {})}):
                if item_type in self._item_type_click_time_func:
                    if self.check_item_type_click_time_red_point(item_type):
                        return True
                return True

        return False

    def record_main_rp(self, field):
        from logic.gutils.red_point_utils import copy_dict
        item_type_list = lobby_item_type.MAIN_RP_TYPE.get(field, ())
        rp_dict = copy_dict({item_type:self.rp_data.get(item_type, {}) for item_type in item_type_list})
        global_data.achi_mgr.set_cur_user_archive_data(field, rp_dict)
        global_data.emgr.refresh_item_red_point.emit()

    def get_item_type_rp_click_time(self, item_type, *args, **kwargs):
        if item_type not in self._item_type_click_time_func:
            return False
        c_func = self._item_type_click_time_func[item_type]
        category, _, get_func = c_func
        return get_func(category, item_type, *args, **kwargs)

    def set_item_type_rp_click_time(self, item_type, *args, **kwargs):
        if item_type not in self._item_type_click_time_func:
            return
        c_func = self._item_type_click_time_func[item_type]
        category, set_func, _ = c_func
        if set_func:
            set_func(category, item_type, *args, **kwargs)
        global_data.emgr.refresh_item_red_point.emit()

    def check_item_type_click_time_red_point(self, item_type):
        if not global_data.player:
            return False
        role_id_list = self._role_id_list
        item_dict = self.rp_data.get(item_type, {})
        for role_id in role_id_list:
            click_time = global_data.lobby_red_point_data.get_item_type_rp_click_time(item_type, role_id)
            for item_no in six_ex.keys(item_dict):
                item_info = global_data.player.get_item_by_no(int(item_no))
                if not item_info:
                    continue
                if item_info.get_create_time() > click_time:
                    return True

        return False