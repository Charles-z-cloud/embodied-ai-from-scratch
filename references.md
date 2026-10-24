# 官方资料、经典项目与来源记录

[返回阅读入口](README.md) · [项目阅读安排](project-plan.md)

核验日期：**2026-10-24**。以下页面已通过网页访问或搜索结果核对其存在与主要用途；来源网页核验不等于完整仓库运行。Python、NumPy、PyTorch等基础依赖及Gymnasium已用于教材自编实验；其他经典仓库的完整训练或推理未运行。实际版本见[环境说明](environment.md)，动态链接可能变化。

本书的学习顺序是针对初学者目标做出的教学安排，不是某个项目官方推荐的唯一顺序。

## 基础资料

| 资料 | 适合进入的位置 | 选用理由与使用方式 |
| --- | --- | --- |
| [Python 官方教程](https://docs.python.org/3/tutorial/) | 第03—07章 | 用来核对语言行为。官方教程面向已经具有编程常识的读者，本教材会补齐从零编程的解释，不直接要求初学者读完它 |
| [NumPy 初学者指南](https://numpy.org/doc/stable/user/absolute_beginners.html) | 第09章 | 核对数组、索引、形状与基本运算 |
| [PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/) | 第20—21章 | 对照数据加载、网络、自动求导和训练流程 |
| [Dive into Deep Learning](https://d2l.ai/) | 第09章以后按主题选读 | 数学基础、深度学习和注意力的参考材料；本教材按自身前置顺序讲解 |
| [Modern Robotics：运动基础](https://modernrobotics.northwestern.edu/nu-gm-book-resource/foundations-of-robot-motion/) | 第33—35章 | 核对位置、姿态、自由度和刚体运动的基础位置 |
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 第27章后 | Transformer 原始论文；先读架构和注意力，完整机器翻译实验可选学 |

## 开源项目索引

| 项目 | 身份与用途 | 当前采用方式 |
| --- | --- | --- |
| [micrograd](https://github.com/karpathy/micrograd) | 作者的微型自动求导项目 | 第19章后选读标量反向传播 |
| [nanoGPT](https://github.com/karpathy/nanoGPT) | 作者的紧凑 GPT 训练实现 | 第28章历史代码选读；README 已标明老旧与弃用 |
| [OpenCLIP](https://github.com/mlfoundations/open_clip) | 开放 CLIP 实现与训练生态 | 第31章图文检索；明确与原始论文实现区分 |
| [LLaVA](https://github.com/haotian-liu/LLaVA) | 视觉指令微调作者仓库 | 第32章架构和数据流案例 |
| [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) | Farama 的交互环境接口项目 | 第37章轻量环境；配合[基本用法](https://gymnasium.farama.org/introduction/basic_usage/) |
| [LeRobot](https://github.com/huggingface/lerobot) | Hugging Face 的机器人学习工具 | 第41、46、54章分层阅读；配合[官方文档](https://huggingface.co/docs/lerobot/index) |
| [Diffusion Policy](https://github.com/real-stanford/diffusion_policy) | 论文作者的动作扩散实现 | 第46章后；完整基准的平台要求独立核对 |
| [DreamerV3](https://github.com/danijar/dreamerv3) | 作者维护的 JAX 重实现 | 第50章后；先讲框架差异，完整复现选学 |
| [OpenVLA](https://github.com/openvla/openvla) | VLA 作者仓库 | 第52章案例，第54章后考虑资源允许的适配 |

每个项目的阅读入口、练习、资源边界和替代路径见[项目安排](project-plan.md)。本次未按星标数或“最新排行榜”排序，也未把网页仍可访问等同于项目仍积极维护。

## 来源记录原则

每条核心来源至少记录：标题、作者或维护者、年份、原文链接、对应章节、所支持的结论、核验时间。涉及模型能力时指出评测任务和实验条件；涉及运行时增加版本或提交、权重和环境。

收录实际访问并核对过的资料。VAE、扩散、流匹配及其他方法的来源已在对应章节及下方索引中列出；摘要或项目页核验不标为已精读全文。

## 第01章补充来源

核验日期：2026-10-24。用途为概念入门与案例定位；访问论文摘要或作者项目页，不声称已完成全文精读或实验复现。

| 来源 | 作者或维护者、年份 | 支持的内容 | 对应正文 |
| --- | --- | --- | --- |
| [AI Habitat](https://aihabitat.org/) | Habitat 项目团队，持续维护 | 实体或虚拟身体、感知行动交互、仿真研究 | [第01章](chapters/01-orientation/README.md)1.4、1.10节 |
| [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485) | Haotian Liu 等，2023 | 视觉语言模型用于图像与语言交互的案例 | 第01章1.6节 |
| [OpenVLA](https://arxiv.org/abs/2406.09246) | Moo Jin Kim 等，2024 | 将视觉语言信息与机器人动作学习联系起来的案例 | 第01章1.7节 |
| [World Models](https://worldmodels.github.io/) | David Ha、Jürgen Schmidhuber，2018 | 环境表示、预测与行为学习之间的联系 | 第01章1.8节 |

第01章的桌面任务、动作接口、流程图和练习为原创教学示例，不是上述项目的实测输出。来源链接在正文的相关论述附近同时给出。

## 第05章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [函数定义与参数](https://docs.python.org/3/tutorial/controlflow.html)
- [模块](https://docs.python.org/3/tutorial/modules.html)

## 第06章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [文件读写](https://docs.python.org/3/tutorial/inputoutput.html)
- [异常](https://docs.python.org/3/tutorial/errors.html)
- [csv](https://docs.python.org/3/library/csv.html)
- [json](https://docs.python.org/3/library/json.html)

## 第07章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Python类](https://docs.python.org/3/tutorial/classes.html)
- [随机数模块](https://docs.python.org/3/library/random.html)
- [Git初始化](https://git-scm.com/docs/git-init)
- [Git比较](https://git-scm.com/docs/git-diff)
- [Git恢复](https://git-scm.com/docs/git-restore)

## 第08章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Python math函数](https://docs.python.org/3/library/math.html)
- [Matplotlib基础绘图](https://matplotlib.org/stable/tutorials/pyplot.html)

## 第09章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [NumPy入门](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [线性代数教学参考](https://d2l.ai/chapter_preliminaries/linear-algebra.html)

## 第10章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [NumPy solve 文档](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html)
- [NumPy lstsq 文档](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)
- [D2L 线性代数](https://d2l.ai/chapter_preliminaries/linear-algebra.html)

## 第11章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [0,1)$ 的数，因此“小于0.01”约有1%的机会发生。[NumPy Generator 文档](https://numpy.org/doc/stable/reference/random/generator.html)
- [D2L 概率与统计](https://d2l.ai/chapter_preliminaries/probability.html)

## 第12章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [NumPy normal 文档](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.normal.html)
- [NumPy var 文档](https://numpy.org/doc/stable/reference/generated/numpy.var.html)

## 第13章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [D2L 微积分](https://d2l.ai/chapter_preliminaries/calculus.html)

## 第14章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [D2L SGD 说明](https://d2l.ai/chapter_optimization/sgd.html)
- [Adam 原论文](https://arxiv.org/abs/1412.6980)
- [D2L Adam](https://d2l.ai/chapter_optimization/adam.html)

## 第15章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [D2L 线性回归](https://d2l.ai/chapter_linear-regression/linear-regression.html)
- [NumPy loadtxt 文档](https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html)

## 第16章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [NumPy logaddexp 文档](https://numpy.org/doc/stable/reference/generated/numpy.logaddexp.html)
- [D2L softmax回归](https://d2l.ai/chapter_linear-classification/softmax-regression.html)

## 第17章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [scikit-learn 常见错误](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn 概率校准说明](https://scikit-learn.org/stable/modules/calibration.html)
- [SciPy bootstrap 文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)

## 第18章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [He等人的初始化研究](https://arxiv.org/abs/1502.01852)
- [Glorot与Bengio的原始研究](https://proceedings.mlr.press/v9/glorot10a.html)
- [D2L 多层感知机](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)

## 第19章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [D2L 反向传播](https://d2l.ai/chapter_multilayer-perceptrons/backprop.html)
- [karpathy/micrograd](https://github.com/karpathy/micrograd)
- [micrograd/engine.py](https://github.com/karpathy/micrograd/blob/master/micrograd/engine.py)

## 第20章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [PyTorch 自动求导教程](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- [PyTorch 优化教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [PyTorch 保存与加载教程](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html)

## 第21章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [PyTorch Dropout](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Dropout.html)
- [PyTorch BatchNorm1d](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm1d.html)
- [PyTorch AMP 文档](https://docs.pytorch.org/docs/2.14/amp.html)
- [PyTorch 检查点教程](https://docs.pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html)
- [PyTorch 可复现性说明](https://docs.pytorch.org/docs/2.14/notes/randomness.html)

## 第22章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Pillow 教程](https://pillow.readthedocs.io/en/stable/handbook/tutorial.html)
- [D2L 图像卷积](https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html)
- [PyTorch Conv2d](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Conv2d.html)

## 第23章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [ResNet 原论文](https://arxiv.org/abs/1512.03385)
- [PyTorch 迁移学习教程](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [pytorch/vision](https://github.com/pytorch/vision)

## 第24章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [子词BPE的经典论文](https://arxiv.org/abs/1508.07909)
- [PyTorch Embedding](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Embedding.html)
- [Hugging Face Tokenizers 文档](https://huggingface.co/docs/tokenizers/index)

## 第25章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [D2L 语言模型](https://d2l.ai/chapter_recurrent-neural-networks/language-model.html)
- [D2L RNN](https://d2l.ai/chapter_recurrent-neural-networks/rnn.html)

## 第26章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [PyTorch缩放点积注意力接口](https://docs.pytorch.org/docs/2.14/generated/torch.nn.functional.scaled_dot_product_attention.html)

## 第27章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Transformer 原论文](https://arxiv.org/abs/1706.03762)
- [LayerNorm 原论文](https://arxiv.org/abs/1607.06450)
- [PyTorch接口](https://docs.pytorch.org/docs/2.14/generated/torch.nn.LayerNorm.html)
- [PyTorch GELU](https://docs.pytorch.org/docs/2.14/generated/torch.nn.GELU.html)

## 第28章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)

## 第29章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [LoRA论文](https://arxiv.org/abs/2106.09685)

## 第30章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [ViT原论文](https://arxiv.org/abs/2010.11929)
- [PyTorch TransformerEncoderLayer](https://docs.pytorch.org/docs/2.14/generated/torch.nn.TransformerEncoderLayer.html)

## 第31章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [CLIP论文](https://arxiv.org/abs/2103.00020)
- [OpenCLIP](https://github.com/mlfoundations/open_clip)

## 第32章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [LLaVA论文](https://arxiv.org/abs/2304.08485)
- [官方项目](https://github.com/haotian-liu/LLaVA)

## 第33章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Modern Robotics齐次变换课程](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/)

## 第34章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Modern Robotics数值逆运动学](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)
- [奇异位形](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-3-singularities/)

## 第35章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Modern Robotics力/力矩输入的PD与PID控制](https://modernrobotics.northwestern.edu/nu-gm-book-resource/11-4-motion-control-with-torque-or-force-inputs-part-2-of-3/)

## 第36章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [OpenCV相机标定官方文档](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

## 第37章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Gymnasium](https://gymnasium.farama.org/introduction/basic_usage/)
- [Farama-Foundation/Gymnasium](https://github.com/Farama-Foundation/Gymnasium)

## 第38章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [《Reinforcement Learning: An Introduction》第二版](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)

## 第39章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Gymnasium时间上限说明](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/)

## 第40章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [PPO论文](https://arxiv.org/abs/1707.06347)
- [策略优化教学](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html)

## 第41章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [DAgger原论文](https://proceedings.mlr.press/v15/ross11a.html)
- [LeRobot](https://github.com/huggingface/lerobot)

## 第42章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [MIT轨迹优化课程](https://underactuated.mit.edu/trajopt.html)

## 第43章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)

## 第44章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [DDPM论文](https://arxiv.org/abs/2006.11239)
- [作者项目](https://github.com/hojonathanho/diffusion)

## 第45章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)

## 第46章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [ACT论文](https://arxiv.org/abs/2304.13705)
- [作者代码](https://github.com/tonyzhaozh/act)
- [Diffusion Policy项目页](https://diffusion-policy.cs.columbia.edu/)
- [官方仓库](https://github.com/real-stanford/diffusion_policy)

## 第47章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [World Models项目](https://worldmodels.github.io/)

## 第48章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [PyTorch GRU](https://docs.pytorch.org/docs/2.14/generated/torch.nn.GRU.html)
- [PlaNet论文](https://arxiv.org/abs/1811.04551)

## 第50章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Dreamer论文](https://arxiv.org/abs/1912.01603)
- [DreamerV3论文](https://arxiv.org/abs/2301.04104)
- [作者仓库](https://github.com/danijar/dreamerv3)

## 第51章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [World Models](https://worldmodels.github.io/)
- [PlaNet](https://arxiv.org/abs/1811.04551)

## 第52章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [OpenVLA论文](https://arxiv.org/abs/2406.09246)
- [官方仓库](https://github.com/openvla/openvla)

## 第53章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [π₀论文](https://arxiv.org/abs/2410.24164)
- [openpi作者仓库](https://github.com/Physical-Intelligence/openpi)

## 第54章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [Open X-Embodiment项目](https://robotics-transformer-x.github.io/)
- [BridgeData V2代码](https://github.com/rail-berkeley/bridge_data_v2)

## 第55章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [LeRobot官方仓库](https://github.com/huggingface/lerobot)

## 第56章来源索引

核验日期：2026-10-24。用于核对语言、工具行为或本章方法；自编实验结果见该章检查记录。

- [论文v2](https://arxiv.org/abs/2210.02747v2)
- [官方Flow Matching库](https://github.com/facebookresearch/flow_matching)

## 第02章来源索引（补录）

从已完成正文汇集的官方来源；用途与核验范围以章节为准。

- [macOS](https://docs.python.org/3/using/mac.html)
- [Windows](https://docs.python.org/3/using/windows.html)
- [Python venv 官方说明](https://docs.python.org/3/library/venv.html)
- [Python 使用说明](https://docs.python.org/3/using/index.html)
- [环境与包教程](https://docs.python.org/3/tutorial/venv.html)

## 第03章来源索引（补录）

从已完成正文汇集的官方来源；用途与核验范围以章节为准。

- [Python 数值与字符串教程](https://docs.python.org/3/tutorial/introduction.html)

## 第04章来源索引（补录）

从已完成正文汇集的官方来源；用途与核验范围以章节为准。

- [Python 控制流](https://docs.python.org/3/tutorial/controlflow.html)
- [数据结构](https://docs.python.org/3/tutorial/datastructures.html)
