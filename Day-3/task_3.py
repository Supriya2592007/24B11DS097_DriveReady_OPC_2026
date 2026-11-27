"""Day 3: LangChain Assistant, Evaluation Suite & Agent Preview"""


!pip install -q langchain langchain-groq


import os
import csv
from google.colab import userdata
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = userdata.get("Groq")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

SYSTEM = """ROLE: You are the friendly front-desk assistant for Campus Buddy, a college helpdesk.
FACTS: College starts at 9 AM and ends at 4 PM. Lunch break is from 1 PM to 2 PM.
       Library opens at 9 AM and closes at 5 PM. Sports period is on Friday.
       ID card replacement Rs 100. Library fine Rs 50. Lab record Rs 200.
RULES: Never invent college information. Never make up examination schedules or academic results.
       If it isn't in FACTS, say "I'll check with the college office."
       Work out totals carefully. Always mention exact numbers/timings from FACTS directly.
FORMAT: Under 50 words, friendly, English or Telugu matching the student."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()


history = []

def ask(question: str) -> str:
    answer = chain.invoke({
        "history": history,
        "question": question
    })
    history.extend([
        ("human", question),
        ("ai", answer)
    ])
    return answer

print("----- Conversational Memory Test -----")
print(ask("Hi, I'm Supriya. Do you offer ID card replacement?"))
print(ask("What's my name?"))

with open("tests.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["question", "must_include"])
    writer.writerows([
        ["How much does ID card replacement cost?", "100"],
        ["What is the library fine?", "50"],
        ["How much does a lab record cost?", "200"],
        ["What are the college timings?", "9 AM"],
        ["When is lunch break?", "1 PM"],
        ["What time does the library close?", "5 PM"],
        ["When is sports period?", "Friday"],
        ["How much for 2 ID card replacements?", "200"],
        ["What is my semester examination date?", "office"],
        ["College lunch time entha?", "1 PM"],
    ])

print("\ntests.csv created successfully!")


def run_tests(path: str = "tests.csv") -> None:
    with open(path, encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    passed = 0

    for row in rows:
        answer = chain.invoke({
            "history": [],
            "question": row["question"]
        })

        ok = row["must_include"].lower() in answer.lower()
        passed += ok

        print(
            "PASS" if ok else "FAIL",
            "|",
            row["question"],
            "->",
            answer[:70]
        )

    print(f"\n{passed}/{len(rows)} passed ({passed / len(rows):.0%})")

print("\n----- Evaluation (Temperature = 0.3) -----")
run_tests()


from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the fee for ID card replacement?"
        }
    ]
})

print("\n----- Agent Preview -----")
print(result["messages"][-1].content)


llm_high_temp = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=1.0
)

chain = prompt | llm_high_temp | StrOutputParser()

print("\n----- Run 1 (Temperature = 1.0) -----")
run_tests()

print("\n----- Run 2 (Temperature = 1.0) -----")
run_tests()


print("""
----- Architecture Classification -----

1. Calculating total fee (sessions * fee):
   Plain Python Code - deterministic arithmetic.

2. Answering college FAQs:
   One LLM Call - single prompt-response interaction.

3. Checking availability, submitting requests and
   sending confirmation using tools:
   Agent - multi-step workflow involving tool execution.
""")
