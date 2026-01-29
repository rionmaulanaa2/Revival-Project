# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/client/const/hotkey_const.py
from __future__ import absolute_import
from data import hot_key_def
HOTKET_FAMILIES_CATALOG = [
 {
  hot_key_def.HUMAN_JUMP, hot_key_def.MECHA_JUMP},
 {
  hot_key_def.HUMAN_FIRE, hot_key_def.MECHA_FIRE},
 {
  hot_key_def.HUMAN_RELOAD, hot_key_def.MECHA_RELOAD}]
COMBINATION_BLACKLIST = {
 hot_key_def.MOVE_FORWARD,
 hot_key_def.MOVE_LEFT,
 hot_key_def.MOVE_RIGHT,
 hot_key_def.MOVE_BACKWARD,
 hot_key_def.RUN,
 hot_key_def.LOCK_MOVE_ROCKER,
 hot_key_def.HUMAN_JUMP,
 hot_key_def.MECHA_JUMP,
 hot_key_def.HUMAN_ROLL,
 hot_key_def.HUMAN_SQUAT,
 hot_key_def.HUMAN_FIRE,
 hot_key_def.MECHA_FIRE,
 hot_key_def.HUMAN_RELOAD,
 hot_key_def.MECHA_RELOAD,
 hot_key_def.HUMAN_AIM,
 hot_key_def.PICK_THING,
 hot_key_def.SCENE_INTERACTION,
 hot_key_def.TDM_OPEN_WEAPON,
 hot_key_def.FREE_SIGHT,
 hot_key_def.SWITCH_BIG_MAP}
from data import hot_key_conflict_catalog_def
GENERAL_CONFLICT_SET = {
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_REGULAR,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_HUMAN_BATTLE,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_MECHA_BATTLE,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_VEHICLE,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_VEHICLE_SKILL,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_ITEM,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_COMM,
 hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_MISC}
EXCEPTION_NON_CONFLICT_CATALOG = [
 {
  hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_HUMAN_BATTLE, hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_MECHA_BATTLE},
 {
  hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_MECHA_BATTLE, hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_VEHICLE},
 {
  hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_HUMAN_BATTLE, hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_VEHICLE_SKILL},
 {
  hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_MECHA_BATTLE, hot_key_conflict_catalog_def.HOTKEY_CONFLICT_CAT_VEHICLE_SKILL}]
HOTKEY_WHITESET_WHEN_TYPEING = {
 hot_key_def.EXIT_GAME,
 hot_key_def.FULLSCREEN_SWITCH,
 hot_key_def.FULLSCREEN_SWITCH_RIGHT,
 hot_key_def.PASTE}
from data import hot_key_def
HOTKEY_BLOCK_SET_WHEN_TYPEING = hot_key_def.ALL_HOTKEY_SET - HOTKEY_WHITESET_WHEN_TYPEING