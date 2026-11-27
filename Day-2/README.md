# Task 2: Stateful Multi-Turn Assistant Using OpenAI-Compatible Groq API

## 1. Overview

This task implements a stateful, multi-turn conversational assistant using the OpenAI Python SDK connected to Groq's OpenAI-compatible API endpoint.

The assistant, **Campus Buddy**, is designed to provide college-related information, maintain conversational context, work with structured service data, log helper function calls, handle API errors, and interact continuously with users through a chat loop.

## 2. Google Colab Notebook

[Open the Day-2 Google Colab Notebook](https://colab.research.google.com/drive/157ZltbjuD1RxJIJmjObeLNAtZk5d7a9G?usp=sharing)

## 3. Systems & Setup

- **Use-Case / Domain System:** Campus Buddy, a college helpdesk assistant.
- **Execution Environment:** Google Colab (Python 3).
- **API & Model Setup:** Groq API accessed through the OpenAI Python SDK (`base_url="https://api.groq.com/openai/v1"`) using `openai/gpt-oss-120b`.
- **Authentication:** Groq API key stored securely in Google Colab Secrets and accessed using `google.colab.userdata`.
- **Libraries Used:** `openai`, `json`, and `functools`.

## 4. How It Was Implemented

1. **Connected OpenAI Client to Groq:** Initialized the `OpenAI` client with the Groq API endpoint to send chat completion requests using the OpenAI-compatible API.
2. **Structured Service Data & JSON Handling:** Defined a college services dictionary containing sample service fees and practiced safe dictionary lookups, multiplication of fees, and JSON serialization/deserialization using `json.dumps()` and `json.loads()`.
3. **Designed the Constrained System Prompt:** Defined college timings, lunch break, library timings, sports period, service information, fallback responses, student memory instructions, and English/Telugu language matching under 50 words.
4. **Added a Logged Helper Function:** Implemented `get_fee(service, sessions)` with a custom `@log_call` decorator using `functools.wraps` to log function calls and return values.
5. **Implemented Sliding-Window Memory & Error Handling:** Maintained conversation messages using `history` and limited the API payload to the system prompt and recent messages using `MAX_TURNS = 8`. Handled `RateLimitError` and `APIConnectionError` with fallback responses.
6. **Built the Interactive Chat Loop:** Created a continuous `while` loop that accepts user queries, generates responses using `chat(text)`, and exits when the user enters `bye`, `exit`, or `quit`.

## 5. How to Run

1. Add the Groq API key to Google Colab **Secrets** and enable Notebook access.
2. Open the Day-2 notebook using the link above.
3. Run the notebook cells sequentially.
4. Enter questions at the `You:` prompt to interact with Campus Buddy.
5. Type `bye`, `exit`, or `quit` to end the conversation.

## 6. Project

Campus Buddy is a college helpdesk conversational assistant built to explore stateful LLM interactions, structured data handling, function logging, sliding-window conversation memory, and error handling using the Groq API.
