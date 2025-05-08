import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import re
from urllib.parse import quote

# Configure Streamlit app
st.set_page_config(page_title="HN Keyword Analyzer", layout="centered")
st.title("🔍 Hacker News Keyword Sentiment")
st.write("Analyze sentiment of comments discussing any keyword")

# User inputs
with st.form("search_form"):
    keyword = st.text_input("Enter keyword to analyze", "AI")
    max_comments = st.slider("Max comments to analyze", 10, 200, 50)
    submitted = st.form_submit_button("Analyze")

def search_hn(keyword):
    """Search HN for posts containing the keyword"""
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={quote(keyword)}&tags=story"
        response = requests.get(url, timeout=10)
        results = response.json().get("hits", [])
        return [f"https://news.ycombinator.com/item?id={hit['objectID']}" for hit in results]
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return []

def scrape_hn_comments(url, max_comments):
    """Scrape comments from HN thread"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = []
        
        for comment in soup.select(".commtext")[:max_comments]:
            text = ' '.join(comment.stripped_strings)
            text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text.split()) > 4:  # Only meaningful comments
                comments.append(text)
        return comments
    except Exception as e:
        st.warning(f"Couldn't scrape {url}: {str(e)}")
        return []

def analyze_sentiment(texts):
    """Analyze sentiment with TextBlob"""
    results = []
    for text in texts:
        analysis = TextBlob(text)
        pol = analysis.sentiment.polarity
        sent = "positive" if pol > 0.1 else "negative" if pol < -0.1 else "neutral"
        results.append({
            "comment": text[:200] + "..." if len(text) > 200 else text,
            "sentiment": sent,
            "polarity": round(pol, 3),
            "subjectivity": round(analysis.sentiment.subjectivity, 3)
        })
    return pd.DataFrame(results)

if submitted and keyword:
    with st.spinner(f"Searching HN for '{keyword}'..."):
        thread_urls = search_hn(keyword)[:5]
        
    if not thread_urls:
        st.warning("No discussions found. Try a different keyword.")
        st.stop()
        
    st.success(f"Found {len(thread_urls)} discussions about '{keyword}'")
    
    all_comments = []
    for url in thread_urls:
        comments = scrape_hn_comments(url, max_comments//len(thread_urls))
        all_comments.extend(comments)
        st.write(f"ℹ️ Scraped {len(comments)} comments from [thread]({url})")
        
    if not all_comments:
        st.error("No comments found in these threads")
        st.stop()
        
    with st.spinner("Analyzing sentiment..."):
        df = analyze_sentiment(all_comments)
    
    # Metrics
    st.subheader("📊 Sentiment Summary")
    pos = len(df[df.sentiment == "positive"])
    neg = len(df[df.sentiment == "negative"])
    
    cols = st.columns(3)
    cols[0].metric("Total Comments", len(df))
    cols[1].metric("Positive", f"{pos} ({pos/len(df):.0%})")
    cols[2].metric("Negative", f"{neg} ({neg/len(df):.0%})")
    
    # Visualizations
    st.subheader("📈 Distribution")
    st.bar_chart(df.sentiment.value_counts())
    
    st.subheader("🔥 Most Polarizing Comments")
    st.dataframe(
        df.sort_values("polarity", key=abs, ascending=False)[:10],
        column_config={
            "comment": "Comment",
            "sentiment": st.column_config.TextColumn("Sentiment"),
            "polarity": st.column_config.ProgressColumn(
                "Polarity",
                min_value=-1,
                max_value=1,
                format="%.2f"
            )
        }
    )