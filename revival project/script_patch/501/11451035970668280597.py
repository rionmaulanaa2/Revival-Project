# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/cocomate.py
from __future__ import absolute_import
import json
import ccui
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from common.uisys.uielment.CCUIText import CCUIText
from common.uisys.uielment.CCUIButton import CCUIButton
from common.uisys.uielment.CCRichText import CCRichText
from common.uisys.uielment.CCLabelAtlas import CCLabelAtlas
from common.uisys.uielment.CCEditBoxExt import CCEditBoxExt
from common.uisys.uielment.CCLabelBMFont import CCLabelBMFont
from common.uisys.uielment.NewCCUIListView import CCHorzAsyncList_CSB, CCVerAsyncList_CSB
from common.uisys.uielment.CCScrollView import VIEW_CHILD_TAG
com_attr_name = 'ComAttributeCocomate'
key_label_text = 'Cocomate_LabelText'
key_button_text = 'Cocomate_ButtonText'
key_placeholder_text = 'Cocomate_PlaceHolderText'
key_is_project_node = 'Cocomate_IsProjectNode'
key_ext_data = 'Cocomate_ExtData'
key_type_name = 'ccm_type_name'
key_splendor_filename = 'Splendor_FileName'
key_splendor_texturekey = 'Splendor_Texture'
LAYOUT_COCOMATE_COMPONENT_NAME = '__ui_layout_cocomate'
ASSIGN_TO_NONE = 0
ASSIGN_TO_PARENT = 1
ASSIGN_TO_ROOT = 2
SCRIPT_ATTR_NAME = 'script_widget'
SCRIPT_BIND_NAME = 'script_name'
REFUSE_BIND_TAG = 77758520
GLOBAL_NUM = 0
_reload_all = True
cocomate_type_to_script_type = {'CCHorzAsyncList': CCHorzAsyncList_CSB,
   'CCVerAsyncList': CCVerAsyncList_CSB
   }

def get_csb_filename(file_name):
    import os
    if file_name:
        p, ext = os.path.splitext(file_name)
        if p.startswith('gui/template/'):
            ret = p[len('gui/template/'):]
            return ret
        else:
            return p

    return ''


def get_cocomate_layout(node):
    return node.getComponent(LAYOUT_COCOMATE_COMPONENT_NAME)


def wrap_cocos_node(node):
    from common.uisys.ui_proxy import trans2ProxyObj, getProxyObj
    if not node:
        return None
    else:
        ccm_ty = node.getCCMTypeName()
        if ccm_ty not in cocomate_type_to_script_type:
            return trans2ProxyObj(node)
        ret = getProxyObj(node)
        if ret:
            return ret
        return cocomate_type_to_script_type[ccm_ty](node)
        return None


def get_node_children_for_bind(node):
    normal_children = node.getChildren()
    if isinstance(node, ccui.ScrollView):
        container = node.getInnerContainer()
        speical_children = container.getProtectedChildrenByTag(VIEW_CHILD_TAG)
        return normal_children + speical_children
    else:
        return normal_children


def bind_child(node, attributes=None, is_clone=False):
    global GLOBAL_NUM
    GLOBAL_NUM = 0
    proxy_node = wrap_cocos_node(node)
    proxy_node.store_name()
    for child in get_node_children_for_bind(node):
        bind_name(proxy_node, child, proxy_node, attributes, is_clone=is_clone)

    csb_init(proxy_node)
    if not is_clone:
        fix_node_for_language(proxy_node)
        localize(proxy_node, None)
    return proxy_node


def bind_names(root, node=None, parent=None, attributes=None, action_func=None):
    global GLOBAL_NUM
    GLOBAL_NUM = 0
    if root is None:
        bind_child(node)
    else:
        node_proxy = bind_name(root, node, parent, attributes, action_func)
    return


def bind_name(root, node=None, parent=None, attributes=None, action_func=None, is_clone=False):
    parent = parent or root
    com_attr = node.getComponent(com_attr_name)
    if root is not node:
        node_proxy = bind_one_name(root, node, parent, attributes, com_attr)
    else:
        node_proxy = root
    is_project_node = com_attr and com_attr.getBool(key_is_project_node, False)
    is_project_node and action_func and action_func(node_proxy.GetFileName_csb(), node_proxy)
    if is_project_node:
        ccbFile = node_proxy.GetFileName_csb()
        if root:
            root.ReportCCBFile(ccbFile, node_proxy)
        global_data.uisystem.BindWidgetSoundName(ccbFile, node_proxy)
    for child in get_node_children_for_bind(node):
        if is_project_node:
            if child.getIsDirectChildInCocomate():
                bind_name(node_proxy, child, node_proxy, action_func=action_func, is_clone=is_clone)
            else:
                bind_name(root, child, node_proxy, action_func=action_func, is_clone=is_clone)
        else:
            bind_name(root, child, node_proxy, attributes, action_func=action_func, is_clone=is_clone)

    csb_init(node_proxy)
    if not is_clone:
        fix_node_for_language(node_proxy)
        localize(node_proxy, com_attr)
    return node_proxy


def bind_one_name(root, node, parent=None, _=None, com_attr=None):
    global GLOBAL_NUM
    if not com_attr:
        com_attr = node.getComponent(com_attr_name)
    script_widget = wrap_cocos_node(node)
    script_widget.store_name()
    if not script_widget:
        raise ValueError('bind_one_name error!!!!', node, script_widget)
    if global_data.is_inner_server:
        if not script_widget.GetName():
            node.setName('@%s%s@' % (script_widget.__class__.__name__, GLOBAL_NUM))
            GLOBAL_NUM += 1
    name = script_widget.GetName()
    if name:
        setattr(root, name, script_widget)
        if parent:
            setattr(parent, name, script_widget)
            parent.AddChildRecord(name, script_widget)
        else:
            setattr(root, name, script_widget)
    elif parent:
        parent.AddChildRecord(name, script_widget)
    return script_widget


def get_cocomate_node_by_cocos_node(node, check=False, bind=True):
    from common.uisys.uielment.CCNode import CCNode
    if check and isinstance(node, CCNode):
        return node
    if bind:
        return wrap_cocos_node(node)


def fix_node_for_language(node_proxy):
    node_name = node_proxy.GetName()
    if not (node_name and node_name.startswith('nd_multilang_')):
        return
    else:
        def_node = None
        lang_code_node = None
        final_node_name = ''
        all_lang_node = []
        lang_name = get_cur_lang_name()
        cur_lang_name_lower = lang_name.lower()
        for child in node_proxy.getChildren():
            name = child.getName()
            if not name:
                continue
            oversea_name_list = name.split('_OV_')
            if oversea_name_list and len(oversea_name_list) == 2:
                real_name, lang_name = oversea_name_list
                final_node_name = real_name
                all_lang_node.append(child)
                if lang_name.lower() == cur_lang_name_lower:
                    lang_code_node = child
                elif lang_name.lower() == 'default':
                    def_node = child
                else:
                    continue

        show_node = lang_code_node or def_node
        if show_node:
            for child in all_lang_node:
                if child != show_node:
                    child.setVisible(False)
                else:
                    child.setVisible(True)
                    child.setName(final_node_name)

        return


def localize(root, com_attr=None, recursive=False):
    if not com_attr:
        com_attr = root.getComponent(com_attr_name)
    if com_attr:
        root_type = type(root)
        if root_type in [CCUIText, CCRichText, CCLabelBMFont, CCLabelAtlas]:
            txt = com_attr.getString(key_label_text, '')
            if txt and txt.isdigit():
                root.SetString(int(txt))
            elif root_type in [CCUIText, CCRichText]:
                root.UpdateAutoFitChild()
        elif root_type is CCUIButton:
            if root.getTitleRenderer():
                txt = com_attr.getString(key_button_text, '')
                if txt and txt.isdigit():
                    root.SetText(int(txt))
        elif root_type is CCEditBoxExt:
            txt = com_attr.getString(key_label_text, '')
            if txt and txt.isdigit():
                root.setString(int(txt))
            text = com_attr.getString(key_placeholder_text, '')
            if text and text.isdigit():
                root.setPlaceHolder(get_text_by_id(text))
    if recursive:
        for child in get_node_children_for_bind(root):
            child = get_cocomate_node_by_cocos_node(child)
            localize(child, recursive=True)


def recursive_do_language_things(root, recursive=False):
    localize(root)
    fix_node_for_language(root)
    if recursive:
        for child in get_node_children_for_bind(root):
            child = get_cocomate_node_by_cocos_node(child)
            recursive_do_language_things(child, recursive=True)


def csb_init(root):
    root.csb_init()
    from common.uisys.uielment.CCScrollView import CCScrollView
    if isinstance(root, CCScrollView):
        root.SyncAttrToContainer()


def init_clone_base_node(root):
    proxy_node = wrap_cocos_node(root)
    localize(proxy_node, None, recursive=True)
    do_cocomate_layout(root, False, True)
    return proxy_node


def get_ext_data(node, key=None, default=None):
    data = getattr(node, key_ext_data, None)
    if not data:
        com_attr = node.getComponent(com_attr_name)
        if com_attr:
            json_str = com_attr.getString(key_ext_data, '')
            if json_str != '':
                data = json.loads(json_str)
                setattr(node, key_ext_data, data)
    if data:
        if key is None:
            return data
        else:
            return data.get(key, default)

    else:
        return default
    return


def do_cocomate_layout(node, do_self=True, includeSpecialChildren=False):
    node and ccui.Helper.doCocomateLayout(node, do_self, includeSpecialChildren)