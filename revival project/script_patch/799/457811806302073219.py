# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/ui_redpoint_mgr.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.framework import Singleton
from data import redpoint_info
from collections import defaultdict
import weakref
import json
from logic.comsys.guide_ui.GuideSetting import GuideSetting
import traceback

class RedPointMgr(Singleton):
    ALIAS_NAME = 'redpoint_mgr'

    def init(self):
        self._all_elems = {}
        self._project_elem_map = defaultdict(dict)

    def register_redpoint(self, redpoint_panel, redpoint_id, custom_func=None, *args, **kwargs):
        elem_data = redpoint_info.all_elem_datas.get(redpoint_id)
        if not elem_data:
            log_error('redpoint_id %s not exist', redpoint_id)
            traceback.print_stack()
            return
        if args or kwargs:
            hash_key = str(redpoint_panel) + str(redpoint_id) + json.dumps(args) + json.dumps(kwargs)
        else:
            hash_key = str(redpoint_panel) + str(redpoint_id)
        if hash_key in self._all_elems:
            self.unregister_by_key(hash_key)
        elem = RedPointElem(redpoint_panel, custom_func, elem_data, *args, **kwargs)
        self._all_elems[hash_key] = elem
        print(self._project_elem_map, elem_data.get('cProjectName'))
        project_elems = self._project_elem_map[elem_data.get('cProjectName')]
        project_elems[hash_key] = elem

    def register_by_project_name_auto(self, root_panel, project_name):
        redpoints = redpoint_info.project_redpoint_ids.get(project_name)
        if redpoints:
            all_elem_datas = redpoint_info.all_elem_datas
            for redpoint_id in redpoints:
                elem_data = all_elem_datas.get(redpoint_id)
                if elem_data:
                    widget_path = elem_data.get('cRedPointPath')
                    if widget_path:
                        paths = widget_path.split('.')
                        cur_widget = root_panel
                        for widget_name in paths:
                            if widget_name != '':
                                cur_widget = getattr(cur_widget, widget_name, None)

                        if not cur_widget:
                            log_error('redpoint_id %s widget_path %s not exist' % (redpoint_id, widget_path))
                            traceback.print_stack()
                            continue
                        if redpoint_id in self._all_elems:
                            self.unregister_by_key(redpoint_id)
                        elem = RedPointElem(cur_widget, None, elem_data)
                        self._all_elems[redpoint_id] = elem
                        project_elems = self._project_elem_map[project_name]
                        project_elems[redpoint_id] = elem

        return

    def unregister_by_key(self, hash_key):
        elem = self._all_elems.get(hash_key)
        del self._all_elems[hash_key]
        project_elems = self._project_elem_map.get(elem.get_project_name())
        del project_elems[hash_key]
        elem.destroy()

    def unregister_by_project_name(self, project_name):
        project_elems = self._project_elem_map.get(project_name)
        if project_elems:
            for hash_key, elem in six.iteritems(project_elems):
                del self._all_elems[hash_key]
                elem.destroy()

            project_elems.clear()

    def remove_all_elems(self):
        for project_name in six.iterkeys(self._project_elem_map):
            self.unregister_by_project_name(project_name)


class RedPointElem(object):

    def __init__(self, redpoint_panel, custom_func, elem_data, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._elem_data = elem_data
        self._custom_func = weakref.ref(custom_func) if custom_func else None
        self._redpoint_panel = weakref.ref(redpoint_panel) if redpoint_panel else None
        self._check_event_names = []
        self._child_ids = elem_data.get('cChildIds')
        self.register_redpoint()
        self.refresh()
        return

    def register_redpoint(self):
        self._check_event_names = self._elem_data.get('cCheckEvent', set())
        if not self._check_event_names and self._child_ids:
            self._check_event_names = self.get_child_event_names(self._child_ids)
        for event_name in self._check_event_names:
            global_data.emgr.add_event_notify(event_name, self.refresh)

    def get_child_event_names(self, child_ids):
        all_elem_datas = redpoint_info.all_elem_datas
        event_names = set()
        for child_redpoint_id in child_ids:
            child_elem_data = all_elem_datas.get(child_redpoint_id)
            if not child_elem_data:
                log_error('child redpoint_id %s not exist', child_redpoint_id)
                traceback.print_stack()
                continue
            child_event_names = child_elem_data.get('cCheckEvent', [])
            if child_event_names:
                event_names = event_names | set(child_event_names)
                continue
            sub_child_ids = child_elem_data.get('cChildIds')
            if sub_child_ids:
                event_names = event_names | self.get_child_event_names(sub_child_ids)

        return event_names

    def unregister_redpoint(self):
        for event_name in self._check_event_names:
            global_data.emgr.remove_event_notify(event_name, self.refresh)

        self._check_event_names = []

    def refresh(self, *args):
        check_hide_func = self._elem_data.get('check_hide_func')
        visible = False
        if not check_hide_func or not check_hide_func():
            check_func = self._elem_data.get('check_func')
            if check_func:
                visible = True if check_func(*self._args, **self._kwargs) else False
            elif self._child_ids:
                visible = self.check_all_childs_redpoint(self._child_ids)
            else:
                visible = False
        if self._redpoint_panel and self._redpoint_panel():
            self._redpoint_panel().setVisible(visible)
        else:
            self.unregister_redpoint()
            return
        if self._custom_func and self._custom_func():
            self._custom_func()(*self._args, **self._kwargs)

    def check_all_childs_redpoint(self, child_ids):
        all_elem_datas = redpoint_info.all_elem_datas
        for child_redpoint_id in child_ids:
            child_elem_data = all_elem_datas.get(child_redpoint_id)
            if not child_elem_data:
                log_error('child redpoint_id %s not exist', child_redpoint_id)
                traceback.print_stack()
                continue
            child_check_func = child_elem_data.get('check_func')
            if child_check_func and child_check_func():
                return True
            sub_child_ids = child_elem_data.get('cChildIds')
            if sub_child_ids and self.check_all_childs_redpoint(sub_child_ids):
                return True

        return False

    def get_project_name(self):
        return self._elem_data.get('cProjectName')

    def destroy(self):
        self.unregister_redpoint()