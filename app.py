from flask import Flask, request, jsonify
from keyword_extraction import extract_keywords
from pdf_extraction import extract_text_from_pdf
from search_internet import search_duckduckgo
from search_internet import search_google
from email_extraction import search_emails_for_multiple_companies

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

# New route for email extraction
@app.route('/search_emails', methods=['POST'])
def search_emails_route():
    try:
        data = request.get_json()
        
        # Check if 'company_names' exists in the input data
        if data is None or 'company_names' not in data:
            raise ValueError("'company_names' key not found in the JSON data")
        
        company_names = data['company_names']
        
        # Ensure 'company_names' is a list of strings
        if not isinstance(company_names, list) or not all(isinstance(name, str) for name in company_names):
            raise ValueError("'company_names' must be a list of strings")

        # Call the function to search emails for multiple companies
        results = search_emails_for_multiple_companies(company_names)
        
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3200)
