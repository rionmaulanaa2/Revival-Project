# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/EntityMgr.py
try:
    from typing import Dict
except ImportError:
    Dict = None

from functools import partial
from uuid import uuid4
from ....SunshineRpc.Event import Event

class EntityMgr(object):

    def __init__(self):
        self._defaultDocID = str(uuid4())
        self._docs = {self._defaultDocID: EntityDocument()}
        self.EventEntitiesAdded = Event()
        self.EventEntitiesDeleted = Event()
        self.EventEntitiesModified = Event()

    def AddDocument(self, docID, doc):
        if docID in self._docs:
            return
        self._docs[docID] = doc
        doc.EventEntitiesAdded += partial(self.EventEntitiesAdded)
        doc.EventEntitiesDeleted += partial(self.EventEntitiesDeleted)
        doc.EventEntitiesModified += partial(self.EventEntitiesModified)

    def CreateDocument(self, docID=None, docName='EntityDocument'):
        doc = EntityDocument(docName)
        docID = docID or str(uuid4())
        self.AddDocument(docID, doc)
        return docID

    def GetDocument(self, docID):
        return self._docs.get(docID)

    def IterAllDocuments(self):
        for k in self._docs:
            yield (k, self._docs[k])

    @property
    def DefaultDocument(self):
        return self._docs[self._defaultDocID]

    @property
    def DefaultDocumentID(self):
        return self._defaultDocID

    def GetEntity(self, key):
        for docID in self._docs:
            doc = self._docs[docID]
            entity = doc.GetEntity(key)
            if entity:
                return entity

    def GetEntityKey(self, entity):
        for docID in self._docs:
            doc = self._docs[docID]
            for key, ent in doc.IterEntities():
                if ent is entity:
                    return key

    def GetEntityDocument(self, key):
        for docID in self._docs:
            doc = self._docs[docID]
            entity = doc.GetEntity(key)
            if entity:
                return doc

    def IterAllEntities(self):
        for docID in self._docs:
            doc = self._docs[docID]
            for key, entity in doc.IterEntities():
                yield (
                 key, entity)

    def HasEntity(self, key):
        for docID in self._docs:
            doc = self._docs[docID]
            if doc.HasEntity(key):
                return True

        return False

    def ModifyEntity(self, ey):
        pass


class EntityDocument(object):

    def __init__(self, name='EntityDocument'):
        self.name = name
        self._entities = {}
        self.EventEntitiesAdded = Event()
        self.EventEntitiesDeleted = Event()
        self.EventEntitiesModified = Event()

    def EntityCount(self):
        return len(self._entities)

    def AddEntity(self, key, entity):
        if key in self._entities:
            return
        self._entities[key] = entity
        self.EventEntitiesAdded((key,))

    def DeleteEntity(self, key):
        if key in self._entities:
            del self._entities[key]
            self.EventEntitiesDeleted((key,))

    def HasEntity(self, key):
        return key in self._entities

    def GetEntity(self, key):
        return self._entities.get(key)

    def IterEntities(self):
        for key in self._entities:
            yield (key, self._entities[key])

    def CreateEditComponent(self, entity):
        pass