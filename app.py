import streamlit as st
import pandas as pd

# Titre de l'application
st.title("📊 Lecture et affichage d'un fichier Excel")

# Upload du fichier Excel
uploaded_file = st.file_uploader(
    "📂 Choisir un fichier Excel",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(uploaded_file)

        st.success("✅ Fichier chargé avec succès")

        # Affichage du tableau
        st.subheader("📋 Contenu du fichier Excel")
        st.dataframe(df)

        # Informations supplémentaires
        st.subheader("ℹ️ Informations")
        st.write(f"Nombre de lignes : {df.shape[0]}")
        st.write(f"Nombre de colonnes : {df.shape[1]}")

    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
else:
    st.info("⬆️ Veuillez importer un fichier Excel")
