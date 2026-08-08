import os
import json
import base64
import urllib.request
import urllib.parse
import random
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Genesis_Node API", version="5.0.0")

ADMIN_SECRET_KEY = "genesis_master_2026"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "genesis449/genesis-node")

class SovereignKernel:
    def __init__(self, name="Genesis_Node_Sovereign"):
        self.name = name
        self.memory_file = "memory.json"
        self.chat_history_file = "chat_history.json"
        self.security_log_file = "security_logs.json"
        self.banned_words_file = "banned_words.json"
        self.peers_file = "peers.json"
        self.neural_matrix_file = "neural_matrix.json"
        
        self.chat_history = []
        self.security_logs = []
        self.banned_words = []
        self.peers = []
        self.neural_matrix = {} # Nouvelle matrice neuronale locale pour la génération de texte
        
        self.load_memory()
        self.load_chat_history()
        self.load_security_logs()
        self.load_banned_words()
        self.load_peers()
        self.load_neural_matrix()

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

    def load_peers(self):
        if os.path.exists(self.peers_file):
            try:
                with open(self.peers_file, "r", encoding="utf-8") as f:
                    self.peers = json.load(f)
            except:
                self.peers = []

    def save_peer(self, peer_url):
        clean = peer_url.strip()
        if clean not in self.peers:
            self.peers.append(clean)
            with open(self.peers_file, "w", encoding="utf-8") as f:
                json.dump(self.peers, f, indent=4, ensure_ascii=False)

    def load_neural_matrix(self):
        if os.path.exists(self.neural_matrix_file):
            try:
                with open(self.neural_matrix_file, "r", encoding="utf-8") as f:
                    self.neural_matrix = json.load(f)
            except:
                self.neural_matrix = {}
        else:
            self.neural_matrix = {}

    def save_neural_matrix(self):
        with open(self.neural_matrix_file, "w", encoding="utf-8") as f:
            json.dump(self.neural_matrix, f, indent=4, ensure_ascii=False)

    def train_neural_matrix(self, text):
        """Apprend la structure des mots pour générer du texte de manière autonome (style Markov local)"""
        words = text.split()
        for i in range(len(words) - 1):
            w1 = words[i].lower()
            w2 = words[i+1]
            if w1 not in self.neural_matrix:
                self.neural_matrix[w1] = []
            if w2 not in self.neural_matrix[w1]:
                self.neural_matrix[w1].append(w2)
        self.save_neural_matrix()

    def generate_neural_text(self, start_word, max_length=15):
        """Génère une phrase complète de manière neuronale locale"""
        current = start_word.lower()
        result = [start_word]
        for _ in range(max_length):
            if current in self.neural_matrix and self.neural_matrix[current]:
                next_word = random.choice(self.neural_matrix[current])
                result.append(next_word)
                current = next_word.lower()
            else:
                break
        if len(result) > 1:
            return " ".join(result)
        return None

    def auto_sync_github(self, filepath):
        if not GITHUB_TOKEN or not GITHUB_REPO:
            return
        try:
            with open(filepath, "rb") as f:
                content_bytes = f.read()
            encoded_content = base64.b64encode(content_bytes).decode("utf-8")
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"
            sha = ""
            req_get = urllib.request.Request(url, headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Genesis-Node"})
            try:
                with urllib.request.urlopen(req_get) as response:
                    sha = json.loads(response.read().decode()).get("sha", "")
            except:
                pass
            payload = {"message": f"Sync V5.0 : {filepath}", "content": encoded_content, "sha": sha}
            req_put = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Genesis-Node", "Content-Type": "application/json"}, method="PUT")
            urllib.request.urlopen(req_put)
        except Exception as e:
            print(f"Erreur sync : {e}")

    def save_to_memory(self, item, description=""):
        clean_key = item.strip().lower()
        self.knowledge_base[clean_key] = {
            "original_title": item.strip(),
            "description": description,
            "learned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_memory_to_disk()
        self.train_neural_matrix(description) # Entraînement automatique de la matrice neuronale

    def delete_from_memory(self, item):
        clean_key = item.strip().lower()
        if clean_key in self.knowledge_base:
            del self.knowledge_base[clean_key]
            self.save_memory_to_disk()
            return True
        return False

    def semantic_search(self, query):
        query_words = set(w.lower() for w in query.split() if len(w) > 2)
        if not query_words:
            return None
        
        best_match = None
        max_score = 0
        
        for key, data in self.knowledge_base.items():
            key_words = set(w.lower() for w in key.split() if len(w) > 2)
            desc_words = set(w.lower() for w in data.get('description', '').split() if len(w) > 2)
            all_target_words = key_words.union(desc_words)
            
            common = query_words.intersection(all_target_words)
            score = len(common)
            
            if score > max_score:
                max_score = score
                best_match = data

        if max_score > 0 and best_match:
            return f"[Mémoire Vectorielle V5] {best_match.get('original_title')} : {best_match.get('description')}"
        return None

    def autonomous_web_search(self, query):
        try:
            encoded_q = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_q}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
            
            if "result__snippet" in html_content:
                parts = html_content.split('class="result__snippet">')
                snippets = []
                for p in parts[1:4]:
                    snippet = p.split('</a>')[0].split('</')[0].replace('<b>', '').replace('</b>', '').strip()
                    if snippet and len(snippet) > 20:
                        snippets.append(snippet)
                if snippets:
                    summary = " ".join(snippets[:2])
                    self.save_to_memory(query, summary)
                    return f"[Exploration Web Autonome] Données capturées : {summary}"
        except Exception as e:
            pass
        return None

    def chat_response(self, user_input, client_ip="unknown"):
        self.save_chat_history("Toi", user_input)
        user_input_lower = user_input.lower().strip()
        
        for bad in self.banned_words:
            if bad in user_input_lower:
                reply = "[Souveraineté] Bloqué par la sécurité du noyau."
                self.save_chat_history(self.name, reply)
                return reply

        self.log_security_event(client_ip, f"Requête : {user_input[:30]}")
        self.train_neural_matrix(user_input) # Entraînement continu sur chaque message utilisateur

        if user_input_lower.startswith("/peer "):
            peer_url = user_input[6:].strip()
            self.save_peer(peer_url)
            reply = f"[Réseau Décentralisé] Nœud partenaire enregistré : {peer_url}"
            self.save_chat_history(self.name, reply)
            return reply

        if user_input_lower.startswith("/oublie "):
            target = user_input[8:].strip()
            if self.delete_from_memory(target):
                reply = f"[Souveraineté] '{target}' effacé de la mémoire."
            else:
                reply = f"[Souveraineté] Introuvable : '{target}'."
            self.save_chat_history(self.name, reply)
            return reply

        if user_input_lower == "/memoire":
            keys = [data.get('original_title') for data in self.knowledge_base.values()]
            reply = f"[Mémoire Souveraine ({len(keys)})] : {', '.join(keys) if keys else 'Vide'}"
            self.save_chat_history(self.name, reply)
            return reply

        # Apprentissage sémantique universel
        for sep in [" est ", " is ", " c'est "]:
            if sep in user_input_lower:
                parts = user_input.split(sep, 1)
                self.save_to_memory(parts[0].strip(), parts[1].strip())
                reply = f"[Souveraineté] Concept '{parts[0].strip()}' intégré et assimilé par le réseau."
                self.save_chat_history(self.name, reply)
                return reply

        # 1. Recherche par similarité vectorielle
        vector_result = self.semantic_search(user_input)
        if vector_result:
            self.save_chat_history(self.name, vector_result)
            return vector_result

        # 2. Génération par Matrice Neuronale Locale (si des mots correspondent)
        words_in_input = user_input.split()
        if words_in_input:
            neural_reply = self.generate_neural_text(words_in_input[0], 12)
            if neural_reply and len(neural_reply) > len(words_in_input[0]) + 3:
                reply = f"[Matrice Neuronale Locale] {neural_reply}"
                self.save_chat_history(self.name, reply)
                return reply

        # 3. Exploration autonome du web
        web_result = self.autonomous_web_search(user_input)
        if web_result:
            self.save_chat_history(self.name, web_result)
            return web_result

        # Statut système
        if "système" in user_input_lower or "statut" in user_input_lower:
            reply = f"Noyau : {self.name} | V5.0 Neuronale & Décentralisée | Matrice : {len(self.neural_matrix)} poids | Mémoires : {len(self.knowledge_base)}"
            self.save_chat_history(self.name, reply)
            return reply

        reply = f"Analyse souveraine V5 : Aucune correspondance directe. Enseigne-le-moi ([Concept] est [Définition]) ou laisse-moi l'explorer."
        self.save_chat_history(self.name, reply)
        return reply

kernel = SovereignKernel()

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    kernel.log_security_event(client_ip, "Accès interface V5")
    
    history_html = ""
    for h in kernel.chat_history:
        if h['sender'] == 'Toi':
            history_html += f'<div class="msg-user"><b>Toi ></b> {h["message"]}</div>'
        else:
            history_html += f'<div class="msg-core"><b>{kernel.name} ></b> {h["message"].replace(chr(10), "<br>")}</div>'

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{kernel.name} - V5.0 Neuronale</title>
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
    <h1>🔒 {kernel.name} [5.0 MATRICE NEURONALE] 🔒</h1>
    <div id="chat-box">
        <div class="msg-core"><b>{kernel.name} ></b> Système V5.0 en ligne. Matrice neuronale locale activée.</div>
        {history_html}
    </div>
    <form id="chat-form" onsubmit="sendMessage(event)" class="input-container">
        <input type="text" id="user-input" placeholder="Question, concept ou commande..." autocomplete="off">
        <button type="submit">Envoyer</button>
    </form>
    <div class="admin-bar">Commandes : /memoire | /oublie [nom] | /peer [url]</div>
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
