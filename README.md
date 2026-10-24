# 从零开始学习具身智能、VLM、世界模型与 VLA

一本以中文编写、按知识依赖逐章推进的入门教材。请按01—58顺序学习，每章先读正文，再做练习，最后对照答案。

**当前版本：完整初稿 v1.0（2026-10-24），58/58章正文已完成。**

## 从哪里开始

从[第 01 章正文：从一个桌面任务认识整本书](chapters/01-orientation/README.md)开始阅读，接着完成[本章练习](chapters/01-orientation/exercises.md)，再对照[参考答案](chapters/01-orientation/solutions.md)。也可以先浏览[学习路线](roadmap.md)了解全书安排。

第01章用桌面任务解释观察与反馈、具身智能、VLM、VLA、世界模型及仿真的用途，配有两张流程图、9道练习与自测。它是概念入门章，无需编程或安装环境。

第01—58章均有正文、练习、参考答案与检查记录。自编小实验的结果和局限已记录；完整外部大模型、原论文基准和真实硬件部署不属于已完成的复现范围。详见[全书交付检查](book-validation.md)。

## 为谁编写

默认读者会使用电脑和进行日常算术，但没有系统学过编程、微积分、机器学习或机器人。分数、比例、函数和代数表达会在需要时补齐。技术英文会给出中文解释。

默认从普通电脑和二维仿真开始，不要求购买机器人或具备独立显卡。较大的模型训练和完整论文复现属于明确标注的进阶实验。资源需求在各项目实际选型和验证时重新核对。

**遇到新术语时，请先用12岁小朋友都能听懂的语言解释，再给出准确的定义。**

## 文件入口

| 文件 | 用途 |
| --- | --- |
| [roadmap.md](roadmap.md) | 推荐学习顺序、阶段标准、NLP 范围和选学分支 |
| [curriculum.md](curriculum.md) | 58 章细分目录、前置链接、练习与过关标准 |
| [project-plan.md](project-plan.md) | 每个阶段的实践、经典 GitHub 项目与资源边界 |
| [dependency-audit.md](dependency-audit.md) | 容易跳过的知识、首次讲解位置和后续使用位置 |
| [repository-plan.md](repository-plan.md) | 多文件章节结构、命名、导航和发布安排 |
| [writing-guide.md](writing-guide.md) | 正文教学、公式、代码、来源和完成标准 |
| [references.md](references.md) | 已核验的官方资料与仓库入口 |
| [environment.md](environment.md) | 实际运行环境、依赖版本与使用方式 |
| [experiments.md](experiments.md) | 按章排列的示例入口、运行顺序与权重依赖 |
| [learning-checklist.md](learning-checklist.md) | 可勾选的逐章学习记录 |
| [book-validation.md](book-validation.md) | 全书检查与实际实现范围 |
| [publication.md](publication.md) | 发布包内容、重建方式和GitHub状态 |

## 按学习顺序浏览章节

下列58个入口均指向已完成正文。编号就是推荐阅读顺序，不要因为已经听说某个模型名而跳过它的先修章节。

### A．从零开始使用电脑和 Python

- [01 从一个桌面任务认识整本书](chapters/01-orientation/README.md)（已完成）
- [02 电脑、文件、命令行与第一个程序](chapters/02-computer-and-environment/README.md)（已完成）
- [03 Python 的数值、变量与表达式](chapters/03-python-values/README.md)（已完成）
- [04 列表、字典、条件与循环](chapters/04-python-collections/README.md)（已完成）
- [05 函数、模块与拆分程序](chapters/05-python-functions/README.md)（已完成）
- [06 文件、数据与排查错误](chapters/06-files-and-debugging/README.md)（已完成）
- [07 对象、Git 与可重复的实验记录](chapters/07-classes-git-and-reproducibility/README.md)（已完成）

### B．数学与数值计算

- [08 数学表达式、函数与曲线](chapters/08-math-language-and-functions/README.md)（已完成）
- [09 向量、矩阵、张量与 NumPy](chapters/09-numpy-vectors-and-arrays/README.md)（已完成）
- [10 线性代数与几何直觉](chapters/10-linear-algebra-and-geometry/README.md)（已完成）
- [11 概率、条件概率与贝叶斯公式](chapters/11-probability/README.md)（已完成）
- [12 随机变量、分布、期望与抽样](chapters/12-distributions-and-statistics/README.md)（已完成）
- [13 导数、偏导数、链式法则与梯度](chapters/13-calculus-and-gradients/README.md)（已完成）
- [14 从误差到梯度下降](chapters/14-optimization/README.md)（已完成）

### C．机器学习与深度学习

- [15 第一个机器学习问题：线性回归](chapters/15-regression-workflow/README.md)（已完成）
- [16 分类、似然与交叉熵](chapters/16-classification-and-information/README.md)（已完成）
- [17 怎样判断模型真的学会了](chapters/17-evaluation-and-generalization/README.md)（已完成）
- [18 神经网络如何做一次预测](chapters/18-neural-network-forward/README.md)（已完成）
- [19 反向传播与自动求导](chapters/19-backpropagation/README.md)（已完成）
- [20 使用 PyTorch 训练神经网络](chapters/20-pytorch-training/README.md)（已完成）
- [21 让训练过程可排查、可复现](chapters/21-training-engineering/README.md)（已完成）

### D．视觉、NLP 与 Transformer

- [22 图像、像素与卷积](chapters/22-images-and-convolution/README.md)（已完成）
- [23 卷积网络、视觉特征与迁移学习](chapters/23-cnn-and-visual-representations/README.md)（已完成）
- [24 NLP 入门：文字怎样变成数字](chapters/24-text-tokenization-and-embeddings/README.md)（已完成）
- [25 序列、记忆与下一个词元预测](chapters/25-sequence-and-language-modeling/README.md)（已完成）
- [26 注意力机制：从相关性到信息聚合](chapters/26-attention/README.md)（已完成）
- [27 从注意力搭建 Transformer](chapters/27-transformer/README.md)（已完成）
- [28 训练自己的小型语言模型](chapters/28-tiny-language-model/README.md)（已完成）
- [29 预训练、微调、指令与评测](chapters/29-adaptation-and-llm-evaluation/README.md)（已完成）
- [30 把图像交给 Transformer](chapters/30-vision-transformer/README.md)（已完成）

### E．多模态与 VLM

- [31 图文对齐与 CLIP 思路](chapters/31-multimodal-alignment/README.md)（已完成）
- [32 VLM：看图、读指令与生成回答](chapters/32-vision-language-models/README.md)（已完成）

### F．机器人、控制与仿真

- [33 机器人在哪里：坐标系与位姿](chapters/33-robot-frames-and-pose/README.md)（已完成）
- [34 机器人怎样到达目标：运动学](chapters/34-robot-kinematics/README.md)（已完成）
- [35 运动、时间与反馈控制](chapters/35-dynamics-and-feedback-control/README.md)（已完成）
- [36 相机、传感器与动作数据](chapters/36-sensors-and-robot-data/README.md)（已完成）
- [37 搭建可交互的仿真任务](chapters/37-simulation-and-environment-api/README.md)（已完成）

### G．决策、强化学习、模仿与规划

- [38 状态、观测、动作、奖励与策略](chapters/38-sequential-decision-making/README.md)（已完成）
- [39 价值函数与第一种强化学习算法](chapters/39-value-learning/README.md)（已完成）
- [40 策略梯度与 Actor–Critic](chapters/40-policy-gradients/README.md)（已完成）
- [41 从示范学习动作](chapters/41-imitation-learning/README.md)（已完成）
- [42 先想几步再行动：规划与 MPC](chapters/42-planning-and-mpc/README.md)（已完成）

### H．生成模型与动作序列

- [43 潜变量、自动编码器与 VAE](chapters/43-latent-generative-models/README.md)（已完成）
- [44 扩散模型：从噪声逐步生成](chapters/44-diffusion-models/README.md)（已完成）
- [45 流匹配与连续生成](chapters/45-flow-matching/README.md)（已完成）
- [46 动作序列、ACT 与生成式策略](chapters/46-action-chunks-and-generative-policies/README.md)（已完成）

### I．世界模型

- [47 世界模型起步：学会预测下一步](chapters/47-learned-dynamics/README.md)（已完成）
- [48 潜在世界模型与记忆](chapters/48-latent-world-models/README.md)（已完成）
- [49 用学到的世界模型规划](chapters/49-planning-with-world-models/README.md)（已完成）
- [50 在想象中学习策略：Dreamer 思路](chapters/50-imagined-policy-learning/README.md)（已完成）
- [51 视频生成与世界模型的边界](chapters/51-video-and-world-model-boundaries/README.md)（已完成）

### J．VLA、机器人数据与部署

- [52 VLA：把视觉和语言连接到动作](chapters/52-vla-discrete-actions/README.md)（已完成）
- [53 连续动作 VLA 与动作生成模块](chapters/53-vla-continuous-actions/README.md)（已完成）
- [54 机器人数据、跨本体与评测](chapters/54-robot-datasets-and-benchmarks/README.md)（已完成）
- [55 从模型输出到稳定闭环](chapters/55-closed-loop-deployment/README.md)（已完成）

### K．论文、综合项目与进阶方向

- [56 独立读论文与做可解释的实验](chapters/56-reading-and-reproducing-papers/README.md)（已完成）
- [57 综合项目：听懂指令的桌面智能体](chapters/57-capstone/README.md)（已完成）
- [58 把知识连起来与选择下一步](chapters/58-synthesis-and-next-steps/README.md)（已完成）

## 本书怎样帮助你学会

每章包含直观解释、准确概念、例题、必要公式、示例或实验、自测和答案。以桌面任务贯穿各阶段：先处理数字，再学识别图像和理解短指令，最后学习决策与闭环控制。第01章的搬运方块是概念案例；实际毕业项目简化为按红蓝指令移动到目标，不模拟抓取、接触或搬运物理。各阶段的具体任务与假设均在对应章节说明。

每章写明你应该达到“理解”“手算或推导”“独立实现”还是“使用工具”的哪种程度。通过本章自测后再进入下一章；看懂答案不等于已经能独立完成。

## GitHub 阅读与下载

教材仓库：[Charles-z-cloud/embodied-ai-from-scratch](https://github.com/Charles-z-cloud/embodied-ai-from-scratch)（私有，需要登录有权限的GitHub账号）。按上面的编号目录阅读；下载后可以用Markdown阅读器离线学习。

发布内容与可重建实验产物的区别见[发布说明](publication.md)。
