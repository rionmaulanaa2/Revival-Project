# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Mecha.py
from __future__ import absolute_import
import six
from mobile.common.EntityManager import Dynamic
from .NPC import CacheableNPC
from ext_package.ext_decorator import mecha_unit_use_default_skin

@Dynamic
class Mecha(CacheableNPC):

    def __init__(self, entityid=None):
        if global_data.use_sunshine:
            from sunshine.Editor.Meta.MechaMeta import InitMechaMetaLink
            InitMechaMetaLink(self)
        super(Mecha, self).__init__(entityid)

    @mecha_unit_use_default_skin
    def init_from_dict(self, bdict):
        super(Mecha, self).init_from_dict(bdict)
        self.mecha_robot = bdict['mecha_robot']
        self.share = bdict.get('share', False)
        self.mecha_fashion = bdict.get('mecha_fashion', None)
        self.mecha_sfx = bdict.get('mecha_sfx', None)
        return

    def cache(self):
        self.mecha_robot = None
        self.share = None
        self.mecha_fashion = None
        super(Mecha, self).cache()
        return

    def get_logic_type(self):
        if self.mecha_robot and not global_data.player.is_in_global_spectate():
            from logic.units.LMechaRobot import LMechaRobot
            logic_type = LMechaRobot
        else:
            from logic.units.LMecha import LMecha
            logic_type = LMecha
        if getattr(logic_type, 'MASK', None) is None:
            logic_type.MASK = 0
        return logic_type

    def is_share(self):
        return self.share

    def trans_to_share(self):
        self.share = True
        if self.logic:
            self.logic.send_event('E_TRANS_CREATE_MECHA_TO_SHARE_NOTIFY')

    def on_add_to_battle(self, battle_id):
        from mobile.common.EntityManager import EntityManager
        from logic.gcommon.common_const import mecha_const
        bdata = self._data
        super(Mecha, self).on_add_to_battle(battle_id)
        battle = self.get_battle()
        battle.add_actor_id(self.id)
        trans_pattern = bdata.get('trans_pattern')
        if bdata:
            driver_id = bdata.get('driver_id')
            if not global_data.player.logic.ev_g_is_groupmate(driver_id):
                global_data.war_noteam_mechas[self.id] = self.logic
        if bdata and trans_pattern == mecha_const.MECHA_PATTERN_VEHICLE:
            driver_id = bdata.get('driver_id')
            passenger_info = bdata.get('passenger_dict')
            driver = None
            if driver_id:
                driver = EntityManager.getentity(driver_id)
            target = self
            if driver:
                driver.logic.send_event('E_SET_CONTROL_TARGET', target)
            myid = global_data.player.id
            if myid == driver_id:
                target.logic.send_event('E_START_CONTROL_VEHICLE')
            if passenger_info and not self.mecha_robot:
                for pid, seat_name in six.iteritems(passenger_info):
                    if driver_id == pid:
                        continue
                    p = EntityManager.getentity(pid)
                    if p and p.logic:
                        p.logic.send_event('E_SET_CONTROL_TARGET', target)

        return

    def on_remove_from_battle(self):
        battle = self.get_battle()
        battle.del_actor_id(self.id)
        if self.id in global_data.war_noteam_mechas:
            del global_data.war_noteam_mechas[self.id]
        super(Mecha, self).on_remove_from_battle()