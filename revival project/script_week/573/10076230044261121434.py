# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: 10076230044261121434.py
import render
import __builtin__
import game3d

def init_urllib3_https():
    import os
    import sys
    import urllib3
    import game3d
    import C_file
    sys.setcheckinterval(10000)
    urllib3.disable_warnings()
    doc = game3d.get_doc_dir()
    try:
        if not os.path.exists(doc):
            os.makedirs(doc)
        ccp = '{}/cacert.pem'.format(doc)
        if not os.path.exists(ccp):
            d = C_file.get_res_file('cacert.pem', '')
            open(ccp, 'wb').write(d)
    except:
        try:
            import __builtin__
            __builtin__.__dict__['PRIORITY_FAILED'] = True
            import exception_hook
            exception_hook.update_game_version()
            exception_hook.post_error('[init_urllib3_https] error')
        except:
            pass


def start_game():
    import init_game
    init_game.init()
    render.logic = empty_logic
    render.set_logic(empty_logic)
    game3d.delay_exec(100, lambda : init_game.start())


def start_ext_patch():
    try:
        from patch.patch_utils import is_support_base_package
        if is_support_base_package():
            from ext_package import ext_patch_ui
            ext_patch_ui.ExtPatchUI(start_game)
        else:
            start_game()
    except:
        start_game()


def start():
    render.set_logic(logic)


def logic():
    import exception_hook
    exception_hook.register_hook()
    exception_hook.update_game_version()
    render.set_logic(None)
    import game3d
    game3d.show_render_info(False)
    init_urllib3_https()
    import C_file
    aab_package = bool(C_file.find_res_file('aab_package_flag.flag', ''))
    if aab_package:
        try:
            import playassetdelivery
        except:
            aab_package = False

    if aab_package:
        start_game()
    else:
        start_game()
    return


def start_abb_package():
    from patch import patch_aab
    patch_aab.AABPackageUI(start_patch)


def start_patch():
    __builtin__.__dict__['AAB_UI_INSTANCE'] = None
    from patch import patch_ui
    patch_ui.PatchUI(start_ext_patch)
    return


def check_package():
    import package_utils
    import C_file
    import __builtin__
    reverted = __builtin__.__dict__.get('NEW_PACKAGE_REVERTED', False)
    if package_utils.check_new_package() and not reverted:
        C_file.unload_fileloader('week')
        C_file.unload_fileloader('patch')
    else:
        C_file.set_fileloader_enable('week', True)
        C_file.set_fileloader_enable('patch', True)


def empty_logic():
    pass