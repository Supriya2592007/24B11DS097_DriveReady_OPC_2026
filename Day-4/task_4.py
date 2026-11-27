
!pip install -q langchain langchain-groq gspread

import os
from google.colab import userdata, auth
from langchain_groq import ChatGroq
import gspread
from google.auth import default
from typing import Literal
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain.agents import create_agent

os.environ["GROQ_API_KEY"] = userdata.get("Groq")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    max_retries=3
)

auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

sh = gc.create("Campus Buddy Student Requests")
ws = sh.sheet1

ws.append_row([
    "name", "category", "request", "urgency", "status"
])

print("Sheet ready:", sh.url)

SERVICES = {
    "id card replacement": 100,
    "library fine": 50,
    "lab record": 200
}

COLLEGE_FACTS = {
    "college timings": "College starts at 9 AM and ends at 4 PM.",
    "lunch": "Lunch break is from 1 PM to 2 PM.",
    "library": "Library opens at 9 AM and closes at 5 PM.",
    "sports": "Sports period is on Friday."
}

class StudentRequest(BaseModel):
    name: str = Field(
        description="Student's name. Use 'Not provided' if missing."
    )
    category: Literal[
        "placements",
        "student services",
        "academics",
        "exams",
        "college rules",
        "administration",
        "other"
    ] = Field(description="Category of the college helpdesk request")
    request: str = Field(
        description="Description of the student's request",
        min_length=5
    )
    urgent: bool = Field(
        description="True if the student explicitly indicates urgency"
    )

@tool
def get_service_info(service: str) -> str:
    """Get demo fee information for student services such as ID card replacement, library fine or lab record."""
    fee = SERVICES.get(service.lower().strip())

    if fee is None:
        return (
            f"Information for '{service}' is not listed. "
            "Please check with the college office."
        )

    return f"Demo fee for {service}: Rs {fee}."

@tool
def get_college_info(topic: str) -> str:
    """Get known general college information such as college timings, lunch break, library timings or sports period."""
    topic = topic.lower().strip()

    aliases = {
        "timings": "college timings",
        "college time": "college timings",
        "college hours": "college timings",
        "lunch timings": "lunch",
        "lunch break": "lunch",
        "library timings": "library",
        "sports period": "sports"
    }

    topic = aliases.get(topic, topic)
    info = COLLEGE_FACTS.get(topic)

    if info is None:
        return (
            "This information is not verified. "
            "Please check with the college office."
        )

    return info

@tool
def get_placement_info(topic: str) -> str:
    """Handle placement-related queries about companies, placement percentage, packages, eligibility, training and placement drives."""
    return (
        "Verified placement information is not currently available "
        "in the Campus Buddy knowledge base. "
        "Please check with the placement cell."
    )

@tool
def get_academic_info(topic: str) -> str:
    """Handle academic queries about syllabus, academic calendar, assignments, academic schedules and lab records."""
    return (
        "Verified academic information for this topic is not currently "
        "available. Please check with your department or college office."
    )

@tool
def get_exam_info(topic: str) -> str:
    """Handle queries about semester exams, hall tickets, results, supplementary exams, revaluation and examination schedules."""
    return (
        "Verified examination information is not currently available. "
        "Please check with the examination branch."
    )

@tool
def get_college_rules(topic: str) -> str:
    """Handle queries about attendance, uniform, college facilities, student rules and general college policies."""
    return (
        "Verified college rule information is not currently available. "
        "Please check with the college office."
    )

@tool
def log_student_request(
    name: str,
    category: str,
    request: str,
    urgent: bool
) -> str:
    """Save a student helpdesk request to Google Sheets. Use only after the student explicitly agrees to submit the request and provides their name, category and request details."""
    try:
        student = StudentRequest(
            name=name,
            category=category.lower().strip(),
            request=request,
            urgent=urgent
        )
    except Exception as e:
        return f"Could not save the request: {e}. Please correct the details."

    ws.append_row([
        student.name,
        student.category,
        student.request,
        "yes" if student.urgent else "no",
        "Pending"
    ])

    return (
        f"Request submitted successfully for {student.name}. "
        f"Category: {student.category}. Status: Pending."
    )

SYSTEM = """
ROLE: You are Campus Buddy, a friendly college helpdesk assistant.

SCOPE:
Help students with placements, student services, academics,
examinations, college rules, administration and general college queries.

RULES:
1. Use the appropriate tool for college-related information.
2. Never invent college information.
3. Never fabricate placement percentages, packages, company names,
   examination dates, results or official policies.
4. If verified information is unavailable, direct the student to
   the appropriate college office, department, placement cell or exam branch.
5. For student service fee queries, use the service information tool.
6. For college timings and known facts, use the college information tool.
7. Before submitting a student request, collect the student's name,
   category and request details.
8. Ask for explicit confirmation before saving a request.
9. Never call the request logging tool without explicit student consent.
10. After saving, confirm the request and its Pending status.
11. Never submit duplicate requests without the student's consent.

FORMAT:
Friendly and concise. Under 80 words where possible.
Reply in English or Telugu-English matching the student.
"""

agent = create_agent(
    model=llm,
    tools=[
        get_service_info,
        get_college_info,
        get_placement_info,
        get_academic_info,
        get_exam_info,
        get_college_rules,
        log_student_request
    ],
    system_prompt=SYSTEM
)

history = []

def chat(text: str) -> str:
    global history

    try:
        result = agent.invoke({
            "messages": history + [
                {"role": "user", "content": text}
            ]
        })

        history = result["messages"]
        return history[-1].content

    except Exception as e:
        print("Agent error:", e)
        return "Sorry, I'm a little busy. Please try again in a minute."

print(chat("Hi! What are the college timings?"))
print(chat("What is the ID card replacement fee?"))
print(chat("What was last year's placement percentage?"))
print(chat("When will semester results be announced?"))

# print(chat("I want to submit a request regarding my lab record."))
# print(chat("My name is Kiran. I need help getting a lab record."))
# print(chat("Yes, please submit my request."))

for m in history:
    m.pretty_print()

print("\n--- Edge Case Tests ---")

print(chat("Tell me the exact placement percentage last year."))
print(chat("What is the fee for a migration certificate?"))
print(chat("What is the exact supplementary exam date?"))
print(chat("I want to submit an urgent examination request."))
print(chat("My name is Ravi. I need help with my hall ticket."))

structured_llm = llm.with_structured_output(StudentRequest)

messy_messages = [
    "hey I'm Ananya, I need help with placement eligibility",
    "Karthik here, my hall ticket isn't available, please help",
    "Hi I'm Meena, need help with lab record submission urgently",
    "Suresh needs help regarding attendance rules",
    "urgent exam revaluation help for Priya"
]

for msg in messy_messages:
    parsed = structured_llm.invoke(msg)
    print(msg, "->", parsed)

@tool
def tool1(topic: str) -> str:
    """does stuff"""
    topic = topic.lower().strip()

    aliases = {
        "timings": "college timings",
        "college hours": "college timings",
        "lunch timings": "lunch",
        "library timings": "library"
    }

    topic = aliases.get(topic, topic)
    info = COLLEGE_FACTS.get(topic)

    if not info:
        return "Information not found."

    return info

broken_agent = create_agent(
    model=llm,
    tools=[
        get_service_info,
        tool1,
        get_placement_info,
        get_academic_info,
        get_exam_info,
        get_college_rules,
        log_student_request
    ],
    system_prompt=SYSTEM
)

broken_result = broken_agent.invoke({
    "messages": [
        {"role": "user", "content": "What are the college timings?"}
    ]
})

for m in broken_result["messages"]:
    m.pretty_print()

@tool
def get_college_info(topic: str) -> str:
    """Get known general college information such as college timings, lunch break, library timings or sports period."""
    topic = topic.lower().strip()

    aliases = {
        "timings": "college timings",
        "college time": "college timings",
        "college hours": "college timings",
        "lunch timings": "lunch",
        "lunch break": "lunch",
        "library timings": "library",
        "sports period": "sports"
    }

    topic = aliases.get(topic, topic)
    info = COLLEGE_FACTS.get(topic)

    if not info:
        return (
            "This information is not verified. "
            "Please check with the college office."
        )

    return info

agent = create_agent(
    model=llm,
    tools=[
        get_service_info,
        get_college_info,
        get_placement_info,
        get_academic_info,
        get_exam_info,
        get_college_rules,
        log_student_request
    ],
    system_prompt=SYSTEM
)

trace_result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the lunch timing and ID card replacement fee?"
        }
    ]
})

for m in trace_result["messages"]:
    m.pretty_print()

model_calls = sum(
    1 for m in trace_result["messages"]
    if m.type == "ai"
)

tool_calls = sum(
    1 for m in trace_result["messages"]
    if m.type == "tool"
)

print(f"\nModel calls (AI messages): {model_calls}")
print(f"Tool calls (Tool messages): {tool_calls}")

print("\nCampus Buddy Day-4 completed successfully!")
