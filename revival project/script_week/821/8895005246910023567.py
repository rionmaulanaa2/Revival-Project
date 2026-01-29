# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/lottery/art_collection_main_uis.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_art_collection_main_uis import *
else:
    main_uis = {'WIDGET_LOTTERY_AUTO_ROTATE1_MainUI': {'PANEL_CONFIG_NAME': 'mall/i_lottery_activity/s8/lottery_activity_main_s8','ACTIVITY_TYPE': 'WIDGET_LOTTERY_AUTO_ROTATE1'},'WIDGET_LOTTERY_AUTO_ROTATE2_MainUI': {'PANEL_CONFIG_NAME': 'mall/i_lottery_activity/s8/lottery_activity_main_s8','ACTIVITY_TYPE': 'WIDGET_LOTTERY_AUTO_ROTATE2'},'WIDGET_LOTTERY_AUTO_CSWZLD240930_MainUI': {'PANEL_CONFIG_NAME': 'mall/i_lottery_activity/chaoshouwuzhuang/lottery_activity_main_cswz','ACTIVITY_TYPE': 'WIDGET_LOTTERY_AUTO_CSWZLD240930'}}
import six
g = globals()

class Module(object):

    def __getattr__(self, uiname):
        global main_uis
        try:
            cls = main_uis[uiname]
            if isinstance(cls, dict):
                from .ArtCollectionMainUI import ArtCollectionMainUI
                cls = main_uis[uiname] = type(uiname, (ArtCollectionMainUI,), cls)
            return cls
        except Exception as e:
            log_error('[MAIN UI %s] not exist, %s' % (uiname, str(e)))
            return None

        return None


module = Module()
for uiname in six.iterkeys(main_uis):
    g[uiname] = module