# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSelectionBase.py
from __future__ import absolute_import
import six_ex
from ..UnitCom import UnitCom

class ComSelectionBase(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_ON_BEING_SELECTED': '_on_being_selected',
       'E_ON_LOSING_SELECTED': '_on_losing_selected',
       'E_SELECTOR_MODEL_LOADED': '_on_selector_model_loaded'
       }

    def __init__(self):
        super(ComSelectionBase, self).__init__()
        self.mp_holder = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComSelectionBase, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComSelectionBase, self).destroy()

    def try_get_selector_entity(self, id_selector):
        from mobile.common.EntityManager import EntityManager
        e_selector = EntityManager.getentity(id_selector)
        return e_selector

    def check_model_binding(self, id_selector):
        if not id_selector:
            return
        e_selector = self.try_get_selector_entity(id_selector)
        if not e_selector or not e_selector.logic:
            log_error('[ComSelectionBase] Getting e_selector entity by id error.')
            return
        mdl_selector = e_selector.logic.ev_g_model()
        m_model = self.ev_g_model()
        if not mdl_selector or not m_model:
            return
        self.do_model_binding(id_selector, mdl_selector, m_model)

    def _on_model_loaded(self, model):
        for id_selector in six_ex.keys(self.mp_holder):
            self.check_model_binding(id_selector)

    def _on_selector_model_loaded(self, id_selector, mdl_selector):
        if id_selector:
            self.check_model_binding(id_selector)

    def _on_being_selected(self, id_selector, control_info):
        if id_selector is None:
            log_error('[ComSelectionBase] error id_selector - None.')
            return
        else:
            self.mp_holder[id_selector] = control_info
            if id_selector != self.unit_obj.id:
                self.check_model_binding(id_selector)
            return

    def _on_losing_selected(self, id_selector):
        if id_selector in self.mp_holder:
            self.mp_holder.pop(id_selector)
        e_selector = self.try_get_selector_entity(id_selector)
        if e_selector:
            mdl_selector = e_selector.logic.ev_g_model()
            if mdl_selector:
                self.do_model_unbinding(mdl_selector)

    def do_model_binding(self, id_selector, mdl_selector, mdl_target):
        raise NotImplementedError('Every Selection should implement <do_model_binding> method.')

    def do_model_unbinding(self, mdl_selector):
        mdl_selector.remove_from_parent()
        mdl_selector.visible = True
        self.scene.add_object(mdl_selector)