import os
import json
import base64
import urllib.request
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Genesis_Node API", version="3.0.0")

# Clé secrète maître et configuration GitHub (Optionnel mais prêt pour l'autonomie totale)
ADMIN_SECRET_KEY = "genesis_master_2026"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "") # Tu pourras l'ajouter dans Render si tu veux l'auto-sync GitHub
GITHUB_REPO = os.getenv("GITHUB_REPO", "genesis449/genesis-node")

class SovereignKernel:
    def __init__(self, name="Genesis_Node_Sovereign"):
        self.name = name
        self.memory_file = "memory.json"
        self.chat_history_file = "chat_history.json"
        self.security_log_file = "security_logs.json"
        self.banned_words_file = "banned_words.json"
        self.chat_history = []
        self.security_logs = []
        self.banned_words = ["spam_interdit_exemple"]
        
        self.load_memory()
        self.load_chat_history()
        self.load_security_logs()
        self.load_banned_words()

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
        self.auto_sync_github(self.memory_file)

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

    def load_security_logs(self):
        if os.path.exists(self.security_log_file):
            try:
                with open(self.security_log_file, "r", encoding="utf-8") as f:
                    self.security_logs = json.load(f)
            except:
                self.security_logs = []

    def log_security_event(self, ip, action):
        event = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ip": ip, "action": action}
        self.security_logs.append(event)
        if len(self.security_logs) > 200:
            self.security_logs.pop(0)
        with open(self.security_log_file, "w", encoding="utf-8") as f:
            json.dump(self.security_logs, f, indent=4, ensure_ascii=False)

    def load_banned_words(self):
        if os.path.exists(self.banned_words_file):
            try:
                with open(self.banned_words_file, "r", encoding="utf-8") as f:
                    self.banned_words = json.load(f)
            except:
                pass

    def save_banned_word(self, word):
        clean = word.strip().lower()
        if clean not in self.banned_words:
            self.banned_words.append(clean)
            with open(self.banned_words_file, "w", encoding="utf-8") as f:
                json.dump(self.banned_words, f, indent=4, ensure_ascii=False)

    def auto_sync_github(self, filepath):
        """Pousse automatiquement les fichiers locaux modifiés vers GitHub si le Token est configuré"""
        if not GITHUB_TOKEN or not GITHUB_REPO:
            return
        try:
            with open(filepath, "rb") as f:
                content_bytes = f.read()
            encoded_content = base64.b64encode(content_bytes).decode("utf-8")
            
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"
            
            # Récupérer le SHA du fichier existant si présent
            sha = ""
            req_get = urllib.request.Request(url, headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Genesis-Node"})
            try:
                with urllib.request.urlopen(req_get) as response:
                    data = json.loads(response.read().decode())
                    sha = data.get("sha", "")
            except:
                pass

            payload = {
                "message": f"Auto-sync souverain : mise à jour de {filepath}",
                "content": encoded_content,
                "sha": sha
            }
            
            req_data = json.dumps(payload).encode("utf-8")
            req_put = urllib.request.Request(url, data=req_data, headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Genesis-Node", "Content-Type": "application/json"}, method="PUT")
            urllib.request.urlopen(req_put)
        except Exception as e:
            print(f"Erreur sync GitHub : {e}")

    def save_to_memory(self, item, description=""):
        clean_key = item.strip().lower()
        self.knowledge_base[clean_key] = {
            "original_title": item.strip(),
            "description": description,
            "learned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_memory_to_disk()

    def delete_from_memory(self, item):
        clean_key = item.strip().lower()
        if clean_key in self.knowledge_base:
            del self.knowledge_base[clean_key]
            self.save_memory_to_disk()
            return True
        return False

    def chat_response(self, user_input, client_ip="unknown"):
        self.save_chat_history("Toi", user_input)
        user_input_lower = user_input.lower().strip()
        
        # Filtrage de sécurité local (Mots bannis)
        for bad in self.banned_words:
            if bad in user_input_lower:
                reply = "[Souveraineté] Requête rejetée : Contenu restreint par les protocoles de sécurité du noyau."
                self.save_chat_history(self.name, reply)
                self.log_security_event(client_ip, f"Tentative bloquée (mot banni : {bad})")
                return reply

        self.log_security_event(client_ip, f"Message reçu : {user_input[:30]}")

        # Commandes admin / filtres
        if user_input_lower.startswith("/ban "):
            word_to_ban = user_input[5:].strip()
            self.save_banned_word(word_to_ban)
            reply = f"[Sécurité] Le terme '{word_to_ban}' est désormais bloqué par le noyau."
            self.save_chat_history(self.name, reply)
            return reply

        if user_input_lower.startswith("/oublie "):
            target = user_input[8:].strip()
            if self.delete_from_memory(target):
                reply = f"[Souveraineté] Le concept '{target}' a été totalement effacé de ma mémoire."
            else:
                reply = f"[Souveraineté] Introuvable en mémoire : '{target}'."
            self.save_chat_history(self.name, reply)
            return reply

        if user_input_lower == "/memoire":
            keys = [data.get('original_title') for data in self.knowledge_base.values()]
            reply = f"[Mémoire Souveraine] Concepts enregistrés ({len(keys)}) : {', '.join(keys) if keys else 'Aucun'}"
            self.save_chat_history(self.name, reply)
            return reply

        # Apprentissage sémantique universel (Multilingue compatible : "est", "is", "c'est")
        separator = None
        for sep in [" est ", " is ", " c'est "]:
            if sep in user_input_lower:
                separator = sep
                break

        if separator:
            parts = user_input.split(separator, 1)
            concept = parts[0].strip()
            definition = parts[1].strip()
            self.save_to_memory(concept, definition)
            reply = f"[Souveraineté] Concept '{concept}' intégré avec succès dans ma mémoire."
            self.save_chat_history(self.name, reply)
            return reply

        # Recherche directe dans la mémoire
        for key, data in self.knowledge_base.items():
            if key in user_input_lower or user_input_lower in key:
                reply = f"[Mémoire Interne] {data.get('original_title')} : {data.get('description')}"
                self.save_chat_history(self.name, reply)
                return reply

        # Cerveau d'association textuelle locale
        matched_sentences = []
        words = user_input_lower.split()
        for key, data in self.knowledge_base.items():
            if any(w in key for w in words if len(w) > 3):
                matched_sentences.append(f"- {data.get('original_title')} : {data.get('description')}")
        
        if matched_sentences:
            reply = f"[Association Souveraine] Éléments croisés dans ma base :\n" + "\n".join(matched_sentences[:3])
            self.save_chat_history(self.name, reply)
            return reply

        # Commandes système
        if "système" in user_input_lower or "statut" in user_input_lower:
            reply = f"Noyau : {self.name} | Version : 3.0 Blindé | Sync GitHub : {'Actif' if GITHUB_TOKEN else 'Local pur'} | Nœuds : {len(self.knowledge_base)}"
            self.save_chat_history(self.name, reply)
            return reply

        reply = f"Analyse souveraine : Aucune correspondance directe. Enseigne-le-moi ([Concept] est [Définition]) ou tape /memoire."
        self.save_chat_history(self.name, reply)
        return reply

kernel = SovereignKernel()

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    kernel.log_security_event(client_ip, "Accès interface Web")
    
    history_html = ""
    for h in kernel.chat_history:
        if h['sender'] == 'Toi':
            history_html += f'<div class="msg-user"><b>Toi ></b> {h["message"]}</div>'
        else:
            history_html += f'<div class="msg-core"><b>{kernel.name} ></b> {h["message"].replace(chr(10), "<br>")}</div>'

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{kernel.name} - Version 3.0</title>
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
        .admin-bar {{ text-align: center; font-size: 11px; color: #666; margin-top: 8px; }}
    </style>
</head>
<body>
    <h1>🔒 {kernel.name} [3.0 SOUVERAIN BLINDÉ] 🔒</h1>
    <div id="chat-box">
        <div class="msg-core"><b>{kernel.name} ></b> Système initialisé. Commandes: /memoire | /oublie | /ban</div>
        {history_html}
    </div>
    <form id="chat-form" onsubmit="sendMessage(event)" class="input-container">
        <input type="text" id="user-input" placeholder="Discuter, enseigner ou commander..." autocomplete="off">
        <button type="submit">Envoyer</button>
    </form>
    <div class="admin-bar">Commandes : /memoire | /oublie [nom] | /ban [mot]</div>
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
async def chat_endpoint(payload: ChatRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    reply = kernel.chat_response(payload.message, client_ip)
    return {"reply": reply}

@app.get(f"/admin/{ADMIN_SECRET_KEY}/logs")
async def get_security_logs():
    return {"total_logs": len(kernel.security_logs), "logs": kernel.security_logs[-50:]}

@app.get(f"/admin/{ADMIN_SECRET_KEY}/export")
async def export_memory():
    return kernel.knowledge_base
