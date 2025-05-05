import os
import pandas as pd
import pickle
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optional: load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class MutualFundRecommender:
    def __init__(self,
                 api_url: str = 'https://financialmodelingprep.com/api/v3/symbol/available-mutual-funds',
                 api_key_env: str = 'FMP_API_KEY',
                 model_pickle: str = 'model.pkl'):
        """
        Fetch mutual fund data from Financial Modeling Prep API,
        build TF-IDF matrix of holdings_text, and pickle model.
        """
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError(f"Environment variable {api_key_env} not set.")

        # Fetch fund list (handles existing params)
        sep = '&' if '?' in api_url else '?'
        url = f"{api_url}{sep}apikey={api_key}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        # Load into DataFrame
        df = pd.DataFrame(data)
        # Use 'name' as text for TF-IDF; expand with other fields if available
        df['holdings_text'] = df['name']
        self.df = df.set_index('symbol')

        # Vectorize
        self.vectorizer = TfidfVectorizer(stop_words='english', min_df=5)
        self.fund_matrix = self.vectorizer.fit_transform(self.df['holdings_text'])

        # Persist model components
        with open(model_pickle, 'wb') as f:
            pickle.dump((self.vectorizer, self.fund_matrix, self.df[['name']]), f)

    def recommend(self, goal_text: str, top_n: int = 10) -> dict:
        """
        Transform goal_text to TF-IDF, compute cosine similarity,
        and return top_n recommendations.
        """
        vec = self.vectorizer.transform([goal_text])
        scores = cosine_similarity(vec, self.fund_matrix).flatten()
        idxs = scores.argsort()[::-1][:top_n]

        recs = []
        for idx in idxs:
            ticker = self.df.index[idx]
            recs.append({
                'ticker': ticker,
                'fund_name': self.df.iloc[idx]['name'],
                'score': float(scores[idx])
            })
        return {'recommendations': recs}

if __name__ == '__main__':
    MutualFundRecommender()