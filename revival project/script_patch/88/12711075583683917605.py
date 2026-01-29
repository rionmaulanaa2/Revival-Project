# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/mecha_sens_open_scheme.py
_reload_all = True
scheme = {8005: {
        'SpecialForm', 'SpecialFormMainWeapon'},
   8007: {
        'Scope'},
   8023: {
        'Scope'},
   8022: {
        'SpecialForm', 'SpecialFormMainWeapon'}
   }

def check_scope_sensitivity_opened(mecha_id):
    return 'Scope' in scheme.get(mecha_id, ())


def check_scope_main_weapon_sensitivity_opened(mecha_id):
    return 'ScopeMainWeapon' in scheme.get(mecha_id, ())


def check_scope_sub_weapon_sensitivity_opened(mecha_id):
    return 'ScopeSubWeapon' in scheme.get(mecha_id, ())


def check_special_form_sensitivity_opened(mecha_id):
    return 'SpecialForm' in scheme.get(mecha_id, ())


def check_special_form_main_weapon_sensitivity_opened(mecha_id):
    return 'SpecialFormMainWeapon' in scheme.get(mecha_id, ())


def check_special_form_sub_weapon_sensitivity_opened(mecha_id):
    return 'SpecialFormSubWeapon' in scheme.get(mecha_id, ())