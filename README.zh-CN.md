# Sema HaluMem-Long 评测

**[English](README.md) | [简体中文](README.zh-CN.md)**

本仓库记录了使用 Sema 进行的一次可复现的单用户 HaluMem-Long 长期记忆实验。本仓库是一个公开安全快照：基准测试产生的对话、问题、答案和逐题证据均被明确排除。

## 结果

| Accuracy | Hallucination | Omission |
| ---: | ---: | ---: |
| 89.02% (146/164) | 4.88% (8/164) | 6.10% (10/164) |

复核估计是在人工审查原始来源后，对有来源支持的答案以及包含额外细节的混合情况进行重新分类得到的。我们进行这次复核，是因为官方评测器似乎对一些有来源支持的答案和相关额外细节存在过度惩罚。Codex 将被标记的回答与原始对话及参考证据进行独立比较，以区分真实错误和可能的评测器误判。原始官方评测器结果仍保存在仓库中，并未被这次复核覆盖。

## 实验配置

| 参数 | 记录值 |
| --- | --- |
| 基准测试 | HaluMem-Long |
| 范围 | 一个 HaluMem 用户、115 个按顺序排列的 session、164 道问题 |
| 被测系统 | Sema |
| Runtime 配置 | Developer mode |
| STM budget | 10,000 tokens |
| WM budget | 10,000 tokens |
| LTM Maintainer 激活阈值 | 100 个待维护 slot |
| 权限策略 | Unattended |
| API 返回的模型 | `deepseek-flash`（DeepSeek V4 Flash） |
| 运行元数据中的配置模型值 | `deepseek-chat` |
| 二次复核者 | Codex / GPT-5.6 Luna XHigh；仅用于人工复核 |
| 官方评测器版本 | `718f16ff0c83413b1c86fa83fc13cc1a639871f9` |

上述 STM、WM、Runtime 配置、阈值和权限设置描述的是本地 Sema 执行环境。这些信息用于保证实验可复现，并不属于官方 HaluMem 基准测试规范。

影响结果解释的其他条件包括：

- 作答阶段使用了指定的作答规范，包括每个答案最多使用 20 个英文单词。
- 学习阶段和考试阶段彼此分离。考试开始前，学习数据已从 Sema workspace 中移除。
- 官方 HaluMem 评测器使用了上面记录的固定版本。
- 二次复核使用了私有证据副本中的原始对话和参考资料；它没有修改官方评测器的输入。
- 公开分支不包含原始基准测试对话、问题/答案文件或逐题证据。

## 公开发布边界

本快照包含实验配置、提示词、哈希值、来源引用、评测方法和聚合结果。完整证据保存在本地 `main` 分支中。要完整复现实验，需要根据适用条款单独获取 HaluMem，并将外部参考数据提供给私有评测脚本。

## 内容

- `learning_prompt.md`：学习阶段提示词
- `exam_prompt.md`：考试阶段文件协议
- `answering_guidelines.md`：作答规范
- `experiment_manifest.json`：实验元数据和公开边界
- `LearningData.sha256`：私有学习数据集的哈希清单
- `Sema/Placeholder text for test.txt`：用于挤出前台记忆的占位文档
- `Evaluation/full-115-sessions-20261116T000000Z/summary.md`：不含原始对话的聚合运行摘要
- `reports/sema-halumem-long-evaluation-report.pdf`：公开安全版结果报告
- `reports/sema-halumem-long-evaluation-report.md`：报告源文件

MIT 许可证仅适用于本仓库中的原创文件，不授予任何使用 HaluMem 数据或其他外部基准材料的权利。

## HaluMem 来源与许可

HaluMem 是一个外部基准测试。本仓库不重新分发 HaluMem 对话数据或派生的问题/答案证据。适用的数据条款和署名要求请参阅 HaluMem 仓库及其维护者说明：

- https://github.com/MemTensor/HaluMem
- https://github.com/MemTensor/HaluMem/issues/13

## 复现边界

本实验使用了上面记录的 HaluMem 数据顺序和评测器版本。由于基准测试产生的输入和详细证据被有意排除，仅凭公开快照无法完整复现实验。
