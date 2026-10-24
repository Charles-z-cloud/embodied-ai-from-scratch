# 知识依赖审查

[返回阅读入口](README.md) · [学习路线](roadmap.md) · [各章设计](curriculum.md)

审查版本：v1.0，2026-10-24。下表保留全书知识依赖设计，后文记录各章实际完成情况。自动检查确认重点前置仅指向更早章节；人工编写检查及实现范围见各章validation.md与[全书交付记录](book-validation.md)。

## 顺序规则

1. 主线按 01—58 学习。每章先完成定义与例子，再使用公式、接口或算法。
2. 每章列出的重点前置只能指向编号更小的章节。没有定义的必要知识必须在当前使用前补上，或前移到合适章节。
3. 同章首次出现的知识按小节顺序展开，例如第35章先解释积分是累积，再讲 PID 的积分项。
4. 概览可以介绍用途；正式定义、计算、代码和习题不能依赖尚未讲解的内容。
5. 选学内容不出现在必学练习的隐含要求里。主线项目使用教学实现；官方仓库额外依赖由其选学导读负责。

## 容易漏掉的基础：首次讲解与后续使用

| 必需知识 | 首次系统讲解 | 后续首次重要使用 | 顺序处理 |
| --- | --- | --- | --- |
| 工作目录、路径、环境与包 | [02](curriculum.md#ch-02) | [05](curriculum.md#ch-05)、[06](curriculum.md#ch-06) | 安装和运行命令逐项说明；不要求先会 Linux |
| 类、继承、可调用对象 | [07](curriculum.md#ch-07) | [19](curriculum.md#ch-19)、[20](curriculum.md#ch-20) | 在阅读求导器和 nn.Module 前补齐 |
| 下标、求和、指数、对数、三角函数 | [08](curriculum.md#ch-08) | [09](curriculum.md#ch-09)、[16](curriculum.md#ch-16)、[27](curriculum.md#ch-27) | 不在交叉熵或位置编码中突然引入数学记号 |
| 数组形状、广播、矩阵乘法 | [09](curriculum.md#ch-09) | [15](curriculum.md#ch-15)、[26](curriculum.md#ch-26) | 每个重要矩阵式都标注形状 |
| 秩、低秩乘积、余弦相似度 | [10](curriculum.md#ch-10) | [29](curriculum.md#ch-29)、[31](curriculum.md#ch-31) | LoRA 不依赖选学的完整 SVD 证明 |
| 条件概率、贝叶斯与独立性 | [11](curriculum.md#ch-11) | [16](curriculum.md#ch-16)、[25](curriculum.md#ch-25)、[43](curriculum.md#ch-43) | 先手算小表格，再进入概率模型 |
| Gaussian、Categorical、期望、方差与抽样 | [12](curriculum.md#ch-12) | [17](curriculum.md#ch-17)、[40](curriculum.md#ch-40)、[44](curriculum.md#ch-44) | 密度与概率分开讲；Monte Carlo 用简单采样定义 |
| 链式法则、梯度与 Jacobian | [13](curriculum.md#ch-13) | [14](curriculum.md#ch-14)、[19](curriculum.md#ch-19)、[34](curriculum.md#ch-34) | 先微小数值例子，再矩阵形式 |
| 优化、动量、移动平均与 Adam | [14](curriculum.md#ch-14) | [15](curriculum.md#ch-15)、[21](curriculum.md#ch-21) | 开始训练前已经解释优化器用途与更新 |
| 数据划分与基线 | [15](curriculum.md#ch-15) | 所有训练实验 | 第一份机器学习代码就划分数据，不等到评测专章才做 |
| softmax、负对数似然、交叉熵、离散 KL | [16](curriculum.md#ch-16) | [25](curriculum.md#ch-25)、[26](curriculum.md#ch-26)、[31](curriculum.md#ch-31) | 先解释概率目标，再把它放入注意力或对比学习 |
| 评测、数据泄漏、分组划分 | [17](curriculum.md#ch-17) | [23](curriculum.md#ch-23)、[28](curriculum.md#ch-28)、[41](curriculum.md#ch-41) | 机器人数据后来补充“按轨迹分组”的具体规则 |
| 前向计算、反向传播、PyTorch 训练循环 | [18](curriculum.md#ch-18)—[20](curriculum.md#ch-20) | 所有深度学习项目 | 不在 CNN、GPT 章节中假定读者已熟练训练网络 |
| 图像坐标、通道与图像张量 | [22](curriculum.md#ch-22) | [23](curriculum.md#ch-23)、[30](curriculum.md#ch-30)、[36](curriculum.md#ch-36) | 与机器人空间坐标在第33—36章明确区分 |
| token、嵌入、序列与语言模型目标 | [24](curriculum.md#ch-24)—[25](curriculum.md#ch-25) | [26](curriculum.md#ch-26)—[32](curriculum.md#ch-32) | NLP 的必要部分保留在主线 |
| 残差、归一化、注意力与位置编码 | [23](curriculum.md#ch-23)、[26](curriculum.md#ch-26)—[27](curriculum.md#ch-27) | [28](curriculum.md#ch-28)、[30](curriculum.md#ch-30) | LayerNorm 在 Transformer 中先单独解释再使用 |
| 坐标、运动学与命令类型 | [33](curriculum.md#ch-33)—[36](curriculum.md#ch-36) | [37](curriculum.md#ch-37)、[41](curriculum.md#ch-41)、[52](curriculum.md#ch-52) | 动作的单位、坐标系和频率都有落点 |
| 积分、微分方程与离散时间 | [35](curriculum.md#ch-35) | [45](curriculum.md#ch-45) | 第35章先从累积与 Euler 更新讲起，第45章再正式解释 ODE |
| 环境、回合、终止和截断 | [37](curriculum.md#ch-37) | [38](curriculum.md#ch-38)—[42](curriculum.md#ch-42) | API 先讲含义，第38章再形式化 MDP 与回报 |
| 部分可观测、历史与记忆 | [25](curriculum.md#ch-25)、[38](curriculum.md#ch-38) | [48](curriculum.md#ch-48) | RNN 先教，GRU 在 RSSM 前于第48章补齐 |
| 策略、价值和 actor–critic | [38](curriculum.md#ch-38)—[40](curriculum.md#ch-40) | [50](curriculum.md#ch-50) | Dreamer 不会成为第一次遇到强化学习的章节 |
| 轨迹切分、时间窗口、行为克隆 | [36](curriculum.md#ch-36)、[41](curriculum.md#ch-41) | [46](curriculum.md#ch-46)、[52](curriculum.md#ch-52) | 先讲单步示范学习，再讲动作块与 VLA |
| 已知模型 rollout 与 MPC | [42](curriculum.md#ch-42) | [49](curriculum.md#ch-49) | 学习模型规划只是替换预测器，规划原理已先教过 |
| 连续 KL、Jensen、ELBO、重参数化 | [43](curriculum.md#ch-43) | [46](curriculum.md#ch-46)、[48](curriculum.md#ch-48) | 本章自含必要数学，ACT 和 RSSM 不再突然使用 VAE |
| 扩散、流匹配、动作 chunk | [44](curriculum.md#ch-44)—[46](curriculum.md#ch-46) | [51](curriculum.md#ch-51)、[53](curriculum.md#ch-53) | 从二维数据开始，之后才迁移到动作和视频 |
| lambda return、离散梯度近似 | [50](curriculum.md#ch-50) | 同章 Dreamer 方法解释 | 在公式中使用前补定义和局限，完整复杂实现为选学 |
| 多机器人 schema、跨任务评测 | [54](curriculum.md#ch-54) | [55](curriculum.md#ch-55)—[57](curriculum.md#ch-57) | 第36、41章已经教会单机器人数据；此处才扩展到多来源 |

## 设计中已经处理的主要跳跃风险

- **直接从 Python 跳到 PyTorch**：加入函数、类、数组、训练目标、前向计算和反向传播，PyTorch 排在第20章。
- **只教 Transformer 名称而缺少 NLP**：第24—25章先教 token、嵌入、条件概率目标和生成，之后再学注意力。
- **VLA 没有机器人动作基础**：坐标、运动学、控制、传感器、动作归一化和时间同步均在 VLA 前安排。
- **扩散策略缺少生成模型基础**：先学 VAE、扩散和流匹配，再学 ACT、Diffusion Policy 和连续动作 VLA。
- **Dreamer 缺少 RL、记忆或概率推断**：先安排 actor–critic、RNN、潜变量和 RSSM。JAX 不偷偷进入主线代码。
- **把第54章数据集知识当作第41章的前置**：单条轨迹、观测动作配对、切分与归一化在第36、41章先教；第54章处理跨来源数据。
- **经典仓库带来未教过的工程依赖**：完整仓库运行设为选学，主线先实现最小机制；选学仍须解释新增依赖。
- **让所有模型成为同一系统的必需组件**：第57章比较不同方案并做消融，不强制 VLA 一定包含世界模型。

## 编写与后续修订检查规则

- 扫描新术语、新数学符号、新库接口，登记它们的首次定义位置。
- 对每个公式确认所有符号已定义，形状、单位和条件已说明。
- 逐段核对代码所需的语法与接口；首次出现的库功能就地解释。
- 对每道题写出所需知识，保证答案不用尚未讲过的方法。
- 对每个实验核对数据和资源条件，并记录实际运行状态。
- 更新前置知识、前后章导航与项目入口。

这些规则指导编写和后续修订；自动导航检查不能证明所有概念都没有教学跳跃。发现不理解的前置时，按各章先修说明回溯，并记录需要补充的解释。

## 第01章正文检查记录

检查对象：[正文](chapters/01-orientation/README.md)、[练习](chapters/01-orientation/exercises.md)、[答案](chapters/01-orientation/solutions.md)。

| 知识 | 先解释的位置 | 后续使用 |
| --- | --- | --- |
| 任务目标与成功条件 | 1.2节 | 反馈判断、综合比较、练习1与8 |
| 观测、感知、决策、动作、反馈 | 1.2节 | 1.3节闭环及后文各模型用途 |
| 闭环、开环与观测不完整 | 1.3节 | 具身任务、部署例子、练习2 |
| 环境、智能体、身体与具身智能 | 1.4节 | 真实与虚拟环境比较 |
| 模型、输入、输出、训练与推理 | 1.5节 | VLM、VLA、世界模型及练习9 |
| 模态与 VLM | 1.6节 | VLA、综合比较和练习3 |
| VLA、动作序列、接口与控制 | 1.7节 | 指令与结果比较、练习4 |
| 世界模型、候选动作与规划 | 1.8节 | 三种方案、练习5—6 |
| 仿真 | 1.10节 | 真实/虚拟任务比较、练习7 |

练习1—9都有对应答案，且只依赖第01章已经讲过的内容。数学推导、网络结构和具体训练算法没有被作为本章过关要求。1.11节中的后续学科名称提供用途解释，并明确属于路线预告。

本章使用两张自绘 Mermaid 流程图，并为每张提供文字解释；无程序实验，因此没有“未运行代码却声称验证成功”的情况。正文中的输入输出、动作与预测均标为教学示例。第01章下一章入口现已连接到第02章正文。

## 第05章完成记录

[正文与先修说明](chapters/05-python-functions/README.md) · [实际检查记录](chapters/05-python-functions/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第06章完成记录

[正文与先修说明](chapters/06-files-and-debugging/README.md) · [实际检查记录](chapters/06-files-and-debugging/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第07章完成记录

[正文与先修说明](chapters/07-classes-git-and-reproducibility/README.md) · [实际检查记录](chapters/07-classes-git-and-reproducibility/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第08章完成记录

[正文与先修说明](chapters/08-math-language-and-functions/README.md) · [实际检查记录](chapters/08-math-language-and-functions/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第09章完成记录

[正文与先修说明](chapters/09-numpy-vectors-and-arrays/README.md) · [实际检查记录](chapters/09-numpy-vectors-and-arrays/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第10章完成记录

[正文与先修说明](chapters/10-linear-algebra-and-geometry/README.md) · [实际检查记录](chapters/10-linear-algebra-and-geometry/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第11章完成记录

[正文与先修说明](chapters/11-probability/README.md) · [实际检查记录](chapters/11-probability/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第12章完成记录

[正文与先修说明](chapters/12-distributions-and-statistics/README.md) · [实际检查记录](chapters/12-distributions-and-statistics/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第13章完成记录

[正文与先修说明](chapters/13-calculus-and-gradients/README.md) · [实际检查记录](chapters/13-calculus-and-gradients/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第14章完成记录

[正文与先修说明](chapters/14-optimization/README.md) · [实际检查记录](chapters/14-optimization/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第15章完成记录

[正文与先修说明](chapters/15-regression-workflow/README.md) · [实际检查记录](chapters/15-regression-workflow/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第16章完成记录

[正文与先修说明](chapters/16-classification-and-information/README.md) · [实际检查记录](chapters/16-classification-and-information/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第17章完成记录

[正文与先修说明](chapters/17-evaluation-and-generalization/README.md) · [实际检查记录](chapters/17-evaluation-and-generalization/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第18章完成记录

[正文与先修说明](chapters/18-neural-network-forward/README.md) · [实际检查记录](chapters/18-neural-network-forward/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第19章完成记录

[正文与先修说明](chapters/19-backpropagation/README.md) · [实际检查记录](chapters/19-backpropagation/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第20章完成记录

[正文与先修说明](chapters/20-pytorch-training/README.md) · [实际检查记录](chapters/20-pytorch-training/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第21章完成记录

[正文与先修说明](chapters/21-training-engineering/README.md) · [实际检查记录](chapters/21-training-engineering/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第22章完成记录

[正文与先修说明](chapters/22-images-and-convolution/README.md) · [实际检查记录](chapters/22-images-and-convolution/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第23章完成记录

[正文与先修说明](chapters/23-cnn-and-visual-representations/README.md) · [实际检查记录](chapters/23-cnn-and-visual-representations/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第24章完成记录

[正文与先修说明](chapters/24-text-tokenization-and-embeddings/README.md) · [实际检查记录](chapters/24-text-tokenization-and-embeddings/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第25章完成记录

[正文与先修说明](chapters/25-sequence-and-language-modeling/README.md) · [实际检查记录](chapters/25-sequence-and-language-modeling/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第26章完成记录

[正文与先修说明](chapters/26-attention/README.md) · [实际检查记录](chapters/26-attention/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第27章完成记录

[正文与先修说明](chapters/27-transformer/README.md) · [实际检查记录](chapters/27-transformer/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第28章完成记录

[正文与先修说明](chapters/28-tiny-language-model/README.md) · [实际检查记录](chapters/28-tiny-language-model/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第29章完成记录

[正文与先修说明](chapters/29-adaptation-and-llm-evaluation/README.md) · [实际检查记录](chapters/29-adaptation-and-llm-evaluation/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第30章完成记录

[正文与先修说明](chapters/30-vision-transformer/README.md) · [实际检查记录](chapters/30-vision-transformer/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第31章完成记录

[正文与先修说明](chapters/31-multimodal-alignment/README.md) · [实际检查记录](chapters/31-multimodal-alignment/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第32章完成记录

[正文与先修说明](chapters/32-vision-language-models/README.md) · [实际检查记录](chapters/32-vision-language-models/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第33章完成记录

[正文与先修说明](chapters/33-robot-frames-and-pose/README.md) · [实际检查记录](chapters/33-robot-frames-and-pose/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第34章完成记录

[正文与先修说明](chapters/34-robot-kinematics/README.md) · [实际检查记录](chapters/34-robot-kinematics/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第35章完成记录

[正文与先修说明](chapters/35-dynamics-and-feedback-control/README.md) · [实际检查记录](chapters/35-dynamics-and-feedback-control/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第36章完成记录

[正文与先修说明](chapters/36-sensors-and-robot-data/README.md) · [实际检查记录](chapters/36-sensors-and-robot-data/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第37章完成记录

[正文与先修说明](chapters/37-simulation-and-environment-api/README.md) · [实际检查记录](chapters/37-simulation-and-environment-api/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第38章完成记录

[正文与先修说明](chapters/38-sequential-decision-making/README.md) · [实际检查记录](chapters/38-sequential-decision-making/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第39章完成记录

[正文与先修说明](chapters/39-value-learning/README.md) · [实际检查记录](chapters/39-value-learning/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第40章完成记录

[正文与先修说明](chapters/40-policy-gradients/README.md) · [实际检查记录](chapters/40-policy-gradients/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第41章完成记录

[正文与先修说明](chapters/41-imitation-learning/README.md) · [实际检查记录](chapters/41-imitation-learning/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第42章完成记录

[正文与先修说明](chapters/42-planning-and-mpc/README.md) · [实际检查记录](chapters/42-planning-and-mpc/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第43章完成记录

[正文与先修说明](chapters/43-latent-generative-models/README.md) · [实际检查记录](chapters/43-latent-generative-models/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第44章完成记录

[正文与先修说明](chapters/44-diffusion-models/README.md) · [实际检查记录](chapters/44-diffusion-models/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第45章完成记录

[正文与先修说明](chapters/45-flow-matching/README.md) · [实际检查记录](chapters/45-flow-matching/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第46章完成记录

[正文与先修说明](chapters/46-action-chunks-and-generative-policies/README.md) · [实际检查记录](chapters/46-action-chunks-and-generative-policies/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第47章完成记录

[正文与先修说明](chapters/47-learned-dynamics/README.md) · [实际检查记录](chapters/47-learned-dynamics/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第48章完成记录

[正文与先修说明](chapters/48-latent-world-models/README.md) · [实际检查记录](chapters/48-latent-world-models/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第49章完成记录

[正文与先修说明](chapters/49-planning-with-world-models/README.md) · [实际检查记录](chapters/49-planning-with-world-models/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第50章完成记录

[正文与先修说明](chapters/50-imagined-policy-learning/README.md) · [实际检查记录](chapters/50-imagined-policy-learning/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第51章完成记录

[正文与先修说明](chapters/51-video-and-world-model-boundaries/README.md) · [实际检查记录](chapters/51-video-and-world-model-boundaries/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第52章完成记录

[正文与先修说明](chapters/52-vla-discrete-actions/README.md) · [实际检查记录](chapters/52-vla-discrete-actions/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第53章完成记录

[正文与先修说明](chapters/53-vla-continuous-actions/README.md) · [实际检查记录](chapters/53-vla-continuous-actions/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第54章完成记录

[正文与先修说明](chapters/54-robot-datasets-and-benchmarks/README.md) · [实际检查记录](chapters/54-robot-datasets-and-benchmarks/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第55章完成记录

[正文与先修说明](chapters/55-closed-loop-deployment/README.md) · [实际检查记录](chapters/55-closed-loop-deployment/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第56章完成记录

[正文与先修说明](chapters/56-reading-and-reproducing-papers/README.md) · [实际检查记录](chapters/56-reading-and-reproducing-papers/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第57章完成记录

[正文与先修说明](chapters/57-capstone/README.md) · [实际检查记录](chapters/57-capstone/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第58章完成记录

[正文与先修说明](chapters/58-synthesis-and-next-steps/README.md) · [实际检查记录](chapters/58-synthesis-and-next-steps/validation.md)。本章按设计顺序完成，新增术语、公式和示例在使用前解释；运行范围与限制在检查记录中列出。

## 第02章完成记录

[正文](chapters/02-computer-and-environment/README.md)与[检查记录](chapters/02-computer-and-environment/validation.md)已完成；本段补齐早期索引，不代表重新运行实验。

## 第03章完成记录

[正文](chapters/03-python-values/README.md)与[检查记录](chapters/03-python-values/validation.md)已完成；本段补齐早期索引，不代表重新运行实验。

## 第04章完成记录

[正文](chapters/04-python-collections/README.md)与[检查记录](chapters/04-python-collections/validation.md)已完成；本段补齐早期索引，不代表重新运行实验。
