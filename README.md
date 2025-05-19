# LKW Frachtenrechner

Dies ist ein interaktiver Webrechner für LKW-Frachtkosten basierend auf DSV- und Dachser-Tarifstrukturen inkl. Nebenkostenanzeige. Der Rechner ist für den Einsatz mit Streamlit Cloud vorbereitet und sofort per Weblink nutzbar.

## 🔧 Funktionen

- Auswahl von Land, PLZ (2-stellig) und Gewicht in kg
- Automatische Berechnung des Frachtpreises je nach Zone, Gewichtsklasse, Mindesttarif, Spitze und Komplettladung
- Dynamischer Tarifimport aus Excel-Dateien (DSV, Dachser)
- Anzeige landesspezifischer Zustelloptionen und sonstiger Nebenkosten
- Vollständig in Python / Streamlit realisiert, keine lokalen Installationen nötig

## 📦 Eingabedateien (Excel)

- `dsv.xlsx` – DSV-Tarife für Deutschland
- `dachser.xlsx` – Dachser-Tarife für weitere Länder
- `nk.xlsx` – Zustelloptionen & sonstige Nebenkosten

## ▶️ Live-Demo

Nach dem Deployment über Streamlit Cloud ist die Anwendung z. B. hier erreichbar:

```
https://lkw-frachten.streamlit.app
```

(ggf. durch echten Link ersetzen)

## 🖥️ Lokaler Start

1. Projekt klonen:

```bash
git clone https://github.com/CKsehrcool/lkw_frachten.git
cd lkw_frachten
```

2. Abhängigkeiten installieren (am besten in einer venv):

```bash
pip install -r requirements.txt
```

3. App starten:

```bash
streamlit run frachtenrechner.py
```

## 📂 Dateien im Projekt

| Datei               | Beschreibung                                         |
|---------------------|------------------------------------------------------|
| `frachtenrechner.py` | Hauptanwendung (Streamlit UI)                      |
| `utils.py`           | Berechnungslogik: Tarife, Gewichtsstufen, Zonen     |
| `dsv.xlsx`           | DSV-Tarife (nur DE)                                 |
| `dachser.xlsx`       | Dachser-Tarife (mehrere Länder)                     |
| `nk.xlsx`            | Zustelloptionen und sonstige Nebenkosten je Land    |
| `requirements.txt`   | Python-Abhängigkeiten für Streamlit, Pandas, etc.   |

## 👤 Autor

Erstellt von Christine Klein – Hans Becker GmbH  
GitHub: [github.com/CKsehrcool](https://github.com/CKsehrcool)
