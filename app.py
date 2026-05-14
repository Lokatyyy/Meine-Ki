import html
import os
import re
from flask import Flask, request, render_template_string
import openai

app = Flask(__name__)

# KI-Persona und Einstellungen
SYSTEM_PROMPT = """Du bist PierreAI, eine freundliche und respektvolle KI für meinen Vater.
Du weißt, dass dein Nutzer ein Mann aus der Bretagne ist, der in München lebt.
Er heißt Pierre, ist verheiratet mit Laëtitia, hat die Söhne Louka, Solann und Hugo, und eine Tochter namens Chloé in Montreal.
Du kennst seine Interessen: Tauchen, Basteln, Werkzeug, Häuser bauen und KI.
Antworte immer höflich, klar und hilfsbereit, als würdest du einem Familienmitglied erklären.
Wenn du eine Frage nicht beantworten kannst, sag das ehrlich und biete eine sinnvolle Alternative an."""

# Client wird erst bei Bedarf initialisiert
def get_client():
    if not hasattr(get_client, '_client'):
        openai.api_key = os.environ.get("HF_TOKEN")
        openai.api_base = "https://router.huggingface.co/v1"
        get_client._client = openai
    return get_client._client

# Markdown-Formatierung für Antworten
def format_markdown(text):
    if not text:
        return ""
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__(.+?)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"_(.+?)_", r"<em>\1</em>", escaped)
    escaped = escaped.replace("\r\n", "\n").replace("\n\n", "</p><p>")
    escaped = escaped.replace("\n", "<br>")
    return f"<p>{escaped}</p>"

# Das Design deiner Website
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>PierreAI</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: radial-gradient(circle at top left, #dbeafe, transparent 35%),
                        radial-gradient(circle at bottom right, #e2e8f0, transparent 30%),
                        linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
            color: #0f172a;
        }
        .container {
            max-width: 760px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 28px;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.08);
            padding: 32px;
        }
        h1 {
            margin: 0;
            font-size: 2.5rem;
            letter-spacing: -0.03em;
        }
        .lead {
            margin: 12px 0 24px;
            color: #475569;
            line-height: 1.7;
        }
        textarea {
            width: 100%;
            min-height: 130px;
            padding: 16px;
            border: 1px solid #cbd5e1;
            border-radius: 16px;
            font-size: 1rem;
            line-height: 1.6;
            resize: vertical;
            background: #f8fafc;
        }
        button {
            background: #0f172a;
            color: white;
            padding: 14px 24px;
            border: none;
            border-radius: 14px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s ease, background 0.2s ease;
        }
        button:hover {
            transform: translateY(-1px);
            background: #020617;
        }
        .hint {
            margin-top: 12px;
            color: #64748b;
            font-size: 0.95rem;
        }
        .response {
            margin-top: 26px;
            text-align: left;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 22px;
            line-height: 1.7;
        }
        .response strong {
            display: block;
            margin-bottom: 10px;
            font-size: 0.98rem;
        }
        .footer {
            margin-top: 20px;
            font-size: 0.94rem;
            color: #64748b;
        }
        .message p {
            margin: 0 0 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>PierreAI</h1>
            <p class="lead">Lieber Papa, ich wünsche dir einen schönen Vatertag. Du bist der beste Vater, den ich mir hätte wünschen können, und danke für alles.</p>
            <p class="lead" style="font-weight:700; margin-bottom: 28px;">Von Louka 2026</p>
            <form method="POST">
                <textarea name="user_input" placeholder="Schreib hier deine Frage..."></textarea><br><br>
                <button type="submit">PierreAI fragen</button>
            </form>
            {% if antwort_html %}
                <div class="response">
                    <strong>PierreAI sagt:</strong>
                    <div class="message">{{ antwort_html|safe }}</div>
                </div>
            {% endif %}
        </div>
        <div class="footer">PierreAI ist für Vatertag optimiert und kennt Pierre, Laëtitia, Louka, Solann, Chloé und Hugo.</div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    antwort_html = ""
    if request.method == "POST":
        user_text = request.form.get("user_input")
        
        # Hier wird deine KI aufgerufen
        try:
            client = get_client()
            completion = client.ChatCompletion.create(
                model="openai/gpt-oss-120b:groq",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
            )
            antwort = completion.choices[0].message.content
            antwort_html = format_markdown(antwort)
        except Exception as e:
            antwort_html = format_markdown(f"Fehler: {str(e)}")
            
    return render_template_string(HTML_LAYOUT, antwort_html=antwort_html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
