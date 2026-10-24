# 实验入口与实际运行顺序

[全书目录](README.md) · [环境说明](environment.md) · [交付检查](book-validation.md)

先按正文学习，再执行代码。下表是源码导航，不是让初学者跳过正文批量训练。运行命令、输入方式、预期结果和限制见对应正文与检查记录；模型辅助模块无需单独执行。

## 必须先生成的文件

| 后续实验 | 必须先完成的生成步骤 |
|---|---|
| 第15章训练和绘图 | 同章依次generate_data.py → train.py → plot_results.py |
| 第29章微调 | 第28章train_language.py生成模型与语料划分 |
| 第42章规划比较 | 第41章bc.py生成BC权重 |
| 第49、50章 | 第47章dynamics.py生成动力学权重 |
| 第53章 | 第52章train_vla.py生成冻结骨干 |
| 第54、56章 | 第52→53章训练和评测生成权重及report.json |
| 第55章 | 第52→53章生成骨干与连续动作头 |
| 第57章 | 第41、47、52、53章生成四个检查点 |

其他跨章导入也要保留完整目录，例如第32章导入第27、31章代码，第44—45章复用前章数据函数；这些导入不要求先训练前章模型。第03章interactive.py需要终端输入；第04章有故意提供坏输入的排错练习；第05章以main.py调用motion.py。

## 按章查找

| 章 | 正文与运行说明 | 示例源码 | 检查记录 |
|---|---|---|---|
| 01 | [从一个桌面任务认识整本书](chapters/01-orientation/README.md) | 概念阅读与自测 | [记录](chapters/01-orientation/validation.md) |
| 02 | [电脑、文件、命令行与第一个程序](chapters/02-computer-and-environment/README.md) | [hello.py](chapters/02-computer-and-environment/examples/hello.py) | [记录](chapters/02-computer-and-environment/validation.md) |
| 03 | [Python 的数值、变量与表达式](chapters/03-python-values/README.md) | [interactive.py](chapters/03-python-values/examples/interactive.py)、[motion.py](chapters/03-python-values/examples/motion.py) | [记录](chapters/03-python-values/validation.md) |
| 04 | [列表、字典、条件与循环](chapters/04-python-collections/README.md) | [records.py](chapters/04-python-collections/examples/records.py)、[valid_time.py](chapters/04-python-collections/examples/valid_time.py) | [记录](chapters/04-python-collections/validation.md) |
| 05 | [函数、模块与拆分程序](chapters/05-python-functions/README.md) | [main.py](chapters/05-python-functions/examples/main.py)、[motion.py](chapters/05-python-functions/examples/motion.py) | [记录](chapters/05-python-functions/validation.md) |
| 06 | [文件、数据与排查错误](chapters/06-files-and-debugging/README.md) | [clean_records.py](chapters/06-files-and-debugging/examples/clean_records.py) | [记录](chapters/06-files-and-debugging/validation.md) |
| 07 | [对象、Git 与可重复的实验记录](chapters/07-classes-git-and-reproducibility/README.md) | [record_book.py](chapters/07-classes-git-and-reproducibility/examples/record_book.py) | [记录](chapters/07-classes-git-and-reproducibility/validation.md) |
| 08 | [数学表达式、函数与曲线](chapters/08-math-language-and-functions/README.md) | [formulas.py](chapters/08-math-language-and-functions/examples/formulas.py)、[plot_functions.py](chapters/08-math-language-and-functions/examples/plot_functions.py) | [记录](chapters/08-math-language-and-functions/validation.md) |
| 09 | [向量、矩阵、张量与 NumPy](chapters/09-numpy-vectors-and-arrays/README.md) | [arrays.py](chapters/09-numpy-vectors-and-arrays/examples/arrays.py) | [记录](chapters/09-numpy-vectors-and-arrays/validation.md) |
| 10 | [线性代数与几何直觉](chapters/10-linear-algebra-and-geometry/README.md) | [geometry.py](chapters/10-linear-algebra-and-geometry/examples/geometry.py) | [记录](chapters/10-linear-algebra-and-geometry/validation.md) |
| 11 | [概率、条件概率与贝叶斯公式](chapters/11-probability/README.md) | [sensor_probability.py](chapters/11-probability/examples/sensor_probability.py) | [记录](chapters/11-probability/validation.md) |
| 12 | [随机变量、分布、期望与抽样](chapters/12-distributions-and-statistics/README.md) | [plot_distributions.py](chapters/12-distributions-and-statistics/examples/plot_distributions.py)、[statistics_demo.py](chapters/12-distributions-and-statistics/examples/statistics_demo.py) | [记录](chapters/12-distributions-and-statistics/validation.md) |
| 13 | [导数、偏导数、链式法则与梯度](chapters/13-calculus-and-gradients/README.md) | [gradients.py](chapters/13-calculus-and-gradients/examples/gradients.py)、[plot_gradient.py](chapters/13-calculus-and-gradients/examples/plot_gradient.py) | [记录](chapters/13-calculus-and-gradients/validation.md) |
| 14 | [从误差到梯度下降](chapters/14-optimization/README.md) | [optimize.py](chapters/14-optimization/examples/optimize.py) | [记录](chapters/14-optimization/validation.md) |
| 15 | [第一个机器学习问题：线性回归](chapters/15-regression-workflow/README.md) | [generate_data.py](chapters/15-regression-workflow/examples/generate_data.py)、[plot_results.py](chapters/15-regression-workflow/examples/plot_results.py)、[train.py](chapters/15-regression-workflow/examples/train.py) | [记录](chapters/15-regression-workflow/validation.md) |
| 16 | [分类、似然与交叉熵](chapters/16-classification-and-information/README.md) | [color_classifier.py](chapters/16-classification-and-information/examples/color_classifier.py) | [记录](chapters/16-classification-and-information/validation.md) |
| 17 | [怎样判断模型真的学会了](chapters/17-evaluation-and-generalization/README.md) | [evaluation.py](chapters/17-evaluation-and-generalization/examples/evaluation.py) | [记录](chapters/17-evaluation-and-generalization/validation.md) |
| 18 | [神经网络如何做一次预测](chapters/18-neural-network-forward/README.md) | [forward.py](chapters/18-neural-network-forward/examples/forward.py) | [记录](chapters/18-neural-network-forward/validation.md) |
| 19 | [反向传播与自动求导](chapters/19-backpropagation/README.md) | [check_matrix_backward.py](chapters/19-backpropagation/examples/check_matrix_backward.py)、[scalar_autodiff.py](chapters/19-backpropagation/examples/scalar_autodiff.py) | [记录](chapters/19-backpropagation/validation.md) |
| 20 | [使用 PyTorch 训练神经网络](chapters/20-pytorch-training/README.md) | [tensor_and_forward.py](chapters/20-pytorch-training/examples/tensor_and_forward.py)、[train_xor.py](chapters/20-pytorch-training/examples/train_xor.py) | [记录](chapters/20-pytorch-training/validation.md) |
| 21 | [让训练过程可排查、可复现](chapters/21-training-engineering/README.md) | [accumulation.py](chapters/21-training-engineering/examples/accumulation.py)、[debug_training.py](chapters/21-training-engineering/examples/debug_training.py)、[resume_training.py](chapters/21-training-engineering/examples/resume_training.py) | [记录](chapters/21-training-engineering/validation.md) |
| 22 | [图像、像素与卷积](chapters/22-images-and-convolution/README.md) | [image_convolution.py](chapters/22-images-and-convolution/examples/image_convolution.py) | [记录](chapters/22-images-and-convolution/validation.md) |
| 23 | [卷积网络、视觉特征与迁移学习](chapters/23-cnn-and-visual-representations/README.md) | [train_vision.py](chapters/23-cnn-and-visual-representations/examples/train_vision.py) | [记录](chapters/23-cnn-and-visual-representations/validation.md) |
| 24 | [NLP 入门：文字怎样变成数字](chapters/24-text-tokenization-and-embeddings/README.md) | [simple_bpe.py](chapters/24-text-tokenization-and-embeddings/examples/simple_bpe.py)、[text_basics.py](chapters/24-text-tokenization-and-embeddings/examples/text_basics.py) | [记录](chapters/24-text-tokenization-and-embeddings/validation.md) |
| 25 | [序列、记忆与下一个词元预测](chapters/25-sequence-and-language-modeling/README.md) | [bigram.py](chapters/25-sequence-and-language-modeling/examples/bigram.py)、[rnn_forward.py](chapters/25-sequence-and-language-modeling/examples/rnn_forward.py) | [记录](chapters/25-sequence-and-language-modeling/validation.md) |
| 26 | [注意力机制：从相关性到信息聚合](chapters/26-attention/README.md) | [attention.py](chapters/26-attention/examples/attention.py)、[multihead_shapes.py](chapters/26-attention/examples/multihead_shapes.py) | [记录](chapters/26-attention/validation.md) |
| 27 | [从注意力搭建 Transformer](chapters/27-transformer/README.md) | [transformer_block.py](chapters/27-transformer/examples/transformer_block.py) | [记录](chapters/27-transformer/validation.md) |
| 28 | [训练自己的小型语言模型](chapters/28-tiny-language-model/README.md) | [model_parts.py](chapters/28-tiny-language-model/examples/model_parts.py)、[train_language.py](chapters/28-tiny-language-model/examples/train_language.py) | [记录](chapters/28-tiny-language-model/validation.md) |
| 29 | [预训练、微调、指令与评测](chapters/29-adaptation-and-llm-evaluation/README.md) | [finetune.py](chapters/29-adaptation-and-llm-evaluation/examples/finetune.py) | [记录](chapters/29-adaptation-and-llm-evaluation/validation.md) |
| 30 | [把图像交给 Transformer](chapters/30-vision-transformer/README.md) | [compare_vision.py](chapters/30-vision-transformer/examples/compare_vision.py) | [记录](chapters/30-vision-transformer/validation.md) |
| 31 | [图文对齐与 CLIP 思路](chapters/31-multimodal-alignment/README.md) | [alignment.py](chapters/31-multimodal-alignment/examples/alignment.py) | [记录](chapters/31-multimodal-alignment/validation.md) |
| 32 | [VLM：看图、读指令与生成回答](chapters/32-vision-language-models/README.md) | [visual_qa.py](chapters/32-vision-language-models/examples/visual_qa.py) | [记录](chapters/32-vision-language-models/validation.md) |
| 33 | [机器人在哪里：坐标系与位姿](chapters/33-robot-frames-and-pose/README.md) | [frames.py](chapters/33-robot-frames-and-pose/examples/frames.py) | [记录](chapters/33-robot-frames-and-pose/validation.md) |
| 34 | [机器人怎样到达目标：运动学](chapters/34-robot-kinematics/README.md) | [kinematics.py](chapters/34-robot-kinematics/examples/kinematics.py) | [记录](chapters/34-robot-kinematics/validation.md) |
| 35 | [运动、时间与反馈控制](chapters/35-dynamics-and-feedback-control/README.md) | [control.py](chapters/35-dynamics-and-feedback-control/examples/control.py) | [记录](chapters/35-dynamics-and-feedback-control/validation.md) |
| 36 | [相机、传感器与动作数据](chapters/36-sensors-and-robot-data/README.md) | [sensors.py](chapters/36-sensors-and-robot-data/examples/sensors.py) | [记录](chapters/36-sensors-and-robot-data/validation.md) |
| 37 | [搭建可交互的仿真任务](chapters/37-simulation-and-environment-api/README.md) | [run_environment.py](chapters/37-simulation-and-environment-api/examples/run_environment.py)、[tabletop_env.py](chapters/37-simulation-and-environment-api/examples/tabletop_env.py) | [记录](chapters/37-simulation-and-environment-api/validation.md) |
| 38 | [状态、观测、动作、奖励与策略](chapters/38-sequential-decision-making/README.md) | [decision.py](chapters/38-sequential-decision-making/examples/decision.py) | [记录](chapters/38-sequential-decision-making/validation.md) |
| 39 | [价值函数与第一种强化学习算法](chapters/39-value-learning/README.md) | [value_learning.py](chapters/39-value-learning/examples/value_learning.py) | [记录](chapters/39-value-learning/validation.md) |
| 40 | [策略梯度与 Actor–Critic](chapters/40-policy-gradients/README.md) | [reinforce.py](chapters/40-policy-gradients/examples/reinforce.py) | [记录](chapters/40-policy-gradients/validation.md) |
| 41 | [从示范学习动作](chapters/41-imitation-learning/README.md) | [bc.py](chapters/41-imitation-learning/examples/bc.py) | [记录](chapters/41-imitation-learning/validation.md) |
| 42 | [先想几步再行动：规划与 MPC](chapters/42-planning-and-mpc/README.md) | [mpc.py](chapters/42-planning-and-mpc/examples/mpc.py) | [记录](chapters/42-planning-and-mpc/validation.md) |
| 43 | [潜变量、自动编码器与 VAE](chapters/43-latent-generative-models/README.md) | [vae.py](chapters/43-latent-generative-models/examples/vae.py) | [记录](chapters/43-latent-generative-models/validation.md) |
| 44 | [扩散模型：从噪声逐步生成](chapters/44-diffusion-models/README.md) | [diffusion.py](chapters/44-diffusion-models/examples/diffusion.py) | [记录](chapters/44-diffusion-models/validation.md) |
| 45 | [流匹配与连续生成](chapters/45-flow-matching/README.md) | [flow.py](chapters/45-flow-matching/examples/flow.py) | [记录](chapters/45-flow-matching/validation.md) |
| 46 | [动作序列、ACT 与生成式策略](chapters/46-action-chunks-and-generative-policies/README.md) | [chunks.py](chapters/46-action-chunks-and-generative-policies/examples/chunks.py) | [记录](chapters/46-action-chunks-and-generative-policies/validation.md) |
| 47 | [世界模型起步：学会预测下一步](chapters/47-learned-dynamics/README.md) | [dynamics.py](chapters/47-learned-dynamics/examples/dynamics.py) | [记录](chapters/47-learned-dynamics/validation.md) |
| 48 | [潜在世界模型与记忆](chapters/48-latent-world-models/README.md) | [memory.py](chapters/48-latent-world-models/examples/memory.py) | [记录](chapters/48-latent-world-models/validation.md) |
| 49 | [用学到的世界模型规划](chapters/49-planning-with-world-models/README.md) | [learned_mpc.py](chapters/49-planning-with-world-models/examples/learned_mpc.py) | [记录](chapters/49-planning-with-world-models/validation.md) |
| 50 | [在想象中学习策略：Dreamer 思路](chapters/50-imagined-policy-learning/README.md) | [imagination.py](chapters/50-imagined-policy-learning/examples/imagination.py) | [记录](chapters/50-imagined-policy-learning/validation.md) |
| 51 | [视频生成与世界模型的边界](chapters/51-video-and-world-model-boundaries/README.md) | [action_counterexample.py](chapters/51-video-and-world-model-boundaries/examples/action_counterexample.py) | [记录](chapters/51-video-and-world-model-boundaries/validation.md) |
| 52 | [VLA：把视觉和语言连接到动作](chapters/52-vla-discrete-actions/README.md) | [scene.py](chapters/52-vla-discrete-actions/examples/scene.py)、[train_vla.py](chapters/52-vla-discrete-actions/examples/train_vla.py) | [记录](chapters/52-vla-discrete-actions/validation.md) |
| 53 | [连续动作 VLA 与动作生成模块](chapters/53-vla-continuous-actions/README.md) | [continuous.py](chapters/53-vla-continuous-actions/examples/continuous.py) | [记录](chapters/53-vla-continuous-actions/validation.md) |
| 54 | [机器人数据、跨本体与评测](chapters/54-robot-datasets-and-benchmarks/README.md) | [audit_data.py](chapters/54-robot-datasets-and-benchmarks/examples/audit_data.py) | [记录](chapters/54-robot-datasets-and-benchmarks/validation.md) |
| 55 | [从模型输出到稳定闭环](chapters/55-closed-loop-deployment/README.md) | [deployment.py](chapters/55-closed-loop-deployment/examples/deployment.py) | [记录](chapters/55-closed-loop-deployment/validation.md) |
| 56 | [独立读论文与做可解释的实验](chapters/56-reading-and-reproducing-papers/README.md) | [reproduction_record.py](chapters/56-reading-and-reproducing-papers/examples/reproduction_record.py) | [记录](chapters/56-reading-and-reproducing-papers/validation.md) |
| 57 | [综合项目：听懂指令的桌面智能体](chapters/57-capstone/README.md) | [capstone.py](chapters/57-capstone/examples/capstone.py) | [记录](chapters/57-capstone/validation.md) |
| 58 | [把知识连起来与选择下一步](chapters/58-synthesis-and-next-steps/README.md) | 概念阅读与自测 | [记录](chapters/58-synthesis-and-next-steps/validation.md) |

## 最小毕业项目运行链

在激活环境且当前目录为教材根目录时执行。前四条是训练准备；若对应权重已生成，只执行最后一条。

```bash
python chapters/41-imitation-learning/examples/bc.py
python chapters/47-learned-dynamics/examples/dynamics.py
python chapters/52-vla-discrete-actions/examples/train_vla.py
python chapters/53-vla-continuous-actions/examples/continuous.py
python chapters/57-capstone/examples/capstone.py
```

逐章结果已经运行并记录。最终交付阶段未重复所有训练；这是为了避免把同一次训练的重复评测误写成独立实验。完整大模型和真实机器人项目仍为选学，不能用本书环境兼容性推断其兼容性。
