from flask import Flask, request, jsonify
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load model components
with open('model.pkl', 'rb') as f:
    vectorizer, fund_matrix, fund_meta = pickle.load(f)

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_funds():
    payload = request.get_json(force=True)
    goal = payload.get('goal', '')
    top_n = payload.get('n', 10)

    vec = vectorizer.transform([goal])
    sims = cosine_similarity(vec, fund_matrix).flatten()
    idxs = sims.argsort()[::-1][:top_n]

    recs = [
        {
            'ticker': fund_meta.index[i],
            'fund_name': fund_meta.iloc[i]['name'],
            'score': float(sims[i])
        }
        for i in idxs
    ]
    return jsonify({'recommendations': recs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)