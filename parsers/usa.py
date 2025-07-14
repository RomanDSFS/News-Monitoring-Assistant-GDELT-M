
import feedparser

FEEDS = [
    ("ABC",            "https://abcnews.go.com/abcnews/internationalheadlines"),
    ("Al_Jazeera",     "https://www.aljazeera.com/xml/rss/all.xml"),
    ("BBC News",       "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("CNBC",           "https://www.cnbc.com/id/100727362/device/rss/rss.html"),
    ("DER SPIEGEL",    "https://www.spiegel.de/international/index.rss"),
    ("France 24",      "https://www.france24.com/en/rss"),
    ("Globalnews",     "https://globalnews.ca/world/feed/"),
    ("Government_ru",  "http://government.ru/en/all/rss/"),
    ("Independent",    "https://whttps://www.independent.co.uk/news/world/rss"),
    ("Los_A Tms",      "https://www.latimes.com/world-nation/rss2.0.xml#nt=1col-7030col1"),
    ("NBC News",       "https://feeds.nbcnews.com/nbcnews/public/news"),
    ("NDTV",           "https://feeds.feedburner.com/ndtvnews-world-news"),
    ("NewYorkTimes",   "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"),
    ("RT",             "https://www.rt.com/rss/news/"),
    ("Skynews",        "https://feeds.skynews.com/feeds/rss/world.xml"),
    ("SouthChinaMP",   "https://www.scmp.com/rss/91/feed/"),
    ("SputnikNews",    "https://sputnikglobe.com/export/rss2/archive/index.xml"),
    ("TASS",           "https://tass.com/rss/v2.xml"),
    ("TmsOfIndia",     "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"),
    ("TheGuardian",    "https://www.theguardian.com/world/rss"),
    ("TheMoscowTms",   "https://www.themoscowtimes.com/rss/news"),
    ("TheSun",         "https://www.thesun.co.uk/news/worldnews/feed/"),
    ("Time",           "https://feeds.feedburner.com/time/world"),
    ("WashingtonPost", "https://feeds.washingtonpost.com/rss/world"),
    

]

def fetch_articles():
    articles = []
    for source, feed_url in FEEDS:
        print(f"[USA] Reading RSS: {source} ({feed_url})")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
           
            text = (
                entry.get("summary")
                or entry.get("description")
                or entry.get("media_description")
                or entry.get("media:description")
                or entry.get("title")
                or ""
            ).strip()

            article = {
                "title": entry.get("title", '').strip(),
                "text": text,
                "link": entry.get("link", '').strip(),
                "published": entry.get("published", None),
                "source": source,
                "country": "USA"
            }

            
            if not text:
                print(f"[USA] Missing text: {article['link']} (источник: {source})")

            articles.append(article)
    return articles
