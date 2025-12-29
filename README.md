# Clothing Offers Notifier

Simple Python app to fetch listings from configurable online clothing stores, detect offers and size matches (shirts size XXL, trousers size 40), track price changes, and send email alerts.

Quick start

1. Create a virtualenv and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Edit `config.yaml` with store entries and SMTP credentials.

3. Run:

```powershell
python -m src.main
```

4. Add more stores by providing `base_url`, `listings_path`, and CSS selectors in `config.yaml`.
