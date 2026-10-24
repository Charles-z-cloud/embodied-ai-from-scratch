# 第 02 章参考答案与思路

[正文](README.md) · [练习](exercises.md) · [全书目录](../../README.md)

## 练习1

文件保存源码，目录组织文件，编辑器修改源码，解释器执行源码，终端接收执行命令并显示结果。编辑器打开文件不表示终端进入其目录。

## 练习2

绝对路径是 `/Users/mei/ai-study/examples/hello.py`，相对路径是 `examples/hello.py`。进入上一级 `/Users/mei` 后，应使用 `ai-study/examples/hello.py`；原相对路径将指向另一个位置。

## 练习3

第二行应保存为 `print("我能找到自己的程序")`。重新运行应该显示新文字。版本和绝对路径以你实际检查结果为准，不能填教材作者电脑的结果冒充自己的记录。

## 练习4

不能确定。程序使用哪个环境取决于执行时选择的解释器。macOS/Linux 可以直接调用项目中的 `.venv/bin/python`，Windows 使用 `.venv\Scripts\python.exe`；相对路径的起点仍须正确。

## 练习5

先检查路径。可以 cd 到桌面的项目目录再运行，也可以给解释器传入 hello.py 的完整路径。还需确认文件没有保存成 hello.py.txt。

## 练习6

`>>>` 是 Python 交互窗口，cd 是 shell 的命令。输入 `exit()` 返回终端，再切换目录。这两种输入位置使用不同的语言规则。
