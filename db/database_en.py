
import psycopg2
from config import DB_CONFIG
from dateutil import parser

def init_db_en():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles_en (
            id SERIAL PRIMARY KEY,
            title TEXT,
            text TEXT,
            link TEXT UNIQUE,
            published TIMESTAMP,
            source TEXT,
            country TEXT,
            date DATE,
            topic TEXT
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_en_date ON articles_en(date);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_en_topic ON articles_en(topic);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_en_source ON articles_en(source);")
    conn.commit()
    cur.close()
    conn.close()

def save_article_en(article):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    pub_date = None
    try:
        if article.get("published"):
            pub_date = parser.parse(article["published"]).date()
    except Exception as e:
        print(f"[EN] ❌ Ошибка даты: {article.get('published')} | {e}")


    try:
        cur.execute("""
            INSERT INTO articles_en (title, text, link, published, source, country, date, topic)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (
            article["title"], article["text"], article["link"], article["published"],
            article["source"], article["country"], pub_date, article.get("topic", "other")
        ))
    except Exception as e:
        print(f"[EN] ❌ Ошибка вставки: {e}")
        print(f"[EN] 🔗 LINK: {article.get('link')}")
        print(f"[EN] 📄 TITLE: {article.get('title')[:60]}")
    
    conn.commit()
    cur.close()
    conn.close()
