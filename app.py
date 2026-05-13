import os
from flask import Flask, request, render_template_string
from openai import OpenAI

app = Flask(__name__)

# Wir nutzen dein OpenAI-Beispiel als Basis
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"), # Holt den Key sicher aus den Render-Einstellungen
)

# Das Design deiner Website
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>Meine KI Website</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; text-align: center; }
        textarea { width: 100%; height: 100px; padding: 10px; }
        button { background: #0084ff; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: #f9f9f9; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Frag die KI</h1>
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
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b:groq",
                messages=[{"role": "user", "content": user_text}],
            )
            antwort = completion.choices[0].message.content
        except Exception as e:
            antwort = f"Fehler: {str(e)}"
            
    return render_template_string(HTML_LAYOUT, antwort=antwort)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
