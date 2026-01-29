# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/cocos_ps_blend_mode_utils.py
from __future__ import absolute_import
PS_BLEND_NONE = 0
PS_BLEND_MULTIPLY = 1
PS_BLEND_SCREEN = 2
PS_BLEND_LINEAR_DODGE_ADD_APPROX = 3
PS_BLEND_NONE_FACTORS = 0
PS_BLEND_MULTIPLY_FACTORS = 1
PS_BLEND_SCREEN_FIRST_PASS_FACTORS = 2
PS_BLEND_SCREEN_SECOND_PASS_FACTORS = 3
PS_BLEND_LINEAR_DODGE_ADD_APPROX_FACTORS = 4
PS_BLEND_FACTORS_MAP = {PS_BLEND_NONE_FACTORS: ('BLEND_ONE', 'BLEND_INVSRCALPHA'),
   PS_BLEND_MULTIPLY_FACTORS: ('BLEND_ZERO', 'BLEND_SRCCOLOR'),
   PS_BLEND_SCREEN_FIRST_PASS_FACTORS: ('BLEND_ZERO', 'BLEND_SRCCOLOR'),
   PS_BLEND_SCREEN_SECOND_PASS_FACTORS: ('BLEND_SRCALPHA', 'BLEND_ONE'),
   PS_BLEND_LINEAR_DODGE_ADD_APPROX_FACTORS: ('BLEND_SRCALPHA', 'BLEND_ONE')
   }
PS_BLEND_PASS_MAP = {PS_BLEND_NONE: (
                 PS_BLEND_NONE_FACTORS,),
   PS_BLEND_MULTIPLY: (
                     PS_BLEND_MULTIPLY_FACTORS,),
   PS_BLEND_SCREEN: (
                   PS_BLEND_SCREEN_FIRST_PASS_FACTORS, PS_BLEND_SCREEN_SECOND_PASS_FACTORS),
   PS_BLEND_LINEAR_DODGE_ADD_APPROX: (
                                    PS_BLEND_LINEAR_DODGE_ADD_APPROX_FACTORS,)
   }

def get_ps_blend_factors_list(ps_blend_mode):
    passes = PS_BLEND_PASS_MAP.get(ps_blend_mode, None)
    if passes is None:
        return
    else:
        ret = []
        for factors_type in passes:
            factors = get_ps_blend_factors(factors_type)
            if factors is None:
                continue
            ret.append(factors)

        return ret


def get_ps_blend_factors(ps_blend_factors_type):
    factor_pair = PS_BLEND_FACTORS_MAP.get(ps_blend_factors_type, None)
    if factor_pair is None:
        return
    else:
        src_str, dst_str = factor_pair
        from common.utils.cocos_utils import BlendFactorDict
        src_factor = BlendFactorDict.get(src_str, None)
        dst_factor = BlendFactorDict.get(dst_str, None)
        if src_factor is None or src_factor is None:
            return
        return (src_factor, dst_factor)


def replace_multiply_shader(node):
    from common.utils import cocos_utils
    state = cocos_utils.create_program_state_by_path('common/shader/cocosui', 'positiontexturecolor_nomvp_ps_multiply')
    node.setGLProgramState(state)


def replace_screen_first_pass_shader(node):
    from common.utils import cocos_utils
    state = cocos_utils.create_program_state_by_path('common/shader/cocosui', 'positiontexturecolor_nomvp_ps_screen_first_pass')
    node.setGLProgramState(state)


def update_second_pass_opacity(parent, node):
    if not parent.isCascadeOpacityEnabled():
        node.setOpacity(parent.getDisplayedOpacity())
    else:
        node.setOpacity(255)