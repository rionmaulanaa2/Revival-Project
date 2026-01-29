# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/IdManager.py
from __future__ import absolute_import
import bson.objectid as objectid
import uuid

class IdManagerInterface(object):

    @staticmethod
    def genid():
        raise NotImplementedError

    @staticmethod
    def str2id(string):
        raise NotImplementedError

    @staticmethod
    def id2str(uid):
        raise NotImplementedError

    @staticmethod
    def bytes2id(bytes):
        raise NotImplementedError

    @staticmethod
    def id2bytes(uid):
        raise NotImplementedError

    @staticmethod
    def get_id_type():
        raise NotImplementedError

    @staticmethod
    def is_id_type(obj):
        raise NotImplementedError


class IdManagerImpl_UUID(IdManagerInterface):

    @staticmethod
    def genid():
        return uuid.uuid1()

    @staticmethod
    def str2id(string):
        return uuid.UUID(string)

    @staticmethod
    def id2str(uid):
        return str(uid)

    @staticmethod
    def bytes2id(bytes):
        return uuid.UUID(bytes=bytes)

    @staticmethod
    def id2bytes(uid):
        return uid.bytes

    @staticmethod
    def get_id_type():
        return uuid.UUID

    @staticmethod
    def is_id_type(obj):
        return isinstance(obj, uuid.UUID)


class IdManagerImpl_ObjectId(IdManagerInterface):

    @staticmethod
    def genid():
        return objectid.ObjectId()

    @staticmethod
    def str2id(string):
        return objectid.ObjectId(string)

    @staticmethod
    def id2str(uid):
        return str(uid)

    @staticmethod
    def bytes2id(bytes):
        return objectid.ObjectId(bytes)

    @staticmethod
    def id2bytes(uid):
        return uid.binary

    @staticmethod
    def get_id_type():
        return objectid.ObjectId

    @staticmethod
    def is_id_type(obj):
        return isinstance(obj, objectid.ObjectId)


IdManager = IdManagerImpl_ObjectId