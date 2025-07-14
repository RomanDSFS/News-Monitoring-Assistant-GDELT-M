import streamlit as st
import pandas as pd
import psycopg2
from collections import Counter
from config import DB_CONFIG
import string
from nltk.corpus import stopwords
import nltk

st.set_page_config(layout="wide")
nltk.download("stopwords")

@st.cache_data
def load_data():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM articles_en WHERE date IS NOT NULL", conn)
    conn.close()
    return df

def main():
    df = load_data()
    df["date"] = pd.to_datetime(df["date"])
    all_topics = list(df["topic"].unique())
    all_sources = list(df["source"].unique())

    
    with st.sidebar:
        st.header("Filters")
        date_range = st.date_input("Date", [df["date"].min(), df["date"].max()])

        st.write("Source")
        
        selected_sources = []
        for src in all_sources:
            if st.checkbox(src, value=True, key=f"src_{src}"):
                selected_sources.append(src)
        if not selected_sources:
            selected_sources = all_sources


    st.markdown("### 📚 Categories")
    if "selected_topics" not in st.session_state:
        st.session_state.selected_topics = []

    cols = st.columns(len(all_topics) + 1)
    for i, topic in enumerate(all_topics):
        if topic in st.session_state.selected_topics:
            if cols[i].button(f"✅ {topic}", key=f"topic_{topic}"):
                st.session_state.selected_topics.remove(topic)
        else:
            if cols[i].button(topic, key=f"topic_{topic}"):
                st.session_state.selected_topics.append(topic)
    if cols[-1].button("Reset", key="reset_topics"):
        st.session_state.selected_topics = []

    if not st.session_state.selected_topics:
        filtered_topics = all_topics
    else:
        filtered_topics = st.session_state.selected_topics

   
    filtered = df[
        (df["source"].isin(selected_sources)) &
        (df["topic"].isin(filtered_topics)) &
        (df["date"].dt.date >= date_range[0]) &
        (df["date"].dt.date <= date_range[1])
    ]

   
    STOPWORDS = set(stopwords.words("english"))
    all_text = " ".join(filtered["title"].fillna('')) + " " + " ".join(filtered["text"].fillna(''))
    words = [
        word.lower().strip(string.punctuation)
        for word in all_text.split()
        if word.isalpha() and word.lower() not in STOPWORDS and len(word) > 2
    ]
    top_words = Counter(words).most_common(30)
    top_words_df = pd.DataFrame(top_words, columns=["word", "count"])

    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📈 Activity")
        timeline = filtered.groupby("date").size()
        st.line_chart(timeline)
    with col2:
        st.subheader("📊 Frequency")
        st.bar_chart(filtered["topic"].value_counts())
    with col3:
        st.subheader("🔠 Keywords")
        st.dataframe(top_words_df, use_container_width=True)

    
    main_col, search_col = st.columns([2, 1])

    with main_col:
        st.markdown(f"### 📄 {len(filtered)} articles found")
        st.dataframe(filtered[["topic", "date", "title", "text", "link", "country", "source"]], use_container_width=True)

    with search_col:
        st.markdown("### Keyword search")
        query = st.text_input("Enter keyword for search", value="", key="search_box")
        if query.strip():
            query_lower = query.strip().lower()
            
            mask = filtered["title"].str.lower().str.contains(query_lower) | filtered["text"].str.lower().str.contains(query_lower)
            search_results = filtered[mask]
            st.write(f"Found {len(search_results)} articles for: `{query}`")
            st.dataframe(
                search_results[["topic", "date", "title", "text", "link", "country", "source" ]],
                use_container_width=True
            )
        else:
            st.info("Enter a keyword to show articles here.")

if __name__ == "__main__":
    main()
