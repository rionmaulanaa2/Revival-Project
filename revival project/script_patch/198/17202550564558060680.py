# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_npk.py
from __future__ import absolute_import
from __future__ import print_function
import os
import json
import zlib
import time
import C_file
import game3d
import package
from . import pn_utils
from . import patch_path
from . import patch_utils
from patch import patch_const
from .patch_log import log_error, cout_info
import six
LOG_C = 'patch_npk'
LOADER_TAG = 'patch_npk'
SCRIPT_LOADER_TAG = 'script_patch_npk'
TEMP_RES_NPK_PATTERN = 'p_res_{}_tmp.npk'
TEMP_SCRIPT_NPK_PATTERN = 'p_script_{}_tmp.npk'
W_NPK_STATE_FLUSHED = 1
W_NPK_STATE_WRITABLE = 0
IS_RELEASE = game3d.is_release_version()

def count_info(msg):
    print('[INFO]', msg)


def get_patch_const_bool(attribute_name, default_ret=False):
    if hasattr(patch_const, attribute_name):
        return getattr(patch_const, attribute_name)
    else:
        return default_ret


class WriteNpkWrapper(object):

    def __init__(self, in_w_npk, in_temp_name, in_final_name, in_is_script):
        super(WriteNpkWrapper, self).__init__()
        self.w_npk = in_w_npk
        self.npk_size = 0
        self.temp_name = in_temp_name
        self.final_name = in_final_name
        self.npk_state = W_NPK_STATE_WRITABLE
        self.flist_lst = []
        self.flist_dict = {}
        self.index_lst = []
        self.is_script = in_is_script

    def get_flist_npk_name(self):
        flist_npk_name = pn_utils.PN_SCRIPT_NAME if self.is_script else self.final_name
        return flist_npk_name

    def get_flist_index(self):
        flist_npk_name = self.get_flist_npk_name()
        return pn_utils.get_patch_npk_flist_file_id(flist_npk_name)


class PatchNpkProcessor(object):

    def __init__(self, err_queue):
        super(PatchNpkProcessor, self).__init__()
        self._remove_res_npk_set = set()
        self._exist_npk_info = {}
        self._idx_to_exist_res_npk_dict = {}
        self._patch_version = 0
        self._err_queue = err_queue
        self._w_npk_lst = [None, []]
        self._duplicate_res_npk_set = set()
        self._all_new_res_idx_set = set()
        self._all_new_script_idx_set = set()
        self._new_flist_map = {}
        self._base_npk_flist_map = {}
        self._enable_local_flist = get_patch_const_bool('ENABLE_LOCAL_FLIST')
        self._root_dir = pn_utils.get_patch_npk_dir()
        return

    def is_file_in_patch_npk(self, f_path, pkg_crc, is_script):
        if not self._exist_npk_info:
            return False
        else:
            if not self._enable_local_flist and f_path == 'res/confs/version.json':
                return False
            file_index_id = patch_path.get_patch_file_hash(f_path)
            if file_index_id is None:
                return False
            for npk_name in self._exist_npk_info:
                if is_script and npk_name != pn_utils.PN_SCRIPT_NAME:
                    continue
                flist_dict = self._exist_npk_info[npk_name][1]
                if file_index_id in flist_dict:
                    record_pkg_crc = int(flist_dict[file_index_id][3])
                    if record_pkg_crc == pkg_crc:
                        return True
                    if npk_name in self._duplicate_res_npk_set:
                        continue
                    else:
                        return False

            return False

    def set_patch_version(self, patch_version):
        self._patch_version = patch_version

    def set_new_flist_map(self, new_map):
        self._new_flist_map = new_map

    def set_base_npk_flist_map(self, in_local_npk_map):
        self._base_npk_flist_map = in_local_npk_map

    def add_patch_data(self, file_type, src_data, index_id, pkg_crc, in_finfo):
        if pkg_crc < 0:
            pkg_crc_sign = 0 if 1 else 1
            if not self._prepare_npk_writer(file_type):
                return False
            if file_type == patch_path.RES_TYPE:
                all_new_idx = self._all_new_res_idx_set
                npk_wrapper = self._w_npk_lst[1][-1]
                need_limit_size = True
                force_no_compress = False
            else:
                all_new_idx = self._all_new_script_idx_set
                npk_wrapper = self._w_npk_lst[0]
                need_limit_size = False
                force_no_compress = True
            if index_id in all_new_idx:
                if self._err_queue:
                    self._err_queue.put('[patch_npk] add patch data index collision: {} {}'.format(index_id, in_finfo))
                return False
            ret_size = npk_wrapper.w_npk.add_patch_data(index_id, src_data, pkg_crc_sign, abs(pkg_crc), force_no_compress)
            if ret_size < 0:
                log_error('[patch_npk] add patch data failed, ret code: {}'.format(ret_size))
                return False
            all_new_idx.add(index_id)
            npk_wrapper.flist_lst.append('{}\t{}\t{}\t{}'.format(index_id, in_finfo[0], in_finfo[1], in_finfo[2]))
            npk_wrapper.flist_dict[index_id] = (in_finfo[0], int(in_finfo[1]), int(in_finfo[2]))
            npk_wrapper.index_lst.append(index_id)
            npk_wrapper.npk_size += ret_size
            if need_limit_size and npk_wrapper.npk_size >= pn_utils.MAX_NPK_SIZE:
                flush_ret = self._npk_flush(npk_wrapper)
                flush_ret or log_error('[patch_npk] npk flush failed in add patch data')
                return False
            npk_wrapper.npk_state = W_NPK_STATE_FLUSHED
        return True

    def _add_old_npk_data_to_new(self, file_type, index_id, npk_reader, f_info):
        if not self._prepare_npk_writer(file_type):
            return (False, False)
        if file_type == patch_path.RES_TYPE:
            npk_wrapper = self._w_npk_lst[1][-1]
            need_limit_size = True
        else:
            npk_wrapper = self._w_npk_lst[0]
            need_limit_size = False
        if index_id in npk_wrapper.index_lst:
            if self._err_queue:
                self._err_queue.put('[patch_npk] index id duplication:{} {} {}'.format(index_id, npk_wrapper.temp_name, f_info[1]))
            return (False, False)
        ret_size = npk_wrapper.w_npk.add_npk_data_v2(index_id, npk_reader)
        if ret_size < 0:
            log_error('[patch_npk] add npk data failed, ret code: {}'.format(ret_size))
            return (
             False, False)
        npk_wrapper.index_lst.append(index_id)
        npk_wrapper.flist_lst.append('\t'.join(f_info))
        npk_wrapper.flist_dict[index_id] = (f_info[1], int(f_info[2]), int(f_info[3]))
        npk_wrapper.npk_size += ret_size
        if need_limit_size and npk_wrapper.npk_size >= pn_utils.MAX_NPK_SIZE:
            flush_ret = self._npk_flush(npk_wrapper)
            if not flush_ret:
                log_error('[patch_npk] npk flush failed in add npk data')
                return (
                 False, False)
            npk_wrapper.npk_state = W_NPK_STATE_FLUSHED
            return (
             flush_ret, True)
        return (True, False)

    def update_and_flush_all_npk(self, update_prog_func=None):
        b_time = time.time()
        has_new_script_npk = self._w_npk_lst[0] is not None
        has_new_res_npk = len(self._w_npk_lst[1]) > 0
        cout_info(LOG_C, '[update_and_flush_all] new script:{} new res:{}'.format(has_new_script_npk, has_new_res_npk))
        need_up_npk = set()
        for npk_name in self._duplicate_res_npk_set:
            need_up_npk.add(npk_name)

        for index_id in self._all_new_res_idx_set:
            if index_id in self._idx_to_exist_res_npk_dict:
                for hit_npk_name in self._idx_to_exist_res_npk_dict[index_id]:
                    need_up_npk.add(hit_npk_name)

        all_old_script_npk = set()
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
                        cout_info(LOG_C, 'need tidy:{} for no need res'.format(npk_file_name))
                        need_up_npk.add(npk_file_name)
                        break
                    elif int(self._new_flist_map[f_path][2]) != int(f_info[3]):
                        cout_info(LOG_C, 'need tidy:{} for old res'.format(npk_file_name))
                        need_up_npk.add(npk_file_name)
                        break

            if not npk_file_name.startswith(pn_utils.PN_SCRIPT_PREFIX):
                npk_size = self._exist_npk_info[npk_file_name][0]
                if npk_size < pn_utils.MAX_NPK_SIZE:
                    all_old_small_res_npk.add(npk_file_name)
            else:
                all_old_script_npk.add(npk_file_name)

        if has_new_res_npk or need_up_npk or len(all_old_small_res_npk) > 1:
            need_up_npk.update(all_old_small_res_npk)
        if has_new_script_npk or len(all_old_script_npk) > 1:
            need_tidy_script = True
        elif len(all_old_script_npk) == 1 and pn_utils.PN_SCRIPT_NAME not in all_old_script_npk:
            need_tidy_script = True
        else:
            need_tidy_script = False
        if need_tidy_script:
            need_up_npk.update(all_old_script_npk)
        cout_info(LOG_C, 'need up npk:{} need tidy script:{}'.format(need_up_npk, need_tidy_script))
        C_file.unload_fileloader(LOADER_TAG)
        C_file.unload_fileloader(SCRIPT_LOADER_TAG)
        all_process_num = 1
        processed_num = 0
        if update_prog_func is not None:
            for up_npk_name in need_up_npk:
                flist_dict = self._exist_npk_info[up_npk_name][1]
                all_process_num += len(flist_dict)

        processed_npk_lst = []
        if get_patch_const_bool('ENABLE_CHECK_BASE_NPK') and hasattr(patch_utils, 'get_base_npk_flist_dict'):
            if self._base_npk_flist_map:
                base_npk_flist_dict = self._base_npk_flist_map
            else:
                base_npk_flist_dict, base_flist_ret = patch_utils.get_base_npk_flist_dict()
        else:
            base_npk_flist_dict = {}
        for up_npk_name in need_up_npk:
            cout_info(LOG_C, 'processing old npk:{}'.format(up_npk_name))
            py_npk_path, abs_real_path = self._get_nx_npk_path(up_npk_name)
            try:
                nx_open_npk = package.nxnpk(py_npk_path)
            except Exception as e:
                if self._err_queue:
                    self._err_queue.put('[patch_npk] open npk except: {} {}'.format(up_npk_name, str(e)))
                return False

            npk_org_flist_dict = self._exist_npk_info[up_npk_name][1]
            flist_index = pn_utils.get_patch_npk_flist_file_id(up_npk_name)
            if up_npk_name.startswith(pn_utils.PN_SCRIPT_PREFIX):
                file_type = patch_path.SCRIPT_TYPE
                all_new_idx_set = self._all_new_script_idx_set
                need_check_base_npk = False
            else:
                file_type = patch_path.RES_TYPE
                all_new_idx_set = self._all_new_res_idx_set
                need_check_base_npk = True
            for index_id in npk_org_flist_dict:
                processed_num += 1
                if update_prog_func is not None:
                    update_prog_func(processed_num * 1.0 / all_process_num)
                if index_id in all_new_idx_set or index_id == flist_index:
                    continue
                else:
                    f_info = npk_org_flist_dict[index_id]
                    f_path = f_info[1]
                    org_crc_in_npk = int(f_info[2])
                    if self._new_flist_map:
                        if f_path not in self._new_flist_map:
                            cout_info(LOG_C, 'not in new flist, ignore:{}'.format(f_path))
                            continue
                        elif int(self._new_flist_map[f_path][2]) != int(f_info[3]):
                            cout_info(LOG_C, 'file: {} is old in {} for pkg crc'.format(f_path, up_npk_name))
                            continue
                        elif int(self._new_flist_map[f_path][1]) != org_crc_in_npk:
                            cout_info(LOG_C, 'file: pkg equal, org not equal{}, in {}'.format(f_path, up_npk_name))
                    if need_check_base_npk and f_path in base_npk_flist_dict and org_crc_in_npk == int(base_npk_flist_dict[f_path][1]):
                        cout_info(LOG_C, 'res file exists in base npk: {}'.format(f_path))
                        continue
                    ret, flushed = self._add_old_npk_data_to_new(file_type, index_id, nx_open_npk, f_info)
                    if not ret:
                        return False
                    all_new_idx_set.add(index_id)
                    if flushed:
                        self._remove_old_npk(processed_npk_lst)
                        processed_npk_lst = []

            nx_open_npk = None
            cout_info(LOG_C, 'processing old npk done')
            if up_npk_name != pn_utils.PN_SCRIPT_NAME:
                processed_npk_lst.append(up_npk_name)

        for npk_wrapper in self._w_npk_lst[1]:
            if npk_wrapper.npk_state != W_NPK_STATE_FLUSHED:
                flush_ret = self._npk_flush(npk_wrapper)
                if not flush_ret:
                    log_error('[patch_npk] flush not success')
                    return False

        self._remove_old_npk(processed_npk_lst)
        npk_wrapper = self._w_npk_lst[0]
        if npk_wrapper and npk_wrapper.npk_state != W_NPK_STATE_FLUSHED:
            flush_ret = self._npk_flush(npk_wrapper)
            if not flush_ret:
                log_error('[patch_npk] flush script not success')
                return False
            final_path = os.path.join(self._root_dir, npk_wrapper.final_name)
            if not os.path.exists(final_path):
                if self._err_queue:
                    self._err_queue.put('[patch_npk] script npk flush success but not exists')
                return False
            final_script_path = os.path.join(self._root_dir, pn_utils.PN_SCRIPT_NAME)
            try:
                if os.path.exists(final_script_path):
                    os.remove(final_script_path)
                cout_info(LOG_C, 'remove old script npk Done')
            except Exception as e:
                if self._err_queue:
                    self._err_queue.put('[patch_npk] [except] remove p_script.npk except:{}'.format(str(e)))
                return False

            try:
                os.rename(final_path, final_script_path)
                cout_info(LOG_C, 'rename new script npk Done')
            except Exception as e:
                if self._err_queue:
                    self._err_queue.put('[patch_npk] [except] rename to p_script.npk except:{}'.format(str(e)))
                return False

        cout_info(LOG_C, '[update_and_flush_all] process:{} cost time:{}'.format(all_process_num, time.time() - b_time))
        if hasattr(patch_utils, 'del_tidy_patch_npk_flag'):
            patch_utils.del_tidy_patch_npk_flag()
        return True

    def _remove_old_npk(self, remove_lst):
        for processed_npk_name in remove_lst:
            up_npk_path = os.path.join(self._root_dir, processed_npk_name)
            try:
                os.remove(up_npk_path)
            except Exception as e:
                print('[Except] [patch_npk] remove:{} except:{}'.format(processed_npk_name, str(e)))

            self._remove_res_npk_set.add(processed_npk_name)

        remove_lst = []

    def verify_and_save_new_npk_info(self, update_prog_func=None):
        all_npk_name_lst = set()
        for npk_name in self._exist_npk_info:
            if npk_name not in self._remove_res_npk_set:
                all_npk_name_lst.add(npk_name)

        for npk_wrapper in self._w_npk_lst[1]:
            all_npk_name_lst.add(npk_wrapper.final_name)

        if self._w_npk_lst[0]:
            all_npk_name_lst.add(pn_utils.PN_SCRIPT_NAME)
        new_info = {}
        for npk_name in all_npk_name_lst:
            npk_path = os.path.join(self._root_dir, npk_name)
            try:
                if not os.path.exists(npk_path):
                    log_error('[patch_npk] [save_npk_info] npk not exists:{}'.format(npk_path))
                    return False
                npk_size = os.path.getsize(npk_path)
            except Exception as e:
                self._err_queue.put('[patch_npk] [save_npk_info] except: {} {}'.format(npk_name, str(e)))
                self._w_npk_lst = [None, []]
                return False

            new_info.setdefault(npk_name, {})
            new_info[npk_name]['size'] = npk_size

        save_ret, error_str = pn_utils.save_patch_npk_info(new_info)
        if not save_ret:
            log_error('[patch_npk] save npk info except:{}'.format(error_str))
            self._w_npk_lst = [None, []]
            return False
        else:
            self._w_npk_lst = [
             None, []]
            return True

    def _prepare_npk_writer(self, file_type):
        if file_type == patch_path.SCRIPT_TYPE:
            if self._w_npk_lst[0] is None:
                w_npk = package.npkwriter()
                tmp_name, final_name = self._generate_new_npk_name(True)
                w_npk_file_path = os.path.join(self._root_dir, tmp_name)
                ret = w_npk.open(w_npk_file_path, 0)
                if not ret:
                    log_error('[patch_npk] open write npk failed:{}'.format(tmp_name))
                    return False
                self._w_npk_lst[0] = WriteNpkWrapper(w_npk, tmp_name, final_name, True)
        else:
            if not self._w_npk_lst[1]:
                if not self._add_new_npk_writer():
                    return False
            if self._w_npk_lst[1][-1].npk_state != W_NPK_STATE_WRITABLE:
                if not self._add_new_npk_writer():
                    return False
        return True

    def _add_new_npk_writer(self):
        new_tmp_file_name, new_final_file_name = self._generate_new_npk_name(False)
        w_npk_path = os.path.join(self._root_dir, new_tmp_file_name)
        w_npk = package.npkwriter()
        ret = w_npk.open(w_npk_path, 0)
        if ret:
            self._w_npk_lst[-1].append(WriteNpkWrapper(w_npk, new_tmp_file_name, new_final_file_name, False))
        else:
            log_error('[patch_npk] open write res npk failed:{}'.format(new_tmp_file_name))
        return ret

    def _generate_new_npk_name(self, is_script):
        b_num = 1
        final_pattern = pn_utils.SCRIPT_NPK_SUBFIX_PATTERN if is_script else pn_utils.RES_NPK_SUBFIX_PATTERN
        temp_pattern = TEMP_SCRIPT_NPK_PATTERN if is_script else TEMP_RES_NPK_PATTERN
        while True:
            final_file_name = final_pattern.format(b_num)
            tmp_file_name = temp_pattern.format(b_num)
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
        cout_info(LOG_C, '[flush] add flist to npk:{}, flist num:{}'.format(npk_final_name, len(w_npk_wrapper.flist_lst)))
        if file_index_id in w_npk_wrapper.index_lst:
            if self._err_queue:
                self._err_queue.put('[patch_npk] [flush] flist_path:{} index id collision:{}'.format(npk_final_name, file_index_id))
            return False
        flist_data = '\n'.join(w_npk_wrapper.flist_lst)
        flist_data = six.ensure_binary(flist_data)
        try:
            data_crc32 = zlib.crc32(flist_data)
        except Exception as e:
            if self._err_queue:
                self._err_queue.put('[patch_npk] cal crc32 path:{} Except:{}'.format(npk_final_name, str(e)))
            return False

        if data_crc32 < 0:
            pkg_crc_sign = 0 if 1 else 1
            ret_size = w_npk_wrapper.w_npk.add_patch_data(file_index_id, flist_data, pkg_crc_sign, abs(data_crc32))
            if ret_size < 0:
                log_error('[patch_npk] add flist data ret code:{} data len:{}'.format(ret_size, len(flist_data)))
                return False
            ret = w_npk_wrapper.w_npk.flush()
            if not ret:
                log_error('[patch_npk] flush:{} ret:{}'.format(w_npk_wrapper.temp_name, ret))
                return False
            ret = self.verify_flushed_npk(w_npk_wrapper)
            ret or log_error('[patch_npk] verify flushed npk failed!')
            return False
        tmp_file_path = os.path.join(self._root_dir, w_npk_wrapper.temp_name)
        final_file_path = os.path.join(self._root_dir, npk_final_name)
        try:
            cout_info(LOG_C, 'rename:{} to {}'.format(tmp_file_path, final_file_path))
            os.rename(tmp_file_path, final_file_path)
        except Exception as e:
            log_error('[patch_npk] rename {} Except:{}'.format(w_npk_wrapper.temp_name, str(e)))
            return False

        cout_info(LOG_C, 'flush:{} success'.format(npk_final_name))
        return True

    def init_npk_file_info(self):
        exist_npk_name_set = set()
        ret, saved_npk_info = pn_utils.get_saved_patch_npk_info()
        if not ret:
            if self._err_queue:
                self._err_queue.put('[patch_npk] [init] get saved info failed!')
            return False
        else:
            try:
                if not os.path.exists(self._root_dir):
                    return False
                file_name_lst = os.listdir(self._root_dir)
            except Exception as e:
                if self._err_queue:
                    self._err_queue.put('[patch_npk] list dir [init] except:{}'.format(str(e)))
                return False

            script_npk_exist = pn_utils.PN_SCRIPT_NAME in file_name_lst
            for file_name in file_name_lst:
                is_tmp = file_name.endswith('.npk.tmp') or file_name.endswith('_tmp.npk')
                if is_tmp:
                    try:
                        absolute_path = os.path.join(self._root_dir, file_name)
                        os.remove(absolute_path)
                    except Exception as e:
                        log_error('[patch_npk] remove {} Except:{}'.format(file_name, str(e)))

                elif file_name.endswith('.npk'):
                    if file_name.startswith(pn_utils.PN_SCRIPT_PREFIX) and file_name != pn_utils.PN_SCRIPT_NAME and script_npk_exist:
                        try:
                            absolute_path = os.path.join(self._root_dir, file_name)
                            os.remove(absolute_path)
                        except Exception as e:
                            log_error('[patch_npk] remove {} Except:{}'.format(file_name, str(e)))

                        cout_info(LOG_C, '[init_info] del script tmp:{}'.format(file_name))
                        continue
                    exist_npk_name_set.add(file_name)

            def _remove_not_verified_npk(in_npk_name, in_npk_path):
                if not os.path.exists(in_npk_path):
                    return
                need_del = True
                if in_npk_name in saved_npk_info:
                    saved_size = saved_npk_info[in_npk_name].get('size', 0)
                    try:
                        real_size = os.path.getsize(in_npk_path)
                    except Exception as e:
                        log_error('[patch_npk] get npk size except:{}'.format(str(e)))
                        return

                    if int(real_size) == int(saved_size):
                        need_del = False
                if need_del:
                    try:
                        os.remove(in_npk_path)
                        count_info('[patch_npk] [init] remove info get failed npk:{} sz:{} real_sz:{}'.format(in_npk_name, saved_size, real_size))
                    except Exception as e:
                        log_error('[patch_npk] [init] remove {} except:{}'.format(in_npk_path, str(e)))

            for file_name in exist_npk_name_set:
                file_path = os.path.join(self._root_dir, file_name)
                if not os.path.exists(file_path):
                    log_error('[patch_npk] npk:{} not exists??'.format(file_path))
                    return False
                tmp_path = file_path[:-4]
                try:
                    nx_open_npk = package.nxnpk(tmp_path)
                    npk_size = os.path.getsize(file_path)
                except Exception as e:
                    nx_open_npk = None
                    _remove_not_verified_npk(file_name, file_path)
                    if self._err_queue:
                        self._err_queue.put('[patch_npk] open npk:{} except:{}'.format(file_name, str(e)))
                    return False

                try:
                    flist_dict, get_ret = pn_utils.get_npk_flist_info(nx_open_npk, file_name)
                except Exception as e:
                    nx_open_npk = None
                    _remove_not_verified_npk(file_name, file_path)
                    if self._err_queue:
                        self._err_queue.put('[patch_npk] get npk flist except:{}'.format(str(e)))
                    return False

                if not get_ret:
                    nx_open_npk = None
                    _remove_not_verified_npk(file_name, file_path)
                    if self._err_queue:
                        self._err_queue.put('[patch_npk] get npk flist data is None: {}'.format(file_name))
                    return False
                cout_info(LOG_C, 'npk:{} flist num:{}'.format(file_name, len(flist_dict)))
                self._exist_npk_info[file_name] = (npk_size, flist_dict)
                if not file_name.startswith(pn_utils.PN_SCRIPT_PREFIX):
                    for file_index in flist_dict:
                        index_info = IS_RELEASE or nx_open_npk.get_file_index_info_by_id(file_index)
                        offset, compress_size, uncompress_size, compress_hash, uncompress_hash, compress_type = index_info
                        if compress_hash not in (0, 1):
                            nx_open_npk = None
                            log_error('[patch_npk] [song_test] compress_hash error:{}'.format(compress_hash))
                            return False
                        if compress_hash == 0:
                            pkg_crc = -uncompress_hash if 1 else uncompress_hash
                            flist_record_crc = int(flist_dict[file_index][3])
                            if pkg_crc != flist_record_crc:
                                nx_open_npk = None
                                log_error('[patch_npk] [song_test] pkg crc not equal:{} {}'.format(pkg_crc, flist_record_crc))
                                return False
                        self._idx_to_exist_res_npk_dict.setdefault(file_index, [])
                        npk_name_lst = self._idx_to_exist_res_npk_dict[file_index]
                        if file_name not in npk_name_lst:
                            npk_name_lst.append(file_name)
                        if len(npk_name_lst) > 1:
                            for npk_name in npk_name_lst:
                                if npk_name not in self._duplicate_res_npk_set:
                                    self._duplicate_res_npk_set.add(npk_name)

                nx_open_npk = None

            if self._duplicate_res_npk_set:
                cout_info(LOG_C, 'duplicate res npk:{}'.format(self._duplicate_res_npk_set))
            return True

    def _verify_npk_failed(self, in_npk_path=None, in_error_msg=''):
        if in_npk_path and os.path.exists(in_npk_path):
            try:
                os.remove(in_npk_path)
            except Exception as e:
                in_error_msg += ' and remove failed npk except:{}'.format(str(e))

        if in_error_msg:
            log_error(in_error_msg)
            if self._err_queue:
                self._err_queue.put(in_error_msg)
        self._w_npk_lst = []

    def verify_flushed_npk(self, npk_wrapper):
        all_process_num = 0
        b_time = time.time()
        nx_open_npk = None
        is_script = npk_wrapper.is_script
        crc_index_in_flist = 2 if is_script else 1
        tmp_npk_name = npk_wrapper.temp_name
        file_path = os.path.join(self._root_dir, tmp_npk_name)
        cout_info(LOG_C, '[verify_npk] verify:{}'.format(tmp_npk_name))
        if not os.path.exists(file_path):
            self._verify_npk_failed(None, '[patch_npk] [verify] npk:{} not exists'.format(file_path))
            return False
        else:
            tmp_path = file_path[:-4]
            try:
                nx_open_npk = package.nxnpk(tmp_path)
            except Exception as e:
                nx_open_npk = None
                self._verify_npk_failed(file_path, '[patch_npk] [verify] open npk:{} except:{}'.format(tmp_npk_name, str(e)))
                return False

            flist_npk_name = npk_wrapper.get_flist_npk_name()
            saved_flist_dict, get_ret = pn_utils.get_npk_flist_info(nx_open_npk, flist_npk_name)
            if not get_ret:
                nx_open_npk = None
                self._verify_npk_failed(file_path, '[patch_npk] [verify] get flist info false:{}'.format(tmp_npk_name))
                return False
            all_flist_dict = npk_wrapper.flist_dict
            for index_id in all_flist_dict:
                all_process_num += 1
                if index_id not in saved_flist_dict:
                    nx_open_npk = None
                    self._verify_npk_failed(file_path, '[patch_npk] [verify] saved flist_dict not contains index_id:{}'.format(index_id))
                    return False
                name_in_flist = all_flist_dict[index_id][0]
                if name_in_flist == 'res/confs/version.json':
                    check_crc = all_flist_dict[index_id][2]
                else:
                    check_crc = all_flist_dict[index_id][crc_index_in_flist]
                ret_code = nx_open_npk.check_data_crc_by_id(index_id, check_crc)
                if ret_code <= 0:
                    file_data = nx_open_npk.get_file_by_id(index_id)
                    data_crc = zlib.crc32(file_data)
                    erro_msg = '[patch_npk] check_data_crc failed:{}, ret_code:{} file_name:{} get_crc:{} check_crc:{}'.format(tmp_npk_name, ret_code, name_in_flist, data_crc, check_crc)
                    nx_open_npk = None
                    self._verify_npk_failed(file_path, erro_msg)
                    return False

            nx_open_npk = None
            cout_info(LOG_C, '[verify_npk] verify suc:{} cost time:{}'.format(all_process_num, time.time() - b_time))
            return True

    def _get_nx_npk_path(self, file_name):
        file_path = os.path.join(self._root_dir, file_name)
        tmp_path = file_path[:-4]
        return (
         tmp_path, file_path)

    def destroy(self):
        self._remove_res_npk_set = set()
        self._exist_npk_info = {}
        self._idx_to_exist_res_npk_dict = {}
        self._patch_version = 0
        self._err_queue = None
        self._w_npk_lst = [None, []]
        self._all_new_res_idx_set = set()
        self._all_new_script_idx_set = set()
        self._new_flist_map = {}
        self._base_npk_flist_map = {}
        self._duplicate_res_npk_set = set()
        return

    @staticmethod
    def get_record_crc_in_index_info(nx_open_npk, file_index):
        index_info = nx_open_npk.get_file_index_info_by_id(file_index)
        if index_info is None:
            return (None, False)
        else:
            offset, compress_size, uncompress_size, compress_hash, uncompress_hash, compress_type = index_info
            if compress_hash not in (0, 1):
                return (None, True)
            pkg_crc = -uncompress_hash if compress_hash == 0 else uncompress_hash
            return (
             pkg_crc, False)

    def simple_check(self):
        info_path = pn_utils.get_patch_npk_info_file_path()
        if not os.path.exists(info_path):
            return (True, False)
        try:
            with open(info_path, 'rb') as tmp_file:
                info_data = tmp_file.read()
                info = json.loads(zlib.decompress(info_data))
                for npk_name in info:
                    npk_path = os.path.join(self._root_dir, npk_name)
                    record_size = int(info[npk_name].get('size', 0))
                    if os.path.exists(npk_path):
                        real_size = os.path.getsize(npk_path)
                        if int(real_size) != record_size:
                            print('[patch_npk] size not match:{} {} {}'.format(npk_name, record_size, real_size))
                            return (
                             False, False)
                    else:
                        print('[patch_npk] npk:{} recorded but not exist'.format(npk_name))
                        return (
                         False, False)

            return (
             True, False)
        except Exception as e:
            self._err_queue.put('[patch_npk] read patch npk info except:{}'.format(str(e)))
            return (
             False, True)