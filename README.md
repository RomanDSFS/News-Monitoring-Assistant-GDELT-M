# News-Monitoring-Assistant-GDELT-M
A Python-based pipeline for monitoring and analyzing global English-language news from open sources.
It extracts news via RSS feeds, classifies them into topics using NLP with lemmatization, stores them in a PostgreSQL database, and presents the results in an interactive Streamlit dashboard.

While the current configuration targets geopolitics and current affairs, the framework is modular and domain-agnostic — simply add new keywords or feeds to adapt it for other domains like climate, tech, or health.



## Table of Contents

- Key Capabilities
- Folder Layout
- Quick Start
- Configuration
- Running the Pipeline
- Streamlit Dashboard
- Outputs
- Extending
- License

---

## Key Capabilities

| Stage           | Description                                           | Main Libraries                        |
|----------------|-------------------------------------------------------|----------------------------------------|
| 1. Parse        | Fetch articles from multiple English-language feeds  | `feedparser`, `requests`              |
| 2. Classify     | Topic classification using keyword lemmatization     | `nltk`, `re`, `WordNetLemmatizer`     |
| 3. Store        | Articles stored in PostgreSQL with rich metadata     | `psycopg2`, `SQL`                      |
| 4. Visualize    | Streamlit dashboard: filters, charts, search         | `streamlit`, `matplotlib`, `pandas`   |

## Folder Layout
```
.
├── config.py # DB connection config
├── main_en.py # ETL pipeline runner (English)
├── parsers/
│ └── usa.py # RSS fetcher for English feeds
├── nlp/
│ └── topic_classification_en.py # Keyword-based topic classification
├── streamlit/
│ └── dashboard_en.py # Streamlit dashboard (EN version)
├── db/
│ └── database_en.py # DB schema for articles_en
├── requirements.txt
└── README.md

---
```
## Quick Start
```
```bash
# 1. Clone and enter the project
git clone https://github.com/your-username/News-Monitoring-Assistant-GDELT-M.git
cd News-Monitoring-Assistant-GDELT-M

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure PostgreSQL connection in config.py

# 5. Run the ETL pipeline
python main_en.py

# 6. Launch the dashboard
streamlit run streamlit/dashboard_en.py

```
Configuration
```
In config.py, define the PostgreSQL settings:

DB_CONFIG = {
    "dbname": "gdeltmaxi",
    "user": "your_db_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}


Running the Pipeline

The main_en.py script runs a complete ETL cycle:

Fetches articles from 15+ RSS sources

Classifies each article into a topic

Stores clean data into the articles_en table

python main_en.py


Streamlit Dashboard

Launch the dashboard:

streamlit run streamlit/dashboard_en.py

Features:

Filters: Date, source, category (via checkboxes and buttons)

Charts: Articles over time, topic frequency, top keywords

Article viewer: Rich table with title, date, link, source, and topic

Keyword search: Instant filtering by search term in title/text

By default, articles are sourced from:

New York Times

BBC World

NBC News

CNBC
...


Outputs

Output
Articles database
Dashboard visualizations
Logs / Warnings


Extending

To add new topics → update TOPIC_KEYWORDS in topic_classification_en.py

To include more feeds → edit parsers/usa.py and add more RSS URLs

To change database → update credentials in config.py


License

Released under the MIT License — see LICENSE.
