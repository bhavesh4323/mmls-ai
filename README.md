# MMLS-AI - deployment bundle (Streamlit Cloud + Render)

Two services deploy from this folder (push it to one GitHub repo):

- **API** (`app.py` + `lsco_twin/`) -> **Render** free web service via `render.yaml`.
  Serves inventory, scans, forecasts and the `/twin/*` digital-twin routes. Needs
  the `MONGO_URI` env var (MongoDB Atlas).
- **Dashboard** (`dashboard.py` + `twin_dashboard.py`) -> **Streamlit Community Cloud**
  (free). Set the API location in Streamlit Cloud **Settings -> Secrets**:
  ```toml
  MMLS_AI_API_URL = "https://YOUR-RENDER-API.onrender.com"
  ```

Prototype on synthetic demonstration data. Outputs are planning estimates, not
validated clinical or operational advice.
