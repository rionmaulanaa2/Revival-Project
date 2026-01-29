# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/archive/appendarchievedata.py
from __future__ import absolute_import
import os
import game3d

class AppendArchiveData(object):

    def __init__(self, key='default', delimiter='\t\t\t'):
        super(AppendArchiveData, self).__init__()
        self.filename = '{0}_{1}'.format('data', key)
        self._delimiter = delimiter
        self.init()

    def init(self):
        doc_dir = game3d.get_doc_dir()
        filename = self.filename
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)
        self._path = os.path.join(doc_dir, filename)

    def load(self):
        try:
            with open(self._path, 'r') as f:
                s = f.read()
            data_list = s.split(self._delimiter)
        except Exception as e:
            log_error('[AppendArchiveData] load file except:{}'.format(str(e)))
            data_list = []

        return data_list

    def clear_save_data(self):
        try:
            with open(self._path, 'w') as f:
                f.write('')
        except Exception as e:
            log_error('[AppendArchiveData] clear_save_data except: {}'.format(str(e)))

    def append_save(self, data_list):
        doc_dir = game3d.get_doc_dir()
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)
        try:
            result_str = self._delimiter.join(data_list)
            with open(self._path, 'a') as tmp_file:
                tmp_file.write(result_str)
        except Exception as e:
            log_error('[AppendArchiveData] append save except:{}'.format(str(e)))

    def del_data(self):
        if os.path.exists(self._path):
            try:
                os.remove(self._path)
            except Exception as e:
                log_error('[AppendArchiveData] del_data except:{}'.format(str(e)))