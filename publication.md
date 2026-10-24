# 发布说明

[全书目录](README.md) · [交付检查](book-validation.md)

## GitHub 仓库

本教材的发布仓库为[Charles-z-cloud/embodied-ai-from-scratch](https://github.com/Charles-z-cloud/embodied-ai-from-scratch)，可见性为私有。进入仓库后从README的01—58章目录顺序阅读。完整初稿为v1.0，文件内容可用release-manifest.json中的摘要核对。

## 发布包包含什么

包含正文、练习、答案、检查记录、示例源码、少量合成输入、自绘图、来源、环境说明和工具脚本。排除虚拟环境、Python缓存、模型权重和examples/output中的可重建结果。关键实验数字已写入各章validation.md；毕业项目另有results.md。

不存在需要下载的第三方大数据或模型才可阅读的正文。要运行依赖检查点的后续实验，按experiments.md生成先前权重。所有外部项目仅提供来源链接，没有把其代码或权重打包进来。

## 检查与打包

从教材根目录使用Python 3执行：

```bash
python scripts/check_book.py
python scripts/package_book.py
```

打包工具在教材的上一级目录创建`embodied-ai-textbook-v1.0.zip`，同时生成release-manifest.json记录每个发布文件的SHA-256。重新打包会更新同名交付包；不会修改章节正文。检查工具只做文件、语法、链接、章节顺序等结构检查，不运行训练，也不能证明每个学术判断正确。

GitHub可直接阅读Markdown及其数学公式、Mermaid图。其他Markdown阅读器若不支持公式或Mermaid，可以阅读周围的文字解释。发布前可预览README、任意公式章和毕业项目结果，确认渲染方式。

## 原创内容与来源

教材正文、教学代码和图例按本任务编写，引用资料在相应章节与references.md标明。尚未替用户选择对外授权许可证；公开可见与授予开源许可是不同设置，发布时按用户选定方式处理。外部资料继续适用各自条款。
