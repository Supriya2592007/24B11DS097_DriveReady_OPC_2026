# Task 1: Constrained LLM Assistant & Prompt Guard

## Overview

This task covers two parts using the Groq API:

1. **Constrained Domain Assistant:** Built with `langchain_groq` (`ChatGroq`, model `openai/gpt-oss-120b`, `temperature=0`) acting as the front-desk assistant for **Campus Buddy**, a College Helpdesk Assistant, under strict facts, rules, and a 60-word limit.
2. **Prompt Injection Detection:** Uses the `groq` SDK with `meta-llama/llama-prompt-guard-2-22m` to test whether an input attempts to override system instructions.

## Google Colab Notebook

[Open the Day-1 Google Colab Notebook](https://colab.research.google.com/drive/1lAB0LdMa62_IVLATlEmegyGiar8TN9Ja?usp=sharing)

## Setup & API Key

- Install packages: `pip install langchain_groq groq`
- Add `GROQ_API_KEY` in Google Colab **Secrets** (enable Notebook access). The secret is named `Groq` in this notebook.
- The script retrieves the API key using `google.colab.userdata` and sets it as the `GROQ_API_KEY` environment variable.

## What the Code Does

- **System Prompt (Campus Buddy):** Defines college timings, lunch break, library timings, and sports period.
- **Rules:** Restricts answers to predefined college facts, prevents fabricated information, and enforces responses under 60 words.
- **`ask(question)` & Test Queries:** Sends system and human messages to `llm.invoke(...)` and tests college timings, lunch break, and unknown examination-related queries.
- **Prompt Guard Check:** Uses `meta-llama/llama-prompt-guard-2-22m` to test a prompt attempting to override system instructions.

## Project

Campus Buddy is a constrained college helpdesk assistant designed to provide basic campus-related information while following predefined instructions and testing prompt-injection detection.
