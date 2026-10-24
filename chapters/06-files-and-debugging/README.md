# 第 06 章　文件、数据与排查错误

[上一章：函数、模块与拆分程序](../05-python-functions/README.md) · [全书目录](../../README.md) · 下一章：[第07章：对象、Git 与可重复的实验记录](../07-classes-git-and-reproducibility/README.md)

**阅读顺序：正文 → [练习](exercises.md) → [参考答案](solutions.md)。**

## 6.1 让数据离开程序源码

前置：[第05章](../05-python-functions/README.md)。把三条记录直接写在程序中很方便，但相机采集了几千条记录后，就需要把数据保存为文件。本章把“读取 → 检查 → 计算 → 输出”接起来，同时保留原始数据和被拒绝记录的原因。

**数据字段（field）**是记录中的一个有名称的部分，例如颜色、起点位置和经过时间。读文件之前先确定每个字段的名称、类型、单位与允许范围；否则文件能打开，也未必能正确解释其中的数据。

## 6.2 文本、编码与打开方式

电脑保存文字时，需要规则把字符与存储的数字对应起来，这些规则叫**字符编码（encoding）**。本书文本统一使用UTF-8，避免不同机器默认设置造成中文乱码。

```python
with open("note.txt", "w", encoding="utf-8") as file:
    file.write("记录一次方块移动。\n")
```

`open`打开文件；`"w"`表示写入模式，会创建文件，或覆盖同名文件的已有内容。`encoding`明确编码。`as file`让我们用file这个名称操作打开的文件；`write`写入文字。字符串里的 `\n` 是一个换行符，不是要显示的两个普通字符。

**with语句**在进入代码块时取得资源，退出时负责释放；这里就是在离开代码块时关闭文件，即使中途发生错误也会执行必要的关闭操作。具体机制可以以后再研究，此时会正确使用即可。

读取使用 `"r"`：

```python
with open("note.txt", "r", encoding="utf-8") as file:
    text = file.read()
print(text)
```

`read()`一次读出全部文本，适合本章的小文件。较大文件可以 `for line in file:` 逐行处理。追加模式`"a"`在末尾继续写，但重复运行可能重复添加，必须符合实验意图。

## 6.3 路径不是跟着脚本自动走的

`open("note.txt")`通常以**当前工作目录**为起点，不是以源码所在目录为起点。从不同目录运行同一程序，可能读到不同的文件。

标准库 `pathlib` 提供Path工具来表达路径：

```python
from pathlib import Path

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "records.csv"
```

`__file__`在普通脚本中提供当前源码文件的路径；交互窗口中通常没有它。`Path(...)`把路径变成一个可操作的对象，`resolve()`得到解析后的绝对路径，`.parent`取得上级目录。Path对象之间的`/`用于拼接路径，这里不是做数值除法。

这样可以明确表示“读取与当前脚本放在一起的records.csv”。`Path`也有`.exists()`检查存在性、`.mkdir(parents=True, exist_ok=True)`创建必要目录等操作；两个参数分别表示允许创建上级目录、允许目标目录已经存在。

本章输出放入独立的output目录，不写回原始CSV。重新运行会覆盖生成的report.json，这是明确约定的示例行为。

## 6.4 CSV：每行一条记录

CSV可先理解为“用逗号分隔列的文本表格”。本章使用第一行作为字段名：

```csv
color,start_cm,end_cm,duration_s
red,2,8,3
green,8,2,3
```

第一条记录红色方块从2厘米到8厘米，经过3秒。CSV本身没有规定这些列都是浮点数；读取到的`"2"`仍需按我们自己的约定转换。

使用标准库csv读取：

```python
import csv

with open(input_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["color"], row["start_cm"])
```

`DictReader`按照表头把每条记录变成字典。`newline=""`让csv工具处理换行约定。字段中含逗号或引号时，CSV有专门的引用规则，因此不要简单用 `split(",")`代替正式读取器。需要不同分隔符时应明确配置。

本章代码还会检查表头与约定一致，避免误把米当成厘米。`reader.line_num`记录读取到的物理行位置；跨多行的CSV记录可能不只占一行，所以记录编号和文件行号不是永远相同。

## 6.5 错误为什么会沿着函数一层层返回

如果执行 `float("很快")`，语法本身合法，但这段文字不能转换成数字。执行时发现这类问题会产生**异常（exception）**。

未处理的异常通常会打印 **Traceback**，也就是调用过程的记录：哪里调用了哪个函数，最后哪一行出了问题。读报错时先看最后一行的异常类型和说明，再沿着文件名与行号定位；真正的原因有时在更早的数据处理环节。

例如“在除法处报错”可能是前面允许了时间0。只修改报错那一行未必解决了输入约定问题。

### 捕获可以预期的错误

```python
try:
    duration_s = float("很快")
except ValueError:
    print("时间必须是数值文字。")
```

`try`中的操作尝试执行；若出现指定的ValueError，进入对应的except块。若没有错误，就跳过该except。捕获错误后要明确怎么办，例如提示重新输入或拒绝这条记录，不能把坏数据悄悄当成0。

只捕获自己能够处理的错误。把整个程序包在一个不分类型的捕获块里，会掩盖拼写错误、缺文件等不同原因，也让后面的结果难以相信。

### 主动报告不满足约定的数据

```python
if duration_s <= 0:
    raise ValueError("经过时间必须大于0")
```

`raise`主动产生异常，把错误交给调用者处理。相比第05章返回None，这是一种更显式的失败约定；需要在接口说明中讲清楚。

`except ValueError as error:` 可以给捕获到的异常起一个名称，`str(error)`取得其中的文字说明。不要把所有失败当作相同的“程序没用”。

## 6.6 缺失、格式错误与范围错误

检查数据时至少要区分：

| 情况 | 例子 | 本章处理 |
| --- | --- | --- |
| 缺失 | 起点字段为空 | 拒绝该条并记录原因 |
| 格式不对 | 起点写成“很远” | 数值转换失败，记录原因 |
| 范围不合理 | 经过时间为0或负数 | 拒绝该条 |
| 数值不是有限值 | NaN或无穷大 | 拒绝该条 |
| 字段不匹配 | 表头写成start_m | 停止处理，要求明确单位约定 |

**NaN**表示“不是一个有效数值结果”的特殊浮点值，**无穷大**也可以以特殊浮点形式存在。`float("nan")`或`float("inf")`可能转换成功，所以“能转换”不代表“适合本任务”。标准库 `math.isfinite(value)`检查是否为有限数值。

本例把颜色限制为red、green、blue；位置允许正负数，单位厘米；时间必须是正的有限数。实际数据集应根据任务制定规则，不应无理由删除所有负位置。

读取CSV后，字符串的 `.strip()`可以去掉首尾空白。它不会修复错误单位，也不会证明数据真实。清洗数据必须保留处理记录，避免不知道最后少了哪些样本。

## 6.7 JSON：保存有结构的结果

CSV适合规则的表格，**JSON**适合表达嵌套的记录、列表和配置。它是一种与具体编程语言无关的文本数据格式。Python中的字典与列表可以转换成JSON。

```python
import json

report = {"accepted": 2, "message": "已检查"}
with open("report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, ensure_ascii=False, indent=2)
```

`dump`把对象写到文件；`ensure_ascii=False`让中文直接显示；`indent=2`以两个空格缩进便于阅读。读取用`json.load(file)`。

JSON里的字符串通常用双引号；Python的True、False、None对应JSON的true、false、null。JSON不是可以随意执行的Python代码，也不能靠改扩展名就完成转换。本章输出还设置`allow_nan=False`，避免把NaN等写成不符合通常JSON约定的数值。

## 6.8 完整实验：清洗移动记录

目录中的[records.csv](examples/records.csv)有6条记录：2条有效，另外4条分别缺失数值、时间为0、数值格式错误、出现NaN。[clean_records.py](examples/clean_records.py)按以下步骤处理：

1. 检查表头是否完全符合字段和单位约定。
2. 对每条记录检查字段、转换数字、检查有限性与时间。
3. 成功时计算位移和速度，保存到有效结果。
4. 失败时保存文件行号和具体原因。
5. 把统计、有效记录和拒绝原因写到新的JSON文件。

运行：

```bash
python3 examples/clean_records.py
```

预期显示有效2条、拒绝4条，并产生 `examples/output/report.json`。第一条速度2.0，第二条速度−2.0。查看拒绝信息，确认每条被排除的数据都有解释。

代码中的 `f"字段缺失：{name}"` 是**格式化字符串**：前面的f允许把花括号内的值放进文字。`set(row)`得到当前字典的键集合；集合只关心有哪些不同元素，代码用它检查是否存在多余或缺失列。核心流程的函数、循环、分支都来自前面章节。

## 6.9 小结与过关

文件读写需要明确路径、编码和模式。结构化文件需要明确字段类型与单位。异常处理的目的，是让失败有可解释的去向，而不是让程序无论数据多坏都宣布成功。

过关时能读取一份CSV，保留原始文件、报告坏行并输出JSON；能沿Traceback找到故障位置；能解释为什么NaN、缺字段和时间0是不同检查。

实际验证见[validation.md](validation.md)。来源：[文件读写](https://docs.python.org/3/tutorial/inputoutput.html)、[异常](https://docs.python.org/3/tutorial/errors.html)、[csv](https://docs.python.org/3/library/csv.html)、[json](https://docs.python.org/3/library/json.html)，核验2026-10-24。

---

[上一章：函数、模块与拆分程序](../05-python-functions/README.md) · [全书目录](../../README.md) · 下一章：[第07章：对象、Git 与可重复的实验记录](../07-classes-git-and-reproducibility/README.md)
