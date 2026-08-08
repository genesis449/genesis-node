import os
import json
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Genesis_Node API", version="1.0.0")

class SovereignKernel:
    def __init__(self, name="Genesis_Node_Sovereign"):
        self.name = name
        self.memory_file = "memory.json"
        self.chat_history_file = "chat_history.json"
        self.chat_history = []
        self.load_memory()
        self.load_chat_history()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.knowledge_base = json.load(f)
            except:
                self.knowledge_base = {}
        else:
            self.knowledge_base = {}

    def save_memory_to_disk(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, indent=4, ensure_ascii=False)

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            try:
                with open(self.chat_history_file, "r", encoding="utf-8") as f:
                    self.chat_history = json.load(f)
            except:
                self.chat_history = []

    def save_chat_history(self, sender, message):
        self.chat_history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "sender": sender, "message": message})
        if len(self.chat_history) > 100:
            self.chat_history.pop(0)
        with open(self.chat_history_file, "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=4, ensure_ascii=False)

    def save_to_memory(self, item, description=""):
        clean_key = item.strip().lower()
        self.knowledge_base[clean_key] = {
            "original_title": item.strip(),
            "description": description,
            "learned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_memory_to_disk()

    def chat_response(self, user_input):
        self.save_chat_history("Toi", user_input)
        user_input_lower = user_input.lower().strip()
        
        # Apprentissage sémantique ("X est Y")
        if " est " in user_input_lower:
            parts = user_input.split(" est ", 1)
            concept = parts[0].strip()
            definition = parts[1].strip()
            self.save_to_memory(concept, definition)
            reply = f"[Souveraineté] Concept '{concept}' intégré avec succès dans ma mémoire."
            self.save_chat_history(self.name, reply)
            return reply

        # Recherche dans la mémoire
        for key, data in self.knowledge_base.items():
            if key in user_input_lower or user_input_lower in key:
                reply = f"[Mémoire Interne] {data.get('original_title')} : {data.get('description')}"
                self.save_chat_history(self.name, reply)
                return reply

        # Commandes système de base
        if "système" in user_input_lower or "statut" in user_input_lower:
            reply = f"Noyau : {self.name} | CPU : Helio G37 | RAM : 6 Go | Nœuds mémoriels : {len(self.knowledge_base)}"
            self.save_chat_history(self.name, reply)
            return reply

        reply = f"Analyse souveraine de '{user_input}' : Aucune correspondance en mémoire. Enseigne-le-moi en écrivant par exemple '[Concept] est [Définition]'."
        self.save_chat_history(self.name, reply)
        return reply

kernel = SovereignKernel()

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_index():
    history_html = ""
    for h in kernel.chat_history:
        if h['sender'] == 'Toi':
            history_html += f'<div class="msg-user"><b>Toi ></b> {h["message"]}</div>'
        else:
            history_html += f'<div class="msg-core"><b>{kernel.name} ></b> {h["message"]}</div>'

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{kernel.name} - Cloud Ready</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ background-color: #050505; color: #00ff66; font-family: monospace; padding: 15px; margin: 0; }}
        h1 {{ color: #ff0055; text-align: center; font-size: 16px; text-shadow: 0 0 8px rgba(255,0,85,0.4); }}
        #chat-box {{ background: #0f0f0f; border: 1px solid #00ff6633; height: 60vh; overflow-y: scroll; padding: 12px; border-radius: 6px; margin-bottom: 12px; white-space: pre-wrap; font-size: 13px; }}
        .msg-user {{ color: #ffffff; margin: 8px 0; }}
        .msg-core {{ color: #00ff66; margin: 8px 0; }}
        .input-container {{ display: flex; gap: 8px; }}
        input[type="text"] {{ flex: 1; padding: 12px; background: #0a0a0a; border: 1px solid #00ff6666; color: #00ff66; border-radius: 4px; font-size: 14px; outline: none; }}
        button {{ padding: 12px 18px; background: #ff0055; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>🔒 {kernel.name} [SOUVERAIN] 🔒</h1>
    <div id="chat-box">
        <div class="msg-core"><b>{kernel.name} ></b> Système initialisé. Prêt pour tes instructions.</div>
        {history_html}
    </div>
    <form id="chat-form" onsubmit="sendMessage(event)" class="input-container">
        <input type="text" id="user-input" placeholder="Discuter ou enseigner (ex: Python est un langage)..." autocomplete="off">
        <button type="submit">Envoyer</button>
    </form>
    <script>
        const box = document.getElementById('chat-box');
        box.scrollTop = box.scrollHeight;
        
        function sendMessage(e) {{
            e.preventDefault();
            const input = document.getElementById('user-input');
            const text = input.value.trim();
            if(!text) return;
            
            box.innerHTML += '<div class="msg-user"><b>Toi ></b> ' + text + '</div>';
            input.value = '';
            box.scrollTop = box.scrollHeight;
            
            fetch('/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: text }})
            }})
            .then(res => res.json())
            .then(data => {{
                box.innerHTML += '<div class="msg-core"><b>' + '{kernel.name}' + ' ></b> ' + data.reply.replace(/\\n/g, '<br>') + '</div>';
                box.scrollTop = box.scrollHeight;
            }});
        }}
    </script>
</body>
</html>"""

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    reply = kernel.chat_response(payload.message)
    return {"reply": reply}
