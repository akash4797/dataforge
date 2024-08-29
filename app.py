from flask import Flask, request, jsonify
from keyword_extraction import extract_keywords
from pdf_extraction import extract_text_from_pdf
from search_internet import search_duckduckgo
from search_internet import search_google

app = Flask(__name__)

@app.route('/momo-callback', methods=['POST'])
def momo_callback():
    try:
        data = request.get_json()
        print("Callback received:", data)
        return jsonify({'message': 'Callback received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_route():
    try:
        data = request.get_json()
        print("Received data:", data)

        if data is None:
            raise ValueError("No JSON data received")

        if 'text' not in data:
            raise ValueError("'text' key not found in JSON data")

        text = data['text']

        if not isinstance(text, str):
            raise ValueError("'text' should be a string")


        keywords = extract_keywords(text)

        if keywords is None:
            raise ValueError("Keyword extraction returned None")

        return jsonify({'keywords': keywords}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract_text_from_pdf', methods=['POST'])
def extract_text_from_pdf_route():
    try:
        print("main request",request.files)
        if 'file' not in request.files:
            raise ValueError("No file part in the request")

        file = request.files['file']

        if file.filename == '':
            raise ValueError("No selected file")

        if not file.filename.endswith('.pdf'):
            raise ValueError("File is not a PDF")

        # Save the uploaded file to a temporary location
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        # Extract text from the PDF
        text = extract_text_from_pdf(file_path)

        return jsonify({'text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/searchweb', methods=['GET'])
def search_duckduckgo_route():
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data received")

        if 'query' not in data:
            raise ValueError("'query' key not found in JSON data")

        query = data['query']

        if not isinstance(query, str):
            raise ValueError("'query' should be a string")

        # Perform DuckDuckGo search using the function from duckduckgo_search.py
        results = search_google(query)

        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3200)
