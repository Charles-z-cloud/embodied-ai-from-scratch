# 第 04 章　列表、字典、条件与循环

[上一章：Python 的数值、变量与表达式](../03-python-values/README.md) · [全书目录](../../README.md) · 下一章：[第05章：函数、模块与拆分程序](../05-python-functions/README.md)

**阅读顺序：正文 → [练习](exercises.md) → [参考答案](solutions.md)。**

## 4.1 一个值不够用了

前置：[第03章](../03-python-values/README.md)。我们已经可以处理一个方块的位置，但一张桌上可能有很多物体，相机也可能连续记录多个时刻。为每条记录写 `x1`、`x2`、`x3`，很快就难以维护。

本章用容器把多个值放在一起，再用条件与循环处理它们。**容器**就是能保存其他对象的数据结构；你可以先把它理解为有组织的收纳盒。

## 4.2 列表：保留先后顺序

**列表（list）**是一组按顺序存放的对象，使用方括号和逗号：

```python
positions_cm = [2.0, 3.5, 6.0]
print(positions_cm[0])
print(positions_cm[2])
```

输出2.0与6.0。方括号中用来指定位置的整数称为**索引（index）**。Python的列表索引从0开始：第一个元素编号0，第二个编号1，第三个编号2。`len(positions_cm)` 返回元素数量3，因此最后一个正常非负索引是2，而不是3。

`positions_cm[-1]` 取最后一个元素，`[-2]` 取倒数第二个。索引越出范围会产生 `IndexError`。空列表写为 `[]`，它没有“第一个”或“最后一个”元素，使用前需要检查。

### 切片取出一段

`positions_cm[0:2]` 得到 `[2.0, 3.5]`，从索引0开始，到索引2之前停止。这样的区间采用“包含起点、不包含终点”的规则。省略起点默认从头，省略终点默认到末尾，所以 `positions_cm[1:]` 取第二个到最后一个。

切片产生新的列表；它不会删除原来的元素。步长形式如 `[::2]` 表示隔一个取一个，等掌握普通切片后再尝试。

### 修改与追加

```python
positions_cm[0] = 2.5
positions_cm.append(7.0)
print(positions_cm)
```

`列表.append(值)` 是向末尾追加元素的写法。点号表示访问这个对象提供的操作，这种绑定在对象上的操作称为**方法（method）**。本章使用现成方法，第07章再学习怎样定义自己的类与方法。

## 4.3 元组与字典解决不同问题

**元组（tuple）**也保存有序对象，例如 `point_cm = (2.0, 5.0)`。创建后不能直接替换其中的元素，适合表达不打算改变结构的一组值。它也能按索引读取，`point_cm[0]` 为2.0。只有一个元素时需要逗号，如 `(2.0,)`。元组不能直接改元素，不意味着其中包含的列表也会自动冻结。

有时编号不如名称清楚。`["red", 2.0, 5.0]` 要靠记忆知道第二项是什么；**字典（dict）**用名称或其他可用的键对应值：

```python
block = {"color": "red", "x_cm": 2.0, "y_cm": 5.0}
print(block["color"])
block["x_cm"] = 3.0
```

`"color"` 是**键（key）**，`"red"` 是对应的值。冒号表示键值对应，逗号分隔不同项。`block["missing"]` 在不存在这个键时会产生 `KeyError`。如果允许缺失并给默认值，可以写 `block.get("name", "未命名")`。`.get` 不会自动把默认项写入字典。

**嵌套（nesting）**就是容器里再放容器。多条物体记录可以表示为字典组成的列表：

```python
blocks = [
    {"color": "red", "x_cm": 2.0},
    {"color": "green", "x_cm": 8.0},
]
print(blocks[1]["x_cm"])
```

先通过 `[1]` 找到第二条字典，再通过 `["x_cm"]` 取位置，结果8.0。不要一次把这一串符号看成新魔法，把它拆成两次查找即可。

## 4.4 条件分支：只有条件满足才做

上一章写出 `duration_s > 0` 只能产生真假。**条件分支（conditional branch）**让程序根据这个真假选择代码。

```python
duration_s = 0.0
if duration_s > 0:
    velocity_cm_s = 6.0 / duration_s
    print(velocity_cm_s)
else:
    print("经过时间必须大于0。")
```

`if` 表示“如果”，冒号之后是条件满足时执行的代码块；`else` 表示否则。缩进显示哪些行属于同一个代码块。本书统一每层缩进四个空格，避免混用Tab。

本例条件为假，因此只打印提示，没有执行除法。把时间改为3才会进入第一块。若要区分多个互斥情况，可以用 `elif`，意思是“否则如果”：

```python
if position_cm < 0:
    print("在原点左边")
elif position_cm == 0:
    print("在原点")
else:
    print("在原点右边")
```

运行这段之前需先给 `position_cm` 赋值。`if/elif/else` 按顺序判断，执行第一个满足的分支；多个独立 `if` 则可以各自执行，二者含义不同。

`in` 可以判断成员关系，例如 `"color" in block` 检查字典是否有这个键；`"red" in colors` 检查列表中是否包含这个值。

## 4.5 for：对每条记录重复相同操作

**循环（loop）**是重复执行一段代码。`for` 逐个取得容器里的元素：

```python
positions_cm = [2.0, 3.5, 6.0]
for position_cm in positions_cm:
    print(position_cm)
```

第一次 `position_cm` 取2.0，第二次取3.5，第三次取6.0，然后循环结束。这里每次拿到的是值，不是索引。若同时需要编号和值，使用 `enumerate`：

```python
for index, position_cm in enumerate(positions_cm):
    print(index, position_cm)
```

逗号把每次取得的两个内容分别放入两个名称，这叫**解包（unpacking）**。若只想重复固定次数，`range(3)` 给出0、1、2这三个整数，可以写 `for index in range(3):`。

### 计数和累计

设三条物体记录颜色为红、绿、红，要数红色物体：

```python
red_count = 0
for block in blocks:
    if block["color"] == "red":
        red_count = red_count + 1
print(red_count)
```

先在循环外把计数设为0；每遇到符合条件的记录就加一。如果把初始化放进循环，之前的累计结果就会被清掉。上面沿用前面两条记录时输出1，改成三条红绿红记录才输出2。

循环也可以筛选数据：先建空列表 `selected = []`，符合条件时调用 `selected.append(block)`。遍历一个列表时直接删除它的元素，容易改变后续迭代的位置；初学时优先建立结果列表。

## 4.6 while：只要条件满足就继续

`while` 每次执行代码块之前检查条件。例如，让数值位置一步步靠近5厘米：

```python
position_cm = 2
while position_cm < 5:
    position_cm = position_cm + 1
    print(position_cm)
```

输出3、4、5。最后再检查时，5小于5为假，结束循环。若忘记更新 `position_cm`，条件可能永远成立，形成无限循环。运行中可以用Ctrl+C中断。

这是一个数值练习，不是向真实机器人发指令。如果数值需要多次尝试，最好明确停止条件。`break` 立即退出当前循环，`continue` 跳过当前这一轮的剩余代码、进入下一轮。

在 `while` 中使用 `continue` 时尤其要小心：若跳过了改变条件的那一行，就可能停不下来。能用 `for` 表达有限条记录的处理时，优先用它。

## 4.7 变量别名与复制

第03章中把整数x赋给y，后来重新给x赋值不会改变y。但列表本身可以修改，情况有所不同：

```python
original = [2.0, 3.0]
alias = original
alias.append(4.0)
print(original)
```

输出 `[2.0, 3.0, 4.0]`。两个名称指向同一个列表，追加改变了这个列表本身。`alias = original` 没有复制一份内容。

```python
copied = original.copy()
copied.append(5.0)
print(original)
```

现在original不会多出5.0，因为`.copy()`创建了一个新的外层列表。不过这是**浅复制（shallow copy）**：若元素是字典或列表，它们仍可能被共享。

例如 `copied_blocks = blocks.copy()` 后，修改 `copied_blocks[0]["x_cm"]` 也会影响原来第一条字典。这时只复制了装记录的盒子，没有复制记录本身。主线练习会主动新建需要独立修改的字典；复杂递归复制以后按需介绍。

## 4.8 完整实验：筛选物体记录

[examples/records.py](examples/records.py)包含四条数据。脚本统计红色物体数量，并找出红色且位置大于5厘米的记录。从本章目录运行：

```bash
python3 examples/records.py
```

预期红色数量为3，筛选的位置为7.0与9.0。请逐轮记录“当前颜色、当前位置、red_count、selected”，再对照输出。随后加入一条位置恰好为5.0的红色记录，观察 `>` 与 `>=` 的区别。

[examples/valid_time.py](examples/valid_time.py)先接收数值输入，再用条件阻止非正时间参与除法。输入文字仍会转换失败，这一限制要到第06章的异常处理才补齐。

## 4.9 小结与过关

列表解决顺序，字典解决按名称查值；条件决定执行哪一段，循环决定重复处理哪些内容。可变容器可能被多个名称共享，修改与重新赋值要分清。

过关时应能够处理一组字典记录、统计与筛选、解释循环每一步的状态，并对空列表、边界值和缺失键作出明确安排。示例检查见[validation.md](validation.md)。行为参考：[Python 控制流](https://docs.python.org/3/tutorial/controlflow.html)和[数据结构](https://docs.python.org/3/tutorial/datastructures.html)，核验2026-10-24。

---

[上一章：Python 的数值、变量与表达式](../03-python-values/README.md) · [全书目录](../../README.md) · 下一章：[第05章：函数、模块与拆分程序](../05-python-functions/README.md)
