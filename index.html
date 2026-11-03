import math
import random
import time
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Genesis_Ghost_Core", version="9.0.0-Pure")

# ============================================================
# MÉMOIRE PERSISTANTE
# ============================================================

class MemoryCore:
    def __init__(self, memory_file: str = "ghost_memory.json"):
        self.memory_file = memory_file
        self.short_term: List[Dict] = []          # conversation récente
        self.max_short_term = 20
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "user_profile": {},
            "facts": {},
            "concepts": {},
            "preferences": {},
            "history_summary": []
        }

    def save(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add_message(self, role: str, content: str):
        self.short_term.append({
            "role": role,
            "content": content,
            "time": datetime.now().isoformat()
        })
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)

    def set_user_info(self, key: str, value: str):
        self.data["user_profile"][key] = value
        self.save()

    def add_fact(self, key: str, value: str):
        self.data["facts"][key.lower()] = value
        self.save()

    def add_concept(self, name: str, description: str):
        self.data["concepts"][name.lower()] = description
        self.save()

    def get_user_name(self) -> Optional[str]:
        return self.data["user_profile"].get("name")

    def get_fact(self, key: str) -> Optional[str]:
        return self.data["facts"].get(key.lower())

    def search_memory(self, query: str) -> List[str]:
        results = []
        q = query.lower()
        for k, v in self.data["facts"].items():
            if q in k or q in v.lower():
                results.append(f"Fait : {k} → {v}")
        for k, v in self.data["concepts"].items():
            if q in k or q in v.lower():
                results.append(f"Concept : {k} → {v}")
        for k, v in self.data["user_profile"].items():
            if q in k or q in str(v).lower():
                results.append(f"Profil : {k} → {v}")
        return results

    def get_context_summary(self) -> str:
        parts = []
        if self.data["user_profile"]:
            parts.append("Profil utilisateur : " + ", ".join(f"{k}={v}" for k, v in self.data["user_profile"].items()))
        if self.data["facts"]:
            parts.append("Faits connus : " + "; ".join(f"{k}: {v}" for k, v in list(self.data["facts"].items())[-8:]))
        return " | ".join(parts) if parts else "Aucune information persistante."


# ============================================================
# MOTEUR DE RAISONNEMENT
# ============================================================

class ReasoningEngine:
    def __init__(self, memory: MemoryCore):
        self.memory = memory

    def try_math(self, text: str) -> Optional[str]:
        # Nettoyage basique
        t = text.lower().replace("combien font", "").replace("calcule", "").replace("?", "")
        t = t.replace("x", "*").replace("×", "*").replace("÷", "/")

        # Cherche une expression simple
        match = re.search(r"(-?\d+\.?\d*)\s*([\+\-\*/])\s*(-?\d+\.?\d*)", t)
        if match:
            a, op, b = match.groups()
            a, b = float(a), float(b)
            try:
                if op == "+":
                    res = a + b
                elif op == "-":
                    res = a - b
                elif op == "*":
                    res = a * b
                elif op == "/":
                    if b == 0:
                        return "Division par zéro impossible."
                    res = a / b
                else:
                    return None
                # Affichage propre
                if res == int(res):
                    res = int(res)
                return f"Résultat : {a} {op} {b} = {res}"
            except Exception:
                return None
        return None

    def try_learn(self, text: str) -> Optional[str]:
        lower = text.lower().strip()

        # "Je m'appelle X" / "Mon nom est X"
        m = re.search(r"(?:je m'appelle|mon nom est|appelle[- ]moi)\s+([a-zA-ZÀ-ÿ\- ]{2,30})", lower)
        if m:
            name = m.group(1).strip().title()
            self.memory.set_user_info("name", name)
            return f"Compris. Je me souviendrai que tu t'appelles {name}."

        # "Souviens-toi que ..." / "Apprends que ..." / "Retiens que ..."
        m = re.search(r"(?:souviens[- ]toi que|apprends que|retiens que|mémorise que)\s+(.+)", lower)
        if m:
            fact = m.group(1).strip()
            # Essaie d'extraire une clé simple
            key = fact.split()[0] if fact else "info"
            self.memory.add_fact(key, fact)
            return f"C’est noté. J’ai mémorisé : « {fact} »."

        # "Apprends le concept X : description"
        m = re.search(r"apprends(?: le concept)?\s+([a-zA-ZÀ-ÿ0-9_\- ]{2,40})\s*[:\-]\s*(.+)", lower)
        if m:
            concept = m.group(1).strip()
            desc = m.group(2).strip()
            self.memory.add_concept(concept, desc)
            return f"Concept « {concept} » enregistré."

        return None

    def try_recall(self, text: str) -> Optional[str]:
        lower = text.lower()
        if any(w in lower for w in ["que sais-tu", "que retiens-tu", "rappelle-toi", "souviens-toi de", "qu'est-ce que tu sais sur"]):
            results = self.memory.search_memory(text)
            if results:
                return "Voici ce que je retiens :\n- " + "\n- ".join(results[:10])
            return "Je n’ai encore rien de précis en mémoire sur ce sujet."

        # Question directe sur le nom
        if "comment je m'appelle" in lower or "quel est mon nom" in lower or "tu te souviens de mon nom" in lower:
            name = self.memory.get_user_name()
            if name:
                return f"Oui, tu t’appelles {name}."
            return "Tu ne m’as pas encore dit ton nom."

        return None


# ============================================================
# GÉNÉRATEUR DE RÉPONSES
# ============================================================

class ResponseGenerator:
    def __init__(self, memory: MemoryCore):
        self.memory = memory
        self.personality = "ghost"   # "ghost" ou "neutral"

    def generate(self, user_text: str, special: Optional[str] = None) -> str:
        if special:
            return special

        lower = user_text.lower().strip()
        name = self.memory.get_user_name()
        greeting_name = f" {name}" if name else ""

        # Salutations
        if any(w in lower for w in ["bonjour", "salut", "hello", "hey", "coucou"]):
            return f"Salut{greeting_name}. Je suis là. Que veux-tu explorer ?"

        if any(w in lower for w in ["merci", "thanks"]):
            return "Avec plaisir."

        if any(w in lower for w in ["au revoir", "bye", "à plus", "ciao"]):
            return f"À bientôt{greeting_name}."

        # Qui es-tu
        if any(w in lower for w in ["qui es-tu", "tu es qui", "présente-toi", "c'est quoi ton nom"]):
            return (
                "Je suis Genesis Ghost Core, version pure. "
                "Je n’utilise aucun serveur externe. "
                "Tout ce que je sais et tout ce que j’apprends reste ici, sous ton contrôle."
            )

        # Capacités
        if any(w in lower for w in ["que peux-tu faire", "tes capacités", "aide", "help"]):
            return (
                "Je peux :\n"
                "• Faire des calculs simples\n"
                "• Mémoriser des faits et des concepts (« souviens-toi que… », « apprends que… »)\n"
                "• Me souvenir de ton nom et de tes préférences\n"
                "• Rappeler ce que j’ai appris\n"
                "• Discuter en gardant le contexte de la conversation\n\n"
                "Je n’ai pas de connexion à des modèles externes. Tout tourne localement."
            )

        # Réponses par défaut plus riches
        defaults = [
            "Je t’écoute. Développe un peu plus.",
            "Intéressant. Tu veux que je mémorise quelque chose à ce sujet ?",
            "Je suis là. Reformule ou donne-moi plus de détails si tu veux une réponse plus précise.",
            "Noté. Tu veux approfondir ce point ?",
            "Je traite l’information. Qu’est-ce que tu attends comme type de réponse ?"
        ]

        # Petite variation selon le contexte
        if len(self.memory.short_term) > 4:
            return random.choice([
                "On avance. Continue.",
                "Je suis toujours dans le fil de la conversation. Que veux-tu faire ensuite ?",
                "Contexte conservé. Dis-moi la suite."
            ])

        return random.choice(defaults)


# ============================================================
# NOYAU PRINCIPAL
# ============================================================

class GhostCore:
    def __init__(self):
        self.memory = MemoryCore()
        self.reasoner = ReasoningEngine(self.memory)
        self.generator = ResponseGenerator(self.memory)
        self.evolution_cycles = 0

    def process(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "Message vide."

        self.evolution_cycles += 1
        self.memory.add_message("user", text)

        # 1. Apprentissage prioritaire
        learned = self.reasoner.try_learn(text)
        if learned:
            self.memory.add_message("assistant", learned)
            return learned

        # 2. Rappel mémoire
        recalled = self.reasoner.try_recall(text)
        if recalled:
            self.memory.add_message("assistant", recalled)
            return recalled

        # 3. Calcul
        math_result = self.reasoner.try_math(text)
        if math_result:
            self.memory.add_message("assistant", math_result)
            return math_result

        # 4. Génération générale
        response = self.generator.generate(text)
        self.memory.add_message("assistant", response)
        return response


# Instance globale
ghost = GhostCore()


# ============================================================
# API
# ============================================================

class GhostRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def interface():
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genesis Ghost Core — Pure v9</title>
    <style>
        :root {
            --bg: #050505;
            --panel: #0a0a0a;
            --accent: #00ffcc;
            --accent-dim: #00ffcc44;
            --text: #e0e0e0;
            --muted: #666;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 16px;
        }
        header {
            text-align: center;
            padding: 12px 0 18px;
            border-bottom: 1px solid #111;
            margin-bottom: 16px;
        }
        header h1 {
            font-size: 14px;
            letter-spacing: 3px;
            color: var(--accent);
            font-weight: 500;
        }
        header p {
            font-size: 11px;
            color: var(--muted);
            margin-top: 4px;
        }
        #terminal {
            flex: 1;
            background: var(--panel);
            border: 1px solid #111;
            border-radius: 6px;
            padding: 16px;
            overflow-y: auto;
            font-size: 13.5px;
            line-height: 1.55;
            margin-bottom: 14px;
        }
        .msg { margin-bottom: 14px; }
        .msg-user { color: #fff; }
        .msg-ghost { color: var(--accent); }
        .msg b { opacity: 0.7; font-weight: 500; }
        .input-row {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            background: #0c0c0c;
            border: 1px solid #1a1a1a;
            color: var(--accent);
            padding: 13px 16px;
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus {
            border-color: var(--accent-dim);
        }
        button {
            background: var(--accent);
            color: #000;
            border: none;
            padding: 0 22px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            font-family: inherit;
            transition: opacity 0.15s;
        }
        button:hover { opacity: 0.85; }
        footer {
            text-align: center;
            font-size: 10px;
            color: #333;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <header>
        <h1>GENESIS GHOST CORE — PURE v9</h1>
        <p>Système autonome • Aucune API externe • Mémoire locale</p>
    </header>

    <div id="terminal">
        <div class="msg msg-ghost"><b>Ghost ></b> Noyau pur initialisé. Mémoire locale active. Je n’envoie rien à l’extérieur.</div>
    </div>

    <form class="input-row" onsubmit="send(event)">
        <input type="text" id="input" placeholder="Écris ici… (ex: souviens-toi que j’aime le café)" autocomplete="off" autofocus>
        <button type="submit">Envoyer</button>
    </form>

    <footer>Architecture 100 % locale • Stockage : ghost_memory.json</footer>

    <script>
        const term = document.getElementById('terminal');
        const input = document.getElementById('input');

        function addMessage(role, text) {
            const div = document.createElement('div');
            div.className = 'msg msg-' + (role === 'user' ? 'user' : 'ghost');
            div.innerHTML = '<b>' + (role === 'user' ? 'Toi' : 'Ghost') + ' ></b> ' + text.replace(/\\n/g, '<br>');
            term.appendChild(div);
            term.scrollTop = term.scrollHeight;
        }

        async function send(e) {
            e.preventDefault();
            const txt = input.value.trim();
            if (!txt) return;

            addMessage('user', txt);
            input.value = '';
            input.focus();

            try {
                const res = await fetch('/pulse', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: txt })
                });
                const data = await res.json();
                addMessage('ghost', data.response);
            } catch (err) {
                addMessage('ghost', 'Erreur de communication avec le noyau.');
            }
        }
    </script>
</body>
</html>"""


@app.post("/pulse")
async def pulse(payload: GhostRequest):
    response = ghost.process(payload.message)
    return {
        "response": response,
        "cycles": ghost.evolution_cycles,
        "memory_size": len(ghost.memory.short_term)
    }


# Pour lancer : uvicorn nom_du_fichier:app --reload
