# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/grenade_debug_utils.py
from __future__ import absolute_import
from __future__ import print_function
from common.cfg import confmgr
import math3d
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK
res_id = None
boom_res_id = None
col_radius = None
col_dmg = None
flying_timer = None

def init_debug_item(wp_id, res=None, res_scale=None, boom_res=None, boom_res_scale=None, radius=None, dmg_radius=None):
    global col_dmg
    global boom_res_id
    global col_radius
    global res_id
    if res_id:
        global_data.sfx_mgr.remove_sfx_by_id(res_id)
    if boom_res_id:
        global_data.sfx_mgr.remove_sfx_by_id(boom_res_id)
    if col_radius:
        global_data.game_mgr.scene.scene_col.remove_object(col_radius)
    if col_dmg:
        global_data.game_mgr.scene.scene_col.remove_object(col_dmg)
    res_conf = confmgr.get('grenade_res_config', str(wp_id))
    data_conf = confmgr.get('grenade_config', str(wp_id))
    if not res_conf or not data_conf:
        global_data.game_mgr.show_tip('\xe8\xa1\xa8\xe9\x87\x8c\xe6\xb2\xa1\xe5\xa1\xab\xe5\x90\xa7\xef\xbc\x9f(\xe6\x8a\x95\xe6\x8e\xb7\xe7\x89\xa9\xe5\x8f\x82\xe6\x95\xb0\xe8\xa1\xa8 & \xe6\x8a\x95\xe6\x8e\xb7\xe7\x89\xa9\xe7\xbe\x8e\xe6\x9c\xaf\xe8\xb5\x84\xe6\xba\x90\xe8\xa1\xa8)\xef\xbc\x9a%s' % str(wp_id))
        return
    else:
        ret_res = res if res else res_conf['cRes']
        ret_res_scale = res_scale if res_scale else res_conf['fBulletSfxScale']
        ret_boom_res = boom_res if boom_res else res_conf['cSfx'][0][0]
        ret_boom_res_scale = boom_res_scale if boom_res_scale else res_conf['fScale']
        ret_radius = radius if radius else data_conf['fCollisionRadius']
        ret_dmg_radius = dmg_radius if dmg_radius else None
        if global_data.mecha and global_data.mecha.logic:
            target = global_data.mecha
        else:
            target = global_data.player
        pos = math3d.vector(target.logic.ev_g_position())
        forward = target.logic.ev_g_forward()
        forward.normalize()
        right = math3d.vector(0, 1, 0).cross(forward)
        right.normalize()
        pos += forward * 130
        pos += right * 65
        pos.y += 65
        print(ret_res)
        print(ret_res_scale)
        print(ret_boom_res)
        print(ret_boom_res_scale)
        print(ret_radius)
        print(ret_dmg_radius)
        print(pos)

        def res_cb(sfx):
            sfx.scale = math3d.vector(ret_res_scale, ret_res_scale, ret_res_scale)
            sfx.position = pos

        res_id = global_data.sfx_mgr.create_sfx_in_scene(ret_res, on_create_func=res_cb)

        def boom_res_cb(sfx):
            sfx.scale = math3d.vector(ret_boom_res_scale, ret_boom_res_scale, ret_boom_res_scale)
            sfx.position = pos

        boom_res_id = global_data.sfx_mgr.create_sfx_in_scene(ret_boom_res, on_create_func=boom_res_cb)
        col_radius = collision.col_object(collision.SPHERE, math3d.vector(ret_radius, ret_radius, ret_radius) * NEOX_UNIT_SCALE, 0, 0, 0)
        col_radius.position = pos
        global_data.game_mgr.scene.scene_col.add_object(col_radius)
        if ret_dmg_radius:
            col_dmg = collision.col_object(collision.SPHERE, math3d.vector(ret_dmg_radius, ret_dmg_radius, ret_dmg_radius) * NEOX_UNIT_SCALE, 0, 0, 0)
            col_dmg.position = pos
            global_data.game_mgr.scene.scene_col.add_object(col_dmg)
        return


def init_debug_aoe_item--- This code section failed: ---

 126       0  LOAD_GLOBAL           0  'res_id'
           3  POP_JUMP_IF_FALSE    25  'to 25'

 127       6  LOAD_GLOBAL           1  'global_data'
           9  LOAD_ATTR             2  'sfx_mgr'
          12  LOAD_ATTR             3  'remove_sfx_by_id'
          15  LOAD_GLOBAL           0  'res_id'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          
          22  JUMP_FORWARD          0  'to 25'
        25_0  COME_FROM                '22'

 129      25  LOAD_GLOBAL           4  'boom_res_id'
          28  POP_JUMP_IF_FALSE    50  'to 50'

 130      31  LOAD_GLOBAL           1  'global_data'
          34  LOAD_ATTR             2  'sfx_mgr'
          37  LOAD_ATTR             3  'remove_sfx_by_id'
          40  LOAD_GLOBAL           4  'boom_res_id'
          43  CALL_FUNCTION_1       1 
          46  POP_TOP          
          47  JUMP_FORWARD          0  'to 50'
        50_0  COME_FROM                '47'

 132      50  LOAD_GLOBAL           5  'col_radius'
          53  POP_JUMP_IF_FALSE    81  'to 81'

 133      56  LOAD_GLOBAL           1  'global_data'
          59  LOAD_ATTR             6  'game_mgr'
          62  LOAD_ATTR             7  'scene'
          65  LOAD_ATTR             8  'scene_col'
          68  LOAD_ATTR             9  'remove_object'
          71  LOAD_GLOBAL           5  'col_radius'
          74  CALL_FUNCTION_1       1 
          77  POP_TOP          
          78  JUMP_FORWARD          0  'to 81'
        81_0  COME_FROM                '78'

 135      81  LOAD_GLOBAL          10  'col_dmg'
          84  POP_JUMP_IF_FALSE   112  'to 112'

 136      87  LOAD_GLOBAL           1  'global_data'
          90  LOAD_ATTR             6  'game_mgr'
          93  LOAD_ATTR             7  'scene'
          96  LOAD_ATTR             8  'scene_col'
          99  LOAD_ATTR             9  'remove_object'
         102  LOAD_GLOBAL          10  'col_dmg'
         105  CALL_FUNCTION_1       1 
         108  POP_TOP          
         109  JUMP_FORWARD          0  'to 112'
       112_0  COME_FROM                '109'

 139     112  LOAD_FAST             0  'res'
         115  POP_JUMP_IF_TRUE    138  'to 138'

 140     118  LOAD_GLOBAL           1  'global_data'
         121  LOAD_ATTR             6  'game_mgr'
         124  LOAD_ATTR            11  'show_tip'
         127  LOAD_CONST            1  '\xe4\xb8\x8d\xe5\xa1\xab\xe8\xb5\x84\xe6\xba\x90\xe9\x82\xa3\xe5\x93\xa5\xe4\xbb\xac\xe6\xb2\xa1\xe5\x8a\x9e\xe6\xb3\x95\xe4\xba\x86'
         130  CALL_FUNCTION_1       1 
         133  POP_TOP          

 141     134  LOAD_CONST            0  ''
         137  RETURN_END_IF    
       138_0  COME_FROM                '115'

 143     138  LOAD_FAST             1  'model_scale'
         141  POP_JUMP_IF_FALSE   150  'to 150'
         144  LOAD_FAST             1  'model_scale'
         147  JUMP_FORWARD          3  'to 153'
         150  LOAD_CONST            2  1.0
       153_0  COME_FROM                '147'
         153  STORE_FAST            4  'ret_model_scale'

 144     156  LOAD_FAST             2  'socket_scale'
         159  POP_JUMP_IF_FALSE   168  'to 168'
         162  LOAD_FAST             2  'socket_scale'
         165  JUMP_FORWARD          3  'to 171'
         168  LOAD_CONST            2  1.0
       171_0  COME_FROM                '165'
         171  STORE_FAST            5  'ret_socket_scale'

 146     174  LOAD_FAST             4  'ret_model_scale'
         177  LOAD_FAST             5  'ret_socket_scale'
         180  BINARY_MULTIPLY  
         181  STORE_DEREF           0  'scale'

 148     184  LOAD_GLOBAL           1  'global_data'
         187  LOAD_ATTR            12  'mecha'
         190  POP_JUMP_IF_FALSE   217  'to 217'
         193  LOAD_GLOBAL           1  'global_data'
         196  LOAD_ATTR            12  'mecha'
         199  LOAD_ATTR            13  'logic'
       202_0  COME_FROM                '190'
         202  POP_JUMP_IF_FALSE   217  'to 217'

 149     205  LOAD_GLOBAL           1  'global_data'
         208  LOAD_ATTR            12  'mecha'
         211  STORE_FAST            6  'target'
         214  JUMP_FORWARD          9  'to 226'

 151     217  LOAD_GLOBAL           1  'global_data'
         220  LOAD_ATTR            14  'player'
         223  STORE_FAST            6  'target'
       226_0  COME_FROM                '214'

 152     226  LOAD_GLOBAL          15  'math3d'
         229  LOAD_ATTR            16  'vector'
         232  LOAD_FAST             6  'target'
         235  LOAD_ATTR            13  'logic'
         238  LOAD_ATTR            17  'ev_g_position'
         241  CALL_FUNCTION_0       0 
         244  CALL_FUNCTION_1       1 
         247  STORE_DEREF           1  'pos'

 153     250  LOAD_FAST             6  'target'
         253  LOAD_ATTR            13  'logic'
         256  LOAD_ATTR            18  'ev_g_forward'
         259  CALL_FUNCTION_0       0 
         262  STORE_FAST            7  'forward'

 154     265  LOAD_FAST             7  'forward'
         268  LOAD_ATTR            19  'normalize'
         271  CALL_FUNCTION_0       0 
         274  POP_TOP          

 155     275  LOAD_GLOBAL          15  'math3d'
         278  LOAD_ATTR            16  'vector'
         281  LOAD_CONST            3  ''
         284  LOAD_CONST            4  1
         287  LOAD_CONST            3  ''
         290  CALL_FUNCTION_3       3 
         293  LOAD_ATTR            20  'cross'
         296  LOAD_FAST             7  'forward'
         299  CALL_FUNCTION_1       1 
         302  STORE_FAST            8  'right'

 156     305  LOAD_FAST             8  'right'
         308  LOAD_ATTR            19  'normalize'
         311  CALL_FUNCTION_0       0 
         314  POP_TOP          

 157     315  LOAD_DEREF            1  'pos'
         318  LOAD_FAST             7  'forward'
         321  LOAD_CONST            5  130
         324  BINARY_MULTIPLY  
         325  INPLACE_ADD      
         326  STORE_DEREF           1  'pos'

 158     329  LOAD_DEREF            1  'pos'
         332  LOAD_FAST             8  'right'
         335  LOAD_CONST            6  65
         338  BINARY_MULTIPLY  
         339  INPLACE_ADD      
         340  STORE_DEREF           1  'pos'

 159     343  LOAD_DEREF            1  'pos'
         346  DUP_TOP          
         347  LOAD_ATTR            21  'y'
         350  LOAD_CONST            6  65
         353  INPLACE_ADD      
         354  ROT_TWO          
         355  STORE_ATTR           21  'y'

 161     358  LOAD_FAST             3  'dmg_radius'
         361  POP_JUMP_IF_FALSE   370  'to 370'
         364  LOAD_FAST             3  'dmg_radius'
         367  JUMP_FORWARD          3  'to 373'
         370  LOAD_CONST            0  ''
       373_0  COME_FROM                '367'
         373  STORE_FAST            9  'ret_dmg_radius'

 163     376  LOAD_GLOBAL          23  'print'
         379  LOAD_FAST             0  'res'
         382  CALL_FUNCTION_1       1 
         385  POP_TOP          

 164     386  LOAD_GLOBAL          23  'print'
         389  LOAD_FAST             4  'ret_model_scale'
         392  CALL_FUNCTION_1       1 
         395  POP_TOP          

 165     396  LOAD_GLOBAL          23  'print'
         399  LOAD_FAST             5  'ret_socket_scale'
         402  CALL_FUNCTION_1       1 
         405  POP_TOP          

 166     406  LOAD_GLOBAL          23  'print'
         409  LOAD_DEREF            0  'scale'
         412  CALL_FUNCTION_1       1 
         415  POP_TOP          

 167     416  LOAD_GLOBAL          23  'print'
         419  LOAD_FAST             9  'ret_dmg_radius'
         422  CALL_FUNCTION_1       1 
         425  POP_TOP          

 168     426  LOAD_GLOBAL          23  'print'
         429  LOAD_DEREF            1  'pos'
         432  CALL_FUNCTION_1       1 
         435  POP_TOP          

 171     436  LOAD_CLOSURE          0  'scale'
         439  LOAD_CLOSURE          1  'pos'
         445  LOAD_CONST               '<code_object res_cb>'
         448  MAKE_CLOSURE_0        0 
         451  STORE_FAST           10  'res_cb'

 175     454  LOAD_GLOBAL           1  'global_data'
         457  LOAD_ATTR             2  'sfx_mgr'
         460  LOAD_ATTR            24  'create_sfx_in_scene'
         463  LOAD_ATTR             8  'scene_col'
         466  LOAD_FAST            10  'res_cb'
         469  CALL_FUNCTION_257   257 
         472  STORE_GLOBAL          0  'res_id'

 177     475  LOAD_FAST             9  'ret_dmg_radius'
         478  POP_JUMP_IF_FALSE   564  'to 564'

 178     481  LOAD_GLOBAL          25  'collision'
         484  LOAD_ATTR            26  'col_object'
         487  LOAD_GLOBAL          25  'collision'
         490  LOAD_ATTR            27  'SPHERE'
         493  LOAD_GLOBAL          15  'math3d'
         496  LOAD_ATTR            16  'vector'
         499  LOAD_FAST             9  'ret_dmg_radius'
         502  LOAD_FAST             9  'ret_dmg_radius'
         505  LOAD_FAST             9  'ret_dmg_radius'
         508  CALL_FUNCTION_3       3 
         511  LOAD_GLOBAL          28  'NEOX_UNIT_SCALE'
         514  BINARY_MULTIPLY  
         515  LOAD_CONST            3  ''
         518  LOAD_CONST            3  ''
         521  LOAD_CONST            3  ''
         524  CALL_FUNCTION_5       5 
         527  STORE_GLOBAL         10  'col_dmg'

 179     530  LOAD_DEREF            1  'pos'
         533  LOAD_GLOBAL          10  'col_dmg'
         536  STORE_ATTR           29  'position'

 180     539  LOAD_GLOBAL           1  'global_data'
         542  LOAD_ATTR             6  'game_mgr'
         545  LOAD_ATTR             7  'scene'
         548  LOAD_ATTR             8  'scene_col'
         551  LOAD_ATTR            30  'add_object'
         554  LOAD_GLOBAL          10  'col_dmg'
         557  CALL_FUNCTION_1       1 
         560  POP_TOP          
         561  JUMP_FORWARD          0  'to 564'
       564_0  COME_FROM                '561'
         564  LOAD_CONST            0  ''
         567  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_257' instruction at offset 469


def init_debug_flying_ammo_item--- This code section failed: ---

 196       0  LOAD_GLOBAL           0  'res_id'
           3  POP_JUMP_IF_FALSE    25  'to 25'

 197       6  LOAD_GLOBAL           1  'global_data'
           9  LOAD_ATTR             2  'sfx_mgr'
          12  LOAD_ATTR             3  'remove_sfx_by_id'
          15  LOAD_GLOBAL           0  'res_id'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          
          22  JUMP_FORWARD          0  'to 25'
        25_0  COME_FROM                '22'

 199      25  LOAD_FAST             0  'res'
          28  POP_JUMP_IF_TRUE     51  'to 51'

 200      31  LOAD_GLOBAL           1  'global_data'
          34  LOAD_ATTR             4  'game_mgr'
          37  LOAD_ATTR             5  'show_tip'
          40  LOAD_CONST            1  '\xe4\xb8\x8d\xe5\xa1\xab\xe8\xb5\x84\xe6\xba\x90\xe9\x82\xa3\xe5\x93\xa5\xe4\xbb\xac\xe6\xb2\xa1\xe5\x8a\x9e\xe6\xb3\x95\xe4\xba\x86'
          43  CALL_FUNCTION_1       1 
          46  POP_TOP          

 201      47  LOAD_CONST            0  ''
          50  RETURN_END_IF    
        51_0  COME_FROM                '28'

 203      51  LOAD_GLOBAL           6  'flying_timer'
          54  POP_JUMP_IF_FALSE    82  'to 82'

 204      57  LOAD_GLOBAL           1  'global_data'
          60  LOAD_ATTR             4  'game_mgr'
          63  LOAD_ATTR             7  'unregister_logic_timer'
          66  LOAD_GLOBAL           6  'flying_timer'
          69  CALL_FUNCTION_1       1 
          72  POP_TOP          

 205      73  LOAD_CONST            0  ''
          76  STORE_GLOBAL          6  'flying_timer'
          79  JUMP_FORWARD          0  'to 82'
        82_0  COME_FROM                '79'

 207      82  LOAD_GLOBAL           1  'global_data'
          85  LOAD_ATTR             9  'mecha'
          88  POP_JUMP_IF_FALSE   115  'to 115'
          91  LOAD_GLOBAL           1  'global_data'
          94  LOAD_ATTR             9  'mecha'
          97  LOAD_ATTR            10  'logic'
       100_0  COME_FROM                '88'
         100  POP_JUMP_IF_FALSE   115  'to 115'

 208     103  LOAD_GLOBAL           1  'global_data'
         106  LOAD_ATTR             9  'mecha'
         109  STORE_FAST            4  'target'
         112  JUMP_FORWARD          9  'to 124'

 210     115  LOAD_GLOBAL           1  'global_data'
         118  LOAD_ATTR            11  'player'
         121  STORE_FAST            4  'target'
       124_0  COME_FROM                '112'

 211     124  LOAD_GLOBAL          12  'math3d'
         127  LOAD_ATTR            13  'vector'
         130  LOAD_FAST             4  'target'
         133  LOAD_ATTR            10  'logic'
         136  LOAD_ATTR            14  'ev_g_position'
         139  CALL_FUNCTION_0       0 
         142  CALL_FUNCTION_1       1 
         145  STORE_DEREF           3  'pos'

 212     148  LOAD_FAST             4  'target'
         151  LOAD_ATTR            10  'logic'
         154  LOAD_ATTR            15  'ev_g_forward'
         157  CALL_FUNCTION_0       0 
         160  STORE_DEREF           4  'forward'

 213     163  LOAD_DEREF            4  'forward'
         166  LOAD_ATTR            16  'normalize'
         169  CALL_FUNCTION_0       0 
         172  POP_TOP          

 214     173  LOAD_GLOBAL          12  'math3d'
         176  LOAD_ATTR            13  'vector'
         179  LOAD_CONST            2  ''
         182  LOAD_CONST            3  1
         185  LOAD_CONST            2  ''
         188  CALL_FUNCTION_3       3 
         191  LOAD_ATTR            17  'cross'
         194  LOAD_DEREF            4  'forward'
         197  CALL_FUNCTION_1       1 
         200  STORE_FAST            5  'right'

 215     203  LOAD_FAST             5  'right'
         206  LOAD_ATTR            16  'normalize'
         209  CALL_FUNCTION_0       0 
         212  POP_TOP          

 217     213  LOAD_DEREF            2  'reverse'
         216  POP_JUMP_IF_TRUE    250  'to 250'

 218     219  LOAD_DEREF            3  'pos'
         222  LOAD_DEREF            4  'forward'
         225  LOAD_CONST            4  50
         228  BINARY_MULTIPLY  
         229  INPLACE_ADD      
         230  STORE_DEREF           3  'pos'

 219     233  LOAD_DEREF            3  'pos'
         236  LOAD_FAST             5  'right'
         239  LOAD_CONST            5  35
         242  BINARY_MULTIPLY  
         243  INPLACE_ADD      
         244  STORE_DEREF           3  'pos'
         247  JUMP_FORWARD         28  'to 278'

 221     250  LOAD_DEREF            3  'pos'
         253  LOAD_DEREF            4  'forward'
         256  LOAD_CONST            6  500
         259  BINARY_MULTIPLY  
         260  INPLACE_ADD      
         261  STORE_DEREF           3  'pos'

 222     264  LOAD_DEREF            3  'pos'
         267  LOAD_FAST             5  'right'
         270  LOAD_CONST            5  35
         273  BINARY_MULTIPLY  
         274  INPLACE_SUBTRACT 
         275  STORE_DEREF           3  'pos'
       278_0  COME_FROM                '247'

 224     278  LOAD_DEREF            3  'pos'
         281  DUP_TOP          
         282  LOAD_ATTR            18  'y'
         285  LOAD_CONST            7  65
         288  INPLACE_ADD      
         289  ROT_TWO          
         290  STORE_ATTR           18  'y'

 226     293  LOAD_DEREF            0  'scale'
         296  POP_JUMP_IF_FALSE   305  'to 305'
         299  LOAD_DEREF            0  'scale'
         302  JUMP_FORWARD          3  'to 308'
         305  LOAD_CONST            8  1.0
       308_0  COME_FROM                '302'
         308  STORE_DEREF           0  'scale'

 227     311  LOAD_DEREF            1  'flying_speed'
         314  POP_JUMP_IF_FALSE   323  'to 323'
         317  LOAD_DEREF            1  'flying_speed'
         320  JUMP_FORWARD          3  'to 326'
         323  LOAD_CONST            8  1.0
       326_0  COME_FROM                '320'
         326  STORE_DEREF           1  'flying_speed'

 229     329  LOAD_GLOBAL          19  'print'
         332  LOAD_FAST             0  'res'
         335  CALL_FUNCTION_1       1 
         338  POP_TOP          

 230     339  LOAD_GLOBAL          19  'print'
         342  LOAD_DEREF            0  'scale'
         345  CALL_FUNCTION_1       1 
         348  POP_TOP          

 231     349  LOAD_GLOBAL          19  'print'
         352  LOAD_DEREF            1  'flying_speed'
         355  CALL_FUNCTION_1       1 
         358  POP_TOP          

 232     359  LOAD_GLOBAL          19  'print'
         362  LOAD_DEREF            3  'pos'
         365  CALL_FUNCTION_1       1 
         368  POP_TOP          

 235     369  LOAD_CLOSURE          0  'scale'
         372  LOAD_CLOSURE          3  'pos'
         375  LOAD_CLOSURE          2  'reverse'
         378  LOAD_CLOSURE          4  'forward'
         381  LOAD_CLOSURE          1  'flying_speed'
         387  LOAD_CONST               '<code_object res_cb>'
         390  MAKE_CLOSURE_0        0 
         393  STORE_FAST            6  'res_cb'

 257     396  LOAD_GLOBAL           1  'global_data'
         399  LOAD_ATTR             2  'sfx_mgr'
         402  LOAD_ATTR            20  'create_sfx_in_scene'
         405  LOAD_ATTR            10  'logic'
         408  LOAD_FAST             6  'res_cb'
         411  CALL_FUNCTION_257   257 
         414  STORE_GLOBAL          0  'res_id'

 258     417  LOAD_GLOBAL          19  'print'
         420  LOAD_GLOBAL           0  'res_id'
         423  CALL_FUNCTION_1       1 
         426  POP_TOP          
         427  LOAD_CONST            0  ''
         430  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_257' instruction at offset 411


# global flying_timer ## Warning: Unused global