from openai import OpenAI
import json
json_file = "result.json"
client = OpenAI(
  api_key="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"
)

with open("template.json", "r", encoding="utf-8") as file:
    TEMPLATE = file.read()

project_idea = "نظام ذكاء اصطناعي لتقييم الواجبات وتصحيحها تلقائيًا."

prompt = f"""
{TEMPLATE}
"{project_idea}"
"""

response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": (
                        "You are a professional entrepreneurship analyst, understand business models, "
                        "market trends, and innovation strategies deeply. Analyze startup ideas logically "
                        "and realistically, providing structured feedback in Arabic. Focus on clarity and "
                        "practicality. Strictly adhere to the requested JSON format, avoid extra commentary, "
                        "and ensure all fields are filled accurately. Respond only in Arabic."
                    )
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt
                }
            ]
        }
    ]
)

def convertToJson(output):
    if isinstance(output, dict):
        data = output
    else:
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
            return

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("The analysis result saved to "+json_file)

convertToJson(response.output_text)
