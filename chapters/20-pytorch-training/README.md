# 第 20 章　使用 PyTorch 训练神经网络

[上一章：反向传播与自动求导](../19-backpropagation/README.md) · [全书目录](../../README.md) · 下一章：[第21章：让训练过程可排查、可复现](../21-training-engineering/README.md)

**阅读顺序：正文 → [练习](exercises.md) → [参考答案](solutions.md)。**

## 学会工具，而不是绕过原理

前面已经手算梯度、实现过最小求导器。这一章使用 **PyTorch**：一个提供张量计算、自动求导、神经网络模块和优化工具的Python库。它替你管理重复计算，但不会替你选择正确标签、评测划分或任务目标。

本章重做第18章四个XOR点。先用同一组手工参数对照NumPy与PyTorch前向结果，再从随机参数训练。四个点全部用于教学训练，报告的是对完整二进制真值表的拟合，不设置虚假的独立测试集，也不声称具身任务泛化。

当前实际环境：Python 3.12.10、PyTorch 2.14.1、macOS arm64、CPU。版本与安装记录见[环境说明](../../environment.md)。已有虚拟环境可安装 `python -m pip install torch`；不同硬件的GPU版本按PyTorch官方安装说明选择，本章CPU即可。

## 1. Tensor与NumPy数组有哪些相同和不同

**Tensor（张量）**在这里可以先看作带着设备位置和求导信息的多维数字表。它也有 `shape`、索引、广播、矩阵乘法，但还可以参与自动求导，放在CPU或支持的加速设备上。

```python
x = torch.tensor([[0., 1.], [1., 0.]], dtype=torch.float32)
print(x.shape, x.dtype, x.device)
```

`dtype` 是数据类型。浮点输入常用 `float32`；类别索引通常用 `torch.long`，即64位整数。整数标签编号不表示可连续调整的数值，所以通常不对它求梯度。

`device` 表示数据存放和运算的位置。`cpu` 是中央处理器；`cuda` 用于受支持的NVIDIA GPU；部分Apple环境支持`mps`加速后端。模型和输入需位于兼容设备上，否则常报设备不匹配。本章显式使用CPU，避免入门时将算法问题与硬件配置混在一起。

NumPy和PyTorch之间也能转换。`torch.from_numpy(array)` 在支持条件下与数组共享CPU内存；若想隔离修改，可以复制。把需要梯度的Tensor转成NumPy用于记录，可用 `tensor.detach().cpu().numpy()`：`detach` 得到不沿原计算图追踪梯度的视图，`cpu` 确保在CPU上。它们不应插进需要继续反传的训练路径。

## 2. requires_grad、计算图和梯度累加

`requires_grad=True` 像给一个数贴上“请记录它如何影响结果”的标签：

```python
w = torch.tensor(3., requires_grad=True)
loss = w * w + w
loss.backward()
print(w.grad)  # 7
```

PyTorch在前向时记录相关运算，`backward()` 使用第19章的链式法则。这里 `loss` 是单个标量；多元素输出若要反向，应先明确合成哪个标量目标，或提供对应的外部梯度。

直接创建并要求梯度的输入参数常称为**叶子Tensor**：它没有由其他受跟踪运算生成。默认情况下这些叶子节点会保存 `.grad`；中间节点虽然参与计算，不一定自动把梯度保存在可读取的 `.grad` 中。

PyTorch会把新的梯度加到已有参数 `.grad` 中。如果不清零，多次训练迭代会混入旧梯度。标准训练常在每次独立更新前执行 `optimizer.zero_grad(set_to_none=True)`；把梯度设为 `None` 让下一次反传重新建立它。[PyTorch 自动求导教程](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

反向后图中为求导保存的中间量通常会释放，下一步重新前向生成新图。不要为了掩盖重复反向报错，就随意加 `retain_graph=True`；先检查是否真的需要对同一图多次反传。

## 3. nn.Module：把参数与前向规则放在一起

第07章已经学过类、继承和 `super()`。PyTorch的 `nn.Module` 是所有网络模块的基础。我们定义：

```python
class XORNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
        )

    def forward(self, x):
        return self.layers(x)
```

`nn.Sequential` 按顺序调用其中的模块。`nn.Linear(2,8)` 为2个输入和8个输出管理权重与偏置，`nn.ReLU()` 不包含可学习参数。把这些子模块赋给 `self` 的属性后，它们的参数会被模块系统注册，`model.parameters()` 就能找到它们。

调用时写 `model(x)`，而不是直接依赖 `model.forward(x)`；模块调用机制还负责框架附加行为。网络输出形状 `(B,1)`，是logit；参数量为 $2\times8+8+8\times1+1=33$。

注意权重存储约定：NumPy章节用 `X @ W + b`，$W$形状是输入×输出；PyTorch `nn.Linear` 把 `.weight` 存成输出×输入，内部等价于 `X @ weight.T + bias`。因此拷贝同一组手工权重时要转置，这是约定差异，不是数学改变。

## 4. 标签、损失与输出形状对齐

本章只有一个二分类logit，使用 `nn.BCEWithLogitsLoss()`，意思是“把sigmoid和二元交叉熵用稳定方式合在一起”。输入是原始logit，标签为相同形状的浮点0或1，不要先手动sigmoid再传进去。

若是互斥的K类分类，常用 `nn.CrossEntropyLoss()`：输入 `(B,K)` 的原始logit，类别索引标签形状 `(B,)`、类型long。它内部处理稳定的log-softmax。不要先softmax后又当作logit传入。

若是回归，用 `nn.MSELoss()` 等损失，预测与目标形状应一致。能广播不意味着语义正确，第09、15章的 `(B,)` 和 `(B,1)` 陷阱在这里仍存在。

## 5. Dataset和DataLoader让数据按批到来

**Dataset（数据集对象）**像一本能按页码取出样本的册子；**DataLoader（数据加载器）**像把册子中的若干页整理成一叠，再送给训练程序。准确地说，前者定义样本读取，后者负责分批、可选打乱以及加载调度。

本章数据已在内存中，用 `TensorDataset(x,y)` 把同一行输入与标签绑定，再用 `DataLoader(..., batch_size=2, shuffle=True, num_workers=0)` 分批。4个样本每轮2步；`num_workers=0` 表示由当前进程加载，最便于跨平台入门排错。

打乱时必须让输入与标签一起移动，不能分别打乱两个数组。示例给DataLoader一个固定种子的生成器，使本环境中的抽样顺序可复现。

## 6. 训练循环每一行都要能解释

```python
model.train()
for features, targets in loader:
    optimizer.zero_grad(set_to_none=True)
    logits = model(features)
    loss = criterion(logits, targets)
    loss.backward()
    optimizer.step()
```

先切到训练模式，再每批清零、前向、计算损失、反向、更新。`optimizer` 本章用 `torch.optim.Adam(model.parameters(), lr=0.03)`，它更新注册参数，采用第14章的Adam机制。`loss.backward()` 本身不会改变权重。[PyTorch 优化教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)

记录一轮平均损失时，先将每批平均损失乘以该批样本数，加起来再除以总样本数。尤其最后一批较小时，不能简单对各批均值再等权平均。

`loss.item()` 把单元素Tensor转成Python数，适合写日志；如果把它当作新的训练目标，就已经不再是原计算图中的Tensor，不能继续自动求导。

## 7. eval和no_grad解决两个不同问题

`model.eval()` 设置评估模式，让某些层改变行为；`model.train()` 设置训练模式。下一章的Dropout和BatchNorm需要这种区别。当前纯Linear/ReLU网络两种模式的数值规则相同，但仍应形成正确习惯。

`with torch.no_grad():` 则停止记录梯度计算，节省推理时的相关开销；它不会自动把模型切到评估模式。因此常同时使用：

```python
model.eval()
with torch.no_grad():
    logits = model(x)
    probability = torch.sigmoid(logits)
    predicted = probability >= 0.5
```

这里sigmoid用于解释预测概率，训练损失依然接收logit。`eval()`也不是冻结参数的同义词，只有模式切换并不能禁止梯度计算或优化器更新。

## 8. 保存参数，并验证加载后的输出

**state_dict**像给模型各部件贴名字后记录数值的一张表，包含注册参数和持久缓冲状态。保存与加载示例：

```python
torch.save(model.state_dict(), path)
restored = XORNet()
state = torch.load(path, map_location="cpu", weights_only=True)
restored.load_state_dict(state)
restored.eval()
```

新对象的结构必须匹配。保存权重不等于保存了所有训练状态；若想从中断处继续Adam训练，还要保存优化器状态、步数与随机状态，下一章会展开。本章加载自己刚保存的参数文件，核对输出一致。[PyTorch 保存与加载教程](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html)

部署所需的不只权重，还包括输入单位、预处理、类别顺序、网络结构和运行环境。即使文件能加载，如果把输入两列调换，预测语义也会错误。

## 9. 实验入口与检查方法

```bash
python chapters/20-pytorch-training/examples/tensor_and_forward.py
python chapters/20-pytorch-training/examples/train_xor.py
```

第一份脚本比较同参数的NumPy/PyTorch前向，并展示独立计算图的梯度累积。第二份脚本随机初始化33参数网络，固定种子7，Adam学习率0.03，小批量2，训练400轮。输出记录保存到本章 `examples/output/`，包括参数文件与JSON报告。

如果损失不下降，先打印一批输入与标签，再看logit和loss形状、参数梯度是否存在、优化器是否收到正确参数，不要一开始就切换GPU。实际运行结果与范围见本章完成后附上的检查记录。

## 过关标准

能独立写出训练循环并解释五个计算动作；能给每个Tensor标注形状、类型、设备；能区别train/eval与是否求导；能保存、重建同结构模型、加载参数并核对预测。做到这些以后，才进入更真实的训练排错与工程问题。

---

[上一章：反向传播与自动求导](../19-backpropagation/README.md) · [全书目录](../../README.md) · 下一章：[第21章：让训练过程可排查、可复现](../21-training-engineering/README.md)
