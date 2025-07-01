from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import logging
import uuid
import base64
import io
import threading
import sys

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Sémaphore pour limiter les générations concurrentes
generation_semaphore = threading.Semaphore(3)

def generate_pattern(sides, depth, size, angle, color):
    """Génère un motif via un sous-processus isolé"""
    try:
        # Créer un fichier temporaire pour les paramètres
        param_file = f"params_{uuid.uuid4()}.json"
        with open(param_file, 'w') as f:
            json.dump({
                "sides": sides,
                "depth": depth,
                "size": size,
                "angle": angle,
                "color": color
            }, f)
        
        # Configuration des flags selon l'OS
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        
        # Lancer le sous-processus
        result = subprocess.run(
            ['python', 'turtle_worker.py', param_file],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=creationflags
        )
        
        if result.returncode != 0:
            raise Exception(f"Erreur génération: {result.stderr}")
        
        # Lire l'image générée
        if not os.path.exists('output.png'):
            raise Exception("Fichier de sortie non généré")
            
        with open('output.png', 'rb') as img_file:
            return io.BytesIO(img_file.read())
            
    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        raise
    finally:
        # Nettoyage
        if os.path.exists(param_file):
            os.remove(param_file)
        if os.path.exists('output.png'):
            os.remove('output.png')

@app.route("/api/generate", methods=['POST', 'OPTIONS'])
def generate_endpoint():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        # Validation des paramètres
        sides = max(3, min(12, int(data.get("sides", 5))))
        depth = max(1, min(50, int(data.get("depth", 10))))
        size = max(10, min(300, int(data.get("size", 100))))
        angle = max(0, min(360, float(data.get("angle", 20))))
        color = data.get("color", "#0070f3")
        
        # Génération de l'image avec limitation de concurrence
        with generation_semaphore:
            img_io = generate_pattern(sides, depth, size, angle, color)
        
        # Convertir en base64 pour le frontend
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return jsonify({
            "image": f"data:image/png;base64,{img_base64}",
            "params": data
        })
        
    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route("/api/forme_geo", methods=['GET'])
def home_endpoint():
    return jsonify({
        "message": "Bienvenue sur le générateur de motifs géométriques !",
        "peoples": ["Jean", "Pierre", "Jacques", "Paul"],
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080, threaded=True)
