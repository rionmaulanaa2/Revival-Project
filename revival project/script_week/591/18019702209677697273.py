# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/predownload/uni_extend.py
import game3d

class ChannelWrapper(object):

    def __init__(self):
        import social
        self._channel = social.get_channel()
        self._channel_delegate = None
        self._channel.extend_callback = self.__local_extend_callback
        self._callbacks = {}
        return

    def __local_extend_callback(self, json_str):
        import json
        json_dict = json.loads(json_str)
        mid = json_dict['methodId']
        callbacks = self._callbacks.pop(mid, {})
        if callbacks:
            for callback in callbacks.values():
                callback(json_dict)

    def extend_func(self, source, method, callback):
        import json
        ex_params = method
        if self._channel_delegate:
            self._channel_delegate.temp_extend_callback_function(source, ex_params['methodId'], callback)
            self._channel_delegate.extend_func_by_dict(ex_params)
        else:
            self._callbacks.setdefault(ex_params['methodId'], {})
            self._callbacks[ex_params['methodId']][source] = callback
            self._channel.extend_func(json.dumps(ex_params))

    def set_channel_delegate(self, channel):
        self._channel_delegate = channel
        if not channel:
            self._channel.extend_callback = self.__local_extend_callback

    @property
    def name(self):
        if self._channel_delegate:
            return self._channel_delegate.get_name()
        else:
            return self._channel.name


channel_wrapper = ChannelWrapper()

class ExFuncException(Exception):

    def __init__(self, json_dict):
        self.data = json_dict

    def __str__(self):
        return 'ExFuncException: {}'.format(self.data)


class ExFuncCallerInter(object):
    default_exception_handler = None

    def __init__(self, _callable):
        self._next_callable = None
        self._failed_callable = None
        self._type = None
        self._callable = _callable
        self._is_ex_call = False
        self._no_ex_except = False
        return

    def ex_call(self, params):
        self._next_callable = ExFuncCallerInter(params)
        self._next_callable._is_ex_call = True
        return self._next_callable

    def then(self, callback):
        self._next_callable = ExFuncCallerInter(callback)
        return self._next_callable

    def ex_call_noexcept(self, params):
        self._next_callable = ExFuncCallerInter(params)
        self._next_callable._no_ex_except = True
        self._next_callable._is_ex_call = True
        return self._next_callable

    def exception(self, callback):
        self._failed_callable = callback
        return self

    def _do_call(self, callback_args=None):
        if self._is_ex_call and self._callable:
            self._ex_call(self._callable())
        else:
            try:
                if self._callable:
                    self._callable(callback_args)
                if self._next_callable:
                    self._next_callable._do_call(callback_args)
            except Exception as e:
                if self._failed_callable:
                    self._failed_callable(e)
                elif self.default_exception_handler:
                    self.default_exception_handler(e)
                else:
                    raise e

    def _ex_call(self, method):
        ex_params = method
        if isinstance(method, str):
            ex_params = {'channel': 'store_pre_download','methodId': method
               }
        if ex_params:
            channel_wrapper.extend_func(self, ex_params, self._ex_callback)
        else:
            self._ex_callback({})

    def _ex_callback(self, json_dict):
        is_ok = json_dict.get('respCode', 0) == 0 and json_dict.get('errorCode', 0) == 0
        if not is_ok and not self._no_ex_except:
            print '[store_pre_download] {} failed: {}'.format(self._callable, json_dict)
            e = ExFuncException(json_dict)
            if self._failed_callable:
                self._failed_callable(e)
            elif self.default_exception_handler:
                self.default_exception_handler(e)
            else:
                raise e
        elif self._next_callable:
            self._next_callable._do_call(json_dict)


class ExFuncCaller(ExFuncCallerInter):

    def __init__(self):
        super(ExFuncCaller, self).__init__(None)
        game3d.delay_exec(30, self._do_call)
        return