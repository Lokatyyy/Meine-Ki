import os
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

# Das Design deiner Website
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>PierreAI</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; text-align: center; }
        textarea { width: 100%; height: 100px; padding: 10px; }
        button { background: #0084ff; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: #f9f9f9; }
    </style>
</head>
<body>
    <div class="box">
        <h1>PierreAI</h1>
        <form method="POST">
            <textarea name="user_input" placeholder="Schreib hier etwas..."></textarea><br><br>
            <button type="submit">Antwort generieren</button>
        </form>
        {% if antwort %}
            <div style="margin-top:20px; text-align:left;">
                <strong>KI sagt:</strong>
                <p>{{ antwort }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    antwort = ""
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
        except Exception as e:
            antwort = f"Fehler: {str(e)}"
            
    return render_template_string(HTML_LAYOUT, antwort=antwort)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
