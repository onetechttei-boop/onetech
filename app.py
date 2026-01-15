import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import threading
import time

# ======================
# Initialisation Firebase
# ======================
cred = credentials.Certificate("ttei-a1956-firebase-adminsdk-fbsvc-92f346cb8c.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ttei-a1956-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Référence à la racine ou à un chemin spécifique
ref = db.reference('/')

# ======================
# Variables Streamlit
# ======================
st.set_page_config(page_title="Boutons en temps réel", layout="wide")
st.title("État des boutons en temps réel")

# Zone où on affichera le dernier bouton appuyé
bouton_display = st.empty()

# ======================
# Fonction listener Firebase
# ======================
def firebase_listener(event):
    """
    Cette fonction sera appelée à chaque changement dans Firebase
    """
    if event.data is None:
        return

    # Exemple : si tu as /bouton1 ou /bouton2 dans Firebase
    if 'bouton1' in str(event.path):
        bouton_display.markdown("### 🔵 Bouton 1 appuyé")
    elif 'bouton2' in str(event.path):
        bouton_display.markdown("### 🟠 Bouton 2 appuyé")
    else:
        bouton_display.markdown(f"### {event.data}")

# ======================
# Thread pour écouter Firebase
# ======================
def listen_firebase():
    ref.listen(firebase_listen_
