# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LPet.py
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=[
 'ComStatusMonster'], client=[
 'com_pet.ComPetAppearance',
 'com_pet.ComPetBehavior',
 'com_pet.ComPetAnimMgr',
 'com_pet.ComLodPet',
 'com_pet.ComPetFollow',
 'com_pet.ComPetSynchronizer'])
class LPet(Unit):
    MASK = 0

    def init_from_dict(self, bdict):
        super(LPet, self).init_from_dict(bdict)

    def destroy(self):
        super(LPet, self).destroy()

    def is_pet(self):
        return True