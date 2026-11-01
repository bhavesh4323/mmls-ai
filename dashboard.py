"""
dashboard.py — MMLS-AI v2.0 (Complete Edition)
Real QR camera scanner + register new items + all previous features
Run app.py first, then: streamlit run dashboard.py
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib, os, time, json, random
from datetime import datetime

st.set_page_config(page_title="MMLS-AI Dashboard", page_icon="🏥", layout="wide")

st.markdown("""
<style>
/* Global app and page background */
html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
    background-image: none !important;
    color: #c9d1d9 !important;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0b0f12 !important;
    color: #c9d1d9 !important;
    border-right: 1px solid #22272b !important;
}
/* Main container spacing */
.block-container{padding-top:1rem}
/* Cards and tiles */
.metric-card{background:linear-gradient(145deg, #0f1418, #161b22);border:1px solid #30363d;border-radius:10px;padding:16px;text-align:center;box-shadow: 0 4px 12px rgba(0,0,0,0.15);position: relative;overflow: hidden;transition: transform 0.2s ease}.metric-card:hover {transform: translateY(-2px);border-color: #58a6ff;}
.hos-GREEN {background:#071710;border:1px solid #238636;border-radius:8px;padding:10px;text-align:center}
.hos-TEAL  {background:#071818;border:1px solid #1f6f6f;border-radius:8px;padding:10px;text-align:center}
.hos-AMBER {background:#1a1308;border:1px solid #e3b341;border-radius:8px;padding:10px;text-align:center}
.hos-RED   {background:#160808;border:1px solid #f85149;border-radius:8px;padding:10px;text-align:center}
.hos-PURPLE{background:#0f0714;border:1px solid #8b5cf6;border-radius:8px;padding:10px;text-align:center}
/* Headings and text */
h1,h2,h3,h4,p,span,div { color: #c9d1d9 !important; }
/* Inputs */
input, textarea, .stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: #0f1418 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
}
/* Select boxes and file uploader */
div[data-baseweb="input"], div[data-baseweb="input"] > div {
    background-color: #0f1418 !important;
    border-color: #30363d !important;
}
div[data-baseweb="input"] input {
    color: #c9d1d9 !important;
    background-color: transparent !important;
    -webkit-text-fill-color: #c9d1d9 !important;
}

/* Fix the Selectbox closed state */
div[data-baseweb="select"] > div {
    background-color: #0f1418 !important;
    color: #c9d1d9 !important;
    border-color: #30363d !important;
}

/* Fix the Selectbox open dropdown menu (popover) */
div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul {
    background-color: #0f1418 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
}
div[data-baseweb="popover"] li {
    color: #c9d1d9 !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #1f2937 !important;
    color: #58a6ff !important;
}

/* Fix Checkboxes */
div[data-testid="stCheckbox"] label span {
    color: #c9d1d9 !important;
}
div[data-testid="stCheckbox"] div[data-baseweb="checkbox"] > div:first-child {
    background-color: #0f1418 !important;
    border-color: #30363d !important;
}
/* Buttons (primary green style used in screenshot) */
.stButton>button, .stDownloadButton>button, button[type="button"] {
    background: linear-gradient(180deg,#1fb95f,#127a3f) !important;
    color: #ffffff !important;
    border: 1px solid #0b5a34 !important;
    box-shadow: none !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
}
/* Subtle hover and click animation */
.stButton>button:hover, .stDownloadButton>button:hover, button[type="button"]:hover {
    transform: translateY(-2px) scale(1.01);
    transition: transform 120ms ease-in-out;
}
.stButton>button:active, .stDownloadButton>button:active, button[type="button"]:active {
    animation: click-pulse 260ms ease-out;
}
@keyframes click-pulse {
    0% { transform: scale(1); box-shadow: 0 0 0 rgba(0,0,0,0); }
    50% { transform: scale(0.98); box-shadow: 0 6px 12px rgba(0,0,0,0.25); }
    100% { transform: scale(1); box-shadow: 0 0 0 rgba(0,0,0,0); }
}
/* Secondary (dark green) buttons */
.btn-secondary { background: linear-gradient(180deg,#2b6f3a,#114b2a) !important; }
/* Dataframes / tables */
.stDataFrame, table {
    background: #0d1117 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px;
}
thead tr th {
    background-color: #161b22 !important;
    color: #8b949e !important;
    border-bottom: 1px solid #30363d !important;
}
tbody tr:nth-child(even) {
    background-color: #161b22 !important;
}
tbody tr:hover {
    background-color: #1f2937 !important;
}
/* Tabs and panels */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #161b22 !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid #30363d !important;
    border-bottom: none !important;
    padding: 10px 16px !important;
}
.stTabs [aria-selected="true"] {
    background-color: #1fb95f !important;
    color: white !important;
    border-color: #1fb95f !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none; /* Hides the default red underline */
}
/* File uploader placeholder text */
.stFileUploader input[type=file] + label {
    color: #c9d1d9 !important;
}
/* Misc tweaks */
.stAlert, .stMarkdown, .stMetric { color: #c9d1d9 !important; }
/* Scrollbar: wider + distinct color for usability */
::-webkit-scrollbar { width: 14px; height: 14px; }
::-webkit-scrollbar-track { background: #0d1117; border-radius: 7px; }
::-webkit-scrollbar-thumb { background: #58a6ff; border-radius: 7px; border: 3px solid #0d1117; }
::-webkit-scrollbar-thumb:hover { background: #79c0ff; }
* { scrollbar-width: thin; scrollbar-color: #58a6ff #0d1117; }
</style>
""", unsafe_allow_html=True)

def _resolve_api_url():
    # 1) Streamlit Community Cloud: .streamlit/secrets.toml -> ["MMLS_AI_API_URL"]
    # 2) any host: MMLS_AI_API_URL environment variable
    # 3) fall back to the Render API default below.
    try:
        import streamlit as _st
        _sec = _st.secrets
        if "MMLS_AI_API_URL" in _sec:
            return _sec["MMLS_AI_API_URL"]
    except Exception:
        pass
    return os.environ.get("MMLS_AI_API_URL", "https://mmls-ai-api.onrender.com")

API = _resolve_api_url()
HOS_COLOR = {"GREEN":"#238636","TEAL":"#1f9e9e","AMBER":"#e3b341","RED":"#f85149","PURPLE":"#8b5cf6"}

USERS = {
    "medic01":    {"password":"medic123",   "role":"Medic (Role 1)",       "echelon":"Role1"},
    "surgeon01":  {"password":"surgeon123", "role":"FST Surgeon (Role 2)", "echelon":"Role2"},
    "logistic01": {"password":"admin123",   "role":"Logistician (Role 3)", "echelon":"Role3"},
}
ROLE_COLOR = {
    "Medic (Role 1)":       "#3fb950",
    "FST Surgeon (Role 2)": "#58a6ff",
    "Logistician (Role 3)": "#e3b341",
}

for key, val in [("logged_in",False),("username",""),("role",""),("echelon",""),
                  ("qr_result",None),("register_mode",False),("med_info",None),
                  ("med_raw",""),("fda_name",""),("fda_source",""),("last_registered",""),
                  ("matched_item",None),("search_no_match",False),("search_raw",""), 
                  ("delete_mode", False)]: # <-- ADD THIS HERE
    if key not in st.session_state:
        st.session_state[key] = val

# ── HELPERS ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_excel_catalog():
    """
    Loads the static Excel catalog and returns it as a dictionary 
    mapped by NSN/Item ID.
    """
    catalog = {}
    try:
        # Update this filename if yours is different
        excel_file = "BST_Medical_Consumables_NSN_v2.xlsx"
        
        # Check if the file exists first to avoid crashing
        if os.path.exists(excel_file):
            # Read all sheets
            all_sheets = pd.read_excel(excel_file, sheet_name=None)
            
            # Combine sheets and map to a dictionary
            # Note: You may need to adjust "NSN" depending on your exact Excel column headers
            for sheet_name, df in all_sheets.items():
                if "NSN" in df.columns:
                    # Convert dataframe to dictionary with NSN as the key
                    sheet_dict = df.set_index("NSN").to_dict(orient="index")
                    catalog.update(sheet_dict)
                    
        return catalog
    except Exception as e:
        st.error(f"Error loading Excel catalog: {e}")
        return {}
def _api_request(method, path, **kw):
    # Render's free API instance sleeps after ~15 min idle and needs ~60-90s to
    # wake. Instead of blocking and then showing a hard error (which forced the
    # user to refresh manually), we poll once and, if the API is still asleep,
    # auto-rerun the page every few seconds until it answers. Bounded to ~90s.
    url = f"{API}{path}"
    kw.setdefault("timeout", 20)
    r = None
    last_err = None
    try:
        r = requests.request(method, url, **kw)
    except Exception as e:
        last_err = e
    if r is not None and r.status_code not in (502, 503, 504):
        st.session_state.pop("_api_wake_n", None)  # API is warm -> reset counter
        return r
    n = st.session_state.get("_api_wake_n", 0)
    if n < 18:
        st.session_state["_api_wake_n"] = n + 1
        st.info("🔄 The inventory service is asleep and waking up. This page refreshes "
                "automatically — please wait ~60s. (First load is slow on free hosting.)")
        time.sleep(5)
        st.rerun()
    st.session_state.pop("_api_wake_n", None)
    if r is not None:
        return r
    if last_err:
        raise last_err
    return r

def api_get(path):
    try:
        return _api_request("get", path).json()
    except Exception:
        st.error("Cannot reach the inventory service after ~90s. It may still be starting - please refresh once more.")
        return []

def api_post(path, body):
    try:
        return _api_request("post", path, json=body).json()
    except Exception:
        st.error("Cannot connect to Flask API.")
        return {}

def api_post_raw(path, body):
    try:
        r = requests.post(f"{API}{path}", json=body, timeout=5)
        try:
            resp = r.json()
        except:
            resp = {"error": r.text}
        return r.status_code, resp
    except Exception as e:
        return 500, {"error": str(e)}

# ── LOGIN ──────────────────────────────────────────────────────────────────────
def show_login():
    # ── BST Logo top-left ─────────────────────────────────────────────────────
    col_logo, col_spacer = st.columns([1, 5])
    with col_logo:
        logo_b64 = "/9j/4AAQSkZJRgABAQEA2ADYAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAMgBOIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8qqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACitTw34X1bxfqkenaLp8+pXsnSKBMkD1J6Ae5wK+l/hv8AsXFljvPGmoFT1/s3T25+jy4/RR/wKvLxuZYXAK9edn26/ce9leR4/N5WwlO66yekV8/0V35Hy3Y2F1qd1HbWdtNd3MhwkMCF3Y+gA5NeueEv2UPH/iYRy3FjDoVs3PmalLtfH/XNQWB9mAr7X8J+A/D3gW0+zaDpFrpkeMM0KfO/+85yzfiTW9XwuK4sqybWFhyru9X92y/E/Wcv8PMPTSlj6rk+0dF971f4HzP4d/Yh0a3VW13xFe3z9THYxLAo9stvJH5V6No/7Mvw40UKV8Ox3kg6yXk8kuf+Altv6V6lRXzNbN8fX+Os/lp+Vj7vDcN5RhF+6w0fmuZ/fK5zVj8M/CGmhfsvhbRrcr0aOwiB+udua1oNB0u1UrDptpEpOSscCqM+vAq/RXmSq1J/FJv5nuQw9GmrQgl6JFT+ybH/AJ8rf/v0v+FH9k2P/Plb/wDfpf8ACrdFRzPuaezh2Kn9k2P/AD5W/wD36X/Cj+ybH/nyt/8Av0v+FW6KOZ9w9nDsVP7Jsf8Anyt/+/S/4Uf2TY/8+Vv/AN+l/wAKt0Ucz7h7OHYqf2TY/wDPlb/9+l/wo/smx/58rf8A79L/AIVboo5n3D2cOxU/smx/58rf/v0v+FH9k2P/AD5W/wD36X/CrdFHM+4ezh2Kn9k2P/Plb/8Afpf8KP7Jsf8Anyt/+/S/4Vboo5n3D2cOxU/smx/58rf/AL9L/hR/ZNj/AM+Vv/36X/CrdFHM+4ezh2Kn9k2P/Plb/wDfpf8ACj+ybH/nyt/+/S/4Vboo5n3D2cOxU/smx/58rf8A79L/AIUf2TY/8+Vv/wB+l/wq3RRzPuHs4dip/ZNj/wA+Vv8A9+l/wo/smx/58rf/AL9L/hVuijmfcPZw7FT+ybH/AJ8rf/v0v+FH9k2P/Plb/wDfpf8ACrdFHM+4ezh2Kn9k2P8Az5W//fpf8KP7Jsf+fK3/AO/S/wCFW6KOZ9w9nDsVP7Jsf+fK3/79L/hR/ZNj/wA+Vv8A9+l/wq3RRzPuHs4dip/ZNj/z5W//AH6X/Cj+ybH/AJ8rf/v0v+FW6KOZ9w9nDsVP7Jsf+fK3/wC/S/4Uf2TY/wDPlb/9+l/wq3RRzPuHs4dip/ZNj/z5W/8A36X/AAo/smx/58rf/v0v+FW6KOZ9w9nDsVP7Jsf+fK3/AO/S/wCFH9k2P/Plb/8Afpf8Kt0Ucz7h7OHYqf2TY/8APlb/APfpf8KP7Jsf+fK3/wC/S/4Vboo5n3D2cOxU/smx/wCfK3/79L/hR/ZNj/z5W/8A36X/AAq3RRzPuHs4dip/ZNj/AM+Vv/36X/Cj+ybH/nyt/wDv0v8AhVuijmfcPZw7FT+ybH/nyt/+/S/4Uf2TY/8APlb/APfpf8Kt0Ucz7h7OHYqf2TY/8+Vv/wB+l/wo/smx/wCfK3/79L/hVuijmfcPZw7FT+ybH/nyt/8Av0v+FH9k2P8Az5W//fpf8Kt0Ucz7h7OHYqf2TY/8+Vv/AN+l/wAKP7Jsf+fK3/79L/hVuijmfcPZw7FT+ybH/nyt/wDv0v8AhR/ZNj/z5W//AH6X/CrdFHM+4ezh2Kn9k2P/AD5W/wD36X/Cj+ybH/nyt/8Av0v+FW6KOZ9w9nDsVP7Jsf8Anyt/+/S/4Uf2TY/8+Vv/AN+l/wAKt0Ucz7h7OHYqf2TY/wDPlb/9+l/wo/smx/58rf8A79L/AIVboo5n3D2cOxU/smx/58rf/v0v+FH9k2P/AD5W/wD36X/CrdFHM+4ezh2Kn9k2P/Plb/8Afpf8KP7Jsf8Anyt/+/S/4Vboo5n3D2cOxU/smx/58rf/AL9L/hR/ZNj/AM+Vv/36X/CrdFHM+4ezh2Kn9k2P/Plb/wDfpf8ACj+ybH/nyt/+/S/4Vboo5n3D2cOxU/smx/58rf8A79L/AIUf2TY/8+Vv/wB+l/wq3RRzPuHs4dip/ZNj/wA+Vv8A9+l/wo/smx/58rf/AL9L/hVuijmfcPZw7FT+ybH/AJ8rf/v0v+FH9k2P/Plb/wDfpf8ACrdFHM+4ezh2Kn9k2P8Az5W//fpf8KP7Jsf+fK3/AO/S/wCFW6KOZ9w9nDsVP7Jsf+fK3/79L/hR/ZNj/wA+Vv8A9+l/wq3RRzPuHs4dip/ZNj/z5W//AH6X/Cj+ybH/AJ8rf/v0v+FW6KOZ9w9nDsVP7Jsf+fK3/wC/S/4Uf2TY/wDPlb/9+l/wq3RRzPuHs4dip/ZNj/z5W/8A36X/AAo/smx/58rf/v0v+FW6KOZ9w9nDsVP7Jsf+fK3/AO/S/wCFH9k2P/Plb/8Afpf8Kt0Ucz7h7OHYqf2TY/8APlb/APfpf8KP7Jsf+fK3/wC/S/4Vboo5n3D2cOxU/smx/wCfK3/79L/hR/ZNj/z5W/8A36X/AAq3RRzPuHs4dip/ZNj/AM+Vv/36X/Cj+ybH/nyt/wDv0v8AhVuijmfcPZw7FT+ybH/nyt/+/S/4Uf2TY/8APlb/APfpf8Kt0Ucz7h7OHYqf2TY/8+Vv/wB+l/wo/smx/wCfK3/79L/hVuijmfcPZw7FT+ybH/nyt/8Av0v+FH9k2P8Az5W//fpf8Kt0Ucz7h7OHYqf2TY/8+Vv/AN+l/wAKP7Jsf+fK3/79L/hVuijmfcPZw7FT+ybH/nyt/wDv0v8AhR/ZNj/z5W//AH6X/CrdFHM+4ezh2Kn9k2P/AD5W/wD36X/Cj+ybH/nyt/8Av0v+FW6KOZ9w9nDsVP7Jsf8Anyt/+/S/4VSuPBugXm77Roemz7juPmWkbZPqcjrWxRVKc47Nkyo05K0op/I4XU/gZ8P9WUrP4R0pAeptrcQH849tcNr37HfgHVFJsRqOjP2+zXPmL+IkDEj8RXudFd1LMcZR/h1ZL5v8jysRkmWYpWrYeD/7dV/vWp8deKf2JdcsleXQNdtNUUciG7jNvJ9AQWUn64rxXxh8LfFfgJj/AG7oV3YxA7ftBTfCT6CRcrn2zX6X0ySNJo2jkVXRgVZWGQQeoIr6HDcU4yjpWSmvuf4afgfGY7gDLcQm8LJ0n/4Evuev4n5VUV97fEL9lrwX42WWe0tf+Ed1JuRcaeoEZP8AtRfdI/3dpPrXy38T/wBnPxb8M/NupLb+19HX5v7QsVLKi+si9U+pyvvX2+Bz3B460VLll2f6PZ/n5H5Vm3CeZ5SnUlHnpr7UdfvW6/LzPLaKKK+iPjAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooqW1tZr65itraJ57iZxHHFGpZnYnAAA6kmjbVjSbdkRV7p8Gv2WdY8frBquvGXQ9BfDICuLm5XsUUj5VP94/gCDmvVfgP+yza+G0tte8YQR3mr8SQaa2Gitj1Bfs7+3Qe55H0fX55m3EvK3QwL9Zf5f5/d3P2bh3gfnUcVmq03UP/kv8vv7GB4N8C6F4A0pdP0HTobC343lBl5CP4nY8sfqa36KK/OZzlUk5zd2z9qp0qdGCp0oqMVslokFFYvirxpoXgjT/ALbruqW+mW/8LTvhnI7Ko5Y+wBNfO/jj9ti1t2kg8J6K12w4F7qRKR/hGp3EfVl+lehg8txeOf7iDa77L7zx8yzzL8pX+11Un23f3LX9D6irJ1rxZofhtS2raxYaYOv+mXKRf+hEV+f/AIs+P3j3xgzi88RXVtbt/wAu1g32ePHodmCw/wB4mvP5JHmkZ3ZndjksxySfU19dQ4RqSV8RVS8kr/i7fkfnGL8RaUW1hKDfnJ2/BX/M/QvUv2kfhtpbFZfFNvIwOP8ARoZZs9e6IR2rDn/a5+HEO3ZqF5Pn/nnZOMfmBXwdRXrx4UwS+KUn81/kfOVPELNJP3KcF8n/APJH3Z/w1/8ADv8A5+dQ/wDAM/40f8Nf/Dv/AJ+dQ/8AAM/418J0Vp/qrgO8vvX+Rj/r/m/aH/gL/wAz7s/4a/8Ah3/z86h/4Bn/ABo/4a/+Hf8Az86h/wCAZ/xr4Too/wBVcB3l96/yD/X/ADftD/wF/wCZ92f8Nf8Aw7/5+dQ/8Az/AI0f8Nf/AA7/AOfnUP8AwDP+NfCdFH+quA7y+9f5B/r/AJv2h/4C/wDM+7P+Gv8A4d/8/Oof+AZ/xo/4a/8Ah3/z86h/4Bn/ABr4Too/1VwHeX3r/IP9f837Q/8AAX/mfdn/AA1/8O/+fnUP/AM/40f8Nf8Aw7/5+dQ/8Az/AI18J0Uf6q4DvL71/kH+v+b9of8AgL/zPuz/AIa/+Hf/AD86h/4Bn/Gj/hr/AOHf/PzqH/gGf8a+E6KP9VcB3l96/wAg/wBf837Q/wDAX/mfdn/DX/w7/wCfnUP/AADP+NH/AA1/8O/+fnUP/AM/418J0Uf6q4DvL71/kH+v+b9of+Av/M+7P+Gv/h3/AM/Oof8AgGf8aP8Ahr/4d/8APzqH/gGf8a+E6KP9VcB3l96/yD/X/N+0P/AX/mfdn/DX/wAO/wDn51D/AMAz/jR/w1/8O/8An51D/wAAz/jXwnRR/qrgO8vvX+Qf6/5v2h/4C/8AM+7P+Gv/AId/8/Oof+AZ/wAaP+Gv/h3/AM/Oof8AgGf8a+E6KP8AVXAd5fev8g/1/wA37Q/8Bf8Amfdn/DX/AMO/+fnUP/AM/wCNH/DX/wAO/wDn51D/AMAz/jXwnRR/qrgO8vvX+Qf6/wCb9of+Av8AzPuz/hr/AOHf/PzqH/gGf8aP+Gv/AId/8/Oof+AZ/wAa+E6KP9VcB3l96/yD/X/N+0P/AAF/5n3Z/wANf/Dv/n51D/wDP+NH/DX/AMO/+fnUP/AM/wCNfCdFH+quA7y+9f5B/r/m/aH/AIC/8z7s/wCGv/h3/wA/Oof+AZ/xo/4a/wDh3/z86h/4Bn/GvhOij/VXAd5fev8AIP8AX/N+0P8AwF/5n3Z/w1/8O/8An51D/wAAz/jR/wANf/Dv/n51D/wDP+NfCdFH+quA7y+9f5B/r/m/aH/gL/zPuz/hr/4d/wDPzqH/AIBn/Gj/AIa/+Hf/AD86h/4Bn/GvhOij/VXAd5fev8g/1/zftD/wF/5n3Z/w1/8ADv8A5+dQ/wDAM/40f8Nf/Dv/AJ+dQ/8AAM/418J0Uf6q4DvL71/kH+v+b9of+Av/ADPuz/hr/wCHf/PzqH/gGf8AGj/hr/4d/wDPzqH/AIBn/GvhOij/AFVwHeX3r/IP9f8AN+0P/AX/AJn3Z/w1/wDDv/n51D/wDP8AjR/w1/8ADv8A5+dQ/wDAM/418J0Uf6q4DvL71/kH+v8Am/aH/gL/AMz7s/4a/wDh3/z86h/4Bn/Gj/hr/wCHf/PzqH/gGf8AGvhOij/VXAd5fev8g/1/zftD/wABf+Z92f8ADX/w7/5+dQ/8Az/jR/w1/wDDv/n51D/wDP8AjXwnRR/qrgO8vvX+Qf6/5v2h/wCAv/M+7P8Ahr/4d/8APzqH/gGf8aP+Gv8A4d/8/Oof+AZ/xr4Too/1VwHeX3r/ACD/AF/zftD/AMBf+Z92f8Nf/Dv/AJ+dQ/8AAM/40f8ADX/w7/5+dQ/8Az/jXwnRR/qrgO8vvX+Qf6/5v2h/4C/8z7s/4a/+Hf8Az86h/wCAZ/xo/wCGv/h3/wA/Oof+AZ/xr4Too/1VwHeX3r/IP9f837Q/8Bf+Z92f8Nf/AA7/AOfnUP8AwDP+NH/DX/w7/wCfnUP/AADP+NfCdFH+quA7y+9f5B/r/m/aH/gL/wAz7s/4a/8Ah3/z86h/4Bn/ABo/4a/+Hf8Az86h/wCAZ/xr4Too/wBVcB3l96/yD/X/ADftD/wF/wCZ92f8Nf8Aw7/5+dQ/8Az/AI0f8Nf/AA7/AOfnUP8AwDP+NfCdFH+quA7y+9f5B/r/AJv2h/4C/wDM+7P+Gv8A4d/8/Oof+AZ/xo/4a/8Ah3/z86h/4Bn/ABr4Too/1VwHeX3r/IP9f837Q/8AAX/mfdn/AA1/8O/+fnUP/AM/40f8Nf8Aw7/5+dQ/8Az/AI18J0Uf6q4DvL71/kH+v+b9of8AgL/zPuz/AIa/+Hf/AD86h/4Bn/Gj/hr/AOHf/PzqH/gGf8a+E6KP9VcB3l96/wAg/wBf837Q/wDAX/mfdn/DX/w7/wCfnUP/AADP+NH/AA1/8O/+fnUP/AM/418J0Uf6q4DvL71/kH+v+b9of+Av/M+7P+Gv/h3/AM/Oof8AgGf8aP8Ahr/4d/8APzqH/gGf8a+E6KP9VcB3l96/yD/X/N+0P/AX/mfdn/DX/wAO/wDn51D/AMAz/jR/w1/8O/8An51D/wAAz/jXwnRR/qrgO8vvX+Qf6/5v2h/4C/8AM+7P+Gv/AId/8/Oof+AZ/wAaP+Gv/h3/AM/Oof8AgGf8a+E6KP8AVXAd5fev8g/1/wA37Q/8Bf8Amfdn/DX/AMO/+fnUP/AM/wCNH/DX/wAO/wDn51D/AMAz/jXwnRR/qrgO8vvX+Qf6/wCb9of+Av8AzPuz/hr/AOHf/PzqH/gGf8aP+Gv/AId/8/Oof+AZ/wAa+E6KP9VcB3l96/yD/X/N+0P/AAF/5n3Z/wANf/Dv/n51D/wDP+NH/DX/AMO/+fnUP/AM/wCNfCdFH+quA7y+9f5B/r/m/aH/AIC/8z7s/wCGv/h3/wA/Oof+AZ/xo/4a/wDh3/z86h/4Bn/GvhOij/VXAd5fev8AIP8AX/N+0P8AwF/5n3Z/w1/8O/8An51D/wAAz/jR/wANf/Dv/n51D/wDP+NfCdFH+quA7y+9f5B/r/m/aH/gL/zPuz/hr/4d/wDPzqH/AIBn/Gj/AIa/+Hf/AD86h/4Bn/GvhOij/VXAd5fev8g/1/zftD/wF/5n3Z/w1/8ADv8A5+dQ/wDAM/40f8Nf/Dv/AJ+dQ/8AAM/418J0Uf6q4DvL71/kH+v+b9of+Av/ADPuz/hr/wCHf/PzqH/gGf8AGj/hr/4d/wDPzqH/AIBn/GvhOij/AFVwHeX3r/IP9f8AN+0P/AX/AJn3Z/w1/wDDv/n51D/wDP8AjR/w1/8ADv8A5+dQ/wDAM/418J0Uf6q4DvL71/kH+v8Am/aH/gL/AMz7s/4a/wDh3/z86h/4Bn/Gj/hr/wCHf/PzqH/gGf8AGvhOij/VXAd5fev8g/1/zftD/wABf+Z92f8ADX/w7/5+dQ/8Az/jR/w1/wDDv/n51D/wDP8AjXwnRR/qrgO8vvX+Qf6/5v2h/wCAv/M+7P8Ahr/4d/8APzqH/gGf8aP+Gv8A4d/8/Oof+AZ/xr4Too/1VwHeX3r/ACD/AF/zftD/AMBf+Z92f8Nf/Dv/AJ+dQ/8AAM/40f8ADX/w7/5+dQ/8Az/jXwnRR/qrgO8vvX+Qf6/5v2h/4C/8z7s/4a/+Hf8Az86h/wCAZ/xo/wCGv/h3/wA/Oof+AZ/xr4Too/1VwHeX3r/IP9f837Q/8Bf+Z92f8Nf/AA7/AOfnUP8AwDP+NH/DX/w7/wCfnUP/AADP+NfCdFH+quA7y+9f5B/r/m/aH/gL/wAz7s/4a/8Ah3/z86h/4Bn/ABo/4a/+Hf8Az86h/wCAZ/xr4Too/wBVcB3l96/yD/X/ADftD/wF/wCZ92f8Nf8Aw7/5+dQ/8Az/AI1o2v7VXw0uWCtr8luTgDzbKfH5hDj8a+AqKl8K4B7Skvmv8i4+IObResYP5P8A+SP0l0f4yeBteKrZ+K9Kd2+7HJcrE5/4C+D+ldhDMlxGskTrLGwyrocgj1Br8qq1vD/i7XPCs3m6Nq97pb5yTaztGD9QDg/jXnVuEY2/c1fvX6r/ACPaw3iNUvbFYdPzi7fg7/mfqFRXxD4N/bG8Y6C0cetxWviK1HBMiiCfHs6Db+ak+9fQ/wAPv2mPBXj54rYXp0bU5OBZ6liPcfRZPut7DIJ9K+VxmR47BpylDmj3Wv8AwfwP0DLeK8qzNqFOpySfSWj/AMn8mer0nXg9KWivBPrzwj4ufsp6F44WfUfD3laBrZyxRFxazt/tqB8hP95fxBr448XeDdZ8C6zLpeuWEtheR87ZBlXX+8rDhh7iv0+rl/iB8N9C+JmhvpmuWgmTBMVxHgTQN/eRux/MHuDX1+VcRVsG1SxHvw/Ff5+h+bcQcF4bMk6+CSp1f/JZeq6PzXzTPzPor0L4wfBXWvhDrAiuwbzSZ2ItdSjTCSf7LD+F8dvyJrz2v1WjXp4imqtKV4s/n3FYWvgq0sPiIuM47p/1+IUUUVucoUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAS2trNfXMVtbRPPcTOI44o1LM7E4AAHUk19yfs9/s82vw2sYta1qKO68TzpkZAZbJSPuJ/t/wB5vwHGS2D+y38BV8L2EHi/X7b/AInNym6xt5BzaxMPvkdnYH/gIPqSB9G1+X8QZ260ng8M/dW77+Xp+fpv+9cH8LLDQjmOOj771jF/ZXd+b6dvXYoorC8aeNdH+H+gT6xrd2trZxcDu8jYOEQfxMcdPxOACa+GhCVSShBXbP1epUhRg6lRpRWrb2Rr3l5Bp9rLc3M0dtbxKXkmmcKiKOpJPAFfMnxb/bDhsmn0zwPGt1MMo2r3CZjU/wDTJD97/ebj2I5rxr4zfH7XPixeSW4Z9N8PI+YdOjb7+OjSkfeb26Dt6ny2v0vKuGYU0quN1l/L0Xr3/L1PwziDjqrWbw+Vvlj/AD9X6dl57+ho694i1PxTqUuoavfz6jeyH5prhyx+g9B6AcCs6iivvIxUUoxVkj8knOVSTnN3b6sKKKKogKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA9V+F37R3iv4aNFamc61oq4B0+9cnYvpG/JT6cr7V9lfDH4x+HPitp5l0i68u9jXdPp1xhZ4u2cfxLn+IZHIzg8V+cFW9I1i90HUrfUNOupbK9t23xTwsVdT7EV8xmWQYbHpzguSfdbP1X67n3mR8X43KWqVV+0pdnuv8L/Tb03P1NorwL4B/tNWvj9oNC8SNFY+IsbYp1+WG8Pt/df/AGeh7Y+7Xvtfk+LwdbA1XRrqz/PzR/Q2XZlhs1oLE4WV4v70+zXR/wBbGZ4k8N6b4u0W60nVrVLzT7lNkkUg/Ig9QQeQRyCMivgb44fBLUfhBrgGWvNBumP2O+I59fLkx0cD8COR3A/Qysfxd4T0zxx4fvNG1e3FzY3SbWX+JT2ZT2YHkGvSyjNqmWVe9N7r9V5/meHxHw7Rz2hp7tWPwy/R+T/DddU/y/orsfit8M9R+FPi240a+/fQ/wCstbsLhZ4ieGHoexHYj6GuOr9opVYVoKpTd4vY/mHEYerhasqFaPLKLs0FFFFanOFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV7v+yv8GR488RHxDqsG/QtLkGxHHy3NwMEJ7qvDH6qOhNePeEfDF7408S6domnJvvL6YRJ6L3LH2ABJ9ga/SbwT4RsfAfhbTtC05MWtnEEDEYMjdWc+7Nkn618hxFmbwdD2FJ+/P8F1fz2Xz7H6PwXkSzPFvFV1elT/ABl0Xy3fyXU3KKKhvLyDTbOe7upkt7aBGkllkYBUUDJYnsAK/I9Xoj+jm0ldmR428aaV8P8Aw3d63rE/kWduOi8vIx+6iDuxP+JwATX59/Fj4sax8WPEUl/qEjRWUbMLOwVspboe3uxwMt3PoMAbHx6+M1z8WvFLNCzw6BZMUsbc5G4dDKw/vN+gwPUnzCv13IsmWBpqvWX7x/8Akq7evf7vX+cOLOJpZtVeFwztQi//AAJ935dl8/Qooor64/OQooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBVYowZSVYHII6ivsj9mf9ok+LFg8KeJrgf2yi7bO+kPN2APuOf+egHf8Ai+o+b42p8E8lrNHNDI0U0bB0kjYqysDkEEdCDXlZll1LMqLpVN+j7P8ArdH0GSZ1iMkxSr0XeL+KPSS/z7Pp6XP1Vorx/wDZz+NS/FTwybTUJFHiTTkVbpeB56dFmA9+jY6H0BAr2CvxLE4ephK0qFVWkj+p8DjaOY4aGKw7vGS/pPzXU89+OHwptviz4LmsNqR6tbZm0+4b+CTH3Sf7rYAP4HsK/PC+sbjTL24s7uF7e6t5GilhkGGR1OCpHqCDX6o18j/tj/CkWd3B4306HEVwVt9SVBwJMYjl/EDafcL3NfY8M5m6NT6lVfuy+Hyfb5/n6n5nx1kSxFH+06C9+Hxece/qvy9D5fooor9RPwQKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiirWk6Xca3qlnp1onm3d3MkEKD+J2YKo/Mik2oq7KjFyajFXbPqf9i/4beXBf8AjW8i+aTdZ2G4fwj/AFsg+pwoPs4719T1jeDfDFt4L8K6VodmP3FjbrCG/vkD5mPuzZJ+tbNfhGZYx4/FTrvZ7enQ/rbI8tjlOX0sKt0ry85Pf/JeVgr5Z/bC+LzW8a+BtLm2vIqzanIh5CnlIfx4Y+231NfRHjvxdaeA/CGq6/ecwWMJk2ZwZH6Ig92Yqv41+aeva5eeJNavdV1CUz3t5M08sh7sxyceg9B2FfQ8M5csTXeKqL3Ybf4v+Bv9x8Xx1nTwWFWAou06u/lH/wC229EyjRRRX6ufz2FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB0HgHxtf/DzxZp+vac37+1ky0ecLLGeGjb2IyPbg9RX6R+FfElj4w8O6frWmyebZXsIljPcZ6qfcHII9Qa/LyvqP9jD4lNDfX3gu9lzFMGu7Dcejj/WIPqPmx/st618VxNlyxGH+tQXvQ381/wADf7z9R4Fzp4PF/UKr9yrt5S6fft62PrWsnxX4bs/GPhvUtEv032l9C0L+q5HDD3BwR7gVrUV+VRlKElKLs0f0DUhGpBwmrp6NeTPy78U+Hbvwj4j1LRb5dt3YztBJjocHAYexGCPYisuvpf8AbV8Ciw8QaV4rt48R6gn2S6ZRx5qDKMfcpkf9s6+aK/eMuxax2FhXW7Wvr1/E/kjOsueVZhVwj2i9PR6r8PxCiiivSPECiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACva/2R/CI8SfFiG+lTdbaPA92c9DIfkjH1yxb/gFeKV9l/sT+HRY+CNa1plxJf3ogU+qRLwf++pH/ACr5/PsR9Wy+o1u9Pv8A+Bc+w4RwSx2cUYyWkXzP/t3VfjY+jaKKK/FD+pT5V/bY8dFY9G8I28uN3/Ewu1U9uViU/jvOPZTXyjXcfG7xYfGnxU8R6mH3wfamggIPHlR/u0I+oXP4muHr9zyjCrB4KnS62u/V6/8AAP5O4izB5lmlavf3b2XotF9+/wAwooor2D5sKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArV8J+JLrwh4m0zWrM4ubG4SdRnAbaclT7EZB9jWVRUyipxcZLRl06kqU1Ug7Nar1R+pei6tba9o9jqdm/mWt5AlxE3qjqGH6GrteJfsh+LD4h+E0djK++40i5e1wx58s4dD9PmKj/AHK9tr8BxmHeExNSg/su3+X4H9gZZjFmGCpYpfbin8+q+TPOP2hvCA8afCPXrVU33NrF9ut+MkPF8xA9yu5f+BV+d1fqrJGs0bRuodGG1lYZBB6ivzF8b+Hz4V8Y63o5BxY3s1uue6q5Cn8Rg/jX33COIvCrh30s189H+h+QeIuCUatDGxW6cX8tV+b+4xKKKK/Qj8bCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACv0R/Z20f+w/gv4Wg24aW2N0TjGfNdpAfyYflX53V+n/gvTxpPg7QrELsFtYQQ7eONsajHH0r4Li6pahSp9239y/4J+ueHNFSxdet/LFL73f/ANtNmsDx9rx8L+B9f1YNtezsZpkP+2qEqPzxW/XlH7UepHTfgh4g2tte48mBecfemTcP++Q1fnmDpe2xNKk/tSS+9n7PmWIeFwNeut4xk/uTPz+ooor+gD+PAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooo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v6/IOJ6vtMwcf5Ul+v6n9JcB4d0cmU39uUn+Uf8A20K+Mf2278TfELQ7MHPk6YJD7F5XGP8AxwfnX2dXwF+1RrX9sfGvWlVt0dmkNqhzn7salh/30zVXC9Nzx/N/LFv8l+pnx9WVPKOT+eUV+b/Q8kooor9dP5xCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvsb9iTxKLzwjruhu+ZLG7W5QHrslXGB7Boyf+BV8c17L+yf4wHhf4uWdrK+221eJrFsngOcNGfqWUKP9+vAz3DvE5fUit1qvlr+Vz6/hPGrA5xQnJ6SfK/8At7RfjY+86KKK/Ez+pj85fjx4TPgz4seIrBUKW8lwbqDjjy5fnAHsNxX/AIDXA19cftr+BWutN0fxbbx7mtT9huyB/wAs2JaNj6ANuH1cV8j1+5ZPiljMDTqdUrP1Wn/BP5Q4ky95bmlajb3W+Zej1X3bfIKKKK9k+ZCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK2/BHhW58ceLtJ0K0z519cLFuAzsXqz/RVBb8Kic404ucnZLU0p051pxp01eUnZerPtb9kvwmfDfwitLqVNtxq073rZHIThEH0KoG/wCB17PVbTNNt9H020sLSMRWtrEkEUY6KiqFUfgAKs1+A4vEPFYidd/abZ/YGXYOOX4OlhY/Yil8+r+b1I55o7aGSaVgkUal3dugAGSa/MHxdrreJ/FWsau+c395Lc4Pbe5YD8Aa+9P2kPGH/CG/CHW5UfZdXyf2fBzglpchse4Tefwr89a/QeEsO406mIfVpL5av80fjviLjVKtQwcX8Kcn89F+T+8KKKK/QD8dCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAK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kP8ArVHSFj/eA+76jjqBn6gr8qY5HhkWSNmR1IZWU4II6EGvtP8AZz/aOg8aWtt4b8SXCweIYwI7e5kOFvgOmT2k9R/F1HPFfmfEGSOm3jMMtH8S7ea8u/b02/dODuKlVjHLcdL3lpCT6/3X59u+2+/0HWX4m8M6Z4w0W50nWLOO+sLhdrxSD8mB6hh2I5FalFfAxlKDUouzR+vThGpFwmrp7pnwX8bP2b9Y+GE02pacJNW8NFiRcquZbYekoH/oY4PtnFeN1+q0kazRsjqGRhhlYZBHoa+dfi1+yHpfiRp9T8IPFouotlm09xi1lP8As45jP0yvTgda/SMq4mjJKjjtH/N/n/mfiXEHAs4N4nKtV1h1X+F9fR69rnxnRW54u8Ea74E1NrDXtMn065H3fNX5HHqjD5WHuCaw6+/hONSKnB3T7H49UpzozdOpFxkt09GgoooqzMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoooUFiABkngAUAFanhnwvqvjDWINK0axl1C/mOEhiHbuSeigdycAV6v8Lf2V/FHjporzVkfw5o558y6T/SJR/sRnBH1bA5yM19hfD74Y+HvhjpP2HQrIQbgPOuZPmnnI7u2Oe/AwBngCvk8z4hw+CTp0Xzz/Ber/RfgfoeR8G43NGquJTp0u7+J+i/V6drnA/Ar9nHTvhekeraoY9T8TMv+uAzFaZHKx56nBwWPPYY5z7TRRX5VisVWxlV1q8rtn9BYHAYbLaCw2FhyxX4+b7sK57x5460r4c+GrrW9Xm8u3hGFjUjfM5+6iA9WP9CegNTeMfGWk+A/D9zrOs3S2tlAPq0jdkQd2PYV8A/GL4xar8XvEP2u6zbaZbkrZWCtlYlPc+rnAyfwHAr18nyipmdS8tKa3f6Lz/I+b4l4kpZHQ5Ya1pfCu3m/L8/vax/iP8QdT+Jviu61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FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH/9k="
        st.markdown(f"""
        <img src="data:image/jpeg;base64,{logo_b64}"
             style="width:230px;border-radius:12px;margin-top:10px;filter:drop-shadow(0px 0px 10px rgba(255,106,0,.45)">
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;margin-top:10px'>
      <h1 style='color:#58a6ff;font-size:48px;font-weight:800'>🏥 MMLS-AI</h1>
      <p style='color:#8b949e;font-size:22px;font-weight:600'>Military Medical Logistics System</p>
      <p style='color:#e07b30;font-size:13px;letter-spacing:4px'>
        POWERED BY BLACK SPACE TECHNOLOGY</p>
    </div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1.1,1.8,1.1])
    with col:
        
        st.markdown("<h2 style='color:#c9d1d9;text-align:center;font-size:36px;font-weight:700;margin-bottom:35px'>🔐 Secure Login</h2>",
                    unsafe_allow_html=True)
        username = st.text_input("👤Username", )
        password = st.text_input("🔒Password", type="password")
        if st.button("🔐 Secure Login", use_container_width=True):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.role      = USERS[username]["role"]
                st.session_state.echelon   = USERS[username]["echelon"]
                st.rerun()
            else:
                st.error("Invalid username or password")
        st.markdown("""
        <div style='margin-top:18px;border-top:1px solid #30363d;padding-top:14px'>
          <p style='color:#8b949e;font-size:11px;margin:0 0 4px'>Demo credentials:</p>
          <p style='color:#8b949e;font-size:11px;margin:2px 0'>medic01 / medic123 → Role 1</p>
          <p style='color:#8b949e;font-size:11px;margin:2px 0'>surgeon01 / surgeon123 → Role 2</p>
          <p style='color:#8b949e;font-size:11px;margin:2px 0'>logistic01 / admin123 → Role 3 (Admin)</p>
        </div>""", unsafe_allow_html=True)
        

# ── MAIN DASHBOARD ─────────────────────────────────────────────────────────────
def show_dashboard():
    role   = st.session_state.role
    rcolor = ROLE_COLOR.get(role, "#8b949e")

    col_h, col_u = st.columns([4,1])
    with col_h:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, #0d1117 0%, #161b22 100%);
                border:1px solid #30363d;border-radius:12px;padding:16px 24px;margin-bottom:16px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);'>
          <h1 style='color:#58a6ff;margin:0;font-size:24px; letter-spacing:0.5px;'>
            🏥 MMLS-AI — Military Medical Logistics System</h1>
          <p style='color:#8b949e;margin:4px 0 0;font-size:12px; text-transform:uppercase; letter-spacing:1px;'>
            AI-Powered Inventory · Demand Forecasting · Hours-of-Supply Engine
          </p>
        </div>""", unsafe_allow_html=True)
    with col_u:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, #161b22 0%, #0d1117 100%); border:1px solid #30363d;border-radius:12px;
                    padding:12px;text-align:center;margin-bottom:16px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
          <p style='color:#8b949e;margin:0;font-size:10px; text-transform:uppercase;'>Logged in as</p>
          <p style='color:#c9d1d9;margin:4px 0;font-size:14px;font-weight:600'>
            {st.session_state.username}</p>
          <span style='background:{rcolor}22;color:{rcolor};
                       border:1px solid {rcolor}66;padding:3px 10px;
                       border-radius:20px;font-size:11px; font-weight:bold; box-shadow: 0 0 8px {rcolor}33;'>{role}</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # KPI cards
    inv_all  = api_get("/inventory")
    if "Role 3" in role:
        inv = inv_all  
    else:
        inv = [item for item in inv_all if item.get("echelon") == st.session_state.echelon]
    if inv:
        total   = len(inv)
        alerts  = sum(1 for i in inv if i.get("alert"))
        expwarn = sum(1 for i in inv if i.get("expiry_warning"))
        ctrl    = sum(1 for i in inv if i.get("controlled_drug"))
        c1,c2,c3,c4 = st.columns(4)
        for col, label, val, default_color, icon in [
            (c1,"TOTAL ITEMS",  total,   "#58a6ff", "📦"),
            (c2,"LOW STOCK",    alerts,  "#f85149" if alerts else "#3fb950", "📉"),
            (c3,"EXPIRY WARNING", expwarn, "#e3b341" if expwarn else "#3fb950", "⏳"),
            (c4,"CONTROLLED",   ctrl,    "#8b5cf6", "🔒"),
        ]:
            with col:
                st.markdown(f"""<div class='metric-card'style='border-top: 3px solid {default_color};'> <div style='position:absolute; right:-10px; top:-10px; font-size:60px; opacity:0.05;'>{icon}</div>
                  <p style='color:#8b949e;margin:0;font-size:11px;font-weight:bold;letter-spacing:1px;'>{label}</p>
                  <h2 style='color:{default_color};margin:8px 0 0 0;font-size:36px;'>{val}</h2>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    if "Role 1" in role:
        tab1,tab2,tab4,tab5,tab9 = st.tabs([
            "📦 Inventory", "🔍 Medicine Search", "⏱️ Hours of Supply",
            "📋 Audit Log", "🪖 Digital Twin",
        ])
        tab3=tab6=tab7=tab8=None
    elif "Role 2" in role:
        tab1, tab2, tab4, tab5, tab3, tab6, tab9 = st.tabs([
            "📦 Inventory", "🔍 Medicine Search", "⏱️ Hours of Supply", 
            "📋 Audit Log", "🤖 XGBoost Forecast", "📈 LSTM Trend", "🪖 Digital Twin"])
        tab7 = tab8 = None
    else:
        tab1,tab2,tab3,tab6,tab4,tab7,tab8,tab5,tab9 = st.tabs([
            "📦 Inventory","🔍 Medicine Search","🤖 XGBoost Forecast",
            "📈 LSTM Trend","⏱️ Hours of Supply",
            "🗺️ Cross-Echelon Map","✅ Validation","📋 Audit Log","🪖 Digital Twin"])

    # ── TAB 1: INVENTORY ──────────────────────────────────────────────────────
    with tab1:
        st.subheader("📦 Live Inventory ")
        
        # Action Buttons
        col_ref, col_del, _ = st.columns([1, 1, 4])
        with col_ref:
            if st.button("🔄 Refresh", key="ref1"): st.rerun()
        with col_del:
            # Button to toggle delete mode
            if st.button("🗑️ Delete Items", key="del_mode"):
                st.session_state.delete_mode = not st.session_state.delete_mode
                st.rerun()
        
        # 1. Load the static Excel data instantly from cache
        excel_catalog = load_excel_catalog()
        
        if inv:
            rows = []
            for i, item in enumerate(inv):
                # 2. Get the live backend data
                nsn = item.get("item_id", "")
                ech = item.get("echelon", "")
                stk = item.get("current_stock", 0)
                
                # 3. Fetch the static text from Excel
                cat_data = excel_catalog.get(nsn, {})
                
                status = "🔴 LOW STOCK" if item.get("alert") else "🟢 OK"
                hos = f"{float(item.get('hours_of_supply', 0)):.1f}h" if item.get("hours_of_supply") else "—"
                tier = item.get("hos_tier", "—")
                controlled = " | 🔒 Controlled" if item.get("controlled_drug") else ""
                
                ai_metrics = f"[{status} | HoS: {hos} ({tier}){controlled}]"
                
                ex_contents = cat_data.get("CONTENTS / SPECIFICATION", "—")
                ex_notes = cat_data.get("NOTES / PROCUREMENT", "—")
                ex_unit = cat_data.get("UNIT", "ea")
                ex_fsc = cat_data.get("FSC", "—")
                ex_cotccc = cat_data.get("CoTCCC / Clinical Ref", "—")
                ex_sterile = cat_data.get("Sterile ?", "YES")

                raw_contents = item.get("contents") if item.get("contents") else ex_contents
                raw_notes = item.get("notes") if item.get("notes") else ex_notes
                
                if pd.isna(raw_contents): raw_contents = "—"
                if pd.isna(raw_notes): raw_notes = "—"

                if raw_notes not in ["—", "", None]:
                    final_notes = f"{ai_metrics} {raw_notes}"
                else:
                    final_notes = ai_metrics

                rows.append({
                    "Cat #": f"M{i+1}", 
                    "CATEGORY": item.get("category", "Other"),
                    "ITEM / DESCRIPTION": item.get("item_name", "—"),
                    "NSN": nsn,
                    "UNIT": item.get("unit") if item.get("unit") else ex_unit, 
                    "Role 1 (BAS)": item.get("role1") or cat_data.get("Role 1 (BAS)", stk if ech == "Role1" else "—"),
                    "Role 2 (FSE)": item.get("role2") or cat_data.get("Role 2 (FSE)", stk if ech == "Role2" else "—"),
                    "Role 2+ (E-FST)": item.get("role2_plus") or cat_data.get("Role 2+ (E-FST)", "—"),
                    "FST": item.get("fst") or cat_data.get("FST", "—"),
                    "Role 3 (CSH)": item.get("role3") or cat_data.get("Role 3 (CSH)", stk if ech == "Role3" else "—"),
                    "FSC": item.get("fsc") if item.get("fsc") else ex_fsc,
                    "CONTENTS / SPECIFICATION": raw_contents,
                    "CoTCCC / Clinical Ref": item.get("cotccc") if item.get("cotccc") else ex_cotccc,
                    "Sterile ?": item.get("sterile") if item.get("sterile") else ex_sterile,
                    "NOTES / PROCUREMENT": final_notes,
                    "HoS Tier": tier 
                })
                
            df = pd.DataFrame(rows)
            
            def color_tier(val):
                c = {"GREEN":"background-color:#0d2818;color:#3fb950;font-weight:bold;",
                     "TEAL":  "background-color:#0d2626;color:#1f9e9e;font-weight:bold;",
                     "AMBER": "background-color:#2d1f00;color:#e3b341;font-weight:bold;",
                     "RED":   "background-color:#2d0d0d;color:#f85149;font-weight:bold;",
                     "PURPLE":"background-color:#1a0d2d;color:#8b5cf6;font-weight:bold;"}
                return c.get(val,"")

            # --- DELETE MODE LOGIC ---
            if st.session_state.delete_mode:
                st.warning("⚠️ **DELETE MODE ACTIVE:** Check the boxes of the items you want to remove, then click Confirm.")
                
                # Insert a boolean column at the front for checkboxes
                df.insert(0, "Select", False)
                
                # Render an editable dataframe
                edited_df = st.data_editor(
                    df,
                    hide_index=True,
                    use_container_width=True,
                    height=520,
                    # Disable editing for everything EXCEPT the "Select" checkbox column
                    disabled=[col for col in df.columns if col != "Select"], 
                    column_config={
                        "Select": st.column_config.CheckboxColumn("Delete?", default=False),
                        "CONTENTS / SPECIFICATION": st.column_config.TextColumn(width="large"),
                        "NOTES / PROCUREMENT": st.column_config.TextColumn(width="large"),
                        "ITEM / DESCRIPTION": st.column_config.TextColumn(width="medium")
                    }
                )
                
                # Find which rows the user checked
                items_to_delete = edited_df[edited_df["Select"] == True]["NSN"].tolist()
                
                col_confirm, _ = st.columns([1, 4])
                with col_confirm:
                    if st.button("🚨 Confirm Deletion", type="primary"):
                        if items_to_delete:
                            # Send the list of IDs to delete to the backend API
                            response = api_post("/delete_items", {"item_ids": items_to_delete})
                            if response:
                                st.success(f"✅ Successfully deleted {len(items_to_delete)} items!")
                                st.session_state.delete_mode = False
                                time.sleep(1) # Pause briefly to let the user read the success message
                                st.rerun()
                        else:
                            st.info("No items selected.")
                            
            # --- NORMAL MODE LOGIC ---
            else:
                styled_df = df.style.map(color_tier, subset=["HoS Tier"]) \
                                    .set_properties(subset=["Role 1 (BAS)", "Role 2 (FSE)", "Role 2+ (E-FST)", "FST", "Role 3 (CSH)", "UNIT", "Cat #", "FSC", "Sterile ?"], **{'text-align': 'center'}) \
                                    .hide(subset=["HoS Tier"], axis=1)
                                    
                st.dataframe(
                    styled_df, 
                    use_container_width=True, 
                    height=520, 
                    hide_index=True,
                    column_config={
                        "CONTENTS / SPECIFICATION": st.column_config.TextColumn(width="large"),
                        "NOTES / PROCUREMENT": st.column_config.TextColumn(width="large"),
                        "ITEM / DESCRIPTION": st.column_config.TextColumn(width="medium")
                    }
                )
    # ── TAB 2: QR SCANNER ─────────────────────────────────────────────────────
  
    with tab2:
        st.subheader("🔍 Item Search & Registration")
        col_scan, col_qr = st.columns([3, 2])
        with col_scan:
            st.markdown("#### Search Inventory / Look Up Online")
            
            # Toggle for Medicine vs Equipment
            search_type = st.radio("Item Type", ["💊 Medicine", "🩺 Medical Equipment"], horizontal=True)
            
            st.caption("Type any item name or ID to look it up in inventory or search online.")
            raw = None
            
            # ── STEP 1: Convert generic name to FDA name ──────────────────────
            # Only run this step if Medicine is selected
            if search_type == "💊 Medicine":
                st.markdown("**Step 1 — Convert to FDA name** *(optional)*")
                col_inp, col_btn = st.columns([3,1])
                with col_inp:
                    generic_input = st.text_input(
                        "Generic / Brand name",
                        placeholder="e.g. paracetamol, adrenaline, salbutamol",
                        key="generic_input",
                        label_visibility="collapsed"
                    )
                with col_btn:
                    convert_clicked = st.button("🔄 Convert", use_container_width=True, key="convert_btn")
                
                if convert_clicked and generic_input:
                    with st.spinner("Converting..."):
                        import requests as req2
                        name_map_local = {
                            "paracetamol":"acetaminophen","adrenaline":"epinephrine",
                            "pethidine":"meperidine","lignocaine":"lidocaine",
                            "salbutamol":"albuterol","frusemide":"furosemide",
                            "amoxycillin":"amoxicillin","morphine":"morphine sulfate",
                            "amlodipine":"amlodipine besylate","cephalexin":"cefalexin",
                        }
                        name_lower = generic_input.lower().strip()
                        fda_name   = None
                        source     = ""
                        for gen, fda in name_map_local.items():
                            if gen in name_lower:
                                fda_name = fda.title()
                                source   = "Local conversion map"
                                break
                        if not fda_name:
                            try:
                                url  = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={generic_input}&search=1"
                                resp = req2.get(url, timeout=5)
                                if resp.status_code == 200:
                                    rxcui = resp.json().get("idGroup",{}).get("rxnormId",[None])[0]
                                    if rxcui:
                                        nurl  = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/property.json?propName=RxNorm%20Name"
                                        nresp = req2.get(nurl, timeout=5)
                                        if nresp.status_code == 200:
                                            props = nresp.json().get("propConceptGroup",{}).get("propConcept",[])
                                            if props:
                                                fda_name = props[0].get("propValue", generic_input)
                                                source   = "RxNorm Database"
                            except:
                                pass
                        if not fda_name:
                            fda_name = generic_input.title()
                            source   = "No conversion found — using as-is"
                        st.session_state["fda_name"]   = fda_name
                        st.session_state["fda_source"] = source
                
                if st.session_state.get("fda_name"):
                    src = st.session_state["fda_source"]
                    st.markdown(f"""
                    <div style='background:#0d2818;border:1px solid #238636;border-radius:8px;
                                padding:10px 14px;margin:6px 0'>
                      <span style='color:#8b949e;font-size:11px'>FDA Name ({src}):</span><br>
                      <span style='color:#3fb950;font-size:16px;font-weight:500'>
                        {st.session_state["fda_name"]}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("---")
                
            # ── STEP 2: Search & Look Up ──────────────────────────────────────
            st.markdown("**Step 2 — Search inventory or look up online**")
            default_search = st.session_state.get("fda_name","") if search_type == "💊 Medicine" else ""
            manual_id = st.text_input(
                "Item name or ID",
                value=default_search,
                placeholder="e.g. Acetaminophen, Chest Drain, or ITM004",
                key="manual_qr"
            )
            if manual_id:
                raw = manual_id.strip()
            
            if raw and st.button("🔍 Search & Look Up", use_container_width=True, key="lookup_btn"):
                inv_all = api_get("/inventory")
                found = next((i for i in inv_all
                    if i["item_id"].lower() == raw.lower()
                    or i["item_name"].lower() == raw.lower()), None)
                
                if found:
                    st.session_state["matched_item"]   = found
                    st.session_state["search_no_match"] = False
                    st.session_state.register_mode     = False
                    st.session_state["med_info"]       = None
                else:
                    st.session_state["matched_item"]   = None
                    st.session_state["search_no_match"] = True
                    st.session_state["search_raw"]     = raw
            
            # Show matched item persistently across reruns
            matched = st.session_state.get("matched_item")
            if matched:
                inv_all  = api_get("/inventory")
                matched  = next((i for i in inv_all if i["item_id"] == matched["item_id"]), matched)
                tc = HOS_COLOR.get(matched.get("hos_tier","GREEN"),"#3fb950")
                st.markdown(f"""
                <div style='background:#0d2818;border:1px solid #238636;
                            border-radius:10px;padding:14px;margin:8px 0'>
                  <h4 style='color:#3fb950;margin:0'>✅ Already in MMLS-AI Inventory</h4>
                  <p style='color:#c9d1d9;margin:6px 0 2px;font-size:14px'>
                    <b>{matched["item_name"]}</b> ({matched["item_id"]})</p>
                  <p style='color:#8b949e;margin:0;font-size:12px'>
                    Category: {matched["category"]} · Echelon: {matched["echelon"]}<br>
                    Current Stock: <b>{matched["current_stock"]}</b> units ·
                    Alert Threshold: {matched["alert_threshold"]}<br>
                    Hours of Supply: <span style='color:{tc}'>
                    {matched.get("hours_of_supply","—")}h ({matched.get("hos_tier","—")})</span>
                  </p>
                </div>""", unsafe_allow_html=True)
                
                qty_scan  = st.number_input("Quantity Used", 1, 50, 1, key="qrqty2")
                user_scan = st.text_input("User ID", value=st.session_state.username, key="qrusr2")
                col_rec, col_clr = st.columns(2)
                with col_rec:
                    if st.button("✅ Record Usage", use_container_width=True, key="rec2"):
                        r = api_post("/scan",{"item_id":matched["item_id"],
                                              "quantity_used":qty_scan,
                                              "user":user_scan})
                        if r:
                            if r.get("alert"):
                                st.error(f"⚠️ LOW STOCK: {r['item_name']} → {r['new_stock']} left")
                            else:
                                st.success(f"✅ Recorded — New stock: {r['new_stock']}")
                            st.session_state["matched_item"] = None
                            st.rerun()
                with col_clr:
                    if st.button("✖ Clear", use_container_width=True, key="clr_match"):
                        st.session_state["matched_item"] = None
                        st.rerun()
            
            # NOT IN INVENTORY — search online or in BST Catalog
            elif st.session_state.get("search_no_match"):
                raw = st.session_state.get("search_raw", raw)
                if True:
                    st.markdown(f"""
                    <div style='background:#2d1f00;border:1px solid #e3b341;
                                border-radius:8px;padding:10px;margin:6px 0'>
                      <b style='color:#e3b341'>⚠️ Not found in inventory.</b>
                      <span style='color:#8b949e;font-size:12px'>
                      Searching BST NSN Catalog and online databases...</span>
                    </div>""", unsafe_allow_html=True)
                    
                    with st.spinner(f"🔍 Looking up '{raw}'..."):
                        try:
                            import requests as req
                            
                            med_info = {}
                            search_name = raw.lower()
                            
                            # ── 1. SEARCH LOCAL BST NSN CATALOG FIRST (EXCEL) ──
                            try:
                                import re
                                all_sheets = pd.read_excel("BST_Medical_Consumables_NSN_v2.xlsx", sheet_name=None)
                                
                                for sheet_name, sheet_df in all_sheets.items():
                                    mask = sheet_df.astype(str).apply(lambda col: col.str.lower().str.contains(search_name, na=False))
                                    match = sheet_df[mask.any(axis=1)]
                                    
                                    if not match.empty:
                                        matched_row = match.iloc[0]
                                        
                                        # -- SMART HEADER FINDER --
                                        # Excel files often have titles in the first few rows. 
                                        # We scan the first 10 rows to find the REAL column headers.
                                        header_idx = -1
                                        for r_idx in range(min(10, len(sheet_df))):
                                            row_str = " ".join(sheet_df.iloc[r_idx].astype(str).str.upper())
                                            if "CATEGORY" in row_str and ("NSN" in row_str or "ITEM" in row_str):
                                                header_idx = r_idx
                                                break
                                                
                                        if header_idx != -1:
                                            real_headers = sheet_df.iloc[header_idx].astype(str).str.upper().str.replace('\n', ' ')
                                        else:
                                            real_headers = pd.Series([str(c).upper().replace('\n', ' ') for c in sheet_df.columns])
                                        
                                        # Helper function to grab values using the REAL headers
                                        def get_smart_val(search_strs, default="—"):
                                            for i, h in enumerate(real_headers):
                                                if any(s in h for s in search_strs):
                                                    val = str(matched_row.iloc[i]).strip()
                                                    return val if val.lower() not in ['nan', 'none', ''] else default
                                            return default

                                        nsn_match = re.search(r'\d{4}-\d{2}-\d{3}-\d{4}', str(matched_row.values))
                                        nsn_code = nsn_match.group(0) if nsn_match else "Unknown NSN"
                                        
                                        item_name = raw.title()
                                        for cell in matched_row.values:
                                            if search_name in str(cell).lower():
                                                item_name = str(cell).replace('\n', ' ').strip()
                                                break

                                        # Extract ALL exact Excel columns using our smart finder!
                                        med_info = {
                                            "medicine_name": f"{item_name} (NSN: {nsn_code})",
                                            "category": get_smart_val(["CATEGORY"], "Equipment"),
                                            "unit": get_smart_val(["UNIT"], "ea"),
                                            "role1": get_smart_val(["ROLE 1"], "—"),
                                            "role2": get_smart_val(["ROLE 2 (FSE)", "FSE"], "—"),
                                            "role2_plus": get_smart_val(["ROLE 2+", "E-FST"], "—"),
                                            "fst": get_smart_val(["FST"], "—"),
                                            "role3": get_smart_val(["ROLE 3", "CSH"], "—"),
                                            "fsc": get_smart_val(["FSC"], "—"),
                                            "contents": get_smart_val(["CONTENTS", "SPECIFICATION"], "—"),
                                            "cotccc": get_smart_val(["COTCCC", "CLINICAL"], "—"),
                                            "sterile": get_smart_val(["STERILE"], "YES"),
                                            "notes": get_smart_val(["NOTES", "PROCUREMENT"], "—"),
                                            "source": f"BST NSN Database ({sheet_name})",
                                            # Fallbacks for backend calculation
                                            "controlled": False, 
                                            "suggested_stock": 50, "suggested_threshold": 10,
                                            "suggested_consumption_per_hour": 1.0, "expiry_days": 1095,
                                        }
                                        break  
                            except Exception as e:
                                pass # Silent fail, proceed to API fallback
                            
                            # ── 2. FALLBACK TO FDA / WIKIPEDIA IF NOT IN CATALOG ──
                            if not med_info:
                                if search_type == "🩺 Medical Equipment":
                                    # ── FDA DEVICE CLASSIFICATION DATABASE ──
                                    try:
                                        search_term = search_name.replace(" ", "+")
                                        fda_url = f"https://api.fda.gov/device/classification.json?search=device_name:{search_term}&limit=1"
                                        fda_resp = req.get(fda_url, timeout=8)
                                        if fda_resp.status_code == 200:
                                            result = fda_resp.json()["results"][0]
                                            device_name = result.get("device_name", raw.title())
                                            specialty = result.get("medical_specialty_description", "Other")
                                            description = result.get("definition", f"Medical Device. Specialty: {specialty}")
                                            
                                            spec_lower = specialty.lower()
                                            if "orthopedic" in spec_lower: cat = "Orthopaedic"
                                            elif "anesthesiology" in spec_lower: cat = "Anaesthetic"
                                            elif "cardiovascular" in spec_lower: cat = "Haemostasis"
                                            else: cat = "Equipment"
                                            
                                            med_info = {
                                                "medicine_name": device_name.title(),
                                                "category": cat,
                                                "description": description[:250],
                                                "typical_use": f"Classification: {specialty}",
                                                "storage": "Clean, dry environment",
                                                "controlled": False,
                                                "echelon": "Role2",
                                                "suggested_stock": 20,
                                                "suggested_threshold": 5,
                                                "suggested_consumption_per_hour": 0.5,
                                                "expiry_days": 1825,
                                                "source": "FDA Device Database"
                                            }
                                    except Exception:
                                        pass
                                else:
                                    # ── FDA DRUG LABEL DATABASE ──
                                    name_map = {
                                        "paracetamol": "acetaminophen", "adrenaline": "epinephrine",
                                        "pethidine": "meperidine", "lignocaine": "lidocaine",
                                        "salbutamol": "albuterol", "frusemide": "furosemide",
                                        "amoxycillin": "amoxicillin",
                                    }
                                    for uk, us in name_map.items():
                                        if uk in search_name:
                                            search_name = search_name.replace(uk, us)
                                    try:
                                        search_term = search_name.split()[0]
                                        fda_url  = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:%22{search_term}%22&limit=1"
                                        fda_resp = req.get(fda_url, timeout=8)
                                        if fda_resp.status_code == 200:
                                            result   = fda_resp.json()["results"][0]
                                            openfda  = result.get("openfda", {})
                                            brand   = openfda.get("brand_name",  [raw.title()])[0]
                                            generic = openfda.get("generic_name",[""])[0]
                                            route   = openfda.get("route",       ["oral"])[0]
                                            pharm_class_str = ", ".join(openfda.get("pharm_class_epc", []))
                                            
                                            purpose = ""
                                            for field in ["purpose","indications_and_usage","description","clinical_pharmacology"]:
                                                val = result.get(field)
                                                if val and val[0].strip():
                                                    purpose = val[0].strip()
                                                    break
                                            
                                            junk_phrases = ["INDICATIONS AND USAGE","PURPOSE","DESCRIPTION","WARNING","See full prescribing information"]
                                            for junk in junk_phrases:
                                                purpose = purpose.replace(junk, "").replace(junk.upper(), "").strip()
                                            
                                            sentences = [s.strip() for s in purpose.replace("\\n"," ").split(".") if len(s.strip()) > 20]
                                            purpose = ". ".join(sentences[:2])[:250] if sentences else ""
                                            
                                            if not purpose or len(purpose) < 30:
                                                if pharm_class_str: purpose = f"{brand} is classified as: {pharm_class_str}. Used as a {route.lower()} medication."
                                                else: purpose = f"{brand} ({generic}) — {route} medication."
                                                
                                            storage = (result.get("storage_and_handling") or ["Store at room temperature"])[0][:120].strip()
                                            controlled = any(x in str(result).lower() for x in ["schedule ii","schedule iii","schedule iv","controlled substance","opioid"])
                                            
                                            name_lower = (brand + " " + generic + " " + search_name).lower()
                                            all_text = name_lower + " " + str(openfda.get("pharm_class_epc",[])).lower()
                                            if any(x in all_text for x in ["acetaminophen","ibuprofen","morphine","fentanyl","opioid","analgesic"]): cat = "Analgesic"
                                            elif any(x in all_text for x in ["ketamine","propofol","lidocaine","anesthetic","sedative"]): cat = "Anaesthetic"
                                            elif any(x in all_text for x in ["antibiotic","amoxicillin","penicillin"]): cat = "Other"
                                            else: cat = "Other"
                                            
                                            med_info = {
                                                "medicine_name": f"{brand} ({generic})" if generic else brand,
                                                "category": cat,
                                                "description": purpose,
                                                "typical_use": purpose[:150],
                                                "storage": storage,
                                                "controlled": controlled,
                                                "echelon": "Role1",
                                                "suggested_stock": 50,
                                                "suggested_threshold": 10,
                                                "suggested_consumption_per_hour": 2.0,
                                                "expiry_days": 365,
                                                "source": "FDA Drug Database"
                                            }
                                    except Exception:
                                        pass

                                # ── FALLBACK FOR BOTH (Wikipedia or generic) ──
                                if not med_info:
                                    try:
                                        wiki_url  = f"https://en.wikipedia.org/api/rest_v1/page/summary/{raw.replace(' ','_')}"
                                        wiki_resp = req.get(wiki_url, timeout=8)
                                        if wiki_resp.status_code == 200:
                                            wiki = wiki_resp.json()
                                            summary = wiki.get("extract","")[:300]
                                            name_low = raw.lower()
                                            med_info = {
                                                "medicine_name": wiki.get("title", raw),
                                                "category": "Equipment" if search_type == "🩺 Medical Equipment" else "Other",
                                                "description": summary,
                                                "typical_use": summary[:150],
                                                "storage": "Room temperature",
                                                "controlled": any(x in name_low for x in ["morphine","fentanyl","ketamine"]) if search_type == "💊 Medicine" else False,
                                                "echelon": "Role2" if search_type == "🩺 Medical Equipment" else "Role1",
                                                "suggested_stock": 20 if search_type == "🩺 Medical Equipment" else 50,
                                                "suggested_threshold": 5 if search_type == "🩺 Medical Equipment" else 10,
                                                "suggested_consumption_per_hour": 0.5 if search_type == "🩺 Medical Equipment" else 2.0,
                                                "expiry_days": 1825 if search_type == "🩺 Medical Equipment" else 365,
                                                "source": "Wikipedia"
                                            }
                                    except Exception:
                                        pass

                                # Final Manual Fallback
                                if not med_info:
                                    med_info = {
                                        "medicine_name": raw,
                                        "category": "Equipment" if search_type == "🩺 Medical Equipment" else "Other",
                                        "description": f"{search_type.split()[1]} item: {raw}. Please fill details.",
                                        "typical_use": "Please specify",
                                        "storage": "Standard",
                                        "controlled": False,
                                        "echelon": "Role1",
                                        "suggested_stock": 20,
                                        "suggested_threshold": 5,
                                        "suggested_consumption_per_hour": 1.0,
                                        "expiry_days": 365,
                                        "source": "Manual Entry"
                                    }
                                    
                            st.session_state["med_info"]   = med_info
                            st.session_state["med_raw"]    = raw
                            st.session_state.register_mode = True

                        except Exception as e:
                            st.error(f"Search error: {e}")
                            st.session_state.register_mode = False
                
                # Show pre-filled register form
                if st.session_state.register_mode and st.session_state.get("med_info"):
                    med = st.session_state["med_info"]
                    st.markdown("---")
                    source = med.get("source","Online")
                    st.markdown(f"""
                    <div style='background:#161b22;border:1px solid #58a6ff;border-radius:10px;padding:16px;margin:8px 0'>
                      <div style='display:flex;justify-content:space-between;align-items:center'>
                        <h4 style='color:#58a6ff;margin:0'>🌐 Info Found Online</h4>
                        <span style='background:#1c2d4a;color:#58a6ff;font-size:10px;padding:2px 8px;border-radius:20px;border:1px solid #58a6ff44'>{source}</span>
                      </div>
                      <p style='color:#c9d1d9;margin:8px 0 4px;font-size:15px;font-weight:500'>{med.get("medicine_name","—")}</p>
                      <p style='color:#8b949e;margin:0 0 8px;font-size:12px;line-height:1.6'><b>Contents:</b> {med.get("contents", "—")[:250]}...</p>
                    </div>""", unsafe_allow_html=True)
                    
                    st.markdown("#### Add to MMLS-AI Inventory")
                    cats = ["Analgesic","Anaesthetic","Haemostasis","Thoracic","Transfusion","IV Therapy","IV Access","Airway","Equipment","PPE","Burns","Trauma","Orthopaedic","DCO/DCS","Other", "General Surgery", "Neurosurgery"]
                    default_cat = med.get("category","Other")
                    cat_idx = cats.index(default_cat) if default_cat in cats else len(cats)-1
                    _inv_count = len(api_get("/inventory"))
                    
                    med_name_full = med.get("medicine_name", raw)
                    extracted_nsn = ""
                    clean_name = med_name_full
                    if "(NSN:" in med_name_full:
                        parts = med_name_full.split("(NSN:")
                        clean_name = parts[0].strip()
                        extracted_nsn = parts[1].replace(")", "").strip()
                    
                    col_f1, col_f2 = st.columns(2)
                    with col_f1:
                        r_nsn  = st.text_input("NSN (NATO Stock Number)", value=extracted_nsn if extracted_nsn else f"ITM{str(_inv_count+1).zfill(3)}")
                        r_name = st.text_input("ITEM / DESCRIPTION", value=clean_name)
                        r_cat  = st.selectbox("CATEGORY", cats, index=cat_idx)
                        r_unit = st.text_input("UNIT", value=med.get("unit", "ea"))
                        r_fsc  = st.text_input("FSC", value=med.get("fsc", "—"))
                        r_cotccc = st.text_input("CoTCCC / Clinical Ref", value=med.get("cotccc", "—"))
                        r_sterile = st.text_input("Sterile?", value=med.get("sterile", "YES"))

                    with col_f2:
                        r_role1 = st.text_input("Role 1 (BAS)", value=med.get("role1", "—"))
                        r_role2 = st.text_input("Role 2 (FSE)", value=med.get("role2", "—"))
                        r_role2p = st.text_input("Role 2+ (E-FST)", value=med.get("role2_plus", "—"))
                        r_fst = st.text_input("FST", value=med.get("fst", "—"))
                        r_role3 = st.text_input("Role 3 (CSH)", value=med.get("role3", "—"))
                        
                        echs = ["Role1","Role2","Role3"]
                        r_ech = st.selectbox("Assign AI Echelon", echs, index=0)
                        r_stk = st.number_input("Initial AI Stock", 1, 1000, int(med.get("suggested_stock", 50)))

                    r_contents = st.text_area("CONTENTS / SPECIFICATION", value=med.get("contents", "—"))
                    r_notes = st.text_area("NOTES / PROCUREMENT", value=med.get("notes", "—"))
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save_clicked = st.button("💾 Add to Inventory", use_container_width=True, key="save_med")
                    with col_cancel:
                        if st.button("✖ Cancel", use_container_width=True, key="cancel_med"):
                            st.session_state.register_mode = False; st.rerun()
                            
                    if save_clicked:
                        payload = {
                            "item_id": r_nsn.strip(), "item_name": r_name.strip(),
                            "category": r_cat, "unit": r_unit,
                            "role1": r_role1, "role2": r_role2, "role2_plus": r_role2p,
                            "fst": r_fst, "role3": r_role3, "fsc": r_fsc,
                            "contents": r_contents, "cotccc": r_cotccc,
                            "sterile": r_sterile, "notes": r_notes,
                            "echelon": r_ech, "current_stock": int(r_stk),
                            "initial_stock": int(r_stk), "alert_threshold": 10,
                            "avg_consumption_per_hour": 1.0, "expiry_days": 365, "pack_type": "Standalone"
                        }
                        try:
                            code, resp = api_post_raw("/register_item", payload)
                            if code == 200:
                                st.session_state["last_registered"] = r_name
                                st.session_state.register_mode      = False
                                st.session_state["med_info"]        = None
                                st.session_state["fda_name"]        = ""
                                st.session_state.qr_result          = None
                                st.balloons()
                                st.success(f"✅ **{r_name}** added to MMLS-AI inventory! Go to Inventory tab to see it.")
                            elif code == 409:
                                st.warning(f"⚠️ Item ID **{r_nsn}** already exists. Change the Item ID and try again.")
                            else:
                                st.error(f"Registration failed: {resp}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    
                    if st.session_state.get("last_registered"):
                        st.info(f"Last registered: **{st.session_state['last_registered']}** — search a new item above")


       

    # ── TAB 3: XGBOOST FORECAST ───────────────────────────────────────────────
    if tab3:
        with tab3:
            st.subheader("XGBoost AI Demand Forecast")
            c1,c2,c3,c4 = st.columns(4)
            with c1: tempo = st.slider("Operational Tempo",0.1,1.0,0.5,0.05)
            with c2: t1    = st.slider("T1 Severe",        0.0,0.5,0.2,0.05)
            with c3: t2    = st.slider("T2 Moderate",      0.0,0.4,0.2,0.05)
            with c4: t3    = st.slider("T3 Minor",         0.0,0.4,0.1,0.05)
            if st.button("🤖 Run XGBoost Forecast", use_container_width=True):
                data = api_get(f"/forecast?operational_tempo={tempo}&t1={t1}&t2={t2}&t3={t3}")
                if data and "predictions" in data:
                    preds = data["predictions"]
                    df_p  = pd.DataFrame(preds)
                    col_chart, col_fi = st.columns([3,2])
                    with col_chart:
                        # Shorten names to 30 chars so they look clean
                        df_p["short_name"] = df_p["item_name"].apply(lambda x: x if len(str(x)) < 30 else str(x)[:27] + "...")
                        
                        fig = px.bar(df_p.sort_values("predicted_rate"),
                            x="predicted_rate", y="short_name", orientation="h",
                            color="hos_tier", color_discrete_map=HOS_COLOR,
                            title=f"Predicted Consumption — Tempo:{tempo} T1:{t1} T2:{t2} T3:{t3}",
                            labels={"predicted_rate":"Rate (u/hr)", "short_name":""},
                            hover_data={"item_name": True}) 
                            
                        # Removed the restrictive left margin (l=10)
                        fig.update_layout(plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                                          font_color="#c9d1d9", height=480, title_font_size=12,
                                          margin=dict(r=20, t=40, b=20)) 
                        
                        # Force Plotly to automatically make room for the text labels
                        fig.update_yaxes(automargin=True)
                        fig.update_xaxes(rangemode="tozero")
                        
                        st.plotly_chart(fig, use_container_width=True, theme=None)
                    with col_fi:
                        st.markdown("**Feature Importance (XGBoost)**")
                        if os.path.exists("feature_importance.png"):
                            st.image("feature_importance.png", width=400)
                        else:
                            st.info("Run train_model.py to generate feature_importance.png")
                    df_show = df_p[["item_id","item_name","current_stock",
                                    "predicted_rate","hours_of_supply","hos_tier"]]
                    df_show.columns = ["ID","Name","Stock","Rate (u/hr)","HoS (hrs)","Tier"]
                    st.dataframe(df_show, use_container_width=True)

    # ── TAB 6: LSTM TREND ─────────────────────────────────────────────────────
    if tab6:
        with tab6:
            st.subheader("LSTM Surge Trend Model")
            st.caption("LSTM predicts consumption trends over time — detects MASCAL surges.")
            try:
                actual    = np.load("lstm_actual.npy")
                preds_arr = np.load("lstm_preds.npy")
                hours_arr = np.load("lstm_hours.npy")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hours_arr,y=actual,name="Actual",
                    line=dict(color="#58a6ff",width=2)))
                fig.add_trace(go.Scatter(x=hours_arr,y=preds_arr,name="LSTM Predicted",
                    line=dict(color="#f85149",width=2,dash="dash")))
                fig.add_vline(x=24,line_dash="dot",line_color="#e3b341",
                    annotation_text="MASCAL Surge →",annotation_position="top left")
                fig.update_layout(
                    title="LSTM: 48-Hour Consumption Trend — CAT Tourniquet (MASCAL surge at H+24)",title_font=dict(color="#ffffff", size=16),
                    xaxis_title="Hour",yaxis_title="Consumption Rate (units/hr)",
                    plot_bgcolor="#0d1117",paper_bgcolor="#161b22",
                    font=dict(color="#c9d1d9"),height=420,
                   legend=dict(
                        bgcolor="#161b22",
                        font=dict(color="#c9d1d9"), 
                        bordercolor="#30363d",      
                        borderwidth=1))
                st.plotly_chart(fig, use_container_width=True,theme=None)
                from sklearn.metrics import r2_score, mean_squared_error
                r2  = r2_score(actual, preds_arr)
                mse = mean_squared_error(actual, preds_arr)
                c1,c2,c3 = st.columns(3)
                with c1: st.metric("LSTM R²",  f"{r2:.4f}")
                with c2: st.metric("LSTM MSE", f"{mse:.4f}")
                with c3: st.metric("Purpose",  "Surge Detection")
                st.info("💡 LSTM tracks consumption trends over time. XGBoost predicts per-item demand. Together they provide complete AI coverage.")
            except FileNotFoundError:
                st.warning("LSTM files not found. Make sure lstm_actual.npy, lstm_preds.npy, lstm_hours.npy are in the mmsai folder.")

    # ── TAB 4: HOURS OF SUPPLY ────────────────────────────────────────────────
    with tab4:
        st.subheader("Hours of Supply — Live Status")
        hos_data = api_get("/hours_of_supply")
        if hos_data:
            tier_counts = {}
            for item in hos_data:
                t = item["hos_tier"]
                tier_counts[t] = tier_counts.get(t,0)+1
            cols = st.columns(5)
            for col,tier in zip(cols,["GREEN","TEAL","AMBER","RED","PURPLE"]):
                with col:
                    st.markdown(f"""<div class='hos-{tier}'>
                      <p style='margin:0;font-size:10px;color:#8b949e'>{tier}</p>
                      <h2 style='margin:4px 0;color:{HOS_COLOR[tier]}'>{tier_counts.get(tier,0)}</h2>
                    </div>""", unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            df_h = pd.DataFrame(hos_data).sort_values("hours_of_supply")
            colors = [HOS_COLOR.get(t,"#58a6ff") for t in df_h["hos_tier"]]
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_h["hours_of_supply"],y=df_h["item_name"],
                orientation="h",marker_color=colors,
                text=[f"{h}h" for h in df_h["hours_of_supply"]],
                textposition="outside"))
            for xval,color,label in [(2,"#f85149","Critical 2h"),
                                      (6,"#e3b341","AMBER 6h"),
                                      (24,"#238636","GREEN 24h")]:
                fig.add_vline(x=xval,line_dash="dash",line_color=color,
                              annotation_text=label,annotation_position="top")
            fig.update_layout(title="Hours of Supply per Item",
                plot_bgcolor="#0d1117",paper_bgcolor="#161b22",
                font_color="#c9d1d9",height=560,xaxis_title="Hours of Supply")
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 7: CROSS-ECHELON MAP ──────────────────────────────────────────────
    if tab7:
        with tab7:
            st.subheader("Cross-Echelon Supply Chain View")
            st.caption("Multi-echelon visibility across Role 1, 2 and 3 facilities")
            st.caption("Positioning inputs: geographic coordinates reflect a realistic theatre layout — R1 forward (closest to contact), R2 mid-distance (FST), R3 rear area (general hospital). Nodes are ~80-120 km apart to represent typical echelon spacing in LSCO.")
            echelons = [
                {"node":"R1-ALPHA","role":"Role 1","lat":28.30,"lon":76.80,
                 "items":8,"avg_hos":round(random.uniform(6,18),1),"tier":"AMBER","personnel":12},
                {"node":"R2-BRAVO","role":"Role 2","lat":28.55,"lon":77.18,
                 "items":7,"avg_hos":round(random.uniform(14,26),1),"tier":"TEAL","personnel":28},
                {"node":"R3-CHARLIE","role":"Role 3","lat":28.85,"lon":77.60,
                 "items":20,"avg_hos":round(random.uniform(28,48),1),"tier":"GREEN","personnel":85},
            ]
            df_eco = pd.DataFrame(echelons)
            col_map, col_tbl = st.columns([2,1])
            with col_map:
                fig = go.Figure()
                for _,row in df_eco.iterrows():
                    fig.add_trace(go.Scattergeo(
                        lon=[row["lon"]],lat=[row["lat"]],
                        mode="markers+text",
                        marker=dict(size=14,color=HOS_COLOR[row["tier"]],
                                    line=dict(width=2,color="white")),
                        text=[row["node"]],textposition="bottom center",
                        textfont=dict(color="#ffffff",size=11),
                        name=f"{row['node']} ({row['tier']})",
                        hovertemplate=f"<b>{row['node']}</b><br>Role: {row['role']}<br>Avg HoS: {row['avg_hos']}h<br>Tier: {row['tier']}<extra></extra>"))
                for i in range(len(echelons)-1):
                    fig.add_trace(go.Scattergeo(
                        lon=[echelons[i]["lon"],echelons[i+1]["lon"]],
                        lat=[echelons[i]["lat"],echelons[i+1]["lat"]],
                        mode="lines",line=dict(width=2,color="#8b949e"),showlegend=False))
                fig.update_layout(
                    title="Echelon Supply Chain",title_font=dict(color="#ffffff", size=16),font=dict(color="#c9d1d9"),
                    geo=dict(showland=True,landcolor="#161b22",showocean=True,
                             oceancolor="#0d1117",showcountries=True,countrycolor="#30363d",
                             center=dict(lat=28.55,lon=77.18),projection_scale=3.5,
                             bgcolor="#0d1117"),
                    paper_bgcolor="#161b22",font_color="#c9d1d9",height=420,margin=dict(l=0, r=0, t=40, b=0),
                    legend=dict(
                        bgcolor="#161b22",
                        font=dict(color="#c9d1d9", size=12), 
                        bordercolor="#30363d",
                        borderwidth=1))
                st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
            with col_tbl:
                st.markdown("**Node Status**")
                for _,row in df_eco.iterrows():
                    tc = HOS_COLOR[row["tier"]]
                    st.markdown(f"""
                    <div style='background:#161b22;border:1px solid #30363d;
                                border-left:3px solid {tc};border-radius:8px;
                                padding:10px 12px;margin-bottom:8px'>
                      <b style='color:#c9d1d9;font-size:13px'>{row["node"]}</b>
                      <span style='color:{tc};font-size:11px;float:right'>{row["tier"]}</span><br>
                      <span style='color:#8b949e;font-size:11px'>{row["role"]} · {row["personnel"]} personnel<br>
                      Avg HoS: {row["avg_hos"]}h · {row["items"]} item types</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("**Resupply Pipeline**")
                for p in [
                    {"from":"R3-CHARLIE","to":"R2-BRAVO","item":"IV Fluids x50","eta":"2h","status":"🚛 In Transit"},
                    {"from":"R2-BRAVO","to":"R1-ALPHA","item":"Tourniquets x20","eta":"45min","status":"📦 Packed"},
                ]:
                    st.markdown(f"""
                    <div style='background:#161b22;border:1px solid #30363d;border-radius:6px;
                                padding:8px 10px;margin-bottom:6px;font-size:11px'>
                      {p["status"]} <b style='color:#c9d1d9'>{p["item"]}</b><br>
                      <span style='color:#8b949e'>{p["from"]} → {p["to"]} · ETA: {p["eta"]}</span>
                    </div>""", unsafe_allow_html=True)

    # ── TAB 8: VALIDATION ─────────────────────────────────────────────────────
    if tab8:
        with tab8:
            st.subheader("Validation Scenarios")
            sc1,sc2,sc3 = st.tabs(["Scenario 1 — Low Stock Alert",
                                    "Scenario 2 — MASCAL Surge",
                                    "Scenario 3 — Controlled Drug Audit"])
            with sc1:
                st.markdown("**Deplete tourniquet stock until alert fires**")
                st.info("Logs 12 tourniquet uses. Stock drops below threshold (10) → LOW STOCK alert fires.")
                if st.button("▶️ Run Scenario 1", use_container_width=True):
                    results = []
                    prog = st.progress(0)
                    for i in range(12):
                        r = api_post("/scan",{"item_id":"ITM004","quantity_used":1,"user":"Validator_01"})
                        if r:
                            results.append({"Use #":i+1,"Stock After":r.get("new_stock","—"),
                                            "Alert":r.get("alert",False),"Message":r.get("message","")})
                        prog.progress((i+1)/12)
                        time.sleep(0.1)
                    df_r = pd.DataFrame(results)
                    st.dataframe(df_r, use_container_width=True)
                    if df_r["Alert"].sum() > 0:
                        st.success("✅ PASS — LOW STOCK alert fired correctly")
                    else:
                        st.warning("Stock still above threshold — run again or check seed data")

            with sc2:
                st.markdown("**MASCAL Surge — High tempo + T1 casualties**")
                c1,c2 = st.columns(2)
                with c1:
                    s2t  = st.slider("Tempo",0.1,1.0,0.9,0.05,key="s2t")
                    s2t1 = st.slider("T1",   0.0,0.5,0.4,0.05,key="s2t1")
                with c2:
                    s2t2 = st.slider("T2",0.0,0.4,0.2,0.05,key="s2t2")
                    s2t3 = st.slider("T3",0.0,0.4,0.1,0.05,key="s2t3")
                if st.button("▶️ Run MASCAL Forecast", use_container_width=True):
                    data = api_get(f"/forecast?operational_tempo={s2t}&t1={s2t1}&t2={s2t2}&t3={s2t3}")
                    if data and "predictions" in data:
                        preds = data["predictions"]
                        df_p  = pd.DataFrame(preds)
                        fig   = px.bar(df_p.sort_values("predicted_rate"),
                            x="predicted_rate",y="item_name",orientation="h",
                            color="hos_tier",color_discrete_map=HOS_COLOR,
                            title=f"MASCAL Surge — Tempo:{s2t} T1:{s2t1}",
                            labels={"predicted_rate":"Rate (u/hr)","item_name":""})
                        fig.update_layout(plot_bgcolor="#0d1117",paper_bgcolor="#161b22",
                                          font_color="#c9d1d9",height=480)
                        st.plotly_chart(fig, use_container_width=True)
                        crit = df_p[df_p["hos_tier"].isin(["RED","PURPLE"])]
                        if len(crit)>0:
                            st.error(f"⚠️ {len(crit)} items in RED/PURPLE — emergency resupply needed!")
                            st.dataframe(crit[["item_name","predicted_rate","hours_of_supply","hos_tier"]],
                                         use_container_width=True)
                            st.success("✅ PASS — Surge correctly detected and tiered")

            with sc3:
                st.markdown("**Morphine audit — administer 5 times, verify audit trail**")
                if st.button("▶️ Run Scenario 3", use_container_width=True):
                    clinicians = ["CMT_Alpha","CMT_Bravo","FST_Nurse_01","CMT_Charlie","MO_01"]
                    results = []
                    prog = st.progress(0)
                    for i,clin in enumerate(clinicians):
                        r = api_post("/scan",{"item_id":"ITM001","quantity_used":1,"user":clin})
                        if r:
                            results.append({"#":i+1,"Clinician":clin,
                                            "Stock After":r.get("new_stock","—")})
                        prog.progress((i+1)/5)
                        time.sleep(0.2)
                    st.dataframe(pd.DataFrame(results), use_container_width=True)
                    logs = api_get("/audit_log")
                    morph = [l for l in logs if l.get("item_id")=="ITM001"] if logs else []
                    st.markdown(f"**Morphine audit entries: {len(morph)}**")
                    if morph:
                        st.dataframe(pd.DataFrame(morph[:10]), use_container_width=True)
                        st.success(f"✅ PASS — All {len(morph)} morphine uses recorded in audit log")

    # ── TAB 5: AUDIT LOG ──────────────────────────────────────────────────────
    with tab5:
        st.subheader("Controlled Drug & Clinical Event Audit Log")
        if st.button("🔄 Refresh", key="ref5"): st.rerun()
        logs = api_get("/audit_log")
        if logs:
            df_l = pd.DataFrame(logs)
            st.dataframe(df_l, use_container_width=True, height=420)
            st.caption(f"Total events: {len(logs)}")
            csv = df_l.to_csv(index=False)
            st.download_button("📥 Download CSV", csv,
                               "audit_log.csv","text/csv",use_container_width=True)
        else:
            st.info("No events logged yet.")

    with tab9:
        from twin_dashboard import render_twin_dashboard
        render_twin_dashboard(API)

# ── MAIN ───────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()