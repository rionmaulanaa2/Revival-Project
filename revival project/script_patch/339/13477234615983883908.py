# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/proto_python/client_gate_pb2.py
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
DESCRIPTOR = _descriptor.FileDescriptor(name='client_gate.proto', package='mobile.server', serialized_pb=_b('\n\x11client_gate.proto\x12\rmobile.server\x1a\x0ccommon.proto"#\n\rEncryptString\x12\x12\n\nencryptstr\x18\x01 \x02(\x0c"\x1b\n\x0bSessionSeed\x12\x0c\n\x04seed\x18\x01 \x02(\x03"k\n\nSessionKey\x12\x1d\n\x15random_padding_header\x18\x01 \x02(\x0c\x12\x13\n\x0bsession_key\x18\x02 \x02(\x0c\x12\x0c\n\x04seed\x18\x03 \x02(\x03\x12\x1b\n\x13random_padding_tail\x18\x04 \x02(\x0c2\xb0\x04\n\x0cIGateService\x128\n\x0cseed_request\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12@\n\x0bsession_key\x12\x1c.mobile.server.EncryptString\x1a\x13.mobile.server.Void\x12J\n\x0econnect_server\x12#.mobile.server.ConnectServerRequest\x1a\x13.mobile.server.Void\x12C\n\x0eentity_message\x12\x1c.mobile.server.EntityMessage\x1a\x13.mobile.server.Void\x12A\n\x0csoul_message\x12\x1c.mobile.server.EntityMessage\x1a\x13.mobile.server.Void\x12?\n\rreg_md5_index\x12\x19.mobile.server.Md5OrIndex\x1a\x13.mobile.server.Void\x12J\n\x14forward_aoi_pos_info\x12\x1d.mobile.server.ForwardAoiInfo\x1a\x13.mobile.server.Void\x12C\n\x0ecustom_message\x12\x1c.mobile.server.CustomMessage\x1a\x13.mobile.server.Void2\xf8\x05\n\x0bIGateClient\x12=\n\nseed_reply\x12\x1a.mobile.server.SessionSeed\x1a\x13.mobile.server.Void\x12:\n\x0esession_key_ok\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12G\n\rconnect_reply\x12!.mobile.server.ConnectServerReply\x1a\x13.mobile.server.Void\x12?\n\rcreate_entity\x12\x19.mobile.server.EntityInfo\x1a\x13.mobile.server.Void\x12@\n\x0edestroy_entity\x12\x19.mobile.server.EntityInfo\x1a\x13.mobile.server.Void\x12C\n\x0eentity_message\x12\x1c.mobile.server.EntityMessage\x1a\x13.mobile.server.Void\x12A\n\x0echat_to_client\x12\x1a.mobile.server.OutBandInfo\x1a\x13.mobile.server.Void\x12?\n\rreg_md5_index\x12\x19.mobile.server.Md5OrIndex\x1a\x13.mobile.server.Void\x12L\n\x17dispatch_filter_message\x12\x1c.mobile.server.FilterMessage\x1a\x13.mobile.server.Void\x12F\n\x10forward_aoi_info\x12\x1d.mobile.server.ForwardAoiInfo\x1a\x13.mobile.server.Void\x12C\n\x0ecustom_message\x12\x1c.mobile.server.CustomMessage\x1a\x13.mobile.server.VoidB\x06\x80\x01\x01\x90\x01\x01'), dependencies=[
 common_pb2.DESCRIPTOR])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_ENCRYPTSTRING = _descriptor.Descriptor(name='EncryptString', full_name='mobile.server.EncryptString', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='encryptstr', full_name='mobile.server.EncryptString.encryptstr', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=50, serialized_end=85)
_SESSIONSEED = _descriptor.Descriptor(name='SessionSeed', full_name='mobile.server.SessionSeed', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='seed', full_name='mobile.server.SessionSeed.seed', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=87, serialized_end=114)
_SESSIONKEY = _descriptor.Descriptor(name='SessionKey', full_name='mobile.server.SessionKey', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='random_padding_header', full_name='mobile.server.SessionKey.random_padding_header', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='session_key', full_name='mobile.server.SessionKey.session_key', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='seed', full_name='mobile.server.SessionKey.seed', index=2, number=3, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='random_padding_tail', full_name='mobile.server.SessionKey.random_padding_tail', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=116, serialized_end=223)
DESCRIPTOR.message_types_by_name['EncryptString'] = _ENCRYPTSTRING
DESCRIPTOR.message_types_by_name['SessionSeed'] = _SESSIONSEED
DESCRIPTOR.message_types_by_name['SessionKey'] = _SESSIONKEY
EncryptString = _reflection.GeneratedProtocolMessageType('EncryptString', (_message.Message,), dict(DESCRIPTOR=_ENCRYPTSTRING, __module__='client_gate_pb2'))
_sym_db.RegisterMessage(EncryptString)
SessionSeed = _reflection.GeneratedProtocolMessageType('SessionSeed', (_message.Message,), dict(DESCRIPTOR=_SESSIONSEED, __module__='client_gate_pb2'))
_sym_db.RegisterMessage(SessionSeed)
SessionKey = _reflection.GeneratedProtocolMessageType('SessionKey', (_message.Message,), dict(DESCRIPTOR=_SESSIONKEY, __module__='client_gate_pb2'))
_sym_db.RegisterMessage(SessionKey)
DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\x80\x01\x01\x90\x01\x01'))
_IGATESERVICE = _descriptor.ServiceDescriptor(name='IGateService', full_name='mobile.server.IGateService', file=DESCRIPTOR, index=0, options=None, serialized_start=226, serialized_end=786, methods=[
 _descriptor.MethodDescriptor(name='seed_request', full_name='mobile.server.IGateService.seed_request', index=0, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='session_key', full_name='mobile.server.IGateService.session_key', index=1, containing_service=None, input_type=_ENCRYPTSTRING, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='connect_server', full_name='mobile.server.IGateService.connect_server', index=2, containing_service=None, input_type=common_pb2._CONNECTSERVERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='entity_message', full_name='mobile.server.IGateService.entity_message', index=3, containing_service=None, input_type=common_pb2._ENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='soul_message', full_name='mobile.server.IGateService.soul_message', index=4, containing_service=None, input_type=common_pb2._ENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reg_md5_index', full_name='mobile.server.IGateService.reg_md5_index', index=5, containing_service=None, input_type=common_pb2._MD5ORINDEX, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='forward_aoi_pos_info', full_name='mobile.server.IGateService.forward_aoi_pos_info', index=6, containing_service=None, input_type=common_pb2._FORWARDAOIINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='custom_message', full_name='mobile.server.IGateService.custom_message', index=7, containing_service=None, input_type=common_pb2._CUSTOMMESSAGE, output_type=common_pb2._VOID, options=None)])
IGateService = service_reflection.GeneratedServiceType('IGateService', (_service.Service,), dict(DESCRIPTOR=_IGATESERVICE, __module__='client_gate_pb2'))
IGateService_Stub = service_reflection.GeneratedServiceStubType('IGateService_Stub', (IGateService,), dict(DESCRIPTOR=_IGATESERVICE, __module__='client_gate_pb2'))
_IGATECLIENT = _descriptor.ServiceDescriptor(name='IGateClient', full_name='mobile.server.IGateClient', file=DESCRIPTOR, index=1, options=None, serialized_start=789, serialized_end=1549, methods=[
 _descriptor.MethodDescriptor(name='seed_reply', full_name='mobile.server.IGateClient.seed_reply', index=0, containing_service=None, input_type=_SESSIONSEED, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='session_key_ok', full_name='mobile.server.IGateClient.session_key_ok', index=1, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='connect_reply', full_name='mobile.server.IGateClient.connect_reply', index=2, containing_service=None, input_type=common_pb2._CONNECTSERVERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='create_entity', full_name='mobile.server.IGateClient.create_entity', index=3, containing_service=None, input_type=common_pb2._ENTITYINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='destroy_entity', full_name='mobile.server.IGateClient.destroy_entity', index=4, containing_service=None, input_type=common_pb2._ENTITYINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='entity_message', full_name='mobile.server.IGateClient.entity_message', index=5, containing_service=None, input_type=common_pb2._ENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='chat_to_client', full_name='mobile.server.IGateClient.chat_to_client', index=6, containing_service=None, input_type=common_pb2._OUTBANDINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reg_md5_index', full_name='mobile.server.IGateClient.reg_md5_index', index=7, containing_service=None, input_type=common_pb2._MD5ORINDEX, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='dispatch_filter_message', full_name='mobile.server.IGateClient.dispatch_filter_message', index=8, containing_service=None, input_type=common_pb2._FILTERMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='forward_aoi_info', full_name='mobile.server.IGateClient.forward_aoi_info', index=9, containing_service=None, input_type=common_pb2._FORWARDAOIINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='custom_message', full_name='mobile.server.IGateClient.custom_message', index=10, containing_service=None, input_type=common_pb2._CUSTOMMESSAGE, output_type=common_pb2._VOID, options=None)])
IGateClient = service_reflection.GeneratedServiceType('IGateClient', (_service.Service,), dict(DESCRIPTOR=_IGATECLIENT, __module__='client_gate_pb2'))
IGateClient_Stub = service_reflection.GeneratedServiceStubType('IGateClient_Stub', (IGateClient,), dict(DESCRIPTOR=_IGATECLIENT, __module__='client_gate_pb2'))