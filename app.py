import streamlit as st
import pandas as pd
import os

# Titre
st.title("📊 Affichage du fichier incident.xlsx")

# Nom du fichier Excel (dans le même dossier)
FILE_NAME = "incident.xlsx"

# Vérifier si le fichier existe
if os.path.exists(FILE_NAME):
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(FILE_NAME)

        st.success("✅ Fichier incident.xlsx chargé avec succès")

        # Affichage du tableau
        st.subheader("📋 Contenu du fichier Excel")
        st.dataframe(df, use_container_width=True)

        # Infos
        st.subheader("ℹ️ Informations")
        st.write("Nombre de lignes :", df.shape[0])
        st.write("Nombre de colonnes :", df.shape[1])

    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
else:
    st.error("❌ Le fichier incident.xlsx est introuvable dans le dossier")
