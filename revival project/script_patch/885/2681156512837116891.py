# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/__init__.py
from __future__ import absolute_import
import six
import sys
__widget_class_dict = {}

def __widget_class(widget_type):
    global __widget_class_dict
    if widget_type in __widget_class_dict:
        widget_class = __widget_class_dict[widget_type]
    else:
        mpath = 'logic.comsys.activity.widget.%s' % widget_type
        mod = sys.modules.get(mpath, None)
        if mod is None:
            mod = __import__(mpath, globals(), locals(), [widget_type])
        widget_class = __widget_class_dict[widget_type] = getattr(mod, widget_type, None)
    return widget_class


def widget(*widget_types):

    def _uiclass(cls):
        on_init_panel = cls.on_init_panel
        on_finalize_panel = cls.on_finalize_panel
        refresh_panel = cls.refresh_panel

        def _on_init_panel--- This code section failed: ---

  27       0  LOAD_DEREF            0  'on_init_panel'
           3  LOAD_FAST             0  'self'
           6  CALL_FUNCTION_1       1 
           9  POP_TOP          

  28      10  BUILD_MAP_0           0 
          13  LOAD_FAST             0  'self'
          16  STORE_ATTR            0  '_widgets'

  29      19  SETUP_LOOP           48  'to 70'
          22  LOAD_DEREF            1  'widget_types'
          25  GET_ITER         
          26  FOR_ITER             40  'to 69'
          29  STORE_FAST            1  'widget_type'

  30      32  LOAD_GLOBAL           1  '__widget_class'
          35  LOAD_FAST             1  'widget_type'
          38  CALL_FUNCTION_1       1 
          41  LOAD_FAST             0  'self'
          44  LOAD_ATTR             2  'panel'
          47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             3  '_activity_type'
          53  CALL_FUNCTION_2       2 
          56  LOAD_FAST             0  'self'
          59  LOAD_ATTR             0  '_widgets'
          62  LOAD_FAST             1  'widget_type'
          65  STORE_SUBSCR     
          66  JUMP_BACK            26  'to 26'
          69  POP_BLOCK        
        70_0  COME_FROM                '19'

  32      70  LOAD_GLOBAL           4  'hasattr'
          73  LOAD_GLOBAL           1  '__widget_class'
          76  CALL_FUNCTION_2       2 
          79  POP_JUMP_IF_FALSE   107  'to 107'
          82  LOAD_GLOBAL           5  'getattr'
          85  LOAD_GLOBAL           1  '__widget_class'
          88  CALL_FUNCTION_2       2 
        91_0  COME_FROM                '79'
          91  POP_JUMP_IF_FALSE   107  'to 107'

  33      94  LOAD_FAST             0  'self'
          97  LOAD_ATTR             6  'post_init_widget'
         100  CALL_FUNCTION_0       0 
         103  POP_TOP          
         104  JUMP_FORWARD          0  'to 107'
       107_0  COME_FROM                '104'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 76

        def _on_finalize_panel(self):
            on_finalize_panel(self)
            for widget in six.itervalues(self._widgets):
                widget.on_finalize_panel()

            self._widgets.clear()

        def _refresh_panel(self):
            refresh_panel(self)
            for widget in six.itervalues(self._widgets):
                widget.refresh_panel()

        cls.on_init_panel = _on_init_panel
        cls.on_finalize_panel = _on_finalize_panel
        cls.refresh_panel = _refresh_panel
        return cls

    return _uiclass