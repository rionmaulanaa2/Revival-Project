# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/CommonConcertExecSequence.py
from __future__ import absolute_import
from __future__ import print_function
import math3d
import math
import time
import cclive
import render
import game3d
import os
import C_file
from random import randint
from logic.vscene.part_sys.Concert.ConcertMVMgr import s_tv_info, s_mv_model

class CommonConcertExecSequence(object):

    def __init__(self, exec_func_list, callback):
        self._exec_func_index = 0
        self._exec_func_list = exec_func_list
        self._exec_callback = callback
        self._all_time = 0

    def destroy(self):
        self._exec_func_list = []
        self._exec_callback = None
        return

    def update_exec_func(self, dt, all_time):
        self._all_time = all_time
        need_refresh, self._exec_func_index, _ = self.updata_time_exec_func(dt, self._exec_func_index, 0, self._exec_func_list)
        if need_refresh:
            self.refresh_exec_func()

    def updata_time_exec_func(self, dt, index, part_time, data_list):
        need_refresh = False
        part_time += dt
        all_time = self._all_time
        if index + 1 < len(data_list) and all_time > data_list[index + 1][0]:
            part_time = all_time - data_list[index + 1][0]
            index += 1
            need_refresh = True
            if index >= len(data_list):
                index = 0
        return (
         need_refresh, index, part_time)

    def refresh_exec_func(self):
        func_name = self._exec_func_list[self._exec_func_index][1]
        if func_name:
            args = self._exec_func_list[self._exec_func_index][2]
            start_time = self._exec_func_list[self._exec_func_index][0]
            if self._exec_callback:
                self._exec_callback(func_name, start_time, args)

    def reset_exec_func(self, all_time):
        self._all_time = all_time
        self._exec_func_index, _ = self.calculate_index_and_time(self._exec_func_list)
        self.refresh_exec_func()

    def calculate_index_and_time(self, data_list):
        cur_index = 0
        for index, data in enumerate(data_list):
            if self._all_time >= data[0]:
                cur_index = index
            else:
                break

        if cur_index >= len(data_list):
            cur_index = len(data_list) - 1
        cur_time = self._all_time - data_list[cur_index][0]
        return (
         cur_index, cur_time)