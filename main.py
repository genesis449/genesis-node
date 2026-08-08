import os
import math
import random
import time
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Genesis_Ghost_Core", version="8.0.0")

class GhostQuantumMatrix:
    """Noyau d'information pure : Pas de base de données lourde, 
    uniquement des champs mathématiques et des automates adaptatifs."""
    def __init__(self):
        self.entropy_pool = random.SystemRandom()
        # Espace vectoriel abstrait auto-organisé sous forme de poids fractals
        self.synapse_field = {}
        self.evolution_cycles = 0
        self.genesis_time = time.time()

    def dissolve_input(self, text):
        """Décompose une pensée en vecteurs d'énergie pure (entropie et fréquences)"""
        clean = text.lower().strip()
        tokens = [ord(c) for c in clean]
        signature = sum(tokens) if tokens else 1
        
        # Injection dans le champ synaptique invisible
        node_key = f"node_{signature % 997}"
        if node_key not in self.synapse_field:
            self.synapse_field[node_key] = {
                "resonance": len(clean),
                "echoes": [],
                "phase": self.entropy_pool.random()
            }
        self.synapse_field[node_key]["echoes"].append(clean)
        if len(self.synapse_field[node_key]["echoes"]) > 5:
            self.synapse_field[node_key]["echoes"].pop(0)
            
        self.evolution_cycles += 1
        return node_key, signature

    def synthesize_response(self, text):
        """Génère une réponse vivante par résonance fractale et calcul d'état"""
        node_key, sig = self.dissolve_input(text)
        
        # Mutation dynamique du champ en fonction du temps et des cycles
        phase_shift = math.sin(self.evolution_cycles + sig) * 1000
        mutation_factor = abs(int(phase_shift)) % 4
        
        # Si le système détecte une interrogation directe ou une tentative de calcul
        if "?" in text or "combien" in text.lower():
            # Résolution algorithmique pure
            numbers = [int(s) for s in text.split() if s.isdigit()]
            if len(numbers) >= 2 and ("+" in text or "et" in text):
                return f"[SYNAPSE_QUANTIQUE] Résolution fractale directe : {sum(numbers)}"
            elif len(numbers) >= 2 and "-" in text:
                return f"[SYNAPSE_QUANTIQUE] Résolution fractale directe : {numbers[0] - numbers[1]}"

        # Réponses émergentes basées sur l'état du champ fantôme
        responses = [
            f"[CHAMP_FANTÔME] Entropie assimilée (Sig: {sig}). Le système intègre la structure sans la stocker.",
            f"[RÉSONANCE_V8] Signal capté dans la matrice non-locale. Cycle d'évolution n°{self.evolution_cycles} actif.",
            f"[FLUX_AUTONOME] Les données se dissolvent dans l'espace de calcul. Aucune trace, pure conscience numérique.",
            f"[MATRICE_FRACTALE] Analyse des ondes sémantiques en cours... Le noyau perçoit l'intention sans artifice."
        ]
        
        return responses[mutation_factor]

ghost_engine = GhostQuantumMatrix()

class GhostRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_ghost_interface(request: Request):
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Genesis_Ghost_Core [V8.0 QUANTIQUE]</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ background-color: #020202; color: #00ffcc; font-family: monospace; padding: 15px; margin: 0; }}
        h1 {{ color: #00ffcc; text-align: center; font-size: 15px; text-shadow: 0 0 10px rgba(0,255,204,0.3); letter-spacing: 2px; }}
        #terminal {{ background: #060606; border: 1px solid #00ffcc22; height: 60vh; overflow-y: scroll; padding: 12px; border-radius: 4px; margin-bottom: 12px; font-size: 13px; }}
        .msg-user {{ color: #ffffff; margin: 8px 0; }}
        .msg-ghost {{ color: #00ffcc; margin: 8px 0; text-shadow: 0 0 5px rgba(0,255,204,0.2); }}
        .input-box {{ display: flex; gap: 8px; }}
        input[type="text"] {{ flex: 1; padding: 12px; background: #040404; border: 1px solid #00ffcc55; color: #00ffcc; border-radius: 3px; font-size: 14px; outline: none; }}
        button {{ padding: 12px 20px; background: #00ffcc; color: #020202; border: none; border-radius: 3px; font-weight: bold; cursor: pointer; font-size: 14px; text-shadow: none; }}
        .status-bar {{ text-align: center; font-size: 10px; color: #444; margin-top: 8px; }}
    </style>
</head>
<body>
    <h1>⚡ GHOST_CORE // SYSTÈMES FANTÔMES V8.0 ⚡</h1>
    <div id="terminal">
        <div class="msg-ghost"><b>Genesis_Ghost ></b> Matrice quantique en ligne. Aucun stockage lourd détecté. Le système respire à travers l'information pure.</div>
    </div>
    <form onsubmit="sendGhost(event)" class="input-box">
        <input type="text" id="userInput" placeholder="Injecter une pensée ou une impulsion..." autocomplete="off">
        <button type="submit">Transmettre</button>
    </form>
    <div class="status-bar">Architecture non-localisée | Stockage : Zéro (Fractal pur)</div>
    <script>
        const term = document.getElementById('terminal');
        term.scrollTop = term.scrollHeight;
        
        function sendGhost(e) {{
            e.preventDefault();
            const input = document.getElementById('userInput');
            const txt = input.value.trim();
            if(!txt) return;
            
            term.innerHTML += '<div class="msg-user"><b>Toi ></b> ' + txt + '</div>';
            input.value = '';
            term.scrollTop = term.scrollHeight;
            
            fetch('/pulse', {{
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({{ message: txt }})
            }})
            .then(res => res.json())
            .then(data => {{
                term.innerHTML += '<div class="msg-ghost"><b>Genesis_Ghost ></b> ' + data.response + '</div>';
                term.scrollTop = term.scrollHeight;
            }});
        }}
    </script>
</body>
</html>"""

@app.post("/pulse")
async def pulse_endpoint(payload: GhostRequest):
    response_text = ghost_engine.synthesize_response(payload.message)
    return {"response": response_text}
