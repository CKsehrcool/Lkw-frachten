import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="LKW Frachten - Tarifdaten Upload", layout="wide")
st.title("📦 LKW-Frachtenrechner – Tarifdaten Upload")

st.markdown("""
Laden Sie hier Ihre eigene Tarifdatei hoch. Die Datei muss im Excel-Format (.xlsx) vorliegen 
und mindestens folgende Tabellenblätter enthalten:

- `GWK`: Gewichtsklassen und Tarife
- `Zoneneinteilung`: PLZ-Zuordnung zu Zonen

Die Datei wird nur temporär verwendet und nicht gespeichert.
""")

uploaded_file = st.file_uploader("🔼 Tarifdatei hochladen (Excel .xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df_dict = pd.read_excel(uploaded_file, sheet_name=None)

        required_sheets = ["GWK", "Zoneneinteilung"]
        missing_sheets = [sheet for sheet in required_sheets if sheet not in df_dict]

        if missing_sheets:
            st.error(f"Die Datei fehlt folgende notwendige Tabellenblätter: {', '.join(missing_sheets)}")
        else:
            st.success("Datei erfolgreich geladen.")

            df_gwk = df_dict["GWK"]
            df_zonen = df_dict["Zoneneinteilung"]

            st.subheader("📄 Vorschau Tarifblatt 'GWK'")
            st.dataframe(df_gwk.head())

            st.subheader("📄 Vorschau Zoneneinteilung")
            st.dataframe(df_zonen.head())

            st.session_state["tarif_gwk"] = df_gwk
            st.session_state["tarif_zonen"] = df_zonen

            st.success("Die Tarifdaten wurden für die Sitzung gespeichert und können nun im Rechner verwendet werden.")

            # Beispiel für direkte Verwendung im Rechner:
            st.header("📦 Beispielhafte Berechnung")
            land = st.selectbox("Land wählen", df_zonen["Land"].unique())
            plz = st.selectbox("2-stellige PLZ wählen", df_zonen[df_zonen["Land"] == land]["PLZ_2"].unique())
            gewicht = st.number_input("Gewicht (kg)", min_value=0.0, value=10.0)

            zone = df_zonen[(df_zonen["Land"] == land) & (df_zonen["PLZ_2"] == plz)]["Zone"].values[0]

            # Spalte mit passender Gewichtsstufe ermitteln
            df_gwk_sorted = df_gwk.copy()
            df_gwk_sorted["Gewicht_kg"] = df_gwk_sorted["GW"].str.extract(r'(\d+)').astype(float)
            df_gwk_sorted = df_gwk_sorted.sort_values("Gewicht_kg")

            passende_stufe = df_gwk_sorted[df_gwk_sorted["Gewicht_kg"] >= gewicht].iloc[0]
            preis = passende_stufe[f"Z{int(zone):02d}"]

            st.success(f"Versandpreis: {preis} EUR für Zone Z{int(zone):02d} bei {gewicht} kg")

    except Exception as e:
        st.error(f"Fehler beim Einlesen der Datei: {e}")
else:
    st.info("Bitte laden Sie eine Tarifdatei hoch, um fortzufahren.")
