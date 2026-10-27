# 计数口径 / Counting method

日期：2026-10-27。tiktoken版本：0.14.0.

O = `o200k_base`；C = `cl100k_base`。方法：`len(encoding.encode(text, disallowed_special=()))`。文本中的特殊标记样式按普通字符串处理，不解释为消息协议的特殊token。

计数保留原标点、大小写、空格和显式换行，不作Unicode归一化；排版自动折行不改变计数原文。每个标注仅对应其相邻的文字；数字标注、标题标签等不计入该片段。模板有逐行和整段两种计数，两者不能用加法互换。

Counts preserve original punctuation, case, spaces, and explicit newlines without Unicode normalization. Badges and visual line wrapping are excluded. Whole templates are encoded independently from their lines. Message wrappers, system prompts, tools, and extra rounds are separate costs.

本次实测不向任何模型发送文档。两种公开分词器不代表所有模型；跨模型执行准确率尚未测试。数字是文本长度测量，不是理解准确率、压缩成功率或全局最优证明。

No documents were sent to a model for this measurement. The two encodings do not represent every model. Task execution and translation accuracy remain separate, unvalidated results.

`counts/*.csv` 保存准确计数原文、UTF-8 SHA-256与两种结果；`measurement.json`记录分词器版本及词表规模。运行 `python scripts/build.py` 重新计数并构建。

来源：[tiktoken官方项目](https://github.com/openai/tiktoken)；[官方计数示例](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)。
