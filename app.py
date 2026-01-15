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

# Référence à la racine ou chemin spécifique
ref = db.reference('/')  # ou '/boutons' si tes boutons sont sous ce noeud

# ======================
# Streamlit
# ======================
st.set_page_config(page_title="Valeurs Firebase en temps réel", layout="wide")
st.title("Valeurs des boutons en temps réel")

# Zone où on affichera les valeurs
valeurs_display = st.empty()

# ======================
# Fonction listener Firebase
# ======================
def firebase_listener(event):
    """
    Cette fonction est appelée à chaque changement dans Firebase
    """
    # Lire toutes les données à la racine
    data = ref.get()
    valeurs_display.markdown("### Données actuelles :")
    # Afficher les clés et valeurs
    for key, value in data.items():
        valeurs_display.markdown(f"- **{key}** : {value}")

# ======================
# Thread pour écouter Firebase
# ======================
def listen_firebase():
    ref.listen(firebase_listener)  # <-- Parenthèse fermée ici !

# Lancer l'écoute dans un thread séparé
listener_thread = threading.Thread(target=listen_firebase, daemon=True)
listener_thread.start()

# ======================
# Boucle principale Streamlit
# ======================
while True:
    time.sleep(1)
