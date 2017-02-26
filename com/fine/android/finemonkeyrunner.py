#!/usr/bin/env finemonkeyrunner
# -*- coding:utf8 -*-
'''
Copyright (C) 2017 fineMonkeyRunner
Created on Sep ,2017
@auther: wangxu
This file is the main apis sourcecode of the finemonkeyrunner
'''
import sys
import os
from datetime import datetime
import traceback


'''
Global variables
'''
DEBUG = True
INFO = True
ERROR = True
repeatTimesOnError = 3
idCheckTimes = 20
waitForConnectionTime = 10
ANDROID_HOME = os.environ['ANDROID_HOME'] if os.environ.has_key('ANDROID_HOME') else '/root/android-sdk-linux/'

'''
import android libs and internal libs
'''
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By
from com.android.chimpchat.hierarchyviewer import HierarchyViewer
from com.android.hierarchyviewerlib.models import ViewNode

from com.android.chimpchat.core import TouchPressType
# from testCaseManager import testCaseManager


class fineMonkeyRunner:
    '''
    #############################
    finemonkeyrunner class
    #############################
    '''

    def __init__(self, emulatorname):
        device = mr.waitForConnection(10, emulatorname)
        self.debug("__int__: creating the finemonkeyrunner object with emulatorname %s" % emulatorname)
        # self.deviceId = deviceId
        self.easyDevice = EasyMonkeyDevice(device)
        self.device = device
        # self.DOWN = TouchPressType.DOWN.getIdentifier()
        # self.UP = TouchPressType.UP.getIdentifier()
        # self.DOWN_AND_UP = TouchPressType.DOWN_AND_UP.getIdentifier()
        self.DOWN = self.device.DOWN
        self.UP = self.device.UP
        self.DOWN_AND_UP = self.device.DOWN_AND_UP
        # self.caseManager = testCaseManager(self)
        self.debug('created the fineEasyDevice')
