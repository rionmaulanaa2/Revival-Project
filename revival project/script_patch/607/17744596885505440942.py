# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/nx_file_logic/physx_cook_npk.py
from __future__ import absolute_import
from __future__ import print_function
import six
import os
import zlib
import json
import C_file
import game3d
import package
import shutil
from patch import patch_path
NX_DIR = patch_path.get_neox_dir()
PHYSX_COOK_NPK_TAG = 'physx_cook_npk'
PHYSX_DATA_PATH = os.path.join(NX_DIR, 'physx_data')
LEN_RES_PREFIX = len(patch_path.RES_PREFIX)

def cal_file_id(file_path):
    target_relative_path = file_path.replace('/', '\\')
    return game3d.calc_filename_hash64(target_relative_path)


def log_error(in_msg):
    print('[ERROR] [physx_cook_npk]: {}'.format(in_msg))


def log_except(in_msg):
    print('[EXCEPT] [physx_cook_npk]: {}'.format(in_msg))


def cout_info(in_msg):
    print('[INFO] [physx_cook_npk]: {}'.format(in_msg))


def get_physx_saved_flist_path():
    return os.path.join(PHYSX_DATA_PATH, 'last_info_new.lst')


def get_physx_saved_flist_data--- This code section failed: ---

  48       0  LOAD_GLOBAL           0  'get_physx_saved_flist_path'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            0  'flist_path'

  49       9  LOAD_GLOBAL           1  'os'
          12  LOAD_ATTR             2  'path'
          15  LOAD_ATTR             3  'exists'
          18  LOAD_FAST             0  'flist_path'
          21  CALL_FUNCTION_1       1 
          24  POP_JUMP_IF_TRUE     37  'to 37'

  50      27  LOAD_GLOBAL           4  'True'
          30  BUILD_MAP_0           0 
          33  BUILD_TUPLE_2         2 
          36  RETURN_END_IF    
        37_0  COME_FROM                '24'

  51      37  SETUP_EXCEPT         65  'to 105'

  52      40  LOAD_GLOBAL           5  'open'
          43  LOAD_GLOBAL           1  'os'
          46  CALL_FUNCTION_2       2 
          49  SETUP_WITH           19  'to 71'
          52  STORE_FAST            1  'tmp_file'

  53      55  LOAD_FAST             1  'tmp_file'
          58  LOAD_ATTR             6  'read'
          61  CALL_FUNCTION_0       0 
          64  STORE_FAST            2  'r_data'
          67  POP_BLOCK        
          68  LOAD_CONST            0  ''
        71_0  COME_FROM_WITH           '49'
          71  WITH_CLEANUP     
          72  END_FINALLY      

  54      73  LOAD_GLOBAL           4  'True'
          76  LOAD_GLOBAL           7  'json'
          79  LOAD_ATTR             8  'loads'
          82  LOAD_GLOBAL           9  'zlib'
          85  LOAD_ATTR            10  'decompress'
          88  LOAD_FAST             2  'r_data'
          91  CALL_FUNCTION_1       1 
          94  CALL_FUNCTION_1       1 
          97  BUILD_TUPLE_2         2 
         100  RETURN_VALUE     
         101  POP_BLOCK        
         102  JUMP_FORWARD         45  'to 150'
       105_0  COME_FROM                '37'

  55     105  DUP_TOP          
         106  LOAD_GLOBAL          11  'Exception'
         109  COMPARE_OP           10  'exception-match'
         112  POP_JUMP_IF_FALSE   149  'to 149'
         115  POP_TOP          
         116  STORE_FAST            3  'e'
         119  POP_TOP          

  56     120  LOAD_GLOBAL          12  'print'
         123  LOAD_CONST            2  '[Except] [physx_cook_npk] get flist data error:{}'
         126  LOAD_ATTR            13  'format'
         129  LOAD_FAST             3  'e'
         132  CALL_FUNCTION_1       1 
         135  CALL_FUNCTION_1       1 
         138  POP_TOP          

  57     139  LOAD_GLOBAL          14  'False'
         142  BUILD_MAP_0           0 
         145  BUILD_TUPLE_2         2 
         148  RETURN_VALUE     
         149  END_FINALLY      
       150_0  COME_FROM                '149'
       150_1  COME_FROM                '102'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 46


def save_physx_flist_data(in_dict_data):
    try:
        flist_path = get_physx_saved_flist_path()
        dir_path = os.path.dirname(flist_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(flist_path, 'wb') as tmp_f:
            tmp_f.write(six.ensure_binary(zlib.compress(six.ensure_binary(json.dumps(in_dict_data)))))
    except Exception as e:
        log_except('save flist data error:{}'.format(e))


class PhysxCookNpkProcessor(object):

    def __init__(self):
        super(PhysxCookNpkProcessor, self).__init__()
        self._npk_file_path = os.path.join(PHYSX_DATA_PATH, 'physx_cook.npk')
        self._temp_npk_file_name = self._npk_file_path.replace('.npk', '_temp.npk')
        self._discrete_path = os.path.join(NX_DIR, 'res/physxcook')
        self._met_error = False
        self._old_npk_flist_dict = {}
        self._saved_flist_data = {}
        self._outdate_id_set = set()

    def can_enable_cook(self):
        return not self._met_error

    def process(self, new_flist):
        self._pre_init()
        if self._met_error:
            return False
        else:
            self._init_npk_info()
            if self._met_error:
                return False
            for file_name in self._saved_flist_data:
                need_delete = False
                if file_name not in new_flist:
                    need_delete = True
                else:
                    saved_org_crc = self._saved_flist_data[file_name][1]
                    new_orc_crc = new_flist[file_name][1]
                    if int(saved_org_crc) != int(new_orc_crc):
                        need_delete = True
                if need_delete:
                    self._remove_outdate_cook_file(file_name)

            if self._met_error:
                self._remove_all()
                return False
            if not self._update_and_flush() or self._met_error:
                self._remove_all()
                return False
            self.active_loader()
            if self._met_error:
                self._remove_all()
                return False
            save_physx_flist_data(new_flist)
            return True

    def _pre_init(self):
        if not os.path.exists(PHYSX_DATA_PATH):
            try:
                os.makedirs(PHYSX_DATA_PATH)
            except Exception as e:
                log_except('create physx data path failed:{}'.format(str(e)))
                self._met_error = True
                return False

        ret = self._remove_tmp_npk()
        get_success, saved_flist_data = get_physx_saved_flist_data()
        if not get_success:
            self._remove_all()
            return False
        if not saved_flist_data:
            self._remove_all()
        self._saved_flist_data = saved_flist_data
        return True and ret

    def _init_npk_info(self):
        met_error = False
        nx_open_npk = None
        try:
            if os.path.exists(self._npk_file_path):
                self._npk_exists = True
                nx_open_npk = package.nxnpk(self._npk_file_path[:-4])
                self._old_npk_flist_dict, ret = self.get_npk_flist_info(nx_open_npk)
                nx_open_npk = None
                if not ret:
                    log_error('get npk info error, clear npk!')
                    met_error = True
            else:
                self._old_npk_flist_dict = {}
        except Exception as e:
            nx_open_npk = None
            met_error = True
            log_except('get npk info error:{}, clear npk'.format(str(e)))

        if met_error:
            self._old_npk_flist_dict = {}
            self._remove_npk()
        return

    def get_flist_index(self):
        return cal_file_id('physx_cook_flist.txt')

    def get_npk_flist_info(self, in_nx_open_npk):
        flist_file_index = self.get_flist_index()
        flist_data = in_nx_open_npk.get_file_by_id(flist_file_index)
        flist_data = six.ensure_str(flist_data)
        if flist_data is None:
            return ({}, False)
        else:
            flist_dict = {}
            for line in flist_data.splitlines():
                if not line:
                    continue
                info = line.split('\t')
                flist_dict[int(info[0])] = info[1]

            return (flist_dict, True)

    def _update_and_flush(self):
        try:
            if os.path.exists(self._discrete_path):
                discrete_file_list = os.listdir(self._discrete_path)
            else:
                discrete_file_list = []
        except Exception as e:
            log_except('get discrete file list error:{}'.format(str(e)))
            self._met_error = True
            return False

        num_discrete_file = len(discrete_file_list)
        old_npk_file_num = len(self._old_npk_flist_dict)
        npk_outdate_num = len(self._outdate_id_set)
        if npk_outdate_num > 0 and npk_outdate_num >= old_npk_file_num:
            self._old_npk_flist_dict = {}
            self._outdate_id_set = set()
            npk_outdate_num = 0
            old_npk_file_num = 0
            if not self._remove_npk():
                return False
        if num_discrete_file > 0 or npk_outdate_num > 0 and npk_outdate_num < old_npk_file_num:
            cout_info('need up npk:{} {} {}'.format(num_discrete_file, npk_outdate_num, old_npk_file_num))
        else:
            cout_info('no need up npk !')
            return True
        if not self._remove_tmp_npk():
            return False
        else:
            npk_writer = package.npkwriter()
            ret = npk_writer.open(self._temp_npk_file_name, 0)
            if not ret:
                npk_writer = None
                self._met_error = True
                log_error('open tmp write npk failed')
                return False
            if os.path.exists(self._npk_file_path):
                try:
                    nx_open_npk = package.nxnpk(self._npk_file_path[:-4])
                except Exception as e:
                    log_except('open npk file:{}'.format(str(e)))
                    nx_open_npk = None
                    if not self._remove_npk():
                        npk_writer = None
                        return False

            else:
                nx_open_npk = None
            flist_lst = []
            all_index_set = set()
            for file_name in discrete_file_list:
                if not file_name.endswith('.pxcooked'):
                    continue
                full_path = os.path.join(self._discrete_path, file_name)
                index_id = cal_file_id('physxcook\\{}'.format(file_name))
                if index_id in all_index_set:
                    log_error('duplicate index id: {} {}'.format(index_id, file_name))
                    continue
                try:
                    with open(full_path, 'rb') as tmp_file:
                        r_data = tmp_file.read()
                        data_crc32 = zlib.crc32(r_data)
                except Exception as e:
                    log_except('open discrete file:{}'.format(str(e)))
                    continue

                if data_crc32 < 0:
                    pkg_crc_sign = 0 if 1 else 1
                    ret_size = npk_writer.add_patch_data(index_id, r_data, pkg_crc_sign, abs(data_crc32), True)
                    if ret_size > 0:
                        flist_lst.append('{}\t{}'.format(index_id, data_crc32))
                        all_index_set.add(index_id)
                        try:
                            os.remove(full_path)
                        except Exception as e:
                            log_except('remove discrete file:{}'.format(str(e)))
                            continue

                    continue

            if nx_open_npk:
                for file_index in self._old_npk_flist_dict:
                    if file_index not in self._outdate_id_set and file_index not in all_index_set:
                        ret = npk_writer.add_npk_data_v2(file_index, nx_open_npk)
                        if ret > 0:
                            data_crc32 = self._old_npk_flist_dict[file_index]
                            all_index_set.add(file_index)
                            flist_lst.append('{}\t{}'.format(file_index, data_crc32))
                        else:
                            log_error('add_npk_data_v2 failed:{}'.format(file_index))

            nx_open_npk = None
            if len(flist_lst) > 0:
                flist_file_index = self.get_flist_index()
                flist_data = '\n'.join(flist_lst)
                try:
                    flist_data = six.ensure_binary(flist_data)
                    data_crc32 = zlib.crc32(flist_data)
                except Exception as e:
                    log_except('zlib crc32 error:{}'.format(str(e)))
                    self._met_error = True
                    return False

                if data_crc32 < 0:
                    pkg_crc_sign = 0 if 1 else 1
                    ret_size = npk_writer.add_patch_data(flist_file_index, flist_data, pkg_crc_sign, abs(data_crc32), True)
                    if ret_size < 0:
                        log_error('add flist data ret code:{} data len:{}'.format(ret_size, len(flist_data)))
                        self._met_error = True
                        npk_writer = None
                        return False
                    flush_ret = npk_writer.flush()
                    if not flush_ret:
                        log_error('flush failed!! ret code:{}'.format(flush_ret))
                        self._met_error = True
                        npk_writer = None
                        return False
                    npk_writer = None
                    try:
                        new_npk = package.nxnpk(self._temp_npk_file_name[:-4])
                    except Exception as e:
                        new_npk = None
                        self._remove_tmp_npk()
                        log_except('new npk error:{}'.format(str(e)))
                        return False

                    support_py3_crc = hasattr(new_npk, 'check_data_py3_crc_by_id')
                    for line in flist_lst:
                        info = line.split('\t')
                        ret_code = self._vefify_npk_file(new_npk, int(info[0]), int(info[1]), support_py3_crc)
                        if ret_code <= 0:
                            try:
                                r_data = new_npk.get_file_by_id(int(info[0]))
                                get_crc = zlib.crc32(r_data)
                            except Exception as e:
                                get_crc = 0
                                log_except('get_file_by_id error:{}'.format(str(e)))

                            new_npk = None
                            self._remove_tmp_npk()
                            log_error('check_data_crc failed:{} {} {}'.format(ret_code, info, get_crc))
                            return False

                    new_npk = None
                    if os.path.exists(self._npk_file_path):
                        return self._remove_npk() or False
                try:
                    os.rename(self._temp_npk_file_name, self._npk_file_path)
                except Exception as e:
                    self._remove_tmp_npk()
                    log_except('rename npk error:{}'.format(str(e)))

                return True
            npk_writer = None
            return True

    def active_loader(self):
        try:
            if os.path.exists(self._npk_file_path):
                ret = C_file.add_res_npk_loader(self._npk_file_path[:-4], 0, PHYSX_COOK_NPK_TAG)
                if not ret:
                    log_error('add npk failed !')
                else:
                    cout_info('add npk success!')
        except Exception as e:
            log_error('active_loader failed:{}'.format(str(e)))

    def _remove_all(self):
        self._remove_discrete_folder()
        self._remove_npk()
        self._remove_physx_data_path()

    def _remove_tmp_npk(self):
        if os.path.exists(self._temp_npk_file_name):
            try:
                os.remove(self._temp_npk_file_name)
            except Exception as e:
                self._met_error = True
                log_except('remove tmp npk file error:{}'.format(str(e)))
                return False

        return True

    def _remove_npk(self):
        try:
            C_file.del_fileloader_by_tag(PHYSX_COOK_NPK_TAG)
        except Exception as e:
            print('[revert] del_fileloader_by_tag except:{}'.format(str(e)))

        met_error = False
        try:
            if os.path.exists(self._npk_file_path):
                os.remove(self._npk_file_path)
        except Exception as e:
            self._met_error = True
            met_error = True
            print('remove npk except:{}'.format(str(e)))

        if met_error:
            return False
        return True

    def _remove_physx_data_path(self):
        try:
            saved_flist_path = get_physx_saved_flist_path()
            if os.path.exists(saved_flist_path):
                os.remove(saved_flist_path)
        except Exception as e:
            log_except('remove physx data path except:{}'.format(str(e)))

    def _remove_discrete_folder(self):
        try:
            if os.path.exists(self._discrete_path):
                shutil.rmtree(self._discrete_path)
        except Exception as e:
            self._met_error = True
            print('remove except:{}'.format(str(e)))

    def _remove_outdate_cook_file(self, in_file_name):
        rel_path = in_file_name[LEN_RES_PREFIX:].replace('\\', '/')
        if rel_path.find('lodmodels') >= 0:
            file_path_prefix = rel_path.split('.')[0]
            index = 0
            cur_file_path = '{}_{}.mesh'.format(file_path_prefix, index)
            while self._remove_single_path(cur_file_path):
                index += 1
                cur_file_path = '{}_{}.mesh'.format(file_path_prefix, index)

        else:
            self._remove_single_path(rel_path)

    def _remove_single_path(self, in_rel_path):
        file_id = cal_file_id(in_rel_path)
        cook_file_path = 'res/physxcook/{}.pxcooked'.format(file_id)
        cook_file_path = os.path.join(NX_DIR, cook_file_path)
        process_true = False
        if os.path.exists(cook_file_path):
            process_true = True
            try:
                os.remove(cook_file_path)
            except Exception as e:
                log_except('remove_single_path except:{}'.format(str(e)))
                self._met_error = True

        file_index_id = cal_file_id('physxcook\\{}.pxcooked'.format(file_id))
        if file_index_id in self._old_npk_flist_dict:
            self._outdate_id_set.add(file_index_id)
            process_true = True
        return process_true

    def _vefify_npk_file(self, in_npk, index_id, cache_crc32, support_py3_crc32):
        if six.PY2:
            ret_code = in_npk.check_data_crc_by_id(index_id, cache_crc32)
        elif support_py3_crc32:
            ret_code = in_npk.check_data_py3_crc_by_id(index_id, cache_crc32)
        else:
            ret_code = 1
        return ret_code