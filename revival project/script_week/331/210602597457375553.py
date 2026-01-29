# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/predownload/store_pre_download_helper.py
import os.path
from .uni_extend import channel_wrapper, ExFuncCaller, ExFuncException
from .store_adapter.factory import StoreAdapterFactory
SUPPORT_CHANNELS = {'nearme_vivo': 18174
   }
DONT_COPY_TWICE = True
DEBUG_PRE_DOWNLOAD = False

def _log(*args):
    if DEBUG_PRE_DOWNLOAD:
        print args


def __package_support():
    import game3d
    import version
    ret = False
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        ret = channel_wrapper.name in SUPPORT_CHANNELS
        if ret:
            ver = SUPPORT_CHANNELS[channel_wrapper.name]
            try:
                ret = int(version.get_engine_version().split('.')[-1]) >= ver
            except ValueError as e:
                ret = False

    print 'store pre_download support: {}'.format(ret)
    return ret or DEBUG_PRE_DOWNLOAD


class PreDownloadObject(object):

    def __init__(self, files, target_dir):
        self._files = files
        self._target_dir = target_dir
        self._channel_name = None
        self._pre_download_jobs = None
        self._progress_callback = None
        self._finish_callback = None
        self._all_pdfiles = []
        self._success_files = []
        self._files_can_remove = []
        self._remove_all = False
        self._skip_files = PreDownloadObject.read_skip_files()
        self._store_adapter = None
        return

    @staticmethod
    def read_skip_files():
        import game3d
        import os
        doc_dir = game3d.get_doc_dir()
        skip_files_db = os.path.join(doc_dir, 'skip_files_db')
        if os.path.exists(skip_files_db):
            with open(skip_files_db, 'r') as f:
                return set(f.read().splitlines())
        return set()

    @staticmethod
    def write_skip_files(skip_files):
        import game3d
        import os
        doc_dir = game3d.get_doc_dir()
        skip_files_db = os.path.join(doc_dir, 'skip_files_db')
        with open(skip_files_db, 'w') as f:
            f.write('\n'.join(skip_files))

    @staticmethod
    def read_status():
        import game3d
        import os
        doc_dir = game3d.get_doc_dir()
        pdfiles_status_db = os.path.join(doc_dir, 'pdfiles_status_db')
        if os.path.exists(pdfiles_status_db):
            with open(pdfiles_status_db, 'r') as f:
                return f.read()
        return ''

    @staticmethod
    def set_status(status):
        import game3d
        import os
        doc_dir = game3d.get_doc_dir()
        pdfiles_status_db = os.path.join(doc_dir, 'pdfiles_status_db')
        with open(pdfiles_status_db, 'w') as f:
            f.write(status)

    def set_copy_callback(self, progress_callback, finish_callback):
        self._progress_callback = progress_callback
        self._finish_callback = finish_callback

    @staticmethod
    def ex_check_support():
        return 'checkSupport'

    def on_get_support(self, r):
        self._channel_name = r.get('pdChannel')
        self._store_adapter = StoreAdapterFactory.create(self._channel_name)

    def ex_check_available_pdfiles(self):
        ex_param = {'channel': 'store_pre_download',
           'methodId': 'checkAvailablePdFiles'
           }
        ex_param = self._store_adapter.check_available_pdfiles(ex_param)
        return ex_param

    def on_get_pdfiles(self, r):
        need_download_files = set(self._files)
        self._all_pdfiles, pre_download_jobs = self._store_adapter.get_available_pdfiles(r, need_download_files)
        _log('need_download_files:', need_download_files)
        _log('all_files:', self._all_pdfiles)
        _log('pd_files:', pre_download_jobs)
        self._pre_download_jobs = pre_download_jobs

    def ex_copy_pdfiles(self):
        if not self._pre_download_jobs:
            return {}
        skip_files = self._skip_files
        filtered_jobs = []
        _log('skip_copy_files:', skip_files)
        for file_status in self._pre_download_jobs:
            if file_status['name'] in skip_files and DONT_COPY_TWICE:
                continue
            filtered_jobs.append(file_status)

        if not filtered_jobs:
            return {}
        ex_param = {'channel': 'store_pre_download',
           'methodId': 'copyPdFiles',
           'desDirPath': self._target_dir,
           'interval': 500,
           'pdFiles': filtered_jobs
           }
        return ex_param

    def on_copy_finish(self, r):
        print 'on_copy_finish'
        success_files = []
        new_skip_files = []
        skip_files = self._skip_files
        self._store_adapter.on_copy_finish(r)
        for file_status in r.get('successfulPdFiles', []):
            if file_status['name'] in skip_files and DONT_COPY_TWICE:
                continue
            success_files.append(os.path.basename(file_status['name']))
            new_skip_files.append(file_status['name'])

        self._success_files = success_files
        PreDownloadObject.write_skip_files(skip_files.union(new_skip_files))
        if self._finish_callback:
            self._finish_callback(self._success_files)

    def on_copy_progress(self, r):
        _log(r)
        progress = r.get('progress', 0)
        if self._progress_callback:
            self._progress_callback(progress)

    def set_delete_params(self, files_can_remove, remove_all):
        self._files_can_remove = files_can_remove
        self._remove_all = remove_all

    def ex_check_and_delete_pdfiles(self):
        if not self._all_pdfiles:
            return {}
        params = self._store_adapter.check_and_delete_pdfiles(self._all_pdfiles, self._files_can_remove, self._remove_all, {})
        if not params:
            return {}
        params.update({'channel': 'store_pre_download',
           'methodId': 'deletePdFiles'
           })
        return params

    def ex_update_status(self):
        if not self._remove_all or self.read_status() != '':
            return {}
        self.set_status('success')
        params = self._store_adapter.update_status({})
        if not params:
            return {}
        params.update({'channel': 'store_pre_download',
           'methodId': 'updateStatus'
           })
        return params


def check_and_move_files(files_to_download, target_dir, progress_callback, all_finish_callback):
    print 'check_and_move_files'
    if not __package_support() or not files_to_download:
        all_finish_callback([])
        return

    def on_failed(e):
        if isinstance(e, ExFuncException):
            error_msg = '[store_pre_download] failed: {}'.format(e)
        else:
            import traceback
            traceback.print_stack()
            error_msg = '[store_pre_download] failed: {}'.format(e)
        all_finish_callback([], error_msg)

    pd_job = PreDownloadObject(files_to_download, target_dir)
    pd_job.set_copy_callback(progress_callback, all_finish_callback)
    ExFuncCaller().ex_call(pd_job.ex_check_support).exception(on_failed).then(pd_job.on_get_support).exception(on_failed).ex_call(pd_job.ex_check_available_pdfiles).exception(on_failed).then(pd_job.on_get_pdfiles).exception(on_failed).ex_call_noexcept(pd_job.ex_copy_pdfiles).then(pd_job.on_copy_finish)


def clear_files(files_can_remove, remove_all):
    print 'clear_files'
    if not __package_support():
        return

    def on_failed(e):
        if isinstance(e, ExFuncException):
            error_msg = '[store_pre_download] checkSupport failed: {}'.format(e)
        else:
            import traceback
            traceback.print_stack()
            error_msg = '[store_pre_download] checkSupport failed: {}'.format(e)
        print error_msg

    pd_job = PreDownloadObject([], '')
    pd_job.set_delete_params(files_can_remove, remove_all)
    ExFuncCaller().ex_call(pd_job.ex_check_support).exception(on_failed).then(pd_job.on_get_support).exception(on_failed).ex_call(pd_job.ex_check_available_pdfiles).exception(on_failed).then(pd_job.on_get_pdfiles).exception(on_failed).ex_call_noexcept(pd_job.ex_check_and_delete_pdfiles).ex_call_noexcept(pd_job.ex_update_status)


def test():
    check_and_move_files(['a'], 'tmp', lambda x: _log(x), lambda x, y: _log(x))