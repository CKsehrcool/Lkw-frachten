import pandas as pd
import os

def load_tariffs(country):
    dtype = {"PLZ_2": str}
    excel_file = "dachser.xlsx" if country != "DE" else "dsv.xlsx"
    sheets = pd.ExcelFile(excel_file).sheet_names
    df = {}
    for sheet in sheets:
        if sheet in ["GWK", "Zonen"]:
            df[sheet] = pd.read_excel(excel_file, sheet_name=sheet, dtype=dtype)
        else:
            df[sheet] = pd.read_excel(excel_file, sheet_name=sheet, dtype=dtype, index_col=0)
    tariftyp = "Dachser" if country != "DE" else "DSV"
    return df, tariftyp

def find_zonenblatt(df):
    for sheet in df:
        if "zone" in sheet.lower():
            return df[sheet]
    return None

def find_gewichtsklasse(gwk_df, weight):
    for gw_id, row in gwk_df.iterrows():
        if row["Von"] <= weight <= row["Bis"]:
            return gw_id, row.get("GW_1"), row.get("GW_komp")
    return None, None, None

def calculate_freight(country, plz, weight):
    df, tariftyp = load_tariffs(country)
    plz_str = str(plz).upper()
    if plz_str.isdigit():
        plz_str = plz_str.zfill(2)

    #plz_str = str(plz).zfill(2)
    zonenblatt = find_zonenblatt(df)
    if zonenblatt is None:
        return {"rate": "Zonenblatt fehlt", "type": tariftyp}

    if "PLZ_2" not in zonenblatt.columns or country not in zonenblatt.columns:
        return {"rate": f"Spalte 'PLZ_2' oder '{country}' fehlt", "type": tariftyp}

    zone_row = zonenblatt[zonenblatt["PLZ_2"] == plz_str]
    if zone_row.empty:
        return {"rate": f"Keine Zone gefunden für PLZ {plz}", "type": tariftyp}
    zone = zone_row[country].values[0]
    if pd.isna(zone):
        return {"rate": f"Zone leer für PLZ {plz}", "type": tariftyp}

    zone_col = f"Z{str(zone).zfill(2)}" if not str(zone).startswith("Z") else str(zone)

    gwk_df_raw = df.get("GWK")
    if gwk_df_raw is None or "GW" not in gwk_df_raw.columns:
        return {"rate": "GWK fehlt oder hat keine Spalte 'GW'", "type": tariftyp}
    gwk_df = gwk_df_raw.set_index("GW")

    gwk_id, gw_next, gw_kom = find_gewichtsklasse(gwk_df, weight)
    if gwk_id is None:
        return {"rate": "Kein Tarif hinterlegt für dieses Gewicht", "type": tariftyp}

    tarifblatt = df.get(country)
    if tarifblatt is None:
        return {"rate": f"Tarifblatt '{country}' fehlt", "type": tariftyp}

    def get_tarif(gw_id):
        try:
            value = tarifblatt.loc[gw_id, zone_col]
            if isinstance(value, str) and "anfrage" in value.lower():
                return value
            return float(value)
        except:
            return None

    normal_rate = get_tarif(gwk_id)
    if normal_rate is None or pd.isna(normal_rate):
        return {"rate": "Kein Tarif hinterlegt für diese Gewichtsstufe", "type": tariftyp}

    if isinstance(normal_rate, str):
        return {"rate": normal_rate, "type": tariftyp}

    result_typ = "Normaler Tarif"
    cost = normal_rate * (weight / 100)

    # 1. Spitze prüfen
    if gw_next and gw_next in gwk_df.index:
        next_row = gwk_df.loc[gw_next]
        next_tarif = get_tarif(gw_next)
        if isinstance(next_tarif, (float, int)):
            if cost > next_tarif * (next_row["Von"] / 100):
                cost = next_tarif * (next_row["Von"] / 100)
                result_typ = "Spitze: nächsthöhere Gewichtsklasse"

    # 2. Mindesttarif
    mindest = get_tarif("G001")
    if isinstance(mindest, (float, int)) and cost < mindest:
        cost = mindest
        result_typ = "Mindesttarif angewendet"

    # 3. Komplettladung
    if gw_kom:
        komplett = get_tarif(gw_kom)
        if isinstance(komplett, (float, int)) and cost > komplett:
            cost = komplett
            result_typ = "Komplettladung"

    return {"rate": f"{cost:.2f} €", "type": f"{result_typ} ({tariftyp})"}
