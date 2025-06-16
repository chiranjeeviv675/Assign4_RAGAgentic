from flask import Flask, request, jsonify
from flask_cors import CORS
from agentic_rag_simplified import app

api = Flask(__name__)
CORS(api)

@api.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        question = data.get('question')
        if not question:
            return jsonify({'error': 'Question is required'}), 400

        final_state = app.invoke({"question": question})
        if not final_state:
            return jsonify({'error': 'Failed to process question'}), 500
            
        response = {
            'question': final_state.get('question', ''),
            'answer': final_state.get('answer', ''),
            'critique': final_state.get('critique', '')
        }
        return jsonify(response), 200
    except Exception as e:
        print(f'Error processing request: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    api.run(debug=True)