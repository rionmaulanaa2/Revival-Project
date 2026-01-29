# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_patch_npk.py
from __future__ import absolute_import
import os
import zlib
import time
import C_file
import game3d
import package
from patch import patch_path
from ext_package import ext_pn_utils
from .ext_package_utils import other_err_log, cout_error, cout_info
import six
LOG_CHANNEL = 'ext_patch_npk'
W_NPK_STATE_FLUSHED = 1
W_NPK_STATE_WRITABLE = 0
IS_RELEASE = game3d.is_release_version()

class ExtWriteNpkWrapper(object):

    def __init__(self, in_w_npk, in_temp_name, in_final_name):
        super(ExtWriteNpkWrapper, self).__init__()
        self.w_npk = in_w_npk
        self.npk_size = 0
        self.temp_name = in_temp_name
        self.final_name = in_final_name
        self.npk_state = W_NPK_STATE_WRITABLE
        self.flist_lst = []
        self.flist_dict = {}
        self.index_lst = []

    def get_flist_npk_name(self):
        return self.final_name

    def get_flist_index(self):
        flist_npk_name = self.get_flist_npk_name()
        return ext_pn_utils.get_patch_npk_flist_file_id(flist_npk_name)


class ExtPatchNpkProcessor(object):

    def __init__(self):
        super(ExtPatchNpkProcessor, self).__init__()
        self._removed_npk_set = set()
        self._exist_npk_info = {}
        self._idx_to_exist_npk_dict = {}
        self._w_npk_lst = []
        self._duplicate_npk_set = set()
        self._all_new_idx_set = set()
        self._new_flist_map = {}
        self._local_npk_flist_map = {}
        self._root_dir = ext_pn_utils.get_ext_patch_npk_dir()

    def is_file_in_ext_patch_npk(self, f_path, pkg_crc):
        if not self._exist_npk_info:
            return False
        else:
            file_index_id = patch_path.get_patch_file_hash(f_path)
            if file_index_id is None:
                return False
            for npk_name in self._exist_npk_info:
                flist_dict = self._exist_npk_info[npk_name][1]
                if file_index_id in flist_dict:
                    record_pkg_crc = int(flist_dict[file_index_id][3])
                    if record_pkg_crc == pkg_crc:
                        return True
                    if npk_name in self._duplicate_npk_set:
                        continue
                    else:
                        return False

            return False

    def set_new_flist_map(self, new_map):
        self._new_flist_map = new_map

    def set_local_npk_flist_map(self, in_npk_map):
        self._local_npk_flist_map = in_npk_map

    def add_ext_patch_data(self, src_data, index_id, pkg_crc, in_finfo):
        if pkg_crc < 0:
            pkg_crc_sign = 0 if 1 else 1
            if not self._prepare_npk_writer():
                return False
            npk_wrapper = self._w_npk_lst[-1]
            if index_id in self._all_new_idx_set:
                cout_error(LOG_CHANNEL, 'index_id:{} has already added'.format(index_id))
                return False
            ret_size = npk_wrapper.w_npk.add_patch_data(index_id, src_data, pkg_crc_sign, abs(pkg_crc), False)
            if ret_size < 0:
                cout_error(LOG_CHANNEL, 'add_patch_data return:{}'.format(ret_size))
                return False
            self._all_new_idx_set.add(index_id)
            npk_wrapper.flist_lst.append('{}\t{}\t{}\t{}'.format(index_id, in_finfo[0], in_finfo[1], in_finfo[2]))
            npk_wrapper.flist_dict[index_id] = int(in_finfo[1])
            npk_wrapper.index_lst.append(index_id)
            npk_wrapper.npk_size += ret_size
            if npk_wrapper.npk_size >= ext_pn_utils.MAX_NPK_SIZE:
                flush_ret = self._npk_flush(npk_wrapper)
                flush_ret or cout_error(LOG_CHANNEL, 'flush:{} failed'.format(npk_wrapper.final_name))
                return False
            npk_wrapper.npk_state = W_NPK_STATE_FLUSHED
        return True

    def _add_old_npk_data_to_new(self, index_id, npk_reader, f_info):
        if not self._prepare_npk_writer():
            return False
        npk_wrapper = self._w_npk_lst[-1]
        if index_id in npk_wrapper.index_lst:
            cout_error(LOG_CHANNEL, 'index id duplication:{} {} {}'.format(index_id, npk_wrapper.temp_name, f_info[1]))
            return (
             False, False)
        ret_size = npk_wrapper.w_npk.add_npk_data_v2(index_id, npk_reader)
        if ret_size < 0:
            cout_error(LOG_CHANNEL, 'add npk data return:{}'.format(ret_size))
            return (
             False, False)
        npk_wrapper.index_lst.append(index_id)
        npk_wrapper.flist_lst.append('\t'.join(f_info))
        npk_wrapper.flist_dict[index_id] = int(f_info[2])
        npk_wrapper.npk_size += ret_size
        if npk_wrapper.npk_size >= ext_pn_utils.MAX_NPK_SIZE:
            flush_ret = self._npk_flush(npk_wrapper)
            if not flush_ret:
                return (False, False)
            npk_wrapper.npk_state = W_NPK_STATE_FLUSHED
            return (
             flush_ret, True)
        return (True, False)

    def ext_update_and_flush_all_npk(self, update_prog_func=None):
        b_time = time.time()
        has_new_res_npk = len(self._w_npk_lst) > 0
        cout_info(LOG_CHANNEL, '[update_and_flush_all] new res:{}'.format(has_new_res_npk))
        if not has_new_res_npk:
            pass
        need_up_npk = set()
        for npk_name in self._duplicate_npk_set:
            need_up_npk.add(npk_name)

        for index_id in self._all_new_idx_set:
            if index_id in self._idx_to_exist_npk_dict:
                for hit_npk_name in self._idx_to_exist_npk_dict[index_id]:
                    need_up_npk.add(hit_npk_name)

        all_old_small_res_npk = set()
        for npk_file_name in self._exist_npk_info:
            if npk_file_name in need_up_npk:
                continue
            if self._new_flist_map:
                npk_org_flist_dict = self._exist_npk_info[npk_file_name][1]
                for index_id in npk_org_flist_dict:
                    f_info = npk_org_flist_dict[index_id]
                    f_path = f_info[1]
                    if f_path not in self._new_flist_map:
                        cout_info(LOG_CHANNEL, 'need tidy:{} for no need res'.format(npk_file_name))
                        need_up_npk.add(npk_file_name)
                        break
                    elif int(self._new_flist_map[f_path][2]) != int(f_info[3]):
                        cout_info(LOG_CHANNEL, 'need tidy:{} for old res'.format(npk_file_name))
                        need_up_npk.add(npk_file_name)
                        break

            npk_size = self._exist_npk_info[npk_file_name][0]
            if npk_size < ext_pn_utils.MAX_NPK_SIZE:
                all_old_small_res_npk.add(npk_file_name)

        if has_new_res_npk or need_up_npk or len(all_old_small_res_npk) > 1:
            need_up_npk.update(all_old_small_res_npk)
        cout_info(LOG_CHANNEL, 'need up npk:{}'.format(need_up_npk))
        C_file.unload_fileloader(ext_pn_utils.EXT_LOADER_TAG)
        all_process_num = 1
        processed_num = 0
        if update_prog_func is not None:
            for up_npk_name in need_up_npk:
                flist_dict = self._exist_npk_info[up_npk_name][1]
                all_process_num += len(flist_dict)

        from patch import patch_const
        if hasattr(patch_const, 'ENABLE_CHECK_BASE_NPK') and patch_const.ENABLE_CHECK_BASE_NPK:
            npk_flist_dict = self._local_npk_flist_map
        else:
            npk_flist_dict = {}
        processed_npk_lst = []
        for up_npk_name in need_up_npk:
            cout_info(LOG_CHANNEL, 'processing old npk:{}'.format(up_npk_name))
            py_npk_path, abs_real_path = self._get_nx_npk_path(up_npk_name)
            try:
                nx_open_npk = package.nxnpk(py_npk_path)
            except Exception as e:
                other_err_log(LOG_CHANNEL, 'open npk except: {} {}'.format(up_npk_name, str(e)))
                return False

            npk_org_flist_dict = self._exist_npk_info[up_npk_name][1]
            flist_index = ext_pn_utils.get_patch_npk_flist_file_id(up_npk_name)
            for index_id in npk_org_flist_dict:
                processed_num += 1
                if update_prog_func is not None:
                    update_prog_func(processed_num * 1.0 / all_process_num)
                if index_id in self._all_new_idx_set or index_id == flist_index:
                    continue
                else:
                    f_info = npk_org_flist_dict[index_id]
                    f_path = f_info[1]
                    org_crc_in_npk = int(f_info[2])
                    if self._new_flist_map:
                        if f_path not in self._new_flist_map:
                            cout_info(LOG_CHANNEL, 'not in new flist, ignore:{}'.format(f_path))
                            continue
                        elif int(self._new_flist_map[f_path][2]) != int(f_info[3]):
                            cout_info(LOG_CHANNEL, 'file:{} is old in {} for pkg crc'.format(f_path, up_npk_name))
                            continue
                        elif int(self._new_flist_map[f_path][1]) != org_crc_in_npk:
                            cout_info(LOG_CHANNEL, 'file:{} pkg equal, org not equal, in {}'.format(f_path, up_npk_name))
                            continue
                    if f_path in npk_flist_dict and org_crc_in_npk == int(npk_flist_dict[f_path][1]):
                        cout_info(LOG_CHANNEL, 'res file exists in local npk: {}'.format(f_path))
                        continue
                    ret, flushed = self._add_old_npk_data_to_new(index_id, nx_open_npk, f_info)
                    if not ret:
                        return False
                    self._all_new_idx_set.add(index_id)
                    if flushed:
                        self._remove_old_npk(processed_npk_lst)
                        processed_npk_lst = []

            nx_open_npk = None
            cout_info(LOG_CHANNEL, 'processing old npk done')
            processed_npk_lst.append(up_npk_name)

        for npk_wrapper in self._w_npk_lst:
            if npk_wrapper.npk_state != W_NPK_STATE_FLUSHED:
                flush_ret = self._npk_flush(npk_wrapper)
                if not flush_ret:
                    return False

        self._remove_old_npk(processed_npk_lst)
        cout_info(LOG_CHANNEL, '[update_and_flush_all] process:{} cost time:{}'.format(all_process_num, time.time() - b_time))
        return True

    def _remove_old_npk(self, remove_lst):
        for processed_npk_name in remove_lst:
            up_npk_path = os.path.join(self._root_dir, processed_npk_name)
            try:
                os.remove(up_npk_path)
            except Exception as e:
                cout_error(LOG_CHANNEL, 'remove:{} except:{}'.format(processed_npk_name, str(e)))

            self._removed_npk_set.add(processed_npk_name)

        remove_lst = []

    def verify_and_save_new_npk_info(self, update_prog_func=None):
        all_npk_name_lst = set()
        for npk_name in self._exist_npk_info:
            if npk_name not in self._removed_npk_set:
                all_npk_name_lst.add(npk_name)

        for npk_wrapper in self._w_npk_lst:
            all_npk_name_lst.add(npk_wrapper.final_name)

        new_info = {}
        for npk_name in all_npk_name_lst:
            npk_path = os.path.join(self._root_dir, npk_name)
            try:
                if not os.path.exists(npk_path):
                    cout_error(LOG_CHANNEL, '[save_npk_info] npk not exists:{}'.format(npk_path))
                    return False
                npk_size = os.path.getsize(npk_path)
            except Exception as e:
                other_err_log(LOG_CHANNEL, '[save_npk_info] except: {} {}'.format(npk_name, str(e)))
                return False

            new_info.setdefault(npk_name, {})
            new_info[npk_name]['size'] = npk_size

        save_ret, error_str = ext_pn_utils.save_ext_patch_npk_info(new_info)
        if not save_ret:
            self._w_npk_lst = []
            cout_error(LOG_CHANNEL, 'save npk info except:{}'.format(error_str))
            return False
        self._w_npk_lst = []
        return True

    def _prepare_npk_writer(self):
        if not self._w_npk_lst:
            if not self._add_new_npk_writer():
                return False
        if self._w_npk_lst[-1].npk_state != W_NPK_STATE_WRITABLE:
            if not self._add_new_npk_writer():
                return False
        return True

    def _add_new_npk_writer(self):
        new_tmp_file_name, new_final_file_name = self._generate_new_npk_name()
        w_npk_path = os.path.join(self._root_dir, new_tmp_file_name)
        w_npk = package.npkwriter()
        ret = w_npk.open(w_npk_path, 0)
        if ret:
            self._w_npk_lst.append(ExtWriteNpkWrapper(w_npk, new_tmp_file_name, new_final_file_name))
        return ret

    def _generate_new_npk_name(self):
        b_num = 1
        final_pattern = ext_pn_utils.EXT_RES_NPK_SUBFIX_PATTERN
        temp_pattern = ext_pn_utils.TEMP_EXT_RES_NPK_SUBFIX_PATTERN
        while True:
            tmp_file_name = temp_pattern.format(b_num)
            final_file_name = final_pattern.format(b_num)
            tmp_file_path = os.path.join(self._root_dir, tmp_file_name)
            final_file_path = os.path.join(self._root_dir, final_file_name)
            if final_file_name in self._exist_npk_info:
                b_num += 1
                continue
            elif os.path.exists(tmp_file_path) or os.path.exists(final_file_path):
                b_num += 1
                continue
            else:
                return (
                 tmp_file_name, final_file_name)

    def _npk_flush(self, w_npk_wrapper):
        npk_final_name = w_npk_wrapper.final_name
        file_index_id = w_npk_wrapper.get_flist_index()
        if file_index_id in w_npk_wrapper.index_lst:
            cout_error(LOG_CHANNEL, '[flush] flist_path:{} index id collision:{}'.format(npk_final_name, file_index_id))
            return False
        cout_info(LOG_CHANNEL, '[flush] add flist data:{}, flist num:{}'.format(npk_final_name, len(w_npk_wrapper.flist_lst)))
        flist_data = '\n'.join(w_npk_wrapper.flist_lst)
        flist_data = six.ensure_binary(flist_data)
        try:
            data_crc32 = zlib.crc32(flist_data)
        except Exception as e:
            other_err_log(LOG_CHANNEL, 'cal crc32 path:{} Except:{}'.format(npk_final_name, str(e)))
            return False

        if data_crc32 < 0:
            pkg_crc_sign = 0 if 1 else 1
            ret_size = w_npk_wrapper.w_npk.add_patch_data(file_index_id, flist_data, pkg_crc_sign, abs(data_crc32))
            if ret_size < 0:
                cout_error(LOG_CHANNEL, 'add flist data ret code:{} data len:{}'.format(ret_size, len(flist_data)))
                return False
            ret = w_npk_wrapper.w_npk.flush()
            if not ret:
                cout_error(LOG_CHANNEL, 'flush:{} ret:{}'.format(w_npk_wrapper.temp_name, ret))
                return False
            ret = self.verify_flushed_npk(w_npk_wrapper)
            ret or cout_error(LOG_CHANNEL, 'verify flushed npk failed!')
            return False
        tmp_file_path = os.path.join(self._root_dir, w_npk_wrapper.temp_name)
        final_file_path = os.path.join(self._root_dir, npk_final_name)
        try:
            cout_info(LOG_CHANNEL, 'rename:{} to {}'.format(tmp_file_path, final_file_path))
            os.rename(tmp_file_path, final_file_path)
        except Exception as e:
            cout_error(LOG_CHANNEL, 'rename {} Except:{}'.format(w_npk_wrapper.temp_name, str(e)))
            return False

        cout_info(LOG_CHANNEL, 'flush:{} success'.format(npk_final_name))
        return True

    def init_npk_file_info(self):
        exist_npk_name_set = set()
        ret, saved_npk_info = ext_pn_utils.get_saved_ext_patch_npk_info()
        if not ret:
            other_err_log(LOG_CHANNEL, '[init] get saved info failed!')
            return False
        else:
            try:
                if not os.path.exists(self._root_dir):
                    return False
                file_name_lst = os.listdir(self._root_dir)
            except Exception as e:
                other_err_log(LOG_CHANNEL, 'list dir except:{}'.format(str(e)))
                return False

            for file_name in file_name_lst:
                is_tmp = file_name.endswith('.npk.tmp') or file_name.endswith('_tmp.npk')
                if is_tmp:
                    try:
                        absolute_path = os.path.join(self._root_dir, file_name)
                        os.remove(absolute_path)
                    except Exception as e:
                        cout_error(LOG_CHANNEL, 'remove {} Except:{}'.format(file_name, str(e)))

                elif file_name.endswith('.npk'):
                    exist_npk_name_set.add(file_name)
                    continue

            def _remove_not_verified_npk(in_npk_name, in_npk_path):
                if not os.path.exists(in_npk_path):
                    return
                need_del = True
                if in_npk_name in saved_npk_info:
                    saved_size = saved_npk_info[in_npk_name].get('size', 0)
                    try:
                        real_size = os.path.getsize(in_npk_path)
                    except Exception as e:
                        cout_error('[patch_npk] get npk size except:{}'.format(str(e)))
                        return

                    if int(real_size) == int(saved_size):
                        need_del = False
                if need_del:
                    try:
                        os.remove(in_npk_path)
                        cout_error('[patch_npk] [init] remove info get failed npk:{} sz:{} real_sz:{}'.format(in_npk_name, saved_size, real_size))
                    except Exception as e:
                        cout_error('[patch_npk] [init] remove {} except:{}'.format(in_npk_path, str(e)))

            for file_name in exist_npk_name_set:
                file_path = os.path.join(self._root_dir, file_name)
                if not os.path.exists(file_path):
                    cout_error(LOG_CHANNEL, 'npk:{} not exists??'.format(file_path))
                    return False
                tmp_path = file_path[:-4]
                try:
                    nx_open_npk = package.nxnpk(tmp_path)
                    npk_size = os.path.getsize(file_path)
                except Exception as e:
                    nx_open_npk = None
                    _remove_not_verified_npk(file_name, file_path)
                    other_err_log(LOG_CHANNEL, 'open npk:{} except:{}'.format(file_name, str(e)))
                    return False

                try:
                    flist_dict, get_ret = ext_pn_utils.get_npk_flist_info(nx_open_npk, file_name)
                except Exception as e:
                    nx_open_npk = None
                    _remove_not_verified_npk(file_name, file_path)
                    other_err_log(LOG_CHANNEL, 'get npk flist except:{}'.format(str(e)))
                    return False

                if not get_ret:
                    nx_open_npk = None
                    _remove_not_verified_npk(file_name, file_path)
                    other_err_log(LOG_CHANNEL, 'get npk flist data is None:{}'.format(tmp_path))
                    return False
                cout_info(LOG_CHANNEL, 'npk:{} flist num:{}'.format(file_name, len(flist_dict)))
                self._exist_npk_info[file_name] = (npk_size, flist_dict)
                for file_index in flist_dict:
                    index_info = IS_RELEASE or nx_open_npk.get_file_index_info_by_id(file_index)
                    offset, compress_size, uncompress_size, compress_hash, uncompress_hash, compress_type = index_info
                    if compress_hash not in (0, 1):
                        nx_open_npk = None
                        cout_error(LOG_CHANNEL, '[song_test] compress_hash error:{}'.format(compress_hash))
                        return False
                    if compress_hash == 0:
                        pkg_crc = -uncompress_hash if 1 else uncompress_hash
                        flist_record_crc = int(flist_dict[file_index][3])
                        if pkg_crc != flist_record_crc:
                            nx_open_npk = None
                            cout_error(LOG_CHANNEL, '[song_test] pkg crc not equal:{} {}'.format(pkg_crc, flist_record_crc))
                            return False
                    self._idx_to_exist_npk_dict.setdefault(file_index, [])
                    npk_name_lst = self._idx_to_exist_npk_dict[file_index]
                    if file_name not in npk_name_lst:
                        npk_name_lst.append(file_name)
                    if len(npk_name_lst) > 1:
                        for npk_name in npk_name_lst:
                            self._duplicate_npk_set.add(npk_name)

                if self._duplicate_npk_set:
                    cout_info(LOG_CHANNEL, 'duplicate res npk:{}'.format(self._duplicate_npk_set))
                nx_open_npk = None

            return True

    def _verify_npk_failed(self, in_npk_path=None, in_error_msg=''):
        if in_npk_path and os.path.exists(in_npk_path):
            try:
                os.remove(in_npk_path)
            except Exception as e:
                in_error_msg += ' and remove failed npk except:{}'.format(str(e))

        if in_error_msg:
            other_err_log(LOG_CHANNEL, in_error_msg)
        self._w_npk_lst = []

    def verify_flushed_npk(self, npk_wrapper):
        nx_open_npk = None
        all_process_num = 0
        b_time = time.time()
        npk_name = npk_wrapper.temp_name
        file_path = os.path.join(self._root_dir, npk_name)
        if not os.path.exists(file_path):
            self._verify_npk_failed(None, '[verify] npk:{} not exists'.format(npk_name))
            return False
        else:
            tmp_path = file_path[:-4]
            try:
                nx_open_npk = package.nxnpk(tmp_path)
            except Exception as e:
                nx_open_npk = None
                self._verify_npk_failed(file_path, '[verify] open npk:{} except:{}'.format(npk_name, str(e)))
                return False

            flist_npk_name = npk_wrapper.get_flist_npk_name()
            saved_flist_dict, get_ret = ext_pn_utils.get_npk_flist_info(nx_open_npk, flist_npk_name)
            if not get_ret:
                nx_open_npk = None
                self._verify_npk_failed(file_path, '[verify] get flist info false:{}'.format(npk_name))
                return False
            all_flist_dict = npk_wrapper.flist_dict
            for index_id in all_flist_dict:
                all_process_num += 1
                if index_id not in saved_flist_dict:
                    nx_open_npk = None
                    self._verify_npk_failed(file_path, '[verify] saved flist_dict not contains index_id:{}'.format(index_id))
                    return False
                check_crc = all_flist_dict[index_id]
                ret_code = nx_open_npk.check_data_crc_by_id(index_id, check_crc)
                if ret_code <= 0:
                    nx_open_npk = None
                    error_msg = '[verify] check_data_crc failed:{}, ret code:{}'.format(npk_name, ret_code)
                    self._verify_npk_failed(file_path, error_msg)
                    return False

            nx_open_npk = None
            cout_info(LOG_CHANNEL, '[verify] verify:{} cost time:{}'.format(all_process_num, time.time() - b_time))
            return True

    def _get_nx_npk_path(self, file_name):
        file_path = os.path.join(self._root_dir, file_name)
        tmp_path = file_path[:-4]
        return (
         tmp_path, file_path)

    def destroy(self):
        self._removed_npk_set = set()
        self._exist_npk_info = {}
        self._idx_to_exist_npk_dict = {}
        self._w_npk_lst = []
        self._duplicate_npk_set = set()
        self._all_new_idx_set = set()
        self._new_flist_map = {}
        self._local_npk_flist_map = {}
        self._root_dir = ext_pn_utils.get_ext_patch_npk_dir()

    @staticmethod
    def get_record_crc_in_index_info(nx_open_npk, file_index):
        index_info = nx_open_npk.get_file_index_info_by_id(file_index)
        if index_info is None:
            return (None, True)
        else:
            offset, compress_size, uncompress_size, compress_hash, uncompress_hash, compress_type = index_info
            if compress_hash not in (0, 1):
                return (None, True)
            pkg_crc = -uncompress_hash if compress_hash == 0 else uncompress_hash
            return (
             pkg_crc, False)