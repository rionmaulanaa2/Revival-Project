# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPerfsys.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from .ScenePart import ScenePart
from common.utils import timer
import struct
import game3d
CMD_STRUCT = 0
CMD_RECORD = 1
CMD_KEY_NAMES = 2
CMD_MESSAGE = 3
INVALID_INDEX = -99

class Node(object):
    __slots__ = ('Name', 'Index', 'Children', 'TimeCost')

    def __init__(self, name, idx):
        self.Name = name
        self.Index = idx
        self.Children = {}
        self.TimeCost = 0

    def merge(self, other):
        self.TimeCost += other.TimeCost
        for name, child in six.iteritems(other.Children):
            if name in self.Children:
                self_child = self.Children[name]
                self_child.merge(child)
            else:
                child.invalid()
                self.Children[name] = child

    def invalid(self):
        self.Index = INVALID_INDEX
        for child in six.itervalues(self.Children):
            child.invalid()

    def update_value(self, record):
        if self.Index != INVALID_INDEX:
            self.TimeCost += record[self.Index]
            for child in six.itervalues(self.Children):
                child.update_value(record)

    def printf(self, names, total_time, file_obj, layer=0):
        percent = self.TimeCost / total_time * 100.0
        if percent < 0.1 and layer == 0:
            return
        else:
            line = '{}{}: {:.2f}%    [{:.2f}ms]'.format('\t' * layer, names[self.Name], percent, self.TimeCost)
            if file is None:
                print(line)
            else:
                file_obj.write(line + '\n')
            for child in six.itervalues(self.Children):
                child.printf(names, total_time, file_obj, layer + 1)

            return


class Parser(object):

    def __init__(self):
        self._current_stree = None
        self._merged_frames = None
        self._messages = []
        self._handlers = {CMD_STRUCT: self._read_struct,
           CMD_RECORD: self._read_record,
           CMD_KEY_NAMES: self._read_names,
           CMD_MESSAGE: self._read_message
           }
        return

    def read(self, file):
        self._current_stree = None
        self._merged_frames = None
        self._messages = []
        data = open(file, 'rb').read()
        data_len = len(data)
        ofs = 0
        while data_len > ofs:
            cmd = struct.unpack_from('!H', data, ofs)[0]
            ofs += 2
            ofs = self._handlers[cmd](data, ofs)

        return

    def _read_struct(self, data, ofs):
        count = struct.unpack_from('!I', data, ofs)[0]
        ofs += 4
        tree_vec = struct.unpack_from('!{}i'.format(count), data, ofs)
        ofs += count * 4
        self._build_tree(tree_vec)
        return ofs

    def _read_names(self, data, ofs):
        count = struct.unpack_from('!I', data, ofs)[0]
        ofs += 4
        names = []
        for i in range(count):
            strlen = struct.unpack_from('!I', data, ofs)[0]
            ofs += 4
            names.append(struct.unpack_from('!{}s'.format(strlen), data, ofs)[0])
            ofs += strlen

        self._names = names
        return ofs

    def _build_tree(self, structure):
        roots = {}
        nodes = []
        for i in range(0, len(structure), 2):
            nodes.append(Node(structure[i], i / 2))

        for i in range(0, len(structure), 2):
            item = nodes[i / 2]
            parent = structure[i + 1]
            if parent == -1:
                roots[item.Name] = item
            else:
                nodes[parent].Children[item.Name] = item

        if self._current_stree is None:
            self._current_stree = roots
        else:
            for key, tree in six.iteritems(self._current_stree):
                if key in roots:
                    roots[key].merge(tree)
                else:
                    tree.invalid()
                    roots[key] = tree

            self._current_stree = roots
        return

    def _read_record(self, data, ofs):
        count = struct.unpack_from('!I', data, ofs)[0]
        ofs += 4
        record = struct.unpack_from('!{}d'.format(count), data, ofs)
        ofs += count * 8
        self._create_frame(record)
        return ofs

    def _read_message(self, data, ofs):
        count = struct.unpack_from('!I', data, ofs)[0]
        ofs += 4
        msg = struct.unpack_from('!{}s'.format(count), data, ofs)[0]
        self._messages.append(msg)
        ofs += count
        return ofs

    def _create_frame(self, record):
        for root in six.itervalues(self._current_stree):
            root.update_value(record)

    def printf(self, file_path=None):
        total_time = 0
        file_obj = None
        if file_path is not None:
            file_obj = open(file_path, 'wb')
        self._print_message(file_obj)
        for root in six.itervalues(self._current_stree):
            total_time += root.TimeCost

        for root in six.itervalues(self._current_stree):
            root.printf(self._names, total_time, file_obj)

        if file_obj:
            file_obj.close()
        return

    def _print_message(self, file_obj):
        if not self._messages:
            return
        else:
            if file_obj is None:
                for msg in self._messages:
                    print(msg)

            else:
                file_obj.write('\n'.join(self._messages) + '\n')
            return


def _write_message(file, msg_str):
    file.write(struct.pack('!HI{}s'.format(len(msg_str)), CMD_MESSAGE, len(msg_str), msg_str))


def summary(path):
    p = Parser()
    p.read(path)
    summary_path = path.replace('.log', '.summary')
    p.printf(summary_path)


class PartPerfsys(ScenePart):

    def __init__(self, scene, name):
        super(PartPerfsys, self).__init__(scene, name, False)
        self._profile_start_time = 0
        self._profile_duration = 0
        self._start_timer = 0
        self._update_timer = 0
        self._log_file = None
        self._log_file_path = ''
        self._frame_count = 0
        self._auto_summary = False
        self._lag_only = False
        if global_data.perf_sys:
            self._profile_duration = global_data.perf_sys.profile_duration
            self._profile_start_time = global_data.perf_sys.profile_start_time
            self._auto_summary = global_data.perf_sys.gen_summay
            self._lag_only = global_data.perf_sys.lag_only
        return

    def on_enter(self):
        if self._profile_duration:
            t = global_data.game_mgr.get_logic_timer()
            self._start_timer = t.register(func=self._start, interval=self._profile_start_time, times=1, mode=timer.CLOCK)

    def _start(self):
        if self._log_file is None:
            from datetime import datetime
            import common
            import os.path
            now = datetime.now()
            log_file = os.path.join(common.utils.path.get_neox_dir(), 'perf_{}.log'.format(now.strftime('%Y_%m_%d_%H_%M_%S'))).replace('\\', '/')
            self._log_file_path = log_file
            try:
                self._log_file = open(log_file, 'wb')
            except:
                log_error("Can't write file {}".format(log_file))
                self._log_file = None
                return timer.RELEASE

        t = global_data.game_mgr.get_post_logic_timer()
        self._update_timer = t.register(func=self._update, interval=60, timedelta=True)
        self._total_time = 0
        self._frame_count = 0
        global_data.perf_sys.start()
        if self._lag_only:
            global_data.perf_sys.set_lag_report_func(self._upload_lag)
            global_data.perf_sys.enable_lag_record(log_file=False)
        else:
            global_data.perf_sys.enable_full_record()
            global_data.perf_sys.enable_lag_count_record(50)
        self._start_timer = 0
        return timer.RELEASE

    def _update(self, dt):
        self._total_time += dt
        last_struct_id = None
        p = global_data.perf_sys
        timer = p.get_timer()
        self._frame_count += len(timer)
        for record, struct_id in timer:
            if last_struct_id != struct_id:
                last_struct_id = struct_id
                tree_struct = p.get_timer_structure(struct_id)
                data_len = len(tree_struct)
                self._log_file.write(struct.pack('!HI{}i'.format(data_len), CMD_STRUCT, data_len, *tree_struct))
            data_len = len(record)
            self._log_file.write(struct.pack('!HI{}d'.format(data_len), CMD_RECORD, data_len, *record))

        if self._total_time >= self._profile_duration:
            self._stop()
        return

    def _stop(self):
        if self._log_file:
            if self._total_time > 0:
                import version
                import profiling
                names = profiling.get_timer_names()
                data_len = len(names)
                self._log_file.write(struct.pack('!HI', CMD_KEY_NAMES, data_len))
                for key_name in names:
                    self._log_file.write(struct.pack('!I{}s'.format(len(key_name)), len(key_name), key_name))

                _write_message(self._log_file, 'Average Frame Rate:{:.2f}'.format(self._frame_count / self._total_time))
                _write_message(self._log_file, 'Lag Times:{}'.format(global_data.perf_sys.lag_count))
                _write_message(self._log_file, 'Version:{}'.format(version.get_cur_version_str()))
                _write_message(self._log_file, 'Device:{}'.format(profiling.get_device_model()))
            self._log_file.close()
            self._log_file = None
        global_data.perf_sys.stop()
        if self._start_timer:
            global_data.game_mgr.get_logic_timer().unregister(self._start_timer)
            self._start_timer = 0
        if self._update_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self._update_timer)
            self._update_timer = 0
        if self._auto_summary:
            self.summary()
        return

    def summary(self, path=None):
        if path is None:
            path = self._log_file_path
        summary(path)
        return

    def on_exit(self):
        self._stop()

    def _upload_lag(self, msg):
        game3d.post_hunter_message('lag', msg)