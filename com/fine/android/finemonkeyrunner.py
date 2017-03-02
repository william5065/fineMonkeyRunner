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

    def __init__(self, emulatorname,switch=PHONE_EMULATOR_SWITCH):
        device = self.waitforconnection(waitForConnectionTime, emulatorname)
        self.debug("__int__: creating the finemonkeyrunner object with emulatorname %s" % emulatorname)
        # use EasyMonkeyDevice and MonkeyDevice
        self.easydevice = EasyMonkeyDevice(device)
        self.device = device
        # presskey type
        self.DOWN = self.device.DOWN
        self.UP = self.device.UP
        self.DOWN_AND_UP = self.device.DOWN_AND_UP
        self.switch = switch
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

    def installapp(self,apppath):
        try:
            self.device.installPackage(apppath)
        except:
            self.error("Install app Fail ")
    def remove(self,packagename):
        try:
            self.device.removePackage(packagename)
        except:
            self.error("Uninstall app Fail ")


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

            #self.debug('isexist: the %dst time check id (%s) existing error ,  , will retry ' % (tmp, id))
            self.sleep(1)

        return False

    '''获取文本根据id'''
    def gettextbyid(self,id):
        if self.isexist(id):
            view = self.getview(id)
            viewtext = self.gettextbyview(view)
            return viewtext
        else:
            self.error('Not look for the element or it has a error!')
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

    '''点击元素根据view 对话框除外'''
    def clickbyview(self,view,x=0,y=0):
        self.debug('calling clickbyview function')
        for tmp in range(repeatTimesOnError):
            try:
                hierarchyviewer = self.device.getHierarchyViewer()
                point = hierarchyviewer.getAbsoluteCenterOfView(view)
                item_btn_x = point.x + x
                item_btn_y = point.y + y
                print item_btn_x, item_btn_y
                self.device.touch(item_btn_x, item_btn_y,self.DOWN_AND_UP)
                return True
            except:

                self.debug('clickbyview: the %dst time click error , not found the view , will retry ' % tmp)
                if (tmp > 1 & DEBUG):
                    self.debug('Please wait to click the view')
                mr.sleep(1)
                continue
        self.error(
            'clickbyview: sorry , still can\'t click view. please check the view is exist or not , or increase the repeat times variable?')
        sys.exc_info()
        traceback.print_exc()
        return False

    def clickbyviewondialog(self):
        pass

    '''根据id点击元素'''
    def clickbyid(self, id, type):

        self.debug('calling clickbyid function')
        for tmp in range(repeatTimesOnError):
            try:
                self.easydevice.touch(By.id(id), type)
                return True
            except:

                self.debug(
                    'clickbyid: the %dst time click error by this id (%s) , not found the view , will retry ' % (
                    tmp, id))
                if (tmp > 1 & DEBUG):
                    self.debug('Please wait to click the view')
                mr.sleep(1)
                continue
        self.error(
            'clickbyid: sorry , still can\'t click view. please check the view is exist or not , or increase the repeat times variable?')
        sys.exc_info()
        traceback.print_exc()
        return False

    '''判断给定的id元素是否是选中状态'''
    def isfocused(self, id):

        self.debug('checking the view is focused or not')
        # hierarchyViewer = self.device.getHierarchyViewer()
        # print hierarchyViewer.findViewById(id).hasFocus

        for tmp in range(repeatTimesOnError):
            try:
                hierarchyViewer = self.device.getHierarchyViewer()
                return hierarchyViewer.findViewById(id).hasFocus
            except:
                self.debug('isfocused: the %dst time check focus error  , will retry ' % tmp)
                mr.sleep(1)
                continue
        self.error('isfocused: error occured')
        sys.exc_info()
        traceback.print_exc()
        return False

    '''获取指定的view文本'''
    def gettextbyview(self, view):
        # if view != None:
        #  return (view.namedProperties.get('text:mText').value.encode('utf8'))
        textProperty = view.namedProperties.get("text:mText")
        if textProperty==None:
            self.debug('No text property on node')
            textProperty = view.namedProperties.get("mText")
            if textProperty == None:
                self.debug('No text property on node')
        return textProperty.value.encode('utf8')

    '''清除编辑框的文本'''
    def cleartextbyid(self, id):
        self.debug('calling cleartextbyid function by the id (%s)' % id)
        if (self.isexist(id)):
            if not self.isfocused(id):
                self.clickbyid(id, self.DOWN_AND_UP)
            TextView = self.getview(id)
            rangenumber = len(self.gettextbyview(TextView))
            for x in range(rangenumber):
                self.device.press('KEYCODE_DEL', self.DOWN_AND_UP)
            for x in range(rangenumber):
                self.device.press('KEYCODE_FORWARD_DEL', self.DOWN_AND_UP)
            self.debug('cleartextbyid: cleared the text in id (%s)' % id)
            return True
        self.error('cleartextbyid: sorry ,the id (%s) is not exist ' % id)
        sys.exc_info()
        traceback.print_exc()
        return False

    '''根据id输入文本框内容'''
    def inputtextbyid(self,id,text):

        self.clickbyid(id,self.DOWN_AND_UP)
        if self.isfocused(id):
            self.type(text)
        else:
            self.debug('No Selected the element by id,Please check')

        if self.switch =='E':
            self.presskey('KEYCODE_BACK', self.DOWN_AND_UP, 1)

        # 如果是真机需要打开语句，模拟器需关闭
        # self.pressKey('KEYCODE_BACK', self.DOWN_AND_UP, 1)
        # mr.sleep(1)
        return True


    '''根据当前界面上的任意id获取rootview'''
    def getcurrentrootview(self,id):
        hierarchyviewer = self.device.getHierarchyViewer()
        currentview = hierarchyviewer.findViewById(id)
        p = currentview
        rootview = currentview
        while p != None:
            rootview = p
            p = p.parent
        return rootview

    '''遍历viewnode节点,type=1是完全匹配type=0是包含关系'''

    def traversalviewnode(self, viewnode, text, type):
        # self.debug('calling traversalViewnode：%s '%str(viewnode))
        tmplist = []
        for eachitem in range(len(viewnode.children)):
            viewnodestr = str(viewnode.children[eachitem])
            if len(viewnode.children[eachitem].children) != 0:
                result = self.traversalviewnode(viewnode.children[eachitem], text, type)
                if result:
                    return self.traversalviewnode(viewnode.children[eachitem], text, type)
            else:
                if 'TextView' in viewnodestr:
                    viewnodetext = viewnode.children[eachitem].namedProperties.get('text:mText').value.encode('utf8')
                    if type == 1 and viewnodetext == text:
                        # self.debug('1 Find the text：%s ' % viewnodetext)
                        tmplist.append('P')
                        return True

                    elif type == 0 and (text in viewnodetext):
                        # self.debug('0 Find the text: %s ' % viewnodetext)
                        tmplist.append('P')
                        return True
                    else:
                        tmplist.append('F')

    '''该元素内的文本是否包含指定的文本'''
    def elementshouldcontaintext(self, id, text, type):
        # 获取指定元id元素的viewnode
        hierarchyviewer = self.device.getHierarchyViewer()
        viewnode = hierarchyviewer.findViewById(id)
        result = self.traversalviewnode(viewnode, text, type)
        print result
        if result:
            self.debug('----PASS----')
        else:
            self.debug('----FAIL----')

    '''当前界面的文本是否包含指定的文本'''

    def pageshouldcontaintext(self, id, text, type):
        # 获取指定元id元素的rootview
        #hierarchyviewer = self.device.getHierarchyViewer()
        #viewnode = hierarchyviewer.findViewById(id)
        viewnode = self.getcurrentrootview(id)
        result = self.traversalviewnode(viewnode, text, type)

        print result
        if result:
            self.debug('----PASS----')
        else:
            self.debug('----FAIL----')

    '''判断id的元素文本是否相等'''
    def equaltextbyid(self,id,text):
        if self.isexist(id):
            view =self.getview(id)
            viewtext = self.gettextbyview(view)
            if text ==viewtext:
                self.debug('----Pass----')
                return True
            else:
                self.debug('----Fail----')
                return False

    '''判断activity是否与预期的相同'''
    def assertcurrentactivity(self,currentactivity):
        self.debug('calling assertcurrentactivity function ')
        try:
            activity = self.device.shell('adb shell dumpsys activity | findstr "mFocusedActivity"')
        except IOError:
            # print '获取当前activity失败'
            self.debug('获取当前activity失败')
        else:
            tmp = activity.split(' ')
            activity = tmp[3]
            self.debug('activity : %s' % activity)
            if activity == currentactivity:
                return True
            else:
                return False

    '''等待期望的activity出现，默认时间20秒'''
    def waitforactivity(self,waitactivity,repeatTimesOnError=20):
        for tmp in range(repeatTimesOnError):
            if self.assertcurrentactivity(waitactivity):
                return True
            else:
                self.debug('waitforactivity: %s this waitactivity does not exists,will try check again' % waitactivity)
                mr.sleep(1)
                continue

    '''停止应用'''
    def forcestopapp(self,packagename):

        self.debug('calling forcestopapp function ')
        try:
            activity = self.device.shell('adb shell am force-stop %s' % packagename)
            return True
        except IOError:
            self.debug('强制停止应用')



'''from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.chimpchat.hierarchyviewer import HierarchyViewer
device = MonkeyRunner.waitForConnection(5,"emulator-5554")
hViewer = device.getHierarchyViewer() # 对当前UI视图进行解析
content = hViewer.findViewById('id/content')  # 通过id查找对应元素
memberView = content.children[0]
text = memberView.namedProperties.get('text:mText').value.encode('utf8')
desc = memberView.namedProperties.get('accessibility:getContentDescription()').value.encode('utf8')
mleft = memberView.namedProperties.get('layout:mLeft').value.encode('utf8')
height = memberView.height'''