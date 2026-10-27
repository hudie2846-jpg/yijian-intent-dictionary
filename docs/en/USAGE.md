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

