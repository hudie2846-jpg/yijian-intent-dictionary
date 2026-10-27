# 意简使用说明

计数口径：O / C = o200k_base / cl100k_base；只计算原始文本。

## 它能帮你做什么

把日常需求组织成清楚、可组合的短句，并查看词、释义、示例或整段模板在指定分词器下的 token 数。它不是所有模型都通用的最短编码，也不能保证任意意图无损。 [O 58 / C 81]

## 怎样查、怎样复制

按字段词、动作词、逻辑词和常用短句查找。只复制与你任务有关的表达；不复制数字标注、词义解释、目录或整本词典。复杂任务再补依据、范围、条件与输出。 [O 55 / C 81]

## 如何读 token 标注

O 代表 o200k_base，C 代表 cl100k_base。[O 2 / C 3] 表示紧邻原始文本在两种分词器下分别是2和3个 token。两列均为实测，不是字数估算，也不代表所有模型。 [O 64 / C 80]

## 数字到底包含什么

保留原始标点、大小写、空格及换行后计数，不作 Unicode 归一化。标注本身、排版自动折行、标题标签与说明文字不计入被标注片段。模板另标整段总数；逐行数字不能直接相加得到总数。 [O 70 / C 81]

## 复制之后要重新计数

改一个字、换一种标点、增加空格、翻译或替换对象，都可能改变 token。把最终提示词连同必须发送的解释卡一起重新编码，不用词条数值求和。聊天消息包装、系统提示、工具信息等费用另算。 [O 61 / C 87]

## 如何选择语言

先用自己能准确表达的语言。不同语言的示例不是普遍优劣排名。要比较就用同一意图、同一分词器、同一约束的完整输入，并另行检验模型理解与执行。Claude、Gemini及其他模型应使用各自适用的计数方式。 [O 72 / C 95]

## 哪些内容不能为了短而删

动作对象、否定、必要与充分条件、允许与必须、范围、例外、数量、单位、精度、日期、时区、权限和缺失信息处理。表述不明确时保留完整原句。 [O 50 / C 68]

## 如何验证效果

token测量与任务准确率分开记录。先人工核对语义，再在目标模型上实际执行。记录模型版本、运行配置、输入、token、检查点与失败案例。 [O 42 / C 55]

## 发布与维护

PDF用于阅读，Markdown用于网页查阅，JSON与计数CSV用于复核，脚本用于重新生成。条目编号已去掉；索引只保留词名、计数与页码。译文仍待独立母语审校，跨模型准确率尚未实测。 [O 66 / C 91]

## 直接复制的示例

```text
总结附件报告。保留关键数字。输出三条要点。缺失信息写“未知”，不猜测。
```

整段: [O 26 / C 36]

复制上面的原句，不复制 token 标注；替换“附件报告”或改变输出要求后重新计数。

---

# 의도 표현 사전 사용법

계산: O / C = o200k_base / cl100k_base. 원문만 계산.

## 무엇에 쓰나요

요구를 명확하고 조합 가능한 짧은 표현으로 정리하고 단어, 정의, 예문, 양식의 실제 토큰 수를 확인합니다. 모든 모델의 공통 최단 부호가 아니며 모든 의도의 무손실 표현을 보장하지 않습니다. [O 61 / C 96]

## 찾고 복사하기

필드, 동작, 논리, 자주 쓰는 표현에서 찾습니다. 작업에 필요한 문구만 복사하고 숫자 표시, 정의, 목차, 사전 전체는 복사하지 않습니다. 필요하면 근거, 범위, 조건, 출력 요구를 추가합니다. [O 61 / C 93]

## 토큰 표시 읽기

O는 o200k_base, C는 cl100k_base입니다. [O 2 / C 3]은 바로 옆 원문이 각각 2개와 3개의 토큰으로 인코딩됨을 뜻합니다. 둘 다 실측값이며 글자 수 추정이나 모든 모델의 수치가 아닙니다. [O 72 / C 99]

## 무엇을 센 값인가요

원래 문장 부호, 대소문자, 공백, 줄바꿈을 유지하고 Unicode 정규화는 하지 않습니다. 숫자 표시, 지면의 자동 줄바꿈, 제목, 설명용 라벨은 대상에 포함하지 않습니다. 양식은 전체 수치도 별도로 표시합니다. 행별 수치를 더해도 전체 수치와 같지 않을 수 있습니다. [O 83 / C 123]

## 수정 후 다시 세기

글자, 문장 부호, 공백, 번역, 대상 변경으로 토큰 수가 바뀔 수 있습니다. 필요한 해석 카드까지 합쳐 최종 입력 전체를 다시 셉니다. 단어별 수치를 합산해 대신하지 않습니다. 메시지 구조, 시스템 지시, 도구 오버헤드는 별도입니다. [O 74 / C 115]

## 언어 선택

의도를 정확하게 표현할 수 있는 언어를 우선합니다. 예문은 언어의 보편적인 우열을 입증하지 않습니다. 같은 의도, 제약, 토크나이저로 전체 입력을 비교하고 실행도 따로 검증합니다. Claude, Gemini 등에는 각자 맞는 계산 방식을 사용합니다. [O 73 / C 108]

## 줄이려고 지우면 안 되는 것

동작과 대상, 부정, 필요조건과 충분조건, 허용과 의무, 범위, 예외, 수량, 단위, 정밀도, 날짜, 시간대, 권한, 누락 정보 처리를 보존합니다. 모호해지면 완전한 문장을 유지합니다. [O 66 / C 98]

## 효과는 따로 검증

토큰 수와 작업 정확도는 서로 다른 결과입니다. 먼저 의미를 검토하고 대상 모델에서 실제로 실행합니다. 버전, 설정, 입력, 토큰 수, 확인점, 실패 사례를 기록합니다. [O 47 / C 78]

## 게시와 유지 관리

PDF는 읽기, Markdown은 웹 열람, JSON과 계산 CSV는 재검토, 스크립트는 재생성에 사용합니다. 항목 번호는 없애고 색인에는 표현, 수치, 쪽수만 표시합니다. 독립 원어민 교정과 여러 모델의 실행 검증은 아직 하지 않았습니다. [O 74 / C 114]

## 바로 복사할 예문

```text
첨부 보고서를 요약. 핵심 수치 유지. 요점 세 개 출력. 누락 정보는 "알 수 없음"으로 표시하고 추측하지 않음.
```

전체: [O 37 / C 58]

숫자 표시는 복사하지 않습니다. 첨부 자료나 출력 조건을 바꾸면 다시 계산합니다.

---

# 意図表現辞典の使い方

計数：O / C = o200k_base / cl100k_base。元の文字列のみ。

## 何に使うか

依頼を明確で組み合わせ可能な短い表現に整理し、語句・定義・例文・テンプレートのトークン数を確認します。全モデル共通の最短符号ではなく、任意の意図の無損失表現も保証しません。 [O 69 / C 101]

## 探してコピーする

フィールド、動作、論理、定型表現から探します。必要な表現だけをコピーし、数値ラベル、定義、目次、辞典全体はコピーしません。必要に応じ根拠資料、範囲、条件、出力を加えます。 [O 68 / C 93]

## 数値ラベルの読み方

Oはo200k_base、Cはcl100k_baseです。[O 2 / C 3] は隣接する元の文字列が、それぞれ2個・3個のトークンになることを示します。実測値であり、文字数からの推定や全モデル共通の値ではありません。 [O 73 / C 93]

## 何を数えたか

元の句読点、大文字・小文字、空白、改行を保ち、Unicode正規化は行いません。数値ラベル、紙面上の自動折り返し、見出し、説明用ラベルは対象文字列に含めません。テンプレートは全体の数も別に示します。各行の合計と全体の数は一致するとは限りません。 [O 94 / C 123]

## 編集後は数え直す

文字、句読点、空白、翻訳、対象の変更で数が変わる場合があります。必要な解釈カードも含め、最終プロンプト全体を数え直します。単語別の値を足して代用しません。メッセージ構造、システム指示、ツールのオーバーヘッドは別です。 [O 85 / C 117]

## 言語を選ぶ

意図を正確に書ける言語を優先します。用例は言語の普遍的な優劣を示しません。同一の意図・制約・トークナイザーで入力全体を比較し、実行も別途検証します。Claude、Geminiなどはそれぞれ適切な計数方法を使います。 [O 83 / C 117]

## 短くするために削らない要素

動作と対象、否定、必要条件と十分条件、許可と義務、範囲、例外、数量、単位、精度、日付、時間帯、権限、欠落情報の扱いを保ちます。曖昧になるなら完全な文を残します。 [O 69 / C 90]

## 効果を別途検証する

トークン数とタスク精度は別の結果です。先に意味を確認し、対象モデルで実行します。版、設定、入力、トークン数、確認点、失敗例を記録します。 [O 51 / C 77]

## 公開と更新

PDFは閲覧、Markdownはウェブ閲覧、JSONと計数CSVは再確認、スクリプトは再生成に使います。項目番号を削除し、索引には語句・計数・ページ番号を示します。独立した母語校閲と複数モデルでの実行検証は未実施です。 [O 79 / C 112]

## そのまま使える例文

```text
添付報告書を要約。主要な数値を保持。要点を3つ出力。欠落情報は「不明」とし、推測しない。
```

全体: [O 39 / C 50]

数値ラベルはコピーしません。添付資料や出力条件を変えたら数え直します。

---

# Yijian usage guide

Counting: O / C = o200k_base / cl100k_base; original text only.

## What this reference does

Organize requests into clear, composable expressions and inspect measured token counts for terms, definitions, examples, and templates. It is not a universally shortest encoding and does not guarantee lossless expression of arbitrary intent. [O 42 / C 42]

## Look up and copy

Browse fields, actions, logic, and common phrases. Copy only wording relevant to your task, not count labels, definitions, navigation, or the full dictionary. Add sources, scope, conditions, and output requirements when needed. [O 45 / C 45]

## Read the token labels

O means o200k_base and C means cl100k_base. [O 2 / C 3] means the adjacent original text encodes to two and three tokens respectively. Both are measured values, not character estimates or counts for every model. [O 51 / C 51]

## Know the counted boundary

Counts preserve original punctuation, case, spaces, and line breaks, without Unicode normalization. The badge itself, visual line wrapping, display headings, and explanatory labels are excluded. Templates have a separate whole-block count. Line counts need not sum to the block count. [O 52 / C 52]

## Recount after editing

A letter, punctuation mark, space, translation, or changed object may change the count. Encode the final prompt with any required interpretation card as one complete input. Do not sum dictionary counts. Message wrappers, system instructions, and tools add separate overhead. [O 50 / C 50]

## Choose the language deliberately

Use the language in which you can state the intent accurately. Examples do not establish a universal ranking of languages. Compare complete inputs with the same intent, constraints, and tokenizer, then test model execution. Use appropriate counting methods for Claude, Gemini, and other models. [O 53 / C 53]

## Do not shorten away constraints

Keep action and object, negation, necessary versus sufficient conditions, permission versus obligation, scope, exceptions, quantities, units, precision, dates, time zones, authority, and missing-data handling. Retain full sentences if meaning becomes unclear. [O 48 / C 48]

## Validate performance separately

Token measurement and task accuracy are different results. Review meaning first, then actually run the target model. Record its version, configuration, input, tokens, checks, and failures. [O 35 / C 35]

## Publish and maintain

Use PDFs for reading, Markdown for browsing, JSON and count CSV for auditing, and scripts for rebuilding. Entry numbers are removed; the index shows terms, counts, and page numbers. Independent native-speaker review and cross-model execution validation remain outstanding. [O 50 / C 51]

## Ready-to-copy example

```text
Summarize the attached report. Preserve key numbers. Output three bullet points. Mark missing information "unknown"; do not guess.
```

Whole block: [O 26 / C 26]

Copy the original wording, not its count badge. Recount after changing the attachment or output requirement.

---

