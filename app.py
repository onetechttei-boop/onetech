import streamlit as st
import pandas as pd
import datetime
import os

# ======================
# CONFIGURATION
# ======================
st.set_page_config(page_title="SafeYear 2026", layout="wide")

ADMIN_PASSWORD = "onetech2026"
ACCIDENT_FILE = "accidents.csv"

# ======================
# SESSION
# ======================
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ======================
# TITRE
# ======================
st.markdown(
    """
    <h1 style='text-align: center;'>
        <span style='color: blue;'>ONE</span><span style='color: orange;'>TECH</span>
    </h1>
    """,
    unsafe_allow_html=True
)

st.subheader("🚨 Suivi des accidents - SafeYear 2026")

# ======================
# DATES
# ======================
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# ======================
# CALENDRIER 2026
# ======================
@st.cache_data
def create_calendar():
    dates = pd.date_range("2026-01-01", "2026-12-31")
    df = pd.DataFrame({"Date": dates})
    df["Accident"] = False
    return df

df = create_calendar()
df = df[df["Date"] <= pd.Timestamp(yesterday)]

# ======================
# CHARGER ACCIDENTS
# ======================
def load_accidents():
    if os.path.exists(ACCIDENT_FILE):
        return pd.read_csv(ACCIDENT_FILE, parse_dates=["date"])
    return pd.DataFrame(columns=["date", "description"])

accidents_df = load_accidents()

# Appliquer accidents au calendrier
for _, row in accidents_df.iterrows():
    df.loc[df["Date"] == row["date"], "Accident"] = True

# ======================
# CALCUL JOURS SANS ACCIDENT
# ======================
def calculate_lta_days(df):
    count = 0
    values = []
    for acc in df["Accident"]:
        if acc:
            count = 0
        else:
            count += 1
        values.append(count)
    df["JoursSansAccident"] = values
    return df

df = calculate_lta_days(df)

# ======================
# DERNIER ACCIDENT
# ======================
if not accidents_df.empty:
    last_accident = accidents_df["date"].max().date()
    last_desc = accidents_df.loc[
        accidents_df["date"] == pd.Timestamp(last_accident),
        "description"
    ].values[0]
    days_since = (yesterday - last_accident).days
else:
    last_accident = None
    last_desc = "Aucun accident enregistré"
    days_since = df["JoursSansAccident"].iloc[-1]

# ======================
# AFFICHAGE DERNIER ACCIDENT
# ======================
st.markdown(
    f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <h3>Dernier accident</h3>
        <h2>{days_since} jours sans accident</h2>
        <p style='color: lightcoral; font-size:18px;'>
            {last_desc}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================
# STATISTIQUES
# ======================
st.subheader("📊 Statistiques globales")

col1, col2 = st.columns(2)
with col1:
    st.metric("Jours sans accident depuis le 1er janvier", df["JoursSansAccident"].iloc[-1])
with col2:
    st.metric("Total accidents enregistrés", df["Accident"].sum())

st.divider()

# ======================
# CONNEXION ADMIN
# ======================
st.sidebar.header("🔐 Accès Administrateur")

pwd = st.sidebar.text_input("Mot de passe admin", type="password")

if st.sidebar.button("Connexion"):
    if pwd == ADMIN_PASSWORD:
        st.session_state.admin_logged = True
        st.sidebar.success("Connexion réussie ✅")
    else:
        st.sidebar.error("Mot de passe incorrect ❌")

# ======================
# AJOUT ACCIDENT (ADMIN)
# ======================
if st.session_state.admin_logged:
    st.sidebar.divider()
    st.sidebar.header("📌 Ajouter un accident")

    new_date = st.sidebar.date_input(
        "Date de l'accident",
        max_value=yesterday
    )

    new_desc = st.sidebar.text_area("Description")

    if st.sidebar.button("Enregistrer"):
        new_row = pd.DataFrame([{
            "date": new_date,
            "description": new_desc
        }])

        accidents_df = pd.concat([accidents_df, new_row], ignore_index=True)
        accidents_df.to_csv(ACCIDENT_FILE, index=False)

        st.sidebar.success("Accident enregistré 💾")
        st.rerun()

# ======================
# CALENDRIER
# ======================
st.subheader("📅 Calendrier")

months = df["Date"].dt.month.unique()

for m in months:
    month_df = df[df["Date"].dt.month == m]
    month_name = month_df["Date"].dt.strftime("%B %Y").iloc[0]

    st.markdown(f"### {month_name}")

    table = pd.DataFrame({
        "Jour": month_df["Date"].dt.day,
        "Accident": month_df["Accident"].map(lambda x: "🔴" if x else "🟢"),
        "Jours sans accident": month_df["JoursSansAccident"]
    })

    st.table(table)
