from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import jwt
import datetime
import os
from generer import creer_facture

app = Flask(__name__)
CORS(app)

# === CONFIG SÉCURITÉ (à changer sur Render) ===
SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkeychangeenproduction')
USERNAME = os.environ.get('APP_USERNAME', 'mounir')
PASSWORD = os.environ.get('APP_PASSWORD', '123456')   # Change ce mot de passe !

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == USERNAME and data.get('password') == PASSWORD:
        token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'erreur': 'Identifiants incorrects'}), 401

@app.route('/generer-pdf', methods=['POST'])
def generer_pdf():
    token = request.headers.get('Authorization')
    if not token or not verify_token(token):
        return jsonify({'erreur': 'Accès refusé'}), 401
    data = request.json
    nom_pdf = creer_facture(
        num=data.get('numero'),
        nom=data.get('nom'),
        adr=data.get('adresse'),
        ville=data.get('ville', 'Mila'),
        tel=data.get('telephone', ''),
        articles=data.get('articles', []),
        date_v=data.get('date'),
        ent_nom=data.get('entreprise'),
        ent_adr=data.get('ent_adresse'),
        ent_wa=data.get('ent_whatsapp'),
        ent_imm=data.get('ent_immat'),
        ent_tel=data.get('ent_telephone', '')
    )
    return send_file(nom_pdf, as_attachment=True)

def verify_token(token):
    try:
        jwt.decode(token.replace('Bearer ', ''), SECRET_KEY, algorithms=['HS256'])
        return True
    except:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)