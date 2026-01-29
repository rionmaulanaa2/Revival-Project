# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaControlBtn/MechaModule.py
from __future__ import absolute_import
import six

class MechaModule(object):

    def __init__(self, parent, nd_aprent, kargs):
        self.kargs = kargs
        self.parent = parent
        self.nd_parent = nd_aprent
        self.icon_path = None
        if self.nd_parent.icon:
            self.icon_path = self.nd_parent.icon.GetDisplayFramePath()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'observer_install_module_result_event': self.on_installed,
           'observer_uninstall_module_result_event': self.on_uninstall
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def bind_events(self, mecha):
        self.process_event(True)
        lplayer = global_data.cam_lplayer
        if lplayer and self.kargs:
            cur_modules = lplayer.ev_g_mecha_all_installed_module()
            for slot_pos, v in six.iteritems(cur_modules):
                card_id, item_id = v
                if str(card_id) in self.kargs:
                    self.on_installed(True, slot_pos, card_id, item_id)

    def unbind_events(self, mecha):
        self.process_event(False)

    def destroy(self):
        self.process_event(False)
        self.parent = None
        self.nd_parent = None
        return

    def on_installed(self, result, slot_pos, card_id, item_id):
        if not self.kargs:
            return
        if not result:
            return
        path = self.kargs.get(str(card_id))
        if self.nd_parent.icon and path:
            self.nd_parent.icon.SetDisplayFrameByPath('', path)

    def on_uninstall(self, result, slot_pos, card_id, clear_item):
        if not self.kargs:
            return
        if not result:
            return
        if str(card_id) in self.kargs and self.nd_parent.icon and self.icon_path:
            self.nd_parent.icon.SetDisplayFrameByPath('', self.icon_path)