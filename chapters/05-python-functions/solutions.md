# 第 05 章参考答案与思路

[正文](README.md) · [练习](exercises.md) · [全书目录](../../README.md)

## 练习1

```python
def distance_1d(start_cm, end_cm):
    return abs(end_cm - start_cm)
```

它不保留方向，结果非负。只有起终点，无法得知途中总路程；中间往返可能增加路程。

## 练习2

得到None。用return返回计算结果，让外层再按需print。显示与返回可以同时发生，但用途要区分。

## 练习3

第一次走到return就离开函数，第二条记录没有机会被处理。需要处理完后返回完整列表。

## 练习4

`average_velocity(2.0, 8.0, 3.0)`，或 `average_velocity(start_cm=2.0, end_cm=8.0, duration_s=3.0)`。用 `if result is None:` 处理无效时间，不把None作为数值。

## 练习5

演示放入main函数，并在 `if __name__ == "__main__":` 之下调用。模块里保留可导入的工具函数定义。

## 练习6

不会。类型提示表达期望，不负责通常的运行时转换和完整校验。仍需按接口约定转换和检查输入。
