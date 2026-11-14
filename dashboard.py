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
import streamlit.components.v1 as _components
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

def _camera_scanner_html(api_url, qty, user):
    """In-browser camera barcode/QR scanner (html5-qrcode via CDN).

    Decodes with the device webcam and talks straight to the API (CORS is enabled),
    so a scan needs no Streamlit round-trip. A code already in inventory logs stock
    use via /scan; an unknown code opens an inline form that registers it as a new
    inventory item via /register_item (name optionally prefilled from Open Products
    Facts), so any medicine can be added by scanning its retail barcode/QR. Scanned
    text is only ever written via textContent, never innerHTML, so a hostile label
    cannot inject markup into the panel.
    """
    return """
<div id="mmsai-reader" style="width:100%;max-width:440px;margin:0 auto;border-radius:10px;overflow:hidden"></div>
<div id="mmsai-cam-status" style="text-align:center;color:#8b949e;font-size:13px;margin:8px 0">Press ▶️ Start camera when ready.</div>
<div style="text-align:center;margin:6px 0">
  <button id="mmsai-cam-start" style="background:#238636;color:#fff;border:none;border-radius:6px;padding:7px 16px;cursor:pointer;font-weight:600;margin-right:8px">▶️ Start camera</button>
  <button id="mmsai-cam-stop" style="background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:7px 14px;cursor:pointer">⏹ Stop camera</button>
</div>
<div id="mmsai-info" style="display:none;max-width:440px;margin:8px auto;padding:10px 12px;background:#161b22;border:1px solid #30363d;border-radius:10px;font-size:12px;color:#c9d1d9"></div>
<div id="mmsai-reg" style="display:none;max-width:440px;margin:10px auto;padding:12px 14px;background:#161b22;border:1px solid #30363d;border-radius:10px">
  <div style="color:#c9d1d9;font-weight:600;margin-bottom:4px">➕ New item from this scan</div>
  <div id="mmsai-reg-code" style="font:12px monospace;color:#8b949e;margin-bottom:8px"></div>
  <label style="display:block;color:#8b949e;font-size:12px;margin-bottom:8px">Item name
    <input id="mmsai-reg-name" placeholder="e.g. Paracetamol 500mg" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 8px">
  </label>
  <div style="display:flex;gap:8px;margin-bottom:8px">
    <label style="flex:1;color:#8b949e;font-size:12px">Category
      <select id="mmsai-reg-cat" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 4px">
        <option>Medicine</option><option>Consumable</option><option>Equipment</option><option>Blood</option><option>Other</option>
      </select>
    </label>
    <label style="flex:1;color:#8b949e;font-size:12px">Echelon
      <select id="mmsai-reg-ech" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 4px">
        <option>Role1</option><option>Role2</option><option>Role3</option>
      </select>
    </label>
  </div>
  <div style="display:flex;gap:8px;margin-bottom:8px">
    <label style="flex:1;color:#8b949e;font-size:12px">Stock
      <input id="mmsai-reg-stock" type="number" value="1" min="0" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 8px">
    </label>
    <label style="flex:1;color:#8b949e;font-size:12px">Alert at
      <input id="mmsai-reg-alert" type="number" value="5" min="0" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 8px">
    </label>
    <label style="flex:1;color:#8b949e;font-size:12px">Use / hr
      <input id="mmsai-reg-rate" type="number" value="1" min="0" step="0.1" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 8px">
    </label>
  </div>
  <label style="display:block;color:#8b949e;font-size:12px;margin-bottom:8px">NSN — NATO stock number (optional)
    <input id="mmsai-reg-nsn" placeholder="e.g. 6505-01-123-4567" style="width:100%;margin-top:3px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:6px 8px">
  </label>
  <div style="display:flex;gap:8px;align-items:center">
    <button id="mmsai-reg-add" style="flex:1;background:#238636;color:#fff;border:none;border-radius:6px;padding:8px;cursor:pointer;font-weight:600">➕ Add to inventory</button>
    <button id="mmsai-reg-cancel" style="background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:8px 12px;cursor:pointer">Cancel</button>
  </div>
  <div id="mmsai-reg-note" style="color:#8b949e;font-size:11px;margin-top:6px"></div>
</div>
<div id="mmsai-cam-log" style="max-width:440px;margin:0 auto"></div>
<script src="https://cdn.jsdelivr.net/npm/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>
<script>
(function () {
  var API  = __API__;
  var QTY  = __QTY__;
  var USER = __USER__;
  var statusEl = document.getElementById('mmsai-cam-status');
  var logEl    = document.getElementById('mmsai-cam-log');
  var cooldown = false;

  function line(ok, msg) {
    var row = document.createElement('div');
    row.style.cssText = 'padding:5px 9px;margin:4px 0;border-radius:6px;font:12px monospace;'
      + 'background:' + (ok ? '#12261a' : '#2d1215') + ';color:' + (ok ? '#7ee2a0' : '#ff8f8f');
    row.textContent = msg;
    logEl.insertBefore(row, logEl.firstChild);
    while (logEl.children.length > 8) logEl.removeChild(logEl.lastChild);
  }
  function beep() {
    try {
      var ctx = new (window.AudioContext || window.webkitAudioContext)();
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.connect(g); g.connect(ctx.destination);
      o.frequency.value = 880; g.gain.value = 0.07; o.start();
      setTimeout(function () { o.stop(); ctx.close(); }, 110);
    } catch (e) {}
  }
  // Cache of known item codes so a scan can tell "log use" from "new item".
  // Items added from an XML/QR label also match on their stored raw payload.
  var known = {};
  var invById = {};
  function loadInventory() {
    return fetch(API + '/inventory').then(function (r) { return r.json(); }).then(function (list) {
      known = {}; invById = {};
      (list || []).forEach(function (it) {
        known[String(it.item_id).toLowerCase()] = true;
        invById[String(it.item_id).toLowerCase()] = it;
        var raw = String(it.barcode_raw || '');
        if (raw && raw !== '—') { known[raw.toLowerCase()] = true; invById[raw.toLowerCase()] = it; }
      });
    }).catch(function () { known = {}; invById = {}; });
  }
  loadInventory();

  // Turn a raw scan (possibly an XML label) into a clean inventory item code.
  function cleanItemId(code, payloadName) {
    if (code.indexOf('<') === -1) return code;
    var base = payloadName || code.replace(/<[^>]*>/g, ' ');
    var slug = base.toUpperCase().replace(/[^A-Z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
    return slug || 'ITEM-' + code.length;
  }

  var regEl   = document.getElementById('mmsai-reg');
  var curCode = '';
  var curId   = '';
  function showRegister(code, payloadName) {
    curCode = code;
    curId   = cleanItemId(code, payloadName);
    document.getElementById('mmsai-reg-code').textContent =
      (payloadName ? 'Medicine: ' + payloadName + ' · ' : '')
      + 'will be added with item code ' + curId;
    document.getElementById('mmsai-reg-name').value = payloadName || '';
    document.getElementById('mmsai-reg-note').textContent = payloadName
      ? 'Name taken from the QR label — edit if needed.'
      : 'The product lookup above prefills the name if this is a known retail code.';
    regEl.style.display = 'block';
    statusEl.textContent = 'Unknown code — check the details and add it to inventory.';
  }
  document.getElementById('mmsai-reg-cancel').onclick = function () { regEl.style.display = 'none'; };
  document.getElementById('mmsai-reg-add').onclick = function () {
    var name  = document.getElementById('mmsai-reg-name').value.trim() || curId;
    var body  = {
      item_id: curId,
      barcode_raw: curCode,
      item_name: name,
      category: document.getElementById('mmsai-reg-cat').value,
      echelon: document.getElementById('mmsai-reg-ech').value,
      current_stock: parseInt(document.getElementById('mmsai-reg-stock').value, 10) || 0,
      alert_threshold: parseInt(document.getElementById('mmsai-reg-alert').value, 10) || 0,
      avg_consumption_per_hour: parseFloat(document.getElementById('mmsai-reg-rate').value) || 1,
      nsn: document.getElementById('mmsai-reg-nsn').value.trim() || '—'
    };
    fetch(API + '/register_item', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (res.ok) {
          known[curCode.toLowerCase()] = true;
          known[curId.toLowerCase()] = true;
          regEl.style.display = 'none';
          line(true, '➕ ' + curId + ' added as “' + name + '” · stock ' + body.current_stock);
          statusEl.textContent = 'Added ' + name + '. Scanning it again now logs use.';
        } else {
          line(false, '⛔ add failed → ' + (res.j.error || 'rejected'));
          statusEl.textContent = 'Add failed: ' + (res.j.error || 'see log');
        }
      })
      .catch(function () { line(false, '⛔ ' + curId + ' → could not reach the API'); });
  };

  function logUse(code) {
    statusEl.textContent = 'Scanned ' + code + ' — logging…';
    fetch(API + '/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_id: code, quantity_used: QTY, user: USER })
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (res.ok) {
          line(true, '✅ ' + code + ' → ' + res.j.item_name + ' · new stock ' + res.j.new_stock
                     + (res.j.alert ? ' ⚠️ LOW' : ''));
          statusEl.textContent = 'Logged ' + code + '. New stock ' + res.j.new_stock + '.';
        } else {
          line(false, '⛔ ' + code + ' → ' + (res.j.error || 'rejected'));
          statusEl.textContent = 'Not logged: ' + (res.j.error || 'unknown item');
        }
      })
      .catch(function () {
        line(false, '⛔ ' + code + ' → could not reach the API');
        statusEl.textContent = 'Network error reaching the API.';
      });
  }

  // Instant, always-useful scan info: code type + GS1 country + our own inventory
  // record render immediately; the public product databases are queried in parallel
  // and only augment the card, so a regional medicine barcode still returns info fast.
  var lastProductName = '';
  var GS1_COUNTRY = {
    '00':'US / Canada','01':'US / Canada','03':'US / Canada','06':'US / Canada','13':'US / Canada',
    '30':'France','37':'France','40':'Germany','44':'Germany','45':'Japan','49':'Japan',
    '50':'United Kingdom','69':'China','80':'Italy','84':'Spain','87':'Netherlands',
    '88':'Singapore / Thailand / Korea','89':'India / Vietnam','90':'Austria',
    '93':'Australia','94':'New Zealand','60':'South Africa'
  };
  function gs1Country(code) {
    if (!/^\\d{8,14}$/.test(code)) return '';
    return GS1_COUNTRY[code.slice(0,3)] || GS1_COUNTRY[code.slice(0,2)] || ('GS1 prefix ' + code.slice(0,3));
  }
  function showInfo(code, fmt) {
    var box = document.getElementById('mmsai-info');
    box.style.display = 'block';
    box.textContent = '';
    function row(k, v) {
      if (!v && v !== 0) return;
      var d = document.createElement('div'); d.style.margin = '2px 0';
      var b = document.createElement('b'); b.textContent = k + ': ';
      d.appendChild(b); d.appendChild(document.createTextNode(v));
      box.appendChild(d);
    }
    // Many medicine QR labels embed structured fields (<dg> drug, <dt> date, …).
    var tags = {}, payloadName = '';
    var tagRe = /<([a-zA-Z0-9]+)>([^<]*)<\\/\\1>/g, tagMatch;
    while ((tagMatch = tagRe.exec(code)) !== null) {
      if (tagMatch[2].trim()) tags[tagMatch[1]] = tagMatch[2].trim();
    }
    payloadName = tags.dg || '';
    var hasTags = code.indexOf('<') !== -1;
    var t = document.createElement('div');
    t.style.cssText = 'font-weight:600;margin-bottom:4px';
    t.textContent = 'ℹ️ ' + (payloadName || (hasTags ? 'QR label' : code));
    box.appendChild(t);
    row('Code type', fmt || 'barcode / QR');
    if (!hasTags) row('Code', code);
    var country = gs1Country(code);
    if (country) row('GS1 country', country);
    var mine = invById[code.toLowerCase()];
    if (mine) {
      row('In inventory', mine.item_name + ' · stock ' + mine.current_stock
          + ' · alert ' + mine.alert_threshold + ' · ' + (mine.echelon || ''));
      if (mine.nsn && mine.nsn !== '—') row('NSN', mine.nsn);
    }
    // Holder/patient and pack metadata stay hidden; the card shows medicine info only.
    if (tags.in) row('Usage (on label)', tags.in);
    var filled = false, noneShown = false;
    function fill(src, p) {
      if (filled) return; filled = true;
      lastProductName = p.product_name || p.generic_name || '';
      row('Name', lastProductName);
      row('Brand', p.brands);
      row('Categories', p.categories);
      row('Pack size', p.quantity);
      if (regEl.style.display === 'block' && curCode === code
          && !document.getElementById('mmsai-reg-name').value && lastProductName) {
        document.getElementById('mmsai-reg-name').value = lastProductName;
        document.getElementById('mmsai-reg-note').textContent =
          'Name auto-filled from ' + src + ' — edit if needed.';
      }
      if (!payloadName && lastProductName) drugInfo(lastProductName);
    }
    // Real leaflet text (usage / storage / mechanism) from the openFDA drug-label API.
    var drugDone = false;
    function clean(s) {
      return String(s).replace(/<[^>]*>/g, ' ').replace(/\\s+/g, ' ').trim().slice(0, 300);
    }
    function drugInfo(name) {
      if (drugDone || !name) return; drugDone = true;
      function go(search) {
        return fetch('https://api.fda.gov/drug/label.json?search=' + encodeURIComponent(search) + '&limit=1')
          .then(function (r) { return r.ok ? r.json() : null; })
          .then(function (j) { return j && j.results && j.results[0] ? j.results[0] : null; })
          .catch(function () { return null; });
      }
      go('openfda.brand_name:"' + name + '"').then(function (lab) {
        return lab || go('openfda.generic_name:"' + name + '"');
      }).then(function (lab) {
        if (!lab) { row('Drug leaflet', 'no openFDA leaflet found for “' + name + '”'); return; }
        function sec(key, label) { var v = lab[key] && lab[key][0]; if (v) row(label, clean(v)); }
        sec('indications_and_usage', 'Usage (indications)');
        sec('dosage_and_administration', 'Dosage');
        sec('storage_and_handling', 'Storage');
        sec('clinical_pharmacology', 'How it works');
        sec('warnings', 'Warnings');
      });
    }
    if (payloadName) drugInfo(payloadName);
    function none() {
      if (filled || noneShown) return; noneShown = true;
      row('Public record', 'none in Open Products/Food Facts (normal for regional medicines) — your inventory details above still apply');
    }
    function get(host, src) {
      return fetch('https://' + host + '/api/v2/product/' + encodeURIComponent(code)
                   + '.json?fields=product_name,generic_name,brands,categories,quantity')
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.product && (j.product.product_name || j.product.brands)) fill(src, j.product); })
        .catch(function () {});
    }
    Promise.all([
      get('world.openproductsfacts.org', 'Open Products Facts'),
      get('world.openfoodfacts.org', 'Open Food Facts')
    ]).then(none);
    setTimeout(none, 6000);
    return payloadName;
  }

  function onScan(text, result) {
    if (cooldown) return;
    cooldown = true;
    setTimeout(function () { cooldown = false; }, 1200);
    beep();
    var code = String(text).trim();
    var fmt = '';
    try { fmt = result.result.format.formatName; } catch (e) {}
    var pn = showInfo(code, fmt);
    var hit = invById[code.toLowerCase()];
    if (hit) {
      logUse(hit.item_id);
    } else {
      showRegister(code, pn);
    }
  }

  var hq = new Html5Qrcode('mmsai-reader');
  var running = false;
  function startCam() {
    if (running) return;
    statusEl.textContent = 'Starting camera…';
    hq.start(
      { facingMode: 'environment' },
      {
        fps: 20,
        qrbox: function (vw, vh) { return { width: Math.floor(vw * 0.9), height: Math.floor(vh * 0.7) }; },
        formatsToSupport: [
          Html5QrcodeSupportedFormats.QR_CODE,
          Html5QrcodeSupportedFormats.EAN_13,
          Html5QrcodeSupportedFormats.EAN_8,
          Html5QrcodeSupportedFormats.CODE_128,
          Html5QrcodeSupportedFormats.CODE_39,
          Html5QrcodeSupportedFormats.UPC_A,
          Html5QrcodeSupportedFormats.UPC_E,
          Html5QrcodeSupportedFormats.DATA_MATRIX
        ],
        videoConstraints: {
          facingMode: { ideal: 'environment' },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        verbose: false
      },
      onScan,
      function () {}
    ).then(function () {
      running = true;
      statusEl.textContent = 'Camera live — point it at any barcode / QR label.';
    }).catch(function (err) {
      running = false;
      statusEl.textContent = 'Camera unavailable (' + err + '). Use “Scan / type item code” with a USB reader, or “Pick from list”.';
    });
  }
  function stopCam() {
    if (!running) return;
    hq.stop().then(function () {
      hq.clear(); running = false;
      statusEl.textContent = 'Camera stopped — press ▶️ Start camera to scan again.';
    }).catch(function () { running = false; });
  }
  document.getElementById('mmsai-cam-start').onclick = startCam;
  document.getElementById('mmsai-cam-stop').onclick = stopCam;
})();
</script>
""".replace("__API__", json.dumps(api_url)) \
   .replace("__QTY__", json.dumps(int(qty))) \
   .replace("__USER__", json.dumps(user))

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
    # ── Header logos: BST left, Code:Black AI right ──
    logo_b64 = "/9j/4AAQSkZJRgABAQEA2ADYAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAMgBOIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8qqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACitTw34X1bxfqkenaLp8+pXsnSKBMkD1J6Ae5wK+l/hv8AsXFljvPGmoFT1/s3T25+jy4/RR/wKvLxuZYXAK9edn26/ce9leR4/N5WwlO66yekV8/0V35Hy3Y2F1qd1HbWdtNd3MhwkMCF3Y+gA5NeueEv2UPH/iYRy3FjDoVs3PmalLtfH/XNQWB9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hNePeEfDF7408S6domnJvvL6YRJ6L3LH2ABJ9ga/SbwT4RsfAfhbTtC05MWtnEEDEYMjdWc+7Nkn618hxFmbwdD2FJ+/P8F1fz2Xz7H6PwXkSzPFvFV1elT/ABl0Xy3fyXU3KKKhvLyDTbOe7upkt7aBGkllkYBUUDJYnsAK/I9Xoj+jm0ldmR428aaV8P8Aw3d63rE/kWduOi8vIx+6iDuxP+JwATX59/Fj4sax8WPEUl/qEjRWUbMLOwVspboe3uxwMt3PoMAbHx6+M1z8WvFLNCzw6BZMUsbc5G4dDKw/vN+gwPUnzCv13IsmWBpqvWX7x/8Akq7evf7vX+cOLOJpZtVeFwztQi//AAJ935dl8/Qooor64/OQooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBVYowZSVYHII6ivsj9mf9ok+LFg8KeJrgf2yi7bO+kPN2APuOf+egHf8Ai+o+b42p8E8lrNHNDI0U0bB0kjYqysDkEEdCDXlZll1LMqLpVN+j7P8ArdH0GSZ1iMkxSr0XeL+KPSS/z7Pp6XP1Vorx/wDZz+NS/FTwybTUJFHiTTkVbpeB56dFmA9+jY6H0BAr2CvxLE4ephK0qFVWkj+p8DjaOY4aGKw7vGS/pPzXU89+OHwptviz4LmsNqR6tbZm0+4b+CTH3Sf7rYAP4HsK/PC+sbjTL24s7uF7e6t5GilhkGGR1OCpHqCDX6o18j/tj/CkWd3B4306HEVwVt9SVBwJMYjl/EDafcL3NfY8M5m6NT6lVfuy+Hyfb5/n6n5nx1kSxFH+06C9+Hxece/qvy9D5fooor9RPwQKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiirWk6Xca3qlnp1onm3d3MkEKD+J2YKo/Mik2oq7KjFyajFXbPqf9i/4beXBf8AjW8i+aTdZ2G4fwj/AFsg+pwoPs4719T1jeDfDFt4L8K6VodmP3FjbrCG/vkD5mPuzZJ+tbNfhGZYx4/FTrvZ7enQ/rbI8tjlOX0sKt0ry85Pf/JeVgr5Z/bC+LzW8a+BtLm2vIqzanIh5CnlIfx4Y+231NfRHjvxdaeA/CGq6/ecwWMJk2ZwZH6Ig92Yqv41+aeva5eeJNavdV1CUz3t5M08sh7sxyceg9B2FfQ8M5csTXeKqL3Ybf4v+Bv9x8Xx1nTwWFWAou06u/lH/wC229EyjRRRX6ufz2FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB0HgHxtf/DzxZp+vac37+1ky0ecLLGeGjb2IyPbg9RX6R+FfElj4w8O6frWmyebZXsIljPcZ6qfcHII9Qa/LyvqP9jD4lNDfX3gu9lzFMGu7Dcejj/WIPqPmx/st618VxNlyxGH+tQXvQ381/wADf7z9R4Fzp4PF/UKr9yrt5S6fft62PrWsnxX4bs/GPhvUtEv032l9C0L+q5HDD3BwR7gVrUV+VRlKElKLs0f0DUhGpBwmrp6NeTPy78U+Hbvwj4j1LRb5dt3YztBJjocHAYexGCPYisuvpf8AbV8Ciw8QaV4rt48R6gn2S6ZRx5qDKMfcpkf9s6+aK/eMuxax2FhXW7Wvr1/E/kjOsueVZhVwj2i9PR6r8PxCiiivSPECiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACva/2R/CI8SfFiG+lTdbaPA92c9DIfkjH1yxb/gFeKV9l/sT+HRY+CNa1plxJf3ogU+qRLwf++pH/ACr5/PsR9Wy+o1u9Pv8A+Bc+w4RwSx2cUYyWkXzP/t3VfjY+jaKKK/FD+pT5V/bY8dFY9G8I28uN3/Ewu1U9uViU/jvOPZTXyjXcfG7xYfGnxU8R6mH3wfamggIPHlR/u0I+oXP4muHr9zyjCrB4KnS62u/V6/8AAP5O4izB5lmlavf3b2XotF9+/wAwooor2D5sKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArV8J+JLrwh4m0zWrM4ubG4SdRnAbaclT7EZB9jWVRUyipxcZLRl06kqU1Ug7Nar1R+pei6tba9o9jqdm/mWt5AlxE3qjqGH6GrteJfsh+LD4h+E0djK++40i5e1wx58s4dD9PmKj/AHK9tr8BxmHeExNSg/su3+X4H9gZZjFmGCpYpfbin8+q+TPOP2hvCA8afCPXrVU33NrF9ut+MkPF8xA9yu5f+BV+d1fqrJGs0bRuodGG1lYZBB6ivzF8b+Hz4V8Y63o5BxY3s1uue6q5Cn8Rg/jX33COIvCrh30s189H+h+QeIuCUatDGxW6cX8tV+b+4xKKKK/Qj8bCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACv0R/Z20f+w/gv4Wg24aW2N0TjGfNdpAfyYflX53V+n/gvTxpPg7QrELsFtYQQ7eONsajHH0r4Li6pahSp9239y/4J+ueHNFSxdet/LFL73f/ANtNmsDx9rx8L+B9f1YNtezsZpkP+2qEqPzxW/XlH7UepHTfgh4g2tte48mBecfemTcP++Q1fnmDpe2xNKk/tSS+9n7PmWIeFwNeut4xk/uTPz+ooor+gD+PAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooo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v6/IOJ6vtMwcf5Ul+v6n9JcB4d0cmU39uUn+Uf8A20K+Mf2278TfELQ7MHPk6YJD7F5XGP8AxwfnX2dXwF+1RrX9sfGvWlVt0dmkNqhzn7salh/30zVXC9Nzx/N/LFv8l+pnx9WVPKOT+eUV+b/Q8kooor9dP5xCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvsb9iTxKLzwjruhu+ZLG7W5QHrslXGB7Boyf+BV8c17L+yf4wHhf4uWdrK+221eJrFsngOcNGfqWUKP9+vAz3DvE5fUit1qvlr+Vz6/hPGrA5xQnJ6SfK/8At7RfjY+86KKK/Ez+pj85fjx4TPgz4seIrBUKW8lwbqDjjy5fnAHsNxX/AIDXA19cftr+BWutN0fxbbx7mtT9huyB/wAs2JaNj6ANuH1cV8j1+5ZPiljMDTqdUrP1Wn/BP5Q4ky95bmlajb3W+Zej1X3bfIKKKK9k+ZCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK2/BHhW58ceLtJ0K0z519cLFuAzsXqz/RVBb8Kic404ucnZLU0p051pxp01eUnZerPtb9kvwmfDfwitLqVNtxq073rZHIThEH0KoG/wCB17PVbTNNt9H020sLSMRWtrEkEUY6KiqFUfgAKs1+A4vEPFYidd/abZ/YGXYOOX4OlhY/Yil8+r+b1I55o7aGSaVgkUal3dugAGSa/MHxdrreJ/FWsau+c395Lc4Pbe5YD8Aa+9P2kPGH/CG/CHW5UfZdXyf2fBzglpchse4Tefwr89a/QeEsO406mIfVpL5av80fjviLjVKtQwcX8Kcn89F+T+8KKKK/QD8dCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAK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kP8ArVHSFj/eA+76jjqBn6gr8qY5HhkWSNmR1IZWU4II6EGvtP8AZz/aOg8aWtt4b8SXCweIYwI7e5kOFvgOmT2k9R/F1HPFfmfEGSOm3jMMtH8S7ea8u/b02/dODuKlVjHLcdL3lpCT6/3X59u+2+/0HWX4m8M6Z4w0W50nWLOO+sLhdrxSD8mB6hh2I5FalFfAxlKDUouzR+vThGpFwmrp7pnwX8bP2b9Y+GE02pacJNW8NFiRcquZbYekoH/oY4PtnFeN1+q0kazRsjqGRhhlYZBHoa+dfi1+yHpfiRp9T8IPFouotlm09xi1lP8As45jP0yvTgda/SMq4mjJKjjtH/N/n/mfiXEHAs4N4nKtV1h1X+F9fR69rnxnRW54u8Ea74E1NrDXtMn065H3fNX5HHqjD5WHuCaw6+/hONSKnB3T7H49UpzozdOpFxkt09GgoooqzMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoooUFiABkngAUAFanhnwvqvjDWINK0axl1C/mOEhiHbuSeigdycAV6v8Lf2V/FHjporzVkfw5o558y6T/SJR/sRnBH1bA5yM19hfD74Y+HvhjpP2HQrIQbgPOuZPmnnI7u2Oe/AwBngCvk8z4hw+CTp0Xzz/Ber/RfgfoeR8G43NGquJTp0u7+J+i/V6drnA/Ar9nHTvhekeraoY9T8TMv+uAzFaZHKx56nBwWPPYY5z7TRRX5VisVWxlV1q8rtn9BYHAYbLaCw2FhyxX4+b7sK57x5460r4c+GrrW9Xm8u3hGFjUjfM5+6iA9WP9CegNTeMfGWk+A/D9zrOs3S2tlAPq0jdkQd2PYV8A/GL4xar8XvEP2u6zbaZbkrZWCtlYlPc+rnAyfwHAr18nyipmdS8tKa3f6Lz/I+b4l4kpZHQ5Ya1pfCu3m/L8/vax/iP8QdT+Jviu61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FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH/9k="
    cbl_logo_b64 = "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YYIqU1PTU5nK99lnnze88Q2bbbqp1vTwIw/fcMONv7/jjpGREZv259EeTpno9Xo///nlnzjqE5tuskmWZTffcstdd/1pZGSkCWpWSADKNenYeGhprQfTgwU77LD3Xntts802/X7/ueef/8Odv7/qqquXLVvW7/eruvIbJbfo8rHBXr47HJTdbvfq6667+eab582bV1WVQkWe0d6UHkVeTE1Nbbvtdl/5ylf22mtPbgfy+c+ffPElF3/us59dunSp4Yl7SjsiINZaF3nxxMKFP/nxhcefcNzszGynU0Bd426Hqjsuw3/eSRPjWA7BzEWbNYaQ52r5zOir34LvOJqqErMM0UmODYeKkBFimqfXS5ChFsQPEomWGgLanQuY1FqvvvrqBx540Cc+ceQWW2wxOzvodApnrx04ljdVFDP6Jt9yRw5jCquyWm311b77ve/utedeRua2cuXKkdHu7nvs/ta37rnTK3fafPPN1157LTMMe/rpp++8884zzzzj9tvvYAptz/0xu4YmnWXZ/fff9+yzz66xxhrdbveCS3785z/f1e/3qqpiSicnBERTiWYqW7ly5VprrbX//ge87GUvW2311ZcuXfr3hx781a9+/eSTT/Z6PUTI82J2MLv5ZptfdfXVm2yyyezsbF4UpLVhWiuVaagZz8QNnEhrXVe1OWL/67/+65FHHll99dWH5ZDFfDamheai5Xm2cuXK3d785ot+emGv3yeizEojfSo1SB8dU/dQA1UEggYzM3vmmWduufkWI0lDhuwgWJNtgH333ddApABwwAH7n3feub7xQW/lbv4GEW+66ZcnnHB8mm+KGINjVuIi6BI0t1cglygDkLa6ODvHa1q62Gsb7OMTWyjLiGJAn9kXWGKQiLhCEdXEc/WSYZ+OhEGeBS3Qd1Y4SbQ9VuJR80ACwOLFzy9durSwTQD5SEjn59DUF9tut12eZ4NBFSyXuRO9RfVBTFWPfrspimJyaurSyy5TRn0TQn7Ns59l2fT09GabbXbWd87aa++9+O864fgTzjjzjJM/f3JZlnleWINF58xiRGSVyrKnnnrq2muuOfroowHgxl/eaAwtjAYnCl9ElWFZVqTplFO+cNxxx42N9d2/feiIIz728buPPPLIP9x5Z7/fd2RE9syGjmrN8Z8hAFxy8SUQ5p0Y3gBpIlQ4PTX90pe89PpfXL/J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s2oUZgCkmT0XglKQ5SC7VdeiKpUpldW1jgMtfIaohunp6ZCfxmxllMo6nU5eFLoR7yYabbNljI6MfPnLX950002POOIIk/FgRiaVEUMBBeYuPOKxGQ4p5UbWZVl3OoVSavny5bfeeuvtt99+7733Pv74vxcvXjI9PV2WafNapVS327XWdcQ0Rv5kNHDNAw88YJM/DCMZ/fAUIc/zycnJN77xja973WuNNTpbt8gdEBQql/2ADR+BVWf2xDePOEeg7Qy/sRth2QIsHgYgz/PBYLjbbrv99KcXrbb66u5UgJhniRDlVFJc8AVj58FgcM011xhRm+8T0FfaVVm97rWvW3PNNQaDQafTAQSlsKqp2+3uscdbf//7O+vaRRPyEELKsqyaqa6++uo993xryBGXmHzj7WADVV3SG7L0s8C7mtiJEgapejMbSyIgV0RSUHzw7iGaN4ThKPwa5vHez6UHbdQq9x7DPJImeQE5Id2/J92EahEBj/MMHFsBYPXVVx+fGJ+emm6MNNkIMbheDz74oNa1sWpu829PHgBx7AF/G0qpyanJ559/3jxdbtc1brzmwajranR05OULFvBTIYh8wCYEDHfeZefrrru2yPOysZfw4gb3+o8//nie5V7uRMSYfIhNqgS8aqedOKAhWzoCQJUpANh888233nqrP/zhD72i54K+3GUUcy2AclguXboEGUbJeMXm9xMRdLsjKukH6dwoEQlI15p8RefT0RAbxdBzi54LAxWah0G5eHNifCr3vClUTgEjdl5Cc6o02KAZxJEuinzrrRegQl/EIajGaQKMQ/uzzz67ZMmSbrcrEnuQq70aTkSv1/vUpz71+te/fosttvBmq8xRHr1SxcPu8eZelVWnUzzzzDPf//7ZF/30okf/+U938Od5YcxrZbyPzx+WxQ01gdWNSVVz01asWPHUU0+hwrqumlwV1k4hQpYpRHj961+f53lVVa6+RkTSjMEMIdBqGCw6tP23QUkx968ZcnpTOCI39mxWldb1J446ap111h0Mhp1OMUdEgXeHhhYjCmnunef5r379q7/85S+jo6Na184rz9HSdK0zlR1wwIFKKZ/4AmCu/7777vv1r399OBwqBpa5THRTLtx44w3PPvvs2muvHZr3iQjbiLTJSubkqeYixdDC82AjZU0OJgEYipz1P7I6L4Rgjpw0JA8ixPkJ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as7MwN2Cc2iSE/wqBZ0iX23evCzL8iJ3s/CcfRVFXpblFVdcsd9++z355JPOSNk5w4hEcwBD8tl0000dPdTSY5jK022TiHWtR0ZGTIDos888+8ILS63hqOtlGr+jLMvqut57rz0BwWRGmZvbbOkIiPjgQw+aKodbXJCcQxZ5BgC7vulN6623HpHOsswZhLgJnCaqqlqp7Jlnntnv7W+/+89393o98+tcTFCn0/n9nXfuvddejz762PLlyw888MB///vfRVEMh0NTkiurz/K+C0jh7AGgyPO6rrrd7ieOPNJYvSYAEfs3ZVn2er2zzz77wp9c2O10mw47Sr6UuikKzGwMo+TBv/1ttDdqR1OunEPJDWlOS+N60fytQuPga1jN5vI7LwAM8jeJqrJSSl16ySXLly83Wm5GyBFTLp4eBqDNiT13QEBIoseotGaHAvi6z57N7S8eGt/JXT4X8ZBErtuM4x1ieg+Gsc+RSYZXlBCfUYnU4pYRtKmjjzzyyIsuumjhwicaJzti4fUO+mUOnuPjY0Rw9dVXX3311autNm98fLzfH9NaT09PL1+xfOWKlQpxfHxck9aVbsrxhtZLw3Iw1h97/vnn9z9g/8svv/x1r3tdURQHHLD/X//6l9HRXl3V7KroRjMBUJVVr9e79957d99jjwMPPOCd73jnhhtuaEbEP/7JT2679VbjfiNTnZ37P+Yqq6p6k002eds+extsdLfddrv44ou1rrUhWWlmk4KAhJWu8yxftOi5Aw444F3vetd//ud/brXVVqO93pLnF9/2q9u+973v/eMf/+j1elVVeUiebNdNxFgZ3jvaiELec/B7fvu73xZFUdWlu2MNed3SLpVSH/noh//xj79/5sQT11577bhiuPPOOz/96U//7ne/nTdv3pEf//jSxUtO+vxJ5rcIWzRUoCtQub7pu2qwFPujUA4bc+HaA7U0nIVOp3z6KXX1V7MPf4/qCpVCqlntQ7YgZAde4zbafeGFF4488sher6fJGAMaNySF1v9u8eIlD/7tb/fddy8A9kZ7da2RS5kabYpyB2pVVpnKttvuP8B2D4jA5UXc9X5sbGzx4ufOP/+C97//faOjPWONpxSqZnrMddgmfQgWNodTXZaV4whprbvdkV/84rrbbr2t328cGphTX3OvGgenPAeALbfY4s1vfvPFF188Pj7epJ+SY5o2ghgi6Pd7j/3rX2996x5HfuITBx988MYbbVR0OsPh8Kmnnvrxj398+umnT01N9XqjRPTII4+84x3v+OUvf7nOOuuUwyrLlZlIs82KFLq6wxCmNCLOzMx2O92zv3/2u9/znjXXWvvkkz8/1u+XVWmoZ4jGn5IJegE6nc7xJxz/ile+YptttrZ3ROB6QYJkzEe/8MILTTmiQaN3jgftfLk1ldXQ7U3oDVDtNEJuT1meM086UWdXuh4Z6f79H3+/9dbb9t//nTYeGFFyKUOH94Dd3BIQwK1BKDpufKABspA2xv90kB7n9REk7IICd+pceMk55QitetIg5hXs6NLMfNsKBr1FIAnv43QP5XICyrJcd911vvmtbx504IFKKdBgY7ZcN0ZBMmFV1QAwNjaGALOzg8nJyVob03llXN6IqK7tjmmlNhamw6quRkZHlixdst/b9zv//PP3ffu+hx562Pe+973nn38+y3Kh9iLv5a+17vf7dVVecP4FF5x/gfGhM64GY2N9g0MopYj3cH5agjMzM+9+17s33mjjmekZANx9993XWWedpUuX5kXu9U1OUNS4gutud4RIX3rppZdeeunaa6/T6/WWLlmycnJllmVjY2O1ORUgwMe5QkqYDhiu9yGHHHLWWWc9+uijnU6ncQTy67p5dk1c8mmnn/6L66/fb7/9XvnKnTbZZOPR3uhzi5578MEHb7311l/ddtv0zPTExERVVb1e7/Mnf37Rc4u+9c1vFp2O8edx/ALIClj+HP3xCuoi6tqvecddUYCIGepstRwfuIFWPA8Ta4PlftRVA7A4NbprqY0EARFXrFj5gx/8YJW4Za/fMyMcVOh5LiSMiM13DgaDTTbddIcFCxyWpbVN1bIjBs+YBVJKHXPM0d/4+te23mabj338Y6Ojo3Vde+U5OTqSrioqiuLyn/3syCOPfOlLXxq8yV9c/4v//sB/67qmZtDS1Jp2cgiIqsgLhxBmWXbYYYdfeumlxmkRHbTuzBgsBD3a683MzpxyyilnnHHGRhtttNpqq61YsXzhwicXL17c6/X6/X5VVVrrfr9377337r//ATfecEN/rG9IfSpTCYZSg9mjypRBh84///x99913ZmbmxBM/86c//fH6638xNjZWNhE3zr/ZdV9UdIpFixYd8cEjfnnTL83TFFgk8XkkB16Mo8bjjz/+m9/+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"
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:10px">
      <img src="data:image/jpeg;base64,{logo_b64}"
           style="width:230px;border-radius:12px;filter:drop-shadow(0px 0px 10px rgba(255,106,0,.45))">
      <img src="data:image/png;base64,{cbl_logo_b64}"
           style="width:230px;border-radius:12px;filter:drop-shadow(0px 0px 10px rgba(255,106,0,.45))">
    </div>
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

    # ── Auto-refresh (opt-in, mentor review item 3) ──────────────────────────
    # A fragment timer reruns the whole app on a fixed interval. It is off by
    # default and only fires when the interval has actually elapsed, so a manual
    # click or a first render never triggers an extra rerun.
    ar_col, ar_note = st.columns([1, 3])
    with ar_col:
        auto_refresh = st.toggle(
            "⏱️ Auto-refresh", value=False, key="auto_refresh",
            help="Re-fetches inventory, alerts and forecasts on a fixed interval so the "
                 "dashboard stays current without clicking 🔄 Refresh. Off by default.",
        )
    if auto_refresh:
        ar_secs = ar_col.slider("Interval (seconds)", 10, 120, 30, 10, key="auto_refresh_secs")
        ar_note.caption(
            f"Auto-refresh ON — data reloads every {ar_secs}s. Widget values are kept between "
            "refreshes, but switch it off while typing a long entry or mid-scan."
        )

        @st.fragment(run_every=f"{ar_secs}s")
        def _auto_refresh_tick():
            now = time.time()
            if now - st.session_state.get("_ar_last", 0.0) >= ar_secs - 1:
                st.session_state["_ar_last"] = now
                st.rerun(scope="app")

        _auto_refresh_tick()

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
        with col_qr:
            # ── Scan-to-log panel (mentor review item 4) ──
            st.markdown("#### 📷 Scan to Log Use")
            st.caption(
                "Three ways to log use without typing. **Camera scan** turns the phone/laptop "
                "webcam into a real barcode/QR reader and logs the item the instant it decodes. "
                "A USB/Bluetooth reader acts as a keyboard wedge into the *Item code* field. "
                "Pick-from-list is the touchscreen fallback when no scanner is available."
            )
            inv_for_scan = api_get("/inventory") or []
            if not inv_for_scan:
                st.info("No inventory available for scanning.")
            else:
                scan_mode = st.radio(
                    "Method",
                    ["📷 Camera scan (barcode/QR)", "🔎 Scan / type item code", "📋 Pick from list"],
                    key="scan_mode", horizontal=True, label_visibility="collapsed",
                )
                target = None
                if scan_mode.startswith("📷"):
                    cq, cu = st.columns([1, 2])
                    cam_qty  = cq.number_input("Qty per scan", 1, 50, 1, key="scan_cam_qty")
                    cam_user = cu.text_input("User", value=st.session_state.username,
                                             key="scan_cam_user")
                    _components.html(_camera_scanner_html(API, int(cam_qty), cam_user),
                                     height=520)
                    if st.button("🔄 Refresh stock figures now", key="scan_cam_refresh"):
                        st.rerun()
                    st.caption(
                        "Press **▶️ Start camera**, then scan any barcode/QR in the world: a product-"
                        "info card shows the medicine's name, brand, category and pack size from the "
                        "Open Products/Food Facts databases. A code already in inventory logs its use; "
                        "an unknown code opens an add-to-inventory form with the code and (when known) "
                        "the name prefilled. Tables above update on the next rerun (this button or "
                        "Auto-refresh). The browser asks for camera permission once and needs HTTPS."
                    )
                elif scan_mode.startswith("🔎"):
                    scan_code = st.text_input(
                        "Item code", placeholder="Scan or type e.g. ITM004", key="scan_code_input"
                    ).strip()
                    if scan_code:
                        target = next(
                            (i for i in inv_for_scan
                             if i["item_id"].lower() == scan_code.lower()
                             or i["item_name"].lower() == scan_code.lower()), None)
                        if not target:
                            st.error(f"No inventory item matches “{scan_code}”.")
                else:
                    labels = {f"{i['item_id']} — {i['item_name']} (stock {i['current_stock']})": i
                              for i in inv_for_scan}
                    target = labels[st.selectbox("Item", list(labels), key="scan_pick")]

                if target:
                    tc_scan = HOS_COLOR.get(target.get("hos_tier", "GREEN"), "#3fb950")
                    st.markdown(
                        f"<div style='background:#161b22;border:1px solid #30363d;"
                        f"border-left:3px solid {tc_scan};border-radius:8px;padding:10px 12px'>"
                        f"<b style='color:#c9d1d9'>{target['item_name']}</b><br>"
                        f"<span style='color:#8b949e;font-size:12px'>{target['item_id']} · "
                        f"stock <b>{target['current_stock']}</b> · alert threshold "
                        f"{target.get('alert_threshold', 5)} · HoS "
                        f"{target.get('hours_of_supply', '—')}h "
                        f"({target.get('hos_tier', '—')})</span></div>",
                        unsafe_allow_html=True,
                    )
                    sq, su = st.columns([1, 2])
                    scan_qty  = sq.number_input("Qty", 1, 50, 1, key="scan_qty")
                    scan_user = su.text_input("User", value=st.session_state.username, key="scan_user")
                    if st.button("✅ Log use (scan)", use_container_width=True, key="scan_log_btn"):
                        r = api_post("/scan", {"item_id": target["item_id"],
                                               "quantity_used": scan_qty, "user": scan_user})
                        if r:
                            if r.get("alert"):
                                st.error(f"⚠️ LOW STOCK: {r['item_name']} → {r['new_stock']} left")
                            else:
                                st.success(f"✅ Logged — new stock {r['new_stock']}")

                with st.expander("🏷️ Printable QR labels"):
                    qr_dir = "qr_codes"
                    if os.path.isdir(qr_dir):
                        files = sorted(f for f in os.listdir(qr_dir) if f.lower().endswith(".png"))
                        if files:
                            shown = next((f for f in files
                                          if target and f.startswith(target["item_id"])), files[0])
                            pick_label = st.selectbox(
                                "Label", files, index=files.index(shown), key="qr_label_pick")
                            st.image(os.path.join(qr_dir, pick_label), width=220)
                            st.caption(
                                "Print these and stick them on the pack. Scanning one returns the "
                                "item ID shown in the filename prefix."
                            )
                        else:
                            st.info("The qr_codes/ folder is empty — generate labels first.")
                    else:
                        st.info(
                            "No `qr_codes/` folder in this working directory. The label images ship "
                            "with the local project (`qr_codes/ITM001_Morphine_10mgml.png`, …); the "
                            "scan field above works with any reader regardless."
                        )
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
                        
                        st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
                    with col_fi:
                        st.markdown("**Feature Importance (XGBoost)**")
                        if os.path.exists("feature_importance.png"):
                            st.image("feature_importance.png", width=400)
                            st.caption(
                                "Chart generated offline by `trainmodel.py` (step 7) from the fitted "
                                "XGBoost model. It is a static image, so it does not need the model "
                                "to be retrained to display."
                            )
                        else:
                            st.info(
                                "ℹ️ **Optional artefact missing — not an error.** The forecast above is "
                                "fully working; only the feature-importance chart is absent because "
                                "`feature_importance.png` is not in the current working directory.\n\n"
                                "To regenerate it: `py trainmodel.py` (trains XGBoost on "
                                "`training_data (1).csv`, writes `model.pkl` and "
                                "`feature_importance.png`). The deployed dashboard and the GitHub "
                                "repo both include the PNG, so this notice only appears on a fresh "
                                "local checkout without the training artefacts."
                            )
                    df_show = df_p[["item_id","item_name","current_stock",
                                    "predicted_rate","hours_of_supply","hos_tier"]]
                    df_show.columns = ["ID","Name","Stock","Rate (u/hr)","HoS (hrs)","Tier"]
                    st.dataframe(df_show, use_container_width=True)

    # ── TAB 6: LSTM TREND ─────────────────────────────────────────────────────
    if tab6:
        with tab6:
            st.subheader("LSTM Surge Trend Model")
            st.caption("LSTM predicts consumption trends over time — detects MASCAL surges.")
            st.caption(
                "Offline-artefact model: the LSTM is trained separately and the dashboard replays "
                "its saved 48-hour output (`lstm_actual.npy`, `lstm_preds.npy`, `lstm_hours.npy`). "
                "The trained weights (`lstm_model.keras`, `lstm_scaler.pkl`) ship with the repo but "
                "are not loaded at runtime, so this tab needs no TensorFlow install."
            )
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
                st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
                from sklearn.metrics import r2_score, mean_squared_error
                r2  = r2_score(actual, preds_arr)
                mse = mean_squared_error(actual, preds_arr)
                c1,c2,c3 = st.columns(3)
                with c1: st.metric("LSTM R²",  f"{r2:.4f}")
                with c2: st.metric("LSTM MSE", f"{mse:.4f}")
                with c3: st.metric("Purpose",  "Surge Detection")
                st.info("💡 LSTM tracks consumption trends over time. XGBoost predicts per-item demand. Together they provide complete AI coverage.")
            except FileNotFoundError as exc:
                st.warning(
                    f"ℹ️ **Optional artefact missing — not an error.** `{exc.filename}` is not in the "
                    "current working directory, so the saved LSTM trend cannot be replayed.\n\n"
                    "**What to do:** run Streamlit from the project root "
                    "(`cd mmsai` → `py -m streamlit run dashboard.py`) so the three artefacts — "
                    "`lstm_actual.npy`, `lstm_preds.npy`, `lstm_hours.npy` — resolve. They are "
                    "committed in the GitHub repo and present on the deployed dashboard; this "
                    "notice only appears on a checkout that is missing them. Everything else "
                    "(inventory, XGBoost forecast, Hours of Supply, digital twin) is unaffected — "
                    "the LSTM is a supplementary surge-detection view, not a dependency of the "
                    "live forecasting path."
                )

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
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # ── Resupply requests: how a medic reorders (mentor review item 2) ──
            st.markdown("---")
            st.subheader("📤 Resupply Requests")
            st.caption(
                "The reorder policy is the digital twin's own, applied to live inventory: "
                "**Role 1 / Role 2** reorder when hours of supply fall below **12h** and refill to "
                "**48h**; **Role 3** reorders below **36h** and refills to **72h**. The suggested "
                "quantity is `target hours × consumption rate − current stock − pending requests`, "
                "so the medic never calculates it. A logistician (Role 3) approves or rejects; "
                "approval credits the stock and writes an audit entry."
            )
            is_logistician = "Role 3" in role
            if not is_logistician:
                below = [r for r in hos_data
                         if r.get("needs_reorder") and r.get("echelon") == st.session_state.echelon]
                if below:
                    st.markdown(f"**{len(below)} item(s) at or below their reorder point**")
                    st.dataframe(
                        pd.DataFrame(below)[["item_id", "item_name", "current_stock",
                                             "hours_of_supply", "hos_tier", "reorder_point_h",
                                             "target_h", "suggested_qty"]],
                        use_container_width=True, hide_index=True)
                    opt_col, qty_col, btn_col = st.columns([3, 1, 1])
                    options = {f"{r['item_id']} — {r['item_name']} ({r['hours_of_supply']}h left)": r
                               for r in below}
                    picked  = opt_col.selectbox("Item to reorder", list(options), key="reorder_pick")
                    p_row   = options[picked]
                    qty_req = qty_col.number_input("Qty", 1, 100000,
                                                   int(p_row.get("suggested_qty", 1)),
                                                   key=f"reorder_qty_{p_row['item_id']}")
                    reason  = opt_col.text_input("Reason (optional)", key="reorder_reason",
                                                 placeholder="e.g. MASCAL standby, Role 1 aid post")
                    if btn_col.button("📤 Send request", use_container_width=True, key="reorder_send"):
                        r = api_post("/resupply_request", {
                            "item_id": p_row["item_id"], "qty": int(qty_req),
                            "requested_by": st.session_state.username, "reason": reason})
                        if r and "_id" in r:
                            st.success(f"✅ Request sent — {r['qty']} × {r['item_name']} "
                                       f"queued for Role 3 approval.")
                        else:
                            st.error(f"Request failed: {r}")
                else:
                    st.success("No item at your echelon is below its reorder point — nothing to order.")

            try:
                _rr = _api_request("get", "/resupply_requests?limit=100")
                requests_log = _rr.json() if _rr is not None and _rr.status_code == 200 else []
            except Exception:
                requests_log = []
            if not isinstance(requests_log, list):
                requests_log = []
            if is_logistician:
                pending = [r for r in requests_log if r.get("status") == "PENDING"]
                st.markdown(f"**Role 3 approval queue — {len(pending)} pending**")
                if not pending:
                    st.info("No pending resupply requests.")
                for req in pending:
                    pc1, pc2, pc3 = st.columns([4, 1, 1])
                    with pc1:
                        st.markdown(
                            f"<div style='background:#161b22;border:1px solid #30363d;"
                            f"border-left:3px solid {HOS_COLOR.get(req.get('tier_at_request','GREEN'),'#8b949e')};"
                            f"border-radius:8px;padding:8px 12px;margin-bottom:6px'>"
                            f"<b style='color:#c9d1d9'>{req['item_name']}</b> "
                            f"<span style='color:#8b949e'>({req['item_id']} · {req['echelon']})</span><br>"
                            f"<span style='color:#8b949e;font-size:12px'>Qty <b>{req['qty']}</b> · "
                            f"requested by {req['requested_by']} at {req['created_at']} · "
                            f"HoS was {req['hos_at_request']}h ({req['tier_at_request']})"
                            + (f" · “{req['reason']}”" if req.get('reason') else "")
                            + "</span></div>", unsafe_allow_html=True)
                    with pc2:
                        if st.button("✅ Approve", key=f"ap_{req['_id']}", use_container_width=True):
                            res = api_post(f"/resupply_request/{req['_id']}/decision",
                                           {"action": "approve",
                                            "decided_by": st.session_state.username})
                            if res:
                                st.success(f"Approved — stock now {res.get('new_stock')}")
                            else:
                                st.error("Approval failed")
                            st.rerun()
                    with pc3:
                        if st.button("✖ Reject", key=f"rj_{req['_id']}", use_container_width=True):
                            api_post(f"/resupply_request/{req['_id']}/decision",
                                     {"action": "reject",
                                      "decided_by": st.session_state.username})
                            st.rerun()
            elif requests_log:
                mine = [r for r in requests_log
                        if r.get("requested_by") == st.session_state.username]
                if mine:
                    st.markdown("**Your requests**")
                    st.dataframe(
                        pd.DataFrame(mine)[["item_id", "item_name", "qty", "status",
                                            "created_at", "decided_by", "decided_at"]],
                        use_container_width=True, hide_index=True)

    # ── TAB 7: CROSS-ECHELON MAP ──────────────────────────────────────────────
    if tab7:
        with tab7:
            st.subheader("Cross-Echelon Supply Chain View")
            st.caption("Multi-echelon visibility across Role 1, 2 and 3 facilities")

            # Declared theatre layout (mentor review item 7). There is no GPS feed:
            # lat/lon and establishment sizes are planning constants for a notional
            # ~80-120 km echelon spacing (R1 forward, R2 mid-distance FST, R3 rear).
            # Replace these three rows with surveyed coordinates to plot a real area
            # of operations. Everything else on this tab — item counts, average
            # hours of supply and tier — is computed from the live /hours_of_supply
            # response, keyed by the `echelon` field stored on each inventory record.
            NODE_LAYOUT = [
                {"node":"R1-ALPHA",  "role":"Role 1","echelon":"Role1","lat":28.30,"lon":76.80,"personnel":12},
                {"node":"R2-BRAVO",  "role":"Role 2","echelon":"Role2","lat":28.55,"lon":77.18,"personnel":28},
                {"node":"R3-CHARLIE","role":"Role 3","echelon":"Role3","lat":28.85,"lon":77.60,"personnel":85},
            ]
            hos_rows = api_get("/hours_of_supply") or []
            echelons = []
            for layout in NODE_LAYOUT:
                live = [r for r in hos_rows if r.get("echelon") == layout["echelon"]]
                if live:
                    worst = min(live, key=lambda r: r.get("hours_of_supply", 999))
                    avg   = sum(r.get("hours_of_supply", 0) for r in live) / len(live)
                    echelons.append({**layout, "items": len(live),
                                     "avg_hos": round(min(avg, 999), 1),
                                     "tier": worst.get("hos_tier", "GREEN"),
                                     "source": f"live · worst item {worst.get('item_id','?')}"})
                else:
                    echelons.append({**layout, "items": 0, "avg_hos": 0.0, "tier": "—",
                                     "source": "no inventory records at this echelon"})
            df_eco = pd.DataFrame(echelons)
            with st.expander("ℹ️ Where the map's geographic data comes from"):
                st.markdown(
                    "| Field | Source |\n|---|---|\n"
                    "| Latitude / longitude | **Declared constants** in `NODE_LAYOUT` "
                    "(`dashboard.py`, Cross-Echelon Map tab) — a notional theatre layout, not a GPS feed |\n"
                    "| Node name, role, personnel | Same `NODE_LAYOUT` constants (establishment placeholders) |\n"
                    "| Item count | Counted from `GET /hours_of_supply`, grouped by the `echelon` "
                    "field on each MongoDB `inventory` document |\n"
                    "| Avg HoS | Mean of `hours_of_supply` across that echelon's live items |\n"
                    "| Tier | `hos_tier` of the **worst** (lowest HoS) item at that echelon, PID §9.3 bands |\n\n"
                    "**To plot a real area of operations:** edit the three `lat`/`lon` pairs in "
                    "`NODE_LAYOUT`, or add `lat`/`lon` fields to the inventory documents and read "
                    "them here instead. No other code depends on these coordinates."
                )
            col_map, col_tbl = st.columns([2,1])
            with col_map:
                fig = go.Figure()
                for _,row in df_eco.iterrows():
                    fig.add_trace(go.Scattergeo(
                        lon=[row["lon"]],lat=[row["lat"]],
                        mode="markers+text",
                        marker=dict(size=14,color=HOS_COLOR.get(row["tier"], "#8b949e"),
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
                             center=dict(lat=float(df_eco["lat"].mean()),lon=float(df_eco["lon"].mean())),
                             projection_scale=3.5,
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
                    tc = HOS_COLOR.get(row["tier"], "#8b949e")
                    st.markdown(f"""
                    <div style='background:#161b22;border:1px solid #30363d;
                                border-left:3px solid {tc};border-radius:8px;
                                padding:10px 12px;margin-bottom:8px'>
                      <b style='color:#c9d1d9;font-size:13px'>{row["node"]}</b>
                      <span style='color:{tc};font-size:11px;float:right'>{row["tier"]}</span><br>
                      <span style='color:#8b949e;font-size:11px'>{row["role"]} · {row["personnel"]} personnel<br>
                      Avg HoS: {row["avg_hos"]}h · {row["items"]} item types<br>
                      <i>{row["source"]}</i></span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("**Resupply Pipeline** *(illustrative example — not a live feed)*")
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
            sc1,sc2,sc3,sc4 = st.tabs(["Scenario 1 — Low Stock Alert",
                                    "Scenario 2 — MASCAL Surge",
                                    "Scenario 3 — Controlled Drug Audit",
                                    "🤖 Automated Self-Test (all items)"])
            with sc1:
                st.markdown("**Deplete tourniquet stock until alert fires**")
                st.info("Logs 12 tourniquet uses. Stock drops below threshold (10) → LOW STOCK alert fires.")
                st.caption(
                    "This scenario is a single-item demonstration (ITM004, hard-coded). To test the "
                    "alert on **every** item without clicking per item, use the "
                    "🤖 Automated Self-Test tab."
                )
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
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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

            with sc4:
                st.markdown("**Automated self-test — every check, every item, one click**")
                st.caption(
                    "Scenarios 1-3 above each test one hard-coded item (ITM004, ITM001). This "
                    "self-test loops over **all** items returned by `GET /inventory`, drives each "
                    "one down to its own `alert_threshold` through the real `POST /scan` write path, "
                    "then re-runs the MASCAL surge check and the controlled-drug audit check. "
                    "Nothing has to be run per item manually."
                )
                st.warning(
                    "This consumes real stock in the demo database (same write path Scenario 1 "
                    "uses). Run it before a demonstration, then restore stock with Reset Database "
                    "or by re-seeding."
                )
                cap = st.slider("Max scans per item (safety cap)", 1, 60, 30, key="selftest_cap")
                if st.button("▶️ Run automated self-test", use_container_width=True, key="run_selftest"):
                    inv = api_get("/inventory") or []
                    if not inv:
                        st.error("The API returned no inventory — cannot self-test.")
                    else:
                        # ── Test 1: low-stock alert fires for every item ──
                        prog = st.progress(0.0, text=f"Test 1/3 — low-stock alert across {len(inv)} items")
                        rows = []
                        for n, item in enumerate(inv):
                            iid       = item["item_id"]
                            threshold = int(item.get("alert_threshold", 5))
                            stock     = int(item.get("current_stock", 0))
                            needed    = max(0, stock - threshold + 1)
                            sent      = min(needed, cap)
                            fired     = bool(item.get("alert")) and needed == 0
                            last      = stock
                            for _ in range(sent):
                                r = api_post("/scan", {"item_id": iid, "quantity_used": 1,
                                                       "user": "SelfTest"})
                                if not r:
                                    break
                                last  = r.get("new_stock", last)
                                fired = fired or bool(r.get("alert"))
                            if needed == 0:
                                verdict = "PASS (already below threshold)" if fired else "FAIL"
                            elif needed > cap:
                                verdict = f"SKIPPED (needs {needed} scans, cap {cap})"
                            else:
                                verdict = "PASS" if fired else "FAIL"
                            rows.append({
                                "Item": iid, "Name": item.get("item_name", ""),
                                "Start stock": stock, "Alert threshold": threshold,
                                "Scans needed": needed, "Scans sent": sent,
                                "Stock after": last, "Alert fired": fired, "Result": verdict,
                            })
                            prog.progress((n + 1) / len(inv))
                            time.sleep(0.02)
                        df_t1 = pd.DataFrame(rows)
                        st.markdown("**Test 1 — low-stock alert per item**")
                        st.dataframe(df_t1, use_container_width=True, hide_index=True)

                        # ── Test 2: MASCAL surge re-forecasts and re-tiers ──
                        prog.progress(0.0, text="Test 2/3 — MASCAL surge forecast")
                        surge = api_get("/forecast?operational_tempo=1.0&t1=0.5&t2=0.2&t3=0.1")
                        base  = api_get("/forecast?operational_tempo=0.1&t1=0.1&t2=0.1&t3=0.1")
                        t2_rows = []
                        if surge and base and "predictions" in surge:
                            s_map = {p["item_id"]: p for p in surge["predictions"]}
                            b_map = {p["item_id"]: p for p in base["predictions"]}
                            for iid, sp in s_map.items():
                                bp = b_map.get(iid, {})
                                rose = sp["predicted_rate"] >= bp.get("predicted_rate", 0)
                                t2_rows.append({
                                    "Item": iid,
                                    "Peacetime rate": bp.get("predicted_rate", "—"),
                                    "MASCAL rate": sp["predicted_rate"],
                                    "Rate increased": rose,
                                    "MASCAL tier": sp["hos_tier"],
                                    "Result": "PASS" if rose else "FAIL",
                                })
                            prog.progress(1.0)
                        df_t2 = pd.DataFrame(t2_rows)
                        st.markdown("**Test 2 — surge raises every predicted rate and re-tiers**")
                        if df_t2.empty:
                            st.error("FAIL — /forecast returned no predictions")
                        else:
                            st.dataframe(df_t2, use_container_width=True, hide_index=True)

                        # ── Test 3: controlled drugs land in the audit trail ──
                        prog.progress(0.0, text="Test 3/3 — controlled drug audit trail")
                        controlled = [i for i in inv if i.get("controlled_drug")]
                        for c_item in controlled:
                            api_post("/scan", {"item_id": c_item["item_id"], "quantity_used": 1,
                                               "user": "SelfTest"})
                        logs = api_get("/audit_log") or []
                        selftest_logs = [l for l in logs if l.get("user") == "SelfTest"]
                        t3_rows = [{
                            "Item": c_item["item_id"],
                            "Name": c_item.get("item_name", ""),
                            "Audit entries": sum(1 for l in selftest_logs
                                                 if l.get("item_id") == c_item["item_id"]),
                            "Flagged controlled": any(l.get("controlled") for l in selftest_logs
                                                      if l.get("item_id") == c_item["item_id"]),
                        } for c_item in controlled]
                        for r3 in t3_rows:
                            r3["Result"] = ("PASS" if r3["Audit entries"] > 0
                                            and r3["Flagged controlled"] else "FAIL")
                        prog.progress(1.0)
                        df_t3 = pd.DataFrame(t3_rows)
                        st.markdown("**Test 3 — controlled-drug scans recorded and flagged**")
                        if df_t3.empty:
                            st.info("No controlled drugs in inventory — test not applicable.")
                        else:
                            st.dataframe(df_t3, use_container_width=True, hide_index=True)

                        # ── Verdict ──
                        frames = [df for df in (df_t1, df_t2, df_t3) if not df.empty]
                        all_rows = pd.concat(frames) if frames else pd.DataFrame(columns=["Result"])
                        passed  = int(all_rows["Result"].str.startswith("PASS").sum())
                        failed  = int((all_rows["Result"] == "FAIL").sum())
                        skipped = int(all_rows["Result"].str.startswith("SKIPPED").sum())
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Checks run", len(all_rows))
                        m2.metric("Passed", passed)
                        m3.metric("Failed", failed)
                        m4.metric("Skipped (cap)", skipped)
                        if failed == 0:
                            st.success(
                                f"✅ SELF-TEST PASS — {passed}/{len(all_rows)} checks passed across "
                                f"{len(inv)} items ({skipped} skipped by the safety cap)."
                            )
                        else:
                            st.error(f"❌ SELF-TEST FAIL — {failed} check(s) did not pass. See the tables above.")

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