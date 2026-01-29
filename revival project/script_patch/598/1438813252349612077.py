# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCBFile.py
from __future__ import absolute_import
from __future__ import print_function
from .CCNode import CCNodeCreator

class CCBFileCreator(CCNodeCreator):
    COM_NAME = 'CCBFile'
    ATTR_DEFINE = CCNodeCreator.ATTR_DEFINE + [
     ('ccbFile', 'default/ccbfile_default'),
     (
      'template_info', {})]

    @staticmethod
    def create(parent, root, ccbFile, template_info, size, zorder, scale):
        tconf = global_data.uisystem.load_template(ccbFile, template_info)
        ntconf = global_data.uisystem._modify_template_top_node_attr(tconf, {'size': size,'zorder': zorder,'scale': scale})
        ret = global_data.uisystem.create_item(ntconf, parent, None)
        if root:
            root.ReportCCBFile(ccbFile, ret)
        if ret:
            global_data.uisystem.BindWidgetSoundName(ccbFile, ret)
        return ret

    @staticmethod
    def set_attr_group_name(obj, parent, root, name, assign_root, zorder, attach_data):
        if assign_root and name and root is not obj:
            setattr(root, name, obj)
        if parent is None:
            return
        else:
            obj._attach_data = attach_data
            if parent is not None and name is not None:
                parent.AddChildRecord(name, obj)
                obj.widget_name = name
            return
            if parent is None:
                return
            print('--------------set_attr_group_name--------------------------', obj)
            print(name, assign_root, parent)
            print(root)
            parent.AddChild(name, obj, zorder)
            return

    @staticmethod
    def set_attr_group_size(obj, parent, root, size):
        pass