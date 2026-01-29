# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/rank_region_const.py
from __future__ import absolute_import
from logic.gcommon.common_const import rank_const as rconst
REGION_RANK_TYPE_FAULT = '0'
REGION_RANK_TYPE_UNKNOW = '1'
REGION_RANK_TYPE_COUNTRY = '2'
REGION_RANK_TYPE_PROVINCE = '3'
REGION_RANK_TYPE_CITY = '4'
REGION_RANK_TYPE_DISTRICT = '5'
REGION_RANK_PRIORITY_QUEUE = (
 REGION_RANK_TYPE_COUNTRY, REGION_RANK_TYPE_PROVINCE, REGION_RANK_TYPE_CITY, REGION_RANK_TYPE_UNKNOW)
if rconst.is_world_mecha_region_rank():

    def get_region_rank_type(rank_adcode):
        try:
            adcode = str(rank_adcode)
            if adcode == '0000000':
                return REGION_RANK_TYPE_UNKNOW
            if adcode[-2:] != '00':
                return REGION_RANK_TYPE_DISTRICT
            if adcode[-4:-2] != '00':
                return REGION_RANK_TYPE_CITY
            if adcode[:3] != '100':
                return REGION_RANK_TYPE_PROVINCE
            return REGION_RANK_TYPE_COUNTRY
        except:
            return REGION_RANK_TYPE_FAULT


else:

    def get_region_rank_type(rank_adcode):
        try:
            adcode = str(rank_adcode)
            if adcode == '000000':
                return REGION_RANK_TYPE_UNKNOW
            if adcode[-2:] != '00':
                return REGION_RANK_TYPE_DISTRICT
            if adcode[-4:-2] != '00':
                return REGION_RANK_TYPE_CITY
            if adcode[:2] != '10':
                return REGION_RANK_TYPE_PROVINCE
            return REGION_RANK_TYPE_COUNTRY
        except:
            return REGION_RANK_TYPE_FAULT