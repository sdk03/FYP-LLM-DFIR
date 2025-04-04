from flask import Flask, jsonify
import pickle
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FILE_PATH_LLM = 'llm-response.pkl'
FILE_PATH_OG = 'cleaned_data.pkl'

def load_data():
    """Loads data from pickle files and formats it for JSON."""
    with open(FILE_PATH_LLM, 'rb') as file:
        data = pickle.load(file)

    with open(FILE_PATH_OG, 'rb') as fileOG:
        raw_data = pickle.load(fileOG)

    nodes = []
    links = []

    for index, i in enumerate(data):
        response = json.loads(i['response'])  # Convert the string to a dictionary
        window_start = i['window_start']
        window_end = i['window_end']
        
        original_data = raw_data[index]
        # Format messages with pipes and include all four fields
        formatted_og_data = "\n".join([
            f"{msg['Date/Time']}|{msg['Message Type']}|{msg['Text']}|{msg['From Phone Number']}"
            for msg in original_data["messages"]
        ])

        # Append node
        nodes.append({
            "id": index,
            "summary": response['window_summary'],
            "window_start": window_start,
            "window_end": window_end,
            "original_messages": formatted_og_data
        })

        # Create links between consecutive windows
        if index > 0:
            links.append({"source": index - 1, "target": index - 1})

    return {"nodes": nodes, "links": links}

@app.route('/get_data')
def get_data():
    """API endpoint to serve data dynamically."""
    return jsonify(load_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)