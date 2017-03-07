## Welcome to fineMonkeyRunner Pages

fineMonkeyRunner 是一个基于MonkeyRunner的api的二次封装，增加了大量的接口方便使用者调用，由于MonkeyRunner提供的
一些接口不能调用成功，在fineMonkeyRunner中再次封装了，也提供了一些作为结果验证的接口，方便使用者判断case的结果。
目前第一版已经可以使用。也欢迎大家能一起把fineMonkeyRunner一起维护下去，更好的方便大家使用。减少使用者的代码量
以及提高元素定位的准确度以及效率将是这个目标。再次欢迎大家一起加入，快乐开源，开源快乐！
在这里也说明一下fineMonkeyRunner也参考得了wrapEasyMonkey，非常感谢！让我们继续开源。

### 使用说明
1、将文件下载到指定的目录下并解压:例如./fineMonkeyRunner/com/fine/android/finmonkeyrunner.py
2、在fineMonkeyRunner目录下建测试文件如：test.py
3、在测试文件中先使用sys.path.append(r'./fineMonkeyRunner')根据自己的实际目录添加
4、在from com.fine.android.finemonkeyrunner import fineMonkeyRunner
5、实例化fineMoneyRunner的一个类，即可调用接口


```接口介绍
1、elementshouldcontaintext
   某元素下是否包含指定的文本
2、pageshouldcontaintext
   某指定的id元素所在的整个视图内是否包含指定的文本
3、equaltextbyview
   指定视图的文本是否与期望的相等

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/william5065/fineMonkeyRunner/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### 技术讨论
qq群：601631209
mail:123777618@qq.com