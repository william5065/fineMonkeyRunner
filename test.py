#!/usr/bin/env finemonkeyrunner
# -*- coding:utf8 -*-
import sys
sys.path.append(r'D:\learning\python\auto\fineMonkeyRunner')
from com.fine.android.finemonkeyrunner import fineMonkeyRunner

# 导入包路径，否则找不到 ---注意
#sys.path.append(r'C:\Users\wangxu\AppData\Local\Android\sdk\tools\testscript')
#sys.path.append(r'D:\learning\python\auto\fineMonkeyRunner')
finemonkeyrunner = fineMonkeyRunner('emulator-5554')
finemonkeyrunner.assertfocusedwindowmame('com.mdsd.wiicare/com.mdsd.wiicare.function.LoginActivity_')
finemonkeyrunner.assertcurrentactivity('com.mdsd.wiicare/com.mdsd.wiicare.function.LoginActivity_')
#finemonkeyrunner.forcestopapp('com.mdsd.wiicare')