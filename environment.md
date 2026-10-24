# 教材示例的验证环境

[全书目录](README.md)

2026-10-24，在教材目录内建立独立的`.venv`，未修改全局Python包。当前验证平台为macOS arm64，Python 3.12.10。

第02—07章仅需Python标准功能；第08章开始使用Matplotlib，第09章开始使用NumPy，第20章开始使用PyTorch；图像章节使用Pillow，第37章开始使用Gymnasium（实测1.4.0）。读者可以按各章安装所需部分，不必在编程入门时就下载所有工具。

作者实际安装的核心版本见[requirements-core.txt](requirements-core.txt)，全部传递依赖见[environment-lock-macos-arm64.txt](environment-lock-macos-arm64.txt)。这些版本记录服务于本次复现，不代表所有操作系统和旧硬件都支持；选择其他平台时按官方支持范围建立环境，并记录差异。

从教材根目录可使用`.venv/bin/python`执行示例。Windows对应环境解释器一般位于`.venv\Scripts\python.exe`。各章写出的`python3`命令表示使用自己选定的Python 3解释器，运行前应确认相关包安装在同一环境中。

绘图验证使用非交互式绘图方式生成文件；图像已保存到对应章节，可直接阅读，不需要先安装软件才能看图。模型实验优先使用CPU、小型合成数据，实际运行设置与结果见各章validation.md。

## 从下载后的干净目录开始

先读第02章解释的解释器、工作目录和虚拟环境。进入含有本文件的教材根目录后，macOS / Linux可使用：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-core.txt
python -c "import sys; print(sys.executable)"
```

Windows PowerShell通常用`py -m venv .venv`创建，再运行`.venv\Scripts\Activate.ps1`激活；也可直接调用`.venv\Scripts\python.exe`，避免激活步骤。Windows与Linux说明未在本次机器上实测。

本书记录的是当前机器已安装并运行的版本。若官方不为你的Python、系统或处理器提供某版本，不要机械套用macOS完整锁文件；先查看对应包官方安装说明，选受支持组合，并记录版本差异。仅阅读正文和图片无需安装依赖。

激活后，各章的`python`与`python3`应指向同一虚拟环境；不确定时优先使用该环境解释器的完整路径。训练输出和权重没有放入发布包，按[实验索引](experiments.md)重新生成。不要先运行依赖权重的后章，再把缺少文件误认为模型本身出错。
