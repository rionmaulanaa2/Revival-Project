# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/jsonrpc/manager.py
import traceback
from .utils import is_invalid_params, DecodeList, DecodeDict
from .exceptions import JSONRPCInvalidParams, JSONRPCInvalidRequest, JSONRPCInvalidRequestException, JSONRPCMethodNotFound, JSONRPCServerError, JSONRPCDispatchException
from .jsonrpc import JSONRPC20BatchRequest, JSONRPC20BatchResponse, JSONRPC20Response
from .jsonrpc import JSONRPCRequest
from .... import PY2

class JSONRPCResponseManager(object):
    RESPONSE_CLASS_MAP = {'2.0': JSONRPC20Response
       }
    DISPATCH_ENCODING = None

    @classmethod
    def handle(cls, data, context, dispatcher):
        try:
            request = JSONRPCRequest.from_data(data)
        except JSONRPCInvalidRequestException:
            return JSONRPC20Response(error=JSONRPCInvalidRequest()._data)

        return cls.handle_request(request, context, dispatcher)

    @classmethod
    def handle_request(cls, request, context, dispatcher):
        if isinstance(request, JSONRPC20BatchRequest):
            rs = request if 1 else [
             request]
            responses = [ r for r in cls._get_responses(rs, context, dispatcher) if r is not None
                        ]
            return responses or None
        else:
            if isinstance(request, JSONRPC20BatchRequest):
                return JSONRPC20BatchResponse(*responses)
            return responses[0]
            return

    @classmethod
    def _get_responses(cls, requests, context, dispatcher):
        for request in requests:

            def response():
                return cls.RESPONSE_CLASS_MAP[request.JSONRPC_VERSION](_id=request._id, **kwargs)

            data = {'method': request.method,
               'request_args': request.args,
               'request_kwargs': request.kwargs
               }
            try:
                method = dispatcher[request.method]
            except KeyError:
                output = response(error=JSONRPCMethodNotFound(data=data)._data)
            else:
                args = request.args
                kwargs = request.kwargs
                if PY2 and cls.DISPATCH_ENCODING:
                    try:
                        args = DecodeList(args, cls.DISPATCH_ENCODING)
                        kwargs = DecodeDict(kwargs, cls.DISPATCH_ENCODING)
                    except:
                        traceback.print_exc()

                try:
                    result = method(context, *args, **kwargs)
                except JSONRPCDispatchException as e:
                    output = response(error=e.error._data)
                except Exception as e:
                    data.update({'type': e.__class__.__name__,
                       'args': e.args,
                       'message': str(e),
                       'traceback': traceback.format_exc()
                       })
                    if isinstance(e, TypeError) and is_invalid_params(method, *request.args, **request.kwargs):
                        output = response(error=JSONRPCInvalidParams(data=data)._data)
                    else:
                        print 'RPC Exception: {0}'.format(data)
                        traceback.print_exc()
                        output = response(error=JSONRPCServerError(data=data)._data)
                else:
                    output = response(result=result)

            if not request.is_notification:
                yield output