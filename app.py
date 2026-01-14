import streamlit as st
import pandas as pd
import datetime
import os

# ======================
# Configuration page
# ======================
st.set_page_config(page_title="SafeYear 2026", layout="wide")

# ======================
# Titre ONETECH
# ======================
st.markdown(
    """
    <h1 style='text-align: center;'>
        <span style='color: blue;'>ONE</span><span style='color: orange;'>TECH</span>
    </h1>
    """,
    unsafe_allow_html=True
)

st.subheader("🚨 Suivi des accidents de travail")

# ======================
# Dates utiles
# ======================
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# ======================
# 🔎 Lecture du dernier accident depuis Excel
# ======================
@st.cache_data
def read_last_accident_from_excel():
    file_path = "incident.xlsx"

    if not os.path.exists(file_path):
        st.error("❌ Fichier inciden.xlsx introuvable")
        st.stop()

    df_excel = pd.read_excel(file_path, header=None)
    df_excel = df_excel.dropna(how="all")

    if df_excel.empty:
        st.error("❌ Le fichier inciden.xlsx est vide")
        st.stop()

    last_row = df_excel.iloc[-1]

    day = int(last_row[0])    # Colonne A
    month = int(last_row[1])  # Colonne B
    year = int(last_row[2])   # Colonne C

    last_date = datetime.date(year, month, day)

    if last_date > yesterday:
        st.error("❌ La date du dernier accident est dans le futur")
        st.stop()

    return last_date

last_accident_date = read_last_accident_from_excel()

# ======================
# Description accident
# ======================
last_accident_desc = (
    "Dernier accident enregistré automatiquement depuis le fichier Excel."
)

# ======================
# Création calendrier annuel
# ======================
@st.cache_data
def create_calendar():
    start_date = datetime.date(2026, 1, 1)
    end_date = datetime.date(2026, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date)
    df = pd.DataFrame(dates, columns=["Date"])
    df["Accident"] = False
    return df

df = create_calendar()

# Limiter jusqu'à hier
df = df[df["Date"] <= pd.Timestamp(yesterday)]

# ======================
# ⛔ Marquer le dernier accident dans le calendrier
# ======================
df.loc[df["Date"] == pd.Timestamp(last_accident_date), "Accident"] = True

# ======================
# Sidebar – ajout manuel d'accident
# ======================
st.sidebar.header("📌 Enregistrer un accident")

date_accident = st.sidebar.date_input(
    "Date de l'accident",
    value=yesterday,
    max_value=yesterday
)

if st.sidebar.button("Ajouter accident"):
    df.loc[df["Date"] == pd.Timestamp(date_accident), "Accident"] = True
    st.sidebar.success(f"Accident ajouté pour {date_accident}")

# ======================
# Calcul jours consécutifs sans accident
# ======================
def calculate_lta_days(df):
    count = 0
    values = []

    for accident in df["Accident"]:
        if accident:
            count = 0
        else:
            count += 1
        values.append(count)

    df["JoursSansAccident"] = values
    return df

df = calculate_lta_days(df)

# ======================
# Calcul jours depuis dernier accident
# ======================
days_since_last_accident = (yesterday - last_accident_date).days

# ======================
# Affichage dernier accident
# ======================
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h3>Dernier accident ({last_accident_date.strftime('%d/%m/%Y')})</h3>
        <h2>{days_since_last_accident} jours sans accident</h2>
        <p style='font-size:18px; color: lightcoral; font-weight:bold;'>
            {last_accident_desc}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================
# Statistiques globales
# ======================
st.subheader("📊 Statistiques globales (du 1er janvier jusqu'à hier)")

total_days_without_accident = df["JoursSansAccident"].iloc[-1]
total_accidents = df["Accident"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Jours sans accident depuis le dernier accident",
        total_days_without_accident
    )

with col2:
    st.metric(
        "Total d'accidents enregistrés",
        total_accidents
    )

st.divider()

# ======================
# Calendrier
# ======================
st.subheader("📅 Calendrier (du 1er janvier jusqu'à hier)")

months = df["Date"].dt.month.unique()

for month in months:
    month_name = df[df["Date"].dt.month == month]["Date"].dt.strftime("%B %Y").iloc[0]
    st.markdown(f"### {month_name}")

    month_df = df[df["Date"].dt.month == month]

    display_df = pd.DataFrame({
        "Jour": month_df["Date"].dt.day,
        "Accident": month_df["Accident"].map(lambda x: "🔴" if x else "🟢"),
        "Jours consécutifs sans accident": month_df["JoursSansAccident"]
    })

    st.table(display_df)
