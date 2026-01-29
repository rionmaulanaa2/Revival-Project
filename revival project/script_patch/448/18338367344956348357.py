# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/proto_python/gamemanager_pb2.py
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
from . import gate_game_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='gamemanager.proto', package='mobile.server', serialized_pb=_b('\n\x11gamemanager.proto\x12\rmobile.server\x1a\x0ccommon.proto\x1a\x0fgate_game.proto"A\n\x0fGameServerInfos\x12.\n\x0bgameservers\x18\x01 \x03(\x0b2\x19.mobile.server.ServerInfo"%\n\nCallbackId\x12\x17\n\x0bcallback_id\x18\x01 \x02(\x05:\x02-1"\x88\x01\n\x12GlobalEntityRegMsg\x12\x17\n\x0bcallback_id\x18\x01 \x01(\x05:\x02-1\x12\x18\n\x10entity_uniq_name\x18\x02 \x02(\x0c\x12-\n\x07mailbox\x18\x03 \x01(\x0b2\x1c.mobile.server.EntityMailbox\x12\x10\n\x08override\x18\x04 \x01(\x08"\x9b\x01\n\x14ForwardMessageHeader\x12\x17\n\x0bcallback_id\x18\x01 \x01(\x05:\x02-1\x12+\n\x05srcmb\x18\x02 \x01(\x0b2\x1c.mobile.server.EntityMailbox\x12+\n\x05dstmb\x18\x03 \x01(\x0b2\x1c.mobile.server.EntityMailbox\x12\x10\n\x08clientid\x18\x04 \x01(\x0c"\x90\x02\n\x10EntityInfoHeader\x12\x17\n\x0bcallback_id\x18\x01 \x01(\x05:\x02-1\x12\x17\n\x0ftransfer_entity\x18\x02 \x02(\x08\x12\x16\n\x0ecreate_from_db\x18\x03 \x02(\x08\x12\x17\n\x0fcreate_anywhere\x18\x04 \x02(\x05\x12-\n\ndst_server\x18\x05 \x01(\x0b2\x19.mobile.server.ServerInfo\x12-\n\nclientinfo\x18\x06 \x01(\x0b2\x19.mobile.server.ClientInfo";\n\nServerType\x12\x0c\n\x08AnyWhere\x10\x00\x12\x0f\n\x0bSpecifyType\x10\x01\x12\x0e\n\nSpecifySvr\x10\x02" \n\rGlobalMessage\x12\x0f\n\x07message\x18\x01 \x01(\x0c"(\n\nGlobalData\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c"2\n\x0eLocalIdMessage\x12\r\n\x05begin\x18\x01 \x01(\x05\x12\x11\n\trange_num\x18\x02 \x01(\x05"\x96\x02\n\x0bGmReturnVal\x12G\n\x04type\x18\x01 \x02(\x0e2\'.mobile.server.GmReturnVal.CallbackType:\x10NO_SUCH_CALLBACK\x12\x17\n\x0bcallback_id\x18\x02 \x02(\x05:\x02-1\x12\x15\n\rreturn_status\x18\x03 \x01(\x08\x12\x12\n\nreturn_val\x18\x04 \x01(\x0c\x12\x11\n\terror_msg\x18\x05 \x01(\x0c"g\n\x0cCallbackType\x12\x14\n\x10NO_SUCH_CALLBACK\x10\x00\x12\x16\n\x12REG_ENTITY_MAILBOX\x10\x01\x12\x16\n\x12FORWARD_ENTITY_MSG\x10\x02\x12\x11\n\rCREATE_ENTITY\x10\x03"C\n\x0cServerMethod\x12\x13\n\x0bserver_type\x18\x01 \x01(\x05\x12\x0e\n\x06method\x18\x02 \x01(\x0c\x12\x0e\n\x06params\x18\x03 \x01(\x0c" \n\x06Script\x12\x16\n\x0escript_content\x18\x01 \x02(\x0c"\x1f\n\x0cDbServerInfo\x12\x0f\n\x07db_name\x18\x01 \x01(\x0c"\xc9\x02\n\x08CtrlType\x12/\n\x02op\x18\x01 \x02(\x0e2\x1e.mobile.server.CtrlType.CtrlOp:\x03NOP"\x8b\x02\n\x06CtrlOp\x12\x07\n\x03NOP\x10\x00\x12\x19\n\x15FORBID_NEW_CONNECTION\x10\x01\x12\x1c\n\x18IGNORE_CLIENT_ENTITY_MSG\x10\x02\x12\x1d\n\x19DISCONNECT_ALL_CONNECTION\x10\x03\x12\x0e\n\nCLOSE_GATE\x10\x04\x12\x1d\n\x19NOTIFY_SERVER_MAINTENANCE\x10\x05\x12\x19\n\x15NOTIFY_SERVER_CLOSING\x10\x06\x12\x18\n\x14NOTIFY_SERVER_CLOSED\x10\x07\x12\x0e\n\nCLOSE_GAME\x10\x08\x12\x14\n\x10CLOSE_DB_MANAGER\x10\t\x12\x16\n\x12CLOSE_GAME_MANAGER\x10\n2\x8f\t\n\x0cIGameManager\x128\n\nrun_script\x12\x15.mobile.server.Script\x1a\x13.mobile.server.Void\x12;\n\x0bserver_ctrl\x12\x17.mobile.server.CtrlType\x1a\x13.mobile.server.Void\x12A\n\rreg_dbmanager\x12\x1b.mobile.server.DbServerInfo\x1a\x13.mobile.server.Void\x12@\n\x14get_gameservers_info\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12@\n\x0ereg_gameserver\x12\x19.mobile.server.ServerInfo\x1a\x13.mobile.server.Void\x12L\n\x12reg_entity_mailbox\x12!.mobile.server.GlobalEntityRegMsg\x1a\x13.mobile.server.Void\x12N\n\x14unreg_entity_mailbox\x12!.mobile.server.GlobalEntityRegMsg\x1a\x13.mobile.server.Void\x12K\n\x16forward_entity_message\x12\x1c.mobile.server.EntityMessage\x1a\x13.mobile.server.Void\x12P\n\x15global_entity_message\x12".mobile.server.GlobalEntityMessage\x1a\x13.mobile.server.Void\x12C\n\x0eglobal_message\x12\x1c.mobile.server.GlobalMessage\x1a\x13.mobile.server.Void\x12=\n\x0bglobal_data\x12\x19.mobile.server.GlobalData\x1a\x13.mobile.server.Void\x12A\n\x0fdel_global_data\x12\x19.mobile.server.GlobalData\x1a\x13.mobile.server.Void\x12?\n\rcreate_entity\x12\x19.mobile.server.EntityInfo\x1a\x13.mobile.server.Void\x12@\n\rgame_callback\x12\x1a.mobile.server.GmReturnVal\x1a\x13.mobile.server.Void\x12:\n\x0ekeep_alive_ack\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12;\n\x0flocalid_request\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12A\n\rserver_method\x12\x1b.mobile.server.ServerMethod\x1a\x13.mobile.server.Void2\xa8\x08\n\x12IGameManagerClient\x12K\n\x14send_gameserver_info\x12\x1e.mobile.server.GameServerInfos\x1a\x13.mobile.server.Void\x12A\n\rserver_method\x12\x1b.mobile.server.ServerMethod\x1a\x13.mobile.server.Void\x12L\n\x12reg_entity_mailbox\x12!.mobile.server.GlobalEntityRegMsg\x1a\x13.mobile.server.Void\x12N\n\x14unreg_entity_mailbox\x12!.mobile.server.GlobalEntityRegMsg\x1a\x13.mobile.server.Void\x12;\n\x0bserver_ctrl\x12\x17.mobile.server.CtrlType\x1a\x13.mobile.server.Void\x12J\n\x15remote_entity_message\x12\x1c.mobile.server.EntityMessage\x1a\x13.mobile.server.Void\x12P\n\x15global_entity_message\x12".mobile.server.GlobalEntityMessage\x1a\x13.mobile.server.Void\x12C\n\x0eglobal_message\x12\x1c.mobile.server.GlobalMessage\x1a\x13.mobile.server.Void\x12=\n\x0bglobal_data\x12\x19.mobile.server.GlobalData\x1a\x13.mobile.server.Void\x12A\n\x0fdel_global_data\x12\x19.mobile.server.GlobalData\x1a\x13.mobile.server.Void\x12?\n\rcreate_entity\x12\x19.mobile.server.EntityInfo\x1a\x13.mobile.server.Void\x12G\n\x14gamemanager_callback\x12\x1a.mobile.server.GmReturnVal\x1a\x13.mobile.server.Void\x128\n\nrun_script\x12\x15.mobile.server.Script\x1a\x13.mobile.server.Void\x126\n\nkeep_alive\x12\x13.mobile.server.Void\x1a\x13.mobile.server.Void\x12F\n\x10localid_response\x12\x1d.mobile.server.LocalIdMessage\x1a\x13.mobile.server.VoidB\x06\x80\x01\x01\x90\x01\x01'), dependencies=[
 common_pb2.DESCRIPTOR, gate_game_pb2.DESCRIPTOR])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_ENTITYINFOHEADER_SERVERTYPE = _descriptor.EnumDescriptor(name='ServerType', full_name='mobile.server.EntityInfoHeader.ServerType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='AnyWhere', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SpecifyType', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SpecifySvr', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=684, serialized_end=743)
_sym_db.RegisterEnumDescriptor(_ENTITYINFOHEADER_SERVERTYPE)
_GMRETURNVAL_CALLBACKTYPE = _descriptor.EnumDescriptor(name='CallbackType', full_name='mobile.server.GmReturnVal.CallbackType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='NO_SUCH_CALLBACK', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='REG_ENTITY_MAILBOX', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FORWARD_ENTITY_MSG', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CREATE_ENTITY', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=1049, serialized_end=1152)
_sym_db.RegisterEnumDescriptor(_GMRETURNVAL_CALLBACKTYPE)
_CTRLTYPE_CTRLOP = _descriptor.EnumDescriptor(name='CtrlOp', full_name='mobile.server.CtrlType.CtrlOp', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='NOP', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FORBID_NEW_CONNECTION', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='IGNORE_CLIENT_ENTITY_MSG', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DISCONNECT_ALL_CONNECTION', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOSE_GATE', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NOTIFY_SERVER_MAINTENANCE', index=5, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NOTIFY_SERVER_CLOSING', index=6, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NOTIFY_SERVER_CLOSED', index=7, number=7, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOSE_GAME', index=8, number=8, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOSE_DB_MANAGER', index=9, number=9, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOSE_GAME_MANAGER', index=10, number=10, options=None, type=None)], containing_type=None, options=None, serialized_start=1353, serialized_end=1620)
_sym_db.RegisterEnumDescriptor(_CTRLTYPE_CTRLOP)
_GAMESERVERINFOS = _descriptor.Descriptor(name='GameServerInfos', full_name='mobile.server.GameServerInfos', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='gameservers', full_name='mobile.server.GameServerInfos.gameservers', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=67, serialized_end=132)
_CALLBACKID = _descriptor.Descriptor(name='CallbackId', full_name='mobile.server.CallbackId', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='callback_id', full_name='mobile.server.CallbackId.callback_id', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=134, serialized_end=171)
_GLOBALENTITYREGMSG = _descriptor.Descriptor(name='GlobalEntityRegMsg', full_name='mobile.server.GlobalEntityRegMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='callback_id', full_name='mobile.server.GlobalEntityRegMsg.callback_id', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='entity_uniq_name', full_name='mobile.server.GlobalEntityRegMsg.entity_uniq_name', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='mailbox', full_name='mobile.server.GlobalEntityRegMsg.mailbox', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='override', full_name='mobile.server.GlobalEntityRegMsg.override', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=174, serialized_end=310)
_FORWARDMESSAGEHEADER = _descriptor.Descriptor(name='ForwardMessageHeader', full_name='mobile.server.ForwardMessageHeader', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='callback_id', full_name='mobile.server.ForwardMessageHeader.callback_id', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='srcmb', full_name='mobile.server.ForwardMessageHeader.srcmb', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dstmb', full_name='mobile.server.ForwardMessageHeader.dstmb', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='clientid', full_name='mobile.server.ForwardMessageHeader.clientid', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=313, serialized_end=468)
_ENTITYINFOHEADER = _descriptor.Descriptor(name='EntityInfoHeader', full_name='mobile.server.EntityInfoHeader', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='callback_id', full_name='mobile.server.EntityInfoHeader.callback_id', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='transfer_entity', full_name='mobile.server.EntityInfoHeader.transfer_entity', index=1, number=2, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='create_from_db', full_name='mobile.server.EntityInfoHeader.create_from_db', index=2, number=3, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='create_anywhere', full_name='mobile.server.EntityInfoHeader.create_anywhere', index=3, number=4, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dst_server', full_name='mobile.server.EntityInfoHeader.dst_server', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='clientinfo', full_name='mobile.server.EntityInfoHeader.clientinfo', index=5, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _ENTITYINFOHEADER_SERVERTYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=471, serialized_end=743)
_GLOBALMESSAGE = _descriptor.Descriptor(name='GlobalMessage', full_name='mobile.server.GlobalMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='message', full_name='mobile.server.GlobalMessage.message', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=745, serialized_end=777)
_GLOBALDATA = _descriptor.Descriptor(name='GlobalData', full_name='mobile.server.GlobalData', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='mobile.server.GlobalData.key', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='value', full_name='mobile.server.GlobalData.value', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=779, serialized_end=819)
_LOCALIDMESSAGE = _descriptor.Descriptor(name='LocalIdMessage', full_name='mobile.server.LocalIdMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='begin', full_name='mobile.server.LocalIdMessage.begin', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='range_num', full_name='mobile.server.LocalIdMessage.range_num', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=821, serialized_end=871)
_GMRETURNVAL = _descriptor.Descriptor(name='GmReturnVal', full_name='mobile.server.GmReturnVal', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='type', full_name='mobile.server.GmReturnVal.type', index=0, number=1, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='callback_id', full_name='mobile.server.GmReturnVal.callback_id', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='return_status', full_name='mobile.server.GmReturnVal.return_status', index=2, number=3, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='return_val', full_name='mobile.server.GmReturnVal.return_val', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error_msg', full_name='mobile.server.GmReturnVal.error_msg', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _GMRETURNVAL_CALLBACKTYPE], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=874, serialized_end=1152)
_SERVERMETHOD = _descriptor.Descriptor(name='ServerMethod', full_name='mobile.server.ServerMethod', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='server_type', full_name='mobile.server.ServerMethod.server_type', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='method', full_name='mobile.server.ServerMethod.method', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='params', full_name='mobile.server.ServerMethod.params', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1154, serialized_end=1221)
_SCRIPT = _descriptor.Descriptor(name='Script', full_name='mobile.server.Script', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='script_content', full_name='mobile.server.Script.script_content', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1223, serialized_end=1255)
_DBSERVERINFO = _descriptor.Descriptor(name='DbServerInfo', full_name='mobile.server.DbServerInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='db_name', full_name='mobile.server.DbServerInfo.db_name', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1257, serialized_end=1288)
_CTRLTYPE = _descriptor.Descriptor(name='CtrlType', full_name='mobile.server.CtrlType', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='op', full_name='mobile.server.CtrlType.op', index=0, number=1, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _CTRLTYPE_CTRLOP], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=1291, serialized_end=1620)
_GAMESERVERINFOS.fields_by_name['gameservers'].message_type = common_pb2._SERVERINFO
_GLOBALENTITYREGMSG.fields_by_name['mailbox'].message_type = common_pb2._ENTITYMAILBOX
_FORWARDMESSAGEHEADER.fields_by_name['srcmb'].message_type = common_pb2._ENTITYMAILBOX
_FORWARDMESSAGEHEADER.fields_by_name['dstmb'].message_type = common_pb2._ENTITYMAILBOX
_ENTITYINFOHEADER.fields_by_name['dst_server'].message_type = common_pb2._SERVERINFO
_ENTITYINFOHEADER.fields_by_name['clientinfo'].message_type = gate_game_pb2._CLIENTINFO
_ENTITYINFOHEADER_SERVERTYPE.containing_type = _ENTITYINFOHEADER
_GMRETURNVAL.fields_by_name['type'].enum_type = _GMRETURNVAL_CALLBACKTYPE
_GMRETURNVAL_CALLBACKTYPE.containing_type = _GMRETURNVAL
_CTRLTYPE.fields_by_name['op'].enum_type = _CTRLTYPE_CTRLOP
_CTRLTYPE_CTRLOP.containing_type = _CTRLTYPE
DESCRIPTOR.message_types_by_name['GameServerInfos'] = _GAMESERVERINFOS
DESCRIPTOR.message_types_by_name['CallbackId'] = _CALLBACKID
DESCRIPTOR.message_types_by_name['GlobalEntityRegMsg'] = _GLOBALENTITYREGMSG
DESCRIPTOR.message_types_by_name['ForwardMessageHeader'] = _FORWARDMESSAGEHEADER
DESCRIPTOR.message_types_by_name['EntityInfoHeader'] = _ENTITYINFOHEADER
DESCRIPTOR.message_types_by_name['GlobalMessage'] = _GLOBALMESSAGE
DESCRIPTOR.message_types_by_name['GlobalData'] = _GLOBALDATA
DESCRIPTOR.message_types_by_name['LocalIdMessage'] = _LOCALIDMESSAGE
DESCRIPTOR.message_types_by_name['GmReturnVal'] = _GMRETURNVAL
DESCRIPTOR.message_types_by_name['ServerMethod'] = _SERVERMETHOD
DESCRIPTOR.message_types_by_name['Script'] = _SCRIPT
DESCRIPTOR.message_types_by_name['DbServerInfo'] = _DBSERVERINFO
DESCRIPTOR.message_types_by_name['CtrlType'] = _CTRLTYPE
GameServerInfos = _reflection.GeneratedProtocolMessageType('GameServerInfos', (_message.Message,), dict(DESCRIPTOR=_GAMESERVERINFOS, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(GameServerInfos)
CallbackId = _reflection.GeneratedProtocolMessageType('CallbackId', (_message.Message,), dict(DESCRIPTOR=_CALLBACKID, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(CallbackId)
GlobalEntityRegMsg = _reflection.GeneratedProtocolMessageType('GlobalEntityRegMsg', (_message.Message,), dict(DESCRIPTOR=_GLOBALENTITYREGMSG, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(GlobalEntityRegMsg)
ForwardMessageHeader = _reflection.GeneratedProtocolMessageType('ForwardMessageHeader', (_message.Message,), dict(DESCRIPTOR=_FORWARDMESSAGEHEADER, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(ForwardMessageHeader)
EntityInfoHeader = _reflection.GeneratedProtocolMessageType('EntityInfoHeader', (_message.Message,), dict(DESCRIPTOR=_ENTITYINFOHEADER, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(EntityInfoHeader)
GlobalMessage = _reflection.GeneratedProtocolMessageType('GlobalMessage', (_message.Message,), dict(DESCRIPTOR=_GLOBALMESSAGE, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(GlobalMessage)
GlobalData = _reflection.GeneratedProtocolMessageType('GlobalData', (_message.Message,), dict(DESCRIPTOR=_GLOBALDATA, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(GlobalData)
LocalIdMessage = _reflection.GeneratedProtocolMessageType('LocalIdMessage', (_message.Message,), dict(DESCRIPTOR=_LOCALIDMESSAGE, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(LocalIdMessage)
GmReturnVal = _reflection.GeneratedProtocolMessageType('GmReturnVal', (_message.Message,), dict(DESCRIPTOR=_GMRETURNVAL, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(GmReturnVal)
ServerMethod = _reflection.GeneratedProtocolMessageType('ServerMethod', (_message.Message,), dict(DESCRIPTOR=_SERVERMETHOD, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(ServerMethod)
Script = _reflection.GeneratedProtocolMessageType('Script', (_message.Message,), dict(DESCRIPTOR=_SCRIPT, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(Script)
DbServerInfo = _reflection.GeneratedProtocolMessageType('DbServerInfo', (_message.Message,), dict(DESCRIPTOR=_DBSERVERINFO, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(DbServerInfo)
CtrlType = _reflection.GeneratedProtocolMessageType('CtrlType', (_message.Message,), dict(DESCRIPTOR=_CTRLTYPE, __module__='gamemanager_pb2'))
_sym_db.RegisterMessage(CtrlType)
DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\x80\x01\x01\x90\x01\x01'))
_IGAMEMANAGER = _descriptor.ServiceDescriptor(name='IGameManager', full_name='mobile.server.IGameManager', file=DESCRIPTOR, index=0, options=None, serialized_start=1623, serialized_end=2790, methods=[
 _descriptor.MethodDescriptor(name='run_script', full_name='mobile.server.IGameManager.run_script', index=0, containing_service=None, input_type=_SCRIPT, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='server_ctrl', full_name='mobile.server.IGameManager.server_ctrl', index=1, containing_service=None, input_type=_CTRLTYPE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reg_dbmanager', full_name='mobile.server.IGameManager.reg_dbmanager', index=2, containing_service=None, input_type=_DBSERVERINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='get_gameservers_info', full_name='mobile.server.IGameManager.get_gameservers_info', index=3, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reg_gameserver', full_name='mobile.server.IGameManager.reg_gameserver', index=4, containing_service=None, input_type=common_pb2._SERVERINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reg_entity_mailbox', full_name='mobile.server.IGameManager.reg_entity_mailbox', index=5, containing_service=None, input_type=_GLOBALENTITYREGMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='unreg_entity_mailbox', full_name='mobile.server.IGameManager.unreg_entity_mailbox', index=6, containing_service=None, input_type=_GLOBALENTITYREGMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='forward_entity_message', full_name='mobile.server.IGameManager.forward_entity_message', index=7, containing_service=None, input_type=common_pb2._ENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='global_entity_message', full_name='mobile.server.IGameManager.global_entity_message', index=8, containing_service=None, input_type=common_pb2._GLOBALENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='global_message', full_name='mobile.server.IGameManager.global_message', index=9, containing_service=None, input_type=_GLOBALMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='global_data', full_name='mobile.server.IGameManager.global_data', index=10, containing_service=None, input_type=_GLOBALDATA, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='del_global_data', full_name='mobile.server.IGameManager.del_global_data', index=11, containing_service=None, input_type=_GLOBALDATA, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='create_entity', full_name='mobile.server.IGameManager.create_entity', index=12, containing_service=None, input_type=common_pb2._ENTITYINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='game_callback', full_name='mobile.server.IGameManager.game_callback', index=13, containing_service=None, input_type=_GMRETURNVAL, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='keep_alive_ack', full_name='mobile.server.IGameManager.keep_alive_ack', index=14, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='localid_request', full_name='mobile.server.IGameManager.localid_request', index=15, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='server_method', full_name='mobile.server.IGameManager.server_method', index=16, containing_service=None, input_type=_SERVERMETHOD, output_type=common_pb2._VOID, options=None)])
IGameManager = service_reflection.GeneratedServiceType('IGameManager', (_service.Service,), dict(DESCRIPTOR=_IGAMEMANAGER, __module__='gamemanager_pb2'))
IGameManager_Stub = service_reflection.GeneratedServiceStubType('IGameManager_Stub', (IGameManager,), dict(DESCRIPTOR=_IGAMEMANAGER, __module__='gamemanager_pb2'))
_IGAMEMANAGERCLIENT = _descriptor.ServiceDescriptor(name='IGameManagerClient', full_name='mobile.server.IGameManagerClient', file=DESCRIPTOR, index=1, options=None, serialized_start=2793, serialized_end=3857, methods=[
 _descriptor.MethodDescriptor(name='send_gameserver_info', full_name='mobile.server.IGameManagerClient.send_gameserver_info', index=0, containing_service=None, input_type=_GAMESERVERINFOS, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='server_method', full_name='mobile.server.IGameManagerClient.server_method', index=1, containing_service=None, input_type=_SERVERMETHOD, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reg_entity_mailbox', full_name='mobile.server.IGameManagerClient.reg_entity_mailbox', index=2, containing_service=None, input_type=_GLOBALENTITYREGMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='unreg_entity_mailbox', full_name='mobile.server.IGameManagerClient.unreg_entity_mailbox', index=3, containing_service=None, input_type=_GLOBALENTITYREGMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='server_ctrl', full_name='mobile.server.IGameManagerClient.server_ctrl', index=4, containing_service=None, input_type=_CTRLTYPE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='remote_entity_message', full_name='mobile.server.IGameManagerClient.remote_entity_message', index=5, containing_service=None, input_type=common_pb2._ENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='global_entity_message', full_name='mobile.server.IGameManagerClient.global_entity_message', index=6, containing_service=None, input_type=common_pb2._GLOBALENTITYMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='global_message', full_name='mobile.server.IGameManagerClient.global_message', index=7, containing_service=None, input_type=_GLOBALMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='global_data', full_name='mobile.server.IGameManagerClient.global_data', index=8, containing_service=None, input_type=_GLOBALDATA, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='del_global_data', full_name='mobile.server.IGameManagerClient.del_global_data', index=9, containing_service=None, input_type=_GLOBALDATA, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='create_entity', full_name='mobile.server.IGameManagerClient.create_entity', index=10, containing_service=None, input_type=common_pb2._ENTITYINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='gamemanager_callback', full_name='mobile.server.IGameManagerClient.gamemanager_callback', index=11, containing_service=None, input_type=_GMRETURNVAL, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='run_script', full_name='mobile.server.IGameManagerClient.run_script', index=12, containing_service=None, input_type=_SCRIPT, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='keep_alive', full_name='mobile.server.IGameManagerClient.keep_alive', index=13, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='localid_response', full_name='mobile.server.IGameManagerClient.localid_response', index=14, containing_service=None, input_type=_LOCALIDMESSAGE, output_type=common_pb2._VOID, options=None)])
IGameManagerClient = service_reflection.GeneratedServiceType('IGameManagerClient', (_service.Service,), dict(DESCRIPTOR=_IGAMEMANAGERCLIENT, __module__='gamemanager_pb2'))
IGameManagerClient_Stub = service_reflection.GeneratedServiceStubType('IGameManagerClient_Stub', (IGameManagerClient,), dict(DESCRIPTOR=_IGAMEMANAGERCLIENT, __module__='gamemanager_pb2'))