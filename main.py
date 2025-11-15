from openai import OpenAI
import json

from toPdf import convert_to_pdf

json_file = "result.json"
client = OpenAI(
  api_key="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"
)

with open("template.json", "r", encoding="utf-8") as file:
    TEMPLATE = file.read()
def make_prompt(idea):
    prompt = f"""
    {TEMPLATE}
    "{idea}"
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
    convertToJsonAndPdf(response.output_text)
    return response

def convertToJsonAndPdf(output):
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
    convert_to_pdf(json.load(open("result.json", "r", encoding="utf-8")))



convert_to_pdf(json.load(open("result.json", "r", encoding="utf-8")))
