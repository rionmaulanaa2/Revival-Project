# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sprite_usage_uploader.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import six
import os
import time
import json
import C_file
import game3d
from logic.gcommon.time_utility import get_date_str, get_server_time, ONE_WEEK_SECONDS, ONE_MINUTE_SECONDS

class PlistSpriteExistChecker(object):

    def check(self):
        from common.utils.ui_utils import GetPlistConf
        s = C_file.get_res_file('gui/ui_res_plist/plist.json', '')
        plists = json.loads(s)
        for plist_path in plists:
            frames = GetPlistConf(plist_path)
            for frame in frames:
                if 'out-of-date/' in frame:
                    frame = frame.replace('out-of-date/', '')
                if not C_file.find_res_file(frame, ''):
                    print('fame', plist_path, frame)


class PlistRefChecker(object):

    def __init__(self):
        self._sprite_map = {}

    def check(self):
        from common.utils.ui_utils import GetPlistConf
        s = C_file.get_res_file('gui/ui_res_plist/plist.json', '')
        all_pngs = []
        plists = json.loads(s)
        for plist_path in plists:
            self._sprite_map[plist_path] = []
            frames = GetPlistConf(plist_path)
            for frame in frames:
                if 'out-of-date/' in frame:
                    frame = frame.replace('out-of-date/', '')
                self._sprite_map[plist_path].append(frame)
                all_pngs.append(frame)

        print('self._sprite_map', all_pngs)


class HashChecker(object):

    def __init__(self):
        self._hash_dict = {}
        import logic
        src_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'res')
        self._src_path = src_path
        self._png_set = set()

    def check(self):
        from tools.json_tools.for_each_json import for_file_in_res_do
        for_file_in_res_do(self.check_full_path, dir_list=('res/gui', ))
        t = time.time()
        print('hash_dict size', len(self._png_set))
        for relative_path in self._png_set:
            print('relative_path', os.path.normpath(relative_path).replace('\\', '/'))
            name_hash = game3d.calc_filename_hash64(relative_path)
            if name_hash not in self._hash_dict:
                self._hash_dict[name_hash] = relative_path
            else:
                log_error('file name collided', relative_path, self._hash_dict[name_hash])

        print('name_hash cost time ', time.time() - t)

    def check_full_path(self, full_path):
        relative_path = os.path.relpath(full_path, self._src_path)
        self._png_set.add(relative_path)


class UploaderBase(object):

    def __init__(self, root_dir):
        self._root_dir = root_dir

    def upload(self, target_usages, finish_cb):
        pass


class SpriteFileServerUploader(UploaderBase):

    def __init__(self, root_dir):
        super(SpriteFileServerUploader, self).__init__(root_dir)
        self._upload_usages = {}
        self.all_uploaded_usage = {}

    def upload(self, target_usages, finish_cb):
        self._upload_usages = target_usages
        json_path = os.path.join(self._root_dir, 'usage_collections.json')
        zip_path = os.path.join(self._root_dir, 'usage_collect.zip')
        with open(json_path, 'w') as tmp_file:
            json.dump(self._upload_usages, tmp_file, sort_keys=True)
        try:
            import zipfile
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                time_stamp = time.strftime('%H%M%S')
                user_id = global_data.player or 'empty' if 1 else global_data.player.uid
                log_name = '%s_%s.json' % (user_id, time_stamp)
                z.write(json_path, log_name)
        except Exception as e:
            log_error('[UsageRecord] zip error:%s' % str(e))
            return

        self._upload_file_outer_file_server_version(zip_path)

    def _upload_file_outer_file_server_version(self, zip_path):
        if not global_data.player:
            return False
        global_data.player.try_upload_usage_collect(zip_path, self._upload_to_file_picker_cb)
        return True

    def _upload_to_file_picker_cb(self, status, error, record_names, file_path):
        if global_data.is_inner_server:
            print('[UsageRecord] upload cb:', status, file_path, record_names)
        self._on_upload_finish(status)
        if file_path:
            try:
                os.remove(file_path)
            except Exception as e:
                log_error('[UsageRecord] os remove error:%s' % str(e))

    def _on_upload_finish(self, ret):
        if ret:
            print('up num:', len(self._upload_usages))
            t = int(get_server_time())
            for key in six.iterkeys(self._upload_usages):
                self.all_uploaded_usage[key] = t

            self._upload_usages = {}
            try:
                uploaded_json_path = os.path.join(self._root_dir, 'sp_uploaded_usages.json')
                with open(uploaded_json_path, 'w') as tmp_file:
                    json.dump(self.all_uploaded_usage, tmp_file, sort_keys=True)
            except Exception as e:
                log_error('[UsageRecord] save all_uploaded_usages error: %s' % str(e))


class SpriteUsageUploader(UploaderBase):

    def __init__(self, root_dir):
        super(SpriteUsageUploader, self).__init__(root_dir)

    def get_sprite_uploaded_usage(self):
        try:
            from mobile.common.JsonConfig import parse
            uploaded_json_path = os.path.join(self._root_dir, 'sp_uploaded_usages.json')
            if os.path.exists(uploaded_json_path):
                all_uploaded_usage = parse(uploaded_json_path)
                import exception_hook
                size = os.path.getsize(uploaded_json_path)
                if size > 1048576:
                    msg = 'size of sp_uploaded_usages.json is larger than 1MB'
                    exception_hook.post_error(msg)
            else:
                all_uploaded_usage = {}
        except Exception as e:
            log_error('[SpriteUsageUploader] get all uploaded error: %s' % str(e))
            all_uploaded_usage = {}

        return all_uploaded_usage

    def get_sprite_base_usage(self):
        try:
            from common.cfg import confmgr
            if C_file.find_res_file('confs/used_usage_conf.json', ''):
                base_usage_list = confmgr.get('used_usage_conf', default=[])
                base_usage_set = set(base_usage_list.get_conf())
            else:
                base_usage_set = set()
        except Exception as e:
            log_error('[SpriteUsageUploader] get base usage error: %s' % str(e))
            base_usage_set = set()

        return base_usage_set

    def normalize_path(self, p):
        windows_p = os.path.normpath(p)
        return windows_p.replace('\\', '/')

    def upload(self, target_usages, finish_cb):
        t = int(get_server_time())
        remove_keys = set()
        _upload_usages_hashed = [ str(i) if 1 else str(game3d.calc_filename_hash64(self.normalize_path(i))) for i in six.iterkeys(target_usages) if type(i) in six.integer_types
                                ]
        all_uploaded_usage = self.get_sprite_uploaded_usage()
        if global_data.is_inner_server:
            print('before upload all_uploaded_usage num is ', len(all_uploaded_usage))
        if not global_data.is_inner_server or global_data.force_check_sprite_recorder_base_dict:
            base_usages = self.get_sprite_base_usage()
        else:
            base_usages = set()
        for key in _upload_usages_hashed:
            str_key = key
            if str_key in base_usages:
                remove_keys.add(key)
            elif str_key in all_uploaded_usage:
                last_upload_time = all_uploaded_usage[str_key]
                if 0 < t - last_upload_time < ONE_WEEK_SECONDS * 3:
                    remove_keys.add(key)

        for key in remove_keys:
            _upload_usages_hashed.remove(key)

        if not _upload_usages_hashed:
            if global_data.is_inner_server:
                print('[SpriteUsageUploader] no upload usages')
            if finish_cb:
                finish_cb(False, [], {})
            return

        def cb():
            self.sprite_on_finish_uploaded(_upload_usages_hashed, all_uploaded_usage)
            if finish_cb:
                finish_cb(True, _upload_usages_hashed, all_uploaded_usage)

        self.sprite_upload_file_log_version(_upload_usages_hashed, cb)

    def sprite_upload_file_log_version(self, filename_list, cb):
        from logic.gutils.salog import SALog
        salog_writer = SALog.get_instance()
        log_error('NX709S_sprite_upload_file_log_version')
        all_files_count = len(filename_list)
        each_size = 100
        batch_count = len(filename_list) // each_size
        remain_count = all_files_count - each_size * batch_count
        if remain_count > 20 or batch_count == 0:
            batch_count += 1
        for i in range(batch_count):
            if i == batch_count - 1:
                upload_list = filename_list[i * each_size:]
            else:
                upload_list = filename_list[i * each_size:(i + 1) * each_size]
            if global_data.is_inner_server:
                print('_upload_file_log_version', upload_list)
            salog_writer.write(SALog.COLLECT_UI, upload_list)

        if cb:
            cb()

    def sprite_on_finish_uploaded(self, filename_list, all_uploaded_usage):
        t = int(get_server_time())
        for f in filename_list:
            all_uploaded_usage[str(f)] = t

        all_uploaded_usage = self.check_clear_outdate_usages(all_uploaded_usage)
        if global_data.is_inner_server:
            print('up num:', len(filename_list))
            print('all_uploaded_usage num ', len(all_uploaded_usage))
        try:
            uploaded_json_path = os.path.join(self._root_dir, 'sp_uploaded_usages.json')
            with open(uploaded_json_path, 'w') as tmp_file:
                json.dump(all_uploaded_usage, tmp_file, sort_keys=True)
        except Exception as e:
            log_error('[SpriteUsageUploader] save all_uploaded_usages error: %s' % str(e))

        log_error('NX709S_sprite_upload_file_log_version end')

    def check_clear_outdate_usages(self, all_uploaded_usage):
        current_t = int(get_server_time())
        need_remove_set = set()
        last_all_usage_clear_time = global_data.achi_mgr.get_general_archive_data().get_field('last_all_uploaded_usage_clear_time', 0)
        if last_all_usage_clear_time - current_t > ONE_WEEK_SECONDS:
            if global_data.is_inner_server:
                print('[SpriteUsageUploader] Run check_clear_outdate_usages')
            global_data.achi_mgr.get_general_archive_data().set_field('last_all_uploaded_usage_clear_time', current_t)
            for file_key, t in six.iteritems(all_uploaded_usage):
                if current_t - t > ONE_WEEK_SECONDS * 4:
                    need_remove_set.add(file_key)

            for k in need_remove_set:
                del all_uploaded_usage[k]

            return all_uploaded_usage
        else:
            if global_data.is_inner_server:
                print('[SpriteUsageUploader] Do not run check_clear_outdate_usages')
            return all_uploaded_usage