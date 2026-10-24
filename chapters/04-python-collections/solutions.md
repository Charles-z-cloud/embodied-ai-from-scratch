# 第 04 章参考答案与思路

[正文](README.md) · [练习](exercises.md) · [全书目录](../../README.md)

## 练习1

分别为2、8、`[4, 6]`。索引4越界，因为四个元素的非负索引为0—3。

## 练习2

```python
blocks = [
    {"color": "red", "x_cm": 2.0},
    {"color": "green", "x_cm": 8.0},
    {"color": "red", "x_cm": 7.0},
]
count = 0
selected = []
for block in blocks:
    if block["color"] == "red":
        count = count + 1
        if block["x_cm"] > 5.0:
            selected.append(block)
print(count)
print(selected)
```

数量2，结果只包含红色7厘米的记录。字典元素被结果列表引用，没有自动复制。

## 练习3

每轮清零会丢掉之前的计数。练习2会在末轮得到1，而不是累计2。应在循环之前初始化。

## 练习4

0和−2进入else，3进入计算分支。“很快”在float转换时已经报错，尚未进入if。条件只处理成功转换之后的数值范围。

## 练习5

前者让两个名称指向同一列表，后者新建外层列表。浅复制仍共享内部字典，所以不能保证字典字段独立。

## 练习6

`>`排除恰好5.0的记录，`>=`包含它。应根据任务的边界定义选择。

## 练习7

计数从0开始，循环执行零次，所以仍为0。空列表没有索引0，直接访问会报IndexError。
