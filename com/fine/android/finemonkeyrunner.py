#!/usr/bin/env finemonkeyrunner
# -*- coding:utf8 -*-
'''
Copyright (C) 2017 fineMonkeyRunner
Created on Sep ,2017
@auther: wangxu
This file is the main apis sourcecode of the finemonkeyrunner
'''
import sys
import os,time
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
from com.android.monkeyrunner import MonkeyView


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
        self.viewlist = []

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
            self.debug("waitforconnectiontime:Success")
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
            if (self.easydevice.exists(self.getviewbyid(id))):
                return True
            else:
                self.debug('isexist: %s this id does not exists,will try check again' % id)
                self.sleep(1)
        except:
            # self.debug('isexist: the %dst time check id (%s) existing error ,  , will retry ' % (tmp, id))
            self.sleep(1)

        return False

    '''对某一个键按多次'''
    def presskey(self, key, times, type):
        # self.device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)
        for i in range(times):
            self.device.press(key, type)
        self.sleep(1)

    '''根据ID长按'''
    def longpressbyid(self,id,x=0,y=0):
        self.debug('calling longpressbyid function')

        hierarchyviewer = self.device.getHierarchyViewer()
        view = hierarchyviewer.findViewById(id)
        point = hierarchyviewer.getAbsoluteCenterOfView(view)
        item_btn_x = point.x + x
        item_btn_y = point.y + y
        self.device.touch(item_btn_x, item_btn_y, self.DOWN)
        self.sleep(1)
        self.device.touch(item_btn_x, item_btn_y, self.UP)
        return True

    '''根据view长按'''
    def longpressbyview(self,view,x=0,y=0):
        self.debug('calling longpressbyview function')
        hierarchyviewer = self.device.getHierarchyViewer()

        point = hierarchyviewer.getAbsoluteCenterOfView(view)
        item_btn_x = point.x + x
        item_btn_y = point.y + y
        self.device.touch(item_btn_x, item_btn_y, self.DOWN)
        self.sleep(1)
        self.device.touch(item_btn_x, item_btn_y, self.UP)
        return True

    '''获view的信息--p'''
    def getviewinfo_text(self,view):
        # text = view.namedProperties.get('text:mText').value.encode('utf8')
        try:
            textproperty = view.namedProperties.get("text:mText").value.encode('utf8')
        except:
            self.debug('%s has not text:mText Property!'% str(view))
        else:
            #self.debug('The text is %s ' % textproperty)
            return textproperty


    '''--p'''
    def getviewinfo_height(self, view):
        height = view.namedProperties.get('layout:getHeight()').value.encode('utf8')
        return height
    '''--p'''
    def getviewinfo_width(self,view):
        width = view.namedProperties.get('layout:getWidth()').value.encode('utf8')
        return width
    '''--p'''
    def getviewinfo_mleft(self,view):
        mleft = view.namedProperties.get('layout:mLeft').value.encode('utf8')
        return mleft
    '''-p'''
    def getviewinfo_mtop(self,view):
        mtop = view.namedProperties.get('layout:mTop').value.encode('utf8')
    '''--p'''
    def getviewinfo_mid(self,view):
        mid = view.namedProperties.get('mID').value#.encode('utf8')
        return mid
    '''--p'''
    def getviewinfo_visible(self,view):
        visible = view.namedProperties.get('getVisibility()').value.encode('utf8')
        if visible =='VISIBLE':
            self.debug('visible')
            return True
        else:
            return False

    '''--p'''
    def getviewinfo_xy(self,view):
        hierarchyviewer = self.device.getHierarchyViewer()
        point = hierarchyviewer.getAbsoluteCenterOfView(view)
        return point.x,point.y

    '''获取文本根据id'''
    def gettextbyid(self, id):
        if self.isexist(id):
            view = self.getviewbyid(id)
            viewtext = self.getviewinfo_text(view)
            return viewtext
        else:
            self.error('Not look for the element or it has a error!')
            return False

    '''获取view根据id --p'''
    def getviewbyID(self, id):
        starttime = time.time()
        print starttime
        hierarchyviewer = self.device.getHierarchyViewer()
        view = hierarchyviewer.findViewById(id)
        endtime = time.time()
        self.debug('Elapsed Iime:%f' % (endtime - starttime))
        return view

    '''获取view根据id --p'''

    def getviewbyid(self, id):
        self.debug('calling getviewbyid function by the id (%s)' % id)
        for tmp in range(repeatTimesOnError):
            try:
                return By.id(id)
            except:
                self.debug('getviewbyid: the %dst time error by id (%s) ,  will retry ' % (tmp, id))
                mr.sleep(1)
                continue
        self.error('getviewbyid: sorry , still can\'t get the view by this id (%s). please check the view ' % id)
        sys.exc_info()
        traceback.print_exc()
        return None

    '''根据层级结构来获取view,childseq表示层级的元组（1,1,0,0,2）---p'''
    def getchildviewbylayer(self,parentid,childseq):
        self.debug('calling getchildviewbylayer function')
        hierarchyviewer=self.device.getHierarchyViewer()
        childview = "hierarchyviewer.findViewById('" + parentid + "')"
        for index in childseq:
            childview += ('.children[' + str(index) + ']')
        #print childview
        try:
            eval(childview)
        except:
            self.debug('No find the view and please check childseq')
        else:
            return eval(childview)

    '''--p'''
    '''根据id返回该元素的一个x,y,h,w的元组'''
    def getelementinfo_locate(self,id):
        xyhw= self.easydevice.locate(By.id(id))
        return xyhw

    '''根据view获取类名---p'''
    def getviewinfo_classname(self,view):#,view
        self.debug('calling traversalViewnode：%s ' % str(view))
        tmp = str(view).split('.')
        classname = tmp[-1].split('@')[0]
        return classname

    '''type：1是代表classname，type：2代表是id type：3代表是text ---p'''
    def traversalviewsametype(self, viewnode, name,type):
        # self.debug('calling traversalViewnode：%s '%str(viewnode))
        #tmplist = []
        for eachitem in range(len(viewnode.children)):
            tmpclassname = viewnode.children[eachitem]
            controls = 'TextView' in str(tmpclassname) or 'EditText' in str(tmpclassname) or 'tButton' in str(tmpclassname)
            if len(viewnode.children[eachitem].children) != 0:

                if type == 1 and (name in str(tmpclassname)):
                    self.viewlist.append(viewnode.children[eachitem])
                if type == 2 and self.getviewinfo_mid(viewnode.children[eachitem]) == name:
                    self.viewlist.append(viewnode.children[eachitem])

                if type == 3 and controls and self.getviewinfo_text(viewnode.children[eachitem]) == name:
                    self.viewlist.append(viewnode.children[eachitem])
                self.traversalviewsametype(viewnode.children[eachitem], name, type)
                # self.debug(result)
            else:
                if type == 1 and (name in str(tmpclassname)):
                    self.viewlist.append(viewnode.children[eachitem])
                if type == 2 and self.getviewinfo_mid(viewnode.children[eachitem]) == name:
                    self.viewlist.append(viewnode.children[eachitem])
                if type == 3 and controls and self.getviewinfo_text(viewnode.children[eachitem]) == name:
                    self.viewlist.append(viewnode.children[eachitem])

    '''获取指定id元素下的相同id的view对象列表 --p'''
    def getviewssameid(self,parentid,id):
        self.debug('calling getviewssameid function...')
        self.viewlist = []
        starttime =time.time()
        hierarchyviewer = self.device.getHierarchyViewer()
        viewnode = hierarchyviewer.findViewById(parentid)
        self.traversalviewsametype(viewnode,id,2)
        endtime = time.time()
        self.debug('Elapsed Iime:%f' % (endtime-starttime))
        return self.viewlist
        #pass

    '''获取指定id元素下的相同classname的view对象列表 --p'''

    def getviewssameclassname(self, parentid, classname):
        self.debug('calling getviewssameclassname function...')
        self.viewlist = []
        starttime = time.time()
        hierarchyviewer = self.device.getHierarchyViewer()
        viewnode = hierarchyviewer.findViewById(parentid)
        self.traversalviewsametype(viewnode, classname, 1)
        endtime = time.time()
        self.debug('Elapsed Iime:%f' % (endtime-starttime))
        return self.viewlist

    '''获取子views根据父view ---p'''
    def getchildviewsbyparentview(self,parentview):
        self.debug('calling getchildviewsbyparentview function...')
        viewlists = []
        if len(parentview.children) !=0:
            for i in range(len(parentview.children)):
                viewlists.append(parentview.children[i])
            return viewlists
        else:
            self.debug('%s has not children view'% str(parentview))

    '''获取子view的数量 ---p'''
    def getchilrenlength(self,parentview):
        self.debug('calling getchilrenlength function...')
        return len(parentview.children)

    '''获取指定id元素下的相同文本的view对象列表 ---p'''
    def getviewssametext(self, parentid, text):
        self.debug('calling getviewssametext function...')
        self.viewlist = []
        starttime = time.time()
        hierarchyviewer = self.device.getHierarchyViewer()
        viewnode = hierarchyviewer.findViewById(parentid)
        self.traversalviewsametype(viewnode, text, 3)
        endtime = time.time()
        self.debug('Elapsed Iime:%f' % (endtime-starttime))
        return self.viewlist

    '''拖拽屏幕 ---p'''
    def dragscreen(self, start, end, duration, steps):
        self.debug('calling dragscreen function...')
        md.drag(start, end, duration, steps)

    '''在指定的id上输入文字--p'''
    def typebyid(self,id, content):
        self.debug('device input the %s by id' % content)
        self.easydevice.type(By.id(id),content)

    '''在当前焦点输入文字--p'''
    def type(self, content):
        self.debug('device input the %s' % content)
        self.device.type(content)

    '''点击元素根据view 对话框除外 ---p'''
    def clickelementbyview(self,view,x=0,y=0):
        self.debug('calling clickelementbyview function')
        for tmp in range(repeatTimesOnError):
            try:
                hierarchyviewer = self.device.getHierarchyViewer()
                point = hierarchyviewer.getAbsoluteCenterOfView(view)
                item_btn_x = point.x + x
                item_btn_y = point.y + y
                # print item_btn_x, item_btn_y
                self.debug('Click Position:x = %d ,y = %d' % (item_btn_x, item_btn_y))
                self.device.touch(item_btn_x, item_btn_y,self.DOWN_AND_UP)
                return True
            except:
                self.debug('clickelementbyview: the %dst time click error , not found the view , will retry ' % tmp)
                if (tmp > 1 & DEBUG):
                    self.debug('Please wait to click the view')
                mr.sleep(1)
                continue
        self.error(
            'clickelementbyview: sorry , still can\'t click view. please check the view is exist or not , or increase the repeat times variable?')
        sys.exc_info()
        traceback.print_exc()
        return False

    '''点击对话框中的view'''
    def clickdialogelementbyview(self, view):
        self.debug('calling clickdialogelementbyview function')
        hierarchyviewer = self.device.getHierarchyViewer()
        width = self.device.getProperty("display.width")
        height = self.device.getProperty("display.height")
        point = hierarchyviewer.getAbsoluteCenterOfView(view)
        p = view
        rootview = view
        while p != None:
            rootview = p
            p = p.parent
        x = (int(width) - int(rootview.width)) / 2 + point.x
        y = (int(height) - int(rootview.height)) / 2 + point.y
        self.debug('Position:x= %d ; y=%d' % (x, y))
        self.device.touch(x, y, self.DOWN_AND_UP)

        #print "clicked view"

    def clickbyviewondialog(self):
        pass

    '''根据文本点击元素，由于根据文本获取的是相同文本的view列表，默认使用第一个view，
    可以根据实际情况再调整,num代表view列表中的序号，默认0   非对话框 ---P'''
    def clickbytext(self,parentid,text,num=0):
        self.debug('calling clickbytext function')
        viewlist = self.getviewssametext(parentid,text)
        if viewlist !=[]:
            self.clickelementbyview(viewlist[num])
            return True
        else:
            self.debug('No find the view, please check')
            return None
    '''根据id点击元素 ---p'''
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

    '''根据point点击元素 ---p'''
    def clickpoint(self, x, y, type):
        self.debug('calling click the point ')
        for tmp in range(repeatTimesOnError):
            try:
                self.device.touch(x, y, type)
                return True
            except:
                self.debug('clickpoint: %d time click point error , will retry ' % tmp)
                mr.sleep(1)
                continue
        self.error(
            'clickpoint: sorry , still can\'t click point. please check the view is exist or not , or increase the repeat times variable?')
        sys.exc_info()
        traceback.print_exc()
        return False

    '''判断给定的id元素是否是选中状态---p'''
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

    '''获取指定的view文本 getviewinfo_text已经存在
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
    '''
    '''清除编辑框的文本 ---P'''
    def cleartextbyid(self, id):
        self.debug('calling cleartextbyid function by the id (%s)' % id)
        if self.isexist(id):
            if not self.isfocused(id):
                self.clickbyid(id, self.DOWN_AND_UP)
            textview = self.getviewbyID(id)
            rangenumber = len(self.getviewinfo_text(textview))
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

    '''根据id输入文本框内容 ---p'''
    def inputtextbyid(self,id,text):
        self.debug('calling inputtextbyid function by the id (%s)' % id)
        self.clickbyid(id,self.DOWN_AND_UP)
        if self.isfocused(id):
            self.type(text)
        else:
            self.debug('No Selected the element by id,Please check')

        if self.switch =='E':
            self.debug('This is an emulator')
        else:
            self.presskey('KEYCODE_BACK', self.DOWN_AND_UP, 1)
        # 如果是真机需要打开语句，模拟器需关闭
        # self.pressKey('KEYCODE_BACK', self.DOWN_AND_UP, 1)
        # mr.sleep(1)
        return True


    '''根据当前界面上的任意id获取rootview ---p'''
    def getcurrentrootview(self,id):
        self.debug('calling getcurrentrootview function by the id (%s)' % id)
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
                if 'TextView' in viewnodestr or 'EditText' in viewnodestr or 'tButton' in viewnodestr:
                    viewnodetext = self.getviewinfo_text(viewnode.children[eachitem]) #viewnode.children[eachitem].namedProperties.get('text:mText').value.encode('utf8')
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

    '''该元素内的文本是否包含指定的文本 ---p'''
    def elementshouldcontaintext(self, id, text, type):
        self.debug('calling elementshouldcontaintext function by the id (%s)' % id)
        # 获取指定元id元素的viewnode
        starttime = time.time()
        hierarchyviewer = self.device.getHierarchyViewer()
        viewnode = hierarchyviewer.findViewById(id)
        result = self.traversalviewnode(viewnode, text, type)
        endtime =time.time()
        #print result
        if result:
            self.debug('Elapsed Iime:%f' % (endtime - starttime))
            return True
        else:
            self.debug('Elapsed Iime:%f' % (endtime - starttime))
            return False

    '''当前界面的文本是否包含指定的文本 ---p'''

    def pageshouldcontaintext(self, id, text, type):
        # 获取指定元id元素的rootview
        self.debug('calling pageshouldcontaintext function by the id (%s)' % id)
        starttime = time.time()
        viewnode = self.getcurrentrootview(id)
        result = self.traversalviewnode(viewnode, text, type)
        endtime = time.time()
        #print result
        if result:
            self.debug('Elapsed Iime:%f' % (endtime - starttime))
            return True
        else:
            self.debug('Elapsed Iime:%f' % (endtime - starttime))
            return False

    '''判断id的元素文本是否相等---p'''
    def equaltextbyid(self,id,text):
        self.debug('calling equaltextbyid function by the id (%s)' % id)
        if self.isexist(id):
            view = self.getviewbyID(id)
            viewtext = self.getviewinfo_text(view)
            if text == viewtext:
                #self.debug('----Pass----')
                return True
            else:
                #self.debug('----Fail----')
                return False

    '''判断view的元素文本是否相等---p'''
    def equaltextbyview(self, view, text):
        self.debug('calling equaltextbyview function by the id (%s)' % str(view))
        viewtext = self.getviewinfo_text(view)
        if text == viewtext:
            return True
        else:
            return False

    '''判断activity是否与预期的相同
    def assertcurrentactivity(self,currentactivity):
        starttime = time.time()
        self.debug('calling assertcurrentactivity function ')
        try:
            activity = self.device.shell('dumpsys activity | findstr "mFocusedActivity"') #adb shell
        except IOError:
            # print '获取当前activity失败'
            self.debug('获取当前activity失败')
        else:
            print activity
            tmp = activity.split(' ')
            activity = tmp[3]
            self.debug('activity : %s' % activity)
            if activity == currentactivity:
                endtime = time.time()
                times = endtime - starttime
                self.debug('Execute time is %d' % times)
                return True
            else:
                return False
    '''
    '''等待期望的activity出现，默认时间20秒 ---p'''
    def waitforactivity(self,waitactivity,repeatTimesOnError=20):
        for tmp in range(repeatTimesOnError):
            if self.assertfocusedwindowmame(waitactivity):
                return True
            else:
                self.debug('waitforactivity: %s this waitactivity does not exists,will try check again' % waitactivity)
                mr.sleep(1)
                continue

    '''判断activity是否相等 --p'''
    def assertfocusedwindowmame(self,expectactivity):
        starttime = time.time()
        #hierarchyviewer = self.device.getHierarchyViewer()
        winId = self.easydevice.getFocusedWindowId()
        if winId ==expectactivity:
            self.debug('%s is correct'% winId)#.encode('utf-8')
            endtime = time.time()
            times = endtime-starttime
            self.debug('Execute time is %d' % times)
            return True
            #print winId.encode('utf-8')
        else:
            self.debug('%s is wrong' % winId)
            return False
    '''--p'''
    '''Force to stop the App'''
    def forcestopapp(self,packagename):

        self.debug('calling forcestopapp function ')
        try:
            activity = self.device.shell('am force-stop %s' % packagename)
            return True
        except IOError:
            self.debug('force stop the app')

