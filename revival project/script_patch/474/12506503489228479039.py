# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/rich_text_custom_utils.py


def show_assult_rank_list_imp(titles, contents, **kwargs):
    if type(titles) not in (list, tuple):
        log_error('show_list_imp titles is not list or tuple', titles, contents)
        return None
    else:
        if type(contents) not in (list, tuple):
            log_error('show_list_imp contents is not list or tuple', titles, contents)
            return None
        nd_table = global_data.uisystem.load_template_create('mail/i_mail_table_rank')
        nd_table.lab_rich_table.setVisible(False)
        old_nd_width, old_nd_height = nd_table.GetContentSize()
        old_height_offset = nd_table.lab_rich_table.GetContentSize()[1]
        nd_table.list_title.SetNumPerUnit(len(titles))
        nd_table.list_content.SetNumPerUnit(len(titles))
        nd_table.list_title.SetInitCount(len(titles))
        for idx, title_conf in enumerate(titles):
            title_item = nd_table.list_title.GetItem(idx)
            if type(title_conf) == dict:
                title_item.lab_title.SetString(title_conf.get('txt', ''))
            else:
                title_item.lab_title.SetString(title_conf)

        nd_table.list_title._refreshItemPos()
        nd_table.list_title.UpdateAutoFitChild()
        nd_table.list_content.SetInitCount(len(contents))
        for idx, cont_conf in enumerate(contents):
            cont_item = nd_table.list_content.GetItem(idx)
            if type(cont_conf) == dict:
                cont_item.lab_title.SetString(cont_conf.get('txt', ''))
            else:
                cont_item.lab_title.SetString(cont_conf)

        nd_table.list_content._refreshItemPos()
        title_w, title_h = nd_table.list_title.GetContentSize()
        content_w, content_h = nd_table.list_content.GetContentSize()
        new_height = title_h + content_h + old_height_offset
        nd_table.SetContentSize(old_nd_width, new_height)
        nd_table.list_title.ReConfPosition()
        return nd_table


def show_rank_list_imp(titles, contents, **kwargs):
    if type(titles) not in (list, tuple):
        log_error('show_list_imp titles is not list or tuple', titles, contents)
        return None
    else:
        if type(contents) not in (list, tuple):
            log_error('show_list_imp contents is not list or tuple', titles, contents)
            return None
        nd_table = global_data.uisystem.load_template_create('mail/i_mail_table')
        old_nd_width, old_nd_height = nd_table.GetContentSize()

        def cb(*args):
            from logic.comsys.chat.chat_link import battle_flag_title_jump
            battle_flag_title_jump({})

        nd_table.lab_rich_table.SetCallback(cb)
        old_height_offset = nd_table.lab_rich_table.GetContentSize()[1]
        nd_table.list_title.SetNumPerUnit(len(titles))
        nd_table.list_content.SetNumPerUnit(len(titles))
        nd_table.list_title.SetInitCount(len(titles))
        for idx, title_conf in enumerate(titles):
            title_item = nd_table.list_title.GetItem(idx)
            if type(title_conf) == dict:
                title_item.lab_title.SetString(title_conf.get('txt', ''))
            else:
                title_item.lab_title.SetString(title_conf)

        nd_table.list_content.SetInitCount(len(contents))
        for idx, cont_conf in enumerate(contents):
            cont_item = nd_table.list_content.GetItem(idx)
            if type(cont_conf) == dict:
                cont_item.lab_title.SetString(cont_conf.get('txt', ''))
            else:
                cont_item.lab_title.SetString(cont_conf)

        title_w, title_h = nd_table.list_title.GetContentSize()
        content_w, content_h = nd_table.list_content.GetContentSize()
        new_height = title_h + content_h + old_height_offset
        nd_table.SetContentSize(old_nd_width, new_height)
        nd_table.list_title.ReConfPosition()
        return nd_table


def show_pve_rank_list_imp(titles, contents, **kwargs):
    if type(titles) not in (list, tuple):
        log_error('show_pve_rank_list_imp titles is not list or tuple', titles, contents)
        return None
    else:
        if type(contents) not in (list, tuple):
            log_error('show_pve_rank_list_imp contents is not list or tuple', titles, contents)
            return None
        nd_table = global_data.uisystem.load_template_create('mail/i_mail_table_rank')
        nd_table.lab_rich_table.setVisible(False)
        old_nd_width, old_nd_height = nd_table.GetContentSize()
        old_height_offset = nd_table.lab_rich_table.GetContentSize()[1]
        nd_table.list_title.SetNumPerUnit(len(titles))
        nd_table.list_content.SetNumPerUnit(len(titles))
        nd_table.list_title.SetInitCount(len(titles))
        for idx, title_conf in enumerate(titles):
            title_item = nd_table.list_title.GetItem(idx)
            if type(title_conf) == dict:
                title_item.lab_title.SetString(title_conf.get('txt', ''))
            else:
                title_item.lab_title.SetString(title_conf)

        nd_table.list_title._refreshItemPos()
        nd_table.list_title.UpdateAutoFitChild()
        nd_table.list_content.SetInitCount(len(contents))
        for idx, cont_conf in enumerate(contents):
            cont_item = nd_table.list_content.GetItem(idx)
            if type(cont_conf) == dict:
                cont_item.lab_title.SetString(cont_conf.get('txt', ''))
            else:
                cont_item.lab_title.SetString(cont_conf)

        nd_table.list_content._refreshItemPos()
        title_w, title_h = nd_table.list_title.GetContentSize()
        content_w, content_h = nd_table.list_content.GetContentSize()
        new_height = title_h + content_h + old_height_offset
        nd_table.SetContentSize(old_nd_width, new_height)
        nd_table.list_title.ReConfPosition()
        return nd_table


def show_pve_mecha_rank_list_imp(titles, contents, **kwargs):
    if type(titles) not in (list, tuple):
        log_error('show_pve_mecha_rank_list_imp titles is not list or tuple', titles, contents)
        return None
    else:
        if type(contents) not in (list, tuple):
            log_error('show_pve_mecha_rank_list_imp contents is not list or tuple', titles, contents)
            return None
        nd_table = global_data.uisystem.load_template_create('mail/i_mail_table_rank')
        nd_table.lab_rich_table.setVisible(False)
        old_nd_width, old_nd_height = nd_table.GetContentSize()
        old_height_offset = nd_table.lab_rich_table.GetContentSize()[1]
        nd_table.list_title.SetNumPerUnit(len(titles))
        nd_table.list_content.SetNumPerUnit(len(titles))
        nd_table.list_title.SetInitCount(len(titles))
        for idx, title_conf in enumerate(titles):
            title_item = nd_table.list_title.GetItem(idx)
            if type(title_conf) == dict:
                title_item.lab_title.SetString(title_conf.get('txt', ''))
            else:
                title_item.lab_title.SetString(title_conf)

        nd_table.list_title._refreshItemPos()
        nd_table.list_title.UpdateAutoFitChild()
        nd_table.list_content.SetInitCount(len(contents))
        for idx, cont_conf in enumerate(contents):
            cont_item = nd_table.list_content.GetItem(idx)
            if type(cont_conf) == dict:
                cont_item.lab_title.SetString(cont_conf.get('txt', ''))
            else:
                cont_item.lab_title.SetString(cont_conf)

        nd_table.list_content._refreshItemPos()
        title_w, title_h = nd_table.list_title.GetContentSize()
        content_w, content_h = nd_table.list_content.GetContentSize()
        new_height = title_h + content_h + old_height_offset
        nd_table.SetContentSize(old_nd_width, new_height)
        nd_table.list_title.ReConfPosition()
        return nd_table


def on_click_show_rank_list_imp(msg, element, touch, eventTouch):
    pos = touch.getLocation()
    from logic.gutils.rich_text_utils import get_rich_text_custom_node
    nd_table = get_rich_text_custom_node(element)
    if not nd_table:
        return
    if nd_table.IsDestroyed():
        return
    if nd_table.lab_rich_table.IsPointIn(pos):
        from logic.gutils.jump_to_ui_utils import jump_tp_battle_flag
        from logic.comsys.role.PlayerBattleFlagWidget import TAB_TITLE
        jump_tp_battle_flag(flag_tab=TAB_TITLE)