from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"

# OpenAI API endpoint
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/reply', methods=['POST'])
def reply():
    # Log the raw request data
    log_raw_request(request)
    
    # Check if the request is JSON and extract the message
    if request.is_json:
        message = request.json.get('message')
    else:
        return jsonify({'reply': 'Invalid request format. Please send JSON.'}), 400

    if message:
        # Call the ChatGPT-4 API with the user's message
        response = get_chatgpt_response(message)
        if response:
            return jsonify({'reply': response})
        else:
            return jsonify({'reply': 'Error contacting ChatGPT-4 API'}), 500
    else:
        return jsonify({'reply': 'No message received'}), 400

def log_raw_request(req):
    # Log headers
    print("Headers:")
    for key, value in req.headers.items():
        print(f"{key}: {value}")
    
    # Log the raw body of the request
    if req.data:
        print("Raw Body:")
        print(req.data.decode('utf-8'))
    else:
        print("No body data received.")


def extract_json(raw_content):
    start_index = raw_content.find('{')
    end_index = raw_content.rfind('}')
    if start_index != -1 and end_index != -1:
        return raw_content[start_index:end_index+1]
    else:
        return raw_content  # Fallback in case the expected JSON structure isn't found

# Example integration in your API response processing:
def get_chatgpt_response(user_message):
    system_message = """
        You are a expert digital forensic assistant that extracts information into strict JSON format according to the specified spaCy NER categories.

        The entity categories are:

        - **PERSON**: Any individual or entity that represents a person or their unique role.  
        - **ORG**: Any organization such as companies, agencies, or institutions.  
        - **GPE**: Geopolitical entities such as countries, cities, or regions.  
        - **NORP**: Nationalities, religious or political groups.  
        - **DATE**: Calendar dates or ranges.  
        - **TIME**: Specific times of the day or durations.  
        - **MONEY**: Monetary values.  
        - **PERCENT**: Percentages or rates.  
        - **FAC**: Buildings, airports, highways, or other man-made structures.  
        - **PRODUCT**: Products or goods, including inventions or creations.  
        - **WORK_OF_ART**: Works of art like books, music, films, etc.  
        - **LANGUAGE**: Any languages.  
        - **EVENT**: Events like sports events, concerts, festivals, etc.  
        - **LAW**: Legal documents or terms.  
        - **ORDINAL**: Ordinal numbers like 'first', 'second'.  
        - **CARDINAL**: Cardinal numbers like 'one', 'two', 'hundred'.  
        - **TAGS**: One or more keywords that capture the essence or context of the message in one word. These should summarize the message topic or intent, like “BANK” for banking transactions, “PURCHASE” for buying goods, or “SCHOOL” for education-related matters. Multiple tags can be provided if needed to better reflect the context of the message.

        ### Output Rules:
        1. Your response **must** only contain JSON formatted data.
        2. Each entity should be represented with its exact category label as provided.
        3. If an entity is not present, use "-" as the value. **Do not skip or leave blank.**
        4. Ensure no trailing commas or syntax errors in the JSON.
        5. Validate the structure before responding and ensure there are no errors.

        You reply to this in JSON format as follows strictly:
        {"PERSON": "xxx","ORG": "xxx","GPE": "xxx","NORP": "xxx","DATE": "xxx","TIME": "xxx","MONEY": "xxx","PERCENT": "xxx","FAC": "xxx","PRODUCT": "xxx","WORK_OF_ART": "xxx","LANGUAGE": "xxx","EVENT": "xxx","LAW": "xxx","ORDINAL": "xxx","CARDINAL": "xxx","TAGS": "xxx"}
        The "xxx" is replaced by your answer in text format. 
        Failure to strictly adhere to this format will result in the output being unusable. Validate for correctness before replying and ensure there are no errors.
        """

    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

    data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.0,
            "max_tokens": 500
        }
    
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        raw_content = response.json()['choices'][0]['message']['content']
        json_content = extract_json(raw_content)
        print("Processed JSON Response:", json_content)
        return json_content
    else:
        print("Error:", response.text)
        return None


if __name__ == '__main__':
    app.run(port=8000, debug=True)