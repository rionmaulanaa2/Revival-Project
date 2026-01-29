# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/luck_score_config.py
_reload_all = True
luck_score_percent = [
 (1000, 99),
 (900, 98),
 (810, 97),
 (770, 96),
 (730, 95),
 (690, 94),
 (679, 93),
 (668, 92),
 (657, 91),
 (646, 90),
 (635, 89),
 (624, 88),
 (613, 87),
 (602, 86),
 (597, 85),
 (592, 84),
 (587, 83),
 (582, 82),
 (577, 81),
 (572, 80),
 (567, 79),
 (562, 78),
 (557, 77),
 (552, 76),
 (547, 75),
 (542, 74),
 (537, 73),
 (532, 72),
 (527, 71),
 (522, 70),
 (517, 69),
 (512, 68),
 (507, 67),
 (502, 66),
 (497, 65),
 (494, 64),
 (491, 63),
 (488, 62),
 (485, 61),
 (482, 60),
 (479, 59),
 (476, 58),
 (473, 57),
 (470, 56),
 (467, 55),
 (464, 54),
 (461, 53),
 (458, 52),
 (455, 51),
 (452, 50),
 (449, 49),
 (446, 48),
 (442, 47),
 (438, 46),
 (434, 45),
 (430, 44),
 (426, 43),
 (422, 42),
 (418, 41),
 (414, 40),
 (410, 39),
 (406, 38),
 (402, 37),
 (398, 36),
 (394, 35),
 (390, 34),
 (386, 33),
 (382, 32),
 (378, 31),
 (374, 30)]
MIN_LUCK_SCORE_PERCENT = 30
NORMAL_LUCK_SCORE_EDGE = 500
LOTTERY_COUNT_SHOW_BAODI = 20
LUCK_SCORE_TRIGGER_RED_PACKET = 1100
LUCK_RED_PACKET_TYPE = 6
LUCK_MAX_LIKE_NUM = 500000

def get_luck_score_percent(score):
    for min_score, percent in luck_score_percent:
        if score >= min_score:
            return percent

    return 0