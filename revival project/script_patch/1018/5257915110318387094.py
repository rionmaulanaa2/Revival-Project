# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/MontageEditor/EditorUIHelper.py
from cocosui import cc, ccui

class UIHelper(object):

    def __init__(self, ui):
        self.ui = ui
        self.subTitleText = None
        self.optionsText = None
        self.imageView = None
        self.screenWidth = global_data.ui_mgr.design_screen_size.width
        self.screenHeight = global_data.ui_mgr.design_screen_size.height
        self.currentOptions = None
        if global_data.use_sunshine:
            self.keyListener = cc.EventListenerKeyboard.create()
            self.keyListener.setOnKeyPressedCallback(self.onKeyDown)
            dispatcher = cc.Director.getInstance().getEventDispatcher()
            dispatcher.addEventListenerWithFixedPriority(self.keyListener, 1)
        else:
            self.keyListener = None
        self._idPointer = 0
        return

    def getId(self):
        self._idPointer += 1
        return self._idPointer

    def _createText(self):
        text = ccui.Text.create()
        text.setFontName('font/DroidSansFallback.ttf')
        text.setFontSize(40)
        text.setTextColor(cc.Color4B(255, 255, 255, 255))
        text.setString('')
        text.setContentSize(cc.Size(700, 150))
        text.setAnchorPoint(cc.Vec2(0.5, 0))
        posX = self.screenWidth / 2
        posY = 50
        text.setPosition(posX, posY)
        self.ui.addChild(text)
        return text

    def _createImageView(self):
        imageView = ccui.ImageView.create('')
        imageView.setAnchorPoint(cc.Vec2(0, 0))
        imageView.setPositionType(1)
        imageView.setSizeType(1)
        self.ui.addChild(imageView)
        return imageView

    def showText(self, text, color=None, fontSize=None):
        if self.subTitleText is None:
            self.subTitleText = self._createText()
        self.subTitleText.setString(text)
        if color:
            while len(color) < 4:
                color.append(255)

            self.subTitleText.setTextColor(cc.Color4B(*color))
        if fontSize:
            self.subTitleText.setFontSize(fontSize)
        self.subTitleText.setVisible(True)
        return

    def hideText(self):
        if self.subTitleText is not None:
            self.subTitleText.setVisible(False)
        return

    def showImage(self, image, position=(0, 0), size=(1, 1), origin=False):
        if self.imageView is None:
            self.imageView = self._createImageView()
        self.imageView.loadTexture(image)
        contentSize = self.imageView.getContentSize()
        self.imageView.setPosition(self.screenWidth * position[0], self.screenHeight * position[1])
        if origin:
            self.imageView.setScale(size[0], size[1])
        else:
            self.imageView.setScale((self.screenWidth / contentSize.width if contentSize.width > 0 else 1) * size[0], (self.screenHeight / contentSize.height if contentSize.height > 0 else 1) * size[1])
        self.imageView.setVisible(True)
        return

    def hideImage(self):
        if self.imageView is not None:
            self.imageView.setVisible(False)
        return

    def showOptions(self, title='', options=None, waitTime=3.0, overtimeCallback=None):
        if self.optionsText is None:
            self.optionsText = self._createText()
        self.optionsText.setString('%s: %s' % (title, '|'.join([ '%i:%s' % (i, option[0]) for i, option in enumerate(options) ])))
        self.optionsText.setVisible(True)
        self.currentOptions = options

        def onOvertime():
            if self.currentOptions:
                if callable(overtimeCallback):
                    overtimeCallback()

        self.optionsText.runAction(cc.Sequence.create([
         cc.DelayTime.create(waitTime),
         cc.CallFunc.create(onOvertime)]))
        return

    def hideOptions(self):
        if self.optionsText is not None:
            self.optionsText.setVisible(False)
        self.currentOptions = None
        return

    def onKeyDown(self, key, event):
        if self.currentOptions is None:
            return
        else:
            choise = key - 76
            if choise < 0 or choise >= len(self.currentOptions):
                return
            self.currentOptions[choise][1]()
            return