# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComStatus.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
import logic.gcommon.const as const
import time
import traceback
if G_IS_CLIENT:
    import game3d
    IS_CLIENT_WIN32 = game3d.get_platform() == game3d.PLATFORM_WIN32
else:
    IS_CLIENT_WIN32 = False

class ComStatus(UnitCom):
    STATUS_FORBID = 1
    STATUS_COVER = 2
    MAX_STATUS_DURATION_SCALE = 2
    DEAD_STATE = None
    BIND_EVENT = {'G_STATUS_TRY_TRANS': '_try_trans_st',
       'E_SET_LOCK_TIME': '_set_lock_time',
       'G_CANCEL_STATE': '_cancel_state',
       'G_GET_STATE': 'get_state',
       'G_GET_ALL_STATE': 'get_all_state',
       'G_IS_IN_ANY_STATE': '_is_in_any_state',
       'G_STATUS_CHECK_PASS': '_check_pass',
       'E_DUMP_STATE': '_dump_state',
       'G_GET_STATE_VALUE': 'get_str_state_2_num',
       'G_GET_STATE_DESC': '_get_nulm_state_2_str',
       'E_STATUS_LOG': 'enable_log',
       'E_REGISTER_UNLOCK_HOOK': '_register_unlock_hook',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'G_NEW_COVER_OLD_STATE': 'is_new_cover_old_state',
       'G_GET_STATUS_DURATION': 'get_status_duration',
       'E_UPDATE_STATUS_TIME': 'update_status_start_time',
       'E_ADD_WHITE_STATE': 'on_add_white_state',
       'E_CLEAR_WHITE_STATE': 'on_clear_white_state',
       'E_ADD_BLACK_STATE': 'on_add_black_state',
       'E_DEL_BLACK_STATE': 'on_del_black_state',
       'E_CLEAR_BLACK_STATE': 'on_clear_black_state',
       'G_CAN_COVER_STATES': 'get_can_cover_states',
       'G_IS_COVER_STATE': 'is_cover_state',
       'G_ALL_LOGIC_STATE_DESC': 'get_all_state_desc',
       'E_RESET_STATE': 'reset_state'
       }

    def __init__(self):
        super(ComStatus, self).__init__()
        self.set_st = set()
        self.is_open_log = False
        self.mp_st_forbid = {}
        self.mp_st_cover = {}
        self.unlock_hoot = {}
        self.maxlock_duration = {}
        self.status_config = None
        self._is_debug_mode = False
        self._debug_status_stack = {}
        self._status_start_time = {}
        self._white_state = set([])
        self._white_state_to_cover = {}
        self._black_state = set([])
        self.is_show_status_out_of_time = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComStatus, self).init_from_dict(unit_obj, bdict)

    def _change_character_attr(self, name, *arg):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        value = arg[0]
        if name == 'debug_status':
            self._is_debug_mode = bool(value)

    def reset(self):
        self.set_st = set()
        self._white_state = set([])
        self._white_state_to_cover = {}
        self._black_state = set([])

    def on_add_white_state(self, state, to_cover_state_list=None):
        if isinstance(state, int):
            state = set([state])
        self._white_state |= state
        if to_cover_state_list:
            if isinstance(to_cover_state_list, int):
                to_cover_state_list = [
                 to_cover_state_list]
            for one_state in state:
                self._white_state_to_cover[one_state] = set(to_cover_state_list)

    def on_clear_white_state(self, *args):
        self._white_state = set([])
        self._white_state_to_cover = {}

    def on_add_black_state(self, state):
        self._black_state |= state

    def on_del_black_state(self, state):
        self._black_state -= state

    def on_clear_black_state(self):
        self._black_state = set([])

    def check_white_state(self, new_st):
        return new_st in self._white_state

    def check_black_state(self, new_st):
        return new_st in self._black_state

    def is_new_cover_old_state(self, old_state, new_state):
        return old_state in self.mp_st_cover[new_state]

    def remove_state(self, status):
        if isinstance(status, int):
            if status in self.set_st:
                self.set_st.remove(status)
        else:
            for one_status in status:
                if one_status in self.set_st:
                    self.set_st.remove(one_status)

    def _cancel_state(self, cancel_simple_state, sync=False):
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'try_cancel_status', (cancel_simple_state,), True)
        if cancel_simple_state not in self.set_st:
            return
        self.remove_state(cancel_simple_state)
        self._cancel_combine_state(cancel_simple_state)
        self.send_event('E_LEAVE_STATE', cancel_simple_state)

    def _cancel_combine_state(self, cancel_simple_state):
        if self.status_config is None:
            return
        else:
            for combine_state, simple_states in six.iteritems(self.status_config.combine_state):
                if cancel_simple_state in simple_states:
                    if combine_state in self.set_st:
                        self.remove_state(combine_state)
                        self.send_event('E_LEAVE_STATE', combine_state)

            return

    def enable_log(self, is_log):
        self.is_open_log = bool(is_log)

    def _register_unlock_hook(self, status, hook_func):
        if isinstance(status, (list, tuple)):
            for one_status in status:
                self.unlock_hoot[one_status] = hook_func

        else:
            self.unlock_hoot[status] = hook_func

    def _set_lock_time(self, new_st, lock_duration):
        if lock_duration <= 0:
            return
        self.maxlock_duration[new_st] = {'start_time': time.time(),'lock_duration': lock_duration}

    def remove_invalid_status(self, new_st):
        cur_time = time.time()
        for status, hook_func in six.iteritems(self.unlock_hoot):
            if status in self.set_st:
                if status in self.maxlock_duration:
                    state_config = self.maxlock_duration[status]
                    pass_time = cur_time - state_config['start_time']
                    if pass_time < state_config['lock_duration']:
                        continue
                    del self.maxlock_duration[status]
                hook_func(status, new_st)

        remove_status = []
        for status in self.set_st:
            max_duration = self.get_status_max_duration(status)
            if max_duration is not None and max_duration > 0:
                start_time = self._status_start_time.get(status, 0)
                pass_time = cur_time - start_time
                if pass_time >= max_duration:
                    if not remove_status:
                        self.send_event('E_DUMP_STATE')
                    remove_status.append(status)
                    traceback_desc = ''
                    if self._is_debug_mode:
                        traceback_desc = self._debug_status_stack.get(status, '')
                    if self.is_show_status_out_of_time:
                        error_desc_list = [
                         '[ComStatus] [warning] invalid status = ', self._get_nulm_state_2_str(status), '--pass_time =', str(pass_time), '--max_duration =', str(max_duration), '\n', traceback_desc]
                        error_desc = ''.join(error_desc_list)
                        self.send_event('E_SHOW_MESSAGE', error_desc)

        for status in remove_status:
            self._cancel_state(status)

        self.resolve_empty_status()
        return

    def get_status_max_duration(self, status):
        if not self.status_config:
            print(('[Error] test--status =', status, '--unit_obj =', self.unit_obj))
            import traceback
            traceback.print_stack()
            return 0
        else:
            max_duration = self.status_config.state_duration_config.get(status, -1)
            if max_duration == 0:
                model = self.ev_g_model()
                clip_name = self.status_config.state_clip_config.get(status, None)
                if model and clip_name:
                    max_duration = model.get_anim_length(clip_name)
                    max_duration /= 1000.0
                    max_duration *= self.MAX_STATUS_DURATION_SCALE
                    self.status_config.state_duration_config[status] = max_duration
            return max_duration

    def _check_pass(self, new_st, is_quiet=False, only_avatar=True, ignore_st=None):
        self.remove_invalid_status(new_st)
        if type(new_st) is str:
            if not hasattr(self.status_config, new_st):
                return 0
            new_st = getattr(self.status_config, new_st)
        if new_st not in self.mp_st_forbid:
            if G_IS_CLIENT:
                pass
            return 0
        else:
            can_cover_states = None
            if self.check_white_state(new_st):
                can_cover_states = self._white_state_to_cover.get(new_st, None)
                if not can_cover_states:
                    return True
            if self.check_black_state(new_st):
                return False
            all_forbid_set = self.mp_st_forbid[new_st]
            if ignore_st:
                all_forbid_set = all_forbid_set - ignore_st
            if can_cover_states:
                all_forbid_set = all_forbid_set - can_cover_states
            if all_forbid_set & self.set_st:
                if self.is_open_log:
                    import logic.gcommon.cdata.status_config as status_config
                    forbid_set = all_forbid_set & self.set_st
                    print('test--_check_pass--forbid--new_st = ', self._get_nulm_state_2_str(new_st), ', --new_st_val =', str(new_st), ', --forbit_set = ', self._get_nulm_state_2_str(forbid_set), ', --self.unit_obj = ', self.unit_obj.__class__.__name__)
                return 0
            is_pass = 1
            is_check_add = new_st not in self.set_st
            self.set_st.add(new_st)
            combine_state = self._gen_combine_state(new_st)
            if combine_state:
                if combine_state not in self.mp_st_forbid:
                    if G_IS_CLIENT:
                        pass
                    is_pass = 0
                all_forbid_set = self.mp_st_forbid[combine_state]
                if ignore_st:
                    all_forbid_set = all_forbid_set - ignore_st
                if can_cover_states:
                    all_forbid_set = all_forbid_set - can_cover_states
                if all_forbid_set & self.set_st:
                    if self.is_open_log:
                        forbid_set = all_forbid_set & self.set_st
                        print('test--_check_pass--forbid--new_st = ', self._get_nulm_state_2_str(new_st), ', --new_st_val = ', new_st, ', --combine_state = ', self._get_nulm_state_2_str(combine_state), ', --new_combine_st_val = ', str(combine_state), ', --forbit_set = ', self._get_nulm_state_2_str(forbid_set), ', --self.unit_obj = ', self.unit_obj.__class__.__name__)
                    is_pass = 0
            if is_check_add:
                self.set_st.remove(new_st)
            if is_pass and is_quiet:
                can_cover_states = self.mp_st_cover.get(new_st, set())
                if can_cover_states & self.set_st:
                    return 0
            return is_pass

    def _cover_state(self, new_st):
        can_cover_states = self.mp_st_cover.get(new_st, set())
        need_cover_old_states = can_cover_states & self.set_st
        if need_cover_old_states:
            self.remove_state(can_cover_states)
            for one_simple_state in need_cover_old_states:
                self._cancel_combine_state(one_simple_state)

        return need_cover_old_states

    def get_status_duration(self, st):
        if st not in self.set_st:
            return 0
        now = time.time()
        return now - self._status_start_time.get(st, now)

    def update_status_start_time(self, new_st):
        self._status_start_time[new_st] = time.time()

    def get_can_cover_states(self, new_st):
        need_cover_old_states = None
        if self.check_white_state(new_st):
            can_cover_states = self._white_state_to_cover.get(new_st, None)
            if can_cover_states:
                need_cover_old_states = can_cover_states & self.set_st
                can_cover_states = self.mp_st_cover.get(new_st, set())
                need_cover_old_states |= can_cover_states & self.set_st
            else:
                need_cover_old_states = self.set_st.copy()
        else:
            if not self._check_pass(new_st):
                return need_cover_old_states
            can_cover_states = self.mp_st_cover.get(new_st, set())
            need_cover_old_states = can_cover_states & self.set_st
        return need_cover_old_states

    def _try_trans_st(self, new_st, sync=False, force=False):
        if self.check_white_state(new_st):
            can_cover_states = self._white_state_to_cover.get(new_st, None)
            if can_cover_states:
                need_cover_old_states = can_cover_states & self.set_st
                if need_cover_old_states:
                    self.remove_state(can_cover_states)
                for one_simple_state in need_cover_old_states:
                    self._cancel_combine_state(one_simple_state)

                need_cover_old_states |= self._cover_state(new_st)
            else:
                need_cover_old_states = self.set_st.copy()
                self.reset()
            self.on_clear_white_state()
        else:
            if not force and not self._check_pass(new_st):
                return False
            need_cover_old_states = self._cover_state(new_st)
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'try_trans_status', (new_st,), True)
        self.set_st.add(new_st)
        now_time = time.time()
        self._status_start_time[new_st] = now_time
        for one_old_state in need_cover_old_states:
            self.send_event('E_LEAVE_STATE', one_old_state, new_st)

        self.send_event('E_ENTER_STATE', new_st)
        combine_state = self._gen_combine_state(new_st)
        if combine_state:
            if not self._check_pass(combine_state):
                self.remove_state(new_st)
                return False
            need_cover_old_states = self._cover_state(combine_state)
            self.set_st.add(combine_state)
            for one_old_state in need_cover_old_states:
                self.send_event('E_LEAVE_STATE', one_old_state, combine_state)

            self.send_event('E_ENTER_STATE', combine_state)
        if combine_state:
            self._status_start_time[combine_state] = now_time
        if self._is_debug_mode:
            stack = traceback.format_stack()
            self._debug_status_stack[new_st] = ''.join(stack)
            if combine_state:
                self._debug_status_stack[combine_state] = ''.join(stack)
        return True

    def _gen_combine_state(self, add_simple_state):
        if self.status_config is None:
            return
        else:
            for combine_state, simple_states in six.iteritems(self.status_config.combine_state):
                if add_simple_state in simple_states:
                    if simple_states.issubset(self.set_st):
                        return combine_state

            return

    def get_str_state_2_num(self, state_desc):
        if isinstance(state_desc, list) or isinstance(state_desc, tuple) or isinstance(state_desc, set):
            num_states = []
            for one_state_desc in state_desc:
                one_state = self.status_config.desc_2_num.get(one_state_desc, 'Unknow')
                num_states.append(one_state)

            return num_states
        else:
            if isinstance(state_desc, dict):
                num_states = []
                for one_state_desc in six.iterkeys(state_desc):
                    one_state = self.status_config.desc_2_num.get(one_state_desc, 'Unknow')
                    num_states.append(one_state)

                return num_states
            return self.status_config.desc_2_num.get(state_desc, 'Unknow')

    def _get_nulm_state_2_str(self, state):
        if isinstance(state, list) or isinstance(state, tuple) or isinstance(state, set):
            str_states = []
            for one_state in state:
                one_state = self.status_config.num_2_desc.get(one_state, 'Unknow')
                str_states.append(one_state)

            return str_states
        else:
            if isinstance(state, dict):
                str_states = []
                for one_state in six.iterkeys(state):
                    one_state = self.status_config.num_2_desc.get(one_state, 'Unknow')
                    str_states.append(one_state)

                return str_states
            return self.status_config.num_2_desc.get(state, 'Unknow')

    def _dump_state(self):
        if IS_CLIENT_WIN32:
            pass

    def get_all_state_desc(self):
        str_states = self._get_nulm_state_2_str(self.set_st)
        white_state = self._get_nulm_state_2_str(self._white_state)
        black_state = self._get_nulm_state_2_str(self._black_state)
        white_state_to_cover = {}
        for key, value in six.iteritems(self._white_state_to_cover):
            key_desc = self._get_nulm_state_2_str(key)
            white_state_to_cover[key_desc] = self._get_nulm_state_2_str(value)

        desc = 'test--all states = ' + str(str_states) + '--white_state =' + str(white_state) + '--black_state =' + str(black_state) + '--white_state_to_cover = ' + str(white_state_to_cover)
        return desc

    def destroy(self):
        super(ComStatus, self).destroy()
        self.status_config = None
        return

    def get_state(self, query_state):
        if self.set_st is None:
            return False
        else:
            return query_state in self.set_st

    def get_all_state(self):
        return self.set_st

    def _is_in_any_state(self, query_state):
        if isinstance(query_state, int):
            return query_state in self.set_st
        for one_state in query_state:
            if one_state in self.set_st:
                return True

        return False

    def resolve_empty_status(self):
        if self.set_st:
            return
        self.reset_state()
        self.send_event('E_CTRL_STAND', is_break_run=False, ignore_col=True)

    def reset_state(self, *args, **kwargs):
        pass

    def is_cover_state(self, cover_state, new_state):
        can_cover_states = self.mp_st_cover.get(new_state, set())
        return cover_state in can_cover_states