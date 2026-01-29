# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/device_compatibility.py
from __future__ import absolute_import
from __future__ import print_function
import six
import game3d
import render
import profiling
import world
import exception_hook
import os
import package_utils
from common.utils.path import get_neox_dir, QUALITY_FILE_NAME
import json
import zlib
import six.moves.builtins
import device_limit
MALI_GPU_WITH_ATSC_LOAD_ERROR_OVER_2048 = [
 'Mali-T880', 'Mali-T860', 'Mali-T830']
DEVICE_NEED_DISABLE_GPU_SKIN = ('Adreno (TM) 308', )
DEVICE_NAME_NEED_DISABLE_GPU_SKIN = ()
LIMIT_GPU_SKIN_MAX_BONE_CNT = 30
DEVICE_NEED_LIMIT_GPU_SKIN = {}
GL_INVALIDATE_MODEL_LIST = ('moto g(8) power lite', 'PCKM80', 'CPH1945', 'CPH1951',
                            'PCDM10', 'PCDT10', 'cph1979')
PERF_FLAG_ANDROID_LOW = 0
PERF_FLAG_IOS_LOW = 2
PERF_FLAG_IOS_MED = 3
PERF_FLAG_IOS_HIGH = 5
PERF_FLAG_ANDROID_MED = 1
PERF_FLAG_ANDROID_HIGH = 4
MALI_BLACK_LIST = ('Mali-2', 'Mali-3', 'Mali-4', 'Mali-T6', 'Mali-T7')
MALI_MED_LIST = ('Mali-T8', )
ADRENO_BLACK_LIST = ('2', '3', '4')
ADRENO_MED_LIST = ('5', )
HDR_ADRENO_BLACK_LIST = (305, 306, 308)
IPAD_MINI_MODEL_SERIES = frozenset([
 'iPad2,5', 'iPad2,6', 'iPad2,7',
 'iPad4,4', 'iPad4,5', 'iPad4,6',
 'iPad4,7', 'iPad4,8', 'iPad4,9',
 'iPad5,1', 'iPad5,2',
 'iPad11,1', 'iPad11,2'])
IPAD_MINI_HIGH_PPI_MODEL_SERIES = frozenset([
 'iPad4,4', 'iPad4,5', 'iPad4,6',
 'iPad4,7', 'iPad4,8', 'iPad4,9',
 'iPad5,1', 'iPad5,2',
 'iPad11,1', 'iPad11,2'])
GPU_DISABLE_SHADER_COMPILED_DATA_DISCARD = ()
PACKAGE_QUALITY_INIT = -1
PACKAGE_QUALITY_LOW_END = 1
PACKAGE_QUALITY_HIGH_END = 2
INGAME_PACKAGE_COMPABILITY = None
DEBUG_PERF_FLAG = None
RENDER_SYS_NAME = render.get_render_system_name()
IS_DX = False
IS_DX9 = False
IS_DX11 = False
if RENDER_SYS_NAME:
    IS_DX = 'DirectX' in RENDER_SYS_NAME
    IS_DX9 = 'DirectX 9' in RENDER_SYS_NAME
    IS_DX11 = 'DirectX 11' in RENDER_SYS_NAME
MTL_DEVICE_LOWLOW = 4000
MTL_DEVICE_LOW = 5000
MTL_DEVICE_MED = 6000
MTL_DEVICE_HIGH = 7000

def init_gpu_skin():
    gpu_name = profiling.get_video_card_name()
    device_name = profiling.get_device_model()
    for item in DEVICE_NEED_DISABLE_GPU_SKIN:
        if item in gpu_name:
            world.enable_gpu_skin(False)
            print('[COMPATIBILITY] %s has to disable GPU-SKIN...' % gpu_name)

    for item in DEVICE_NAME_NEED_DISABLE_GPU_SKIN:
        if item in device_name:
            world.enable_gpu_skin(False)
            print('[COMPATIBILITY] %s has to disable GPU-SKIN(with device_name)' % device_name)

    if hasattr(world, 'set_gpu_skin_max_bone'):
        print('[COMPATIBILITY] Start DEVICE_NEED_LIMIT_GPU_SKIN CHECK...')
        for item in DEVICE_NEED_LIMIT_GPU_SKIN:
            if item in gpu_name:
                max_cnt = DEVICE_NEED_LIMIT_GPU_SKIN.get(item, None)
                if max_cnt is not None:
                    world.set_gpu_skin_max_bone(max_cnt)
                    print('[COMPATIBILITY] %s has to limit GPU-SKIN-MAX-BONE TO %d...' % (gpu_name, max_cnt))

    else:
        print('[COMPATIBILITY] Cur engine version has NO DEVICE_NEED_LIMIT_GPU_SKIN CHECK...')
    if device_limit.is_running_gles2():
        print('[COMPATIBILITY] %s has to disable GPU-SKIN because running GLES2...' % gpu_name)
        world.enable_gpu_skin(False)
    return


def init_shader_compiled_data_discard():
    gpu_name = profiling.get_video_card_name()
    has_disable_gpu = False
    for item in GPU_DISABLE_SHADER_COMPILED_DATA_DISCARD:
        if item in gpu_name:
            has_disable_gpu = True
            break

    if not has_disable_gpu:
        render.enable_shader_compiled_data_discard(True)


def init_gl_api_compatibility():
    if hasattr(render, 'set_gl_map_invalidate_range_bit_enable'):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            device_model = profiling.get_device_model()
            for device_item in GL_INVALIDATE_MODEL_LIST:
                if device_item in device_model:
                    print('device:%s set_gl_map_invalidate_range_bit_enable False...' % device_model)
                    render.set_gl_map_invalidate_range_bit_enable(False)


def configure_device_performance--- This code section failed: ---

 193       0  SETUP_EXCEPT        127  'to 130'

 194       3  LOAD_GLOBAL           0  'is_device_gpu_qualified'
           6  CALL_FUNCTION_0       0 
           9  UNARY_NOT        
          10  LOAD_GLOBAL           1  'six'
          13  LOAD_ATTR             2  'moves'
          16  LOAD_ATTR             3  'builtins'
          19  LOAD_ATTR             4  '__dict__'
          22  LOAD_CONST            1  'DEVICE_WARNING'
          25  STORE_SUBSCR     

 196      26  LOAD_GLOBAL           5  'profiling'
          29  LOAD_ATTR             6  'get_total_memory'
          32  CALL_FUNCTION_0       0 
          35  STORE_FAST            0  'mem'

 197      38  STORE_FAST            2  'e'
          41  COMPARE_OP            0  '<'
          44  JUMP_IF_FALSE_OR_POP    65  'to 65'
          47  LOAD_GLOBAL           7  'game3d'
          50  LOAD_ATTR             8  'get_platform'
          53  CALL_FUNCTION_0       0 
          56  LOAD_GLOBAL           7  'game3d'
          59  LOAD_ATTR             9  'PLATFORM_ANDROID'
          62  COMPARE_OP            2  '=='
        65_0  COME_FROM                '44'
          65  STORE_FAST            1  'mem_forbid'

 198      68  LOAD_GLOBAL          10  'device_limit'
          71  LOAD_ATTR            11  'is_cn_device_limit'
          74  CALL_FUNCTION_0       0 
          77  JUMP_IF_TRUE_OR_POP   110  'to 110'
          80  LOAD_GLOBAL           1  'six'
          83  LOAD_ATTR             2  'moves'
          86  LOAD_ATTR             3  'builtins'
          89  LOAD_ATTR             4  '__dict__'
          92  LOAD_ATTR            12  'get'
          95  LOAD_CONST            3  'DEVICE_LIMIT'
          98  LOAD_GLOBAL          13  'False'
         101  CALL_FUNCTION_2       2 
         104  JUMP_IF_TRUE_OR_POP   110  'to 110'
         107  LOAD_FAST             1  'mem_forbid'
       110_0  COME_FROM                '104'
       110_1  COME_FROM                '77'
         110  LOAD_GLOBAL           1  'six'
         113  LOAD_ATTR             2  'moves'
         116  LOAD_ATTR             3  'builtins'
         119  LOAD_ATTR             4  '__dict__'
         122  LOAD_CONST            3  'DEVICE_LIMIT'
         125  STORE_SUBSCR     
         126  POP_BLOCK        
         127  JUMP_FORWARD         39  'to 169'
       130_0  COME_FROM                '0'

 200     130  DUP_TOP          
         131  LOAD_GLOBAL          14  'Exception'
         134  COMPARE_OP           10  'exception-match'
         137  POP_JUMP_IF_FALSE   168  'to 168'
         140  POP_TOP          
         141  STORE_FAST            2  'e'
         144  POP_TOP          

 201     145  LOAD_GLOBAL          15  'print'
         148  LOAD_CONST            4  'configure_device_performance, error:%s'
         151  LOAD_GLOBAL          16  'str'
         154  LOAD_FAST             2  'e'
         157  CALL_FUNCTION_1       1 
         160  BINARY_MODULO    
         161  CALL_FUNCTION_1       1 
         164  POP_TOP          
         165  JUMP_FORWARD          1  'to 169'
         168  END_FINALLY      
       169_0  COME_FROM                '168'
       169_1  COME_FROM                '127'

Parse error at or near `STORE_FAST' instruction at offset 38


def is_ios_support_astc():
    check_res = True
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        import profiling
        i_platform = profiling.get_device_info()
        if i_platform:
            i_platform = i_platform[3]
            if i_platform in ('iPhone6,1', 'iPhone6,2', 'iPad4,1', 'iPad4,2', 'iPad4,3',
                              'iPad4,4', 'iPad4,5', 'iPad4,6', 'iPad4,7', 'iPad4,8',
                              'iPad4,9'):
                check_res = False
    return check_res


def ios_need_reduce_resolution():
    check_res = False
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        import profiling
        i_platform = profiling.get_device_info()
        if i_platform:
            i_platform = i_platform[3]
            if i_platform in ('iPhone10,3', 'iPhone10,6', 'iPhone11,2', 'iPhone11,4',
                              'iPhone11,6'):
                check_res = True
    return check_res


def ios_low_device_flag():
    check_res = False
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        import profiling
        i_platform = profiling.get_device_info()
        if i_platform:
            i_platform = i_platform[3]
            if i_platform in ('iPhone9,1', 'iPhone9,3', 'iPhone8,4', 'iPhone8,2', 'iPhone8,1',
                              'iPhone7,1', 'iPhone7,2', 'iPhone6,1', 'iPhone6,2',
                              'iPad3,4', 'iPad3,5', 'iPad3,6', 'iPad4,1', 'iPad4,2',
                              'iPad4,3', 'iPad5,1', 'iPad5,2', 'iPad4,4', 'iPad4,5',
                              'iPad4,6', 'iPad4,7', 'iPad4,8', 'iPad4,9'):
                check_res = True
    return check_res


def ios_med_device_flag():
    check_res = False
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        import profiling
        i_platform = profiling.get_device_info()
        if i_platform:
            i_platform = i_platform[3]
            if i_platform in ('iPhone9,2', 'iPhone9,4', 'iPhone10,1', 'iPhone10,4',
                              'iPhone10,2', 'iPhone10,5', 'iPad5,3', 'iPad5,4'):
                check_res = True
    return check_res


def is_ipad():
    check_res = False
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        import profiling
        i_platform = profiling.get_device_info()
        if i_platform:
            if 'iPad' in i_platform[3]:
                check_res = True
    return check_res


def configure_device_setting():
    from common.utils import pc_platform_utils
    render_api_name = render.get_render_system_name()
    print('current render system is [%s]' % render_api_name)
    if G_IS_NA_PROJECT:
        if render_api_name == 'DirectX 9':
            technique_map = 'common\\shader\\technique_map_dx9.xml'
        else:
            technique_map = 'common\\shader\\technique_map_mobile_na.xml'
    elif pc_platform_utils.is_pc_hight_quality():
        technique_map = 'common\\shader\\technique_map_pc_cn.xml'
    else:
        technique_map = 'common\\shader\\technique_map_mobile_cn.xml'
    if technique_map:
        if hasattr(render, 'set_technique_map_file'):
            render.set_technique_map_file(technique_map)
        render.enable_technique_map(True)
    gpu_name = profiling.get_video_card_name()
    print('configure device compatibility with gpu [%s]' % gpu_name)
    from common.utils import package_type
    if package_type.is_android_dds_package():
        print('is android dds package')
    elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
        if not render.is_android_support_astc():
            print('set texture appendix _etc2')
            render.set_texture_appendix('_etc2')
        elif game3d.is_feature_ready('UI_ASTC'):
            print('set texture appendix _astc')
            render.set_texture_appendix('_astc')
    elif game3d.get_platform() == game3d.PLATFORM_IOS:
        if not is_ios_support_astc():
            print('set ios texture appendix _etc2')
            render.set_texture_appendix('_etc2')
        elif game3d.is_feature_ready('UI_ASTC'):
            print('set texture appendix _astc')
            render.set_texture_appendix('_astc')
    if gpu_name in MALI_GPU_WITH_ATSC_LOAD_ERROR_OVER_2048:
        if hasattr(render, 'set_texture_astc_max_size'):
            render.set_texture_astc_max_size(2047)
            print('[COMPATIBILITY] %s has to limit max astc size', gpu_name)
    init_gpu_skin()
    init_shader_compiled_data_discard()
    init_gl_api_compatibility()


def is_running_gles2():
    return render.get_render_system_name() == 'GLES2'


def is_sys_uv_left_bottom():
    return 'GL' in render.get_render_system_name()


def is_device_gpu_qualified():
    if global_data.is_device_gpu_qualified_flag is not None:
        return global_data.is_device_gpu_qualified_flag
    else:
        check_res = True
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            gpu_desc = profiling.get_video_card_name().strip().lower()
            mali_res = True
            gpu_lower = gpu_desc.lower()
            if 'mali' in gpu_lower:
                print('mali gpu', gpu_lower)
                for black_desc in MALI_BLACK_LIST:
                    desc = black_desc.lower()
                    if gpu_lower.find(desc) >= 0:
                        print('GPU CHECK: cur mali is low performance ', gpu_lower)
                        mali_res = False
                        break

            adreno_res = True
            if 'adreno' in gpu_lower:
                print('checking adreno gpu')
                desc_list = gpu_lower.split(' ')
                series = None
                for desc in desc_list:
                    if desc.isdigit():
                        series = int(float(desc))

                print('series of adreno is', series)
                series_str = str(series)
                if len(series_str) > 0:
                    if series_str[0] in ADRENO_BLACK_LIST:
                        print('GPU CHECK: cur adreno is low performance ', series)
                        adreno_res = False
            check_res = mali_res and adreno_res
        global_data.is_device_gpu_qualified_flag = check_res
        return check_res


def get_android_device_perf_level():
    if game3d.get_platform() != game3d.PLATFORM_ANDROID:
        return 0
    else:
        if global_data.is_android_pc or global_data.is_in_mumu:
            return PERF_FLAG_ANDROID_HIGH
        gpu_desc = profiling.get_video_card_name().strip().lower()
        gpu_lower = gpu_desc.lower()
        if 'mali' in gpu_lower:
            for black_desc in MALI_BLACK_LIST:
                desc = black_desc.lower()
                if gpu_lower.find(desc) >= 0:
                    print('get_android_device_perf_level: cur mali is low performance ', gpu_lower)
                    return PERF_FLAG_ANDROID_LOW

            for black_desc in MALI_MED_LIST:
                desc = black_desc.lower()
                if gpu_lower.find(desc) >= 0:
                    print('get_android_device_perf_level: cur mali is med performance ', gpu_lower)
                    return PERF_FLAG_ANDROID_MED

            return PERF_FLAG_ANDROID_HIGH
        if 'adreno' in gpu_lower:
            desc_list = gpu_lower.split(' ')
            series = None
            for desc in desc_list:
                if desc.isdigit():
                    series = int(float(desc))

            print('series of adreno is', series)
            series_str = str(series)
            if len(series_str) > 0:
                if series_str[0] in ADRENO_BLACK_LIST:
                    print('get_android_device_perf_level: cur adreno is low performance ', series)
                    return PERF_FLAG_ANDROID_LOW
                if series_str[0] in ADRENO_MED_LIST:
                    print('get_android_device_perf_level: cur adreno is med performance ', series)
                    return PERF_FLAG_ANDROID_MED
            return PERF_FLAG_ANDROID_HIGH
        return PERF_FLAG_ANDROID_MED


def get_device_perf_flag():
    if DEBUG_PERF_FLAG is not None:
        return DEBUG_PERF_FLAG
    else:
        if global_data.is_android_pc or global_data.is_in_mumu:
            return PERF_FLAG_IOS_HIGH
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            if ios_low_device_flag():
                return PERF_FLAG_IOS_LOW
            else:
                if ios_med_device_flag():
                    return PERF_FLAG_IOS_MED
                return PERF_FLAG_IOS_HIGH

        elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
            return get_android_device_perf_level()
        return PERF_FLAG_IOS_HIGH


def get_device_level():
    from common.cfg import confmgr
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        if ios_low_device_flag():
            return MTL_DEVICE_LOW
        else:
            if ios_med_device_flag():
                return MTL_DEVICE_MED
            return MTL_DEVICE_HIGH

    elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
        if global_data.is_android_pc or global_data.is_in_mumu:
            return MTL_DEVICE_HIGH
        else:
            val = global_data.deviceinfo.get_device_score()
            if val is None:
                return
            if val == '':
                val = 0
            val = int(val)
            if val == 0:
                return MTL_DEVICE_LOW
            return val

    return MTL_DEVICE_HIGH


def is_device_highend():
    level = get_device_level()
    if level and level >= MTL_DEVICE_HIGH:
        return True
    return False


def get_custom_default_quality_and_resolution():
    from common.cfg import confmgr
    my_device_model = profiling.get_device_model().strip().lower()
    my_gpu_desc = profiling.get_video_card_name().strip().lower()
    my_quality = -1
    my_resolution = -1
    device_map = confmgr.get('device_quality_conf', default={})
    matched_device = ''
    matched_gpu = ''
    print('get_custom_default_quality check: device:%s, gpu:%s' % (my_device_model, my_gpu_desc))
    for idx, dinfo in six.iteritems(device_map):
        device_model = dinfo.get('mobile_type', '')
        gpu_desc = dinfo.get('gpu_type', '')
        quality = dinfo.get('quality', 1)
        reso = dinfo.get('resolution', 1)
        if my_device_model == device_model.strip().lower():
            print('It is custom_default_quality check: device:%s' % (my_device_model,))
            my_quality = quality
            my_resolution = reso
            matched_device = my_device_model
        elif my_gpu_desc and my_gpu_desc == gpu_desc.strip().lower() and not matched_device:
            print('It is custom_default_quality check: gpu:%s' % (my_gpu_desc,))
            my_quality = quality
            my_resolution = reso
            matched_gpu = my_gpu_desc

    return (my_quality, my_resolution)


def get_default_quality_and_resolution--- This code section failed: ---

 555       0  LOAD_GLOBAL           0  'get_custom_default_quality_and_resolution'
           3  CALL_FUNCTION_0       0 
           6  UNPACK_SEQUENCE_2     2 
           9  STORE_FAST            0  'custom_quality'
          12  STORE_FAST            1  'custom_reso'

 556      15  STORE_FAST            1  'custom_reso'
          18  COMPARE_OP            5  '>='
          21  POP_JUMP_IF_FALSE    90  'to 90'
          24  LOAD_FAST             1  'custom_reso'
          27  LOAD_CONST            1  ''
          30  COMPARE_OP            5  '>='
        33_0  COME_FROM                '21'
          33  POP_JUMP_IF_FALSE    90  'to 90'

 557      36  LOAD_GLOBAL           1  'print'
          39  LOAD_CONST            2  'Use custom quality:%d, resolution:%d.....'
          42  LOAD_FAST             0  'custom_quality'
          45  LOAD_FAST             1  'custom_reso'
          48  BUILD_TUPLE_2         2 
          51  BINARY_MODULO    
          52  CALL_FUNCTION_1       1 
          55  POP_TOP          

 558      56  POP_TOP          
          57  PRINT_ITEM_TO    
          58  PRINT_ITEM_TO    
          59  COMPARE_OP            4  '>'
          62  POP_JUMP_IF_FALSE    71  'to 71'
          65  LOAD_CONST            3  1
          68  JUMP_FORWARD          3  'to 74'
          71  LOAD_CONST            1  ''
        74_0  COME_FROM                '68'
          74  STORE_FAST            2  'fps'

 559      77  LOAD_FAST             0  'custom_quality'
          80  LOAD_FAST             1  'custom_reso'
          83  LOAD_FAST             2  'fps'
          86  BUILD_TUPLE_3         3 
          89  RETURN_END_IF    
        90_0  COME_FROM                '33'

 561      90  LOAD_GLOBAL           2  'get_device_level'
          93  CALL_FUNCTION_0       0 
          96  STORE_FAST            3  'perf_level'

 563      99  LOAD_CONST            4  2
         102  STORE_FAST            4  'quality'

 564     105  LOAD_CONST            4  2
         108  STORE_FAST            5  'reso'

 565     111  LOAD_CONST            3  1
         114  STORE_FAST            2  'fps'

 567     117  LOAD_FAST             3  'perf_level'
         120  LOAD_CONST            0  ''
         123  COMPARE_OP            8  'is'
         126  POP_JUMP_IF_FALSE   280  'to 280'

 568     129  LOAD_CONST            1  ''
         132  LOAD_CONST            0  ''
         135  IMPORT_NAME           4  'game3d'
         138  STORE_FAST            6  'game3d'

 570     141  LOAD_GLOBAL           5  'get_device_perf_flag'
         144  CALL_FUNCTION_0       0 
         147  STORE_FAST            7  'perf_flag'

 571     150  LOAD_FAST             7  'perf_flag'
         153  LOAD_GLOBAL           6  'PERF_FLAG_ANDROID_LOW'
         156  BUILD_TUPLE_1         1 
         159  COMPARE_OP            6  'in'
         162  POP_JUMP_IF_FALSE   186  'to 186'

 572     165  LOAD_CONST            3  1
         168  STORE_FAST            4  'quality'

 573     171  LOAD_CONST            3  1
         174  STORE_FAST            5  'reso'

 574     177  LOAD_CONST            1  ''
         180  STORE_FAST            2  'fps'
         183  JUMP_FORWARD         81  'to 267'

 576     186  LOAD_FAST             7  'perf_flag'
         189  LOAD_GLOBAL           7  'PERF_FLAG_ANDROID_MED'
         192  LOAD_GLOBAL           8  'PERF_FLAG_IOS_LOW'
         195  BUILD_TUPLE_2         2 
         198  COMPARE_OP            6  'in'
         201  POP_JUMP_IF_FALSE   225  'to 225'

 577     204  LOAD_CONST            4  2
         207  STORE_FAST            4  'quality'

 578     210  LOAD_CONST            3  1
         213  STORE_FAST            5  'reso'

 579     216  LOAD_CONST            1  ''
         219  STORE_FAST            2  'fps'
         222  JUMP_FORWARD         42  'to 267'

 581     225  LOAD_FAST             7  'perf_flag'
         228  LOAD_GLOBAL           9  'PERF_FLAG_ANDROID_HIGH'
         231  LOAD_GLOBAL          10  'PERF_FLAG_IOS_HIGH'
         234  LOAD_GLOBAL          11  'PERF_FLAG_IOS_MED'
         237  BUILD_TUPLE_3         3 
         240  COMPARE_OP            6  'in'
         243  POP_JUMP_IF_FALSE   267  'to 267'

 582     246  LOAD_CONST            4  2
         249  STORE_FAST            4  'quality'

 583     252  LOAD_CONST            4  2
         255  STORE_FAST            5  'reso'

 584     258  LOAD_CONST            3  1
         261  STORE_FAST            2  'fps'
         264  JUMP_FORWARD          0  'to 267'
       267_0  COME_FROM                '264'
       267_1  COME_FROM                '222'
       267_2  COME_FROM                '183'

 586     267  LOAD_FAST             4  'quality'
         270  LOAD_FAST             5  'reso'
         273  LOAD_FAST             2  'fps'
         276  BUILD_TUPLE_3         3 
         279  RETURN_END_IF    
       280_0  COME_FROM                '126'

 588     280  LOAD_FAST             3  'perf_level'
         283  LOAD_GLOBAL          12  'MTL_DEVICE_LOWLOW'
         286  COMPARE_OP            1  '<='
         289  POP_JUMP_IF_FALSE   313  'to 313'

 589     292  LOAD_CONST            1  ''
         295  STORE_FAST            4  'quality'

 590     298  LOAD_CONST            1  ''
         301  STORE_FAST            5  'reso'

 591     304  LOAD_CONST            1  ''
         307  STORE_FAST            2  'fps'
         310  JUMP_FORWARD         66  'to 379'

 593     313  LOAD_FAST             3  'perf_level'
         316  LOAD_GLOBAL          13  'MTL_DEVICE_LOW'
         319  COMPARE_OP            1  '<='
         322  POP_JUMP_IF_FALSE   346  'to 346'

 594     325  LOAD_CONST            1  ''
         328  STORE_FAST            4  'quality'

 595     331  LOAD_CONST            1  ''
         334  STORE_FAST            5  'reso'

 596     337  LOAD_CONST            3  1
         340  STORE_FAST            2  'fps'
         343  JUMP_FORWARD         33  'to 379'

 598     346  LOAD_FAST             3  'perf_level'
         349  LOAD_GLOBAL          14  'MTL_DEVICE_MED'
         352  COMPARE_OP            1  '<='
         355  POP_JUMP_IF_FALSE   379  'to 379'

 599     358  LOAD_CONST            3  1
         361  STORE_FAST            4  'quality'

 600     364  LOAD_CONST            3  1
         367  STORE_FAST            5  'reso'

 601     370  LOAD_CONST            3  1
         373  STORE_FAST            2  'fps'
         376  JUMP_FORWARD          0  'to 379'
       379_0  COME_FROM                '376'
       379_1  COME_FROM                '343'
       379_2  COME_FROM                '310'

 603     379  LOAD_FAST             4  'quality'
         382  LOAD_FAST             5  'reso'
         385  LOAD_FAST             2  'fps'
         388  BUILD_TUPLE_3         3 
         391  RETURN_VALUE     

Parse error at or near `STORE_FAST' instruction at offset 15


def can_use_msaa():
    return is_device_gpu_qualified()


def can_use_hdr():
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        gpu_desc = profiling.get_video_card_name().strip().lower()
        if 'adreno' in gpu_desc:
            desc_list = gpu_desc.split(' ')
            series = None
            for desc in desc_list:
                if desc.isdigit():
                    series = int(float(desc))

            if series in HDR_ADRENO_BLACK_LIST:
                return False
    return True


def can_use_high_fps():
    if global_data.is_pc_mode:
        return True
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        return global_data.feature_mgr.is_support_android_high_fps()
    return True


DEVICE_144 = {
 'NX659J'}
DEVICE_120 = {
 'V2024A', 'KB2000'}
DEVICE_LIGHT_FX = {
 'NX659J'}

def get_max_screen_refresh_rate--- This code section failed: ---

 647       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'enable_144'
           6  UNARY_NOT        
           7  POP_JUMP_IF_TRUE     26  'to 26'
          10  LOAD_GLOBAL           0  'global_data'
          13  LOAD_ATTR             2  'feature_mgr'
          16  LOAD_ATTR             3  'is_support_ntd'
          19  CALL_FUNCTION_0       0 
          22  UNARY_NOT        
        23_0  COME_FROM                '7'
          23  POP_JUMP_IF_FALSE    30  'to 30'

 648      26  LOAD_CONST            1  60
          29  RETURN_END_IF    
        30_0  COME_FROM                '23'

 650      30  LOAD_CONST            1  60
          33  STORE_FAST            0  'max_refresh'

 651      36  LOAD_GLOBAL           4  'hasattr'
          39  LOAD_GLOBAL           5  'game3d'
          42  LOAD_CONST            2  'get_support_frame_rates'
          45  CALL_FUNCTION_2       2 
          48  POP_JUMP_IF_FALSE   114  'to 114'

 652      51  LOAD_GLOBAL           5  'game3d'
          54  LOAD_ATTR             6  'get_support_frame_rates'
          57  CALL_FUNCTION_0       0 
          60  STORE_FAST            0  'max_refresh'

 653      63  LOAD_GLOBAL           7  'isinstance'
          66  LOAD_FAST             0  'max_refresh'
          69  LOAD_GLOBAL           8  'tuple'
          72  LOAD_GLOBAL           9  'list'
          75  BUILD_TUPLE_2         2 
          78  CALL_FUNCTION_2       2 
          81  POP_JUMP_IF_FALSE   105  'to 105'
          84  LOAD_FAST             0  'max_refresh'
        87_0  COME_FROM                '81'
          87  POP_JUMP_IF_FALSE   105  'to 105'

 654      90  LOAD_GLOBAL          10  'max'
          93  LOAD_FAST             0  'max_refresh'
          96  CALL_FUNCTION_1       1 
          99  STORE_FAST            0  'max_refresh'
         102  JUMP_ABSOLUTE       114  'to 114'

 656     105  LOAD_CONST            1  60
         108  STORE_FAST            0  'max_refresh'
         111  JUMP_FORWARD          0  'to 114'
       114_0  COME_FROM                '111'

 658     114  LOAD_GLOBAL           5  'game3d'
         117  LOAD_ATTR            11  'get_platform'
         120  CALL_FUNCTION_0       0 
         123  LOAD_GLOBAL           5  'game3d'
         126  LOAD_ATTR            12  'PLATFORM_ANDROID'
         129  COMPARE_OP            2  '=='
         132  POP_JUMP_IF_FALSE   204  'to 204'

 660     135  LOAD_GLOBAL          13  'profiling'
         138  LOAD_ATTR            14  'get_device_model'
         141  CALL_FUNCTION_0       0 
         144  STORE_FAST            1  'device_model'

 662     147  LOAD_FAST             1  'device_model'
         150  LOAD_GLOBAL          15  'DEVICE_144'
         153  COMPARE_OP            6  'in'
         156  POP_JUMP_IF_FALSE   174  'to 174'

 663     159  LOAD_GLOBAL          16  'min'
         162  LOAD_GLOBAL           3  'is_support_ntd'
         165  CALL_FUNCTION_2       2 
         168  STORE_FAST            0  'max_refresh'
         171  JUMP_ABSOLUTE       204  'to 204'

 664     174  LOAD_FAST             1  'device_model'
         177  LOAD_GLOBAL          17  'DEVICE_120'
         180  COMPARE_OP            6  'in'
         183  POP_JUMP_IF_FALSE   204  'to 204'

 665     186  LOAD_GLOBAL          16  'min'
         189  LOAD_GLOBAL           4  'hasattr'
         192  CALL_FUNCTION_2       2 
         195  STORE_FAST            0  'max_refresh'
         198  JUMP_ABSOLUTE       204  'to 204'
         201  JUMP_FORWARD          0  'to 204'
       204_0  COME_FROM                '201'

 667     204  LOAD_FAST             0  'max_refresh'
         207  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 165


def can_light_effect():
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        return False
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        device_model = profiling.get_device_model()
        return device_model in DEVICE_LIGHT_FX
    return True


def get_package_quality--- This code section failed: ---

 686       0  LOAD_GLOBAL           0  'INGAME_PACKAGE_COMPABILITY'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            9  'is-not'
           9  POP_JUMP_IF_FALSE    16  'to 16'

 687      12  LOAD_GLOBAL           0  'INGAME_PACKAGE_COMPABILITY'
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 688      16  LOAD_GLOBAL           2  'game3d'
          19  LOAD_ATTR             3  'get_platform'
          22  CALL_FUNCTION_0       0 
          25  LOAD_GLOBAL           2  'game3d'
          28  LOAD_ATTR             4  'PLATFORM_ANDROID'
          31  COMPARE_OP            3  '!='
          34  POP_JUMP_IF_FALSE    47  'to 47'

 689      37  LOAD_GLOBAL           5  'PACKAGE_QUALITY_HIGH_END'
          40  STORE_GLOBAL          0  'INGAME_PACKAGE_COMPABILITY'

 690      43  LOAD_GLOBAL           0  'INGAME_PACKAGE_COMPABILITY'
          46  RETURN_END_IF    
        47_0  COME_FROM                '34'

 692      47  LOAD_GLOBAL           6  'package_utils'
          50  LOAD_ATTR             7  'MINI_PACKAGE_FLAG'
          53  POP_JUMP_IF_TRUE     66  'to 66'

 693      56  LOAD_GLOBAL           5  'PACKAGE_QUALITY_HIGH_END'
          59  STORE_GLOBAL          0  'INGAME_PACKAGE_COMPABILITY'

 694      62  LOAD_GLOBAL           0  'INGAME_PACKAGE_COMPABILITY'
          65  RETURN_END_IF    
        66_0  COME_FROM                '53'

 696      66  LOAD_GLOBAL           8  'os'
          69  LOAD_ATTR             9  'path'
          72  LOAD_ATTR            10  'join'
          75  LOAD_GLOBAL          11  'get_neox_dir'
          78  CALL_FUNCTION_0       0 
          81  LOAD_GLOBAL          12  'QUALITY_FILE_NAME'
          84  CALL_FUNCTION_2       2 
          87  STORE_FAST            0  'quality_file'

 697      90  LOAD_GLOBAL           8  'os'
          93  LOAD_ATTR             9  'path'
          96  LOAD_ATTR            13  'exists'
          99  LOAD_FAST             0  'quality_file'
         102  CALL_FUNCTION_1       1 
         105  POP_JUMP_IF_TRUE    112  'to 112'

 698     108  LOAD_GLOBAL          14  'PACKAGE_QUALITY_INIT'
         111  RETURN_END_IF    
       112_0  COME_FROM                '105'

 699     112  SETUP_EXCEPT         81  'to 196'

 700     115  LOAD_GLOBAL          15  'open'
         118  LOAD_GLOBAL           1  'None'
         121  CALL_FUNCTION_2       2 
         124  SETUP_WITH           63  'to 190'
         127  STORE_FAST            1  'tmp_file'

 701     130  LOAD_GLOBAL          16  'int'
         133  LOAD_FAST             1  'tmp_file'
         136  LOAD_ATTR            17  'read'
         139  CALL_FUNCTION_0       0 
         142  LOAD_ATTR            18  'strip'
         145  CALL_FUNCTION_0       0 
         148  CALL_FUNCTION_1       1 
         151  STORE_FAST            2  'quality_info'

 702     154  LOAD_FAST             2  'quality_info'
         157  LOAD_GLOBAL           5  'PACKAGE_QUALITY_HIGH_END'
         160  LOAD_GLOBAL          19  'PACKAGE_QUALITY_LOW_END'
         163  BUILD_TUPLE_2         2 
         166  COMPARE_OP            7  'not-in'
         169  POP_JUMP_IF_FALSE   176  'to 176'

 703     172  LOAD_GLOBAL          14  'PACKAGE_QUALITY_INIT'
         175  RETURN_END_IF    
       176_0  COME_FROM                '169'

 704     176  LOAD_FAST             2  'quality_info'
         179  STORE_GLOBAL          0  'INGAME_PACKAGE_COMPABILITY'

 705     182  LOAD_GLOBAL           0  'INGAME_PACKAGE_COMPABILITY'
         185  RETURN_VALUE     
         186  POP_BLOCK        
         187  LOAD_CONST            0  ''
       190_0  COME_FROM_WITH           '124'
         190  WITH_CLEANUP     
         191  END_FINALLY      
         192  POP_BLOCK        
         193  JUMP_FORWARD         21  'to 217'
       196_0  COME_FROM                '112'

 706     196  POP_TOP          
         197  POP_TOP          
         198  POP_TOP          

 707     199  LOAD_GLOBAL          20  'exception_hook'
         202  LOAD_ATTR            21  'post_error'
         205  LOAD_CONST            2  '[PATCH] GET PACKAGE QUALITY ERROR'
         208  CALL_FUNCTION_1       1 
         211  POP_TOP          

 708     212  LOAD_GLOBAL          14  'PACKAGE_QUALITY_INIT'
         215  RETURN_VALUE     
         216  END_FINALLY      
       217_0  COME_FROM                '216'
       217_1  COME_FROM                '193'
         217  LOAD_CONST            0  ''
         220  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 121


def set_package_info_quality(quality_info):
    if game3d.get_platform() != game3d.PLATFORM_ANDROID:
        return True
    if not package_utils.MINI_PACKAGE_FLAG:
        return True
    if not render.is_android_support_astc():
        return PACKAGE_QUALITY_LOW_END
    try:
        quality_path = os.path.join(get_neox_dir(), QUALITY_FILE_NAME)
        with open(quality_path, 'wb') as tmp_file:
            tmp_file.write(str(quality_info))
        return True
    except:
        exception_hook.post_error('[PACTH] SET PACKAGE QUALITY ERROR')
        return False

    return True


def get_high_end_package_size():
    info_name = 'npk_info.config'
    config_file = os.path.join(get_neox_dir(), info_name)
    if not os.path.exists(config_file):
        return 0
    with open(config_file, 'rb') as tmp_file:
        npk_info = json.loads(zlib.decompress(tmp_file.read()))
    high_end_item = npk_info.get('highend', {})
    size = 0
    for k, v in six.iteritems(high_end_item):
        size += v[1]

    return size


def is_ppi_qualified--- This code section failed: ---

 746       0  LOAD_CONST            1  ''
           3  STORE_FAST            0  'ppi'

 748       6  SETUP_EXCEPT         20  'to 29'

 749       9  LOAD_GLOBAL           0  'game3d'
          12  LOAD_ATTR             1  'get_window_dpi'
          15  CALL_FUNCTION_0       0 
          18  LOAD_CONST            2  1
          21  BINARY_SUBSCR    
          22  STORE_FAST            0  'ppi'
          25  POP_BLOCK        
          26  JUMP_FORWARD         34  'to 63'
        29_0  COME_FROM                '6'

 750      29  DUP_TOP          
          30  LOAD_GLOBAL           2  'Exception'
          33  COMPARE_OP           10  'exception-match'
          36  POP_JUMP_IF_FALSE    62  'to 62'
          39  POP_TOP          
          40  STORE_FAST            1  'e'
          43  POP_TOP          

 751      44  LOAD_GLOBAL           3  'print'
          47  LOAD_CONST            3  'get ppi error.........%s'
          50  LOAD_FAST             1  'e'
          53  BINARY_MODULO    
          54  CALL_FUNCTION_1       1 
          57  POP_TOP          

 752      58  LOAD_GLOBAL           4  'True'
          61  RETURN_VALUE     
          62  END_FINALLY      
        63_0  COME_FROM                '62'
        63_1  COME_FROM                '26'

 754      63  LOAD_GLOBAL           3  'print'
          66  LOAD_CONST            4  'Current device PPI is:%s ====='
          69  LOAD_FAST             0  'ppi'
          72  BINARY_MODULO    
          73  CALL_FUNCTION_1       1 
          76  POP_TOP          

 756      77  LOAD_GLOBAL           0  'game3d'
          80  LOAD_ATTR             5  'get_platform'
          83  CALL_FUNCTION_0       0 
          86  LOAD_GLOBAL           0  'game3d'
          89  LOAD_ATTR             6  'PLATFORM_IOS'
          92  COMPARE_OP            2  '=='
          95  POP_JUMP_IF_FALSE   178  'to 178'

 757      98  LOAD_GLOBAL           7  'profiling'
         101  LOAD_ATTR             8  'get_device_info'
         104  CALL_FUNCTION_0       0 
         107  STORE_FAST            2  'i_platform'

 758     110  LOAD_FAST             2  'i_platform'
         113  POP_JUMP_IF_FALSE   171  'to 171'

 759     116  LOAD_FAST             2  'i_platform'
         119  LOAD_CONST            5  3
         122  BINARY_SUBSCR    
         123  STORE_FAST            2  'i_platform'

 760     126  LOAD_GLOBAL           3  'print'
         129  LOAD_CONST            6  'Current device model is:%s, is_in_series:%s ====='
         132  LOAD_FAST             2  'i_platform'
         135  LOAD_FAST             2  'i_platform'
         138  LOAD_GLOBAL           9  'IPAD_MINI_HIGH_PPI_MODEL_SERIES'
         141  COMPARE_OP            6  'in'
         144  BUILD_TUPLE_2         2 
         147  BINARY_MODULO    
         148  CALL_FUNCTION_1       1 
         151  POP_TOP          

 762     152  LOAD_FAST             2  'i_platform'
         155  LOAD_GLOBAL           9  'IPAD_MINI_HIGH_PPI_MODEL_SERIES'
         158  COMPARE_OP            6  'in'
         161  POP_JUMP_IF_FALSE   171  'to 171'

 763     164  LOAD_GLOBAL          10  'False'
         167  RETURN_END_IF    
       168_0  COME_FROM                '161'
         168  JUMP_FORWARD          0  'to 171'
       171_0  COME_FROM                '168'

 765     171  JUMP_FORWARD          7  'to 181'
         174  COMPARE_OP            5  '>='
         177  RETURN_END_IF    
       178_0  COME_FROM                '95'

 767     178  LOAD_GLOBAL           0  'game3d'
       181_0  COME_FROM                '171'
         181  LOAD_ATTR             5  'get_platform'
         184  CALL_FUNCTION_0       0 
         187  LOAD_GLOBAL           0  'game3d'
         190  LOAD_ATTR            11  'PLATFORM_ANDROID'
         193  COMPARE_OP            2  '=='
         196  POP_JUMP_IF_FALSE   206  'to 206'

 768     199  POP_JUMP_IF_FALSE     7  'to 7'
         202  COMPARE_OP            5  '>='
         205  RETURN_END_IF    
       206_0  COME_FROM                '199'
       206_1  COME_FROM                '196'

 770     206  LOAD_GLOBAL           0  'game3d'
         209  LOAD_ATTR             5  'get_platform'
         212  CALL_FUNCTION_0       0 
         215  LOAD_GLOBAL           0  'game3d'
         218  LOAD_ATTR            12  'PLATFORM_WIN32'
         221  COMPARE_OP            2  '=='
         224  POP_JUMP_IF_FALSE   231  'to 231'

 771     227  LOAD_GLOBAL           4  'True'
         230  RETURN_END_IF    
       231_0  COME_FROM                '224'

 773     231  LOAD_GLOBAL           4  'True'
         234  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `COMPARE_OP' instruction at offset 174


def is_not_good_memory_size_device():
    mem = profiling.get_total_memory()
    if 2150.4 > mem:
        return True
    if game3d.get_platform() == game3d.PLATFORM_ANDROID:
        if not render.is_android_support_astc():
            return True
        if 3174.4 > mem:
            return True
    return False


def is_support_astc():
    from common.utils import package_type
    if package_type.is_android_dds_package():
        return False
    platform = game3d.get_platform()
    if platform == game3d.PLATFORM_ANDROID:
        return render.is_android_support_astc()
    if platform == game3d.PLATFORM_IOS:
        return is_ios_support_astc()
    return False


def collect_performance_info():
    info = {}
    gds = global_data.game_mgr.gds
    if not gds:
        return 'Collect failed! No global_display_setting!'
    quality = gds.get_actual_quality()
    orig_resolution = game3d.get_window_size()
    resolution_scale = render.get_redirect_scale()
    scn = world.get_active_scene()
    if scn:
        shadowmap = scn.is_scene_light_enable_shadowmap()
        hdr = scn.is_hdr_enable
    else:
        shadowmap = False
        hdr = False
    if hasattr(render, 'get_msaa_sample_nums'):
        msaa = render.get_msaa_sample_nums()
    else:
        msaa = 'Not support get MSAA in this Engine Version.'
    gpu_name = profiling.get_video_card_name()
    info.update({'quality': quality,
       'resolution_origin': orig_resolution,
       'resolution_scale': resolution_scale,
       'resolution_actual': (
                           orig_resolution[0] * resolution_scale, orig_resolution[1] * resolution_scale),
       'shadowmap': shadowmap,
       'hdr': hdr,
       'msaa_samples': msaa,
       'gpu_name': gpu_name,
       'dp': profiling.get_dp_num(),
       'fps': profiling.get_render_rate(),
       'vertex_count': profiling.get_prim_num(),
       'mem_usage(MB)': profiling.get_process_mem_used() / 1024 / 1024,
       'mem_available(MB)': 1.0 * profiling.get_total_memory() - 1.0 * profiling.get_process_mem_used() / 1024 / 1024,
       'in_gpu_blacklist': not is_device_gpu_qualified(),
       'can_use_hdr': can_use_hdr(),
       'ios_need_reduce_resolution': ios_need_reduce_resolution(),
       'is_running_gles2': device_limit.is_running_gles2(),
       'is_ios_support_astc': is_ios_support_astc()
       })
    ret_str = '===== Performance info result START=====\n'
    for k, v in six.iteritems(info):
        ret_str += str(k) + ': ' + str(v) + '\n'

    ret_str += '===== Performance info result END=====\n'
    return ret_str


# global INGAME_PACKAGE_COMPABILITY ## Warning: Unused global