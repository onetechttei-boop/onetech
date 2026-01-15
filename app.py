import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import threading
import time

# ======================
# Initialisation Firebase
# ======================
cred = credentials.Certificate("ttei-a1956-firebase-adminsdk-fbsvc-92f346cb8c.json")

# Vérifie si Firebase n'est pas déjà initialisé
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ttei-a1956-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# Référence à la racine
ref = db.reference('/')

# ======================
# Streamlit
# ======================
st.set_page_config(page_title="Valeurs Firebase en temps réel", layout="wide")
st.title("Valeurs des boutons en temps réel")
valeurs_display = st.empty()

# ======================
# Fonction listener Firebase
# ======================
def firebase_listener(event):
    data = ref.get()
    valeurs_display.markdown("### Données actuelles :")
    for key, value in data.items():
        valeurs_display.markdown(f"- **{key}** : {value}")

# ======================
# Thread pour écouter Firebase
# ======================
def listen_firebase():
    ref.listen(firebase_listener)

listener_thread = threading.Thread(target=listen_firebase, daemon=True)
listener_thread.start()

while True:
    time.sleep(1)
