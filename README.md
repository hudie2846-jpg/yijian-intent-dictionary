# 意简 YIJIAN

**四语言意图表达词典，逐项标注实测 token 数。v0.4**

把意思说清楚，再比较表达成本。含中文、韩文、日文和英文词典，各133个词条及示例、30个语义评测种子。

Intent-expression dictionaries in Chinese, Korean, Japanese, and English with measured token counts. Each contains 133 entries and examples plus 30 semantic test seeds. No visible entry or chapter IDs; page numbers remain.

## 阅读 / Read

| 语言 | 词典 PDF | 网页版 | 使用说明 |
| --- | --- | --- | --- |
| 中文 | [PDF](docs/zh-CN/dictionary.pdf) | [Markdown](docs/zh-CN/dictionary.md) | [使用说明](docs/zh-CN/USAGE.md) |
| 한국어 | [PDF](docs/ko/dictionary.pdf) | [Markdown](docs/ko/dictionary.md) | [사용법](docs/ko/USAGE.md) |
| 日本語 | [PDF](docs/ja/dictionary.pdf) | [Markdown](docs/ja/dictionary.md) | [使い方](docs/ja/USAGE.md) |
| English | [PDF](docs/en/dictionary.pdf) | [Markdown](docs/en/dictionary.md) | [Usage](docs/en/USAGE.md) |

[四语使用说明 PDF / Four-language usage guide](docs/usage-four-languages.pdf) · [使用说明网页版](USAGE.md)

## token 标注 / Token labels

`[O 2 / C 3]`：相邻原始文本在 `o200k_base` 下为2个token，在 `cl100k_base` 下为3个。使用 `tiktoken==0.14.0` 本地实测，含原始标点、空格、换行；不含标注本身及排版折行。模板另给整段总数。只复制表达，不复制标注。

O = o200k_base; C = cl100k_base. Counts apply to the adjacent original text, not the badge. Preserve original spaces, punctuation, and newlines. Individual counts are not additive: recount the complete prompt after editing. The two encodings do not stand in for every model or tokenizer.

已验证的是文本计数，不是任务执行准确率。韩日英译文尚未经独立母语审校，跨模型任务实验尚未完成。

Text counts are measured; cross-model execution accuracy and independent native-speaker review remain outstanding.

## 数据与复核 / Data and audit

- `data/`：不含条目编号的各语言词库，附词条、释义和示例的独立计数。
- `eval/`：无编号的语义种子，附原句与候选计数。
- `counts/`：全部被标注片段的准确原文、UTF-8 SHA-256及计数CSV。
- `locales/`：四语言正文和使用说明的可编辑源文本。
- `scripts/build.py`：计数、生成PDF/Markdown及导出记录。
- [计数口径与版本记录](TOKEN-COUNTING.md)

```bash
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/verify_counts.py
```

初次运行需下载公开分词词表。默认中文微软雅黑、日文游ゴシック、韩文맑은 고딕、英文Arial；字体不随包分发。其他系统设置 `YIJIAN_ZH_CN_FONT`、`YIJIAN_ZH_CN_BOLD_FONT`、`YIJIAN_JA_FONT`、`YIJIAN_JA_BOLD_FONT`、`YIJIAN_KO_FONT`、`YIJIAN_KO_BOLD_FONT`、`YIJIAN_EN_FONT`、`YIJIAN_EN_BOLD_FONT` 指向可嵌入且覆盖所需字符的兼容TrueType字体。

First run downloads public tokenizer vocabularies. Compatible embeddable TrueType fonts are required; font files are not redistributed. Configure the language-specific environment variables above on other systems. TTC fonts use subfont zero.

## 计数方法来源 / Counting references

[tiktoken 官方项目](https://github.com/openai/tiktoken) · [官方计数示例](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)

## 许可 / License

许可与个人署名尚未指定，见 [LICENSE-STATUS.md](LICENSE-STATUS.md)。
