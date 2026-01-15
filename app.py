import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import threading
import time

# Firebase
cred = credentials.Certificate("ttei-a1956-firebase-adminsdk-fbsvc-92f346cb8c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ttei-a1956-default-rtdb.europe-west1.firebasedatabase.app/'
})
ref = db.reference('/')

# Streamlit
st.set_page_config(page_title="Boutons en temps réel", layout="wide")
st.title("État des boutons en temps réel")
bouton_display = st.empty()

# Listener Firebase
def firebase_listener(event):
    if event.data is None:
        return
    if 'bouton1' in str(event.path):
        bouton_display.markdown("### 🔵 Bouton 1 appuyé")
    elif 'bouton2' in str(event.path):
        bouton_display.markdown("### 🟠 Bouton 2 appuyé")
    else:
        bouton_display.markdown(f"### {event.data}")

# Thread pour écouter Firebase
def listen_firebase():
    ref.listen(firebase_listener)  # <-- Parenthèse fermée ici !

listener_thread = threading.Thread(target=listen_firebase, daemon=True)
listener_thread.start()

# Boucle principale pour garder Streamlit actif
while True:
    time.sleep(1)
