import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# ======================
# Initialisation Firebase
# ======================
cred = credentials.Certificate("ttei-a1956-firebase-adminsdk-fbsvc-92f346cb8c.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ttei-a1956-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# Référence à la base
ref = db.reference('/')  # racine de la DB

# ======================
# Streamlit
# ======================
st.set_page_config(page_title="Valeurs boutons", layout="wide")
st.title("Valeurs des boutons")

# Lire les valeurs dans Firebase
data = ref.get()

# Afficher les valeurs
if data:
    for key, value in data.items():
        st.write(f"{key} : {value}")
else:
    st.write("Pas de données dans Firebase")
