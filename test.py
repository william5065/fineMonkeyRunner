#!/usr/bin/env finemonkeyrunner
# -*- coding:utf8 -*-
import sys
sys.path.append(r'D:\learning\python\auto\fineMonkeyRunner')
from com.fine.android.finemonkeyrunner import fineMonkeyRunner

# 导入包路径，否则找不到 ---注意
#sys.path.append(r'C:\Users\wangxu\AppData\Local\Android\sdk\tools\testscript')
#sys.path.append(r'D:\learning\python\auto\fineMonkeyRunner')
finemonkeyrunner = fineMonkeyRunner('emulator-5554')
#finemonkeyrunner.assertfocusedwindowmame('com.mdsd.wiicare/com.mdsd.wiicare.function.LoginActivity_')
#finemonkeyrunner.assertcurrentactivity('com.mdsd.wiicare/com.mdsd.wiicare.function.LoginActivity_')
view = finemonkeyrunner.getviewbyID('id/etAccount')
print finemonkeyrunner.getviewinfo_classname(view)
#print finemonkeyrunner.getelementinfo_locate('id/etAccount')
#print finemonkeyrunner.getviewinfo_visible(view)
#finemonkeyrunner.typebyid('id/etPassword','123')
#ss = finemonkeyrunner.getviewssametext('id/drawerLayout','经鼻气管插管')
#print finemonkeyrunner.viewlist
#finemonkeyrunner.getviewinfo(view)
#finemonkeyrunner.forcestopapp('com.mdsd.wiicare')