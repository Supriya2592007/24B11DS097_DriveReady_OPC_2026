# Task 4: Tool-Using Campus Buddy Agent, Pydantic Validation & Google Sheets Integration

## 1. What the Task Is & System Chosen

- **Goal:** Upgrade the conversational assistant into a full **LangChain Agent** (`create_agent`) equipped with custom `@tool` functions, **Pydantic** input validation (`BaseModel` & `with_structured_output`), live **Google Sheets** persistence via `gspread`, execution trace inspection (`pretty_print()`), and tool-routing sensitivity experiments.
- **Selected System:** **Campus Buddy** college helpdesk assistant for student services, placements, academics, examinations, college rules, and administrative queries.
- **Environment & Setup:** Google Colab (Python 3) using `langchain`, `langchain-groq` (`ChatGroq` with `model="openai/gpt-oss-20b"`, `temperature=0.2`), `pydantic`, `gspread`, `GROQ_API_KEY` from Colab Secrets, and Google Colab OAuth (`google.colab.auth`).

## 2. Core Implementation & Outputs (Cells 1–10)

1. **Setup & Google Sheet Initialization (`Cells 1–2`):** Installed dependencies, initialized `ChatGroq`, authenticated the Google account, and created the **`Campus Buddy Student Requests`** spreadsheet with columns `["name", "category", "request", "urgency", "status"]`.

2. **Pydantic Model & Custom Tools (`Cell 3`):**
   - Defined the `StudentRequest` Pydantic schema enforcing valid request categories (`placements`, `student services`, `academics`, `exams`, `college rules`, `administration`, `other`), request details, student name, and boolean urgency.
   - Built seven custom `@tool` functions with type hints and descriptive docstrings:
     - `get_service_info(service)`: Retrieves demo fee information for ID card replacement, library fine, and lab record.
     - `get_college_info(topic)`: Returns known college timings, lunch break, library timings, and sports information.
     - `get_placement_info(topic)`: Handles placement-related queries without inventing unverified statistics or company details.
     - `get_academic_info(topic)`: Handles academic information queries.
     - `get_exam_info(topic)`: Handles examination-related queries.
     - `get_college_rules(topic)`: Handles college rules and facilities queries.
     - `log_student_request(name, category, request, urgent)`: Validates student request details using `StudentRequest` and saves confirmed requests to Google Sheets.

3. **Stateful Agent Execution (`Cells 4–5`):** Created a Campus Buddy agent using `create_agent(model=llm, tools=[...], system_prompt=SYSTEM)` with conversation history retention.
   - **Output Tested:** Asked questions about college timings, ID card replacement fees, placements, and examination information. The agent uses relevant tools and directs students to the appropriate college office when verified information is unavailable. Student requests are logged only after explicit confirmation.

4. **Trace Inspection & Edge-Case Testing (`Cells 6–7`):** Used `m.pretty_print()` to inspect `HumanMessage` -> `AIMessage` (`tool_calls`) -> `ToolMessage` -> final `AIMessage` steps. Tested unknown services, unavailable placement information, unknown examination dates, and incomplete student requests.

## 3. "Your 30%" Hands-On Work & Observations

1. **Custom `@tool` Functions:** Designed seven Campus Buddy tools covering student services, college information, placements, academics, examinations, college rules, and student request logging.

2. **Structured Extraction (`with_structured_output`):** Tested `llm.with_structured_output(StudentRequest)` across five unformatted student messages and extracted structured request information into validated `StudentRequest` objects.

3. **Google Sheets Persistence (`log_student_request`):** Connected the `Campus Buddy Student Requests` Google Sheet and implemented request validation and row insertion after collecting the required student details and explicit confirmation.

4. **Tool Docstring Sensitivity ("Break It" Experiment):** Temporarily replaced `get_college_info` with a vaguely named `tool1` function having a generic docstring (`"does stuff"`), inspected the agent's tool selection trace, and restored the descriptive tool.

5. **Execution Trace Count (`pretty_print()`):** Inspected a multi-tool query about lunch timings and ID card replacement fees using a fresh agent trace, then counted the exact `AIMessage` (model calls) and `ToolMessage` (tool calls) steps.

6. **College Information Handling:** Added known college facts and demo service fees while ensuring that unverified placement statistics, company information, examination schedules, and official policies are not fabricated.

## 4. How to Run

1. Add `GROQ_API_KEY` in Google Colab **Secrets** and enable **Notebook access**.
2. Run **Cell 1** and complete the Google OAuth prompt to authorize Google Sheets access. Use `gc.open("Campus Buddy Student Requests")` on subsequent runs instead of creating a new spreadsheet.
3. Run the remaining implementation and experiment cells sequentially.
4. Verify confirmed student requests in the generated Google Sheet URL.
