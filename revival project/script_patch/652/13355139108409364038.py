# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/LetterOpenShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class LetterOpenShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_ANNIV_LETTER_OPEN'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(LetterOpenShareCreator, self).create(parent)

    def destroy(self):
        super(LetterOpenShareCreator, self).destroy()

    def set_share_info(self):
        pass

    def set_letter_info(self, text):
        if text:
            self.panel.lab_benediction.SetString(text)