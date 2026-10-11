# CyberShield — Streamlit

This is a Streamlit conversion of the LlamaCoder CyberCrime Reporter App.

## Features
- CyberShield login screen
- Demo authentication: any email + password with at least 6 characters
- Cybercrime incident dashboard
- Total/Critical/Open/Resolved statistics
- New incident report form
- Categories and severity levels
- Report status updates
- Delete reports
- Dark cybersecurity-themed UI

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. In Streamlit Community Cloud, create a new app.
4. Select your GitHub repository.
5. Set the main file to `app.py`.
6. Deploy.

## Important persistence note

The original LlamaCoder app stores reports only in browser memory. This Streamlit conversion keeps reports in Streamlit session state, so reports are available during the active session but are not a permanent database.

For permanent multi-user storage, connect the app to a database such as Supabase/PostgreSQL/SQLite-backed storage appropriate for your deployment.
