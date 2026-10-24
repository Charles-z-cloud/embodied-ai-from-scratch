# 第 05 章　函数、模块与拆分程序

[上一章：列表、字典、条件与循环](../04-python-collections/README.md) · [全书目录](../../README.md) · 下一章：[第06章：文件、数据与排查错误](../06-files-and-debugging/README.md)

**阅读顺序：正文 → [练习](exercises.md) → [参考答案](solutions.md)。**

## 5.1 为什么要把代码分成小块

前置：[第04章](../04-python-collections/README.md)。如果三个实验都要计算位移，把同样几行复制三遍，修改单位时就容易漏掉一处。我们希望给这段计算一个名称，提供输入，就能重复得到结果。

**函数（function）**可以理解为有明确入口和出口的小工具。准确地说，它是一段可调用的代码，可以接收参数、执行操作并返回结果。先学会函数，再把有关函数放进模块，才能逐步组织更大的训练程序。

## 5.2 定义与调用不是同一件事

```python
def displacement(start_cm, end_cm):
    change_cm = end_cm - start_cm
    return change_cm

result = displacement(2.0, 8.0)
print(result)
```

`def` 开始定义函数；`displacement` 是名称；括号里的 `start_cm` 和 `end_cm` 是**形参**，也就是定义入口时使用的名称。冒号与缩进表示函数内部的代码块。

写下定义时，Python建立这个函数，但不会立刻替你算一次位移。直到执行 `displacement(2.0, 8.0)` 才真正调用它；2.0和8.0是这次调用提供的**实参**。进入函数后，它们分别对应start_cm与end_cm。

`return` 把结果交回调用位置并结束这一次函数执行。因此 `result` 得到6.0。下一次调用 `displacement(8.0, 2.0)` 会得到−6.0，前一次调用不会把这个结果固定住。

## 5.3 return 与 print

`print` 把内容展示给人，`return` 把结果交给后续程序。这两项工作不同：

```python
def show_displacement(start_cm, end_cm):
    print(end_cm - start_cm)

result = show_displacement(2.0, 8.0)
print(result)
```

这里先显示6.0，随后显示 `None`。**None**是Python中专门表示“这里没有提供一个通常结果”的值。函数执行到结尾没有return时，会返回None。

如果你希望结果继续参与计算，就要返回数值。一般让计算函数返回数据，让外层程序决定怎样打印，日后便能把同样的结果保存成文件、画图或交给另一个函数。

一旦执行return，这次调用就结束；写在其后且没有其他到达路径的语句不会执行。初学者常把循环中的return写得太早，导致只处理了第一条记录。

## 5.4 参数名称、默认值与调用顺序

除了按位置传值，还可以明确写参数名：

```python
result = displacement(end_cm=8.0, start_cm=2.0)
```

这叫**关键字参数**，可以减少位置弄反。位置参数必须写在普通关键字参数之前，同一个参数不能重复传两次。

有些参数有常见值，可以提供默认值：

```python
def select_color(records, color="red"):
    selected = []
    for record in records:
        if record["color"] == color:
            selected.append(record)
    return selected
```

`select_color(records)`默认筛选红色；`select_color(records, color="green")`改为绿色。返回语句放在循环之后，才会收集全部符合条件的记录。

默认参数在函数定义时建立。如果把可变列表作为默认值，多个调用可能共享它。因此不把“每次都应该是新的列表”直接写成默认参数。需要这种设计时，可以默认None，再在函数内部创建：

```python
def add_record(record, records=None):
    if records is None:
        records = []
    records.append(record)
    return records
```

`is None` 检查是不是那个专门的None对象，不用它替代所有数值相等比较。注意：如果传入已有列表，函数会修改这个列表；这应在函数说明里写清楚。

## 5.5 局部变量与副作用

函数里的临时名称通常是**局部变量**，只在这次函数调用的范围内使用。前面函数里的 `change_cm` 不会自动变成外部程序能直接使用的变量；通过return把必要结果交出来即可。

参数也只是名称。给一个数值参数重新赋值，通常不改变调用者的名称；但是对传入列表调用append，可能改到调用者同样引用的那个列表。

这种“除了返回结果，还改变了外部可见状态”的行为称为**副作用（side effect）**。打印、写文件、修改传入列表都属于常见副作用。副作用不是必然错误，但需要有意安排。

我们在 `select_color` 中新建结果列表，却仍然引用原来的记录字典。所以返回列表之后直接修改其中字典的字段，仍可能影响原数据。这与第04章的共享引用规则一致。

## 5.6 让函数互相配合

我们想把三件事分开：计算位移、筛选记录、报告结果。代码可以先调用筛选函数，再对结果调用计算函数，最后统一打印。

还有一种情况是输入有效性。当前先采用None作为无法计算的返回值：

```python
def average_velocity(start_cm, end_cm, duration_s):
    if duration_s <= 0:
        return None
    change_cm = displacement(start_cm, end_cm)
    return change_cm / duration_s
```

这个函数约定输入已经是数值。外层必须检查None，不能直接拿它做算术：

```python
velocity = average_velocity(2.0, 8.0, 0.0)
if velocity is None:
    print("无法计算：经过时间必须大于0。")
else:
    print("平均速度：", velocity)
```

第06章会学习另一种表达错误的方式——异常。现在重要的是输入要求、成功结果和失败结果都写清楚。

### 简单类型提示

有时你会看到：

```python
def displacement(start_cm: float, end_cm: float) -> float:
    return end_cm - start_cm
```

冒号后的float说明希望传入浮点数，箭头后说明希望返回浮点数，这叫**类型提示（type hint）**。它帮助读者和检查工具理解接口；Python通常不会仅因为这条提示就自动转换输入或拒绝错误类型。

本章示例不依赖复杂类型写法。以后看到训练代码中的提示，也先把它当作接口说明，不要以为它替代了运行时检查。

## 5.7 模块：把工具放进另一个文件

**模块（module）**可以先理解为可被导入的Python文件。把 `displacement`、`average_velocity` 和 `select_color` 放入 `motion.py`，就能在同目录的 `main.py` 中使用：

```python
from motion import displacement
print(displacement(2.0, 8.0))
```

`from motion import displacement` 表示从motion模块取出这个名称。导入名称不写`.py`。也可以 `import motion`，然后写 `motion.displacement(...)`；点号说明使用的是这个模块里的工具。

Python还自带很多模块，称为**标准库（standard library）**。下一章处理CSV与JSON时会用到它们。标准库通常无需额外pip安装；第三方包则要安装到正在使用的环境中。

导入自己的文件时要注意命名。不要把练习文件命名为常用标准库的名字，例如 `json.py`，以免它遮住真正想使用的工具。

## 5.8 为什么示例里经常有 __name__

导入模块时，Python会执行其中顶层的语句，包括没有被函数包住的print。因此需要区分“别人导入我的函数”和“我直接运行这份文件”。

```python
def main():
    print(displacement(2.0, 8.0))

if __name__ == "__main__":
    main()
```

`__name__` 是Python提供的名称。直接运行该文件时，它是字符串 `"__main__"`，于是执行main；被其他模块导入时，它通常是模块名称，就不进入这段演示。下划线数量是写法的一部分。

这不是要求每份程序都必须有这个结构，但它能让工具文件在被导入时保持安静，便于复用与检查。

## 5.9 实验：三条轨迹的处理

[examples/motion.py](examples/motion.py)提供函数，[examples/main.py](examples/main.py)组织示例。从本章目录运行：

```bash
python3 examples/main.py
```

筛选两条红色记录，分别输出速度2.0和“时间无效”。绿色记录不会进入报告。把颜色改成green，观察筛选结果改变；修改函数时只改工具文件即可。

检查函数时，先准备小而明确的输入输出：位移(2,8)应为6；(8,2)应为−6；空记录列表筛选应为空；时间0应返回None。它们分别检查普通情况、方向、空输入与边界，能帮助发现只对一个例子碰巧正确的实现。

## 5.10 小结

函数提供明确的输入输出，模块把相关工具组合起来。可复用代码应让调用者知道参数、单位、返回值和副作用。能导入一个函数并不意味着已经理解它，仍需要通过小例子确认行为。

完成标准是独立拆出计算、筛选和显示三个部分，解释return与print，并从另一个文件调用工具。实际检查见[validation.md](validation.md)。参考：[函数定义与参数](https://docs.python.org/3/tutorial/controlflow.html)、[模块](https://docs.python.org/3/tutorial/modules.html)，核验2026-10-24。

---

[上一章：列表、字典、条件与循环](../04-python-collections/README.md) · [全书目录](../../README.md) · 下一章：[第06章：文件、数据与排查错误](../06-files-and-debugging/README.md)
