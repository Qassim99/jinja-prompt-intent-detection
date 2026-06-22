# Jinja Prompt Generation for Customer-Support Intent Detection

A small NLP project showing how the **Jinja** templating engine can generate
LLM prompts dynamically for a **customer-support intent-detection** task.

> Course: Advanced Natural Language Processing (SoSe 2026) — Homework 2, Part 5.
> Domain deliberately differs from the Lecture 5 notebook examples.

## The task / domain

Given a customer message (e.g. *"My package never arrived and I want my money back"*),
the model must classify it into one of a fixed set of **support intents**
(`order_status`, `refund_request`, `cancel_order`, `technical_issue`,
`billing_question`, `general_inquiry`) and optionally return a confidence score.

Support teams need this to route tickets automatically. Prompts for this task vary
along several axes: number of candidate intents, whether few-shot examples are
included, whether a clarifying instruction is added for ambiguous messages, and
whether the output should be plain text or JSON.

## What the Jinja template does

`prompt_template.j2` renders a complete classification prompt from a small set of
variables. From **one** template it produces several prompt **variants**:

- **Zero-shot** — just the instruction + intent list.
- **Few-shot** — loops over labeled examples with `{% for %}`.
- **JSON-output** — toggles a structured-output instruction with `{% if %}`.
- **Clarification mode** — optional block telling the model to ask a follow-up
  question when the message is ambiguous.

## Why Jinja is appropriate here

Plain string concatenation or a few Python `if` statements would get messy fast,
because the prompt has genuinely **variable structure**:

- **Loops** over the intent list and over a variable number of few-shot examples
  (`{% for intent in intents %}`, `{% for ex in examples %}`).
- **Optional sections** that appear only when relevant
  (`{% if examples %}`, `{% if want_json %}`, `{% if allow_clarify %}`).
- **Reusable components**: the intent list and example block are written once and
  reused across every variant.
- **Multiple output formats** from a single source of truth, so changing the
  wording in one place updates all variants.

Doing this with f-strings would mean scattering newline handling, join logic, and
conditional fragments throughout the Python code — exactly the maintenance problem
templating engines were designed to solve.

## Files

| File | Purpose |
|------|---------|
| `prompt_template.j2` | The Jinja template (all variants in one file). |
| `generate_prompts.py` | Loads the template, fills it with the example inputs, prints the prompts. |
| `examples.json` | Three+ example inputs from the domain. |
| `requirements.txt` | Dependencies (`Jinja2`). |

## Run it

```bash
pip install -r requirements.txt
python generate_prompts.py
```
