# 第24章检查记录

[正文](README.md) · [全书目录](../../README.md)

验证日期：2026-10-24。验证状态：已完成。

在NumPy/PyTorch CPU环境运行text_basics.py与标准库simple_bpe.py。字符词表15项，四条已知文本均能精确往返；抓黄块变为抓<UNK>块，明确未知信息丢失。三条指令ID形状(3,9)、嵌入(3,9,8)、排除PAD/BOS/EOS后的平均(3,8)，内容长度7/7/3，PAD行全0。相反空间关系的字符词袋逐项相同。BPE学到l+o、lo+w、low+e、lowe+r四条规则，lowering分为lower/i/n/g，拼接能还原；aaa合并aa后剩a的非重叠行为核对通过。随机嵌入未训练语义，BPE仅片段合并演示；未声称运行Hugging Face外部库。
