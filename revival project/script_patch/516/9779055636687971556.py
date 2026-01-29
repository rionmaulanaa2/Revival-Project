# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/proto_python/common_pb2.py
from __future__ import absolute_import
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='common.proto', package='mobile.server', serialized_pb=_b('\n\x0ccommon.proto\x12\rmobile.server"\x06\n\x04Void"\xfa\x01\n\x14ConnectServerRequest\x12\x0e\n\x06routes\x18\x01 \x01(\x0c\x12=\n\x04type\x18\x02 \x02(\x0e2/.mobile.server.ConnectServerRequest.RequestType\x12\x10\n\x08deviceid\x18\x03 \x01(\x0c\x12\x10\n\x08entityid\x18\x04 \x01(\x0c\x12\x0f\n\x07authmsg\x18\x05 \x01(\x0c\x12\x17\n\x0fcompressor_type\x18\x06 \x01(\x0c"E\n\x0bRequestType\x12\x12\n\x0eNEW_CONNECTION\x10\x00\x12\x11\n\rRE_CONNECTION\x10\x01\x12\x0f\n\x0bBIND_AVATAR\x10\x02"\x81\x02\n\x12ConnectServerReply\x12\x0e\n\x06routes\x18\x01 \x01(\x0c\x12?\n\x04type\x18\x02 \x02(\x0e2+.mobile.server.ConnectServerReply.ReplyType:\x04BUSY\x12\x10\n\x08entityid\x18\x03 \x01(\x0c\x12\x10\n\x08extramsg\x18\x04 \x01(\x0c"v\n\tReplyType\x12\x08\n\x04BUSY\x10\x00\x12\r\n\tCONNECTED\x10\x01\x12\x17\n\x13RECONNECT_SUCCEEDED\x10\x02\x12\x14\n\x10RECONNECT_FAILED\x10\x03\x12\r\n\tFORBIDDEN\x10\x04\x12\x12\n\x0eMAX_CONNECTION\x10\x05",\n\nMd5OrIndex\x12\x0b\n\x03md5\x18\x01 \x01(\x0c\x12\x11\n\x05index\x18\x02 \x01(\x11:\x02-1".\n\tFilterObj\x12\x0e\n\x06strexp\x18\x01 \x02(\x0c\x12\x11\n\x05index\x18\x02 \x01(\x05:\x02-1"\xb1\x01\n\nFilterRule\x120\n\x04type\x18\x01 \x01(\x0e2".mobile.server.FilterRule.RuleType\x12(\n\x06filter\x18\x02 \x01(\x0b2\x18.mobile.server.FilterObj\x12\x0e\n\x06idlist\x18\x03 \x03(\x0c"7\n\x08RuleType\x12\x0e\n\nBROAD_CAST\x10\x00\x12\x0e\n\nFILTER_EXP\x10\x01\x12\x0b\n\x07ID_LIST\x10\x02"^\n\rFilterMessage\x12\x0c\n\x04rule\x18\x01 \x01(\x0c\x12)\n\x06method\x18\x02 \x02(\x0b2\x19.mobile.server.Md5OrIndex\x12\x14\n\nparameters\x18\x03 \x01(\x0c:\x00"\x99\x01\n\rEntityMessage\x12\x0e\n\x06routes\x18\x01 \x01(\x0c\x12\x0c\n\x02id\x18\x02 \x01(\x0c:\x00\x12)\n\x06method\x18\x03 \x02(\x0b2\x19.mobile.server.Md5OrIndex\x12\x12\n\nparameters\x18\x04 \x01(\x0c\x12\x16\n\x08reliable\x18\x05 \x01(\x08:\x04true\x12\x13\n\x07localid\x18\x06 \x01(\x05:\x02-1"\x8f\x02\n\tRouteData\x129\n\x04type\x18\x01 \x01(\x0e2".mobile.server.RouteData.RouteType:\x07Default\x12\x0f\n\x05strid\x18\x02 \x01(\x0c:\x00\x12\x11\n\x05intid\x18\x03 \x01(\x05:\x02-1"\xa2\x01\n\tRouteType\x12\x0b\n\x07Default\x10\x00\x12\x11\n\rClient2Server\x10\x01\x12\x11\n\rServer2Client\x10\x02\x12\x12\n\x0eServer2Sserver\x10\x03\x12\x12\n\x0eClient2Service\x10\x04\x12\x12\n\x0eService2Client\x10\x05\x12\x12\n\x0eServer2Service\x10\x06\x12\x12\n\x0eService2Server\x10\x07"E\n\rCustomMessage\x12\'\n\x05route\x18\x01 \x01(\x0b2\x18.mobile.server.RouteData\x12\x0b\n\x03msg\x18\x02 \x01(\x0c"G\n\tServiceId\x12\x14\n\x0cservice_type\x18\x01 \x02(\x0c\x12\x18\n\rservice_subid\x18\x02 \x01(\x05:\x010\x12\n\n\x02id\x18\x03 \x01(\x0c"\x85\x01\n\x0eServiceMessage\x120\n\nentity_msg\x18\x01 \x02(\x0b2\x1c.mobile.server.EntityMessage\x12,\n\nservice_id\x18\x02 \x01(\x0b2\x18.mobile.server.ServiceId\x12\x13\n\x08hash_key\x18\x03 \x01(\x05:\x010"|\n\x13GlobalEntityMessage\x12\x0e\n\x06target\x18\x01 \x01(\x0c\x12)\n\x06method\x18\x02 \x02(\x0b2\x19.mobile.server.Md5OrIndex\x12\x12\n\nparameters\x18\x03 \x01(\x0c\x12\x16\n\x08reliable\x18\x04 \x01(\x08:\x04true"_\n\nEntityInfo\x12\x0e\n\x06routes\x18\x01 \x01(\x0c\x12\'\n\x04type\x18\x02 \x01(\x0b2\x19.mobile.server.Md5OrIndex\x12\n\n\x02id\x18\x03 \x01(\x0c\x12\x0c\n\x04info\x18\x04 \x01(\x0c"\x83\x02\n\x0bServiceInfo\x12.\n\x0bentity_info\x18\x01 \x02(\x0b2\x19.mobile.server.EntityInfo\x12,\n\nservice_id\x18\x02 \x02(\x0b2\x18.mobile.server.ServiceId\x12\x17\n\x0cforward_type\x18\x03 \x01(\x05:\x012\x12\x16\n\x0blayout_type\x18\x04 \x01(\x05:\x010"9\n\x0bForwardType\x12\x07\n\x03Any\x10\x00\x12\t\n\x05Every\x10\x01\x12\x08\n\x04Hash\x10\x02\x12\x0c\n\x08HashRing\x10\x03"*\n\nLayoutType\x12\x0c\n\x08AnyWhere\x10\x00\x12\x0e\n\nEveryWhere\x10\x01".\n\x0bOutBandInfo\x12\x0e\n\x06routes\x18\x01 \x01(\x0c\x12\x0f\n\x07message\x18\x02 \x02(\x0c"\xf8\x01\n\nServerInfo\x12\n\n\x02ip\x18\x01 \x02(\x0c\x12\x0c\n\x04port\x18\x02 \x02(\x05\x12\x0b\n\x03sid\x18\x03 \x01(\x05\x12\x11\n\tbanclient\x18\x04 \x01(\x08\x12\x0f\n\x07svrtype\x18\x05 \x01(\x05\x12\x12\n\nservername\x18\x06 \x01(\x0c\x12\x0b\n\x03dip\x18\x07 \x01(\x0c\x12\r\n\x05dport\x18\x08 \x01(\x05"o\n\x07SvrType\x12\x08\n\x04GAME\x10\x01\x12\n\n\x06BATTLE\x10\x02\x12\x11\n\rDIRECT_BATTLE\x10\x03\x12\t\n\x05MATCH\x10\x04\x12\x07\n\x03WEB\x10\x05\x12\x08\n\x04CHAT\x10\x06\x12\x0c\n\x08SPECTATE\x10\x07\x12\x0f\n\x0bBATTLE_TOOL\x10\x08"P\n\rEntityMailbox\x12\x10\n\x08entityid\x18\x01 \x02(\x0c\x12-\n\nserverinfo\x18\x02 \x01(\x0b2\x19.mobile.server.ServerInfo"n\n\x0eServiceMailbox\x12.\n\x08entitymb\x18\x01 \x02(\x0b2\x1c.mobile.server.EntityMailbox\x12,\n\nservice_id\x18\x02 \x02(\x0b2\x18.mobile.server.ServiceId":\n\x0eForwardAoiInfo\x12\x0e\n\x06routes\x18\x01 \x01(\x0c\x12\n\n\x02id\x18\x02 \x01(\x0c\x12\x0c\n\x04info\x18\x03 \x01(\x0c"t\n\x0bGameMessage\x12-\n\nserverinfo\x18\x01 \x01(\x0b2\x19.mobile.server.ServerInfo\x12\x0e\n\x06routes\x18\x02 \x01(\x0c\x12\x12\n\nmethodname\x18\x03 \x02(\x0c\x12\x12\n\nparameters\x18\x04 \x01(\x0cB\x06\x80\x01\x01\x90\x01\x01'))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_CONNECTSERVERREQUEST_REQUESTTYPE = _descriptor.EnumDescriptor(name='RequestType', full_name='mobile.server.ConnectServerRequest.RequestType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='NEW_CONNECTION', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='RE_CONNECTION', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BIND_AVATAR', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=221, serialized_end=290)
_sym_db.RegisterEnumDescriptor(_CONNECTSERVERREQUEST_REQUESTTYPE)
_CONNECTSERVERREPLY_REPLYTYPE = _descriptor.EnumDescriptor(name='ReplyType', full_name='mobile.server.ConnectServerReply.ReplyType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='BUSY', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CONNECTED', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='RECONNECT_SUCCEEDED', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='RECONNECT_FAILED', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FORBIDDEN', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MAX_CONNECTION', index=5, number=5, options=None, type=None)], containing_type=None, options=None, serialized_start=432, serialized_end=550)
_sym_db.RegisterEnumDescriptor(_CONNECTSERVERREPLY_REPLYTYPE)
_FILTERRULE_RULETYPE = _descriptor.EnumDescriptor(name='RuleType', full_name='mobile.server.FilterRule.RuleType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='BROAD_CAST', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FILTER_EXP', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='ID_LIST', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=769, serialized_end=824)
_sym_db.RegisterEnumDescriptor(_FILTERRULE_RULETYPE)
_ROUTEDATA_ROUTETYPE = _descriptor.EnumDescriptor(name='RouteType', full_name='mobile.server.RouteData.RouteType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='Default', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Client2Server', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Server2Client', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Server2Sserver', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Client2Service', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Service2Client', index=5, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Server2Service', index=6, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Service2Server', index=7, number=7, options=None, type=None)], containing_type=None, options=None, serialized_start=1188, serialized_end=1350)
_sym_db.RegisterEnumDescriptor(_ROUTEDATA_ROUTETYPE)
_SERVICEINFO_FORWARDTYPE = _descriptor.EnumDescriptor(name='ForwardType', full_name='mobile.server.ServiceInfo.ForwardType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='Any', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Every', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='Hash', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='HashRing', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=2014, serialized_end=2071)
_sym_db.RegisterEnumDescriptor(_SERVICEINFO_FORWARDTYPE)
_SERVICEINFO_LAYOUTTYPE = _descriptor.EnumDescriptor(name='LayoutType', full_name='mobile.server.ServiceInfo.LayoutType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='AnyWhere', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='EveryWhere', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=2073, serialized_end=2115)
_sym_db.RegisterEnumDescriptor(_SERVICEINFO_LAYOUTTYPE)
_SERVERINFO_SVRTYPE = _descriptor.EnumDescriptor(name='SvrType', full_name='mobile.server.ServerInfo.SvrType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='GAME', index=0, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BATTLE', index=1, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DIRECT_BATTLE', index=2, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MATCH', index=3, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='WEB', index=4, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CHAT', index=5, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SPECTATE', index=6, number=7, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BATTLE_TOOL', index=7, number=8, options=None, type=None)], containing_type=None, options=None, serialized_start=2303, serialized_end=2414)
_sym_db.RegisterEnumDescriptor(_SERVERINFO_SVRTYPE)
_VOID = _descriptor.Descriptor(name='Void', full_name='mobile.server.Void', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=31, serialized_end=37)
_CONNECTSERVERREQUEST = _descriptor.Descriptor(name='ConnectServerRequest', full_name='mobile.server.ConnectServerRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.ConnectServerRequest.routes', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='type', full_name='mobile.server.ConnectServerRequest.type', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='deviceid', full_name='mobile.server.ConnectServerRequest.deviceid', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='entityid', full_name='mobile.server.ConnectServerRequest.entityid', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='authmsg', full_name='mobile.server.ConnectServerRequest.authmsg', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='compressor_type', full_name='mobile.server.ConnectServerRequest.compressor_type', index=5, number=6, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _CONNECTSERVERREQUEST_REQUESTTYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=40, serialized_end=290)
_CONNECTSERVERREPLY = _descriptor.Descriptor(name='ConnectServerReply', full_name='mobile.server.ConnectServerReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.ConnectServerReply.routes', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='type', full_name='mobile.server.ConnectServerReply.type', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='entityid', full_name='mobile.server.ConnectServerReply.entityid', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='extramsg', full_name='mobile.server.ConnectServerReply.extramsg', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _CONNECTSERVERREPLY_REPLYTYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=293, serialized_end=550)
_MD5ORINDEX = _descriptor.Descriptor(name='Md5OrIndex', full_name='mobile.server.Md5OrIndex', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='md5', full_name='mobile.server.Md5OrIndex.md5', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='index', full_name='mobile.server.Md5OrIndex.index', index=1, number=2, type=17, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=552, serialized_end=596)
_FILTEROBJ = _descriptor.Descriptor(name='FilterObj', full_name='mobile.server.FilterObj', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='strexp', full_name='mobile.server.FilterObj.strexp', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='index', full_name='mobile.server.FilterObj.index', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=598, serialized_end=644)
_FILTERRULE = _descriptor.Descriptor(name='FilterRule', full_name='mobile.server.FilterRule', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='type', full_name='mobile.server.FilterRule.type', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='filter', full_name='mobile.server.FilterRule.filter', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='idlist', full_name='mobile.server.FilterRule.idlist', index=2, number=3, type=12, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _FILTERRULE_RULETYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=647, serialized_end=824)
_FILTERMESSAGE = _descriptor.Descriptor(name='FilterMessage', full_name='mobile.server.FilterMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='rule', full_name='mobile.server.FilterMessage.rule', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='method', full_name='mobile.server.FilterMessage.method', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='parameters', full_name='mobile.server.FilterMessage.parameters', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=True, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=826, serialized_end=920)
_ENTITYMESSAGE = _descriptor.Descriptor(name='EntityMessage', full_name='mobile.server.EntityMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.EntityMessage.routes', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='id', full_name='mobile.server.EntityMessage.id', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=True, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='method', full_name='mobile.server.EntityMessage.method', index=2, number=3, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='parameters', full_name='mobile.server.EntityMessage.parameters', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='reliable', full_name='mobile.server.EntityMessage.reliable', index=4, number=5, type=8, cpp_type=7, label=1, has_default_value=True, default_value=True, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='localid', full_name='mobile.server.EntityMessage.localid', index=5, number=6, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=923, serialized_end=1076)
_ROUTEDATA = _descriptor.Descriptor(name='RouteData', full_name='mobile.server.RouteData', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='type', full_name='mobile.server.RouteData.type', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='strid', full_name='mobile.server.RouteData.strid', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=True, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='intid', full_name='mobile.server.RouteData.intid', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _ROUTEDATA_ROUTETYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1079, serialized_end=1350)
_CUSTOMMESSAGE = _descriptor.Descriptor(name='CustomMessage', full_name='mobile.server.CustomMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='route', full_name='mobile.server.CustomMessage.route', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='mobile.server.CustomMessage.msg', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1352, serialized_end=1421)
_SERVICEID = _descriptor.Descriptor(name='ServiceId', full_name='mobile.server.ServiceId', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='service_type', full_name='mobile.server.ServiceId.service_type', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='service_subid', full_name='mobile.server.ServiceId.service_subid', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='id', full_name='mobile.server.ServiceId.id', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1423, serialized_end=1494)
_SERVICEMESSAGE = _descriptor.Descriptor(name='ServiceMessage', full_name='mobile.server.ServiceMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='entity_msg', full_name='mobile.server.ServiceMessage.entity_msg', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='service_id', full_name='mobile.server.ServiceMessage.service_id', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='hash_key', full_name='mobile.server.ServiceMessage.hash_key', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1497, serialized_end=1630)
_GLOBALENTITYMESSAGE = _descriptor.Descriptor(name='GlobalEntityMessage', full_name='mobile.server.GlobalEntityMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='target', full_name='mobile.server.GlobalEntityMessage.target', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='method', full_name='mobile.server.GlobalEntityMessage.method', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='parameters', full_name='mobile.server.GlobalEntityMessage.parameters', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='reliable', full_name='mobile.server.GlobalEntityMessage.reliable', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=True, default_value=True, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1632, serialized_end=1756)
_ENTITYINFO = _descriptor.Descriptor(name='EntityInfo', full_name='mobile.server.EntityInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.EntityInfo.routes', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='type', full_name='mobile.server.EntityInfo.type', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='id', full_name='mobile.server.EntityInfo.id', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='info', full_name='mobile.server.EntityInfo.info', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1758, serialized_end=1853)
_SERVICEINFO = _descriptor.Descriptor(name='ServiceInfo', full_name='mobile.server.ServiceInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='entity_info', full_name='mobile.server.ServiceInfo.entity_info', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='service_id', full_name='mobile.server.ServiceInfo.service_id', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='forward_type', full_name='mobile.server.ServiceInfo.forward_type', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=True, default_value=2, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='layout_type', full_name='mobile.server.ServiceInfo.layout_type', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _SERVICEINFO_FORWARDTYPE,
 _SERVICEINFO_LAYOUTTYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1856, serialized_end=2115)
_OUTBANDINFO = _descriptor.Descriptor(name='OutBandInfo', full_name='mobile.server.OutBandInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.OutBandInfo.routes', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='message', full_name='mobile.server.OutBandInfo.message', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=2117, serialized_end=2163)
_SERVERINFO = _descriptor.Descriptor(name='ServerInfo', full_name='mobile.server.ServerInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='ip', full_name='mobile.server.ServerInfo.ip', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='port', full_name='mobile.server.ServerInfo.port', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sid', full_name='mobile.server.ServerInfo.sid', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='banclient', full_name='mobile.server.ServerInfo.banclient', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='svrtype', full_name='mobile.server.ServerInfo.svrtype', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='servername', full_name='mobile.server.ServerInfo.servername', index=5, number=6, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dip', full_name='mobile.server.ServerInfo.dip', index=6, number=7, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dport', full_name='mobile.server.ServerInfo.dport', index=7, number=8, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _SERVERINFO_SVRTYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=2166, serialized_end=2414)
_ENTITYMAILBOX = _descriptor.Descriptor(name='EntityMailbox', full_name='mobile.server.EntityMailbox', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='entityid', full_name='mobile.server.EntityMailbox.entityid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='serverinfo', full_name='mobile.server.EntityMailbox.serverinfo', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=2416, serialized_end=2496)
_SERVICEMAILBOX = _descriptor.Descriptor(name='ServiceMailbox', full_name='mobile.server.ServiceMailbox', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='entitymb', full_name='mobile.server.ServiceMailbox.entitymb', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='service_id', full_name='mobile.server.ServiceMailbox.service_id', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=2498, serialized_end=2608)
_FORWARDAOIINFO = _descriptor.Descriptor(name='ForwardAoiInfo', full_name='mobile.server.ForwardAoiInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.ForwardAoiInfo.routes', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='id', full_name='mobile.server.ForwardAoiInfo.id', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='info', full_name='mobile.server.ForwardAoiInfo.info', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=2610, serialized_end=2668)
_GAMEMESSAGE = _descriptor.Descriptor(name='GameMessage', full_name='mobile.server.GameMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='serverinfo', full_name='mobile.server.GameMessage.serverinfo', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='routes', full_name='mobile.server.GameMessage.routes', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='methodname', full_name='mobile.server.GameMessage.methodname', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='parameters', full_name='mobile.server.GameMessage.parameters', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=2670, serialized_end=2786)
_CONNECTSERVERREQUEST.fields_by_name['type'].enum_type = _CONNECTSERVERREQUEST_REQUESTTYPE
_CONNECTSERVERREQUEST_REQUESTTYPE.containing_type = _CONNECTSERVERREQUEST
_CONNECTSERVERREPLY.fields_by_name['type'].enum_type = _CONNECTSERVERREPLY_REPLYTYPE
_CONNECTSERVERREPLY_REPLYTYPE.containing_type = _CONNECTSERVERREPLY
_FILTERRULE.fields_by_name['type'].enum_type = _FILTERRULE_RULETYPE
_FILTERRULE.fields_by_name['filter'].message_type = _FILTEROBJ
_FILTERRULE_RULETYPE.containing_type = _FILTERRULE
_FILTERMESSAGE.fields_by_name['method'].message_type = _MD5ORINDEX
_ENTITYMESSAGE.fields_by_name['method'].message_type = _MD5ORINDEX
_ROUTEDATA.fields_by_name['type'].enum_type = _ROUTEDATA_ROUTETYPE
_ROUTEDATA_ROUTETYPE.containing_type = _ROUTEDATA
_CUSTOMMESSAGE.fields_by_name['route'].message_type = _ROUTEDATA
_SERVICEMESSAGE.fields_by_name['entity_msg'].message_type = _ENTITYMESSAGE
_SERVICEMESSAGE.fields_by_name['service_id'].message_type = _SERVICEID
_GLOBALENTITYMESSAGE.fields_by_name['method'].message_type = _MD5ORINDEX
_ENTITYINFO.fields_by_name['type'].message_type = _MD5ORINDEX
_SERVICEINFO.fields_by_name['entity_info'].message_type = _ENTITYINFO
_SERVICEINFO.fields_by_name['service_id'].message_type = _SERVICEID
_SERVICEINFO_FORWARDTYPE.containing_type = _SERVICEINFO
_SERVICEINFO_LAYOUTTYPE.containing_type = _SERVICEINFO
_SERVERINFO_SVRTYPE.containing_type = _SERVERINFO
_ENTITYMAILBOX.fields_by_name['serverinfo'].message_type = _SERVERINFO
_SERVICEMAILBOX.fields_by_name['entitymb'].message_type = _ENTITYMAILBOX
_SERVICEMAILBOX.fields_by_name['service_id'].message_type = _SERVICEID
_GAMEMESSAGE.fields_by_name['serverinfo'].message_type = _SERVERINFO
DESCRIPTOR.message_types_by_name['Void'] = _VOID
DESCRIPTOR.message_types_by_name['ConnectServerRequest'] = _CONNECTSERVERREQUEST
DESCRIPTOR.message_types_by_name['ConnectServerReply'] = _CONNECTSERVERREPLY
DESCRIPTOR.message_types_by_name['Md5OrIndex'] = _MD5ORINDEX
DESCRIPTOR.message_types_by_name['FilterObj'] = _FILTEROBJ
DESCRIPTOR.message_types_by_name['FilterRule'] = _FILTERRULE
DESCRIPTOR.message_types_by_name['FilterMessage'] = _FILTERMESSAGE
DESCRIPTOR.message_types_by_name['EntityMessage'] = _ENTITYMESSAGE
DESCRIPTOR.message_types_by_name['RouteData'] = _ROUTEDATA
DESCRIPTOR.message_types_by_name['CustomMessage'] = _CUSTOMMESSAGE
DESCRIPTOR.message_types_by_name['ServiceId'] = _SERVICEID
DESCRIPTOR.message_types_by_name['ServiceMessage'] = _SERVICEMESSAGE
DESCRIPTOR.message_types_by_name['GlobalEntityMessage'] = _GLOBALENTITYMESSAGE
DESCRIPTOR.message_types_by_name['EntityInfo'] = _ENTITYINFO
DESCRIPTOR.message_types_by_name['ServiceInfo'] = _SERVICEINFO
DESCRIPTOR.message_types_by_name['OutBandInfo'] = _OUTBANDINFO
DESCRIPTOR.message_types_by_name['ServerInfo'] = _SERVERINFO
DESCRIPTOR.message_types_by_name['EntityMailbox'] = _ENTITYMAILBOX
DESCRIPTOR.message_types_by_name['ServiceMailbox'] = _SERVICEMAILBOX
DESCRIPTOR.message_types_by_name['ForwardAoiInfo'] = _FORWARDAOIINFO
DESCRIPTOR.message_types_by_name['GameMessage'] = _GAMEMESSAGE
Void = _reflection.GeneratedProtocolMessageType('Void', (_message.Message,), dict(DESCRIPTOR=_VOID, __module__='common_pb2'))
_sym_db.RegisterMessage(Void)
ConnectServerRequest = _reflection.GeneratedProtocolMessageType('ConnectServerRequest', (_message.Message,), dict(DESCRIPTOR=_CONNECTSERVERREQUEST, __module__='common_pb2'))
_sym_db.RegisterMessage(ConnectServerRequest)
ConnectServerReply = _reflection.GeneratedProtocolMessageType('ConnectServerReply', (_message.Message,), dict(DESCRIPTOR=_CONNECTSERVERREPLY, __module__='common_pb2'))
_sym_db.RegisterMessage(ConnectServerReply)
Md5OrIndex = _reflection.GeneratedProtocolMessageType('Md5OrIndex', (_message.Message,), dict(DESCRIPTOR=_MD5ORINDEX, __module__='common_pb2'))
_sym_db.RegisterMessage(Md5OrIndex)
FilterObj = _reflection.GeneratedProtocolMessageType('FilterObj', (_message.Message,), dict(DESCRIPTOR=_FILTEROBJ, __module__='common_pb2'))
_sym_db.RegisterMessage(FilterObj)
FilterRule = _reflection.GeneratedProtocolMessageType('FilterRule', (_message.Message,), dict(DESCRIPTOR=_FILTERRULE, __module__='common_pb2'))
_sym_db.RegisterMessage(FilterRule)
FilterMessage = _reflection.GeneratedProtocolMessageType('FilterMessage', (_message.Message,), dict(DESCRIPTOR=_FILTERMESSAGE, __module__='common_pb2'))
_sym_db.RegisterMessage(FilterMessage)
EntityMessage = _reflection.GeneratedProtocolMessageType('EntityMessage', (_message.Message,), dict(DESCRIPTOR=_ENTITYMESSAGE, __module__='common_pb2'))
_sym_db.RegisterMessage(EntityMessage)
RouteData = _reflection.GeneratedProtocolMessageType('RouteData', (_message.Message,), dict(DESCRIPTOR=_ROUTEDATA, __module__='common_pb2'))
_sym_db.RegisterMessage(RouteData)
CustomMessage = _reflection.GeneratedProtocolMessageType('CustomMessage', (_message.Message,), dict(DESCRIPTOR=_CUSTOMMESSAGE, __module__='common_pb2'))
_sym_db.RegisterMessage(CustomMessage)
ServiceId = _reflection.GeneratedProtocolMessageType('ServiceId', (_message.Message,), dict(DESCRIPTOR=_SERVICEID, __module__='common_pb2'))
_sym_db.RegisterMessage(ServiceId)
ServiceMessage = _reflection.GeneratedProtocolMessageType('ServiceMessage', (_message.Message,), dict(DESCRIPTOR=_SERVICEMESSAGE, __module__='common_pb2'))
_sym_db.RegisterMessage(ServiceMessage)
GlobalEntityMessage = _reflection.GeneratedProtocolMessageType('GlobalEntityMessage', (_message.Message,), dict(DESCRIPTOR=_GLOBALENTITYMESSAGE, __module__='common_pb2'))
_sym_db.RegisterMessage(GlobalEntityMessage)
EntityInfo = _reflection.GeneratedProtocolMessageType('EntityInfo', (_message.Message,), dict(DESCRIPTOR=_ENTITYINFO, __module__='common_pb2'))
_sym_db.RegisterMessage(EntityInfo)
ServiceInfo = _reflection.GeneratedProtocolMessageType('ServiceInfo', (_message.Message,), dict(DESCRIPTOR=_SERVICEINFO, __module__='common_pb2'))
_sym_db.RegisterMessage(ServiceInfo)
OutBandInfo = _reflection.GeneratedProtocolMessageType('OutBandInfo', (_message.Message,), dict(DESCRIPTOR=_OUTBANDINFO, __module__='common_pb2'))
_sym_db.RegisterMessage(OutBandInfo)
ServerInfo = _reflection.GeneratedProtocolMessageType('ServerInfo', (_message.Message,), dict(DESCRIPTOR=_SERVERINFO, __module__='common_pb2'))
_sym_db.RegisterMessage(ServerInfo)
EntityMailbox = _reflection.GeneratedProtocolMessageType('EntityMailbox', (_message.Message,), dict(DESCRIPTOR=_ENTITYMAILBOX, __module__='common_pb2'))
_sym_db.RegisterMessage(EntityMailbox)
ServiceMailbox = _reflection.GeneratedProtocolMessageType('ServiceMailbox', (_message.Message,), dict(DESCRIPTOR=_SERVICEMAILBOX, __module__='common_pb2'))
_sym_db.RegisterMessage(ServiceMailbox)
ForwardAoiInfo = _reflection.GeneratedProtocolMessageType('ForwardAoiInfo', (_message.Message,), dict(DESCRIPTOR=_FORWARDAOIINFO, __module__='common_pb2'))
_sym_db.RegisterMessage(ForwardAoiInfo)
GameMessage = _reflection.GeneratedProtocolMessageType('GameMessage', (_message.Message,), dict(DESCRIPTOR=_GAMEMESSAGE, __module__='common_pb2'))
_sym_db.RegisterMessage(GameMessage)
DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\x80\x01\x01\x90\x01\x01'))