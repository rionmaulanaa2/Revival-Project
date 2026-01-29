# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/editor_utils/mecha_data_utils.py
from __future__ import absolute_import
import six_ex
from logic.gutils.editor_utils import mecha_weapons_skills_params
import os

def check_update_local_mecha_weapons_skills_data(check_mecha_id, bdict):
    if check_mecha_id and 8000 < check_mecha_id < 8200:
        if check_mecha_id not in mecha_weapons_skills_params.weapons_skills_params:
            mecha_weapons_skills_params.weapons_skills_params[check_mecha_id] = {'weapons': bdict.get('weapons', {}),'skills': bdict.get('skills', {})
               }
            need_write = True
        else:
            need_write = mecha_weapons_skills_params.weapons_skills_params[check_mecha_id]['weapons'] == bdict.get('weapons', {}) and mecha_weapons_skills_params.weapons_skills_params[check_mecha_id]['skills'] == bdict.get('skills', {})
        if need_write:
            output_str_list = [
             '# -*- coding:utf-8 -*-\n\nweapons_skills_params = {']
            all_mecha_ids = six_ex.keys(mecha_weapons_skills_params.weapons_skills_params)
            all_mecha_ids.sort()
            for mecha_id in all_mecha_ids:
                data = mecha_weapons_skills_params.weapons_skills_params[mecha_id]
                output_str_list.append('\t%d: {' % mecha_id)
                output_str_list.append("\t\t'weapons': %s," % str(data['weapons']))
                output_str_list.append("\t\t'skills': %s," % str(data['skills']))
                output_str_list.append('\t},')

            output_str_list.append('}\n')
            with open(os.path.basename(mecha_weapons_skills_params.__file__), 'w') as f:
                f.write('\n'.join(output_str_list))