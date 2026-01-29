# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/predownload/store_adapter/factory.py


class StoreAdapterCommon(object):

    def check_available_pdfiles(self, params):
        return params

    def get_available_pdfiles(self, result_dict, need_download_files):
        import os.path
        all_files = []
        pre_download_jobs = []
        for file_status in result_dict.get('pdFiles', []):
            if file_status.get('state', 2) == 2:
                all_files.append(file_status)
                if os.path.basename(file_status['name']) in need_download_files:
                    pre_download_jobs.append(file_status)

        return (
         all_files, pre_download_jobs)

    def check_and_delete_pdfiles(self, all_pdfiles, files_can_remove, remove_all, params):
        import os.path
        all_pdfiles_dict = {}
        for file_status in all_pdfiles:
            all_pdfiles_dict[file_status['name']] = file_status

        remove_files = []
        if remove_all:
            remove_files = all_pdfiles
        else:
            for file_name in files_can_remove:
                file_name = os.path.basename(file_name)
                if file_name in all_pdfiles_dict:
                    remove_files.append(all_pdfiles_dict[file_name])

        if remove_files:
            params['pdFiles'] = remove_files
        return params

    def on_copy_finish(self, result_dict):
        return result_dict

    def update_status(self, params):
        return params


class StoreAdapterHuawei(StoreAdapterCommon):

    def check_available_pdfiles(self, params):
        params['requestPermission'] = True
        params['permissionTips'] = '\xe8\xaf\xb7\xe5\x85\x81\xe8\xae\xb8\xe5\xba\x94\xe7\x94\xa8\xe8\xae\xbf\xe9\x97\xae\xe6\x82\xa8\xe7\x9a\x84\xe5\xad\x98\xe5\x82\xa8\xe7\xa9\xba\xe9\x97\xb4\xef\xbc\x8c\xe4\xbb\xa5\xe4\xbe\xbf\xe4\xbd\xbf\xe7\x94\xa8\xe5\xba\x94\xe7\x94\xa8\xe5\x95\x86\xe5\xba\x97\xe9\xa2\x84\xe4\xb8\x8b\xe8\xbd\xbd\xe8\xb5\x84\xe6\xba\x90\xe3\x80\x82'
        params['gotoSettingReason'] = '\xe8\xaf\xb7\xe5\x85\x81\xe8\xae\xb8\xe5\xba\x94\xe7\x94\xa8\xe8\xae\xbf\xe9\x97\xae\xe6\x82\xa8\xe7\x9a\x84\xe5\xad\x98\xe5\x82\xa8\xe7\xa9\xba\xe9\x97\xb4,\xe4\xbb\xa5\xe4\xbe\xbf\xe5\xba\x94\xe7\x94\xa8\xe5\x95\x86\xe5\xba\x97\xe9\xa2\x84\xe4\xb8\x8b\xe8\xbd\xbd\xe8\xb5\x84\xe6\xba\x90\xe3\x80\x82'
        return params

    def update_status(self, params):
        params['copySuccess'] = True
        return params


class StoreAdapterHonor(StoreAdapterCommon):

    def update_status(self, params):
        params['copySuccess'] = True
        return params


class StoreAdapterXiaomi(StoreAdapterCommon):

    def check_and_delete_pdfiles(self, all_pdfiles, files_can_remove, remove_all, params):
        if not remove_all:
            return params
        super(StoreAdapterXiaomi, self).check_and_delete_pdfiles(all_pdfiles, files_can_remove, remove_all, params)
        if len(params.pop('pdFiles', [])) == len(files_can_remove):
            params['finished'] = True
        return params


class StoreAdapterVivo(StoreAdapterCommon):

    def check_and_delete_pdfiles(self, all_pdfiles, files_can_remove, remove_all, params):
        super(StoreAdapterVivo, self).check_and_delete_pdfiles(all_pdfiles, files_can_remove, remove_all, params)
        params['finished'] = remove_all
        return params


class StoreAdapterOppo(StoreAdapterCommon):

    def check_available_pdfiles(self, params):
        params['requestPermission'] = True
        params['permissionTips'] = '\xe8\xaf\xb7\xe5\x85\x81\xe8\xae\xb8\xe5\xba\x94\xe7\x94\xa8\xe8\xae\xbf\xe9\x97\xae\xe6\x82\xa8\xe7\x9a\x84\xe5\xad\x98\xe5\x82\xa8\xe7\xa9\xba\xe9\x97\xb4,\xe4\xbb\xa5\xe4\xbe\xbf\xe4\xb8\x8b\xe8\xbd\xbd\xe9\xa2\x84\xe7\xbd\xae\xe5\x8c\x85\xe4\xbd\x93\xe3\x80\x82'
        params['gotoSettingReason'] = '\xe8\xaf\xb7\xe5\x85\x81\xe8\xae\xb8\xe5\xba\x94\xe7\x94\xa8\xe8\xae\xbf\xe9\x97\xae\xe6\x82\xa8\xe7\x9a\x84\xe5\xad\x98\xe5\x82\xa8\xe7\xa9\xba\xe9\x97\xb4,\xe4\xbb\xa5\xe4\xbe\xbf\xe4\xb8\x8b\xe8\xbd\xbd\xe9\xa2\x84\xe7\xbd\xae\xe5\x8c\x85\xe4\xbd\x93\xe3\x80\x82'
        return params


class StoreAdapterFactory(object):

    @staticmethod
    def create(channel_name):
        channel_name_to_class = 'StoreAdapter' + channel_name.lower().capitalize()
        cls = globals().get(channel_name_to_class, StoreAdapterCommon)
        return cls()