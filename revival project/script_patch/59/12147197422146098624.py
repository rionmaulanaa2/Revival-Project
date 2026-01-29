# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_critical_info.py
PATCH_TYPE_FULL = 'full'
PATCH_TYPE_MINI = 'mini'
PATCH_TYPE_INVALID = None

class PatchCriticalInfo(object):

    def __init__(self, info_str, http_prefix, patch_prefix):
        super(PatchCriticalInfo, self).__init__()
        self.patch_type = PATCH_TYPE_INVALID
        self.info = info_str
        self.url = '%s%s%s' % (http_prefix, patch_prefix, info_str)
        self.parse()

    def parse(self):
        info_list = self.info.split('_')
        if len(info_list) == 3:
            info_list.append('')
        if len(info_list) == 4:
            info_list.append('')
        if len(info_list) == 5:
            info_list.append('')
        if len(info_list) == 6:
            info_list.append('0')
        if len(info_list) == 7:
            info_list.append('')
        if len(info_list) == 8:
            info_list.append('0')
        if len(info_list) == 9:
            info_list.append('')
        self.high_res_zip_size = 0
        self.high_res_zip_md5 = ''
        self.low_res_zip_size = 0
        self.low_res_zip_md5 = ''
        self.patch_type = info_list[0]
        self.target_version = int(info_list[1])
        self.start_version = int(info_list[2])
        self.filelist_md5 = info_list[3]
        self.branch_info = info_list[4]
        self.patch_channel = info_list[5]
        self.high_res_zip_range_info = None
        self.low_res_zip_range_info = None
        return