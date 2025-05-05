import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Mutual Fund Recommender")

st.title("Mutual Fund Recommender System")
st.write("Describe your investment goals and get personalized fund matches.")

goal = st.text_area(
    "Your investment goals:",
    "e.g. High dividend income with low expense ratio, or aggressive growth in technology sector, or balanced conservative fund with minimal volatility"
)
num = st.slider("Number of recommendations", 1, 20, 5)

if st.button("Get Recommendations"):
    if not goal:
        st.warning("Please enter your investment goals above.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                resp = requests.post(
                    'http://localhost:5000/recommend',
                    json={'goal': goal, 'n': num}
                )
                resp.raise_for_status()
                recs = resp.json().get('recommendations', [])
                if recs:
                    df = pd.DataFrame(recs)
                    st.table(df.set_index('ticker'))
                else:
                    st.info("No matching funds found.")
            except Exception as e:
                st.error(f"API error: {e}")