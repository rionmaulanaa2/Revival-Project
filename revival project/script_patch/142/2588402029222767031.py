# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartGenLut.py
from __future__ import absolute_import
from . import PartTestBase
import math3d
import game3d
import world
import render
from common.framework import Functor

class PartGenLut(PartTestBase.PartTestBase):

    def __init__(self, scene, name):
        super(PartGenLut, self).__init__(scene, name)

    def init_lut_pipeline(self, auto_exit=False):
        if hasattr(game3d, 'set_window_size_force'):
            game3d.set_window_size_force(1024, 35, 32, 1)
            game3d.set_window_size_force(1024, 32, 32, 1)
        else:
            game3d.set_window_size(1024, 32, 32, 1)
        global_data.display_agent.set_pipeline('common/pipeline/pipeline_lut_gen.xml')
        global_data.display_agent.set_longtime_post_process_active('tonemap_gen', True)
        game3d.delay_exec(3, self.init_prams)

    def mat_set_var(self, mat, name, value):
        _HASH_name = game3d.calc_string_hash(name)
        mat.set_var(_HASH_name, name, value)

    def init_prams(self, auto_exit=False):
        Slope = 0.9
        Toe = 0.45
        Shoulder = 1.0
        BlackClip = 0.0
        WhiteClip = 0.01
        WhiteTemp = 6500.0
        WhiteTint = 0.0
        Saturation = (1.0, 1.0, 1.0, 1.0)
        Contrast = (1.0, 1.0, 1.0, 1.0)
        Gamma = (1.0, 1.0, 1.0, 1.0)
        Gain = (1.0, 1.0, 1.0, 1.0)
        Offset = (0.0, 0.0, 0.0, 0.0)
        SaturationShadows = (1.0, 1.0, 1.0, 1.0)
        ContrastShadows = (1.0, 1.0, 1.0, 1.0)
        GammaShadows = (1.0, 1.0, 1.0, 1.0)
        GainShadows = (1.0, 1.0, 1.0, 1.0)
        OffsetShadows = (0.0, 0.0, 0.0, 0.0)
        CorrectionShadowsMax = 0.09
        SaturationMidtones = (1.0, 1.0, 1.0, 1.0)
        ContrastMidtones = (1.0, 1.0, 1.0, 1.0)
        GammaMidtones = (1.0, 1.0, 1.0, 1.0)
        GainMidtones = (1.0, 1.0, 1.0, 1.0)
        OffsetMidtones = (0.0, 0.0, 0.0, 0.0)
        SaturationHighlights = (1.0, 1.0, 1.0, 1.0)
        ContrastHighlights = (1.0, 1.0, 1.0, 1.0)
        GammaHighlights = (1.0, 1.0, 1.0, 1.0)
        GainHighlights = (1.0, 1.0, 1.0, 1.0)
        OffsetHighlights = (0.0, 0.0, 0.0, 0.0)
        CorrectionHighlightsMin = 0.5
        BlueCorrection = 0.6
        ExpandGamut = 1.0
        SceneColorTint = [255, 255, 255]
        ColorGradingLut = ''
        LutWeight = 1.0
        LutSize = 16.0
        mat = global_data.display_agent.get_post_effect_pass_mtl('tonemap_gen', 0)
        lut_enable = 'TRUE' if ColorGradingLut else 'FALSE'
        mat.set_macro('USE_COLOR_GRADING_LUT', lut_enable)
        mat.rebuild_tech()
        self.mat_set_var(mat, 'Slope', Slope)
        self.mat_set_var(mat, 'Toe', Toe)
        self.mat_set_var(mat, 'Shoulder', Shoulder)
        self.mat_set_var(mat, 'BlackClip', BlackClip)
        self.mat_set_var(mat, 'WhiteClip', WhiteClip)
        self.mat_set_var(mat, 'WhiteTemp', WhiteTemp)
        self.mat_set_var(mat, 'WhiteTint', WhiteTint)
        self.mat_set_var(mat, 'ColorSaturation', Saturation)
        self.mat_set_var(mat, 'ColorContrast', Contrast)
        self.mat_set_var(mat, 'ColorGamma', Gamma)
        self.mat_set_var(mat, 'ColorGain', Gain)
        self.mat_set_var(mat, 'ColorOffset', Offset)
        self.mat_set_var(mat, 'ColorSaturationShadows', SaturationShadows)
        self.mat_set_var(mat, 'ColorContrastShadows', ContrastShadows)
        self.mat_set_var(mat, 'ColorGammaShadows', GammaShadows)
        self.mat_set_var(mat, 'ColorGainShadows', GainShadows)
        self.mat_set_var(mat, 'ColorOffsetShadows', OffsetShadows)
        self.mat_set_var(mat, 'ColorCorrectionShadowsMax', CorrectionShadowsMax)
        self.mat_set_var(mat, 'ColorSaturationMidtones', SaturationMidtones)
        self.mat_set_var(mat, 'ColorContrastMidtones', ContrastMidtones)
        self.mat_set_var(mat, 'ColorGammaMidtones', GammaMidtones)
        self.mat_set_var(mat, 'ColorGainMidtones', GainMidtones)
        self.mat_set_var(mat, 'ColorOffsetMidtones', OffsetMidtones)
        self.mat_set_var(mat, 'ColorSaturationHighlights', SaturationHighlights)
        self.mat_set_var(mat, 'ColorContrastHighlights', ContrastHighlights)
        self.mat_set_var(mat, 'ColorGammaHighlights', GammaHighlights)
        self.mat_set_var(mat, 'ColorGainHighlights', GainHighlights)
        self.mat_set_var(mat, 'ColorOffsetHighlights', OffsetHighlights)
        self.mat_set_var(mat, 'ColorCorrectionHighlightsMin', CorrectionHighlightsMin)
        self.mat_set_var(mat, 'BlueCorrection', BlueCorrection)
        self.mat_set_var(mat, 'ExpandGamut', ExpandGamut)
        self.mat_set_var(mat, 'SceneColorTint', (SceneColorTint[0] / 255.0, SceneColorTint[1] / 255.0, SceneColorTint[2] / 255.0))
        self.mat_set_var(mat, 'LutWeight', LutWeight)
        self.mat_set_var(mat, 'LutSize', LutSize)
        if ColorGradingLut:
            _HASH_ColorGradingLut = game3d.calc_string_hash('ColorGradingLut')
            lut_tex = render.texture(ColorGradingLut)
            mat.set_texture(_HASH_ColorGradingLut, 'ColorGradingLut', lut_tex)
        callback = auto_exit and game3d.exit or None
        game3d.delay_exec(3, Functor(render.save_screen_to_file, 'res/lut_gen.bmp', render.IFF_BMP, 0, 2, callback, True))
        return

    def test_model(self):
        scn = self.scene()
        model = world.model('common/invalidres/model.gim', scn)
        model.position = math3d.vector(0, -50, 50)
        trans = self.scene().active_camera.transformation
        trans.translation = math3d.vector(0, 0, -100)
        self.scene().active_camera.transformation = trans

    def on_enter(self):
        self.test_model()
        game3d.delay_exec(3, self.init_lut_pipeline)

    def on_exit(self):
        pass