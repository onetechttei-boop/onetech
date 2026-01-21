import streamlit as st
import pandas as pd
import datetime
import os

# ======================
# CONFIGURATION
# ======================
st.set_page_config(page_title="SafeYear 2026", layout="wide")

ADMIN_PASSWORD = "onetech2026"
ACCIDENT_FILE = "accidentss.csv"

# ======================
# SESSION
# ======================
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ======================
# TITRE
# ======================
st.title("🔵 ONE🟠TECH")
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
        df = pd.read_csv(ACCIDENT_FILE)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        return df
    return pd.DataFrame(columns=["date", "description"])

accidents_df = load_accidents()

# ======================
# APPLIQUER ACCIDENTS
# ======================
for _, row in accidents_df.iterrows():
    if pd.notna(row["date"]):
        df.loc[df["Date"] == row["date"], "Accident"] = True

# ======================
# CALCUL JOURS SANS ACCIDENT
# ======================
count = 0
jours_sans_accident = []

for acc in df["Accident"]:
    if acc:
        count = 0
    else:
        count += 1
    jours_sans_accident.append(count)

df["JoursSansAccident"] = jours_sans_accident

# ======================
# DERNIER ACCIDENT
# ======================
if not accidents_df.empty and accidents_df["date"].notna().any():
    last_accident_ts = accidents_df["date"].dropna().max()
    last_accident_date = last_accident_ts.date()
    last_accident_text = last_accident_date.strftime("%d/%m/%Y")

    last_desc = accidents_df.loc[
        accidents_df["date"] == last_accident_ts,
        "description"
    ].values[0]

    days_since = (yesterday - last_accident_date).days
else:
    last_accident_text = "—"
    last_desc = "Aucun accident enregistré"
    days_since = df["JoursSansAccident"].iloc[-1]

# ======================
# AFFICHAGE DERNIER ACCIDENT (SIMPLE)
# ======================
st.subheader("Dernier accident")
st.caption(f"📅 Date : {last_accident_text}")
st.metric("Jours sans accident", days_since)
st.write(f"📝 {last_desc}")

st.divider()

# ======================
# STATISTIQUES
# ======================
st.subheader("📊 Statistiques globales")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Jours sans accident depuis le 1er janvier",
        df["JoursSansAccident"].iloc[-1]
    )

with col2:
    st.metric(
        "Total d'accidents enregistrés",
        df["Accident"].sum()
    )

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
# GESTION DES ACCIDENTS
# ======================
if st.session_state.admin_logged:
    st.sidebar.divider()
    st.sidebar.header("📌 Gestion des accidents")

    # AJOUT
    st.sidebar.subheader("Ajouter un accident")
    new_date = st.sidebar.date_input(
        "Date de l'accident",
        min_value=datetime.date(2026, 1, 1),
        max_value=yesterday
    )
    new_desc = st.sidebar.text_area("Description")

    if st.sidebar.button("Enregistrer"):
        new_row = pd.DataFrame([{
            "date": pd.to_datetime(new_date),
            "description": new_desc
        }])
        accidents_df = pd.concat([accidents_df, new_row], ignore_index=True)
        accidents_df.to_csv(ACCIDENT_FILE, index=False)
        st.sidebar.success("Accident enregistré 💾")
        st.rerun()

    st.sidebar.divider()

    # SUPPRESSION
    st.sidebar.subheader("Supprimer un accident")

    if not accidents_df.empty:
        options = accidents_df.apply(
            lambda x: f"{x['date'].date()} - {x['description']}", axis=1
        ).tolist()

        to_delete = st.sidebar.selectbox("Choisir", options)

        if st.sidebar.button("Supprimer"):
            index = options.index(to_delete)
            accidents_df = accidents_df.drop(index)
            accidents_df.to_csv(ACCIDENT_FILE, index=False)
            st.sidebar.success("Accident supprimé ✅")
            st.rerun()

# ======================
# CALENDRIER
# ======================
st.subheader("📅 Calendrier")

for month in df["Date"].dt.month.unique():
    month_df = df[df["Date"].dt.month == month]
    month_name = month_df["Date"].dt.strftime("%B %Y").iloc[0]

    st.markdown(f"### {month_name}")

    st.table(pd.DataFrame({
        "Jour": month_df["Date"].dt.day,
        "Accident": month_df["Accident"].map(lambda x: "🔴" if x else "🟢"),
        "Jours sans accident": month_df["JoursSansAccident"]
    }))
