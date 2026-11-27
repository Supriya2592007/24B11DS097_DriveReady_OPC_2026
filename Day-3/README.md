# Day 3: LangChain Assistant, Evaluation Suite & Agent Preview

## Overview

This project implements **Campus Buddy**, a college helpdesk conversational assistant built using LangChain and Groq. It uses a conversational chain with memory, automated keyword-based evaluation, prompt refinement experiments, temperature testing, and a basic LangChain agent preview.

The assistant provides college-related information such as college timings, library hours, lunch breaks, sports periods, and sample service fees while following predefined rules.

## Google Colab Notebook

[Open Day-3 Notebook in Google Colab](https://colab.research.google.com/drive/1Fh2NaqmCE4s--xtJY8GOtUn-ub3Gg7WA?usp=sharing)

## Objectives

- Build a conversational assistant using LangChain.
- Implement conversational memory using `MessagesPlaceholder`.
- Create an LCEL pipeline using `ChatPromptTemplate`, `ChatGroq`, and `StrOutputParser`.
- Evaluate chatbot responses using a custom CSV benchmark.
- Experiment with prompt refinement and temperature.
- Explore the basic LangChain Agent architecture using `create_agent`.
- Understand when to use plain code, an LLM, or an Agent.

## Technologies Used

- Python
- LangChain
- LangChain-Groq
- Groq API
- Google Colab
- CSV

## System Configuration

- **LLM:** `openai/gpt-oss-20b`
- **Initial Temperature:** `0.3`
- **Experimental Temperature:** `1.0`
- **Framework:** LangChain
- **Environment:** Google Colab

## Campus Buddy Facts

The assistant operates using the following predefined sample college information:

| Information | Details |
|---|---|
| College start time | 9 AM |
| College end time | 4 PM |
| Lunch break | 1 PM – 2 PM |
| Library opening time | 9 AM |
| Library closing time | 5 PM |
| Sports period | Friday |
| ID card replacement | Rs 100 |
| Library fine | Rs 50 |
| Lab record | Rs 200 |

These are sample facts configured for the assistant.

## Implementation

### 1. LangChain Conversational Chain

Implemented a conversational pipeline using:

- `ChatPromptTemplate` for prompt construction.
- `MessagesPlaceholder` for conversation history.
- `ChatGroq` for LLM integration.
- `StrOutputParser` for extracting text responses.
- LCEL pipeline composition.

The assistant maintains conversation history and can recall information shared during earlier turns.

### 2. Stateful Conversation

Implemented an `ask()` function that maintains conversation history between user interactions.

Example:

- Student introduces themselves and asks about a college service.
- Student subsequently asks for their name.
- Assistant recalls the previously shared name through conversation history.

### 3. Automated Evaluation Suite

Created a custom `tests.csv` benchmark containing 10 test questions and expected keywords.

The evaluation function `run_tests()`:

- Reads test cases from the CSV file.
- Sends each question to the LangChain chain.
- Compares the model's response against the expected keyword.
- Identifies each test as PASS or FAIL.
- Calculates the overall pass rate.

### 4. Prompt Refinement Experiment

Refined the system prompt to encourage the assistant to state exact numbers, fees, and timings directly from the provided facts.

Prompt refinement helps improve response consistency and adherence to predefined information.

### 5. Temperature Experiment

Compared responses using two temperature settings:

- **Temperature 0.3:** Relatively consistent and predictable responses.
- **Temperature 1.0:** Greater response variation and potential inconsistency in exact wording.

The automated test suite was executed repeatedly at the higher temperature to observe changes in evaluation results.

### 6. LangChain Agent Preview

Implemented a basic agent using `create_agent` with an empty tool list.

This experiment demonstrates the basic Agent initialization process and compares its response behavior with the standard conversational chain.

## Architecture Classification

| Use Case | Architecture | Reason |
|---|---|---|
| Calculating service fees | Plain Python Code | Deterministic arithmetic calculations |
| Answering college FAQs | One LLM Call | Generates an answer from provided facts |
| Checking availability and submitting requests using tools | Agent | Multi-step workflow involving tool execution |

## How to Run

1. Open the Google Colab notebook linked above.
2. Add your Groq API key to Colab Secrets under the name `Groq`.
3. Enable notebook access to the secret.
4. Run all notebook cells in sequence.
5. Execute the CSV creation cell before running the evaluation function.
6. Observe the benchmark results and temperature experiment outputs.

## Learning Outcomes

- Understanding LangChain prompt templates and LCEL.
- Implementing stateful conversational memory.
- Integrating Groq models with LangChain.
- Building a basic automated evaluation framework.
- Understanding prompt refinement and temperature sensitivity.
- Exploring the distinction between traditional code, LLM calls, and Agents.

## Project

**Campus Buddy** is a learning project focused on exploring conversational AI, LangChain workflows, prompt engineering, automated evaluation, and agent-based architectures.
