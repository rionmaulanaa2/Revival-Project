# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/editor_utils/sfx_editor_utils.py
from __future__ import absolute_import
from six.moves import range
from common.framework import Singleton
from common.utils.sfxmgr import SfxMgr, BulletSfxMgr
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref
import world

class SfxEditorConnector(Singleton):
    ALIAS_NAME = 'sfx_editor_connector'

    def init(self):
        self.max_queue_length = 10
        self.created_sfx_path_queue = [ ('', None) for i in range(self.max_queue_length) ]
        self.queue_head = 0
        self.editor_sfx_path_map = {}
        self.notify_queue_updated_func = None
        return

    def _fill_and_get_new_queue(self, start, new_max_queue_length):
        new_queue = [ ('', None) for i in range(new_max_queue_length) ]
        index = 0
        initial_start = start
        while index < new_max_queue_length:
            new_queue[index] = self.created_sfx_path_queue[start]
            index += 1
            start += 1
            if start >= self.max_queue_length:
                start = 0
            if start == initial_start:
                break

        return new_queue

    def modify_max_queue_length(self, new_max_queue_length):
        if self.max_queue_length == new_max_queue_length:
            return None
        else:
            if new_max_queue_length > self.max_queue_length:
                if self.created_sfx_path_queue[self.queue_head]:
                    self.created_sfx_path_queue = self._fill_and_get_new_queue(self.queue_head, new_max_queue_length)
                else:
                    self.created_sfx_path_queue.extend([ ('', None) for i in range(new_max_queue_length - self.max_queue_length) ])
                self.queue_head = self.max_queue_length
            else:
                if new_max_queue_length <= self.queue_head:
                    self.created_sfx_path_queue = self.created_sfx_path_queue[self.queue_head - new_max_queue_length:self.queue_head]
                else:
                    self.created_sfx_path_queue = self._fill_and_get_new_queue(self.max_queue_length - (new_max_queue_length - self.queue_head), new_max_queue_length)
                self.queue_head = 0
            self.max_queue_length = new_max_queue_length
            if self.notify_queue_updated_func:
                self.notify_queue_updated_func(self.get_created_sfx_path_queue())
            return None

    def record_created_sfx_path(self, sfx_path, model_ref=None):
        self.created_sfx_path_queue[self.queue_head] = (sfx_path, model_ref)
        self.queue_head += 1
        if self.queue_head >= self.max_queue_length:
            self.queue_head = 0
        if self.notify_queue_updated_func:
            self.notify_queue_updated_func(self.get_created_sfx_path_queue())

    def get_created_sfx_path_queue(self):
        head = self.queue_head - 1
        if head < 0:
            head = self.max_queue_length - 1
        end = head
        queue = self.created_sfx_path_queue
        ret = []
        while queue[head][0]:
            ret.append(queue[head])
            head -= 1
            if head < 0:
                head = self.max_queue_length - 1
            if head == end:
                break

        return ret

    def update_sfx_path_map(self, new_sfx_path_map):
        self.editor_sfx_path_map = new_sfx_path_map

    def clear_created_sfx_path_queue(self):
        self.created_sfx_path_queue = [ ('', None) for i in range(self.max_queue_length) ]
        self.queue_head = 0
        return None

    def get_sfx_path_mapping(self, sfx_path):
        return self.editor_sfx_path_map.get(sfx_path, sfx_path)

    @staticmethod
    def preview_sfx(sfx_path, model_ref=None, dist=5):
        if sfx_path.find('\t') != -1:
            socket, sfx_path = sfx_path.split('\t')
            if model_ref is None or not model_ref() or not model_ref().valid:
                cam = world.get_active_scene().active_camera
                sfx_pos = cam.position + cam.rotation_matrix.forward * dist * NEOX_UNIT_SCALE
                global_data.sfx_mgr.directly_create_sfx_in_scene(sfx_path, sfx_pos, duration=1.5)
            else:
                model = model_ref()
                if model.get_socket_index(socket) == -1:
                    global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b{}\xe4\xb8\x8d\xe5\x85\xb7\xe6\x9c\x89\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{}\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe8\xb5\x84\xe6\xba\x90'.format(model.filename.replace('\\', '/'), socket))
                else:
                    global_data.sfx_mgr.directly_create_sfx_on_model(sfx_path, model, socket, duration=2.0)
        else:
            cam = world.get_active_scene().active_camera
            sfx_pos = cam.position + cam.rotation_matrix.forward * dist * NEOX_UNIT_SCALE
            global_data.sfx_mgr.directly_create_sfx_in_scene(sfx_path, sfx_pos, duration=1.5)
        return


sfx_editor_connector = SfxEditorConnector()

def check_replace_sfx_path(func):

    def wrapper(self, sfx_path, *args, **kwargs):
        sfx_path = sfx_editor_connector.get_sfx_path_mapping(sfx_path)
        return func(self, sfx_path, *args, **kwargs)

    return wrapper


class SfxEditorSfxMgr(SfxMgr):

    def directly_create_sfx_in_scene(self, *args, **kwargs):
        super(SfxEditorSfxMgr, self).create_sfx_in_scene(ex_data={'need_record': False}, *args, **kwargs)

    def directly_create_sfx_on_model(self, *args, **kwargs):
        super(SfxEditorSfxMgr, self).create_sfx_on_model(ex_data={'need_record': False}, *args, **kwargs)

    @check_replace_sfx_path
    def create_sfx_in_scene(self, sfx_path, *args, **kwargs):
        return super(SfxEditorSfxMgr, self).create_sfx_in_scene(sfx_path, *args, **kwargs)

    @check_replace_sfx_path
    def create_sfx_on_model(self, sfx_path, model, socket, *args, **kwargs):
        if model.get_socket_index(socket) == -1:
            sfx_editor_connector.record_created_sfx_path('{}\t{}'.format(socket, sfx_path))
            global_data.game_mgr.show_tip('model:[%s]\xe4\xb8\x8a\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9[%s]\xef\xbc\x8c\xe7\x89\xb9\xe6\x95\x88[%s]\xe6\x8c\x82\xe6\x8e\xa5\xe5\xa4\xb1\xe8\xb4\xa5\xe3\x80\x82' % (model.filename, socket, sfx_path))
            return
        ex_data = {'model_ref': weakref.ref(model),'socket': socket}
        if 'ex_data' in kwargs:
            kwargs['ex_data'].update(ex_data)
        else:
            kwargs['ex_data'] = ex_data
        return super(SfxEditorSfxMgr, self).create_sfx_on_model(sfx_path, model, socket, *args, **kwargs)

    @check_replace_sfx_path
    def create_sfx_for_model(self, sfx_path, *args, **kwargs):
        return super(SfxEditorSfxMgr, self).create_sfx_for_model(sfx_path, *args, **kwargs)

    def _create_sfx(self, sfx_path, duration=0, on_create_func=None, on_remove_func=None, ex_data={}, sfx_instance=None):
        if ex_data.get('need_record', True):
            if 'socket' in ex_data:
                sfx_editor_connector.record_created_sfx_path('{}\t{}'.format(ex_data['socket'], sfx_path), ex_data['model_ref'])
            else:
                sfx_editor_connector.record_created_sfx_path(sfx_path)
        return super(SfxEditorSfxMgr, self)._create_sfx(sfx_path, duration, on_create_func, on_remove_func, ex_data)


class SfxEditorBulletSfxMgr(BulletSfxMgr):

    @check_replace_sfx_path
    def create_sfx_in_scene(self, sfx_path, *args, **kwargs):
        return super(SfxEditorBulletSfxMgr, self).create_sfx_in_scene(sfx_path, *args, **kwargs)

    @check_replace_sfx_path
    def create_sfx_on_model(self, sfx_path, *args, **kwargs):
        return super(SfxEditorBulletSfxMgr, self).create_sfx_on_model(sfx_path, *args, **kwargs)

    @check_replace_sfx_path
    def create_sfx_for_model(self, sfx_path, *args, **kwargs):
        return super(SfxEditorBulletSfxMgr, self).create_sfx_for_model(sfx_path, *args, **kwargs)

    def _create_sfx(self, sfx_path, *args, **kwargs):
        sfx_editor_connector.record_created_sfx_path(sfx_path)
        return super(SfxEditorBulletSfxMgr, self)._create_sfx(sfx_path, *args, **kwargs)