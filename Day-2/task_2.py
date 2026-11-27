"""task_2:-Campus Buddy - Stateful Multi-Turn College Helpdesk Assistant"""

!pip install -q openai

from google.colab import userdata              
from openai import OpenAI                        

client = OpenAI(
    api_key=userdata.get("Groq"),                
    base_url="https://api.groq.com/openai/v1",  
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",                 
    messages=[
        {"role": "system", "content": "You are a college helpdesk assistant."},
        {"role": "user", "content": "Describe a student trying to finish an assignment 10 minutes before the deadline."},
    ],
)
print(response.choices[0].message.content)

SYSTEM = """ROLE:   You are the front-desk assistant for Campus Buddy, a college helpdesk.
FACTS:  College starts at 9 AM and ends at 4 PM. Lunch break is from 1 PM to 2 PM.
        Library hours are 9 AM to 5 PM. Sports period is on Friday.
RULES:  Never invent college information. If the answer isn't in FACTS, say "I'll check with the college office."
FORMAT: Under 50 words, friendly, English or Telugu matching the student."""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    temperature=0.2,                             
    messages=[{"role": "system", "content": SYSTEM},
              {"role": "user", "content": "College timings enti? Library 4 PM ki open untunda?"}],
)
print(response.choices[0].message.content)
print(response.usage)

SERVICES = {"id card replacement": 100, "library fine": 50, "lab record": 200}   

SERVICES.get("bus pass", "service not listed")    

student_request = {"student": "Rahul", "service": "lab record", "sessions": 2, "urgent": True}

student_request["sessions"] * SERVICES[student_request["service"]]  

import json
text = json.dumps(student_request)   
back = json.loads(text)             
text

back

def get_fee(service: str, sessions: int = 1) -> int:
    return SERVICES[service.lower().strip()] * sessions

get_fee("id card replacement", 3)   
get_fee("  lab record ")             

import json, functools
from openai import RateLimitError, APIConnectionError

MODEL = "openai/gpt-oss-120b"
SERVICES = {"id card replacement": 100, "library fine": 50, "lab record": 200}

SYSTEM = f"""ROLE:   You are the friendly front-desk assistant for Campus Buddy, a college helpdesk.
FACTS:  College services with fees in rupees: {json.dumps(SERVICES)}
        College starts at 9 AM and ends at 4 PM. Lunch break is from 1 PM to 2 PM.
        Library hours are 9 AM to 5 PM. Sports period is on Friday.
RULES:  Never invent college information.
        If it isn't in FACTS, say "I'll check with the college office."
        Remember the student's name and requested service during the chat.
        Do not make up examination schedules, results or fee details.
FORMAT: Under 50 words, friendly, English or Telugu matching the student."""

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"   [log] {func.__name__}{args} -> {result!r}")
        return result
    return wrapper

@log_call
def get_fee(service: str, sessions: int = 1) -> int:
    """Return the total fee in rupees for sessions of a college service."""
    return SERVICES[service.lower().strip()] * sessions

history = [{"role": "system", "content": SYSTEM}]
MAX_TURNS = 8

def chat(user_text: str) -> str:
    history.append({"role": "user", "content": user_text})
    recent = [history[0]] + history[1:][-MAX_TURNS:]
    try:
        response = client.chat.completions.create(model=MODEL, messages=recent, temperature=0.3)
        reply = response.choices[0].message.content
    except RateLimitError:
        reply = "We're a little busy. Please try again in a minute."
    except APIConnectionError:
        reply = "I can't reach the server right now. Please try again shortly."
    history.append({"role": "assistant", "content": reply})
    return reply


while True:
    text = input("You: ")
    if text.lower().strip() in ("bye", "exit", "quit"):
        print("Bot: Thank you for contacting Campus Buddy!")
        break
    print("Bot:", chat(text))

history
