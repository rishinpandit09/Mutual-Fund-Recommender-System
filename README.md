```markdown
# README.md

**Mutual Fund Recommender System**

Now fetching fund data dynamically from the free Financial Modeling Prep API.

---

## API Choice

We use the Financial Modeling Prep (FMP) Mutual Fund endpoint:
```

https://financialmodelingprep.com/api/v3/mutual-fund/list?apikey=YOUR_KEY

````

It provides over 14,000 funds with metadata like `symbol`, `fundName`, `category`, etc.

## Getting an API Key
1. Sign up for a free account at https://financialmodelingprep.com.
2. Retrieve your API key from your profile dashboard.
3. Export it:

```bash
export FMP_API_KEY="your_api_key_here"
````

## Tech Stack

- **Python** 3.8+
- **Flask** for API
- **Pandas** for data handling
- **Scikit-learn** for TF-IDF & similarity
- **Streamlit** for interactive UI
- **Requests** for HTTP calls

## Setup Instructions

```bash
# 1. Clone repository and remove existing git history
git clone <your-repo-url> mutual_fund_recommender_system && cd mutual_fund_recommender_system
rm -rf .git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
export FMP_API_KEY="<your_api_key>"

# 4. Build the recommendation model (fetch & pickle data)
python recommender.py

# 5. Start the Flask API server
python app.py

# 6. Launch the Streamlit UI in a new terminal
streamlit run streamlit_app.py
```

## Usage

- Open your browser to the Streamlit UI at `http://localhost:8501`.
- Enter your investment goals in the text box.
- Adjust the recommendation count slider and click **Get Recommendations**.
- View the personalized list of fund tickers, names, and similarity scores.

Enjoy automated mutual fund suggestions powered by TF‑IDF and cosine similarity via FMP’s free API!"```}]}
