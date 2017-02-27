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
PHONE_EMULATOR_SWITCH = 'E' #'P' OR 'E

'''
import android libs and internal libs
'''
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By
from com.android.chimpchat.hierarchyviewer import HierarchyViewer
from com.android.hierarchyviewerlib.models import ViewNode



class fineMonkeyRunner:
    '''
    #############################
    finemonkeyrunner class
    #############################
    '''

    def __init__(self, emulatorname,PHONE_EMULATOR_SWITCH):
        device = self.waitforconnection(waitForConnectionTime, emulatorname)
        self.debug("__int__: creating the finemonkeyrunner object with emulatorname %s" % emulatorname)
        # use EasyMonkeyDevice and MonkeyDevice
        self.easydevice = EasyMonkeyDevice(device)
        self.device = device
        # presskey type
        self.DOWN = self.device.DOWN
        self.UP = self.device.UP
        self.DOWN_AND_UP = self.device.DOWN_AND_UP
        self.debug('created the fineEasyDevice')

    def debug(self, debuginfo):
        if DEBUG:
            print '[%s] DEBUG:  %s ' % (datetime.today(), debuginfo)

    def info(self, info):
        if INFO:
            print '[%s] Info: %s ' % (datetime.today(), info)

    def error(self, error):
        if ERROR:
            print '[%s] ERROR: %s ' % (datetime.today(), error)

    def sleep(self, seconds):
        self.debug('sleeping %f seconds' % seconds)
        mr.sleep(seconds)

    '''建立device连接'''
    def waitforconnection(self, waitForConnectionTime,emulatorname):
        try:
            self.debug("waitForConnectionTime:Success")
            return mr.waitForConnection(waitForConnectionTime,emulatorname)
        except:
            self.error("waitForConnection error")
            sys.exc_info()
            traceback.print_exc()
            return None

    ''' 启动应用的activity'''
    def startactivity(self, activity):
        try:
            self.debug("starting the activity... %s" % activity)
            self.easydevice.startActivity(component=activity)
        except:
            self.error("starting the activity %s error" % activity)
            sys.exc_info()
            traceback.print_exc()
            return False

    '''指定的id元素是否存在'''

    def isexist(self, id):

        self.debug('check the id is exist or not')

        try:
            if (self.easydevice.exists(self.getview(id))):

                return True
            else:

                self.debug('isexist: %s this id does not exists,will try check again' % id)
                self.sleep(1)

        except:

            self.debug('isexist: the %dst time check id (%s) existing error ,  , will retry ' % (tmp, id))
            self.sleep(1)

        return False

    '''获取view根据id'''
    def getview(self, id):
        self.debug('calling getview function by the id (%s)' % id)
        for tmp in range(repeatTimesOnError):
            try:
                return By.id(id)
            except:
                self.debug('getview: the %dst time error by id (%s) ,  will retry ' % (tmp, id))
                mr.sleep(1)
                continue
        self.error('getview: sorry , still can\'t get the view by this id (%s). please check the view ' % id)
        sys.exc_info()
        traceback.print_exc()
        return None

    '''对某一个键按多次'''
    def presskey(self, key, times, type):
        # self.device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)
        for i in range(times):
            self.device.press(key, type)
        mr.sleep(1)

    '''输入文字'''
    def type(self, content):
        self.debug('device input the %s' % content)
        self.device.type(content)

    def cleartextbyid(self, id):
        self.debug('calling clearTextById function by the id (%s)' % id)
        if (self.checkIdExist(id)):
            if not self.isFocused(id):
                self.touchViewById(id, self.DOWN_AND_UP)
            TextView = self.getview(id)
            rangenumber = len(self.getText(TextView))
            for x in range(rangenumber):
                self.device.press('KEYCODE_DEL', self.DOWN_AND_UP)
            for x in range(rangenumber):
                self.device.press('KEYCODE_FORWARD_DEL', self.DOWN_AND_UP)
            self.debug('clearTextById: cleared the text in id (%s)' % id)
            return True
        self.error('clearTextById: sorry ,the id (%s) is not exist ' % id)
        sys.exc_info()
        traceback.print_exc()
        return False