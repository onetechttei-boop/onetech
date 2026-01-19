# afficher_accidents.py
import streamlit as st
import pandas as pd
import os

# ======================
# CONFIGURATION
# ======================
st.set_page_config(page_title="Accidents CSV", layout="wide")
ACCIDENT_FILE = "accidentss.csv"

# ======================
# TITRE
# ======================
st.title("📋 Visualisation des accidents")

# ======================
# CHARGER ET AFFICHER LE CSV
# ======================
if os.path.exists(ACCIDENT_FILE):
    df = pd.read_csv(ACCIDENT_FILE)
    st.subheader("Tableau des accidents")
    st.dataframe(df)  # Affiche le tableau
else:
    st.warning(f"Le fichier {ACCIDENT_FILE} n'existe pas.")
