Technopolis Promotions Scraper

A Python scraper that automatically extracts promotional products from the Technopolis website and exports the data to an Excel file.

This project is intended for educational and demonstration purposes, showcasing:

browser automation with Playwright

capturing internal API requests

processing JSON data

exporting structured data with pandas

🚀 Features

Opens the Technopolis promotions page

Automatically accepts cookies and closes modal popups

Uses the website’s internal public API

Extracts promotional products only

Collects key product data:

product code

product name

promotional price

original price (if available)

product URL

Exports results to an .xlsx file

📦 Tech Stack

Python 3.10+

Playwright (sync API)

pandas

Chromium (installed automatically by Playwright)


🛠 Installation

Clone the repository:

git clone https://github.com/your-username/technopolis-promotions-scraper.git
cd technopolis-promotions-scraper


Create a virtual environment (recommended):

python -m venv .venv
source .venv/binactivate   # Linux / macOS
.venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Install Playwright browsers:

playwright install

▶️ Usage

Run the scraper with:

python scraper.py


After successful execution, an Excel file will be generated, for example:

Technopolis_promotions_YYYY-MM-DD.xlsx


⚠️ Disclaimer

This project extracts publicly available information only

No authentication, paywalls, or restricted areas are accessed

Website structure or API changes may break the scraper at any time

📚 Notes

This repository contains only the public demo implementation

More advanced features (full catalog scraping, price history, etc.) are intentionally out of scope

The code is structured for readability and easy extension

📄 License

MIT License
Free to use, modify, and learn from.