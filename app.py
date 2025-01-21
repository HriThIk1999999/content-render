
# Importing necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import pickle

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the saved index (embedding and model) object
with open('/content/vector_store_index_last.pkl', 'rb') as file:
    loaded_index = pickle.load(file)

# Initialize the query engine
query_engine = loaded_index.as_query_engine(llm=llm)

# Define the API endpoint for search recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        user_query = data.get('query', '')

        if not user_query:
            return jsonify({"error": "Query parameter is required."}), 400

        response = query_engine.query(user_query)
        return jsonify({"query": user_query, "recommendations": str(response)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Default route for testing
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Search Recommendation API! Use the `/recommend` endpoint to get recommendations."

# Handle favicon requests
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

if __name__ == '__main__':
    # Start Ngrok tunnel
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")

    app.run()
