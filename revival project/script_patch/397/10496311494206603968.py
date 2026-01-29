# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/item_config.py
from __future__ import absolute_import
if G_IS_CLIENT:
    import common.cfg.confmgr as confmgr

    def get_by_id(item_id):
        return confmgr.get('item', str(item_id))


    def get_use_by_id(item_id):
        return confmgr.get('item_use', str(item_id))


else:
    from data import item_data, item_use_data

    def get_by_id(item_id):
        return item_data.get_config_by_item_id(item_id)


    def get_use_by_id(item_id):
        return item_use_data.get_config_by_item_id(item_id)