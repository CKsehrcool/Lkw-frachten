import streamlit as st
from utils import calculate_freight
import pandas as pd

st.title("Frachtenrechner für LKW-Transporte")

land = st.selectbox("Land", ["DE", "AT", "BE", "CZ", "DK", "FR", "LU", "NL", "PL", "CH",
    "GB", "NO", "CY", "EE", "ES", "FI", "GR", "HR", "HU", "IE", "IS",
    "IT", "LT", "PT", "RO", "SE", "SK", "SL"])
plz = st.text_input("PLZ (2-stellig) / GB 1 oder 2-stellig", max_chars=2)
gewicht = st.number_input("Gewicht (kg)", min_value=1, step=1)

if st.button("Berechnen"):
    if plz and len(plz) <= 2:
        result = calculate_freight(land, plz, gewicht)
        st.markdown(f"**Frachtkosten:** {result['rate']}")
        st.markdown(f"**Verwendeter Tariftyp:** {result['type']}")
    else:
        st.error("Bitte eine gültige 2-stellige PLZ eingeben.")

# Zusatzdaten direkt aus Hauptverzeichnis laden
@st.cache_data
def load_nk_data():
    df1 = pd.read_excel("nk.xlsx", sheet_name=0)
    df2 = pd.read_excel("nk.xlsx", sheet_name=1)
    return df1, df2

df_zustell, df_neben = load_nk_data()

# Filter nach Land
zustell_filtered = df_zustell[df_zustell["Land"] == land].copy()
neben_filtered = df_neben[df_neben["Land"] == land].copy()

# Formatierung der Kosten-Spalten als Euro
if "Kosten" in zustell_filtered.columns:
    zustell_filtered["Kosten"] = zustell_filtered["Kosten"].apply(
        lambda x: f"{x:.2f} €" if pd.notna(x) and isinstance(x, (float, int)) else x
    )
if "Kosten" in neben_filtered.columns:
    neben_filtered["Kosten"] = neben_filtered["Kosten"].apply(
        lambda x: f"{x:.2f} €" if pd.notna(x) and isinstance(x, (float, int)) else x
    )

st.subheader("Zustelloptionen")
if not zustell_filtered.empty:
    st.table(zustell_filtered[["Zustelloption", "Kosten", "Bemerkung"]].reset_index(drop=True))
else:
    st.markdown("_Keine Daten verfügbar._")

st.subheader("Sonstige Nebenkosten")
if not neben_filtered.empty:
    st.table(neben_filtered[["sonstige Nebenkosten", "Kosten", "Bemerkung"]].reset_index(drop=True))
else:
    st.markdown("_Keine Daten verfügbar._")
