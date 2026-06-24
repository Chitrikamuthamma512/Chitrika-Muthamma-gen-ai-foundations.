from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

# Load API key from environment variable (keep it secret!)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    """Generate interview questions based on role, level, and type."""
    data = request.json
    role  = data.get("role", "Software Developer")
    level = data.get("level", "fresher")
    type_ = data.get("type", "Mixed")
    count = data.get("count", 5)

    prompt = (
        f"Generate exactly {count} interview questions for a {level} {role} role. "
        f"Interview type: {type_}.\n"
        "Return ONLY a JSON array, no markdown, no extra text. Format:\n"
        '[{"q": "question text", "type": "HR" or "Technical", "hint": "1 short guidance hint"}]'
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()

    import json
    questions = json.loads(raw)
    return jsonify({"questions": questions})


@app.route("/evaluate-answer", methods=["POST"])
def evaluate_answer():
    """Evaluate a candidate's answer and return score + feedback."""
    data     = request.json
    role     = data.get("role", "Software Developer")
    level    = data.get("level", "fresher")
    question = data.get("question", "")
    answer   = data.get("answer", "")

    prompt = (
        f"You are an expert interview coach. Evaluate this interview answer.\n\n"
        f"Role: {role} ({level})\n"
        f"Question: {question}\n"
        f"Candidate answer: {answer}\n\n"
        "Return ONLY a JSON object, no markdown:\n"
        "{\n"
        '  "score": <integer 1-10>,\n'
        '  "feedback": "<2-3 sentence constructive evaluation>",\n'
        '  "tip": "<1 specific improvement tip for next time>"\n'
        "}"
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
