
import logging
from parsers import usa
from db.database_en import init_db_en, save_article_en
from nlp.topic_classification_en import classify_topic_en
import nltk
nltk.download('punkt')


logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Database initialization...")
    init_db_en()

    logging.info("Uploading news ...")
    us_articles = usa.fetch_articles()
    for article in us_articles:
        article["language"] = "en" 
        article["topic"] = classify_topic_en(article["text"] + " " + article["title"])
        article["country"] = "USA"
        

        if not article.get("text"):
            print(f"[EN] The text is missed: {article.get('link')}")

    
        save_article_en(article)

    logging.info("EN flow is complete!")

if __name__ == "__main__":
    main()
