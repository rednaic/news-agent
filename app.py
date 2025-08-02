import streamlit as st
import openai
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extract article text from a URL
def extract_article_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join(p.get_text() for p in paragraphs if p.get_text())
    except Exception as e:
        return f"Error extracting article: {e}"

# Generate analysis for a section
def analyze_section(instruction, article):
    prompt = f"""
    ARTICLE:
    {article}

    TASK: {instruction} (Respond in concise bullet points. Keep total length under 100 words.)
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit app
st.set_page_config(page_title="News Insight Agent", layout="wide")
st.title("🧠 News Analysis Agent")

url = st.text_input("Enter a news article URL:")

if st.button("Analyze"):
    if not url.strip():
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Extracting and analyzing article..."):
            article = extract_article_text(url)

            if article.startswith("Error"):
                st.error(article)
            else:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("🧭 Bias Assessment")
                    st.markdown(analyze_section("Assess whether the article is biased or neutral.", article))

                with col2:
                    st.subheader("🏛️ Persuasion of Reporter")
                    st.markdown(analyze_section("What political perspective does this article reflect: left, right, or center?", article))

                with col3:
                    st.subheader("🔗 Other Views")
                    st.markdown(analyze_section("Suggest 2–3 credible alternative sources with links that cover the same story.", article))

                st.markdown("---")
                st.subheader("🧾 Full Article Analysis")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Summary**")
                    st.markdown(analyze_section("Summarize the article using 3–4 concise bullet points with emojis.", article))

                    st.markdown("**Narrative & Framing**")
                    st.markdown(analyze_section("What is the main narrative or message in this article? What framing is used?", article))

                with col2:
                    st.markdown("**Tone & Bias**")
                    st.markdown(analyze_section("Analyze the tone and any ideological bias.", article))

                    st.markdown("**Missing Facts**")
                    st.markdown(analyze_section("What relevant facts or perspectives are missing or underrepresented?", article))

                with col3:
                    st.markdown("**Alternative Viewpoints**")
                    st.markdown(analyze_section("Offer two other viewpoints that could be taken.", article))

                    st.markdown("**Misinterpretation Risk**")
                    st.markdown(analyze_section("How could the article be misinterpreted or weaponized?", article))

                st.success("Analysis complete. Scroll up to review.")