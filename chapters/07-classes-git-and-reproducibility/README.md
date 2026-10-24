# 第 07 章　对象、Git 与可重复的实验记录

[上一章：文件、数据与排查错误](../06-files-and-debugging/README.md) · [全书目录](../../README.md) · 下一章：[第08章：数学表达式、函数与曲线](../08-math-language-and-functions/README.md)

**阅读顺序：正文 → [练习](exercises.md) → [参考答案](solutions.md)。**

## 7.1 把状态和操作放在一起

前置：[第06章](../06-files-and-debugging/README.md)。我们已有列表记录数据、函数处理数据、JSON保存结果。随着代码变多，记录属于谁、哪些函数可以修改它，会变得难以追踪。

可以把记录本和操作它的按钮做成一个整体。这就是**对象（object）**的一种直觉：它携带自己的数据，也提供操作这些数据的方法。**类（class）**描述这类对象怎样建立、有哪些操作；依据类创建的具体对象叫**实例（instance）**。

类像记录本的设计，实例像按设计做出的某一本记录本。比喻的边界是：Python里的类也是真正可操作的对象，本章先学习最常用的定义方式。

## 7.2 第一个自己的类

```python
class RecordBook:
    def __init__(self, name):
        self.name = name
        self.records = []

    def add(self, x_cm):
        self.records.append({"x_cm": x_cm})

    def count(self):
        return len(self.records)
```

`class RecordBook:`开始定义类；内部的def定义方法。`__init__`在建立实例时初始化它，`self`指向正在操作的那个实例。

```python
morning = RecordBook("上午")
morning.add(2.0)
morning.add(4.0)
print(morning.name)
print(morning.count())
```

输出上午和2。调用 `morning.add(2.0)` 时，Python帮我们把morning传到self的位置。方法定义中的self仍必须写出来；调用时则不需要再传一次。

`self.name`、`self.records`是实例的**属性（attribute）**，用于保存它的状态。这里的点号和先前使用`列表.append`相呼应：现在你也能自己提供属性和方法。

## 7.3 两个实例的数据应当分开

```python
morning = RecordBook("上午")
afternoon = RecordBook("下午")
morning.add(2.0)
print(morning.count())
print(afternoon.count())
```

结果1与0。每次初始化都会建立新的空列表。如果把 `records = []` 放在类的顶层，实例可能共享同一列表，导致上午的记录进入下午的记录本。

因此要分清**实例属性**与**类属性**。需要每个实例各自变化的内容，通常在`__init__`里赋给self。全体实例共享的信息可以有意放在类上，但不能误把可变的个人状态放成公共状态。

## 7.4 设计接口，不让外部随意弄乱数据

假设我们的记录要求位置是有限数值。可以让add方法统一检查，再保存。读取时则返回一份适当复制的数据，减少外部程序意外改坏原记录。

本章的[sample程序](examples/record_book.py)提供 `snapshot()`，逐条复制仅包含数值的字典。这里称为**快照（snapshot）**：记录某一时刻可供查看的数据副本。因为字段都只是数值，一层字典复制就足够；如果以后加入嵌套列表，需要重新检查复制规则。

不以双下划线等命名技巧代替接口说明。调用者仍需知道单位、允许范围、是否修改对象，以及失败时会抛出什么异常。

## 7.5 继承：在已有类型上增加约定

某些记录本只允许非负位置。可以在基础类上增加限制：

```python
class NonnegativeBook(RecordBook):
    def add(self, x_cm):
        if x_cm < 0:
            raise ValueError("本记录本不接受负位置")
        super().add(x_cm)
```

括号里的RecordBook是**父类**，新类是**子类**。子类重新定义同名方法叫**覆盖（override）**；`super().add(...)`调用继承关系中相应的已有实现，这里用于复用父类的保存逻辑。

这是例子中特定记录本的规则，不表示机器人坐标永远不能为负。是否应该用继承，要看新对象是否仍能遵守调用者对原接口的合理期待。简单问题优先用简单函数或对象组合，没必要层层继承。

## 7.6 一个对象为什么能像函数那样调用

以后你会看到 `model(data)` 这样的写法，虽然model可能是一个对象。Python允许类定义`__call__`，来说明对象被加括号调用时该做什么：

```python
class AboveThreshold:
    def __init__(self, threshold_cm):
        self.threshold_cm = threshold_cm

    def __call__(self, x_cm):
        return x_cm > self.threshold_cm

check = AboveThreshold(5.0)
print(check(7.0))
```

输出True。这个对象记住自己的阈值，每次调用检查新位置。**可调用（callable）**表示对象支持这种调用方式；`callable(check)`可以检查。

这里没有神经网络，也没有自动学习。只是提前学会以后阅读模型接口会用到的Python机制。

## 7.7 配置与日志：让别人知道做过什么

**配置（configuration）**是一次运行采用的设置，例如筛选颜色、位置阈值与输入文件。把它保存成JSON，比只在脑中记住更可靠。

**日志（log）**是运行过程或结果的记录。最小实验日志可以包括输入文件、配置、解释器版本、有效记录数、输出文件与失败原因。输出“成功”两个字不足以复现实验。

本章[配置文件](examples/config.json)保存记录本名称、位置数据与阈值。程序读取后创建对象，最后输出快照和检查结果。以后可以把读取的实际配置与结果一同存档。

**复现（reproduction）**在这里先指：别人获得代码、数据、配置和环境说明后，可以重复同样的步骤并核对结果。较复杂的科学实验还涉及统计波动与硬件差异，后面会展开。

### 随机种子先认识用途

有些程序需要打乱记录顺序。Python的伪随机数生成器按照算法产生看起来随机的序列，**种子（seed）**帮助指定其起点。

```python
import random

items = [1, 2, 3, 4]
generator = random.Random(7)
generator.shuffle(items)
print(items)
```

在相同相关环境中，使用相同生成器设置与调用顺序，可以重现这段打乱过程。但种子相同不保证所有库、硬件和并行计算都完全一致。第12章学习概率和抽样后会更准确地理解它。此处仅要求知道要记录种子、软件与操作步骤，不能把种子当成万能证明。

## 7.8 Git：保存可以回看的修改历史

复制`代码最终版2真的最终版.py`很快会乱。**Git**是一种记录文件变化的版本管理工具。每次有意义的保存可以形成一个**提交（commit）**，记录那时的文件内容和说明。

**仓库（repository）**保存项目及其版本历史。Git是工具；GitHub是可以存放远程仓库、协作和浏览内容的平台。使用本地Git不要求先注册或上传到GitHub。

先在一个新的练习目录中试，不对已有重要仓库做实验。需要Git命令时用 `git --version` 检查。以下命令在练习仓库目录内执行：

```bash
git init
git status
```

`init`建立本地仓库；`status`显示文件状态。文件改完后并不会自动进入历史，还需要两个步骤：

```bash
git add hello.py
git commit -m "Add first greeting program"
```

`add`把选定文件的当前内容放入**暂存区（staging area）**，也就是准备纳入下一次提交的内容。`commit`把暂存内容保存成版本；`-m`后是说明文字。

若提示缺少作者身份，在当前练习仓库用 `git config user.name "你的名字"` 和 `git config user.email "你选择的提交邮箱"` 配置，替换中文占位。这里不使用`--global`，避免改变所有项目的设置。

### 看清哪些内容发生了变化

修改hello.py后依次查看：

```bash
git diff
git add hello.py
git diff --staged
git commit -m "Update greeting"
git log --oneline
```

`git diff`比较工作文件与暂存区；`git diff --staged`比较暂存区与上次提交。`log`显示提交历史，`--oneline`让每次提交简洁显示。理解比较的是哪两个状态，比背命令更重要。

### 恢复时先决定要保留什么

`git restore --staged hello.py`把文件从这次暂存安排中撤回，工作目录里的修改仍保留。`git restore hello.py`则会用暂存版本恢复工作文件，丢掉相应未暂存修改。只有明确不再需要这些修改时才使用后者；先看diff，并复制需要保留的内容。

新文件如果从未被提交或暂存，Git未必能帮助找回它。版本管理替代不了对重要数据的备份。

## 7.9 哪些文件应该进入仓库

代码、教学文档、小型示例数据和必要配置适合跟随版本。可重新生成的环境、缓存、运行输出和大模型权重通常另行管理。

`.gitignore`是告诉Git哪些未跟踪路径通常忽略的文本文件，例如：

```text
.venv/
__pycache__/
*.pyc
output/
```

这些规则不会自动删除文件，也不会让已经被Git跟踪的文件自动退出历史。`__pycache__`是Python可能生成的缓存目录，不是手写源码。

## 7.10 实验与过关

从本章目录运行 `python3 examples/record_book.py`，观察记录数、快照和阈值结果。然后建立第二个记录本，确认它没有继承第一本的记录；修改快照，确认原始数据不变。

再在独立练习仓库完成两次提交，修改文件、查看diff、暂存、撤销暂存，并解释每一步。把代码、输入配置、Python版本和预期输出写进说明。

完成这些后，你已经能管理一个小型可复现程序。下一阶段会用它们学习数学和数据计算。实际运行与临时Git仓库检查见[validation.md](validation.md)。来源：[Python类](https://docs.python.org/3/tutorial/classes.html)、[随机数模块](https://docs.python.org/3/library/random.html)、[Git初始化](https://git-scm.com/docs/git-init)、[Git比较](https://git-scm.com/docs/git-diff)、[Git恢复](https://git-scm.com/docs/git-restore)，核验2026-10-24。

---

[上一章：文件、数据与排查错误](../06-files-and-debugging/README.md) · [全书目录](../../README.md) · 下一章：[第08章：数学表达式、函数与曲线](../08-math-language-and-functions/README.md)
