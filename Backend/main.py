from openai import OpenAI
import json
from flask import Flask, request, send_file, jsonify, render_template
app = Flask(__name__, template_folder="../Frontend")
import time

from toPdf import convert_to_pdf

json_file = "result/result.json"
json_template = "template/template.json"
pdf_file = "result/result.pdf"

client = OpenAI()



with open(json_template, "r", encoding="utf-8") as file:
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
    convert_to_pdf(json.load(open(json_file, "r", encoding="utf-8")), pdf_file)


# convert_to_pdf(json.load(open(json_file, "r", encoding="utf-8")), pdf_file)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", loading=False)

@app.route("/submitted", methods=["POST"])
def submitted():
    global idea
    idea = request.form.get("idea")
    if not idea:
        return render_template("index.html", loading=False)

    return render_template("index.html", loading=True)

@app.route("/waiting", methods=["POST"])
def waiting():
    make_prompt(idea)
    time.sleep(2)
    data = json.load(open(json_file, "r", encoding="utf-8"))
    return render_template("index.html", data=data, loading=False)

@app.route('/download', methods=['POST'])
def download_report():
    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)