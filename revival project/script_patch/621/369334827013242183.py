# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/frame_data_utils.py


class FrameData(object):

    def __init__(self, get_data_func):
        self.get_data_func = get_data_func
        self.timestamp = 0
        self.data = None
        return

    def get_data(self):
        if self.timestamp == global_data.game_time:
            return self.data
        self.data = self.get_data_func()
        self.timestamp = global_data.game_time
        return self.data

    def destroy(self):
        self.get_data_func = None
        self.data = None
        return


def filter_duplicated_execution(func):

    def wrapper(self, *args, **kwargs):
        if self.sd.ref_frame_data_map is None:
            self.sd.ref_frame_data_map = {}
        func_name = func.__name__
        if func_name not in self.sd.ref_frame_data_map:
            self.sd.ref_frame_data_map[func_name] = [
             0, None]
        frame_data = self.sd.ref_frame_data_map[func_name]
        if frame_data[0] == global_data.game_time:
            return frame_data[1]
        else:
            ret = func(self, *args, **kwargs)
            frame_data[0] = global_data.game_time
            frame_data[1] = ret
            return ret

    return wrapper


def filter_duplicated_execution_with_arg_key(key_arg_count):
    if key_arg_count == 1:

        def method(func):

            def wrapper(self, *args, **kwargs):
                if self.sd.ref_frame_data_map is None:
                    self.sd.ref_frame_data_map = {}
                func_name = func.__name__
                if func_name not in self.sd.ref_frame_data_map:
                    self.sd.ref_frame_data_map[func_name] = {}
                key = args[0]
                if key not in self.sd.ref_frame_data_map[func_name]:
                    self.sd.ref_frame_data_map[func_name][key] = [
                     0, None]
                frame_data = self.sd.ref_frame_data_map[func_name][key]
                if frame_data[0] == global_data.game_time:
                    return frame_data[1]
                else:
                    ret = func(self, *args, **kwargs)
                    frame_data[0] = global_data.game_time
                    frame_data[1] = ret
                    return ret

            return wrapper

    else:

        def method(func):

            def wrapper(self, *args, **kwargs):
                if self.sd.ref_frame_data_map is None:
                    self.sd.ref_frame_data_map = {}
                func_name = func.__name__
                if func_name not in self.sd.ref_frame_data_map:
                    self.sd.ref_frame_data_map[func_name] = {}
                data_map = self.sd.ref_frame_data_map[func_name]
                for index in range(key_arg_count - 1):
                    key = args[index]
                    if key not in data_map:
                        data_map[key] = {}
                    data_map = data_map[key]

                if args[key_arg_count - 1] not in data_map:
                    data_map[args[key_arg_count - 1]] = [
                     0, None]
                frame_data = data_map[args[key_arg_count - 1]]
                if frame_data[0] == global_data.game_time:
                    return frame_data[1]
                else:
                    ret = func(self, *args, **kwargs)
                    frame_data[0] = global_data.game_time
                    frame_data[1] = ret
                    return ret

            return wrapper

    return method