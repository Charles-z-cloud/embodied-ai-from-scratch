# 第 20 章练习与自测

[正文](README.md) · [参考答案](solutions.md) · [全书目录](../../README.md)

1. `nn.Linear(3,5)` 的weight、bias各是什么形状？批量8时输出形状与参数量是多少？
2. 二分类一个logit使用BCEWithLogitsLoss，标签类型和形状有什么要求？为何不能先sigmoid？
3. 连续两次计算新的 `loss=w*w` 并反传，但不清空w.grad，w=2且不更新权重时，最终梯度是多少？
4. `model.eval()` 是否关闭梯度？`torch.no_grad()` 是否自动启用评估模式？
5. Dataset中有10个样本，batch_size=4，最后一批损失均值4，其余两批均值各1，一轮正确平均损失是多少？
6. 只加载state_dict到不同隐藏宽度的模型会怎样？只存模型权重是否能精确恢复Adam训练？
7. 本章XOR训练全部正确，为什么没有宣称新场景泛化？怎样设计后续连续二维任务的独立测试？
