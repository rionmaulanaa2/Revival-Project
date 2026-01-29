# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/UICreatorConfig.py
from __future__ import absolute_import
import six_ex
import six
from collections import OrderedDict
from inspect import getargspec

class CustomCfg(object):

    def __init__(self, conf, default_cls):
        self.conf = conf
        default_cls.ATTR_DEFINE = dict(default_cls.ATTR_DEFINE)
        self.default_cls = default_cls

    def has_key(self, key):
        if key in self.conf:
            return True
        return key in self.default_cls.ATTR_DEFINE

    def get(self, key, default=None):
        val = self.conf.get(key, default)
        if val is None:
            return self.default_cls.ATTR_DEFINE.get(key, default)
        else:
            return val

    def __getitem__(self, key):
        val = self.conf.get(key, None)
        if val is None:
            return self.default_cls.ATTR_DEFINE.get(key)
        else:
            return val

    def __setitem__(self, key, value):
        self.conf.__setitem__(key, value)

    def __delitem__(self, key):
        self.conf.__delitem__(key)

    def __iter__(self):
        raise ValueError('NotImplemented')

    def next(self):
        raise ValueError('NotImplemented')

    def __eq__(self, obj):
        raise ValueError('NotImplemented')

    def __len__(self):
        return len(self.conf) + len(self.default_cls.ATTR_DEFINE)

    def __contains__(self, item):
        return item in self.conf or item in self.default_cls.ATTR_DEFINE

    def iteritems(self):
        raise ValueError('NotImplemented')


class UICreatorConfig(object):

    def __init__(self, ctor_cls, uisys):
        cname = ctor_cls.COM_NAME
        create_func, create_attrs, check_func_list = None, [], []
        attr_define = {}
        attr_init = []
        attr_conf = []
        create_func = getattr(ctor_cls, 'create')
        create_attrs = getargspec(create_func).args[2:]
        check_conf_func = getattr(ctor_cls, 'check_config', None)
        if check_conf_func:
            check_func_list.append(check_conf_func)
        attr_define = ctor_cls.ATTR_DEFINE
        attrs_dict = OrderedDict(attr_define)
        attr_define = six_ex.items(attrs_dict)
        if global_data.enable_ui_custom_cfg:
            self.ctor_cls = ctor_cls
        dynamic_attr = ctor_cls.DYNAMIC_ARGS
        self._check_attr_valid(create_attrs, attrs_dict, dynamic_attr)
        attr_init = ctor_cls.ATTR_INIT
        for group_name in attr_init:
            handler = getattr(ctor_cls, 'set_attr_group_%s' % group_name, None)
            if not handler:
                raise Exception('can not find set attr gourp func %s' % group_name)
            group_attrs = getargspec(handler).args[3:]
            self._check_attr_valid(group_attrs, attrs_dict, dynamic_attr)
            attr_conf.append((handler, group_attrs))

        self.create_info = (attr_define, create_func, create_attrs)
        self.attr_conf = attr_conf
        self.check_func_list = check_func_list
        if uisys:
            uisys.regist_uicreator(cname, self)
        return

    def _check_attr_valid(self, attr_list, attr_define_dict, dynamic_attr):
        for aname in attr_list:
            if aname in dynamic_attr:
                continue
            if aname not in attr_define_dict:
                raise Exception('attr %s not in define' % aname)

    def Create(self, conf, parent, root, aniConf):
        if global_data.enable_ui_custom_cfg:
            conf = self.MergeCustomCfg(conf)
        else:
            self.MergeCfg(conf)
        attr_define, create_func, create_attrs = self.create_info
        params = [ conf.get(aname) for aname in create_attrs ]
        ctrl = create_func(parent, root, *params)
        ctrl.SetConf(conf)
        self.add_ani_data_2_ani_conf(conf, aniConf, ctrl)
        if 'ani_times' in conf:
            ctrl.SetAnimationPlayTimes(conf['ani_times'].copy())
        if root is None:
            root = ctrl
        conf['aniConf'] = aniConf
        for attr_setter, attr_list in self.attr_conf:
            params = [ conf.get(aname) for aname in attr_list ]
            attr_setter(ctrl, parent, root, *params)

        del conf['aniConf']
        return ctrl

    @staticmethod
    def add_ani_data_2_ani_conf(template_conf, ani_conf, ctrl, get_anim_name=None, target_ani_name_list=None):
        ani_data_conf = template_conf.get('ani_data', None)
        if ani_data_conf:
            for aniname, aniData in six.iteritems(ani_data_conf):
                if target_ani_name_list and aniname not in target_ani_name_list:
                    continue
                if callable(get_anim_name):
                    aniname = get_anim_name(aniname)
                if aniname not in ani_conf:
                    ani_conf[aniname] = []
                ani_conf[aniname].append([ctrl, aniData, template_conf.get('uniforms', 0)])

        return

    def MergeCfg(self, cfg):
        if '__init_conf__' not in cfg:
            cfg['__init_conf__'] = True
            attr_define = self.create_info[0]
            for aname, default in attr_define:
                if aname not in cfg:
                    cfg[aname] = default

            self.CheckAttributeName(cfg)

    def MergeCustomCfg(self, cfg):
        cfg = CustomCfg(cfg, self.ctor_cls)
        if '__init_conf__' not in cfg:
            cfg['__init_conf__'] = True
            self.CheckAttributeName(cfg)
        return cfg

    def CheckAttributeName(self, cfg):
        for checker in self.check_func_list:
            checker(cfg)