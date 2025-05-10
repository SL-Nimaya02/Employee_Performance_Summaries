import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

with open("prompts/prompt_template.txt", "r") as f:
    PROMPT_TEMPLATE = f.read()

def generate_summary(employee):
    prompt = PROMPT_TEMPLATE.format(
        name=employee.get("Employee Name", ""),
        id=employee.get("Employee ID", ""),
        department=employee.get("Department", ""),
        month=employee.get("Month", ""),
        tasks=employee.get("Tasks Completed", ""),
        goals=employee.get("Goals Met (%)", ""),
        peer=employee.get("Peer Feedback", "No feedback provided."),
        manager=employee.get("Manager Comments", "No comments provided.")
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"
