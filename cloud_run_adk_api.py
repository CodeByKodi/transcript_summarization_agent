from flask import Flask, request, jsonify
import google.auth
from vertexai import init, agent_engines
import os
import json

REGION = "asia-south1"
PROJECT_ID = "geni-project"
ENGINE_ID = "7284150184806711296"
APP_NAME = "Transcript Summarizer"  # Replace with your agent name if different

# === Init Vertex AI ===
credentials, PROJECT_ID = google.auth.default()
init(project=PROJECT_ID, location=REGION)

# === Load Agent Engine ===
apps = list(agent_engines.list(filter=f'display_name="{APP_NAME}"'))
if not apps:
    raise Exception(f"No agent found with display name '{APP_NAME}'")
agent_engine = apps[0]

# === Flask App ===
app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query_agent():
    data = request.json
    text = data.get("text", "")
    user_id = data.get("userId", "user-123")
    session_id = data.get("sessionId", "session-abc")

    try:
        session = agent_engine.create_session(user_id=user_id)
        stream = agent_engine.stream_query(
            user_id=user_id,
            session_id=session["id"],
            message=text
        )

        response_text = ""
        for event in stream:
            for part in event["content"]["parts"]:
                response_text += part.get("text", "")

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
