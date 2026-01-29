# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/proto_python/monitor_server_pb2.py
from __future__ import absolute_import
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
from . import common_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='monitor_server.proto', package='mobile.server', serialized_pb=_b('\n\x14monitor_server.proto\x12\rmobile.server\x1a\x0ccommon.proto"(\n\nMonitorSet\x12\x0b\n\x03key\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x02(\t"\x19\n\nMonitorGet\x12\x0b\n\x03key\x18\x01 \x03(\t"\x1d\n\x0cMonitorReply\x12\r\n\x05reply\x18\x01 \x02(\t2\xc9\x01\n\x0fIMonitorService\x128\n\x0cmonitor_info\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12=\n\x0bmonitor_get\x12\x19.mobile.server.MonitorGet\x1a\x13.mobile.server.Void\x12=\n\x0bmonitor_set\x12\x19.mobile.server.MonitorSet\x1a\x13.mobile.server.Void2\xe6\x01\n\x0eIMonitorClient\x12F\n\x12monitor_info_reply\x12\x1b.mobile.server.MonitorReply\x1a\x13.mobile.server.Void\x12E\n\x11monitor_get_reply\x12\x1b.mobile.server.MonitorReply\x1a\x13.mobile.server.Void\x12E\n\x11monitor_set_reply\x12\x1b.mobile.server.MonitorReply\x1a\x13.mobile.server.VoidB\x03\x90\x01\x01'), dependencies=[
 common_pb2.DESCRIPTOR])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_MONITORSET = _descriptor.Descriptor(name='MonitorSet', full_name='mobile.server.MonitorSet', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='mobile.server.MonitorSet.key', index=0, number=1, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='value', full_name='mobile.server.MonitorSet.value', index=1, number=2, type=9, cpp_type=9, label=2, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=53, serialized_end=93)
_MONITORGET = _descriptor.Descriptor(name='MonitorGet', full_name='mobile.server.MonitorGet', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='mobile.server.MonitorGet.key', index=0, number=1, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=95, serialized_end=120)
_MONITORREPLY = _descriptor.Descriptor(name='MonitorReply', full_name='mobile.server.MonitorReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='reply', full_name='mobile.server.MonitorReply.reply', index=0, number=1, type=9, cpp_type=9, label=2, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=122, serialized_end=151)
DESCRIPTOR.message_types_by_name['MonitorSet'] = _MONITORSET
DESCRIPTOR.message_types_by_name['MonitorGet'] = _MONITORGET
DESCRIPTOR.message_types_by_name['MonitorReply'] = _MONITORREPLY
MonitorSet = _reflection.GeneratedProtocolMessageType('MonitorSet', (_message.Message,), dict(DESCRIPTOR=_MONITORSET, __module__='monitor_server_pb2'))
_sym_db.RegisterMessage(MonitorSet)
MonitorGet = _reflection.GeneratedProtocolMessageType('MonitorGet', (_message.Message,), dict(DESCRIPTOR=_MONITORGET, __module__='monitor_server_pb2'))
_sym_db.RegisterMessage(MonitorGet)
MonitorReply = _reflection.GeneratedProtocolMessageType('MonitorReply', (_message.Message,), dict(DESCRIPTOR=_MONITORREPLY, __module__='monitor_server_pb2'))
_sym_db.RegisterMessage(MonitorReply)
DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\x90\x01\x01'))
_IMONITORSERVICE = _descriptor.ServiceDescriptor(name='IMonitorService', full_name='mobile.server.IMonitorService', file=DESCRIPTOR, index=0, options=None, serialized_start=154, serialized_end=355, methods=[
 _descriptor.MethodDescriptor(name='monitor_info', full_name='mobile.server.IMonitorService.monitor_info', index=0, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='monitor_get', full_name='mobile.server.IMonitorService.monitor_get', index=1, containing_service=None, input_type=_MONITORGET, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='monitor_set', full_name='mobile.server.IMonitorService.monitor_set', index=2, containing_service=None, input_type=_MONITORSET, output_type=common_pb2._VOID, options=None)])
IMonitorService = service_reflection.GeneratedServiceType('IMonitorService', (_service.Service,), dict(DESCRIPTOR=_IMONITORSERVICE, __module__='monitor_server_pb2'))
IMonitorService_Stub = service_reflection.GeneratedServiceStubType('IMonitorService_Stub', (IMonitorService,), dict(DESCRIPTOR=_IMONITORSERVICE, __module__='monitor_server_pb2'))
_IMONITORCLIENT = _descriptor.ServiceDescriptor(name='IMonitorClient', full_name='mobile.server.IMonitorClient', file=DESCRIPTOR, index=1, options=None, serialized_start=358, serialized_end=588, methods=[
 _descriptor.MethodDescriptor(name='monitor_info_reply', full_name='mobile.server.IMonitorClient.monitor_info_reply', index=0, containing_service=None, input_type=_MONITORREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='monitor_get_reply', full_name='mobile.server.IMonitorClient.monitor_get_reply', index=1, containing_service=None, input_type=_MONITORREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='monitor_set_reply', full_name='mobile.server.IMonitorClient.monitor_set_reply', index=2, containing_service=None, input_type=_MONITORREPLY, output_type=common_pb2._VOID, options=None)])
IMonitorClient = service_reflection.GeneratedServiceType('IMonitorClient', (_service.Service,), dict(DESCRIPTOR=_IMONITORCLIENT, __module__='monitor_server_pb2'))
IMonitorClient_Stub = service_reflection.GeneratedServiceStubType('IMonitorClient_Stub', (IMonitorClient,), dict(DESCRIPTOR=_IMONITORCLIENT, __module__='monitor_server_pb2'))