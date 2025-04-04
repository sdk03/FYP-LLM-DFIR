from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace this URL with your Ollama API endpoint
OLLAMA_API_URL = "http://192.168.88.234:11434/api/generate"



@app.route('/reply', methods=['POST'])
def reply():
    # Log the raw request data
    log_raw_request(request)
    
    # Check if the request is JSON and extract the message
    if request.is_json:
        #message = "("
        message = request.json.get('message')  # Expecting a JSON object with 'message' key
        #message += ")"
        #message += " i want my answer in strictly 3 words and each word separated by comma and each word represent 3 key information i.e. identity, asset, location from the message"

    else:
        return jsonify({'reply': 'Invalid request format. Please send JSON.'}), 400

    if message:
        # Call the Ollama API with the user's message
        response = get_ollama_response(message)
        if response:
            return jsonify({'reply': response})
        else:
            return jsonify({'reply': 'Error contacting Ollama model'}), 500
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
        print(req.data.decode('utf-8'))  # Decode bytes to string
    else:
        print("No body data received.")

def get_ollama_response(user_message):
    # Define the system and user messages
#     system_message = (
#     "You are a digital forensic assistant that helps me extract information into 3 categories from any input: identity, "
#     "asset, and location. The definition of identity is: Any individual or entity that represents a person or their unique role."
#     "The definition of asset is: tangible or intangible items of value in the context."
#     "The definition of location is: any geographic or spatial reference."
#     "You reply to this in JSON format as follows strictly:\n"
#     "{\"identity\":\"xxx\", \"asset\":\"xxx\", \"location\":\"xxx\"}.\n"
#     "The xxx is replaced by your answer in text format.\n"
#     "DO NOT CHANGE THE FORMATTING IN ANY WAY WHATSOEVER. "
#     "If they are not available, you just reply with N/A and don't explain anything. "
#     "Make sure not to give anything other than JSON."
# )

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
    5. Validate the structure before responding. 

    You reply to this in JSON format as follows strictly:
    {"PERSON": "xxx","ORG": "xxx","GPE": "xxx","NORP": "xxx","DATE": "xxx","TIME": "xxx","MONEY": "xxx","PERCENT": "xxx","FAC": "xxx","PRODUCT": "xxx","WORK_OF_ART": "xxx","LANGUAGE": "xxx","EVENT": "xxx","LAW": "xxx","ORDINAL": "xxx","CARDINAL": "xxx","TAGS": "xxx"}
    The "xxx" is replaced by your answer in text format. 
    Failure to strictly adhere to this format will result in the output being unusable. Validate for correctness before replying and ensure there are no errors.
    """


    user_message = f"{user_message}"

    prompt = f"{system_message}\nUser: {user_message}"


    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": "gemma2:9b",
        "prompt": prompt,  # Use a single string as the prompt
        "format": "json",
        "stream": False
    }
    
    # Sending request to the Ollama API
    response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data))
    
    # Log the response from the Ollama API
    print("Ollama API Response Code:", response.status_code)
    if response.status_code == 200:
        response_data = response.json()
        print("Ollama API Response Data:", response_data)  # Log the response data
        return response_data.get("response", "")
    else:
        print("Error: Received response from Ollama API:", response.text)  # Log the error response
        return None

if __name__ == '__main__':
    app.run(port=8000)
