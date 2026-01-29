# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/client/ClientAoIData.py
from __future__ import absolute_import
from ..common.Md5OrIndexCodec import Md5OrIndexDecoder
from ..common.proto_python import common_pb2
import aoi_data_client
PosDir = aoi_data_client.PosDir
PosType = aoi_data_client.PosType
DirType = aoi_data_client.DirType
Properties = aoi_data_client.Properties
PROPERTY_TYPE = aoi_data_client.CLIENT_TYPE
AoIUpdatesDispatcher = aoi_data_client.AoIUpdatesDispatcher
parse_collector_from_string = aoi_data_client.parse_collector_from_string
parse_posdir_from_string = aoi_data_client.parse_posdir_from_string
serialized_posdir_to_string = aoi_data_client.serialized_posdir_to_string

class AoIUpdates(aoi_data_client.AoIUpdates):

    def __init__(self, owner, id, proto_encoder):
        super(AoIUpdates, self).__init__(id)
        self.owner = owner
        self.subscribe_rpc_callback(self.rpc_callback)
        self.proto_encoder = proto_encoder

    def rpc_callback(self, md5, index, param):
        try:
            methodname, need_reg_index, index = Md5OrIndexDecoder.raw_decode(md5, index)
        except:
            return

        if methodname is None:
            return
        else:
            method = getattr(self.owner, methodname)
            if method is None:
                return
            try:
                method(self.proto_encoder.decode(param))
            except:
                pass

            return