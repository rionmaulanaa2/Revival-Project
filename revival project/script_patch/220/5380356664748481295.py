# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/VehicleTestUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.uisys.basepanel import BasePanel
from cocosui import cc
from common.const.uiconst import TOP_ZORDER
import math3d
from common.const import uiconst

class VehicleTestUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/vehicle_test'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    property_map = {'engine': [
                'peak_torque', 'max_omega', 'engine_moi', 'engine_full_rate', 'engine_zero_rate', 'engine_zero_rate_disengated'],
       'wheel': [
               'wheel_damping_rate', 'wheel_moi', 'max_steer', 'max_hand_brake_torque', 'longitudinal_force', 'wheel_width', 'camber_force', 'latstiffx', 'latstiffy', 'anti_rollbar'],
       'clutch': [
                'clutch_strength'],
       'suspension': [
                    'suspension_max_droop', 'spring_strength', 'spring_damper_rate'],
       'dynamicbody': [
                     'rigid_mass', 'rigid_center', 'rigid_moi'],
       'different': [
                   'front_rear', 'front_left_right', 'rear_left_right', 'front_bias', 'rear_bias', 'center_bias']
       }
    translate_map = {'engine': [
                'PxVehicleEngineData', '\xe5\xbc\x95\xe6\x93\x8e\xe7\x9b\xb8\xe5\x85\xb3'],
       'wheel': [
               'PxVehicleWheelData', '\xe8\xbd\xae\xe8\x83\x8e\xe7\x9b\xb8\xe5\x85\xb3'],
       'clutch': [
                'PxVehicleClutchData', '\xe7\xa6\xbb\xe5\x90\x88\xe5\x99\xa8\xe7\x9b\xb8\xe5\x85\xb3'],
       'suspension': [
                    'PxVehicleSuspensionData ', '\xe6\x82\xac\xe6\x8c\x82\xe7\x9b\xb8\xe5\x85\xb3'],
       'dynamicbody': [
                     'PxRigidDynamic', '\xe5\x88\x9a\xe4\xbd\x93\xe7\x9b\xb8\xe5\x85\xb3'],
       'different': [
                   'PxVehicleDifferential4WData', '\xe9\xa9\xb1\xe5\x8a\xa8\xe5\xb7\xae\xe9\x80\x9f\xe5\x99\xa8\xe7\x9b\xb8\xe5\x85\xb3'],
       'peak_torque': [
                     'mPeakTorque', '\xe6\x89\xad\xe7\x9f\xa9'],
       'max_omega': [
                   'mMaxOmega', '\xe5\xbc\x95\xe6\x93\x8e\xe8\xbd\xac\xe6\x95\xb0'],
       'engine_moi': [
                    'mMOI', '\xe8\xbd\xac\xe5\x8a\xa8\xe6\x83\xaf\xe6\x80\xa7'],
       'engine_full_rate': [
                          'mDampingRateFullThrottle', '\xe5\xbc\x95\xe6\x93\x8e\xe6\xbb\xa1\xe9\x98\xbb\xe5\xb0\xbc'],
       'engine_zero_rate': [
                          'mDampingRateZeroThrottleClutchEngaged', '\xe5\xbc\x95\xe6\x93\x8e\xe9\x9b\xb6\xe9\x98\xbb\xe5\xb0\xbc'],
       'engine_zero_rate_disengated': [
                                     'mDampingRateZeroThrottleClutchDisengaged', '\xe5\xbc\x95\xe6\x93\x8e\xe5\x90\xaf\xe5\x8a\xa8\xe9\x98\xbb\xe5\xb0\xbc'],
       'wheel_damping_rate': [
                            'mDampingRate', '\xe9\x98\xbb\xe5\xb0\xbc\xe7\x8e\x87'],
       'wheel_moi': [
                   'mMOI', '\xe8\xbd\xac\xe5\x8a\xa8\xe6\x83\xaf\xe6\x80\xa7'],
       'max_hand_brake_torque': [
                               'mMaxHandBrakeTorque', '\xe6\x9c\x80\xe5\xa4\xa7\xe6\x89\x8b\xe5\x88\xb9\xe6\x89\xad\xe7\x9f\xa9'],
       'max_steer': [
                   'mMaxSteer', '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xbd\xac\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x88\xe5\x89\x8d\xe8\xbd\xae\xef\xbc\x89'],
       'longitudinal_force': [
                            'mLongitudinalStiffnessPerUnitGravity', '\xe8\xbd\xae\xe8\x83\x8e\xe7\xba\xb5\xe5\x90\x91\xe5\x8e\x8b\xe5\x8a\x9b'],
       'wheel_width': [
                     'mWidth', '\xe8\xbd\xae\xe8\x83\x8e\xe5\xae\xbd\xe5\xba\xa6'],
       'camber_force': [
                      'mCamberStiffnessPerUnitGravity', '\xe8\xbd\xae\xe8\x83\x8e\xe6\xa8\xaa\xe5\x90\x91\xe5\x8e\x8b\xe5\x8a\x9b'],
       'latstiffx': [
                   'mLatStiffX', '\xe8\xbd\xae\xe8\x83\x8e\xe6\xa8\xaa\xe5\x90\x91\xe5\x88\x9a\xe5\xba\xa6'],
       'latstiffy': [
                   'mLatStiffY', '\xe8\xbd\xae\xe8\x83\x8e\xe7\xba\xb5\xe5\x90\x91\xe5\x88\x9a\xe5\xba\xa6'],
       'anti_rollbar': [
                      'mStiffness', '\xe5\xb9\xb3\xe8\xa1\xa1\xe6\x9d\xa0'],
       'clutch_strength': [
                         'mStrength', '\xe7\xa6\xbb\xe5\x90\x88\xe5\x99\xa8\xe5\x8e\x8b\xe5\x8a\x9b'],
       'suspension_max_droop': [
                              'mMaxDroop', '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x8e\x8b\xe7\xbc\xa9\xe9\x87\x8f'],
       'spring_strength': [
                         'mSpringStrength', '\xe6\x82\xac\xe6\x8c\x82\xe5\xbc\xb9\xe7\xb0\xa7\xe5\x8a\x9b'],
       'spring_damper_rate': [
                            'mSpringDamperRate', '\xe5\xbc\xb9\xe7\xb0\xa7\xe9\x98\xbb\xe5\xb0\xbc\xe7\x8e\x87'],
       'rigid_mass': [
                    'Mass', '\xe5\x88\x9a\xe4\xbd\x93\xe8\xb4\xa8\xe9\x87\x8f'],
       'rigid_center': [
                      'Center of mass', '\xe8\xb4\xa8\xe5\xbf\x83'],
       'rigid_moi': [
                   'Moment of Inertia', '\xe6\x83\xaf\xe6\x80\xa7'],
       'front_rear': [
                    'mFrontRearSplit', '\xe5\x89\x8d\xe5\x90\x8e\xe6\x89\xad\xe7\x9f\xa9\xe5\x88\x86\xe9\x85\x8d\xef\xbc\x88\xe5\x9b\x9b\xe9\xa9\xb1\xef\xbc\x89'],
       'front_left_right': [
                          'mFrontLeftRightSplit', '\xe5\xb7\xa6\xe5\x89\x8d\xe6\x89\xad\xe7\x9f\xa9\xe5\x88\x86\xe9\x85\x8d'],
       'rear_left_right': [
                         'mRearLeftRightSplit', '\xe5\xb7\xa6\xe5\x90\x8e\xe6\x89\xad\xe7\x9f\xa9\xe5\x88\x86\xe9\x85\x8d'],
       'front_bias': [
                    'mFrontBias', '\xe5\x89\x8d\xe5\xb7\xae\xe9\x80\x9f\xe6\xaf\x94'],
       'rear_bias': [
                   'mRearBias', '\xe5\x90\x8e\xe5\xb7\xae\xe9\x80\x9f\xe6\xaf\x94'],
       'center_bias': [
                     'mCentreBias', '\xe5\x89\x8d\xe5\x90\x8e\xe5\xb7\xae\xe9\x80\x9f\xe6\xaf\x94']
       }

    def on_init_panel(self):
        self.init_event()
        self.translate_flag = False
        self.init_vehicle_event()
        self.init_property()

    def init_property(self):
        vehicle = global_data.v
        if vehicle:
            for k, ps in six.iteritems(self.property_map):
                node = getattr(self.panel, 'node_%s' % k, None)
                if node:
                    for p in ps:
                        input_p = getattr(node, p, None)
                        if input_p:
                            value = getattr(vehicle, p, '')
                            if type(value) is math3d.vector:
                                value = '%f %f %f' % (value.x, value.y, value.z)
                            else:
                                value = '%f' % value
                            value = str(value)
                            input_p.setString(value)

        if global_data.gravity_factor == None:
            global_data.gravity_factor = 1.0
        if global_data.brake_factor == None:
            global_data.brake_factor = 0.1
        self.panel.gravity.setString('%s' % global_data.gravity_factor)
        self.panel.brake_factor.setString('%s' % global_data.brake_factor)
        return

    def init_vehicle_event(self):

        @self.panel.btn_translate.callback()
        def OnClick(btn, callback):
            self.translate()

        @self.panel.btn_ok.callback()
        def OnClick(btn, callback):
            self.reset_param()

    def init_event(self):
        pass

    def translate(self):
        print('translate')
        index = self.translate_flag or 0 if 1 else 1
        self.translate_flag = not self.translate_flag
        for key in self.property_map:
            node = getattr(self.panel, 'node_%s' % key, None)
            if node:
                title = getattr(node, key, None)
                title.setString(self.translate_map[key][index])
                for value in self.property_map[key]:
                    label = getattr(node, 'l_%s' % value, None)
                    label.setString(self.translate_map[value][index])
                    text = getattr(node, value, None)
                    text.setVisible(index != 0)

        return

    def reset_param(self):
        if global_data.v:
            for key in self.property_map:
                node = getattr(self.panel, 'node_%s' % key, None)
                if node:
                    for value in self.property_map[key]:
                        t = getattr(node, value, None)
                        if t:
                            ss = t.getString()
                            p = None
                            if value in ('rigid_center', 'rigid_moi'):
                                vs = [ float(x) for x in ss.split(' ') ]
                                p = math3d.vector(vs[0], vs[1], vs[2])
                                print(p)
                            else:
                                p = float(ss)
                            setattr(global_data.v, value, p)

        s = self.panel.gravity.getString()
        global_data.gravity_factor = float(s)
        s = self.panel.brake_factor.getString()
        global_data.brake_factor = float(s)
        global_data.game_mgr.scene.scene_col.gravity = math3d.vector(0, -98, 0) * global_data.gravity_factor
        global_data.emgr.battle_show_message_event.emit('\xe4\xbf\xae\xe6\x94\xb9\xe6\x88\x90\xe5\x8a\x9f')
        return